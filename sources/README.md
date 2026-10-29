# sources/ — primary materials (the only things the build may quote)

Two voices, two folders. Everything here is INPUT. Nothing here is generated.

## lectures/ — Analayo (the teacher; archive voice #1)

| path | what |
|---|---|
| `audio/` | 33 lecture mp3s (`analayo-nibbana-lecture-NN.mp3`; some symlinked into `ds-full/`) |
| `transcripts/` | 23 CF-whisper JSONs (DS-native timebase = mp3 seconds) |
| `yt-subs/` | 27 YT cue JSONs (YT-only lectures: 03,06,07,14,17,20,22,24,26,27 + spares; YT timebase, anchor-mapped at render) |
| `ds-full/` `ds-mp3/` | DharmaSeed originals (10 + 4; `audio/` symlinks resolve here where CF is missing) |
| `cutplans/` | era-1 cutplans (`lecture-NN.cutplan.json/.md`, 33/33 done) + `lecture-03.notes.md` — SUPERSEDED method, kept for provenance |
| `cutplans/keeps/` | era-1 keep-lists (`lecNN_keeps.py`) + `gen_plan01.py` — SUPERSEDED inputs |

## sermons/ — Ñāṇananda (the text; verbatim home)

| path | what |
|---|---|
| `excavations/` | 33 `sermon-NN-excavation.md` = **the only verbatim home** (G5 anchors quotes here, repo-local first; legacy `/tmp/satsang-ext/` path is fallback only) + `nibbana-scaffold.md` (argument map) + `nibbana-10-passes.md`, `REPORT.md`, `MERGE-Notes` (method history) |
| `audio/` | 33 sermon READINGS (`Nibbana_Stilled_NN.mp3`, 412MB — the verbatim heard aloud) |
| `readings/` | 33 faster-whisper transcripts of the readings (CF schema) + SERMON-01 word-for-word YT transcript |

Rule: verbatim fields are extracted from `excavations/` (or `readings/` for alignment), never typed. Quote without {file,start,end} provenance does not exist.
