#!/usr/bin/env python3
"""Session 44 Round 3 — _s44_r3_actgold.py corrected: a title counts as BOXED only when EVERY heading occurrence of it on the gold
pages sits inside div.activity (the first version counted any one boxed occurrence). WSL: python3 _s44_r3_actgold2.py _s44_r3_acttables.log"""
import sys, collections, io
sys.argv = sys.argv[:2]
exec(open("_s44_r3_actgold.py", encoding="utf-8").read().split("res = collections.defaultdict")[0])
res = collections.defaultdict(collections.Counter)
for ln in io.open(sys.argv[1], encoding="utf-8"):
    if not ln.startswith("TSV\t"): continue
    _, code, reo, eng, nk = ln.rstrip("\n").split("\t")
    hits = []
    for t in (reo, eng):
        n = norm(t)
        if len(n) < 2: continue
        for tag, tx, st in blocks(code):
            if tx == n and tag[0] == "h":
                hits.append("activity" if any(re.search(r"\bactivity\b", c) for _, c in st) else "free")
    w = "absent" if not hits else ("activity" if all(h == "activity" for h in hits) else ("free" if all(h == "free" for h in hits) else "mixed"))
    res[code][w] += 1
for code, c in sorted(res.items()): print(code, dict(c))
