#!/usr/bin/env python3
"""_s51_r8_lost.py — session 51 Round 8 PICK: gold body blocks (>= 5 words) whose text is on NO Claude page of the module but IS in
the Writers Template (the WT line holding >= 70 % of its words, all on one line). Split by whether that WT line's matching text is
BLACK (the converter lost learner content) or inside a RED span (a writer note the developer turned into text — class C), and
by the WT line's leading tag. WSL, from reference/tests/."""
import os, re, sys, glob, collections
sys.path.insert(0, os.getcwd()); sys.path.append("../../outputs")
import _corpus
import _placement_census as PC
from anchor_compare import CLAUDE, HUMAN

RED = re.compile(r"🔴\[RED TEXT\](.*?)\[/RED TEXT\]🔴")
fold = lambda t: " ".join(re.sub(r"[^a-z0-9 ]", " ", re.sub(r"\*", "", t.lower())).split())
kind = collections.Counter(); tagc = collections.Counter(); ex = collections.defaultdict(list); mods = collections.defaultdict(set)
for code in sorted(_corpus.gate_mods(CLAUDE)):
    gd = _corpus.mdir(HUMAN, code); cd = _corpus.mdir(CLAUDE, code)
    w = [f for f in glob.glob(os.path.join(gd, "*_parsed.txt")) if "Writers" in f]
    if not w or not os.path.isdir(cd): continue
    lines = open(w[0], encoding="utf-8", errors="replace").read().split("\n")
    black = [fold(RED.sub(" ", l)) for l in lines]; red = [fold(" ".join(RED.findall(l))) for l in lines]
    ctext = " ".join(b[1] for f in glob.glob(os.path.join(cd, "*.html")) for b in PC.parse(f))
    cset = set(ctext.split())
    for f in sorted(glob.glob(os.path.join(gd, "*.html"))):
        for b in PC.parse(f):
            if not b[3].startswith("body") or len(b[1].split()) < 5: continue
            words = b[1].split()
            if b[1][:60] in ctext: continue
            if sum(1 for x in words if x in cset) / len(words) >= 0.9: continue   # present in Claude, reworded
            ws = set(words)
            best, bi, src = 0, -1, ""
            for i in range(len(lines)):
                for s, lab in ((black[i], "black"), (red[i], "red")):
                    if not s: continue
                    sc = len(ws & set(s.split())) / len(ws)
                    if sc > best: best, bi, src = sc, i, lab
            if best < 0.7: continue
            lead = re.match(r"\s*🔴\[RED TEXT\]\s*\[([^\]]*)\]", lines[bi])
            t = re.sub(r"\d+[a-z]?", "N", lead.group(1).lower().strip())[:30] if lead else "(none)"
            k = f"{src:5s} | {b[3].split(':')[0]}:{b[3].split(':')[-1]} | lead [{t}]"
            kind[src] += 1; tagc[k] += 1; mods[k].add(code)
            if len(ex[k]) < 3: ex[k].append(f"{code} {os.path.basename(f)}: {b[2][:70]}")
print("gold body blocks lost from every Claude page but in the WT:", dict(kind))
for k, n in tagc.most_common(30): print(f"{n:4d} {len(mods[k]):3d}m  {k:60s} e.g. {ex[k][0]}")
