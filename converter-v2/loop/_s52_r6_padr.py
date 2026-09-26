#!/usr/bin/env python3
"""_s52_r6_padr.py — session 52 Round 6: the body content column's `paddingR` — per family, gold vs Claude: col-md-8 columns in
#body with / without paddingR, and (gold) whether a col-md-4 sibling column follows in the same row. Regex-level. WSL."""
import re, glob, collections
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
col = re.compile(r'<div class="([^"]*\bcol-md-8\b[^"]*)">')
def div_close(s, i):
    d = 0
    for m in re.finditer(r"<(/?)div\b[^>]*>", s[i:]):
        d += -1 if m.group(1) else 1
        if d == 0: return i + m.end()
    return len(s)
def census(root, side=False):
    st = collections.defaultdict(collections.Counter)
    for f in glob.glob(root + "/*/*/*.html"):
        mod = f.split("/")[-2]; fam = re.sub(r"\d.*$", "", mod)
        s = open(f, encoding="utf-8", errors="replace").read(); b = s.find('id="body"')
        if b < 0: continue
        for m in col.finditer(s, b):
            cls = m.group(1).split()
            pr = "paddingR" in cls
            k = "padR" if pr else "plain"
            if side:
                e = div_close(s, m.start())
                nxt = s[e:e + 200].lstrip()
                k += "+side" if re.match(r'<div class="[^"]*col-md-4', nxt) else ""
            st[fam][k] += 1
    return st
g = census(R + "/01-Finalized_Modules_", True); c = census(R + "/01-Claude_Modules_", True)
rows = sorted(((g[f]["padR"] + g[f]["padR+side"], f) for f in g), reverse=True)[:22]
for n, f in rows:
    t = sum(g[f].values())
    print(f"{f:8s} gold padR {n:4d} / {t:4d} ({n / max(1, t):.2f}) {dict(g[f])}  | claude {dict(c[f])}")
