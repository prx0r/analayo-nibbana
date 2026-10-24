"""YT phrase cues (punctuation-less) -> readable sentence-ish lines by pause/length."""
import json, sys, os
n = f"{int(sys.argv[1]):02d}"
src = f"/home/box/Downloads/yt/analayo-nibbana/yt-subs/lecture-{n}.json"
out = f"/tmp/opencode/lec{n}_yt.txt"
d = json.load(open(src))
cues = d["cues"]
lines, cur, cur_t, cur_e, words = [], [], None, None, 0
def flush():
    global cur, cur_t, words
    if cur:
        lines.append(f"{cur_t:7.1f}-{cur_e:7.1f} {''.join(cur).strip()}")
    cur, cur_t, words = [], None, 0
for i, c in enumerate(cues):
    x = c["x"]
    if cur_t is None: cur_t = c["t"]
    # space-join: add a space unless x brings its own or cur empty
    if cur and not x.startswith(" ") and not "".join(cur).endswith((" ", "\n")):
        cur.append(" ")
    cur.append(x)
    cur_e = c["e"]
    words += 1
    nxt_gap = (cues[i + 1]["t"] - c["e"]) if i + 1 < len(cues) else 99
    if nxt_gap > 0.7 or words >= 16:
        flush()
flush()
open(out, "w").write("\n".join(lines) + "\n")
print(f"lec{n}: {len(lines)} lines {os.path.getsize(out)}B first={lines[0][:50]!r}" if lines else f"lec{n}: EMPTY")
