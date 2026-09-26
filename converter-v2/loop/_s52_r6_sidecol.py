#!/usr/bin/env python3
"""_s52_r6_sidecol.py — session 52 Round 6: THE GOLD'S SIDE COLUMN. Every #body `col-md-8` content column followed in its row
by a `col-md-4` column: what the side column holds (its child sequence), per family — gold vs Claude counts. WSL."""
import re, glob, collections, sys
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
col = re.compile(r'<div class="([^"]*\bcol-md-8\b[^"]*)">')
def div_close(s, i):
    d = 0
    for m in re.finditer(r"<(/?)div\b[^>]*>", s[i:]):
        d += -1 if m.group(1) else 1
        if d == 0: return i + m.end()
    return len(s)
def kids(inner):
    seq = []
    for t, attrs in re.findall(r"<(p|img|div|h[1-6]|ul|ol|a|iframe|table|figure)\b([^>]*)>", inner):
        c = re.search(r'class="([^"]*)"', attrs); c = c.group(1).split()[0] if c else ""
        k = t + ("." + c if c and t in ("div", "p") else "")
        if k in ("div.row", "div.col-12") or (seq and seq[-1] == k): continue
        seq.append(k)
    return " ".join(seq[:4])
def census(root):
    st = collections.defaultdict(collections.Counter); tot = collections.Counter()
    for f in glob.glob(root + "/*/*/*.html"):
        mod = f.split("/")[-2]; fam = re.sub(r"\d.*$", "", mod)
        s = open(f, encoding="utf-8", errors="replace").read(); b = s.find('id="body"')
        if b < 0: continue
        for m in col.finditer(s, b):
            e = div_close(s, m.start())
            nxt = s[e:e + 300].lstrip()
            mm = re.match(r'<div class="([^"]*col-md-4[^"]*)">', nxt)
            if not mm: continue
            st0 = e + (len(s[e:e + 300]) - len(s[e:e + 300].lstrip()))
            e2 = div_close(s, st0)
            k = kids(s[st0 + len(mm.group(0)):e2])
            st[fam][k] += 1; tot[k] += 1
    return st, tot
g, gt = census(R + "/01-Finalized_Modules_"); c, ct = census(R + "/01-Claude_Modules_")
print("GOLD side-column contents (all families):", gt.most_common(14))
print("CLAUDE side-column contents:", ct.most_common(8))
for f in sorted(g, key=lambda x: -sum(g[x].values()))[:14]:
    print(f"{f:8s} gold {sum(g[f].values()):4d} {dict(g[f].most_common(4))} | claude {sum(c[f].values())}")
