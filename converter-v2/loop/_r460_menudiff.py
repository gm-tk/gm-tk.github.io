#!/usr/bin/env python3
"""ROUND 460 — print the MENU-ONLY skeleton diff (gold -> ON) for one page. Usage (tests dir, WSL): python3 _r460_menudiff.py CODE PAGE"""
import os, sys, difflib
sys.path.insert(0, os.getcwd())
import _discrepancy_audit as DA, _skeleton_compare as K
def menu_only(sk):
    out = []; inside = None
    for ln in sk:
        ind = len(ln) - len(ln.lstrip())
        if inside is not None and ind <= inside: inside = None
        if "div#module-menu-content" in ln: inside = ind; out.append(ln.strip()); continue
        if inside is not None: out.append(ln[inside:])
    return out
code, nm = sys.argv[1], sys.argv[2]
for n, cp, hp in DA.pairs(code):
    if os.path.basename(cp) != nm: continue
    g = menu_only(K._skel(hp, False)); o = menu_only(K._skel(os.path.join("../../outputs/_r460_on", code, nm), False))
    for l in difflib.unified_diff(g, o, "gold", "ON", lineterm="", n=1): print(l)
