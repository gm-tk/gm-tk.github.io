#!/usr/bin/env python3
"""_s52_r7_whkcol.py — session 52 Round 7: the gold's whakataukī column — is the box the direct child of the content column, or
nested in an extra `col-md-12 col-12` column inside it? Per family (gold); and Claude's form. WSL."""
import re, glob, collections
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
def census(root):
    st = collections.defaultdict(collections.Counter)
    for f in glob.glob(root + "/*/*/*.html"):
        mod = f.split("/")[-2]; fam = re.sub(r"\d.*$", "", mod)
        s = open(f, encoding="utf-8", errors="replace").read()
        for m in re.finditer(r'<div class="whakatauki[^"]*">', s):
            pre = re.findall(r'<div class="([^"]*)">', s[max(0, m.start() - 400):m.start()])
            closes = s[max(0, m.start() - 400):m.start()].count("</div>")
            p1 = pre[-1] if pre else ""
            p2 = pre[-2] if len(pre) > 1 else ""
            if "col-md-12" in p1 and "col-md-8" in p2: k = "NESTED col-md-8>col-md-12"
            elif "col-md-12" in p1: k = "col-md-12"
            elif "col-md-8" in p1: k = "col-md-8"
            else: k = "other:" + p1[:20]
            st[fam][k] += 1; st["ALL"][k] += 1
    return st
g = census(R + "/01-Finalized_Modules_"); c = census(R + "/01-Claude_Modules_")
print("GOLD ALL", dict(g["ALL"])); print("CLAUDE ALL", dict(c["ALL"]))
for f in sorted(g, key=lambda x: -sum(g[x].values())):
    if f == "ALL" or sum(g[f].values()) < 3: continue
    n = g[f]["NESTED col-md-8>col-md-12"]; t = sum(g[f].values())
    print(f"{f:8s} nested {n:3d} / {t:3d} ({n / t:.2f})  {dict(g[f])}  | claude {dict(c[f])}")
