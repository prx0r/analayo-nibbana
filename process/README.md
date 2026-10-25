# The Process: sermon series → condensed explainers

Turn a long recorded teaching series into short self-contained explainers
without writing a single word of doctrine yourself.

## What it is

Given a **primary source** (the teaching text) and an **mp3 rendition**
(someone speaking it — lectures, readings, commentary), this process
produces 3 versions of the same material:

- **V1 Pool** — everything kept, reordered from sermon order into *argument
  order* (6 segments here, ~20.7h). The archive. Navigable, nothing wasted.
- **V2 Gold** — the A-grade spine only (~6.3h). The deep dive.
- **V3 Core** — one killer beat per cluster (~96 min Analayo + pads/pauses
  ≈ 2h). The clearest explanation. Self-contained movies, one per segment.

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
--- between 05 and 06 lives the FINAL LOOKOVER: REVIEW.md (read every
    beat as a first-time listener, findings only, then an amendment
    pass that fixes with sourced quotes — logs in CONDENSED-BUILD-NOTES)
```

Supporting files: `AXIOMS.md` (binding rules), `SKILLS.md` (reusable
techniques), `MISTAKES.md` (everything we got wrong + fixes),
`REPRODUCE.md` (exact rerun), `FILES.md` (artifact map),
`12-ARGUMENT.md` (constructed order + question ritual), `REVIEW.md`
(root: the final lookover itself), `scripts/`
(the deterministic tooling), `verify.sh` (one-command audit),
`07-PLAIN-ENGLISH-STANDARD.md` (testable plainness + blunting),
`08-PORTING.md` (new texts/languages, e.g. Sanskrit),
`09-BELLS-ZOOM.md` (two-bell grammar + zoom assembly order),
`10-MATHEMATICS.md` (measured structure: 6, 72, ~3.5×, 340, 2, 1).
`11-STICKINESS.md` (why the format sticks: mechanisms already in the build, cheap adds, parked jokes track, portability verdict).

## What it guarantees

- No invented doctrine: every sacred word is an exact, provenanced slice
  of the source (reconstruction asserted, independently re-extracted).
- No slop narration: Fish speaks mapped words only; below-lines are pure
  function of (verbatim, key). Deterministic — reruns are byte-identical.
- Nothing lost: pool holds 100% of kept material; gold/core are views.
- Flow is read, not assumed: every core read as a script, joins fixed.
