#!/usr/bin/env python3
"""ROUND 456 — §1e population split from _r458_prescore.log (per gold page: OLD = the r454 disk, NEW = the ON pages): pairs on
both sides (the pre-existing population), new pairs, lost pairs; every per-page dip listed. Run under WSL."""
import re, os
H = os.path.dirname(os.path.abspath(__file__))
rows = []
for l in open(os.path.join(H, "_r458_prescore.log"), encoding="utf-8"):
    m = re.match(r"\s+(\S+)\s+OLD\s+(\S+)\s+([\d.]+|——)\s+NEW\s+(\S+)\s+([\d.]+|——)", l)
    if m: rows.append(m.groups())
both = [(g, oc, float(o), nc, float(n)) for g, oc, o, nc, n in rows if o != "——" and n != "——"]
new = [(g, nc, float(n)) for g, oc, o, nc, n in rows if o == "——" and n != "——"]
lost = [(g, oc, float(o)) for g, oc, o, nc, n in rows if o != "——" and n == "——"]
so = sum(r[2] for r in both); sn = sum(r[4] for r in both)
print(f"pre-existing pairs {len(both)}: sum {so:.1f} -> {sn:.1f} ({sn - so:+.1f} pp-sum)")
dips = sorted([r for r in both if r[4] < r[2] - 0.05], key=lambda r: r[4] - r[2])
print(f"dips {len(dips)}:")
for g, oc, o, nc, n in dips: print(f"   {g:32s} {oc:18s} {o:5.1f} -> {nc:18s} {n:5.1f} ({n - o:+.1f})")
ups = [r for r in both if r[4] > r[2] + 0.05]
print(f"ups {len(ups)}")
print(f"new pairs {len(new)}, mean {sum(r[2] for r in new) / max(1, len(new)):.1f}")
print(f"lost pairs {len(lost)}: {lost}")
BASE, N = 54.8967, 2519
pre = (BASE * N + (sn - so) - sum(r[2] for r in lost)) / (N - len(lost))
print(f"pre-existing population (excluding lost): {BASE:.4f} -> {pre:.4f} ({pre - BASE:+.4f}pp)")
