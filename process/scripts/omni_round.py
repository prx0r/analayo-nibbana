#!/usr/bin/env python3
"""Omni audit round on fresh p0 render. Descriptive prompts only (no verdicts).
Chunks <=12min with 30s overlap. One call per chunk. Results -> build/ear_round3.json."""
import json
import subprocess
import sys
import urllib.request

D = '/root/analayo-nibbana/build/audio_p0'
URL = 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions'
AUDIT_Q = (
    'Describe exactly what you hear, literally, second by second. '
    'Note each of these ONLY if present, with timestamps: '
    '(a) speech starting or ending mid-sentence, '
    '(b) silence longer than 5 seconds where speech should be, '
    '(c) clicks, thumps, or glitches, '
    '(d) sudden volume jumps between voices, '
    '(e) synthetic or robotic voices. '
    'Quote a few words at each voice change. Do not summarize the content; '
    'do not give a pass/fail verdict.'
)

PLAN = [('seed', 1), ('s1', 2), ('s2', 3), ('s3', 3), ('s4', 1), ('s5', 2), ('s6', 2)]


def dur(p):
    o = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                        '-of', 'csv=p=0', p], capture_output=True, text=True)
    return float(o.stdout.strip())


def ask(key, url, model='qwen3-omni-flash'):
    body = json.dumps({
        'model': model,
        'messages': [{'role': 'user', 'content': [
            {'type': 'input_audio', 'input_audio': {'data': url, 'format': 'mp3'}},
            {'type': 'text', 'text': AUDIT_Q}]}],
        'max_tokens': 800, 'temperature': 0}).encode()
    req = urllib.request.Request(URL, data=body,
                                 headers={'Authorization': 'Bearer %s' % key,
                                          'Content-Type': 'application/json'})
    d = json.loads(urllib.request.urlopen(req, timeout=600).read().decode())
    return d['choices'][0]['message']['content']


def upload(p):
    o = subprocess.run(['curl', '-s', '-F', 'files[]=@%s' % p, 'https://uguu.se/upload.php'],
                       capture_output=True, text=True, timeout=180)
    return json.loads(o.stdout)['files'][0]['url']


def main():
    only = sys.argv[1:]
    p = subprocess.run(['agent-vault', 'vault', 'credential', 'get',
                        'DASHSCOPE_API_KEY', '--vault', 'oracle'],
                       capture_output=True, text=True)
    key = p.stdout.strip()
    assert key, 'no key'
    total = dur('%s/seed.mp3' % D)
    try:
        results = json.load(open('/root/analayo-nibbana/build/ear_round3.json'))
    except (FileNotFoundError, json.JSONDecodeError):
        results = {}
    for tag, n in PLAN:
        if only and tag not in only:
            continue
        src = '%s/%s.mp3' % (D, tag)
        total_d = dur(src)
        results[tag] = []
        for i in range(n):
            a = max(0.0, (total_d / n) * i - (30 if i > 0 else 0))
            b = min(total_d, (total_d / n) * (i + 1) + (30 if i < n - 1 else 0))
            if i == n - 1:
                b = total_d
            if i == 0:
                a = 0.0
            f = '/tmp/omni_%s_%d.mp3' % (tag, i)
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a), '-to', str(b),
                            '-i', src, '-c:a', 'libmp3lame', '-b:a', '128k', f], check=True)
            url = upload(f)
            print('calling omni %s chunk %d/%d (%.0f-%.0fs) ...' % (tag, i + 1, n, a, b), flush=True)
            try:
                txt = ask(key, url)
            except Exception as e:
                txt = 'CALL FAILED: %r' % e
            results[tag].append({'chunk': i, 'start': a, 'end': b, 'url': url, 'text': txt})
            print('--- %s/%d (%.0f chars)' % (tag, i, len(txt)), flush=True)
    open('/root/analayo-nibbana/build/ear_round3.json', 'w').write(json.dumps(results, indent=1))
    print('wrote build/ear_round3.json')


if __name__ == '__main__':
    main()
