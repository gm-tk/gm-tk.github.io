#!/usr/bin/env python3
"""The gold's plain `row › row`: the full div-ancestor chain (classes) up to #body, the inner row's position among the outer
row's direct children, the previous sibling, and the inner row's first child. python3 _s26_r393_rowchain.py"""
import os, sys, re
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
sys.path.insert(0, OUTPUTS)
src = open(os.path.join(OUTPUTS, "_s26_r392_adjul.py"), encoding="utf-8").read()
exec(src[:src.index("ADJ = re.compile")])
from collections import Counter, defaultdict
TAG = re.compile(r"<(/?)([a-z][a-z0-9]*)\b([^>]*)>", re.I)
CLS = re.compile(r'class="([^"]*)"'); ID = re.compile(r'id="([^"]*)"')
VOID = {"br", "img", "input", "hr", "meta", "link", "source", "wbr"}
def walk(s):
    """yield (chain, prev_sibling_label, first_child_label, idx_among_children, outer_text_before) for each plain row>row."""
    st = []  # entries: [label, children_labels]
    out = []
    for m in TAG.finditer(s):
        closing, tag, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID and not closing:
            if st: st[-1][1].append(tag)
            continue
        if closing:
            if st:
                ent = st.pop()
                if ent[2] is not None: out.append(ent[2] + (tuple(ent[1][:1]),))
            continue
        c = CLS.search(attrs); cls = c.group(1).strip() if c else ""; i = ID.search(attrs)
        label = tag + ("#" + i.group(1) if i else "") + (("." + ".".join(cls.split())) if cls else "")
        rec = None
        if tag == "div" and "row" in cls.split() and st:
            par = st[-1]
            if par[0] == "div.row" and label == "div.row":
                chain = " > ".join(e[0] for e in st[-4:])
                rec = (chain, par[1][-1] if par[1] else "(first)", len(par[1]))
        if st: st[-1][1].append(label)
        st.append([label, [], rec])
    return out
CH = Counter(); PREV = Counter(); FIRST = Counter(); IDX = Counter(); BYS = Counter(); N = 0
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"
    for n, cp, hp in pairs(code):
        try: gh = body(open(hp, encoding="utf-8", errors="replace").read())
        except Exception: continue
        gl = "".join(live_pieces(gh))
        for chain, prev, idx, first in walk(gl):
            N += 1; CH[chain] += 1; PREV[prev] += 1; FIRST[first[0] if first else "(empty)"] += 1; IDX["first child" if idx == 0 else "later"] += 1; BYS[f"{tf}/{subj}"] += 1
print("gold plain row>row:", N)
print("chains:"); [print(f"   {n:5d}  {k}") for k, n in CH.most_common(8)]
print("previous sibling of the inner row:", PREV.most_common(8))
print("inner row's first child:", FIRST.most_common(8))
print("position:", IDX.most_common())
print("by group:", BYS.most_common(10))
