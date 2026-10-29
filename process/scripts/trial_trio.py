#!/usr/bin/env python3
"""Trial the shiva Sanskrit trio on our essay-0 Qs + plains.
Usage: python3 process/scripts/trial_trio.py
Writes build/ears/trio_Q1..P6_<voice>.mp3 slices + 3 audition concats.
FREE TIER ONLY (s2.1-pro-free, abort anything else). Key never written anywhere.
"""
import json
import os
import subprocess
import sys
import urllib.request

D = '/root/analayo-nibbana'
OUT = D + '/build/ears/trio_trial'
os.makedirs(OUT, exist_ok=True)

TRIO = {
    'sadhguru': '37a8fbc200e74961bee0597c3b4e4041',
    'osho': '06134e9a49cb4a36997b75402c8a0621',
    'gurudeep': '82926c3143bc4d259fa9834b96897fad',
}
MODEL = 's2.1-pro-free'
assert MODEL == 's2.1-pro-free', 'paid model blocked: never spend credits'


def key():
    k = (os.getenv('FISH_API_KEY') or '').strip()
    if not k:
        for ef in ('/root/characters/audition/.env',):
            try:
                import re as _re
                m = _re.search(r'^FISH_API_KEY=(.*)$', open(ef).read(), _re.M)
                if m and m.group(1).strip():
                    k = m.group(1).strip()
                    break
            except OSError:
                pass
    assert k, 'FISH_API_KEY missing'
    return k


def tts(text, dst, vid, K):
    body = json.dumps({'text': text, 'format': 'mp3',
                       'reference_id': vid}).encode()
    req = urllib.request.Request('https://api.fish.audio/v1/tts', data=body,
                                 headers={'Authorization': f'Bearer {K}',
                                          'Content-Type': 'application/json',
                                          'model': MODEL})
    with urllib.request.urlopen(req, timeout=120) as r:
        open(dst, 'wb').write(r.read())


def main():
    K = key()
    e = json.load(open(D + '/build/canon/essay0.json'))['units']
    lines = []
    for k in sorted(e, key=int):
        u = e[k]
        lines.append(('Q' + k, u['question'].replace('Nibbana', 'Nirvana')))
        lines.append(('P' + k, u['plain']))
    for vname, vid in TRIO.items():
        parts = []
        for tag, text in lines:
            dst = f'{OUT}/{tag}_{vname}.mp3'
            if not (os.path.exists(dst) and os.path.getsize(dst) > 0):
                tts(text, dst, vid, K)
                print(f'tts {tag} {vname}', flush=True)
            parts.append(dst)
        lst = f'{OUT}/audition_{vname}.lst'
        open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
        out = f'{OUT}/audition_{vname}.mp3'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat',
                        '-safe', '0', '-i', lst, '-c:a', 'copy', out],
                       check=True)
        print('wrote', out)


if __name__ == '__main__':
    main()
