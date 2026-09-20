#!/usr/bin/env python3
"""r415 — the loop README row (inserted above the Round 414 row). Run under WSL."""
import io
p = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/loop/README.md"
s = io.open(p, encoding="utf-8").read()
anchor = "| `_s29_r5_emptyrows.{py,out}`"
assert s.count(anchor) == 1
row = ("| `_s29_r6_emptybox.{py,out}` / `_s29_r6_notable_rows.tsv` / `_s29_r6_goldcheck.py` / `_s29_r6_notablecheck.out` / `_s29_r6_colwidth.{py,out}` / "
       "`_s29_r6_intflag.{py,out}` / `_s29_r6_rowpair.out` / `_s29_r6_widgetflow.{py,out}` / `_s29_r6_pick.py` / "
       "`_s29_r415_{probe_run,regen,postship,checksums}.sh` / `_s29_r415_{pagescore,finalise,state,readme}.py` / "
       "`_s29_r415_{gates,scoped_ship,cs_decomp,fastloop_commit,selftests,index,spotcheck_plan,batch_plan,regen,regen_batch_1..4,sk_full,skdelta,pagescore}.log` / "
       "`_s29_r415_probe_{OFF,ON}_0*.log` / `_s29_r415_{codes,codes_0*,ON_modules,OFF_modules,ON_pages}.txt` / `_s29_r415_sk_final.json` / `_s29_r415_onscore.json` / "
       "`_affected_r415.txt` / `_diff_miner_s29_r415.log` / `_diff_queue_pre_r415.md` | `CONVERTER_V2/outputs/` | **Round 415 (session 29 Round 6, 2026-09-20)** — "
       "THE OWNED HEADING-LED BUNDLE WITH NO TABLE: the empty-box census (`_s29_r6_emptybox.py`: Claude 96 EMPTY writer-owned boxes on 73 pages / 47 modules; the gold's "
       "same-numbered box holds text 39 / media 21 = 0.63) + the r4 owned-walk census's no-table rows (`_s29_r6_notable_rows.tsv`, 47 owned bundles) → the gold check over "
       "all 125 heading-led no-table bundles (`_s29_r6_goldcheck.py`: IN 46 / 99 = 0.46, a tie split by family — the unowned half 0.41 stays free, the owned half decided "
       "by the gate's own scorer: `_s29_r415_pagescore.py` 34 paired pages 24 up / 2 down / 8 same, +57.7pp-sum; without WJFUN 16 / 2, +36.6); the A/B probe (OFF = disk "
       "2555 / 2555; ON 35 pages / 22 modules — the r92 embedded-id form `[Activity 1A] [Dropdown Quiz…]` widened the gate to `activityId != null`); the scoped regeneration "
       "(4 batches rc 0; 0 truly stale; containment 22 ⊆ 22; spot-check 12 / 12); the ship checkpoint FAILED on `compare_structure exact chain` −6 alone → decomposed per "
       "module (`_s29_r415_cs_decomp.log`: the matched pool −13, every one inside the affected set — the r57 / r147 relocation class) → `_fastloop_diff.py --accept-named` "
       "(`_s29_r415_fastloop_commit.log`) + the manifest snapshot; the gates / selftests / miner (181 → 181) logs and the r415 skeleton state (+0.0246pp, ≥50 +3). "
       "`_s29_r6_colwidth` / `_s29_r6_intflag` / `_s29_r6_rowpair` / `_s29_r6_widgetflow` = the PICK-stage instruments that declined DIFF_QUEUE #3677 (the gold's single-column "
       "body row is `col-12 col-md-8` ≥ 0.78), #587 / #606 (the `interactive` flag tracks the widget Claude's box holds; the 446 gold-interactive / Claude-plain boxes hold no "
       "widget) and the after-widget row break (0.63 skeleton-line vs 0.57 raw-HTML — a tie). |\n")
s = s.replace(anchor, row + anchor)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("README row inserted")
