# BELLS + ZOOM — the two sounds that hold the whole thing together.

## The two bells
- **Motto bell** (bright, ~2.5s decay): rings WITH "this is excellent".
  Every motto refrain — section cold opens, internal refrain returns.
  It says: *the theme, again, deeper now.*
- **Zoom bell** (low, ~6s decay + sub octave): rings on layer changes
  and section thresholds. It says: *we are going one level deeper* (or,
  at the end: *we have returned*). Longer, darker, never confused with
  the motto bell.

Both are synthesized (see `build/assets/`), same two sounds everywhere —
no library bells, no variation. Recognition IS the function.

## The zoom order (one timeline, four layers)
- **L0 SEED** = §1 core as cold open (~10 min Analayo + pads).
  No title, no intro. Straight into "This is peaceful, this is excellent."
- **ZOOM bell** → **L1 CORE** = all 6 section cores in order (~96 min
  Analayo + pads + human intros). §1 replays here — that's intentional:
  first hearing was the promise, second is the proof.
- **ZOOM bell** → **L2 GOLD** (6.3h, A-only spines, same cluster order).
  Each gold section opens with its core's beats as a recap, then widens.
- **ZOOM bell** → **L3 FULL** (20.7h pool, same order). The archive.
- **Close**: SEED reprise (motto only) + motto bell + 30s silence.
  The film ends where it began; it means something different now.

## Beat grammar (inside every section)
1. Human intro (section open only, ~40s, from `build/human-scripts.md`)
2. MOTTO bell + motto (cold open of every section)
3. Per beat: Nanananda verbatim on screen → Fish speaks the plain English
   → 1.5s breath → [term drops if Pali is heard] → Analayo clip plays
   → 2.5s water.
4. Internal motto refrains get the motto bell, never the zoom bell.
   The two bells never sound within 30s of each other.

## Assembly manifests
`build/assembly_sN.json`: ordered event lists —
{human-intro, pending} {motto-bell + Analayo cold-open (motto, no Fish first)} [{verbatim on screen, fish (plain English), breath, [fish-terms], analayo, water} per beat] {zoom-bell at section end, except §6 → {seed reprise,
motto-bell, silence}}. `build/assets/motto-bell.wav`,
`build/assets/zoom-bell.wav`. Human intros referenced from
`build/human-scripts.md` (recorded separately, dropped in).
