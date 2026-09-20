#!/usr/bin/env python3
"""r417 — the loop README row (inserted above the Round 416 row). Run under WSL."""
import io
p = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/loop/README.md"
s = io.open(p, encoding="utf-8").read()
anchor = "| `_s29_r7_emptybox.out`"
assert s.count(anchor) == 1
row = ("| `_s29_r8_boxcol.{py,out}` / `_s29_r8_xdlsrow.{py,out}` / `_s29_r8_pick.py` / `_s29_r417_{probe_run,regen,postship,checksums}.sh` / "
       "`_s29_r417_{pagescore,finalise,state,readme}.py` / `_s29_r417_{gates,gatecheck,spotcheck_plan,batch_plan,regen_batch_1..3,scoped_ship,selftests,index,"
       "postship,sk_full,skdelta,pagescore}.log` / `_s29_r417_probe_{OFF,ON}_0*.log` / `_s29_r417_{codes,ON_modules,OFF_modules,ON_pages}.txt` / "
       "`_s29_r417_sk_final.json` / `_s29_r417_onscore.json` / `_affected_r417.txt` / `_diff_miner_s29_r417.log` / `_diff_queue_pre_r417.md` | "
       "`CONVERTER_V2/outputs/` | **Round 417 (session 29 Round 8, 2026-09-20)** — THE XDLS CHOICE-PAGE PANEL HOLDS ITS CONTENT DIRECTLY: the activity-box "
       "column census (`_s29_r8_boxcol.py`: the box's first col class gold vs Claude per subject|template and family — the ONE real difference in the whole census is "
       "the XDLS family, gold `(no row>col)` 0.69 of 341) decomposed per module (`_s29_r8_xdlsrow.py`: the gold's r307 `clickDropContent activity dropbox` panels hold "
       "their content directly on 144 / 145; Claude wrapped all 179 in `row > col-12`); the A/B probe (OFF = disk 2555 / 2555; ON 30 pages / 5 modules) and its scoring "
       "on the gate's own `match()` (30 up / 0 down, +457.4pp-sum); the SCOPED regeneration of the 5 + the 12-module spot-check (3 batches rc 0, 0 truly stale, 12 / 12 "
       "byte-identical), `scoped_ship.sh --commit` (containment 5 ⊆ 5; skeleton 53.93 → 54.12, ≥50 1415 → 1438, every other row HELD; scoped #1 since the r416 FULL), the "
       "gates / selftests / index / miner (181 → 182 — two XDLS rows the panel's inner lines uncovered) logs and the r417 skeleton state (+0.1947pp; `_s29_r417_skdelta.log`: "
       "30 movers, 0 outside the set). |\n")
s = s.replace(anchor, row + anchor)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("README row inserted")
