#!/usr/bin/env python3
"""ROW DIRECTLY INSIDE THE TEXT COLUMN: `div.col-12.col-md-8 > div.row` (Claude) / `div.col-md-8.col-12 > div.row` (gold) — the
inner row's own class and its first child's class, Claude vs gold, corpus-wide (live body). python3 _s26_r398_colrow12.py"""
import os, sys, re
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
sys.path.insert(0, OUTPUTS)
src = open(os.path.join(OUTPUTS, "_s26_r392_adjul.py"), encoding="utf-8").read()
exec(src[:src.index("ADJ = re.compile")])
from collections import Counter, defaultdict
TAG = re.compile(r"<(/?)([a-z][a-z0-9]*)\b([^>]*)>", re.I)
CLS = re.compile(r'class="([^"]*)"')
VOID = {"br", "img", "input", "hr", "meta", "link", "source", "wbr"}
def col8(cls): t = set(cls.split()); return t == {"col-12"}
def scan(s):
    st = []; out = []
    for m in TAG.finditer(s):
        closing, tag, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID and not closing:
            if st and st[-1][2] is None: st[-1][2] = tag
            continue
        if closing:
            if st:
                e = st.pop()
                if e[3]: out.append((e[1], e[2] or "(empty)"))
            continue
        c = CLS.search(attrs); cls = " ".join(sorted((c.group(1) if c else "").split()))
        label = tag + (("." + cls.replace(" ", ".")) if cls else "")
        if st and st[-1][2] is None: st[-1][2] = label
        isinner = tag == "div" and "row" in cls.split() and st and st[-1][0] == "div" and col8(st[-1][1].split(".", 1)[1].replace(".", " ") if "." in st[-1][1] else "")
        st.append([tag, label, None, bool(isinner)])
    return out
C = Counter(); G = Counter(); CP = defaultdict(set); CM = defaultdict(set); GP = defaultdict(set)
for code in sorted(fam):
    for n, cp, hp in pairs(code):
        try:
            ch = body(open(cp, encoding="utf-8", errors="replace").read()); gh = body(open(hp, encoding="utf-8", errors="replace").read())
        except Exception: continue
        for k in scan("".join(live_pieces(ch))): C[k] += 1; CP[k].add(cp); CM[k].add(code)
        for k in scan("".join(live_pieces(gh))): G[k] += 1; GP[k].add(hp)
print("==== a div.row DIRECTLY inside the activity box col-12 column: (inner row's class, its first child) ====")
print("Claude:"); [print(f"   {n:4d} (pages {len(CP[k]):3d} / mods {len(CM[k]):3d})  {k[0]}  ›  {k[1]}") for k, n in C.most_common(14)]
print("gold:"); [print(f"   {n:4d} (pages {len(GP[k]):3d})  {k[0]}  ›  {k[1]}") for k, n in G.most_common(14)]
