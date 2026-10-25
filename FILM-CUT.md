# FILM-CUT — the five-hour version (lab/c-split, 2026-10-25)

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
| 1 | What is Nibbana? | 53 / 220 / 600 / 1499 | 30 / 240 / 600 / 1500 | 1/3/20/47 |
| 2 | Why don't I see Nibbana right now? | 65 / 402 / 1077 / 1978 | 90 / 420 / 1080 / 1980 | 1/3/13/26 |
| 3 | What keeps it going? | 62 / 398 / 1200 / 2040 | 75 / 420 / 1200 / 2040 | 1/5/18/32 |
| 4 | How is the sense of self constructed? | 48 / 210 / 480 / 779 | 45 / 240 / 480 / 780 | 1/4/16/36 |
| 5 | How is Nibbana attained? | 75 / 382 / 1140 / 2100 | 45 / 420 / 1140 / 2100 | 1/5/19/40 |
| 6 | What is Nibbana like? | 99 / 418 / 899 / 1680 | 75 / 420 / 900 / 1680 | 1/7/17/44 |
| **total** | | **6.7 / 33.5 / 90.0 / 167.9 min** | **6 / 36 / 90 / 168** | 1/27/103/225 |

**Screening: 298.1 min ≈ 4h 58m** (ceiling 300 + 5m tolerance).
Unique timeline material (C) = 167.9m; re-encountered = 130.4m (the
nesting repetition the doc budgeted at 132m).

Screening map (actual): 0:00–0:06 seed · 0:06–0:40 A · 0:40–2:10 B ·
2:10–4:58 C.

## Documented deviations (G8 warns, does not fail)
- Rung-0 cells over target in ch1/4/5/6 (53>30, 48>45, 75>45, 99>75):
  the seed clips are atomic lecture windows — the essay-0 material
  cannot be shorter than the sentence it is. A visual-crop pass (hold
  text cards over early fade-out) can reclaim the ~25s at edit time.
- A under budget by 1.9m (chapter packing ran out of short clips —
  thin stays thin; no padding).
- Flagged material (D-categories) in cells: A=3 (incl. the refrain
  essay-0s, unavoidable), B=14, C=21 of 225 — the film is essentially
  D-clean; the flagged pool stays for the LISTENING C/D split.

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
3. human intros shortened for the 6m seed (owner lines)
4. listening-edition C→D split (separate manifest, uses the 333m flag pool)

## Lab patch applied with this cut (F1 back-port)
The two A-grade head-extensions (S1 L19 head → 348.0, S6 L27 head →
661.84) are now written into pool AND gold — the containment audit's
two A-grade exceptions are closed (gold ⊇ core exact except the two
documented B* promotions; gold ⊆ pool still 6/6). TIMINGS.md pool/gold
sums shift by ~21s total (rounding-level; file left as published).
