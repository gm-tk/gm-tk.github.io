#!/usr/bin/env python3
"""Session 27 Round 4 — WHERE DO THE GOLD'S MISSING <p> COME FROM? (label census: p MISSING 5651 lines / 1039 pages,
EXTRA 3412). Per paired page, count gold vs Claude <p> by SUB-KIND — empty / text-only / img-only / a-only / b-only /
br-carrying / mixed — and by the p's parent label; sum the per-page deficit (gold − Claude, positive part) per sub-kind and
per (parent, sub-kind); group by template/subject.  wsl: python3 _s27_r4_pkinds.py -> _s27_r4_pkinds.out"""
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
SKIP = set(WIDGET_MARKERS) | {"cv2-interactive", "cv2-note", "cv2-comment", "acks"}
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
def pkind(p):
    kids = p.kids
    if not kids: return "empty"
    tags = [k.tag for k in kids]
    txt = any(t == "#text" for t in tags)
    els = [t for t in tags if t != "#text"]
    if not els: return "text"
    if not txt and els == ["img"]: return "img-only"
    if not txt and els == ["a"]: return "a-only"
    if not txt and els in (["b"], ["strong"]): return "b-only"
    if not txt and els in (["i"], ["em"]): return "i-only"
    if "br" in els: return "br"
    if txt and set(els) <= {"b", "strong", "i", "em", "a", "span", "sup", "sub", "u"}: return "text+inline"
    if not txt and set(els) <= {"b", "strong", "i", "em", "a", "span"}: return "inline-only"
    return "other:" + ",".join(sorted(set(els)))[:30]
def walk(n, f):
    for c in n.kids:
        if c.tag != "#text": f(c); walk(c, f)
DEF = Counter(); DEFP = Counter(); EXC = Counter(); pages = defaultdict(set); mods = defaultdict(set); BYG = defaultdict(Counter); EX = defaultdict(list)
GT = Counter(); CT = Counter()
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"; g = tf + "/" + subj
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
        try:
            gt = TB(); gt.feed(body_source(open(hp, encoding="utf-8", errors="replace").read()))
            ct = TB(); ct.feed(body_source(open(cp, encoding="utf-8", errors="replace").read()))
        except Exception: continue
        gc = Counter(); cc = Counter(); gcp = Counter(); ccp = Counter(); gex = {}
        def gw(x):
            if x.tag == "p":
                k = pkind(x); gc[k] += 1; gcp[(lab(x.parent), k)] += 1
                if k not in gex: gex[k] = (lab(x.parent), " ".join(c.text for c in x.kids if c.tag == "#text")[:40])
        def cw(x):
            if x.tag == "p":
                k = pkind(x); cc[k] += 1; ccp[(lab(x.parent), k)] += 1
        walk(gt.root, gw); walk(ct.root, cw)
        for k in set(gc) | set(cc):
            GT[k] += gc[k]; CT[k] += cc[k]
            d = gc[k] - cc[k]
            if d > 0:
                DEF[k] += d; pages[k].add(hp); mods[k].add(code); BYG[g][k] += d
                if len(EX[k]) < 4: EX[k].append(f"{code} {os.path.basename(hp)} +{d} {gex.get(k)}")
            elif d < 0: EXC[k] += -d
        for k in set(gcp) | set(ccp):
            d = gcp[k] - ccp[k]
            if d > 0: DEFP[k] += d
out = []
def P(s=""): out.append(s); print(s)
P("==== gold <p> sub-kinds: total gold / total claude / per-page DEFICIT (gold over claude) / per-page EXCESS / deficit pages / modules ====")
for k, v in sorted(DEF.items(), key=lambda kv: -kv[1]):
    P(f"   {k:22s} gold {GT[k]:6d} claude {CT[k]:6d}  deficit {v:5d}  excess {EXC[k]:5d}  pages {len(pages[k]):4d}  mods {len(mods[k]):3d}")
P()
P("==== deficit by (parent, sub-kind) — top 25 ====")
for (par, k), v in DEFP.most_common(25): P(f"   {v:5d}  {par:44s} {k}")
P()
P("==== per group (deficit ≥ 60): top sub-kinds ====")
for g, c in sorted(BYG.items(), key=lambda kv: -sum(kv[1].values())):
    t = sum(c.values())
    if t < 60: continue
    P(f"   {g:42s} n={t:5d}  " + "  ".join(f"[{k}] {v}" for k, v in c.most_common(5)))
P()
for k, ex in EX.items():
    if DEF[k] >= 100:
        for e in ex: P(f"   {k}: {e}")
open(os.path.join(OUTPUTS, "_s27_r4_pkinds.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
