#!/usr/bin/env python3
"""ROUND 535 finalise (session 53 Round 1 — the writer's [close X] is not an opener). WSL. argv: MEAN RAW."""
import sys
import _s53_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-26 (round 535, build 260620.94) — THE WRITER'S `[close alert box]` IS NOT AN OPENER: a callout closer typed with the word "close" (`[close alert box]`, `[close important box]`, `[close alert]`, `[close important note]`) no longer opens a phantom box — it is read as the writer's instruction (a developer note), and the box it closes keeps the form it already had; 11 modules / 20 pages, skeleton +0.0057pp, ≥50 +3

### 1. WHAT CHANGED

**The class** (session 53 Round 1's PICK pass — the s52 follow-up lane, the empty `[Alert]` + tagged content, `_s53_r1_emptyalert.py`, below the floor at 30 sites / 12 modules — exposed the root cause of part of it): `TagNormaliser.#CLOSE_PREFIX` knows only `end` / `end of` / `/`, so a closer typed with **close** fell through to the alias match and resolved to its own OPENER. For the callouts: `[close alert box]` 13, `[close important box]` 18 (12 of them `[close important box] [close tab]`), `[close alert]`, `[close important note]` — each opened a strict box that either gathered the NEXT paragraph (MXEO202 2: "You can also click on the protractor icon…" shipped in an alert the gold leaves free) or, empty, shipped with an "Empty [important]" red flag or span-wrapped the following widget (BLL252 / 254, BLLR201–203). The widget forms (`[close modal]` 46, `[close accordion]` 16, `[close clickdrop]` 17, `[close tab]` 21, `[close box]` 9) are scanner-internal and are NOT touched.

**Two designs measured before this one** (the in-memory probe, `_s52_on.sh r535`): (1) `close X` ≡ `end X` for every container, widget and sub-part → 65 pages / 19 modules, **−0.0012pp** (the tab / click-drop bundles ended early — ENGJ403's `[close tab 1]` orphaned the next tab; ENGS404's dropbox lost its box); (2) the same for the callout openers only → 20 pages, **−0.0139pp** (an explicit end switches the opener to SPAN mode, which never takes the r505 / r506 right-hand side column — MXEO202 2's `[RHS Alert box]` lost its `col-md-4 alertActivity`, −13.7 — and ENGC403's `[important box] … [open important box] … [close important box]` pairs re-nested). (3) SHIPPED: the callout `close` is a no-op writer instruction.

**The fix** (`TagNormaliser.#resolveFragment` step 3c; data `Tag_Lexicon.json _meta.close_word_closer` {{max_words 4, mode "instruction", directives [CONTAINER_OPEN]}}, env **`CLOSEWORD_OFF`**): a fragment `close [the] <≤ 4 words>` whose rest resolves to a CONTAINER_OPEN tag is returned as the instruction guard (a red developer note, which the skeleton ignores); an image description `[close up of …]` is long and never matches.

### 2. PROOF

- In-memory probe over all 545 modules: `CLOSEWORD_OFF=1` → 6,432 / 6,432 pages identical; ON → **20 pages / 11 modules** (BLL250 / 252 / 254, BLLR201–203, ENGC403, ENGJ403, ENGS404, MXEO202, MXFL301); 0 ASSEMBLE ERROR. `scoped_ship.sh … --round 535 --commit` PASS: 0 stale, containment 11 ⊆ 11, the 12-module spot-check byte-identical.
- The skeleton gate's own `match()` (`_s51_prescore.py`): **+0.0056pp, 17 up / 3 down** (BLL252_1_0 +1.7, ENGC403_11_0 +1.9, ENGJ403_3_1 +1.9, ENGC403_12_0 +1.8, MXEO202_2_0 +1.5 …); the dips are all ENGC403: 5_0 −5.07, 7_0 −0.70, 4_2 −0.32 — the phantom EMPTY `div.alert.solid > div.row > div.col-12` wrappers had matched the gold's real box, whose content (the PIPS / PEGS list) Claude leaves free because its opener `[insert important box] [insert image small to r h s …]` loses the primary slot to the image (a separate co-tag class, below the floor).

### 3. PROTECTED GATES

Skeleton **56.3343 → {MEAN} % @ 2486 (+0.0057pp)**, ≥50 1638 → 1641, ≥75 305, ≥90 29; RAW 39.9707 → {RAW} %; compare_structure exact 17024 / EXTRA 198 / missing 661 held; body_compare ANY 233 held; leak 52 / 42 EXACT; tags 9557; every verifier ✓, every COUNT held (`_r535_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 535`; `--gate-baseline-check` PASS. Plateau: **1 of 3** (+0.0057pp).

**Ledger:** scoped #1 since the s52-r11 FULL · data `Tag_Lexicon.json _meta.close_word_closer` · env `CLOSEWORD_OFF` · code `TagNormaliser.#resolveFragment` step 3c · session 53 Round 1.
"""
F.finalise(
    N=535, old_build="260620.93", new_build="260620.94", entry=entry,
    config_comment="THE WRITER'S [close alert box] IS NOT AN OPENER (session 53 Round 1; a callout closer typed with 'close' is a writer instruction). Env CLOSEWORD_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 535 BASELINE (the callout `close` closer, `CLOSEWORD_OFF`; SCOPED, scoped #1 "
        f"since the s52-r11 FULL): SCAFFOLD mean {MEAN}% / >=50% 1641 / >=75% 305 / >=90% 29 / RAW {RAW}% @ 2486 pairs (+0.0057pp); cs exact 17024 / "
        f"EXTRA 198 / missing 661; body ANY 233.**",
    og11="| `CLOSEWORD_OFF` | 535 | **THE WRITER'S `[close alert box]` IS NOT AN OPENER** (session 53 Round 1). Reverts `Tag_Lexicon.json _meta.close_word_closer`: "
         "a callout closer typed with the word 'close' resolves to the callout's OPENER again (a phantom box — the r534 output exactly). |",
    og14=f"- **Build:** `260620.94` (round 535 — **the callout `close` closer**; `CLOSEWORD_OFF`; scoped #1 since the s52-r11 FULL; 11 modules / 20 pages; "
         f"skeleton {MEAN} % (+0.0057pp), RAW {RAW} %, ≥50 +3).",
    gb_note=f"Round 535 (session 53 Round 1, 2026-09-26) — THE CALLOUT CLOSE CLOSER (CLOSEWORD_OFF): 11 modules / 20 pages; skeleton 56.3343 -> {MEAN} "
            f"(+0.0057pp), >=50 1641; every other gate held; scoped #1 since the s52-r11 FULL.",
    no_round=f"- **No round in flight** (26 Sept 2026 {T}, session 53 Round 1 — r535 (the callout `close` closer) SHIPPED and committed; the in-flight marker "
             "is cleared). LAST SHIPPED **r535** (260620.94); **LAST FULL = r534 (the session-52 Round 11 backstop)**; ledger **scoped #1** (7 of headroom). "
             "Ride-along patches (LOOP §3 step 1 reads this list at every PICK): "
             "`outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, 10 pages / 9 modules — "
             "CEDK401, HIS1002, HPRE203, MXDI201, MXDI202 ×2, MXEX302, SSOG105, TWHA906, XGF9004) / `_r489_accbullet_declined.patch` (the accordion "
             "bulleted bold lead, 8 accordions / 4 modules — MXEX302, ENGS101, XGF9003, XLP05) / `_r463_declined.patch` (the WJFUN tile's \"Year N\" "
             "lead, 1 page) / `_r512_declined.patch` (the `[Activity: Embedded] <widget>` bracket, 10 modules — rides only after the TRR table-dialect "
             "ownership fix) / `_r524_declined.patch` (the callout + heading co-tag, 17 modules — rides only once an alert's run gathers the list "
             "after its title). Checked at r535: `_r469_declined.patch` names ENGC403 (in r535's set) but its class (the alert title) is not r535's — "
             "not taken; none rides.",
    last_shipped=f"- LAST SHIPPED: **r535** (build 260620.94, 26 Sept {T}, session 53 Round 1 — THE WRITER'S `[close alert box]` IS NOT AN OPENER, `CLOSEWORD_OFF`; "
                 "SCOPED, **scoped #1 since the s52-r11 FULL**; 11 modules / 20 pages; skeleton 56.3343 → "
                 f"{MEAN} % (+0.0057pp), ≥50 1641, ≥75 305, RAW {RAW} %; every other gate held).",
    before_them_add="r533 the bare video URL",
    plateau="- Plateau window (§4): **1 of 3** — r535 +0.0057pp (< 0.02: counts); r534 +0.0575pp (a real gain: reset); r533 +0.0063pp (counted); ",
    standing="- Standing facts: AppVersion **260620.94** (r535 the callout `close` closer — session 53 Round 1, 26 Sept); before it 260620.93 (",
    roundlog=f"- s53-r1 (engine r535, build 260620.94, 26 Sept 22:50 → {T}) · a PICK pass (the s52 empty-`[Alert]` + tagged-content lane, `_s53_r1_emptyalert.py`: 30 sites / "
             "12 modules, below the floor; the RHS-with-explicit-end lane `_s53_r1_rhsend.py`, 52 sites — side columns not visible to the cs chain) then THE "
             "WRITER'S `[close alert box]` IS NOT AN OPENER (a no-op instruction; two designs declined on the probe: `close` ≡ `end` −0.0012pp / −0.0139pp) · "
             "SHIPPED scoped #1 · 11 modules / 20 pages · skeleton **+0.0057pp**, ≥50 +3 · three ENGC403 dips NAMED · plateau 1 of 3.",
    archive_extra="- **What shipped (r535, 260620.94):** `TagNormaliser.#resolveFragment` step 3c; data `Tag_Lexicon.json _meta.close_word_closer` (mode instruction). "
                  "Probe OFF 6,432 / 6,432 identical; ON 20 pages / 11 modules; +0.0057pp; every gate held-or-improved. Declined designs: close ≡ end for every "
                  "container / widget / sub-part (65 pages, −0.0012pp) and for the callouts only (20 pages, −0.0139pp — the explicit end switches the opener to "
                  "SPAN mode: the RHS side column lost, ENGC403 re-nested).",
)
