#!/usr/bin/env python3
"""Session 44 Round 8 — KB constraint 38 / 03A "autoCheck Auto-Application": on pages whose <html template="…"> is ECH / 1-3 / 4-6, every
interactive that supports autoCheck carries it. Count, per side (Claude corpus, gold corpus) and per template value, the widget roots of the
autoCheck-capable types and how many carry the autoCheck class. Types: dragAndDrop, dropQuiz, multiChoiceQuiz, radioQuiz, wordSelect, typing,
clickDrop (a D&D-family quiz), dropDown. WSL, from outputs/: python3 _s44_r8_autocheck.py"""
import os, re, glob, io, collections
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GOLD = os.path.join(ROOT, "01-Finalized_Modules_"); CL = os.path.join(ROOT, "01-Claude_Modules_")
TYPES = ["dragAndDrop", "dropQuiz", "multiChoiceQuiz", "radioQuiz", "wordSelect", "typing", "clickDrop", "dropDown", "selectionBox", "reorder"]
TRE = re.compile(r'<html[^>]*\btemplate="([^"]*)"', re.I)
DIV = re.compile(r'<div\b[^>]*\bclass="([^"]*)"', re.I)
def scan(root):
    res = collections.defaultdict(collections.Counter); mods = collections.defaultdict(set)
    for p in glob.glob(os.path.join(root, "*", "*", "*.html")):
        s = io.open(p, encoding="utf-8", errors="replace").read()
        m = TRE.search(s); tpl = (m.group(1).lower() if m else "?")
        for d in DIV.finditer(s):
            cls = d.group(1).split()
            for t in TYPES:
                if t in cls:
                    k = (tpl, t); res[k]["ac" if "autoCheck" in cls else "plain"] += 1; mods[k].add(p.split(os.sep)[-2]); break
    return res, mods
for side, root in (("GOLD", GOLD), ("CLAUDE", CL)):
    res, mods = scan(root)
    print(f"== {side}")
    for tpl in ("1-3", "4-6", "ech", "7-8", "9-10", "ncea", "combo"):
        row = [(t, res[(tpl, t)]) for t in TYPES if sum(res[(tpl, t)].values())]
        if not row: continue
        print(f"  template {tpl}: " + "; ".join(f"{t} {c['ac']}/{c['ac'] + c['plain']} ({len(mods[(tpl, t)])}m)" for t, c in row))
