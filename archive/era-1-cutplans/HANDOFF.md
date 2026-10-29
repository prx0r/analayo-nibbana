# SUPERSEDED — see HANDOVER.md (2026-10-25)

This was the era-1 cutplan handoff. All 33 cutplans are done and
pushing works now (its 'push impossible' note is stale). Kept for
the cutplan method only.

# HANDOFF — Nibbāna lecture cut plans (for finishing agent)

## Task
Produce a cut plan per lecture for all 33 Analayo/Nyanananda "Nibbāna: The Mind Stilled"
lectures: condense each to 20–40 min (aim ~30, we've been landing ~39). A/B/C grades.
**Do NOT render audio. Cut plans only** (user approves before any render).

## Status (2026-10-24 update)
- **Done (29/33):** lectures 01–27, 29, 31 → `lecture-NN.cutplan.{json,md}`.
  01–09 manual (09 seam-audited); 10 manual + seam-fixed (Pali-fragment start
  trimmed, summary corrected); 11–27, 29, 31 via `tools/auto_keeps.py`
  (A=rank1 spine+technical, B=rank2 flow, C=rank3 boring, D=cut in MAJOR).
  All in 20–40 band (29 @20.9m floor, rest 30–39.9m).
- **In progress (4/33):** 28, 30, 32, 33 — no CF/YT in repo, YouTube blocked
  from this network (transcript API RequestBlocked, yt-dlp bot-check, MCP
  isError without proxy). Fallback: DharmaSeed mp3s
  (`ds-mp3/lec-{58747,58749,58751,58752}.mp3`) + local faster-whisper
  (`tools/local_transcribe.py`, running in bg, log `/tmp/localtr.log`).
  Then `auto_keeps.py` + `gen_plan.py` as usual.
- youtube-transcript MCP installed (`pip`, module `mcp_youtube_transcript`)
  and registered in `~/.config/opencode/opencode.jsonc`; needs
  Webshare/ScrapingAnt/HTTP proxy env to work from blocked networks.

## How the process works (proven — follow it)
1. Read transcript of lecture NN:
   - CF (DS-native, best): `/tmp/opencode/lecNN_cf.txt` (or regenerate: `tools/cf_whisper.py`).
   - YT fallback: `/tmp/opencode/lecNN_yt.txt` (compacted from `yt-subs/lecture-NN.json`).
   - If neither: run `/tmp/opencode/fetch_yt_subs.sh` (YT, cooldown/IP-block issues) or
     `tools/cf_queue.sh` (Cloudflare whisper, ~214 min/day free, log `/tmp/opencode/cf_queue.log`).
2. Read `CUTTING-FORMULA.md`. Core rules:
   - Keep band 1200–2400 s. Design r1 (rank 1) so r1-only ≤ 2400.
   - Cut: forum/preamble/logistics/bio, lec recap, restated translations (2nd translation
     of same verse/passage — Bodhi/Woodward/Norman/Ireland/etc.), Pali recitations before
     kept English (split keep-spans at big ≥10 s gaps so the Pali is cut), dry surveys,
     academic article/forum mentions, repetition (e.g. re-telling an earlier simile).
   - Seam rule: the block after a cut must read standalone — never start mid-sentence,
     no dangling "as mentioned above/this paragraph" unless the referent is KEPT.
     "End of comment"/"Comment" markers = instructor asides, cuttable for budget.
   - Grades are auto-emitted from ranks: 1→A, 2→B, 3/4/5→C. Rank 2/3 = expendable;
     generator drops rank>1 largest-first until ≤2400, so r3 = always cut, r2 = keep
     only if room (small r2 survives, large r2 dropped first).
3. Write keep file `/tmp/opencode/lecNN_keeps.py`:
   ```python
   KEEPS = [(start, end, rank), ...]   # seconds, DS/CF timebase (or YT if no CF)
   MAJOR  = [(a, b, "kind", "reason"), ...]  # labels for big cut spans (±1.5s match)
   SUMMARY = "one-line what survives"
   ```
4. Run: `python3 /tmp/opencode/gen_plan.py NN /tmp/opencode/lecNN_keeps.py`
   - Asserts kept ≤2400; auto-drops r>1; writes `lecture-NN.cutplan.{json,md}`.
   - ffprobe duration when CF transcript exists, else YT cues.
5. Audit: read `cuts`/`dropped_spans` in the JSON; verify every seam (block after cut
   reads standalone) and that no r1 span begins/ends mid-sentence (use segment boundary
   numbers from the transcript). Iterate.
6. `git add -A && git commit` (repo lives in this directory; push impossible — GitHub
   token invalid, `gh auth login` needed).

## Timebases
- CF transcript present → native seconds = mp3 seconds (use directly). CF exists for
  01,02,04,05,08,09,10,11,12,13,15,16,18,19,21,23,25,29,31 (`lecture-NN.transcript.cf.json`).
- YT-only lectures (no CF): 03,06,07,14,17,20,22,24,26,27 (+28,30,32,33 pending) — keeps
  are in YT-cue seconds; `timebase.yt` recorded in plan; convert anchors at render time.
- Check before each lecture: `ls lecture-NN.transcript.cf.json yt-subs/lecture-NN.json`.

## Subagent warning
Task-tool subagents returned EMPTY results 3× (wrote no files). Work solo: read →
design → write keeps → generate → audit. Autosave everything to disk.

## Per-lecture notes
- lec01: v2 restores sankara + exam content (gen_plan01.py built-in keeps).
- lec08: grades A=41/B=0/C=0 accepted — B=0 is OK when content is dense.
- lec09: CF fully read.90.6 min source (5437 s) — the densest; expect ~2390 s kept,
  almost all rank-1. Structure: [forum preamble 0–607.8 CUT] motto → Satipatthana
  postures/pantomime → hands/feet relativity → seven suns + impermanence→voidness →
  Dhammapada verses → King Moolaka catechism (Pali answers cut, EN kept) → chanda/
  Unnabha iddhipada → gem-in-rubbish-heap analysis → Brahmachala 62 views → Samiddhi
  parallel catechism → Ummaggajataka parable → via-media/shadow conclusion.
  Second translations to cut: Vicakkarani/Bodhi/Woodward/Norman/Empiccobody/McIver/
  Ireland/Walsh blocks. Big Pali gaps to split at: 865.8–886.6, 908.4–929.2,
  1276.9–1297.7, 1374.6–1386.4, 1438.8–1450.2, 1566.7–1584.5 (keep span must cover
  1552–1557.4: EN question is fragmentary there), 1705.3–1727.9, 1767.8–1794.4,
  2394.8–2418.0, 3089.8–3099.5, 3131.3–3150.2, 3468.4–3483.7, 3735.6–3792.9,
  4089.1–4104.6, 4243.7–4259.0, 4617.9–4664.6, 4933.3–4952.1, 5363.3–5376.1.
- Long analysis spans worth keeping rank-1: 3150.2–3373.3 (gem analysis; trim tail
  3344.5–3373.3), 5199.4–5363.3 (conclusion), 2215.6–2394.8 (chanda chapter).

## Render (FUTURE — after user approval only)
ffmpeg concat of keep segments per `kept_segments[]`; DS mp3s are the source.

## SERIES EDITS — three tiers from one cut (2026-10-24 plan)

Totals (30/33 cut; 32+33 pending transcription): source ~46.2h, full-series kept ~21.5h,
A-only total ~6.3h (post-standardisation 2026-10-24), B-only ~14.4h. All A/B/C standardised: A=gold spine, B=relevant flow, C=boring (cut first).

### Layer 0 — FULL series (~21.5h): everything as cut
All 33 lecture cutplans, in sermon order. The archive / deep-study layer. No extra work.

### Layer 1 — CONCISE 8h (~480 min): 8 full episodes + 14 A-only episodes
Tier-1 FULL (8 eps, ~300m): 01 (32.6, foundations), 04 (39.7, Kaccayana hinge),
09 (39.9, densest philosophy), 11 (38.6, Bahiya/flame), 13 (29.8, Mulapariyaya),
21 (39.8, Vaccha/Anuradha/Radha), 31 (39.1, raft/endeavors close).
Tier-2 A-ONLY (~196m): 12 (9.7), 14 (7.0), 15 (11.8), 16 (12.2), 17 (6.1), 18 (11.3),
19 (9.6), 20 (8.8), 23 (14.0), 24 (8.9), 25 (14.8), 26 (13.1), 28 (9.6),
29 (13.2), 30 (13.6), 32 (14.6), 33 (5.7). Sum Tier-1 (~269m) + Tier-2 (~196m) ≈ 465m ≈ 7.7h.
Omitted from concise: 02, 03, 05, 06, 07, 08, 10 (manual-era A too broad for filtering; full versions live in Layer 0).
Build method: NO re-cutting. Concise = filter existing kept_segments by grade
(full keeps for Tier-1, grade-A only for Tier-2) + per-episode md generated from
a selector script (to write: ~30 min, same schema + tier field).
Grading standard (applied all 33, 2026-10-24): A = load-bearing spine (gold: motto,
signature similes, payoff lines/verses, definitional cores — must survive);
B = relevant flow (droppable largest-first if over budget); C = boring
(drop first); D = cut outright (forum/recap/Pali/2nd-translations/closers).
Manual-era A-inflation fixed (02–10 re-graded; lec09/10 keep dense-episode
exceptions: big load-bearing chapters stay A by design, Tier-1 full anyway).

### Layer 2 — MINI 2h (120 min): 6 chapters x 20 min, thematic, own arc
1. "The Fire Goes Out" — what Nibbana is: lec01 fire/lamp arc + lec21 Vaccha.
2. "Name and Form" — the mirror/image core: lec01 + lec10 rope/mirror/contact.
3. "The Middle Way" — Kaccayana (lec04) + bhava/vibhava extremes (lec09).
4. "Bahiya" — in the seen only the seen + flame verse + Papancha (lec11).
5. "The Worldling's Mistake" — Mulapariyaya (lec13) + honey-ball (lec12).
6. "No Footing" — non-manifestative (lec07/08) + Anuradha/Radha (lec21) + similes (lec25).
Build method: NEW editorial pass — 6 chapter keeps files selecting A-gold spans
(killer lines, signature similes, payoffs) across 1–3 lectures each, with motto
spans as chapter cold-opens. Requires a cross-lecture plan generator
(mini_gen.py: list of (lec,start,end) → concat plan, ~30 min to write).
Render maps each span via its lecture's timebase (ds native or yt anchors).
Effort: ~2–3h curation. No new recording; all spans already exist.

### Tier list (grand-scheme importance)
T1 load-bearing: 01, 04, 09, 11, 13, 21, 31 (+10 as alternate).
T2 major: 02, 03, 05, 06, 07, 08, 12, 18, 20, 25, 30.
T3 supporting: 14, 15, 16, 17, 19, 22, 23, 24, 26, 27, 28, 29 (+32/33 provisional).

## CONDENSED BUILD (2026-10-24 — text pipeline DONE; current entry points below)
TEXT IS COMPLETE AND GATED: 71 beats, 6 sections, all amendments +
A-pass applied (sourced quotes only). Read in this order:
`process/README.md` (method) → `REVIEW.md` (full lookover + queue
status) → `CONDENSED-BUILD-NOTES.md` §25–26 (fix logs) →
`process/MISTAKES.md` (lessons M1–M7 + M-A1–A7). `bash process/verify.sh`
must pass (G1/G5-semantic/G6/G6b-canary). REMAINING: human intros
(build/human-scripts.md, ~4min), ear listen pass, ffmpeg render.
Builder/repair entry points: `process/scripts/{rebuild_text,make_assembly,
g5_provenance,g6_tts_check}.py` — all target build/ directly.

### OLD STATUS BLOCK (kept for history)
## CONDENSED BUILD (2026-10-24, in progress — see CONDENSED-BUILD-NOTES.md)
Same 33 cutplans reorganized into 6 argument-order segments (§1 What … §6 Remains), 3 versions each: V1 pool 20.7h / V2 gold 6.3h / V3 core ~111m (82 clips + Nanananda pads from 53-nibbana-scaffold excavations). Manifests + ordered JSON in /tmp/opencode/condensed/. Render proven: §1 core 11/14 → 10.2m mp3. Blocked: 10 DS mp3s to fetch (03,06,07,14,17,20,22,24,26,27). QA flags: f1 S3 376s clip split at render, f2 S5 heavy closer, f3 S4 thin 8.8m by design, f4 S2 8m L10 weight.
