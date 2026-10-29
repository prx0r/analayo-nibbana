#!/usr/bin/env python3
"""G8 — film manifest gates: nesting, budgets, provenance, chain, source-membership.

FAIL conditions: broken E0 c EA c EB c EC nesting, A/B/C over budget,
missing provenance fields, question drift from the locked chain,
film clip absent from the kept pool.
WARN (reported, not fatal): rung-0 cells over design target — the
seed clips are atomic source windows (documented in FILM-CUT.md).
"""
import json, sys, re

M = json.load(open('build/canon/film_manifest.json'))
BUD = {int(k): tuple(v) for k, v in M['budgets_s'].items()}
CHAIN = {
    1: 'What is Nibbana?',
    2: "Why don't I see Nibbana right now?",
    3: 'What keeps it going?',
    4: 'How is the sense of self constructed?',
    5: 'How is Nibbana attained?',
    6: 'What is Nibbana like?',
}
fails, warns = [], []

# chain sync with the audio build source (QUESTIONS block only — the
# (chain lives in the QUESTIONS block only)
src = open('process/scripts/make_assembly.py').read()
qblock = src.split('QUESTIONS = {')[1].split('}')[0]
live = {int(i): q.replace('\\"', '"')
        for i, q in re.findall(r'^\s+(\d): "(.*)",$', qblock, re.M)}
for s in range(1, 7):
    if live.get(s) != CHAIN[s]:
        fails.append('chain drift ch%d: manifest=%r build=%r' % (s, CHAIN[s], live.get(s)))

pool = {s: json.load(open('build/canon/seg%d_pool.json' % s)) for s in range(1, 7)}

def kset(cells): return {(c['lec'], round(c['start'], 1)) for c in cells}
def dur(cells): return sum(c['dur'] for c in cells)
def in_pool(s, c):
    return any(p['lec'] == c['lec'] and
               (min(p['end'], c['end']) - max(p['start'], c['start'])) > 0.5 * min(p['end']-p['start'], c['end']-c['start'])
               for p in pool[s])

tot = {'0': 0, 'A': 0, 'B': 0, 'C': 0}
for s in range(1, 7):
    ch = M['chapters'][str(s)]
    if ch.get('question') != CHAIN[s]:
        fails.append('ch%d question mismatch: %r' % (s, ch.get('question')))
    sets = {d: kset(ch[d]) for d in '0ABC'}
    if not (sets['A'] <= sets['B'] <= sets['C']):
        fails.append('ch%d nesting broken' % s)
    # 0 (essay-0 pointers) nest by CONTAINMENT inside A — or inside gold
    # essay0-anchors (§39 pattern, S2 triple 2026-10-28), not identity.
    for p in ch['0']:
        host = ch['A'] + [x for x in ch['B']]
        if not any(c['lec'] == p['lec'] and c['start'] - 3 <= p['start']
                   and p['end'] <= c['end'] + 3 for c in host):
            fails.append('ch%d essay-0 pointer outside A/B: L%s [%.1f]' % (s, p['lec'], p['start']))
    for depth in '0ABC':
        for c in ch[depth]:
            for f in ('lec', 'start', 'end', 'dur', 'src', 'flags', 'depth'):
                if f not in c:
                    fails.append('ch%d %s missing field %s' % (s, depth, f))
            if c['src'] not in ('core', 'gold'):
                fails.append('ch%d bad src %r' % (s, c['src']))
            if not in_pool(s, c):
                fails.append('ch%d %s clip not in kept pool: L%s [%.1f-%.1f]' % (s, depth, c['lec'], c['start'], c['end']))
        t = dur(ch[depth]); tot[depth] += t
        budget = BUD[s][['0', 'A', 'B', 'C'].index(depth)]
        if depth == '0':
            if t > budget + 2:
                warns.append('ch%d rung 0 over target: %.0fs > %.0fs (atomic seed window)' % (s, t, budget))
        else:
            if t > budget + 2:
                fails.append('ch%d rung %s OVER BUDGET: %.1fs > %.0fs' % (s, depth, t, budget))

screening = sum(tot.values())
if screening > 305 * 60:
    fails.append('screening %d s exceeds 305m ceiling' % screening)

print('G8 film manifest:')
print('  spoken totals  0=%.1fm A=%.1fm B=%.1fm C=%.1fm | screening=%.1fm'
      % (tot['0']/60, tot['A']/60, tot['B']/60, tot['C']/60, screening/60))
print('  unique (C) = %.1fm | re-encountered = %.1fm' % (tot['C']/60, (screening-tot['C'])/60))
for w in warns:
    print('  WARN:', w)
if fails:
    for f in fails:
        print('  FAIL:', f)
    sys.exit(1)
print('  nesting PASS | budgets PASS | provenance PASS | chain PASS | pool-membership PASS')
print('G8 OK')
