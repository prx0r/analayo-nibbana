# AGENTS.md — read this first. Then you know where you are.

You are in **analayo-nibbana**: 33 Analayo lectures on Ñāṇananda's
*Nibbāna: The Mind Stilled*, compressed into one argument (six questions,
rungs 0/A/B/C/D + film). No other repo's rules apply here.

## Read order (do not skip, do not reorder)

1. **This file** (you are here) — 2 minutes, the map.
2. `CONDENSED-BUILD-NOTES.md` — THE LOG. Append-only session history (§1–§96;
   §§1–86 frozen history, §87+ the living tail).
   It takes **precedent over every other doc including this one**: when two
   docs disagree, the log's latest dated entry wins. Your first job on any
   confusion is to check what the log says, not to reason from first principles.
3. `VISION.md` — the owner's intent (north star; taste lives here, not in gates).
4. `HANDOVER.md` — current state: branch, numbers, queue, traps.
5. `process/RECURRING-MISTAKES.md` — R1 (never author prose) and R9
   (verify content, not proxies) have bitten every agent so far.
6. `process/AXIOMS.md` + `process/12-ARGUMENT.md` — binding rules.
7. `build/canon/README.md` — what the product data is and what reads it.

Then the work at hand: `TODO`-equivalent is HANDOVER's "Next queue";
history is `reviews/` (frozen — read, never edit).

## The shape of this repo (after 2026-10-28 reorg)

```
AGENTS.md · HANDOVER.md · VISION.md · DONE.md · SPEAKER-RULES.md
TIMINGS.md · FILM-CUT.md · CONDENSED-BUILD-NOTES.md   living root docs
reviews/            frozen first-listener reviews (REVIEW.md, REVIEW-Q1–6, COVERAGE)
archive/era-1-cutplans/  frozen era-1 method (CUTTING-FORMULA.md, HANDOFF.md)
sources/
  lectures/         PRIMARY ANALAYO: audio/ transcripts/ yt-subs/ ds-full/ ds-mp3/ cutplans/
  sermons/          PRIMARY NANANANDA: excavations/ audio/ readings/
build/
  canon/            THE PRODUCT DATA (essay0, assemblies, manifests, segs, keys)
  versions/         superseded, dated, do-not-build-from (VERSIONS.md explains)
  ears/             ear rounds + ledger (DONE evidence)
  audio_*/ assets/  renders (local-only, gitignored) + bells/sfx
process/            machinery: stage docs 00–14, scripts/, verify.sh (run it)
tools/              era-1 cutplan tools (frozen method) + live render/storyboard
visuals/            film design canon (binding specs)
```

## Laws (violations fail the build)

1. **Gospel:** TEXT VERBATIM → PLAIN ENGLISH → AUDIO. Never author prose —
   not in files, not in chat (R1). Questions + intros are the owner's;
   answers are verbatim only.
2. **Canon is single-source:** `build/canon/essay0.json` is THE essay-0.
   Builders read `build/canon/`; gates check `build/canon/`. Never write
   outside it, never check a different path than the writer's (axiom 13).
3. **Gates before and after every change:** `bash process/verify.sh`
   (ALL PASS or stop). Fix data/keys, never the gate.
4. **Rungs:** 0 seed ⊂ A newA ⊂ B ⊂ C ⊂ D, archive = reference (not a pass).
   C retired from the listening path (§62); film keeps C-cells.
5. **Raw model verdicts never gate** (DONE.md taxonomy). Mechanical claims →
   meters; text claims → whisper/transcript (transcript wins).
6. **Frozen stays frozen:** `reviews/`, `archive/`, `CONDENSED-BUILD-NOTES.md`
   §§1–86, `build/versions/`, era-1 tools. Log new findings; never edit old ones.
7. **Audio never commits** (`build/audio_*` gitignored). New artifact →
   note it in the log the same day.
