#!/usr/bin/env python3
"""Session 46 Round 1 — a compact listing of the 'markers in cells' accordion declines (item 2). WSL, from outputs/."""
import json, re, sys
sys.argv = ["x", "--scored"]
exec(open("_s46_r1_accclass.py").read().split("by = collections")[0])
red = re.compile("\U0001f534\\[RED TEXT\\]|\\[/RED TEXT\\]\U0001f534")
want = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else "item2-markers-in-cells"
for r in R:
    if classify(r) != want: continue
    ts = [m for m in r["members"] if m and m["k"] == "table"]
    other = [(m.get("tag") or m["k"]) for m in r["members"] if m and m["k"] != "table"]
    print(f"{r['code']} {r['page']} #{r['index']} tables={len(ts)} other={other[:8]}")
    for t in ts[:1]:
        rows = t["rows"]
        print(f"    rows={len(rows)} cols={max(len(x) for x in rows)}")
        for row in rows[:3]:
            print("    |", " || ".join(red.sub("", c).replace("\n", " ")[:80] for c in row))
