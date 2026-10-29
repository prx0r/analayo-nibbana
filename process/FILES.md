# FILES — artifact map. Live set only (superseded versions in build/versions/).
Updated 2026-10-29. Entry point for agents: ../AGENTS.md, then ../HANDOVER.md.

## Build outputs (`build/canon/` — committed, this IS the product data)
Sources (edit only via logged, gated fixes):
- `build/canon/segN_pool.json` (N=1..6): the archive (1147 spans, ~20.8h).
  Reference only: provenance home, swap source, completeness proof. NOT
  a listening pass (no sequence law, no motto-cap, no listen order).
  The pool files keep their names (builders + G5 read them).
- `build/canon/segN_gold.json`: gold file (555 spans incl. essay-0 anchors;
  6.9h raw). Deepening source for rungs B/C/D — NOT rung B itself (53.1m).
  A-flow order, edge-audited. Motto-cap enforced in manifests, never in data.
- `build/canon/segN_core_v4.json`: core clips (83: 71 + 12 hunt §75),
  sharpened orders (§37), verified holder of every flow fix. Assemblies play
  all core beats + essay-0 pointer hosts.
- `build/canon/segN_script.json`: per beat {analayo clip, nanananda_verbatim
  (+provenance), plain_english_below, tts_line, match}.
- `build/canon/segN_terms.json`: term drops per clip.
- `build/canon/quote_pool.json`, `build/canon/fish_filter.py` (PALI2EN key),
  `build/canon/blunt_key.json`.
- `build/canon/verbatim_audio_v1.json`: every verbatim part -> sermon-reading window
  (71/71 aligned); `build/canon/yt_anchor_map.json` (YT→DS offsets);
  `build/versions/gold_fix_log.json` (frozen §38 sharpen history);
  `build/ears/ear_floors.json` (G-ear blocking floors);
  `build/ears/EAR_LEDGER.md` (fix ledger with meters);
  `build/ears/EAR_REPORT.md` (listen-back verdicts per round).
- `build/canon/essay0.json`: THE essay-0 (Q + plain + TEXT + audio windows).
- `build/canon/rhythm.json` (+ `rhythm.md`): the silence engine (slots,
  per-unit overrides, word-pause marks). `build/canon/voice_match.json`:
  post-production guide trims.
- `build/canon/FINAL_ESSAY_TEXT_0A.md`: the complete spoken text 0+A
  (generated from canon data, never typed).

Derived (never hand-edit — regenerate):
- `build/canon/assembly_sN.json` <- `process/scripts/make_assembly.py`
  (rhythm slots, scaled waters, 6s settle closes, post-essay-0 stillness)
- `build/canon/assembly_s0_seed.json` <- `process/scripts/build_seed.py`
  (47 events)
- `build/canon/newA_manifest.json` <- `process/scripts/build_newA.py`
  (rung A picks, budget 340s) · `build/canon/ladder_manifest.json` <-
  `process/scripts/build_rungs.py` (rungs B/C/D, budgets 600/1200/2700)
- `build/canon/film_manifest.json` <- `process/scripts/build_film_manifest.py`
  (four-depth membership, film budgets 6/36/90/168, screening 291.8m)
- `build/canon/manifest_*.txt` (ffmpeg lists), `build/canon/manifest_index.json`
- `build/canon/STORYBOARD.md` <- `tools/build_storyboard.py` (full-core
  shooting script: beats, clocks, flags; newA counterpart pending)

Other: `build/canon/human-scripts.md` (questions + EMPTY owner slots — never write
content there), `build/assets/` (motto-bell 2.5s, zoom-bell 6s),
`build/assets/sfx/` (bowls/ding/long-break/blocks kit, partially wired),
`build/versions/essay_a_analayo_transcript.md` (old p0 transcript — superseded,
do not build from; see `build/versions/VERSIONS.md`),
`build/versions/` (superseded canon states, dated, never live).

## Process (`process/` — you are here)
README (where-things-live index), 00..18 stage docs, 12-ARGUMENT
(spine/ritual/formula), 13-SHARPENING (rung method), 14-LISTENING
(machine ears doctrine), 15-RHYTHM (silence engine), 16-VOICE-MATCH
(post-production loudness), 17-CASTING (voice trials/locks),
18-MODIFICATIONS (the change loop), AXIOMS, RECURRING-MISTAKES (R1–R9, read first),
MISTAKES (M1–M13, M-A1–A10, M-R1–R8), SKILLS, REPRODUCE, FILES (this),
HANDOVER (root), DONE (root: definition-of-done + taxonomy), `verify.sh`
(G0/G1/G5/G6/G6b/G7/G8/G9 + files), `scripts/`:
- builders: make_assembly (reads rhythm.json), build_seed (+ rhythm),
  build_newA (rung A picks), build_rungs (rungs B/C/D), build_film_manifest,
  rebuild_text (gloss+tts functions; writes build/canon/ explicitly),
  rematch2 (pool builder, FROZEN era-1), sharpen_gold (FROZEN — rerun
  deletes §59/§61 promotions; log lives in build/versions/),
  p0_mix_check (mix proof: order/beds/edges/levels; retarget OUT for audio_B),
  voice_match (measure/apply/check), trial_trio (voice auditions),
  ear_regression (fixture calibration runner),
  ear_probes (checkable-question ear protocol), ear_local (G9: whisper order
  + essay-0 phrases with fuzzy narrow retry + advisory downgrade),
  omni_round (Qwen rounds; AUDIO_DIR + EAR_OUT env), regen_manifest_index,
  render_newA (driver: [seed|s1..|all|full]), render_B (AUDIO_OUT=build/audio_B)
- gates: g5_provenance (semantic quote-anchor, 98/98), g6_tts_check
  (hardened + canary), g7_essay_check (chain/seed), g8_film_check
  (nesting/budgets/provenance)
- render: `tools/render_a_essay.py` (vox slices keyed by vid+trim,
  room-bridge beds, dual-pass LINEAR master, Fish free-tier only,
  guide = KID Q + OLD MAN plain; writes audio_p0/audio_p1/audio_v1/
  audio_newA/ + per-section manifest timelines; `tools/validate_sheet.py`
  = G0 sheet check, run before any render), `tools/align_verbatim_audio.py`
  (coverage scoring + cross-sermon fallback + PINs), `tools/build_storyboard.py`

## Film + intent (root)
- `AGENTS.md` — read FIRST (map + laws). `HANDOVER.md` — entry state (locks, queue, traps).
- `DONE.md` — definition of done + adjudication taxonomy + fixtures.
- `FILM-CUT.md` — five-hour cut report (lab/c-split).
- `TIMINGS.md` — measured runtimes per rung (from manifests; assemblies are truth).
- `VISION.md` — owner intent; `CONDENSED-BUILD-NOTES.md` — THE log (§§1–86 frozen).
- `AUDIT-2026-10-28.md` (+ §6 addendum) — staleness audit with fix list.
- `reviews/` (frozen first-listener reviews), `SPEAKER-RULES.md` (v7: KID + OLD MAN),
  `archive/era-1-cutplans/` (CUTTING-FORMULA.md + HANDOFF.md, frozen method),
  `sources/lectures/cutplans/` (era-1 cutplans, 33/33 done).

## Visuals (`visuals/` — 11 design docs, index in HANDOVER)
The film canon: engine, 6-path canon, endings (MISSING-FLICK,
SONG-ENDS, ENDING-B, FINAL-RETURN), sound mechanism, ballerina box,
three-clocks (cue-sheet spec), FIVE-HOUR-CUT
(budgets), VISUAL-MASTER-PLAN (production: shots, schema, three-rule).

## Sources (read-only, never edited)
- `sources/sermons/excavations/` (vendored 2026-10-28, byte-identical) —
  excavations = THE verbatim home (G5 anchors here, repo-local first;
  legacy /tmp path fallback). Packs 51/52 = movie manual.
- `sources/lectures/` (audio/ 33 mp3s, transcripts/ 23 CF JSONs, yt-subs/, ds-full/, ds-mp3/, cutplans/ era-1), `tools/`.
- `sources/sermons/audio/` (33 readings, tracked) + `sources/sermons/readings/` (33
  faster-whisper JSONs, tracked) = THE verbatim voice (alignment needs
  the JSONs, slicing needs the mp3s; G5 anchors on the scaffold above).

## Quarantine (outside repo, never ships)
`/tmp/opencode/condensed/slop/` — composed-Fish scripts + hand pads.
Evidence for MISTAKES M1-M2.
