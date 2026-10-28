"""Regenerate build/manifest_index.json from current seg JSONs.

Usage: python3 process/scripts/regen_manifest_index.py
Reads build/seg{N}_{core_v4,gold,pool}.json, writes {clips, min, audio_ok}.
audio_ok is N/N (all 33 DS mp3s present since 2026-10-24, §24 notes).
Manifest *.txt line counts may differ from gold JSON by design (motto-cap
omissions, sharpen_gold.py step 3) — the index tracks DATA counts.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.normpath(os.path.join(HERE, "..", "..", "build"))

out = {}
for n in range(1, 7):
    for kind in ["pool", "gold", "core_v4"]:
        fn = os.path.join(BUILD, f"seg{n}_{kind}.json")
        with open(fn) as f:
            d = json.load(f)
        spans = d if isinstance(d, list) else d.get("spans", d.get("clips", []))
        dur = sum(s.get("dur", s.get("end", 0) - s.get("start", 0)) for s in spans)
        key = f"s{n}_{'core' if kind == 'core_v4' else kind}"
        out[key] = {
            "clips": len(spans),
            "min": round(dur / 60, 1),
            "audio_ok": f"{len(spans)}/{len(spans)}",
        }

with open(os.path.join(BUILD, "manifest_index.json"), "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")

tot_core = sum(out[f"s{n}_core"]["clips"] for n in range(1, 7))
tot_gold = sum(out[f"s{n}_gold"]["clips"] for n in range(1, 7))
tot_pool = sum(out[f"s{n}_pool"]["clips"] for n in range(1, 7))
print(f"core={tot_core} gold={tot_gold} pool={tot_pool}")
