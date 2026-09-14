# LOOP_STATE.md — position of the autonomous PageForge loop (LOOP__Autonomous_Rounds.md)

**Session 1 started:** 2026-09-14 (Claude Code on Chris's Windows machine). Budget: 10 rounds or 6 hours.
**Session 2 started:** 2026-09-14 (Claude Code, same machine). Budget: 12 rounds or 10 hours. Resumed Round 1 (engine r314) from session 1's recipe (tree PASS, HEAD 763e036) and shipped it.
**Authority carried by the kickoff message:** `REGENERATE CORPUS` for every round, scoped by CLAUDE.md §0a/§0b.

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
- Remaining KB queue (§D): c65 quiz omission (56 shells — decision 3, NEXT), c55 full stops (420 buttons, gate-neutral), stickyNav (33 modules,
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
(none yet)

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
