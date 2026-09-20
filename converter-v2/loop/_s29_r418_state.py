#!/usr/bin/env python3
"""r418 finalise — LOOP_STATE.md: the Round 9 PICK section moves to the archive (+ the what-shipped record), the Position updates,
the Round-log line is appended; PLUS the §5d condense (LOOP_STATE.md crossed 100 KB): the s21–s26 Round-log lines (37) move to the
archive under 'Round-log lines s21–s26 (archived …)', a one-line pointer stays. Run under WSL."""
import os, io
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
STATE, ARCH = R + "LOOP_STATE.md", R + "LOOP_STATE_ARCHIVE.md"
lines = io.open(STATE, encoding="utf-8").read().split("\n")
def idx(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix): return i
    raise SystemExit("not found: " + prefix)
a = idx("## Session 29 — Round 9 PICK (engine r418)"); b = idx("## Round log")
pick = lines[a:b]
shipped = ("- **What shipped (r418, build 260619.89, 20 Sept ≈22:05):** (a) `activityTitleLevelPostpass`'s `titleRe` inner `row > col-12` group made OPTIONAL — the "
           "r417 bare panel had lost the r334 `<h3>` pin (114 of 179 panels at h5; repaired, not reverted; untoggled — r417's own defect); (b) "
           "`interactive_builders.clickDrop.tile_grid.first_panel_row {enabled, env CDFIRSTROW_OFF, row_open, col_open_pattern, row_class_open}` — in "
           "`ContentConverter.#cdTilePair` the first panel id's box keeps its own class and the section row directly wrapping it (`<div class=\"row\">` + "
           "`<div class=\"col-md-8 col-12\">`, nothing else between) takes `row clickDropContent noBorder`; any other shape keeps the prefix form. Probe OFF "
           "(`CDFIRSTROW_OFF`) = the disk + the 20 pin-repaired pages; ON 30 pages / 5 modules — every changed line one of three kinds (114 h5 → h3 titles, 30 section "
           "rows, 30 first-panel boxes); scored 30 up / 0 down, +147.9pp-sum (XDLS904_2_0 +16.1). SCOPED regeneration of the 5 + 12 spot-checks (0 truly stale, 12 / 12 "
           "byte-identical); `scoped_ship.sh --commit` containment 5 ⊆ 5, the ledger scoped #2 since the r416 FULL (6 of headroom). `run_all_gates.sh`: skeleton "
           "54.1231 → 54.1860 % (+0.0630pp; 30 movers 30 up / 0 down, 0 outside the set), ≥50 1438 → 1439, ≥75 238 / ≥90 20 EXACT, RAW 38.142 → 38.204; cs 14168 / 186 / "
           "683 / 23, body 54 / 5 / 190 / 247, clean 2504 / 2548, leak 73 / 44, tags 9557 — all EXACT; every verifier ✓; 16 selftests GREEN (46 / 0); feature index GREEN; "
           "miner 182 → 183 (#1036 gone; `activity EXTRA div.activity.dropbox › a` = the declined per-panel upload button; `activity MISSING div.col-12.col-md-8 › "
           "div.activity.dropbox` = XDLS902 lessons 2–7's all-row form, 6 pages — the module's own); checksums engine 4 changed / gates 0. Plateau: +0.0630pp — 0 of 3.")
lines[a:b] = ["## Session 29 — Round 9 (engine r418) — THE FIRST TILE PANEL TAKES THE `row.clickDropContent.noBorder` FORM + the r417 title-pin repair — SHIPPED; the PICK + what-shipped record is in LOOP_STATE_ARCHIVE.md 'Session 29 — Round 9 PICK (engine r418) + what shipped'; the one-line summary is the s29-r9 Round-log line below.", ""]
p = idx("- LAST SHIPPED: **r417**")
lines[p] = ("- LAST SHIPPED: **r418** (build 260619.89, 20 Sept ≈22:05, session 29 Round 9 — THE FIRST TILE PANEL TAKES THE `row.clickDropContent.noBorder` FORM (the "
            "gold's first panel on every choice page puts the `clickDropContent` token on the section row, 35 / 35 pages of XDLS902–906; `tile_grid.first_panel_row`, env "
            "`CDFIRSTROW_OFF`) + THE r417 TITLE-PIN REPAIR (the bare panel had lost the r334 `<h3>` pin — 114 panels at h5; `activityTitleLevelPostpass` reaches the bare "
            "box now); probe OFF = disk + the 20 repaired pages, ON 30 pages / 5 modules (30 up / 0 down, +147.9pp-sum); SCOPED regeneration of the 5 (scoped ship #2 since "
            "the r416 FULL); **skeleton 54.123 → 54.186 % (+0.0630pp), ≥50 1438 → 1439, ≥75 238, ≥90 20, RAW 38.204 % @ 2349 pairs**; cs 14168 / 186 / 683 / 23, body 54 / 5 "
            "/ 190 / 247, clean 2504 / 2548, leak 73 / 44 — all EXACT; every verifier EXACT; 16 selftests GREEN; the miner 182 → 183); before it **r417** (build 260619.88, "
            "20 Sept ≈21:40, session 29 Round 8 — the XDLS choice-page panel holds its content directly, `CDPANELROW_OFF`, 30 up / 0 down, +0.1947pp, ≥50 +23), **r416** "
            "(build 260619.87, the activity title typed inside the red span, `EMBTITLE_OFF`, +0.0174pp; THE FULL REGENERATION of all 494 — the ledger's backstop, counter 0), "
            "**r415** (build 260619.86, the owned heading-led bundle with no table, `NOTABLEOWNED_OFF`, +0.0246pp), **r414** (build 260619.85, the nested activity box, "
            "`NESTBOX_OFF`, +0.0696pp), **r413** (build 260619.84, `HEADTABLEOWNED_OFF`, +0.0080pp), **r412** (build 260619.83, `HEADTABLE_OFF`, +0.0139pp), **r411** "
            "(build 260619.82, `TILEMENUROW_OFF`, +0.0058pp) and **r410** (build 260619.81, the WJFUN tile-page dialect, `TILEPAGE_OFF`, 53.680 → 53.789 %). **Corpus = r418** "
            "(2555 pages / 494 dirs / 2349 pairs; `gate_baseline.json` at r418; `outputs/_s29_r418_sk_final.json` the skeleton state; ceiling 90.9 % → 54.186 = **59.6 % of "
            "achievable**).")
q = idx("- Plateau window (§4): **0 of 3**")
lines[q] = "- Plateau window (§4): **0 of 3** — r418 +0.0630pp (≥50 +1), r417 +0.1947pp (≥50 +23) after r416's +0.0174 (the one sub-0.02 round). Read every delta on the post-intake 2,349-pair population (§1e)."
r = idx("- Standing facts: AppVersion 260619.88")
lines[r] = lines[r].replace("AppVersion 260619.88 (r417, session 29 Round 8, 20 Sept); before it 260619.87 (r416)", "AppVersion 260619.89 (r418, session 29 Round 9, 20 Sept); before it 260619.88 (r417) / 260619.87 (r416)")
assert "260619.89" in lines[r]
t = idx("- s29-r8 (engine r417")
lines.insert(t + 1, "- s29-r9 (engine r418, build 260619.89, 20 Sept ≈21:45 → 22:05) · THE FIRST TILE PANEL TAKES THE `row.clickDropContent.noBorder` FORM — the gold's first tile panel on every choice page is `row clickDropContent noBorder > col-12 col-md-8 > activity dropbox` (the token on the section ROW — the JS's first `.clickDropContent` shows open; the later panels keep it on the box), 35 / 35 pages of XDLS902–906 (`_s29_r9_panelforms.py`; XDLS902 lessons 2–7 all-row = the module's own, not taken) · `tile_grid.first_panel_row {enabled, env CDFIRSTROW_OFF}` in `ContentConverter.#cdTilePair` (the first panel's section row takes the class, the box keeps its own; any other shape keeps the prefix) · + THE r417 TITLE-PIN REPAIR: the bare panel had lost the r334 `<h3>` pin (`titleRe` read the inner row / col — 114 of 179 panels shipped h5; the gates did not flag it, the row / col removal outweighed it) — the inner group is optional now, repaired not reverted (r293b), untoggled · SHIPPED · probe OFF = disk + the 20 repaired pages, ON 30 pages / 5 modules (30 up / 0 down, +147.9pp-sum) · SCOPED regeneration of the 5 + 12 spot-checks (scoped ship #2 since the r416 FULL) · skeleton 54.123 → 54.186 (+0.0630pp; 30 movers, 0 outside the set), ≥50 1438 → 1439, ≥75 238, ≥90 20, RAW 38.204; every other gate EXACT · miner 182 → 183 (#1036 gone; the per-panel upload button and XDLS902's all-row form surfaced) · plateau 0 of 3 · DECLINED, recorded: #1035 the per-panel `Upload to dropbox` button (Claude one per writer marker; the gold's ONE per page = an INVENTED box `2G Share your learning!` with prose in no WT; XDLS909's gold keeps the per-panel form — class C)")
# ---- §5d condense: the s21–s26 Round-log lines → the archive (LOOP_STATE.md crossed 100 KB at the Round 9 PICK)
s21 = idx("- s21-r1 (engine r364"); s27 = idx("- s27-r1")
moved = lines[s21:s27]
assert all(l.startswith("- s2") for l in moved) and 30 <= len(moved) <= 45, len(moved)
lines[s21:s27] = ["- s21–s26 round-log lines (37 rounds, sessions 21–26: engine r364–r397 + the s25 loss ledger / s26 r398 PICK pass) → LOOP_STATE_ARCHIVE.md 'Round-log lines s21–s26 (archived from LOOP_STATE.md 2026-09-20 ≈22:05 NZST, session 29 §5d condense)' — grep the engine number there; every verdict stands."]
io.open(STATE, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
with io.open(ARCH, "a", encoding="utf-8", newline="\n") as f:
    f.write("\n## Session 29 — Round 9 PICK (engine r418) + what shipped — THE FIRST TILE PANEL TAKES THE row.clickDropContent.noBorder FORM + the r417 title-pin repair (20 Sept ≈21:45 → 22:05 NZST)\n\n" + "\n".join(pick).rstrip("\n") + "\n" + shipped + "\n")
    f.write("\n## Round-log lines s21–s26 (archived from LOOP_STATE.md 2026-09-20 ≈22:05 NZST, session 29 §5d condense)\n\n" + "\n".join(moved) + "\n")
print("LOOP_STATE.md", os.path.getsize(STATE), "bytes; archive", os.path.getsize(ARCH), "; moved", len(moved))
