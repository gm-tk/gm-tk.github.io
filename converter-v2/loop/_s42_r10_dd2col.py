#!/usr/bin/env python3
"""Session 42 Round 10 PICK — the two-column dragAndDrop tables the column builder refuses (`width < min_columns 3`). For every declined
dragAndDrop bundle whose shape is `table Nx2` and whose reason is the width fence (the r286 records on the r470 corpus), find the paired
gold page and census the gold's dragAndDrop widgets there: the layout attribute, the drop-container's ddColumn count, the drags' count.
Run under WSL from CONVERTER_V2/reference/tests: python3 ../../outputs/_s42_r10_dd2col.py > ../../outputs/_s42_r10_dd2col.log"""
import os, re, sys, json, collections
sys.path.insert(0, os.getcwd())
import _corpus, _discrepancy_audit as DA
from anchor_compare import CLAUDE, HUMAN
O = os.path.join("..", "..", "outputs")
d = json.load(open(os.path.join(O, "_r286_declines.json")))
R = d if isinstance(d, list) else (d.get("records") or next(v for v in d.values() if isinstance(v, list)))
gm = set(_corpus.gate_mods(CLAUDE))
B = [r for r in R if r["type"] == "dragAndDrop" and not r["built"] and "min_columns" in (r.get("decideWhy") or "")
     and re.match(r"table \d+x2$", r.get("shape") or "") and r["code"] in gm]
print(f"two-column D&D bundles (width fence, gate modules): {len(B)} / pages {len(set((r['code'], r['page']) for r in B))} / modules {len(set(r['code'] for r in B))}")
pair = {}
for code in sorted(set(r["code"] for r in B)):
    for _, cp, hp in DA.pairs(code):
        m = re.match(r".*_(\d+)_(\d+)\.html$", os.path.basename(cp))
        if m: pair[(code, f"{int(m.group(1))}.{int(m.group(2))}")] = hp
forms = collections.Counter(); per_page = collections.Counter(); ex = collections.defaultdict(list); nopair = 0
for (code, page) in sorted(set((r["code"], r["page"]) for r in B)):
    hp = pair.get((code, page))
    if not hp: nopair += 1; continue
    s = open(hp, encoding="utf-8", errors="replace").read()
    dds = [m.start() for m in re.finditer(r'<div class="dragAndDrop[^"]*"', s)]
    if not dds: forms["(no dragAndDrop on the gold page)"] += 1; ex["(no dragAndDrop on the gold page)"].append(f"{code} {page}"); continue
    for st in dds:
        head = s[st:st + 300]; lay = re.search(r'layout="([^"]+)"', head); lay = lay.group(1) if lay else "standard"
        seg = s[st:st + 20000]
        dc = re.search(r'<div class="row dropContainer">(.*?)<div class="row dragContainer">', seg, re.S)
        ncol = len(re.findall(r'<div class="ddColumn"', dc.group(1))) if dc else 0
        ndrop = len(re.findall(r'<div class="drop"', seg[:8000])); ndrag = len(re.findall(r'<div class="drag"', seg[:8000]))
        key = f"layout={lay} dropCols={ncol}"
        forms[key] += 1
        if len(ex[key]) < 6: ex[key].append(f"{code} {page} (drops {ndrop}, drags {ndrag})")
print(f"no pair for {nopair} bundle pages")
for k, n in forms.most_common(): print(f"{n:4d}  {k}   e.g. {'; '.join(ex[k][:4])}")
