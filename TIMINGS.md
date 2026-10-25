# TIMINGS — computed from the timestamped build (2026-10-25)

Source of truth: build/segN_{pool,gold,core_v4}.json span windows,
build/assembly_sN.json event timelines, build/assembly_s0_seed.json.
Fish lines estimated at ~156 wpm; archive-voice windows counted exactly.
Bells: motto 2.5s / zoom 6s (process/09-BELLS-ZOOM.md).
NOT counted: human intros (owner lines, TBD) + visual-layer holds/song
fragments (film additions sit on top of these audio times).

## Rung 0 — THE SEED (six micro-sessions chained)

- unit 1 — What is Nibbana? — 0.9 min clip
- unit 2 — Why don't I see Nibbana right now? — 0.8 min clip
- unit 3 — What keeps it going? — 1.0 min clip
- unit 4 — How is the sense of self constructed? — 0.8 min clip
- unit 5 — How is Nibbana attained? — 1.2 min clip
- unit 6 — What is Nibbana like? — 1.6 min clip

**Seed total: 7m 02s** (questions + 3s recollects + water + bells)

## Rung A — CORE (assembled: questions, pauses, bells included)

| path | clips | raw speech | assembled |
|---|---|---|---|
| 1 | 11 | 8.9 min | **12.4 min** |
| 2 | 13 | 25.5 min | **30.8 min** |
| 3 | 15 | 24.7 min | **29.4 min** |
| 4 | 5 | 4.8 min | **6.1 min** |
| 5 | 14 | 17.0 min | **21.5 min** |
| 6 | 13 | 12.5 min | **16.6 min** |
| **total** | **71** | **93.4 min** | **1h 56m** |

## Rung B — GOLD (est. assembled: raw + seam pauses)

| path | spans | raw speech | assembled est |
|---|---|---|---|
| 1 | 190 | 112.1 min | **~118.1 min** |
| 2 | 62 | 55.0 min | **~56.9 min** |
| 3 | 91 | 63.7 min | **~66.5 min** |
| 4 | 54 | 22.1 min | **~23.8 min** |
| 5 | 115 | 84.7 min | **~88.3 min** |
| 6 | 78 | 41.5 min | **~44.0 min** |
| **total** | **590** | **379.1 min** | **~6h 37m** |

Pause model: 1.5s per join (584 joins) + 2.5s water per cluster boundary
(46) + 15s per section question + bells; pauses distributed by join share.

## Rung C — POOL (est. assembled: raw + seam pauses)

| path | spans | raw speech | assembled est |
|---|---|---|---|
| 1 | 329 | 325.2 min | **~334.6 min** |
| 2 | 220 | 252.2 min | **~258.5 min** |
| 3 | 193 | 223.2 min | **~228.7 min** |
| 4 | 88 | 69.9 min | **~72.4 min** |
| 5 | 239 | 251.0 min | **~257.9 min** |
| 6 | 124 | 120.6 min | **~124.1 min** |
| **total** | **1193** | **1242.2 min** | **~21h 16m** (incl. 30s terminal coda) |

Pause model: 1.5s per join (1187 joins) + 2.5s water per cluster boundary
(56) + questions + bells + 30s final black-silence coda.

## Four-pass totals (video run-order: 0 -> A -> B -> C, bells at thresholds)

| pass | duration |
|---|---|
| 0 seed | 7m 02s |
| A core | 1h 56m |
| B gold | ~6h 37m |
| C pool | ~21h 16m |
| **all four** | **~29h 58m** |

Film decision pending: the FILM is presumably the A-run (~1.9 h) with
path visuals + holds + song fragments layered on top; B and C are the
listening editions. Path 4 is intentionally thin (6.1 min A) — honest,
not padded. Ending: 30s terminal silence (test duration, 09-BELLS).
