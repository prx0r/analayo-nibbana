"""G7 essay gates — called by process/verify.sh.

Validates the ARGUMENT structure (process/12-ARGUMENT.md), which no
other gate touches: the question chain, the essay-0 openers, and the
length ladder. A section can pass provenance/TTS and still be
meaningless if its opener answers the wrong question — that is the
failure class this gate exists for (S2/S5 motto-echoes, 2026-10-24).

Checks:
  G7a structure  — per section: event order is exactly
                   motto-bell -> fish(question) -> pause -> verbatim(essay 0,
                   non-empty text+plain) -> analayo(audio); question
                   non-empty, ends in '?', all 6 distinct.
  G7b chain      — regression canary: for s2..s6 the essay-0 verbatim
                   must NOT be the motto ("This is peaceful..."). The
                   motto answers Q1 only; if it reappears as another
                   section's opener, the chain is broken. (This is the
                   S2/S5 failure, pinned as a permanent test.)
  G7c gold-dust  — essay 0 is compressed: plain <= 80 words (soft),
                   verbatim <= 600 chars; prints every essay 0 with its
                   length so the human sees the gold.

Prints the six essay 0s + the A/B/C length ladder (core/gold/pool) so
"output essay 0" is one command: python3 process/scripts/g7_essay_check.py
"""
import json
import re
import sys

D = '/root/analayo-nibbana/build'
QUESTIONS_EXPECTED = {
    1: "What is Nibbana?",
    2: "What keeps it all going?",
    3: "Is any of it real?",
    4: "What am I made of?",
    5: "How do I see through it?",
    6: "What's left when the show stops?",
}
# essay 0 lengths (soft budget)
PLAIN_MAX_WORDS = 80
VERBATIM_MAX_CHARS = 600


def words(s):
    return len([w for w in re.split(r'\s+', s) if w.strip()])


def main():
    bad = []
    print('== G7 essay gates (structure + chain + gold-dust) ==')
    print('-- essay 0, per section --')
    for s in range(1, 7):
        ev = json.load(open('%s/assembly_s%d.json' % (D, s)))
        # structure: first five events in fixed order
        head = [e['t'] for e in ev[:5]]
        want = ['motto-bell', 'fish', 'pause', 'verbatim', 'analayo']
        if head != want:
            bad.append(('S%d' % s, 'open-order', head))
        if len(ev) < 5:
            bad.append(('S%d' % s, 'too-short', len(ev)))
            continue
        q, pb, vb, an = ev[1], ev[2], ev[3], ev[4]
        # G7a: question sane
        if q.get('role') != 'question':
            bad.append(('S%d' % s, 'no-question-role', q.get('role')))
        qtxt = q.get('say', '')
        if qtxt != QUESTIONS_EXPECTED.get(s):
            bad.append(('S%d' % s, 'question-unsynced', qtxt))
        if not qtxt.endswith('?') or not qtxt.strip():
            bad.append(('S%d' % s, 'not-a-question', qtxt))
        # essay 0 present
        vtxt = vb.get('text', '')
        if isinstance(vtxt, list):
            vtxt = ' // '.join(str(x) for x in vtxt)
        pt = vb.get('plain', '')
        if vb.get('essay') != 0:
            bad.append(('S%d' % s, 'essay-tag', vb.get('essay')))
        if not vtxt.strip():
            bad.append(('S%d' % s, 'essay0-empty-verbatim', ''))
        if not pt.strip():
            bad.append(('S%d' % s, 'essay0-empty-plain', ''))
        if an.get('start') is None:
            bad.append(('S%d' % s, 'essay0-no-audio', ''))
        # G7c gold-dust budgets
        w, c = words(pt), len(vtxt)
        if w > PLAIN_MAX_WORDS:
            bad.append(('S%d' % s, 'essay0-fat-plain-%dwords' % w, ''))
        if c > VERBATIM_MAX_CHARS:
            bad.append(('S%d' % s, 'essay0-fat-verbatim-%dch' % c, ''))
        print('  S%d "%s"' % (s, qtxt))
        print('     %3dw plain  %4dch verbatim  audio L%s[%s]s' % (
            w, c, an.get('lec'), an.get('dur')))
        print('     0: %s' % re.sub(r'\s+', ' ', vtxt)[:110])
    # distinct questions
    qs = [QUESTIONS_EXPECTED[s] for s in range(1, 7)]
    if len(set(qs)) != 6:
        bad.append(('chain', 'questions-not-distinct', len(set(qs))))
    # G7b motto-echo regression (the S2/S5 failure, pinned)
    for s in range(2, 7):
        ev = json.load(open('%s/assembly_s%d.json' % (D, s)))
        vtxt = ev[3].get('text', '')
        if isinstance(vtxt, list):
            vtxt = ' // '.join(str(x) for x in vtxt)
        if re.match(r'\s*(This is peaceful|This is sublime)', vtxt):
            bad.append(('S%d' % s, 'MOTTO-ECHO: opener answers Q1, not this Q', vtxt[:60]))
    print('-- length ladder (essay a=core, b=gold, c=pool; s0=answer) --')
    for s in range(1, 7):
        core = json.load(open('%s/seg%d_core_v4.json' % (D, s)))
        gold = json.load(open('%s/seg%d_gold.json' % (D, s)))
        pool = json.load(open('%s/seg%d_pool.json' % (D, s)))
        cm = sum(x['dur'] for x in core) / 60
        gm = sum(x['dur'] for x in gold) / 60
        pm = sum(x['dur'] for x in pool) / 60
        print('  S%d: 0=~20s | a=%4.1fm | b=%4.1fm | c=%5.1fm' % (s, cm, gm, pm))
    tc = sum(sum(x['dur'] for x in json.load(open('%s/seg%d_core_v4.json' % (D, s)))) for s in range(1, 7)) / 60
    tg = sum(sum(x['dur'] for x in json.load(open('%s/seg%d_gold.json' % (D, s)))) for s in range(1, 7)) / 60
    tp = sum(sum(x['dur'] for x in json.load(open('%s/seg%d_pool.json' % (D, s)))) for s in range(1, 7)) / 60
    print('  ALL: a=%.1fm  b=%.1fm  c=%.1fh' % (tc, tg, tp / 60))
    if bad:
        for b in bad:
            print('  FAIL', b)
        print('G7 FAILED (%d)' % len(bad))
        return 1
    print('G7 essay gates: OK')
    return 0


if __name__ == '__main__':
    sys.exit(main())
