#!/usr/bin/env python3
"""Session 49 /loop-stop — LOOP_STATE.md: decisions, Position (r510 toggled OFF, uncommitted), STOPPED entry, round log,
follow-ups, the Next-session line. WSL."""
import io, os, re, shutil
import _s49_fin as F
T = F.now()
ROOT = F.ROOT
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
ss = F.rd(S); L = ss.split("\n")
shutil.copyfile(S, os.path.join(ROOT, "_Backups", "loop_state", "LOOP_STATE.md.pre-s49-stop.bak"))

def idx(pred, what):
    h = [i for i, l in enumerate(L) if pred(l)]
    assert len(h) == 1, (what, h)
    return h[0]

# (1) Decisions from Chris — session 49
d48 = idx(lambda l: l.startswith("## Decisions from Chris (session 48"), "d48")
L.insert(d48, f"## Decisions from Chris (session 49 — 2026-09-25 17:57 → {T} NZST): the standing `/loop-start` kickoff (the default budget, "
         "16 rounds or 10 hours) and, at ≈21:55, the standing `/loop-stop` (finish-and-commit if provable in under 10 minutes, else toggle "
         "OFF and leave it uncommitted-but-described; record decisions; \"Next session starts with:\"; commit what is finished; the §5 "
         "report; a safe-to-close sentence) — NO new numbered decision; no new Needs-Chris item. Applied stop: r510 needed a guard, a "
         "45-module regeneration and its proofs (≈ 30 min) → its data flag set `enabled: false`, engine + data left uncommitted and "
         "described in Position (proven inert: 303 / 303 pages identical over its 45 modules).")
L.insert(d48 + 1, "")

# (2) Position: the r510 marker → built / toggled OFF / uncommitted; r509's no-round line → "Before r510"
fl = idx(lambda l: l.startswith("- **ROUND 510 IN FLIGHT — NOT PROVEN**"), "r510 marker")
L[fl] = L[fl].replace("- **ROUND 510 IN FLIGHT — NOT PROVEN**",
                      f"- **ROUND 510 BUILT, TOGGLED OFF AT THE /loop-stop ({T}) — UNCOMMITTED; FINISH IT AS THE NEXT SESSION'S ROUND 1**", 1) + (
    " **State at the stop:** `app/js/TagNormaliser.js` + `data/Tag_Lexicon.json` modified and NOT committed; the data flag "
    "`_meta.interactive_qualifier_free_widget.enabled` is **false** (proven inert: `_r510_stop_inert.log`, 303 / 303 pages identical over "
    "its 45 modules); nothing regenerated — the corpus on disk is the r509 state. **Measured before the stop:** probe OFF 0 / ON 214 pages "
    "/ 45 modules (`_r510_ON_pages.txt`); hand-offs labelled 'unclassified' 337 → 153, the writer's widget named (dragAndDrop boxes 4 → 96, "
    "flipCard 8 → 31, memoryGame 1 → 16, carousel 25 → 41 …, `_r510_tally.sh`); 12 new dragAndDrops (+2 dropQuiz), 11 of 12 carrying the "
    "gold's own drags (`_r510_dndcheck.cjs`). **Left to do:** (1) a guard so the r69 pair reading does not build HPFUN101_0_0's category "
    "sort ('[Interactive] Drag and drop, drop the statements into the relevant coloured square' → built pairs from the 2×2 zone table, 0 % "
    "of the gold's drags) — e.g. `dragAndDrop.standard_decline_opener_pattern` on the opener's words, proven inert on every existing build; "
    "(2) set `enabled: true`, re-probe, regenerate the 45 (`_s49_regen_par.sh`), `scoped_ship.sh … --round 510`, the gates, the finalise "
    "(`_s49_fin.py`). The engine / gate checksum manifests were NOT refreshed for the two files, so the next health check reports them "
    "changed — this round's work, not a broken tree.")
nr = idx(lambda l: l.startswith("- **No round in flight** (25 Sept 2026") and "session 49 Round 10" in l, "r509 no-round")
L[nr] = L[nr].replace("- **No round in flight** (", "- **Before r510: no round in flight** (", 1)

# (3) STOPPED entry: the s46 one → archive pointer; the s49 one on top
st46 = idx(lambda l: l.startswith("## >>> STOPPED 2026-09-25 15:57 NZST (session 46)"), "s46 stopped")
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## STOPPED entry, session 46 (verbatim, s49 stop)\n\n" + L[st46] + "\n")
L[st46] = ("## STOPPED entry, session 46 (25 Sept 15:57, §4 BUDGET; r491–r500 shipped + the r498 FULL backstop) -> LOOP_STATE_ARCHIVE.md "
           "'STOPPED entry, session 46 (verbatim, s49 stop)'. Superseded by the session-49 entry above; every verdict stands.")
L.insert(st46, f"## >>> STOPPED 2026-09-25 {T} NZST (session 49) on Chris's `/loop-stop` (≈ 4 h, 10 of the 16-round budget shipped). "
         "**TEN ROUNDS SHIPPED + the r505 FULL backstop, every one committed:** r501 the gate tools (the baseline written by `--commit`; six "
         "verifiers' count test), r502 D15-23 the MX bare lesson menu (+0.0929pp), r503 D15-22 the BLL2xx K / P tabs, r504 D15-17 CEDT301 one "
         "page (a NAMED population change, 2491 → 2486 pairs), r505 / r506 D15-18 the RHS side column + the lost boxes, r507 D15-19 the yellow-✅ "
         "multiChoiceQuiz, r508 the nested bracket (+0.0449pp), r509 KB 10 §5 the empty-menu To Do. **r510 (the generic interactive bracket) "
         "BUILT, TOGGLED OFF, UNCOMMITTED** — Position. Skeleton **55.4588 % @ 2491 → 55.5883 % @ 2486**, ≥50 1592 → 1602, ≥75 277, ≥90 26, "
         "RAW 39.425 → 39.516; cs exact 16746 → 16762 (EXTRA 198 → 204 / missing 887 NAMED); body ANY 232 → 230; leak 52; **60.6 % of "
         "achievable** (ceiling 91.7 %). Plateau 0 of 3. Needs Chris: #1 / #10 only (human actions). <<<")

# (4) Round log
rl = idx(lambda l: l == "## Round log", "round log")
L.insert(rl + 1, f"- s49-r11 (engine r510, 25 Sept 21:43 → {T}) · a PICK pass (the miner's remaining rows dispositioned; the loss ledger; "
         "XGF9 scoped miner below floor; a scoped-miner overwrite of `_diff_queue_details.md` FIXED in `_diff_miner.py`) then THE WIDGET NAMED "
         "AFTER A GENERIC INTERACTIVE BRACKET (KB c14) · BUILT, probed ON 214 pages / 45 modules, one wrong build found (HPFUN101) · TOGGLED "
         "OFF at the /loop-stop, UNCOMMITTED — finish as the next Round 1.")

# (5) Follow-ups
fu = idx(lambda l: l.startswith("- **(s49-r9) the placement census on the r507 corpus**"), "s49-r9 follow-up")
L.insert(fu + 1, "- **(s49-r10 / r11) recorded, each below the floor:** BLL265's Knowledge / Practices land in the page body (its `[LESSON] "
         "Lesson 1` + `[Lesson content]` after the overview's `[End page]` — the one D15-22 overview r503 could not reach); the one-word "
         "`[radioquiz]` spelling (17 tags / 13 modules, no alias) and `[mtk quiz] [autocheck]` (2 — the demote prefers an INTERACTIVE tag); "
         "the MXEX201 / 202 lessons with no menu at all (10 pages); `_verify_mcq.cjs` pairs only `<p class=\"mcqQuestionText\">` golds (the "
         "`<li>` form — MXEX302 — reads 'no gold'); the mcq yellow TABLE bundles (40, many shapes); the D15-19 dropDown type is the NEXT "
         "kickoff's (one widget type per kickoff).")

# (6) Next session starts with
ns = idx(lambda l: l.startswith("**Next session starts with:**"), "next session")
L[ns] = ("**Next session starts with:** `/loop-start` (16 rounds or 10 hours). The tree is DIRTY by design: `TagNormaliser.js` + "
         "`Tag_Lexicon.json` = **r510, built and TOGGLED OFF (`enabled: false`), uncommitted** — the health check's two engine-checksum "
         "mismatches are this round, not a broken tree. **Round 1 = finish r510** (Position: the HPFUN101 category-sort guard, `enabled: true`, "
         "re-probe, regenerate the 45, scoped_ship --round 510, gates, finalise). Then the D15-19 dropDown kickoff (yellow ✅, the D15 guards), "
         "then the ordinary PICK order (the §1g census rows, the follow-up list, the ride-along patches r469 / r469b / r468 / r489 / r463). "
         "LAST SHIPPED r509; LAST FULL r505; scoped #4; plateau 0 of 3; 2,486 pairs; miner 193 CANDIDATE.")
out = "\n".join(L)
F.wr(S, out); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S), "next-line chars", len(L[ns]))
