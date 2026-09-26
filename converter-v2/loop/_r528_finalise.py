#!/usr/bin/env python3
"""ROUND 528 finalise (session 52 Round 1 — the untagged whakataukī, finished from the s51 stop). WSL. argv: MEAN RAW."""
import sys
import _s52_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-26 (round 528, build 260620.87) — THE UNTAGGED WHAKATAUKĪ: a free black reo paragraph (every word Māori-phonotactic, ≥ 4 words) followed by its English is the proverb + translation the writer typed without the `[Whakatauki]` tag, and renders as the `div.whakatauki` box (KB 07B §7; the gold boxes it 49 / 64 where its text survives); 53 modules, skeleton +0.0259pp, compare_structure missing −69

### 1. WHAT CHANGED

**The class** (session 51 Round 13, `_s51_r13_proverb.cjs` → `_s51_r13_provgold.py`; the s51-r13 cs MISSING census: `div.whakatauki` 111 elements / 59 pages / 55 modules): a proverb pair typed as two plain paragraphs — the reo line, then the English — ships as two free `<p>`s; the gold wraps the pair in `div.whakatauki` on 49 of 77 untagged pairs (0.64; 0.77 of the 64 whose text is in the gold; Inquiry 0.65 / Standard 0.63, 69 pages, no family > 6). KB 07B §7 names the whakatauki component.

**The fix** (`PageAssembler.#untaggedProverb`, after `#boldIdWidgetActivity`; data `callouts.untagged_proverb`, env **`UNTAGPROVERB_OFF`**): the reo item is re-typed as the `[Whakatauki]` tag with `reo | english` as its payload (the writer's one-line form — `split_payload_on_pipe` makes the two `<p>`s), so the existing proverb-only callout builds the box. Session 52 refined the s51 build (+0.0030pp, 25 up / 34 down) after triangulating its downs: (1) by emit time a later pass has merged the English with the paragraphs after it (PHE1005: 283 chars), so `#gatherProverb` read it as commentary and 15 of 63 boxes shipped reo-only — the pair is now handed over whole and the English item emptied (an "English" over `max_english_chars` is commentary and stays free); (2) a proverb right after an INTERACTIVE tag is that widget's content (ANZH301 / 302's `[interactive]` — the s51 build left an 'unbundled' red flag); (3) a line within `tagged_lookback` short lines of a writer-tagged whakatauki belongs to that box (ENGC204's four-line box was split in two); (4) a payload-free `owner_tags` callout whose whole content is the pair is REPLACED by the whakatauki (AGH1002 / CBI1004 / CEDT207 / CEDT301 / XDLS901's `[Important]` + proverb — the gold ships the whakatauki alone; the s51 build left 'Empty [important]' red flags), any other owned line stays with its callout; (5) the writer's bare label line (`Whakataukī`, `[Whakataukī]`, `Whakatauki:`) and an inline `Whakatauki:` prefix are dropped, as the gold drops them.

### 2. PROOF

- In-memory probe over all 545 modules: `UNTAGPROVERB_OFF=1` → 6,432 / 6,432 pages identical; ON → **59 pages / 53 modules**; 0 ASSEMBLE ERROR; 0 red-flag notes added. `_s45_regen.sh 528`: 53 + a 12-module spot-check sample regenerated, 0 stale, the sample byte-identical. `scoped_ship.sh … --round 528 --commit` PASS: containment 53 ⊆ 53.
- The skeleton gate's own `match()` (`_s51_prescore.py`, `_r528b_prescore.log`): **+0.0258pp, 30 up / 22 down** (PWY1001_0_0 +7.2, XMES102_0_0 +6.4, XTAS102_0_0 +5.0, …); the downs are the gold's own row placement — the box first in `#body` with no row (ENGC201), inline after the heading (CEDR203), HES1003's NCEA1 flow exclusion and its human-added English.

### 3. PROTECTED GATES

Skeleton **56.1010 → {MEAN} % @ 2486 (+0.0259pp)**, ≥50 1627 → 1628, ≥75 292 → 295, ≥90 28; RAW 39.844 → {RAW} %; compare_structure exact 16830 → 16867 (+37) / EXTRA 204 → 201 / missing 879 → 810 (−69); body_compare ANY 234 held; clean 98.40 %, leak 52 / 42 EXACT; tags 9557; every verifier ✓, every COUNT held (`_r528_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 528`; `--gate-baseline-check` PASS. Plateau: **reset** (+0.0259pp).

**Ledger:** scoped #1 since the s51-r12 FULL (r526) · data `callouts.untagged_proverb` · env `UNTAGPROVERB_OFF` · code `PageAssembler.#untaggedProverb` · session 51 Round 13 (built) / session 52 Round 1 (refined, shipped).
"""
F.finalise(
    N=528, old_build="260620.86", new_build="260620.87", entry=entry,
    config_comment="THE UNTAGGED WHAKATAUKĪ (session 51 Round 13 built / session 52 Round 1 shipped; KB 07B §7). Env UNTAGPROVERB_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 528 BASELINE (the untagged whakataukī, `UNTAGPROVERB_OFF`; "
        f"SCOPED, scoped #1 since the s51-r12 FULL): SCAFFOLD mean {MEAN}% / >=50% 1628 / >=75% 295 / >=90% 28 / RAW {RAW}% @ 2486 pairs "
        f"(+0.0259pp); cs exact 16867 / EXTRA 201 / missing 810; body ANY 234.**",
    og11="| `UNTAGPROVERB_OFF` | 528 | **THE UNTAGGED WHAKATAUKĪ** (session 52 Round 1). Reverts `callouts.untagged_proverb`: a free reo "
         "paragraph + its English stay two plain `<p>`s (the r526 output exactly). |",
    og14=f"- **Build:** `260620.87` (round 528 — **the untagged whakataukī**; `UNTAGPROVERB_OFF`; scoped #1 since the s51-r12 FULL; "
         f"53 modules; skeleton {MEAN} % (+0.0259pp), RAW {RAW} %, cs missing −69).",
    gb_note=f"Round 528 (session 52 Round 1, 2026-09-26) — THE UNTAGGED WHAKATAUKI (UNTAGPROVERB_OFF): 53 modules; skeleton 56.1010 -> "
            f"{MEAN} (+0.0259pp), >=50 1628, >=75 295; cs exact 16867 / EXTRA 201 / missing 810; every other gate held; scoped #1.",
    no_round=f"- **No round in flight** (26 Sept 2026 {T}, session 52 Round 1 — r528 (the untagged whakataukī) SHIPPED and committed; "
             "the in-flight marker is cleared). LAST SHIPPED **r528** (260620.87); **LAST FULL = r526 (the session-51 Round 12 "
             "backstop)**; ledger **scoped #1** (7 of headroom). Ride-along patches (LOOP §3 step 1 reads this list at every PICK): "
             "`outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, 10 pages / "
             "9 modules — CEDK401, HIS1002, HPRE203, MXDI201, MXDI202 ×2, MXEX302, SSOG105, TWHA906, XGF9004) / "
             "`_r489_accbullet_declined.patch` (the accordion bulleted bold lead, 8 accordions / 4 modules — MXEX302, ENGS101, XGF9003, "
             "XLP05) / `_r463_declined.patch` (the WJFUN tile's \"Year N\" lead, 1 page) / `_r512_declined.patch` (the `[Activity: "
             "Embedded] <widget>` bracket, 10 modules — rides only after the TRR table-dialect ownership fix) / `_r524_declined.patch` "
             "(the callout + heading co-tag, 17 modules — rides only once an alert's run gathers the list after its title). Checked at "
             "r528: none rides — no patch has ALL its pages inside r528's 53 modules (r469: ENGC403 in, ANZH301 / 302 out; r469b: 4 of 9 "
             "modules in; the rest 0).",
    last_shipped=f"- LAST SHIPPED: **r528** (build 260620.87, 26 Sept {T}, session 52 Round 1 — THE UNTAGGED WHAKATAUKĪ, "
                 "`UNTAGPROVERB_OFF`; SCOPED, **scoped #1 since the s51-r12 FULL**; 53 modules; skeleton 56.1010 → "
                 f"{MEAN} % (+0.0259pp), ≥50 1628, ≥75 295, RAW {RAW} %; cs exact +37 / EXTRA −3 / missing −69; every other gate held).",
    before_them_add="r525 the bold activity id after a widget tag",
    plateau="- Plateau window (§4): **0 of 3** — r528 +0.0259pp (a real gain: reset); ",
    standing="- Standing facts: AppVersion **260620.87** (r528 the untagged whakataukī — session 52 Round 1, 26 Sept); before it "
             "260620.86 (",
    roundlog=f"- s52-r1 (engine r528, build 260620.87, 26 Sept 15:12 → {T}) · FINISHED s51's toggled-OFF r528, THE UNTAGGED WHAKATAUKĪ "
             "(gold 49 / 64; KB 07B §7), refined on its triangulated downs (the merged English, the widget / callout owners, the tagged "
             "box's later lines, the label line) · SHIPPED scoped #1 · 53 modules · skeleton **+0.0259pp**, ≥50 +1, ≥75 +3, cs exact +37 / "
             "missing −69 · plateau reset (0 of 3).",
    archive_extra="- **What shipped (r528, 260620.87):** `PageAssembler.#untaggedProverb`; data `callouts.untagged_proverb`. Probe OFF "
                  "6,432 / 6,432 identical; ON 59 pages / 53 modules; +0.0259pp; cs missing −69; every other gate held.",
)
