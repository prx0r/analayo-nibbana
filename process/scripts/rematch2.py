"""ERA-1 SUPERSEDED (kept for method, 2026-10-28): pool builder from the
cutplan era. Reads/writes /tmp/opencode/condensed/ (vanished scratch).
Not run by verify.sh or any builder. Do not revive without re-pointing
I/O to build/."""
import json,re
clus={1:['motto','stilling','fire','lamp','wood','fuel','epithet','staircase','weaving','vaccha','annihilat','warming','third truth','thirst','well','two elements','oil-lamp','deathless','ocean','rivers','iron'],2:['wound','whirlpool','vortex','reeds','bundles','ruler','twelve','kaccayana','middle','banana','time'],3:['formal name','nominal','honey','blind','papancha','reckoning','colombo','delight','imagining','earth'],4:['mirror','anidassana','non-manifestative','signless','observer','tetralemma','foam','anatta'],5:['bahiya','only the seen','cinema','spectator','razor','satipatthana','relinquish','renunciation','raft'],6:['embers','lamp','oil-lamp','iron','ocean','lotus','faculties','seamstress','knots','chess','magic','close']}
D='/root/analayo-nibbana'
STOP=set('the,a,an,and,or,but,of,to,in,on,for,with,as,at,by,from,is,are,was,were,be,been,it,its,this,that,these,those,he,she,they,we,you,i,not,no,so,if,then,than,there,here,when,where,which,who,what,how,all,also,just,like,even,only,very,more,most,such,into,out,up,down,over,under,again,further,once,two,one,another,other,both,either,neither,because,while,although,though,since,until,unless,whereas,whether,whose,whom,do,does,did,doing,done,have,has,had,having,will,would,shall,should,may,might,must,can,could,say,said,buddha'.split(','))
def toks(t): return set(w.strip('.,;:!?()\"') for w in t.lower().split() if w.strip('.,;:!?()\"') not in STOP and len(w)>3)
def cliptext(x):
  import os
  p=D+'/lecture-%02d.transcript.cf.json'%x['lec']
  if os.path.exists(p):
    tr=json.load(open(p)); return ' '.join(s['text'] for s in tr['sentences'] if s['end']>x['start'] and s['t']<x['end']).lower()
  tr=json.load(open(D+'/yt-subs/lecture-%02d.json'%x['lec'])); cues=tr.get('cues',[])
  return ' '.join(c.get('x','') for c in cues if c.get('e',0)>x['start'] and c.get('t',0)<x['end']).lower()
pool={int(s):[(n,q) for n,q in v] for s,v in json.load(open('/tmp/opencode/condensed/quote_pool.json')).items()}
for s in range(1,7):
  core=json.load(open('/tmp/opencode/condensed/seg%d_core_v4.json'%s))
  pf=json.load(open('/tmp/opencode/condensed/seg%d_pool.json'%s))
  def clipci(x):
    best=None; bd=1e9
    for y in pf:
      if y['lec']==x['lec']:
        dd=abs(y['start']-x['start'])
        if dd<bd: bd=dd; best=y.get('ci',99)
    return best if bd<200 else 99
  script=[]; used=set()
  for i,x in enumerate(core):
    ci=clipci(x); ct=toks(cliptext(x))
    cands=[]
    for (serm,q) in pool[s]:
      if q in used: continue
      qcl=max(range(1,7), key=lambda j:(sum(k in q.lower() for k in clus[j]),-j))
      sc=len(ct & toks(q)) + (3 if serm==x['lec'] else 0) + (4 if qcl==s else -2)
      cands.append((sc,serm,q))
    cands.sort(reverse=True)
    serm,q=cands[0][1],cands[0][2]
    # motto clips get motto quote deterministically
    if x.get('ismotto') or 'stilling of all preparations' in cliptext(x) or 'namely distilling' in cliptext(x) or 'tanaka kayo' in cliptext(x):
      m=[(n2,q2) for n2,q2 in pool[s] if 'stilling of all preparations' in q2.lower() or 'namely the stilling' in q2.lower() or q2.lower().startswith('etam santam')]
      if m: serm,q=m[0]
    used.add(q)
    script.append({'clip':i+1,'analayo':{'lec':x['lec'],'start':x['start'],'end':x['end'],'dur':x['dur']},'nanananda_verbatim':q,'nanananda_sermon':serm,'cluster':ci})
  json.dump(script,open('/tmp/opencode/condensed/seg%d_script.json'%s,'w'),indent=1)
  print('S%d: %d beats'%(s,len(script)))
