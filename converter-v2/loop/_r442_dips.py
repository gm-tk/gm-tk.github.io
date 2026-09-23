#!/usr/bin/env python3
"""ROUND 442 — the MXFL202 dips: companion numbers (LOOP §3 step 6). For each dipping pair: SCAFFOLD (the gate),
the POSITION-FREE overlap of the scaffold skeletons (multiset intersection / gold length — how many of the gold's
structural lines Claude now has, anywhere), the matched-line count, and RAW; OLD (disk) vs NEW (the ON page).
Run from CONVERTER_V2/reference/tests under WSL: python3 ../../outputs/_r442_dips.py
"""
import os, sys, difflib
from collections import Counter
sys.path.insert(0, os.getcwd())
from _discrepancy_audit import pairs
from _skeleton_compare import match, _skel

O = os.path.join("..", "..", "outputs")
for n, cp, hp in pairs("MXFL202"):
    onp = os.path.join(O, "_r442_on", "MXFL202", os.path.basename(cp))
    if not os.path.exists(onp):
        continue
    out = []
    for label, c in (("OLD", cp), ("NEW", onp)):
        s, a, b = match(c, hp, scaffold=True)
        r = match(c, hp)[0]
        ca, cb = Counter(a), Counter(b)
        inter = sum((ca & cb).values())
        sm = difflib.SequenceMatcher(None, b, a, autojunk=False)
        matched = sum(bl.size for bl in sm.get_matching_blocks())
        out.append((label, s, inter / max(1, len(b)), matched, r, len(a), len(b)))
    (lo, so, po, mo, ro, lao, lb), (ln, sn, pn, mn, rn, lan, _) = out
    print(f"{os.path.basename(cp):18s} gold {lb:4d} lines | SCAFFOLD {100*so:5.1f} -> {100*sn:5.1f} | position-free overlap "
          f"{100*po:5.1f} -> {100*pn:5.1f} | matched lines {mo} -> {mn} | RAW {100*ro:5.1f} -> {100*rn:5.1f} | claude lines {lao} -> {lan}")
