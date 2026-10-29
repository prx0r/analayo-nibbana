# 17 — CASTING. Trialing and locking voices (2026-10-28/29).

Voices are cast like actors: audition, owner pick, lock with a backup.
Never ship a voice the owner hasn't heard; never re-audition a locked seat
without an owner reason.

## The trial pattern (cheap, decisive)

1. Harvest candidate voice IDs (Fish `/model`, `title=` search; shiva trio
   came from their locked cast).
2. Render the SAME short text per candidate (our shape: Q1 question for
   asker candidates, U1 plain for answerer candidates) — timbre judges
   timbre, not text. Whisper round-trip each sample (proves speakability:
   Osho's "Nibbana" passed; a voice that can't say the words is out).
3. Concat per role into ONE audition mp3 (kids ask, then old men answer),
   delete individuals, upload one link. Owner picks by timestamp.
4. Lock: IDs into the render (`tools/render_a_essay.py` `FISH_Q_VOICE` /
   `FISH_A_VOICE`, cast shared by the newA + B drivers) with provenance
   comment; previous cast kept as commented backup.

## The locked cast (2026-10-29)

- Q (kid, inquisitive): `0c0f9d7d87e44e2dabb53ebb092f5f53`
- Plain (wise old British): `98db2383e6a14132b75a79b565f731ab`
- Backup old man (original elderly): `f4011527d52045bebe004aa874695276`
- Retired: Osho + Sadhguru + Gurudeep (trio trial 2026-10-29; Osho voiced
  one full render, replaced same day — "not Osho throughout" was a stale
  cache serving Osho slices under new IDs, fixed by keying vid in the hash).

## Rules

- One voice per seat; rotation (e.g. a different kid per question) needs an
  explicit owner call and a per-unit cast map — never improvise.
- Speech says NIRVANA (data keeps Nibbana; substitution at voice time).
  Any voice change re-proves speakability (carrier probes + whisper).
- Voice identity is NEVER verified by model ears (Qwen flip-flops on
  "same/different voice" across identical bytes — measured). Proof is
  deterministic: cache provenance + code path + F0 clusters per role.
