# HANDOVER — start here (2026-10-29: 0+A shipped, B rendered)

You are the next agent on **analayo-nibbana**: the 33 Analayo lectures on
Ñāṇananda's *Nibbāna: The Mind Stilled*, compressed into an argument
(six sections, four rungs) and a five-hour film. Everything below is
where things are, why, and what's next. Nothing here is decoration.

## Read in this order (seriously — this prevents the failure modes)
0. `AGENTS.md` — read FIRST (map + laws; log takes precedent over all docs).
1. `VISION.md` — the owner's intent, collated. When lost, this answers
   "what did the owner actually want?"
2. `process/RECURRING-MISTAKES.md` — failure patterns R1–R9. R1
   (writing composed prose — even in chat) is the fatal one; R9
   (proxies vs content) is the expensive one.
3. `process/AXIOMS.md` + `process/12-ARGUMENT.md` — binding rules,
   the six-slot chain, the question formula, the ritual.
4. `CONDENSED-BUILD-NOTES.md` — §35 onward = the p0 session (render
   pipeline, sharpening, machine ears); §§87–96 = stamp day + voice work.
   The log is the truth; memory is not.
5. `DONE.md` — definition of done + adjudication taxonomy (read before
   claiming anything finished).
6. `visuals/` docs (see index below) — the film's design canon.
7. `process/MISTAKES.md`, `reviews/REVIEW.md` — history of what was wrong.

## Branch topology (HEAD `ac4cbc8`, pushed to `origin/lab-c-split`)
- **`main`** → the locked argument: chain, seed, essays, gates
  green, visuals canon saved.
- **`lab/c-split`** ← YOU ARE HERE (usually): newA essay-A (direct
  essay-0, kid Q + old-man plain, room bridges, dual-pass linear), sharpened
  A+B, storyboard, machine ears, DONE rule + 0+A stamp
  (renders local-only, never committed).
- **tag `baseline-before-lab`** = pre-experiment main. Diff any lab
  change against it: `git diff baseline-before-lab..lab/c-split`.
- Push ONLY when the owner says push. Commit freely on your branch.

## Where everything is and why (reorged 2026-10-28 — see AGENTS.md for read order)

### Root (read-mostly)
| file | what it is |
|---|---|
| `AGENTS.md` | ★ READ FIRST: map, read order, laws |
| `VISION.md` | owner's intent, collated — the north star |
| `HANDOVER.md` | this file — next agent's entry point |
| `TIMINGS.md` | computed runtimes (recomputed 2026-10-28) |
| `FILM-CUT.md` | the five-hour film cut: budget-vs-actual tables (lab branch) |
| `CONDENSED-BUILD-NOTES.md` | THE log — every build change, §1–§86 (precedent over all docs) |
| `AUDIT-2026-10-28.md` | staleness audit (canon proof, per-doc verdicts, fix list) |
| `reviews/` | frozen first-listener reviews (REVIEW.md, REVIEW-Q1–6, COVERAGE) |
| `archive/era-1-cutplans/` | frozen era-1 method (CUTTING-FORMULA.md, HANDOFF.md) |
| `DONE.md` | definition of done + adjudication taxonomy |
| `SPEAKER-RULES.md` | voice rules v7: KID Q + OLD MAN plain (backup elderly-ref), Analayo archive |

### `sources/` — primary materials (see `sources/README.md`)
- `lectures/`: audio/ (33 mp3s) · transcripts/ (23 CF JSONs) · yt-subs/ ·
  ds-full/ ds-mp3/ · cutplans/ (era-1, superseded) + keeps/
- `sermons/`: excavations/ (33 quote pools = verbatim home; G5 anchors here,
  repo-local first) · audio/ (33 readings) · readings/ (33 transcripts)

### `build/` — THE product data (see `build/canon/README.md`)
- **`canon/`** (gates + builders read this): `essay0.json` (THE essay-0) ·
  `assembly_s0..s6.json` · `newA_manifest.json` · `ladder_manifest.json` ·
  `film_manifest.json` · `manifest_index.json` · `segN_{core_v4,gold,pool,script,terms,pads_full}.json` (core 83, gold 555, pool 1147) ·
  keys `fish_filter.py` + `blunt_key.json` · `quote_pool.json` ·
  `verbatim_audio_v1.json` · `yt_anchor_map.json` · `human-scripts.md`
  (empty owner slots) · `STORYBOARD.md` · `manifest_sN_*.txt` (derived)
- **`versions/`** (superseded, do-not-build-from): old p0 transcript + §38 gold log (see VERSIONS.md)
- **`ears/`**: ear rounds + `EAR_LEDGER.md`/`EAR_REPORT.md` (DONE evidence) + fixtures
- `assets/` — motto-bell (2.5s) + zoom-bell (6s) wavs; `assets/sfx/` kit
- `audio_p0/` `audio_p1/` `audio_newA/` — LOCAL ONLY renders (never committed):
  newA = seed + S1..S6 + full + 30s seed→A gap + manifest.json + .lst files.

### `process/` — the machinery
- Stage docs `00..11` + `12-ARGUMENT` (spine/ritual) + `13-SHARPENING`
  (rung method) + `14-LISTENING` (machine ears) + `15-RHYTHM` (silence
  engine) + `16-VOICE-MATCH` (post-production loudness) + `17-CASTING`
  (voice trials/locks) — read 12 first.
- **Builders:** `scripts/make_assembly.py`, `scripts/build_seed.py`,
  `scripts/build_film_manifest.py`, `scripts/sharpen_gold.py` (log:
  gold_fix_log), `scripts/p0_mix_check.py` (mix proof),
  `scripts/ear_regression.py` (calibration), `scripts/ear_probes.py`
  (checkable-question protocol), `scripts/rebuild_text.py`
  (gloss+tts functions), `scripts/rematch2.py` (pool builder, legacy, frozen),
  `scripts/voice_match.py` (measure/apply/check post-production loudness),
  `scripts/trial_trio.py` (voice auditions), `process/scripts/render_newA.py`
  [seed|s1..|all|full] + `process/scripts/render_B.py` (AUDIO_OUT).
- **Render:** `tools/render_a_essay.py` (voice-match trims, room bridges,
  dual-pass linear, Fish free-tier, timeline manifests; sheet==master),
  `tools/validate_sheet.py` (G0 seconds-fast sheet check),
  `tools/align_verbatim_audio.py`, `tools/build_storyboard.py`.
- **Gates (verify.sh):** G0 sheet → G1 totals → G5 quote-anchor (98/98) →
  G6 TTS → G6b hardened+canary → G7 essay/chain → G8 film manifest →
  G9 local ears → files.
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
| `THREE-CLOCKS.md` | teaching/music/visual clocks + cue-sheet spec (mirror anchor fixed 2026-10-28: §4 pointer+beats; §2b2 winding reassigned to Path 3) |
| `FIVE-HOUR-CUT.md` | 6+36+90+168=300m budget table (drives film_manifest) |
| `VISUAL-MASTER-PLAN.md` | THE production doc: 24-part storyboard, 65–100 shot inventory, `source_clip/shot_id/...` schema, binding three-rule test |

### Sermon readings (2026-10-25) — the verbatim voice
`sources/sermons/audio/` = all 33 "Nibbana: The Mind Stilled" READINGS (412MB,
from the mediafire folder, key uudqwtf9aflpg via api/1.4/folder/
get_content + file-page scrape). `sources/sermons/readings/` = timestamped
transcripts (faster-whisper small.en, CF schema) via
`tools/sermon_transcribe.py` (background, /tmp/sermon_tr.log) +
SERMON-01-youtube-transcript.md (word-for-word, YT OiduBXAHtUA).
WHY IT MATTERS: the sermon text has its own narration — the verbatim
layer can be HEARD; Fish is not needed for quoting. Quote-align =
match excavation quotes against sources/sermons/readings JSONs (next queue item).

### Verbatim home (vendored 2026-10-28 — G5 no longer needs /tmp)
`sources/sermons/excavations/` = the 33 sermon excavations =
**the only verbatim home** (G5 anchors quotes there, repo-local first;
legacy `/tmp/satsang-ext/` path kept as fallback). The audio source
of truth: `sources/lectures/` (audio/ + transcripts/ + ds-full/ + ds-mp3/ + yt-subs/;
YT-only: 03,06,07,14,17,20,22,24,26,27 — YT timebase).

## Locked decisions (do not re-litigate; the owner locked these)
- **Chain:** What is Nibbana? → Why don't I see Nibbana right now? →
  What keeps it going? → How is the sense of self constructed? →
  How is Nibbana attained? → What is Nibbana like?
- **Essay 0** = six repaired units (notes §32–32c, §51, §74): motto /
  TRIPLE pointer for U2 (maññanā + only-looking + no-seer, owner
  2026-10-28: "literally the clearest explanation"; was dog-ignorance,
  then no-seer alone) / craving-gap / mirror "Ah, here I am!" / Bahiya /
  grown-cool. Every window opens and closes on the spoken answer. Q4 seam closed on
  transcript (notes §40).
- **Rungs:** 0 ⊂ A ⊂ B ⊂ C ⊂ D (ladders 21.6 / 53.1 / 121.0 / 260.7m;
  film cells 0/A/B/C 1.5/32.7/89.7/167.9m). **Archive** = the pool files
  (1147 spans, reference only — NOT a listening pass). C rung retired from
  the listening path (§62); film keeps its C-cells (167.9m) as-is.
- **Ritual (newA, owner-locked 2026-10-29):** motto bell → KID asks the
  question → 5s recollect (U1) / 3s (U2–U6, listener answers first) →
  OLD MAN gives the plain-English response (word-pause marks where mapped)
  → 5s breath → essay-0 verbatim on screen + Analayo pointer → beats
  (verbatim on screen → Analayo clip) → zoom-bell. Nothing wedges between
  question and answer. (p0-era draft rules — NO PLAIN, NO BELLS — superseded.)
- **Ending:** candle out → ordinary life → same angle → still box →
  hold → black + silence (30s coda test). Nothing rings after the hold.
- **Gospel:** TEXT VERBATIM → PLAIN (guide, mechanical) → AUDIO. Never
  authored prose anywhere, including chat (R1).
- **Done rule (DONE.md):** text gates + mix proof + 2 clean ear rounds +
  ledger. Raw model verdicts never gate (canary).
- **Owner-only domains:** question wording, essay-0 answer swaps,
  voice approval, demote calls, intros, anything by taste. Tests inform;
  they decide.

## Numbers that are true today (recomputed, not remembered)
Pool 1147 spans ~20.76h · gold 555 · core **83 clips** (71 + 12 hunt §75) ·
seed 47 events, ~4.5m rendered (bell/Q/plain/5s-breath/essay0 canon, rhythm.json slots) ·
ladder A 21.6m / B 53.1m / C 121.0m / D 260.7m, nesting
0⊂A⊂B⊂C⊂D proven per section · film screening 291.8m (~4h52, FILM-CUT
current) · G8 fully green · G5 98/98 semantic anchors.
newA render: build/audio_newA/ (seed + S1..S6 + full, analayo-only,
bells, kid Q + old-man plain, Nirvana spoken) — fresh render 2026-10-29,
all sections validated. Voice match 0.1-0.2 LU + mix proof PASS.
B render: build/audio_B/full_B_essay.mp3 (NEW B: ~57m, 56.6m speech:). FINAL PASS 2026-10-29:
B re-picked (53.1 -> 56.7m speech; +definitions/equations/charter verses per
§97, -116s S3 fat, Upatissa cut) — RE-RENDER + MIX + VOICE + EARS QUEUED.
NOT stamped (old stamp was pre-merge audio).

## Next queue (in order)
1. **Taste locks (owner — the packet, updated 2026-10-29):** (a) U6 grown-cool stands
   (callback-gamble disclosed §37); (b) ~~Fish voice approval~~ DONE —
   kid asks + wise-old-British answers (backup elderly-ref); Osho retired;
   (c) 7 demote-candidates
   (gold_fix_log.json demotes — was 16, trims resolved 9); (d) human
   intros (slots empty by design, build/canon/human-scripts.md); (e) YT
   cold opens S3b1/S6b1 (ears required, transcripts can't arbitrate).
   P1–P12 applied §61 (off the list). Tests inform; they decide.
2. **p1 (bells + sfx, future):** bells back (motto/zoom) + sfx kit wiring
   (bowls/ding/break/blocks per assets/sfx/README.md) + YT anchor-maps at cut.
   STATUS: `build/canon/yt_anchor_map.json` measured (whisper word-times,
   multi-anchor incl. L20 per-window offsets); seed proof rendered to
   `build/audio_p1/` (bowls→bells). newA (analayo-only) is the current
   listening path; p1 remains for a future belled full-A render.
   Driver: `process/scripts/render_p1.py [seed|all]`.
3. **Cue sheet** (visual-master-plan §7 schema): per beat —
   source_clip, essay_depth, visual_motif, shot_id, audio_cue,
   duration, reuse_from. Absolute timestamps after audio master.
   (C rung retired §62 — no C-curation pass.)
4. **G-ear live** (DONE: `process/scripts/ear_local.py` wired as G9 —
   whisper order + essay-0 phrases (fuzzy key_heard + narrow retry;
   persistent misses are ADVISORY, transcript wins) + seam regression,
   zero tokens, cached. Qwen rounds: 0+A stamped (two clean rounds);
   B rounds queued. (14-LISTENING free-first protocol.)

## Traps (the ones that actually bit)
- **R6 inline drift:** never paste builder code in chat/shell — use
  the scripts. `build_seed` and `build_film_manifest` exist BECAUSE
  of this.
- **rebuild_text.main is fixed** (§33: td = build/) — the old trap below
  is retired. Import its functions, never hand-edit below-lines.
- **sharpen_gold.py is FROZEN (2026-10-28):** rerun DELETES the §59/§61
  promotion spans (observed: etymology/fire-catechism/mid-ocean dropped).
  gold_fix_log.json is history of the §38 run, not current state —
  current truth is seg JSONs + manifest_index.json. Revive only with a
  promotion allowlist + diff review.
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
  Whisper itself is nondeterministic run-to-run on identical bytes
  (measured 1237/2279/2794 chars) — fuzzy-match phrases, retry narrow,
  and downgrade persistent misses to advisory; transcript wins.
- **Cache keys cover every input** (axiom 16): the 2026-10-29 wrong-cast
  render shipped Osho slices under the kid/old cast because vid wasn't in
  the vox hash. After any voice/trim change, stale slices serve silently.
- **Symlinks rot silently under cache hits**: the 2026-10-28 reorg broke
  10 lecture symlinks; every render hit cache and never touched the mp3s
  until the first miss crashed. After any move: `find -xtype l` first.
- **Snaps only shrink** (M-R8): essay-0/B* windows atomic; fragment-head
  rule YT-only; motto opens exempt.
