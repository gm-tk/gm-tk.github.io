#!/usr/bin/env python3
"""Session 27 Round 5 — skeleton opcode diff for one page pair: the gate's own skeleton lines (scaffold), the difflib
opcodes with sizes, and the first lines of each block so the ORDER failure can be read.
  wsl: python3 _s27_r5_skdiff.py CODE PAGEFILE [maxlines]"""
import os, sys, re, difflib
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS); sys.path.insert(1, OUTPUTS)
from _discrepancy_audit import pairs
from _skeleton_compare import match
code, pg = sys.argv[1], sys.argv[2]; maxl = int(sys.argv[3]) if len(sys.argv) > 3 else 6
for n, cp, hp in pairs(code):
    if os.path.basename(cp) != pg: continue
    r, a, b = match(cp, hp, True)   # a = claude lines, b = gold lines
    print(f"{code}/{pg}: gate {100*r:.1f}  claude {len(a)} lines  gold {os.path.basename(hp)} {len(b)} lines")
    sm = difflib.SequenceMatcher(None, b, a, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal" and (i2 - i1) < 3: continue
        print(f"\n[{tag:7s}] gold {i1}-{i2} ({i2-i1})  claude {j1}-{j2} ({j2-j1})")
        if tag != "equal":
            for l in b[i1:i1 + maxl]: print("   G  " + l.rstrip()[:110])
            if i2 - i1 > maxl: print(f"   G  … +{i2-i1-maxl}")
            for l in a[j1:j1 + maxl]: print("   C  " + l.rstrip()[:110])
            if j2 - j1 > maxl: print(f"   C  … +{j2-j1-maxl}")
        else:
            print("   =  " + a[j1].rstrip()[:100] + f"  … ({i2-i1} equal)")
    break
