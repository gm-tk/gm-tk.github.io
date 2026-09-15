#!/usr/bin/env python3
"""ROUND 326 diagnostic — is a page's skeleton dip STRUCTURAL or a SCORER ARTEFACT?

The PRIMARY gate scores difflib.SequenceMatcher over the page's skeleton LINES after
_structural_skeleton collapses consecutive repeats into one "┌ N× repeated block of K:" line.
Wrapping a button in <a> can turn `p / div.button / p / a>div.button / p` into ONE collapsed
"2× repeated block of 3" line — a shape the gold's skeleton does not use — and the ratio drops
sharply although the page's element sequence now matches the gold's better (XMES201_5_0:
0.667 → 0.479 collapsed, while the gold carries the same `a > div.button`).

For each moved page (OFF page saved by _r322_probe.cjs --save, ON page on disk, the gate's own
gold pairing) this prints the gate ratio (collapsed lines) AND the ratio over the UNCOLLAPSED
line sequence, ON vs OFF. If the uncollapsed delta is >= 0 where the gate delta is < 0, the dip
is the scorer's repeat-collapsing, not the structure. Run from reference/tests (WSL):
  python3 ../../outputs/_r326_scorer_diag.py ../../outputs/_r326_off_pages ../../outputs/_r326_sk_moved.json
"""
import os, sys, json, glob, difflib
sys.path.insert(0, ".")
import _structural_skeleton as S
from _discrepancy_audit import pairs
import _corpus

OFFDIR, MOVED = sys.argv[1], sys.argv[2]
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CLAUDE = os.path.join(ROOT, "01-Claude_Modules_")

_orig_render_children = S.render_children


def _flat_children(kids, indent):
    _NOTE_CLS = {"cv2-comment", "cv2-note"}
    kids = [k for k in kids if not (_NOTE_CLS & set((k.attrs.get("class") or "").split()))]
    out = []
    for k in kids:
        out += S.render(k, indent)
    return out


def skel(path, collapsed):
    S._SCAFFOLD = True
    S.render_children = _orig_render_children if collapsed else _flat_children
    sk = S.skeleton(path).splitlines()
    return sk[sk.index("body.container-fluid"):] if "body.container-fluid" in sk else sk


def ratio(a, b):
    return difflib.SequenceMatcher(None, b, a).ratio()


moved = json.load(open(MOVED))["moved"]
want = {k for k, _, _ in moved}
rows = []
for code in sorted({k.split("_")[0] for k in want}):
    offmod = os.path.join(OFFDIR, code)
    if not os.path.isdir(offmod):
        continue
    for n, cp, hp in pairs(code):
        name = os.path.basename(cp)
        if name not in want:
            continue
        offp = os.path.join(offmod, name)
        if not os.path.exists(offp):
            continue
        g_c, g_f = skel(hp, True), skel(hp, False)
        on_c, on_f = skel(cp, True), skel(cp, False)
        off_c, off_f = skel(offp, True), skel(offp, False)
        gate_d = (ratio(on_c, g_c) - ratio(off_c, g_c)) * 100
        flat_d = (ratio(on_f, g_f) - ratio(off_f, g_f)) * 100
        rows.append((name, gate_d, flat_d))
S.render_children = _orig_render_children
rows.sort(key=lambda r: r[1])
dips = [r for r in rows if r[1] < -1e-9]
rises = [r for r in rows if r[1] > 1e-9]
print("pages scored: %d | gate dips %d | gate rises %d" % (len(rows), len(dips), len(rises)))
art = [r for r in dips if r[2] >= -1e-9]
print("dips whose UNCOLLAPSED delta is >= 0 (scorer artefact): %d of %d" % (len(art), len(dips)))
real = [r for r in dips if r[2] < -1e-9]
print("dips that ALSO dip uncollapsed (structural): %d — %s" % (len(real), [(n, "%+.2f/%+.2f" % (g, f)) for n, g, f in real[:15]]))
print("gate pp-sum %+.2f | uncollapsed pp-sum %+.2f" % (sum(r[1] for r in rows), sum(r[2] for r in rows)))
print("biggest gate dips (name, gate, uncollapsed):", [(n, "%+.2f" % g, "%+.2f" % f) for n, g, f in rows[:12]])
json.dump(rows, open(os.path.join(os.path.dirname(MOVED), "_r326_scorer_diag.json"), "w"), indent=1)
