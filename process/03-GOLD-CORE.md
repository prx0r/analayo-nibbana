# 03 — GOLD + CORE. Spines, then killers.

## Gold (A-only, cluster order)
- Filter each pool to grade-A spans, keep cluster order. Result: the
  deep dive (~6.3h here: S1 112m … S4 22m …). Uneven is honest — dense
  doctrines (fire) sprawl, concentrated ones (observer) don't.
- Apply the motto-cap here (files keep full data; manifests enforce it).
- Gold joins audit: sample cross-lecture joins, verify standalone reads.

## Core (one killer per cluster, ~2h total here: 73 clips, 96m Analayo)
- Per cluster, top 1–2 by duration (dense exegesis earns length), drop
  <10s slivers, motto first as cold open, end on the payoff clip.
- Then READ THE CORE AS A SCRIPT (the textual flow audit). Fix list
  classes, all found here, all fixed and logged:
  - empty fragments ("The Buddha says," ×2), spliced 5s clips → drop
  - dangling opens ("so of those…", "And I will be using…") → extend
    head to sentence start or drop
  - sermon boilerplate inside clips (permission formulas, "19th sermon",
    thank-yous, recap callbacks) → split clip or trim
  - wrong-order pairs (commentary-before-verse) → swap
  - closers that trail off (word-study tails, garbled YT ends) → replace
    with pad-close + silence
  - oversized single clips (376s exegesis) → breath split at render
  - missing signature content (honey-ball never in keeps as "honey" —
    lives under "Madhupindika") → B-promotion with note
- Re-audit after fixes. Cores version (v1→v4 here); manifests pin versions.

## Outputs
`segN_gold.json`, `segN_core_vN.json` + `manifest_sN_{pool,gold,core}.txt`
(ffmpeg-ready clip lists). Fail the stage if any core clip opens
mid-sentence or any beat lacks a closing thought.
