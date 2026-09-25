#!/usr/bin/env python3
"""_s51_sk3.py — one page's SCAFFOLD skeletons: the OFF (disk) → ON (a probe's saved page) diff, then the gold region around the
first changed line. WSL, from reference/tests/:  python3 ../../outputs/_s51_sk3.py PAGE.html SAVEDIR [CONTEXT]"""
import os, re, sys, difflib
sys.path.insert(0, os.getcwd())
from _discrepancy_audit import pairs
import _skeleton_compare as K

name, save = sys.argv[1], sys.argv[2]; ctx = int(sys.argv[3]) if len(sys.argv) > 3 else 25
code = re.split(r"[_.]", name)[0]
for n, cp, hp in pairs(code):
    if os.path.basename(cp) != name: continue
    g = K._skel(hp, True); a = K._skel(cp, True); b = K._skel(os.path.join(save, code, name), True)
    print(f"gold {os.path.basename(hp)} {len(g)} / off {len(a)} / on {len(b)}")
    for l in difflib.unified_diff(a, b, "off", "on", n=2, lineterm=""): print(l)
    print("=== gold vs ON")
    for l in difflib.unified_diff(g, b, "gold", "on", n=1, lineterm=""): print(l)
