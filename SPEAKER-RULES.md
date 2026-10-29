# SPEAKER RULES — v6 (2026-10-29). Matches the build as it stands.

Analayo's archive audio is BOTH voices already: his reading of Nanananda
(incl. all Pali) + his own explanatory comments.

## The two voices (analayo-only rule; guide = OSHO, owner 2026-10-29)
1. **ANALAYO (archive, untouched)** — every spoken teaching clip. Inside
   beats he both reads Nanananda and explains him; the assembly never
   splits a clip. He owns Pali inside clips (mottos, verses he reads).
2. **OSHO (Fish TTS guide, `06134e9a…` — shiva trio)** — two jobs:
   a. the section question at every ritual open ("What is Nibbana?" —
      data, screen and speech all say Nibbana; Osho proven on carrier
      probes 2026-10-29, whisper round-trip exact),
   b. the plain-English RESPONSE in every section opening (the essay-0
      plain; spoken == on-screen plain, G7a2-gated; word-pause marks
      from `build/canon/rhythm.json` land inside the line).
   Osho speaks Nibbana cleanly, so the old Nirvana substitution is deleted.
   Beat plains live ON SCREEN only (analayo-only).
3. **HUMAN (you)** — section intros only (~40s × 6, your words: what it
   answers, why now — DRAFT in build/canon/human-scripts.md). No Pali (his
   voice owns it), no verses. Bridge lines ONLY where marked BRIDGE —
   none currently marked; default is pause, not words.

## Per-section order (identical everywhere — the listener learns it once)
motto bell → Osho asks the question → 5s recollect (U1; 3s elsewhere) →
Osho gives the plain-English response (word-pause marks where mapped) →
5s breath → essay-0 verbatim on screen + Analayo pointer →
beats (verbatim on screen → Analayo clip) → zoom bell. Nothing wedges
between question and plain, or plain and essay-0.
Section close: zoom bell (S6: seed reprise + motto bell + 30s silence).

## Bells (synthesized, fixed — build/assets/)
- **Motto bell**(bright, 2.5s): with "this is excellent" — refrain
  moments + every section open.
- **Zoom bell** (low + sub octave, 6.0s): section thresholds only,
  never within 30s of a motto bell.

## Hard rules (violations fail the build)
- No invented sentences in Osho's mouth — script only, deterministic.
- Marks land inside Osho's line only (never in archive clips); each mark
  asserts its anchor word once, in order — fail loud otherwise.
- No voice overlaps another; pauses are separate events in the manifest.
- Verbatim is extracted, with provenance — never typed (see
  process/AXIOMS.md).
