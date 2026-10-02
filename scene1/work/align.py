"""Force-align a short phrase in a window and print each word's start/end. Usage: align.py wav t0 t1 "phrase" """
import sys, wave
from pocketsphinx import Decoder
wav, t0, t1, ph = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
d = Decoder(samprate=16000)
for w, p in (("tavik", "T AH V IH K"), ("tavreak", "T AE V R IY K"), ("taveek", "T AH V IY K")):
    try: d.add_word(w, p, False)
    except RuntimeError: pass
d.set_jsgf_string("a", "#JSGF V1.0;\ngrammar a;\npublic <s> = %s;\n" % ph.lower()); d.activate_search("a")
wf = wave.open(wav); sr = wf.getframerate(); wf.setpos(int(t0 * sr)); raw = wf.readframes(int((t1 - t0) * sr))
d.start_utt(); d.process_raw(raw, full_utt=True); d.end_utt()
print([(s.word, round(t0 + s.start_frame / 100, 2), round(t0 + s.end_frame / 100, 2)) for s in d.seg()])
