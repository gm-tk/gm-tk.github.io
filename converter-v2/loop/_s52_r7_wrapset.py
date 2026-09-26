#!/usr/bin/env python3
"""_s52_r7_wrapset.py — session 52 Round 7: compare_structure's `wrapper_set` bucket (same wrappers, different nesting /
duplication) split by (Claude chain, gold chain) pair, per family, with examples. WSL, from reference/tests/:
    python3 ../../outputs/_s52_r7_wrapset.py > ../../outputs/_s52_r7_wrapset.log"""
import os, re, sys, collections
sys.path.insert(0, os.getcwd())
import compare_structure as CS
fam = lambda t: "h" if t.startswith("h") else t
famof = lambda m: re.sub(r"\d.*$", "", m)
by = collections.Counter(); pages = collections.defaultdict(set); mods = collections.defaultdict(set)
fams = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list)
mlist = sorted(m for m in CS._corpus.gate_mods(CS.CLAUDE)
               if os.path.isdir(CS._corpus.mdir(CS.CLAUDE, m)) and os.path.isdir(CS._corpus.mdir(CS.HUMAN, m)))
for mod in mlist:
    cdir = CS._corpus.mdir(CS.CLAUDE, mod); hdir = CS._corpus.mdir(CS.HUMAN, mod)
    cpages = sorted([f for f in os.listdir(cdir) if f.endswith(".html")], key=CS.page_sort_key)
    hpages = sorted(CS._corpus.gold_pages(mod, [f for f in os.listdir(hdir) if f.endswith(".html")]), key=CS.page_sort_key)
    for ci in range(min(len(cpages), len(hpages))):
        cp = CS.parse_page(os.path.join(cdir, cpages[ci])); hp = CS.parse_page(os.path.join(hdir, hpages[ci]))
        hindex = {}
        for e in hp.elements: hindex.setdefault((fam(e["tag"]), e["text"][:80]), []).append(e)
        for e in cp.elements:
            m = hindex.get((fam(e["tag"]), e["text"][:80]))
            if not m: continue
            cch, hch = list(e["chain"]), list(m[0]["chain"])
            if cch == hch or set(cch) != set(hch): continue
            k = f"claude {'>'.join(cch)}  |  gold {'>'.join(hch)}"
            by[k] += 1; pages[k].add(cpages[ci]); mods[k].add(mod); fams[k][famof(mod)] += 1
            if len(ex[k]) < 3: ex[k].append(f"{cpages[ci]} <{e['tag']}> {e['text'][:50]!r}")
print("wrapper_set elements", sum(by.values()))
for k, n in by.most_common(16):
    print(f"\n{n:5d} el / {len(pages[k]):4d} pages / {len(mods[k]):3d} mods  {k}")
    print("   fams:", ", ".join(f"{f} {c}" for f, c in fams[k].most_common(8)))
    for x in ex[k]: print("   e.g.", x)
