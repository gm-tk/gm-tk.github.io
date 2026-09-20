#!/usr/bin/env python3
"""r413 finalise — LOOP_STATE.md: the Round 4 PICK section moves to the archive (+ the what-shipped record), the Position updates,
the Round-log line is appended."""
import os
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
STATE, ARCH = R + "LOOP_STATE.md", R + "LOOP_STATE_ARCHIVE.md"
lines = open(STATE, encoding="utf-8").read().split("\n")
def idx(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix): return i
    raise SystemExit("not found: " + prefix)
a = idx("## Session 29 — Round 4 PICK (engine r413)"); b = idx("## Round log")
pick = lines[a:b]
shipped = ("- **What shipped (r413, build 260619.84, 20 Sept ≈17:35):** `heading_table_owner.owned_bundles {enabled, env HEADTABLEOWNED_OFF, between_media_tags}` — "
           "`#headingTableOwner` accepts an owned bundle when the owner carries no title tail (empty / the id / the r306 bare-id tail) and its lead holds no heading; the real "
           "owner stays, the heading goes FIRST in the lead, media between allowed, the walk resumed at the table. Probe OFF = disk 2555 / 2555; ON 13 pages / 5 modules "
           "(8 census pages + 5 index-only); scored 8 up / 0 down / 4 same, +18.9pp-sum; SCOPED regeneration of the 5 + the 12-module sample (4 batches rc 0; `scoped_ship.sh` "
           "PASS — 0 stale, containment 5 ⊆ 5, spot-check 12 / 12, every gate held-or-improved); skeleton 53.8088 → 53.8168 % (+0.0080pp; 8 movers all up, 0 outside the set), "
           "buckets 1408 / 236 / 20 EXACT, RAW 37.970 EXACT; compare_structure / body_compare / defect / every verifier EXACT; 16 selftests GREEN; feature index GREEN; "
           "ledger scoped #5 since the 19 Sept FULL (3 of headroom); miner 182 → 182; checksums engine 4 changed / gates 0. Not reached, recorded: AGH1004 lessons 1 / 5 "
           "(the `[Interactive: activity]` lookback lead spans a whole earlier section — the guard leaves it), COM1006 5.0 and XGF9003 1.2.")
lines[a:b] = ["## Session 29 — Round 4 (engine r413) — the OWNED half of the r412 class (the r407-recorded item completed) — SHIPPED; the PICK + what-shipped record is in LOOP_STATE_ARCHIVE.md 'Session 29 — Round 4 PICK (engine r413) + what shipped'; the one-line summary is the s29-r4 Round-log line below.", ""]
p = idx("- LAST SHIPPED: **r412**")
lines[p] = ("- LAST SHIPPED: **r413** (build 260619.84, 20 Sept ≈17:35, session 29 Round 4 — THE OWNED HALF OF THE r412 CLASS, the r407-recorded item completed: "
            "`heading_table_owner.owned_bundles`, env `HEADTABLEOWNED_OFF` (inside `HEADTABLE_OFF`); the gold's box 12 / 14 = 0.86; probe OFF = disk 2555 / 2555, ON 13 pages / 5 modules "
            "(8 up / 0 down); SCOPED regeneration of the 5 — scoped ship #5 since the 19 Sept FULL (3 of headroom); **skeleton 53.809 → 53.817 % (+0.0080pp), ≥50 1408 / ≥75 236 / ≥90 20 EXACT, "
            "RAW 37.970 % EXACT @ 2349 pairs**; every other gate EXACT; 16 selftests GREEN; the miner 182 → 182); before it **r412** (build 260619.83, 20 Sept ≈16:20, session 29 Round 3 — "
            "the heading-then-table shape after an empty typed-widget invocation takes the owner form, `HEADTABLE_OFF`: 14 up / 3 down, +0.0139pp, ≥50 +2, cs exact −1 = pool −1 named), "
            "**r411** (build 260619.82, the tile menu ROW+COL shell, `TILEMENUROW_OFF`, +0.0058pp) and **r410** (build 260619.81, the WJFUN tile-page dialect, `TILEPAGE_OFF`, "
            "skeleton 53.680 → 53.789 %, ≥50 +8). **Corpus = r413** (2555 pages / 494 dirs / 2349 pairs; `gate_baseline.json` at r413; `outputs/_s29_r413_sk_final.json` the skeleton state; "
            "ceiling 90.9 % → 53.817 = **59.2 % of achievable**).")
q = idx("- Plateau window (§4): **0 of 3**")
lines[q] = "- Plateau window (§4): **1 of 3** — r412 RESET it (+0.0139pp, ≥50 +2); r413 +0.0080pp with no other gate moved is the first. Read every delta on the post-intake 2,349-pair population (§1e)."
r = idx("- Standing facts: AppVersion 260619.83")
lines[r] = lines[r].replace("AppVersion 260619.83 (r412, session 29 Round 3, 20 Sept); before it 260619.82 (r411)", "AppVersion 260619.84 (r413, session 29 Round 4, 20 Sept); before it 260619.83 (r412) / 260619.82 (r411)")
assert "260619.84" in lines[r]
t = idx("- s29-r3 (engine r412")
lines.insert(t + 1, "- s29-r4 (engine r413, build 260619.84, 20 Sept ≈17:05 → 17:35) · THE OWNED HALF OF THE r412 CLASS — a writer-owned typed-widget box whose walk ended at the writer's `[H3]` takes the heading, prose (+ an `[image]`) and table too (`[Activity] **6A**` + `[multi-choice]` + `[H3]` + table → the gold's box 6A with the h3 and the built widget; the r407-recorded item completed; `heading_table_owner.owned_bundles`, env `HEADTABLEOWNED_OFF`; measured by the owned-mode census `_s29_r4_ownedwalk_T.tsv` + `_s29_r4_ownedcheck.out`: 15 bundles / 13 pages / 8 modules, gold box 12 / 14 = 0.86) · SHIPPED · probe OFF = disk 2555 / 2555, ON 13 pages / 5 modules (8 up / 0 down, +18.9) · SCOPED regen of the 5 (scoped #5 since the 19 Sept FULL; 0 stale; spot-check 12 / 12) · skeleton 53.809 → 53.817 (+0.0080pp), buckets EXACT; all else EXACT · miner 182 → 182 · plateau 1 of 3 · recorded: DIFF_QUEUE #36's three under-floor family dialects (ARFUN0 OFFSET, XGF9 COL6x2, EXPFUN0 PADLR — registry rows for a data round), the D10-3 widened-wrapper rider measured (no layout ≥ 0.21 — the r334 decline stands), AGH1004's lookback lead")
open(STATE, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
with open(ARCH, "a", encoding="utf-8") as f:
    f.write("\n## Session 29 — Round 4 PICK (engine r413) + what shipped — the OWNED half of the r412 class (20 Sept ≈17:05 → 17:35 NZST)\n\n" + "\n".join(pick).rstrip("\n") + "\n" + shipped + "\n")
print("LOOP_STATE.md", os.path.getsize(STATE), "bytes; archive", os.path.getsize(ARCH))
