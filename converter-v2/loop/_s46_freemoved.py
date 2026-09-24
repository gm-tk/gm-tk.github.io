#!/usr/bin/env python3
"""Session 46 — which FREE-body text blocks (outside any widget / hand-off box) a round moved: OLD render dir vs NEW render dir,
per page, then where the GOLD keeps each moved block (_s46_goldloc). WSL, from outputs/:
    python3 _s46_freemoved.py OLD_DIR NEW_DIR CODE …"""
import os, re, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _s46_goldloc import P, locate, fold
WIDGET = re.compile(r"cv2-interactive|accordion|accContent|carousel|flipCard|tabs|clickDrop|dropDown|shapeHover|modal")
def free_blocks(path):
    p = P(); p.feed(open(path, encoding="utf-8", errors="replace").read())
    out = []
    for d, st in p.nodes:
        if any(WIDGET.search(c or "") for _, c, _ in st): continue
        if not any(i == "body" for _, _, i in st): continue
        t = fold(d)
        if len(t) >= 25: out.append((t, d.strip()[:80]))
    return out
old_dir, new_dir = sys.argv[1], sys.argv[2]
for code in sys.argv[3:]:
    for fn in sorted(os.listdir(os.path.join(new_dir, code))):
        if not fn.endswith(".html") or not os.path.exists(os.path.join(old_dir, code, fn)): continue
        o = free_blocks(os.path.join(old_dir, code, fn)); n = set(t for t, _ in free_blocks(os.path.join(new_dir, code, fn)))
        gone = [(t, raw) for t, raw in o if t not in n]
        if not gone: continue
        print(f"{code}/{fn}: {len(gone)} free blocks left the free body")
        for t, raw in gone[:12]:
            g = locate(code, raw[:60])
            where = g[0][1].split(" > ")[-2:] if g else ["(not in gold)"]
            print(f"    {raw[:70]!r}  gold: {' > '.join(where)[:80]}")
