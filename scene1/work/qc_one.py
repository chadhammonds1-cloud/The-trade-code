#!/usr/bin/env python3
"""Per-clip QC for one Scene 1 draft (adapted from handoff qc/film_qc.py to run one shot at a time).

Usage: python3 qc_one.py <shot id e.g. 01> <clip.mp4> <still.png> [prev_clip.mp4]
Writes: frames/<id>_sheet.jpg (2 fps eye-pass sheet), frames/<id>_last.png, frames/<id>_first.png,
        frames/cut_<prev>_<id>.jpg (cut pair) and prints a JSON report.
"""
import json, os, subprocess, sys, re
import numpy as np, cv2
from skimage.metrics import structural_similarity as ssim

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lines import LINES, VISIBLE
VOICES = {"TAV": f"{HERE}/../TheTrade_Scene1_handoff/voices/tavik.wav",
          "VES": f"{HERE}/../TheTrade_Scene1_handoff/voices/vessa.wav",
          "DAD": f"{HERE}/../TheTrade_Scene1_handoff/voices/dad.wav"}
FR = f"{HERE}/frames"; os.makedirs(FR, exist_ok=True)
sid, mp4, still = sys.argv[1], sys.argv[2], sys.argv[3]
prev = sys.argv[4] if len(sys.argv) > 4 else None
flags = []

def masks(bgr):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV); H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    tav = (H >= 112) & (H <= 124) & (S >= 95) & (V >= 55) & (V <= 160)
    ves = (H >= 95) & (H <= 105) & (S >= 90) & (V >= 100) & (V <= 215)
    return tav, ves

try:
    import torch, open_clip
    from PIL import Image
    torch.set_num_threads(4)
    M, _, PRE = open_clip.create_model_and_transforms("ViT-B-32", pretrained="laion2b_s34b_b79k"); M.eval()
    def emb(bgrs):
        ims = torch.stack([PRE(Image.fromarray(cv2.cvtColor(b, cv2.COLOR_BGR2RGB))) for b in bgrs])
        with torch.no_grad(): e = M.encode_image(ims)
        return torch.nn.functional.normalize(e, dim=-1).numpy()
except Exception as ex:
    emb = None; print("CLIP unavailable:", ex, file=sys.stderr)

cap = cv2.VideoCapture(mp4); fps = cap.get(cv2.CAP_PROP_FPS) or 24
frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(f)
n = len(frames); dur = n / fps
cv2.imwrite(f"{FR}/{sid}_first.png", frames[0]); cv2.imwrite(f"{FR}/{sid}_last.png", frames[-1])

# ---- picture ----
G = [cv2.cvtColor(cv2.resize(f, (320, 180)), cv2.COLOR_BGR2GRAY) for f in frames]
L = np.array([g.mean() for g in G])
D = np.array([0] + [np.mean(cv2.absdiff(G[i], G[i - 1])) for i in range(1, n)])
SS = np.array([1] + [ssim(G[i], G[i - 1]) for i in range(1, n)])
if emb:
    E = np.vstack([emb([cv2.resize(f, (320, 180)) for f in frames[i:i + 32]]) for i in range(0, n, 32)])
    se = emb([cv2.resize(cv2.imread(still), (640, 360))])[0]
    CS = E @ se; CP = np.array([1] + [float(E[i] @ E[i - 1]) for i in range(1, n)])
else:
    CS = CP = None
for i in np.nonzero(L < 12)[0][:3]: flags.append({"type": "black", "t": round(i / fps, 2)})
run = 0
for i in range(1, n):
    run = run + 1 if D[i] < 0.15 else 0
    if run == int(1.5 * fps): flags.append({"type": "freeze", "t": round((i - run) / fps, 2)})
for i in range(1, n):
    local = np.median(SS[max(1, i - 12):min(n, i + 13)])
    cp = CP[i] if CP is not None else 1
    if (CP is not None and cp < 0.80) or (SS[i] < 0.35 and D[i] > 25):
        flags.append({"type": "hidden_cut", "t": round(i / fps, 2), "clip_prev": round(float(cp), 3), "ssim": round(float(SS[i]), 3)})
    elif SS[i] < local - 0.25 and cp < 0.92:
        flags.append({"type": "glitch", "t": round(i / fps, 2), "ssim": round(float(SS[i]), 3)})
drift = None
if CS is not None:
    base = float(np.median(CS[:int(fps)])); w = int(np.argmin(CS))
    drift = {"baseline": round(base, 3), "min": round(float(CS[w]), 3), "worst_t": round(w / fps, 2)}
    if CS[w] < base - 0.12: flags.append({"type": "drift", **drift})
exp = VISIBLE.get(sid, "")
for who, idx in (("T", 0), ("V", 1)):
    if who in exp:
        miss = [int(masks(cv2.resize(f, (640, 360)))[idx].sum()) < 400 for f in frames[::2]]
        r = 0
        for i, m in enumerate(miss):
            r = r + 1 if m else 0
            if r == int(fps / 2):
                flags.append({"type": "presence", "who": who, "t": round((i - r + 1) * 2 / fps, 2)}); break

# ---- eye-pass sheet at 2 fps ----
step = max(1, int(round(fps / 2))); picks = list(range(0, n, step))
th = [cv2.resize(frames[i], (320, 180)) for i in picks]
for k, i in enumerate(picks):
    cv2.putText(th[k], f"{i / fps:.1f}s", (6, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
cols = 6; rows = (len(th) + cols - 1) // cols
th += [np.zeros_like(th[0])] * (rows * cols - len(th))
cv2.imwrite(f"{FR}/{sid}_sheet.jpg", np.vstack([np.hstack(th[r * cols:(r + 1) * cols]) for r in range(rows)]), [cv2.IMWRITE_JPEG_QUALITY, 70])

# ---- audio ----
import parselmouth, jiwer
wav = f"{FR}/{sid}.wav"
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", mp4, "-ac", "1", "-ar", "16000", wav], check=True)
from pocketsphinx import Decoder
import wave
class W:  # word with start/end seconds, like faster-whisper's
    def __init__(s, word, start, end): s.word, s.start, s.end = word, start, end
dec = Decoder(samprate=16000)
# names: the right sound and the known wrong ones, so a wrong name is heard as wrong
for w_, ph in (("tavik", "T AH V IH K"), ("tuhvik", "T AH V IH K"), ("tavreak", "T AE V R IY K"), ("taviki", "T AH V IY K IY"), ("taveek", "T AH V IY K"), ("tavique", "T AE V IY K")):
    dec.add_word(w_, ph, True)
wf = wave.open(wav); raw = wf.readframes(wf.getnframes())
dec.start_utt(); dec.process_raw(raw, full_utt=True); dec.end_utt()
words = [W(sg.word.split("(")[0], sg.start_frame / 100, sg.end_frame / 100) for sg in dec.seg()
         if not sg.word.startswith("<") and sg.word not in ("[NOISE]", "<sil>", "<s>", "</s>") and not sg.word.startswith("[")]
heard = " ".join(w.word.strip() for w in words)
lines = LINES[sid]
nw = lambda t: re.sub(r"[^a-z' ]", " ", t.lower().replace("’", "'")).split()
expected = " ".join(t for _, t in lines)
NAME = {"tavique", "tavik", "tuh", "vik"}
exp_n = [w for w in nw(expected) if w not in NAME]
got_n = [w for w in nw(heard) if not w.startswith("tav") and w not in ("tuh", "vik", "vick", "tavik")]
cer = jiwer.cer("".join(exp_n), "".join(got_n))
if cer > 0.10: flags.append({"type": "words", "cer": round(cer, 3)})
n_names = sum(1 for w in nw(expected) if w in ("tavique", "tavik"))
heard_names = [w.word.strip().lower().strip(".,!?") for w in words if re.match(r"^\W*(tav|tuh|ta)", w.word.strip().lower())]
OKN = {"tavik", "tuhvik"}
if n_names:
    bad = [h for h in heard_names if h not in OKN]
    if len(heard_names) < n_names or bad: flags.append({"type": "name", "heard": heard_names, "expected_count": n_names})
# speech timing
first_word = words[0].start if words else None; last_word = words[-1].end if words else None
snd = parselmouth.Sound(wav); y = snd.values[0]; sr = snd.sampling_frequency
peak = 20 * np.log10(np.max(np.abs(y)) + 1e-9)
if peak > -0.3: flags.append({"type": "clip_peak", "peak": round(peak, 2)})
sp = [(max(0, w.start - 0.15), w.end + 0.15) for w in words]; gaps = []; cur = 0.0
for a, b in sorted(sp):
    if a - cur > 0.5: gaps.append((cur, a))
    cur = max(cur, b)
if snd.duration - cur > 0.5: gaps.append((cur, snd.duration))
pitch = snd.to_pitch(pitch_floor=75, pitch_ceiling=600)
for a, b in gaps:
    seg = y[int(a * sr):int(b * sr)]
    if len(seg) < sr * 0.3: continue
    db = 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9)
    f0 = np.array([pitch.get_value_at_time(t) or 0 for t in np.arange(a, b, 0.01)]); f0 = np.nan_to_num(f0)
    held = 0; best = 0
    for i in range(1, len(f0)):
        held = held + 1 if f0[i] > 0 and f0[i - 1] > 0 and abs(f0[i] - f0[i - 1]) / f0[i - 1] < 0.01 else 0
        best = max(best, held)
    if db > -45 and (best * 0.01 >= 0.6 or (b - a >= 1.5 and db > -35 and (f0 > 0).mean() < 0.15)):
        flags.append({"type": "bed", "t0": round(a, 2), "t1": round(b, 2), "db": round(db, 1), "held_s": best * 0.01})
# speaker ID vs locked samples: split heard words across expected lines by word count
voice = []
try:
    from resemblyzer import VoiceEncoder, preprocess_wav
    import soundfile as sf
    enc = VoiceEncoder("cpu")
    refs = {k: enc.embed_utterance(preprocess_wav(v)) for k, v in VOICES.items()}
    yy, ssr = sf.read(wav)
    counts = [len(nw(t)) for _, t in lines]; tot = sum(counts); i = 0
    for (spk, txt), c in zip(lines, counts):
        k = max(1, round(c / tot * len(words))); ch = words[i:i + k]; i += k
        if not ch or ch[-1].end - ch[0].start < 0.8: voice.append({"spk": spk, "note": "short"}); continue
        e = enc.embed_utterance(preprocess_wav(yy[int(ch[0].start * ssr):int(ch[-1].end * ssr)], source_sr=ssr))
        sims = {kk: round(float(e @ v), 3) for kk, v in refs.items()}
        best = max(sims, key=sims.get)
        voice.append({"spk": spk, "t0": round(ch[0].start, 2), "sims": sims})
        if best != spk: flags.append({"type": "voice", "spk": spk, "closer_to": best, "sims": sims})
except Exception as ex:
    voice = [f"speaker ID unavailable: {ex}"]

# ---- cut pair with previous shot ----
cut = None
if prev:
    pid = os.path.basename(prev).split("_")[0]
    a = cv2.imread(f"{FR}/{pid}_last.png"); b = frames[0]
    if a is not None:
        a2, b2 = cv2.resize(a, (640, 360)), cv2.resize(b, (640, 360))
        sheet = np.hstack([a2, np.full((360, 8, 3), 255, np.uint8), b2])
        cv2.imwrite(f"{FR}/cut_{pid}_{sid}.jpg", sheet)
        cut = {"pair": f"cut_{pid}_{sid}.jpg"}
        if emb:
            ea, eb = emb([a2, b2]); cut["clip_sim"] = round(float(ea @ eb), 3)
            if cut["clip_sim"] >= 0.88: flags.append({"type": "jump_cut_check", **cut})
        pj = json.load(open(f"{FR}/{pid}_audio.json")) if os.path.exists(f"{FR}/{pid}_audio.json") else None
        if pj and first_word is not None:
            gap = (pj["dur"] - pj["last_word"]) + first_word
            cut["silence_across_cut"] = round(gap, 2)
            if gap < 0.5: flags.append({"type": "cut_silence", "gap": round(gap, 2)})
json.dump({"dur": dur, "first_word": first_word, "last_word": last_word}, open(f"{FR}/{sid}_audio.json", "w"))
print(json.dumps({"shot": sid, "dur": round(dur, 2), "fps": fps, "heard": heard, "cer": round(cer, 3),
                  "first_word": first_word and round(first_word, 2), "last_word": last_word and round(last_word, 2),
                  "drift": drift, "voice": voice, "cut": cut, "flags": flags}, indent=1))
