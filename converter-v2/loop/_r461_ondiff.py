#!/usr/bin/env python3
"""ROUND 461 — SCAFFOLD diff gold -> ON page (outputs/_r461_on) for one module page. Usage (tests dir, WSL): CODE PAGE-substring [ctx]"""
import os, sys, difflib
sys.path.insert(0, os.getcwd())
import _discrepancy_audit as DA, _skeleton_compare as K
code, want = sys.argv[1], sys.argv[2]; n = int(sys.argv[3]) if len(sys.argv) > 3 else 1
for _, cp, hp in DA.pairs(code):
    if want not in os.path.basename(cp): continue
    on = os.path.join("../../outputs/_r461_on", code, os.path.basename(cp))
    g = K._skel(hp, True); c = K._skel(cp, True); o = K._skel(on, True)
    print(f"#### {os.path.basename(cp)} <- {os.path.basename(hp)}")
    for l in difflib.unified_diff(c, o, "disk", "ON", lineterm="", n=n): print(l)
    print("---- gold audioImage context:")
    for i, l in enumerate(g):
        if "audioImage" in l and "Option" not in l: print("   ", " | ".join(x.strip() for x in g[max(0, i-3):i+3]))
