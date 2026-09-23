#!/usr/bin/env python3
"""ROUND 453 — SPLIT THE DECOMPOSITION BY POPULATION (LOOP §1e). The scoped-ship gate flagged compare_structure missing
+44 and body_compare ANY +6 while 10 new pairs entered. Per page of the affected modules: baseline (the r452 fast-loop
snapshot) vs the scoped re-score scoped_ship.sh just wrote (reference/tests/structural_comparison.json + body_compare.json),
each page tagged EXISTING (in the baseline) or NEW. Run under WSL from CONVERTER_V2/reference/tests."""
import os, sys, json, collections
sys.path.insert(0, os.getcwd())
from _fastloop_diff import _bc_broken
O = os.path.join("..", "..", "outputs")
B = os.path.join(O, "_fastloop_baseline")
codes = set(c.strip() for c in open(os.path.join(O, "_r456_changed22.txt")) if c.strip())
bcs = json.load(open(os.path.join(B, "structural_comparison.json")))
ncs = json.load(open("structural_comparison.json"))
bbc = json.load(open(os.path.join(B, "body_compare.json")))
nbc = json.load(open("body_compare.json"))
def key(r):
    if "page" not in r and "module" in r: return r["module"]
    return r.get("page") or r.get("claude") or r.get("file") or r.get("claude_page") or json.dumps({k: r[k] for k in list(r)[:2]})
print("cs row keys:", list(ncs[0].keys())[:14])
print("bc row keys:", list(nbc[0].keys())[:14] if isinstance(nbc, list) else type(nbc))
def mod(r):
    return r.get("module") or r.get("code") or str(key(r)).split("_")[0].split("/")[-1]
bcs_m = {key(r): r for r in bcs if mod(r) in codes}
ncs_m = {key(r): r for r in ncs if mod(r) in codes}
tot = collections.Counter()
print(f"\n{'page':34s} {'':8s} matched exact extra missing")
for k in sorted(set(bcs_m) | set(ncs_m)):
    o, n = bcs_m.get(k), ncs_m.get(k)
    tag = "NEW" if o is None else ("GONE" if n is None else "EXIST")
    f = lambda r, a: (r or {}).get(a, 0)
    d = {a: f(n, a) - f(o, a) for a in ("matched", "exact_chain", "claude_extra_container", "claude_missing_container")}
    for a, v in d.items(): tot[(tag, a)] += v
    if any(d.values()):
        print(f"{str(k)[:34]:34s} {tag:8s} {d['matched']:+5d} {d['exact_chain']:+5d} {d['claude_extra_container']:+5d} {d['claude_missing_container']:+5d}")
for tag in ("EXIST", "NEW", "GONE"):
    print(f"TOTAL {tag}: matched {tot[(tag,'matched')]:+d} exact {tot[(tag,'exact_chain')]:+d} extra {tot[(tag,'claude_extra_container')]:+d} missing {tot[(tag,'claude_missing_container')]:+d}")
bb = {key(r): r for r in bbc if mod(r) in codes}
nb = {key(r): r for r in nbc if mod(r) in codes}
print("\nbody_compare broken pages:")
for k in sorted(set(bb) | set(nb)):
    o, n = bb.get(k), nb.get(k)
    ob, nb_ = (o is not None and _bc_broken(o)), (n is not None and _bc_broken(n))
    if ob != nb_ or (n is not None and o is None and nb_):
        tag = "NEW" if o is None else "EXIST"
        r = n or o
        print(f"  {str(k)[:40]:40s} {tag:6s} {int(ob)} -> {int(nb_)}  over={r.get('over_capture')} widget={r.get('biggest_widget_chars')} lost={r.get('lost_blocks')} multi={r.get('multi_type')} empty={r.get('empty_widgets')}")
# ROUND 456 addition — the structural-defect audit: unclean / leaking pages, baseline vs the scoped re-score
bdf = json.load(open(os.path.join(B, "defect.json")))
ndf = json.load(open(os.path.join("..", "..", "outputs", "_fastloop_current", "defect_scoped.json")))
def dpages(dj):
    out = {}
    rows = dj.get("pages") if isinstance(dj, dict) else dj
    for r in rows or []:
        p = r.get("page") or r.get("file")
        if p and p.split("/")[0].split("_")[0] in codes: out[p] = r
    return out
bo, no = dpages(bdf), dpages(ndf)
print("\ndefect pages (unclean or leaking) changed:")
for p in sorted(set(bo) | set(no)):
    o, n = bo.get(p), no.get(p)
    f = lambda r: (r or {}).get("defects") or (r or {}).get("counts") or r
    if json.dumps(f(o), sort_keys=True) != json.dumps(f(n), sort_keys=True):
        print("  ", p, "OLD", json.dumps(f(o))[:120], "NEW", json.dumps(f(n))[:120])
