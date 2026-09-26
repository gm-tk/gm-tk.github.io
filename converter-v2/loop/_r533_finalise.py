#!/usr/bin/env python3
"""ROUND 533 finalise (session 52 Round 9 — the bare video URL). WSL. argv: MEAN RAW."""
import sys
import _s52_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-26 (round 533, build 260620.92) — THE BARE VIDEO URL IS THE EMBED: a body paragraph that is nothing but a YouTube / Vimeo URL becomes the `videoSection` embed (KB 01E; the gold embeds that video on the page 0.86), or goes when the page already embeds it; 62 modules / 82 pages, skeleton +0.0063pp, compare_structure exact +19

### 1. WHAT CHANGED

**The class** (r532's follow-up — `_s52_r9_videourl.py`, un-built hand-off boxes excluded by exact span): 134 bare YouTube / Vimeo URL paragraphs with a video id — a writer's video line under a `[video]` whose own line held the title, in an activity, after an instruction; the gold EMBEDS that video on the paired page for **115 (0.86)** — 92 where Claude has no embed, 23 where Claude already embeds it (a duplicate line). r340's seam A (a url-only `[link]` line → the embed, gold 0.90) on every such line.

**The fix** (`ContentConverter.#bareVideoUrlEmbed`, a page post-pass beside `#bareStockUrlImage`; data `elements.bare_video_url_embed` {{host_pattern}}, env **`VIDEOURLEMBED_OFF`**): outside the un-built hand-off boxes the paragraph becomes `video.youtube` (the group's host convention) or `video.generic_iframe` with Vimeo's player URL; the page's icon pass adds `icon`; when the page already embeds that video the line is dropped.

### 2. PROOF

- In-memory probe over all 545 modules: `VIDEOURLEMBED_OFF=1` → 6,432 / 6,432 pages identical; ON → **82 pages / 62 modules**; 0 ASSEMBLE ERROR. The first `scoped_ship.sh … --round 533` FAILED on skeleton ≥50 −2; the corpus was restored (`VIDEOURLEMBED_OFF=1 _s45_regen.sh 533` → `_content_manifest.py diff` 0 pages), the two movers measured, the ON state regenerated and shipped with `--accept-named "pages >=50%"`: PASS, 0 stale, containment 62 ⊆ 62, the 12-module spot-check byte-identical.
- The skeleton gate's own `match()` (`_s51_prescore.py`): **+0.0064pp, 29 up / 13 down**. **The two NAMED movers across the 50 line** (`_s52_companion.py`): **HIS1008_6_0 54.71 → 44.38** — the change is exactly the gold's embed; position-free overlap 123 → **124** / 164 while the aligned matches fall 90 → 73 (difflib re-anchors on a 165-line page): the alignment artefact; **MXS1004_0_0 50.57 → 48.84** — the writer's YouTube Short, which the developer dropped from the gold entirely (overlap 25 → 24): the KB 01E form against a developer deletion, a NAMED override (the rule's 14 % minority — no discriminator: Shorts split 1 : 1).

### 3. PROTECTED GATES

Skeleton **56.2705 → {MEAN} % @ 2486 (+0.0063pp)**, ≥50 1634 → 1632 (−2, NAMED above), ≥75 301 → 302, ≥90 28; RAW 39.947 → {RAW} %; compare_structure exact 17005 → 17024 (+19) / EXTRA 198 / missing 661 held; body_compare ANY 233 held; clean 98.40 %, leak 52 / 42 EXACT; tags 9557; every verifier ✓, every COUNT held (`_r533_gates.log`); `--gate-baseline-check` PASS. Plateau: **1 of 3** (+0.0063pp < 0.02).

**Ledger:** scoped #6 since the s51-r12 FULL (r526) · data `elements.bare_video_url_embed` · env `VIDEOURLEMBED_OFF` · code `ContentConverter.#bareVideoUrlEmbed` · session 52 Round 9.
"""
F.finalise(
    N=533, old_build="260620.91", new_build="260620.92", entry=entry,
    config_comment="THE BARE VIDEO URL IS THE EMBED (session 52 Round 9; KB 01E). Env VIDEOURLEMBED_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 533 BASELINE (the bare video URL, `VIDEOURLEMBED_OFF`; SCOPED, scoped #6 "
        f"since the s51-r12 FULL): SCAFFOLD mean {MEAN}% / >=50% 1632 (−2 NAMED) / >=75% 302 / >=90% 28 / RAW {RAW}% @ 2486 pairs (+0.0063pp); "
        f"cs exact 17024 / EXTRA 198 / missing 661; body ANY 233.**",
    og11="| `VIDEOURLEMBED_OFF` | 533 | **THE BARE VIDEO URL IS THE EMBED** (session 52 Round 9). Reverts `elements.bare_video_url_embed`: a body paragraph "
         "that is nothing but a YouTube / Vimeo URL ships as a visible link again (the r532 output exactly). |",
    og14=f"- **Build:** `260620.92` (round 533 — **the bare video URL**; `VIDEOURLEMBED_OFF`; scoped #6 since the s51-r12 FULL; 62 modules / 82 pages; "
         f"skeleton {MEAN} % (+0.0063pp), RAW {RAW} %, cs exact +19; ≥50 −2 NAMED).",
    gb_note=f"Round 533 (session 52 Round 9, 2026-09-26) — THE BARE VIDEO URL (VIDEOURLEMBED_OFF): 62 modules / 82 pages; skeleton 56.2705 -> {MEAN} "
            f"(+0.0063pp), >=50 1632 (-2 NAMED: HIS1008_6_0 alignment, MXS1004_0_0 the gold drops the writer's Short), >=75 302; cs exact 17024; scoped #6.",
    no_round=f"- **No round in flight** (26 Sept 2026 {T}, session 52 Round 9 — r533 (the bare video URL) SHIPPED and committed; the in-flight marker "
             "is cleared). LAST SHIPPED **r533** (260620.92); **LAST FULL = r526 (the session-51 Round 12 backstop)**; ledger **scoped #6** (2 of "
             "headroom — a FULL backstop is due at scoped #8). Ride-along patches (LOOP §3 step 1 reads this list at every PICK): "
             "`outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, 10 pages / 9 modules — "
             "CEDK401, HIS1002, HPRE203, MXDI201, MXDI202 ×2, MXEX302, SSOG105, TWHA906, XGF9004) / `_r489_accbullet_declined.patch` (the accordion "
             "bulleted bold lead, 8 accordions / 4 modules — MXEX302, ENGS101, XGF9003, XLP05) / `_r463_declined.patch` (the WJFUN tile's \"Year N\" "
             "lead, 1 page) / `_r512_declined.patch` (the `[Activity: Embedded] <widget>` bracket, 10 modules — rides only after the TRR table-dialect "
             "ownership fix) / `_r524_declined.patch` (the callout + heading co-tag, 17 modules — rides only once an alert's run gathers the list "
             "after its title). Checked at r533: none rides.",
    last_shipped=f"- LAST SHIPPED: **r533** (build 260620.92, 26 Sept {T}, session 52 Round 9 — THE BARE VIDEO URL IS THE EMBED, `VIDEOURLEMBED_OFF`; "
                 "SCOPED, **scoped #6 since the s51-r12 FULL**; 62 modules / 82 pages; skeleton 56.2705 → "
                 f"{MEAN} % (+0.0063pp), ≥75 302, cs exact +19, RAW {RAW} %; ≥50 −2 NAMED (HIS1008_6_0 alignment, MXS1004_0_0 a developer deletion)).",
    before_them_add="r531 the bracket fragment in a button label",
    plateau="- Plateau window (§4): **1 of 3** — r533 +0.0063pp (< 0.02: counts); r532 +0.0240pp (a real gain: reset); ",
    standing="- Standing facts: AppVersion **260620.92** (r533 the bare video URL — session 52 Round 9, 26 Sept); before it 260620.91 (",
    roundlog=f"- s52-r9 (engine r533, build 260620.92, 26 Sept 18:10 → {T}) · THE BARE VIDEO URL IS THE EMBED (134 bare YouTube / Vimeo lines; the "
             "gold embeds that video on the page 0.86; KB 01E, r340's seam A extended) · SHIPPED scoped #6 (the first ship FAILED on ≥50 −2 — "
             "restored, measured: HIS1008_6_0 alignment, MXS1004_0_0 a developer deletion — shipped NAMED) · 62 modules / 82 pages · skeleton "
             "**+0.0063pp**, ≥75 +1, cs exact +19 · plateau 1 of 3.",
    archive_extra="- **What shipped (r533, 260620.92):** `ContentConverter.#bareVideoUrlEmbed`; data `elements.bare_video_url_embed`. Probe OFF 6,432 / "
                  "6,432 identical; ON 82 pages / 62 modules; +0.0063pp; ≥50 −2 NAMED; every other gate held-or-improved.",
)
