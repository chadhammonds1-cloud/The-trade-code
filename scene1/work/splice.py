import sys, numpy as np, soundfile as sf
g, pad = float(sys.argv[1]), float(sys.argv[2])
a, sr = sf.read("frames/12a_48k.wav"); b, _ = sf.read("frames/12b_48k.wav")
sa, ea = int((8.05 - pad) * sr), int((8.62 + pad) * sr)
sb = int((8.77 - pad) * sr); L = ea - sa; eb = sb + L
word = a[sa:ea] * g
f = int(0.015 * sr); r = np.linspace(0, 1, f)[:, None]
out = b.copy()
out[sb:sb+f] = b[sb:sb+f]*(1-r) + word[:f]*r
out[sb+f:eb-f] = word[f:L-f]
out[eb-f:eb] = word[L-f:]*(1-r) + b[eb-f:eb]*r
sf.write("frames/12d_48k.wav", out, sr)
