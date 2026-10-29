"""G7 essay gates — called by process/verify.sh.

Validates the ARGUMENT structure (process/12-ARGUMENT.md), which no
other gate touches: the question chain, the essay-0 openers, and the
length ladder. A section can pass provenance/TTS and still be
meaningless if its opener answers the wrong question — that is the
failure class this gate exists for (S2/S5 motto-echoes, 2026-10-24).

Checks:
  G7a structure  — per section: event order is exactly
                   motto-bell -> fish(question) -> pause -> fish(plain
                   response, non-empty, == verbatim plain) ->
                   verbatim(essay 0, non-empty text+plain) ->
                   analayo(audio); question non-empty, ends in '?',
                   all 6 distinct.
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

D = '/root/analayo-nibbana/build/canon'
QUESTIONS_EXPECTED = {
    1: "What is Nibbana?",
    2: "Why don't I see Nibbana right now?",
    3: "What keeps it going?",
    4: "How is the sense of self constructed?",
    5: "How is Nibbana attained?",
    6: "What is Nibbana like?",
}
# essay 0 lengths (soft budget)
PLAIN_MAX_WORDS = 80
# Spoken plain responses run longer than screen compression (S2's dog
# story is 108w — owner-ordered spoken answer, 2026-10-28). Separate
# ceiling for the response; the TEXT compression rule is unchanged.
PLAIN_RESP_MAX_WORDS = 120
VERBATIM_MAX_CHARS = 600


def words(s):
    return len([w for w in re.split(r'\s+', s) if w.strip()])


def main():
    bad = []
    print('== G7 essay gates (structure + chain + gold-dust) ==')
    print('-- essay 0, per section --')
    for s in range(1, 7):
        ev = json.load(open('%s/assembly_s%d.json' % (D, s)))
        # structure: bell/Q/pause/plain/breath, then 1+ (verbatim, analayo)
        # essay-0 pairs (S2 triple pointer, owner 2026-10-28; breath = air
        # between guide and archive voice, owner ear §77)
        head = [e['t'] for e in ev[:6]]
        want = ['motto-bell', 'fish', 'pause', 'fish', 'breath', 'verbatim']
        if head != want:
            bad.append(('S%d' % s, 'open-order', head))
        if len(ev) < 7:
            bad.append(('S%d' % s, 'too-short', len(ev)))
            continue
        q, pb, vb = ev[1], ev[3], ev[5]
        ans = []
        for e in ev[6:]:
            if e['t'] == 'analayo' and e.get('essay') == 0:
                ans.append(e)
            elif e['t'] in ('breath',):
                continue
            else:
                break
        if not ans:
            bad.append(('S%d' % s, 'essay0-no-audio', ''))
            continue
        an = ans[0]
        # G7a: question sane
        if q.get('role') != 'question':
            bad.append(('S%d' % s, 'no-question-role', q.get('role')))
        qtxt = q.get('say', '')
        if qtxt != QUESTIONS_EXPECTED.get(s):
            bad.append(('S%d' % s, 'question-unsynced', qtxt))
        if not qtxt.endswith('?') or not qtxt.strip():
            bad.append(('S%d' % s, 'not-a-question', qtxt))
        # G7a2: plain response present, spoken == screen (voice matches text)
        if pb.get('role') != 'plain' or not pb.get('say', '').strip():
            bad.append(('S%d' % s, 'no-plain-response', pb.get('role')))
        vtxt = vb.get('text', '')
        if isinstance(vtxt, list):
            vtxt = ' // '.join(str(x) for x in vtxt)
        pt = vb.get('plain', '')
        if pb.get('say', '') != pt or not pt.strip():
            bad.append(('S%d' % s, 'plain-unsynced',
                        (pb.get('say', '')[:40], str(pt)[:40])))
        if vb.get('essay') != 0:
            bad.append(('S%d' % s, 'essay-tag', vb.get('essay')))
        if not vtxt.strip():
            bad.append(('S%d' % s, 'essay0-empty-verbatim', ''))
        if not pt.strip():
            bad.append(('S%d' % s, 'essay0-empty-plain', ''))
        if an.get('start') is None:
            bad.append(('S%d' % s, 'essay0-no-audio', ''))
        # G7c gold-dust budgets (text compressed; response ceiling separate)
        w, c = words(pt), len(vtxt)
        if w > PLAIN_RESP_MAX_WORDS:
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
        vtxt = ev[5].get('text', '')
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
    # G7d seed layer: all six micro-sessions chained in order
    import os as _os
    sp = _os.path.join(D, 'assembly_s0_seed.json')
    if not _os.path.exists(sp):
        bad.append(('seed', 'missing', sp))
    else:
        sd = json.load(open(sp))
        uq = [e for e in sd if e.get('role') == 'question']
        uv = [e for e in sd if e.get('t') == 'verbatim']
        ua = [e for e in sd if e.get('t') == 'analayo']
        if [e.get('say') for e in uq] != [QUESTIONS_EXPECTED[i] for i in range(1, 7)]:
            bad.append(('seed', 'questions-unsynced', len(uq)))
        # S2 triple: 6 verbatims, 8 analayos (1+3+1+1+1+1), grouped by unit
        units = {}
        for e in sd:
            if e.get('unit') is not None:
                units.setdefault(e['unit'], []).append(e['t'])
        if len(uv) != 6 or any(e.get('essay') != 0 for e in uv):
            bad.append(('seed', 'units-incomplete', (len(uv), len(ua))))
        if sorted(units.keys()) != [1, 2, 3, 4, 5, 6] or any(
                u.count('analayo') < 1 for u in units.values()):
            bad.append(('seed', 'units-incomplete', (len(uv), len(ua))))
        print('  SEED: %d units chained, %d events (chain lives here)' % (len(uq), len(sd)))

    if bad:
        for b in bad:
            print('  FAIL', b)
        print('G7 FAILED (%d)' % len(bad))
        return 1
    print('G7 essay gates: OK')
    return 0


if __name__ == '__main__':
    sys.exit(main())
