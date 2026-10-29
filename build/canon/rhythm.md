# RHYTHM — the silence engine (2026-10-28)

Words end; meaning lands in the pause after them. Every silence in the
build is a NAMED SLOT with a default duration. Defaults hold unless a unit
carries an owner-dated override with a reason. No magic numbers in builders.

## How it works

1. `make_assembly.py` reads this file. Every pause/breath/water event takes
   its duration from `slots` unless `overrides[str(section)][slot]` exists.
2. The assembly timeline IS the sheet: `render_a_essay.py` asserts
   sheet==master every render (no silent drift).
3. Silence is room air (bridges from neighboring lecture rooms, ~30dB under
   speech), never digital zero — 5s of pause = 5s of the room the voice
   just left. (Vatulanatha rule; Qwen "no pause" readings confirm continuity.)
4. Phase 2 (not built): marks INSIDE long pauses — vatulanatha sfx kit
   (`build/assets/sfx/`: bowls/ding/long-break/blocks) for attention hits
   and emphasis. Slots marked `mark: null` take marks when wired.

## Slots (seconds)

| slot | default | where | mark |
|---|---|---|---|
| `motto_bell` | 2.5 | every section open | — |
| `recollect` | 3.0 | after Fish Q (listener answers first) | — |
| `plain_breath` | 1.5 | after Fish plain, before Analayo (voice-change air) | null |
| `triple_breath` | 1.5 | between essay-0 multi-window parts (same voice) | — |
| `essay0_stillness` | 2.5 | after pointer, before beats (the answer lands) | null |
| `beat_breath` | 1.5 | per beat, before Analayo | — |
| `beat_water_base` | 2.5 | per beat, after Analayo (+1s per 60s clip, cap 6) | null |
| `settle` | 6.0 | section boundary, after zoom-bell | — |
| `terminal` | 30 | S6 end: seed reprise + motto-bell + silence | — |

## Overrides (owner-dated, with reason — never silent)

| unit | slot | dur | why |
|---|---|---|---|
| U1 | `plain_breath` | 5.0 | owner 2026-10-28: the flame image (34w plain) must land before the 13s motto pointer; 1.5s clips it |
