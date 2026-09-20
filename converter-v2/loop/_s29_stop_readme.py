#!/usr/bin/env python3
"""session 29 stop — the loop README row for the Round 10 PICK pass (inserted above the Round 418 row). Run under WSL."""
import io
p = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/loop/README.md"
s = io.open(p, encoding="utf-8").read()
anchor = "| `_s29_r9_panelforms.{py,out}`"
assert s.count(anchor) == 1
row = ("| `_s29_r10_boxforms.{py,out}` / `_s29_r10_alertlead.{py,out}` / `_s29_r10_colmd12.{py,out}` / `_s29_r10_labelcensus.{py,out,json,log}` / "
       "`_s29_stop_{state,readme}.py` | `CONVERTER_V2/outputs/` | **Session 29 Round 10 PICK pass (2026-09-20, no engine change; ended by `/loop-stop`)** — four censuses "
       "on the r418 corpus, none at the floor: the container first-child ladder gold vs Claude for every callout / panel class (14 differing groups, all under 20 pages or "
       "dispositioned), the bare-lead alert (60 boxes / 47 pages, the gold bare 19 : wrapped 13 — a tie), the gold's `col-12 col-md-12` column by context (1734 vs 133 — the "
       "r331 widened wrapper + full-width body rows), and the s27-r1 position-free label census re-run (`span.ch-text` 494 on 32 pages / 11 Chinese modules = the next "
       "session's first measurement). |\n")
s = s.replace(anchor, row + anchor)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("README row inserted")
