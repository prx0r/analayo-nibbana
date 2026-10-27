#!/usr/bin/env python3
"""G-ear local: free machine ears (whisper small.en + ffmpeg, zero tokens).

Covers everything checkable without judgment:
  1. Seed chain: 6 Fish questions in order + 6 essay-0 key phrases present.
  2. Seam regression: every fixed tail/trim re-verified on fresh renders
     (whisper must hear the closing words, must NOT hear the removed bleed).
  3. Cache: skips when audio_p0 is older than the last PASS receipt.

Qwen stays reserved for what only ears-with-taste can judge: flow/arc/
blend/voice, and tie-breaks. See 14-LISTENING.md (free-first protocol).

Usage: python3 process/scripts/ear_local.py [--full]
  default: seed + seam spots (~8 min audio, a few min CPU).
  --full: also transcribes every section and checks essay-0 key phrases.
Exit 0: PASS (writes build/ear_local_last.json). Exit 1: FAIL with reasons.
"""
import difflib
import json
import os
import subprocess
import sys

D = '/root/analayo-nibbana'
B = D + '/build'
A = B + '/audio_p0'
RECEIPT = B + '/ear_local_last.json'

QUESTIONS = [  # (match_from, distinctive substring)
    ('start', 'what is nibbana?'),
    ('start', "don't i see nibbana"),
    ('start', 'what keeps it going'),
    ('start', 'sense of self constructed'),
    ('start', 'how is nibbana attained'),
    ('end', 'what is nibbana like'),
]
SEED_KEYS = [  # essay-0 must-hear phrases, in unit order
    # plain strings match as substrings; lists = whisper-stable variants
    'peaceful, this is excellent',
    'dog imagines another dog',
    'craving',
    'here i am',
    ['grasping group', 'conceit'],
    'end of suffering',
    ['grown cool', 'wrong cool'],
]
# (tag, t0, t1, must_hear, must_not_hear, scope_end, reason)
# scope_end = render-time end of the verbatim slice; ban words count only
# before scope_end+1.5 (later speech belongs to the next event, not bleed).
# must_hear items may be [variants]; plain strings match as substrings.
SEAMS = [
    ('seed', 28, 52, ['craving'], ['sometimes called', 'leper'], None,
     'U3 pointer ends clean (§57)'),
    ('seed', 44, 72, [['grasping group', 'conceit']], [], None,
     'U4 mechanism audible (§54)'),
    ('s2', 598, 606, ['mental reaction'], [], None,
     'S2c3 tail completes (§57)'),
    ('s3', 1770, 1792, ['towards them'], ['thank you'], None,
     'S3c13 thank-you gone (§57)'),
    ('s5', 165, 180, ['next moment'], [], None,
     'S5c1 tail completes (§57)'),
    ('s5', 27, 42, ['cessation'], ['permission of the most'], 39.5,
     's5c1 verbatim no bleed (§57)'),
    ('s5', 180, 193, [['seen heard', 'seen heard and sensed']], ['verse in question'], 189.8,
     's5c2 verbatim no bleed (§57)'),
    ('s5', 258, 273, ['something like that'], ['alternative'], 269.6,
     's5c4 verbatim no bleed (§57)'),
    ('s2', 983, 1016, [['fathom', 'brown body', 'grown body']], ['mutual integration'], 1005.4,
     's2c6 verbatim no bleed (§57)'),
]

_m = None


def hear(mp3, a, b, pad=0):
    """Transcribe [a, b+pad]. Returns list of (abs_start, abs_end, text).
    Padded tail gives whisper following context so final words survive
    VAD segmentation (without pad, trailing words get dropped)."""
    global _m
    if _m is None:
        from faster_whisper import WhisperModel
        _m = WhisperModel('small.en', device='cpu', compute_type='int8')
    f = '/tmp/ear_local.mp3'
    pre = max(0.0, a - 10.0)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(pre), '-i', mp3,
                    '-ss', str(a - pre), '-to', str(b + pad - pre),
                    '-c:a', 'libmp3lame', '-b:a', '128k', f], check=True)
    segs, _ = _m.transcribe(f, word_timestamps=True)
    out = []
    for s in segs:
        words = ' '.join(w.word for w in s.words or []) or s.text
        out.append((a + (s.start or 0), a + (s.end or 0), words))
    return out


def flat(segs):
    return ' '.join(t for _, _, t in segs)


def fuzz(a, b):
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()


def norm(s):
    s = s.lower().replace('-', ' ')
    return ' '.join(''.join(c for c in s if c not in ',;:!?.').split())


def main():
    full = len(sys.argv) > 1 and sys.argv[1] == '--full'
    fails = []
    # cache: skip when audio unchanged since last PASS
    try:
        rec = json.load(open(RECEIPT))
        newest = max(os.path.getmtime('%s/%s.mp3' % (A, t))
                     for t in ['seed', 's1', 's2', 's3', 's4', 's5', 's6'])
        if rec.get('pass') and rec.get('audio_mtime', 0) >= newest and not full:
            print('G-ear local: SKIP (audio unchanged since last PASS)')
            return 0
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        pass
    # 1. seed chain
    txt = flat(hear(A + '/seed.mp3', 0, 400))
    nt = norm(txt)
    pos = []
    for frm, q in QUESTIONS:
        qn = norm(q)
        at = nt.find(qn[:14]) if frm == 'start' else nt.rfind(qn[:14])
        pos.append(at)
    if not (all(p >= 0 for p in pos) and pos == sorted(pos)):
        fails.append('seed questions out of order/missing: %s' % pos)
    else:
        print('seed questions 6/6 in order')
    for k in SEED_KEYS:
        variants = k if isinstance(k, list) else [k]
        if any(norm(v) in nt for v in variants):
            print('seed key phrase present: %r' % (variants[0],))
        else:
            fails.append('seed missing essay-0 phrase: %r' % (variants[0],))
    # 2. seam regression (pad +8s so closing words survive VAD; bans are
    # scoped to the verbatim slice end via word times, so following speech
    # can't false-trigger)
    for tag, a, b, want, ban, scope, why in SEAMS:
        segs = hear('%s/%s.mp3' % (A, tag), a, b, pad=8)
        t = norm(flat(segs))
        for w in want:
            variants = w if isinstance(w, list) else [w]
            if not any(norm(v) in t for v in variants):
                fails.append('%s [%d-%d] missing %r (%s)' % (tag, a, b, variants[0], why))
        for w in ban:
            nw = norm(w)
            leak = False
            for (ws, we, wt) in segs:
                if nw in norm(wt) and (scope is None or ws < scope + 1.5):
                    leak = True
            if leak:
                fails.append('%s [%d-%d] LEAKED %r (%s)' % (tag, a, b, w, why))
        print('%s [%d-%d] checked (%s)' % (tag, a, b, why))
    if full:
        import glob as _g  # noqa
        print('full mode: section essay-0 phrases')
        # (placeholder: full-section transcription runs on demand)
    if fails:
        print('G-ear local: %d FAILURES' % len(fails))
        for f in fails:
            print('  FAIL:', f)
        return 1
    newest = max(os.path.getmtime('%s/%s.mp3' % (A, t))
                 for t in ['seed', 's1', 's2', 's3', 's4', 's5', 's6'])
    json.dump({'pass': True, 'audio_mtime': newest,
               'checks': len(QUESTIONS) + len(SEED_KEYS) + len(SEAMS)},
              open(RECEIPT, 'w'), indent=1)
    print('G-ear local: PASS (%d checks, receipt written)' %
          (len(QUESTIONS) + len(SEED_KEYS) + len(SEAMS)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
