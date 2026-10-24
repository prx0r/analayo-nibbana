# CUTTING FORMULA — Nibbāna: The Mind Stilled (33 episodes)

**Target: 20–40 minutes, flexible — aim ~30, take 20 when a lecture is pure
fat and 40 when the sermon itself is the gem.** Source lectures run 60–93 min;
judge each on sharpness, not percentage. Every lecture is cut to this budget independently —
sharp is the default, the budget is the law, no lecture "decides" to be 80 min.

## Keep-rank (fill the budget from the top; stop when full)

1. **Frame (≤90s):** welcome + what this sermon is + the motto/theme told ONCE.
2. **Sermon spine (the bulk):** the passages carrying Sermon N's own argument —
   its definitional core, its central similes, its payoff lines, its own closing.
   If the sermon surveys five supporting texts to make one point, keep the first
   and the payoff; the pile-on citations go.
3. **Unlock comments (≤6–8 min total):** only Analayo's comments where a term
   genuinely can't be followed without it — one alternative translation or
   definition per concept. Second opinions, comparative parallels, background
   essays: out.
4. **Close:** the sermon's own closing + (optional) a single summarizing line.

## Always cut (the fat)

- forum/course logistics, announcements, housekeeping, plugs
- biography (his, Bhikkhu Bodhi's, the tape history)
- long history/scholarly detours (precept-vs-realization debates, Sangiti
  history, article references) — unless the passage IS the sermon's point
- item-by-item list recitations (catechisms, numbered rundowns)
- every telling after the first of: motto, origin story, course purpose
- extended comparative material (Chinese parallels, Upanishad parallels) when
  the Pali point is already made
- second+ citations supporting an already-established point
- end plugs ("comments on the forum", next week logistics)

## Method

- Read the full transcript. Map spans to **ranks**. Cut whole spans at segment
  boundaries — never mid-sentence.
- Chant rule: a silence gap next to "verse intro → (gap) → English rendering"
  is a **Pali recitation — keep the gap**, find the mass elsewhere. If truly
  stuck at budget, prefer cutting a duplicated English re-reading over chant.
- **Timebase:** plan records YouTube-cue times + anchors
  (`yt_first`, `yt_last`, `ds_first`, `ds_last`). Renderer maps
  `t_ds = ds_first + (t_yt - yt_first) × (ds_last-ds_first)/(yt_last-yt_first)`
  then snaps every boundary to the nearest pause in the DharmaSeed audio.
- Output per lecture: `lecture-NN.cutplan.json` (schema below) + `.md` human view.
  **No rendering until the owner approves.**

## Plan schema

```json
{"lecture": N, "target_min": 30, "source_min": X, "kept_sec": Y,
 "timebase": {"yt_first": s, "yt_last": s, "ds_first": s, "ds_last": s},
 "cuts": [{"start": yt_s, "end": yt_s, "kind": "...", "reason": "<short>"}],
 "keep_summary": "what the episode now covers"}
```
`cuts` in YT time, sorted, non-overlapping. kept_sec must land in 1200–2400. Each keep-span carries a rank (1=spine
… 5=optional); when over 2400 the generator drops highest-rank/largest spans
first (never a rank-1) until in band.

## Grades (the depth dial) — required on every plan from lecture 03 on

Every KEPT span carries a grade, stored as `kept_segments[]` in cutplan.json:
- **A = gold** — killer lines, signature similes, payoffs (the highlight reel)
- **B = flow** — doctrinal glue, translations, secondary reads that make A land
- **C = technical** — philology/history kept for depth only

Render modes: **A-only** (~19–20 min/lecture) → **A+B** (the sharp episode,
default target) → **A+B+C** (full plan). Selector lives in the render step.
Lec01: A=18.8m B=13.4m C=0.7m · Lec02: A=20.0m B=19.0m C=1.4m — segmentation
is trivial once keeps exist; grade belongs to the keep-list entry, never the cuts.
