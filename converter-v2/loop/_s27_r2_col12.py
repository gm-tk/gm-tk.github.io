#!/usr/bin/env python3
"""Session 27 Round 2 candidate — THE FULL-WIDTH COLUMN `div.col-12.col-md-12` (gold 1514 skeleton lines / Claude 130).
Over every gate pair's live body: every gold column whose class set is exactly {col-12, col-md-12} — its parent, its FIRST
child label (what it holds), by template / subject; and for the same FIRST-CHILD KIND across the gold, the column-class
share (col-md-12 vs col-md-8 vs col-12 vs other) — is the width predicted by the content? Then the paired view for the
non-widget kinds: the gold's col-md-12 holding X vs Claude's column holding the same X (matched by the child's text).
  wsl: python3 _s27_r2_col12.py → _s27_r2_col12.out"""
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
    __slots__ = ("tag", "cls", "toks", "kids", "parent", "text")
    def __init__(s, tag, cls, parent): s.tag, s.cls, s.toks, s.kids, s.parent, s.text = tag, cls, set(cls.split()), [], parent, ""
class TB(HTMLParser):
    def __init__(s):
        super().__init__(); s.root = N("root", "", None); s.cur = s.root; s.stack = []
    def handle_starttag(s, tag, attrs):
        a = dict(attrs); cls = " ".join(sorted((a.get("class") or "").split()))
        n = N(tag, cls, s.cur); s.cur.kids.append(n)
        if tag in VOID: return
        s.stack.append(n); s.cur = n
    def handle_startendtag(s, tag, attrs): s.handle_starttag(tag, attrs)
    def handle_endtag(s, tag):
        if tag in VOID or not s.stack: return
        n = s.stack.pop(); s.cur = n.parent or s.root
    def handle_data(s, data):
        if data.strip():
            t = N("#text", "", s.cur); t.text = data.strip(); s.cur.kids.append(t)
def lab(n):
    if n is None: return "—"
    if n.tag == "#text": return "#text"
    return n.tag + ("." + n.cls.replace(" ", ".") if n.cls else "")
def kind(n):
    """the first ELEMENT child's kind: a widget marker name if it is one, else its label"""
    for k in n.kids:
        if k.tag == "#text": return "#text"
        w = k.toks & WIDGET_MARKERS
        if w: return "WIDGET:" + sorted(w)[0]
        if k.toks & {"cv2-interactive"}: return "WIDGET:cv2"
        return lab(k)
    return "(empty)"
def colkind(n):
    t = n.toks
    if "col-md-12" in t and "col-12" in t and len(t) == 2: return "col-12.col-md-12"
    if "col-md-8" in t: return "col-md-8"
    if t == {"col-12"}: return "col-12"
    if any(x.startswith("col-md-") for x in t): return "col-md-other"
    return "col-other"
def ftext(n):
    s = []
    def w(x):
        for k in x.kids:
            if k.tag == "#text": s.append(k.text)
            else: w(k)
    w(n); return re.sub(r"\W+", " ", " ".join(s).lower()).strip()[:80]
COL12 = Counter(); COL12_T = defaultdict(Counter); PAR = Counter()
BYKIND = defaultdict(Counter)   # kind -> colkind -> count (gold, all columns)
PAIRED = defaultdict(Counter)   # kind -> claude colkind for the same first-child text
pages = set(); mods = set()
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
        if re.search(r'acks|acknowledge|glossary', os.path.basename(cp), re.I): continue
        try:
            gt = TB(); gt.feed(body_source(open(hp, encoding="utf-8", errors="replace").read()))
            ct = TB(); ct.feed(body_source(open(cp, encoding="utf-8", errors="replace").read()))
        except Exception: continue
        # index Claude's columns by their first-child text
        cidx = {}
        def cw(x, inside):
            for k in x.kids:
                if k.tag == "#text": continue
                if k.tag == "div" and any(t.startswith("col") for t in k.toks) and "row" not in k.toks:
                    ft = ftext(k)
                    if ft and ft not in cidx: cidx[ft] = colkind(k)
                cw(k, inside)
        cw(ct.root, False)
        def gw(x):
            for k in x.kids:
                if k.tag == "#text": continue
                if k.tag == "div" and any(t.startswith("col") for t in k.toks) and "row" not in k.toks:
                    ck = colkind(k); kd = kind(k)
                    BYKIND[kd][ck] += 1
                    if ck == "col-12.col-md-12":
                        COL12[kd] += 1; COL12_T[tf + "/" + subj][kd] += 1; PAR[lab(k.parent)] += 1
                        pages.add(hp); mods.add(code)
                        ft = ftext(k)
                        if ft in cidx: PAIRED[kd][cidx[ft]] += 1
                        else: PAIRED[kd]["(no Claude column with this text)"] += 1
                gw(k)
        gw(gt.root)
out = []
def P(s=""): out.append(s); print(s)
P(f"gold col-12.col-md-12 columns: {sum(COL12.values())} on {len(pages)} pages / {len(mods)} modules; parents {PAR.most_common(5)}")
P("==== by FIRST CHILD (what the full-width column holds) — gold count; the same kind's column-class share across ALL gold columns; the paired Claude column for the same text ====")
for kd, v in COL12.most_common(40):
    tot = sum(BYKIND[kd].values()); bk = BYKIND[kd]
    share = " ".join(f"{k}={c}({c/tot:.2f})" for k, c in bk.most_common(4))
    pr = PAIRED[kd]; pt = sum(pr.values())
    ps = " ".join(f"{k}={c}" for k, c in pr.most_common(4))
    P(f"   {v:5d}  {kd:38s} | all-gold {share} | paired {ps}")
P()
P("==== per template/subject group (n ≥ 20 col-md-12 columns): the kinds held ====")
for g, c in sorted(COL12_T.items(), key=lambda kv: -sum(kv[1].values())):
    t = sum(c.values())
    if t < 20: continue
    P(f"   {g:45s} n={t:4d}  " + "  ".join(f"{k} {v}" for k, v in c.most_common(6)))
open(os.path.join(OUTPUTS, "_s27_r2_col12.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
