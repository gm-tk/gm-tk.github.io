#!/usr/bin/env python3
"""Session 25 — the ledger's container-shift:*->widget family (2.56pp): a GOLD text line (free body or inside an activity
box, unmatched by the gate) whose text Claude holds INSIDE a built widget. By the Claude widget TYPE that holds it, the
gold container, the gold tag, and the text's position relative to the Claude widget (the widget's first / last member or
mid); weighted in pp, with pages / modules and examples. A type whose swallowed text the gold keeps free at ≥ 0.60 is a
members / boundary class for that builder (the r352 carousel precedent).  python3 _s25_swallow.py [prefix-filter]"""
import os, sys, re, difflib
from collections import Counter, defaultdict
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS)
import _corpus
from _diff_miner import page_lines, unorm, TextTree, _cls, node_text
import _structural_skeleton
from _structural_skeleton import WIDGET_MARKERS
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, HUMAN
from _measure_ceiling import load_meta
SKIP = re.compile(r"acks|acknowledge|glossary|references", re.I)
args = [a for a in sys.argv[1:] if not a.startswith("--")]
flt = args[0] if args else ""
TEXT_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "td", "th", "b", "strong", "a", "span", "label", "caption", "figcaption", "button", "i", "em")

def fold(t):
    return re.sub(r"[^a-z0-9]+", " ", unorm(t or "").lower()).strip()

def containers(lines):
    out = []; stack = []
    for ln in lines:
        d = ln.depth
        while stack and stack[-1][0] >= d: stack.pop()
        cont = next((s[1] for s in reversed(stack) if s[1]), None) or "free"
        out.append(cont)
        s = ln.sig
        k = "activity" if s.startswith("div.activity") else "alert" if s.startswith("div.alert") else "panel" if ("Panel" in s or s.startswith("div.introduction")) else None
        stack.append((d, k))
    return out

def claude_widget_texts(path):
    """folded text -> (widget type, member index, member count, the widget's own first text) for every text element
    inside a Claude built widget (cv2-interactive hand-off boxes excluded — they are not built)"""
    raw = open(path, encoding="utf-8", errors="replace").read()
    src = _structural_skeleton.body_source(raw)
    tb = TextTree(); tb.feed(src)
    out = {}
    def walk(n, wtype, bag):
        c = _cls(n)
        hit = sorted((c & WIDGET_MARKERS) - {"cv2-interactive"})
        if hit and wtype is None:
            wtype = hit[0]; bag = []
            for k in n.kids: walk(k, wtype, bag)
            for idx, ft in enumerate(bag):
                out.setdefault(ft, (wtype, idx, len(bag)))
            return
        if wtype and n.tag in TEXT_TAGS:
            t = node_text(n)
            if t: bag.append(fold(t))
        for k in n.kids: walk(k, wtype, bag)
    body = next((k for k in tb.root.kids if k.tag == "body"), None)
    walk(body if body is not None else tb.root, None, None)
    return out

fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
meta = load_meta()
loss = defaultdict(float); pages = defaultdict(set); mods = defaultdict(set); ex = defaultdict(list); N = 0
bytype = defaultdict(float); bytype_pages = defaultdict(set)
for code in sorted(fam):
    if flt and not code.startswith(flt): continue
    tf = fam[code]
    for n, cp, hp in pairs(code):
        if SKIP.search(os.path.basename(hp)) or SKIP.search(os.path.basename(cp)): continue
        try:
            g, _ = page_lines(hp); c, _ = page_lines(cp)
        except Exception:
            continue
        N += 1
        gs = [l.pad + l.sig for l in g]; cs = [l.pad + l.sig for l in c]
        gc = containers(g)
        w = 1.0 / max(len(gs) + len(cs), 1)
        sm = difflib.SequenceMatcher(None, gs, cs, autojunk=False)
        ug = [i for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal" for i in range(i1, i2)]
        if not ug: continue
        cw = None
        for i in ug:
            l = g[i]
            if not l.text or l.region not in ("body", "activity"): continue
            t = re.match(r"([a-z0-9]+)", l.sig).group(1)
            if t not in TEXT_TAGS: continue
            if cw is None: cw = claude_widget_texts(cp)
            hit = cw.get(fold(l.text))
            if not hit: continue
            wtype, idx, cnt = hit
            posn = "first" if idx == 0 else "last" if idx == cnt - 1 else "mid"
            key = (wtype, gc[i], t, posn)
            loss[key] += w; pages[key].add(hp); mods[key].add(code)
            bytype[wtype] += w; bytype_pages[wtype].add(hp)
            if len(ex[key]) < 3: ex[key].append((code, os.path.basename(cp), (l.text or "")[:60]))
print(f"pages {N}; gold text (free / activity) that Claude holds inside a built widget — by Claude widget type:")
for wt, v in sorted(bytype.items(), key=lambda kv: -kv[1]):
    print(f"   {v/N*100:6.2f}pp  pages {len(bytype_pages[wt]):5d}   {wt}")
print("\nby (Claude widget type · gold container · gold tag · position in the widget):")
for key, v in sorted(loss.items(), key=lambda kv: -kv[1])[:40]:
    print(f"   {v/N*100:6.2f}pp  pages {len(pages[key]):5d} / modules {len(mods[key]):3d}   {key}   e.g. {ex[key][:2]}")
