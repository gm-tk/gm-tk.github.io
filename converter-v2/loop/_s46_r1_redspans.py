#!/usr/bin/env python3
"""Session 46 Round 1 — every red span inside the declined item-2 accordion tables, tested against the r491 marker_table
vocabulary (read from data/Emit_Templates.json), so each refusal names its span. WSL, from outputs/:
    python3 _s46_r1_redspans.py [_s46_r1_accdump_OFF.json] [CODE ...]"""
import json, re, sys, collections
DATA = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/data/Emit_Templates.json"
mt = json.load(open(DATA))["interactive_builders"]["accordion"]["panel_delimiters"]["marker_table"]
pats = {k: re.compile(mt[k], re.I) for k in ("head_pattern", "bare_head_pattern", "heading_pattern", "body_pattern", "image_pattern", "closer_pattern")}
src = next((a for a in sys.argv[1:] if a.endswith(".json")), "_s46_r1_accdump_OFF.json")
codes = [a for a in sys.argv[1:] if not a.endswith(".json")]
sys.argv = ["x", "--scored"]
exec(open("_s46_r1_accclass.py").read().split("by = collections")[0])
RED = re.compile("\U0001f534\\[RED TEXT\\]([\\s\\S]*?)\\[/RED TEXT\\]\U0001f534")
unk = collections.Counter()
for r in [x for x in json.load(open(src)) if not x["built"]]:
    if classify(r) != "item2-markers-in-cells" or (codes and r["code"] not in codes): continue
    bad = []
    for m in r["members"]:
        if not m or m["k"] != "table": continue
        for row in m["rows"]:
            for c in row:
                for s in RED.findall(c):
                    s = s.strip()
                    if not any(p.search(s) for p in pats.values()) and not re.fullmatch(r"\d{1,2}", s): bad.append(s[:70]); unk[s[:40]] += 1
    print(f"{r['code']} {r['page']} #{r['index']}: {len(bad)} unknown  {bad[:5]}")
print("\nmost common unknown spans:", unk.most_common(25))
