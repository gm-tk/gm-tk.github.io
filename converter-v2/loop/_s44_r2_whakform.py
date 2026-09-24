#!/usr/bin/env python3
"""Session 44 Round 2 — the GOLD's whakataukī form in a set of modules (default: the Bilingual folder), and Claude's for the same
page: the ancestor chain of every div.whakatauki, its child signatures, and the next sibling after its wrapper; for Claude, the
same, or — when Claude has no box — the elements around the proverb text. WSL, from outputs/: python3 _s44_r2_whakform.py [CODE…]"""
import os, re, sys, glob, io
from html.parser import HTMLParser
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GOLD = os.path.join(ROOT, "01-Finalized_Modules_"); CL = os.path.join(ROOT, "01-Claude_Modules_")
VOID = {"br", "img", "hr", "input", "source", "meta", "link", "audio", "wbr"}
class N:
    def __init__(s, tag, cls, parent): s.tag, s.cls, s.parent, s.kids, s.text = tag, cls, parent, [], []
    def sig(s): return s.tag + ("." + ".".join(s.cls.split()) if s.cls else "")
    def txt(s): return re.sub(r"\s+", " ", "".join(s.text) + " ".join(k.txt() for k in s.kids)).strip()
class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.root = N("root", "", None); s.cur = s.root
    def handle_starttag(s, t, a):
        n = N(t, dict(a).get("class") or "", s.cur); s.cur.kids.append(n)
        if t not in VOID: s.cur = n
    def handle_endtag(s, t):
        x = s.cur
        while x is not s.root and x.tag != t: x = x.parent
        if x is not s.root: s.cur = x.parent
    def handle_data(s, d): s.cur.text.append(d)
def walk(n):
    yield n
    for k in n.kids: yield from walk(k)
def chain(n):
    out = []
    while n.parent and n.parent.tag != "root":
        n = n.parent
        if n.tag in ("body", "html"): break
        out.append(n.sig())
    return " < ".join(out[:5])
codes = sys.argv[1:] or [os.path.basename(d) for d in sorted(glob.glob(os.path.join(GOLD, "Bilingual", "*")))]
for code in codes:
    gd = glob.glob(os.path.join(GOLD, "*", code)); cd = glob.glob(os.path.join(CL, "*", code))
    for d, who in ((gd[0] if gd else None, "GOLD"), (cd[0] if cd else None, "CLAUDE")):
        if not d: continue
        for p in sorted(glob.glob(os.path.join(d, "*.html"))):
            s = io.open(p, encoding="utf-8", errors="replace").read()
            if "whakatauki" not in s and "Whakataukī" not in s and "Proverb" not in s: continue
            x = P(); x.feed(s)
            for n in walk(x.root):
                if n.tag == "div" and "whakatauki" in n.cls.split():
                    kids = " ".join(k.sig() + ("(" + ",".join(g.sig() for g in k.kids) + ")" if k.kids and k.tag == "p" else "") for k in n.kids)
                    w = n.parent; sib = None
                    if w and w.parent:
                        i = w.parent.kids.index(w); sib = w.parent.kids[i + 1].sig() if i + 1 < len(w.parent.kids) else "—"
                    print(f"{who:6} {code:7} {os.path.basename(p):18} BOX  < {chain(n)}  | kids: {kids[:90]} | next-after-wrapper: {sib}")
                elif who == "CLAUDE" and n.tag in ("h2", "h3", "h4", "h5") and re.search(r"whakatauk|proverb", n.txt(), re.I):
                    par = n.parent; i = par.kids.index(n)
                    nxt = " ".join(k.sig() for k in par.kids[i:i + 7])
                    print(f"{who:6} {code:7} {os.path.basename(p):18} HEAD «{n.txt()[:30]}» < {chain(n)} | run: {nxt}")
