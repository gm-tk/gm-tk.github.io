#!/usr/bin/env python3
"""_s51_r7_sidegold.py — session 51 Round 7 PICK: after every Claude activity-sidebar side column (col-md-4 > alertActivity), the
next row's first text block — where the GOLD puts that text (census parser, jacc >= 0.6): inside an activity (the RHS box cut
the writer's activity short) or free. WSL, from reference/tests/."""
import os, re, sys, collections
sys.path.insert(0, os.getcwd()); sys.path.append("../../outputs")
import _corpus
import _placement_census as PC
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE
SIDE = re.compile(r'<div class="[^"]*\bcol-md-4\b[^"]*">\s*<div class="alertActivity[^"]*"', re.I)
ROW = re.compile(r'<div class="row[^"]*">', re.I)
strip = lambda h: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip()
fold = lambda t: " ".join(re.sub(r"[^a-z0-9 ]", " ", t.lower()).split())
res = collections.Counter(); fam = collections.defaultdict(collections.Counter); ex = []
for code in sorted(_corpus.gate_mods(CLAUDE)):
    for n, cp, hp in pairs(code):
        html = open(cp, encoding="utf-8", errors="replace").read()
        ms = list(SIDE.finditer(html))
        if not ms: continue
        g = None
        for m in ms:
            nx = ROW.search(html, m.end())
            if not nx: continue
            seg = html[nx.start(): nx.start() + 4000]
            if re.match(r'<div class="row[^"]*">\s*<div class="[^"]*">\s*<div class="activity', seg): continue   # a new box follows: not this lane
            b = re.search(r"<(p|h[2-5]|li)\b[^>]*>(.*?)</\1>", seg, re.S)
            if not b: continue
            t = fold(strip(b.group(2)))
            if len(t.split()) < 4: continue
            if g is None: g = PC.parse(hp)
            best = max(g, key=lambda x: PC.jacc(x[1], t), default=None)
            where = best[3] if best and PC.jacc(best[1], t) >= 0.6 else "—"
            k = "activity" if "activity" in where else ("free" if re.search(r"(^|:)free", where) else where)
            res[k] += 1; fam[re.sub(r"\d.*$", "", code)][k] += 1
            if k == "activity" and len(ex) < 12: ex.append(f"{os.path.basename(cp)}: {strip(b.group(2))[:60]}")
print("after an activity sidebar, the next free row's first text — gold:", dict(res.most_common(6)))
for f, c in sorted(fam.items(), key=lambda kv: -kv[1]["activity"])[:15]: print(f"  {f:8s} {dict(c.most_common(4))}")
print("\n".join(ex))
