#!/usr/bin/env python3
"""Session 27 Round 4 — THE SOFT-BREAK `<br>` FORM BY SERIES: the r227 census (`_measure_softbreak`) re-cut per
SERIES (prefix + first digit) over every gate module, with the affected PAGE count per series (gold pages whose
element holds the writer's soft break as a <br>) and the gold <br> parent tags.  wsl: python3 _s27_r4_brseries.py"""
import os, sys, re, json
from collections import Counter, defaultdict
HERE = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
sys.path.insert(0, HERE); sys.path.insert(0, TESTS)
import _measure_softbreak as M
import _corpus
from anchor_compare import CLAUDE
EL = re.compile(r'<(p|li|td|th|h[1-6])\b[^>]*>([\s\S]*?)</\1>', re.I)
def gold_els(code):
    base = M.mdir(code); els = []
    for f in sorted(os.listdir(base)):
        if not f.endswith(".html"): continue
        html = open(os.path.join(base, f), encoding="utf-8", errors="replace").read()
        for m in EL.finditer(html):
            inner = m.group(2)
            els.append((M.fold(re.sub(r"<[^>]+>", " ", inner)), "<br" in inner.lower(), f, m.group(1).lower()))
    return els
codes = sorted(d for d in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))
S = defaultdict(Counter); SP = defaultdict(set); SM = defaultdict(set); PAR = defaultdict(Counter); permod = {}
for c in codes:
    try: brs = M.wt_breaks(c)
    except Exception: continue
    if not brs: continue
    els = gold_els(c)
    series = re.match(r"[A-Z]+\d?", c).group(0)
    r = Counter(); pgs = set()
    for before, after, red in brs:
        if red: r["red"] += 1; continue
        A = M.fold(before.replace("**", "").replace("*", ""))[-28:].strip(); B = M.fold(after.replace("**", "").replace("*", ""))[:28].strip()
        if len(A) < 10 or len(B) < 10: r["short"] += 1; continue
        hit = None
        for i, (txt, hasbr, f, tag) in enumerate(els):
            ia = txt.find(A)
            if ia < 0: continue
            ib = txt.find(B, ia)
            if ib >= 0:
                gap = txt[ia + len(A):ib]
                hit = "br" if hasbr else ("glued" if gap == "" else "spaced")
                if hit == "br": pgs.add(f); PAR[series][tag] += 1
                break
            if i + 1 < len(els) and B in els[i + 1][0][:len(B) + 40]: hit = "split"; break
        r[hit or "unmatched"] += 1
    permod[c] = dict(r)
    for k, v in r.items(): S[series][k] += v
    SP[series] |= {c + "/" + p for p in pgs}; SM[series].add(c)
rows = []
for s, c in S.items():
    dec = c["br"] + c["split"] + c["spaced"] + c["glued"]
    if dec < 8: continue
    rows.append((s, dec, c["br"] / dec, c, len(SP[s]), len(SM[s])))
rows.sort(key=lambda r: -r[1])
print("series   decided  br-share   br/split/spaced/glued | red short unmatched | br-pages mods | gold br parents")
for s, dec, sh, c, np_, nm in rows:
    print(f"{s:8s} {dec:5d}   {sh:.2f}   {c['br']}/{c['split']}/{c['spaced']}/{c['glued']} | {c['red']} {c['short']} {c['unmatched']} | {np_} {nm} | {dict(PAR[s].most_common(4))}")
print()
print("modules with >= 6 br sites:", {c: r for c, r in permod.items() if r.get("br", 0) >= 6})
json.dump(permod, open(os.path.join(HERE, "_s27_r4_brseries.json"), "w"), indent=1)
