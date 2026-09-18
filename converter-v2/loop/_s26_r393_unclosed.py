#!/usr/bin/env python3
"""THE GOLD'S UNCLOSED ROW: a `div.row` whose first `div.row` child follows a column (the row was never closed, so the next
rows nest inside it). For each such event: the column's LAST child (tag/class) and its first child; the same census for the
CLOSED rows (last child of the last column) → consensus per block type. Pages / modules / subjects. python3 _s26_r393_unclosed.py"""
import os, sys, re
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
sys.path.insert(0, OUTPUTS)
src = open(os.path.join(OUTPUTS, "_s26_r392_adjul.py"), encoding="utf-8").read()
exec(src[:src.index("ADJ = re.compile")])
from collections import Counter, defaultdict
TAG = re.compile(r"<(/?)([a-z][a-z0-9]*)\b([^>]*)>", re.I)
CLS = re.compile(r'class="([^"]*)"'); ID = re.compile(r'id="([^"]*)"')
VOID = {"br", "img", "input", "hr", "meta", "link", "source", "wbr"}
def events(s):
    """returns list of (kind, col_last_child, col_first_child, depth) — kind 'UNCLOSED' when a div.row's child div.row directly
    follows a column child; 'CLOSED' for a div.row that closes with its last child a column."""
    st = []; out = []
    for m in TAG.finditer(s):
        closing, tag, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID and not closing:
            if st: st[-1][1].append(tag)
            continue
        if closing:
            if st:
                ent = st.pop()
                if ent[0] == "div.row" and ent[1] and ent[1][-1].startswith("div.col") and not ent[3]:
                    out.append(("CLOSED", ent[2].get(len(ent[1]) - 1, ["(empty)"])[-1], ent[2].get(len(ent[1]) - 1, ["(empty)"])[0], len(st)))
            continue
        c = CLS.search(attrs); cls = c.group(1).strip() if c else ""; i = ID.search(attrs)
        label = tag + ("#" + i.group(1) if i else "") + (("." + ".".join(cls.split())) if cls else "")
        if st:
            par = st[-1]
            if par[0] == "div.row" and label.startswith("div.row") and par[1] and par[1][-1].startswith("div.col") and not par[3]:
                par[3] = True
                k = len(par[1]) - 1
                out.append(("UNCLOSED", par[2].get(k, ["(empty)"])[-1], par[2].get(k, ["(empty)"])[0], len(st)))
            par[1].append(label)
            if len(st) >= 2 and st[-2][0] == "div.row" and par[0].startswith("div.col"):
                st[-2][2].setdefault(len(st[-2][1]) - 1, []).append(label)
        st.append([label, [], {}, False])
    return out
U = Counter(); Cc = Counter(); UP = set(); UM = set(); US = Counter(); UF = Counter(); EX = []
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"
    for n, cp, hp in pairs(code):
        try: gh = body(open(hp, encoding="utf-8", errors="replace").read())
        except Exception: continue
        gl = "".join(live_pieces(gh))
        for kind, last, first, depth in events(gl):
            key = last
            if kind == "UNCLOSED":
                U[key] += 1; UP.add(hp); UM.add(code); US[f"{tf}/{subj}"] += 1; UF[first] += 1
                if len(EX) < 6: EX.append(f"{os.path.basename(hp)} last «{last}» first «{first}» depth {depth}")
            else: Cc[key] += 1
print(f"gold UNCLOSED-row events: {sum(U.values())} on {len(UP)} pages / {len(UM)} modules; CLOSED rows {sum(Cc.values())}")
print("by group:", US.most_common(10))
print("the column's LAST child before the un-closure (unclosed / closed → share):")
for k, n in U.most_common(14): print(f"   {n:4d} / {Cc.get(k, 0):5d} → {n/(n+Cc.get(k,0)):.2f}   {k}")
print("the column's FIRST child in unclosed rows:", UF.most_common(8))
print("examples:"); [print("  ", e) for e in EX]
