#!/usr/bin/env python3
"""_s51_r13_csmiss.py — session 51 Round 13, a NEW instrument: compare_structure's 'claude MISSING container' (879) split by the
wrapper class(es) the human used, per module family, with the Claude chain's innermost container and examples. Same pairing and
matching as compare_structure.compare_module (document order, (tag family, text[:80]) index, interactive subtrees skipped).
WSL, from reference/tests/:  python3 ../../outputs/_s51_r13_csmiss.py > ../../outputs/_s51_r13_csmiss.log"""
import os, re, sys, collections
sys.path.insert(0, os.getcwd())
import compare_structure as CS

fam = lambda t: "h" if t.startswith("h") else t
famof = lambda m: re.sub(r"\d.*$", "", m)
by = collections.Counter(); pages = collections.defaultdict(set); mods = collections.defaultdict(set)
fams = collections.defaultdict(collections.Counter); inner = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list)
mlist = sorted(m for m in CS._corpus.gate_mods(CS.CLAUDE)
               if os.path.isdir(CS._corpus.mdir(CS.CLAUDE, m)) and os.path.isdir(CS._corpus.mdir(CS.HUMAN, m)))
for mod in mlist:
    try:
        cdir = CS._corpus.mdir(CS.CLAUDE, mod); hdir = CS._corpus.mdir(CS.HUMAN, mod)
    except Exception:
        continue
    if not cdir or not hdir or not os.path.isdir(cdir) or not os.path.isdir(hdir):
        continue
    cpages = sorted([f for f in os.listdir(cdir) if f.endswith(".html")], key=CS.page_sort_key)
    hpages = sorted(CS._corpus.gold_pages(mod, [f for f in os.listdir(hdir) if f.endswith(".html")]), key=CS.page_sort_key)
    if not cpages or not hpages:
        continue
    for ci in range(min(len(cpages), len(hpages))):
        cp = CS.parse_page(os.path.join(cdir, cpages[ci])); hp = CS.parse_page(os.path.join(hdir, hpages[ci]))
        hindex = {}
        for e in hp.elements:
            hindex.setdefault((fam(e["tag"]), e["text"][:80]), []).append(e)
        for e in cp.elements:
            m = hindex.get((fam(e["tag"]), e["text"][:80]))
            if not m:
                continue
            cch, hch = e["chain"], m[0]["chain"]
            if cch == hch or set(cch) == set(hch):
                continue
            cset, hset = set(cch), set(hch)
            if (cset - hset) & CS.CALLOUT_CLASSES:
                continue
            miss = (hset - cset) & CS.CALLOUT_CLASSES
            if not miss:
                continue
            k = " + ".join(sorted(miss))
            by[k] += 1; pages[k].add(cpages[ci]); mods[k].add(mod); fams[k][famof(mod)] += 1
            inner[k][(list(cch)[-1] if cch else "-") + " | " + e["tag"]] += 1
            if len(ex[k]) < 4:
                ex[k].append(f"{cpages[ci]} <{e['tag']}> {e['text'][:50]!r}  claude {list(cch)[-4:]}  human {list(hch)[-4:]}")
tot = sum(by.values())
print(f"MISSING-container elements {tot}")
for k, n in by.most_common(14):
    print(f"\n{n:5d} el / {len(pages[k]):4d} pages / {len(mods[k]):3d} modules  human wrapped in [{k}]")
    print("   families:", ", ".join(f"{f} {c}" for f, c in fams[k].most_common(8)))
    print("   claude innermost | tag:", ", ".join(f"{i} {c}" for i, c in inner[k].most_common(5)))
    for x in ex[k]: print("   e.g.", x)
