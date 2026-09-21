#!/usr/bin/env python3
"""Session 30 stop — the loop README row for the Round 6 PICK pass + the stop (inserted above the Round 422 row). Run under WSL."""
import io
p = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/loop/README.md"
s = io.open(p, encoding="utf-8").read()
anchor = "| `_s30_r5_items.cjs`"
assert s.count(anchor) == 1, s.count(anchor)
row = ("| `_s30_r6_{carousel,accordion,flipCard,clickDrop}.log` / `_s30_r6_modal_dump.log` / `_s30_r6_shapes.{py,out}` / `_s30_r6_accdump.tsv` / "
       "`_s30_r6_accjoin.py` / `_s30_stop_state.py` / `_s30_condense.py` / `_s30_stop_readme.py` | `CONVERTER_V2/outputs/` | **Session 30 Round 6 PICK pass + the "
       "STOP (2026-09-21, §4 EXHAUSTION)** — the D10-3 widget lane re-read by CONTENT from the disk boxes: the four big types' bundles dumped through the live "
       "scanner and joined to the disk truth (every remaining un-built shape ≤ 13 sites or the gold absent / diffuse; the accordion + one-table bundles paired "
       "to the gold); the stop-state and §5d-condense scripts (the s29 instrument / Round 10 sections and the s30 Round 5 / 6 sections archived). |\n")
s = s.replace(anchor, row + anchor)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("README row inserted")
