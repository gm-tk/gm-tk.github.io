#!/usr/bin/env python3
"""SESSION 28 / TASK 1 — LOOP_STATE.md: the corrected census (the 19 Sept intake handover's §2), the r408 position, the
round-log line, the 'Next session starts with' line. Idempotent; LF preserved; size-checked (target ≤ 100 KB). WSL."""
import io, os
P = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/LOOP_STATE.md"
s = io.open(P, encoding="utf-8", newline="").read()
if "Session 28 (pre-loop" in s:
    print("already updated"); raise SystemExit

# 1. the session note + the corrected census, right after the session-27 start line
A = "**Session 27 started:** 2026-09-19 08:42 NZST"
i = s.index(A); j = s.index("\n", i) + 1
NOTE = ("**Session 28 (pre-loop, NOT a loop session — Chris's `NEXT_SESSION__Pre_Loop_Fixes.md` four tasks) started:** 2026-09-20 ≈09:40 NZST (Claude Code, Opus 5, "
        "Chris's Windows machine). **THE CENSUS, corrected (the 19 Sept intake handover §2 — the session-27 figures below are stale):** gold dirs **552** "
        "(454 before the 98-module September intake) · docx **762** · Claude dirs **494** · Claude pages **2,555** after Task 1 (2,613 at the 19 Sept regen; the 21 WJFUN + "
        "JPFUN01 collapsed to the gold's one page) · the gates' paired pages **2,349** · **ship ledger: scoped #1 since the 19 Sept FULL** (r408 — headroom 7 before the "
        "backstop) · plateau window **0 of 3**, untouched · **the ceiling (91.6 % / 1880 pairs) is VOID on this corpus — `_measure_ceiling.py` not yet re-run over the 2,349 "
        "pairs; `COVERAGE_DASHBOARD.md` / `_coverage_dashboard.json` last built on the r349 corpus — both unmeasured until re-run** · gate baseline = the whole 2,349-pair "
        "population (re-based 19 Sept; method `gate_baseline.json._meta._note_intake_2026_09_19`; a metric that looks lower must be SPLIT BY POPULATION first) · "
        "`_gatecheck.py` prints CACHED rows for gates it did not run — read compare_structure / body_compare from `run_all_gates.sh`'s own output or run `cs bc`.\n")
s = s[:j] + NOTE + s[j:]

# 2. Position: LAST SHIPPED + standing facts
OLD = "- LAST SHIPPED: **r407** (build 260619.78, 19 Sept ≈16:35, session 27 Round 12 — the heading-led numbered opener takes the owner form too;"
assert s.count(OLD) == 1, "LAST SHIPPED anchor"
NEW = ("- LAST SHIPPED: **r408** (build 260619.79, 20 Sept ≈11:30, session 28 pre-loop Task 1 — THE MINED REGISTRIES REBUILT OVER THE 552-MODULE GOLD CORPUS: "
       "Module_Structure_Index module_meta 454 → 552, 24 new Style-Anchor bases (WJFUN + JPFUN single-file), the Menu / Convention / lexicon / feature / consensus "
       "registries, the NEW `data/Subject_Prefix_Map.json` (labels PROPOSED — Chris approves), FRFUN held back (measured); SCOPED regen of the 103 modules the probe named, "
       "scoped ship #1 since the 19 Sept FULL; skeleton 53.134 → 53.680 % (+0.5455pp), ≥50 +20, ≥75 +8, ≥90 +1; WJFUN 10.4 → 37.6 %; miner 187 → 183); before it "
       "**r407** (build 260619.78, 19 Sept ≈16:35, session 27 Round 12 — the heading-led numbered opener takes the owner form too;")
s = s.replace(OLD, NEW, 1)
OLD = "- Standing facts: AppVersion 260619.78 (session 27 STOPPED 19 Sept ≈16:40 on the budget);"
assert s.count(OLD) == 1, "standing facts anchor"
s = s.replace(OLD, "- Standing facts: AppVersion 260619.79 (r408, session 28 pre-loop Task 1, 20 Sept); before it 260619.78 (session 27 STOPPED 19 Sept ≈16:40 on the budget);", 1)

# 3. the round-log line after s27-r12
A = "- s27-r12 (engine r407) · THE HEADING-LED NUMBERED OPENER TAKES THE OWNER FORM TOO"
i = s.index(A); j = s.index("\n", i) + 1
LINE = ("- s28-t1 (data r408, build 260619.79, 20 Sept) · THE MINED REGISTRIES REBUILT OVER THE 552-MODULE GOLD CORPUS (module_meta 454 → 552 with the 98 intake codes; 24 "
        "new Style-Anchor bases mined per family with `ReferenceMiner.Distil` — WJFUN + JPFUN `page_model single-file`, the r265 CHFUN precedent; the r263 floor-flip rows "
        "ANZHFUN / ENO / XOTP* corrected; Menu 120 → 174 groups / 370 → 525 series rows; Convention 43 → 52 groups, 14 re-measured; lexicon 61 → 66; feature index 552; legacy "
        "consensus 604 / 147; `Subject_Prefix_Map.json` PROPOSED; FRFUN held back — its faithful row scored 26 / 28 pages down under the HPFUN `[New tab]` panel sentinel; "
        "cascade / parity pins re-pinned BLL254 body|@p + MXDI101 menu|@p). Probe OFF = pre snapshot 2613 / 2613, ON 457 pages / 103 modules; scoped regen of the 103, "
        "0 stale, probe == disk 590 / 590. **Skeleton 53.134 → 53.680 % (+0.5455pp; 275 movers 197 up / 76 down, 0 outside the set, the 1813 unaffected pairs EXACT), "
        "≥50 1378 → 1398, ≥75 228 → 236, ≥90 19 → 20, RAW 37.487 → 37.884 %; WJFUN 21 modules 10.4 → 37.6 %**; compare_structure exact 13410 → 14091 (pool +746) / 186 / "
        "690 (+2 / +5 inside five newly single-file modules, named); body_compare 54 / 6 / 190 / 248 (EMPTY −2, ANY −2); defect pages 44 / leak 73 EXACT (2548 pages now); "
        "every verifier EXACT; 46 selftest lines GREEN; miner 187 → 183 — the five WJFUN chrome rows collapsed as one; `nav:phases` MISSING (WJFUN's in-page phases, "
        "38 pages) is Task 3's remaining class.\n")
s = s[:j] + LINE + s[j:]

# 4. Next session starts with
OLD = "**Next session starts with:** the standing `/loop-start`; health check (locks, `verify_after_transfer.sh` PASS, `wc -c`); `git status` in pageforge-site: a CLEAN tree at the session-27 stop commit (r407 beneath it);"
assert s.count(OLD) == 1, "next-session anchor"
NEW = ("**Next session starts with:** the standing `/loop-start`; health check (locks, `verify_after_transfer.sh` PASS — its census is now 552 gold / 494 Claude dirs / 762 docx "
       "/ 2,555 Claude pages, `wc -c`); `git status` in pageforge-site: a CLEAN tree at the session-28 commits (r408 + the Task 2 / 3 / 4 rounds beneath it); **FIRST re-run "
       "`_measure_ceiling.py` over the 2,349-pair corpus and rebuild `COVERAGE_DASHBOARD.md` — both are void on this corpus**; the miner's queue (20 Sept, the r408 corpus) is "
       "current — 183 CANDIDATE rows; `nav:phases` MISSING for WJFUN (38 pages) is the standing lead unless the session-28 Task 3 round closed it; "
       "**Chris's pending decision: the `Subject_Prefix_Map.json` labels (session 28 report)**; the ledger is at scoped #1 since the 19 Sept FULL; [the session-27 line follows] "
       "the standing `/loop-start`; health check (locks, `verify_after_transfer.sh` PASS, `wc -c`); `git status` in pageforge-site: a CLEAN tree at the session-27 stop commit (r407 beneath it);")
s = s.replace(OLD, NEW, 1)
io.open(P, "w", encoding="utf-8", newline="").write(s)
print("LOOP_STATE.md updated;", len(s.encode("utf-8")), "bytes")
