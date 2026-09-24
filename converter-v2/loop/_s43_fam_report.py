#!/usr/bin/env python3
"""Session 43 — the widget family from _s43_family_{off,on}.json: bundles / built / modules per state for TYPE, and the
family list (every module carrying TYPE in the OFF state) written to OUT. Usage: python3 _s43_fam_report.py TYPE OUT"""
import json, sys
T, OUT = sys.argv[1], sys.argv[2]
for tag in ("off", "on"):
    try: R = json.load(open(f"_s43_family_{tag}.json"))
    except FileNotFoundError: continue
    f = [r for r in R if r["type"] == T]
    print(tag, T, "bundles", len(f), "built", sum(1 for r in f if r["built"]), "modules", len({r["code"] for r in f}),
          "built-lossy", sum(1 for r in f if r["built"] and r["lost"]))
R = json.load(open("_s43_family_off.json"))
mods = sorted({r["code"] for r in R if r["type"] == T})
open(OUT, "w").write("\n".join(mods) + "\n")
print("family", len(mods), "->", OUT)
