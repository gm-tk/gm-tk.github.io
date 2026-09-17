#!/usr/bin/env python3
"""r368 PICK probe (session 21, Round 5) — WHO BOXES WHICH WIDGET. The miner pairs Claude's `activity EXTRA WIDGET` (#541, 237
pages) with the gold's `body MISSING WIDGET` (#6091, 226 pages): Claude's r217 standalone box wraps a widget the gold leaves
free in the body — or the reverse. Measured on the WIDGET ELEMENTS themselves (the skeleton's WIDGET_MARKERS classes on the
gold side; the cv2 captures + the same built-widget classes on Claude's side), never on text: for every paired page, every
widget on each side and whether it sits inside a `div.activity` box, by widget class (gold) / capture type (Claude) and by
template / subject. Writes _r368_boxshare.{json,log}."""
import os, re, sys, json, io, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
for p in (HERE, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, HERE); sys.path.insert(0, TESTS)
import _corpus
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE
from _structural_skeleton import WIDGET_MARKERS
from _measure_ceiling import load_meta

TAG = re.compile(r"<(/?)([a-zA-Z0-9]+)([^>]*)>")
HDR = re.compile(r"INTERACTIVE \(un-built\) #(\d+): ([^—<]+?) — ([^—<]+?) — see", re.S)
def balanced(html, start):
    depth = 1
    for t in TAG.finditer(html, start):
        if t.group(2).lower() != "div": continue
        depth += -1 if t.group(1) else 1
        if depth == 0: return t.start()
    return len(html)
def box_ranges(html):
    return [(m.start(), balanced(html, m.end())) for m in re.finditer(r'<div class="activity[^"]*"[^>]*>', html)]
MARK = set(x.lower() for x in WIDGET_MARKERS)
def widgets(html, side):
    """(kind, boxed, pos) for every widget marker element; Claude captures report the header type."""
    rngs = box_ranges(html); out = []; seen = set()
    for m in re.finditer(r'<div class="([^"]*)"[^>]*>', html):
        cls = set(m.group(1).lower().split())
        hit = cls & MARK
        if not hit: continue
        if "cv2-interactive" in cls and "cv2-int-ref" not in cls: continue     # the inner dashed box of a capture
        # skip a marker nested inside an already-counted marker's extent
        if any(a <= m.start() < b for a, b in seen): continue
        end = balanced(html, m.end()); seen.add((m.start(), end))
        kind = sorted(hit)[0]
        if side == "claude" and "cv2-int-ref" in cls:
            h = HDR.search(html, m.end(), end); kind = "capture:" + (h.group(2).strip().split(" (")[0].split(" + ")[0] if h else "?")
        boxed = any(a < m.start() < b for a, b in rngs)
        out.append((kind, boxed))
    return out

meta = load_meta()
rows = []
codes = sorted(_corpus.gate_mods(CLAUDE))
for ci, code in enumerate(codes):
    m = meta.get(code) or {}
    for n, cp, hp in pairs(code):
        if re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I): continue
        g = re.sub(r"<!--.*?-->", "", io.open(hp, encoding="utf-8", errors="replace").read(), flags=re.S)
        c = re.sub(r"<!--.*?-->", "", io.open(cp, encoding="utf-8", errors="replace").read(), flags=re.S)
        for kind, boxed in widgets(g, "gold"): rows.append({"side": "gold", "module": code, "page": os.path.basename(hp), "kind": kind, "boxed": boxed, "template": m.get("template_type", "?"), "subject": m.get("subject", "?")})
        for kind, boxed in widgets(c, "claude"): rows.append({"side": "claude", "module": code, "page": os.path.basename(cp), "kind": kind, "boxed": boxed, "template": m.get("template_type", "?"), "subject": m.get("subject", "?")})
    if ci % 60 == 0: print(f"  … {ci}/{len(codes)} modules, {len(rows)} widgets", flush=True)
json.dump(rows, io.open(os.path.join(HERE, "_r368_boxshare.json"), "w", encoding="utf-8"), indent=0, ensure_ascii=False)
L = []
def P(*a): s = " ".join(str(x) for x in a); L.append(s); print(s)
def tab(rs, key):
    d = collections.defaultdict(lambda: [0, 0, set()])
    for r in rs:
        k = key(r); d[k][0] += 1; d[k][1] += r["boxed"]; d[k][2].add(r["module"])
    return sorted(((k, v[0], round(v[1] / v[0], 2), len(v[2])) for k, v in d.items()), key=lambda x: -x[1])
gold = [r for r in rows if r["side"] == "gold"]; cl = [r for r in rows if r["side"] == "claude"]
P(f"gold widgets {len(gold)} (boxed {sum(r['boxed'] for r in gold) / max(1, len(gold)):.2f}); Claude widgets {len(cl)} (boxed {sum(r['boxed'] for r in cl) / max(1, len(cl)):.2f})")
P("\nGOLD by widget class: n / boxed share / modules"); [P("  ", x) for x in tab(gold, lambda r: r["kind"])[:24]]
P("\nCLAUDE by kind: n / boxed share / modules"); [P("  ", x) for x in tab(cl, lambda r: r["kind"])[:30]]
P("\nGOLD by template: "); [P("  ", x) for x in tab(gold, lambda r: r["template"])]
P("CLAUDE by template: "); [P("  ", x) for x in tab(cl, lambda r: r["template"])]
P("\nGOLD by subject: "); [P("  ", x) for x in tab(gold, lambda r: r["subject"])[:12]]
P("CLAUDE by subject: "); [P("  ", x) for x in tab(cl, lambda r: r["subject"])[:12]]
io.open(os.path.join(HERE, "_r368_boxshare.log"), "w", encoding="utf-8").write("\n".join(L) + "\n")
