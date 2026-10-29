# 16 — VOICE MATCH. Post-production loudness (2026-10-29).

The guide (kid questions + old-man plains, studio TTS) and the archive
(Analayo, lecture room, dynamic) must sit in one room. This is proven with
meters, not ears — and without any plugin.

## No plugins. The whole chain is ffmpeg.

Measurement and correction use exactly one instrument: ffmpeg's
`loudnorm` filter in dual-pass mode (measure JSON → linear gain).
`process/scripts/voice_match.py` wraps it in three verbs:

- `measure [dir]` — splits every section mp3 by manifest timeline into
  GUIDE ranges (fish + plain events) vs ARCHIVE ranges (analayo events),
  concats each role, reports integrated LUFS per role, writes
  `build/canon/voice_match.json` (`{guide: trim, archive: 0.0}`).
- `apply [dir] [trim]` — timeline-edit `volume=` on guide ranges only
  (single ffmpeg pass, sample-accurate; everything else bit-identical),
  then loudnorm-linear re-norm (uniform gain preserves the new match).
  NO re-render, NO TTS — runs while the Fish API is on fire.
- `check [dir]` — re-measures; FAILS (exit 1) if guide-vs-archive gap
  exceeds 1.0 LU.

House numbers (2026-10-29): guide −13.1 vs archive −13.5 → trim −0.5 →
re-measured gap 0.1–0.2 LU. Per-section gaps all within ±1.3 BEFORE the
trim — levels were already close; the perceived gap is dynamics/brightness,
not level (see §Taste below).

## The anchor rule (binding)

ARCHIVE stays at trim 0.0 — the lecture audio is the historical record and
is never touched by mastering. The synthetic voices move to match it, for
free, forever. `render_a_essay.py` reads the trims and applies them
POST-loudnorm inside `VOICE_AF_FISH` (a trim placed BEFORE a fixed-target
loudnorm is erased by it — measured 2026-10-29: −0.5dB in, 0.0dB out).
The trim is part of the vox cache hash (R6 rule: every input that shapes
bytes is in the key — voice IDs are too, after the 2026-10-29 wrong-cast
incident).

## Taste vs meter (read before reaching for EQ)

Meters prove LEVEL. If the archive still *feels* quieter at 0.2 LU, that is
dynamics (TTS is compressed flat; Analayo breathes) and brightness (kid
presence vs room tone) — a taste call, never a meter fix. Options, in order:
(1) leave it; (2) archive presence lift / gentle compression as an explicit
owner-dated override in voice_match.json; (3) full voice-profile EQ later.
Never "fix" perception with the trim — the trim is the meter's, and the
meter says 0.2.

## Run order (post-production, after any render touching voices)

`voice_match.py check` → if gap > 1.0: `measure` → `apply` → `check`
→ mix proof → ears on the delta → stamp.
