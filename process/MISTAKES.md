# MISTAKES — everything we got wrong, with cause + fix. Read before touching the pipeline.

## Slop (writing things that aren't his)
- **M1. Hand-written S1 beats.** Six beat quotes typed from memory instead
  of extracted. One ("Itself a meditation subject") was excavator prose,
  not his words — caught by the user, not by audit (it matched a
  transcript of Analayo *explaining*, which our sources wrongly
  included). Fix: deleted, rebuilt mechanically; sources restricted to
  excavation quotations ONLY. Rule born: verbatim = extracted + offsets.
- **M2. Fish narration ("he's about to say…", 82 composed cues).**
  Caught by user ("never write", "your slop"). Fix: deleted to slop/;
  Fish = term-key drops + plain-English lines derived by key ONLY.
- **M3. Mid-quote splits orphaning Pali leads.** Regex split
  `"What is burning?"` from its continuation, `"Khayamatta na nibbanam"`
  from its sentence. Fix: reattach + contiguity-verify each.
- **M4. Honey concatenation.** Four excerpts joined with [...] presented
  as one quote. Fix: excerpt LISTS, each verified separately.

## Audit/check bugs (ours, not the data's)
- **M5. One-sided normalization ×3.** Stripped markdown/quotes on the
  verbatim side but not the source side (and once reversed). Fix:
  identical normalization both sides, always; verify.sh encodes the
  correct version.
- **M6. Metric worship.** Shared-vocabulary counts flagged 47 beats;
  reading showed most were fine (mottos are stopwords; Pali vs English
  never overlaps). Fix: metric flags CANDIDATES, human reading verdicts.
  (Still caught 4 real misassignments — keep the metric, demote it.)
- **M7. YT timebase scans skipped.** CF-only code silently unscored 10
  units' spans (banana, Kaccayana, mirror, Bahiya all "missing").
  Fix: YT-cue pseudo-sentences + ascii aliases (baya, kachayana).
- **M8. Float timestamp keys.** Core spans keyed by rounded ints;
  `round(363.5)=364` broke dict lookups. Fix: tolerance matching (±3s).

## Content misses (real, fixed by design)
- **M9. S1 core opened on pileup.** 8 stacked mottos in gold; permission
  formulas + sermon numbers inside core clips; thank-yous mid-flow.
  Fix: motto-cap rule, head/tail trims, closer swaps (see notes §10-13).
- **M10. Signature content under other names.** Honey-ball lives under
  "Madhupindika"; anidassana under "non-manifestative". Fix: search
  concepts, alias table, B-promotion with note.
- **M11. Thin sections.** §4 (observer) nearly all in a few spans; no
  clean closer existed in Analayo's voice → close on Nanananda pad +
  silence (a feature: ends on him, not the explainer).

## Process scars (structural)
- **M12. /tmp as build home.** Weeks of artifacts in /tmp (volatile).
  Fix: `build/` in repo is the live copy; /tmp is scratch. Copied late —
  don't repeat.
- **M13. Stale-file confusion.** Multiple generations (v2/v3/v4, hand
  vs mechanical) coexisted; fixes applied to files then overwritten by
  rebuilds from older ones. Fix: single live set + manifests pinning
  versions + verify.sh before every commit.
