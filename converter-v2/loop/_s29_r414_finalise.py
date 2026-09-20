#!/usr/bin/env python3
"""r414 finalise (CLAUDE.md §12): changelog entry, Config.js bump, CLAUDE.md §9 / §11 / §14, gate_baseline.json. Run under WSL."""
import re, json
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
PF = R + "pageforge-site/converter-v2/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

entry = """## 2026-09-20 (round 414, build 260619.85) — THE NESTED ACTIVITY BOX: a synthetic widget box never opens inside an open activity box — the widget belongs to the open box (the autonomous loop's session 29 Round 5; SCOPED regeneration of the 65 affected modules — scoped ship #6 since the 19 Sept FULL; every protected gate HELD-or-IMPROVED)

### 1. WHAT CHANGED

**The class.** Claude shipped an `activity` box INSIDE another `activity` box on **108 sites / 94 pages / 65 modules**; the gold nests on 3 pages (11 boxes, all Mathematics — MXDI101 / MXFL101 / MXFL301, editorial). The inner box was ALWAYS `activity interactive` — the r217 SYNTHETIC standalone-widget box (`saOwner`) or the r266 level-pages box (`lvOwner`): both are decided AFTER the bundle site's `isNewActivity` guard (which closes an open activity only for a bundle with a REAL owner or id), so a standalone task widget met while a writer's activity frame was still on the stack — a bundle-owned box whose frame stayed open after its own widget (77 of 108; the r314 / r378 held frames and the plain owned box), a plain writer box (22), a super-content box (9) — opened its own box inside the open one (HIS1004 7D: the writer's `[Activity 7D]` + `[Interactive] Please add a button …` → `activity 7D › activity interactive 7E`; MXFL102 8A › 7B; BLL114 2B › 2C). Found through the empty-shell census (`outputs/_s29_r5_emptyrows.py` → `_s29_r5_emptyrows.out`: 818 empty `row › col` shells — 725 the module menu's `moduleMenu › row › col-md-8` shell on pages whose gold menu has TEXT (445) or no menu element (56), the body's 154 decomposing to the nested box's own artefact (76: the inner box's close pops the outer's inner `row › col-12`, and the outer's own close then lands in a fresh `row › col-md-8` shell), 38 writer-owned empty boxes and 14 HPFUN omitted-prompt rows).

**Measured** (`outputs/_s29_r5_nestbox.py` → `_s29_r5_nestbox.out`, every nested pair on a paired page, the inner box's words found in the gold): 97 pairs / 84 pages / 63 modules; decided 43 — the gold keeps the widget INSIDE the outer's box 19 (BLL 10 / 10, the phonics multi-widget box of the r229 CL-0030 record), starts a SEPARATE sibling box 18 (Mathematics 5 / 6, English 3 / 3, FRFUN 4 / 4, NCEA1 3), no box 6; 54 ABSENT (the gold's built widget carries different words). The nesting itself is 0.97 wrong in every group; the un-nesting FORM looked split by family — so both forms were scored with the skeleton gate's own `match()` on the probe's 84 paired ON pages (`_s29_r414_variants.sh`): SUPPRESS the synthetic box everywhere = **81 up / 3 down (+163.5 pp-sum; every subject group net up — Mathematics 12 / 0, English 9 / 0, NCEA1 15 / 1, BLL 23 / 1)**; CLOSE the outer first everywhere = 28 up / 24 down (+27.7; BLL 2 / 14); the per-subject mix 50 / 10 (+115.4). The gate decides: the widget belongs to the OPEN box (the `activity_close_before.keeps_inside` rule — "everything content-like including interactive placeholders stays inside").

**The fix (DATA OVER CODE).** `activity_wrapper.standalone_widget_box.inside_open_activity {enabled, env NESTBOX_OFF, close_outer_subjects: []}`: at the bundle site, when the synthetic owner (`saOwner` / `lvOwner`) is about to open and the stack top is an activity, the synthetic box is SUPPRESSED and the widget renders inside the open box (no positional letter spent — every later box on the page keeps the gold's lettering); a subject listed in `close_outer_subjects` (the module index's subject; none measured to want it) takes the other form — the outer closes first (the `isNewActivity` convention) and the widget becomes the next sibling box. `ContentConverter` (the bundle site, `actOwner` now `let`). OFF = the r413 output byte-for-byte.

### 2. PROOF

- `_s29_r414_probe_run.sh` (the r410 harness over all 494 Claude-dir modules, 4 shards): **OFF (`NESTBOX_OFF`) = disk 2555 / 2555**; **ON = 94 pages / 65 modules** (`_affected_r414.txt`) = the nested-box census to the page; nested boxes in the ON output **108 → 0**; the body's empty shells 154 → 74.
- `_s29_r414_pagescore.py` (the gate's own `match()` on the ON pages before regenerating): **81 up / 3 down / 0 same, SCAFFOLD pp-sum +163.5, RAW +64.1**; the three dips BLL162_1_0 −1.1, HIS1004_8_0 −0.5, XDLS909_4_0 −0.1 (alignment on pages whose gold boxes differ in count; RAW up on BLL162).
- `REGENERATE CORPUS` scoped by §0a: the 65 + the 12-module spot-check sample (`_s29_r414_regen.sh`, 7 batches rc 0); `scoped_ship.sh --affected _affected_r414.txt --toggle NESTBOX_OFF --no-regen --commit --round 414` **PASS** — content-hash 0 truly stale, containment 65 ⊆ 65, spot-check 12 / 12 byte-identical, the exact decomposition gate proof (`_s29_r414_scoped_ship.log`).
- `_s29_skdelta.py _s29_r413_sk_final.json _s29_r414_sk_final.json --affected _affected_r414.txt`: **84 movers, 81 up / 3 down, 0 outside the affected set**, 0 pages added / gone; BLL143_1_0 +15.1, FRFUN06_3_0 +12.2, AGH1008_5_0 +7.9, BLL151_1_0 +6.6, ENGS404_2_0 +6.4.
- Verifiers in the gate run: dragAndDrop 21 widgets / defect 0, flipCard divergence 0, speechBubble / modal / mtkquiz / math / menulabels ✓ — every RESULT identical to r413.

### 3. PROTECTED GATES (all HELD-or-IMPROVED — `_s29_r414_gates.log`, `_s29_r414_scoped_ship.log`)

- **Skeleton (PRIMARY)**: SCAFFOLD **53.817 → 53.886 % (+0.0696pp)**; ≥50 **1408 → 1412**, ≥75 **236 → 238**, ≥90 **20** EXACT; RAW **37.970 → 37.997 %**; 2349 pairs, skipped 0 (state `outputs/_s29_r414_sk_final.json`).
- **compare_structure** exact **14174** / EXTRA **186** / MISSING **690** / row-wrap **23** EXACT; **body_compare** 54 / 6 / 190 / 248 EXACT; **defect** clean 2504 / 2548 = 98.27 %, leak 73 / 44 EXACT.
- tags **9557 / 9557**; entry-parity PASS; index-sync 33 / 28; **16 selftests GREEN** (46 PASS / GREEN lines, 0 FAIL).
- Ship ledger: **scoped ship #6 since the 19 Sept FULL** (2 of headroom); fast-loop baseline + content manifest refreshed; feature index `--rehtml` / `--merge` / `--selftest` GREEN.
- DIFF MINER re-mined on the r414 corpus (`_diff_miner_s29_r414.log`): **182 → 181 CANDIDATE rows** — the `activity EXTRA div.col-12` row (the nested box's inner column) gone, nothing new.
- Plateau: **+0.0696pp with ≥50 +4 / ≥75 +2 — the window RESETS (0 of 3)**.

### 4. RECORDED, NOT TAKEN (the Round 5 PICK's measurements — `LOOP_STATE.md`)

- The module menu's empty `row › col-md-8` shell (725 of the 818 shells): right where the gold's menu has content (445 pages — class C menu text, the r147 "not-in-WT" record); where the gold ships NO menu element (56: FRFUN 25 / 26 lesson pages, ConnectED 13) the fix is a family `menu_type` row, not a shell rule.
- The 38 writer-owned EMPTY boxes (the r379 `[Activity: Embedded – Brainstorm]` class) and the 14 HPFUN omitted-prompt rows (r203).
- The r314 / r378 held-frame `breakRow()` running with an outer container still open (the shell artefact's mechanism) — closed for the nested-box case by this round; no other producer found.

"""
p = PF + "BUILD_CHANGELOG.md"; s = rd(p)
head, rest = s.split("\n", 1)
assert head.startswith("# BUILD CHANGELOG") and rest.lstrip("\n").startswith("## 2026-09-20 (round 413")
wr(p, head + "\n\n" + entry + rest.lstrip("\n"))

p = PF + "app/js/Config.js"; s = rd(p)
old = '\tstatic AppVersion = "260619.84";'; assert s.count(old) == 1
note = ("\t// ROUND 414 (260619.85): THE NESTED ACTIVITY BOX — a synthetic widget box (the r217 standalone box / the r266 level-pages box) never opens inside an "
        "open activity box: the widget belongs to the open box (108 nested boxes on 94 pages / 65 modules; the gold nests on 3 pages). "
        "`activity_wrapper.standalone_widget_box.inside_open_activity`, env NESTBOX_OFF. The loop's session 29 Round 5: OFF = disk 2555 / 2555, ON 94 pages / 65 modules "
        "(81 up / 3 down, +163.5pp-sum — the close-the-outer form scored 28 / 24); SCOPED regeneration of the 65 (scoped ship #6 since the 19 Sept FULL); "
        "skeleton 53.817 → 53.886 % (+0.0696pp), ≥50 1408 → 1412, ≥75 236 → 238, every other gate EXACT; miner 182 → 181.\n")
wr(p, s.replace(old, note + '\tstatic AppVersion = "260619.85";'))

p = PF + "CLAUDE.md"; s = rd(p)
old9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 413 BASELINE ("; assert s.count(old9) == 1
new9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 414 BASELINE (the nested activity box — the synthetic widget box suppressed inside an open "
        "activity box, `standalone_widget_box.inside_open_activity`, env `NESTBOX_OFF`; 65 modules / 94 pages; SCOPED regeneration of the 65, the probe proving the other 429 "
        "byte-identical; scoped ship #6 since the 19 Sept full): SCAFFOLD mean 53.886% / >=50% 1412 / >=75% 238 / >=90% 20 / RAW 37.997% @ 2349 pairs, pairs skipped 0 — "
        "hold-or-improve; 84 movers (81 up, 3 down — BLL162_1_0 −1.1, HIS1004_8_0 −0.5, XDLS909_4_0 −0.1; 0 outside the affected set); the 2265 unaffected pairs EXACT. "
        "compare_structure exact 14174 / EXTRA 186 / MISSING 690 / row-wrap 23 EXACT; body_compare 54 / 6 / 190 / 248 EXACT; defect clean 2504 / 2548 = 98.27%, "
        "leak 73 / 44 EXACT.** Previous — ROUND 413 BASELINE (")
s = s.replace(old9, new9)
old11 = "| `HEADTABLEOWNED_OFF` | 413 | **THE OWNED HALF OF THE r412 CLASS**"; assert s.count(old11) == 1
row11 = ("| `NESTBOX_OFF` | 414 | **THE NESTED ACTIVITY BOX — a synthetic widget box never opens inside an open activity box** (the autonomous loop's session 29 Round 5). "
         "The r217 standalone-widget box (`saOwner`) and the r266 level-pages box (`lvOwner`) are decided after the bundle site's `isNewActivity` guard, so a standalone "
         "task widget met while a writer's activity frame was still open (a bundle-owned box whose frame stayed open after its own widget 77, a plain writer box 22, a "
         "super-content box 9) opened its box INSIDE the open one: 108 nested boxes on 94 pages / 65 modules, the gold on 3 pages (11, all Mathematics — editorial). "
         "Measured on the paired pages (`_s29_r5_nestbox.py` → `_s29_r5_nestbox.out`): the gold keeps the widget inside the outer box 19 (BLL 10 / 10) or starts a "
         "separate box 18 (Mathematics 5 / 6, English 3 / 3, FRFUN 4 / 4) — but scored with the gate's own `match()` on the probe's 84 paired pages "
         "(`_s29_r414_variants.sh`) suppressing the synthetic box everywhere = 81 up / 3 down (every group net up) vs closing the outer first everywhere = 28 up / 24 down. "
         "Data `activity_wrapper.standalone_widget_box.inside_open_activity {enabled, env, close_outer_subjects: []}`: when the synthetic owner is about to open and the "
         "stack top is an activity the synthetic box is SUPPRESSED — the widget renders inside the open box (the `activity_close_before.keeps_inside` rule) and spends no "
         "positional letter; a subject in `close_outer_subjects` takes the close-first form (the `isNewActivity` convention). OFF = the r413 output byte-for-byte "
         "(2555 / 2555). ON = 94 pages / 65 modules, 81 up / 3 down (+163.5pp-sum). Recorded: the module menu's empty shell (725 — the gold's menu has content on 445 pages; "
         "FRFUN / ConnectED ship no menu element = a family `menu_type` row), the 38 writer-owned empty boxes, the 14 HPFUN omitted-prompt rows. |\n")
s = s.replace(old11, row11 + old11)
old14 = "- **Build:** `260619.84` (round 413 — **the owned half of the r412 class"; assert s.count(old14) == 1
b14 = ("- **Build:** `260619.85` (round 414 — **the nested activity box: a synthetic widget box never opens inside an open activity box — the widget belongs to the open "
       "box** (the r217 standalone box / the r266 level-pages box, decided after the `isNewActivity` guard, opened INSIDE a writer's still-open frame: 108 nested boxes on "
       "94 pages / 65 modules, the gold on 3 pages; `activity_wrapper.standalone_widget_box.inside_open_activity`, env `NESTBOX_OFF`); the autonomous loop's session 29 "
       "Round 5 — found through the empty-shell census; the two un-nesting forms scored on the gate's own `match()`: suppress everywhere 81 up / 3 down vs close-the-outer "
       "28 / 24; the probe OFF = disk 2555 / 2555, ON 94 pages / 65 modules (+163.5pp-sum, 0 outside the set); **SCOPED regeneration of the 65 (scoped ship #6 since the "
       "19 Sept FULL)**; **ROUND 414 BASELINE: SCAFFOLD mean 53.886% / >=50% 1412 / >=75% 238 / >=90% 20 / RAW 37.997% @ 2349 pairs** (+0.0696pp; ≥50 +4, ≥75 +2); "
       "compare_structure 14174 / 186 / 690 / 23, body 54 / 6 / 190 / 248, clean 2504 / 2548, leak 73 / 44 — all EXACT; every verifier EXACT; 16 selftests GREEN; the miner "
       "182 → 181; plateau window RESET (0 of 3)). Previous: ")
s = s.replace(old14, b14 + old14)
wr(p, s)

p = R + "CONVERTER_V2/reference/tests/gate_baseline.json"; s = rd(p)
def setv(key, old, new):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=1); assert n == 1, key
setv("build", '"260619.84"', '"260619.85"'); setv("round", 413, 414)
setv("mean_scaffold_pct", 53.82, 53.89); setv("median_scaffold_pct", 54.7, 54.8)
setv("pages_ge_50", 1408, 1412); setv("pages_ge_75", 236, 238); setv("raw_mean_pct", 37.97, 38.0)
a = '    "_note_r413": "Round 413 (session 29 Round 4)'; assert s.count(a) == 1
s = s.replace(a, '    "_note_r414": "Round 414 (session 29 Round 5): the nested activity box — the synthetic widget box suppressed inside an open activity box (standalone_widget_box.inside_open_activity, env NESTBOX_OFF; 65 modules / 94 pages; SCOPED regeneration of the 65; skeleton 53.8168 -> 53.8864, >=50 1408 -> 1412, >=75 236 -> 238, RAW 37.970 -> 37.997; every other gate EXACT).",\n' + a)
a2 = '    "_note_r412b": "Round 413: SCAFFOLD 53.8088'; assert s.count(a2) == 1
s = s.replace(a2, '    "_note_r413b": "Round 414: SCAFFOLD 53.8168 -> 53.8864 (+0.0696pp; 84 movers 81 up / 3 down — BLL143_1_0 +15.1, FRFUN06_3_0 +12.2, AGH1008_5_0 +7.9; dips BLL162_1_0 -1.1, HIS1004_8_0 -0.5, XDLS909_4_0 -0.1; 0 outside the 65-module affected set), 1412 / 238 / 20, RAW 37.997; 2349 pairs.",\n' + a2)
wr(p, s); json.load(open(p, encoding="utf-8"))
print("r414 finalise: changelog + Config.js 260619.85 + CLAUDE.md §9/§11/§14 + gate_baseline.json done")
