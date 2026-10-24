# AXIOMS — binding rules. Violations fail the build.

1. **Verbatim is extracted, never typed.** Every sacred word carries
   {source file, start, end} provenance. Reconstruction (slice source at
   offsets) must equal the text, byte for byte modulo whitespace/markdown.
2. **Sources are quotations only.** Excavation ` "..." ` blocks count.
   Excavator prose, forum text, Analayo's explanations, and our notes are
   NEVER verbatim sources — even when they sound right.
3. **One span, one home.** Every kept span belongs to exactly one segment.
   Overlaps resolve by content keyword; ties go to the lecture's primary
   segment. Totals must reconcile (pool sum == full kept duration).
4. **Seams read standalone.** No keep starts mid-sentence, ends mid-thought,
   or dangles ("as mentioned above", bare "therefore", "so..."). Blocks
   after a cut must parse cold. Sentence-snapped boundaries only.
5. **Grades are load-bearing.** A = spine (never dropped), B = flow
   (dropped largest-first over budget), C/D = cut outright (forum, recap,
   2nd translations, Pali chant, closers). Core prefers A; B enters only
   with a written reason (e.g. definitional reading lives in B).
6. **Fish speaks mappings, never sentences it invents.** Term-key only:
   max ~5 words, first hearing per section, max 2 drops per clip.
   TTS lines are English-first (no leading Pali refrains), punctuation is
   direction (commas breathe, dashes land, no parens, no mid-sentence
   starts). Below-lines are pure function of (verbatim, key) — reruns are
   byte-identical (hash-recorded).
7. **One voice per job.** Analayo = readings + explanations (archive).
   Fish = mapped words + plain-English lines (never Pali, never narration).
   Human = intros + rare bridges (never Pali verses — the archive voice
   owns them).
8. **Mottos open, never stack.** One motto per core (cold open). Max three
   spaced in gold (open/middle/close). Never back-to-back.
9. **Slop is quarantined, not deleted.** Hand-written or failed artifacts
   move to `slop/` with a dated note, never ship, never silently fixed.
10. **Audit before render.** Provenance 100%, flow-read complete, hold-up
    test passed (pad primes its clip — verified by reading, not counting),
    TTS lines scanned (no dead air, no orphaned punctuation). Audio is
    always the LAST step.
11. **Thin is honest.** A thin section stays thin (no padding to quotas).
    Gaps are declared (missing mp3s, YT-only timebases) with owners.
12. **Every fix is logged with cause.** No silent edits. MISTAKES.md grows;
    the pipeline only changes by adding checks, never by relaxing them.
