"""Session 50 — skeleton of a Claude page OFF (a saved probe dir) vs ON (disk), each against the gold. Tests dir, WSL:
python3 ../../outputs/_s50_skoffon.py CODE PAGE OFFDIR [context]"""
import os, sys, difflib
sys.path.insert(0, os.getcwd())
import _discrepancy_audit as DA, _skeleton_compare as K
code, page, offdir = sys.argv[1:4]; n = int(sys.argv[4]) if len(sys.argv) > 4 else 0
for _, cp, hp in DA.pairs(code):
    if os.path.basename(cp) != page: continue
    g = K._skel(hp, True); on = K._skel(cp, True); off = K._skel(os.path.join(offdir, code, page), True)
    r = lambda a, b: 100 * difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()
    print(f"gold {len(g)} lines; OFF {len(off)} lines {r(g, off):.1f}% ; ON {len(on)} lines {r(g, on):.1f}%")
    for l in difflib.unified_diff(off, on, "OFF", "ON", lineterm="", n=n): print(l)
