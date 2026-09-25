#!/usr/bin/env python3
"""ROUND 515 finalise (session 50 Round 7 — KB c64: [Insert animated character] IS A CREATIVE SERVICES VIDEO, CSVIDEO_OFF). WSL."""
import sys
import _s50_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-26 (round 515, build 260620.77) — KB CONSTRAINT 64: `[Insert animated character]` IS A CREATIVE SERVICES VIDEO — the pending Vimeo `videoSection` scaffold + its Designer/Developer To Do, with the writer's `Animation Script` link folded into the To Do (74 modules, the BLL blended-literacy family; skeleton +0.0107pp)

### 1. WHAT CHANGED

**The rule** (KB constraint 64 / CL-0037; 05A "Creative Services Videos (Vimeo)" — authority level 1): *"Any video produced by Creative Services (a Te Kura in-house / Audiovisual production — e.g. an animated intro …) is embedded as a Vimeo `videoSection` scaffold with the video ID left pending, and is always accompanied by a visible `Designer/Developer To Do:` note"*; the scaffold emitted exactly as the design team supplies it (its two time-placeholder comments are the KB's narrow comment exception). KB §A row 64 was CAPTURED-INERT: round 233 declined it because the generic `[Audiovisual item N]` marker is mostly audio, and it pre-named "the day the writers' templates start marking a CS video explicitly".

**Found by** the widened recognition census (`_s50_r4_unresolved.cjs`): `[Insert animated character]` is the widest bracket that resolves to no tag — 73 tags in 73 modules (the BLL blended-literacy family), each followed by the writer's `__Animation Script__` link. Claude shipped a red Writers Note and the script link as student text (74 pages). `_s50_r7_animchar.py`: the gold page carries a Vimeo player at 53 of the 61 locatable tags (0.87) and hides the script link on 60 of 61.

**The fix** (`ContentConverter.#csVideoPrepass` + its render case; data `elements.cs_video_marker`; env `CSVIDEO_OFF`): the marker's red span (the writer's request in the same span rides along — "As this is a new Set, can we please have an animated man again …") becomes `Designer/Developer To Do: add vimeo embed for the animated character …` + the KB 64 scaffold (`src="https://player.vimeo.com/video/"`, no ID); a following `Animation Script` line joins the To Do as `(Animation Script: <link>)` instead of shipping as student text. The r200 house style still adds the series' `icon` class.

### 2. PROOF

- In-memory probe over all 545 modules: `CSVIDEO_OFF=1` → 0 pages changed; ON → **74 modules** (`outputs/_affected_r515.txt`). `scoped_ship.sh … --round 515` PASS outright (0 stale, containment 74 ⊆ 74, the 12-module spot-check byte-identical). On disk: 74 To Do + scaffold pairs; student-visible `Animation Script` links 74 → 5 (the five whose script line does not directly follow the marker — BLL240 / BLL225 / BLL226 … — recorded).

### 3. PROTECTED GATES

- **Skeleton 55.7384 → {MEAN} % @ 2486 (+0.0107pp)**, 52 up / 15 down (+26.6pp-sum; every dip ≤ 2.0pp — the gold's own Vimeo embed is a bare `div` with inline padding, KB 64's is `div.videoSection.ratio`, so the iframe line matches and the wrapper line does not: a NAMED KB form); ≥50 1612, **≥75 283 → 285** (BLL136_0_0 / BLL137_0_0 74.6 → 76.8), ≥90 26; RAW 39.546 → {RAW} %.
- compare_structure, body_compare, clean, leak EXACT; tags 9557; every verifier ✓, every COUNT held (`_r515_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 515`; `--gate-baseline-check` PASS. Plateau: neither (+0.0107pp, but ≥75 +2 — a protected bucket moved).

**Ledger:** scoped #2 since the r513 FULL · data `elements.cs_video_marker` · env `CSVIDEO_OFF` · code `ContentConverter.#csVideoPrepass` + the `csvideo` render case · tools `_s50_r7_animchar.py`, `_r515_finalise.py` · session 50 Round 7 (the in-flight marker was raised after the code edit — a procedural slip, recorded). KB status: §A row 64 → CAPTURED-LIVE for the explicit `[Insert animated character]` marker (the generic `[Audiovisual item N]` stays inert, r233).
"""
F.finalise(
    N=515, old_build="260620.76", new_build="260620.77", entry=entry,
    config_comment="KB c64 — [Insert animated character] IS A CREATIVE SERVICES VIDEO (session 50 Round 7): the pending Vimeo scaffold + "
                   "its To Do; the Animation Script link folds into the To Do. Env CSVIDEO_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 515 BASELINE (KB c64 the animated-character Vimeo scaffold, "
        f"`CSVIDEO_OFF`; SCOPED, scoped #2 since the r513 FULL): SCAFFOLD mean {MEAN}% / >=50% 1612 / >=75% 285 / >=90% 26 / RAW {RAW}% @ "
        f"2486 pairs (+0.0107pp, 52 up / 15 down); every other gate EXACT.**",
    og11="| `CSVIDEO_OFF` | 515 | **KB c64 — `[Insert animated character]` IS A CREATIVE SERVICES VIDEO** (session 50 Round 7). Reverts "
         "`elements.cs_video_marker`: the marker is a red Writers Note again and the `Animation Script` link ships as student text; "
         "byte-identical to r514. |",
    og14=f"- **Build:** `260620.77` (round 515 — **KB c64, the animated-character Vimeo scaffold**; `CSVIDEO_OFF`; scoped #2 since the r513 "
         f"FULL; 74 modules; skeleton {MEAN} % (+0.0107pp), ≥75 285).",
    gb_note=f"Round 515 (session 50 Round 7, 2026-09-26) — KB c64 THE ANIMATED-CHARACTER VIMEO SCAFFOLD (CSVIDEO_OFF): 74 modules; SCAFFOLD "
            f"55.7384 -> {MEAN} @ 2486 (+0.0107pp, 52 up / 15 down), >=75 283 -> 285, RAW 39.546 -> {RAW}; every other gate EXACT; scoped #2.",
    no_round=f"- **No round in flight** (26 Sept 2026 {T}, session 50 Round 7 — r515 (KB c64, the animated-character Vimeo scaffold) "
             "SHIPPED and committed; the in-flight marker is cleared). LAST SHIPPED **r515** (260620.77); **LAST FULL = r513 (the "
             "session-50 Round 5 backstop)**; ledger **scoped #2** (6 of headroom). Ride-along patches (LOOP §3 step 1 reads this list at "
             "every PICK): `outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, "
             "10 pages / 9 modules — CEDK401, HIS1002, HPRE203, MXDI201, MXDI202 ×2, MXEX302, SSOG105, TWHA906, XGF9004) / "
             "`_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages — CBI1008 L1 / L2, PES1004_8_0) / "
             "`_r489_accbullet_declined.patch` (the accordion bulleted bold lead, 8 accordions / 4 modules — MXEX302, ENGS101, XGF9003, "
             "XLP05) / `_r463_declined.patch` (the WJFUN tile's \"Year N\" lead, 1 page) / `_r512_declined.patch` (the `[Activity: "
             "Embedded] <widget>` bracket, 10 modules — rides only after the TRR table-dialect ownership fix). Checked at r515 (the BLL "
             "family): none rides.",
    last_shipped=f"- LAST SHIPPED: **r515** (build 260620.77, 26 Sept {T}, session 50 Round 7 — KB c64, `[Insert animated character]` IS A "
                 "CREATIVE SERVICES VIDEO, `CSVIDEO_OFF`; SCOPED, **scoped #2 since the r513 FULL**; 74 modules; the pending Vimeo "
                 f"scaffold + To Do; student-visible script links 74 → 5; skeleton 55.7384 → {MEAN} % (+0.0107pp), ≥75 +2; every other "
                 "gate EXACT).",
    before_them_add="the bare [hover] paren def",
    plateau="- Plateau window (§4): **0 of 3** — r515 +0.0107pp but ≥75 +2 (a protected bucket moved: neither); ",
    standing="- Standing facts: AppVersion **260620.77** (r515 KB c64 the animated-character Vimeo scaffold — session 50 Round 7, 26 Sept); "
             "before it 260620.76 (",
    roundlog=f"- s50-r7 (engine r515, build 260620.77, 26 Sept 03:03 → {T}) · KB c64: `[Insert animated character]` IS A CREATIVE SERVICES "
             "VIDEO (the pending Vimeo scaffold + To Do; the Animation Script link folded in) · SHIPPED scoped #2 · 74 modules · skeleton "
             "+0.0107pp, ≥75 +2 · plateau: neither (≥75 moved). Marker raised after the code edit (a slip).",
    archive_extra="- **What shipped (r515, 260620.77):** `elements.cs_video_marker` (CSVIDEO_OFF); `ContentConverter.#csVideoPrepass` + the "
                  "`csvideo` render case. Probe OFF 0; ON 74 modules; +0.0107pp.",
)
