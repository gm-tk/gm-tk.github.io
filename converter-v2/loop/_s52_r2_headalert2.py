#!/usr/bin/env python3
"""_s52_r2_headalert2.py — session 52 Round 2: the summary-heading texts only, per (text, family): Claude-BARE headings and how
many of them the gold boxes in an alert, the gold heading tag inside the box, and the Claude tag. WSL, from reference/tests/:
    python3 ../../outputs/_s52_r2_headalert2.py > ../../outputs/_s52_r2_headalert2.log"""
import os, re, sys, collections
sys.path.insert(0, os.getcwd())
import compare_structure as CS
famof = lambda m: re.sub(r"\d.*$", "", m)
PAT = re.compile(r"^(lesson summary|key points|key questions|what have (?:we|you) learned|summary|in summary)$")
bare = collections.Counter(); boxed = collections.Counter(); tags = collections.defaultdict(collections.Counter)
mods = collections.defaultdict(set); ex = collections.defaultdict(list)
mlist = sorted(m for m in CS._corpus.gate_mods(CS.CLAUDE)
               if os.path.isdir(CS._corpus.mdir(CS.CLAUDE, m)) and os.path.isdir(CS._corpus.mdir(CS.HUMAN, m)))
for mod in mlist:
    cdir = CS._corpus.mdir(CS.CLAUDE, mod); hdir = CS._corpus.mdir(CS.HUMAN, mod)
    cpages = sorted([f for f in os.listdir(cdir) if f.endswith(".html")], key=CS.page_sort_key)
    hpages = sorted(CS._corpus.gold_pages(mod, [f for f in os.listdir(hdir) if f.endswith(".html")]), key=CS.page_sort_key)
    for ci in range(min(len(cpages), len(hpages))):
        cp = CS.parse_page(os.path.join(cdir, cpages[ci])); hp = CS.parse_page(os.path.join(hdir, hpages[ci]))
        hindex = {}
        for e in hp.elements:
            if e["tag"][:1] == "h": hindex.setdefault(e["text"][:80], []).append(e)
        for e in cp.elements:
            if e["tag"] not in ("h2", "h3", "h4", "h5") or not PAT.match(e["text"]): continue
            if set(e["chain"]) & CS.CALLOUT_CLASSES: continue
            m = hindex.get(e["text"][:80])
            k = (e["text"], famof(mod))
            bare[k] += 1; mods[k].add(mod)
            if m and "alert" in set(m[0]["chain"]):
                boxed[k] += 1; tags[k][f"{e['tag']}->{m[0]['tag']}"] += 1
            elif len(ex[k]) < 2:
                ex[k].append(f"{cpages[ci]} gold {'-' if not m else m[0]['tag'] + str(sorted(set(m[0]['chain']) & CS.CALLOUT_CLASSES))}")
for t in sorted({k[0] for k in bare}):
    ks = sorted((k for k in bare if k[0] == t), key=lambda k: -bare[k])
    B = sum(bare[k] for k in ks); X = sum(boxed[k] for k in ks)
    print(f"\n{t!r}: bare {B}, gold-boxed {X} ({X / B:.2f})")
    for k in ks:
        print(f"   {k[1]:8s} bare {bare[k]:3d} boxed {boxed[k]:3d} mods {len(mods[k]):2d} tags {dict(tags[k])} {ex[k]}")
