#!/usr/bin/env python3
"""ROUND 440 (session 39 Round 2 — D13-6, the dual-build gold pairing) — the BEFORE picture.
For the five dual-build modules: every gold .html on disk, every Claude page, and how the three pairing
paths pair them today — pairs() (skeleton + miner, content-first) with each pair's SCAFFOLD score, and the
positional pairing compare_structure / body_compare use.
Run from CONVERTER_V2/reference/tests under WSL: python3 ../../outputs/_r440_pairs_probe.py
"""
import os, sys
sys.path.insert(0, os.getcwd())
import _corpus
from _discrepancy_audit import pairs, HUMAN
from anchor_compare import CLAUDE
from _skeleton_compare import match
import compare_structure as CS

MODS = ["MXFUN01", "BLL240", "CEDT207", "CEDT301", "CEDK501"]
tot_pairs = 0
for code in MODS:
    cdir, hdir = _corpus.mdir(CLAUDE, code), _corpus.mdir(HUMAN, code)
    cf = sorted(f for f in os.listdir(cdir) if f.endswith(".html"))
    hf = sorted(f for f in os.listdir(hdir) if f.endswith(".html"))
    print("=" * 100)
    print(f"{code}: claude {len(cf)} pages, gold {len(hf)} files: {hf}")
    pr = pairs(code)
    tot_pairs += len(pr)
    sc = []
    for n, cp, hp in pr:
        s, r = match(cp, hp, scaffold=True)[0], match(cp, hp)[0]
        sc.append(s)
        print(f"   pairs(): {os.path.basename(cp):22s} <-> {os.path.basename(hp):45s} scaffold {100*s:5.1f}  raw {100*r:5.1f}")
    if sc:
        print(f"   pairs() n={len(sc)} mean scaffold {100*sum(sc)/len(sc):.2f}")
    unpaired_c = [f for f in cf if f not in {os.path.basename(p[1]) for p in pr}]
    unpaired_h = [f for f in hf if f not in {os.path.basename(p[2]) for p in pr}]
    print(f"   unpaired claude: {unpaired_c}")
    print(f"   unpaired gold  : {unpaired_h}")
    cpos = sorted(cf, key=CS.page_sort_key)
    hpos = sorted(hf, key=CS.page_sort_key)
    print("   positional (compare_structure / body_compare): " +
          ", ".join(f"{a}<->{b}" for a, b in zip(cpos, hpos)))
print(f"TOTAL pairs() pairs over the five: {tot_pairs}")
