#!/usr/bin/env python3
"""r431 — which paired pages appeared / disappeared between the r430 and r431 skeleton states, and how each is paired."""
import json, os
O = os.path.dirname(os.path.abspath(__file__))
a = json.load(open(O + "/_s35_r430_sk_final.json", encoding="utf-8"))
b = json.load(open(O + "/_s35_r431_sk_final.json", encoding="utf-8"))
def pages(j):
    rows = j.get("pages") or j.get("pairs") or j.get("rows") or (j if isinstance(j, list) else [])
    out = {}
    for r in rows:
        if not isinstance(r, dict): continue
        k = r.get("claude") or r.get("claude_page") or r.get("page") or r.get("c")
        out[str(k)] = r
    return out
A, B = pages(a), pages(b)
print("keys sample:", list(A.keys())[:2], "fields:", list(next(iter(A.values())).keys())[:12] if A else None)
for k in sorted(set(B) - set(A)): print("NEW ", k, {x: B[k].get(x) for x in ("human", "human_page", "gold", "scaffold", "scaffold_pct") if x in B[k]})
for k in sorted(set(A) - set(B)): print("GONE", k, {x: A[k].get(x) for x in ("human", "human_page", "gold", "scaffold", "scaffold_pct") if x in A[k]})
for k in ("GEO1004/GEO1004_0_0.html", "GEO1004_0_0.html", "GEO1004/GEO1004_1_0.html", "GEO1004_1_0.html"):
    if k in A or k in B: print("GEO", k, "old:", A.get(k, {}).get("human") or A.get(k, {}).get("human_page"), "new:", B.get(k, {}).get("human") or B.get(k, {}).get("human_page"))
