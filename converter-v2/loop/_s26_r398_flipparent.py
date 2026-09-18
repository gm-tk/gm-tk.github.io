#!/usr/bin/env python3
"""FLIP-CARD GROUP'S PARENT COLUMN by card count: for every flipCardsContainer, its parent column class (col-md-8 / col-12 /
col-md-12 …) × the number of cards, gold vs Claude, per subject. python3 _s26_r398_flipparent.py"""
import os, sys, re
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
sys.path.insert(0, OUTPUTS)
src = open(os.path.join(OUTPUTS, "_s26_r392_adjul.py"), encoding="utf-8").read()
exec(src[:src.index("ADJ = re.compile")])
from collections import Counter, defaultdict
TAG = re.compile(r"<(/?)([a-z][a-z0-9]*)\b([^>]*)>", re.I)
CLS = re.compile(r'class="([^"]*)"')
VOID = {"br", "img", "input", "hr", "meta", "link", "source", "wbr"}
def groups(s):
    st = []; out = []
    for m in TAG.finditer(s):
        closing, tag, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID and not closing: continue
        if closing:
            if st:
                e = st.pop()
                if e[1] is not None: out.append((e[2], e[1]))
            continue
        c = CLS.search(attrs); toks = (c.group(1) if c else "").split(); cls = " ".join(sorted(toks))
        rec = None; par = ""
        if tag == "div" and "flipCardsContainer" in toks:
            rec = 0; par = st[-1][0] if st else ""
        elif st and st[-1][1] is not None and tag == "div" and any(t.startswith("col") for t in toks):
            st[-1][1] += 1
        st.append([cls, rec, par])
    return out
G = defaultdict(Counter); C = defaultdict(Counter); GP = defaultdict(set); CP = defaultdict(set); CM = defaultdict(set)
def bucket(n): return "1" if n == 1 else "2" if n == 2 else "3" if n == 3 else "4" if n == 4 else "5-6" if n <= 6 else "7-9" if n <= 9 else "10+"
for code in sorted(fam):
    subj = (meta.get(code, {}) or {}).get("subject") or "None"
    for n, cp, hp in pairs(code):
        try:
            ch = body(open(cp, encoding="utf-8", errors="replace").read()); gh = body(open(hp, encoding="utf-8", errors="replace").read())
        except Exception: continue
        for par, k in groups(gh):
            p = "col-md-12" if "col-md-12" in par.split() else "col-md-8" if "col-md-8" in par.split() else "col-12" if par == "col-12" else "other:" + par[:24]
            G[bucket(k)][p] += 1; GP[(bucket(k), p)].add(hp)
        for par, k in groups(ch):
            p = "col-md-12" if "col-md-12" in par.split() else "col-md-8" if "col-md-8" in par.split() else "col-12" if par == "col-12" else "other:" + par[:24]
            C[bucket(k)][p] += 1; CP[(bucket(k), p)].add(cp); CM[(bucket(k), p)].add(code)
print("==== the flip group's PARENT column by card count — gold vs Claude ====")
for b in ("1", "2", "3", "4", "5-6", "7-9", "10+"):
    tg = sum(G[b].values()); tc = sum(C[b].values())
    print(f"   cards {b:4s} gold n={tg:3d} " + ", ".join(f"{p} {n} ({n/tg:.2f}; pages {len(GP[(b, p)])})" for p, n in G[b].most_common(4)))
    print(f"   {'':9s} claude n={tc:3d} " + ", ".join(f"{p} {n} (pages {len(CP[(b, p)])} / mods {len(CM[(b, p)])})" for p, n in C[b].most_common(4)))
