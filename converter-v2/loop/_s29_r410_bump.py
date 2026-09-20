#!/usr/bin/env python3
"""r410 finalise — Config.js AppVersion 260619.80 -> 260619.81 with the ROUND 410 comment (CLAUDE.md §12 step 2)."""
p = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/app/js/Config.js"
s = open(p, encoding="utf-8").read()
old = '\tstatic AppVersion = "260619.80";'
assert s.count(old) == 1, s.count(old)
note = ("\t// ROUND 410 (260619.81): the WJFUN \"My Te Kura Writing\" TILE-PAGE dialect — a single-file Fundamentals module laid out as "
        "clickable tiles builds the gold's tabs menu (an Overview pane in two columns + one single-column pane per tile), the `div.phases` "
        "nav, the `phaseLink` tile row and one `fundamentalsPanel` per tile with its title as `<h2>` (ContentConverter.#tilePagesPrepass → "
        "the r265 level-pages machinery; InteractiveScanner.#tilePageMarker hard terminator; MenuBuilder.#levelTabs single-column panes; "
        "PanelsBuilder.panelTitleLevelPostpass level_dialect_code_prefixes; data body_region.fundamentals_panels.tile_pages, env "
        "TILEPAGE_OFF). Built and proven in session 28 Task 3, shipped by the loop's session 29 Round 1: OFF = disk 2555 / 2555, ON exactly "
        "the 21 WJFUN overviews (21 up / 0 down, +257.1pp-sum; the family 37.6 → 49.9 %); SCOPED regeneration of the 23 WJFUN + JPFUN "
        "modules (scoped ship #2 since the 19 Sept FULL); skeleton 53.680 → 53.789 % (+0.1095pp), ≥50 1398 → 1406, compare_structure exact "
        "14091 → 14175, every other gate EXACT; miner 183 → 184 (the phases-nav rows gone).\n")
s = s.replace(old, note + '\tstatic AppVersion = "260619.81";')
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("Config.js bumped to 260619.81")
