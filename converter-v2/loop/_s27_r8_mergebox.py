#!/usr/bin/env python3
"""Session 27 Round 8 — the synthetic box after a writer box: merge / own box / free in the gold (see the tail). wsl: python3 _s27_r8_mergebox.py"""
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

# ---- Session 27 Round 8 — THE SYNTHETIC BOX AFTER A WRITER'S BOX: does the gold MERGE the following standalone widget into
# the preceding numbered box, box it separately, or leave it free?  For every Claude top-level box with NO heading whose leaves
# are a single hand-off widget (the r217 synthetic box), on every paired lesson page: the previous Claude top-level box's number
# N, the gold box N's widget count vs Claude's box N's, whether the gold ships a box with the synthetic box's OWN number, and
# what sits between the previous box and the synthetic box on Claude's page (adjacent or not).
def widgets_in(n):
    c = 0
    def w(x):
        nonlocal c
        for k in x.kids:
            if k.tag == "#text": continue
            if k.toks & WM or "cv2-interactive" in k.toks: c += 1; continue
            w(k)
    w(n); return c
def between(prev, cur):
    """element tags between two top-level boxes in document order (their common ancestor walk, coarse)"""
    seq = []
    def w(x):
        for k in x.kids:
            if k.tag == "#text": continue
            if k is prev: seq.append(("PREV", k)); continue
            if k is cur: seq.append(("CUR", k)); continue
            if k.tag == "div" and "activity" in k.toks and not ({"clickDropContent", "cv2-interactive"} & k.toks): seq.append(("BOX", k)); continue
            if k.tag == "div" and k.toks <= {"row", "col-12", "col-md-8", "col-md-12", "col-md-4", "col-md-6", "paddingR", "paddingL", "offset-md-0", "col-6"}: w(k); continue
            seq.append((k.tag, k))
    return seq
C = Counter(); BYG = defaultdict(Counter); pages = defaultdict(set); mods = defaultdict(set); EX = defaultdict(list); ADJ = Counter(); TOT = 0
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"; g = tf + "/" + subj
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
        if re.search(r"_0_0\.html$", cp): continue
        try:
            gt = TB(); gt.feed(body_source(open(hp, encoding="utf-8", errors="replace").read()))
            ct = TB(); ct.feed(body_source(open(cp, encoding="utf-8", errors="replace").read()))
        except Exception: continue
        cb = boxes(ct.root); gb = boxes(gt.root)
        gnum = {}
        for b in gb:
            k = (b.attrs.get("number") or "").upper()
            if k and k not in gnum: gnum[k] = b
        cnum = {}
        for b in cb:
            k = (b.attrs.get("number") or "").upper()
            if k and k not in cnum: cnum[k] = b
        seq = between(None, None)  # unused
        for idx, b in enumerate(cb):
            lvl, h = first_heading(b)
            if h: continue
            k = kinds(b)
            if k != "W:cv2-interactive" and k != "cv2box": continue
            TOT += 1
            own = (b.attrs.get("number") or "").upper()
            prev = cb[idx - 1] if idx > 0 else None
            pn = (prev.attrs.get("number") or "").upper() if prev is not None else ""
            # what lies between the previous box and this one on Claude's page
            adj = "first-box"
            if prev is not None:
                s = between(prev, b); i0 = [i for i, (t, _) in enumerate(s) if t == "PREV"]; i1 = [i for i, (t, _) in enumerate(s) if t == "CUR"]
                mid = [t for t, _ in s[i0[0] + 1:i1[0]]] if i0 and i1 else ["?"]
                adj = "adjacent" if not mid else "gap:" + ",".join(mid[:4])
            gprev = gnum.get(pn) if pn else None
            cprev_w = widgets_in(prev) if prev is not None else 0
            gprev_w = widgets_in(gprev) if gprev is not None else -1
            if own and own in gnum: verdict = "gold-own-box"
            elif gprev is not None and gprev_w > cprev_w: verdict = "gold-merged-into-prev"
            elif gprev is not None: verdict = "gold-prev-same-widgets"
            elif pn: verdict = "gold-no-prev-box"
            else: verdict = "no-prev-box"
            key = (verdict, "adjacent" if adj == "adjacent" else ("first" if adj == "first-box" else "gap"))
            C[key] += 1; BYG[g][verdict] += 1; pages[key].add(cp); mods[key].add(code); ADJ[adj.split(":")[0] if adj.startswith("gap") else adj] += 1
            if len(EX[key]) < 4: EX[key].append(f"{code}/{os.path.basename(cp)} own=#{own} prev=#{pn} cw={cprev_w} gw={gprev_w} {adj[:40]}")
print(f"synthetic (heading-less single-widget) Claude boxes on paired lesson pages: {TOT}")
for key, v in C.most_common(): print(f"   {v:4d} pages {len(pages[key]):4d} mods {len(mods[key]):3d}  {key}")
print("adjacency:", dict(ADJ.most_common(8)))
print("==== per group ====")
for g, c in sorted(BYG.items(), key=lambda kv: -sum(kv[1].values()))[:16]:
    t = sum(c.values()); print(f"   {g:42s} n={t:4d}  " + "  ".join(f"{k} {v} ({v/t:.2f})" for k, v in c.most_common(4)))
for key, ex in EX.items():
    for e in ex: print(f"   {key}: {e}")
