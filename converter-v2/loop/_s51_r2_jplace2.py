#!/usr/bin/env python3
"""_s51_r2_jplace2.py — session 51 Round 2 PICK: the learner's JOURNAL instruction naming an activity id ("Go to your
learning journal and complete 3A.", "Complete activity 4A in your journal.") — every such block on the paired pages, gold
and Claude, by container path (the §1g census parser). Per family: the gold's placement share (activity box vs anything
else) and Claude's. WSL, from reference/tests/. Writes outputs/_s51_r2_jplace2.tsv (one row per gold block)."""
import os, re, sys, collections
sys.path.insert(0, os.getcwd()); sys.path.append("../../outputs")
import _corpus
import _placement_census as PC
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE

J = re.compile(r"journal", re.I)
ID = re.compile(r"\b\d{1,2}[A-Za-z]\b")
GO = re.compile(r"\b(complete|go to|do)\b", re.I)
isj = lambda t: bool(J.search(t) and ID.search(t) and GO.search(t) and len(t.split()) <= 30)
kind = lambda r: "activity" if r.endswith(":activity") or r == "body:activity" else r
G = collections.defaultdict(collections.Counter); C = collections.defaultdict(collections.Counter)
rows = []
for code in sorted(_corpus.gate_mods(CLAUDE)):
    f = re.sub(r"\d.*$", "", code)
    for n, cp, hp in pairs(code):
        gb = [b for b in PC.parse(hp) if isj(b[2])]
        cb = [b for b in PC.parse(cp) if isj(b[2])]
        for b in gb:
            G[f][kind(b[3])] += 1
            m = [c for c in cb if PC.jacc(c[1], b[1]) >= 0.5]
            rows.append((code, os.path.basename(cp), kind(b[3]), kind(m[0][3]) if m else "—", b[2][:80]))
        for b in cb: C[f][kind(b[3])] += 1
tot = collections.Counter()
print("family: gold placements || claude placements")
for f in sorted(G, key=lambda f: -sum(G[f].values())):
    g = G[f]; n = sum(g.values()); act = g["activity"]; tot["gold"] += n; tot["gold_act"] += act
    print(f"{f:8s} gold n={n:3d} activity {act / n:4.2f} {dict(g.most_common(3))} || claude {dict(C[f].most_common(3))}")
print("TOTAL gold blocks", tot["gold"], "in activity", tot["gold_act"])
with open("../../outputs/_s51_r2_jplace2.tsv", "w") as fh:
    for r in rows: fh.write("\t".join(r) + "\n")
