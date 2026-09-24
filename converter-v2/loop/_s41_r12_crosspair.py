#!/usr/bin/env python3
"""Session 41 Round 12 PICK — CROSSED PAIRS in the gate's pairing. For every module: the gate's pairs (_discrepancy_audit.pairs);
a pair is CROSSED when the Claude page's lesson number and the gold page's lesson number (the first number in each file name
after the code) differ while BOTH pages' own-number partners exist in the other's pair list — i.e. a 2-cycle (Claude A↔gold B,
Claude B↔gold A). For each 2-cycle: the SCAFFOLD sum as paired vs swapped (A↔A, B↔B). Run under WSL from reference/tests."""
import os, re, sys, collections
sys.path.insert(0, os.getcwd())
import _discrepancy_audit as DA, _corpus
from _skeleton_compare import match
from anchor_compare import CLAUDE
def num(name, code):
    m = re.search(re.escape(code) + r"[_\-. ]*0*(\d+)", name) or re.search(r"(\d+)", name)
    return m.group(1) if m else None
tot = collections.Counter(); rows = []
for code in sorted(_corpus.gate_mods(CLAUDE)):
    P = list(DA.pairs(code))
    byC = {}; byG = {}
    for _, cp, hp in P:
        cn, gn = num(os.path.basename(cp), code), num(os.path.basename(hp), code)
        byC[cn] = (cp, hp, gn); byG[gn] = (cp, hp, cn)
    seen = set()
    for cn, (cp, hp, gn) in byC.items():
        if cn is None or gn is None or cn == gn or (cn, gn) in seen: continue
        # the 2-cycle: Claude cn ↔ gold gn and Claude gn ↔ gold cn
        if gn in byC and byC[gn][2] == cn:
            cp2, hp2, _ = byC[gn]; seen.add((cn, gn)); seen.add((gn, cn))
            a = match(cp, hp, scaffold=True)[0] + match(cp2, hp2, scaffold=True)[0]
            b = match(cp, hp2, scaffold=True)[0] + match(cp2, hp, scaffold=True)[0]
            tot["cycles"] += 1; tot["better_swapped"] += b > a
            rows.append(f"{code}: Claude {cn}<->gold {gn} + Claude {gn}<->gold {cn}: paired {100*a:.1f} / swapped {100*b:.1f} ({100*(b-a):+.1f})")
        else:
            tot["other crossed"] += 1
print(dict(tot))
for r in rows: print("  ", r)
