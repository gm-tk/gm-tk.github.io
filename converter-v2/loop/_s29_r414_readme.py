#!/usr/bin/env python3
"""r414 — the loop README row (inserted above the Round 413 row). Run under WSL."""
import io
p = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/loop/README.md"
s = io.open(p, encoding="utf-8").read()
anchor = "| `_s29_r4_menucols.{py,out}`"
assert s.count(anchor) == 1
row = ("| `_s29_r5_emptyrows.{py,out}` / `_s29_r5_nestbox.{py,out}` / `_s29_r5_shellprobe{,2}.cjs` / `_s29_r5_unclass_T.tsv` / `_s29_r5_unclasscheck.out` / "
       "`_s29_r5_pick.py` / `_s29_r414_{probe_run,regen,postship,checksums,variants}.sh` / `_s29_r414_{pagescore,var_pagescore,finalise,state,readme}.py` / "
       "`_s29_r414_{gates,scoped_ship,selftests,index,spotcheck_plan,batch_plan,regen,regen_batch_1..7,sk_full,skdelta,pagescore}.log` / "
       "`_s29_r414_probe_{OFF,ON}_0*.log` / `_s29_r414_var_{ALLKEEP,ALLCLOSE}_{0..3,score}.log` / `_s29_r414_var_{ALLKEEP,ALLCLOSE}_score.json` / "
       "`_s29_r414_{codes,ON_modules,OFF_modules,ON_pages}.txt` / `_s29_r414_sk_final.json` / `_s29_r414_onscore.json` / `_affected_r414.txt` / "
       "`_diff_miner_s29_r414.log` / `_diff_queue_pre_r414.md` | `CONVERTER_V2/outputs/` | **Round 414 (session 29 Round 5, 2026-09-20)** — THE NESTED ACTIVITY BOX: "
       "the empty-shell census (`_s29_r5_emptyrows.py`: 818 empty `row › col` shells, 725 the module menu's, the body's 154 decomposed) led to the nested box "
       "(`_s29_r5_nestbox.py`: 108 boxes inside boxes on 94 pages / 65 modules, the gold on 3 pages; the inner always the r217 / r266 synthetic box, decided after "
       "the `isNewActivity` guard); the raw-parts probes (`_s29_r5_shellprobe{,2}.cjs` — the shell is the outer box's close landing in a lazily opened row); the "
       "A/B probe (OFF = disk 2555 / 2555; ON 94 pages / 65 modules); the two un-nesting forms scored on the gate's own `match()` (`_s29_r414_variants.sh`: suppress "
       "everywhere 81 up / 3 down, close-the-outer 28 / 24 — the widget belongs to the open box); the scoped regeneration (7 batches rc 0; 0 stale; containment "
       "65 ⊆ 65; spot-check 12 / 12) + ship checkpoint (PASS), the gates / selftests / miner logs and the r414 skeleton state. `_s29_r5_unclass_T.tsv` / "
       "`_s29_r5_unclasscheck.out` = the PICK-stage instrument that declined the unclassified-path later-heading rows (gold IN 8 / out 6 = 0.57 — the r362 guard stands). |\n")
s = s.replace(anchor, row + anchor, 1)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("README row added")
