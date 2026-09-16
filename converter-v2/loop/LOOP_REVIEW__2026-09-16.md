# LOOP_REVIEW__2026-09-16.md — the first health review of the PageForge autonomous loop

**Written:** 16 September 2026, evening, by a `/loop-review` session (a review, not a loop run: no round was started, no converter code or data changed, nothing regenerated).
**Period reviewed:** the whole life of the loop so far — 14 September (round 313, the starting state) to the session-12 stop at round 347. There has been no earlier review, so "since the last review" means "since the loop began".
**Who it is for:** Chris. Every technical term is defined the first time it is used.

---

## The words used in this report

- **Round** — one pass of the loop: pick a class of mismatch, measure it across the whole library, fix it behind a switch, rebuild the pages it touches, prove no score got worse, write it up, commit. Rounds are numbered by the engine build they produce (r314 … r347).
- **Session** — one Claude Code conversation. Twelve so far (session 10 was a decisions session, not a loop run).
- **The gold** — the human developers' finished modules under `01-Finalized_Modules_/`. Read-only.
- **The KB (knowledge base)** — the HTML Convertor rulebook under `00-Other-TK-Resources/htmlconvertor-kb/`: numbered *constraints* (rules), a *change ledger* of dated decisions (`CL-0001` onward), and *family rules* (document 14) for particular subjects.
- **The skeleton score (SCAFFOLD)** — the main number: how closely the structure of each PageForge page (rows, columns, activity boxes, headings) matches the matching gold page, with the insides of interactive widgets ignored. Reported as a mean over all paired pages. **pp** = percentage points of that score.
- **The ceiling** — the share of the gold's structure that has *some* source in the writer's Word document. Structure the developer invented has no source and no converter rule can ever produce it. The ceiling is 91.9%, so "% of achievable" = score ÷ 91.9.
- **A gate** — one of the automatic scores that must never get worse (the skeleton score and its ≥50 / ≥75 / ≥90 buckets, "structurally clean", the literal-tag leak count, compare_structure, body_compare, the tag-regression count, and one *verifier* per built widget type).
- **A named override** — when the loop follows a KB rule the gold does not, the pages that score lower are listed by name and excluded from the "must not get worse" test. Intentional, not a bug.
- **Declined** — a class the loop measured and decided not to build, because fewer than 60% of the gold's group does it (the *solidify floor*), or it is a tie, or there is no signal in the writer's document to drive it. Recorded, never re-attempted without new evidence.
- **Blocked** — a class the loop could not settle on its own and parked for Chris.
- **Compaction** — Claude Code automatically summarising an over-long conversation to free memory. The summary keeps the gist but not the rules, which is why the loop re-reads its two files after each one.

---

## 1. Health check — PASS, with two housekeeping findings

| check | result |
|---|---|
| `git status` in pageforge-site | clean; branch `main` at `27dbdf9`, up to date with `origin/main` (so the last push has been done) |
| `git log` | the 30 newest commits are the loop's rounds r330–r347 and their state records, in order |
| stale `.git/index.lock` | none |
| `verify_after_transfer.sh` | PASS on all six sections (5 symlinks, 62 engine files, 81 gate tools byte-identical; census 454 gold / 416 Claude / 2110 pages; both git histories intact; node 24 / python 3.14 / git 2.55). One WARN: the transfer snapshot still names `9fb3ebd` (round 313) as HEAD — harmless, the script itself says "fine if you have since committed" |
| `.claude/settings.json` | `defaultMode: auto`; shell timeout 30 min default / 60 min ceiling — matches §5c |
| `loop-start/SKILL.md` vs §7 start message | identical except the intended `$ARGUMENTS — if that is blank,` budget hook that §7 itself documents |
| `loop-stop/SKILL.md` vs §7 stop message | identical, word for word |

**Drift found inside the loop file itself.** §4 "Budget" still says *default: 10 rounds per session … default: 6 hours*, while the §7 message (the one that actually runs) says *12 rounds or 10 hours*. Sessions 11 and 12 ran on `10 rounds or 3 hours`. The file disagrees with itself; proposal 4 fixes it.

**Two more project commands exist that §7 does not mention:** `/loop-decisions` (used in session 10) and `/loop-review` (this one). Proposal 11 adds one sentence.

**One committed file is stale.** The loop mirrors its instruments into `pageforge-site/converter-v2/loop/` at each commit so nothing is lost between sessions. The mirror of `gate_baseline.json` (the committed record of every gate's last proven value) was last refreshed at round 340; the live copy in `CONVERTER_V2/reference/tests/` is at round 347. Seven rounds of baseline are in git only as changelog prose. Every other mirrored file checked (`LOOP_STATE.md`, `KB_AMALGAMATION_STATUS.md`, `run_all_gates.sh`) is byte-identical to its live copy. Proposal 9.

---

## 2. What was read

`LOOP__Autonomous_Rounds.md` in full (317 lines). `LOOP_STATE.md` by section: the twelve session banners, every "Decisions from Chris" section (sessions 2, 5, 6, 8, 9, 10), Declined classes, Blocked classes, the Round log, the ceiling record, the environment notes, and the "Next session starts with" line. `KB_AMALGAMATION_STATUS.md` §D (the KB queue) and §E. The four newest `BUILD_CHANGELOG.md` entries (r344–r347) and the gate lines of every loop entry back to r314. The live and committed `gate_baseline.json`, the skeleton result files `_r340` … `_r347_sk_final.json`, the r347 gate log, `COVERAGE_DASHBOARD.md`, the ship ledger, and `run_all_gates.sh`. In the KB repo: `git log` since 13 September, the newest ledger part (`12E6`, CL-0093–0095), and `12G` (the PageForge-facing log).

---

## 3. Assessment

### 3a. KB drift — **change needed (small)**

- **The KB has moved one commit past the audit.** `KB_AMALGAMATION_STATUS.md` was built against KB commit `ee2853c` (14 Sept). The KB is now at `469f496` (16 Sept 06:02 UTC): "Assessment Mode (Mode 9)". It adds `18_ASSESSMENT_MODE.md` (converting an NCEA assessment Word template into a single assessment page — a different product, not a module), splits 00A into 00A2, and gives constraint 2 an Assessment-Mode-only exception. **No new CL row** (the commit says so), no change to any `14_` family file, nothing that a module conversion must follow. The highest CL is still CL-0095 — the status file already knows it. Verdict on the content: nothing to queue. Verdict on the record: the status file should say which KB commit it was last checked against, and the loop's health check should re-check it each session.
- **The KB repo has an untracked stray file:** `Claude outputs/Assessment-US4249.html`. Not the loop's business, but Chris should know it is sitting uncommitted in the KB folder.
- **Five places where the converter now deliberately disagrees with the KB's wording, by Chris's decisions, and the KB has not yet been edited:** stickyNav (14A/14B/14D say add it; D10-4 keeps the ban), equations (05A says LaTeX; D10-7 ships MathML), tables (06 §6 says `table noHover tableFixed`; D10-5 makes 05D's `table table-bordered` the rule), bilingual lesson titles (00G c79 / 01A say nothing about order; D10-2 makes Standard modules English-first), and `alertPadding` (01F/05B example, D10-8 says it is an example not a default). These were recorded on 16 Sept as "an Admin-Mode KB round — the KB is untouched". The loop is right to follow the recorded decision (§5b), but until the KB is edited, any future reader of the KB alone will be told the wrong thing five times. Owed work, listed in §3f.
- **12G's "PageForge status" lines are all stale.** `12G_PAGEFORGE_AMALGAMATION_LOG.md` is the KB's own list of decisions written for PageForge; its rule is that the `PageForge status:` line is updated when a round implements the rule. All six entries (CL-0089, 0090, 0091, 0093, 0094, 0095) still read "Not yet amalgamated", though CL-0089 shipped in r319, CL-0090 in r317, and CL-0091 was already live. `KB_AMALGAMATION_STATUS.md` §E promised this reciprocal update; it has never been made.
- **One over-claim in the status file.** §D row 7 reads "c47 / c95 … SHIPPED round 344". Round 344 implemented constraint 47 (drop the opening body heading that repeats the title). Constraint 95 (CL-0095, 13 Sept: strip a leading label such as `FUNdamental:` from a body heading, then apply c47) is **not** in the engine — the only "label prefix strip" in the code is the tab-widget one (`Tab 1: Step 1` → `Step 1`, round 293). Its `Lesson N` half is covered by r324/r344; its `FUNdamental:` half (the reported WJFUN112 case, measured at 12 pages in r320 — under the 20-page floor) is not. The row should say "c47 SHIPPED; c95's label-prefix half NOT CAPTURED (12 pages, under the floor)".
- **No conflict found between the KB and any rule the loop shipped on its own authority** (the near-red tags r341, the hyperlinked media tags r342, the video-button/link embeds r339/r340, the external-button r338 — the KB is silent on each, and the changelog says so each time).

### 3b. Progress — **fine as is on the numbers; change needed on the plateau rule (see 3c)**

The scorecard from the starting state to now (the first loop round's baseline is used for the bucket counts; the mean is the pre-loop r313 figure):

| gate | start (r313 / r314 @ 1939 pairs) | now (r347 @ 1955 pairs) |
|---|---|---|
| skeleton SCAFFOLD mean | 49.941% | **51.283%** |
| as % of achievable | 54.5% (ceiling 91.6%) | **55.8%** (ceiling 91.9%) |
| pages ≥50 / ≥75 / ≥90 | 1005 / 192 / 16 | 1074 / 198 / 15 |
| structurally clean | 2056 / 2102 = 97.81% | 2080 / 2103 = 98.91% |
| literal-tag leak (occurrences / pages) | 288 / 46 | **26 / 23** |
| compare_structure exact / EXTRA / missing | 11355 / 186 / 591 | 11464 / 175 / 607 |
| body_compare breakdowns | 192 | 180 |
| tags handled | 9557 / 9557 | 9557 / 9557 |
| widget selftests | 12 | 14 (mtkQuiz r322, math r346 added) |

**Where the +1.342pp came from.** +0.258 was the pairing-parser repair in r315 (a measurement fix — 15 more true page pairs — not a converter gain, and recorded as such). +0.135 was the r343 population change (Chris's D10-6: eight edit-brief modules leave the comparison set — recorded as "never a gain"). The converter itself earned **≈ +0.95pp over 32 engine rounds**, about +0.03pp per round. Six rounds supplied three quarters of it: r332 footers +0.269, r334 activity titles +0.167, r314 upload boxes +0.090, r333 side alerts +0.066, r326 button anchors +0.057, r316 bilingual titles +0.056. The ≥90 bucket fell 16 → 15 at r317 (a named KB-over-gold override on the acknowledgements block) and has stayed there.

**The one big non-skeleton win** was r341: the literal-tag leak fell from 288 occurrences on 46 pages to 26 on 23, and "clean" rose 97.81% → 98.91%, because a writer's tag typed in a slightly different red had been shipping as literal text on 30 modules. That gate had never had a round picked for it before session 9.

**Rounds and sessions.**

| session | date, start → stop (NZST) | hours | rounds shipped | how it stopped |
|---|---|---|---|---|
| 1 | 14 Sept | — | 0 (Round 0 + 0b; r314 started) | Chris: "STOP THE LOOP NOW" (context filled) |
| 2 | 14 Sept 23:21 → 15 Sept 03:43, resumed 07:48 → 08:15 | ≈ 4.8 | 8 (r314–r321) | budget (10 h) |
| 3 | 15 Sept 09:41 → 13:10 | 3.5 | 4 (r322–r325) | plateau |
| 4 | 13:27 → 15:45 | 2.3 | 4 (r326–r329) | plateau |
| 5 | 16:05 → 20:05 | 4.0 | 5 (r330–r334) + full backstop; r335 built | Chris's stop |
| 6 | 20:49 → 22:40 | 1.9 | 3 (r335–r337) | plateau |
| 7 | 23:06 → ≈ 01:00 | ≈ 2 | 2 (r338, r339); r340 coded | **no record of why it ended** |
| 8 | 16 Sept 08:03 → 10:10 | 2.1 | 1 (r340) | exhaustion |
| 9 | 09:21 → 11:10 | 1.8 | 1 (r341); r342 built | Chris's stop |
| 10 | ≈ 14:00 → 15:30 | — | 0 (`/loop-decisions`) | not a loop run |
| 11 | 15:27 → 17:20 | 1.9 | 2 (r342, r343) | budget (3 h) |
| 12 | 18:18 → 20:45 | 2.5 | 4 (r344–r347) | budget (3 h) |

Totals: **34 shipped rounds in ≈ 27 hours of loop time — about 47 minutes per round** including every measurement that ended in a decline. Outcomes per attempted class: 34 shipped; about 20 measured and declined (every one with its probe and numbers recorded); 6 blocked for Chris, all six answered in the one `/loop-decisions` session. No round ever reached the three-attempt repair limit; the "two blocked in a row" stop never fired.

**Stop reasons across eleven loop sessions:** budget 3, plateau 3, Chris's instruction 3 (sessions 1, 5, 9), exhaustion 1, unrecorded 1 (session 7).

**Is the plateau rule firing for the right reason? No.** All three plateau stops were followed by a gate-moving round in the very next session:

- Session 3 stopped on r323 0.000 / r324 +0.005 / r325 +0.019. Session 4's first round (r326) moved +0.057.
- Session 4 stopped on r327 0.000 / r328 0.000 / r329 +0.004. Session 5 then shipped **+0.564pp in five rounds** — the loop's best session.
- Session 6 stopped on r335 +0.018 / r336 0.000 / r337 +0.001. Session 7's first round (r338) moved +0.023.

In sessions 3 and 4, two of the three window rounds were **text-only KB rounds that could never move the skeleton** (r323 removes a full stop from button labels; r327 sentence-cases a title; r328 lengthens a label). They were correct, KB-required work, but counting them toward "the score has plateaued" is a category error. The loop noticed: from session 12 it started writing "plateau window (both §4 conditions)" and excluded gate-neutral r345 as "1 of 3" — an interpretation, not a rule. Proposal 1 makes it the rule.

### 3c. Rule quality — **change needed in three places; fine in three**

- **The 0.60 solidify floor — change needed.** It is the right test when the target comes from the gold (authority levels 3–4). It was wrongly consulted twice when a numbered KB constraint already covered the element: constraint 47 was DECLINED in r320 because the gold keeps the duplicate heading 43% of the time ("share 0.57 < 0.60 … c47 is pre-ledger documentation, not a locked admin decision"), and constraint 23's label form was BLOCKED in session 8 because the gold's overview convention sits at 0.80. §1b already says a `00_MASTER_INSTRUCTIONS` constraint outranks the gold; the loop invented a "pre-ledger vs locked" distinction the file does not contain. Chris confirmed the KB on both (D10-1, D10-9). Against that, Chris sided with the gold on `alertPadding` (a component-doc example, not a numbered rule) and with his own project instruction on stickyNav (a family note vs `00_PROJECT_CONTEXT_AND_PHILOSOPHY.md`) — so the binding rule must be limited to numbered constraints and front-facing CL rows, and KB-internal conflicts and KB-vs-project-instruction conflicts must still block. Proposal 2.
- **The 20-page floor — fine as is, but its home is wrong.** The floor is written in §1c (KB rows) and §4 (exhaustion), never in §3's PICK step, so the loop treats it as a soft convention: r320 shipped 6 pages "on the r320 precedent", r337 shipped 24 pages and still called itself "under the floor". Nothing bad resulted (each small ship was a proven, gate-neutral-or-better hygiene fix) and the floor did its real job in the exhaustion tests. Proposal 2 mentions it once in §3 so precedent stops standing in for rule.
- **The three-attempt repair limit — fine as is (never exercised).** No round needed a second attempt; every gate regression was a named override or an explained pool change. Untested, not proven.
- **Per-template / per-subject grouping (§1b) — fine as is, and working.** r347 measured tables per template (Standard 0.51 tie, Inquiry 0.72, Fundamentals 0.69, Bilingual 0.86) and named the Standard dip as the override; r345 scoped English-first to Standard and left MTK Māori-first; r330/r331 were Bilingual-only; r336 corrected five Fundamentals families individually.
- **The authority order — change needed** (the same change as the floor, Proposal 2): numbered constraints bind; component-doc forms, KB-internal conflicts, and KB-vs-Chris conflicts block.
- **Dips named as "artefacts" that recur — change needed.** "The scorer's repeat-collapse / alignment artefact" is named in **10 of the 34 rounds** (r326, r329, r330, r331, r335, r336, r338, r339, r340, r344), with single-page dips of −10.31pp (PES1002_4_0) and −6.17pp (MXFU302_1_0) in r344 alone. Each naming is plausible and some carry a companion number ("position-free overlap RISING"), but the loop has no rule requiring that number, and a −10pp page dip attributed to the instrument ten rounds running is exactly the pattern §3 was written to prevent. The r315 pairing-parser repair shows the right response: fix the instrument once. Proposal 3.
- **The stop rules — one gap.** Session 8 stopped on "EXHAUSTION — the GOOD ending" while six classes covering thousands of pages sat BLOCKED on Chris. The real state was *waiting for decisions*, which §4 has no name for, so the report told Chris the loop was done when it was stalled. It took a separate session to unblock. Proposal 5 adds a "Waiting" stop reason.

### 3d. Gate health — **fine as is on the measurements; change needed on two records and one habit**

- **Pairing parser:** repaired in r315 (void-aware; 1939 → 1954 true pairs, explained). `pairs skipped (parse error)` is **0** in every skeleton result file from r340 to r347 and in every changelog gate line back to r314.
- **Baseline moves, all explained:** r315 +15 pairs (the repair), r341 +8 pairs (HIS1005 now ships the gold's exact 15-page set), r343 −7 pairs (the CED exclusion). Buckets, clean, leak, body and tags line up round to round.
- **One unexplained stale field:** the live `gate_baseline.json` says `skeleton.pairs: 1954`. It has been 1955 since r343; every other field in the file was refreshed. Cosmetic, but a baseline file must be wholly right or it is not a baseline. Proposal 9.
- **Two verifiers print a red RESULT line every run and the loop has learned to read red as "at baseline".** In the r347 gate log the speechBubble verifier ends `RESULT: real defects present ✗ — fix before proceeding` (defect 4, unchanged since r313, A/B-proven pre-existing) and the new math verifier ends the same way (defect 1 = PES1007's pre-existing page-tail loss, named). Neither is passing vacuously — the opposite: they are permanently failing, and every round the loop writes "at its standing baseline" past a line that says stop. That is a habit the loop must not be allowed to keep; a verifier should be green at its recorded baseline and red only above it. Proposal 10 (a small tooling round, not for this session).
- **Vacuous-pass check:** `_verify_mtkquiz.cjs` and `_verify_math.cjs` both carry a liveness/detection selftest (a doctored shell must raise); the entry-parity gate has `--selftest`; 14 selftests are GREEN at r347. The gate suite's widget verifiers run on fixed 4–11 module samples, so on their own they could miss a module outside the sample — the loop compensates by running each touched widget's verifier over its whole family per round (ten family logs at r341). Fine as is.
- **The coverage dashboard is stale.** `COVERAGE_DASHBOARD.md` was generated at 09:26 on 16 Sept (449 modules / 2102 pages, three freshness warnings) — before r341–r347 changed 2110 pages. D10-3 makes its *Still a box* count the "moved" test for widget-build rounds and says to re-run it at each kickoff; the §4 amendment does not say so. Proposal 6.

### 3e. Session mechanics — **change needed (three small tightenings); §5c is working**

- **Stalls.** §5c was added on 15 Sept after the loop stalled "several times" waiting for Chris to type "continue" (session 6 at 21:10 records one: "continue the loop once the gates finish"). Since §5c entered the kickoff message (session 7 onward) no session records being prompted. §5c is working.
- **Session 7 ended without a stop record.** It shipped r338 and r339, coded r340, and stopped; session 8's health check found three uncommitted engine files and reconciled them from the PICK — exactly as §7 intends — but nothing says why session 7 ended (context, a closed window, a crash). The loop cannot learn from an ending it did not record.
- **Compactions: cannot be assessed.** The loop file makes re-reading after compaction the first action, but no session has written down that a compaction happened, so the count per session is unknown. Session 1 is known to have filled 1M of context in an hour (the §6 note); nothing since. Proposal 8 asks for one line per compaction.
- **Commands past the timeout:** none recorded after §5c. A full regeneration is 36 batches under 4 workers in ≈ 17–20 minutes; the gate suite ≈ 12–15 minutes; both fit the 30-minute shell timeout.
- **A recurring mechanical defect:** the batch runner's oembed-cache write race fails about 3 of 36 batches on every full regeneration (r347: batches 15, 21, 26 re-run singly, rc 0). Known, worked around each time, never fixed.
- **A near-miss in r347:** a helper script opened `DocxExtractor.js` for writing before encoding its new content, hit an encoding error, and left the engine file at **0 bytes**. It was rebuilt from the committed blob with `git show` (never a checkout) and the round shipped. The environment notes already say "long writes go through the Write tool"; the loop's lesson list says "encode first, then open". Neither is in the loop file. Proposal 8 makes engine writes atomic.
- **§3 step 5 is stale:** it tells the loop to rebuild "via `_batch_plan.py` and `_regen_safe.sh`", but `_regen_safe.sh` hard-codes the old sandbox's 40-second wall and the loop has (correctly) run `batch_convert.cjs` directly since session 1. Proposal 7.
- **Budget use in the 3-hour sessions:** sessions 11 and 12 each stopped with 45–70 minutes unused because the next round (a full regeneration plus a new verifier) could not ship *and prove* in the time left; both used the tail to finish the next round's measurement and record it. That is the right behaviour, and Proposal 4 writes it down.

### 3f. Decisions and work owed by Chris — none blocking, four worth a sentence each

Session 10 left "Still open for Chris: NOTHING", and that is true of the recorded queue. Four items have arisen or remain that only Chris can close, oldest first:

1. **16 Sept 15:20 — the widget-build reading of §4 (D10-3's "Chris to veto if wrong" paragraph).** The loop wrote its own rule for how build rounds count toward the plateau test. Not yet confirmed or struck. Holds up 0 pages today; governs ≈ 2,400 un-built widget sites once build rounds start.
2. **16 Sept 15:20 — the five KB edits your decisions imply** (stickyNav 14A/14B/14D, 05A → MathML, 06 §6 → 05D, 00G/01A English-first, 01F/05B `alertPadding` note). An Admin-Mode session in the KB project, one CL row each. Holds up no loop pages; leaves the rulebook wrong in five places until done.
3. **16 Sept ≈ 20:30 — D10-5's `tableFixed` half.** You asked for `table tableFixed` on true two-column comparison tables. The loop measured the gold's 13 contrast-header tables, found them split four ways, declined that half and shipped the hook OFF. Accept the decline, or supply the comparison-word list you want? 13 tables / ≈ 13 pages.
4. **16 Sept 20:35 — D10-9's wording half.** Your Option A normalises the success label by year level (`I can:` for years 7–10, `You will show your understanding by:` for years 1–6). The pre-measurement found **no year-level data exists** — the module code's digit is not a year (digit 1 = NCEA1, years 11+), and the 1–10 series is mixed at every digit — though each module is internally consistent. The loop will ship the `<h5>` form on every label and keep the writer's own wording (the KB's "level unknown" clause) unless a per-module year list arrives as data. Accept that fallback, or supply a year list (≈ 130 modules)? Holds up the wording half on ≈ 1,056 lesson pages + ≈ 296 overview pages; the form half proceeds regardless.

Housekeeping the loop side can do without a decision (needs only your OK): the KB status header (KB HEAD checked), the row-7 wording (c95 not captured), the 12G "PageForge status" lines (six one-line edits in the KB repo — or a list of them for your next KB session), the `gate_baseline.json` mirror, and the stale `skeleton.pairs` field.

---

## 4. Proposals — concrete changes to `LOOP__Autonomous_Rounds.md`

Each proposal gives the current text, the proposed text, what happens if it is made, what happens if it is not, and a recommendation. **None changes the §7 start or stop message, so neither SKILL.md needs to change.** Nothing here has been applied.

### Proposal 1 — Plateau counts only rounds that could have moved the score  (§4)

**Current:**
> **Plateau.** Three consecutive shipped rounds each move the skeleton SCAFFOLD mean by less than 0.02 percentage points AND move no other protected gate. Stop and report — the next lever needs a human decision, not another round.

**Proposed:**
> **Plateau.** Three consecutive shipped rounds **whose PICK predicted a skeleton move** each move the skeleton SCAFFOLD mean by less than 0.02 percentage points AND move no other protected gate. A round the PICK declares gate-neutral by design — text-only, `<head>`-only, a class or attribute the skeleton ignores, a registry correction, a gate-configuration round — neither counts toward the window nor resets it. The window does not fire while the §3 queue still holds a derivable class ≥ 20 pages, or a NOT CAPTURED / AUTHORISED KB row, whose PICK predicts ≥ 0.02pp: a plateau is a statement about the queue, not about the last three picks. Stop and report — the next lever needs a human decision, not another round.

**If made:** sessions 3, 4 and 6 would have continued into r326, r330–r334 and r338 instead of stopping and waiting for a kickoff; the rule fires only when the queue is genuinely flat. **If not:** every run of KB hygiene rounds will keep stopping the loop for the wrong reason (3 of 3 plateau stops so far). **Recommendation: make it.**

### Proposal 2 — A numbered KB constraint is binding; the 0.60 floor is for gold-derived targets  (§2 Declines, plus one sentence in §3 step 3)

**Current (§2, second bullet):**
> **Declines.** A class may be DECLINED without asking Chris when the r182 solidify procedure says so: the measured share of the corpus that follows the candidate rule is below 0.60, or it is a tie, or there is no derivable discriminator. …

**Proposed (append to that bullet):**
> The 0.60 floor and the tie test apply only when the target comes from authority levels 3–4 (this module's gold, or template / subject consensus). When a numbered `00_MASTER_INSTRUCTIONS` constraint or a front-facing CL row covers the element (level 1), the gold share is not consulted: the KB form is the target, the gold's disagreement is a NAMED override (§1b "Gates and KB overrides"), and the round ships — whether or not the constraint has a CL row of its own. BLOCK for Chris only when (a) two KB documents disagree with each other, (b) the KB disagrees with one of Chris's own project instructions, or (c) the KB offers a component-doc example rather than a numbered rule and the gold contradicts it at ≥ 0.60. The 20-page floor is a PICK floor: a class under it is recorded, not built, unless it rides along with a round already in scope and is proven the same way.

**Current (§3 step 3, last sentences):**
> … If the share is < 0.60 or tied in every group → DECLINE (§2), log it, go to 1. …

**Proposed:**
> … If the target is gold-derived and the share is < 0.60 or tied in every group → DECLINE (§2), log it, go to 1. If a numbered constraint covers the element, skip the share test — measure only the override list. …

**If made:** c47 and c23 would have shipped in September's first week as named overrides, as Chris later decided; stickyNav, the table conflict and `alertPadding` would still have blocked (they fall under a–c). **If not:** the loop will keep declining or blocking KB-required work on a gold share the KB was written to overrule, and Chris will keep being asked questions §1b already answers. **Recommendation: make it.**

### Proposal 3 — An "artefact" dip needs a number, and a recurring artefact gets its own repair round  (§3 step 6)

**Current (§3 step 6, end):**
> … If a gate regresses: **debug, never revert** (§0a). Up to **three** repair attempts inside the round. …

**Proposed (new sentences before that):**
> A page dip may be attributed to the scorer's alignment or repeat-collapse artefact only when a companion number on that page rises — the position-free overlap or the uncollapsed matched-line count — and both numbers are written beside the page name. When the same artefact has been named in three shipped rounds, the next PICK is a measurement-tool round (the r315 pairing-parser precedent) that makes the scorer report the companion metric itself.

**If made:** the next artefact claim carries its proof, and the scorer is fixed once instead of narrated ten times. **If not:** a −10pp page dip can keep being waved through as "the instrument", which is the one thing the hold-or-improve test exists to catch. **Recommendation: make it.**

### Proposal 4 — Budget text agrees with §7, and the tail of a session is used for measurement  (§4)

**Current:**
> **Budget.** The round cap Chris set in the starting message (default: 10 rounds per session) is reached, or the session has run for the time cap he set (default: 6 hours).

**Proposed:**
> **Budget.** The round cap or time cap in the kickoff message is reached (`/loop-start` with no argument = 12 rounds or 10 hours, the §7 default). When the time left is less than the next round needs to ship AND prove (≈ 60–75 minutes for an engine round, more with a full regeneration), do not start it: finish that round's PICK and measurement, record them in `LOOP_STATE.md`, and stop — the sessions 11–12 pattern.

**If made:** the file agrees with itself and with what the loop already does. **If not:** a future reader has two defaults to choose from. **Recommendation: make it** (housekeeping).

### Proposal 5 — "Waiting on Chris" is a stop reason, distinct from Exhaustion  (§4)

**Current (Exhaustion bullet, unchanged) — proposed new bullet after it:**
> **Waiting.** Every remaining class ≥ 20 pages is BLOCKED — needs Chris. This is not exhaustion: report it as "the loop needs N decisions", list each with §5 item 4, and point Chris at `/loop-decisions`. Resume only after `LOOP_STATE.md` carries the answers.

**If made:** the session-8 report would have said "six decisions needed" rather than "the good ending", and Chris would have gone straight to `/loop-decisions`. **If not:** the loop will again call a stall a finish. **Recommendation: make it.**

### Proposal 6 — Refresh the dashboard before a build round is judged  (§4 amendment for widget-BUILD rounds)

**Current:**
> … (a) the plateau rule's "moved" test is the type's *Still a box* count on `COVERAGE_DASHBOARD.md` — a round that converts ≥ 20 sites from hand-off box to built widget has moved; …

**Proposed:**
> … (a) the plateau rule's "moved" test is the type's *Still a box* count on `COVERAGE_DASHBOARD.md`, regenerated with `_coverage_dashboard.py` at the start of every build round and again after its regeneration (a stale dashboard cannot be the test — today's is from 09:26 on 16 Sept, seven rounds old) — a round that converts ≥ 20 sites from hand-off box to built widget has moved; …

**If made:** build rounds are judged on today's corpus. **If not:** the first build round could be judged against a count from before r341–r347 changed 2110 pages. **Recommendation: make it.**

### Proposal 7 — Replace the stale rebuild instruction  (§3 step 5)

**Current:**
> **REBUILD** the affected set + the tag/type family (§0a/§0b), via `_batch_plan.py` and `_regen_safe.sh`, one batch per command. There is no 45-second wall in Claude Code, but keep each command under ~10 minutes and write progress to a file so nothing is lost.

**Proposed:**
> **REBUILD** the affected set + the tag/type family (§0a/§0b), via `_batch_plan.py` and `batch_convert.cjs` run directly with a long timeout — `_regen_safe.sh` hard-codes the old 40-second wall, do not use it. A full regeneration uses the `_fullship_par.sh` pattern (36 batches, 4 workers, ≈ 17–20 min); batches that fail on the oembed-cache write race are re-run singly (rc 0 every time so far — a tooling fix is owed). Keep each command under the 30-minute shell timeout and write progress to a file so nothing is lost.

**If made:** the file describes what the loop does. **If not:** a fresh session that follows the file literally hits a 40-second timeout on its first rebuild. **Recommendation: make it.**

### Proposal 8 — Engine writes are atomic; compactions are logged  (§6)

**Proposed (two new bullets in §6):**
> - Never rewrite an engine or data file in place from a script. Write to a temporary file, check it is non-empty and parses (`node --check` for `.js`, a JSON load for `.json`), then move it over the original. (r347: a writer that opened `DocxExtractor.js` before encoding its content truncated the engine file to 0 bytes; it was rebuilt from the committed blob with `git show`, never a checkout.)
> - Record every automatic compaction as one line in `LOOP_STATE.md` — "compaction at HH:MM during rN, step X" — so the review can count them. Record why a session ended if it was not a §4 stop.

**If made:** one class of near-disaster is closed and the next review can measure what this one could not. **If not:** the same 0-byte accident can recur on any engine file, and compaction frequency stays unknown. **Recommendation: make it.**

### Proposal 9 — The committed mirror includes the baseline, byte-identical  (§3 step 7)

**Current:**
> **FINALISE** (§12): prepend the `BUILD_CHANGELOG.md` entry, bump `Config.js AppVersion`, update `CLAUDE.md` §14 if a baseline or toggle changed, refresh `gate_baseline.json` and the feature index (`build_feature_index.cjs`) after any regeneration, `git add` + `git commit` in `pageforge-site`. …

**Proposed:**
> **FINALISE** (§12): prepend the `BUILD_CHANGELOG.md` entry, bump `Config.js AppVersion`, update `CLAUDE.md` §14 if a baseline or toggle changed, refresh `gate_baseline.json` (every field — `skeleton.pairs` included) and the feature index (`build_feature_index.cjs`) after any regeneration, mirror every changed loop artefact — `gate_baseline.json`, `run_all_gates.sh`, `_corpus.py`, any new verifier, `LOOP_STATE.md`, `KB_AMALGAMATION_STATUS.md` — into `pageforge-site/converter-v2/loop/` and prove the mirror byte-identical (`cmp`), then `git add` + `git commit` in `pageforge-site`. …

Plus the one-off repair this review can do now with your OK: copy the live r347 `gate_baseline.json` into the mirror and correct `skeleton.pairs` 1954 → 1955 in both copies (a record field, not converter data).

**If made:** a crash between sessions loses at most one round of baseline, as §6 promises. **If not:** seven rounds of baseline exist only as changelog prose (today's state). **Recommendation: make it, and do the one-off repair.**

### Proposal 10 — A verifier is green at its recorded baseline  (§3 step 6; a small tooling round, not for this session)

**Proposed (new sentence in §3 step 6):**
> A verifier's RESULT line must read ✓ at its recorded baseline and ✗ only above it (speechBubble defect 4 since r313; math defect 1 since r346 — both carried as "the standing baseline" past a line that says "fix before proceeding"). A round may not ship while any RESULT line is red; the loop is not allowed to learn that red means "as usual".

Implementation is a one-line baseline argument in `_verify_speechbubble.cjs` and `_verify_math.cjs` (or in `run_all_gates.sh`) — a mechanical round for the next `/loop-start`, queued in `LOOP_STATE.md`, not done here.

**If made:** the gate log is readable at a glance and a real new defect cannot hide behind a familiar red. **If not:** the habit hardens. **Recommendation: make the rule now; queue the tooling round.**

### Proposal 11 — §7 names all four project commands  (§7 shortcut paragraph)

**Current:**
> **Shortcut (added 15 Sept 2026):** both messages below are installed as project slash commands in `.claude/skills/loop-start/SKILL.md` and `.claude/skills/loop-stop/SKILL.md`. …

**Proposed (append):**
> Two more project commands exist for sessions that are NOT loop runs and carry no `REGENERATE CORPUS` code: `/loop-decisions` (explain every blocked item to Chris in plain English and record his answers — session 10) and `/loop-review` (the periodic health review of the loop itself, which writes `LOOP_REVIEW__<date>.md`).

**Recommendation: make it** (housekeeping).

### Proposal 12 — KB status housekeeping (not a loop-file change; needs only your OK)

(a) Add the KB HEAD checked (`469f496`, 16 Sept — Assessment Mode; no CL, no `14_` change) to the header of `KB_AMALGAMATION_STATUS.md`, and add "KB HEAD unchanged / changed since the status file" to the §0 health check. (b) Correct §D row 7 to "c47 SHIPPED r344; c95's `FUNdamental:` label-prefix half NOT CAPTURED (12 pages, under the floor)". (c) Either update the six `PageForge status:` lines in the KB's `12G` (one commit in the KB repo) or list them in §E for your next KB session — your call, since the loop's git rule is pageforge-site only.

---

## 5. What this review did not do

No round was started. No converter code, data file, gate tool or module was changed. The KB repo was not touched. Nothing was pushed. The only file this session has written is this report; any edits to `LOOP__Autonomous_Rounds.md`, `KB_AMALGAMATION_STATUS.md`, the baseline mirror or `LOOP_STATE.md` wait for Chris's answer to the proposal list, and will be committed in pageforge-site as "Loop review 2026-09-16".
