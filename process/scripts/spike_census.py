"""Census of spikes/coughs/clips in newA + seed Analayo windows.

For each window: peak + mean (volumedetect) + crest. Flags:
  CLIP if peak > -3dB, BURST if crest > 20dB (cough candidate).
Speech reference: lecture mean ≈ -23dB raw. Coughs read as short,
broadband, 10dB+ over local speech. Output guides duck/cut calls;
nothing is modified here.
Usage: python3 process/scripts/spike_census.py
"""
import json
import subprocess
from pathlib import Path

D = Path('/root/analayo-nibbana')
B = D / 'build' / 'canon'


def stats(src, ss, to):
    p = subprocess.run(
        # NOTE: no -v error — volumedetect prints at info level and
        # -v error hides it (same trap as the loudnorm JSON, ledger #3).
        ['ffmpeg', '-ss', str(max(0, ss - 1)), '-t',
         str(to - ss + 2), '-i', str(src), '-ar', '44100', '-ac', '1',
         '-af', 'volumedetect', '-f', 'null', '-'],
        capture_output=True, text=True)
    vals = {}
    for line in (p.stdout + p.stderr).splitlines():
        for k in ('mean_volume', 'max_volume'):
            if k in line:
                try:
                    vals[k] = float(line.split(f'{k}:')[1].split('dB')[0])
                except ValueError:
                    pass
    return vals


def main():
    man = json.loads((B / 'newA_manifest.json').read_text())
    wins = []
    seed = json.loads((B / 'assembly_s0_seed.json').read_text())
    for e in seed:
        if e['t'] == 'analayo':
            wins.append(('seed', e['lec'], e['start'], e['end']))
    for n in range(1, 7):
        sec = man['sections'][str(n)]
        for u in [sec['pointer']] + sec['beats']:
            a = u['analayo']
            wins.append((f'S{n}b{u["beat"]}', a['lec'], a['start'], a['end']))
    print(f'{len(wins)} windows')
    for tag, lec, ss, to in wins:
        v = stats(D / f'sources/lectures/audio/analayo-nibbana-lecture-{lec:02d}.mp3', ss, to)
        peak, mean = v.get('max_volume', -99), v.get('mean_volume', -99)
        crest = peak - mean
        flag = ('CLIP' if peak > -3 else '') + ('BURST' if crest > 20 else '')
        print(f'{tag:6s} L{lec:02d} [{ss:.0f}-{to:.0f}] '
              f'peak {peak:6.1f} mean {mean:6.1f} crest {crest:5.1f} {flag}',
              flush=True)


if __name__ == '__main__':
    main()
