#!/usr/bin/env python3
"""_s51_r4_unboxform.py — session 51 Round 4 PICK: for every gold activity box Claude renders wholly unboxed
(outputs/_s51_r3_unboxed.tsv), the WRITER'S FORM: the Writers Template line holding the box's first text and the red tags on
that line or the nearest red span within 4 lines before it. Grouped by a tag signature (tags lower-cased, numbers -> N).
WSL, from reference/tests/."""
import os, re, sys, glob, collections
sys.path.insert(0, os.getcwd())
import _corpus
from anchor_compare import HUMAN

fold = lambda t: " ".join(re.sub(r"[^a-z0-9 ]", " ", re.sub(r"🔴\[/?RED TEXT\]🔴|\*", " ", t.lower())).split())
RED = re.compile(r"🔴\[RED TEXT\](.*?)\[/RED TEXT\]🔴")
sig = collections.Counter(); ex = collections.defaultdict(list); mods = collections.defaultdict(set); nf = 0
wtc = {}
for l in open("../../outputs/_s51_r3_unboxed.tsv", encoding="utf-8"):
    code, page, box, nfree, first = l.rstrip("\n").split("\t")[:5]
    if code not in wtc:
        gd = _corpus.mdir(HUMAN, code)
        w = [f for f in glob.glob(os.path.join(gd, "*_parsed.txt")) if "Writers" in f]
        wtc[code] = open(w[0], encoding="utf-8", errors="replace").read().split("\n") if w else []
    lines = wtc[code]; key = fold(first)[:40]
    hit = next((i for i, x in enumerate(lines) if key and key in fold(x)), None)
    if hit is None: nf += 1; continue
    s = None
    for k in range(hit, max(-1, hit - 5), -1):
        reds = RED.findall(lines[k])
        br = [r for r in reds if "[" in r]
        if br: s = " ".join(br); break
    s = re.sub(r"\d+[a-z]?", "N", re.sub(r"\s+", " ", (s or "(no red tag)").lower())).strip()[:70]
    sig[s] += 1; mods[s].add(code)
    if len(ex[s]) < 400: ex[s].append(f"{code} {box}: {first[:50]}")
print("not found in WT:", nf)
for s, n in sig.most_common(40): print(f"{n:4d} {len(mods[s]):3d}m  {s}   e.g. {ex[s][0]}")
if len(sys.argv) > 1:
    for s in sys.argv[1:]:
        print("==", s); c = collections.Counter(" ".join(fold(e.split(": ", 1)[1]).split()[:2]) for e in ex[s])
        print(c.most_common(40))
