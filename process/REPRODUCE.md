# REPRODUCE — exact rerun, top to bottom.

Prerequisites: repo + `/tmp/satsang-ext` (51/52/53 packs) + transcripts
(`lecture-*.transcript.cf.json`, `yt-subs/`) + 23 DS mp3s present
(10 missing = audio-only gap, text pipeline unaffected).

## Stage order (deterministic unless marked ✎ human)
1. Cutplans exist already (`lecture-*.cutplan.json`; regenerate via
   `tools/auto_keeps.py <NN>` then `tools/gen_plan.py <NN> <keeps>`,
   then seam-audit by hand ✎).
2. Assign spans → `segN_pool.json` (keyword scorer + primary fallback;
   reference: `process/scripts/rematch2.py` pool logic + cluster lists
   in `02-SEGMENT.md`). Assert totals == kept total.
3. Gold = filter grade A, cluster order. Apply motto-cap at manifest
   time (keep data intact).
4. Cores: top-2-per-cluster by duration, motto first, slivers <10s
   dropped — then apply the hand-fix list (CONDENSED-BUILD-NOTES §10-13:
   drops, swaps, trims, S4 rebuild, S6 reorder, motto head extensions).
   Hand fixes are DATA (recorded), not vibes; manifests pin v4.
5. Pads: match excavation quotes per clip (keyword overlap +
   same-sermon +3, uniqueness per section, targeted overrides listed
   in notes §22). Record {sermon} per beat; provenance is re-derived
   (never stored offsets — recompute + assert each run).
6. Below-lines: `fish_filter.PALI2EN` then `blunt_key.json`, then
   TTS transform (parentheses→dashes, English-first lead-drop,
   artifact cleanup). Deterministic — hash must match notes.
7. Run `process/verify.sh` — G1/G5/G6 + file presence. ALL PASS or stop.
8. Render (audio present): per-manifest `ffmpeg -ss/-to` cuts,
   concat with breath/water beds + bells, `loudnorm`, `afade 0.15s`.
9. QA listen (ears, unskippable): fixed cores + flags f1–f4.

## What is NOT reproducible (human by design, marked ✎)
Targeted pad overrides, flow-audit verdicts, hand-fix list, human
intros/bridges, bell choices, listen-pass signoff. Everything else is
scripted or it doesn't belong in the pipeline.
