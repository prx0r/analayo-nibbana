# SPEAKER RULES — v4 (2026-10-24). Matches the build as it stands.

Analayo's archive audio is BOTH voices already: his reading of Nanananda
(incl. all Pali) + his own explanatory comments. Measured on core v4:
most clips are him reading Nanananda; only S1 leans explaining.

## The three voices
1. **ANALAYO (archive, untouched)** — opens every section cold (motto
   bell, then his motto reading — no Fish before him). Inside beats he
   both reads Nanananda and explains him; the assembly never splits a
   clip.
2. **FISH (TTS)** — two jobs, both English-only, never narration:
   a. the plain-English line per beat (the gloss, TTS-punctuated),
   b. term drops when Analayo's audio speaks Pali (mapped word only,
      max ~5 words, first hearing per section, max 2 per clip —
      23 drops across the whole core).
   Fish never speaks Pali. Fish never explains, primes, or bridges.
3. **HUMAN (you)** — section intros only (~40s × 6, your words: what it
   answers, why now — DRAFT in build/human-scripts.md). No Pali (his
   voice owns it), no verses. Bridge lines ONLY where marked BRIDGE —
   none currently marked; default is pause, not words.

## Per-beat order (identical everywhere — the listener learns it once)
Nanananda verbatim on screen → Fish speaks the plain English →
1.5s breath → [term drops if Pali is heard] → Analayo clip plays →
2.5s water → next beat. Section cold open: motto bell → Analayo reads
the motto (no Fish first). Internal motto refrains get the motto bell.
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
