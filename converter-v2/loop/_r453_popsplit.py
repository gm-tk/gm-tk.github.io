#!/usr/bin/env python3
"""ROUND 453 — THE §1e POPULATION SPLIT of the skeleton gate. For the 13 changed modules: OLD = pairs() with the Claude dir
pointed at the TABLETB_OFF pages (outputs/_r453_offsave = the r452 state, proven byte-identical by the OFF probe); NEW = pairs()
over the regenerated disk. Matched BY GOLD PAGE: EXISTING pairs (a gold page paired on both sides) vs NEW pairs (paired only
after r453). Prints the pre-existing subset's delta — the hold-or-improve test on an unchanged population — and the new pairs.
Run from CONVERTER_V2/reference/tests under WSL: python3 ../../outputs/_r453_popsplit.py"""
import os, sys
sys.path.insert(0, os.getcwd())
import _discrepancy_audit as DA
import _corpus
from _skeleton_compare import match
from anchor_compare import CLAUDE

O = os.path.abspath(os.path.join("..", "..", "outputs"))
codes = [c.strip() for c in open(os.path.join(O, "_r453_changed13.txt")) if c.strip()]
_mdir = _corpus.mdir
OFF = {"on": False}
def mdir(root, *parts):
    if OFF["on"] and os.path.abspath(root) == os.path.abspath(CLAUDE) and parts and parts[0] in codes:
        return os.path.join(O, "_r453_offsave", parts[0])
    return _mdir(root, *parts)
_corpus.mdir = mdir
DA._corpus.mdir = mdir

def score(code):
    return {os.path.basename(hp): (os.path.basename(cp), match(cp, hp, scaffold=True)[0], match(cp, hp, scaffold=False)[0])
            for n, cp, hp in DA.pairs(code)}

ex_o = ex_n = 0.0; nex = 0; newp = []; lost = []; rows = []
for code in codes:
    OFF["on"] = True; old = score(code)
    OFF["on"] = False; new = score(code)
    for h in sorted(set(old) | set(new)):
        o, n = old.get(h), new.get(h)
        if o and n:
            ex_o += o[1]; ex_n += n[1]; nex += 1
            if abs(n[1] - o[1]) > 1e-9:
                rows.append((n[1] - o[1], code, h, o, n))
        elif n:
            newp.append((code, h, n))
        else:
            lost.append((code, h, o))
rows.sort()
print(f"EXISTING pairs (same gold page both sides): {nex}; SCAFFOLD sum {100*ex_o:.1f} -> {100*ex_n:.1f} ({100*(ex_n-ex_o):+.1f}pp-sum)")
for d, code, h, o, n in rows:
    print(f"   {h:26s} {o[0]:16s} {100*o[1]:5.1f} -> {n[0]:16s} {100*n[1]:5.1f} ({100*d:+.1f})   RAW {100*o[2]:5.1f} -> {100*n[2]:5.1f}")
print(f"NEW pairs (paired only after r453): {len(newp)}, mean {100*sum(x[2][1] for x in newp)/max(1,len(newp)):.1f}")
for code, h, n in newp:
    print(f"   {h:26s} {n[0]:16s} {100*n[1]:5.1f}")
print(f"LOST pairs: {len(lost)} {lost}")
BASE_MEAN, BASE_PAIRS = 54.7484, 2477
pre = (BASE_MEAN * BASE_PAIRS + 100 * (ex_n - ex_o)) / BASE_PAIRS
print(f"\nskeleton on the PRE-EXISTING population ({BASE_PAIRS} pairs): {BASE_MEAN:.4f} -> {pre:.4f} ({pre-BASE_MEAN:+.4f}pp)")
allp = (BASE_MEAN * BASE_PAIRS + 100 * (ex_n - ex_o) + 100 * sum(x[2][1] for x in newp)) / (BASE_PAIRS + len(newp))
print(f"skeleton on the WHOLE population ({BASE_PAIRS + len(newp)} pairs): {BASE_MEAN:.4f} -> {allp:.4f} ({allp-BASE_MEAN:+.4f}pp)")
