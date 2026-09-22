#!/usr/bin/env python3
"""ROUND 0d (session 33 Round 3) — LOOP_STATE.md: the Round-log line, Position (LAST FULL = intake-2026-09-22, the corpus bullet), the
miner line, the ceiling bullet, the next-session line; the archive record. Run under WSL."""
import re
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)
st = rd(R + "LOOP_STATE.md"); ar = rd(R + "LOOP_STATE_ARCHIVE.md")
o = "- s33-r2 (engine r422 ENABLED, build 260619.98"
assert st.count(o) == 1
line = ("- s33-r3 (ROUND 0d · intake 2026-09-22 · 38 modules · no engine change, build 260619.98, 22 Sept ≈11:25 → ≈12:20) · THE 38 PRE-INTAKE NEVER-CONVERTED "
        "MODULES (the 22 Sept review's finding — never in compare_set, never reached by a full regen): 38 / 38 converted, 0 refused, 0 ghost dirs; 161 pages / 114 "
        "pairs · the FULL regeneration on the unchanged registries (42 batches rc 0, 0 stale, the 504 pre-existing modules byte-identical; ledger FULL at "
        "intake-2026-09-22, counter 0) · SPLIT BY POPULATION (`_intake_split.py`): the 2377 pre-existing pairs EXACT = r422e, 0 movers; the new 114 pairs 51.42 % "
        "(67 ≥50 / 16 ≥75 / 3 ≥90) · re-based: skeleton 54.1172 % @ 2491 / 1531 / 254 / 23, cs 15131 / 194 / 773 / 23, body 57 / 5 / 206 / 265, clean "
        "2690 / 2736, leak 75 / 46 (BLL260's 2 pages) · ceiling 91.2 % → 59.4 % of achievable · miner 184 → 190 (the six new rows = the single-page Inquiry "
        "page-model family: 8 golds Claude over-splits at 3–10 %) · dashboard rebuilt · handover `LOOP_INTAKE__2026-09-22_38_Modules.md` (§7: the page-model "
        "registry rows first) · corpus 2744 / 545 / 2491 · plateau window unchanged (a population round)\n")
st = st.replace(o, line + o)
o = "- LAST SHIPPED: **r422 ENABLED** (build 260619.98"
assert st.count(o) == 1
st = st.replace(o, ("- LAST FULL: **ROUND 0d — the 22 Sept 2026 intake of the 38 pre-intake never-converted modules** (session 33 Round 3, no engine change, "
                    "build 260619.98; ledger FULL at `intake-2026-09-22`, counter 0; **corpus = 2744 pages / 545 dirs / 2491 pairs**; `gate_baseline.json` at "
                    "`intake-2026-09-22` (`_note_intake_2026_09_22`) — **skeleton 54.1172 % @ 2491, ≥50 1531, ≥75 254, ≥90 23, RAW 38.049 %**; cs 15131 / 194 / 773 / 23; "
                    "body 57 / 5 / 206 / 265; clean 2690 / 2736 = 98.32 %; leak 75 / 46; the 2377 pre-existing pairs EXACT = r422e; `outputs/_intake_2026-09-22_sk_final.json` "
                    "the skeleton state; **ceiling 91.2 % on 2491 pairs (`_ceiling_intake_2026-09-22`) → 54.117 = 59.4 % of achievable**; the miner re-run 22 Sept 11:51, "
                    "190 CANDIDATE; the handover `LOOP_INTAKE__2026-09-22_38_Modules.md`, §7 = the queue). LAST ENGINE SHIP: **r422 ENABLED** (build 260619.98"))
o = "`DIFF_QUEUE.md` 22 Sept 11:09 on the r422e corpus (2,377 pairs / 496 modules), 184 CANDIDATE rows — re-mined after every ship)."
assert st.count(o) == 1
st = st.replace(o, "`DIFF_QUEUE.md` 22 Sept 11:51 on the intake-2026-09-22 corpus (2,491 pairs / 533 modules), 190 CANDIDATE rows — re-mined after every ship; the scoped miner over the 38 in `outputs/_diff_miner_scoped.md`).")
o = "- Plateau window (§4): **1 of 3** — r422e predicted"
assert st.count(o) == 1
st = st.replace(o, "- Plateau window (§4): **1 of 3** — the 22 Sept Round 0d is a population round (does not count); r422e predicted")
m = re.search(r"^\*\*Next session starts with:\*\* .*$", st, re.M); assert m
nxt = ("**Next session starts with:** the standing `/loop-start` (health check — the census is now 552 gold / 545 Claude dirs / 2,744 Claude pages; the \"Amended:\" "
       "line; the §7 diff check; `git status` CLEAN at the session-33 commits). No round in flight. r425 finished, r422 enabled, the 38 never-converted modules "
       "intaken (22 Sept). The re-ranked queue is `LOOP_INTAKE__2026-09-22_38_Modules.md` §7: **(1) the single-page Inquiry page-model registry rows** — BLL250 / "
       "260 / 270, CEDK401, CEDO402, TWHT903, CEDR101, CEDR401 over-split at 3–10 % (a `page_model` row / exception per code, measured per module in memory first, "
       "its own ledgered round with a named delta); (2) the lesson chip `lesson-number` vs `decimal-number` (14 modules); (3) #4177 the `col-md-6 > img` EXTRA "
       "(19 modules); (4) the standing miner queue (190 CANDIDATE) under §3 / §4, one untried lane before any exhaustion verdict. NEEDS CHRIS: the open lines of "
       "the \"Needs Chris\" section (a new item = one new line there).")
st = st[:m.start()] + nxt + st[m.end():]
record = """## Session 33 — Round 3 (ROUND 0d, the 22 Sept 2026 intake of the 38 pre-intake never-converted modules; no engine change; 22 Sept ≈11:25 → ≈12:20)

**PICK (the 22 Sept review's Round 3; LOOP §0 + §1f).** The 38 gold modules the review's adversarial check found with a Writers Template and no Claude dir (never in `compare_set.txt`; unreachable by a full regeneration because `_batch_plan.py` enumerates Claude dirs). Phase 1 skipped (placed, parsed, every code a `Module_Structure_Index` key — `_intake_2026-09-22_delta.txt`).

**WHAT HAPPENED.** Phase 2: the 38 nested dirs pre-created in their gold folders (21 Standard / 16 Inquiry / 1 Bilingual), converted by explicit code list in four batches (`_intake_2026-09-22_convert.sh`, rc 0 × 4): **38 / 38, 0 refused, 0 ghost dirs; 161 pages** (`_results.txt`). Phase 3: the FULL regeneration on the unchanged registries (`_fullship_par.sh`: 42 batches, 6 min, rc 0; 0 stale; `_content_manifest.py changed` = exactly the 38; the 504 pre-existing modules byte-identical); `run_all_gates.sh`; `_intake_split.py` (NEW — the generalised `_s28_t1_split.cjs`, kept): the 2377 pre-existing pairs EXACT = r422e on every gate (0 movers); the new 114 pairs 51.42 % / 67 / 16 / 3, cs 813 / 8 / 84 / 0, body ANY 14, clean 158 / 160, leak 2 (BLL260); the whole population re-based — skeleton **54.1172 % @ 2491 / 1531 / 254 / 23**, cs 15131 / 194 / 773 / 23, body 57 / 5 / 206 / 265, clean 2690 / 2736, leak 75 / 46; every verifier ✓; 17 selftests GREEN; `_gatecheck.py`'s REGRESSED rows all population arithmetic; ledger `record-full --round intake-2026-09-22`, fast-loop + manifest snapshots. Phase 4 NOT skipped but deferred to its own round: the low scorers are the eight single-page Inquiry golds Claude over-splits (BLL250 8 / BLL260 13 / BLL270 5 / CEDK401 12 / CEDO402 6 / TWHT903 5 / CEDR101 2 / CEDR401 2 pages vs 1) — their codes are in no Style-Anchor level's members / `page_model_exceptions`. Phase 5: the ceiling re-measured (91.2 % → 59.4 % of achievable), the dashboard rebuilt (`--allow-stale` — the feature index was rebuilt after the census in the same script, a same-corpus mtime nit), the miner full (190 CANDIDATE, six new rows = the page-model family + #4177) and scoped (11 CANDIDATE; F15 / F16 crumbs + inquiry footer, F1 / F2 the lesson chip), the feature index GREEN. Phase 6: the changelog entry, OPERATING_GUIDE §9 / §14, `gate_baseline.json` (`_note_intake_2026_09_22`), the loop file's §0 table + no-build paragraph + §2 bullet, the verify script (`.pre-intake-2026-09-22.bak`), the checksums, `NEW_MODULES__Intake_2026-09-22.md` + `LOOP_INTAKE__2026-09-22_38_Modules.md`. Phase 7: the queue re-ranked (the handover's §7; the pre-intake exhaustion verdicts VOID).
"""
ar = ar.rstrip("\n") + "\n\n" + record + "\n"
wr(R + "LOOP_STATE.md", st); wr(R + "LOOP_STATE_ARCHIVE.md", ar)
print("STATE_INTAKE_DONE", len(st))
