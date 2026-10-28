"""Build the new A rung: 5 min/question highest-signal (2026-10-28).

Ladder after the left-shift: 0 seed 2m -> newA 30m -> B old-A 90m ->
C old-B 7h -> D archive. Curator picks (ASSEMBLY beat numbers, pointer
= 1st analayo) with reasons.

ANALAYO-ONLY rule (owner 2026-10-28): ears get one voice. Verbatim TEXT
+ plain live ON SCREEN (kept in the manifest as the screen script);
audio is Fish questions + Analayo clips only. No sermon-reader audio,
no plain voice — no voice switching, no alignment dependency.

Usage: python3 process/scripts/build_newA.py
Writes build/newA_manifest.json. Asserts every section <= 340s.
Cost = Analayo + 8s pauses/beat + 7s Q (no reader, no plain voice).
"""
import json
from pathlib import Path

D = Path('/root/analayo-nibbana')
B = D / 'build'
ESSAY0_BEAT = {1: 1, 2: 13, 3: 5, 4: 2, 5: 3, 6: 1}
BUDGET = 340.0

# section: [(assembly_beat, reason)] — beat 1 is always the pointer.
PICKS = {
    1: [(1, 'pointer motto'),
        (3, 'CONTRADICTION in commentarial definitions (owner: FIRST)'),
        (6, 'third-truth resolution — mass of suffering just before us'),
        (11, 'debt/freedom — payoff, not debt')],
    2: [(1, 'pointer dog-ignorance'),
        (2, 'whirlpool bodies — what the blind are caught in'),
        (10, 'akalika immediacy — seen here and now')],
    3: [(1, 'pointer craving-gap'),
        (4, 'honey-ball chain — the centerpiece')],
    4: [(1, 'pointer mirror+mechanism'),
        (2, 'anidassana — what is not constructed'),
        (5, 'barb — the hook')],
    5: [(1, 'pointer Bahiya'),
        (4, 'razor warning — grasping ruins the tool'),
        (5, 'honing strokes — technique after warning (§37 pair)')],
    6: [(1, 'pointer grown-cool'),
        (2, 'chessboard — the vision'),
        (4, 'myriad lotuses — bloom'),
        (11, 'magic-show seen from the stage')],
}


def beats(asm):
    """Split assembly events into beats: opening + one per analayo."""
    out, cur, n_ana = [], [], 0
    for e in asm:
        cur.append(e)
        if e['t'] == 'analayo':
            n_ana += 1
            out.append((n_ana, cur))
            cur = []
    return out  # beat 1 = pointer (opening incl bell/Q)


def main():
    man = {'budget_s': BUDGET, 'rule': 'analayo-only', 'sections': {}}
    for n in range(1, 7):
        asm = json.load(open(B / f'assembly_s{n}.json'))
        scr = json.load(open(B / f'seg{n}_script.json'))
        e0plain = next(s.get('plain_english_below', '')
                       for s in scr if s.get('clip') == ESSAY0_BEAT[n])
        Q = next(e['say'] for e in asm
                 if e['t'] == 'fish' and e.get('role') == 'question')
        ab = dict(beats(asm))
        sec = {'question': Q, 'pointer': None, 'beats': [], 'total_s': 0.0}
        total = 7.0  # Q + recollect
        for (b, reason) in PICKS[n]:
            evs = ab[b]
            verb = next(e for e in evs if e['t'] == 'verbatim')
            ana = next(e for e in evs if e['t'] == 'analayo')
            vtext = verb.get('text', '')
            plain = e0plain if b == 1 else ''
            cost = ana['dur'] + 8.0
            total += cost
            unit = {'beat': b, 'reason': reason,
                    'screen_verbatim': vtext,
                    'screen_plain': plain,
                    'analayo': {'lec': ana['lec'], 'start': ana['start'],
                                'end': ana['end'], 'dur': ana['dur']},
                    'cost_s': round(cost, 1)}
            if b == 1:
                sec['pointer'] = unit
            else:
                sec['beats'].append(unit)
        sec['total_s'] = round(total, 1)
        print(f"S{n}: {sec['total_s']}s "
              f"({'OVER' if total > BUDGET else 'ok'}) "
              f"beats={[u['beat'] for u in [sec['pointer']] + sec['beats']]}",
              flush=True)
        assert total <= BUDGET, f'S{n} over budget'
        man['sections'][str(n)] = sec
    (B / 'newA_manifest.json').write_text(json.dumps(man, indent=1) + '\n')
    print('wrote build/newA_manifest.json')


if __name__ == '__main__':
    main()
