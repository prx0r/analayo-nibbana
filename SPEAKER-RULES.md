# SPEAKER RULES — 3 voices, v2 (2026-10-24): Analayo *is* Nanananda's voice

Measured on core v4: the clips are mostly Analayo READING Nanananda (S2 1033s N vs
229s explaining; S3 931 vs 294; S5 751 vs 138; S4 entirely Nanananda). Only S1
leans explaining. So: no human Pali recording needed — his motto readings stand
(10 in gold, 1 per core). The decompilation (Comment/End-of-comment split) already
separates Nanananda-reading from Analayo-explaining inside his audio.

## The Pali rule (unchanged: Fish never reads Pali — PLAIN-ENGLISH law)
- Fish speaks English ONLY (filter in /tmp/opencode/condensed/fish_filter.py).
  Pali on-screen as citation text, never in Fish's script.
- ALL Pali out loud = Analayo's own readings (motto per section cold-open +
  verse lines inside Nanananda-reading clips). One consistent Pali voice: his.
- Human reads NO Pali. Human does section intros + bridge lines only.

## Who speaks what (v2)
1. ANALAYO (archive) — BOTH voices, as cut: (a) Nanananda-reading (incl. Pali
   motto/verses + English sermon text), (b) his own unlock comments. Unchanged audio.
2. FISH (TTS) — the KEY, nothing else. When Analayo's audio speaks a Pali term,
   Fish says the mapped English word/phrase and stops. First hearing per section
   only, max 2 drops per clip (23 drops across the whole ~2h core). Never a
   sentence. Never "he's about to say", never "in other words", never narration.
   Map: /tmp/opencode/condensed/fish_filter.py (ascii-spelling safe).
   Drops: segN_terms.json. E.g. hears "papancha" → says "spiralling". That's it.
3. HUMAN (you) — section intros (~40s ×6, your words: what it answers, why now)
   + bridge lines ONLY where neither Fish nor Analayo covers the join (marked
   BRIDGE in manifests — rare). Total ≈ 4-5 min raw. No Pali, no verses.

## The Pali rule (Fish never reads Pali — your PLAIN-ENGLISH law already says this)
- Fish speaks English ONLY. Every Pali term in Nanananda pads passes through the
  PLAIN-ENGLISH map first (sankhara→preparations, upadana→grasping/fuel, etc.).
  Pali appears on-screen as citation text, never in Fish's script. If a sentence
  needs a Pali word to make sense, rewrite the sentence.
- Human (you) reads ALL Pali out loud: motto per section + ~8 verse lines.
  Your voice owns the sacred sounds; Fish owns explanation; Analayo owns analysis.
- Analayo clips stay as-is (his Pali recitations were already cut as chant gaps —
  do NOT restore them; the Human covers Pali now, one consistent voice for it).

## Who speaks what
1. HUMAN — cold open per section: motto in Pali, then English, ~15s. Then a
   30-45s intro in your own words: what this section answers, why it matters.
   Plus ~8 verse readings total (listed below). Plus bridge lines only where
   Analayo's join needs a human hand (marked BRIDGE in manifests — use sparingly).
2. FISH — Nanananda pads (English, plain-English filtered): the simile, the
   verse meaning, the refutation, in Nanananda's order. Never Pali, never meta-talk.
3. ANALAYO — unlock clips only (core v4 lists): translation disambiguation,
   parallels proof, "why it matters" glosses. Never the motto (Human has it),
   never forum/recaps (already cut).

## Handoff grammar (same every beat — listener learns it once)
Human intro → [bell] → Fish pad (Nanananda: image/verse/refutation) → 1.5s breath
→ Analayo unlock → 2.5s water → next beat. Bells: F §1 / R §2 / C §3 / D §4 / Z §5 / L §6.
No voice overlaps another. Pauses are separate clips.

## Human recording list (total ≈ 7 minutes — not ages)
Motto ×6 (Pali + English, ~25s each — same take, reuse melody):
  "Etam santam etam panitam: sabbasankharasamatho, sabbupadhipatinissaggo,
   tanhakkhayo, virago, nirodho, nibbanam. This is peaceful, this is excellent:
   the stilling of all preparations, the relinquishment of all assets, the
   destruction of craving, detachment, cessation, extinction."
Section intros ×6 (~40s each, your words): 1 question each answers + why now.
Bridges ×a handful (~15s each, only where marked BRIDGE).
Total ≈ 4-5 min raw. No Pali, no verses — Analayo's readings stand.

## Fish script prep (assembly step, scripted)
Strip Pali from pad texts via PLAIN-ENGLISH map; expand abbreviations; split
>220-char sentences; mark bell slots [BELL:X]; mark Analayo handoffs [BREATH].
Fish voice: one consistent voice, slightly drier than Human (staging: Human is
warm/close, Fish is clear/mid, Analayo is room/archive — three depths).

## Alternatives considered and rejected
- Phonetic Pali for Fish ("ay-tung sun-tung"): inconsistent, breaks on long
  compounds, violates the language law you already set. No.
- Restoring Analayo's Pali chant gaps: wrong vibe (chant vs your spoken refrain),
  two Pali voices. No.
- Fish reads everything incl. Pali: butchers it, kills authority. No.
- You read everything: hours of recording. No — ~10 min raw is the whole job.
