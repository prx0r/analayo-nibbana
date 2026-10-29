# DONE — definition of done (adapted vatulanatha pattern, 2026-10-26)

A rung (0/A/B) is DONE when **all four** hold:

1. **Text gates PASS** (`process/verify.sh`: totals, provenance, TTS,
   essay, film, files).
2. **Mix proof PASS** (`process/scripts/p0_mix_check.py`: order==assembly,
   every spec bed present at position, edges audible, levels in band).
3. **Two consecutive ear rounds with zero blocking findings after
   adjudication** (adapted whole-mix rule: our full is 132 min, so rounds
   run per-section whole files + seed, not one giant mix).
4. **Every raw finding classed and ruled** in `build/ears/EAR_LEDGER.md`.

**The raw model verdict is never the gate** (canary 2026-10-26: blind
10-clip battery scored 10/10 PASS with confabulated reasons). Findings,
not tokens: mechanical claims → p0_mix_check/maps; text claims →
whisper/transcript (transcript wins); then count blocking findings.

## Taxonomy (blocking rules)

mechanical → **block** · structural → **block** · flow-with-evidence →
adjudicate (maps/cross-checks) · taste → policy row (once, never
re-litigated) · transcript-level → discard (G5 guarantees by
construction) · unstable → discard when refuted by verbatim.

## Ear-regression fixtures (run on any model/prompt/engine change)

- `build/ears/ear_fixtures/bad_*.mp3` (5) + `good_*.mp3` (3), tracked.
  Runner: `process/scripts/ear_regression.py` (descriptive prompts,
  full texts to `build/ears/ear_regression_last.json`).
- 2026-10-26 calibration: keyword-gating scored 4/8 (midcut needs
  expected-text to judge a start as mid-thought; 2s good_fish
  false-alarmed). So fixtures are CALIBRATION, not a gate: a human
  reads the eight texts each run; drift (new misses, new false alarms)
  blocks model/prompt changes, never the build. Mid-thought detection
  stays mechanical (whisper edge-words vs expected).

Next product of this pattern auto-closes on gates 1+2 unless a **novel**
finding class appears (new class → ledger row → rule).
