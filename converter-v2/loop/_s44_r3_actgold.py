#!/usr/bin/env python3
"""Session 44 Round 3 — for every ACT-label table title (the TSV lines of _s44_r3_acttables.cjs), where the GOLD puts the title
(inside div.activity / free / absent) — per module, split by what follows the table (marker / other). WSL, from outputs/:
python3 _s44_r3_actgold.py _s44_r3_acttables.log"""
import os, re, sys, glob, io, collections
from html.parser import HTMLParser
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GOLD = os.path.join(ROOT, "01-Finalized_Modules_", "Bilingual")
def norm(t): return re.sub(r"[^\wĀ-ſ ]+", "", re.sub(r"\s+", " ", t)).strip().lower()
class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.st = []; s.blocks = []; s.cur = None
    def handle_starttag(s, t, a):
        if t in ("br", "img", "hr", "input", "source", "meta", "link", "audio"): return
        s.st.append((t, dict(a).get("class") or ""))
        if t in ("h1", "h2", "h3", "h4", "h5", "h6", "p"): s.cur = [t, [], list(s.st)]
    def handle_endtag(s, t):
        if s.cur and s.cur[0] == t: s.blocks.append((t, norm("".join(s.cur[1])), s.cur[2])); s.cur = None
        while s.st:
            if s.st.pop()[0] == t: break
    def handle_data(s, d):
        if s.cur: s.cur[1].append(d)
cache = {}
def blocks(code):
    if code not in cache:
        bl = []
        for p in sorted(glob.glob(os.path.join(GOLD, code, "*.html"))):
            x = P(); x.feed(io.open(p, encoding="utf-8", errors="replace").read()); bl += x.blocks
        cache[code] = bl
    return cache[code]
res = collections.defaultdict(collections.Counter)
for ln in io.open(sys.argv[1], encoding="utf-8"):
    if not ln.startswith("TSV\t"): continue
    _, code, reo, eng, nk = ln.rstrip("\n").split("\t")
    hits = []
    for t in (reo, eng):
        n = norm(t)
        if len(n) < 2: continue
        for tag, tx, st in blocks(code):
            if tx == n and tag[0] == "h":
                hits.append("activity" if any(re.search(r"\bactivity\b", c) for _, c in st) else "free")
    w = "activity" if "activity" in hits else ("free" if hits else "absent")
    res[code][(w, "MARKER" if nk.startswith("MARKER") else "other")] += 1
for code, c in sorted(res.items()):
    print(code, dict(c))
