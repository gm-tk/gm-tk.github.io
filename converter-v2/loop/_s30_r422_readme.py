#!/usr/bin/env python3
"""r422 — the loop README row (inserted above the Rounds 3–4 row). Run under WSL."""
import io
p = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/loop/README.md"
s = io.open(p, encoding="utf-8").read()
anchor = "| `_s30_r3_sctables.{py,out}`"
assert s.count(anchor) == 1, s.count(anchor)
row = ("| `_s30_r5_items.cjs` / `_s30_r5_items_frfun06.log` / `_s30_r422_{probe_run,checksums}.sh` / `_s30_r422_{pagescore,finalise,readme}.py` / "
       "`_s30_r422_probe_ON_0*.log` / `_s30_r422_{codes,ON_modules,OFF_modules}.txt` / `_s30_r422_selftests.log` | `CONVERTER_V2/outputs/` | "
       "**Round 422 (session 30 Round 5, 2026-09-21) — DECLINED-INERT** — THE SIDE-TAB-NAVIGATION FUNDAMENTALS DIALECT (FRFUN06): the item-stream dump that "
       "showed the r100 inquiry mode firing on `[Side tab navigation]` and dropping every label; the build (`inquiry_tabs.side_tab_nav` + the fundamentals "
       "flavour) measured in memory — FRFUN06 10 / 10 pages, 8 up / 2 down, +34.7pp-sum; FRFUN07 / 08 unchanged — and shipped `enabled: false` (10 pages / 1 "
       "module, under the floor; enabling it is Chris's call); the corpus proven byte-identical (2555 / 2555), the selftests GREEN. |\n")
s = s.replace(anchor, row + anchor)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("README row inserted")
