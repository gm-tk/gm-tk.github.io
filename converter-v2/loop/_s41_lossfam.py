#!/usr/bin/env python3
"""Session 41 PICK pass — the loss ledger by family on the r452 skeleton state.
Loss = (100 - scaffold) summed over a family's pages; share of the corpus loss. Family = the module code's
alpha prefix + first digit (the Style_Anchor_Registry level key), and the template folder. Run under WSL."""
import json, os, re, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else "_r452_sk_final.json")))
pp = d["per_page"]
print("per_page type", type(pp).__name__, "n", len(pp))
first = pp[0] if isinstance(pp, list) else next(iter(pp.items()))
print("sample", str(first)[:300])
rows = []
if isinstance(pp, list):
    for r in pp:
        rows.append((r.get("module") or r.get("code"), r.get("page") or r.get("file"), r.get("scaffold")))
else:
    for k, v in pp.items():
        sc = v.get("scaffold") if isinstance(v, dict) else v
        mod = v.get("module") if isinstance(v, dict) else None
        rows.append((mod, k, sc))
def fam(code, page):
    c = code or re.split(r"[_ ]", os.path.basename(page))[0]
    m = re.match(r"([A-Z]+)(\d)?", c)
    return (m.group(1) + (m.group(2) or "")) if m else c
agg = collections.defaultdict(lambda: [0, 0.0, set()])
tot = 0.0
for mod, page, sc in rows:
    if sc is None: continue
    sc = float(sc); sc = sc * 100 if sc <= 1.0 else sc
    f = fam(mod, page)
    agg[f][0] += 1; agg[f][1] += 100 - sc; agg[f][2].add(mod or page.split("_")[0])
    tot += 100 - sc
print("total loss pp-sum", round(tot, 1), "pages", len(rows))
out = sorted(agg.items(), key=lambda kv: -kv[1][1])
print(f"{'family':10} {'pages':>5} {'mods':>4} {'mean':>6} {'loss':>8} {'share':>6}")
for f, (n, loss, mods) in out[:45]:
    print(f"{f:10} {n:5d} {len(mods):4d} {100 - loss / n:6.1f} {loss:8.1f} {loss / tot * 100:5.1f}%")
