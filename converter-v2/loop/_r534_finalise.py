#!/usr/bin/env python3
"""ROUND 534 finalise (session 52 Round 10 — the bare link line). WSL. argv: MEAN RAW."""
import sys
import _s52_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-26 (round 534, build 260620.93) — THE BARE LINK LINE IS THE DEVELOPER'S: a body paragraph that is nothing but a URL (neither a stock photo nor a video — a D2L / Te Kura page, a source site, a Google doc) becomes the house `Designer/Developer To Do: the writer's link — …` note; 195 modules / 300 pages, skeleton +0.0575pp, ≥50 +6, ≥75 +3

### 1. WHAT CHANGED

**The class** (r532 / r533's follow-up — `_s52_r10_d2lurl.py`, un-built hand-off boxes excluded by exact span): the remaining bare-URL paragraphs. D2L / Te Kura links: 138, the gold shows the link on the paired page 7 times (absent **0.95**); other hosts ≈ 355: absent 261 (**0.74**), an inline anchor on nearby prose 81 (which words — not derivable), a button 4. The gold ships 19 bare-URL paragraphs corpus-wide.

**The fix** (`ContentConverter.#bareLinkUrlNote`, a page post-pass after `#bareVideoUrlEmbed`; data `elements.bare_link_url_note` {{exclude_host_pattern, todo_text}}, env **`BARELINKNOTE_OFF`**): outside the un-built hand-off boxes, a `<p>` whose whole content is one URL not matched by r532 / r533 becomes the house To Do note (`NotesAndComments.redFlag`) — the learner sees no URL, the developer keeps the link (to anchor on text, make a button or credit in the acks). KB c5 (no writer residue in the output).

### 2. PROOF

- In-memory probe over all 545 modules: `BARELINKNOTE_OFF=1` → 6,432 / 6,432 pages identical; ON → **300 pages / 195 modules**, every changed line a bare-URL paragraph; 0 ASSEMBLE ERROR. `scoped_ship.sh … --round 534 --commit` PASS: 0 stale, containment 195 ⊆ 195, the 12-module spot-check byte-identical.
- The skeleton gate's own `match()` (`_s51_prescore.py`): **+0.0581pp, 217 up / 55 down** (COM1005_3_0 +9.5, DTC1004_4_0 +6.0 …; the dips: BLL251_1_0 −9.1 and ENGJ301_1_0 −6.4 — those golds carry the link as an anchor elsewhere on the page (position-free overlap 49 → 48, 48 → 47) — the rest ≤ 2.3); the buckets net ≥50 +6, ≥75 +3.

### 3. PROTECTED GATES

Skeleton **56.2768 → {MEAN} % @ 2486 (+0.0575pp)**, ≥50 1632 → 1638, ≥75 302 → 305, ≥90 28; RAW 39.948 → {RAW} %; compare_structure exact 17024 / EXTRA 198 / missing 661 held; body_compare ANY 233 held; clean 98.40 %, leak 52 / 42 EXACT; tags 9557; every verifier ✓, every COUNT held (`_r534_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 534`; `--gate-baseline-check` PASS. Plateau: **reset** (+0.0575pp).

**Ledger:** scoped #7 since the s51-r12 FULL (r526) — **the FULL backstop is due at the next ship (cadence 8)** · data `elements.bare_link_url_note` · env `BARELINKNOTE_OFF` · code `ContentConverter.#bareLinkUrlNote` · session 52 Round 10.
"""
F.finalise(
    N=534, old_build="260620.92", new_build="260620.93", entry=entry,
    config_comment="THE BARE LINK LINE IS THE DEVELOPER'S (session 52 Round 10; the To Do note in place of a bare URL). Env BARELINKNOTE_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 534 BASELINE (the bare link line, `BARELINKNOTE_OFF`; SCOPED, scoped #7 "
        f"since the s51-r12 FULL): SCAFFOLD mean {MEAN}% / >=50% 1638 / >=75% 305 / >=90% 28 / RAW {RAW}% @ 2486 pairs (+0.0575pp); cs exact 17024 / "
        f"EXTRA 198 / missing 661; body ANY 233.**",
    og11="| `BARELINKNOTE_OFF` | 534 | **THE BARE LINK LINE IS THE DEVELOPER'S** (session 52 Round 10). Reverts `elements.bare_link_url_note`: a body "
         "paragraph that is nothing but a (non-stock, non-video) URL ships as a visible link again (the r533 output exactly). |",
    og14=f"- **Build:** `260620.93` (round 534 — **the bare link line**; `BARELINKNOTE_OFF`; scoped #7 since the s51-r12 FULL; 195 modules / 300 pages; "
         f"skeleton {MEAN} % (+0.0575pp), RAW {RAW} %, ≥50 +6, ≥75 +3).",
    gb_note=f"Round 534 (session 52 Round 10, 2026-09-26) — THE BARE LINK LINE (BARELINKNOTE_OFF): 195 modules / 300 pages; skeleton 56.2768 -> {MEAN} "
            f"(+0.0575pp), >=50 1638, >=75 305; every other gate held; scoped #7 (the FULL backstop is due next).",
    no_round=f"- **No round in flight** (26 Sept 2026 {T}, session 52 Round 10 — r534 (the bare link line) SHIPPED and committed; the in-flight marker "
             "is cleared). LAST SHIPPED **r534** (260620.93); **LAST FULL = r526 (the session-51 Round 12 backstop)**; ledger **scoped #7** — **the "
             "FULL backstop is due next (cadence 8)**. Ride-along patches (LOOP §3 step 1 reads this list at every PICK): "
             "`outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, 10 pages / 9 modules — "
             "CEDK401, HIS1002, HPRE203, MXDI201, MXDI202 ×2, MXEX302, SSOG105, TWHA906, XGF9004) / `_r489_accbullet_declined.patch` (the accordion "
             "bulleted bold lead, 8 accordions / 4 modules — MXEX302, ENGS101, XGF9003, XLP05) / `_r463_declined.patch` (the WJFUN tile's \"Year N\" "
             "lead, 1 page) / `_r512_declined.patch` (the `[Activity: Embedded] <widget>` bracket, 10 modules — rides only after the TRR table-dialect "
             "ownership fix) / `_r524_declined.patch` (the callout + heading co-tag, 17 modules — rides only once an alert's run gathers the list "
             "after its title). Checked at r534: none rides.",
    last_shipped=f"- LAST SHIPPED: **r534** (build 260620.93, 26 Sept {T}, session 52 Round 10 — THE BARE LINK LINE IS THE DEVELOPER'S, `BARELINKNOTE_OFF`; "
                 "SCOPED, **scoped #7 since the s51-r12 FULL**; 195 modules / 300 pages; skeleton 56.2768 → "
                 f"{MEAN} % (+0.0575pp), ≥50 1638, ≥75 305, RAW {RAW} %; every other gate held).",
    before_them_add="r532 the bare stock-photo URL",
    plateau="- Plateau window (§4): **0 of 3** — r534 +0.0575pp (a real gain: reset); r533 +0.0063pp (counted); ",
    standing="- Standing facts: AppVersion **260620.93** (r534 the bare link line — session 52 Round 10, 26 Sept); before it 260620.92 (",
    roundlog=f"- s52-r10 (engine r534, build 260620.93, 26 Sept 18:37 → {T}) · THE BARE LINK LINE IS THE DEVELOPER'S (≈ 490 bare D2L / source / doc "
             "URL lines; the gold shows them 0.05 / 0.26 on the page) → the house To Do note · SHIPPED scoped #7 · 195 modules / 300 pages · "
             "skeleton **+0.0575pp**, ≥50 +6, ≥75 +3 · plateau reset (0 of 3); the FULL backstop is due next.",
    archive_extra="- **What shipped (r534, 260620.93):** `ContentConverter.#bareLinkUrlNote`; data `elements.bare_link_url_note`. Probe OFF 6,432 / 6,432 "
                  "identical; ON 300 pages / 195 modules; +0.0575pp; every gate held-or-improved.",
)
