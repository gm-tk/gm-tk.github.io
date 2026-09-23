#!/usr/bin/env python3
"""ROUND 446 PICK (D13-9 part 2) — the OS / TEDC placeholder class. Gold: of every `row speechBubble`, how many carry an
<img> (the character picture) — per family. Claude: every text-only bubble row (`row speechBubble` > col-12, no <img>)
in OS* / TEDC*, split by the layout attribute and by whether the page ALSO carries a Writers Note naming a picture
(the TEDC 'avatar Tina …' dialect, where the writer DID name one) — the population D13-9 (2) would add a placeholder to.
Run from CONVERTER_V2/reference/tests under WSL: python3 ../../outputs/_r446_bubble_family.py
"""
import os, re, sys, glob
from collections import Counter
sys.path.insert(0, os.getcwd())
import _corpus
ROOT = os.path.normpath(os.path.join(os.getcwd(), "..", "..", ".."))
GOLD = os.path.join(ROOT, "01-Finalized_Modules_")
CLAUDE = os.path.join(ROOT, "01-Claude_Modules_")
ROW = re.compile(r'<div class="row speechBubble"([^>]*)>(.*?)(?=<div class="row speechBubble"|</div>\s*</div>\s*</div>\s*<(?:p|div class="row"|h)|\Z)', re.S)

def fam(code):
    return "OS" if code.startswith("OS") else ("TEDC" if code.startswith("TEDC") else None)

g, c, cmods = Counter(), Counter(), Counter()
for root, side in ((GOLD, "gold"), (CLAUDE, "claude")):
    for code in _corpus.mods(root):
        f = fam(code)
        if not f:
            continue
        for fn in glob.glob(os.path.join(_corpus.mdir(root, code), "*.html")):
            h = open(fn, encoding="utf-8", errors="replace").read()
            for m in re.finditer(r'<div class="row speechBubble"([^>]*)>\s*<div class="([^"]*)">\s*(<img)?', h):
                has_img = bool(m.group(3)) or ("<img" in h[m.end():m.end() + 900].split('class="row speechBubble"')[0][:900] and "col-12" not in m.group(2))
                if side == "gold":
                    g[(f, "img" if (m.group(3) or 'col-md-4' in m.group(2) or 'col-md-3' in m.group(2)) else "no_img")] += 1
                else:
                    if m.group(3):
                        c[(f, "avatar")] += 1
                    elif m.group(2).strip() == "col-12":
                        lay = re.search(r'layout="([^"]*)"', m.group(1))
                        near = h[m.end():m.end() + 2500]
                        named = bool(re.search(r"Writers Note:[^<]{0,200}(avatar|istock|image|photo|picture)", near, re.I))
                        c[(f, "text_only", lay.group(1) if lay else "-", "picture-note-nearby" if named else "no-picture-note")] += 1
                        cmods[(f, code)] += 1
                    else:
                        c[(f, "other:" + m.group(2))] += 1
print("GOLD bubble rows by family:", dict(g))
for f in ("OS", "TEDC"):
    tot = g[(f, "img")] + g[(f, "no_img")]
    print(f"  {f}: picture share {g[(f, 'img')]}/{tot} = {g[(f, 'img')]/max(1, tot):.2f}")
print("CLAUDE bubble rows:")
for k, v in sorted(c.items(), key=lambda x: -x[1]):
    print("  ", k, v)
print("Claude text-only modules:", len(cmods), dict(Counter(k[0] for k in cmods)))
print("  ", " ".join(f"{k[1]}:{v}" for k, v in sorted(cmods.items())))
