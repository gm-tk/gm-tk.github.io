#!/usr/bin/env python3
"""The gold's row-in-row: which parent (its full class) holds a direct child div.row, per subject; examples. python3 _s26_r393_rowrow_gold.py"""
import os, sys, re
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
sys.path.insert(0, OUTPUTS)
src = open(os.path.join(OUTPUTS, "_s26_r392_adjul.py"), encoding="utf-8").read()
exec(src[:src.index("ADJ = re.compile")])
from collections import Counter, defaultdict
TAG = re.compile(r"<(/?)div\b([^>]*)>", re.I)
CLS = re.compile(r'class="([^"]*)"')
def pairs_of(s):
    st = []; out = []
    for m in TAG.finditer(s):
        if m.group(1):
            if st: st.pop()
            continue
        c = CLS.search(m.group(2)); cls = c.group(1).strip() if c else ""
        toks = cls.split()
        if "row" in toks and st and "row" in st[-1][0].split():
            out.append((st[-1][0], cls, re.sub(r"\s+", " ", s[m.start():m.start()+220])))
        st.append((cls, m.start()))
    return out
G = Counter(); C = Counter(); GS = defaultdict(Counter); EX = {}
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"
    for n, cp, hp in pairs(code):
        try:
            ch = body(open(cp, encoding="utf-8", errors="replace").read()); gh = body(open(hp, encoding="utf-8", errors="replace").read())
        except Exception:
            continue
        cl = "".join(live_pieces(ch)); gl = "".join(live_pieces(gh))
        for par, cls, ctx in pairs_of(gl):
            k = (par, cls); G[k] += 1; GS[k][subj] += 1
            if k not in EX: EX[k] = f"{os.path.basename(hp)}: {ctx[:200]}"
        for par, cls, ctx in pairs_of(cl):
            C[(par, cls)] += 1
print("==== gold row-in-row by (parent class, child class) ====")
for k, n in G.most_common(12):
    print(f"   {n:5d}  parent «{k[0]}» › child «{k[1]}»  claude {C.get(k, 0)}  subjects {GS[k].most_common(4)}")
    print("          ", EX[k][:220])
print("==== Claude row-in-row by (parent, child) ====")
for k, n in C.most_common(6): print(f"   {n:5d}  parent «{k[0]}» › child «{k[1]}»  gold {G.get(k, 0)}")
