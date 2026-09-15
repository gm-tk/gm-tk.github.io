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
stay open (not re-asked); the loop works the derivable queue that needs no decision.

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
- **c67 `overflowYScroll scroll="500"` on long panels — DECLINED 2026-09-15 (Round 11 PICK).** Measured over every gold accordion / tab panel
  (4,932 panels): the class rides 25 accContent + 6 tab-pane + 8 other panels on 27 pages (HIS1004 ×9), and its share is ≤ 0.05 in EVERY
  length bucket (accContent 1–2k chars 9/164, 2–4k 8/158, 4–8k 4/186, 8k+ 2/178; tab-pane 2–4k 4/97) — panel length does not predict it, no
  other discriminator exists. Below the r182 solidify floor in every group.
- **c47 / CL-0095 — the duplicate body heading on a lesson page (Round 7 candidate, measured 2026-09-15 03:30, `outputs/_measure_r320_dupheading.py`
  → `_r320_dupheading.json`).** 88 cases / 77 pages where a Claude body heading equals the header title (exact, or after a `Lesson N` / label
  prefix). (a) The `Lesson N`-PREFIXED opening duplicate: gold drops 11/11 first-heading cases (12 with one later) — a 100% convention, both
  authorities agree — but only **12 pages**, under the loop's 20-page floor. (b) The EXACT duplicate: 70 cases, but 41 of them only match because
  Claude's TITLE is wrong (TRR108/114/203/304 `Finished!` — the MTK title-source defect, a c79 sub-mechanism); among the 14 first-heading cases
  where both sides carry the same title the gold drops 8 (57%) and keeps 6 (XDLS903 `Poi`, ENGI101 `Being Frank`, ENGJ101, MXEO202, OSSM301 …);
  corpus-wide the gold KEEPS an exact duplicate on 111 lesson pages. Share 0.57 < 0.60 and a signature that misfires on wrong titles → DECLINED
  under §2/§3 (the r182 solidify rule). c47 is pre-ledger documentation, not a locked admin decision, so the KB-over-gold override was not
  invoked for a 21-page dip. Re-open (a) as part of a later heading round once the TRR title-source class lands, or if Chris says the KB's
  universal wording should be applied regardless of the gold (then: strip + drop the opening duplicate on lesson pages, strip-only on the overview).

## Blocked classes
- **stickyNav `<head>` include (KB queue rank 10; 14A/14B/14D) — BLOCKED 2026-09-15, needs Chris.** Measured (`outputs/_measure_r323_stickynav.py` →
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


## Round log
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
