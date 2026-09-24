#!/usr/bin/env python3
"""Session 44 — the miner's per-line diff classes aggregated over ONE family's pages (a scoped miner view, lines + pages + modules).
usage (WSL, from outputs/): python3 _s44_famdiff.py <regex on module code> [--pages <regex on page>] [--top N] [--full]"""
import sys, os, io, json, re, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "tests"))
import _diff_miner as dm
import _corpus
mre = re.compile(sys.argv[1])
pre = re.compile(sys.argv[sys.argv.index("--pages") + 1]) if "--pages" in sys.argv else None
top = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else 60
full = "--full" in sys.argv
OUT = os.path.dirname(os.path.abspath(__file__))
pp = json.load(io.open(os.path.join(OUT, "_diff_miner.json"), encoding="utf-8"))["per_page"]
lines = collections.Counter(); pages = collections.defaultdict(set); mods = collections.defaultdict(set); ex = {}
n = 0
for rec in pp:
    code, page = rec["module"], rec["page"]
    if not mre.search(code) or (pre and not pre.search(page)): continue
    g, _ = dm.page_lines(os.path.join(_corpus.mdir(dm.HUMAN, code), rec["gold"]))
    c, _ = dm.page_lines(os.path.join(_corpus.mdir(dm.CLAUDE, code), page))
    n += 1
    for d, gl, cl, carried in dm.diff_lines(g, c):
        if carried and not full: continue
        reg = (gl or cl).region
        k = (reg, d, gl.role if gl else "—", cl.role if cl else "—")
        lines[k] += 1; pages[k].add(page); mods[k].add(code)
        if k not in ex: ex[k] = (page, (gl.text if gl else "")[:40], (cl.text if cl else "")[:40])
print(f"pages {n}")
for k, v in lines.most_common(top):
    print(f"{v:5d} {len(pages[k]):4d}p {len(mods[k]):3d}m  {k[0]:9} {k[1]:11} {k[2][:38]:38} -> {k[3][:38]:38}  e.g. {ex[k][0]} «{ex[k][1]}» «{ex[k][2]}»")
