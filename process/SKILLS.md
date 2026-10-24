# SKILLS — reusable techniques, each with when + how.

1. **Excavation-first sourcing.** Don't quote the commentary about the
   text; quote text that was already excavated per-unit and per-section.
   When: any build with a primary source + a commentary layer.
   How: one file per unit, `## SECTION` headers, `###` subheads, teacher
   words in `"..."`, excavator prose outside. Verbatim pool = quoted
   strings only (regex `"([^"]{30,600})"`, filter `analayo|http`).
2. **Decomp via voice markers.** If the speaker alternates roles (reads
   vs explains), the transcript must mark it. Here: literal `Comment …
   End of comment`. That split is load-bearing — it separates the
   teacher's words from the explainer's without any model judgment.
3. **Keyword + primary assignment.** Score spans against per-section
   keyword lists; ties and zeroes fall back to the unit's primary
   section. Deterministic, auditable, totals must reconcile.
   Always: normalize spelling variants FIRST (aliases table).
4. **Cluster-ordered journeys.** Order by simile/theme groups, not by
   source order. Within group: (lecture, start). Groups ARE the movie.
5. **Motto-cap.** Any repeated opener gets capped (1 core / 3 spaced
   gold). Detected by counting, not by taste.
6. **B-promotion with note.** When the definitional reading lives in a
   B-grade span, promote it into core/gold AND write the reason down.
7. **Honey-pattern (thin-in-audio carried by text).** Check signature
   content by CONCEPT, not keyword ("Madhupindika", not "honey").
   If the audio skims it, the pad carries it — that's the two-source
   design working, not a gap.
8. **Refrain-return structure.** The theme restated at structural joints
   (open, proof-open, section-open) is architecture, not repetition.
   Don't dedupe it away.
9. **Lead-drop TTS.** Fish opens in English, always: drop leading Pali-only
   sentences (function-word density <20%), keep inline terms with dash
   glosses. Punctuation is direction: commas breathe, dashes land,
   no parens in anything spoken.
10. **Two-method verification.** Prove verbatim two independent ways
    (reconstruction from recorded offsets + independent re-split pool).
    One method catches typos; two catch method bugs (both our misses
    were caught this way — one real, one check bug).
11. **Slop quarantine dir.** `slop/` with dated reasons. Never delete
    failures silently — future you needs to see what was tried.
12. **Determinism hash.** Hash the generated outputs; reruns must match
    byte-identically (here: below-lines hash recorded in notes).
13. **Fix the check before the data.** When an audit fails, first suspect
    is a one-sided normalization (strip markdown BOTH sides; don't strip
    quotes the source keeps). Two of our "failures" were check bugs.
14. **Header-bleed trim.** Quote extraction catches trailing subheads
    (`- Udana verse:`) inside captures. Trim `\\n- Header:` tails, then
    re-verify contiguity (substrings stay substrings).
