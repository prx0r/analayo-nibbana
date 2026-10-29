# The Process: sermon series → condensed explainers

Turn a long recorded teaching series into short self-contained explainers
without writing a single word of doctrine yourself.

## What it is

Given a **primary source** (the teaching text) and an **mp3 rendition**
(someone speaking it — lectures, readings, commentary), this process
produces 3 versions of the same material:

- **V1 Pool** — everything kept, reordered from sermon order into *argument
  order* (6 segments here, ~20.7h). The archive. Navigable, nothing wasted.
- **V2 Gold** — the A-grade spine only (~6.9h). The deep dive.
- **V3 Core** — one killer beat per cluster (83 clips: 71 + 12 hunt-found §75,
  ~1.7h Analayo + pads/pauses ≈ 2h). The clearest explanation. Self-contained movies, one per segment.

Each core beat is a fixed 3-layer stack:

1. **Analayo** (archive audio clip: `lec,start,end`) — the structure. His
   voice carries both the reading AND the explanation; the transcripts'
   `Comment ... End of comment` markers are the decompilation.
2. **Nanananda verbatim** (exact excavation quote, provenance recorded) —
   shown (and heard, since he reads it). Never typed, only extracted.
3. **Plain English below** (deterministic key transform, no free text) —
   what it means, unmistakable words. Fish speaks the TTS version.

Plus: Fish term-drops (mapped Pali word → English, first hearing per
section), human intro per segment, bells + pauses per the flow grammar.

## The pipeline (each step has its own doc)

```
00 INPUTS          primary text + mp3 + transcripts
01 TRANSCRIBE+CUT  sentences -> keeps -> cutplans (A/B/C/D, seams)
02 SEGMENT         every kept span -> exactly one of N segments, clustered, ordered
03 GOLD+CORE       A-only spines -> killer beats (+ hand fixes, all logged)
04 PAD+GLOSS+VOICE verbatim assignment w/ provenance -> key gloss -> TTS lines -> 3 speakers
05 QA              gates at every stage (provenance, flow, hold-up, TTS)
06 RENDER          ffmpeg assembly, loudnorm, bells, cough cover
--- between 05 and 06 lives the FINAL LOOKOVER: reviews/REVIEW.md (read every
    beat as a first-time listener, findings only, then an amendment
    pass that fixes with sourced quotes — logs in CONDENSED-BUILD-NOTES)
```

## The film layer (added 2026-10-25, see HANDOVER.md at repo root)
Same material, four cumulative rungs for one five-hour screening:
**0 (seed, 6 questions) ⊂ A (33m) ⊂ B (90m) ⊂ C (168m)** — membership
in `build/canon/film_manifest.json`, budgets from `visuals/FIVE-HOUR-CUT.md`,
gates: G8 (nesting + ceilings + provenance + chain). The visual design
canon lives in `visuals/` (11 docs; index in HANDOVER). The next build
artifacts: the cue sheet (VISUAL-MASTER-PLAN §7 schema) and Fish
speaking the plain line after each clip.

Supporting files: `RECURRING-MISTAKES.md` (the patterns I keep
repeating — read FIRST, before touching anything), `AXIOMS.md` (binding rules), `SKILLS.md` (reusable
techniques), `MISTAKES.md` (everything we got wrong + fixes),
`REPRODUCE.md` (exact rerun), `FILES.md` (artifact map),
`12-ARGUMENT.md` (constructed order + question ritual), `reviews/REVIEW.md`
(root: the final lookover itself), `scripts/`
(the deterministic tooling), `verify.sh` (one-command audit),
`07-PLAIN-ENGLISH-STANDARD.md` (testable plainness + blunting),
`08-PORTING.md` (new texts/languages, e.g. Sanskrit),
`09-BELLS-ZOOM.md` (two-bell grammar + zoom assembly order),
`10-MATHEMATICS.md` (measured structure: 6, 72, ~3.5×, 340, 2, 1).
`11-STICKINESS.md` (why the format sticks: mechanisms already in the build, cheap adds, parked jokes track, portability verdict).
`13-SHARPENING.md` (the rung method: A first → distill 0 → B/C by sequence
law; minimal moves; essay-0 re-derivation test).
`14-LISTENING.md` (machine ears: why listen when text is proven; audit ear
vs critic ear with ratings; meters beside ears; operating limits; taste
locks stay human).

## What it guarantees

- No invented doctrine: every sacred word is an exact, provenanced slice
  of the source (reconstruction asserted, independently re-extracted).
- No slop narration: Fish speaks mapped words only; below-lines are pure
  function of (verbatim, key). Deterministic — reruns are byte-identical.
- Nothing lost: pool holds 100% of kept material; gold/core are views.
- Flow is read, not assumed: every core read as a script, joins fixed.
