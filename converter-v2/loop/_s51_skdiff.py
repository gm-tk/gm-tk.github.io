#!/usr/bin/env python3
"""_s51_skdiff.py — print the SCAFFOLD skeleton diff of one Claude page against its gold pair (the gate's own pairing).
WSL, from reference/tests/:  python3 ../../outputs/_s51_skdiff.py ENGI201_2_0.html [--raw]"""
import os, sys, difflib, re
sys.path.insert(0, os.getcwd())
from _discrepancy_audit import pairs
import _skeleton_compare as K

name = sys.argv[1]; code = re.split(r"[_.]", name)[0]
for n, cp, hp in pairs(code):
    if os.path.basename(cp) == name:
        a = K._skel(hp, "--raw" not in sys.argv); b = K._skel(cp, "--raw" not in sys.argv)
        print(f"# gold {os.path.basename(hp)} ({len(a)} lines) vs claude {name} ({len(b)} lines)")
        for l in difflib.unified_diff(a, b, "gold", "claude", n=1, lineterm=""):
            print(l)
        break
else:
    print("no pair for", name)
