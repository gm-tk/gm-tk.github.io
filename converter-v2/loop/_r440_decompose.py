#!/usr/bin/env python3
"""ROUND 440 (session 39 Round 2 — D13-6) — decompose every metric the scoped ship calls REGRESSED, module by module.
The movement is a POPULATION change: the 537 unaffected modules are byte-identical and their pairing is unchanged
(compare_gold_pages.txt has rules for the five only), so every delta lives inside MXFUN01 / BLL240 / CEDT207 /
CEDT301 / CEDK501. OLD = the fast-loop baseline (the r439 shipped state); NEW = the scoped re-score scoped_ship.sh
just wrote (reference/tests/structural_comparison.json is the full list with the affected rows patched in;
_fastloop_current/skeleton_scoped.json and defect_scoped.json hold the affected set).
Run from CONVERTER_V2/reference/tests under WSL: python3 ../../outputs/_r440_decompose.py
"""
import json, os
O = os.path.join("..", "..", "outputs")
FIVE = ["MXFUN01", "BLL240", "CEDT207", "CEDT301", "CEDK501"]
L = lambda p: json.load(open(p))

osk = [p for p in L(os.path.join(O, "_fastloop_baseline", "skeleton.json"))["per_page"] if p["module"] in FIVE]
nsk = [p for p in L(os.path.join(O, "_fastloop_current", "skeleton_scoped.json"))["per_page"] if p["module"] in FIVE]
ocs = {r["module"]: r for r in L(os.path.join(O, "_fastloop_baseline", "structural_comparison.json")) if r["module"] in FIVE}
ncs = {r["module"]: r for r in L("structural_comparison.json") if r["module"] in FIVE}
odf = L(os.path.join(O, "_fastloop_baseline", "defect.json"))
ndf = L(os.path.join(O, "_fastloop_current", "defect_scoped.json"))

print(f"{'module':8s} | {'sk pairs':>9s} | {'sk mean':>13s} | {'>=50':>7s} | {'>=75':>7s} | {'cs exact':>9s} | {'EXTRA':>7s} | {'missing':>7s} | {'df clean/total':>15s}")
T = dict(sk_o=0, sk_n=0, b50_o=0, b50_n=0, b75_o=0, b75_n=0, ex_o=0, ex_n=0, xt_o=0, xt_n=0, mi_o=0, mi_n=0)
for m in FIVE:
    o = [p["scaffold"] for p in osk if p["module"] == m]; n = [p["scaffold"] for p in nsk if p["module"] == m]
    b50o, b50n = sum(x >= 0.5 for x in o), sum(x >= 0.5 for x in n)
    b75o, b75n = sum(x >= 0.75 for x in o), sum(x >= 0.75 for x in n)
    co, cn = ocs.get(m, {}), ncs.get(m, {})
    g = lambda d, k: d.get(k, 0) or 0
    mo = f"{100*sum(o)/len(o):5.1f}" if o else "  -  "; mn = f"{100*sum(n)/len(n):5.1f}" if n else "  -  "
    dfo = f"{odf['per_module_clean'].get(m, 0)}/{odf['per_module_pages'].get(m, 0)}"
    dfn = f"{ndf['per_module_clean'].get(m, 0)}/{ndf['per_module_pages'].get(m, 0)}"
    print(f"{m:8s} | {len(o):3d} -> {len(n):3d} | {mo} -> {mn} | {b50o:2d} -> {b50n:2d} | {b75o:2d} -> {b75n:2d} | "
          f"{g(co,'exact_chain'):3d} -> {g(cn,'exact_chain'):3d} | {g(co,'claude_extra_container'):2d} -> {g(cn,'claude_extra_container'):2d} | "
          f"{g(co,'claude_missing_container'):2d} -> {g(cn,'claude_missing_container'):2d} | {dfo:>6s} -> {dfn:<6s}")
    for k, a, b in (("sk", len(o), len(n)), ("b50", b50o, b50n), ("b75", b75o, b75n), ("ex", g(co, 'exact_chain'), g(cn, 'exact_chain')),
                    ("xt", g(co, 'claude_extra_container'), g(cn, 'claude_extra_container')), ("mi", g(co, 'claude_missing_container'), g(cn, 'claude_missing_container'))):
        T[k + "_o"] += a; T[k + "_n"] += b
    print(f"         pages OLD: " + ", ".join(f"{p['page']} {100*p['scaffold']:.1f}" for p in osk if p['module'] == m))
    print(f"         pages NEW: " + ", ".join(f"{p['page']} {100*p['scaffold']:.1f}" for p in nsk if p['module'] == m))
print("TOTAL    | " + " | ".join(f"{k}: {T[k+'_o']} -> {T[k+'_n']} ({T[k+'_n']-T[k+'_o']:+d})" for k in ("sk", "b50", "b75", "ex", "xt", "mi")))
print(f"defect corpus: clean {odf['clean_pages']}/{odf['total_pages']} = {100*odf['clean_pages']/odf['total_pages']:.3f} %  (the new corpus figure is in the scoped-ship log)")
