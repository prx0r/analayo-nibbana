#!/bin/bash
mkdir -p /home/box/Downloads/yt/analayo-nibbana/yt-subs
while IFS=$'\t' read -r n vid title; do
  out="/home/box/Downloads/yt/analayo-nibbana/yt-subs/lecture-$n.json"
  [ -s "$out" ] && continue
  /home/box/ytsub-env/bin/python - "$vid" "$out" "$n" << 'PYEOF'
import json, sys, time
from youtube_transcript_api import YouTubeTranscriptApi
vid, out, n = sys.argv[1], sys.argv[2], sys.argv[3]
for attempt in range(4):
    try:
        tl = YouTubeTranscriptApi().fetch(vid, languages=['en'])
        cues = [{"t": round(s.start, 2), "e": round(s.start + s.duration, 2), "x": s.text} for s in tl]
        json.dump({"video": vid, "cues": cues}, open(out, 'w'), ensure_ascii=False)
        print(f"{n} ok {len(cues)} cues", flush=True)
        break
    except Exception as e:
        if attempt == 3:
            print(f"{n} FAIL {type(e).__name__}", flush=True)
        time.sleep(120 * (attempt + 1))
PYEOF
  sleep 25
done < /tmp/opencode/yt_lectures.tsv
echo "YT SUBS DONE"
