#!/usr/bin/env python3
"""Round 8 PICK → LOOP_STATE.md (inserted before '## Round log'). Run under WSL."""
import io, os
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
STATE = R + "LOOP_STATE.md"
lines = io.open(STATE, encoding="utf-8").read().split("\n")
b = next(i for i, l in enumerate(lines) if l.startswith("## Round log"))
pick = [
"## Session 29 — Round 8 PICK (engine r417) — THE XDLS CHOICE-PAGE PANEL HOLDS ITS CONTENT DIRECTLY: the r307 `clickDropContent activity dropbox` panel without the inner `row > col-12` (20 Sept ≈21:15 → in progress; scoped ship #1 since the r416 FULL)",
"- **Class.** The r307 tile-grid PANEL — the `[Activity] **2A**` anchor the choice-page tile reveals — is opened through the standard `activity_wrapper.open` (`<div class=\"activity…\" number=\"2A\"><div class=\"row\"><div class=\"col-12\">`), so every panel carries an inner `row > col-12`; the gold's `<div class=\"clickDropContent activity dropbox\" number=\"2A\">` holds its `<h3>` / `<p>` / video DIRECTLY (XDLS903.02 L120–145 vs Claude XDLS903_2_0 L132–172). Each panel = 2 extra skeleton lines (`div.row`, `div.col-12`) on the family's every lesson page.",
"- **Measured** (`_s29_r8_boxcol.py` — the activity box's first col class gold vs Claude, per subject|template and family; `_s29_r8_xdlsrow.py` — per module): the ONE real difference in the whole census is the XDLS family (`(Inquiry, Leaving to Learn)` plain boxes gold `(no row>col)` 0.69 of 84; XDLS family 0.69 of 341 — every other group's gold is `col-12` ≥ 0.55 and Claude's col-12 right); decomposed: the gold's `clickDropContent activity` panels hold content directly on 144 / 145 (XDLS902 5 / 5, 903 35 / 35, 904 34 / 35, 905 34 / 34, 906 35 / 35, 909 21 / 22), while Claude wraps ALL 179 panels (902 41, 903 36, 904 36, 905 36, 906 30) on 35 pages / 5 modules; the family's PLAIN boxes are a 7 / 7 tie (not the class); the gold's minority `row.clickDropContent.noBorder > col-12.col-md-8 > activity.dropbox` form (XDLS902 37, one page each on 903–906) is a different wrapper either way. Claude has no panels on XDLS909 (the r307 decline). Floor: 35 pages ≥ 20 ✓; NEW-FAMILY: an intake-free class (the r307 XDLS90x family, all pre-intake).",
"- **Authority:** §1b (2) — the gold's own panel form (the r307 tile grid's panels, 144 / 145); the r307 pairing post-pass reads only the opening tag, so the bare form pairs unchanged.",
"- **Fix (planned):** `interactive_builders.clickDrop.tile_grid.panel_no_inner_row {enabled, env CDPANELROW_OFF}` + `activity_wrapper.open_bare` / `close_bare` (`<div class=\"activity{modifiers}\"{numberAttr}>` / `</div>`): in `ActivitiesBuilder.activityOpen`, a `_r307PanelId`-tagged opener on the standard (non-supervisor-note) path emits the bare open and pushes the bare close; every other box byte-identical. Probe OFF must equal disk 2555 / 2555; ON expected ≈ 35 pages / 5 modules; scored with the gate's own `match()` before regenerating; SCOPED regeneration of the 5 + a 12-module spot-check.",
"- **Not taken, recorded (measured this PICK pass):** DIFF_QUEUE #4 (title MISSING h1, 246 pages) = the gold's Te Reo lesson titles in NO WT (class C, the r198 record); GENO901 (16 `[Hintslider front/back]` leaks on one page) and DTC1005 (14 black-typed tags in one section) = single-module cases under the chrome floor; #32 / #33 / #34 module-menu rows = rewritten menu text / pairing artefacts; #589 (MISSING inner row in activity.interactive, MiW 0.91) — the WJFUN gold box col is `col-12` on 0.73, Claude already right; the XDLS plain-box `(no row>col)` 0.69 = the panel class above once decomposed.",
"",
]
lines[b:b] = pick
io.open(STATE, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("LOOP_STATE.md", os.path.getsize(STATE), "bytes")
