#!/usr/bin/env python3
"""FLIP-CARD COLUMN WIDTH: for every `div.flipCardsContainer` (gold and Claude), the number of direct child columns and their
class → (n cards → column class) tables, per subject; plus the container's own class variants. python3 _s26_r395_flipcols.py"""
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
    """yield (container class, [child column classes]) for each flipCardsContainer."""
    st = []; out = []
    for m in TAG.finditer(s):
        closing, tag, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID and not closing: continue
        if closing:
            if st:
                e = st.pop()
                if e[1] is not None: out.append((e[0], e[1]))
            continue
        c = CLS.search(attrs); cls = " ".join(sorted((c.group(1) if c else "").split()))
        rec = [] if (tag == "div" and "flipCardsContainer" in cls.split()) else None
        if st and st[-1][1] is not None and tag == "div": st[-1][1].append(cls)
        st.append([cls, rec])
    return out
G = Counter(); C = Counter(); GS = defaultdict(Counter); CS = defaultdict(Counter); GC = Counter(); CC = Counter(); GP = defaultdict(set); CP = defaultdict(set); CM = defaultdict(set)
for code in sorted(fam):
    subj = (meta.get(code, {}) or {}).get("subject") or "None"
    for n, cp, hp in pairs(code):
        try:
            ch = body(open(cp, encoding="utf-8", errors="replace").read()); gh = body(open(hp, encoding="utf-8", errors="replace").read())
        except Exception: continue
        for cc, cols in groups(gh):
            k = (len(cols), Counter(cols).most_common(1)[0][0] if cols else "(none)"); G[k] += 1; GS[subj][k] += 1; GC[cc] += 1; GP[k].add(hp)
        for cc, cols in groups(ch):
            k = (len(cols), Counter(cols).most_common(1)[0][0] if cols else "(none)"); C[k] += 1; CS[subj][k] += 1; CC[cc] += 1; CP[k].add(cp); CM[k].add(code)
print("==== flipCardsContainer: (cards, column class) — gold vs Claude ====")
keys = sorted(set(G) | set(C), key=lambda k: (-(G[k] + C[k])))
for k in keys[:16]: print(f"   cards {k[0]:2d}  «{k[1]}»   gold {G[k]:4d} (pages {len(GP[k]):3d})   claude {C[k]:4d} (pages {len(CP[k]):3d} / mods {len(CM[k]):3d})")
print("container classes — gold:", GC.most_common(5), " claude:", CC.most_common(5))
print("by subject (gold → claude), the top keys:")
for sj in sorted(set(GS) | set(CS), key=lambda x: -(sum(GS[x].values()) + sum(CS[x].values())))[:10]:
    print(f"   {sj:34s} gold {GS[sj].most_common(3)}   claude {CS[sj].most_common(3)}")
print("==== per subject, the gold's 2-card and 4-card column classes in full (Claude pages with such groups in brackets) ====")
for sj in sorted(GS, key=lambda x: -sum(GS[x].values())):
    for n in (2, 4):
        d = {k[1]: v for k, v in GS[sj].items() if k[0] == n}
        c = {k[1]: v for k, v in CS[sj].items() if k[0] == n}
        if sum(d.values()) + sum(c.values()) >= 3: print(f"   {sj:34s} {n} cards  gold {d}   claude {c}")
