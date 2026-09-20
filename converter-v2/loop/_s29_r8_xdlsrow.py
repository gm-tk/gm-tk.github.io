#!/usr/bin/env python3
"""_s29_r8_xdlsrow.py — the Leaving to Learn (XDLS / XLP / XTAS) activity box WITHOUT the inner row > col: per module and per box class,
the gold's share of boxes whose content sits directly in the box (no `div.row` first child) vs wrapped; Claude's shape; pages.
Run under WSL from CONVERTER_V2/reference/tests: python3 ../../outputs/_s29_r8_xdlsrow.py [PREFIX ...]"""
import os, re, sys, json, collections
sys.path.insert(0, ".")
import _discrepancy_audit as da, _corpus
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CLAUDE = os.path.join(ROOT, "01-Claude_Modules_")
sys.path.insert(0, HERE)
from _s29_r8_boxcol import boxes
prefs = sys.argv[1:] or ["XDLS", "XLP", "XTAS", "XMES", "XGF", "XWHA", "XFUN"]
def shape(inner):
    s = re.sub(r"<!--[\s\S]*?-->", "", inner).lstrip()
    m = re.match(r'<div class="([^"]*)"', s)
    if not m: return "direct"
    c = m.group(1)
    if re.search(r"(^|\s)row(\s|$)", c): return "row>col"
    if "super-content" in c: return "super-content"
    return "div:" + c.split()[0]
per = collections.defaultdict(lambda: collections.defaultdict(collections.Counter)); pages = collections.defaultdict(set)
for code in _corpus.gate_mods(CLAUDE):
    if not any(code.startswith(p) for p in prefs): continue
    try: prs = da.pairs(code)
    except Exception: continue
    for t in prs:
        cp, hp = t[1], t[2]
        try: c = open(cp, encoding="utf-8").read(); gh = open(hp, encoding="utf-8", errors="replace").read()
        except Exception: continue
        for n, cl, inner in boxes(gh):
            k = "panel" if "clickDropContent" in cl else ("interactive" if "interactive" in cl.split() else "plain")
            per[code]["gold " + k][shape(inner)] += 1
        for n, cl, inner in boxes(c):
            k = "panel" if "clickDropContent" in cl else ("interactive" if "interactive" in cl.split() else "plain")
            per[code]["claude " + k][shape(inner)] += 1; pages[code].add(cp)
tot = collections.defaultdict(collections.Counter)
for code in sorted(per):
    print(code, "pages", len(pages[code]))
    for k in sorted(per[code]):
        print("   %-19s %s" % (k, dict(per[code][k].most_common())))
        tot[k].update(per[code][k])
print("\nTOTAL:")
for k in sorted(tot): print("   %-19s %s" % (k, dict(tot[k].most_common())))
