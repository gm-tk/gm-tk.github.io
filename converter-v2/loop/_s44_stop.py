#!/usr/bin/env python3
"""Session 44 STOP (§4 BUDGET — the 12-round default reached): Round 12's PICK-pass record, the STOPPED entry (the s43 entry → the archive,
verbatim), the session-44 Decisions block, the session start-note stop line, Follow-up, the "Next session starts with" line. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
shutil.copyfile(S, S + ".pre-s44-stop.bak")
L = io.open(S, encoding="utf-8").read().split("\n"); n0 = os.path.getsize(S)
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
# Round 12 — the round log + Follow-up
k = find("## Round log")
L.insert(k + 1, "- s44-r12 (no engine change, 25 Sept 03:21 → 03:25) · a PICK pass: KB c79's module-title FALLBACK on lesson pages "
         "(`_s44_r12_fallback.py`): 87 pages / 38 modules — TRR 42 (Chris's decision 2 / r321: an MTK lesson with no title of its own carries "
         "both module titles — decided), XMES1 9, PNR 6, ANZH4 4, DTC1 4, MXEO1 4 … scattered; of the non-TRR, the gold's own title is in the WT "
         "on a handful of untagged / red lines with no single source ≥ the floor — no class · plateau 0 of 3 (neither). **The 12-round budget is "
         "reached — §4 BUDGET stop.**")
k = find("- **(s44-r2) THE TRR1 LESSON-PAGE LANE")
L.insert(k, "- **(s44-r5 / r11 / r12) left after this session, each measured:** the Online Safety title bars — OSBY101 / 201's unfilled `MODULE "
         "TITLE TE REO` placeholder and six English-only title bars (OSAH501 / OSAI501 / OSBY501 / OSGM201 / OSGM501 / OSSC501) whose Te Reo "
         "title the gold takes from the series (class C unless a sibling-title rule is decided); KB c38's ECH level (0 Claude ECH pages carry a "
         "built widget today); c27 (dropQuiz standalone pairs → list) — the per-shape check; c66 (acks titles verbatim) not measured; c62's "
         "writer-side count (two widget TAGS under one heading) never taken; PMT101's one-table template (its lesson pages 23–35 %, one module).")
# the STOPPED entry: the s43 one → the archive, verbatim
k43 = find("## >>> STOPPED 2026-09-24 23:05 NZST (session 43)")
s43 = L[k43]
L[k43] = ("## >>> STOPPED 2026-09-25 03:25 NZST (session 44) on §4 BUDGET — the 12-round default reached (≈ 3 h 50 min; the 10 h cap not "
          "reached). **EIGHT ENGINE ROUNDS SHIPPED + THE FULL BACKSTOP, every one committed:** r478 (s43's toggled-OFF round finished — KB c75 "
          "the activity lead's links); r479 KB 07B the bilingual whakataukī box (21 modules); r480 KB 07B the MTK activity as ONE box (a TRR "
          "family dialect, TRR102 excluded); r481 the MTK data rows as one hand-off; r482 KB 07D the bilingual lesson title h2; r483 / r484 KB c38 "
          "autoCheck on the 1-3 / 4-6 templates (D&D, then the quiz types); r485 the title bar's language-boundary split. **The FULL backstop** "
          "(Round 7): 545 modules, 0 pages differ. **Three passes:** R5 (bold / P3 / c62), R10 (c7 / c15 / c27 verified), R12 (c79 fallback). "
          "Skeleton **55.2360 → 55.3463 % @ 2491 (+0.1103pp)**, ≥50 1577 → 1582, ≥75 275 → 277, ≥90 25 → 26, RAW 39.195 → 39.231; cs exact "
          "16759 → 16691 (r480's −80 NAMED pool shrink), missing 903 → 872; body / clean / leak EXACT; **60.4 % of achievable** (ceiling 91.7 %). "
          "Plateau 0 of 3 (reset by r480). Needs Chris: #17–#19, #22 (none new). <<<")
k43b = find("## STOPPED entry, session 42 (24 Sept 16:45")
L.insert(k43b, "## STOPPED entry, session 43 (24 Sept 23:05, `/loop-stop`; r472–r477 shipped, r478 toggled OFF) -> LOOP_STATE_ARCHIVE.md 'STOPPED "
         "entry, session 43 (verbatim, s44 stop)'. Superseded by the session-44 entry above (which finished r478); every verdict stands.")
# the decisions block for session 44
kd = find("## Decisions from Chris (session 43 — 2026-09-24 18:06 → 23:05 NZST)")
L.insert(kd, "## Decisions from Chris (session 44 — 2026-09-24 23:33 → 2026-09-25 03:25 NZST): the standing `/loop-start` kickoff only (the "
         "default budget, 12 rounds or 10 hours — the 12 rounds reached first) — NO new numbered decision; no new Needs-Chris item.")
L.insert(kd + 1, "")
# the session-44 start note: the stop line
ks = find("**Session 44 started:**")
L[ks] += (" **Stopped 03:25 on §4 BUDGET** (12 rounds: 8 engine ships r478–r485, the FULL backstop, 3 PICK / verification passes; 0 "
          "compactions). **Clock note:** the ≈ times in the s44 round records ran up to ≈ 15–35 min ahead of the commit clock — read "
          "`git log` (r478 00:00, r479 00:36, r480 01:16, r481 01:32, r482 01:55, backstop 02:24, r483 02:44, r484 02:59, R10 03:00, r485 03:21).")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** the standing `/loop-start` — a clean start expected (every round committed; `verify_after_transfer.sh` "
        "PASS at the stop). LAST SHIPPED **r485** (260620.49, the title-bar language split); LAST FULL = **r482** (the s44 backstop, 0 pages "
        "differ); ledger scoped #3; plateau **0 of 3**; 2,491 pairs; census 552 / 545 / 2,679. First PICK lanes not yet used after s44: the "
        "writer-side c62 count; c66 acks titles; the OS series-title question; the placement census's P1b / P8. Ride-along patches "
        "`_r469_declined.patch` / `_r469b_declined.patch` / `_r468_declined.patch`. Needs Chris #17–#19, #22.")
io.open(S, "w", encoding="utf-8", newline="\n").write("\n".join(L))
with io.open(A, "a", encoding="utf-8", newline="\n") as f:
    f.write("\n## STOPPED entry, session 43 (verbatim, s44 stop)\n\n" + s43 + "\n")
print("LOOP_STATE", n0, "->", os.path.getsize(S))
