# The Process: sermon series → condensed explainers

Turn a long recorded teaching series into short self-contained explainers
without writing a single word of doctrine yourself.

## What it is

Given a **primary source** (the teaching text) and an **mp3 rendition**
(someone speaking it — lectures, readings, commentary), this process
produces the same material at widening radius — rungs, not versions:

- **Archive** — everything kept, reordered from sermon order into *argument
  order* (6 segments here, 1147 spans, ~20.8h). Reference only, never played.
  Navigable, nothing wasted.
- **D (45m)** — curated deepening (260.7m total).
- **C (20m)** — curated deepening (121.0m total).
- **B (10m)** — curated subsets + whole old-A where it fits (53.1m total).
- **A newA (3–5m)** — one killer arc per section (83 core clips:
  pointer + 3–7 beats, 21.6m speech). The clearest explanation.
- **0 seed (~20s each)** — six Q→plain→pointer micro-sessions chained
  (47 events, 4.5m rendered).

Each core beat is a fixed 3-layer stack:

1. **Analayo** (archive audio clip: `lec,start,end`) — the structure. His
   voice carries both the reading AND the explanation; the transcripts'
   `Comment ... End of comment` markers are the decompilation.
2. **Nanananda verbatim** (exact excavation quote, provenance recorded) —
   shown (and heard, since he reads it). Never typed, only extracted.
3. **Plain English below** (deterministic key transform, no free text) —
   what it means, unmistakable words. The guide voice (KID asks, OLD MAN
   answers) speaks questions + plain responses; beat plains stay on screen.

Plus: Fish term-drops (mapped Pali word → English, first hearing per
section), human intro per segment, bells + pauses per the rhythm engine
(`15-RHYTHM.md`: named slots, per-unit overrides, word-pause marks).

## The pipeline (each step has its own doc)

```
00 INPUTS          primary text + mp3 + transcripts
01 TRANSCRIBE+CUT  sentences -> keeps -> cutplans (era-1, frozen; see sources/lectures/cutplans/)
02 SEGMENT         every kept span -> exactly one of N segments, clustered, ordered
03 GOLD+CORE       A-only spines -> killer beats (+ hand fixes, all logged)
04 PAD+GLOSS+VOICE verbatim assignment w/ provenance -> key gloss -> TTS lines -> guide + archive voices
05 RENDER          ffmpeg assembly (render_newA.py [seed|s1..|all|full], render_B.py + AUDIO_OUT), loudnorm, bells, room bridges
06 QA              gates at every stage (G0 sheet, provenance, flow, hold-up, TTS, ears)
--- between 06 and ship lives the FINAL LOOKOVER: reviews/REVIEW.md (read every
    beat as a first-time listener, findings only, then an amendment
    pass that fixes with sourced quotes — logs in CONDENSED-BUILD-NOTES)
```

## The film layer (see HANDOVER.md at repo root)
Same material, four cumulative cells for one five-hour screening:
**0 (1.5m) ⊂ A (32.7m) ⊂ B (89.7m) ⊂ C (167.9m)** — membership
in `build/canon/film_manifest.json`, budgets from `visuals/FIVE-HOUR-CUT.md`,
gates: G8 (nesting + ceilings + provenance + chain). The visual design
canon lives in `visuals/` (11 docs; index in HANDOVER). The listening ladder
(0/A/B/C/D + archive) is built by `build_newA.py` / `build_rungs.py` from
the same assemblies; rung manifests live in `build/canon/`.

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
`15-RHYTHM.md` (the silence engine: named slots, per-unit overrides,
word-pause marks; sheet==master).
`16-VOICE-MATCH.md` (post-production loudness: measure/apply/check, no
plugins, archive-anchored trims).
`17-CASTING.md` (voice trials, locked cast + backup, speakability proofs).
`18-MODIFICATIONS.md` (the change loop: edit data → sheet → rebuild →
section render → prove → log → commit).
`07-PLAIN-ENGLISH-STANDARD.md` (testable plainness + blunting),

## What it guarantees

- No invented doctrine: every sacred word is an exact, provenanced slice
  of the source (reconstruction asserted, independently re-extracted).
- No slop narration: the guide speaks script only; below-lines are pure
  function of (verbatim, key). Deterministic — reruns are byte-identical.
- Nothing lost: pool holds 100% of kept material; gold/core are views.
- Flow is read, not assumed: every core read as a script, joins fixed.
