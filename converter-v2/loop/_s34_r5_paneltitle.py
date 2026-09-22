#!/usr/bin/env python3
"""Session 34 Round 5 PICK measurement — THE INQUIRY PANEL'S FIRST-HEADING LEVEL BY FAMILY (the r429 follow-up): for every gold page
carrying div.inquiryPanel, the tag level of each panel's FIRST heading (h1–h6; the panel's own title), counted by family prefix
(the code's letters + the hundreds digit where the family splits — BLL1 / BLL2 / CEDK / CEDO / CEDR / CEDT / CEDW / TWHA / TWHK / TWHR / TWHT
/ EXP …), and the same on the paired Claude page (the r385 post-pass promotes every panel's first own heading to h2).
Run under WSL: python3 _s34_r5_paneltitle.py
"""
import os, re, glob, collections, sys
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
sys.path.insert(0, R + "CONVERTER_V2/reference/tests")
import _corpus
from _discrepancy_audit import pairs as _pairs
def fam(code):
    m = re.match(r'^([A-Z]+)(\d)?', code)
    letters = m.group(1); d = m.group(2) or ""
    if letters == "BLL": return "BLL" + d
    return letters
def panels_of(html):
    out = []
    for m in re.finditer(r'<div class="inquiryPanel[^"]*"[^>]*>', html):
        i = m.end(); depth = 1; j = i
        while depth and j < len(html):
            no = html.find("<div", j); nc = html.find("</div>", j)
            if nc < 0: break
            if no >= 0 and no < nc: depth += 1; j = no + 4
            else: depth -= 1; j = nc + 6
        out.append(html[m.end():j])
    return out
def first_heading_level(panel_html):
    m = re.search(r'<(h[1-6])\b', panel_html)
    return m.group(1) if m else "none"
gold = collections.defaultdict(collections.Counter); claude = collections.defaultdict(collections.Counter)
pages_by_fam = collections.defaultdict(set)
for code in _corpus.gate_mods(R + "01-Claude_Modules_"):
    try: pl = list(_pairs(code))
    except Exception: continue
    for n, cp, hp in pl:
        if re.search(r"acks|acknowledge|glossary", os.path.basename(cp), re.I): continue
        gh = open(hp, encoding="utf-8", errors="replace").read()
        if "inquiryPanel" not in gh: continue
        ch = open(cp, encoding="utf-8", errors="replace").read()
        f = fam(code)
        gp = panels_of(gh); cpn = panels_of(ch)
        if not gp: continue
        pages_by_fam[f].add(code)
        for p in gp: gold[f][first_heading_level(p)] += 1
        for p in cpn: claude[f][first_heading_level(p)] += 1
print("family   modules  GOLD panels' first heading                 CLAUDE panels' first heading")
tot_gold = collections.Counter()
for f in sorted(pages_by_fam):
    g = gold[f]; c = claude[f]; tot_gold.update(g)
    print(f"{f:8s} {len(pages_by_fam[f]):3d}     {dict(g.most_common())!s:44s} {dict(c.most_common())}")
print("ALL gold:", dict(tot_gold.most_common()))
# the class: panels whose gold first heading is h3 while Claude's (same page, same panel index) is h2
mism = collections.Counter(); pages = set()
for code in _corpus.gate_mods(R + "01-Claude_Modules_"):
    try: pl = list(_pairs(code))
    except Exception: continue
    for n, cp, hp in pl:
        if re.search(r"acks|acknowledge|glossary", os.path.basename(cp), re.I): continue
        gh = open(hp, encoding="utf-8", errors="replace").read()
        if "inquiryPanel" not in gh: continue
        ch = open(cp, encoding="utf-8", errors="replace").read()
        gp = panels_of(gh); cpn = panels_of(ch)
        for i in range(min(len(gp), len(cpn))):
            gl, cl = first_heading_level(gp[i]), first_heading_level(cpn[i])
            if gl != cl and gl != "none" and cl != "none":
                mism[(fam(code), gl, cl)] += 1; pages.add((code, os.path.basename(cp)))
print("\npanel first-heading level mismatches (family, gold, Claude) by panel:", dict(mism.most_common()), "\npages with a mismatch:", len(pages))
