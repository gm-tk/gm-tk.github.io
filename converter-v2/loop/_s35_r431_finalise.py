#!/usr/bin/env python3
"""r431 finalise (OPERATING_GUIDE §12) — session 35 Round 2 (22 Sept 2026): changelog entry, Config.js 260620.03 -> 260620.04,
OPERATING_GUIDE §9 / §11 / §14, gate_baseline.json (round 431 — mean / >=50 / >=75 / RAW / exact / missing), the r359 data note
(the queued class is now measured and shipped), LOOP_STATE.md (Round-log line, the Position bullets — the IN-FLIGHT marker CLEARED —
plateau window RESET, standing facts, the next-session line; the Round 2 PICK section MOVED to the archive with the what-shipped record;
the follow-up lines), LOOP__Autonomous_Rounds.md §0 (the census-table build). Exact-text edits only; every anchor asserted.
Run under WSL: python3 _s35_r431_finalise.py
"""
import re, json
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
PF = R + "pageforge-site/converter-v2/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

entry = """## 2026-09-22 (round 431, build 260620.04) — THE OVERVIEW MENU'S INNER-WORD LABEL OVER-FIRE: a single-word section label ("do", "know", "understand") is a label at the START of a heading only, and the labels are tested against a punctuation-free fold — the loop's session 35 Round 2 (the miner's module-menu EXTRA rows #48 / #49; the r359 queued class measured and shipped)

### 1. WHAT CHANGED

**The class (the miner's module-menu lane — the chrome region's EXTRA rows #48 `div.col-12.col-md-8 › Claude h5` 81 pages / 25 modules and #49 `p`; authority §1b level 3, the gold's own menu region; the s35 census `outputs/_s35_r2_menuover.py` → `.log`: 56 pages / 34 modules carry menu-region text the paired GOLD keeps in its BODY).** Round 1's Inquiry census had left CEDO204's page-1 content (`Why do birds build nests?` … `How do spiders build webs?`) inside `div#module-menu-content`. The mechanism (`ContentConverter.#partitionItems`, the content-based overview fallback for a page with no `[MODULE INTRODUCTION]`): `matchesLabel` accepted a heading that CONTAINS a `menu.overview_section_labels` entry as an inner or trailing word — `f.includes(" " + l + " ")` / `f.endsWith(" " + l)` — so the SINGLE-WORD labels "do" / "know" / "understand" opened a menu section on every question heading and its block left the body (CEDO204, TWHK901's `Reflect: What can you do …`, CEDR302's `What do I know?`). The first repair (single-word labels at the start only) scored 8 up / 18 DOWN: the bilingual-pair headings `He aha tāku hei tīmata? | What do I need to get started?` had been caught ONLY by the inner-word "do" — the fold (`Utils.Fold`) keeps `?` / `|` / `.`, so no multi-word label ever matched them. The second repair tests every label against a PUNCTUATION-FREE fold as well (`he aha taku hei timata what do i need to get started`): a single-word label matches whole or at the start (the bilingual pairs match at the start through their Māori label — `hononga …`, `tirohanga whanui …`, `aromatawai …`), the multi-word labels keep the inner / trailing tests. That second form also lets the r359 colon forms (`Understand:` / `Know:` / `Do:`) match OUTSIDE the Inquiry family — exactly the class r359 queued with its own measurement ("the 12 Standard overviews": ANZH104 / XGF9004 gold-correct, the five TABS overviews ART1006 / HIS1007 / MXDI101 / MXEO201 / MXFL103, and the unpaired ENGR102 / HES1006 / HIS1002 / PES1005 / XDLS501) — now measured: every paired one UP except XGF9004 (named below).

**The fix.** `Emit_Templates.json` `menu.overview_section_labels_word_start` {enabled, env `MENUWORD_OFF`, min_words_for_inner 2}. `ContentConverter.#partitionItems`: `wsPlain(f)` (letters / digits / spaces only), `innerOk(l)` (a label of ≥ min_words_for_inner words keeps the inner / trailing tests); `matchesLabel` = whole / start on `f` or `fp`, inner / trailing on either for multi-word labels, the r359 colon forms unchanged.

**What it builds:** CEDO204's page-1 block back in the body (28.7 → 36.3); the curriculum block (`Understand / Know / Do` + their sentences) into the menu where the gold's menu holds it — COM1002 55.0 → 74.5, GEO1004 45.0 → 70.4, DAN1004 55.7 → 71.7, COM1005 54.1 → 67.9, ANZH104 60.6 → 71.6, COM1006 67.7 → 77.6, MXDI101 46.2 → 55.3, DAN1003 50.0 → 56.5, MXEO201 75.9 → 80.9, CBI1009 60.5 → 64.4, COM1002_1 43.8 → 47.5, ART1006 43.8 → 47.1, MXFL103 50.6 → 53.5, MUS1004 66.7 → 69.2, HIS1007 60.6 → 63.0; the r359 unpaired five change the same way (HES1006 / HIS1002 / PES1005's `_0_0` pages now PAIR — 69.6 / 56.0 / 78.3 — and their `_1_0` pairs drop, 65.1 / 37.5 / 78.4: the gate's pairing re-seated, pair count 2491 EXACT).

### 2. PROOF

- `_s35_r431_probe_run.sh` (all 545 modules, 4 shards; OFF = `MENUWORD_OFF=1`): **OFF = 2699 / 2699 identical, 0 changed**; **ON = exactly 23 modules / 23 pages** (every one an overview page — the content-based fallback's population), pre-scored with the gate's own `match()` (`_s35_r431_pagescore.log`, 19 paired): 16 up / 3 down, +121.8pp-sum SCAFFOLD / +70.4 RAW. The first repair's probe (8 up / 18 down, −57.5pp-sum) is the recorded measurement that found the punctuation cause.
- SCOPED regeneration (`_s35_r431_regen.sh`: the 23 + a 12-module spot-check sample seed 431, 35 / 35 fresh): `scoped_ship.sh --affected _affected_r431.txt --toggle MENUWORD_OFF --round 431 --no-regen --commit` — containment 23 ⊆ 23, spot-check 12 / 12 byte-identical, 0 truly stale, then **`compare_structure missing container 790 → 793 REGRESSED`** (`_s35_r431_scoped_ship.log`); decomposed (`_s35_r431_decomp.log`): the +3 are ENTIRELY TWHK901 (matched 63 → 69, exact 49 → 52, missing 13 → 16 — its page-1 `Whakataukī` / `We are learning to` / `You will show your understanding by` block, back in the body, now text-matches the gold, whose form wraps each panel's WALT block in a `div.alert` the WT never types: 16 of 63 Inquiry first panels carry that alert, the module's own form, under the floor); the r426 / HIS1005 precedent — the composition of NEWLY-matched elements — so `_fastloop_diff.py … --accept-named "compare_structure missing container" --commit` (`_s35_r431_fastloop_accept.log`): every other protected gate HELD or IMPROVED, the fast-loop baseline patched, the ledger scoped #6 since the intake FULL.
- `_s35_r431_postship.sh` (`_s35_r431_gates.log`): `run_all_gates.sh` rc 0 — skeleton state `_s35_r431_sk_final.json` **54.3617 → 54.4248 % @ 2491 pairs (+0.0630pp; 20 movers, 16 up / 4 down, +134.3pp-sum, 0 outside the set)**; ≥50 1537 → 1540, ≥75 254 → 255; RAW 38.227 → 38.294; every verifier RESULT ✓; 49 selftests PASS / 0 FAIL; the feature index GREEN; the DIFF MINER re-run 18:26 → 198 CANDIDATE (+2 rows to disposition).

### 3. PROTECTED GATES (all HELD or IMPROVED, the dips NAMED — `_s35_r431_gates.log`, `_s35_r431_scoped_ship.log`, `_s35_r431_fastloop_accept.log`, `_s35_r431_skdelta.log`)

- **Skeleton (PRIMARY)**: SCAFFOLD **54.4248 % @ 2491 pairs** (+0.0630pp; 16 up / 4 down — XGF9004 37.7 → 34.0 NAMED: its `Do:` block joins the menu where the gold's menu holds `Understand | Know | Do`, the body row that held it gone (gold-correct, the alignment scores it down); GEO1004_1_0 69.8 → 66.7 NAMED with its module companion GEO1004_0_0 45.0 → 70.4 (the pairing re-seated, the module +22.3 net); MUS1006_1_0 74.1 → 72.7 NAMED with RAW 61.3 → 69.7; TWHK901 −0.0); ≥50 **1540** (+3), ≥75 **255** (+1), ≥90 **23**, RAW **38.294 %** (+0.067); pairs skipped 0.
- **compare_structure** 15462 / 195 / 793 / 24 (exact +2, the matched pool 17968 → 17973; missing +3 = TWHK901's newly-matched WALT-alert elements, ACCEPTED AS NAMED); **body_compare** 56 / 5 / 203 / 262 EXACT; **defect** clean 2646 / 2691 = 98.33 %, leak 75 / 45 EXACT; tags 9557 / 9557; every verifier EXACT.
- Plateau (§4): the PICK predicted a skeleton move and delivered +0.0630pp with two other gates improving — the window RESETS to **0 of 3**.

"""
p = PF + "BUILD_CHANGELOG.md"; s = rd(p)
head, rest = s.split("\n", 1)
assert head.startswith("# BUILD CHANGELOG") and rest.lstrip("\n").startswith("## 2026-09-22 (round 430, build 260620.03)")
wr(p, head + "\n\n" + entry + rest.lstrip("\n"))

p = PF + "app/js/Config.js"; s = rd(p)
old = '\tstatic AppVersion = "260620.03";'; assert s.count(old) == 1
note = ("\t// ROUND 431 (260620.04): THE OVERVIEW MENU'S INNER-WORD LABEL OVER-FIRE — in the content-based overview fallback a single-word section label "
        "(do / know / understand) matches a heading only whole or at its start, and every label is tested against a punctuation-free fold too, so the "
        "bilingual-pair headings (He aha taku hei timata? | What do I need to get started?) match through their own labels instead of an accidental "
        "inner 'do' (menu.overview_section_labels_word_start; env MENUWORD_OFF). The loop's session 35 Round 2 (the miner's module-menu EXTRA rows #48 / "
        "#49; the r359 queued class of 12 Standard overviews measured and shipped): OFF probe 2699 / 2699 identical, ON = exactly 23 pages / 23 modules; "
        "scoped regeneration of the 23; skeleton 54.3617 -> 54.4248 % @ 2491 (+0.0630pp, 16 up / 4 down named), >=50 +3, >=75 +1, cs exact +2, missing "
        "+3 accepted as named (TWHK901's newly matched WALT-alert elements), every other gate EXACT.\n")
wr(p, s.replace(old, note + '\tstatic AppVersion = "260620.04";'))

p = PF + "OPERATING_GUIDE.md"; s = rd(p)
old9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 430 BASELINE ("; assert s.count(old9) == 1
new9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 431 BASELINE (the overview menu's inner-word label over-fire — `MENUWORD_OFF`; "
        "SCOPED regeneration of the 23, scoped ship #6 since the intake FULL): SCAFFOLD mean 54.4248% / >=50% 1540 / >=75% 255 / >=90% 23 / RAW 38.294% @ 2491 "
        "pairs, pairs skipped 0 — 16 up / 4 down (XGF9004 −3.7 the gold-correct Do block into the menu; GEO1004_1_0 −3.1 with page 0 +25.4, the pairing "
        "re-seated; MUS1006_1_0 −1.3 with RAW +8.5), +134.3pp-sum, 0 movers elsewhere; cs 15462 / 195 / 793 / 24 (exact +2; missing +3 = TWHK901's newly "
        "matched WALT-alert elements, accepted as named), body 56 / 5 / 203 / 262 EXACT, clean 2646 / 2691 = 98.33 %, leak 75 / 45 EXACT.** Previous — ROUND 430 BASELINE (")
s = s.replace(old9, new9)
old11 = "| `INQOPENER2_OFF` | 430 |"; assert s.count(old11) == 1
row11 = ("| `MENUWORD_OFF` | 431 | **THE OVERVIEW MENU'S INNER-WORD LABEL OVER-FIRE** (the autonomous loop's session 35 Round 2; the miner's module-menu EXTRA rows "
         "#48 h5 / #49 p; the s35 menu-overrun census 56 pages / 34 modules). `menu.overview_section_labels_word_start`: in `#partitionItems`' content-based "
         "overview fallback (no `[MODULE INTRODUCTION]`) a SINGLE-WORD `overview_section_labels` entry (\"do\" / \"know\" / \"understand\" …) matches a heading "
         "only whole or at its start — the inner-word test had read `Why do birds build nests?` (CEDO204), `Reflect: What can you do …` (TWHK901), `What do I "
         "know?` (CEDR302) as the Do / Know sections and moved page-1 blocks into the menu; every label is also tested against a PUNCTUATION-FREE fold, so the "
         "bilingual-pair headings (`He aha tāku hei tīmata? | What do I need to get started?`) match through their own labels (the fold keeps `?` / `|`, and "
         "only the accidental inner \"do\" had been catching them) — which also lets the r359 colon forms (`Understand:` / `Know:` / `Do:`) match outside the "
         "Inquiry family: the r359 queued class of 12 Standard overviews, now measured (ANZH104 +11.0, the five TABS overviews all up, XGF9004 −3.7 gold-correct). "
         "OFF probe 2699 / 2699 identical; ON exactly 23 pages / 23 modules; skeleton +0.0630pp (16 up / 4 down named), ≥50 +3, ≥75 +1, cs exact +2, missing +3 "
         "accepted as named (TWHK901's newly matched WALT-alert elements); every other gate EXACT. |\n")
s = s.replace(old11, row11 + old11)
old14 = "- **Build:** `260620.03` (round 430 — **THE INQUIRY PANEL OPENER ROBUSTNESS, PART 2**"; assert s.count(old14) == 1
b14 = ("- **Build:** `260620.04` (round 431 — **THE OVERVIEW MENU'S INNER-WORD LABEL OVER-FIRE** — `menu.overview_section_labels_word_start`, env `MENUWORD_OFF`; "
       "the autonomous loop's session 35 Round 2 (the miner's module-menu rows #48 / #49; the r359 queued class of 12 Standard overviews measured and shipped); "
       "OFF probe 2699 / 2699 identical, ON = exactly 23 pages / 23 modules; **SCOPED regeneration of the 23 (scoped ship #6 since the intake FULL)**; **ROUND 431 "
       "BASELINE: SCAFFOLD mean 54.4248% / >=50% 1540 / >=75% 255 / >=90% 23 / RAW 38.294% @ 2491 pairs** — +0.0630pp, 16 up / 4 down (named), +134.3pp-sum; cs "
       "15462 / 195 / 793 / 24 (exact +2, missing +3 accepted as named), body 56 / 5 / 203 / 262, clean 2646 / 2691, leak 75 / 45; every verifier EXACT; 49 "
       "selftest PASS; the miner 198; plateau window RESET to 0 of 3). Previous: ")
s = s.replace(old14, b14 + old14)
wr(p, s)

p = PF + "data/Emit_Templates.json"; s = rd(p)
o = '"_inquiry_only_note": "ROUND 359: true = only for a page the Inquiry family claims (menu.two_col_li.inquiry_family).'; assert s.count(o) == 1
s = s.replace(o, '"_inquiry_only_note": "ROUND 431: the queued class below is MEASURED and SHIPPED — overview_section_labels_word_start tests every label against a punctuation-free fold, so `Understand:` / `Know:` / `Do:` match everywhere regardless of this flag (ANZH104 +11.0, XGF9004 −3.7 gold-correct, the five TABS overviews ART1006 +3.2 / HIS1007 +2.4 / MXDI101 +9.2 / MXEO201 +5.0 / MXFL103 +2.9 — all UP; the unpaired five change the same way); this flag now only governs the literal colon forms on the raw fold. ROUND 359: true = only for a page the Inquiry family claims (menu.two_col_li.inquiry_family).')
json.loads(s); wr(p, s)

p = R + "CONVERTER_V2/reference/tests/gate_baseline.json"; s = rd(p)
def setv(key, old, new):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=1); assert n == 1, key
setv("build", '"260620.03"', '"260620.04"'); setv("round", 430, 431)
setv("mean_scaffold_pct", 54.36, 54.42); setv("raw_mean_pct", 38.23, 38.29)
setv("pages_ge_50", 1537, 1540); setv("pages_ge_75", 254, 255)
setv("exact_chain", 15460, 15462); setv("claude_missing_container", 790, 793)
a = '    "_note_r430": "Round 430 (session 35 Round 1, 2026-09-22; LOOP §1d exception 1'; assert s.count(a) == 1
s = s.replace(a, '    "_note_r431": "Round 431 (session 35 Round 2, 2026-09-22; the miner\'s module-menu EXTRA rows #48 / #49 — the r359 queued class measured): the overview menu\'s inner-word label over-fire — in the content-based overview fallback a single-word section label matches a heading whole or at its start only, every label is tested against a punctuation-free fold too (menu.overview_section_labels_word_start; env MENUWORD_OFF). OFF probe 2699 / 2699 identical, ON = exactly 23 pages / 23 modules; SCOPED regeneration of the 23 (scoped #6 since the intake FULL). Skeleton 54.3617 -> 54.4248 @ 2491 (+0.0630pp; 16 up / 4 down named: XGF9004 -3.7 gold-correct, GEO1004_1_0 -3.1 with page 0 +25.4, MUS1006_1_0 -1.3 with RAW +8.5), >=50 1537 -> 1540, >=75 254 -> 255, RAW 38.227 -> 38.294; cs exact 15460 -> 15462 (+2; the pool 17968 -> 17973), missing 790 -> 793 ACCEPTED AS NAMED (TWHK901 matched 63 -> 69 / exact 49 -> 52 / missing 13 -> 16 — the gold\'s per-panel WALT div.alert on newly matched elements), EXTRA / row-wrap, body, defect, leak, every verifier EXACT; the pairing re-seated on HES1006 / HIS1002 / PES1005 (_0_0 in, _1_0 out; 2491 pairs EXACT).",\n' + a)
a2 = '    "_note_r430": "Round 430: SCAFFOLD 54.3603 -> 54.3617'; assert s.count(a2) == 1
s = s.replace(a2, '    "_note_r431": "Round 431: SCAFFOLD 54.3617 -> 54.4248 @ 2491 pairs (+0.0630pp; GEO1004_0_0 45.0 -> 70.4, COM1002_0_0 55.0 -> 74.5, DAN1004 55.7 -> 71.7, COM1005 54.1 -> 67.9, ANZH104 60.6 -> 71.6, COM1006 67.7 -> 77.6, MXDI101 46.2 -> 55.3, CEDO204 28.7 -> 36.3, DAN1003 50.0 -> 56.5, MXEO201 75.9 -> 80.9, CBI1009 60.5 -> 64.4, COM1002_1_0 43.8 -> 47.5, ART1006 43.8 -> 47.1, MXFL103 50.6 -> 53.5, MUS1004 66.7 -> 69.2, HIS1007 60.6 -> 63.0; XGF9004 37.7 -> 34.0, GEO1004_1_0 69.8 -> 66.7, MUS1006_1_0 74.1 -> 72.7 named); >=50 1537 -> 1540 / >=75 254 -> 255 / >=90 23; RAW 38.227 -> 38.294. State outputs/_s35_r431_sk_final.json.",\n' + a2)
a3 = '    "_note_r430": "Round 430: exact 15442 -> 15460'; assert s.count(a3) == 1
s = s.replace(a3, '    "_note_r431": "Round 431: exact 15460 -> 15462 (+2), the matched pool 17968 -> 17973 (+5); missing 790 -> 793 ACCEPTED AS NAMED — entirely TWHK901 (matched +6 / exact +3 / missing +3: the gold wraps each panel\'s We-are-learning / You-will-show block in a div.alert the WT never types; 16 / 63 Inquiry first panels carry it — the module\'s own form, under the floor); EXTRA 195 / row-wrap 24 EXACT.",\n' + a3)
a4 = '    "_note_r430": "Round 430: over-capture 56'; assert s.count(a4) == 1
s = s.replace(a4, '    "_note_r431": "Round 431: over-capture 56 / runaway 5 / EMPTY 203 / ANY 262 EXACT on 2691 pages.",\n' + a4)
a5 = '    "_note_r430": "Round 430: clean 2646 / 2691'; assert s.count(a5) == 1
s = s.replace(a5, '    "_note_r431": "Round 431: clean 2646 / 2691 = 98.33, leak 75 occ / 45 pages EXACT.",\n' + a5)
json.loads(s); wr(p, s)

p = R + "LOOP__Autonomous_Rounds.md"; s = rd(p)
o = "Current (22 September 2026, build 260620.03 — after the 22 Sept Round 0d and r426–r430:"; assert s.count(o) == 1
s = s.replace(o, "Current (22 September 2026, build 260620.04 — after the 22 Sept Round 0d and r426–r431:")
wr(p, s)

st = rd(R + "LOOP_STATE.md")
o = "- s35-r1 (engine r430, build 260620.03"; assert st.count(o) == 1
line = ("- s35-r2 (engine r431, build 260620.04, 22 Sept ≈17:56 → ≈18:40) · THE OVERVIEW MENU'S INNER-WORD LABEL OVER-FIRE (the miner's module-menu EXTRA rows "
        "#48 / #49; the r359 queued class of 12 Standard overviews measured and shipped) — in the content-based overview fallback a single-word section label "
        "(\"do\" / \"know\" / \"understand\") matches a heading whole or at its start only, and every label is tested against a punctuation-free fold "
        "(`MENUWORD_OFF`) · OFF probe 2699 / 2699 identical · ON exactly 23 pages / 23 modules · the first repair's probe 8 up / 18 DOWN found the punctuation "
        "cause · SCOPED regen of the 23 (scoped #6) · skeleton 54.3617 → 54.4248 % @ 2491 (+0.0630pp; 16 up / 4 down NAMED — XGF9004 −3.7 gold-correct, "
        "GEO1004_1_0 −3.1 with page 0 +25.4, MUS1006_1_0 −1.3 with RAW +8.5), ≥50 +3, ≥75 +1, cs exact +2, missing +3 ACCEPTED AS NAMED (TWHK901's newly "
        "matched WALT-alert elements — the r426 / HIS1005 precedent), all else EXACT · plateau window RESET to 0 of 3\n")
st = st.replace(o, line + o)
o = "- Every shipped round r314–r430 is ONE line"; assert st.count(o) == 1
st = st.replace(o, "- Every shipped round r314–r431 is ONE line")
o = "`DIFF_QUEUE.md` 22 Sept 17:43 on the r430 corpus (2,491 pairs / 533 modules), 196 CANDIDATE rows"; assert st.count(o) == 1
st = st.replace(o, "`DIFF_QUEUE.md` 22 Sept 18:26 on the r431 corpus (2,491 pairs / 533 modules), 198 CANDIDATE rows")
lines = st.split("\n")
idx = [i for i, l in enumerate(lines) if l.startswith("- **ROUND 431 IN FLIGHT — NOT PROVEN**")]
assert len(idx) == 1
lines[idx[0]] = ("- **No round in flight** (22 Sept 2026 ≈18:40, session 35 Round 2: r431 SHIPPED and committed; the corpus on disk IS the r431 state; the r431 "
                 "record is in LOOP_STATE_ARCHIVE.md 'Session 35 — Round 2 (engine r431 …)'). The §3 step-1 rule stands: the next PICK raises "
                 "`ROUND <N> IN FLIGHT — NOT PROVEN` here BEFORE any code is edited.")
st = "\n".join(lines)
o = "- LAST SHIPPED: **r430** (build 260620.03, 22 Sept ≈17:55, session 35 Round 1 — "; assert st.count(o) == 1
st = st.replace(o, ("- LAST SHIPPED: **r431** (build 260620.04, 22 Sept ≈18:40, session 35 Round 2 — the overview menu's inner-word label over-fire, `MENUWORD_OFF`; "
                    "SCOPED regeneration of the 23, scoped #6 since the intake FULL (2 of headroom); **skeleton 54.4248 % @ 2491, ≥50 1540, ≥75 255, ≥90 23, RAW "
                    "38.294 %** (+0.0630pp, 16 up / 4 down named); cs 15462 / 195 / 793 / 24 (missing +3 accepted as named); body 56 / 5 / 203 / 262; clean 2646 / "
                    "2691 = 98.33 %; leak 75 / 45; `gate_baseline.json` at r431 (`_note_r431`); `outputs/_s35_r431_sk_final.json` the skeleton state; 54.425 / 91.2 = "
                    "**59.7 % of achievable**; the miner re-run 22 Sept 18:26, 198 CANDIDATE; corpus 2699 pages / 545 dirs / 2491 pairs). Before it **r430** (build "
                    "260620.03, 22 Sept ≈17:55, session 35 Round 1 — "))
o = "- Plateau window (§4): **1 of 3** — r430 predicted a skeleton move and delivered +0.0015pp BUT two other protected gates moved (≥50 +1, cs exact +18: neither counts nor resets);"; assert st.count(o) == 1
st = st.replace(o, "- Plateau window (§4): **0 of 3** — r431 predicted a skeleton move and delivered +0.0630pp (the window RESETS); r430 predicted a skeleton move and delivered +0.0015pp BUT two other protected gates moved (≥50 +1, cs exact +18: neither counts nor resets);")
o = "- Standing facts: AppVersion 260620.03 (r430 the Inquiry panel opener robustness part 2, session 35 Round 1, 22 Sept); before it"; assert st.count(o) == 1
st = st.replace(o, "- Standing facts: AppVersion 260620.04 (r431 the overview menu's inner-word label over-fire, session 35 Round 2, 22 Sept); before it 260620.03 (r430 the Inquiry panel opener robustness part 2, session 35 Round 1, 22 Sept); before it")
i0 = st.index("## Session 35 — Round 2 (engine r431) — THE OVERVIEW MENU'S INNER-WORD LABEL OVER-FIRE")
i1 = st.index("## Session 35 — Round 1 (engine r430, build 260620.03) — THE INQUIRY PANEL OPENER ROBUSTNESS, PART 2 — SHIPPED;")
r2 = st[i0:i1]
pointer = ("## Session 35 — Round 2 (engine r431, build 260620.04) — THE OVERVIEW MENU'S INNER-WORD LABEL OVER-FIRE — SHIPPED; the PICK + what-shipped record is in "
           "LOOP_STATE_ARCHIVE.md 'Session 35 — Round 2 (engine r431 …) + what shipped'; the one-line summary is the s35-r2 Round-log line below.\n\n")
st = st[:i0] + pointer + st[i1:]
shipped = """**WHAT SHIPPED (22 Sept ≈17:56 → ≈18:40).** `Emit_Templates.json` `menu.overview_section_labels_word_start` {enabled, env `MENUWORD_OFF`, min_words_for_inner 2} (+ the r359 `_inquiry_only_note` updated: its queued class measured and shipped). `ContentConverter.#partitionItems`: `wsPlain(f)` — the heading's fold with everything but letters / digits / spaces stripped; `innerOk(l)` — a label of ≥ min_words_for_inner words keeps the inner / trailing tests; `matchesLabel` = whole / start on `f` or the plain fold, inner / trailing on either for multi-word labels only, the r359 colon forms unchanged. Two repairs inside the round: the first (single-word labels at the start only, the raw fold) probed 8 up / 18 DOWN (`_s35_r431_pagescore.log`'s first run: CBI1009 −12.1, DAN1004 −8.9, HIS1007 −8.8, MXEO201 −8.2 — every one lost `He aha tāku hei tīmata? | What do I need to get started?`, which only the inner-word "do" had been catching because the fold keeps `?` / `|`); the second (the punctuation-free fold) probed 16 up / 3 down, +121.8pp-sum. Probe OFF = 2699 / 2699 identical; ON = exactly 23 modules / 23 pages (`_s35_r431_probe_run.sh`). `_s35_r431_regen.sh` (the 23 + 12 spot-checks seed 431, 35 / 35 fresh); `scoped_ship.sh … --round 431 --commit` FAILED on `compare_structure missing container 790 → 793`; `_s35_r431_decomp.py`: the +3 entirely TWHK901 (matched 63 → 69, exact 49 → 52, missing 13 → 16 — the gold's per-panel `div.alert` around the WALT block, 16 / 63 Inquiry first panels, the module's own form); `_fastloop_diff.py … --accept-named "compare_structure missing container" --commit` (the r426 / HIS1005 precedent) PASS. `_s35_r431_postship.sh`: `run_all_gates.sh` rc 0 — **skeleton 54.3617 → 54.4248 % @ 2491 (+0.0630pp; 20 movers, 16 up / 4 down, +134.3pp-sum; 0 outside the set)**; ≥50 1537 → 1540; ≥75 254 → 255; ≥90 23; RAW 38.227 → 38.294; cs 15460 → 15462 exact (+2; the pool +5), 195 / 793 / 24; body 56 / 5 / 203 / 262 EXACT; clean 2646 / 2691; leak 75 / 45; every verifier ✓; 49 selftest PASS / 0 FAIL; feature index GREEN; the ledger scoped #6 since the intake FULL (2 of headroom); the miner 18:26 → 198 CANDIDATE. The pairing re-seated on the r359 unpaired five: HES1006 / HIS1002 / PES1005's `_0_0` pages now pair (69.6 / 56.0 / 78.3) and their `_1_0` pairs drop (65.1 / 37.5 / 78.4); GEO1004's pair re-seated (page 0 +25.4, page 1 −3.1). Finalise: `_s35_r431_finalise.py` (the changelog entry, Config.js 260620.04, OPERATING_GUIDE §9 / §11 / §14, gate_baseline.json `_note_r431`, the r359 data note, LOOP_STATE.md, the loop file §0 build), the checksum manifests, the mirror.
"""
ar = rd(R + "LOOP_STATE_ARCHIVE.md")
assert "## Session 35 — Round 2 (engine r431" not in ar
r2_head = "## Session 35 — Round 2 (engine r431, build 260620.04, 22 Sept ≈17:56 → ≈18:40) — THE OVERVIEW MENU'S INNER-WORD LABEL OVER-FIRE + what shipped\n\n"
r2_body = r2.split("\n", 1)[1].strip("\n")
wr(R + "LOOP_STATE_ARCHIVE.md", ar.rstrip("\n") + "\n\n" + r2_head + r2_body + "\n\n" + shipped)
o = "- **(r430) The remaining Inquiry PANELS-DIFF residue, one module each"; assert st.count(o) == 1
st = st.replace(o, ("- **(r431) The menu-overrun residue (`_s35_r2_menuover.log`, 56 pages / 34 modules before r431):** MXFUN03 (32 elements) / CHFUN05 (31) — Fundamentals "
                    "single pages whose `module-menu-content` holds body content through a different mechanism (a tabs widget inside the menu; a `[Lesson Overview]` "
                    "page family); ENGJ201 (14 over 6 pages); CEDR302's remaining 24 (the KWL `What do I know? / What do I want to know?` headings — the gold's body); "
                    "TWHK901's per-panel WALT `div.alert` (16 / 63 Inquiry first panels — the module's own form, under the floor). Re-run the census on the r431 "
                    "corpus before any pick.\n" + o))
i = st.rfind("**Next session starts with:**"); assert i > 0
st = st[:i] + ("**Next session starts with:** the standing `/loop-start` (health check — the census is 552 gold / 545 Claude dirs / 2,699 Claude pages; the \"Amended:\" line; "
               "the §7 diff check; `git status` CLEAN at the session-35 commits). No round in flight (r431 shipped by session 35 Round 2 — see the Position section). "
               "Session 35 continues after r431 with the lanes (the miner's 198 rows — two new since r430 — re-read on the r431 corpus; the menu-overrun census re-run; "
               "the KB queue; the widget census; the loss ledger); if it stops on §4, its STOPPED entry above names the lanes. NEEDS CHRIS: the open lines of the "
               "\"Needs Chris\" section.\n")
wr(R + "LOOP_STATE.md", st)
print("finalise OK")
