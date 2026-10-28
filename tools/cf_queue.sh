#!/bin/bash
# ERA-1 SUPERSEDED (kept for method, 2026-10-28): references
# /home/box/Downloads + /tmp/opencode/cf_whisper.py. 33/33 transcripts
# exist. Not run by any live path.
D=/home/box/Downloads/yt/analayo-nibbana
for n in $(seq -w 1 33); do
  mp3="$D/analayo-nibbana-lecture-$n.mp3"
  out="$D/lecture-$n.transcript.cf.json"
  [ -s "$mp3" ] || { echo "$n no mp3 yet, skip"; continue; }
  [ -s "$out" ] && { echo "$n already transcribed"; continue; }
  for try in 1 2 3; do
    echo "$n transcribe try $try"
    python3 -u /tmp/opencode/cf_whisper.py "$mp3" "$out" && break
    echo "$n failed try $try"; sleep 300
  done
done
echo "QUEUE DONE"
