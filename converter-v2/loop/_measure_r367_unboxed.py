#!/usr/bin/env python3
"""r367 PICK probe (session 21, Round 4) — THE UN-BOXED STANDALONE WIDGET. The r217 standalone box wraps a bare widget tag in a
numbered activity box only for `standalone_widget_box.types` (dragAndDrop, unclassified, multiChoiceQuiz, radioQuiz, selfCheck,
interactive). Every OTHER un-built capture that sits in no activity box on Claude's page (dropDown, typing, reorder, modal,
carousel, accordion, flipCard, …): does the gold wrap the same widget in an activity box? The widget is matched on the gold page
by the capture's first member paragraph or first table cell text. Aggregated by capture type, owner, template. Writes
_r367_unboxed.{json,log}."""
import os, re, sys, json, io, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
for p in (HERE, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, HERE); sys.path.insert(0, TESTS)
import _corpus
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE
from _measure_ceiling import has_source, unorm, load_meta

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
    out = []
    for m in re.finditer(r'<div class="activity[^"]*"[^>]*>', html):
        out.append((m.start(), balanced(html, m.end())))
    return out
def captures(html):
    rngs = box_ranges(html); out = []
    for m in re.finditer(r'<div class="cv2-interactive cv2-int-ref"[^>]*>', html):
        end = balanced(html, m.end()); block = html[m.end():end]
        h = HDR.search(block)
        if not h: continue
        boxed = any(a < m.start() < b for a, b in rngs)
        k = block.find('<div style="font-size: 0.95em">', h.end())
        inner = block[k:] if k >= 0 else block[h.end():]
        txt = None
        pm = re.search(r"<p>(.*?)</p>", inner, re.S)
        if pm: txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", pm.group(1))).strip()
        if not txt or len(txt.split()) < 2:
            tm = re.search(r"<t[dh][^>]*>(.*?)</t[dh]>", inner, re.S)
            if tm: txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", tm.group(1))).strip()
        out.append({"type": h.group(2).strip(), "owner": h.group(3).strip(), "boxed": boxed, "key": (txt or "")[:120]})
    return out
def gold_boxed(html, key):
    t = unorm(key)
    if len(t.split()) < 2: return "no-key"
    rngs = box_ranges(html)
    text_positions = []
    plain = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    # locate the key by scanning the tags-stripped text with an offset map (coarse): search each box's text first
    for a, b in rngs:
        seg = unorm(re.sub(r"<[^>]+>", " ", plain[a:b]))
        if has_source(t, " " + seg + " "): return "gold-boxed"
    if has_source(t, " " + unorm(re.sub(r"<[^>]+>", " ", plain)) + " "): return "gold-free"
    return "gold-absent"

meta = load_meta()
rows = []
codes = sorted(_corpus.gate_mods(CLAUDE))
for ci, code in enumerate(codes):
    m = meta.get(code) or {}
    for n, cp, hp in pairs(code):
        if re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I): continue
        craw = re.sub(r"<!--.*?-->", "", io.open(cp, encoding="utf-8", errors="replace").read(), flags=re.S)
        caps = [c for c in captures(craw) if not c["boxed"]]
        if not caps: continue
        graw = io.open(hp, encoding="utf-8", errors="replace").read()
        for c in caps:
            v = gold_boxed(graw, c["key"])
            rows.append({"module": code, "page": os.path.basename(cp), "type": c["type"], "owner": c["owner"], "verdict": v, "key": c["key"][:60],
                         "template": m.get("template_type", "?"), "subject": m.get("subject", "?")})
    if ci % 60 == 0: print(f"  … {ci}/{len(codes)} modules, {len(rows)} un-boxed captures", flush=True)
json.dump(rows, io.open(os.path.join(HERE, "_r367_unboxed.json"), "w", encoding="utf-8"), indent=0, ensure_ascii=False)
L = []
def P(*a): s = " ".join(str(x) for x in a); L.append(s); print(s)
base = lambda t: t.split(" (")[0].split(" + ")[0].strip()
def agg(rs, key):
    d = collections.defaultdict(lambda: [0, 0, 0, set(), set()])
    for r in rs:
        k = key(r); d[k][0] += 1; d[k][1] += (r["verdict"] == "gold-boxed"); d[k][2] += (r["verdict"] == "no-key"); d[k][3].add(r["module"] + "/" + r["page"]); d[k][4].add(r["module"])
    return sorted(((k, v[0], round(v[1] / max(1, v[0] - v[2]), 2), v[2], len(v[3]), len(v[4])) for k, v in d.items()), key=lambda x: -x[1])
P(f"un-boxed captures: {len(rows)} on {len(set(r['module'] + '/' + r['page'] for r in rows))} pages / {len(set(r['module'] for r in rows))} modules")
P("verdicts:", collections.Counter(r["verdict"] for r in rows).most_common())
P("\nBY base type: n / gold-boxed share (of keyed) / no-key / pages / modules"); [P("  ", x) for x in agg(rows, lambda r: base(r["type"]))[:20]]
P("\nBY template:"); [P("  ", x) for x in agg(rows, lambda r: r["template"])]
P("\nBY subject:"); [P("  ", x) for x in agg(rows, lambda r: r["subject"])[:12]]
bx = [r for r in rows if r["verdict"] == "gold-boxed"]
P(f"\nTHE CLASS (gold boxes it, Claude has no box): {len(bx)} captures / {len(set(r['module'] + '/' + r['page'] for r in bx))} pages / {len(set(r['module'] for r in bx))} modules")
P("  by type:", collections.Counter(base(r["type"]) for r in bx).most_common(12))
P("  examples:", [(r["module"], r["page"], base(r["type"]), r["key"][:40]) for r in bx[:8]])
io.open(os.path.join(HERE, "_r367_unboxed.log"), "w", encoding="utf-8").write("\n".join(L) + "\n")
