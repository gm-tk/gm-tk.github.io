#!/usr/bin/env python3
"""Session 27 Round 2 candidate — THE GOLD'S <br> (gold 2169 skeleton lines / Claude 3). Where does the gold put a line break?
Over every gate pair's LIVE body (cv2 dumps / notes / built-widget subtrees carved out on Claude's side; the gold's widget
subtrees excluded by the same class list so both sides are comparable): every <br> with its PARENT label, the parent's parent,
and what precedes / follows it inside the parent (text / img / a / b …). Then the paired view: for each gold <p> that holds
a <br>, does Claude ship the same words as ONE <p> (br dropped), as TWO <p>s (split), or not at all?
  wsl: python3 _s27_r2_brcensus.py → _s27_r2_brcensus.out"""
import os, sys, re, json
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
SKIP = set(WIDGET_MARKERS) | {"cv2-note", "cv2-comment", "acks"}
class N:
    __slots__ = ("tag", "cls", "kids", "parent", "text")
    def __init__(s, tag, cls, parent): s.tag, s.cls, s.kids, s.parent, s.text = tag, cls, [], parent, ""
class TB(HTMLParser):
    def __init__(s):
        super().__init__(); s.root = N("root", "", None); s.cur = s.root; s.skip = 0; s.stack = []
    def handle_starttag(s, tag, attrs):
        a = dict(attrs); cls = " ".join(sorted((a.get("class") or "").split()))
        toks = set(cls.split())
        n = N(tag, cls, s.cur)
        if s.skip == 0: s.cur.kids.append(n)
        if tag in VOID: return
        if toks & SKIP: s.skip += 1
        s.stack.append((n, bool(toks & SKIP))); s.cur = n
    def handle_startendtag(s, tag, attrs): s.handle_starttag(tag, attrs)
    def handle_endtag(s, tag):
        if tag in VOID or not s.stack: return
        n, sk = s.stack.pop()
        if sk: s.skip -= 1
        s.cur = n.parent or s.root
    def handle_data(s, data):
        if s.skip == 0 and data.strip():
            s.cur.kids.append(N("#text", "", s.cur)); s.cur.kids[-1].text = data.strip()
def lab(n):
    if n is None: return "—"
    if n.tag == "#text": return "#text"
    return n.tag + ("." + n.cls.replace(" ", ".") if n.cls else "")
def walk(n, out):
    for i, k in enumerate(n.kids):
        if k.tag == "br":
            prev = n.kids[i - 1] if i > 0 else None; nxt = n.kids[i + 1] if i + 1 < len(n.kids) else None
            # collapse consecutive brs into one record
            if prev is not None and prev.tag == "br": continue
            out.append((lab(n), lab(n.parent), lab(prev), lab(nxt), n))
        walk(k, out)
def ptext(n):
    s = []
    def w(x):
        for k in x.kids:
            if k.tag == "#text": s.append(k.text)
            elif k.tag == "br": s.append("\n")
            else: w(k)
    w(n); return " ".join(" ".join(s).split())
def paras(root):
    out = {}
    def w(x):
        for k in x.kids:
            if k.tag in ("p", "li", "td", "th", "h1", "h2", "h3", "h4", "h5", "h6"):
                t = ptext(k)
                if t: out.setdefault(re.sub(r"\W+", " ", t.lower()).strip(), []).append(k)
            w(k)
    w(root); return out
def fold(t): return re.sub(r"\W+", " ", t.lower()).strip()
CTX = Counter(); CTX_T = defaultdict(Counter); PAIR = Counter(); PAIR_T = defaultdict(Counter); EX = defaultdict(list)
pages_with = set(); gold_br = 0
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
        if re.search(r'acks|acknowledge|glossary', os.path.basename(cp), re.I): continue
        try:
            gt = TB(); gt.feed(body_source(open(hp, encoding="utf-8", errors="replace").read()))
            ct = TB(); ct.feed(body_source(open(cp, encoding="utf-8", errors="replace").read()))
        except Exception: continue
        brs = []; walk(gt.root, brs)
        if not brs: continue
        pages_with.add(hp); gold_br += len(brs)
        cpar = paras(ct.root); cfold_all = " ".join(cpar.keys())
        for par, gp, prev, nxt, node in brs:
            key = (par, prev, nxt); CTX[key] += 1; CTX_T[tf + "/" + subj][key] += 1
            if par in ("p", "li", "td", "th") or par.startswith("p.") or par.startswith("li."):
                # the paired view: the gold paragraph's whole text vs Claude
                full = ptext(node); segs = [s.strip() for s in re.split(r"\s*\n\s*", " ".join(x.text if x.tag == "#text" else ("\n" if x.tag == "br" else ptext(x)) for x in node.kids)) if s.strip()]
                ff = fold(full)
                if ff in cpar: verdict = "ONE-P (br dropped, same words)"
                elif len(segs) >= 2 and all(fold(sg) in cpar for sg in segs): verdict = "SPLIT-P (each line its own p)"
                elif ff and ff[:40] in cfold_all: verdict = "reworded / partial"
                else: verdict = "absent on Claude"
                PAIR[verdict] += 1; PAIR_T[tf + "/" + subj][verdict] += 1
                if len(EX[verdict]) < 3: EX[verdict].append(f"{code} {os.path.basename(hp)}: «{full[:110]}»")
out = []
def P(s=""): out.append(s); print(s)
P(f"gold <br> records (consecutive brs collapsed): {gold_br} on {len(pages_with)} pages")
P("==== by (parent, previous sibling, next sibling) — top 30 ====")
for k, v in CTX.most_common(30): P(f"   {v:5d}  parent {k[0]:32s} prev {k[1]:22s} next {k[2]}")
P()
P("==== the gold paragraph that holds a <br>: what Claude ships (paired) ====")
for k, v in PAIR.most_common(): P(f"   {v:5d}  {k}")
for k, ex in EX.items():
    for e in ex: P(f"      {k[:10]}: {e}")
P()
P("==== per template/subject group (n ≥ 30): verdict shares ====")
for g, c in sorted(PAIR_T.items(), key=lambda kv: -sum(kv[1].values())):
    t = sum(c.values())
    if t < 30: continue
    P(f"   {g:45s} n={t:4d}  " + "  ".join(f"{k.split(' ')[0]} {v/t:.2f}" for k, v in c.most_common()))
open(os.path.join(OUTPUTS, "_s27_r2_brcensus.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
