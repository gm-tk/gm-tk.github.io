#!/usr/bin/env python3
"""Session 27 Round 3 candidate — THE GOLD'S h4 (MISSING 1522 lines / 686 pages). Every gold <h4> on the gate pairs (free body,
widgets excluded): its parent label; the same text on Claude's page → Claude's element (h3 / h5 / p / b / li / absent) and
parent; by template/subject, and by the WRITER'S source (the WT line holding the text: its tag).  wsl: python3 _s27_r3_h4.py"""
import os, sys, re
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
from collections import Counter, defaultdict
from html.parser import HTMLParser
meta = load_meta()
fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
VOID = {"br", "img", "input", "hr", "meta", "link", "source", "wbr", "area", "base", "col", "embed", "track"}
SKIP = set(WIDGET_MARKERS) | {"cv2-interactive", "cv2-note", "acks"}
class N:
    __slots__ = ("tag", "toks", "kids", "parent", "text")
    def __init__(s, tag, cls, parent): s.tag, s.toks, s.kids, s.parent, s.text = tag, set(cls.split()), [], parent, ""
class TB(HTMLParser):
    def __init__(s):
        super().__init__(); s.root = N("root", "", None); s.cur = s.root; s.stack = []; s.skip = 0
    def handle_starttag(s, tag, attrs):
        a = dict(attrs); n = N(tag, a.get("class") or "", s.cur)
        if s.skip == 0: s.cur.kids.append(n)
        if tag in VOID: return
        if n.toks & SKIP: s.skip += 1
        s.stack.append((n, bool(n.toks & SKIP))); s.cur = n
    def handle_startendtag(s, tag, attrs): s.handle_starttag(tag, attrs)
    def handle_endtag(s, tag):
        if tag in VOID or not s.stack: return
        n, sk = s.stack.pop()
        if sk: s.skip -= 1
        s.cur = n.parent or s.root
    def handle_data(s, data):
        if s.skip == 0 and data.strip():
            t = N("#text", "", s.cur); t.text = data.strip(); s.cur.kids.append(t)
def lab(n): return "—" if n is None else (n.tag + ("." + ".".join(sorted(n.toks)) if n.toks else ""))
def ftext(n):
    s = []
    def w(x):
        for c in x.kids:
            if c.tag == "#text": s.append(c.text)
            else: w(c)
    w(n); return re.sub(r"\W+", " ", " ".join(s).lower()).strip()
def wt_lines(code):
    d = _corpus.mdir(HUMAN, code)
    fs = sorted(f for f in os.listdir(d) if f.endswith("_parsed.txt"))
    pref = [f for f in fs if "writers template" in f.lower()] or fs
    if not pref: return []
    return open(os.path.join(d, pref[0]), encoding="utf-8", errors="replace").read().split("\n")
TAGLINE = re.compile(r"🔴\[RED TEXT\]\s*\[([^\]]*)\]")
def writer_tag(lines, folded, key):
    k5 = " ".join(key.split()[:5])
    if len(k5) < 8: return "(short)"
    for i, fl in enumerate(folded):
        if k5 in fl:
            m = TAGLINE.search(lines[i])
            if m: return re.sub(r"\d+[a-z]?", "N", m.group(1).strip().lower())[:22]
            return "(black line)"
    return "(not in WT)"
C = Counter(); BYG = defaultdict(Counter); BYTAG = defaultdict(Counter); pages = defaultdict(set); mods = defaultdict(set); EX = defaultdict(list)
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"; g = tf + "/" + subj
    WT = {"lines": None, "folded": None}
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
        if re.search(r'acks|acknowledge|glossary', os.path.basename(cp), re.I): continue
        try:
            gt = TB(); gt.feed(body_source(open(hp, encoding="utf-8", errors="replace").read()))
            ct = TB(); ct.feed(body_source(open(cp, encoding="utf-8", errors="replace").read()))
        except Exception: continue
        cidx = {}
        def cw(x):
            for c in x.kids:
                if c.tag == "#text": continue
                if c.tag in ("h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "td", "th", "b", "strong"):
                    t = ftext(c)
                    if t and t not in cidx: cidx[t] = (c.tag, lab(c.parent))
                cw(c)
        cw(ct.root)
        def gw(x):
            for c in x.kids:
                if c.tag == "#text": continue
                if c.tag == "h4":
                    t = ftext(c)
                    if t:
                        par = lab(c.parent); par = re.sub(r"\[.*", "", par)
                        cl = cidx.get(t)
                        ck = cl[0] if cl else "absent"
                        if ck == "p" and cl[1].startswith("h"): ck = "p-in-" + cl[1]
                        key = (par, ck)
                        C[key] += 1; BYG[g][key] += 1; pages[key].add(hp); mods[key].add(code)
                        if ck != "h4":
                            if WT["lines"] is None: WT["lines"] = wt_lines(code); WT["folded"] = [re.sub(r"\W+", " ", l.lower()) for l in WT["lines"]]
                            wt = writer_tag(WT["lines"], WT["folded"], t)
                            BYTAG[(par, ck)][wt] += 1
                            if len(EX[(par, ck, wt)]) < 2: EX[(par, ck, wt)].append(f"{code} {os.path.basename(hp)} «{t[:45]}»")
                gw(c)
        gw(gt.root)
out = []
def P(s=""): out.append(s); print(s)
P("==== gold h4 by (parent, Claude's element for the same text) — top 30 ====")
for (par, ck), v in C.most_common(30):
    P(f"   {v:5d}  pages {len(pages[(par, ck)]):4d} mods {len(mods[(par, ck)]):3d}   parent {par:36s} claude {ck}")
P()
P("==== the writer's tag behind the mismatches (top 8 per (parent, claude) with ≥ 40) ====")
for (par, ck), c in sorted(BYTAG.items(), key=lambda kv: -sum(kv[1].values())):
    t = sum(c.values())
    if t < 40: continue
    P(f"   parent {par:36s} claude {ck:10s} n={t:4d}  " + "  ".join(f"[{k}] {v}" for k, v in c.most_common(8)))
P()
P("==== per group (n ≥ 20): the top mismatches ====")
for g, c in sorted(BYG.items(), key=lambda kv: -sum(kv[1].values())):
    t = sum(c.values())
    if t < 20: continue
    mis = [(k, v) for k, v in c.most_common() if k[1] != "h4"][:4]
    P(f"   {g:42s} gold h4 n={t:4d}  claude h4 {sum(v for k, v in c.items() if k[1] == 'h4')/t:.2f}  " + "  ".join(f"[{k[0][:24]} → {k[1]}] {v}" for k, v in mis))
P()
for key, ex in list(EX.items())[:24]:
    if C[(key[0], key[1])] >= 30:
        for e in ex: P(f"   {key}: {e}")
open(os.path.join(OUTPUTS, "_s27_r3_h4.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
