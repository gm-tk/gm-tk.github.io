#!/usr/bin/env python3
"""Session 26 — print the module-menu region of the gold and Claude skeletons side by side for named pages.
  python3 _s26_menu_peek.py AGH1003_1_0 AGH1001_2_0 ..."""
import os, sys, re
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS)
from _diff_miner import page_lines
from _discrepancy_audit import pairs

REGIONS = set((os.environ.get("REG") or "module-menu").split(","))
want = sys.argv[1:]
codes = sorted({re.match(r"([A-Z]+[0-9]+[A-Z]*)", w).group(1) for w in want})
for code in codes:
    for n, cp, hp in pairs(code):
        base = os.path.basename(cp).replace(".html", "")
        if base not in want: continue
        g, _ = page_lines(hp); c, _ = page_lines(cp)
        print(f"\n===== {base}   gold={os.path.relpath(hp, '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA')}")
        print("--- GOLD module-menu ---")
        for ln in g:
            if ln.region in REGIONS:
                print(f"  {ln.pad}{ln.sig}  |{(ln.text or '')[:70]}")
        print("--- CLAUDE module-menu ---")
        for ln in c:
            if ln.region in REGIONS:
                print(f"  {ln.pad}{ln.sig}  |{(ln.text or '')[:70]}")
