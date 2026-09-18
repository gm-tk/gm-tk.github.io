#!/usr/bin/env python3
"""r392 — per-page skeleton delta: the probe's ON pages (outputs/_s26_r394_on/<code>/) vs the disk pages, both against the gold via the gate's own match()."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
sys.path.insert(0, HERE); sys.path.insert(0, TESTS)
import _corpus, re
from _discrepancy_audit import pairs
from _skeleton_compare import match
from anchor_compare import CLAUDE
ON = os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else "_s26_r394_on")
codes = [l.split(":")[0].strip() for l in open(os.path.join(HERE, "_s26_r394_changed_modules.txt")) if l.strip()]
rows = []; up = down = same = 0; dsum = 0.0
for code in codes:
    for n, cp, hp in pairs(code):
        if re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I): continue
        onp = os.path.join(ON, code, os.path.basename(cp))
        if not os.path.exists(onp): continue
        if open(onp, encoding="utf-8", errors="replace").read() == open(cp, encoding="utf-8", errors="replace").read(): continue
        a, _, _ = match(cp, hp, scaffold=True); b, _, _ = match(onp, hp, scaffold=True)
        rows.append((code, os.path.basename(cp), 100 * a, 100 * b)); dsum += 100 * (b - a)
        if b > a + 1e-9: up += 1
        elif b < a - 1e-9: down += 1
        else: same += 1
print(f"changed paired pages {len(rows)}: up {up} / down {down} / same {same}; pp-sum {dsum:+.1f}; mean delta {dsum/max(1,len(rows)):+.2f}pp per changed page")
rows.sort(key=lambda r: r[3] - r[2])
print("worst 12:"); [print(f"  {c} {p} {a:.1f} -> {b:.1f} ({b-a:+.1f})") for c, p, a, b in rows[:12]]
print("best 8:"); [print(f"  {c} {p} {a:.1f} -> {b:.1f} ({b-a:+.1f})") for c, p, a, b in rows[-8:]]
json.dump(rows, open(os.path.join(HERE, "_s26_r394_onscore.json"), "w"), indent=0)
