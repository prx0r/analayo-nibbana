#!/bin/bash
# CF Whisper queue for 33 sermon readings -> sources/sermons/readings/*.json
D=/root/analayo-nibbana
LOG=/tmp/sermon_cf.log
echo "=== CF queue start $(date -u) ===" >> "$LOG"
for n in $(seq -w 1 33); do
  src="$D/sources/sermons/audio/Nibbana_Stilled_${n}.mp3"
  out="$D/sources/sermons/readings/Nibbana_Stilled_${n}.json"
  # skip if already done with CF engine
  if [ -s "$out" ] && grep -q "cf-whisper-large-v3-turbo" "$out" 2>/dev/null; then
    echo "$n already CF-done, skip" | tee -a "$LOG"
    continue
  fi
  echo "--- $n $src $(date -u) ---" | tee -a "$LOG"
  for try in 1 2 3 4 5; do
    if python3 -u "$D/tools/cf_whisper.py" "$src" "$out" >> "$LOG" 2>&1; then
      echo "$n DONE try $try" | tee -a "$LOG"
      break
    fi
    echo "$n FAILED try $try, sleep 60" | tee -a "$LOG"
    sleep 60
  done
  sleep 5
done
echo "=== ALL SERMONS CF-TRANSCRIBED $(date -u) ===" | tee -a "$LOG"
