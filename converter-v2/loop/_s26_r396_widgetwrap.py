#!/usr/bin/env python3
"""BUILT-WIDGET ROOT WRAPPERS: for each widget root class, the two enclosing wrappers (grandparent › parent), gold vs Claude —
the r394 clickDrop instrument generalised. python3 _s26_r396_widgetwrap.py"""
import os, sys, re
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
sys.path.insert(0, OUTPUTS)
src = open(os.path.join(OUTPUTS, "_s26_r392_adjul.py"), encoding="utf-8").read()
exec(src[:src.index("widgets = json.load")])
from _discrepancy_audit import pairs
from _measure_ceiling import load_meta
import _corpus
from anchor_compare import CLAUDE
from collections import Counter, defaultdict
meta = load_meta()
fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
def body(html):
    m = re.search(r"<div id=\"body\"", html); s = html[m.start():] if m else html
    a = s.find("<div class=\"acks"); return s if a < 0 else s[:a]
ROOTS = ["accordion", "tabs", "carousel", "flipCardsContainer", "dragAndDrop", "multiChoiceQuiz", "dropQuiz", "wordSelect", "hintSlider", "TKmodal", "speechBubble", "table-responsive", "videoSection", "audioPlayer", "clickDropContent", "dropbox", "wordHighlighter", "sortable", "typing", "matching"]
TAG = re.compile(r"<(/?)([a-z][a-z0-9]*)\b([^>]*)>", re.I)
CLS = re.compile(r'class="([^"]*)"')
VOID = {"br", "img", "input", "hr", "meta", "link", "source", "wbr"}
def scan(s):
    st = []; out = []
    for m in TAG.finditer(s):
        closing, tag, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID and not closing:
            if tag == "img" or tag == "input":
                pass
            continue
        if closing:
            if st: st.pop()
            continue
        c = CLS.search(attrs); toks = (c.group(1) if c else "").split()
        cls = " ".join(sorted(toks)); label = tag + (("." + cls.replace(" ", ".")) if cls else "")
        root = next((r for r in ROOTS if r in toks), None)
        if root and not any(e[1] == root for e in st[-6:]):   # the OUTERMOST element of that widget kind
            out.append((root, " › ".join(e[0] for e in st[-2:])))
        st.append((label, root))
    return out
C = defaultdict(Counter); G = defaultdict(Counter); CP = defaultdict(lambda: defaultdict(set)); GP = defaultdict(lambda: defaultdict(set)); CM = defaultdict(lambda: defaultdict(set))
for code in sorted(fam):
    for n, cp, hp in pairs(code):
        try:
            ch = body(open(cp, encoding="utf-8", errors="replace").read()); gh = body(open(hp, encoding="utf-8", errors="replace").read())
        except Exception: continue
        for r, k in scan(ch): C[r][k] += 1; CP[r][k].add(cp); CM[r][k].add(code)
        for r, k in scan(gh): G[r][k] += 1; GP[r][k].add(hp)
for r in ROOTS:
    if not C[r] and not G[r]: continue
    print(f"==== {r}: gold {sum(G[r].values())} / claude {sum(C[r].values())} ====")
    keys = sorted(set(G[r]) | set(C[r]), key=lambda k: -(G[r][k] + C[r][k]))
    for k in keys[:6]:
        print(f"   gold {G[r][k]:4d} (pages {len(GP[r][k]):3d})   claude {C[r][k]:4d} (pages {len(CP[r][k]):3d} / mods {len(CM[r][k]):3d})   {k}")
