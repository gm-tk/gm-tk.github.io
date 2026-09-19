#!/usr/bin/env python3
"""Session 27 Round 6 — THE GOLD'S EXTRA ACTIVITY BOXES (529 lesson pages where the gold ships more top-level boxes than Claude).
For every gold top-level activity box whose first heading text is NOT the first heading of any Claude box on the paired page:
what is inside it (heading level, the child kinds — prose / widget class / table / image / button / journal h4), the number of
child element kinds, and what Claude ships for that heading text (free h3 in a column / inside another box / absent). By
subject; the writer's opener for the heading where the parsed WT has it.  wsl: python3 _s27_r6_goldboxes.py"""
import os, sys, re
from collections import Counter, defaultdict
from html.parser import HTMLParser
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
HUMAN = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/01-Finalized_Modules_'
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
def ftext(n):
    s = []
    def w(x):
        for c in x.kids:
            if c.tag == "#text": s.append(c.text)
            else: w(c)
    w(n); return re.sub(r"\W+", " ", " ".join(s).lower()).strip()
def boxes(root):
    out = []
    def w(n, inside):
        for c in n.kids:
            if c.tag == "div" and "activity" in c.toks and not ({"clickDropContent", "cv2-interactive"} & c.toks):
                if not inside: out.append(c)
                w(c, True)
            else: w(c, inside)
    w(root, False); return out
def first_heading(n):
    st = list(n.kids)
    while st:
        x = st.pop(0)
        if x.tag == "#text": continue
        if x.tag in ("h1", "h2", "h3", "h4", "h5"): return x.tag, ftext(x)
        st = [c for c in x.kids if c.tag != "#text"] + st
    return "", ""
def kinds(n):
    """the leaf kinds inside a box (widgets collapsed), in order, deduped adjacent"""
    out = []
    def w(x):
        for c in x.kids:
            if c.tag == "#text": continue
            if c.toks & WM: out.append("W:" + sorted(c.toks & WM)[0]); continue
            if "cv2-interactive" in c.toks: out.append("cv2box"); continue
            if c.tag in ("h1", "h2", "h3", "h4", "h5"):
                out.append("goJournal" if "goJournal" in c.toks else c.tag); continue
            if c.tag == "p": out.append("p"); continue
            if c.tag in ("ul", "ol"): out.append(c.tag); continue
            if c.tag == "table": out.append("table"); continue
            if c.tag == "img": out.append("img"); continue
            if c.tag == "a": out.append("a"); continue
            if c.tag == "iframe": out.append("iframe"); continue
            if c.tag == "div" and ({"button", "externalButton"} & c.toks): out.append("button"); continue
            if c.tag == "div" and ({"alert", "alertActivity", "important"} & c.toks): out.append("alert"); continue
            w(c)
    w(n)
    rle = []
    for k in out:
        if not rle or rle[-1] != k: rle.append(k)
    return ",".join(rle)[:70]
def in_box(n):
    p = n.parent
    while p is not None:
        if "activity" in p.toks: return True
        p = p.parent
    return False
def walk(n, f):
    for c in n.kids:
        if c.tag != "#text": f(c); walk(c, f)
C = Counter(); BYG = defaultdict(Counter); pages = defaultdict(set); mods = defaultdict(set); EX = defaultdict(list); CL = Counter(); TOT = 0
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"; g = tf + "/" + subj
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
        if re.search(r"_0_0\.html$", cp): continue
        try:
            gt = TB(); gt.feed(body_source(open(hp, encoding="utf-8", errors="replace").read()))
            ct = TB(); ct.feed(body_source(open(cp, encoding="utf-8", errors="replace").read()))
        except Exception: continue
        gb = boxes(gt.root); cb = boxes(ct.root)
        if len(gb) <= len(cb): continue
        cheads = {first_heading(b)[1] for b in cb}
        # Claude's headings anywhere + their context
        cctx = {}
        def cw(x):
            if x.tag in ("h1", "h2", "h3", "h4", "h5"):
                t = ftext(x)
                if t and t not in cctx: cctx[t] = ("in-box" if in_box(x) else "free") + "-" + x.tag
        walk(ct.root, cw)
        for b in gb:
            lvl, h = first_heading(b)
            if h and h in cheads: continue
            TOT += 1
            k = kinds(b)
            cl = cctx.get(h, "absent") if h else "no-heading"
            key = (cl, k)
            C[key] += 1; BYG[g][cl] += 1; pages[key].add(cp); mods[key].add(code); CL[cl] += 1
            if len(EX[key]) < 3: EX[key].append(f"{code}/{os.path.basename(cp)} #{b.attrs.get('number','')} «{h[:36]}»")
print(f"gold extra boxes on gold-more lesson pages: {TOT}")
print("Claude's rendering of the box's heading:", dict(CL.most_common()))
print("==== (claude context, gold box content) — top 40 ====")
for key, v in C.most_common(40):
    print(f"   {v:4d} pages {len(pages[key]):4d} mods {len(mods[key]):3d}  {key[0]:14s} {key[1]}")
print("==== per group: Claude context of the gold-only boxes ====")
for g, c in sorted(BYG.items(), key=lambda kv: -sum(kv[1].values()))[:14]:
    t = sum(c.values()); print(f"   {g:42s} n={t:4d}  " + "  ".join(f"{k} {v}" for k, v in c.most_common(4)))
for key, ex in EX.items():
    if C[key] >= 12:
        for e in ex: print(f"   {key}: {e}")
