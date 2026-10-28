# Rebuild below-lines + TTS lines from verbatim. Deterministic.
# Rules: below = gloss(verbatim); TTS = spoken version (no leading Pali,
# parens become pauses, no trailing dashes). Verify with verify.sh.
import json
import re
import unicodedata

D = '/root/analayo-nibbana'
td = D + '/build'  # axiom 13: builders target build/, not /tmp

exec(open(D + '/build/fish_filter.py').read().split('# below-line')[0])
blunt = json.load(open(D + '/build/blunt_key.json'))
blunt.sort(key=lambda x: -len(x[0]))

CIT = re.compile(r'\b(MN|SN|AN|DN|MA|SĀ|EA|T|Snp|Ud|Iti|Thag|Thig|Dhp)\b|\d+[./:]\d+')
FUNC = set('the,a,an,is,are,was,were,be,been,am,and,or,but,of,to,in,on,for,with,by,from,as,at,this,that,these,those,he,she,they,we,you,not,no,so,if,then,than,there,here,when,where,which,who,what,how,all,do,does,did,have,has,had,will,would,shall,should,may,might,must,an,is,are,his,her,their,our,your,my,me,him,us,them'.split(','))


def is_en(s):
    w = [x.strip('.,;:!?()"').lower() for x in s.split()]
    w = [x for x in w if x]
    if not w:
        return True
    return sum(1 for x in w if x in FUNC) / len(w) >= 0.2


def gloss(t):
    t = re.sub(r'\s+', ' ', t)

    def clean_paren(m):
        inner = m.group(1)
        for pat, _ in PALI2EN:
            try:
                if re.search(pat, inner, re.I):
                    return ''
            except Exception:
                continue
        if len(inner.split()) <= 6 and not CIT.search(inner):
            return ''
        return m.group(0)
    t = re.sub(r'\(([^()]*)\)', clean_paren, t)
    seen = set()

    def repT(m, r):
        if r.lower() in seen:
            return r
        seen.add(r.lower())
        return '%s (%s)' % (m.group(0), r)
    for pat, r in PALI2EN:
        try:
            t = re.sub(pat, lambda m: repT(m, r), t, flags=re.I)
        except Exception:
            pass
    for pat, r in blunt:
        try:
            t = re.sub(pat, r, t, flags=re.I)
        except Exception:
            pass
    t = ''.join(c for c in unicodedata.normalize('NFKD', t) if not unicodedata.combining(c))
    t = re.sub(r'\s+([.,;:!?])', r'\1', t)
    t = re.sub(r'\bthe the\b', 'the', t, flags=re.I)
    t = re.sub(r'namely the everything', 'namely everything', t, flags=re.I)
    t = re.sub(r'\bthe (everything|anything|nothing)\b', r'\1', t, flags=re.I)
    return re.sub(r'\s+', ' ', t).strip()


def tts(t):
    t = re.sub(r'\*\*', '', t)
    t = re.sub(r'(?<!\w)\*(?!\w)', '', t)
    t = re.sub(r'\s+', ' ', t).strip()
    # drop a leading quoted Pali chunk (+ optional gloss paren) when English follows;
    # separator may be dash, colon, slash, or a plain sentence end
    for _ in range(2):
        m = re.match(r'^("[^"]{1,200}"\s*(?:\([^()]*\)\s*)?(?:—|:|/|\.)\s*)(.*)$', t, re.S)
        if not m:
            # bare leading Pali term (+ optional gloss paren) + dash/colon.
            # Word class includes comma (2026-10-28: "Animittanca bhavehi,
            # mananusayamujjaha — ..." slipped through on its comma).
            # Regen-diff proof: exactly 1 line changes corpus-wide, zero
            # English-head damage (drops need zero FUNC words + dash/colon).
            m = re.match(r'^([A-Za-z\u0101\u012b\u016b\u1e6d\u1e47\u1e43\u1e62\u1e6a\u1e44,\-]+(?:\s+[A-Za-z\u0101\u012b\u016b\u1e6d\u1e47\u1e43\u1e62\u1e6a\u1e44,\-]+){0,3}\s*(?:\([^()]*\)\s*)?(?:—|:)\s*)(.*)$', t, re.S)
        if m and m.group(2).strip():
            head = re.sub(r'\([^()]*\)', ' ', m.group(1))
            words = [x.strip('.,;:!?()"').lower() for x in head.split()]
            words = [x for x in words if x]
            if words and not any(w in FUNC or w in ('what', 'how', 'when', 'where', 'why') for w in words):
                t = m.group(2).strip()
                continue
        break
    # inline glosses in parens become pauses
    t = re.sub(r'\s*\(([^()]*)\)', r' — \1 — ', t)
    t = re.sub(r'\s*:\s*', ' — ', t)
    t = re.sub(r'\s*;\s*', ', ', t)
    t = re.sub(r'\s*/\s*', '. ', t)
    t = re.sub(r'\s*—\s*', ' — ', t)
    t = re.sub(r'\s+([.,])', r'\1', t)
    t = re.sub(r'(^|[.] )\s*-\s*', r'\1', t)
    t = re.sub(r'\s+—\s*\.', '.', t)
    t = re.sub(r'—(\s*—)+', '—', t)
    t = re.sub(r'^[—–-]\s*', '', t)
    t = re.sub(r'\s+', ' ', t).strip()
    t = re.sub(r'\bnamely\b,?', 'namely,', t, flags=re.I)
    parts = re.split(r'(?<=[.!?])\s+(?=["A-Z0-9])', t)
    parts = [x.strip() for x in parts if x.strip()]
    while len(parts) > 1 and not is_en(parts[0]):
        parts.pop(0)
    t = ' '.join(parts)
    return t.strip()


if __name__ == '__main__':
    for sn in range(1, 7):
        p = td + '/seg%d_script.json' % sn
        sc = json.load(open(p))
        for e in sc:
            v = e.get('nanananda_verbatim', '')
            if isinstance(v, list):
                b = ' / '.join(gloss(x) for x in v)
            else:
                b = gloss(v) if v else ''
            e['plain_english_below'] = b
            e['tts_line'] = tts(b)
        json.dump(sc, open(p, 'w'), indent=1)
    print('rebuilt all below+tts')
