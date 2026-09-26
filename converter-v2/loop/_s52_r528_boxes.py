#!/usr/bin/env python3
"""s52 Round 1 — the r528 ON boxes: for every whakatauki box a saved ON page has beyond its disk (OFF) page, report
its <p> count, the line just before its row, and the line just after the box. WSL:
  python3 _s52_r528_boxes.py SAVEDIR"""
import os, re, sys, glob
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
save = sys.argv[1]
box_re = re.compile(r'<div class="whakatauki[^"]*">(.*?)</div>', re.S)
def boxes(t): return [m for m in box_re.finditer(t)]
def strip(s): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()
one = two = 0; labels = {}
for code in sorted(os.listdir(save)):
    for on in sorted(glob.glob(os.path.join(save, code, "*.html"))):
        off = glob.glob(os.path.join(R, "01-Claude_Modules_", "*", code, os.path.basename(on)))
        if not off: continue
        a = io = open(off[0], encoding="utf-8").read(); b = open(on, encoding="utf-8").read()
        oldtexts = {strip(m.group(1)) for m in boxes(a)}
        for m in boxes(b):
            inner = m.group(1)
            if strip(inner) in oldtexts: continue
            ps = re.findall(r"<p[^>]*>(.*?)</p>", inner, re.S)
            before = b[:m.start()].rstrip().split("\n")
            prevp = next((strip(l) for l in reversed(before) if "<p" in l), "")
            after = b[m.end():].split("\n")
            nextp = next((strip(l) for l in after if "<p" in l), "")
            if len(ps) < 2: one += 1
            else: two += 1
            if len(prevp) < 25: labels[prevp] = labels.get(prevp, 0) + 1
            print(f"{os.path.basename(on):26s} p={len(ps)} | prev: {prevp[:50]!r} | box: {strip(inner)[:70]!r} | next: {nextp[:60]!r}")
print(f"NEW BOXES: {one + two} — 1 <p>: {one}, 2+ <p>: {two}")
print("short prev lines:", sorted(labels.items(), key=lambda x: -x[1])[:15])
