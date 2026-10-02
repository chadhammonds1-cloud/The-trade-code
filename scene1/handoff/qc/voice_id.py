import json, subprocess, numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
enc = VoiceEncoder("cpu")
R = json.load(open("out/qc_report.json"))
refs = {k: enc.embed_utterance(preprocess_wav(f"/home/claude/trade/voices/{f}.wav")) for k, f in (("TAV","tavik"),("VES","vessa"),("DAD","dad"))}
# the refs against each other, to know what "different person" looks like
print("ref-vs-ref:", {f"{a}-{b}": round(float(refs[a]@refs[b]),3) for a in refs for b in refs if a<b})
out = []
for s in R["shots"]:
    clip = s["clip"]
    subprocess.run(["ffmpeg","-loglevel","error","-y","-i",f"/home/claude/trade/s1v/{clip}.mp4","-ac","1","-ar","16000","/tmp/_v.wav"],check=True)
    import soundfile as sf
    y, sr = sf.read("/tmp/_v.wav")
    for ln in s["audio"]["lines"]:
        if ln.get("t0") is None: continue
        seg = y[int(ln["t0"]*sr):int(ln["t1"]*sr)]
        if len(seg) < sr*0.8: 
            out.append((s["shot"], ln["speaker"], "too short")); continue
        e = enc.embed_utterance(preprocess_wav(seg, source_sr=sr))
        sims = {k: round(float(e@v),3) for k,v in refs.items()}
        best = max(sims, key=sims.get)
        out.append((s["shot"], ln["speaker"], sims, "OK" if best==ln["speaker"] else f"MISMATCH->{best}"))
for o in out: print(o)
