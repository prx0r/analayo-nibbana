# SPEAKER RULES — v5 (2026-10-28). Matches the build as it stands.

Analayo's archive audio is BOTH voices already: his reading of Nanananda
(incl. all Pali) + his own explanatory comments.

## The two voices (analayo-only rule, owner 2026-10-28)
1. **ANALAYO (archive, untouched)** — every spoken teaching clip. Inside
   beats he both reads Nanananda and explains him; the assembly never
   splits a clip. He owns ALL spoken Pali (mottos, verses) — no other
   voice touches Pali.
2. **FISH (TTS guide)** — two jobs, all English-only:
   a. the section question at every ritual open ("What is Nirvana?" spoken;
      data keeps Nibbana — 6 questions, verbatim from build/human-scripts.md
      headers; these ARE the 6-slot argument, process/12-ARGUMENT.md),
   b. the plain-English RESPONSE in every section opening (the essay-0
      plain; spoken == on-screen plain, G7a2-gated).
   Fish never speaks Pali. Beat plains live ON SCREEN only (analayo-only).
3. **HUMAN (you)** — section intros only (~40s × 6, your words: what it
   answers, why now — DRAFT in build/human-scripts.md). No Pali (his
   voice owns it), no verses. Bridge lines ONLY where marked BRIDGE —
   none currently marked; default is pause, not words.

## Per-section order (identical everywhere — the listener learns it once)
motto bell → Fish asks the question → 3s recollect → Fish gives the
plain-English response → essay-0 verbatim on screen + Analayo pointer →
beats (verbatim on screen → Analayo clip) → zoom bell. Nothing wedges
between question and plain, or plain and essay-0.
Section close: zoom bell (S6: seed reprise + motto bell + 30s silence).

## Bells (synthesized, fixed — build/assets/)
- **Motto bell**(bright, 2.5s): with "this is excellent" — refrain
  moments + every section open. 10 across the core.
- **Zoom bell** (low + sub octave, 6.0s): section thresholds only
  (5 across the build), never within 30s of a motto bell.

## Hard rules (violations fail the build)
- No invented sentences in Fish's mouth — script or glosses only,
  both deterministic from verbatim + key.
- No Pali in TTS lines — verified by scan (no diacritics, no leading
  Pali chunks; inline terms carry immediate English glosses).
- No voice overlaps another; pauses are separate events in the manifest.
- Verbatim is extracted, with provenance — never typed (see
  process/AXIOMS.md).
