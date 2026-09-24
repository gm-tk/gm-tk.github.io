#!/usr/bin/env python3
"""Session 45 Round 1 (part 2) — the UNTAGGED quote: is there a writer-side shape that predicts the gold's p.quoteText?
(1) for every gold p.quoteText / p.quoteAck whose text sits on an UNTAGGED WT line, print the raw WT line (shape census).
(2) the candidate discriminator over EVERY untagged WT paragraph: Q = the line opens with a quote mark (“ " ‘) and its quoted run
    closes, optionally followed by an attribution (– / — / by / Source), or is followed by a dash/Source attribution line.
    For each Q line found in the gold: gold p.quoteText vs other (the precision), per subject prefix.
WSL, from outputs/: python3 _s45_r1_quote2.py > _s45_r1_quote2.log"""
import os, re, sys, glob, io, collections, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "tests"))
import _corpus
from _s45_r1_quote import blocks, norm, form, container, GOLD, CL
RED = re.compile(r"🔴\[RED TEXT\].*?\[/RED TEXT\]🔴")
def raw(line): return RED.sub(" ", line)
TAGGED = re.compile(r"🔴\[RED TEXT\]\s*\[")
QOPEN = re.compile(r"^\s*[\*_]*\s*[“\"‘]")
DASHACK = re.compile(r"^\s*[\*_]*\s*([–—-]\s*\S|source\s*:|by\s+[A-Z])", re.I)
def is_q(line, nxt):
    t = raw(line).strip()
    if not QOPEN.match(t): return False
    s = t.replace("*", "").replace("_", "")
    # the quoted run closes somewhere in the line
    if not re.search(r"[”\"’]", s[1:]): return False
    return True
shape = collections.Counter(); shex = collections.defaultdict(list)
Q = collections.Counter(); Qfam = collections.defaultdict(collections.Counter); Qex = collections.defaultdict(list)
for code in _corpus.gate_mods(GOLD):
    gd = _corpus.mdir(GOLD, code)
    wts = [p for p in glob.glob(os.path.join(gd, "*_parsed.txt")) if "writers template" in os.path.basename(p).lower()]
    if not wts: continue
    lines = []
    for w in wts: lines += io.open(w, encoding="utf-8", errors="replace").read().split("\n")
    gbl = blocks(gd)
    gq = [g for g in gbl if "quoteText" in g["cls"] or "quoteAck" in g["cls"]]
    nl = [(ln, norm(raw(ln).replace("*", ""))) for ln in lines]
    for g in gq:
        key = g["txt"][:40]
        if len(key) < 8: continue
        for k, (ln, n) in enumerate(nl):
            if key in n:
                if TAGGED.search(ln): break
                t = raw(ln).strip()
                sh = ("qopen" if QOPEN.match(t) else "dash/source" if DASHACK.match(t) else "italic" if t.startswith("*") else "plain")
                sh = form(g) + ":" + sh
                shape[sh] += 1
                if len(shex[sh]) < 5: shex[sh].append(f"{code} «{t[:90]}»")
                break
    # (2) the discriminator's precision
    fam = re.match(r"[A-Z]+", code).group(0)
    for k, (ln, n) in enumerate(nl):
        if TAGGED.search(ln) or not n or len(n) < 12: continue
        nxt = nl[k + 1][0] if k + 1 < len(nl) else ""
        if not is_q(ln, nxt): continue
        key = n[:40]; g = next((b for b in gbl if key in b["txt"]), None)
        if g is None: v = "ABSENT"
        else: v = "quoteText" if "quoteText" in g["cls"] else (g["tag"] + "@" + container(g))
        Q[v] += 1; Qfam[fam][v] += 1
        if len(Qex[v]) < 5: Qex[v].append(f"{code} «{raw(ln).strip()[:80]}»")
print("(1) untagged gold quote blocks by WT shape:")
for k, n in shape.most_common(): print(f"  {n:4d} {k:28s} {' | '.join(shex[k][:3])}")
print("\n(2) untagged WT lines that OPEN with a quote mark (and close it): where the gold puts them")
tot = sum(Q.values())
for k, n in Q.most_common(12): print(f"  {n:5d} {n/tot:5.2f} {k:28s} {' | '.join(Qex[k][:2])}")
print("\n  by family (n >= 10, share quoteText):")
for f, c in sorted(Qfam.items(), key=lambda x: -sum(x[1].values())):
    s = sum(c.values()); p = s - c["ABSENT"]
    if s >= 10: print(f"    {f:8s} n={s:4d} found={p:4d} quoteText={c['quoteText']:4d} share={c['quoteText']/max(p,1):.2f}")
