#!/usr/bin/env bash
# verify.sh — one-command audit. Fails loud.
set -e
cd "$(dirname "$0")/.."
echo "== G1 totals =="
python3 -c "
import json
pool=sum(sum(x['dur'] for x in json.load(open('build/seg%d_pool.json'%s))) for s in range(1,7))
print('pool total h: %.2f (expect ~20.70)'%(pool/3600))
assert 20.0 < pool/3600 < 21.5, 'TOTALS DO NOT RECONCILE'
print('OK')"
echo "== G5 provenance (semantic quote-anchor) =="
python3 process/scripts/g5_provenance.py || exit 1
echo "== G6 TTS scan =="
python3 -c "
import json,re
bad=[]
for s in range(1,7):
  for e in json.load(open('build/seg%d_script.json'%s)):
    t=e.get('tts_line','')
    if re.search(r'[—:;] *$|\(|\)|^[\-\—]|  | $', t): bad.append((s,e['clip'],'punct'))
    if re.search(r'[āīūṭḍṇṃñḷṅḥṛṣ]', t): bad.append((s,e['clip'],'diacritic'))
print('tts issues:', bad if bad else 'none')
assert not bad, 'TTS SCAN FAILURES'
print('OK')"
echo "== G6b hardened TTS gate (leading-Pali + term-attachment + canary) =="
python3 process/scripts/g6_tts_check.py || exit 1
echo "== G7 essay gates (structure + chain + essay-0 gold-dust) =="
python3 process/scripts/g7_essay_check.py || exit 1
echo "== G8 film manifest (nesting + budgets + provenance + chain) =="
python3 process/scripts/g8_film_check.py || exit 1
echo "== files =="

for f in build/seg1_script.json build/seg6_script.json build/manifest_index.json build/film_manifest.json FILM-CUT.md build/fish_filter.py build/blunt_key.json SPEAKER-RULES.md; do
  [ -f "$f" ] || { echo "MISSING $f"; exit 1; }
done
echo "ALL GATES PASS"
