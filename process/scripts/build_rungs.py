"""Build ladder rungs B/C/D (2026-10-28, owner: 10/25/45 min per q).

Full ladder: 0 seed 2m -> A newA ~3m/q -> B 10m/q -> C 25m/q ->
D 45m/q -> archive 20h (reference only). Analayo-only throughout
(verbatim+plain on screen; Fish questions + Analayo audio).

- B: whole old-A where it fits (S1 9.2m, S4 4.9m), else curated
  assembly-beat subsets (S2/S3/S5/S6) with reasons.
- C/D: full old-A + gold head-fill in manifest listen order,
  skipping spans overlapping core (>50%, same passage) to budgets
  1500s / 2700s (+40s slack). Fill cost = dur + 10s seams.

Usage: python3 process/scripts/build_rungs.py
Writes build/canon/ladder_manifest.json (rungs B/C/D). Asserts budgets.
"""
import json
import re
from pathlib import Path

D = Path('/root/analayo-nibbana')
B = D / 'build' / 'canon'
BUDGETS = {'B': 600.0, 'C': 1200.0, 'D': 2700.0}
SLACK = 40.0

# B curated subsets: assembly beat numbers, PLUS gold-tuple picks
# ('gold', lec, start, end, reason) for spans the assembly doesn't hold.
# FINAL PASS 2026-10-29 (owner: merge B+C, question by question):
# S1 +b12/b13 hunt definitions (catechism↔B9 swap DEFERRED to owner —
# deletes sa-upadisesa from all listening); S2 +gold mirror-image;
# S3 +Colombo/+Being-eq/+Mula displacing B2/B5/B15; S4 +Kevaddha verse/
# +sankhata-debate/+tangle-snapped; S5 +grasp/+smoked/+raft displacing
# Upatissa b7; S6 +b9-prepared/+b5-unknot/+lotus-leaf.
# Every gold pick below ALSO lands in C (C base = full B unit list),
# so B⊂C holds by construction; post-build asserts verify it.
GOLD = lambda lec, ss, to, why: ('gold', lec, ss, to, why)
B_PICKS = {
    1: [(1, 'pointer motto'), (2, 'fire/lamp'),
        (3, 'CONTRADICTION (owner: FIRST)'),
        (4, 'Vaccha undesignable'), (5, 'warming vs cooling'),
        (6, 'third-truth resolution'), (7, 'quenched thirst'),
        (8, 'motto refrain'), (9, 'sa-upadisesa'),
        (10, 'oil-lamp cooling'), (11, 'debt/freedom'),
        (12, 'cessation-of-existence definition (hunt)'),
        (13, 'elevenfold fire = extinction (hunt)')],
    2: [(1, 'pointer TRIPLE (owner §74)'), (2, 'whirlpool bodies'),
        (8, 'ignorance dethroned — not first either'),
        (10, 'akalika immediacy'), (11, 'three-periods warrant'),
        (12, 'banana cut'), (13, 'Channa payoff'),
        GOLD(10, 537.3, 568.5, 'mirror-image knowledge-vision (P2)')],
    3: [(1, 'pointer craving-gap'),
        (4, 'honey chain'),
        (9, 'steadied'), (10, 'no-delight-in-Nibbana'),
        (16, 'contact-chain alt gloss (hunt)'),
        (17, 'craving bridges gap (hunt)'),
        GOLD(12, 1156.1, 1218.6, 'Colombo/pamada-vs-papanca parable (P5)'),
        GOLD(21, 4181.5, 4200.0, 'Being equation (P4)'),
        GOLD(13, 804.2, 833.0, 'Mula non-imagining (P10)')],
    4: None,  # whole (old-A + hunt beats 6-8) + S4_GOLDS below
    5: [(1, 'pointer Bahiya'), (3, 'dhono stance'),
        (4, 'razor warning'), (5, 'honing technique'),
        (8, 'postures monodrama'),
        (12, 'longing licensed'), (13, 'lotus result'),
        (14, 'raft close'),
        (15, 'develop the signless (hunt)'),
        GOLD(8, 3843.7, 3906.1, 'grasp-in-the-middle (razor why)'),
        GOLD(29, 3026.2, 3033.0, 'smoked-out-without-residue'),
        GOLD(18, 2366.6, 2381.3, 'raft-abandon verse')],
    6: [(1, 'pointer grown-cool'), (2, 'chessboard'),
        (3, 'peaceful draw'), (4, 'lotuses'),
        (5, 'unknot (S33 triptych 1/3)'),
        (8, 'faculties chain'), (9, 'prepared->unprepared (S32 charter)'),
        (11, 'magic-show seen through'),
        (13, 'detached close'),
        (14, 'fire-no-path (hunt)'), (15, 'chess organic (hunt)'),
        (16, 'neither shore (hunt)'),
        GOLD(18, 1183.3, 1195.9, 'lotus-leaf sage')],
}
S4_GOLDS = [  # S4 whole old-A + these (all already C head-fills)
    GOLD(7, 663.0, 685.5, 'Kevaddha charter verse (P1)'),
    GOLD(2, 2154.9, 2219.0, 'sankhata/atta firewall'),
    GOLD(10, 4263.6, 4283.5, 'tangle snapped (S10 climax)'),
]


def abeats(asm):
    """Beat split with STABLE numbering (see build_newA.beats)."""
    anas = [i for i, e in enumerate(asm) if e['t'] == 'analayo']
    j = 0
    while j < len(anas) and asm[anas[j]].get('essay') == 0:
        j += 1
    assert j >= 1, 'no essay-0 pointer'
    out = {1: asm[:anas[j - 1] + 1]}
    cur, n = [], 1
    for e in asm[anas[j - 1] + 1:]:
        cur.append(e)
        if e['t'] == 'analayo':
            n += 1
            out[n] = cur
            cur = []
    return out


def core_windows(n):
    d = json.load(open(B / f'seg{n}_core_v4.json'))
    clips = d if isinstance(d, list) else d.get('clips', [])
    return [(c['lec'], c['start'], c['end']) for c in clips]


def overlaps_core(lec, ss, to, cw):
    for (l, a, b) in cw:
        if l == lec and max(0, min(to, b) - max(ss, a)) > 0.5 * min(to - ss, b - a):
            return True
    return False


def parse_gold_txt(n):
    out = []
    for line in open(B / f'manifest_s{n}_gold.txt').read().strip().split('\n'):
        m = re.match(r'L(\d+)\s+([\d.]+)-([\d.]+)\s+([ABC*]+)', line)
        if m:
            out.append((int(m.group(1)), float(m.group(2)),
                        float(m.group(3)), m.group(4)))
    return out


def gold_unit(lec, ss, to, reason):
    return {'beat': f'gold@{lec}:{ss:.0f}', 'reason': reason,
            'analayo': {'lec': lec, 'start': ss, 'end': to,
                        'dur': round(to - ss, 1)}}


def beat_unit(ab, b, reason):
    anas = [e for e in ab[b] if e['t'] == 'analayo']
    ana = anas[0]
    return {'beat': b, 'reason': reason,
            'analayo': {'lec': ana['lec'], 'start': ana['start'],
                        'end': ana['end'], 'dur': ana['dur']}}


def main():
    man = {'budgets': BUDGETS, 'rule': 'analayo-only', 'rungs': {}}
    # taken[(rung, n)] = set of unit keys, for nesting B⊂C⊂D: D starts
    # from exactly what C took (greedy is not budget-monotone, so force it).
    taken, totals = {}, {}
    bunits = {}  # section -> resolved B unit dicts (beats + golds)
    for n in range(1, 7):
        asm = json.load(open(B / f'assembly_s{n}.json'))
        ab = abeats(asm)
        picks = B_PICKS[n]
        if picks is None:
            picks = [(b, 'whole old-A fits' if b == 1 else 'whole old-A')
                     for b in sorted(ab)]
            if n == 4:
                picks = picks + S4_GOLDS
        units = []
        for p in picks:
            if isinstance(p[0], str) and p[0] == 'gold':
                _, lec, ss, to, reason = p
                units.append(gold_unit(lec, ss, to, reason))
            else:
                b, reason = p
                units.append(beat_unit(ab, b, reason))
        bunits[n] = units
    for rung, budget in BUDGETS.items():
        rsec = {}
        for n in range(1, 7):
            asm = json.load(open(B / f'assembly_s{n}.json'))
            ab = abeats(asm)
            Q = next(e['say'] for e in asm
                     if e['t'] == 'fish' and e.get('role') == 'question')
            if rung == 'B':
                base = [(u, u.get('reason', '')) for u in bunits[n]]
            else:
                base = [(u, u.get('reason', '')) for u in bunits[n]] + [
                    (beat_unit(ab, b, 'old-A remainder (prefix order)'),
                     'old-A remainder (prefix order)')
                    for b in sorted(ab)
                    if not any(u.get('beat') == b for u in bunits[n])]
            beats, total = [], 7.0
            if rung == 'D' and (n in taken):
                # seed from C takes (nesting forced, not greedy)
                for (key, unit, cost) in taken[n]:
                    beats.append(unit)
                    total += cost
                seedkeys = {k for k, _, _ in taken[n]}
            else:
                seedkeys = set()
            for (unit_t, reason) in base:
                bu = unit_t.get('beat')
                if isinstance(bu, str) and bu.startswith('gold@'):
                    a0 = unit_t['analayo']
                    key = ('gold', a0['lec'], round(a0['start'], 1))
                else:
                    key = ('beat', bu)
                if key in seedkeys:
                    continue
                anas = [unit_t['analayo']]
                cost = sum(a['dur'] for a in anas) + 8.0
                if rung in ('C', 'D') and total + cost > budget + SLACK:
                    continue
                total += cost
                unit = {'beat': unit_t['beat'], 'reason': reason,
                        'analayo': dict(unit_t['analayo'])}
                beats.append(unit)
                if rung == 'C':
                    taken.setdefault(n, []).append((key, unit, cost))
            if rung in ('C', 'D'):
                cw = core_windows(n)
                for (lec, ss, to, grade) in parse_gold_txt(n):
                    key = ('gold', lec, round(ss, 1))
                    if key in seedkeys or any(
                            k == key for k, _, _ in taken.get(n, [])):
                        # D re-take of C's gold: re-add from record below
                        pass
                    if rung == 'D' and key in {k for k, _, _ in taken.get(n, [])}:
                        continue  # added from C record (already counted)
                    if overlaps_core(lec, ss, to, cw):
                        continue
                    if any(abs(x['analayo']['start'] - ss) < 2
                           and x['analayo']['lec'] == lec for x in beats):
                        continue
                    cost = (to - ss) + 10.0
                    if total + cost > budget + SLACK:
                        continue
                    total += cost
                    unit = {'beat': f'gold@{lec}:{ss:.0f}',
                            'reason': 'gold head-fill (manifest order)',
                            'analayo': {'lec': lec, 'start': ss,
                                        'end': to,
                                        'dur': round(to - ss, 1)}}
                    beats.append(unit)
                    if rung == 'C':
                        taken.setdefault(n, []).append((key, unit, cost))
                    if total >= budget:
                        break
            print(f'{rung} S{n}: {total:.0f}s ({len(beats)} units) '
                  f'{"OVER" if total > budget + SLACK else "ok"}', flush=True)
            assert total <= budget + SLACK, f'{rung} S{n} over budget'
            rsec[str(n)] = {'question': Q, 'total_s': round(total, 1),
                            'units': beats}
        man['rungs'][rung] = rsec
    # NESTING LAW (2026-10-29 final pass): B⊂C per section, by window
    # containment (everything heard in B reappears in C). C = B-prefix +
    # old-A remainders-that-fit + gold fills (greedy under budget); spans
    # that don't fit live in D/pool — reported below, not failed.
    # (Old-A completeness was never true: S2 beats 6/7/9 = Kalaha-deepest-joint /
    # physician-breach / prepared-cessation were deliberately placed in D.)
    for n in map(str, range(1, 7)):
        asm = json.load(open(B / f'assembly_s{n}.json'))
        ab = abeats(asm)
        oldA = set(ab)
        cbeats = {u['beat'] for u in man['rungs']['C'][n]['units']
                  if isinstance(u.get('beat'), int)}
        missing = sorted(oldA - cbeats)
        if missing:
            print(f'C-S{n} old-A absent (in D/pool by design): {missing}',
                  flush=True)
        cw = [(u['analayo']['lec'], u['analayo']['start'], u['analayo']['end'])
              for u in man['rungs']['C'][n]['units']]
        for u in man['rungs']['B'][n]['units']:
            a = u['analayo']
            assert any(l == a['lec'] and cs <= a['start'] and a['end'] <= ce
                       for (l, cs, ce) in cw), \
                f'B-S{n} beat {u["beat"]} not contained in C'
        print(f'nesting S{n}: B({len(man["rungs"]["B"][n]["units"])}) ⊂ C ok',
              flush=True)
    (B / 'ladder_manifest.json').write_text(json.dumps(man, indent=1) + '\n')
    print('wrote build/canon/ladder_manifest.json')


if __name__ == '__main__':
    main()
