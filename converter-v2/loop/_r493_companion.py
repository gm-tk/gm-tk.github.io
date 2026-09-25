#!/usr/bin/env python3
"""ROUND 493: OLD = the toggles-OFF render (outputs/_r493_off), NEW = the disk — the companion numbers for the dipping pages (LOOP §3 step 6): the position-free overlap (multiset of skeleton line
roles, depth ignored, gold ∩ Claude) and the count of quote-form lines, OLD (disk) vs NEW (outputs/_r493_off). WSL, from outputs/:
python3 _r486_companion.py MODULE:page.html ..."""
import sys, os, io, json, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "tests"))
import _diff_miner as dm
import _corpus
OUT = os.path.dirname(os.path.abspath(__file__))
pp = json.load(io.open(os.path.join(OUT, "_diff_miner.json"), encoding="utf-8"))["per_page"]
def roles(lines): return collections.Counter(str(getattr(l, "role", l)) for l in lines)
for arg in sys.argv[1:]:
    code, page = arg.split(":")
    rec = next((p for p in pp if p["module"] == code and p["page"] == page), None)
    if not rec: print(arg, "not paired"); continue
    g, _ = dm.page_lines(os.path.join(_corpus.mdir(dm.HUMAN, code), rec["gold"]))
    o, _ = dm.page_lines(os.path.join(_corpus.mdir(dm.CLAUDE, code), page))
    n, _ = dm.page_lines(os.path.join(OUT, "_r493_off", code, page))
    G = roles(g); O = roles(o); N = roles(n)
    ov = lambda C: sum((G & C).values())
    q = lambda C: {k: v for k, v in C.items() if "carousel" in k or "WIDGET" in k}
    print(f"{code}/{page}: gold {len(g)} lines | position-free overlap OLD(r492) {ov(N)} / {len(n)}  NEW(r493) {ov(O)} / {len(o)}  "
          f"(Δ {ov(O) - ov(N):+d}) | widget lines gold {q(G)} OLD {q(N)} NEW {q(O)}")
