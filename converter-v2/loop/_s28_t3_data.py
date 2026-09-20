#!/usr/bin/env python3
"""SESSION 28 / TASK 3 (round 410) — insert `body_region.fundamentals_panels.tile_pages` into data/Emit_Templates.json, right before
`level_pages` (text splice: LF-preserving, tab-indented like its neighbours, JSON-validated after). Idempotent. WSL."""
import io, os, json
P = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/data/Emit_Templates.json"
s = io.open(P, encoding="utf-8", newline="").read()
if '"tile_pages": {' in s:
    print("already present"); raise SystemExit
anchor = '\t\t\t"level_pages": {\n'
assert s.count(anchor) == 1, "anchor"
block = {
    "enabled": True,
    "env": "TILEPAGE_OFF",
    "_doc": ("ROUND 410 (session 28, Task 3 — the WJFUN 'My Te Kura Writing' FUNdamentals family, 21 modules). THE TILE-PAGE fundamentals dialect: "
             "the writer authors ONE single-file module whose lessons are TILES — `[Tile N content]` (or `[Tile N]`) opens each, `[Tile N content ENDS]` "
             "closes it; inside a tile `[H1] <title>` names it, `[Overview]` + `[Learning intention for tile]` (a 'We are learning:' lead + bullets) + "
             "`[Success criteria for tile]` ('I can:' + bullets) carry its menu pane, `[Lesson content]` opens the body; before the tiles the module's "
             "`[Overview]` holds the `[H3] Knowledge Year N` / `[H3] Practices Year N` bullet blocks (the menu's Overview pane, two columns), the "
             "`[Introduction content]` prose, an `[Insert links/buttons to the individual tile sections …]` tile table (rendered by the tile row, so consumed) "
             "and the `[RHS side tab navigation: for all pages/tiles]` list of `Tab N <label>` lines (the phases nav's labels, consumed). Measured on the "
             "21 golds (outputs/_s28_t3_tiles.py): the distinct `[Tile N …]` count equals the gold's fundamentalsPanel count on 16 / 21 (the `Tab N` list on "
             "15 / 21; both together 19 / 21 — WJFUN105's developer split one tile in two, WJFUN112's nav lists a 'Test' phase without a panel). The gold "
             "form: `div.phases` nav labelled with the tab labels, `div.introduction` ending in a `row phaseContainer` of `col-md-3 col-6` phaseLink tiles "
             "(h3 label + phaseImg), one `fundamentalsPanel phase=N` per tile opening with the tile title as `<h2>`, and a tabs menu Overview + one pane per "
             "tile (ONE `col-md-8 col-12` column: `<h5>Learning Intentions</h5><p>We are learning:</p><ul>…</ul><p>I can:</p><ul>…</ul>`). Rides the r265 "
             "level-pages machinery: the pre-pass pushes a phasebreak per tile, synthesizes the tile title as a writer heading (title_writer_level), fills "
             "run._levelMenu (PanelsBuilder.#levelPagesNav builds nav + tiles from the registry row; MenuBuilder.#levelTabs composes the panes — the NEW "
             "menu.pane_form 'single_col' puts LI + SC in one column). Registry-gated (WJFUN|1-3 / 4-6 / 7-8) + fundamentals body class + single-file; a "
             "module with fewer than min_markers distinct tile markers is left exactly as before. Env TILEPAGE_OFF reverts the whole dialect."),
    "marker_pattern": "^\\[tile\\s*(\\d+)(?:\\s+content)?\\]$",
    "marker_ends_pattern": "^\\[tile\\s*\\d+\\s+content\\s+ends\\]$",
    "min_markers": 2,
    "nav_tag_pattern": "side tab navigation",
    "tab_line_pattern": "^tab\\s*(\\d+)\\b",
    "tile_links_pattern": "^\\[insert links?\\s*/\\s*buttons? to the individual tile sections",
    "li_tag_pattern": "^\\[learning intentions? for tile\\]$",
    "sc_tag_pattern": "^\\[success criteria for tile\\]$",
    "lesson_content_pattern": "^\\[lesson content\\]$",
    "overview_alias_pattern": "^\\[overview\\]$",
    "module_pane_heading_pattern": "knowledge|practices|learning intention|success criteria|how will i know",
    "title_writer_level": 1,
    "title_tags": ["h1", "h2", "h3"],
    "menu": {
        "pane_form": "single_col",
        "overview_label": "Overview",
        "nav_item": "\n<li><a>{label}</a></li>",
        "pane_open": "\n<div class=\"tab-pane\">\n<div class=\"row\">",
        "pane_close": "\n</div>\n</div>",
        "col_template": "<div class=\"{cls}\">\n{content}\n</div>",
        "heading_template": "<h5>{label}</h5>",
        "li_label_default": "Learning Intentions",
        "sc_label_default": "How will I know I have learned it?"
    },
    "registry": {
        "_doc": "series (this module's own code) beats the subject|template_phase group. Every WJFUN level shares the gold's one tile form.",
        "series": {},
        "groups": {
            "WJFUN|1-3": {
                "menu_cols": ["col-md-8 col-12"],
                "menu_cols_overview": ["col-md-6 col-12 paddingR", "col-md-6 col-12 paddingL"],
                "phases_nav_item": "<div phase=\"{n}\">\n<p>{label}</p>\n</div>",
                "tiles_open": "<div class=\"row phaseContainer\">",
                "tile_open": "<div class=\"col-md-3 col-6\">\n<div class=\"phaseLink\" phase=\"{n}\">\n<h3>{label}</h3>",
                "tile_img": "<img class=\"phaseImg\" src=\"{src}\" alt=\"{alt}\">",
                "tile_close": "</div>\n</div>",
                "tiles_close": "</div>",
                "tiles_inside_col": False
            }
        }
    }
}
block["registry"]["groups"]["WJFUN|4-6"] = dict(block["registry"]["groups"]["WJFUN|1-3"])
block["registry"]["groups"]["WJFUN|7-8"] = dict(block["registry"]["groups"]["WJFUN|1-3"])
txt = json.dumps({"tile_pages": block}, indent="\t", ensure_ascii=False)
# strip the outer braces, re-indent to three tabs like the neighbours
lines = txt.split("\n")[1:-1]
lines = ["\t\t" + l for l in lines]
ins = "\n".join(lines).rstrip() + ",\n"
s = s.replace(anchor, ins + anchor, 1)
json.loads(s)  # validate
io.open(P, "w", encoding="utf-8", newline="").write(s)
print("inserted tile_pages;", len(s), "bytes; JSON valid")
