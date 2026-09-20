#!/usr/bin/env python3
"""r418 finalise (CLAUDE.md §12): changelog entry, Config.js bump, CLAUDE.md §9 / §11 / §14, gate_baseline.json. Run under WSL."""
import re, json
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
PF = R + "pageforge-site/converter-v2/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

entry = """## 2026-09-20 (round 418, build 260619.89) — THE FIRST TILE PANEL TAKES THE `row.clickDropContent.noBorder` FORM + THE r417 TITLE-PIN REPAIR (the autonomous loop's session 29 Round 9; SCOPED regeneration of the 5 XDLS modules — scoped ship #2 since the r416 FULL; every protected gate HELD-or-IMPROVED: skeleton 54.123 → 54.186 % (+0.0630pp), ≥50 1438 → 1439)

### 1. WHAT CHANGED

**(a) The r417 defect, repaired.** The r417 bare panel LOST the r334 title pin: `ActivitiesBuilder.activityTitleLevelPostpass`'s `titleRe` read `<div class="row"><div class="col-12"><h…` after the box open, so a bare panel's first heading stayed at the relevel level — **114 of the 179 panels shipped `<h5>`** where the gold (and the r416 disk) has `<h3>` (XDLS903 14 / 36, 904 36 / 36, 905 35 / 35, 906 29 / 29; XDLS902's writer typed `[H3]`). The gates did not flag it (the row / col removal outweighed it: 30 up / 0 down). Repaired, not reverted (the r293b rule): the inner `row > col-12` group of `titleRe` is OPTIONAL — a box with the inner row / col matches exactly as before (byte-identical everywhere else by construction: no other box opens straight onto a heading).

**(b) The class.** The gold's FIRST tile panel on every choice page is the ROW form — `<div class="row clickDropContent noBorder"><div class="col-12 col-md-8"><div class="activity dropbox" number="2A">` — the `clickDropContent` token on the section ROW (the site JS's first `.clickDropContent` shows open, without a border), the box itself without it; the later panels keep `clickDropContent activity dropbox` on the box. Claude put the token on every box and left the section row plain.

**Measured** (`outputs/_s29_r9_panelforms.py` → `_s29_r9_panelforms.out`, every paired page of XDLS902–906 + 909): the first panel is the row form on **35 / 35** pages of 902–906 (XDLS902 lessons 2–7 carry ALL six panels in the row form — the module's own extension, not taken; lesson 1 first-only; 903–906 7 / 7 each first-only); the row class `row clickDropContent noBorder` 65 / 65, the col `col-12 col-md-8` 64 / 65, the box `activity dropbox` 65 / 65. XDLS909 (no tile grid in Claude) all direct.

**The fix (DATA OVER CODE).** `interactive_builders.clickDrop.tile_grid.first_panel_row {enabled, env CDFIRSTROW_OFF, row_open, col_open_pattern, row_class_open}`: in `ContentConverter.#cdTilePair` the first panel id's box keeps its own class and the section row directly wrapping it (`<div class="row">` + `<div class="col-md-8 col-12">`, nothing else between — the r51 section row) takes `row clickDropContent noBorder`; any other shape keeps the prefix form (never half-applied). OFF = the prefix on every panel (the r417 output).

**Also measured, DECLINED (record):** DIFF_QUEUE #1035 — the per-panel `Upload to dropbox` button (Claude 157 buttons on 39 pages, one per writer `[3 buttons – film, camera and microphone] Upload to dropbox` marker at the end of EVERY panel) vs the gold's ONE per page on 35 / 35 pages of 902–906: the gold's developer consolidated them into an INVENTED extra box (`activity dropbox` number 2G `Share your learning!` + prose in NO WT) after the panels; XDLS909's gold keeps the per-panel form (6 / 6 per page). An A1 substitution with invented text — class C; the writer's per-panel button stands.

### 2. PROOF

- `_s29_r418_probe_run.sh` (the r410 harness over all 494 Claude-dir modules, 4 shards): **OFF (`CDFIRSTROW_OFF`) = the disk except 20 pages / 4 modules** — exactly the pin repair (the `<h5>` → `<h3>` title lines on the bare panels; XDLS902's are h3 already), the r417 defect it fixes; **ON = 30 pages / 5 modules**, every changed line one of three kinds: 114 `<h5>` → `<h3>` panel titles, 30 section rows → `row clickDropContent noBorder`, 30 first-panel boxes losing the `clickDropContent ` prefix.
- `_s29_r418_pagescore.py` (the gate's own `match()` BEFORE regenerating): **30 paired pages, 30 up / 0 down, SCAFFOLD pp-sum +147.9 (mean +4.93pp), RAW +146.4** — XDLS904_2_0 +16.1, XDLS905_5_0 +8.1, XDLS903_2_0 +7.7; XDLS902's seven pages +1.0 each (the row form alone).
- SCOPED regeneration (`_s29_r418_regen.sh`: the 5 + a fresh 12-module spot-check sample, 3 batches rc 0): `_content_manifest.py fresh` **0 truly stale**; `_scoped_spotcheck.py verify` **12 / 12 byte-identical under the fix**.
- `scoped_ship.sh --affected _affected_r418.txt --toggle CDFIRSTROW_OFF --no-regen --commit --round 418` (`_s29_r418_scoped_ship.log`): containment **5 ⊆ 5**, the decomposition gate proof — skeleton 54.12 → 54.19 IMPROVED, ≥50 1438 → 1439 IMPROVED, every other row HELD; the fast-loop baseline PATCHED, the manifest refreshed, the ledger **scoped #2 since the r416 FULL** (6 of headroom).
- `run_all_gates.sh` (`_s29_r418_gates.log`): every row HELD-or-IMPROVED; every verifier RESULT ✓ identical to r417; entry parity PASS; index-sync 33 / 28. `_gatecheck.py` refuses on the mtime staleness of the untouched modules (the r302 class; `fresh` is the authority).
- `_s29_skdelta.py _s29_r417_sk_final.json _s29_r418_sk_final.json --affected _affected_r418.txt`: **30 movers, 30 up / 0 down, 0 outside the affected set; 0 pages added / gone**.
- 16 selftests GREEN (46 / 0); feature index GREEN; DIFF MINER **182 → 183 CANDIDATE rows** — #1036 (the SUBSTITUTED first-panel row) GONE; two XDLS rows surfaced: `activity EXTRA div.activity.dropbox › a` (the per-panel upload button, now on the first panel's own form — the declined #1035 class) and `activity MISSING div.col-12.col-md-8 › div.activity.dropbox` (XDLS902 lessons 2–7's all-row form — the module's own, 6 pages). The pre-round queue is `_diff_queue_pre_r418.md`.

### 3. PROTECTED GATES (all HELD-or-IMPROVED — `_s29_r418_gates.log`, `_s29_r418_scoped_ship.log`)

- **Skeleton (PRIMARY)**: SCAFFOLD **54.123 → 54.186 % (+0.0630pp)**; ≥50 **1438 → 1439**, ≥75 **238**, ≥90 **20** EXACT; RAW **38.142 → 38.204 %**; 2349 pairs, skipped 0 (state `outputs/_s29_r418_sk_final.json`).
- **compare_structure** exact **14168** / EXTRA **186** / MISSING **683** / row-wrap **23** EXACT; **body_compare** 54 / 5 / 190 / 247 EXACT; **defect** clean 2504 / 2548 = 98.27 %, leak 73 / 44 EXACT; tags **9557 / 9557**.
- Plateau (§4): **+0.0630pp with ≥50 +1 — the window stays at 0 of 3**.

"""
p = PF + "BUILD_CHANGELOG.md"; s = rd(p)
head, rest = s.split("\n", 1)
assert head.startswith("# BUILD CHANGELOG") and rest.lstrip("\n").startswith("## 2026-09-20 (round 417")
wr(p, head + "\n\n" + entry + rest.lstrip("\n"))

p = PF + "app/js/Config.js"; s = rd(p)
old = '\tstatic AppVersion = "260619.88";'; assert s.count(old) == 1
note = ("\t// ROUND 418 (260619.89): THE FIRST TILE PANEL TAKES THE ROW FORM + THE r417 TITLE-PIN REPAIR — the gold's first tile panel on every choice page is "
        "`row clickDropContent noBorder > col-12 col-md-8 > activity dropbox` (the clickDropContent token on the section row, 35 / 35 pages of XDLS902-906); "
        "`tile_grid.first_panel_row`, env CDFIRSTROW_OFF, in ContentConverter.#cdTilePair. And r417's bare panel had lost the r334 title pin (114 panels at h5): "
        "activityTitleLevelPostpass's inner row / col is optional now — repaired, not reverted. The loop's session 29 Round 9: OFF = disk + the 20 repaired pages, "
        "ON 30 pages / 5 modules (30 up / 0 down, +147.9pp-sum); SCOPED regeneration of the 5 (scoped #2 since the r416 FULL); skeleton 54.123 -> 54.186 % "
        "(+0.0630pp), >=50 1438 -> 1439, every other gate EXACT; miner 182 -> 183.\n")
wr(p, s.replace(old, note + '\tstatic AppVersion = "260619.89";'))

p = PF + "CLAUDE.md"; s = rd(p)
old9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 417 BASELINE ("; assert s.count(old9) == 1
new9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 418 BASELINE (the first tile panel takes the `row.clickDropContent.noBorder` form + "
        "the r417 title-pin repair — `tile_grid.first_panel_row`, env `CDFIRSTROW_OFF`; `activityTitleLevelPostpass` reaches the bare box; 5 modules / 30 pages; "
        "SCOPED regeneration of the 5, the probe proving the other 489 byte-identical; scoped ship #2 since the r416 FULL): SCAFFOLD mean 54.186% / >=50% 1439 / "
        ">=75% 238 / >=90% 20 / RAW 38.204% @ 2349 pairs, pairs skipped 0 — hold-or-improve; 30 movers (30 up, 0 down — XDLS904_2_0 +16.1; 0 outside the affected "
        "set); the 2319 unaffected pairs EXACT. compare_structure 14168 / 186 / 683 / 23 EXACT; body_compare 54 / 5 / 190 / 247 EXACT; defect clean 2504 / 2548 = "
        "98.27%, leak 73 / 44 EXACT.** Previous — ROUND 417 BASELINE (")
s = s.replace(old9, new9)
old11 = "| `CDPANELROW_OFF` | 417 | **THE XDLS CHOICE-PAGE PANEL HOLDS ITS CONTENT DIRECTLY"; assert s.count(old11) == 1
row11 = ("| `CDFIRSTROW_OFF` | 418 | **THE FIRST TILE PANEL TAKES THE `row.clickDropContent.noBorder` FORM + THE r417 TITLE-PIN REPAIR** (the autonomous loop's "
         "session 29 Round 9). (a) The r417 bare panel had LOST the r334 title pin — `activityTitleLevelPostpass`'s `titleRe` read the inner `row > col-12` before the "
         "heading, so 114 of the 179 panels shipped `<h5>` where the gold has `<h3>`; the inner group is OPTIONAL now (a box with the inner row / col matches exactly as "
         "before) — repaired, not reverted, untoggled (it is r417's own defect). (b) The gold's FIRST tile panel on every choice page is `<div class=\"row clickDropContent "
         "noBorder\"><div class=\"col-12 col-md-8\"><div class=\"activity dropbox\" number=\"2A\">` — the token on the section ROW (the JS's first `.clickDropContent` "
         "shows open, `noBorder`), the box without it; the later panels keep the token on the box. Measured (`_s29_r9_panelforms.py`): 35 / 35 pages of XDLS902–906 "
         "(XDLS902 lessons 2–7 carry every panel in the row form — the module's own extension, not taken). Data `tile_grid.first_panel_row {enabled, env, row_open, "
         "col_open_pattern, row_class_open}`: in `ContentConverter.#cdTilePair` the first panel id's box keeps its own class and the section row directly wrapping it "
         "(the r51 `<div class=\"row\">` + `<div class=\"col-md-8 col-12\">`, nothing else between) takes `row clickDropContent noBorder`; any other shape keeps the "
         "prefix form. Declined the same round: #1035 the per-panel upload button (the gold's ONE per page is an INVENTED box with prose in no WT — class C). OFF = the "
         "r417 output + the pin repair (20 pages). ON = 30 pages / 5 modules, 30 up / 0 down (+147.9pp-sum). |\n")
s = s.replace(old11, row11 + old11)
old14 = "- **Build:** `260619.88` (round 417 — **the XDLS choice-page panel holds its content directly"; assert s.count(old14) == 1
b14 = ("- **Build:** `260619.89` (round 418 — **the first tile panel takes the `row.clickDropContent.noBorder` form — the gold's first panel on every choice page "
       "puts the `clickDropContent` token on the section row (`row clickDropContent noBorder > col-12 col-md-8 > activity dropbox`, 35 / 35 pages of XDLS902–906) — "
       "and the r417 title-pin repair (the bare panel had lost the r334 `<h3>` pin: 114 panels at h5, the inner row / col is optional in `activityTitleLevelPostpass` "
       "now)** (`tile_grid.first_panel_row`, env `CDFIRSTROW_OFF`; `ContentConverter.#cdTilePair`); the autonomous loop's session 29 Round 9; the probe OFF = disk + "
       "the 20 repaired pages, ON 30 pages / 5 modules (30 up / 0 down, +147.9pp-sum, 0 outside the set); **SCOPED regeneration of the 5 (scoped ship #2 since the "
       "r416 FULL)**; **ROUND 418 BASELINE: SCAFFOLD mean 54.186% / >=50% 1439 / >=75% 238 / >=90% 20 / RAW 38.204% @ 2349 pairs** (+0.0630pp); compare_structure "
       "14168 / 186 / 683 / 23, body 54 / 5 / 190 / 247, clean 2504 / 2548, leak 73 / 44 — all EXACT; every verifier EXACT; 16 selftests GREEN; the miner 182 → 183 "
       "(#1036 gone; the per-panel upload button — declined, class C — and XDLS902's all-row form surfaced); plateau window 0 of 3). Previous: ")
s = s.replace(old14, b14 + old14)
wr(p, s)

p = R + "CONVERTER_V2/reference/tests/gate_baseline.json"; s = rd(p)
def setv(key, old, new):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=1); assert n == 1, key
setv("build", '"260619.88"', '"260619.89"'); setv("round", 417, 418)
setv("mean_scaffold_pct", 54.12, 54.19); setv("pages_ge_50", 1438, 1439); setv("raw_mean_pct", 38.1, 38.2)
a = '    "_note_r417": "Round 417 (session 29 Round 8)'; assert s.count(a) == 1
s = s.replace(a, '    "_note_r418": "Round 418 (session 29 Round 9): the first tile panel takes the row.clickDropContent.noBorder form (tile_grid.first_panel_row, env CDFIRSTROW_OFF) + the r417 title-pin repair (activityTitleLevelPostpass reaches the bare box — 114 panels back at h3); 5 modules / 30 pages; SCOPED regeneration of the 5, scoped #2 since the r416 FULL; skeleton 54.1231 -> 54.1860, >=50 1438 -> 1439, RAW 38.142 -> 38.204; every other gate EXACT).",\n' + a)
a2 = '    "_note_r416b": "Round 417: SCAFFOLD 53.9284'; assert s.count(a2) == 1
s = s.replace(a2, '    "_note_r417b": "Round 418: SCAFFOLD 54.1231 -> 54.1860 (+0.0630pp; 30 movers, 30 up / 0 down — XDLS904_2_0 +16.1, XDLS905_5_0 +8.1; 0 outside the 5-module affected set), 1439 / 238 / 20, RAW 38.204; 2349 pairs. Plateau window 0 of 3.",\n' + a2)
b2 = '    "_note_r417": "Round 417: 14168 / 186 / 683 / 23 EXACT'; assert s.count(b2) == 1
s = s.replace(b2, '    "_note_r418": "Round 418: 14168 / 186 / 683 / 23 EXACT.",\n' + b2)
b3 = '    "_note_r417": "Round 417: over-capture 54 / runaway 5'; assert s.count(b3) == 1
s = s.replace(b3, '    "_note_r418": "Round 418: over-capture 54 / runaway 5 / EMPTY 190 / ANY 247 EXACT.",\n' + b3)
wr(p, s); json.load(open(p, encoding="utf-8"))
print("r418 finalise: changelog + Config.js 260619.89 + CLAUDE.md §9/§11/§14 + gate_baseline.json done")
