#!/usr/bin/env python3
"""Session 43 — summarise a _s43_widgetloss[_TAG].json: per widget type, built bundles / bundles with a LOST run / pages / modules /
lost runs; then the examples for one type. Usage: python3 _s43_wl_report.py <json> [TYPE [N]]"""
import json, sys, collections
recs = json.load(open(sys.argv[1]))
by = collections.defaultdict(lambda: [0, 0, set(), set(), 0])
for r in recs:
    b = by[r["type"]]; b[0] += 1
    if r["lost"]:
        b[1] += 1; b[2].add((r["code"], r["page"])); b[3].add(r["code"]); b[4] += r["lost"]
print(f"{'type':18} {'built':>6} {'lossy':>6} {'pages':>6} {'mods':>5} {'runs':>6}")
for t, b in sorted(by.items(), key=lambda kv: -kv[1][1]):
    print(f"{t:18} {b[0]:6} {b[1]:6} {len(b[2]):6} {len(b[3]):5} {b[4]:6}")
print("TOTAL", len(recs), sum(1 for r in recs if r["lost"]))
if len(sys.argv) > 2:
    t = sys.argv[2]; n = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    for r in [r for r in recs if r["type"] == t and r["lost"]][:n]:
        print(f"  {r['code']} p{r['page']} #{r['index']} runs {r['runs']} lost {r['lost']}: " + " || ".join(r["lostText"])[:300])
