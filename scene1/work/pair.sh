#!/bin/bash
# pair.sh <prev id> <still name> <still url> — download still, make pair sheet with previous shot's last frame
cd "$(dirname "$0")"; ./get.sh "$3" stills/$2.png >/dev/null
python3 -c "
import cv2,numpy as np
a=cv2.resize(cv2.imread('frames/$1_last.png'),(896,504));b=cv2.resize(cv2.imread('stills/$2.png'),(896,504))
cv2.imwrite('frames/pair_$1_$2.jpg',np.hstack([a,np.full((504,8,3),255,np.uint8),b]))"
echo frames/pair_$1_$2.jpg
