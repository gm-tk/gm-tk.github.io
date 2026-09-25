#!/usr/bin/env python3
"""ROUND 513 finalise (session 50 Round 4 — THE BARE [hover] WITH ITS DEFINITION IN PARENTHESES, HOVERPAREN_OFF). WSL. argv: MEAN RAW."""
import sys
import _s50_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-26 (round 513, build 260620.75) — THE BARE `[hover]` WITH ITS DEFINITION IN PARENTHESES: `Hoa ako [hover] (learning partner) could find a class…` weaves the hover and keeps the writer's sentence, instead of sending the tag and the rest of the sentence into a red Writers Note (5 XDLS modules; the dips NAMED — the gold hovers only a term's first occurrences)

### 1. WHAT CHANGED

**Found by** a widened recognition census (`outputs/_s50_r4_unresolved.cjs`: every red bracket in every Writers Template that resolves to NO tag — 3,313 spans / 420 modules; a bare `[hover]` the largest, 152 spans / 26 modules). `_s50_r4_barehover.py` splits the bare `[hover]` by form: **P — `ANCHOR [hover] (DEF) rest…`, the definition in parentheses right after the tag, black — 48 spans / 5 modules (XDLS502 / 902 / 903 / 905 / 906, the learning-support family's idiom)**; R — the def inside the red span (186 — already form C of the weave, or flip-card "hover over" labels); O — the tag then an unbracketed sentence (68 — CEDK401; the gold has no consensus, 17 / 68).

**The defect:** `InteractiveScanner.#weaveHoverDefinition` (r82 → r500) found no definition in a CLOSED bare bracket and returned, so the tag became a red designer note that carried the rest of the writer's sentence with it — XDLS902's accordion panels ended at "You and your Hoa ako" and "(learning partner) could find a class or a book to follow…" rendered as a red `Writers Note:` line.

**The fix** (a new form (A5) in the weave; data `elements.hover_definition_inline.split_bracket.paren_def`; env `HOVERPAREN_OFF`): the parenthesised text right after a closed bare `[hover]` / `[rollover]` / `[mouseover]` is the definition; it weaves onto the preceding word like every other hover form (`<span class="infoTrigger" info="learning partner">ako</span>`), and the sentence continues after it (a continuation opening with punctuation joins with no space).

### 2. PROOF

- In-memory probe over all 545 modules: `HOVERPAREN_OFF=1` → 0 pages changed; ON → **exactly the 5 XDLS modules** (36 files). `scoped_ship.sh … --round 513` PASS (0 stale, containment 5 ⊆ 5, the 12-module spot-check byte-identical). The woven hovers: `restrictive eating` / "Only eating a limited number of foods.", `whakamana` / "Agency", `ako` / "learning partner"; the Writers Notes that carried the sentences are gone.

### 3. PROTECTED GATES

- **Skeleton 55.6992 → {MEAN} % @ 2486 (−0.0063pp), ≥50 1609 → 1607, ≥75 280 → 281**, ≥90 26, RAW {RAW} % — 16 movers, 8 up / 8 down, −15.6pp-sum. **NAMED (KB c14 — the writer's tag decides the component; §1b "Gates and KB overrides"):** the gold hovers only a term's FIRST occurrences — XDLS902's opening accordion carries `<span class="infoTrigger" info="learning partner">hoa ako</span>`, while its later activities (1A–1E) print "with your hoa ako and discuss…" plain, the writer's `[hover] (learning partner)` dropped by the developer. The writer tagged every occurrence, so every one is woven; those later paragraphs gain a `span.infoTrigger` the gold does not have — XDLS902_1_0 58.7 → 49.8, XDLS902_7_0 52.6 → 46.7 (the two ≥50 crossings), XDLS902_5_0 / _6_0 / _3_0, XDLS903_2_0, XDLS905_1_0, XDLS906_3_0 (each ≤ 3.3pp); XDLS905_4_0 +2.4 and six more rise, XDLS905_5_0 crosses ≥75. The module-level check (the gold's info = the writer's def on 45 of 48) confirmed the reading; the anchor is the weave's standing one word (`ako`; the gold's `hoa ako` — recorded).
- compare_structure, body_compare, clean, leak EXACT; tags 9557; every verifier ✓, every COUNT held (`_r513_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 513 --accept-named`; `--gate-baseline-check` PASS. Plateau: neither (a named KB-override dip).

**Ledger:** scoped #7 since the r505 FULL (a FULL backstop is due after the next scoped ship) · data `elements.hover_definition_inline.split_bracket.paren_def` · env `HOVERPAREN_OFF` · code `InteractiveScanner.#weaveHoverDefinition` (A5) · tools `_s50_r4_unresolved.cjs`, `_s50_r4_barehover.py`, `_r513_finalise.py` · session 50 Round 4.
"""
F.finalise(
    N=513, old_build="260620.74", new_build="260620.75", entry=entry,
    config_comment="THE BARE [hover] WITH ITS DEFINITION IN PARENTHESES (session 50 Round 4): the paren def weaves the hover and the "
                   "sentence stays in the paragraph. Env HOVERPAREN_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 513 BASELINE (the bare [hover] paren def, `HOVERPAREN_OFF`; "
        f"SCOPED, scoped #7 since the r505 FULL): SCAFFOLD mean {MEAN}% / >=50% 1607 / >=75% 281 / >=90% 26 / RAW {RAW}% @ 2486 pairs "
        f"(−0.0063pp NAMED: the gold hovers only a term's first occurrences, KB c14); every other gate EXACT.**",
    og11="| `HOVERPAREN_OFF` | 513 | **THE BARE `[hover]` WITH ITS DEFINITION IN PARENTHESES** (session 50 Round 4). Reverts "
         "`hover_definition_inline.split_bracket.paren_def`: `Hoa ako [hover] (learning partner) …` sends the tag and the rest of the "
         "sentence into a red Writers Note again; byte-identical to r511. |",
    og14=f"- **Build:** `260620.75` (round 513 — **the bare `[hover]` paren def**; `HOVERPAREN_OFF`; scoped #7 since the r505 FULL; 5 "
         f"XDLS modules; skeleton {MEAN} % (−0.0063pp NAMED), ≥50 1607, ≥75 281).",
    gb_note=f"Round 513 (session 50 Round 4, 2026-09-26) — THE BARE HOVER PAREN DEF (HOVERPAREN_OFF): 5 XDLS modules; SCAFFOLD 55.6992 -> "
            f"{MEAN} @ 2486 (-0.0063pp, 8 up / 8 down NAMED: the gold hovers only a term's first occurrences, the writer tagged every "
            f"one - KB c14), >=50 1609 -> 1607, >=75 280 -> 281; cs / body / clean / leak EXACT; scoped #7.",
    no_round=f"- **No round in flight** (26 Sept 2026 {T}, session 50 Round 4 — r513 (the bare `[hover]` paren def) SHIPPED and committed; "
             "the in-flight marker is cleared). LAST SHIPPED **r513** (260620.75); **LAST FULL = r505 (the session-49 Round 6 backstop)**; "
             "ledger **scoped #7** (1 of headroom — the NEXT round is the FULL backstop). Ride-along patches (LOOP §3 step 1 reads this list "
             "at every PICK): `outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` "
             "(buttons, 10 pages / 9 modules — CEDK401, HIS1002, HPRE203, MXDI201, MXDI202 ×2, MXEX302, SSOG105, TWHA906, XGF9004) / "
             "`_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages — CBI1008 L1 / L2, PES1004_8_0) / "
             "`_r489_accbullet_declined.patch` (the accordion bulleted bold lead, 8 accordions / 4 modules — MXEX302, ENGS101, XGF9003, "
             "XLP05) / `_r463_declined.patch` (the WJFUN tile's \"Year N\" lead, 1 page) / `_r512_declined.patch` (the `[Activity: "
             "Embedded] <widget>` bracket, 10 modules — rides only after the TRR table-dialect ownership fix). Checked at r513 (XDLS502 / "
             "902 / 903 / 905 / 906): none rides. A FULL backstop carries no ride-along (§2).",
    last_shipped=f"- LAST SHIPPED: **r513** (build 260620.75, 26 Sept {T}, session 50 Round 4 — THE BARE `[hover]` WITH ITS DEFINITION IN "
                 "PARENTHESES, `HOVERPAREN_OFF`; SCOPED, **scoped #7 since the r505 FULL**; 5 XDLS modules; the writer's sentences no longer "
                 f"go into a red Writers Note; skeleton 55.6992 → {MEAN} % (−0.0063pp NAMED — the gold hovers only first occurrences), "
                 "≥50 −2, ≥75 +1; every other gate EXACT).",
    before_them_add="the widget named after a generic interactive bracket",
    plateau="- Plateau window (§4): **0 of 3** — r513 a named KB-override dip (neither); ",
    standing="- Standing facts: AppVersion **260620.75** (r513 the bare [hover] paren def — session 50 Round 4, 26 Sept); before it "
             "260620.74 (",
    roundlog=f"- s50-r4 (engine r513, build 260620.75, 26 Sept ≈01:45 → {T}) · a PICK pass (the KB queue, the BLL2 ledger, the dragAndDrop "
             "button blocker, the widened recognition census) then THE BARE `[hover]` WITH ITS DEFINITION IN PARENTHESES (the sentence was "
             "going into a red Writers Note) · SHIPPED scoped #7 · 5 XDLS modules · skeleton −0.0063pp NAMED (the gold hovers first "
             "occurrences only), ≥50 −2, ≥75 +1 · plateau 0 of 3 (neither).",
    archive_extra="- **What shipped (r513, 260620.75):** `hover_definition_inline.split_bracket.paren_def` (HOVERPAREN_OFF); "
                  "`InteractiveScanner.#weaveHoverDefinition` (A5). Probe OFF 0; ON 5 modules; named dip.",
)
