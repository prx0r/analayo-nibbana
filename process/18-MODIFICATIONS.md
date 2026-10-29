# 18 — MODIFICATIONS. Change the build without breaking it (2026-10-29).

Every change follows the same loop: **edit data → validate_sheet (seconds)
→ rebuild assemblies → re-render ONLY the touched sections →
mix proof + voice check → ears on the delta → gates → log → commit**.
Never re-render everything for a local change. Never ship without the gates.

## 0. Pre-flight (every time, 10 seconds)

```bash
python3 tools/validate_sheet.py   # G0: rhythm, marks, picks, manifest coherence
```
Red sheet stops the line. Green sheet means the data is coherent — render next.

## 1. Change a pause

1. Edit `build/canon/rhythm.json`: slot default or per-unit override
   (`{dur, why}` + owner date — the assert fires without both).
2. `validate_sheet.py` → `make_assembly.py` + `build_seed.py` →
   `render_newA.py` the touched sections (opener pauses live in seed + that
   section) → `render_newA.py full` (re-concat only, seconds).
3. Prove: `p0_mix_check`-class mix proof (beds present), G9 ears,
   Qwen spot on the touched sections, `voice_match.py check`.
4. Log the why in CONDENSED-BUILD-NOTES.md (new §, never amend old).

## 2. Change a voice (or its trim)

1. Trial first: `process/scripts/trial_trio.py` pattern — same text per
   candidate, whisper speakability round-trip, one audition mp3, owner pick.
   Lock IDs + backup in `tools/render_a_essay.py` with provenance comment;
   update `process/17-CASTING.md`.
2. Voice IDs live in the vox cache hash — a voice change auto-invalidates
   old slices (axiom 16). No manual cache wipe needed (verify with
   `ls build/audio_newA/cache/vox_*.wav` mtimes if paranoid).
3. Trims live in `build/canon/voice_match.json` (`measure` → edit →
   `apply` → `check`). Trim position is POST-loudnorm (a pre-loudnorm
   trim is erased to zero — measured 2026-10-29). The trim value is in the
   vox hash too.
4. Re-render touched sections (guide voice ⇒ all sections with Fish lines),
   mix proof, voice check, Qwen spot, owner ear (blend is taste).

## 3. Add/move a word-pause mark

1. Add `{after, dur, why}` to `rhythm.json marks[unit]`.
2. `validate_sheet.py` asserts the anchor occurs EXACTLY ONCE in that
   unit's opener plain (seed + section) — fixes here cost nothing.
3. Rebuild + re-render the unit's sections (seed + sN), Qwen spot the marks
   (they read as phrasing, not holes), owner ear.

## 4. Change picks (newA/ladder) or essay-0

1. Picks: edit the manifest via its builder (`build_newA.py` /
   `build_rungs.py`), never by hand. Essay-0: edit ONLY `essay0.json`
   (builders + G5/G7 read it with drift asserts).
2. `validate_sheet.py` checks picks ⊆ assembly beats.
3. Re-render touched sections + full re-concat. Mix proof, voice check,
   full Qwen rounds if the change moves meaning (nesting re-proven by G8
   for film; A-follows re-derived for essay-0).

## 5. Run ears + stamp a rung

1. Free first: `ear_local.py --full` (whisper, zero tokens) + mix proof.
2. Qwen: `omni_round.py` with `AUDIO_DIR=` + `EAR_OUT=` (14 chunks/round).
   Adjudicate per DONE.md taxonomy into `build/ears/EAR_LEDGER.md` —
   raw model verdicts never gate (whisper/CF/energy decide; transcript wins).
3. Stamp needs ALL FOUR: text gates + mix proof + two consecutive clean
   ear rounds + ledger rows. Stamp in the ledger + notes; update HANDOVER
   numbers the same day (assert your `count == 1` per M17).

## 6. Add a new artifact or doc

New data → `build/canon/` (+ README row). Superseded → `build/versions/`
(+ VERSIONS.md row). New ear evidence → `build/ears/`. New doc → index it
in `process/FILES.md` + `process/README.md` the same day. Audio never
commits (`build/audio_*/` gitignored). Counts change → `sync_counts`-
equivalent recompute + the three gates; docs edited by script assert
`count == 1` (M17 — the HANDOVER §-number drift of 2026-10-29 is why).
