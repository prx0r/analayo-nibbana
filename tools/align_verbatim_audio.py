"""Align every seg-script verbatim excerpt to its sermon reading audio.

Method: per beat, take verbatim (str or list of contiguous excerpts) +
nanananda_sermon N, normalize (lower, strip punctuation), and locate the
best token window in sources/sermons/readings/Nibbana_Stilled_NN.json via
difflib longest-match. Window snapped to sentence bounds, padded ±1
sentence. Output: build/canon/verbatim_audio_v1.json
[{s, clip, sermon, parts:[{t,end,score,text}], status}]
status: ok (all parts>=0.40) | partial | miss.
No thresholds hidden: scores ship with every part; the renderer decides.
"""
import json
import re
import difflib
from pathlib import Path

D = Path('/root/analayo-nibbana')
BUILD = D / 'build' / 'canon'
SR = D / 'sources/sermons/readings'
THRESH = 0.40

# Manual pins (evidence-logged, last resort): the reader chants Pali the
# transcriber drops as non-English, leaving a gap where English resumes
# exactly on the quote's gloss.
# (1,3,0) "Khayamatta na nibbanam": sermon-01 gap 2173.0-2177.2 (4.2s) —
# prior sentence ends 2173.0, English resumes 2177.2 on the staircase
# simile this Pali line heads. The chant lives in the gap.
PINS = {(1, 3, 0): (1, 2173.0, 2177.2)}


def norm(t):
    t = t.lower()
    t = re.sub(r"[^a-z0-9' ]", ' ', t)
    return re.sub(r'\s+', ' ', t).strip().split()


def load_sermon(n):
    d = json.loads((SR / f'Nibbana_Stilled_{n:02d}.json').read_text())
    toks, owner = [], []
    for i, s in enumerate(d['sentences']):
        for w in norm(s['text']):
            toks.append(w)
            owner.append(i)
    return d['sentences'], toks, owner


def align_quote(qtok, stoks, owner, sents):
    """Coverage scoring (not longest-run): whisper noise scatters single-word
    misses through long quotes, so a single contiguous run under-scores them
    (e.g. banana-trunk scored 0.35 on one run while the passage IS there).
    Score = matched tokens / quote tokens over all blocks; window anchors on
    the largest block and expands to cover the quote's token length."""
    if not qtok or not stoks:
        return None
    sm = difflib.SequenceMatcher(None, stoks, qtok, autojunk=False)
    blocks = sm.get_matching_blocks()
    matched = sum(b.size for b in blocks)
    if matched == 0:
        return None
    score = matched / len(qtok)
    big = max(blocks, key=lambda b: b.size)
    si0, si1 = owner[big.a], owner[big.a + big.size - 1]
    # expand to cover quote length (±1 sentence, cap growth)
    while si0 > 0 and (si1 - si0) < len(sents) and sum(1 for o in owner if si0 - 1 <= o <= si1) < len(qtok) + 20 and (si0 > owner[big.a] - 1):
        si0 -= 1
        if si0 <= max(0, owner[big.a] - 1):
            break
    while si1 < len(sents) - 1 and sum(1 for o in owner if si0 <= o <= si1 + 1) < len(qtok) + 20 and (si1 < owner[big.a + big.size - 1] + 1):
        si1 += 1
        if si1 >= min(len(sents) - 1, owner[big.a + big.size - 1] + 1):
            break
    # head-trim (owner 2026-10-26): never cold-open on Pali chant or
    # preamble — drop leading sentences sharing zero tokens with the quote
    # (e.g. Namotasya chant before the motto). Keeps ≥1 sentence.
    qset = set(qtok)
    while si1 - si0 >= 1:
        toks = set(norm(sents[si0]['text']))
        if toks & qset:
            break
        si0 += 1
    return {'t': sents[si0]['t'], 'end': sents[si1]['end'], 'score': round(score, 3)}


def main():
    cache = {}
    out = []

    def get_sermon(n):
        if n not in cache:
            cache[n] = load_sermon(n)
        return cache[n]

    def best_window(qtok, first_try):
        """Assigned sermon first; if under threshold, scan all 33 and take
        the best. Returns (result, sermon_used)."""
        order = [first_try] + [n for n in range(1, 34) if n != first_try]
        best, best_srm = None, first_try
        for n in order:
            try:
                sents, stoks, owner = get_sermon(n)
            except FileNotFoundError:
                continue
            r = align_quote(qtok, stoks, owner, sents)
            if r is None:
                continue
            if best is None or r['score'] > best['score']:
                best, best_srm = r, n
            if n == first_try and best is not None and best['score'] >= THRESH:
                break
        return best, best_srm

    for s in range(1, 7):
        for b in json.loads((BUILD / f'seg{s}_script.json').read_text()):
            srm = b.get('nanananda_sermon')
            if isinstance(srm, str):
                m0 = re.search(r'\d+', srm)
                srm = int(m0.group()) if m0 else None
            txt = b.get('nanananda_verbatim', '')
            parts = txt if isinstance(txt, list) else [txt]
            aligned = []
            for pi, p in enumerate(parts):
                if (s, b['clip'], pi) in PINS:
                    srm_pin, t_pin, e_pin = PINS[(s, b['clip'], pi)]
                    aligned.append({'t': t_pin, 'end': e_pin, 'score': 1.0,
                                    'pinned': True, 'text': p[:80]})
                    continue
                if not p.strip() or not srm:
                    aligned.append({'t': None, 'end': None, 'score': 0.0, 'text': p[:80]})
                    continue
                r, used = best_window(norm(p), srm)
                if r is None:
                    aligned.append({'t': None, 'end': None, 'score': 0.0, 'text': p[:80]})
                else:
                    r['text'] = p[:80]
                    if used != srm:
                        r['sermon'] = used
                    aligned.append(r)
            scores = [a['score'] for a in aligned]
            status = 'ok' if scores and min(scores) >= THRESH else ('partial' if max(scores or [0]) >= THRESH else 'miss')
            out.append({'s': s, 'clip': b['clip'], 'sermon': srm, 'parts': aligned, 'status': status})
    (BUILD / 'verbatim_audio_v1.json').write_text(json.dumps(out, indent=1), encoding='utf-8')
    from collections import Counter
    c = Counter(e['status'] for e in out)
    sc = sorted([p['score'] for e in out for p in e['parts']])
    print(f'beats={len(out)} {dict(c)} median_score={sc[len(sc)//2]:.3f} '
          f'p10={sc[len(sc)//10]:.3f} min={sc[0]:.3f}')
    for e in out:
        if e['status'] != 'ok':
            print(' ', e['s'], e['clip'], e['sermon'], [p['score'] for p in e['parts']], e['parts'][0]['text'][:60])


if __name__ == '__main__':
    main()
