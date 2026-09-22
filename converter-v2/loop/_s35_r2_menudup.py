#!/usr/bin/env python3
"""Session 35 Round 2 PICK measurement — BODY CONTENT DUPLICATED INTO THE MODULE-MENU REGION (the CEDO204 finding).
For every Claude page: the text of every <p>/<h2>-<h6>/<li> in the region BEFORE `<div id="body">` (the header + module menu),
and the same in the body. A region element whose normalised text (>= 40 chars) also occurs in the body is a DUPLICATE. Also
count the region's text elements that occur NOWHERE in the gold's own menu region (the gold's page 0 / the same page) — the
over-capture. Report per module (pages, duplicates) and the corpus totals; list the top modules.
Run under WSL: python3 _s35_r2_menudup.py
"""
import re, os, glob, html, collections
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"

def norm(s):
    return re.sub(r'[^a-z0-9]+', '', html.unescape(re.sub(r'<[^>]+>', ' ', s)).lower())

def texts(h):
    return [norm(m.group(2)) for m in re.finditer(r'<(p|h[2-6]|li)\b[^>]*>((?:(?!</?(?:p|h[2-6]|li)\b).)*?)</\1>', h, re.S)]

per = collections.OrderedDict(); tot_pages = 0; tot_dup = 0; pages_with = 0
for cdir in sorted(glob.glob(R + "01-Claude_Modules_/*/*/")):
    code = os.path.basename(cdir.rstrip("/"))
    for cp in sorted(glob.glob(cdir + "*.html")):
        if "acks" in os.path.basename(cp).lower():
            continue
        h = open(cp, encoding="utf-8", errors="replace").read()
        i = h.find('<div id="body">')
        if i < 0:
            continue
        head, body = h[:i], h[i:]
        ht = [t for t in texts(head) if len(t) >= 40]
        bt = set(texts(body))
        dup = [t for t in ht if t in bt]
        tot_pages += 1
        if dup:
            pages_with += 1; tot_dup += len(dup)
            per.setdefault(code, []).append((os.path.basename(cp), len(ht), len(dup)))

print("pages %d; pages with >=1 duplicated region element: %d; duplicated elements: %d; modules: %d" % (tot_pages, pages_with, tot_dup, len(per)))
rows = sorted(per.items(), key=lambda kv: -sum(d for _, _, d in kv[1]))
for code, items in rows[:40]:
    print("  %-10s pages %2d  dup %3d  e.g. %s" % (code, len(items), sum(d for _, _, d in items), ", ".join("%s %d/%d" % (p[:18], d, n) for p, n, d in items[:3])))
