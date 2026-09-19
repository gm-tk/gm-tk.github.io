## 2026-09-19 (round 405, build 260619.76) — THE JOURNAL SECTION IS AN ACTIVITY BOX: a free heading whose section ends in a go-to-journal button is re-tagged as a bare `[Activity]` opener in English / Leaving to Learn, where the gold boxes it (the autonomous loop's session 27 Round 10; **a FULL regeneration of all 416 — the ledger's backstop after seven scoped ships — 0 stale, the manifest diff = the round's 11 pages exactly, no residue from r397–r403**; a small ship under the 20-page floor on the r320 precedent)

### 1. WHAT CHANGED

**The class (Round 6's `_s27_r6_journalsec.py`).** A writer types `[H3] Title` + prose + `[button] Go to journal` with no `[Activity]` opener; Claude ships the section free (h3 + p + the r239 `h4.goJournal` in the page column); the gold's developer boxes the task — a numbered `div.activity` holding the h3 title, the prose and the goJournal h4. Over every free heading section on Claude's paired pages that carries a journal / activity-id button (115): the gold BOXES it in **1-10 English 15 / 17 = 0.88** and **Leaving to Learn 9 / 10 = 0.90**; NCEA1 0.50 and Mathematics 0.45 are ties, EXPlore's gold drops the heading (0.68 absent), ConnectED 0.45 — none listed.

**The fix (DATA OVER CODE, one env `JOURNALBOX_OFF`).** `Interactive_Boundary_ChildTag_Bank._meta.opener_rule.id_heading_opener.journal_section {enabled, env, subjects, heading_tags, stop_tags, max_items, _doc}`; `InteractiveScanner.#idHeadingOpeners` (the r364 / r377 re-tagger) — when the module's `module_meta` subject is listed, a free h2–h4 heading whose section (the items before the next heading / `[Activity]` / section marker / PAGE or CONTAINER directive / INTERACTIVE invocation / table) carries a `[button]` that `#isGoJournalButton` recognises is re-tagged in place as a bare `[Activity]` opener: the heading's own words become the box title (the r66 standalone title), the r400 positional letter numbers the box, r239 ships the button as the goJournal h4 inside it. A heading directly after a writer's `[Activity]` opener is that box's title and is never re-tagged; a section led by a table is a widget's and is left alone. OFF = the r404 output (probe 2109 / 2109).

### 2. PROOF

- `_s27_r405_probe.cjs` + `_s27_r405_probe_run.sh`: **OFF = disk 2109 / 2109**; ON = **11 pages / 5 modules changed** (ENGC301, XGF9001 / 9003 / 9004 / 9006), 2098 identical.
- `_s27_r405_pagescore.py` (the gate's own `match()` on the probe's ON pages BEFORE regenerating): 9 changed paired pages — **up 6 / down 3 / same 0; pp-sum +6.3** (XGF9006_4_0 +2.3, ENGC301_6_0 +2.3, XGF9001_4_0 +0.8, XGF9003_1_3 +0.8; the dips ≤ 0.3).
- **THE FULL REGENERATION** (`_s27_r405_fullship_par.sh`, the r396 36-batch list, 4 workers, all rc 0, ≈5 min): `_stalecheck.sh` **0 stale**; `_content_manifest.py diff` vs the r403 snapshot = **11 pages / 5 modules changed, 0 added / 0 removed — exactly the probe's set, so the seven scoped ships r397–r403 left no residue**; **probe ON == regenerated disk 47 / 47 pages** over the 5 modules.
- `_s27_r405_skdelta.py`: 9 movers, 6 up / 2 down, **0 outside the affected set**.

### 3. PROTECTED GATES (all HELD-or-IMPROVED)

- **Skeleton (PRIMARY)**: SCAFFOLD **53.998 → 54.001 % (+0.0032pp)**; ≥50 **1175**; ≥75 **200**; ≥90 **18** — EXACT; RAW **38.006 → 38.008 %**; 1956 pairs / 0 skipped (state `outputs/_s27_r405_sk_final.json`). Dips: XGF9006_2_0 −0.3, XGF9006_6_0 −0.2 (the scorer's alignment on a page whose later boxes re-letter — named).
- **compare_structure** exact 11798 → **11796 / EXTRA 172 / MISSING 626** — the −2 is the text-matched POOL 13816 → 13814 (the boxed h3 / goJournal lines leaving the pool, the r344 relocation class; EXTRA and MISSING EXACT); **body_compare** 42 / 4 / 173 / 218 EXACT; structural-defect **clean 2079 / 2102, leak 26 / 23** EXACT; tags 9557 / 9557; every widget verifier RESULT identical to r403; 15 selftests + the feature-index selftest GREEN (46 PASS / GREEN lines).
- Ship ledger: **FULL ship recorded, the scoped-since counter reset to 0**; content manifest + fast-loop baselines re-snapshotted; feature index `--rehtml` + `--merge` + `--selftest` GREEN.
- DIFF MINER re-mined on the r405 corpus: 169 CANDIDATE rows, nothing gone, nothing new.
- Plateau: +0.0032pp with no other protected gate moving — the window's 2 of 3 (r404 the declined-inert 1).

### 4. RECORDED, NOT TAKEN

- The bracket-less red `Activity 4A` opener line (ENGI102 lesson 8's `🔴Activity 4A🔴` + `[H4] Check your understanding` + a red instruction + the answer table — the gold's box 4A with a built dragAndDrop): 36 sites / 14 modules in the parsed WTs, 8 tracked — the r148 BARELEAD class for the activity opener, under the floor.
- The NCEA1 / Mathematics journal sections (ties) and EXPlore's heading-less form stay free.
