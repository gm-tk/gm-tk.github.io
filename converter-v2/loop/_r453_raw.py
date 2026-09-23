#!/usr/bin/env python3
"""ROUND 453 — the companion numbers for the named dips: SCAFFOLD and RAW, OLD (disk) vs NEW (_r453_on), same gold page."""
import os, sys
sys.path.insert(0, os.getcwd())
from _skeleton_compare import match
G = "../../../01-Finalized_Modules_/Bilingual"; C = "../../../01-Claude_Modules_/Bilingual"; N = "../../outputs/_r453_on"
for code, cold, cnew, gold in [("TRR102", "0_0", "0_0", "0.0"), ("TRR111", "0_0", "0_0", "0.0"), ("TRR114", "1_0", "1_0", "1.0"),
                               ("TRR116", "0_0", "5_0", "5_0"), ("TRR107", "0_0", "1_0", "1.0"), ("TRR107", "2_0", "2_0", "2.0")]:
    g = f"{G}/{code}/{code}_{gold}.html"
    o = f"{C}/{code}/{code}_{cold}.html"; n = f"{N}/{code}/{code}_{cnew}.html"
    so, ro = match(o, g, scaffold=True)[0], match(o, g, scaffold=False)[0]
    sn, rn = match(n, g, scaffold=True)[0], match(n, g, scaffold=False)[0]
    print(f"{code}_{gold}: SCAFFOLD {100*so:.1f} -> {100*sn:.1f}   RAW {100*ro:.1f} -> {100*rn:.1f}")
