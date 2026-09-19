## 2026-09-20 (round 409, build 260619.80) — THE XOTP ACTIVITY-TABLE TEMPLATE IS RECOGNISED BY THE MODULE DEVELOPMENT TAB'S PARSER AND SAID SO PLAINLY (session 28, pre-loop Task 2; **V1-parser message only — no engine / data / output change, no regeneration; the r408 baselines stand**)

### 1. THE ASSUMPTION, CHECKED FIRST — the parser was already fine

Chris's finding held on the other variant too. The V1 parser (`pageforge-site/js/docx-parser.js` + `formatter.js`, the Module Development tab; the harness runs the same files through `outputs/parse_docx.cjs`) was run over **all 12** XOTP Writers Templates: every dump is complete and faithful — the two-column `Section heading ║ Text/Activity` table with every row (13 rows + the nested "I can" self-assessment table), the `CS:` line marked `🔴[RED TEXT]…[/RED TEXT]🔴` where the B variant has one, images as `[IMAGE: imageN.png]`, the Drive / Docs links resolved. Nothing lost. The only thing it emitted was `⚠ [TITLE BAR] marker not found. Showing all extracted content.` — the correct fallback for a document with no red tags, but a warning that reads like breakage. **The parser was NOT rewritten.**

### 2. WHAT CHANGED — the message

`OutputFormatter.formatContent` (`pageforge-site/js/formatter.js`): when the `[TITLE BAR]` opener is missing AND the document is the activity-table dialect, the line reads **`ℹ Activity-table template detected (a "Section heading | Text/Activity" table, no red tags) — no [TITLE BAR] expected. Showing all extracted content.`** The detector `_isActivityTableDoc` looks for a table whose first `scan_rows` (3) rows hold exactly two cells folding to `section heading` | `text/activity` — the header row is the SECOND row of every XOTP table (the first is the merged title row). It is the header row and never the `CS:` line that triggers it (the six G / O modules have no `CS:` lines at all). Data-shaped switch `OutputFormatter.ACTIVITY_TABLE_NOTICE {enabled, header, scan_rows, message}`; A/B toggle `window.PF_ACTIVITY_TABLE_NOTICE_OFF` (the V1 site has no env).

**Uniqueness, measured over the whole corpus:** `Section heading ║ Text/Activity` appears in **exactly the 12 XOTP parsed Writers Templates and nowhere else in the 762 documents** (`Section heading` alone occurs once more, in PWY1009, without the second cell — the pair is the discriminator).

### 3. PROOF (`outputs/_s28_t2_verify.sh` — the harness parser, WSL)

- **All 12 XOTP Writers Templates**: the re-parsed dump differs from the corpus `_parsed.txt` in **exactly that one line** (the notice replaces the warning) — every other byte identical, which is also the proof that nothing else in the parser moved.
- **Genuine no-`[TITLE BAR]` controls keep the warning byte-for-byte**: PMT101 (Writers Template + Media List), PNR107, TRR102 Media List.
- **Normal documents byte-identical**: SCCH301 (WT + Media List), WJFUN105 (WT + Media List).
- The 12 corpus `_parsed.txt` files for XOTPB08–13 / XOTPG01, 03–06 / XOTPO01 were refreshed with the new line (gold-side derived inputs; no Claude output exists for the family, so no gate can move).
- Harness note: `parse_docx.cjs` needs `jszip` + `@xmldom/xmldom` under `$PF_NODE_MODULES` (default `$HOME/pfdeps/node_modules`); they were installed in the WSL home on this machine (outside the connected folder).

### 4. THE REAL GAP IS THE CONVERTER (Task 4)

`ModuleResolver.PrepareRun` still refuses all 12 with "no Writers Template (no content opener found)" because `DocxExtractor.LooksLikeWritersTemplate` needs a paragraph-level red opener. That is a different piece of work — the recognition round (`input_shapes.activity_table` + this same header-row detector on the engine side) and then the adapter; spec `00-NEW_NEW_NEW/_SPEC__XOTP_Activity_Table_Template.md`.

