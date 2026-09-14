# LOOP_STATE.md — position of the autonomous PageForge loop (LOOP__Autonomous_Rounds.md)

**Session 1 started:** 2026-09-14 (Claude Code on Chris's Windows machine). Budget: 10 rounds or 6 hours.
**Authority carried by the kickoff message:** `REGENERATE CORPUS` for every round, scoped by CLAUDE.md §0a/§0b.

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
- `CONVERTER_V2/outputs/` and `reference/` are OUTSIDE the git repo; loop artefacts are mirrored into
  `pageforge-site/converter-v2/loop/` at each commit (see its README).
- `_regen_safe.sh` hard-codes `timeout 40` (the old sandbox wall): run `batch_convert.cjs` directly with a long
  timeout for regenerations, then prove freshness with `_content_manifest.py fresh --affected`.

## Position
- Round 0 (ceiling instrument): DONE 2026-09-14, commit ca59d13.
- Round 0b (KB amalgamation audit): DONE 2026-09-14 — `KB_AMALGAMATION_STATUS.md` at the folder root
  (mirrored in `converter-v2/loop/`); facts in `outputs/_r0b_kbfacts.json`, `_r0b_kbsignatures.json`,
  `_r0b_kbsignatures2.json`. Census + dashboard refreshed (coverage 50.8%).
- Round 1 (= engine round 314): PICKED — see below. IN PROGRESS.

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
- **Preliminary size:** 208 non-BLL Claude activities followed by an upload button that lack the modifier
  (XDLS 63 · XMES 32 · XTAS 22 · TWHA 10 · ANZH/ENGI/ENGS 7 · HIS 6 ...); the exact inside/trailing split per
  template and series comes from `outputs/_measure_r314_dbxplace.py` (BLL kept separate). Ships only where the
  gold convention share >= 0.60 in the group.
- **Triangulated:** XMES101 2D (WT `[Activity 2D] ... [body] Upload to dropbox ... [microphone, camera and video
  dropbox buttons] [End page]` -> gold `activity dropbox` with the button as the box's last child -> Claude closes
  the box after the clickDrop and ships the button + To Do note in a new row); XTAS101 1C/1E/1F/1G (WT
  `[insert dropbox link]` inside each activity -> gold `activity interactive dropbox`); XMES101 3A.
- **Planned mechanism:** keep the freed dropbox bundle inside the open activity when the writer's marker sits
  inside the activity's span (data flag + env toggle); the r305 postpass then marks the box unchanged.
  Regeneration scope: the affected modules + the §0b family (every module carrying a dropbox/upload marker).

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
- r0b · KB amalgamation status (95 CLs, 92 constraints, 12 families; 11 queued rows) · shipped (document, no converter change) · pages moved 0
