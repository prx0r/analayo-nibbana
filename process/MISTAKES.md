# MISTAKES — everything we got wrong, with cause + fix. Read before touching the pipeline.

## Render mistakes (2026-10-26, p0 — all caught by the owner's ear, not by gates)

- **M-R1 afade-out at st=0 silences the whole file.** `afade=t=out:st=0:d=0.03`
  fades to zero at 30ms and STAYS at zero — every voice slice shipped as a
  30ms blip + digital silence, in v1 AND p0. The user heard exactly that
  ("initial blip then no audio") across three hosts before any gate noticed.
  Fix: `fade_tail(dur)` — fade-out starts at (dur−0.03), computed per slice
  (probed for espeak); VTAG bumped normv2→normv3 so poisoned cache can't
  survive. Rule: never st=0 on a fade-out; fade positions are durations,
  not constants.
- **M-R2 loudness verification masked silence.** Integrated LUFS (−18.7),
  clean decode (exit 0), correct CBR file sizes, byte-identical re-downloads
  ALL PASSED on files that were 99.9% silence — the final loudnorm pass
  dutifully amplified the noise floor to target, so loudness *proved*
  nothing. CBR size proves nothing (constant bitrate, silent or not).
  Fix: `assert_audible()` in the renderer — every cut slice must show
  peak > −60 dB or the render aborts; plus energy-timeline spot checks
  (volumedetect per chunk), never loudnorm numbers alone. See R9.
- **M-R3 truncated uploads present as success.** Catbox returned file URLs +
  HTTP 200 for 1.1MB fragments of 6MB files (egress cut mid-POST). Fix:
  re-download every upload and compare size/md5 before sending any link.
  No link ships without a byte check.
- **M-R4 R2 presigns need SigV4 + short links.** Default `aws s3 presign`
  minted SigV2 URLs (R2: "SigV2 not supported"); fix `--region auto`.
  Separately, 400-char signed URLs get mangled in chat clients — prefer
  short direct links (uguu.se worked; note 3h retention).
- **M-R5 string sermon tag vs int lookup.** A beat carrying
  `nanananda_sermon` as a string ("S11-Madhupindika…") failed `in SERM`
  (int keys) → 4 honey-ball parts fell back to robot voice. The aligner
  already regex-extracted ints; the renderer didn't. Fix: normalize in
  `verbatim_wavs`. Rule: IDs cross module boundaries in ONE type.
- **M-R6 longest-run alignment under-scored long quotes.** 17/71 beats
  "missed" although the passages were present — whisper noise breaks
  contiguity, so longest-match/len collapsed on 100+ word quotes.
  Fix: coverage scoring (matched tokens / quote tokens) + cross-sermon
  fallback scan → 70/71; last fragment (Pali chant the transcriber dropped
  as non-English, living in a 4.2s transcript gap) via evidence-logged
  manual PIN. Final: 71/71, zero robot voices.

> Also read `RECURRING-MISTAKES.md` — the META patterns (R1–R9) that
> produced most of the incidents below (slop reflex, wrong-path writes,
> memory-claims, happy-path gates). This file logs WHAT happened;
> that file says WHAT KEEPS HAPPENING.
- **M-R7 verbatim windows cold-opening on chant.** Seed U1's sermon window
  (45.16–78.48) opened on the 7s Namotasya chant, 20s before the matched
  motto — ±1-sentence expansion outran the anchor. Owner: never open on
  Pali/preamble. Fix: head-trim to first quote-token sentence in
  align_quote. Rule: a window's first sentence must share tokens with its
  quote (checked, not assumed).
- **M-R8 snapper eating quote content.** Mechanical edge-trims ate CF
  quote-openings split across sentences (mirror's "Even / if one already")
  and drifted a head backward through overlapping timestamps. Essay-0/B*
  windows are atomic — exempt like mottos. Fragment-head rule is YT-only.
  Snaps only shrink, never expand. Rule: trim markers and chants only;
  never trim words that could be the quote.
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

## Amendment-pass mistakes (2026-10-24, review→fix round)
- **M-A1 lead-drop regex**: first fix required uppercase after the dash
  (`[A-Z"']`) but corpus continues lowercase ("va — the arahant"). Found
  by testing against the real line, not by re-reading the regex. Fix:
  accept any letter start + English-tail guard so we never eat content.
- **M-A2 /tmp-vs-build divergence — THIRD instance of this class.**
  I rebuilt into /tmp while auditing build/, then ran the "all clear"
  audit against STALE build/ files — a vacuous pass that reported 0
  failures on old data. (Same class as MISTAKES §13; caught only
  because S1 beat-count looked wrong: 12 vs 11.) Permanent fix applied:
  rebuild_text.py + make_assembly.py now read AND write build/ directly,
  copy-step eliminated. Rule: an audit must read the same path it will
  report on; if the writer and checker paths differ, the check is void.
- **M-A3 circular detector**: first unglossed-Pali gate used a ±40-char
  window around each term — but the dash that TERMINATES the leading
  Pali run sits inside that window, so the violation passed its own
  check (retro-test on the known-bad line flagged nothing). Fix: split
  into two checks — positional leading-run detection (before first
  punctuation) and marker-based term attachment. Canary line embedded
  in the gate so this can never silently regress again.
- **M-A4 inline python-in-bash fragility**: the G6 hardening written
  as `python3 -c "..."` inside verify.sh broke on quote/escapes (third
  shell-quoting casualty). Fix: standalone `process/scripts/
  g6_tts_check.py`, verify.sh calls it. Complex logic never inlines
  into shell strings.
- **M-A5 detector false positives**: first working detector flagged 3
  English lines ("Once gone beyond," "Those wise ones...") because the
  function-word ratio (0.2) misreads dense English content sentences.
  Fix: require >=4 words AND zero function words. Tradeoff documented
  in the docstring; the canary pins the true-positive side.
- **M-A6 unicode-vs-ascii key**: satipatthana gloss never attached
  because verbatim carries `ṭh` while key patterns are ASCII and
  gloss() stripped diacritics AFTER matching. Fix: strip before match.
  Lesson: sources are mixed-unicode; normalizing late means patterns
  silently never fire.

- **M-A7 gate-implementing sins (two at once).** (a) Rewrote the G5
  provenance check inline in verify.sh — broke on shell quote-escaping,
  the SECOND casualty of the same M-A4 rule I had just written.
  (b) The old G5 span-set used naive quote pairing; sermon-30 has an
  off-by-one quote earlier in the file, which paired labels instead of
  content — a semantically valid quote would have been REJECTED by its
  own gate. Fix: semantic anchor test (quote+text+quote in normalized
  source), standalone script, file-mode tested before wiring in.
  Bonus: my first draft of that script called .values() on a list —
  caught by running it. Lesson (relearned): write gate logic as a
  runnable file and RUN it before wiring; never inline; never trust
  pairing-derived indexes when a direct search exists.

- **M-A8 retrofitted openers leaked seams.** Built cores first, bolted
  questions on later: Q and A came from different sessions, so pairs
  didn't answer each other ("Why do I suffer?" over a verbatim that
  never says suffer). User caught it as "it doesn't really make sense".
  Fix: essay-0-first build order (12-ARGUMENT) — write the micro-session
  (Q+A as dialogue, oral test) BEFORE any beat; adjust OUR question to
  the extracted answer, never the verbatim. Question rewrites this
  pass: S2 "What keeps it going?", S3 "Is any of it real?",
  S6 "What's left when the show stops?" (each closes a concrete leap).

- **M-A9 dangling pronoun in the chain.** Chained Q1 "What is Nibbana?"
  → Q2 "What keeps it going?" — *it* referenced nothing: Q1 is about
  the goal, Q2 silently switched to samsara without naming it. User
  caught it as nonsense. Fix: THE ANTECEDENT RULE (12-ARGUMENT) —
  pronoun in Q(n) must resolve inside A(n-1); Q2 reworded to "What
  keeps it all going?" where "it all" = Q1's answer. Added to the
  chain's edge test (b).

- **M-A10 naked-pronoun questions.** "Is any of it real?" — *it* has
  no standalone referent (user: "is any of WHAT real?"). M-A9's
  antecedent patch ("it all" resolving into the previous answer) was
  still a bandage: questions must not lean on ANY previous beat at all.
  Fix: THE FORMULA (12-ARGUMENT) — 4 tests (standalone+precise /
  cut / content-fit / plain). Precision sub-clause followed: "What
  am I made of?" was vague (body? character?) while the material
  dissects the self -> "What is the self made of?". New questions written to it: Q2 from user's
  example ("Why don't I see Nibbana right now?" — which turned out to
  make the OLD motto-echo beat the RIGHT essay 0, "this point is hard
  to see"), Q3 "Why does the world feel real?", Q5 "How does anyone
  actually wake up?", Q6 "What's left when everything stops?".

