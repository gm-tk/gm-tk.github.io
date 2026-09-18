#!/usr/bin/env python3
"""Session 27 Round 3 candidate — THE TWO-CELL LAYOUT TABLE'S GRID WIDTH. Claude's r46 layout-table grid turns a 2-cell writer table
into `row > col-md-6 + col-md-6`; the gold on CEDO502_7_0 stacks two `col-12`s. Over every gate pair: each Claude row holding exactly
TWO text-bearing `col-md-6` columns (no widget inside) → the gold's column form for the FIRST cell's text (its enclosing col's
classes + the sibling count of its row), by template/subject.  wsl: python3 _s27_r3_grid2.py → _s27_r3_grid2.out"""
import os, sys, re
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
from collections import Counter, defaultdict
from html.parser import HTMLParser
meta = load_meta()
fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
VOID = {"br", "img", "input", "hr", "meta", "link", "source", "wbr", "area", "base", "col", "embed", "track"}
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
def ftext(n, k=8):
    s = []
    def w(x):
        for c in x.kids:
            if c.tag == "#text": s.append(c.text)
            elif "cv2-note" not in c.toks: w(c)
    w(n); return " ".join(re.sub(r"\W+", " ", " ".join(s).lower()).split()[:k])
def has_widget(n):
    for c in n.kids:
        if c.tag == "#text": continue
        if c.toks & WIDGET_MARKERS or "cv2-interactive" in c.toks: return True
        if has_widget(c): return True
    return False
def colsig(col):
    return ".".join(sorted(t for t in col.toks if t.startswith("col") or t.startswith("offset") or t.startswith("padding")))
GOLD = defaultdict(Counter); pages = defaultdict(set); mods = defaultdict(set); ALL = Counter(); EX = defaultdict(list)
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"; g = tf + "/" + subj
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
        if re.search(r'acks|acknowledge|glossary', os.path.basename(cp), re.I): continue
        try:
            gt = TB(); gt.feed(body_source(open(hp, encoding="utf-8", errors="replace").read()))
            ct = TB(); ct.feed(body_source(open(cp, encoding="utf-8", errors="replace").read()))
        except Exception: continue
        # gold index: first-8-words of every col's text → (colsig, nsiblings)
        gidx = {}
        def gw(x):
            for c in x.kids:
                if c.tag == "#text": continue
                if c.tag == "div" and any(t.startswith("col") for t in c.toks):
                    row = c.parent; sib = [s for s in row.kids if s.tag == "div" and any(t.startswith("col") for t in s.toks)] if row else [c]
                    ft = ftext(c)
                    if ft and ft not in gidx: gidx[ft] = (colsig(c), len(sib))
                gw(c)
        gw(gt.root)
        def cw(x):
            for c in x.kids:
                if c.tag == "#text": continue
                if c.tag == "div" and "row" in c.toks:
                    cols = [s for s in c.kids if s.tag == "div" and any(t.startswith("col") for t in s.toks)]
                    if len(cols) == 2 and all("col-md-6" in s.toks for s in cols) and not any(has_widget(s) for s in cols) and all(ftext(s, 3) for s in cols):
                        ALL[g] += 1
                        ft = ftext(cols[0])
                        gk = gidx.get(ft)
                        key = (f"{gk[0]} ×{gk[1]}" if gk else "not found")
                        GOLD[g][key] += 1; pages[g].add(hp); mods[g].add(code)
                        if len(EX[(g, key)]) < 2: EX[(g, key)].append(f"{code} {os.path.basename(hp)} «{ft[:40]}»")
                cw(c)
        cw(ct.root)
out = []
def P(s=""): out.append(s); print(s)
P(f"Claude 2×col-md-6 text rows (no widget): {sum(ALL.values())} on {len(set().union(*pages.values()) if pages else set())} pages")
P("==== per group (n ≥ 5): the gold's column form for the first cell's text ====")
for g, c in sorted(GOLD.items(), key=lambda kv: -sum(kv[1].values())):
    t = sum(c.values())
    if t < 5: continue
    P(f"   {g:42s} n={t:4d} pages {len(pages[g]):3d} mods {len(mods[g]):3d}  " + "  ".join(f"[{k}] {v} ({v/t:.2f})" for k, v in c.most_common(4)))
P()
for (g, k), ex in list(EX.items())[:20]:
    for e in ex: P(f"   {g} [{k}]: {e}")
open(os.path.join(OUTPUTS, "_s27_r3_grid2.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
