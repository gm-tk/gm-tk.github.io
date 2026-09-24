#!/usr/bin/env python3
"""Session 43 — the media-aware loss census report: per widget type, built bundles / bundles losing LEARNER text (not a media
label) / pages / modules / lost learner parts by source; then examples for one type.
Usage: python3 _s43_wl2_report.py <json> [TYPE [N]]"""
import json, sys, collections
recs = json.load(open(sys.argv[1]))
by = collections.defaultdict(lambda: {"built": 0, "lossy": 0, "pages": set(), "mods": set(), "parts": 0, "src": collections.Counter(), "media": 0})
for r in recs:
    b = by[r["type"]]; b["built"] += 1; b["media"] += r["lostMedia"]
    if r["lostReal"]:
        b["lossy"] += 1; b["pages"].add((r["code"], r["page"])); b["mods"].add(r["code"]); b["parts"] += r["lostReal"]
        for x in r["real"]: b["src"][x["src"]] += 1
print(f"{'type':16} {'built':>6} {'lossy':>6} {'pages':>6} {'mods':>5} {'parts':>6} {'media':>6}  by source")
for t, b in sorted(by.items(), key=lambda kv: -kv[1]["lossy"]):
    if not b["lossy"] and not b["media"]: continue
    print(f"{t:16} {b['built']:6} {b['lossy']:6} {len(b['pages']):6} {len(b['mods']):5} {b['parts']:6} {b['media']:6}  {dict(b['src'])}")
if len(sys.argv) > 2:
    T = sys.argv[2]; n = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    for r in [r for r in recs if r["type"] == T and r["lostReal"]][:n]:
        print(f"  {r['code']} p{r['page']} #{r['index']} runs {r['runs']} lostReal {r['lostReal']} media {r['lostMedia']}")
        for x in r["real"][:3]: print(f"      [{x['src']}] {x['raw'][:130]}")
