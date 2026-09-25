#!/usr/bin/env python3
"""ROUND 504 finalise (session 49 Round 4 — D15-17 CEDT301 single-file + the writer's black side-tab list, INQBLACKLIST_OFF). WSL.
argv[1] = the new skeleton mean (4 dp), argv[2] = RAW mean (3 dp) — read off _r504_gates.log."""
import sys
import _s49_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-25 (round 504, build 260620.67) — D15-17 CEDT301 IS ONE TABBED PAGE: the CEDT3 registry row goes single-file like every other CEDT module, and the writer's BLACK side-tab list (`Side Tabs:` + `Tab 1 – Introduction` … `Tab 9 – Digital Collage`) becomes the nine crumbs and panels instead of dead paragraphs (1 module, 7 pages → 1; a NAMED population change, 6 pairs → 1)

### 1. WHAT CHANGED

**The decision** (Chris, 25 Sept 2026, D15-17 — "17. CEDT301 one page or split: Option A (One tabbed page, like every other CEDT module) — as recommended"): CEDT301 has two human builds — one Inquiry page with seven tabs (`CEDT301 My place and me.html`) and a rougher split set. r440 (D13-6) built the other dual-build modules single-file but kept CEDT301 split because its caveat fired (single 45.0 % vs split 57.7 %). Chris chose the one page anyway and ACCEPTED the lower score as NAMED.

**Two changes.**
1. `data/Style_Anchor_Registry.json` CEDT3 level `page_model` multi-file → **single-file** (`_r504_note`; the row also governs CEDT302 / 303, which have no gold or build) — the r440 precedent: a registry value, the committed pre-round file (`outputs/_r504_pre/`) is its OFF state. The gates score CEDT301 against its single file (`compare_gold_pages.txt` `exclude` → `only`).
2. **The writer's black side-tab list** (`ContentConverter` — the r428 Inquiry-template fallback; data `inquiry_tabs.template_fallback.black_list`; env `INQBLACKLIST_OFF`). Built single-file with (1) alone, CEDT301 printed `Side Tabs:` and the nine `Tab N – …` lines as paragraphs in an extra "Introduction" panel (crumbs Introduction | Introduction | Mauri … Hikoi around town), because the r428 list capture reads only red `[Tab N] label` tags and CEDT301's writer typed the list in BLACK (WT l.61–79). Now a side-tabs instruction (a black `Side Tabs:` line or a red `[Side Tabs]` tag) followed by ≥ 3 black `Tab N – label` lines numbered 1, 2, 3 … is the writer's crumb list: its labels are the crumbs, the lines render nothing (the lines reach the converter joined into ONE black item, so the capture reads an item's lines and consumes only whole items); a heading of any level that repeats a listed label opens its panel (`any_heading_level` — the writer's `[H4] Digital collage`); and a listed heading that is the FIRST heading of a panel a `[page N]` boundary opened names that panel instead of opening another (`boundary_heading_names_panel` — `[page 6]` + a picture + `[H1] Hikoi around town`). Census (`_r504_blacklist_census.cjs`): only CEDT301 (black instruction), CEDT207 (red instruction — its list sits in the MENU partition, which this capture does not reach: recorded as a follow-up) and MXEX201 (Standard — outside the fallback's Inquiry scope) write the black form.

**The result:** CEDT301 is ONE page — crumbs **Introduction | Mauri | Mana | Wairua | Presentation | Hikoi around town | Investigate Site | Map it out | Digital Collage**, the writer's nine tabs, each panel opening at its own heading. The gold's seven tabs (Intro | Mauri | Mana | Wairua | Hikoi | Investigation | Collage) merge Map it out into Investigation and drop the Presentation page — the developer's edits (class C).

### 2. PROOF

- In-memory A/B over all 545 modules: ON **2 files / 1 module** (CEDT301's page + its interactives list); OFF (`INQBLACKLIST_OFF=1`) also only CEDT301 (the registry flip alone) — the black-list code is inert on every other module. CEDT207 / MXEX201 byte-identical under both.
- Regenerated: `01-Claude_Modules_/Inquiry/CEDT301/` 7 pages → **1** (= the probe's ON page byte-for-byte); `scoped_ship.sh`: 0 stale, containment 1 ⊆ 1, the 12-module spot-check byte-identical.
- `_r504_decompose.log`: before, 6 split pairs 34.8 / 58.2 / 64.0 / 64.3 / 67.2 / 80.8 (mean 61.5, five ≥50, one ≥75); after, **one pair, CEDT301_0_0 ↔ `CEDT301 My place and me.html` 45.2 %** (RAW 37.4; r440's single-file probe had 45.0).

### 3. PROTECTED GATES — a NAMED population change (D15-17)

- **Skeleton 55.5517 % @ 2491 → {MEAN} % @ 2486** (−0.02, the six split pairs → one page), **≥50 1604 → 1599 (−5)**, **≥75 277 → 276 (−1)** — all three NAMED: exactly CEDT301's five ≥50 / one ≥75 split pages leaving the population; 0 movers outside CEDT301; RAW {RAW} %. **cs exact 16746 → 16762 (+16)**, EXTRA 198 → 200 (+2, NAMED — the one page's own); missing 888; body ANY 232; clean 2585 / 2627 = 98.40 % (NAMED arithmetic: 6 clean split pages leave); leak 52 / 42; tags 9557 / 9557; every verifier ✓, every COUNT held (`_r504_gates.log`). `_fastloop_diff.py … --accept-named … --commit --round 504`; `--gate-baseline-check` PASS.
- Census: Claude pages **2,679 → 2,673**, skeleton pairs **2,491 → 2,486** (`verify_after_transfer.sh` expect updated, `.pre-r504.bak`; LOOP §0 table). Plateau: a population change — neither.

**Named overrides:** the lower CEDT301 score (Chris's D15-17 over D13-6's caveat); the writer's nine tabs over the gold's seven (the developer merged / dropped two).

**Ledger:** scoped #7 since the r498 FULL (the FULL backstop is due after #8) · data `Style_Anchor_Registry` CEDT3 `page_model`, `inquiry_tabs.template_fallback.black_list` · env `INQBLACKLIST_OFF` (the registry flip's OFF state = `outputs/_r504_pre/`) · code `ContentConverter` (the r428 fallback's list capture + listed-heading opener) · gate tooling `compare_gold_pages.txt` · tools `_r504_blacklist_census.cjs`, `_r504_decompose.py`, `_r504_finalise.py` · session 49 Round 4.
"""
F.finalise(
    N=504, old_build="260620.66", new_build="260620.67", entry=entry,
    config_comment="D15-17 CEDT301 IS ONE TABBED PAGE (session 49 Round 4) — the CEDT3 row single-file + the writer's black side-tab "
                   "list read as the crumb list. Env INQBLACKLIST_OFF (the registry flip's OFF = outputs/_r504_pre/).",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 504 BASELINE (D15-17 CEDT301 one tabbed page, "
        f"`INQBLACKLIST_OFF` + the CEDT3 registry row; SCOPED, scoped #7 since the r498 FULL; a NAMED population change): SCAFFOLD mean "
        f"{MEAN}% / >=50% 1599 / >=75% 276 / >=90% 26 / RAW {RAW}% @ 2486 pairs — 6 split pairs → 1 page (45.2 %); cs exact 16762 (+16).**",
    og11="| `INQBLACKLIST_OFF` | 504 | **THE WRITER'S BLACK SIDE-TAB LIST** (D15-17, session 49 Round 4). Reverts "
         "`inquiry_tabs.template_fallback.black_list`: a black `Side Tabs:` + `Tab N – label` list prints as paragraphs again and "
         "its labels open no panel. (The same round's CEDT3 `page_model` single-file flip has no env toggle — its OFF state is "
         "`outputs/_r504_pre/Style_Anchor_Registry.json`, the r440 precedent.) |",
    og14=f"- **Build:** `260620.67` (round 504 — **D15-17 CEDT301 one tabbed page**; `INQBLACKLIST_OFF`; scoped #7 since the r498 FULL; "
         f"1 module, 7 pages → 1; skeleton {MEAN} % @ 2486 — a NAMED population change).",
    gb_note=f"Round 504 (session 49 Round 4, 2026-09-25) — D15-17 CEDT301 ONE TABBED PAGE (INQBLACKLIST_OFF + the CEDT3 page_model): "
            f"7 pages -> 1, 6 split pairs -> 1 (45.2 %); SCAFFOLD 55.5517 @ 2491 -> {MEAN} @ 2486, >=50 -5 / >=75 -1 / EXTRA +2 / clean "
            f"-0.00 ACCEPTED AS NAMED (the population change Chris accepted); cs exact +16; scoped #7.",
    no_round=f"- **No round in flight** (25 Sept 2026 {T}, session 49 Round 4 — r504 (D15-17 CEDT301 one tabbed page) SHIPPED and "
             "committed; the in-flight marker is cleared). LAST SHIPPED **r504** (260620.67); **LAST FULL = r498**; ledger **scoped #7** "
             "(1 of headroom — the FULL backstop is due after scoped #8). Ride-along patches (LOOP §3 step 1 reads this list at every "
             "PICK): `outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` (buttons, 10 pages) / "
             "`_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages) / `_r489_accbullet_declined.patch` (the accordion bulleted "
             "bold lead, 8 accordions / 4 modules) / `_r463_declined.patch` (the WJFUN tile's \"Year N\" lead, 1 page).",
    last_shipped=f"- LAST SHIPPED: **r504** (build 260620.67, 25 Sept {T}, session 49 Round 4 — D15-17 CEDT301 ONE TABBED PAGE, the "
                 "CEDT3 registry row single-file + `INQBLACKLIST_OFF` (the writer's black `Side Tabs:` / `Tab N – label` list read as "
                 "the crumb list); SCOPED, **scoped #7 since the r498 FULL**; 7 pages → 1, the writer's nine tabs as crumbs + panels; a "
                 f"NAMED population change: **skeleton 55.5517 % @ 2491 → {MEAN} % @ 2486**, ≥50 1599 (−5), ≥75 276 (−1), EXTRA +2, "
                 "clean −0.00 — all CEDT301's; cs exact +16; census 2,679 → 2,673 pages).",
    before_them_add="the MX bare lesson menu",
    plateau="- Plateau window (§4): **0 of 3** — r504 a NAMED population change (neither); ",
    standing="- Standing facts: AppVersion **260620.67** (r504 D15-17 CEDT301 one tabbed page — session 49 Round 4, 25 Sept); before it "
             "260620.66 (",
    roundlog=f"- s49-r4 (engine r504, build 260620.67, 25 Sept 19:14 → {T}) · D15-17 CEDT301 ONE TABBED PAGE (the CEDT3 row single-file; "
             "the writer's black side-tab list → the nine crumbs / panels, `INQBLACKLIST_OFF`) · SHIPPED scoped #7, the movers NAMED "
             f"(6 pairs → 1: ≥50 −5, ≥75 −1) · skeleton {MEAN} % @ 2486, cs exact +16 · plateau 0 of 3 (neither).",
    archive_extra="- **What shipped (r504, 260620.67):** CEDT3 `page_model` single-file (`_r504_note`), `template_fallback.black_list` "
                  "(env `INQBLACKLIST_OFF`), `compare_gold_pages.txt` CEDT301 `only`. Probe ON / OFF each 1 module; scoped proof with "
                  "`--accept-named`; CEDT301 45.2 % as one page.",
)
