#!/usr/bin/env python3
"""session 28 task 3 — per WJFUN module: the ON page's panel / tile / menu shape vs the gold's, and the
h2 heading sets on both sides (tile titles are h2 in every WJFUN gold)."""
import os, re, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
ON = os.path.join(HERE, "_s28_t3_on")
codes = [l.strip() for l in open(os.path.join(HERE, "_s28_t3_ON_modules.txt")) if l.strip()]
H = re.compile(r"<h([1-6])[^>]*>(.*?)</h\1>", re.S)
def fold(t): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip().lower()
def shape(html):
    return dict(panels=len(re.findall(r'class="fundamentalsPanel"', html)),
                intro=len(re.findall(r'class="introduction fundamentalsPanel"', html)),
                phases=len(re.findall(r'<div class="phases"', html)),
                tiles=len(re.findall(r'class="phaseLink"', html)),
                panes=len(re.findall(r'class="tab-pane"', html)),
                h2=[fold(m.group(2)) for m in H.finditer(html) if m.group(1) == "2"],
                phaseN=len(re.findall(r"<h[1-6][^>]*>\s*Phase \d+\s*</h[1-6]>", html)))
tot = dict(pan_eq=0, tile_eq=0, pane_eq=0, h2_all=0, n=0)
for code in codes:
    onp = os.path.join(ON, code, f"{code}_0_0.html")
    gp = glob.glob(os.path.join(ROOT, "01-Finalized_Modules_", "*", code, f"{code}_0_0.html"))
    if not os.path.exists(onp) or not gp: print(code, "MISSING"); continue
    o = shape(open(onp, encoding="utf-8", errors="replace").read()); g = shape(open(gp[0], encoding="utf-8", errors="replace").read())
    gh2 = set(g["h2"]); oh2 = set(o["h2"])
    tile_h2_ok = all(h in gh2 for h in oh2)
    tot["n"] += 1; tot["pan_eq"] += o["panels"] == g["panels"]; tot["tile_eq"] += o["tiles"] == g["tiles"]; tot["pane_eq"] += o["panes"] == g["panes"]; tot["h2_all"] += tile_h2_ok
    print(f"{code}: panels {o['panels']}/{g['panels']} tiles {o['tiles']}/{g['tiles']} panes {o['panes']}/{g['panes']} phaseN-heads {o['phaseN']}/{g['phaseN']} "
          f"h2 {len(oh2)}/{len(gh2)} {'all-in-gold' if tile_h2_ok else 'EXTRA:' + ';'.join(sorted(oh2 - gh2))[:80]}")
print(f"\n{tot['n']} modules: panels == gold {tot['pan_eq']}, tiles == gold {tot['tile_eq']}, panes == gold {tot['pane_eq']}, every Claude h2 in gold {tot['h2_all']}")
