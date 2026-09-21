# LOOP_REVIEW__2026-09-22.md — the second health review of the PageForge autonomous loop

**Run by:** `/loop-review` on Fable, 22 September 2026, with Chris present. NOT a loop run: no round started, no converter code or data changed, nothing regenerated.
**Covers:** everything since the first review (`LOOP_REVIEW__2026-09-16.md`, evening of 16 September): loop sessions 13–31 plus the pre-loop session 28, engine rounds r348 → r425, the 98-module intake of 19 September.
**Headline:** the loop is healthy and productive (70 rounds shipped in five days, the score up from 55.8 % to 59.6 % of what is achievable), but **the twelve rule changes you approved on 16 September were lost the next day** — session 19 wrote the loop file from an older copy — and nobody noticed for 78 rounds. Restoring them is proposal 1. The other findings are: the "exhaustion" stop keeps firing and being proved wrong (9 times in 18 sessions), the start message now carries stale state it was designed never to carry, and the committed copy of the gate baseline is twelve rounds behind the live one.

---

## The words used in this report

- **Round** — one pass of the loop: pick a class of mismatch, fix it, rebuild what the fix touches, prove the gates held, write it up, commit.
- **Class** — a repeating kind of difference between our page and the human developer's page (for example "the activity title sits inside the red span"), counted in pages and modules.
- **Gold** — the human developer's finished module pages in `01-Finalized_Modules_`; the reference we measure against.
- **Skeleton score (SCAFFOLD)** — how closely a page's row / column / activity / section structure matches the gold, ignoring the insides of interactive widgets. The primary number. Quoted as a mean over all paired pages.
- **pp** — percentage points. 54.17 % → 54.19 % is +0.02pp.
- **Ceiling / "% of achievable"** — the share of the gold's structure that has a source in the Writers Template at all. What is not in the template no converter rule can ever build. The ceiling is 90.9 %, so a raw 54.17 % is 59.6 % of achievable.
- **Gate** — one of the automatic scores that must never get worse from one round to the next.
- **Verifier** — a gate for one widget type (drag-and-drop, bingo, speech bubble…) that checks every built widget is well-formed and matches the gold's form.
- **KB** — the HTML Convertor knowledge base in `00-Other-TK-Resources/htmlconvertor-kb`, the most recent statement of what a finished module must look like. Its numbered rows are **CL** entries (change-ledger entries).
- **The miner** — `_diff_miner.py`, which reads every structural difference between our pages and the gold and ranks them into `DIFF_QUEUE.md`.
- **Declined** — a class measured and deliberately not built (the gold is split, or the template gives no way to tell). A recorded decline is a good outcome.
- **Blocked** — a class the rules cannot settle; it needs a decision from Chris.
- **Inert** — built and committed but switched off; the pages are unchanged until the switch is flipped.
- **Compaction** — the tool's automatic summarising of the conversation when it fills up. "Thrash" is when it fills again immediately after.
- **Mirror** — the copy of the loop's files kept inside the git repository at `pageforge-site/converter-v2/loop/` so they are version-controlled.

---

## 1. Health check — PASS, with three drift findings

| check | result |
|---|---|
| `git status` in pageforge-site | clean on `main`, nothing uncommitted, 0 commits ahead of the recorded `origin/main` |
| stale git locks | none |
| `verify_after_transfer.sh` | PASS on all six checks: 5 / 5 symlinks, 62 / 62 engine files, 81 / 81 gate tools, census 552 gold / 495 Claude dirs / 2,559 Claude pages / 2,993 gold pages / 762 docx / 33 engine js / 24 data json, both git histories intact (one cosmetic WARN: its snapshot HEAD is from the 19 August transfer) |
| `wc -c` | LOOP_STATE.md 87.7 KB (under the 100 KB target), DIFF_QUEUE.md 134 KB, LOOP_STATE_ARCHIVE.md 1.06 MB (grep-only, as designed) |
| the loop mirror | LOOP_STATE.md, KB_AMALGAMATION_STATUS.md, DIFF_QUEUE.md, LOOP__Autonomous_Rounds.md all byte-identical to the mirror; **`gate_baseline.json` is NOT** (see 3d) |
| the KB repo | HEAD `44c7c8e` (21 Sept), clean apart from two untracked designer outputs |

**Drift 1 — the 16 September amendments are gone.** Commit `b64b4f5` ("Loop review 2026-09-16") carried the loop file with an "Amended: 16 September 2026" header and all twelve approved changes (29,285 bytes). The very next commit to touch it, `85cb9db` (17 Sept, session 19, Round 0c — the diff miner), wrote a 28,716-byte version with none of them: no "Amended" line, §4 back to "10 rounds / 6 hours", no WAITING stop, no atomic-write rule, no compaction logging, no "a numbered constraint is binding". Session 19 evidently edited an older copy of the file and added its new §1d on top. Every later edit (sessions 20, 27–28, 31) built on that copy. Today's file at the root and in the mirror are identical to each other and both lack the amendments. The full list of what was lost is in section 4, proposal 1.

**Drift 2 — §7 and the `/loop-start` skill no longer match, and the skill carries state.** `.claude/skills/loop-start/SKILL.md` (last edited 21 Sept 21:53) contains five things §7's quoted message does not: a sentence about the 98-module intake and "round 410 … BUILT AND PROVEN BUT NOT SHIPPED with five files uncommitted — decide it before picking anything new"; "ANY exhaustion verdict reached before 19 September 2026" (§7 says only sessions 15–18); the §1e population-split instruction; the "never call python3 from the Bash tool / run `cs bc` first" instruction; and "CLAUDE.md is now only a 4 KB pointer". The round-410 sentence has been wrong since session 29 shipped it on 20 September; sessions 30 and 31 both had to note "the kickoff's 'five files uncommitted' is stale". §7 says the message "contains no state … so it never needs editing" — the skill now contains state, and the rule "if the message text changes, change the SKILL.md files too" was applied in reverse (the skill changed, §7 did not). The `/loop-stop` skill matches §7's stop message exactly.

**Drift 3 — the loop file's own facts are stale.** §0 items 6–7 still say round 410 is unshipped; the census table says 494 Claude dirs / 2,555 pages (now 495 / 2,559 after PMT101); §1 says the ceiling is "currently UNMEASURED … do not quote a % of achievable" although session 29 re-measured it on 20 September (90.9 % on 2,290 pairs, `_ceiling_r410`) and every report since quotes it; §2 says PMT101 "is a real recognition gap" (fixed at r423) and lists the 12 XOTP modules as refused (the adapter is built, r425, awaiting its ship); §3 step 1 tells the session to run `python3 …` from the shell, which §6 forbids on this machine.

`.claude/settings.json` is unchanged since 15 September (auto mode, 30-minute shell timeout, 60-minute ceiling) and agrees with §5c.

---

## 2. What was read

By section, never whole: `LOOP__Autonomous_Rounds.md` (all 550 lines); `LOOP_STATE.md` — the four STOPPED entries, all Decisions-from-Chris blocks, Position, the ceiling, Declined classes, Blocked classes, the Round log, the 16 Sept review pointer, the "Next session starts with" line; `LOOP_STATE_ARCHIVE.md` — the archived round-log lines for sessions 13–29 (90 round lines in all), every archived STOPPED heading, the archived 16 Sept review entry, the session-26 needs-Chris list; `KB_AMALGAMATION_STATUS.md` — header, §C rows for CL-0093–0095, §D, §E; `BUILD_CHANGELOG.md` — the headings of the 78 entries since r347 and the r425 entry in full; `DIFF_QUEUE.md` — header, summary, completeness census, the top of the ranked table; the KB repo — `git log` since 16 Sept, the file list it touched, `12E6` / `12E7` (CL-0093–CL-0100), `12G`'s status lines, the diff of `00_MASTER_INSTRUCTIONS` and `14_SUBJECT_GLOBAL_PARAMETERS` since `469f496`; `gate_baseline.json` live and mirror; the r423 gate log; `_ceiling_r410.log`; `COVERAGE_DASHBOARD.md`'s header; `LOOP_INTAKE__2026-09-19_98_Modules.md` §7 and §9; `git diff b64b4f5 85cb9db` on the loop file; the four skill files.

---

## 3. Assessment

### 3a. KB drift — **fine as is on the rules; change needed on two housekeeping lines**

- **The KB moved 7 commits** since the status file's "re-checked" line (HEAD `8b8d8e5`, 17 Sept → `44c7c8e`, 21 Sept). The new ledger rows are **CL-0096 → CL-0100** (20–21 Sept): publishing the nine operating modes as Claude Skills, splitting the Comparison skill, two documentation corrections, renaming the ten skills. **None is a module rule.** The files touched under `00_MASTER_INSTRUCTIONS` are the operating-modes list, the file index and the when-to-load guide — 9 lines changed, no constraint text. `00D_CONSTRAINTS_1.md`, the `14_` family files, `06` and `10` are untouched since 16 September. Constraints 1–92 and CL-0001 → CL-0095 are what the status file already knows. Nothing new to capture.
- **Highest CL the status file knows:** CL-0095. Highest in the ledger: CL-0100. The gap is five non-module entries.
- **Conflicts between the KB and rules the loop shipped since 16 Sept:** none found. The KB-driven rounds — r399 (wānanga box = KB 05B cultural alert), r403 (`[embed]` = the KB externalButton), r419 (CL-0093's CJK half, "locked admin"), r420 (KB 03E bingo), r397 (05D plain header cells) — each names its KB source. One item to check when r425 ships, not now: its record says the XOTP acknowledgements land on page 1 "KB c33, named" while the gold puts them on page 2 — confirm c33 actually says page 1 before that override is accepted.
- **Housekeeping owed in `KB_AMALGAMATION_STATUS.md`:** the header still says "re-checked 17 September, HEAD 8b8d8e5" although session 30 updated row 92 on 21 September and session 31 recorded HEAD `44c7c8e` in LOOP_STATE.md; the §C heading says "CL-0001 → CL-0095" and should note that 0096–0100 are skills / documentation entries with no PageForge action. (Proposal 8.)
- **Still owed by Chris from the last review:** the six `12G` "PageForge status" lines (all still read "Not yet amalgamated"; r419 now adds CL-0093's CJK half to that list) and the five KB edits from the D10 decisions. Documentation only — no page depends on them — but until they land the KB's wording contradicts shipped behaviour in five places.

### 3b. Progress — **fine as is on the numbers; the stop pattern needs attention (3c)**

**The score.** At the last review the skeleton mean was 51.283 % on 1,955 paired pages, ceiling 91.9 % → **55.8 % of achievable**. Today it is **54.170 % on 2,353 pairs, ceiling 90.9 % → 59.6 % of achievable** (build 260619.96, round 423's corpus; round 425 changed no page). ≥ 50 % pages 1,074 → 1,442 (61.3 %), ≥ 75 % 198 → 238, ≥ 90 % 15 → 20; structurally clean 98.3 %; literal-tag leak 73 occurrences / 44 pages (26 / 23 on the pre-intake subset, exact); tags 9,557 / 9,557; every verifier at divergence / defect 0 or its recorded baseline; 17 self-tests green.

**What earned it.** Raw movement +2.887pp, of which:
- +1.197pp were **instrument corrections** (r355 the scorer's autojunk cliff +1.014; r382 the body reader +0.096; r386 sorted class tokens +0.087) — the score was under-read before, not the pages worse;
- −0.440pp were **population changes** (the 19 Sept intake −0.404 at 2,349 pairs; PMT101 joining −0.036) — harder pages joined;
- −0.318pp was one deliberate **KB-over-gold override** (r349, the `<h5>` menu labels, your D10-9);
- the remaining **≈ +2.45pp is converter rules matching the gold**, over 66 gold-matching shipped rounds ≈ **+0.037pp per round** (last review: +0.03). The biggest single rounds: r362 +0.173, r371 +0.149, r417 +0.195, r400 +0.118, r394 +0.114, r399 +0.103, r410 +0.110.

**Rounds and sessions.** 78 engine numbers (r348–r425) in 18 loop sessions plus one pre-loop session, ≈ 66.6 hours of loop time, 86 rounds counting PICK passes → **≈ 46 minutes per round** (last review 47).
- **Shipped: 70** (67 engine / data rounds + 3 instrument rounds; includes r424 output-inert by design).
- **Declined on measurement, shipped inert: 7** (r353, r367, r368, r369, r384, r404, r422).
- **Stopped mid-flight, shipped inert: 1** (r425, on your `/loop-stop`; built and proven on its 12 modules, the corpus-level proof not run).
- **Blocked: 0.** The three-attempt repair limit and the two-blocked stop never fired.
- **PICK passes with nothing at the floor: ≈ 10**, plus ≈ 30 further classes measured and declined inside other rounds.

**Rounds per session:** s13 1, s14 1, s15 5, s16 1, s17 0, s18 0, s19 6 (+ Round 0c), s20 1 (died), s21 5, s22 1, s23 7, s24 10, s25 0, s26 12, s27 12, s29 10, s30 6, s31 3. The two 12-round sessions and the 10-round ones are the budget working as intended.

**How sessions ended:** 9 on EXHAUSTION (s15, s16, s17, s18, s21, s22, s24, s25, s30), 5 on `/loop-stop` (s14, s19, s23, s29, s31), 3 on BUDGET (s13, s26, s27), 1 died of compaction thrash (s20). **The plateau rule fired 0 times** (last review: 3 of 3 for the wrong reason). The window reached 2 of 3 at the start of session 27 and was reset by r406 / r407.

**The plateau rule** is therefore no longer the problem. Its replacement text from 16 September ("counts only rounds whose PICK predicted a skeleton move; never fires while the queue holds a ≥ 0.02pp class") was lost, but sessions behaved as if it were there: gate-neutral rounds (r396, r402, r424) were logged "gate-invisible, window unchanged". Restore the text so the behaviour is a rule, not a habit.

### 3c. Rule quality — **change needed in three places; fine in four**

**Change needed 1 — the EXHAUSTION stop is the loop's most-used stop and it has been wrong every time.** Nine of eighteen sessions ended on it. Four (s15–s18) predate the miner and were declared void on 17 September. The five since, each declared "with the miner's queue quoted, every candidate row dispositioned": s21 (03:05, 18 Sept), s22 (08:35), s24 (19:30), s25 (20:40), s30 (19:10, 21 Sept). What followed each:
- after s21 / s22 → session 23 shipped **7 rounds, +0.289pp** (the heading-digit census: r371–r375);
- after s24 / s25 → session 26 shipped **11 rounds, +0.344pp** (the paired row / column census: r387–r397);
- after s30 → session 31 shipped r423 (PMT101, a recognition gap **written down in the intake handover's §7 since 19 September** and never dispositioned by s30) and built r425 (the 12-module XOTP adapter, also in that list).
So "exhaustion" in practice means "the instruments this session thought of have nothing left", not "the queue is empty". The miner's 184 candidate rows are "all dispositioned" at every stop — the picks that moved the score came from hand-built probes (a census the session invented), or from a list that already existed and was not consulted. Session 30 was honest about it in its own record ("VALID in form but INCOMPLETE"). The cost is small per event (an early end to a session) but it happens every other session, and it makes the loop depend on a human noticing. **Proposal 2** adds the missing sources to the checklist, requires the STOPPED entry to list the angles tried, and makes an exhaustion verdict provisional until one round has been spent on a lane not yet used that session.

**Change needed 2 — the 20-page floor is producing built-then-parked rounds for family dialects.** Round 422 (session 30): FRFUN06's side-tab navigation, one module, 10 pages, built, measured 8 pages up / 2 down, +34.7pp summed over its pages, OFF corpus byte-identical, every gate held — and shipped **inert** "under the floor; enabling it is Chris's call". Round 404 (session 27) is the same shape (the alert-top side column by subject, declined-inert). The floor exists to stop a rule learnt on a few pages being applied corpus-wide; a rule keyed to one family (a registry row, a family flag) cannot over-reach — the §3 NEW-FAMILY CHECK already says a family dialect's right fix is a registry row. Related: the `<br>` soft-break class (session 27 Round 2) holds ≥ 0.60 per prefix (ENGJ 0.97, HIS 0.65, EXPFUN 0.99) but "each family under the 20-page floor alone" — ≈ 25 pages summed, estimated +0.03pp, not taken. **Proposal 3** lets a family-keyed rule ship under the floor when it matches its family's own gold on every page and the OFF corpus is byte-identical, and lets per-group rules count the SUM of the groups that each pass consensus.

**Change needed 3 — "artefact" dips are again being named without the companion number the lost rule required.** Much better than last time: 5 of 90 round-log lines name a scorer artefact (last review 10 of 34). But r419 ("the JPN1004 dips = alignment artefacts, form = the gold's"), r420 (−0.0005pp accepted via `--accept-named`) and r425 ("the scorer's alignment artefact on a strictly-closer menu — the r334 / r385 / r389 class, NAMED") each name the same alignment artefact without quoting the position-free overlap or matched-line count beside the page. The 16 Sept rule ("a dip may be attributed to an artefact only when a companion number on that page rises … a third recurrence → a scorer-repair round") was lost with the rest; r382 / r386 were exactly such repair rounds and they paid (+0.183pp). Restore (proposal 1e). The `--accept-named` flag added at r420 is the right mechanism — the rule should say it may only be used with the companion number written in the log.

**Fine as is:**
- **The 0.60 solidify floor.** Declines since 16 Sept all read as genuine: the minor-heading row break (h5 flows 0.57 = a tie, 25 pages); the widened wrapper per built layout (≤ 0.36 in every group); `div.alert.solid` (the gold keeps solid 22 / 295 = KB-correct); the standalone dropDown / typing box (declined twice on the probe, 36 up / 135 down then 19 / 52). No decline looked derivable on re-reading.
- **The three-attempt repair limit and the two-blocked stop** — never fired; untested but not in the way.
- **Per-template / subject grouping (§1b)** — working and productive: r391 (Leaving to Learn only), r373–r375 (heading digits per prefix), r395 (flip-card widths with four family exclusions), r387 (Standard only, NCEA1 excluded).
- **The authority order** — the KB-first rounds were taken as KB rounds (r399, r403, r419, r420) and the one named KB-over-gold cost (r349, −0.318pp) was declared as such. The lost §2 sentence "a numbered constraint is BINDING — no gold-share test" was followed by habit (r419 shipped c92 on the KB's authority with the gold at 0.99 anyway). Restore the text (proposal 1b / 1c).

### 3d. Gate health — **fine as is on the measurements; change needed on one committed file**

- **Pairing parser:** `pairs skipped (parse error): 0` in the r423 gate log and in the miner (2,353 pairs / 484 modules, 0 parse errors). Entry parity PASS.
- **Baseline moves, all explained:** r408 (2,606 → 2,548 pages when WJFUN / JPFUN went single-file, `_note_r408`), the 19 Sept intake re-base (`_note_intake`: the pre-existing subset EXACT), r410, r423 (2,349 → 2,353, PMT101). The §1e population-split rule was used correctly each time; no gate moved without a cause.
- **Verifiers that could pass vacuously:** checked in the r423 log. flipCard: TRR114 "built 0 card-texts, no builds" (1 of the 10-module gate set — the others carry 61 cards); bingo: BLL113 / BLL154 "built 0 (all fell back)" by design, the other 7 modules carry 52 grids; the pop-out verifier passes on "well-formed" with exact 4 / dev-edit 34 of 38 triggers — it proves shape, not content, which is what it claims. speechBubble reads ✓ at its recorded baseline (OSAI401 3, OSAH501 1) since r348 — the last review's red-at-baseline problem is fixed. Nothing vacuous.
- **Change needed — the committed gate baseline is stale.** `CONVERTER_V2/reference/tests/` (the 81 gate tools and `gate_baseline.json`) is **not in git at all**; the only version-controlled copy is the mirror in `pageforge-site/converter-v2/loop/`. Every mirrored file is byte-identical to the live one except `gate_baseline.json`: the mirror is at round 410 (2,349 pairs, committed 20 Sept 15:36); the live file is at round 423 (2,353 pairs, 21 Sept 20:10) and carries the r419–r423 notes. The 16 Sept rule "mirror every changed loop artefact and prove it byte-identical" was among the lost amendments. **Proposals 1f and 7.** (A larger question for Chris, not for today: whether `CONVERTER_V2/reference/tests/` should itself be under git — a power cut today would lose the gate tools' last twelve rounds of edits except through the checksum manifests.)

### 3e. Session mechanics — **change needed in two places; §5c is working**

- **Stalls / prompting:** none recorded since the last review — no "shall I continue", no turn ended to wait. §5c holds.
- **Compactions:** still not logged per event, so still not countable — the lost §6 rule. What is known: session 20 died of thrash (17 Sept; LOOP_STATE.md was 636 KB) → the §5d caps; session 31 had **three automatic compactions and one manual `/compact`** in 2 h 45 → the root cause was found and fixed that night: `converter-v2/CLAUDE.md` had reached 1.3 MB and the harness auto-loads every `CLAUDE.md` after every compaction, refilling the context at once. Renamed `OPERATING_GUIDE.md`; `CLAUDE.md` is a 4.8 KB pointer. Sessions 29 and 30 (8 h 15 and 3 h 35) ran without a recorded thrash on the r410-era file, so the fix is plausible but unproven by a long session. **Restore the compaction log (proposal 1h) so the next review can count.**
- **Commands past the timeout:** the Windows Store `python3` stub. Recorded hits: three in session 28, one in session 29 (a `python3 - <<EOF` heredoc), one in session 31 (`python - <<EOF`) — **five hits at up to 30 minutes each, ≈ 2.5 hours lost**, every one after the rule was written into §6 and into the loop-start message. A written rule is not holding; the fix belongs in the tool, not the text. **Proposal 6** adds a pre-command hook to `.claude/settings.json` that refuses any Bash command invoking `python` / `python3` outside `wsl`, so a slip fails in a second instead of hanging for thirty minutes.
- **Anything the session had to be prompted for:** only the two `/loop-stop`s you sent (s29, s31) and the D11 instructions — both are intended interactions.
- **§5c and §6:** fine. The §5d caps have held (LOOP_STATE.md 87 KB; two condenses, no decision deleted).
- **Engine-file safety:** no 0-byte incident since r347; the atomic-write rule that would have prevented it was lost (proposal 1h restores it).

### 3f. Decisions owed by Chris — fifteen open, none blocking a round today

Oldest first; "holding up" = what cannot change until you decide.

1. **16 Sept — the six `12G` "PageForge status" lines and five KB edits from D10-2 / 4 / 5 / 7 / 8** (an Admin-Mode KB session, your choice to do yourself). Holding up: 0 pages; the KB's wording contradicts shipped behaviour in five places.
2. **16 Sept — D10-5's declined `tableFixed` half:** accept the decline or re-specify. Holding up: 13 gold contrast-header tables.
3. **16 Sept — D10-9's wording half:** accept the writer's wording as the fallback or supply a per-module year list. Holding up: ≈ 130 modules' menu labels, text only.
4. **17 Sept (s17 / s18) — does D10-3 extend to the quiz-engine widget types** (multiChoiceQuiz 357 / typing 255 / dropDown 232 hand-off boxes on disk)? Holding up: **844 boxes — the largest single item on the list.**
5. **18 Sept (s21) — the journal button** (`Go to your journal`: ≈ 58 gold-invented headings / the missing `div.button`, diffuse). Holding up: ≈ 58 sites.
6. **18 Sept (s21) — the dual-build gold directories' gate pairing** (the MXFUN family). Holding up: a handful of modules' pairing.
7. **18 Sept (s22) — the activity-number provenance** (r369 inert: 279 pages ON, 46 up / 77 down). Holding up: a policy on renumbering the writer's duplicate / foreign ids.
8. **19 Sept (s26) — the 12 empty-lesson-menu repeaters.** Holding up: 12 modules' lesson menus.
9. **19 Sept (s26) — the speech bubble's character image** (the gold adds one: Online Safety 0.95, TEDC 0.91). Holding up: a placeholder-image policy per subject.
10. **19 Sept (intake) — seven modules with no Writers Template** (GER1003–1007, SAM1005, SAM1006) need collecting. Holding up: 7 modules that can never convert until then.
11. **19 Sept (intake) — XOTPB08's pasted picture** (8 of 12 payload items exist only as an image). Holding up: 1 module.
12. **20 Sept (s28) — the `Subject_Prefix_Map.json` labels** (the Languages split). Holding up: no page, but no rule may depend on the labels until they are confirmed.
13. **21 Sept (s30) — enable the FRFUN06 side-tab dialect (r422).** Ready to flip: 10 pages / 1 module, 8 up / 2 down. Proposal 3 would settle this class of case for good.
14. **21 Sept (s31) — the XOTP reader book** (carousel images, matching sentences, acknowledgements — no Media List on any of the 12). Holding up: the 12 modules' end-to-end conversion; the text adapter finishes without it.
15. **21 Sept (s31) — the XOTPB Overview text** (an external Google Doc). Holding up: 6 modules' overview text.

These live in six different places today (the session-26 STOPPED entry, the intake §9, the s28 report, the s30 and s31 entries, the 16 Sept review). **Proposal 9** gives them one standing section.

---

## 4. Proposals

Each: what changes, what happens if it is made, what happens if it is not, my recommendation. Nothing is applied until you say so.

### Proposal 1 — Restore the twelve amendments you approved on 16 September (lost 17 September)

**What.** Put back, word for word except where a later change superseded them, the text `git diff b64b4f5 85cb9db` shows was removed. Eight edits:

**1a — §0, after "regenerate anything on a broken tree."** Add:
> Then note the KB repo's HEAD (`git -C 00-Other-TK-Resources/htmlconvertor-kb log -1 --oneline`) against the commit `KB_AMALGAMATION_STATUS.md` names as last checked: if it has moved, read the new commits' ledger rows before the first PICK and record the new HEAD in the status file's header.

**1b — §2, the Declines bullet.** Current text ends "…never re-attempt a declined class in this loop unless new evidence is named." Append:
> **The 0.60 floor and the tie test apply only when the target comes from authority levels 3–4** (this module's gold, or template / subject consensus). When a numbered `00_MASTER_INSTRUCTIONS` constraint or a front-facing CL row covers the element (level 1), the gold share is NOT consulted: the KB form is the target, the gold's disagreement is a NAMED override (§1b "Gates and KB overrides"), and the round ships — whether or not the constraint has a CL row of its own. BLOCK for Chris only when (a) two KB documents disagree with each other, (b) the KB disagrees with one of Chris's own project instructions, or (c) the KB offers a component-doc example rather than a numbered rule and the gold contradicts it at ≥ 0.60. The 20-page floor is a PICK floor: a class under it is recorded, not built, unless it rides along with a round already in scope and is proven the same way. (Review of 16 Sept 2026: c47 and c23 were declined / blocked on the gold share and Chris confirmed the KB on both.)

**1c — §3 step 3.** Current: "If the share is < 0.60 or tied in every group → DECLINE (§2), log it, go to 1." Proposed: "If the target is gold-derived and the share is < 0.60 or tied in every group → DECLINE (§2), log it, go to 1. If a numbered constraint covers the element, skip the share test — measure only the override list."

**1d — §3 step 5.** Current: "via `_batch_plan.py` and `_regen_safe.sh`, one batch per command. There is no 45-second wall in Claude Code, but keep each command under ~10 minutes and write progress to a file so nothing is lost." Proposed: "with `batch_convert.cjs` run directly under WSL for the affected set (the form every round since r410 has used: `STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs batch_convert.cjs <codes> --force`), `scoped_ship.sh` for a scoped ship, and the OPERATING_GUIDE.md §10 recipe for a FULL regeneration (batches of ~11; batches that fail on the oembed-cache write race are re-run singly). `_regen_safe.sh` only with `REGEN_TIMEOUT` set. Keep each command under the 30-minute shell timeout and write progress to a file so nothing is lost."

**1e — §3 step 6.** After the existing "If a gate regresses…" sub-bullet, add:
> - A page dip may be attributed to the scorer's alignment or repeat-collapse artefact ONLY when a companion number on that page rises — the position-free overlap or the uncollapsed matched-line count — and both numbers are written beside the page name; `--accept-named` may be used only with those numbers in the log. When the same artefact has been named in three shipped rounds, the next PICK is a measurement-tool round (the r315 / r382 / r386 precedents) that makes the scorer report the companion metric itself.
> - A verifier's RESULT line must read ✓ at its recorded baseline and ✗ only above it (the r348 form). A round may not ship while any RESULT line is red.

**1f — §3 step 7.** Current: "refresh `gate_baseline.json` and the feature index (`build_feature_index.cjs`) after any regeneration, `git add` + `git commit` in `pageforge-site`." Proposed: "refresh `gate_baseline.json` (every field — `skeleton.pairs` included) and the feature index (`build_feature_index.cjs`) after any regeneration, mirror every changed loop artefact — `gate_baseline.json`, `run_all_gates.sh`, `_corpus.py`, any new verifier, `LOOP_STATE.md`, `KB_AMALGAMATION_STATUS.md`, `DIFF_QUEUE.md`, this file — into `pageforge-site/converter-v2/loop/` and prove the mirror byte-identical (`cmp`; `CONVERTER_V2/reference/tests/` is NOT in git, so the mirror is the gate tooling's only committed copy), then `git add` + `git commit` in `pageforge-site`. **This file is edited in place only — never rewritten from an older copy** (17 Sept 2026: session 19 did, and the 16 Sept amendments were lost for 78 rounds)."

**1g — §4.** Replace the Plateau and Budget bullets and add two more:
> - **Waiting.** Every remaining class ≥ 20 pages is BLOCKED — needs Chris. This is NOT exhaustion: report it as "the loop needs N decisions", list each with §5 item 4, and point Chris at `/loop-decisions`. Resume only after `LOOP_STATE.md` carries the answers.
> - **Plateau.** Three consecutive shipped rounds **whose PICK predicted a skeleton move** each move the skeleton SCAFFOLD mean by less than 0.02 percentage points AND move no other protected gate. A round the PICK declares gate-neutral by design — text-only, `<head>`-only, a class or attribute the skeleton ignores, a registry correction, a recognition round, a gate-configuration round — neither counts toward the window nor resets it. The window does not fire while the §3 queue still holds a derivable class ≥ 20 pages, or a NOT CAPTURED / AUTHORISED KB row, whose PICK predicts ≥ 0.02pp: a plateau is a statement about the QUEUE, not about the last three picks. Read every delta on the post-intake population (§1e). Stop and report — the next lever needs a human decision, not another round.
> - **Budget.** The round cap or time cap in the kickoff message is reached (`/loop-start` with no argument = 12 rounds or 10 hours, the §7 default). When the time left is less than the next round needs to ship AND prove (≈ 60–75 minutes for an engine round, more with a full regeneration), do not start it: finish that round's PICK and measurement, record them in `LOOP_STATE.md`, and stop.
> - **Widget-BUILD rounds (D10-3).** A build round is invisible to the skeleton score by design, so: (a) the plateau "moved" test is the type's *Still a box* count on `COVERAGE_DASHBOARD.md`, regenerated at the start of every build round and after its regeneration — ≥ 20 sites converted from hand-off box to built widget is progress; (b) the solidify share test does not apply — the writer's tag is the target — while the 20-page floor applies per authoring SHAPE family within the type; (c) exhaustion counts the dashboard's un-built widget rows as queue classes.

**1h — §6.** Add two bullets:
> - **Never rewrite an engine or data file in place from a script.** Write to a temporary file, check it is non-empty and parses (`node --check` for `.js`, a JSON load for `.json`), then move it over the original (r347: a 0-byte `DocxExtractor.js`, rebuilt from the committed blob).
> - **Record every automatic compaction** as one line in `LOOP_STATE.md` — "compaction at HH:MM during rN, step X" — and record why a session ended whenever the reason is not a §4 stop.

Plus the header line **"Amended: 16 September 2026 (the first `/loop-review`, lost 17 Sept, restored 22 Sept) and 22 September 2026 (the second)"**.

**If made:** the rules the loop has mostly been following by habit become rules again; the gate baseline mirror is kept current; a lost-amendment repeat is far less likely.
**If not:** the next session that edits from an older copy loses more; the KB-binding rule, the artefact rule and the compaction log stay absent.
**Recommendation:** apply all eight. (The one lost item I do NOT restore: the §5 git block with a `git log` line — the current two-line block, no `git log`, supersedes it.)

### Proposal 2 — Exhaustion may only be declared after every recorded source is consulted and one unused lane tried (§4)

**Current text (§4 Exhaustion, first sentence):** "ALL of: `DIFF_QUEUE.md` exists, was produced by the §1d miner on the CURRENT corpus, and has no candidate row left (…); `KB_AMALGAMATION_STATUS.md` has no NOT CAPTURED row left with ≥ 20 in-scope pages; and the dashboard backlog has no derivable class ≥ 20 pages."
**Proposed:** keep it and add, after "…no derivable class ≥ 20 pages;":
> and every item in the intake handover's recommended round order (`LOOP_INTAKE__*.md` §7), in `LOOP_STATE.md`'s "Follow-up candidates" section and in its open needs-Chris list has been dispositioned in writing. **An exhaustion verdict is PROVISIONAL until the session has spent one PICK pass on a lane it has not used this session** — the lanes are: the miner's rows; the KB queue; a content-level re-read of the hand-off boxes on disk; the recognition / no-build list; per-family registry rows; the loss ledger's largest family — and the STOPPED entry names the lanes and instruments tried. (Review of 22 Sept 2026: nine exhaustion stops in eighteen sessions; each of the five miner-quoted ones was followed within two sessions by 7–11 shipped rounds and +0.29 to +0.34pp found on a lane the stopping session had not tried; session 30 stopped with two items still recorded in the intake list.)

**If made:** a session that has run out of ideas at 3 h 35 (s30) spends one more pass on a different lane before stopping; the stop entry tells the next session where NOT to look again.
**If not:** the pattern continues — roughly every other session ends early and the next one finds a productive lane.
**Recommendation:** apply.

### Proposal 3 — A family-keyed rule may ship under the 20-page floor; per-group rules count the sum of passing groups (§1d candidate rule and §3 NEW-FAMILY CHECK)

**Current text (§1d):** "A class is a candidate when: modules ≥ 10 … the 20-page floor still applies to body classes …"
**Proposed addition (end of the §1d Candidate rule paragraph):**
> Two exceptions, both because the floor exists to stop a rule learnt on a few pages being applied where it does not belong, and neither can over-reach: (1) a **family dialect** — a rule keyed to one family by a registry row or a family flag — may ship under the floor when it matches that family's own gold on every page of the family, its OFF corpus is byte-identical, and every other gate holds (the r422 FRFUN06 side-tab dialect is the worked example: 10 pages, 8 up / 2 down, parked for want of this rule); (2) a **per-group rule** (a data table keyed by prefix, subject or template with one row per group) meets the floor on the SUM of the groups that each pass consensus ≥ 0.60, not on each group alone (the s27 `<br>` soft-break form: ENGJ 0.97 / HIS 0.65 / EXPFUN 0.99, ≈ 25 pages together).

**If made:** r422 ships next session without a decision from you (item 13 in 3f is closed by the rule); the `<br>` per-prefix registry becomes a candidate; future dialects from intakes stop queueing for you.
**If not:** every dialect under 20 pages is built, proven and parked, and each becomes a line in your decisions list.
**Recommendation:** apply — and if you would rather decide r422 yourself today, say "enable r422" and I will record it under Decisions from Chris either way.

### Proposal 4 — Stale-state sweep of the loop file (§0, §1, §2, §3 step 1)

- §0 item 6: keep the intake pointer; drop "Read this once per session until the loop has shipped three rounds on the new corpus" (it has shipped sixteen).
- §0 item 7 (the round-410 handover): replace with "**`SESSION_28__Pre_Loop_Summary_2026-09-20.md`** — the pre-loop session that rebuilt the registries (r408); round 410 was finished by session 29. CHECK FOR AN IN-FLIGHT ROUND BEFORE PICKING ANYTHING: `LOOP_STATE.md`'s Position section and its 'Next session starts with' line say whether a round is in flight (today: r425, built and shipped inert)."
- §0 census table: Claude module dirs 494 → **495**, Claude pages 2,555 → **2,559**; the sentence below it: "**552 gold dirs against 495 Claude dirs is CORRECT** … 19 modules have no Claude build (the 12 XOTP until the r425 adapter is enabled; 7 with no Writers Template)".
- §1 ceiling paragraph: replace "The ceiling is currently UNMEASURED on this corpus (20 Sept 2026) … `COVERAGE_DASHBOARD.md` is stale for the same reason" with "**The ceiling was re-measured on 20 September 2026 (session 29, `_ceiling_r410`): scaffold 90.9 % (loose 93.5 %) on 2,290 paired pages, full-scope 86.7 %.** Every report quotes '% of achievable' against 90.9 %. Re-run `_measure_ceiling.py` after any intake; `COVERAGE_DASHBOARD.md` was regenerated the same day."
- §2 the 20-modules bullet: "**The modules with no Claude build are NOT converter faults.** 12 XOTP modules are refused until the r425 activity-table adapter is enabled (built 21 Sept, `adapter.enabled: false`; the spec is `00-NEW_NEW_NEW/_SPEC__XOTP_Activity_Table_Template.md`). Seven (`GER1003–1007`, `SAM1005`, `SAM1006`) have no Writers Template at all. PMT101 converts since r423. Do not recreate an empty Claude dir for any refused module."
- §3 step 1: "`python3 reference/tests/_coverage_dashboard.py`" → "`_coverage_dashboard.py` under WSL".

**If made:** a fresh session reads true facts. **If not:** each session spends its first minutes discovering the file is wrong (sessions 30 and 31 both did). **Recommendation:** apply.

### Proposal 5 — §7 and the `/loop-start` skill made identical and state-free again

**What.** One message text, kept in §7 and copied byte-for-byte into `.claude/skills/loop-start/SKILL.md`. It keeps the skill's four useful additions (the pre-19-Sept void, §1e before judging a gate, no native `python3` / run `cs bc` first, the `OPERATING_GUIDE.md` pointer, `$ARGUMENTS`) and drops its state (the census, "round 410 … five files uncommitted", the two once-read files — §0 already lists them). Proposed message:

> Continue the PageForge autonomous loop in this folder. Start with a health check: `git status` in pageforge-site, `bash _MIGRATION/verify_after_transfer.sh` (must PASS), delete every stale git lock in pageforge-site (`.git/index.lock`, `.git/HEAD.lock`, `.git/next-index-*.lock`, `.git/objects/maintenance.lock`, and any `.git/objects/*/tmp_obj_*`), and `wc -c LOOP_STATE.md DIFF_QUEUE.md` — LOOP_STATE.md over 100 KB → condense/archive per §5d BEFORE anything else (over 160 KB = health check FAILED until fixed); never read any file over 100 KB whole (LOOP_STATE_ARCHIVE.md and outputs/_diff_queue_details.md are grep-only). Note the KB repo's HEAD against KB_AMALGAMATION_STATUS.md. Then read LOOP__Autonomous_Rounds.md and LOOP_STATE.md — if LOOP_STATE.md does not exist, do Round 0 and Round 0b first. Reconcile git with the state file: any uncommitted engine or data files belong to the round LOOP_STATE.md names as in progress — never git checkout or git restore them; check them against that round's PICK, finish or toggle OFF, and continue from the step the state file shows; if the Position section names a built-but-inert round, finishing it is Round 1. Honour every entry under "Decisions from Chris" and never re-ask them. THE DIFF MINER (§1d) IS MANDATORY: if reference/tests/_diff_miner.py or DIFF_QUEUE.md does not exist, or DIFF_QUEUE.md is older than the corpus, do Round 0c FIRST — build/re-run the miner, commit DIFF_QUEUE.md — and take the PICK from it (chrome regions first: module-code chip, title, module menu, crumbs/side-nav, footer). Any exhaustion verdict reached before 19 September 2026 and any "do not re-measure" note in LOOP_STATE.md are VOID; exhaustion may only be declared under §4's full test with the miner's queue quoted. BEFORE JUDGING ANY GATE READ §1e: when a gate looks worse, split it by population or run _content_manifest.py fresh; never stop on a plateau or a regression you have not split. Never call python3 from the Bash tool on this machine (the Windows Store stub hangs 30 minutes) — every Python and gate runs under WSL; _gatecheck.py prints CACHED rows for gates it did not run, so run `cs bc` before believing the compare_structure or body_compare lines. This message carries the code REGENERATE CORPUS for every round of the loop, scoped by the §0a/§0b family rules in OPERATING_GUIDE.md (the converter guide; CLAUDE.md is only a pointer to it). Budget for this session: $ARGUMENTS — if that is blank, 12 rounds or 10 hours, whichever comes first. RUN UNINTERRUPTED (§5c): never end your turn to wait for gates, regenerations, verifiers or background commands — run them in the foreground with a long timeout or poll them until done; never ask me whether to continue; a blocked item ends the round, not the session — record it and move to the next class. Follow the §6 context-diet rules: never read OPERATING_GUIDE.md or BUILD_CHANGELOG.md whole, and after every automatic compaction do ONLY the bounded §5d re-read and log the compaction in LOOP_STATE.md. Update LOOP_STATE.md before and after every round and commit after every round, never push. Stop only when §4 says so; then give me the §5 plain-English report with the copy-and-paste push block, and end LOOP_STATE.md with a "Next session starts with:" line.

(In §7 the `$ARGUMENTS` placeholder is written as "the budget you typed after `/loop-start`, or if blank 12 rounds or 10 hours".) The `/loop-stop` message is unchanged.

**If made:** the message is true again and needs no editing after the next intake — the state stays in `LOOP_STATE.md` as §7 intends. **If not:** every session keeps reading a false "decide round 410 first". **Recommendation:** apply.

### Proposal 6 — A settings hook that refuses native `python` in the shell (`.claude/settings.json`)

**What.** A pre-command hook: before any Bash command runs, a two-line script checks whether the command invokes `python` or `python3` other than through `wsl`; if so it refuses with the message "python runs under WSL on this machine (LOOP §6)". Files: `.claude/hooks/no_native_python.sh` (new, ≈ 10 lines) and this addition to `.claude/settings.json`:

```json
"hooks": {
  "PreToolUse": [
    { "matcher": "Bash",
      "hooks": [ { "type": "command", "command": "bash .claude/hooks/no_native_python.sh" } ] }
  ]
}
```

**If made:** a slip costs one second and a clear message instead of thirty minutes (five slips so far, ≈ 2.5 hours, all after the rule was written down). **If not:** the rule stays a written rule that has already failed five times. **Recommendation:** apply; I will test the hook on a harmless command before committing it, and it is a one-line removal if it misbehaves.

### Proposal 7 — Refresh the committed gate baseline now (housekeeping, no rule change)

Copy the live `CONVERTER_V2/reference/tests/gate_baseline.json` (round 423, 2,353 pairs) over the mirror `pageforge-site/converter-v2/loop/gate_baseline.json` (round 410, 2,349 pairs), prove `cmp` identical, commit with the review. The 16 Sept review did exactly this. **If made:** git carries the current baseline. **If not:** a power cut loses twelve rounds of baseline notes. **Recommendation:** apply.

### Proposal 8 — KB status housekeeping (two lines)

`KB_AMALGAMATION_STATUS.md`: the "KB re-checked" header line → "22 September 2026 (`/loop-review` — HEAD `44c7c8e`; CL-0096 → CL-0100 are the skills / documentation publications of 20–21 Sept, no module rule; constraints 1–92 and the `14_` families unchanged since `469f496`)"; the §C heading → "CL-0001 → CL-0100 (0096–0100 no PageForge action)". **Recommendation:** apply.

### Proposal 9 — One standing "Needs Chris" list in `LOOP_STATE.md` (§5b gets one sentence)

Add a section `## Needs Chris — open decisions (one line each, oldest first, pages held up)` holding the fifteen items of 3f, and a §5b sentence: "Every needs-Chris item is ONE line in `LOOP_STATE.md`'s 'Needs Chris' section — a STOPPED entry points at it and never restates it; `/loop-decisions` reads it first." **If made:** the next `/loop-decisions` has one list instead of six scattered ones, and STOPPED entries stop saying "the five items of the session-26 entry stand". **If not:** the list keeps growing in six places. **Recommendation:** apply.

---

## 6. What Chris said, and what was then applied (22 September 2026, the same session)

After the nine proposals were put to him, Chris gave three standing instructions, recorded in
`LOOP_STATE.md` as D12-1 / D12-2 / D12-3. His words:

> "When performing this review in the future, I would like you to automatically carry out all of your
> recommendations when it comes to any potential issues you identify when carrying out this review, and
> make any and all changes to the loop instructions and automatically amend the next starting loop (which
> will then have any required updated instructions to ensure all future loops carry out the development
> work to the standard that you discern needs to be applied and the instructional framework that will
> provide virtual scaffolding for this project to continue operating as autonomously as possible.). Also
> take note that from time to time there will be new modules introduced into the human developer module
> folders that will need to be taken into account by Claude by setting up the claude generated equivalent
> files and folders that relate to these new modules and then ascertaining all of the discrepancies be
> amalgamated into the loop pipeline and then to have the pending tasks in the loop to be reassessed and
> reprioritized based on this new information. Please now put this info into action now as part of this
> same loop-review, and make sure these requests are all implemented for the future."

**Applied in this session (the "nothing is applied until you say so" line in §4 is superseded):**

| # | change | where |
|---|---|---|
| 1 | the twelve lost amendments restored (1a–1h), plus the "Amended:" header and the edit-in-place rule | `LOOP__Autonomous_Rounds.md` header, §0, §2, §3 steps 3 / 5 / 6 / 7, §4, §6 |
| 2 | exhaustion needs every recorded source dispositioned and one untried lane | §4 |
| 3 | family dialects and per-group sums may ship under the floor (r422 is authorised) | §1d, §2 |
| 4 | the stale-state sweep (census 495 / 2,559 / 2,353 pairs; ceiling 90.9 % measured; PMT101 converts; XOTP adapter inert) | §0, §1, §2, §3 step 1 |
| 5 | the start message rewritten as one state-free line, kept byte-identical in the skill, with a mechanical diff check | §7, `.claude/skills/loop-start/SKILL.md` |
| 6 | the native-python hook, tested on eight commands (three native forms blocked, two WSL forms and three non-python commands allowed) | `.claude/settings.json`, `.claude/hooks/no_native_python.sh`, §6 |
| 7 | the committed gate baseline refreshed to round 423 (2,353 pairs), `cmp` identical | `pageforge-site/converter-v2/loop/gate_baseline.json` |
| 8 | the KB status header (HEAD `44c7c8e`, CL-0096–0100 non-module) and the §C heading | `KB_AMALGAMATION_STATUS.md` |
| 9 | the one "Needs Chris" list (15 items, #13 settled by rule) and the §5b sentence | `LOOP_STATE.md`, §5b, `/loop-decisions` skill |
| D12-1 / D12-2 | `/loop-review` applies its recommendations and rewrites the next starting message itself; asks only for converter code / data changes, regeneration, deleting a decision, or a push | `.claude/skills/loop-review/SKILL.md` (rewritten), §7's command descriptions |
| D12-3 | **§1f — Round 0d, the INTAKE ROUND**: the trigger on the census, the one exception to the read-only gold rule (additions only), and eight phases reconstructed from the two intakes' records with every tool verified on disk — provenance / classification / placement, the Claude equivalents, all registries in one round, the full regeneration with the population split, the voided instruments (ceiling, dashboard, miner), the records and the handover file, the re-ranked queue, the stop | `LOOP__Autonomous_Rounds.md` §1f, §0 (the trigger), §2 (the authorisation), §7 (the message) |

**Adversarial check, and one more health finding.** After the first commit, four independent readers were set on the amended files (contradictions; completeness of the restored text and of §1f's tool names; a fresh-session dry run of the start message; the state file). The first two reported 27 + 17 findings; every must-fix and should-fix was applied in a follow-up commit. The largest is a new health finding: **the gold-only gap is 57 modules, not 19.** Thirty-eight pre-intake modules (the BLL243–BLL276 block, CEDK401, CEDO201, CEDO402, CEDR101, CEDR203, CEDR401, CEDT102, CEDW303, HPRE301, OSSM501, SSCI104, SSEA203, SSOG105, TRR110, TWHK902, TWHK907, TWHR905, TWHR907, TWHT903, XMES202) each hold a Writers Template and its parsed text but have never been converted, and no full regeneration ever reaches them because the batch planner enumerates Claude directories. They were on no recorded list; they are now listed in §0 and are the next session's Round 3 (a Round 0d over just those 38). The other corrections: §1f's staging-area trigger would have fired every session on leftovers the September audit already dispositioned; §1f's phases 3 and 4 were in the wrong order (the full regeneration must re-base on unchanged registries, then the registry rebuild is its own scoped round, as on 19–20 September); two tool paths were wrong; the verify script's expected counts must be updated at any finalise that changes them; the exhaustion "untried lane" rule was undefined at both ends.

Three readers reconstructed the intake procedure before §1f was written (the 19 September intake in 30
steps, the 3 August precedent in 13, and 29 tools each confirmed present on disk); their reports are in
this session's workflow transcript. Two things the record did not supply and §1f now asks for on the next
intake: a script for the nested-dir pre-creation and the ghost-dir removal, and a reusable population-split
script (`outputs/_intake_split.cjs`, generalised from `_s28_t1_split.cjs`).

## 5. What this review did not do

No round, no converter code or data change, no regeneration, nothing under `01-Finalized_Modules_` or `01-Claude_Modules_` touched, the KB repo untouched, nothing pushed. The loop's next Round 1 is still "finish r425" exactly as the 21 September "Next session starts with" line says (and, if proposal 3 is approved, r422 is enabled in the same session).

**Next `/loop-review`:** after the quiz-engine decision (item 4) is actioned or after ≈ 30 more rounds, whichever comes first — and in either case the first check is that the "Amended" header line is still there.
