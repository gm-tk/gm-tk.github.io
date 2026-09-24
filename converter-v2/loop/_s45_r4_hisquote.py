#!/usr/bin/env python3
"""Session 45 Round 4 — the HIS untagged quote: every UNTAGGED WT line that opens with a quotation mark (the r486 discriminator) in the
HIS family (and, for comparison, ANZH / every other prefix), with the NEXT non-empty WT line; where the gold puts each (p.quoteText /
plain p / li / container) and whether the next line is an attribution (`Source:` / dash / `By`) the gold makes p.quoteAck. Per page.
WSL, from outputs/: python3 _s45_r4_hisquote.py [PREFIX_REGEX] > _s45_r4_hisquote.log"""
import os, re, sys, glob, io, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _s45_r1_quote import blocks, norm, container, GOLD, CL
import _corpus
RED = re.compile(r"🔴\[RED TEXT\].*?\[/RED TEXT\]🔴")
TAGGED = re.compile(r"🔴\[RED TEXT\]\s*\[")
QOPEN = re.compile(r"^\s*[\*_]*\s*[“\"‘]")
ACK = re.compile(r"^\s*[\*_(]*\s*(?:[–—-]\s*\S|source\s*:|by\s+[A-Z])", re.I)
pre = re.compile(sys.argv[1] if len(sys.argv) > 1 else r"^HIS")
def gform(g): return "quoteText" if "quoteText" in g["cls"] else "quoteAck" if "quoteAck" in g["cls"] else (g["tag"] + "@" + container(g))
Q = collections.Counter(); A = collections.Counter(); pages = collections.defaultdict(set); ex = collections.defaultdict(list)
CQ = collections.Counter()
for code in _corpus.gate_mods(GOLD):
    if not pre.search(code): continue
    gd = _corpus.mdir(GOLD, code); cd = _corpus.mdir(CL, code)
    wts = [p for p in glob.glob(os.path.join(gd, "*_parsed.txt")) if "writers template" in os.path.basename(p).lower()]
    if not wts: continue
    lines = []
    for w in wts: lines += io.open(w, encoding="utf-8", errors="replace").read().split("\n")
    gbl = blocks(gd); cbl = blocks(cd) if os.path.isdir(cd) else []
    nonempty = [(k, l) for k, l in enumerate(lines) if norm(RED.sub(" ", l).replace("*", ""))]
    for j, (k, ln) in enumerate(nonempty):
        if TAGGED.search(ln): continue
        t = RED.sub(" ", ln).strip()
        n = norm(t.replace("*", ""))
        if len(n) < 12 or not QOPEN.match(t): continue
        s = t.replace("*", "").replace("_", "")
        if not re.search(r"[”\"’]", s[1:]): continue
        g = next((b for b in gbl if n[:40] in b["txt"]), None)
        c = next((b for b in cbl if n[:40] in b["txt"]), None)
        v = gform(g) if g else "ABSENT"
        Q[v] += 1
        if g: pages[v].add(code + "/" + g["page"])
        CQ[(v, (c["tag"] + "@" + container(c)) if c else "ABSENT")] += 1
        if len(ex[v]) < 5: ex[v].append(f"{code} «{t[:70]}»")
        # the next line: an attribution?
        if j + 1 < len(nonempty):
            nl = RED.sub(" ", nonempty[j + 1][1]).strip(); nn = norm(nl.replace("*", ""))
            if ACK.match(nl) and len(nn) >= 6:
                ga = next((b for b in gbl if nn[:40] in b["txt"]), None)
                A[(v, gform(ga) if ga else "ABSENT")] += 1
print("untagged quote-opening lines — the gold's element:")
for v, n in Q.most_common(): print(f"  {n:4d}  {v:24s} pages {len(pages[v]):3d}  {' | '.join(ex[v][:3])}")
print("\n(gold, Claude) pairs:"); [print(f"  {n:4d}  {k}") for k, n in CQ.most_common(12)]
print("\nthe NEXT line is an attribution — (the quote's gold form, the attribution's gold form):")
for k, n in A.most_common(): print(f"  {n:4d}  {k}")
