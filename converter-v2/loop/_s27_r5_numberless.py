#!/usr/bin/env python3
"""Session 27 Round 5 — CLAUDE'S NUMBERLESS ACTIVITY BOXES (label census: `div.activity` EXTRA 529 lines / 265 pages / 115
modules; the gold ships 6). For every Claude div.activity WITHOUT a number attribute on a paired page: its class tokens, its
first heading text, the page kind (overview / lesson / single-file), the writer's opener form if recoverable from the
box's first heading; and the gold's box holding the same heading text — numbered (which id, and is it the NEXT letter in
the page's sequence?) / un-numbered / no box (the gold's element for that text).  wsl: python3 _s27_r5_numberless.py"""
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
    __slots__ = ("tag", "toks", "kids", "parent", "text", "attrs")
    def __init__(s, tag, cls, parent, attrs): s.tag, s.toks, s.kids, s.parent, s.text, s.attrs = tag, set(cls.split()), [], parent, "", attrs
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
def ftext(n):
    s = []
    def w(x):
        for c in x.kids:
            if c.tag == "#text": s.append(c.text)
            else: w(c)
    w(n); return re.sub(r"\W+", " ", " ".join(s).lower()).strip()
def first_heading(n):
    st = list(n.kids)
    while st:
        x = st.pop(0)
        if x.tag == "#text": continue
        if x.tag in ("h1", "h2", "h3", "h4", "h5"): return ftext(x)
        if "activity" in x.toks and x is not n: continue
        st = [c for c in x.kids if c.tag != "#text"] + st
    return ""
def widget_in(n):
    st = list(n.kids)
    while st:
        x = st.pop(0)
        if x.tag == "#text": continue
        if x.toks & WM: return sorted(x.toks & WM)[0]
        if "cv2-interactive" in x.toks: return "cv2box"
        st.extend([c for c in x.kids if c.tag != "#text"])
    return None
def walk(n, f):
    for c in n.kids:
        if c.tag != "#text": f(c); walk(c, f)
C = Counter(); BYG = defaultdict(Counter); pages = defaultdict(set); mods = defaultdict(set); EX = defaultdict(list); GOLDID = Counter()
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"; g = tf + "/" + subj
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
        try:
            gt = TB(); gt.feed(body_source(open(hp, encoding="utf-8", errors="replace").read()))
            ct = TB(); ct.feed(body_source(open(cp, encoding="utf-8", errors="replace").read()))
        except Exception: continue
        pk = "overview" if re.search(r"_0_0\.html$", cp) else "lesson"
        gboxes = []   # (number, first heading, order)
        def gw(x):
            if x.tag == "div" and "activity" in x.toks: gboxes.append((x.attrs.get("number", ""), first_heading(x)))
        walk(gt.root, gw)
        gheads = {}
        def gh(x):
            if x.tag in ("h1", "h2", "h3", "h4", "h5", "p", "b"):
                t = ftext(x)
                if t and t not in gheads: gheads[t] = x.tag
        walk(gt.root, gh)
        cseq = []
        def cw(x):
            if x.tag == "div" and "activity" in x.toks:
                num = x.attrs.get("number", ""); cseq.append(num)
                if num: return
                h = first_heading(x); w = widget_in(x)
                toks = ".".join(sorted(x.toks - {"activity"})) or "plain"
                gv = "gold:none"
                for gn, ghd in gboxes:
                    if h and ghd == h: gv = "gold:box#" + (gn if gn else "none"); break
                if gv == "gold:none" and h and h in gheads: gv = "gold:free-" + gheads[h]
                if gv == "gold:none" and not h: gv = "gold:?(no heading)"
                kind = "numbered" if re.match(r"^\d{1,2}[a-z]?$", gv.split("#")[-1]) else gv.split("#")[0] if "#" in gv else gv
                key = (pk, toks, "widget" if w else "prose", kind)
                C[key] += 1; BYG[g][key] += 1; pages[key].add(cp); mods[key].add(code)
                if "#" in gv: GOLDID[gv.split("#")[-1][:1].isdigit()] += 1
                if len(EX[key]) < 3: EX[key].append(f"{code}/{os.path.basename(cp)} «{h[:40]}» {gv} w={w}")
        walk(ct.root, cw)
print(f"Claude numberless activity boxes on paired pages: {sum(C.values())}")
print("==== (page kind, box classes, content, gold verdict) ====")
for key, v in C.most_common(28):
    print(f"   {v:4d} pages {len(pages[key]):3d} mods {len(mods[key]):3d}  {key}")
print("==== per group ====")
for g, c in sorted(BYG.items(), key=lambda kv: -sum(kv[1].values()))[:14]:
    t = sum(c.values()); print(f"   {g:42s} n={t:4d}  " + "  ".join(f"[{k[0][:3]}/{k[1][:14]}/{k[2][:4]}/{k[3][:12]}] {v}" for k, v in c.most_common(3)))
print()
for key, ex in EX.items():
    if C[key] >= 12:
        for e in ex: print(f"   {key}: {e}")
