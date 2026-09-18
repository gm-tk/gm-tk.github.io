#!/usr/bin/env python3
"""What decides the gold's `item video`? For every gold carousel item containing a videoSection: its class vs its other content
(a heading h4/h5, a paragraph, a carousel-caption, an image). python3 _s26_r396_itemvideo2.py"""
import os, sys, re
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
sys.path.insert(0, OUTPUTS)
src = open(os.path.join(OUTPUTS, "_s26_r396_widgetwrap.py"), encoding="utf-8").read()
exec(src[:src.index("ROOTS = ")])
from collections import Counter, defaultdict
ITEM = re.compile(r'<div class="(item(?: video)?|video item)">(.*?)(?=<div class="(?:item(?: video)?|video item)">|</div>\s*</div>\s*</div>)', re.S)
def shape(inner):
    t = []
    if re.search(r"<h[1-6]\b", inner): t.append("heading")
    if re.search(r"<p\b(?![^>]*carousel-caption)", inner): t.append("p")
    if "carousel-caption" in inner: t.append("caption")
    if "<img" in inner: t.append("img")
    if "<table" in inner: t.append("table")
    return "+".join(t) or "video-only"
G = defaultdict(Counter); C = defaultdict(Counter); GS = defaultdict(lambda: defaultdict(Counter))
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"
    for n, cp, hp in pairs(code):
        try:
            ch = body(open(cp, encoding="utf-8", errors="replace").read()); gh = body(open(hp, encoding="utf-8", errors="replace").read())
        except Exception: continue
        for side, s, D in (("gold", gh, G), ("claude", ch, C)):
            for m in ITEM.finditer(s):
                inner = m.group(2)
                if "videoSection" not in inner: continue
                sh = shape(inner); lab = "item video" if "video" in m.group(1) else "item"
                D[sh][lab] += 1
                if side == "gold": GS[sh][f"{tf}/{subj}"][lab] += 1
print("==== gold: video-carrying items by their OTHER content → class ====")
for sh in sorted(G, key=lambda x: -sum(G[x].values())):
    t = sum(G[sh].values()); v = G[sh]["item video"]
    print(f"   {sh:26s} gold n={t:4d}  item video {v:4d} ({v/t:.2f})   claude n={sum(C[sh].values()):4d} item video {C[sh]['item video']:4d}")
    for g, c in sorted(GS[sh].items(), key=lambda x: -sum(x[1].values()))[:6]:
        tt = sum(c.values())
        if tt >= 15: print(f"        {g:40s} n={tt:4d} item video {c['item video']:4d} ({c['item video']/tt:.2f})")
