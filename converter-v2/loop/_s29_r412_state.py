#!/usr/bin/env python3
"""r412 finalise — LOOP_STATE.md: the Round 3 PICK section moves to the archive (+ the what-shipped record), the Position updates,
the Round-log line is appended."""
import os
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
STATE, ARCH = R + "LOOP_STATE.md", R + "LOOP_STATE_ARCHIVE.md"
lines = open(STATE, encoding="utf-8").read().split("\n")
def idx(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix): return i
    raise SystemExit("not found: " + prefix)

# the PICK section: from its heading to the '## Round log' heading
a = idx("## Session 29 — Round 3 PICK (engine r412)"); b = idx("## Round log")
pick = lines[a:b]
shipped = ("- **What shipped (r412, build 260619.83, 20 Sept ≈16:20):** `BoundaryBank._meta.opener_rule.heading_table_owner {enabled, env HEADTABLE_OFF, types, heading_tags, "
           "between_tags, max_between}` + `InteractiveScanner.#headingTableOwner` right after the member walk (a synthetic bare owner — the r402 shape —, the heading + prose "
           "as activityLeadItems, instruction spans as the bundle's instructions, the walk resumed AT the table). Probe OFF = disk 2555 / 2555; ON 24 pages / 18 modules "
           "(17 census pages + TEDC401 3–6 index-only + XGF9003 1.2 / 1.3 the r223 letter continuation); scored on the ON pages 14 up / 3 down / 7 same, +32.6pp-sum "
           "scaffold / +17.5 RAW (the dips named: HPFUN201_0_0 −7.0 the family's un-boxed minority, TEDC401_2_0 −5.6 the gold's own box 2D with the hand-off dump inside, "
           "HES1002_5_0 −2.4 a mispaired page); SCOPED regeneration of the 18 + the 12-module sample (4 batches rc 0; `scoped_ship.sh` 0 stale, containment 18 ⊆ 18, "
           "spot-check 12 / 12; the fast-loop commit with the NAMED `compare_structure exact chain` −1 = the matched pool −1, SCES201 alone — the r57 / r147 relocation "
           "class); skeleton 53.7949 → 53.8088 % (+0.0139pp; 17 movers 14 up / 3 down, 0 outside the set), ≥50 1406 → 1408 (TEFUN06_0_0, AGH1006_8_0), ≥75 236 / ≥90 20 EXACT, "
           "RAW 37.963 → 37.970 %; body_compare / defect / every verifier EXACT; 9 new 03B dragAndDrops (defect 0); 16 selftests GREEN; feature index GREEN; ledger scoped #4 "
           "since the 19 Sept FULL; miner 182 → 182 (the class lives below the miner's floor); checksums engine 4 changed / gates 0.")
lines[a:b] = ["## Session 29 — Round 3 (engine r412) — the heading-then-table shape after an empty typed-widget invocation takes the owner form — SHIPPED; the PICK + what-shipped record is in LOOP_STATE_ARCHIVE.md 'Session 29 — Round 3 PICK (engine r412) + what shipped'; the one-line summary is the s29-r3 Round-log line below.", ""]

# Position
p = idx("- LAST SHIPPED: **r411**")
lines[p] = ("- LAST SHIPPED: **r412** (build 260619.83, 20 Sept ≈16:20, session 29 Round 3 — THE HEADING-THEN-TABLE SHAPE AFTER AN EMPTY TYPED-WIDGET INVOCATION TAKES THE OWNER FORM, "
            "the r407-recorded follow-up at the normal widget path: `opener_rule.heading_table_owner`, env `HEADTABLE_OFF`; the gold boxes the section 15 / 17 = 0.88 (10 / 13 without WJFUN); "
            "probe OFF = disk 2555 / 2555, ON 24 pages / 18 modules (14 up / 3 down, named); SCOPED regeneration of the 18 — scoped ship #4 since the 19 Sept FULL (4 of headroom); "
            "**skeleton 53.795 → 53.809 % (+0.0139pp), ≥50 1406 → 1408, ≥75 236 / ≥90 20 EXACT, RAW 37.963 → 37.970 % @ 2349 pairs**; compare_structure exact −1 = the matched pool −1 "
            "(SCES201, named, the relocation class); every other gate EXACT; 9 new 03B dragAndDrops; 16 selftests GREEN; the miner 182 → 182); before it **r411** (build 260619.82, "
            "20 Sept ≈15:35, session 29 Round 2 — the tile dialect's menu takes the gold's ROW+COL tabs shell, `TILEMENUROW_OFF`: 21 up / 0 down, +0.0058pp) and **r410** (build 260619.81, "
            "20 Sept ≈15:05, session 29 Round 1 — the WJFUN tile-page dialect, `TILEPAGE_OFF`: 21 up / 0 down, skeleton 53.680 → 53.789 %, ≥50 +8, WJFUN 37.6 → 49.9 %). "
            "**Corpus = r412** (2555 pages / 494 dirs / 2349 pairs; `gate_baseline.json` at r412; `outputs/_s29_r412_sk_final.json` the skeleton state; ceiling 90.9 % → 53.809 = **59.2 % of achievable**).")
q = idx("- Plateau window (§4): **1 of 3**")
lines[q] = "- Plateau window (§4): **0 of 3** — r412 RESET it (+0.0139pp with ≥50 +2 — a bucket moved); r411 had been the first (+0.0058pp, nothing else moved). Read every delta on the post-intake 2,349-pair population (§1e)."
r = idx("- Standing facts: AppVersion 260619.82")
lines[r] = lines[r].replace("AppVersion 260619.82 (r411, session 29 Round 2, 20 Sept); before it 260619.81 (r410) / 260619.80 (r409)", "AppVersion 260619.83 (r412, session 29 Round 3, 20 Sept); before it 260619.82 (r411) / 260619.81 (r410) / 260619.80 (r409)")
assert "260619.83" in lines[r]

# Round-log line after the s29-r2 line
t = idx("- s29-r2 (engine r411")
lines.insert(t + 1, "- s29-r3 (engine r412, build 260619.83, 20 Sept ≈15:45 → 16:20) · THE HEADING-THEN-TABLE SHAPE AFTER AN EMPTY TYPED-WIDGET INVOCATION TAKES THE OWNER FORM (a bare `[drag and drop]` / `[Interactive activity]` / `[Activity 2C][drag and drop]` + the writer's `[H3]` + prose + TABLE → the gold's `activity interactive` box with the h3 title, the lead prose and the BUILT widget — the r407-recorded follow-up at the normal path; `opener_rule.heading_table_owner` + `InteractiveScanner.#headingTableOwner`, env `HEADTABLE_OFF`; found by the live-scanner census `_s29_r3_headwalk.cjs` + `_s29_r3_goldcheck.py`: 31 bundles / 29 pages / 28 modules, gold box 15 / 17 = 0.88, 10 / 13 without WJFUN) · SHIPPED · probe OFF = disk 2555 / 2555, ON 24 pages / 18 modules (14 up / 3 down, +32.6) · SCOPED regen of the 18 (scoped #4 since the 19 Sept FULL; 0 stale; spot-check 12 / 12) · skeleton 53.795 → 53.809 (+0.0139pp), ≥50 +2; cs exact −1 = pool −1 (SCES201, named); all else EXACT · 9 new 03B dragAndDrops · miner 182 → 182 · plateau RESET 0 of 3 · recorded: the 12 unclassified-path census pages (already the r362 / r407 form), the 22 declined tables inside the new boxes, HPFUN201's un-boxed minority")

open(STATE, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
with open(ARCH, "a", encoding="utf-8") as f:
    f.write("\n## Session 29 — Round 3 PICK (engine r412) + what shipped — the heading-then-table shape after an empty typed-widget invocation takes the owner form (20 Sept ≈15:45 → 16:20 NZST)\n\n" + "\n".join(pick).rstrip("\n") + "\n" + shipped + "\n")
print("LOOP_STATE.md", os.path.getsize(STATE), "bytes; archive", os.path.getsize(ARCH))
