# 07 — PLAIN-ENGLISH STANDARD. What "plain" means, testably.

"Plain" is not a vibe. A line is plain English iff it passes all four.
Anything that fails goes back through the key, never straight to TTS.

## Test 1 — No untranslated source tokens (automated)
Every word must be English or on the LOANWORD list. Loanwords are named
concepts the audience already owns (here: "Nibbana", "Dhamma", "karma" —
decided once, listed in one place, never improvised per line).
Check: tokenize the line, drop the loanword list, drop proper names —
every remaining token must be plain ASCII English. Diacritics anywhere
outside an explicit on-screen-only field = instant fail.
(Our TTS scan checks diacritics; extend it with your loanword list.)

## Test 2 — Every domain term is replaced or glossed on first use
`TERM (plain)` first occurrence per beat, plain alone after. "Replaced"
means the KEY did it (fish_filter-style map), not a human paraphrase
inline. If a term has no key entry, the line is not done — add the
mapping (owner-vetted), don't improvise around it.

## Test 3 — Actor + action, no nominalizations hiding the verb
Fail: "the cessation of craving", "the relinquishment of assets",
"the stilling of preparations". These name processes as things.
Pass: "wanting ends", "dropping everything you carry",
"everything the mind makes comes to a stop".
Mechanical check: flag -tion/-sion/-ment/-ance/-ence nouns derived from
verbs (cessation, relinquishment, detachment, proliferation, reckoning,
imagination). Each flagged noun must either be replaced by its verb
form or be a KEY entry with a vetted plain form. Keep a stoplist of
allowed ones (here: almost none — "existence" survived only inside
fixed phrases, flagged for review).

## Test 4 — One idea per breath unit
Commas separate items, em-dashes mark turns, periods stop. No colons,
semicolons, or parentheses in anything spoken (they become dashes/
periods per the TTS transform). No sentence over ~25 words. No
subordinate clause stacked on another — split it.

## How to make it blunt (procedure, not taste)
1. Start from the literal gloss (key output).
2. Ask: WHO does WHAT to WHAT? If the sentence can't answer, rewrite
   until it can. ("Stillness of preparations" → who? the mind. does
   what? stops. what? making things.)
3. Prefer short Germanic words over Latinate ones (stop over cease,
   end over terminate, hold over grasp where meaning survives — but
   NEVER at the cost of accuracy; owner vets every mapping).
4. Read it aloud once. If you stumble, it fails Test 4 — split it.
5. Worked example (from this build):
   IN:  "the stilling of all preparations"
   OUT: "everything the mind makes comes to a stop"
   (actor=mind, action=stops, object=making things; zero jargon left)

## Ownership rule
The KEY files (term map + blunt map) are the ONLY place plain-English
decisions live. Mappings are proposals until the domain owner signs
them. Generated lines are never hand-edited — fix the map, rerun,
verify byte-identical change is limited to the intended lines (diff it).
