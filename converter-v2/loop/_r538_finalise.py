#!/usr/bin/env python3
"""ROUND 538 finalise (session 53 Round 4 — the family heading digit pin, the rest of its passing groups). WSL. argv: MEAN RAW."""
import sys
import _s53_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-27 (round 538, build 260620.97) — THE FAMILY KEEPS THE WRITER'S HEADING DIGIT, THE REST OF THE PASSING GROUPS: COM / GEO `[H2]` → h2, TWHK / TWHR / EXPFUN / CEDK `[H3]` → h3, CEDO `[H4]` → h4, OSOH `[H5]` → h5 (r536's rule, a second row block); 20 modules / 39 pages, skeleton +0.0100pp, ≥50 +1

### 1. WHAT CHANGED

**The class** (session 53 Round 4's PICK pass: the coverage dashboard refreshed — the no-builder radioQuiz lane is 3 answer-marked True/False tables of 19, D13-4 forbids the rest; the fate census extended with a CHROME section and a FAMILY-DIALECT detector — its BLL modal / click-drop rows are the gold's clickDrop substitution for the writer's `[Modal]` (Claude builds the TKmodals: A1) and its BLL menu `[H2]` rows the KB canonical labels (D10-9) — then the rest of r536's per-family table, `outputs/_s53_r2_hlevel.py`): the gold keeps the writer's heading digit at ≥ 0.60 while Claude shifts it in **COM `[H2]` 0.61** (33 items / 14 pages), **GEO `[H2]` 0.78** (9 / 6), **TWHK `[H3]` 1.00** (20 / 4), **TWHR `[H3]` 0.96** (23 / 2), **EXPFUN `[H3]` 0.67** (12 / 2), **CEDK `[H3]` 0.71** (21 / 7), **CEDO `[H4]` 0.90** (10 / 3), **OSOH `[H5]` 0.83** (12 / 6). Probed per family on the gate's own `match()` and DROPPED as net-negative: OSAI `[H5]` (0.75, −2.5), MXDB `[H5]` (0.78, −0.7), TRR `[H3]` (0.62, −0.7), TWHA `[H3]` / `[H4]` (0.77 / 1.00, −0.2). Authority §1b-3/4; LOOP §1d exception 2 (a per-group rule, the groups summed).

**The fix** (`ContentConverter` heading emitter, path (c) now reads every `keep_writer_digit.digits_by_prefix_families*` block, each on its own env — r536's block byte-identical; data `digits_by_prefix_families_2` {{"2": [COM, GEO], "3": [TWHK, TWHR, EXPFUN, CEDK], "4": [CEDO], "5": [OSOH]}}, env **`HKEEPFAM2_OFF`**).

### 2. PROOF

- In-memory probe over all 545 modules: `HKEEPFAM2_OFF=1` → 6,432 / 6,432 pages identical; ON → **39 pages / 20 modules**; 0 ASSEMBLE ERROR. `scoped_ship.sh … --round 538 --commit` PASS: 0 stale, containment 20 ⊆ 20, the 12-module spot-check byte-identical.
- The skeleton gate's own `match()`: **+0.0100pp, 18 up / 8 down** (TWHK +13.2, OSOH +4.8, CEDK +3.6, COM +2.6 — COM1005 +12.8, EXPFUN +0.4, GEO +0.2). The dips, NAMED: COM1006 2_0 / 4_0 / 5_0 (−1.7 / −3.5 / −3.5) and COM1002_3_0 (−1.5) — those golds follow the shift (position-free 29 → 28, 45 → 44, 32 → 30, 46 → 45: the family's outliers); COM1005_5_0 −2.5 (position-free 54 → 54) and COM1005_7_0 −2.2 (position-free 28 → 30 RISES — alignment); GEO1005_3_0 −0.7 (75 → 74) and GEO1005_5_0 −1.0 (48 → 49 RISES — alignment).

### 3. PROTECTED GATES

Skeleton **56.3661 → {MEAN} % @ 2486 (+0.0100pp)**, ≥50 1644 → 1645, ≥75 305, ≥90 29; RAW 40.0211 → {RAW} %; compare_structure exact 17024 / EXTRA 198 / missing 661 held; body_compare ANY 233 held; leak 52 / 42 EXACT; tags 9557; every verifier ✓, every COUNT held (`_r538_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 538`; `--gate-baseline-check` PASS. Plateau: **1 of 3** (+0.0100pp).

**Ledger:** scoped #4 since the s52-r11 FULL · data `keep_writer_digit.digits_by_prefix_families_2` · env `HKEEPFAM2_OFF` · code `ContentConverter` heading emitter path (c) · session 53 Round 4.
"""
F.finalise(
    N=538, old_build="260620.96", new_build="260620.97", entry=entry,
    config_comment="THE FAMILY HEADING DIGIT PIN, THE REST OF THE PASSING GROUPS (session 53 Round 4; COM / GEO [H2], TWHK / TWHR / EXPFUN / CEDK [H3], CEDO [H4], OSOH [H5]). Env HKEEPFAM2_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 538 BASELINE (the family heading digit pin, block 2, `HKEEPFAM2_OFF`; SCOPED, scoped #4 "
        f"since the s52-r11 FULL): SCAFFOLD mean {MEAN}% / >=50% 1645 / >=75% 305 / >=90% 29 / RAW {RAW}% @ 2486 pairs (+0.0100pp); cs exact 17024 / "
        f"EXTRA 198 / missing 661; body ANY 233.**",
    og11="| `HKEEPFAM2_OFF` | 538 | **THE FAMILY HEADING DIGIT PIN, THE REST OF THE PASSING GROUPS** (session 53 Round 4). Reverts `keep_writer_digit.digits_by_prefix_families_2`: "
         "COM / GEO [H2], TWHK / TWHR / EXPFUN / CEDK [H3], CEDO [H4] and OSOH [H5] take the r45 shift + rank again (the r537 output exactly). |",
    og14=f"- **Build:** `260620.97` (round 538 — **the family heading digit pin, block 2**; `HKEEPFAM2_OFF`; scoped #4 since the s52-r11 FULL; 20 modules / 39 pages; "
         f"skeleton {MEAN} % (+0.0100pp), RAW {RAW} %, ≥50 +1).",
    gb_note=f"Round 538 (session 53 Round 4, 2026-09-27) — THE FAMILY HEADING DIGIT PIN, BLOCK 2 (HKEEPFAM2_OFF): 20 modules / 39 pages; skeleton 56.3661 -> {MEAN} "
            f"(+0.0100pp), >=50 1645; every other gate held; scoped #4 since the s52-r11 FULL.",
    no_round=f"- **No round in flight** (27 Sept 2026 {T}, session 53 Round 4 — r538 (the family heading digit pin, block 2) SHIPPED and committed; the in-flight marker "
             "is cleared). LAST SHIPPED **r538** (260620.97); **LAST FULL = r534 (the session-52 Round 11 backstop)**; ledger **scoped #4** (4 of headroom). "
             "Ride-along patches (LOOP §3 step 1 reads this list at every PICK): "
             "`outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, 10 pages / 9 modules — "
             "CEDK401, HIS1002, HPRE203, MXDI201, MXDI202 ×2, MXEX302, SSOG105, TWHA906, XGF9004) / `_r489_accbullet_declined.patch` (the accordion "
             "bulleted bold lead, 8 accordions / 4 modules — MXEX302, ENGS101, XGF9003, XLP05; its `bullet_bold_lead` data block is ALREADY in `Emit_Templates.json` "
             "(the r491 ride-along note) — verify and strike at the next accordion round) / `_r463_declined.patch` (the WJFUN tile's \"Year N\" "
             "lead, 1 page) / `_r512_declined.patch` (the `[Activity: Embedded] <widget>` bracket, 10 modules — rides only after the TRR table-dialect "
             "ownership fix) / `_r524_declined.patch` (the callout + heading co-tag, 17 modules — rides only once an alert's run gathers the list "
             "after its title). Checked at r538: none rides (CEDK401 is in r538's set; r469b's class — the button — is not r538's).",
    last_shipped=f"- LAST SHIPPED: **r538** (build 260620.97, 27 Sept {T}, session 53 Round 4 — THE FAMILY HEADING DIGIT PIN, BLOCK 2, `HKEEPFAM2_OFF`; "
                 "SCOPED, **scoped #4 since the s52-r11 FULL**; 20 modules / 39 pages; skeleton 56.3661 → "
                 f"{MEAN} % (+0.0100pp), ≥50 1645, ≥75 305, RAW {RAW} %; every other gate held).",
    before_them_add="r536 the family heading digit pin",
    plateau="- Plateau window (§4): **1 of 3** — r538 +0.0100pp (< 0.02: counts); r537 skeleton-blind by design (neither); r536 +0.0261pp (a real gain: reset); ",
    standing="- Standing facts: AppVersion **260620.97** (r538 the family heading digit pin, block 2 — session 53 Round 4, 27 Sept); before it 260620.96 (",
    roundlog=f"- s53-r4 (engine r538, build 260620.97, 26 Sept 23:53 → 27 Sept {T}) · a PICK pass (the dashboard refreshed; radioQuiz's T/F tables answer-marked 3 of 19 — "
             "not a round; the fate census's CHROME + FAMILY-DIALECT sections: BLL modal / click-drop = A1, BLL menu labels = D10-9) then r536's rule, THE REST OF "
             "THE PASSING GROUPS (COM / GEO [H2], TWHK / TWHR / EXPFUN / CEDK [H3], CEDO [H4], OSOH [H5]; OSAI / MXDB / TRR / TWHA dropped on the probe) · "
             "SHIPPED scoped #4 · 20 modules / 39 pages · skeleton **+0.0100pp**, ≥50 +1 · 8 dips NAMED · plateau 1 of 3.",
    archive_extra="- **What shipped (r538, 260620.97):** `ContentConverter` heading emitter path (c) over every `digits_by_prefix_families*` block; data "
                  "`digits_by_prefix_families_2`. Probe OFF 6,432 / 6,432 identical; ON 39 pages / 20 modules; +0.0100pp. Dropped on the probe: OSAI / MXDB [H5], "
                  "TRR [H3], TWHA [H3] / [H4].",
)
