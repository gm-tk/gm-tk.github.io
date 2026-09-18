#!/usr/bin/env python3
"""Session 26 — the supervisor panel's TEXT-column class (the inner row's second col), gold vs Claude, per template / subject /
series — the r390 miner row #3735 (`div.col-12 › EXTRA ul`) is a parent-label mismatch: gold `col-12 col-md-12` vs Claude `col-12`?
  python3 _s26_r391_panelcol.py"""
import sys, os, re
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS)
from _diff_miner import page_lines
from _discrepancy_audit import pairs
from _measure_ceiling import load_meta
import _corpus
from anchor_compare import CLAUDE
from collections import Counter, defaultdict
meta = load_meta()
fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
def subtree_end(L, i):
    d = L[i].depth; j = i + 1
    while j < len(L) and L[j].depth > d: j += 1
    return j
G = defaultdict(Counter); C = defaultdict(Counter); Gm = defaultdict(set); Cm = defaultdict(set)
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"
    ser = re.match(r"[A-Z]+\d?", code).group(0)
    for n, cp, hp in pairs(code):
        for lab, p, D, M in (("g", hp, G, Gm), ("c", cp, C, Cm)):
            try: L, _ = page_lines(p)
            except Exception: continue
            for i, l in enumerate(L):
                if not l.sig.startswith("div.row.super-content"): continue
                e = subtree_end(L, i)
                inner = [k for k in range(i + 1, e) if L[k].depth == l.depth + 1 and L[k].sig.startswith("div.row")]
                base = inner[0] if inner else i
                cols = [x.sig.split("[")[0] for x in L[base + 1:e] if x.depth == L[base].depth + 1 and x.sig.startswith("div.col")]
                key = cols[-1] if cols else "?"
                for k in ("ALL", tf, f"{tf}/{subj}", f"series={ser}"):
                    D[k][key] += 1; M[k].add(code)
print("==== the supervisor panel TEXT column (the inner row's last col) — gold vs Claude, per group ====")
for k in sorted(G, key=lambda x: (not x.startswith("ALL"), x.startswith("series"), x)):
    if sum(G[k].values()) < 5: continue
    print(f"  {k:36s} gold n={sum(G[k].values()):4d} m={len(Gm[k]):3d} {dict(G[k].most_common(3))}   claude n={sum(C[k].values()):4d} {dict(C[k].most_common(2))}")
