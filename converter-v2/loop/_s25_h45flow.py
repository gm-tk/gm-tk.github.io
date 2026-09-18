#!/usr/bin/env python3
"""Session 25 — SIMULATE "a minor heading (h5 / h4) FLOWS into the current row instead of opening a new one" on the
gate's own scorer (difflib ratio over the scaffold skeleton, autojunk=False), page by page, before any engine change.
For every Claude top-level row whose single col-12.col-md-8 column opens with the target heading level, and whose
previous top-level sibling is a plain div.row with a single col-12.col-md-8 column (not ending in an activity), the
row + column lines are removed so the heading and its followers join the previous column. Reports per template /
subject / series: pages touched, up / down, pp-sum, mean delta.
  python3 _s25_h45flow.py h5|h4|h4h5 [prefix-filter] [--json OUT]"""
import os, sys, re, json, difflib
from collections import Counter, defaultdict
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
sys.path.insert(0, TESTS)
import _corpus
from _skeleton_compare import _skel
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, HUMAN
from _measure_ceiling import load_meta
SKIP = re.compile(r"acks|acknowledge|glossary|references", re.I)
argv = list(sys.argv[1:])
jout = None
if "--json" in argv:
    i = argv.index("--json"); jout = argv[i + 1]; del argv[i:i + 2]
args = [a for a in argv if not a.startswith("--")]
mode = args[0] if args else "h5"
flt = args[1] if len(args) > 1 else ""
LEVELS = {"h5": ("h5",), "h4": ("h4",), "h4h5": ("h4", "h5"), "h3": ("h3",), "pick": ("h4", "h5")}[mode]
H4_SUBJECTS = {"NCEA1", "1-10 Mathematics", "Leaving to Learn"}   # the pick scope: h4 flows only in these subject groups
DEFAULT_COL = "div.col-12.col-md-8"
LEVELS_DEFAULT = LEVELS

def ind(l): return len(l) - len(l.lstrip(" "))

def top_children(lines):
    """indices of the top-level children of div#body, and the body's indent"""
    bi = None
    for i, l in enumerate(lines):
        if l.strip().startswith("div#body") and ind(l) <= 4:
            bi = i; break
    if bi is None: return None, None
    base = ind(lines[bi])
    idx = []
    i = bi + 1
    while i < len(lines) and ind(lines[i]) > base:
        if ind(lines[i]) == base + 2: idx.append(i)
        i += 1
    return base, idx

def block_end(lines, i):
    d = ind(lines[i]); j = i + 1
    while j < len(lines) and ind(lines[j]) > d: j += 1
    return j

def simulate(lines, levels=None):
    """return (new_lines, n_merged, n_candidates)"""
    LEVELS = levels or LEVELS_DEFAULT
    base, tops = top_children(lines)
    if base is None: return lines, 0, 0
    drop = set(); merged = 0; cands = 0
    for k, i in enumerate(tops):
        row = lines[i].strip()
        if row != "div.row": continue
        end = block_end(lines, i)
        # single column?
        cols = [j for j in range(i + 1, end) if ind(lines[j]) == base + 4]
        if len(cols) != 1 or lines[cols[0]].strip() != DEFAULT_COL: continue
        kids = [j for j in range(cols[0] + 1, end) if ind(lines[j]) == base + 6]
        if not kids: continue
        first = lines[kids[0]].strip()
        if not any(first == lv or first.startswith(lv + ".") or first.startswith(lv + "[") for lv in LEVELS): continue
        cands += 1
        if k == 0: continue
        p = tops[k - 1]
        if p in drop: pass   # the previous row was itself merged — its content now sits in the row before; still mergeable
        prow = lines[p].strip()
        if prow != "div.row": continue
        pend = block_end(lines, p)
        pcols = [j for j in range(p + 1, pend) if ind(lines[j]) == base + 4]
        if len(pcols) != 1 or lines[pcols[0]].strip() != DEFAULT_COL: continue
        pkids = [j for j in range(pcols[0] + 1, pend) if ind(lines[j]) == base + 6]
        if not pkids: continue
        last = lines[pkids[-1]].strip()
        if last.startswith("div.activity") or last == "WIDGET": continue
        drop.add(i); drop.add(cols[0]); merged += 1
    if not merged: return lines, 0, cands
    return [l for j, l in enumerate(lines) if j not in drop], merged, cands

fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
meta = load_meta()
res = defaultdict(lambda: {"pages": 0, "touched": 0, "up": 0, "down": 0, "flat": 0, "sum": 0.0, "merged": 0, "cands": 0})
rows = []
for code in sorted(fam):
    if flt and not code.startswith(flt): continue
    tf = fam[code]
    mm = meta.get(code, {})
    subject = mm.get("subject") or "None"
    for n, cp, hp in pairs(code):
        if SKIP.search(os.path.basename(hp)) or SKIP.search(os.path.basename(cp)): continue
        try:
            g = _skel(hp, True); c = _skel(cp, True)
        except Exception:
            continue
        if mode == "pick":
            if tf != "Standard": continue
            lv = ("h4", "h5") if subject in H4_SUBJECTS else ("h5",)
            c2, merged, cands = simulate(c, lv)
        else:
            c2, merged, cands = simulate(c)
        keys = ["ALL", f"template={tf}", f"subject={subject}", f"series={code[:5]}"]
        for k in keys:
            res[k]["pages"] += 1; res[k]["cands"] += cands
        if not merged: continue
        r0 = difflib.SequenceMatcher(None, g, c, autojunk=False).ratio()
        r1 = difflib.SequenceMatcher(None, g, c2, autojunk=False).ratio()
        d = (r1 - r0) * 100
        for k in keys:
            R = res[k]; R["touched"] += 1; R["merged"] += merged; R["sum"] += d
            if d > 0.05: R["up"] += 1
            elif d < -0.05: R["down"] += 1
            else: R["flat"] += 1
        rows.append((code, os.path.basename(cp), tf, subject, merged, round(r0 * 100, 2), round(r1 * 100, 2), round(d, 2)))

order = sorted(res, key=lambda k: (0 if k == "ALL" else 1 if k.startswith("template=") else 2 if k.startswith("subject=") else 3, -res[k]["pages"]))
print(f"mode {mode}: merge a row-opening {LEVELS} into the previous plain col-md-8 row")
for k in order:
    R = res[k]
    if R["touched"] == 0: continue
    if k.startswith("series=") and R["touched"] < 3: continue
    print(f"  {k:48s} pages {R['pages']:5d} touched {R['touched']:4d} (cands {R['cands']:4d}, merged {R['merged']:4d})  up {R['up']:4d} / down {R['down']:4d} / flat {R['flat']:3d}  pp-sum {R['sum']:+8.1f}  mean/touched {R['sum']/max(R['touched'],1):+.2f}")
print("\nworst 12 pages:")
for r in sorted(rows, key=lambda r: r[7])[:12]: print("  ", r)
print("best 8 pages:")
for r in sorted(rows, key=lambda r: -r[7])[:8]: print("  ", r)
if jout:
    json.dump({"mode": mode, "pages": rows}, open(jout, "w"))
    print("wrote", jout)
