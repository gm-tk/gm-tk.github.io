#!/usr/bin/env python3
"""Session 45 Round 7 — for the in-body lesson-menu pages, the WT lines around the gold menu's first sentence (the marker form).
WSL, from outputs/: python3 _s45_r7_wtform.py CODE:claude_page ..."""
import os, re, io, sys, json, glob
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "tests"))
import _corpus
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_s45_r7_emptymenu.py"), encoding="utf-8").read().split("pp = json.load")[0])
pp = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_diff_miner.json"), encoding="utf-8"))["per_page"]
RED = re.compile(r"🔴\[RED TEXT\]|\[/RED TEXT\]🔴")
for arg in sys.argv[1:]:
    code, cpage = arg.split(":")
    rec = next(r for r in pp if r["module"] == code and r["page"] == cpage)
    gm, _ = split_regions(os.path.join(_corpus.mdir(GOLD, code), rec["gold"]))
    key = " ".join(gm.split()[:6])
    wts = [p for p in glob.glob(os.path.join(_corpus.mdir(GOLD, code), "*_parsed.txt")) if "writers template" in p.lower()]
    lines = []
    for w in wts: lines += io.open(w, encoding="utf-8", errors="replace").read().split("\n")
    hit = next((i for i, l in enumerate(lines) if key and key[:30] in n(RED.sub(" ", l))), None)
    if hit is None:
        k2 = " ".join(gm.split()[1:5])
        hit = next((i for i, l in enumerate(lines) if k2 and k2 in n(RED.sub(" ", l))), None)
    print(f"===== {code} {cpage} (gold menu starts «{key}»)")
    if hit is None: print("   (not found in WT)"); continue
    for l in lines[max(0, hit - 9):hit + 3]:
        if l.strip(): print("   " + RED.sub("", l)[:170])
