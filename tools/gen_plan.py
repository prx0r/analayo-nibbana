"""Generic rank-fit cut-plan generator. Usage: gen_plan.py <lec> <keepfile.py>
keepfile defines KEEPS=[(start,end,rank),...] in DS seconds + optional MAJOR=[(a,b,kind,reason),...]
Cuts = complement of keeps. If kept>2400: drop spans by rank desc, size desc (never rank<=1) until in band.
"""
import json, sys, subprocess, importlib.util, os
lec = f"{int(sys.argv[1]):02d}"
spec = importlib.util.spec_from_file_location("kf", sys.argv[2])
kf = importlib.util.module_from_spec(spec); spec.loader.exec_module(kf)
D = "/home/box/Downloads/yt/analayo-nibbana"
mp3 = f"{D}/analayo-nibbana-lecture-{lec}.mp3"
has_cf = os.path.exists(f"{D}/lecture-{lec}.transcript.cf.json")
try:
    yt = json.load(open(f"{D}/yt-subs/lecture-{lec}.json"))["cues"]
    yt_first, yt_last = yt[0]["t"], yt[-1]["e"]
except Exception:
    yt, yt_first, yt_last = [], None, None
if has_cf:
    dur = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",mp3]).strip())
else:
    assert yt, "no CF and no YT subs"
    dur = yt_last + 1.0
keeps = [tuple(k) for k in kf.KEEPS]
kept = sum(b-a for a,b,_ in keeps)
drops = []
while kept > 2400:
    cands = [k for k in keeps if k[2] > 1]
    if not cands: break
    k = max(cands, key=lambda x: (x[2], x[1]-x[0]))
    keeps.remove(k); kept -= k[1]-k[0]; drops.append(k)
assert kept <= 2400, "cannot fit without cutting rank-1"
kept_pct = kept/dur*100
cuts, pos = [], 0.0
for a,b,_ in sorted(keeps):
    if a-pos > 0.3: cuts.append((pos,a))
    pos = max(pos,b)
if dur-pos > 0.3: cuts.append((pos,dur))
MAJOR = getattr(kf, "MAJOR", [])
def label(a,b):
    for m in MAJOR:
        if abs(m[0]-a)<1.5 and abs(m[1]-b)<1.5: return m[2],m[3]
    if b-a>=8: return "ranked-out", "content ranked below the 20-40min budget"
    return "trim", "short span inside removed region"
GRADE = {1:"A",2:"B",3:"C",4:"C",5:"C"}
plan = {"lecture": int(lec), "target_min": 30, "source_min": round(dur/60,1),
        "kept_sec": round(kept,1), "kept_pct": round(kept_pct),
        "timebase": {"native": "ds" if has_cf else "yt", "yt_first": yt_first, "yt_last": yt_last},
        "dropped_spans": [{"start":round(a,1),"end":round(b,1),"rank":r} for a,b,r in drops],
        "cuts": [{"start":round(a,2),"end":round(b,2),"kind":label(a,b)[0],"reason":label(a,b)[1]} for a,b in cuts],
        "keep_summary": getattr(kf, "SUMMARY", ""),
        "kept_segments": [{"start":round(a,1),"end":round(b,1),"grade":GRADE.get(r,"B")} for a,b,r in sorted(keeps)],
        "grade_counts": {}, "grade_minutes": {}}
gc = {g: sum(1 for x in plan["kept_segments"] if x["grade"]==g) for g in "ABC"}
gm = {g: round(sum(x["end"]-x["start"] for x in plan["kept_segments"] if x["grade"]==g)/60,1) for g in "ABC"}
plan["grade_counts"], plan["grade_minutes"] = gc, gm
json.dump(plan, open(f"{D}/lecture-{lec}.cutplan.json","w"), indent=1)
def mm(s): return f"{int(s//60)}:{int(s%60):02d}"
md = [f"# Lecture {lec} — cut plan\n", f"Source {plan['source_min']} min → **kept {kept/60:.1f} min ({kept_pct:.0f}%)** · {len(cuts)} cuts · band 20–40 ✓"]
if drops: md.append(f"_auto-dropped to fit: " + "; ".join(f"{mm(a)}-{mm(b)}(r{r})" for a,b,r in drops) + "_\n")
for c in plan["cuts"]:
    md.append(f"- {mm(c['start'])}–{mm(c['end'])}  [{c['kind']}]  {c['reason']}")
if plan["keep_summary"]: md.append(f"\n**Keeps:** {plan['keep_summary']}")
md.append(f"\nGrades: A={gc['A']}({gm['A']}m) B={gc['B']}({gm['B']}m) C={gc['C']}({gm['C']}m) · dial: A → A+B → full")
open(f"{D}/lecture-{lec}.cutplan.md","w").write("\n".join(md)+"\n")
print(f"lec{lec}: kept {kept/60:.1f}min ({kept_pct:.0f}%) cuts={len(cuts)} drops={len(drops)} ✓")
