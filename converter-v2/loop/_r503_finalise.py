#!/usr/bin/env python3
"""ROUND 503 finalise (session 49 Round 3 — D15-22 the BLL2xx Knowledge / Practices tabs, BLLKPTABS_OFF). WSL."""
import _s49_fin as F
T = F.now()
entry = f"""## 2026-09-25 (round 503, build 260620.66) — D15-22 THE BLL2xx KNOWLEDGE / PRACTICES TABS: the tabbed BLL2xx overview menu gets its own Knowledge and Practices tabs in the KB c67 order, and the empty Information tab goes (18 pages / 18 modules; skeleton-blind by design — the menu-only compare +148.1pp-sum)

### 1. WHAT CHANGED

**The decision** (Chris, 25 Sept 2026, D15-22 — "22. BLL overview tabs: Option A (Their own tabs (the rulebook's set)) — as recommended"): r460 (KB c67 / CL-0040) made Knowledge / Practices their own nav tabs in every TABBED overview menu but left BLL on `exclude_subjects`, because CL-0040 had left the BLL263 D2 tab-split question open. Chris settled it for PageForge: in the tabbed BLL2xx overviews Knowledge and Practices are their own tabs (Overview → Knowledge → Practices → Information → Standards, 01B l.39) and the Information tab the promotions empty is removed (01B l.117). The 11 flat BLL2xx menus are untouched; BLL1xx was not asked and stays excluded.

**Triangulated** (BLL243): gold `BLL243-0.0.html` l.28–30 — Knowledge | Practices | Learning intentions tabs; PageForge `BLL243_0_0.html` l.23–50 — Overview (holding `Knowledge:` / `Practices:`) | an EMPTY Information tab (empty in all 19 — the D15 report's correction 7).

**The fix** (`MenuBuilder` — the r460 kpRe gate; data `menu.extra_tabs.curriculum_tabs.kb_canonical.readmit` {{ code_pattern `^BLL2\\d{{2}}$` }}; env `BLLKPTABS_OFF`): a module whose code matches the readmit pattern is taken off `exclude_subjects`, so r460's canonical promotion + `drop_empty_tab2` apply to it.

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 0 pages changed**; ON **18 overview pages / 18 modules** (BLL243 247 250 251 253 255 257 261 262 263 264 266 271–276) — every one now Overview | Knowledge | Practices with the empty Information tab gone; `_r503_check.cjs`: every change is inside `#module-menu-content`, the body byte-identical. **BLL265 does not change** — its Knowledge / Practices land in the page BODY, not the menu (Follow-up (b), a separate fault).
- Regenerated = the probe's ON pages byte-for-byte; `scoped_ship.sh` PASS (0 stale, containment 18 ⊆ 18, the 12-module spot-check byte-identical).
- **The region's own compare** (`_r503_rawmenu.py`, the r460 menu-only skeleton, OFF saved under `BLLKPTABS_OFF=1` vs ON): **menu-only +148.1pp-sum, RAW +59.4pp-sum**; **6 up** — BLL253 52.6 → 93.7, BLL247 36.1 → 79.1, BLL261 51.2 → 85.4, BLL273 46.8 → 74.2, BLL262 61.7 → 71.4, BLL243 39.0 → 42.4 (the own-tab golds); **12 down, NAMED**: the Information / combined-tab golds Chris ruled on — BLL251 7.7 → 2.4, BLL263 63.3 → 61.0, BLL250 33.3 → 32.0 (combined tab), BLL255 / 257 / 264 / 266 / 275 −0.1 to −0.2 — and BLL271 / 272 / 274 / 276 −0.1 to −0.2 (menus ≈ 6 % alike either way: the gold overview menu differs elsewhere).

### 3. PROTECTED GATES

- **Skeleton-blind by design** (§1g: the menu's `div.tabs` collapses to one WIDGET line): skeleton 55.5517 % @ 2491 EXACT (0 movers), ≥50 1604, ≥75 277, ≥90 26; RAW 39.477 → 39.50 %; cs / body / clean / leak EXACT; tags 9557 / 9557; every verifier ✓, every COUNT held (`_r503_gates.log`); `gate_baseline.json` aggregates written by `scoped_ship.sh … --commit --round 503`; `--gate-baseline-check` PASS. Plateau: neither (skeleton-blind by design).

**Named overrides (§1b):** KB c67 / 01B over the BLL2xx golds that keep Knowledge / Practices in an Information tab (BLL251 / 255 / 257 / 263 / 264 / 266 / 275), BLL250's combined tab and BLL265's hybrid — by Chris's D15-22.

**Ledger:** scoped #6 since the r498 FULL · data `kb_canonical.readmit` · env `BLLKPTABS_OFF` · code `MenuBuilder` (the r460 kpRe gate) · tools `_r503_check.cjs`, `_r503_rawmenu.py`, `_r503_finalise.py` · session 49 Round 3.
"""
F.finalise(
    N=503, old_build="260620.65", new_build="260620.66", entry=entry,
    config_comment="D15-22 THE BLL2xx KNOWLEDGE / PRACTICES TABS (session 49 Round 3) — the tabbed BLL2xx overview gets the KB c67 "
                   "Knowledge / Practices tabs, the empty Information tab dropped. Env BLLKPTABS_OFF.",
    og9="| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 503 BASELINE (D15-22 the BLL2xx Knowledge / Practices tabs, "
        "`BLLKPTABS_OFF`; SCOPED, scoped #6 since the r498 FULL; skeleton-blind by design): SCAFFOLD mean 55.5517% / >=50% 1604 / >=75% 277 / "
        ">=90% 26 / RAW 39.50% @ 2491 pairs — EXACT; the menu-only compare +148.1pp-sum (6 up / 12 down NAMED).**",
    og11="| `BLLKPTABS_OFF` | 503 | **D15-22 THE BLL2xx KNOWLEDGE / PRACTICES TABS** (session 49 Round 3). Reverts "
         "`kb_canonical.readmit`: BLL2xx goes back on r460's `exclude_subjects` — its Knowledge / Practices sections stay in the Overview "
         "pane beside an empty Information tab; byte-identical to r502. |",
    og14="- **Build:** `260620.66` (round 503 — **D15-22 the BLL2xx Knowledge / Practices tabs**; `BLLKPTABS_OFF`; scoped #6 since the "
         "r498 FULL; 18 overview pages; skeleton EXACT (blind by design), menu-only +148.1pp-sum).",
    gb_note="Round 503 (session 49 Round 3, 2026-09-25) — D15-22 THE BLL2xx KNOWLEDGE / PRACTICES TABS (BLLKPTABS_OFF): 18 tabbed BLL2xx "
            "overviews get Knowledge / Practices tabs, the empty Information tab dropped; skeleton-blind by design (EXACT), RAW 39.48 -> "
            "39.50; menu-only +148.1pp-sum (6 up / 12 down NAMED); scoped #6.",
    no_round=f"- **No round in flight** (25 Sept 2026 {T}, session 49 Round 3 — r503 (D15-22 the BLL2xx Knowledge / Practices tabs) SHIPPED "
             "and committed; the in-flight marker is cleared). LAST SHIPPED **r503** (260620.66); **LAST FULL = r498**; ledger **scoped #6** "
             "(2 of headroom — the FULL backstop is due after scoped #8). Ride-along patches (LOOP §3 step 1 reads this list at every PICK): "
             "`outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` (buttons, 10 pages) / `_r468_declined.patch` (the "
             "lesson menu's `[H2]` lead, 3 pages) / `_r489_accbullet_declined.patch` (the accordion bulleted bold lead, 8 accordions / 4 "
             "modules) / `_r463_declined.patch` (the WJFUN tile's \"Year N\" lead, 1 page).",
    last_shipped=f"- LAST SHIPPED: **r503** (build 260620.66, 25 Sept {T}, session 49 Round 3 — D15-22 THE BLL2xx KNOWLEDGE / PRACTICES "
                 "TABS, `BLLKPTABS_OFF`; SCOPED, **scoped #6 since the r498 FULL**, scoped_ship PASS; 18 tabbed BLL2xx overviews → Overview | "
                 "Knowledge | Practices, the empty Information tab dropped (BLL265 unchanged — Follow-up (b)); skeleton-blind by design: "
                 "SCAFFOLD 55.5517 % EXACT, RAW 39.477 → 39.50 %; the menu-only compare +148.1pp-sum, 6 up / 12 down NAMED; cs / body / "
                 "clean / leak EXACT).",
    before_them_add="the gate-tool round (no engine change)",
    plateau="- Plateau window (§4): **0 of 3** — r503 skeleton-blind by design (neither); ",
    standing="- Standing facts: AppVersion **260620.66** (r503 D15-22 the BLL2xx Knowledge / Practices tabs — session 49 Round 3, 25 Sept); "
             "before it 260620.65 (",
    roundlog=f"- s49-r3 (engine r503, build 260620.66, 25 Sept 18:38 → {T}; ≈30 min lost to a hung grep) · D15-22 THE BLL2xx KNOWLEDGE / "
             "PRACTICES TABS (r460's KB c67 promotion readmitted for BLL2xx; the empty Information tab dropped) · SHIPPED scoped #6 · 18 "
             "overview pages · skeleton EXACT (blind by design), menu-only +148.1pp-sum (6 up / 12 down NAMED) · plateau 0 of 3 (neither).",
    archive_extra="- **What shipped (r503, 260620.66):** `kb_canonical.readmit` (env `BLLKPTABS_OFF`), `MenuBuilder` kpRe gate. Probe OFF "
                  "0; ON 18 pages / 18 modules, menu-only (`_r503_check.cjs`); scoped_ship PASS; `_r503_rawmenu.py` menu-only +148.1pp-sum.",
)
