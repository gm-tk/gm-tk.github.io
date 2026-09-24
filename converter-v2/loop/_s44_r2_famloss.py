#!/usr/bin/env python3
"""Session 44 Round 2 — the loss ledger by FAMILY PREFIX on the current skeleton state: per family, pages, mean SCAFFOLD, and the
pp the family costs the corpus mean (sum over its pages of (100 - score) / N). WSL, from outputs/: python3 _s44_r2_famloss.py [json]"""
import json, re, sys, collections
p = sys.argv[1] if len(sys.argv) > 1 else "_r478_sk_final.json"
d = json.load(open(p)); pp = d["per_page"]
if isinstance(pp, dict): items = list(pp.items())
else: items = [(r.get("page") or r.get("name"), r) for r in pp]
N = len(items)
fam = collections.defaultdict(list)
sample = items[0]
for k, v in items:
    sc = v if isinstance(v, (int, float)) else (v.get("scaffold") if isinstance(v, dict) else None)
    if sc is None and isinstance(v, dict):
        for kk in ("scaffold_pct", "score", "ratio"):
            if kk in v: sc = v[kk]; break
    code = re.split(r"[/_ ]", str(k))[0]
    m = re.match(r"([A-Z]+)(\d?)", code)
    f = (m.group(1) + (m.group(2) or "")) if m else code
    fam[f].append((str(k), 100.0 * float(sc)))
print("sample:", str(sample)[:200], "N", N)
rows = []
for f, L in fam.items():
    mean = sum(s for _, s in L) / len(L)
    rows.append((sum(100 - s for _, s in L) / N, f, len(L), mean))
rows.sort(reverse=True)
print(f"{'family':8} {'pages':>5} {'mean':>6} {'loss pp':>8}")
for loss, f, n, mean in rows[:40]:
    print(f"{f:8} {n:5d} {mean:6.1f} {loss:8.3f}")
if len(sys.argv) > 2:
    for f in sys.argv[2:]:
        print("==", f); [print(f"  {k} {s:.1f}") for k, s in sorted(fam.get(f, []), key=lambda x: x[1])]
