#!/usr/bin/env python3
"""ROUND 532 finalise (session 52 Round 8 — the bare stock-photo URL). WSL. argv: MEAN RAW."""
import sys
import _s52_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-26 (round 532, build 260620.91) — THE BARE STOCK-PHOTO URL IS AN IMAGE REFERENCE: a body paragraph that is nothing but a stock-photo URL (`<p><a href="https://www.istockphoto.com/…">https://www.istockphoto.com/…</a></p>`) no longer ships as visible learner text — it becomes the house `Designer/Developer To Do: image goes here (iStock-N). Link: …` note, or goes when the page already shows that image; 107 modules / 140 pages, skeleton +0.0240pp

### 1. WHAT CHANGED

**The class** (found from the BLL scoped miner's #110 `activity EXTRA p>a`, 43 pages / 40 modules): `_s52_r8_bareurl.py` (un-built hand-off boxes excluded by exact span) — Claude ships ≈ 353 stock-photo URL paragraphs on ≈ 160 pages (+ ≈ 140 video, 137 D2L, ≈ 360 other-host bare URLs) where the gold has 19 bare-URL paragraphs in all. Their WT forms are diffuse (`_s52_r8_urlcue.py`: a URL-only line after a description, a second / third URL after an `[image]` whose own line held the first — ARFUN04's `[insert item #17: images]` + two more lines — an unknown bracket's payload, a URL splitting a writer's note), but `_s52_r8_stockimg.py` shows the gold displays that very image on the paired page for 205 of 325 with an id (0.63), elsewhere in the module for 40 more. MediaBuilder's standing contract: the pasted iStock URL is the asset reference, never visible text.

**The fix** (`ContentConverter.#bareStockUrlImage`, a page post-pass beside `#summaryHeadingAlert`; data `elements.bare_stock_url_image` {{mode, todo_text, host_pattern, id_patterns}}, env **`STOCKURLIMG_OFF`**): outside the un-built hand-off boxes (the developer's raw copy stays), a `<p>` whose whole content is one stock-photo URL becomes the house To Do note (`NotesAndComments.redFlag`, the Media List item note's wording) — dropped instead when the page already shows that image. Three forms were measured (`mode`): the in-place placeholder `<img>` **+0.0078pp (96 up / 30 down)** — the gold places these pictures in side columns and widgets, not at the URL's line, so an in-place image misaligns even where the gold shows it on that page (CEDO / CEDK / OSAI: img 3.26pp-sum vs note 12.53); drop and the To Do note both **+0.0241pp (106 up / 19 down)** — the note keeps the image as the developer's cue and sits outside the skeleton. Not taken (recorded): video URLs (should be embeds), D2L links, other hosts.

### 2. PROOF

- In-memory probe over all 545 modules: `STOCKURLIMG_OFF=1` → 6,432 / 6,432 pages identical; ON → **140 pages / 107 modules**, every changed line a bare stock URL (XGF9006_7_0: the URL between the two halves of a writer's note — dropped, the halves rejoin); 0 ASSEMBLE ERROR. `scoped_ship.sh … --round 532 --commit` PASS: 0 stale, containment 107 ⊆ 107, the 12-module spot-check byte-identical.
- The skeleton gate's own `match()` (`_s51_prescore.py`): **+0.0241pp, 106 up / 19 down** (the dips: BLL137_1_0 −10.2 / BLL114_1_0 −5.4 — a URL line that anchored the alignment, DTC1004_5_0 −2.2, the rest ≤ 1.2).

### 3. PROTECTED GATES

Skeleton **56.2465 → {MEAN} % @ 2486 (+0.0240pp)**, ≥50 1632 → 1634, ≥75 301, ≥90 28; RAW 39.943 → {RAW} %; compare_structure exact 17005 / EXTRA 198 / missing 661 held; body_compare ANY 234 → 233; clean 98.40 %, leak 52 / 42 EXACT; tags 9557; every verifier ✓, every COUNT held (`_r532_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 532`; `--gate-baseline-check` PASS. Plateau: **reset** (+0.0240pp ≥ 0.02).

**Ledger:** scoped #5 since the s51-r12 FULL (r526) · data `elements.bare_stock_url_image` · env `STOCKURLIMG_OFF` · code `ContentConverter.#bareStockUrlImage` · session 52 Round 8.
"""
F.finalise(
    N=532, old_build="260620.90", new_build="260620.91", entry=entry,
    config_comment="THE BARE STOCK-PHOTO URL IS AN IMAGE REFERENCE (session 52 Round 8; the To Do note in place of the visible URL). Env STOCKURLIMG_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 532 BASELINE (the bare stock-photo URL, `STOCKURLIMG_OFF`; SCOPED, "
        f"scoped #5 since the s51-r12 FULL): SCAFFOLD mean {MEAN}% / >=50% 1634 / >=75% 301 / >=90% 28 / RAW {RAW}% @ 2486 pairs (+0.0240pp); "
        f"cs exact 17005 / EXTRA 198 / missing 661; body ANY 233.**",
    og11="| `STOCKURLIMG_OFF` | 532 | **THE BARE STOCK-PHOTO URL IS AN IMAGE REFERENCE** (session 52 Round 8). Reverts `elements.bare_stock_url_image`: a "
         "body paragraph that is nothing but a stock-photo URL ships as a visible link again (the r531 output exactly). |",
    og14=f"- **Build:** `260620.91` (round 532 — **the bare stock-photo URL**; `STOCKURLIMG_OFF`; scoped #5 since the s51-r12 FULL; 107 modules / "
         f"140 pages; skeleton {MEAN} % (+0.0240pp), RAW {RAW} %, ≥50 +2).",
    gb_note=f"Round 532 (session 52 Round 8, 2026-09-26) — THE BARE STOCK-PHOTO URL (STOCKURLIMG_OFF): 107 modules / 140 pages; skeleton 56.2465 -> "
            f"{MEAN} (+0.0240pp), >=50 1634; body ANY 233; every other gate held; scoped #5.",
    no_round=f"- **No round in flight** (26 Sept 2026 {T}, session 52 Round 8 — r532 (the bare stock-photo URL) SHIPPED and committed; the "
             "in-flight marker is cleared). LAST SHIPPED **r532** (260620.91); **LAST FULL = r526 (the session-51 Round 12 backstop)**; ledger "
             "**scoped #5** (3 of headroom). Ride-along patches (LOOP §3 step 1 reads this list at every PICK): `outputs/_r469_declined.patch` "
             "(alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, 10 pages / 9 modules — CEDK401, HIS1002, HPRE203, "
             "MXDI201, MXDI202 ×2, MXEX302, SSOG105, TWHA906, XGF9004) / `_r489_accbullet_declined.patch` (the accordion bulleted bold lead, 8 "
             "accordions / 4 modules — MXEX302, ENGS101, XGF9003, XLP05) / `_r463_declined.patch` (the WJFUN tile's \"Year N\" lead, 1 page) / "
             "`_r512_declined.patch` (the `[Activity: Embedded] <widget>` bracket, 10 modules — rides only after the TRR table-dialect ownership "
             "fix) / `_r524_declined.patch` (the callout + heading co-tag, 17 modules — rides only once an alert's run gathers the list after its "
             "title). Checked at r532: none rides — no patch has ALL its pages inside r532's 107 modules with its own class in scope.",
    last_shipped=f"- LAST SHIPPED: **r532** (build 260620.91, 26 Sept {T}, session 52 Round 8 — THE BARE STOCK-PHOTO URL IS AN IMAGE REFERENCE, "
                 "`STOCKURLIMG_OFF`; SCOPED, **scoped #5 since the s51-r12 FULL**; 107 modules / 140 pages; skeleton 56.2465 → "
                 f"{MEAN} % (+0.0240pp), ≥50 1634, body ANY 233, RAW {RAW} %; every other gate held).",
    before_them_add="r530 the whakataukī's other writer forms",
    plateau="- Plateau window (§4): **0 of 3** — r532 +0.0240pp (a real gain: reset); ",
    standing="- Standing facts: AppVersion **260620.91** (r532 the bare stock-photo URL — session 52 Round 8, 26 Sept); before it 260620.90 (",
    roundlog=f"- s52-r8 (engine r532, build 260620.91, 26 Sept 17:36 → {T}) · a PICK pass (the KB queue §D, the heading-level rows, the BLL "
             "scoped miner's #110) then THE BARE STOCK-PHOTO URL IS AN IMAGE REFERENCE (353 URL-only paragraphs; the gold shows the image "
             "0.63 on the page; the To Do note beat the in-place <img> 3×) · SHIPPED scoped #5 · 107 modules / 140 pages · skeleton "
             "**+0.0240pp**, ≥50 +2, body ANY −1 · plateau reset (0 of 3).",
    archive_extra="- **What shipped (r532, 260620.91):** `ContentConverter.#bareStockUrlImage`; data `elements.bare_stock_url_image` (mode todo). "
                  "Probe OFF 6,432 / 6,432 identical; ON 140 pages / 107 modules; +0.0240pp; every gate held.",
)
