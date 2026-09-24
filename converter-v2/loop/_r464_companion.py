#!/usr/bin/env python3
"""Round 461 — the COMPANION numbers (LOOP §3 step 6, the r447 form) for EVERY changed pair: SCAFFOLD ratio (the gate's
match()), the POSITION-FREE overlap (multiset intersection of gold and Claude scaffold lines, as a share of the gold's lines)
and the matched-line count (difflib's matching blocks), disk (r463) vs ON (outputs/_r464_on). Pairs = the gate's own pairing
(_discrepancy_audit.pairs) over the changed modules. A dip whose position-free overlap RISES is the scorer's alignment artefact.
Run from CONVERTER_V2/reference/tests under WSL."""
import os, sys, difflib, collections
sys.path.insert(0, os.getcwd())
import _discrepancy_audit as DA
from _skeleton_compare import _skel
O = os.path.join("..", "..", "outputs")
pages = set(p.strip() for p in open(os.path.join(O, "_r464_ON_pages.txt")) if p.strip())
codes = sorted(set(p.split("/")[0] for p in pages))
def stats(c, g):
    a = _skel(c, True); b = _skel(g, True)
    sm = difflib.SequenceMatcher(None, b, a, autojunk=False)
    inter = sum((collections.Counter(a) & collections.Counter(b)).values())
    return sm.ratio(), inter / max(1, len(b)), sum(m.size for m in sm.get_matching_blocks())
tot = collections.Counter(); art = []; real = []
for code in codes:
    for _, cp, hp in DA.pairs(code):
        nm = os.path.basename(cp)
        if f"{code}/{nm}" not in pages: continue
        on = os.path.join(O, "_r464_on", code, nm)
        r0, o0, m0 = stats(cp, hp); r1, o1, m1 = stats(on, hp)
        d = 100 * (r1 - r0)
        tag = "UP" if d > 0.05 else ("DOWN" if d < -0.05 else "=")
        if tag == "DOWN":
            (art if (o1 > o0 + 1e-9 or m1 > m0) else real).append(f"{code}/{nm}<-{os.path.basename(hp)} {d:+.1f} (overlap {100*o0:.1f}->{100*o1:.1f}, matched {m0}->{m1})")
        tot[tag] += 1; tot["pp"] += d
        print(f"{tag:4s} {code}/{nm:22s} <- {os.path.basename(hp):22s} scaffold {100*r0:5.1f} -> {100*r1:5.1f} ({d:+.1f}); overlap {100*o0:5.1f} -> {100*o1:5.1f}; matched {m0} -> {m1}")
print(f"\nUP {tot['UP']} / DOWN {tot['DOWN']} / = {tot['=']}; pp-sum {tot['pp']:+.1f}")
print(f"DOWN with a rising companion (artefact, nameable) {len(art)}:"); [print("  ", x) for x in art]
print(f"DOWN with NO rising companion (real) {len(real)}:"); [print("  ", x) for x in real]
