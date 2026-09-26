#!/usr/bin/env python3
"""_s51_r3_acthead.py — session 51 Round 3 PICK: the writer's activity opener typed in ONE red span with a heading tag, either
order — `[Activity 1A] [H3] Title` / `[H3] [Activity 2A] Title` (the heading's ELEMENT precedence wins, so no box opens and the
title ships as a bare <hN>). For each span: the title (the black text after it); where the GOLD puts a heading with that text
(container region, and whether that gold box carries the writer's id) and where Claude does. Per family. WSL, from
reference/tests/. Writes outputs/_s51_r3_acthead.tsv."""
import os, re, sys, glob, collections
sys.path.insert(0, os.getcwd()); sys.path.append("../../outputs")
import _corpus
import _placement_census as PC
from anchor_compare import CLAUDE, HUMAN

SPAN = re.compile(r"🔴\[RED TEXT\]((?:\s*\[[^\]]*\])+)\s*\[/RED TEXT\]🔴\s*([^🔴]*)")
ACT = re.compile(r"\[\s*activit(?:y|ies)\s*(\d{1,2}(?:\.\d+)?[a-z]?)?[^\]]*\]", re.I)
HD = re.compile(r"\[\s*h([1-6])\s*\]", re.I)
fold = lambda t: " ".join(re.sub(r"[^a-z0-9 ]", " ", re.sub(r"\*", "", t.lower())).split())
G = collections.defaultdict(collections.Counter); C = collections.defaultdict(collections.Counter); rows = []; nspan = collections.Counter()
for code in sorted(_corpus.gate_mods(CLAUDE)):
    gd = _corpus.mdir(HUMAN, code)
    wts = [f for f in glob.glob(os.path.join(gd, "*_parsed.txt")) if "Writers" in f]
    if not wts: continue
    txt = open(wts[0], encoding="utf-8", errors="replace").read()
    gb = [b for f in sorted(glob.glob(os.path.join(gd, "*.html"))) for b in PC.parse(f)]
    cd = _corpus.mdir(CLAUDE, code)
    cb = [b for f in sorted(glob.glob(os.path.join(cd, "*.html"))) for b in PC.parse(f)] if os.path.isdir(cd) else []
    fam = re.sub(r"\d.*$", "", code)
    for m in SPAN.finditer(txt):
        tags, after = m.group(1), m.group(2).split("\n")[0]
        a, h = ACT.search(tags), HD.search(tags)
        if not a or not h: continue
        title = fold(after)
        if len(title.split()) < 2: continue
        nspan[fam] += 1
        gh = [b for b in gb if re.match(r"h[1-6]$", b[0]) and PC.jacc(b[1], title) >= 0.6]
        ch = [b for b in cb if re.match(r"h[1-6]$", b[0]) and PC.jacc(b[1], title) >= 0.6]
        greg = gh[0][3] if gh else "—"; creg = ch[0][3] if ch else "—"
        G[fam][greg] += 1; C[fam][creg] += 1
        rows.append((code, (a.group(1) or "").upper(), "h" + h.group(1), greg, creg, after[:60]))
tot = collections.Counter(r[3] for r in rows); ctot = collections.Counter(r[4] for r in rows)
print("spans", len(rows), "modules", len({r[0] for r in rows}), "| gold", dict(tot.most_common(5)), "| claude", dict(ctot.most_common(5)))
for f in sorted(nspan, key=lambda f: -nspan[f]):
    n = sum(G[f].values()); act = sum(v for k, v in G[f].items() if k.endswith("activity"))
    print(f"{f:8s} spans {nspan[f]:3d} gold in-activity {act}/{n}  {dict(G[f].most_common(3))} || claude {dict(C[f].most_common(3))}")
with open("../../outputs/_s51_r3_acthead.tsv", "w") as fh:
    for r in rows: fh.write("\t".join(r) + "\n")
