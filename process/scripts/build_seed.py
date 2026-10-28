#!/usr/bin/env python3
"""Build build/assembly_s0_seed.json — the six micro-sessions chained.

Seed = question -> 3s recollect -> essay-0 (verbatim+plain on screen,
archive window answers) per section, water between units, motto-bell
opens, zoom-bell closes. Essay-0 clip = assembly_sN beat at ESSAY0[s].
"""
import json

D = '/root/analayo-nibbana'
BELL = {'motto-bell': 2.5, 'zoom-bell': 6.0}

seed = [{'t': 'motto-bell', 'note': 'SEED opens on the refrain bell'}]
for i, s in enumerate(range(1, 7)):
    a = json.load(open('%s/build/assembly_s%d.json' % (D, s)))
    q = [e for e in a if e.get('role') == 'question'][0]
    # Type-based (2026-10-28: opening gained a plain event; no more indices).
    # Triple-pointer sections (S2): every essay-0 analayo following the
    # essay-0 verbatim rides along, in order.
    vi = next(i for i, e in enumerate(a)
              if e['t'] == 'verbatim' and e.get('essay') == 0)
    vb = a[vi]
    ans = []
    for e in a[vi + 1:]:
        if e['t'] == 'analayo' and e.get('essay') == 0:
            ans.append(e)
        elif e['t'] in ('breath',):
            continue
        else:
            break
    assert ans, f'section {s}: no essay-0 audio'
    seed.append({'t': 'fish', 'role': 'question', 'say': q['say'], 'unit': i + 1})
    seed.append({'t': 'pause', 'dur': 3.0, 'role': 'recollect'})
    # PLAIN RESPONSE in seed too (owner 2026-10-28: QUESTION, PLAIN,
    # ANALAYO everywhere — no exceptions, not even the trailer).
    seed.append({'t': 'fish', 'role': 'plain', 'say': vb.get('plain', ''),
                 'unit': i + 1})
    seed.append({'t': 'verbatim', 'text': vb['text'], 'plain': vb.get('plain', ''),
                 'sermon': vb.get('sermon'), 'essay': 0, 'unit': i + 1})
    for k, an in enumerate(ans):
        seed.append({'t': 'analayo', 'lec': an['lec'], 'start': an['start'],
                     'end': an['end'], 'dur': an['dur'], 'unit': i + 1,
                     'note': 'essay-0 unit %d part %d/%d' % (i + 1, k + 1, len(ans))})
    if i < 5:
        seed.append({'t': 'water', 'dur': 2.5})
seed.append({'t': 'zoom-bell', 'note': 'SEED done -> zoom into section 1'})
json.dump(seed, open('%s/build/assembly_s0_seed.json' % D, 'w'), indent=1)
qs = [e['say'] for e in seed if e['t'] == 'fish']
print('seed rebuilt: %d units' % len(qs))
for i, q in enumerate(qs):
    print('  %d. %s' % (i + 1, q))
