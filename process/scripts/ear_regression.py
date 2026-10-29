#!/usr/bin/env python3
"""ear_regression.py — run the tracked ear fixtures after any model,
prompt, or engine change. Descriptive prompts only (blanket verdicts
proven worthless 2026-10-26); expectations are FINDINGS with keywords.

Usage: python3 process/scripts/ear_regression.py
Uploads 8 small fixtures to a temp host, one descriptive call each,
checks expected finding-keywords present (bad) / defect-keywords absent
(good). Any miss = ears uncalibrated: stop, fix, re-run. Exits nonzero.
"""
import json
import subprocess
import sys
import urllib.request
import urllib.error
from pathlib import Path

D = Path('/root/analayo-nibbana')
FIX = D / 'build' / 'ear_fixtures'
MODEL = 'qwen3-omni-flash'
URL = 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions'

# file -> (must_contain_any, must_not_contain_any)
EXPECT = {
    'bad_blip.mp3': (['silence', 'silent', 'no speech', 'no sound'], []),
    'bad_trunc.mp3': (['cut off', 'cutoff', 'abrupt', 'ends suddenly', 'incomplete'], []),
    'bad_midcut.mp3': (['mid-sentence', 'mid sentence', 'mid-thought', 'abruptly', 'begins abruptly'], []),
    'bad_quiet.mp3': (['quiet', 'faint', 'low volume', 'barely'], []),
    'bad_chant.mp3': (['chant', 'Pali', 'unintelligible', 'foreign'], []),
    'good_motto.mp3': ([], ['silence where', 'cut off', 'robotic', 'glitch']),
    'good_analayo.mp3': ([], ['silence where', 'cut off', 'robotic', 'glitch']),
    'good_fish.mp3': ([], ['silence where', 'cut off', 'robotic', 'glitch']),
}


def ask(key, url, kind):
    if kind == 'bad':
        q = ('Describe exactly what you hear, literally and second by '
             'second. Note any silence, cutoff, mid-sentence start, '
             'unnatural quiet, chanting, or robotic voice.')
    else:
        q = ('Describe exactly what you hear, literally. Note any defect: '
             'silence where speech should be, cutoff, glitch, robotic voice.')
    body = json.dumps({
        'model': MODEL,
        'messages': [{'role': 'user', 'content': [
            {'type': 'input_audio', 'input_audio': {'data': url, 'format': 'mp3'}},
            {'type': 'text', 'text': q}]}],
        'max_tokens': 300}).encode()
    req = urllib.request.Request(URL, data=body,
                                 headers={'Authorization': f'Bearer {key}',
                                          'Content-Type': 'application/json'})
    try:
        d = json.loads(urllib.request.urlopen(req, timeout=300).read().decode())
        return d['choices'][0]['message']['content']
    except urllib.error.HTTPError as e:
        return f'HTTP {e.code}: {e.read().decode()[:200]}'


def main():
    import os
    key = (os.environ.get('DASHSCOPE_API_KEY') or '').strip()
    if not key:
        p = subprocess.run(['agent-vault', 'vault', 'credential', 'get',
                            'DASHSCOPE_API_KEY', '--vault', 'oracle'],
                           capture_output=True, text=True)
        key = p.stdout.strip()
    if not key:
        print('no DashScope key')
        return 1
    results = {}
    for f in EXPECT:
        up = subprocess.run(['curl', '-s', '-F', f'files[]=@{FIX / f}',
                             'https://uguu.se/upload.php'],
                            capture_output=True, text=True, timeout=180)
        url = json.loads(up.stdout)['files'][0]['url']
        txt = ask(key, url, 'bad' if f.startswith('bad_') else 'good')
        results[f] = {'url': url, 'text': txt}
        print(f'--- {f}\n{txt[:400]}\n')
    json.dump(results, open(D / 'build' / 'ear_regression_last.json', 'w'),
              indent=1)
    print('full texts: build/ears/ear_regression_last.json')
    print('NOTE: keyword-gating scored 4/8 on 2026-10-26 (midcut needs',
          'expected-text to judge; good_fish false-alarmed on a 2s clip).',
          'This runner is CALIBRATION (human reads the texts), not a gate.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
