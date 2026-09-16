#!/usr/bin/env python3
"""_r346_dips.py — ROUND 346: per moved page, our <math> count vs the gold's on the paired page, and how many of our
equations the gold carries with the same token text (tags stripped, whitespace removed). Run from anywhere under WSL."""
import re, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.normpath(os.path.join(HERE, "..", "reference", "tests")); sys.path.insert(0, TESTS)
from _discrepancy_audit import pairs, CLAUDE
M = re.compile(r"<math\b"); MB = re.compile(r"<math\b[\s\S]*?</math>")
def keys(h): return [re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", m.group(0))) for m in MB.finditer(h)]
mv = [l.split()[0] for l in open(os.path.join(HERE, "_r346_sk_movers.log"), encoding="utf-8") if l.strip().endswith(("raw", )) or " -> " in l]
mv = [p for p in mv if p.endswith(".html")]
by = {}
for p in mv: by.setdefault(p.split("_")[0], []).append(p)
for code, fs in by.items():
    for n, cp, hp in pairs(code):
        if os.path.basename(cp) in fs:
            c = open(cp, encoding="utf-8", errors="replace").read(); g = open(hp, encoding="utf-8", errors="replace").read()
            ck = keys(c); gk = keys(g); gset = set(gk); hit = sum(1 for k in ck if k in gset)
            disp = {}
            for d in re.findall(r'<math[^>]*display="(\w+)"', g): disp[d] = disp.get(d, 0) + 1
            print(f"{os.path.basename(cp):20s} gold {os.path.basename(hp):22s} claude<math> {len(ck):3d}  gold<math> {len(gk):3d}  ours-in-gold(text) {hit:3d}  gold display {disp}")
