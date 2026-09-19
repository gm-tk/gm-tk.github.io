#!/usr/bin/env python3
"""Session 27 Round 6 — THE ACTIVITY NUMBER CENSUS after r400: on every paired page, Claude's top-level activity boxes vs the gold's
in order — box counts equal / Claude more / gold more; on the count-equal pages the k-th numbers: equal / letter differs / lesson
digit differs / form differs (case, dotted, numberless); on the count-differs pages the numbers that never appear on the other side.
By page kind (overview / lesson) and subject; the writer's opener for the mismatches where a heading is shared.
  wsl: python3 _s27_r6_numbers.py"""
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
    __slots__ = ("tag", "toks", "kids", "parent", "attrs")
    def __init__(s, tag, cls, parent, attrs): s.tag, s.toks, s.kids, s.parent, s.attrs = tag, set(cls.split()), [], parent, attrs
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
    def handle_data(s, data): pass
def boxes(root):
    out = []
    def w(n, inside):
        for c in n.kids:
            if c.tag == "div" and "activity" in c.toks and not ({"clickDropContent", "cv2-interactive"} & c.toks):
                if not inside: out.append(c.attrs.get("number", "").strip())
                w(c, True)
            else: w(c, inside)
    w(root, False); return out
def split_id(x):
    m = re.match(r"^(\d+(?:\.\d+)?)\s*([A-Za-z]?)$", x or "")
    return (m.group(1), m.group(2).upper()) if m else (None, None)
CNT = Counter(); EQ = Counter(); BYG = defaultdict(Counter); pages = defaultdict(set); EX = defaultdict(list); DIFFC = Counter(); MORE = defaultdict(set)
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"; g = tf + "/" + subj
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
        pk = "overview" if re.search(r"_0_0\.html$", cp) else "lesson"
        try:
            gt = TB(); gt.feed(body_source(open(hp, encoding="utf-8", errors="replace").read()))
            ct = TB(); ct.feed(body_source(open(cp, encoding="utf-8", errors="replace").read()))
        except Exception: continue
        gb = boxes(gt.root); cb = boxes(ct.root)
        if not gb and not cb: continue
        CNT[(pk, "equal" if len(gb) == len(cb) else ("claude-more" if len(cb) > len(gb) else "gold-more"))] += 1
        if len(gb) != len(cb):
            DIFFC[(pk, len(cb) - len(gb))] += 1; MORE[(pk, "claude-more" if len(cb) > len(gb) else "gold-more")].add(cp)
            continue
        for k, (c, gn) in enumerate(zip(cb, gb)):
            cl, cL = split_id(c); gl, gL = split_id(gn)
            if c.upper() == gn.upper(): v = "equal"
            elif not c: v = "claude-numberless"
            elif not gn: v = "gold-numberless"
            elif cl is None or gl is None: v = "form-differs"
            elif cl != gl and cL == gL: v = "lesson-digit-differs"
            elif cl == gl and cL != gL: v = "letter-differs"
            else: v = "both-differ"
            EQ[(pk, v)] += 1; BYG[g][v] += 1; pages[(pk, v)].add(cp)
            if v != "equal" and len(EX[(pk, v)]) < 6: EX[(pk, v)].append(f"{code}/{os.path.basename(cp)} k={k} claude={c or '—'} gold={gn or '—'} seq={cb} / {gb}")
print("pages with boxes by count relation:", dict(CNT))
print("count-differs (claude − gold):", sorted(DIFFC.items(), key=lambda kv: -kv[1])[:12], {k: len(v) for k, v in MORE.items()})
print("==== count-equal pages: k-th number verdicts ====")
for key, v in sorted(EQ.items(), key=lambda kv: -kv[1]): print(f"   {v:5d} pages {len(pages[key]):4d}  {key}")
print("==== per group (lesson-digit / letter / both / form mismatches) ====")
for g, c in sorted(BYG.items(), key=lambda kv: -sum(kv[1].values()))[:16]:
    t = sum(c.values()); print(f"   {g:42s} n={t:4d}  " + "  ".join(f"{k} {v}" for k, v in c.most_common(5)))
for key, ex in EX.items():
    for e in ex: print(f"   {key}: {e}")
