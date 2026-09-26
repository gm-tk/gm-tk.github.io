#!/usr/bin/env python3
"""_s51_cslost.py — compare_structure's own element matcher: the gold-matched Claude elements present in an OFF copy of a module
(a probe's --save dir) but NOT in the on-disk (ON) pages — what a round took out of the matched set. WSL, from reference/tests/:
python3 ../../outputs/_s51_cslost.py OFFDIR CODE…"""
import os, sys
sys.path.insert(0, os.getcwd())
import compare_structure as CS
import _corpus
from anchor_compare import CLAUDE, HUMAN

off = sys.argv[1]
fam = lambda t: "h" if t.startswith("h") else t
for mod in sys.argv[2:]:
    cdir = _corpus.mdir(CLAUDE, mod); hdir = _corpus.mdir(HUMAN, mod)
    cpages = sorted([f for f in os.listdir(cdir) if f.endswith(".html")], key=CS.page_sort_key)
    hpages = sorted(_corpus.gold_pages(mod, [f for f in os.listdir(hdir) if f.endswith(".html")]), key=CS.page_sort_key)
    for ci in range(min(len(cpages), len(hpages))):
        hp = CS.parse_page(os.path.join(hdir, hpages[ci]))
        hkeys = {(fam(e["tag"]), e["text"][:80]) for e in hp.elements}
        on = CS.parse_page(os.path.join(cdir, cpages[ci]))
        offp = os.path.join(off, mod, cpages[ci])
        if not os.path.exists(offp): continue
        of = CS.parse_page(offp)
        mk = lambda p: [(fam(e["tag"]), e["text"][:80]) for e in p.elements if (fam(e["tag"]), e["text"][:80]) in hkeys]
        a, b = mk(of), mk(on)
        lost = [k for k in a if k not in b]; gained = [k for k in b if k not in a]
        for k in lost: print(f"{mod} {cpages[ci]} LOST   {k[0]} {k[1][:90]}")
        for k in gained: print(f"{mod} {cpages[ci]} GAINED {k[0]} {k[1][:90]}")
