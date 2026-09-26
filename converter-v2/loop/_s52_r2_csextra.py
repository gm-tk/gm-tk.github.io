#!/usr/bin/env python3
"""_s52_r2_csextra.py — session 52 Round 2: compare_structure's EXTRA-container elements whose extra class is `alert`, on a module
list — page, element, text, chains. WSL, from reference/tests/:  python3 ../../outputs/_s52_r2_csextra.py MODLIST"""
import os, sys
sys.path.insert(0, os.getcwd())
import compare_structure as CS
fam = lambda t: "h" if t.startswith("h") else t
mods = [l.strip() for l in open(sys.argv[1]) if l.strip()]
n = 0
for mod in mods:
    try:
        cdir = CS._corpus.mdir(CS.CLAUDE, mod); hdir = CS._corpus.mdir(CS.HUMAN, mod)
    except Exception:
        continue
    if not cdir or not hdir or not os.path.isdir(cdir) or not os.path.isdir(hdir): continue
    cpages = sorted([f for f in os.listdir(cdir) if f.endswith(".html")], key=CS.page_sort_key)
    hpages = sorted(CS._corpus.gold_pages(mod, [f for f in os.listdir(hdir) if f.endswith(".html")]), key=CS.page_sort_key)
    for ci in range(min(len(cpages), len(hpages))):
        cp = CS.parse_page(os.path.join(cdir, cpages[ci])); hp = CS.parse_page(os.path.join(hdir, hpages[ci]))
        hindex = {}
        for e in hp.elements: hindex.setdefault((fam(e["tag"]), e["text"][:80]), []).append(e)
        for e in cp.elements:
            m = hindex.get((fam(e["tag"]), e["text"][:80]))
            if not m: continue
            cset, hset = set(e["chain"]), set(m[0]["chain"])
            if cset == hset: continue
            if "alert" in (cset - hset) & CS.CALLOUT_CLASSES:
                n += 1
                print(f"{cpages[ci]:22s} {hpages[ci]:26s} <{e['tag']}> {e['text'][:50]!r} claude {list(e['chain'])[-4:]} human {list(m[0]['chain'])[-4:]}")
print("EXTRA alert elements:", n)
