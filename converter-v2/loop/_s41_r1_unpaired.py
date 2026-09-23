#!/usr/bin/env python3
"""Session 41 Round 1 PICK — every gold page the skeleton gate leaves UNPAIRED (the gate's own pairs()), with
(a) the share of its body text that exists in the module's Writers Template (derivable) and (b) which Claude page
holds that text (a merged / under-split lesson) or none (no Claude page carries it). Run under WSL from
CONVERTER_V2/reference/tests:  python3 ../../outputs/_s41_r1_unpaired.py > ../../outputs/_s41_r1_unpaired.log"""
import os, sys, re, glob, json, collections, html
sys.path.insert(0, os.getcwd())
import _corpus
from _discrepancy_audit import pairs
from anchor_compare import HUMAN
from anchor_compare import CLAUDE

def text_of(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r"<body[^>]*>(.*)</body>", s, re.S | re.I)
    s = m.group(1) if m else s
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return s

def norm(s):
    s = s.lower()
    s = re.sub(r"[‘’“”'\"`]", "", s)
    s = re.sub(r"[^0-9a-zāēīōū]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def shingles(s, k=6):
    w = s.split()
    return {" ".join(w[i:i + k]) for i in range(0, max(0, len(w) - k + 1))}

def wt_text(code):
    d = _corpus.mdir(HUMAN, code)
    fs = [f for f in glob.glob(os.path.join(d, "*_parsed.txt"))]
    return norm(" ".join(open(f, encoding="utf-8", errors="replace").read() for f in fs)), len(fs)

rows = []
mods = _corpus.gate_mods(CLAUDE) if hasattr(_corpus, "gate_mods") else []
for code in sorted(mods):
    pr = pairs(code)
    hdir = _corpus.mdir(HUMAN, code); cdir = _corpus.mdir(CLAUDE, code)
    if not os.path.isdir(hdir) or not os.path.isdir(cdir): continue
    hf = _corpus.gold_pages(code, sorted(f for f in os.listdir(hdir) if f.endswith(".html")))
    used = {os.path.basename(hp) for _, _, hp in pr}
    un = [f for f in hf if f not in used and re.match(re.escape(code) + r"[_-]\d", f)]
    if not un: continue
    wt, nwt = wt_text(code)
    csh = {}
    for f in os.listdir(cdir):
        if f.endswith(".html"):
            csh[f] = shingles(norm(text_of(os.path.join(cdir, f))))
    for f in un:
        g = shingles(norm(text_of(os.path.join(hdir, f))))
        if not g:
            rows.append((code, f, 0, 0.0, "", 0.0)); continue
        der = sum(1 for x in g if x in wt) / len(g)
        best, bov = "", 0.0
        for cf, cs in csh.items():
            ov = len(g & cs) / len(g)
            if ov > bov: best, bov = cf, ov
        rows.append((code, f, len(g), der, best, bov))

by = collections.defaultdict(list)
for r in rows: by[r[0]].append(r)
print("unpaired gold pages", len(rows), "modules", len(by))
agg = []
for code, rs in by.items():
    dv = [r for r in rs if r[3] >= 0.5]
    hold = [r for r in dv if r[5] >= 0.5]
    agg.append((len(dv), len(hold), code, rs))
agg.sort(key=lambda a: (-a[0], a[2]))
print("pages derivable>=0.5:", sum(a[0] for a in agg), " of them held by a Claude page (>=0.5 of shingles):", sum(a[1] for a in agg))
for nd, nh, code, rs in agg:
    print(f"\n## {code} unpaired={len(rs)} derivable={nd} held-by-claude={nh}")
    for c, f, n, der, best, bov in rs:
        print(f"   {f:28} shingles={n:5d} der={der:.2f} held={bov:.2f} in {best}")
