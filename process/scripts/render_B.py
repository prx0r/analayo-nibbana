#!/usr/bin/env python3
"""Render ladder rung B: same rhythm as newA (bell/Q/plain/analayo,
analayo-only) but using ladder_manifest.json units (B picks).

Each B unit = {beat, reason, analayo:[{lec,start,end,dur}]}.
Reads assemblies for Q+plain, picks from B picks, renders to
build/audio_B/ (seed + S1..S6 + full_B.mp3).

Usage: python3 process/scripts/render_B.py [seed|all]
Renders stay local-only, uncommitted.
"""
import json
import os
import sys

sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent.parent.parent / 'tools'))
import render_a_essay as R

os.environ['AUDIO_OUT'] = '/root/analayo-nibbana/build/audio_B'
R.NEWA = True  # reuse the newA event builder (analayo-only, breath)
R.P0_NO_BELLS = False
R.NEWA_SEED_ONLY = (len(sys.argv) < 2 or sys.argv[1] == 'seed')

# We monkey-patch render_a_essay's main to use ladder_manifest instead
# of newA_manifest. Cleanest: point NEWA_MANIFEST at the B rung.
import pathlib
B = pathlib.Path('/root/analayo-nibbana/build/canon')
ladder = json.loads((B / 'ladder_manifest.json').read_text())
b_rung = ladder['rungs']['B']
# Build a newA-shaped manifest from B rungs (units have 'analayo' as list)
newa_shaped = {'sections': {}}
for s in map(str, range(1, 7)):
    sec = b_rung[s]
    # first unit = pointer (has 'analayo' list)
    ptr = sec['units'][0]
    newa_shaped['sections'][s] = {
        'question': sec['question'],
        'total_s': sec['total_s'],
        'pointer': {'beat': ptr['beat'], 'reason': ptr.get('reason', 'pointer'),
                    'analayo': ptr['analayo'] if isinstance(ptr['analayo'], list)
                    else [ptr['analayo']]},
        'beats': [{'beat': u['beat'], 'reason': u.get('reason', ''),
                   'analayo': u['analayo'] if isinstance(u['analayo'], list)
                   else [u['analayo']]} for u in sec['units'][1:]],
    }
(B / '_tmp_newA_B.json').write_text(json.dumps(newa_shaped))

# Patch: point render_a_essay at the B manifest
_orig_main = R.main
def b_main():
    # swap the manifest file
    real = B / 'newA_manifest.json'
    backup = real.read_text()
    real.write_text((B / '_tmp_newA_B.json').read_text())
    try:
        _orig_main()
    finally:
        real.write_text(backup)
        (B / '_tmp_newA_B.json').unlink(missing_ok=True)
R.main = b_main
R.main()
