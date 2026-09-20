#!/usr/bin/env python3
"""r410 finalise — CLAUDE.md §9 (the skeleton baseline row), §11 (the TILEPAGE_OFF toggle row), §14 (the state snapshot bullet)."""
p = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/CLAUDE.md"
s = open(p, encoding="utf-8").read()

# --- §9: the skeleton row — prepend the r410 baseline, demote r408 to "Previous —"
old9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 408 BASELINE ("
assert s.count(old9) == 1
new9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 410 BASELINE (the WJFUN tile-page dialect — "
        "`body_region.fundamentals_panels.tile_pages`, env `TILEPAGE_OFF`; 21 WJFUN modules / 21 pages; SCOPED regeneration of the 23 "
        "WJFUN + JPFUN modules, the probe proving the other 471 byte-identical; scoped ship #2 since the 19 Sept full): SCAFFOLD mean "
        "53.789% / >=50% 1406 / >=75% 236 / >=90% 20 / RAW 37.925% @ 2349 pairs, pairs skipped 0 — hold-or-improve; 21 movers (21 up, "
        "0 down — WJFUN107 +35.9, WJFUN106 +30.1, WJFUN305 +29.0; 0 outside the affected set); the 2328 unaffected pairs EXACT. "
        "compare_structure exact 14175 (pool 16414 → 16470) / EXTRA 186 / MISSING 690 / row-wrap 23; body_compare over-capture 54 / "
        "runaway 6 / EMPTY 190 / ANY 248 EXACT; defect clean 2504 / 2548 = 98.27%, leak 73 / 44 EXACT; WJFUN 37.6 → 49.9%.** "
        "Previous — ROUND 408 BASELINE (")
s = s.replace(old9, new9)

# --- §11: the toggle row, inserted directly above HEADLEDOWNER_OFF (newest first in that block)
old11 = "| `HEADLEDOWNER_OFF` | 407 | **THE HEADING-LED NUMBERED OPENER TAKES THE OWNER FORM TOO**"
assert s.count(old11) == 1
row11 = ("| `TILEPAGE_OFF` | 410 | **THE WJFUN \"MY TE KURA WRITING\" TILE-PAGE DIALECT** (built and proven in session 28 Task 3, "
         "shipped by the autonomous loop's session 29 Round 1 — the intake handover's #1 round). A single-file Fundamentals module the "
         "writer lays out as clickable tiles — a `[Tile N content]` / `[Tile N]` marker (16 modules), a `[LESSON N]` marker alone or "
         "riding the title's span (WJFUN205 / 210 / 212), or a top-level heading whose text is a tile NAME the writer declared in the "
         "`Tab N` side-tab list or the `[Tile title] / X` cells (WJFUN210 / 307), counted together against `min_markers` 2 — builds the "
         "gold's form (21 / 21): a tabs menu (an Overview pane in two columns Knowledge | Practices + one SINGLE-column pane per tile "
         "carrying that tile's `We are learning:` / `I can:` lists), the `div.phases` nav, the introduction ending in a `phaseContainer` "
         "row of `phaseLink` tiles, and one `fundamentalsPanel` per tile opening with the tile title as `<h2>`. Engine: "
         "`ContentConverter.#tilePagesPrepass` (the writer's tiles → the r265 level-pages machinery; the first tile's learning block "
         "re-routed to its pane when the menu partition had taken it; `[Introduction content]` / `[Lesson content]` consumed inside the "
         "dialect only), `InteractiveScanner.#tilePageMarker` (the markers are hard terminators — a widget bundle never swallows one), "
         "`MenuBuilder.#levelTabs` (single-column panes; the level-tabs branch when the menu would otherwise be empty), "
         "`PanelsBuilder.panelTitleLevelPostpass` (`first_heading_level.level_dialect_code_prefixes [\"WJFUN\"]` — the `<h2>` promotion "
         "only on pages the dialect built, so OFF reverts it too). Data `body_region.fundamentals_panels.tile_pages` (patterns, menu, "
         "registry.groups WJFUN|1-3 / 4-6 / 7-8). OFF = the r408 output byte-for-byte (2555 / 2555). ON = exactly the 21 WJFUN overviews, "
         "21 up / 0 down (+257.1pp-sum; the family 37.6 → 49.9%); JPFUN01 / 02 unhelped (no markers). Named KB-over-gold delta: the "
         "tile pane's `<h5>We are learning:</h5>` where the gold ships `<p>` is r349's `lesson_label_form` (D10-9) working as designed. |\n")
s = s.replace(old11, row11 + old11)

# --- §14: the snapshot bullet, prepended above the r409 bullet
old14 = "- **Build:** `260619.80` (round 409 — **the XOTP activity-table template is recognised"
assert s.count(old14) == 1
b14 = ("- **Build:** `260619.81` (round 410 — **the WJFUN \"My Te Kura Writing\" tile-page dialect: a single-file Fundamentals module "
       "laid out as clickable tiles builds the gold's tabs menu + `div.phases` nav + `phaseLink` tile row + one `fundamentalsPanel` per "
       "tile** (built and proven in session 28 Task 3, finished and shipped by the autonomous loop's session 29 Round 1; "
       "`ContentConverter.#tilePagesPrepass` → the r265 level-pages machinery, `InteractiveScanner.#tilePageMarker`, "
       "`MenuBuilder.#levelTabs`, `PanelsBuilder.panelTitleLevelPostpass` `level_dialect_code_prefixes`; data "
       "`body_region.fundamentals_panels.tile_pages`, env `TILEPAGE_OFF`); the probe OFF = disk 2555 / 2555, ON exactly the 21 WJFUN "
       "overviews (21 up / 0 down, +257.1pp-sum, 0 outside the set); **SCOPED regeneration of the 23 WJFUN + JPFUN modules (scoped ship "
       "#2 since the 19 Sept FULL)**; **ROUND 410 BASELINE: SCAFFOLD mean 53.789% / >=50% 1406 / >=75% 236 / >=90% 20 / RAW 37.925% @ "
       "2349 pairs** (53.680 → 53.789 = +0.1095pp; ≥50 +8); compare_structure exact 14091 → 14175 (pool 16414 → 16470) / 186 / 690 / 23; "
       "body 54 / 6 / 190 / 248 EXACT; clean 2504 / 2548, leak 73 / 44 EXACT; every verifier EXACT; 16 selftests GREEN; the WJFUN family "
       "37.6 → 49.9%; the miner 183 → 184 (the three phases-nav rows and two body h2 rows gone, six surfaced beneath)). Previous: ")
s = s.replace(old14, b14 + old14)

open(p, "w", encoding="utf-8", newline="\n").write(s)
print("CLAUDE.md §9 / §11 / §14 updated;", len(s), "chars")
