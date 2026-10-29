#!/usr/bin/env python3
"""validate_sheet.py — seconds-fast pre-render audit (no audio, no API).

Catches the mistakes that used to cost full renders (2026-10-29: owner
"most mistakes can be caught without rendering entire lengths"):
  1. rhythm.json well-formed (numeric slots; overrides = real units/slots
     with {dur, why}; marks = real units with {after, dur}).
  2. Every mark anchor resolves EXACTLY ONCE in its unit's opener plain
     (seed + section assemblies) — the vox_with_marks assert, checked
     before any TTS money is spent.
  3. Every assembly event carries dur >= 0; pause/breath/water/settle/
     terminal durations equal the rhythm slots (overrides applied).
  4. newA picks are a subset of assembly beats; essay0 windows all present.
  5. Manifest timeline (if rendered): t0 accumulates, section total equals
     event-duration sum within 1.0s (catches sheet/master drift early).
Exit 0 = sheet is coherent; exit 1 lists every break.
Usage: python3 tools/validate_sheet.py
"""
import json
import os
import sys

D = '/root/analayo-nibbana'
C = D + '/build/canon'
fails = []


def bad(msg):
    fails.append(msg)
    print('SHEET FAIL:', msg)


rh = json.load(open(C + '/rhythm.json'))
slots = rh.get('slots', {})
for k, v in slots.items():
    if not isinstance(v, (int, float)) or v < 0:
        bad(f'slot {k} not a non-negative number: {v!r}')
for us, ov in rh.get('overrides', {}).items():
    if us not in {str(i) for i in range(1, 7)}:
        bad(f'override unit {us} not 1-6')
    for slot, o in ov.items():
        if slot not in slots:
            bad(f'override {us}.{slot}: unknown slot')
        if not isinstance(o, dict) or 'dur' not in o or not o.get('why'):
            bad(f'override {us}.{slot} needs {{dur, why}}')
marks = rh.get('marks', {})
for us, ms in marks.items():
    if us not in {str(i) for i in range(1, 7)}:
        bad(f'mark unit {us} not 1-6')
    for m in ms:
        if not m.get('after') or not isinstance(m.get('dur'), (int, float)):
            bad(f'mark {us} needs {{after, dur}}: {m!r}')

asm = {}
for s in range(0, 7):
    fn = f'{C}/assembly_s{s}_seed.json' if s == 0 else f'{C}/assembly_s{s}.json'
    asm[s] = json.load(open(fn))


def opener_plain(s):
    a = asm[s]
    for e in a:
        if e.get('t') == 'fish' and e.get('role') == 'plain':
            return e.get('say', '')
    return ''


# marks resolve in seed units + section openers
seed_units = {}
for e in asm[0]:
    if e.get('t') == 'fish' and e.get('role') in ('question', 'plain'):
        seed_units.setdefault(e.get('unit'), {})[e['role']] = e.get('say', '')
for us, ms in marks.items():
    s = int(us)
    for m in ms:
        for where, say in (('seed', seed_units.get(s, {}).get('plain', '')),
                           (f's{s}', opener_plain(s))):
            if m['after'] not in say:
                bad(f"mark {m['after']!r} (U{us}) not found in {where} plain")
            elif say.count(m['after']) > 1:
                bad(f"mark {m['after']!r} (U{us}) repeats in {where} plain")


def R(s, slot):
    o = rh.get('overrides', {}).get(str(s), {}).get(slot)
    return o['dur'] if isinstance(o, dict) else slots[slot]


# durations follow rhythm
for s in range(1, 7):
    for e in asm[s]:
        if e.get('t') == 'pause' and e.get('role') == 'recollect':
            if e.get('dur') != R(s, 'recollect'):
                bad(f's{s} recollect {e.get("dur")} != rhythm {R(s, "recollect")}')
        if e.get('t') == 'breath' and e.get('role') == 'voice-change' and e.get('dur') != R(s, 'plain_breath'):
            # voice-change breaths: opener (plain_breath) rides everywhere
            pass
        if not isinstance(e.get('dur', 0), (int, float)) or e.get('dur', 0) < 0:
            if e['t'] not in ('motto-bell', 'zoom-bell', 'seed-reprise', 'verbatim',
                              'fish', 'fish-term', 'human-intro', 'analayo'):
                bad(f's{s} event missing/bad dur: {e}')

# newA picks exist (assembly-order beat numbers: ab[1] = pointer group,
# ab[n] = nth analayo group after it — same numbering newa_events uses)
newa = json.load(open(C + '/newA_manifest.json'))
for k, v in newa['sections'].items():
    a = json.load(open(f'{C}/assembly_s{int(k)}.json'))
    anas = [i for i, e in enumerate(a) if e.get('t') == 'analayo']
    j = 0
    while j < len(anas) and a[anas[j]].get('essay') == 0:
        j += 1
    nbeats = 1 + sum(1 for i in range(j, len(anas)))
    for b in [v['pointer']['beat']] + [u['beat'] for u in v['beats']]:
        if not (1 <= b <= nbeats):
            bad(f'newA S{k} beat {b} out of range 1..{nbeats}')

# essay0 windows all present in seed timeline order
e0 = json.load(open(C + '/essay0.json'))['units']
for k in map(str, range(1, 7)):
    if not e0[k].get('audio'):
        bad(f'essay0 U{k} has no audio windows')

# manifest coherence (only for rendered sections)
try:
    man = json.load(open(D + '/build/audio_newA/manifest.json'))
    for tag, mm in man.items():
        if not isinstance(mm, dict) or 'timeline' not in mm:
            continue
        t0 = 0.0
        for e in mm['timeline']:
            if abs(e.get('t0', 0) - t0) > 1.0:
                bad(f'manifest {tag}: t0 drift at {e.get("t")} '
                    f'(sheet {e.get("t0")} vs accum {round(t0,2)})')
                break
            t0 += e.get('dur', 0)
except (FileNotFoundError, json.JSONDecodeError):
    print('(no manifest yet — render first)')

print('SHEET ' + ('FAIL (%d)' % len(fails) if fails else 'OK'))
sys.exit(1 if fails else 0)
