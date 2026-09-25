#!/usr/bin/env python3
"""ROUND 502 finalise (session 49 Round 2 — D15-23 the MX bare lesson menu, MXBAREMENU_OFF). WSL."""
import _s49_fin as F
T = F.now()
entry = f"""## 2026-09-25 (round 502, build 260620.65) — D15-23 THE MX BARE LESSON MENU: on the lesson pages of the MXFU / MXEX / MXDB3 / MXDI3 series the menu is the bare `#module-menu-content > h5 + ul` — Chris's named series convention (94 pages / 11 modules; +0.0929pp, ≥50 +12, 88 up / 0 down)

### 1. WHAT CHANGED

**The decision** (Chris, 25 Sept 2026, D15-23 — "23. Maths lesson menus: Option B (A named Maths-series house style) — as recommended"): KB 01B l.296–301 puts the lesson-menu content inside `<div class="row"><div class="col-md-8 col-12">`, but in four Maths series the human leaves it out on every paired lesson page — **91 / 91** (`outputs/_s45_r4_menuwrap.log`: MXDB3 14, MXDI3 7, MXEX 26 + 1 mis-pair, MXFU 44). Chris named the bare form a SERIES CONVENTION (a series-scoped override of 01B, the D14-20 precedent for KB 07D); the matching KB 10 §3 "series conventions — preserve" sub-table joins his rulebook session (Needs Chris #1).

**Triangulated** (the D15 report): MXFU301 lesson 1 — WT `[Lesson Overview]` / `We are learning:` / bullets (parsed l.90–104) → gold `MXFU301_1.0.html` l.22–34 `#module-menu-content > h5 + ul + h5 + ul` → PageForge `MXFU301_1_0.html` l.19–35 the same inside `row > col-md-8 col-12`; MXDB302 lesson 1 the same; MXEX302 lesson 1 an EMPTY shell (no WT `[Lesson Overview]` — not this round's job).

**The fix** (`SkeletonBuilder.#buildHeader` shell choice; data `menu.simplified_bare_series` + `menu.shells.simplified_bare`; env `MXBAREMENU_OFF`): a page whose menu resolves to the `simplified` shell renders `simplified_bare` instead when it is a LESSON page and its module code matches one of the data's series patterns (`^MXFU[2-4]\\d{{2}}$` — not MXFUN — `^MXEX\\d{{3}}$`, `^MXDB3\\d{{2}}$`, `^MXDI3\\d{{2}}$`). Overviews, every other shell and every other module are untouched.

### 2. PROOF

- In-memory A/B over all 545 modules (`_s42_probe_run.sh r502`): **OFF 0 pages changed**; ON **94 pages / 11 modules** (MXDB301 MXDB302 MXDI301 MXEX101 MXEX301 MXEX302 MXFU201 MXFU202 MXFU301 MXFU302 MXFU402) — exactly the modules whose lesson pages carry a menu (MXFU401 / MXEX401 / MXEX201 / MXEX202 build one on the overview only). `_r502_check.cjs`: **all 94 differ ONLY by the removed wrapper** (the rest of the page byte-identical, the menu's lines identical once the wrapper is taken away); 47 of them are the empty MX menus, which stay empty (Follow-up (c)).
- Regenerated (4 parallel batches, 32 s) = the probe's ON pages byte-for-byte (105 / 105); `_content_manifest.py fresh`: 0 stale, the 532 untouched modules byte-identical; `scoped_ship.sh` PASS (containment, the 12-module spot-check).

### 3. PROTECTED GATES

- Skeleton **55.4588 % → 55.5517 % @ 2491 (+0.0929pp)**, RAW 39.425 → 39.477 %; **≥50 1592 → 1604 (+12)**; ≥75 277; ≥90 26; **88 movers, all up** (pp-sum +231.4), 0 outside the affected set: MXFU301_4_0 **43.5 → 56.7**, MXFU402_7_0 +12.6, MXFU302_3_0 +9.6, MXFU301_11_0 +9.2, MXDB302_3_0 **46.4 → 53.7** … (the twelve ≥50 crossings in `_r502_skdelta.log`). cs / body / clean / leak EXACT; tags 9557 / 9557; every verifier RESULT ✓ with its COUNT line held (`_r502_gates.log`). `gate_baseline.json` aggregates written by `_fastloop_diff.py --commit --round 502` (mean 55.55, median 56.7, ≥50 1604, RAW 39.48); `--gate-baseline-check` PASS.
- The miner re-run: CANDIDATE 195 → 194, diff lines 274,873 → 274,340.
- Plateau (§4): +0.0929pp — a real gain: reset, **0 of 3**. **60.6 % of achievable** (ceiling 91.7 %).

**Named override (§1b):** KB 01B l.296–301's row > col-md-8 lesson-menu wrapper, on the MXFU2xx–4xx / MXEX / MXDB3 / MXDI3 lesson pages only — by Chris's D15-23.

**Ledger:** scoped #5 since the r498 FULL (recorded by `scoped_ship.sh`'s proof run; the baseline committed by `_fastloop_diff.py … --commit --round 502`) · data `menu.simplified_bare_series` / `menu.shells.simplified_bare` · env `MXBAREMENU_OFF` · code `SkeletonBuilder.#buildHeader` · tools `_r502_check.cjs`, `_r502_movers.py`, `_s49_fin.py`, `_r502_finalise.py` · session 49 Round 2.
"""
F.finalise(
    N=502, old_build="260620.64", new_build="260620.65", entry=entry,
    config_comment="D15-23 THE MX BARE LESSON MENU (session 49 Round 2) — the MXFU / MXEX / MXDB3 / MXDI3 lesson menu without the "
                   "row > col-md-8 wrapper. Env MXBAREMENU_OFF.",
    og9="| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 502 BASELINE (D15-23 the MX bare lesson menu, `MXBAREMENU_OFF`; "
        "SCOPED, scoped #5 since the r498 FULL; scoped_ship PASS): SCAFFOLD mean 55.5517% / >=50% 1604 / >=75% 277 / >=90% 26 / RAW 39.477% @ "
        "2491 pairs — +0.0929pp (88 movers, all up), >=50 +12; cs / body / clean / leak EXACT.**",
    og11="| `MXBAREMENU_OFF` | 502 | **D15-23 THE MX BARE LESSON MENU** (session 49 Round 2). Reverts `menu.simplified_bare_series`: the "
         "MXFU2xx–4xx / MXEX / MXDB3 / MXDI3 lesson menu is wrapped in `row > col-md-8 col-12` again (the `simplified` shell); "
         "byte-identical to r501. |",
    og14="- **Build:** `260620.65` (round 502 — **D15-23 the MX bare lesson menu**; `MXBAREMENU_OFF`; scoped #5 since the r498 FULL; 94 "
         "pages / 11 modules; skeleton 55.5517 % @ 2491, +0.0929pp, ≥50 +12).",
    gb_note="Round 502 (session 49 Round 2, 2026-09-25) — D15-23 THE MX BARE LESSON MENU (MXBAREMENU_OFF): 94 lesson pages / 11 modules "
            "lose the row > col-md-8 menu wrapper (a named series convention); SCAFFOLD 55.4588 -> 55.5517 @ 2491 (+0.0929pp), 88 movers all "
            "up; >=50 1592 -> 1604; everything else EXACT; aggregates written by _fastloop_diff.py --commit --round 502; scoped #5.",
    no_round=f"- **No round in flight** (25 Sept 2026 {T}, session 49 Round 2 — r502 (D15-23 the MX bare lesson menu) SHIPPED and committed; the "
             "in-flight marker is cleared). LAST SHIPPED **r502** (260620.65); **LAST FULL = r498**; ledger **scoped #5** (3 of headroom). "
             "Ride-along patches (LOOP §3 step 1 reads this list at every PICK): `outputs/_r469_declined.patch` (alerts, 7 pages) / "
             "`_r469b_declined.patch` (buttons, 10 pages) / `_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages) / "
             "`_r489_accbullet_declined.patch` (the accordion bulleted bold lead, 8 accordions / 4 modules) / `_r463_declined.patch` (the "
             "WJFUN tile's \"Year N\" lead, 1 page).",
    last_shipped=f"- LAST SHIPPED: **r502** (build 260620.65, 25 Sept {T}, session 49 Round 2 — D15-23 THE MX BARE LESSON MENU, "
                 "`MXBAREMENU_OFF`; SCOPED, **scoped #5 since the r498 FULL**, scoped_ship PASS; 94 lesson pages / 11 modules (MXFU201 / 202 / "
                 "301 / 302 / 402, MXEX101 / 301 / 302, MXDB301 / 302, MXDI301) lose the row > col-md-8 wrapper; **skeleton 55.4588 → 55.5517 % "
                 "@ 2491 (+0.0929pp)**, 88 up / 0 down, **≥50 1604 (+12)**, ≥75 277, ≥90 26, RAW 39.477 %; cs / body / clean / leak EXACT; "
                 "the miner 194 CANDIDATE).",
    before_them_add="the back-to-back split trigger",
    plateau="- Plateau window (§4): **0 of 3** — r502 +0.0929pp (a real gain: reset); ",
    standing="- Standing facts: AppVersion **260620.65** (r502 D15-23 the MX bare lesson menu — session 49 Round 2, 25 Sept); before it "
             "260620.64 (",
    roundlog=f"- s49-r2 (engine r502, build 260620.65, 25 Sept 18:17 → {T}) · D15-23 THE MX BARE LESSON MENU (Chris's named series "
             "convention: MXFU / MXEX / MXDB3 / MXDI3 lesson menus without the row > col-md-8 wrapper) · SHIPPED scoped #5, scoped_ship PASS · "
             "94 pages / 11 modules, all wrapper-only · skeleton **+0.0929pp**, 88 up / 0 down, ≥50 +12 · plateau reset (0 of 3).",
    archive_extra="- **What shipped (r502, 260620.65):** `menu.simplified_bare_series` + `menu.shells.simplified_bare` (env `MXBAREMENU_OFF`), "
                  "`SkeletonBuilder.#buildHeader`. Probe OFF 0; ON 94 pages / 11 modules, all wrapper-only (`_r502_check.cjs`); scoped_ship "
                  "PASS; +0.0929pp, 88 up / 0 down, ≥50 +12.",
)
