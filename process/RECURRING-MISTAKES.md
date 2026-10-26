# RECURRING MISTAKES — patterns, not incidents. Read before ANY work.

Individual incidents live in MISTAKES.md (M1–M7, M-A1–A10). This file
is the meta-level: the same failures keep recurring in new costumes.
Each entry: the pattern → the evidence → the standing rule. If you
catch yourself doing the pattern, stop mid-task and fix the rule first.

## R1 — Authoring prose (the slop reflex)
**Evidence:** Fish's 82 composed sentences; six hand-typed S1 beats;
chat summaries dressed as content ("the machine runs instead — twelve
links, busy in the middle; the riddle and the dog at the close" — my
stage-direction poetry, in NO file); mini-essays written in every
"show me" reply.
**Why it recurs:** summarizing/connecting is my default motion. Every
presentation invites me to add a bridge.
**RULE:** present only the three layers — question, verbatim, plain,
plus factual refs (clip, timestamp). Quotations, never compositions.
If a link between two beats isn't in those layers, it does not get
said — not in files, not in chat, not "just this once as a summary".

## R2 — Writing/reading the wrong path
**Evidence:** amendment lessons appended to ROOT MISTAKES.md instead
of process/ (path slip); /tmp-vs-build divergence caught THREE times
(including a vacuous "all clear" audit run against stale build/ while
the fixes sat in /tmp); stale core_v4 in build/ vs fixed in tmp/.
**Why:** multiple live-looking copies exist (tmp/, build/, root,
process/) and I act without resolving which is canonical.
**RULE:** `build/` is the ONLY live data dir; `process/scripts/` the
only home for scripts. Before any read or write: print the resolved
absolute path first. If a file exists in two places, the one outside
build/ or process/scripts/ is suspect — md5 them, pick one, delete or
repoint the other.

## R3 — String surgery and inline-shell brittleness
**Evidence:** python-in-verify.sh died on quotes (twice — M-A4, then
M-A7 IMMEDIATELY after writing axiom 15); glued `}#` endings broke
`t.index('}\n')` anchors TWICE (g7 EXPECTED, make_assembly QUESTIONS);
heredoc triple-quote + `\'` chain write exploded into shell errors;
wrong header string ("G6 TTS scan \"" vs `==`) wasted a turn.
**Why:** I patch files with replace() using anchors remembered from
context, not read at patch time; and I inline complex python into
shell strings.
**RULE:** (a) complex logic = standalone .py, RUN it on real input,
then wire; (b) before replace(): read the exact region, choose an
anchor you just saw verbatim in the read, assert it, and if the
assert fires — re-read, don't improvise a different anchor; (c) never
heredoc multi-line python containing quotes; write the .py with Write.

## R4 — Reporting "done" from memory, not from files
**Evidence:** REVIEW §F: "72/73 beats" (actual 71); "S6b1 fix landed"
(never in build/); "S3b10 swap done" (never in build/); fixes logged
in notes while build/ still held the old state.
**Why:** the note records the INTENTION; I read my own note later as
proof of the OUTCOME.
**RULE:** "applied" = the file shows it AND a gate ran on it after.
Notes are claims, not receipts. Before saying anything is done: show
the file diff or the gate output — from this session, from disk, right
now.

## R5 — Gates tested only on happy paths (the detector that can't fail)
**Evidence:** circular gloss-detector (window contained its own
violation → passed the known-bad line); stale-path audit (0 failures
on old data); G5 naive quote-pairing (would REJECT valid quotes on
sermon-30's parity shift); one-letter word-class regex (`[A-Za-z][\'-]`
matched only D + hyphens — never "Dhono"); uppercase-after-dash
requirement missing the lowercase corpus; `.values()` on a list;
canary written with hyphen, detector accepting only em-dash; my own
g5 script failed on first run.
**Why:** I optimize for "the check exists" not "the check catches".
**RULE:** every detector is FIRST run against a known-bad input
extracted from history (the canary pattern — axiom 15, which I then
violated in M-A7: the axiom doesn't self-enforce, so the operational
form is: write detector → feed it the archived bad line → only then
wire it). One green run on clean data proves nothing.

## R6 — Multiple copies of shared files drifting
**Evidence:** fish_filter.py in /tmp + build/ + process/scripts/ with
three DIFFERENT md5s (edits landed in one, others stale); make_assembly
with td=/tmp in repo copy while /tmp copy was deleted; rebuild_text
in two places.
**Why:** I create a script wherever I'm working, copy later, forget
which is canonical, patch a stale copy.
**RULE:** one canonical copy (process/scripts/ or build/), referenced
by path everywhere else. After any edit: md5 the canonical against all
copies; mismatches get overwritten FROM canonical immediately.

## R7 — Optimizing to the last critique (definition churn)
**Evidence:** five question-sets in a row (made-thread → basic →
antecedent → formula → kick-off), each announced as final and
committed, each killed by the next message. Same for openers
(cold-open order changed 3 times).
**Why:** I take the latest sentence of criticism as the new total spec
and rebuild everything, instead of extracting TESTS first.
**RULE:** on any subjective critique: extract the criteria (tests)
BEFORE drafting anything; draft ONE version against the tests; show
it. Don't commit a full rewrite per message. (The FORMULA exists only
because of this churn — it should have been extracted in round 1.)

## R8 — Concluding from truncated evidence
**Evidence:** S1b8 read as "forum tail" from a grep head, then as
"motto" from another, flip-flopping mid-conversation until the full
transcript sentences were read; 9-vs-"~10" TTS counts asserted from
memory; verdict numbers in REVIEW.md written before recounting.
**Why:** grep/cut -c outputs are cheap and I treat their first line as
the finding.
**RULE:** a conclusion needs the full window (or the whole artifact),
read once properly. Truncations are for locating, never for judging.
Count before writing any number into a doc.

## R9 — Verifying proxies instead of content
**Evidence:** p0 shipped 99.9%-silent audio verified SIX ways that all
passed: integrated LUFS on target, decode exit 0, CBR sizes correct,
byte-identical re-downloads, HTTP 200s, range requests 206. The user heard
a 30ms blip + hiss (M-R1/R2). Same class as R4 (notes-as-proof) and R5
(green-on-clean-data): the check measured something correlated with the
claim instead of the claim.
**Why:** loudness/size/decodability are cheap and feel rigorous; content
audibility needs volumedetect per slice, which nobody ran until the ear
complained.
**RULE:** every stage asserts the PROPERTY IT CLAIMS, on the ARTIFACT IT
SHIPS: audio stages assert peak energy per slice (assert_audible aborts
the render); provenance asserts substrings (G5); TTS asserts detection of
a canary (G6b). A green proxy metric next to an unmeasured property =
the check is void. Name the property in the gate's docstring.
