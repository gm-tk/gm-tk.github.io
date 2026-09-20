#!/usr/bin/env python3
"""r417 finalise — LOOP_STATE.md: the Round 8 PICK section moves to the archive (+ the what-shipped record), the Position updates,
the Round-log line is appended. Run under WSL."""
import os, io
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
STATE, ARCH = R + "LOOP_STATE.md", R + "LOOP_STATE_ARCHIVE.md"
lines = io.open(STATE, encoding="utf-8").read().split("\n")
def idx(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix): return i
    raise SystemExit("not found: " + prefix)
a = idx("## Session 29 — Round 8 PICK (engine r417)"); b = idx("## Round log")
pick = lines[a:b]
shipped = ("- **What shipped (r417, build 260619.88, 20 Sept ≈21:40):** `interactive_builders.clickDrop.tile_grid.panel_no_inner_row {enabled, env CDPANELROW_OFF}` + "
           "`activity_wrapper.open_bare / close_bare` — `ActivitiesBuilder.activityOpen` emits the bare box open (`<div class=\"activity{modifiers}\"{numberAttr}>`) and pushes "
           "the bare close for a `_r307PanelId`-tagged opener on the standard (non-supervisor-note) path; every other box byte-identical; the r307 pairing and r305 dropbox "
           "post-passes read only the opening tag / a balanced div span, so the class tokens land unchanged. Probe OFF = disk 2555 / 2555; ON 30 pages / 5 modules "
           "(XDLS902–906); scored on the gate's own `match()` 30 up / 0 down, +457.4pp-sum (XDLS903_7_0 +27.1). SCOPED regeneration of the 5 + the 12-module spot-check "
           "(`_s29_r417_regen.sh`, 3 batches rc 0): 0 truly stale, 12 / 12 byte-identical; `scoped_ship.sh --commit` containment 5 ⊆ 5, the fast-loop baseline patched, the "
           "manifest refreshed, the ledger scoped #1 since the r416 FULL (7 of headroom). `run_all_gates.sh`: every row HELD-or-IMPROVED — skeleton 53.9284 → 54.1231 % "
           "(+0.1947pp; 30 movers 30 up / 0 down, 0 outside the set), ≥50 1415 → 1438, ≥75 238 / ≥90 20 EXACT, RAW 38.000 → 38.142; cs 14168 / 186 / 683 / 23, body 54 / 5 / "
           "190 / 247, clean 2504 / 2548, leak 73 / 44, tags 9557 — all EXACT; every verifier ✓; 16 selftests GREEN (46 / 0); feature index GREEN; miner 181 → 182 (two "
           "XDLS rows the panel's inner lines uncovered: #1035 the r308 per-panel upload button 23 pages / 4 modules — the gold consolidates to one per page, the XDLS501 "
           "over-emit named at r308; #1036 the gold's minority `row.clickDropContent.noBorder > col-12.col-md-8 > activity.dropbox` wrapper 21 / 4); checksums engine 3 "
           "changed / gates 0. Plateau: +0.1947pp — the window RESETS (0 of 3).")
lines[a:b] = ["## Session 29 — Round 8 (engine r417) — THE XDLS CHOICE-PAGE PANEL HOLDS ITS CONTENT DIRECTLY — SHIPPED; the PICK + what-shipped record is in LOOP_STATE_ARCHIVE.md 'Session 29 — Round 8 PICK (engine r417) + what shipped'; the one-line summary is the s29-r8 Round-log line below.", ""]
p = idx("- LAST SHIPPED: **r416**")
lines[p] = ("- LAST SHIPPED: **r417** (build 260619.88, 20 Sept ≈21:40, session 29 Round 8 — THE XDLS CHOICE-PAGE PANEL HOLDS ITS CONTENT DIRECTLY: the r307 "
            "`clickDropContent activity dropbox` panel without the inner `row > col-12` — the gold's panel opens straight onto its `<h3>` / `<p>` / video on 144 / 145, "
            "Claude wrapped all 179; `tile_grid.panel_no_inner_row` + `activity_wrapper.open_bare / close_bare`, env `CDPANELROW_OFF`; probe OFF = disk 2555 / 2555, ON "
            "30 pages / 5 modules (30 up / 0 down, +457.4pp-sum); SCOPED regeneration of the 5 (scoped ship #1 since the r416 FULL); **skeleton 53.928 → 54.123 % "
            "(+0.1947pp), ≥50 1415 → 1438, ≥75 238, ≥90 20, RAW 38.142 % @ 2349 pairs**; cs 14168 / 186 / 683 / 23, body 54 / 5 / 190 / 247, clean 2504 / 2548, leak "
            "73 / 44 — all EXACT; every verifier EXACT; 16 selftests GREEN; the miner 181 → 182); before it **r416** (build 260619.87, 20 Sept ≈21:05, session 29 Round 7 — "
            "the activity title typed inside the red span, `EMBTITLE_OFF`, 22 up / 12 down, +0.0174pp; THE FULL REGENERATION of all 494, the ledger's backstop, counter 0), "
            "**r415** (build 260619.86, the owned heading-led bundle with no table, `NOTABLEOWNED_OFF`, +0.0246pp, ≥50 +3), **r414** (build 260619.85, the nested activity "
            "box, `NESTBOX_OFF`, +0.0696pp, ≥50 +4, ≥75 +2), **r413** (build 260619.84, the owned half of the r412 class, `HEADTABLEOWNED_OFF`, +0.0080pp), **r412** "
            "(build 260619.83, the heading-then-table owner form, `HEADTABLE_OFF`, +0.0139pp), **r411** (build 260619.82, the tile menu ROW+COL shell, `TILEMENUROW_OFF`, "
            "+0.0058pp) and **r410** (build 260619.81, the WJFUN tile-page dialect, `TILEPAGE_OFF`, 53.680 → 53.789 %, ≥50 +8). **Corpus = r417** (2555 pages / 494 dirs / "
            "2349 pairs; `gate_baseline.json` at r417; `outputs/_s29_r417_sk_final.json` the skeleton state; ceiling 90.9 % → 54.123 = **59.5 % of achievable**).")
q = idx("- Plateau window (§4): **1 of 3**")
lines[q] = "- Plateau window (§4): **0 of 3** — RESET by r417 (+0.1947pp, ≥50 +23); before it r416 +0.0174 (the one sub-0.02 round), r415 +0.0246, r414 +0.0696. Read every delta on the post-intake 2,349-pair population (§1e)."
r = idx("- Standing facts: AppVersion 260619.87")
lines[r] = lines[r].replace("AppVersion 260619.87 (r416, session 29 Round 7, 20 Sept); before it 260619.86 (r415)", "AppVersion 260619.88 (r417, session 29 Round 8, 20 Sept); before it 260619.87 (r416) / 260619.86 (r415)")
assert "260619.88" in lines[r]
t = idx("- s29-r7 (engine r416")
lines.insert(t + 1, "- s29-r8 (engine r417, build 260619.88, 20 Sept ≈21:10 → 21:40) · THE XDLS CHOICE-PAGE PANEL HOLDS ITS CONTENT DIRECTLY — the r307 tile-grid panel (`[Activity] **2A**`, tagged `_r307PanelId`) opened through the standard `activity_wrapper.open`, so every panel carried an inner `row > col-12` where the gold's `clickDropContent activity dropbox` panel opens straight onto its `<h3>` / `<p>` / video (144 / 145 on XDLS902–906 + 909; Claude wrapped all 179 on 30 pages / 5 modules) — found by the activity-box column census (`_s29_r8_boxcol.py`: the box's first col class gold vs Claude per subject|template and family — the ONE real difference in the whole census; `_s29_r8_xdlsrow.py` per module) · `tile_grid.panel_no_inner_row {enabled, env CDPANELROW_OFF}` + `activity_wrapper.open_bare / close_bare`; `ActivitiesBuilder.activityOpen` emits the bare form for a panel anchor on the standard path · SHIPPED · probe OFF = disk 2555 / 2555, ON 30 pages / 5 modules (30 up / 0 down, +457.4pp-sum) · SCOPED regeneration of the 5 + 12 spot-checks (0 truly stale, 12 / 12 byte-identical; scoped ship #1 since the r416 FULL) · skeleton 53.928 → 54.123 (+0.1947pp; 30 movers, 0 outside the set), ≥50 1415 → 1438, ≥75 238, ≥90 20, RAW 38.142; every other gate EXACT · miner 181 → 182 (#1035 the per-panel upload button 23 / 4 — the r308 XDLS501 over-emit class; #1036 the gold's `noBorder` row wrapper 21 / 4 — the next PICK pass's candidates) · plateau RESET 0 of 3 · recorded: #4 (the gold's Te Reo lesson titles, class C), GENO901 / DTC1005 single-module leaks, #32–#34 menu rows, #589 (WJFUN col-12 0.73, Claude right), the XDLS plain boxes' 7 / 7 tie")
io.open(STATE, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
with io.open(ARCH, "a", encoding="utf-8", newline="\n") as f:
    f.write("\n## Session 29 — Round 8 PICK (engine r417) + what shipped — THE XDLS CHOICE-PAGE PANEL HOLDS ITS CONTENT DIRECTLY (20 Sept ≈21:10 → 21:40 NZST)\n\n" + "\n".join(pick).rstrip("\n") + "\n" + shipped + "\n")
print("LOOP_STATE.md", os.path.getsize(STATE), "bytes; archive", os.path.getsize(ARCH))
