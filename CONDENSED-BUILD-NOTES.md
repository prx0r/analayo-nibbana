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
## 10. Audio gaps — next step
10 DS mp3s missing (L03,06,07,14,17,20,22,24,26,27). dharmaseed.org reachable (200 OK) but no clean talk API; course-page lookup parked. YT-cue transcripts already in repo (yt-subs/) so cutting positions exist — only audio bytes missing. Cores render at 77% coverage meanwhile (64/83 clips).

## 10. Textual flow audit (2026-10-24, all 6 cores read as scripts)
Method: open/close 14 words per clip + dangle/Q flags. Verdict: 70% there; breaks are specific.
FIXES (apply at manifest build):
- S1: drop L21 [377-394] 17s ("The Buddha says," x2, empty fragment); drop L17 5s (spliced-sounding); drop L21 [567-618] (dangles + Isidatta tail drift); reorder end as oil-lamp(10)→iron(14)→devoid(13) so "that realization" has its antecedent. Extend L19 [356-522] head ~8s to motto start (currently opens mid-refrain — works as refrain-return, but clean the inhale). New S1 core: 11 clips ≈10m.
- S2: drop L30 [3382-3439] (off-theme, belongs §5); swap L10 [4064-4229] BEFORE L10 [4292-4455] (12 continues into 4 — same Kalaha verse, currently backwards); extend L04 ruler head ~10s (opens "And I will..."); trim L25 [3418-3510] tail ~15s (Pali-recitation transcript garbage); pad L03 motto head (opens mid-recap).
- S3: CUT L14 [729-745] opener (broken — forum text "bondage of Mara", mis-scored; move out of §3 gold); promote one L12 honey-ball A-span into core (signature simile currently missing — core has reckoning but not the honey); trim L24 [1030-1100] head (opens "[Music]") or swap with honey-ball; split L10 [974-1350] 376s with breath at render (f1 stays, execution noted).
- S4: REBUILD — 9 fragments, no anchor, Pali-chant opener (L29), two mid-sentence opens. Pull 2 anchors from gold: full Kevatta-verse reading + one observer span as opener/closer; demote 3 weakest fragments to gold-only. Nanananda pads carry (excavation §4 strong). Target 4-5 clips ≈10m, not 9.
- S5: trim L14 [4478-4561] tail ~8s (ends "Thank you very much" — closer contamination); CUT L30 [563-584] (2nd motto + "thirtieth sermon" tail breaks timelessness); move L09 [1003-1037] directly after L09 [1003→ rel. clip 9] ("emptiness of both" → "even attachment is..." flows); swap closer: raft L31 [611-673] LAST, demote L10 [3401-3733] 332s to gold (f2 executed).
- S6: reorder to motto → film-reel → lotus → seamstress → faculties/path → ocean/magic; close with NANANANDA pad (no Analayo clip ends clean — L32 tuleti ends mid-exposition); extend L27 motto head 5s to "This is peaceful"; trim L16 [935-1066]? (130s motto+contact — keep, it bridges).
- Global: "thank you for your attention" tails inside kept spans (S3c13, S5c3) → trim at render, flag trim_keeps for gold too.

## 11. Flow fixes applied (core v3, 2026-10-24)
segN_core_v3.json + manifest_sN_core_v3.txt. 73 clips, 96.1m Analayo (≈2h with pads/pauses).
- S1 11 clips 9.5m: dropped empty fragment + spliced 5s + drifting ocean-tail; end reordered oil-lamp→iron→devoid ("that realization" antecedent fixed); L19 head extended to motto.
- S2 13 clips 25.5m: dropped off-theme L30; Kalaha clips reordered lecture-order (12→4 was backwards); ruler head +10s; Pali-garbage tail trimmed.
- S3 15 clips 24.7m: cut broken L14 opener (forum text, moved out of §3); B-promoted L12 [1299-1431] Madhupindika/pamada-tavern (the simile lives there); honey "miss" resolved = vocabulary (Analayo says Madhupindika, never "honey" — 0 hits full transcript).
- S4 5 clips 4.9m: rebuilt around B-promoted L08 anidassana-gist anchor; 3 weakest fragments demoted; Pali-chant opener cut. Thin by nature — pads carry.
- S5 14 clips 17.2m: "thank you" tail trimmed; 2nd motto + sermon-number tail cut; attachment moved after emptiness (flows); raft LAST, L10 332s demoted to gold (f2 executed).
- S6 15 clips 14.2m: narrative reorder; motto head +5s; closes on NANANANDA pad (no Analayo clip ends clean).
- B-promotions (2, both noted in JSON): L12 Madhupindika, L08 anidassana-gist. Rule: core is A-only except where the definitional reading lives in B.
- Gold files unchanged (motto-cap + closer-trims are manifest-build rules — apply at render, files keep full data).

## 12. Pads full text (2026-10-24)
segN_pads_full.json for §2-6 (cluster → sermon-section bodies from excavations, capped): S2 13 sections/23k chars · S3 14/13k · S4 7/6.8k · S5 13/14k · S6 12/6.4k. §1 pads stay hand-curated (6 beats). Pad selection at assemble = 1-2 quotes per beat from these bodies (30-60s each).

## 13. Core v4 final (2026-10-24) — 72 clips, 96.3m Analayo (+pads/pauses ≈ 2h)
S1 12/12.1m · S2 13/25.5m · S3 15/24.7m · S4 5/4.8m · S5 14/17m · S6 13/12.3m.
Fixes from flow audit all applied; S6 head-revert verified (motto intact at 675); S1 split verified (refrain 348-359 + teaching 371-522, permission excised).
Audio coverage v4: S1 10/12 · S2 10/13 · S3 12/15 · S4 3/5 · S5 13/14 · S6 10/13 = 58/72 (81%).

## 14. Fish scripts (2026-10-24) — segN_fish.json (N=1..6), filter in fish_filter.py
Pali→English map (word-boundary safe; longest-first). Fish never speaks Pali: S1 motto Pali stripped to Human. Total Fish lines: 6+16+16+10+18+16 = 82 cues ≈ 25-30m speech.
Human recording scripts: SPEAKER-RULES.md list (≈10 min raw). Next: record Human → TTS Fish → assemble per handoff grammar.

## 15. Fish = key only (2026-10-24) — NO sentences, NO "he's about to say"
Slop scripts (segN_fish.json, 82 composed cues) DELETED to slop/. Replacement:
segN_terms.json — per core clip, Pali terms actually heard → mapped English
(first hearing per section only, max 2 drops/clip). 40 drops total across 72 clips.
Filter: fish_filter.py (ascii-spelling safe — transcripts write papancha/sankhara/upadana).
Rule: Fish speaks the mapped word/phrase and nothing else (e.g. hears "papancha" → says "spiralling").

## 16. Three-layer scripts final (2026-10-24) — segN_script.json
Per core clip: Analayo (lec,start,end) → Nanananda VERBATIM (excavation quote, untouched) → plain_english_below (key-derived: TERM (plain) first-use; slop-free). S1 12 (hand beats) · S2 13 · S3 16 (incl. Madhupindika honey-ball narrative, cross-sourced S11 — pads aren't section-bound) · S4 5 · S5 14 · S6 13 = 73 beats. Quotes unique per section (S3 15/16). S1c2 sample: "Upadana (grasping) = fuel AND grasping."
