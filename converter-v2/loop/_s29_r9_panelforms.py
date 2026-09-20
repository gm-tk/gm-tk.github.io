#!/usr/bin/env python3
"""_s29_r9_panelforms.py — the XDLS tile-grid family per PAGE: the gold's panel forms (row.clickDropContent.noBorder > col > activity.dropbox
vs clickDropContent activity dropbox direct), which panel index takes the row form, the upload-button count and its panel index, vs Claude
(panels all direct after r417; one upload button per [dropbox] marker). Run under WSL from CONVERTER_V2/reference/tests:
python3 ../../outputs/_s29_r9_panelforms.py
"""
import os, re, sys, glob
sys.path.insert(0, ".")
import _discrepancy_audit as da
HERE = os.path.dirname(os.path.abspath(__file__))

def panels(html):
    """ordered list of (form, number, has_upload) for every tile-grid panel on the page"""
    out = []
    for m in re.finditer(r'<div class="(row clickDropContent[^"]*|clickDropContent activity[^"]*)"[^>]*>', html):
        form = "row" if m.group(1).startswith("row") else "direct"
        # span to the panel's balanced close
        depth = 0; i = m.start(); end = len(html)
        for mm in re.finditer(r"<(/?)div\b", html[m.start():]):
            depth += -1 if mm.group(1) else 1
            if depth == 0: end = m.start() + mm.end(); break
        seg = html[m.start():end]
        num = re.search(r'number="([^"]*)"', seg)
        up = len(re.findall(r'type=dropbox|Upload to [Dd]ropbox', seg))
        out.append((form, num.group(1) if num else "-", up))
    return out

tot = {"pages": 0, "gold_row_first": 0, "gold_row_other": 0, "gold_up1": 0, "gold_up_last": 0, "claude_up": 0, "gold_up": 0, "claude_panels": 0, "gold_panels": 0}
for code in ["XDLS902", "XDLS903", "XDLS904", "XDLS905", "XDLS906", "XDLS909"]:
    for n, cp, hp in da.pairs(code):
        g = open(hp, encoding="utf-8", errors="replace").read(); c = open(cp, encoding="utf-8", errors="replace").read()
        gp, cpn = panels(g), panels(c)
        if not gp and not cpn: continue
        tot["pages"] += 1; tot["gold_panels"] += len(gp); tot["claude_panels"] += len(cpn)
        gforms = "".join("R" if f == "row" else "d" for f, _, _ in gp)
        cforms = "".join("R" if f == "row" else "d" for f, _, _ in cpn)
        gup = [i for i, (_, _, u) in enumerate(gp) if u]; cup = [i for i, (_, _, u) in enumerate(cpn) if u]
        gpage_up = len(re.findall(r'type=dropbox', g)); cpage_up = len(re.findall(r'>Upload to dropbox<', c))
        tot["gold_up"] += gpage_up; tot["claude_up"] += cpage_up
        if gp and gp[0][0] == "row": tot["gold_row_first"] += 1
        tot["gold_row_other"] += sum(1 for f, _, _ in gp[1:] if f == "row")
        if gpage_up == 1: tot["gold_up1"] += 1
        if gp and gup and gup[-1] == len(gp) - 1: tot["gold_up_last"] += 1
        print(f"{code} {os.path.basename(cp):22s} gold {gforms:8s} up@{gup} (page {gpage_up})  |  claude {cforms:8s} up@{cup} (page {cpage_up})  nums {[x[1] for x in gp]}")
print(tot)
