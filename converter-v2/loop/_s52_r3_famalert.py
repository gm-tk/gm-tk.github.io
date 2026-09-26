#!/usr/bin/env python3
"""_s52_r3_famalert.py — session 52 Round 3: for one family prefix (argv[1]), every gold alert RUN whose first element Claude
renders bare: page, the gold alert's class, its first 3 elements, and Claude's chain for the first. WSL, from reference/tests/:
    python3 ../../outputs/_s52_r3_famalert.py TRR"""
import os, re, sys, collections
sys.path.insert(0, os.getcwd())
import compare_structure as CS
FAM = sys.argv[1]
fam = lambda t: "h" if t.startswith("h") else t
mlist = sorted(m for m in CS._corpus.gate_mods(CS.CLAUDE) if re.sub(r"\d.*$", "", m) == FAM
               and os.path.isdir(CS._corpus.mdir(CS.CLAUDE, m)) and os.path.isdir(CS._corpus.mdir(CS.HUMAN, m)))
leads = collections.Counter(); n = 0
for mod in mlist:
    cdir = CS._corpus.mdir(CS.CLAUDE, mod); hdir = CS._corpus.mdir(CS.HUMAN, mod)
    cpages = sorted([f for f in os.listdir(cdir) if f.endswith(".html")], key=CS.page_sort_key)
    hpages = sorted(CS._corpus.gold_pages(mod, [f for f in os.listdir(hdir) if f.endswith(".html")]), key=CS.page_sort_key)
    for ci in range(min(len(cpages), len(hpages))):
        cp = CS.parse_page(os.path.join(cdir, cpages[ci])); hp = CS.parse_page(os.path.join(hdir, hpages[ci]))
        cindex = {}
        for e in cp.elements: cindex.setdefault((fam(e["tag"]), e["text"][:80]), []).append(e)
        els = hp.elements; i = 0
        while i < len(els):
            if "alert" not in set(els[i]["chain"]): i += 1; continue
            j = i
            while j < len(els) and "alert" in set(els[j]["chain"]): j += 1
            run = els[i:j]; i = j
            first = next((e for e in run if len(e["text"]) >= 8), None)
            if not first: continue
            m = cindex.get((fam(first["tag"]), first["text"][:80]))
            if not m or "alert" in set(m[0]["chain"]): continue
            n += 1; leads[first["text"][:30]] += 1
            print(f"{cpages[ci]:18s} {len(run):2d} el | " + " / ".join(f"<{e['tag']}> {e['text'][:40]}" for e in run[:3]) + f" | claude {list(m[0]['chain'])[-3:]}")
print("runs", n); print("leads:", leads.most_common(15))
