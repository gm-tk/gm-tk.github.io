#!/usr/bin/env python3
"""Session 25 — PAIR every Claude row-opening heading (h2 / h3 / h4 / h5 at the head of a top-level body row) with the
gold's element of the same text, and report WHERE the gold put it (its level + position: row-open / inline / col-open /
nested inside an activity / alert / panel / repeat) and what the gold's PREVIOUS top-level sibling was — the row census
(_s25_rowcol.py) shows Claude opening 933 more h3 rows than the gold in Standard. Uses the miner's text-bearing
page_lines (the gate's own skeleton with text alongside).
  python3 _s25_h3pair.py [h3|h2|h4|h5] [prefix-filter]"""
import os, sys, re, json
from collections import Counter, defaultdict
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS)
import _corpus
from _diff_miner import page_lines, unorm
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, HUMAN
from _measure_ceiling import load_meta
SKIP = re.compile(r"acks|acknowledge|glossary|references", re.I)
args = [a for a in sys.argv[1:] if not a.startswith("--")]
LEVEL = args[0] if args else "h3"
PANELS = "--panels" in sys.argv
flt = args[1] if len(args) > 1 else ""

def fold(t):
    return re.sub(r"[^a-z0-9]+", " ", unorm(t or "").lower()).strip()

def kind(sig):
    s = sig
    if s == "WIDGET": return "WIDGET"
    if s.startswith("div.activity"): return "activity"
    if s.startswith("div.alert"): return "alert"
    if "Panel" in s or s.startswith("div.introduction"): return "panel"
    if s.startswith("div.row"): return "row"
    if s.startswith("div.col"): return "col"
    m = re.match(r"(h[1-6])\b", s)
    if m: return m.group(1)
    if s == "p" or s.startswith("p."): return "p"
    if s.startswith("img"): return "img"
    if s.startswith("ul") or s.startswith("ol"): return "list"
    if "videoSection" in s: return "video"
    if s.startswith("table") or "table-responsive" in s: return "table"
    return s.split(".")[0].split("[")[0]

def analyse(lines):
    """for each heading line: (idx, level, text, position, prev_kind, ancestors-kinds)"""
    # body index
    bi = next((i for i, l in enumerate(lines) if l.sig.startswith("div#body")), None)
    if bi is None: return []
    base = lines[bi].depth
    stack = []   # [depth, kind, nkids, colidx]
    heads = []
    prev_top = None   # kind of the previous top-level sibling's LAST leaf-ish content (its first column's last child)
    last_top_kind = None
    prev_sib = {}
    for i in range(bi + 1, len(lines)):
        ln = lines[i]; d = ln.depth
        if d <= base: break
        while stack and stack[-1][0] >= d: stack.pop()
        parent = stack[-1] if stack else None
        cidx = parent[2] if parent else 0
        if parent: parent[2] += 1
        k = kind(ln.sig)
        m = re.match(r"(h[2-6])\b", ln.sig)
        if m:
            anc = [s[1] for s in stack]
            nest = next((a for a in reversed(anc) if a in ("activity", "alert", "WIDGET", "table", "list") or (a == "panel" and not PANELS)), None)
            depth = d - base
            if nest: pos = "nested:" + nest
            elif PANELS and len(anc) >= 3 and anc[-1] == "col" and anc[-2] == "row" and anc[-3] == "panel":
                colidx = stack[-1][3]
                pos = ("row-open" if colidx == 0 else "col-open") if cidx == 0 else "inline"
            elif depth == 3 and len(anc) >= 2 and anc[-1] == "col" and anc[-2] == "row":
                colidx = stack[-1][3]
                pos = ("row-open" if colidx == 0 else "col-open") if cidx == 0 else "inline"
            elif depth == 1: pos = "top-level"
            else: pos = "deep"
            prevk = prev_sib.get(id(parent), "-") if parent else "-"
            heads.append((i, m.group(1), fold(ln.text), pos, prevk, last_top_kind))
        if parent: prev_sib[id(parent)] = k
        if d == base + 1:
            last_top_kind = k
        entry = [d, k, 0, cidx if (k == "col" and parent and parent[1] == "row") else 0]
        stack.append(entry)
    return heads

fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
meta = load_meta()
agg = defaultdict(Counter); agg_prev = defaultdict(Counter); pagesets = defaultdict(set); modsets = defaultdict(set)
examples = defaultdict(list)
npages = 0
for code in sorted(fam):
    if flt and not code.startswith(flt): continue
    tf = fam[code]
    subject = (meta.get(code, {}) or {}).get("subject") or "None"
    for n, cp, hp in pairs(code):
        if SKIP.search(os.path.basename(hp)) or SKIP.search(os.path.basename(cp)): continue
        try:
            g, _ = page_lines(hp); c, _ = page_lines(cp)
        except Exception:
            continue
        npages += 1
        gh = analyse(g); ch = analyse(c)
        gidx = defaultdict(list)
        for h in gh: gidx[h[2]].append(h)
        for (i, lv, txt, pos, prevk, lasttop) in ch:
            if lv != LEVEL or pos != "row-open": continue
            if not txt: continue
            cand = gidx.get(txt)
            if not cand:
                verdict = "NOT-IN-GOLD"
            else:
                gp = cand[0]
                verdict = f"gold {gp[1]} {gp[3]}" + (f" after {gp[4]}" if gp[3] == "inline" else "")
            ptype = "overview" if n == 0 else "lesson"
            for k in ("ALL", f"template={tf}", f"template+ptype={tf}/{ptype}", f"subject={subject}", f"subject+ptype={subject}/{ptype}", f"series={code[:5]}"):
                agg[k][verdict] += 1
                pagesets[(k, verdict)].add(cp); modsets[(k, verdict)].add(code)
            if len(examples[verdict]) < 4:
                examples[verdict].append((code, os.path.basename(cp), txt[:60]))

print(f"Claude row-opening {LEVEL} → where the gold puts the same-text heading; pages scanned {npages}")
for k in sorted(agg, key=lambda k: (0 if k == "ALL" else 1 if k.startswith("template=") else 2 if k.startswith("subject=") else 3, -sum(agg[k].values()))):
    tot = sum(agg[k].values())
    if tot < 30: continue
    print(f"\n== {k} — Claude row-open {LEVEL}: {tot}")
    for v, n in agg[k].most_common(14):
        print(f"   {v:34s} {n:5d} ({n/tot:.2f})  pages {len(pagesets[(k, v)]):4d} / modules {len(modsets[(k, v)]):3d}")
print("\nexamples:")
for v, ex in examples.items():
    print(" ", v, "→", ex)
