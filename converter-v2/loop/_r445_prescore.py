#!/usr/bin/env python3
"""ROUND 445 (session 39 Round 7 — D13-2, the comparison table) — pre-score the ON pages with the gate's own pairing and match().
For each changed module (_r444_ON_modules.txt): pairs() on the disk (the r441 state), then each pair's SCAFFOLD with the disk page (OLD) and
with the ON page saved by `_r445_probe_run.sh SAVE` (NEW). Prints every mover, the up / down counts, the pp-sum
and the corpus-mean estimate (pp-sum / 2476 pairs).
Run from CONVERTER_V2/reference/tests under WSL: python3 ../../outputs/_r442_prescore.py
"""
import os, sys
sys.path.insert(0, os.getcwd())
from _discrepancy_audit import pairs
from _skeleton_compare import match

O = os.path.join("..", "..", "outputs")
codes = [c.strip() for c in open(os.path.join(O, "_r445_ON_modules.txt")) if c.strip()]
rows = []
for code in codes:
    for n, cp, hp in pairs(code):
        onp = os.path.join(O, "_r445_on", code, os.path.basename(cp))
        if not os.path.exists(onp):
            continue
        a = match(cp, hp, scaffold=True)[0]
        b = match(onp, hp, scaffold=True)[0]
        if abs(b - a) > 1e-9:
            rows.append((b - a, code, os.path.basename(cp), os.path.basename(hp), a, b))
rows.sort()
for d, code, cf, hf, a, b in rows:
    print(f"{code:8s} {cf:20s} <-> {hf:28s} {100*a:5.1f} -> {100*b:5.1f}  ({100*d:+.1f})")
up = sum(1 for r in rows if r[0] > 0); dn = sum(1 for r in rows if r[0] < 0)
pp = 100 * sum(r[0] for r in rows)
print(f"movers {len(rows)}: {up} up / {dn} down, pp-sum {pp:+.1f}  ->  corpus mean ≈ {pp/2476:+.4f}pp over 2476 pairs")
b50 = sum(1 for r in rows if r[4] < 0.5 <= r[5]) - sum(1 for r in rows if r[5] < 0.5 <= r[4])
b75 = sum(1 for r in rows if r[4] < 0.75 <= r[5]) - sum(1 for r in rows if r[5] < 0.75 <= r[4])
print(f">=50 {b50:+d}   >=75 {b75:+d}")
