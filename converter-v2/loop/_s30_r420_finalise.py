#!/usr/bin/env python3
"""r420 finalise (CLAUDE.md §12): changelog entry, Config.js bump, CLAUDE.md §9 / §11 / §14, gate_baseline.json (+ the bingo
section), KB_AMALGAMATION_STATUS.md D10-3 row, CHECKSUMS__gates.txt gains _verify_bingo.cjs. Run under WSL."""
import re, json, os, hashlib
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
PF = R + "pageforge-site/converter-v2/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

entry = """## 2026-09-21 (round 420, build 260619.91) — THE LETTER-GRID BINGO: the BLL family's `[Self check]` + a table of letters builds the KB's 03E bingo widget (Chris's D10-3 build lane — the selfCheck type's largest un-built authoring shape; the autonomous loop's session 30 Round 2; SCOPED regeneration of the 7 BLL modules, the probe proving the other 487 byte-identical)

### 1. WHAT CHANGED

**The lane.** D10-3 (2026-09-16): widget-BUILD rounds inside the loop, one type per kickoff, each round the type's largest un-built authoring SHAPE family ≥ 20 sites, judged A1 on the widget's own verifier. Session 27 Round 4 measured the lane to its floor on the pre-intake corpus ("no type has an un-built dialect ≥ 20 sites") — keyed on the r286 signature strings (`table 6x3`, `MULTI-TABLE x2` …), which split ONE authoring family across a dozen table dimensions. Re-read on the post-intake decline records by CONTENT (`outputs/_s30_r2_shapes.py`, `_s30_r2_bingo.py` → `_s30_r2_bingo.out`, `_s30_r2_scdump.cjs`): **selfCheck 215 un-built sites / 72 modules, 0 ever built** — the r69 question-list builder declines 127 of them on `bundle.tables`. Of the WT's 182 `[Self check]` tags, 113 are followed by a table and **55 of those are a LETTER GRID**: `[Self check] Click on the lower case letter ‘s’.` + a 2 × 6 table of single letters with the correct cells typed in RED, in 9 Blended Literacy modules (BLL120 14, BLL110 12, BLL130 12, BLL150 6, BLL160 4, BLL113 / BLL140 / BLL170 2, BLL154 1) — ≈ 28 bundles, each holding the lower-case and the capital grid plus the writer's `[Add an audio that when they click/hover on the letter it says the name of the letter …]` ELEMENT tag and an `**Alphabet Audio** [LINK]` line after each. The other 58 tables are the Question | Model-answer form (MXDI103, MXDB202, ENFUN04 — the KB selfCheck proper; a later shape).

**The gold builds the KB's BINGO** (03E COMP_04 `bingo` — `div.bingo.col-12 > div.bingoContainer[grid=N] > div.number[value=correct] > p` + the `row > activityButton reset-btn / activityButton hidden check-btn` row; required wrapper `activity interactive`): 96 bingos on 32 pages / 28 modules, **74 of them letter grids** — grid 12 cells → `grid="4"` 52 / 53, 9 → 3 12 / 13, 16 → 4; the wrapper `bingo col-12` 90 / 96; the button row 95 / 96; no `h4` card title 92 / 96; the cell `p.sassoonI-text` 53 / 74 (the family's Sassoon Infant font — 39 of them with a `span.audioTrigger[audioName=Name-X]`, the developer's snipped alphabet audio), `p.sassoon-text` 11, plain `p` 5; the cells re-typed by the developer in 20 of 52 grids (a different letter order, the same counts). The gold's bingo boxes are mostly BARE (`activity alertPadding interactive > h3, p, bingo…` 66 / 76) where Claude's boxes carry the inner `row > col-12` — measured corpus-wide (`_s30_r2_boxinner.py`): the bare box is 0.07 of the gold's alertPadding boxes (Inquiry BLL 0.21, its highest group), a per-module choice, not a class.

**The fix (DATA OVER CODE, never half-built).** `interactive_builders.selfCheck.letter_grid_bingo {enabled, env BINGO_OFF, max_cell_chars 2, min_cells 4, grid_by_cells {6: 3, 9: 3, 12: 4, 16: 4}, grid_default 4, lead, open, container_open, cell, cell_correct_attr, container_close, buttons, close, cell_class_by_prefix {BLL: sassoonI-text}, correct_from [red, lead_quote], lead_quote_pattern, asset_note_pattern, note_prefix}` + `InteractiveBuilder.#letterGridBingo`, tried BEFORE the r69 question-list form in `case "selfCheck"`. It fires only when every table in the bundle is a letter grid (every non-empty cell ≤ 2 letters / digits once the red markers and bold marks are stripped, ≥ 4 cells), every extra type is `selfCheck` itself (the second grid), every tag member is a selfCheck invocation or the audio ELEMENT request, and each table follows its own invocation whose black text is the lead. Per table: `<p>lead</p>` + the bingo — the cells row-major from the writer's table; `value="correct"` on the RED cells or, when the writer marked none, on the cells equal to the letter quoted in the lead (neither → decline); `grid` from the cell count; the cell `<p class="sassoonI-text">` for the BLL prefixes (plain `<p>` = the KB form elsewhere); no `audioTrigger` (the package cannot supply the asset) — the writer's audio request and the link line ride as the red Writers Note after the widget (`bundle.instructions`, the r214 / r350 form). The r356 read tracker sees every member read, so the members rule places nothing else; the box takes `.interactive` through `interactive_widget_types` (bingo is listed). BLL113's word grids (`Click on the word ‘the’` — 3-letter cells) and BLL154's tile shape decline by design.

**The new PROTECTED gate — `reference/tests/_verify_bingo.cjs`** (a `run_all_gates.sh` line over the 9 modules; `_selftest_core.cjs` inject spec; `gate_baseline.json.bingo`): every built grid is the 03E form — a `div.bingo` wrapper, a `bingoContainer` with a positive-integer `grid`, ≥ 4 cells each a `<p>` with text, at least one `value="correct"` cell, the Reset / Check row, no raw `[tag]` / red marker in a cell (defect 0 protected); exact / copy-edit / dev-edit against the gold's same-module bingos by cell multiset + correct count / cell count + correct count.

### 2. PROOF

- `_verify_bingo.cjs` over the 9: **52 grids / 624 cells on 7 modules — exact 34, copy-edit 11, dev-edit 7, defect 0**; gold bingos 12 / 14 / 12 / 2 / 9 / 4 / 2 on BLL110 / 120 / 130 / 140 / 150 / 160 / 170 (BLL150's other 3 are a picture-grid shape); selftest GREEN (liveness 12 on BLL110; the injected malformed grid 0 → 2).
- `_s30_r420_probe_run.sh` (the r410 harness over all 494 Claude-dir modules): **OFF (`BINGO_OFF`) = the disk on every page, 2555 / 2555**; **ON = exactly 7 pages / 7 modules** (BLL113 / BLL154 unchanged by design).
- `_s30_r420_pagescore.py` (the gate's own `match()` BEFORE regenerating): 7 paired pages, **RAW pp-sum +4.7 (every page up)**; SCAFFOLD pp-sum −1.1 (6 down by 0.1–0.6, BLL170 +0.4) — decomposed with `_s30_r420_dipdiff.py`: the hand-off box's one `WIDGET` line becomes the gold's own `p + WIDGET` per grid (`┌ 2× repeated block of 2:`), but Claude's box holds the inner `row > col-12` where the gold's BLL bingo boxes are bare, so the new lines sit two indents deeper than the gold's and cannot pair — the r289 documented class ("the SCAFFOLD view collapses a widget to one marker … while the RAW view rises"), accepted through the r289 NAMED-MOVEMENT override (`_fastloop_diff.py --commit --accept-named "skeleton SCAFFOLD mean"`, recorded in the baseline manifest) and the §1 A1 exception (a writer-tagged widget is judged on its verifier).
- SCOPED regeneration (`_s30_r420_regen.sh`: the 7 + a fresh 12-module spot-check sample, 3 batches rc 0): `_content_manifest.py fresh` **0 truly stale**; `_scoped_spotcheck.py verify` **12 / 12 byte-identical under the fix**.
- `scoped_ship.sh --affected _affected_r420.txt --toggle BINGO_OFF --no-regen --commit --round 420` (`_s30_r420_scoped_ship.log`): containment **7 ⊆ 7**; the decomposition proof — every row HELD except the scaffold mean −0.00 (named above); the ledger at scoped #4 since the r416 FULL; the baseline + manifest committed by the named re-run (`_s30_r420_fastloop_named.log`).
- `run_all_gates.sh` (`_s30_r420_gates.log`): skeleton 54.2 % / ≥50 1441 / ≥75 238 / ≥90 20 (state `_s30_r420_sk_final.json`: **54.2072 → 54.2067 %, −0.0005pp**; RAW 38.227 → 38.229 %; 7 movers, 0 outside the set); compare_structure 14170 / 186 / 683 / 23, body 54 / 5 / 190 / 247, clean 2504 / 2548, leak 73 / 44, tags 9557 — all EXACT; every verifier ✓; **17 selftests GREEN** (49 / 0 — the bingo selftest added); feature index GREEN; DIFF MINER 182 → 182 CANDIDATE rows.
- D10-3's "moved" test for a build round: the selfCheck type's *Still a box* count **215 → 163** (52 sites converted ≥ 20).

### 3. PROTECTED GATES (`_s30_r420_gates.log`, `_s30_r420_scoped_ship.log`, `_s30_r420_fastloop_named.log`)

- **Skeleton (PRIMARY)**: SCAFFOLD **54.2072 → 54.2067 % (−0.0005pp — NAMED, the r289 widget-marker class, the A1 exception)**; ≥50 **1441**, ≥75 **238**, ≥90 **20** EXACT; RAW **38.227 → 38.229 %**; 2349 pairs, skipped 0.
- **compare_structure** 14170 / 186 / 683 / 23 EXACT; **body_compare** 54 / 5 / 190 / 247 EXACT; **defect** clean 2504 / 2548, leak 73 / 44 EXACT; tags 9557 / 9557; every verifier EXACT; **bingo (NEW): 52 grids / defect 0**.
- Plateau (§4): a build round's "moved" test is the *Still a box* count (D10-3) — 215 → 163; the window stays at 0 of 3.

"""
p = PF + "BUILD_CHANGELOG.md"; s = rd(p)
head, rest = s.split("\n", 1)
assert head.startswith("# BUILD CHANGELOG") and rest.lstrip("\n").startswith("## 2026-09-21 (round 419")
wr(p, head + "\n\n" + entry + rest.lstrip("\n"))

p = PF + "app/js/Config.js"; s = rd(p)
old = '\tstatic AppVersion = "260619.90";'; assert s.count(old) == 1
note = ("\t// ROUND 420 (260619.91): THE LETTER-GRID BINGO — Chris's D10-3 build lane, the selfCheck type's largest un-built authoring shape: the BLL family's "
        "`[Self check] Click on the lower case letter ‘s’.` + a table of single letters (the correct cells in red) builds the KB's 03E bingo "
        "(`div.bingo.col-12 > div.bingoContainer[grid] > div.number[value=correct] > p.sassoonI-text` + the Reset / Check row; InteractiveBuilder.#letterGridBingo "
        "before the r69 question-list form; data interactive_builders.selfCheck.letter_grid_bingo, env BINGO_OFF; the writer's audio request rides as the Writers "
        "Note). 55 tables / 28 bundles in 9 modules; 52 grids built on 7 (BLL113's word grids and BLL154's tiles decline by design), exact 34 / copy-edit 11 / "
        "dev-edit 7 / defect 0 on the NEW protected gate _verify_bingo.cjs. The loop's session 30 Round 2: OFF = disk 2555 / 2555, ON 7 pages / 7 modules; SCOPED "
        "regeneration of the 7 (scoped #4 since the r416 FULL); RAW +4.7pp-sum, scaffold -0.0005pp (the r289 widget-marker class, named); every other gate EXACT; "
        "selfCheck still-a-box 215 -> 163.\n")
wr(p, s.replace(old, note + '\tstatic AppVersion = "260619.91";'))

p = PF + "CLAUDE.md"; s = rd(p)
old9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 419 BASELINE ("; assert s.count(old9) == 1
new9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 420 BASELINE (the letter-grid bingo — D10-3's selfCheck build, `letter_grid_bingo`, env "
        "`BINGO_OFF`; 7 BLL modules / 7 pages; SCOPED regeneration of the 7, the probe proving the other 487 byte-identical; scoped ship #4 since the r416 FULL): "
        "SCAFFOLD mean 54.2067% / >=50% 1441 / >=75% 238 / >=90% 20 / RAW 38.229% @ 2349 pairs, pairs skipped 0 — the mean −0.0005pp is the r289 widget-marker "
        "class, NAMED and accepted (7 movers: 6 down 0.1–0.6, BLL170 +0.4 — the built `p + WIDGET` pairs sit inside Claude's inner `row > col-12` where the gold's "
        "BLL bingo boxes are bare; RAW up on every page); every bucket EXACT; the 2342 unaffected pairs EXACT. compare_structure 14170 / 186 / 683 / 23, body_compare "
        "54 / 5 / 190 / 247, defect clean 2504 / 2548, leak 73 / 44 — all EXACT.** Previous — ROUND 419 BASELINE (")
s = s.replace(old9, new9)
olda = "Adjunct verifiers (run when you touch a widget): `_verify_dragdrop.cjs` (round 350"; assert s.count(olda) == 1
s = s.replace(olda, "Adjunct verifiers (run when you touch a widget): `_verify_bingo.cjs` (round 420 — a PROTECTED gate in `run_all_gates.sh` over the nine BLL letter-grid modules: every built bingo is the KB 03E form — a `div.bingo` wrapper, a `bingoContainer` with a positive-integer `grid`, ≥ 4 cells each a `<p>` with text, at least one `value=\"correct\"` cell, the Reset / Check row, no raw `[tag]` in a cell; exact / copy-edit / dev-edit against the gold's same-module bingos), " + olda[len("Adjunct verifiers (run when you touch a widget): "):])
old11 = "| `LANGFONT_OFF` | 419 | **THE LANGUAGE-FONT WRAP"; assert s.count(old11) == 1
row11 = ("| `BINGO_OFF` | 420 | **THE LETTER-GRID BINGO — the BLL family's `[Self check]` + a table of letters builds the KB's 03E bingo** (Chris's D10-3 build lane; the "
         "autonomous loop's session 30 Round 2 — the selfCheck type's largest un-built authoring shape, found by reading the r286 decline records by CONTENT rather than "
         "by signature string: 55 letter-grid tables / ≈ 28 bundles in 9 modules — BLL120 14, BLL110 12, BLL130 12, BLL150 6, BLL160 4, BLL113 / 140 / 170 2, BLL154 1; "
         "`_s30_r2_bingo.py`, `_s30_r2_scdump.cjs`). `InteractiveBuilder.#letterGridBingo` runs BEFORE the r69 question-list form: fires only when every table in the "
         "bundle is a letter grid (every non-empty cell ≤ `max_cell_chars` once the red markers / bold marks are stripped, ≥ `min_cells`), every extra type is selfCheck "
         "itself, every tag member is a selfCheck invocation or the writer's `[Add an audio …]` ELEMENT request, and each table follows its own invocation whose black "
         "text is the lead; per table → `<p>lead</p>` + `div.bingo.col-12 > div.bingoContainer[grid] > N × div.number[value=correct] > p(.sassoonI-text)` + the Reset / "
         "Check row (the cells row-major from the writer's table; correct = the RED cells, else the cells equal to the letter quoted in the lead, neither → decline; "
         "`grid` from the cell count 12 → 4 / 9 → 3 / 16 → 4; the cell class by module-code prefix — BLL → Sassoon Infant, plain `<p>` = the KB form elsewhere); no "
         "`audioTrigger` (the package cannot supply the developer's snipped audio) — the writer's request and the `**Alphabet Audio** [LINK]` line ride as the red "
         "Writers Note after the widget (`bundle.instructions`). Measured: the gold's 74 letter-grid bingos (of 96) — grid 4 for 12 cells 52 / 53, `bingo col-12` 90 / 96, "
         "the button row 95 / 96, `p.sassoonI-text` 53 / 74; the bare bingo box (no inner row / col) is 0.07 of the gold's alertPadding boxes corpus-wide (BLL Inquiry "
         "0.21) — not taken. Verifier `_verify_bingo.cjs` (protected, defect 0; 52 grids: exact 34 / copy-edit 11 / dev-edit 7). OFF = the r419 output (2555 / 2555). "
         "ON = 7 pages / 7 modules (RAW +4.7pp-sum; scaffold −1.1pp-sum = the r289 widget-marker class, named); selfCheck still-a-box 215 → 163. |\n")
s = s.replace(old11, row11 + old11)
old14 = "- **Build:** `260619.90` (round 419 — **the language-font wrap"; assert s.count(old14) == 1
b14 = ("- **Build:** `260619.91` (round 420 — **the letter-grid bingo: the BLL family's `[Self check]` + a table of letters builds the KB's 03E bingo** — Chris's D10-3 "
       "build lane, the selfCheck type's largest un-built authoring shape (`interactive_builders.selfCheck.letter_grid_bingo`, env `BINGO_OFF`; "
       "`InteractiveBuilder.#letterGridBingo`; the NEW protected gate `_verify_bingo.cjs` — 52 grids / 624 cells on 7 modules, exact 34 / copy-edit 11 / dev-edit 7 / "
       "defect 0; 17 selftests GREEN); the autonomous loop's session 30 Round 2; the probe OFF = disk 2555 / 2555, ON 7 pages / 7 modules; **SCOPED regeneration of the 7 "
       "(scoped ship #4 since the r416 FULL)**; **ROUND 420 BASELINE: SCAFFOLD mean 54.2067% / >=50% 1441 / >=75% 238 / >=90% 20 / RAW 38.229% @ 2349 pairs** (the mean "
       "−0.0005pp = the r289 widget-marker class, NAMED and accepted; RAW +4.7pp-sum); compare_structure 14170 / 186 / 683 / 23, body 54 / 5 / 190 / 247, clean 2504 / 2548, "
       "leak 73 / 44 — all EXACT; every verifier EXACT; the miner 182 → 182; selfCheck still-a-box 215 → 163). Previous: ")
s = s.replace(old14, b14 + old14)
wr(p, s)

p = R + "CONVERTER_V2/reference/tests/gate_baseline.json"; s = rd(p)
def setv(key, old, new):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=1); assert n == 1, key
setv("build", '"260619.90"', '"260619.91"'); setv("round", 419, 420)
a = '    "_note_r419": "Round 419 (session 30 Round 1)'; assert s.count(a) == 1
s = s.replace(a, '    "_note_r420": "Round 420 (session 30 Round 2): the letter-grid bingo — D10-3\'s selfCheck build (interactive_builders.selfCheck.letter_grid_bingo, env BINGO_OFF; the NEW protected gate _verify_bingo.cjs, defect 0). SCOPED regeneration of the 7 BLL modules (scoped #4 since the r416 FULL); the probe proving the other 487 byte-identical. The scaffold mean 54.2072 -> 54.2067 (-0.0005pp) is the r289 widget-marker class, NAMED and accepted through _fastloop_diff.py --accept-named; RAW 38.227 -> 38.229.",\n' + a)
a2 = '    "_note_r418b": "Round 419: SCAFFOLD 54.1860'; assert s.count(a2) == 1
s = s.replace(a2, '    "_note_r419b": "Round 420: SCAFFOLD 54.2072 -> 54.2067 (-0.0005pp NAMED — the r289 widget-marker class: 7 movers, 6 down 0.1-0.6 / BLL170 +0.4, the built p + WIDGET pairs inside Claude\'s inner row > col-12 where the gold\'s BLL bingo boxes are bare; RAW up on every page), 1441 / 238 / 20 EXACT, RAW 38.229; 2349 pairs. mean_scaffold_pct stays 54.21 at the recorded precision.",\n' + a2)
b2 = '    "_note_r419": "Round 419: exact 14168 -> 14170'; assert s.count(b2) == 1
s = s.replace(b2, '    "_note_r420": "Round 420: 14170 / 186 / 683 / 23 EXACT.",\n' + b2)
b3 = '    "_note_r419": "Round 419: over-capture 54 / runaway 5 / EMPTY 190 / ANY 247 EXACT.",'; assert s.count(b3) == 1
s = s.replace(b3, '    "_note_r420": "Round 420: over-capture 54 / runaway 5 / EMPTY 190 / ANY 247 EXACT.",\n' + b3)
# the bingo section, after dragdrop
tail = s.rstrip()
assert tail.endswith("}")
body = tail[:-1].rstrip()
assert body.endswith("}"), body[-40:]
bingo = (',\n  "bingo": {\n    "grids": 52,\n    "cells": 624,\n    "defect": 0,\n    "exact": 34,\n    "copy_edit": 11,\n    "dev_edit": 7,\n'
         '    "_note": "Round 420 — _verify_bingo.cjs over BLL110 BLL120 BLL130 BLL140 BLL150 BLL160 BLL170 BLL113 BLL154: 52 grids / 624 cells on 7 modules (BLL113 / BLL154 build none by design); the KB 03E form on every grid — defect 0 protected; exact / copy-edit / dev-edit a tracked baseline, hold-or-improve."\n  }\n}\n')
s = body + bingo
wr(p, s); json.load(open(p, encoding="utf-8"))

# KB status — the D10-3 row records the selfCheck kickoff
p = R + "KB_AMALGAMATION_STATUS.md"; s = rd(p)
old = "no dragAndDrop shape ≥ 20 sites remains derivable (word tiles 37 need the answer sentence, image column-sort 13, red-header sub-shapes < 20 each) → the kickoff moves to clickDrop (323 / 107)**"
assert s.count(old) == 1
s = s.replace(old, old[:-2] + "; **selfCheck kickoff shape 1 SHIPPED r420 (2026-09-21, the loop's session 30 Round 2: the BLL family's letter grid → the KB 03E bingo, 52 grids / 7 modules of 55 tables / 9; new protected gate `_verify_bingo.cjs`, defect 0; found by re-reading the r286 decline records by content — the s27-r4 'no dialect ≥ 20 sites' verdict was keyed on the signature strings, which split one family across table dimensions); selfCheck still-a-box 215 → 163 (the Question | Model-answer table form, 58 sites, is the next shape)**")
wr(p, s)

# the gate checksum manifest gains the new verifier (the r420 checksums script refreshes every existing row)
p = R + "_MIGRATION/CHECKSUMS__gates.txt"; s = rd(p)
if "_verify_bingo.cjs" not in s:
    md5 = hashlib.md5(open(R + "CONVERTER_V2/reference/tests/_verify_bingo.cjs", "rb").read()).hexdigest()
    lines = s.rstrip("\n").split("\n")
    lines.append(md5 + " *CONVERTER_V2/reference/tests/_verify_bingo.cjs")
    wr(p, "\n".join(sorted(lines, key=lambda l: l.split("*", 1)[1])) + "\n")
print("r420 finalise: changelog + Config.js 260619.91 + CLAUDE.md §9/§11/§14 + gate_baseline.json (+bingo) + KB status + gates manifest done")
