#!/usr/bin/env python3
"""_r340_dips.py — ROUND 340: for each skeleton mover, show the paired gold page and the scaffold-skeleton diff
around the video embed (OFF page = outputs/_r340_off/<code>/<page> vs the regenerated disk page vs the gold)."""
import os, sys, difflib
HERE = os.path.dirname(os.path.abspath(__file__)); T = os.path.join(HERE, "..", "reference", "tests"); sys.path.insert(0, T)
import _corpus
from _discrepancy_audit import pairs
import _skeleton_compare as K
OUT = os.path.join(T, "..", "..", "..", "01-Claude_Modules_"); OFF = os.path.join(HERE, "_r340_off")
want = sys.argv[1:] or ["ANZH303_6_0.html", "ENFUN01_0_0.html", "HIS1008_5_0.html", "HIS1008_1_0.html", "HIS1008_7_0.html"]
for w in want:
    code = w.split("_")[0]
    for n, cp, hp in pairs(code):
        if os.path.basename(cp) != w: continue
        offp = os.path.join(OFF, code, w)
        r_on, a_on, b = K.match(cp, hp, scaffold=True); r_off, a_off, _ = K.match(offp, hp, scaffold=True)
        print(f"\n===== {w}  gold={os.path.basename(hp)}  scaffold OFF {r_off*100:.2f} -> ON {r_on*100:.2f}  ({(r_on-r_off)*100:+.2f})  lines gold {len(b)} claudeOFF {len(a_off)} claudeON {len(a_on)}")
        print("--- skeleton OFF -> ON (claude):")
        for l in difflib.unified_diff(a_off, a_on, lineterm="", n=2): 
            if not l.startswith(("---", "+++")): print("   " + l[:150])
        print("--- gold lines mentioning video/iframe/externalButton/embed (with 1 line of context):")
        for i, l in enumerate(b):
            if any(k in l for k in ("videoSection", "iframe", "externalButton", "embed")):
                print(f"   {i:4d} {l[:150]}")
        print("--- claude ON lines mentioning the same:")
        for i, l in enumerate(a_on):
            if any(k in l for k in ("videoSection", "iframe", "externalButton", "embed")):
                print(f"   {i:4d} {l[:150]}")
