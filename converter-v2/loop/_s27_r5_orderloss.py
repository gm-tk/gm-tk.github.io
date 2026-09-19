#!/usr/bin/env python3
"""Session 27 Round 5 — THE ORDER LOSS: per page, the position-free ratio (multiset overlap) minus the gate's difflib
ratio = the share of the skeleton lost to ORDER / NESTING (every label present, the alignment failing). Ranks the pages
by lost lines (loss × page size) and groups the loss by template / subject; the top pages are then diffed by hand.
  wsl: python3 _s27_r5_orderloss.py"""
import os, sys, re, json
from collections import Counter, defaultdict
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS); sys.path.insert(1, OUTPUTS)
from _measure_ceiling import load_meta
import _corpus
from anchor_compare import CLAUDE
meta = load_meta()
fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
lc = json.load(open(os.path.join(OUTPUTS, "_s27_r3_labelcensus.json")))
sk = json.load(open(os.path.join(OUTPUTS, "_s27_r399_sk_final.json")))
gate = {v["page"]: v["scaffold"] for v in sk["per_page"]}
print("gate pages:", len(gate), "sample:", list(gate.items())[:2])
rows = []
BYG = defaultdict(lambda: [0.0, 0.0, 0]); BYM = defaultdict(lambda: [0.0, 0])
for code, page, la, lb, inter in lc["per_page"]:
    pf = 2.0 * inter / max(1, la + lb)
    key = page[:-5] if page.endswith(".html") else page
    g = gate.get(key) or gate.get(page) or gate.get(code + "/" + page) or gate.get(code + "/" + key)
    if g is None: continue
    if g > 1: g = g / 100.0
    loss = pf - g
    lost_lines = loss * (la + lb) / 2
    tf = fam.get(code, "?"); subj = (meta.get(code, {}) or {}).get("subject") or "None"
    rows.append((lost_lines, loss, pf, g, code, page, la, lb))
    BYG[tf + "/" + subj][0] += lost_lines; BYG[tf + "/" + subj][1] += (la + lb) / 2; BYG[tf + "/" + subj][2] += 1
    BYM[code][0] += lost_lines; BYM[code][1] += 1
rows.sort(reverse=True)
print(f"pages scored {len(rows)}; total lost lines {sum(r[0] for r in rows):.0f}; mean pf {100*sum(r[2] for r in rows)/len(rows):.2f} mean gate {100*sum(r[3] for r in rows)/len(rows):.2f}")
print("==== top 40 pages by lost lines (pf − gate) ====")
for lost, loss, pf, g, code, page, la, lb in rows[:40]:
    print(f"   {lost:6.1f}  loss {100*loss:5.1f}pp  pf {100*pf:5.1f}  gate {100*g:5.1f}  {code}/{page}  claude {la} gold {lb}")
print("==== by group: lost lines / mean lines / pages ====")
for g, (lost, lines, n) in sorted(BYG.items(), key=lambda kv: -kv[1][0])[:16]:
    print(f"   {g:42s} lost {lost:7.0f}  of {lines:8.0f} lines ({100*lost/max(1,lines):.1f}%)  pages {n}")
print("==== top 25 modules by lost lines ====")
for m, (lost, n) in sorted(BYM.items(), key=lambda kv: -kv[1][0])[:25]:
    print(f"   {m:10s} lost {lost:6.0f}  pages {n}")
json.dump(rows, open(os.path.join(OUTPUTS, "_s27_r5_orderloss.json"), "w"))
