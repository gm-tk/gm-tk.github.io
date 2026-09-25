#!/usr/bin/env python3
"""_s51_prescore.py — the skeleton gate's own match() on a probe's SAVED ON pages vs the pages on disk (OFF), per page and
summed; the mean delta over the whole paired population (2,486 pairs, from the newest full sk_final). WSL, from
reference/tests/:  python3 ../../outputs/_s51_prescore.py /tmp/SAVEDIR [N_PAIRS]"""
import os, sys
sys.path.insert(0, os.getcwd())
from _discrepancy_audit import pairs
import _skeleton_compare as K

save = sys.argv[1]; npairs = int(sys.argv[2]) if len(sys.argv) > 2 else 2486
rows = []
for code in sorted(os.listdir(save)):
    for n, cp, hp in pairs(code):
        on = os.path.join(save, code, os.path.basename(cp))
        if not os.path.exists(on): continue
        a = K.match(cp, hp, True)[0]; b = K.match(on, hp, True)[0]
        if abs(b - a) > 1e-9: rows.append((b - a, code, os.path.basename(cp), a, b))
rows.sort()
for d, code, p, a, b in rows: print(f"{p:28s} {a * 100:6.2f} -> {b * 100:6.2f}  ({d * 100:+.2f})")
up = sum(1 for r in rows if r[0] > 0); dn = sum(1 for r in rows if r[0] < 0); s = sum(r[0] for r in rows)
print(f"pages moved {len(rows)}: {up} up / {dn} down; sum {s * 100:+.2f}pp; mean delta over {npairs} pairs {s * 100 / npairs:+.4f}pp")
