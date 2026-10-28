"""Render essays (seed + sections) to mp3 with the full ritual.

Voices: Fish Audio guide (questions + plain responses, flat) · Analayo
(lecture slices, exact; sermon-reader path retained for p0/p1 only).
Modes (module flags, one output dir each, never mixed): p0 draft
(audio_p0, no bells/plain), p1 (audio_p1, bells+sfx+YT offsets),
newA (audio_newA, uniform rhythm bell/Q/plain/Analayo, analayo-only).
Bells + pauses/breath/water as built.
seed-reprise = the essay-0 Analayo windows in seed order. human-intro skipped.

Out: build/<mode>/{seed,s1..s6}.mp3 + full mp3 + manifest.json (+cache/).
"""
import json
import re
import sys
import hashlib
import subprocess
from pathlib import Path

D = Path('/root/analayo-nibbana')
BUILD = D / 'build'
SR = 44100
FISH_RATE = 150  # wpm, flat
ESSAY0_BEAT = {1: 1, 2: 13, 3: 5, 4: 2, 5: 3, 6: 1}  # script clip per section, TEXT identity only.
# Canonical essay-0 AUDIO windows live in build/essay0_windows.json and ride
# inside assemblies (seed + section openers) — this file never defines windows
# (single-source rule, R6; deleted the duplicate 2026-10-26 pointers).

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

# p1 (2026-10-28, §69): bells back + sfx kit + YT anchor offsets.
# Driven by process/scripts/render_p1.py (sets P1=True, optionally
# P1_SEED_ONLY). Outputs NEVER mix: p0=audio_p0 (no bells),
# v1=audio_v1 (frozen 2026-10-26), p1=audio_p1.
P1 = False
P1_SEED_ONLY = False
YT_OFF = {}  # lec -> seconds (DS = YT - off); loaded from yt_anchor_map.json
# Windows already in DS timebase (§64 U5/c2/c3 repairs + §75 hunt beats
# measured in DS): never shift these.
DS_FIXED = {(14, 4406.0), (14, 4430.4),
            (14, 2487.0), (6, 1326.9), (20, 2378.7)}
# L20 drifts: per-window overrides only (constant forbidden, §69).
# (20,488.0)=S1b11 debt window: anchor @482 gives 8.7, window opens 488.
PERW = {(20, 488.0): 8.7}
SFX = BUILD / 'assets' / 'sfx'
# README gains (sfx/README.md strike map): bowls/ding +10dB, blocks -4dB.
SFX_GAIN = {'bowls_intro': 10, 'long_break_bell': 0, 'bell_ding': 10,
            'block_tick': -4, 'block_resonant': -4}
BREAK_DUR = 4.7  # long_break_bell.wav measured; refreshed at prep
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
#
# 2026-10-28 voice-match (owner ear: Fish denser/clearer, sermon muffled,
# same LUFS). Octave-band measures vs the Analayo reference: sermon +4dB
# at 250-500Hz and -2.8dB at 4k (boomy+dull); Fish +4-5dB at 1-2kHz
# (presence-hot). EQ trims both toward the reference before loudnorm
# (norm absorbs the gain shift). Script: process/scripts/voice_spectrum.py.
VTAG = 'normv6'
# Restoration (2026-10-28 owner ear: coughs/clips): adeclick (mouth
# clicks/ticks, save mode leaves clean samples untouched) + adeclip
# (reconstructs clipped peaks — lectures peak 0dB, census:
# process/scripts/spike_census.py). Before loudnorm so norm absorbs
# shifts. Long cough bursts mid-speech are NOT auto-fixed (would eat
# speech) — they get per-timestamp duck/cut + whisper re-verify (§57).
RESTORE = 'adeclick=t=2.5:m=s,adeclip=t=10:n=1000,'
VOICE_AF = ('highpass=f=80,lowpass=f=12000,'
            'acompressor=threshold=-18dB:ratio=2:attack=20:release=200,'
            + RESTORE + 'loudnorm=I=-19:TP=-1.5:LRA=11')
SERMON_EQ = 'equalizer=f=350:width_type=o:w=1:g=-3.5,highshelf=f=4500:g=2.5'
FISH_EQ = 'equalizer=f=1500:width_type=o:w=1.2:g=-4'
VOICE_AF_SERM = ('highpass=f=80,lowpass=f=12000,'
                 'acompressor=threshold=-18dB:ratio=2:attack=20:release=200,'
                 + RESTORE + SERMON_EQ + ',loudnorm=I=-19:TP=-1.5:LRA=11')
VOICE_AF_FISH = ('highpass=f=80,lowpass=f=12000,'
                 'acompressor=threshold=-18dB:ratio=2:attack=20:release=200,'
                 + FISH_EQ + ',loudnorm=I=-19:TP=-1.5:LRA=11')

LECT = {n: (D / f'analayo-nibbana-lecture-{n:02d}.mp3') for n in range(1, 34)}
SERM = {n: (D / 'sermon-audio' / f'Nibbana_Stilled_{n:02d}.mp3') for n in range(1, 34)}


def run(*a):
    subprocess.run(a, check=True, capture_output=True)


def fade_tail(dur, base=0.0):
    """Fade-out starting at (dur-0.03). afade=t=out:st=0 fades to zero at 30ms
    and STAYS silent — never st=0 on a fade-out (2026-10-26: every slice was
    a blip, user's ear caught it). base = pre-trim offset: output -ss trims
    AFTER filtering, so fade times live on the untrimmed timeline
    (2026-10-28: fades at trimmed times silenced whole slices)."""
    return (f'afade=t=in:st={base:.2f}:d=0.03,'
            f'afade=t=out:st={max(base, base + dur - 0.03):.2f}:d=0.03')


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
    # Accurate seek (2026-10-28 owner ear: input -ss starts slices EARLY on
    # keyframes — pre-roll chant/breath audible before sentence starts).
    # Hybrid: fast input seek to (ss-PRE), sample-accurate output trim.
    # Output -ss trims AFTER filtering, so fades use the untrimmed base.
    PRE = 5.0
    ss_in = max(0.0, float(ss) - PRE)
    off = float(ss) - ss_in
    chain = VOICE_AF_SERM if 'sermon-audio' in str(src) else VOICE_AF
    run('ffmpeg', '-v', 'error', '-y', '-ss', str(ss_in), '-i', str(src),
        '-ss', str(off), '-to', str(off + dur),
        '-ar', str(SR), '-ac', '1', '-c:a', 'pcm_s16le',
        '-af', chain + ',' + fade_tail(dur, off), str(dst))
    assert_audible(dst, f'{src}[{ss}-{to}]')
    got = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                                'format=duration', '-of', 'csv=p=0', str(dst)],
                               check=True, capture_output=True, text=True).stdout.strip())
    if abs(got - dur) > 0.15:
        raise SystemExit(f'SLICE DRIFT: {src}[{ss}-{to}] want {dur}s got {got}s')


def silence(dur, dst):
    run('ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i',
        f'anullsrc=r={SR}:cl=mono:d={dur}', '-c:a', 'pcm_s16le', str(dst))


def fish_wav(text, dst):
    """Fish Audio guide voice: questions + plain responses (owner 2026-10-28:
    QUESTION, PLAIN, ANALAYO — beat plains stay on screen, analayo-only).
    FREE TIER ONLY — model pinned to s2.1-pro-free, abort anything else
    (owner: never spend credits). Default voice, flat delivery. Key from
    $FISH_API_KEY, else characters/audition/.env (same key the audition
    build uses); the key is never written anywhere by this script. No
    silent fallback: API failure aborts the render instead of shipping
    robot voice (R5).
    Owner 2026-10-28: speech says NIRVANA (data + gates keep Nibbana)."""
    import json as _json
    import os as _os
    import urllib.request as _url
    MODEL = 's2.1-pro-free'
    assert MODEL == 's2.1-pro-free', 'paid model blocked: never spend credits'
    text = text.replace('Nibbana', 'Nirvana')
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
        '-c:a', 'pcm_s16le', '-af', VOICE_AF_FISH + ',' + fade_tail(dur),
        str(dst))
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
    if voice[0] in ('fish', 'plain'):
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


def newa_events(n, asm, picks):
    """Analayo-only new-A section events: opening (bell/Q/pause/plain/
    pointer-analayo/water) + picked beats (analayo + surrounding pauses).
    Verbatim lives on screen; fish-term/human-intro never taken.
    Beat numbering is STABLE (pointer triple = beat 1, see build_newA)."""
    ab, cur = {}, []
    anas = [i for i, e in enumerate(asm) if e['t'] == 'analayo']
    j = 0
    while j < len(anas) and asm[anas[j]].get('essay') == 0:
        j += 1
    assert j >= 1, 'no essay-0 pointer'
    ab[1] = asm[:anas[j - 1] + 1]
    n = 1
    for e in asm[anas[j - 1] + 1:]:
        cur.append(e)
        if e['t'] == 'analayo':
            n += 1
            ab[n] = cur
            cur = []
    full = [e for _, evs in sorted(ab.items()) for e in evs]
    assert any(e['t'] == 'verbatim' for e in ab[1]), 'no pointer verbatim'
    assert ab[1][1]['t'] == 'fish' and ab[1][3]['t'] == 'fish', \
        'opening order drifted (want bell/Q/pause/plain/verb/ana)'
    take = set()
    for b in picks:
        for e in ab[b]:
            # Verbatim lives on screen in newA audio (Fish voices Q +
            # opening plain only); fish-term/human-intro never taken.
            if e['t'] not in ('human-intro', 'fish-term', 'verbatim'):
                take.add(id(e))
    for b in picks:
        if b == 1:
            continue
        for i, e in enumerate(full):
            if e is ab[b][-1] and i + 1 < len(full) \
                    and full[i + 1]['t'] == 'water':
                take.add(id(full[i + 1]))
    final = []
    for e in full:
        if id(e) not in take:
            continue
        if e['t'] == 'verbatim':
            continue  # on screen only (analayo-only); kept out of audio
        final.append(e)
    return final


def verbatim_slot(events, i, e, tag, n):
    """Resolve (s, clip) for a verbatim event (shared by render + voice-id).
    Pointer = the event flagged essay 0 (index-free: openings gained a
    plain event 2026-10-28, so no positional indexing anywhere here)."""
    if tag == 'seed':
        return e['unit'], ESSAY0_BEAT[e['unit']]
    if e.get('essay') == 0:
        return n, ESSAY0_BEAT[n]  # opening essay-0 pointer
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
        if xt == 'fish' and (not NO_PLAIN or x.get('role') in ('question', 'plain')):
            return ('fish',)
        if xt == 'verbatim':
            s, clip = verbatim_slot(events, j, x, tag, n)
            # Seed stays a DIRECT trailer in every mode; section essay-0
            # pointers go direct outside newA (analayo-only: newA skips
            # all verbatim audio before this is even reached).
            if DIRECT_ESSAY0 and (tag == 'seed' or (x.get('essay') == 0 and not NEWA)):
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
    if P1 and tag == 'seed':
        # Bowls open the piece (sfx README: intro bell; echo at close).
        wavs.append(CACHE / 'sfx_bowls_intro.wav')
        kinds.append('sfx-bowls')
        log.append('sfx bowls_intro opens seed (+10dB)')
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
            if (P1 and t == 'pause' and e['dur'] >= 6.0 and kinds
                    and kinds[-1] == 'zoom-bell'):
                # Section settle: long-break bell first, room bridge holds
                # the remainder — total pause time preserved (TIMINGS intact).
                wavs.append(CACHE / 'sfx_long_break_bell.wav')
                kinds.append('sfx-break')
                log.append('sfx long_break_bell under settle')
                rest = round(e['dur'] - BREAK_DUR, 2)
                if prv is not None and nxt is not None and rest > 0.5:
                    wavs.append(bridge_wav(rest, prv, nxt))
                    kinds.append(t)
                    log.append(f'{t} {rest}s bridge {prv}->{nxt} (post-break)')
                else:
                    wavs.append(get_slice('sil', f'{t}{rest}', 0, rest, None))
                    kinds.append(t)
                    log.append(f'{t} {rest}s')
            elif prv is not None and nxt is not None:
                wavs.append(bridge_wav(e['dur'], prv, nxt))
                kinds.append(t)
                log.append(f'{t} {e["dur"]}s bridge {prv}->{nxt}')
            else:
                wavs.append(get_slice('sil', f'{t}{e["dur"]}', 0, e['dur'], None))
                kinds.append(t)
                log.append(f'{t} {e["dur"]}s')
        elif t == 'fish':
            if e.get('role') in ('question', 'plain'):
                # Guide voice: questions + plain responses (owner 2026-10-28).
                # Beat plains (role None) stay on screen (analayo-only).
                STATS['fish_lines'] += 1
                say = e.get('say', '')
                wavs.append(get_slice('vox', f'f{n}', 0, 0, None, say))
                kinds.append('fish' if e.get('role') == 'question' else 'plain')
                prev_voice[0] = ('fish',)
                log.append(f'{e.get("role")}: {say[:60]}')
            elif NO_PLAIN:
                STATS['plain_skipped'] = STATS.get('plain_skipped', 0) + 1
                log.append(f'beat plain on screen (analayo-only): {e.get("say", "")[:60]}')
                continue
            else:
                STATS['fish_lines'] += 1
                say = e.get('say', '')
                wavs.append(get_slice('vox', f'f{n}', 0, 0, None, say))
                kinds.append('fish')
                prev_voice[0] = ('fish',)
                log.append(f'fish: {say[:60]}')
        elif t == 'fish-term':
            if NO_PLAIN:
                STATS['plain_skipped'] = STATS.get('plain_skipped', 0) + 1
                log.append(f'fish-term skipped (beat plains live on screen): {e.get("say", "")}')
                continue
            STATS['fish_lines'] += 1
            wavs.append(get_slice('vox', f'ft{n}', 0, 0, None, e.get('say', '')))
            kinds.append('fish-term')
            log.append(f'fish-term: {e.get("say", "")}')
        elif t == 'analayo':
            ss, to = e['start'], e['end']
            pw = next(((l, s) for (l, s) in PERW if l == e['lec']
                       and abs(s - e['start']) < 0.05), None)
            ds_fixed = any(l == e['lec'] and abs(s - e['start']) < 0.05
                           for (l, s) in DS_FIXED)
            if not ds_fixed and ((P1 or NEWA)
                    and (pw or e['lec'] in YT_OFF or e['lec'] == 20)):
                if pw:
                    off = PERW[(pw[0], pw[1])]
                    ss, to = round(ss - off, 2), round(to - off, 2)
                    log.append(f'L{e["lec"]} {e["start"]}-{e["end"]} PERW-{off}s -> DS')
                else:
                    if e['lec'] == 20:
                        raise SystemExit(
                            'p1: L20 drifts — measure its per-window offset first (§69)')
                    off = YT_OFF[e['lec']]
                    if off == 0.0:
                        log.append(f'WARN L{e["lec"]} no YT offset (renders YT-time)')
                    ss, to = round(ss - off, 2), round(to - off, 2)
                    log.append(f'L{e["lec"]} {e["start"]}-{e["end"]} YT-{off}s -> DS')
            else:
                log.append(f'L{e["lec"]} {e["start"]}-{e["end"]}')
            wavs.append(get_slice('src', f'a{n}', ss, to, LECT[e['lec']]))
            kinds.append('analayo')
            prev_voice[0] = ('lect', e['lec'])
            if tag == 'seed':
                ESSAY0_WINDOWS.append((e['lec'], ss, to))
        elif t == 'verbatim':
            if NEWA:
                # Analayo-only rule: verbatim lives on screen; ears stay
                # with one voice. (Manifest keeps screen_verbatim/plain.)
                log.append('verbatim ON SCREEN only (analayo-only)')
                continue
            if tag == 'seed':
                s, clip = e['unit'], ESSAY0_BEAT[e['unit']]
            elif e.get('essay') == 0:
                s, clip = n, ESSAY0_BEAT[n]  # opening essay-0 pointer (flagged)
            else:
                nxt = next(x for x in events[i + 1:] if x['t'] == 'fish' and 'beat' in x)
                s, clip = n, nxt['beat']
            if DIRECT_ESSAY0 and (tag == 'seed' or (e.get('essay') == 0 and not NEWA)):
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
    global ALIGN, OUT, CACHE, BREAK_DUR
    OUT = BUILD / ('audio_newA' if NEWA else ('audio_p1' if P1 else ('audio_p0' if P0_NO_BELLS else 'audio_v1')))
    CACHE = OUT / 'cache'
    OUT.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    for b in ('motto-bell', 'zoom-bell'):
        dst = CACHE / f'{b}.wav'
        if not dst.exists():
            run('ffmpeg', '-v', 'error', '-y', '-i', str(BUILD / 'assets' / f'{b}.wav'),
                '-ar', str(SR), '-ac', '1', '-c:a', 'pcm_s16le', str(dst))
    if P1 or NEWA:
        # NEWA needs YT offsets too (newA S1b11 rides L20); no sfx in newA.
        YT_OFF.update({int(k): (v.get('offset_s') or 0.0)
                       for k, v in json.loads((BUILD / 'yt_anchor_map.json').read_text()).items() if isinstance(v, dict) and v.get('offset_s')})
        for name, gain in SFX_GAIN.items():
            dst = CACHE / f'sfx_{name}.wav'
            if not (dst.exists() and dst.stat().st_size > 0):
                run('ffmpeg', '-v', 'error', '-y', '-i', str(SFX / f'{name}.wav'),
                    '-ar', str(SR), '-ac', '1', '-c:a', 'pcm_s16le',
                    '-af', f'volume={gain}dB', str(dst))
                assert_audible(dst, f'sfx:{name}')
        dp = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                             'format=duration', '-of', 'csv=p=0',
                             str(CACHE / 'sfx_long_break_bell.wav')],
                            check=True, capture_output=True, text=True)
        BREAK_DUR = round(float(dp.stdout.strip()), 2)
    ALIGN = {(e['s'], e['clip']): e for e in
             json.loads((BUILD / 'verbatim_audio_v1.json').read_text())}
    asm = {0: json.loads((BUILD / 'assembly_s0_seed.json').read_text())}
    asm.update({n: json.loads((BUILD / f'assembly_s{n}.json').read_text()) for n in range(1, 7)})

    manifest, files = {}, {}
    mp3, dur, log = render_section(0, asm[0], 'seed')
    files['seed'] = mp3
    manifest['seed'] = {'min': round(dur / 60, 2), 'log': log,
                        'timeline': manifest_timeline['seed']}
    if P1_SEED_ONLY or (NEWA and NEWA_SEED_ONLY):
        manifest['stats'] = STATS
        (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=1))
        print('STATS', STATS)
        return
    if NEWA:
        newa = json.loads((BUILD / 'newA_manifest.json').read_text())
        for n in range(1, 7):
            sec = newa['sections'][str(n)]
            picks = [sec['pointer']['beat']] + [u['beat'] for u in sec['beats']]
            evs = newa_events(n, asm[n], picks)
            mp3, dur, log = render_section(n, evs, f's{n}')
            files[f's{n}'] = mp3
            manifest[f's{n}'] = {'min': round(dur / 60, 2), 'log': log,
                                 'timeline': manifest_timeline[f's{n}'],
                                 'beats': picks}
        lst = OUT / 'full.lst'
        lst.write_text(''.join(f"file '{files[t]}'\n" for t in ['seed'] + [f's{n}' for n in range(1, 7)]))
        run('ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', str(lst),
            '-c:a', 'copy', str(OUT / 'full_newA_essay.mp3'))
        manifest['stats'] = STATS
        (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=1))
        print('STATS', STATS)
        return
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
