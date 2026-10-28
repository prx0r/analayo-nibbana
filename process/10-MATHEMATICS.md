# 10 — THE MATHEMATICS. Measured structure, not imposed design.

Every number below is computed from the build artifacts (commands at the
end to reproduce). Nothing here was chosen for beauty; the beauty is that
it came out this way anyway.

## 6 chambers
The 33-lecture series collapses into 6 argument-ordered segments (§1 What
it is … §6 What remains). Not selected — the scaffold's keyword clustering
converged there independently of the Analayo cut plans, and the Analayo
gold independently lands in the same six buckets. Two dissections, one
elephant.

## 83 beats (canonical: 71 of 2026-10-27 + 12 hunt-found §75 — assemblies play 77 + 6 essay-0 pointers)
Core beats per section: 11, 13, 15, 5, 14, 13 = **71**.
§4's 5 is the honest thin one (concentrated doctrine — anidassana,
tetralemma, no-footing). No padding was added to round it out; the
asymmetry is structural. Total Analayo runtime in core: 90.5 min.
The essay-0 host beat of each section is consumed by the opening
(pointer replaces it), so the heard A is 77 beats + 8 pointers (S2 triple).

## The ratio canon (owner 2026-10-28): rungs are RATIOS, not minutes

The ladder is defined by nesting (0⊂A⊂B⊂C⊂D, proven per section) and
by step ratio ≈ **2–2.5× per rung** after the seed jump (~11×). Minutes
are today's measurements, not targets — the next text keeps the ratios
with different minutes.

| rung | today | step from previous |
|---|---|---|
| 0 seed | ~2m | — (the root) |
| A newA | ~22m | ~11× (root statement → first expansion) |
| B | ~54m | ~2.5× |
| C | ~121m | ~2.2× |
| D | ~261m | ~2.2× |
| archive | ~20.7h reference | — (not a rung: provenance home, swap source) |

Seed → archive total compression ≈ **500×** (2m → 20.7h). The grading
rule was never tuned to hit a ratio — ~2–2.5×/rung is the material's
own density constant. Self-similarity across scales: the cluster order
is IDENTICAL at pool, gold, and core (same sort key),
so each layer is the same walk at a different resolution. That is the
fractal property, and it is structural, not decorative.

## 520 events, 2 bells
Assembly manifests (`build/assembly_sN.json` + seed) hold **520 events**
(recomputed 2026-10-28: +12 hunt beats, +6 plains, U2 triple pointer,
+8 voice-change breaths):
101 fish lines (12 questions + 77 beat plains +
12 plain responses), 89 verbatims
(77 beats + 6 essay-0 on-screen texts + 6 seed essay-0 texts), 93 Analayo clips (77 beats + 8
pointers + 8 seed units), 88 waters, 87 breaths, 17 pauses, 23 fish-terms, 8
motto-bells, 6 zoom-bells, 6 human-intro slots (empty by design), 1
seed-reprise, 1 terminal silence.
- **Motto bell** (bright, 2.5 s decay): section opens (seed + S1–S6)
  plus the S6 close (8 total). In the p0 draft the bells are SKIPPED at
  render (timing/voice check); they return in p1 with the sfx kit.
- **Zoom bell** (low + sub octave, 6.0 s decay): 6 thresholds (seed +
  S1–S5 closes; S6 closes seed-reprise + motto-bell + 30s silence).
  Bell ratio 6.0/2.5 = **2.4** — the zoom is the motto stretched in time,
  the same relationship as gold to core.
- **Pauses**: 1.5 s breath (inside beats), 2.5 s water (between beats),
  30 s terminal silence. Water/breath = 5/3 ≈ 1.667 (near φ — admitted
  coincidence, kept because it breathes right, not for the number).
  30 s = 20 breaths: the close is scored in the same unit as everything.

## 1 word
20.75 h → 6.9 h → 1.5 h → 2 min (seed) → 1 sentence (the motto) → 1 word:
**stilling.** Each layer answers the question the previous layer poses;
the compression is lossless in meaning, lossy only in elaboration.

## Invariants (what makes it mathematics, not layout)
1. Same order at every scale (cluster sort key shared pool→gold→core).
2. Every span in exactly one segment (totals reconcile: 20.75 h).
3. Every beat is the same 5-tuple (*motto-bell?*, fish, breath,
   analayo, water) — 71 repetitions of one rhythmic cell.
4. No two bells within 30 s of each other. No motto stacking in gold.
5. Provenance closes over everything (78/78 verified excerpts).

## Falsifiability
Re-grade with different thresholds and recompute: if pool/gold or
gold/core leaves the 3–4.5 band, the "natural density" claim dies and
this document gets rewritten. The verify script (`process/verify.sh`)
checks totals, provenance, and TTS hygiene; add the ratio bounds there
if you want them enforced.

## Reproduce
```bash
python3 - <<'EOF'
import json
for s in range(1,7):
  p=lambda n: 'build/seg%d_%s.json'%(s,n)
  P=json.load(open(p('pool'))); G=json.load(open(p('gold'))); C=json.load(open(p('core_v4')))
  print(s, 'pool %.2fh/%d'%(sum(x['dur'] for x in P)/3600,len(P)),
        'gold %.2fh/%d'%(sum(x['dur'] for x in G)/3600,len(G)),
        'core %.2fm/%d'%(sum(x['dur'] for x in C)/60,len(C)))
EOF
```
