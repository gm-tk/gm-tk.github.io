#!/usr/bin/env python3
"""_s51_r6_empty.py — session 51 Round 6 PICK: every hand-off box body_compare counts EMPTY (< 40 member characters) on the
current corpus — its banner (type / modifier) and its member text, grouped by type and by the member text's shape. WSL, from
reference/tests/."""
import json, os, re, sys, collections
sys.path.insert(0, os.getcwd())
import _corpus
from anchor_compare import CLAUDE

d = json.load(open("body_compare.json"))
pages = [r["page"] for r in d if r.get("empty_widgets", 0) > 0]
BOX = re.compile(r'<div class="cv2-interactive" data-cv2-index="\d+"[^>]*>\s*<p[^>]*>⚙ INTERACTIVE \(un-built\) #\d+: (.*?)</p>\s*<div[^>]*>(.*?)</div>\s*</div>', re.S)
strip = lambda h: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)).strip()
by = collections.Counter(); ex = collections.defaultdict(list)
for pg in pages:
    code = pg.split("/")[0]
    p = os.path.join(_corpus.mdir(CLAUDE, code), pg.split("/")[1])
    html = open(p, encoding="utf-8", errors="replace").read()
    for m in BOX.finditer(html):
        txt = strip(m.group(2))
        if len(txt) >= 40: continue
        typ = m.group(1).split(" — ")[0][:40]
        shape = "empty" if not txt else ("url" if re.match(r"https?://", txt) else ("1-3 words" if len(txt.split()) <= 3 else "short"))
        k = f"{typ} | {shape}"
        by[k] += 1
        if len(ex[k]) < 4: ex[k].append(f"{pg}: '{txt[:38]}'")
print("empty boxes:", sum(by.values()))
for k, n in by.most_common(30): print(f"{n:4d} {k:55s} e.g. {ex[k][0]}")
