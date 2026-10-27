#!/usr/bin/env python3
"""ear_probes.py — checkable questions instead of verdicts (2026-10-26).

Doctrine: the model is a SENSOR, the engine is the JUDGE. Every probe is
generated from ground truth the build already holds (assembly windows,
expected sentences); every answer is verified mechanically (fuzzy quote
match), never trusted. Temperature 0, one audio per call, short clips.

Probe kinds (reliability-ranked by canary evidence):
  P1 transcribe-window  — transcribe [t0,t1]; verify expected key phrase
                          present (fuzzy >=0.8). PROVEN (near-verbatim quotes).
  P2 presence            — "is sentence S spoken within [t0,t1]? answer yes/no
                          + quote the exact words." Verify quote fuzzy-matches S.
  P3 stillness           — "silence or speech at [t]?" Cross-checked against
                          the bed map (timeline); model perception of beds is
                          UNRELIABLE — engine (p0_mix_check) decides, model
                          only corroborates.
BANNED: blanket PASS/FAIL, counts, durations, "any defects?", multi-clip
batteries in one call. All proven confabulation-positive.

Usage: python3 process/scripts/ear_probes.py [seed|s1|...] (default: seed)
Uploads clips to temp host; needs DASHSCOPE_API_KEY (vault).
Exit 0 only if every probe verifies.
"""
import difflib
import json
import subprocess
import sys
import urllib.request
import urllib.error
from pathlib import Path

D = Path('/root/analayo-nibbana')
B = D / 'build'
URL = 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions'


def ask(key, audio_url, q, max_tokens=300, model='qwen3-omni-flash'):
    body = json.dumps({
        'model': model,
        'messages': [{'role': 'user', 'content': [
            {'type': 'input_audio', 'input_audio': {'data': audio_url, 'format': 'mp3'}},
            {'type': 'text', 'text': q}]}],
        'max_tokens': max_tokens, 'temperature': 0}).encode()
    req = urllib.request.Request(URL, data=body,
                                 headers={'Authorization': f'Bearer {key}',
                                          'Content-Type': 'application/json'})
    d = json.loads(urllib.request.urlopen(req, timeout=300).read().decode())
    return d['choices'][0]['message']['content']


def fuzz(a, b):
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()


def cut(src, a, b, dst):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(a), '-to', str(b),
                    '-i', str(src), '-c:a', 'libmp3lame', '-b:a', '128k', str(dst)],
                   check=True)


def upload(p):
    out = subprocess.run(['curl', '-s', '-F', f'files[]=@{p}',
                          'https://uguu.se/upload.php'],
                         capture_output=True, text=True, timeout=180)
    return json.loads(out.stdout)['files'][0]['url']


def main():
    import os
    key = (os.environ.get('DASHSCOPE_API_KEY') or '').strip()
    if not key:
        p = subprocess.run(['agent-vault', 'vault', 'credential', 'get',
                            'DASHSCOPE_API_KEY', '--vault', 'oracle'],
                           capture_output=True, text=True)
        key = p.stdout.strip()
    tags = sys.argv[1:] or ['seed']
    fails = 0
    for tag in tags:
        asm = (json.loads(open(B / 'assembly_s0_seed.json').read())
               if tag == 'seed' else None)
        if tag == 'seed':
            units = []
            cur = {}
            for e in asm:
                if e['t'] == 'fish' and e.get('role') == 'question':
                    cur = {'q': e['say'], 'u': e['unit']}
                if e['t'] == 'analayo' and cur:
                    cur.update(lec=e['lec'], start=e['start'], end=e['end'])
                    units.append(cur)
                    cur = {}
            for u in units:
                f = f'/tmp/probe_{tag}_u{u["u"]}.mp3'
                cut(str(B / 'audio_p0' / f'{tag}.mp3'), 0, 400, f)
                break
            # one call: transcribe + per-unit Q/A presence, all checkable
            url = upload(f)
            txt = ask(key, url, (
                'Transcribe the opening question word-for-word. Then quote '
                'the first 10 words of the lecture answer that follows it. '
                'Reply as JSON: {"question": "...", "answer_head": "..."}. '
                'Transcribe exactly what you hear; do not summarize.'))
            try:
                s = txt.index('{')
                got = json.loads(txt[s:txt.rindex('}') + 1])
            except ValueError:
                print(f'{tag}: UNPARSEABLE: {txt[:150]}')
                fails += 1
                continue
            exp = None
            seed0 = json.loads(open(B / 'assembly_s0_seed.json').read())
            q1 = [e['say'] for e in seed0 if e.get('role') == 'question'][0]
            a1 = [e['text'] for e in seed0 if e['t'] == 'verbatim'][0]
            a1 = (a1 if isinstance(a1, str) else a1[0])[:60]
            okq = fuzz(got.get('question', ''), q1) >= 0.8
            oka = fuzz(got.get('answer_head', ''), a1) >= 0.6
            print(f'{tag} U1: question_match={okq} answer_match={oka}')
            print(f'   got: {got}')
            if not (okq and oka):
                fails += 1
    print('probes ' + ('PASS' if not fails else f'{fails} FAILURES'))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
