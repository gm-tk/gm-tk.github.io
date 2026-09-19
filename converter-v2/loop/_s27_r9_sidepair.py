#!/usr/bin/env python3
"""Session 27 Round 9 — THE TWO-COLUMN SIDE PAIR: every `div.row` whose element children are exactly ONE col-md-8 column followed by ONE
col-md-4 / col-md-3 column — the pair's (left class, right class, right's first child kind) on the gold and on Claude, paired pages, by
template / subject. Which class strings does the gold use for the left and the right column when the right holds an alert / alertActivity /
image, and what does Claude ship?  wsl: python3 _s27_r9_sidepair.py"""
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
    __slots__ = ("tag", "toks", "kids", "parent", "attrs", "cls")
    def __init__(s, tag, cls, parent, attrs): s.tag, s.toks, s.kids, s.parent, s.attrs, s.cls = tag, set(cls.split()), [], parent, attrs, " ".join(sorted(cls.split()))
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
def first_kind(n):
    for c in n.kids:
        if c.tag == "div" and (c.toks & {"alert", "alertActivity", "alertImage", "whakatauki", "supervisor", "activity", "row"}):
            return "div." + ".".join(sorted(c.toks & {"alert", "top", "solid", "alertActivity", "alertImage", "whakatauki", "supervisor", "activity", "row"}))
        if c.tag in ("img", "p", "h2", "h3", "h4", "h5", "ul", "a", "table", "iframe"): return c.tag
        if c.tag == "div": return "div." + ".".join(sorted(c.toks))[:30]
    return "empty"
def rows(root, out):
    for c in root.kids:
        if c.tag == "div" and "row" in c.toks:
            kids = [k for k in c.kids if k.tag == "div"]
            if len(kids) == 2 and any(t.startswith("col-md-8") for t in kids[0].toks) and any(t in ("col-md-4", "col-md-3") for t in kids[1].toks):
                out.append((kids[0].cls, kids[1].cls, first_kind(kids[1])))
        rows(c, out)
G = Counter(); Cl = Counter(); GR = Counter(); CR = Counter(); GBY = defaultdict(Counter); CBY = defaultdict(Counter); gp = set(); cp_ = set()
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"; g = tf + "/" + subj
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
        try:
            gt = TB(); gt.feed(body_source(open(hp, encoding="utf-8", errors="replace").read()))
            ct = TB(); ct.feed(body_source(open(cp, encoding="utf-8", errors="replace").read()))
        except Exception: continue
        go = []; co = []; rows(gt.root, go); rows(ct.root, co)
        for l, r, k in go: G[(l, r, k)] += 1; GR[(r, k)] += 1; GBY[g][(l, r, k)] += 1; gp.add(hp)
        for l, r, k in co: Cl[(l, r, k)] += 1; CR[(r, k)] += 1; CBY[g][(l, r, k)] += 1; cp_.add(cp)
print(f"GOLD two-column side pairs: {sum(G.values())} on {len(gp)} pages;  CLAUDE: {sum(Cl.values())} on {len(cp_)} pages")
print("==== GOLD top 20 (left | right | right's first kind) ====")
for k, v in G.most_common(20): print(f"   {v:4d}  {k[0]:44s} | {k[1]:44s} | {k[2]}")
print("==== CLAUDE top 12 ====")
for k, v in Cl.most_common(12): print(f"   {v:4d}  {k[0]:44s} | {k[1]:44s} | {k[2]}")
print("==== GOLD by right-kind: the right column's class share ====")
for kind in ("div.alert.top", "div.alert", "div.alertActivity", "img", "div.alert.solid"):
    tot = sum(v for (r, k), v in GR.items() if k == kind)
    if not tot: continue
    print(f"   {kind:18s} n={tot:4d}  " + "  ".join(f"{r} {v} ({v/tot:.2f})" for (r, k), v in sorted(((rk, v) for rk, v in GR.items() if rk[1] == kind), key=lambda x: -x[1])[:5]))
print("==== GOLD left-column class when the right is div.alert.top / div.alertActivity ====")
for kind in ("div.alert.top", "div.alertActivity", "img"):
    LC = Counter()
    for (l, r, k), v in G.items():
        if k == kind: LC[l] += v
    tot = sum(LC.values())
    if tot: print(f"   {kind:18s} n={tot:4d}  " + "  ".join(f"{l} {v} ({v/tot:.2f})" for l, v in LC.most_common(4)))
print("==== per group (gold): the dominant full pair for alert.top ====")
for g, c in sorted(GBY.items(), key=lambda kv: -sum(kv[1].values()))[:12]:
    sub = Counter({k: v for k, v in c.items() if k[2] == "div.alert.top"}); t = sum(sub.values())
    if t >= 5: print(f"   {g:42s} n={t:4d}  " + "  ".join(f"[{k[0]} | {k[1]}] {v} ({v/t:.2f})" for k, v in sub.most_common(2)))
