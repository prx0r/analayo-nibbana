# 04 — PAD + GLOSS + VOICES. The three-layer beat.

## Nanananda pads (verbatim assignment + provenance)
- Per core clip, match one excavation quotation: keyword overlap +
  same-sermon bonus (+3), uniqueness enforced per section (no quote
  twice, except deliberate refrain returns). Honey-pattern: if the
  signature content lives under another name ("Madhupindika", not
  "honey"), search the concept, not the word.
- Targeted overrides beat pure matching where reading proved mismatch
  (here: 5 cases — Bahiya payoff/na-tena, magic-show hiding-place,
  honey exposition, delight-in-existence mirror, Kaccayana lead).
  Overrides are normal; UNLOGGED overrides are slop.
- Record provenance per beat: {source file, char offsets}. Verify by
  RECONSTRUCTION: slicing source at offsets must equal the text
  (whitespace/markdown-insensitive). Then verify again with an
  INDEPENDENT method (different splitter, e.g. quote-split pool).
  Here: 75 excerpts, 0 failures, both methods.
- Multi-part pads (exposition + verse + hunger…) are stored as excerpt
  LISTS, each individually verified — never concatenated prose.

## Plain English (mechanical gloss, zero free text)
- Two deterministic layers over the verbatim: term map (`fish_filter.py`
  PALI2EN: Pali word → plain word, word-boundary safe) then blunt map
  (`blunt_key.json`: doctrinal phrase → unmistakable plain words).
- Format: `TERM (plain)` first use per beat, then plain alone. Parens in
  the source that merely cite get stripped; citations (sutta refs) stay.
- Determinism: reruns are byte-identical (hash recorded). Any hand edit
  breaks the chain — edits go into the KEY, never into the output.

## TTS lines (Fish's script — punctuation IS direction)
- From the gloss: strip markdown, parens → em-dash pauses, colons →
  dashes, semicolons → commas, slashes → periods, drop leading Pali-only
  sentences (Fish never opens in Pali — English-first rule), fix
  article pile-ups ("the the", "namely the everything").
- Voice grammar: commas breathe, dashes land, periods stop. Motto beats
  keep the user's requested "namely," cadence.
- Fish ALSO drops mapped single words on first hearing per section
  (`segN_terms.json`, max 2/clip) — the glossary function, separate
  from beat lines.

## Speaker mapping (v3 — locked)
- ANALAYO (archive): readings + explanations, untouched. Owns ALL Pali
  spoken aloud (mottos, verses). No other voice touches Pali.
- FISH (TTS): term drops + plain-English beat lines ONLY. Never Pali,
  never narration ("he's about to say" and friends are banned —
  see MISTAKES.md § slop).
- HUMAN: section intros (~40s) + rare marked bridges. No Pali verses
  (archive voice owns them). ~5 min raw total.
- Beat order: [human intro per section] → bell → Fish line (prime) →
  Analayo clip (lands) → 2.5s water → next. Nanananda verbatim rides
  on-screen with the Analayo clip that contains/expands it.

## Outputs
`segN_script.json` (clip + verbatim + provenance + plain + tts),
`segN_terms.json` (Fish drops), `SPEAKER-RULES.md`. Fail the stage if:
any verbatim lacks provenance, any TTS line opens in Pali, any Fish
sentence isn't traceable to (verbatim, key).
