#!/usr/bin/env python3
"""ROUND 506 finalise (session 49 Round 7 — D15-18 part 2, the lost RHS boxes, RHSTAGGED_OFF). WSL. argv: MEAN RAW."""
import sys
import _s49_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-25 (round 506, build 260620.69) — D15-18 PART 2: THE LOST RIGHT-HAND BOXES — a box whose content the writer typed on the following lines under their own tags gets that content, in the side column (15 pages / 8 modules; XGF9001's nine `[Alert RHS] [H3]` boxes restored; the "Empty [alert]" flags on those pages 12 → 4)

### 1. WHAT CHANGED

**The decision** (Chris, 25 Sept 2026, D15-18 — Option B; the lost-box fix "the box must never vanish"). **The fault:** a right-hand box whose writer typed its content under its own tags — `[alert RHS]` then `[body] When rounding, remember these two rules:` + bullets (MXFL301), `[Alert box RHS]` then `[H3] Extra fun – a jigsaw` + `[Body] …` (SSFUN05), the Ākonga notes of SSFUN01 / 07, HIS1005's `Modern-day slavery` — rendered as an EMPTY box with the red flag "Empty [alert] — the writer left a callout blank" and the content falling out below it; and `[Alert RHS] [H3] Key questions` + bullets (XGF9001 ×9, the heading wins the parse) rendered no box at all (gold `XGF9001-01.1.html` l.56–61: `col-md-3 offset-md-1 … > alertActivity > h3 + ul`; PageForge `XGF9001_2_0.html` l.39–46: an `<h4>` and a list in the main column).

**The fix** (`ContentConverter` — `rhsTaggedRun` / `rhsPlace`, the r333 branch and the ELEMENT case; `#sideAlertCol` takes the gathered content; data `callouts.positional_side_alert.always_side.tagged_content`; env `RHSTAGGED_OFF`; Standard / Fundamentals only, as r505): the run after the box — one heading as the box's lead (the def's `h4`, never the group's div-lead convention), then `[body]` lines and plain lines, bullets included — becomes the box's content; the box ends where its list ends (a plain or `[Body]` line after the bullets stays on the page — XGF9001's "Click on the accordion…"; consecutive black lines arrive joined in one item, so an item is taken line by line and its remainder left in place). The side column goes beside the row just closed (r333's pairing and box-style choice) or is held for the next row (r505).

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 0 pages changed**; ON **15 pages / 8 modules** (EXIP901 HIS1005 HPRE203 MXFL301 SSFUN01 SSFUN05 SSFUN07 XGF9001 ×8 pages); regenerated = ON byte-for-byte (56 / 56); `scoped_ship.sh`: 0 stale, containment 8 ⊆ 8, the 12-module spot-check byte-identical.
- **"Empty [alert]" red flags on the 15 pages: 12 → 4.** The RHS family (`_r506_measure_on.py`, `_r506_tagdelta.log`, before = the shipped r505 state): **side-column agreement 95 → 100 / 139** (+9 — XGF9001's boxes; −4 NAMED — SSFUN05 / EXIP901 gold paragraph, HPRE203 / MXFL301 gold full-width); exact shape 78 → 76 (XGF9001's gold box style is `alertActivity`, the position rule gives a forward-held box `alert top` — XGF9006's golds use `alert top` 8 : 4, so there is no XGF series convention to follow).

### 3. PROTECTED GATES

- Skeleton **55.5401 → {MEAN} % @ 2486**, RAW 39.467 → {RAW} %; ≥50 1599, ≥75 276 HELD; 15 movers, **10 up / 5 down** (pp-sum +8.0): SSFUN07_0_0 +4.6, XGF9001_9_0 +1.9, MXFL301_4_0 +1.7, XGF9001_3_0 +1.7 …; down NAMED — HIS1005_9_0 57.1 → 55.6, SSFUN05_0_0 24.5 → 23.9 (gold paragraph), XGF9001_4 / 5 / 7 −0.4 to −0.8.
- **compare_structure exact 16766 → 16762 (−4), EXTRA 199 → 204 (+5), missing 888 → 887 (−1) — ACCEPTED AS NAMED** (`_r506_csdelta.py`): XGF9001 exact −4 / EXTRA +4 — the nine restored boxes sit in `alert top` where the XGF9001 gold writes `alertActivity` (the position rule Chris kept); SSFUN01 EXTRA +1 / missing −1 — its Ākonga box now in the side column. body / clean / leak EXACT; every verifier ✓, every COUNT held (`_r506_gates.log`); `_fastloop_diff.py … --accept-named … --commit --round 506`; `--gate-baseline-check` PASS. Plateau: skeleton +0.00 but cs moved (NAMED) — neither.

**Named overrides:** the side column over SSFUN05 / EXIP901's gold paragraph and HPRE203 / MXFL301's full-width gold box; `alert top` over XGF9001's `alertActivity` — by Chris's D15-18.

**Ledger:** scoped #1 since the r505 FULL · data `positional_side_alert.always_side.tagged_content` · env `RHSTAGGED_OFF` · code `ContentConverter` · tools `_r506_measure_on.py`, `_r506_tagdelta.py`, `_r506_csdelta.py`, `_r506_finalise.py` · the in-flight marker was raised late (after the edits) — recorded · session 49 Round 7.
"""
F.finalise(
    N=506, old_build="260620.68", new_build="260620.69", entry=entry,
    config_comment="D15-18 PART 2 — THE LOST RHS BOXES (session 49 Round 7): a right-hand box's content typed under its own tags on the "
                   "following lines is gathered into the side column. Env RHSTAGGED_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 506 BASELINE (D15-18 part 2 the lost RHS boxes, "
        f"`RHSTAGGED_OFF`; SCOPED, scoped #1 since the r505 FULL): SCAFFOLD mean {MEAN}% / >=50% 1599 / >=75% 276 / >=90% 26 / RAW {RAW}% "
        f"@ 2486 pairs — 10 up / 5 down; cs exact 16762 (−4) / EXTRA 204 (+5) / missing 887 (−1) ACCEPTED AS NAMED (XGF9001's box style).**",
    og11="| `RHSTAGGED_OFF` | 506 | **D15-18 PART 2 — THE LOST RHS BOXES** (session 49 Round 7). Reverts "
         "`positional_side_alert.always_side.tagged_content`: a right-hand box whose content follows under its own tags is an EMPTY box "
         "again ('Empty [alert]'), and a heading line co-tagged with an RHS alert renders as a plain heading; byte-identical to r505. |",
    og14=f"- **Build:** `260620.69` (round 506 — **D15-18 part 2, the lost RHS boxes**; `RHSTAGGED_OFF`; scoped #1 since the r505 FULL; "
         f"15 pages / 8 modules; skeleton {MEAN} % @ 2486; side-column agreement 95 → 100; cs −4 / +5 NAMED).",
    gb_note=f"Round 506 (session 49 Round 7, 2026-09-25) — D15-18 PART 2 THE LOST RHS BOXES (RHSTAGGED_OFF): 15 pages / 8 modules; "
            f"SCAFFOLD 55.5401 -> {MEAN} @ 2486, 10 up / 5 down; cs exact -4 / EXTRA +5 / missing -1 ACCEPTED AS NAMED (XGF9001's gold "
            f"alertActivity vs the position rule's alert top; SSFUN01's Akonga box); Empty [alert] flags 12 -> 4; scoped #1.",
    no_round=f"- **No round in flight** (25 Sept 2026 {T}, session 49 Round 7 — r506 (D15-18 part 2, the lost RHS boxes) SHIPPED and "
             "committed; the in-flight marker is cleared). LAST SHIPPED **r506** (260620.69); **LAST FULL = r505 (the session-49 Round 6 "
             "backstop)**; ledger **scoped #1** (7 of headroom). Ride-along patches (LOOP §3 step 1 reads this list at every PICK): "
             "`outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403; checked at r505 / r506, outside their sets) / "
             "`_r469b_declined.patch` (buttons, 10 pages) / `_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages) / "
             "`_r489_accbullet_declined.patch` (the accordion bulleted bold lead, 8 accordions / 4 modules) / `_r463_declined.patch` (the "
             "WJFUN tile's \"Year N\" lead, 1 page).",
    last_shipped=f"- LAST SHIPPED: **r506** (build 260620.69, 25 Sept {T}, session 49 Round 7 — D15-18 PART 2, THE LOST RHS BOXES, "
                 "`RHSTAGGED_OFF`; SCOPED, **scoped #1 since the r505 FULL**; 15 pages / 8 modules; XGF9001's nine boxes restored, the "
                 f"\"Empty [alert]\" flags 12 → 4, side-column agreement 95 → 100 / 139; **skeleton 55.5401 → {MEAN} % @ 2486**, 10 up / 5 "
                 "down; cs exact −4 / EXTRA +5 / missing −1 NAMED).",
    before_them_add="D15-17 CEDT301 one tabbed page",
    plateau="- Plateau window (§4): **0 of 3** — r506 skeleton +0.00 but cs moved NAMED (neither); ",
    standing="- Standing facts: AppVersion **260620.69** (r506 D15-18 part 2 the lost RHS boxes — session 49 Round 7, 25 Sept); before it "
             "260620.68 (",
    roundlog=f"- s49-r7 (engine r506, build 260620.69, 25 Sept ≈20:25 → {T}) · D15-18 PART 2 THE LOST RHS BOXES (a box's content typed "
             "under its own tags gathered into the side column; XGF9001's co-tagged `[Alert RHS] [H3]`) · SHIPPED scoped #1, cs −4 / +5 "
             "NAMED · 15 pages / 8 modules, Empty [alert] 12 → 4, side agreement 95 → 100 · plateau 0 of 3 (neither). The in-flight "
             "marker was raised late (after the edits).",
    archive_extra="- **What shipped (r506, 260620.69):** `always_side.tagged_content` (env `RHSTAGGED_OFF`), `ContentConverter` rhsTaggedRun "
                  "/ rhsPlace. Probe OFF 0; ON 15 pages / 8 modules; scoped proof with the cs movers NAMED.",
)
