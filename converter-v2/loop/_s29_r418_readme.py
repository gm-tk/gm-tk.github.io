#!/usr/bin/env python3
"""r418 — the loop README row (inserted above the Round 417 row). Run under WSL."""
import io
p = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/loop/README.md"
s = io.open(p, encoding="utf-8").read()
anchor = "| `_s29_r8_boxcol.{py,out}`"
assert s.count(anchor) == 1
row = ("| `_s29_r9_panelforms.{py,out}` / `_s29_r9_pick.py` / `_s29_r418_{probe_run,regen,postship,checksums}.sh` / `_s29_r418_{pagescore,finalise,state,readme}.py` / "
       "`_s29_r418_{gates,gatecheck,spotcheck_plan,batch_plan,regen_batch_1..3,scoped_ship,selftests,index,postship,sk_full,skdelta,pagescore}.log` / "
       "`_s29_r418_probe_{OFF,ON}_0*.log` / `_s29_r418_{codes,ON_modules,OFF_modules,ON_pages}.txt` / `_s29_r418_sk_final.json` / `_s29_r418_onscore.json` / "
       "`_affected_r418.txt` / `_diff_miner_s29_r418.log` / `_diff_queue_pre_r418.md` | `CONVERTER_V2/outputs/` | **Round 418 (session 29 Round 9, 2026-09-20)** — "
       "THE FIRST TILE PANEL TAKES THE `row.clickDropContent.noBorder` FORM + THE r417 TITLE-PIN REPAIR: the per-page panel-form census (`_s29_r9_panelforms.py`: the "
       "gold's first panel is the row form on 35 / 35 pages of XDLS902–906 with the `clickDropContent` token on the section row; the gold's ONE upload button per page = "
       "an invented box, the per-panel button declined class C) and the r417 defect it found (114 of 179 bare panels at h5 — the r334 pin read the inner row / col); "
       "the A/B probe (OFF = disk + the 20 repaired pages; ON 30 pages / 5 modules, every changed line one of three kinds) and its scoring on the gate's own `match()` "
       "(30 up / 0 down, +147.9pp-sum); the SCOPED regeneration of the 5 + 12 spot-checks, `scoped_ship.sh --commit` (containment 5 ⊆ 5; skeleton 54.12 → 54.19, ≥50 "
       "1438 → 1439; scoped #2 since the r416 FULL), the gates / selftests / index / miner (182 → 183) logs and the r418 skeleton state (+0.0630pp; 30 movers, 0 outside "
       "the set). |\n")
s = s.replace(anchor, row + anchor)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("README row inserted")
