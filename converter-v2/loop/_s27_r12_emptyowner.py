#!/usr/bin/env python3
"""Session 27 Round 12 census — THE WRITER-OWNED EMPTY BOX: every Claude top-level activity box whose whole content is the
`no content captured` flag (a writer's own numbered opener whose member walk captured nothing), what FOLLOWS it on the Claude
page (the free section: heading / prose / table / a cv2 box), and what the GOLD's same-numbered box holds (h3? prose? a widget?
a kept table?). The r362 owner-form question re-asked on the post-r406 corpus.  wsl: python3 _s27_r12_emptyowner.py"""
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
WIDGET = {"dragAndDrop", "clickDrop", "accordion", "tabs", "carousel", "flipCardsContainer", "flipCard", "mcqOptions", "dropQuiz", "selfCheck",
          "hintSlider", "speechBubble", "TKmodal", "wordFind", "crossword", "memoryGame", "shapeHover", "typing", "reorder", "rotateBanner", "cv2-interactive"}
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
def boxes(root):
    out = []
    def w(n, inside):
        for c in n.kids:
            if c.tag == "div" and "activity" in c.toks and not ({"clickDropContent", "cv2-interactive"} & c.toks):
                if not inside: out.append(c)
                w(c, True)
            else: w(c, inside)
    w(root, False); return out
def leaves(n):
    out = []
    def w(x):
        for c in x.kids:
            if c.tag == "#text": continue
            if c.tag == "div" and c.toks <= {"row", "col-12", "col-md-8", "col-md-12", "col-md-6", "paddingLR", "paddingR", "paddingL"}: w(c); continue
            out.append(c)
    w(n); return out
def ftext(n):
    s = []
    def w(x):
        for c in x.kids:
            if c.tag == "#text": s.append(c.text)
            else: w(c)
    w(n); return " ".join(s)
def has_widget(n):
    found = []
    def w(x):
        for c in x.kids:
            if c.tag == "#text": continue
            if c.tag == "table": found.append("table")
            if c.toks & WIDGET: found.append(sorted(c.toks & WIDGET)[0])
            w(c)
    w(n); return found
def flat(root):
    """document-order list of element nodes (for 'what follows the box')."""
    out = []
    def w(x):
        for c in x.kids:
            if c.tag == "#text": continue
            out.append(c); w(c)
    w(root); return out
def sig(n):
    if n.tag in ("h1","h2","h3","h4","h5","h6"): return n.tag
    if n.tag == "table": return "table"
    if n.toks & WIDGET: return "W:" + sorted(n.toks & WIDGET)[0]
    if n.tag == "p": return "p"
    if n.tag in ("ul","ol"): return n.tag
    if n.tag == "img": return "img"
    return None
FLAG = Counter(); FOLLOW = Counter(); GOLD = Counter(); GOLDW = Counter(); EX = []; total = 0; pages = set(); mods = set(); BYG = defaultdict(Counter)
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"; g = tf + "/" + subj
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
        try:
            ct = TB(); ct.feed(body_source(open(cp, encoding="utf-8", errors="replace").read()))
            gt = TB(); gt.feed(body_source(open(hp, encoding="utf-8", errors="replace").read()))
        except Exception: continue
        cb = boxes(ct.root); gb = {b.attrs.get("number", ""): b for b in boxes(gt.root)}
        cflat = flat(ct.root)
        for b in cb:
            lv = leaves(b)
            if not lv or any(not (x.tag == "p" and ({"cv2-note", "cv2-comment"} & x.toks)) for x in lv): continue
            t = ftext(b)
            if "no content captured" not in t: continue
            total += 1; pages.add(cp); mods.add(code)
            m = re.search(r"Un-built \[([^\]]+)\]", t); FLAG[m.group(1) if m else "?"] += 1
            # what follows the empty box on the Claude page: the next 4 signature-bearing elements after the box subtree
            idx = cflat.index(b); sub = set(flat(b)); seq = []
            for x in cflat[idx + 1:]:
                if x in sub: continue
                sg = sig(x)
                if sg: seq.append(sg)
                if len(seq) >= 4: break
            FOLLOW[" ".join(seq)] += 1
            num = b.attrs.get("number", "")
            gbox = gb.get(num)
            if gbox is None: GOLD["gold: no box of that number"] += 1; BYG[g]["gold-absent"] += 1
            else:
                glv = leaves(gbox); gw = has_widget(gbox)
                heads = [x.tag for x in glv if x.tag in ("h3","h4","h5")]
                key = ("h3+" if "h3" in heads else "") + ("widget" if any(w != "table" for w in gw) else ("table" if gw else "prose-only"))
                GOLD["gold: " + key] += 1; BYG[g][key] += 1
                if gw: GOLDW[gw[0]] += 1
            if len(EX) < 40: EX.append(f"{code}/{os.path.basename(cp)} #{num} [{FLAG and (m.group(1) if m else '?')}] follows «{' '.join(seq)}» gold {'ABSENT' if gbox is None else key}")
print(f"writer-owned EMPTY boxes (the `no content captured` flag alone): {total} on {len(pages)} pages / {len(mods)} modules")
print("flag types:", dict(FLAG.most_common()))
print("what follows on the Claude page (next 4 elements):")
for k, v in FOLLOW.most_common(15): print(f"   {v:3d}  {k}")
print("the gold's same-numbered box:")
for k, v in GOLD.most_common(): print(f"   {v:3d}  {k}")
print("gold widget kinds:", dict(GOLDW.most_common()))
print("by template/subject:")
for g, c in sorted(BYG.items(), key=lambda kv: -sum(kv[1].values()))[:14]: print(f"   {g:40s} {dict(c)}")
print("examples:")
for e in EX: print("   " + e)
