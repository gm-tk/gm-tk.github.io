#!/usr/bin/env python3
"""_s51_r7_intro.py — session 51 Round 7 PICK: the writer's bare red `[Introduction]` tag — per module family, the gold's form
for the "Introduction" heading on the overview page (tag + the class of its column + whether it is alone in its row) against
Claude's. WSL, from reference/tests/."""
import os, re, sys, glob, collections
sys.path.insert(0, os.getcwd())
import _corpus
from anchor_compare import CLAUDE, HUMAN
from _discrepancy_audit import pairs

TAG = re.compile(r"🔴\[RED TEXT\]\s*\[\s*introduction\s*\]\s*\[/RED TEXT\]🔴", re.I)
HEAD = re.compile(r'<div class="row[^"]*">\s*<div class="([^"]*)">\s*<(h[1-6])[^>]*>\s*Introduction\s*</\2>\s*(</div>)?', re.I)
g = collections.defaultdict(collections.Counter); c = collections.defaultdict(collections.Counter); n = collections.Counter()
for code in sorted(_corpus.gate_mods(CLAUDE)):
    gd = _corpus.mdir(HUMAN, code)
    w = [f for f in glob.glob(os.path.join(gd, "*_parsed.txt")) if "Writers" in f]
    if not w or not TAG.search(open(w[0], encoding="utf-8", errors="replace").read()): continue
    fam = re.sub(r"\d.*$", "", code); n[fam] += 1
    for _, cp, hp in pairs(code):
        for side, path, agg in (("g", hp, g), ("c", cp, c)):
            m = HEAD.search(open(path, encoding="utf-8", errors="replace").read())
            if m: agg[fam][f"{m.group(2)} in {m.group(1).strip()}{' ALONE' if m.group(3) else ''}"] += 1
for fam in sorted(n, key=lambda f: -n[f]):
    print(f"{fam:8s} modules {n[fam]:3d}  gold {dict(g[fam].most_common(3))}  ||  claude {dict(c[fam].most_common(3))}")
