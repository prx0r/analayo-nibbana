"""Audit seam safety of a cutplan: print transcript context at every keep boundary.
Usage: python3 audit_seams.py <lec> [transcript.txt]
Shows the 2 segments before each keep-start and 2 segments after each keep-end.
"""
import json, re, sys, os

lec = f"{int(sys.argv[1]):02d}"
D = "/home/box/Downloads/yt/analayo-nibbana"
plan = json.load(open(f"{D}/lecture-{lec}.cutplan.json"))
if len(sys.argv) > 2:
    tf = sys.argv[2]
else:
    tf = next((p for p in (f"/tmp/opencode/lec{lec}_cf.txt", f"/tmp/opencode/lec{lec}_yt.txt")
               if os.path.exists(p)), None)
assert tf and os.path.exists(tf), "no transcript found"

segs = []
for line in open(tf, errors="replace"):
    m = re.search(r"(\d+(?:\.\d+)?)-\s*(\d+(?:\.\d+)?)\s+(.+)", line)
    if m:
        segs.append((float(m.group(1)), float(m.group(2)), m.group(3).strip()))
segs.sort()

def mm(s):
    return f"{int(s//60)}:{s%60:04.1f}"

for k in plan["kept_segments"]:
    a, b = k["start"], k["end"]
    prev = [s for s in segs if s[1] <= a + 0.15][-2:]
    nxt = [s for s in segs if s[0] >= b - 0.15][:2]
    print(f"\n== KEEP {mm(a)}-{mm(b)} [{k['grade']}] ==")
    for s in prev:
        print(f"  PRE  {mm(s[0])}-{mm(s[1])}  {s[2][:110]}")
    for s in nxt:
        print(f"  POST {mm(s[0])}-{mm(s[1])}  {s[2][:110]}")
