#!/usr/bin/env python3
"""Round 447 — which skeleton PAIR appeared (sk_pages 2476 -> 2477)? Compares the fast-loop baseline's per-page keys
(the r446 state) with the scoped re-score's per-page keys for the affected modules. Run from reference/tests under WSL."""
import os, sys, json
sys.path.insert(0, os.getcwd())
import _fastloop_diff as F
base = F._load(F._baseline_paths()["sk"])["per_page"]
cur = F._load(os.path.join(F.CURRENT, "skeleton_scoped.json"))["per_page"]
aff = [c.strip() for c in open(os.path.join("..", "..", "outputs", "_affected_r447.txt")) if c.strip()]
def keyset(rows):
    out = {}
    for r in rows:
        k = r.get("module") or r.get("code") or r.get("mod")
        out.setdefault(k, []).append(r)
    return out
print("row keys:", sorted(base[0].keys()) if isinstance(base, list) and base else type(base))
B = keyset(base) if isinstance(base, list) else base
C = keyset(cur) if isinstance(cur, list) else cur
for code in sorted(set(C) | set(aff)):
    b = B.get(code, []); c = C.get(code, [])
    if len(b) != len(c):
        print(f"{code}: baseline {len(b)} pairs -> now {len(c)}")
        bn = {json.dumps({k: v for k, v in r.items() if k not in ('score', 'scaffold', 'raw', 'ratio')}, sort_keys=True) for r in b}
        for r in c:
            s = json.dumps({k: v for k, v in r.items() if k not in ('score', 'scaffold', 'raw', 'ratio')}, sort_keys=True)
            if s not in bn: print("   NEW:", s[:300])
        cn = {json.dumps({k: v for k, v in r.items() if k not in ('score', 'scaffold', 'raw', 'ratio')}, sort_keys=True) for r in c}
        for r in b:
            s = json.dumps({k: v for k, v in r.items() if k not in ('score', 'scaffold', 'raw', 'ratio')}, sort_keys=True)
            if s not in cn: print("   GONE:", s[:300])
