#!/usr/bin/env python3
"""Round 447 — the COMPANION numbers for the DOWN movers on an h4.goJournal gold (LOOP §3 step 6): for each page,
the SCAFFOLD ratio (the gate's match()), the POSITION-FREE overlap (the multiset intersection of the gold and Claude
scaffold lines, as a share of the gold's lines) and the uncollapsed matched-line count (sum of difflib's matching
blocks), disk (r446) vs ON. A dip whose position-free overlap RISES is the scorer's alignment artefact.
Run from CONVERTER_V2/reference/tests under WSL."""
import os, sys, glob, difflib, collections
sys.path.insert(0, os.getcwd())
from _skeleton_compare import _skel
O = os.path.join("..", "..", "outputs"); ROOT = os.path.normpath(os.path.join("..", "..", ".."))
PAGES = [("ENGI405", "ENGI405_5_0.html", "ENGI405_5.2.html"), ("ENGI401", "ENGI401_8_0.html", "ENGI401_5.3.html"),
         ("SSCI104", "SSCI104_3_0.html", "SSCI104-3.0.html"), ("MXFU202", "MXFU202_3_0.html", "MXFU202_3.0.html"),
         ("MXFU202", "MXFU202_2_0.html", "MXFU202_2.0.html"), ("MXEX401", "MXEX401_6_0.html", "MXEX401_06.0.html")]
def stats(c, g):
    a = _skel(c, True); b = _skel(g, True)
    sm = difflib.SequenceMatcher(None, b, a, autojunk=False)
    inter = sum((collections.Counter(a) & collections.Counter(b)).values())
    return sm.ratio(), inter / max(1, len(b)), sum(m.size for m in sm.get_matching_blocks())
for code, cf, gf in PAGES:
    disk = glob.glob(os.path.join(ROOT, "01-Claude_Modules_", "*", code, cf))[0]
    on = os.path.join(O, "_r447_on", code, cf)
    gold = glob.glob(os.path.join(ROOT, "01-Finalized_Modules_", "*", code, gf))[0]
    r0, o0, m0 = stats(disk, gold); r1, o1, m1 = stats(on, gold)
    print(f"{code} {cf}: scaffold {100*r0:.1f} -> {100*r1:.1f} ({100*(r1-r0):+.1f}); position-free overlap {100*o0:.1f} -> {100*o1:.1f} ({100*(o1-o0):+.1f}); matched lines {m0} -> {m1} ({m1-m0:+d})")
