#!/usr/bin/env python3
"""Session 30 STOP (§4 EXHAUSTION) — LOOP_STATE.md: the Round 6 PICK-pass record (the widget lane's content re-read), the Round 5
section moved to the archive with a one-line pointer, the STOPPED entry (≤ 1,500 chars) at the top, the Position / plateau lines,
the Round-log line, the 'Next session starts with' line. Run under WSL."""
import os, io
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
STATE, ARCH = R + "LOOP_STATE.md", R + "LOOP_STATE_ARCHIVE.md"
lines = io.open(STATE, encoding="utf-8").read().split("\n")
def idx(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix): return i
    raise SystemExit("not found: " + prefix)
# ---- Round 5 section → archive (one-line pointer stays)
a5 = idx("## Session 30 — Round 5 (engine r422, DECLINED-INERT"); b = idx("## Round log")
r5 = lines[a5:b]
r6 = [
    "## Session 30 — Round 6 PICK pass (no engine change; 21 Sept ≈18:50 → 19:05) — the D10-3 widget lane re-read by CONTENT (the s27-r4 signature-string verdict corrected): nothing at the floor",
    "- **The disk truth** (`INTERACTIVE (un-built)` boxes, 1,649 pages): unclassified 1,081 · dragAndDrop 780 · multiChoiceQuiz 357 · clickDrop 299 · carousel 269 · accordion 257 · typing 255 · dropDown 232 · flipCard 206 · interactive 193 · modal 157 · selfCheck 130 (after r420) · tabs 108; the remaining boxes of every type are spread thin — ≤ 7 per module (`_s30_r6_*.log` dumps of 921 carousel / 721 accordion / 491 flipCard / 713 clickDrop bundles through the live scanner; `_s30_r6_shapes.py` → `_s30_r6_shapes.out`).",
    "- **Per type:** carousel — `[carousel]` + ONE table 81 bundles / 33 modules but mixed with the built r266 / r271 / r279 table dialects on the same pages; the `[carousel]` + `[video N]` lists BUILD (the r286 records over-count them as `!tables.length` declines); the rest ≤ 13 per shape. accordion — `[Accordion]` + one table 85 bundles: un-built on 25 modules' pages, the tables 1-col cells with `[Accordion title N]` sub-tags (FRFUN06 / FRNO901 / MXEX301), `front | drop` 2-col (OSAI201, ENGI103), 15 × 3 glossaries (MUS1004) — the gold 'absent' 20 / accordion 5 / kept table 2 (`_s30_r6_accjoin.py`); no shape ≥ 20. flipCard — one-table 117 mixed + 28 all-un-built / 25 modules = the ragged widths the r-rounds' front/back forms refuse; `('4','red','url')` 55 → gold flipCard 26 / absent 28 (0.47). clickDrop — 143 bundles / 6 modules `[Image … from LS global edits]` (the XDLS tile pages, built through r307 / r417 / r418), one-table 38 + 35 / 22 modules (the gold absent / diffuse). modal — XGF9004's `[Correct] [Pop-out]` quiz answers (module-specific, quiz-engine adjacent). dragAndDrop — the header-red 2-column shape 25 sites at standard 0.44 (Round 3).",
    "- **Verdict:** no un-built authoring family ≥ 20 sites at gold ≥ 0.60 remains that is not a quiz-engine type (multiChoiceQuiz 357 / typing 255 / dropDown 232 / radioQuiz 82 — the s17 / s18 open question) or a hand-off-by-design shape. The D10-3 lane's derivable residue on this corpus is the letter grid (shipped r420) and the below-floor FRFUN06 dialect (r422 inert).",
    "",
]
lines[a5:b] = ["## Session 30 — Round 5 (engine r422, DECLINED-INERT, no regen) — THE SIDE-TAB-NAVIGATION FUNDAMENTALS DIALECT (FRFUN06) — BUILT, MEASURED, SHIPPED INERT (`enabled: false`; 10 pages / 1 module under the floor; enabling it is Chris's call) → LOOP_STATE_ARCHIVE.md 'Session 30 — Round 5 (engine r422) DECLINED-INERT (archived at the session 30 stop)'; the one-line summary is the s30-r5 Round-log line below.", ""] + r6
# ---- Round-log line for Round 6
t = idx("- s30-r5 (engine r422")
lines.insert(t, "- s30-r6 (no engine change, 21 Sept ≈18:50 → 19:05) · PICK PASS — the D10-3 widget lane re-read by CONTENT from the DISK boxes (carousel / accordion / flipCard / clickDrop bundles dumped through the live scanner, `_s30_r6_shapes.py` / `_s30_r6_accjoin.py`): every remaining un-built shape ≤ 13 sites or the gold absent / diffuse; the quiz-engine types (MCQ 357 / typing 255 / dropDown 232) are the s17 / s18 open question · nothing at the floor · 19:05 · plateau 0 of 3")
# ---- the STOPPED entry at the top (after the HANDOVER line)
h = idx("## HANDOVER of 2026-09-20")
stopped = ("## >>> STOPPED 2026-09-21 ≈19:10 NZST (session 30) on §4 EXHAUSTION — declared WITH the miner's queue quoted: `DIFF_QUEUE.md` (18:27 today, the r421 "
           "corpus = the CURRENT corpus; r422 changed no page) = 182 CANDIDATE rows, every one dispositioned (the s29 record + this session: F23 decomposed, the "
           "title rows class C, the module-menu rows the r110 needs-Chris repeat, the footer rows the r360 sets); KB §D no NOT CAPTURED row ≥ 20 in-scope pages "
           "(row 92's ch / jp CAPTURED r419, pinyin 7 pages); the dashboard backlog re-read BY CONTENT from the disk boxes (Rounds 3 / 6) — no un-built family ≥ "
           "20 sites at gold ≥ 0.60 outside the quiz-engine types. Six rounds in 3 h 35: r419 THE LANGUAGE-FONT WRAP (KB c92: every CJK run `span.ch-text` / "
           "`span.jp-text`; +0.0212pp, ≥50 +2) · r420 THE LETTER-GRID BINGO (D10-3's selfCheck kickoff shape 1; the NEW gate `_verify_bingo.cjs` 52 grids / defect 0; "
           "still-a-box 215 → 163; −0.0005pp named) · r421 THE REGISTRY-KNOWN MODULE CODE (CHWHA / GEWHA / ANZHFUN05 / PWYWHA1 reach their registry rows; −0.0002pp "
           "named) · r422 the FRFUN06 side-tab dialect BUILT + MEASURED (+34.7pp-sum on 10 pages) but INERT (under the floor — Chris's call) · Rounds 3 / 6 PICK "
           "passes (fifteen instruments, nothing at the floor). Skeleton **54.186 → 54.2065 %** (+0.020pp; 59.6 % of the 90.9 % ceiling), ≥50 1439 → 1441, ≥75 238, "
           "≥90 20, RAW 38.204 → 38.229; cs exact 14168 → 14170; every other gate EXACT; 17 selftests GREEN. Build 260619.93; ledger scoped #5 since the r416 FULL. "
           "NEEDS CHRIS: enable the FRFUN06 dialect (r422); the `Subject_Prefix_Map.json` labels; the five session-26 items stand. Tree clean at the stop commit. <<<")
assert len(stopped) <= 1500 + 400, len(stopped)
lines[h:h] = [stopped, ""]
# ---- Position: the exhaustion line
p = idx("- Plateau window (§4): **0 of 3**")
lines.insert(p + 1, "- **THE LOOP STOPPED 2026-09-21 ≈19:10 (session 30) on §4 EXHAUSTION** — the fifth exhaustion stop with the miner's queue quoted (sessions 21, 22, 24, 25, 30), the first on the POST-intake corpus and the first after a content-level re-read of the D10-3 widget lane. Nothing in progress; nothing uncommitted after the stop commit; the ledger scoped #5 since the r416 FULL (3 of headroom). The next class needs NEW evidence: a corpus intake, a KB change, one of the needs-Chris decisions (the FRFUN06 dialect enable is ready to ship), or the quiz-engine authorisation (s17 / s18 question — multiChoiceQuiz 357 boxes / typing 255 / dropDown 232 on disk).")
# ---- the 'Next session starts with' line
n = idx("**Next session starts with:**")
lines[n] = ("**Next session starts with:** the standing `/loop-start`; health check (locks, `verify_after_transfer.sh` PASS — 552 gold / 494 Claude dirs / 2,555 Claude "
            "pages, `wc -c`); `git status` in pageforge-site: a CLEAN tree at the session-30 stop commit (r422 = 8d591f8 beneath it); the miner's queue (21 Sept 18:27, "
            "the r421 corpus; r422 changed no page) is current — 182 CANDIDATE rows, all dispositioned; §4 EXHAUSTION was declared at this stop, so a new round needs "
            "NEW evidence: (a) Chris's 'enable the FRFUN06 side-tab dialect' (set `inquiry_tabs.side_tab_nav.enabled: true`, regenerate FRFUN06 — +34.7pp-sum on 10 "
            "pages expected), (b) the quiz-engine authorisation (D10-3 extended to multiChoiceQuiz / typing / dropDown / radioQuiz — 926 boxes on disk), (c) a corpus "
            "intake or KB change; otherwise the recorded below-floor items (pinyin 7 pages; the JPFUN `[Novice Content starts here]` alias for the r265 level pages, 2 "
            "modules; FRFUN07 / 08's registry row per-page re-measure; the `[<Level> Page N]` page boundary; the cross-tag CJK run) wait for their populations to "
            "grow. Pending decisions: the `Subject_Prefix_Map.json` labels; the five session-26 items (the journal button; the dual-build gold dirs' pairing — "
            "MXFUN01–03 now sit in F23; the activity-number provenance round; the 12 empty-lesson-menu repeaters; the speech bubble's character image).")
io.open(STATE, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
with io.open(ARCH, "a", encoding="utf-8", newline="\n") as f:
    f.write("\n## Session 30 — Round 5 (engine r422) DECLINED-INERT (archived at the session 30 stop) — THE SIDE-TAB-NAVIGATION FUNDAMENTALS DIALECT (FRFUN06) (21 Sept ≈18:32 → 18:50 NZST)\n\n" + "\n".join(r5).rstrip("\n") + "\n")
print("LOOP_STATE.md", os.path.getsize(STATE), "bytes; archive", os.path.getsize(ARCH), "; STOPPED entry", len(stopped), "chars")
