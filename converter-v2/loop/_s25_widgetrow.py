#!/usr/bin/env python3
"""Session 25 — HOW a built widget sits at the top of the body, gold vs Claude, by widget TYPE: 'row-is-widget' (the
widget's wrapper carries the row class itself: div.row.carousel…), 'in-col' (row > col > widget), 'deep' (inside an
activity / alert / panel / other). The scaffold skeleton collapses both to WIDGET, but at different depths — a
row-is-widget gold vs an in-col Claude costs two lines + the indent on every page. Un-collapsed skeleton read.
  python3 _s25_widgetrow.py [prefix-filter]"""
import os, sys, re, json
from collections import Counter, defaultdict
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
sys.path.insert(0, TESTS)
import _corpus
from _skeleton_compare import _skel
from _structural_skeleton import WIDGET_MARKERS
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, HUMAN
from _measure_ceiling import load_meta
SKIP = re.compile(r"acks|acknowledge|glossary|references", re.I)
args = [a for a in sys.argv[1:] if not a.startswith("--")]
flt = args[0] if args else ""

def ind(l): return len(l) - len(l.lstrip(" "))

def wtype(lbl):
    s = lbl.strip()
    if not s.startswith("div"): return None
    toks = set(s.split("[")[0].split(".")[1:])
    hit = toks & WIDGET_MARKERS
    return sorted(hit)[0] if hit else None

def widgets(lines):
    """yield (type, position, wrapper-label) for every OUTERMOST widget node in the body"""
    bi = None
    for i, l in enumerate(lines):
        if l.strip().startswith("div#body") and ind(l) <= 4:
            bi = i; break
    if bi is None: return []
    base = ind(lines[bi])
    out = []
    i = bi + 1
    stack = []   # (indent, label)
    while i < len(lines) and ind(lines[i]) > base:
        l = lines[i]; d = ind(l)
        while stack and stack[-1][0] >= d: stack.pop()
        t = wtype(l)
        if t:
            depth = d - base
            anc = [s[1].strip() for s in stack]
            nest = next((a for a in reversed(anc) if a.startswith("div.activity") or a.startswith("div.alert") or "Panel" in a), None)
            if nest:
                pos = "deep:" + ("activity" if "activity" in nest else "alert" if "alert" in nest else "panel")
            elif depth == 2:
                pos = "row-is-widget" if ".row" in l.strip().split("[")[0].replace("div.", ".") else "top-level"
            elif depth == 4 and anc and anc[-1].startswith("div.row"):
                pos = "row>widget"
            elif depth == 6 and len(anc) >= 2 and anc[-2].startswith("div.row") and anc[-1].startswith("div.col"):
                pos = "in-col"
            else:
                pos = f"deep:{depth}"
            out.append((t, pos, l.strip().split("[")[0]))
            # skip the subtree
            j = i + 1
            while j < len(lines) and ind(lines[j]) > d: j += 1
            i = j
            continue
        stack.append((d, l))
        i += 1
    return out

fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
meta = load_meta()
agg = defaultdict(lambda: {"gold": defaultdict(Counter), "claude": defaultdict(Counter), "gwrap": defaultdict(Counter), "cwrap": defaultdict(Counter), "pages": 0})
for code in sorted(fam):
    if flt and not code.startswith(flt): continue
    tf = fam[code]
    mm = meta.get(code, {})
    subject = mm.get("subject") or "None"
    for n, cp, hp in pairs(code):
        if SKIP.search(os.path.basename(hp)) or SKIP.search(os.path.basename(cp)): continue
        try:
            g = widgets(_skel(hp, False)); c = widgets(_skel(cp, False))
        except Exception:
            continue
        for k in ("ALL", f"template={tf}"):
            A = agg[k]; A["pages"] += 1
            for t, pos, w in g: A["gold"][t][pos] += 1; A["gwrap"][t][w] += 1
            for t, pos, w in c: A["claude"][t][pos] += 1; A["cwrap"][t][w] += 1

def line(c):
    t = sum(c.values()) or 1
    return ", ".join(f"{k} {v} ({v/t:.2f})" for k, v in c.most_common(5))
for k in ("ALL", "template=Standard", "template=Inquiry", "template=Fundamentals", "template=Bilingual"):
    A = agg[k]
    if not A["pages"]: continue
    print(f"\n== {k} — pages {A['pages']}")
    types = sorted(set(A["gold"]) | set(A["claude"]), key=lambda t: -(sum(A["gold"][t].values()) + sum(A["claude"][t].values())))
    for t in types:
        gt = sum(A["gold"][t].values()); ct = sum(A["claude"][t].values())
        if gt + ct < 10: continue
        print(f"  {t:16s} gold   n={gt:4d}: {line(A['gold'][t])}")
        print(f"  {'':16s} claude n={ct:4d}: {line(A['claude'][t])}")
        print(f"  {'':16s} wrappers gold: {line(A['gwrap'][t])} | claude: {line(A['cwrap'][t])}")
