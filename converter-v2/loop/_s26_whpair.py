#!/usr/bin/env python3
"""Session 26 — the PAIRED whakatauki after-rule (the session-25 lesson: a gold-side census must survive pairing).
For every Claude `div.whakatauki` that is a direct child of a top-level body column: take the FIRST content element
of the NEXT top-level row on Claude's page (the element the r51 after-break pushed into a fresh row).  If it is a
heading / activity / callout / widget the fix would not touch it (those open a row anyway) → 'untouched'.  Otherwise
find the same text on the gold page and ask: is it inside the SAME top-level column as the gold's whakatauki (FLOW —
the fix matches the gold) or in a different top-level row (BREAK — the fix would regress) or nowhere (editorial)?
Per template / subject; the module list of the FLOW pages = the probe's ON set.
  python3 _s26_whpair.py"""
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
from anchor_compare import CLAUDE
from _measure_ceiling import load_meta
SKIP = re.compile(r"acks|acknowledge|glossary|references", re.I)
TEXT_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "td", "th", "b", "strong", "a", "span", "label", "caption", "figcaption", "button", "i", "em")
OPENERS = ("h1", "h2", "h3", "h4", "h5", "h6")   # a heading opens a row under r51 regardless

def fold(t): return re.sub(r"[^a-z0-9]+", " ", unorm(t or "").lower()).strip()
def tag_of(sig):
    m = re.match(r"([a-z0-9]+)", sig); return m.group(1) if m else sig

def top_rows(lines):
    """indices of #body's direct div.row lines and, for each, its top-level column line indices"""
    bi = next((i for i, l in enumerate(lines) if l.sig.startswith("div#body")), None)
    if bi is None: return []
    base = lines[bi].depth
    rows = []
    for i in range(bi + 1, len(lines)):
        if lines[i].depth <= base: break
        if lines[i].depth == base + 1 and lines[i].sig.startswith("div.row"):
            rows.append(i)
    return rows

def subtree(lines, i):
    d = lines[i].depth; j = i + 1
    while j < len(lines) and lines[j].depth > d: j += 1
    return j   # exclusive end

fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
meta = load_meta()
R = defaultdict(Counter); ON = defaultdict(set); ONmods = defaultdict(set); EX = defaultdict(list)
for code in sorted(fam):
    tf = fam[code]
    subject = (meta.get(code, {}) or {}).get("subject") or "None"
    for n, cp, hp in pairs(code):
        if SKIP.search(os.path.basename(hp)) or SKIP.search(os.path.basename(cp)): continue
        try:
            g, _ = page_lines(hp); c, _ = page_lines(cp)
        except Exception:
            continue
        crows = top_rows(c); grows = top_rows(g)
        if not crows: continue
        # gold: map fold(text) -> index of the top-level row that contains it
        g_row_of = {}
        for ri, r in enumerate(grows):
            end = subtree(g, r)
            for k in range(r + 1, end):
                if g[k].text and tag_of(g[k].sig) in TEXT_TAGS:
                    g_row_of.setdefault(fold(g[k].text), ri)
        g_wh_rows = set()
        for ri, r in enumerate(grows):
            end = subtree(g, r)
            if any(g[k].sig.startswith("div.whakatauki") for k in range(r + 1, end)): g_wh_rows.add(ri)
        keys = ("ALL", f"template={tf}", f"tmpl+subj={tf}/{subject}")
        for ri, r in enumerate(crows):
            end = subtree(c, r)
            wh = [k for k in range(r + 1, end) if c[k].sig.startswith("div.whakatauki")]
            if not wh: continue
            # the whakatauki must be the row's last content (the r51 after-break) — then the next row's first content
            if ri + 1 >= len(crows):
                for k in keys: R[k]["page-end"] += 1
                continue
            nr = crows[ri + 1]; nend = subtree(c, nr)
            first = next((k for k in range(nr + 1, nend) if not c[k].sig.startswith(("div.row", "div.col-"))), None)
            if first is None:
                for k in keys: R[k]["next-row-empty"] += 1
                continue
            fs = c[first].sig; ftag = tag_of(fs)
            if ftag in OPENERS or fs.startswith(("div.activity", "div.alert", "div.whakatauki", "div.wananga", "div.quoteText", "WIDGET", "div.row.supervisor")):
                for k in keys: R[k]["untouched:" + (ftag if ftag in OPENERS else fs.split("[")[0].split(".")[1] if "." in fs else fs)] += 1
                continue
            # a text-bearing element: p / list / img / video …  find its (first) text on the gold page
            txt = None
            for k in range(first, nend):
                if c[k].text and tag_of(c[k].sig) in TEXT_TAGS: txt = fold(c[k].text); break
            if txt is None:
                for k in keys: R[k]["next-no-text:" + ftag] += 1
                continue
            gri = g_row_of.get(txt)
            if gri is None:
                verdict = "gold-nowhere"
            elif gri in g_wh_rows:
                verdict = "FLOW (gold same row as its whakatauki)"
            else:
                verdict = "BREAK (gold new row)"
            for k in keys: R[k][verdict] += 1
            if verdict.startswith("FLOW"):
                ON[tf].add(os.path.basename(cp)); ONmods[tf].add(code)
            if len(EX[verdict]) < 6: EX[verdict].append(f"{os.path.basename(cp)[:-5]} {ftag} «{(c[first].text or txt)[:40]}»")

def show(k):
    c = R[k]; tot = sum(c.values())
    if not tot: return
    fl = c["FLOW (gold same row as its whakatauki)"]; br = c["BREAK (gold new row)"]
    print(f"\n== {k}: Claude whakatauki rows {tot}; paired FLOW {fl} / BREAK {br} → flow share {fl/max(fl+br,1):.2f}")
    for x, v in c.most_common(): print(f"   {v:4d}  {x}")
show("ALL")
for k in sorted(K for K in R if K.startswith("template=")): show(k)
for k in sorted(K for K in R if K.startswith("tmpl+subj=")): show(k)
print("\n== examples ==")
for v, ex in EX.items(): print(f"   {v}: " + " | ".join(ex[:5]))
print("\n== ON set (FLOW pages) ==")
for tf in ON: print(f"   {tf}: {len(ON[tf])} pages / {len(ONmods[tf])} modules: {' '.join(sorted(ONmods[tf]))}")
