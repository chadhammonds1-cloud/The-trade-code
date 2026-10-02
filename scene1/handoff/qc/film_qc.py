#!/usr/bin/env python3
"""Frame-by-frame automated QC for AI-generated shot clips.

Every frame of every clip is measured. Audio is transcribed and pitch-tracked.
Output: qc_frames.csv (one row per frame), qc_report.json (flags), flag images.

Usage: python3 film_qc.py [08=V08b ...]   (swap a shot for an alternate take)
Needs: shots.py manifest (shot id, clip, expected lines with speaker, storyboard still)

Checks
  PICTURE (every frame)
    black        frame mean brightness below 12/255
    freeze       picture stops changing for >= 1.5 s
    hidden_cut   a hard cut inside what should be one continuous shot
    glitch       sudden single-frame jump that is not a cut (morph / pop)
    drift        frame content drifts far from the approved storyboard still
    presence     a character who should be in frame is missing (costume colour)
    order        screen order broken (Vessa must stay left of Tavique)
  CUTS (between shots)
    light_jump   brightness / colour cast jumps across a cut in the same room
  AUDIO (per clip)
    words        transcript vs script, letter error rate > 10%
    voice        speaker ID: each line vs that character's other lines (<0.80, or closer to someone else)
                 (pitch is recorded but is NOT a flag: children's pitch swings with emotion)
    bed          sustained held note (music) or loud unvoiced noise (ambience) between lines
    clip_peak    audio hitting 0 dBFS
"""
import json, os, subprocess, sys, re, math
import numpy as np, cv2
from skimage.metrics import structural_similarity as ssim

sys.path.insert(0, os.path.dirname(__file__))
from shots import SHOTS, VISIBLE
OVERRIDE = dict(a.split("=") for a in sys.argv[1:])  # e.g. 08=V08b

CLIPS = "/home/claude/trade/s1v"
STILLS = "/home/claude/trade/s1"
VOICES = {"TAV": "/home/claude/trade/voices/tavik.wav",
          "VES": "/home/claude/trade/voices/vessa.wav",
          "DAD": "/home/claude/trade/voices/dad.wav"}
OUT = os.environ.get("QC_OUT", "/home/claude/trade/qc/out")
os.makedirs(OUT, exist_ok=True)
FPS = 24

# ---------- costume colour masks (OpenCV HSV: H 0-180) ----------
def masks(bgr):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    tav = (H >= 112) & (H <= 124) & (S >= 95) & (V >= 55) & (V <= 160)   # royal-blue hoodie
    ves = (H >= 95) & (H <= 105) & (S >= 90) & (V >= 100) & (V <= 215)   # light-blue hoodie
    return tav, ves

def centroid_frac(m, min_px):
    n = int(m.sum())
    if n < min_px:
        return n, None
    xs = np.nonzero(m)[1]
    return n, float(xs.mean() / m.shape[1])

# ---------- CLIP ----------
import torch, open_clip
torch.set_num_threads(2)
MODEL, _, PRE = open_clip.create_model_and_transforms("ViT-B-32", pretrained="laion2b_s34b_b79k")
MODEL.eval()
from PIL import Image
def clip_embed(bgr_list):
    ims = torch.stack([PRE(Image.fromarray(cv2.cvtColor(b, cv2.COLOR_BGR2RGB))) for b in bgr_list])
    with torch.no_grad():
        e = MODEL.encode_image(ims)
    return torch.nn.functional.normalize(e, dim=-1).numpy()

# ---------- audio helpers ----------
import parselmouth
def median_pitch(wav, t0=None, t1=None):
    snd = parselmouth.Sound(wav)
    if t0 is not None:
        snd = snd.extract_part(from_time=max(0, t0), to_time=min(snd.duration, t1))
    p = snd.to_pitch(pitch_floor=75, pitch_ceiling=600).selected_array["frequency"]
    p = p[p > 0]
    return float(np.median(p)) if len(p) > 10 else None

def norm_words(t):
    t = t.lower().replace("’", "'")
    return re.sub(r"[^a-z' ]", " ", t).split()

from faster_whisper import WhisperModel
WM = WhisperModel("small", device="cpu", compute_type="int8")
import jiwer

REF_PITCH = {k: median_pitch(v) for k, v in VOICES.items()}

def audio_checks(mp4, lines):
    wav = f"{OUT}/_a.wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", mp4, "-ac", "1", "-ar", "24000", wav], check=True)
    segs, _ = WM.transcribe(wav, language="en", word_timestamps=True)
    words = [w for s in segs for w in s.words]
    heard = " ".join(w.word.strip() for w in words)
    expected = " ".join(t for _, t in lines)
    # compare letters only, so "paint brush" vs "paintbrush" is not an error
    wer = jiwer.cer("".join(norm_words(expected)), "".join(norm_words(heard)))
    # split heard words across expected lines by word count, then measure each speaker's pitch
    counts = [len(norm_words(t)) for _, t in lines]
    tot = sum(counts); per_line = []; i = 0
    for (spk, txt), c in zip(lines, counts):
        k = max(1, round(c / tot * len(words))) if words else 0
        chunk = words[i:i + k]; i += k
        if not chunk:
            per_line.append({"speaker": spk, "pitch": None}); continue
        t0, t1 = chunk[0].start, chunk[-1].end
        p = median_pitch(wav, t0, t1)
        ref = REF_PITCH[spk]
        dev = None if (p is None or ref is None) else (p - ref) / ref
        per_line.append({"speaker": spk, "t0": round(t0, 2), "t1": round(t1, 2),
                         "pitch": None if p is None else round(p), "ref": round(ref),
                         "dev": None if dev is None else round(dev, 3)})
    # gaps between words: what is left when nobody talks
    snd = parselmouth.Sound(wav); dur = snd.duration
    speech = [(max(0, w.start - 0.15), w.end + 0.15) for w in words]
    gaps = []; cur = 0.0
    for a, b in sorted(speech):
        if a - cur > 0.5: gaps.append((cur, a))
        cur = max(cur, b)
    if dur - cur > 0.5: gaps.append((cur, dur))
    y = snd.values[0]; sr = snd.sampling_frequency
    gap_db = []
    for a, b in gaps:
        seg = y[int(a * sr):int(b * sr)]
        if len(seg) < sr * 0.3: continue
        rms = np.sqrt(np.mean(seg ** 2)) + 1e-9
        # tonality: a music bed shows narrow persistent spectral peaks
        spec = np.abs(np.fft.rfft(seg * np.hanning(len(seg))))
        flat = float(np.exp(np.mean(np.log(spec + 1e-12))) / (np.mean(spec) + 1e-12))
        sub = snd.extract_part(from_time=a, to_time=b)
        pp = sub.to_pitch(pitch_floor=60, pitch_ceiling=900).selected_array["frequency"]
        vf = float((pp > 0).mean()) if len(pp) else 0.0
        vv = pp[pp > 0]
        # longest run of steady pitch (within 3%) = a held note
        run = best = 0
        for k in range(1, len(pp)):
            run = run + 1 if (pp[k] > 0 and pp[k-1] > 0 and abs(pp[k] - pp[k-1]) / pp[k-1] < 0.03) else 0
            best = max(best, run)
        gap_db.append({"t0": round(a, 2), "t1": round(b, 2), "db": round(20 * math.log10(rms), 1), "flatness": round(flat, 3),
                       "voiced": round(vf, 2), "f0": None if not len(vv) else round(float(np.median(vv))), "held_note_s": round(best * 0.01, 2)})
    peak = float(np.max(np.abs(y)))
    return {"heard": heard, "expected": expected, "wer": round(wer, 3), "lines": per_line,
            "gaps": gap_db, "peak_dbfs": round(20 * math.log10(peak + 1e-9), 2), "duration": round(dur, 2)}

# ---------- main per-clip pass ----------
rows = []; report = {"ref_pitch": {k: round(v) for k, v in REF_PITCH.items()}, "shots": []}
film_t = 0.0
for sid, clip, lines, still in SHOTS:
    clip = OVERRIDE.get(sid, clip)
    mp4 = f"{CLIPS}/{clip}.mp4"
    cap = cv2.VideoCapture(mp4)
    frames_small, frames_clip, idx = [], [], 0
    still_img = cv2.imread(f"{STILLS}/{still}.png")
    still_emb = clip_embed([cv2.resize(still_img, (640, 360))])[0]
    prev_g = prev_h = None
    shot_rows = []
    batch = []
    while True:
        ok, fr = cap.read()
        if not ok: break
        sm = cv2.resize(fr, (320, 180), interpolation=cv2.INTER_AREA)
        g = cv2.cvtColor(sm, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(sm, cv2.COLOR_BGR2HSV)
        h = cv2.calcHist([hsv], [0, 1], None, [30, 16], [0, 180, 0, 256]); cv2.normalize(h, h)
        tav_m, ves_m = masks(cv2.resize(fr, (640, 360), interpolation=cv2.INTER_AREA))
        tav_n, tav_x = centroid_frac(tav_m, 400)
        ves_n, ves_x = centroid_frac(ves_m, 400)
        r = {"shot": sid, "frame": idx, "t": round(idx / FPS, 3), "film_t": round(film_t + idx / FPS, 3),
             "luma": float(g.mean()),
             "diff": None if prev_g is None else float(np.mean(cv2.absdiff(g, prev_g))),
             "ssim": None if prev_g is None else float(ssim(g, prev_g)),
             "hist": None if prev_h is None else float(cv2.compareHist(h, prev_h, cv2.HISTCMP_CORREL)),
             "tav_px": tav_n, "tav_x": tav_x, "ves_px": ves_n, "ves_x": ves_x}
        shot_rows.append(r); batch.append(cv2.resize(fr, (320, 180)))
        prev_g, prev_h = g, h; idx += 1
        if idx in (1,) or idx % 999999 == 0: pass
    cap.release()
    # CLIP for every frame, in batches
    embs = []
    for i in range(0, len(batch), 32):
        embs.append(clip_embed(batch[i:i + 32]))
    embs = np.vstack(embs)
    for i, r in enumerate(shot_rows):
        r["clip_still"] = float(embs[i] @ still_emb)
        r["clip_prev"] = None if i == 0 else float(embs[i] @ embs[i - 1])
    rows += shot_rows
    n = len(shot_rows); dur = n / FPS
    flags = []
    L = np.array([r["luma"] for r in shot_rows])
    D = np.array([r["diff"] or 0 for r in shot_rows])
    SS = np.array([r["ssim"] if r["ssim"] is not None else 1 for r in shot_rows])
    HC = np.array([r["hist"] if r["hist"] is not None else 1 for r in shot_rows])
    CS = np.array([r["clip_still"] for r in shot_rows])
    CP = np.array([r["clip_prev"] if r["clip_prev"] is not None else 1 for r in shot_rows])
    # black
    for i in np.nonzero(L < 12)[0]: flags.append({"type": "black", "frame": int(i)})
    # freeze: run of near-identical frames
    run = 0
    for i in range(1, n):
        run = run + 1 if D[i] < 0.15 else 0
        if run == int(1.5 * FPS): flags.append({"type": "freeze", "frame": int(i - run), "len_s": 1.5})
    # hidden cut vs glitch. A cut = the picture's meaning jumps (CLIP) or colour and structure both jump.
    # A glitch = a structural jump well below the local norm while the meaning stays (a pop / morph).
    for i in range(1, n):
        lo, hi = max(1, i - 12), min(n, i + 13)
        local = np.median(SS[lo:hi])
        if CP[i] < 0.80 or (HC[i] < 0.6 and SS[i] < 0.45):
            flags.append({"type": "hidden_cut", "frame": i, "t": round(i / FPS, 2), "clip_prev": round(float(CP[i]), 3), "ssim": round(float(SS[i]), 3)})
        elif SS[i] < local - 0.25 and CP[i] < 0.92:
            flags.append({"type": "glitch", "frame": i, "t": round(i / FPS, 2), "ssim": round(float(SS[i]), 3), "local": round(float(local), 3), "clip_prev": round(float(CP[i]), 3)})
    # drift from storyboard still (compare to this shot's own first second as baseline)
    base = float(np.median(CS[:FPS]))
    bad_i = [i for i in range(n) if CS[i] < base - 0.12]
    if bad_i:
        w = int(np.argmin(CS))
        flags.append({"type": "drift", "first_frame": bad_i[0], "t": round(bad_i[0] / FPS, 2), "worst_frame": w, "clip_still": round(float(CS[w]), 3), "baseline": round(base, 3), "frames": len(bad_i)})
    # presence (need >= 1 s continuous absence) and screen order
    exp = VISIBLE[sid]
    for who, key in (("T", "tav_px"), ("V", "ves_px")):
        if who in exp:
            miss = [r[key] < 400 for r in shot_rows]; run = 0
            for i, m in enumerate(miss):
                run = run + 1 if m else 0
                if run == FPS:
                    flags.append({"type": "presence", "who": {"T": "Tavique", "V": "Vessa"}[who], "frame": i - run + 1}); break
    bad = [r for r in shot_rows if r["tav_x"] is not None and r["ves_x"] is not None and r["ves_x"] > r["tav_x"]]
    if len(bad) > FPS // 2:
        flags.append({"type": "order", "frame": bad[0]["frame"], "frames_bad": len(bad)})
    audio = audio_checks(mp4, lines)
    # names must be said right: a name that is close but not equal ("Tavreak" for "Tavik") is a fail
    NAMES = {"tavique": {"tavik", "tavick", "tavic"}, "tavik": {"tavik", "tavick", "tavic"}}
    exp_names = [w for w in norm_words(audio["expected"]) if w in NAMES]
    heard_tav = [w for w in norm_words(audio["heard"]) if w.startswith("tav")]
    for i, w in enumerate(exp_names):
        got = heard_tav[i] if i < len(heard_tav) else None
        if got not in NAMES[w]:
            flags.append({"type": "name", "expected": "tuh-VIK", "heard": got})
    if audio["wer"] > 0.10: flags.append({"type": "words", "letter_error_rate": audio["wer"]})
    for ln in audio["lines"]:
        if ln.get("dev") is not None and abs(ln["dev"]) > 0.25:
            ln["pitch_note"] = "pitch far from sample; speaker-ID check decides"
    for gp in audio["gaps"]:
        long = gp["t1"] - gp["t0"]
        if gp["db"] > -45 and (gp["held_note_s"] >= 0.6 or (gp["voiced"] < 0.15 and long >= 1.5 and gp["db"] > -35)):
            flags.append({"type": "bed", **gp})
    if audio["peak_dbfs"] > -0.3: flags.append({"type": "clip_peak", "peak": audio["peak_dbfs"]})
    report["shots"].append({"shot": sid, "clip": clip, "frames": n, "seconds": round(dur, 2), "film_start": round(film_t, 2),
                            "luma_first": round(float(L[:3].mean()), 1), "luma_last": round(float(L[-3:].mean()), 1),
                            "clip_still_baseline": round(base, 3), "clip_still_min": round(float(CS.min()), 3),
                            "audio": audio, "flags": flags})
    film_t += dur
    print(f"shot {sid}: {n} frames, {len(flags)} flags", flush=True)

# voice identity: speaker embeddings, each line vs that character's in-episode voice (leave-one-out)
from resemblyzer import VoiceEncoder, preprocess_wav
import soundfile as sf
ENC = VoiceEncoder("cpu")
embs = []
for s in report["shots"]:
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{CLIPS}/{s['clip']}.mp4", "-ac", "1", "-ar", "16000", f"{OUT}/_v.wav"], check=True)
    y, sr = sf.read(f"{OUT}/_v.wav")
    for ln in s["audio"]["lines"]:
        if ln.get("t0") is None or ln["t1"] - ln["t0"] < 0.8: continue
        e = ENC.embed_utterance(preprocess_wav(y[int(ln["t0"] * sr):int(ln["t1"] * sr)], source_sr=sr))
        embs.append((s, ln, e))
for s, ln, e in embs:
    own = [x for (s2, l2, x) in embs if l2["speaker"] == ln["speaker"] and x is not e]
    if not own: continue
    c = np.mean(own, 0); c /= np.linalg.norm(c)
    ln["voice_sim"] = round(float(e @ c), 3)
    others = {}
    for spk in {l2["speaker"] for (_, l2, _) in embs} - {ln["speaker"]}:
        o = np.mean([x for (_, l2, x) in embs if l2["speaker"] == spk], 0); o /= np.linalg.norm(o)
        others[spk] = round(float(e @ o), 3)
    ln["voice_sim_others"] = others
    closer = [k for k, v in others.items() if v > ln["voice_sim"]]
    if ln["voice_sim"] < 0.80 or closer:
        s["flags"].append({"type": "voice", "speaker": ln["speaker"], "t0": ln["t0"], "sim_own": ln["voice_sim"], "closer_to": closer})

# cut boundaries: lighting continuity between consecutive shots (same room, same time of day)
cuts = []
for a, b in zip(report["shots"], report["shots"][1:]):
    jump = abs(a["luma_last"] - b["luma_first"])
    cuts.append({"from": a["shot"], "to": b["shot"], "luma_jump": round(jump, 1)})
    if jump > 25:
        b["flags"].append({"type": "light_jump", "from": a["shot"], "jump": round(jump, 1)})
report["cuts"] = cuts
report["total_frames"] = len(rows)

import csv
with open(f"{OUT}/qc_frames.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
json.dump(report, open(f"{OUT}/qc_report.json", "w"), indent=1)
print("frames:", len(rows))
