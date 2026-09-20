#!/usr/bin/env python3
"""Session 29 /loop-stop (20 Sept ≈22:45 NZST) — LOOP_STATE.md: the Round 10 PICK-pass record (no engine change), its Round-log line,
the session-29 'Decisions from Chris' entry, the STOPPED entry (≤ 1,500 chars) and the 'Next session starts with:' line (≤ 800 chars,
replacing the session-28 text). Run under WSL."""
import os, io
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
STATE = R + "LOOP_STATE.md"
lines = io.open(STATE, encoding="utf-8").read().split("\n")
def idx(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix): return i
    raise SystemExit("not found: " + prefix)

# 1. the Round 10 PICK pass (measured, none taken) — before '## Round log'
b = idx("## Round log")
r10 = [
"## Session 29 — Round 10 PICK pass (no engine change; 20 Sept ≈22:05 → 22:43 NZST, ended by `/loop-stop`) — four censuses on the r418 corpus, nothing at the floor",
"- **`_s29_r10_boxforms.py` → `_s29_r10_boxforms.out`** (the r8 box-column census generalised to every callout / panel container's first-child ladder, gold vs Claude per template|subject): 14 groups differ at gold consensus ≥ 0.60 — every one under the 20-page floor or already dispositioned: the LtL `choice` tile image (`choiceImg hoverSwitch › img` — the r307 no-invented-img decision), the Languages activity boxes (Claude's are hand-off dumps — the build backlog), the BLL1 inquiryPanel heading row (`row › col-12.col-md-12 › h2` 49 / 81 on 9 pages vs Claude `col-12.col-md-8`), the ENFUN fundamentalsPanel first heading (gold h3 23 / 32 on 7 pages vs Claude h4 — an r385 `first_heading_level` per-prefix level, 8 pages), the SSFUN panels' bare `h3` (6 pages), the alert family (the inner row / col and the h4 lead are editorial-MIXED in every group: MXFUN bare `p` 0.62 on 8 Claude pages, HPFUN 0.80 on 6 — under the floor), the `accContent` / `clickDropContent` rows (Claude's are dumps).",
"- **`_s29_r10_alertlead.py` → `_s29_r10_alertlead.out`**: Claude's span-mode alert with a lead emits the `<h4>` BEFORE the inner `row > col-12` (`<div class=\"alert\"><h4>Key points:</h4><div class=\"row\">…`) — 60 boxes on 47 pages / 27 modules; the gold's same-lead box is bare 19 / wrapped 13 / absent 28 (reworded) — a tie, not a class. Recorded.",
"- **`_s29_r10_colmd12.py` → `_s29_r10_colmd12.out`**: the label census's biggest MISSING container, the gold's `col-12 col-md-12` column (1734 vs Claude 133): 634 inside activity boxes (380 = the WIDENED wrapper around `div.activity.interactive` — the r331 declined class; D10-3's 'measure per built layout' still open: flipCardsContainer 77 / dragAndDrop 43 first children), 1000 in body rows (h3 223 / p 154 / ol 91 / whakatauki 77 / img 64 — full-width section rows with no derivable discriminator), 112 the BLL1 panel heading rows (9 pages), 119 super-content, 83 tab-panes. Recorded.",
"- **`_s29_r10_labelcensus.py` → `_s29_r10_labelcensus.out`** (the s27-r1 position-free label census re-run on the r418 corpus, 2349 pairs; position-free ratio mean 72.588 %): the EXTRA side is the named KB-over-gold overrides (`acks acksTemplate` 409, `table-bordered` 810, `h4.goJournal` 558) + `audio.audioPlayer.icon` 490 (the r342 TMoA wordDrag class) + `div.alert.solid` 439 (Claude keeps the writer's `solid` modifier the gold drops — measure the gold's `[alert solid]` → plain share before any round); the MISSING side is the widget builds (`WIDGET` 2920, `clickDropContent` 1230, `alertImage` 481 declined, `br` 2568 declined, `iframe.embed-responsive-item` 1086 KB-correct) and **`span.ch-text` 494 on 32 pages / 11 modules — the Chinese-language modules' Han-script span (gold 494 / Claude 0): a Unicode-script rendering rule (CJK runs → `<span class=\"ch-text\">`), the intake Languages family only — the next session's first measurement (consistency of the wrap per Han run; KB §14.1)**.",
"- DIFF_QUEUE #4 / #32–#34 / #589 / #1035 / #1036 dispositioned this session (see the r417 / r418 records); F26 `footer:inside-body` = the gold's own mis-nesting at 0.05–0.23 per group (TWHA 0.62 on 5 modules, under the chrome floor).",
"",
]
lines[b:b] = r10
t = idx("- s29-r9 (engine r418")
lines.insert(t + 1, "- s29-r10 (no engine change, 20 Sept ≈22:05 → 22:43, ended by `/loop-stop`) · PICK PASS — four censuses on the r418 corpus, nothing at the floor: the container first-child ladder (`_s29_r10_boxforms.py`: 14 differing groups, all under 20 pages or dispositioned — the BLL1 panel heading row col-md-12 9 pages, the ENFUN panel h3 8 pages, the alert family editorial-mixed), the bare-lead alert (`_s29_r10_alertlead.py`: 60 boxes / 47 pages, the gold bare 19 : wrapped 13 — a tie), the gold's `col-12 col-md-12` column (`_s29_r10_colmd12.py`: 1734 vs 133 — the r331 widened wrapper 380 + full-width body rows with no discriminator), the position-free label census re-run (`_s29_r10_labelcensus.py`: `span.ch-text` 494 on 32 pages / 11 Chinese modules = the next session's first measurement; `div.alert.solid` 439 to measure)")

# 2. Decisions from Chris (session 29) — above the sessions 14–25 entry
d = idx("## Decisions from Chris (sessions 14–25")
lines[d:d] = [
"## Decisions from Chris (session 29 — 2026-09-20 ≈14:30 → 22:43 NZST): the standing `/loop-start` kickoff (12 rounds or 10 hours; health check first; the r410 decision before any new pick; the miner mandatory, chrome-first; the sessions 15–18 exhaustion verdicts void; §1e population-split before judging any gate; never `python3` from the Bash tool — WSL only; `cs bc` before believing cached rows; `REGENERATE CORPUS` scoped by §0a / §0b; RUN UNINTERRUPTED; the §6 context diet + the bounded §5d re-read after compaction; LOOP_STATE.md before / after every round; commit after every round, never push) and, at ≈22:43, the standing `/loop-stop` message (stop at the next logical point without interrupting anything running; finish-and-commit a round provable in ≤ 10 minutes, else toggle OFF and describe; record every decision; the exact position + a 'Next session starts with:' line; commit; the §5 report with the push block; the safe-to-close sentence). **No numbered decision was asked or given**; every D10-1…D10-9 decision stood. Applied stop: Round 10 was a PICK pass with no engine change and a clean tree — nothing to finish or toggle; its record + instruments committed at the stop.",
"",
]

# 3. the STOPPED entry — above the session-27 one
s = idx("## >>> STOPPED 2026-09-19")
lines[s:s] = [
"## >>> STOPPED 2026-09-20 ≈22:45 NZST (session 29) on Chris's `/loop-stop` — 10 rounds of the 12 (8 h 15 of the 10). NINE SHIPPED: r410 the WJFUN tile-page dialect (+0.1095pp, ≥50 +8) · r411 the tile menu's ROW+COL shell (+0.0058) · r412 the heading-then-table owner form (+0.0139) · r413 its owned half (+0.0080) · r414 the nested activity box suppressed (+0.0696, ≥50 +4 / ≥75 +2) · r415 the owned heading-led bundle with no table (+0.0246, ≥50 +3) · r416 the activity title typed inside the red span (+0.0174; THE FULL REGENERATION of all 494 — the ledger's backstop, no residue) · r417 the XDLS choice-page panel holds its content directly (+0.1947, ≥50 +23) · r418 the first tile panel's `row.clickDropContent.noBorder` form + the r417 title-pin repair (+0.0630, ≥50 +1); Round 10 a PICK pass (four censuses, none at the floor). Skeleton **53.680 → 54.186 %** (+0.506pp; 59.1 → 59.6 % of the 90.9 % ceiling), ≥50 1398 → 1439, ≥75 236 → 238, ≥90 20, RAW 37.884 → 38.204; compare_structure 14091 → 14168; every other gate EXACT or better; every verifier RESULT identical; 16 selftests GREEN every round. The miner re-mined after every ship: 183 → 183 CANDIDATE rows, all dispositioned. Plateau window 0 of 3. Build 260619.89; ledger scoped #2 since the r416 FULL (6 of headroom). NEEDS CHRIS: the `Subject_Prefix_Map.json` labels (session 28 report) + the five items of the session-26 STOPPED entry (archive) stand. Tree clean at cf504e3 + the stop commit. <<<",
"",
]

# 4. the 'Next session starts with:' line (≤ 800 chars), replacing the session-28 text
n = idx("**Next session starts with:**")
lines[n] = ("**Next session starts with:** the standing `/loop-start`; health check (locks, `verify_after_transfer.sh` PASS — 552 gold / 494 Claude dirs / 2,555 Claude pages, `wc -c`); "
            "`git status` in pageforge-site: a CLEAN tree at the session-29 stop commit (r418 = cf504e3 beneath it); the miner's queue (20 Sept 21:58, the r418 corpus) is "
            "current — 183 CANDIDATE rows, all dispositioned; FIRST measurement: `span.ch-text` (gold 494 on 32 pages / 11 Chinese modules, Claude 0 — a Han-script span "
            "rule, `_s29_r10_labelcensus.out`) and `div.alert.solid` 439 (the writer's `solid` the gold drops?); then D10-3's open item (the widened `col-12 col-md-12` "
            "wrapper per BUILT widget layout — `_s29_r10_colmd12.out`); the ledger is scoped #2 since the r416 FULL. Pending decision: the `Subject_Prefix_Map.json` labels.")
assert len(lines[n]) <= 800, len(lines[n])
io.open(STATE, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("LOOP_STATE.md", os.path.getsize(STATE), "bytes; next-line", len(lines[n]), "chars; stopped-entry", len(lines[s]), "chars")
