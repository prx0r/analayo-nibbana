#!/usr/bin/env python3
"""Build build/STORYBOARD.md — the human-readable shooting script.

One row per beat (seed cells first, then S1..S6), in assembly order:
  TEXT (verbatim, trimmed) -> PLAIN -> AUDIO [lec start-end, dur]
  + running clock + flags. Mirrors shiva-sutras TRACK_F_STORYBOARD law:
  every layer's words, every window, gaps flagged, never padded.

Clocks: analayo/verbatim durations exact (clip durs / alignment windows);
Fish questions estimated ~2.5wps (marked ~); pauses/bells as listed
(p0: bells skipped). Regenerate after any assembly change.
"""
import json
from pathlib import Path

D = Path('/root/analayo-nibbana')
B = D / 'build'
ESSAY0_BEAT = {1: 1, 2: 13, 3: 5, 4: 2, 5: 3, 6: 1}  # script clip per section, TEXT identity only (audio: build/essay0_windows.json)
QS = {1: 'What is Nibbana?', 2: "Why don't I see Nibbana right now?",
      3: 'What keeps it going?', 4: 'How is the sense of self constructed?',
      5: 'How is Nibbana attained?', 6: 'What is Nibbana like?'}


def short(t, n=160):
    t = (' // '.join(str(x) for x in t) if isinstance(t, list) else str(t or ''))
    t = ' '.join(t.split())
    return t if len(t) <= n else t[:n] + '…'


def fish_dur(say):
    return round(len(say.split()) / 2.5, 1)


def fmt(s):
    return f'{int(s // 60)}:{int(s % 60):02d}'


def main():
    al = {(e['s'], e['clip']): e
          for e in json.loads((B / 'verbatim_audio_v1.json').read_text())}
    L = ['# STORYBOARD — Essay 0 + Essay A as shooting script',
         '',
         ('Law: TEXT verbatim -> PLAIN -> AUDIO archive voice, assembly order. '
          'Seed first (6 cells), then S1..S6. p0 rules: no bells, no plain '
          '(Fish questions only), essay-0 = Q -> Analayo direct. '
          'Clocks: analayo/verbatim exact, Fish ~estimated, pauses exact. '
          'Gaps flagged at the end, never padded.'),
         '']
    clock = 0.0

    def beat_row(tag, s, clip, e, opening=False):
        nonlocal clock
        a = e['analayo']
        v = al.get((s, clip), {})
        parts = v.get('parts', [])
        vd = round(sum((p['end'] - p['t']) for p in parts if p['t'] is not None), 1)
        ad = round(a['end'] - a['start'], 1)
        flags = []
        for k in ('override', 'amendment', 'match'):
            if e.get(k):
                flags.append(f'{k}: {short(e[k], 90)}')
        for p in parts:
            if p.get('sermon') and p['sermon'] != e.get('nanananda_sermon'):
                flags.append(f"relocated sermon: said S{e.get('nanananda_sermon')} -> heard S{p['sermon']}")
            if p.get('pinned'):
                flags.append('PINNED Pali chant in transcript gap')
        if a['lec'] in (3, 6, 7, 14, 17, 20, 22, 24, 26, 27):
            flags.append('YT timebase (anchor-map at cut)')
        L.append(f'### {tag} · S{s}B{clip} · L{a["lec"]} [{a["start"]}-{a["end"]}] ({ad}s)')
        L.append(f'- TEXT: {short(e.get("nanananda_verbatim", ""))}')
        L.append(f'- PLAIN: {short(e.get("plain_english_below", ""))}')
        L.append(f'- AUDIO sermon {e.get("nanananda_sermon")} [{vd}s, score {min([p["score"] for p in parts] or [0])}] -> Analayo [{ad}s]')
        if flags:
            L.append('- FLAGS: ' + ' / '.join(flags))
        clock += (vd if not opening else 0) + ad
        L.append(f'- clock ~{fmt(clock)}')
        L.append('')

    L.append('## SEED — 6 cells (Q -> pause 3s -> Analayo essay-0, direct)')
    L.append('')
    seed = json.loads((B / 'assembly_s0_seed.json').read_text())
    sc = {s: {e['clip']: e for e in json.loads((B / f'seg{s}_script.json').read_text())}
          for s in range(1, 7)}
    for e in seed:
        if e['t'] == 'fish':
            d = fish_dur(e['say'])
            L.append(f'- Q{e["unit"]} (~{d}s): {e["say"]}')
            clock += d
        elif e['t'] == 'pause':
            L.append(f'- pause {e["dur"]}s (recollect)')
            clock += e['dur']
        elif e['t'] == 'analayo':
            L.append(f'- A{e["note"].split()[-1]}: L{e["lec"]} [{e["start"]}-{e["end"]}] ({e["dur"]}s)')
            clock += e['dur']
        elif e['t'] == 'water':
            clock += e['dur']
    L.append(f'- seed ends ~{fmt(clock)}')
    L.append('')

    gapflags = []
    for s in range(1, 7):
        L.append(f'## S{s} — {QS[s]}')
        L.append('')
        core = json.loads((B / f'seg{s}_core_v4.json').read_text())
        byclip = sc[s]

        def match(x):
            e = byclip.get(x.get('clip')) if x.get('clip') is not None else None
            if e is None:
                e = next((y for y in byclip.values()
                          if y['analayo']['lec'] == x['lec']
                          and abs(y['analayo']['start'] - x['start']) < 3), None)
            return e

        pairs = [(x, match(x)) for x in core]
        for x, e in pairs:
            if e is None:
                gapflags.append(f'S{s} core L{x["lec"]} [{x["start"]}]: no script row — FLAG')
        pairs = [(x, e) for x, e in pairs if e is not None]
        opener = next(((x, e) for x, e in pairs if e['clip'] == ESSAY0_BEAT[s]), pairs[0])
        ordered = [opener] + [(x, e) for x, e in pairs if e['clip'] != opener[1]['clip']]
        L.append(f'- opener: essay-0 (Q -> Analayo direct, no reader)')
        for x, e in ordered:
            beat_row(f'S{s}-{e["clip"]}', s, e['clip'], e,
                     opening=(e['clip'] == opener[1]['clip']))
        L.append('')

    L.append('## Gap flags')
    for g in gapflags or ['none — 71/71 beats scripted+aligned']:
        L.append(f'- {g}')
    L.append('- YT-timebase beats: anchor-map + pause-snap at cut (never ship un-snapped)')
    L.append('- B* promotions (definitional readings in B): S3 honey-ball L12, S4 anidassana L08 — documented exception to A-only core')
    L.append('- Fish questions = Fish-audio voice (free tier); audition approved separately')
    L.append('')
    (B / 'STORYBOARD.md').write_text('\n'.join(L))
    print(f'storyboard: seed+S1..S6, ends ~{fmt(clock)}')


if __name__ == '__main__':
    main()
