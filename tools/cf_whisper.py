# ERA-1 SUPERSEDED (kept for method, 2026-10-28): Cloudflare transcription
# worker. Uses /tmp/opencode/cfseg.mp3 scratch. Not run by any live path
# (33/33 transcripts exist). Cf. tools/sermon_transcribe.py for the current
# sermon-reading transcriber.
import base64, json, urllib.request, subprocess, math, sys, time, os
LECT, OUT = sys.argv[1], sys.argv[2]
KEY = open('/root/.cloudflare_r2').read().split('API_TOKEN=')[1].split('\n')[0].strip()
ACCT = '954612afb5a97bb15dddcdc70176813d'
URL = f'https://api.cloudflare.com/client/v4/accounts/{ACCT}/ai/run/@cf/openai/whisper-large-v3-turbo'
dur = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',LECT]).strip())
CH = 600
n = math.ceil(dur / CH)
segments = []
for i in range(n):
    seg = f'/tmp/opencode/cfseg.mp3'
    subprocess.run(['ffmpeg','-v','error','-ss',str(i*CH),'-t',str(CH),'-i',LECT,'-b:a','64k','-y',seg], check=True)
    audio = base64.b64encode(open(seg,'rb').read()).decode()
    body = json.dumps({'audio': audio, 'task': 'transcribe'}).encode()
    for attempt in range(4):
        try:
            req = urllib.request.Request(URL, data=body,
                headers={'Authorization': f'Bearer {KEY}','Content-Type':'application/json'})
            with urllib.request.urlopen(req, timeout=300) as r:
                d = json.load(r)
            break
        except Exception as e:
            if attempt == 3: raise
            time.sleep(5 * (attempt + 1))
    res = d.get('result', {})
    off = i * CH
    for s in res.get('segments', []):
        segments.append({'t': round(off + float(s['start']), 2),
                         'end': round(off + float(s['end']), 2),
                         'text': s['text'].strip()})
    print(f'chunk {i+1}/{n} -> {len(res.get("segments",[]))} segments', flush=True)
    os.remove(seg)
json.dump({'source': LECT, 'duration': dur, 'engine': 'cf-whisper-large-v3-turbo', 'sentences': segments},
          open(OUT,'w'), ensure_ascii=False, indent=1)
print('SENTENCES:', len(segments), flush=True)
print('ALL DONE', flush=True)
