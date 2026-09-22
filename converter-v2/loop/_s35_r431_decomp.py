#!/usr/bin/env python3
"""r431 — per-module decomposition of the scoped-ship delta (compare_structure matched / exact / EXTRA / missing and the skeleton
per page) for the affected set: the fast-loop baseline (outputs/_fastloop_baseline, the r429 state) vs the scoped re-score just run
(reference/tests/structural_comparison.json + outputs/_fastloop_current/skeleton_scoped.json). Names the page behind every moved number.
Run under WSL from reference/tests: python3 ../../outputs/_s34_r428_decomp.py
"""
import json, os, sys
T = os.path.dirname(os.path.abspath(__file__)) + "/../reference/tests"
O = os.path.dirname(os.path.abspath(__file__))
aff = [l.strip() for l in open(O + "/_affected_r431.txt", encoding="utf-8") if l.strip()]
def load(p): return json.load(open(p, encoding="utf-8"))
base_cs = load(O + "/_fastloop_baseline/structural_comparison.json")
new_cs = load(T + "/structural_comparison.json")
def rows(j):
    r = j["modules"] if isinstance(j, dict) and "modules" in j else (j if isinstance(j, list) else j.get("rows", []))
    out = {}
    for x in r:
        code = x.get("module") or x.get("code")
        if code: out[code] = x
    return out
b, n = rows(base_cs), rows(new_cs)
print("compare_structure per module (matched / exact / EXTRA / missing): baseline -> new")
tot = [0, 0, 0, 0]
for c in aff:
    x, y = b.get(c), n.get(c)
    if not x or not y: print(f"  {c}: missing row ({'base' if not x else 'new'})"); continue
    k = ("matched", "exact_chain", "claude_extra_container", "claude_missing_container")
    d = [y.get(kk, 0) - x.get(kk, 0) for kk in k]
    for i in range(4): tot[i] += d[i]
    flag = "  <-- missing +%d" % d[3] if d[3] > 0 else ""
    print(f"  {c:8s} {x.get(k[0],0):4d}/{x.get(k[1],0):4d}/{x.get(k[2],0):3d}/{x.get(k[3],0):3d} -> {y.get(k[0],0):4d}/{y.get(k[1],0):4d}/{y.get(k[2],0):3d}/{y.get(k[3],0):3d}   delta {d[0]:+d}/{d[1]:+d}/{d[2]:+d}/{d[3]:+d}{flag}")
print("  TOTAL delta matched/exact/EXTRA/missing:", "/".join("%+d" % v for v in tot))
# skeleton per page
bsk = load(O + "/_fastloop_baseline/skeleton.json"); nsk = load(O + "/_fastloop_current/skeleton_scoped.json")
def pages(j):
    pp = j["per_page"] if isinstance(j, dict) and "per_page" in j else j
    return {(p.get("module") or p.get("code"), p.get("claude") or p.get("claude_page") or p.get("page")): p for p in pp}
bp, np_ = pages(bsk), pages(nsk)
print("\nskeleton per page (scaffold): baseline -> new, the affected modules")
up = down = 0; ssum = 0.0
for (code, page), p in sorted(np_.items(), key=lambda kv: str(kv[0])):
    if code not in aff: continue
    q = bp.get((code, page))
    if q is None:
        print(f"  {code:8s} {str(page):24s} NEW PAIR  -> {p['scaffold']*100:5.1f}"); continue
    d = (p["scaffold"] - q["scaffold"]) * 100
    ssum += d
    if abs(d) >= 0.05: up += d > 0; down += d < 0
    print(f"  {code:8s} {str(page):24s} {q['scaffold']*100:5.1f} -> {p['scaffold']*100:5.1f}  {d:+5.1f}")
for (code, page), q in sorted(bp.items(), key=lambda kv: str(kv[0])):
    if code in aff and (code, page) not in np_: print(f"  {code:8s} {str(page):24s} GONE PAIR  {q['scaffold']*100:5.1f} ->")
print(f"  up {up} / down {down}, pp-sum {ssum:+.1f}")
