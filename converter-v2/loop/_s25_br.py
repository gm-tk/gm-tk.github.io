#!/usr/bin/env python3
"""Session 25 — the gold's <br> lines OUTSIDE widgets (the ledger's wrapper-empty br, 0.64pp): by parent signature and
by series, gold vs Claude; the share of pages per series carrying a block-level br (a column child, not inside a p)."""
import os, sys, re
from collections import Counter, defaultdict
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
sys.path.insert(0, TESTS)
import _corpus
from _skeleton_compare import _skel
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE
SKIP = re.compile(r"acks|acknowledge|glossary|references", re.I)
def ind(l): return len(l) - len(l.lstrip(" "))
fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
par = {"gold": Counter(), "claude": Counter()}; ser = defaultdict(lambda: {"gold": 0, "claude": 0, "pages": 0, "gpages": set()})
for code in sorted(fam):
    for n, cp, hp in pairs(code):
        if SKIP.search(os.path.basename(hp)) or SKIP.search(os.path.basename(cp)): continue
        S = ser[code[:5]]; S["pages"] += 1
        for side, path in (("gold", hp), ("claude", cp)):
            try: lines = _skel(path, True)
            except Exception: continue
            stack = []
            for l in lines:
                d = ind(l)
                while stack and stack[-1][0] >= d: stack.pop()
                if l.strip() == "br":
                    parent = stack[-1][1] if stack else "-"
                    par[side][parent] += 1; S[side] += 1
                    if side == "gold" and parent.startswith("div.col"): S["gpages"].add(hp)
                stack.append((d, l.strip().split("[")[0]))
print("gold br by parent:", par["gold"].most_common(10))
print("claude br by parent:", par["claude"].most_common(10))
print("\nseries with block-level gold br (a column child) on >= 0.5 of pages:")
for s, S in sorted(ser.items(), key=lambda kv: -len(kv[1]["gpages"])):
    if S["pages"] >= 10 and len(S["gpages"]) / S["pages"] >= 0.5:
        print(f"   {s} pages {S['pages']} gold-br-pages {len(S['gpages'])} ({len(S['gpages'])/S['pages']:.2f}) gold br {S['gold']} claude br {S['claude']}")
