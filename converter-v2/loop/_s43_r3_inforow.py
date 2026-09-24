#!/usr/bin/env python3
"""Session 43 Round 3 — the placement census transition `menu:Information → menu:Overview` (and any gold→claude pair given) split by
module: the blocks per module and their text, so the non-BLL modules (outside Needs Chris #22) can be read. The census JSON keeps
only 8 examples per row, so this re-reads the per-block records if the census stored them, else re-runs the census matcher on the
listed modules. Usage (WSL, outputs/): python3 _s43_r3_inforow.py 'menu:Information' 'menu:Overview' [CODES...]"""
import json, sys, subprocess, os
G, C = sys.argv[1], sys.argv[2]
codes = sys.argv[3:]
d = json.load(open("_placement_census.json"))
row = [t for t in d["transitions"] if t["gold"] == G and t["claude"] == C]
if not row: raise SystemExit("no such transition")
row = row[0]
print(row["rank"], G, "->", C, row["blocks"], "blocks /", row["pages"], "pages /", row["modules"], "modules")
print("families", row["families"])
mods = codes or [m for m in row["module_list"]]
print("modules:", " ".join(mods))
for ex in row["examples"]:
    print("  ex", ex)
