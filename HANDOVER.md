# HANDOVER — start here (2026-10-26, rebuilt after the p0 session)

You are the next agent on **analayo-nibbana**: the 33 Analayo lectures on
Ñāṇananda's *Nibbāna: The Mind Stilled*, compressed into an argument
(six sections, four rungs) and a five-hour film. Everything below is
where things are, why, and what's next. Nothing here is decoration.

## Read in this order (seriously — this prevents the failure modes)
1. `VISION.md` — the owner's intent, collated. When lost, this answers
   "what did the owner actually want?"
2. `process/RECURRING-MISTAKES.md` — my failure patterns R1–R9. R1
   (writing composed prose — even in chat) is the fatal one; R9
   (proxies vs content) is the expensive one.
3. `process/AXIOMS.md` + `process/12-ARGUMENT.md` — binding rules,
   the six-slot chain, the question formula, the ritual.
4. `CONDENSED-BUILD-NOTES.md` — §35 onward = the p0 session (render
   pipeline, sharpening, machine ears). The log is the truth; memory
   is not.
5. `DONE.md` — definition of done + adjudication taxonomy (read before
   claiming anything finished).
6. `visuals/` docs (see index below) — the film's design canon.
7. `process/MISTAKES.md`, `REVIEW.md` — history of what was wrong.

## Branch topology
- **`main`** → the audio build: chain locked, seed, essays, gates
  green, visuals canon saved. Last pushed: `393ab8f`.
- **`lab/c-split`** ← YOU ARE HERE (usually): p0 essay-A (direct
  essay-0, Fish questions, room bridges, dual-pass linear), sharpened
  A+B, storyboard, machine ears, DONE rule. Last pushed: `ef30f91`
  (renders local-only, never committed).
- **tag `baseline-before-lab`** = pre-experiment main. Diff any lab
  change against it: `git diff baseline-before-lab..lab/c-split`.
- Push ONLY when the owner says push. Commit freely on your branch.

## Where everything is and why

### Root (read-mostly)
| file | what it is |
|---|---|
| `VISION.md` | owner's intent, collated — the north star |
| `HANDOVER.md` | this file — next agent's entry point |
| `TIMINGS.md` | computed runtimes (seed 7m / A 1h57 / B ~6.6h / C ~21.3h) |
| `FILM-CUT.md` | the five-hour film cut: budget-vs-actual tables (lab branch) |
| `CONDENSED-BUILD-NOTES.md` | THE log — every build change, §1–§49 |
| `REVIEW.md` | the first-listener read-through (2026-10-24) |
| `DONE.md` | definition of done + adjudication taxonomy |
| `SPEAKER-RULES.md` | voice rules for the three speakers |
| `CUTTING-FORMULA.md` + `lecture-NN.cutplan.{json,md}` | era-1 cutplans (33/33 done; method history) |
| `HANDOFF.md` | SUPERSEDED cutplan-era handoff (kept for method) |

### `build/` — THE product data (canonical; read by gates and builders)
- **Sources (edit only via logged fixes):** `segN_pool/gold/core_v4/script.json`
  (pool 1196 / gold 608 incl. 6 essay-0 anchors + 2 A-strays (§58) + 9 B* gems (§59) / core 71 sharpened),
  `segN_terms.json`, keys `fish_filter.py` + `blunt_key.json`,
  `quote_pool.json`, `verbatim_audio_v1.json` (71/71 aligned),
  `gold_fix_log.json`, `ear_floors.json`.
- **Derived (never hand-edit — regenerate):** `assembly_sN.json`
  (make_assembly: scaled waters, settle closes, post-essay-0 stillness),
  `assembly_s0_seed.json` (build_seed), `film_manifest.json`
  (build_film_manifest), `manifest_*.txt`, `STORYBOARD.md`
  (build_storyboard.py), `EAR_REPORT.md` + `EAR_LEDGER.md` (rounds).
- `human-scripts.md` — section questions + **empty owner slots** (my
  prose was stripped; never write content there).
- `assets/` — motto-bell (2.5s) + zoom-bell (6s) wavs; `assets/sfx/`
  (bowls/ding/long-break/blocks kit, p1 wiring).
- `audio_p0/` — LOCAL ONLY p0 render (never committed): seed + S1..S6 +
  full + manifest.json (per-slice timeline) + .lst files.

### `process/` — the machinery
- Stage docs `00..11` + `12-ARGUMENT` (spine/ritual) + `13-SHARPENING`
  (rung method) + `14-LISTENING` (machine ears) — read 12 first.
- **Builders:** `scripts/make_assembly.py`, `scripts/build_seed.py`,
  `scripts/build_film_manifest.py`, `scripts/sharpen_gold.py` (log:
  gold_fix_log), `scripts/p0_mix_check.py` (mix proof),
  `scripts/ear_regression.py` (calibration), `scripts/ear_probes.py`
  (checkable-question protocol), `scripts/rebuild_text.py`
  (gloss+tts functions; its `main` td path is stale — use functions,
  write to build/), `scripts/rematch2.py` (pool builder, legacy).
- **Render:** `tools/render_a_essay.py` (voice-match, room bridges,
  dual-pass linear, Fish free-tier, draft flags; timeline manifests),
  `tools/align_verbatim_audio.py`, `tools/build_storyboard.py`.
- **Gates (verify.sh):** G1 totals → G5 quote-anchor → G6 TTS →
  G6b hardened+canary → G7 essay/chain → G8 film manifest → files.
  NEVER relax a gate; fix the data or the key (axiom 12).
- `verify.sh` = one command, ALL GATES PASS or stop.

### `visuals/` — the film's design canon (read-only history + binding specs)
| doc | one line |
|---|---|
| `VISUAL-ENGINE.md` | the unlock: visuals ANSWER each section's question (first doc) |
| `6-PATH-CANON.md` | six recurring visual paths, locked |
| `THE-MISSING-FLICK.md` | ending angle A: top slows, flick never comes |
| `THE-SOUND-MECHANISM.md` | the ting = hidden clock; bells get diegetic origin |
| `BALLERINA-BOX-LOCK.md` | ballerina music box = path-3 object; box=charm/top=mechanism |
| `THE-SONG-ENDS.md` | ending angle B: box finishes its song, no rewind |
| `ENDING-B.md` | ending B locked: still box, audience wanting, cut to black |
| `THE-FINAL-RETURN.md` | path-6 rungs: story completes in B, C = black-silence coda |
| `THREE-CLOCKS.md` | teaching/music/visual clocks + cue-sheet spec (note: its §2 mirror anchor is stale — use §4's mirror stack) |
| `FIVE-HOUR-CUT.md` | 6+36+90+168=300m budget table (drives film_manifest) |
| `VISUAL-MASTER-PLAN.md` | THE production doc: 24-part storyboard, 65–100 shot inventory, `source_clip/shot_id/...` schema, binding three-rule test |

### Sermon readings (2026-10-25) — the verbatim voice
`sermon-audio/` = all 33 "Nibbana: The Mind Stilled" READINGS (412MB,
from the mediafire folder, key uudqwtf9aflpg via api/1.4/folder/
get_content + file-page scrape). `sermon-readings/` = timestamped
transcripts (faster-whisper small.en, CF schema) via
`tools/sermon_transcribe.py` (background, /tmp/sermon_tr.log) +
SERMON-01-youtube-transcript.md (word-for-word, YT OiduBXAHtUA).
WHY IT MATTERS: the sermon text has its own narration — the verbatim
layer can be HEARD; Fish is not needed for quoting. Quote-align =
match excavation quotes against sermon-readings JSONs (next queue item).

### External dependency (NOT in repo — G5 dies without it)
`/tmp/satsang-ext/53-nibbana-scaffold/` = the 33 sermon excavations =
**the only verbatim home** (G5 anchors quotes there). The audio source
of truth: `ds-full/`, `ds-mp3/`, root lecture mp3s + `lecture-*.transcript.cf.json`
+ `yt-subs/` (YT-only: 03,06,07,14,17,20,22,24,26,27 — YT timebase).

## Locked decisions (do not re-litigate; the owner locked these)
- **Chain:** What is Nibbana? → Why don't I see Nibbana right now? →
  What keeps it going? → How is the sense of self constructed? →
  How is Nibbana attained? → What is Nibbana like?
- **Essay 0** = six repaired units (notes §32–32c, §51): motto / dog-ignorance
  ("due to ignorance... the dog imagines another dog", owner pick locking
  the U2 upgrade) / craving-gap / mirror "Ah, here I am!" / Bahiya /
  grown-cool. Every window opens and closes on the spoken answer. Q4 seam closed on
  transcript (notes §40).
- **Rungs:** 0 ⊂ A ⊂ B ⊂ C (Russian dolls), verified by overlap 6/6,
  71/71 exact (notes §39, §55, §58); film budgets 6/36/90/168.
  **D = archive** (the pool files: 1196 spans, reference only — NOT a
  listening pass; 2026-10-27 rename, notes §58). C is the curated
  deepening (film C-cells); D is the complete record.
- **p0 draft rules (2026-10-26):** NO PLAIN (verbatim → Analayo direct),
  NO BELLS (timing/voice check), essay-0 DIRECT (Q → archive answer, no
  reader repeat). Fish = questions only (Fish-audio voice, free tier).
  Bells + sfx kit return in p1.
- **Ending:** candle out → ordinary life → same angle → still box →
  hold → black + silence (30s coda test). Nothing rings after the hold.
- **Ritual:** bell → Fish Q → 3s → archive voice (nothing wedged).
- **Gospel:** TEXT VERBATIM → PLAIN (Fish, mechanical) → AUDIO. Never
  authored prose anywhere, including chat (R1).
- **Done rule (DONE.md):** text gates + mix proof + 2 clean ear rounds +
  ledger. Raw model verdicts never gate (canary).
- **Owner-only domains:** question wording, essay-0 answer swaps,
  voice approval, demote calls, intros, anything by taste. Tests inform;
  they decide.

## Numbers that are true today (recomputed, not remembered)
Pool 1196 spans 20.73h · gold 608 (essay-0 anchors §39 + 2 A-strays §58 + 9 B* §59, + S2
dog-arc reinstatement §52) ·
core **71 clips** · seed 6 units, ~2m (75s pointers) · A 33.2m · B 89.8m ·
C 167.9m · **screening 292.3m (~4h52)** · G8 warns only atomic rung-0
over-targets (documented WARNs, not fails). Containment 0⊂A⊂B⊂C exact
(6/6, 71/71 by overlap, pool⊇gold).
p0 audio (local-only, pre-U4-extension): seed + S1..S6, 71/71 real
voices, Fish Qs, room-bridge beds, dual-pass linear; p0_mix_check PASS.

## Next queue (in order)
1. **Taste locks (owner):** essay-0 picks (U2/U6 standing), Fish voice
   approval (audition sent), 16 demote calls (gold_fix_log.json),
   human intros (slots empty by design).
2. **p1:** bells back (motto/zoom) + sfx kit wiring (bowls/ding/break/
   blocks per assets/sfx/README.md) + YT anchor-maps at cut.
3. **Film-C curation** (pool-only gems → film C-cells; budgets are
   ceilings — swap, don't pad. B already absorbed the 2 A-grade strays,
   §58) + cue sheet (visual-master-plan §7 schema): per beat —
   source_clip, essay_depth, visual_motif, shot_id, audio_cue,
   duration, reuse_from. Absolute timestamps after audio master.
4. **G-ear live** (DONE 2026-10-27: `process/scripts/ear_local.py` wired
   as G9 — whisper order + essay-0 phrases + seam regression, zero
   tokens, cached). Qwen reserved for critic/tie-breaks (14-LISTENING
   free-first protocol).

## Traps (the ones that actually bit)
- **R6 inline drift:** never paste builder code in chat/shell — use
  the scripts. `build_seed` and `build_film_manifest` exist BECAUSE
  of this.
- **rebuild_text.main** targets `/tmp/opencode/condensed` (stale) —
  import its functions and write to build/ explicitly.
- Gate failures: fix data/keys, never the gate.
- Counts in old notes drift (73→71, event tallies); trust the files,
  recompute anything that matters.
- **afade=t=out:st=0 stays silent** (M-R1): fade-outs start at dur-0.03
  via fade_tail(), never st=0. Every slice asserts audible at cut.
- **Loudness proves nothing** (M-R2/R9): verify content (peaks, edges),
  never LUFS/size/decode alone. Mastering is dual-pass LINEAR.
- **Rooms never get loudnorm** (ledger #3): beds sit ~30dB under speech.
- **`-v error` hides loudnorm JSON** (ledger): measurement passes run loud.
- **Truncated uploads look successful** (M-R3): re-download + byte-check
  every link before sending. uguu.se ≈ 3h retention; R2 presigns need
  `--region auto` (SigV4).
- **Model verdicts are decoration** (canary): descriptive prompts +
  mechanical verification only; mid-thought stays whisper-edges.
- **Snaps only shrink** (M-R8): essay-0/B* windows atomic; fragment-head
  rule YT-only; motto opens exempt.
