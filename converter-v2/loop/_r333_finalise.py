#!/usr/bin/env python3
"""ROUND 333 — finalise: changelog, AppVersion (260619.03 → 260619.04), CLAUDE.md §9/§11/§14, gate_baseline.json,
LOOP_STATE.md (what shipped + position + round log + header), KB status D-row. Idempotent."""
import io, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)
SK_B, SK_A, RAW_B, RAW_A = "50.827", "50.893", "35.066", "35.119"

CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
ENTRY = f"""## 2026-09-15 (round 333, build 260619.04) — A RIGHT-HAND ALERT IS A SIDE COLUMN; `rhs` AND `summary` ARE NOT CLASSES (KB 05B "Alerts" + 01F/05B "Activity sidebar"; the autonomous loop, session 5, Round 4; **SCOPED regeneration of the 53 affected modules; skeleton +0.066pp / ≥50% +5, compare_structure exact +15 / EXTRA −15 / missing +2 NAMED, every other gate EXACT; scoped ship #7 since the round-326 full**)

### 1. WHAT CHANGED, IN ONE LINE

**The writer's positional and label words (`[alert box rhs]`, `[rhs alert]`, `[alert box rhc]`, `[important info box rhs]`, `[alert.rhs]`; `[alert box lesson summary]`) reached the page as the class tokens `rhs` and `summary` — which the gold ships 0 times and KB 05B does not define. A `summary` box is now the plain `alert` / `alert solid` (the gold 29/29); a right-hand box is a SIDE COLUMN paired as the right sibling of the content column it follows (the gold 56/70 = 0.80) — the KB's activity sidebar `alertActivity` after an activity box (15/20), an `alert top` after plain content (26/41).**

### 2. THE EVIDENCE (docx → human → Claude)

- **ANZH101 lesson 1** — WT `[rhs alert]` directly after activity 1B → gold `row > col-md-8 [activity 1B] + col-md-4 col-12 > alertActivity > p` → Claude before: `row > col-md-8 > alert rhs` in its own row under the activity's row; after: the activity's row un-closed and the alertActivity column spliced in as its right sibling (the r123 pairing).
- **XGF9006 lesson 2** — WT `[alert.rhs]` after prose → gold `col-md-8 paddingR [prose] + col-md-4 col-12 paddingL > alert top > p` → Claude before: a full-width `alert rhs` row; after: `col-md-8 [prose] + col-md-4 col-12 > alert top > p` (the gold's padding tokens are editorial and not chased).
- **ANZH404 lesson 1** — WT `[alert box lesson summary]` → gold `alert` → Claude before `alert summary`; after `alert`.
- **The KB:** 05B "Alerts" — `alert` / `alert solid` / `alert top` (`<h4>Heading</h4><p>Text</p>`) / `alert blank` / `alert teacher` / `alert cultural`; 01F + 05B "Activity sidebar" — `<div class="col-md-4 offset-md-0 col-12"><div class="alertActivity"><h4>Note</h4><p>Text</p></div></div>` beside the activity's `col-md-8`. No `rhs`, no `summary`.

### 3. THE MEASUREMENT (every paired Standard page; each Claude box matched to the gold by its first 8 words — `outputs/_measure_r333_alertmods.py`, `_alerttags.py`, `_rhsdisc.py`, `_rhscol.py`)

- Claude shipped **`alert rhs` 135 occ / 94 pages / 48 modules** (+ `alert solid rhs` 15, `alert solid top rhs` 1) and **`alert summary` / `alert solid summary` 63 + 35 occ / 62 pages / 11 modules**; gold non-KB alert tokens corpus-wide: padding0 29 / paddingL 10 / combined 9 / alertSolid 8 … — `rhs` 0, `summary` 0.
- `summary` (29 matched): gold plain `alert` 25 / `alert solid` 4 — the token is never there; the writer's spelling (`lesson summary` / `module summary` / `summary statement`) makes no difference.
- `rhs` (70 matched): the gold box's CLASS splits `alert top` 27 / `alertActivity` 23 / `alert` 20 (no form ≥ 0.60 alone) but its COLUMN solidifies — a side column (`col-md-4` / `col-4`) as the right sibling of a `col-md-8` on **56/70 = 0.80** (alertActivity 23/23, alert top 26/27, alert 7/20); the class follows what PRECEDES the box: **after an activity box → alertActivity 15/20 = 0.75; after plain content → alert top 26/41 = 0.63** (alertActivity 8, plain alert 7). Not discriminators: the writer's spelling (`[alert box rhc]` → alertActivity 5 / alert 2 / alert top 2), the subject (XGF9 alert 6 : top 7; MXFL 4 : 5 : 4), the box length, a heading lead. The `important` + rhs boxes (6 matched): alertActivity 4 / alert 1 / alert top 1 — never `alert solid` in a side column.
- The gold's inner wrap inside a side `alert top` is a near-tie (row>col-12 146 : direct 100 = 0.59 — below the floor) and the KB form is direct; inside `alertActivity` direct dominates (≈ 360 : 27) — both defs ship `wrap_content: false`.

### 4. THE FIX — one data block `callouts.positional_side_alert` `{{ enabled, env: "ALERTRHS_OFF", tags: [alert, important], keywords: [rhs, rhc], strip_tokens: {{rhs, rhc, summary}}, after_activity: {{alertActivity in col-md-4 offset-md-0 col-12, lead h4}}, after_content: {{alert top in col-md-4 col-12, lead h4}} }}`

- `ContentConverter` (the callout emit site): an `alert` / `important` whose leftover remainder words carry a keyword, in STRICT mode (no writer `[end alert]` ahead, no structured-content wrap), with the preceding content row just closed, is spliced as that row's right sibling through the r123 side-alert pairing — `after_activity` when the closed row's first block is an activity box (the lazy row-open now records `lastRowOpenIdx`), `after_content` otherwise; an EMPTY box (no ≤12-word lead, no black text, no unconsumed black run) keeps the ordinary path so its "Empty [alert]" flag survives; the leftover-word red flags ride inside the column. `#sideAlertCol` honours a def's `lead_element` (through the r61 module convention, as `#calloutOpen` does) so an embedded payload lead is never dropped — the `[side alert]` def has none and is byte-untouched. `#calloutOpen` strips the `strip_tokens` fragments from every callout's modifier string (the `summary` rule; the rhs fallback when no row precedes).
- Engine precedents the round reuses: r92/r94 (the TABLE-form positional alert → `col-md-4 > alert top` paired right, ENGS302), r121/r123 (`[Side alert]` → the paired `alertActivity` column), r239 (the exact spelling `[right-hand alert]` promoted to `side alert`; this wider family — 80 occ / 40 modules then — recorded as the follow-up).

### 5. THE PROOF AND THE GATES

- The in-memory probe over ALL 416 modules (`_r333_probe.cjs`, four shards): **OFF (`ALERTRHS_OFF=1`) = disk 2102/2102**; ON names **143 pages / 53 modules** and every differing line is one of: 150 `alert … rhs` opens gone, 98 `alert … summary` opens gone, 92 side columns gained (61 `col-md-4 col-12 > alert top`, 31 `col-md-4 offset-md-0 col-12 > alertActivity`), 106 plain `alert` / `alert solid` opens gained, and re-indented row/col/content lines that balance exactly (0 content lines lost or gained, `_r333_diffcheck.py`; the one clipped diff, MXFUN03_0_0, word-bag identical OFF vs ON). Scoped regeneration in the planner's 7 batches (`_r333_batches_run.sh`, all rc 0); `_content_manifest.py fresh --affected` → **0 truly stale**; `diff` = exactly the 143 pages, 0 added/removed.
- **Skeleton (PRIMARY): SCAFFOLD mean {SK_B}% → {SK_A}% (+0.066pp) IMPROVED / ≥50% 1044 → 1049 / ≥75% 200 / ≥90% 15 / skipped 0 @ 1954; RAW {RAW_B}% → {RAW_A}%.** 87 pages moved — **73 up / 14 down**, pp-sum +129 (HIS1004_4_0 +16.2, MXEO202_2_0 +15.4, ANZH301_8_0 +8.1, ANZH301_6_0 +7.4, MXFL301_2_0 +6.9, ANZH105_2_0 +6.2). The 14 dips NAMED (`_r333_bagcheck.py`, position-free overlap OFF → ON): TEFUN05_0_0 −4.9 / TEFUN04_0_0 −3.2 / ANZH304_6_0 −3.4 / ANZH303_6_0 −2.8 = the scorer's alignment artefact with the overlap RISING on each (197→198, 197→199, 73→74, 47→48); ANZH203_4_0 −1.6 overlap flat; MXFL301_1_0 −2.9 = one of its two rhs boxes is the gold's full-width `alert` (the after-content rule's 7/41 minority) and the other's gold column carries `offset-md-0 paddingL`; MXEX302_6_0 −1.5 = gold `alertActivity` after prose (the 8/41 minority); ENGI102_6_0 −1.1 = a box whose text the gold does not carry (the r176 coincidental-match class); six more under 0.5.
- **compare_structure exact 11360 → 11375 (+15) / EXTRA 186 → 171 (−15) IMPROVED / missing 591 → 593 (+2, accepted BY NAME via `--accept-named`):** ANZH301_3_0 "The MWWL is still going strong…" and HIS1004_2_0 "The learning in this lesson links to the FUNdamental…" — the after-activity rule's 2-of-20 minority, where the gold keeps a full-width `alert` and the comparator (whose CALLOUT_CLASSES has no `alertActivity`) reads the KB sidebar as no callout at all.
- Every other gate EXACT (`_r333_gates.log` line-for-line identical to r332 outside the skeleton block, plus rows-ratio 1.37 → 1.36 and ANZH303's over-nesting 6 → 5 IMPROVED): clean 2056/2102 / leak 288/46 · body 191 · tags 9557/9557 · flipCard TOTAL 61 divergence 0 · mtkQuiz 17 shells defect 0 · entry-parity PASS · index-sync 33/28 · **13 selftests GREEN**.
- **Verifier:** Claude `alert rhs` 150 → 0, `alert summary` 98 → 0; side columns 92 of the 150 rhs boxes (the other 58 = no closed content row directly before them, a span, or an empty box → the plain `alert`). **Ceiling:** SCAFFOLD {SK_A}% = **55.6% of achievable** (55.56).

### 6. NAMED, NOT CHASED

- The 13/70 rhs sites whose gold keeps a full-width plain `alert` (consensus-over-gold); the gold's editorial column padding on the alert-top sites (`paddingL` 13 / none 8 / `col-4` 6 / `offset-md-0` on some); the gold's inner `row > col-12` inside 59% of its side `alert top` boxes (below the floor; the KB form is direct); the writer instruction leads a plain path already ships as leads ("Can this be a bubble?", ENGI102 — pre-existing, rendered through the module's r61 lead convention either way).

**Ledger:** scoped ship #7 since the r326 full · data `callouts.positional_side_alert` · env `ALERTRHS_OFF` · tools `outputs/_measure_r333_alertmods.py`, `_measure_r333_alerttags.py`, `_measure_r333_rhsdisc.py`, `_measure_r333_rhscol.py`, `_r333_probe.cjs`, `_r333_diffcheck.py`, `_r333_bagcheck.py`, `_r333_finalise.py` · state `outputs/_r333_sk_final.json` (FRESH) · logs `_r333_gates.log`, `_r333_sk_full.log`, `_r333_fastloop.log`, `_r333_fastloop_commit.log`, `_r333_selftests.log`, `_r333_probe_off_0*.log`, `_r333_probe_on1_0*.log` (the first cut — its 10 lost "Empty" flags and the h4-vs-convention lead were the two fixes), `_r333_probe_on2_0*.log`, `_r333_probe_on.log`, `_r333_probe_offsave.log`, `_r333_regen.log`, `_r333_fresh.log`, `_r333_affected.txt`, `_r333_batches_run.sh`, `_r333_off_pages/` (the dip check).

"""
if "round 333, build 260619.04" not in s:
    assert s.startswith(head); s = head + ENTRY + s[len(head):]; wr(CL, s); print("changelog prepended")

CF = os.path.join(PF, "app", "js", "Config.js"); c = rd(CF)
OLD = '\tstatic AppVersion = "260619.03";\n'
NEW = ('\t// ROUND 333 (2026-09-15, build 260619.04): a right-hand alert is a side column; rhs and summary are\n'
       '\t// not classes (KB 05B) — the writer\'s [alert box rhs] / [rhs alert] family pairs as the right sibling of\n'
       '\t// the content column it follows (alertActivity after an activity box, alert top after prose), and\n'
       '\t// [alert box lesson summary] ships the plain alert; scoped regeneration of 53 modules; env ALERTRHS_OFF.\n'
       '\tstatic AppVersion = "260619.04";\n')
if '"260619.04"' not in c:
    assert c.count(OLD) == 1; c = c.replace(OLD, NEW, 1); wr(CF, c); print("AppVersion bumped")

CM = os.path.join(PF, "CLAUDE.md"); m = rd(CM)
OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 332 BASELINE (the empty footer → the KB's page-position form + the BLL1 footer class; scoped 130 modules)"
NEW9 = (f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 333 BASELINE (a right-hand alert is a side column; rhs / summary are not classes — KB 05B; scoped 53 modules): SCAFFOLD mean {SK_A}% / >=50% 1049 / >=75% 200 / >=90% 15 / skipped 0 @ 1954; RAW {RAW_A}%** (state `outputs/_r333_sk_final.json`, FRESH). r333 +0.066 (87 moved, 73 up; the 14 dips NAMED = the scorer's alignment artefact with position-free overlap rising (TEFUN05/04, ANZH304_6, ANZH303_6), the after-content rule's gold-plain-alert / gold-alertActivity minorities (MXFL301_1, MXEX302_6), a coincidental match (ENGI102_6)); compare_structure missing +2 ACCEPTED BY NAME (ANZH301_3_0, HIS1004_2_0 — the after-activity rule's gold-plain-alert minority). Older r332 text: **ROUND 332 BASELINE (the empty footer → the KB's page-position form + the BLL1 footer class; scoped 130 modules)")
if "ROUND 333 BASELINE" not in m:
    assert m.count(OLD9) == 1, "§9"; m = m.replace(OLD9, NEW9, 1); print("§9")
ROW = ("| `ALERTRHS_OFF` | 333 | **A RIGHT-HAND ALERT IS A SIDE COLUMN; `rhs` AND `summary` ARE NOT CLASSES** (KB 05B \"Alerts\" + 01F/05B \"Activity sidebar\"; the autonomous loop's session-5 Round 4; **SCOPED regeneration of the 53 affected modules; scoped ship #7 since the r326 full**). Reverts byte-for-byte (the tokens ship again, no routing). ON (default), `callouts.positional_side_alert`: at the callout emit site an `alert` / `important` whose leftover remainder words carry `rhs` / `rhc`, in STRICT mode, with the preceding content row just closed, is spliced as that row's right sibling through the r123 side-alert pairing — the KB activity sidebar `col-md-4 offset-md-0 col-12 > alertActivity` when the closed row's first block is an activity box, `col-md-4 col-12 > alert top` otherwise (both with an h4 lead through the r61 module convention; an EMPTY box keeps the ordinary path and its \"Empty [alert]\" flag); with no preceding content row, or in span mode, the plain box ships with the token stripped; `summary` is stripped everywhere (→ `alert` / `alert solid`). MEASURED (every paired Standard page, each box matched by its first 8 words): `summary` → gold plain `alert` 25 / `alert solid` 4 (29/29); `rhs` → a side column beside a col-md-8 on 56/70 = 0.80, `alertActivity` after an activity 15/20, `alert top` after prose 26/41; spelling / subject / length are not discriminators. Claude `alert rhs` 150 → 0, `alert summary` 98 → 0; 92 side columns. 143 pages / 53 modules changed. Skeleton +0.066pp (≥50% +5; 73 up / 14 down, dips named); compare_structure exact +15 / EXTRA −15 / missing +2 NAMED (ANZH301_3_0, HIS1004_2_0 — gold keeps a full-width alert after the activity); every other gate EXACT; 13 selftests GREEN. |\n")
if "| `ALERTRHS_OFF` | 333 |" not in m:
    A = "| `FOOTERPOS_OFF` | 332 |"; assert m.count(A) == 1, "§11"; m = m.replace(A, ROW + A, 1); print("§11")
B14 = (f"- **Build:** `260619.04` (round 333 — **a right-hand alert is a side column; `rhs` / `summary` are not classes** (KB 05B; the autonomous loop's session-5 Round 4; **SCOPED regeneration of 53 modules; scoped ship #7 since the r326 full — the full-ship backstop is DUE at 8**). **ROUND 333 BASELINE: SCAFFOLD mean {SK_A}% / ≥50% 1049 / ≥75% 200 / ≥90% 15 / skipped 0 @ 1954; RAW {RAW_A}%** (state `outputs/_r333_sk_final.json`, FRESH) = **55.6% of achievable** (ceiling 91.6%). compare_structure exact **11375** (+15) / EXTRA **171** (−15) / missing **593** (+2 NAMED — ANZH301_3_0, HIS1004_2_0); every other gate EXACT: clean **2056/2102** / leak **288/46** · body **191** · tags **9557/9557** · flipCard TOTAL 61 divergence 0 · index-sync 33/28 · entry-parity PASS · mtkQuiz shell defect 0 · all THIRTEEN selftests GREEN. Corpus 2102 pages / 413 modules, 0-stale, **143 pages / 53 modules changed, 0 added/removed**; toggle `ALERTRHS_OFF`; data `callouts.positional_side_alert`. `alert rhs` 150 → 0, `alert summary` 98 → 0, 92 side columns paired. **Plateau window: r331 +0.022 · r332 +0.269 · r333 +0.066.**)\n")
if "- **Build:** `260619.04` (round 333" not in m:
    A = "- **Build:** `260619.03` (round 332 —"; assert m.count(A) == 1, "§14"; m = m.replace(A, B14 + A, 1); print("§14")
wr(CM, m)

GB = os.path.join(HERE, "..", "reference", "tests", "gate_baseline.json"); raw = rd(GB); d = json.loads(raw)
d["_meta"]["build"] = "260619.04"; d["_meta"]["round"] = 333; d["_meta"]["date"] = "2026-09-15"
d["skeleton"].update({"mean_scaffold_pct": float(SK_A), "raw_mean_pct": float(RAW_A), "pages_ge_50": 1049, "pages_ge_75": 200})
for k in ("compare_structure", "structure"):
    if k in d and isinstance(d[k], dict):
        for kk, vv in (("exact_chain", 11375), ("exact", 11375), ("claude_extra_container", 171), ("extra", 171), ("claude_missing_container", 593), ("missing", 593)):
            if kk in d[k]: d[k][kk] = vv
d["_meta"]["_round333_note"] = f"Round 333 (a right-hand alert is a side column; rhs / summary are not classes — KB 05B; scoped 53-module regeneration, scoped ship #7 since the r326 full). Skeleton {SK_B}->{SK_A} (+0.066pp; 87 moved, 73 up; >=50 1044->1049, >=75 200, >=90 15); compare_structure exact 11360->11375, EXTRA 186->171, missing 591->593 (NAMED: ANZH301_3_0, HIS1004_2_0 — the after-activity rule's gold-plain-alert minority); every other gate EXACT; 13 selftests GREEN."
wr(GB, json.dumps(d, ensure_ascii=False) + ("\n" if raw.endswith("\n") else "")); print("gate_baseline.json refreshed")

KB = os.path.join(HERE, "..", "..", "KB_AMALGAMATION_STATUS.md"); k = rd(KB)
anchor = "| ~~—~~ | 01B \"Footer and Acknowledgements\""
row = ("| ~~—~~ | 05B \"Alerts\" vocabulary + 01F/05B \"Activity sidebar\" — `rhs` / `summary` are not classes; a right-hand alert is a side column (`alertActivity` beside an activity, `alert top` beside prose) | **SHIPPED round 333** (`alert rhs` 150 → 0, `alert summary` 98 → 0; 92 side columns paired; 143 pages / 53 modules) | 143 pages | +0.066pp / ≥50 +5 | `ALERTRHS_OFF` | CAPTURED-LIVE |\n")
if "05B \"Alerts\" vocabulary" not in k:
    assert k.count(anchor) == 1; k = k.replace(anchor, row + anchor, 1); wr(KB, k); print("KB status D-row")

LS = os.path.join(HERE, "..", "..", "LOOP_STATE.md"); s = rd(LS); nl = "\r\n" if "\r\n" in s[:3000] else "\n"
def L(t): return t.replace("\n", nl)
SEC = L(f"""## Session 5 · Round 4 (engine r333) — what shipped (a right-hand alert is a side column; `rhs` / `summary` are not classes)
- **Fix:** `callouts.positional_side_alert` {{enabled, env ALERTRHS_OFF, tags [alert, important], keywords [rhs, rhc], strip_tokens
  {{rhs, rhc, summary}}, after_activity (the KB activity sidebar `col-md-4 offset-md-0 col-12 > alertActivity`, lead h4), after_content
  (`col-md-4 col-12 > alert top`, lead h4)}}: at the callout emit site a strict-mode `alert`/`important` carrying a keyword, with the preceding
  content row just closed, is spliced as that row's right sibling through the r123 pairing (`#sideAlertCol`, which now honours a def's
  lead through the r61 module convention); an empty box keeps the ordinary path and its "Empty" flag; with no preceding row or in span
  mode the plain box ships with the token stripped; `summary` is stripped everywhere. `emit` records `lastRowOpenIdx` so the closed row's
  first block (activity vs content) decides the def.
- **Regeneration:** scoped — the in-memory probe over ALL 416 modules (4 shards): OFF = disk 2102/2102; ON named 143 pages / 53 modules;
  every diff line = 150 rhs opens + 98 summary opens gone, 92 side columns (61 alert top / 31 alertActivity) + 106 plain alerts gained,
  content lines balancing exactly (0 lost / 0 gained); the planner's 7 batches, all rc 0; 0 truly stale; manifest diff = exactly the 143.
  The first cut lost 10 "Empty [alert]" flags and rendered the lead as a fixed h4 — both fixed before the regeneration (`_r333_probe_on1_*`).
- **Gates:** skeleton {SK_B} → {SK_A} (+0.066pp; 87 moved, 73 up / 14 down — dips NAMED: TEFUN05_0_0 −4.9 / TEFUN04_0_0 −3.2 / ANZH304_6_0
  −3.4 / ANZH303_6_0 −2.8 = alignment artefacts with the position-free overlap rising; MXFL301_1_0 −2.9 + MXEX302_6_0 −1.5 = the
  after-content rule's gold-plain-alert / gold-alertActivity minorities; ENGI102_6_0 −1.1 a coincidental match); ≥50 1044 → 1049; ≥75 200;
  compare_structure exact 11360 → 11375 / EXTRA 186 → 171 / missing 591 → 593 (ACCEPTED BY NAME: ANZH301_3_0 + HIS1004_2_0, the
  after-activity rule's 2-of-20 minority where the gold keeps a full-width `alert`); every other gate EXACT; 13 selftests GREEN.
  **55.6% of achievable.**
- **Verifier:** `alert rhs` 150 → 0; `alert summary` 98 → 0; 92 side columns. **Plateau window: r331 +0.022 · r332 +0.269 · r333 +0.066.**
  Ship ledger: scoped #7 since the r326 full — **the full-ship backstop is due at the next scoped ship (8).**

""")
ANCHOR = "## Session 5 · Round 4 PICK (engine r333)"
if "## Session 5 · Round 4 (engine r333) — what shipped" not in s:
    assert s.count(ANCHOR) == 1; s = s.replace(ANCHOR, SEC + ANCHOR, 1); print("LOOP_STATE section")
OLD_P = "- Session 5 Round 3 (engine r332 — the empty footer → the KB's page-position form, KB 01B; + the BLL1 registry footer class): SHIPPED 2026-09-15 ≈17:40 (session 5). AppVersion 260619.03, CLAUDE.md §9/§11/§14, KB status D-row added, scoped ship #6 since the r326 full. Skeleton +0.269pp, ≥50 +10, ≥75 +4."
NEW_P = OLD_P + nl + "- Session 5 Round 4 (engine r333 — a right-hand alert is a side column; rhs / summary are not classes, KB 05B): SHIPPED 2026-09-15 ≈18:30 (session 5). AppVersion 260619.04, CLAUDE.md §9/§11/§14, KB status D-row added, scoped ship #7 since the r326 full (backstop due at 8). Skeleton +0.066pp, ≥50 +5; compare_structure exact +15 / EXTRA −15 / missing +2 named."
if "- Session 5 Round 4 (engine r333" not in s:
    assert s.count(OLD_P) == 1, "position"; s = s.replace(OLD_P, NEW_P, 1); print("position")
OLD_R = "- s5-r3 (engine r332) · the empty footer"
i = s.find(OLD_R); assert i > 0; j = s.find(nl, i) + len(nl)
NEW_R = "- s5-r4 (engine r333) · a right-hand alert is a side column; rhs / summary are not classes (KB 05B: `[alert box rhs]`-family boxes pair as the right sibling of the content column they follow — the KB activity sidebar alertActivity after an activity box, alert top after prose; `[alert box lesson summary]` → the plain alert) · SHIPPED 2026-09-15 · scoped regeneration, 143 pages / 53 modules · scaffold 50.827→50.893 (+0.066; 73 up / 14 down, dips named), ≥50 +5, compare_structure exact +15 / EXTRA −15 / missing +2 NAMED, every other gate EXACT · alert rhs 150→0, alert summary 98→0, 92 side columns · 55.6% of achievable · commit (see git log)" + nl
if "- s5-r4 (engine r333)" not in s:
    s = s[:j] + NEW_R + s[j:]; print("round log")
old_h = "· r332 (the empty footers, scoped 130 modules, +0.269pp) · SHIPPED ≈17:40.**"
new_h = "· r332 (the empty footers, scoped 130 modules, +0.269pp; commit 8a347d4) · r333 (the right-hand alert side column + the summary token, scoped 53 modules, +0.066pp) · SHIPPED ≈18:30.**"
if old_h in s: s = s.replace(old_h, new_h, 1); print("header")
wr(LS, s); print("LOOP_STATE.md written")
