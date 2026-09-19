#!/usr/bin/env python3
"""Session 27 Round 6 — CLAUDE'S NOTE-ONLY ACTIVITY BOXES: every Claude top-level activity box whose whole content is red notes
(cv2-note / cv2-comment paragraphs) inside the standard row > col-12 — no heading, no prose, no widget, no table, no image.
Count / pages / modules, the note kinds, the box number, and the gold's box count relation on that page.  wsl: python3 _s27_r6_emptybox.py"""
import os, sys, re
from collections import Counter, defaultdict
from html.parser import HTMLParser
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS); sys.path.insert(1, OUTPUTS)
from _discrepancy_audit import pairs
from _measure_ceiling import load_meta
from _structural_skeleton import body_source
import _corpus
from anchor_compare import CLAUDE
meta = load_meta()
fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
VOID = {"br", "img", "input", "hr", "meta", "link", "source", "wbr", "area", "base", "col", "embed", "track"}
class N:
    __slots__ = ("tag", "toks", "kids", "parent", "attrs", "text")
    def __init__(s, tag, cls, parent, attrs): s.tag, s.toks, s.kids, s.parent, s.attrs, s.text = tag, set(cls.split()), [], parent, attrs, ""
class TB(HTMLParser):
    def __init__(s):
        super().__init__(); s.root = N("root", "", None, {}); s.cur = s.root; s.stack = []
    def handle_starttag(s, tag, attrs):
        a = dict(attrs); n = N(tag, a.get("class") or "", s.cur, a); s.cur.kids.append(n)
        if tag in VOID: return
        s.stack.append(n); s.cur = n
    def handle_startendtag(s, tag, attrs): s.handle_starttag(tag, attrs)
    def handle_endtag(s, tag):
        if tag in VOID or not s.stack: return
        n = s.stack.pop(); s.cur = n.parent or s.root
    def handle_data(s, data):
        if data.strip():
            t = N("#text", "", s.cur, {}); t.text = data.strip(); s.cur.kids.append(t)
def boxes(root):
    out = []
    def w(n, inside):
        for c in n.kids:
            if c.tag == "div" and "activity" in c.toks and not ({"clickDropContent", "cv2-interactive"} & c.toks):
                if not inside: out.append(c)
                w(c, True)
            else: w(c, inside)
    w(root, False); return out
def leaves(n):
    out = []
    def w(x):
        for c in x.kids:
            if c.tag == "#text": continue
            if c.tag == "div" and c.toks <= {"row", "col-12", "col-md-8", "col-md-12"}: w(c); continue
            out.append(c)
    w(n); return out
def ftext(n):
    s = []
    def w(x):
        for c in x.kids:
            if c.tag == "#text": s.append(c.text)
            else: w(c)
    w(n); return " ".join(s)
C = Counter(); pages = set(); mods = set(); KIND = Counter(); REL = Counter(); EX = []
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"; g = tf + "/" + subj
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
        try:
            ct = TB(); ct.feed(body_source(open(cp, encoding="utf-8", errors="replace").read()))
            gt = TB(); gt.feed(body_source(open(hp, encoding="utf-8", errors="replace").read()))
        except Exception: continue
        cb = boxes(ct.root); gb = boxes(gt.root)
        for b in cb:
            lv = leaves(b)
            if not lv or any(not (x.tag == "p" and ({"cv2-note", "cv2-comment"} & x.toks)) for x in lv): continue
            t = ftext(b)
            k = "no-content-flag" if "no content captured" in t else ("writers-note" if "Writers Note" in t else ("todo" if "To Do" in t else "other-note"))
            C[g] += 1; KIND[k] += 1; pages.add(cp); mods.add(code)
            REL["gold-fewer" if len(gb) < len(cb) else ("equal" if len(gb) == len(cb) else "gold-more")] += 1
            EX.append(f"{code}/{os.path.basename(cp)} #{b.attrs.get('number','')} {k} «{t[:70]}»")
print(f"note-only activity boxes: {sum(C.values())} on {len(pages)} pages / {len(mods)} modules; kinds {dict(KIND)}; page box-count relation {dict(REL)}")
for g, v in C.most_common(12): print(f"   {g:42s} {v}")
for e in EX: print("   " + e)
