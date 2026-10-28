# 05 — RENDER. Audio is always last.

## Preconditions (all verified before a single cut)
- Textual flow audit complete, all fixes applied (03).
- Provenance 100%, TTS lines English-first (04).
- Audio inventory: which clips have DS-native mp3 vs YT-only
  (here: 33/33 present; 10 YT-timebase lectures cut via anchor map
  build/yt_anchor_map.json — DS leads YT 0–30s depending on lecture).
  Missing audio NEVER blocks text work; it blocks only final assembly.

## Cut + assemble (ffmpeg)
- Per clip: `ffmpeg -ss START -to END -i LECTURE.mp3` (+0.15s handles),
  re-encode at assembly (mp3 `-c copy` concat throws DTS warnings —
  harmless in dry-run, re-encode for real).
- YT-only lectures: anchor-map times to DS audio when fetched
  (`t_ds = ds_first + (t_yt-yt_first)*ratio`), then snap every boundary
  to the nearest pause. Never ship un-snapped YT timings.
- Bed: 1.5s breath inside beats, 2.5s water between groups, motto
  cold-open per section, bell per motif (F/C/R/D/Z/L), terminal 30s
  silence on §6 (no climax — stilling, not resolution).
- Per-clip `afade t=in/out 0.15s`; full-mix `loudnorm` (-16 LUFS stereo);
  bells at -20dB under voice; room tone from lecture gaps (no library
  silence — same room).

## Cough/artifact cover
- Coughs cluster in ALREADY-CUT gaps (pauses the transcriber marks) —
  most vanish with the cuts. Leftovers: micro-cut ±0.3s or cover with
  the breath bed. Flag during QA listen; never hunt blindly.

## Outputs
Preview mp3s per segment (here: 10.2m §1 partial proven), then full
masters. Dry-run concat first (fast, lossy-tolerant), re-encoded master
second. Fail the stage if: any boundary unsnapped, any loudness drift,
any bell masking speech, any cough surviving the pass.
