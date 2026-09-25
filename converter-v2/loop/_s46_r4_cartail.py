#!/usr/bin/env python3
"""Session 46 Round 4 — for each carousel (or CT_TYPE) bundle with a table then a [body] (_s46_r4_cartail.json / _s46_r4_tail_<T>.json),
where does the GOLD put the first post-table [body] text: inside a carousel (a caption / slide), inside another widget, or FREE?
WSL, from outputs/: python3 _s46_r4_cartail.py [json]"""
import json, sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _s46_goldloc import locate
src = sys.argv[1] if len(sys.argv) > 1 else "_s46_r4_cartail.json"
R = json.load(open(src))
excl = set(l.split()[0] for l in open("../reference/tests/compare_exclusions.txt") if l.strip() and not l.startswith("#"))
R = [r for r in R if r["code"] not in excl]
own = collections.Counter(); fate = collections.Counter(); byfam = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list)
for r in R:
    t = r["bodies"][0][:60] if r["bodies"] else ""
    if len(t) < 12: fate["(short)"] += 1; continue
    hits = locate(r["code"], t)
    if not hits: k = "absent"
    else:
        ch = hits[0][1]
        k = "carousel" if "carousel" in ch else ("other-widget" if any(w in ch for w in ("accordion", "flipCard", "tabs", "clickDrop", "modal", "activity")) else "free")
    fate[k] += 1; byfam[r["code"][:3]][k] += 1; own[(r.get("owned"), k)] += 1
    if len(ex[k]) < 6: ex[k].append(f"{r['code']} {r['page']} built={r['built']} before={r['before'][:3]} | {t[:50]!r} → {hits[0][1][-70:] if hits else '-'}")
print(f"{len(R)} carousel bundles with a table then a [body] ({len(set(r['code'] for r in R))} modules); gold fate of the first post-table [body]:", dict(fate))
for k, v in ex.items():
    print(f"  {k}:")
    for e in v: print("     ", e)
print("by prefix:", {f: dict(c) for f, c in sorted(byfam.items(), key=lambda x: -sum(x[1].values()))[:14]})
print("by activity-owned:", dict(own))
