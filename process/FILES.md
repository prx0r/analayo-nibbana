# FILES — artifact map. Live set only (superseded versions deleted).

## Build outputs (`build/` — committed, this IS the product data)
- `segN_pool.json` (N=1..6): every kept span assigned+ordered (1193 total,
  20.7h). Fields: lec,start,end,grade,dur,ci.
- `segN_gold.json`: A-only, cluster order (590 spans, 6.3h).
- `segN_core_v4.json`: killer beats (73 clips, 96m Analayo).
- `segN_script.json`: per beat {analayo clip, nanananda_verbatim
  (+provenance), plain_english_below, tts_line}.
- `segN_terms.json`: Fish term-drops per clip (23 total).
- `segN_pads*.json`: Nanananda pad texts per beat/cluster.
- `manifest_sN_{pool,gold,core}.txt` + `manifest_sN_core_v4.txt`:
  ffmpeg-ready clip lists. `manifest_index.json`: runtimes+coverage.
- `fish_filter.py` (PALI2EN key), `blunt_key.json` (plain-meaning map).
- `s1_core_partial.mp3` (NOT in repo — 10.2m dry-run proof, /tmp only).

## Process (`process/` — you are here)
README, 00..06 stage docs, AXIOMS, SKILLS, MISTAKES, REPRODUCE,
FILES (this), `verify.sh`, `scripts/` (fish_filter, blunt_key,
rematch2 pool-builder).

## Sources (read-only, never edited)
- `/tmp/satsang-ext/53-nibbana-scaffold/` (excavations = verbatim home),
  `/51-nibbana-movie/` (12-level manual, PLAIN-ENGLISH law, MOTIFS),
  `/52-nibbana-arguments/`.
- `lecture-*.transcript.cf.json`, `yt-subs/`, `*.mp3`, `tools/`,
  `lecture-*.cutplan.json`, HANDOFF.md, CONDENSED-BUILD-NOTES.md,
  SPEAKER-RULES.md (repo root).

## Quarantine (`/tmp/opencode/condensed/slop/` — NOT in repo, never ships)
seg1-7_fish.json (composed Fish narration), seg1_pads.json (hand beats).
Kept as evidence. See MISTAKES.md M1–M2.
