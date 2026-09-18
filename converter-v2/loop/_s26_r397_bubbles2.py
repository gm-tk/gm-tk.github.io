#!/usr/bin/env python3
"""SPEECH BUBBLE FORM vs IMAGE: per speechBubble row — the bubble's tail class (top / right / left / none) × whether the row
holds an <img> (a character image) × the column layout, gold vs Claude, per subject. python3 _s26_r397_bubbles2.py"""
import os, sys, re
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
sys.path.insert(0, OUTPUTS)
src = open(os.path.join(OUTPUTS, "_s26_r396_widgetwrap.py"), encoding="utf-8").read()
exec(src[:src.index("ROOTS = ")])
from collections import Counter, defaultdict
ROW = re.compile(r'<div class="row speechBubble"[^>]*>')
def rows(s):
    out = []
    for m in ROW.finditer(s):
        i = m.end(); depth = 1; j = i
        for mm in re.finditer(r"<div\b|</div>", s[i:]):
            depth += 1 if mm.group(0) == "<div" else -1
            if depth == 0: j = i + mm.start(); break
        inner = s[i:j]
        tails = re.findall(r'class="([^"]*bubble-[^"]*)"', inner)
        tail = "none"
        for t in tails:
            toks = t.split()
            if "bubble-top" in toks: tail = "top"; break
            if "bubble-right" in toks: tail = "right"; break
            if "bubble-left" in toks: tail = "left"; break
            if "bubble-basic" in toks: tail = "basic"
        cols = re.findall(r'<div class="(col[^"]*)"', inner)
        lay = re.search(r'layout="([^"]*)"', m.group(0))
        out.append((tail, "img" if "<img" in inner else "no-img", lay.group(1) if lay else "-", " | ".join(cols[:2])))
    return out
G = Counter(); C = Counter(); GS = defaultdict(Counter); CS = defaultdict(Counter); CP = defaultdict(set); CM = defaultdict(set); GCOL = Counter(); CCOL = Counter()
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"
    for n, cp, hp in pairs(code):
        try:
            ch = body(open(cp, encoding="utf-8", errors="replace").read()); gh = body(open(hp, encoding="utf-8", errors="replace").read())
        except Exception: continue
        for t, im, lay, cols in rows(gh): G[(t, im, lay)] += 1; GS[f"{tf}/{subj}"][(t, im, lay)] += 1; GCOL[(im, cols)] += 1
        for t, im, lay, cols in rows(ch): C[(t, im, lay)] += 1; CS[f"{tf}/{subj}"][(t, im, lay)] += 1; CP[(t, im, lay)].add(cp); CM[(t, im, lay)].add(code); CCOL[(im, cols)] += 1
print("==== speechBubble rows: (tail, image?, layout) — gold vs Claude ====")
for k in sorted(set(G) | set(C), key=lambda x: -(G[x] + C[x]))[:12]:
    print(f"   gold {G[k]:4d}   claude {C[k]:4d} (pages {len(CP[k]):3d} / mods {len(CM[k]):3d})   {k}")
print("column layouts — gold:", GCOL.most_common(6)); print("column layouts — claude:", CCOL.most_common(6))
print("per group (top-6 keys):")
for g in sorted(set(GS) | set(CS), key=lambda x: -(sum(GS[x].values()) + sum(CS[x].values())))[:8]:
    print(f"   {g:36s} gold {GS[g].most_common(4)}\n   {'':36s} claude {CS[g].most_common(3)}")
