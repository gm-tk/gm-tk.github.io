#!/usr/bin/env python3
"""_s51_csdiff.py — per-page compare_structure movers between the fast-loop baseline and the last scoped run
(outputs/_fastloop_baseline/structural_comparison.json vs outputs/_fastloop_current/cs_scoped.json). WSL, any cwd."""
import json, os, collections
O = os.path.dirname(os.path.abspath(__file__))
base = json.load(open(os.path.join(O, "_fastloop_baseline", "structural_comparison.json")))
cur = json.load(open(os.path.join(O, "..", "reference", "tests", "structural_comparison.json")))
rows = lambda d: d if isinstance(d, list) else (d.get("pages") or d.get("per_page") or d.get("rows") or d)
def index(d):
    r = rows(d)
    if isinstance(r, dict): r = [dict(v, page=k) for k, v in r.items()]
    out = {}
    for x in r:
        if not isinstance(x, dict): continue
        k = x.get("page") or x.get("claude") or x.get("file") or (x.get("module"), x.get("name"))
        out[str(k)] = x
    return out
b, c = index(base), index(cur)
keys = [k for k in c if k in b]
if not keys:
    print("no common keys; base sample", list(b)[:3], "cur sample", list(c)[:3]); raise SystemExit
fields = [f for f in ("exact_chain", "matched", "claude_extra_container", "claude_missing_container") if f in c[keys[0]]]
mv = []
for k in keys:
    d = {f: (c[k].get(f, 0) or 0) - (b[k].get(f, 0) or 0) for f in fields}
    if any(d.values()): mv.append((d.get("exact_chain", 0), k, d))
mv.sort()
for e, k, d in mv: print(f"{k:45s} {d}")
print("sum", {f: sum(x[2][f] for x in mv) for f in fields})
