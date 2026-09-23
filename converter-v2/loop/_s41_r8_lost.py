#!/usr/bin/env python3
"""Session 41 Round 8 PICK — CONTENT THE CONVERTER DROPS. Per module (gate population): 6-word shingles of the Writers Template
(every _parsed.txt in the gold dir, markup stripped) that the human's pages carry (anywhere in the module) but NO Claude page
carries. Ranks modules by lost shingles and prints a sample of each module's lost runs (joined consecutive WT shingles).
Run under WSL from CONVERTER_V2/reference/tests: python3 ../../outputs/_s41_r8_lost.py > ../../outputs/_s41_r8_lost.log"""
import os, re, sys, glob, html
sys.path.insert(0, os.getcwd())
import _corpus
from anchor_compare import CLAUDE, HUMAN

def norm(s):
    s = s.lower()
    s = re.sub(r"🔴|\[/?red text\]", " ", s)
    s = re.sub(r"\[[^\]]{0,60}\]", " ", s)
    s = re.sub(r"[‘’“”'\"`*_]", "", s)
    s = re.sub(r"[^0-9a-zāēīōū]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()
def page_text(p):
    s = open(p, encoding="utf-8", errors="replace").read()
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", s))
K = 6
def shingles_list(s):
    w = s.split()
    return [" ".join(w[i:i + K]) for i in range(0, max(0, len(w) - K + 1))]

rows = []
for code in sorted(_corpus.gate_mods(CLAUDE)):
    hd, cd = _corpus.mdir(HUMAN, code), _corpus.mdir(CLAUDE, code)
    if not (os.path.isdir(hd) and os.path.isdir(cd)): continue
    wts = [f for f in glob.glob(os.path.join(hd, "*_parsed.txt")) if "media list_parsed" not in f.lower()]
    if not wts: continue
    wt = norm(" ".join(open(f, encoding="utf-8", errors="replace").read() for f in wts))
    wl = shingles_list(wt)
    g = set(shingles_list(norm(" ".join(page_text(p) for p in glob.glob(os.path.join(hd, "*.html"))))))
    c = set(shingles_list(norm(" ".join(page_text(p) for p in glob.glob(os.path.join(cd, "*.html"))))))
    both = [x for x in wl if x in g]
    lost_idx = [i for i, x in enumerate(wl) if x in g and x not in c]
    if not both: continue
    # join consecutive lost shingles into runs
    runs = []; cur = None
    for i in lost_idx:
        if cur and i == cur[1] + 1: cur[1] = i
        else:
            if cur: runs.append(cur)
            cur = [i, i]
    if cur: runs.append(cur)
    runs.sort(key=lambda r: r[0] - r[1])
    samples = [" ".join(wl[r[0]].split()[:K] + [x.split()[-1] for x in wl[r[0] + 1:r[1] + 1]])[:120] for r in runs[:3]]
    rows.append((len(lost_idx), len(both), code, samples))
rows.sort(reverse=True)
tot_l = sum(r[0] for r in rows); tot_b = sum(r[1] for r in rows)
print(f"modules {len(rows)}; WT∩gold shingles {tot_b}; lost (not in any Claude page) {tot_l} ({tot_l / max(1, tot_b):.3f})")
for l, b, code, samples in rows[:45]:
    print(f"{code:9s} lost {l:6d} / {b:6d} ({l / b:.2f})  | " + " || ".join(samples))
