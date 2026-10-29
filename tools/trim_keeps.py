"""Seam-trim auto keeps: advance keep-starts past fragment/End/thanks openers,
retreat keep-ends before fragment/closer tails. Sentence-snapped. Max 4 steps each side.
Usage: trim_keeps.py <lec>  (rewrites tools/lecNN_keeps.py KEEPS only)
"""
import json, sys, re
lec = f"{int(sys.argv[1]):02d}"
D = "/root/analayo-nibbana"
d = json.load(open(f"{D}/sources/lectures/transcripts/lecture-{lec}.transcript.cf.json")) if __import__("os").path.exists(f"{D}/sources/lectures/transcripts/lecture-{lec}.transcript.cf.json") else None
if d is None:
    d = {"sentences": [{"t": c["t"], "end": c["e"], "text": c["x"]} for c in json.load(open(f"{D}/sources/lectures/yt-subs/lecture-{lec}.json"))["cues"]], "duration": 0}
segs = sorted(d["sentences"], key=lambda s: s["t"])

BAD_START = re.compile(r"^(end of (comment|quote|count|command)|thank you|\[music\]|comment\??|common[,.]?\s*(translation)?|translation by|commenter[,.]?)\b", re.I)

def bad_start(t):
    t = t.strip()
    if not t:
        return True
    if BAD_START.match(t):
        return True
    if len(t.split()) < 4:
        return True
    if t[0].islower():
        return True
    return False

def bad_end(t):
    t = t.strip()
    if not t:
        return True
    low = t.lower()
    if low.startswith("thank you"):
        return True
    if re.match(r"^(end of (comment|quote|count)|comment\??)$", t, re.I):
        return True
    if len(t.split()) < 4:
        return True
    if t.rstrip().endswith((",", "so", "as", "the", "to", "of", "and", "in", "is", "that")):
        return True
    return False

import importlib.util
spec = importlib.util.spec_from_file_location("kf", f"{D}/tools/lec{lec}_keeps.py")
kf = importlib.util.module_from_spec(spec); spec.loader.exec_module(kf)
new_keeps, n_trim = [], 0
for a, b, r in kf.KEEPS:
    inside = [s for s in segs if s["t"] >= a - 0.3 and s["end"] <= b + 0.3]
    if not inside:
        continue
    i, j = 0, len(inside) - 1
    steps = 0
    while i < j and bad_start(inside[i]["text"]) and steps < 8:
        i += 1; steps += 1
    steps = 0
    while j > i and bad_end(inside[j]["text"]) and steps < 8:
        j -= 1; steps += 1
    # motto protection: never trim a keep down to nothing; keep >=1 seg
    na, nb = inside[i]["t"], inside[j]["end"]
    if (a, b) != (round(na, 2), round(nb, 2)):
        n_trim += 1
    if nb - na > 1.0:
        new_keeps.append((round(na, 2), round(nb, 2), r))
print(f"lec{lec}: {len(kf.KEEPS)} -> {len(new_keeps)} keeps, trimmed {n_trim}")
# rewrite file preserving MAJOR + SUMMARY
src = open(f"{D}/tools/lec{lec}_keeps.py").read()
head = src.split("KEEPS = [")[0]
major = src.split("MAJOR = [", 1)[1]
keeps_txt = "KEEPS = [\n" + "".join(f"    ({a}, {b}, {r}),\n" for a, b, r in new_keeps) + "]"
open(f"{D}/tools/lec{lec}_keeps.py", "w").write(head + keeps_txt + "\nMAJOR = [" + major)
