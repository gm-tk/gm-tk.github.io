#!/usr/bin/env python3
"""Session 46 Round 1 — classify the declined accordion bundles (_s46_r1_accdump.json) by authoring shape, mapped onto
WHY_UNBUILT__accordion.md's suggested order (items 1–6) and its reasons. Run under WSL from CONVERTER_V2/outputs:
    python3 _s46_r1_accclass.py [_s46_r1_accdump.json] [--show SHAPE] [--scored]"""
import json, re, sys, collections, os
src = next((a for a in sys.argv[1:] if a.endswith(".json")), "_s46_r1_accdump.json")
show = sys.argv[sys.argv.index("--show") + 1] if "--show" in sys.argv else None
R = [r for r in json.load(open(src)) if not r["built"]]
excl = set()
ce = "../reference/tests/compare_exclusions.txt"
if os.path.exists(ce):
    for l in open(ce):
        l = l.strip()
        if l and not l.startswith("#"): excl.add(l.split()[0])
if "--scored" in sys.argv: R = [r for r in R if r["code"] not in excl]

MARK = re.compile(r"\[\s*(accordion|acc)\s*\d*\s*\]|\[\s*h[2-5]\s*\]|\[\s*body\s*\]", re.I)
HDRW = re.compile(r"^\s*(images?|instructions?|heading|headings|content|front|back|drop|title|text|panel|question|answer|accordion|body|topic|description)\b.*$", re.I)
BUL_BOLD = re.compile(r"^\s*[•·▪◦‣\-\*]\s*\*\*(.+?)\*\*")
def tags(r): return [(m.get("tag") or "").lower() for m in r["members"] if m and m["k"] == "tag"]
def texts(r):
    out = []
    for m in r["members"]:
        if not m: continue
        if m["k"] == "black": out.append(m["text"])
        elif m["k"] == "tag": out.append(m.get("after") or "")
    return out
def classify(r):
    ms = [m for m in r["members"] if m]
    if not ms: return "4-captured-nothing"
    tabs = [m for m in ms if m["k"] == "tag" and False] + [m for m in ms if m["k"] == "table"]
    nested = [m for m in ms if m["k"] == "nested"]
    tg = tags(r)
    if nested: return "3-nested-widget"
    if "button" in tg: return "item5-button"
    if tabs:
        if len(tabs) > 1: return "1D-multi-table"
        rows = tabs[0]["rows"]
        cells = " ".join(c for row in rows for c in row)
        if MARK.search(cells): return "item2-markers-in-cells"
        if len(rows) == 1: return "item6/1C-one-row-table"
        first = [c.strip() for c in rows[0] if c.strip()]
        if first and all(len(c.split()) <= 4 for c in first) and any(HDRW.match(re.sub(r"[\*\[\]]", " ", c)) for c in first): return "item3-header-row"
        return "1B-plain-grid"
    acc = [t for t in tg if t.startswith("accordion")]
    lines = [l for t in texts(r) for l in t.split("\n") if l.strip()]
    if not acc and sum(1 for l in lines if BUL_BOLD.match(l)) >= 2: return "item1-bulleted-bold"
    if acc:
        # the last [accordion N] tag with nothing after it = an empty trailing panel
        last = max(i for i, m in enumerate(ms) if m["k"] == "tag" and (m.get("tag") or "").lower().startswith("accordion"))
        tail = ms[last + 1:]
        if not tail and not (ms[last].get("after") or "").strip(): return "item4-empty-trailing-panel"
        return "5/6-panels-other"
    if not lines and not any(m["k"] == "tag" for m in ms): return "4-captured-nothing"
    return "2-prose/other"
by = collections.defaultdict(list)
for r in R: by[classify(r)].append(r)
print(f"{len(R)} declined accordion bundles, {len(set(r['code'] for r in R))} modules")
for k, v in sorted(by.items(), key=lambda x: -len(x[1])):
    mods = collections.Counter(r["code"] for r in v)
    print(f"  {len(v):4d} bundles {len(set((r['code'], r['page']) for r in v)):4d} pg {len(mods):3d} mod  {k:32s} {', '.join(f'{c}×{n}' for c, n in mods.most_common(8))}")
if show:
    for r in by.get(show, [])[:40]:
        print(f"\n=== {r['code']} {r['page']} #{r['index']}")
        for m in r["opener"][:2]: print("   OPEN", json.dumps(m, ensure_ascii=False)[:300])
        for m in r["members"][:14]:
            if m and m["k"] == "table":
                for row in m["rows"][:5]: print("   ROW", json.dumps(row, ensure_ascii=False)[:420])
            else: print("   MEM", json.dumps(m, ensure_ascii=False)[:300])
