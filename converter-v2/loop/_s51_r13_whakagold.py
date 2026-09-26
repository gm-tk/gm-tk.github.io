#!/usr/bin/env python3
"""_s51_r13_whakagold.py — session 51 Round 13 PICK: every gold `div.whakatauki` box, per module and page — its paragraphs' text,
whether it sits in a bilingual (reo) template dir, and where it sits (the box's parent chain + its position among the col's children).
Writes _s51_r13_whakagold.tsv (code, page, template dir, n paragraphs, p1, p2, parent classes). WSL, from reference/tests/."""
import os, re, sys, collections
sys.path.insert(0, os.getcwd())
import _corpus
from html.parser import HTMLParser
G = os.path.join(os.getcwd(), "..", "..", "..", "01-Finalized_Modules_")

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.stack = []; s.boxes = []; s.cur = None; s.pdepth = None; s.buf = []
    def handle_starttag(s, t, a):
        cls = (dict(a).get("class") or "").split()
        if t in ("br", "img", "hr", "input", "meta", "link", "source"):
            return
        s.stack.append((t, cls))
        if t == "div" and "whakatauki" in cls and s.cur is None:
            s.cur = {"parent": [c for (_t, cc) in s.stack[:-1] for c in cc if c in ("row", "col", "col-12", "col-md-8", "col-md-4", "activity", "alert", "tab-pane", "card-body", "rhs")][-3:], "ps": []}
            s.cur["depth"] = len(s.stack)
        elif s.cur is not None and t == "p":
            s.pdepth = len(s.stack); s.buf = []
    def handle_endtag(s, t):
        if not s.stack:
            return
        if s.cur is not None and s.pdepth == len(s.stack) and t == "p":
            s.cur["ps"].append(" ".join("".join(s.buf).split())); s.pdepth = None
        if s.cur is not None and len(s.stack) == s.cur["depth"] and t == "div":
            s.boxes.append(s.cur); s.cur = None
        s.stack.pop()
    def handle_data(s, d):
        if s.pdepth is not None:
            s.buf.append(d)

rows = []; fam = collections.Counter()
for tdir in sorted(os.listdir(G)):
    tp = os.path.join(G, tdir)
    if not os.path.isdir(tp):
        continue
    for code in sorted(os.listdir(tp)):
        cp = os.path.join(tp, code)
        if not os.path.isdir(cp):
            continue
        for f in sorted(os.listdir(cp)):
            if not f.endswith(".html"):
                continue
            try:
                h = open(os.path.join(cp, f), encoding="utf-8", errors="replace").read()
            except Exception:
                continue
            if "whakatauki" not in h:
                continue
            p = P(); p.feed(h)
            for b in p.boxes:
                ps = b["ps"] + ["", ""]
                rows.append((code, f, tdir, len(b["ps"]), ps[0][:70], ps[1][:70], "/".join(b["parent"])))
                fam[tdir] += 1
out = os.path.join(os.getcwd(), "..", "..", "outputs", "_s51_r13_whakagold.tsv")
with open(out, "w", encoding="utf-8") as fh:
    for r in rows:
        fh.write("\t".join(map(str, r)) + "\n")
print("boxes", len(rows), "modules", len({r[0] for r in rows}), "by template dir", dict(fam))
print("paragraph counts", collections.Counter(r[3] for r in rows).most_common(6))
print("parents", collections.Counter(r[6] for r in rows).most_common(8))
