# 05 — RENDER. Audio is always last. (Machinery: render_newA.py / render_B.py drivers → tools/render_a_essay.py; sheet validated first by tools/validate_sheet.py = G0.)

## Preconditions (all verified before a single cut)
- `tools/validate_sheet.py` green (seconds).
- Textual flow audit complete, all fixes applied (03).
- Provenance 100%, TTS lines English-first (04).
- Audio inventory: which clips have DS-native mp3 vs YT-only
  (here: 33/33 present; 10 YT-timebase lectures cut via measured per-window
  offsets in build/canon/yt_anchor_map.json — incl. L20 per-window).
  Missing audio NEVER blocks text work; it blocks only final assembly.

## Cut + assemble (ffmpeg, via the drivers — never hand-rolled)
- Per clip: sample-accurate hybrid seek (fast input seek + output trim),
  TAIL 0.6s so the last word finishes before the fade; fades live on the
  untrimmed base (fades at trimmed times once silenced whole slices).
- YT-only lectures: anchor-map times to DS audio, then snap every boundary
  to the nearest pause. Never ship un-snapped YT timings.
- Bed: room-tone bridges from lecture gaps (no library silence, no digital
  zero on archive transitions — same room); Fish lines are studio-dry TTS.
- Per-clip `afade t=in 0.03s / t=out` (fade-out never st=0); full-mix
  dual-pass LINEAR `loudnorm` (-16 LUFS — dynamics preserved, never pumped);
  bells sit under voice; post-production voice trims via voice_match.py.
- Driver: `render_newA.py [seed|s1|..|all|full]` (section-scoped fast
  iteration; `full` only re-concats), `render_B.py` with
  `AUDIO_OUT=build/audio_B` (never renders into another rung's dir).

## Cough/artifact cover
- Coughs cluster in ALREADY-CUT gaps (pauses the transcriber marks) —
  most vanish with the cuts. Leftovers: micro-cut ±0.3s or cover with
  the breath bed. Flag during QA listen; never hunt blindly.

## Outputs
Per-section mp3s + full assembly (manifest.json carries the per-slice
timeline = the sheet; re-renders assert sheet==master). Dry-run the sheet
first (validate_sheet.py, seconds), re-encoded master second. Fail the stage
if: any boundary unsnapped, any loudness drift, any bell masking speech,
any cough surviving the pass.
