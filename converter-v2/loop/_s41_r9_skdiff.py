#!/usr/bin/env python3
"""Session 41 Round 9 PICK — the SCAFFOLD skeleton diff (gold -> Claude) for one module's pages. Usage (tests dir, WSL):
python3 ../../outputs/_s41_r9_skdiff.py CODE [PAGE-substring] [context]"""
import os, sys, difflib
sys.path.insert(0, os.getcwd())
import _discrepancy_audit as DA, _skeleton_compare as K
code = sys.argv[1]; want = sys.argv[2] if len(sys.argv) > 2 else ""; n = int(sys.argv[3]) if len(sys.argv) > 3 else 1
for _, cp, hp in DA.pairs(code):
    if want and want not in os.path.basename(cp): continue
    g = K._skel(hp, True); c = K._skel(cp, True)
    r = difflib.SequenceMatcher(None, g, c, autojunk=False).ratio()
    print(f"#### {os.path.basename(cp)} <- {os.path.basename(hp)}  {100*r:.1f}%  gold {len(g)} / claude {len(c)} lines")
    for l in difflib.unified_diff(g, c, "gold", "claude", lineterm="", n=n): print(l)
