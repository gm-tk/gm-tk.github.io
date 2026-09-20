#!/usr/bin/env python3
"""r412 finalise (CLAUDE.md §12): changelog entry, Config.js bump, CLAUDE.md §9 / §11 / §14, gate_baseline.json."""
import re, json
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
PF = R + "pageforge-site/converter-v2/"

def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

# ---------- 1. changelog ----------
entry = """## 2026-09-20 (round 412, build 260619.83) — THE HEADING-THEN-TABLE SHAPE AFTER AN EMPTY TYPED-WIDGET INVOCATION TAKES THE OWNER FORM: the writer's `[H3]` title, instruction paragraph and table after a bare `[drag and drop]` / `[Interactive activity]` / `[Activity 2C][drag and drop]` are the box's title, lead and widget data (the autonomous loop's session 29 Round 3 — the follow-up r407 recorded: "the typed-widget empty boxes — the normal path's opener + a heading"; env `HEADTABLE_OFF`; **SCOPED regeneration of the 18 affected modules, scoped ship #4 since the 19 Sept FULL**)

### 1. WHAT CHANGED

**The class.** A task-typed widget invocation with no activity opener before it (`[interactive: flowchart drag and drop]` AGH1004 lesson 6, `[Interactive activity]` HPFUN201, `[Activity: Embedded]` AGH1009) or with its id embedded in the span (`[Activity 2C][drag and drop]` WJFUN110, `[Activity 1A] [Drag and drop]` WJFUN211) is followed by the writer's `[H3]` title ("From Grass to Glass", "Guess the audience"), an instruction paragraph and the widget's TABLE. Headings terminate the member walk, so the bundle held only its invocation: the r401 skip_empty rendered no box (and spent no letter), the heading and prose shipped free and the table as a kept `<table>`. The gold boxes the section — `<div class="activity interactive" number="1B"><h3>…</h3><p>…</p>` + the BUILT `dragAndDrop` (the r362 / r363 / r407 owner form, at the NORMAL widget path this time).

**Measured** (`outputs/_s29_r3_headwalk.cjs` through the LIVE scanner over all 494 Claude-dir modules → `_s29_r3_headwalk_rows.tsv`; `_s29_r3_goldcheck.py` → `_s29_r3_goldcheck.out`): 378 empty task bundles / 176 modules; the forward walk (blanks skipped, ≤ 8 items) ends at a TABLE on **31 bundles / 29 pages / 28 modules** — dragAndDrop 21, unclassified 7, dropDown 2, mcq 1 with a heading (3 heading-less flipCard / carousel rows excluded by the rule's heading requirement). Where the paired gold page carries the heading (17 of the 26 with one): INSIDE an activity box **15 = 0.88**, the widget BUILT after it on 13 (dragAndDrop 9, reorder, tabs, selectionBox, dropQuiz); outside-with-widget 2. Per template: Standard 6 / 7, Fundamentals 11 / 12, Inquiry 1 / 1. **NEW-FAMILY CHECK:** WJFUN is 7 of the 29 pages; without it the gold boxes 10 / 13 = 0.77 — the class holds outside the September-intake family. Gold heading ABSENT on 9 (the gold re-titled the box — TEDC401 2.0's gold is `activity interactive 2D` + `<h3>Design principles identified</h3>` for the writer's "Design principles identified (label)": the box form, a different title text).

**The fix (DATA OVER CODE, env `HEADTABLE_OFF`).** `Interactive_Boundary_ChildTag_Bank._meta.opener_rule.heading_table_owner {enabled, env, types, heading_tags, between_tags, max_between}`. `InteractiveScanner.#headingTableOwner` (called right after the member walk): a listed-type bundle with no owner, no captured table and no member beyond its invocation whose walk stopped at a listed heading, followed within `max_between` (6) blank / prose / `[body]` / `[list]` / instruction items by a TABLE and nothing else (another opener, a marker, a media element or a consumed item ends the look-ahead with no change), becomes an OWNED bundle: a synthetic bare owner (the r402 `_aliasElementOwner` shape — an embedded `[Activity 2C]` id keeps its number, an id-less one takes the r400 positional letter), the heading + prose = `activityLeadItems` (ContentConverter's lead loop renders the `<h3>` title and the free prose inside the box), instruction spans join the bundle's instructions (the red Writers Note), and the walk resumes AT the table so it is captured as the widget's data — the r69 / r350 / r351 dragAndDrop builders then build it (9 new 03B dragAndDrops: EXBP901, HPFUN302, TEFUN06 ×2, TWHA904, TWHA905, XGF9003 ×3; the rest keep the honest hand-off box INSIDE the gold's box form).

### 2. PROOF

- `_s29_r412_probe_run.sh` (the r410 harness over all 494 Claude-dir modules): **OFF = disk 2555 / 2555** (516 + 711 + 816 + 512, 0 changed); **ON = 24 pages / 18 modules** (`_affected_r412.txt`), the other 476 modules byte-identical: the 17 census pages the rule reaches + TEDC401 3.0 / 4.0 / 5.0 / 6.0 (`data-cv2-index` renumbering only — the r303 index-only class, gate-invisible) + XGF9003 1.2 / 1.3 (the r223 letter continuation — the new box on 1.0 shifts the sub-pages' letters 1K → 1L, gate-neutral: the gold paginates XGF9003 one file per lesson).
- The 12 census pages the rule does NOT reach are the r362 unclassified-activity path (a numbered `[Activity N]` with a table and no keyword — AGH1009, HPFUN102, HPFUN402, TWHA902, TEDC402, EXIP901's second bundle: they already carry the owner form or the r407 empty-walk rule) and DAN1004 / CEDR501 / CHFUN05 / TEFUN05 (no heading) — untouched by construction.
- `_s29_r412_pagescore.py` (the gate's own `match()` on the ON pages before regenerating): **14 up / 3 down / 7 same, pp-sum +32.6 scaffold / +17.5 RAW** — EXBP901_3_0 18.3 → 26.5, TEFUN06_0_0 43.0 → 50.1, AGH1004_6_0 53.0 → 59.9, WJFUN110_0_0 53.3 → 57.8, SCES201_3_0 77.0 → 81.3, TWHA904 +3.5, AGH1006_8_0 46.6 → 50.0, HPFUN302 +3.1, WJFUN305 / 212 / 208 / 211 +1.4 … +1.9. **The 3 dips, named:** HPFUN201_0_0 −7.0 (the gold ships that section UN-boxed — `<h3>` free + the dropQuiz after it — the HPFUN family's own 1-of-4 minority: HPFUN102 / 302 / 402 box theirs); TEDC401_2_0 −5.6 (the gold's own `activity interactive 2D` + `<h3>` form, matched to the number; the un-built dragAndDrop + speechBubble + carousel bundle's hand-off dump now sits inside the box — the r176 net-positive alignment class; the box and its title are the gold's); HES1002_5_0 −2.4 (a mispaired page — the gold library's HES1002 carries no contraceptives lesson; the change is judged against unrelated gold).
- `REGENERATE CORPUS` scoped by §0a: the 18 + the 12-module spot-check sample (`_s29_r412_regen.sh`, 4 batches rc 0); `scoped_ship.sh --affected _affected_r412.txt --toggle HEADTABLE_OFF --no-regen --commit --round 412` (`_s29_r412_scoped_ship.log`): **0 truly stale**, **containment 18 ⊆ 18**, **spot-check 12 / 12 byte-identical** (BLL131 BLL164 BLL240 CEDW201 DAN1006 ENGJ102 HPFUN102 PWY1007 PWY1009 TEFUN05 TWHA906 WJFUN304); the exact decomposition MOVED on ONE metric, accepted by name (`_fastloop_diff.py --commit --accept-named "compare_structure exact chain"`, `_s29_r412_fastloop_commit.log`): exact **14175 → 14174 = the matched pool 16470 → 16469, SCES201 alone (matched 58 → 57, exact 54 → 53)** — the r57 / r147 relocation class, the kept `<table>` / free heading moving into the built widget's box on a page that rose 77.0 → 81.3.
- `_s29_skdelta.py _s29_r411_sk_final.json _s29_r412_sk_final.json`: **17 movers, 14 up / 3 down, 0 outside the affected set, 0 pages added or gone.**
- `_verify_dragdrop.cjs` over the 18 affected: **9 widgets (images 1, column 2, drags 74), defect 0 ✓**; over the gate set 21 / 0 EXACT.

### 3. PROTECTED GATES (all HELD-or-IMPROVED — `_s29_r412_gates.log`, `_s29_r412_scoped_ship.log`)

- **Skeleton (PRIMARY)**: SCAFFOLD **53.795 → 53.809 % (+0.0139pp)**; ≥50 **1406 → 1408 (+2: TEFUN06_0_0, AGH1006_8_0)** / ≥75 **236** / ≥90 **20** EXACT; RAW **37.963 → 37.970 %**; 2349 pairs / 0 skipped (state `outputs/_s29_r412_sk_final.json`).
- **compare_structure** exact **14175 → 14174 (−1 = the matched pool −1, SCES201 — NAMED, the relocation class)** / EXTRA **186** / MISSING **690** / row-wrap **23** EXACT; **body_compare** 54 / 6 / 190 / 248 EXACT; **defect audit** clean **2504 / 2548 = 98.27 %**, leak **73 / 44** EXACT.
- tags **9557 / 9557**; flipCard 61 / divergence 0; speechBubble defect 4 (baseline); modal 0; mtkQuiz 0; math 323 / 323; menulabels 99 / 0; dragAndDrop 21 / 0; entry-parity PASS; **16 selftests GREEN** (46 PASS / GREEN, 0 FAIL); feature index GREEN (rehtml / merge / selftest).
- Ship ledger: **scoped ship #4 since the 19 Sept FULL** (4 of headroom); fast-loop baseline + content manifest refreshed.
- DIFF MINER re-mined on the r412 corpus (`_diff_miner_s29_r412.log`): **182 → 182 CANDIDATE rows** — the class lives below the miner's floor (29 pages spread over 18 subject groups).
- Plateau: **+0.0139pp with ≥50 +2 — a bucket moved, the window RESETS (0 of 3)**. Read on the post-intake 2,349-pair population (§1e).

### 4. RECORDED, NOT TAKEN

- The 12 remaining `h … T` census pages on the unclassified-activity path (AGH1009, HPFUN102, HPFUN402, TWHA902, TEDC402, EXIP901) — the r362 / r407 form already owns them; the hand-off box inside is the widget-build backlog (the `[Activity: Embedded]` un-buildable type).
- The 22 dragAndDrop tables the r69 / r350 / r351 builders decline inside the new boxes (AGH1004's 2-column term ║ description table with a header row of instructions, WJFUN's 3-column feature tables, SCES201) — honest hand-off boxes in the gold's box form; the builders' next dialects.
- HPFUN201's un-boxed gold form (1 of 4 in HPFUN) — the family's own minority, named above.

"""
p = PF + "BUILD_CHANGELOG.md"; s = rd(p)
head, rest = s.split("\n", 1)
assert head.startswith("# BUILD CHANGELOG") and rest.lstrip("\n").startswith("## 2026-09-20 (round 411")
wr(p, head + "\n\n" + entry + rest.lstrip("\n"))

# ---------- 2. Config.js ----------
p = PF + "app/js/Config.js"; s = rd(p)
old = '\tstatic AppVersion = "260619.82";'; assert s.count(old) == 1
note = ("\t// ROUND 412 (260619.83): the heading-then-table shape after an EMPTY typed-widget invocation takes the owner form — the writer's `[H3]` title, "
        "instruction paragraph and table after a bare `[drag and drop]` / `[Interactive activity]` / `[Activity 2C][drag and drop]` are the box's title, lead and "
        "widget data (the gold's box on 15 / 17 = 0.88, the widget built inside it on 13; 10 / 13 without the WJFUN intake family). "
        "`opener_rule.heading_table_owner` + InteractiveScanner.#headingTableOwner (a synthetic bare owner, the heading + prose as activityLeadItems, the walk "
        "resumed at the table); env HEADTABLE_OFF. The loop's session 29 Round 3 (the r407-recorded follow-up): OFF = disk 2555 / 2555, ON 24 pages / 18 modules "
        "(14 up / 3 down, +32.6pp-sum); SCOPED regeneration of the 18 (scoped ship #4 since the 19 Sept FULL); skeleton 53.795 → 53.809 % (+0.0139pp), ≥50 +2; "
        "compare_structure exact −1 = the matched pool −1 (SCES201, named); every other gate EXACT; miner 182 → 182.\n")
wr(p, s.replace(old, note + '\tstatic AppVersion = "260619.83";'))

# ---------- 3. CLAUDE.md ----------
p = PF + "CLAUDE.md"; s = rd(p)
old9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 411 BASELINE ("; assert s.count(old9) == 1
new9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 412 BASELINE (the heading-then-table shape after an empty typed-widget invocation "
        "takes the owner form — `opener_rule.heading_table_owner`, env `HEADTABLE_OFF`; 18 modules / 24 pages; SCOPED regeneration of the 18, the probe proving "
        "the other 476 byte-identical; scoped ship #4 since the 19 Sept full): SCAFFOLD mean 53.809% / >=50% 1408 / >=75% 236 / >=90% 20 / RAW 37.970% @ 2349 pairs, "
        "pairs skipped 0 — hold-or-improve; 17 movers (14 up, 3 down — HPFUN201_0_0 −7.0 the family's un-boxed minority, TEDC401_2_0 −5.6 the gold's own box form "
        "with the hand-off dump inside, HES1002_5_0 −2.4 a mispaired page; 0 outside the affected set); the 2325 unaffected pairs EXACT. compare_structure exact "
        "14174 (−1 = the matched pool −1, SCES201, the relocation class) / EXTRA 186 / MISSING 690 / row-wrap 23; body_compare 54 / 6 / 190 / 248 EXACT; defect clean "
        "2504 / 2548 = 98.27%, leak 73 / 44 EXACT.** Previous — ROUND 411 BASELINE (")
s = s.replace(old9, new9)
old11 = "| `TILEMENUROW_OFF` | 411 | **THE TILE DIALECT'S MENU TAKES THE GOLD'S ROW+COL TABS SHELL**"; assert s.count(old11) == 1
row11 = ("| `HEADTABLE_OFF` | 412 | **THE HEADING-THEN-TABLE SHAPE AFTER AN EMPTY TYPED-WIDGET INVOCATION TAKES THE OWNER FORM** (the autonomous loop's session 29 "
         "Round 3 — the follow-up r407 recorded: the typed-widget empty boxes at the NORMAL widget path). A task-typed invocation with no activity opener before it "
         "(`[interactive: drag and drop]`, `[Interactive activity]`) or with its id embedded in the span (`[Activity 2C][drag and drop]`) is followed by the writer's "
         "`[H3]` title, an instruction paragraph and the widget's TABLE; headings terminate the member walk, so the bundle held only its invocation — the r401 "
         "skip_empty rendered no box, the heading and prose shipped free and the table as a kept `<table>`. The gold boxes the section: `<h3>` title + `<p>` + the "
         "BUILT widget (measured through the live scanner over all 494 Claude-dir modules, `_s29_r3_headwalk.cjs` + `_s29_r3_goldcheck.py`: 31 bundles / 29 pages / "
         "28 modules; the gold's box on 15 of the 17 pages carrying the heading = 0.88, the widget built inside on 13; Standard 6 / 7, Fundamentals 11 / 12, Inquiry "
         "1 / 1; 10 / 13 without the WJFUN intake family). Data `BoundaryBank._meta.opener_rule.heading_table_owner {types, heading_tags, between_tags, max_between}`; "
         "`InteractiveScanner.#headingTableOwner` right after the member walk: a listed-type bundle with no owner, no table and no member beyond its invocation whose "
         "walk stopped at a heading, followed within max_between prose / `[body]` / instruction items by a TABLE and nothing else, takes a synthetic bare owner (the "
         "r402 shape — an embedded id keeps its number, an id-less one the r400 positional letter), the heading + prose as `activityLeadItems`, instruction spans as "
         "the bundle's instructions, and the walk resumes AT the table (the r69 / r350 / r351 builders then build it — 9 new 03B dragAndDrops). OFF = the r411 output "
         "byte-for-byte (2555 / 2555). ON = 24 pages / 18 modules, 14 up / 3 down (+32.6pp-sum; the dips named in the r412 changelog). Recorded: the 12 census pages "
         "on the unclassified-activity path (already the r362 / r407 owner form), the 22 tables the dragAndDrop builders decline inside the new boxes. |\n")
s = s.replace(old11, row11 + old11)
old14 = "- **Build:** `260619.82` (round 411 — **the tile dialect's menu takes the gold's ROW+COL tabs shell**"; assert s.count(old14) == 1
b14 = ("- **Build:** `260619.83` (round 412 — **the heading-then-table shape after an empty typed-widget invocation takes the owner form** (the writer's `[H3]` "
       "title, instruction paragraph and table after a bare `[drag and drop]` / `[Interactive activity]` / `[Activity 2C][drag and drop]` become the box's title, "
       "lead and widget data — the gold's `activity interactive` box + `<h3>` + the built widget on 15 / 17 = 0.88, 10 / 13 without the WJFUN intake family; "
       "`opener_rule.heading_table_owner` + `InteractiveScanner.#headingTableOwner`, env `HEADTABLE_OFF`); the autonomous loop's session 29 Round 3 — the "
       "r407-recorded follow-up, measured by `_s29_r3_headwalk.cjs` (31 bundles / 29 pages / 28 modules); the probe OFF = disk 2555 / 2555, ON 24 pages / 18 modules "
       "(14 up / 3 down, +32.6pp-sum, 0 outside the set); **SCOPED regeneration of the 18 (scoped ship #4 since the 19 Sept FULL)**; **ROUND 412 BASELINE: SCAFFOLD "
       "mean 53.809% / >=50% 1408 / >=75% 236 / >=90% 20 / RAW 37.970% @ 2349 pairs** (+0.0139pp; ≥50 +2); compare_structure 14174 / 186 / 690 / 23 (exact −1 = the "
       "matched pool −1, SCES201, named), body 54 / 6 / 190 / 248, clean 2504 / 2548, leak 73 / 44 — all EXACT; every verifier EXACT, 9 new 03B dragAndDrops "
       "(defect 0); 16 selftests GREEN; the miner 182 → 182; plateau window RESET (0 of 3)). Previous: ")
s = s.replace(old14, b14 + old14)
wr(p, s)

# ---------- 4. gate_baseline.json ----------
p = R + "CONVERTER_V2/reference/tests/gate_baseline.json"; s = rd(p)
def setv(key, old, new):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=1); assert n == 1, key
setv("build", '"260619.82"', '"260619.83"'); setv("round", 411, 412)
setv("mean_scaffold_pct", 53.79, 53.81)
setv("median_scaffold_pct", 54.6, 54.7)
setv("pages_ge_50", 1406, 1408)
setv("raw_mean_pct", 37.96, 37.97)
setv("exact_chain", 14175, 14174)
a = '    "_note_r411": "Round 411 (session 29 Round 2)'; assert s.count(a) == 1
s = s.replace(a, '    "_note_r412": "Round 412 (session 29 Round 3): the heading-then-table shape after an empty typed-widget invocation takes the owner form (opener_rule.heading_table_owner, env HEADTABLE_OFF; 18 modules / 24 pages; SCOPED regeneration of the 18; skeleton 53.7949 -> 53.8088, >=50 1406 -> 1408, RAW 37.963 -> 37.970; compare_structure exact 14175 -> 14174 = the matched pool 16470 -> 16469, SCES201 alone — the relocation class, accepted by name; every other gate EXACT).",\n' + a)
a2 = '    "_note_r410b": "Round 411: SCAFFOLD 53.7891'; assert s.count(a2) == 1
s = s.replace(a2, '    "_note_r411b": "Round 412: SCAFFOLD 53.7949 -> 53.8088 (+0.0139pp; 17 movers 14 up / 3 down — HPFUN201_0_0 -7.0 the family\'s un-boxed minority, TEDC401_2_0 -5.6 the gold\'s own box form with the hand-off dump inside, HES1002_5_0 -2.4 a mispaired page; 0 outside the 18-module affected set), >=50 1406 -> 1408 (TEFUN06_0_0, AGH1006_8_0), 236 / 20 EXACT, RAW 37.963 -> 37.970; 2349 pairs.",\n' + a2)
wr(p, s); json.load(open(p, encoding="utf-8"))
print("r412 finalise: changelog + Config.js 260619.83 + CLAUDE.md §9/§11/§14 + gate_baseline.json done")
