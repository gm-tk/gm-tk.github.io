#!/usr/bin/env python3
"""Session 41 /loop-stop — LOOP_STATE.md: the s41 STOPPED entry (the s40 one moved verbatim to the archive), the session's
Decisions-from-Chris block, the r464 Position line (BUILT, NOT SHIPPED, toggled OFF, uncommitted), the r464 PICK's result line,
the s41-r12 round-log line, the clock correction, and the "Next session starts with:" line. .pre-s41-stop.bak kept. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
shutil.copyfile(S, S + ".pre-s41-stop.bak")
s = io.open(S, encoding="utf-8").read(); L = s.split("\n"); n0 = len(s.encode("utf-8"))
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
# 1. STOPPED entries
i = find("## >>> STOPPED 2026-09-24 05:30 NZST (session 40)"); s40 = L[i]
stop = ("## >>> STOPPED 2026-09-24 12:50 NZST (session 41) on CHRIS'S `/loop-stop` — received during Round 12, the last of the "
        "12-round budget (≈ 5 h 25 min; the 10 h cap not reached). **EIGHT ENGINE ROUNDS SHIPPED, r453–r461, every one "
        "committed:** r453 the MTK overview-table tabs; r454 the red `[Activity: Embedded]` marker; r456–r459 the page model (a "
        "mid-page lesson heading, section-label markers, placement notes, the introduction on the overview); r460 KB c67 Knowledge "
        "/ Practices tabs (THE FULL BACKSTOP); r461 the audio-image unit. **Three DECLINED** (r455, r462, r463 — reverted, patches "
        "kept). **r464 (the untagged `Merge item N` line) BUILT, NOT SHIPPED:** its data flag is OFF and its two files are "
        "UNCOMMITTED (`outputs/_r464_wip.patch`). Skeleton **54.7484 % @ 2477 → 54.9477 % @ 2524 (+0.1993pp)**, ≥50 1544 → 1581, "
        "≥75 260 → 275, ≥90 23 → 25, RAW 38.60 → 38.98; cs exact 15657 → 16719; body ANY 237 → 239 and missing 796 → 896 NAMED "
        "(new pages); 60.0 % of achievable. Plateau 2 of 3. Needs Chris: #17–#21 (#21 new). <<<")
L[i] = stop
L.insert(i + 1, "## STOPPED entry, session 40 (24 Sept 05:30, §4 BUDGET; r447–r452 shipped) -> LOOP_STATE_ARCHIVE.md 'STOPPED entry, "
         "session 40 (verbatim, s41 stop)'. Superseded by the session-41 entry above; every verdict stands.")
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## STOPPED entry, session 40 (verbatim, s41 stop)\n\n" + s40 + "\n")
# 2. Decisions from Chris (session 41)
k = find("## Decisions from Chris (session 40")
L.insert(k, "## Decisions from Chris (session 41 — 2026-09-24 07:25 → 12:50 NZST): the standing `/loop-start` kickoff (default budget, "
         "12 rounds or 10 hours) and, at 12:48, `/loop-stop` with one addition — \"then tell me how many rounds took place in "
         "addition to the normal loop-stop processes\" (answered in the §5 report: 12 rounds). NO new numbered decision. One new "
         "Needs-Chris item was raised (#21, the `Merge item N` lessons); #20 (the TRR900 course-code heading) was raised at r453.")
L.insert(k + 1, "")
# 3. Position line for r464
i = find("- **ROUND 12 (engine r464) IN FLIGHT — NOT PROVEN**")
L[i] = ("- **ROUND 12 (engine r464) BUILT, NOT SHIPPED — TOGGLED OFF, UNCOMMITTED** (24 Sept 2026, stopped by `/loop-stop` at "
        "12:48): THE UNTAGGED `Merge item N` LESSON LINE (`asset_todo_notes.black_line.unbracketed`, env `TODOMERGELINE_OFF`). "
        "Its two files are loose in `pageforge-site`: `converter-v2/app/js/ContentConverter.js` (#assetTodoPrepass) and "
        "`converter-v2/data/Emit_Templates.json` (the `unbracketed` block, **`enabled: false`** — so a regeneration reproduces "
        "the r461 corpus; checked: CHI1003 / 1004 / 1005 / JPN1004 42 / 42 pages identical). The diff: `outputs/_r464_wip.patch`. "
        "Nothing was regenerated; the corpus on disk is the r461 state. LAST SHIPPED **r461** (260620.31); LAST FULL = **r460**; "
        "ledger **scoped #1**; plateau **2 of 3**.")
# 4. the r464 PICK's result
i = find("## Session 41 — Round 12 PICK (engine r464)")
j = i + 1
while j < len(L) and L[j].startswith("- "): j += 1
L.insert(j, "- **Measured before the stop** (`outputs/_r464_probe_run.sh`, `_r464_companion.log`): OFF 3217 / 3217 identical; ON "
         "21 pages / 3 modules (CHI1003 / 1004 / 1005 — JPN1004's lines differ in form); **17 up / 3 down, pp-sum −0.3** — the "
         "dips CHI1003_8_0 −1.6, CHI1004_3_0 −1.3, CHI1004_8_0 −1.4 have NO rising companion (the note paragraph carries a class "
         "the gold's lesson body lacks). Not provable inside the stop's 10 minutes → toggled OFF, left uncommitted.")
# 5. round log + clock note
k = find("## Round log")
L.insert(k + 1, "- s41-r12 (engine r464, 24 Sept ≈12:40 → 12:48, real clock) · THE UNTAGGED `Merge item N` LESSON LINE (a "
         "recognition round) · BUILT, PROBED (21 pages, 17 up / 3 down, pp-sum −0.3), NOT SHIPPED — `/loop-stop` arrived; data flag "
         "OFF, two files uncommitted (`outputs/_r464_wip.patch`) · Needs Chris #21 raised · clock note: the ≈ times written on "
         "s41-r10 → r12 (≈13:10 / 13:40 / 14:25) ran ≈ 45–100 min ahead of the real clock (12:25 / 12:35 / 12:42).")
# 6. Next session line
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** the standing `/loop-start`. Health check: census 552 / 545 / **2,675** pages / **2,524** "
        "pairs. `git status` WILL show two loose files — `converter-v2/app/js/ContentConverter.js` + `converter-v2/data/"
        "Emit_Templates.json` = **r464** (the untagged `Merge item N` line, `TODOMERGELINE_OFF`, data flag OFF, not regenerated; "
        "diff `outputs/_r464_wip.patch`): Round 1 = finish it (flag ON, name its 3 dips, scoped ship CHI1003 / 1004 / 1005) or "
        "back its hunks out by hand — never `git checkout`. LAST SHIPPED **r461** (260620.31); LAST FULL = **r460**; ledger scoped "
        "#1; plateau **2 of 3**. Needs Chris #17–#21.")
assert len(L[k]) <= 800, len(L[k])
out = "\n".join(L); tmp = S + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="\n").write(out); os.replace(tmp, S)
print("LOOP_STATE.md", n0, "->", os.path.getsize(S), "; stopped entry", len(stop), "chars")
