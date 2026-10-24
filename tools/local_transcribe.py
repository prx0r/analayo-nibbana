"""Local fallback transcription for lectures missing CF transcripts (28,30,32,33).
Uses faster-whisper (small.en) on DharmaSeed mp3s. Output matches CF transcript
schema: {source, duration, engine, sentences:[{t,end,text}]} so auto_keeps/gen_plan work unchanged.
"""
import os, time, json, subprocess, sys
from faster_whisper import WhisperModel

D = "/root/analayo-nibbana"
JOBS = [("28", "58747"), ("30", "58749"), ("32", "58751"), ("33", "58752")]
MODEL = "small.en"

def mp3_ready(path, wait=0):
    if not os.path.exists(path):
        return False
    s1 = os.path.getsize(path)
    time.sleep(10)
    return os.path.getsize(path) == s1 and os.path.getsize(path) > 1_000_000

model = WhisperModel(MODEL, device="cpu", compute_type="int8", cpu_threads=4)
print(f"model {MODEL} loaded", flush=True)
for lec, talk in JOBS:
    src = f"{D}/ds-mp3/lec-{talk}.mp3"
    dst_mp3 = f"{D}/analayo-nibbana-lecture-{lec}.mp3"
    out = f"{D}/lecture-{lec}.transcript.cf.json"
    if os.path.exists(out):
        print(f"lec{lec}: transcript exists, skip", flush=True)
        continue
    print(f"lec{lec}: waiting for {src}", flush=True)
    while not mp3_ready(src):
        time.sleep(30)
    # hardlink/copy into canonical mp3 name for gen_plan ffprobe
    if not os.path.exists(dst_mp3):
        os.link(src, dst_mp3)
        print(f"lec{lec}: linked mp3", flush=True)
    dur = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", dst_mp3]).strip())
    print(f"lec{lec}: transcribing {dur/60:.1f}min", flush=True)
    segments, _ = model.transcribe(dst_mp3, beam_size=5, vad_filter=True,
                                   vad_parameters={"min_silence_duration_ms": 500})
    sents = [{"t": round(s.start, 2), "end": round(s.end, 2),
              "text": s.text.strip()} for s in segments if s.text.strip()]
    json.dump({"source": dst_mp3, "duration": dur, "engine": "faster-whisper-small.en",
               "sentences": sents}, open(out, "w"), ensure_ascii=False, indent=1)
    print(f"lec{lec}: DONE {len(sents)} segments", flush=True)
print("ALL TRANSCRIBED", flush=True)
