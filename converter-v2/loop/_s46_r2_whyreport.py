#!/usr/bin/env python3
"""Session 46 Round 2 — report _s46_r2_why.json: per declined accordion bundle, the LAST member-walk guard it hit (if any), grouped by
the guard kind and the tag. WSL, from outputs/: python3 _s46_r2_whyreport.py [--show KIND]"""
import json, sys, collections, os
R = json.load(open("_s46_r2_why.json"))
excl = set()
ce = "../reference/tests/compare_exclusions.txt"
if os.path.exists(ce):
    for l in open(ce):
        l = l.strip()
        if l and not l.startswith("#"): excl.add(l.split()[0])
R = [r for r in R if r["code"] not in excl]
show = sys.argv[sys.argv.index("--show") + 1] if "--show" in sys.argv else None
by = collections.defaultdict(list)
for r in R:
    h = [v for ln, v in r["hits"]]
    key = "(no member-walk guard)" if not h else " ".join(h[-1].split(" | ")[0].split()[:2])
    by[key].append((r, h[-1] if h else ""))
print(f"{len(R)} declined (scored), {len(set(r['code'] for r in R))} modules")
for k, v in sorted(by.items(), key=lambda x: -len(x[1])):
    mods = collections.Counter(r["code"] for r, _ in v)
    print(f"  {len(v):4d} bundles {len(mods):3d} mod  {k}")
    if show and show in k:
        for r, h in v[:60]: print(f"        {r['code']} {r['page']} #{r['index']}: {h[:200]}")
