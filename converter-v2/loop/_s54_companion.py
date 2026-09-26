#!/usr/bin/env python3
"""_s54_companion.py — session 54: the §3 step-6 COMPANION numbers for a page dip: for each named page, the skeleton score and the
position-free overlap (multiset intersection of scaffold lines / the gold's line count) OFF vs ON, from two saved page dirs.
WSL, from reference/tests/:  python3 ../../outputs/_s54_companion.py OFFDIR ONDIR CODE/PAGE.html [...]"""
import os, sys, collections
sys.path.insert(0, os.getcwd())
from _discrepancy_audit import pairs
import _skeleton_compare as K
off, on = sys.argv[1], sys.argv[2]
for spec in sys.argv[3:]:
    code, page = spec.split("/")
    hp = next(h for n, c, h in pairs(code) if os.path.basename(c) == page)
    row = []
    for d in (off, on):
        r, a, b = K.match(os.path.join(d, code, page), hp, True)
        inter = sum((collections.Counter(a) & collections.Counter(b)).values())
        row.append((r * 100, inter, len(a), len(b)))
    (r0, i0, a0, g), (r1, i1, a1, _) = row
    print(f"{page:24s} score {r0:6.2f} -> {r1:6.2f} ({r1 - r0:+.2f})   position-free overlap {i0}/{g} -> {i1}/{g} ({i1 - i0:+d})   claude lines {a0} -> {a1}")
