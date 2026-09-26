#!/usr/bin/env python3
"""_s54_r4_ddlayout.py — session 54 Round 4: for every dragAndDrop widget NEW in a probe's saved ON pages (present there, absent on
disk), find the gold widget of the same module whose drag texts overlap it most and compare the two layouts (standard / column /
FIB / …). WSL, from reference/tests/:  python3 ../../outputs/_s54_r4_ddlayout.py SAVEDIR AFFECTED.txt"""
import os, re, sys, glob, html as H
sys.path.insert(0, os.getcwd())
import _corpus
from anchor_compare import CLAUDE, HUMAN

save, aff = sys.argv[1], sys.argv[2]
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", H.unescape(re.sub(r"<[^>]+>", " ", s)).lower())).strip()


def widgets(s):
    out = []
    for m in re.finditer(r'<div class="dragAndDrop[^"]*"[^>]*layout="([^"]*)"', s):
        seg = s[m.start(): m.start() + 60000]
        end = seg.find('class="dragAndDrop', 20)
        seg = seg[: end if end > 0 else len(seg)]
        drags = [norm(x) for x in re.findall(r'<div class="drag"[^>]*>([\s\S]*?)</div>', seg)]
        out.append((m.group(1), [d for d in drags if d]))
    return out


agree = dis = nomatch = 0
for mod in [l.strip() for l in open(aff) if l.strip()]:
    gold = []
    for p in glob.glob(os.path.join(_corpus.mdir(HUMAN, mod), "*.html")):
        gold += widgets(open(p, encoding="utf-8", errors="replace").read())
    for p in sorted(glob.glob(os.path.join(save, mod, "*.html"))):
        on = widgets(open(p, encoding="utf-8", errors="replace").read())
        dp = os.path.join(_corpus.mdir(CLAUDE, mod), os.path.basename(p))
        off = widgets(open(dp, encoding="utf-8", errors="replace").read()) if os.path.exists(dp) else []
        offkeys = [tuple(d) for _, d in off]
        for lay, drags in on:
            if tuple(drags) in offkeys: offkeys.remove(tuple(drags)); continue      # already built before
            best, bs = None, 0
            for glay, gd in gold:
                s = len(set(drags) & set(gd))
                if s > bs: best, bs = glay, s
            if not best: nomatch += 1; v = "no gold widget shares a drag"
            elif best == lay: agree += 1; v = "AGREE"
            else: dis += 1; v = f"gold {best}"
            print(f"{os.path.basename(p):24s} claude {lay:9s} ({len(drags)} drags) → {v}  [{bs} shared]  e.g. {drags[:3]}")
print(f"\nnew widgets: layout agrees {agree} / differs {dis} / no matching gold widget {nomatch}")
