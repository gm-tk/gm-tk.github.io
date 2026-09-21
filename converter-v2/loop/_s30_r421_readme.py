#!/usr/bin/env python3
"""r421 — the loop README row (inserted above the Round 420 row); the Round 3 PICK-pass instruments ride in the same row. Run under WSL."""
import io
p = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/loop/README.md"
s = io.open(p, encoding="utf-8").read()
anchor = "| `_s30_r2_alertsolid.{py,out}`"
assert s.count(anchor) == 1, s.count(anchor)
row = ("| `_s30_r3_sctables.{py,out}` / `_s30_r3_sidepad.{py,out}` / `_s30_r3_buttons.{py,out}` / `_s30_r3_bold.{py,out}` / `_s30_r3_thbold.{py,out}` / "
       "`_s30_r3_sassoon.{py,out}` / `_s30_r3_alertactivity.{py,out}` / `_s30_r3_uncdump.cjs` / `_s30_r3_uncdump.tsv` / `_s30_r3_uncpair.{py,out}` / "
       "`_s30_r3_dddump.tsv` / `_s30_r3_ddpair.{py,out}` / `_s30_r3_ddhead.{py,out}` / `_s30_r4_fcdump.tsv` / `_s30_r4_fcpair.{py,out}` / "
       "`_s30_r421_{probe_run,regen,postship,checksums}.sh` / `_s30_r421_{finalise,state,readme}.py` / "
       "`_s30_r421_{gates,gatecheck,spotcheck_plan,batch_plan,regen_batch_1..3,scoped_ship,fastloop_named,selftests,index,postship,sk_full,skdelta}.log` / "
       "`_s30_r421_probe_{OFF,ON}_0*.log` / `_s30_r421_{codes,ON_modules,OFF_modules,ON_pages}.txt` / `_s30_r421_sk_final.json` / `_affected_r421.txt` / "
       "`_diff_miner_s30_r421.log` / `_diff_queue_pre_r421.md` | `CONVERTER_V2/outputs/` | **Rounds 3–4 (session 30, 2026-09-21)** — the Round 3 PICK pass "
       "(nine instruments, nothing at the floor: the selfCheck kickoff's other shapes, the two-column padding, the missing buttons, the writer's bold by "
       "context, the Sassoon font contexts, the gold's alertActivity, the unclassified and dragAndDrop one-table bundles paired to the gold's widgets — the "
       "header-red 2-column D&D 25 sites at standard 0.44) and **Round 421 — THE REGISTRY-KNOWN MODULE CODE**: the A/B probe (OFF = disk 2555 / 2555; ON = "
       "exactly CHWHA / GEWHA / ANZHFUN05 / PWYWHA1, each output renamed), the SCOPED regeneration of the 4 + 12 spot-checks, the scoped-ship log and the "
       "named-movement commit (−0.0002pp: the four re-paired pages), the gates / 17 selftests / index / miner (182 → 182) logs and the r421 skeleton state. |\n")
s = s.replace(anchor, row + anchor)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("README row inserted")
