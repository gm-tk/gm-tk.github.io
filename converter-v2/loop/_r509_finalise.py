#!/usr/bin/env python3
"""ROUND 509 finalise (session 49 Round 10 — KB 10 §5 the empty lesson menu's red flag, EMPTYMENUFLAG_OFF). WSL. argv: MEAN RAW."""
import sys
import _s49_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-25 (round 509, build 260620.72) — KB 10 §5 THE EMPTY LESSON MENU'S RED FLAG: a lesson page whose Writers Template gives no learning intentions now tells the designer to supply the lesson-menu copy, instead of shipping a silent blank menu (412 pages / 95 modules; gate-neutral by design)

### 1. WHAT CHANGED

**The rule** (KB `10_CORPUS_VALIDATED_SCAFFOLDING.md` §5 l.63 — authority level 1): *"When the source has no such wording and no reference supplies it, you cannot invent it: build the empty `#module-menu-content` shell the skeleton requires and raise a visible red flag telling the designer the lesson-menu copy needs to be supplied."* D13-8 overrode that rule for its twelve repeater modules ONLY (their lesson menus copy the overview's). **Measured** (`outputs/_s49_r10_emptymenu.cjs`, the r508 corpus): **427 pages / 108 modules** shipped a menu with no text and no flag — MXFL 30, PWY 27, CHI 23, COM 23, MXDI 22, ANZH 20, FRFUN 19, HPRE 19, MXEX 19, MXFU 18 … (the empty MX menus r502 left bare among them — the D15 session's follow-up (c)).

**The fix** (`SkeletonBuilder.#buildHeader`; data `menu.empty_lesson_menu_flag`; env `EMPTYMENUFLAG_OFF`): a LESSON page whose `simplified` / `simplified_bare` menu holds no text gets the designer To Do — "Designer/Developer To Do: Lesson menu: the Writers Template has no learning intentions / success criteria for this lesson — supply the lesson-menu copy (KB 10 §5)." The engine's existing note placement puts it at the top of `#body` (notes never ride inside the header), where the designer sees it first.

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 0 pages changed**; ON **412 pages / 95 modules** — every change the one added To Do line (the 15 other empty-menu pages of the census are overview-named / non-simplified shells). Regenerated = ON byte-for-byte (848 / 848, 11 batches, 4 workers); `scoped_ship.sh` PASS (0 stale, containment 95 ⊆ 95, the 12-module spot-check byte-identical).

### 3. PROTECTED GATES

- **Gate-neutral by design** (the skeleton, compare_structure and the defect audit exclude the `cv2-note` family, r72): skeleton {MEAN} % @ 2486 EXACT (0 movers), ≥50 1602, ≥75 277, ≥90 26, RAW {RAW} %; cs EXACT; clean / leak EXACT; **body_compare ANY 232 → 230, over-capture 59 → 57 — an ARTEFACT, named**: body_compare counts a free-standing note's characters in the page's free body, so two over-capture pages fall under its 0.40 threshold; nothing was un-captured. Every verifier ✓, every COUNT held (`_r509_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 509`; `--gate-baseline-check` PASS. Plateau: neither (gate-neutral by design).

**Ledger:** scoped #4 since the r505 FULL · data `menu.empty_lesson_menu_flag` · env `EMPTYMENUFLAG_OFF` · code `SkeletonBuilder.#buildHeader` · tools `_s49_r10_emptymenu.cjs`, `_s49_regen_par.sh`, `_r509_finalise.py` · session 49 Round 10.
"""
F.finalise(
    N=509, old_build="260620.71", new_build="260620.72", entry=entry,
    config_comment="KB 10 §5 THE EMPTY LESSON MENU'S RED FLAG (session 49 Round 10): an empty lesson menu carries the designer To Do. "
                   "Env EMPTYMENUFLAG_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 509 BASELINE (KB 10 §5 the empty lesson menu's red flag, "
        f"`EMPTYMENUFLAG_OFF`; SCOPED, scoped #4 since the r505 FULL; gate-neutral by design): SCAFFOLD mean {MEAN}% / >=50% 1602 / >=75% "
        f"277 / >=90% 26 / RAW {RAW}% @ 2486 pairs — EXACT; body ANY 230 (−2, an artefact: the note's characters join the free body).**",
    og11="| `EMPTYMENUFLAG_OFF` | 509 | **KB 10 §5 — THE EMPTY LESSON MENU'S RED FLAG** (session 49 Round 10). Reverts "
         "`menu.empty_lesson_menu_flag`: a lesson page whose menu has no source text ships the silent blank menu again; byte-identical "
         "to r508. |",
    og14=f"- **Build:** `260620.72` (round 509 — **KB 10 §5, the empty lesson menu's red flag**; `EMPTYMENUFLAG_OFF`; scoped #4 since the "
         f"r505 FULL; 412 pages / 95 modules; skeleton {MEAN} % EXACT).",
    gb_note=f"Round 509 (session 49 Round 10, 2026-09-25) — KB 10 SECTION 5 THE EMPTY LESSON MENU'S RED FLAG (EMPTYMENUFLAG_OFF): 412 "
            f"pages / 95 modules gain the designer To Do; gate-neutral (cv2-note excluded); body ANY 232 -> 230 / over_capture 59 -> 57 "
            f"is an ARTEFACT (the note's characters join the free body); scoped #4.",
    no_round=f"- **No round in flight** (25 Sept 2026 {T}, session 49 Round 10 — r509 (KB 10 §5 the empty lesson menu's red flag) SHIPPED "
             "and committed; the in-flight marker is cleared). LAST SHIPPED **r509** (260620.72); **LAST FULL = r505 (the session-49 "
             "Round 6 backstop)**; ledger **scoped #4** (4 of headroom). Ride-along patches (LOOP §3 step 1 reads this list at every "
             "PICK): `outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, 10 "
             "pages) / `_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages — checked at r509: 2 of its 3 pages (CBI1008 L1 / L2) "
             "are in r509's set, PES1004_8_0 is not — not all inside, so it does not ride along; when it lands those two menus gain the "
             "writer's own WALT text and lose r509's flag) / `_r489_accbullet_declined.patch` "
             "(the accordion bulleted bold lead, 8 accordions / 4 modules) / `_r463_declined.patch` (the WJFUN tile's \"Year N\" lead, 1 page).",
    last_shipped=f"- LAST SHIPPED: **r509** (build 260620.72, 25 Sept {T}, session 49 Round 10 — KB 10 §5 THE EMPTY LESSON MENU'S RED "
                 "FLAG, `EMPTYMENUFLAG_OFF`; SCOPED, **scoped #4 since the r505 FULL**; 412 pages / 95 modules gain the designer To Do; "
                 f"gate-neutral: skeleton {MEAN} % EXACT; body ANY −2 an artefact, named).",
    before_them_add="D15-19 the yellow-✅ multiChoiceQuiz",
    plateau="- Plateau window (§4): **0 of 3** — r509 gate-neutral by design (neither); ",
    standing="- Standing facts: AppVersion **260620.72** (r509 KB 10 §5 the empty lesson menu's red flag — session 49 Round 10, 25 Sept); "
             "before it 260620.71 (",
    roundlog=f"- s49-r10 (engine r509, build 260620.72, 25 Sept 21:27 → {T}) · a PICK pass (the miner's chrome rows dispositioned) then "
             "KB 10 §5 THE EMPTY LESSON MENU'S RED FLAG (427 pages had a silent blank menu) · SHIPPED scoped #4 · 412 pages / 95 modules · "
             "gate-neutral (body ANY −2 an artefact, named) · plateau 0 of 3 (neither).",
    archive_extra="- **What shipped (r509, 260620.72):** `menu.empty_lesson_menu_flag` (env `EMPTYMENUFLAG_OFF`), `SkeletonBuilder.#buildHeader`. "
                  "Probe OFF 0; ON 412 pages / 95 modules; gate-neutral.",
)
