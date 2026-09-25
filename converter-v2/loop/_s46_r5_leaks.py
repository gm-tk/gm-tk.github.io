#!/usr/bin/env python3
"""Session 46 Round 5 — every literal-[tag] leak the protected gate counts (the gate's own visible_text + LITERAL_TAG), with its context
and the tag, grouped by the leaked tag word and by mechanism hints. WSL, from reference/tests: python3 ../../outputs/_s46_r5_leaks.py"""
import os, sys, re, collections
sys.path.insert(0, os.getcwd())
import _structural_defect_audit as A
import _corpus
CLAUDE = os.path.normpath(os.path.join(os.getcwd(), "..", "..", "..", "01-Claude_Modules_"))
rows = []
for m in _corpus.gate_mods(CLAUDE):
    d = _corpus.mdir(CLAUDE, m)
    if not os.path.isdir(d): continue
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".html"): continue
        html = open(os.path.join(d, fn), encoding="utf-8").read()
        body = html[html.find('id="body"'):] if 'id="body"' in html else html
        vis = A.visible_text(body)
        for mm in A.LITERAL_TAG.finditer(vis):
            ctx = re.sub(r"\s+", " ", vis[max(0, mm.start() - 60): mm.end() + 60])
            rows.append((m, fn, mm.group(0), ctx))
print(len(rows), "leaks on", len(set((r[0], r[1]) for r in rows)), "pages")
print(collections.Counter(re.sub(r"\s+", " ", r[2]).lower() for r in rows).most_common(20))
for r in rows: print(f"  {r[0]:9s} {r[1]:22s} {r[2]!r:14s} …{r[3]}…")
