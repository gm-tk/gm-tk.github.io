#!/usr/bin/env python3
"""_s52_r7_limenu.py — session 52 Round 7: THE LESSON MENU THAT LANDED IN THE BODY. Every Claude lesson page carrying r509's
'Lesson menu: the Writers Template has no learning intentions' red flag: does Claude's BODY hold learning-intentions copy
('We are learning' / 'Learning Intentions' / 'I can' / 'success criteria' / 'we will') near its top, and does the paired
gold page's MENU hold it? Per family. WSL, from reference/tests/:  python3 ../../outputs/_s52_r7_limenu.py"""
import os, re, sys, collections
sys.path.insert(0, os.getcwd())
from _discrepancy_audit import pairs
import compare_structure as CS
import _corpus
LI = re.compile(r"we are learning|learning intentions?|success criteria|i can\b|how will i know|whāinga ako|paearu", re.I)
def split(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    a = s.find('id="module-menu-content"'); b = s.find('id="body"')
    menu = s[a:b] if a >= 0 and b > a else ""
    body = s[b:] if b >= 0 else s
    return s, re.sub(r"<[^>]+>", " ", menu), body
st = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list)
mods = sorted(m for m in _corpus.gate_mods(CS.CLAUDE) if os.path.isdir(_corpus.mdir(CS.CLAUDE, m)))
for mod in mods:
    fam = re.sub(r"\d.*$", "", mod)
    for n, cp, hp in pairs(mod):
        s, cmenu, cbody = split(cp)
        if "To Do: Lesson menu:" not in s: continue
        top = re.sub(r"<[^>]+>", " ", cbody[:6000])
        body_li = bool(LI.search(top))
        _, gmenu, _ = split(hp)
        gold_li = bool(LI.search(gmenu))
        k = ("BODY-has-LI" if body_li else "body-no-LI") + " / " + ("GOLD-menu-LI" if gold_li else "gold-menu-none")
        st["ALL"][k] += 1; st[fam][k] += 1
        if body_li and gold_li and len(ex[fam]) < 2: ex[fam].append(os.path.basename(cp))
print("ALL", dict(st["ALL"]))
for f in sorted(st, key=lambda x: -st[x]["BODY-has-LI / GOLD-menu-LI"]):
    if f == "ALL" or not st[f]["BODY-has-LI / GOLD-menu-LI"]: continue
    print(f"{f:8s} {dict(st[f])} e.g. {ex[f]}")
