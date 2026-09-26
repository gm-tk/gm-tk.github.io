#!/usr/bin/env python3
"""ROUND 523 finalise (session 51 Round 3 — the activity governs a heading co-tag + its duplicate-id guard + the owner look-back).
WSL. argv: MEAN RAW."""
import sys
import _s51_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-26 (round 523, build 260620.84) — THE ACTIVITY GOVERNS A HEADING CO-TAG: `[Activity 1A] [H3] Title` / `[H3] [Activity 2A] Title` (219 spans / 33 modules) opens the writer's numbered box with its title, where it shipped a bare heading — the gold boxes it 0.85; with a duplicate-id guard and the r521 walk-end reading the box owner's id; 36 modules, skeleton +0.1392pp, ≥50 +7

### 1. WHAT CHANGED

**The class** (`_s51_r3_unboxed.py` — 1,144 gold activity boxes on 597 pages that Claude renders wholly unboxed, diffuse by wording — then `_s51_r3_acthead.py` on its XGF9002 rows): the writer types the activity opener and the title's heading level in ONE red span, either order — `[Activity 1A] [H3] Examples of Factors` (HES1007), `[H3] [Activity 2A] Emotion patterns check-in` (XGF9002): **219 spans / 33 modules**. The heading tag is an ELEMENT (precedence 6) and outranked the activity's CONTAINER_OPEN (5), so no box opened, the title shipped as a bare `<h3>`, and the heading fragment's digit joined the ids (`["3","2b"]`). The gold puts that heading inside an activity box on **166 of 195** matched spans (0.85 — ARFUN 47/52, XGF 33/35, CEDO 26/31, HES 19/25, MXEX 13/18); Claude kept 105 free.

**The fix — three parts.**
- **(a) the co-tag** (`TagNormaliser.Parse`; data `Tag_Lexicon._meta.activity_heading_cotag`, env **`ACTHDCOTAG_OFF`** — `ACTHEAD_OFF` is an older ContentConverter toggle): when a span's tags are ONLY the activity tag + heading tags and a heading won the primary slot, the activity takes it (its black tail is the box's title, as for a plain `[Activity 1A] Title`) and each heading fragment's digit leaves `numbers`. A span that also carries a widget or any other tag is untouched.
- **(b) the duplicate-id guard** (`PageAssembler.#cotagDuplicateId`; `activity_heading_cotag.duplicate_id_guard`, same env): a promoted co-tag whose id opens ANOTHER activity later on the same page (before a PAGE_BOUNDARY) keeps its heading — the writer typed the id on a section heading AND on the real activity (MXEX202 lesson 2 `[Activity 2] [H3] Double or Half` … `[Activity 2] [H3] Fun Water Challenge`; HES1002 2.0); the gold boxes only the later one, and a box on the first shifted every later id through the r369 de-dupe. The first build's compare_structure loss fell 19 → 15 with it.
- **(c) the r521 walk-end reads the box owner** (`InteractiveScanner` member walk; data `member_rule.new_activity_id_terminates.owner_lookback`, env **`ACTIDOWNER_OFF`**): during the walk a widget bundle opened UNDER a separate `[Activity N]` opener has no activityId (the owner is attached later), so r521's "a new activity id ends the walk" never fired for it — ARFUN04 1G's drag-and-drop (its box newly opened by (a)) walked into `[Activity 1H drag and drop] [MTK Quiz …]` as a same-type continuation and swallowed the quiz (the mtkQuiz verifier went ✗: '1G: <ol> inside the shell'). The nearest activity opener before the bundle (≤ 60 items back, never past a PAGE_BOUNDARY or another widget opener) now lends its id. Measured with (a) OFF over all 545 modules: **0 pages differ** — (c) acts only where (a) opens a box.

### 2. PROOF

- In-memory probe over all 545 modules: `ACTHDCOTAG_OFF=1` → 6,432 / 6,432 pages identical (vs the r522 corpus); ON → **36 modules** (ANZH401, ARFUN04 / 05, CEDK501, CEDO501 / 502, CEDR501, CEDT501, CEDW501, ENGJ403, GEO1004, HES1002 / 1007, HIS1003, HPFUN402, MXEO401, MXEX201 / 202, MXFL201 / 202, PHE1003 / 1007 / 1008, SSOG301, TEFUN02 / 08, TWHR907, WJFUN106 / 110 / 115 / 208 / 212 / 304, XGF9002 / 9003 / 9006); `ACTIDOWNER_OFF=1` on the (a)+(b) corpus → 0 changed; 0 ASSEMBLE ERROR. `scoped_ship.sh … --round 523` PASS (three commits in the round — the first build, the duplicate guard, the owner look-back): 0 stale, containment 36 ⊆ 36, a re-planned 12-module spot-check byte-identical (the r521 sample held SSOG301, now affected).
- The skeleton gate's own `match()` on the ON pages (`_s51_prescore.py`, the first build): +0.1397pp, 51 up / 25 down (the largest rises CEDO501_2_1 +27.5, MXEX201_1_0 +23.6, CEDK501_5_1 +22.9, MXEX202_4_0 +21.7, HES1007_4_0 +19.9, MXEX202_6_0 +19.2, MXEX202_3_0 +16.8; the dips CEDT501_6_1 −15.4 — one box label 6E → 6D on a short page, difflib's re-anchoring; HES1002_2_0 −12.4 — fixed by (b); CEDK501_2_0 −10.8 — the box's widget walk runs to the next activity (see below); the rest ≤ 5).

### 3. PROTECTED GATES

Skeleton **55.8830 → {MEAN} % @ 2486 (+0.1392pp)**, ≥50 1618 → 1625, ≥75 288 → 289, ≥90 26; RAW 39.709 → {RAW} %; body_compare ANY 234 held; clean 98.40 %, leak 52 / 42 EXACT; tags 9557; every verifier ✓ (the mtkQuiz ✗ of the first build fixed by (c)), every COUNT held (`_r523_gates.log`). **compare_structure exact 16845 → 16830 (−15) NAMED** (`--accept-named`): compare_structure skips everything inside an activity box on both sides (`activity` is in its interactive-class list), so each loss is a Claude element that matched a FREE gold element and now sits in a box: CEDK501_2_0 ×4 (the heading "Sorting expenses" — the gold boxes it too, as 2A, and repeats it free lower down; plus three case-study paragraphs the box's widget walk now reaches — the gold keeps them free), CEDO501 ×4 (each lesson's closing "You've learned … move onto Lesson N" paragraph falls into the page's last box — the ordinary [Activity] auto-close, now on new boxes), MXEX201 ×3 (the "Symbols" section), ANZH401 / CEDR501 / ENGJ403 / WJFUN304 ×1. **Skeleton mean −0.00001pp NAMED** for (c) alone: ARFUN04_0_0 10.05 → 10.02 (the 1H quiz leaves the 1G drag-and-drop). Plateau: **reset** (+0.1392pp).

**Ledger:** scoped #3 since the s50-r14 FULL (r520) · data `Tag_Lexicon._meta.activity_heading_cotag` (+ `duplicate_id_guard`), `Interactive_Boundary_ChildTag_Bank._meta.member_rule.new_activity_id_terminates.owner_lookback` · env `ACTHDCOTAG_OFF`, `ACTIDOWNER_OFF` · code `TagNormaliser.Parse`, `PageAssembler.#cotagDuplicateId`, `InteractiveScanner` (the r521 walk-end) · session 51 Round 3.
"""
F.finalise(
    N=523, old_build="260620.83", new_build="260620.84", entry=entry,
    config_comment="THE ACTIVITY GOVERNS A HEADING CO-TAG (session 51 Round 3) + its duplicate-id guard + the r521 walk-end "
                   "reading the box owner's id. Env ACTHDCOTAG_OFF / ACTIDOWNER_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 523 BASELINE (the activity governs a heading co-tag, "
        f"`ACTHDCOTAG_OFF` / `ACTIDOWNER_OFF`; SCOPED, scoped #3 since the s50-r14 FULL): SCAFFOLD mean {MEAN}% / >=50% 1625 / >=75% 289 / "
        f">=90% 26 / RAW {RAW}% @ 2486 pairs (+0.1392pp); cs exact 16830 NAMED (−15); body ANY 234.**",
    og11="| `ACTHDCOTAG_OFF` | 523 | **THE ACTIVITY GOVERNS A HEADING CO-TAG** (session 51 Round 3). Reverts "
         "`Tag_Lexicon._meta.activity_heading_cotag` (+ its duplicate-id guard): `[Activity 1A] [H3] Title` / `[H3] [Activity 2A] Title` "
         "parse with the heading as primary again — no box, a bare heading (the r522 output exactly). |\n"
         "| `ACTIDOWNER_OFF` | 523 | **THE r521 WALK-END READS THE BOX OWNER'S ID** (session 51 Round 3, part c). Reverts "
         "`new_activity_id_terminates.owner_lookback`: a widget bundle under a separate [Activity N] opener tests no id during the walk "
         "(ARFUN04 1G swallows 1H's MTK quiz again under the co-tag). |",
    og14=f"- **Build:** `260620.84` (round 523 — **the activity governs a heading co-tag**; `ACTHDCOTAG_OFF` / `ACTIDOWNER_OFF`; scoped #3 "
         f"since the s50-r14 FULL; 36 modules; skeleton {MEAN} % (+0.1392pp), RAW {RAW} %; cs exact 16830 NAMED; body ANY 234).",
    gb_note=f"Round 523 (session 51 Round 3, 2026-09-26) — THE ACTIVITY GOVERNS A HEADING CO-TAG (ACTHDCOTAG_OFF) + the owner look-back "
            f"(ACTIDOWNER_OFF): 36 modules; skeleton 55.8830 -> {MEAN} (+0.1392pp), >=50 1625, >=75 289; cs exact 16830 (-15 NAMED: "
            f"elements now boxed that matched a free gold element); body ANY 234; scoped #3.",
    no_round=f"- **No round in flight** (26 Sept 2026 {T}, session 51 Round 3 — r523 (the activity governs a heading co-tag) SHIPPED and "
             "committed; the in-flight marker is cleared). LAST SHIPPED **r523** (260620.84); **LAST FULL = r520 (the session-50 Round 14 "
             "backstop)**; ledger **scoped #3** (5 of headroom). Ride-along patches (LOOP §3 step 1 reads this list at every PICK): "
             "`outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, 10 pages / 9 "
             "modules — CEDK401, HIS1002, HPRE203, MXDI201, MXDI202 ×2, MXEX302, SSOG105, TWHA906, XGF9004) / `_r489_accbullet_declined.patch` "
             "(the accordion bulleted bold lead, 8 accordions / 4 modules — MXEX302, ENGS101, XGF9003, XLP05) / `_r463_declined.patch` (the "
             "WJFUN tile's \"Year N\" lead, 1 page) / `_r512_declined.patch` (the `[Activity: Embedded] <widget>` bracket, 10 modules — rides "
             "only after the TRR table-dialect ownership fix). Checked at r523: none rides (r489's XGF9003 is inside the 36, its other three "
             "modules are not).",
    last_shipped=f"- LAST SHIPPED: **r523** (build 260620.84, 26 Sept {T}, session 51 Round 3 — THE ACTIVITY GOVERNS A HEADING CO-TAG + its "
                 "duplicate-id guard + the r521 walk-end reading the box owner, `ACTHDCOTAG_OFF` / `ACTIDOWNER_OFF`; SCOPED, **scoped #3 since "
                 "the s50-r14 FULL**; 36 modules; skeleton 55.8830 → "
                 f"{MEAN} % (+0.1392pp), ≥50 1625, ≥75 289, RAW {RAW} %, cs exact 16830 NAMED (−15); body ANY 234).",
    before_them_add="the journal instruction's own activity box + the AGH [Summary] alert + the r468 ride-along",
    plateau="- Plateau window (§4): **0 of 3** — r523 +0.1392pp (a real gain: reset); ",
    standing="- Standing facts: AppVersion **260620.84** (r523 the activity governs a heading co-tag — session 51 Round 3, 26 Sept); "
             "before it 260620.83 (",
    roundlog=f"- s51-r3 (engine r523, build 260620.84, 26 Sept 11:47 → {T}) · a PICK pass (`_s51_r3_unboxed.py`: 1,144 gold boxes Claude "
             "renders unboxed → `_s51_r3_acthead.py`: 219 activity + heading co-tags, gold boxes 0.85) then THE ACTIVITY GOVERNS A HEADING "
             "CO-TAG + a duplicate-id guard + the r521 walk-end reading the box owner (three repairs: cs −19 → −15, the mtkQuiz ✗ fixed) · "
             "SHIPPED scoped #3 · 36 modules · skeleton **+0.1392pp**, ≥50 +7, ≥75 +1, cs exact −15 NAMED · plateau reset (0 of 3).",
    archive_extra="- **What shipped (r523, 260620.84):** `TagNormaliser.Parse` (the co-tag), `PageAssembler.#cotagDuplicateId`, "
                  "`InteractiveScanner` (owner_lookback); data `activity_heading_cotag`, `new_activity_id_terminates.owner_lookback`. Probe "
                  "OFF 6,432 / 6,432 identical; ON 36 modules; +0.1392pp; cs exact −15 NAMED; mtkQuiz ✓.",
)
