"""Auto-keeps generator implementing A/B/C/D.
A=rank1 spine+technical (never dropped), B=rank2 flow (drop if must),
C=rank3 boring (drop first), D=cut outright (forum/recap/Pali/2nd-trans/closer).
Usage: python3 tools/auto_keeps.py <lec>
Writes tools/lecNN_keeps.py draft. Human reviews md after gen_plan.
"""
import json, re, sys, os
lec = f"{int(sys.argv[1]):02d}"
D = "/root/analayo-nibbana"
cf_path = f"{D}/sources/lectures/transcripts/lecture-{lec}.transcript.cf.json"
yt_path = f"{D}/sources/lectures/yt-subs/lecture-{lec}.json"
has_cf = os.path.exists(cf_path)
if has_cf:
    d = json.load(open(cf_path))
    segs = sorted(d["sentences"], key=lambda s: s["t"])
    dur = d["duration"]
    TB = "ds"
else:
    y = json.load(open(yt_path))
    cues = y["cues"]
    # convert cues to segs
    segs = [{"t": c["t"], "end": c["e"], "text": c["x"]} for c in cues]
    dur = cues[-1]["e"] + 1.0
    TB = "yt"

def mm(s): return f"{int(s//60)}:{int(s%60):02d}"
texts = [s["text"] for s in segs]

# 1. Find motto / sermon start (D cut before it)
motto_idx = next((i for i,s in enumerate(segs) if "this is peaceful" in s["text"].lower()), None)
if motto_idx is None:
    motto_idx = next((i for i,s in enumerate(segs) if "this is the" in s["text"].lower() and "sermon" in s["text"].lower()), 0)
motto_start = segs[motto_idx]["t"]
# permission/intro end: first 6 segs after motto
intro_end = segs[min(motto_idx+6, len(segs)-1)]["end"]
# sermon number for recap detection
# 2. Find spine start: first of these markers after intro
spine_marks = ["how did", "in order to clarify", "there is a special significance",
               "let us now consider", "in contradistinction", "we can draw upon",
               "now, it is extremely clear", "so what we have here", "the buddha pointed out"]
spine_idx = None
for i in range(motto_idx, len(segs)):
    low = segs[i]["text"].lower()
    if any(m in low for m in spine_marks) and segs[i]["t"] > intro_end:
        spine_idx = i
        break
if spine_idx is None:
    spine_idx = min(motto_idx+12, len(segs)-1)
spine_start = segs[spine_idx]["t"]

# 3. Second-translation blocks (D cut). Start regex, end at next End within 150s else 4 sentences.
cuts = []  # (a,b,kind,reason)
cuts.append((0.0, motto_start, "forum", "course welcome + forum discussion + bridge"))
# chant gap motto->permission handled by complement (small gaps become trim)
cuts.append((segs[motto_idx]["end"], segs[min(motto_idx+1,len(segs)-1)]["t"] if motto_idx+1 < len(segs) else segs[motto_idx]["end"]+1, "chant", "motto-to-permission gap"))
# recap: intro_end to spine_start, BUT cap at 180s (lecture-specific spines vary;
# an over-long recap cut nukes the sermon, e.g. lec13). Prefer keyword end.
recap_end_candidates = []
for i in range(motto_idx, len(segs)):
    if segs[i]["t"] < intro_end:
        continue
    if segs[i]["t"] > intro_end + 600:
        break
    low = segs[i]["text"].lower()
    if any(k in low for k in ["it is described", "it is said", "in these words", "let us bring up",
                              "so today", "to begin with", "this is how", "this discourse"]):
        recap_end_candidates.append(segs[i]["t"])
        break
if spine_start - intro_end > 15:
    if spine_start - intro_end > 240:
        # cap: use keyword end or intro+150s
        cap = recap_end_candidates[0] if recap_end_candidates else intro_end + 150
        cuts.append((intro_end, cap, "recap", "previous-sermon recap + lead-in (capped)"))
    else:
        cuts.append((intro_end, spine_start, "recap", "previous-sermon recap + extremes lead-in"))
start_re = re.compile(r"(comment.*translat|translat.*by|common.*translat|translation by)", re.I)
end_re = re.compile(r"end of (comment|quote|count)", re.I)
i = 0
while i < len(segs):
    if start_re.search(segs[i]["text"]):
        a = segs[i]["t"]
        # find end within 150s
        j = i
        found = None
        while j < len(segs) and segs[j]["t"] - a <= 150:
            if end_re.search(segs[j]["text"]):
                found = j
                break
            j += 1
        if found is not None:
            b = segs[found]["end"]
            cuts.append((a, b, "translation", f"second translation: {segs[i]['text'][:60]}"))
            i = found + 1
            continue
        else:
            # no End nearby: cut 4 sentences max (~60s) to avoid mega-merge
            k = min(i+4, len(segs)-1)
            b = segs[k]["end"]
            cuts.append((a, b, "translation", f"second translation (unclosed, 4-seg cap): {segs[i]['text'][:60]}"))
            i = k + 1
            continue
    i += 1
# Pali gaps >=8s (D cut gap only; keeps complement handles)
for k in range(len(segs)-1):
    g = segs[k+1]["t"] - segs[k]["end"]
    if g >= 8:
        cuts.append((segs[k]["end"], segs[k+1]["t"], "pali", "Pali recitation / chant gap"))
# closer: LAST thank-you to end (first thank-you is often mid-lecture acknowledgement)
thanks = [s for s in segs if "thank you" in s["text"].lower()]
if thanks:
    # take last thank-you occurring after 70% of duration, else last overall
    late = [s for s in thanks if s["t"] > dur*0.7]
    t0 = (late[0] if late else thanks[-1])["t"]
    cuts.append((t0, dur, "closer", "comment + thanks closer"))
else:
    cuts.append((dur-30, dur, "closer", "closing tail"))

# Build keeps = complement of cuts, snapped to sentence boundaries is automatic
cuts = sorted([c for c in cuts if c[1]-c[0] > 0.5], key=lambda c: c[0])
# merge overlapping cuts
merged = []
for a,b,k,r in cuts:
    if merged and a <= merged[-1][1] + 0.05:
        merged[-1][1] = max(merged[-1][1], b)
    else:
        merged.append([a,b,k,r])
keeps_raw = []
pos = 0.0
for a,b,k,r in merged:
    if a-pos > 1.0:
        keeps_raw.append((pos, a))
    pos = max(pos, b)
if dur-pos > 1.0:
    keeps_raw.append((pos, dur))
# snap keeps to nearest sentence boundaries
def snap(a,b):
    sa = min(segs, key=lambda s: abs(s["t"]-a))
    sb = min(segs, key=lambda s: abs(s["end"]-b))
    return (sa["t"], sb["end"])
keeps = []
for a,b in keeps_raw:
    if b-a < 2.0:
        continue
    sa,sb = snap(a,b)
    if sb-sa > 1.5:
        keeps.append((round(sa,2), round(sb,2)))
# Rank: default 1. Rank3 (C boring) if span text hits >=2 boring keywords or 1 strong.
# Split keeps >180s into ~120-150s sentence-snapped chunks FIRST for surgical drops.
boring_strong = ["chinese parallel","tibetan","sanskrit parallel","upanishad","jain-borrowing","hagiography",
                 "version uncertainty","literalism theory","out-of-body","levitation","iands","mbsr",
                 "second translation","restatement","reprise","re-telling","comparative study","article citation"]
boring_weak = ["chinese","tibetan","sanskrit","parallel","upanishad","vedic","jain","article","scholar",
               "commentary","hagiography","uncertainty","levitation","out-of-body","reprise","restatement",
               "re-tell","comparative","translation-workshop","borrowing","debate"]
def rank_chunk(a, b):
    txt = " ".join(s["text"] for s in segs if s["t"] >= a-0.3 and s["end"] <= b+0.3).lower()
    strong = sum(1 for k in boring_strong if k in txt)
    weak = sum(1 for k in boring_weak if k in txt)
    durk = b-a
    if strong >= 1 or weak >= 4 or weak >= 2 and durk > 100:
        if durk < 60 and any(c in txt for c in ["verse","simile","parable","this is peaceful","this is excellent"]):
            return 1
        return 3
    if durk >= 100:
        return 2
    if weak >= 2:
        return 3
    return 1
chunked = []
for a,b in keeps:
    inside = [s for s in segs if s["t"] >= a-0.2 and s["end"] <= b+0.2]
    if b-a <= 180 or len(inside) <= 3:
        chunked.append((a,b))
        continue
    # accumulate ~130s chunks
    cur_start = inside[0]["t"]
    cur_t = cur_start
    for s in inside:
        if s["end"]-cur_start >= 130 and s["end"]-cur_start > 60:
            # end chunk at s
            chunked.append((round(cur_start,2), round(s["end"],2)))
            # next starts at next sentence
            nxt = inside[inside.index(s)+1] if inside.index(s)+1 < len(inside) else None
            cur_start = nxt["t"] if nxt else s["end"]
    if cur_start < b-1.0:
        chunked.append((round(cur_start,2), round(b,2)))
ranked = []
for a,b in chunked:
    ranked.append((a,b,rank_chunk(a,b)))
# Protect conclusion: last 2 chunks before closer -> rank1 (close must survive)
if len(ranked) >= 2:
    a1,b1,r1 = ranked[-1]
    a2,b2,r2 = ranked[-2]
    ranked[-1] = (a1,b1,1)
    if r2 == 3:
        ranked[-2] = (a2,b2,2)  # downgrade C->B, don't force A
# Ensure motto + intro rank1 (only intro, NOT everything before spine)
out = []
for a,b,r in ranked:
    if a < intro_end and r > 1:
        r = 1
    out.append((a,b,r))
total = sum(b-a for a,b,r in out)
print(f"lec{lec}: TB={TB} dur={dur/60:.1f}m keeps={len(out)} raw_kept={total/60:.1f}m cuts={len(merged)}")
for a,b,r in out:
    print(f"  KEEP {mm(a)}-{mm(b)} r{r} ({b-a:.0f}s)")
# write keeps file
with open(f"{D}/tools/lec{lec}_keeps.py","w") as f:
    f.write(f"# Lecture {int(lec)} keeps — {TB} timebase (source {dur/60:.1f} min)\n")
    f.write(f"# A=rank1 spine+technical (keep), B=rank2 flow (drop if must), C=rank3 boring (drop first), D=cut in MAJOR\n")
    f.write("KEEPS = [\n")
    for a,b,r in out:
        f.write(f"    ({a}, {b}, {r}),\n")
    f.write("]\n\nMAJOR = [\n")
    for a,b,k,r in merged:
        f.write(f'    ({round(a,2)}, {round(b,2)}, "{k}", "{r[:100]}"),\n')
    f.write("]\n\nSUMMARY = (\"AUTO DRAFT — review skeleton before ship\")\n")
print(f"wrote tools/lec{lec}_keeps.py")
