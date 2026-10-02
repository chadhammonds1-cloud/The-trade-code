#!/bin/bash
# qc.sh <id> <take> <clip url> <still png> [prev id]
cd "$(dirname "$0")"
id=$1; tk=$2; ./get.sh "$3" clips/${id}_${tk}.mp4 >/dev/null
prev=""; [ -n "$5" ] && prev=clips/$5_x.mp4
python3 qc_one.py $id clips/${id}_${tk}.mp4 $4 $prev 2>/dev/null | sed -n "/^{/,\$p" | python3 -c "
import json,sys; r=json.load(sys.stdin)
print('dur',r['dur'],'| heard:',r['heard']); print('cer',r['cer'],'first',r['first_word'],'last',r['last_word'])
print('voice',[ (v['spk'],v.get('sims')) for v in r['voice'] if isinstance(v,dict)]); print('cut',r['cut']); print('flags',r['flags'])"
n=$(ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames -of csv=p=0 clips/${id}_${tk}.mp4)
ffmpeg -loglevel error -y -i clips/${id}_${tk}.mp4 -vf "select='eq(n\,0)+eq(n\,$((n/5)))+eq(n\,$((2*n/5)))+eq(n\,$((3*n/5)))+eq(n\,$((4*n/5)))+eq(n\,$((n-1)))',scale=640:-2,tile=2x3" -frames:v 1 frames/${id}_big.jpg
