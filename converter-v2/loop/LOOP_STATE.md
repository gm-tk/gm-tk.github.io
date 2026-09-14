# LOOP_STATE.md — position of the autonomous PageForge loop (LOOP__Autonomous_Rounds.md)

**Session 1 started:** 2026-09-14 (Claude Code on Chris's Windows machine). Budget: 10 rounds or 6 hours.
**Authority carried by the kickoff message:** `REGENERATE CORPUS` for every round, scoped by CLAUDE.md §0a/§0b.

## >>> STOPPED 2026-09-14 23:15 NZST on Chris's instruction ("STOP THE LOOP NOW") <<<
- **Where the loop is:** Round 1 (= engine round 314), class = KB constraint 43 (the trailing upload
  box lands OUTSIDE its activity box). Steps TRIANGULATE and MEASURE are DONE; step IMPLEMENT was
  designed and written as a splice script but **NEVER APPLIED**. No engine file, no data file and no
  corpus page was modified in this session after Round 0b. There is no round-314 toggle to switch off
  because the round-314 code is not in the engine.
- **Corpus / engine state:** exactly the round-313 regenerated corpus + commits 71006dc (equation parser),
  ca59d13 (Round 0), 784305b (Round 0b). `git status` in `pageforge-site` was clean before this stop commit;
  the only files added by the stop commit are this LOOP_STATE.md mirror and the Round 1 artefacts below.
- **Shipped this session:** Round 0 (ceiling instrument) and Round 0b (KB amalgamation status). Both committed.
- **Declined this session:** none. **Blocked:** none.
- **Uncommitted anywhere:** nothing in `pageforge-site` after the stop commit. Outside git
  (`CONVERTER_V2/outputs/`, the dev harness, never in the repo): the Round 1 probe + results + the
  unapplied splice — all mirrored into `pageforge-site/converter-v2/loop/` and committed.
- **Round 1 artefacts (mirrored in `converter-v2/loop/`):** `_measure_r314_dbxplace.py` (the measurement
  probe), `_r314_dbxplace.json` + `_r314_affected.txt` (its results: 121 affected modules, 0 ENFUN, 55 BLL),
  `_r314_bundledump.cjs` (diagnostic), `_r314_splice_UNAPPLIED.py` (the complete, anchored edit script for
  Emit_Templates.json + ContentConverter.js + InteractiveBuilder.js — reviewed, not run).
- **Safe to close:** yes. Resume by reading the "Round 1 resume recipe" section below.

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
- Round 0b (KB amalgamation audit): DONE 2026-09-14, commit 784305b — `KB_AMALGAMATION_STATUS.md` at the folder
  root (mirrored in `converter-v2/loop/`); facts in `outputs/_r0b_kbfacts.json`, `_r0b_kbsignatures.json`,
  `_r0b_kbsignatures2.json`. Census + dashboard refreshed (coverage 50.8%).
- Round 1 (= engine round 314): TRIANGULATED + MEASURED; IMPLEMENT written but NOT applied. **STOPPED** (above).

## The ceiling (Round 0 result — quote it in every report)
- Paired population 1880 pairs = the gate's 1939 minus 59 unmeasurable (13 TRR modules with a Media-List-only
  parsed file — 11 of them have an unparsed Writers Template.docx, TRR104/105 have none — plus TRR115/ENGJ403
  with no parsed file). No-source share, scaffold scope: raw 11.1% -> net 8.4%.
- **CEILING (scaffold) 91.6%** (loose upper bound 94.2%); full-scope ceiling 87.1%.
- **r313 SCAFFOLD 49.941% = 54.5% of achievable (band 53.0-54.5%)**; RAW 34.430% = 39.5% of achievable.
- Formula: % of achievable = skeleton mean / ceiling, ceiling = 1 - net no-source share (per-page mean).

## Round 1 PICK (LOOP §3 step 1 — written before any code)
- **Class:** the writer's dropbox marker inside an activity produces round 308's "Upload to dropbox" button
  OUTSIDE the activity box (own row after the box closes); the gold keeps it INSIDE the box and marks the box
  `activity dropbox` (KB constraint 43). Round 305's postpass only marks a box whose own span holds the button
  (its documented 17% recall), so the class costs two skeleton lines per activity: the button position and the
  modifier.
- **Authority (§1b):** 1 = KB constraint 43 (universal; BLL carve-out — never on BLL) + 14.11; 3 = gold
  (non-BLL gold marks 717 of 816 such activities = 88%; BLL gold marks 32 of 512 = the carve-out).
- **Triangulated:** XMES101 2D (WT `[Activity 2D] ... [body] Upload to dropbox ... [microphone, camera and video
  dropbox buttons] [End page]` -> gold `<div class="activity dropbox" number="2D">` with the button as the box's
  last child (gold XMES101.02.html L289-311) -> Claude closes the box after the clickDrop and ships the button +
  To Do note in a new row (XMES101_2_0.html L233-262)); XTAS101 1C/1E/1F/1G; XMES101 3A.
- **MEASURED (`outputs/_measure_r314_dbxplace.py` -> `_r314_dbxplace.json`, `_r314_affected.txt`):** every
  upload/dropbox/portfolio button on both sides classified inside / trailing / free against the depth-balanced
  activity span, trailing cases cross-checked against the Writers Template. GOLD: non-BLL inside 702 / trailing 12
  / free 19 (96% inside); BLL inside 1024 (100%). CLAUDE: non-BLL inside 127 / trailing 166 / free 212; BLL inside
  214 / trailing 196 / free 2. The 166 non-BLL trailing buttons sit in 65 modules; WT-marker-inside-activity =
  True 75 (22 modules: XMES203 10, XTAS102 9, XDLS912 7, XMES103 7, XTAS101 7, XMES101 5, XMES201 5, XTAS103 4,
  ENGS102 3, XDLS901 3, ...), False 30 (the marker is after the activity's end — current output correct),
  None 61 (activity id not resolvable in the WT). Affected list = 121 modules (0 ENFUN, 55 BLL). Gap between
  box close and button: median ~536 chars, so the button is the box's immediate follower.
- **Mechanism (designed, NOT applied — `_r314_splice_UNAPPLIED.py`):** data flag
  `activity_wrapper.owned_activity_keeps_trailing_dropbox` {enabled, env ACTDBXINSIDE_OFF, max_lookahead 120};
  at the bundle-owner close site in ContentConverter (after `#goJournalTail`, before `emit(stack.pop().close);
  breakRow();`) a new `#dropboxTailHold(bodyItems, i, bundles, it.consumedBy, tpl, renderedHeading)` walks
  forward with the auto-close boundary semantics (skip the owner's members / consumed items / blank lines; black
  text, tables, non-boundary tags = content; a stray non-activity CONTAINER_CLOSE = the widget's own end tag,
  flagged `_dbxStrayCloser`; heading <= rendered_heading_max, activity_close_before directives/tags, an
  activity closer, PAGE_BOUNDARY, SECTION_MARKER, or a foreign non-dropbox bundle = stop, no hold); holds when
  the first foreign bundle is a freed upload-box bundle (`type === "dropDown"`, canonTag !== "activity",
  activityOwner === undefined, activityId === null — the loop's own isNewActivity test inverted — and
  `InteractiveBuilder.UploadBoxCandidate(b, ddTpl)`, round 308's scan factored into `#ddUploadBoxScan` and
  promoted public so scanner/builder/holder cannot drift). On hold: `markContent()`, an info note, and the frame
  stays on the stack; the dropbox bundle renders inside via the non-owner path; autoClose / the page-end drain
  closes the box; the r305 postpass marks `dropbox`. The CONTAINER_CLOSE case gains `&& !it._dbxStrayCloser`.
  Gate `!pirKey` (ENFUN excluded). BLL: the button moves inside, the box stays plain (buttonD convention kept).

## Round 1 resume recipe (for the next session)
1. Confirm the tree is at the stop commit (`git log -1`) and `git status` is clean.
2. Review `CONVERTER_V2/outputs/_r314_splice_UNAPPLIED.py` (identical copy in `converter-v2/loop/`); run it with
   Python from Git Bash (`python3 CONVERTER_V2/outputs/_r314_splice_UNAPPLIED.py`) — it asserts every anchor is
   unique and preserves tabs. Then `node --check` both JS files (WSL) and `python3 -c "import json;json.load(open(
   'pageforge-site/converter-v2/data/Emit_Templates.json',encoding='utf-8'))"`.
3. PROVE in memory (WSL, from `CONVERTER_V2/reference/tests/`, ONE toggle state per process — reuse
   `outputs/_probe_r308_convert.cjs --out <dir> CODES`): ON vs `ACTDBXINSIDE_OFF=1` for XMES101 XTAS101 XMES203
   BLL230 ENFUN02 OSAH501 BLL210 ENGS302. Expect: OFF == the disk pages byte-for-byte; ON changes only affected
   modules; XMES101_2_0 has the Upload-to-dropbox button inside `number="2D"` and the box class gains `dropbox`;
   ENFUN02 + the canaries byte-identical in both states; no new literal-tag leak (defect audit predicate).
4. REGENERATE (§0b family): the 121 affected (`_r314_affected.txt`) + every module carrying a dropbox/upload
   marker (`regen_scope.cjs --feature dropDown --list` over-selects by design) via `batch_convert.cjs` in WSL,
   batches from `_batch_plan.py --codes`, then `_content_manifest.py fresh --affected <list>`.
5. GATES: `_fastloop_diff.py` (accept-named only for a decomposed, named mover), `run_all_gates.sh`, dropDown +
   clickDrop verifiers over the family, refresh the skeleton state after the scoped regen (§16 chain trap).
6. FINALISE: changelog entry (round 314), `Config.js` AppVersion 260618.84 -> 260618.85, CLAUDE.md §11/§14,
   `KB_AMALGAMATION_STATUS.md` row 43 -> PARTIAL/LIVE, feature index `--rehtml`, mirror the loop artefacts,
   LOOP_STATE.md, commit (never push).

## KB facts in hand (gold / Claude) — the KB queue is §D of KB_AMALGAMATION_STATUS.md
- LIVE: c71 footer hrefs, c82 body tag, c63 inner col-12, c61 iStock ID, c24 menu italics, BLL lowercase title.
- NOT CAPTURED (queued): c43 placement/modifier (Round 1), c90/c45 acks statements + class (413 pages, full regen),
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
- r1 (engine r314) · KB constraint 43, the trailing upload box inside its activity · MEASURED, mechanism designed, NOT applied · STOPPED by Chris 2026-09-14 23:15 · pages moved 0 · corpus unchanged
