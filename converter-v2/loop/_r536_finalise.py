#!/usr/bin/env python3
"""ROUND 536 finalise (session 53 Round 2 — the family heading digit pin). WSL. argv: MEAN RAW."""
import sys
import _s53_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-26 (round 536, build 260620.95) — THE FAMILY KEEPS THE WRITER'S HEADING DIGIT: FRFUN's `[H2]` ships at h2, WJFUN's and ENGC's `[H4]` at h4 (the r373 / r374 per-prefix pin, three more families found by the new writer-cue fate census); 15 modules / 41 pages, skeleton +0.0261pp, ≥50 +3

### 1. WHAT CHANGED

**The instrument** (NEW, session 53 Round 2 — the s52 handover asked for the empty lanes re-read with one): `outputs/_s53_tagfate.py`, THE WRITER-CUE FATE CENSUS — every Writers-Template item (the engine's own item stream, `outputs/_s52_items/`) located by its text on the gold paired page and on Claude's (the placement census parser: block tag + container region), its fate recorded per side as `<tag>@<region>` and aggregated by the writer's cue (the item's tag, a bold lead, a bullet): 72,903 items / 533 modules in 70 s. Its heading rows — `[H2]` gold h2 / Claude h3 on 154 items / 97 pages; `[H4]` gold h4 / Claude h5 on 55 / 28 — were split per family by `outputs/_s53_r2_hlevel.py` (writer digit vs the gold's level vs Claude's, free-body headings, TOP vs sub-level on the page).

**The class**: the gold keeps the writer's digit where the r45 shift + rank puts it one level deeper, in three families the r373 / r374 table (`keep_writer_digit.digits_by_prefix`) does not name — **FRFUN `[H2]` → h2 0.92** (64 items / 13 pages; Claude h3 0.73 / h4 0.27), **WJFUN `[H4]` → h4 1.00** (52 / 9 modules; Claude h5 0.90), **ENGC `[H4]` → h4 0.92** (39 / 5 modules / 14 pages; Claude h5 0.46). A per-group rule (LOOP §1d exception 2 — the groups summed). CEDT `[H2]` (0.63 by items) was probed and DROPPED: CEDT501's gold follows the shift (−12.1 over 12 pages). No KB rule fixes body heading levels (authority §1b-3/4).

**The fix** (`ContentConverter` heading emitter, path (c) beside the r371 template pin and the r373 prefix pin; data `Emit_Templates.json body_region.heading_relevel.keep_writer_digit.digits_by_prefix_families` {{env, "2": [FRFUN], "4": [WJFUN, ENGC]}}, env **`HKEEPFAM_OFF`**): the heading carries the transient `data-wd` marker, so `#relevelHeadings` pins it at the writer's digit and ranks the page's other headings exactly as before.

### 2. PROOF

- In-memory probe over all 545 modules: `HKEEPFAM_OFF=1` → 6,432 / 6,432 pages identical; ON → **41 pages / 15 modules** (ENGC206 / 403, FRFUN06 / 07 / 08, ten WJFUN); 0 ASSEMBLE ERROR. `scoped_ship.sh … --round 536 --commit` PASS: 0 stale, containment 15 ⊆ 15, the 12-module spot-check byte-identical.
- The skeleton gate's own `match()`: **+0.0261pp, 19 up / 4 down** (FRFUN06 +61.9 over 10 pages, ENGC403 +4.6, the WJFUN pages +0.2…+0.9). The dips, NAMED: FRFUN06_4_0 −6.36 — the ON page matches the gold's `h2`s exactly; an alignment artefact (position-free overlap 92 → 97 of 139 RISES, `_s52_companion.py`); FRFUN08_8_0 / 9_0 / 10_0 −2.5…−2.7 — FRFUN08's gold follows the shift (`h3`), the family's outlier (position-free 27 → 26, 31 → 30, 23 → 22).

### 3. PROTECTED GATES

Skeleton **56.3400 → {MEAN} % @ 2486 (+0.0261pp)**, ≥50 1641 → 1644, ≥75 305, ≥90 29; RAW 39.9718 → {RAW} %; compare_structure exact 17024 / EXTRA 198 / missing 661 held; body_compare ANY 233 held; leak 52 / 42 EXACT; tags 9557; every verifier ✓, every COUNT held (`_r536_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 536`; `--gate-baseline-check` PASS. Plateau: **reset** (+0.0261pp).

**Ledger:** scoped #2 since the s52-r11 FULL · data `keep_writer_digit.digits_by_prefix_families` · env `HKEEPFAM_OFF` · code `ContentConverter` heading emitter path (c) · session 53 Round 2.
"""
F.finalise(
    N=536, old_build="260620.94", new_build="260620.95", entry=entry,
    config_comment="THE FAMILY KEEPS THE WRITER'S HEADING DIGIT (session 53 Round 2; FRFUN [H2] -> h2, WJFUN / ENGC [H4] -> h4). Env HKEEPFAM_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 536 BASELINE (the family heading digit pin, `HKEEPFAM_OFF`; SCOPED, scoped #2 "
        f"since the s52-r11 FULL): SCAFFOLD mean {MEAN}% / >=50% 1644 / >=75% 305 / >=90% 29 / RAW {RAW}% @ 2486 pairs (+0.0261pp); cs exact 17024 / "
        f"EXTRA 198 / missing 661; body ANY 233.**",
    og11="| `HKEEPFAM_OFF` | 536 | **THE FAMILY KEEPS THE WRITER'S HEADING DIGIT** (session 53 Round 2). Reverts `keep_writer_digit.digits_by_prefix_families`: "
         "FRFUN's [H2] and WJFUN's / ENGC's [H4] take the r45 shift + rank again (the r535 output exactly). |",
    og14=f"- **Build:** `260620.95` (round 536 — **the family heading digit pin**; `HKEEPFAM_OFF`; scoped #2 since the s52-r11 FULL; 15 modules / 41 pages; "
         f"skeleton {MEAN} % (+0.0261pp), RAW {RAW} %, ≥50 +3).",
    gb_note=f"Round 536 (session 53 Round 2, 2026-09-26) — THE FAMILY HEADING DIGIT PIN (HKEEPFAM_OFF): 15 modules / 41 pages; skeleton 56.3400 -> {MEAN} "
            f"(+0.0261pp), >=50 1644; every other gate held; scoped #2 since the s52-r11 FULL.",
    no_round=f"- **No round in flight** (26 Sept 2026 {T}, session 53 Round 2 — r536 (the family heading digit pin) SHIPPED and committed; the in-flight marker "
             "is cleared). LAST SHIPPED **r536** (260620.95); **LAST FULL = r534 (the session-52 Round 11 backstop)**; ledger **scoped #2** (6 of headroom). "
             "Ride-along patches (LOOP §3 step 1 reads this list at every PICK): "
             "`outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, 10 pages / 9 modules — "
             "CEDK401, HIS1002, HPRE203, MXDI201, MXDI202 ×2, MXEX302, SSOG105, TWHA906, XGF9004) / `_r489_accbullet_declined.patch` (the accordion "
             "bulleted bold lead, 8 accordions / 4 modules — MXEX302, ENGS101, XGF9003, XLP05) / `_r463_declined.patch` (the WJFUN tile's \"Year N\" "
             "lead, 1 page) / `_r512_declined.patch` (the `[Activity: Embedded] <widget>` bracket, 10 modules — rides only after the TRR table-dialect "
             "ownership fix) / `_r524_declined.patch` (the callout + heading co-tag, 17 modules — rides only once an alert's run gathers the list "
             "after its title). Checked at r536: none rides (ENGC403 / WJFUN are in r536's set; the r469 alert title and the r463 tile lead are other classes).",
    last_shipped=f"- LAST SHIPPED: **r536** (build 260620.95, 26 Sept {T}, session 53 Round 2 — THE FAMILY KEEPS THE WRITER'S HEADING DIGIT, `HKEEPFAM_OFF`; "
                 "SCOPED, **scoped #2 since the s52-r11 FULL**; 15 modules / 41 pages; skeleton 56.3400 → "
                 f"{MEAN} % (+0.0261pp), ≥50 1644, ≥75 305, RAW {RAW} %; every other gate held).",
    before_them_add="r534 the bare link line",
    plateau="- Plateau window (§4): **0 of 3** — r536 +0.0261pp (a real gain: reset); r535 +0.0057pp (counted); ",
    standing="- Standing facts: AppVersion **260620.95** (r536 the family heading digit pin — session 53 Round 2, 26 Sept); before it 260620.94 (",
    roundlog=f"- s53-r2 (engine r536, build 260620.95, 26 Sept 23:15 → {T}) · a PICK pass with a NEW instrument — THE WRITER-CUE FATE CENSUS "
             "(`_s53_tagfate.py`: every WT item's gold / Claude fate by cue, 72,903 items) + `_s53_r2_hlevel.py` per family — then THE FAMILY KEEPS THE "
             "WRITER'S HEADING DIGIT (FRFUN [H2] → h2, WJFUN / ENGC [H4] → h4; CEDT dropped on the probe) · SHIPPED scoped #2 · 15 modules / 41 pages · "
             "skeleton **+0.0261pp**, ≥50 +3 · four dips NAMED (FRFUN06_4_0 an alignment artefact; FRFUN08 the outlier) · plateau reset (0 of 3).",
    archive_extra="- **What shipped (r536, 260620.95):** `ContentConverter` heading emitter path (c); data `keep_writer_digit.digits_by_prefix_families`. Probe OFF "
                  "6,432 / 6,432 identical; ON 41 pages / 15 modules; +0.0261pp; every gate held-or-improved. CEDT dropped on the first probe (CEDT501 −12.1).",
)
