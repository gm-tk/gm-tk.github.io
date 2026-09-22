#!/usr/bin/env python3
"""r432 finalise (OPERATING_GUIDE §12) — session 35 Round 3 (22 Sept 2026): changelog entry, Config.js 260620.04 -> 260620.05,
OPERATING_GUIDE §9 / §11 / §14, gate_baseline.json (round 432 — mean / >=50 / >=75 / RAW / any_breakdown), LOOP_STATE.md (Round-log
line, the Position bullets — the IN-FLIGHT marker CLEARED — plateau window, standing facts, the next-session line; the Round 3 PICK
section MOVED to the archive with the what-shipped record; the follow-up lines), LOOP__Autonomous_Rounds.md §0 (the census-table build).
Exact-text edits only; every anchor asserted. Run under WSL: python3 _s35_r432_finalise.py
"""
import re, json
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
PF = R + "pageforge-site/converter-v2/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

entry = """## 2026-09-22 (round 432, build 260620.05) — THE LESSON PAGE'S UNMARKED WALT / SC BLOCK IS ITS MENU: an `[Overview]`-marked or bare "We are learning / You will show your understanding by" block at the lesson's start routes to the lesson menu — the loop's session 35 Round 3 (the module-menu chrome region; KB 01B; the gold at 0.97)

### 1. WHAT CHANGED

**The class (the module-menu chrome region; authority §1b level 1 — KB 01B "Lesson Pages — Simplified Module Menu": the lesson page's menu IS its WALT / SC block with `<h5>` labels, canonical whatever the writer's wording).** The mirror of r431's census — gold MENU text (≥ 40 chars) that Claude keeps in its BODY (`outputs/_s35_r3_menuunder.py`): 124 pages / 50 modules / 460 elements, concentrated on the LESSON pages of multi-page modules; `_s35_r3_lessonmenu.py` (104 lesson pages / 30 modules; Claude's menu region EMPTY on 103 of them) and `_s35_r3_waltmenu.py` — the gold's convention over EVERY paired lesson page carrying a WALT / SC lead element ("we are learning", "learning intentions", "you will show your understanding", "how will i know", "i can", "success criteria"): **gold MENU 1,258 pages vs gold BODY-only 38 (0.97; every prefix ≥ 0.79 menu except TRR 1.00 body, XGF 0.64, HPRE 0.53 + 0.47 both)**; Claude: menu 810 (the `[Lesson Overview]` path), none 347 (the human's own LI — the ceiling), BODY 95 pages / 36 modules (+41 gold-both). Triangulated: TEDC402 lesson 1 `[LESSON 1]` + `[H1]` + `[Overview]` + a 2-row layout TABLE; FRNO901 lesson 1 `[LESSON]` + `[Lesson content]` + `[H2] Lesson 1 – …` + `[body text]` + bare `We are learning:` + bullets; PES1004 lesson 2 `[H1] LESSON No. 2 …` + bare `We are learning about:`. `ContentConverter.#partitionItems` routed a lesson's menu only from a `[Lesson Overview]` marker (or the r148 bare red lead).

**The fix.** `Emit_Templates.json` `menu.lesson_overview_implicit` {enabled, env `LESSONWALT_OFF`, alias_words [overview], lead_pattern, max_scan_items 14, opening_tags}. `#partitionItems`: on a LESSON page with a menu and no `[Lesson Overview]` marker, (a) an EMPTY `[Overview]` title-bar alias among the opening items is the marker (consumed — never the page title) when the block after it qualifies; else (b) the first LEAD item (a black line or a body / heading tag whose first line starts with the lead pattern and is ≤ lead_max_words 8 words — a prose sentence never qualifies) reached through opening items only (blank lines, instructions, the title bar / lesson heading, `[Lesson content]`, an empty body tag) starts the block; the block is bounded BY THE RULE (`loiSet`): blank lines, lead lines, list lines (`•` / `-` / `1.` / `a)`), black runs of only those, `list` tags, and heading / body tags whose own text is a lead — a prose line or any other structural item ends it; it fires only when the block holds ≥ 1 lead AND ≥ 1 list line; the set replaces the generic section-stop and bounds `lessonMenuEnd`; `overviewIdx` becomes the item before the lead (never skipped) so the lesson heading stays in the body. MenuBuilder's simplified lesson menu renders the block exactly as the marked form (the lead → the canonical `<h5>`, the bullets → the list). Two repairs inside the round, both caught by the probe: the first draft's generic section-stop dragged the following prose paragraph into the menu (ENGC206's `Welcome! In this lesson …`) and read a prose sentence as a lead (COM1006's `We are learning what an event is. You will show …`, 14 words) and consumed a prose-tailed `[overview] Investigate results …` alias (MXFU202) — 47 up / 12 down; the refined rule 49 up / 1 down.

**What it builds:** FRNO901_8_0 58.7 → 70.8, PES1004_2_0 51.8 → 65.9, TEDC402_9_0 30.8 → 42.7, FRNO901_7_0 61.3 → 71.6, PWY1001_2_1_0 44.2 → 54.4, PES1002_8_0 52.1 → 62.2, PES1004_6_0 54.7 → 64.7, CEDT501_6_0 50.5 → 60.2 … (ENGC206_1_0's ON menu = the gold's `<h5>We are learning:</h5><ul>…</ul><h5>I can:</h5><ul>…</ul>` byte for byte). The TEDC401 / TEDC402 lessons whose block sits INSIDE the layout table stay a recorded follow-up (the table is not a block member).

### 2. PROOF

- `_s35_r432_probe_run.sh` (all 545 modules, 4 shards; OFF = `LESSONWALT_OFF=1`): **OFF = 2699 / 2699 identical, 0 changed**; **ON = exactly 15 modules / 50 paired pages**, pre-scored with the gate's own `match()` (`_s35_r432_pagescore.log`): **49 up / 1 down** (CEDK501_8_0 −2.6 — the gate pairs Claude's `_8_0` with the gold's `_0.0` on this dual-build module, the Needs Chris #6 family; CEDK's convention is 1.00 menu), +254.8pp-sum SCAFFOLD / +159.0 RAW.
- SCOPED regeneration (`_s35_r432_regen.sh`: the 15 + a 12-module spot-check sample seed 432, 27 / 27 fresh): `scoped_ship.sh --affected _affected_r432.txt --toggle LESSONWALT_OFF --round 432 --no-regen --commit` — containment 15 ⊆ 15, spot-check 12 / 12 byte-identical, 0 truly stale, then **`body_compare ANY breakdown 262 → 264 REGRESSED`** (`_s35_r432_scoped_ship.log`); decomposed against `reference/tests/body_compare.json`: the +2 are ENGI301_1_0 (over-capture 0.73 → 0.76, biggest widget 3047 chars UNCHANGED, one clickDrop; Claude's free blocks 7 → 3 as the WALT block left the body, so `lost_blocks` −1 → 3 crosses the flag's ≥ 3 threshold) and GEO1005_6_0 (0.43 → 0.44, 1845 chars UNCHANGED, one tabs bundle; free blocks 13 → 11, lost 1 → 3) — a pre-existing over-capture on each page that the WALT block's presence in the body had MASKED, exposed by the correct move, the widget capture byte-identical — so `_fastloop_diff.py … --accept-named "body_compare ANY breakdown" --commit` (`_s35_r432_fastloop_accept.log`; the r426 / r431 precedent): every other protected gate HELD or IMPROVED, the fast-loop baseline patched, the ledger scoped #7 since the intake FULL (1 of headroom — the FULL backstop is due at #8).
- `_s35_r432_postship.sh` (`_s35_r432_gates.log`): `run_all_gates.sh` rc 0 — skeleton state `_s35_r432_sk_final.json` **54.4248 → 54.5220 % @ 2491 pairs (+0.0972pp; 50 movers, 49 up / 1 down, +254.8pp-sum, 0 outside the set)**; ≥50 1540 → 1546, ≥75 255 → 256; RAW 38.294 → 38.358; every verifier RESULT ✓; 49 selftests PASS / 0 FAIL; the feature index GREEN; the DIFF MINER re-run 19:24 → 198 CANDIDATE. The pairing re-seated one PWY1001 pair (`PWY1001_1_0` in at 37.4, `PWY1001_2_2_0` out at 50.0; 2491 pairs EXACT).

### 3. PROTECTED GATES (all HELD or IMPROVED, the dips NAMED — `_s35_r432_gates.log`, `_s35_r432_scoped_ship.log`, `_s35_r432_fastloop_accept.log`, `_s35_r432_skdelta.log`)

- **Skeleton (PRIMARY)**: SCAFFOLD **54.5220 % @ 2491 pairs** (+0.0972pp; 49 up / 1 down — CEDK501_8_0 45.3 → 42.7 NAMED, the scrambled dual-build pairing; the PWY1001 pair swap NAMED); ≥50 **1546** (+6), ≥75 **256** (+1), ≥90 **23**, RAW **38.358 %** (+0.064); pairs skipped 0.
- **compare_structure** 15462 / 195 / 793 / 24 EXACT (the matched pool 17973 EXACT); **body_compare** 58 / 5 / 203 / **264** (ANY +2 = ENGI301_1_0 / GEO1005_6_0's pre-existing over-capture exposed, widget capture byte-identical — ACCEPTED AS NAMED); **defect** clean 2646 / 2691 = 98.33 %, leak 75 / 45 EXACT; tags 9557 / 9557; every verifier EXACT.
- Plateau (§4): the PICK predicted a skeleton move and delivered +0.0972pp — the window stays **0 of 3**.

"""
p = PF + "BUILD_CHANGELOG.md"; s = rd(p)
head, rest = s.split("\n", 1)
assert head.startswith("# BUILD CHANGELOG") and rest.lstrip("\n").startswith("## 2026-09-22 (round 431, build 260620.04)")
wr(p, head + "\n\n" + entry + rest.lstrip("\n"))

p = PF + "app/js/Config.js"; s = rd(p)
old = '\tstatic AppVersion = "260620.04";'; assert s.count(old) == 1
note = ("\t// ROUND 432 (260620.05): THE LESSON PAGE'S UNMARKED WALT / SC BLOCK IS ITS MENU — on a lesson page with no [Lesson Overview] marker an EMPTY "
        "[Overview] alias among the opening items, or a short 'We are learning / You will show / I can' lead reached through opening items only, starts the "
        "lesson's overview block (lead + list lines, bounded by the rule; a prose line ends it), which routes to the simplified lesson menu exactly as the "
        "marked form (menu.lesson_overview_implicit; env LESSONWALT_OFF). KB 01B; the gold's menu holds the block on 1,258 lesson pages vs its body alone on "
        "38. The loop's session 35 Round 3: OFF probe 2699 / 2699 identical, ON = exactly 15 modules / 50 paired pages (49 up / 1 down named); scoped "
        "regeneration of the 15; skeleton 54.4248 -> 54.5220 % @ 2491 (+0.0972pp), >=50 +6, >=75 +1, body ANY +2 accepted as named (a pre-existing "
        "over-capture exposed on ENGI301_1_0 / GEO1005_6_0, widget capture byte-identical), every other gate EXACT.\n")
wr(p, s.replace(old, note + '\tstatic AppVersion = "260620.05";'))

p = PF + "OPERATING_GUIDE.md"; s = rd(p)
old9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 431 BASELINE ("; assert s.count(old9) == 1
new9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 432 BASELINE (the lesson page's unmarked WALT / SC block is its menu — `LESSONWALT_OFF`; "
        "SCOPED regeneration of the 15, scoped ship #7 since the intake FULL): SCAFFOLD mean 54.5220% / >=50% 1546 / >=75% 256 / >=90% 23 / RAW 38.358% @ 2491 "
        "pairs, pairs skipped 0 — 49 up / 1 down (CEDK501_8_0 −2.6 named, the scrambled dual-build pairing), +254.8pp-sum, 0 movers elsewhere; cs 15462 / 195 / 793 / "
        "24 EXACT, body 58 / 5 / 203 / 264 (ANY +2 accepted as named — ENGI301_1_0 / GEO1005_6_0's pre-existing over-capture exposed), clean 2646 / 2691 = 98.33 %, "
        "leak 75 / 45 EXACT.** Previous — ROUND 431 BASELINE (")
s = s.replace(old9, new9)
old11 = "| `MENUWORD_OFF` | 431 |"; assert s.count(old11) == 1
row11 = ("| `LESSONWALT_OFF` | 432 | **THE LESSON PAGE'S UNMARKED WALT / SC BLOCK IS ITS MENU** (the autonomous loop's session 35 Round 3; the module-menu chrome "
         "region; KB 01B 'Lesson Pages — Simplified Module Menu'; the gold's menu holds the block on 1,258 lesson pages vs its body alone on 38 = 0.97). "
         "`menu.lesson_overview_implicit`: in `#partitionItems`, on a LESSON page with a menu and no `[Lesson Overview]` marker, (a) an EMPTY `[Overview]` "
         "title-bar alias among the opening items is the marker (consumed, never the page title) when a qualifying block follows; else (b) the first lead item "
         "(a black line or a body / heading tag whose first line starts with the lead pattern and is ≤ 8 words) reached through opening items only starts the "
         "block; the block = blank / lead / list lines, `list` tags and lead-titled heading / body tags, bounded by the rule (a prose line ends it), and fires only "
         "with ≥ 1 lead AND ≥ 1 list line; `overviewIdx` = the item before the lead (never skipped). MenuBuilder renders it as the marked form. Recorded follow-up: "
         "the TEDC401 / TEDC402 lessons whose block sits inside a 2-row layout table. OFF probe 2699 / 2699 identical; ON exactly 15 modules / 50 paired pages; "
         "skeleton +0.0972pp (49 up / 1 down named), ≥50 +6, ≥75 +1; body ANY +2 accepted as named; every other gate EXACT. |\n")
s = s.replace(old11, row11 + old11)
old14 = "- **Build:** `260620.04` (round 431 — **THE OVERVIEW MENU'S INNER-WORD LABEL OVER-FIRE**"; assert s.count(old14) == 1
b14 = ("- **Build:** `260620.05` (round 432 — **THE LESSON PAGE'S UNMARKED WALT / SC BLOCK IS ITS MENU** — `menu.lesson_overview_implicit`, env `LESSONWALT_OFF`; "
       "the autonomous loop's session 35 Round 3 (KB 01B; the gold 0.97); OFF probe 2699 / 2699 identical, ON = exactly 15 modules / 50 paired pages; **SCOPED "
       "regeneration of the 15 (scoped ship #7 since the intake FULL — the FULL backstop is due at #8)**; **ROUND 432 BASELINE: SCAFFOLD mean 54.5220% / >=50% 1546 / "
       ">=75% 256 / >=90% 23 / RAW 38.358% @ 2491 pairs** — +0.0972pp, 49 up / 1 down (named), +254.8pp-sum; cs 15462 / 195 / 793 / 24 EXACT, body 58 / 5 / 203 / 264 "
       "(ANY +2 accepted as named), clean 2646 / 2691, leak 75 / 45; every verifier EXACT; 49 selftest PASS; the miner 198; plateau window 0 of 3). Previous: ")
s = s.replace(old14, b14 + old14)
wr(p, s)

p = R + "CONVERTER_V2/reference/tests/gate_baseline.json"; s = rd(p)
def setv(key, old, new):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=1); assert n == 1, key
setv("build", '"260620.04"', '"260620.05"'); setv("round", 431, 432)
setv("mean_scaffold_pct", 54.42, 54.52); setv("raw_mean_pct", 38.29, 38.36)
setv("pages_ge_50", 1540, 1546); setv("pages_ge_75", 255, 256); setv("any_breakdown", 262, 264)
a = '    "_note_r431": "Round 431 (session 35 Round 2, 2026-09-22; the miner\'s module-menu EXTRA rows #48 / #49'; assert s.count(a) == 1
s = s.replace(a, '    "_note_r432": "Round 432 (session 35 Round 3, 2026-09-22; the module-menu chrome region, KB 01B): the lesson page\'s unmarked WALT / SC block is its menu — an EMPTY [Overview] alias or a short lead (\'We are learning\' / \'You will show\' / \'I can\', <= 8 words) at the lesson\'s start routes the lead + list block to the simplified lesson menu (menu.lesson_overview_implicit; env LESSONWALT_OFF). OFF probe 2699 / 2699 identical, ON = exactly 15 modules / 50 paired pages; SCOPED regeneration of the 15 (scoped #7 since the intake FULL). Skeleton 54.4248 -> 54.5220 @ 2491 (+0.0972pp; 49 up / 1 down — CEDK501_8_0 -2.6 named, the scrambled dual-build pairing), >=50 1540 -> 1546, >=75 255 -> 256, RAW 38.294 -> 38.358; cs EXACT; body ANY 262 -> 264 ACCEPTED AS NAMED (ENGI301_1_0 / GEO1005_6_0: the widget capture byte-identical, Claude\'s free-body blocks fell as the WALT block left the body, so a pre-existing over-capture crossed the lost_blocks >= 3 threshold); defect, leak, every verifier EXACT; one PWY1001 pair re-seated (2491 pairs EXACT).",\n' + a)
a2 = '    "_note_r431": "Round 431: SCAFFOLD 54.3617 -> 54.4248'; assert s.count(a2) == 1
s = s.replace(a2, '    "_note_r432": "Round 432: SCAFFOLD 54.4248 -> 54.5220 @ 2491 pairs (+0.0972pp; PES1004_2_0 51.8 -> 65.9, FRNO901_8_0 58.7 -> 70.8, TEDC402_9_0 30.8 -> 42.7, FRNO901_7_0 61.3 -> 71.6, PWY1001_2_1_0 44.2 -> 54.4, PES1002_8_0 52.1 -> 62.2, PES1004_6_0 54.7 -> 64.7, CEDT501_6_0 50.5 -> 60.2 ... 49 up; CEDK501_8_0 45.3 -> 42.7 named); >=50 1540 -> 1546 / >=75 255 -> 256 / >=90 23; RAW 38.294 -> 38.358. State outputs/_s35_r432_sk_final.json.",\n' + a2)
a4 = '    "_note_r431": "Round 431: over-capture 56'; assert s.count(a4) == 1
s = s.replace(a4, '    "_note_r432": "Round 432: over-capture 56 -> 58 / runaway 5 / EMPTY 203 / ANY 262 -> 264 on 2691 pages — ACCEPTED AS NAMED: ENGI301_1_0 (0.73 -> 0.76, the clickDrop 3047 chars unchanged, free blocks 7 -> 3) and GEO1005_6_0 (0.43 -> 0.44, the tabs bundle 1845 chars unchanged, free blocks 13 -> 11): the WALT block moved to the menu, so the pre-existing over-capture crossed lost_blocks >= 3.",\n' + a4)
a5 = '    "_note_r431": "Round 431: clean 2646 / 2691'; assert s.count(a5) == 1
s = s.replace(a5, '    "_note_r432": "Round 432: clean 2646 / 2691 = 98.33, leak 75 occ / 45 pages EXACT.",\n' + a5)
a3 = '    "_note_r431": "Round 431: exact 15460 -> 15462'; assert s.count(a3) == 1
s = s.replace(a3, '    "_note_r432": "Round 432: exact 15462 / EXTRA 195 / missing 793 / row-wrap 24 EXACT; the matched pool 17973 EXACT.",\n' + a3)
json.loads(s); wr(p, s)

p = R + "LOOP__Autonomous_Rounds.md"; s = rd(p)
o = "Current (22 September 2026, build 260620.04 — after the 22 Sept Round 0d and r426–r431:"; assert s.count(o) == 1
s = s.replace(o, "Current (22 September 2026, build 260620.05 — after the 22 Sept Round 0d and r426–r432:")
wr(p, s)

st = rd(R + "LOOP_STATE.md")
o = "- s35-r2 (engine r431, build 260620.04"; assert st.count(o) == 1
line = ("- s35-r3 (engine r432, build 260620.05, 22 Sept ≈18:38 → ≈19:30) · THE LESSON PAGE'S UNMARKED WALT / SC BLOCK IS ITS MENU (the module-menu chrome region; "
        "KB 01B; the gold 1,258 menu vs 38 body = 0.97) — an EMPTY `[Overview]` alias or a short lead at the lesson's start routes the lead + list block to the "
        "simplified lesson menu (`LESSONWALT_OFF`) · OFF probe 2699 / 2699 identical · ON exactly 15 modules / 50 paired pages (two in-round repairs: the prose "
        "paragraph, the prose lead, the prose-tailed alias) · SCOPED regen of the 15 (scoped #7 — the FULL backstop is due at #8) · skeleton 54.4248 → 54.5220 % "
        "@ 2491 (+0.0972pp; 49 up / 1 down NAMED — CEDK501_8_0 −2.6, the scrambled dual-build pairing), ≥50 +6, ≥75 +1, cs EXACT, body ANY +2 ACCEPTED AS NAMED "
        "(ENGI301_1_0 / GEO1005_6_0's pre-existing over-capture exposed, the widget capture byte-identical), all else EXACT · plateau window 0 of 3\n")
st = st.replace(o, line + o)
o = "- Every shipped round r314–r431 is ONE line"; assert st.count(o) == 1
st = st.replace(o, "- Every shipped round r314–r432 is ONE line")
o = "`DIFF_QUEUE.md` 22 Sept 18:26 on the r431 corpus (2,491 pairs / 533 modules), 198 CANDIDATE rows"; assert st.count(o) == 1
st = st.replace(o, "`DIFF_QUEUE.md` 22 Sept 19:24 on the r432 corpus (2,491 pairs / 533 modules), 198 CANDIDATE rows")
lines = st.split("\n")
idx = [i for i, l in enumerate(lines) if l.startswith("- **ROUND 432 IN FLIGHT — NOT PROVEN**")]
assert len(idx) == 1
lines[idx[0]] = ("- **No round in flight** (22 Sept 2026 ≈19:30, session 35 Round 3: r432 SHIPPED and committed; the corpus on disk IS the r432 state; the r432 "
                 "record is in LOOP_STATE_ARCHIVE.md 'Session 35 — Round 3 (engine r432 …)'). The §3 step-1 rule stands: the next PICK raises "
                 "`ROUND <N> IN FLIGHT — NOT PROVEN` here BEFORE any code is edited.")
st = "\n".join(lines)
o = "- LAST SHIPPED: **r431** (build 260620.04, 22 Sept ≈18:40, session 35 Round 2 — "; assert st.count(o) == 1
st = st.replace(o, ("- LAST SHIPPED: **r432** (build 260620.05, 22 Sept ≈19:30, session 35 Round 3 — the lesson page's unmarked WALT / SC block is its menu, `LESSONWALT_OFF`; "
                    "SCOPED regeneration of the 15, scoped #7 since the intake FULL (1 of headroom — the FULL backstop is due at #8); **skeleton 54.5220 % @ 2491, ≥50 1546, "
                    "≥75 256, ≥90 23, RAW 38.358 %** (+0.0972pp, 49 up / 1 down named); cs 15462 / 195 / 793 / 24; body 58 / 5 / 203 / 264 (ANY +2 accepted as named); "
                    "clean 2646 / 2691 = 98.33 %; leak 75 / 45; `gate_baseline.json` at r432 (`_note_r432`); `outputs/_s35_r432_sk_final.json` the skeleton state; 54.522 / "
                    "91.2 = **59.8 % of achievable**; the miner re-run 22 Sept 19:24, 198 CANDIDATE; corpus 2699 pages / 545 dirs / 2491 pairs). Before it **r431** (build "
                    "260620.04, 22 Sept ≈18:40, session 35 Round 2 — "))
o = "- Plateau window (§4): **0 of 3** — r431 predicted a skeleton move and delivered +0.0630pp (the window RESETS);"; assert st.count(o) == 1
st = st.replace(o, "- Plateau window (§4): **0 of 3** — r432 predicted a skeleton move and delivered +0.0972pp; r431 predicted a skeleton move and delivered +0.0630pp (the window RESETS);")
o = "- Standing facts: AppVersion 260620.04 (r431 the overview menu's inner-word label over-fire, session 35 Round 2, 22 Sept); before it"; assert st.count(o) == 1
st = st.replace(o, "- Standing facts: AppVersion 260620.05 (r432 the lesson page's unmarked WALT / SC block is its menu, session 35 Round 3, 22 Sept); before it 260620.04 (r431 the overview menu's inner-word label over-fire, session 35 Round 2, 22 Sept); before it")
i0 = st.index("## Session 35 — Round 3 (engine r432) — THE LESSON PAGE'S UNMARKED WALT / SC BLOCK IS ITS MENU")
i1 = st.index("## Session 35 — Round 2 (engine r431, build 260620.04) — THE OVERVIEW MENU'S INNER-WORD LABEL OVER-FIRE — SHIPPED;")
r3 = st[i0:i1]
pointer = ("## Session 35 — Round 3 (engine r432, build 260620.05) — THE LESSON PAGE'S UNMARKED WALT / SC BLOCK IS ITS MENU — SHIPPED; the PICK + what-shipped record is in "
           "LOOP_STATE_ARCHIVE.md 'Session 35 — Round 3 (engine r432 …) + what shipped'; the one-line summary is the s35-r3 Round-log line below.\n\n")
st = st[:i0] + pointer + st[i1:]
shipped = """**WHAT SHIPPED (22 Sept ≈18:38 → ≈19:30).** `Emit_Templates.json` `menu.lesson_overview_implicit` {enabled, env `LESSONWALT_OFF`, alias_words [overview], lead_pattern, max_scan_items 14, opening_tags [title bar, h1, h2, lesson content, page, body, sub head]}. `ContentConverter.#partitionItems` (after the r148 bare-lead block): `loiAlias` / `loiImplicit` / `loiLeadFirst` / `loiSet` — (a) an EMPTY `[Overview]` alias among the first 14 items whose following block qualifies; (b) the first lead item (`isLead`: a black line or a body / heading tag whose first line matches the lead pattern in ≤ 8 words) reached through `opening` items only; `buildSet` walks the block (`isMember`: blank, lead, list lines — `•` / `-` / `1.` / `a)` — black runs of only those, `list` tags, lead-titled heading / body tags; ≤ 24 items) and returns it only with ≥ 1 lead and ≥ 1 list line; the set replaces `menuIdxSet` and sets `lessonMenuEnd = max + 1`; the alias is skipped before the title-bar branch; the item before an implicit lead is never skipped as a marker. Three repairs inside the round (the probe caught each): the generic section-stop dragged the following prose paragraph into the menu (ENGC206 `Welcome! In this lesson …`); a 14-word prose sentence read as a lead (COM1006 `We are learning what an event is. You will show …`); a prose-tailed `[overview] Investigate results …` alias consumed with a `[context]` note behind it (MXFU202) — 47 up / 12 down became 49 up / 1 down. Probe OFF = 2699 / 2699 identical; ON = exactly 15 modules / 61 pages, 50 paired (`_s35_r432_probe_run.sh`, `_s35_r432_pagescore.log`). `_s35_r432_regen.sh` (the 15 + 12 spot-checks seed 432, 27 / 27 fresh); `scoped_ship.sh … --round 432 --commit` FAILED on `body_compare ANY breakdown 262 → 264`; decomposed against `reference/tests/body_compare.json`: ENGI301_1_0 (over-capture 0.73 → 0.76, the clickDrop 3047 chars unchanged, free blocks 7 → 3, lost −1 → 3) and GEO1005_6_0 (0.43 → 0.44, the tabs bundle 1845 chars unchanged, free blocks 13 → 11, lost 1 → 3) — the WALT block's departure from the body let a pre-existing over-capture cross the flag's `lost_blocks ≥ 3`; `_fastloop_diff.py … --accept-named "body_compare ANY breakdown" --commit` PASS (`_s35_r432_fastloop_accept.log`). `_s35_r432_postship.sh`: `run_all_gates.sh` rc 0 — **skeleton 54.4248 → 54.5220 % @ 2491 (+0.0972pp; 50 movers, 49 up / 1 down, +254.8pp-sum; 0 outside the set)**; ≥50 1540 → 1546; ≥75 255 → 256; ≥90 23; RAW 38.294 → 38.358; cs 15462 / 195 / 793 / 24 EXACT; body 58 / 5 / 203 / 264; clean 2646 / 2691; leak 75 / 45; every verifier ✓; 49 selftest PASS / 0 FAIL; feature index GREEN; the ledger scoped #7 since the intake FULL (1 of headroom); the miner 19:24 → 198 CANDIDATE. One PWY1001 pair re-seated (`_1_0` in at 37.4, `_2_2_0` out at 50.0). Finalise: `_s35_r432_finalise.py` (the changelog entry, Config.js 260620.05, OPERATING_GUIDE §9 / §11 / §14, gate_baseline.json `_note_r432`, LOOP_STATE.md, the loop file §0 build), the checksum manifests, the mirror.
"""
ar = rd(R + "LOOP_STATE_ARCHIVE.md")
assert "## Session 35 — Round 3 (engine r432" not in ar
r3_head = "## Session 35 — Round 3 (engine r432, build 260620.05, 22 Sept ≈18:38 → ≈19:30) — THE LESSON PAGE'S UNMARKED WALT / SC BLOCK IS ITS MENU + what shipped\n\n"
r3_body = r3.split("\n", 1)[1].strip("\n")
wr(R + "LOOP_STATE_ARCHIVE.md", ar.rstrip("\n") + "\n\n" + r3_head + r3_body + "\n\n" + shipped)
o = "- **(r431) The menu-overrun residue (`_s35_r2_menuover.log`, 56 pages / 34 modules before r431):**"; assert st.count(o) == 1
st = st.replace(o, ("- **(r432) The lesson-menu residue:** the TEDC401 / TEDC402 lessons whose WALT / SC block sits INSIDE a 2-row layout table under the `[Overview]` alias "
                    "(≈ 12 pages / 2 modules — the table is not a block member; flatten its cells to items); XGF9002 / XGF9006's TABBED lesson menus (`tab-pane`s in the "
                    "gold's lesson menu, 35 + 15 elements); the r359 note's `HIS1003 / HIS1004 / MXEX101 / PES1001 / PES1002` `[Lesson Overview]` pages whose block "
                    "still lands in the body (the census's LO+LC rows — the section-stop ends early on something; re-measure with `_s35_r3_lessonmenu.py` on the r432 "
                    "corpus); the gold-both / Claude-body 41 pages. The scrambled dual-build pairing (CEDK501 `_8_0` ↔ gold `_0.0`) is Needs Chris #6.\n" + o))
i = st.rfind("**Next session starts with:**"); assert i > 0
st = st[:i] + ("**Next session starts with:** the standing `/loop-start` (health check — the census is 552 gold / 545 Claude dirs / 2,699 Claude pages; the \"Amended:\" line; "
               "the §7 diff check; `git status` CLEAN at the session-35 commits). No round in flight (r432 shipped by session 35 Round 3 — see the Position section). "
               "**The ship ledger is at scoped #7 since the intake FULL — the FULL-corpus backstop (OPERATING_GUIDE §10a cadence 8) is due at the NEXT scoped ship.** "
               "Session 35 continues after r432 with the lanes (the lesson-menu residue re-measured on the r432 corpus; the miner's 198 rows; the KB queue; the widget "
               "census; the loss ledger); if it stops on §4, its STOPPED entry above names the lanes. NEEDS CHRIS: the open lines of the \"Needs Chris\" section.\n")
wr(R + "LOOP_STATE.md", st)
print("finalise OK")
