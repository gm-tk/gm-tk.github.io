#!/usr/bin/env python3
"""_s52_r8_stockimg.py — session 52 Round 8: every bare stock-photo URL paragraph in Claude's body outside the hand-off boxes —
does the GOLD show that image (its iStock id in an <img src/alt>) on the paired page / elsewhere in the module / only in the
acks / nowhere? Per family; and whether the paragraph sits inside a Claude activity box. WSL, from reference/tests/:
    python3 ../../outputs/_s52_r8_stockimg.py"""
import os, re, sys, glob, collections
sys.path.insert(0, os.getcwd())
from _discrepancy_audit import pairs
import compare_structure as CS
import _corpus
P = re.compile(r"<p\b[^>]*>\s*(?:<a\b[^>]*>)?\s*(https?://[^\s<\"]+)\s*(?:</a>)?\s*</p>", re.I)
STOCK = re.compile(r"istockphoto|gettyimages|shutterstock", re.I)
def spans_of(s):
    out = []
    for h in re.finditer(r'<div class="cv2-interactive[^"]*"', s):
        d = 0
        for x in re.finditer(r"<(/?)div\b[^>]*>", s[h.start():]):
            d += -1 if x.group(1) else 1
            if d == 0: out.append((h.start(), h.start() + x.end())); break
    return out
st = collections.Counter(); fam = collections.defaultdict(collections.Counter); pages = collections.defaultdict(set); mods = collections.defaultdict(set)
for mod in sorted(m for m in _corpus.gate_mods(CS.CLAUDE) if os.path.isdir(_corpus.mdir(CS.CLAUDE, m))):
    gall = ""
    try:
        gd = _corpus.mdir(CS.HUMAN, mod)
        gall = "".join(open(f, encoding="utf-8", errors="replace").read() for f in glob.glob(os.path.join(gd, "*.html")))
    except Exception: pass
    for n, cp, hp in pairs(mod):
        s = open(cp, encoding="utf-8", errors="replace").read(); b = s.find('id="body"'); sp = spans_of(s)
        g = open(hp, encoding="utf-8", errors="replace").read()
        gimgs = " ".join(re.findall(r"<img\b[^>]*>", g)); aimgs = " ".join(re.findall(r"<img\b[^>]*>", gall))
        for m in P.finditer(s, max(b, 0)):
            if any(a <= m.start() < z for a, z in sp): continue
            u = m.group(1)
            if not STOCK.search(u): continue
            mid = re.search(r"gm-?(\d{6,10})", u) or re.search(r"/id/(\d{6,10})", u)
            if not mid: k = "no-id"
            else:
                i = mid.group(1)
                k = "gold img on the PAGE" if i in gimgs else ("gold img elsewhere in module" if i in aimgs else ("gold: id in text only (acks)" if i in gall else "gold: absent"))
            st[k] += 1; fam[k][re.sub(r"\d.*$", "", mod)] += 1; pages[k].add(cp); mods[k].add(mod)
for k, n in st.most_common():
    print(f"{n:4d} paras / {len(pages[k]):3d} pages / {len(mods[k]):3d} mods  {k}   top: {', '.join(f'{a} {b}' for a, b in fam[k].most_common(8))}")
