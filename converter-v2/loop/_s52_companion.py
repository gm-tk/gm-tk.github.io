#!/usr/bin/env python3
"""_s52_companion.py — session 52: the §3 step-6 companion numbers for a page dip — the skeleton gate's own match() before
and after, plus the POSITION-FREE overlap (multiset intersection of scaffold lines / gold lines) and the matched-line count,
disk (OFF) vs a saved ON page. WSL, from reference/tests/:  python3 ../../outputs/_s52_companion.py SAVEDIR CODE PAGE…"""
import os, sys, collections, difflib
sys.path.insert(0, os.getcwd())
from _discrepancy_audit import pairs
import _skeleton_compare as K
save, code = sys.argv[1], sys.argv[2]
want = set(sys.argv[3:])
for n, cp, hp in pairs(code):
    b = os.path.basename(cp)
    if want and b not in want: continue
    on = os.path.join(save, code, b)
    if not os.path.exists(on): continue
    g = K._skel(hp, True)
    for tag, path in (("OFF", cp), ("ON ", on)):
        c = K._skel(path, True)
        sc = K.match(path, hp, True)[0]
        inter = sum((collections.Counter(g) & collections.Counter(c)).values())
        sm = difflib.SequenceMatcher(None, g, c, autojunk=False)
        matched = sum(bl.size for bl in sm.get_matching_blocks())
        print(f"{b:24s} {tag} scaffold {sc * 100:6.2f}  position-free overlap {inter}/{len(g)} ({inter / max(1, len(g)) * 100:5.1f} %)  matched lines {matched}  claude lines {len(c)}")
