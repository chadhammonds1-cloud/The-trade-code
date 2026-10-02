"""Which of several phrases best matches a window? Usage: phrase.py wav t0 t1 "phrase A|phrase B|..." """
import sys, wave
from pocketsphinx import Decoder
wav, t0, t1, alts = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4].split("|")
wf = wave.open(wav); sr = wf.getframerate(); wf.setpos(int(t0 * sr)); raw = wf.readframes(int((t1 - t0) * sr))
for i, a in enumerate(alts):
    d = Decoder(samprate=16000)
    d.set_jsgf_string("p", "#JSGF V1.0;\ngrammar p;\npublic <s> = [<any>] %s [<any>];\n<any> = <NULL>;\n" % a.lower())
    d.activate_search("p")
    d.start_utt(); d.process_raw(raw, full_utt=True); d.end_utt()
    h = d.hyp()
    print(f"{a!r}: score {h.score if h else None}")
