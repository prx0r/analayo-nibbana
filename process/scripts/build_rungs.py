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

# B curated subsets (assembly beat numbers; S1/S4 = whole old-A).
B_PICKS = {
    1: [(1, 'pointer motto'), (2, 'fire/lamp'),
        (3, 'CONTRADICTION (owner: FIRST)'),
        (4, 'Vaccha undesignable'), (5, 'warming vs cooling'),
        (6, 'third-truth resolution'), (7, 'quenched thirst'),
        (8, 'motto refrain'), (9, 'sa-upadisesa'),
        (10, 'oil-lamp cooling'), (11, 'debt/freedom')],
    2: [(1, 'pointer TRIPLE (owner §74)'), (2, 'whirlpool bodies'),
        (8, 'ignorance dethroned — not first either'),
        (10, 'akalika immediacy'), (11, 'three-periods warrant'),
        (12, 'banana cut'), (13, 'Channa payoff')],
    3: [(1, 'pointer craving-gap'), (2, 'nominal terrain'),
        (4, 'honey chain'), (5, 'delight-in-existence'),
        (9, 'steadied'), (10, 'no-delight-in-Nibbana'),
        (15, 'barb close'),
        (16, 'contact-chain alt gloss (hunt)'),
        (17, 'craving bridges gap (hunt)')],
    4: None,  # whole (old-A + hunt beats 6-8)
    5: [(1, 'pointer Bahiya'), (3, 'dhono stance'),
        (4, 'razor warning'), (5, 'honing technique'),
        (7, 'Upatissa proof'), (8, 'postures monodrama'),
        (12, 'longing licensed'), (13, 'lotus result'),
        (14, 'raft close'),
        (15, 'develop the signless (hunt)')],
    6: [(1, 'pointer grown-cool'), (2, 'chessboard'),
        (3, 'peaceful draw'), (4, 'lotuses'),
        (8, 'faculties chain'), (11, 'magic-show seen through'),
        (13, 'detached close'),
        (14, 'fire-no-path (hunt)'), (15, 'chess organic (hunt)'),
        (16, 'neither shore (hunt)')],
}


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


def main():
    man = {'budgets': BUDGETS, 'rule': 'analayo-only', 'rungs': {}}
    # taken[(rung, n)] = set of unit keys, for nesting B⊂C⊂D: D starts
    # from exactly what C took (greedy is not budget-monotone, so force it).
    taken, totals = {}, {}
    for rung, budget in BUDGETS.items():
        rsec = {}
        for n in range(1, 7):
            asm = json.load(open(B / f'assembly_s{n}.json'))
            ab = abeats(asm)
            Q = next(e['say'] for e in asm
                     if e['t'] == 'fish' and e.get('role') == 'question')
            if rung == 'B' and B_PICKS[n] is None:
                picks = [(b, 'whole old-A fits' if b == 1 else 'whole old-A')
                         for b in sorted(ab)]
            elif rung == 'B':
                picks = B_PICKS[n]
            else:
                base = (B_PICKS[n] if B_PICKS[n] is not None
                        else [(b, 'whole old-A') for b in sorted(ab)])
                have = {b for b, _ in base}
                picks = list(base) + [
                    (b, 'old-A remainder (prefix order)')
                    for b in sorted(ab) if b not in have]
            beats, total = [], 7.0
            if rung == 'D' and (n in taken):
                # seed from C takes (nesting forced, not greedy)
                for (key, unit, cost) in taken[n]:
                    beats.append(unit)
                    total += cost
                seedkeys = {k for k, _, _ in taken[n]}
            else:
                seedkeys = set()
            for (b, reason) in picks:
                key = ('beat', b)
                if key in seedkeys:
                    continue
                anas = [e for e in ab[b] if e['t'] == 'analayo']
                ana = anas[0]
                cost = sum(a['dur'] for a in anas) + 8.0
                if rung in ('C', 'D') and total + cost > budget + SLACK:
                    continue
                total += cost
                unit = {'beat': b, 'reason': reason,
                        'analayo': {'lec': ana['lec'],
                                    'start': ana['start'],
                                    'end': ana['end'],
                                    'dur': ana['dur']}}
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
    (B / 'ladder_manifest.json').write_text(json.dumps(man, indent=1) + '\n')
    print('wrote build/canon/ladder_manifest.json')


if __name__ == '__main__':
    main()
