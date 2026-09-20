#!/usr/bin/env python3
"""r417 finalise (CLAUDE.md §12): changelog entry, Config.js bump, CLAUDE.md §9 / §11 / §14, gate_baseline.json. Run under WSL."""
import re, json
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
PF = R + "pageforge-site/converter-v2/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

entry = """## 2026-09-20 (round 417, build 260619.88) — THE XDLS CHOICE-PAGE PANEL HOLDS ITS CONTENT DIRECTLY: the r307 `clickDropContent activity dropbox` panel without the inner `row > col-12` (the autonomous loop's session 29 Round 8; SCOPED regeneration of the 5 XDLS modules — scoped ship #1 since the r416 FULL; every protected gate HELD-or-IMPROVED: skeleton 53.928 → 54.123 % (+0.1947pp), ≥50 1415 → 1438)

### 1. WHAT CHANGED

**The class.** The r307 tile-grid PANEL — the `[Activity] **2A**` anchor a choice-page tile reveals, tagged `_r307PanelId` by `ContentConverter.#cdTilePrepass` — opened through the standard `activity_wrapper.open` (`<div class="activity…" number="2A"><div class="row"><div class="col-12">`), so every panel carried an inner `row > col-12`; the gold's `<div class="clickDropContent activity dropbox" number="2A">` holds its `<h3>` / `<p>` / video DIRECTLY (XDLS903.02 L120–145 vs Claude XDLS903_2_0 L132–172). Each panel = 2 extra skeleton lines (`div.row`, `div.col-12`) on every lesson page of the family.

**Measured** (`outputs/_s29_r8_boxcol.py` — the activity box's first col class gold vs Claude, per subject|template and per family; `_s29_r8_xdlsrow.py` per module): the ONE real difference in the whole census is the XDLS family — `(Inquiry, Leaving to Learn)` plain boxes gold `(no row>col)` 0.69 of 84, the XDLS family 0.69 of 341; every other group's gold is `col-12` ≥ 0.55 with Claude's col-12 already right. Decomposed: the gold's `clickDropContent activity` panels hold their content directly on **144 / 145** (XDLS902 5 / 5, 903 35 / 35, 904 34 / 35, 905 34 / 34, 906 35 / 35, 909 21 / 22) while Claude wrapped ALL 179 panels (902 41, 903 36, 904 36, 905 36, 906 30); the family's PLAIN boxes are a 7 / 7 tie (not the class); the gold's minority `row.clickDropContent.noBorder > col-12.col-md-8 > activity.dropbox` form (XDLS902 37, one page each on 903–906) is a different wrapper either way. Claude ships no panels on XDLS909 (the r307 decline). An intake-free class (the r307 XDLS90x family, all pre-intake).

**The fix (DATA OVER CODE).** `interactive_builders.clickDrop.tile_grid.panel_no_inner_row {enabled, env CDPANELROW_OFF}` + `activity_wrapper.open_bare` / `close_bare` (`<div class="activity{modifiers}"{numberAttr}>` / `</div>`): in `ActivitiesBuilder.activityOpen` a `_r307PanelId`-tagged opener on the standard (non-supervisor-note) path emits the bare open and pushes the bare close; the supervisor-note box keeps its own two-child structure; every other box is byte-identical. The r307 pairing post-pass (`#cdTilePair`) and the r305 dropbox post-pass read only the opening tag / a balanced div span, so `clickDropContent ` and `dropbox` land unchanged. OFF (`CDPANELROW_OFF` or `enabled:false`) = the r416 output byte-for-byte.

### 2. PROOF

- `_s29_r417_probe_run.sh` (the r410 harness over all 494 Claude-dir modules, 4 shards): **OFF (`CDPANELROW_OFF`) = disk 2555 / 2555**; **ON = 30 pages / 5 modules** (XDLS902 / 903 / 904 / 905 / 906 — `_affected_r417.txt`); the diff on every ON page is exactly the `<div class="row"><div class="col-12">` … `</div></div>` pair leaving each panel.
- `_s29_r417_pagescore.py` (the gate's own `match()` on the probe's ON pages BEFORE regenerating): **30 paired pages, 30 up / 0 down, SCAFFOLD pp-sum +457.4 (mean +15.25pp per page), RAW +332.4** — XDLS903_7_0 +27.1, XDLS904_4_0 +24.6, XDLS903_6_0 +24.5; the smallest XDLS902_4_0 +2.6 (the gold's row-form page).
- SCOPED regeneration (`_s29_r417_regen.sh`: the 5 + the 12-module spot-check sample, 3 `_regen_safe.sh` batches, all rc 0): `_content_manifest.py fresh` **0 truly stale** (5 affected regenerated, 486 unaffected byte-identical); `_scoped_spotcheck.py verify` **12 / 12 byte-identical under the fix**.
- `scoped_ship.sh --affected _affected_r417.txt --toggle CDPANELROW_OFF --no-regen --commit --round 417` (`_s29_r417_scoped_ship.log`): toggle present, containment **5 changed ⊆ 5 affected**, the exact decomposition gate proof — skeleton 53.93 → 54.12 IMPROVED, ≥50 1415 → 1438 IMPROVED, every other row HELD; the fast-loop baseline PATCHED (2349 pages), the content manifest refreshed, the ledger **scoped #1 since the r416 FULL** (7 of headroom).
- `run_all_gates.sh` (`_s29_r417_gates.log`): every row HELD-or-IMPROVED; every verifier RESULT ✓ identical to r416 (flipCard divergence 0, speechBubble ✓, modal 13 groups defect 0, mtkQuiz 17 shells ✓, math 323 / 323, menulabels 99 ✓, dragAndDrop 21 ✓); entry parity PASS; index-sync 33 / 28. `_gatecheck.py` refuses on the mtime staleness of the 489 untouched modules (the r302 class — `_content_manifest.py fresh` is the authority, 0 truly stale).
- `_s29_skdelta.py _s29_r416_sk_final.json _s29_r417_sk_final.json --affected _affected_r417.txt`: **30 movers, 30 up / 0 down, 0 outside the affected set; 0 pages added / gone**.
- 16 selftests GREEN (46 PASS / GREEN lines, 0 FAIL); feature index `--rehtml` / `--merge` / `--selftest` GREEN.
- DIFF MINER re-mined on the r417 corpus (`_diff_miner_s29_r417.log`): **181 → 182 CANDIDATE rows** — two new XDLS-family rows surfaced by the panel's inner lines leaving: #1035 `activity EXTRA … › a` (23 pages / 4 modules — the r308 per-`[dropbox]` upload button, one per panel where the gold consolidates to one per page; the XDLS501 over-emit named at r308) and #1036 `activity SUBSTITUTED div.col-12.col-md-8 › activity.dropbox` (21 pages / 4 modules — the gold's minority `row.clickDropContent.noBorder` wrapper form); both recorded for the next PICK pass. The pre-round queue is `_diff_queue_pre_r417.md`.

### 3. PROTECTED GATES (all HELD-or-IMPROVED — `_s29_r417_gates.log`, `_s29_r417_scoped_ship.log`)

- **Skeleton (PRIMARY)**: SCAFFOLD **53.928 → 54.123 % (+0.1947pp)**; ≥50 **1415 → 1438 (+23)**, ≥75 **238**, ≥90 **20** EXACT; RAW **38.000 → 38.142 %**; 2349 pairs, skipped 0 (state `outputs/_s29_r417_sk_final.json`).
- **compare_structure** exact **14168** / EXTRA **186** / MISSING **683** / row-wrap **23** EXACT; **body_compare** 54 / 5 / 190 / 247 EXACT; **defect** clean 2504 / 2548 = 98.27 %, leak 73 / 44 EXACT; tags **9557 / 9557**.
- Plateau (§4): **+0.1947pp — the window RESETS (0 of 3)**.

### 4. RECORDED, NOT TAKEN (the Round 8 PICK pass — `LOOP_STATE.md`)

- DIFF_QUEUE #4 (title MISSING h1, 246 pages) = the gold's Te Reo lesson titles in NO WT (class C, the r198 record); GENO901 (16 `[Hintslider front/back]` leaks on one page) and DTC1005 (14 black-typed tags in one section) = single-module cases under the chrome floor; #32 / #33 / #34 module-menu rows = rewritten menu text / pairing artefacts; #589 (MISSING inner row in `activity.interactive`, MiW 0.91) — the WJFUN gold box col is `col-12` on 0.73, Claude already right.
- The XDLS family's two new miner rows above (the per-panel upload button 23 / 4; the `row.clickDropContent.noBorder` wrapper 21 / 4) — the next PICK pass's candidates.

"""
p = PF + "BUILD_CHANGELOG.md"; s = rd(p)
head, rest = s.split("\n", 1)
assert head.startswith("# BUILD CHANGELOG") and rest.lstrip("\n").startswith("## 2026-09-20 (round 416")
wr(p, head + "\n\n" + entry + rest.lstrip("\n"))

p = PF + "app/js/Config.js"; s = rd(p)
old = '\tstatic AppVersion = "260619.87";'; assert s.count(old) == 1
note = ("\t// ROUND 417 (260619.88): THE XDLS CHOICE-PAGE PANEL HOLDS ITS CONTENT DIRECTLY — the r307 tile-grid panel (`[Activity] **2A**`, tagged _r307PanelId) "
        "opened through the standard activity_wrapper.open, so every panel carried an inner row > col-12; the gold's clickDropContent activity dropbox panel holds its "
        "h3 / p / video directly (144 / 145 on XDLS902-906 + 909). `tile_grid.panel_no_inner_row` + `activity_wrapper.open_bare / close_bare`, env CDPANELROW_OFF; "
        "ActivitiesBuilder.activityOpen emits the bare form for a panel anchor on the standard path. The loop's session 29 Round 8: OFF = disk 2555 / 2555, ON 30 pages / "
        "5 modules (30 up / 0 down, +457.4pp-sum); SCOPED regeneration of the 5 (scoped #1 since the r416 FULL); skeleton 53.928 -> 54.123 % (+0.1947pp), >=50 1415 -> 1438, "
        "every other gate EXACT; miner 181 -> 182 (two XDLS rows surfaced).\n")
wr(p, s.replace(old, note + '\tstatic AppVersion = "260619.88";'))

p = PF + "CLAUDE.md"; s = rd(p)
old9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 416 BASELINE ("; assert s.count(old9) == 1
new9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 417 BASELINE (the XDLS choice-page panel holds its content directly — the r307 "
        "`clickDropContent activity dropbox` panel without the inner `row > col-12`; `tile_grid.panel_no_inner_row` + `activity_wrapper.open_bare / close_bare`, env "
        "`CDPANELROW_OFF`; 5 modules / 30 pages; SCOPED regeneration of the 5, the probe proving the other 489 byte-identical; scoped ship #1 since the r416 FULL): "
        "SCAFFOLD mean 54.123% / >=50% 1438 / >=75% 238 / >=90% 20 / RAW 38.142% @ 2349 pairs, pairs skipped 0 — hold-or-improve; 30 movers (30 up, 0 down — "
        "XDLS903_7_0 +27.1, XDLS904_4_0 +24.6; 0 outside the affected set); the 2319 unaffected pairs EXACT. compare_structure 14168 / 186 / 683 / 23 EXACT; "
        "body_compare 54 / 5 / 190 / 247 EXACT; defect clean 2504 / 2548 = 98.27%, leak 73 / 44 EXACT.** Previous — ROUND 416 BASELINE (")
s = s.replace(old9, new9)
old11 = "| `EMBTITLE_OFF` | 416 | **THE ACTIVITY TITLE TYPED INSIDE THE RED SPAN"; assert s.count(old11) == 1
row11 = ("| `CDPANELROW_OFF` | 417 | **THE XDLS CHOICE-PAGE PANEL HOLDS ITS CONTENT DIRECTLY — the r307 `clickDropContent activity dropbox` panel without the inner "
         "`row > col-12`** (the autonomous loop's session 29 Round 8). The r307 tile-grid PANEL — the `[Activity] **2A**` anchor a choice-page tile reveals, tagged "
         "`_r307PanelId` by `ContentConverter.#cdTilePrepass` — opened through the standard `activity_wrapper.open`, so every panel carried an inner `row > col-12`; the "
         "gold's `<div class=\"clickDropContent activity dropbox\" number=\"2A\">` holds its `<h3>` / `<p>` / video DIRECTLY. Measured (`_s29_r8_boxcol.py` — the activity "
         "box's first col class gold vs Claude per subject|template and family — the ONE real difference in the whole census; `_s29_r8_xdlsrow.py` per module): the gold's "
         "panels hold content directly on 144 / 145 (XDLS902 5 / 5, 903 35 / 35, 904 34 / 35, 905 34 / 34, 906 35 / 35, 909 21 / 22), Claude wrapped all 179 on 30 pages / "
         "5 modules; the family's plain boxes a 7 / 7 tie (not taken); the gold's minority `row.clickDropContent.noBorder > col-12.col-md-8 > activity.dropbox` form "
         "(XDLS902 37) a different wrapper either way (recorded). Data `interactive_builders.clickDrop.tile_grid.panel_no_inner_row {enabled, env}` + `activity_wrapper"
         ".open_bare / close_bare`: `ActivitiesBuilder.activityOpen` emits the bare open and pushes the bare close for a panel anchor on the standard (non-supervisor-note) "
         "path; the r307 pairing and r305 dropbox post-passes read only the opening tag / a balanced div span, so the class tokens land unchanged. OFF = the r416 output "
         "byte-for-byte (2555 / 2555). ON = 30 pages / 5 modules, 30 up / 0 down (+457.4pp-sum). |\n")
s = s.replace(old11, row11 + old11)
old14 = "- **Build:** `260619.87` (round 416 — **the activity title typed inside the red span"; assert s.count(old14) == 1
b14 = ("- **Build:** `260619.88` (round 417 — **the XDLS choice-page panel holds its content directly: the r307 `clickDropContent activity dropbox` panel without the "
       "inner `row > col-12` — the gold's panel opens straight onto its `<h3>` / `<p>` / video on 144 / 145, Claude wrapped all 179** (`tile_grid.panel_no_inner_row` + "
       "`activity_wrapper.open_bare / close_bare`, env `CDPANELROW_OFF`; `ActivitiesBuilder.activityOpen`); the autonomous loop's session 29 Round 8 — found by the "
       "activity-box column census (`_s29_r8_boxcol.py`); the probe OFF = disk 2555 / 2555, ON 30 pages / 5 modules (30 up / 0 down, +457.4pp-sum, 0 outside the set); "
       "**SCOPED regeneration of the 5 (scoped ship #1 since the r416 FULL)**; **ROUND 417 BASELINE: SCAFFOLD mean 54.123% / >=50% 1438 / >=75% 238 / >=90% 20 / RAW "
       "38.142% @ 2349 pairs** (+0.1947pp; ≥50 +23); compare_structure 14168 / 186 / 683 / 23, body 54 / 5 / 190 / 247, clean 2504 / 2548, leak 73 / 44 — all EXACT; every "
       "verifier EXACT; 16 selftests GREEN; the miner 181 → 182 (the two XDLS rows the panel's inner lines uncovered — the per-panel upload button, the `noBorder` row "
       "wrapper); plateau window RESET (0 of 3)). Previous: ")
s = s.replace(old14, b14 + old14)
wr(p, s)

p = R + "CONVERTER_V2/reference/tests/gate_baseline.json"; s = rd(p)
def setv(key, old, new):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=1); assert n == 1, key
setv("build", '"260619.87"', '"260619.88"'); setv("round", 416, 417)
setv("mean_scaffold_pct", 53.93, 54.12); setv("median_scaffold_pct", 54.9, 55.2); setv("pages_ge_50", 1415, 1438); setv("raw_mean_pct", 38.0, 38.1)
a = '    "_note_r416": "Round 416 (session 29 Round 7)'; assert s.count(a) == 1
s = s.replace(a, '    "_note_r417": "Round 417 (session 29 Round 8): the XDLS choice-page panel holds its content directly — the r307 clickDropContent activity dropbox panel without the inner row > col-12 (tile_grid.panel_no_inner_row + activity_wrapper.open_bare / close_bare, env CDPANELROW_OFF; 5 modules / 30 pages; SCOPED regeneration of the 5, scoped #1 since the r416 FULL; skeleton 53.9284 -> 54.1231, >=50 1415 -> 1438, RAW 38.000 -> 38.142; every other gate EXACT).",\n' + a)
a2 = '    "_note_r415b": "Round 416: SCAFFOLD 53.9110'; assert s.count(a2) == 1
s = s.replace(a2, '    "_note_r416b": "Round 417: SCAFFOLD 53.9284 -> 54.1231 (+0.1947pp; 30 movers, 30 up / 0 down — XDLS903_7_0 +27.1, XDLS904_4_0 +24.6, XDLS903_6_0 +24.5; 0 outside the 5-module affected set), 1438 / 238 / 20, RAW 38.142; 2349 pairs. Plateau window RESET (0 of 3).",\n' + a2)
b2 = '    "_note_r416": "Round 416: 14168 / 186 / 683 / 23 EXACT'; assert s.count(b2) == 1
s = s.replace(b2, '    "_note_r417": "Round 417: 14168 / 186 / 683 / 23 EXACT (a wrapper the comparator does not text-match).",\n' + b2)
b3 = '    "_note_r416": "Round 416: over-capture 54 / runaway 5'; assert s.count(b3) == 1
s = s.replace(b3, '    "_note_r417": "Round 417: over-capture 54 / runaway 5 / EMPTY 190 / ANY 247 EXACT.",\n' + b3)
wr(p, s); json.load(open(p, encoding="utf-8"))
print("r417 finalise: changelog + Config.js 260619.88 + CLAUDE.md §9/§11/§14 + gate_baseline.json done")
