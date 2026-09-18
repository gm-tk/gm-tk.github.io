#!/usr/bin/env python3
"""clickDrop BUTTON WRAPPERS: for every `div.button.clickDrop` (first of its group), the two enclosing wrappers (parent › grandparent),
Claude vs gold, pages / modules / per subject. python3 _s26_r394_clickdrop.py"""
import os, sys, re
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
sys.path.insert(0, OUTPUTS)
src = open(os.path.join(OUTPUTS, "_s26_r392_adjul.py"), encoding="utf-8").read()
exec(src[:src.index("ADJ = re.compile")])
from collections import Counter, defaultdict
TAG = re.compile(r"<(/?)([a-z][a-z0-9]*)\b([^>]*)>", re.I)
CLS = re.compile(r'class="([^"]*)"')
VOID = {"br", "img", "input", "hr", "meta", "link", "source", "wbr"}
def scan(s):
    st = []; out = []; lastpar = None
    for m in TAG.finditer(s):
        closing, tag, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID and not closing: continue
        if closing:
            if st: st.pop()
            continue
        c = CLS.search(attrs); cls = " ".join(sorted((c.group(1) if c else "").split()))
        label = tag + (("." + cls.replace(" ", ".")) if cls else "")
        if tag == "div" and "clickDrop" in cls.split() and "button" in cls.split():
            par = " › ".join(e for e in st[-3:])
            if par != lastpar: out.append(par); lastpar = par
        st.append(label)
    return out
C = Counter(); G = Counter(); CP = defaultdict(set); CM = defaultdict(set); GP = defaultdict(set); GS = defaultdict(Counter)
for code in sorted(fam):
    subj = (meta.get(code, {}) or {}).get("subject") or "None"
    for n, cp, hp in pairs(code):
        try:
            ch = body(open(cp, encoding="utf-8", errors="replace").read()); gh = body(open(hp, encoding="utf-8", errors="replace").read())
        except Exception: continue
        for k in scan(ch): C[k] += 1; CP[k].add(cp); CM[k].add(code)
        for k in scan(gh): G[k] += 1; GP[k].add(hp); GS[k][subj] += 1
print("==== clickDrop button groups: the three enclosing wrappers (…grandparent › parent) ====")
print("Claude:"); [print(f"   {n:4d} (pages {len(CP[k]):3d} / mods {len(CM[k]):3d})  {k}") for k, n in C.most_common(8)]
print("gold:"); [print(f"   {n:4d} (pages {len(GP[k]):3d})  {k}   {GS[k].most_common(3)}") for k, n in G.most_common(12)]
print("gold groups total", sum(G.values()), "claude", sum(C.values()))
PC = Counter(); PG = Counter(); PGS = defaultdict(Counter)
for k, n in G.items():
    p = k.split(" › ")[-1]; key = "col" if p.startswith("div.col") else p; PG[key] += n
    for sj, c in GS[k].items(): PGS[sj][key] += c
for k, n in C.items():
    p = k.split(" › ")[-1]; PC["col" if p.startswith("div.col") else p] += n
print("gold parent kinds:", PG.most_common(8)); print("claude parent kinds:", PC.most_common(6))
print("gold by subject (parent kind):"); [print("   ", sj, dict(c)) for sj, c in sorted(PGS.items(), key=lambda x: -sum(x[1].values()))[:12]]
