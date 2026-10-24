import json
DUR_DS, DUR_YT = 5292.76, 5280.7
FIRST_DS, FIRST_YT = 12.68, 6.6
KEEPS = [
 (12.68,39.18),(548.3,583.14),(695.52,749.1),(749.9,804.9),(1526.2,1542.8),
 (1548.3,1586.0),(1872.1,1968.0),(2031.2,2088.8),(2100.6,2144.2),(2220.8,2262.7),
 (2296.7,2368.2),(2434.3,2471.8),(2479.0,2517.0),(2535.5,2605.5),(2605.5,2643.1),
 (2649.6,2769.0),(2769.8,2819.6),(2865.4,2923.0),(2924.4,2957.4),(2998.9,3083.0),
 (3083.6,3111.6),(3147.8,3164.3),(3243.8,3345.2),(3345.2,3387.1),(3442.6,3471.8),
 (3645.9,3695.0),(3743.0,3760.4),(3760.4,3863.5),(4195.0,4229.6),(4230.4,4273.6),
 (4273.6,4320.1),(4523.9,4561.2),(4587.5,4614.1),(4691.2,4723.6),(4832.8,4968.0),
 (5012.7,5058.6),(5069.2,5126.2),(5199.0,5220.6),(5242.7,5268.7),
]
MAJOR = [
 (40.4,64.2,"logistics","forum mechanics + first-lecture announcements"),
 (64.2,548.3,"logistics","everything before the sermon: origin stories, biography, course purpose/format, translation preferences — welcome line kept"),
 (583.14,695.52,"repetition","second motto chant + invitation narrative (first telling kept)"),
 (804.9,1526.2,"tangent","six-qualities survey, commentaries-background essay, Manu/Sangiti history comment — the long detour"),
 (1542.8,1548.3,"filler","transition"),
 (1586.0,1872.1,"tangent","catechism rundown + Mahasi slow-walking essay"),
 (1968.0,2031.2,"tangent","Bodhi name-translation + Chinese parallel detour"),
 (2144.2,2202.5,"bio","personal 'this passage changed everything' story"),
 (2368.2,2434.3,"repetition","convention/nameless-tree tail + child rehash"),
 (2471.8,2479.0,"filler","transition"),
 (2517.0,2535.5,"filler","simile preamble (epithets restated in kept line)"),
 (2769.0,2769.8,"filler","transition"),
 (2819.6,2865.4,"repetition","first/second tangle-verse discussion (third verse kept)"),
 (2957.4,2998.9,"repetition","pattika/rupasanya pair restated (resistance core kept)"),
 (3083.0,3083.6,"filler","transition"),
 (3111.6,3147.8,"tangent","weaving-etymology mechanism detail"),
 (3164.3,3243.8,"tangent","Bodhi lamp-translation musing + torch simile list"),
 (3387.1,3442.6,"tangent","Western-winter climate aside + Mahagandhya lead-in"),
 (3471.8,3645.9,"tangent","Upanishad comparative essay + Upadana wordplay"),
 (3695.0,3743.0,"repetition","Vedic being/non-being history (solution kept)"),
 (3863.5,4195.0,"tangent","Bodhi-flame comment + commentators'-critique essay + immediacy comment"),
 (4229.6,4230.4,"filler","transition"),
 (4320.1,4523.9,"tangent","Udana genre essay (Bande, Chinese parallels)"),
 (4561.2,4587.5,"repetition","scholars'-hesitation restatement"),
 (4614.1,4691.2,"repetition","Bhikkhaghosa/imaginary-heretic debate setup (refutation kept)"),
 (4723.6,4832.8,"repetition","limbs simile tail + synonyms preamble"),
 (4968.0,5012.7,"tangent","Rananda heavenly-nymphs story"),
 (5058.6,5069.2,"filler","'some still go asking' pivot"),
 (5126.2,5199.0,"tangent","craving-inclination mechanism essay (bhavanetti, carrot-donkey)"),
 (5220.6,5242.7,"logistics","'hard to summarize' preamble"),
 (5268.7,DUR_DS,"logistics","forum plug, thanks, next-week logistics"),
]
def ds2yt(t): return round((t - FIRST_DS) * ((DUR_YT - FIRST_YT) / (DUR_DS - FIRST_DS)) + FIRST_YT, 2)
cuts, pos = [], 0.0
for a, b in sorted(KEEPS):
    if a - pos > 0.3: cuts.append((pos, a))
    pos = max(pos, b)
if DUR_DS - pos > 0.3: cuts.append((pos, DUR_DS))
def label(a, b):
    for m in MAJOR:
        if abs(m[0]-a) < 1.5 and abs(m[1]-b) < 1.5: return m[2], m[3]
    if b - a >= 5: return "silence", "long pause/chant gap inside removed span"
    return "trim", "short transition inside removed span"
kept = sum(b-a for a, b in KEEPS)
assert 1680 <= kept <= 1980, f"kept {kept} OUT OF BAND"
plan = {
 "lecture": 1, "target_min": 30, "source_min": round(DUR_DS/60,1), "kept_sec": round(kept,1), "v": 2,
 "timebase": {"yt_first": FIRST_YT, "yt_last": 5280.7, "ds_first": FIRST_DS, "ds_last": 5286.0,
              "note": "cuts in DS seconds; yt = linear map via anchors"},
 "cuts": [{"start": round(a,2), "end": round(b,2), "kind": label(a,b)[0], "reason": label(a,b)[1]} for a, b in cuts],
 "keep_summary": "welcome+theme; motto & unlock comment incl. sankara gloss; name/form core (Sopaka, rubber-ball, four elements, tangle); fire arc (lamp, epithets, accusers, cool-body, upadana, tetralemma/Upasiva); Nibbana=extinction (Ratanasutta, 11-fold fire, Radha chain, exam/certificate); sermon close + two-point recap."
}
json.dump(plan, open("/home/box/Downloads/yt/analayo-nibbana/lecture-01.cutplan.json","w"), indent=1)
md = [f"# Lecture 1 — 30-min cut plan (v2)\n", f"Source {plan['source_min']} min → **kept {kept/60:.1f} min ({kept/DUR_DS*100:.0f}%)** · {len(cuts)} cuts · band ✓\n"]
def mm(s): return f"{int(s//60)}:{int(s%60):02d}"
for c in plan["cuts"]:
    md.append(f"- {mm(c['start'])}–{mm(c['end'])}  [{c['kind']}]  {c['reason']}")
md.append(f"\n**Episode keeps:** {plan['keep_summary']}")
open("/home/box/Downloads/yt/analayo-nibbana/lecture-01.cutplan.md","w").write("\n".join(md)+"\n")
print(f"v2 OK kept={kept:.0f}s = {kept/60:.1f}min, {len(cuts)} cuts ✓")
