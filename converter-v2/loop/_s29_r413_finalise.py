#!/usr/bin/env python3
"""r413 finalise (CLAUDE.md §12): changelog entry, Config.js bump, CLAUDE.md §9 / §11 / §14, gate_baseline.json."""
import re, json
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
PF = R + "pageforge-site/converter-v2/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

entry = """## 2026-09-20 (round 413, build 260619.84) — THE OWNED HALF OF THE r412 CLASS: a writer-owned typed-widget box whose walk ended at the heading takes the heading, prose and table too (the r407-recorded item itself — "the typed-widget empty boxes, the normal path's opener + a heading"; the autonomous loop's session 29 Round 4; env `HEADTABLEOWNED_OFF` inside `HEADTABLE_OFF`; **SCOPED regeneration of the 5 affected modules, scoped ship #5 since the 19 Sept FULL**)

### 1. WHAT CHANGED

**The class.** r412 took the heading-then-table shape only where the invocation had NO owner. Its owned twin — a real `[Activity N]` / `[Activity] **6A**` opener (or the r402 synthetic owner) owns the task-typed invocation, the walk still ends at the writer's `[H3]` title, and the box ships EMPTY (the `no content captured` flag) with the heading / prose / table free AFTER it — is the item r407 recorded: TEDC401 1E `[drag and drop]` + `[H3] Metadata matching` + table, 2A `[checkbox]`, 3B, 6A `[mcqsomeselected …]`; TEDC402 6A / 6B; WJFUN109 1B (`[drag and drop]` + `[H3]` + `[image]` + instruction + `[body]` + table) and 2A; TEFUN05 1B; ENGI401 2B `[reorder interactive]`. The gold's same-numbered box holds the section INSIDE (h3 + the built widget).

**Measured** (`outputs/_s29_r3_headwalk.cjs` in `HEADWALK_OWNED=1` mode over all 494 Claude-dir modules → `_s29_r4_ownedwalk_rows.tsv`; the typed rows with the h…T shape → `_s29_r4_ownedwalk_T.tsv`; `_s29_r3_goldcheck.py` → `_s29_r4_ownedcheck.out`): 193 owned empty task bundles; the typed heading-then-table shape = **15 bundles / 13 pages / 8 modules** (dragAndDrop 11, multiChoiceQuiz 2, reorder, selectionBox). Where the paired gold page carries the heading (14): INSIDE the same box **12 = 0.86**, the widget built after it on 10; outside 2 (COM1006 5.0, XGF9003 1.2). The 16 unclassified-path rows with the same shape belong to r362's own later-heading guard (ENGI303 lesson 6 measured worse as the owner form) and are untouched.

**The fix (DATA OVER CODE).** `opener_rule.heading_table_owner.owned_bundles {enabled, env HEADTABLEOWNED_OFF, between_media_tags}`: `InteractiveScanner.#headingTableOwner` also accepts an OWNED bundle when the owner carries no title tail (empty, the box's id, or the bare id the r306 `owner_id_from_tail` rule recovers later — `[Activity] **6A**`) and its existing lead holds no heading tag; the real owner stays, the heading goes FIRST in `activityLeadItems` (the box's `<h3>` under the lead loop's first-line-is-the-title rule), the owner's existing lead follows, then the prose after the heading; instruction spans join the bundle's instructions; a listed media element between the heading and the table (`[image]` — WJFUN109 1B) is the box's own lead media (the r364 rule renders it inside the box); the walk resumes AT the table. An opener with its own title tail, or a lead already holding a heading (AGH1004 lesson 1's `[Interactive: activity]` lookback spans a whole earlier section), is left alone — recorded.

### 2. PROOF

- `_s29_r413_probe_run.sh` (the r410 harness over all 494): **OFF (`HEADTABLEOWNED_OFF`) = disk 2555 / 2555**; **ON = 13 pages / 5 modules** (`_affected_r413.txt`: ENGI401, TEDC401, TEDC402, TEFUN05, WJFUN109) — 8 census pages + TEDC401 4.0 / 5.0 and TEDC402 8.0 / 8.1 / 9.0 (`data-cv2-index` renumbering only, the r303 index-only class). AGH1004 1.0 / 5.0 (the lead-holds-a-heading guard), XGF9003 1.2 (a heading in the lead) and COM1006 (two headings) do not fire.
- `_s29_r413_pagescore.py` (the gate's own `match()` on the ON pages before regenerating): **8 up / 0 down / 4 same, pp-sum +18.9 scaffold** — TEDC401_6_0 22.6 → 31.2, WJFUN109_0_0 63.6 → 66.7, TEDC402_7_0 +1.8, TEDC401_1_0 +1.5, ENGI401_2_0 +1.3, TEFUN05_0_0 +1.3, TEDC401_3_0 +0.9, TEDC401_2_0 +0.3.
- `REGENERATE CORPUS` scoped by §0a: the 5 + the 12-module spot-check sample (`_s29_r413_regen.sh`, 4 batches rc 0); `scoped_ship.sh --affected _affected_r413.txt --toggle HEADTABLEOWNED_OFF --no-regen --commit --round 413` (`_s29_r413_scoped_ship.log`): **0 truly stale**, **containment 5 ⊆ 5**, **spot-check 12 / 12 byte-identical**, the exact decomposition **every gate held-or-improved** (RESULT: PASS).
- `_s29_skdelta.py _s29_r412_sk_final.json _s29_r413_sk_final.json`: **8 movers, 8 up / 0 down, 0 outside the affected set, 0 pages added or gone.**
- `_verify_dragdrop.cjs` over the 5 affected: 4 widgets (images 1, column 1, drags 24), defect 0 ✓; the gate set 21 / 0 EXACT.

### 3. PROTECTED GATES (all HELD-or-IMPROVED — `_s29_r413_gates.log`, `_s29_r413_scoped_ship.log`)

- **Skeleton (PRIMARY)**: SCAFFOLD **53.809 → 53.817 % (+0.0080pp)**; ≥50 **1408** / ≥75 **236** / ≥90 **20** EXACT; RAW **37.970 %** EXACT; 2349 pairs / 0 skipped (state `outputs/_s29_r413_sk_final.json`).
- **compare_structure** exact **14174** / EXTRA **186** / MISSING **690** / row-wrap **23** EXACT; **body_compare** 54 / 6 / 190 / 248 EXACT; **defect audit** clean **2504 / 2548 = 98.27 %**, leak **73 / 44** EXACT.
- tags **9557 / 9557**; every verifier RESULT identical to r412; entry-parity PASS; **16 selftests GREEN** (46 PASS / GREEN, 0 FAIL); feature index GREEN.
- Ship ledger: **scoped ship #5 since the 19 Sept FULL** (3 of headroom); fast-loop baseline + content manifest refreshed.
- DIFF MINER re-mined on the r413 corpus (`_diff_miner_s29_r413.log`): **182 → 182 CANDIDATE rows**.
- Plateau: **+0.0080pp, no bucket moved, no other gate moved — the window advances to 1 of 3** (r412 reset it).

### 4. RECORDED, NOT TAKEN (the Round 4 PICK's measurements — `LOOP_STATE.md`)

- AGH1004 lessons 1 / 5: the `[Interactive: activity]` owner's lookback spans a whole earlier section into the lead (a heading + 10 paragraphs) — the pre-existing lead over-capture, its own class.
- DIFF_QUEUE #36 (Claude's EXTRA overview-menu `paddingR` column, 44 modules) decomposes into the BLL banner-family minority (18), the gold-EMPTY menus (13) and three family dialects under the 10-module chrome floor (ARFUN0 OFFSET 5 / 5, XGF9 COL6x2 4 / 5, EXPFUN0 PADLR 4 / 5) — `_s29_r4_menucols.py`.
- The D10-3 rider "re-measure the widened activity wrapper per built layout" is DONE (`_s29_r4_actwidth.py`): the gold's `col-md-12` wrapper never solidifies by widget (dragAndDrop:scatter 0.21, :column 0.19, :standard 0.10, none 0.06) — the r334 decline stands.

"""
p = PF + "BUILD_CHANGELOG.md"; s = rd(p)
head, rest = s.split("\n", 1)
assert head.startswith("# BUILD CHANGELOG") and rest.lstrip("\n").startswith("## 2026-09-20 (round 412")
wr(p, head + "\n\n" + entry + rest.lstrip("\n"))

p = PF + "app/js/Config.js"; s = rd(p)
old = '\tstatic AppVersion = "260619.83";'; assert s.count(old) == 1
note = ("\t// ROUND 413 (260619.84): the OWNED half of the r412 class — a writer-owned typed-widget box whose walk ended at the writer's `[H3]` takes the "
        "heading, prose and table too (`[Activity] **6A**` + `[multi-choice]` + `[H3]` + table → the gold's box 6A with the h3 and the built widget; 12 / 14 = 0.86). "
        "`heading_table_owner.owned_bundles` — the real owner stays, the heading first in the lead, media between allowed, the walk resumed at the table; "
        "env HEADTABLEOWNED_OFF (inside HEADTABLE_OFF). The loop's session 29 Round 4: OFF = disk 2555 / 2555, ON 13 pages / 5 modules (8 up / 0 down, +18.9pp-sum); "
        "SCOPED regeneration of the 5 (scoped ship #5 since the 19 Sept FULL); skeleton 53.809 → 53.817 % (+0.0080pp), every other gate EXACT; miner 182 → 182.\n")
wr(p, s.replace(old, note + '\tstatic AppVersion = "260619.84";'))

p = PF + "CLAUDE.md"; s = rd(p)
old9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 412 BASELINE ("; assert s.count(old9) == 1
new9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 413 BASELINE (the owned half of the r412 class — `heading_table_owner.owned_bundles`, "
        "env `HEADTABLEOWNED_OFF`; 5 modules / 13 pages; SCOPED regeneration of the 5, the probe proving the other 489 byte-identical; scoped ship #5 since the 19 Sept full): "
        "SCAFFOLD mean 53.817% / >=50% 1408 / >=75% 236 / >=90% 20 / RAW 37.970% @ 2349 pairs, pairs skipped 0 — hold-or-improve; 8 movers (8 up, 0 down; 0 outside the "
        "affected set); the 2336 unaffected pairs EXACT. compare_structure exact 14174 / EXTRA 186 / MISSING 690 / row-wrap 23 EXACT; body_compare 54 / 6 / 190 / 248 EXACT; "
        "defect clean 2504 / 2548 = 98.27%, leak 73 / 44 EXACT.** Previous — ROUND 412 BASELINE (")
s = s.replace(old9, new9)
old11 = "| `HEADTABLE_OFF` | 412 | **THE HEADING-THEN-TABLE SHAPE AFTER AN EMPTY TYPED-WIDGET INVOCATION TAKES THE OWNER FORM**"; assert s.count(old11) == 1
row11 = ("| `HEADTABLEOWNED_OFF` | 413 | **THE OWNED HALF OF THE r412 CLASS** (the autonomous loop's session 29 Round 4 — the item r407 recorded: the typed-widget empty "
         "boxes at the normal path). A real `[Activity N]` / `[Activity] **6A**` opener (or the r402 synthetic owner) owns the task-typed invocation whose walk ended at the "
         "writer's `[H3]` title, then prose / an instruction / an `[image]`, then the TABLE — the box shipped EMPTY (the `no content captured` flag) with the section free "
         "after it (TEDC401 1E / 2A / 3B / 6A, TEDC402 6A / 6B, WJFUN109 1B / 2A, TEFUN05 1B, ENGI401 2B). Measured (`_s29_r4_ownedwalk_T.tsv` + `_s29_r4_ownedcheck.out`): "
         "15 bundles / 13 pages / 8 modules; the gold's same-numbered box holds the section on 12 / 14 = 0.86, the widget built inside on 10. Data "
         "`heading_table_owner.owned_bundles {enabled, env, between_media_tags}`; `#headingTableOwner` accepts an owned bundle when the owner carries no title tail (empty, "
         "the id, or the r306 bare-id tail) and its lead holds no heading: the real owner stays, the heading goes first in the lead (the box's `<h3>`), the owner's existing "
         "lead follows, a listed media element between renders inside the box (the r364 rule), the walk resumes at the table. OFF = the r412 output byte-for-byte "
         "(2555 / 2555); `HEADTABLE_OFF` reverts both halves. ON = 13 pages / 5 modules, 8 up / 0 down (+18.9pp-sum). Recorded: AGH1004's `[Interactive: activity]` "
         "lookback lead (a whole earlier section — the guard leaves it), COM1006 / XGF9003 1.2 (the gold un-boxed / a heading in the lead). |\n")
s = s.replace(old11, row11 + old11)
old14 = "- **Build:** `260619.83` (round 412 — **the heading-then-table shape after an empty typed-widget invocation takes the owner form**"; assert s.count(old14) == 1
b14 = ("- **Build:** `260619.84` (round 413 — **the owned half of the r412 class: a writer-owned typed-widget box whose walk ended at the writer's `[H3]` takes the "
       "heading, prose and table too** (`[Activity] **6A**` + `[multi-choice]` + `[H3]` + table → the gold's box 6A with the h3 title and the built widget, 12 / 14 = 0.86; "
       "`heading_table_owner.owned_bundles`, env `HEADTABLEOWNED_OFF` inside `HEADTABLE_OFF`); the autonomous loop's session 29 Round 4 — the r407-recorded item completed; "
       "the probe OFF = disk 2555 / 2555, ON 13 pages / 5 modules (8 up / 0 down, +18.9pp-sum, 0 outside the set); **SCOPED regeneration of the 5 (scoped ship #5 since the "
       "19 Sept FULL)**; **ROUND 413 BASELINE: SCAFFOLD mean 53.817% / >=50% 1408 / >=75% 236 / >=90% 20 / RAW 37.970% @ 2349 pairs** (+0.0080pp; buckets EXACT); "
       "compare_structure 14174 / 186 / 690 / 23, body 54 / 6 / 190 / 248, clean 2504 / 2548, leak 73 / 44 — all EXACT; every verifier EXACT; 16 selftests GREEN; the miner "
       "182 → 182; plateau window 1 of 3). Previous: ")
s = s.replace(old14, b14 + old14)
wr(p, s)

p = R + "CONVERTER_V2/reference/tests/gate_baseline.json"; s = rd(p)
def setv(key, old, new):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=1); assert n == 1, key
setv("build", '"260619.83"', '"260619.84"'); setv("round", 412, 413)
setv("mean_scaffold_pct", 53.81, 53.82)
a = '    "_note_r412": "Round 412 (session 29 Round 3)'; assert s.count(a) == 1
s = s.replace(a, '    "_note_r413": "Round 413 (session 29 Round 4): the owned half of the r412 class (heading_table_owner.owned_bundles, env HEADTABLEOWNED_OFF; 5 modules / 13 pages; SCOPED regeneration of the 5; skeleton 53.8088 -> 53.8168, buckets EXACT, RAW 37.970 EXACT; every other gate EXACT).",\n' + a)
a2 = '    "_note_r411b": "Round 412: SCAFFOLD 53.7949'; assert s.count(a2) == 1
s = s.replace(a2, '    "_note_r412b": "Round 413: SCAFFOLD 53.8088 -> 53.8168 (+0.0080pp; 8 movers all up — TEDC401_6_0 +8.6, WJFUN109_0_0 +3.1; 0 outside the 5-module affected set), 1408 / 236 / 20 EXACT, RAW 37.970 EXACT; 2349 pairs.",\n' + a2)
wr(p, s); json.load(open(p, encoding="utf-8"))
print("r413 finalise: changelog + Config.js 260619.84 + CLAUDE.md §9/§11/§14 + gate_baseline.json done")
