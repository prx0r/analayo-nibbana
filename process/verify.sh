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
echo "== G5 provenance =="
python3 -c "
import json,glob,re
spans=set()
for f in sorted(glob.glob('/tmp/satsang-ext/53-nibbana-scaffold/sermon-*-excavation.md')):
  raw=open(f).read()
  for m in re.finditer(r'\"([^\"]{10,})\"', raw, re.S):
    spans.add(re.sub(r'\\s+',' ',re.sub(r'\*','',m.group(1))).strip().lower())
def normstrip(t):
  t=re.sub(r'\s+',' ',re.sub(r'\*','',t)).strip()
  if (t.startswith('\"') and t.endswith('\"')) or (t.startswith(chr(8220)) and t.endswith(chr(8221))): t=t[1:-1]
  return t.strip().lower()
bad=total=0
miss=[]
for s in range(1,7):
  for e in json.load(open('build/seg%d_script.json'%s)):
    v=e.get('nanananda_verbatim','')
    for q in (v if isinstance(v,list) else [v]):
      if not q: bad+=1; continue
      total+=1
      if normstrip(q) not in spans: bad+=1; miss.append((s,e['clip'],normstrip(q)[:60]))
print('provenance %d/%d'%(total-bad,total))
assert not bad, 'PROVENANCE FAILURES: %s' % miss[:5]
print('OK')"
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
echo "== files =="
for f in build/seg1_script.json build/seg6_script.json build/manifest_index.json build/fish_filter.py build/blunt_key.json SPEAKER-RULES.md; do
  [ -f "$f" ] || { echo "MISSING $f"; exit 1; }
done
echo "ALL GATES PASS"
