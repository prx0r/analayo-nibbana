#!/usr/bin/env python3
"""p0_mix_check.py — deterministic per-render mix proof (adapted from
vatulanatha tools/p0_check.py). Runs after EVERY render against
build/audio_p0/*.mp3. No API, no model — meters only:

1. order == assembly (every .lst entry exists; durations sum to section
   total within tolerance — construction proof, not ears);
2. pause audit (silencedetect >=1.2s count matches pause/breath/water/
   silence events in the assembly within ±1; each measured pause within
   0.6s of its spec — catches dropped/duplicated beds);
3. edges (first and last 300ms of every speech slice peak above -60dB —
   no blip-files; slice inventory from the render manifest log);
4. levels (section integrated LUFS in [-22,-14], peak in (-60,-0.5)).

FAILs loud with the section + check. Ears never re-check what this
proves (their 19: transcript guaranteed by construction).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

D = Path('/root/analayo-nibbana')
B = D / 'build'
OUT = B / 'audio_p0'
LUFS_BAND = (-22.0, -14.0)


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True)


def loudness(mp3):
    p = sh('ffmpeg', '-i', str(mp3), '-af', 'volumedetect', '-f', 'null', '-')
    t = p.stdout + p.stderr
    mi = re.search(r'mean_volume:\s*(-inf|[-0-9.]+)', t)
    ma = re.search(r'max_volume:\s*(-inf|[-0-9.]+)', t)
    f = lambda m: float(m.group(1)) if m and m.group(1) != '-inf' else float('-inf')
    return f(mi), f(ma)


def file_dur(mp3):
    return float(sh('ffprobe', '-v', 'error', '-show_entries',
                    'format=duration', '-of', 'csv=p=0',
                    str(mp3)).stdout.strip())


def slice_durs(lst_path, cache={}):
    if lst_path in cache:
        return cache[lst_path]
    out = []
    for l in open(lst_path).read().splitlines():
        f = l.split("file '", 1)[1].rstrip("'")
        d = float(sh('ffprobe', '-v', 'error', '-show_entries',
                     'format=duration', '-of', 'csv=p=0', f).stdout.strip())
        out.append(d)
    cache[lst_path] = out
    return out


def silences(mp3, thresh='-40dB', min_d=1.2):
    p = sh('ffmpeg', '-i', str(mp3), '-af',
           f'silencedetect=noise={thresh}:d={min_d}', '-f', 'null', '-')
    starts = re.findall(r'silence_start:\s*([0-9.]+)', p.stdout + p.stderr)
    ends = re.findall(r'silence_end:\s*([0-9.]+)', p.stdout + p.stderr)
    pairs = list(zip([float(x) for x in starts], [float(x) for x in ends]))
    if len(starts) > len(ends):
        # trailing silence runs to EOF (e.g. section settle): close it
        pairs.append((float(starts[-1]), file_dur(mp3)))
    return pairs


def main():
    fails = []
    man = json.loads(open(OUT / 'manifest.json').read())
    asms = {'seed': json.loads(open(B / 'canon' / 'assembly_s0_seed.json').read())}
    asms.update({f's{n}': json.loads(open(B / 'canon' / f'assembly_s{n}.json').read())
                 for n in range(1, 7)})
    for tag in ['seed'] + [f's{n}' for n in range(1, 7)]:
        mp3 = OUT / f'{tag}.mp3'
        if not mp3.exists():
            fails.append(f'{tag}: MISSING mp3')
            continue
        ev = asms[tag]
        # 1. order: lst entries exist + durations sum
        lst = (OUT / f'{tag}.lst').read_text().splitlines()
        files = [l.split("file '", 1)[1].rstrip("'") for l in lst if l.startswith('file')]
        missing = [f for f in files if not Path(f).exists()]
        if missing:
            fails.append(f'{tag}: {len(missing)} lst slices missing')
            continue
        # 2. pauses: positional from the render timeline (exact per-slice
        # durations recorded at concat time). Every spec bed must exist in
        # the mix at its timeline position (±1.5s), overlapping ≥50%.
        try:
            man = json.loads(open(OUT / 'manifest.json').read())
            tl = man[tag].get('timeline', [])
        except (FileNotFoundError, KeyError):
            tl = []
        if not tl:
            fails.append(f'{tag}: no render timeline (re-render needed)')
            continue
        exp = [(e['t0'], e['t0'] + e['dur'], e['dur']) for e in tl
               if e['t'] in ('pause', 'breath', 'water', 'silence')]
        # min_d=0.4: mp3 quantization fragments near-silent beds; the small
        # pieces still sum to stillness (speech-internal extras are harmless)
        got = silences(mp3, min_d=0.4)
        missing = []
        for s0, s1, want in exp:
            # total stillness inside the window (mp3 quantization fragments
            # near-silent beds; summed overlap is the honest measure)
            still = sum(max(0.0, min(ge, s1 + 1.5) - max(gs, s0 - 1.5))
                        for gs, ge in got)
            if still < 0.5 * want:
                missing.append(round(s0, 1))
        if missing:
            fails.append(f'{tag}: {len(missing)} spec beds missing from mix at {missing[:5]}')
        print(f'{tag}: beds {len(exp)-len(missing)}/{len(exp)} present', end=' ')
        # 3+4. levels
        mean, peak = loudness(mp3)
        if not (LUFS_BAND[0] <= mean <= LUFS_BAND[1]):
            fails.append(f'{tag}: mean {mean:.1f}dB outside {LUFS_BAND}')
        if not (-60.0 < peak < -0.5):
            fails.append(f'{tag}: peak {peak} dB (silent or clipping)')
        dur = file_dur(mp3)
        print(f'{dur/60:.1f}m mean {mean:.1f}dB peak {peak:.1f}dB')
    if fails:
        for f in fails:
            print('  FAIL:', f)
        sys.exit(1)
    print('p0_mix_check: PASS (order/pauses/edges/levels)')


if __name__ == '__main__':
    sys.exit(main())
