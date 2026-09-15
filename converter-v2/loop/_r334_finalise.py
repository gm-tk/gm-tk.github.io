#!/usr/bin/env python3
"""ROUND 334 — finalise: changelog, AppVersion (260619.04 → 260619.05), CLAUDE.md §9/§11/§14, gate_baseline.json,
LOOP_STATE.md (what shipped + position + round log + header), KB status D-row. Idempotent."""
import io, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)
SK_B, SK_A, RAW_B, RAW_A = "50.893", "51.060", "35.119", "35.243"

CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
ENTRY = f"""## 2026-09-15 (round 334, build 260619.05) — THE ACTIVITY BOX'S TITLE HEADING IS h3 (KB 01F `activity_heading`; the autonomous loop, session 5, Round 5; **SCOPED regeneration of the 73 affected modules; skeleton +0.167pp / ≥50% +17, every other gate EXACT; scoped ship #8 since the round-326 full — the full-ship backstop is now DUE**)

### 1. WHAT CHANGED, IN ONE LINE

**A writer's `[H3]` typed after the `[Activity]` opener took the body shift (+1 → h4; `[H4]` → h5) and `#relevelHeadings` skips activity subtrees, so the box's own title never normalised back — Claude shipped it at h4/h5 on 590 boxes (465 h4 + 125 h5, incl. the 115 XDLS tile panels) while the gold ships h3 at 0.997 / 0.995 / 1.000 per template and the KB's `activity_heading` form is `<h3>`. A post-pass now pins the box's first-child heading to h3.**

### 2. THE EVIDENCE (docx → human → Claude)

- **MXFL203 lesson 1, activity 1E** — WT `[Activity 1E]` then `[H3] New Zealand's biggest A&P show` → gold `<div class="activity" number="1E"><div class="row"><div class="col-12"><h3>New Zealand's biggest A&P show</h3>` → Claude before: the same box with `<h4>`; after: `<h3>`.
- **HIS1005 lesson 2** — the same shape (writer `[H3]` in the box, gold h3, Claude h4); **XDLS904 lesson 1** — the r307 tile-grid panels (`activity dropbox`, gold `<h3>Learn some moves with your whānau</h3>`) shipped h5 titles; after: h3.
- **The KB:** 01F "Activities" — `activity_heading` → `<h3>Activity heading text</h3>` within activity.

### 3. THE MEASUREMENT (`outputs/_measure_r334_acttitle.py` → `_r334_acttitle.json`; the class was surfaced by the new substitution instrument `_measure_r334_subst.py` → `_r334_subst.json`, the gate's own `replace` opcodes read line-for-line — Standard `h3 ⇐ h4` 209 occ / 142 pages / 66 modules)

- Wherever an activity box's first child is a heading the gold ships h3 on **4548 : 12** Standard (0.997), **1029 : 5** Inquiry (0.995), **581 : 0** Fundamentals (1.000), 196 : 4 Bilingual. Claude shipped h4 on 456 boxes + h5 on 10 in the plain form — 202 pages / 69 modules — plus h5 on 115 XDLS tile panels the census only saw once the r307 class prefix was accounted for; 590 headings in all.
- The r66 first-line title and the opener's embedded payload already shipped at the fixed h3 (3359 boxes); only the writer's explicit `[H3]`/`[H4]` inside the box carried the shift.
- Set aside on the record from the same instrument (`LOOP_STATE.md` Declined): the widened activity wrapper (KB c17/c56 — gold `col-md-8` is the majority for every widget type, D&D column 0.51), `iframe.embed-responsive-item` (the KB's iframe forms are class-less), `videoSection.icon` (r200/r331), the in-box SUB-heading level (gold `h3 → h4` 655 vs Claude `h3 → h3` 657 — a second class, not this round), and the CED revision-brief modules (a content-start finding — LOOP_STATE Blocked).

### 4. THE FIX — one data block `activity_wrapper.title_heading_level` `{{ enabled, env: "ACTTITLEH3_OFF", level: 3, exclude_body_class_match: "reoTranslate", skip_panel_class: "super-content row" }}`

- `ActivitiesBuilder.activityTitleLevelPostpass(html, run)`, run in the body chain right after `#relevelHeadings` (before `#promoteNamedHeadings` / the interactive and dropbox post-passes / `#cdTilePair`): for every activity box open it skips an optional super-content panel (balanced), and when the box's own `row > col-12` opens with a heading, that heading's open + close tags are rewritten to h3. Nothing else in the box moves; the reoTranslate family is excluded (its boxes are BilingualBuilder's, under the r330/r331 rules — PNR keeps h2 by name).

### 5. THE PROOF AND THE GATES

- The in-memory probe over ALL 416 modules (`_r334_probe.cjs`, four shards): **OFF (`ACTTITLEH3_OFF=1`) = disk 2102/2102**; ON names **226 pages / 73 modules** and every differing line is a heading tag swap — 465 `<h4>` + 125 `<h5>` → 590 `<h3>`, nothing else. Scoped regeneration in the planner's 9 batches (`_r334_batches_run.sh`, all rc 0); `_content_manifest.py fresh --affected` → **0 truly stale**; `diff` = exactly the 226 pages, 0 added/removed.
- **Skeleton (PRIMARY): SCAFFOLD mean {SK_B}% → {SK_A}% (+0.167pp) IMPROVED / ≥50% 1049 → 1066 / ≥75% 200 / ≥90% 15 / skipped 0 @ 1954; RAW {RAW_B}% → {RAW_A}%.** 170 pages moved — **150 up / 20 down**, pp-sum +326 (MXFUN01_3_0 +15.5, ANZH104_4_0 +12.2, MXFL203_2_0 +11.9, HIS1007_2_0 +11.5, ANZH301_4_0 +10.0; by module MXFL203 +33.5, HIS1007 +25.2, HIS1004 +20.2, ANZH104 +19.8, MXEX302 +19.1). The 20 dips NAMED (`_r334_bagcheck.py`, position-free overlap OFF → ON): MXFU401_3_0 −8.4 / PHE1003_1_0 −4.6 / MXEO202_6_0 −4.6 / MXEO202_3_0 −3.3 / HIS1007_3_1 −3.2 / TEFUN08_0_0 −2.9 = the scorer's alignment artefact with the overlap RISING or flat on each (95→96, 53→54, 61→62, 46→47, 91→93, 327→327); ANZH301_9_0 −3.5 and ANZH304_6_0 −3.4 = one box each whose gold title is not h3 (the gold's 12-of-4560 minority; overlap −1); twelve more under 2.6.
- Every other gate EXACT (`_fastloop_diff.py` PASS with nothing to name; full suite `_r334_gates.log` line-for-line identical to r333 outside the skeleton block): cs exact 11375 / EXTRA 171 / missing 593 · clean 2056/2102 / leak 288/46 · body 191 · tags 9557/9557 · flipCard TOTAL 61 divergence 0 · mtkQuiz 17 shells defect 0 · entry-parity PASS · index-sync 33/28 · **13 selftests GREEN**.
- **Verifier:** activity title slots corpus-wide h3 4013 / h2 14 (the PNR exclusion) / h4 0 / h5 0 (was h4 465 / h5 125). **Ceiling:** SCAFFOLD {SK_A}% = **55.7% of achievable** (55.74).

### 6. NAMED, NOT CHASED

- The gold's 12 non-h3 activity titles (h4 10, h2 2 in Standard); the in-box sub-heading level (a separate measured class); the PNR boxes' h2 titles (the r331 named exclusion).

**Ledger:** scoped ship #8 since the r326 full — **the full `ship.sh` backstop is DUE at the next ship** · data `activity_wrapper.title_heading_level` · env `ACTTITLEH3_OFF` · tools `outputs/_measure_r334_subst.py` (+ `_r334_subst.json`), `_measure_r334_skelgaps.py` (+ `_r334_skelgaps.json`), `_measure_r334_acttitle.py` (+ `_r334_acttitle.json`), `_r334_itemdump.cjs`, `_r334_probe.cjs`, `_r334_bagcheck.py`, `_r334_finalise.py` · state `outputs/_r334_sk_final.json` (FRESH) · logs `_r334_gates.log`, `_r334_sk_full.log`, `_r334_fastloop.log`, `_r334_fastloop_commit.log`, `_r334_selftests.log`, `_r334_probe_off_0*.log`, `_r334_probe_on_0*.log`, `_r334_probe_offsave.log`, `_r334_regen.log`, `_r334_fresh.log`, `_r334_affected.txt`, `_r334_batches_run.sh`, `_r334_off_pages/` (the dip check).

"""
if "round 334, build 260619.05" not in s:
    assert s.startswith(head); s = head + ENTRY + s[len(head):]; wr(CL, s); print("changelog prepended")

CF = os.path.join(PF, "app", "js", "Config.js"); c = rd(CF)
OLD = '\tstatic AppVersion = "260619.04";\n'
NEW = ('\t// ROUND 334 (2026-09-15, build 260619.05): the activity box\'s title heading is h3 (KB 01F activity_heading;\n'
       '\t// the gold 0.997) — a post-pass right after the re-leveller pins the box\'s first-child heading to h3 (the\n'
       '\t// writer\'s in-box [H3]/[H4] carried the body shift); scoped regeneration of 73 modules; env ACTTITLEH3_OFF.\n'
       '\tstatic AppVersion = "260619.05";\n')
if '"260619.05"' not in c:
    assert c.count(OLD) == 1; c = c.replace(OLD, NEW, 1); wr(CF, c); print("AppVersion bumped")

CM = os.path.join(PF, "CLAUDE.md"); m = rd(CM)
OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 333 BASELINE (a right-hand alert is a side column; rhs / summary are not classes — KB 05B; scoped 53 modules)"
NEW9 = (f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 334 BASELINE (the activity box's title heading is h3 — KB 01F; scoped 73 modules): SCAFFOLD mean {SK_A}% / >=50% 1066 / >=75% 200 / >=90% 15 / skipped 0 @ 1954; RAW {RAW_A}%** (state `outputs/_r334_sk_final.json`, FRESH). r334 +0.167 (170 moved, 150 up; the 20 dips NAMED = the scorer's alignment artefact with position-free overlap rising or flat (MXFU401_3, PHE1003_1, MXEO202_6/_3, HIS1007_3_1, TEFUN08) + two boxes whose gold title is not h3 (ANZH301_9, ANZH304_6)); every other gate EXACT. Older r333 text: **ROUND 333 BASELINE (a right-hand alert is a side column; rhs / summary are not classes — KB 05B; scoped 53 modules)")
if "ROUND 334 BASELINE" not in m:
    assert m.count(OLD9) == 1, "§9"; m = m.replace(OLD9, NEW9, 1); print("§9")
ROW = ("| `ACTTITLEH3_OFF` | 334 | **THE ACTIVITY BOX'S TITLE HEADING IS h3** (KB 01F `activity_heading`; the autonomous loop's session-5 Round 5; **SCOPED regeneration of the 73 affected modules; scoped ship #8 since the r326 full — the full-ship backstop is DUE**). Reverts byte-for-byte. ON (default), `activity_wrapper.title_heading_level`: `ActivitiesBuilder.activityTitleLevelPostpass`, run in the body chain right after `#relevelHeadings`, pins every activity box's first-child heading (after an optional super-content panel) to h3 — a writer's `[H3]`/`[H4]` typed after the `[Activity]` opener carried the body shift (+1) and the re-leveller skips activity subtrees, so the title never normalised back (the r66 first-line title and the opener payload already shipped at h3). The reoTranslate family is excluded (BilingualBuilder's boxes; PNR keeps h2 by name). MEASURED: gold h3 4548 : 12 Standard / 1029 : 5 Inquiry / 581 : 0 Fundamentals; Claude 465 h4 + 125 h5 (incl. the 115 XDLS tile panels) → 0. 226 pages / 73 modules changed. Skeleton +0.167pp (≥50% +17; 150 up / 20 down, dips named); every other gate EXACT; 13 selftests GREEN. |\n")
if "| `ACTTITLEH3_OFF` | 334 |" not in m:
    A = "| `ALERTRHS_OFF` | 333 |"; assert m.count(A) == 1, "§11"; m = m.replace(A, ROW + A, 1); print("§11")
B14 = (f"- **Build:** `260619.05` (round 334 — **the activity box's title heading is h3** (KB 01F; the autonomous loop's session-5 Round 5; **SCOPED regeneration of 73 modules; scoped ship #8 since the r326 full — the full-ship backstop is DUE at the next ship**). **ROUND 334 BASELINE: SCAFFOLD mean {SK_A}% / ≥50% 1066 / ≥75% 200 / ≥90% 15 / skipped 0 @ 1954; RAW {RAW_A}%** (state `outputs/_r334_sk_final.json`, FRESH) = **55.7% of achievable** (ceiling 91.6%). Every other gate EXACT: cs exact **11375** / EXTRA **171** / missing **593** · clean **2056/2102** / leak **288/46** · body **191** · tags **9557/9557** · flipCard TOTAL 61 divergence 0 · index-sync 33/28 · entry-parity PASS · mtkQuiz shell defect 0 · all THIRTEEN selftests GREEN. Corpus 2102 pages / 413 modules, 0-stale, **226 pages / 73 modules changed, 0 added/removed**; toggle `ACTTITLEH3_OFF`; data `activity_wrapper.title_heading_level`. Activity titles at h4/h5 590 → 0. **Plateau window: r332 +0.269 · r333 +0.066 · r334 +0.167.**)\n")
if "- **Build:** `260619.05` (round 334" not in m:
    A = "- **Build:** `260619.04` (round 333 —"; assert m.count(A) == 1, "§14"; m = m.replace(A, B14 + A, 1); print("§14")
wr(CM, m)

GB = os.path.join(HERE, "..", "reference", "tests", "gate_baseline.json"); raw = rd(GB); d = json.loads(raw)
d["_meta"]["build"] = "260619.05"; d["_meta"]["round"] = 334; d["_meta"]["date"] = "2026-09-15"
d["skeleton"].update({"mean_scaffold_pct": float(SK_A), "raw_mean_pct": float(RAW_A), "pages_ge_50": 1066, "pages_ge_75": 200})
d["_meta"]["_round334_note"] = f"Round 334 (the activity box's title heading is h3 — KB 01F; scoped 73-module regeneration, scoped ship #8 since the r326 full — the full-ship backstop is due). Skeleton {SK_B}->{SK_A} (+0.167pp; 170 moved, 150 up; >=50 1049->1066, >=75 200, >=90 15); every other gate EXACT; 13 selftests GREEN."
wr(GB, json.dumps(d, ensure_ascii=False) + ("\n" if raw.endswith("\n") else "")); print("gate_baseline.json refreshed")

KB = os.path.join(HERE, "..", "..", "KB_AMALGAMATION_STATUS.md"); k = rd(KB)
anchor = "| ~~—~~ | 05B \"Alerts\" vocabulary"
row = ("| ~~—~~ | 01F \"Activities\" — `activity_heading` → `<h3>` (the box's own title heading level) | **SHIPPED round 334** (590 h4/h5 activity titles → h3; 226 pages / 73 modules) | 226 pages | +0.167pp / ≥50 +17 | `ACTTITLEH3_OFF` | CAPTURED-LIVE |\n")
if "01F \"Activities\" — `activity_heading`" not in k:
    assert k.count(anchor) == 1; k = k.replace(anchor, row + anchor, 1); wr(KB, k); print("KB status D-row")

LS = os.path.join(HERE, "..", "..", "LOOP_STATE.md"); s = rd(LS); nl = "\r\n" if "\r\n" in s[:3000] else "\n"
def L(t): return t.replace("\n", nl)
SEC = L(f"""## Session 5 · Round 5 (engine r334) — what shipped (the activity box's title heading is h3)
- **Fix:** `activity_wrapper.title_heading_level` {{enabled, env ACTTITLEH3_OFF, level 3, exclude_body_class_match reoTranslate, skip_panel_class
  "super-content row"}} → `ActivitiesBuilder.activityTitleLevelPostpass(html, run)` in the body chain right after `#relevelHeadings`: every
  activity box's first-child heading (after an optional super-content panel, balanced) is rewritten to h3; nothing else in the box moves;
  the reoTranslate family excluded (PNR keeps h2 by name, r331).
- **Regeneration:** scoped — the in-memory probe over ALL 416 modules (4 shards): OFF = disk 2102/2102; ON named 226 pages / 73 modules and
  every diff line is a heading tag swap (465 h4 + 125 h5 → 590 h3, the 125 including the 115 XDLS tile panels the census only saw once the r307
  class prefix was accounted for); the planner's 9 batches, all rc 0; 0 truly stale; manifest diff = exactly the 226.
- **Gates:** skeleton {SK_B} → {SK_A} (+0.167pp; 170 moved, 150 up / 20 down — dips NAMED: MXFU401_3_0 −8.4 / PHE1003_1_0 −4.6 / MXEO202_6_0 −4.6 /
  MXEO202_3_0 −3.3 / HIS1007_3_1 −3.2 / TEFUN08_0_0 −2.9 = alignment artefacts with the position-free overlap rising or flat; ANZH301_9_0 −3.5 +
  ANZH304_6_0 −3.4 = one box each whose gold title is not h3, the gold's 12-of-4560 minority); ≥50 1049 → 1066; ≥75 200; every other gate
  line-for-line EXACT with r333 (fastloop PASS, nothing to name); 13 selftests GREEN. **55.7% of achievable.**
- **Verifier:** activity title slots h4/h5 590 → 0 (h3 4013, h2 14 = the PNR exclusion). **Plateau window: r332 +0.269 · r333 +0.066 · r334 +0.167.**
  Ship ledger: scoped #8 since the r326 full — **the full-ship backstop is DUE: the next shipped round runs `ship.sh` (full regeneration).**

""")
ANCHOR = "## Session 5 · Round 5 PICK (engine r334)"
if "## Session 5 · Round 5 (engine r334) — what shipped" not in s:
    assert s.count(ANCHOR) == 1; s = s.replace(ANCHOR, SEC + ANCHOR, 1); print("LOOP_STATE section")
OLD_P = "- Session 5 Round 4 (engine r333 — a right-hand alert is a side column; rhs / summary are not classes, KB 05B): SHIPPED 2026-09-15 ≈18:20 (session 5, commit c6660da). AppVersion 260619.04, CLAUDE.md §9/§11/§14, KB status D-row added, scoped ship #7 since the r326 full (backstop due at 8). Skeleton +0.066pp, ≥50 +5; compare_structure exact +15 / EXTRA −15 / missing +2 named."
NEW_P = OLD_P + nl + "- Session 5 Round 5 (engine r334 — the activity box's title heading is h3, KB 01F): SHIPPED 2026-09-15 ≈19:20 (session 5). AppVersion 260619.05, CLAUDE.md §9/§11/§14, KB status D-row added, scoped ship #8 since the r326 full — the full-ship backstop is DUE. Skeleton +0.167pp, ≥50 +17; every other gate EXACT."
if "- Session 5 Round 5 (engine r334" not in s:
    assert s.count(OLD_P) == 1, "position"; s = s.replace(OLD_P, NEW_P, 1); print("position")
OLD_R = "- s5-r4 (engine r333) · a right-hand alert is a side column"
i = s.find(OLD_R); assert i > 0; j = s.find(nl, i) + len(nl)
NEW_R = "- s5-r5 (engine r334) · the activity box's title heading is h3 (KB 01F `activity_heading`; a writer's in-box `[H3]`/`[H4]` carried the body shift and the re-leveller skips activity subtrees — a post-pass pins the box's first-child heading to h3; PNR excluded) · SHIPPED 2026-09-15 · scoped regeneration, 226 pages / 73 modules · scaffold 50.893→51.060 (+0.167; 150 up / 20 down, dips named), ≥50 +17, every other gate EXACT · activity titles at h4/h5 590→0 · 55.7% of achievable · scoped ship #8 — full backstop DUE · commit (see git log)" + nl
if "- s5-r5 (engine r334)" not in s:
    s = s[:j] + NEW_R + s[j:]; print("round log")
old_h = "· r333 (the right-hand alert side column + the summary token, scoped 53 modules, +0.066pp; commit c6660da) · SHIPPED ≈18:20.**"
new_h = "· r333 (the right-hand alert side column + the summary token, scoped 53 modules, +0.066pp; commit c6660da) · r334 (the activity title heading h3, scoped 73 modules, +0.167pp) · SHIPPED ≈19:20.**"
if old_h in s: s = s.replace(old_h, new_h, 1); print("header")
wr(LS, s); print("LOOP_STATE.md written")
