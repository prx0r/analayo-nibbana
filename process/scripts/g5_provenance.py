"""G5 provenance gate — called by process/verify.sh.

Semantic test: every nanananda_verbatim must sit BETWEEN QUOTE MARKS
in some sermon-*.md source file (whitespace/markdown normalized).

History: the earlier set-membership version built its span set with a
naive "..." pairing regex — sermon-30 has a quote-parity shift (stray
quote earlier), which paired LABELS instead of CONTENT, so a
semantically-valid quote would have been rejected. The anchor test
("quote + text + quote" contiguous) is immune to pairing errors
because it does not depend on where pairing starts.

Inline-in-shell version of this check (python3 -c inside verify.sh)
failed on quote escaping — second casualty of M-A4 (complex python
never inlines into shell strings). Standalone file, file-mode tested.
"""
import glob
import json
import os
import re
import sys

SRC = '/tmp/satsang-ext/53-nibbana-scaffold/sermon-*.md'
# Portable resolution (2026-10-28): repo-vendored sources/ first, then
# $SERMON_SCAFFOLD_DIR override, then the legacy /tmp path. Fail loud
# listing every path tried.
def _resolve_src():
    here = os.path.dirname(os.path.abspath(__file__))
    cands = [
        os.path.normpath(os.path.join(here, '..', '..', 'sources',
                                      '53-nibbana-scaffold', 'sermon-*.md')),
        os.path.join(os.environ.get('SERMON_SCAFFOLD_DIR', ''), 'sermon-*.md')
        if os.environ.get('SERMON_SCAFFOLD_DIR') else None,
        SRC,
    ]
    for pat in [c for c in cands if c]:
        if glob.glob(pat):
            return pat
    print('G5: no sermon scaffold found. Tried:')
    for pat in [c for c in cands if c]:
        print('  -', pat)
    return None


def norm(t):
    return re.sub(r'\s+', ' ', re.sub(r'\*', '', t))


def normstrip(t):
    t = norm(t).strip()
    if ((t.startswith(chr(34)) and t.endswith(chr(34))) or
            (t.startswith(chr(8220)) and t.endswith(chr(8221)))):
        t = t[1:-1]
    return t.strip()


def main():
    pat = _resolve_src()
    if pat is None:
        print('G5 PROVENANCE FAILED (no scaffold)')
        return 1
    files = [norm(open(f).read()) for f in sorted(glob.glob(pat))]
    bad, total, miss = 0, 0, []
    for s in range(1, 7):
        for e in json.load(open('build/seg%d_script.json' % s)):
            v = e.get('nanananda_verbatim', '')
            for q in (v if isinstance(v, list) else [v]):
                if not q:
                    bad += 1
                    miss.append((s, e['clip'], 'EMPTY'))
                    continue
                total += 1
                qn = normstrip(q)
                if not any((chr(34) + qn + chr(34)) in raw for raw in files):
                    bad += 1
                    miss.append((s, e['clip'], qn[:60]))
    # Essay-0 TEXT (build/essay0.json, canonical) bypasses the scripts —
    # anchor it too (S2 triple, owner 2026-10-28). Same rule, no exceptions.
    for _u in json.load(open('build/essay0.json'))['units'].values():
        v = _u.get('text', '')
        for q in (v if isinstance(v, list) else [v]):
            total += 1
            qn = normstrip(q)
            if not any((chr(34) + qn + chr(34)) in raw for raw in files):
                bad += 1
                miss.append(('essay0', _u.get('question', '')[:30], qn[:60]))
    print('G5 provenance %d/%d (semantic quote-anchor)' % (total - bad, total))
    if bad:
        for m in miss[:8]:
            print('  FAIL', m)
        print('G5 PROVENANCE FAILED (%d)' % bad)
        return 1
    print('OK')
    return 0


if __name__ == '__main__':
    sys.exit(main())
