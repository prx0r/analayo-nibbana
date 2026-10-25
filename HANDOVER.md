# HANDOVER — start here (2026-10-25, written by the build agent)

You are the next agent on **analayo-nibbana**: the 33 Analayo lectures on
Ñāṇananda's *Nibbāna: The Mind Stilled*, compressed into an argument
(six sections, four rungs) and a five-hour film. Everything below is
where things are, why, and what's next. Nothing here is decoration.

## Read in this order (seriously — this prevents the failure modes)
1. `VISION.md` — the owner's intent, collated. When lost, this answers
   "what did the owner actually want?"
2. `process/RECURRING-MISTAKES.md` — my failure patterns R1–R8. R1
   (writing composed prose — even in chat) is the fatal one.
3. `process/AXIOMS.md` + `process/12-ARGUMENT.md` — binding rules,
   the six-slot chain, the question formula, the ritual.
4. `CONDENSED-BUILD-NOTES.md` — §25 onward = every change this
   session (essay-0 repairs, pool corrections, film cut). The log is
   the truth; memory is not.
5. `visuals/` docs (see index below) — the film's design canon.
6. `process/MISTAKES.md`, `REVIEW.md` — history of what was wrong.

## Branch topology
- **`main`** → the audio build: chain locked, seed, essays, gates
  green, visuals canon saved. Last pushed: `393ab8f`.
- **`lab/c-split`** ← YOU ARE HERE (usually): the film experiment.
  Film manifest, G8, F1 containment fix, six essay-0 repairs,
  A-composition review. Last pushed: `f2dfc6a`.
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
| `CONDENSED-BUILD-NOTES.md` | THE log — every build change, §1–§33 |
| `REVIEW.md` | the first-listener read-through (2026-10-24) |
| `SPEAKER-RULES.md` | voice rules for the three speakers |
| `CUTTING-FORMULA.md` + `lecture-NN.cutplan.{json,md}` | era-1 cutplans (33/33 done; method history) |
| `HANDOFF.md` | SUPERSEDED cutplan-era handoff (kept for method) |

### `build/` — THE product data (canonical; read by gates and builders)
- **Sources (edit only via logged fixes):** `segN_pool/gold/core_v4/script.json`,
  `segN_terms.json`, keys `fish_filter.py` + `blunt_key.json`,
  `quote_pool.json`.
- **Derived (never hand-edit — regenerate):** `assembly_sN.json`
  (make_assembly), `assembly_s0_seed.json` (build_seed),
  `film_manifest.json` (build_film_manifest), `manifest_*.txt`.
- `human-scripts.md` — section questions + **empty owner slots** (my
  prose was stripped; never write content there).
- `assets/` — motto-bell (2.5s) + zoom-bell (6s) wavs.

### `process/` — the machinery
- Stage docs `00..11` + `12-ARGUMENT` (spine/ritual) — read 12 first.
- **Builders:** `scripts/make_assembly.py`, `scripts/build_seed.py`,
  `scripts/build_film_manifest.py`, `scripts/rebuild_text.py`
  (gloss+tts functions; its `main` td path is stale — use functions,
  write to build/), `scripts/rematch2.py` (pool builder, legacy).
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

### External dependency (NOT in repo — G5 dies without it)
`/tmp/satsang-ext/53-nibbana-scaffold/` = the 33 sermon excavations =
**the only verbatim home** (G5 anchors quotes there). The audio source
of truth: `ds-full/`, `ds-mp3/`, root lecture mp3s + `lecture-*.transcript.cf.json`
+ `yt-subs/` (YT-only: 03,06,07,14,17,20,22,24,26,27 — YT timebase).

## Locked decisions (do not re-litigate; the owner locked these)
- **Chain:** What is Nibbana? → Why don't I see Nibbana right now? →
  What keeps it going? → How is the sense of self constructed? →
  How is Nibbana attained? → What is Nibbana like?
- **Essay 0** = six repaired units (notes §32–32c): motto / whirlpool /
  craving-gap / mirror "Ah, here I am!" / Bahiya / grown-cool. Every
  window opens and closes on the spoken answer.
- **Rungs:** 0 ⊂ A ⊂ B ⊂ C (Russian dolls), film budgets 6/36/90/168.
- **Ending:** candle out → ordinary life → same angle → still box →
  hold → black + silence (30s coda test). Nothing rings after the hold.
- **Ritual:** bell → Fish Q → 3s → archive voice (nothing wedged).
- **Gospel:** TEXT VERBATIM → PLAIN (Fish, mechanical) → AUDIO. Never
  authored prose anywhere, including chat (R1).
- **Owner-only domains:** question wording, essay-0 answer swaps,
  intros, anything by ear. Tests inform; they decide.

## Numbers that are true today (recomputed, not remembered)
Pool 1193 spans 20.70h · gold 590 = 6.3h · core **71 clips** (notes
once said 72 — wrong, §11 was right) · seed spoken 4.0m · A 33.1m ·
B 89.9m · C 167.9m · **screening 294.9m (~4h55)** · G8 warns only the
atomic refrain (ch1 53s>30s). Containment: gold⊇core exact for A-grade
(two B* promotions remain, documented), gold⊇pool 6/6.

## Next queue (in order)
1. **Cue sheet** (visual-master-plan §7 schema): per beat —
   source_clip, essay_depth, visual_motif, shot_id, audio_cue,
   duration, reuse_from. Absolute timestamps after audio master.
2. **Fish speaks the plain** (design locked in chat): Fish reads the
   mechanical plain line AFTER each Analayo clip (never between Q and
   A), ONLY when plain ≠ verbatim; new `plain_tts` field + G6 scan.
   Build on seed first.
3. **Audio renders** per rung (CF exact; YT-anchor map for YT-only).
4. **Human intros** — owner writes (slots are empty by design).
5. **Ears listen pass** — nothing has been heard end-to-end yet.
6. **Listening C→D split** (notes §31 F1): ~333m flagged pool
   (refrain/commentary/citation/etym/Pali) → study edition; audition
   commentary class first.
7. Optional: B/C signal pass (same treatment as the A-review with
   FORCE picks), gold/pool openings question-sync for listening cuts.

## Traps (the ones that actually bit)
- **R6 inline drift:** never paste builder code in chat/shell — use
  the scripts. `build_seed` and `build_film_manifest` exist BECAUSE
  of this.
- **rebuild_text.main** targets `/tmp/opencode/condensed` (stale) —
  import its functions and write to build/ explicitly.
- Gate failures: fix data/keys, never the gate.
- Counts in old notes drift (73→71, event tallies); trust the files,
  recompute anything that matters.
