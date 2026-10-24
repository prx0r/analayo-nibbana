# CONDENSED BUILD — process notes (2026-10-24)

Goal: 3 versions of the same thing from 33 Analayo lectures (20.7h kept) + 33 Nanananda sermons.
V1 Pool (archive, ~20.7h) → V2 Gold (A-only, ~6.3h) → V3 Core (~2h, self-contained movies).
Method: pool ordering/clustering first → gold plot arises → core as highest-signal rendering.
Order: argument order (§1-6 scaffold), NOT sermon order. Nanananda quote first, Analayo unlock after. No new writing.

## 1. Inventory (done)
1193 kept spans: 590 A (6.32h) + 602 B (14.38h). CF/DS-native: 23 lectures. YT-only: 10 (03,06,07,14,17,20,22,24,26,27) — anchor-mapped at render, snapped to pauses.
Timebase rule: DS seconds where CF exists; YT-cue seconds + anchor map otherwise. All boundaries sentence-snapped (seam rule: block after cut reads standalone).

## 2. Pool assignment (done, span-level)
Keyword scorer + lecture-primary fallback. Totals check: 20.69h (matches 20.70h).
§1 What 245 spans 3.72h (A 83m) · §2 Mechanism 256 spans 4.98h (A 69m) · §3 Keeps-running 238 spans 4.73h (A 77m) · §4 Builds 106 spans 1.56h (A 27m) · §5 See-through 217 spans 3.50h (A 77m) · §6 Remains 131 spans 2.20h (A 46m).

## 3. Pool clusters (done — counts below, order = journey, NOT lecture number)
Coherence rule: group by simile/theme, order groups as question→answer. Same voice/mic throughout; 1.5s breath inside beats, 2.5s water between groups, motto cold-open per group, bell per motif.

## 4. Audit log (gap check — v3 final, YT text + aliases + primary tie-break)
Assignment: keyword scorer, ties → lecture-primary section, zero-score → primary. Totals hold 20.70h.
- a1 banana/Kaccayana: RESOLVED — L03 banana → §2 ✓, kaccayana 4x → §2 ✓ (L04 + L22).
- a2 mirror/foam: RESOLVED — foam 3x → §4 ✓ (L06 YT + L25 — YT inclusion worked). Mirror: L10 → §2 (correct — rope/mirror does mechanism work there), 1x each §4/§6 passing mentions.
- a3 Bahiya: RESOLVED — baya→bahiya alias, 11x → §5 ✓.
- a4 anidassana/pixel: aliases, not misses (Analayo says "non-manifestative", "cinema/film show").
- a5 sandcastle: THIN (1 span, L22) — real: Analayo skims it. Nanananda excavation carries the weight; keep the 1 span in gold, bell it.
- a6 observer: 0 literal hits — phrased as "watcher/looker/who is resting" in audio; §4 signless/tetralemma clusters cover the function. Flag for core curation (pick the looker span by ear).
Pool files: /tmp/opencode/condensed/segN_pool.json (ordered by cluster → lec → start).

## 5. Gold plots (A-only, cluster order) — /tmp/opencode/condensed/segN_gold.json
§1 190 spans 112m · §2 62 spans 55m · §3 91 spans 64m · §4 54 spans 22m · §5 115 spans 85m · §6 78 spans 42m = 590 spans 380m (6.3h ✓).
Uneven is honest: fire is everywhere (§1 fat), observer is concentrated (§4 thin — keep tight, don't pad).
Continuity rules: cluster order = journey; within cluster lec→start; 1.5s breath inside beats, 2.5s water between groups, motto cold-open per group, bells F (§1) / R (§2 rope) / C (§3 Colombo) / D (§4 dog) / Z (§5 razor) / L (§6 lotus).
FIX c1 (found in continuity pass): §1 gold opens with 8 mottos stacked (L01,L09,L18,L21,L23,L26…) — every lecture opens with the verse so all matched ci=1. Rule: cap mottos at 1 (core: §1 opener L01 [696-749]) / 3 spaced (gold: open/middle/close). Same check queued for §2-6 (motto + "this is peaceful" openers).
Joins audit (§1 gold): 82/189 cross-lecture joins, sampled 3 — all read standalone ✓ (same voice/mic, sentence-snapped). Lec mix spans ~30 lectures for §1 — supporting lines from everywhere, fine; clusters keep them grouped by simile, not scattered.

## 6. Cores (~1.9h) — /tmp/opencode/condensed/segN_core.json (motto-capped, slivers dropped, top-2 per cluster)
§1 13 clips 16m (hand-plotted) · §2 14 clips 26.4m · §3 15 clips 23m · §4 9 clips 8.8m · §5 16 clips 23.2m · §6 15 clips 14.1m = 82 clips ≈ 111m.
Motto rule applied: first motto only per core (S4/S6 cores open on content — S4 opens mirror L07, S6 opens L08 cinema-link — accepted, mottos live in gold/pool).
FLAGS for QA listen: (f1) S3 L10 [974-1350] 376s unbroken bhuta/bhava — split with breath at render at sentence boundary. (f2) S5 closes on L10 [3401-3733] 332s — heavy closer, confirm or swap with raft L31. (f3) S4 8.8m thin — by design, add B-bridges only if it feels starved. (f4) S2 L10 rope 316s + L10 164s = 8m L10 — centerpiece, keep.
## 7. Manifests / audio / QA — pending (ffmpeg concat from segN_gold/core lists, DS-native cuts where CF, YT-anchor map + pause-snap otherwise, loudnorm -16 LUFS, afade 0.15s, bell -20dB, cough micro-cuts ±0.3s, seam audit)
(End of notes — updated as build proceeds.)
Nanananda pads: /tmp/opencode/condensed/seg1_pads.json (6 beats, sermon-file refs). Sandcastle rides beat 4 via pad — thin-in-Analayo motifs carried by excavation, as designed. §2-6 pads same method (excavation §-matching blocks).
FLAGS f1-f4 unchanged (QA listen).

## 8. Render proof (2026-10-24)
§1 core 11/14 clips cut + concat → s1_core_partial.mp3, 614s ≈ 10.2m ✓. 3 clips skipped: no DS audio yet (L17 5s, L20 11s+7s). mp3 -c copy concat throws benign non-monotonic-DTS warnings; final build re-encodes with acrossfade 0.15s + loudnorm, warnings go away.
AUDIO GAPS (10 lectures need DharmaSeed mp3 fetch before full render): L03,06,07,14,17,20,22,24,26,27. Core coverage with current audio: §1 11/14, §2 11/14, §3 11/15, §4 6/9, §5 14/16, §6 11/15 = 64/83 clips (77%).
## 9. 3-version runtimes (Analayo spine only; +Nanananda pads/pauses at assemble)
V1 pool 20.70h · V2 gold 6.3h (S1 112m S2 55m S3 64m S4 22m S5 85m S6 42m) · V3 core ≈111m incl §1 hand 16m (S2 26.4 S3 23 S4 8.8 S5 23.2 S6 14.1).
Deliverables: manifest_sN_{pool,gold,core}.txt + segN_{pool,gold,core,pads}.json in /tmp/opencode/condensed/ (move to repo at ship).
