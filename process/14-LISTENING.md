# 14 — LISTENING. How the machine hears the build (owner method, 2026-10-26).

## 1. Why listen at all (the transcript is already proven)

Gates prove WORDS: provenance (right words), order (right sequence),
levels (right loudness). None of them proves EXPERIENCE. Listening
catches the failure classes text cannot see:

- **Cuts inside windows.** A slice can be sentence-snapped on paper and
  still sever a thought mid-breath. Only ears hear it.
- **Felt fit.** Q→A can pass the oral test on the page and still feel
  evasive in the ear (seed U2: text leans, audio rescues — found by
  reading, CONFIRMED by listening).
- **Rhythm and fatigue.** Density the eye skims, the ear drowns in.
  The 316s rope and 376s word-study were green on every gate and heavy
  on every listen — ears set the water-scaling rule.
- **Voice blend.** Levels can match while timbres fight. Meters said
  −19 LUFS both voices; only ears can pass timbre (still human-only).
- **Arc.** Does the section land, or just stop? A per-beat pass never
  asks this. The critic does.

Rule: text gates are necessary, never sufficient. Nothing ships on
transcripts alone (R9: proxies, not content — loudness proved this).

## 2. The two ears (separate jobs, same render)

**Ear 1 — AUDIT (defects only).** Prompt constrains to timestamps:
mid-thought starts/ends, dead air >5s, clicks/thumps, volume jumps,
synthetic voices. Output is binary per chunk: CLEAN or timestamped
defects. No opinions allowed — opinions smuggle taste into verification.

**Ear 2 — CRITIC (ratings + advice).** Qwen is the peer reviewer. Per
section, 1–5 on five axes, each with one quoted moment as evidence:

1. **Directness** — does each answer land on its question within 30s?
2. **Flow** — does each beat follow from the last without a swerve?
3. **Pace** — contemplative vs dragging, per section (S2/S3 are the risk).
4. **Arc** — does the section close, or trail off?
5. **Blend** — do the voices sit in one room?

Then: three timestamped granular notes (best moment, weakest joint,
one surprise), plus one piece of structural advice ("what would you
cut or move?"). Advice is ADVISORY — it enters the fix queue only
after the read-through confirms it against sources (M6: metrics and
models nominate, reading disposes — models included).

## 3. Technical analysis (meters beside ears)

Per render, per section: integrated LUFS, peak dB, silence map
(≥1.2s), zero-run/dropout scan, per-chunk energy timeline. Meters
catch what ears forgive (slow level drift, sub-threshold hiss pumping
from loudnorm on quiet tails). Ears catch what meters forgive
(everything in §1). Both run; either can fail the build.

## 4. Operating limits (learned, not documented anywhere)

- Models: `qwen3-omni-flash` (cheapest ear, proven on our audio) and
  `qwen3.8-omni-flash` (newer generation, thinking on — both verified
  working) via DashScope intl compatible-mode; key = vault
  DASHSCOPE_API_KEY. Docs confirm the line: 3.8 built for audio/video
  understanding + thinking + function calling, 1M context, combined
  text+image+audio+video in one request. Default to 3-omni-flash;
  escalate to 3.8 when a verdict needs reasoning depth (strip its
  reasoning_content before parsing).
- Unused full potential, queued: 1M context lets us send STORYBOARD
  text + audio in ONE request (grounded critique: model reads the plan
  while hearing the cut); thinking on for critic, off for audit;
  `response_format: json_object` verified — ratings return parsable
  (strip fences), feeding a future G-ear gate with floors; dedicated
  `qwen3-asr-flash` (language+emotion annotations) for fast order-checks
  when local CPU bottlenecks; `qwen3-omni-30b-a3b-captioner` for
  ambience/music characterization when the sound design lands.
- Max audio per call ≈ 15 min: chunk longer sections at ≤12 min with
  30s overlap; critique chunks, never downsample (downsampling destroys
  exactly the artifacts under test).
- `input_audio.data` takes a PUBLIC URL string (base64 rejected,
  `{"type":"audio"}` rejected). Upload chunks to a temp host, critique
  immediately (uguu.se ≈ 3h retention — the critique must run same-day).
- Whisper (local faster-whisper) does ORDER checks (questions in
  sequence, essay-0 phrases present, no robot remnants) — it does NOT
  do quality judgment. Never ask transcription to opine; never ask the
  critic to transcribe.
- Re-listens are scoped: after a fix, re-hear affected chunks only,
  plus one seed end-to-end (the chain lives there). Full passes only
  after structural moves (reorders, voice swaps).

## 5. What stays human (taste locks, not verification)

Timbre match, YT-anchor naturalness, Fish voice approval, essay-0
answer picks (U2/U6), demote calls, human intros, and the final
"does it move me" — the one question no meter or model may answer.
Owner listens for locks; the machine listens for flaws. Never the
reverse.
