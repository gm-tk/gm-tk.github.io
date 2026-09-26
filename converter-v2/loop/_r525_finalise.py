#!/usr/bin/env python3
"""ROUND 525 finalise (session 51 Round 5 — the bold activity id after a widget tag, the FRNO dialect). WSL. argv: MEAN RAW."""
import sys
import _s51_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-26 (round 525, build 260620.85) — THE BOLD ACTIVITY ID AFTER A WIDGET TAG: the FRNO family's `[Reorder autocheck]] **2C****Put the conversation together**` opens the numbered box with the bold title as its h3 (50 spans / FRNO901, FRNO902, FRFUN06); 4 modules, skeleton +0.0238pp

### 1. WHAT CHANGED

**The class** (the session-51 unboxed-box census `_s51_r3_unboxed.tsv`: 56 FRNO gold boxes rendered unboxed; the WT form by `grep`): the FRNO family (and FRFUN06) types the widget tag, then the activity id and its title in BOLD black text — `[Reorder autocheck]] **2C****Put the conversation together**`, `[Drag and drop column autocheck]] **1B****Sort the greetings**`, `[Dropbox] **1F****Lesson one task**`, and with a stray bracket span between, `[Wordfind autocheck] ] **1E****Find the French**` — **50 spans: FRNO901 28, FRNO902 20, FRFUN06 2**. The id is black text, so no box opened: the id and the title shipped inside the hand-off box as text. The gold boxes every one as `div.activity[number=<id>]` with the title as its `<h3>` above the widget.

**The fix** (`PageAssembler.#boldIdWidgetActivity`; data `Tag_Lexicon._meta.bold_id_widget_activity`, env **`BOLDIDACT_OFF`**): a widget tag (INTERACTIVE primary, no activity tag) whose black tail opens with `**<id>**` is re-parsed in the round-365 form `[Activity <id> – <the widget words>]` — the round-92 activity + widget span, which opens the numbered box, and whose tail `typed_tag_title` makes the box's `<h3>` — and the bold id leaves the tail. A stray bracket span's tail moves to the widget tag before it on the same paragraph. A family dialect (LOOP §1d exception 1: the whole FRNO family, every page).

### 2. PROOF

- In-memory probe over all 545 modules: `BOLDIDACT_OFF=1` → 6,432 / 6,432 pages identical; ON → **4 modules** (FRFUN06, FRFUN08 — its hand-off manifest only, FRNO901, FRNO902); 0 ASSEMBLE ERROR. `scoped_ship.sh … --round 525` PASS: 0 stale, containment 4 ⊆ 4, a re-planned 12-module spot-check byte-identical.
- The skeleton gate's own `match()` (`_s51_prescore.py`): **+0.0233pp, 13 up / 2 down** (FRNO902_2_0 +12.9, FRNO902_1_0 +10.8, FRNO901_5_0 +9.1, FRNO901_3_0 / 2_0 / 6_0 / 4_0 ≈ +5, …; the two dips < 0.3pp).

### 3. PROTECTED GATES

Skeleton **56.0222 → {MEAN} % @ 2486 (+0.0238pp)**, ≥50 1625 → 1627, ≥75 289 → 290, ≥90 26; RAW 39.783 → {RAW} %; compare_structure exact 16830 / EXTRA 204 / missing 879 held; body_compare ANY 234 held; clean 98.40 %, leak 52 / 42 EXACT; tags 9557; every verifier ✓, every COUNT held (`_r525_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 525`; `--gate-baseline-check` PASS. Plateau: **reset** (+0.0238pp).

**Ledger:** scoped #4 since the s50-r14 FULL (r520) · data `Tag_Lexicon._meta.bold_id_widget_activity` · env `BOLDIDACT_OFF` · code `PageAssembler.#boldIdWidgetActivity` · session 51 Round 5.
"""
F.finalise(
    N=525, old_build="260620.84", new_build="260620.85", entry=entry,
    config_comment="THE BOLD ACTIVITY ID AFTER A WIDGET TAG (session 51 Round 5; the FRNO dialect). Env BOLDIDACT_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 525 BASELINE (the bold activity id after a widget tag, "
        f"`BOLDIDACT_OFF`; SCOPED, scoped #4 since the s50-r14 FULL): SCAFFOLD mean {MEAN}% / >=50% 1627 / >=75% 290 / >=90% 26 / "
        f"RAW {RAW}% @ 2486 pairs (+0.0238pp); cs exact 16830; body ANY 234.**",
    og11="| `BOLDIDACT_OFF` | 525 | **THE BOLD ACTIVITY ID AFTER A WIDGET TAG** (session 51 Round 5). Reverts "
         "`Tag_Lexicon._meta.bold_id_widget_activity`: the FRNO `[Widget] **2C****Title**` form opens no box again — the id and title "
         "ship inside the hand-off box (the r523 output exactly). |",
    og14=f"- **Build:** `260620.85` (round 525 — **the bold activity id after a widget tag**; `BOLDIDACT_OFF`; scoped #4 since the "
         f"s50-r14 FULL; 4 modules; skeleton {MEAN} % (+0.0238pp), RAW {RAW} %).",
    gb_note=f"Round 525 (session 51 Round 5, 2026-09-26) — THE BOLD ACTIVITY ID AFTER A WIDGET TAG (BOLDIDACT_OFF): FRNO901 / 902, "
            f"FRFUN06 / 08; skeleton 56.0222 -> {MEAN} (+0.0238pp), >=50 1627, >=75 290; every other gate held; scoped #4.",
    no_round=f"- **No round in flight** (26 Sept 2026 {T}, session 51 Round 5 — r525 (the bold activity id after a widget tag) SHIPPED and "
             "committed; the in-flight marker is cleared). LAST SHIPPED **r525** (260620.85); **LAST FULL = r520 (the session-50 Round 14 "
             "backstop)**; ledger **scoped #4** (4 of headroom). Ride-along patches (LOOP §3 step 1 reads this list at every PICK): "
             "`outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, 10 pages / 9 "
             "modules — CEDK401, HIS1002, HPRE203, MXDI201, MXDI202 ×2, MXEX302, SSOG105, TWHA906, XGF9004) / `_r489_accbullet_declined.patch` "
             "(the accordion bulleted bold lead, 8 accordions / 4 modules — MXEX302, ENGS101, XGF9003, XLP05) / `_r463_declined.patch` (the "
             "WJFUN tile's \"Year N\" lead, 1 page) / `_r512_declined.patch` (the `[Activity: Embedded] <widget>` bracket, 10 modules — rides "
             "only after the TRR table-dialect ownership fix) / `_r524_declined.patch` (the callout + heading co-tag, 17 modules — rides only "
             "once an alert's run gathers the list after its title). Checked at r525: none rides (no patch has all its pages inside the 4).",
    last_shipped=f"- LAST SHIPPED: **r525** (build 260620.85, 26 Sept {T}, session 51 Round 5 — THE BOLD ACTIVITY ID AFTER A WIDGET TAG, "
                 "`BOLDIDACT_OFF`; SCOPED, **scoped #4 since the s50-r14 FULL**; 4 modules (FRNO901 / 902, FRFUN06 / 08); skeleton 56.0222 → "
                 f"{MEAN} % (+0.0238pp), ≥50 1627, ≥75 290, RAW {RAW} %; every other gate held).",
    before_them_add="the activity governs a heading co-tag",
    plateau="- Plateau window (§4): **0 of 3** — r525 +0.0238pp (a real gain: reset); s51-r4 r524 declined (neither); ",
    standing="- Standing facts: AppVersion **260620.85** (r525 the bold activity id after a widget tag — session 51 Round 5, 26 Sept); "
             "before it 260620.84 (",
    roundlog=f"- s51-r5 (engine r525, build 260620.85, 26 Sept ≈12:43 → {T}) · a PICK pass (title-only alerts: 0; the footer order F34 = KB "
             "01B's own; r522's residue ≈ 14 hand-off-swallowed journal lines) then THE BOLD ACTIVITY ID AFTER A WIDGET TAG (the FRNO dialect, "
             "50 spans) · SHIPPED scoped #4 · 4 modules · skeleton **+0.0238pp**, ≥50 +2, ≥75 +1, every other gate held · plateau reset (0 of 3).",
    archive_extra="- **What shipped (r525, 260620.85):** `PageAssembler.#boldIdWidgetActivity`; data `bold_id_widget_activity`. Probe OFF "
                  "6,432 / 6,432 identical; ON 4 modules; +0.0238pp; every other gate held.",
)
