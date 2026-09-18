#!/usr/bin/env python3
"""Session 27 Round 3 candidate — THE PADDED SIDEBAR PAIR. Every ROW holding exactly two columns [a col-md-8 + a col-md-4] on the
gate pairs' live body: the class tokens of each column (paddingR on the content col? paddingL / offset-md-0 on the side col?), the
side col's first child (alertActivity / alert top / alertImage / other), gold vs Claude, by template/subject; paired by the side
column's opening words → what Claude ships for the same box.  wsl: python3 _s27_r3_sidepad.py → _s27_r3_sidepad.out"""
import os, sys, re
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
def ftext(n):
    s = []
    def w(x):
        for k in x.kids:
            if k.tag == "#text": s.append(k.text)
            elif "cv2-note" not in k.toks: w(k)
    w(n); return " ".join(re.sub(r"\W+", " ", " ".join(s).lower()).split()[:8])
def side_kind(col):
    for k in col.kids:
        if k.tag == "#text": continue
        t = k.toks
        if "alertActivity" in t: return "alertActivity"
        if "alertImage" in t: return "alertImage"
        if "alert" in t: return "alert " + " ".join(sorted(t - {"alert"})) if t - {"alert"} else "alert"
        return k.tag + ("." + ".".join(sorted(t)) if t else "")
    return "(empty)"
def sig(col):
    t = col.toks
    keep = sorted(x for x in t if x.startswith("col-") or x.startswith("offset-") or x.startswith("padding"))
    return ".".join(keep)
GOLD = defaultdict(Counter); CL = defaultdict(Counter); PAIR = defaultdict(Counter); pages = defaultdict(set); mods = defaultdict(set); KINDS = Counter()
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"; g = tf + "/" + subj
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
        if re.search(r'acks|acknowledge|glossary', os.path.basename(cp), re.I): continue
        try:
            gt = TB(); gt.feed(body_source(open(hp, encoding="utf-8", errors="replace").read()))
            ct = TB(); ct.feed(body_source(open(cp, encoding="utf-8", errors="replace").read()))
        except Exception: continue
        def rows(root, out):
            for k in root.kids:
                if k.tag == "#text": continue
                if k.tag == "div" and "row" in k.toks:
                    cols = [c for c in k.kids if c.tag == "div" and any(t.startswith("col") for t in c.toks)]
                    if len(cols) == 2 and "col-md-8" in cols[0].toks and "col-md-4" in cols[1].toks:
                        out.append((sig(cols[0]), sig(cols[1]), side_kind(cols[1]), ftext(cols[1])))
                rows(k, out)
        gr = []; rows(gt.root, gr); cr = []; rows(ct.root, cr)
        cidx = {}
        for a, b, kd, w in cr: cidx.setdefault(w, (a, b, kd))
        for a, b, kd, w in gr:
            KINDS[kd] += 1
            key = kd.split(" ")[0]
            GOLD[(g, key)][(a, b)] += 1
            if w in cidx:
                PAIR[(g, key)][((a, b), cidx[w][:2])] += 1; pages[(g, key)].add(hp); mods[(g, key)].add(code)
        for a, b, kd, w in cr:
            CL[(g, kd.split(" ")[0])][(a, b)] += 1
out = []
def P(s=""): out.append(s); print(s)
P("gold side-column kinds (all 2-col 8|4 rows): " + "; ".join(f"{k} {v}" for k, v in KINDS.most_common(10)))
P()
P("==== per group × side kind (gold n ≥ 15): the gold's column-class pair (content | side) shares; then the PAIRED Claude pair ====")
for (g, kd), c in sorted(GOLD.items(), key=lambda kv: -sum(kv[1].values())):
    t = sum(c.values())
    if t < 15: continue
    P(f"   {g:40s} {kd:14s} gold n={t:4d}  " + "  ".join(f"[{a} | {b}] {v} ({v/t:.2f})" for (a, b), v in c.most_common(3)))
    pc = PAIR.get((g, kd), Counter()); pt = sum(pc.values())
    if pt:
        P(f"   {'':40s} {'':14s} paired n={pt:4d} pages {len(pages[(g, kd)]):3d} mods {len(mods[(g, kd)]):3d}  " + "  ".join(f"gold [{ga}|{gb}] → claude [{ca}|{cb}] {v}" for ((ga, gb), (ca, cb)), v in pc.most_common(3)))
P()
P("==== Claude's own 8|4 rows by group × side kind (n ≥ 5) ====")
for (g, kd), c in sorted(CL.items(), key=lambda kv: -sum(kv[1].values())):
    t = sum(c.values())
    if t < 5: continue
    P(f"   {g:40s} {kd:14s} claude n={t:4d}  " + "  ".join(f"[{a} | {b}] {v}" for (a, b), v in c.most_common(3)))
open(os.path.join(OUTPUTS, "_s27_r3_sidepad.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
