#!/usr/bin/env python3
"""_s51_r2_summary.py — session 51 Round 2: the writer's bare red `[Summary]` tag (the lexicon resolves no tag — Claude ships a
Writers Note and the content free). For every occurrence, the next 1–3 content lines after it in the parsed Writers Template,
and the container the GOLD (and Claude) puts each in (the §1g census parser, text matched with jacc >= 0.6 on the module's
pages). Per family: the share of the gold's matched blocks inside `body:alert`. WSL, from reference/tests/."""
import os, re, sys, glob, collections
sys.path.insert(0, os.getcwd()); sys.path.append("../../outputs")
import _corpus
import _placement_census as PC
from anchor_compare import CLAUDE, HUMAN

TAG = re.compile(r"🔴\[RED TEXT\]\s*\[\s*summary\s*\]\s*\[/RED TEXT\]🔴\s*(.*)$", re.I)
fold = lambda s: re.sub(r"[^a-z0-9 ]", " ", re.sub(r"🔴\[/?RED TEXT\]🔴|\*", " ", s.lower())).split()
fam = collections.defaultdict(collections.Counter); cfam = collections.defaultdict(collections.Counter); occ = collections.Counter()
ex = []
for code in sorted(_corpus.gate_mods(CLAUDE)):
    gd = _corpus.mdir(HUMAN, code)
    wts = [f for f in glob.glob(os.path.join(gd, "*_parsed.txt")) if "Writers" in f]
    if not wts: continue
    lines = open(wts[0], encoding="utf-8", errors="replace").read().split("\n")
    gblocks = [b for f in sorted(glob.glob(os.path.join(gd, "*.html"))) for b in PC.parse(f)]
    cd = _corpus.mdir(CLAUDE, code)
    cblocks = [b for f in sorted(glob.glob(os.path.join(cd, "*.html"))) for b in PC.parse(f)] if os.path.isdir(cd) else []
    f = re.sub(r"\d.*$", "", code)
    for i, l in enumerate(lines):
        m = TAG.search(l)
        if not m: continue
        occ[f] += 1
        nxt = ([m.group(1)] if m.group(1).strip() else []) + [x for x in lines[i + 1:i + 8] if x.strip()][:3]
        for t in nxt[:3]:
            if "[RED TEXT]" in t and not re.sub(r"🔴\[RED TEXT\].*?\[/RED TEXT\]🔴", "", t).strip(): break
            w = " ".join(fold(t))
            if len(w.split()) < 3: continue
            best = max(gblocks, key=lambda b: PC.jacc(b[1], w), default=None)
            if best and PC.jacc(best[1], w) >= 0.6: fam[f][best[3]] += 1
            else: fam[f]["(none)"] += 1
            cb = max(cblocks, key=lambda b: PC.jacc(b[1], w), default=None)
            cfam[f][cb[3] if cb and PC.jacc(cb[1], w) >= 0.6 else "(none)"] += 1
            if len(ex) < 12: ex.append(f"{code}: {t[:70]} -> gold {best[3] if best else '-'}")
for f in sorted(occ, key=lambda f: -occ[f]):
    g = fam[f]; n = sum(v for k, v in g.items() if k != "(none)")
    print(f"{f:8s} [Summary] x{occ[f]:3d}  gold matched {n:3d}: alert {g['body:alert'] / max(1, n):4.2f} {dict(g.most_common(4))} || claude {dict(cfam[f].most_common(3))}")
print("\n".join(ex))
