#!/usr/bin/env python3
"""Session 42 Round 4 PICK — the overview menu's NAV TAB SET, gold vs Claude, per module (gate population, the paired overview
page = the pair whose Claude page is *_0_0.html). Prints the canonical tab sequence both sides and a census of (gold set, Claude
set) combinations, with the modules; then, for the modules where the gold has a Standards / Assessment tab and Claude does not,
the first two headings of the gold's Standards pane and where that text sits in Claude's menu.
Run under WSL from CONVERTER_V2/reference/tests: python3 ../../outputs/_s42_r4_navtabs.py > ../../outputs/_s42_r4_navtabs.log"""
import os, re, sys, collections, html as H
sys.path.insert(0, os.getcwd())
import _corpus, _discrepancy_audit as DA
from anchor_compare import CLAUDE, HUMAN
sys.path.insert(0, os.path.join("..", "..", "outputs"))
from _placement_census import canon_pane, norm

def nav(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r'id="module-menu-content"(.*?)<div id="body"', s, re.S)
    if not m: return None, [], ""
    blk = m.group(1)
    ul = re.search(r'<ul class="nav nav-tabs[^"]*"[^>]*>(.*?)</ul>', blk, re.S)
    labs = [H.unescape(re.sub(r"<[^>]+>", "", t)).strip() for t in re.findall(r"<li[^>]*>(.*?)</li>", ul.group(1), re.S)] if ul else []
    panes = re.split(r'<div class="tab-pane[^"]*"[^>]*>', blk)[1:]
    return [canon_pane(l, i) for i, l in enumerate(labs)], panes, blk

combo = collections.Counter(); ex = collections.defaultdict(list); std_rows = []
for code in sorted(_corpus.gate_mods(CLAUDE)):
    for _, cp, hp in DA.pairs(code):
        if not os.path.basename(cp).endswith("_0_0.html"): continue
        g, gp, gb = nav(hp); c, cpn, cb = nav(cp)
        if g is None and c is None: continue
        key = (" > ".join(g or ["(no menu)"]) or "(flat)", " > ".join(c or ["(no menu)"]) or "(flat)")
        combo[key] += 1; ex[key].append(code)
        if g and "Standards" in g and "Standards" not in (c or []):
            i = g.index("Standards"); pane = gp[i] if i < len(gp) else ""
            hs = [H.unescape(re.sub(r"<[^>]+>", "", x)).strip() for x in re.findall(r"<(?:h[1-6]|p)[^>]*>(.*?)</(?:h[1-6]|p)>", pane, re.S)][:3]
            where = []
            for h in hs[:2]:
                t = norm(h)[:30]
                j = next((k for k, p in enumerate(cpn) if t and t in norm(p)), None)
                where.append((c[j] if (c and j is not None and j < len(c)) else ("body/none" if t not in norm(cb) else "menu-flat")))
            std_rows.append((code, " > ".join(g), " > ".join(c or []), hs, where))
for (g, c), n in combo.most_common(): print(f"{n:4d}  gold [{g}]  claude [{c}]  :: {' '.join(ex[(g, c)])[:220]}")
print(f"\n== gold has a Standards tab, Claude does not: {len(std_rows)} modules")
for code, g, c, hs, where in std_rows: print(f"{code:9s} gold [{g}] claude [{c}] | {' / '.join(h[:50] for h in hs)} | claude: {where}")
