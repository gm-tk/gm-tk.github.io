#!/usr/bin/env python3
"""Session 42 Round 9 — the widget-build lane (§4 / D10-3): the r286 decline records on the r470 corpus, per widget type, grouped by
the builder's decline reason (decideBranch + decideWhy) and by authoring shape; pages / modules per bucket, largest first. The
§4 widget-build floor is 20 pages per authoring SHAPE family within a type. Run under WSL from CONVERTER_V2/outputs."""
import json, collections, sys
d = json.load(open("_r286_declines.json"))
R = d if isinstance(d, list) else (d.get("records") or next(v for v in d.values() if isinstance(v, list)))
TYPES = sys.argv[1:] or ["carousel", "accordion", "flipCard", "clickDrop", "dropDown", "modal", "tabs", "selfCheck", "dragAndDrop"]
for t in TYPES:
    rs = [r for r in R if r["type"] == t and not r["built"]]
    print(f"\n=== {t}: {len(rs)} declined / {len(set(r['code'] for r in rs))} modules")
    by = collections.defaultdict(list)
    for r in rs: by[(r.get("decideBranch"), (r.get("decideWhy") or "")[:90])].append(r)
    for (br, why), v in sorted(by.items(), key=lambda x: -len(x[1]))[:6]:
        pages = set((r["code"], r["page"]) for r in v); mods = set(r["code"] for r in v)
        shp = collections.Counter(r.get("shape") for r in v).most_common(3)
        print(f"  {len(v):4d} bundles {len(pages):4d} pg {len(mods):3d} mod  [{br}] {why}")
        print(f"         shapes: {shp}  e.g. {v[0]['code']} {v[0]['page']}")
