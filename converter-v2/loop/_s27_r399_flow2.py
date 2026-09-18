#!/usr/bin/env python3
"""r399 — after a gold `alert cultural` box: does the next block FLOW inside the same column (a sibling after the box) or does a
new row open? And the same for the r399 ON pages. wsl: python3 _s27_r399_flow.py"""
import os, re, sys
from html.parser import HTMLParser
from collections import Counter
HUMAN = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/01-Finalized_Modules_'
ON = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs/_s27_r399_on'
VOID = {"br", "img", "input", "hr", "meta", "link", "source", "wbr", "area", "base", "col", "embed", "track"}
class N:
    __slots__ = ("tag", "cls", "kids", "parent")
    def __init__(s, tag, cls, parent): s.tag, s.cls, s.kids, s.parent = tag, cls, [], parent
class TB(HTMLParser):
    def __init__(s):
        super().__init__(); s.root = N("root", "", None); s.cur = s.root; s.stack = []
    def handle_starttag(s, tag, attrs):
        a = dict(attrs); n = N(tag, a.get("class") or "", s.cur); s.cur.kids.append(n)
        if tag in VOID: return
        s.stack.append(n); s.cur = n
    def handle_startendtag(s, tag, attrs): s.handle_starttag(tag, attrs)
    def handle_endtag(s, tag):
        if tag in VOID or not s.stack: return
        n = s.stack.pop(); s.cur = n.parent or s.root
def census(root_dir, label):
    A = Counter()
    C = Counter(); NX = Counter()
    for dp, dn, fn in os.walk(root_dir):
        for f in fn:
            if not f.endswith(".html"): continue
            h = open(os.path.join(dp, f), encoding="utf-8", errors="replace").read()
            if "alert cultural" not in h: continue
            t = TB(); t.feed(h)
            def walk(n):
                for k, ch in enumerate(n.kids):
                    if ch.tag == "div" and "cultural" in ch.cls.split():
                        # next element sibling
                        nxt = next((x for x in n.kids[k+1:] if x.tag not in ("#text",)), None)
                        anc = ch.parent; ina = False
                        while anc is not None:
                            if anc.tag == "div" and "activity" in anc.cls.split(): ina = True; break
                            anc = anc.parent
                        A["inside activity" if ina else "outside"] += 1
                        if nxt is None:
                            # box is the last child of its column: does the column's parent row have a following row?
                            C["LAST-in-column (row closes)"] += 1
                        else:
                            C["FLOW (sibling follows in the column)"] += 1; NX[nxt.tag + ("." + nxt.cls.split()[0] if nxt.cls else "")] += 1
                    walk(ch)
            walk(t.root)
    print(f"{label}: " + "; ".join(f"{k} {v}" for k, v in A.most_common()) + " || " + "; ".join(f"{k} {v}" for k, v in C.most_common()) + " | next sibling: " + ", ".join(f"{k} {v}" for k, v in NX.most_common(6)))
census(HUMAN, "GOLD")
census(ON, "ON  ")
