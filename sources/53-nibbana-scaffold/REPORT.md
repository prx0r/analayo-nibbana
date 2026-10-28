# REPORT — 53-nibbana-scaffold (2026-10-20, extension pack)

The 33 sermons collapsed into the logical argument, reorganized for
clarity. Plus the full excavation of all 33 sermons: every useful
metaphor, explanation, argument, refutation and insight, organized into
the six-section scaffold — raw material for compression into the movie.

## Files

| file | what | status |
|---|---|---|
| nibbana-scaffold.md | 6-section argument scaffold (JSON in markdown), merge-passed 2026-10-21 (answer_p1 + depth links + completed sermons[]) | structured data |
| nibbana-10-passes.md | The six answers in ten additive depth passes over all 33 excavations | generated 2026-10-21 |
| sermon-01…33-excavation.md | Full per-sermon extraction, 11 sections each | 33/33 complete |
| HANDOVER.md | Continuation instructions (superseded: sermons complete) | archive |

## Excavation status: COMPLETE (33/33)

Each excavation follows `54-excavation-skill/SKILL.md` three passes:
full extraction → verification against source (fidelity audit) → hole
hunting. Every file validated `ALL PASS` by `check_pack.py`
(gates: schema, ids, refs, dialect, no-transcript, urls, license,
contact, redflag, rights).

### Fidelity audit method (per sermon)
Quoted lines were machine-checked against the source `.txt`
(` /tmp/opencode/nibbana/Nibbana-*.txt`) with a fuzzy matcher: each
quoted fragment must appear in the source or score ≥0.92 similarity.
Misses were fixed in-place and recorded under `PASS 2 FINDS`. The
final sermon (33) passed with **zero** low-similarity quotes.

### Defects repaired (2026-10-21)
- **sermon-01** was structurally incomplete (missing SECTION 5, SECTION 6,
  REFUTATIONS, EVIDENCE, VOICE, Pass 2-3). Repaired from
  `Nibbana-01-1.txt` under the three-pass method: the Pass-2 re-read found
  the Vacchagotta accusation + tetralemma framing, the commentarial āgamma
  formula, the six qualities of the Dhamma, the Dhamma-eye passage, the
  Upanishad cross-references, the Āṇisutta Pali verse, and the
  Manorathapūraṇī name all ABSENT from Pass 1 — added with source-verified
  quotes (54 quoted spans machine-checked against the source; all scored
  1.0 against a 0.92 threshold), plus the four missing buckets and both
  pass sections. Findings recorded in the file's own PASS 2 FINDS.
- **sermon-06** was missing SECTION 6 — reconstructed from
  `Nibbana-06.txt`: the state-of-Nibbāna passage (ignorance ceases → no
  unit → no inward pleasure or pain), the field/ground/base exposition,
  the Upatissa-and-Kolita flash, and the full winding-end sentence; all
  quotes machine-verified. Repair noted in its PASS 2 FINDS.
- Four files spelled SECTION 3 as "MECHANATION" (sermons 15, 16, 18, 21) —
  standardized to MECHANISM.

## Series arc (from excavations)

- **Sermons 1–27:** the "purgative" — clearing wrong views about the
  goal (extinction, not annihilation; the tetralemma dissolved; the
  commentators refuted).
- **Sermon 27 pivot:** "Up to now... a purgative... it is time now for
  the elixir."
- **Sermons 28–33:** the "elixir" — the path: element meditation,
  graded pathways (36 steps), signless concentration, seven tool-kits,
  balancing faculties, middle-path depth, and the series synopsis: the
  two ends and the middle (Sermon 33).

## Verification

- JSON scaffold parses (checked at pack build).
- All sermon references resolve (1-33 mapped in pack 50).
- Evidence cites specific suttas and Analayo parallels (SĀ/MĀ/EĀ
  parallels recorded per sermon).
- No transcripts, no media blobs. RIGHTS.md §3 compliant.
- Latest gate receipt in `/tmp/opencode/receipts53`.

## What is NOT here

- Compression — the excavations are raw material. The 10-pass ladder
  (`nibbana-10-passes.md`) is graded raw material, still not a script;
  compression into movie scripts happens per `51-nibbana-movie/PLAIN-ENGLISH.md`
  language law.
- Structural repair of sermon-01/sermon-06: DONE 2026-10-21 (see
  Defects repaired above).
- The scaffold merge pass is DONE (2026-10-21): `answer_p1` (his words at
  pass-1 depth), `depth` (links into the 33-sermon pools), and completed
  `sermons[]` (all nine previously-uncited sermons placed: 9, 18, 21,
  23, 24, 25, 29, 30, 31).
