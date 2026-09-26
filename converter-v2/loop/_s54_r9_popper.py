#!/usr/bin/env python3
"""_s54_r9_popper.py — the gold's wrapper around the BLL closing party-popper (iStock 1461683255): the chain of div classes from the
column holding it up to its row, and its sibling column, per series (BLL1 / BLL2 / BLLR). WSL, any cwd."""
import glob, re, collections, os
ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/01-Finalized_Modules_"
c = collections.defaultdict(collections.Counter)
for f in glob.glob(ROOT + "/*/*/*.html"):
    s = open(f, encoding="utf-8", errors="replace").read()
    i = s.find("1461683255")
    if i < 0: continue
    code = os.path.basename(os.path.dirname(f)); ser = re.sub(r"(\D+\d).*", r"\1", code)
    before = s[max(0, i - 900):i]; after = s[i:i + 700]
    opens = re.findall(r'<div class="([^"]*)"', before)[-3:]
    sib = re.findall(r'<div class="([^"]*)"', after)[:1]
    key = " > ".join(x.strip() for x in opens) + "  || next: " + (sib[0].strip() if sib else "-")
    c[ser][key] += 1
for ser, cc in sorted(c.items()):
    n = sum(cc.values())
    print(f"== {ser}: {n} pages")
    for k, v in cc.most_common(5): print(f"   {v:3d} ({v / n:.2f})  {k}")
