#!/usr/bin/env python3
"""_s52_r14_overgen.py — session 52 Round 14: the scaffold LENGTH ratio per paired page (Claude lines / gold lines) — the
over-generating pages (ratio ≥ 1.4) and the under-generating ones (≤ 0.7), per family, with each family's mean score on them, and the
scaffold lines Claude has most in EXCESS on the over-generating pages (a multiset difference of signatures). WSL, from
reference/tests/:  python3 ../../outputs/_s52_r14_overgen.py"""
import os, sys, re, collections
sys.path.insert(0, os.getcwd())
from _discrepancy_audit import pairs
import _skeleton_compare as K
import compare_structure as CS
import _corpus
famof = lambda m: re.sub(r"\d.*$", "", m)
over = collections.Counter(); under = collections.Counter(); tot = collections.Counter(); excess = collections.Counter(); deficit = collections.Counter()
ex = collections.defaultdict(list)
for mod in sorted(m for m in _corpus.gate_mods(CS.CLAUDE) if os.path.isdir(_corpus.mdir(CS.CLAUDE, m))):
    for n, cp, hp in pairs(mod):
        c = K._skel(cp, True); g = K._skel(hp, True)
        if not g: continue
        r = len(c) / len(g); f = famof(mod); tot[f] += 1
        strip = lambda x: x.strip().split("  ")[0].strip()
        if r >= 1.4:
            over[f] += 1
            d = collections.Counter(map(strip, c)) - collections.Counter(map(strip, g))
            excess.update(d)
            if len(ex[f]) < 2: ex[f].append(f"{os.path.basename(cp)} {len(c)}/{len(g)}")
        elif r <= 0.7:
            under[f] += 1
            deficit.update(collections.Counter(map(strip, g)) - collections.Counter(map(strip, c)))
print("OVER-generating pages (ratio >= 1.4):", sum(over.values()), "; UNDER (<= 0.7):", sum(under.values()), "of", sum(tot.values()))
print("over by family:", ", ".join(f"{f} {n}/{tot[f]}" for f, n in over.most_common(14)))
print("under by family:", ", ".join(f"{f} {n}/{tot[f]}" for f, n in under.most_common(14)))
print("\nlines in EXCESS on the over-generating pages:", excess.most_common(18))
print("\nlines in DEFICIT on the under-generating pages:", deficit.most_common(18))
for f, l in list(ex.items())[:10]: print("  e.g.", f, l)
