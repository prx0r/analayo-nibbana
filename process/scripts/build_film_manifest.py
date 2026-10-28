#!/usr/bin/env python3
"""Build build/film_manifest.json — four-depth membership per chapter.

Implements visuals/FIVE-HOUR-CUT.md: every clip assigned to its EARLIEST
depth. Rules (deterministic):
  0 = the seed's essay-0 windows (atomic)
  A/B/C = greedy fill to the cumulative budgets, scoring:
      unflagged before flagged (the five D-categories), core before
      gold, cluster-spread caps (A:2, B:5/cluster, C:open),
      gold spans overlapping a core clip (>50%) deduped (same passage,
      core window wins). Cell contents cumulative: 0 c A c B c C.
Flags computed from transcripts (whisper sentences inside the window),
cached in build/.film_flags_cache.json (gitignored). Gates: process/scripts/g8_film_check.py.
"""
import json, re, os, bisect, sys

D = '/root/analayo-nibbana'
CACHE = os.path.join(D, 'build', '.film_flags_cache.json')
BUD = {1: (30, 240, 600, 1500), 2: (90, 420, 1080, 1980), 3: (75, 420, 1200, 2040),
       4: (45, 240, 480, 780), 5: (45, 420, 1140, 2100), 6: (75, 420, 900, 1680)}
# Documented hand-picks (REVIEW pass: highest-signal A composition).
# out = weaker A slot (still available to B/C); in = its replacement.
FORCE_IN  = {1: [(1, 3244.0), (1, 4524.0)],   # fire + well-spring
             4: [(25, 711.0)],                 # barb ("I know, I see")
             6: [(33, 1918.7)]}                # great man beyond both ends
FORCE_OUT = {1: [(19, 390.0)],                 # sa-upadisesa -> B
             4: [(8, 1382.0)],                 # sun/moon backdrop -> B
             6: [(31, 4604.6)]}                # faculties formula -> B
def _key(c):
    return (1 if c['_flags'] else 0, 0 if c.get('grade') == 'A' else 1, c['_fi'])
def _in(s, c, table):
    return any(c['lec'] == l and abs(c['start'] - st) < 1 for l, st in table.get(s, []))

QS = {1: 'What is Nibbana?', 2: "Why don't I see Nibbana right now?", 3: 'What keeps it going?',
      4: 'How is the sense of self constructed?', 5: 'How is Nibbana attained?', 6: 'What is Nibbana like?'}
YTSUB = {3, 6, 7, 14, 17, 20, 22, 24, 26, 27}

REF = re.compile(r'stilling of all preparations', re.I)
CMT = re.compile(r'(common|comment)\s*,?\s*translat|translat(?:ion)?\s+by\s+\w|end of comment|according to the commentar', re.I)
CIT = re.compile(r'nikāya|nikaya|sutta|gāthā|jātaka|dhammapada|visuddhimagga|milinda|theragāthā|udāna|saṃyutta|samyutta', re.I)
ETYM = re.compile(r'\bword\b.*\bterm\b|\bPali\b|\betymol|literally means|rendered as|translated as', re.I)

_scache = {}
def sents(lec):
    if lec in _scache:
        return _scache[lec]
    out = []
    if lec not in YTSUB and os.path.exists('%s/lecture-%02d.transcript.cf.json' % (D, lec)):
        d = json.load(open('%s/lecture-%02d.transcript.cf.json' % (D, lec)))
        out = sorted([(float(s.get('t', 0)), float(s.get('end', s.get('e', 0))), s.get('text', ''))
                      for s in d.get('sentences', [])])
    elif os.path.exists('%s/yt-subs/lecture-%02d.json' % (D, lec)):
        d = json.load(open('%s/yt-subs/lecture-%02d.json' % (D, lec)))
        out = sorted([(float(c['t']), float(c['e']), c.get('x', '')) for c in d.get('cues', [])])
    _scache[lec] = out
    return out

def span_text(sp):
    ss = sents(sp['lec'])
    starts = [x[0] for x in ss]
    i = bisect.bisect_left(starts, sp['start'] - 1.0)
    parts = []
    while i < len(ss) and ss[i][0] <= sp['end'] + 0.5:
        if ss[i][1] >= sp['start'] - 1.0:
            parts.append(ss[i][2])
        i += 1
    return re.sub(r'\s+', ' ', ' '.join(parts)).strip()

def compute_flags(sp):
    t = span_text(sp)
    f = []
    if REF.search(t):
        f.append('refrain')
    if CMT.search(t) and (t.count('ranslat') + t.count('omment') >= 2 or len(t) < 400):
        f.append('commentary')
    pw = [w for w in t.split() if re.search(r'[āīūñṃṁṇṭḍḷ]', w)]
    if len(pw) >= 6 and len(pw) > 0.12 * len(t.split()):
        f.append('pali')
    if len(CIT.findall(t)) >= 3:
        f.append('citation')
    if ETYM.search(t):
        f.append('etym')
    return f

_cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
def flags_of(s, sp):
    k = '%d|%d|%.1f' % (s, sp['lec'], sp['start'])
    if k not in _cache:
        _cache[k] = compute_flags(sp)
        json.dump(_cache, open(CACHE, 'w'))
    return _cache[k]

def d(c):
    return c['end'] - c['start']
def overlap(a, b):
    return a['lec'] == b['lec'] and (min(a['end'], b['end']) - max(a['start'], b['start'])) > 0

seed = json.load(open('%s/build/assembly_s0_seed.json' % D))
e0win = [e for e in seed if e['t'] == 'analayo']

manifest = {'budgets_s': {str(k): list(v) for k, v in BUD.items()}, 'questions': QS, 'chapters': {}}
grand = {'0': 0, 'A': 0, 'B': 0, 'C': 0}

for s in range(1, 7):
    core = json.load(open('%s/build/seg%d_core_v4.json' % (D, s)))
    gold = json.load(open('%s/build/seg%d_gold.json' % (D, s)))
    for i, c in enumerate(core):
        c['_src'], c['_fi'], c['_flags'] = 'core', i, flags_of(s, c)
    lec0, st0, en0 = e0win[s - 1]['lec'], e0win[s - 1]['start'], e0win[s - 1]['end']
    # Essay-0 pointers live INSIDE core clips (essay0_windows.json), not on
    # their boundaries: containment, not start-identity (2026-10-26 pointers).
    e0 = next((c for c in core if c['lec'] == lec0 and c['start'] - 3 <= st0
               and en0 <= c['end'] + 3), None)
    assert e0, 'e0 pointer not inside any core clip for section %d' % s

    gkeep = []
    for g in gold:
        if any(overlap(g, c) for c in core):
            continue
        g['_src'], g['_flags'] = 'gold', flags_of(s, g)
        gkeep.append(g)

    def dcell(items):
        return sum(d(x) for x in items)

    def greedy(pool, cap, taken, cluster_cap):
        chosen, rem = [], cap
        for x in pool:
            if d(x) > rem:
                continue
            ci = x.get('ci', -1)
            if taken.get(ci, 0) >= cluster_cap:
                continue
            chosen.append(x)
            rem -= d(x)
            taken[ci] = taken.get(ci, 0) + 1
        return chosen

    b0, ba, bb, bc = BUD[s]
    A = [e0]
    takA = {e0.get('ci', -1): 1}
    forced = [c for c in core if c is not e0 and _in(s, c, FORCE_IN)]
    outl = [c for c in core if _in(s, c, FORCE_OUT)]
    for f in forced:
        if not any(f is x for x in A):
            A.append(f)
            takA[f.get('ci', -1)] = takA.get(f.get('ci', -1), 0) + 1
    poolA = sorted([c for c in core if c is not e0 and c not in forced and c not in outl],
                   key=_key)
    A += greedy(poolA, ba - dcell(A), takA, 2)

    B = list(A)
    takB = {}
    for x in B:
        takB[x.get('ci', -1)] = takB.get(x.get('ci', -1), 0) + 1
    remB = sorted([c for c in core if not any(c is x for x in B)], key=_key)
    B += greedy(remB, bb - dcell(B), takB, 5)
    B += greedy([g for g in gkeep if not g['_flags']], bb - dcell(B), takB, 6)

    C = list(B)
    takC = {}
    for x in C:
        takC[x.get('ci', -1)] = takC.get(x.get('ci', -1), 0) + 1
    remC = sorted([c for c in core if not any(c is x for x in C)], key=_key)
    C += greedy(remC, bc - dcell(C), takC, 99)
    C += greedy([g for g in gkeep if not g['_flags'] and not any(g is x for x in C)], bc - dcell(C), takC, 99)
    C += greedy([g for g in gkeep if g['_flags'] and not any(g is x for x in C)], bc - dcell(C), takC, 99)

    def pack(items, depth):
        return [dict(lec=x['lec'], start=x['start'], end=round(x['end'], 2), dur=round(d(x), 1),
                     src=x['_src'], ci=x.get('ci'), grade=x.get('grade'),
                     flags=x['_flags'], depth=depth) for x in items]

    # Depth 0 = the essay-0 POINTER window (seed's atomic clip), NOT the full
    # core beat — pointers live inside core clips (2026-10-26 pointers).
    e0w = e0win[s - 1]
    cell0 = [dict(lec=e0w['lec'], start=e0w['start'], end=round(e0w['end'], 2),
                  dur=round(e0w['end'] - e0w['start'], 1), src='core',
                  ci=e0.get('ci'), grade=e0.get('grade'), flags=[],
                  depth='0')]
    manifest['chapters'][str(s)] = {'question': QS[s], '0': cell0, 'A': pack(A, 'A'),
                                    'B': pack(B, 'B'), 'C': pack(C, 'C')}
    for dep, items in (('0', cell0), ('A', A), ('B', B), ('C', C)):
        grand[dep] += sum(c['end'] - c['start'] for c in items)
    ks = lambda cells: {(c['lec'], round(c['start'], 1)) for c in cells}
    ch = manifest['chapters'][str(s)]
    assert ks(ch['A']) <= ks(ch['B']) <= ks(ch['C']), 'nesting s%d' % s
    p0 = ch['0'][0]
    assert any(c['lec'] == p0['lec'] and c['start'] - 3 <= p0['start']
               and p0['end'] <= c['end'] + 3 for c in ch['A']), \
        'essay-0 pointer outside A for s%d' % s

json.dump(manifest, open('%s/build/film_manifest.json' % D, 'w'), indent=1)
scr = sum(grand.values())
print('film manifest built: 0=%.1fm A=%.1fm B=%.1fm C=%.1fm | screening=%.1fm'
      % (grand['0'] / 60, grand['A'] / 60, grand['B'] / 60, grand['C'] / 60, scr / 60))
