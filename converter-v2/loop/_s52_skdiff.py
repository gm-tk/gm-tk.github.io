#!/usr/bin/env python3
"""_s52_skdiff.py — the skeleton gate's own scaffold lines for one paired page, gold vs Claude, as a unified diff (context 1).
WSL, from reference/tests/:  python3 ../../outputs/_s52_skdiff.py CODE PAGE.html [MAXLINES]"""
import os, sys, difflib
sys.path.insert(0, os.getcwd())
from _discrepancy_audit import pairs
import _skeleton_compare as K
code, page = sys.argv[1], sys.argv[2]; mx = int(sys.argv[3]) if len(sys.argv) > 3 else 140
for n, cp, hp in pairs(code):
    if os.path.basename(cp) != page: continue
    g = K._skel(hp, True); c = K._skel(cp, True)
    print(f"{page} ↔ {os.path.basename(hp)}: scaffold {K.match(cp, hp, True)[0] * 100:.1f} %  gold {len(g)} lines / claude {len(c)}")
    d = list(difflib.unified_diff(g, c, "gold", "claude", lineterm="", n=1))
    print("\n".join(d[:mx]))
