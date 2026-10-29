"""G6b hardened TTS gate — called by process/verify.sh.

Catches what the plain G6 missed (documented in REVIEW.md section D):
  G6a  punctuation hygiene + diacritics (inherited from old G6)
  G6b  leading non-English word-run (the S5b2 class: a Pali sentence
       opening the line). Self-tests with a CANARY: the known-bad
       pre-fix S5b2 line is embedded below, and the gate fails LOUD
       if its detector ever stops flagging it. The gate proves itself
       on every run.
  G6c  every mid-sentence Pali token must be either gloss-attached
       (a dash/paren/comma/quote marker within +-40 chars) or on the
       APPROVED list, where every entry carries its reason.

Design notes (MISTAKES.md M-A4): an earlier detector used a +-40
"window" that was CIRCULAR — the dash terminating the leading Pali
run sat inside the window and passed the run as "glossed". Fixed by
splitting the checks: leading-run detection is positional (before
first punctuation), term-attachment is marker-based. Both directions
of marker search, because glosses may precede ("that is to say',
yadidam") or follow ("asava, influx").
"""
import json
import re
import sys
import unicodedata

FUNC = set('the,a,an,is,are,was,were,be,and,or,but,of,to,in,on,for,with,'
           'as,at,this,that,it,he,she,they,we,you,not,no,so,if,then,than,'
           'there,here,when,where,which,who,what,how,all,do,does,did,have,'
           'has,had,will,would,can,could,shall,should,may,might,must,by,'
           'from,into,its,itself,them,his,her,our,your,my,i,am,me,us'.split(','))

PALI = re.compile(
    r'\b(asavasamudaya|avijjasamudayo|avijja|paticca|samuppada|samuppanna|'
    r'yadidam|abhisaikhata|janami|passami|etam|dhono|mannati|ditthasutam|'
    r'mutesu|satipatthana|sammappadhana|paramasana|asava|'
    r'papancasannasankha|yathabhuta|tanhakkhayo|arahant|dhamma|tathagata|'
    # ASCII-folded inflected forms found in corpus 2026-10-28 (S5c15/S6c15:
    # NFKD folding defeats the diacritic forms above; tts lead-drop now
    # strips the S5c15 lead, these guard the rest)
    r'animittanca|mananusaya|upadinna|anupadinna|bhavehi|samsara|samsaric)\b')

APPROVED = {
    'arahant': 'loanword, corpus-standard spoken form (7x)',
    'dhamma': 'loanword (the teaching)',
    'tathagata': 'loanword (title)',
    'janami': 'quoted citation unit; English gloss precedes ("I know, I see")',
    'passami': 'same citation unit as janami',
    'etam': 'same citation unit; English gloss precedes',
    'asavasamudaya': 'Pali citation unit wrapped by English gloss (influxes)',
    'avijjasamudayo': 'Pali citation unit; English gloss wraps (not seeing how it works)',
    'paticca': 'formula term; key gloss attaches on first use (paticca samuppada)',
    'samuppada': 'formula term; same unit as paticca',
    'samuppanna': 'citation unit; English gloss precedes (things dependently arisen)',
    'yadidam': "gloss precedes: 'that is to say', yadidam",
    'samsara': 'loanword, corpus-standard spoken form (owner 2026-10-28)',
    'samsaric': 'same standing as samsara',
}

# The pre-fix S5b2 line. If this ever stops being flagged, G6b's
# detector is broken and this gate must fail.
CANARY = ("Dhono na hi tena mannati yadidam ditthasutam mutesu va - "
          "the arahant does not imagine 'thereby', namely by whatever is "
          "seen, heard and sensed.")


def strip_dia(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn').lower()


def has_leading_pali_run(t):
    """A >=3-word non-English run before the first punctuation."""
    t = re.sub(r'[*"()]', '', t)
    for chunk in re.split(r'(?<=[.!?])\s+', t):
        m = re.match(r'^([A-Za-z][A-Za-z\'\-]*(?:\s+[A-Za-z][A-Za-z\'\-]*){2,})'
                     r'\s*(?:—|-|:|,|\.)', chunk)
        if m:
            words = [w.lower() for w in m.group(1).split()]
            # True class: >=4 words with ZERO English function words.
            # (ratio thresholds false-flag dense English content sentences:
            #  "Once gone beyond", "Those wise ones get extinguished"...)
            if len(words) >= 4 and not any(w in FUNC for w in words):
                return True
    return False


def attached(line, m):
    """A gloss marker (dash/paren/comma/quote) within 40 chars either side."""
    after = line[m.end():m.end() + 40]
    before = line[max(0, m.start() - 40):m.start()]
    if re.search(r'[—(,]\s*[a-zA-Z]', after):
        return True
    if re.search(r'[—(,]\s*[a-zA-Z]', before):
        return True
    if re.search(r"'[A-Za-z][^']*'\s*,?\s*$", before.rstrip()):
        return True
    if re.search(r"'[A-Za-z][^']*", after):
        return True
    return False


def main():
    bad = []
    # --- G6a: punctuation + diacritics
    for s in range(1, 7):
        for e in json.load(open('build/canon/seg%d_script.json' % s)):
            t = e.get('tts_line', '')
            if re.search(r'[—:;] *$|\(|\)|^[-\—]|  | $', t):
                bad.append((s, e['clip'], 'punct'))
            if re.search(r'[āīūṭḍṇṃñḷṅḥṛṣ]', t):
                bad.append((s, e['clip'], 'diacritic'))

    # --- G6b: canary first (gate proves itself), then the corpus
    if not has_leading_pali_run(CANARY):
        bad.append(('canary', 'fail',
                    'G6b DETECTOR BROKEN: did not flag the known-bad S5b2 line'))
    for s in range(1, 7):
        for e in json.load(open('build/canon/seg%d_script.json' % s)):
            if has_leading_pali_run(e.get('tts_line', '')):
                bad.append((s, e['clip'], 'leading-pali-run'))

    # --- G6c: term must be attached or approved
    for s in range(1, 7):
        for e in json.load(open('build/canon/seg%d_script.json' % s)):
            t = e.get('tts_line', '')
            for m in PALI.finditer(t):
                term = strip_dia(m.group(0))
                if term in APPROVED:
                    continue
                if not attached(t, m):
                    bad.append((s, e['clip'], 'unglossed:' + m.group(0)))

    if bad:
        print('tts issues:')
        for b in bad:
            print('  ', b)
        print('G6b HARDENED SCAN FAILED (%d)' % len(bad))
        return 1
    print('G6b hardened TTS scan: none (canary armed, %d approved terms)'
          % len(APPROVED))
    print('OK')
    return 0


if __name__ == '__main__':
    sys.exit(main())
