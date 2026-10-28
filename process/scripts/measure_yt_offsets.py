"""Measure YT-cue -> DS-audio offsets for the 10 YT-timebase lectures.

DS audio leads YT cues by ~5-10s (lectures fetched later from retreat
4373). For one anchor window per lecture: slice DS mp3 around the YT
window start, transcribe (faster-whisper small.en, word times), locate
the window's opening words, offset = YTstart - DStime.

Writes build/yt_anchor_map.json {lec: {offset_s, anchor_yt, anchor_ds}}.
Free, mechanical, cached: rerun overwrites. Known: L14 = 10.0s (§64).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

D = Path('/root/analayo-nibbana')
YT_LECS = [3, 6, 7, 14, 17, 20, 22, 24, 26, 27]


def norm(t):
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z0-9 ]', '', t.lower())).strip()


# One anchor window per lecture (YT seconds, opening words known from cues).
# Core windows preferred; gold windows where core has none.
ANCHORS = {
    3: (525.0, 652.5),
    6: (1409.0, 1446.8),
    7: None,  # resolved from gold below
    14: (1494.2, 1559.3),  # s3c12 (s5 windows already DS, §64)
    17: None,
    20: (488.0, 499.0),
    22: None,
    24: (4305.6, 4428.5),
    26: (1650.7, 1749.1),
    27: (3655.6, 3694.8),
}


def gold_anchor(lec):
    for n in range(1, 7):
        d = json.load(open(D / f'build/seg{n}_gold.json'))
        spans = d if isinstance(d, list) else d.get('spans', [])
        for s in spans:
            if s.get('lec') == lec and s.get('dur', 0) > 20:
                return (s['start'], s['end'])
    return None


def cue_words(lec, ss, to):
    """(word, yt_time) list from cues overlapping [ss, to]."""
    d = json.load(open(D / f'yt-subs/lecture-{lec:02d}.json'))
    out = []
    for c in d.get('cues', []):
        if c.get('e', 0) > ss and c.get('t', 0) < to:
            for w in c.get('x', '').split():
                out.append((norm(w), c.get('t', ss)))
    return [(w, t) for w, t in out if w]


def measure(model, lec, ss, to):
    """Try matching cue words at several depths; return (offset, yt, ds, n)."""
    mp3 = D / f'analayo-nibbana-lecture-{lec:02d}.mp3'
    seg = f'/tmp/yt_off_{lec}.mp3'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss',
                    str(max(0, ss - 30)), '-t', '70', '-i', str(mp3),
                    '-ar', '16000', '-ac', '1', seg], check=True)
    segs, _ = model.transcribe(seg, language='en', word_timestamps=True)
    words = []
    for s in segs:
        words += [(norm(w.word), w.start) for w in (s.words or [])]
    got = [w for w, _ in words if w]
    exp = cue_words(lec, ss, to)
    base = max(0, ss - 30)
    for depth in (0, 10, 20):
        chunk = exp[depth:depth + 10]
        if len(chunk) < 5:
            continue
        best, best_i, best_yt = 0, None, None
        for i in range(len(got)):
            k = 0
            while (k < len(chunk) and i + k < len(got)
                   and got[i + k] == chunk[k][0]):
                k += 1
            if k > best:
                best, best_i, best_yt = k, i, chunk[0][1]
        if best >= 5:
            # first matched cue word ≈ YT best_yt; DS time = base + words[..]
            j = 0
            while j < len(words) and not words[j][0]:
                j += 1
            ds_t = base + words[best_i][1]
            return (round(best_yt - ds_t, 1), best_yt, round(ds_t, 1), best)
    return None


def candidates(lec):
    """Anchor windows to try: core windows, then gold spans >20s."""
    out = []
    for n in range(1, 7):
        d = json.load(open(D / f'build/seg{n}_core_v4.json'))
        clips = d if isinstance(d, list) else d.get('clips', [])
        for s in clips:
            if s.get('lec') == lec:
                out.append((s['start'], s['end']))
    for n in range(1, 7):
        d = json.load(open(D / f'build/seg{n}_gold.json'))
        spans = d if isinstance(d, list) else d.get('spans', [])
        for s in spans:
            if s.get('lec') == lec and s.get('dur', 0) > 30:
                out.append((s['start'], s['end']))
                if len(out) >= 5:
                    return out
    return out


def main():
    from faster_whisper import WhisperModel
    model = WhisperModel('small.en', device='cpu', compute_type='int8')
    prior = {}
    try:
        prior = json.load(open(D / 'build/yt_anchor_map.json'))
    except FileNotFoundError:
        pass
    out = dict(prior)
    for lec in YT_LECS:
        if lec == 14:
            out[lec] = {'offset_s': 10.0, 'anchor_yt': 1494.2,
                        'anchor_ds': 1484.2, 'method': 'prior-§64'}
            print(f'L{lec:02d}: offset=10.0 (prior §64, skipped)', flush=True)
            continue
        if str(lec) in out and out[str(lec)].get('method', '').startswith('whisper-match-1'):
            pass  # re-measure weak ones too
        done = False
        for (ss, to) in candidates(lec)[:5]:
            r = measure(model, lec, ss, min(to, ss + 60))
            if r:
                off, yt, ds, n = r
                out[lec] = {'offset_s': off, 'anchor_yt': yt,
                            'anchor_ds': ds, 'method': f'whisper-match-{n}w'}
                print(f'L{lec:02d}: offset={off} ({n}w match @YT{yt})', flush=True)
                done = True
                break
        if not done:
            print(f'L{lec:02d}: NO MATCH', flush=True)
    json.dump({str(k): v for k, v in out.items()},
              open(D / 'build/yt_anchor_map.json', 'w'), indent=1)
    print('wrote build/yt_anchor_map.json')


if __name__ == '__main__':
    main()
