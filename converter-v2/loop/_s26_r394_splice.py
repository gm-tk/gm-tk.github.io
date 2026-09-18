#!/usr/bin/env python3
"""Session 26 Round 8 (engine r394) — THE CLICKDROP BUTTONS SIT DIRECTLY IN THE COLUMN: no inner `<div class="row">` around a
built clickDrop's buttons + panels. Data: `interactive.clickDrop.no_row_wrapper {enabled, env CDROW_OFF}`. Engine: the two
clickDrop emit sites in InteractiveBuilder take their wrapper from `#cdWrap(tpl)` (empty when the flag is on). Also writes the
PICK. LF preserved. Idempotent. Run under WSL."""
import io, os, sys
ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
PF = ROOT + "/pageforge-site/converter-v2"

LS = ROOT + "/LOOP_STATE.md"
s = io.open(LS, encoding="utf-8", newline="").read()
if "## Session 26 — Round 8 PICK (engine r394)" not in s:
    PICK = """## Session 26 — Round 8 PICK (engine r394): THE CLICKDROP BUTTONS SIT DIRECTLY IN THE COLUMN — the built widget's inner `<div class="row">` is Claude's, not the gold's
- **The lead:** the r393 miner's one new row #3699 (`body EXTRA div.col-12.col-md-8 › div.row`, 20 pages / 18 modules, Online Safety 7) read against the page: ENGJ302_8_0's inner row wraps `div.button.clickDrop` × 4 + their `clickDropContent` panels — the built clickDrop's own `open` template (`<div class="row">`). The column census (`outputs/_s26_r394_colrow.py` → `.out`, a `div.row` DIRECTLY inside the col-md-8 text column, Claude vs gold): Claude's third-largest kind is `div.row › div.button.clickDrop` (93 on 72 pages / 51 modules); the gold has no such kind at all.
- **The paired widget census (`outputs/_s26_r394_clickdrop.py` → `.out`, the three wrappers enclosing every clickDrop button group, corpus-wide):** **gold 385 groups — the buttons' PARENT is a column (`div.col-12.col-md-8` under the page row, `div.col-12` under an activity box) 302 = 0.78; an inner `div.row` 19 = 0.05** (accContent 9, alert.solid 7, the rest single-digit widget-internal shapes). By subject: Mathematics 71 col / 0 row, Online Safety 47 / 2, NCEA1 41 / 3, English 35 / 6, BLL 26 / 0, ConnectED 22 / 0, Leaving to Learn 13 / 0, the subject-less TEDC 19 / 7 (0.73), Social Science 10 / 0 — every group at the floor ≥ 0.73. **Claude 128 groups — 127 wrapped in an inner `div.row`** (`div.row › div.col-12.col-md-8 › div.row` 73 on 72 pages / 51 modules; `div.row › div.col-12 › div.row` 52 on 52 pages / 34 modules — the activity-owned ones), 1 the conversation reveal-bubble form (its own template, untouched).
- **KB-first check:** the widget data's own `_comment` ("the human renders, inside a <div class=row>, ALL the buttons FIRST then ALL the content panels") is the r283 reading; the gold measured today puts that row NOWHERE — the buttons sit in the column the page (or the activity box) already opened. 05D / the Interactive_Wrapper_Catalogue say nothing about an extra row → §1b level 3 / 4 (the gold's own consensus 0.78, ≥ 0.73 in every group). A wrapper-only change, structure-only → derivable; the r283 verifier pairs button[i] ↔ content[i] by index — the wrapper is invisible to it (its RESULT must hold).
- **Fix (DATA OVER CODE):** `interactive.clickDrop.no_row_wrapper {enabled, env: CDROW_OFF}` — the two clickDrop emit sites (`#clickDrop` narrow walk, `#clickDropEntry` r283 composer) take `open` / `close` from `#cdWrap(tpl)`: empty strings when the flag is on (empties filtered from the join so no blank line is left). The r307 tile grid (`row_open`) and the conversation reveal bubble keep their own wrappers. OFF = the r393 output. Regeneration: SCOPED (the probe's ON list) = scoped ship #6 since the r388 full.

"""
    i = s.index("## Round log\n")
    s = s[:i] + PICK + s[i:]
    io.open(LS, "w", encoding="utf-8", newline="").write(s); print("PICK written")

P = PF + "/data/Emit_Templates.json"
s = io.open(P, encoding="utf-8", newline="").read()
if '"no_row_wrapper"' not in s:
    old = '\t\t\t"enabled": true,\n\t\t\t"list_content": true,\n\t\t\t"open": "<div class=\\"row\\">",\n'
    assert s.count(old) == 1, s.count(old)
    new = ('\t\t\t"no_row_wrapper": {\n'
           '\t\t\t\t"_doc": "ROUND 394 (the autonomous loop\'s session 26 Round 8 — the r393 miner row #3699 decomposed; the census outputs/_s26_r394_clickdrop.py). THE CLICKDROP BUTTONS SIT DIRECTLY IN THE COLUMN: over the gold\'s 385 clickDrop button groups the buttons\' parent is a column (the page\'s col-md-8 or the activity box\'s col-12) 302 = 0.78, an inner div.row 19 = 0.05 — every subject at the floor >= 0.73 (Mathematics 71 / 0, Online Safety 47 / 2, NCEA1 41 / 3, English 35 / 6, BLL 26 / 0). Claude wrapped 127 of its 128 groups in the `open` row below. When enabled, both clickDrop emit sites drop `open` / `close` (the r307 tile grid and the conversation reveal bubble keep their own wrappers). OFF = the r393 output.",\n'
           '\t\t\t\t"enabled": true,\n'
           '\t\t\t\t"env": "CDROW_OFF"\n'
           '\t\t\t},\n' + old)
    s = s.replace(old, new, 1)
    io.open(P, "w", encoding="utf-8", newline="").write(s); print("data: clickDrop.no_row_wrapper added")
else:
    print("data: already")

P2 = PF + "/app/js/InteractiveBuilder.js"
s = io.open(P2, encoding="utf-8", newline="").read()
if "#cdWrap" not in s:
    old1 = "\t\treturn [tpl.open, ...buttons, ...contents, tpl.close].join(\"\\n\");\n\t}\n"
    assert s.count(old1) == 1, s.count(old1)
    new1 = ("\t\tconst _cdw = this.#cdWrap(tpl);\n"
            "\t\treturn [_cdw.open, ...buttons, ...contents, _cdw.close].filter((x) => x !== \"\").join(\"\\n\");\n\t}\n"
            "\n"
            "\t/**\n"
            "\t * ROUND 394 — THE CLICKDROP BUTTONS SIT DIRECTLY IN THE COLUMN. Over the gold's 385\n"
            "\t * clickDrop button groups the buttons' parent is a column (the page's col-md-8 or the\n"
            "\t * activity box's col-12) 302 = 0.78; an inner div.row 19 = 0.05 — every subject >= 0.73.\n"
            "\t * Claude wrapped 127 of its 128 groups in the template's `open` row. With\n"
            "\t * clickDrop.no_row_wrapper enabled both emit sites take an EMPTY wrapper from here\n"
            "\t * (empties are filtered from the join). Env toggle: CDROW_OFF (= the r393 output).\n"
            "\t * @param {Object} tpl - the clickDrop template block\n"
            "\t * @returns {{open: string, close: string}}\n"
            "\t */\n"
            "\tstatic #cdWrap(tpl) {\n"
            "\t\tconst cfg = tpl?.no_row_wrapper;\n"
            "\t\tconst off = typeof process !== \"undefined\" && process.env && process.env[cfg?.env ?? \"CDROW_OFF\"];\n"
            "\t\tif (cfg && cfg.enabled !== false && !off) return { open: \"\", close: \"\" };\n"
            "\t\treturn { open: tpl.open, close: tpl.close };\n"
            "\t}\n")
    s = s.replace(old1, new1, 1)
    old2 = "\t\tconst html = [tpl.open, ...built.buttons, ...built.contents, tpl.close].join(\"\\n\");\n"
    assert s.count(old2) == 1, s.count(old2)
    new2 = ("\t\tconst _cdw = this.#cdWrap(tpl);   // ROUND 394: no inner row around the buttons (clickDrop.no_row_wrapper)\n"
            "\t\tconst html = [_cdw.open, ...built.buttons, ...built.contents, _cdw.close].filter((x) => x !== \"\").join(\"\\n\");\n")
    s = s.replace(old2, new2, 1)
    io.open(P2, "w", encoding="utf-8", newline="").write(s); print("engine: #cdWrap + the two emit sites")
else:
    print("engine: already")
