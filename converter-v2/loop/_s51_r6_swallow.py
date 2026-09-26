#!/usr/bin/env python3
"""_s51_r6_swallow.py — session 51 Round 6 PICK: gold blocks the human keeps FREE (body:free, any panel) that Claude has only inside
a hand-off box (body:widget:cv2-interactive) on the paired page — the widget walk swallowed them. Each block is mapped to its
Writers Template line; grouped by the red tag signature on that line (or the nearest within 3 lines above) and by the block tag.
WSL, from reference/tests/."""
import os, re, sys, glob, collections
sys.path.insert(0, os.getcwd()); sys.path.append("../../outputs")
import _corpus
import _placement_census as PC
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, HUMAN

fold = lambda t: " ".join(re.sub(r"[^a-z0-9 ]", " ", re.sub(r"🔴\[/?RED TEXT\]🔴|\*", " ", t.lower())).split())
RED = re.compile(r"🔴\[RED TEXT\](.*?)\[/RED TEXT\]🔴")
sig = collections.Counter(); mods = collections.defaultdict(set); pages = collections.defaultdict(set); ex = collections.defaultdict(list)
tot = 0
for code in sorted(_corpus.gate_mods(CLAUDE)):
    gd = _corpus.mdir(HUMAN, code)
    w = [f for f in glob.glob(os.path.join(gd, "*_parsed.txt")) if "Writers" in f]
    lines = open(w[0], encoding="utf-8", errors="replace").read().split("\n") if w else []
    flines = [fold(x) for x in lines]
    for n, cp, hp in pairs(code):
        g = PC.parse(hp); c = PC.parse(cp)
        cw = [b for b in c if "cv2-interactive" in b[3]]
        cfree = [b for b in c if "cv2-interactive" not in b[3]]
        for b in g:
            if not re.search(r"(^|:)free", b[3]) or len(b[1].split()) < 4: continue
            if any(PC.jacc(x[1], b[1]) >= 0.6 for x in cfree): continue
            if not any(PC.jacc(x[1], b[1]) >= 0.6 for x in cw): continue
            tot += 1
            key = b[1][:40]
            hit = next((i for i, x in enumerate(flines) if key and key in x), None)
            s = "(not in WT)"
            if hit is not None:
                s = "(no red tag)"
                for k in range(hit, max(-1, hit - 4), -1):
                    br = [r for r in RED.findall(lines[k]) if "[" in r]
                    if br: s = ("same-line " if k == hit else "above ") + re.sub(r"\d+[a-z]?", "N", re.sub(r"\s+", " ", " ".join(br).lower())).strip()[:60]; break
            s = f"{b[0]} | {s}"
            sig[s] += 1; mods[s].add(code); pages[s].add(os.path.basename(cp))
            if len(ex[s]) < 3: ex[s].append(f"{os.path.basename(cp)}: {b[2][:60]}")
print("gold-free blocks Claude has only inside a hand-off box:", tot)
for s, n in sig.most_common(40): print(f"{n:4d} {len(pages[s]):3d}p {len(mods[s]):3d}m  {s}   e.g. {ex[s][0]}")
