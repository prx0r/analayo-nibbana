
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
