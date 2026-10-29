# build/canon/ — THE product data (single source; gates read this)

Everything a builder reads and every gate checks lives here. Builders write
here (axiom 13). Regenerate via `process/REPRODUCE.md`, never hand-edit —
`process/verify.sh` proves it after any change.

## Rung 0 — the seed (essay-0)

| file | what |
|---|---|
| `essay0.json` | **THE essay-0**: Q + plain + TEXT + audio windows per unit (U2 = triple L25). `make_assembly.py` reads it with a drift assert; G5/G7 read it directly |
| `assembly_s0_seed.json` | 41 events: six micro-sessions chained (bell → Fish Q → 3s → plain → Analayo pointer) |

## Rungs A/B/C/D + film (assemblies → pick-lists)

| file | what |
|---|---|
| `assembly_s1.json` … `assembly_s6.json` | full-core assemblies (83 clips + essay-0 hosts): verbatim on screen → Analayo clip, pause/breath/water events |
| `newA_manifest.json` | rung A picks (budget 340s/section; S1 = pointer + beats [3,6,11]) |
| `ladder_manifest.json` | rungs B/C/D picks (budgets B600/C1200/D2700 per section) |
| `film_manifest.json` | five-hour film cells (C-cells 167.9m; screening 291.8m) |
| `manifest_index.json` | clip census per section (regen via `regen_manifest_index.py`) |

## Corpus (what the rungs pick from)

| file | what |
|---|---|
| `segN_script.json` | 83 core beats: Analayo window + verbatim + tts_line (N=1..6) |
| `segN_core_v4.json` | core clips (A-flow order; LIVE — assemblies + B/C/D read these) |
| `segN_gold.json` | gold spans 555 (~6.9h; B/C/D deepen from here) |
| `segN_pool.json` | pool spans 1147 (~20.8h; archive reference, NOT a pass) |
| `segN_terms.json` | per-clip Pali terms for the Fish key |
| `segN_pads_full.json` | Ñāṇananda pad bodies (N=2..6; S1 pads live in scripts) |
| `quote_pool.json` | candidate verbatim pool |
| `verbatim_audio_v1.json` | 71/71 quote→sermon-audio alignment (G5 cross-check) |
| `yt_anchor_map.json` | YT→DS timebase offsets per lecture (incl. L20 per-window) |

## Keys + speech + docs

| file | what |
|---|---|
| `fish_filter.py` + `blunt_key.json` | THE translation key (Pali→plain; deterministic, hash-checked). `process/scripts/blunt_key.json` was a stale duplicate — canonical is here |
| `human-scripts.md` | section questions (locked chain) + EMPTY owner intro slots (never author content here) |
| `STORYBOARD.md` | full-core shooting script (assemblies order; newA counterpart pending) |
| `manifest_sN_{core_v4,gold,pool}.txt` | cut lists (derived — regenerate, don't hand-edit) |
