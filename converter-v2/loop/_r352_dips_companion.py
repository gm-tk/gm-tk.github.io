#!/usr/bin/env python3
"""_r352_dips_companion.py — ROUND 352 proof: the LOOP §3 step-6 companion numbers for every skeleton dip page. For each page:
the skeleton SequenceMatcher ratio (the gate) BEFORE (the OFF engine's page, saved in outputs/_r352_off_sample) and AFTER (the
regenerated disk page), and two position-free companions — the multiset overlap of skeleton lines with the human's page
(|claude ∩ human| / |human|) and the raw count of matched lines. A dip is the scorer's alignment artefact only when a companion
RISES. Run from reference/tests: python3 ../../outputs/_r352_dips_companion.py CODE…"""
import os, sys, re, glob, json, difflib
from collections import Counter
sys.path.insert(0, ".")
import _corpus
import _structural_skeleton as S
from _structural_skeleton import skeleton
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)))
OFF = os.path.join(OUT, "_r352_off_sample")
def skel(path):
    S._SCAFFOLD = True
    sk = skeleton(path).splitlines()
    return sk[sk.index("body.container-fluid"):] if "body.container-fluid" in sk else sk
def ratio(a, b): return difflib.SequenceMatcher(None, b, a).ratio()
def overlap(a, b):
    ca, cb = Counter(a), Counter(b); inter = sum((ca & cb).values())
    return inter, (inter / len(b) if b else 0.0)
pre = json.load(open(os.path.join(OUT, "_r351_sk_final.json")))
post = json.load(open(os.path.join(OUT, "_r352_sk_final.json")))
P = {p["page"]: p["scaffold"] for p in pre["per_page"]}; Q = {p["page"]: p["scaffold"] for p in post["per_page"]}
codes = sys.argv[1:]
print(f"{'page':26} {'gate before':>11} {'after':>7} {'delta':>7} | {'overlap before':>14} {'after':>7} | {'matched lines before':>20} {'after':>6} | verdict")
for code in codes:
    for n, cp, hp in pairs(code):
        if re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I): continue
        name = os.path.basename(cp)
        if name not in P or abs(P[name] - Q[name]) < 1e-9: continue
        offp = os.path.join(OFF, code, name)
        if not os.path.exists(offp): continue
        h = skel(hp); a0 = skel(offp); a1 = skel(cp)
        r0, r1 = ratio(a0, h), ratio(a1, h)
        m0, o0 = overlap(a0, h); m1, o1 = overlap(a1, h)
        verdict = "artefact (companion rises)" if (r1 < r0 and (o1 > o0 or m1 > m0)) else ("gain" if r1 > r0 else "REAL dip")
        print(f"{name:26} {r0*100:11.2f} {r1*100:7.2f} {(r1-r0)*100:+7.2f} | {o0*100:14.2f} {o1*100:7.2f} | {m0:20d} {m1:6d} | {verdict}")
