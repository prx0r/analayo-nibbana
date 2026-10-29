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

13. **Audit the path you write.** A checker reading a different path
    than its writer produces vacuous passes on stale data (happened
    three times: /tmp vs build/). Builders and gates read and write
    `build/` directly; a check whose input path differs from the
    writer's output path is void until proven same-file.
14. **Gate logic runs as files, never inline in shell.** Complex
    python in `python3 -c "..."` inside bash dies on quote-escaping
    (twice: M-A4, M-A7). Write the gate as `process/scripts/*.py`,
    RUN it standalone first, then wire it into verify.sh.
15. **Detectors carry their own canary.** A detection rule embeds a
    known-bad input it must flag (G6b: the pre-fix S5b2 line); if the
    detector stops flagging it, the gate fails. A detector that cannot
    fail its own test is not a gate. Provenance-style checks get the
    dual: semantic anchors over derived indexes (M-A7: naive quote
    pairing rejected valid quotes).

16. **Cache keys cover every input that shapes the bytes.** A cache hit
returns old bytes for a new request — after the 2026-10-29 wrong-cast
render (voice IDs changed, Osho slices kept serving under kid/old IDs),
every hash includes voice IDs, trims, and text. A changed input with an
unchanged key ships stale audio with a green gate. (Symlink twin:
after any move, `find -xtype l` before declaring done — the reorg broke
10 lecture links, masked by cache hits until the first miss.)

17. **Presentation order is gospel: TEXT VERBATIM → PLAIN ENGLISH →
    AUDIO.** Every beat shows Nanananda's words first, then Fish speaks
    the plain-English underneath, then the Analayo clip plays. Never
    reorder — the listener reads the claim, hears the translation in
    English, then hears the teacher. The section opening follows the
    same spine: bell → Fish asks the question → 3s recollect → ESSAY 0
    (the compressed answer) on screen → the archive voice answers it
    directly. Nothing wedges between question and answer (no intro
    bridges there; a human intro, if used at all, comes AFTER the
    answer — see 12-ARGUMENT.md).

