# 15 — RHYTHM. The silence engine (2026-10-29).

Words end; meaning lands in the pause after them. Every silence in the
build is a NAMED SLOT with a default duration. Defaults hold unless a unit
carries an owner-dated override with a reason. No magic numbers in builders.

## The contract

1. `build/canon/rhythm.json` is the single source: `slots` (defaults),
   `overrides` (per-unit, per-slot, `{dur, why}`), `marks` (word-pause
   anchors per unit). `rhythm.md` beside it is the human-readable map.
2. `make_assembly.py` + `build_seed.py` read it via `R(s, slot)`; every
   pause/breath/water event takes its duration from there. Builders assert
   each override carries `{dur, why}` — an undated override fails the build.
3. The assembly timeline IS the sheet: `render_a_essay.py` asserts
   sheet==master every render. `tools/validate_sheet.py` proves the sheet
   coherent in seconds, before any audio exists.
4. Silence is ROOM AIR for archive transitions (bridges from neighboring
   lecture rooms, ~30dB under speech), never digital zero. Marks INSIDE a
   Fish line are the exception: TTS is studio-dry, so marks render as
   digital silence — correct, because they mimic TTS's own comma prosody,
   only longer. (Qwen "no pause" readings confirm continuity; volumedetect
   confirms the air.)

## Slots (defaults; see rhythm.json — the file, not this doc, is truth)

recollect 3.0 · plain_breath 5.0 · triple_breath 1.5 ·
essay0_stillness 2.5 · beat_breath 1.5 · beat_water 2.5 +1/60s cap 6 ·
settle 6.0 · terminal 30.

## Word-pause marks (2026-10-29)

`marks[unit] = [{after, dur, why}]`. The render splits the Fish line at
each anchor, TTSes each chunk, joins with digital-silence gaps. Each anchor
must match EXACTLY ONCE in that unit's opener plain — asserted at render
(and pre-checked by validate_sheet, no API spent). Marks live on the
guide's lines only, never in archive clips.

## How to change a pause (the only allowed procedure)

1. Add/adjust the slot default or a unit override in `rhythm.json`
   (with owner date + reason —違 no, never undated).
2. Run `tools/validate_sheet.py` (seconds).
3. Rebuild assemblies (`make_assembly.py` + `build_seed.py`).
4. Re-render ONLY the touched sections (`render_newA.py seed s1 ...`).
5. Reassemble + mix proof + ears on the delta.

Never: magic numbers in builders, hand-edited assemblies, digital-zero
pauses at archive transitions.
