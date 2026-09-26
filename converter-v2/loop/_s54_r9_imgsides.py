#!/usr/bin/env python3
"""_s54_r9_imgsides.py — list (family filter) the Claude main-column stock images whose gold placement is the SIDE column: page, id,
the Claude context (the block before the image) and the gold's row (the side column's sibling column's first block). WSL, from
reference/tests/:  python3 ../../outputs/_s54_r9_imgsides.py FAM [FAM …]"""
import os, re, sys, glob
sys.path.insert(0, os.getcwd())
from _discrepancy_audit import pairs
import _corpus
from anchor_compare import CLAUDE, HUMAN
import importlib.util
spec = importlib.util.spec_from_file_location("imf", os.path.join("..", "..", "outputs", "_s54_r9_imgfate.py"))
fams = set(sys.argv[1:])
ID = re.compile(r"(?:iStock-|gm)(\d{6,})|shutterstock[^\d]{0,40}(\d{6,})", re.I)
exec(open(os.path.join("..", "..", "outputs", "_s54_r9_imgfate.py"), encoding="utf-8").read().split("fam = lambda")[0])
for mod in sorted(set(_corpus.gate_mods(CLAUDE))):
    if re.sub(r"\d.*$", "", mod) not in fams: continue
    for n, cp, hp in pairs(mod):
        g = dict((i, w) for i, w in imgs(hp))
        for i, w in imgs(cp):
            if w == "main" and g.get(i) == "side":
                cs = open(cp, encoding="utf-8").read(); hs = open(hp, encoding="utf-8", errors="replace").read()
                ci = cs.find(i); hi = hs.find(i)
                ctx = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "|", cs[max(0, ci - 500):ci]))[-160:]
                gctx = re.sub(r"\s+", " ", hs[max(0, hi - 700):hi])
                gcls = re.findall(r'class="(col[^"]*|row[^"]*)"', gctx)[-4:]
                print(f"{os.path.basename(cp):20s} {i}  claude-before: …{ctx[-110:]!r}\n{'':20s} gold classes before: {gcls}")
