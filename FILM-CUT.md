# FILM-CUT — the five-hour version (lab/c-split, recomputed 2026-10-28
from build/film_manifest.json; recompute: sum chapter depth durs)

Built from visuals/FIVE-HOUR-CUT.md. Membership manifest:
`build/film_manifest.json` — every clip assigned to its EARLIEST depth,
gates: `process/scripts/g8_film_check.py` (wired into verify.sh as G8).

## Method
- Rung 0 = the seed's essay-0 windows (atomic source clips, uncut).
- A/B/C fill per chapter to the FIVE-HOUR-CUT budgets (cumulative cells),
  greedy by score: unflagged before flagged (the five D-categories from
  the C-audit), core before gold, cluster-spread caps (A:2, B:5/cluster).
- Gold spans overlapping a core clip (>50%) deduped — same passage,
  core window kept (the flow-fixed one).
- Cell order in the file = membership order (core flow, then gold
  cluster-journey); final EDIT order = the cue-sheet stage (three clocks).

## Budget vs actual (spoken source audio, seconds: 0 / A / B / C)

| ch | question (locked chain) | actual | budget | clips 0/A/B/C |
|---|---|---|---|---|
| 1 | What is Nibbana? | 14 / 191 / 599 / 1499 | 30 / 240 / 600 / 1500 | 1/3/9/37 |
| 2 | Why don't I see Nibbana right now? | 9 / 395 / 1080 / 1979 | 90 / 420 / 1080 / 1980 | 1/2/11/22 |
| 3 | What keeps it going? | 4 / 387 / 1199 / 2039 | 75 / 420 / 1200 / 2040 | 1/6/19/32 |
| 4 | How is the sense of self constructed? | 24 / 226 / 478 / 779 | 45 / 240 / 480 / 780 | 1/4/11/28 |
| 5 | How is Nibbana attained? | 22 / 408 / 1138 / 2099 | 45 / 420 / 1140 / 2100 | 1/7/22/44 |
| 6 | What is Nibbana like? | 7 / 385 / 900 / 1677 | 75 / 420 / 900 / 1680 | 1/9/17/31 |
| **total** | | **1.3 / 33.2 / 89.9 / 167.9 min** | **6 / 36 / 90 / 168** | 6/31/89/194 |

**Screening: 292.3 min ≈ 4h 52m** (ceiling 300 + 5m tolerance).
Unique timeline material (C) = 167.9m; re-encountered = 124.4m (the
nesting repetition the doc budgeted at 132m).

Screening map (actual): 0:00–0:01 seed · 0:01–0:35 A · 0:35–2:04 B ·
2:04–4:52 C.

## Documented deviations (G8 warns, does not fail)
- Rung-0 cells all UNDER target now (pointer-shrink §51 closed the old
  ch1/4/5/6 over-target WARNs): 14<30, 9<90, 4<75, 24<45, 22<45, 7<75.
- A under budget by 2.8m (chapter packing ran out of short clips —
  thin stays thin; no padding).
- Flagged material (D-categories) in cells: A=4, B=13, C=18 of 194 —
  the film is essentially D-clean.

## Gates (G8)
1. nesting E0 ⊂ EA ⊂ EB ⊂ EC (by (lec,start), per chapter)
2. A/B/C cumulative cells ≤ budget (+2s slack) — hard fail
3. every clip carries provenance {lec,start,end,dur,src,ci,grade,flags,depth}
4. every clip inside the kept pool (overlap ≥50%)
5. chapter questions == locked chain == make_assembly source
6. screening ≤ 305m

## Next (in order)
1. cue sheet: intra-cell ORDER + shot IDs + music passages (three clocks)
2. audio render per rung (CF exact; YT-anchor mapping for L03/06/14/24/27…)
3. human intros shortened for the ~2m seed (owner lines)
4. C rung retired from the listening path (§62) — film keeps its C-cells
   as-is; no separate listening-edition C→D manifest planned.

## Lab patch applied with this cut (F1 back-port)
The two A-grade head-extensions (S1 L19 head → 348.0, S6 L27 head →
661.84) are now written into pool AND gold — the containment audit's
two A-grade exceptions are closed (gold ⊇ core exact except the two
documented B* promotions; gold ⊆ pool still 6/6). TIMINGS.md pool/gold
sums shift by ~21s total (rounding-level; file left as published).
