#!/usr/bin/env python3
"""r419 — the loop README row (inserted above the session-29 stop row). Run under WSL."""
import io
p = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/loop/README.md"
s = io.open(p, encoding="utf-8").read()
anchor = "| `_s29_r10_boxforms.{py,out}`"
assert s.count(anchor) == 1, s.count(anchor)
row = ("| `_s30_r1_langfont.{py,out,json,log}` / `_s30_r1_langspans.{py,out}` / `_s30_r419_unit.cjs` / `_s30_r419_dipdiff.py` / "
       "`_s30_r419_{probe_run,regen,postship,checksums}.sh` / `_s30_r419_{pagescore,finalise,state,readme}.py` / "
       "`_s30_r419_{gates,gatecheck,spotcheck_plan,batch_plan,regen_batch_1..3,scoped_ship,selftests,index,postship,sk_full,skdelta,pagescore}.log` / "
       "`_s30_r419_probe_{OFF,ON}_0*.log` / `_s30_r419_{codes,ON_modules,OFF_modules,ON_pages}.txt` / `_s30_r419_sk_final.json` / `_s30_r419_onscore.json` / "
       "`_affected_r419.txt` / `_diff_miner_s30_r419.log` / `_diff_queue_pre_r419.md` | `CONVERTER_V2/outputs/` | **Round 419 (session 30 Round 1, 2026-09-21)** — "
       "THE LANGUAGE-FONT WRAP (KB constraint 92 / CL-0093, the CJK half): the paired language-font census (`_s30_r1_langfont.py`: the gold wraps 5,437 of 5,512 CJK "
       "runs = 0.99; Claude shipped 3,812 bare on 26 pages / 14 modules; the CHI1003–1005 dialogues are not in the WT) and the gold's FORM census (`_s30_r1_langspans.py`: "
       "carrier span 98 %, every context, the `<b>` outside, runs start on a character 4,331 : 64, pinyin's tone-mark discriminator 1,897 / 2,116); the 22-case unit "
       "check; the A/B probe (OFF = disk 2555 / 2555; ON 25 pages / 13 modules) and its scoring on the gate's own `match()` (13 up / 7 down, +49.7pp-sum; the JPN1004 "
       "dips inspected with `_s30_r419_dipdiff.py` — alignment artefacts, the form is the gold's); the SCOPED regeneration of the 13 + 12 spot-checks, `scoped_ship.sh "
       "--commit` (containment 13 ⊆ 13; skeleton 54.19 → 54.21, ≥50 1439 → 1441, cs exact +2; scoped #3 since the r416 FULL), the gates / selftests / index / miner "
       "(183 → 182) logs and the r419 skeleton state (+0.0212pp; 20 movers, 0 outside the set). |\n")
s = s.replace(anchor, row + anchor)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("README row inserted")
