# SPEAKER RULES — v7 (2026-10-29). Matches the build as it stands.

Analayo's archive audio is BOTH voices already: his reading of Nanananda
(incl. all Pali) + his own explanatory comments.

## The two voices (analayo-only rule; guide = KID + OLD MAN, owner 2026-10-29)
1. **ANALAYO (archive, untouched)** — every spoken teaching clip. Inside
   beats he both reads Nanananda and explains him; the assembly never
   splits a clip. He owns Pali inside clips (mottos, verses he reads).
2. **KID + OLD MAN (Fish TTS guide; trialed 5+6, picks locked 2026-10-29)** —
   a. KID asks every section question (`0c0f9d…` inquisitive; backup: none —
      rotation across questions possible later),
   b. OLD MAN answers every plain (`98db23…` wise old British; backup:
      elderly-ref `f40115…`, the original).
   Speech says NIRVANA (data keeps Nibbana; substitution at voice time).
   Word-pause marks from `build/canon/rhythm.json` land inside plain lines.
   Beat plains live ON SCREEN only (analayo-only).
3. **HUMAN (you)** — section intros only (~40s × 6, your words: what it
   answers, why now — DRAFT in build/canon/human-scripts.md). No Pali (his
   voice owns it), no verses. Bridge lines ONLY where marked BRIDGE —
   none currently marked; default is pause, not words.

## Per-section order (identical everywhere — the listener learns it once)
motto bell → KID asks the question → 5s recollect (U1; 3s elsewhere) →
OLD MAN gives the plain-English response (word-pause marks where mapped) →
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
- No invented sentences in the guide's mouth — script only, deterministic.
- Marks land inside the OLD MAN's line only (never in archive clips); each mark
  asserts its anchor word once, in order — fail loud otherwise.
- No voice overlaps another; pauses are separate events in the manifest.
- Verbatim is extracted, with provenance — never typed (see
  process/AXIOMS.md).
