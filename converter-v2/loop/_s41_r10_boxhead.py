#!/usr/bin/env python3
"""Session 41 Round 10 PICK — the FIRST heading level inside each activity box (div.activity* > div.row > div.col-*), gold vs Claude,
per family (letters of the module code) and per template dir, over the gate's pairs; plus whether the box carries `interactive`.
Run under WSL from CONVERTER_V2/reference/tests."""
import os, re, sys, collections
sys.path.insert(0, os.getcwd())
import _discrepancy_audit as DA, _corpus
from _skeleton_compare import _skel
from anchor_compare import CLAUDE
def boxes(sk):
    out = []
    for i, l in enumerate(sk):
        s = l.strip()
        if s.startswith("div.activity"):
            ind = len(l) - len(l.lstrip()); inter = ".interactive" in s; head = None
            for m in sk[i + 1:i + 12]:
                if len(m) - len(m.lstrip()) <= ind: break
                t = m.strip()
                if re.fullmatch(r"h[1-6]", t): head = t; break
            out.append((head, inter))
    return out
fam = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list)
for code in sorted(_corpus.gate_mods(CLAUDE)):
    f = re.match(r"[A-Z]+", code).group(0)
    for _, cp, hp in DA.pairs(code):
        g = boxes(_skel(hp, True)); c = boxes(_skel(cp, True))
        for (gh, gi), (ch, ci) in zip(g, c):
            fam[f][f"gold {gh} / claude {ch}"] += 1
            fam[f][f"interactive gold {gi} / claude {ci}"] += 1
tot = collections.Counter()
for f, c in sorted(fam.items(), key=lambda x: -sum(v for k, v in x[1].items() if k.startswith("gold"))):
    n = sum(v for k, v in c.items() if k.startswith("gold"))
    if n < 15: continue
    heads = {k: v for k, v in c.items() if k.startswith("gold")}
    mism = sum(v for k, v in heads.items() if k.split(" / ")[0][5:] != k.split(" / ")[1][7:])
    inter = {k: v for k, v in c.items() if k.startswith("interactive")}
    print(f"{f:7s} boxes {n:5d}  heading-mismatch {mism:4d}  " + ", ".join(f"{k} {v}" for k, v in sorted(heads.items(), key=lambda x: -x[1])[:4]) + "  | " + ", ".join(f"{k[12:]} {v}" for k, v in sorted(inter.items(), key=lambda x: -x[1])[:3]))
    for k, v in heads.items(): tot[k] += v
print("\nALL:", tot.most_common(12))
