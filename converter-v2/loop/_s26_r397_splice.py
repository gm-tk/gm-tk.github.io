#!/usr/bin/env python3
"""Session 26 Round 11 (engine r397) — A HEADER CELL IS PLAIN: a `<th>` whose whole content is one <b>/<strong> span (the writer's
**bold** header row) drops the wrapper — the gold's th is plain 0.96. Data: `elements.table.header_cell_plain {enabled, env
THPLAIN_OFF}`. Engine: TablesAndGrids' cell emit, header cells of FREE-BODY tables only. Also writes the PICK. LF preserved.
Idempotent. Run under WSL."""
import io, os, sys
ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
PF = ROOT + "/pageforge-site/converter-v2"

LS = ROOT + "/LOOP_STATE.md"
s = io.open(LS, encoding="utf-8", newline="").read()
if "## Session 26 — Round 11 PICK (engine r397)" not in s:
    PICK = """## Session 26 — Round 11 PICK (engine r397): A TABLE HEADER CELL IS PLAIN — the writer's **bold** header row renders `<th>text</th>`, not `<th><b>text</b></th>`
- **The lead:** the r394 miner's row #3725 (`body EXTRA th>b › b`, 20 pages / 15 modules, consensus 1.00) fell under the floor at r394's re-mine; the position-free census (`outputs/_s26_r397_thb.py` → `.out`, every `<th>` in every paired page's live body): **the gold's 2170 header cells are wholly bold 97 = 0.04 (plain 0.96); Claude's 2012 are wholly bold 369 = 0.18 on 86 pages / 56 modules.** Per group the gold is plain in every one with a floor-sized population: Mathematics 0.93 (Claude bold 114 on 24 pages / 15 modules), ConnectED 0.98 (44 / 14 pages / 5), TEDC 1.00 (37 / 8 pages), NCEA1 1.00 (25 / 7 pages), Inquiry EXPlore 1.00 (39 / 3 pages), Leaving to Learn 1.00 (11 / 5 pages); English is the one place the gold keeps some bold (30 / 178 = 0.17) and Claude is already below it there (16 / 243). Fundamentals / Arts (gold 11 / 13 bold on ONE page) is noise under the floor.
- **Where Claude's come from:** the r383 first-row-header rule promotes a writer's wholly-bold first row to `<th>`; the cell's own `**…**` markdown then renders `<b>` inside it — `TablesAndGrids.renderCellInline`'s own comment already states the convention ("PLAIN text in a HEADER cell — already bold by default in the site's CSS") for tag-rendered cells, but the markdown path keeps the wrapper.
- **KB-first check:** 05D's table forms show `<tr><th>Header 1</th><th>Header 2</th></tr>` — plain header cells; nothing sanctions `<th><b>` → §1b level 1 / 3 (the KB form + the gold's 0.96). Markup-only, deterministic (a whole-cell bold wrapper inside a `<th>`) → derivable.
- **Fix (DATA OVER CODE):** `elements.table.header_cell_plain {enabled, env: THPLAIN_OFF}` — at the cell emit in `TablesAndGrids` (free-body tables only, `!insidePlaceholder`): when the cell is a header cell and its rendered content is exactly ONE `<b>…</b>` / `<strong>…</strong>` span with no other bold inside, the wrapper is dropped. Data cells (`<td>`) untouched — the gold keeps `<td><b>` for a matrix's row labels. OFF = the r396 output. Regeneration: SCOPED (the probe's ON list) = scoped ship #1 since the r396 full.

"""
    i = s.index("## Round log\n")
    s = s[:i] + PICK + s[i:]
    io.open(LS, "w", encoding="utf-8", newline="").write(s); print("PICK written")

P = PF + "/data/Emit_Templates.json"
s = io.open(P, encoding="utf-8", newline="").read()
if '"header_cell_plain"' not in s:
    old = '\t\t\t"header_cell": "<th>{content}</th>",\n\t\t\t"cell": "<td>{content}</td>",\n'
    assert s.count(old) == 1, s.count(old)
    new = (old +
           '\t\t\t"header_cell_plain": {\n'
           '\t\t\t\t"_doc": "ROUND 397 (the autonomous loop\'s session 26 Round 11 — the census outputs/_s26_r397_thb.py). A TABLE HEADER CELL IS PLAIN: the gold\'s 2170 <th> cells are wholly bold 97 = 0.04 (plain 0.96; Mathematics 0.93, ConnectED 0.98, TEDC / NCEA1 / EXPlore / LtL 1.00); Claude\'s were wholly bold 369 = 0.18 on 86 pages / 56 modules — the r383 first-row-header rule promotes a writer\'s **bold** row to <th> and the cell\'s own markdown then renders <b> inside it (KB 05D\'s form is <tr><th>Header 1</th>…, plain). At the cell emit, free-body tables only: a header cell whose rendered content is exactly one <b>/<strong> span with no other bold inside drops the wrapper; data cells (<td>) keep theirs (the gold keeps <td><b> for a matrix\'s row labels). OFF = the r396 output.",\n'
           '\t\t\t\t"enabled": true,\n'
           '\t\t\t\t"env": "THPLAIN_OFF"\n'
           '\t\t\t},\n')
    s = s.replace(old, new, 1)
    io.open(P, "w", encoding="utf-8", newline="").write(s); print("data: table.header_cell_plain added")
else:
    print("data: already")

P2 = PF + "/app/js/TablesAndGrids.js"
s = io.open(P2, encoding="utf-8", newline="").read()
if "header_cell_plain" not in s:
    old = "\t\t\t\t\treturn Utils.FillTemplate(cellTpl, { content });\n"
    assert s.count(old) == 1, s.count(old)
    new = ("\t\t\t\t\t// ROUND 397 — A HEADER CELL IS PLAIN: the gold's <th> is wholly bold 0.04 (KB 05D's\n"
           "\t\t\t\t\t// <tr><th>Header 1</th> form); Claude's writer-bold header row rendered <th><b>…</b></th>\n"
           "\t\t\t\t\t// on 86 pages. A header cell whose rendered content is exactly ONE <b>/<strong> span\n"
           "\t\t\t\t\t// (no other bold inside) drops the wrapper; <td> cells keep theirs. Free-body only.\n"
           "\t\t\t\t\t// Data elements.table.header_cell_plain; env THPLAIN_OFF (= the r396 output).\n"
           "\t\t\t\t\tlet _cell = content;\n"
           "\t\t\t\t\tconst _thp = t.header_cell_plain;\n"
           "\t\t\t\t\tif (isHdr && !insidePlaceholder && _thp && _thp.enabled !== false\n"
           "\t\t\t\t\t\t&& !(typeof process !== \"undefined\" && process.env && process.env[_thp.env ?? \"THPLAIN_OFF\"])) {\n"
           "\t\t\t\t\t\tconst _m = String(_cell).match(/^\\s*<(b|strong)>([\\s\\S]*)<\\/\\1>\\s*$/);\n"
           "\t\t\t\t\t\tif (_m && !/<\\/?(?:b|strong)\\b/.test(_m[2])) _cell = _m[2];\n"
           "\t\t\t\t\t}\n"
           "\t\t\t\t\treturn Utils.FillTemplate(cellTpl, { content: _cell });\n")
    s = s.replace(old, new, 1)
    io.open(P2, "w", encoding="utf-8", newline="").write(s); print("engine: TablesAndGrids header cell plain")
else:
    print("engine: already")
