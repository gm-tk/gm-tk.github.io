#!/usr/bin/env python3
"""PUNCTUATION-ONLY PARAGRAPHS: per glyph — Claude occurrences / pages / modules, gold occurrences / pages; for each Claude one,
does the gold page carry the same glyph-only paragraph (SAME) or not (DROPPED)? Contexts. python3 _s26_r393_punct.py"""
import os, sys, re, html as H
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
sys.path.insert(0, OUTPUTS)
src = open(os.path.join(OUTPUTS, "_s26_r392_adjul.py"), encoding="utf-8").read()
exec(src[:src.index("ADJ = re.compile")])
from collections import Counter, defaultdict
PUNCT = re.compile(r"<p\b[^>]*>\s*(?:<[^>]+>\s*)*([^\w<>\s])\s*(?:</[^>]+>\s*)*</p>")
CN = Counter(); CP = defaultdict(set); CM = defaultdict(set); GN = Counter(); GP = defaultdict(set); SAME = Counter(); DROP = Counter(); EX = defaultdict(list); BYS = defaultdict(Counter)
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"
    for n, cp, hp in pairs(code):
        try:
            ch = body(open(cp, encoding="utf-8", errors="replace").read()); gh = body(open(hp, encoding="utf-8", errors="replace").read())
        except Exception: continue
        cl = "".join(live_pieces(ch)); gl = "".join(live_pieces(gh))
        gg = Counter(H.unescape(g) for g in PUNCT.findall(gl))
        for g in gg: GN[g] += gg[g]; GP[g].add(hp)
        for m in PUNCT.finditer(cl):
            g = H.unescape(m.group(1)); CN[g] += 1; CP[g].add(cp); CM[g].add(code); BYS[g][f"{tf}/{subj}"] += 1
            if gg.get(g, 0) > 0: SAME[g] += 1; gg[g] -= 1
            else: DROP[g] += 1
            if len(EX[g]) < 3: EX[g].append(f"{os.path.basename(cp)[:-5]}: …{re.sub(r'\s+',' ',cl[max(0,m.start()-100):m.start()])[-70:]} ▶{m.group(0)[:40]}◀ {re.sub(r'\s+',' ',cl[m.end():m.end()+50])[:40]}")
print("glyph  claude n / pages / mods   gold n / pages   SAME  DROPPED  (drop share)")
for g, n in CN.most_common(14):
    print(f"  {g!r:6s} {n:4d} / {len(CP[g]):3d} / {len(CM[g]):3d}     {GN.get(g,0):3d} / {len(GP.get(g,set())):3d}     {SAME[g]:3d}  {DROP[g]:3d}   ({DROP[g]/n:.2f})   {BYS[g].most_common(3)}")
    for e in EX[g]: print("        ", e)
allp = set().union(*CP.values()); allm = set().union(*CM.values())
d = sum(DROP.values()); s = sum(SAME.values())
print(f"ALL glyphs: claude {sum(CN.values())} on {len(allp)} pages / {len(allm)} modules; dropped {d} / same {s} → drop share {d/(d+s):.2f}")
