"""Render the A essay (seed + S1-S6) to mp3 with the full ritual.

Voices: Fish (espeak-ng, flat/mechanical) · Nyananda (sermon slices via
verbatim_audio_v1.json, espeak placeholder where score<0.40) · Analayo
(lecture slices, exact). Bells + pauses/breath/water as built.
seed-reprise = the 6 essay-0 Analayo windows in seed order. human-intro skipped.

Out: build/audio_v1/{seed,s1..s6}.mp3 + full_a_essay.mp3 + manifest.json
Caches slices/vox in build/audio_v1/cache/.
"""
import json
import re
import hashlib
import subprocess
from pathlib import Path

D = Path('/root/analayo-nibbana')
BUILD = D / 'build'
SR = 44100
FISH_RATE = 150  # wpm, flat
ESSAY0 = {1: 1, 2: 1, 3: 5, 4: 2, 5: 3, 6: 1}  # script clip per section (mirror make_assembly)

# Draft rule (owner 2026-10-26): NO PLAIN in this draft — verbatim -> Analayo
# directly. Fish keeps questions only; beat plain lines + term drops skipped.
NO_PLAIN = True

# p0 (owner 2026-10-26): essay-A proof draft with NO BELLS — timing/voice
# check only. Bells return in p1. Output goes to build/audio_p0/ so the
# belled build/audio_v1/ is untouched.
P0_NO_BELLS = True

# Essay-0 direct (owner 2026-10-26): at essay-0 positions (seed units +
# section openers) play Q -> ANALAYO answer directly, skipping the
# sermon-reader verbatim there. Hearing the motto twice back-to-back
# (reader, then Analayo) is redundant; the archive voice answers the
# question. Beat verbatims inside sections keep the sermon voice.
DIRECT_ESSAY0 = True
OUT = BUILD / ('audio_p0' if P0_NO_BELLS else 'audio_v1')
CACHE = OUT / 'cache'

# Voice-match chain (owner 2026-10-26): Analayo lectures (44.1k stereo,
# ~-20 LUFS) vs sermon readings (22k mono, ~-18.5 LUFS, hotter peaks) get
# the IDENTICAL chain so both voices land in the same profile. Bump VTAG
# whenever the chain changes — it enters the slice hash and busts the cache.
#
# 2026-10-26 P0 lesson (user's ear): afade=t=out:st=0 fades to zero at 30ms
# and STAYS silent — every slice was a blip. Fade-out MUST start at
# (duration-0.03), computed per slice. Never st=0 on a fade-out again.
VTAG = 'normv3'
VOICE_AF = ('highpass=f=80,lowpass=f=12000,'
            'acompressor=threshold=-18dB:ratio=2:attack=20:release=200,'
            'loudnorm=I=-19:TP=-1.5:LRA=11')

LECT = {n: (D / f'analayo-nibbana-lecture-{n:02d}.mp3') for n in range(1, 34)}
SERM = {n: (D / 'sermon-audio' / f'Nibbana_Stilled_{n:02d}.mp3') for n in range(1, 34)}


def run(*a):
    subprocess.run(a, check=True, capture_output=True)


def fade_tail(dur):
    """Fade-out starting at (dur-0.03). afade=t=out:st=0 fades to zero and
    STAYS silent — never st=0 on a fade-out (2026-10-26: every slice was
    a blip, user's ear caught it)."""
    return f'afade=t=in:st=0:d=0.03,afade=t=out:st={max(0.0, dur - 0.03):.2f}:d=0.03'


def assert_audible(path, what):
    """Render-time content check: fail loud on silent slices so a bad
    filter chain can never ship quiet files again (loudnorm masks it)."""
    p = subprocess.run(['ffmpeg', '-i', str(path), '-af', 'volumedetect',
                        '-f', 'null', '-'],
                       capture_output=True, text=True)
    m = re.search(r'max_volume:\s*(-inf|[-0-9.]+)', p.stdout + p.stderr)
    peak = float(m.group(1)) if m and m.group(1) != '-inf' else float('-inf')
    if not (peak > -60.0):
        raise SystemExit(f'SILENT SLICE: {what} -> {path} (peak {peak} dB)')


def uni_wav(src, ss, to, dst):
    dur = float(to) - float(ss)
    run('ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-to', str(to), '-i', str(src),
        '-ar', str(SR), '-ac', '1', '-c:a', 'pcm_s16le',
        '-af', VOICE_AF + ',' + fade_tail(dur), str(dst))
    assert_audible(dst, f'{src}[{ss}-{to}]')


def silence(dur, dst):
    run('ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i',
        f'anullsrc=r={SR}:cl=mono:d={dur}', '-c:a', 'pcm_s16le', str(dst))


def fish_wav(text, dst):
    """Fish Audio voice for questions (owner 2026-10-26: espeak robot out).
    FREE TIER ONLY — model pinned to s2.1-pro-free, abort anything else
    (owner: never spend credits). Default voice, flat delivery — Fish asks
    the question, never narrates. Key from $FISH_API_KEY, else
    characters/audition/.env (same key the audition build uses); the key
    is never written anywhere by this script. No silent fallback: API
    failure aborts the render instead of shipping robot voice (R5)."""
    import json as _json
    import os as _os
    import urllib.request as _url
    MODEL = 's2.1-pro-free'
    assert MODEL == 's2.1-pro-free', 'paid model blocked: never spend credits'
    key = (_os.getenv('FISH_API_KEY') or '').strip()
    if not key:
        for _ef in ('/root/characters/audition/.env',):
            try:
                for _ln in open(_ef).read().splitlines():
                    _ln = _ln.strip()
                    if _ln.startswith('FISH_API_KEY'):
                        key = _ln.split('=', 1)[1].strip()
            except FileNotFoundError:
                pass
    if not key:
        raise SystemExit('FISH_API_KEY missing — cannot voice questions')
    body = _json.dumps({'text': text, 'format': 'mp3'}).encode()
    req = _url.Request('https://api.fish.audio/v1/tts', data=body,
                       headers={'Authorization': f'Bearer {key}',
                                'Content-Type': 'application/json',
                                'model': MODEL})
    try:
        with _url.urlopen(req, timeout=120) as r:
            data = r.read()
    except Exception as e:
        raise SystemExit(f'fish tts failed for {text!r}: {e}')
    if len(data) < 2000:
        raise SystemExit(f'fish tts returned {len(data)}B for {text!r}')
    tmp = str(dst) + '.fish.mp3'
    Path(tmp).write_bytes(data)
    dp = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                         'format=duration', '-of', 'csv=p=0', tmp],
                        check=True, capture_output=True, text=True)
    dur = float(dp.stdout.strip())
    run('ffmpeg', '-v', 'error', '-y', '-i', tmp, '-ar', str(SR), '-ac', '1',
        '-c:a', 'pcm_s16le', '-af', VOICE_AF + ',' + fade_tail(dur), str(dst))
    Path(tmp).unlink()
    assert_audible(dst, f'fish:{text[:40]}')


def get_slice(kind, key, ss, to, src, text=''):
    h = hashlib.sha1(f'{VTAG}|fishs2|{kind}|{key}|{ss}|{to}|{text}'.encode()).hexdigest()[:12]
    dst = CACHE / f'{kind}_{h}.wav'
    if dst.exists() and dst.stat().st_size > 0:
        return dst
    if kind == 'vox':
        fish_wav(text, dst)
    elif kind == 'sil':
        silence(to, dst)
    else:
        uni_wav(src, ss, to, dst)
    return dst


ALIGN = {}
STATS = {'verbatim_aligned': 0, 'verbatim_placeholder': 0, 'fish_lines': 0}
ESSAY0_WINDOWS = []


def verbatim_wavs(s, clip, text, sermon):
    if isinstance(sermon, str):
        m0 = re.search(r'\d+', sermon)
        sermon = int(m0.group()) if m0 else None
    a = ALIGN.get((s, clip))
    txts = text if isinstance(text, list) else [text]
    out = []
    for i, t in enumerate(txts):
        p = a['parts'][i] if a and i < len(a['parts']) else {'t': None, 'end': None, 'score': 0.0}
        src_srm = p.get('sermon', sermon)  # aligner may relocate to the sermon that holds it
        if p['t'] is not None and p['score'] >= 0.40 and src_srm and src_srm in SERM:
            STATS['verbatim_aligned'] += 1
            out.append((get_slice('src', f'v{s}b{clip}p{i}', p['t'], p['end'], SERM[src_srm]),
                        f'sermon{src_srm} {p["t"]}-{p["end"]} score={p["score"]}'))
        else:
            STATS['verbatim_placeholder'] += 1
            out.append((get_slice('vox', f'v{s}b{clip}p{i}', 0, 0, None, t),
                        f'placeholder S{s}B{clip}p{i} score={p["score"]}'))
    return out


def render_section(n, events, tag):
    wavs, log = [], []
    for i, e in enumerate(events):
        t = e['t']
        if t in ('motto-bell', 'zoom-bell'):
            if P0_NO_BELLS:
                log.append(f'{t} SKIPPED (p0: no bells)')
                continue
            wavs.append(CACHE / f'{t}.wav')
            log.append(t)
        elif t in ('pause', 'breath', 'water', 'silence'):
            wavs.append(get_slice('sil', f'{t}{e["dur"]}', 0, e['dur'], None))
            log.append(f'{t} {e["dur"]}s')
        elif t == 'fish':
            if NO_PLAIN and e.get('role') != 'question':
                STATS['plain_skipped'] = STATS.get('plain_skipped', 0) + 1
                log.append(f'plain SKIPPED (draft: no plain): {e.get("say", "")[:60]}')
                continue
            STATS['fish_lines'] += 1
            say = e.get('say', '')
            wavs.append(get_slice('vox', f'f{n}', 0, 0, None, say))
            log.append(f'fish: {say[:60]}')
        elif t == 'fish-term':
            if NO_PLAIN:
                STATS['plain_skipped'] = STATS.get('plain_skipped', 0) + 1
                log.append(f'fish-term SKIPPED (draft: no plain): {e.get("say", "")}')
                continue
            STATS['fish_lines'] += 1
            wavs.append(get_slice('vox', f'ft{n}', 0, 0, None, e.get('say', '')))
            log.append(f'fish-term: {e.get("say", "")}')
        elif t == 'analayo':
            wavs.append(get_slice('src', f'a{n}', e['start'], e['end'], LECT[e['lec']]))
            log.append(f'L{e["lec"]} {e["start"]}-{e["end"]}')
            if tag == 'seed':
                ESSAY0_WINDOWS.append((e['lec'], e['start'], e['end']))
        elif t == 'verbatim':
            if tag == 'seed':
                s, clip = e['unit'], ESSAY0[e['unit']]
            elif i == 3:
                s, clip = n, ESSAY0[n]  # opening essay-0 (event order: bell,fish,pause,verbatim)
            else:
                nxt = next(x for x in events[i + 1:] if x['t'] == 'fish' and 'beat' in x)
                s, clip = n, nxt['beat']
            if DIRECT_ESSAY0 and (tag == 'seed' or i == 3):
                STATS['essay0_direct'] = STATS.get('essay0_direct', 0) + 1
                log.append(f'essay-0 DIRECT: Q -> Analayo (sermon reader skipped at S{s}B{clip})')
                continue
            for w, note in verbatim_wavs(s, clip, e.get('text', ''), e.get('sermon')):
                wavs.append(w)
                log.append('verbatim ' + note)
        elif t == 'human-intro':
            log.append('human-intro SKIPPED (owner slot)')
        elif t == 'seed-reprise':
            for j, (lec, ss, ee) in enumerate(ESSAY0_WINDOWS):
                wavs.append(get_slice('src', 'reprise', ss, ee, LECT[lec]))
                log.append(f'reprise essay-0 U{j + 1}: L{lec} {ss}-{ee}')
        else:
            log.append(f'UNKNOWN {t} SKIPPED')
    lst = OUT / f'{tag}.lst'
    lst.write_text(''.join(f"file '{w}'\n" for w in wavs))
    wav = OUT / f'{tag}.wav'
    run('ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(lst),
        '-c:a', 'pcm_s16le', str(wav))
    mp3 = OUT / f'{tag}.mp3'
    run('ffmpeg', '-v', 'error', '-y', '-i', str(wav), '-af',
        'loudnorm=I=-16:TP=-1.5:LRA=11', '-c:a', 'libmp3lame', '-b:a', '128k', str(mp3))
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                                'format=duration', '-of', 'csv=p=0', str(mp3)],
                               check=True, capture_output=True, text=True).stdout.strip())
    print(f'{tag}: {dur / 60:.1f}min {len(events)} events', flush=True)
    return mp3, dur, log


def main():
    global ALIGN
    OUT.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    for b in ('motto-bell', 'zoom-bell'):
        dst = CACHE / f'{b}.wav'
        if not dst.exists():
            run('ffmpeg', '-v', 'error', '-y', '-i', str(BUILD / 'assets' / f'{b}.wav'),
                '-ar', str(SR), '-ac', '1', '-c:a', 'pcm_s16le', str(dst))
    ALIGN = {(e['s'], e['clip']): e for e in
             json.loads((BUILD / 'verbatim_audio_v1.json').read_text())}
    asm = {0: json.loads((BUILD / 'assembly_s0_seed.json').read_text())}
    asm.update({n: json.loads((BUILD / f'assembly_s{n}.json').read_text()) for n in range(1, 7)})

    manifest, files = {}, {}
    mp3, dur, log = render_section(0, asm[0], 'seed')
    files['seed'] = mp3
    manifest['seed'] = {'min': round(dur / 60, 2), 'log': log}
    for n in range(1, 7):
        mp3, dur, log = render_section(n, asm[n], f's{n}')
        files[f's{n}'] = mp3
        manifest[f's{n}'] = {'min': round(dur / 60, 2), 'log': log}
    lst = OUT / 'full.lst'
    lst.write_text(''.join(f"file '{files[t]}'\n" for t in ['seed'] + [f's{n}' for n in range(1, 7)]))
    run('ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(lst),
        '-c:a', 'copy', str(OUT / 'full_a_essay.mp3'))
    manifest['stats'] = STATS
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=1))
    print('STATS', STATS)


if __name__ == '__main__':
    main()
