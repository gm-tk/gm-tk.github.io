#!/usr/bin/env python3
"""SPEECH BUBBLES: per page, speechBubble rows vs bubble divs, and how many bubbles each row holds (gold vs Claude); adjacent
speechBubble rows (nothing but whitespace between). python3 _s26_r397_bubbles.py"""
import os, sys, re
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
sys.path.insert(0, OUTPUTS)
src = open(os.path.join(OUTPUTS, "_s26_r396_widgetwrap.py"), encoding="utf-8").read()
exec(src[:src.index("ROOTS = ")])
from collections import Counter, defaultdict
TAG = re.compile(r"<(/?)([a-z][a-z0-9]*)\b([^>]*)>", re.I)
CLS = re.compile(r'class="([^"]*)"')
VOID = {"br", "img", "input", "hr", "meta", "link", "source", "wbr"}
def rows(s):
    """yield per speechBubble row: (layout attr, [bubble classes], col class)."""
    st = []; out = []
    for m in TAG.finditer(s):
        closing, tag, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID and not closing: continue
        if closing:
            if st:
                e = st.pop()
                if e[1] is not None: out.append(e[1])
            continue
        c = CLS.search(attrs); toks = (c.group(1) if c else "").split()
        rec = None
        if tag == "div" and "speechBubble" in toks and "row" in toks:
            lay = re.search(r'layout="([^"]*)"', attrs); rec = {"layout": lay.group(1) if lay else "-", "bubbles": [], "cols": []}
        else:
            par = next((e for e in reversed(st) if e[1] is not None), None)
            if par is not None:
                if any(t.startswith("bubble-") for t in toks): par[1]["bubbles"].append(" ".join(sorted(t for t in toks if t.startswith("bubble-") or t in ("secondary", "no-hover"))))
                elif any(t.startswith("col") for t in toks) and len(st) - st.index(par) == 1: par[1]["cols"].append(" ".join(sorted(toks)))
        st.append((tag, rec))
    return out
ADJ = re.compile(r'</div>\s*<div class="row speechBubble"')
G = Counter(); C = Counter(); GL = Counter(); CL = Counter(); GA = 0; CA = 0; GP = set(); CP = set(); CM = set(); GB = Counter(); CB = Counter(); GS = defaultdict(Counter); CS = defaultdict(Counter)
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"
    for n, cp, hp in pairs(code):
        try:
            ch = body(open(cp, encoding="utf-8", errors="replace").read()); gh = body(open(hp, encoding="utf-8", errors="replace").read())
        except Exception: continue
        gr = rows(gh); cr = rows(ch)
        for r in gr: G[min(len(r["bubbles"]), 6)] += 1; GL[r["layout"]] += 1; GB[tuple(sorted(set(r["bubbles"])))[:2]] += 1; GS[f"{tf}/{subj}"][min(len(r["bubbles"]), 6)] += 1
        for r in cr: C[min(len(r["bubbles"]), 6)] += 1; CL[r["layout"]] += 1; CB[tuple(sorted(set(r["bubbles"])))[:2]] += 1; CS[f"{tf}/{subj}"][min(len(r["bubbles"]), 6)] += 1
        ga = len(ADJ.findall(gh)); ca = len(ADJ.findall(ch)); GA += ga; CA += ca
        if gr: GP.add(hp)
        if cr: CP.add(cp); CM.add(code)
print(f"speechBubble rows: gold {sum(G.values())} on {len(GP)} pages; claude {sum(C.values())} on {len(CP)} pages / {len(CM)} modules")
print("bubbles per row (6 = 6+):  gold", sorted(G.items()), "  claude", sorted(C.items()))
print("layout attr:  gold", GL.most_common(5), "  claude", CL.most_common(5))
print(f"ADJACENT speechBubble rows (whitespace only between): gold {GA}  claude {CA}")
print("bubble class sets — gold:", GB.most_common(6)); print("bubble class sets — claude:", CB.most_common(6))
print("per group, bubbles-per-row (gold | claude):")
for k in sorted(set(GS) | set(CS), key=lambda x: -(sum(GS[x].values()) + sum(CS[x].values())))[:10]:
    print(f"   {k:40s} gold {sorted(GS[k].items())}   claude {sorted(CS[k].items())}")
