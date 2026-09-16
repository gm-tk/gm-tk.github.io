# LOOP_STATE.md — position of the autonomous PageForge loop (LOOP__Autonomous_Rounds.md)

**Session 1 started:** 2026-09-14 (Claude Code on Chris's Windows machine). Budget: 10 rounds or 6 hours.
**Session 2 started:** 2026-09-14 (Claude Code, same machine). Budget: 12 rounds or 10 hours. Resumed Round 1 (engine r314) from session 1's recipe (tree PASS, HEAD 763e036) and shipped it.
**Authority carried by the kickoff message:** `REGENERATE CORPUS` for every round, scoped by CLAUDE.md §0a/§0b.
**Session 3 started:** 2026-09-15 09:41 NZST (Claude Code, same machine; hard stop 19:41). Budget: 12 rounds or 10 hours. Chris's kickoff:
"Continue the PageForge autonomous loop … REGENERATE CORPUS for every round … Budget 12 rounds or 10 hours … commit after every round, never push."
Health check: `verify_after_transfer.sh` PASS, git clean at 1914ab5 (nothing uncommitted — nothing to reconcile), no stale index.lock.
**Round 9 (engine r322) SHIPPED 2026-09-15 ≈11:35 NZST — c65 / CL-0082 (Chris's decision 3); commit 509c216. Round 10 (engine r323) SHIPPED 2026-09-15 ≈12:15 NZST — KB row 55's text defect, the trailing full stop on button labels (212 pages / 82 modules, FULL regeneration); commit (see git log). Round 11 (engine r324) SHIPPED 2026-09-15 ≈12:35 NZST — KB c79's `Lesson N` LABEL titles (79 pages / 24 modules, scoped; commit 1afd467). Round 12 (engine r325) SHIPPED 2026-09-15 ≈13:10 NZST — phase-scoped activity numbering on the Fundamentals pages (17 pages / 17 modules, scoped; commit — see git log).

**Session 4 started:** 2026-09-15 13:27 NZST (Claude Code, same machine; hard stop 23:27). Budget: 12 rounds or 10 hours. Chris's kickoff:
"Continue the PageForge autonomous loop … REGENERATE CORPUS for every round … Budget 12 rounds or 10 hours … Honour every entry under 'Decisions
from Chris' and never re-ask them … commit after every round, never push." Health check: `verify_after_transfer.sh` PASS, git clean at b8bfdf0
(nothing uncommitted — nothing to reconcile), no stale index.lock, KB repo unchanged at ee2853c. **Plateau counter:** the session-3 stop was the
plateau rule's "needs a human decision"; Chris's explicit "continue" IS that decision, so the three-round window restarts at this session's first
shipped round (the same reading session 2 used after the r320 stop). stickyNav stays BLOCKED (no recorded answer — not re-asked); decisions 1 / 4 / 5
stay open (not re-asked); the loop works the derivable queue that needs no decision. **Session 4 result: r326 (button anchor, FULL, +0.057pp) · r327 (ALL-CAPS titles, 0.000) · r328 (c55 labels, 0.000) · r329 (engagement marker, +0.004) — STOPPED on the plateau rule at ≈15:45; commits 955c0c8 · bdb33a1 · 2d478e4 · 6e25190.**

**Session 5 started:** 2026-09-15 16:05 NZST (Claude Code, same machine; hard stop 02:05 NZST 16 Sep). Budget: 12 rounds or 10 hours. Chris's kickoff:
"Continue the PageForge autonomous loop … REGENERATE CORPUS for every round … Budget 12 rounds or 10 hours … Honour every entry under 'Decisions
from Chris' and never re-ask them … commit after every round, never push." Health check: `verify_after_transfer.sh` PASS, git clean at 7b8ffa2
(nothing uncommitted — nothing to reconcile), no stale index.lock. **Plateau counter:** the session-4 stop was the plateau rule's "needs a human
decision"; Chris's explicit "continue" IS that decision (the same reading sessions 2 and 4 used), so the three-round window restarts at this
session's first shipped round. stickyNav stays BLOCKED (no recorded answer — not re-asked); decisions 1 / 4 / 5 stay open (not re-asked); the loop
works the derivable queue that needs no decision. Tools run in WSL (native node EACCES through the symlinks re-confirmed 16:11). **Session 5 so far: r330 (Bilingual section-id numbers, scoped, +0.040pp — the plateau window restarts; commit 0e068c6) · r331 (Bilingual in-box heading level, scoped, +0.022pp; commit 612da6d) · r332 (the empty footers, scoped 130 modules, +0.269pp; commit 8a347d4) · r333 (the right-hand alert side column + the summary token, scoped 53 modules, +0.066pp; commit c6660da) · r334 (the activity title heading h3, scoped 73 modules, +0.167pp; commit b89f20c) · the FULL-SHIP BACKSTOP (IDENTICAL, 19:43) · r335 (the engagement quiz button, BUILT + probe-proven, SHIPPED OFF at Chris's stop ≈20:03). STOPPED ≈20:05 on Chris's instruction.**

**Session 6 started:** 2026-09-15 20:49 NZST (Claude Code, same machine; hard stop 06:49 NZST 16 Sep). Budget: 12 rounds or 10 hours. Chris's kickoff: "Continue the PageForge autonomous loop … REGENERATE CORPUS for every round … Budget 12 rounds or 10 hours … Honour every entry under 'Decisions from Chris' and never re-ask them … commit after every round, never push." Health check: `verify_after_transfer.sh` PASS, git clean at 3de4ca5 (nothing uncommitted — nothing to reconcile), no stale index.lock. **Plateau counter:** the session-5 stop was Chris's instruction, not the plateau rule; the window carries r333 +0.066 · r334 +0.167 (both above 0.02). stickyNav / equations / table form / CED briefs stay BLOCKED (no recorded answer — not re-asked); decisions 1 / 4 / 5 stay open (not re-asked). **Session 6 first step:** finish Round 6 / engine r335 from the state file's recipe (flip `kb_form.enabled` ON, regenerate the 28, gates, finalise, commit — scoped ship #1 since the r334 full backstop). **Session 6 result: r335 (the engagement quiz button, flipped ON + finalised, 28 modules, +0.018pp; commit 0f8317c) · r336 (the Fundamentals overview chip — a registry correction, 31 modules, +0.000pp; commit 2be6466) · r337 (numbered steps → `<ol>`, KB c42, 24 modules, +0.001pp; commit 66c81c5) — STOPPED ≈22:40 on the PLATEAU rule (three consecutive shipped rounds under 0.02pp, no other gate moved). Declined on measurement: the in-box sub-heading level, the outside-box heading ladder, paddingR, p⇐h5, c41's untagged captions. New for Chris: the `alertPadding` activity class. Next PICK candidate: c75's untagged hyperlink buttons (needs the live extractor's link channel).**
**Session 7 started:** 2026-09-15 23:06 NZST (Claude Code, same machine; hard stop 09:06 NZST 16 Sep). Budget: 12 rounds or 10 hours. Chris's kickoff: "Continue the PageForge autonomous loop … REGENERATE CORPUS for every round … Budget 12 rounds or 10 hours … RUN UNINTERRUPTED (§5c) … Honour every entry under 'Decisions from Chris' and never re-ask them … commit after every round, never push." Health check: `verify_after_transfer.sh` PASS, git clean at fce650f (nothing uncommitted — nothing to reconcile), no stale index.lock, KB repo unchanged at ee2853c, WSL toolchain OK (node v22.23.2 / python 3.14.4). **Plateau counter:** the session-6 stop was the plateau rule's "needs a human decision"; Chris's explicit "continue" IS that decision (the same reading sessions 2, 4 and 5 used), so the three-round window restarts at this session's first shipped round. stickyNav / equations / table form / CED briefs / alertPadding stay BLOCKED (no recorded answer — not re-asked); decisions 1 / 4 / 5 stay open (not re-asked); the loop works the derivable queue that needs no decision. **Session 7 first PICK:** c75's untagged standalone hyperlinks (the one measured candidate above the 20-page floor), measured with a LIVE-extractor probe (`DocxExtractor` → `block.links`) before any code. Ship ledger at the start: scoped #3 since the r334 full backstop (5 of headroom).
**Session 8 started:** 2026-09-16 08:03 NZST (Claude Code, same machine; hard stop 18:03 NZST). Budget: 12 rounds or 10 hours. Chris's kickoff: "Continue the PageForge autonomous loop … REGENERATE CORPUS for every round … Budget 12 rounds or 10 hours … RUN UNINTERRUPTED (§5c) … Honour every entry under 'Decisions from Chris' and never re-ask them … commit after every round, never push." Health check: `verify_after_transfer.sh` reported FAIL on 4 engine checksums — EVERY ONE explained by git and none a corruption: `Config.js` = the committed r338/r339 AppVersion bumps (HEAD df9a5f0; the manifest was last refreshed at 22:28 on 15 Sep, before r338), and `ContentConverter.js` / `MediaBuilder.js` / `Emit_Templates.json` = the three UNCOMMITTED files of Session 7 · Round 3 (engine r340), whose PICK is recorded below and whose edits (mtimes 00:50–00:52) match the PICK's two seams + data block exactly (`node --check` OK, duplicate-key JSON load OK). Symlinks 5/5, gate tooling 81/81 byte-identical, corpus census PASS, both git histories intact, no stale index.lock, KB repo unchanged at ee2853c, WSL toolchain OK (node v22.23.2 / python 3.14.4). The same shape as the r316 power-cut restart — the checksum manifest is refreshed at the r340 commit. **Reconciliation:** the three files are NOT reverted; r340 resumes at §3 step 5 (REBUILD — the in-memory OFF/ON probe over all 416 modules first). **Plateau counter:** r338 +0.023 · r339 +0.010 (one under-0.02 round in the window). stickyNav / equations / table form / CED briefs / alertPadding stay BLOCKED (no recorded answer — not re-asked); decisions 1 / 4 / 5 stay open (not re-asked). Ship ledger at the start: scoped #5 since the r334 full backstop (3 of headroom; r340 would be #6).

**Session 9 started:** 2026-09-16 09:21 NZST (Claude Code, same machine; hard stop 19:21 NZST). Budget: 12 rounds or 10 hours. Chris's kickoff: the standing §7 message, unchanged ("Continue the PageForge autonomous loop … REGENERATE CORPUS for every round … Budget 12 rounds or 10 hours … RUN UNINTERRUPTED (§5c) … Honour every entry under 'Decisions from Chris' and never re-ask them … commit after every round, never push"). Health check: `verify_after_transfer.sh` PASS (symlinks 5/5, engine 62/62 and gate tooling 81/81 byte-identical, census PASS, both git histories intact), git clean at e9e2826 (nothing uncommitted — nothing to reconcile), no stale index.lock, WSL toolchain OK (node v22.23.2 / python 3.14.4). **State inherited:** the loop stopped on §4 EXHAUSTION in session 8 and the message carries NO answer to any recorded decision — so no blocked class is unblocked. **Session 9 first step:** a fresh §3 PICK pass (the dashboard queue + KB §D + the substitution instrument re-run) to confirm exhaustion on today's corpus rather than inherit it; a round only if a derivable class ≥ 20 pages surfaces; otherwise the §4 EXHAUSTION stop again with the §5 report. stickyNav / equations / c23 / alertPadding / table form / CED briefs / decisions 1 / 4 / 5 stay BLOCKED (no recorded answer — not re-asked). Ship ledger at the start: scoped #6 since the r334 full backstop (2 of headroom). **Session 9 result: r341 (near-red tag runs, FULL regeneration, +0.021pp; commit bb56efc) · r342 (hyperlinked media tags) built + part-proven, STOPPED by Chris at ≈11:05 NZST with both flags OFF, uncommitted-but-described.**

**Session 10 (2026-09-16 ≈14:00–15:30 NZST, `/loop-decisions` — NOT a loop run):** the nine pending decisions explained in plain English (`DECISIONS__Pending_2026-09-16.md`, folder root) and ALL NINE answered by Chris in one message → recorded as **D10-1 … D10-9** under "Decisions from Chris (session 10)"; no round, no regeneration, no engine / data / KB file touched; LOOP_STATE + KB status committed ("Decisions from Chris 2026-09-16"), not pushed.
**Session 11 started:** 2026-09-16 15:27 NZST (Claude Code, same machine; hard stop 18:27 NZST). Budget: **10 rounds or 3 hours**. Chris's kickoff: the standing §7 message via `/loop-start [10 rounds or 3 hours]` (it carries `REGENERATE CORPUS`). Health check: `verify_after_transfer.sh` PASS (symlinks 5/5, engine 62/62 and gate tooling 81/81 byte-identical, census PASS, both git histories intact), no stale index.lock, git = 9e8a479 + EXACTLY the four r342 files described by session 9 (reconciled against the r342 PICK — never checked out), WSL toolchain OK (node v22.23.2 / python 3.14.4). **State inherited:** the session-10 queue in the top banner (D10-1 … D10-9 decided). **Session 11 first step:** item 0 — finish r342 (flip both flags ON, settle gap 2 by measurement, prove, ship). **Session 11 result so far: r342 SHIPPED ≈16:50 (see the round log).**


## >>> DECISIONS RECORDED 2026-09-16 ≈15:20 NZST (session 10 — `/loop-decisions`, NOT a loop run): Chris answered ALL NINE pending decisions — every Blocked class is now DECIDED; the loop is UNBLOCKED with a nine-item authorised queue; nothing regenerated, no engine/data file touched; r342 stays as session 9 left it (four files uncommitted, both flags OFF) <<<
- The nine answers are recorded verbatim under "Decisions from Chris (session 10 …)" below as **D10-1 … D10-9**; the Blocked / Declined entries they
  settle point at them; `KB_AMALGAMATION_STATUS.md` rows updated; the report he answered is `DECISIONS__Pending_2026-09-16.md` (folder root).
  Two are CLOSED with no round (D10-4 stickyNav — keep the ban; D10-8 alertPadding — leave plain); seven authorise rounds.
- **KB edits authorised but NOT made here** (an Admin-Mode KB round in `00-Other-TK-Resources/htmlconvertor-kb`, one CL row each, `check_kb.py`,
  timestamps — the KB repo is untouched at ee2853c): 14A/14B/14D stickyNav → "never emitted" (D10-4); 05A equations → MathML (D10-7); 06 §6 tables →
  reconciled to 05D (D10-5); 00G c79 / 01A → "Standard: English first; MTK: Māori first" (D10-2); 01F line 27 / 05B `alertPadding` = example, not
  default (D10-8, a note). The loop does NOT wait for these — §5b: a recorded decision outranks the KB's stale wording.

**Next session starts with:** the standing §7 kickoff (it carries `REGENERATE CORPUS`); health check; reconcile git — the four r342 files are the round
in progress (never checkout / restore); then this ORDER (each item one §3 round unless stated; §4 stop rules apply; the plateau window restarts at the
first shipped round because these are Chris's explicit decisions):
  0. **r342 (the hyperlinked media tag)** — flip both flags ON, settle gap 2 by measurement per its own note, prove, ship — OR, if it fails the §3
     three-repair limit, toggle OFF, prove identity, record BLOCKED and move on. One round, no more.
  1. **D10-6 — exclude the 8 CED revision-brief modules from the comparison set** (an exclusion list in `_corpus.py` `mods()` read from
     `reference/tests/compare_exclusions.txt`; no regeneration) and RE-BASELINE every gate on the new population (`gate_baseline.json`, CLAUDE.md §14,
     fast-loop baseline, ceiling, `CORPUS_CENSUS.txt`) — the ≈ +0.3pp is a population change, named as such, never claimed. FIRST, so nothing later is polluted.
  2. **D10-1 — c47 in full** (drop the opening duplicate body heading; activity-box titles kept; + the title's stray `*` / `**` markers as a measured
     sibling). Scoped regeneration, named override on the ≈ 6 gold-kept pages.
  3. **D10-2 — English-first lesson-title pairs in Standard modules** (the r316 mechanism, `reo_detect "macron"`). 4 pages; scoped.
  4. **D10-7 — Word equations → MathML** (OMML extraction + `omml-to-mathml` port + `mathJax` body class; an equation-count verifier). 12 modules, scoped.
  5. **D10-5 — 05D tables: `table table-bordered` default, `table tableFixed` for two-column comparison tables** (contrast-lexicon test, measured first).
     FULL regeneration — may be shared with 6 if each is A/B-proven OFF/ON on a sample first (the r334 backstop precedent).
  6. **D10-9 — c23 lesson-menu labels everywhere** (`<h5>`, normalised wording by year level, no section title above, overview tab too; the c70 OSSC
     lead-in `<p>` stays; a `_verify_menulabels` gate). FULL regeneration, named override ≈ −0.1pp.
  7. **D10-3 — widget-build kickoffs, one type at a time, largest first:** dragAndDrop → clickDrop → accordion → carousel → flipCard → selfCheck → modal →
     tabs → slider → infoTrigger → shapeHover → hint → hintSlider. Each round = the type's largest un-built shape family ≥ 20 sites (the r286 decline
     instrument), judged on the widget's own verifier (A1), never half-built, family regeneration per type; the plateau "moved" test for a build round is
     the dashboard's *Still a box* count (recorded in D10-3 — Chris may veto).
  Then the ordinary §3 PICK over whatever remains. Expect ≈ 3 full regenerations across items 5–7; budget accordingly (12 rounds / 10 hours per session).

## >>> STOPPED 2026-09-16 ≈11:10 NZST (session 9) on CHRIS'S INSTRUCTION — "stop the loop at the next logical point" — after ONE shipped round (r341, the near-red tag rule, the FULL-regeneration backstop, commit bb56efc); Round 2 (engine r342 — the HYPERLINKED media tag) is built and part-proven, could NOT be finished and proven inside 10 minutes, so BOTH of its data flags are switched OFF (the engine reproduces the disk corpus byte-for-byte, 89/89 pages on 12 modules), its four files stay UNCOMMITTED-but-described below <<<
- Session 9 shipped r341 (76 pages / 10 added / 2 removed across 23 modules; skeleton +0.021pp, ≥50 +7, cs exact +103, clean 97.81 → 98.91%, leak
  288/46 → 26/23; corpus now 2110 pages). Round 2 (r342) reached PROVE: the OFF leg = disk 2110/2110; the ON leg changed 76 pages / 52 modules and
  surfaced TWO pre-existing gaps in the hand-off box (one fixed in the same working tree, one measured and left for the next session — see
  "Session 9 · Round 2 (engine r342) — IN PROGRESS at the stop"). Tree: verify PASS (its page-count expectation corrected 2102 → 2110 for the r341
  corpus; the engine checksum manifest refreshed to the working tree, backup `CHECKSUMS__engine.pre-r342stop.bak`), git = bb56efc + 4 modified files.

## >>> STOPPED 2026-09-16 ≈10:10 NZST (session 8) on the EXHAUSTION rule (§4 — the GOOD ending): after r340 shipped, no class with a derivable population ≥ 20 pages remains and every KB row ≥ 20 pages left is BLOCKED on a decision from Chris (stickyNav, equations, c23 label form, alertPadding, table form, CED briefs, decision 5 interactives) or DECLINED on measurement <<<
- Session 8 shipped ONE round: r340 (finished from session 7's PICK + code) — 19 pages / 9 modules, skeleton −0.000pp at 3 dp (three dips
  NAMED, +0.0006 net of the two A1 pages), cs exact +1, every other gate EXACT; commit 56bb70c. Then the Round 2 PICK measured five candidates
  (below) and none reached the floor. Tree: verify PASS, git clean after the stop commit, manifests refreshed.

## >>> STOPPED 2026-09-15 ≈22:40 NZST (session 6) on the PLATEAU rule (§4) — three consecutive shipped rounds under 0.02pp with no other protected gate moved: r335 +0.018pp, r336 +0.000pp, r337 +0.001pp <<<

**Session 6 shipped three rounds (r335 → r337; commits 0f8317c · 2be6466 · 66c81c5) in ≈1h50m of the 10-hour budget (20:49 → 22:40).** Everything is
committed; nothing is uncommitted; nothing was pushed. The ship ledger stands at scoped #3 since the r334 full-ship backstop (5 of headroom).
- **r335** finished session 5's Round 6: the `[Engagement quiz button]` KB form flipped ON, 28 modules regenerated, skeleton +0.018pp (19 up / 9 down,
  dips ≤ 0.33pp named), every other gate line-for-line EXACT. Gotcha fixed: the session-5 affected list was CRLF and defeated `_fastloop_diff.py`.
- **r336** corrected the Style-Anchor registry for five Fundamentals families (ARFUN / ENFUN / TEFUN / MXFUN0 drop the `#module-code` chip their golds
  never ship; SSFUN gains the chip its golds ship 5/6) — 31 overview pages, +0.000pp (the removed phantom chip's `h1` had been coincidentally matching
  the gold's unshipped Te Reo `h1`), every other gate EXACT. The affected set came from resolving all 416 modules before and after the edit.
- **r337** shipped KB constraint 42 small (24 pages, under the 20-page floor on the r320 precedent): numbered steps as a semantic `<ol>` — the
  writer's typed `1. 2. 3.` runs AND the extractor's Word-numbered-list marker (`1.` on every item, so a Word list inside a built accordion panel
  shipped every question numbered 1). +0.001pp; every other gate EXACT; the accordion verifier over the 24 clean.
- **Scorecard 20:49 → 22:40:** SCAFFOLD 51.060% → **51.079%** (+0.019pp; 55.7% → 55.8% of achievable, ceiling 91.6%); ≥50 1066; ≥75 200; ≥90 15;
  cs exact 11375 / EXTRA 171 / missing 593; body 191; clean 2056/2102; leak 288/46; tags 9557/9557; flipCard TOTAL 61 divergence 0; 13 selftests
  GREEN at every round. RAW 35.243% → 35.263%.
- **Declined this session (measured):** the activity box's SUB-heading level (text-paired agreement already 0.957 — the r334 note's 655-vs-657 was a
  position artefact); the outside-box heading LADDER (per-module: HIS/PES split 0/−1/−2 by module; only TEDC 0.72 / XTAS 0.69 / TWHA 0.91 solidify,
  all < 20 pages); `paddingR` (0.22 even in paired rows); `p ⇐ h5` (25 cases / 17 pages); c41's untagged captions (the line after an image is a
  caption in the gold at ~0.00 — 308 of the 512 gold captions are editorial, the 50 tagged ones all ship). **Blocked (need Chris), new:** the
  `alertPadding` activity class (KB 01F's table vs the gold's 0.81 plain majority + 05B's "follow the activity's own class set").
- **The queue after r337:** the post-r335 substitution ranking has no derivable structural class ≥ 20 pages left; the KB rows still carrying a gap are
  c75 (external-link buttons — 15 tagged-and-missing on 13 pages, under the floor; **452 UNTAGGED hyperlink phrases the human buttoned, 255 pages —
  the standalone-hyperlink discriminator cannot be read from the parsed-text dumps and needs the live extractor's `block.links` channel**), the
  blocked decisions, and the crumb-less Inquiry dialects (each a PanelsBuilder round of 1–14 pages).

## >>> STOPPED 2026-09-15 ≈20:05 NZST (session 5) on CHRIS'S INSTRUCTION — "stop the loop at the next safe point" — after 5 shipped rounds + the full-ship backstop; Round 6 (engine r335) built and probe-proven, SHIPPED OFF <<<

**Where the loop is:** Session 5 · Round 6 (engine r335, the `[Engagement quiz button]` KB form). Its step when Chris stopped it: PROVE — the
28-module scoped regeneration was done (0 truly stale, manifest diff = exactly the 28), `_fastloop_diff.py` had PASSED on the 28 (skeleton
+0.02pp, every other gate HELD), and the full gate suite was mid-run (~12 min from done — over Chris's 5-minute rule), so per the instruction
the round's data flag was switched OFF (`buttons["engagement quiz button"].kb_form.enabled: false`, `_status` note in the data) and the 28
modules were regenerated OFF: **`_content_manifest.py diff` = IDENTICAL, 0 pages differ — the corpus is byte-for-byte the full-ship state**
(the mtime-only `_stalecheck.sh` warning after that edit is the documented r148/r175 false alarm; content-hash proven). The engine branch +
data block are COMMITTED, OFF; no finalise was written for r335 (no changelog round entry, no AppVersion bump, no §9/§11/§14 baseline
change, no KB D-row, no ship-ledger record) — those are the next session's first steps once the flag is flipped ON.
**Shipped this session:** r330 (0e068c6) · r331 (612da6d) · r332 (8a347d4) · r333 (c6660da) · r334 (b89f20c) · the FULL-SHIP BACKSTOP after
r334 (all 416 dirs regenerated, 0 stale, manifest IDENTICAL — eight scoped ships proven complete; ledger record-full, counter 0; fast-loop
baseline re-snapshotted from the fresh corpus). **Declined this session:** the widened activity wrapper (KB c17/c56), `iframe.embed-responsive-item`,
`body.mathJax` as a class (not derivable per module), the whole-bold short paragraph → h5, the in-box sub-heading level, the `alertImage` sidebar
(r331), the KB `table-bordered` (conflict → Chris). **Blocked (need Chris):** stickyNav (unchanged), the KB table form 05D vs 06 §6, the CED
revision-brief modules (content-start), **Word equations dropped — MathML (gold, V1.5 finding) vs LaTeX (KB 05A)**; decisions 1 / 4 / 5 open.
**Uncommitted at the stop:** nothing (see the final commit). Scorecard: skeleton 50.496 → **51.060** (+0.564pp this session; 55.1% → 55.7% of
achievable, ceiling 91.6%); ≥50 1030 → 1066; ≥75 196 → 200; ≥90 15; cs exact 11360 → 11375 / EXTRA 186 → 171 / missing 591 → 593 (named); body
191; clean 2056/2102; leak 288/46; tags 9557/9557; 13 selftests GREEN.

## >>> STOPPED 2026-09-15 ≈15:45 NZST (session 4) on the PLATEAU rule (§4) — three consecutive shipped rounds under 0.02pp with no other protected gate moved: r327 0.000pp, r328 0.000pp, r329 +0.004pp <<<
**Session 4 shipped four rounds (r326 → r329; commits 955c0c8 · bdb33a1 · 2d478e4 · 6e25190) in ≈2h15m of the 10-hour budget (13:27 → 15:42).** Everything is committed; nothing is uncommitted; nothing was pushed.
- r326 (FULL regeneration) moved the skeleton +0.057pp (the KB's universal button anchor; 285 lost hyperlinks recovered) and restarted the plateau window; r327 (ALL-CAPS titles → sentence case), r328 (constraint 55's label half) and r329 (the `[trigger engagement]` marker) were KB-backed rounds that could not move the gate by 0.02pp — the derivable, KB-backed queue above the 20-page floor is now spent.
- **Scorecard 13:27 → 15:45:** SCAFFOLD 50.435% → **50.496%** (55.1% of achievable, ceiling 91.6%); ≥50 1031 → 1030 (a NAMED scorer-alignment dip on r326, identical net of the changed pages); ≥75 193 → **196**; ≥90 15; body 192 → **191**; every other gate EXACT; 13 selftests GREEN at every round.
**Next session starts with:** Chris's decisions — unchanged from session 3 and NOT re-asked: (a) stickyNav (BLOCKED: the KB 14 families say ADD the `<head>` include, the project instruction says NEVER; recommendation = KB families only), (b) decision 5 — the interactive builds (the corpus's largest class by far: 824 un-built drag-and-drops, 237 widgets with no builder; the writer's `[button] Check answers` / `Reset` controls (219 buttons / 38 modules) belong to this class), (c) decision 4 — the Standard-template title-pair order, (d) decision 1 — c47. With none of those, the remaining measured candidates are all under the plateau threshold: the Bilingual `number="N.M"` section-id boxes (KB 07B; 72 boxes / 25 pages, est. +0.01pp — the one still-unshipped KB row ≥ 20 pages), the 28 residual compound engagement brackets, the `[engagement quiz button]`'s own form (23 modules), the 44 c79 module-title fallbacks (~24 derivable across four source tags, none ≥ 20 alone), the box-less `[MTKquiz]` shells (~17 pages). If Chris wants the loop to run without a decision, start with the Bilingual section-id boxes (a KB row) and expect the plateau rule to stop it again after it.

## >>> STOPPED 2026-09-15 ≈13:10 NZST on the PLATEAU rule (§4) — three consecutive shipped rounds under 0.02pp with no other protected gate moved: r323 0.000pp, r324 +0.005pp, r325 +0.019pp <<<
**Session 3 shipped four rounds (r322 → r325; 4 commits) in ≈3h30m of the 10-hour budget.** Everything is committed; nothing is uncommitted; nothing was pushed.
**Next session starts with:** Chris's decisions — (a) stickyNav (BLOCKED: the KB 14 families say ADD the `<head>` include, the project instruction says NEVER; recommendation = KB families only), (b) decision 5 — the interactive builds (the corpus's largest class: 824 un-built drag-and-drops, 237 widgets with no builder, invisible to the gates by design), (c) decision 4 — the Standard-template title-pair order, (d) decision 1 — c47. With none of those, the derivable ≥ 20-page queue is exhausted for gate-moving work; the remaining measured candidates are the box-less `[MTKquiz]` shells (now numberable — 32 shells, ~17 pages), the Bilingual `number="N.M"` section-id boxes (KB 07B; 72 boxes / 25 pages, est. +0.01pp), the c79 trailing-punctuation titles (8), and the 172 empty hand-off boxes (15 shapes, none ≥ 20). stickyNav (KB queue rank 10) is BLOCKED — needs Chris (see Blocked classes). Plateau guard: r322 moved +0.043pp.**

## >>> STOPPED 2026-09-15 ≈08:15 NZST on the BUDGET rule (§4) — the 10-hour session cap (hard stop 09:21) after 8 shipped rounds <<<
- **Why:** Chris answered the plateau report ("Yes to 2 and 3 — start with the TRR title source") at ≈07:48 NZST; Round 8 (decision 2, the MTK
  title source) shipped at 08:06 with ≈75 min of the 10-hour budget left — not enough to design, measure, prove and regenerate decision 3
  (c65 / CL-0082) to the loop's standard, so it is recorded below as the AUTHORISED NEXT KICKOFF rather than left half-built at the hard stop.
- **Everything is committed** (pageforge-site, 10 commits this session: 314–321 + the two loop-state records); nothing pushed. `git status` clean;
  `verify_after_transfer.sh` PASS; corpus 0-stale, manifest / fast-loop baseline / feature index / gate_baseline.json refreshed at r321.
- **NEXT KICKOFF (authorised by Chris — decision 3): c65 / CL-0082, the `[MTKquiz]` shell without the quiz content.** Measured 2026-09-15
  (`outputs/_r322_mtkquiz_shells.json`): 68 activity shells holding a "Go to quiz" button on 30 pages / 24 modules; **39 carry list/table
  markup** (the questions/options/answers the KB says to omit SILENTLY — no Red Flag, no comment), 11 of them with answer/correct wording; 29 are
  already the four-child shape. The KB form (constraint 65): a numbered `activity` box holding ONLY (1) `<h3>` = the writer's quiz title or
  `Quiz`, (2) the writer's student instructions (omitted where none), (3) the `Designer/Developer To Do:` note (create in MTK DEV, orgunit link),
  (4) `<a href="#" target="_blank"><div class="button">Go to quiz</div></a>` — in that order. Design sketch: reverse round 232's "marker is a
  non-capturing ELEMENT" retag for the MTKquiz family so the marker opens a capturing bundle again; classify members — title (the first heading /
  a `[H3]`/`[H4]` before the marker), instructions (prose before the first question), quiz content (numbered/lettered items, `[answer]`/`[correct]`
  marks, option tables, answer keys — the r287/r305 mcq token stream already recognises these) — and emit the four children in the KB order,
  dropping the quiz-content members without a note; a `_verify_mtkquiz.cjs` selftest (LIVENESS + DETECTION: a doctored shell that leaks an
  `<ol>` must raise). Gate-visible as a NAMED override (the gold keeps the content on 157 of 199 shells — pre-rule); judge net of the named
  pages like round 317. Family regen: every module carrying an MTKquiz marker (24 + the r232 detector's 21). Budget: one full round.
- **Decisions still open for Chris:** 1 (c47 exact-duplicate heading drop — now unblocked on the TRR side: the `Finished!` titles are gone),
  4 (the Standard-template lesson-pair order), 5 (interactive-build kickoffs per widget type).

## Session 2 — (started 2026-09-14 23:21 NZST; stopped 03:43 after 7 rounds; the power cut during Round 3 cost ~15 min)
- **Round 1 (engine r314) SHIPPED** (commit f1f4de2) — KB c43, the trailing upload box inside its activity.
- **Round 2 (engine r315) SHIPPED** (commit 3528986) — KB c28, the XHTML shell, FULL regeneration + the `anchor_compare` pairing-parser repair.
- **Round 3 (engine r316) SHIPPED 2026-09-15** — KB c79, the lesson's own bilingual title pair (two h1 spans, code stripped, Te Reo first in
  reoTranslate modules); scoped regeneration of 179. **A power cut interrupted this round** after the engine edits and before the rebuild; on
  restart the tree was verified (git fsck, every JSON, corpus == r315 manifest), the one casualty — `reference/tests/batch_results.json`, a 48-byte
  NUL run — was repaired with the corrupt copy kept, and the migration checksum manifests (`_MIGRATION/CHECKSUMS__*.txt`, a r313 snapshot) are now
  refreshed at each commit (old copies `*.pre-r316.bak`). Commit: see the round log.
- **Round 3 (engine r316) SHIPPED** (commit 414ef28).
- **Round 4 (engine r317) SHIPPED 2026-09-15** — KB c45 + c90, the acks block's template form (`acks acksTemplate`, no typed statements); FULL
  regeneration, a NAMED KB-over-gold override (skeleton −0.024pp on exactly the 387 named pages, identical net of them). Commit: see the round log.
- **Round 4 (engine r317) SHIPPED** (commit 81dfb05).
- **Round 5 (engine r318) SHIPPED 2026-09-15** — KB c83, no `loading="lazy"` inside moving interactives (2424 images / 228 pages / 146 modules);
  FULL regeneration, gate-neutral (skeleton page-for-page identical). Commit: see the round log.
- **Round 5 (engine r318) SHIPPED** (commit bd2ca1b).
- **Round 6 (engine r319) SHIPPED 2026-09-15** — KB c89, `learningSupport` on every X-prefixed module's `<html>` (228 pages / 35 modules); scoped
  regeneration, gate-neutral. Commit: see the round log.
- **Round 6 (engine r319) SHIPPED** (commit 0827965).
- **Round 7 (engine r320) SHIPPED 2026-09-15** — the upload box keeps the writer's order around its button (6 pages / 4 modules, a small ship
  under the floor; the round's first candidate c47/c95 DECLINED on measurement). Commit: see the round log.
- **Corpus / engine state:** the r320 scoped dropDown-family regeneration on top of r319 (6 pages changed, 0 stale); content manifest, fast-loop
  baseline, feature index, ledger (scoped #2 since the r318 full), gate_baseline.json refreshed; skeleton state `outputs/_r320_sk_final.json`
  FRESH. Build 260618.91.
- **MEASUREMENT RULE FROM ROUND 2 ON:** `reference/tests/anchor_compare.py` is void-aware now. Any comparison across round 315 must use the
  repaired tool on both sides; the r313/r314 skeleton state files were scored with the void-blind pairing (1939 pairs) and are NOT comparable
  page-for-page to `_r315_sk_final.json` (1954 pairs) — compare against r315 from here on.
- **RESUMED 2026-09-15 07:48 NZST on Chris's instruction: "Yes to 2 and 3 — start with the TRR title source."** Round 8 = decision 2 SHIPPED
  (engine r321, commit 968bf14). Decision 3 (c65 / CL-0082, engine r322) = the next kickoff (above). Decisions 1, 4, 5 stay open.

## Decisions from Chris (session 10 — 2026-09-16 ≈15:20 NZST; the `/loop-decisions` session — NOT a loop run; ALL NINE pending decisions answered in one message, recorded verbatim; the report he answered is `DECISIONS__Pending_2026-09-16.md` at the folder root)

**His standing instruction with the answers (verbatim):** "Here are my answers to act on (dedicate this session to actioning these and then perform any
necessary actions in order for a standard development loop to occur in a new Claude Code session after these 9 pending items have all been rectified)".
Applied in this session: the nine answers are recorded below; every Blocked / Declined entry they settle now points at its decision; "Next session starts
with:" (the banner at the top) is the ordered queue the next `/loop-start` works; `KB_AMALGAMATION_STATUS.md` rows updated; both files mirrored into
`converter-v2/loop/` and committed in pageforge-site ("Decisions from Chris 2026-09-16"), never pushed. **No converter code, data or corpus changed** — this
session carried no `REGENERATE CORPUS` code; the rounds themselves run in the next loop session under the standing §7 kickoff. The r342 working tree (four
uncommitted files, both flags OFF) is untouched. **Still open for Chris: NOTHING** — every recorded Blocked class now has a decision.

- **D10-1 — 2026-09-16 — the duplicate opening body heading (KB constraint 47; the plateau report's decision 1).** Question: apply c47 in full (A), only
  the `Lesson N:` form (B), or leave the title printed twice (C)? Answer (verbatim): "The human is correct, for instance: [the SSOG101 lesson-3 example —
  gold `<h1><span> Police Officers</span></h1>` then `<div id="body"> … <p>The police are like community helpers …` with no heading in the body; PageForge
  `<h1><span>* Police Officers</span></h1>` … `<h3>Lesson 3: Police Officers</h3>`] In the human-built version, the lesson number is isolated to the
  top-right corner and the lesson title is kept as the h1. This is correct and should be adhered to." = **Option A.** Authorises: ONE round — on every
  lesson page of every template, DROP the opening body heading whose text equals the header title once case, punctuation and a `Lesson N` prefix
  (`Lesson 3:`, `Lesson #3`, `Lesson One`, `Lesson 5 continued`) are ignored (the c47 test); the lesson NUMBER stays in the `#module-code` `<h1>`
  (the top-right corner) and the lesson's OWN title stays the `<h1><span>` (c79 — never emptied, never the module title); a heading INSIDE an activity
  box (ENGI101 "Being Frank" = the activity's own title) or one that introduces a different sub-topic is KEPT; on the overview page strip-only (the r320
  note). Scope: the `_r320_dupheading.json` population re-measured on today's corpus (77 pages / 54 modules at r320; the 41 TRR false matches are gone
  since r321). Target form: the gold's SSOG101_3.0 / MXFU302_1.0 shape. Authority: KB level 1 (c47, Universal) over the gold's 57% on the exact form —
  a NAMED override on the ≈ 6 pages where the human kept the repeat (ENGJ101_1, ENGR201_1, MXDB302_6, MXEO202_3, MXFU201_2, OSGM201_1 …); the 12
  `Lesson N` pages are under the 20-page floor and ship on this authorisation. **Sibling to measure in the same round:** the header title's stray
  markdown markers (`<h1><span>* Police Officers</span></h1>`, `<h1><span>**Statistics and Sports**</span></h1>` — the writer's italic / bold asterisks
  leaking into the title; c79 hygiene, the r327 title-casing seam) — ship if derivable, else record. Scoped regeneration (the heading family).
- **D10-2 — 2026-09-16 — the bilingual lesson-title pair ORDER in Standard-template modules (the plateau report's decision 4).** Question: keep the
  writer's order (A), English first (B), Māori first everywhere (C)? Answer (verbatim): "Go with option B — English first in Standard modules."
  Authorises: ONE small round — in a Standard-template module, a LESSON title that is a `|`-separated bilingual pair ships the ENGLISH half first and the
  Te Reo half second (the r316 `header.lesson_bilingual_pair` mechanism: `reo_detect "macron"` decides which half is Te Reo; where neither half carries a
  macron the writer's order stands and the page is recorded); the MTK rule (`reo_first_when_body_class "reoTranslate"`, 07D rule 7 — Māori first) is
  UNTOUCHED for Bilingual modules. Scope: the r316 pipe-title set in Standard (13 pages, 8 modules): ANZH101_2_0 and MXDB202_3_0 gain the gold's order;
  ANZH105_1_0 and HIS1006_10_0 become NAMED overrides (the human kept the writer's Te-Reo-first order there); the MXFL101 / TEDC402 / XGF9002 pages
  where the gold carries a different pair altogether are unaffected in pairing terms. NOT in this decision: the overview page's `[TITLE BAR]` module-title
  pair (measure separately if its order ever differs) and Languages three-part titles (c85 — writer's order). Authority: Chris's house rule (the KB is
  silent for Standard) — a KB delta: 00G c79 / 01A to gain the sentence "a bilingual lesson-title pair is English first in Standard modules, Māori first
  in MTK (07D rule 7)" (a KB session, own CL row). Data flag + env toggle; scoped regeneration of the pipe-title family.
- **D10-3 — 2026-09-16 — building the un-built interactives (the plateau report's decision 5).** Question: widget-build rounds inside the loop (A),
  leave builds to the Interactives Build Mode / developer path (B), only the three builder-less types (C)? Answer (verbatim): "Option A — authorise
  widget-build rounds inside the loop, one type per kickoff,". Authorises: widget-BUILD rounds in this loop, ONE widget type per kickoff, largest un-built
  population first — **dragAndDrop** (822 un-built / 291 modules / 682 shapes) → **clickDrop** (324 / 108) → **accordion** (255 / 112) → **carousel**
  (239 / 140) → **flipCard** (215 / 121) → **selfCheck** (153 / 65 — NO builder today) → **modal** (153 / 59) → **tabs** (75 / 45) → **slider** (47 / 30 —
  NO builder) → **infoTrigger** (37 / 22 — NO builder) → **shapeHover** (27) → **hint** (17) → **hintSlider** (12) → glossary (1) (the
  `COVERAGE_DASHBOARD.md` census, refreshed 2026-09-16 — re-run it at each kickoff). A kickoff is a SEQUENCE of rounds on one type: each round takes the
  type's largest un-built authoring SHAPE family ≥ 20 sites (measured with the r286 decline instrument — `_measure_r286_declines.cjs` — the builder's
  own give-up reason names the shape), extends the type's builder to it behind a data flag + env toggle (the r246 / r276–r289 interactive-coverage chain
  pattern: build the WRITER's tag; A1 — judged on the widget's own verifier at divergence / defect 0, never on the human's substitution; **never
  half-build** — a shape that cannot be built to the KB's 03B–03F form stays the hand-off box with its worklist entry), family regeneration of the type
  (§0b — the whole tag family, working half included; dragAndDrop ≈ 291 modules ≈ near-full), gates hold; the kickoff ends when no shape family ≥ 20
  sites remains, then the next type. **§4 reading for build rounds (recorded here, Chris to veto if wrong):** a build is invisible to the skeleton score
  by design, so the plateau rule's "moved" test for a build round is the type's *Still a box* count on the dashboard (a round that converts ≥ 20 sites
  from box to built is progress); the budget / exhaustion rules apply unchanged. Authority: Chris (this decision + the A1 standing ruling "the writer's
  tag is the target"); overrides nothing in the KB (03B–03F + 15 describe the forms). Consequences: the activity `interactive` modifier (r339 Declined)
  and the widened wrapper (c17/c56, r334 Declined) follow each BUILD (the token follows the widget — still never inferred from the box side); the
  gold's own widget substitutions around a built element (r339 / r340 A1 pages) stay A1. Sequence: AFTER the structure rounds D10-6 → D10-1 → D10-2 →
  D10-7 → D10-5 → D10-9 (they change the pages the builds land on and D10-5 / D10-9 need the full regeneration anyway).
- **D10-4 — 2026-09-16 — the `stickyNav` `<head>` include (KB queue rank 10; 14A / 14B / 14D vs the project instruction).** Question: KB families only
  (A), every ≥ 60% series (B), keep the ban (C)? Answer (verbatim): "Option C — keep the ban everywhere. No change; the KB's three family rules stay
  un-honoured and the KB should then be edited to say so." Authorises: NO round — the class is **CLOSED** (decided, not blocked, not declined).
  `Emit_Templates.skeleton.never_emit` (`stickyNav.js`) stays; `00_PROJECT_CONTEXT_AND_PHILOSOPHY.md` line 85 ("a templating error that was copied
  across modules; never emit it") is the governing rule for every series including CED Phase 5 / HES / PHE / HPFUN. **KB edits authorised** (an
  Admin-Mode KB round in the KB repo — its own CL row, `check_kb.py`, timestamps — NOT done in this session, which touches no KB file):
  `14A_SGP_PURPOSE_FAMILIES_1_5.md` line 54 (Languages "Sticky nav on every page"), line ~121 (CED Phase 5 "Sticky-nav dictionary links"),
  `14B_SGP_FAMILIES_6_11.md` line 93 (HPE "Sticky / floating nav"), `14D_SGP_CROSSCUTTING_AND_TECHNOLOGY.md` line 11 (the cross-cutting summary) →
  each to state that the `stickyNav.js` include is NEVER emitted by the Convertor or by PageForge (a templating error; where a family needs a floating
  nav it is the developer's post-build set-up) and the "set up the `stickyNav.js` file" To Do note is withdrawn. KB status queue row 10 → CLOSED.
- **D10-5 — 2026-09-16 — the table form (KB 05D vs 06 §6, a KB-internal conflict).** Question: bordered everywhere per 05D (A), bordered only where
  the family agrees (B), leave plain (C); which KB page is right? Answer (verbatim): "Option A — 05D's table table-bordered everywhere (plus tableFixed
  for true two-column comparison tables). Every table gets cell borders. A named override in Standard (the tie), a gain in the other three templates.
  Gate-moving (tiny net), full regeneration in practice (tables are everywhere)." = **05D is the rule; 06 §6 is superseded.** Authorises: ONE round,
  FULL regeneration — every writer table ships `<div class="table-responsive"><table class="table table-bordered">` (05D's default) EXCEPT a two-column
  COMPARISON table, which ships `<table class="table tableFixed">` (no `table-bordered`, 05D lines 239–246); the comparison test is DATA-DRIVEN and
  measured before coding — exactly two columns AND a header pair from a contrast lexicon (can / cannot, pros / cons, advantages / disadvantages, before /
  after, do / don't, true / false, similarities / differences, fact / opinion, …; a two-column table whose headers are not a contrast pair stays
  bordered); the existing `th` header rule and the `table-responsive` wrapper are unchanged; 05D's optional `noHover` / `center-text` are NOT emitted (no
  writer signal; gold 0.09). Scope: 1,063 tables / 518 pages at r331 — re-measure. Authority: KB 05D level 1 over the gold's Standard tie (0.51) — a
  NAMED override on every Standard page whose gold table is plain (≈ 133 matched lines lost), gains in Inquiry 0.72 / Fundamentals 0.69 / Bilingual 0.86
  (+74); net ≈ −0.01pp, named. **KB delta:** `06_TEMPLATE_RECOGNITION.md` lines 405–411 (`table noHover tableFixed`) to be reconciled to 05D (a KB
  session, own CL row). Verifier: every table's class set ∈ {`table table-bordered`, `table tableFixed`} (defect 0).
- **D10-6 — 2026-09-16 — the eight CED revision-brief modules (CEDR201 / CEDR301 / CEDR302 / CEDT201 / CEDT202 / CEDT203 / CEDT204 / CEDW303).**
  Question: scaffold from the brief (A), leave them (B), exclude them from the score (C)? Answer (verbatim): "Option C — exclude revision briefs from the
  comparison set. The eight stay in the corpus (so a developer still gets whatever PageForge can make) but stop counting in the score. No page changes; a
  one-line change to the gate configuration." Authorises: the eight modules are REMOVED from the skeleton / compare-set population (ONE list, honoured by
  every gate — the natural seam is `reference/tests/_corpus.py` `mods()`, the shared module-list helper 18 gate scripts import, reading a new
  `reference/tests/compare_exclusions.txt` with the eight codes and the reason; no gate has an exclusion hook today; the reason recorded: "Writers Template is an edit brief for content held in the previous module version — not a
  conversion source"); their Claude dirs STAY, are regenerated with their families as today, and keep their `_interactives.txt`; every baseline
  (`gate_baseline.json`, `CLAUDE.md` §14, the fast-loop baseline, the ceiling report's page count, `CORPUS_CENSUS.txt`) is RE-ESTABLISHED on the new
  population BEFORE any later class ships, so no round's delta is polluted by the population change (expected: the skeleton mean rises ≈ +0.3pp purely
  from the exclusion — recorded as a POPULATION change, never claimed as a gain). **Do this FIRST in the next session.** Option A (a phase scaffold
  with the edit notes) is NOT authorised. Authority: Chris; overrides nothing. No regeneration.
- **D10-7 — 2026-09-16 — Word equations (dropped by the V2 extractor; the output form).** Question: MathML (A), LaTeX (B), MathML + LaTeX in a comment
  (C)? Answer (verbatim): "Option A — MathML (the gold's form, the one that renders in MTK). ~80 pages gain their equations; the KB's 05A page gets a
  recorded correction (the "KB delta"). Gate-moving up (the gold has 2,052 of these); scoped regeneration of the 12 modules." Authorises: ONE round —
  (1) the extraction half: `DocxExtractor.js` reads `m:oMath` / `m:oMathPara` where they sit BESIDE the `w:r` runs of a `w:p` (an unknown OMML element is
  preserved as its text, never silently dropped — the V1.5 `ommlConverter.stats.unknownElements` discipline; counter `mathEquations`); (2) the output
  half: **MathML** — the gold's `<math xmlns="http://www.w3.org/1998/Math/MathML">` form; an equation inside a text run is inline, an equation paragraph
  on its own is block (measure the gold's 1,822 bare / 105 `display="inline"` / 66 `display="block"` split and follow its majority convention per
  position); ported from V1.5 `pageforge-site/js/omml-to-mathml.js` (tested against this corpus) through a small plain-object XML tree under V2's regex
  extractor; (3) `body class="container-fluid mathJax"` on every page that carries a `<math>` (the gold's per-page form, 0.92 precision). Scope: the 12
  WTs / 329 equations (MXDI102 154, MXDI301 69, PES1008 24, MXEX301 18, PES1007 17, MXFU302 15, MXFU401 12, MXDB301 6, MXDI201 6, CEDK401 6, MXDB202 1,
  SCCH301 1) → ~80 pages; scoped regeneration of those 12 (+ any module the OMML probe finds). Authority: the gold (level 3, 100% MathML) + Chris's V1.5
  finding (2026-08-26, MathML renders / LaTeX does not in MTK) over KB 05A's LaTeX letter — **KB delta:** 05A "MathJax / Equations" (lines 217–223) →
  MathML is the shipped form (a KB session, own CL row). Verifier: per module, docx OMML count == page `<math>` count (defect 0), plus the 12 selftests.
- **D10-8 — 2026-09-16 — the `alertPadding` activity class (KB 01F table vs the gold's 0.81 plain majority).** Question: apply (A), leave plain (B), make
  it a KB rule first (C)? Answer (verbatim): "Option B — leave the plain form (the gold's 81% and 05B's "own class set"). No change." Authorises: NO round
  — **CLOSED**. PageForge keeps plain `activity` on text / workbook boxes (+ the `dropbox` / `interactive` modifiers as today). KB note for the KB
  session's judgement (no edit required by this decision): 01F line 27's `activity alertPadding` row and 05B line 39's example are an EXAMPLE, not the
  default — 05B line 50's "follow the activity's own class set" governs.
- **D10-9 — 2026-09-16 — the lesson-menu label form (KB constraint 23 / 01B; session-8 Round 2 PICK).** Question: the KB's `<h5>` form everywhere
  including the overview tab (A), lesson menus only (B), leave (C)? Answer (verbatim): "Option A — apply constraint 23 everywhere: every lesson-menu label
  becomes <h5> with the KB's normalised wording, the section titles above them go, and the overview tab's labels become <h5> too. ~80 lesson pages + ~296
  overview pages change. A named KB-over-gold override, skeleton ≈ −0.1pp; close to a full regeneration (the menu is on every page)." Authorises: ONE
  round, FULL regeneration (it may SHARE the D10-5 full regeneration if each is first proven by its own OFF-toggle A/B on a sample — the r334 backstop
  precedent) — inside `#module-menu-content` on every LESSON page of every template: (a) every learning / success LABEL is `<h5>` — the r117 exact-fold
  phrase list is replaced by a ROLE classifier (the line that introduces the list: "We are learning…", "Ākonga will / can…", "Learning intentions",
  "I can…", "You will show your understanding…", "Success criteria", "Students will…" — measured over the WT corpus first); (b) the wording is
  NORMALISED per 01B lines 240–244: learning label `We are learning:`; success label `I can:` for years 7–10 and `You will show your understanding by:`
  for years 1–6 (the year level from `Module_Structure_Index.json` `module_meta` / the code's level digit — a data table; the writer's own label kept
  where the level is unknown); (c) NO section title above the labels on a lesson page (`<h5>Learning intentions</h5>`, `<h3><span>Learning
  Intentions</span></h3>`, "How will I know if I've learned it?" are dropped — 01B line 223); (d) the r81 eng-family `<p>` skip is RETIRED for lesson
  menus; (e) the constraint-70 OSSC "Ākonga will …" lead-in SENTENCE stays a `<p>` ABOVE the first `<h5>` (it is not a label — 01B lines 225–236);
  (f) the OVERVIEW tab's "We are learning:" / "I can:" labels become `<h5>` too (01B lines 196–197) — the r81 two_col eng-family overview `<p>` form is
  retired; the overview's `<h4><span>` Learning Intentions / How will I know titles STAY (01B's overview form, distinct from the lesson-page rule).
  Scope: 206 residue labels / 176 lesson pages / 42 modules + ~296 overview pages (`_r341_menulabels.log`); expected skeleton ≈ −0.1pp as a NAMED
  override (the 80 lesson pages whose gold keeps `<p>` — English 22 / ConnectED 20 / Maths 17 / OS 16 / L2L 5 — plus the overview pages whose gold is
  `<p>`). Authority: KB c23 + 01B (level 1) over the gold's per-series split and the 0.80 overview convention. Verifier: `_verify_menulabels` — every
  lesson-menu label `<h5>`, its wording in the normalised set, no section title above it (defect 0).

## Decisions from Chris (session 9 — 2026-09-16; every instruction he gave, in order; the durable record)
- **2026-09-16 09:21 — the session-9 kickoff (the standing §7 message, verbatim in the header above).** Question: continue the loop? Answer: continue in this
  folder; health check first; read the loop file + LOOP_STATE; reconcile git with the state file (nothing was uncommitted); honour every prior "Decisions from
  Chris" entry and never re-ask; **the message carries `REGENERATE CORPUS` for every round, scoped by CLAUDE.md §0a/§0b**; budget **12 rounds or 10 hours**
  (hard stop 19:21 NZST); **RUN UNINTERRUPTED (§5c)**; §6 context diet; update LOOP_STATE before and after every round; commit after every round, never push;
  stop only when §4 says so, then the §5 report + push block and "Next session starts with:". Authorises: a fresh PICK pass over today's corpus and any round
  it surfaces under the same rules. It answers NONE of the recorded decisions (stickyNav, equations, c23, alertPadding, table form, CED briefs, decisions
  1 / 4 / 5) — every one stays BLOCKED and is not re-asked.

- **2026-09-16 ≈11:05 — "STOP THE LOOP at the next logical point, without interrupting anything already running."** Question: keep going? Answer:
  let any regeneration / gate / verifier in progress finish, start no new round, class or rebuild; if the current round's remaining steps can be
  finished and proven in under 10 minutes, finish and commit it — otherwise **switch its toggle OFF so the corpus is back to its last proven state and
  leave its work uncommitted-but-described**; then record every decision of the session here, update LOOP_STATE with exactly where the loop is
  (round / class / step / shipped-declined-blocked / anything uncommitted) ending with "Next session starts with:", commit everything FINISHED in
  pageforge-site, give the §5 report with the push block, and confirm it is safe to close. Applied: r342 needed well over 10 minutes (the media
  embedded-lead gap, the 416-module re-probe, the scoped regeneration, gates, finalise) → both r342 flags OFF, disk identity re-proven, four files
  left modified and described; r341 was already committed (bb56efc). No answer to any recorded decision — all stay BLOCKED, not re-asked.

## Decisions from Chris (session 8 — 2026-09-16; every instruction he gave, in order; the durable record)
- **2026-09-16 08:03 — the session-8 kickoff (the standing §7 message, verbatim in the header above).** Question: continue the loop? Answer: continue in this
  folder; health check first (`git status`, `verify_after_transfer.sh` must PASS, delete a stale index.lock); read the loop file + LOOP_STATE; reconcile git
  with the state file — uncommitted engine/data files belong to the round in progress, never `git checkout` / `git restore` them, check them against that
  round's PICK, finish or toggle OFF; honour every prior "Decisions from Chris" entry and never re-ask; **the message carries `REGENERATE CORPUS` for every
  round, scoped by CLAUDE.md §0a/§0b**; budget **12 rounds or 10 hours** (hard stop 18:03 NZST); **RUN UNINTERRUPTED (§5c)** — never end the turn to wait, a
  blocked item ends the round not the session; §6 context diet; update LOOP_STATE before and after every round; commit after every round, never push; stop
  only when §4 says so, then the §5 report + push block and "Next session starts with:". Authorises: finishing r340 on the three uncommitted files (the
  in-memory 416-module probe, the url-only fence, the 9-module scoped regeneration, the proof suite, finalise, commit) and every further round under the
  same rules. What happened: r340 shipped (56bb70c); the Round 2 PICK found nothing ≥ 20 derivable pages → the loop stopped on §4 EXHAUSTION at ≈10:10.
- **Still open (NOT re-asked):** stickyNav, the equation form, decision 5 (interactive builds), decision 4 (Standard title-pair order), decision 1 (c47),
  the KB table form (05D vs 06 §6), the CED revision-brief modules, `alertPadding`; **new this session:** KB constraint 23's lesson-menu label form.

## Decisions from Chris (session 6 — 2026-09-15; every instruction he gave, in order; the durable record)
- **2026-09-15 20:49 — the session-6 kickoff.** Question: continue the loop? Answer (verbatim in the header above): continue in this folder;
  health check first; read the loop file + LOOP_STATE; reconcile git with the state file, never `git checkout`/`git restore` uncommitted
  engine/data files; honour every prior "Decisions from Chris" entry and never re-ask; **the message carries `REGENERATE CORPUS` for every
  round, scoped by CLAUDE.md §0a/§0b**; budget **12 rounds or 10 hours** (hard stop 06:49 NZST 16 Sep); §6 context diet; update LOOP_STATE
  before and after every round; commit after every round, never push; on stopping give the §5 report + push block and end LOOP_STATE with
  "Next session starts with:". Authorises: finishing r335 (flag ON, the 28-module scoped regeneration, gates, finalise, commit) and every
  further round's scoped/family regeneration + per-round commit under the same rules.
- **2026-09-15 ≈21:10 — "continue the loop once the gates finish."** Question: (implicit) carry on past r335? Answer: yes — continue the loop
  after the r335 proof suite. Authorises: the session's remaining rounds under the kickoff's budget and rules.
- **2026-09-15 ≈22:42 — "STOP THE LOOP at the next safe point."** Question: (implicit) how to close. Answer: do not start any new round or class;
  finish the current step only if it can be finished AND proven in under 5 minutes, otherwise switch the round's toggle OFF so the corpus is back to
  its last proven state; then (1) record every decision given this session under "Decisions from Chris", (2) update LOOP_STATE with exactly where the
  loop is and end with "Next session starts with:", (3) commit everything finished in pageforge-site, (4) the §5 report + push block, (5) a
  one-sentence safe-to-close confirmation. State at the instruction: the loop had ALREADY stopped on the plateau rule after r337 (committed 66c81c5)
  and its stop state was committed (f37135d) — no round in progress, no class in progress, no toggle to switch, nothing uncommitted. Authorises:
  this final LOOP_STATE record + its commit; no push.
- **Still open from earlier sessions (NOT re-asked):** stickyNav, decision 5 (interactive builds), decision 4 (Standard title-pair order),
  decision 1 (c47), the KB table form (05D vs 06 §6), the CED revision-brief modules, the equation form (MathML vs LaTeX) — all under
  Blocked classes; new this session: the `alertPadding` activity class (below).

## Decisions from Chris (session 5 — 2026-09-15; every instruction he gave, in order; the durable record)
- **2026-09-15 ≈16:05 — the session-5 kickoff.** Question: continue the loop? Answer (verbatim in the header above): continue in this folder;
  health check first; read the loop file + LOOP_STATE; reconcile git with the state file, never `git checkout`/`git restore` uncommitted
  engine/data files; honour every prior "Decisions from Chris" entry and never re-ask; **the message carries `REGENERATE CORPUS` for every
  round, scoped by CLAUDE.md §0a/§0b**; budget **12 rounds or 10 hours** (hard stop 02:05 NZST 16 Sep); §6 context diet (never read CLAUDE.md or
  BUILD_CHANGELOG.md whole; re-read the loop file + LOOP_STATE after every compaction); update LOOP_STATE before and after every round; commit
  after every round, never push; on stopping give the §5 report + push block and end LOOP_STATE with "Next session starts with:".
  Authorises: the five scoped regenerations (r330–r334), the full-ship backstop regeneration after r334, and every per-round commit.
- **2026-09-15 ≈20:00 — "STOP THE LOOP at the next safe point."** Question: (implicit) how to close mid-round. Answer: do not start any new
  round or class; finish the current step only if it can be finished AND proven in under 5 minutes, otherwise switch the round's toggle OFF so
  the corpus is back to its last proven state; then (1) record every decision given this session under a "Decisions from Chris" heading
  (date, question, answer, what it authorises), (2) update LOOP_STATE with exactly where the loop is and end with "Next session starts
  with:", (3) commit everything finished in pageforge-site with a clear message, (4) the §5 report + push block, (5) one-sentence
  safe-to-close confirmation. Authorises: r335 shipped OFF (data flag false, 28 modules regenerated OFF, manifest IDENTICAL) with its code
  committed but un-finalised; the final commit; no push.
- **Still open from earlier sessions (NOT re-asked, per the kickoff):** stickyNav (blocked), decision 5 (interactive builds), decision 4
  (Standard title-pair order), decision 1 (c47); new this session: the KB table form (05D vs 06 §6), the CED revision-brief modules, the
  equation form (MathML vs LaTeX) — all listed under Blocked classes.

## Decisions from Chris (session 2 — every instruction he gave, in order; the durable record)

| # | Date (NZST) | The question / situation put to Chris | His answer (verbatim) | What it authorises |
|---|---|---|---|---|
| D1 | 2026-09-14 ≈23:20 | The session kickoff (no question — the standing instruction that started session 2). | "Re-read LOOP__Autonomous_Rounds.md and LOOP_STATE.md, then continue the loop from where it left off. … This message carries the code REGENERATE CORPUS for every round of the loop, scoped by the §0a/§0b family rules in CLAUDE.md. Budget for this session: 12 rounds or 10 hours, whichever comes first. Follow the context-diet rules in §6 … Commit after every round, never push. When you stop, give me the plain-English report in §5 of the loop file, including the copy-and-paste push block." | Corpus regeneration for every round (scoped by the §0a/§0b family rules; a full rebuild when a change is corpus-wide); a budget of 12 rounds or 10 hours; a commit after every round with no push; the §5 report on every stop. Rounds 1–8 (engine r314–r321) ran under this. |
| D2 | 2026-09-15 ≈01:20 | After the power cut during Round 3 (engine r316): the two uncommitted engine/data files carried the partial r316 implementation; how to proceed? | "The computer lost power during Round 3 (engine r316). Do NOT discard anything. … check the two uncommitted files against the Round 3 PICK — finish anything incomplete, never git checkout or git restore them — and continue Round 3 from the REBUILD step onward. Budget: 12 rounds or 10 hours. Follow the §6 context-diet rules, and after every automatic compaction re-read the loop file and LOOP_STATE.md first. Commit after every round, never push." | Finishing Round 3 on the partial edits (never reverting them); the same budget and commit discipline; re-verifying the tree after the cut (done: git fsck, every JSON, corpus == manifest; the one casualty `batch_results.json` kept as a corrupt copy and repaired). Round 3 shipped as commit 414ef28. |
| D3 | 2026-09-15 07:48 | The plateau report's five decisions: (1) c47 exact-duplicate heading drop, (2) the TRR / MTK title source, (3) c65 / CL-0082 MTK quiz-content omission, (4) the Standard-template lesson-pair order, (5) interactive-build kickoffs. | "Yes to 2 and 3 — start with the TRR title source" | Two named rounds: decision 2 = the MTK title source — SHIPPED as Round 8 (engine r321, commit 968bf14); decision 3 = c65 / CL-0082, the `[MTKquiz]` shell without the quiz content — AUTHORISED, measured (`outputs/_r322_mtkquiz_shells.json`) and recorded as the next kickoff, not started (the 10-hour budget ran out). Decisions 1, 4 and 5 were NOT answered and stay open. |
| D4 | 2026-09-15 ≈09:39 | The final report after Round 8 (stopped on the budget rule). | "Record every decision I have given you in this session under a '## Decisions from Chris' heading in LOOP_STATE.md (date, question, my answer, what it authorises). Only carry out this task - DO NOT continue with the loop afterwards." | This section, mirrored into `converter-v2/loop/` and committed; nothing else — the loop is NOT resumed. The next session starts from the c65 kickoff above only when Chris says so. |

Not a session-2 decision but still governing: session 1's "STOP THE LOOP NOW" (2026-09-14 23:15, commit 763e036) ended Round 1's first attempt; session 2 resumed it under D1.

## Environment (decided 2026-09-14, session 1)
- **All gate tools, probes and regenerations run in WSL** (`wsl.exe -e bash -lc '...'`, project at
  `/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA`). WSL has Node v22.23.2, Python 3.14.4, git 2.53.0.
- **Why:** native Windows Node/Python cannot open files through the project's symlinks
  (`CONVERTER_V2/app` -> EACCES, `CONVERTER_V2/data` -> EINVAL), so every gate fails natively; WSL
  traverses them and `_MIGRATION/verify_after_transfer.sh` = PASS under WSL. Windows Python also
  defaults to a non-UTF-8 locale encoding, which the tools do not guard against.
- **Git commits are made with Windows git (2.55) from Git Bash** in `pageforge-site`. Never push.
- WSL `/tmp` persists between calls. Timings under WSL: defect audit ~10 s, ceiling tool ~60 s, KB facts ~55 s,
  16-shard census + dashboard ~4 min.
- Tool quirks: long file writes go through the Write tool (a ~30 KB heredoc hits ENAMETOOLONG); ONE heredoc
  per shell call (two heredocs in one call break the tool's quoting); commit messages from a file (`git commit -F`).
  Gold page filenames use the dot form `XMES101.02.html` (a `*2.0.html` glob finds nothing); gold dirs are
  nested under the template folder (`01-Finalized_Modules_/Standard/XMES101`) — resolve with `_corpus.mdir`.
  `grep` reports `InteractiveBuilder.js` as binary — use `grep -a`.
- `CONVERTER_V2/outputs/` and `reference/` are OUTSIDE the git repo; loop artefacts are mirrored into
  `pageforge-site/converter-v2/loop/` at each commit (see its README).
- `_regen_safe.sh` hard-codes `timeout 40` (the old sandbox wall): run `batch_convert.cjs` directly with a long
  timeout for regenerations, then prove freshness with `_content_manifest.py fresh --affected`.

## Position
- Round 0 (ceiling instrument): DONE 2026-09-14, commit ca59d13.
- Round 0b (KB amalgamation audit): DONE 2026-09-14, commit 784305b.
- Round 1 (engine r314, KB c43 — the upload box inside its activity): SHIPPED 2026-09-15 (session 2). Changelog entry written, AppVersion
  260618.85, CLAUDE.md §9/§11/§14 updated, `KB_AMALGAMATION_STATUS.md` row 43 → CAPTURED-LIVE, gate_baseline.json refreshed, ledger scoped #1.
- Round 2 (engine r315, KB c28 — the XHTML shell + the pairing-parser repair): SHIPPED 2026-09-15. AppVersion 260618.86, CLAUDE.md §9/§11/§14/§16,
  `KB_AMALGAMATION_STATUS.md` row 28 → CAPTURED-LIVE, full ship recorded.
- Round 3 (engine r316, KB c79 — the lesson's own bilingual title pair): SHIPPED 2026-09-15. AppVersion 260618.87, CLAUDE.md §9/§11/§14,
  `KB_AMALGAMATION_STATUS.md` row 79 → PARTIAL (pair mechanism LIVE), scoped ship #1 since the r315 full.
- Round 4 (engine r317, KB c45 + c90 — the acks block's template form): SHIPPED 2026-09-15. AppVersion 260618.88, CLAUDE.md §9/§11/§14,
  `KB_AMALGAMATION_STATUS.md` rows 45 + 90 → CAPTURED-LIVE, full ship recorded (ledger 0).
- Round 5 (engine r318, KB c83 — no lazy inside moving interactives): SHIPPED 2026-09-15. AppVersion 260618.89, CLAUDE.md §11/§14,
  `KB_AMALGAMATION_STATUS.md` row 83 → CAPTURED-LIVE, full ship recorded (ledger 0).
- Round 6 (engine r319, KB c89 — learningSupport on X-prefixed <html>): SHIPPED 2026-09-15. AppVersion 260618.90, CLAUDE.md §11/§14,
  `KB_AMALGAMATION_STATUS.md` row 89 → CAPTURED-LIVE, scoped ship #1 since the r318 full.
- Round 7 (engine r320 — the upload box's release order; c47/c95 measured and DECLINED): SHIPPED 2026-09-15. AppVersion 260618.91, CLAUDE.md
  §11/§14, scoped ship #2 since the r318 full. **LOOP STOPPED (plateau).**
- Round 8 (engine r321 — the MTK title source, decision 2): SHIPPED 2026-09-15 08:2x. AppVersion 260618.92, CLAUDE.md §9/§11/§14, scoped ship #3.
- Round 9 (engine r322 — the [MTKquiz] shell without the quiz content, decision 3 / KB c65): SHIPPED 2026-09-15 ≈11:35 (session 3). AppVersion 260618.93, CLAUDE.md §9/§11/§14, KB status row 65 → CAPTURED-LIVE, new gate `_verify_mtkquiz.cjs` in `run_all_gates.sh` (13 selftests), scoped ship #4.
- Round 10 (engine r323 — a button label never ends in a full stop, KB row 55's text defect): SHIPPED 2026-09-15 (session 3). AppVersion 260618.94, CLAUDE.md §9/§11/§14, KB status row 55 → defect CLEARED, FULL regeneration (the first since r318; scoped-ship counter reset). stickyNav BLOCKED — needs Chris.
- Round 11 (engine r324 — a `Lesson N` label is not a lesson title, KB c79): SHIPPED 2026-09-15 ≈12:35 (session 3). AppVersion 260618.95, CLAUDE.md §9/§11/§14, KB status row 79 → the label mechanism CAPTURED-LIVE, scoped ship #1 since the r323 full. c67 overflowYScroll DECLINED on measurement.
- Round 12 (engine r325 — phase-scoped activity numbering on the Fundamentals pages, the r217/r266 follow-up): SHIPPED 2026-09-15 ≈13:10 (session 3). AppVersion 260618.96, CLAUDE.md §9/§11/§14, scoped ship #2 since the r323 full. **THE LOOP STOPPED after it (plateau rule).**
- Session 4 Round 1 (engine r326 — a call-to-action button is an anchor, the KB's universal button form): SHIPPED 2026-09-15 ≈15:05 (session 4). AppVersion 260618.97, CLAUDE.md §9/§11/§14, KB status D-row added, FULL regeneration (scoped-ship counter reset).
- Session 4 Round 2 (engine r327 — a multi-word ALL-CAPS title renders in sentence case, the KB's title-casing rule): SHIPPED 2026-09-15 ≈15:15 (session 4). AppVersion 260618.98, CLAUDE.md §9/§11/§14, KB status row 1 → ALL-CAPS normalisation CAPTURED-LIVE, scoped ship #1 since the r326 full. Gate-neutral.
- Session 4 Round 3 (engine r328 — a submission button keeps its full 'Go to' label, KB constraint 55's label half): SHIPPED 2026-09-15 ≈15:25 (session 4). AppVersion 260618.99, CLAUDE.md §9/§11/§14, KB status row 55 → the label half CAPTURED, scoped ship #2 since the r326 full. Gate-neutral.
- Session 4 Round 4 (engine r329 — `[trigger engagement]` is a marker, not a button, KB constraint 43): SHIPPED 2026-09-15 ≈15:45 (session 4). AppVersion 260619.00, CLAUDE.md §9/§11/§14, scoped ship #3 since the r326 full. **THE LOOP STOPPED after it (plateau rule: r327 0.000 / r328 0.000 / r329 +0.004).**
- Session 5 Round 1 (engine r330 — the bilingual section id is the activity number, not a heading, KB 07B): SHIPPED 2026-09-15 ≈16:40 (session 5). AppVersion 260619.01, CLAUDE.md §9/§11/§14, KB status D-row added, scoped ship #4 since the r326 full. Skeleton +0.040pp — the plateau window restarts.
- Session 5 Round 2 (engine r331 — a bilingual section box's headings render at the KB's activity level h3, KB 07B): SHIPPED 2026-09-15 ≈17:10 (session 5). AppVersion 260619.02, CLAUDE.md §9/§11/§14, scoped ship #5 since the r326 full. Skeleton +0.022pp.
- Session 5 Round 3 (engine r332 — the empty footer → the KB's page-position form, KB 01B; + the BLL1 registry footer class): SHIPPED 2026-09-15 ≈17:40 (session 5). AppVersion 260619.03, CLAUDE.md §9/§11/§14, KB status D-row added, scoped ship #6 since the r326 full. Skeleton +0.269pp, ≥50 +10, ≥75 +4.
- Session 5 Round 4 (engine r333 — a right-hand alert is a side column; rhs / summary are not classes, KB 05B): SHIPPED 2026-09-15 ≈18:20 (session 5, commit c6660da). AppVersion 260619.04, CLAUDE.md §9/§11/§14, KB status D-row added, scoped ship #7 since the r326 full (backstop due at 8). Skeleton +0.066pp, ≥50 +5; compare_structure exact +15 / EXTRA −15 / missing +2 named.
- Session 5 Round 5 (engine r334 — the activity box's title heading is h3, KB 01F): SHIPPED 2026-09-15 ≈19:17 (session 5, commit b89f20c). AppVersion 260619.05, CLAUDE.md §9/§11/§14, KB status D-row added, scoped ship #8 since the r326 full — the full-ship backstop is DUE. Skeleton +0.167pp, ≥50 +17; every other gate EXACT.
- FULL-SHIP BACKSTOP after r334 (no code change): all 416 gated dirs regenerated 2026-09-15 19:26–19:43 (36 batches, all rc 0), `_stalecheck.sh` 0 stale, `_content_manifest.py diff` IDENTICAL (0 pages) — eight scoped ships proven complete; `_fastloop_snapshot.py` re-baselined from the fresh corpus (values unchanged), manifest snapshot, `_ship_ledger.py record-full --build 260619.05` (counter 0).
- Session 5 Round 6 = Session 6 Round 1 (engine r335 — the `[Engagement quiz button]` KB form, 01F + c65): BUILT + PROBE-PROVEN in session 5, SHIPPED OFF at Chris's stop, **flipped ON + SHIPPED 2026-09-15 ≈21:2x (session 6)**. AppVersion 260619.06, CLAUDE.md §9/§11/§14, KB status D-row added, scoped ship #1 since the r334 full backstop. Skeleton +0.018pp; every other gate EXACT.
- Session 6 Round 2 (engine r336 — the Fundamentals overview chip is a family convention, a registry correction): SHIPPED 2026-09-15 (session 6). AppVersion 260619.07, CLAUDE.md §9/§11/§14, scoped ship #2 since the r334 full backstop. Skeleton +0.000pp; every other gate EXACT.
- Session 6 Round 3 (engine r337 — numbered steps are a semantic <ol>, KB constraint 42): SHIPPED 2026-09-15 (session 6). AppVersion 260619.08, CLAUDE.md §9/§11/§14, KB status row 42 → CAPTURED-LIVE + D-row, scoped ship #3 since the r334 full backstop. Skeleton +0.001pp; every other gate EXACT. **THE LOOP STOPPED after it (plateau rule: r335 +0.018 / r336 +0.000 / r337 +0.001).**
- Session 7 Round 1 (engine r338 — an external destination is the KB's externalButton, 05D + constraint 75): SHIPPED 2026-09-16 ≈00:05 (session 7). AppVersion 260619.09, CLAUDE.md §9/§11/§14, KB status row 75 → the destination half CAPTURED-LIVE + D-row, scoped ship #4 since the r334 full backstop. Skeleton +0.023pp, ≥75 +1, ≥50 −1 named; every other gate EXACT. The untagged standalone-hyperlink candidate DECLINED on the live-extractor measurement.
- Session 7 Round 2 (engine r339 — a [button] whose destination is a video is the embedded video; the gold's consensus 0.90, nearest KB rule 01E): SHIPPED 2026-09-16 ≈00:55 (session 7). AppVersion 260619.10, CLAUDE.md §9/§11/§14, KB status D-row (01E extended to the button form), scoped ship #5 since the r334 full backstop. Skeleton +0.010pp, ≥50 +1, cs exact +3, every other gate EXACT, nothing named. The activity `interactive` modifier DECLINED on measurement (decision 5's population).
- Session 7 Round 3 (engine r340 — a standalone [link] paragraph that is nothing but a video url is the embedded video; the gold's consensus 0.90 of the url-only sites, nearest KB rule 01E; r339's sibling): PICK + code in session 7 (ended after the IMPLEMENT step), probe / fence / regeneration / proof / finalise in session 8 — **SHIPPED 2026-09-16 ≈08:45 (session 8)**. AppVersion 260619.11, CLAUDE.md §9/§11/§14, KB status D-row (01E extended to the link form), scoped ship #6 since the r334 full backstop. Skeleton −0.000pp at 3 dp (−0.0003; three dips NAMED, +0.0006 net of the two A1 pages), cs exact +1, every other gate EXACT.
- Session 9 Round 1 (engine r341 — a writer's tag typed in a NON-STANDARD RED is still a tag: the near-red run rule + the r299 weave's parenthesised-tail form; the loop's first fresh PICK after the session-8 exhaustion stop — the literal-tag-leak PROTECTED GATE had never had a PICK): **SHIPPED 2026-09-16 ≈10:40 (session 9)**. AppVersion 260619.12, CLAUDE.md §9/§11/§14, KB status D-row, CONVERTER_V2_GUIDE A4, **FULL regeneration (the backstop; ledger 0)**. Skeleton +0.021pp, ≥50 +7, ≥75 −1 named, cs exact +103, clean 97.81 → 98.91%, leak 288/46 → 26/23; HIS1005 ships the gold's exact 15-page set.
- Session 9 Round 2 = Session 11 Round 0 (engine r342 — a writer's MEDIA tag typed as a HYPERLINK is still a tag: `[audio 1]` linked to its sound file; the r341 seam extended to `w:hyperlink` runs behind three measured fences (head words / `exclude_words` / `link_target_match`); its own words the caption (`MEDIALEAD_OFF`); a tag member's bracket line or link keeps the hand-off box (`MEMBERTEXT_OFF`); a bare `[audio button]` never invents a journal label (`BTNLABELDEF_OFF`)): built + OFF-proven in session 9, **gap 2 decided by measurement, gap 3 + two reading-book half-builds fenced, flipped ON + SHIPPED 2026-09-16 ≈16:50 (session 11)**. AppVersion 260619.13, CLAUDE.md §9/§11/§14, KB status D-row, CONVERTER_V2_GUIDE A4, **FULL regeneration (ledger 0)**. Skeleton −0.003pp (≥75 −2 named — the r300 non-derivable audio form), ≥50 / ≥90 EXACT, cs EXACT, body 191 → 180 IMPROVED, clean / leak EXACT; 248 pages / 147 modules.
- Session 11 Round 1 (gate-config round r343 — Chris's D10-6: the eight CED revision-brief modules leave the comparison set via `compare_exclusions.txt` + `_corpus.gate_mods()`; no engine change, no regeneration): **SHIPPED 2026-09-16 ≈17:15 (session 11)**. AppVersion 260619.14, CLAUDE.md §9/§14, KB status D-row, `gate_baseline.json` + fast-loop baseline + ceiling RE-ESTABLISHED on 1955 pairs (skeleton 51.265%, ceiling 91.9%, 55.8% of achievable) — the +0.135pp is a population change, never a gain.
- Remaining KB queue (§D): stickyNav (BLOCKED — needs Chris; 33 KB-scoped modules,
  gate-neutral), c67 overflowYScroll (27 pages), c47 (decision 1 — now unblocked on the TRR side).

## The ceiling (Round 0 result — quote it in every report)
- Paired population 1880 pairs = the gate's 1939 minus 59 unmeasurable (13 TRR modules with a Media-List-only
  parsed file — 11 of them have an unparsed Writers Template.docx, TRR104/105 have none — plus TRR115/ENGJ403
  with no parsed file). No-source share, scaffold scope: raw 11.1% -> net 8.4%.
- **CEILING (scaffold) 91.6%** (loose upper bound 94.2%); full-scope ceiling 87.1%.
- **r313 SCAFFOLD 49.941% = 54.5% of achievable (band 53.0-54.5%)**; RAW 34.430% = 39.5% of achievable.
- Formula: % of achievable = skeleton mean / ceiling, ceiling = 1 - net no-source share (per-page mean).

## Round 1 (engine r314) — what shipped (the PICK, measurement and mechanism are in the round-314 changelog entry)
- **Class:** a wider-owned activity box closed at its widget's end, so the writer's trailing dropbox marker (still inside the activity) shipped
  its "Upload to dropbox" button in its own row UNDER the box; gold keeps it INSIDE and marks `activity dropbox` (KB c43; gold 702/733 non-BLL, 1024/1024 BLL).
- **Mechanism:** data `activity_wrapper.owned_activity_keeps_trailing_dropbox` {enabled, env ACTDBXINSIDE_OFF, max_lookahead 120};
  `ContentConverter.#dropboxTailHold` at the owner close site + the `_dbxStrayCloser` guard in the CONTAINER_CLOSE case;
  `InteractiveBuilder.#ddUploadBoxScan` factored out of `#ddUploadBox` verbatim, public `UploadBoxCandidate`. Splice: `outputs/_r314_splice_APPLIED.py`
  (the session-1 draft's owner-close anchor was one tab too deep — fixed, nothing else changed).
- **Regeneration:** 121 affected ∪ 212 dropDown family − 20 ghosts = 243 modules / 21 batches (~10 min WSL); 0 stale; 65 pages / 43 modules
  changed, 0 added/removed; changed ⊆ affected, zero from the working half; OFF re-conversion of the 43 hashes to the pre-round manifest (203/203).
- **Gates:** SCAFFOLD 49.941 → 50.031 (+0.090pp) / ≥50 1000→1005 / ≥75 191→192 / ≥90 16 / skipped 0; RAW 34.430→34.465; 60 moved (52 up / 8 down),
  pp-sum +174.49 / +66.76; clean 2056/2102 + leak 288/46 EXACT; cs exact 11355 (+92) / EXTRA 186 / missing 591 (−4); body 192 EXACT; tags 9557/9557;
  dropDown family verifier 295 groups / 205 units defect 0; all other verifiers line-for-line identical ON vs OFF; 12 selftests GREEN.
  **54.5% → 54.6% of achievable.**
- **Named dip:** ENGS201_7_0 −4.04 (its 7D box now IS the gold's inside-button `dropbox` form; alignment artefact of the removed row).

## Round 2 PICK (engine r315) — written before any code, 2026-09-15 00:20 NZST
- **Class:** KB constraint 28 — lowercase `<!doctype html>` + XHTML-style self-closing void elements (` />`). Claude ships `<!DOCTYPE html>` on
  2102/2102 pages and 0 self-closing voids (11992 `<img>`, 2930 `<br>`, every `<meta>`/`<link>`/`<hr>`).
- **Authority (§1b):** 1 = KB constraint 28 (universal) + `01A_TEMPLATE_LEVELS_CORE.md` "Void element self-closing syntax" / "DOCTYPE casing"
  + the `02C` verification checklist. The gold MAJORITY does NOT follow it (doctype UPPER 1810 : lower 572 : none 3) — the KB outranks the gold
  (the gold predates the rule); INTENTIONAL OVERRIDE, gate-neutral (every protected gate parses via html.parser, where `<img … />` == `<img …>`;
  the doctype and `<html>` are outside the skeleton).
- **Measured (gold, this session):** the two halves are ONE style — lowercase-doctype pages self-close ` />` 10371 : `/>` 552 : `>` 2519 (77%;
  img 80%, meta 99%, br 53%), uppercase-doctype pages self-close 1% (395+108 of 40853). Form = a space before the slash (` />`). Families:
  BLL lower 99 / UPPER 222 · TRR 48/35 · XDLS 41/52 · ENGS 33/39 · XGF 22/25 · ENGI 10/81 · MX*, HIS, AGH, PES, ARFUN 0 lower.
- **Population:** every page (2102 / 413 modules) — corpus-wide by construction (a shell/formatter change) → FULL regeneration (§2; ~12 min WSL).
- **Mechanism (planned):** `HtmlFormatter.Indent` gains a data-flagged pass `formatter.xhtml_voids` {enabled, env XHTMLVOID_OFF, doctype
  "<!doctype html>", void_tags [img br meta link hr input source wbr area base col embed track], close " />"}: the doctype line is rewritten and
  every void open tag (attribute-aware, the #GLUED pattern) gets its tail normalised to ` />`. One choke point (PageAssembler → Indent).
- **Gate expectation:** all EXACT (gate-neutral); proof = every gate identical to r314 + a byte-level check that ON differs from OFF ONLY by the
  doctype line and void-tag tails (normalise both and compare = identical).
- **Plateau guard:** gate-neutral KB rounds must alternate with gate-moving ones (LOOP §4 plateau = three consecutive <0.02pp rounds).
  Round 3 will therefore be a gate-moving class (c79 lesson-title bilingual pair, c90/c45 acks, or the dashboard's top gold-matching class).

## Round 2 (engine r315) — what shipped
- **Fix:** `formatter.xhtml_voids` {enabled, env XHTMLVOID_OFF, doctype, void_tags, close " />"}; `HtmlFormatter.#voidPass` + `#xhtmlVoids` per line in
  `Indent`. Unit test `outputs/_r315_unit.cjs` (18 cases ON/OFF). Splice `outputs/_r315_splice.py` (idempotent AFTER the prefix-test fix — a "new"
  that ends with its own anchor re-applied once and duplicated both blocks; caught by node --check + a duplicate-key JSON load).
- **Regeneration:** FULL, 416 dirs / 36 batches (~15 min WSL), 0 stale; 2102 pages changed / 0 added/removed. Toggle-OFF invariant proven three ways
  (59 in-memory pages; 387 pages of every-5th-module re-converted OFF = manifest, ON = normalise(OFF); the 82 pages of the 13 movers the same).
- **The exposed defect:** `anchor_compare.Tree`/`ATree` (the skeleton gate's PAIRING parser) had no void handling — OFF vs ON parses differed on
  298/469 (Tree) and 309/469 (ATree) pages. Repaired (`outputs/_r315_repair_anchor_compare.py`; pre-repair copy `_r315_anchor_compare_BEFORE.py`):
  identical on 469/469. Under the old parser this round's corpus scored 1941 pairs / 50.131 (kept as `_r315_sk_prerepair.json`).
- **Gates:** every gate other than the skeleton EXACT to r314. Skeleton RE-BASELINED: 1954 pairs (26 true pairs found, 11 off-by-one mis-pairs
  released — AGH1003 5_0↔06.0 became 5_0↔05.0 + 6_0↔06.0; MXDB301 4/5/6_0↔3/4/5.0 became 4/5_0↔4/5.0 + 6_0 released), mean 50.289 / ≥50 1028 /
  ≥75 193 / ≥90 16 / RAW 34.624; ceiling 91.6% unchanged (`_ceiling_r315.json`) → **54.9% of achievable**. Verifiers ON vs OFF over 83 modules:
  all ELEVEN verifier logs line-for-line IDENTICAL ON vs OFF (speechBubble truncated at the same 300 s point in both — MXFL301 is pathologically slow in that verifier, pre-existing). 12 selftests GREEN + skeleton selftest PASS.

## Round 3 PICK (engine r316) — written before any code, 2026-09-15 01:30 NZST
- **Class:** a lesson page whose OWN title is a `|`-joined bilingual pair ships ONE `<h1><span>` with the pipe inside (and, where the writer typed
  it, the module code in front: `TRR102 The vowels: Aa | Ngā Oropuare: Aa`); the KB and the gold ship TWO `<h1><span>`s — the lesson's own
  English + Te Reo pair — with no code. Gate-moving (h1 count is skeleton-visible).
- **Authority (§1b):** 1 = KB constraint 79 ("a second h1 span appears only where the writer gave THAT lesson its own bilingual name — the
  lesson's English + Te Reo pair, split by the TITLE BAR parsing rule") + `01A` "YEARS 9-10 and NCEA lesson pages" + `07D` MTK skeleton rule 7
  ("Titles in h1 span — Māori first, English second"); 3 = gold: two spans on 40/40 paired pipe pages (100%), Te Reo first on 26/26 TRR pages.
- **Triangulated:** ANZH101 L2 (WT `[H2] Lesson 2: Pūrākau | Stories` → gold `Stories` / `Pūrākau` → Claude `Pūrākau | Stories`); MXFL101 L1
  (WT `[H1] One | Tahi` → gold repeats the MODULE pair `Numbers 1–10` / `Ngā tau 1–10`, the c79 human anti-pattern → Claude `One | Tahi`);
  TRR102 L1 (WT docx, unparsed → gold `Ngā Oropuare: Aa` / `The vowels: Aa` → Claude `TRR102 The vowels: Aa | Ngā Oropuare: Aa`).
- **MEASURED (`outputs/_measure_r316_lessonpair.py` → `_r316_lessonpair.json`; every Claude lesson page through the gate's repaired pairing):**
  1549 lesson pairs; 40 pipe pages / 16 modules (Bilingual template 27 = TRR 26 + PNR 1; Standard 13 = MXFL101 6, ANZH 2, HIS/MXDB/TEDC/XDLS/XGF 1
  each) — gold two-span on 40/40. ORDER: TRR + PNR (body class `reoTranslate`) gold Te Reo FIRST 27/27 although the writer types English | Te Reo;
  Standard gold English-first 4 : as-written-Te-Reo-first 2 (n = 6, below the solidify floor — payload order kept, the overview's own rule).
  Code prefix in a lesson title: Claude 30 pages (TRR 25, MXEO102 4 — a module-title fallback, a different seam, PNR 1); gold 0 lesson pages.
  Unpaired pipe pages bring the population to ~45 pages.
- **Mechanism (planned):** data `header.lesson_bilingual_pair` {enabled, env LESSONPAIR_OFF, separators ["|"], strip_module_code, reo_first_when_
  body_class "reoTranslate", reo_detect "macron", reo_fallback "second"}; `SkeletonBuilder.#lessonPair` splits the lesson's own title (page.pageTitle)
  on the first separator after stripping a leading module code (+ dash/colon), orders per the rule, pushes BOTH spans exempt from the registry
  h1_count cap, and skips the module-Te-Reo push. Scoped regeneration: the ~16 affected modules + every module whose lesson title carries a
  separator (the same detector), plus the header/title family (any module with a bilingual [TITLE BAR]) as the §0b working half.
- **Gate expectation:** skeleton ≥ hold (40 pages gain the second h1 the gold has); MXFL101/TEDC402/PNR101 pages now match the gold's span COUNT
  even though the words differ (the skeleton is text-stripped). Named residue: TRR112/113 gold rewords the English half (editorial, C).

## Round 3 (engine r316) — what shipped
- **Fix:** `header.lesson_bilingual_pair` {enabled, env LESSONPAIR_OFF, separators ["|"], strip_module_code, reo_first_when_body_class "reoTranslate",
  reo_detect "macron", reo_fallback "second"}; `SkeletonBuilder.#lessonPair` + the pair exempt from the h1_count cap, no module-Te-Reo push beside it.
  Splice `outputs/_r316_splice.py` (idempotent by the prefix test). Probe `_measure_r316_lessonpair.py` → `_r316_lessonpair.json`.
- **Regeneration:** 17 affected ∪ 172 two-span-title family = 179 modules / 18 batches (~9 min); 0 stale; 45 pages / 17 modules changed, 0 added/removed;
  changed == affected, the 162 working-half modules byte-identical; OFF re-conversion of the 17 hashes to the pre-round manifest 127/127; every
  differing line on the 32 sample pages is an h1 title line.
- **Gates:** SCAFFOLD 50.289 → 50.345 (+0.056pp) / ≥50 1028 / ≥75 193 / ≥90 16 EXACT / skipped 0 @ 1954; RAW 34.624 → 34.662; 40 moved, ALL UP,
  pp-sum +110.47 / +74.77; every other gate EXACT to r315; verifiers ON vs OFF identical over the 17 (mcq differs only by the OFF run's
  "h1_count wants 2" notes, now satisfied); 12 selftests GREEN. **54.9% → 55.0% of achievable.**
- **Named:** Standard-group pair order (English-first 4 : as-written 2, n = 6 — kept as written); MXEO102's unsplit code-prefixed slash title bar
  + red-text `[H2]` lesson titles (the broader c79 source-order class); TRR overview pages with no title spans (MTK pathway); TRR112/113 editorial.

## Round 4 PICK (engine r317) — written before any code, 2026-09-15 01:55 NZST
- **Class:** KB constraints 45 + 90 — the acknowledgements block's TEMPLATE form: wrapper `acks acksTemplate` (+ `acksAI` with AI media), and the
  apology / copyright (with `currentYear`) / AI statements are GENERATED by those classes, never typed; only "All other images ©…" stays typed.
  Claude ships the pre-rule form on 394 overview pages (bare `acks`, apology + copyright typed in their own `acksLesson` divs); the 19 AI-variant
  pages already ship the KB form (round 241). Gate-visible (skeleton scores the whole body) — a NAMED KB-over-gold override.
- **Authority (§1b):** 1 = KB constraint 90 (CL-0090, a LOCKED admin decision; Design Team Lead, 27 Aug 2026 — the typed statements double up on the
  published page under the template classes) + constraint 45 + `05C_COMP14_ACKNOWLEDGEMENTS.md`. The gold is the OLD convention: bare `acks` typed
  421 blocks : template-class 74 (35 generated, 23 mixed) — the KB outranks (the gold predates the rule). Constraint 33 (acks on the overview page)
  is already live on 413/413 Claude pages; the gold's last-page placement (249 paired overview pages without a block) is the old convention.
- **Triangulated:** XMES101 0.0 (Claude `<div class="acks">` + apology div + … + catch-all div + copyright div; gold XMES101.08 the same old form on
  the LAST page); WJFUN105_0.0 is the KB's own example; the KB form = `<div class="acks acksTemplate">` … lesson groups … catch-all div, nothing else.
- **MEASURED (`outputs/_measure_r317_acks.py` → `_r317_acks.json`; every paired Claude acks page, the KB form SIMULATED on the page text and
  scored with the gate's own scorer):** 406 paired acks pages; 387 would change (Standard 279, Fundamentals 50, Inquiry 47, Bilingual 11).
  Gold on those pairs: no acks block 249, bare `acks` 116, `acks acksTemplate` 17, triple 23. EXPECTED SKELETON DELTA (the named override):
  pp-sum −46.05 → corpus mean **−0.024pp**, 88 pages down (all gold bare-`acks`, ≈ −0.5pp each), 12 up (gold `acks acksTemplate`), 287 zero;
  ≥50 0 crossers, ≥75 −1, ≥90 −2. Every other gate expected EXACT (the change is confined to the acks block: class token + two `acksLesson` divs).
- **Mechanism (planned):** data `Acks_Formats.standing_items.kb_template_form` {enabled, env ACKSTEMPLATE_OFF, acks_class_standard "acks acksTemplate",
  omit_always true}; `AcksBuilder` picks the standard class from it and applies the round-241 `template_variant_omit` list unconditionally (the AI
  variant unchanged; ACKSBOILER_OFF still governs the omit list). FULL regeneration (acks = corpus-wide by construction, §2).
- **Gate handling (the override policy, `Subject_Global_Parameters._meta.gold_override_policy` (b)):** the round is judged on (a) its own verifier —
  every acks block carries `acksTemplate`, none types the apology / copyright / AI statements, the catch-all kept — and (b) every OTHER gate
  holding; the skeleton is reported RAW and NET of the named pages (the 387 changed pages listed in `_r317_acks.json`), with the crossers named.
- **Plateau guard:** R1 moved, R2 neutral, R3 moved, R4 = a named-override dip (moves the gate). Fine.

## Round 4 (engine r317) — what shipped
- **Fix:** `Acks_Formats.standing_items.kb_template_form` {enabled, env ACKSTEMPLATE_OFF, acks_class_standard "acks acksTemplate", omit_always}; `AcksBuilder`
  takes the standard class from it and applies the r241 omit list always (AI variant unchanged). Splice `outputs/_r317_splice.py`. Probe
  `_measure_r317_acks.py` → `_r317_acks.json` (the KB form SIMULATED and scored with the gate's own scorer before coding — the predicted delta).
- **Regeneration:** FULL, 36 batches (~15 min); 0 stale; 394 pages / 394 modules changed, 0 added/removed; the round's own verifier 413/413 blocks
  in the KB form; OFF re-conversion of every 5th module 387/387 = manifest; canaries change only the overview's acks lines; AI-variant modules byte-identical.
- **Gates:** skeleton RAW 50.345 → 50.322 (−0.024pp) / ≥50 1028 EXACT / ≥75 193→192 (OSBY401_0_0) / ≥90 16→15 net (BLL242, BLL246 down, one up);
  386 moved — EVERY one a named page, 387/387 match the predicted delta; NET of the named pages IDENTICAL (49.050 = 49.050 over 1568); RAW-scope
  34.662 → 34.724 IMPROVED; every other gate EXACT to r316; verifiers identical ON vs OFF; 12 selftests GREEN. **54.9% of achievable (55.0% net).**
- **Named:** the gold's old last-page acks placement (249 paired overviews without a block) — constraint 33 already overrides it; never chase.

## Round 5 PICK (engine r318) — written before any code, 2026-09-15 02:35 NZST
- **Class:** KB constraint 83 (CL-0083) — NEVER `loading="lazy"` on an image INSIDE a moving-or-draggable interactive (rotating banner, carousel,
  drag-and-drop, click-drop incl. `.clickDropContent`, flip card, memory game, sketcher); every other image keeps it. Round 240's `FinishImg`
  adds the attribute to every image it builds, host-blind. Gate-neutral (`loading` is not a KEEP_ATTR; no gate reads it).
- **Authority (§1b):** 1 = KB constraint 83 (universal) + `01_PIPELINE` Images → Rules Common to Both Modes; 3 = gold AGREES: inside the hosts the
  gold ships 11730 images without the attribute vs 3574 with (76.6% — above the 0.60 floor); outside them the gold is era-mixed (4369 lazy :
  10731 not) and the r240 forward rule stands.
- **Triangulated:** XMES101 2D's clickDropContent (Claude `<img class="img-fluid" loading="lazy" …>` inside `.clickDropContent`; gold: no
  attribute inside its clickDrop); a flipCard front image (Claude lazy inside `.front`); a carousel slide image (Claude lazy inside `.carousel`).
- **MEASURED (`outputs/_measure_r318_lazyhosts.py` → `_r318_lazyhosts.json`; a void-aware depth walk on every page):** Claude 2424 lazy images
  inside hosts on 228 pages / 146 modules — carousel 1000, flipCard front 1040 + back 74, clickDropContent 182, bannerItem 86, clickDrop 42;
  by template Standard 1846, Fundamentals 472, Inquiry 106, Bilingual 0. Outside hosts: 9183 lazy (kept). Gold inside hosts: 23.4% lazy.
- **Mechanism (planned):** `HtmlFormatter` gains a whole-document pass `formatter.lazy_free_hosts` {enabled, env LAZYHOST_OFF, host_classes
  [the KB's 19], attribute} run before `Indent`'s line walk: a void-aware tag walk keeps an open-element stack and strips the attribute from any
  `<img>` whose ancestor carries a host class. One choke point (PageAssembler → Indent). Scoped regeneration: the 146 affected ∪ every module
  carrying any host class (the §0a whole-type family — the working half must come back byte-identical).
- **Gate expectation:** every gate EXACT; proof = OFF == manifest, and ON differs from OFF ONLY by the removed attribute on images inside hosts
  (normalise and compare). Widget verifiers A/B (the flipCard verifier's Mode-P template mentions the attribute — check it is identical).
- **Plateau guard:** R4 moved (the named dip); R5 gate-neutral is allowed; R6 may be neutral too (c89) but R7 must move.

## Round 5 (engine r318) — what shipped
- **Fix:** `formatter.lazy_free_hosts` {enabled, env LAZYHOST_OFF, attribute, host_classes [the KB's 19]}; `HtmlFormatter.#lazyFreeHosts` (a whole-document
  void-aware tag walk before the line passes). Unit test `_r318_unit.cjs` (9 containment cases). Splice `_r318_splice.py`. Probe `_measure_r318_lazyhosts.py`.
- **Regeneration:** FULL (the host family is 303 modules, over the 60% guard); 0 stale; 228 pages / 146 modules changed = the measured population;
  the round's verifier 0 lazy images inside hosts corpus-wide; every differing line an img losing exactly the attribute; OFF re-conversion 387/387 = manifest.
- **Gates:** every gate EXACT to r317; skeleton page-for-page identical (0 moved); 10 verifiers identical ON vs OFF over 20 affected modules; 12 selftests GREEN.

## Round 6 PICK (engine r319) — written before any code, 2026-09-15 03:05 NZST
- **Class:** KB constraint 89 (CL-0089, a locked admin decision) — a module whose CODE begins with `X` is a learning-support module and ships
  `learningSupport` appended to the `<html>` class list on every page (`class="notranslate learningSupport"`), never touching `template=`;
  a non-X module never receives it. Claude: 0 of 228 X pages (35 modules) carry it. Gate-neutral (the `<html>` tag is outside the skeleton).
- **Authority (§1b):** 1 = KB constraint 89 + `06_TEMPLATE_RECOGNITION` §4.4 ("the test is the code, not the reference files"); the gold has it on
  72 of 250 X pages (29%) and on 0 non-X pages — the KB outranks (the gold predates the rule); a CSS hook (larger font), no font CSS is written.
- **Triangulated:** XFUN01_00 / XDLS9004_03_0 / XWHA01-02 are the KB's own observed forms; Claude XMES101_0_0 `<html lang="en" level=""
  template="combo" class="notranslate" translate="no">` → target `class="notranslate learningSupport"`.
- **Measured:** Claude X pages 228 / 35 modules (XMES, XTAS, XDLS, XGF, XLP, XWHA …); non-X 1874 pages untouched. Gold X: LS 72 / no-LS 178.
- **Mechanism (planned):** data `skeleton.html_class_cohorts` {enabled, env HTMLCOHORT_OFF, rules [{code_prefix "X", add_class "learningSupport"}]};
  `SkeletonBuilder` appends each matching rule's class to the filled `html_open` tag's class list. Scoped regeneration: the 35 X modules +
  a completeness spot-check of non-X modules (byte-identical by construction).
- **Gate expectation:** every gate EXACT; proof = OFF == manifest, ON differs from OFF only in the `<html>` tag's class attribute.
- **Plateau guard:** R5 and R6 are gate-neutral; R7 MUST move a gate.

## Round 6 (engine r319) — what shipped
- **Fix:** `skeleton.html_class_cohorts` {enabled, env HTMLCOHORT_OFF, rules [{code_prefix X, add_class learningSupport}]}; `SkeletonBuilder.#cohortHtmlClass`
  at the html_open fill. Splice `_r319_splice.py`.
- **Regeneration:** scoped, the 35 X modules / 5 batches; 0 stale; 228 pages changed = the population; verifier 0 violations over 2102 pages; OFF
  re-conversion 228/228 = manifest; canaries change only the <html> line, non-X byte-identical.
- **Gates:** every gate EXACT; skeleton page-for-page identical; decomposition PASS; 12 selftests GREEN.

## Round 7 PICK (engine r320) — written before any code, 2026-09-15 03:50 NZST
- **Class:** the round-308 upload box releases the writer's captured text AFTER the button (button, To Do note, then the text), even when the
  writer typed that text BEFORE the dropbox marker ("3. Upload some pictures … here. [insert dropbox link]" → gold `<li>Upload some pictures…</li>`
  then the button). The gold keeps the button as the activity box's LAST content child in 629/720 non-BLL (87%) and 463/475 BLL (97%) boxes, and
  KB constraint 43 speaks of an activity that ENDS in the dropbox button. Gate-moving (the skeleton is order-sensitive).
- **Authority (§1b):** 3 = the gold (87% / 97%, above the floor; the writer's own order is the discriminator) with 1 = KB c43's wording; the r0b
  "dropbox terminates its activity" follow-up, narrowed to the part the bundle itself controls. The c47/c95 heading class was DECLINED first (above).
- **Triangulated:** XTAS101 1G (WT `3. Upload some pictures … here.[insert dropbox link] photo/video` → gold `<li>Upload some pictures…</li></ol>` +
  button → Claude button + note + `<ol><li>Upload some pictures…</li></ol>`); XDLS901_4_0 (WT marker THEN `Ka pai! You can now arrange…` → gold
  button then the text → Claude the same: text AFTER the marker stays after the button — the split is by the writer's order, not a blanket flip);
  CEDW501_6_0 (WT text then marker → gold text then button).
- **MEASURED (current corpus, `outputs/_r320_dbxlast_rows.json` + the signature count):** 49 upload boxes on 46 pages / 35 modules ship released
  content directly after the button (48 `<p>`, 1 `<ol>`); 37 activity boxes on 35 pages / 27 modules carry content after their dropbox button
  (gold convention: last child 87% / 97%). The scanner keeps memberItems in document order (backward absorptions `unshift`), so "before the
  opener" is exact.
- **Mechanism (planned):** data `interactive_builders.dropDown.upload_box.release_split` {enabled, env DBXORDER_OFF}; `#ddUploadBoxScan` returns
  rawBefore / rawAfter (members before the opener vs the opener's trailing text + later members); `#ddUploadBox` emits [before…, button, note,
  after…]; the leak guard still sees all released content; `UploadBoxCandidate` unchanged. Scoped regeneration: the affected modules + the §0b
  dropDown family (the r314 set, 212 modules).
- **Gate expectation:** skeleton ≥ hold (the reorder matches the gold's form where the text precedes the marker); every other gate EXACT; the
  dropDown verifier over the whole family defect 0.

## Round 7 (engine r320) — what shipped
- **Fix:** `interactive_builders.dropDown.upload_box.release_split` {enabled, env DBXORDER_OFF}; `#ddUploadBoxScan` counts released items before the LAST
  dropbox bracket member; `#ddUploadBox` emits [before…, button, note, after…]. Splice `_r320_splice.py`; member dump `_r320_memberdump.cjs`.
- **Regeneration:** the 212-module dropDown family (192 real) / 17 batches; 0 stale; 6 pages / 4 modules changed (ENGI400, XTAS101/102/103), 208
  working-half modules byte-identical; OFF re-conversion 22/22 = manifest; dropDown verifier 252 groups / 184 units defect 0.
- **Gates:** skeleton 50.322 → 50.325 (+0.003pp; XTAS102_0_0 +4.65, XTAS101_0_0 +1.29, ENGI400_3_0 +0.30), buckets EXACT; every other gate EXACT.
- **Measured and kept as is:** the gold keeps the button BEFORE after-marker text 16 : 3 (84%), so round 308's order for that case stands.

## Round 8 PICK (engine r321) — Chris's decision 2, written before any code, 2026-09-15 08:10 NZST
- **Class:** the MTK (Te Reo Rangatira, `reoTranslate`) title source. Claude ships NO title on 13 TRR overview pages, a stray body heading
  (`Finished!`, `Karakia Whakakapi`) as the lesson title on ~10 pages, and a single title where the gold has the pair on PNR102/104 lessons.
- **Authority (§1b):** 1 = `07A` "Sections to EXTRACT" (the metadata table → module code + title; the `[TITLE BAR]` row; the per-page
  `[H1] TRR1XX … | …` repetition), `07C/07D` rule 7 (titles Māori first, English second on every page; lesson page = the lesson's own title else
  the module titles), constraint 79; 3 = gold (TRR overviews all carry the pair Māori-first; lessons repeat the module pair where no own title).
- **Triangulated:** TRR108 (docx Module Code cell `TRR108: Ngā Orokati Tuarua – Final Consonants`; the `[TITLE BAR]` rows EMPTY → gold
  `Ngā Orokati Tuarua` / `Final Consonants` on every page → Claude overview no title, lesson 1 `Finished!`, lesson 2 `Karakia Whakakapi`);
  TRR102 (cell `TRR102 – Ngā Oropuare Aa`, every lesson opens `[H1] TRR102 The vowels: Aa | Ngā Oropuare: Aa` → gold the pair Māori-first on
  all 6 pages → Claude overview empty, lessons right since r316); PNR102 (metadata Module Name `Nga tau: 2 | Numbers: 2` → gold the pair on
  every page → Claude lessons `Nga tau: 2` only — the registry h1_count cap).
- **Measured:** 19 Bilingual-template modules with a Claude dir (16 TRR + 3 PNR); 13 TRR overviews without a title; 7 stray-heading lesson
  titles (TRR107 ×2, TRR108, TRR114 ×2, TRR203, TRR304) + 2 `Karakia Whakakapi`; PNR102/104 4 single-title lessons. Gate-visible (h1 count).
- **Mechanism (planned), one data block `header.mtk_titles` {enabled, env MTKTITLES_OFF, body_class "reoTranslate"}:** (A) DocxExtractor captures the
  Module Code cell's remainder as `metadata.moduleCodeTitle`; (B) PageAssembler's title fallback (after the r212 Module-Name source): the first
  `[H1]`/`[Title Bar]` item carrying a `|` anywhere (code stripped), else the cell remainder (pipe / spaced-dash-with-macron / single);
  (C) the overview emits the Māori-looking title first in reoTranslate modules; (D) a reoTranslate lesson with no own title pushes BOTH module
  titles (Māori first), exempt from the h1_count cap; (E) PageSplitter's first-heading harvest accepts only `[H1]` in reoTranslate modules.
  Scoped regeneration: the 19 Bilingual modules (+ a non-reo spot-check, byte-identical by construction).

## Round 8 (engine r321) — what shipped (Chris's decision 2)
- **Fix:** `header.mtk_titles` {enabled, env MTKTITLES_OFF, body_class reoTranslate, repetition_tags, harvest_heading_tags} + `front_matter_metadata.
  title_in_code_cell`: five seams (DocxExtractor cell remainder; PageAssembler fallback — [H1]/[Title Bar] repetition with a pipe, else the cell;
  SkeletonBuilder overview Māori-first; lesson without an own title = both module titles Māori-first, cap-exempt; PageSplitter harvest h1-only).
  Splice `_r321_splice.py`; title dump `_r321_titledump.cjs`.
- **Regeneration:** the 19 Bilingual modules / 4 batches; 0 stale; 24 pages / 14 modules changed; OFF re-conversion 57/57 = manifest; 6 non-reo canaries byte-identical.
- **Gates:** skeleton 50.325 → 50.368 (+0.043pp; 21 up / 2 down, named: TRR114_0_0 −1.01 vs the gold's two EMPTY title lines, TRR203_1_0 −0.38),
  buckets EXACT; cs exact +5; every other gate EXACT; 12 selftests GREEN. **55.0% of achievable.**
- **Named residue (the ceiling):** TRR203's English title, TRR304's second line, TRR111/112/113's module-level titles are in no WT; TRR114 gold empty.

## Round 9 PICK (engine r322) — Chris's decision 3, written before any code, 2026-09-15 10:55 NZST
- **Class:** KB constraint 65 / CL-0082 — the `[MTKquiz]` shell WITHOUT the quiz content. Round 232 (CL-0038) made the marker a non-capturing
  ELEMENT that emits the "Go to quiz" button + a To Do note and left the writer's quiz content rendered. CL-0082 (the designer's locked decision of
  21 Aug 2026) REVERSES that limb: the activity box holds ONLY (1) `<h3>` title, (2) the writer's student instructions, (3) the `Designer/Developer
  To Do:` note, (4) the button — in that order; the questions / options / `[correct]` marks / answer keys / the in-page quiz widget the writer also
  described / the quiz's own in-D2L title+instructions are omitted SILENTLY (no Red Flag). Gate-visible (skeleton: the dropped `<ol>`/`<p>`/tables).
- **Authority (§1b):** 1 = KB c65 + `05D_COMP14_BUTTONS_TABLES_COLUMNS.md` → MTK Quiz + constraint 1(b) (the one sanctioned silent omission);
  3 = the gold AGREES on every triangulated shell: SCPH301 4E (the quiz COMMENTED OUT, then note + button), ARFUN03 1A / ARFUN04 1H + 2E /
  TEFUN02 1D + 2A / TEFUN06 1A / TEFUN07 1A / EXBP901 1E (title + instructions + button, nothing else; EXBP901 and TEFUN07 SYNTHESISE the
  box), ENG1004 Checkpoint 1 (the four steps dropped). The gold keeps the content on the 157-of-199 pre-rule shells the old scan counted only
  where the writer typed NO marker (BLL110's 18 writer `[button] Go to quiz`s carry no `[MTKquiz]`) — those are outside the KB rule's scope.
- **Triangulated:** SCPH301 4E (WT `[activity 4E] Quiz` / `[body] Complete this quiz…` / `[MTK quiz. Trigger engagement…]` / `[button] Quiz` /
  Q1–11 with `[correct]` `[type answer]` `[Answer guide…]` / `[end activity]` → gold h3 + p + (commented quiz) + note + button → Claude h3 + p +
  To Do + button + EVERY question as `<ol>`/`<p>` + 20 orphan-`[correct]` Red Flags); TEFUN02 1A (WT `[H3] Show your kaiako` `[Body] If you would
  like to…` `[button] Go to quiz` `[MTK quiz…]` `[H3] Show your kaiako` `[Body] Now you can share…` `[end quiz]` → gold h3 + p + button (the
  post-marker H3/Body — the quiz's in-D2L text — dropped) → Claude h3, p, button, note, h4, p); ARFUN04 2E (opener `[Activity 2E] [MTK Quiz…]
  [H3] True or false…` then 8 `1. … ☐ True ☐ False` lines, no closer — the box auto-closes at the next `[H3]` → gold h3 + note + button → Claude
  h3 + notes + button + 8 `<ol>` + 16 `<p>`).
- **MEASURED (`outputs/_measure_r322_mtkquiz.cjs` → `_r322_mtkquiz_windows.json`, the LIVE engine over every WT the r232 detector lists —
  `_detect_mtkquiz.cjs` re-run: 64 spans / 25 modules, up from 33/21 at r232 with the corpus intake):** 64 markers on 33 pages / 25 modules;
  63 have content after them inside their window. Path 1 (an UNCONSUMED marker): 41 — 24 inside a writer's `[Activity]` box, 4 that ARE the
  opener (`[Activity 2B] [MTK quiz…][H3]`), 13 with no box at all (SCFUN01 ×4, TEFUN07 ×4, MXFUN02 ×2, EXBP901, SSOG301, ENG1005 ×1 loose).
  Path 2a (the marker rides a QUIZ-TYPE bundle — mcq / radioQuiz / dragAndDrop / clickDrop — as its opening span or a member): 15 — ARFUN03 ×4,
  ARFUN05 ×4, ARFUN04 ×2, TEFUN03 ×3, HPRE301 ×1, MXFUN02 ×1. Path 2b (a member of a NON-quiz container bundle — accordion ENG1004/1005 ×5,
  speechBubble TEDC401, `unclassified` HPRE203 p1 + MXFU402): 8 — NAMED, not chased this round (the widget's own member renderer; ENG1004's
  accordion is un-built anyway). Window ends: explicit `[end …]` closer 36, end of page 18, next `[Activity]` 5, page/section boundary 3, next
  marker 1, `[end MTKQuiz]` 1. By template: Fundamentals 36 (ARFUN/TEFUN/SCFUN/MXFUN/EXPFUN), Standard 27, Inquiry 1 (EXBP901); the 20-page
  floor is met (33 pages) and the KB row outranks (§1c).
- **Mechanism (planned), one data block `interactive_builders.mtk_quiz.omit_quiz_content` {enabled, env MTKQUIZOMIT_OFF, note_first true,
  todo_note (the KB wording + the writer's spec), silence_end {…}}:**
  (A) `#mtkQuizEmit` emits note THEN button (KB order) and ALWAYS the button — a writer's own quiz button the r232 pre-pass claimed
  (`_mtkQuizAnchor` / bundle `_mtkQuizBtn`) renders NOTHING under the flag (the button is the box's LAST child, the gold's 16:3 / 87% convention
  already recorded at r320), so one button ships per quiz.
  (B) SILENCE: after the marker emits (directly, or through `#mtkQuizBundleTail`), the page loop skips every content item until the quiz block
  ends — the enclosing activity box's close (explicit `[end …]` or the existing heading auto-close, ARFUN04 2E), any CONTAINER_CLOSE, the next
  `[Activity]` opener, a page/section boundary, the next marker, or — with NO box open — a rendered heading ≤ `rendered_heading_max` / any
  CONTAINER_OPEN (SSOG301's `[H2] Forming a government` ends it at once; EXBP901's `[Alert]` rubric stops it after the first table). A bundle whose
  trigger item is silenced is marked emitted (never renders later); the box-close and boundary items themselves still process.
  (C) Path 2a: a quiz-type bundle carrying the marker builds the SHELL instead of the widget — [owned activity open] + the members BEFORE the marker
  rendered as content (TEFUN03's `[Body] Show your kaiako…`) + note + button; the members after it dropped; the box closes at the widget's end as
  now. The un-built placeholder box is not emitted either (the whole widget is the quiz).
  Scoped regeneration: the 25 affected modules ∪ the §0b family = every module whose WT carries an MTK-quiz span (the detector's list IS the
  family — the tag has one canonical) plus the r232 button family (modules with a writer `[button] Go to quiz`: the ~40-module standalone class,
  so the prepass change is proven inert there).
- **Gate expectation:** skeleton: the 33 pages lose the dropped `<ol>`/`<p>`/tables and un-built quiz placeholders; where the gold commented the
  quiz out or shipped the shell (every triangulated case) the page RISES; a page whose gold kept the content visible (pre-rule — the old scan's
  "39 carry list/table markup") DIPS — a NAMED KB-over-gold override, judged per `gold_override_policy` (b): the round's own verifier
  (`_verify_mtkquiz.cjs`: every marker's box holds no `<ol>`/`<table>`/question `<p>` after the note+button; LIVENESS + DETECTION) and every other
  gate holding. Compare_structure / body_compare may move on the 33 pages (fewer content elements); leak/clean ≥ hold (fewer orphan-tag flags).
- **Plateau guard:** R8 moved (+0.043); this round is gate-moving (a named override, possibly net negative — judged net of the named pages).

## Round 10 PICK (engine r323) — written before any code, 2026-09-15 11:50 NZST
- **Class:** KB row 55's recorded text defect — a button label that ends in a full stop (`[button] Learning journal.` → `<div class="button">Learning journal.</div>`).
  The KB's canonical labels (constraint 55 "Go to dropbox" / "Go to portfolio", 14.11 "Upload to Dropbox", constraint 75 "Go to website", CL-0038 "Go to quiz")
  carry no terminal punctuation; the writer's full stop is sentence punctuation, not label. Authority: §1b-1 the KB's label forms + §1b-3/4 the gold
  convention (below) — the two agree.
- **Measurement (`outputs/_measure_r323_buttonstop.py` → `_r323_buttonstop.json`, every Claude and gold page, `button` / `externalButton` / `buttonD`
  divs, widget chrome excluded):** gold **9 of 5,553** buttons end in a full stop (0.16% — seven sentence-like labels: "Finished? Go to the next step." ×3,
  "4. Keep it real." …); Claude **441 of 3,052** (14.5%) on **221 pages / 90 modules** — Standard 381/2,486, Inquiry 49/334, Fundamentals 11/232; every
  subject family (MX 125, XDLS 89, HIS 37, BLL 30, CED 18 …); `button` 436 / `buttonD` 5 / `externalButton` 0. Top labels: "Upload to dropbox." 142,
  "Learning journal." 37, "Check answers." 27, "Go to quiz." 13, "Go to learning journal." 13, "Go to dropbox." 11, "Portfolio." 11, "Reset." 9. Other
  terminal punctuation the gold KEEPS ("?" 64, "!" 17, ":" 10) is NOT touched. Share ≥ 0.60 in every group → the rule is corpus-wide, one data flag.
- **Triangulation:** MXFL203 WT `[button] Learning journal.` / `[button] Check answers.` / `[button] Reset.` → gold `Go to journal` (an editorial
  relabel, class C — the full stop is gone either way) / `Check answers` / no full stop anywhere → Claude `Learning journal.` ×14, `Check answers.`;
  BLL233 WT `Upload to dropbox.` → gold `<div class="buttonD">Upload to dropbox</div>` → Claude `Upload to dropbox.`; HPFUN103 `[button] Check answers.`
  → gold `Check answers` (widget chrome) → Claude `Check answers.`.
- **Mechanism:** ONE seam — the generic `[button]`-family emit in `ContentConverter.#element` (the only site that fills a writer's label into a button
  form: 6,194; the external-link labelled site already refuses a label ending in `.!?:`): `label = #buttonLabelTrim(label)` strips ONE trailing full
  stop (never an ellipsis, never an abbreviation `e.g.`/`i.e.`/`etc.`) under `buttons.label_trailing_stop` {enabled, env BTNSTOP_OFF,
  strip_pattern, keep_pattern}. Nothing else changes.
- **Family (§0b):** the `button` tag family = 429 modules (`Module_Feature_Index.by_feature.button`) — the whole corpus → a FULL regeneration
  (allowed: the change is tag-family-wide; scoped ship count since the r318 full: 4). Expect 221 pages / 90 modules changed, 0 added/removed.
- **Gate expectation:** gate-neutral to the skeleton (text-immune); compare_structure / body_compare text-matching may IMPROVE (a label now equals the
  gold's); every other gate EXACT. Plateau guard: this is a text round — r322 was gate-moving, so no plateau risk yet.
- **Verifier:** the measure script re-run after the regeneration must report Claude full-stop buttons = the gold-like residue only (labels whose stop is
  an abbreviation) — expected 0–3; `--selftest`-style check: the ON probe over BLL233 shows `Upload to dropbox.` → `Upload to dropbox`.

## Round 12 PICK + what shipped (engine r325) — phase-scoped activity numbering, 2026-09-15 12:40–13:10 NZST
- **PICK (written before code):** the r217 / r266 recorded follow-up — "fundamentals number by PHASE". Measured (`_measure_r325_phasenumbers.py`):
  788 gold boxes on the 51 Fundamentals phase-panel modules vs Claude 397 (111 unnumbered, 45 bare digits); the gold numbers `{phase}{letter}`
  restarting per phase (53 of 101 pages exactly, the rest the same rule with human gaps); position-wise number matches 66, simulated 133.
  Authority §1b-3/4 (the gold convention at ≥ 0.85; no KB rule on Fundamentals numbering). Also sized and passed over: the empty hand-off boxes
  (`_measure_r325_emptyboxes.py`: 172 on 112 pages / 85 modules, 15 widget types — clickDrop 50, dragAndDrop 48 — no single shape ≥ 20; the
  TEFUN06 `[Clickdrop] + [Dropdown text]` pair is one module), the Bilingual `number="N.M"` section boxes (72 boxes / 25 pages, est. +0.01pp).
- **Fix:** `activity_wrapper.phase_numbering` {enabled, env PHASENUM_OFF, writer_digit_over_dedupe true, synthetic_unnumbered false}: the phasebreak
  ordinal on every lesson-number-less page, following the PANELS (an empty segment between sentinels makes no panel — ARFUN02 reached ordinal 6
  for 4 panels before the repair); `#phaseBareId` passes the writer's bare digit over the scanner's module-wide collision letter (ENFUN02 `1A` →
  `2A`); the r217 synthetic box asserts. A fourth seam (unnumbered synthetic boxes, the gold's `1A,-,-,-,1B` shape) was built, measured −0.004pp
  and turned OFF in the data. Splice `_r325_splice.py` (9 steps, reproduces the two files from the committed r324 tree).
- **Regeneration:** the 51 phase-panel modules (the §0b family — phase panels exist only in Fundamentals); 0 stale; 17 pages / 17 modules changed;
  OFF in memory = disk on 2,102/2,102 pages. Position-wise number matches 66 → 178.
- **Gates:** skeleton 50.416 → 50.435 (+0.019pp; 17 moved, 12 up / 5 down — ARFUN05 +21.86, ARFUN03 +8.28, ENFUN02 +3.45; dips NAMED: ENFUN05 −2.83
  with every box on the gold's number = a scorer alignment artefact, SSFUN03 −0.97 / TEFUN04 −0.96 / TEFUN05 −0.28 / TEFUN01 −0.26 = the r217
  synthetic boxes where the gold's invented boxes are unnumbered); every other gate EXACT; 13 selftests GREEN. **55.1% of achievable.**
- **Plateau:** +0.019pp < 0.02pp → the third consecutive sub-threshold round → STOP (§4).

## Round 11 PICK (engine r324) — written before any code, 2026-09-15 12:50 NZST
- **Class:** KB constraint 79 / CL-0069/0076 (a locked decision: the lesson page `<h1><span>` is the lesson's OWN title; `Lesson N` is stripped;
  the module title only as a disclosed fallback) — the `Lesson N` LABEL sub-mechanism, which the KB status row lists as still queued. Claude
  ships a header title that is nothing but a lesson label — `Lesson One` (ENGI102/ENGI202 ×9), `Lesson 1` (ANZH203), `Lesson #3 Opening
  Doors…` (ENGC201/ENGI203/ENGI301/ENGJ301/ENGJ302 ×23: the existing strip accepts `Lesson 3` but not `Lesson #3`), `Lesson One – The Ode`
  (ENGJ402 ×5: word numbers), `Lesson 5 continued` (CEDT501 sub-pages ×2) — where the gold ships the lesson's own title. Authority §1b-1.
- **Measurement (`outputs/_measure_r324_lessontitles.py` → `_r324_lessontitles.json`; every paired lesson page, the Claude title vs the gold's,
  classified by the difference):** 1,247 paired pages — exact 528 · case/whitespace/macron-only 87 · `Lesson N` label 44 · trailing punctuation
  only 8 · Claude = module title while the gold has its own 50 (the gold's source in the WT is scattered: plain line 11, not in the WT 14,
  [H2] 13, [LESSON] 6, [PAGE] 4 — no single derivable mechanism ≥ 20, recorded) · gold = module title 95 (the KB rejects, never chased) ·
  pair-count 45 · pair order 2 (decision 4, open) · other / editorial 388 (class C). The label class: Standard-template English modules
  (ENGI/ENGJ/ENGC/ANZH) + CEDT501's sub-pages; the gold strips the label on every one of the 44 (100%).
- **Triangulation:** ENGI202 WT `[LESSON] Lesson One` → `[H1] What is a traditional story?` → gold h1 `What is a traditional story?` (no body
  repeat) → Claude h1 `Lesson One` + body `<h3>What is a traditional story?</h3>`; ANZH203 `[LESSON] Lesson 1` → `[H2] *First European
  Explorers*` → gold `First European Explorers` → Claude `Lesson 1` + body h3; ENGC201 `[H2] *Lesson #3* Opening Doors with Open Questions`
  → gold `Opening Doors with Open Questions` → Claude `Lesson #3 Opening Doors with Open Questions`.
- **Mechanism (PageSplitter's title harvest, one seam):** `body_region.lesson_title_dedup.lesson_label_titles` {enabled, env LESSONLABEL_OFF,
  label_pattern (digits, `#N`, word numbers one–twelve, an optional `continued`), strip_existing_title, inherit_parent_on_subpage}: a page
  title that is ONLY a label is treated like the bare number the round-NN rule already replaces — the first real heading (label-only headings
  skipped) becomes the title, label stripped; a label-prefixed title keeps its own words (`Lesson One – The Ode` → `The Ode`); a label-only
  sub-page (`N.M`, M > 0) with no heading of its own inherits its parent lesson's title (CEDT501 5.1 → `Speaking up`). The lesson-NUMBER
  logic (the writer's `Lesson N` heading number wins) is untouched. The existing body de-dup then drops the body heading that now equals the
  title — the gold's shape (ENGI202 1.0, ANZH203 1.0).
- **Family (§0b):** the [LESSON]/[PAGE] page-title harvest touches every multi-page module → the OFF invariant is proven in memory over the whole
  corpus (`_r322_probe.cjs`); the regeneration is the affected set (the ON-changed modules) — a scoped ship (#1 since the r323 full).
- **Gate expectation:** skeleton-moving UP on the pages whose body heading is now de-duplicated (one h3 fewer, the gold's shape); h1 count
  unchanged; every other gate EXACT. ENGJ302's off-by-one (Claude page 2.0 carries `Lesson #1: Definitions` while the gold's 2.0 is `Wild
  Maths`) is a pagination difference — the strip still applies, the title stays different, NAMED.

## Round 11 (engine r324) — what shipped (KB constraint 79, the `Lesson N` label mechanism)
- **Fix:** `body_region.lesson_title_dedup.lesson_label_titles` {enabled, env LESSONLABEL_OFF, label_pattern (digits / `#N` / one–twelve / `continued`),
  strip_existing_title, inherit_parent_on_subpage}: PageSplitter's harvest skips label-only headings, strips the label from the harvested one,
  replaces a label-only page title, keeps a prefixed title's own words; a still-label-only sub-page inherits its parent's title; the body de-dup
  strips the same forms. Splice `_r324_splice.py` (5 steps); measure `_measure_r324_lessontitles.py` → `_r324_lessontitles{,_before,_after}.json`.
- **Regeneration:** scoped — 24 modules / 4 batches; 0 stale; **79 pages / 24 modules changed** = the ON probe's set; OFF in memory = disk on
  2,102/2,102 pages (`_r324_probe_off_0*.log`).
- **Gates:** skeleton 50.411 → 50.416 (+0.005pp; 14 moved, 11 up / 3 down — ENGI102_12_0 −2.82, _10_0 −1.22, _2_0 −0.54 NAMED: the pre-existing
  page re-leveller ranks the remaining [H2] headings h3 once the title heading is de-duplicated, where the gold keeps h4), ≥50 1030 → 1031; every
  other gate EXACT; 13 selftests GREEN. Titles: exact 528 → 550, the label class 44 → 0. **55.0% of achievable.**
- **Named residue:** Claude = module title while the gold has its own (44 pages, scattered WT sources); 8 trailing-punctuation titles; ENGJ302's
  off-by-one pagination; the gold's editorial re-wording of stripped titles (class C).

## Round 10 (engine r323) — what shipped (KB row 55's text defect)
- **Fix:** `buttons.label_trailing_stop` {enabled, env BTNSTOP_OFF, strip_pattern "\\.$", keep_pattern (ellipsis / e.g. / i.e. / etc. …)} — ONE seam,
  the generic `[button]`-family emit in `ContentConverter.#element` (`label = #buttonLabelTrim(label, tpl)` before the fill). Splice `_r323_splice.py`
  (3 steps, idempotent). Measure `_measure_r323_buttonstop.py` → `_r323_buttonstop.json` (before) / `_r323_buttonstop_after.json` (after).
- **Regeneration:** FULL — the `[button]` tag family is 429 modules (`Module_Feature_Index.by_feature.button`), so the whole corpus (416 modules / 70
  batches, `_r323_batches_run.sh`); 0 stale; **212 pages / 82 modules changed, 0 added/removed**; OFF in memory = disk on 2,102/2,102 pages
  before the regeneration (`_r323_probe_off_0*.log`). After: 29 of 3052 Claude buttons end in a full stop (the widget-internal label pickers' own sentence-labels — 'Wearable Art (WOW) entry to raise awareness of Cancer.' ×6, BLL 'Find things in your house that have the … sound in them.', story titles 'Weka in a flap.' — a different seam (InteractiveBuilder's URL-button / tile labels), the r307/r308 sentence-button class, named).
- **Gates:** skeleton 50.411 → 50.411 (+0.000pp; 0 moved, text-immune), ≥50 1030 / ≥75 193 / ≥90 15; cs exact 11360 / EXTRA 186 /
  missing 591 (text-matched 13398); clean 2056/2102; leak 288/46; body 192; tags 9557/9557; every verifier line identical; 13 selftests GREEN.
  **55.0% of achievable.**
- **Named residue:** the gold's own nine sentence-labels (class C); a writer's sentence that became a button loses only its stop (the r307/r308
  "sentence [button]" class is its own round).

## Round 9 (engine r322) — what shipped (Chris's decision 3, KB constraint 65 / CL-0082)
- **Fix:** `interactive_builders.mtk_quiz.omit_quiz_content` {enabled, env MTKQUIZOMIT_OFF, note_first, todo_note, instruction_max_items 2,
  instruction_tags, question_pattern, answer_mark_pattern, shell_max_members_before 2, quiz_bundle_types, non_quiz_widget_ends_silence,
  shell_box_plain, absorb_tags ["engagement quiz button"], absorb_window 2} + `Tag_Lexicon._meta.mtk_quiz_retag.omit_quiz_content_drop` {tags ["alert"]}.
  Seams (ContentConverter): the marker's emit DEFERRED behind an instruction run (`mtkPending` / `#mtkQuizRunStep`), note + button flushed in the
  open box, then the SILENCE (`mtkGuard`) to the block's end — an explicit `[end …]` ahead runs it there (`mtkCloserAhead`), a NON-quiz widget
  ends it (HPRE203 2D / SSOG103 6A speech bubbles kept); a quiz-type bundle carrying the marker builds the shell instead of the widget
  (`#mtkQuizShellBundle` "widget" / "lead", `#mtkQuizShellPre`, `#mtkQuizTrimLead`), its box the plain `activity` form (gold 142 plain vs 14
  interactive around "Go to quiz"); the writer's claimed button and a bare `[Trigger engagement]` render nothing; TagNormaliser drops a
  prose-resolved `alert`. Splice `_r322_splice.py` (22 steps — reproduces the four live files from the committed r321 files; idempotent);
  probe `_r322_probe.cjs` (in-memory A/B vs disk, `--save`); windows `_measure_r322_mtkquiz.cjs` → `_r322_mtkquiz_windows.json`, `_r322_showwin.py`.
- **New gate:** `reference/tests/_verify_mtkquiz.cjs` (+ `_selftest_core.cjs` SPEC, `run_all_gates.sh`): the KB shell per emitted note —
  note→button adjacency, nothing but title/instructions/bullets/inline before the button, no `<ol>`/table/media/quiz-type placeholder/answer-mark
  residue/question line, one button; a Path-2b non-quiz placeholder counts as residue. 61 shells / 23 modules defect 0; `--selftest` GREEN.
- **Regeneration:** the 58-module §0b family (25 marker modules ∪ 33 "go to quiz"/[quiz] WT mentions) / 10 batches; 0 stale; 30 pages / 23
  modules changed = the probe's set byte-for-byte; OFF in memory = disk on 306/306 family pages; the mcq/clickDrop/dropDown/accordion
  verifiers line-for-line identical ON vs OFF (mcq: engine console notes only).
- **Gates:** skeleton 50.368 → 50.411 (+0.043pp; 19 moved, 15 up / 3 down, NAMED KB-over-gold: TEFUN03_0_0 −4.60, ARFUN05_0_0 −2.19,
  TEFUN02_0_0 −0.33 — their gold built the writer's in-page [Quiz] widgets the KB says the MTK marker outranks), ≥50 1028 → 1030, ≥75 192 → 193,
  RAW 34.749 → 34.771; every other gate EXACT; 13 selftests GREEN. **55.0% of achievable.**
- **Named residue:** Path 2b — 8 markers captured by a NON-quiz container bundle (accordion ENG1004 ×3 / ENG1005 ×3, unclassified HPRE203 1C /
  MXFU402 5C, speechBubble TEDC401) keep the r232 form (HPRE203 1C's gold keeps the pre-marker image table, so the "widget" shell's table skip is
  the wrong tool there); the box-less shell — 32 of 61 shells have no [Activity] box, no synthesised box / default `Quiz` h3 (SCFUN01, ARFUN03,
  ARFUN05, TEFUN07/08, ENG1004/1005, MXFUN02, EXBP901, EXPFUN07, SSOG301, TEDC401); trailing prose inside the box after the quiz is silenced with it
  (EXPFUN07 1A "Well done…" — gold keeps it after the button); EXBP901 1.0's rubric alert + question-box table survive after the button (box-less
  silence ends at the first container open); ARFUN04 1H (mid-list member of the previous drag-and-drop's over-capture, r310 class); the post-marker
  instruction line BLLR201's gold dropped is kept; h4 vs the KB's h3 on the writer's titled boxes (pre-existing).
- **Lessons:** the r315 "suffix trap" bit twice more (steps (6)/(3c) early, (10b) late) — every splice step is now keyed on a unique substring;
  a Bash-tool heredoc halves backslashes AND turns `\r` into a raw CR — write any patch with escapes via the Write tool; a Windows-written code
  list carries CRs — `tr -d '\r'` before passing codes to node/python (`corpus.mdir` fails silently on `CODE\r`); an A/B `sed -i` on a data file
  bumps its mtime and trips `_fastloop_diff.py`'s freshness guard — regenerate the affected set again afterwards (done here, 58 modules).

## Session 11 · Round 1 (gate-config round r343 — D10-6) — what shipped (the eight CED revision-brief modules leave the comparison set)
- **Fix:** `reference/tests/compare_exclusions.txt` (CEDR201 / CEDR301 / CEDR302 / CEDT201 / CEDT202 / CEDT203 / CEDT204 / CEDW303 + the reason) + `_corpus.excluded()` / `gate_mods(root)`; the eight scored-population
  lines switched to `gate_mods` (`_skeleton_compare.py`, `_structural_defect_audit.py`, `compare_structure.py`, `body_compare.py`,
  `_discrepancy_audit.py`, `strict_compare.py`, `scaffold_audit.py`, `anchor_compare.py`) + `outputs/_measure_ceiling.py`; `mods()` stays
  inclusive (batch plans / manifest / registries / feature index). Durable record (the gate tools are outside git): `outputs/_r343_exclusions.py`
  (idempotent, re-applies every edit), mirrored with `compare_exclusions.txt` + `_corpus.py`; `_MIGRATION/CHECKSUMS__gates.txt` refreshed
  (82 entries, backup `.pre-r343.bak`), `verify_after_transfer.sh` PASS; `CORPUS_CENSUS.txt` notes the scored population (2103 / 409).
- **No regeneration, no engine change** (AppVersion 260619.14 bumped for the round ↔ build mapping only). **Proof:** `_r343_sk_final.json` vs
  `_r342_sk_final.json` = 1962 → 1955 pairs, exactly the seven paired briefs dropped (8.31 – 19.59%), 0 added, **0 pages score-moved**.
- **Gates (RE-BASELINED — the population change, never a gain):** skeleton 51.129 → 51.265 (+0.135pp; 51.1291 → 51.2646); ≥50 1073 / ≥75 198 /
  ≥90 15 EXACT; RAW 35.309 → 35.394; cs exact 11482 → 11469 (−13 = the seven pages' elements) / EXTRA 175 / missing 608 → 607; clean
  2087/2110 = 98.91% → 2080/2103 = 98.91%; leak 26/23; body 180 EXACT; every verifier identical to r342. **Ceiling re-measured on the new population:
  91.6% → 91.9% (`_ceiling_r343.json`; the tool's default run overwrote `_ceiling_r0.*`, restored from the mirror) → SCAFFOLD 51.265% =
  55.8% of achievable.** Fast-loop baseline re-snapshotted (`_r343_fastloop_snapshot.log`), `gate_baseline.json` refreshed.
- **The plateau window** ignores this round (a population change moves no page); it stands at r341 +0.021 · r342 −0.003.

## Session 11 · Round 1 PICK (gate-config round r343 — D10-6, the eight CED revision-brief modules leave the comparison set) — written before any code, 2026-09-16 16:58 NZST
- **Class:** Chris's D10-6 (Option C, verbatim in the session-10 decisions): CEDR201 / CEDR301 / CEDR302 / CEDT201 / CEDT202 / CEDT203 / CEDT204 / CEDW303 stay in the
  corpus (regenerated with their families, `_interactives.txt` kept) but stop counting in the score — their Writers Template is an edit brief for content
  held in the previous module version, not a conversion source. Authority: Chris (D10-6); overrides nothing. No regeneration; no engine change.
- **Seam:** `reference/tests/_corpus.py` gains `compare_exclusions.txt` (the eight codes + the reason) and `gate_mods(root)` = `mods(root)` minus the list;
  `mods()` itself stays INCLUSIVE (batch plans, the content manifest, the registries and the feature index still cover the eight). The gate scripts
  that define the scored population switch to `gate_mods`: `_skeleton_compare.py`, `_structural_defect_audit.py`, `compare_structure.py`,
  `body_compare.py`, `_discrepancy_audit.py`, `strict_compare.py`, `scaffold_audit.py`, `anchor_compare.py`'s gate list. Then RE-BASELINE on the
  new population BEFORE anything later ships: `gate_baseline.json`, CLAUDE.md §9 / §14, the fast-loop baseline, the ceiling (`_measure_ceiling.py`),
  `CORPUS_CENSUS.txt` — every delta recorded as a POPULATION change, never claimed as a gain (D10-6: expect ≈ +0.3pp on the skeleton mean).
- Steps: PICK ✔ · IMPLEMENT → PROVE (the eight absent from every gate's population; every other module's per-page score IDENTICAL) → FINALISE.

## Session 9 · Round 2 = Session 11 · Round 0 (engine r342) — what shipped (a writer's MEDIA tag typed as a HYPERLINK is still a tag)
- **Fix:** `Input_Doc_Rules.red_runs.hyperlinked_tag_runs` {enabled, env HYPERTAG_OFF, head_words, exclude_words ["animation"], link_target_match}
  + `DocxExtractor.#hyperlinkedTagHead` + the `block.hyperTag` side-channel: a run inside a `w:hyperlink` whose bracket opens with a listed
  media word, carries no excluded word, and whose target is a media-file carrier (the drive / sharepoint / istock / youtube hosts that carry 590
  of the 600 hyperlinked bracket runs, or a media file extension) counts as red; the r341 `nearOpen` depth keeps a split bracket whole.
  `embed` deliberately absent (its 3 hyperlinked runs = BLL262/263's `[Embed audio book]`, the r279 reading-book family — as a recognised
  element the carousel half-built a SharePoint Word doc as an iframe slide). **Riding on it:** `MEDIALEAD_OFF` — `MediaBuilder.media` (now
  taking `norm` as a sixth argument) folds a `hyperTag` item's own words in front of its caption (gap 2, DECIDED by `_r342_medlead_gold.py`:
  the gold keeps a media lead's words on 0.25 of the hyperlinked / 0.24 of the 359 pre-existing red-span sites — per-word widgets, the r300
  non-derivable form — so the fold is scoped to the hyperlinked class and the pre-existing leads stay dropped); `MEMBERTEXT_OFF` — session 9's
  `embedded_member_text` (a tag member's bracket line is hand-off content) + session 11's `linked_tag_counts` (a text-less hyperlinked media tag
  dumps `[audio] <url>` — gap 3: without it BLL141 / BLL171's dragAndDrop box and `.txt` entry vanished with the writer's `[drop and drag]`
  request); `BTNLABELDEF_OFF` — `buttons["audio button"].label_default: ""` (the gold's audioButton is text-less 1,014 / 1,014; 7 corpus sites
  + 8 new ones would have said `Go to your journal`).
- **Regeneration:** FULL (all 416 gated dirs, 36 batches / 4 workers, `_r342_fullship_par.sh`; seven batches rc 1 = the r279 parallel-write
  race on batch_convert's results cache (`BATCH FATAL: SyntaxError … in JSON`, `batch_progress.log`), re-run one at a time rc 0; 0 stale). The
  in-memory probe over ALL 416 first (`_r342_s11_probe_run.sh`): ALL-OFF (4 toggles) = disk 2110/2110; ON = 248 pages / 147 modules
  (`_r342_s11_affected.txt`). Manifest diff = exactly 248 / 147, 0 added / removed, the other 269 byte-identical (= the §0b whole-family
  proof: the r341 full ship's manifest is the OFF state). Quality (`_r342_s11_quality.py`): leaks by the gate's own predicate 15 → 15, no
  module worse; word-loss = reference URLs → `<img>` placeholders (r240 D3), tag tokens, note chrome, the 7 invented journal labels;
  hand-off boxes 7 gained (the gap-1 rescues) / 0 lost / 1 BUILT (BLL253_2_0's five `[image]`-hyperlinked clickDrop panels, verifier defect 0).
  The three-repair rule: gap 2 settled (fold), gap 3 the vanishing box (fence 1: the link counts), the two reading-book half-builds
  (fence 2: the target host + no `embed`), the CS-animation briefs (fence 3: `exclude_words`) — inside the round.
- **Gates:** skeleton 51.133 → 51.129 (−0.003pp; 51.1325 → 51.1291; pairs 1962); ≥50 1073 EXACT; ≥75 200 → 198 (−2 NAMED: BLL217_1_0 75.86 →
  73.83, BLL126_1_0 76.39 → 74.48 — the hyperlinked `[audio]` ships the standing audio element (in its own section row) + the words as a
  caption where the gold builds the per-word `wordDrag` / `word` widget, the r300 non-derivable form; the OFF literal `<p>[audio] …</p>` had
  matched a gold `<p>` by coincidence); ≥90 15; RAW 35.323 → 35.309; 41 moved — 16 up / 25 down, every mover in the affected set, pp-sum −6.76 scaffold / −1.65 RAW; every dip ≤ 2.21pp and every one the SAME class: a hyperlinked `[audio]` now ships the standing audio element (`audio.audioPlayer.icon`, in its own section row when it stands alone) plus its words as the caption `<p>`, where the gold builds the per-word `wordDrag` / `audioButton` / `word` widget (the r300 non-derivable `audioName` form — decision D10-3's dragAndDrop kickoff territory) and where the OFF page's literal `<p>[audio] …</p>` line had matched a gold `<p>` by coincidence — BLL151_2_0 −2.21, BLL217_1_0 −2.04 (75.86 → 73.83, the ≥75 down-crosser: `<p><b>[audio]</b> crane, above, glove…</p>` → `<p>crane, above…</p>` + a `row > col-md-8 > audio` where the gold's `row.wordDrag` holds 8 `div.word`s), BLL126_1_0 −1.91 (76.39 → 74.48, the other crosser: `<p>[audio]</p>` + a Writers Note → the audio element + the script as its caption), BLL252 / BLL253 / BLL166 / BLL131 / BLL222 / BLL241 / BLL114 / BLL157 / BLL176 / BLL172 / BLL242 −1.33 … −0.53; MXEO201_4_0 −0.32, XWHA02_3_0 −0.31, ENGC101_4_0 −0.22, HIS1001_10_0 −0.11, EXPFUN04_0_0 −0.00 = the session-9 gap-1 rescues (a hand-off box now stands — one collapsed widget marker — where the notes-only render stood; ENGC101's RAW 35.4 → 34.1 is the box's five `[Source image: …]` faces now dumped); the gains: BLL160_0_0 +2.61, BLL151_1_0 +2.06, BLL137_1_0 +2.03, BLL162_1_0 +1.75 (the gold ships `audio.audioPlayer.icon` there — exact), BLL251 +1.02, BLL166_1_0 +0.87, HIS1002_13_0 +0.65 (the hyperlinked `[Link: youtube]` → the r340 embed, the gold's own), BLL220 +0.57, BLL146 +0.53 …. cs exact 11482 / EXTRA 175 / missing 608 EXACT. body
  191 → 180 IMPROVED. clean 2087/2110 = 98.91% / leak 26/23 EXACT; tags 9557/9557; flipCard divergence 0; speechBubble defect 4 =
  r341's standing baseline; modal / mtkQuiz defect 0; over the 147: clickDrop 47 / 116 items defect 0, accordion 276 panels every one matching
  the human, dropDown defect 0, tabs defect 2 = PHE1005 / XLP06 (r196 / r281 editorial rewrites), carousel 18 mismatched ids = the r246 / r295
  A1 class, proven pre-existing (identical video ids OFF vs ON on all six modules, `_r342_s11_off6/`); 13 selftests GREEN. Fast-loop
  baseline re-snapshotted, manifest snapshot (2110 / 413), `_ship_ledger.py record-full --build 260619.13` (counter 0), feature index
  rebuilt (selftest GREEN). **55.8% of achievable.** The plateau window: r341 +0.021 · r342 −0.003 (one under-0.02 round).
- **Verifier:** the literal-tag-leak gate's own predicate over the 147 changed modules (`_r342_s11_quality.py`): **15 → 15**, no module worse; corpus-wide **26 / 23 → 26 / 23 EXACT**; the word-loss check over the 147 (every word incl. notes / dumps / attribute values): the losses are the reference URLs that became `<img>` placeholders (the r240 D3 class — istock / shutterstock / drive link text), the literal tag tokens, Writers-Note chrome, the seven `Go to your journal` labels the audio button no longer invents, and the `Go to video` externalButton HIS1002_13_0 replaced with the gold's own embed; hand-off boxes: **7 pages gain a box** (BLL150_0_0, BLL166_1_0, ENGC101_4_0, EXPFUN04_0_0, HIS1001_10_0, MXEO201_4_0, XWHA02_3_0 — the gap-1 rescues) and **1 page 'loses' one because it BUILT**: BLL253_2_0's five `[image]`-hyperlinked clickDrop panels (5 buttons / 5 panels with the prose inside; the affected-set clickDrop verifier 47 clickDrops / 116 items defect 0).
- **Named:** the audio element's FORM (audioPlayer vs the gold's text-less audioButton / per-word wordDrag — D10-3's build kickoffs); the 359
  pre-existing red-span media leads (gold drops 0.76); the hyperlinked `[audiovisual]` / `[av]` heads (39 runs — BLL254's `[Audiovisual
  request item 1]` now an r300 orphan note rather than the black link line, 1 site); the plain-BLACK tag class (≈ 300, the 26 residual leaks);
  BLL263_1_0's pre-existing `] Read it like you heard it` split-bracket heading; BLL126's `[embed book 1] Are we able…` question now visible
  inside its hand-off box's note.

## Session 9 · Round 2 (engine r342) — IN PROGRESS at the stop (Chris ≈11:05 NZST): what was built, what the proof found, what is left
- **State of the tree:** four files modified and UNCOMMITTED in `pageforge-site/converter-v2` — `data/Input_Doc_Rules.json` (the `hyperlinked_tag_runs`
  block, **`enabled: false`** at the stop), `app/js/DocxExtractor.js` (`hyperRed` in `#parseParagraph` + `static #hyperlinkedTagHead`), `data/Emit_Templates.json`
  (the `interactive_placeholder.embedded_member_text` block, **`enabled: false`** at the stop), `app/js/ContentConverter.js` (the `embeddedText` helper wired
  into `hasText` / `hasRenderedNonInstr` / the member dump of `#interactivePlaceholder`). With both flags OFF the engine reproduces the r341 disk corpus
  byte-for-byte (`_r342_flagsoff_identity.log`: 89/89 pages on BLL240 BLL150 BLL166 ENGC101 XMES101 XDLS904 XDLS905 HIS1002 BLL220 OSAH501 CEDW501 TRR203).
  **To resume: flip both `enabled` to `true` (never git checkout these files).** Patch scripts: `_r342_patch_membertext.py` (the ContentConverter + Emit_Templates
  edit, already applied); the DocxExtractor / Input_Doc_Rules edit was applied in-session (described in the PICK). The r341 checksum manifest was refreshed to
  this working tree so `verify_after_transfer.sh` PASSES (backup `_MIGRATION/CHECKSUMS__engine.pre-r342stop.bak`); its page-count expectation was corrected
  2102 → 2110 (the r341 corpus) in the script and `CORPUS_CENSUS.txt`.
- **Step reached:** PICK ✔ · TRIANGULATE ✔ · MEASURE ✔ · IMPLEMENT ✔ · REBUILD (in-memory probe) ✔ · **PROVE — in progress** · FINALISE ✘.
- **The in-memory probe (`_r342_probe_run.sh`, 4 shards, all 416 modules):** OFF (HYPERTAG_OFF) = disk **2110/2110**; ON changed **76 pages / 52 modules**
  (`_r342_probe_on_0*.log`; output saved under `outputs/_r342_on/` — NOTE that dir predates the member-text fix, so its BLL240 / BLL150 / BLL166 / ENGC101 /
  XMES101 / XDLS904 pages are the pre-fix form; `outputs/_r342_on2/` holds the post-fix output for those 7 modules).
- **Gap 1 — FOUND, FIXED (the member-text rule).** BLL240 1.1's `[word drag]` bundle has ONE member: the (now red) `[audio] while, whale, whirl, whole, whine`
  element with the words on its own bracket line and an empty tail. `#interactivePlaceholder`'s two guards (`hasText` / `hasRenderedNonInstr`) and the member
  dump read `blackAfter` alone, so the bundle read as notes-only: the box vanished and the writer's word list with it (`_r342_scanstate.cjs` traced it — the
  bundle IS captured, `consumedBy 3`, members [28, 29, 30]; my first diagnosis, a `bare_invocation_dissolve_empty` dissolve, was wrong — that rule is
  `types: ["interactive"]` only). MEASURED over the whole r341 corpus (`_measure_r342_embedded_members.cjs`, OFF state, `_r342_emb_off_*.json`): **1,555 un-built
  bundles / 351 modules carry a tag member with bracket-line text the box never dumps; 92 boxes / 55 modules are suppressed outright** — of those the
  content-ELEMENT/INLINE sub-class is **255 bundles / 124 modules (button 112, image 94, embed 56, audio button 12, external link 12, body 10, audio 9, video 9)
  with 7 boxes lost from the page today** (BLL150 0.0 + BLL166 1.0 `[audio]` word lists, ENGC101 4.0's five `[image] angry person …` faces, MXEO201 4.0 `[h3]`,
  XWHA02 3.0, EXPFUN04 0.0, HIS1001 10.0) — a PRE-EXISTING class the hyperlink rule made visible (the r293b rule: fixed, not worked around). The fix is scoped
  to members whose primary directive is ELEMENT / INLINE and whose span is a TAG (an instruction-class member already surfaces as the note before the box;
  an INTERACTIVE invocation's bracket text is its own spec and lives in the .txt) and renders the raw bracket line (`[audio] while, whale, whirl, whole, whine`).
  Post-fix (`_r342_on2/`): BLL240 1.1 box back with the words in the dump and the note holding only the writer's real instruction; ENGC101 4.0 gains its 4B
  dragAndDrop box with the five `[Source image: …]` lines; BLL150 / BLL166 keep their audio word lists; XMES101 2.0 dumps `[Audio animation] Names for each body
  part …` as one line (was `[Audio animation]` + a note).
- **Gap 2 — FOUND, MEASURED, NOT DECIDED (the media embedded lead).** `MediaBuilder.media` renders an element's OWN text from `blackAfter` (+ gathered following
  black) only — the words INSIDE the red span after the tag (the embedded lead, `RenderText(it.text)`) are never rendered, for audio, video and embed alike.
  MEASURED (`_measure_r342_media_embedded.cjs`, `_r342_medemb_summary.log`): free-body media elements with a bracket-line lead the page drops = **359 / 159
  modules in the r341 corpus (video 136, embed 129, audio 90, audio button 4)** — pre-existing — and **399 / 166 with the hyperlink rule ON; the 40 new ones
  (23 modules) are audio 31 / audio button 8 / video 1**: the BLL phonics word lists (`[audio] snail, paint, trail, stain, faint, train` → the gold's
  `audioButton` / player per word list; today the ON output ships a bare `<audio src="audio/.mp3">` and the words are gone), the `[audio button] / j /` sound
  buttons, and **XDLS903/904/905 0.0's `[Audio Animation N: <sharepoint script doc> Note this will be repeated across five units XDLS 902-6]`** — a CS-produced
  animation (the r233 / CL-0037 class; the gold ships a Vimeo `videoSection`) that the head word `audio` now routes to the audio ELEMENT: a `.mp3` default
  player and the writer's note LOST (the OFF page carried the literal `[Audio Animation 1:` + a Writers Note + the link line). Options for the next session,
  in order of preference: (a) fold the embedded lead into the element's `own` text in `MediaBuilder.media` behind a data flag (env e.g. MEDIALEAD_OFF) — the
  r80 title-drop semantics then apply unchanged (a BUILT video drops it as its title; audio / un-built keep it as the caption `<p>`), which restores every
  word on the 399 sites; (b) for the `[Audio Animation N:` / `[Audiovisual …]` CS-animation forms, either drop `audio` heads whose bracket carries `animation`
  from `head_words` (they stay the OFF literal + note) or route them to the r300 kind-todo note (`Designer/Developer To Do: Audio Animation 1 — <link> — note`),
  the KB-consistent form (05A / CL-0037 declined the vimeo scaffold; the note matches both gold eras). Decide by measuring (a)'s blast over the 359 pre-existing
  sites (a scoped §0b family regeneration of the audio / video / embed tag families — ~160+ modules — follows either way).
- **Still to explain from the ON diff (not yet looked at after the fix):** HIS1002 3/5/7/10/11/13/15 ("anchors removed with nothing added" — the hyperlinked
  `[Link: https://www.youtube.com/watch?v=…]` lines now red → the r340 url-only video-link class? verify each), XDLS904 5.0 / XDLS905 4.0 (a `[Image: Learn by
  Heart icon from LS global edits]` line now inside a box dump), BLL220 0.0, XMES101 2.0 — then the word-loss check (`_r341_quality.py` pattern) over all 76.
- **Remaining steps to ship r342:** flip both flags ON → settle gap 2 → re-run `_r342_probe_run.sh` (OFF must stay 2110/2110; explain every changed page) →
  word-loss / quality check → scoped regeneration = the ON-changed modules ∪ the §0b family (the audio / video / image / embed / link tag carriers; the ledger
  is at 0 after the r341 full ship) → `_stalecheck` / `_content_manifest fresh` → gates (`run_all_gates.sh`; skeleton `--json`; `_fastloop_diff.py`; the cs
  decomposition) → finalise (changelog r342, AppVersion 260619.13, CLAUDE.md §9 / §11 `HYPERTAG_OFF` + `MEMBERTEXT_OFF` (+ the gap-2 toggle) / §14, gate_baseline,
  KB status D-row, guide A4, LOOP_STATE what-shipped + position + round log) → loop mirror → checksum manifest → commit. Three repair attempts on gap 2 is the
  §3 limit — after that toggle OFF, prove identity, record BLOCKED, move on.

## Session 9 · Round 2 PICK (engine r342) — written before any code, 2026-09-16 11:05 NZST
- **How the PICK was made:** the r341 leak decomposition's two sibling sub-classes were sized by PAGES in gated modules (`_r342_blackblue_pages.py`
  → `_r342_blackblue_pages.log`): plain-BLACK tag brackets 195 / 98 gated modules but thinly spread (HIS1002 11 pages = its black `[LESSON N]`
  boundary markers, XGF9004 11, HIS1005 5, TRR111 5 — most modules 1–3 pages; heterogeneous: `[image]` asset briefs 41, `[body]` 40, headings 21,
  `[audio]` 20 …); link-BLUE bracket tags 182 / 52 gated modules — 177 of them INSIDE a `w:hyperlink`, and 175 of the 182 are the `audio` family
  (the BLL phonics writers hyperlink the `[audio N]` tag itself to the sound file). Free-body visible `[audio…]` brackets in today's corpus
  (`_r342_audio_visible.py`): **71 on 36 pages / 30 modules** (+ 423 inside hand-off boxes — widget members, decision 5's population). The
  dashboard / KB §D otherwise unchanged from the Round 1 PICK (nothing ≥ 20 pages unblocked).
- **Class:** a writer's media tag typed as a HYPERLINK — `[audio 1]` (run colour the hyperlink blue `1155cc` / `3494ba` / `0563c1`, or black)
  linked to the sound file on Drive / SharePoint — is invisible to the tag detector (only red runs are scanned; r341 added the near-red band),
  so it ships as the literal `<p>[audio 1] Kim had a roast pork bun.</p>`; a standard-red `[Audio 1] Shan went to the shop.` on the same
  page family already ships the `audioPlayer` scaffold (BLL162).
- **Triangulated:** BLL146 lesson 1 — WT `[audio 1] ` (`1155cc`, hyperlink → drive.google.com file) + black `Kim had a roast pork bun.` → gold
  `<audio preload="none" src="audio/….mp3" class="audioPlayer icon">` ×5 (one per line) → Claude `<p>[audio 1] Kim had a roast pork bun.</p>`
  inside the alertActivity box. BLL162 overview — `[Audio]` (`1155cc`, hyperlink → a drive folder) → gold `<audio … src="audio/BLL162 middle
  sounds.mp3" class="audioPlayer icon">` → Claude the literal. BLL134 lesson 2 — BLACK `[audio 1] cand` ×6 → gold `<div class="audioButton"
  audioName="cand">` ×6 → Claude `<p>[audio 1] cand</p>` (the black, un-hyperlinked sibling — recorded, not this round's mechanism).
- **The safety measurement that shapes the fence (`_measure_r342_hyperlinked_brackets.py` → `_r342_hyperlinked_brackets.log`, every run inside a
  `w:hyperlink` carrying a bracket, all WTs):** 600 hyperlinked bracket runs — heads `audio` 226 · `insert` 43 (already red) · `audiovisual` 27 ·
  `clickdrop` 26 (red) · `av` 12 · `number` 10 (`[Number and Operations]`, MXDI201 — a curriculum-strand link, NOT a tag) · `image` 5 · `video` 4
  · `embed` 3 · **and ~230 phonics WORD links — `[scissors]`, `[wrist]`, `[hedgehog]`, `[scratch]` … (BLL240/250/260: every word of a word list
  bracketed and hyperlinked to its sound — CONTENT, the gold's `audioTrigger` click-to-hear words)**. A blanket "hyperlinked bracket = tag" would
  turn every phonics word into a red instruction span → the rule is fenced to a DATA list of media head words (`audio`, `audios`, `audio button`,
  `audiovisual`, `av`, `video`, `image`, `embed`, `link`); targets drive.google.com 354 / sharepoint 125 / istock 29 / youtube 17.
- **Authority (§1b):** KB 05A lists three audio forms (`audioPlayer`, `audioPlayer icon`, `audioButton`) with no rule for which a free-body line
  takes — the FORM is the developer's choice (the BLL gold's `audioButton` 164 vs `audioPlayer` 20 across the 20 free-body modules; the `audioName`
  varies per module — "audio 1" / "cand" / "BLL222 Spelling 01" — r300's non-derivable finding stands); the RECOGNITION is level 3 / 4: the gold
  builds a sound element at every triangulated site (share ≈ 1.00). Class B-i. This round = recognition only; the element form stays Claude's
  standing `[audio]` form (the same scaffold a red `[Audio N]` line gets today).
- **Fix (data + env, the r341 seam):** `Input_Doc_Rules.red_runs.hyperlinked_tag_runs` {enabled, env HYPERTAG_OFF, head_words [...]}: in
  `DocxExtractor.#parseParagraph` a run INSIDE a `w:hyperlink` (`currentLink` set) whose text carries a bracket whose first word is in `head_words`
  counts as red (the r341 `nearOpen` depth keeps a split bracket whole). Strictly additive; the hyperlink target still rides `block.links`.
- **Rebuild scope:** the 416-module in-memory probe names the changed set (the audio / video / image / embed tag families are the working half —
  proven byte-identical by the ALL-OFF leg on every module the rule does not fire on); scoped regeneration of the changed modules (ledger 0 after
  the r341 full ship). Expected gate movement: ≈ neutral on the skeleton (`p` → `audio.audioPlayer.icon`, both unlike the gold's `div.audioButton`
  where it ships that; exact where the gold ships the player), leak gate unchanged (`audio` is not in its vocabulary); the visible literal
  `[audio N]` lines 71 → ~0 on the hyperlinked sites.
- Steps: PICK ✔ · TRIANGULATE ✔ · MEASURE ✔ · IMPLEMENT → REBUILD → PROVE → FINALISE.

## Session 9 · Round 1 (engine r341) — what shipped (a writer's tag typed in a NON-STANDARD RED is still a tag — the near-red run rule)
- **Fix:** `Input_Doc_Rules.red_runs.near_red_tag_runs` {enabled, env NEARRED_OFF, min_r 176, max_g 64, max_b 64, require_bracket true} +
  `DocxExtractor.#nearRed` + a paragraph-scoped `nearOpen` bracket depth in `#parseParagraph`: a run whose colour is in the red hue band but
  not on `red_hex_values` counts as red when it carries a `[` / `]` or continues a bracket an earlier near-red run of the same paragraph
  opened; a bracket-less near-red run outside any bracket stays black (the content fence — `c00000` is writer content in MXFU302 / ENGI401 /
  ENGS301). The exact list stays primary; strictly additive. **Riding on `DEFPAREN_OFF`:** the r299 definition weave's parenthesised-tail
  form (`paren_tail_def` — `aroha [definition] (Love, concern, compassion.) is important.` → the parenthesis is the tooltip, the sentence
  continues; XDLS904 / XDLS905 now match the gold's own `info="amount needed"` spans) + `lookback_skips_consumed` (a consumed marker spends
  no lookback budget within the SAME paragraph — the 4th definition of one sentence still finds it; the first cut crossed into the previous
  paragraph and mis-anchored CEDT104's hovers on the word "Hover" inside an earlier tooltip → fenced to the same `block`, byte-identical).
- **Regeneration:** FULL (all 416 gated dirs, 36 batches / 4 workers, `_r341_fullship_par.sh`; 3 batches rc 1 under the parallel run with
  empty logs, rc 0 alone — a mounted-filesystem transient; 0 stale). The three-leg in-memory probe over ALL 416 modules first: ALL-OFF = disk
  2102/2102; `NEARRED_OFF` alone = disk on 2101 (PES1003_8_0 = the weave refinement's one standard-red site, gold-ward, named); ON = 76
  changed + 10 new pages / 23 modules (`_r341_affected.txt`: ARFUN05 CEDO501 ENGFUN02 ENGS101 HIS1001 HIS1002 HIS1005 HIS1006 OSAH501 OSGM301
  OSGM401 OSGM501 OSOH301 OSOH401 PES1003 PES1008 TEFUN03 TRR102 TRR106 TRR109 XDLS904 XDLS905 XDLS912). Manifest diff = exactly those 23
  (76 / 10 / 2 removed), the other 393 byte-identical — the six scoped ships r335–r340 proven complete (the backstop); disk == probe ON on all
  184 pages of the 23. Quality (`_r341_quality.py`): leaks over the 23 by the gate's own predicate 269 → 7, no module worse; word-loss = tag
  tokens, URL fragments consumed into assets, the old dumps' "Empty" cells, duplicated instruction text, ENGFUN02's submission-checklist
  boilerplate (gold never ships it). Pagination: HIS1005 12 → 15 = the gold's exact page set; ENGFUN02 2 → 5 (gold 6); HIS1002 20 → 21 and
  HIS1006 14 → 15 (both over-paginated before; the near-red boundary tags now behave like the red ones — named).
- **Gates:** skeleton 51.112 → 51.133 (+0.021pp; 51.1120 → 51.1325; pairs 1954 → 1962); ≥50 1066 → 1073 (+7); ≥75 201 → 200 (−1 NAMED:
  OSGM501_5_0 77.01 → 74.03 — the near-red `[Click drop]` cells now BUILD the real 4-button clickDrop where a dump with literal tags had
  collapsed to a coincidentally-matching marker; RAW +3.5); ≥90 15; RAW 35.285 → 35.323; 39 moved — 20 up / 19 down, every mover in the affected set, pp-sum +70.06 scaffold AND +68.51 RAW; per MODULE (the honest view where a page set changed) HIS1005 41.45 → 50.69 (+9.24; its page set is now the gold's own 15 — the 5.1 / 6.1 / 9.1 sub-page boundaries were near-red), ENGFUN02 11.71 → 26.76 (+15.05; 1 → 5 pairs toward the gold's 6), CEDO501 +1.16, HIS1002 +1.57, TRR102 +1.18, HIS1006 −0.33 (its per-page −43.05 / −19.15 are pure RENUMBERING — an earlier near-red boundary now splits, so `_9_0` is a different lesson; the r186 / r243 pairing class); the NAMED dips: OSGM501_5_0 −2.98 (77.01 → 74.03, the ≥75 down-crosser), OSAH501_5_0 −1.23, OSGM301_2_0 −2.59, OSGM401_1_0 −0.77, OSOH301_1_0 −2.11, OSOH401_1_0 −1.38 = the near-red `[Click drop]` cells now BUILD the real clickDrop (4 buttons + 4 panels; the gold's own widget — OSGM501 lesson 5 gold ships 11 clickDrop buttons) where a `bilingual-unbuilt` dump with literal tags stood — the dump had collapsed to ONE widget marker that coincidentally matched the gold's, the r176 / r186 net-positive class (RAW rises on five of the six: OSGM501 53.6 → 57.1, OSGM301 39.8 → 42.7, OSGM401 41.7 → 44.9, OSOH301 23.6 → 25.5, OSOH401 20.0 → 20.4); HIS1005_2_0 −17.27 = the writer's `[Interactive] Please insert this image with the caption` tag (invisible before) now opens the hand-off box the tag asks for, where the gold shipped an image + caption (an A1 gold substitution); TRR109_5_0 −4.35 = the writer's `[Button] [Checklist]` now opens a widget box where the gold hand-built a drag-and-drop (48 `drag` / 29 `drop` — decision 5's population); ARFUN05_0_0 −5.04 = its two `[Insert video]` lines now embed the gold's OWN videos (YfNmlY1-t5k, MlXi8LfKv-0 — both in the gold page) on the single-page r322-named module, the alignment artefact; CEDO501_2_1 −2.65, HIS1005_0_0 −3.90, HIS1002_3_0 / _11_0, HIS1006_0_0, XDLS904/905 ≤ 0.4 = the same alignment class on pages whose literal `<p>[tag] …</p>` lines had matched gold `<p>`s by coincidence. cs exact 11379 → 11482 (+103) / EXTRA
  171 → 175 / missing 593 → 608 — EXTRA +4 and missing +15 are ENTIRELY HIS1005 (matched +133 / exact +107 — its page set is now the gold's, so 133 more elements text-match; the EXTRA sites are the now-built overview whakataukī box's `row > col` around what the gold puts straight in a `col`, the r61 greenlit class on newly-matched elements; the missing are the gold's editorial `alert` wrappers on the same pages) with HIS1006 missing −2; TRR109 matched −14 / exact −14 = the checklist section moving inside a widget subtree the comparator excludes (the r57 / r147 relocation artefact); no module outside the 23 moved (`_r341_cs_decomp.log`). clean 2056/2102 → 2087/2110 (98.91%); leak 288/46 → 26/23; body 191; tags 9557/9557; flipCard
  divergence 0; every widget verifier over the 23 defect 0 (accordion 32 panels / 9 modules; clickDrop 41 items incl. the new OS builds);
  13 selftests GREEN. The fast-loop's `--accept-named` for ≥75 / EXTRA / missing (the r289 override, every mover decomposed —
  `_r341_sk_movers.log`, `_r341_cs_decomp.log`). Fast-loop baseline re-snapshotted from the fresh corpus (values = the gate suite's), manifest
  snapshot (2110 pages / 413 modules), `_ship_ledger.py record-full --round 341` (counter 0), feature index rebuilt (8 shards + merge,
  selftest GREEN). **55.8% of achievable.**
- **Verifier:** the literal-tag-leak gate's own predicate over the 23 changed modules (`_r341_quality.py`): **269 → 7** leaks, no module worse; corpus-wide **288 / 46 → 26 / 23** — the 26 left are the plain-BLACK tag class (~20 sites: XGF9004's `000000` `[H3]`, ANZH401's `[H3]` inside an alert's black text, HIS1002 / MXDI201 `[Body Text]`, ENGI102's `[image]` asset briefs …), the three bilingual-cell `[Item N] [Image]` lines (TRR102 / TRR106 / TRR304 — the r167 reoMode class) and AGH1006's widget-release `[H3] Knowledge Check`; the word-loss check over the 23 (`_r341_quality.log`, every word incl. notes / dumps / attribute values): the only losses are the literal tag tokens themselves, URL fragments consumed into asset placeholders / embeds, the old dumps' `Empty` cells, duplicated instruction text, and ENGFUN02's trailing SUBMISSION-CHECKLIST boilerplate (the gold never ships it — a near-red end marker is now honoured).
- **Named:** the plain-BLACK tag class (≈ 300 brackets — the 26 residual leaks are mostly it; a content-vs-tag ambiguity, its own PICK if it
  clears 20 pages); the link-BLUE `[audio N]` class (250, BLL, hyperlinked tags); the bilingual-cell `[Item N] [Image]` leaks (r167 class);
  AGH1006's widget-release `[H3]`; HIS1005_2_0 (the writer's `[Interactive]` instruction now opens the hand-off box the tag asks for; gold =
  image + caption, A1) and TRR109_5_0 (the writer's `[Checklist]` → a widget box; gold hand-built a drag-and-drop, decision 5); ARFUN05_0_0
  (its two `[Insert video]` lines now embed the gold's own videos; the r322-named single page's alignment artefact). Ship ledger: FULL —
  counter 0. **Plateau window restarts (Chris's session-9 "continue" after the exhaustion stop): r341 +0.021.**

## Session 9 · Round 1 PICK (engine r341) — written before any code, 2026-09-16 09:55 NZST
- **How the PICK was made (a fresh §3 step 1 pass, not inherited):** (a) the r340 substitution ranking re-read row by row — every Standard row is
  declined / blocked / KB-correct, and the one row no session had named, `div.col-md-8.col-12 ⇐ div.col-12` (140 sites / 112 pages / 64 modules,
  `_r342_col12_sites.py`), is the activity box's INNER column where Claude is KB-correct (c63 `col-12`, CL-0036/0048/0077; the gold itself 0.90);
  (b) the 16-shard interactive census + `_coverage_dashboard.py --refresh` re-run on today's corpus (`_r342_dashboard.log`; coverage 50.8%,
  scaffold 51.11%, clean 97.8%): rows 1/3/5–7/9–11/13–21 are the un-built interactives (decision 5, BLOCKED), rows 2/4 are the advisory
  aggregates, row 8 the empty hand-off boxes (sized r325: no single shape ≥ 20), row 12 over-capture (42 pages, the r310 class) — and **row 15,
  the literal-tag LEAK (26 modules / 46 pages / 288 occurrences), a PROTECTED GATE that has sat at 288/46 through every round and never had a
  PICK**; (c) KB §D has no NOT CAPTURED row ≥ 20 pages that is not BLOCKED or DECLINED.
- **Class:** a writer's structural tag typed in a NON-STANDARD RED ships as literal text. The engine scans ONLY red runs for tags
  (`Input_Doc_Rules.red_runs.red_hex_values` = `ff0000` / `ee0000`; TagNormaliser's contract: "takes one raw span of writer text (a red span)";
  `ListsAndRuns.#renderBlackText`'s r73 note: "only RED text is scanned for [tags] … a black one … LEAKS through as literal content"). The HIS
  NCEA1 writer's red is `ed0000`, ENGFUN02's is `fa0000`, the OS* / CED / ARFUN / TEFUN writers use Word's standard "Dark Red" `c00000` — so
  `[H3] Using browser controls…` ships as `<p>[H3] Using browser controls…</p>` while the same module's `ff0000` tags convert.
- **Measured corpus-wide (`_measure_r342_blacktags.py` → `_r342_blacktags.{json,log}`, every bracket group in every WT that folds to a
  Tag_Lexicon alias, tallied by the colour of the run holding its `[`):** 96,817 red tag brackets vs **1,169 non-red**: NEAR-RED (hue red,
  r ≥ B0 / g,b ≤ 40, not on the list) **598** — `ed0000` 311 · `fa0000` 165 · `c00000` 120 · `ed1c24` 1 · `f72b2b` 1 — on **30 modules (28 gated)**:
  Standard 17 (HIS1005 97, HIS1002 83, CEDO501 27, HIS1006 15, OSGM301/401/501 + OSAH501 + OSOH301/401 32, HIS1001 3, XDLS904/905/912, ENGS101,
  ENGI102, PES1008), Bilingual 8 (TRR102 72, TRR111 20, TRR103/106/109/112/113 33), Fundamentals 3 (ARFUN05 15, TEFUN03 10, TEFUN05), Inquiry 2
  (ENGFUN02 164, CEDK401 5); link-BLUE 250 (`1155cc` / `3494ba` / `0563c1` — the BLL writers' hyperlinked `[audio N]` tags, 3 of the 5 heaviest
  modules have no Claude dir); plain BLACK ≈ 300 (`auto` 192, `000000` 101 — HIS1002's `[LESSON 1]` / `[End page]` boundaries, XDLS902's
  `[Video url]` ×13, TRR109's `[H1]`/`[H2]` ×15). Position: 887 paragraph-leading / 282 mid-paragraph. Gate view: the 288 counted leaks sit
  on 46 pages; ~137 Claude pages in the 28 near-red modules still carry a literal tag somewhere (~65 outside placeholders / notes).
- **The RISK measured (`_measure_r342_nearred_content.py` → `_r342_nearred_content.log`): near-red runs that hold NO bracket** — `ed0000` 170
  paragraphs (HIS1002 126 = the writer's drag-and-drop label lists and instructions, HIS1005 10 = "Please place this original image…", HIS1006
  10 = "Lesson 1 (1.0)" menu lines, TRR102 23 = answer keys / "Audio Files"), `c00000` 46 — and `c00000` is CONTENT in MXFU302 ("+ 5 = 9" ×7),
  ENGI401 ("tone" / "pace" ×5), ENGS301, MXEX401, CEDO501's own word list ("Internet" / "Website"), OSGM301/501's option lines. A blanket
  "near-red = red" rule would turn that content into stripped red-text instructions → NOT the rule. **The discriminator: a near-red run that
  CARRIES A BRACKET.** Every one of the 598 bracket-bearing near-red runs resolves to a lexicon tag; no bracket-less run is touched, no run
  that is red today changes — strictly additive.
- **Triangulated (WT → gold → Claude):** HIS1005 overview `[H1] Ātete | Resist – Part A` (`ed0000`) → gold `<h2>Ātete | Resist – Part A` /
  `[Body text] The whakataukī chosen…` → gold `<p>The whakataukī chosen…` / `[H2] The past shapes the present` → gold `<h2>`; Claude
  `<p>[H1] Ātete | Resist – Part A</p>`, `<p>[Body text]</p>`. CEDO501 lesson 3 `[H3] Using browser controls to navigate the web` (`c00000`) →
  gold `<h3>Using browser controls to navigate the web</h3>`; Claude `<p>[H3] Using browser controls to navigate the web</p>`. ENGFUN02
  `[H2] Close-up` (`fa0000`) → gold `<h2>Close-up</h2>`; Claude a 150-tag literal run on 2 pages.
- **Authority (§1b):** the KB is silent on the SHADE of red — its own raw-docx path reads bare `[tag]` brackets as tags with no colour at all
  (00B line 125 "Tags appear as bare [tag] (no 🔴[RED TEXT]🔴 markers)"; 02B "Red Text Rules" parse red text for embedded tags) → level 3/4, the
  gold: the human renders every near-red tag as its element on every triangulated site (the writer's tag is the writer's tag). Class B-i
  (a derivable input the converter drops). Share: 1.00 of the bracket-bearing near-red runs are tags; no group below 0.60 → SHIP.
- **Fix (data + env, one extractor seam):** `Input_Doc_Rules.json` `red_runs.near_red_tag_runs` {enabled true, min_r 176, max_g 64, max_b 64,
  require_bracket true} + env `NEARRED_OFF`; `DocxExtractor.#parseParagraph`'s `red` test becomes `red_hex_values.includes(color) ||
  (nearRedOn && hueRed(color) && /[\[\]]/.test(runText))`. The exact `red_hex_values` list stays the primary rule (untouched).
- **Rebuild scope (§0a/§0b + §2):** the seam is the extractor's red-run detector — a tag-normalisation-class change, so a FULL regeneration
  is authorised and doubles as the FULL-SHIP BACKSTOP (ledger: scoped #6 since r334, due at 8). The in-memory OFF/ON probe over all 416 modules
  (`_r340_probe.cjs` template) names the changed set first; modules with no near-red bracket run must be byte-identical by construction.
- **Expected gate movement:** literal-tag leak 288/46 → down (every `[H*]` / `[Body]` / `[Image]` / `[Activity]` leak in the 28 modules that is a
  near-red run); % clean 2056/2102 → up; skeleton up on the HIS / CED / TRR pages (headings and paragraphs where a literal `<p>` stood); every
  other gate hold-or-improve. Not covered (recorded, not chased this round): the link-blue `[audio]` tags (a hyperlinked-tag mechanism, BLL) and
  the plain-black brackets (a content-vs-tag ambiguity the r73 strip already handles for `[body]`) — each its own PICK if ≥ 20 pages.
- Steps: PICK ✔ · TRIANGULATE ✔ · MEASURE ✔ · IMPLEMENT → REBUILD → PROVE → FINALISE.

## Session 8 · Round 2 PICK (would have been engine r341) — written 2026-09-16 09:10–10:05 NZST — NO CLASS REACHED THE FLOOR → the loop stops on §4 EXHAUSTION
- **The queue after r340:** the r336 substitution instrument (`_r340_subst.log`, unchanged by r340 except the 27 embeds), the KB queue §D
  (every remaining ≥ 20-page row is BLOCKED — stickyNav, c23 (new, below) — or DECLINED — c47/c95, c67 — or an un-built widget builder —
  rows 26 D&D / 46 labelled diagrams / 48 typing = decision 5), the skeleton gap tallies re-run (`_measure_r334_skelgaps.py` → `_r341_skelgaps.log`:
  the top missing / extra lines are the generic p / div.row / WIDGET / img noise of the content-start and un-built-widget gaps, not classes), and
  FIVE fresh measurements of the rows not yet explicitly settled:
- **(1) `ul ⇐ ol` (gold bullets where Claude numbers; 34 sites / 25 pages / 14 modules — `_r341_ulol_sites.py`, `_r341_ulol_source.cjs`,
  `_measure_r341_numlists.cjs` → `_r341_numlists.log`):** 31 of 33 located sites are the writer's WORD-NUMBERED list (`w:numFmt` decimal) and 2
  are typed digits (r337) — KB constraint 42 (Universal: numbered steps / sub-questions → semantic `<ol>`) makes Claude KB-CORRECT. Corpus-wide the
  gold agrees: 2,530 Word-numbered lists in 330 WTs → gold `ol` **0.84** of found (Standard 0.87, Fundamentals 0.79, Inquiry 0.84). The only
  context that flips is the learning-intention list (gold `ul` 24 of 37 found, 0.35 ol) and ALL 24 `ul`s are ONE series — AGH1001 / AGH1004 /
  AGH1005 (NCEA1; every other subject numbers its LI lists 1.00) — the §1b human outlier at 13 pages, under the floor. NOT a class; recorded.
- **(2) `h5 ⇐ p` (gold h5 where Claude p; 32 sites / 31 pages / 14 modules — `_r341_h5p_sites.py`):** every site is the LESSON-MENU LABEL
  ("We are learning about/to…", "We are learning:", "You will show your understanding by…") that the r117 exact-fold phrase list misses. KB
  constraint 23 / 01B: lesson-page module-menu labels are `<h5>`, the writer's wording normalised to the canonical label. Measured INSIDE
  `#module-menu-content` on every paired lesson page (`_measure_r341_menulabels.py` → `_r341_menulabels.{json,log}`, void-aware parser): 1,491
  Claude labels / 690 pages; Claude `<h5>` 1,257 → gold h5 0.71; **Claude `<p>` 206 labels / 176 pages / 42 modules → gold h5 59 / p 80 / h3 24 /
  absent 39 = h5 0.35 of found** — split BY SERIES: NCEA1 0.95 (18/19), English 0.36 (h5 27 / h3 24 / p 22 — a three-way per-module split:
  ENGI h3-span, ENGJ301 / ENGS401 p, ENGJ402 / 403 h5), Mathematics 0.06, ConnectED 0.20, Online Safety 0.00 (the "Ākonga will…" lead-in
  SENTENCE = KB constraint 70's own `<p>` exception — Claude right), Leaving to Learn 0.00. The one variant that solidifies — the writer's
  "We are learning about/to…" (fold `we are learning about to`, 29 pages / 10 modules, gold h5 0.69) — is **17 pages once the r81 eng-family
  menus (skipped by `skip_named_promotion`; their gold is h3 / p) are removed** (AGH1002 6, AGH1003 8, PES1007, MXDI301, MXEO201) — under the
  floor. Applying c23 to the whole residue would be a KB-over-gold override on 80 gold-`p` pages for 59 gold-h5 pages (a wash the loop does
  not take unattended) and, read with 01B line 196–197 (the OVERVIEW tab's "We are learning:" / "I can:" labels are `<h5>` too), would also
  overturn the r81 two_col eng-family form on ~296 overview pages where the gold keeps `<p>` at 0.80 → **BLOCKED — needs Chris** (below).
- **(3) The Inquiry `body.inquiry` token (`body.inquiry.container-fluid ⇐ body.container-fluid`, 22 pages / 22 modules):** the gold ships the
  token on every module's crumbs / inquiryPanel landing page and on no plain page (r107's measured invariant re-confirmed: 66 token pages, 62
  with panels; 0 all-no modules); Claude ships it iff it BUILT the panels (25 modules) and 24 Inquiry modules build none — the crumb-less
  dialects (`[tab N]` 11 / `[LESSON N]`-as-panels 5 / `[page N]` 2 / EXPFUN `[section N]` 4 / TWH* 5, each a PanelsBuilder round of 1–14 pages —
  and the CED revision briefs, BLOCKED). Emitting the token without the layout would break the r107 invariant to buy the root skeleton line;
  downstream of the dialect rounds, not a class of its own.
- **(4) The Bilingual audio form (`audio.audioPlayer.icon` EXTRA 148 occ / 32 pages / 14 modules vs the gold's `div.audioImage` 290 occ / 33
  pages / 11 TRR modules + `span.audioTrigger` 216 / 13 / 5 — `_r341_audioforms.py`):** the gold's `audioImage` is a click-the-picture-to-hear
  WIDGET (`audioImageOption` per image — "Click on the vowel and hear its sound"), not a player form; the gold uses the plain `audioPlayer.icon`
  on 20 pages / 12 modules where the writer wants a player. An un-built interactive type = decision 5's population; recorded, not chased.
- **(5) `┌ 2× repeated ⇐ ┌ 3× repeated` (50 occ / 49 pages / 40 Standard modules — `_r341_repeat32.py`):** 27 of 50 are three `<p>` where the
  gold has two (the human merged or dropped a paragraph), 9 `li`, 6 `b`, 3 `td` — the ceiling's editorial rewording (class C), no derivable
  discriminator.
- Also re-checked and unchanged: `div#body.container-fluid` (the gold's BLL17x minority), `div.row.supervisor` 16 pages, `div.alert.solid` 19,
  `li ⇐ b` 17, `img.img-fluid ⇐ p` 15, `div.col-md-8 ⇐ div.col-md-8.col-12` 25 pages / 4 modules (a module quirk), the Fundamentals
  `phaseContainer.justify-content-center` 6 modules and `h2 ⇐ h3` 9 — all under the 20-page floor or already declined; the r314 follow-ups
  (dropbox terminates / release order) were closed in r320 / r326. The doc-14 families stay CAPTURED-INERT (`master_enabled:false`, the
  2026-07-12 policy's "one family at a time via a measured round"; every derivable family convention has been worked as its own constraint).
- **Verdict:** no class with a derivable population ≥ 20 pages remains and no KB row ≥ 20 pages is left that a session can act on without a
  decision from Chris — the §4 EXHAUSTION stop (the GOOD ending). Everything remaining is class C, DECLINED, or BLOCKED on a decision.

## Session 7 · Round 3 (engine r340) — what shipped (a standalone [link] paragraph that is nothing but a video url is the embedded video) — FINISHED IN SESSION 8
- **Fix:** `elements.external_link_video_embed` {enabled, env LINKVID_OFF, host_match, media_follow} + `MediaBuilder.LinkVideoEmbedOn / LinkVideoHost /
  LinkVideoUrlOnly / FollowingVideoLinkTag`. **Seam A** (`ContentConverter.#inline`, before the r76 standalone-button rule): an `[external link]`-
  family item that is url-only — `!labelText` AND the item's WHOLE paragraph block minus red spans / urls / `*` is empty — whose url is a video
  url → `MediaBuilder.media(it, [it], 0, "video", run)`. **Seam B** (`MediaBuilder.media`'s following-link source): a `[video]` / `[embed]`
  element with no own url whose next unconsumed item is such a url-only external-link TAG item takes that url and consumes the item (the r247
  black-line rule extended to the tagged line); the `[embed]` route peeks the same helper so the phantom "[video] with no URL found" note never
  prints. `host_match` falls back to r339's `buttons.video_destination.host_match`.
- **The fence the probe forced (a narrowing, not a revert):** the first 416-module probe changed 22 pages / 12 modules — HPRE203_5_0, TEFUN07_0_0,
  XDLS908_5_0 were the PROSE form (18–31 visible words BEFORE a trailing `[link] URL`; gold ANCHOR), reached because `blackAfter` sees only the
  text after the tag. `LinkVideoUrlOnly` applies the measurement's whole-paragraph `words 0` definition on both seams → the second probe = 19 / 9.
- **Regeneration:** scoped — the in-memory OFF/ON probe over ALL 416 modules: OFF = disk 2102/2102; ON = exactly 19 pages / 9 modules
  (`_r340_affected.txt`: ANZH303 ENFUN01 HIS1005 HIS1006 HIS1007 HIS1008 MXDI202 MXFL203 MXFU202); planner batches (3) all rc 0; 0 truly stale;
  manifest diff = exactly the 19 / 9; disk == probe ON on all 88 pages of the 9. Word-loss over the 19 (`_r340_wordloss.py`, OFF vs disk): 0
  non-video links lost, only the 27 dropped "go to video" labels. The PICK's other 3 modules are unreachable by these seams and recorded: EXBP901 /
  HIS1003 (the `[Link]` is bundled into an `[Interactive] Please embed / clip …` hand-off — a third emitter, 2 sites), XWHA02 ("Link to video" is an
  unrecognised bare red span, 1 site).
- **Gates:** skeleton 51.112 → 51.112 (−0.000pp at 3 dp; 5 moved — 2 up / 3 down, every mover in the affected set, pp-sum −0.64 (at 4 dp 51.1124 → 51.1120 = −0.0003pp, which is 0.000 at the 3-dp precision every round reports; NET OF THE TWO A1-NAMED PAGES BELOW +0.0006pp): HIS1008_7_0 +1.08 and HIS1008_1_0 +0.67 (the gold's own embeds, in the gold's positions); the 3 dips are NAMED — ANZH303_6_0 −1.41 and HIS1008_5_0 −0.40 = the gold's OWN embed of the SAME video wrapped in a widget the writer never tagged (ANZH303 a `div.tabs` around `Ez6uNsAONL0`; HIS1008-4.0 a `div.row.carousel` around `XBMfBVsymUo` + `TLberHUJgHY` under "[embed the following two videos with images and play buttons]" — the KB's 04A video-carousel doc says HOW to build one, not WHEN two videos become one; the gold's other multi-video sites (HIS1008-6.0, four embeds) are plain videoSections, so the carousel is the human's one-off) — the Decision-Framework A1 exception: the embed is judged right, its container is the human's widget substitution (decision 5's population); ENFUN01_0_0 −0.58 = the scorer's repeat-collapse artefact (a uniform `┌ 2× repeated` run of h5 / p / a > div.externalButton / table became a mixed run — +12 skeleton lines — while the new embed is the gold's own `us6ZcvCcYoo` at gold line 2563)); ≥50 1066; ≥75 201; ≥90 15; RAW 35.287 → 35.285; cs exact 11378 → 11379
  (+1) / EXTRA 171 / missing 593; every other gate line-for-line EXACT with r339 (full suite `_r340_gates.log`); the fast-loop's
  `--accept-named "skeleton SCAFFOLD"` used for the −0.0003pp (the r289 named-movement override, every mover decomposed — `_r340_dips.py`);
  accordion over the 9: 12 panels / 4 modules, every panel matches the human, defect 0; tabs 7 (exact 3, divergence 4 developer); flipCard over the 9 identical ON vs OFF (ENFUN01's defect 1 = the
  tracked baseline); 13 selftests GREEN. **55.8% of achievable.**
- **Verifier:** corpus-wide anchored buttons with a video href (`_r339_verify_videobtn.py`, the r339 standing verifier) **46 → 19**: the 27 url-only sites now embed (27 new `videoSection`s on the 19 changed pages, 17 phantom "[video] with no URL found" red flags gone); the 19 left are 15 LABELLED video buttons (real writer labels — kept by design: TWHK903's tutorials, MXDI202's titled links, OSBY201 …) + 4 url-only "Go to video" buttons on PROSE paragraphs (TEFUN07, HPRE203, XDLS908 — the fence's own exclusions, gold ANCHOR — and MXFU401's r339-named site); the word-loss check (`_r340_wordloss.py`, OFF pages vs the regenerated disk) over the 19: 0 non-video links lost, the only lost words the 27 dropped "go to video" labels.
- **Named:** the gold's widget substitutions around its OWN embed (ANZH303's tabs, HIS1008-4.0's carousel — decision 5's population; the KB's
  04A video-carousel doc is a HOW, not a WHEN, and the gold's other multi-video site HIS1008-6.0 is plain videoSections); the scorer's
  repeat-collapse artefact (ENFUN01_0_0); the 3 unreached PICK sites; the 15 labelled video buttons + 4 prose-fenced "Go to video" buttons
  (kept by design). Ship ledger: scoped #6 since the r334 full backstop (2 of headroom). **Plateau window: r338 +0.023 · r339 +0.010 · r340 −0.000
  — two consecutive under-0.02 rounds; a third ends the loop on the plateau rule.**

## Session 7 · Round 3 PICK (engine r340) — written before any code, 2026-09-16 01:25 NZST
- **The queue after r339 (the r336 substitution instrument re-run on the current corpus, `_r340_subst.log`, + two re-sizings):** nothing
  new reaches 20 derivable pages in the Standard / Inquiry rankings — the rows left are the declined / blocked / KB-correct classes
  (col widths c17/c56, `iframe.embed-responsive-item`, `videoSection.icon`, the heading ladder, `paddingR`, `p⇐h5`, `mathJax`,
  `table-bordered`, the `interactive` modifier, acks, the BLL footer, the super-content order); `div#body.container-fluid` (23 pages /
  9 modules) is the gold's own minority — 31 pages carry it against 2,347 bare `id="body"` (the BLL17x series), not a class;
  `div.row.supervisor ⇐ div.row` 16 pages / 15 modules and `div.alert.solid ⇐ div.alert` 19 pages / 9 modules sit under the floor
  (recorded). **c79 (KB queue rank 3) re-sized on the current corpus** (`_measure_r324_lessontitles.py` re-run → `_r340_lessontitles_now.
  json`/`.log`; the pair-count residue `_r340_paircount.py`): exact 567 / case-only 71 / punct 8; `claude = module title, gold = own` 44
  pages whose gold title is in the WT as `[H2]` 13, `[LESSON]` 6, `[PAGE]` 4, a plain line 10, NOT in the WT 10 — four small mechanisms,
  text-only (gate-neutral), none ≥ 20 pages; the pair-count residue (51 pages, all gold-more) is the gold's own second `<h1>` = "Lorem
  Ipsum" / "Maori title not provided" junk (23, ENGJ/MXDB), the module Te Reo repeated on lessons (12 — TRR203/301 MTK, ANZH401's three
  h1s), the module English (2), a lesson's own reo not in the WT (14) — not chased. c79 stays PARTIAL with the residue named.
- **Class: A STANDALONE `[link]`-FAMILY PARAGRAPH WHOSE TEXT IS NOTHING BUT A VIDEO URL IS THE EMBEDDED VIDEO** — the r339 verifier's
  residue class (46 video-href anchored buttons on the `[external link]` emitter). The writer types "[Link] https://www.youtube.com/
  watch?v=…" on its own line (often under "[embed video with image and play button]" or after "Watch the following video…"); today the
  r76 standalone rule ships `<a href target=_blank><div class="externalButton">Go to video</div></a>`, or the `[video]` element with no
  own url prints "[video] with no URL found" and the link becomes the button; the gold EMBEDS (videoSection + iframe). Authority: §1b
  level 4 — the KB is silent on the link form (01E `[video]` → videoSection is the nearest rule; r339's sibling); the gold's consensus
  decides.
- **Measured (`outputs/_measure_r340_linkvideo.cjs` → `_r340_linkvideo.json` / `.log`, the LIVE extractor over all 454 WTs; every
  external-link-family para block carrying a video-id url, paired to the gold by the id):** 71 blocks / 22 modules, gold EMBED 0.74 of
  found — but the shape decides: **url-only (0 visible words) 37 blocks / 13 modules, gold EMBED 26 / 29 found = 0.90** (Standard 0.89
  n=36 / Fundamentals 1.00 n=1; NCEA1 0.86 n=29 / Mathematics 1.00 n=4 / English, ANZH, EXPlore, Leaving-to-Learn 1.00 n=1 each; by
  context: after a media tag with no own url 0.94 n=24 (HIS1006 / HIS1008 / HIS1005 / HIS1007 / XWHA02), after a watch / play sentence
  0.75 n=9, neither 1.00 n=4); a link with ≥ 4 visible words 0.47 (the gold anchors the phrase inline — `[Link for video] Title` ×13 in
  one English module) → the titled form is NOT in the class. Gold BUTTON only 2 (HIS1005 / HIS1007 "If you want to learn more…" +
  `[Link]` — an optional extra), gold ANCHOR 1. **Fix population: 30 blocks / 12 modules** (HIS1006 13, HIS1008 6, HIS1005 2, +9 singles
  — ANZH303, ENFUN01, EXBP901, HIS1003, HIS1007, MXDI202, MXFL203, MXFU202, XWHA02); Claude today BUTTON 25 / ANCHOR 4 / OTHER 1.
- **Mechanism (two seams, one data block `elements.external_link_video_embed` `{ enabled, env "LINKVID_OFF", host_match (the r339
  video-id regex), media_follow }`):** (A) in the `[external link]` inline branch, before the r76 standalone-button rule: a url-only
  external-link item whose url is a VIDEO url → `MediaBuilder.media(it, …, "video", run)` (the standard `[video]` embed, host / icon
  / title-drop conventions included); (B) in `MediaBuilder.media`'s r247 following-link source: a `[video]` / `[embed]` element with no
  own url whose next unconsumed item is such a url-only external-link TAG item takes that url and consumes the item (the r247 rule
  extended from a black line to the tagged line) — so the media tag embeds and no phantom "no URL" note + button ships. Gate:
  skeleton-visible (`a > div.externalButton` → `div.videoSection > iframe`); est. +0.005pp over ~15 pages. Regeneration scope (§0b):
  the OFF/ON probe over all 416 modules gives the changed half; the working half (every `[external link]` with a non-video url, every
  `[video]` with its own url) proven byte-identical by the same probe. Scoped ship #6 since the r334 full backstop (2 of headroom).
- **Triangulation:** HIS1008 (WT `[link] https://www.youtube.com/watch?v=…` under `[embed video with image and play button]` → gold
  `<div class="videoSection icon ratio ratio-16x9"><iframe …>` → Claude a "[video] with no URL found" note + `externalButton` "Go to
  video"); HIS1005 lesson 2 (WT "Click on the play button to watch the short video below." + `[Link:] https://www.youtube.com/
  watch?v=NJ9LJfM4PjM` → gold embed → Claude `externalButton` "Go to video"); ENFUN01 (WT "Ricky Baker 'Happy Birthday song'…" +
  `[Link] https://www.youtube.com/watch?v=us6ZcvCcYoo` → gold embed → Claude `externalButton`).

## Session 7 · Round 2 (engine r339) — what shipped (a [button] whose destination is a video is the embedded video)
- **Fix:** `buttons.video_destination` {enabled, env VIDBTN_OFF, host_match, next_tag_families, play_label_match, label_max_words,
  exclude_released} → `ContentConverter.#videoDestination(url, it, bodyItems, i, key, tpl)` at the plain-[button] seam, right after the
  own-URL resolution: OWN (a VIDEO url — youtube watch / shorts / embed, youtu.be, vimeo id; never a channel — in the button's OWN text),
  NEXT-TAG (a `[video]`/`[audio]`-family tag with a video url follows), NEXT-TAG-URL (a non-structural tag whose text is only a video url
  follows — `[link] URL`), NEXT-URL (a bare video-url line follows). A play-like / absent label on NEXT-TAG renders nothing (the `[video]`
  item embeds itself); a real label ("Go to", "Learning journal") keeps the normal button. The other shapes → `MediaBuilder.media(…,
  "video")`, the gather fenced to the button + its url line; a label over 4 words renders as body text above the embed. The r88
  following-url absorb skips a video url while the rule is on.
- **Three refinements the probe forced (all fences, none a revert):** the OWN test (a shared-block link elsewhere in the paragraph turned
  SSOG301's quiz-control / journal buttons into duplicate embeds); a youtube CHANNEL url is not a video (XLP05 `[button] Link` became a
  generic iframe — `host_match` tightened to video-id urls); the media gather fenced (a following rnz article link was swallowed as
  "media residue" — content loss).
- **Regeneration:** scoped — the in-memory OFF/ON probe over ALL 416 modules: OFF = disk 2102/2102; ON = exactly 30 pages / 14 modules
  (`_r339_affected.txt`: ANZH404 HIS1001 HIS1002 HIS1005 HIS1006 HIS1007 HIS1008 HPFUN303 MXEO401 MXEX401 MXFU401 TWHA905 TWHK903
  XGF9006); planner batches (3) all rc 0; 0 truly stale; manifest diff = exactly the 30 / 14. Word-loss over the 30 (`_r339_wordloss.py`):
  0 non-video links lost, only the dropped play-button labels.
- **Gates:** skeleton 51.102 → 51.112 (+0.010pp; 21 moved — 16 up / 5 down, every mover in the affected set, pp-sum +20.26 (HIS1005_9_0 +5.73, HIS1005_5_0 +4.43, HIS1002_1_0 +3.12, HIS1007_4_1 +1.27 …; HIS1007_1_0 49.48 → 50.17 re-crosses ≥50 — the r338 named crosser HEALED, its `[video link]` buttons are now the gold's embeds); the 5 dips ≤ 0.85pp are NAMED: MXEX401_5_0 −0.85 and TWHA905_0_0 −0.26 = the gold's editorial video substitutions (the writer's youtube id is absent from the gold page — MXEX401 one of two, TWHA905 five of eight on its 16-embed single-file page), HIS1005_7_0 −0.33 / MXFU401_1_0 −0.27 / TWHK903_0_0 −0.02 = the scorer's alignment artefact on a strictly closer element sequence (every embedded id is the gold's own embed on the paired page)); ≥50 1065 → 1066; ≥75 201; ≥90 15; RAW 35.279 → 35.287; cs exact
  11375 → 11378 (+3) / EXTRA 171 / missing 593; every other gate line-for-line EXACT with r338 (fastloop PASS, nothing named; full suite
  `_r339_gates.log`); accordion verifier over the 14: 14 panels / 5 modules, every panel matches the human, defect 0; tabs 6/6 exact; flipCard over the 14 identical ON vs OFF (TWHK903's
  divergence 8 = the r282-named A1 module); 13 selftests GREEN. **55.8% of achievable.**
- **Verifier:** the PICK's 54 Claude BUTTON sites (of the 109 button-family video blocks) → 0 on the `[button]` emitter; 36 new `videoSection` embeds on the 30 changed pages; the word-loss check (`_r339_wordloss.py`) over the 30: 0 non-video links lost, the only lost words the dropped play-button labels ("go to video" ×23, "play" ×7, "recording" ×2 …). Corpus-wide, 46 anchored buttons with a video href remain (31 pages / 18 modules, `_r339_verify_videobtn.py`) — ALL on the `[external link]` / `[external link button]` emitters this class excludes by design (a standalone `[Link] URL` after a "watch the video" sentence — HIS1005_2_0, ENFUN01_0_0, ANZH303 `[Link please clip from 1:42-4:16]`; an embed instruction with no own URL followed by a `[link] URL` — HIS1006_10_0).
- **Named:** the gold's editorial video substitutions (MXEX401_5_0, TWHA905); the 8 gold BUTTON sites (TWHK903's tutorial links — real
  labels, kept); shape D (4 sites); the 46 video-href buttons on the `[external link]` / `[external link button]` emitters = THE NEXT
  CANDIDATE CLASS ("a standalone `[link]` to a video after a watch instruction is the embed"; HIS1006's `[embed …]` + `[link] URL` from
  the media side). Ship ledger: scoped #5 since the r334 full backstop (3 of headroom). **Plateau window: r338 +0.023 · r339 +0.010.**

## Session 7 · Round 2 PICK (engine r339) — written before any code, 2026-09-16 00:05 NZST
- **The queue after r338 (the r336 substitution ranking re-read + three new measurements):** the Standard rows left are all declined /
  blocked / KB-correct (col-12 wrappers, iframe class, paddingR, p⇐h5, mathJax, table-bordered, the heading ladder, acks). Checked and
  NOT chased this round: `div.super-content.row` order (the gold's own majority 387:108 — Claude is right); the BLL footer
  `inquiry-nav` (gold 42/48 BLL1 · 40/47 BLL2 — Claude's registry value is the family convention; the 12 plain-footer BLL golds are the
  minority); `videoSection.icon` (the KB 01E form is class-less; the r-old per-series icon list already follows the gold's group
  convention); the Inquiry `body.inquiry` token (22 single-file Inquiry modules whose crumb layout Claude never built — downstream of
  the crumb-less dialect rounds / the CED briefs, blocked; the token rides the build by the r-old `body_class_requires_build` rule).
  **DECLINED on measurement:** the activity `interactive` modifier (`_measure_r339_actinteractive.py` → `_r339_actinteractive.json` /
  `.log`: 4,213 paired boxes — gap 758 boxes / 455 pages / 238 modules, but the gold marks them because it BUILT a widget Claude cannot
  (D&D 212 / mcq 76 / typing 76 / dropQuiz 41 …); on Claude's side the boxes are plain text 0.26 or an `unclassified` hand-off 0.49 —
  no Claude-visible signature ≥ 0.60; decision 5's population).
- **Class: A `[button]` WHOSE DESTINATION IS A VIDEO IS THE EMBEDDED VIDEO, NOT A LINK BUTTON.** The writer's "[Button] Play video" +
  "[video link] URL", "[Button: youtube-url]", and the instruction brackets the normaliser reads as a button ("[embed video with image
  and play button]" + a bare URL line) all reach the page as an anchored button (the r88 following-URL absorb / the r326 anchor; since
  r338 an `externalButton` "Go to video"); the gold EMBEDS the video (`videoSection` + iframe) — HIS1007 lesson 1: three videos, the
  gold embeds all three, Claude embeds one and buttons two. Authority: §1b level 3/4 — the KB is silent on a button that names a video
  (01E's `[video]` → videoSection is the nearest rule; 05D's buttons are internal/external LINKS); the gold's consensus decides.
- **Measured (`outputs/_measure_r339_videobutton.cjs` → `_r339_videobutton.json` / `.log`, the LIVE extractor over all 454 WTs; every
  button-family block carrying a video-host URL — its own, or the next block's):** **109 blocks / 34 modules**; gold EMBED **0.90 of the
  found sites** (Standard 0.90 n=101 / Inquiry 0.75 n=4 / Fundamentals 1.00 n=4); by shape: A own-URL 21 (0.60), **B next-[video]-block
  52 (0.98)**, **C next-bare-URL 32 (0.96)**, D next-prose 4 (0.67 — not chased); by bracket: the instruction-like brackets 63 (0.96), a
  real `[button]` tag 46 (0.81); by label: no label 72 (0.95), "Play" / "Play video" 7 (1.00). Gold BUTTON only 8 (TWHK903's iOS /
  Android tutorial links, XDLS…). Claude today: BUTTON 51 / OTHER 13 / EMBED 33 (some already embed through the `[video]` path).
- **Mechanism:** in the `[button]` element branch (key === "button" only; `_r307Released` items excluded), after the own-URL resolution:
  (A) an own URL on a video host → `MediaBuilder.media(it, …, "video", run)` (the standard `[video]` embed — host / icon conventions
  included; the title-drop rule drops the short label); (B) the next unconsumed item is a `[video]`/`[audio]`-family TAG carrying a
  video-host URL → the button renders nothing and is NOT absorbed — the video item renders itself; (C) the next unconsumed item is a
  bare video-host URL line → `MediaBuilder.media` on the button item (the gather takes the URL line). A label longer than
  `label_max_words` (4) renders as body text before the embed (never silently stripped). Data `buttons.video_destination` `{ enabled, env
  "VIDBTN_OFF", host_match, next_tag_families, label_max_words, exclude_released }`. Gate: skeleton-visible (`a > div.button` → `div.
  videoSection > iframe`); est. +0.02–0.05pp over ~50 pages.
- **Regeneration scope (§0b, the `[button]` + `[video]` families):** the OFF/ON probe over all 416 modules gives the changed half; the
  working half (every `[video]` that already embeds, every `[button]` with a non-video URL) is proven byte-identical by the same probe.
  Scoped ship #5 since the r334 full backstop (3 of headroom).
- **Triangulation:** HIS1007 lesson 1 (WT `[Button] Play Video` + `[video link] https://www.youtube.com/watch?v=lmRkPXfmCx0` → gold
  `<div class="videoSection icon ratio ratio-16x9"><iframe … embed/lmRkPXfmCx0 …>` → Claude `<a href="https://www.youtube.com/
  watch?v=lmRkPXfmCx0" target="_blank"><div class="externalButton">Play Video</div></a>`); HIS1007 lesson 1 (`[Please embed this video
  with a play button and an image of the first scene]` + `[Video link] TED Ed video … https://www.youtube.com/watch?v=3NXC4Q_4JVg` →
  gold embed → Claude `externalButton` "Go to video"); TWHA905 (`[Button] Love Food Hate Waste` + youtube → gold embed → Claude button).

## Session 7 · Round 1 (engine r338) — what shipped (an external destination is the KB's externalButton)
- **Fix:** `buttons.external_destination` {enabled, env EXTDEST_OFF, form, internal_hosts, plain_form_match, default_label, video_label,
  video_host_match} → `ContentConverter.#externalDestination(url, key, form, tpl)` at the plain-[button] seam, after the URL / form /
  label resolution and before the r326 anchor wrap: an http(s) URL whose host is not Te Kura's own (drive / docs / forms.gle /
  desire2learn / sharepoint / vimeo player) on the plain `div.button` form → the KB external form `<a href target=_blank><div
  class="externalButton">`; a label that fell to `journal_label_default` → "Go to website" / "Go to video". Writer labels untouched.
- **Regeneration:** scoped — the in-memory OFF/ON probe over ALL 416 modules: OFF = disk 2102/2102; ON = exactly 134 pages / 71 modules
  (`_r338_affected.txt`; every changed line the class swap or class + default label, 0 other differences); planner batches (8) all rc 0;
  0 truly stale; manifest diff = exactly the 134 / 71.
- **Gates:** skeleton 51.079 → 51.102 (+0.023pp; 60 moved — 37 up / 23 down, every mover in the affected set, pp-sum +44.21 (XMES201_5_0 +18.96, XGF9003_1_4 +10.81 — crosses ≥75, AGH1004_2_0 +5.61, HES1007_9_0 +4.85 …); the 23 dips ≤ 5.17pp are NAMED and of two kinds: (a) the 11 gold `button`s on an external host — the KB-over-gold sites (ANZH404_4_0 −2.92 'Source A/B/C', MXFL401_5_0 −1.18, MXEO201_4_0/_8_0 −0.94/−2.00, ENGC202_5_0 −2.68), (b) the scorer's repeat-collapse / coincidental-match artefact (HIS1007_3_0 −5.17 and HIS1005_9_0 −1.56 each gain +4 gold-matched lines on the uncollapsed multiset — a uniform `┌ N× repeated` run of `a > div.button` became a mixed run; HIS1007_1_0 −1.37 crosses <50: its `[video link]`s ship as buttons the gold embeds, and their `div.button` lines had been matching the gold's journal `div.button`s by coincidence)); ≥50 1066 → 1065 (NAMED, accepted through the r289 override — the r326
  precedent); ≥75 200 → 201; ≥90 15; RAW 35.263 → 35.279; every other gate line-for-line EXACT with r337 (fastloop: every
  non-skeleton metric HELD; full suite `_r338_gates.log`); accordion verifier over the 71: 162 panels / 27 modules, every panel matches the human, defect 0; tabs 35 every built tab matches; flipCard
  over the 71 identical ON vs OFF (pre-existing baseline); 13 selftests GREEN (identical to r337's). **55.8% of achievable.**
- **Verifier:** external-host `div.button` 304 → 41 (the residue = the r73 modal document button + the widget builders' own forms, 18 pages / 13 modules — EXPFUN02/03's istock image modals), external-host `div.externalButton` 230 → 493, gold agreement on the found sites 0.950; the internal-host buttons untouched (docs.google 90 / sharepoint 73 / drive 31 / desire2learn 15 — 0 changed).
- **Named:** the 11 gold `button`s on external hosts (ANZH404 "Source A/B/C", MXFL401, XGF9006, BLL234, TWHK901, MXFU402, XMES103); the
  173 external-host buttons on no gold page (istock / EP / twinkl asset links); the 41-button residue on other emitters; the `[video link]`
  tag routed through the button branch (HIS1007 lesson 1 — the gold embeds the video; a video-tag round). Ship ledger: scoped #4 since
  the r334 full backstop (4 of headroom). **Plateau window restarts at r338 (+0.023pp).**

## Session 7 · Round 1 PICK (engine r338) — written before any code, 2026-09-15 23:45 NZST
- **The queue after r337 (re-measured with the LIVE extractor — `outputs/_measure_r338_standalone_links.cjs` → `_r338_standalone_links.json` /
  `.log`, all 454 gold modules, every `block.links` hyperlink classified by position; and the REVERSE `_measure_r338_gold_buttons.cjs` →
  `_r338_gold_buttons.json` / `.log`, every gold `externalButton` traced to its WT source).** The r337 note's "452 untagged hyperlink phrases
  the human buttoned" was a parsed-text artefact: the untagged STANDALONE hyperlink class is 486 phrase + 1,226 bare-URL paragraphs, and the
  gold buttons them at **0.067 / 0.072 of the found sites** (the rest are the writer's asset references — sharepoint / drive / istock / docs —
  that the gold ships as media, or inline `<a>`s); untagged INLINE 0.067 / 0.202. **DECLINED on measurement** (Declined classes). The reverse
  trace: 873 gold externalButtons on 440 pages / 198 modules → HREF-sourced 526, text-only 140, NO source 207 (class C); the largest
  HREF-sourced signature is the writer's `[button]`-family tag WITH a URL, which Claude already anchors (r326) — as `div.button`.
- **Class (the one that solidifies): AN EXTERNAL DESTINATION IS THE KB'S `externalButton` — KB 05D "Buttons": Internal → `<a href
  target=_blank><div class="button">`, External → `<div class="externalButton">`; plus constraint 75's default label ("a bare URL with no
  accompanying words → Go to website").** Authority: §1b level 1 (the KB rule); the gold confirms it by HOST — gold anchored buttons by host
  (`_r338_extbutton_class.log`): relative paths / `#` / drive.google.com 586:1 / docs.google.com 92:6 / desire2learn 17:8 / player.vimeo 6:0 are
  `button`; youtube 1:24, youtu.be 2:14, earth.google 0:16, sparklers 1:15, teara 3:11, nzhistory 0:11, natlib 0:8 … every outside website is
  `externalButton`. Claude ships `div.button` for every `[button]` regardless of destination, and labels a URL-only `[Button: https://…]` with
  the JOURNAL default ("Go to your journal" ×52 on external sites — TWHA905 → gold "Go to Kiwiharvest", ENFUN02 → "Thoughtful Learning").
- **Measured (`outputs/_measure_r338_extbutton_class.py` → `_r338_extbutton_class.json` / `.log`, every anchored Claude button with an
  http(s) href, host-classified, paired to the gold by href then label): the class = external-host buttons Claude ships as `button` —
  304 buttons / 147 pages / 80 modules.** Gold for the same button: `externalButton` **120** / `button` 11 / not on any gold page 173 (the
  writer's istock / EP / twinkl asset links the gold never buttons) → **0.916 of found**. Per template: Standard 0.913 (126 pages), Inquiry
  0.909 (13), Fundamentals 1.000 (8). Per subject family ≥ 6 found: NCEA1 1.000, Leaving to Learn 0.964, 1-10 English 1.000, ConnectED 1.000,
  1-10 Social Science 1.000, Te ara Whakapuawa 0.833, 1-10 Mathematics 0.667; ANZH 0.400 (5 found — under any floor; its 3 `button`s are
  the human's "Source A/B/C" evidence buttons). The converse (internal hosts the rule must leave alone): docs.google 0/15 ext, sharepoint
  1:1, desire2learn 1:4, drive 1:0 (n=1) — the internal list holds. Label sub-class: 60 `journal_label_default` labels on external
  URLs ("Go to your journal") → the KB's "Go to website" / "Go to video" (constraint 75; the gold's own labels are the resource names —
  editorial, never matched either way, text-only).
- **Mechanism:** in the `[button]` element branch (ContentConverter), after the URL / form / label resolution and before the r326 anchor
  wrap: when the button carries an http(s) URL whose host is not in the data list of INTERNAL hosts (`buttons.external_destination
  .internal_hosts`: drive.google.com, docs.google.com, forms.gle, desire2learn.com, sharepoint (mytekuraschool*), vimeo player) and the
  resolved form is the plain `div.button` (never buttonD / downloadButton / the reveal JS buttons), the form becomes the KB external form
  `<a href="{url}" target="_blank"><div class="externalButton">{label}</div></a>`; a label that fell to `journal_label_default` becomes
  `default_label` "Go to website" (`video_label` "Go to video" for a video host). Data `buttons.external_destination` `{ enabled, env
  "EXTDEST_OFF", internal_hosts, form, default_label, video_label, video_host_match }`. Gate: skeleton-visible (`div.button` →
  `div.externalButton` on ~120 gold-matched sites; the 11 gold-`button` sites dip, NAMED); every other gate expected EXACT.
- **Regeneration scope (§0b, the `[button]` tag family):** every module whose output changes (the OFF/ON probe) ∪ the whole `[button]`
  family is the corpus (r323 precedent: 713 pages / 286 modules carry a button) — the change is keyed on the URL host inside ONE branch, so
  the affected set IS the family's changed half; the working half (internal / no URL) is proven byte-identical by the OFF/ON probe over all
  416 modules (the r337 pattern), then the scoped ship rebuilds the affected set. Scoped ship #4 since the r334 full backstop.
- **Triangulation:** TWHA905 (WT p.? `[Button: https://www.kiwiharvest.org.nz/ ]` → gold `<a href="https://www.kiwiharvest.org.nz/"
  target="_blank"><div class="externalButton">Go to Kiwiharvest</div></a>` → Claude `<a …><div class="button">Go to your journal</div></a>`);
  AGH1007 lesson 4 (`[Button – External Link] https://www.lumendigital.co.nz/staging/TheAmazingCow/` → gold `externalButton` "The Amazing
  Cow…" → Claude `div.button` "Go to your journal"); ENFUN02 (a link table cell "Thoughtful Learning / https://k12.thoughtfullearning.com…"
  → gold `externalButton` "Thoughtful Learning" → Claude `div.button` "Go to your journal").

## Session 6 · Round 3 (engine r337) — what shipped (numbered steps are a semantic <ol>, never <p>1. …</p>)
- **Fix:** `body_region.typed_number_list` {enabled, env TYPEDOL_OFF, lead_pattern, min_run 2, sequential, marker_form_all_equal,
  start_attr, verbatim_widget_classes} → `ListsAndRuns.TypedNumberList(html)`, a full-page post-pass at the r234 EmojiStrip seam
  (PageAssembler, body only): a run of ≥ 2 consecutive bare `<p>`s opening with sequential numbers or the extractor's all-"1."
  Word-list marker → one `<ol>` (`start="n"` when n > 1), the number stripped from the first text node (an emptied `<b>` dropped);
  verbatim zones = EmojiStrip's + the built widgets that own their inner shape. Unit probe 20/20.
- **Regeneration:** scoped — the in-memory OFF/ON probe over ALL 416 modules: OFF = disk 2102/2102; ON = exactly 24 pages / 24 modules
  (`_r337_affected.txt`); planner batches all rc 0; 0 truly stale; manifest diff = exactly the 24.
- **Gates:** skeleton 51.078 → 51.079 (+0.001pp; 3 moved — 2 up / 1 down, every mover in the affected set, pp-sum +1.89 (XLP05_5_0 +2.01, MXFU402_3_0 +0.09; PES1001_5_0 −0.21 NAMED = its new <li>s keep the writer's bold lead the gold strips inside the list, the r164/r165 bold class — the <ol> itself now matches); the other 21 changed pages sit inside collapsed accordion widget markers and cannot move the scaffold); ≥50 1066 → 1066; ≥75 200 → 200; ≥90 15; every other gate
  line-for-line EXACT with r336 (fastloop PASS; full suite `_r337_gates.log`); accordion verifier over the 24: 166 panels / 22 modules, every panel matches the human, defect 0; 13 selftests GREEN.
  **55.8% of achievable.** A small ship under the 20-page floor (14 pages by the strict census, 24 by the shipped rule) — the r320 precedent.
- **Named:** CEDW501's quiz-as-list (the gold builds an MCQ — a nested-quiz follow-up); c41's untagged captions (editorial, "line after
  an image" is a caption at ~0.00); c75's 452 untagged hyperlink buttons (255 pages — needs the live extractor's link channel to measure;
  the next session's first PICK). Ship ledger: scoped #3 since the r334 full backstop.
  **Plateau window: r335 +0.018 · r336 +0.000 · r337 +0.001 — three consecutive shipped rounds under 0.02pp with no other protected
  gate moved → THE LOOP STOPPED after this round (§4 plateau).**

## Session 6 · Round 3 PICK (engine r337) — written 2026-09-15 22:20 NZST (the measurement first, the code alongside it)
- **Queue after r336:** the post-r335 substitution ranking has no derivable structural class ≥ 20 pages left (every Standard row is
  declined / blocked / named; Fundamentals' chip shipped as r336). The KB §A rows still carrying a gap: **c42** (numbered steps = `<ol>`,
  typed `<p>1.` numbering on 28 Claude pages), c41 (captions — Claude 38 pages vs gold 155), c75 (external-link buttons — Claude 117 vs
  gold 417 pages). c42 is a numbered Universal constraint with an exact mechanism; picked first.
- **Class:** KB constraint 42 (Universal): numbered instructions / steps / sub-questions are semantic `<ol><li>` (`start="N"` for a
  continuation), NEVER `<p>1. …</p>`. Claude ships numbered paragraphs in TWO forms: the writer's typed sequence (`1. 2. 3.`) and the
  extractor's Word-numbered-list marker — `DocxExtractor` prefixes EVERY numbered-list paragraph with `1. ` and never counts, so a Word
  list inside a built widget panel ships `<p>1. …</p><p>1. …</p>` (every question numbered 1 — BLL213/214/235/236/237/263). The free-body
  path (`ListsAndRuns.renderBlackText`) already turns both forms into `<ol>`; the widget panels render lines as `<p>` and never see it.
  **Measured on the engine's own adjacency rule (`_measure_r337_numruns.py`): 16 runs on 14 pages / 14 modules, all inside accordion
  panels** (11 marker runs + 5 typed). The wider typed-number census (`_measure_r337_typednum.py`, 218 paragraphs / 34 pages) counts
  single numbered `<p>`s in separate containers too (flipCard faces, D&D questions, captions — not lists; the gold keeps a flipCard's
  `1.` as the card title, a D&D question as a plain `<p>`); where the gold holds the run text it is `<ol>` 111 / `<ul>` 30 / `<p>` 30.
- **Triangulated:** BLL213 lesson 2 — docx `w:numPr` list "Why did Spotty…" → gold `<ol><li>Why did Spotty…</li>…` in the accordion panel →
  Claude `<p>1. Why did Spotty…</p><p>1. How was Sant…</p>` (every item "1."). BLL212 lesson 2 — typed `1. What happened…` → gold `<ol>` →
  Claude `<p>1. …</p><p>2. …</p>`. SCCH301 lesson 1 — the syringe steps, the same.
- **Authority (§1b):** level 1 — constraint 42 is a numbered Universal constraint; the gold agrees (`<ol>` 0.63 / a list 0.81).
- **Fix:** `body_region.typed_number_list` {enabled, env `TYPEDOL_OFF`, lead_pattern, min_run 2, sequential, marker_form_all_equal,
  start_attr, verbatim_widget_classes} → `ListsAndRuns.TypedNumberList(html)`, a full-page post-pass at the r234 EmojiStrip seam
  (PageAssembler, after the emoji list clause, before LinkTextDisplay, body only): a run of ≥ 2 consecutive bare `<p>`s whose text
  opens with sequential numbers or the all-`1.` marker → one `<ol>` (`start="n"` when n > 1), the number removed from the first text
  node; verbatim zones = EmojiStrip's (cv2 boxes, notes, script/style) + the built widgets that own their inner shape (flipCard,
  dragAndDrop, clickDrop, dropQuiz, mcq, speechBubble, carousel, tabs, hintSlider, TKmodal, selfCheck, memoryGame, rotateBanner).
  Unit probe `_r337_unit.cjs` 17/17. **Under the 20-page floor — shipped small on the r320 precedent** (built, proven, KB-right, and
  the marker form is a visible defect).
- **Gate expectation:** gate-neutral by construction (the accordion panel is inside a widget marker the skeleton collapses; cs / body
  exclude widget subtrees; the accordion verifier strips tags and word-overlaps) — every gate EXACT; the accordion verifier over the
  affected modules must stay defect 0. **Plateau window: r335 +0.018 · r336 +0.000 · r337 (expected 0.000) → the plateau rule fires
  after this round unless the queue yields a gate-moving class.**

## Session 6 · Round 2 (engine r336) — what shipped (the Fundamentals overview chip is a family convention)
- **Fix (DATA only, no toggle):** five `Style_Anchor_Registry.json` `module_code` rows — ARFUN / ENFUN / TEFUN base_rules `{overview: absent,
  lesson: absent}` (new rows; the chip had resolved from the `defaults` tier), MXFUN0 delta overview `absent` (was the mis-mined
  `free-text:"MXFUN01"`), SSFUN base_rules overview `full-code` (was the em-dash no-evidence marker → element omitted); a `_note` on each.
  The reversal is the committed pre-round registry; the blast radius is the resolved-rules diff over all 416 modules (`_r336_resolve_all.cjs`).
- **Regeneration:** scoped — exactly the 31 modules whose resolved `module_code` changed (the five bases' every member with a Claude dir);
  4 planner batches all rc 0; 0 truly stale; manifest diff = exactly 31 pages / 31 modules, 0 added/removed.
- **Gates:** skeleton 51.078 → 51.078 (+0.000pp; 31 moved — 9 up / 22 down, every mover in the affected set, pp-sum +0.62; the 22 dips ≤ 0.32pp NAMED = the scorer's alignment artefact: the phantom chip's `h1` line had been coincidentally matching the gold's second (Te Reo) `h1`, which Claude never ships — the element sequence is now the gold's; SSFUN07_0_0 +2.52 the largest gain); ≥50 1066 → 1066; ≥75 200 → 200; ≥90 15; every other gate
  line-for-line EXACT with r335 (fastloop PASS; full suite `_r336_gates.log`); 13 selftests GREEN. **55.8% of achievable.**
- **Verifier:** Fundamentals overview chips = the gold's family form on 30 of 31 (SSFUN07's gold chip is a lesson number — named).
  Ship ledger: scoped #2 since the r334 full-ship backstop. **Plateau window: r334 +0.167 · r335 +0.018 · r336 +0.000.**

## Session 6 · Round 2 PICK (engine r336) — written before any code, 2026-09-15 21:50 NZST
- **Queue re-run after r335:** `_measure_r336_subst.py` → `_r336_subst.json` (the r334 substitution instrument) + the two probes above.
  Standard's top rows are all settled: the widened wrapper (DECLINED c17/c56), `iframe.embed-responsive-item` (KB-correct), `videoSection
  icon` (r200's solidified groups shipped; the rest are r182 near-ties, the KB never names `icon`), `col-md-10` (the KB forbids it),
  `paddingR` (gold 0.22 even in paired rows — a padding choice, declined inline), `p ⇐ h5` (25 text-matched cases / 17 pages — editorial),
  `body.mathJax` (the equations BLOCKED class), `h4/h3 ⇐ h5` (the outside-box heading LADDER — per-MODULE, declined above). Inquiry:
  the acks override (r317, never chase) + the `inquiry` body token (the engine ships it only where the panels build, as the gold does —
  the crumb-less dialect rounds). **Fundamentals: `┌ 2× repeated ⇐ div#module-code` 22 occ / 22 pages / 22 modules — the header CHIP.**
- **Class:** the Fundamentals overview `#module-code` chip is a per-FAMILY convention the registry has no evidence for. Gold header census
  (`_measure_r336_funchip.py`): **ARFUN 54/54 pages no chip, ENFUN 8/8 no chip, TEFUN 8/8 no chip** — Claude ships the chip on all 21
  (the registry rows for those bases carry no `module_code`, so the `defaults` `full-code` applies); **SSFUN 5/6 chip (full code)** —
  Claude ships NO chip on its 6 (the SSFUN base row's overview value is the em-dash no-evidence marker → element omitted). HPFUN (13/15
  chip), CHFUN (5/5), MXFUN (8/11), XFUN (6/7) already match. **27 overview pages / 27 modules.** The second h1 (the ENFUN/TEFUN Te Reo
  title) is NOT in those Writers Templates — editorial, declined; SSFUN's Te Reo title is in the WT and already ships (r177).
- **Triangulated:** ARFUN02 — WT `[Title] Colour and shape`; gold header `<h1><span>Colour and shape</span></h1>` (no chip); Claude
  `<div id="module-code"><h1>ARFUN02</h1></div>` + the h1. ENFUN02 — the same shape (gold: two h1 spans, no chip; Claude: chip + one
  h1). SSFUN05 — gold `<div id="module-code"><h1>SSFUN05</h1></div>` + two h1 spans; Claude: no chip + two h1 spans.
- **Authority (§1b):** level 2/4 — the family's own siblings are unanimous (ARFUN 1.00 / ENFUN 1.00 / TEFUN 1.00 / SSFUN 0.83, all ≥ 0.60);
  KB 06 §3.3 (Fundamentals) is silent on the chip (§3.1 describes it for Standard only). The registry is the sanctioned carrier of a
  family convention (`Style_Anchor_Registry.json`; the r263 / r285 / r332 registry-correction precedent).
- **Fix (planned, DATA only):** `Style_Anchor_Registry.json` base_rules `module_code` for ARFUN / ENFUN / TEFUN → `{"overview": "absent",
  "lesson": "absent"}` (ARFUN04's lesson-like files are chip-less in the gold too) and SSFUN → `{"overview": "full-code", "lesson":
  free-text as mined}`; no engine change, no toggle (a registry correction — the reversal is the committed pre-round registry, and the
  in-memory before/after probe proves the blast radius). Regeneration: scoped to the 27 modules (the affected set = every module whose
  resolved `module_code` changes, derived by resolving ALL 416 codes before and after — the r175 complete-detector rule).
- **Gate expectation:** skeleton ≥ hold (each of the 27 overview pages loses or gains the `div#module-code` + `h1` header lines exactly
  as the gold has them; est. +0.02–0.04pp); every other gate EXACT (the header is outside cs / body / defect). **Plateau window:
  r334 +0.167 · r335 +0.018 · r336 ?**

## Session 6 · Round 1 = Session 5 · Round 6 (engine r335) — what shipped (the [Engagement quiz button] is the KB's external quiz link button)
- **Fix (built in session 5, flipped ON here):** `buttons["engagement quiz button"].kb_form` {enabled, env ENGQUIZ_OFF, form `<a href="{href}"
  target="_blank"><div class="button">{label}</div></a>`, href "#", label "Go to quiz", todo_note} at the ContentConverter button seam right
  after the r329 marker test: an `engagement quiz button` item ships the KB form + ONE Designer/Developer To Do note (cv2-note) carrying the
  writer's link and any tail words; the legacy `engagementTrigger` div is the OFF form.
- **Regeneration:** scoped — session 5's in-memory probe over ALL 416 modules: OFF = disk 2102/2102; ON = exactly 28 pages / 28 modules, every
  diff line the one button swap. Session 6: the 5 batches (`_r335_batches_run.sh`) all rc 0; `_content_manifest.py fresh` → 0 truly stale;
  `diff` = exactly the 28, 0 added/removed. Gotcha: `_r335_affected.txt` was CRLF (written on Windows) — `xargs` fed `_fastloop_diff.py`
  codes ending in `\r` and every guard fired; converted to LF, re-run clean.
- **Gates:** skeleton 51.060 → 51.078 (+0.018pp; 28 moved — 19 up / 9 down, every mover in the affected set, pp-sum +35.31; the 9 dips ≤ 0.33pp NAMED = the scorer's alignment artefact on pages whose gold box has no inner row > col-12 (OSBY501_5, OSSC501_5, OSSC301_3, OSAI201_3, OSOH501_5, OSSC401_4, ARFUN01_0, HPFUN401_0, ARFUN02_0 — the element sequence h3 → p → a → div.button is now the gold's)); ≥50 1066 → 1066; ≥75 200; ≥90 15; every other gate line-for-line
  EXACT with r334 (fastloop PASS, nothing to name; full suite `_r335_gates_s6.log`); 13 selftests GREEN. **55.8% of achievable.**
- **Verifier:** `button engagementTrigger` divs 28 → 0; anchored `Go to quiz` at the engagement sites 0 → 28 (+28 notes, 1:1).
  Ship ledger: scoped #1 since the r334 full-ship backstop. **Plateau window: r333 +0.066 · r334 +0.167 · r335 +0.018.**

## Session 5 · Round 6 PICK (engine r335) — written before any code, 2026-09-15 19:35 NZST — WITH THE FULL-SHIP BACKSTOP
- **Backstop first:** the ship ledger reached 8 scoped ships after r334, so this round opens with the full `ship.sh` regeneration of all 416
  gated dirs (no code change in between): `_stalecheck.sh` 0 stale, `_content_manifest.py diff` must be IDENTICAL (the proof that eight
  scoped ships left nothing under-scoped), then the fast-loop snapshot + manifest + `record-full`. The class below ships on top of it as a
  scoped regeneration (a full-ship round resets the counter to 0, then this round's scoped ship is #1).
- **Class:** the writer's **`[Engagement quiz button]`** (OS family + ARFUN01/02 + HPFUN401: `[Engagement quiz button] <sharepoint quiz doc URL>`)
  ships as `<div class="button engagementTrigger">…</div>` — a bare div, no anchor, and the label falls to the JOURNAL default (`Go to your
  journal` on 13 of 28; the quiz DOCUMENT'S FILENAME on the rest — `Online Safety Scams OSSC301 Quiz - Copy`, `Writers Template -OSAH501 …docx`;
  one carries a stray writer note). **28 pages / 28 modules, 28 buttons.** KB 01F `engagement_quiz_button` → "External quiz link button" (the
  `button` form `<a href target="_blank"><div class="button">`); constraint 65 / CL-0038 (r232) fixed the quiz button's label `Go to quiz` and
  its blank publish-time href. The gold: `engagementTrigger` **0** of 2,385 pages; at these sites `<a href="/d2l/…quickLink…type=quiz…"
  target="_blank"><div class="button">Go to quiz</div></a>` — **25 in the OS golds, ARFUN01 4, HPFUN401 1** (the D2L rcode is publish-time
  wiring, the r232 / CL-0044 class).
- **Triangulated:** OSAI301 lesson 3 — WT `[Engagement quiz button] https://mytekuraschool.sharepoint.com/…`; gold `<a href="/d2l/common/
  dialogs/quickLink/quickLink.d2l?ou={orgUnitId}&type=quiz&rcode=TCS_Dev-74927" target="_blank"><div class="button">Go to quiz</div></a>`;
  Claude `<div class="button engagementTrigger">Go to your journal</div>` (the sharepoint link lost). OSGM301 the same.
- **Authority (§1b):** level 1 (KB 01F button form + constraint 65's label) + the gold 30/30 at the paired sites.
- **Fix (planned), data `buttons["engagement quiz button"].kb_form` {enabled, env `ENGQUIZ_OFF`, form `<a href="{href}" target="_blank"><div
  class="button">{label}</div></a>`, href "#", label "Go to quiz", todo_note "Wire this engagement quiz's D2L quicklink (the href is
  intentionally blank). Writer's quiz source: {url}{text}"}:** at the button seam, right after the r329 marker test, an `engagement quiz
  button` item ships the KB form with the canonical label and ONE Designer/Developer To Do note (cv2-note, gate-neutral) carrying the
  writer's link + any other words; the legacy `engagementTrigger` div is the OFF form. Regeneration: scoped to the 28 modules the probe names.
- **Gate expectation:** skeleton ≥ hold (+28 `a` lines and 28 `div.button` class lines matching the gold; est. +0.01pp — under 0.02 but the
  round is not a plateau step on its own: r333 +0.066 · r334 +0.167); every other gate EXACT. **Plateau window: r333 +0.066 · r334 +0.167.**

## Session 5 · Round 5 (engine r334) — what shipped (the activity box's title heading is h3)
- **Fix:** `activity_wrapper.title_heading_level` {enabled, env ACTTITLEH3_OFF, level 3, exclude_body_class_match reoTranslate, skip_panel_class
  "super-content row"} → `ActivitiesBuilder.activityTitleLevelPostpass(html, run)` in the body chain right after `#relevelHeadings`: every
  activity box's first-child heading (after an optional super-content panel, balanced) is rewritten to h3; nothing else in the box moves;
  the reoTranslate family excluded (PNR keeps h2 by name, r331).
- **Regeneration:** scoped — the in-memory probe over ALL 416 modules (4 shards): OFF = disk 2102/2102; ON named 226 pages / 73 modules and
  every diff line is a heading tag swap (465 h4 + 125 h5 → 590 h3, the 125 including the 115 XDLS tile panels the census only saw once the r307
  class prefix was accounted for); the planner's 9 batches, all rc 0; 0 truly stale; manifest diff = exactly the 226.
- **Gates:** skeleton 50.893 → 51.060 (+0.167pp; 170 moved, 150 up / 20 down — dips NAMED: MXFU401_3_0 −8.4 / PHE1003_1_0 −4.6 / MXEO202_6_0 −4.6 /
  MXEO202_3_0 −3.3 / HIS1007_3_1 −3.2 / TEFUN08_0_0 −2.9 = alignment artefacts with the position-free overlap rising or flat; ANZH301_9_0 −3.5 +
  ANZH304_6_0 −3.4 = one box each whose gold title is not h3, the gold's 12-of-4560 minority); ≥50 1049 → 1066; ≥75 200; every other gate
  line-for-line EXACT with r333 (fastloop PASS, nothing to name); 13 selftests GREEN. **55.7% of achievable.**
- **Verifier:** activity title slots h4/h5 590 → 0 (h3 4013, h2 14 = the PNR exclusion). **Plateau window: r332 +0.269 · r333 +0.066 · r334 +0.167.**
  Ship ledger: scoped #8 since the r326 full — **the full-ship backstop is DUE: the next shipped round runs `ship.sh` (full regeneration).**

## Session 5 · Round 5 PICK (engine r334) — written before any code, 2026-09-15 18:40 NZST
- **Class:** the ACTIVITY BOX'S TITLE HEADING LEVEL. KB 01F `activity_heading` → `<h3>Activity heading text</h3>` within the activity;
  the gold, wherever a box's first child is a heading, ships h3 on **4548 : 12** Standard (0.997), **1029 : 5** Inquiry (0.995), **581 : 0**
  Fundamentals (1.000), 196 : 4 Bilingual. Claude ships the box's title at **h4 on 456 boxes (+ h5 10) — 202 pages / 69 modules** (Standard 346
  boxes / 174 pages / 48 modules — MXFL203 59, HIS1005 37, HIS1004/1006 33 …; Fundamentals 109 / 23 / 16; Inquiry 11 / 5 / 5), because a
  writer's `[H3]` typed after the `[Activity]` opener takes the body shift (+1 → h4, `[H4]` → h5) and `#relevelHeadings` SKIPS activity
  subtrees (the r55 anchor exclusion), so the in-box title never normalises back; the r66 first-line title and the opener's embedded
  payload already ship at the fixed h3 (2283 boxes). (`outputs/_measure_r334_acttitle.py` → `_r334_acttitle.json`.)
- **Triangulated:** MXFL203 lesson 1 activity 1E — WT `[Activity 1E]` then `[H3] New Zealand's biggest A&P show`; gold `<div class="activity"
  number="1E"><div class="row"><div class="col-12"><h3>New Zealand's biggest A&P show</h3>`; Claude the same box with `<h4>`. HIS1005 lesson 2:
  the same shape. The Bilingual family's 14 h2 titles are the PNR boxes the r331 rule excluded by name (PNR's gold keeps h2 — 0.72) and stay
  out of this rule (`exclude_body_class_match: reoTranslate`).
- **How this PICK was found:** the new substitution instrument `outputs/_measure_r334_subst.py` (`_r334_subst.json`) — the gate's own
  `replace` opcodes read line-for-line as "gold ships X where Claude ships Y": Standard `h3 ⇐ h4` 209 occ / 142 pages / 66 modules was the
  largest heading swap; the activity-title census decomposed it. Set aside on the record from the same instrument: `div.col-12 ⇐
  div.col-md-8.col-12` 254 / 220 pages (the KB c17/c56 widened activity wrapper — the gold keeps `col-md-8` as the majority for EVERY widget
  type, D&D column 0.51 / 0.49 widened, and the layout is the developer's choice, not in the tag → DECLINED); `iframe.embed-responsive-item ⇐
  iframe` 130 / 121 (the KB's iframe forms carry no class → Claude is KB-correct); `videoSection.icon` 103 / 90 (the r200/r331 set-aside);
  `body.container-fluid.mathJax` 71 / 17 modules (a page-level class the KB is silent on — measure another round); the 36 Inquiry modules
  whose gold ships `div.crumbs`+`div.inquiryPanel` but Claude does not (KB 06 §3.4) decompose into six delimiter dialects, and the largest
  reachable one (8 CED modules with ALL-CAPS Wonder/Explore/Connect/Act/Reflect lines) turned out to be REVISION BRIEFS whose docx carries the
  edit notes before an unfilled blank template — the live extractor starts at the template's `[TITLE BAR]` and ships the placeholders; a
  content-start question, not a panel round (recorded under Declined/Blocked below).
- **Authority (§1b):** level 1 (KB 01F `activity_heading`) + the gold at 0.997 / 0.995 / 1.000 — no override needed.
- **Fix (planned), data `activity_wrapper.title_heading_level` {enabled, env `ACTTITLEH3_OFF`, level 3, exclude_body_class_match
  "reoTranslate"}:** `ActivitiesBuilder.activityTitleLevelPostpass(html, run)`, run in the body chain right after `#relevelHeadings`: for
  every activity box open, skip an optional `super-content row` panel (balanced), then if the box's own `row > col-12` opens with a heading,
  that heading's open + close tags are rewritten to h3. Nothing else in the box moves. OFF = byte-identical. Regeneration: scoped to the
  modules the in-memory probe names over all 416.
- **Gate expectation:** skeleton ≥ hold — 466 title lines gain the gold's `h3` (est. +0.05–0.10pp; ≥50 +); compare_structure / body /
  defect / leak EXACT (a heading level never enters the wrapper chain). **Plateau window: r331 +0.022 · r332 +0.269 · r333 +0.066.**

## Session 5 · Round 4 (engine r333) — what shipped (a right-hand alert is a side column; `rhs` / `summary` are not classes)
- **Fix:** `callouts.positional_side_alert` {enabled, env ALERTRHS_OFF, tags [alert, important], keywords [rhs, rhc], strip_tokens
  {rhs, rhc, summary}, after_activity (the KB activity sidebar `col-md-4 offset-md-0 col-12 > alertActivity`, lead h4), after_content
  (`col-md-4 col-12 > alert top`, lead h4)}: at the callout emit site a strict-mode `alert`/`important` carrying a keyword, with the preceding
  content row just closed, is spliced as that row's right sibling through the r123 pairing (`#sideAlertCol`, which now honours a def's
  lead through the r61 module convention); an empty box keeps the ordinary path and its "Empty" flag; with no preceding row or in span
  mode the plain box ships with the token stripped; `summary` is stripped everywhere. `emit` records `lastRowOpenIdx` so the closed row's
  first block (activity vs content) decides the def.
- **Regeneration:** scoped — the in-memory probe over ALL 416 modules (4 shards): OFF = disk 2102/2102; ON named 143 pages / 53 modules;
  every diff line = 150 rhs opens + 98 summary opens gone, 92 side columns (61 alert top / 31 alertActivity) + 106 plain alerts gained,
  content lines balancing exactly (0 lost / 0 gained); the planner's 7 batches, all rc 0; 0 truly stale; manifest diff = exactly the 143.
  The first cut lost 10 "Empty [alert]" flags and rendered the lead as a fixed h4 — both fixed before the regeneration (`_r333_probe_on1_*`).
- **Gates:** skeleton 50.827 → 50.893 (+0.066pp; 87 moved, 73 up / 14 down — dips NAMED: TEFUN05_0_0 −4.9 / TEFUN04_0_0 −3.2 / ANZH304_6_0
  −3.4 / ANZH303_6_0 −2.8 = alignment artefacts with the position-free overlap rising; MXFL301_1_0 −2.9 + MXEX302_6_0 −1.5 = the
  after-content rule's gold-plain-alert / gold-alertActivity minorities; ENGI102_6_0 −1.1 a coincidental match); ≥50 1044 → 1049; ≥75 200;
  compare_structure exact 11360 → 11375 / EXTRA 186 → 171 / missing 591 → 593 (ACCEPTED BY NAME: ANZH301_3_0 + HIS1004_2_0, the
  after-activity rule's 2-of-20 minority where the gold keeps a full-width `alert`); every other gate EXACT; 13 selftests GREEN.
  **55.6% of achievable.**
- **Verifier:** `alert rhs` 150 → 0; `alert summary` 98 → 0; 92 side columns. **Plateau window: r331 +0.022 · r332 +0.269 · r333 +0.066.**
  Ship ledger: scoped #7 since the r326 full — **the full-ship backstop is due at the next scoped ship (8).**

## Session 5 · Round 4 PICK (engine r333) — written before any code, 2026-09-15 17:58 NZST
- **Class:** two alert modifier tokens the writer's positional/label words map to that the gold NEVER ships and the KB does not define
  (`Emit_Templates.callouts.modifier_classes` rhs/rhc → ` rhs`, summary → ` summary`): **`alert rhs` 135 occ / 94 pages / 48 modules** (writer
  `[alert box rhs]` / `[alert box rhc]` / `[rhs alert]` / `[alert rhs]` / `[important info box rhs]` / `[alert.rhs]`) and **`alert summary` /
  `alert solid summary` 63 occ / 62 pages / 11 modules** (`[alert box lesson summary]`, `[alert box – summary statement]`, `[alert box module
  summary]`; AGH/ANZH). KB 05B's alert vocabulary is `alert` / `alert solid` / `alert top` / `alert blank` / `alert teacher` (+ cultural); its
  sidebar form (01F "Activity sidebar", 05B) is `col-md-4 offset-md-0 col-12 > div.alertActivity > h4 + p`; `alert top` = `<div class="alert
  top"><h4>Heading</h4><p>Text</p></div>`. Gold non-KB alert tokens corpus-wide are padding0 29 / paddingL 10 / combined 9 / alertSolid 8 …
  — `rhs` 0, `summary` 0.
- **MEASURED (`outputs/_measure_r333_alertmods.py` / `_alerttags.py` / `_rhsdisc.py` / `_rhscol.py`, every paired Standard page, each Claude
  box matched to the gold by its first 8 words):**
  · `summary` — the gold wraps the same text in plain `alert` **25** / `alert solid` **4** / never `summary` (29/29 = 1.00; the writer's
    spelling makes no difference). Drop the token.
  · `rhs` — the gold box's class splits `alert top` 27 / `alertActivity` 23 / `alert` 20 (no form ≥ 0.60 on the class alone) **but its
    COLUMN solidifies: a side column (`col-md-4` / `col-4`) as the RIGHT sibling of a `col-md-8` content column on 56/70 = 0.80** (alertActivity
    23/23, alert top 26/27, alert 7/20). The class is decided by what PRECEDES the box: **after an activity box → `alertActivity` 15/20 = 0.75**
    (the KB's "Activity sidebar" form); **after plain content → `alert top` 26/41 = 0.63** of the side-column matches (alertActivity 8,
    plain alert 7). The writer's spelling is not a discriminator (`[alert box rhc]` → alertActivity 5 / alert 2 / alert top 2). Subject and
    length are not discriminators either (XGF9 alert 6 : top 7; MXFL 4 : 5 : 4). Fundamentals/Inquiry rhs boxes: 8 matched (5 alertActivity,
    3 alert top), 19 unmatched (single-page pairing) — the same rule applies, the probe names them.
- **Authority (§1b):** level 1 for the vocabulary (KB 05B — `rhs`/`summary` are not classes; a right-hand box beside an activity IS the KB's
  activity sidebar) + level 4 consensus for the two side forms (0.80 side column; 0.75 / 0.63 per position). Where the gold keeps a plain
  full-width `alert` for an rhs box (13/70) the side column is a NAMED consensus-over-gold delta. Engine precedents: r92/r94 already render
  the TABLE-form positional alert as `col-md-4 > alert top` paired right (ENGS302), r121/r123 render `[Side alert]` as the paired
  `alertActivity` column, r239 promoted the exact spelling `[right-hand alert]` to `side alert` and RECORDED this wider family (80 occ / 40
  modules) as the follow-up.
- **Triangulated:** ANZH101 lesson 1 (WT `[rhs alert]` after activity 1B; gold `row > col-md-8 [activity 1B] + col-md-4 col-12 > alertActivity >
  p`; Claude `row > col-md-8 > alert rhs` in its own row under the activity's row); XGF9006 lesson 2 (WT `[alert.rhs]` after prose; gold
  `col-md-8 paddingR [prose] + col-md-4 col-12 paddingL > alert top > p`; Claude a full-width `alert rhs` row); ANZH404 lesson 1 (WT `[alert box
  lesson summary]`; gold `alert`; Claude `alert summary`).
- **Fix (planned), data `callouts.positional_side_alert` {enabled, env `ALERTRHS_OFF`, tags [alert, important], keywords [rhs, rhc], strip_tokens
  {rhs: " rhs", rhc: " rhs", summary: " summary"}, after_activity def (= the KB activity sidebar: `col-md-4 offset-md-0 col-12 > alertActivity`,
  lead h4), after_content def (`col-md-4 col-12 > alert top`, lead h4)}:** at the callout emit site, an `alert`/`important` whose remainder
  carries an rhs keyword, in STRICT mode, with the preceding content row closed, is spliced as the RIGHT sibling of that row's `col-md-8`
  column through the r123 pairing (`#sideAlertCol`, which gains an optional h4 lead so an embedded payload is never dropped) — the
  `alertActivity` def when the closed row's first block is an activity box, the `alert top` def otherwise; with no preceding content row, or
  in SPAN mode, it renders as a plain `alert` with the token stripped. `summary` is stripped everywhere (→ `alert` / `alert solid`). OFF =
  byte-identical (the tokens stay, no routing). Regeneration: scoped to the modules the in-memory probe names over all 416.
- **Gate expectation:** skeleton ≥ hold — the rhs boxes gain the gold's `col-md-4` sibling line + the gold's class on ~56 of 70 paired sites
  (and lose a phantom own-row); the summary boxes' class line matches on 29/29; compare_structure may move (a container relocates into
  the preceding row — the r123 precedent moved exact +5); body/defect/leak EXACT. Est. +0.03–0.08pp. **Plateau window: r330 +0.040 ·
  r331 +0.022 · r332 +0.269.**

## Session 5 · Round 3 (engine r332) — what shipped (the empty footer → the KB's page-position form; the BLL1 footer class)
- **Fix:** Part A — `footer.kb_position_defaults` {enabled, env FOOTERPOS_OFF, overview next+home, lesson prev+next+home, final prev+home,
  by_footer_class {fundamentals-nav: home}} in `SkeletonBuilder.#buildFooter`: a registry `footer_links` value with no `value_map` entry (the
  miner's em-dash no-evidence marker) takes the KB's page-position form; forceLinks (the CED inquiry shell) outranks it; a mapped registry
  value is untouched. Part B — the BLL1 registry delta's stale `footer_class: footer-nav` removed (→ `footer-nav inquiry-nav`, gold 0.85).
- **Regeneration:** scoped — the in-memory probe over ALL 416 modules (4 shards) named 239 pages / 130 modules; every diff line = 141 empty
  footers gaining links (141 home, 118 prev, 31 next) + 98 BLL1 class swaps, nothing else; OFF = exactly the 98 BLL1 lines; the planner's 12
  batches, all rc 0; 0 truly stale; manifest diff = exactly the 239; ON = disk 2102/2102.
- **Gates:** skeleton 50.558 → 50.827 (+0.269pp; 207 moved, 185 up / 22 down — dips NAMED: 16 on the BLL1 plain-footer minority modules
  BLL121/172/174–177/145 (the series' 0.15), SSOG101_7_0 −3.5 / MXFL401_7_0 −3.4 / XDLS502_4_0 / TRR102_5_0 / CEDK102_0_0 = final pages whose gold
  keeps `next` under the KB's `prev+home`); ≥50 1034 → 1044; ≥75 196 → 200; every other gate line-for-line EXACT with r331; 13 selftests GREEN.
  **55.5% of achievable.**
- **Verifier:** Claude empty footers 141 → 0; BLL1 plain-footer pages 98 → 0. **Plateau window: r330 +0.040 · r331 +0.022 · r332 +0.269.**

## Session 5 · Round 3 PICK (engine r332) — written before any code, 2026-09-15 17:20 NZST
- **Class (Part A — corpus-wide, KB-backed):** the page FOOTER ships EMPTY (`<div id="footer">` with no `<ul>`/links) on **141 Claude pages /
  ~125 modules** (BLL1 49, TRR1 10, AGH1 9, OSSC 9, HIS1 8, PNR 5, CEDT 5, MXFL 5, CEDR 3, SSOG 3 …) — 120 of them the module's last page, the
  rest OSSC401/501's lesson pages (+ lexical-sort artefacts). Cause: `Style_Anchor_Registry` carries the miner's NO-EVIDENCE marker `—` as the
  `footer_links.final` (≈ 60 groups) / `lesson` (OSSC) value, and `SkeletonBuilder.#buildFooter` treats a present-but-unknown value as a
  pattern (`value_map["—"]` undefined → a warn note + a footer with no links). The KB (01B "Footer and Acknowledgements") fixes the form BY
  PAGE POSITION: overview `next-lesson + home-nav`; middle `prev + next + home`; **final `prev-lesson + home-nav` only** — and the gold on
  exactly those 141 pages is never empty (`prev+next+home` 82 / `prev+home` 29 / no footer at all 12 / `next+home` 2).
- **Class (Part B — the BLL1 series, registry data):** the BLL1 delta's `footer_class` = `footer-nav`, but the BLL1 gold ships
  `footer-nav inquiry-nav` on 128 of 150 pages (41 of 48 modules = 0.85; BLL2 123:25 and the subject rule already say `inquiry-nav`; the
  KB is silent for BLL — 06's table maps `inquiry-nav` to the Inquiry body, BLL1's body is `container-fluid`). Claude ships plain `footer-nav`
  on 98 BLL1 pages. A stale mined value (the r263 class), §1b level 4 (series consensus ≥ 0.60).
- **MEASURED (inline census, all paired pages; `outputs/_r331_skelgaps.json` surfaced the footer lines — `a.home-nav` missing on 280 gold
  pages, `ul.footer-nav.inquiry-nav` on 164):** footer composition gold == Claude on 904 Standard pages; the mismatches decompose into the
  empty-footer class (141) and the BLL1 class (98), plus editorial residue (gold `home+prev+next` orders, `active` items, doubled prev).
- **Authority (§1b):** Part A = 1 (KB 01B, by page position) — where the gold's final page keeps `next` (82) the KB's `prev+home` is a
  NAMED override, and an empty footer matched none of them; Part B = 4 (the BLL1 series consensus 0.85, the registry's own instrument).
- **Triangulated:** BLL112 (gold `-03` `prev+next+home` in `ul.footer-nav.inquiry-nav`; Claude `_2_0` an empty `<div id="footer">`, `_0_0`/`_1_0`
  plain `footer-nav`); OSSC401 lessons 1–3 (gold `prev+next+home`; Claude empty — registry `lesson: —`); HIS1001 lesson 10 (gold
  `prev+home`; Claude empty — registry `final: —`).
- **Fix (planned):** Part A — data `footer.kb_position_defaults` {enabled, env FOOTERPOS_OFF, overview next+home, lesson prev+next+home,
  final prev+home}: in `#buildFooter`, a registry `footer_links` value with no `value_map` entry (the `—` / `n/a` no-evidence literals)
  falls back to the KB's value for the page position; a registry value that IS in the map is untouched; the warn note becomes an info note
  naming the fallback. Part B — delete `footer_class` from the BLL1 delta (it then inherits the subject rule `footer-nav inquiry-nav`); no
  engine change, reversal = git (the r263 / r285 registry-correction precedent). Regeneration: scoped to the modules the in-memory probe
  names over all 416 (≈ 125 + 49 BLL1).
- **Gate expectation:** skeleton ≥ hold (the footer's `ul > li > a` lines appear where the gold has them; BLL1 `ul.footer-nav.inquiry-nav`
  lines match); every other gate EXACT (the footer is outside compare_structure / body_compare / the defect audit). Est. +0.05–0.10pp.
  **Plateau window: r330 +0.040 · r331 +0.022.**

## Session 5 · Round 2 (engine r331) — what shipped (a bilingual section box's headings render at the KB's activity level)
- **Fix:** `elements.dual_language.section_grouping.boxed_heading_level` {enabled, env REOBOXH_OFF, from_level 2, to_level 3, exclude_code_prefixes
  [PNR]}: `BilingualBuilder.boxedHeadingRelevel` moves every `<h2>` open/close pair inside a BOXED section's inner HTML to h3; un-boxed sections
  and h1 / h3+ untouched; PNR excluded (its own gold keeps h2).
- **Regeneration:** scoped — the in-memory probe over the whole Bilingual family (19 modules / 63 pages) named 21 pages / 5 modules (TRR109/111/
  112/113 + TRR301's 2 lines); OFF = disk 63/63; every diff line = 157 `<h2 reo|eng>` → `<h3>`; regenerated; 0 truly stale; manifest diff =
  exactly the 21; ON = disk 63/63.
- **Gates:** skeleton 50.536 → 50.558 (+0.022pp; 21 moved, 18 up / 3 down — dips NAMED TRR113_0_0 −6.25, TRR109_3_0 −4.38, TRR112_0_0 −2.61 =
  the scorer's alignment artefact, position-free overlap RISING on each; TRR111_2_0's r330 dip reversed exactly); ≥50 1033 → 1034; every
  other gate line-for-line EXACT with r330; 13 selftests GREEN. **55.2% of achievable.**
- **Verifier:** the in-box census after → TRR in-box h2 0 (h3 209). **Plateau window: r330 +0.040 · r331 +0.022.**

## Session 5 · Round 2 PICK (engine r331) — written before any code, 2026-09-15 16:50 NZST
- **How the PICK was made:** a new corpus-wide instrument, `outputs/_measure_r331_skelgaps.py` (the PRIMARY gate's own difflib opcodes tallied —
  which skeleton lines are most often MISSING in Claude / EXTRA vs the gold, per template folder; `_r331_skelgaps.json`). Its large signals were
  each KB-checked: the gold's `iframe.embed-responsive-item` (448 pages) and `videoSection.icon` (519) — the KB's canonical embed (05A COMP_13) is
  the plain `videoSection ratio ratio-16x9` + bare `iframe` that Claude already ships, and the KB is silent on `icon` (r200's Chris-approved
  registry) → not classes; the table class `table-bordered` (518 pages) → a KB-internal conflict (05D vs 06 §6) + a Standard gold TIE 0.51 →
  recorded under Blocked (needs Chris); the activity image SIDEBAR `alertImage` (388 gold sidebars, Claude 0) → measured and DECLINED (56% of the
  sidebar images are absent from the writer's document; the derivable signal predicts at 0.13); `[engagement quiz button]`'s form → 28 pages
  in total, the real-button subset ~12 (under the floor). What remains derivable and KB-backed at the floor is in the r330 area:
- **Class:** inside a bilingual (TRR-dialect) SECTION BOX, a writer `[H2]` heading renders at **h3** — the KB 07B activity structure's heading
  level (`<h3 reo>…</h3><h3 eng>…</h3>` as the box's children) — not at the writer's h2. Claude keeps h2 inside the box because the round-55
  re-leveller excludes activity-anchored headings from its pool (correct for the Standard template's `[Activity]` boxes, where the writer's
  `[H3]` is the title), while the bilingual keystone box is opened on `[H1] N.M` with the writer's `[H2]` section title inside it.
- **MEASURED (inline census over the Bilingual family, gold vs Claude, reo/eng headings INSIDE an activity box):** gold h3 348 / h2 42 / h4 …
  (0.89 h3 on the 8 writer-id modules; the box's FIRST heading h3 117 : h2 21 = 0.85); per module TRR109/110/111/112/113 in-box h2 = 0 in the gold;
  the label-form family (TRR102/108/114/203/301) gold in-box h3/h4 only and Claude already h3 there. **The 42 gold h2 are the PNR family**
  (PNR101 12 / PNR102 12 / PNR104 14 — the newer "Te Aka Taumatua" MTK template whose section title is a `[H1] Lesson Title:` row the gold keeps
  at h2, 0.72; 07B does not describe that dialect → its own gold governs, §1b level 3) → **PNR excluded by data**. Claude today: in-box h2 211
  (TRR109/111/112/113 ≈ 155 + PNR 56) / h3 24. Skeleton-visible on every boxed TRR page (≈ 20 pages / 4 modules) — the h2 lines become the
  gold's h3 lines.
- **Authority (§1b):** 1 = the KB (07B "Activity Structure": the activity's headings are `<h3>`; 05B activities `<h3>` title); 3 = the TRR gold
  (0.9+). Class B-ii (an output convention).
- **Triangulated:** TRR111 lesson 1 §1.2 (WT `| [H2] The sound: ia | [H2] Te oro: ia |` inside the boxed section → gold `<h3 reo>Te oro: ia</h3>
  <h3 eng>The sound: ia</h3>` inside `number="1.2"` → Claude `<h2 reo>Te oro: ia</h2><h2 eng>The sound: ia</h2>`); TRR109 lesson 2 (gold in-box
  `<h3>` ×N, Claude `<h2>`); TRR112 lesson 1 §1.3 (gold `<h3 reo>Te oro: oa</h3>` inside `number="1C"` → Claude `<h2>`).
- **Fix (planned):** data `section_grouping.boxed_heading_level` {enabled, env REOBOXH_OFF, from_level 2, to_level 3, exclude_code_prefixes
  ["PNR"]}: in `bilingualSection`, when the section is boxed, every `<h2 reo|eng>` / `</h2>` in the gathered inner HTML is re-levelled to h3
  (h1 / h3+ untouched — the gold keeps the writer's `[H3]` at h3). Scoped regeneration of the Bilingual family (the in-memory probe names the set).
- **Gate expectation:** skeleton ≥ hold (h2→h3 lines on ~20 boxed pages; est. +0.01–0.03pp); every other gate EXACT. **Plateau window: r330 +0.040.**

## Session 5 · Round 1 (engine r330) — what shipped (the bilingual section id is the activity number, not a heading)
- **Fix:** `elements.dual_language.section_grouping.section_id_number` {enabled, env REOSECID_OFF, strip_heading, number_from_section, id_pattern}
  in `BilingualBuilder`: the interleave strip drops a rendered heading whose whole text is a bare `N.M`; a `[H1] N.M`-opened boxed section with no
  `Activity NX:` label takes the id as its `number=`.
- **Regeneration:** scoped — the in-memory probe over the whole Bilingual family (19 modules / 63 pages) named 25 pages / 7 modules; OFF = disk
  63/63; every diff line = 234 phantom headings out + 72 boxes numbered; regenerated; 0 truly stale; manifest diff = exactly the 25; ON = disk 63/63.
- **Gates:** skeleton 50.496 → 50.536 (+0.040pp; 21 moved, 17 up / 4 down — dips NAMED TRR111_2_0 −6.01, PNR102_2_0 −3.73, TRR109_1_0 −0.51 = the
  scorer's repeat-collapse artefact (position-free overlap with the gold RISES on each), TRR113_3_0 −0.81 = the named letter→decimal override);
  ≥50 1030 → 1033; every other gate line-for-line EXACT with r329; 13 selftests GREEN. **55.2% of achievable.**
- **Verifier:** `_measure_r330_sectionid.py` after → phantoms 0 / unnumbered 0 / decimal 72. **Plateau window: r330 +0.040 (restarted).**

## Session 5 · Round 1 PICK (engine r330) — written before any code, 2026-09-15 16:40 NZST
- **Class:** the Bilingual writer's BARE SECTION-ID heading (`[H1] 1.1 | [H1] 1.1` — a numbered section label with no words) is the section's
  activity NUMBER, never a heading. KB 07B "Activity Structure": `<div class="activity" number="1.1">`, decimal form PREFERRED (A→.1, B→.2 …;
  "TRR108 retains the writer's letter format … Preferred approach: use decimal format (1.1, 1.2, 1.3) for consistency with TRR104/TRR105").
  Claude renders the id as a phantom heading pair (`<h3 reo>1.1</h3><h3 eng>1.1</h3>` in an un-boxed section, `<h2 reo>1.2</h2>…` inside a
  box) and leaves the section's `div.activity interactive` box UNNUMBERED. Skeleton-visible twice: the phantom heading lines (the gold has a
  bare-id heading on 0 of 2,385 pages) and the `number` attribute (`_structural_skeleton.KEEP_ATTR`).
- **MEASURED (`outputs/_measure_r330_sectionid.py` → `_r330_sectionid.json`; all 454 gold dirs, the Writers Template .docx read directly —
  13 TRR modules ship no parsed WT):** the tagged `[H1] N.M` form lives ONLY in the Bilingual folder — 8 modules / 298 tagged cells (PNR101 12,
  PNR102 14, PNR104 14, TRR109 60, TRR110 48, TRR111 48, TRR112 50, TRR113 52); 0 in Standard / Fundamentals / Inquiry (an untagged bare `N.M`
  cell in a Standard WT is a maths decimal — MXFU202 `505.5` — and is NOT the signal). Gold on those 8: decimal `number="N.M"` on 6 (PNR101/102/
  104, TRR109/110/111 — 82 boxes; writer id = gold number 22/24 on TRR111, 15/24 TRR110, 7/7 PNR104, 6/7 PNR102) and the human's LETTER
  form `number="1A"` on 2 (TRR112 39, TRR113 26 — the developer re-lettered the writer's `1.1 → 1A`); gold bare-id headings 0. **Share of the
  writer-id modules following "id → decimal number, no heading": 6/8 = 0.75 ≥ 0.60, and the KB names decimal as the preferred form → the 2
  letter modules become a NAMED KB-over-gold override (their `number` will read `1.1` where the gold reads `1A` — today Claude has NO number
  there, so the skeleton line stays mismatched either way: neutral, not a dip).** Claude today: **234 phantom section-id headings on 25
  pages / 7 modules** (TRR110 has no Claude dir), **72 unnumbered activity boxes** in the family (PNR 14, TRR 58), 0 decimal numbers.
  Family split: Bilingual only (PNR ×3, TRR ×4 with output); every other template folder 0 — the rule is scoped to the bilingual section
  path by construction (`BilingualBuilder.bilingualSection`, the round-135 keystone that already opens a section on `[H1] N.M`).
- **Authority (§1b):** 1 = the KB (07B, decimal `number`); 2/3 = the gold on 6 of 8 modules (TRR110/111, PNR — decimal, no heading); the
  human outliers TRR112/113 (letters) are overridden by the KB's stated preference, named. Class B-i (a positional/content convention with a
  tag-link: the `[H1] N.M` tag).
- **Triangulated:** TRR111 lesson 1 (WT `| [H1] 1.1 | [H1] 1.1 |` → `| [H2] Oropuare pūrua: ia | … |` → … `[Activity: Embedded] Wordselect` →
  gold `<h3 reo>Oropuare pūrua: ia</h3>…<div class="activity interactive" number="1.1">` and NO `1.1` heading → Claude `<h3 reo>1.1</h3><h3
  eng>1.1</h3>` + `<div class="activity interactive">`); PNR104 lesson 1 (WT `[H1] 1.1` → gold `<div class="activity interactive"
  number="1.1">` → Claude the box unnumbered with `<h2 reo>1.1</h2><h2 eng>1.1</h2>` inside); TRR112 lesson 1 (WT `[H1] 1.1` → gold
  `number="1A"` (the human's letters) → Claude phantom `1.1` + unnumbered — after: `number="1.1"`, the KB form, named).
- **Fix (planned):** data `elements.dual_language.section_grouping.section_id_number` {enabled, env REOSECID_OFF, strip_heading true,
  number_from_section true}: (1) `bilingualRows`' interleave strip also drops a heading whose whole text is a bare `N.M` section id (the same
  seam that already drops the `Activity NX:` label line); (2) `bilingualSection`, when the section was opened by `[H1] N.M`, has a widget
  (boxed) and found no `Activity NX:` label, numbers the box with the section id as written (decimal). The `Activity NX:` label keeps its
  priority (disjoint in practice: 0 label modules carry `[H1] N.M`); an un-boxed prose section simply loses its phantom (the gold leaves it
  un-boxed and un-numbered). Scoped regeneration: the family = every module the bilingual section path touches (the Bilingual folder, 19
  modules with a Claude dir) — the in-memory probe names the changed set; OFF = disk.
- **Gate expectation:** skeleton ≥ hold (phantom heading lines removed on 25 pages; `[number=N.M]` matches gained on TRR109/111 + PNR);
  every other gate EXACT or improved. Est. +0.01pp (the previous session's estimate). **Plateau window restarts at this round.**
- **Not this round (named for a later PICK):** the section TITLE placement (Claude puts the `[H2]` section title inside the box, the TRR111
  gold outside / the TRR112 gold inside — measure per module group); the `Activity NX:` letter labels → decimal (KB 07B over the 5 label
  modules' gold letters — a KB-over-gold override needing its own measure); TRR109's own duplicate `1.1` (a human error, not chased).

## Session 4 · Round 4 (engine r329) — what shipped (`[trigger engagement]` is a marker, not a button)
- **Fix:** `buttons["engagement quiz button"].trigger_marker` {enabled, env ENGMARKER_OFF, aliases [trigger engagement, engagement trigger],
  words_flag} at the generic `[button]` seam before the label / URL derivation: a label-less marker (bracket equals or ends in an alias, no
  black text) emits nothing; a bracket with other words → one diagnostic red flag. `[engagement quiz button]` untouched.
- **Regeneration:** scoped — the in-memory ON probe over all 416 named 60 pages / 42 modules; regenerated; 0 truly stale; OFF vs disk = exactly
  the 60 pages; ON = disk 266/266. Phantom `button engagementTrigger` 99 → 28 (the residue = compound / text-bearing brackets, named).
- **Gates:** skeleton 50.492 → 50.496 (+0.004pp; 60 moved, 57 up / 3 down — dips NAMED CEDO105_5_0 −7.63 (one removed skeleton line re-aligns
  difflib's blocks; the element sequence is strictly closer to the gold), MXEO301_7_0 −1.15 (repeat-collapse), ENGI401_6_0 −0.42); every other
  gate EXACT; 13 selftests GREEN. **55.1% of achievable.**
- **Plateau:** r327 0.000 · r328 0.000 · r329 +0.004 → the third consecutive sub-threshold round → STOP (§4).

## Session 4 · Round 4 PICK (engine r329) — written before any code, 2026-09-15 15:28 NZST
- **Class:** the writer's `[trigger engagement]` / `[engagement trigger]` / `[to trigger engagement]` is a CONDITION MARKER, not a button — the KB
  reads it as the dropbox-trigger signal (constraint 43: "any activity that ends in a dropbox submission button ('Go to dropbox' / 'Upload to
  dropbox' / `[trigger engagement]`) carries the `dropbox` modifier"; 05B "whose writer source carries `[trigger engagement]`"; 01F the BLL
  form) and the finished modules carry NO engagement markup at all (0 of 2,385 gold pages have any `engag…` class or attribute). Claude's
  Tag_Lexicon folds those aliases into `engagement quiz button` (the KB's `engagement_quiz_button` = "External quiz link button" — a real
  button, `[engagement quiz button]` ×23) and the generic seam emits a PHANTOM `<div class="button engagementTrigger">Go to your journal</div>`
  (the label-less tag falls to `journal_label_default`): **99 phantom buttons on 88 pages / 70 modules** (Standard 74 / Inquiry 10 / Fundamentals
  4 pages; 84 with the journal default label, 15 with a swept-in filename or the bracket's own words). Skeleton-visible: a `div.button` node the
  gold never has.
- **Authority (§1b):** 1 = the KB (c43 / 05B / 01F: a marker on the activity, no element; 01D/01F: `engagement quiz button` is the button, its
  aliases do not include the trigger forms); 3 = the gold, 100% (no engagement element anywhere). The engine already treats the marker as
  content-less in two places (r292 InteractiveBuilder "a stray marker", r322 `_mtkEngAbsorbed`); this closes the third seam.
- **MEASURED (WT bracket forms, all 454 modules):** `[trigger engagement]` 183, `[dropbox to trigger engagement]` 25, `[engagement trigger]` 21,
  `[dev – quiz to trigger engagement …]` 18, `[to trigger engagement]` 8, `[insert mtk quiz – trigger engagement]` 8, MTK-quiz compounds 9,
  `[insert text box for student response – engagement trigger]` 3 — 275 occurrences in 71 modules; `[engagement quiz button]` 23 + 4 quiz
  compounds (the real button, untouched). Gold at the `[trigger engagement]` sites (BLL240 1F, ENGI401 4, XDLS908): the dropbox button and nothing
  after it.
- **Triangulated:** BLL240 1 (WT `[Button] Upload to dropbox [trigger engagement]` → gold `<a href="" target="_blank"><div class="button">Upload
  to dropbox</div></a>` then the box closes → Claude the upload button + `<div class="button engagementTrigger">Go to your journal</div>`);
  ENGI401 4 (WT `[Button] Upload to dropbox. [Trigger Engagement]` → gold the dropbox anchor only → Claude + the phantom); ARFUN01 (WT `[Insert text
  box for student response – Engagement trigger]` → gold an MTK "Go to quiz" (its own class) → Claude the phantom journal button).
- **Fix (planned):** `buttons["engagement quiz button"].trigger_marker` {enabled, env ENGMARKER_OFF, aliases ["trigger engagement", "engagement
  trigger"], words_flag true}: at the generic seam, an `engagement quiz button` item whose bracket text ends in a marker alias and carries no
  black text emits NOTHING (the r292 rule: a content-less marker); a bracket carrying other words (`[insert text box for student response –
  engagement trigger]`) surfaces them as one diagnostic red flag (cv2-note) so nothing the writer wrote is lost. `[engagement quiz button]` itself
  is untouched. Scoped regeneration (the in-memory probe names the set); OFF = disk.
- **Gate expectation:** skeleton ≥ hold (a phantom `div.button` node removed where the gold has none); every other gate EXACT or improved
  (compare_structure may gain an exact chain). **Plateau window: r327 0.000 · r328 0.000 — this round must move ≥ 0.02pp or the loop stops after it.**

## Session 4 · Round 3 (engine r328) — what shipped (KB constraint 55's label half)
- **Fix:** `buttons.canonical_labels` {enabled, env BTNLABEL_OFF, rules [quiz → Go to quiz; portfolio → Go to portfolio; dropbox → Go to dropbox,
  family_labels BLL / LS / HPE → Upload to Dropbox]} — `ContentConverter.#buttonCanonicalLabel` at the generic `[button]` seam, after the r323
  trim and before the r326 anchor. 'Journal' (10) untouched (no KB rule).
- **Regeneration:** scoped — the in-memory ON probe over all 416 named 47 pages / 40 modules; regenerated; 0 truly stale; OFF vs disk = exactly
  the 47 pages; ON = disk 152/152. Bare `Quiz` / `Quiz button` / `Portfolio` / `Dropbox` labels 84 → 0.
- **Gates:** every gate EXACT (fastloop PASS, 10 metrics HELD; full suite identical; skeleton 50.492, 0 moved); 13 selftests GREEN. **55.1% of
  achievable** (unchanged). KB status row 55 → the label half CAPTURED.
- **Plateau window:** r326 +0.057 · r327 0.000 · r328 0.000 — two consecutive sub-threshold rounds; a third stops the loop (§4).

## Session 4 · Round 3 PICK (engine r328) — written before any code, 2026-09-15 15:12 NZST
- **Class:** KB constraint 55's LABEL half — a submission button "keeps its full 'Go to' label — 'Go to dropbox' / 'Go to portfolio' — the
  leading 'Go to' is never dropped to a bare 'Dropbox' / 'Portfolio'"; CL-0038 / constraint 65 — the quiz button reads 'Go to quiz'; 14.11 /
  14D — the BLL, LS and HPE families label the dropbox button 'Upload to Dropbox' (series-scoped, alongside the universal default). Claude ships
  the writer's bare noun as the label: `[Button] Portfolio` → `Portfolio`, `[Add button] Quiz button` → `Quiz button`, `[Add button] Quiz` →
  `Quiz`, `[Button] Dropbox` → `Dropbox`. Gate-neutral (text). Round 323 captured row 55's full-stop half; this is the prefix half.
- **Authority (§1b):** 1 = KB c55 + CL-0038 + 14.11; 3 = the gold agrees in every module carrying the class (below).
- **MEASURED (`_r328` inline probe over every Claude page):** **94 bare-noun labels on 54 pages / 44 modules** — quiz 34 + 'quiz button' 11,
  portfolio 25, dropbox 13 + 'drop box' 1, journal 10 (by template Fundamentals 35 / Standard 32 / Inquiry 27). In the same modules the gold's
  labels: quiz → `Go to quiz` ×128 (no other form), portfolio → `Go to portfolio` ×77, dropbox → `Upload to dropbox` ×58. 'Journal' (10) has no
  KB label rule → left alone (the r239 h4 rule covers 'go to journal' labels only). The gold's bare 'Quiz' (4) / 'Dropbox' (3) are its outliers.
- **Triangulated:** EXPFUN04 (WT `[Button] Portfolio` ×3 → gold `<a …><div class="button">Go to portfolio</div></a>` → Claude `Portfolio`);
  HIS1004 (WT `[Add button] Quiz button` → gold `Go to quiz` → Claude `Quiz button`); HPFUN101 (WT `[Add button] Quiz` → gold `Go to quiz` →
  Claude `Quiz`).
- **Fix (planned):** `Emit_Templates.buttons.canonical_labels` {enabled, env BTNLABEL_OFF, rules [quiz → 'Go to quiz'; portfolio → 'Go to
  portfolio'; dropbox → 'Go to dropbox' with the 14.11 family override 'Upload to Dropbox' for the BLL / LS (XLP, XDLS, XLS, LS, SLO, SL) / HPE
  (HES, PHE, PES, HPE) prefixes]} applied at the generic `[button]` seam after the r323 trim and before the r326 anchor (so the quiz row's `#`
  href and To Do wording key on the canonical label). Scoped regeneration (the in-memory probe names the set); OFF = disk.
- **Gate expectation:** every gate EXACT (text). Plateau window: r326 +0.057 · r327 0.000 · r328 0.000 → the next sub-threshold round stops the loop.

## Session 4 · Round 2 (engine r327) — what shipped (the KB's title-casing rule)
- **Fix:** `header.title_casing` {enabled, env TITLECASE_OFF, min_words 2, keep_tokens_with_digits true, red_flag} — `SkeletonBuilder.#titleCasing`
  at the header title fill (plain / lowercase-span templates; the BLL phonics template untouched): a multi-word all-caps title → sentence case
  (macrons kept, digit tokens kept, single token untouched) + ONE red flag quoting the original (the KB's proper-noun caution applied to all).
- **Regeneration:** scoped — the in-memory ON probe over all 416 named 47 pages / 15 modules (= the measured population); regenerated; 0 truly
  stale; OFF vs disk on the 15 = exactly the 47 pages; ON = disk 160/160. Claude all-caps multi-word header spans 47 → 0; 47 flags.
- **Gates:** every gate EXACT (fastloop PASS, all deltas 0; full suite identical; skeleton 50.492 page-for-page identical, 0 moved); 13 selftests
  GREEN; the r324 title classifier exact 550 → 567 / case-only 88 → 71. **55.1% of achievable** (unchanged). KB status row 1 → the
  ALL-CAPS normalisation CAPTURED-LIVE.
- **Plateau window:** r326 +0.057 · r327 0.000 (gate-neutral, KB-driven) — one sub-threshold round.

## Session 4 · Round 2 PICK (engine r327) — written before any code, 2026-09-15 14:58 NZST
- **Class:** a writer's MULTI-WORD ALL-CAPS title ships ALL CAPS in the header `<h1><span>` (`DREAM IT, PLAN IT, DO IT`, `TE TIRITI O WAITANGI`,
  `INTRODUCTION TO POTENTIAL ENERGY AND WORK`). The KB (01A_TEMPLATE_LEVELS_CORE "Title casing — normalise a MULTI-WORD ALL-CAPS title",
  10_CORPUS_VALIDATED_SCAFFOLDING §1, constraint 1's permitted normalisations — KB status row 1 "ALL-CAPS title UNVERIFIED") says: render it in
  SENTENCE CASE (first letter capitalised, the rest lowercase; the Te Reo span the same, macrons kept); a SINGLE all-caps token is left as written
  (proper noun / acronym); sentence-casing cannot restore internal capitals, so raise a visible red flag quoting the original. Gate-neutral (the
  skeleton is text-stripped).
- **Authority (§1b):** 1 = the KB rule (corpus-validated in the KB itself: 0 of 105 multi-word header spans all-caps). The gold agrees on every
  paired case but is era-mixed in HOW it re-cases (sentence case 26, Title Case 14, lowercase 2 — `a mule, a wizard and jim crow`); the KB's
  sentence case is the target, not the gold's variant.
- **MEASURED (every header `<h1><span>`, acks / glossary pages excluded):** gold 3,047 spans — 15 all-caps multi-word, ALL of them unreplaced
  placeholders (`TE REO TRANSLATION HERE`, `MODULE TITLE TE REO`, `TRANSLATION NEEDED`), i.e. 0 real titles. **Claude 2,345 spans — 47 all-caps
  multi-word on 47 pages / 15 modules** (Standard 44 / Inquiry 3 / Bilingual 0 / Fundamentals 0; CEDK501 3, CEDO502 6, HES1003 5, HES1004 2,
  HIS1001 6, HIS1005 9, HIS1006 3, HIS1007 4, HIS1008 3, PES1007 2, MXEO401 1, ENGS101 1, CEDO501 1, HES1005 1, PES1008 1); every one is the
  writer's own ALL-CAPS text carried verbatim (`claude-in-WT` on all). The wider case-only title class (66 pages) is the gold's editorial
  Title-Case / sentence-case choices on titles the writer typed in mixed case — the KB says render those exactly as written → class C, not chased.
- **Triangulated:** CEDK501 1 (WT `DREAM IT, PLAN IT, DO IT` → gold `Dream it, plan it, do it` → Claude ALL CAPS); HIS1005 2 (WT `TE TIRITI O
  WAITANGI` → gold `Te tiriti o waitangi` → Claude ALL CAPS — the proper-noun caution: the gold itself lost the capitals, the flag exists for this);
  PES1007 4 (WT `INTRODUCTION TO POTENTIAL ENERGY AND WORK` → gold `Introduction to potential energy and work` → Claude ALL CAPS).
- **Fix (planned):** `Emit_Templates.header.title_casing` {enabled, env TITLECASE_OFF, min_words 2, keep_tokens_with_digits true (`(US7121)` is a
  code, not a word), red_flag text quoting the original}; `SkeletonBuilder.#titleCasing` at the header title fill (the plain / lowercase-span
  templates; the BLL phonics template untouched — its lead is the round-125 mechanism). ONE red flag (cv2-note, gate-neutral) after the h1 on
  every normalised title: the KB's proper-noun caution applied to all of them, because the converter cannot tell `Castle Bravo` from `castle bravo`.
- **Regeneration:** the r324 pattern — in-memory ON probe over all 416 modules names the changed set; scoped regeneration of those modules;
  OFF in memory = disk on every page.
- **Gate expectation:** every gate EXACT (text-immune skeleton; compare/body fold case); the r324 title classifier's `case/ws/macron-only` row
  drops by the normalised pages that now match the gold exactly. Plateau window: r326 +0.057 → this round is the first sub-threshold candidate.

## Session 4 · Round 1 (engine r326) — what shipped (the KB's universal button form)
- **Fix:** `buttons.anchor_wrap` {enabled, env BTNANCHOR_OFF, form `<a href="{href}" target="_blank">{button}</a>`, todo_note, exclude_label_match,
  targets [dropbox / portfolio / quiz(href #) / journal|workbook / download], default} — `ContentConverter.#buttonAnchorWrap` at the generic
  `[button]` emit (key === 'button' only). A URL-carrying button keeps its link (285 `[LINK: …]` hyperlinks were being lost); a URL-less one ships
  the blank anchor + ONE To Do note (the r308 pattern). Reveal-type labels excluded (gold = JS `button clickDrop`; 0 false hits on 3,311 gold
  anchored labels). Repair inside the round: the first full regeneration wrapped 219 reveal buttons / 38 modules → exclusion added → second full
  regeneration.
- **Regeneration:** FULL (416 modules / 70 batches, twice); 0 stale (mtime); 713 pages / 286 modules changed, 0 added / removed; OFF in memory =
  disk 2,102 / 2,102 before. Claude bare buttons 1,800 → 338 (upload 480 → 0, quiz 25 → 0, download 17 → 0, journal 460 → 91 = engagementTrigger,
  other 818 → 247 = reveal 219 + builder 28); anchored 475 → 1,937.
- **Gates:** skeleton 50.435 → 50.492 (+0.057pp; 675 moved, 210 up / 465 down; IDENTICAL net of the 713 changed pages — 53.624 = 53.624 over
  1,276), ≥50 1031 → 1030 (NAMED: the scorer's repeat-collapsing — `_r326_scorer_diag.py`: gate pp-sum −4.26 vs uncollapsed +104.40 on the 248
  biggest movers; six of the ten down-crossers sat at exactly 50.00; `_gatecheck.py` says REGRESSED on that line, judged under the §1b override
  accounting as r317), ≥75 193 → 196, ≥90 15; body 192 → 191 IMPROVED; every other gate EXACT; 13 selftests GREEN. **55.1% of achievable.**
- **Plateau window:** restarts at this round: r326 +0.057pp (≥ 0.02).

## Session 4 · Round 1 PICK (engine r326) — written before any code, 2026-09-15 13:55 NZST
- **Class:** a writer's call-to-action `[button]` ships as a BARE `<div class="button">{label}</div>` whenever no URL was found; the KB's
  universal button form (05D_COMP14_BUTTONS_TABLES_COLUMNS lines 11 / 58-59 / 83: `<a href="URL" target="_blank"><div class="button">…</div></a>`,
  constraint 65's `href="#"` quiz button) and the gold (an `<a>` around every non-JS `div.button`/`div.buttonD`) both put the button INSIDE an
  anchor — even when the developer has not wired the target (`href=""` / `href="#"` on 244 gold buttons). Gate-visible: the skeleton sees `<a>` nodes.
- **Authority (§1b):** 1 = the KB's universal button form; 3 = the gold convention (below). Claude's own r308 upload box already ships the
  anchored `<a href="" target="_blank">` form + one To Do note — this round generalises that seam.
- **MEASURED (`outputs/_measure_r326_buttonanchor.py` → `_r326_buttonanchor.json`, every paired page; JS buttons clickDrop / TKmodalButton /
  rSBtn / externalButton excluded):** gold wrapped share by template Bilingual 1.000 (n=65) / Fundamentals 1.000 (159) / Inquiry 0.977 (558) /
  Standard 0.997 (2553); by category upload 0.998 (1245) / journal 1.000 (1179) / quiz 0.995 (193) / download 1.000 (110) / other 0.970 (608);
  by subject prefix: 62 prefixes, NONE below 0.60. Gold href kinds: d2l quicklinks 1372, real URLs 529, blank/# 244, bare 21. **Claude ships
  1,800 bare buttons on 762 pages / 306 modules** (upload 480, journal 460, quiz 25, download 17, other 818 — the 'other' figure includes the
  widget builders' own JS buttons 'Check answers' / 'Reset' etc., which are NOT at this seam and are not touched).
- **Scope of the fix:** the generic `[button]`-family emit in `ContentConverter.#element` (the r323 seam) — the three bare forms `buttons.button`,
  `buttons.button_dropbox` (buttonD) and `buttons.button_download` when no URL was absorbed: wrap in `<a href="" target="_blank">…</a>` and add
  ONE Designer/Developer To Do note (cv2-note, gate-neutral — the r308 pattern) naming what to wire (dropbox quicklink / portfolio / journal
  document / quiz quicklink / the link target). The engagementTrigger / supervisor / audioButton forms (gold carries none of those classes — their
  target shape is unmeasured) are NOT in scope; recorded as a follow-up.
- **Also seen, recorded for a later PICK:** (a) a `[Button] label [LINK: url]` whose Word hyperlink is LOST (SSOG101 6 'How Can I Help Activity' —
  gold anchors the docs.google URL; 162 WT button lines / 56 modules carry a `[LINK:`); (b) KB constraint 55's label part — Claude ships bare
  labels 'Portfolio' 25 / 'Dropbox' 12 / 'Quiz' 33 where the KB says 'Go to portfolio' / 'Go to dropbox' / 'Go to quiz' (gate-neutral text);
  (c) the gold has more upload buttons than Claude on ~230 pages / 142 modules (`_r326_dbxmissing_modules.json`) — 33 modules WT-silent (class C),
  the rest inside un-built interactives or non-lexicon marker forms (`[dev- a dropbox with icons like here?]`, `[CS please create appropriate
  Dropbox]`); (d) the "dropbox terminates its activity" follow-up is CLOSED on measurement (`_measure_r326_dbxterminate.py`: Claude 0 boxes
  with content after the button; gold 710/718 last-child).
- **Regeneration:** the `[button]` tag family = the corpus (r323 precedent) → FULL regeneration.
- **Gate expectation:** skeleton ≥ hold (an `<a>` node appears where the gold has one); every other gate EXACT; the button-family verifiers
  (mtkquiz, dropdown, clickdrop) defect 0; the r323 `_measure_r323_buttonstop.py` after-state unchanged.

## Follow-up candidates surfaced by Round 1 (NOT queued — each needs a PICK + corpus-wide measure per §3)
- **The dropbox bundle terminates its activity.** Gold: the upload button is the box's LAST content child in 629/720 non-BLL (87%) and 463/475 BLL (97%).
  After an r314 hold the box stays open to the next auto-close boundary (XTAS101 1G swallows `[body] Listen and read…` + a carousel before the
  `[Summary box:]`). Same rule every non-owned activity already follows, so measure it over BOTH populations before deciding; gate-visible.
- **The r308 release order** (button, To Do note, then captured learner text) is the reverse of the gold (text, then the button last). Size by the
  number of upload-box bundles that release content; gate-visible.
- **`anchor_compare.wt_items` first-file read** (`pf[0]` of an unsorted listdir — the Round-0 two-file trap) — a measurement-tool repair, not a class.

## KB facts in hand (gold / Claude) — the KB queue is §D of KB_AMALGAMATION_STATUS.md
- LIVE: c71 footer hrefs, c82 body tag, c63 inner col-12, c61 iStock ID, c24 menu italics, BLL lowercase title, **c43 dropbox placement + modifier (r314)**.
- NOT CAPTURED (queued): c90/c45 acks statements + class (413 pages, full regen),
  c79 lesson title + bilingual pair (652 / 227 pages), c89 learningSupport (228 pages, gate-neutral),
  c83 lazy in moving widgets (~243 pages, gate-neutral), c28 doctype/self-closing (2102 pages, gate-neutral),
  c47/c95 Lesson-N heading strip (89 pages), c65 quiz content omission (56 shells), c55 trailing full stops (420 buttons),
  stickyNav (series convention), c67 overflowYScroll (27 pages).

## Declined classes
- **[D10-3, 2026-09-16: the widget BUILDS are now authorised — the modifier follows each build; the decline from the BOX side stands.]** **The activity `interactive` modifier (KB 01F `activity` + ID (interactive) → `<div class="activity interactive" number="ID">`; 03A)
  — DECLINED 2026-09-16 (session 7, Round 2 PICK; `outputs/_measure_r339_actinteractive.py` → `_r339_actinteractive.json` / `.log`,
  every gold activity box paired with Claude's box of the SAME number on the paired page).** 4,213 paired boxes: agree-yes 1,208 · agree-no
  1,964 · GAP gold-yes/Claude-no 758 (455 pages / 238 modules) · OVER gold-no/Claude-yes 283 (Claude's own hand-off boxes). The gold marks a box `interactive` because it
  BUILT a task widget Claude cannot (dragAndDrop 212 / mcq 76 / typing 76 / dropQuiz 41 / clickDrop 38 …): on Claude's side the gap boxes
  hold plain text (n=967, gold-interactive share 0.26) or an `unclassified` hand-off with its table (n=474, 0.49); a built videoSection 0.15, carousel 0.11, image 0.22, accordion 0.22 — no Claude-visible signature reaches the r182 floor,
  and the r58/r64 post-pass already marks every box whose widget Claude names. This is decision 5's population (the un-built task widgets);
  the token follows the build. Never re-attempt from the box side.
- **The UNTAGGED standalone hyperlink → externalButton (KB constraint 75's "position decides" read onto an untagged link) — DECLINED
  2026-09-15 (session 7, Round 1 PICK; `outputs/_measure_r338_standalone_links.cjs` → `_r338_standalone_links.json` / `.log`, the LIVE
  extractor over all 454 modules; the reverse trace `_measure_r338_gold_buttons.cjs` → `_r338_gold_buttons.json` / `.log`).** The r337
  note's "452 untagged hyperlink phrases the human buttoned (255 pages)" was a parsed-text artefact. Untagged STANDALONE hyperlink paragraphs:
  486 phrase + 1,226 bare-URL; the gold ships them as a button at **0.067 / 0.072 of the found sites** (the majority are the writer's asset
  references — sharepoint 114, drive 112, istock 87, docs.google 41 — that the gold ships as media or drops; youtube 62 → inline `<a>` 28 /
  plain 18 / button 1); untagged INLINE 0.067 (phrase) / 0.202 (URL); in a list item 0.028. Below the r182 floor in every template and
  subject group. The 873 gold externalButtons trace to: HREF-sourced 526 (the `[button]`-family tags with a URL dominate → round 338),
  text-only 140, no WT source 207 (class C). Never re-attempt without a new discriminator.
- **The activity box's SUB-heading level (the r334 sibling: every heading inside a box after its title) — DECLINED 2026-09-15 (session 6,
  Round 2 PICK; `outputs/_measure_r336_subhead.py` → `_r336_subhead.json` + `_r336_subhead.log`).** Gold census of 2nd+ headings inside
  Standard boxes: h4 0.494 / h3 0.321 / h5 0.172 (n=5125) — no level ≥ 0.60, the level follows the writer's own digit. Paired BY TEXT
  within the same `number=` box, Claude already matches the gold at **0.957** in Standard (225/235; 5 differing pages / 5 modules),
  0.885 Inquiry (2 pages), Bilingual 0.575 (4 pages / 3 modules — the r331 TRR/PNR box rule). The r334 note's "gold h3→h4 655 vs
  Claude h3→h3 657" was a POSITION-wise artefact: the gold's first sub-heading is usually a heading Claude never ships (the gold's
  own `Go to your journal` h4 sits at a different slot), so position pairing compared different elements. Nothing to build.

- **[D10-3, 2026-09-16: the D&D builds are now authorised — re-measure the wrapper per built layout; the decline from the box side stands.]** **The widened activity wrapper (KB c17 / c56 — `col-md-12 col-12` for wide interactives, `col-12` for a D&D column with many images) —
  DECLINED 2026-09-15 (session 5, Round 5 PICK; measured inline over every gold activity box by the widget type inside it).** The gold keeps
  `col-md-8 col-12` as the MAJORITY for every type — text-only 0.85, videoSection 0.88, D&D standard 0.72, typing 0.78, dropQuiz 0.82, D&D
  column **0.51** (col-12 0.26 / col-md-12 0.23), memoryGame 0.53, flipCard 0.54 — so no widened form solidifies (≥ 0.60), and the D&D
  LAYOUT (column vs standard) is the developer's choice, not in the writer's tag; Claude does not build D&D (decision 5). The substitution
  instrument (`_r334_subst.json`) shows the class as `div.col-12 ⇐ div.col-md-8.col-12` 254 occ / 220 pages + `div.col-md-12.col-12 ⇐ …` 166 /
  142 + `col-md-10` 82 / 69 (the KB forbids col-md-10). Re-open only if the writer's tag carries the layout.
- **`iframe.embed-responsive-item` (130 occ / 121 pages / 59 modules) — Claude is KB-correct**: every KB iframe form (01E, 04A, 05A) is
  class-less; the gold's class is era-mixed. Not chased. Same for `body.container-fluid.mathJax` (71 pages / 17 modules — the KB is silent;
  measure before any round).
- **The activity box's own h4 SUB-headings after the title (gold `h3 → h4` 655 vs Claude `h3 → h3` 657 on the title→next pair)** — a second,
  separate heading class inside the box (the writer's digit is the discriminator to measure); not this round.
- **c67 `overflowYScroll scroll="500"` on long panels — DECLINED 2026-09-15 (Round 11 PICK).** Measured over every gold accordion / tab panel
  (4,932 panels): the class rides 25 accContent + 6 tab-pane + 8 other panels on 27 pages (HIS1004 ×9), and its share is ≤ 0.05 in EVERY
  length bucket (accContent 1–2k chars 9/164, 2–4k 8/158, 4–8k 4/186, 8k+ 2/178; tab-pane 2–4k 4/97) — panel length does not predict it, no
  other discriminator exists. Below the r182 solidify floor in every group.
- **→ DECIDED 2026-09-16 — D10-1 (Chris: Option A — c47 in full, the human's SSOG101 form; queued item 2, scoped). The decline below is superseded by the decision.** Pre-decision record: **c47 / CL-0095 — the duplicate body heading on a lesson page (Round 7 candidate, measured 2026-09-15 03:30, `outputs/_measure_r320_dupheading.py`
  → `_r320_dupheading.json`).** 88 cases / 77 pages where a Claude body heading equals the header title (exact, or after a `Lesson N` / label
  prefix). (a) The `Lesson N`-PREFIXED opening duplicate: gold drops 11/11 first-heading cases (12 with one later) — a 100% convention, both
  authorities agree — but only **12 pages**, under the loop's 20-page floor. (b) The EXACT duplicate: 70 cases, but 41 of them only match because
  Claude's TITLE is wrong (TRR108/114/203/304 `Finished!` — the MTK title-source defect, a c79 sub-mechanism); among the 14 first-heading cases
  where both sides carry the same title the gold drops 8 (57%) and keeps 6 (XDLS903 `Poi`, ENGI101 `Being Frank`, ENGJ101, MXEO202, OSSM301 …);
  corpus-wide the gold KEEPS an exact duplicate on 111 lesson pages. Share 0.57 < 0.60 and a signature that misfires on wrong titles → DECLINED
  under §2/§3 (the r182 solidify rule). c47 is pre-ledger documentation, not a locked admin decision, so the KB-over-gold override was not
  invoked for a 21-page dip. Re-open (a) as part of a later heading round once the TRR title-source class lands, or if Chris says the KB's
  universal wording should be applied regardless of the gold (then: strip + drop the opening duplicate on lesson pages, strip-only on the overview).

- **The activity image SIDEBAR (`col-md-4 offset-md-0 > div.alertImage`, KB 05B / 02B) — DECLINED 2026-09-15 (session 5, Round 2 PICK; `outputs/_measure_r331_alertimage.py` + `_r331_alertimage_pos.py` → `_r331_alertimage.json`).** The gold ships 388 sidebars on the paired pages (Standard 281 / Inquiry 61 / Fundamentals 36 / Bilingual 10), Claude 0 — but **216 of the 388 (56%) use an image that is absent from the writer's document** (the designer's own beautification asset — class C), 36 sit in cv2 hand-off dumps (widget builds), 49 have no same-numbered Claude box; of the derivable remainder the only WT signal — the writer's image inside the activity — predicts a sidebar at **0.13** (48 of 361 Claude boxes holding an image; "last member before the button" 0.17; "image-only row right after the box" 5:11) — below the r182 solidify floor in every template. The KB defines the sidebar's FORM (05B), not a writer-side trigger. Never re-attempt without a new discriminator.
- **→ DECIDED 2026-09-16 — D10-5 (Chris: Option A — apply 05D everywhere; queued item 5).** Pre-decision record: **The KB's default table class `table table-bordered` (05D) — NOT PICKED 2026-09-15 (session 5, Round 2 PICK; measured inline).** Claude ships bare `table.table` on 1,063 tables / 518 pages. The gold is a genuine TIE in Standard (bordered 0.51 of 1,432 tables; 104 modules all-bordered / 51 none / 78 mixed), ≥ 0.60 in Inquiry 0.72 / Fundamentals 0.69 / Bilingual 0.86; `tableFixed` does NOT follow the KB's 2-column guidance (2-col tables 0.19; it tracks 4+ columns). The KB's own two documents disagree (05D `table table-bordered` default vs 06 §6 Refresh baseline `table noHover tableFixed`). A `table-bordered` default would be a KB-over-gold override costing ≈ −133 matched table lines in Standard for +74 in Inquiry / Fundamentals — needs Chris to settle 05D vs 06 (see Blocked classes). Not attempted.

## Blocked classes — ALL SIX DECIDED 2026-09-16 (Decisions from Chris, session 10: D10-1…D10-9); the entries below are kept verbatim as the evidence record each decision was made on
- **→ DECIDED 2026-09-16 — D10-9 (Chris: Option A — the KB's `<h5>` form everywhere, overview tab included; queued item 6, FULL regeneration).** Pre-decision record: **KB constraint 23 / 01B — the lesson-menu LABEL form (`<h5>` for every "We are learning… / I can: / You will show your understanding by:"
  label, the writer's wording normalised) vs the gold's per-series forms — needs Chris, 2026-09-16 (session 8, Round 2 PICK;
  `outputs/_measure_r341_menulabels.py` → `_r341_menulabels.{json,log}`, measured INSIDE `#module-menu-content` on every paired lesson page).**
  Claude already ships `<h5>` on 1,257 labels (gold h5 0.71); the RESIDUE is 206 `<p>` labels / 176 pages / 42 modules where the r117
  exact-fold phrase list misses the writer's variant or the r81 eng-family skip applies — and there the gold is split BY SERIES: NCEA1 h5 0.95,
  English h5 27 / h3 24 / p 22 (per module), Mathematics p, ConnectED p 20 / h5 5, Leaving to Learn p, Online Safety = the c70 "Ākonga will…"
  lead-in SENTENCE (a `<p>` by the KB's own rule — Claude right). 01B lines 196–197 also make the OVERVIEW tab's "We are learning:" / "I can:"
  labels `<h5>`, which the r81 two_col eng-family rule deliberately keeps `<p>` (gold 0.80 on ~296 overview pages). Decision needed: (a) apply
  c23 everywhere — every lesson-menu label `<h5>` (a named KB-over-gold override on ~80 lesson pages + ~296 overview pages; skeleton ≈ −0.1pp,
  KB-correct), (b) apply c23 to lesson menus only, keeping the r81 overview form (override on ~80 lesson pages for ~60 gains — a wash), (c) leave
  the r117 list + the r81 skip (the gold's per-series forms), adding only the NCEA1-solidified "We are learning about/to…" variant (17 pages —
  under the floor, so recorded here rather than shipped). Recommendation: (c) now; (a) only if Chris confirms the KB's label form is meant to
  overturn the eng-family overview convention the gold carries at 0.80 — that is a design-team call, not a converter inference.
- **→ DECIDED 2026-09-16 — D10-8 (Chris: Option B — leave the plain form; CLOSED, no round).** Pre-decision record: **The `alertPadding` activity class — KB 01F table vs the gold's majority — needs Chris, 2026-09-15 (session 6, Round 2 PICK; measured
  inline over every gold Standard activity box).** KB 01F's tag table maps `activity` + ID (text/workbook) → `<div class="activity
  alertPadding">` and 05B's example labels `activity alertPadding` "Standard text activity" — but 05B also says "follow the activity's own
  class set and simply append `dropbox`", and the gold ships plain `activity` **1773** vs `activity alertPadding` **411** (0.19) on the
  non-interactive boxes (`activity interactive` 2213 / `activity interactive alertPadding` 160 / `activity dropbox` 439). Claude ships plain
  `activity` on every text box (the r305/r308 `dropbox` modifier aside). Not a numbered constraint, not a CL, no 14 family rule — a
  component-doc mapping the gold contradicts 4:1, the same shape as the table form (05D vs 06 §6). Applying it corpus-wide would be a
  KB-over-gold override on ~1,700 boxes (skeleton ≈ −0.5pp, every plain-`activity` gold page down); leaving it keeps the gold form.
  Decision needed: (a) apply 01F's `alertPadding` to every text/workbook activity (a named override), (b) leave the plain form (the gold
  0.81 majority + 05B's "own class set"), (c) make it a KB constraint first and then apply. Recommendation: (b) until the KB says it is
  a rule, not an example — `alertPadding` is a padding choice the developer makes, with no writer-side signal.

- **→ DECIDED 2026-09-16 — D10-7 (Chris: Option A — MathML; KB 05A delta recorded; queued item 4, scoped to the 12 modules).** Pre-decision record: **WORD EQUATIONS ARE DROPPED — the form needs Chris, 2026-09-15 (session 5, Round 6 PICK; measured over the live docx files).** The V2 extractor
  has NO OMML path (`DocxExtractor.js` never reads `m:oMath` / `m:oMathPara`, which sit BESIDE the `w:r` runs in a `w:p`), so every Word equation
  is silently absent from the page: **12 WTs carry 329 equations** (MXDI102 154, MXDI301 69, PES1008 24, MXEX301 18, PES1007 17, MXFU302 15,
  MXFU401 12, MXDB301 6, MXDI201 6, CEDK401 6, MXDB202 1, SCCH301 1) and Claude ships **0** math markup on any page; the gold ships **2,052
  `<math>` (MathML) elements on 94 pages** (1822 bare `<math xmlns=…>`, 105 `display="inline"`, 66 `display="block"`). **THE CONFLICT:** KB 05A
  "MathJax / Equations" says the HTML carries **LaTeX** (`\( \)` inline, `\[ \]` block); the gold carries **MathML**; Chris's own PageForge V1.5
  `CLAUDE.md` records the settled production fact (2026-08-26, six live runs) that in MTK **MathML renders and LaTeX does not** and that "the
  downstream Convertor project turns it into `<math>` before the HTML ships" — two of Chris's instructions disagree on the form, so the loop
  does not pick one unattended. The V1.5 repo already holds tested converters for BOTH forms (`pageforge-site/js/omml-to-latex.js`,
  `omml-to-mathml.js` — the MathML one emits the gold's bare `<math xmlns>` form, measured against this corpus, and needs only a small
  plain-object XML tree under V2's regex extractor). Sizing: ~10 reachable modules / ~80 pages, 329 equations; body class `mathJax` rides
  along (the gold carries it per module — 115 pages / 20 modules — 0.92 precision where the page has math). Decision needed: (a) MathML (the
  gold + the V1.5 finding; name the KB delta), (b) LaTeX (the KB's letter; gate-neutral, does not render in MTK per V1.5), (c) both (MathML
  with the LaTeX source in a comment). Either way the extraction half is the same round.
- **→ DECIDED 2026-09-16 — D10-6 (Chris: Option C — exclude the eight from the comparison set, re-baseline; queued item 1, no regeneration).** Pre-decision record: **The CED REVISION-BRIEF modules (CEDR201/301/302, CEDT201–204, CEDW303 — 8 Inquiry modules, 8 pages scoring 8–20%) — a content-start
  finding, needs Chris, 2026-09-15 (session 5, Round 5 PICK).** Their `Writers Template + Media List.docx` is an EDIT BRIEF (`[Keep rest of
  content]`, `[Edit page: …]`, `[Remove video]`, ALL-CAPS Wonder/Explore/Connect/Act/Reflect phase lines) followed by the UNFILLED blank template;
  the live extractor's content start lands on the blank template's `[TITLE BAR]` and ships its placeholders (`Lesson # and title`, `Learning
  outcome/intention`) — the module's real content is either "keep what exists" (not in the WT) or sits before the template. The gold is the
  finished module (crumbs + 6 `inquiryPanel`s, KB 06 §3.4). Options: (a) treat the brief as the source (start at its first `[H1]`, derive the
  inquiry-cycle crumbs from the ALL-CAPS phase lines, ship the edit notes as Writers Notes — the pages would still lack the "kept" content),
  (b) leave them (the gate counts them at ~10%), (c) exclude revision briefs from the comparison set. The other 28 crumb-less Inquiry modules
  are six delimiter dialects (`[tab N]` 11 modules — most with no Claude dir; `[LESSON N]`-as-panels 5; `[page N]` 2; EXPFUN `[section N]` 4;
  TWH* new-tab/tab 5) — each a PanelsBuilder dialect round of its own (the r106/r189/r191/r192 pattern), sized 1–14 pages each.
- **→ DECIDED 2026-09-16 — D10-4 (Chris: Option C — keep the ban everywhere; CLOSED, no round; KB 14A/14B/14D to be edited to say never emitted).** Pre-decision record: **stickyNav `<head>` include (KB queue rank 10; 14A/14B/14D) — BLOCKED 2026-09-15, needs Chris.** Measured (`outputs/_measure_r323_stickynav.py` →
  `_r323_stickynav.json`): the gold carries `<script src="js/stickyNav.js" type="text/javascript" class="stickyNav"></script>` right after `<title>` on
  **1,504 of 2,385 pages (63%)**, per MODULE all-or-nothing (253 modules every page, 171 none, 30 mixed), ≥ 0.60 in 30 series (MX 0.92, ENGI/ENGR/HIS/
  AGH/MXDI/MXEO 1.00, ANZH 0.92, CED 0.96, HES 1.00, PHE 0.98 …) and 0 in others (TRR/PNR Bilingual 0/92, BLL 0.31, ARFUN 0, SC 0.05, HPRE 0/21);
  Claude 0 of 2,102. **The conflict:** the KB (14.1 Languages P1–4 every page + a "set up the stickyNav.js file" To Do note; CED Phase 5; 14.8 HPE)
  says ADD it, and the gold does so far more widely; Chris's own project instruction (`00_PROJECT_CONTEXT_AND_PHILOSOPHY.md` "stickyNav — a templating
  error that was copied across modules; never emit it"; `00_PHASE1_READINESS_BRIEF.md` "Never emit stickyNav.js — deliberate exclusion";
  `Emit_Templates.skeleton.never_emit`) says NEVER. Two of Chris's instructions disagree; the loop does not arbitrate that unattended. Gate-neutral
  (the `<head>` is outside every gate; a `cv2-note` is skeleton-inert). **Recommendation:** honour the KB in its three named families only (Languages
  P1–4, CED Phase 5, HPE — ≈ 33 modules, include + the KB's To Do note) and keep the ban everywhere else (the MX/ENG/HIS… copies are exactly the
  "templating error copied across modules" the philosophy names). Decision needed: (a) KB families only, (b) every ≥ 0.60 series, (c) keep the ban.


- **→ DECIDED 2026-09-16 — D10-5 (Chris: Option A — 05D's `table table-bordered` everywhere + `tableFixed` for two-column comparison tables; 06 §6 superseded; queued item 5, FULL regeneration).** Pre-decision record: **KB table form — 05D vs 06 §6 (a KB-internal conflict) — needs Chris, 2026-09-15 (session 5).** 05D (the component doc) says the general default is `<div class="table-responsive"><table class="table table-bordered">` with `tableFixed` for two-column comparison tables; 06 §6 (the Refresh element reference) shows `<table class="table noHover tableFixed">`. The gold: Standard `table-bordered` 0.51 (a tie), Inquiry 0.72, Fundamentals 0.69, Bilingual 0.86; `noHover` 0.09; `tableFixed` 0.30 and tied to column count (4+ cols 0.51, 2 cols 0.19), not to the KB's comparison-table guidance. Claude ships bare `table.table` (KB-correct wrapper `table-responsive` + `th` headers already). Decision needed: (a) apply 05D's `table table-bordered` default corpus-wide (a named override, skeleton ≈ −0.01pp in Standard / + in Inquiry & Fundamentals), (b) apply it only where the gold family agrees ≥ 0.60 (Inquiry / Fundamentals / Bilingual — a `Template_Modes.json`-style flag), (c) leave `table` bare. Recommendation: (b) — the KB rule where the gold confirms it, the tie left alone until the KB reconciles 05D with 06.

## Round log
- s10 · `/loop-decisions` (no engine round) · Chris answered ALL NINE pending decisions — recorded as D10-1…D10-9; the queue in the top banner · pages moved 0 · commit "Decisions from Chris 2026-09-16" · 2026-09-16 ≈15:30
- r0 · the ceiling instrument · shipped (tool + measurement, no converter change) · ceiling 91.6%, SCAFFOLD 49.941% = 54.5% of achievable · pages moved 0 · commit ca59d13
- r0b · KB amalgamation status (95 CLs, 92 constraints, 12 families; 11 queued rows) · shipped (document, no converter change) · pages moved 0 · commit 784305b
- r1 (engine r314) · KB constraint 43, the trailing upload box inside its activity (+ `dropbox` modifier) · SHIPPED 2026-09-15 · scaffold 49.941→50.031 (+0.090) · ≥50 +5 / ≥75 +1 · pages moved 60 (65 pages / 43 modules rebuilt) · 54.5%→54.6% of achievable · commit (see git log)
- r2 (engine r315) · KB constraint 28, the XHTML shell (lowercase doctype + ` />` voids) + the pairing-parser repair it exposed · SHIPPED 2026-09-15 · FULL regeneration, 2102 pages · converter change gate-neutral (ON == OFF under the repaired parser); skeleton RE-BASELINED 1939→1954 pairs, 50.031→50.289 (all of it the repair) · 54.9% of achievable · commit (see git log)
- r3 (engine r316) · KB constraint 79, the lesson's own bilingual title pair (two h1 spans, code stripped, Te Reo first in reoTranslate) · SHIPPED 2026-09-15 (finished after a power cut) · scaffold 50.289→50.345 (+0.056) · buckets EXACT · pages moved 40, all up (45 pages / 17 modules rebuilt of 179) · 55.0% of achievable · commit (see git log)
- r4 (engine r317) · KB constraints 45 + 90, the acks block's template form (acksTemplate wrapper, statements generated not typed) · SHIPPED 2026-09-15 · FULL regeneration, 394 pages · NAMED KB-over-gold override: scaffold 50.345→50.322 (−0.024, all on the 387 named pages; identical net of them), RAW-scope +0.062, every other gate EXACT · 54.9% of achievable (55.0% net) · commit (see git log)
- r5 (engine r318) · KB constraint 83, no loading="lazy" inside moving interactives · SHIPPED 2026-09-15 · FULL regeneration, 228 pages / 146 modules (2424 images) · gate-neutral, skeleton page-for-page identical, every gate EXACT · 54.9% of achievable · commit (see git log)
- r6 (engine r319) · KB constraint 89, learningSupport on every X-prefixed module's <html> · SHIPPED 2026-09-15 · scoped regeneration, 228 pages / 35 modules · gate-neutral, every gate EXACT · 54.9% of achievable · commit (see git log)
- r7 (engine r320) · the upload box keeps the writer's order around its button (text before the last marker → before the button) · SHIPPED 2026-09-15 (a small ship: 6 pages / 4 modules) · scaffold 50.322→50.325 (+0.003) · every other gate EXACT · c47/c95 DECLINED on measurement · 54.9% of achievable · commit (see git log) · **LOOP STOPPED — plateau (r318 0.000, r319 0.000, r320 +0.003)**
- r8 (engine r321) · the MTK / Te Reo Rangatira title source (Chris's decision 2) · SHIPPED 2026-09-15 · scoped regeneration, 24 pages / 14 modules · scaffold 50.325→50.368 (+0.043), cs exact +5, every other gate EXACT · 55.0% of achievable · commit (see git log)
- r9 (engine r322) · KB constraint 65 / CL-0082, the [MTKquiz] shell without the quiz content (Chris's decision 3) · SHIPPED 2026-09-15 · scoped regeneration, 30 pages / 23 modules (58-module family rebuilt) · scaffold 50.368→50.411 (+0.043; 15 up / 3 down NAMED KB-over-gold), ≥50 +2, ≥75 +1, RAW +0.022 · every other gate EXACT · new gate _verify_mtkquiz.cjs 61 shells defect 0 · 55.0% of achievable · commit (see git log)
- r10 (engine r323) · KB row 55, a button label never ends in a full stop (`Upload to dropbox.` → `Upload to dropbox`) · SHIPPED 2026-09-15 · FULL regeneration (the [button] family = the corpus), 212 pages / 82 modules · scaffold 50.411→50.411 (+0.000pp), cs exact 11360, every other gate EXACT · 55.0% of achievable · stickyNav BLOCKED (needs Chris) · commit (see git log)
- r11 (engine r324) · KB constraint 79, a `Lesson N` label is not a lesson title (the first real heading names the page; `continued` sub-pages inherit) · SHIPPED 2026-09-15 · scoped regeneration, 79 pages / 24 modules · scaffold 50.411→50.416 (+0.005; 11 up / 3 down named), ≥50 +1, every other gate EXACT · titles exact 528→550 · c67 DECLINED · 55.0% of achievable · commit (see git log)
- r12 (engine r325) · phase-scoped activity numbering on the Fundamentals pages (the r217/r266 follow-up: the phase ordinal as the activity-number prefix, the writer's bare digit over the scanner's collision letter) · SHIPPED 2026-09-15 · scoped regeneration, 17 pages / 17 modules · scaffold 50.416→50.435 (+0.019; 12 up / 5 down named), every other gate EXACT · number matches 66→178 · 55.1% of achievable · commit (see git log) · **LOOP STOPPED — plateau (r323 0.000, r324 +0.005, r325 +0.019)**
- s4-r1 (engine r326) · a call-to-action button is an anchor (the KB's universal button form: a plain `[button]` ships inside `<a href target=_blank>` — the writer's hyperlink kept, else a blank href + one To Do note; reveal-type labels stay the gold's JS button) · SHIPPED 2026-09-15 · FULL regeneration, 713 pages / 286 modules · scaffold 50.435→50.492 (+0.057; 675 moved, 210 up; dips NAMED = scorer repeat-collapsing, identical net of the changed pages), ≥50 −1 named, ≥75 +3, body 192→191 · every other gate EXACT · bare buttons 1,800→338, 285 lost links recovered · 55.1% of achievable · commit (see git log)
- s4-r2 (engine r327) · a multi-word ALL-CAPS header title renders in sentence case (the KB's title-casing rule: macrons kept, code tokens kept, single token untouched, one red flag quoting the original) · SHIPPED 2026-09-15 · scoped regeneration, 47 pages / 15 modules · gate-neutral, every gate EXACT (scaffold 50.492, 0 moved) · all-caps titles 47→0, titles exact 550→567 · 55.1% of achievable · commit (see git log)
- s4-r3 (engine r328) · a submission button keeps its full 'Go to' label (KB constraint 55's label half: bare `Quiz` / `Portfolio` / `Dropbox` → `Go to quiz` / `Go to portfolio` / `Go to dropbox`, `Upload to Dropbox` in BLL / LS / HPE) · SHIPPED 2026-09-15 · scoped regeneration, 47 pages / 40 modules · gate-neutral, every gate EXACT (scaffold 50.492, 0 moved) · bare-noun labels 84→0 · 55.1% of achievable · commit (see git log)
- s4-r4 (engine r329) · `[trigger engagement]` is a marker, not a button (KB constraint 43: the dropbox-trigger condition; the phantom `button engagementTrigger` journal button no longer ships) · SHIPPED 2026-09-15 · scoped regeneration, 60 pages / 42 modules · scaffold 50.492→50.496 (+0.004; 57 up / 3 down, dips named), every other gate EXACT · phantoms 99→28 · 55.1% of achievable · commit (see git log) · **LOOP STOPPED — plateau (r327 0.000, r328 0.000, r329 +0.004)**
- s5-r1 (engine r330) · the bilingual section id is the activity number, not a heading (KB 07B: the writer's bare `[H1] N.M` → `number="N.M"` on the boxed section, decimal preferred; the phantom `<h3>1.1</h3>` pair no longer ships) · SHIPPED 2026-09-15 · scoped regeneration, 25 pages / 7 modules · scaffold 50.496→50.536 (+0.040; 17 up / 4 down, dips named), ≥50 +3, every other gate EXACT · phantoms 234→0, unnumbered boxes 72→0 · 55.2% of achievable · commit (see git log)
- s5-r2 (engine r331) · a bilingual section box's headings render at the KB's activity level (KB 07B: the writer's `[H2]` inside a TRR section box → h3; PNR excluded by data) · SHIPPED 2026-09-15 · scoped regeneration, 21 pages / 5 modules · scaffold 50.536→50.558 (+0.022; 18 up / 3 down, dips named), ≥50 +1, every other gate EXACT · TRR in-box h2 155→0 · alertImage sidebar DECLINED, table-class KB conflict → needs Chris · 55.2% of achievable · commit (see git log)
- s5-r3 (engine r332) · the empty footer → the KB's page-position form (KB 01B: a no-evidence registry footer value falls back to overview next+home / lesson all three / final prev+home; fundamentals-nav home) + the BLL1 registry footer class (inquiry-nav, gold 0.85) · SHIPPED 2026-09-15 · scoped regeneration, 239 pages / 130 modules · scaffold 50.558→50.827 (+0.269; 185 up / 22 down, dips named), ≥50 +10, ≥75 +4, every other gate EXACT · empty footers 141→0 · 55.5% of achievable · commit (see git log)
- s5-r4 (engine r333) · a right-hand alert is a side column; rhs / summary are not classes (KB 05B: `[alert box rhs]`-family boxes pair as the right sibling of the content column they follow — the KB activity sidebar alertActivity after an activity box, alert top after prose; `[alert box lesson summary]` → the plain alert) · SHIPPED 2026-09-15 · scoped regeneration, 143 pages / 53 modules · scaffold 50.827→50.893 (+0.066; 73 up / 14 down, dips named), ≥50 +5, compare_structure exact +15 / EXTRA −15 / missing +2 NAMED, every other gate EXACT · alert rhs 150→0, alert summary 98→0, 92 side columns · 55.6% of achievable · commit (see git log)
- s5-r5 (engine r334) · the activity box's title heading is h3 (KB 01F `activity_heading`; a writer's in-box `[H3]`/`[H4]` carried the body shift and the re-leveller skips activity subtrees — a post-pass pins the box's first-child heading to h3; PNR excluded) · SHIPPED 2026-09-15 · scoped regeneration, 226 pages / 73 modules · scaffold 50.893→51.060 (+0.167; 150 up / 20 down, dips named), ≥50 +17, every other gate EXACT · activity titles at h4/h5 590→0 · 55.7% of achievable · scoped ship #8 — full backstop DUE · commit (see git log)
- s5-full · the FULL-SHIP BACKSTOP after r334 · 416 dirs regenerated, 0 stale, manifest IDENTICAL (0 pages) · baselines re-snapshotted unchanged · ledger record-full (counter 0) · 2026-09-15 19:43
- s5-r6 / s6-r1 (engine r335) · the `[Engagement quiz button]` is the KB's external quiz link button (01F; c65 label `Go to quiz`, blank publish-time href, ONE To Do note with the writer's link) · BUILT + PROBE-PROVEN in session 5 (OFF = disk 2102/2102; ON = 28 pages / 28 modules), SHIPPED OFF at Chris's stop, **flipped ON + SHIPPED 2026-09-15 (session 6)** · scoped regeneration, 28 pages / 28 modules · scaffold 51.060→51.078 (+0.018; 28 moved — 19 up / 9 down, every mover in the affected set, pp-sum +35.31; the 9 dips ≤ 0.33pp NAMED = the scorer's alignment artefact on pages whose gold box has no inner row > col-12 (OSBY501_5, OSSC501_5, OSSC301_3, OSAI201_3, OSOH501_5, OSSC401_4, ARFUN01_0, HPFUN401_0, ARFUN02_0 — the element sequence h3 → p → a → div.button is now the gold's)), ≥50 1066→1066, every other gate EXACT · engagementTrigger divs 28→0 · 55.8% of achievable · scoped ship #1 since the r334 full · commit (see git log)
- s6-r2 (engine r336) · the Fundamentals overview `#module-code` chip is a family convention (a `Style_Anchor_Registry.json` correction: ARFUN / ENFUN / TEFUN / MXFUN0 drop the chip the golds never ship, SSFUN gains the chip its golds ship 5/6) · SHIPPED 2026-09-15 · scoped regeneration, 31 pages / 31 modules · scaffold 51.078→51.078 (+0.000; 31 moved — 9 up / 22 down, every mover in the affected set, pp-sum +0.62; the 22 dips ≤ 0.32pp NAMED = the scorer's alignment artefact: the phantom chip's `h1` line had been coincidentally matching the gold's second (Te Reo) `h1`, which Claude never ships — the element sequence is now the gold's; SSFUN07_0_0 +2.52 the largest gain), ≥50 1066→1066, ≥75 200→200, every other gate EXACT · chips = the family form on 30/31 · 55.8% of achievable · scoped ship #2 since the r334 full · sub-heading level / heading ladder / paddingR / p⇐h5 DECLINED on measurement; alertPadding → needs Chris · commit (see git log)
- s6-r3 (engine r337) · numbered steps are a semantic `<ol>`, never `<p>1. …</p>` (KB constraint 42: a run of consecutive numbered paragraphs — the writer's typed count or the extractor's all-"1." Word-list marker inside a built accordion panel — becomes one `<ol>`, `start=N` when needed; a full-page post-pass at the EmojiStrip seam, the built widgets that own their shape verbatim) · SHIPPED 2026-09-15 · scoped regeneration, 24 pages / 24 modules (a small ship under the 20-page floor, the r320 precedent) · scaffold 51.078→51.079 (+0.001; 3 moved — 2 up / 1 down, every mover in the affected set, pp-sum +1.89 (XLP05_5_0 +2.01, MXFU402_3_0 +0.09; PES1001_5_0 −0.21 NAMED = its new <li>s keep the writer's bold lead the gold strips inside the list, the r164/r165 bold class — the <ol> itself now matches); the other 21 changed pages sit inside collapsed accordion widget markers and cannot move the scaffold), every other gate EXACT · numbered-paragraph runs 26→0 · 55.8% of achievable · scoped ship #3 since the r334 full · c41 captions declined (editorial), c75 untagged buttons → next PICK · commit (see git log) · **LOOP STOPPED — plateau (r335 +0.018, r336 +0.000, r337 +0.001)**
- s7-r1 (engine r338) · an external destination is the KB's `externalButton` (KB 05D Internal/External: a `[button]` whose URL points at an outside website ships `<a href target=_blank><div class="externalButton">`, Te Kura's own systems — drive / docs / forms / LMS / sharepoint / vimeo player — stay `button`; + constraint 75's "Go to website" / "Go to video" for a URL-only button that had fallen to the journal default) · SHIPPED 2026-09-16 · scoped regeneration, 134 pages / 71 modules · scaffold 51.079→51.102 (+0.023; 60 moved — 37 up / 23 down, every mover in the affected set, pp-sum +44.21 (XMES201_5_0 +18.96, XGF9003_1_4 +10.81 — crosses ≥75, AGH1004_2_0 +5.61, HES1007_9_0 +4.85 …); the 23 dips ≤ 5.17pp are NAMED and of two kinds: (a) the 11 gold `button`s on an external host — the KB-over-gold sites (ANZH404_4_0 −2.92 'Source A/B/C', MXFL401_5_0 −1.18, MXEO201_4_0/_8_0 −0.94/−2.00, ENGC202_5_0 −2.68), (b) the scorer's repeat-collapse / coincidental-match artefact (HIS1007_3_0 −5.17 and HIS1005_9_0 −1.56 each gain +4 gold-matched lines on the uncollapsed multiset — a uniform `┌ N× repeated` run of `a > div.button` became a mixed run; HIS1007_1_0 −1.37 crosses <50: its `[video link]`s ship as buttons the gold embeds, and their `div.button` lines had been matching the gold's journal `div.button`s by coincidence)), ≥75 +1, ≥50 −1 NAMED, every other gate EXACT · external-host div.button 304→41 · 55.8% of achievable · scoped ship #4 since the r334 full · the untagged standalone-hyperlink candidate DECLINED (gold buttons it at 0.07) · commit (see git log) · **plateau window restarts (r338 +0.023)**
- s7-r2 (engine r339) · a `[button]` whose destination is a video is the embedded video (the writer's "[Button] Play video" + "[video link] URL", "[Button: youtube-url]", the "[embed this video with a play button]" + `[link] URL` instruction brackets → the standard `videoSection` embed instead of an anchored button; a real label keeps the button; the gold embeds 0.90 of 109 sites, nearest KB rule 01E) · SHIPPED 2026-09-16 · scoped regeneration, 30 pages / 14 modules · scaffold 51.102→51.112 (+0.010; 21 moved — 16 up / 5 down, every mover in the affected set, pp-sum +20.26 (HIS1005_9_0 +5.73, HIS1005_5_0 +4.43, HIS1002_1_0 +3.12, HIS1007_4_1 +1.27 …; HIS1007_1_0 49.48 → 50.17 re-crosses ≥50 — the r338 named crosser HEALED, its `[video link]` buttons are now the gold's embeds); the 5 dips ≤ 0.85pp are NAMED: MXEX401_5_0 −0.85 and TWHA905_0_0 −0.26 = the gold's editorial video substitutions (the writer's youtube id is absent from the gold page — MXEX401 one of two, TWHA905 five of eight on its 16-embed single-file page), HIS1005_7_0 −0.33 / MXFU401_1_0 −0.27 / TWHK903_0_0 −0.02 = the scorer's alignment artefact on a strictly closer element sequence (every embedded id is the gold's own embed on the paired page)), ≥50 +1, cs exact +3, every other gate EXACT, nothing named · button-family video sites 54→0, 36 new embeds · 55.8% of achievable · scoped ship #5 since the r334 full · the activity `interactive` modifier DECLINED (no Claude-visible signature ≥ 0.60) · commit (see git log)
- s7-r3 (engine r340, finished in session 8) · a standalone `[link]`-family paragraph whose text is nothing but a video url is the embedded video (the writer's "[link] https://www.youtube.com/watch?v=…" on its own line, under an "[embed video with image and play button]" instruction or after a "watch the video" sentence → the standard `videoSection` embed instead of the r76 "Go to video" button, and the url-less `[video]`/`[embed]` element takes the line's url instead of printing a "no URL" red flag; a titled or prose link keeps its anchor / button; the gold embeds 0.90 of the url-only sites, nearest KB rule 01E) · SHIPPED 2026-09-16 · scoped regeneration, 19 pages / 9 modules · scaffold 51.112→51.112 (−0.000 at 3 dp; 51.1124→51.1120; 5 moved — 2 up / 3 down, every mover in the affected set, the 3 dips NAMED: ANZH303_6_0 −1.41 and HIS1008_5_0 −0.40 = the gold's own embed inside a tabs / carousel widget the writer never tagged (A1), ENFUN01_0_0 −0.58 = the repeat-collapse artefact; +0.0006 net of the two A1 pages), ≥50 1066 / ≥75 201 / ≥90 15 EXACT, cs exact +1, every other gate EXACT · video-href buttons 46→19 (27 new embeds, 17 phantom notes gone) · 55.8% of achievable · scoped ship #6 since the r334 full · commit (see git log) · **plateau window: r338 +0.023 · r339 +0.010 · r340 −0.000 (two under 0.02)**
- s8-pick2 (no engine round) · the Round 2 PICK measured five candidates — `ul ⇐ ol` (Claude KB-correct, c42; gold ol 0.84; the AGH LI-list `ul` is one series at 13 pages), the lesson-menu label variants (c23 — gold split by series, h5 0.35 of the residue; BLOCKED for Chris; the one solidified variant is 17 pages), the Inquiry `body.inquiry` token (downstream of the crumb-less dialect rounds), the Bilingual `audioImage` widget (decision 5), the 3-vs-2 `<p>` repeat (editorial) · NOTHING ≥ 20 derivable pages left · **LOOP STOPPED — EXHAUSTION (§4)** · 2026-09-16 ≈10:10
- s9-r1 (engine r341) · a writer's tag typed in a NON-STANDARD RED is still a tag (the engine scanned only `ff0000` / `ee0000` runs for tags; the HIS writer's `ed0000`, ENGFUN02's `fa0000` and Word's Dark Red `c00000` shipped every tag as literal text — 598 brackets on 30 modules; a run in the red hue band now counts as red when it carries a bracket or continues an open one, never on bare content; + the r299 weave's parenthesised-tail definition form) · SHIPPED 2026-09-16 · FULL regeneration (the backstop, ledger 0), 76 pages changed + 10 added − 2 removed / 23 modules · scaffold 51.112→51.133 (+0.021; 51.1120→51.1325; pairs 1954→1962; 39 moved — 20 up / 19 down, pp-sum +70.06, every mover in the affected set; per module HIS1005 +9.24 (the gold's exact 15-page set), ENGFUN02 +15.05; the dips NAMED: the OS* clickDrop BUILDS replacing coincidentally-matching dumps (RAW up), HIS1006's renumbering, HIS1005_2_0 / TRR109_5_0 A1 substitutions, ARFUN05 alignment), ≥50 1066→1073 (+7), ≥75 201→200 (−1 NAMED OSGM501_5_0), ≥90 15, cs exact +103 (EXTRA +4 / missing +15 = HIS1005's +133 matched pool, named), clean 97.81→98.91%, **leak 288/46→26/23**, every other gate EXACT · 55.8% of achievable · commit (see git log) · **plateau window restarts: r341 +0.021**
- s9-r2 / s11-r0 (engine r342) · a writer's MEDIA tag typed as a HYPERLINK is still a tag (`[audio 1]` in the link blue linked to its Drive / SharePoint sound file — the r341 seam on `w:hyperlink` runs whose bracket head is a data-listed media word, fenced by the head list (the ~230 hyperlinked phonics WORDS stay content), `exclude_words` (the XDLS `[Audio Animation N:` CS briefs) and `link_target_match` (a media-file carrier — BLL262's tahurangi PAGE stays a link); its own words become the caption; a tag member's bracket line or link keeps the hand-off box + `.txt` entry; a bare `[audio button]` never invents `Go to your journal`) · built + OFF-proven s9, gap 2 decided by measurement + 3 fences s11 · SHIPPED 2026-09-16 · FULL regeneration (ledger 0), 248 pages / 147 modules, 0 added/removed · scaffold 51.133→51.129 (−0.003; 51.1325→51.1291; 41 moved — 16 up / 25 down, pp-sum −6.76, every mover in the affected set; every dip ≤ 2.21pp = the recognised `[audio]` shipping the standing audio element where the gold builds the per-word wordDrag / audioButton widget (r300 non-derivable) and the OFF literal line's coincidental `<p>` match), ≥50 1073 EXACT, ≥75 200→198 (−2 NAMED BLL217_1_0 / BLL126_1_0), ≥90 15, cs 11482/175/608 EXACT, **body 191→180 IMPROVED**, clean 98.91% / leak 26/23 EXACT, every other gate EXACT · hand-off boxes +7 rescued / 0 lost / 1 built (BLL253 clickDrop, defect 0) · 55.8% of achievable · commit (see git log) · **plateau window: r341 +0.021 · r342 −0.003**
- s11-r1 (gate-config r343, D10-6) · the eight CED revision-brief modules (CEDR201 / CEDR301 / CEDR302 / CEDT201 / CEDT202 / CEDT203 / CEDT204 / CEDW303) leave every scored gate (`compare_exclusions.txt` + `_corpus.gate_mods()`; the eight stay in the corpus, regenerated with their families) · SHIPPED 2026-09-16 · no regeneration, no engine change · RE-BASELINE: pairs 1962→1955 (exactly the seven paired briefs, 0 pages score-moved), scaffold 51.129→51.265 (+0.135pp = a POPULATION change, never a gain), buckets 1073/198/15 EXACT, cs 11469/175/607, clean 2080/2103 = 98.91%, leak 26/23, body 180 · ceiling 91.6→91.9% · 55.8% of achievable · commit (see git log) · plateau window unchanged (r341 +0.021 · r342 −0.003)

**Next session starts with:** (1) Health check (`verify_after_transfer.sh` — its page count is now 2110), `git status` in pageforge-site: expect HEAD bb56efc
+ EXACTLY four modified files (`app/js/ContentConverter.js`, `app/js/DocxExtractor.js`, `data/Emit_Templates.json`, `data/Input_Doc_Rules.json`) = Round 2
(engine r342) in progress — NEVER git checkout / restore them; both data flags are `enabled: false` (the corpus on disk is the proven r341 state).
(2) Read "Session 9 · Round 2 (engine r342) — IN PROGRESS at the stop" + the Round 2 PICK, flip `hyperlinked_tag_runs.enabled` and
`embedded_member_text.enabled` to `true`, and resume at PROVE: settle gap 2 (the media embedded lead — option (a) `MediaBuilder.media` folds the bracket-line
words into the element's own text behind a data flag; option (b) for the `[Audio Animation N:` CS-animation sites), re-run `_r342_probe_run.sh` (OFF must
= disk 2110/2110), explain every ON-changed page, word-loss check, scoped §0b regeneration, gates, finalise, commit — or, after three failed repairs of
gap 2, toggle OFF, prove identity, record BLOCKED and move on. (3) Then continue the loop under the standing §7 kickoff; the candidates left after r342 are
recorded in the r342 PICK (plain-black tag brackets 195 / 98 modules — thin; the AGH1006 widget-release leak; the bilingual-cell `[Item N] [Image]` r167
class) and every KB row ≥ 20 pages stays BLOCKED on Chris's recorded decisions (stickyNav, equations, c23 label form, alertPadding, table form, CED
briefs, decisions 1 / 4 / 5) — never re-asked. The plateau window after r341 (+0.021pp) is open at one round.
