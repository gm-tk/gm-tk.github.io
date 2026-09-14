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
- WSL `/tmp` persists between calls. Timings under WSL: defect audit ~10 s, ceiling tool ~60 s, KB facts ~55 s.
- Long file writes go through the Write tool, not shell heredocs (a ~30 KB heredoc hits ENAMETOOLONG).
- `CONVERTER_V2/outputs/` and `reference/` are OUTSIDE the git repo; loop artefacts are mirrored into
  `pageforge-site/converter-v2/loop/` at each commit (see its README).

## Position
- Round 0 (ceiling instrument): DONE 2026-09-14. Tool `CONVERTER_V2/outputs/_measure_ceiling.py`; output
  `_ceiling_r0.json` / `_ceiling_r0.md`; changelog entry prepended; CLAUDE.md §9 note added.
  No converter output changed; gates not re-run; the round-313 baselines stand.
- Round 0b (KB amalgamation audit): IN PROGRESS. Facts probe `outputs/_measure_r0b_kbstatus.py` run
  (`_r0b_kbfacts.json`); `KB_AMALGAMATION_STATUS.md` being written at the folder root.
- Rounds 1+: not started.

## The ceiling (Round 0 result — quote it in every report)
- Paired population 1880 pairs = the gate's 1939 minus 59 unmeasurable (13 TRR modules with a Media-List-only
  parsed file — 11 of them have an unparsed Writers Template.docx, TRR104/105 have none — plus TRR115/ENGJ403
  with no parsed file). No-source share, scaffold scope: raw 11.1% -> net 8.4%.
- **CEILING (scaffold) 91.6%** (loose upper bound 94.2%); full-scope ceiling 87.1%.
- **r313 SCAFFOLD 49.941% = 54.5% of achievable (band 53.0-54.5%)**; RAW 34.430% = 39.5% of achievable.
- Formula: % of achievable = skeleton mean / ceiling, ceiling = 1 - net no-source share (per-page mean).
- Trap recorded: read `_parsed.txt` as the UNION of every file in the gold dir (the Media List sorts first).
  `anchor_compare.wt_items` still reads the first file — a repair candidate, not touched.

## KB facts in hand for Round 0b (gold / Claude, from `_r0b_kbfacts.json`)
- c71 footer hrefs empty: LIVE (68 / 0 non-empty). c82 body tag present: LIVE (99 / 0 missing). c63 activity inner col-12: LIVE.
- c89 learningSupport on X-prefixed <html>: NOT CAPTURED (72 of 250 / 0 of 228 pages) — 36 modules, 228 Claude pages; gate-neutral (the html tag is outside the skeleton).
- c92 jp-text/ch-text/pinyin: NOT CAPTURED (5 of 10 / 0 of 7 pages) — scope 3 WT modules (< 20 pages).
- c83 no loading="lazy" inside moving widgets: NOT CAPTURED (3472 of 15322 / 1121 of 1215 images).
- CL-0082 MTK quiz shell never carries quiz content: NOT CAPTURED (157 of 199 / 56 of 80 shells) — 12 WT modules.
- CL-0090 acksTemplate + never type the three statements: NOT CAPTURED (typed on 443 / 394 pages; class on 74 / 19) — corpus-wide (413 overview pages), a locked admin decision.
- Button labels with a trailing full stop: 3 / 420 (Claude-only defect; gate-neutral, text only).
- c79 lesson-page h1 = the lesson's own title: 1534 paired lesson pages, Claude matches gold on 882; Claude falls back to the module title on 141 (gold 233); gold dual-h1 (the lesson's own bilingual pair) 237 vs Claude 10 — structural, skeleton-visible.

## Declined classes
(none yet)

## Blocked classes
(none yet)

## Round log
- r0 · the ceiling instrument · shipped (tool + measurement, no converter change) · ceiling 91.6%, SCAFFOLD 49.941% = 54.5% of achievable · pages moved 0
