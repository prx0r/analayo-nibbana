# REPRODUCE — exact rerun, top to bottom.

Prerequisites: repo (scaffold vendored at `sources/sermons/excavations/`;
legacy `/tmp/satsang-ext` path still works as fallback) + transcripts
(`sources/lectures/transcripts/lecture-NN.transcript.cf.json`, `sources/lectures/yt-subs/`) +
all 33 DS mp3s (10 fetched this session from dharmaseed retreat 4373,
talk IDs 58720+N, symlinked as `sources/lectures/audio/analayo-nibbana-lecture-NN.mp3`).
`build/canon/` is the LIVE data directory — builders (rebuild_text.py,
make_assembly.py, build_seed.py, build_newA.py, build_rungs.py) read AND write
it directly; /tmp is scratch only (axiom 13).

## Stage order (deterministic unless marked ✎ human)
1. Cutplans exist already (`sources/lectures/cutplans/lecture-NN.cutplan.json`;
   era-1, FROZEN — `tools/auto_keeps.py` + `tools/gen_plan.py` kept for method only).
2. Assign spans → `build/canon/segN_pool.json` (keyword scorer + primary fallback;
   reference: FROZEN `process/scripts/rematch2.py` pool logic + cluster lists
   in `02-SEGMENT.md`). Assert totals == kept total.
3. Gold = filter grade A, cluster order. Apply motto-cap at manifest
   time (keep data intact).
4. Cores: top-2-per-cluster by duration, motto first, slivers <10s
   dropped — then apply the hand-fix list (CONDENSED-BUILD-NOTES §10-13:
   drops, swaps, trims, S4 rebuild, S6 reorder, motto head extensions).
   Hand fixes are DATA (recorded), not vibes; manifests pin v4.
   (`sharpen_gold.py` is FROZEN — rerun deletes §59/§61 promotions.)
5. Pads: match excavation quotes per clip (keyword overlap +
   same-sermon +3, uniqueness per section, targeted overrides listed
   in notes §22). Record {sermon} per beat; provenance is re-derived
   (never stored offsets — recompute + assert each run).
6. Below-lines: `fish_filter.PALI2EN` then `blunt_key.json`, then
   TTS transform (parentheses→dashes, English-first lead-drop,
   artifact cleanup). Deterministic — hash must match notes.
6a. Rhythm: `build/canon/rhythm.json` slots + overrides feed every pause
   (`make_assembly.py` + `build_seed.py` read via R(s, slot)) — see 15-RHYTHM.
6b. Seed: `python3 process/scripts/build_seed.py` (reads assemblies; 47 events).
6c. Rungs: `python3 process/scripts/build_newA.py` (rung A, budget 340s) +
   `python3 process/scripts/build_rungs.py` (rungs B/C/D, budgets 600/1200/2700).
6d. Film manifest: `python3 process/scripts/build_film_manifest.py`
   (four-depth membership, budgets, flags cache build/.film_flags_cache.json).
   Data patches that must be present (logged notes §32-32c): head-
   back-ports (S1 L19->348, S6 L27->661.84), pool-move L33 2->3,
   pool-adds L10->4 and L01->6, six essay-0 stacks (S2 triple).
6e. Storyboard: `python3 tools/build_storyboard.py` (build/canon/STORYBOARD.md).
6f. Align verbatim: `python3 tools/align_verbatim_audio.py`
   (build/canon/verbatim_audio_v1.json; 71/71 aligned).
6g. Sheet check: `python3 tools/validate_sheet.py` (G0 — seconds, no audio).
6h. Render: `python3 process/scripts/render_newA.py [seed|s1..|all|full]`
   (needs FISH_API_KEY env or characters/audition/.env; free model pinned;
   guide = KID Q + OLD MAN plain; writes build/audio_newA/ +
   manifest.json with per-slice timeline). Renders are local-only,
   never committed. B: `python3 process/scripts/render_B.py [seed|all]`
   (AUDIO_OUT=build/audio_B).
6i. Mix proof: mix-check script (must PASS: order/beds/edges/levels).
6j. Voice match: `python3 process/scripts/voice_match.py check [dir]`
   (guide vs archive gap ≤ 1.0 LU); if over: measure → apply → re-check.
6k. Ear protocol: G9 `ear_local.py --full` (fuzzy key_heard + narrow retry;
   whisper misses are advisory, transcript wins), fixtures
   (`ear_regression.py`, calibration only), probes (`ear_probes.py`,
   must PASS), omni descriptive rounds (`omni_round.py` + AUDIO_DIR/EAR_OUT)
   per 14-LISTENING (scoped re-listens). Ledger: build/ears/EAR_LEDGER.md.
7. Run `process/verify.sh` — G0 sheet, G1 totals, G5 semantic quote-anchor
   (98/98), G6 punctuation/Pali, G6b hardened (leading-run + term-attachment +
   embedded canary), G7 essay/chain/seed, G8 film manifest (nesting,
   budgets, provenance, chain, pool-membership), G9 local ears, file presence.
   ALL PASS or stop. If a gate
   fails, fix the DATA or the KEY — never relax the gate (axiom 12).
7b. FINAL LOOKOVER (done once per major pass; see reviews/REVIEW.md): read
   every beat as a first-time listener → findings-only REVIEW →
   amendment pass with sourced quotes, logged in
   CONDENSED-BUILD-NOTES §25/§26. Amendments are recorded as
   `amendment` fields on the affected script entries — reruns inherit
   them because build/ is source of truth.
8. Render (audio present): per-manifest `ffmpeg -ss/-to` cuts,
   concat with breath/water beds + bells, `loudnorm`, `afade 0.15s`.
9. QA listen (ears, unskippable): fixed cores + flags f1–f4.
   NOTE: quotes for amendment swaps were all sourced from the 33
   sermon-excavations (A-pass, notes §26) — never invent a quote;
   the G5 anchor gate rejects anything not literally quoted.

## What is NOT reproducible (human by design, marked ✎)
Targeted pad overrides, flow-audit verdicts, hand-fix list, human
intros/bridges, bell choices, listen-pass signoff. Everything else is
scripted or it doesn't belong in the pipeline.
