# 01 — TRANSCRIBE + CUT. Sentences → kept spans → cutplans. (Era-1, FROZEN method: tools below are kept for provenance; live outputs live under sources/lectures/cutplans/.)

## Transcribe
- Cloudflare whisper queue (`tools/cf_whisper.py`, `cf_queue.sh`) or local
  faster-whisper (`tools/local_transcribe.py`) → per-unit
  `{source, duration, engine, sentences:[{t, end, text}]}`.
- YT fallback: compact `sources/lectures/yt-subs/lecture-NN.json` cues into ~800-char
  pseudo-sentences. Mark timebase: `native: ds | yt`. YT spans get
  anchor-mapped at render (`t_ds = ds_first + (t_yt-yt_first)*ratio`,
  then snap every boundary to the nearest pause).

## Auto-keeps draft (`tools/auto_keeps.py`)
Cuts, in order: (1) forum/course/recap before the motto/sermon start,
(2) second translations (regex `translat.*by` → nearest `End of` within
150s, else 4-sentence cap — mega-merge guard), (3) Pali gaps ≥8s,
(4) closer (last thank-you after 70% duration, else last 30s).
Keeps = complement, sentence-snapped. Rank: boring-keyword hit or
≥100s span → 3/2; conclusions protected (last 2 chunks never 3);
pre-intro forced 1. Writes `tools/lecNN_keeps.py`.

## Generate plan (`tools/gen_plan.py`)
`KEEPS=[(start,end,rank)]` → assert kept ≤2400s (40 min), auto-drop
rank>1 largest-first (never rank-1). Emits `sources/lectures/cutplans/lecture-NN.cutplan.{json,md}`
with `kept_segments[]` carrying grades (1→A, 2→B, else C), cuts ledger,
keep_summary. Target band 1200–2400s; the summary is the unit's logline.

## Seam audit (human read, required)
Read `cuts`/`dropped_spans` in every JSON. Every kept span must start at
a sentence start and read standalone after its preceding cut. Fix by
moving boundaries to sentence edges, never by rewriting. Manual-era
plans (01–09 here) get seam-fixes recorded in HANDOFF.

## Outputs
`sources/lectures/cutplans/lecture-NN.cutplan.{json,md}` × N. Totals ledger (era-1 counts: 20.7h kept,
590 A / 602 B spans — superseded by pool 1147 / gold 555). Fail the stage if: any kept >2400s, any mid-sentence
boundary, any unit without a keep_summary.
