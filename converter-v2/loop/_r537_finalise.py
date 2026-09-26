#!/usr/bin/env python3
"""ROUND 537 finalise (session 53 Round 3 — the accordion panel's bullets are a list). WSL. argv: MEAN RAW."""
import sys
import _s53_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-26 (round 537, build 260620.96) — THE ACCORDION PANEL'S BULLETS ARE A LIST: a built accordion's `•` lines ship as `<ul><li>` (glyph dropped) instead of `<p>• …</p>`; 43 modules / 57 pages, skeleton-blind by design (a widget's interior), RAW +0.043

### 1. WHAT CHANGED

**The class** (the s53-r2 writer-cue fate census's largest new row, `outputs/_s53_tagfate.py`): `black:bullet li@widget:accordion → p@widget:accordion` — **431 bullet lines on 49 pages / 36 modules** (BLL 173, ENO 46, WJFUN 43, XGF 40, HES 39). An accordion built by the strict text-only or image path (`InteractiveBuilder.#accordionTextOnly` / `#accordionWithImages`) rendered each panel body line as its own `<p>`, so the writer's bullets shipped with the glyph in a paragraph — BLL116 2.0: `<div class="accContent"><p>• Where do you think Sant and Nat are playing?</p><p>• What clues are there?</p></div>`, where the gold has `<div class="accContent"><ul><li>Where do you think Sant and Nat are playing?</li><li>What clues are there?</li></ul></div>`. The rich and panel-delimiter paths already listed them (through the page renderer). Authority: the writer's own bullets — the page renderer's `•` → `<li>` rule, applied everywhere else.

**The fix** (`InteractiveBuilder.#panelBodyHtml`, called by both strict paths; data `Emit_Templates.json accordion.panel_bullet_list`, env **`ACCBULLETLIST_OFF`**): a run of consecutive `•` lines renders as ONE `<ul>` of `<li>`s with the glyph dropped; every other line keeps its `<p>`; a panel with no bullet line is byte-identical.

### 2. PROOF

- In-memory probe over all 545 modules: `ACCBULLETLIST_OFF=1` → 6,432 / 6,432 pages identical; ON → **57 pages / 43 modules** (the BLL1xx / BLL2xx family, ENG1004, ENGC102, ENGI405, ENO2060, EXPFUN02, HES1007, HPFUN402, HPRE301, JPFUN01, PHE1003, PWY1002, SCCH301, SCPH301, five WJFUN, XGF9001 / 9002, XLP04, XMES202, XTAS101 / 103), every changed line an `accContent`'s bullet run; 0 ASSEMBLE ERROR. `scoped_ship.sh … --round 537 --commit` PASS: 0 stale, containment 43 ⊆ 43, the 12-module spot-check byte-identical.
- Skeleton-blind by design (the SCAFFOLD collapses a widget to one WIDGET line): the skeleton gate's own `match()` moves 0 pages; the RAW (widget-inclusive) mean rises **39.9782 → {RAW} %**.

### 3. PROTECTED GATES

Skeleton **{MEAN} % @ 2486 (held exactly)**, ≥50 1644, ≥75 305, ≥90 29; RAW 39.9782 → {RAW} %; compare_structure exact 17024 / EXTRA 198 / missing 661 held; body_compare ANY 233 held; leak 52 / 42 EXACT; tags 9557; every verifier ✓, every COUNT held (`_r537_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 537`; `--gate-baseline-check` PASS. Plateau: **neither** (skeleton-blind by design — LOOP §1g / §4).

**Ledger:** scoped #3 since the s52-r11 FULL · data `accordion.panel_bullet_list` · env `ACCBULLETLIST_OFF` · code `InteractiveBuilder.#panelBodyHtml` · session 53 Round 3.
"""
F.finalise(
    N=537, old_build="260620.95", new_build="260620.96", entry=entry,
    config_comment="THE ACCORDION PANEL'S BULLETS ARE A LIST (session 53 Round 3; <ul><li> in accContent instead of <p>• …</p>). Env ACCBULLETLIST_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 537 BASELINE (the accordion panel bullet list, `ACCBULLETLIST_OFF`; SCOPED, scoped #3 "
        f"since the s52-r11 FULL; skeleton-blind by design): SCAFFOLD mean {MEAN}% / >=50% 1644 / >=75% 305 / >=90% 29 / RAW {RAW}% @ 2486 pairs (held; RAW +0.043); cs exact 17024 / "
        f"EXTRA 198 / missing 661; body ANY 233.**",
    og11="| `ACCBULLETLIST_OFF` | 537 | **THE ACCORDION PANEL'S BULLETS ARE A LIST** (session 53 Round 3). Reverts `accordion.panel_bullet_list`: the strict "
         "text-only / image accordion paths render each `•` line as its own `<p>` again (the r536 output exactly). |",
    og14=f"- **Build:** `260620.96` (round 537 — **the accordion panel bullet list**; `ACCBULLETLIST_OFF`; scoped #3 since the s52-r11 FULL; 43 modules / 57 pages; "
         f"skeleton {MEAN} % (held — widget interior), RAW {RAW} % (+0.043)).",
    gb_note=f"Round 537 (session 53 Round 3, 2026-09-26) — THE ACCORDION PANEL BULLET LIST (ACCBULLETLIST_OFF): 43 modules / 57 pages; skeleton held at {MEAN} "
            f"(widget interior), RAW 39.9782 -> {RAW}; every other gate held; scoped #3 since the s52-r11 FULL.",
    no_round=f"- **No round in flight** (26 Sept 2026 {T}, session 53 Round 3 — r537 (the accordion panel bullet list) SHIPPED and committed; the in-flight marker "
             "is cleared). LAST SHIPPED **r537** (260620.96); **LAST FULL = r534 (the session-52 Round 11 backstop)**; ledger **scoped #3** (5 of headroom). "
             "Ride-along patches (LOOP §3 step 1 reads this list at every PICK): "
             "`outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, 10 pages / 9 modules — "
             "CEDK401, HIS1002, HPRE203, MXDI201, MXDI202 ×2, MXEX302, SSOG105, TWHA906, XGF9004) / `_r489_accbullet_declined.patch` (the accordion "
             "bulleted bold lead, 8 accordions / 4 modules — MXEX302, ENGS101, XGF9003, XLP05; its `bullet_bold_lead` data block is ALREADY in `Emit_Templates.json` "
             "(the r491 ride-along note) — verify and strike at the next accordion round) / `_r463_declined.patch` (the WJFUN tile's \"Year N\" "
             "lead, 1 page) / `_r512_declined.patch` (the `[Activity: Embedded] <widget>` bracket, 10 modules — rides only after the TRR table-dialect "
             "ownership fix) / `_r524_declined.patch` (the callout + heading co-tag, 17 modules — rides only once an alert's run gathers the list "
             "after its title). Checked at r537: none rides (r489 is the panel-DELIMITER class, not the panel body).",
    last_shipped=f"- LAST SHIPPED: **r537** (build 260620.96, 26 Sept {T}, session 53 Round 3 — THE ACCORDION PANEL'S BULLETS ARE A LIST, `ACCBULLETLIST_OFF`; "
                 "SCOPED, **scoped #3 since the s52-r11 FULL**; 43 modules / 57 pages; skeleton held at "
                 f"{MEAN} % (widget interior, by design), RAW {RAW} % (+0.043); every other gate held).",
    before_them_add="r535 the callout `close` closer",
    plateau="- Plateau window (§4): **0 of 3** — r537 skeleton-blind by design (neither); r536 +0.0261pp (a real gain: reset); ",
    standing="- Standing facts: AppVersion **260620.96** (r537 the accordion panel bullet list — session 53 Round 3, 26 Sept); before it 260620.95 (",
    roundlog=f"- s53-r3 (engine r537, build 260620.96, 26 Sept 23:38 → {T}) · THE ACCORDION PANEL'S BULLETS ARE A LIST (the fate census's largest new row: 431 "
             "`•` lines shipped as `<p>• …</p>` inside built accordions, 49 pages / 36 modules) · SHIPPED scoped #3 · 43 modules / 57 pages · skeleton held "
             "(widget interior, by design), RAW +0.043 · plateau: neither.",
    archive_extra="- **What shipped (r537, 260620.96):** `InteractiveBuilder.#panelBodyHtml` (called by #accordionTextOnly / #accordionWithImages); data "
                  "`accordion.panel_bullet_list`. Probe OFF 6,432 / 6,432 identical; ON 57 pages / 43 modules; skeleton 0 by design; RAW +0.043.",
)
