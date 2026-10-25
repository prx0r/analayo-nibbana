# TIMINGS — computed from the timestamped build (2026-10-25)

Source of truth: build/segN_{pool,gold,core_v4}.json span windows,
build/assembly_sN.json event timelines, build/assembly_s0_seed.json.
Speech estimates at ~156 wpm for Fish lines (windows ARE the archive
voice, counted exactly). Bells: motto 2.5s / zoom 6s (09-BELLS-ZOOM).
NOT counted: human intros (your lines, TBD), visual-layer holds/song
fragments (film additions sit on top of these audio times).

## Rung 0 — THE SEED (six micro-sessions chained)

- unit 1 — Q: What is Nibbana? — L01 [696–749s] — 0.9 min
- unit 2 — Q: Why don't I see Nibbana right now? — L03 [363–411s] — 0.8 min
- unit 3 — Q: What keeps it going? — L24 [1038–1100s] — 1.0 min
- unit 4 — Q: How is the sense of self constructed? — L06 [1346–1393s] — 0.8 min
- unit 5 — Q: How is Nibbana attained? — L14 [4478–4553s] — 1.2 min
- unit 6 — Q: What is Nibbana like? — L27 [661–760s] — 1.6 min

**Seed total: 7m 02s** (incl. questions, 3s recollects, water, bells)

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
| 1 | 190 | 112.1 min | ~471.1 min |
| 2 | 62 | 55.0 min | ~172.1 min |
| 3 | 91 | 63.7 min | ~235.6 min |
| 4 | 54 | 22.1 min | ~124.1 min |
| 5 | 115 | 84.7 min | ~302.0 min |
| 6 | 78 | 41.5 min | ~188.9 min |
| **total** | **590** | **379.1 min** | **~6h 37m** |

Pause model: 1.5s per join (584 joins) + 2.5s water between clusters,
15s per section question + bells. Cluster order = block count 52.

## Rung C — POOL (est. assembled: raw + seam pauses)

| path | spans | raw speech | assembled est |
|---|---|---|---|
| 1 | 329 | 325.2 min | ~890.3 min |
| 2 | 220 | 252.2 min | ~630.1 min |
| 3 | 193 | 223.2 min | ~554.7 min |
| 4 | 88 | 69.9 min | ~221.1 min |
| 5 | 239 | 251.0 min | ~661.5 min |
| 6 | 124 | 120.6 min | ~333.6 min |
| **total** | **1193** | **1242.2 min** | **~21h 16m** (incl. 30s terminal coda) |

Pause model: 1.5s per join (1187 joins) + 2.5s water between clusters
(62 blocks) + questions + bells + 30s final black-silence coda.

## Four-pass totals (video run-order: 0 → A → B → C, bells at thresholds)

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
