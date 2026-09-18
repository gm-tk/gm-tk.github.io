#!/usr/bin/env python3
"""Session 25 — WHERE a heading (h2 / h3 / h4 / h5) and an alert box SIT in the body, gold vs Claude, per template /
subject / page type: 'row-open' (first child of the first column of a top-level #body row), 'col-open' (first child of
a later column in that row), 'inline' (a later child of a top-level column — it FLOWS after content), or nested inside
an activity / alert / panel / other. The r51 row rule breaks a row at every heading and boxed callout; the row census
(_s25_rowcol.py) shows Claude opening 930 more h3 rows, 386 more h4 rows and 390 more alert rows than the gold.
  python3 _s25_headpos.py [prefix-filter] [--json OUT]"""
import os, sys, re, json
from collections import Counter, defaultdict
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
sys.path.insert(0, TESTS)
import _corpus
from _skeleton_compare import _skel
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, HUMAN
from _measure_ceiling import load_meta
SKIP = re.compile(r"acks|acknowledge|glossary|references", re.I)
jout = None
argv = list(sys.argv[1:])
if "--json" in argv:
    i = argv.index("--json"); jout = argv[i + 1]; del argv[i:i + 2]
args = [a for a in argv if not a.startswith("--")]
flt = args[0] if args else ""

def ind(l): return len(l) - len(l.lstrip(" "))

def kind(lbl):
    s = lbl.strip()
    if s == "WIDGET": return "WIDGET"
    if s.startswith("┌"): return "repeat"
    if s.startswith("div.activity"): return "activity"
    if s.startswith("div.alert"): return "alert"
    if s.startswith("div.") and ("Panel" in s or s.startswith("div.introduction")): return "panel"
    if s.startswith("div.row"): return "row"
    if s.startswith("div.col"): return "col"
    m = re.match(r"(h[1-6])\b", s)
    if m: return m.group(1)
    if s.startswith("p") and (len(s) == 1 or s[1] in ".>[ "): return "p"
    if s.startswith("img"): return "img"
    if s.startswith("ul") or s.startswith("ol"): return "list"
    if s.startswith("div.") and "videoSection" in s: return "video"
    if s.startswith("div.table-responsive") or s.startswith("table"): return "table"
    if s.startswith("div"): return "div"
    return s.split(".")[0].split("[")[0]

TARGETS = ("h2", "h3", "h4", "h5", "alert", "img")
ROOTS = "panel" if "--panels" in sys.argv else "body"

def walk(lines):
    """yield (kind, position, prev_sibling_kind, level-context) for every target element in the body"""
    bi = None
    for i, l in enumerate(lines):
        if l.strip().startswith("div#body") and ind(l) <= 4:
            bi = i; break
    if bi is None: return []
    base = ind(lines[bi])
    out = []
    stack = []   # list of (indent, kind, child_index_counter_holder)
    # each stack entry: [indent, kind, nchildren_so_far]
    i = bi + 1
    n = len(lines)
    while i < n and ind(lines[i]) > base:
        l = lines[i]; d = ind(l); k = kind(l)
        while stack and stack[-1][0] >= d:
            stack.pop()
        parent = stack[-1] if stack else None
        child_idx = parent[2] if parent else 0
        if parent: parent[2] += 1
        # the "repeat" collapse line is transparent: its block sits one level deeper — treat its kids as the parent's
        if k in TARGETS:
            depth = d - base            # 2 = top-level child of #body, 4 = column level, 6 = inside a column
            anc = [s[1] for s in stack]
            # context: nested inside what?
            nest = None
            for a in reversed(anc):
                if a in ("activity", "alert", "WIDGET", "table", "list", "repeat") or (a == "panel" and ROOTS != "panel"):
                    nest = a; break
            if nest and not (nest == "repeat"):
                pos = "nested:" + nest
            elif len(anc) >= 3 and anc[-1] == "col" and anc[-2] == "row" and anc[-3] == "panel" and ROOTS == "panel":
                col_entry = stack[-1]
                col_idx = col_entry[3] if len(col_entry) > 3 else 0
                pos = ("row-open" if col_idx == 0 else "col-open") if child_idx == 0 else "inline"
            elif depth == 6 and len(anc) >= 2 and anc[-1] == "col" and anc[-2] == "row":
                # column-level element in a top-level row
                col_entry = stack[-1]; row_entry = stack[-2]
                col_idx = col_entry[3] if len(col_entry) > 3 else 0
                if child_idx == 0:
                    pos = "row-open" if col_idx == 0 else "col-open"
                else:
                    pos = "inline"
            elif depth == 6 and len(anc) >= 2 and anc[-2] == "row" and anc[-1] == "repeat":
                pos = "inline"
            elif depth == 2:
                pos = "top-level"
            elif depth == 4:
                pos = "row-child"
            else:
                pos = "deep:" + "/".join(anc[-2:])
            prev = out_prev.get(id(parent), "-") if parent else "-"
            out.append((k, pos, prev))
        # record the previous sibling kind for the NEXT child of this parent
        if parent:
            out_prev[id(parent)] = k
        # push self; a column records its index among the row's children
        entry = [d, k, 0]
        if k == "col" and parent and parent[1] == "row":
            entry.append(child_idx)
        stack.append(entry)
        i += 1
    return out

out_prev = {}

fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
meta = load_meta()

agg = defaultdict(lambda: {"gold": defaultdict(Counter), "claude": defaultdict(Counter), "pages": 0})
prevagg = defaultdict(lambda: {"gold": defaultdict(Counter), "claude": defaultdict(Counter)})
pagerows = []
for code in sorted(fam):
    if flt and not code.startswith(flt): continue
    tf = fam[code]
    mm = meta.get(code, {})
    subject = mm.get("subject") or "None"
    for n, cp, hp in pairs(code):
        if SKIP.search(os.path.basename(hp)) or SKIP.search(os.path.basename(cp)): continue
        try:
            out_prev.clear(); g = walk(_skel(hp, True))
            out_prev.clear(); c = walk(_skel(cp, True))
        except Exception as e:
            continue
        ptype = "overview" if n == 0 else "lesson"
        keys = ["ALL", f"template={tf}", f"template+ptype={tf}/{ptype}", f"subject={subject}", f"subject+ptype={subject}/{ptype}", f"series={code[:5]}"]
        for k in keys:
            agg[k]["pages"] += 1
            for kk, pos, prev in g:
                agg[k]["gold"][kk][pos] += 1
                if pos == "inline": prevagg[k]["gold"][kk][prev] += 1
            for kk, pos, prev in c:
                agg[k]["claude"][kk][pos] += 1
                if pos == "inline": prevagg[k]["claude"][kk][prev] += 1
        gi = sum(1 for kk, pos, _ in g if pos == "inline"); ci = sum(1 for kk, pos, _ in c if pos == "inline")
        pagerows.append((code, os.path.basename(cp), tf, subject, ptype, gi, ci))

def line(c):
    t = sum(c.values()) or 1
    return ", ".join(f"{k} {v} ({v/t:.2f})" for k, v in c.most_common(7))

order = sorted(agg, key=lambda k: (0 if k == "ALL" else 1 if k.startswith("template=") else 2 if k.startswith("template+") else 3 if k.startswith("subject=") else 4 if k.startswith("subject+") else 5, -agg[k]["pages"]))
for k in order:
    A = agg[k]
    if A["pages"] < 10: continue
    if k.startswith("series=") and A["pages"] < 20: continue
    print(f"\n== {k} — pages {A['pages']}")
    for kk in TARGETS:
        gt = sum(A["gold"][kk].values()); ct = sum(A["claude"][kk].values())
        if gt + ct < 10: continue
        print(f"  {kk:5s} gold   n={gt:5d}: {line(A['gold'][kk])}")
        print(f"  {kk:5s} claude n={ct:5d}: {line(A['claude'][kk])}")
        if prevagg[k]["gold"][kk] or prevagg[k]["claude"][kk]:
            print(f"        inline-after gold: {line(prevagg[k]['gold'][kk])} | claude: {line(prevagg[k]['claude'][kk])}")
if jout:
    json.dump({"pages": pagerows}, open(jout, "w"))
    print("wrote", jout)
