"""Measure per-voice octave-band energies to derive match EQ.

Voices: analayo (lecture mic, the reference), sermon (22k mono readings),
fish (synth Qs). Prints band means; EQ derived by hand from output
(owner ear is the judge; meters only propose).
Usage: python3 process/scripts/voice_spectrum.py
"""
import glob
import subprocess

D = '/root/analayo-nibbana'
BANDS = [125, 250, 500, 1000, 2000, 4000, 8000]


def band_level(path, f, ss=None, t=None):
    cmd = ['ffmpeg']
    if ss is not None:
        cmd += ['-ss', str(ss), '-t', str(t)]
    cmd += ['-i', path, '-ar', '44100', '-ac', '1', '-af',
            f'bandpass=f={f}:width_type=o:w=1,volumedetect', '-f', 'null', '-']
    p = subprocess.run(cmd, capture_output=True, text=True)
    for line in (p.stdout + p.stderr).splitlines():
        if 'mean_volume' in line:
            return float(line.split('mean_volume:')[1].split('dB')[0])
    return float('nan')


SETS = {
    'analayo': [(f'{D}/analayo-nibbana-lecture-01.mp3', 3000, 60),
                (f'{D}/analayo-nibbana-lecture-10.mp3', 1700, 60),
                (f'{D}/analayo-nibbana-lecture-05.mp3', 410, 60)],
    'sermon': [(f'{D}/sermon-audio/Nibbana_Stilled_01.mp3', 60, 60),
               (f'{D}/sermon-audio/Nibbana_Stilled_15.mp3', 300, 60),
               (f'{D}/sermon-audio/Nibbana_Stilled_25.mp3', 100, 60)],
    'fish': [(f, None, None)
             for f in sorted(glob.glob(f'{D}/build/audio_p0/cache/vox_*.wav'))],
}


def main():
    print(f"{'voice':8s}" + ''.join(f'{b:>8d}' for b in BANDS))
    for voice, files in SETS.items():
        row = []
        for f in BANDS:
            vals = [band_level(p, f, ss, t) for p, ss, t in files]
            vals = [v for v in vals if v == v]
            row.append(sum(vals) / len(vals))
        print(f"{voice:8s}" + ''.join(f'{v:>8.1f}' for v in row))


if __name__ == '__main__':
    main()
