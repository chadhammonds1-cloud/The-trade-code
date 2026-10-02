"""Overlap check for location coverage plates.
Finds the same features in the shared strip of two plates and reports how well they line up."""
import cv2, numpy as np, sys
def load(p, w=1536):
    im = cv2.imread(p); h = int(im.shape[0] * w / im.shape[1]); return cv2.resize(im, (w, h))
def match(a, b, label):
    sift = cv2.SIFT_create(4000)
    ka, da = sift.detectAndCompute(cv2.cvtColor(a, cv2.COLOR_BGR2GRAY), None)
    kb, db = sift.detectAndCompute(cv2.cvtColor(b, cv2.COLOR_BGR2GRAY), None)
    m = cv2.BFMatcher().knnMatch(da, db, k=2)
    good = [x for x, y in m if x.distance < 0.7 * y.distance]
    if len(good) < 8:
        print(f"{label}: FAIL, only {len(good)} shared features"); return None
    A = np.float32([ka[g.queryIdx].pt for g in good]); B = np.float32([kb[g.trainIdx].pt for g in good])
    H, mask = cv2.findHomography(A, B, cv2.RANSAC, 6.0)
    inl = int(mask.sum()); scale = float(np.sqrt(abs(np.linalg.det(H[:2, :2]))))
    # where does the strip land in the other plate?
    h, w = a.shape[:2]; corners = cv2.perspectiveTransform(np.float32([[[0,0]],[[w,0]],[[w,h]],[[0,h]]]), H).reshape(-1, 2)
    ok = inl >= 60 and 0.8 < scale < 1.25
    print(f"{label}: {inl} features line up (of {len(good)}), size ratio {scale:.2f} -> {'PASS' if ok else 'FAIL'}; strip lands at x {corners[:,0].min():.0f}-{corners[:,0].max():.0f}")
    return H, inl, scale
C = load("CENTER.png"); W = C.shape[1]; q = W // 4
if len(sys.argv) < 2 or "lr" in sys.argv:
    L = load("LEFT.png"); R = load("RIGHT.png")
    match(C[:, :q], L, "CENTER left quarter  -> LEFT plate ")
    match(C[:, -q:], R, "CENTER right quarter -> RIGHT plate")
if "pano" in sys.argv:
    P = cv2.imread("PANO.png"); P = cv2.resize(P, (int(P.shape[1] * C.shape[0] / P.shape[0]), C.shape[0]))
    match(C, P, "CENTER whole         -> PANORAMA   ")
