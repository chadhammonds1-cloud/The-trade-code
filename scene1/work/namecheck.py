"""Name check: decode a short window with a grammar offering the right name and the known wrong ones.
Usage: python3 namecheck.py <wav16k> <t0> <t1> "<words before>" "<words after>"
Prints which name variant the audio matches best."""
import sys, wave
from pocketsphinx import Decoder
wav, t0, t1, pre, post = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4], sys.argv[5]
V = {"tavik": "T AH V IH K", "tavreak": "T AE V R IY K", "taviki": "T AH V IY K IY", "taveek": "T AH V IY K", "tavique": "T AE V IY K", "trevor": "T R EH V ER", "david": "D EY V IH D"}
d = Decoder(samprate=16000)
for w, p in V.items():
    try: d.add_word(w, p, False)
    except RuntimeError: pass
g = "#JSGF V1.0;\ngrammar n;\npublic <s> = [<pre>] (%s) [<post>];\n<pre> = %s;\n<post> = %s;\n" % (" | ".join(V), pre.lower() or "<NULL>", post.lower() or "<NULL>")
d.set_jsgf_string("n", g); d.activate_search("n")
wf = wave.open(wav); sr = wf.getframerate(); wf.setpos(int(t0 * sr)); raw = wf.readframes(int((t1 - t0) * sr))
d.start_utt(); d.process_raw(raw, full_utt=True); d.end_utt()
h = d.hyp().hypstr if d.hyp() else ""
name = [w for w in h.split() if w in V]
print({"heard": h, "name": name[0] if name else None, "pass": bool(name) and name[0] == "tavik"})
