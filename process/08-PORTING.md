# 08 — PORTING. Running this process on another text (e.g. Sanskrit).

Everything structural transfers unchanged: segments, grades, flow audit,
provenance, 3 speakers, verify gates, 3 versions. What changes is only
the LANGUAGE LAYER and the source-specific inputs. Checklist:

## 1. Source prep (same requirements as 00-INPUTS, any language)
- [ ] Primary text per unit, with QUOTATION marked (teacher's words vs
  commentary — machine-distinguishable, or mark it first).
- [ ] MP3 rendition per unit (any speaker; single mic/room preferred).
- [ ] Timestamped transcripts + voice-role markers (who is reading vs
  explaining — add markers if absent; the decompilation depends on it).
- [ ] Sanskrit specifics: fix ONE transliteration scheme up front
  (IAST with diacritics for text, plain ASCII fold for matching —
  exactly the dual we used). Devanagari, if present, gets romanized
  once, into files, before anything matches on text.

## 2. Build the key (replaces fish_filter + blunt_key, same format)
- Frequency-list the source-language tokens in the text (here: 144×
  papancha, 74× satipatthana — the counts tell you what MUST be mapped).
- For each: plain-English mapping per the 07 standard, owner-vetted.
- Loanword list: named concepts the audience owns (decide once).
- TTS rule is language-independent: NO source-language tokens spoken,
  ever. Pads show them (text), Fish says the plain form. No exceptions,
  no "just this once" — that's how slop enters.

## 3. Where explanations live (objective placement — same for any text)
- PRIMARY AUTHOR: verbatim only. Provenance or it didn't happen.
- KEY/GLOSS: word/phrase meaning, deterministic, versioned.
  May say what a term MEANS. May never add claims, stories, or reasons.
- FISH: mapped terms + gloss lines ONLY. No connective tissue, no
  "as we saw", no setup sentences. If a join needs words, that's a
  HUMAN bridge (marked BRIDGE) or a pause — never Fish improvising.
- HUMAN: framing questions ("what this answers, why now"), rare
  marked bridges. The only place new sentences may originate, and
  each must be flagged as human voice in the manifest.
- COMMENTATOR (archive voice): explanations already in the rendition.
  Selected and ordered, never written. If the rendition lacks an
  explanation a beat needs, the beat gets a human bridge or silence —
  never an invented gloss.
- TEST for any sentence in the build: traceable to (verbatim | key |
  marked-human-bridge | archive-clip)? If none — slop. Delete it.

## 4. What to expect (from this build's numbers)
- ~1,150 kept spans → ~6 segments → 555 gold → 83 core beats is a
  reasonable shape for a ~30-unit, ~20h series. Scale linearly.
- Thin sections are structural (concentrated doctrines) — don't pad.
- YT/auto transcripts WILL need an aliases table; budget for it.
- First provenance audit WILL find hand-written text. That's what it's for.

## 5. Deliverables per port (same as FILES.md)
Staged pool/gold/core JSONs, per-beat scripts (clip + verbatim +
provenance + plain + tts), manifests, keys, speaker rules, verify.sh
green. Nothing else counts as done.
