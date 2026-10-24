#!/bin/bash
# usage: build_one.sh <lec>  — waits for transcript, builds trimmed cutplan + skeleton
lec=$1
D=/root/analayo-nibbana
while [ ! -s $D/lecture-${lec}.transcript.cf.json ]; do sleep 30; done
sleep 5
python3 $D/tools/auto_keeps.py $lec
python3 $D/tools/trim_keeps.py $lec | tail -n 1
python3 $D/tools/gen_plan.py $lec $D/tools/lec${lec}_keeps.py
python3 -c "
import json
d=json.load(open('$D/lecture-${lec}.transcript.cf.json'))
segs=sorted(d['sentences'], key=lambda s: s['t'])
plan=json.load(open('$D/lecture-${lec}.cutplan.json'))
print('===== LEC$lec kept=',round(plan['kept_sec']/60,1),'drops=',len(plan['dropped_spans']),'grades=',plan['grade_counts'])
def mm(s): return f'{int(s//60)}:{int(s%60):02d}'
bad=[]
for k in plan['kept_segments']:
    a,b=k['start'],k['end']
    inside=[s for s in segs if s['t']>=a-0.3 and s['end']<=b+0.3]
    f0=inside[0]['text'][:60] if inside else '?'
    print(f'[{k[\"grade\"]}] {mm(a)} {f0}')
    if not inside: bad.append(a)
    elif f0.strip().lower().startswith(('end of','thank you','[music]')): bad.append((round(a,1),f0[:40]))
print('bad:',bad if bad else 'none')
"
