#!/usr/bin/env python3
"""Assemble the Scene 1 480p rough cut and the cut sheet.

- Each chosen clip (clips/NN_x.mp4) is loudness-levelled (EBU R128, -16 LUFS) and re-encoded,
  then all are joined with a concat that re-encodes the sound as one track (a straight copy-join
  played silent on Chad's phone).
- HOLD_TAIL adds a few frames of the last picture to a clip's end where the silence across a cut
  was short (frames to hold).
- Output: Scene1_H3MAX_shots1-4_480p.mp4 (H.264 Main, AAC stereo, faststart) and cut_sheet_h3.jpg.
"""
import os, subprocess, glob
import cv2, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
HOLD_TAIL = {}
clips = sorted(glob.glob("clips/??_h.mp4"))
os.makedirs("norm", exist_ok=True)
parts = []
for c in clips:
    sid = os.path.basename(c)[:2]
    out = f"norm/{sid}.mp4"
    vf = "scale=832:480,fps=24,format=yuv420p"
    if sid in HOLD_TAIL:
        vf += f",tpad=stop_mode=clone:stop={HOLD_TAIL[sid]}"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", c, "-vf", vf,
                    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,apad", "-shortest",
                    "-c:v", "libx264", "-profile:v", "main", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-ac", "2",
                    out], check=True)
    parts.append(out)
with open("norm/list.txt", "w") as f:
    for p in parts:
        f.write(f"file '{os.path.basename(p)}'\n")
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", "norm/list.txt",
                "-c:v", "libx264", "-profile:v", "main", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-ac", "2",
                "-movflags", "+faststart", "Scene1_H3MAX_shots1-4_480p.mp4"], check=True)

# cut sheet: last frame of N beside first frame of N+1, one row per cut
rows = []
for a, b in zip(parts, parts[1:]):
    ca, cb = cv2.VideoCapture(a), cv2.VideoCapture(b)
    n = int(ca.get(cv2.CAP_PROP_FRAME_COUNT)); ca.set(cv2.CAP_PROP_POS_FRAMES, n - 1)
    _, fa = ca.read(); _, fb = cb.read()
    fa, fb = cv2.resize(fa, (480, 261)), cv2.resize(fb, (480, 261))
    label = np.full((261, 90, 3), 30, np.uint8)
    cv2.putText(label, f"{os.path.basename(a)[:2]}>{os.path.basename(b)[:2]}", (4, 135), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    rows.append(np.hstack([label, fa, np.full((261, 6, 3), 255, np.uint8), fb]))
sheet = np.vstack([np.vstack([r, np.full((6, r.shape[1], 3), 255, np.uint8)]) for r in rows])
cv2.imwrite("cut_sheet_h3.jpg", sheet, [cv2.IMWRITE_JPEG_QUALITY, 80])
print("done", len(parts), "clips")
