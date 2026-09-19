#!/usr/bin/env python3
"""Session 27 Round 5 — THE GOLD'S `col-8` / `col-4` PAIR (MISSING 236 / 104 pages + 208 / 75 pages; Claude ships 0).
For every gold div.col-8 (exact class set) on a paired page: its parent, its sibling columns, its first child, whether it
sits inside a widget marker (the skeleton collapses those — then it is NOT a gate line), by template / subject; and
Claude's rendering of the same first-child text (the column class around it).  wsl: python3 _s27_r5_col8.py"""
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
from _structural_skeleton import body_source, WIDGET_MARKERS
import _corpus
from anchor_compare import CLAUDE
meta = load_meta()
fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
VOID = {"br", "img", "input", "hr", "meta", "link", "source", "wbr", "area", "base", "col", "embed", "track"}
WM = set(WIDGET_MARKERS)
class N:
    __slots__ = ("tag", "toks", "kids", "parent", "text")
    def __init__(s, tag, cls, parent): s.tag, s.toks, s.kids, s.parent, s.text = tag, set(cls.split()), [], parent, ""
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
    def handle_data(s, data):
        if data.strip():
            t = N("#text", "", s.cur); t.text = data.strip(); s.cur.kids.append(t)
def lab(n): return "—" if n is None else (n.tag + ("." + ".".join(sorted(n.toks)) if n.toks else ""))
def ftext(n):
    s = []
    def w(x):
        for c in x.kids:
            if c.tag == "#text": s.append(c.text)
            else: w(c)
    w(n); return re.sub(r"\W+", " ", " ".join(s).lower()).strip()
def in_widget(n):
    p = n.parent
    while p is not None:
        if p.toks & WM: return sorted(p.toks & WM)[0]
        p = p.parent
    return None
def first_kid(n):
    for c in n.kids:
        if c.tag != "#text": return c
    return None
def walk(n, f):
    for c in n.kids:
        if c.tag != "#text": f(c); walk(c, f)
C = Counter(); BYG = defaultdict(Counter); PAIR = defaultdict(Counter); pages = defaultdict(set); mods = defaultdict(set); EX = defaultdict(list)
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"; g = tf + "/" + subj
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
        try:
            gt = TB(); gt.feed(body_source(open(hp, encoding="utf-8", errors="replace").read()))
            ct = TB(); ct.feed(body_source(open(cp, encoding="utf-8", errors="replace").read()))
        except Exception: continue
        cidx = {}
        def cw(x):
            if x.tag == "div" and any(t.startswith("col") for t in x.toks):
                fk = first_kid(x)
                if fk is not None:
                    t = ftext(fk)[:50]
                    if t and t not in cidx: cidx[t] = lab(x)
        walk(ct.root, cw)
        def gw(x):
            if x.tag == "div" and x.toks == {"col-8"}:
                w = in_widget(x)
                par = x.parent; sibs = [lab(c) for c in par.kids if c.tag == "div"] if par else []
                fk = first_kid(x); fkl = lab(fk) if fk is not None else "empty"
                if fk is not None and fk.tag == "div": fk2 = first_kid(fk); fkl += ">" + (lab(fk2) if fk2 is not None else "")
                key = (w or "free", "|".join(sibs)[:60], fkl[:40])
                C[key] += 1; BYG[g][key] += 1; pages[key].add(hp); mods[key].add(code)
                cl = "absent"
                if fk is not None:
                    t = ftext(fk)[:50]
                    if t and t in cidx: cl = cidx[t]
                PAIR[key][cl] += 1
                if len(EX[key]) < 2: EX[key].append(f"{code} {os.path.basename(hp)} grand={lab(par.parent) if par and par.parent else '—'} claude={cl}")
        walk(gt.root, gw)
print(f"gold div.col-8 (exact) on paired pages: {sum(C.values())}")
for key, v in C.most_common(20):
    pr = PAIR[key]; tp = sum(pr.values())
    print(f"   {v:4d} pages {len(pages[key]):3d} mods {len(mods[key]):3d}  widget={key[0]:12s} sibs={key[1]:48s} first={key[2]:28s} claude: " + "  ".join(f"{k} {c}" for k, c in pr.most_common(2)))
print("==== per group ====")
for g, c in sorted(BYG.items(), key=lambda kv: -sum(kv[1].values()))[:12]:
    t = sum(c.values()); print(f"   {g:42s} n={t:4d}  " + "  ".join(f"[{k[0][:6]}/{k[2][:18]}] {v}" for k, v in c.most_common(3)))
for key, ex in list(EX.items())[:14]:
    if C[key] >= 8:
        for e in ex: print(f"   {key}: {e}")
