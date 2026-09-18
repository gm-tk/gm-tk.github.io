#!/usr/bin/env python3
"""THE GOLD'S INNER ROW INSIDE AN ACTIVITY BOX: `div.activity* › div.row › div.col-12 › div.row › div.col-12` — what starts the
inner row (its col-12's first child) and what precedes it (the previous sibling in the outer col-12); per subject; Claude's count.
python3 _s26_r398_actrow.py"""
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
    st = []; out = []
    for m in TAG.finditer(s):
        closing, tag, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID and not closing:
            if st: st[-1][1].append(tag)
            continue
        if closing:
            if st:
                e = st.pop()
                if e[2] is not None: out.append(e[2] + (e[1][0] if e[1] else "(empty)",))
            continue
        c = CLS.search(attrs); toks = (c.group(1) if c else "").split(); cls = " ".join(sorted(toks))
        label = tag + (("." + cls.replace(" ", ".")) if cls else "")
        rec = None
        if tag == "div" and toks == ["col-12"] and len(st) >= 4 and st[-1][0] == "div.row" and st[-2][0] == "div.col-12" and st[-3][0] == "div.row" and st[-4][0].startswith("div.activity"):
            prev = st[-2][1][-1] if st[-2][1] else "(first)"   # the outer col-12's previous child = the inner row itself was appended already? no: appended below
            rec = (st[-4][0][:30], prev)
        if st: st[-1][1].append(label)
        st.append([label, [], rec])
    return out
G = Counter(); PREV = Counter(); FIRST = Counter(); GS = Counter(); GP = set(); N = 0; CN = 0; CP = set()
for code in sorted(fam):
    subj = (meta.get(code, {}) or {}).get("subject") or "None"
    for n, cp, hp in pairs(code):
        try:
            ch = body(open(cp, encoding="utf-8", errors="replace").read()); gh = body(open(hp, encoding="utf-8", errors="replace").read())
        except Exception: continue
        for act, prev, first in scan(gh):
            N += 1; G[act] += 1; PREV[prev] += 1; FIRST[first] += 1; GS[subj] += 1; GP.add(hp)
        for act, prev, first in scan(ch): CN += 1; CP.add(cp)
print(f"gold inner row›col-12 inside an activity's col-12: {N} on {len(GP)} pages;  claude {CN} on {len(CP)} pages")
print("activity kind:", G.most_common(5))
print("previous sibling in the outer col-12 (before the inner row):", PREV.most_common(10))
print("inner col-12's first child:", FIRST.most_common(10))
print("by subject:", GS.most_common(8))
