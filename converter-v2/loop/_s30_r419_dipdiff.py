#!/usr/bin/env python3
"""session 30 round 1 (r419) — inspect the probe's DOWN pages: skeleton line counts, difflib match counts, and the
disk → ON skeleton diff (what the round added) for the named pages. Usage: python3 _s30_r419_dipdiff.py CODE/PAGE ..."""
import sys, os, difflib
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "CONVERTER_V2", "reference", "tests"))
import _corpus
from _skeleton_compare import _skel
from _discrepancy_audit import HUMAN
from anchor_compare import CLAUDE
for arg in sys.argv[1:]:
    code, pg = arg.split("/")
    g = os.path.join(_corpus.mdir(HUMAN, code), pg + ".html")
    c = os.path.join(_corpus.mdir(CLAUDE, code), pg + ".html")
    o = os.path.join(HERE, "_s30_r419_on", code, pg + ".html")
    G = _skel(g, True); C = _skel(c, True); O = _skel(o, True)
    jg = sum(1 for l in G if "-text" in l); jo = sum(1 for l in O if "-text" in l)
    print(f"=== {arg}: gold {len(G)} disk {len(C)} on {len(O)}; lang lines gold {jg} on {jo}")
    sm = difflib.SequenceMatcher(None, G, C, autojunk=False); sm2 = difflib.SequenceMatcher(None, G, O, autojunk=False)
    print("matched lines disk", sum(b.size for b in sm.get_matching_blocks()), "on", sum(b.size for b in sm2.get_matching_blocks()),
          f"ratio {sm.ratio()*100:.1f} -> {sm2.ratio()*100:.1f}")
    print("--- disk vs on ---")
    for l in list(difflib.unified_diff(C, O, "disk", "on", n=1, lineterm=""))[:80]: print(l)
