#!/usr/bin/env python3
"""Session 50 STOP — the STOPPED entry, the session-50 decisions block, the round-log tidy (+ r11 / r16 lines), the archive
of the session-49 STOPPED entry, and the 'Next session starts with' line. WSL, from outputs/."""
import io, re
LS, AR = "../../LOOP_STATE.md", "../../LOOP_STATE_ARCHIVE.md"
with io.open(LS, encoding="utf-8", newline="") as f: L = f.read().split("\n")

# 1. the session-49 STOPPED entry -> archive verbatim; a pointer line replaces it; the session-50 entry goes on top
k49 = [i for i, l in enumerate(L) if l.startswith("## >>> STOPPED 2026-09-25 21:56 NZST (session 49)")]
assert len(k49) == 1, k49
s49 = L[k49[0]]
with io.open(AR, encoding="utf-8", newline="") as f: A = f.read()
A += "\n\n## STOPPED entry, session 49 (verbatim, s50 stop)\n\n" + s49 + "\n"
with io.open(AR, "w", encoding="utf-8", newline="") as f: f.write(A)
stop50 = ("## >>> STOPPED 2026-09-26 06:40 NZST (session 50) on §4 BUDGET — all 16 rounds used (the 16th a PICK pass that found no class "
          "at the floor; ≈ 7 h 35 m of the 10 h). **TEN ENGINE ROUNDS SHIPPED + TWO FULL BACKSTOPS, every one committed:** r510 the widget "
          "named after a generic interactive bracket (finished from s49), r511 D15-19 the yellow-✅ dropDown, r513 the bare [hover] paren def, "
          "r514 the writers' missing spellings, r515 KB c64 the animated-character Vimeo scaffold, r517 / r518 the typing quiz's table form + "
          "its verifier, r519 / r520 the drag-and-drop FIB form + its remainder, **r521 the new activity id ends the walk (+0.0400pp)**; "
          "FULL s50-r5 and s50-r14 (0 pages differ). Declined: r512, r516. Skeleton **55.5883 → 55.7889 % @ 2486**, ≥50 1602 → 1616, ≥75 "
          "277 → 286, ≥90 26, RAW 39.516 → 39.630; cs exact 16762 → 16772 (EXTRA 204, missing 887 → 886); body ANY 230 → 236 (every step "
          "NAMED); leak 52; **60.8 % of achievable** (ceiling 91.7 %). Plateau 0 of 3. Needs Chris: #1 / #10 only (human actions). <<<")
L[k49[0]] = stop50
L.insert(k49[0] + 1, "## STOPPED entry, session 49 (25 Sept 21:56, `/loop-stop`; r501–r509 shipped + the r505 FULL backstop, r510 toggled OFF — "
                     "finished by s50 Round 1) -> LOOP_STATE_ARCHIVE.md 'STOPPED entry, session 49 (verbatim, s50 stop)'. Superseded by the "
                     "session-50 entry above; every verdict stands.")

# 2. the session-50 decisions block, above the session-49 one
kd = [i for i, l in enumerate(L) if l.startswith("## Decisions from Chris (session 49 —")]
assert len(kd) == 1, kd
L.insert(kd[0], "## Decisions from Chris (session 50 — 2026-09-25 23:05 → 2026-09-26 06:40 NZST): the standing `/loop-start` kickoff only "
                "(the default budget, 16 rounds or 10 hours — the 16 rounds reached first) — NO new numbered decision; no new Needs-Chris item.")
L.insert(kd[0] + 1, "")

# 3. the round log: s50-r14 above s50-r13; s50-r16 and s50-r11 lines
def idx(prefix):
    r = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(r) == 1, (prefix, r)
    return r[0]
r14 = L.pop(idx("- s50-r14 ("))
L.insert(idx("- s50-r13 ("), r14)
L.insert(idx("- s50-r15 ("), "- s50-r16 (no engine change, 26 Sept 06:25 → 06:40) · a PICK pass only — the r521 family's rest (`_s50_r15_actid.log`: "
         "one more instance, ENGR202's '[Drag and drop Activity 2c]', under the floor); a NEW instrument, `_s50_r16_actnums.cjs` (the gold's "
         "activity numbers with no Claude activity: 2,346 over 345 modules — the developer's own numbering; 236 named in Claude's text, "
         "scattered: prose references, activity tags inside captured TABLE cells — 21 rows / 11 modules, under the floor) → no class at "
         "the floor; the session stops on §4 BUDGET (the 16th round).")
L.insert(idx("- s50-r10 ("), "- s50-r11 (no engine change, 26 Sept ≈04:20 → 04:27) · a PICK pass only — the literal-tag leak lane "
         "(`_s50_r11_leaks.py`: the 52 audited leaks grouped by bracket wording and module, scattered below the floor) and the hand-off lane "
         "(`_s43_wl2_run.sh s50`) → Round 12's pick (r519).")

# 4. the Next-session line (the last one in the file)
kn = [i for i, l in enumerate(L) if l.startswith("**Next session starts with:**")]
assert kn, "next line"
L[kn[-1]] = ("**Next session starts with:** `/loop-start` (16 rounds or 10 hours). The tree is CLEAN at the session-50 stop commit; "
             "no round in flight. LAST SHIPPED r521 (260620.82); LAST FULL r520 (the s50-r14 backstop); scoped #1; plateau 0 of 3; "
             "2,486 pairs; miner 194 CANDIDATE (all dispositioned). Round 1 = a PICK pass: the follow-up list's newest entries first (the "
             "FIB family's leftovers — the scanner's sentence head left outside a capture, CEDO402 / MXDI201 / MXDB302), then the §1g census, "
             "the dashboard's un-built widget rows, and the ride-along patches (r469 / r469b / r468 / r489 / r463 / r512).")
with io.open(LS, "w", encoding="utf-8", newline="") as f: f.write("\n".join(L))
print("stop ok", len("\n".join(L).encode("utf-8")))
