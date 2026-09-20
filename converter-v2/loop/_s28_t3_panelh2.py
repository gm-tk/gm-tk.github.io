#!/usr/bin/env python3
"""session 28 task 3 — for the 9 WJFUN modules whose disk page already carries fundamentalsPanels (the r106
phase-text path), what level does the GOLD ship each panel's first own heading at? (Decides whether the
first_heading_level WJFUN entry is gold-ward on them, independent of the tile dialect.)"""
import os, re, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
codes = [l.strip() for l in open(os.path.join(HERE, "_s28_t3_OFF_modules.txt")) if l.strip()]
H = re.compile(r"<h([1-6])[^>]*>(.*?)</h\1>", re.S)
def fold(t): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip().lower()
for code in codes:
    cp = glob.glob(os.path.join(ROOT, "01-Claude_Modules_", "*", code, f"{code}_0_0.html"))
    gp = glob.glob(os.path.join(ROOT, "01-Finalized_Modules_", "*", code, f"{code}_0_0.html")) or \
         glob.glob(os.path.join(ROOT, "01-Finalized_Modules_", "*", code, "*.html"))
    if not cp or not gp: print(code, "MISSING", cp, gp); continue
    c = open(cp[0], encoding="utf-8", errors="replace").read(); g = open(gp[0], encoding="utf-8", errors="replace").read()
    gh = {}
    for m in H.finditer(g): gh.setdefault(fold(m.group(2)), []).append(int(m.group(1)))
    # each fundamentalsPanel's first heading on disk
    out = []
    for pm in re.finditer(r'<div class="fundamentalsPanel"[^>]*>', c):
        seg = c[pm.end():pm.end() + 4000]
        hm = H.search(seg)
        if not hm: out.append("(no heading)"); continue
        t = fold(hm.group(2)); lv = int(hm.group(1))
        out.append(f"claude h{lv} '{t[:38]}' -> gold {'h'+'/h'.join(map(str, gh[t])) if t in gh else 'ABSENT'}")
    print(code, f"panels {len(out)}:", " | ".join(out))
