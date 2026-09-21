#!/usr/bin/env python3
"""r420 — the loop README row (inserted above the Round 419 row). Run under WSL."""
import io
p = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/loop/README.md"
s = io.open(p, encoding="utf-8").read()
anchor = "| `_s30_r1_langfont.{py,out,json,log}`"
assert s.count(anchor) == 1, s.count(anchor)
row = ("| `_s30_r2_alertsolid.{py,out}` / `_s30_r2_widecol.{py,out}` / `_s30_r2_shapes.{py,out}` / `_s30_r2_bingo.{py,out,json}` / `_s30_r2_scdump.cjs` / "
       "`_s30_r2_scdump_bll.log` / `_s30_r2_scdump_bll2.log` / `_s30_r2_boxinner.{py,out}` / `_s30_r420_dipdiff.py` / `_s30_r420_{probe_run,regen,postship,checksums}.sh` / "
       "`_s30_r420_{pagescore,finalise,state,readme}.py` / `_s30_r420_{gates,gatecheck,spotcheck_plan,batch_plan,regen_batch_1..3,scoped_ship,fastloop_named,selftests,index,postship,sk_full,skdelta,pagescore,probe_bll}.log` / "
       "`_s30_r420_probe_{OFF,ON}_0*.log` / `_s30_r420_{codes,ON_modules,OFF_modules,ON_pages}.txt` / `_s30_r420_sk_final.json` / `_s30_r420_onscore.json` / "
       "`_affected_r420.txt` / `_diff_miner_s30_r420.log` / `_diff_queue_pre_r420.md` / `_verify_bingo.cjs` / `_selftest_core.cjs` / `run_all_gates.sh` | `CONVERTER_V2/outputs/` (the three gate tools: `CONVERTER_V2/reference/tests/`) | "
       "**Round 420 (session 30 Round 2, 2026-09-21)** — THE LETTER-GRID BINGO (Chris's D10-3 build lane, the selfCheck kickoff's shape 1): the PICK-pass censuses "
       "(the alert-solid pairing — the gold keeps `solid` 22 / 295, KB-correct declined; the widened `col-md-12` wrapper per built widget type ≤ 0.36 in every group, "
       "D10-3's item closed; the r286 decline records re-read by CONTENT; the bingo / letter-grid census — 55 WT letter-grid tables in 9 modules against the gold's 74 "
       "letter-grid bingos of 96; the live-scanner bundle dumps; the box-inner-shape census — the bare box 0.07 corpus-wide); the A/B probe (OFF = disk 2555 / 2555; "
       "ON 7 pages / 7 modules) and its scoring (RAW +4.7pp-sum; scaffold −1.1 = the r289 widget-marker class, named); the SCOPED regeneration of the 7 + 12 "
       "spot-checks, the scoped-ship log and the named-movement commit; the gates (the NEW protected `_verify_bingo.cjs` — 52 grids / defect 0) / 17 selftests / index / "
       "miner (182 → 182) logs and the r420 skeleton state (−0.0005pp; 7 movers, 0 outside the set). |\n")
s = s.replace(anchor, row + anchor)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("README row inserted")
