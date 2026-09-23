#!/usr/bin/env python3
"""ROUND 445 — the population re-measure (D13-2): for each page the comparison form changes, the table's header pair on
the Claude side and the class of every two-column table on the paired gold page. Run from reference/tests under WSL."""
import os, re, sys
sys.path.insert(0, os.getcwd())
from _discrepancy_audit import pairs
from collections import Counter
O = os.path.join("..", "..", "outputs")
pages = [l.strip() for l in open(os.path.join(O, "_r445_ON_pages.txt")) if l.strip()]
tally = Counter()
for pg in pages:
    code, fn = pg.split("/", 1)
    on = open(os.path.join(O, "_r445_on", code, fn), encoding="utf-8").read()
    m = re.search(r'<table class="table table-bordered tableFixed">(.*?)</table>', on, re.S)
    hdr = re.findall(r"<th[^>]*>(.*?)</th>", m.group(1), re.S)[:2] if m else []
    hdr = [re.sub(r"<[^>]+>", "", h).strip()[:24] for h in hdr]
    gp = [hp for n, cp, hp in pairs(code) if os.path.basename(cp) == fn]
    gcls = []
    if gp:
        g = open(gp[0], encoding="utf-8", errors="replace").read()
        for tm in re.finditer(r'<table([^>]*)>(.*?)</table>', g, re.S):
            rows = re.findall(r"<tr[^>]*>(.*?)</tr>", tm.group(2), re.S)
            if rows and all(len(re.findall(r"<t[hd][\s>]", r)) == 2 for r in rows):
                c = re.search(r'class="([^"]*)"', tm.group(1)); gcls.append(c.group(1) if c else "(none)")
    for c in gcls: tally[c] += 1
    print(f"{pg:28s} header {hdr} | gold 2-col tables: {gcls or '—'}")
print("gold two-column table classes on these pages:", dict(tally))
