#!/usr/bin/env python3
"""Session 44 — dump the miner's skeleton lines for ONE paired page, gold and Claude, side by side (depth-indented role + text).
usage (WSL, from outputs/): python3 _s44_skdump.py <MODULE> <claude_page.html> [maxlines]"""
import sys, os, io, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "tests"))
import _diff_miner as dm
import _corpus
code, page = sys.argv[1], sys.argv[2]
mx = int(sys.argv[3]) if len(sys.argv) > 3 else 400
OUT = os.path.dirname(os.path.abspath(__file__))
pp = json.load(io.open(os.path.join(OUT, "_diff_miner.json"), encoding="utf-8"))["per_page"]
rec = next((p for p in pp if p["module"] == code and p["page"] == page), None)
if not rec: sys.exit("not paired")
g, _ = dm.page_lines(os.path.join(_corpus.mdir(dm.HUMAN, code), rec["gold"]))
c, _ = dm.page_lines(os.path.join(_corpus.mdir(dm.CLAUDE, code), page))
def fmt(l):
    d = getattr(l, "depth", 0) or 0
    return ("  " * min(d, 12) + str(getattr(l, "role", l)) + " «" + str(getattr(l, "text", ""))[:50] + "»")
print("gold", rec["gold"], len(g), "| claude", page, len(c))
for i in range(min(mx, max(len(g), len(c)))):
    a = fmt(g[i]) if i < len(g) else ""
    b = fmt(c[i]) if i < len(c) else ""
    print(f"{i:3d} {a[:95]:95} | {b[:95]}")
