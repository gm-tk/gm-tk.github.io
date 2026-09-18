#!/usr/bin/env python3
"""Session 25 — the ROW / COLUMN COMPOSITION census of the top-level body (#body > div.row > div.col-*), gold vs Claude,
per template family / subject / page type. The r51 row-grouping rule ("only a heading / activity / callout breaks a row")
was mined on 370 pages in June 2026 and never re-measured at the COLUMN level: does the gold open a new ROW or a new
COLUMN (in the same row) at a heading, and does a widget sit in its own row or is its wrapper the row?
Reads the skeleton gate's own pairing + scaffold skeleton (widgets collapsed).
  python3 _s25_rowcol.py [prefix-filter] [--json OUT] [--pages]"""
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
want_pages = "--pages" in sys.argv
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
    if s.startswith("div.activity"): return "activity"
    if s.startswith("div.alert"): return "alert"
    if s.startswith("div.") and "videoSection" in s: return "video"
    if s.startswith("div.whakatauki"): return "whakatauki"
    if s.startswith("div.table-responsive") or s.startswith("table"): return "table"
    if s.startswith("┌"): return "repeat"
    if re.match(r"h[1-6]\b", s): return s[:2]
    if s.startswith("img"): return "img"
    if s.startswith("p") and (len(s) == 1 or s[1] in ".>[ "): return "p"
    if s.startswith("ul") or s.startswith("ol"): return "list"
    if s.startswith("a") and (len(s) == 1 or s[1] in ".>[ "): return "a"
    if s.startswith("iframe"): return "iframe"
    if s.startswith("br"): return "br"
    if s.startswith("div.row"): return "row"
    if s.startswith("div.col"): return "col"
    if s.startswith("div."): return "div." + s[4:].split(".")[0].split("[")[0]
    if s.startswith("div"): return "div"
    return s.split(".")[0].split("[")[0]

def width(lbl):
    s = lbl.strip()
    if not s.startswith("div.col"): return s.split("[")[0]
    toks = s[4:].split(".")
    keep = [t for t in toks if t.startswith("col") or t.startswith("offset")]
    return ".".join(keep) if keep else s

def body_children(lines):
    """top-level children of div#body: list of (label, [children-labels (indent+2)], [grandchildren by child])"""
    bi = None
    for i, l in enumerate(lines):
        if l.strip().startswith("div#body") and ind(l) <= 4:
            bi = i; break
    if bi is None: return None
    base = ind(lines[bi])
    out = []   # (label, cols) where cols = [(label, [first-level kids labels])]
    i = bi + 1
    n = len(lines)
    while i < n and ind(lines[i]) > base:
        if ind(lines[i]) == base + 2:
            top = lines[i]
            j = i + 1
            cols = []
            while j < n and ind(lines[j]) > base + 2:
                if ind(lines[j]) == base + 4:
                    col = lines[j]
                    k = j + 1
                    kids = []
                    while k < n and ind(lines[k]) > base + 4:
                        if ind(lines[k]) == base + 6:
                            kids.append(lines[k])
                        k += 1
                    cols.append((col, kids))
                    j = k
                else:
                    j += 1
            out.append((top, cols))
            i = j
        else:
            i += 1
    return out

fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
meta = load_meta()

class Agg:
    def __init__(self):
        self.pages = 0
        self.top = Counter()          # top-level child kind: row / WIDGET / other
        self.rowlabel = Counter()     # the row's own label (div.row / div.row.carousel …)
        self.cols_per_row = Counter() # 1 / 2 / 3+
        self.rows = 0
        self.cols = 0
        self.cols_in_multi = 0
        self.head_col_pos = Counter() # for a column whose first child is h2/h3/h4: "opens-row" / "continues-row"
        self.head_col_only = Counter()# "heading-only" / "heading+content"
        self.row_opener = Counter()   # kind of the first column's first child
        self.col_opener_cont = Counter()  # kind of the first child of a CONTINUING column
        self.multi_pattern = Counter()    # width sequence of multi-column rows (first 4)
        self.widget_top = Counter()   # how a widget sits: "top-level" (own line under #body) / "in-col" (first child of a col) / "row-is-widget"
        self.per_page_rows = []
    def feed(self, tops):
        self.pages += 1
        nrows = 0
        for top, cols in tops:
            k = kind(top)
            if k == "row":
                nrows += 1
                self.top["row"] += 1
                self.rowlabel[top.strip().split("[")[0]] += 1
                nc = len(cols)
                self.rows += 1
                self.cols += nc
                self.cols_per_row["1" if nc == 1 else ("2" if nc == 2 else "3+")] += 1
                if nc >= 2:
                    self.cols_in_multi += nc
                    self.multi_pattern[",".join(width(c) for c, _ in cols[:4]) + ("…" if nc > 4 else "")] += 1
                for ci, (col, kids) in enumerate(cols):
                    fk = kind(kids[0]) if kids else "-"
                    if ci == 0:
                        self.row_opener[fk] += 1
                    else:
                        self.col_opener_cont[fk] += 1
                    if fk in ("h2", "h3", "h4"):
                        self.head_col_pos["opens-row" if ci == 0 else "continues-row"] += 1
                        self.head_col_only["heading-only" if len(kids) == 1 else "heading+content"] += 1
                    if fk == "WIDGET":
                        self.widget_top["in-col"] += 1
            elif k == "WIDGET":
                self.top["WIDGET"] += 1
                self.widget_top["top-level"] += 1
            else:
                self.top["other:" + k] += 1
        self.per_page_rows.append(nrows)

def pct(c, key, denom=None):
    d = denom if denom is not None else sum(c.values())
    return f"{c[key]}/{d}={c[key]/d:.2f}" if d else "0/0"

groups = defaultdict(lambda: {"gold": Agg(), "claude": Agg()})
page_rows = []
codes = sorted(fam)
for code in codes:
    if flt and not code.startswith(flt): continue
    tf = fam[code]
    mm = meta.get(code, {})
    subject = mm.get("subject") or "None"
    for n, cp, hp in pairs(code):
        if SKIP.search(os.path.basename(hp)) or SKIP.search(os.path.basename(cp)): continue
        try:
            g = body_children(_skel(hp, True)); c = body_children(_skel(cp, True))
        except Exception as e:
            continue
        if g is None or c is None: continue
        ptype = "overview" if n == 0 else "lesson"
        keys = ["ALL", f"template={tf}", f"template+ptype={tf}/{ptype}", f"subject={subject}", f"subject+ptype={subject}/{ptype}"]
        for k in keys:
            groups[k]["gold"].feed(g); groups[k]["claude"].feed(c)
        gr = sum(1 for t, _ in g if kind(t) == "row"); cr = sum(1 for t, _ in c if kind(t) == "row")
        gm = sum(1 for t, cols in g if kind(t) == "row" and len(cols) >= 2)
        page_rows.append((code, os.path.basename(cp), tf, subject, ptype, gr, cr, gm))

def show(name, G, C):
    print(f"\n== {name} — pages {G.pages}")
    for side, A in (("gold", G), ("claude", C)):
        rows = A.rows or 1
        print(f"  [{side}] top-level: " + ", ".join(f"{k} {v}" for k, v in A.top.most_common(6)))
        print(f"  [{side}] rows {A.rows} (mean/page {A.rows/max(A.pages,1):.1f}); cols/row: " +
              ", ".join(f"{k} {v} ({v/rows:.2f})" for k, v in sorted(A.cols_per_row.items())) +
              f"; cols in multi-col rows {A.cols_in_multi}/{A.cols} = {A.cols_in_multi/max(A.cols,1):.2f}")
        print(f"  [{side}] row labels: " + ", ".join(f"{k} {v}" for k, v in A.rowlabel.most_common(5)))
        hp = sum(A.head_col_pos.values()) or 1
        print(f"  [{side}] heading-led columns {hp}: opens-row {A.head_col_pos['opens-row']} ({A.head_col_pos['opens-row']/hp:.2f}) / continues-row {A.head_col_pos['continues-row']} ({A.head_col_pos['continues-row']/hp:.2f}); "
              f"heading-only {A.head_col_only['heading-only']} ({A.head_col_only['heading-only']/hp:.2f}) / heading+content {A.head_col_only['heading+content']}")
        print(f"  [{side}] row openers: " + ", ".join(f"{k} {v}" for k, v in A.row_opener.most_common(8)))
        print(f"  [{side}] continuing-column openers: " + ", ".join(f"{k} {v}" for k, v in A.col_opener_cont.most_common(8)))
        print(f"  [{side}] multi-col patterns: " + ", ".join(f"{k} {v}" for k, v in A.multi_pattern.most_common(6)))
        print(f"  [{side}] widgets: " + ", ".join(f"{k} {v}" for k, v in A.widget_top.most_common()))

order = sorted(groups, key=lambda k: (0 if k == "ALL" else 1 if k.startswith("template=") else 2 if k.startswith("template+") else 3 if k.startswith("subject=") else 4, -groups[k]["gold"].pages))
for k in order:
    if groups[k]["gold"].pages < 10: continue
    show(k, groups[k]["gold"], groups[k]["claude"])

if want_pages:
    print("\n== per-page rows (gold / Claude / gold multi-col rows) — pages where gold has ≥ 2 multi-col rows")
    for r in sorted(page_rows, key=lambda r: -r[7])[:40]:
        print("  ", r)
if jout:
    json.dump({"pages": page_rows}, open(jout, "w"), indent=0)
    print("wrote", jout)
