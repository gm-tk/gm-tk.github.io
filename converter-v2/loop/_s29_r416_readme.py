#!/usr/bin/env python3
"""r416 — the loop README row (inserted above the Round 415 row). Run under WSL."""
import io
p = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/loop/README.md"
s = io.open(p, encoding="utf-8").read()
anchor = "| `_s29_r6_emptybox.{py,out}`"
assert s.count(anchor) == 1
row = ("| `_s29_r7_emptybox.out` / `_s29_r7_boxtitle.{py,out,json}` / `_s29_r7_boxtitle2.{py,out}` / `_s29_r7_boxnum.{py,out}` / `_s29_r7_redtitle.{py,out,json}` / "
       "`_s29_r7_parse.cjs` / `_s29_r7_titlerule.cjs` / `_s29_r7_pick.py` / `_s29_r416_{probe_run,fullship_par,postship,checksums}.sh` / `_s29_r416_fullship_run.sh` / "
       "`_s29_r416_{pagescore,finalise,state,readme}.py` / `_s29_r416_helper_tail.js` / `_s29_r416_{gates,gatecheck,stale_manifest,fullship_regen,batch_1..39,selftests,"
       "index,fastloop_snapshot,manifest_snapshot,postship,sk_full,skdelta,pagescore}.log` / `_s29_r416_probe_{OFF,ON}_0*.log` / `_s29_r416_{codes,ON_modules,OFF_modules,"
       "ON_pages,ON_pagenames,manifest_changed_modules,manifest_changed_pages}.txt` / `_s29_r416_sk_final.json` / `_s29_r416_onscore.json` / `_affected_r416.txt` / "
       "`_diff_miner_s29_r416.log` / `_diff_queue_pre_r416.md` | `CONVERTER_V2/outputs/` | **Round 416 (session 29 Round 7, 2026-09-20)** — THE ACTIVITY TITLE TYPED "
       "INSIDE THE RED SPAN + THE FULL-REGENERATION BACKSTOP: DIFF_QUEUE #585 (`activity MISSING h3`, 384 pages) decomposed by `_s29_r7_boxtitle.py` (7582 gold box titles: "
       "MATCH 3275; the rest = the r369 numbering class (`_s29_r7_boxnum.py`: 631 / 3540 title-paired boxes with a different number), the gold's invented titles (1486, "
       "class C), the Bilingual table dialect, and the `opener red-embedded` rows) → `_s29_r7_redtitle.py` (216 red-embedded opener spans / 86 modules) → `_s29_r7_titlerule.cjs` "
       "(the rule with the LIVE normaliser: 48 sites / 30 modules, the gold's h3 on 40 = 0.83); the A/B probe (OFF = disk 2555 / 2555; ON 44 pages / 37 modules) and its scoring "
       "on the gate's own `match()` (22 up / 12 down / 7 same, +33.1pp-sum — the first probe's 49 pages taught the rule its `interactive`-alias, run-split continuation, "
       "capital, trailing-stop and broken-bracket guards); THE FULL REGENERATION of all 494 (`_s29_r416_fullship_par.sh`: `_batch_plan.py`'s 39 batches, 4 workers, all rc 0, "
       "6 min) — 0 stale, the manifest diff = the probe's 44 pages exactly (`_s29_r416_stale_manifest.log`: no residue from r409–r415); the gates / gatecheck (every row "
       "HELD-or-IMPROVED) / selftests / index / miner (181 → 181) logs, the ledger record-full (counter 0), the fast-loop + manifest snapshots and the r416 skeleton state "
       "(+0.0174pp, buckets EXACT; `_s29_r416_skdelta.log`: 33 movers, 0 outside the set, the ENGI101 / MXDI101 pairing re-resolutions named). `_s29_r7_emptybox.out` = the "
       "r6 census re-run on the r415 corpus (64 empty boxes left, 34 with no gold box). |\n")
s = s.replace(anchor, row + anchor)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("README row inserted")
