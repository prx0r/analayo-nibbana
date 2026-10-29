# EAR LEDGER — finding → evidence → change → measured after

## Round 3 (2026-10-26/27, fresh post-U4 render, 14-chunk omni audit)

| # | finding | evidence | change | after |
|---|---|---|---|---|
| 1 | 8/14 omni calls refuse ("text, not audio") while quoting content | ear_round3.json (s2×3, s3/2, s4, s5×2, s6/1); s4 retried ×3 incl. fresh upload + short re-cut, deterministic; upload re-download byte-perfect 5835308B | none to build (instrument failure, not a defect); round-3b queued with variant host/model/chunking | 6/14 descriptives clean, zero defects; mechanical (mix PASS, whisper, probes, assert_audible) covers the 8 |
| 2 | mid-sentence flags at chunk 00:00 (s1/1, s3/1) | chunk boundaries start mid-beat by construction (≤12min +30s overlap) | discard per taxonomy (refuted by construction, not by verbatim) | no action on build |
| 3 | Fish heard as "female voice sings" (s3/0) | descriptive quote, no defect claimed | voice-perception → owner taste lock (Fish approval pending) | no action until owner listens |

## Round 2 (2026-10-26, room bridges + linear mastering)

| # | finding | evidence | change | after |
|---|---|---|---|---|
| 1 | floor-cliff joints (S1 00:58 class: voice switch lands on digital zero) | omni joint notes R1; vatulanatha ledger #4 (same class) | beds = room bridges (prev-room + next-room halves, 80ms crossfade; same-source = own room; Fish side = digital floor) | bridges -47…-65dB max, continuous air; p0 beds 160/160 present |
| 2 | master pass pumped beds ~20dB (S5 1005.9 bed fragmented to 1.39s) | wav-vs-mp3 bed comparison (4.53s → fragments) | dual-pass loudnorm (measure, then LINEAR gain; `-v error` hides the JSON — pass 1 runs loud) | beds intact in mp3; section means -16.4…-17.4, peaks ≤-1.8 |
| 3 | room-hiss normalized to -6.9dB peak (first bridge attempt) | volumedetect on room sample | rooms keep NATURAL level (no loudnorm on beds): lecture air ≈-65dB, sermon floor ≈-90dB | beds read as stillness, sit ~30-45dB under speech |

## Round 1 (2026-10-26)

| # | finding | evidence | change | after |
|---|---|---|---|---|
| 1 | essay-0 answer slammed into beat-2 verbatim, zero pause | omni S1 00:58 joint | 2.5s post-essay-0 stillness in make_assembly (all sections) | rendered in; present from this build forward |

## Standing policy (from vatulanatha, adapted)

Taste → policy row once, never re-litigated. Transcript-level → discard
(G5). Unstable → discard when refuted by verbatim. Mechanical → block.

## Bridge perceptual check: INCONCLUSIVE (2026-10-26)

Model (fresh S1, bridges in): "no pauses between clips... single
uninterrupted flow" — then, asked to list pauses: "NONE", duration
"1000.0s" (actual 816s). p0_mix_check on the same file: 23/23 beds
present at position. Ruling per taxonomy: model perception of beds =
UNSTABLE, refuted by engine → discard. Beds proven present; whether
room-joins *feel* continuous vs cliffy stays human-only until the model
passes a pause-counting canary. Lesson: agreeableness wears many
costumes — "perfectly seamless" is the same disease as "all CLEAN".

## Round newA (2026-10-28, fresh seed+A render, two Fish voices + 30s gap + TAIL)

14 chunks, qwen3-omni-flash descriptive prompts, `build/ears/ear_round_newA.json`.
Adjudicated finding-by-finding (whisper/CF-transcript/volumedetect decide):

| # | finding | evidence | change | after |
|---|---|---|---|---|
| 1 | s2/0 "voice ends 00:14, silence 15-20s, end of recording" | volumedetect 20-92s: mean -17.7dB (speech); s2/1 continues same content | none (model truncation) | UNSTABLE → discard |
| 2 | s1/1 "In the Sutta cuts off mid-sentence" 00:40-43.8 | energy -15.9dB 90-106s; itemization stops at token cap, chunk is 106s | none (token truncation) | discard; coverage via manifest |
| 3 | s6/1 "far-shore ends mid-sentence" | L5 transcript 1753-1764 complete + "End of comment" 1765 | none | transcript wins → discard |
| 4 | s6/0+s6/1 "Pali garble voices" (nijjana/tangahang) | whisper s6 file14-26s: clean English "These preparations are comparable..."; breath-boundary room tone | none | hallucination → discard |
| 5 | s5/1 "stainless tool" vs signless | L29 CF 981-986: "Develop the signless too[l]" | none (audio correct) | transcript wins → discard |
| 6 | s6/1 "resumes mid-sentence" (b11 ~174-176) | YT cues: transition to "conclusive declaration" (discourse phase change); YT can't arbitrate seams | none; YT-only caveat stands | ear-check noted, not blocking |
| 7 | chunk-2/3 "mid-sentence" at 00:00 (s1/1, s2/1, s2/2, s3/1, s5/1, s6/1) | chunks start mid-beat by construction (30s overlap) | none | discard per taxonomy |
| 8 | s3/1 flags mid-honey-read (file 67.7/96.8/116.6) | all inside continuous L12[1299-1431] honey span (G5-anchored, continuous by construction) | none | expected-text refutes → discard |
| 9 | voice counting ("one voice" vs "3rd/4th voice") | model inconsistent across chunks | none | unstable → discard; blend = owner ear (approved 2026-10-28) |
| 10 | "no pause/breath" (s2/0) | design: room bridges = continuous air, never digital zero | none | working as designed |

Blocking findings: **0**. Voices distinct (student Q / elderly plain / Analayo), no clicks/glitches/volume jumps/robotics anywhere, bell clean, breaths before every Analayo.

## Round newA-2 (2026-10-28, repeat, `build/ears/ear_round_newA2.json`)

Same 14 chunks, same model/prompts. Raw findings reproduce round-1 item-for-item
(same truncation points, same garbles, same boundary flags); adjudication identical.
Blocking findings: **0**. Two consecutive clean rounds: **MET**.

## Mix proof newA (2026-10-28, `/tmp/newA_mix_check.py` = p0_mix_check retargeted at audio_newA)

order==assembly, beds 82/82 present (seed 13, s1 11, s2 10, s3 9, s4 13, s5 9, s6 17),
edges audible every slice, levels mean -16.9…-17.6dB peak -1.8…-1.9dB: **PASS**.
TODO: wire AUDIO_DIR into p0_mix_check.py properly instead of the /tmp copy.

## STAMP — rung 0 + rung A DONE (2026-10-28)

Text gates (verify.sh ALL PASS) + mix proof PASS + two consecutive clean ear rounds +
this ledger. Remaining DONE-external: owner ear (taste), B audio re-render, C decision.
Q1 B-territory carry-overs (NOT in 0/A scope): b9 open dangle ("a certain analogy",
L19 390), b10 lowercase open (L19 718) — queued for the B ear round.
