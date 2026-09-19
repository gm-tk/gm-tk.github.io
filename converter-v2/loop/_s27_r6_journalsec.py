#!/usr/bin/env python3
"""Session 27 Round 6 — THE JOURNAL-BUTTON SECTION: a FREE heading section on Claude's page (an h2–h4 outside any activity box) whose
content, before the next heading, holds a button / anchor whose label names an activity id ("Complete activity 4B in your learning
journal") or the journal ("Go to journal"). Does the gold box that section as an activity — and with the label's id? Also the gold's
box number vs the label's id, by subject.  wsl: python3 _s27_r6_journalsec.py"""
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
def ftext(n):
    s = []
    def w(x):
        for c in x.kids:
            if c.tag == "#text": s.append(c.text)
            else: w(c)
    w(n); return re.sub(r"\W+", " ", " ".join(s).lower()).strip()
def in_box(n):
    p = n.parent
    while p is not None:
        if "activity" in p.toks: return p
        p = p.parent
    return None
def seq(root):
    """document-order list of (node) for headings, buttons, widgets, boxes"""
    out = []
    def w(x):
        for c in x.kids:
            if c.tag == "#text": continue
            out.append(c); w(c)
    w(root); return out
IDRE = re.compile(r"\bactivit(?:y|ies)\s+(\d{1,2}[A-Za-z])\b", re.I)
JRE = re.compile(r"\bjournal\b", re.I)
C = Counter(); BYG = defaultdict(Counter); pages = defaultdict(set); mods = defaultdict(set); EX = defaultdict(list)
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"; g = tf + "/" + subj
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
        if re.search(r"_0_0\.html$", cp): continue
        try:
            gt = TB(); gt.feed(body_source(open(hp, encoding="utf-8", errors="replace").read()))
            ct = TB(); ct.feed(body_source(open(cp, encoding="utf-8", errors="replace").read()))
        except Exception: continue
        # gold: heading text -> (box number or None)
        gmap = {}
        for x in seq(gt.root):
            if x.tag in ("h2", "h3", "h4", "h5"):
                t = ftext(x)
                if t and t not in gmap:
                    b = in_box(x); gmap[t] = (b.attrs.get("number", "") if b is not None else None)
        nodes = seq(ct.root)
        for i, x in enumerate(nodes):
            if x.tag not in ("h2", "h3", "h4") or in_box(x) is not None: continue
            if "cv2-note" in x.toks: continue
            h = ftext(x)
            # scan forward to the next heading or box: collect buttons
            btn = None; kind = None
            for y in nodes[i + 1:]:
                if y.tag in ("h1", "h2", "h3", "h4", "h5") or ("activity" in y.toks): break
                if y.tag == "div" and ({"button", "externalButton"} & y.toks) or (y.tag == "h4" and "goJournal" in y.toks):
                    t = ftext(y); m = IDRE.search(t)
                    if m: btn = m.group(1).upper(); kind = "id-button"; break
                    if JRE.search(t): btn = ""; kind = "journal-button"; break
                if y.tag == "p":
                    m = IDRE.search(ftext(y))
                    if m and JRE.search(ftext(y)): btn = m.group(1).upper(); kind = "id-prose"; break
            if kind is None: continue
            gv = gmap.get(h)
            if gv is None and h not in gmap: verdict = "gold:heading-absent"
            elif gv is None: verdict = "gold:free"
            elif btn and gv.upper() == btn: verdict = "gold:box=id"
            elif btn: verdict = "gold:box≠id"
            else: verdict = "gold:box"
            key = (kind, verdict)
            C[key] += 1; BYG[g][verdict] += 1; pages[key].add(cp); mods[key].add(code)
            if len(EX[key]) < 4: EX[key].append(f"{code}/{os.path.basename(cp)} «{h[:34]}» label-id={btn or '—'} gold={gv}")
print("free heading sections with a journal / activity-id button:", sum(C.values()))
for key, v in C.most_common(): print(f"   {v:4d} pages {len(pages[key]):4d} mods {len(mods[key]):3d}  {key}")
print("==== per group ====")
for g, c in sorted(BYG.items(), key=lambda kv: -sum(kv[1].values()))[:14]:
    t = sum(c.values()); print(f"   {g:42s} n={t:4d}  " + "  ".join(f"{k} {v} ({v/t:.2f})" for k, v in c.most_common(4)))
for key, ex in EX.items():
    for e in ex: print(f"   {key}: {e}")
