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
# Essay-0 AUDIO pointers (owner 2026-10-26: pointers, not explanations).
# Canonical single source: build/essay0_windows.json (all other ESSAY0
# copies were deleted — R6). TEXT still comes from the script beat
# (ESSAY0_BEAT below); only the spoken window is the pointer.
E0W = {int(k): v for k, v in
       json.load(open(td + '/essay0_windows.json')).items()}
# Essay-0 TEXT overrides (default: the essay-0 beat's verbatim). S2's text
# is the ignorance sentence alone (independently quoted S25 lines 88-90;
# full simile stays in S2c13 where the screen needs the dog named).
# Owner pick 2026-10-26. Plain/tts derived deterministically below.
ESSAY0_TEXT = {
    2: ("Due to the very ignorance of the fact that it is seeing because "
        "it is looking, the dog imagines another dog, there, in the water."),
}

# The 6 questions — lifted verbatim from build/human-scripts.md section headers.
# They ARE the 6-slot argument (process/12-ARGUMENT.md); Fish speaks them as-is.
QUESTIONS = {
    # THE FORMULA (process/12-ARGUMENT.md): every spine question passes
    # 4 tests — STANDALONE+PRECISE (subject named, named exactly as
    # the section answers it: "the self", not vague "I"; zero naked
    # pronouns),
    # THE CUT (turns the previous answer into tension for THIS listener,
    # now), CONTENT-FIT (that section's essay 0 answers it directly),
    # PLAIN (kick-off: 4-7 words, Fish speaks it flat — each question
    # is the next sentence the previous answer demands).
    1: "What is Nibbana?",
    2: "Why don't I see Nibbana right now?",
    3: "What keeps it going?",
    4: "How is the sense of self constructed?",
    5: "How is Nibbana attained?",
    6: "What is Nibbana like?",
}
# Essay 0 per section (the beat whose answer IS the question's reply).
# S2 b1 = the whirlpool-in-our-bodies quote on the L02 [5128-5193]
# window (Analayo speaks the answer aloud: "Samsara is a whirlpool as
# far as the ordinary beings caught up in it are concerned"). Replaced
# the motto-echo that merely repeated essay-0 unit 1 (owner: "2 doesnt
# answer the question for 2"). S3 b5 "What impels one to ignore that
# gap is craving" answers "What keeps it going?".
ESSAY0_BEAT = {1: 1, 2: 13, 3: 5, 4: 2, 5: 3, 6: 1}  # script clip per section: TEXT identity (audio: essay0_windows.json). S2=13 dog-seeing (owner pick 2026-10-26; was 1 whirlpool)

terms = {s: json.load(open('%s/seg%d_terms.json' % (td, s))) for s in range(1, 7)}
tmap = {}
for s in range(1, 7):
    for o in terms[s]:
        tmap[(s, o['clip'])] = o.get('drops', [])

for s in range(1, 7):
    core = json.load(open('%s/seg%d_core_v4.json' % (td, s)))
    sc = json.load(open('%s/seg%d_script.json' % (td, s)))
    byclip = {e['clip']: e for e in sc}

    # ---- OPENING (owner 2026-10-28): question -> PLAIN RESPONSE (Fish
    # guide voice, plain words) -> essay 0 (verbatim+plain on screen,
    # archive voice answers). The plain is the host beat's tts_line
    # (existing data); Fish speaks it, Analayo grounds it.
    oi = ESSAY0_BEAT[s] - 1
    b1 = core[oi]
    b1e = byclip.get(b1.get('clip'))
    if b1e is None:
        b1e = next((y for y in sc
                    if y['analayo']['lec'] == b1['lec']
                    and abs(y['analayo']['start'] - b1['start']) < 3), None)
    plain0 = (b1e.get('tts_line', '') if b1e else '')
    ev = [
        {'t': 'motto-bell'},
        {'t': 'fish', 'role': 'question', 'say': QUESTIONS[s]},
        {'t': 'pause', 'dur': 3.0, 'role': 'recollect',
         'note': 'listener tries to answer first - this pause IS the learning'},
        {'t': 'fish', 'role': 'plain', 'say': plain0,
         'note': 'PLAIN RESPONSE: the answer in plain words first (voice: Fish guide)'},
        {'t': 'verbatim',
         'text': ESSAY0_TEXT.get(s, (b1e.get('nanananda_verbatim', '') if b1e else '')),
         'plain': plain0,
         'sermon': (b1e.get('nanananda_sermon') if b1e else None),
         'essay': 0,
         'note': 'ESSAY 0 on screen: compressed answer (stack: verbatim over plain-english)'},
        {'t': 'analayo', 'lec': E0W[s]['lec'], 'start': E0W[s]['start'],
         'end': E0W[s]['end'],
         'dur': round(E0W[s]['end'] - E0W[s]['start'], 1),
         'note': 'ESSAY 0 AUDIO: pointer, not explanation (essay0_windows.json)'},
        {'t': 'water', 'dur': 2.5,
         'note': 'post-answer stillness: the answer lands before beats begin (2026-10-26 ear-pass: essay-0 slammed into beat-2 verbatim with zero pause)'},
        {'t': 'human-intro', 'ref': 'human-scripts.md section %d' % s,
         'status': 'optional-pending',
         'note': 'only if used: AFTER the answer, never between question and motto'},
    ]
    if s in ESSAY0_TEXT:  # override text: deterministic gloss (same key path as beats)
        import sys as _sys
        _sys.path.insert(0, '/root/analayo-nibbana/process/scripts')
        import rebuild_text as _rt
        _plain = _rt.tts(_rt.gloss(ev[4]['text']))
        ev[3]['say'] = _plain  # Fish plain response matches screen
        ev[4]['plain'] = _plain

    # ---- BEATS 2..N: fixed stack TEXT VERBATIM -> PLAIN ENGLISH -> AUDIO
    for i, x in enumerate(core):
        if i == oi:          # essay-0 beat already consumed by the opening
            continue
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
        # Water scales with clip weight (owner 2026-10-26): flat 2.5s after
        # a 40s clip is right; after a 5-minute exegesis the listener needs
        # a breath. 2.5s base + 1s per 60s, capped at 6s.
        ev.append({'t': 'water',
                   'dur': min(6.0, round(2.5 + x.get('dur', round(x['end'] - x['start'], 1)) / 60.0, 1))})

    # ---- CLOSE
    if s < 6:
        ev.append({'t': 'zoom-bell'})
        # Section-boundary stillness (owner 2026-10-26): the question
        # changes, the listener needs a reset. 6s settle AFTER the bell —
        # sections must not blur into each other.
        ev.append({'t': 'pause', 'dur': 6.0, 'role': 'settle',
                   'note': 'section boundary stillness after zoom-bell'})
    else:
        ev += [{'t': 'seed-reprise'}, {'t': 'motto-bell'}, {'t': 'silence', 'dur': 30}]
    json.dump(ev, open('%s/assembly_s%d.json' % (td, s), 'w'), indent=1)
    print('S%d: %d events %s' % (s, len(ev), dict(Counter(x['t'] for x in ev))))
