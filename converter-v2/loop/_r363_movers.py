#!/usr/bin/env python3
"""r363 — per-page skeleton movers between two _skeleton_compare --json states (default r362 -> r363)."""
import json, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
A = sys.argv[1] if len(sys.argv) > 1 else "_r362_sk_final.json"
B = sys.argv[2] if len(sys.argv) > 2 else "_r363_sk_final.json"
a = json.load(open(os.path.join(HERE, A))); b = json.load(open(os.path.join(HERE, B)))
pa = a["per_page"]; pb = b["per_page"]


def d(p):
    if isinstance(p, dict):
        return {k: (v["scaffold"] if isinstance(v, dict) else v) for k, v in p.items()}
    out = {}
    for r in p:
        if isinstance(r, dict):
            out[r.get("page") or r.get("claude") or r.get("name")] = r.get("scaffold") if r.get("scaffold") is not None else r.get("sca")
        else:
            out[r[3] if len(r) > 3 else r[0]] = r[0]
    return out


da, db = d(pa), d(pb)
mv = [(k, da[k], db[k]) for k in db if k in da and abs(db[k] - da[k]) > 1e-9]
up = sum(1 for _, x, y in mv if y > x); dn = len(mv) - up
print(f"movers {len(mv)}: up {up} / down {dn}; pp-sum {100 * sum(y - x for _, x, y in mv):+.1f}")
mv.sort(key=lambda t: t[2] - t[1])
print("dips:", [(k, round(100 * x, 1), round(100 * y, 1)) for k, x, y in mv[:8]])
print("gains:", [(k, round(100 * x, 1), round(100 * y, 1)) for k, x, y in mv[-6:]])
sm_a, sm_b = a["scaffold_mean"], b["scaffold_mean"]
print(f"mean {100 * sm_a:.4f} -> {100 * sm_b:.4f} ({100 * (sm_b - sm_a):+.3f}pp); raw {100 * a['raw_mean']:.3f} -> {100 * b['raw_mean']:.3f}")
for thr in (0.5, 0.75, 0.9):
    print(f"  >= {int(thr * 100)}: {sum(1 for v in da.values() if v >= thr)} -> {sum(1 for v in db.values() if v >= thr)}")
