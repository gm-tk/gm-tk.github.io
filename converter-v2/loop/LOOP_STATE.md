# LOOP_STATE.md — position of the autonomous PageForge loop (LOOP__Autonomous_Rounds.md)

**Session 1 started:** 2026-09-14 (Claude Code on Chris's Windows machine). Budget: 10 rounds or 6 hours.
**Session 2 started:** 2026-09-14 (Claude Code, same machine). Budget: 12 rounds or 10 hours. Resumed Round 1 (engine r314) from session 1's recipe (tree PASS, HEAD 763e036) and shipped it.
**Authority carried by the kickoff message:** `REGENERATE CORPUS` for every round, scoped by CLAUDE.md §0a/§0b.

## Session 2 — IN PROGRESS (started 2026-09-14 23:21 NZST; hard stop 09:21 NZST 2026-09-15 or 12 rounds)
- **Round 1 (engine r314) SHIPPED** (commit f1f4de2) — KB c43, the trailing upload box inside its activity.
- **Round 2 (engine r315) SHIPPED** (commit 3528986) — KB c28, the XHTML shell, FULL regeneration + the `anchor_compare` pairing-parser repair.
- **Round 3 (engine r316) SHIPPED 2026-09-15** — KB c79, the lesson's own bilingual title pair (two h1 spans, code stripped, Te Reo first in
  reoTranslate modules); scoped regeneration of 179. **A power cut interrupted this round** after the engine edits and before the rebuild; on
  restart the tree was verified (git fsck, every JSON, corpus == r315 manifest), the one casualty — `reference/tests/batch_results.json`, a 48-byte
  NUL run — was repaired with the corrupt copy kept, and the migration checksum manifests (`_MIGRATION/CHECKSUMS__*.txt`, a r313 snapshot) are now
  refreshed at each commit (old copies `*.pre-r316.bak`). Commit: see the round log.
- **Corpus / engine state:** the r316 scoped regeneration on top of r315 (45 pages / 17 modules changed, 0 stale); content manifest, fast-loop
  baseline, feature index, ledger (scoped #1 since the r315 full), gate_baseline.json all refreshed; skeleton state `outputs/_r316_sk_final.json`
  FRESH. Build 260618.87.
- **MEASUREMENT RULE FROM ROUND 2 ON:** `reference/tests/anchor_compare.py` is void-aware now. Any comparison across round 315 must use the
  repaired tool on both sides; the r313/r314 skeleton state files were scored with the void-blind pairing (1939 pairs) and are NOT comparable
  page-for-page to `_r315_sk_final.json` (1954 pairs) — compare against r315 from here on.
- **If this session is interrupted:** everything describes round 316 as shipped; resume at Round 4 (PICK). Rounds 1 and 3 were gate-moving,
  Round 2 gate-neutral: Round 4 may be a gate-neutral KB row (c83 lazy / c89 learningSupport) but Round 5 must move a gate again.

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
- Round 4: NOT STARTED. Queue (§D of the status file, KB rows first): c90/c45 acks (413 pages, NAMED override, full regen, skeleton-visible),
  c83 lazy in moving widgets (243 pages, gate-neutral), c89 learningSupport (228 pages, gate-neutral), c47/c95 Lesson-N strip (89 pages), c79's
  remaining source-order/fallback mechanisms (141 fallback pages — size per mechanism), c65 quiz omission (56), c55 full stops (420 buttons),
  stickyNav, c67; then the dashboard's top gold-matching class. Plateau guard: at most two gate-neutral rounds in a row.

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
(none yet)

## Blocked classes
(none yet)

## Round log
- r0 · the ceiling instrument · shipped (tool + measurement, no converter change) · ceiling 91.6%, SCAFFOLD 49.941% = 54.5% of achievable · pages moved 0 · commit ca59d13
- r0b · KB amalgamation status (95 CLs, 92 constraints, 12 families; 11 queued rows) · shipped (document, no converter change) · pages moved 0 · commit 784305b
- r1 (engine r314) · KB constraint 43, the trailing upload box inside its activity (+ `dropbox` modifier) · SHIPPED 2026-09-15 · scaffold 49.941→50.031 (+0.090) · ≥50 +5 / ≥75 +1 · pages moved 60 (65 pages / 43 modules rebuilt) · 54.5%→54.6% of achievable · commit (see git log)
- r2 (engine r315) · KB constraint 28, the XHTML shell (lowercase doctype + ` />` voids) + the pairing-parser repair it exposed · SHIPPED 2026-09-15 · FULL regeneration, 2102 pages · converter change gate-neutral (ON == OFF under the repaired parser); skeleton RE-BASELINED 1939→1954 pairs, 50.031→50.289 (all of it the repair) · 54.9% of achievable · commit (see git log)
- r3 (engine r316) · KB constraint 79, the lesson's own bilingual title pair (two h1 spans, code stripped, Te Reo first in reoTranslate) · SHIPPED 2026-09-15 (finished after a power cut) · scaffold 50.289→50.345 (+0.056) · buckets EXACT · pages moved 40, all up (45 pages / 17 modules rebuilt of 179) · 55.0% of achievable · commit (see git log)
