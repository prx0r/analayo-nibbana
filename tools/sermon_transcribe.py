"""Timestamp the 33 sermon readings (sermon-audio/*.mp3) with faster-whisper.

Output: sermon-readings/Nibbana_Stilled_NN.json in the CF transcript schema
{source, duration, engine, sentences:[{t,end,text}]} so quote-alignment tools
(sermon readings = the verbatim voice) work unchanged. Skip-existing; ordered
01..33; log: /tmp/sermon_tr.log (nohup python3 tools/sermon_transcribe.py).
"""
import os, json, subprocess, time
from faster_whisper import WhisperModel

D = "/root/analayo-nibbana"
SRC = f"{D}/sermon-audio"
OUT = f"{D}/sermon-readings"
MODEL = "small.en"
os.makedirs(OUT, exist_ok=True)

model = WhisperModel(MODEL, device="cpu", compute_type="int8", cpu_threads=4)
print(f"model {MODEL} loaded", flush=True)
for n in range(1, 34):
    src = f"{SRC}/Nibbana_Stilled_{n:02d}.mp3"
    out = f"{OUT}/Nibbana_Stilled_{n:02d}.json"
    if os.path.exists(out):
        print(f"{n:02d}: exists, skip", flush=True)
        continue
    if not os.path.exists(src):
        print(f"{n:02d}: MISSING mp3", flush=True)
        continue
    dur = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", src]).strip())
    print(f"{n:02d}: transcribing {dur/60:.1f}min", flush=True)
    t0 = time.time()
    segments, _ = model.transcribe(src, beam_size=5, vad_filter=True,
                                   vad_parameters={"min_silence_duration_ms": 500})
    sents = [{"t": round(s.start, 2), "end": round(s.end, 2),
              "text": s.text.strip()} for s in segments if s.text.strip()]
    json.dump({"source": src, "duration": dur, "engine": "faster-whisper-small.en",
               "sentences": sents}, open(out, "w"), ensure_ascii=False, indent=1)
    print(f"{n:02d}: DONE {len(sents)} segments in {time.time()-t0:.0f}s", flush=True)
print("ALL SERMONS TRANSCRIBED", flush=True)
