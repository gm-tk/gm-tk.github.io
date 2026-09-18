#!/usr/bin/env python3
"""Session 25 — Claude's EXTRA free-body paragraphs (the largest single loss cell, 2.12pp on 1,415 pages): for every
Claude `p` line the gate's alignment leaves unmatched, where does the GOLD hold that text on the same page? Buckets:
gold free `p` elsewhere (alignment residue), inside a gold ACTIVITY box, inside a gold WIDGET, inside a gold ALERT, a
gold heading / li / td / b (tag swap), merged into a longer gold element, split across shorter ones, in the header /
menu, or NOWHERE (reworded / dropped). Weighted in pp of the corpus mean and counted in pages / modules, per template.
Also the same for the gold's MISSING activity `p` (1.45pp): where does CLAUDE hold it?
  python3 _s25_pwhere.py [prefix-filter]"""
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

def elements(path):
    """every text-bearing element of a page INCLUDING widget insides: (tag, folded text, container) where container is
    widget / activity / alert / header / free"""
    raw = open(path, encoding="utf-8", errors="replace").read()
    src = _structural_skeleton.body_source(raw)
    tb = TextTree(); tb.feed(src)
    out = []
    def walk(n, cont):
        c = _cls(n)
        cont2 = cont
        if n.attrs.get("id") in ("header", "module-menu-content", "footer") or (c & {"acks", "acksTemplate"}): cont2 = "header"
        elif cont == "free" or cont == "alert" or cont == "activity":
            if c & WIDGET_MARKERS: cont2 = "widget"
            elif any(t.startswith("activity") for t in c): cont2 = "activity"
            elif any(t.startswith("alert") for t in c) and cont == "free": cont2 = "alert"
        if n.tag in ("h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "td", "th", "b", "strong", "a", "span", "label", "caption", "figcaption", "button", "div"):
            t = node_text(n)
            if t and (n.tag != "div" or len(t) < 200):
                out.append((n.tag, fold(t), cont2))
        for k in n.kids: walk(k, cont2)
    body = next((k for k in tb.root.kids if k.tag == "body"), None)
    walk(body if body is not None else tb.root, "free")
    return out

def locate(ft, gel, own_tag="p"):
    if not ft: return "empty"
    exact = [e for e in gel if e[1] == ft]
    if exact:
        # prefer the same tag
        same = [e for e in exact if e[0] == own_tag]
        e = same[0] if same else exact[0]
        if e[2] == "header": return "gold header/menu/acks"
        if e[2] == "widget": return f"gold inside WIDGET"
        if e[2] == "activity": return f"gold inside ACTIVITY ({e[0]})" if e[0] != own_tag else "gold inside ACTIVITY"
        if e[2] == "alert": return "gold inside ALERT" if e[0] == own_tag else f"gold inside ALERT ({e[0]})"
        return "gold free " + ("same tag (alignment residue)" if e[0] == own_tag else e[0])
    if len(ft) >= 15:
        cont = [e for e in gel if ft in e[1] and e[0] != "div"]
        if cont:
            e = cont[0]
            return "gold MERGED into longer " + e[0] + (" (" + e[2] + ")" if e[2] != "free" else "")
        w = ft.split()
        if len(w) >= 6:
            head = " ".join(w[:5])
            part = [e for e in gel if head in e[1] and e[0] != "div"]
            if part:
                e = part[0]
                return "gold SPLIT / reworded " + e[0] + (" (" + e[2] + ")" if e[2] != "free" else "")
    return "NOWHERE in gold"

fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
meta = load_meta()
lossA = defaultdict(lambda: defaultdict(float)); pagesA = defaultdict(lambda: defaultdict(set)); modsA = defaultdict(lambda: defaultdict(set))
lossB = defaultdict(lambda: defaultdict(float)); pagesB = defaultdict(lambda: defaultdict(set)); modsB = defaultdict(lambda: defaultdict(set))
N = Counter(); ex = defaultdict(list)
for code in sorted(fam):
    if flt and not code.startswith(flt): continue
    tf = fam[code]
    for n, cp, hp in pairs(code):
        if SKIP.search(os.path.basename(hp)) or SKIP.search(os.path.basename(cp)): continue
        try:
            g, _ = page_lines(hp); c, _ = page_lines(cp)
        except Exception:
            continue
        gs = [l.pad + l.sig for l in g]; cs = [l.pad + l.sig for l in c]
        gc = containers(g); cc = containers(c)
        w = 1.0 / max(len(gs) + len(cs), 1)
        sm = difflib.SequenceMatcher(None, gs, cs, autojunk=False)
        keys = ("ALL", f"template={tf}")
        for k in keys: N[k] += 1
        gel = cel = None
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal": continue
            for j in range(j1, j2):
                l = c[j]
                if l.region != "body" or cc[j] != "free" or not (l.sig == "p" or l.sig.startswith("p.")): continue
                if gel is None: gel = elements(hp)
                v = locate(fold(l.text), gel)
                for k in keys:
                    lossA[k][v] += w; pagesA[k][v].add(cp); modsA[k][v].add(code)
                if len(ex[v]) < 4: ex[v].append((code, os.path.basename(cp), (l.text or "")[:70]))
            for i in range(i1, i2):
                l = g[i]
                if l.region != "activity" or gc[i] != "activity" or not (l.sig == "p" or l.sig.startswith("p.")): continue
                if cel is None: cel = elements(cp)
                v = locate(fold(l.text), cel).replace("gold", "Claude")
                for k in keys:
                    lossB[k][v] += w; pagesB[k][v].add(cp); modsB[k][v].add(code)

for title, loss, pg, md in (("A) Claude's EXTRA free-body p — where the GOLD holds the text", lossA, pagesA, modsA),
                            ("B) the gold's MISSING activity p — where CLAUDE holds the text", lossB, pagesB, modsB)):
    for k in ("ALL", "template=Standard", "template=Inquiry", "template=Fundamentals", "template=Bilingual"):
        if not N[k] or not loss[k]: continue
        tot = sum(loss[k].values()) / N[k] * 100
        print(f"\n== {title} — {k} — pages {N[k]}: {tot:.2f}pp")
        for v, x in sorted(loss[k].items(), key=lambda kv: -kv[1])[:14]:
            print(f"   {x/N[k]*100:6.2f}pp  pages {len(pg[k][v]):5d} / modules {len(md[k][v]):3d}   {v}")
print("\nexamples (A):")
for v, e in ex.items(): print(" ", v, "→", e)
