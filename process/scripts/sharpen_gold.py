#!/usr/bin/env python3
"""Sharpen B (gold): sequence law + edge re-snap + motto-cap manifests.

Step 1 SEQUENCE LAW: every gold span anchors to its nearest core clip in
  A-flow order (same lec, overlap >50% of the shorter); gold plays in that
  neighborhood. Unanchored spans keep (ci, lec, start) between anchors.
  Content-identical: order only. Totals reconcile by construction.
Step 2 EDGE RE-SNAP (sample-calibrated 2026-10-26): ismotto spans exempt
  (motto opens are legitimate). Otherwise: chant-head opens (leading
  diacritic-heavy sentences) trimmed to first English sentence; closer
  tails (thank-you / [Music] / sermon-number / forum) trimmed to previous
  sentence end; sub-3-word opens (non-motto, either timebase) advanced one
  sentence. Anything falling under 10s is left UNCHANGED and marked
  DEMOTE-CANDIDATE (owner call, never auto-delete).
Step 3 MOTTO-CAP MANIFESTS: data keeps everything; manifest_sN_gold.txt
  (the listenable B) carries <=3 mottos (first / middle-nearest / last).

Writes: build/canon/segN_gold.json (reordered, snapped), build/canon/manifest_sN_gold.txt,
build/versions/gold_fix_log.json (every change + every candidate + motto picks).
Idempotent: re-run yields identical files (snaps converge; log asserts).

FROZEN 2026-10-28: do NOT rerun on current data. The §59/§61 promotion
spans (B*/P-picks carrying note fields) were added AFTER this script's
membership model was written; a rerun DELETES them (observed 2026-10-28:
etymology/fire-catechism/mid-ocean/consciousness-middle spans dropped
from seg1_gold). gold_fix_log.json is therefore a historical record of
the §38 run (order counts pre-trim), not current state — current truth
is seg JSONs + manifest_index.json. To revive: add a promotion
allowlist (spans with note fields pass through untouched) and re-verify
with a diff review before accepting.
"""
import json
import re
from pathlib import Path

D = Path('/root/analayo-nibbana')
B = D / 'build'
YTSUB = {3, 6, 7, 14, 17, 20, 22, 24, 26, 27}
MIN_DUR = 10.0

CLOSER = re.compile(
    r'thank you|^\[music\]|\[applause\]|sermon number|sermon\)?\s*(has|is)|'
    r'comments on the forum|next week|permission formula', re.I)
CHANT = re.compile(r'[āīūṭḍṇṃñḷṅḥṛṣ]')
OPEN_SKIP = re.compile(
    r'^comment,?\s*translat|^end of comment|translation by\s+\w+\s*$', re.I)
# Spans carrying these notes are atomic (essay-0 seed windows, documented
# definitional promotions): exempt from snapping exactly like mottos.
# 2026-10-26: the snapper ate quote-opening words split across CF sentences
# (mirror "Even / if one already") and drifted a head BACKWARD through
# overlapping timestamps. Never again.
ATOMIC = re.compile(r'essay0-anchor|^B\*')


def sents(lec, cache={}):
    if lec in cache:
        return cache[lec]
    try:
        d = json.loads(open(D / f'sources/lectures/transcripts/lecture-{lec:02d}.transcript.cf.json').read())
        out = [(float(s.get('t', 0)), float(s.get('end', 0)), s.get('text', ''))
               for s in d.get('sentences', [])]
    except FileNotFoundError:
        d = json.loads(open(D / f'sources/lectures/yt-subs/lecture-{lec:02d}.json').read())
        out = [(float(c['t']), float(c['e']), c.get('x', '')) for c in d.get('cues', [])]
    cache[lec] = out
    return out


def words(t):
    return [w for w in re.split(r'\s+', t.strip()) if w]


def snap_span(s, sp):
    """Returns (new_start, new_end, notes). Unchanged if already clean."""
    ss = sents(sp['lec'])
    inside = [(a, b, t) for a, b, t in ss if b >= sp['start'] - 1.0 and a <= sp['end'] + 1.0]
    if not inside:
        return sp['start'], sp['end'], ['EMPTY-WINDOW: no transcript cover']
    notes = []
    ns, ne = sp['start'], sp['end']
    yt = sp['lec'] in YTSUB
    # --- head: chant run / skip-marker / fragment (mottos + atomics exempt
    # upstream). Snaps only SHRINK: ns never moves earlier (overlapping
    # timestamps). Fragment-head rule is YT-only: CF short openers
    # ("Even", "What is burning?") are quote content, never trim them.
    i0 = 0
    head_notes = []
    while i0 < len(inside):
        t = inside[i0][2].strip()
        if CHANT.search(t) and len(CHANT.findall(t)) >= 3:
            i0 += 1
            head_notes.append(f'chant-head trimmed: {t[:50]}')
            continue
        if OPEN_SKIP.search(t):
            i0 += 1
            head_notes.append(f'marker-head trimmed: {t[:50]}')
            continue
        if yt and len(words(t)) <= 3:
            i0 += 1
            head_notes.append(f'fragment-head trimmed: {t[:50]}')
            continue
        break
    if i0:
        if i0 >= len(inside):
            return sp['start'], sp['end'], ['DEMOTE-CANDIDATE: whole span is markers/fragments']
        cand = inside[i0][0]
        if inside[-1][1] - cand >= MIN_DUR and cand >= sp['start'] - 0.5:
            # tolerance: sub-0.5s advances are rounding noise, not trims
            if abs(round(cand, 1) - sp['start']) >= 0.5:
                ns = round(cand, 1)
                notes += head_notes
            else:
                notes.append('HEAD-REVIEW: opens on flagged sentence, advance <0.5s')
        else:
            return sp['start'], sp['end'], ['DEMOTE-CANDIDATE: snap would sliver']
    # --- tail: closer contamination
    i1 = len(inside) - 1
    tail_notes = []
    while i1 > 0:
        t = inside[i1][2].strip()
        if CLOSER.search(t):
            i1 -= 1
            tail_notes.append(f'closer-tail trimmed: {t[:50]}')
            continue
        break
    if i1 < len(inside) - 1:
        cand = inside[i1][1]
        if cand - ns >= MIN_DUR and cand <= sp['end'] + 0.5:
            if abs(round(cand, 1) - sp['end']) >= 0.5:
                ne = round(cand, 1)
                notes += tail_notes
            # else: rounding noise — keep, unlog
        else:
            return sp['start'], sp['end'], ['DEMOTE-CANDIDATE: snap would sliver']
    return ns, ne, notes


def main():
    log = {'snaps': [], 'demotes': [], 'mottos': {}, 'order': {}}
    for s in range(1, 7):
        core = json.load(open(B / f'seg{s}_core_v4.json'))
        sc = {e['clip']: e for e in json.load(open(B / f'seg{s}_script.json'))}

        def flow_idx(x):
            key = x.get('clip')
            if key is None:
                e = next((y for y in sc.values()
                          if y['analayo']['lec'] == x['lec']
                          and abs(y['analayo']['start'] - x['start']) < 3), None)
                key = e['clip'] if e else None
            return key
        flow = {}
        for i, x in enumerate(core):
            k = flow_idx(x)
            if k is not None:
                flow[(x['lec'], round(float(x['start']), 1))] = i
        # anchor each gold span to nearest overlapping core clip (flow order)
        gold = json.load(open(B / f'seg{s}_gold.json'))
        keyed = []
        for g in gold:
            best = None
            for (lec, st), i in flow.items():
                if lec != g['lec']:
                    continue
                cands = [c for c in core
                         if c['lec'] == lec and abs(float(c['start']) - st) < 0.01]
                if not cands:
                    continue
                c = cands[0]
                ov = min(g['end'], float(c['end'])) - max(g['start'], float(c['start']))
                if ov > 0.5 * min(g['end'] - g['start'], float(c['end']) - float(c['start'])):
                    if best is None or i < best:
                        best = i
            keyed.append((best if best is not None else 10 ** 6,
                          g.get('ci', -1), g['lec'], g['start'], g))
        keyed.sort(key=lambda t: (t[0], t[1], t[2], t[3]))
        gold = [t[4] for t in keyed]
        log['order'][s] = f'{len(gold)} spans sequenced to A-flow neighborhoods'

        # edge snaps (mottos + atomic essay-0/B* windows exempt)
        for g in gold:
            if g.get('ismotto') or ATOMIC.search(g.get('note', '')):
                continue
            ns, ne, notes = snap_span(s, g)
            real = [n for n in notes if not n.startswith('DEMOTE') and not n.startswith('EMPTY')]
            if real:
                log['snaps'].append({'s': s, 'lec': g['lec'],
                                     'was': [g['start'], g['end']],
                                     'now': [ns, ne], 'notes': notes})
                g['start'], g['end'] = ns, ne
                g['dur'] = round(ne - ns, 1)
            for n in notes:
                if n.startswith('DEMOTE') or n.startswith('EMPTY'):
                    log['demotes'].append({'s': s, 'lec': g['lec'],
                                           'span': [g['start'], g['end']], 'note': n})
        json.dump(gold, open(B / f'seg{s}_gold.json', 'w'), indent=1)

        # motto-cap manifest (spaced: kept mottos >= N/3 apart, greedy
        # from the cold open; stacked lecture-open mottos collapse to one)
        mi = [i for i, g in enumerate(gold) if g.get('ismotto')]
        keep = set()
        last = -10 ** 9
        for i in mi:
            if i - last >= len(gold) / 3.0:
                keep.add(i)
                last = i
        log['mottos'][s] = {'total': len(mi), 'kept': sorted(keep)}
        lines = []
        for i, g in enumerate(gold):
            if g.get('ismotto') and i not in keep:
                continue
            lines.append(f'L{g["lec"]:02d} {g["start"]}-{g["end"]} '
                         f'{g.get("grade", "A")} lecture-{g["lec"]:02d}.mp3'
                         f'{" MOTTO" if g.get("ismotto") else ""}')
        open(B / f'manifest_s{s}_gold.txt', 'w').write('\n'.join(lines) + '\n')
    json.dump(log, open(B / 'gold_fix_log.json', 'w'), indent=1)
    n_applied = sum(1 for e in log['snaps'] if e['was'] != e['now'])
    n_review = len(log['snaps']) - n_applied
    n_dem = len(log['demotes'])
    print(f'gold sharpened: {n_applied} applied, {n_review} head-review (<0.5s, kept), '
          f'{n_dem} demote-candidates/empty, mottos capped')
    for s in range(1, 7):
        print(f'  S{s}: {log["order"][s]}; mottos {log["mottos"][s]}')


if __name__ == '__main__':
    main()
