#!/usr/bin/env python3
"""Session 45 Round 12 + STOP — the last PICK pass (the two unused §4 lanes), the STOPPED entry (the session-44 one archived verbatim),
Needs Chris #23, the session-start note's clock correction, the "Next session starts with:" line. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
shutil.copyfile(S, S + ".pre-s45-stop.bak")
ss = io.open(S, encoding="utf-8", newline="").read(); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
# 1. the Round 12 record
k = find("## Round log")
L.insert(k + 1, "- s45-r12 (no engine change, 25 Sept 08:36 → 08:45, commit times) · the last PICK pass — the two §4 lanes this session had not "
         "used: the recognition / no-build list (the 7 no-source modules GER1003–1007 / SAM1005 / 1006 and TRR104 / 105's Media-List-only dirs "
         "unchanged, no new docx (the session-start §0 intake checks); the 19 Sept intake §7 list fully dispositioned — WJFUN r410, PMT101 r423, "
         "XOTP r425) and per-family registry rows (no held-back row in the registries) — nothing to build; Needs Chris #23 raised (Round 4's MX bare "
         "lesson menu — the KB 10 §3 series row is Chris's lane, D13-1) · plateau 0 of 3 (neither). **The 12-round budget is reached — §4 BUDGET stop.**")
# 2. Needs Chris #23
k = find("22. **24 Sept (session 42 Round 3, the placement census)**")
L.insert(k + 1, "23. **25 Sept (session 45 Round 4)** — **The MX series' BARE lesson menu: keep KB 01B's `row > col-md-8` or add a KB 10 §3 series "
         "row?** The gold ships `#module-menu-content > h5 + ul` with no row / column on MXFU 44 / 44 lesson pages, MXEX 26 / 27, MXDB3 14 / 14, "
         "MXDI3 7 / 7 (91 pages / 12 modules); KB 01B's 'Key structural rules for lesson page simplified menus' says the row form, "
         "which Claude ships and the rest of the corpus uses (0.92). Options: A keep the KB "
         "form (today — the 91 pages named overrides); B add the four series to KB 10 §3's 'series conventions — preserve' list and let the loop "
         "build a bare lesson-menu shell for them (a small skeleton gain on 91 pages). Recommended: B. `_s45_r4_menuwrap.py`.")
# 3. the STOPPED entry (the session-44 one → archive verbatim)
k = find("## >>> STOPPED 2026-09-25 03:25 NZST (session 44)")
old = L[k]
L[k] = ("## >>> STOPPED 2026-09-25 08:45 NZST (session 45) on §4 BUDGET — the 12-round default reached (≈ 3 h 30 min; the 10 h cap not reached). "
        "**FOUR ENGINE ROUNDS SHIPPED + THE FULL BACKSTOP, every one committed:** r486 KB 01F the writer's quote is `p.quoteText` + "
        "`p.quoteAck`; r487 the unquoted named hover anchor (+70 definitions that were silently dropped); r488 the story-reference carousel shell "
        "(43 hand-off boxes → carousels, Still-a-box 320 → 277); r490 the lesson overview's WALT alert is menu content. **The FULL backstop** "
        "(Round 10): 545 modules, 0 pages differ. **Seven PICK passes** (R3 / R4 / R6 / R7 / R8 / R11 / R12 — one prototype saved as the "
        "ride-along patch `_r489_accbullet_declined.patch`). Skeleton **55.3463 → 55.3705 % @ 2491 (+0.0242pp)**, ≥50 1582 → 1585, ≥75 277, ≥90 "
        "26, RAW 39.231 → 39.285; cs exact 16691 → 16702, EXTRA 208 → 198, missing 872 → 878 (NAMED, r486); body / clean / leak EXACT; **60.4 % "
        "of achievable** (ceiling 91.7 %). Plateau 0 of 3. Needs Chris: #17–#19, #22, **#23 new** (the MX bare lesson menu). <<<")
k2 = find("## STOPPED entry, session 43 (24 Sept 23:05")
L.insert(k2, "## STOPPED entry, session 44 (25 Sept 03:25, §4 BUDGET; r478–r485 shipped + the r482 FULL backstop) -> LOOP_STATE_ARCHIVE.md 'STOPPED "
         "entry, session 44 (verbatim, s45 stop)'. Superseded by the session-45 entry above; every verdict stands.")
# 4. the session-45 start note: condenses + the clock correction
k = find("**Session 45 started:**")
L[k] = L[k] + (" **§5d condenses** #1 at the start (95.6 → 86.2 KB), #2 after Round 5 (93.8 → 87.2 KB), #3 after Round 8 (95.1 → 88.2 KB). No "
               "compaction. **Clock correction:** the ≈ times on the s45-r3 → r8 and r11 Round-log lines and the r486 / r487 finalises ran ≈ 10–70 min AHEAD "
               "of the real clock — the commit times are true (r486 05:59, r487 06:28, r488 07:20, r490 08:01, the FULL 08:33, Round 11 08:36); "
               "the true elapsed at the stop is ≈ 3 h 30 min (05:14 → 08:45).")
# 5. Next session starts with
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** the standing `/loop-start` — a clean start expected (every round committed; `verify_after_transfer.sh` "
        "PASS at the stop). LAST SHIPPED **r490** (260620.53, the LO WALT alert); LAST FULL = **r490** (the s45 Round 10 backstop, 0 pages "
        "differ); ledger scoped #0; plateau **0 of 3**; 2,491 pairs; census 552 / 545 / 2,679. Lanes this session used: all seven (miner, KB, "
        "hand-off boxes, loss ledger, placement census, recognition list, family rows). Open follow-ups with numbers: the accordion vocabulary "
        "batch (the r489 patch + WHY_UNBUILT__accordion items 4 / 5 / 6), the MTK drop-down three-tab header (TRR203 / TRR301 / PMT101), the "
        "gathering lever (WHY_UNBUILT__INDEX A). Ride-along patches `_r489_accbullet_declined.patch` / `_r469_declined.patch` / "
        "`_r469b_declined.patch` / `_r468_declined.patch`. Needs Chris #17–#19, #22, #23.")
# 6. the session-45 decisions block (none new)
k = find("## Decisions from Chris (session 44")
L.insert(k, "## Decisions from Chris (session 45 — 2026-09-25 05:14 → 08:45 NZST): the standing `/loop-start` kickoff only (the default budget, 12 "
         "rounds or 10 hours — the 12 rounds reached first) — NO new numbered decision; one new Needs-Chris item raised (#23, the MX bare lesson "
         "menu).\n")
ns = "\n".join(L)
io.open(S + ".tmp", "w", encoding="utf-8", newline="").write(ns); os.replace(S + ".tmp", S)
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## STOPPED entry, session 44 (verbatim, s45 stop)\n\n" + old + "\n")
print("LOOP_STATE", len(ss.encode()), "->", len(ns.encode()), "; STOPPED entry chars", len(L[find("## >>> STOPPED 2026-09-25 08:45")]))
