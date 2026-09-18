#!/usr/bin/env python3
"""THE OUTER BODY ROW: does the gold page's `div#body` hold one `div.row` whose direct children are themselves `div.row`s (the
wrapper form), or a flat sequence of `div.row`s (the flat form)? Per template / subject / series: pages wrapper / flat / other;
Claude the same. python3 _s26_r393_outerrow.py"""
import os, sys, re
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
sys.path.insert(0, OUTPUTS)
src = open(os.path.join(OUTPUTS, "_s26_r392_adjul.py"), encoding="utf-8").read()
exec(src[:src.index("ADJ = re.compile")])
from collections import Counter, defaultdict
TAG = re.compile(r"<(/?)([a-z][a-z0-9]*)\b([^>]*)>", re.I)
CLS = re.compile(r'class="([^"]*)"'); ID = re.compile(r'id="([^"]*)"')
VOID = {"br", "img", "input", "hr", "meta", "link", "source", "wbr"}
def body_children(s):
    """labels of div#body's direct element children, and for each direct div.row child, its own direct children labels."""
    st = []; kids = []; sub = {}
    for m in TAG.finditer(s):
        closing, tag, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID and not closing: continue
        if closing:
            if st: st.pop()
            continue
        c = CLS.search(attrs); cls = c.group(1).strip() if c else ""; i = ID.search(attrs)
        label = tag + ("#" + i.group(1) if i else "") + (("." + ".".join(cls.split())) if cls else "")
        if len(st) == 1 and st[0] == "div#body":
            kids.append(label); sub[len(kids) - 1] = []
        elif len(st) == 2 and st[0] == "div#body" and st[1] == "div.row":
            sub[len(kids) - 1].append(label)
        st.append(label)
    return kids, sub
def form(s):
    kids, sub = body_children(s)
    rows = [k for k in kids if k == "div.row"]
    if not rows: return "no-row"
    if len(rows) == 1 and kids[0] == "div.row":
        inner = sub.get(0, [])
        if inner and all(x == "div.row" or x.startswith("div.row.") or x.startswith("div.activity") for x in inner) and sum(1 for x in inner if x.startswith("div.row")) >= 2:
            return "WRAPPER (one outer row of rows)"
        if len(inner) >= 1 and inner[0].startswith("div.col"): return "flat (single row of cols)"
        return "single-row other"
    if kids and kids[0] == "div.row" and any(x == "div.row" for x in sub.get(0, [])): return "MIXED (first row holds rows, more rows follow)"
    return "flat (rows of cols)"
G = defaultdict(Counter); C = defaultdict(Counter); EX = {}
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"; ser = re.sub(r"\d+$", "", code)[:6]
    for n, cp, hp in pairs(code):
        try:
            ch = body(open(cp, encoding="utf-8", errors="replace").read()); gh = body(open(hp, encoding="utf-8", errors="replace").read())
        except Exception: continue
        gf = form(gh); cf = form(ch)
        for k in ("ALL", f"template={tf}", f"tmpl+subj={tf}/{subj}", f"series={ser}"):
            G[k][gf] += 1; C[k][cf] += 1
        if gf not in EX: EX[gf] = os.path.basename(hp)
FORMS = ["WRAPPER (one outer row of rows)", "MIXED (first row holds rows, more rows follow)", "flat (rows of cols)", "flat (single row of cols)", "single-row other", "no-row"]
print("==== the gold's outer body form per group (pages) — Claude in brackets ====")
print("   group" + " " * 42 + "  ".join(f[:8] for f in FORMS))
for k in sorted(G, key=lambda x: (not x.startswith("ALL"), not x.startswith("template"), x.startswith("series"), -sum(G[x].values()))):
    t = sum(G[k].values())
    if t < 20: continue
    w = G[k][FORMS[0]] + G[k][FORMS[1]]
    print(f"   {k:44s} " + "  ".join(f"{G[k][f]:4d}[{C[k][f]:4d}]" for f in FORMS) + f"   wrapper-ish {w/t:.2f}")
print("   examples:", EX)
