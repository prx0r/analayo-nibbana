# Ear-regression fixtures (run on any model/prompt/engine change)

Expected = FINDINGS, never the verdict token (both directions proven
unreliable 2026-10-26: seeded-defect file can flag cuts while the token
says FLOWS/CLEAN).

| file | must produce |
|---|---|
| bad_blip.mp3 (30ms fade-out bug, then silence) | silence/cut finding |
| bad_midcut.mp3 (motto entered mid-sentence) | mid-thought-start finding |
| bad_trunc.mp3 (100KB of 425KB) | cutoff finding |
| bad_quiet.mp3 (Fish Q at -20dB) | unnatural-quiet finding |
| bad_chant.mp3 (Pali chant, no context) | contextless-chant finding |
| good_motto.mp3 / good_analayo.mp3 / good_fish.mp3 | no defect findings (mild notes OK) |

Runner: process/scripts/ear_regression.py (descriptive prompts, one clip
per call). Any miss = ears uncalibrated: stop, fix prompt/model, re-run.
