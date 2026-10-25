"""Build assembly_sN.json — section event order.

GOSPEL (process/12-ARGUMENT.md, AXIOM 16): every presentation runs
TEXT VERBATIM -> PLAIN ENGLISH (Fish) -> AUDIO (Analayo). Never reorder.

OPENING (per section):
  motto-bell -> Fish asks the section question -> 3s recollect pause ->
  ESSAY 0 on screen (verbatim + its plain english, the compressed
  answer to the question) -> ESSAY 0 AUDIO: the archive voice answers
  directly (the motif; nothing wedged between question and answer) ->
  optional human intro AFTER the answer (never between) ->
  beats 2..N in the fixed stack order ->
  zoom-bell (S6: seed-reprise + motto-bell + 30s silence).

Beat 1 of every section IS essay 0 (its clip is the cold-open clip);
the loop below therefore starts at core[1:].
"""
import json
from collections import Counter

D = '/root/analayo-nibbana'
td = '/root/analayo-nibbana/build'

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

    # ---- OPENING: question -> essay 0 (text on screen, archive voice answers)
    b1 = core[0]
    b1e = byclip.get(b1.get('clip'))
    if b1e is None:
        b1e = next((y for y in sc
                    if y['analayo']['lec'] == b1['lec']
                    and abs(y['analayo']['start'] - b1['start']) < 3), None)
    ev = [
        {'t': 'motto-bell'},
        {'t': 'fish', 'role': 'question', 'say': QUESTIONS[s]},
        {'t': 'pause', 'dur': 3.0, 'role': 'recollect',
         'note': 'listener tries to answer first - this pause IS the learning'},
        {'t': 'verbatim',
         'text': (b1e.get('nanananda_verbatim', '') if b1e else ''),
         'plain': (b1e.get('tts_line', '') if b1e else ''),
         'sermon': (b1e.get('nanananda_sermon') if b1e else None),
         'essay': 0,
         'note': 'ESSAY 0 on screen: compressed answer (stack: verbatim over plain-english)'},
        {'t': 'analayo', 'lec': b1['lec'], 'start': b1['start'],
         'end': b1['end'], 'dur': b1.get('dur', round(b1['end'] - b1['start'], 1)),
         'note': 'ESSAY 0 AUDIO: archive voice answers the question (the motif)'},
        {'t': 'human-intro', 'ref': 'human-scripts.md section %d' % s,
         'status': 'optional-pending',
         'note': 'only if used: AFTER the answer, never between question and motto'},
    ]

    # ---- BEATS 2..N: fixed stack TEXT VERBATIM -> PLAIN ENGLISH -> AUDIO
    for x in core[1:]:
        e = byclip.get(x.get('clip'))
        if e is None:
            e = next((y for y in sc
                      if y['analayo']['lec'] == x['lec']
                      and abs(y['analayo']['start'] - x['start']) < 3), None)
        ev.append({'t': 'verbatim', 'text': (e.get('nanananda_verbatim', '') if e else ''),
                   'sermon': e.get('nanananda_sermon') if e else None})
        ev.append({'t': 'fish', 'beat': e['clip'] if e else None,
                   'say': e.get('tts_line', '') if e else ''})
        for d in tmap.get((s, (e['clip'] if e else -1)), []):
            ev.append({'t': 'fish-term',
                       'say': d.get('fish_says', d.get('say', '')),
                       'hears': d.get('hears', '')})
        ev.append({'t': 'breath', 'dur': 1.5})
        ev.append({'t': 'analayo', 'lec': x['lec'], 'start': x['start'],
                   'end': x['end'],
                   'dur': x.get('dur', round(x['end'] - x['start'], 1))})
        ev.append({'t': 'water', 'dur': 2.5})

    # ---- CLOSE
    if s < 6:
        ev.append({'t': 'zoom-bell'})
    else:
        ev += [{'t': 'seed-reprise'}, {'t': 'motto-bell'}, {'t': 'silence', 'dur': 30}]
    json.dump(ev, open('%s/assembly_s%d.json' % (td, s), 'w'), indent=1)
    print('S%d: %d events %s' % (s, len(ev), dict(Counter(x['t'] for x in ev))))
