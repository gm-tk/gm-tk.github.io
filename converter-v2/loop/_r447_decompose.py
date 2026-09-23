#!/usr/bin/env python3
"""Round 447 — decompose the scoped skeleton move: the corpus mean over 2476 (baseline) vs 2477 (now), the new pair's
own score, and the mean over the COMMON 2476 pairs (the like-for-like move). Run from reference/tests under WSL."""
import os, sys
sys.path.insert(0, os.getcwd())
import _fastloop_diff as F
base = F._load(F._baseline_paths()["sk"])["per_page"]
cur = F._load(os.path.join(F.CURRENT, "skeleton_scoped.json"))["per_page"]
aff = {c.strip() for c in open(os.path.join("..", "..", "outputs", "_affected_r447.txt")) if c.strip()}
scoped_codes = {r["module"] for r in cur}
key = lambda r: (r["module"], r["page"])
B = {key(r): r["scaffold"] for r in base}
new = {key(r): r["scaffold"] for r in base if r["module"] not in scoped_codes}
new.update({key(r): r["scaffold"] for r in cur})
sc = lambda v: v * 100 if v <= 1.0 else v
mb = sum(sc(v) for v in B.values()) / len(B); mn = sum(sc(v) for v in new.values()) / len(new)
common = [k for k in new if k in B]
mc = sum(sc(new[k]) for k in common) / len(common); mcb = sum(sc(B[k]) for k in common) / len(common)
added = [k for k in new if k not in B]; gone = [k for k in B if k not in new]
print(f"baseline mean {mb:.4f} @ {len(B)}  ->  now {mn:.4f} @ {len(new)}  ({mn-mb:+.4f}pp)")
print(f"COMMON {len(common)} pairs: {mcb:.4f} -> {mc:.4f}  ({mc-mcb:+.4f}pp)  <- the like-for-like move")
for k in added: print(f"NEW pair {k}: scaffold {sc(new[k]):.1f}")
for k in gone: print(f"GONE pair {k}: scaffold {sc(B[k]):.1f}")
up = sum(1 for k in common if new[k] > B[k] + 1e-12); dn = sum(1 for k in common if new[k] < B[k] - 1e-12)
print(f"movers on the common pairs: {up} up / {dn} down")
for thr in (50, 75, 90):
    print(f">={thr}: {sum(1 for v in B.values() if sc(v) >= thr)} -> {sum(1 for v in new.values() if sc(v) >= thr)}"
          f"  (common only: {sum(1 for k in common if sc(new[k]) >= thr) - sum(1 for k in common if sc(B[k]) >= thr):+d})")
