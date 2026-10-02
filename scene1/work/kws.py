"""Keyword check: does each expected key word occur in a time window? Usage: kws.py wav t0 t1 word1,word2,..."""
import sys, wave
from pocketsphinx import Decoder
wav, t0, t1, kw = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4].split(",")
wf = wave.open(wav); sr = wf.getframerate(); wf.setpos(int(t0 * sr)); raw = wf.readframes(int((t1 - t0) * sr))
res = {}
for k in kw:
    for th in ("1e-30", "1e-20", "1e-10"):
        d = Decoder(samprate=16000, keyphrase=k.lower(), kws_threshold=float(th))
        d.start_utt(); d.process_raw(raw, full_utt=True); d.end_utt()
        hit = bool(d.hyp())
        res.setdefault(k, []).append(hit)
print({k: ("strong" if v[2] else "ok" if v[1] else "weak" if v[0] else "MISSING") for k, v in res.items()})
