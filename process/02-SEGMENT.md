# 02 — SEGMENT. Every span gets exactly one home, in journey order.

## Assign (keyword scorer + primary fallback)
- Per section, a keyword list drawn from its similes and doctrines
  (here: §1 fire/lamp/ocean/vaccha…, §2 whirlpool/ruler/kaccayana…).
- Score each kept span's transcript text; highest score wins; ties →
  the lecture's primary section; zero scores → primary section.
- Transcripts must be YT-inclusive (CF-only scans silently orphan 10/33
  units' worth of spans — see MISTAKES.md § missed-content). Apply the
  aliases table first (kachayana→kaccayana, baya→bahiya…).
- Invariant: per-section totals sum to the full kept total (here 20.70h).
  Check it or the assignment leaked.

## Cluster (group by simile, not by lecture)
- Within each section, order spans by CLUSTER (theme group), then
  (lecture, start). Cluster order = the section's journey
  (e.g. §1: motto → fire → refute → synonym → here-now → remains).
- Lectures will scatter across clusters — that is the point. Same-simile
  spans sit together regardless of origin lecture.
- Known thin spots are structural, not failures (§4 observer material is
  concentrated; keep it tight, don't pad to quotas — Axiom 11).

## Continuity rules (no jumps)
- Same voice/mic throughout ⇒ cross-lecture joins need only 1.5s breath
  inside beats, 2.5s water between groups, motto cold-open per group.
- Motto-cap: 1 motto per core (cold open), max 3 spaced in gold
  (open/middle/close). Never stacked — every lecture opens with the
  verse, so unfiltered golds stack 8+ mottos (found in audit: §1).
- B-grade definitional readings may anchor a core beat ONLY with a
  written note (here: 2 cases — anidassana gist, honey-ball exposition).

## Outputs
`build/canon/segN_pool.json` (all spans, cluster-ordered; 1147 spans ~20.8h total), per-section cluster
ledgers with span counts + minutes. Fail the stage if totals don't
reconcile or any cluster is empty without a written reason.
