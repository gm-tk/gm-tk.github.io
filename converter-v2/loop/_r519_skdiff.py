"""_r519_skdiff.py — per-page skeleton delta: the last-ship baseline vs the scoped current. Run under WSL from outputs/."""
import json, sys
B = json.load(open("_fastloop_baseline/skeleton.json"))
C = json.load(open("_fastloop_current/skeleton_scoped.json"))
def rows(d):
    if isinstance(d, dict):
        for k in ("per_page", "rows", "results"):
            if k in d: return rows(d[k])
        return d
    return {(r.get("module"), r.get("page") or r.get("gold") or r.get("file")): r for r in d}
b, c = rows(B), rows(C)
def sc(r):
    if isinstance(r, dict):
        for k in ("scaffold", "scaffold_pct", "score", "pct"):
            if k in r: return float(r[k])
    return float(r)
print("keys b", list(b)[:2], "type", type(next(iter(b.values()))))
out = []
for k, r in c.items():
    if k in b:
        d = sc(r) - sc(b[k])
        if abs(d) > 1e-9: out.append((d, k, sc(b[k]), sc(r)))
for d, k, x, y in sorted(out): print(f"{d:+.4f}  {k}  {x:.2f} -> {y:.2f}")
print("pages moved", len(out), "sum", round(sum(o[0] for o in out), 4))
k = ("MXFL401", "MXFL401_6_0.html")
print("baseline", b.get(k)); print("current ", c.get(k))
