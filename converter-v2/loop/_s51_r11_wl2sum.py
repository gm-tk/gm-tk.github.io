#!/usr/bin/env python3
"""_s51_r11_wl2sum.py — summarise _s43_widgetloss2_<TAG>.json (one record per BUILT bundle: runs, lost, lostReal, lostMedia, real =
the lost learner-text parts): per widget type the bundles, the lossy ones, lost real parts; then the lost real parts' first words.
WSL, any cwd: python3 _s51_r11_wl2sum.py TAG"""
import json, os, sys, collections, re
O = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(O, f"_s43_widgetloss2_{sys.argv[1]}.json")))
by = collections.defaultdict(collections.Counter); shapes = collections.Counter(); ex = collections.defaultdict(list); mods = collections.defaultdict(set)
for r in d:
    t = r["type"]; real = r.get("real") or []
    by[t]["bundles"] += 1; by[t]["lostReal"] += len(real); by[t]["lostMedia"] += r.get("lostMedia", 0) or 0
    if real: by[t]["lossy"] += 1
    for p in real:
        txt = p if isinstance(p, str) else (p.get("text") or json.dumps(p))
        sh = f"{t:14s} | {re.sub(r'[0-9]+', 'N', ' '.join(str(txt).lower().split()[:2]))}"
        shapes[sh] += 1; mods[sh].add(r["code"])
        if len(ex[sh]) < 2: ex[sh].append(f"{r['code']} {r['page']}: {str(txt)[:60]}")
for t, c in sorted(by.items(), key=lambda kv: -kv[1]["lostReal"]): print(f"{t:18s} {dict(c)}")
print("top lost learner-text first words:")
for s, n in shapes.most_common(22): print(f"  {n:4d} {len(mods[s]):3d}m {s:50s} e.g. {ex[s][0]}")
