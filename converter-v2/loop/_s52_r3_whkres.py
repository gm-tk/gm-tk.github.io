#!/usr/bin/env python3
"""_s52_r3_whkres.py — session 52 Round 3: the whakataukī residue after r528 — every gold div.whakatauki box whose first element
Claude renders bare, with the WT items around that text (outputs/_s52_items/<CODE>.tsv: 2 before, 3 after). WSL, from
reference/tests/:  python3 ../../outputs/_s52_r3_whkres.py > ../../outputs/_s52_r3_whkres.log"""
import os, re, sys
sys.path.insert(0, os.getcwd())
import compare_structure as CS
O = os.path.dirname(os.path.abspath(__file__))
fam = lambda t: "h" if t.startswith("h") else t
nt = CS.norm_text
def items_of(mod):
    p = os.path.join(O, "_s52_items", mod + ".tsv")
    if not os.path.exists(p): return []
    out = []
    for line in open(p, encoding="utf-8"):
        f = line.rstrip("\n").split("\t")
        if len(f) < 9: continue
        body = f[7] if f[2] == "tag" else f[8]
        out.append((f, nt(re.sub(r"\*+|<[^>]+>", "", body))))
    return out
mlist = sorted(m for m in CS._corpus.gate_mods(CS.CLAUDE)
               if os.path.isdir(CS._corpus.mdir(CS.CLAUDE, m)) and os.path.isdir(CS._corpus.mdir(CS.HUMAN, m)))
n = 0
for mod in mlist:
    cdir = CS._corpus.mdir(CS.CLAUDE, mod); hdir = CS._corpus.mdir(CS.HUMAN, mod)
    cpages = sorted([f for f in os.listdir(cdir) if f.endswith(".html")], key=CS.page_sort_key)
    hpages = sorted(CS._corpus.gold_pages(mod, [f for f in os.listdir(hdir) if f.endswith(".html")]), key=CS.page_sort_key)
    items = None
    for ci in range(min(len(cpages), len(hpages))):
        cp = CS.parse_page(os.path.join(cdir, cpages[ci])); hp = CS.parse_page(os.path.join(hdir, hpages[ci]))
        cindex = {}
        for e in cp.elements: cindex.setdefault((fam(e["tag"]), e["text"][:80]), []).append(e)
        els = hp.elements; i = 0
        while i < len(els):
            if "whakatauki" not in set(els[i]["chain"]): i += 1; continue
            j = i
            while j < len(els) and "whakatauki" in set(els[j]["chain"]): j += 1
            run = els[i:j]; i = j
            first = next((e for e in run if len(e["text"]) >= 6), None)
            if not first: continue
            m = cindex.get((fam(first["tag"]), first["text"][:80]))
            if not m or "whakatauki" in set(m[0]["chain"]): continue
            n += 1
            if items is None: items = items_of(mod)
            key = first["text"][:30]
            hit = next((x for x, it in enumerate(items) if key and key in it[1]), None)
            print(f"\n== {cpages[ci]} gold: " + " / ".join(e["text"][:45] for e in run[:3]) + f"  | claude chain {list(m[0]['chain'])[-3:]}")
            if hit is None: print("   (not in the WT items)"); continue
            for x in range(max(0, hit - 2), min(len(items), hit + 4)):
                f = items[x][0]
                print(f"   {'>' if x == hit else ' '} {f[2]:5s} {f[3]:14s} {f[5]:1s} t={f[6][:30]!r} a={(f[7] or f[8])[:90]!r}")
print("\nRUNS", n)
