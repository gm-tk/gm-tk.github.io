#!/usr/bin/env python3
"""ROUND 446 PICK (D13-9 part 1) — the dropped-picture census. For every WT table row that holds a [speech bubble] /
[thought bubble] tag AND an iStock picture, take the picture's iStock id and ask whether the module's Claude pages carry
`iStock-<id>` at all (the picture was built somewhere) and inside a `row speechBubble` (built in the bubble layout).
A missing picture is classified by the row's SHAPE: bubbles in the row (1 / 2+), cells in the row, the picture's cell.
Run from CONVERTER_V2/reference/tests under WSL: python3 ../../outputs/_r446_bubble_drop.py
"""
import os, re, sys, glob
from collections import Counter
sys.path.insert(0, os.getcwd())
import _corpus
ROOT = os.path.normpath(os.path.join(os.getcwd(), "..", "..", ".."))
GOLD = os.path.join(ROOT, "01-Finalized_Modules_")
CLAUDE = os.path.join(ROOT, "01-Claude_Modules_")
BUB = re.compile(r"\[(?:speech|thought)\s*bubbles?[^\]]*\]", re.I)
IST = re.compile(r"istockphoto\.com/\S*?gm(\d{6,})", re.I)

def fam(code):
    return "OS" if code.startswith("OS") else ("TEDC" if code.startswith("TEDC") else "other")

tot, shape, famc, examples = Counter(), Counter(), Counter(), []
for code in _corpus.mods(GOLD):
    ps = sorted(glob.glob(os.path.join(_corpus.mdir(GOLD, code), "*Writers*_parsed.txt")))
    if not ps:
        continue
    cd = _corpus.mdir(CLAUDE, code)
    html = "".join(open(f, encoding="utf-8", errors="replace").read() for f in glob.glob(os.path.join(cd, "*.html")))
    bub_blocks = "".join(m.group(0) for m in re.finditer(r'<div class="row speechBubble".*?(?=<div class="row speechBubble"|\Z)', html, re.S))
    for line in open(ps[0], encoding="utf-8", errors="replace").read().split("\n"):
        if not line.startswith("│") or not BUB.search(line):
            continue
        ids = IST.findall(line)
        if not ids:
            continue
        cells = line.strip("│ ").split("║")
        nb = len(BUB.findall(line))
        pic_cell = next((i for i, c in enumerate(cells) if IST.search(c)), -1)
        for gid in ids[:1]:
            tot["rows"] += 1
            anywhere = ("iStock-" + gid) in html or gid in html
            in_bub = gid in bub_blocks
            k = "in_bubble" if in_bub else ("elsewhere" if anywhere else "MISSING")
            tot[k] += 1
            if k != "in_bubble":
                s = f"bubbles={'2+' if nb >= 2 else '1'} cells={len(cells)} pic_cell={pic_cell}"
                shape[(k, s)] += 1
                famc[(k, fam(code))] += 1
                if len(examples) < 40:
                    examples.append(f"{code:9s} {k:9s} {s} | {line[:150]}")
print("rows with a bubble + an iStock picture:", dict(tot))
print("by family:", dict(famc))
print("by shape:")
for (k, s), n in shape.most_common():
    print(f"  {k:9s} {s:32s} {n}")
print("examples:")
for e in examples:
    print("  " + e)
