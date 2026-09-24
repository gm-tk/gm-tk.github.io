#!/usr/bin/env python3
"""Session 43 STOP (Chris's /loop-stop at 22:57, during r478's proof) — LOOP_STATE.md: the STOPPED entry (the s42 entry → archive),
the session-43 Decisions block, the r478 Position line (LAST BUILT, TOGGLED OFF, UNCOMMITTED), its PICK state, the Round-log line,
the Next-session line. Line edits only; .bak kept; every anchor found before anything is written. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
ss = io.open(S, encoding="utf-8", newline="").read(); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("## >>> STOPPED 2026-09-24 16:45 NZST (session 42)", "## Decisions from Chris (session 42 ", "- **ROUND 478 IN FLIGHT — NOT PROVEN**",
          "## Round log", "**Next session starts with:**", "## Session 43 — Round 10 PICK (engine r478)", "**Session 43 started:**"):
    find(p)
shutil.copyfile(S, S + ".pre-s43-stop.bak")
k = find("## >>> STOPPED 2026-09-24 16:45 NZST (session 42)"); s42 = L[k]
L[k] = ("## STOPPED entry, session 42 (24 Sept 16:45, §4 BUDGET; r465 / r466 / r467 / r470 shipped, the §1g placement census built) -> "
        "LOOP_STATE_ARCHIVE.md 'STOPPED entry, session 42 (verbatim, s43 stop)'. Superseded by the session-43 entry above; every verdict stands.")
L.insert(k, "## >>> STOPPED 2026-09-24 23:05 NZST (session 43) on Chris's `/loop-stop` (received 22:57, during r478's proof; 10 of the 12-round "
         "budget used, ≈ 5 h). **SIX ENGINE ROUNDS SHIPPED, every one committed:** r472 the flip-card text guard; r473 the modal text fence; r474 "
         "KB c52 every iStock alt (the FULL backstop); r475 / r476 / r477 KB c75 the writer's inline links (the menu, widget prose, gathered body "
         "text). **Three PICK passes** (R3 / R4 / R6; below-floor residue recorded). **r478 (KB c75 for the activity's lead) BUILT, PROBED, "
         "TOGGLED OFF at the stop — UNCOMMITTED** (its scoped ship held every gate but the mean, −0.0027pp, 16 down / 5 up, no crossing; a NAMED "
         "decision + the post-ship suite did not fit the stop's 10 minutes; the 13 modules regenerated back, manifest 0 pages differ). Skeleton "
         "**55.2245 → 55.2360 % @ 2491 (+0.0115pp)**, ≥50 1576 → 1577, ≥75 276 → 275 (−1 NAMED, r477), ≥90 25, RAW 39.194 → 39.195; cs exact "
         "16757 → 16759; body / clean / leak EXACT; 60.2 % of achievable (ceiling 91.7 %). Plateau 2 of 3. Needs Chris: #17–#19, #22 (none new). <<<")
k = find("## Decisions from Chris (session 42 ")
L.insert(k, "## Decisions from Chris (session 43 — 2026-09-24 18:06 → 23:05 NZST): the standing `/loop-start` kickoff (default budget, 12 rounds or "
         "10 hours) and, at 22:57, the standing `/loop-stop` (finish-and-commit if provable in under 10 minutes, else toggle OFF and leave it "
         "uncommitted-but-described; record decisions; \"Next session starts with:\"; commit what is finished; the §5 report; a safe-to-close "
         "sentence) — NO new numbered decision. Applied stop: r478 needed a NAMED mean-dip acceptance + the post-ship suite (≈ 12–15 min) → "
         "toggled OFF, its 13 modules regenerated back to the r477 bytes, engine + data left uncommitted and described in Position.\n")
k = find("- **ROUND 478 IN FLIGHT — NOT PROVEN**")
L[k] = ("- **LAST BUILT, TOGGLED OFF (UNCOMMITTED): r478** (session 43 Round 10; the marker was raised ≈ 22:50 real clock — the '23:02' first "
        "written ran ≈ 10 min ahead; toggled OFF at Chris's `/loop-stop`, 23:02): KB c75 FOR THE ACTIVITY'S LEAD PROSE. `app/js/ContentConverter.js` "
        "(`#weaveableLinks` — r477's filter factored out, `#leadLinks`, `flushLead`) + `data/Emit_Templates.json` `body_region.activity_lead_links` "
        "(**enabled: false**, env `LEADLINKS_OFF`) are MODIFIED AND UNCOMMITTED — never checkout / restore them. Proven so far: OFF probe 3222 / 3222 "
        "identical; ON 21 pages / 13 modules (`outputs/_affected_r478.txt`), 63 hrefs added (43 the gold carries, 20 public pages it drops; every "
        "one in `<p>` / `<b>` / `<i>` — `_s43_r10_parents.py`); regen + 12-module spot-check OK; `scoped_ship.sh` FAILED on the mean ONLY (55.2360 → "
        "55.2333, −0.0027pp, 16 down / 5 up, worst HES1007_8_0 −1.7 — the gold keeps HES1007's links but in a `<ul><li>` list; `_r478_skdelta.log`), "
        "every other gate HELD. Restored: the 13 regenerated with the flag off, `_content_manifest.py diff` IDENTICAL (0 pages differ) — the corpus "
        "IS the r477 state. The next health check's engine-checksum FAIL on these two files is this round, not a crash.")
k = find("## Session 43 — Round 10 PICK (engine r478)")
L[k] = "## Session 43 — Round 10 PICK (engine r478) — KB c75 FOR THE ACTIVITY'S LEAD PROSE (BUILT, TOGGLED OFF at the stop — UNCOMMITTED)"
j = k + 1
while j < len(L) and not L[j].startswith("## "): j += 1
while j > k + 1 and not L[j - 1].strip(): j -= 1
L.insert(j, "- **State at the stop (23:05):** see the Position line. **To finish (the next session's Round 1):** set `enabled: true`; re-run "
         "`bash outputs/_s42_probe_run.sh r478 ON` (expect the same 13); `bash outputs/_r478_regen.sh`; `scoped_ship.sh --affected "
         "../../outputs/_affected_r478.txt --toggle LEADLINKS_OFF --no-regen --commit --round 478` → on the mean-only FAIL, commit NAMED with "
         "`_fastloop_diff.py <the 13 + the spot-check sample> --accept-named \"skeleton SCAFFOLD mean %\" --commit` (§1b: KB c75 outranks the "
         "gold; the r475 −0.0006pp precedent; 43 of 63 hrefs gold-carried — name the list-form pages HES1007_3…8 and the gold-dropped links); "
         "then `_r478_postship.sh`, the finalise (AppVersion 260620.41 → 260620.42), checksums, mirror, commit. Recommendation: accept NAMED.")
k = find("## Round log")
L.insert(k + 1, "- s43-r10 (engine r478, NOT shipped, 24 Sept ≈22:48 → 23:05 real clock) · KB c75 FOR THE ACTIVITY'S LEAD PROSE (the bundle-owned "
         "activity's `flushLead`; HES1007 3B's reading list) · BUILT + PROBED (63 hrefs, 43 gold-carried) · scoped ship FAILED on the mean "
         "−0.0027pp (16 down / 5 up, no crossing) · TOGGLED OFF at `/loop-stop`, corpus restored (manifest 0 differ), engine + data UNCOMMITTED · "
         "plateau 2 of 3 (neither).")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** the standing `/loop-start`. **Round 1 = FINISH r478** (LAST BUILT, TOGGLED OFF, UNCOMMITTED — the health "
        "check's engine-checksum FAIL on ContentConverter.js / Emit_Templates.json is this round, not a crash; the corpus is the r477 state): "
        "enable `body_region.activity_lead_links`, re-probe, `_r478_regen.sh`, scoped ship, commit NAMED on the mean (the PICK's 'To finish' "
        "line), `_r478_postship.sh`, finalise. LAST SHIPPED **r477** (260620.41); LAST FULL = **r474**; ledger scoped #3; plateau **2 of 3**; "
        "2,491 pairs; census 552 / 545 / 2,679. Needs Chris #17–#19, #22.")
k = find("**Session 43 started:**")
L[k] = L[k] + " **Stopped 23:05 on Chris's `/loop-stop`** (10 rounds: 6 shipped, 3 PICK passes, r478 toggled OFF uncommitted)."
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## STOPPED entry, session 42 (verbatim, s43 stop)\n\n" + s42 + "\n")
tmp = S + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write("\n".join(L)); assert os.path.getsize(tmp) > 50000; os.replace(tmp, S)
print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
