#!/usr/bin/env python3
"""session 29 round 9 (round 418) — per-page skeleton delta: the probe's ON pages (outputs/_s28_t3_on/<code>/) vs the disk
pages, both against the gold via the gate's own match(). Codes = outputs/_s28_t3_ON_modules.txt (or argv[1] list file)."""
import os, sys, json, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
sys.path.insert(0, HERE); sys.path.insert(0, TESTS)
import _corpus
from _discrepancy_audit import pairs
from _skeleton_compare import match
ON = os.path.join(HERE, "_s29_r418_on")
lst = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "_s29_r418_ON_modules.txt")
codes = [l.split(":")[0].strip() for l in open(lst) if l.strip()]
rows = []; up = down = same = 0; dsum = 0.0; rsum = 0.0
for code in codes:
    for n, cp, hp in pairs(code):
        if re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I): continue
        onp = os.path.join(ON, code, os.path.basename(cp))
        if not os.path.exists(onp): continue
        if open(onp, encoding="utf-8", errors="replace").read() == open(cp, encoding="utf-8", errors="replace").read(): continue
        a, _, _ = match(cp, hp, scaffold=True); b, _, _ = match(onp, hp, scaffold=True)
        ra, _, _ = match(cp, hp, scaffold=False); rb, _, _ = match(onp, hp, scaffold=False)
        rows.append((code, os.path.basename(cp), 100 * a, 100 * b, 100 * ra, 100 * rb)); dsum += 100 * (b - a); rsum += 100 * (rb - ra)
        if b > a + 1e-9: up += 1
        elif b < a - 1e-9: down += 1
        else: same += 1
print(f"changed paired pages {len(rows)}: up {up} / down {down} / same {same}; SCAFFOLD pp-sum {dsum:+.1f} (mean {dsum/max(1,len(rows)):+.2f}pp per page); RAW pp-sum {rsum:+.1f}")
rows.sort(key=lambda r: r[3] - r[2])
for c, p, a, b, ra, rb in rows: print(f"  {c} {p} scaffold {a:.1f} -> {b:.1f} ({b-a:+.1f})   raw {ra:.1f} -> {rb:.1f} ({rb-ra:+.1f})")
json.dump(rows, open(os.path.join(HERE, "_s29_r418_onscore.json"), "w"), indent=0)
