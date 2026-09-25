#!/usr/bin/env python3
"""ROUND 522 finalise (session 51 Round 2 — the journal instruction's own activity box + the AGH [Summary] alert + the r468
ride-along). WSL. argv: MEAN RAW."""
import sys
import _s51_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-26 (round 522, build 260620.83) — THE JOURNAL INSTRUCTION IS ITS OWN ACTIVITY BOX: a learner's "go to your journal and complete activity 3A" sentence ships in its own `div.activity[number=3A]` (163 of 165 gold instructions do), the AGH red-bracket form no longer opens an empty or wrong box with a garbled note, and the AGH family's bare `[Summary]` is the gold's alert titled "Summary" — plus the parked r468 `[H2]` WALT lead riding along; 21 modules, skeleton +0.0941pp

### 1. WHAT CHANGED

**The class** (`_s51_r2_jplace2.py`, the session-51 Round 1 PICK pass's activity-number lane): of **165** gold text blocks that tell the learner to go to the journal and complete a named activity, **163 sit inside their own activity box numbered with that id** (AGH 61/61, HES 27/27, PES 22/22, GEO 10/10, COM 9/9, CBI 8/8, EXBP 4/4 …). Claude boxed them only where the writer's own `[Activity]` tag did (HES); elsewhere the sentence shipped free (PES1004 `[Learning journal] Go to your learning journal and complete 3A.`, GEO1005 `Go to your journal to complete Activity 2A`), and the AGH family's red-bracket form `[Go to your learning journal and complete activity 2B]` parsed as an **[Activity] OPENER** (`_s51_r2_jactid.cjs`: 46 spans, 36 AGH): the ids were stripped into a garbled Writers Note ("activity note: go to your learning journal and complete and" — a KB constraint-1 breach) and the box stayed EMPTY (AGH1009 4.0) or swallowed the next ordinary section (AGH1002 2.0 "Soil Structure" boxed as 2B).

**The fix — three parts, three toggles.**
- **(a) the journal sentence** (data `activity_wrapper.journal_instruction_box`, env **`JOURNALINSTR_OFF`** — `JOURNALBOX_OFF` is round 405's journal-SECTION box; the first OFF probe caught the collision): (1) `PageAssembler.#journalBracketSentence`, once after `BuildItemStream`: a tag item whose ONLY tag is the activity tag and whose bracket is a journal SENTENCE (the data's journal / verb / id patterns, 5–40 words) becomes a native black item holding the writer's words verbatim, brackets stripped (a trailing `}}` typo too); (2) `ContentConverter.#journalInstructionBox`, a page post-pass just inside `#pageNumberNormalise`: a FREE `<p>` (its column's own child) naming an id is wrapped in `div.activity[number=<first id>] > div.row > div.col-12` with an adjacent writer journal button (h4.goJournal / a > div.button — never invented, D13-5); the row is split around it; a row with a side column is left alone; IN-BOX: one of (1)'s sentences that ran on as the LAST content of a box numbered with another id leaves it for its own box after that row (a writer's black journal line inside her own box stays — the HES form, already the gold's); an id the page already carries is boxed only when no activity box follows it (the de-dupe then gives it the next letter — AGH1009 7.0's journal box 7B, the gold's own; never a shift of later ids). The gold's box heading is the developer's own (in no Writers Template) — none is added.
- **(b) the AGH `[Summary]`** (data `callouts.bare_summary_alert`, env **`SUMMARYALERT_OFF`** — a family dialect, LOOP §1d exception 1): the bare red `[Summary]` resolves to no tag (the recognition census: 31 spans, every one AGH — AGH1002 / 1003 / 1007 / 1008) and shipped as a Writers Note with its bullets free (or, before (a), inside the mis-parsed journal box). The gold boxes every following block as `div.alert` headed `<h4>Summary</h4>` (`_s51_r2_summary.py`: 83 / 83); `PageAssembler.#bareSummaryAlert` re-parses the span as `[Alert]` with the tag word as its first line — the strict alert path gathers the run and `#alertTitleHeading` lifts "Summary" to the h4.
- **(c) the r468 ride-along** (data `menu.lesson_overview_implicit.lead_heading_members`, env **`LESSONWALTH2_OFF`**): `outputs/_r468_declined.patch` (parked since session 42, below the floor) rides along under LOOP §3 step 1 — its three pages (CBI1008 L1 / L2, PES1004_8_0) all fall inside this round's affected set; applied unchanged (`git apply`, offsets only).

### 2. PROOF

- In-memory probe over all 545 modules (`_s50_probe_par.sh`): `JOURNALINSTR_OFF=1 SUMMARYALERT_OFF=1` → **6,432 / 6,432 pages identical**; ON → **21 modules** (AGH1001–1009, CBI1008, COM1002, EXBP901, EXIP901, GEO1005, HES1002, MXDB301, PES1004, PHE1007, PHE1008, SCCH301, SSCI104); 0 ASSEMBLE ERROR; the r468 patch alone → CBI1008 / PES1004 only (3 pages). `scoped_ship.sh … --round 522` PASS twice (the round, then the ride-along): 0 stale, containment 21 ⊆ 21, the 12-module spot-check byte-identical.
- The skeleton gate's own `match()` on the ON pages (`_s51_prescore.py`), by part: (a) alone +0.0152pp (25 up / 22 down — its AGH dips were the old wrong box that had happened to wrap the `[Summary]` run, whose nesting resembled the gold's alert); (b) alone +0.0458pp (27 up / 2 down); **(a)+(b) +0.0899pp, 56 up / 13 down** (largest rises PHE1008_4_0 +12.1, PES1004_3_0 +8.6, AGH1002_2_0 +8.0, AGH1008_5_0 +7.7, PES1004_5_0 +6.9, GEO1005_5_0 +6.7, AGH1003_4_0 +6.7; the 13 dips ≤ 3.0pp — AGH1009_8_0 −3.0 is a pairing artefact (paired with gold `AGH1009.03.1`; its change removes the empty mis-parsed 8B box), CBI1008_5_0 −1.5, AGH1006_2 / 5 / 8 −1.1 to −1.5, the rest < 1pp); (c) +0.0042pp (3 up).

### 3. PROTECTED GATES

Skeleton **55.7889 → {MEAN} % @ 2486 (+0.0941pp)**, ≥50 1616 → 1618, ≥75 286 → 288, ≥90 26; RAW 39.630 → {RAW} %; **compare_structure exact 16772 → 16845 (+73)**, missing 886 → 879 (−7), EXTRA 204 held; **body_compare ANY 236 → 234**; clean 98.40 %, leak 52 / 42 EXACT; tags 9557; every verifier ✓, every COUNT held (`_r522_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 522`; `--gate-baseline-check` PASS. Plateau: **reset** (+0.0941pp).

**Ledger:** scoped #2 since the s50-r14 FULL (r520) · data `activity_wrapper.journal_instruction_box`, `callouts.bare_summary_alert`, `menu.lesson_overview_implicit.lead_heading_members` · env `JOURNALINSTR_OFF`, `SUMMARYALERT_OFF`, `LESSONWALTH2_OFF` · code `PageAssembler` (`#journalBracketSentence`, `#bareSummaryAlert`), `ContentConverter` (`#journalInstructionBox`; the r468 lead-member test) · session 51 Round 2.
"""
F.finalise(
    N=522, old_build="260620.82", new_build="260620.83", entry=entry,
    config_comment="THE JOURNAL INSTRUCTION IS ITS OWN ACTIVITY BOX (session 51 Round 2) + the AGH [Summary] alert + the r468 "
                   "ride-along. Env JOURNALINSTR_OFF / SUMMARYALERT_OFF / LESSONWALTH2_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 522 BASELINE (the journal instruction's own activity box "
        f"+ the AGH [Summary] alert + the r468 ride-along, `JOURNALINSTR_OFF` / `SUMMARYALERT_OFF` / `LESSONWALTH2_OFF`; SCOPED, scoped #2 "
        f"since the s50-r14 FULL): SCAFFOLD mean {MEAN}% / >=50% 1618 / >=75% 288 / >=90% 26 / RAW {RAW}% @ 2486 pairs (+0.0941pp); "
        f"cs exact 16845 / missing 879; body ANY 234.**",
    og11="| `JOURNALINSTR_OFF` | 522 | **THE JOURNAL INSTRUCTION IS ITS OWN ACTIVITY BOX** (session 51 Round 2). Reverts "
         "`activity_wrapper.journal_instruction_box`: the AGH red-bracket journal sentence parses as an [Activity] opener again (garbled "
         "note + an empty or wrong box) and a free journal instruction ships unboxed (the r521 output exactly). |\n"
         "| `SUMMARYALERT_OFF` | 522 | **THE AGH [Summary] IS AN ALERT TITLED 'Summary'** (session 51 Round 2, part b). Reverts "
         "`callouts.bare_summary_alert`: the bare `[Summary]` ships as a Writers Note with its run free. |\n"
         "| `LESSONWALTH2_OFF` | 522 (built r468) | **THE `[H2]` WALT / SC LEAD IS A LESSON-MENU MEMBER** (the r468 patch, the r522 "
         "ride-along). Reverts `lesson_overview_implicit.lead_heading_members` (CBI1008 L1 / L2, PES1004_8_0). |",
    og14=f"- **Build:** `260620.83` (round 522 — **the journal instruction's own activity box + the AGH [Summary] alert + the r468 "
         f"ride-along**; `JOURNALINSTR_OFF` / `SUMMARYALERT_OFF` / `LESSONWALTH2_OFF`; scoped #2 since the s50-r14 FULL; 21 modules; "
         f"skeleton {MEAN} % (+0.0941pp), RAW {RAW} %; cs exact 16845; body ANY 234).",
    gb_note=f"Round 522 (session 51 Round 2, 2026-09-26) — THE JOURNAL INSTRUCTION IS ITS OWN ACTIVITY BOX (JOURNALINSTR_OFF) + the AGH "
            f"[Summary] alert (SUMMARYALERT_OFF) + the r468 ride-along (LESSONWALTH2_OFF): 21 modules; skeleton 55.7889 -> {MEAN} "
            f"(+0.0941pp), >=50 1618, >=75 288; cs exact 16845 (+73), missing 879 (-7); body ANY 234 (-2); scoped #2.",
    no_round=f"- **No round in flight** (26 Sept 2026 {T}, session 51 Round 2 — r522 (the journal instruction's own activity box + the AGH "
             "[Summary] alert + the r468 ride-along) SHIPPED and committed; the in-flight marker is cleared). LAST SHIPPED **r522** "
             "(260620.83); **LAST FULL = r520 (the session-50 Round 14 backstop)**; ledger **scoped #2** (6 of headroom). Ride-along patches "
             "(LOOP §3 step 1 reads this list at every PICK): `outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / "
             "`_r469b_declined.patch` (buttons, 10 pages / 9 modules — CEDK401, HIS1002, HPRE203, MXDI201, MXDI202 ×2, MXEX302, SSOG105, "
             "TWHA906, XGF9004) / `_r489_accbullet_declined.patch` (the accordion bulleted bold lead, 8 accordions / 4 modules — MXEX302, "
             "ENGS101, XGF9003, XLP05) / `_r463_declined.patch` (the WJFUN tile's \"Year N\" lead, 1 page) / `_r512_declined.patch` (the "
             "`[Activity: Embedded] <widget>` bracket, 10 modules — rides only after the TRR table-dialect ownership fix). "
             "`_r468_declined.patch` RODE ALONG in r522 (struck). Checked at r522: no other patch has all its pages inside the 21 "
             "— none else rides.",
    last_shipped=f"- LAST SHIPPED: **r522** (build 260620.83, 26 Sept {T}, session 51 Round 2 — THE JOURNAL INSTRUCTION IS ITS OWN ACTIVITY "
                 "BOX + the AGH [Summary] alert + the r468 ride-along, `JOURNALINSTR_OFF` / `SUMMARYALERT_OFF` / `LESSONWALTH2_OFF`; "
                 "SCOPED, **scoped #2 since the s50-r14 FULL**; 21 modules; skeleton 55.7889 → "
                 f"{MEAN} % (+0.0941pp), ≥50 1618, ≥75 288, RAW {RAW} %, cs exact 16845 / missing 879; body ANY 234).",
    before_them_add="the new activity id ends the walk",
    plateau="- Plateau window (§4): **0 of 3** — r522 +0.0941pp (a real gain: reset); ",
    standing="- Standing facts: AppVersion **260620.83** (r522 the journal instruction's own activity box — session 51 Round 2, 26 Sept); "
             "before it 260620.82 (",
    roundlog=f"- s51-r2 (engine r522, build 260620.83, 26 Sept 10:45 → {T}) · a PICK pass (the placement census's `body:activity → free` "
             "row → the journal instructions: gold 163 / 165 boxed) then THE JOURNAL INSTRUCTION IS ITS OWN ACTIVITY BOX + the AGH `[Summary]` "
             "alert (83 / 83) + the r468 ride-along · SHIPPED scoped #2 · 21 modules · skeleton **+0.0941pp**, ≥50 +2, ≥75 +2, cs exact +73 / "
             "missing −7, body ANY −2 · plateau reset (0 of 3).",
    archive_extra="- **What shipped (r522, 260620.83):** `PageAssembler.#journalBracketSentence` / `#bareSummaryAlert`, "
                  "`ContentConverter.#journalInstructionBox`, the r468 patch; data `activity_wrapper.journal_instruction_box`, "
                  "`callouts.bare_summary_alert`, `lesson_overview_implicit.lead_heading_members`. Probe OFF 6,432 / 6,432 identical; ON 21 "
                  "modules; +0.0941pp; cs exact +73; body ANY −2.",
)
