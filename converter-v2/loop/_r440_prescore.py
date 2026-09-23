#!/usr/bin/env python3
"""ROUND 440 (session 39 Round 2 — D13-6) — the pre-score, with the gate's own match().
MXFUN01 / BLL240 / CEDT207 / CEDT301: the ON single page (outputs/_r440_on/<code>/) against the single-file gold.
CEDK501: pairs() on the disk under the new gold selection (its unfilled template excluded) vs GOLDPAGES_OFF.
Then the population arithmetic: the r439 skeleton state with the five modules' old rows replaced by the new ones.
Run from CONVERTER_V2/reference/tests under WSL: python3 ../../outputs/_r440_prescore.py
"""
import os, sys, json
sys.path.insert(0, os.getcwd())
import _corpus
import _discrepancy_audit as DA
from _skeleton_compare import match

O = os.path.join("..", "..", "outputs")
HUMAN = DA.HUMAN
SINGLE = {"MXFUN01": "MXFUN01.html", "BLL240": "BLL240.html",
          "CEDT207": "CEDT207 Me, my selfie and I.html", "CEDT301": "CEDT301 My place and me.html"}
new_rows = []
for code, gold in SINGLE.items():
    hp = os.path.join(_corpus.mdir(HUMAN, code), gold)
    ond = os.path.join(O, "_r440_on", code)
    pages = sorted(f for f in os.listdir(ond) if f.endswith(".html"))
    assert os.path.exists(hp), hp
    for f in pages:
        s, r = match(os.path.join(ond, f), hp, scaffold=True)[0], match(os.path.join(ond, f), hp)[0]
        new_rows.append((code, f, gold, s, r))
        print(f"{code:8s} ON {f:20s} <-> {gold:36s} scaffold {100*s:5.1f}  raw {100*r:5.1f}")
    print(f"         gold_pages() keeps: {_corpus.gold_pages(code, sorted(x for x in os.listdir(_corpus.mdir(HUMAN, code)) if x.endswith('.html')))}")

print("-" * 100)
for label, env in (("NEW (compare_gold_pages.txt)", None), ("OLD (GOLDPAGES_OFF=1)", "1")):
    if env: os.environ["GOLDPAGES_OFF"] = env
    else: os.environ.pop("GOLDPAGES_OFF", None)
    pr = DA.pairs("CEDK501")
    sc = []
    print(f"CEDK501 {label}: {len(pr)} pairs")
    for n, cp, hp in pr:
        s = match(cp, hp, scaffold=True)[0]; sc.append(s)
        if not env:
            new_rows.append(("CEDK501", os.path.basename(cp), os.path.basename(hp), s, match(cp, hp)[0]))
        print(f"   {os.path.basename(cp):20s} <-> {os.path.basename(hp):45s} {100*s:5.1f}")
    print(f"   mean {100*sum(sc)/len(sc):.2f}")
os.environ.pop("GOLDPAGES_OFF", None)

st = json.load(open(os.path.join(O, "_r439_sk_final.json")))
FIVE = set(SINGLE) | {"CEDK501"}
keep = [p for p in st["per_page"] if p["module"] not in FIVE]
old5 = [p for p in st["per_page"] if p["module"] in FIVE]
tot_old = sum(p["scaffold"] for p in st["per_page"])
n_old = len(st["per_page"])
tot_new = sum(p["scaffold"] for p in keep) + sum(r[3] for r in new_rows)
n_new = len(keep) + len(new_rows)
print("-" * 100)
print(f"the five, OLD: {len(old5)} pairs, mean {100*sum(p['scaffold'] for p in old5)/len(old5):.2f}")
print(f"the five, NEW: {len(new_rows)} pairs, mean {100*sum(r[3] for r in new_rows)/len(new_rows):.2f}")
print(f"corpus SCAFFOLD: {100*tot_old/n_old:.4f} % @ {n_old}  ->  {100*tot_new/n_new:.4f} % @ {n_new}   ({100*(tot_new/n_new - tot_old/n_old):+.4f}pp)")
b = lambda rows, t: sum(1 for x in rows if x >= t)
olds = [p["scaffold"] for p in st["per_page"]]
news = [p["scaffold"] for p in keep] + [r[3] for r in new_rows]
for t in (0.5, 0.75, 0.9):
    print(f"   >= {int(t*100)}: {b(olds, t)} -> {b(news, t)}")
