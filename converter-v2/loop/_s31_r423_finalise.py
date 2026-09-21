#!/usr/bin/env python3
"""r423 finalise (CLAUDE.md §12): changelog entry, Config.js bump, CLAUDE.md §9 / §11 / §14, gate_baseline.json. Run under WSL."""
import re, json
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
PF = R + "pageforge-site/converter-v2/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

entry = """## 2026-09-21 (round 423, build 260619.94) — A PAGE-BOUNDARY MARKER TYPED AS A TABLE ROW IS A PARAGRAPH: PMT101, the MTK "Te Aka Taumatua" template written as ONE table, now converts (the 19 Sept intake's one real recognition gap; the autonomous loop's session 31 Round 1; SCOPED regeneration of the 1 newly-recognised module, the probe proving all 494 others byte-identical)

### 1. WHAT CHANGED

**The defect.** PMT101 (Te Marautanga o Aotearoa, Bilingual) was one of the 20 intake modules with no Claude build, and the only one whose cause was a converter gap rather than a missing source or an un-specified dialect. Its Writers Template is the same MTK "Te Aka Taumatua" bilingual dialect as PNR101 / 102 / 104 / 107 — a two-column English ║ Māori table with the red tags inside the cells — but where PNR107's writer put the page markers (`[MODULE CONTENT: PAGE 1]`, `[END OF PAGE]`, `[LESSON N CONTENT]`, `[END OF DROP DOWN MENU]`) as PARAGRAPHS between one table per page, PMT101's writer kept the whole module in ONE table and typed the markers as ROWS (the red span alone in the left cell, the right cell empty). `DocxExtractor.IsContentStart` reads paragraph blocks only, so no content start was ever seen, `LooksLikeWritersTemplate` said no, and `ModuleResolver.PrepareRun` refused the module as "no Writers Template" (450 red runs in table cells, 3 at paragraph level — the intake handover §7 item 3).

**The fix (a recognition defect, not a gold-matching class; DATA OVER CODE).** `Input_Doc_Rules.content_start.table_row_boundary_markers {enabled, env ROWMARKER_OFF, promote_tags [page, end page, lesson content, end dropdown]}` + `DocxExtractor.PromoteTableRowMarkers(blocks, normaliser, run)`, called first in `ModuleResolver.PrepareRun`'s classify loop (the ONE shared prep choke point — entry parity by construction, `_verify_entry_parity.cjs` PASS). A table ROW whose non-empty cells are each exactly ONE red span resolving to a promote_tags canonical and nothing else splits the table there and the marker is emitted as a paraBlock between the two halves; a slice of the table that is all blank rows (the writer's spacer rows around a marker) is dropped rather than emitted as an empty table — the first such slice sat between `[END OF PAGE]` and `[LESSON 1 CONTENT]` and tripped the splitter's AR-5 (everything after an end page with no paragraph-level heading = boilerplate) on the first build. PMT101's block stream becomes exactly PNR107's shape; recognition, `TrimFrontMatter`, the r212 drop-down rescue, the reoMode page splitter and the bilingual handlers are all untouched. Every other document gets the SAME array back.

### 2. PROOF

- MEASURED first (`outputs/_s31_r1_rowmarkers.cjs`, all 545 docx-bearing gold modules / 762 docx incl. the combined WT + Media List files): marker-only table rows resolving to the four canonicals exist in EXACTLY PMT101 (9 rows: page 1, end page 4, lesson content 3, end dropdown 1) and in no other document. The `[TITLE BAR] ║ [TITLE BAR]` rows of the 19 MTK modules are content rows (the bilingual path already reads them; "title bar" is deliberately NOT a promote tag); ENGS202's page-opener table (a marker beside other cell text, the r306 fence) never qualifies. The refused Writers Templates corpus-wide are the 12 XOTP (no red tags — the next recognition round), PMT101 (this round) and the pre-existing TRR115.
- Unit (`_s31_r423_unit.cjs`): PNR107 / ENGS202 / TRR116 / TRR115 / TRR102 → the SAME array; PMT101 23 → 41 blocks, 9 promoted, `LooksLikeWritersTemplate` false → true, `PrepareRun` ok, moduleCode PMT101, mtkFlag true. Splitter trace (`_s31_r423_split.cjs`): 16 items in PNR107's shape → pages 0.0 / 1.0 / 2.0 / 3.0 = the gold's four files; the trailing `[END OF MODULE]` dropped by AR-5 exactly as PNR107's is.
- `_s31_r423_probe_run.sh` (the r410 harness over all 495 Claude-dir modules): **OFF (`ROWMARKER_OFF`) = the disk on every page, 2555 / 2555, PMT101 "prep refused (no-wt)" — the pre-round state exactly**; **ON = 2559 / 2559 identical, changed 0** — the rule fires on PMT101 alone and changes nothing else.
- PMT101 against its gold on the gate (`_skeleton_compare.py PMT101 PNR107 PNR101`): from NO BUILD to 4 pages at **32.9 % mean scaffold** (overview 66.7 %, lessons 19.7 / 23.5 / 21.9) — inside its Bilingual siblings' band (PNR107 45.2 %, PNR101 52.9 %; the family's known MTK editorial rewrite, KB 07B). The lesson pages are real, family-shaped content (115 `<p>`, 48 images, 1,328 words vs the gold's 1,881); the gold's 3 activity boxes per lesson are the recorded Bilingual embedded-activity class (the r135 parked guard), not this round's.
- SCOPED regeneration (`_s31_r423_regen.sh`: PMT101 + a fresh 12-module spot-check sample): `_content_manifest.py fresh` **0 truly stale**; `_scoped_spotcheck.py verify` **12 / 12 byte-identical**; `scoped_ship.sh` toggle-exists ✓, containment ✓, **PASS**; the ledger at scoped #6 since the r416 FULL (2 of headroom).
- The exact decomposition (`_fastloop_diff.py`, `_s31_r423_fastloop.log` / `_fastloop_named.log`): every moved line is the population growing by PMT101's four pages — sk_pages 2349 → 2353, cs pool 16458 → 16557 (exact +85 / missing +6 = PMT101's own 85 / 0 / 6), body pages 2548 → 2552 (ANY +1 = PMT101_0_0's over-capture of the drop-down-menu table, the MTK overview pattern), defect 2548 → 2552 with all four clean. `_s29_skdelta.py`: **movers 0 (up 0 / down 0), new-only pages 4, gone 0** — not one pre-existing page moved. Accepted as NAMED through the r289 override (`--accept-named "skeleton SCAFFOLD mean %,compare_structure missing container,body_compare ANY breakdown"`).
- `run_all_gates.sh` (`_s31_r423_gates.log`): skeleton state `_s31_r423_sk_final.json` **54.2065 → 54.1703 % @ 2349 → 2353 pairs** (−0.0362pp = (54.2065 × 2349 + 32.9 × 4) / 2353, pure population arithmetic — LOOP §1e), ≥50 **1441 → 1442**, ≥75 238, ≥90 20, RAW 38.229 → 38.193; compare_structure 14255 / 186 / 689 / 23; body 55 / 5 / 190 / 248; clean 2508 / 2552 = 98.28 %; leak 73 / 44 EXACT; tags 9557 / 9557; every verifier ✓; 17 selftests GREEN (49 / 0); feature index GREEN (495 modules); DIFF MINER 182 → 184 CANDIDATE rows (2353 pairs / 484 modules — the two new rows are the `activity MOVED div.col-12 h3 / p` pair, the r381 box-membership tie already dispositioned, pushed over the floor by PMT101's pages; every other row count-shifted +3 / +4 by the same four pages).

### 3. PROTECTED GATES (all HELD on the 2,349-pair pre-existing population, EXACT page for page; the whole-population absolutes RE-BASED to 2,353 pairs — `_s31_r423_gates.log`, `_s31_r423_scoped_ship.log`, `_s31_r423_fastloop_named.log`, `_s31_r423_skdelta.log`)

- **Skeleton (PRIMARY)**: SCAFFOLD **54.1703 % @ 2353 pairs** (the 2349 pre-existing pairs 54.2065 % EXACT — 0 movers; the 4 new pairs enter at 32.9 %); ≥50 **1442** (+1 = PMT101_0_0), ≥75 **238**, ≥90 **20**, RAW **38.193 %**; skipped 0.
- **compare_structure** 14255 / 186 / 689 / 23 (the pre-existing 14170 / 186 / 683 / 23 EXACT; PMT101 adds 85 / 0 / 6 / 0); **body_compare** 55 / 5 / 190 / 248 (pre-existing 54 / 5 / 190 / 247 EXACT; PMT101_0_0 over-capture, named); **defect** clean 2508 / 2552 = 98.28 % (pre-existing 2504 / 2548 EXACT + 4 clean), leak 73 / 44 EXACT; tags 9557 / 9557; every verifier EXACT.
- Plateau (§4): a recognition round (a module entered the population); the window stays at 0 of 3.

"""
p = PF + "BUILD_CHANGELOG.md"; s = rd(p)
head, rest = s.split("\n", 1)
assert head.startswith("# BUILD CHANGELOG") and rest.lstrip("\n").startswith("## 2026-09-21 (round 422")
wr(p, head + "\n\n" + entry + rest.lstrip("\n"))

p = PF + "app/js/Config.js"; s = rd(p)
old = '\tstatic AppVersion = "260619.93";'; assert s.count(old) == 1
note = ("\t// ROUND 423 (260619.94): A PAGE-BOUNDARY MARKER TYPED AS A TABLE ROW IS A PARAGRAPH — PMT101 (the MTK 'Te Aka Taumatua' bilingual template "
        "written as ONE English | Maori table, its [MODULE CONTENT: PAGE 1] / [END OF PAGE] / [LESSON N CONTENT] / [END OF DROP DOWN MENU] markers typed as "
        "rows) was refused as 'no Writers Template' because IsContentStart reads paragraphs only. DocxExtractor.PromoteTableRowMarkers (first in "
        "ModuleResolver.PrepareRun's classify loop) splits a table at every marker-only row and emits the marker as a paragraph, dropping the blank spacer "
        "slices — PMT101's block stream becomes PNR107's shape and everything downstream is unchanged (Input_Doc_Rules.content_start.table_row_boundary_markers, "
        "env ROWMARKER_OFF). Measured over all 762 docx: the trigger fires on PMT101 alone (9 rows). The loop's session 31 Round 1: OFF = disk 2555 / 2555 with "
        "PMT101 refused, ON = 2559 / 2559 (PMT101's four pages, nothing else); PMT101 no build -> 32.9 % mean scaffold (overview 66.7 %); SCOPED regeneration "
        "of the 1 (scoped #6 since the r416 FULL); the 2349 pre-existing pairs EXACT (0 movers), the whole-population mean 54.2065 -> 54.1703 % @ 2353 pairs "
        "= pure population arithmetic, >=50 1441 -> 1442.\n")
wr(p, s.replace(old, note + '\tstatic AppVersion = "260619.94";'))

p = PF + "CLAUDE.md"; s = rd(p)
old9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 421 BASELINE ("; assert s.count(old9) == 1
new9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 423 BASELINE (a page-boundary marker typed as a table row is a paragraph — PMT101, "
        "the one-table MTK template, now converts; `content_start.table_row_boundary_markers`, env `ROWMARKER_OFF`; the population grows by PMT101's 4 pages, "
        "SCOPED regeneration of the 1, the probe proving the other 494 byte-identical; scoped ship #6 since the r416 FULL): SCAFFOLD mean 54.1703% / >=50% 1442 "
        "/ >=75% 238 / >=90% 20 / RAW 38.193% @ 2353 pairs, pairs skipped 0 — the 2349 pre-existing pairs hold r421 EXACTLY (54.2065 %, 0 movers); the mean "
        "moved by population arithmetic alone ((54.2065 × 2349 + 32.9 × 4) / 2353), NAMED and accepted; every other gate EXACT on the pre-existing population "
        "and RE-BASED to 2353 pairs (cs 14255 / 186 / 689 / 23, body 55 / 5 / 190 / 248, clean 2508 / 2552, leak 73 / 44).** "
        "Previous — ROUND 421 BASELINE (")
s = s.replace(old9, new9)
old11 = "| `SIDETABNAV_OFF` | 422 | **THE SIDE-TAB-NAVIGATION FUNDAMENTALS DIALECT"; assert s.count(old11) == 1
row11 = ("| `ROWMARKER_OFF` | 423 | **A PAGE-BOUNDARY MARKER TYPED AS A TABLE ROW IS A PARAGRAPH — PMT101, the MTK \"Te Aka Taumatua\" template written as ONE "
         "table, now converts** (the autonomous loop's session 31 Round 1; a recognition defect — the 19 Sept intake's one real converter gap among the 20 "
         "modules with no Claude build). PNR107 and the other MTK modules carry `[MODULE CONTENT: PAGE 1]` / `[END OF PAGE]` / `[LESSON N CONTENT]` / "
         "`[END OF DROP DOWN MENU]` as paragraphs between one English ║ Māori table per page; PMT101's writer kept the whole module in one table and typed the "
         "markers as rows (the red span alone in the left cell), so `IsContentStart` (paragraphs only) never saw a content start and `PrepareRun` refused the "
         "module. `Input_Doc_Rules.content_start.table_row_boundary_markers {enabled, env, promote_tags [page, end page, lesson content, end dropdown]}` + "
         "`DocxExtractor.PromoteTableRowMarkers`, called first in `ModuleResolver.PrepareRun`'s classify loop: a row whose non-empty cells are each exactly one "
         "red span resolving to a promote tag splits the table there, the marker becomes a paraBlock, an all-blank slice is dropped (it would trip the "
         "splitter's AR-5). Measured over all 762 docx: PMT101 alone (9 rows); `title bar` deliberately not a promote tag (the 19 MTK `[TITLE BAR] ║ [TITLE "
         "BAR]` content rows). OFF = the r422 output (2555 / 2555, PMT101 refused). ON = PMT101's four pages (no build → 32.9 % mean scaffold, overview 66.7 %), "
         "nothing else. Recorded: the XOTP activity-table family (12 modules, no red tags) is the remaining recognition round; TRR115 stays refused (pre-existing). |\n")
s = s.replace(old11, row11 + old11)
old14 = "- **Build:** `260619.93` (round 422 — **the side-tab-navigation"; assert s.count(old14) == 1
b14 = ("- **Build:** `260619.94` (round 423 — **a page-boundary marker typed as a table row is a paragraph: PMT101, the one-table MTK template, now "
       "converts** — `Input_Doc_Rules.content_start.table_row_boundary_markers`, env `ROWMARKER_OFF`; `DocxExtractor.PromoteTableRowMarkers` first in "
       "`ModuleResolver.PrepareRun`; the autonomous loop's session 31 Round 1; the probe OFF = disk 2555 / 2555 with PMT101 refused, ON = 2559 / 2559; "
       "**SCOPED regeneration of the 1 (scoped ship #6 since the r416 FULL)**; **ROUND 423 BASELINE: SCAFFOLD mean 54.1703% / >=50% 1442 / >=75% 238 / "
       ">=90% 20 / RAW 38.193% @ 2353 pairs** — the 2349 pre-existing pairs EXACT (0 movers), PMT101's 4 pages enter at 32.9 %; cs 14255 / 186 / 689 / 23, "
       "body 55 / 5 / 190 / 248, clean 2508 / 2552, leak 73 / 44; every verifier EXACT; 17 selftests GREEN; the miner 182 → 184 (the r381 MOVED pair over the "
       "floor by PMT101's pages); the corpus is now 2559 pages / 495 dirs). Previous: ")
s = s.replace(old14, b14 + old14)
wr(p, s)

p = R + "CONVERTER_V2/reference/tests/gate_baseline.json"; s = rd(p)
def setv(key, old, new):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=1); assert n == 1, key
setv("build", '"260619.93"', '"260619.94"'); setv("round", 422, 423); setv("date", '"2026-09-20"', '"2026-09-21"')
setv("claude_pages", 2606, 2610); setv("paired_pages", 2349, 2353); setv("gated_dirs", 484, 485)
setv("mean_scaffold_pct", 54.21, 54.17); setv("median_scaffold_pct", 55.2, 55.3); setv("pages_ge_50", 1441, 1442)
setv("pairs", 2349, 2353)
setv("exact_chain", 14170, 14255); setv("claude_missing_container", 683, 689)
setv("any_breakdown", 247, 248); setv("over_capture", 54, 55)
setv("clean_pages", 2504, 2508); setv("total_pages", 2548, 2552); setv("clean_pct", 98.27, 98.28)
a = '    "_note_r422": "Round 422 (session 30 Round 5)'; assert s.count(a) == 1
s = s.replace(a, '    "_note_r423": "Round 423 (session 31 Round 1): a page-boundary marker typed as a table row is a paragraph — PMT101 (the one-table MTK template) recognised and built (Input_Doc_Rules.content_start.table_row_boundary_markers, env ROWMARKER_OFF; DocxExtractor.PromoteTableRowMarkers first in PrepareRun). THE POPULATION GREW: paired 2349 -> 2353 (PMT101_0_0 / 1_0 / 2_0 / 3_0 at 66.7 / 19.7 / 23.5 / 21.9 = 32.9 % mean). Every whole-population absolute below is RE-BASED to 2353 pairs; the 2349 pre-existing pairs reproduce r421 EXACTLY (0 movers — _s31_r423_skdelta.log), so a metric that looks lower than the r421 line is population arithmetic, not a regression (LOOP §1e). SCOPED regeneration of the 1 (scoped #6 since the r416 FULL); the probe proving the other 494 byte-identical.",\n' + a)
a2 = '    "_note_r420b": "Round 421: SCAFFOLD 54.2067'; assert s.count(a2) == 1
s = s.replace(a2, '    "_note_r421b": "Round 423: SCAFFOLD 54.2065 -> 54.1703 @ 2349 -> 2353 pairs (-0.0362pp = (54.2065 x 2349 + 32.9 x 4) / 2353 — the 4 PMT101 pages entering, 0 movers on the pre-existing pairs, NAMED), >=50 1441 -> 1442 (PMT101_0_0), >=75 238 / >=90 20 EXACT, RAW 38.229 -> 38.193, median 55.2 -> 55.3.",\n' + a2)
b2 = '    "_note_r421": "Round 421: 14170 / 186 / 683 / 23 EXACT.",'; assert s.count(b2) == 1
s = s.replace(b2, '    "_note_r423": "Round 423: exact 14170 -> 14255 (+85), MISSING 683 -> 689 (+6) = the text-matched pool 16458 -> 16557 (+99) — all PMT101\'s own four pages (85 / 0 / 6 / 0); the pre-existing 14170 / 186 / 683 / 23 EXACT.",\n' + b2)
b3 = '    "_note_r421": "Round 421: over-capture 54 / runaway 5 / EMPTY 190 / ANY 247 EXACT.",'; assert s.count(b3) == 1
s = s.replace(b3, '    "_note_r423": "Round 423: over-capture 54 -> 55 / ANY 247 -> 248 = PMT101_0_0 (the drop-down-menu table captured as a widget, the MTK overview pattern — named); runaway 5 / EMPTY 190 EXACT; pages 2548 -> 2552.",\n' + b3)
b4 = '    "_note_r410": "Round 410: clean 2504 / 2548 = 98.27, leak 73 occ / 44 pages — EXACT.",'; assert s.count(b4) == 1
s = s.replace(b4, '    "_note_r423": "Round 423: clean 2504 / 2548 -> 2508 / 2552 = 98.28 (PMT101\'s four pages all clean), leak 73 occ / 44 pages EXACT.",\n' + b4)
wr(p, s); json.load(open(p, encoding="utf-8"))
print("r423 finalise: changelog + Config.js 260619.94 + CLAUDE.md §9/§11/§14 + gate_baseline.json done")
