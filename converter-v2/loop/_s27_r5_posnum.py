#!/usr/bin/env python3
"""Session 27 Round 5 — POSITIONAL NUMBERING FOR CLAUDE'S NUMBERLESS BOXES. On every paired LESSON page where Claude and
the gold ship the SAME number of top-level activity boxes, walk the boxes in order: for a Claude box WITH a number, does
it equal the gold's k-th number (the r88/r217 state today)? For a NUMBERLESS Claude box, would the POSITIONAL id
({lesson}{k-th letter}) equal the gold's k-th number? Also the simpler NEXT-LETTER rule (the previous Claude box's letter
+ 1, or A). By subject.  wsl: python3 _s27_r5_posnum.py"""
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
def boxes(root):
    out = []
    def w(n, inside):
        for c in n.kids:
            if c.tag == "div" and "activity" in c.toks and not ({"clickDropContent", "cv2-interactive"} & c.toks):
                if not inside: out.append(c.attrs.get("number", "").strip())
                w(c, True)
            else: w(c, inside)
    w(root, False); return out
def letter(k): return chr(ord("A") + k) if k < 26 else "?"
NUMD = Counter(); POS = Counter(); NXT = Counter(); BYG = defaultdict(Counter); pages = defaultdict(set); mods = defaultdict(set); EX = defaultdict(list); CNT = Counter()
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"; g = tf + "/" + subj
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
        m = re.search(r"_(\d+)_(\d+)\.html$", cp)
        if not m or m.group(1) == "0": continue
        lesson = m.group(1)
        try:
            gt = TB(); gt.feed(body_source(open(hp, encoding="utf-8", errors="replace").read()))
            ct = TB(); ct.feed(body_source(open(cp, encoding="utf-8", errors="replace").read()))
        except Exception: continue
        gb = boxes(gt.root); cb = boxes(ct.root)
        if not cb: continue
        CNT["pages"] += 1
        if not any(x == "" for x in cb): continue
        CNT["pages-with-numberless"] += 1
        if len(gb) != len(cb): CNT["count-differs"] += 1; continue
        CNT["count-equal"] += 1
        prev = None
        for k, (c, gnum) in enumerate(zip(cb, gb)):
            pos = f"{lesson}{letter(k)}"
            if c:
                NUMD["claude-numbered=gold" if c.upper() == gnum.upper() else "claude-numbered≠gold"] += 1
                mm = re.match(r"^(\d+)([A-Za-z])$", c); prev = mm.group(2).upper() if mm else None
                continue
            # numberless
            nxt = f"{lesson}{letter(ord(prev) - ord('A') + 1) if prev else 'A'}"
            v = ("pos=gold" if pos.upper() == gnum.upper() else "pos≠gold")
            v2 = ("next=gold" if nxt.upper() == gnum.upper() else "next≠gold")
            POS[v] += 1; NXT[v2] += 1; BYG[g][v] += 1; pages[v].add(cp); mods[v].add(code)
            if len(EX[(v, v2)]) < 4: EX[(v, v2)].append(f"{code}/{os.path.basename(cp)} k={k} gold={gnum} pos={pos} next={nxt} claude-seq={cb}")
            prev = letter(ord(prev) - ord('A') + 1) if prev else "A"
print(dict(CNT))
print("Claude's NUMBERED boxes on count-equal pages:", dict(NUMD))
print("numberless boxes — positional k-th letter:", dict(POS), " pages", {k: len(v) for k, v in pages.items()}, " mods", {k: len(v) for k, v in mods.items()})
print("numberless boxes — next-letter rule:", dict(NXT))
for g, c in sorted(BYG.items(), key=lambda kv: -sum(kv[1].values()))[:12]:
    t = sum(c.values()); print(f"   {g:42s} n={t:3d}  " + "  ".join(f"{k} {v} ({v/t:.2f})" for k, v in c.most_common()))
for key, ex in EX.items():
    for e in ex: print(f"   {key}: {e}")
