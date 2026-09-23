#!/usr/bin/env python3
"""ROUND 446 PICK (session 39 Round 8 — D13-9, the speech-bubble character picture) — the census D13-9 asks for first:
how many writer [speech bubble]s carry a writer picture, and what Claude builds for them.

WT side (every module's parsed Writers Template): each TABLE ROW holding a [speech bubble] / [thought bubble] tag, and
whether the same row carries an [image] tag or an image URL (istockphoto / shutterstock / .jpg / .png) — 'with picture'.
Claude side (every Claude page): each `row speechBubble` and whether its first column holds an <img> ('avatar') or it is
a single col-12 ('text-only'). Reported per module and per family (OS* / TEDC / other).
Run from CONVERTER_V2/reference/tests under WSL: python3 ../../outputs/_r446_bubble_census.py
"""
import os, re, sys, glob
from collections import Counter, defaultdict
sys.path.insert(0, os.getcwd())
import _corpus
ROOT = os.path.normpath(os.path.join(os.getcwd(), "..", "..", ".."))
GOLD = os.path.join(ROOT, "01-Finalized_Modules_")
CLAUDE = os.path.join(ROOT, "01-Claude_Modules_")
BUB = re.compile(r"\[(?:speech|thought)\s*bubble[^\]]*\]", re.I)
IMG = re.compile(r"\[image[^\]]*\]|istockphoto\.com|shutterstock\.com|\.(?:jpe?g|png|gif)\b", re.I)

def fam(code):
    return "OS" if code.startswith("OS") else ("TEDC" if code.startswith("TEDC") else "other")

wt = defaultdict(Counter)
for code in _corpus.mods(GOLD):
    d = _corpus.mdir(GOLD, code)
    ps = sorted(glob.glob(os.path.join(d, "*Writers*_parsed.txt")))
    if not ps:
        continue
    txt = open(ps[0], encoding="utf-8", errors="replace").read()
    for line in txt.split("\n"):
        if not line.startswith("│") or not BUB.search(line):
            continue
        n = len(BUB.findall(line))
        pic = bool(IMG.search(BUB.sub(" ", line)))
        wt[code]["rows"] += 1
        wt[code]["bubbles"] += n
        wt[code]["rows_with_picture" if pic else "rows_no_picture"] += 1

cl = defaultdict(Counter)
for code in _corpus.mods(CLAUDE):
    for f in glob.glob(os.path.join(_corpus.mdir(CLAUDE, code), "*.html")):
        h = open(f, encoding="utf-8", errors="replace").read()
        for m in re.finditer(r'<div class="row speechBubble"[^>]*>\s*<div class="([^"]*)">\s*(<img)?', h):
            cl[code]["avatar" if m.group(2) else "text_only"] += 1

tot = defaultdict(Counter)
rows = []
for code in sorted(set(wt) | set(cl)):
    f = fam(code)
    for k, v in wt[code].items(): tot[f]["wt_" + k] += v
    for k, v in cl[code].items(): tot[f]["cl_" + k] += v
    if wt[code]["rows_with_picture"] and cl[code]["text_only"]:
        rows.append((code, wt[code]["rows_with_picture"], cl[code]["text_only"], cl[code]["avatar"]))
for f in ("OS", "TEDC", "other"):
    print(f, dict(tot[f]))
print("\nmodules where the WT has picture-bearing bubble rows AND Claude built text-only bubbles:")
for r in rows:
    print(f"  {r[0]:10s} WT rows with picture {r[1]:3d} | Claude text-only {r[2]:3d} / avatar {r[3]:3d}")
print(f"modules: {len(rows)}; WT picture rows in them: {sum(r[1] for r in rows)}; Claude text-only in them: {sum(r[2] for r in rows)}")
