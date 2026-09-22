#!/usr/bin/env python3
"""Session 34 §5d condense (22 Sept 2026 ≈14:20 NZST): LOOP_STATE.md reached 105 KB (over the 100 KB target) when the r428 PICK was
written. The eight s30 / s31 Round-log lines at 770–1,720 characters (the 22 Sept review queued them for "the next finalise") move
VERBATIM to LOOP_STATE_ARCHIVE.md 'Round-log lines s30–s31' and are replaced by ≤ 500-character lines here. No decision deleted.
Run under WSL: python3 _s34_condense.py
"""
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)
st = rd(R + "LOOP_STATE.md"); ar = rd(R + "LOOP_STATE_ARCHIVE.md")
short = {
 "- s31-r3 (engine r425, build 260619.96, BUILT + SHIPPED INERT": "- s31-r3 (engine r425, build 260619.96, BUILT + SHIPPED INERT, 21 Sept ≈20:12 → ≈22:00, ended by `/loop-stop`) · THE XOTP ACTIVITY-TABLE ADAPTER — `DocxExtractor.AdaptActivityTable` + the family conventions (bare box, repeated lesson h1, the alert variant by prefix, the ITEM menu `ITEMMENU_OFF`); the 12 build 24 pages at 35.6–63.1 %; `adapter.enabled: false` at the stop, OFF 78 / 78 canary pages identical; finished as s33-r1. Same commit: `CLAUDE.md` (1.3 MB) → `OPERATING_GUIDE.md`. Full text: archive 'Round-log lines s30–s31'.",
 "- s31-r2 (engine r424, build 260619.95, output-inert": "- s31-r2 (engine r424, build 260619.95, output-inert, 21 Sept ≈19:58 → 20:12) · THE ACTIVITY-TABLE WRITERS TEMPLATE IS RECOGNISED — the 12 XOTP reader documents (no red tags; a `Section heading | Text/Activity` table) detected by `DocxExtractor.IsActivityTableDoc` (`input_shapes.activity_table`, `ACTTABLE_OFF`), refused BY NAME until the adapter; exactly the 12 of 762 docx · SHIPPED · probe ON = 2559 / 2559, no regeneration; every gate as at r423 · plateau 0 of 3. Full text: archive 'Round-log lines s30–s31'.",
 "- s31-r1 (engine r423, build 260619.94": "- s31-r1 (engine r423, build 260619.94, 21 Sept ≈19:18 → 19:55) · A PAGE-BOUNDARY MARKER TYPED AS A TABLE ROW IS A PARAGRAPH — PMT101's one-table MTK template refused as \"no Writers Template\"; `DocxExtractor.PromoteTableRowMarkers` (`content_start.table_row_boundary_markers`, `ROWMARKER_OFF`); PMT101 alone of 762 docx · SHIPPED · OFF = disk 2555 / 2555, ON 2559 / 2559; PMT101 32.9 % (4 pages) · SCOPED regen of the 1 (scoped #6) · skeleton 54.2065 → 54.1703 % @ 2349 → 2353 (population arithmetic, 0 movers) · miner 182 → 184 · plateau 0 of 3. Full text: archive 'Round-log lines s30–s31'.",
 "- s30-r1 (engine r419, build 260619.90": "- s30-r1 (engine r419, build 260619.90, 21 Sept ≈15:40 → 16:50) · THE LANGUAGE-FONT WRAP — every CJK run takes `span.ch-text` / `span.jp-text` (KB constraint 92 / CL-0093; `ListsAndRuns.LanguageFontWrap`, `body_region.language_fonts`, `LANGFONT_OFF`; the gold 0.99, Claude 3,812 bare runs on 26 pages / 14 modules) · SHIPPED · OFF = disk 2555 / 2555, ON 25 pages / 13 modules (13 up / 7 down, +49.7pp-sum, the JPN1004 dips named) · SCOPED regen of the 13 (scoped #3) · skeleton 54.186 → 54.207 (+0.0212pp), ≥50 +2 · miner 183 → 182 · plateau 0 of 3. Full text: archive 'Round-log lines s30–s31'.",
 "- s30-r5 (engine r422, build 260619.93, DECLINED-INERT": "- s30-r5 (engine r422, build 260619.93, DECLINED-INERT, no regen, 21 Sept ≈18:32 → 18:50) · THE SIDE-TAB-NAVIGATION FUNDAMENTALS DIALECT — FRFUN06's `[Side tab navigation]` + label table + one labelled nav tag per panel → the gold's `div.phases` + `fundamentalsPanel`s (`inquiry_tabs.side_tab_nav`, `SIDETABNAV_OFF`); FRFUN06 10 / 10 pages 8 up / 2 down, +34.7pp-sum · shipped INERT under the floor (Chris's call; enabled by rule as s33-r2) · corpus byte-identical · plateau 0 of 3. Full text: archive 'Round-log lines s30–s31'.",
 "- s30-r4 (engine r421, build 260619.92": "- s30-r4 (engine r421, build 260619.92, 21 Sept ≈18:05 → 18:30) · THE REGISTRY-KNOWN MODULE CODE — CHWHA / GEWHA / ANZHFUN05 / PWYWHA1 could not be named by the one regex; a filename token `module_meta` knows is now a candidate (`module_code_detection.registry_token`, `CODEREG_OFF`) · SHIPPED · OFF = disk 2555 / 2555, ON exactly the 4 (renamed; CHWHA +2.9, the other three −0.1 / −1.9 / −1.5 named) · SCOPED regen of the 4 (scoped #5) · skeleton −0.0002pp named · F23 decomposed (FRFUN multi-file, JPFUN alias, MXFUN dual-build) · plateau 0 of 3. Full text: archive 'Round-log lines s30–s31'.",
 "- s30-r3 (no engine change, 21 Sept ≈17:40 → 18:05) · PICK PASS": "- s30-r3 (no engine change, 21 Sept ≈17:40 → 18:05) · PICK PASS on the r420 corpus — nine instruments, nothing at the floor: the selfCheck kickoff's other shapes (quiz-engine; wordSelect 5), the two-column padding 0.30, the missing `div.button` (diffuse; the journal button needs-Chris), the writer's bold by context, the Sassoon font (widgets only), the gold's alertActivity (diffuse), the unclassified one-table bundles (905, diffuse), the dragAndDrop header-red tables (25 sites, no form ≥ 0.60) — `_s30_r3_*.py` · plateau 0 of 3. Full text: archive 'Round-log lines s30–s31'.",
 "- s30-r2 (engine r420, build 260619.91": "- s30-r2 (engine r420, build 260619.91, 21 Sept ≈16:55 → 17:45) · THE LETTER-GRID BINGO — the BLL `[Self check]` letter table builds the KB's 03E bingo (`InteractiveBuilder.#letterGridBingo`, `letter_grid_bingo`, `BINGO_OFF`; D10-3's selfCheck shape 1, 55 tables / 9 modules; NEW gate `_verify_bingo.cjs` 52 grids / defect 0) · PICK pass first: pinyin below floor, `div.alert.solid` KB-correct, the widened wrapper declined · SHIPPED · OFF = disk 2555 / 2555, ON 7 pages · SCOPED regen of the 7 (scoped #4) · scaffold −0.0005pp named (the r289 marker class); selfCheck still-a-box 215 → 163 · plateau 0 of 3. Full text: archive 'Round-log lines s30–s31'.",
}
moved = []
lines = st.split("\n")
for i, l in enumerate(lines):
    for k, v in short.items():
        if l.startswith(k):
            assert len(v) <= 700, (k, len(v))
            moved.append(l); lines[i] = v; break
assert len(moved) == 8, len(moved)
st = "\n".join(lines)
sec = "\n## Round-log lines s30–s31 (verbatim, the eight over-cap lines archived from LOOP_STATE.md 2026-09-22 ≈14:20 NZST, session 34 §5d condense — each replaced by a ≤ 500-character line there)\n\n" + "\n".join(moved) + "\n"
assert "## Round-log lines s30–s31" not in ar
wr(R + "LOOP_STATE_ARCHIVE.md", ar.rstrip("\n") + "\n" + sec)
wr(R + "LOOP_STATE.md", st)
print("condensed 8 lines; LOOP_STATE.md now", len(st.encode("utf-8")), "bytes")
