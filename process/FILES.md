# FILES — artifact map. Live set only (superseded versions deleted).
Updated 2026-10-26. Entry point for agents: ../HANDOVER.md.

## Build outputs (`build/` — committed, this IS the product data)
Sources (edit only via logged, gated fixes):
- `segN_pool.json` (N=1..6): every kept span assigned+ordered (1195 total,
  20.73h). Fields: lec,start,end,grade,dur,ci.
- `segN_gold.json`: A-flow order (596 spans incl. 6 essay-0 anchors, 6.3h).
- `segN_core_v4.json`: killer beats (**71 clips**), sharpened orders
  (S2/S3/S5/S6 moves, §37), 93.4m raw speech.
- `segN_script.json`: per beat {analayo clip, nanananda_verbatim
  (+provenance), plain_english_below, tts_line, match}.
- `segN_terms.json`: Fish term-drops per clip.
- `quote_pool.json`, `fish_filter.py` (PALI2EN key), `blunt_key.json`.
- `verbatim_audio_v1.json`: every verbatim part -> sermon-reading window
  (71/71 aligned, 1 manual PIN); `gold_fix_log.json` (B-sharpening log);
  `ear_floors.json` (G-ear blocking floors); `EAR_LEDGER.md` (fix ledger
  with meters); `EAR_REPORT.md` (listen-back verdicts per round).

Derived (never hand-edit — regenerate):
- `assembly_sN.json` <- `process/scripts/make_assembly.py` (scaled waters,
  6s settle closes, post-essay-0 stillness)
- `assembly_s0_seed.json` <- `process/scripts/build_seed.py`
- `film_manifest.json` <- `process/scripts/build_film_manifest.py`
  (four-depth membership, budgets 6/36/90/168, screening 294.9m)
- `manifest_*.txt` (ffmpeg lists), `manifest_index.json`
- `STORYBOARD.md` <- `tools/build_storyboard.py` (71 rows, clocks, flags)

Other: `human-scripts.md` (questions + EMPTY owner slots — never write
content there), `assets/` (motto-bell 2.5s, zoom-bell 6s),
`assets/sfx/` (bowls/ding/long-break/blocks kit, not yet wired),
`STORYBOARD.md` (A as shooting script, via tools/build_storyboard.py),
`essay_a_analayo_transcript.md` (every core clip's spoken words),
`EAR_REPORT.md` (machine listen-back verdicts per round).

## Process (`process/` — you are here)
README (where-things-live index), 00..11 stage docs, 12-ARGUMENT
(spine/ritual/formula), 13-SHARPENING (rung method), 14-LISTENING
(machine ears doctrine), AXIOMS, RECURRING-MISTAKES (R1–R9, read first),
MISTAKES (M1–M13, M-A1–A10, M-R1–R8), SKILLS, REPRODUCE, FILES (this),
REVIEW (root), DONE (root: definition-of-done + taxonomy), `verify.sh`
(G1/G5/G6/G6b/G7/G8), `scripts/`:
- builders: make_assembly, build_seed, build_film_manifest,
  rebuild_text (gloss+tts functions; its main() td path is stale —
  import functions, write build/ explicitly), rematch2 (pool, legacy),
  sharpen_gold (B sequence law + edge re-snap + motto-cap manifests;
  log: build/gold_fix_log.json), p0_mix_check (per-render mix proof:
  order/beds/edges/levels), ear_regression (fixture calibration runner),
  ear_probes (checkable-question ear protocol)
- gates: g5_provenance (semantic quote-anchor), g6_tts (hardened +
  canary), g7_essay (chain/seed), g8_film (nesting/budgets/provenance)
- render: `tools/render_a_essay.py` (voice-matched slices, room-bridge
  beds, dual-pass linear master, Fish questions free-tier only, draft
  flags NO_PLAIN/P0_NO_BELLS/DIRECT_ESSAY0; writes audio_p0/ + manifest
  with per-slice timeline), `tools/align_verbatim_audio.py` (coverage
  scoring + cross-sermon fallback + PINs), `tools/build_storyboard.py`

## Film + intent (root)
- `HANDOVER.md` — NEXT AGENT START HERE (state, locks, queue, traps).
- `DONE.md` — definition of done + adjudication taxonomy + fixtures.
- `FILM-CUT.md` — five-hour cut report (lab/c-split).
- `TIMINGS.md` — computed runtimes per rung (NOTE 2026-10-26: tables
  predate scaled waters + settle + post-essay-0 stillness; assemblies
  are truth until p1 recompute).
- `VISION.md` — owner intent; `CONDENSED-BUILD-NOTES.md` — THE log.
- `REVIEW.md`, `SPEAKER-RULES.md`, `CUTTING-FORMULA.md`,
  `lecture-NN.cutplan.*` (era-1, 33/33 done), `HANDOFF.md` (superseded).

## Visuals (`visuals/` — 11 design docs, index in HANDOVER)
The film canon: engine, 6-path canon, endings (MISSING-FLICK,
SONG-ENDS, ENDING-B, FINAL-RETURN), sound mechanism, ballerina box,
three-clocks (cue-sheet spec; its mirror anchor is stale), FIVE-HOUR-CUT
(budgets), VISUAL-MASTER-PLAN (production: shots, schema, three-rule).

## Sources (read-only, never edited)
- `/tmp/satsang-ext/53-nibbana-scaffold/` — excavations = THE verbatim
  home (G5 anchors here; missing = G5 fails). Packs 51/52 = movie manual.
- `lecture-*.transcript.cf.json`, `yt-subs/`, 33 mp3s, `tools/`.
- `sermon-audio/` (33 readings, tracked) + `sermon-readings/` (33
  faster-whisper JSONs, tracked) = THE verbatim voice (G5 dies without
  the JSONs for alignment; mp3s for slicing).

## Quarantine (outside repo, never ships)
`/tmp/opencode/condensed/slop/` — composed-Fish scripts + hand pads.
Evidence for MISTAKES M1-M2.
