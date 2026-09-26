#!/usr/bin/env python3
"""ROUND 530 finalise (session 52 Round 3 — the whakataukī's other writer forms). WSL. argv: MEAN RAW."""
import sys
import _s52_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-26 (round 530, build 260620.89) — THE WHAKATAUKĪ'S OTHER WRITER FORMS: the writer's own `[Whakatauki]` no longer ships EMPTY when its proverb, translation and commentary arrive merged into one item, and a proverb typed as a `[Body]` / payload-only `[Alert]` / `[Important]` payload is the whakatauki box (KB 07B §7); 18 modules, skeleton +0.0074pp, compare_structure exact +19 / EXTRA −5 / missing −11

### 1. WHAT CHANGED

**The class** (the whakataukī residue after r528 — `_s52_r3_whkres.py`: 23 gold `div.whakatauki` boxes Claude still renders bare, ≈ 22 modules, in six writer shapes, each read against the module's WT item stream `outputs/_s52_items/`): (A) the writer TAGGED it, but the box shipped EMPTY with an 'Empty [whakatauki]' red flag (SSEA203_0_0, EXBP901_1_0 / _4_0, EXIP901_5_0, FRNO902_0_0 …) — by emit time an earlier pass has joined the proverb, its translation and the commentary into ONE black item (`"**Nāu te rourou…**\\n*With your food basket…*\\nThis whakatauki reflects…"`), and `#gatherProverb`'s length test read the whole item as commentary; (B) the proverb as the payload of a callout whose whole content is the pair (`[Alert] *Kō ngā tahu ā ō tapuwai inanahi…*` + the English: ANZH105, ANZH205, SSOG101; XDLS501's `[Important Statement]`); (C) the proverb as a `[Body]` payload (`[Body] *Tuku iho, he tapu te upoko.*` + the English: PHE1007, BLLR201, XGF9002). Not taken (below the floor, recorded): the reo + English GLUED on one line with no separator (ENGS101, MXFU201 / 202, MXFL203, TWHA905, WJFUN210, EXPFUN06 — 7 pages), the unknown label tags (`[whakaukī]` XGF9003, a bare `Whakatauki` ENGI400), TWHA906's `[quote]`s the gold boxes as whakatauki (class C).

**The fix** — one class, one env **`WHKFORMS_OFF`**: (A) `ContentConverter.#gatherProverb` — a merged item over `proverb_max_chars` gives up its leading short lines up to `proverb_max_paragraphs` and keeps the rest as free body; a leading label line (`**Whakatauki**`, FRNO902) stays out of the box; and the reo|english pipe / spaced-dash split now runs only when the gathered content is ONE line (an English line's own dash — "Pursue excellence – should you stumble…", EXBP901 — is punctuation; unguarded it split the line, −10pp) — data `callouts.by_tag.whakatauki.proverb_split_merged` {{label_pattern, pipe_split_single_line_only}}; (B) + (C) `PageAssembler.#untaggedProverb`'s second pass — a `body` / `alert` / `important` tag whose payload is an all-Māori-phonotactic line followed by its English is re-typed as the whakatauki with `reo | english` as its payload (an alert / important only when a tag or the end follows the English — the pair is its whole content); the overview's module-menu region (a `[TITLE BAR]` section to the next marker) is skipped by this pass (ENGI202's Understand block — unguarded, the menu printed the raw `reo | english`; applied to r528's pass too it cost PWYWHA1 / XWHA01 / TWHA903 their boxes, so it guards this pass only) — data `callouts.untagged_proverb.payload_forms`.

### 2. PROOF

- In-memory probe over all 545 modules: `WHKFORMS_OFF=1` → 6,432 / 6,432 pages identical; ON → **24 pages / 18 modules**; 0 ASSEMBLE ERROR. `scoped_ship.sh … --round 530 --commit` PASS: 0 stale, containment 18 ⊆ 18, the 12-module spot-check byte-identical.
- The skeleton gate's own `match()` (`_s51_prescore.py`): **+0.0074pp, 15 up / 4 down** (ANZH105_0_0 +9.2, SSEA203_0_0 +7.8, BLLR201_0_0 +2.5, XGF9002_9_0 +2.0, SSOG101_0_0 +1.9, ANZH205_0_0 +1.8 …). The dips, NAMED with their companion numbers (`_s52_companion.py`): **EXIP901_5_0 28.26 → 18.74** — its box now matches the gold's exactly (reo + English, commentary free), position-free overlap 122 → **124** / 184 while the aligned matches fall 65 → 43 (difflib re-anchors on a 276-line page); **FRNO902_0_0 78.57 → 74.65** — overlap 56 → **58** / 72 (the gold has TWO proverb boxes, Māori and French, under the one writer tag; the label line stays after the box); PHE1007_1_0 −0.91, CEDR203_0_0 −0.25.

### 3. PROTECTED GATES

Skeleton **56.2391 → {MEAN} % @ 2486 (+0.0074pp)**, ≥50 1632 held, ≥75 300 → 301, ≥90 28; RAW 39.942 → {RAW} %; compare_structure exact 16986 → 17005 (+19) / EXTRA 203 → 198 (−5) / missing 672 → 661 (−11); body_compare ANY 234 held; clean 98.40 %, leak 52 / 42 EXACT; tags 9557; every verifier ✓, every COUNT held (`_r530_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 530`; `--gate-baseline-check` PASS. Plateau: **1 of 3** (+0.0074pp < 0.02 — a real but small gain; the §4 window counts it).

**Ledger:** scoped #3 since the s51-r12 FULL (r526) · data `callouts.by_tag.whakatauki.proverb_split_merged` + `callouts.untagged_proverb.payload_forms` · env `WHKFORMS_OFF` · code `ContentConverter.#gatherProverb` + the split guard, `PageAssembler.#untaggedProverb` (second pass) · session 52 Round 3.
"""
F.finalise(
    N=530, old_build="260620.88", new_build="260620.89", entry=entry,
    config_comment="THE WHAKATAUKĪ'S OTHER WRITER FORMS (session 52 Round 3; KB 07B §7 — the merged lines, the payload forms). Env WHKFORMS_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 530 BASELINE (the whakataukī's other writer forms, `WHKFORMS_OFF`; "
        f"SCOPED, scoped #3 since the s51-r12 FULL): SCAFFOLD mean {MEAN}% / >=50% 1632 / >=75% 301 / >=90% 28 / RAW {RAW}% @ 2486 pairs "
        f"(+0.0074pp); cs exact 17005 / EXTRA 198 / missing 661; body ANY 234.**",
    og11="| `WHKFORMS_OFF` | 530 | **THE WHAKATAUKĪ'S OTHER WRITER FORMS** (session 52 Round 3). Reverts `callouts.by_tag.whakatauki.proverb_split_merged` "
         "(a merged proverb item stays whole — the writer's `[Whakatauki]` empty; the pipe split on every line) and "
         "`callouts.untagged_proverb.payload_forms` (a `[Body]` / `[Alert]` / `[Important]` proverb payload stays its tag) — the r529 output exactly. |",
    og14=f"- **Build:** `260620.89` (round 530 — **the whakataukī's other writer forms**; `WHKFORMS_OFF`; scoped #3 since the s51-r12 FULL; "
         f"18 modules; skeleton {MEAN} % (+0.0074pp), RAW {RAW} %, cs exact +19 / EXTRA −5 / missing −11).",
    gb_note=f"Round 530 (session 52 Round 3, 2026-09-26) — THE WHAKATAUKI'S OTHER WRITER FORMS (WHKFORMS_OFF): 18 modules; skeleton 56.2391 -> "
            f"{MEAN} (+0.0074pp), >=75 301; cs exact 17005 / EXTRA 198 / missing 661; every other gate held; scoped #3.",
    no_round=f"- **No round in flight** (26 Sept 2026 {T}, session 52 Round 3 — r530 (the whakataukī's other writer forms) SHIPPED and "
             "committed; the in-flight marker is cleared). LAST SHIPPED **r530** (260620.89); **LAST FULL = r526 (the session-51 Round 12 "
             "backstop)**; ledger **scoped #3** (5 of headroom). Ride-along patches (LOOP §3 step 1 reads this list at every PICK): "
             "`outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, 10 pages / "
             "9 modules — CEDK401, HIS1002, HPRE203, MXDI201, MXDI202 ×2, MXEX302, SSOG105, TWHA906, XGF9004) / "
             "`_r489_accbullet_declined.patch` (the accordion bulleted bold lead, 8 accordions / 4 modules — MXEX302, ENGS101, XGF9003, "
             "XLP05) / `_r463_declined.patch` (the WJFUN tile's \"Year N\" lead, 1 page) / `_r512_declined.patch` (the `[Activity: "
             "Embedded] <widget>` bracket, 10 modules — rides only after the TRR table-dialect ownership fix) / `_r524_declined.patch` "
             "(the callout + heading co-tag, 17 modules — rides only once an alert's run gathers the list after its title). Checked at "
             "r530: none rides — no patch has ALL its pages inside r530's 18 modules.",
    last_shipped=f"- LAST SHIPPED: **r530** (build 260620.89, 26 Sept {T}, session 52 Round 3 — THE WHAKATAUKĪ'S OTHER WRITER FORMS, "
                 "`WHKFORMS_OFF`; SCOPED, **scoped #3 since the s51-r12 FULL**; 18 modules; skeleton 56.2391 → "
                 f"{MEAN} % (+0.0074pp), ≥75 301, RAW {RAW} %; cs exact +19 / EXTRA −5 / missing −11; every other gate held).",
    before_them_add="r528 the untagged whakataukī",
    plateau="- Plateau window (§4): **1 of 3** — r530 +0.0074pp (< 0.02: counts); r529 +0.1122pp (a real gain: reset); ",
    standing="- Standing facts: AppVersion **260620.89** (r530 the whakataukī's other writer forms — session 52 Round 3, 26 Sept); before it "
             "260620.88 (",
    roundlog=f"- s52-r3 (engine r530, build 260620.89, 26 Sept 16:29 → {T}) · a PICK pass (the alert cue census after r529 — every family "
             "≤ 20 runs; the placement census fresh; the miner's one new row; the whakataukī residue, 23 runs in six shapes) then THE "
             "WHAKATAUKĪ'S OTHER WRITER FORMS (the merged-lines gather — the writer's `[Whakatauki]` no longer empty; the `[Body]` / "
             "`[Alert]` / `[Important]` proverb payload) · SHIPPED scoped #3 · 18 modules · skeleton **+0.0074pp**, ≥75 +1, cs exact +19 / "
             "EXTRA −5 / missing −11 · two dips NAMED (EXIP901_5_0 / FRNO902_0_0, position-free overlap up) · plateau 1 of 3.",
    archive_extra="- **What shipped (r530, 260620.89):** `ContentConverter.#gatherProverb` (merged lines, label line, the one-line pipe split) + "
                  "`PageAssembler.#untaggedProverb` second pass (payload forms, menu guard); data `callouts.by_tag.whakatauki.proverb_split_merged` "
                  "+ `callouts.untagged_proverb.payload_forms`; env renamed PROVSPLIT_OFF → **WHKFORMS_OFF** when the payload pass joined. Probe OFF "
                  "6,432 / 6,432 identical; ON 24 pages / 18 modules; +0.0074pp; every gate held.",
)
