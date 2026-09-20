#!/usr/bin/env python3
"""r411 finalise — LOOP_STATE.md: the Round 2 PICK section moves to the archive (+ the what-shipped record), the Position updates,
the Round-log line is appended."""
import os
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
STATE, ARCH = R + "LOOP_STATE.md", R + "LOOP_STATE_ARCHIVE.md"
lines = rd = open(STATE, encoding="utf-8").read().split("\n")
def idx(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix): return i
    raise SystemExit("not found: " + prefix)

# the PICK section: from its heading to the '## Round log' heading
a = idx("## Session 29 — Round 2 PICK (engine r411)"); b = idx("## Round log")
pick = lines[a:b]
shipped = ("- **What shipped (r411, build 260619.82, 20 Sept ≈15:35):** `menu.shells.writer_tabs_row` + `tile_pages.menu.shell_row {enabled, env TILEMENUROW_OFF, shell}`; "
           "`MenuBuilder.#levelTabs` returns the shell key when its cfg carries the block (the level-pages cfg does not — CHFUN stays bare), both call sites pass `wtShell`, "
           "`SkeletonBuilder` selects it when the name exists in `menu.shells`. Probe OFF = disk 2555 / 2555; ON exactly the 21 WJFUN overviews (CHFUN / ENGS404 untouched); "
           "scored on the ON pages 21 / 21 up, +13.6pp-sum scaffold / +87.3 RAW; SCOPED regeneration of the 21 (2 batches rc 0; `scoped_ship.sh` PASS — 0 stale, containment 21 ⊆ 21, "
           "spot-check 12 / 12 incl. ENGJ403, decomposition exact); skeleton 53.7891 → 53.7949 % (+0.0058pp; 21 movers all up, 0 outside the set), buckets 1406 / 236 / 20 EXACT, "
           "RAW 37.925 → 37.963 %; compare_structure / body_compare / defect / every verifier EXACT; 16 selftests GREEN; feature index GREEN; ledger scoped #3 since the 19 Sept FULL; "
           "miner 184 → 182 (#47 / #48 gone, nothing new); checksums engine 4 changed / gates 0.")
lines[a:b] = ["## Session 29 — Round 2 (engine r411) — the tile dialect's menu takes the gold's ROW+COL tabs shell — SHIPPED; the PICK + what-shipped record is in LOOP_STATE_ARCHIVE.md 'Session 29 — Round 2 PICK (engine r411) + what shipped'; the one-line summary is the s29-r2 Round-log line below.", ""]

# Position
p = idx("- LAST SHIPPED: **r410**")
lines[p] = ("- LAST SHIPPED: **r411** (build 260619.82, 20 Sept ≈15:35, session 29 Round 2 — THE TILE DIALECT'S MENU TAKES THE GOLD'S ROW+COL TABS SHELL, DIFF MINER rows #47 / #48: "
            "`menu.shells.writer_tabs_row` + `tile_pages.menu.shell_row`, env `TILEMENUROW_OFF`; the gold's tabs menu is ROW+COL 279 / 293 = 0.95, WJFUN 21 / 21; probe OFF = disk 2555 / 2555, "
            "ON exactly the 21 WJFUN overviews (21 up / 0 down); SCOPED regeneration of the 21 — scoped ship #3 since the 19 Sept FULL (5 of headroom); **skeleton 53.789 → 53.795 % (+0.0058pp), "
            "≥50 1406 / ≥75 236 / ≥90 20 EXACT, RAW 37.925 → 37.963 % @ 2349 pairs**; every other gate EXACT; 16 selftests GREEN; the miner 184 → 182); before it **r410** (build 260619.81, 20 Sept ≈15:05, "
            "session 29 Round 1 — the WJFUN tile-page dialect, `tile_pages` / `TILEPAGE_OFF`: 21 up / 0 down, +257.1pp-sum, skeleton 53.680 → 53.789 %, ≥50 1398 → 1406, cs exact 14091 → 14175, "
            "WJFUN 37.6 → 49.9 %, scoped ship #2) and **r408** (20 Sept ≈11:30, session 28 pre-loop Task 1 — the registries rebuilt over 552; `Subject_Prefix_Map.json` PROPOSED). "
            "**Corpus = r411** (2555 pages / 494 dirs / 2349 pairs; `gate_baseline.json` at r411; `outputs/_s29_r411_sk_final.json` the skeleton state; ceiling 90.9 % → 53.795 = **59.2 % of achievable**).")
q = idx("- Plateau window (§4): **0 of 3** — RESET by r410")
lines[q] = "- Plateau window (§4): **1 of 3** — r410 RESET it (+0.1095pp, ≥50 +8); r411 +0.0058pp with no bucket moved counts as the first. Read every delta on the post-intake 2,349-pair population (§1e)."
r = idx("- Standing facts: AppVersion 260619.81")
lines[r] = lines[r].replace("AppVersion 260619.81 (r410, session 29 Round 1, 20 Sept); before it 260619.80 (r409)", "AppVersion 260619.82 (r411, session 29 Round 2, 20 Sept); before it 260619.81 (r410) / 260619.80 (r409)")
assert "260619.82" in lines[r]

# Round-log line after the s29-r1 line
t = idx("- s29-r1 (engine r410")
lines.insert(t + 1, "- s29-r2 (engine r411, build 260619.82, 20 Sept ≈15:15 → 15:35) · THE TILE DIALECT'S MENU TAKES THE GOLD'S ROW+COL TABS SHELL (`moduleMenu › div.row › div.tabs.col-12` — the gold's tabs menus 0.95, WJFUN 21 / 21; the r410 branch had inherited the bare r221 writer_tabs shell; `menu.shells.writer_tabs_row` + `tile_pages.menu.shell_row`, `#levelTabs` → `wtShell` → SkeletonBuilder, env `TILEMENUROW_OFF`; found by the DIFF MINER rows #47 / #48 + the tabs-shell census `_s29_r2_menutabs.py`) · SHIPPED · probe OFF = disk 2555 / 2555, ON exactly the 21 WJFUN overviews (21 up / 0 down, +13.6) · SCOPED regen of the 21 (scoped #3 since the 19 Sept FULL; 0 stale; spot-check 12 / 12) · skeleton 53.789 → 53.795 (+0.0058pp), buckets EXACT; all else EXACT · miner 184 → 182 (#47 / #48 gone) · plateau 1 of 3 · recorded: ENGS404 (tie at n = 2), the 9 `row › col-md-8` pages, the 6 bare-gold pages")

open(STATE, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
with open(ARCH, "a", encoding="utf-8") as f:
    f.write("\n## Session 29 — Round 2 PICK (engine r411) + what shipped — the tile dialect's menu takes the gold's ROW+COL tabs shell (20 Sept ≈15:15 → 15:35 NZST)\n\n" + "\n".join(pick).rstrip("\n") + "\n" + shipped + "\n")
print("LOOP_STATE.md", os.path.getsize(STATE), "bytes; archive", os.path.getsize(ARCH))
