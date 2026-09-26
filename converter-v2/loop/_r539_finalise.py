#!/usr/bin/env python3
"""ROUND 539 finalise (session 53 Round 5 — the one-level shift under a body [H1]). WSL. argv: MEAN RAW."""
import sys
import _s53_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-27 (round 539, build 260620.98) — THE ONE-LEVEL SHIFT UNDER A BODY `[H1]`: ARFUN's `[H2]` ships at h3 and ARFUN's / TWHT's `[H3]` at h4 (the gold's single shift) where the r45 rank pushed them two deep; 5 modules / 5 pages, skeleton +0.0038pp — a family dialect under the floor (LOOP §1d exception 1)

### 1. WHAT CHANGED

**The class** (`outputs/_s53_r5_hlevel1.py`, the r536 heading probe extended to the writer's `[H1]`): where a body `[H1]` sits above them, the rank pool holds its level, so the page's `[H2]` / `[H3]` rank TWO levels down while the gold shifts them ONE — ARFUN `[H2]` gold h3 (0.54 sub-level / 0.85 top) / Claude h4 0.89 (64 items / 4 pages), ARFUN `[H3]` gold h4 0.63 / Claude h5 0.63 (30 / 4), TWHT `[H3]` gold h4 0.69 / Claude h5 0.77 (13 / 1). EXPFUN `[H2]` (gold h3 0.70) was probed and DROPPED: −1.2 over 4 pages (EXPFUN02 / 04 / 05 follow the rank).

**The fix** (`ContentConverter` heading emitter path (c): a `digits_by_prefix_families*` block may carry `pin_levels` {{digit: level}}, and the level rides in the transient `data-wd` marker that `#relevelHeadings` pins at — the r536 / r538 blocks carry none and are byte-identical; data `keep_writer_digit.digits_by_prefix_families_3` {{pin_levels {{"2": 3, "3": 4}}, "2": [ARFUN], "3": [ARFUN, TWHT]}}, env **`HKEEPFAM3_OFF`**).

### 2. PROOF

- In-memory probe over all 545 modules: `HKEEPFAM3_OFF=1` → 6,432 / 6,432 pages identical (run before the regeneration); ON → **5 pages / 5 modules** (ARFUN01 / 02 / 04 / 05, TWHT903); 0 ASSEMBLE ERROR. `scoped_ship.sh … --round 539 --commit` PASS (re-run after a comment-only edit that names the toggle for the step-0 invariant; the regenerated pages are byte-identical to the probe's saved ON pages, so the gate suite measured exactly this output): 0 stale, containment 5 ⊆ 5, the 12-module spot-check byte-identical.
- The skeleton gate's own `match()`: **+0.0038pp, 4 up / 0 down** (ARFUN05 +4.7, TWHT903 +2.5, ARFUN02 +2.0, ARFUN04 +0.3; ARFUN01 changed, score unchanged) — every changed page up or neutral: a family dialect under the floor (§1d exception 1).

### 3. PROTECTED GATES

Skeleton **56.3761 → {MEAN} % @ 2486 (+0.0038pp)**, ≥50 1645, ≥75 305, ≥90 29; RAW 40.0256 → {RAW} %; compare_structure exact 17024 / EXTRA 198 / missing 661 held; body_compare ANY 233 held; leak 52 / 42 EXACT; tags 9557; every verifier ✓, every COUNT held (`_r539_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 539`; `--gate-baseline-check` PASS. Plateau: **2 of 3** (+0.0038pp — the next PICK must predict ≥ 0.02pp or be gate-neutral by design).

**Ledger:** scoped #5 since the s52-r11 FULL · data `keep_writer_digit.digits_by_prefix_families_3` · env `HKEEPFAM3_OFF` · code `ContentConverter` heading emitter path (c) `pin_levels` · session 53 Round 5.
"""
F.finalise(
    N=539, old_build="260620.97", new_build="260620.98", entry=entry,
    config_comment="THE ONE-LEVEL SHIFT UNDER A BODY [H1] (session 53 Round 5; ARFUN [H2] -> h3, ARFUN / TWHT [H3] -> h4). Env HKEEPFAM3_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 539 BASELINE (the one-level shift under a body [H1], `HKEEPFAM3_OFF`; SCOPED, scoped #5 "
        f"since the s52-r11 FULL): SCAFFOLD mean {MEAN}% / >=50% 1645 / >=75% 305 / >=90% 29 / RAW {RAW}% @ 2486 pairs (+0.0038pp); cs exact 17024 / "
        f"EXTRA 198 / missing 661; body ANY 233.**",
    og11="| `HKEEPFAM3_OFF` | 539 | **THE ONE-LEVEL SHIFT UNDER A BODY [H1]** (session 53 Round 5). Reverts `keep_writer_digit.digits_by_prefix_families_3`: "
         "ARFUN [H2] and ARFUN / TWHT [H3] take the r45 rank again (two levels under a body [H1]; the r538 output exactly). |",
    og14=f"- **Build:** `260620.98` (round 539 — **the one-level shift under a body [H1]**; `HKEEPFAM3_OFF`; scoped #5 since the s52-r11 FULL; 5 modules / 5 pages; "
         f"skeleton {MEAN} % (+0.0038pp), RAW {RAW} %).",
    gb_note=f"Round 539 (session 53 Round 5, 2026-09-27) — THE ONE-LEVEL SHIFT UNDER A BODY [H1] (HKEEPFAM3_OFF): 5 modules / 5 pages; skeleton 56.3761 -> {MEAN} "
            f"(+0.0038pp); every other gate held; scoped #5 since the s52-r11 FULL.",
    no_round=f"- **No round in flight** (27 Sept 2026 {T}, session 53 Round 5 — r539 (the one-level shift under a body [H1]) SHIPPED and committed; the in-flight marker "
             "is cleared). LAST SHIPPED **r539** (260620.98); **LAST FULL = r534 (the session-52 Round 11 backstop)**; ledger **scoped #5** (3 of headroom). "
             "Ride-along patches (LOOP §3 step 1 reads this list at every PICK): "
             "`outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, 10 pages / 9 modules — "
             "CEDK401, HIS1002, HPRE203, MXDI201, MXDI202 ×2, MXEX302, SSOG105, TWHA906, XGF9004) / `_r489_accbullet_declined.patch` (the accordion "
             "bulleted bold lead, 8 accordions / 4 modules — MXEX302, ENGS101, XGF9003, XLP05; its `bullet_bold_lead` data block is ALREADY in `Emit_Templates.json` "
             "(the r491 ride-along note) — verify and strike at the next accordion round) / `_r463_declined.patch` (the WJFUN tile's \"Year N\" "
             "lead, 1 page) / `_r512_declined.patch` (the `[Activity: Embedded] <widget>` bracket, 10 modules — rides only after the TRR table-dialect "
             "ownership fix) / `_r524_declined.patch` (the callout + heading co-tag, 17 modules — rides only once an alert's run gathers the list "
             "after its title). Checked at r539: none rides.",
    last_shipped=f"- LAST SHIPPED: **r539** (build 260620.98, 27 Sept {T}, session 53 Round 5 — THE ONE-LEVEL SHIFT UNDER A BODY [H1], `HKEEPFAM3_OFF`; "
                 "SCOPED, **scoped #5 since the s52-r11 FULL**; 5 modules / 5 pages; skeleton 56.3761 → "
                 f"{MEAN} % (+0.0038pp), RAW {RAW} %; every other gate held).",
    before_them_add="r537 the accordion panel bullet list",
    plateau="- Plateau window (§4): **2 of 3** — r539 +0.0038pp (< 0.02: counts); r538 +0.0100pp (counted); ",
    standing="- Standing facts: AppVersion **260620.98** (r539 the one-level shift under a body [H1] — session 53 Round 5, 27 Sept); before it 260620.97 (",
    roundlog=f"- s53-r5 (engine r539, build 260620.98, 27 Sept 00:29 → {T}) · THE ONE-LEVEL SHIFT UNDER A BODY [H1] (`_s53_r5_hlevel1.py`: ARFUN [H2] → h3, ARFUN / "
             "TWHT [H3] → h4 where the rank pushed them two deep; EXPFUN dropped on the probe) · SHIPPED scoped #5 · 5 modules / 5 pages · skeleton "
             "**+0.0038pp**, 4 up / 0 down — a family dialect under the floor (§1d exc. 1) · plateau 2 of 3.",
    archive_extra="- **What shipped (r539, 260620.98):** `ContentConverter` heading emitter path (c) `pin_levels`; data `digits_by_prefix_families_3`. Probe OFF "
                  "6,432 / 6,432 identical; ON 5 pages / 5 modules; +0.0038pp. The first ship attempt BLOCKED on the step-0 toggle invariant (the toggle named only "
                  "in data) — a comment naming it added, the set regenerated (byte-identical to the probe's ON pages), the proof re-run: PASS.",
)
