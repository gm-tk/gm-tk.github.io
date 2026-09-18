#!/usr/bin/env python3
"""BOLD INSIDE A TABLE HEADER CELL: `<th>` cells whose content is wrapped in <b>/<strong> — gold vs Claude, live body, per group;
also <td> cells that are entirely bold (a writer's bold header row Claude keeps as td). python3 _s26_r397_thb.py"""
import os, sys, re
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
sys.path.insert(0, OUTPUTS)
src = open(os.path.join(OUTPUTS, "_s26_r392_adjul.py"), encoding="utf-8").read()
exec(src[:src.index("ADJ = re.compile")])
from collections import Counter, defaultdict
TH = re.compile(r"<th\b[^>]*>(.*?)</th>", re.S)
def thb(cell):
    c = cell.strip()
    c = re.sub(r"^<p\b[^>]*>|</p>$", "", c).strip()
    return bool(re.match(r"^<(b|strong)\b[^>]*>.*</\1>$", c, re.S))
G = defaultdict(Counter); C = defaultdict(Counter); CP = defaultdict(set); CM = defaultdict(set); GP = defaultdict(set)
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"
    keys = ("ALL", f"template={tf}", f"tmpl+subj={tf}/{subj}")
    for n, cp, hp in pairs(code):
        try:
            ch = body(open(cp, encoding="utf-8", errors="replace").read()); gh = body(open(hp, encoding="utf-8", errors="replace").read())
        except Exception: continue
        cl = "".join(live_pieces(ch)); gl = "".join(live_pieces(gh))
        for k in keys:
            for cell in TH.findall(gl): G[k]["th"] += 1; G[k]["th>b"] += thb(cell)
            for cell in TH.findall(cl):
                C[k]["th"] += 1
                if thb(cell): C[k]["th>b"] += 1; CP[k].add(cp); CM[k].add(code)
        if any(thb(c) for c in TH.findall(gl)): GP[keys[0]].add(hp); GP[keys[2]].add(hp)
print("==== <th> cells wholly wrapped in <b>: gold vs Claude ====")
for k in sorted(G, key=lambda x: (not x.startswith("ALL"), not x.startswith("template"), -C[x]["th>b"])):
    if G[k]["th"] + C[k]["th"] < 20: continue
    print(f"   {k:46s} gold th {G[k]['th']:5d} bold {G[k]['th>b']:4d} ({G[k]['th>b']/max(1,G[k]['th']):.2f}; pages {len(GP.get(k, set())):3d})   claude th {C[k]['th']:5d} bold {C[k]['th>b']:4d} ({C[k]['th>b']/max(1,C[k]['th']):.2f}; pages {len(CP.get(k, set())):3d} / mods {len(CM.get(k, set())):3d})")
