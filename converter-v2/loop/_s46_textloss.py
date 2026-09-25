#!/usr/bin/env python3
"""Session 46 — did a round LOSE any text? For each page in NEW_DIR, every text block (≥ 20 folded chars) of the OLD render must still
appear somewhere on the NEW page (and vice versa, reported as ADDED). WSL, from outputs/: python3 _s46_textloss.py OLD_DIR NEW_DIR"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _s46_goldloc import P, fold
def blocks(path):
    p = P(); p.feed(open(path, encoding="utf-8", errors="replace").read())
    return [fold(d) for d, st in p.nodes if len(fold(d)) >= 20]
old_dir, new_dir = sys.argv[1], sys.argv[2]
tl = ta = 0
for code in sorted(os.listdir(new_dir)):
    for fn in sorted(os.listdir(os.path.join(new_dir, code))):
        if not fn.endswith(".html") or not os.path.exists(os.path.join(old_dir, code, fn)): continue
        o = blocks(os.path.join(old_dir, code, fn)); n = blocks(os.path.join(new_dir, code, fn))
        nj = " \n ".join(n); oj = " \n ".join(o)
        lost = [b for b in o if b not in nj]; added = [b for b in n if b not in oj]
        tl += len(lost); ta += len(added)
        if lost or added: print(f"{code}/{fn}: lost {len(lost)} added {len(added)}", [x[:50] for x in lost[:3]], [x[:50] for x in added[:2]])
print(f"TOTAL lost {tl} added {ta}")
