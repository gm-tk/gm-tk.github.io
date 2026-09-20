# Message for Claude Code — pre-loop fixes

**Where to paste this:** open Claude Code in `C:\Users\Gavin\TeKura\FINAL_MODULE_DATA` and
paste everything below the line. Do NOT prefix it with `/pageforge` — that command exists only
in Cowork. This folder's `.claude/skills/` provides `/loop-start`, `/loop-stop`, `/loop-review`
and `/loop-decisions` only, and Claude Code reads `CLAUDE.md` from the folder root on its own,
so no router command is needed.

---

Before the autonomous loop restarts, four things need doing. The 98-module September intake
landed on 19 Sept (see `LOOP_INTAKE__2026-09-19_98_Modules.md` and
`NEW_MODULES__Intake_2026-09-19.md`), the corpus was fully regenerated at build 260619.78, and
every protected gate was re-proved. But the mined registries were never rebuilt, so the engine
and the UI are both still working from the pre-intake library of 454 modules.

Work in the order below — tasks 1 and 2 are prerequisites for the loop, task 3 is the largest
accuracy win available, task 4 is optional if time runs short.

## Task 1 — rebuild the mined registries over the 552-module gold corpus (do this first)

**The problem, measured.** The Reference-module picker on the HTML Generator tab reads
`ReferenceMiner.ListLibraryCodes()` → `DataService.Data.ModuleStructureIndex.module_meta` →
`converter-v2/data/Module_Structure_Index.json`. That file holds **exactly 454 module entries
and none of the 98 new ones**, which is why the panel still reads "Showing 45 of 454 library
modules". `Module_Feature_Index.json` is in the same state — 454 modules, 0 of the 98.

**This is not a cosmetic UI problem.** `module_meta` is, in its own words, "the substrate the
6-level precedence cascade (`granular_consensus.resolve`) filters over". While the 98 are
absent, the cascade cannot see any of them as a sibling, so every future conversion in those
subjects and series is resolved against an incomplete library. **Rebuilding this is the
highest-value accuracy fix available that needs no new logic.**

What to do:

1. Find the builder that writes `Module_Structure_Index.json` (it is mined from the gold
   corpus — "Rebuilt with the registry" per its own `_meta`) and re-run it over all **552**
   gold dirs. Confirm `module_meta` reaches 552 and that all 98 new codes are present.
2. **Re-mine the sibling registries in the SAME round** — `Style_Anchor_Registry.json`,
   `Menu_Scaffold_Registry.json`, `Granular_Scaffold_Registry.json` (see
   `reference/tests/build_granular_registry.py`), `Scaffold_Consensus.json`, and
   `Module_Feature_Index.json` (`reference/tests/build_feature_index.cjs`).
   **This is the round-263 STALE-REGISTRY trap:** that round shipped the SCCH302 missing-menu
   bug precisely because the index was rebuilt while the Style-Anchor and Menu registries were
   not re-mined. Do not repeat it. If any registry cannot be rebuilt this round, say so
   explicitly rather than shipping a half-mined set.
3. **The subject labels need a decision.** The library has never seen **29 of the new
   prefixes**: ANZHFUN, CBI, CHI, CHWHA, COM, DAN, DTC, ENO, FRFUN, FRNO, GENO, GEO, GER,
   GEWHA, JPFUN, JPN, MUS, MXS, PMT, PWY, PWYWHA, SAM, SCBI, SCES, SPA, WJFUN, XOTPB, XOTPG,
   XOTPO. The Subject dropdown currently offers 16 labels (1-10 Arts, 1-10 English, NCEA1,
   ConnectED, …). A module whose `subject` comes back blank still appears under "All subjects"
   but is **not offered as a filter entry** — deliberate, per Gavin's "no Unclassified in the
   list". So work out where the prefix → subject mapping is sourced (check
   `00_Module_Template_Map.md` and `outputs/_build_module_template_map.py` first), extend it,
   and **report the label you propose for each new prefix before finalising** — several are
   Languages (CHI, JPN, SPA, GER, FRNO, GENO, SAM, FRFUN, JPFUN) and that grouping is Chris's
   call, not yours. Do not invent a label silently.
4. Re-check the panel afterwards: the count should read 552, the Subject dropdown should gain
   the new subjects, and the Template dropdown should still offer exactly Standard / Inquiry /
   Fundamentals / Bilingual.

Registry data changes affect output, so this needs the normal proof: a regeneration of the
affected modules and the full gate suite. **REGENERATE CORPUS** is authorised for this task at
whatever scope the change actually touches — state the resolved list and its size before
running it.

## Task 2 — the XOTP parsing on the Module Development tab

**Check the assumption first — I think the parser is already fine.** Running the V1 parser
over `XOTPB08 Writers Template.docx` produces a complete, faithful dump: the two-column
`Section heading ║ Text/Activity` table with every row, the `CS:` line correctly marked as
`🔴[RED TEXT]…[/RED TEXT]🔴`, the images as `[IMAGE: image2.png]`, and the Drive/Docs links
resolved. Nothing is lost.

The only thing it emits is:

```
⚠ [TITLE BAR] marker not found. Showing all extracted content.
```

which is the correct fallback, not a failure. So:

- **Do not rewrite the parser.** Verify my finding on two or three more XOTP docs
  (XOTPG01 and XOTPO01 are the other variant), and if it holds, the fix is only to the
  **message**: recognise the activity-table shape (a table whose header row is literally
  `Section heading` | `Text/Activity` — present in all 12 and nothing else in the corpus) and
  say so plainly, e.g. "Activity-table template detected — no [TITLE BAR] expected", instead of
  a warning that reads like breakage.
- **The real gap is in the converter, not the parser.** `ModuleResolver.PrepareRun` rejects
  these 12 modules outright with "no Writers Template (no content opener found)", because
  `DocxExtractor.LooksLikeWritersTemplate` requires a paragraph-level red opener. That is
  task 4 and it is a different piece of work.

## Task 3 — the WJFUN / JPFUN single-file page model (the accuracy round)

This is the biggest converter-accuracy lever in the corpus right now, and it is **data-only,
no code**.

21 WJFUN modules plus JPFUN01 and JPFUN02 ship **one** human page each; the converter builds
2–5. Mean SCAFFOLD across them is **10.4 %** and they hold **17 of the worst 25 module scores
corpus-wide**. This is the documented `page_model: "single-file"` class (r106 / r186,
`MTKPAGE_OFF`) — the family simply has no registry entry. It is the same finding the 3 Aug
intake recorded for CHFUN, which was then fixed; use that as the worked precedent.

The freshly re-mined `DIFF_QUEUE.md` (19 Sept, 2,349 pairs, 188 candidates) independently
confirms it: WJFUN is the best group on **seven** separate new chrome candidate rows —
`header:chip=decimal-number` EXTRA (c=1.00, n=20), `header:chip=module-code` MISSING (c=1.00,
n=20), `nav:phases` MISSING (c=1.00, n=21), `footer:links=home-nav` MISSING (c=1.00, n=21),
`footer:links=prev-lesson,home-nav` EXTRA (c=1.00, n=11) and two `title-h1-count` rows. Those
are not seven problems. Once the converter splits one gold page into four, every invented page
carries a wrong header chip, no phases nav and the wrong footer links. **Fix the pagination and
expect all seven to collapse together — do not chase them individually.**

Follow the normal disciplined loop: triangulate three named modules, measure the class
corpus-wide before coding, ship behind a data flag and an env toggle, prove the gates.
**REGENERATE CORPUS - the WJFUN and JPFUN modules** is authorised.

## Task 4 — recognition fixes, if time allows

Both are refusals, so both are pure gain — nothing currently built can regress.

- **PMT101** — a fully table-laid-out Te Aka Taumatua bilingual template.
  `LooksLikeWritersTemplate` needs a paragraph-level opener; PMT101 has 450 red bracket runs
  inside table cells and only 3 at paragraph level (`[tags]`, `[Content for DROP DOWN MENU]`).
  PNR107 (11 paragraph-level, incl. `[MODULE CONTENT: PAGE 1]`) and TRR116 (22, incl.
  `[Lesson 2]`) convert fine. Round 212 already recorded this family's shape and rescued the
  **trim** step; recognition was never extended. Either let the check look inside table cells
  for `[TITLE BAR]`, or admit `[Content for DROP DOWN MENU]` as an opener for this family —
  r212 already treats it as the rescue anchor, so the second is smaller.
  **Already ruled out — do not re-investigate:** a UTF-8 BOM (30 of the corpus's 762 docx carry
  one and convert fine) and red-hex case (`DocxExtractor` line 1477 already lower-cases it).
- **The XOTP family** — 12 modules, full spec in
  `00-NEW_NEW_NEW/_SPEC__XOTP_Activity_Table_Template.md`. Round 1 is recognition only (a new
  `input_shapes.activity_table` with the header-row detector); round 2 is the adapter. Both are
  output-inert for the existing corpus because nothing else carries that table. Note the trap
  in the spec: the section heading must be the primary trigger, not the `CS:` line — all six
  G/O-variant modules have no `CS:` lines at all.

## Rules for the session

- Read `CONVERTER_V2/CLAUDE.md` §0, §2, §5, §9–§12 and the top of `BUILD_CHANGELOG.md` first.
- DATA OVER CODE; every new behaviour behind a data flag **and** an env toggle.
- Ship only if every protected gate holds-or-improves on a 0-stale regen.
- **The gate baseline was re-based on 19 Sept to the whole 2,349-pair population.** If a metric
  looks like it dropped, split it by population before concluding anything — the pre-existing
  1,956 pairs reproduce round 407 exactly, and the method is written up in
  `gate_baseline.json._meta._note_intake_2026_09_19`.
- **`_gatecheck.py` prints cached rows for gates it did not run.** Always run `cs bc` before
  believing the compare_structure or body_compare lines — this nearly produced a false
  regression verdict on 19 Sept.
- `_regen_safe.sh` now honours `REGEN_TIMEOUT` (default 40). Batches of 11 modules are
  reliable; the 22-module batches `_batch_plan.py` emits are not.
- Commit after each round. **Never push** — leave copy-ready push instructions instead.
- Correct the stale census in `LOOP_STATE.md` while you are in there: 2,613 Claude pages /
  494 Claude dirs / 552 gold dirs / 762 docx, ledger at FULL #0, ceiling and
  `COVERAGE_DASHBOARD.md` both unmeasured on this corpus.

## Report back

For each task: what changed, the before/after numbers in plain English, which gates moved and
by how much, and anything you had to decide. Flag the subject-label proposals from task 1
separately — I want to approve those before they are final.
