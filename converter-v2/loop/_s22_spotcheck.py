#!/usr/bin/env python3
"""Session 22 spot check: print the text-bearing scaffold diff (the miner's own lines) for a few
named pages so a human-style read can look for a mechanism the class queue hides.
Usage: python3 _s22_spotcheck.py CODE:PAGE_SUFFIX ...   e.g. AGH1002:_2_0 BLL234:_0_0
"""
import os, sys, difflib
BASE = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.normpath(os.path.join(BASE, "..", "reference", "tests"))
for p in (BASE,):
    if p in sys.path:
        sys.path.remove(p)
sys.path.insert(0, TESTS)
import _diff_miner as dm
from _discrepancy_audit import pairs

def show(code, suffix):
    for n, cp, hp in pairs(code):
        if suffix not in os.path.basename(cp):
            continue
        g, _ = dm.page_lines(hp)
        c, _ = dm.page_lines(cp)
        gl = [("%s  <%s> %s" % (x.sig, x.region, (x.text or "")[:70])) for x in g]
        cl = [("%s  <%s> %s" % (x.sig, x.region, (x.text or "")[:70])) for x in c]
        print("=" * 100)
        print("%s  gold=%s  claude=%s  gold_lines=%d claude_lines=%d" % (code, os.path.basename(hp), os.path.basename(cp), len(gl), len(cl)))
        sm = difflib.SequenceMatcher(None, [x.sig for x in g], [x.sig for x in c], autojunk=False)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                if i2 - i1 > 2:
                    print("   = %s" % gl[i1]); print("   = ... %d equal ..." % (i2 - i1 - 2)); print("   = %s" % gl[i2 - 1])
                else:
                    for k in range(i1, i2): print("   = %s" % gl[k])
                continue
            for k in range(i1, i2): print("  -G %s" % gl[k])
            for k in range(j1, j2): print("  +C %s" % cl[k])

for arg in sys.argv[1:]:
    code, suf = arg.split(":")
    show(code, suf)
