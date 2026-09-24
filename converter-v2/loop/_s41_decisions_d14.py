#!/usr/bin/env python3
"""Chris's post-stop decisions (session 41, 24 Sept 2026): D14-20, D14-21 and the standing D14-S1 — recorded in LOOP_STATE.md
(Decisions block, Needs Chris #20 / #21 struck, r464 WITHDRAWN, the queued rounds, the STOPPED entry's post-stop note, the
round-log line and the Next-session line). .pre-d14.bak kept. Run under WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md")
shutil.copyfile(S, S + ".pre-d14.bak")
s = io.open(S, encoding="utf-8").read(); L = s.split("\n"); n0 = len(s.encode("utf-8"))
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
# 1. the decisions block (above the session-41 kickoff block)
k = find("## Decisions from Chris (session 41 — 2026-09-24 07:25 → 12:50 NZST)")
L[k] = L[k].replace("NO new numbered decision.", "NO numbered decision DURING the run; the three given after the stop are the block above (D14).", 1)
L[k:k] = [
    "## Decisions from Chris (session 41, AFTER the stop — 2026-09-24 ≈13:00 NZST; his answers to Needs Chris #20 / #21 and one "
    "STANDING instruction) — numbered **D14-N where N = the Needs Chris number**; D14-S1 is standing. Each \"Answer\" is his line VERBATIM.",
    "- **D14-21 — the `Merge item N` lessons (CHI1003, CHI1004, CHI1005, JPN1004).** Answer: *\"these are no-source so can be "
    "ignored for all future stats and comparisons and future development on this PageForge project.\"* → **Authorises:** the four "
    "modules join `compare_exclusions.txt` (the ONE list `_corpus.gate_mods()` honours — every gate, the miner, the census, the "
    "dashboards, the loss ledger) with the reason \"no-source — every lesson is a `Merge item N` line; D14-21\"; no round ever "
    "targets them again; r464 (the note for their `Merge item N` line) is WITHDRAWN — backed out after the stop, patch kept "
    "(`outputs/_r464_wip.patch`). Applying the exclusion is a measurement round (the r343 / D10-6 precedent): add the four "
    "codes, re-run the gate suite + the skeleton json fresh, re-baseline `gate_baseline.json` (every field; never a gain), "
    "re-mine, mirror, commit — **QUEUED: next session's Round 1.**",
    "- **D14-20 — the MTK overview introduction's course-code heading (`[H1] TRR900`).** Answer: *\"Follow the recommended course "
    "of action (drop the TRR900 course headings).\"* → **Authorises:** the writer's course-code heading at the top of an MTK "
    "Module Introduction is dropped (the gold drops it on 17 of 18 overview pages); a NAMED override of the KB 07D skeleton "
    "comment (\"Typically: course code h1\"). Data flag + env `*_OFF`, the TRR family regenerated. **QUEUED: next session's "
    "Round 2.**",
    "- **D14-S1 — STANDING: hunt placement discrepancies everywhere.** Chris, on the r460 finding (\"the gold standard moves "
    "Knowledge/Practices sections out of the Overview pane in 31 of 36 modules … whereas my output kept all 36 in Overview\"): "
    "*\"This is EXACTLY the sort of thing I want Claude to be extra vigilant in identifying and fixing as much as possible, so "
    "continue checking for these types of discrepancies wherever possible in order to then have future loops configured to "
    "patching up the PageForge to make sure this is correctly converting EVERY aspect of the module.\"* → **Written into "
    "LOOP__Autonomous_Rounds.md as §1g THE PLACEMENT CENSUS** (a standing lane in every PICK pass, §3 step 1; the seventh lane "
    "of §4's exhaustion test; skeleton-blind regions judged on their own compare; every find recorded in Follow-up candidates). "
    "He also said the timing of D14-20 / D14-21 is \"inconsequential\" — this loop or a later one.",
    ""]
# 2. strike Needs Chris #20 / #21
k = find("20. **24 Sept (session 41 Round 1, r453)**")
L[k] = ("20. ~~**24 Sept (session 41 Round 1, r453)** — the MTK overview introduction's course-code heading (`[H1] TRR900`)~~ → "
        "**DECIDED D14-20 (drop it). QUEUED: next session's Round 2.**")
k = find("21. **24 Sept (session 41 Round 12)**")
L[k] = ("21. ~~**24 Sept (session 41 Round 12)** — the `Merge item N` lessons (CHI1003 / 1004 / 1005, JPN1004)~~ → **DECIDED D14-21 "
        "(no-source: out of every stat, comparison and future development). QUEUED: next session's Round 1 (the exclusion + "
        "re-baseline); r464 WITHDRAWN.**")
# 3. Position: r464 withdrawn
k = find("- **ROUND 12 (engine r464) BUILT, NOT SHIPPED — TOGGLED OFF, UNCOMMITTED**")
L[k] = ("- **No round in flight** (24 Sept 2026 ≈13:05, after the session-41 stop). **r464 WITHDRAWN by D14-21** — the four "
        "`Merge item N` modules leave all future work, so its note has nothing to serve; its two files were restored from the "
        "committed blobs (`git show HEAD:`), `git status` clean; the diff stays in `outputs/_r464_wip.patch`. Nothing was ever "
        "regenerated for it. LAST SHIPPED **r461** (260620.31); LAST FULL = **r460**; ledger **scoped #1**; plateau **2 of 3**. "
        "**QUEUED by Chris: Round 1 = D14-21 (the exclusion + re-baseline), Round 2 = D14-20 (drop the TRR900 heading)**; the "
        "standing §1g placement lane (D14-S1) in every PICK pass after them.")
# 4. STOPPED entry post-stop note
k = find("## >>> STOPPED 2026-09-24 12:50 NZST (session 41)")
L[k] = L[k].replace("Needs Chris: #17–#21 (#21 new). <<<",
                    "Needs Chris: #17–#19 open. **After the stop:** D14-20 / D14-21 decided, D14-S1 standing (§1g); r464 WITHDRAWN, tree clean. <<<", 1)
assert "After the stop" in L[k] and len(L[k]) <= 1500, len(L[k])
# 5. round-log note
k = find("- s41-r12 (engine r464")
L[k] = L[k] + " → **WITHDRAWN after the stop by D14-21** (backed out, tree clean)."
# 6. Follow-up candidates: the queued rounds + the placement residue
k = find("## Follow-up candidates")
L.insert(k + 1, "- **QUEUED BY CHRIS (D14, 24 Sept) — take these FIRST, in order:** (1) **D14-21** — add CHI1003 / CHI1004 / CHI1005 / "
         "JPN1004 to `compare_exclusions.txt` (reason: no-source, every lesson a `Merge item N` line) → fresh gate suite + skeleton "
         "json → re-baseline `gate_baseline.json` (pairs 2524 → 2524 minus their pairs) + the LOOP §0 census table's pair count → "
         "re-mine → mirror → commit (a measurement round: neither counts nor resets the plateau); (2) **D14-20** — drop the MTK "
         "introduction's `[H1] <course code>` heading (TRR overview pages; data flag + env `*_OFF`; named override of KB 07D's "
         "\"Typically: course code h1\"). Then the §1g placement census (D14-S1) as a standing lane.")
L.insert(k + 2, "- **(D14-S1 placement residue, s41) already measured — the first entries for §1g:** WJFUN112 / 113 / 115 / 116 — the "
         "gold gives Knowledge / Practices their own menu tabs, Claude drops the headings (the r410 tile dialect; r460 excluded "
         "WJFUN); 11 WJFUN modules / 18 menu panes are an empty \"Learning Intentions\" heading while the LI / SC text ships in the "
         "tile body (each module a different authoring form — r463 measured WJFUN116's alone); after r460's promotion the Overview "
         "pane ships ONE `col-md-6` / `col-md-12` column where KB c67 has Var 1 (two `col-md-6` paddingR / paddingL) or Var 2 "
         "(`col-md-8`) — FRNO902 Var 1, SCBI301 Var 2 at 5 + 5 items; BLL tabbed overviews split 12 own-tab / 7 Information (the "
         "open BLL263 D2 question — CL-0040 leaves it); the TRR bilingual cell's media follow all its paragraphs where the gold "
         "interleaves (r461's parked `media_in_place`: 27 up / 37 down). Evidence: `outputs/_s41_r8_kppane.log`, "
         "`_s41_r8_kptabs.log`, `_r460_rawmenu.log`, `_r462_companion.log`.")
# 7. Next session line
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** the standing `/loop-start`. Health check: census 552 / 545 / **2,675** pages / **2,524** "
        "pairs; `git status` CLEAN (r464 withdrawn). **Round 1 = D14-21** (CHI1003 / 1004 / 1005 + JPN1004 into "
        "`compare_exclusions.txt`; fresh gates; re-baseline `gate_baseline.json` + the §0 pair count; re-mine). **Round 2 = "
        "D14-20** (drop the TRR900 course-code heading). Then the miner + the NEW standing §1g placement census (D14-S1) in every "
        "PICK pass. LAST SHIPPED **r461** (260620.31); LAST FULL = **r460**; ledger scoped #1; plateau **2 of 3**. Needs Chris "
        "#17–#19.")
assert len(L[k]) <= 800, len(L[k])
out = "\n".join(L); tmp = S + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="\n").write(out); os.replace(tmp, S)
print("LOOP_STATE.md", n0, "->", os.path.getsize(S))
