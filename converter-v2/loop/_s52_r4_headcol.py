#!/usr/bin/env python3
"""_s52_r4_headcol.py — session 52 Round 4: THE HEADING-ONLY COLUMN. In the gold, a section heading (h2 / h3) that is the
FIRST child of a body column: is the column the heading ALONE (`col-12` holding only the heading — AGH's form) or does
the content follow in the same column? Per family, gold and Claude side by side (Claude pages on disk). Regex-level. WSL:
    python3 _s52_r4_headcol.py"""
import os, re, glob, collections
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
col_re = re.compile(r'<div class="([^"]*\bcol-[^"]*)">\s*(<h([23])\b[^>]*>.*?</h\3>)\s*(</div>|<)', re.S)
def census(root):
    st = collections.defaultdict(collections.Counter)
    for f in glob.glob(root + "/*/*/*.html"):
        mod = f.split("/")[-2]; fam = re.sub(r"\d.*$", "", mod)
        s = open(f, encoding="utf-8", errors="replace").read()
        b = s.find('id="body"')
        if b < 0: continue
        for m in col_re.finditer(s, b):
            cls = m.group(1).split(); alone = m.group(4) == "</div>"
            if "alert" in cls or "activity" in cls: continue
            k = ("ALONE " if alone else "HEAD+ ") + ("col-12" if cls == ["col-12"] else "col-md-8" if "col-md-8" in cls else "other")
            st[fam][k] += 1
    return st
import sys
if len(sys.argv) > 1:   # per-module for the listed family prefixes: body-level sections only (col not inside a box)
    fams = set(sys.argv[1:])
    for f in sorted(glob.glob(R + "/01-Finalized_Modules_/*/*/*.html")):
        mod = f.split("/")[-2]; fam = re.sub(r"\d.*$", "", mod)
        if fam not in fams: continue
        s = open(f, encoding="utf-8", errors="replace").read(); b = s.find('id="body"')
        cnt = collections.Counter()
        for m in col_re.finditer(s, b if b >= 0 else 0):
            cls = m.group(1).split(); alone = m.group(4) == "</div>"
            pre = s[max(0, m.start() - 120):m.start()]
            if 'class="activity' in pre or 'class="alert' in pre: continue
            cnt[("A" if alone else "H") + ("12" if cls == ["col-12"] else "8" if "col-md-8" in cls else "o")] += 1
        print(f"{mod:9s} {os.path.basename(f):28s} {dict(cnt)}")
    sys.exit()
g = census(R + "/01-Finalized_Modules_"); c = census(R + "/01-Claude_Modules_")
rows = []
for fam in g:
    a = g[fam]["ALONE col-12"]; t = sum(g[fam].values())
    if a >= 5: rows.append((a, fam, t))
for a, fam, t in sorted(rows, reverse=True)[:25]:
    print(f"{fam:8s} gold ALONE col-12 {a:4d} / {t:4d} ({a / t:.2f})  gold {dict(g[fam].most_common(4))}  | claude {dict(c[fam].most_common(3))}")
