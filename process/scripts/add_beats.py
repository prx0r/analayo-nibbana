"""Append hunt-found beats to core+script+manifest (2026-10-28, owner:
"implement these" — the 12 most-lucid finds). Appends ONLY (old clip/
beat numbers never shift). Plain lines via rebuild_text gloss+tts
(deterministic, same path as beats). ci = nearest core clip's cluster.
YT windows pre-converted to DS (see notes §74); L20 per-window measured.

Usage: python3 process/scripts/add_beats.py
Asserts G5-anchoring for every new quote BEFORE writing anything.
"""
import json
import re
import sys
from pathlib import Path

D = Path('/root/analayo-nibbana')
B = D / 'build' / 'canon'
sys.path.insert(0, str(D / 'process' / 'scripts'))
import rebuild_text as rt

# (section, lec, start, end, sermon, reason, verbatim)
BEATS = [
 (1, 8, 3517.9, 3521.7, 8, 'cessation-of-existence definition',
  "Nibbana has been defined as the cessation of existence. The Buddha says "
  "that when he is preaching about the cessation of existence, some people, "
  "particularly the brahmins who cling to a soul theory, bring up the charge "
  "of nihilism against him. Not only those brahmins and heretics believing "
  "in a soul theory, but even some Buddhist scholars are scared of the term "
  "bhavanirodha, fearing that it leads to a nihilistic interpretation."),
 (1, 18, 3616.0, 3621.9, 1, 'extinction as of a fire (elevenfold, not lamp)',
  "Existence is said to be an eleven-fold fire. So the entire existence "
  "is a raging fire. Lust, hate, delusion \u2014 all these are fires. "
  "Therefore Nibbana may be best rendered by the word 'extinction'."),
 (1, 14, 2487.0, 2495.0, 30, 'owning/grasping not (DS = YT-10.0)',
  "Not by views, nor by learning, nor by knowledge, nor yet by virtue "
  "and holy vows, they say, can purity come, neither can it come by "
  "without views, learning and knowledge, without virtue and holy vows, "
  "letting go of them all and grasping not one, that peaceful one, "
  "leaning on none, would hanker no more for existence."),
 (3, 11, 4698.4, 4708.0, 27, 'contact->feeling->proliferation chain (alt gloss)',
  "Dependent on eye and forms, friend, arises eye-consciousness; the "
  "concurrence of the three is contact; because of contact, feeling; "
  "what one feels, one perceives; what one perceives, one reasons about; "
  "what one reasons about, one proliferates; what one proliferates, "
  "owing to that, reckonings born of prolific perceptions overwhelm him "
  "in regard to forms cognizable by the eye relating to the past, the "
  "future and the present."),
 (3, 20, 2378.7, 2395.5, 20, 'craving bridges the gap, fuel (DS-measured)',
  "Like a promontory, it juts out into the ocean of samsara. When it "
  "comes to rebirth, it is craving that bridges the apparent gap."),
 (4, 16, 3387.2, 3401.0, 10, 'grasping-mirror, I-am occurs',
  "The magical illusion created by consciousness is so complete that it "
  "is capable of playing a dual role, as in double acting. Because it "
  "reflects, like a mirror, consciousness itself is grasped, just as one "
  "grasps the mirror. Not only the reflection of the mirror, but the "
  "mirror itself is grasped."),
 (4, 15, 1326.2, 1364.0, 23, 'peg drives grammar persons',
  "The primary significance of papa\u00f1ca is traceable to the linguistic "
  "medium. We have already shown how the network of grammar spreads as "
  "soon as the peg 'am' is driven down to earth, as it were. The reality "
  "in the first person in grammar beckons a second and a third person to "
  "complete the picture."),
 (4, 6, 1326.9, 1372.3, 6, 'painter fashions the self (DS = YT-1.5)',
  "Just as a dyer or a painter would fashion the likeness of a woman or "
  "of a man, complete in all its major and minor parts, on a well planed "
  "board, or a wall, or on a strip of cloth, with dye or lac or turmeric "
  "or indigo or madder, even so the untaught worldling creates, as it "
  "were, his own form, feelings, perceptions, preparations, and "
  "consciousness."),
 (5, 29, 981.1, 992.2, 29, 'develop the signless, drop conceit-latency',
  "Animitta\u00f1ca bh\u0101vehi, m\u0101n\u0101nusayamujjaha \u2014 'Develop the "
  "signless, too, and give up the latency to conceit!'"),
 (6, 19, 3993.5, 4014.7, 19, 'fire calms with no traceable path',
  "Just as in the case of a fire blazing like a block of iron in point "
  "of compactness, when it gradually calms down, no path it goes by can "
  "be traced."),
 (6, 28, 2901.8, 2915.8, 28, 'samsara as chess organic-vs-inorganic',
  "Our entire sa\u1e43s\u0101ric existence is a chess game between the organic, "
  "up\u0101di\u1e47\u1e47a, and the inorganic, anup\u0101di\u1e47\u1e47a. The four "
  "elements within this body, the grasped par excellence... and the four "
  "elements as nutrition and atmosphere are always in conflict in their "
  "game of chess."),
 (6, 5, 1753.4, 1764.4, 5, 'neither shore (Brahmin verse)',
  "For whom there is neither a farther shore, nor a hither shore, nor "
  "both, who is undistressed and unfettered, him I call a Brahmin."),
]


def norm(t):
    t = re.sub(r'\*', '', t)
    return re.sub(r'\s+', ' ', t)


def anchored(quotes):
    srcs = {}
    for f in sorted((D / 'sources' / 'sermons/excavations').glob('sermon-*.md')):
        srcs[f] = norm(open(f).read())
    bad = []
    for (s, q) in quotes:
        qn = norm(q).strip()
        if qn.startswith('"') and qn.endswith('"'):
            qn = qn[1:-1].strip()
        if not any((chr(34) + qn + chr(34)) in raw for raw in srcs.values()):
            bad.append((s, qn[:70]))
    return bad


def main():
    bad = anchored([(s, q) for (s, _, _, _, _, _, q) in BEATS])
    if bad:
        print('ANCHOR FAILURES (nothing written):')
        for b in bad:
            print('  ', b)
        raise SystemExit(1)
    print('anchors 12/12 OK')
    by_sec = {}
    for beat in BEATS:
        by_sec.setdefault(beat[0], []).append(beat)
    for s, beats in by_sec.items():
        core = json.load(open(B / f'seg{s}_core_v4.json'))
        scr = json.load(open(B / f'seg{s}_script.json'))
        terms = json.load(open(B / f'seg{s}_terms.json'))
        lines = open(B / f'manifest_s{s}_core_v4.txt').read().rstrip('\n').split('\n')
        # Clip numbers live in SCRIPT-land (max script clip +1). Core files
        # are inconsistent (S1 has clip keys, others don't) — only write a
        # core clip key where the file already uses them. (2026-10-28: the
        # first version numbered from core and collided in S3-S6; repaired.)
        has_clip = any('clip' in c for c in core)
        nxt = max(x.get('clip', 0) for x in scr) + 1
        for (sec, lec, ss, to, sermon, reason, q) in beats:
            ci = min(core, key=lambda c: abs(c.get('start', 0) - ss)
                     if c.get('lec') == lec else 1e18).get('ci', 0)
            dur = round(to - ss, 1)
            entry = {'lec': lec, 'start': ss, 'end': to, 'grade': 'A',
                     'dur': dur, 'ci': ci, 'ismotto': False,
                     'note': f'hunt-found ({reason}, owner 2026-10-28)'}
            if has_clip:
                entry['clip'] = nxt
            core.append(entry)
            below = rt.gloss(q)
            scr.append({'clip': nxt,
                        'analayo': {'lec': lec, 'start': ss, 'end': to,
                                    'dur': dur},
                        'nanananda_verbatim': q,
                        'nanananda_sermon': sermon,
                        'match': 0,
                        'override': None,
                        'plain_english_below': below,
                        'tts_line': rt.tts(below)})
            terms.append({'clip': nxt, 'lec': lec, 'start': ss, 'drops': []})
            lines.append(f'L{lec:02d} {ss}-{to} A lecture-{lec:02d}.mp3')
            print(f'  S{s} clip {nxt}: L{lec} [{ss}-{to}] {reason}')
            nxt += 1
        json.dump(core, open(B / f'seg{s}_core_v4.json', 'w'), indent=1)
        json.dump(scr, open(B / f'seg{s}_script.json', 'w'), indent=1)
        json.dump(terms, open(B / f'seg{s}_terms.json', 'w'), indent=1)
        open(B / f'manifest_s{s}_core_v4.txt', 'w').write('\n'.join(lines) + '\n')
    print('appended 12 beats (core+script+terms+manifests)')


if __name__ == '__main__':
    main()
