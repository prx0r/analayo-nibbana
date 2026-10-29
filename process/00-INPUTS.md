# 00 — INPUTS. What you need before anything runs.

## 1. Primary source (the teaching text)
- The complete sermons/talks as TEXT, organized per unit (here: 33 files,
  `sermon-NN-excavation.md`, each internally sectioned by argument).
- Requirement that matters: the text must distinguish QUOTATION (the
  teacher's words, in `"..."`) from commentary ABOUT the words. Our entire
  verbatim pipeline depends on this distinction. If your source doesn't
  mark it, mark it first — everything downstream assumes it.
- Optional but powerful: a parallel "scaffold" that reorders the material
  into argument order (here: 6 sections). It becomes the segment map.

## 2. MP3 rendition (someone speaking it)
- One audio file per unit, same order as the text units (here:
  `sources/lectures/audio/analayo-nibbana-lecture-NN.mp3`, 33/33 present — 23 native + 10 fetched
  from dharmaseed retreat 4373, symlinked).
- Quality bar: single voice, single mic/room if possible (joins go
  invisible). DS-native seconds are the timebase.
- Missing audio does NOT block text work: cut positions come from
  transcripts; audio fills in at render. Track gaps explicitly.

## 3. Transcripts (the bridge between 1 and 2)
- Per unit, timestamped sentences: `[{t, end, text}]` (here:
  `sources/lectures/transcripts/lecture-NN.transcript.cf.json` from faster-whisper; 23 CF + 10 YT-cue
  fallbacks in `sources/lectures/yt-subs/`).
- The transcript must ALSO mark voice changes if the speaker alternates
  roles. Here: literal `Comment ... End of comment` markers split
  Nanananda-reading from Analayo-explaining — that split IS the
  decompilation the whole build rests on. If your rendition lacks it,
  add it (even roughly); without it you cannot separate text from gloss.
- Spelling variants must be normalized before matching (here: baya→bahiya,
  kachayana→kaccayana, YT transcripts are cue-soup needing sentence
  regrouping). Keep an aliases table; it grows.

## 4. Tooling present (era-1, FROZEN — method history; live paths under sources/)
- `tools/auto_keeps.py` (draft keeps: forum/recap/translation/Pali/closer
  cuts + rank), `tools/gen_plan.py` (band-fit generator, ≤2400s assert).
- `jq`/`python3` + `ffmpeg` + `ffprobe` for render.
- `condensed-build` outputs land in `build/canon/` (repo) — never only /tmp.

## Readiness checklist (all yes before stage 01)
- [ ] Every unit has text, audio-or-gap-note, transcript-or-cue-fallback
- [ ] Quotation vs commentary is machine-distinguishable in the text
- [ ] Voice roles are machine-distinguishable in the transcript
- [ ] Aliases table started (it WILL grow — see MISTAKES.md § transcription)
