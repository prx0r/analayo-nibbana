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
VTAG = 'normv4'
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


def room_wav(voice):
    """3s room tone of a voice for bridges. voice = ('lect',N) / ('serm',N)
    / ('fish',). Lectures/sermons: longest sub--45dB stretch (their own air);
    Fish synth has no room (digital floor) -> digital silence. Cached."""
    key = f'{voice[0]}{voice[1] if len(voice) > 1 else ""}'
    h = hashlib.sha1(f'{VTAG}|room|{key}'.encode()).hexdigest()[:12]
    dst = CACHE / f'room_{h}.wav'
    if dst.exists() and dst.stat().st_size > 0:
        return dst
    if voice[0] == 'fish':
        silence(3.0, dst)
        return dst
    src = LECT[voice[1]] if voice[0] == 'lect' else SERM[voice[1]]
    p = subprocess.run(['ffmpeg', '-i', str(src), '-af',
                        'silencedetect=noise=-45dB:d=1.0', '-f', 'null', '-'],
                       capture_output=True, text=True)
    t = p.stdout + p.stderr
    starts = [float(x) for x in re.findall(r'silence_start:\s*([0-9.]+)', t)]
    ends = [float(x) for x in re.findall(r'silence_end:\s*([0-9.]+)', t)]
    spans = sorted(zip(starts, ends), key=lambda z: z[1] - z[0], reverse=True)
    loop = ''
    if spans and spans[0][1] - spans[0][0] >= 3.2:
        # cut INSIDE a long quiet span (clamped — never bleed speech in)
        a, b = spans[0]
        mid = (a + b) / 2
        ss, to = round(mid - 1.5, 2), round(mid + 1.5, 2)
    elif spans and spans[0][1] - spans[0][0] >= 1.0:
        # short span: tile it to 3s (loop click lives at room floor;
        # ears judge per the regression prompt)
        a, b = spans[0]
        ss, to, loop = round(a + 0.1, 2), round(b - 0.1, 2), ',aloop=loop=-1:size=2e9,atrim=0:3'
    else:
        ss, to = 0.0, 3.0
    # NOTE: rooms keep NATURAL level (no loudnorm — normalizing room hiss
    # to speech level peaked at -6.9dB; beds must sit ~30dB under speech).
    if loop:
        run('ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-to', str(to),
            '-i', str(src), '-ar', str(SR), '-ac', '1', '-c:a', 'pcm_s16le',
            '-af', 'aloop=loop=-1:size=2e9,atrim=0:3', str(dst))
    else:
        run('ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-to', str(to),
            '-i', str(src), '-ar', str(SR), '-ac', '1', '-c:a', 'pcm_s16le', str(dst))
    return dst


def bridge_wav(dur, srcA, srcB):
    """Gap bed where two rooms meet (adapted vatulanatha #4): first half
    srcA's room, second half srcB's, 80ms crossfade — the voice change
    arrives on continuous air instead of a floor-cliff. Same source both
    sides: that source's room throughout."""
    h = hashlib.sha1(
        f'{VTAG}|bridge|{dur}|{srcA}|{srcB}'.encode()).hexdigest()[:12]
    dst = CACHE / f'bridge_{h}.wav'
    if dst.exists() and dst.stat().st_size > 0:
        return dst
    ra, rb = room_wav(srcA), room_wav(srcB)
    half = round(dur / 2 + 0.04, 2)  # acrossfade eats 0.08 overlap -> total dur
    run('ffmpeg', '-v', 'error', '-y', '-i', str(ra), '-i', str(rb),
        '-filter_complex',
        f'[0:a]atrim=0:{half},asetpts=PTS-STARTPTS[a];'
        f'[1:a]atrim=0:{half},asetpts=PTS-STARTPTS[b];'
        f'[a][b]acrossfade=d=0.08[out]',
        '-map', '[out]', '-ar', str(SR), '-ac', '1', '-c:a', 'pcm_s16le', str(dst))
    return dst


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
manifest_timeline = {}


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


def verbatim_slot(events, i, e, tag, n):
    """Resolve (s, clip) for a verbatim event (shared by render + voice-id)."""
    if tag == 'seed':
        return e['unit'], ESSAY0[e['unit']]
    if i == 3:
        return n, ESSAY0[n]  # opening essay-0 (event order: bell,fish,pause,verbatim)
    nxt = next(x for x in events[i + 1:] if x['t'] == 'fish' and 'beat' in x)
    return n, nxt['beat']


def voice_after(events, i, tag, n):
    """Next rendered voice past skips: ('lect',N)/('serm',N)/('fish',)/None.
    Sermon number prefers the aligner's relocation, else the script tag."""
    for j in range(i + 1, len(events)):
        x = events[j]
        xt = x['t']
        if xt == 'analayo':
            return ('lect', x['lec'])
        if xt == 'fish' and (not NO_PLAIN or x.get('role') == 'question'):
            return ('fish',)
        if xt == 'verbatim':
            s, clip = verbatim_slot(events, j, x, tag, n)
            if DIRECT_ESSAY0 and (tag == 'seed' or j == 3):
                continue
            a = ALIGN.get((s, clip))
            if not a:
                continue
            srm = x.get('nanananda_sermon', x.get('sermon'))
            if isinstance(srm, str):
                m0 = re.search(r'\d+', srm or '')
                srm = int(m0.group()) if m0 else None
            for p in a['parts']:
                if p.get('sermon'):
                    srm = p['sermon']
                    break
            if srm in SERM:
                return ('serm', srm)
            return None
        if xt == 'seed-reprise':
            return ('lect', ESSAY0_WINDOWS[0][0]) if ESSAY0_WINDOWS else None
        if xt in ('motto-bell', 'zoom-bell') and not P0_NO_BELLS:
            return None  # bells carry no voice; boundary resets past them
    return None


def render_section(n, events, tag):
    prev_voice = [None]  # last rendered voice (bridges meet in the middle)
    wavs, log, kinds = [], [], []
    for i, e in enumerate(events):
        t = e['t']
        if t in ('motto-bell', 'zoom-bell'):
            if P0_NO_BELLS:
                log.append(f'{t} SKIPPED (p0: no bells)')
                continue
            wavs.append(CACHE / f'{t}.wav')
            kinds.append(t)
            log.append(t)
        elif t in ('pause', 'breath', 'water', 'silence'):
            nxt = voice_after(events, i, tag, n)
            prv = prev_voice[0]
            if prv is not None and nxt is not None:
                wavs.append(bridge_wav(e['dur'], prv, nxt))
                kinds.append(t)
                log.append(f'{t} {e["dur"]}s bridge {prv}->{nxt}')
            else:
                wavs.append(get_slice('sil', f'{t}{e["dur"]}', 0, e['dur'], None))
                kinds.append(t)
                log.append(f'{t} {e["dur"]}s')
        elif t == 'fish':
            if NO_PLAIN and e.get('role') != 'question':
                STATS['plain_skipped'] = STATS.get('plain_skipped', 0) + 1
                log.append(f'plain SKIPPED (draft: no plain): {e.get("say", "")[:60]}')
                continue
            STATS['fish_lines'] += 1
            say = e.get('say', '')
            wavs.append(get_slice('vox', f'f{n}', 0, 0, None, say))
            kinds.append('fish')
            prev_voice[0] = ('fish',)
            log.append(f'fish: {say[:60]}')
        elif t == 'fish-term':
            if NO_PLAIN:
                STATS['plain_skipped'] = STATS.get('plain_skipped', 0) + 1
                log.append(f'fish-term SKIPPED (draft: no plain): {e.get("say", "")}')
                continue
            STATS['fish_lines'] += 1
            wavs.append(get_slice('vox', f'ft{n}', 0, 0, None, e.get('say', '')))
            kinds.append('fish-term')
            log.append(f'fish-term: {e.get("say", "")}')
        elif t == 'analayo':
            wavs.append(get_slice('src', f'a{n}', e['start'], e['end'], LECT[e['lec']]))
            kinds.append('analayo')
            prev_voice[0] = ('lect', e['lec'])
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
            vw = []
            for w, note in verbatim_wavs(s, clip, e.get('text', ''), e.get('sermon')):
                wavs.append(w)
                kinds.append('verbatim')
                vw.append(w)
                log.append('verbatim ' + note)
            a = ALIGN.get((s, clip))
            srm = e.get('nanananda_sermon', e.get('sermon'))
            if isinstance(srm, str):
                m0 = re.search(r'\d+', srm or '')
                srm = int(m0.group()) if m0 else None
            if a and a['parts'] and a['parts'][0].get('sermon'):
                srm = a['parts'][0]['sermon']
            prev_voice[0] = ('serm', srm) if srm in SERM else None
        elif t == 'human-intro':
            log.append('human-intro SKIPPED (owner slot)')
        elif t == 'seed-reprise':
            for j, (lec, ss, ee) in enumerate(ESSAY0_WINDOWS):
                wavs.append(get_slice('src', 'reprise', ss, ee, LECT[lec]))
                kinds.append('seed-reprise')
                log.append(f'reprise essay-0 U{j + 1}: L{lec} {ss}-{ee}')
            prev_voice[0] = ('lect', ESSAY0_WINDOWS[-1][0]) if ESSAY0_WINDOWS else None
        else:
            log.append(f'UNKNOWN {t} SKIPPED')
    assert len(kinds) == len(wavs), f'{tag}: kinds/wavs drift'
    tl = []
    t0 = 0.0
    for k, w in zip(kinds, wavs):
        dp = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                             'format=duration', '-of', 'csv=p=0', str(w)],
                            check=True, capture_output=True, text=True)
        d = float(dp.stdout.strip())
        tl.append({'t': k, 't0': round(t0, 2), 'dur': round(d, 2)})
        t0 += d
    manifest_timeline[tag] = tl
    lst = OUT / f'{tag}.lst'
    lst.write_text(''.join(f"file '{w}'\n" for w in wavs))
    wav = OUT / f'{tag}.wav'
    run('ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(lst),
        '-c:a', 'pcm_s16le', str(wav))
    mp3 = OUT / f'{tag}.mp3'
    # Dual-pass loudnorm (2026-10-26 ear-fix): single-pass DYNAMIC mode
    # rides gain up inside quiet beds (room bridges pumped ~20dB, pause
    # grammar audibly flattened). Measured pass first, then LINEAR gain —
    # relative dynamics (speech vs stillness) preserved exactly.
    # Pass 1 MUST run at default verbosity: loudnorm's measurement JSON
    # prints at info level and `-v error` hides it (2026-10-26: silent
    # fallback to dynamic mode re-pumped the beds).
    p1 = subprocess.run(['ffmpeg', '-y', '-i', str(wav), '-af',
                         'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json',
                         '-f', 'null', '-'],
                        check=True, capture_output=True, text=True)
    m = re.search(r'\{[^{}]*"input_i"[^{}]*\}', p1.stderr, re.S)
    measured = json.loads(m.group(0)) if m else {}
    ln = (f'loudnorm=I=-16:TP=-1.5:LRA=11:linear=true')
    for k in ('measured_I', 'measured_TP', 'measured_LRA', 'measured_thresh',
              'offset'):
        src = {'measured_I': 'input_i', 'measured_TP': 'input_tp',
               'measured_LRA': 'input_lra', 'measured_thresh': 'input_thresh',
               'offset': 'target_offset'}[k]
        if src in measured:
            ln += f':{k}={measured[src]}'
    run('ffmpeg', '-v', 'error', '-y', '-i', str(wav), '-af', ln,
        '-c:a', 'libmp3lame', '-b:a', '128k', str(mp3))
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
    manifest['seed'] = {'min': round(dur / 60, 2), 'log': log,
                        'timeline': manifest_timeline['seed']}
    for n in range(1, 7):
        mp3, dur, log = render_section(n, asm[n], f's{n}')
        files[f's{n}'] = mp3
        manifest[f's{n}'] = {'min': round(dur / 60, 2), 'log': log,
                             'timeline': manifest_timeline[f's{n}']}
    lst = OUT / 'full.lst'
    lst.write_text(''.join(f"file '{files[t]}'\n" for t in ['seed'] + [f's{n}' for n in range(1, 7)]))
    run('ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(lst),
        '-c:a', 'copy', str(OUT / 'full_a_essay.mp3'))
    manifest['stats'] = STATS
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=1))
    print('STATS', STATS)


if __name__ == '__main__':
    main()
