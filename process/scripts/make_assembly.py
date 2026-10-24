"""Build assembly_sN.json with the question ritual.
Ritual (process/12-ARGUMENT.md): motto-bell -> question -> pause(recollect)
-> intro/Analayo unfolds. Then per beat: verbatim -> fish -> breath ->
[terms] -> analayo -> water. Zoom bell closes every section (S6: seed reprise).
"""
import json
from collections import Counter

D = '/root/analayo-nibbana'
td = '/tmp/opencode/condensed'

# The 6 questions — lifted verbatim from build/human-scripts.md section headers.
# They ARE the 6-slot argument (process/12-ARGUMENT.md); Fish speaks them as-is.
QUESTIONS = {
    1: "What is Nibbana?",
    2: "How does suffering actually run?",
    3: "Why do we stay stuck?",
    4: "What does the mechanism build?",
    5: "How do you see through it?",
    6: "What remains when it stops?",
}

terms = {s: json.load(open('%s/seg%d_terms.json' % (td, s))) for s in range(1, 7)}
tmap = {}
for s in range(1, 7):
    for o in terms[s]:
        tmap[(s, o['clip'])] = o.get('drops', [])

for s in range(1, 7):
    core = json.load(open('%s/seg%d_core_v4.json' % (td, s)))
    sc = json.load(open('%s/seg%d_script.json' % (td, s)))
    byclip = {e['clip']: e for e in sc}

    ev = [
        {'t': 'motto-bell'},
        {'t': 'fish', 'role': 'question', 'say': QUESTIONS[s]},
        {'t': 'pause', 'dur': 3.0, 'role': 'recollect',
         'note': 'listener tries to answer before the intro - this pause IS the learning'},
        {'t': 'human-intro', 'ref': 'human-scripts.md section %d' % s,
         'status': 'pending-recording',
         'note': 'the human answers the question in their own words, then Analayo unfolds'},
        {'t': 'analayo', 'lec': core[0]['lec'], 'start': core[0]['start'],
         'end': core[0]['end'], 'dur': core[0].get('dur', 0),
         'note': 'COLD OPEN: Analayo reads the motto first - no Fish before him'},
    ]
    first = True
    for x in core:
        e = byclip.get(x.get('clip'))
        if e is None:
            e = next((y for y in sc
                      if y['analayo']['lec'] == x['lec']
                      and abs(y['analayo']['start'] - x['start']) < 3), None)
        v = (e.get('nanananda_verbatim', '') if e else '')
        ev.append({'t': 'verbatim', 'text': v,
                   'sermon': e.get('nanananda_sermon') if e else None})
        ev.append({'t': 'fish', 'beat': e['clip'] if e else None,
                   'say': e.get('tts_line', '') if e else ''})
        for d in tmap.get((s, (e['clip'] if e else -1)), []):
            ev.append({'t': 'fish-term',
                       'say': d.get('fish_says', d.get('say', '')),
                       'hears': d.get('hears', '')})
        ev.append({'t': 'breath', 'dur': 1.5})
        if first:
            ev.append({'t': 'note',
                       'text': 'beat 1 Analayo already played as cold open - no repeat'})
            first = False
        else:
            ev.append({'t': 'analayo', 'lec': x['lec'], 'start': x['start'],
                       'end': x['end'],
                       'dur': x.get('dur', round(x['end'] - x['start'], 1))})
        ev.append({'t': 'water', 'dur': 2.5})
    if s < 6:
        ev.append({'t': 'zoom-bell'})
    else:
        ev += [{'t': 'seed-reprise'}, {'t': 'motto-bell'}, {'t': 'silence', 'dur': 30}]
    json.dump(ev, open('%s/assembly_s%d.json' % (td, s), 'w'), indent=1)
    print('S%d: %d events %s' % (s, len(ev), dict(Counter(x['t'] for x in ev))))
