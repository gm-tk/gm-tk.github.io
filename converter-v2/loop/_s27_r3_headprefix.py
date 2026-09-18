#!/usr/bin/env python3
"""r399+ — the writer-heading census (_s23_headcensus.json, re-run on the r399 corpus) cut by PREFIX × digit for the FREE-BODY
parents (col-md-8 / col-12 / paddingR): where the gold keeps (or shifts to) a level ≥ 0.60 and Claude disagrees — the
r371–r375 registry's remaining candidates, with pages. wsl: python3 _s27_r3_headprefix.py"""
import json, re
from collections import Counter, defaultdict
rows = json.load(open("_s23_headcensus.json"))
FREE = re.compile(r"^div\.col-12(\.col-md-(8|12))?(\.paddingR)?$")
def prefix(code):
    m = re.match(r"^([A-Z]+)(\d)", code); return (m.group(1) + (m.group(2) if m.group(1) in ("BLL", "HIS", "PES", "AGH", "ANZH", "HES", "PHE", "ENG") else "")) if m else code
by = defaultdict(lambda: defaultdict(Counter)); pages = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))
for r in rows:
    if not FREE.match(r["gold_parent"] or ""): continue
    p = prefix(r["module"]); d = r["wt"]
    by[d][p][(r["gold"], r["claude"])] += 1
    pages[d][p][(r["gold"], r["claude"])].add(r["page"])
for d in ("H2", "H4", "H5", "H1"):
    print(f"== {d} (free-body parents) ==")
    for p, c in sorted(by[d].items(), key=lambda kv: -sum(kv[1].values())):
        t = sum(c.values())
        if t < 8: continue
        gold = Counter(); cl = Counter(); agree = 0
        for (g, k), v in c.items():
            gold[g] += v; cl[k] += v
            if g == k: agree += v
        gtop, gn = gold.most_common(1)[0]
        # pages where claude != gold's top level but gold == top
        wrong_pages = set()
        for (g, k), s in pages[d][p].items():
            if g == gtop and k != gtop: wrong_pages |= s
        flag = "  <<<" if gn / t >= 0.60 and (cl[gtop] / t) < 0.6 and len(wrong_pages) >= 8 else ""
        print(f"   {p:8s} n={t:4d} agree {agree/t:.2f}  gold {gtop} {gn/t:.2f}  claude {gtop} {cl[gtop]/t:.2f}  | gold " + " ".join(f"{g}={v}" for g, v in gold.most_common(3)) + " | claude " + " ".join(f"{k}={v}" for k, v in cl.most_common(3)) + f" | pages-wrong {len(wrong_pages)}{flag}")
