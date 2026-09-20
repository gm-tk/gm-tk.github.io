# Session 28 — pre-loop fixes: what was accomplished (20 September 2026)

**Session type:** interactive Claude Code session (Opus 5), NOT a loop session. Kickoff: `NEXT_SESSION__Pre_Loop_Fixes.md` — four tasks to run before the autonomous dev loop restarts.
**Outcome in one line:** Tasks 1 and 2 (the work the loop cannot do for itself) are **done and committed**; Task 3 (a converter round of the loop's own shape) was **built and proven but deliberately stopped before shipping** at Chris's instruction and handed to the loop; Task 4 was **not started**. The corpus on disk is back at the last shipped state. Nothing has been pushed.

---

## 1. Plain-English summary

| Task | What it was | Status |
|---|---|---|
| **1 — rebuild the mined registries over the 552-module gold corpus** | The converter's "what does this family's HTML normally look like" registries were built from 454 modules; the September intake added 98 more (now 552). Every registry was re-mined in one pass so a new family is never half-known (the round-263 stale-registry trap). | **SHIPPED — round 408, build 260619.79, commit `91bc066`.** Subject labels for 29 new module-code prefixes are **PROPOSED, awaiting Chris's approval** (§4 below). |
| **2 — XOTP on the Module Development tab** | The 12 XOTP documents are an "activity-table" template (a table headed *Section heading \| Text/Activity*) with no `[TITLE BAR]`; the parser already handled them but printed a misleading "marker not found" warning. Only the message changed. | **SHIPPED — round 409, build 260619.80, commit `222adaf`.** |
| **3 — WJFUN / JPFUN single-file "tile pages"** | The 21 WJFUN writing modules lay a module out as clickable tiles; round 408 had already fixed their page count (one page each, 10.4 % → 37.6 %). This round taught the converter the tile dialect itself (tile navigation, one panel per tile, the tile learning intentions in the menu). | **BUILT AND PROVEN, NOT SHIPPED.** Stopped mid-round at Chris's request; code left uncommitted, corpus rolled back, full handover written into `LOOP_STATE.md`. |
| **4 — recognition fixes (PMT101 opener; XOTP recognition round 1)** | "If time allows." | **Not started.** |

**Why the stop.** Chris pointed out that this session had drifted from the pre-loop tasks into ordinary converter rounds — the loop's own job, with its own compaction and handover machinery — which was causing stalls and manual `/compact` interventions. That is correct. A standing memory note now records the rule: an interactive session does only what the loop cannot; converter rounds belong to the loop.

---

## 2. Task 1 — the registries rebuilt (round 408, `91bc066`)

**What changed (data only, plus one builder patch):**
- `Module_Structure_Index.json` — `module_meta` **454 → 552** modules (all 98 new codes present); modules with a blank subject **12 → 0**; template types exactly **Standard 380 / Fundamentals 81 / Inquiry 68 / Bilingual 23**. The Reference-module picker on the HTML Generator now lists 552.
- `Style_Anchor_Registry.json` — **24 new family bases** mined from their own gold pages (BLLR · CBI CHI COM DAN DTC GEO GER JPN MUS MXS PWY PWYWHA SAM SPA · CHWHA FRNO GENO GEWHA JPFUN · SCBI SCES · PMT · WJFUN; WJFUN and JPFUN as single-file page models), new members on 7 existing bases, and the round-263 "evidence-floor flip" rows corrected (ANZHFUN, ENO, XOTPB/G/O had been carrying junk).
- `Menu_Scaffold_Registry.json` groups **120 → 174**, series rows **370 → 525**; `Html_Convention_Registry.json` **43 → 52** groups; the overview-menu heading lexicon **61 → 66**; the Granular registry, Feature Index (552 modules, GREEN) and legacy consensus all rebuilt in the same round.
- New `data/Subject_Prefix_Map.json` (the proposed labels, §4) and `build_granular_registry.py` reads it to fill the gaps the report folders don't file.
- **FRFUN held back, measured:** its faithful registry row scored 26 of 28 lesson pages DOWN (−763.7pp) because the multi-file level-page dialect has no renderer yet — the pre-rebuild row was restored and the follow-up recorded.

**Before → after (the gates, whole 2,349-pair population, 0 stale):**
- Skeleton SCAFFOLD mean **53.134 % → 53.680 %** (+0.55pp); pages ≥50 % **1378 → 1398**; ≥75 % **228 → 236**; ≥90 % **19 → 20**; RAW **37.487 % → 37.884 %**. 275 pages moved (197 up / 76 down, every dip named — the largest GEO1006_3_0 −11.3 and GEO1004_1_0 −9.4, the NCEA phase's h4 → h3); the 1,813 pages outside the affected set EXACT.
- compare_structure exact **13,410 → 14,091** (pool +746) / EXTRA 184 → 186 / MISSING 685 → 690 (named); body_compare over-capture 54 / runaway 6 / EMPTY 190 / ANY 248; defect audit clean 2504 / 2548 = 98.27 %; every widget verifier EXACT; 46 selftests GREEN.
- **WJFUN 10.4 % → 37.6 %** (the single-file page model alone). JPFUN01/02 stayed at 9 % / 6 % (no level or tile markers to work from).
- Scoped regeneration of exactly the **103 modules** the probe named (the other 391 proven byte-identical); scoped ship #1 since the 19 Sept full; the diff miner **187 → 183** rows.

**Also corrected:** the stale census in `LOOP_STATE.md` (2,613 → 2,555 Claude pages after the WJFUN collapse / 494 Claude dirs / 552 gold dirs / 762 docx); the ceiling and the coverage dashboard are flagged UNMEASURED on the new corpus.

---

## 3. Task 2 — the XOTP message (round 409, `222adaf`)

- `pageforge-site/js/formatter.js` gains `OutputFormatter.ACTIVITY_TABLE_NOTICE` (data-shaped) and `_isActivityTableDoc()`: a document whose first table rows hold the two-cell header *Section heading \| Text/Activity* — present in **exactly the 12 XOTP documents and nowhere else in the 762** — now shows *"ℹ Activity-table template detected … no [TITLE BAR] expected"* instead of the warning. A/B switch `window.PF_ACTIVITY_TABLE_NOTICE_OFF`.
- **The parser itself was not touched** (as instructed). Verified: all 12 XOTP dumps differ from the corpus parsed text in that one message line only; PMT101 / PNR107 / TRR102 keep the warning; SCCH301 / WJFUN105 byte-identical.
- The converter side (`ModuleResolver.PrepareRun` refusing all 12 XOTP) remains Task 4's recognition round, untouched.

---

## 4. FOR APPROVAL — the proposed subject labels (Task 1)

These 30 prefixes had no learning-area report folder, so a label had to be supplied. They are marked **PROPOSED** in `data/Subject_Prefix_Map.json` and are used only as the "subject" grouping key; nothing is final until Chris says so. A blank subject shows under "All subjects" in the picker but is not a filter entry (no "Unclassified").

| Proposed label | Prefixes | Basis |
|---|---|---|
| 1-10 Blended Literacy | BLLR | server folder |
| 1-10 Health and PE | HPRE | server folder |
| 1-10 Science | SCPH, SCBI, SCES | server folder |
| 1-10 Social Science | SSEA | server folder |
| 1-10 Technology | TEDC | server folder |
| NCEA1 | CBI, COM, DAN, DTC, GEO, MUS, MXS, PWY, PWYWHA | 4-digit NCEA-style codes |
| **NCEA1** | **CHI, GER, JPN, SAM, SPA** | **Chris's call** — NCEA-level language courses; could instead join Languages |
| **1-10 Languages** | **CHFUN, FRFUN, JPFUN, FRNO, GENO, CHWHA, GEWHA** | **Chris's call** — the FUN / NO / WHA language families |
| 1-10 Writing (MiW) | WJFUN | the "My Te Kura Writing" family |
| Te Marautanga o Aotearoa TMoA | PMT | the TMoA folder |

Decision needed: keep the Languages split as above (NCEA-level CHI/GER/JPN/SAM/SPA under NCEA1, everything else under 1-10 Languages), or put all twelve under one Languages label. Changing it is a one-line data edit followed by a registry re-merge.

---

## 5. Task 3 — the WJFUN tile-page dialect (round 410, IN FLIGHT, NOT SHIPPED)

**Measured first (`outputs/_s28_t3_tiles.out`):** every WJFUN gold page is one file built as a tabs menu (Overview two-column Knowledge \| Practices + one single-column pane per tile), a `div.phases` nav, an introduction ending in a row of `phaseLink` tiles, and one `fundamentalsPanel` per tile opening with the tile title as `<h2>` (21/21).

**What was built (all behind data flag `tile_pages.enabled` + env `TILEPAGE_OFF`, five files, uncommitted):**
- `ContentConverter.#tilePagesPrepass` — turns the writer's tile structure into the existing round-265 level-pages machinery. Three tile boundaries, counted together: a `[Tile N content]` marker (16 modules); a `[LESSON N]` marker, alone or riding the title's own span (WJFUN205/210/212); a top-level heading whose text is one of the tile NAMES the writer listed in the `Tab N` side-tab list or the `[Tile title] / X` table cells (WJFUN210/307 — the round-361 "opener by name" pattern, applied only after the names are declared). A tile's "We are learning: … I can: …" block routes to its menu pane, including the first tile's block when the menu partition had already taken it.
- `InteractiveScanner.#tilePageMarker` — the tile markers are hard terminators so a widget bundle can't swallow them.
- `MenuBuilder.#levelTabs` — single-column tile panes (the gold's WJFUN form) and the level-tabs branch when the menu would otherwise be empty.
- `PanelsBuilder.panelTitleLevelPostpass` — new `level_dialect_code_prefixes ["WJFUN"]`: the tile title is promoted to `<h2>` only on pages the tile dialect built, so the toggle reverts it too.

**Proof reached (all 494 Claude-dir modules, in memory):**
- OFF (`TILEPAGE_OFF=1`) = disk **2,555 / 2,555** pages — a clean null.
- ON changes **exactly the 21 WJFUN overview pages**, nothing else (CHFUN, JPFUN01/02 byte-identical).
- Gate pre-score with the skeleton gate's own `match()`: **21 / 21 pages UP**, +257.1pp-sum scaffold (+12.2pp per page), +96.8 RAW; the biggest WJFUN107 16.7 → 52.0 %, WJFUN106 14.1 → 43.9 %, WJFUN305 28.1 → 57.1 %.
- Panels and tiles match the gold on **20 of 21** (WJFUN105 is the writer's 2 tiles vs the developer's 3 — editorial).
- The authorised scoped regeneration (`REGENERATE CORPUS - the WJFUN and JPFUN modules`, **23 modules**) ran cleanly (probe == disk 23/23, content-hash 0-stale) — and was then **rolled back** with `TILEPAGE_OFF=1` so the corpus matches the shipped manifest again (`_content_manifest.py diff` = 0 pages differ).

**Named delta to carry if the loop ships it:** the tile pane's `<h5>We are learning:</h5>` where the gold ships `<p>` is the round-349 `lesson_label_form` KB-over-gold rule (Chris's D10-9) working as designed — record, never reverse.

**Recorded follow-ups:** JPFUN01/02 unhelped (no markers in their templates); the `[Introduction content]` marker had been rendering as a stray `<h4>` (pre-existing; now consumed inside the dialect only); the developers' editorial tile renames (WJFUN108/304 …) are text, invisible to the skeleton; the 9 WJFUN modules whose panels came from the round-106 "Phase N" path are all superseded by the tile dialect.

**Not done:** gates (`run_all_gates.sh` + population split), postship (selftests, snapshot, feature-index rehtml, ledger, miner), finalise (changelog, `Config.js` → 260619.81, CLAUDE.md §9/§11/§13/§14, `gate_baseline.json`, loop README, checksums), commit.

**For the loop's first session (also in `LOOP_STATE.md`'s HANDOVER block):** either finish round 410 from this state — `bash CONVERTER_V2/outputs/_s28_t3_regen.sh`, gates, finalise, commit — or `git stash` / revert the five files. Never `git checkout` them away without deciding (CLAUDE.md §16, the round-284 lesson).

---

## 6. Repository state

- `pageforge-site` HEAD = `222adaf` (r409) over `91bc066` (r408). **Neither pushed.**
- Uncommitted (round 410): `converter-v2/app/js/ContentConverter.js`, `InteractiveScanner.js`, `MenuBuilder.js`, `PanelsBuilder.js`, `converter-v2/data/Emit_Templates.json` — all LF, JSON valid.
- Corpus: 2,555 Claude pages / 494 dirs, byte-identical to `outputs/_content_manifest.txt` (the r408 shipped state).
- Session artefacts: `CONVERTER_V2/outputs/_s28_t1_*` (Task 1), `_s28_t2_*` (Task 2), `_s28_t3_*` (Task 3 — probe runner, ON pages, pre-scorer, shape check, regen list, rollback log).

**Copy-ready push (when Chris chooses):**

```bash
cd C:\Users\Gavin\TeKura\FINAL_MODULE_DATA\pageforge-site && git push origin HEAD
```

---

## 7. Lessons recorded for future sessions (memory notes)

1. **Interactive sessions do only what the loop cannot** (registry rebuilds after an intake, the parsed-text process, the example-module UI). Converter rounds — measure → probe → regenerate → gates → finalise — belong to the loop. If stopped mid-round: roll the corpus back with the round's `*_OFF` toggle, prove the manifest diff is 0, leave the code uncommitted, write the state into `LOOP_STATE.md`.
2. **Never call `python3` from the Bash tool on this machine** — it resolves to the Windows Store stub and hangs for the full 30-minute timeout (hit three times this session, once as a "harmless" guard line). Every Python and every gate runs under WSL; scripts are written with the Write tool; engine/data edits go through the Edit tool on the real `pageforge-site/converter-v2/…` path.
