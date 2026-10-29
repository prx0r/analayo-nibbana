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

## The zoom order (one timeline per rung; bells mark thresholds, not depths)
- **0 SEED** = ALL SIX micro-sessions chained (build/canon/assembly_s0_seed.json,
  47 events, 4.5m rendered): question -> pause -> plain -> breath -> essay 0 -> archive voice, six times.
  The chain lives HERE — pronouns resolve because the Q->A pairs are
  adjacent. Then ZOOM bell into the full sections.
  No title, no intro. Straight into "This is peaceful, this is excellent."
- **ZOOM bell** → **A newA** = all 6 section As in order (21.6m speech, 27.4m
  rendered). §1 replays here — that's intentional:
  first hearing was the promise, second is the proof.
- **ZOOM bell** → **B** (53.1m speech, 57.9m rendered; curated subsets,
  each section opens with its A beats as a recap, then widens).
- **ZOOM bell** → **C** (121.0m; B-prefix + remainders + gold head-fill).
  D (260.7m) and the archive (pool, 20.7h) are NOT listening passes.
- **Close**: SEED reprise (motto only) + motto bell + 30s silence.
  The film ends where it began; it means something different now.

## Beat grammar (inside every section; durations from build/canon/rhythm.json)
1. RITUAL (the repetition IS the learning, process/12-ARGUMENT.md):
   MOTTO bell → KID asks the section question ("What is Nibbana?") →
   5s recollect (U1) / 3s (U2–U6; the listener tries to answer first) →
   OLD MAN gives the plain-English response (word-pause marks where mapped) →
   5s breath → ESSAY 0 on screen (verbatim + plain english — the compressed
   answer) → the archive voice answers it (the motif). A human intro,
   if used, comes AFTER the answer, never between question and motto.
   Beats then run the fixed stack: verbatim on screen → Analayo clip.
2. Per beat: Nanananda verbatim on screen → breath (beat_breath) →
   [term drops if Pali is heard] → Analayo clip plays
   → scaled water (beat_water_base +1s/60s, cap).
   (Beat plains live ON SCREEN only in newA; the Fish-plain line below is
   the p0-era shape, kept as history.)
3. Internal motto refrains get the motto bell, never the zoom bell.
   The two bells never sound within 30s of each other.

## Assembly manifests
`build/canon/assembly_sN.json`: ordered event lists —
{motto-bell, fish(question), pause(recollect), human-intro(pending), Analayo cold-open} [{verbatim on screen, fish (plain English), breath, [fish-terms], analayo, water} per beat] {zoom-bell at section end, except §6 → {seed reprise,
motto-bell, silence}}. `build/assets/motto-bell.wav`,
`build/assets/zoom-bell.wav`. Human intros referenced from
`build/canon/human-scripts.md` (recorded separately, dropped in).
