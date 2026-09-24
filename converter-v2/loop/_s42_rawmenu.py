#!/usr/bin/env python3
"""SESSION 42 (parametrised: python3 ../../outputs/_s42_rawmenu.py <TAG>; the r460 tool) — the MENU-ONLY evidence. The skeleton SCAFFOLD collapses the module menu's `tabs` to one WIDGET marker, so the
K / P tab promotion is invisible to it BY DESIGN; this scores what it does change: (a) the RAW skeleton (no widget collapse) of
every changed page, disk (the r459 state) vs ON (outputs/_r460_on), against the paired gold page; (b) the MENU-ONLY skeleton —
the #module-menu-content subtree's lines alone — gold vs disk vs ON. Run under WSL from CONVERTER_V2/reference/tests."""
import os, sys, difflib
sys.path.insert(0, os.getcwd())
import _discrepancy_audit as DA
import _corpus
import _skeleton_compare as K
from anchor_compare import CLAUDE
O = os.path.join("..", "..", "outputs"); TAG = sys.argv[1]
pages = [p.strip() for p in open(os.path.join(O, "_" + TAG + "_ON_pages.txt")) if p.strip()]
codes = sorted(set(p.split("/")[0] for p in pages))
def menu_only(sk):
    out = []; inside = None
    for ln in sk:
        ind = len(ln) - len(ln.lstrip())
        if inside is not None and ind <= inside: inside = None
        if "div#module-menu-content" in ln: inside = ind; out.append(ln.strip()); continue
        if inside is not None: out.append(ln[inside:])
    return out
def ratio(a, b): return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()
tot = {"raw": [0, 0], "menu": [0, 0]}; ups = downs = 0
for code in codes:
    for n, cp, hp in DA.pairs(code):
        nm = os.path.basename(cp)
        if f"{code}/{nm}" not in pages: continue
        on = os.path.join(O, "_" + TAG + "_on", code, nm)
        g, d, o = K._skel(hp, False), K._skel(cp, False), K._skel(on, False)
        rd, ro = ratio(d, g), ratio(o, g)
        md, mo = ratio(menu_only(d), menu_only(g)), ratio(menu_only(o), menu_only(g))
        tot["raw"][0] += rd; tot["raw"][1] += ro; tot["menu"][0] += md; tot["menu"][1] += mo
        ups += mo > md + 1e-9; downs += mo < md - 1e-9
        print(f"{code}/{nm:22s} raw {100*rd:5.1f} -> {100*ro:5.1f}   menu-only {100*md:5.1f} -> {100*mo:5.1f}  {'UP' if mo > md else ('DOWN' if mo < md else '')}")
print(f"\nmenu-only: {ups} up / {downs} down; raw pp-sum {100*(tot['raw'][1]-tot['raw'][0]):+.1f}; menu pp-sum {100*(tot['menu'][1]-tot['menu'][0]):+.1f}")
