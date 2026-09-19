#!/usr/bin/env python3
"""Session 27 Round 4 — THE GOLD'S `col-12 col-md-12` COLUMN (MISSING 1407 lines / 685 pages / 276 modules; Claude ships 130).
Where does the gold use it? For every gold `div.col-12.col-md-12` on a PAIRED page: its parent chain (inside an activity box?
a bare section row?), its FIRST child (a widget class / p / hN / table / img / ul), the template / subject; and on Claude's
paired page the column class around the SAME first child (matched by widget class or by the first child's text).
  wsl: python3 _s27_r4_col12md12.py -> _s27_r4_col12md12.out"""
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
def widget_of(n):
    """the widget class marker on n or its descendants (first found)"""
    st = [n]
    while st:
        x = st.pop(0)
        if x.tag != "#text" and (x.toks & WM): return sorted(x.toks & WM)[0]
        st.extend([c for c in x.kids if c.tag != "#text"][:6])
    return None
def first_kid(n):
    for c in n.kids:
        if c.tag != "#text": return c
    return None
def kind_of(col):
    fk = first_kid(col)
    if fk is None: return "empty"
    w = widget_of(fk) or (widget_of(col) if fk.tag == "div" else None)
    if w: return "W:" + w
    return fk.tag + ("." + ".".join(sorted(fk.toks)) if fk.toks and fk.tag == "div" else "")
def box_of(n):
    p = n.parent
    while p is not None:
        if "activity" in p.toks: return "in-activity"
        if p.toks & {"alert", "alertActivity", "important"}: return "in-alert"
        if p.tag == "body" or p.tag == "root": break
        p = p.parent
    return "free"
def walk(n, f):
    for c in n.kids:
        if c.tag != "#text": f(c); walk(c, f)
C = Counter(); BYG = defaultdict(Counter); BYK = defaultdict(Counter); PAIR = defaultdict(Counter); pages = defaultdict(set); mods = defaultdict(set); EX = defaultdict(list)
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"; g = tf + "/" + subj
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
        try:
            gt = TB(); gt.feed(body_source(open(hp, encoding="utf-8", errors="replace").read()))
            ct = TB(); ct.feed(body_source(open(cp, encoding="utf-8", errors="replace").read()))
        except Exception: continue
        # Claude index: widget class -> column labels; first-child text -> column label
        cidx_w = defaultdict(list); cidx_t = {}
        def cw(x):
            if x.tag == "div" and any(t.startswith("col") for t in x.toks):
                fk = first_kid(x)
                if fk is not None:
                    w = widget_of(fk) or (widget_of(x) if fk.tag == "div" else None)
                    if w: cidx_w[w].append(lab(x))
                    t = ftext(fk)[:60]
                    if t and t not in cidx_t: cidx_t[t] = lab(x)
        walk(ct.root, cw)
        def gw(x):
            if x.tag == "div" and x.toks == {"col-12", "col-md-12"}:
                k = kind_of(x); b = box_of(x); par = lab(x.parent) if x.parent else "—"
                key = (b, k)
                C[key] += 1; BYG[g][key] += 1; BYK[k][b] += 1; pages[key].add(hp); mods[key].add(code)
                # Claude's column for the same thing
                cl = "absent"
                fk = first_kid(x)
                if fk is not None:
                    w = widget_of(fk) or (widget_of(x) if fk.tag == "div" else None)
                    if w and cidx_w.get(w): cl = cidx_w[w][0]
                    else:
                        t = ftext(fk)[:60]
                        if t and t in cidx_t: cl = cidx_t[t]
                PAIR[key][cl] += 1
                if len(EX[key]) < 2: EX[key].append(f"{code} {os.path.basename(hp)} parent={par} claude={cl}")
        walk(gt.root, gw)
out = []
def P(s=""): out.append(s); print(s)
tot = sum(C.values())
P(f"gold div.col-12.col-md-12 on paired pages: {tot}")
P("==== by (box, first-child kind) — top 30 ====")
for key, v in C.most_common(30):
    pr = PAIR[key]; tp = sum(pr.values())
    P(f"   {v:5d}  pages {len(pages[key]):4d} mods {len(mods[key]):3d}   {key[0]:12s} {key[1]:34s} claude: " + "  ".join(f"{k} {c} ({c/tp:.2f})" for k, c in pr.most_common(3)))
P()
P("==== per group (n ≥ 15): top kinds ====")
for g, c in sorted(BYG.items(), key=lambda kv: -sum(kv[1].values())):
    t = sum(c.values())
    if t < 15: continue
    P(f"   {g:42s} n={t:4d}  " + "  ".join(f"[{k[0][:6]}/{k[1][:22]}] {v}" for k, v in c.most_common(4)))
P()
for key, ex in list(EX.items())[:30]:
    if C[key] >= 15:
        for e in ex: P(f"   {key}: {e}")
open(os.path.join(OUTPUTS, "_s27_r4_col12md12.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
