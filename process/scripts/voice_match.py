#!/usr/bin/env python3
"""voice_match.py — post-production voice loudness matcher (owner 2026-10-29:
Analayo generally quieter than the TTS guide; fix in mastering, not by ear).

Method (automatic, no hand-tuning):
1. For each section mp3 + manifest timeline, collect per-role ranges
   (fish/question + plain = GUIDE voice; analayo = ARCHIVE voice).
2. Concat each role's ranges, measure integrated loudness (loudnorm dual-pass
   measure only).
3. Emit build/canon/voice_match.json {role: trim_db} that brings every role
   to the same target (TARGET_LUFS). render_a_essay.py reads it and applies
   the trims in the VOICE_AF_* chains — so every future render inherits it.
4. Re-run after render: all roles must land within TOL of target (proof).

Usage:
  python3 process/scripts/voice_match.py measure [outdir]  # print table + write JSON
  python3 process/scripts/voice_match.py check [outdir]    # verify a render (exit 1 on drift)
"""
import json
import os
import re
import subprocess
import sys

D = '/root/analayo-nibbana'
TARGET_LUFS = -16.0
TOL = 1.0


def measure(mp3_ranges):
    """mp3_ranges = [(mp3, [(t0, dur), ...])]. Returns integrated LUFS."""
    flt = []
    for mp3, ranges in mp3_ranges:
        for (a, d) in ranges:
            flt.append(f"aevalsrc=0:d={d:.2f}[sil{d:.0f}]" if False else None)
    # Build: trim each range, concat, loudnorm measure.
    parts, maps = [], []
    for i, (mp3, ranges) in enumerate(mp3_ranges):
        for j, (a, d) in enumerate(ranges):
            parts += ['-ss', str(a), '-to', str(a + d), '-i', mp3]
            maps += [f'[{len(maps)}:a]']
    if not maps:
        return None
    fc = ''.join(f'{m}aresample=44100,aformat=channel_layouts=mono[m{i}];'
                 for i, m in enumerate(maps))
    fc += ''.join(f'[m{i}]' for i in range(len(maps)))
    fc += f'concat=n={len(maps)}:v=0:a=1,loudnorm=print_format=json:dual_mono=true'
    p = subprocess.run(['ffmpeg', '-hide_banner'] + parts +
                       ['-filter_complex', fc, '-f', 'null', '-'],
                       capture_output=True, text=True)
    t = p.stdout + p.stderr
    m = re.search(r'\{[^{}]*"input_i"[^{}]*\}', t, re.S)
    assert m, 'loudnorm JSON missing:\n' + t[-2000:]
    return float(json.loads(m.group(0))['input_i'])


def collect(outdir, manifest):
    m = json.load(open(os.path.join(outdir, manifest)))
    guide, arch = [], []
    for sec, mm in m.items():
        if sec == 'stats' or not isinstance(mm, dict):
            continue
        mp3 = os.path.join(outdir, f'{sec}.mp3')
        if not os.path.exists(mp3):
            continue
        for e in mm.get('timeline', []):
            t = e.get('t')
            if t in ('fish', 'plain'):
                guide.append((mp3, [(e['t0'], e['dur'])]))
            elif t == 'analayo':
                arch.append((mp3, [(e['t0'], e['dur'])]))
    return guide, arch


def apply_trim(outdir, trim_db, manifest='manifest.json'):
    """Post-production voice match — NO re-render, NO TTS (2026-10-29).
    Applies the guide trim to fish/plain ranges only, via timeline-edit
    volume (single ffmpeg pass, sample-accurate, everything else untouched).
    Then re-runs loudnorm linear so the section keeps its integrated level
    (uniform gain: preserves the new relative match)."""
    m = json.load(open(os.path.join(outdir, manifest)))
    for sec in ['seed'] + [f's{n}' for n in range(1, 7)]:
        mm = m.get(sec)
        if not isinstance(mm, dict):
            continue
        mp3 = os.path.join(outdir, f'{sec}.mp3')
        conds = []
        for e in mm.get('timeline', []):
            if e.get('t') in ('fish', 'plain'):
                # escape commas: inside -af, ',' separates filters
                conds.append(f"between(t\\,{e['t0']:.2f}\\,{e['t0'] + e['dur']:.2f})")
        if not conds:
            continue
        en = '+'.join(f'({c})' for c in conds)
        tmp = mp3 + '.vm.mp3'
        r = subprocess.run(['ffmpeg', '-hide_banner', '-y', '-i', mp3,
                            '-af', f'volume={trim_db:+.1f}dB:enable={en}',
                            '-c:a', 'libmp3lame', '-b:a', '128k', tmp],
                           capture_output=True, text=True)
        assert r.returncode == 0, f'voice_match apply failed on {sec}:\n' + r.stderr[-1500:]
        # restore integrated level (uniform gain preserves the match)
        p1 = subprocess.run(['ffmpeg', '-hide_banner', '-y', '-i', tmp, '-af',
                             'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json',
                             '-f', 'null', '-'],
                            capture_output=True, text=True)
        mj = re.search(r'\{[^{}]*"input_i"[^{}]*\}', p1.stdout + p1.stderr, re.S)
        assert mj, f'loudnorm JSON missing on {sec}'
        measured = json.loads(mj.group(0))
        ln = 'loudnorm=I=-16:TP=-1.5:LRA=11:linear=true'
        for k in ('measured_I', 'measured_TP', 'measured_LRA',
                  'measured_thresh', 'offset'):
            src = {'measured_I': 'input_i', 'measured_TP': 'input_tp',
                   'measured_LRA': 'input_lr', 'measured_thresh': 'input_thresh',
                   'offset': 'target_offset'}[k]
            if src in measured:
                ln += f':{k}={measured[src]}'
        r2 = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp,
                             '-af', ln, '-c:a', 'libmp3lame', '-b:a', '128k', mp3],
                            capture_output=True, text=True)
        assert r2.returncode == 0, f'voice_match norm failed on {sec}'
        os.remove(tmp)
        print(f'{sec}: guide {trim_db:+.1f}dB on {len(conds)} ranges, re-normed', flush=True)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'measure'
    outdir = sys.argv[2] if len(sys.argv) > 2 else D + '/build/audio_newA'
    if mode == 'apply':
        # Post-production: apply trims directly to rendered mp3s (no TTS,
        # no re-render). Reads voice_match.json unless trim given.
        trim = float(sys.argv[3]) if len(sys.argv) > 3 else None
        if trim is None:
            trim = json.load(open(D + '/build/canon/voice_match.json'))['trims_db']['guide']
        apply_trim(outdir, trim)
        print('applied; re-run check to prove the gap closed')
        return
    manifest = 'manifest.json'
    guide, arch = collect(outdir, manifest)
    roles = {'guide': guide, 'archive': arch}
    want = {}
    print(f'== voice loudness ({outdir}) ==')
    for role, rr in roles.items():
        tot = sum(d for _, rr2 in rr for _, d in rr2)
        lufs = measure(rr)
        print(f'{role:8s} {tot:7.1f}s  {lufs:+.1f} LUFS')
        want[role] = lufs
    if mode == 'measure':
        trims = {r: round(TARGET_LUFS - v, 1) for r, v in want.items()}
        # Anchor: quietest role gets 0, others attenuate? No — anchor ARCHIVE
        # at 0 (untouched source of truth), move GUIDE to match it.
        base = 0.0
        trims = {'guide': round(want['archive'] - want['guide'], 1),
                 'archive': base}
        out = {'target': 'match-archive (source of truth, never touched)',
               'trims_db': trims,
               'measured': {r: round(v, 1) for r, v in want.items()},
               'why': 'owner 2026-10-29: one guide voice + archive must sit in one room; archive is the reference level'}
        p = D + '/build/canon/voice_match.json'
        json.dump(out, open(p, 'w'), indent=1)
        print(f'wrote {p}: {out["trims_db"]}')
    else:
        fails = [r for r, v in want.items() if abs(v - TARGET_LUFS) > TOL and r == 'guide']
        # check mode: guide must sit within TOL of archive (the reference)
        gap = abs(want['guide'] - want['archive'])
        print(f'gap guide-vs-archive: {gap:.1f} LU (tol {TOL})')
        sys.exit(1 if gap > TOL else 0)


if __name__ == '__main__':
    main()
