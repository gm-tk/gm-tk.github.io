#!/usr/bin/env python3
"""r435 finalise (OPERATING_GUIDE §12) — session 36 Round 3 (22–23 Sept 2026): changelog entry, Config.js 260620.07 -> 260620.08,
OPERATING_GUIDE §9 / §11 / §14, gate_baseline.json (round 435), LOOP_STATE.md (Round-log line, the Position bullets — the IN-FLIGHT
marker CLEARED — plateau window, standing facts, the miner line, the next-session line; the Round 3 PICK section MOVED to the archive
with the what-shipped record; the follow-up line), LOOP__Autonomous_Rounds.md §0. Run under WSL: python3 _s36_r435_finalise.py"""
import re, json
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
PF = R + "pageforge-site/converter-v2/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

entry = """## 2026-09-23 (round 435, build 260620.08) — THE LESSON MENU ENDS AT THE WRITER'S `[Body]`: a `[Body]`-tagged run inside a lesson's overview block is the lesson's body opening, not menu content — the loop's session 36 Round 3 (the module-menu chrome region; the corpus's own gold at 0.976)

### 1. WHAT CHANGED

**The class (the module-menu chrome region; authority §1b level 3 — the corpus's own gold, measured).** Inside a lesson's overview block (the `[Lesson Overview]` / `[Overview]` marker or the WALT lead, up to the block's first heading) the writer sometimes types a `[Body]`-tagged run — "Welcome to lesson six. We are learning how to keep our wairua safe…", "In this lesson you will learn about the properties of 2D shapes…". `menu.lesson_menu_section_stop.menu_section_safe_tags` lists `body`, so the section-stop treated those runs as menu-safe and carried them into `#module-menu-content`: 31 runs on ~30 pages (XDLS903 / 904 / 905 / 906 / 908, MXEO202 ×6, ENGC403, GEO1005, XDLS901 …) — the remaining family rows of the s35 / s36 menu-overrun census.

**The measurement (`outputs/_s36_r3_bodylead.py` / `_bodylead2.py`, every paired lesson page).** 120 such runs on 19 modules. Where the GOLD places them: **BODY 80, MENU 2, absent 38 → 0.976 body**, far above the r182 floor. The two menu ones are XDLS901_4_0's lead and XDLS903_2_0's tail (that page also carries a gold-body one). And the decisive safety fact: **none of the 120 is itself the WALT / SC lead line** (0 WALT-lead runs in every bucket), so ending the section at a `[Body]` tag cannot decapitate a menu block.

**The fix.** `Emit_Templates.json` `menu.lesson_menu_section_stop.body_ends_section` {enabled, env `MENUBODY_OFF`, tags: [body]}: in the section-stop's `textish` test a tag listed in `tags` is not menu-safe — it ends the run, and everything from it onward is ordinary body. **Plus the guard the ON probe demanded: NEVER LEAVE THE MENU LEAD-LESS.** On XDLS901 lesson 4 the writer's `[Body]` run comes BEFORE the WALT block (two scene-setting paragraphs, then "We are learning:"), so stopping there took the whole block out of the menu with it — the very thing this rule exists to protect. The section is now built twice: when the body-stopped set holds no lead line (`menu.lesson_overview_implicit.lead_pattern`) and the un-stopped set does, the un-stopped one is kept — the same shape as the `intentOn` "never regress to an empty menu" guard beside it. Only the SECTION-STOP path consults this; the r432 implicit block builds its own index set and is untouched.

### 2. PROOF

- `_s36_r435_probe_run.sh` (all 545 modules, 4 shards; OFF = `MENUBODY_OFF=1`): **OFF = 2699 / 2699 identical, 0 changed**; **ON = 17 modules / 47 paired pages**, pre-scored with the gate's own `match()` (`_s36_r435_pagescore.py`): **37 up / 4 down / 6 same, +57.3pp-sum** (MXS1004_2_0 32.9 → 46.6, XDLS908_8_0 44.9 → 50.0, MXEO202_3_0 61.8 → 66.7, XDLS903 ×5, XDLS906 ×5 …). The first draft (no lead-less guard) scored XDLS901_4_0 −2.8 with its whole WALT block leaving the menu; the guard fixed it and the probe re-ran clean.
- **The four remaining dips, NAMED** (`_s36_r3_dips.py`): ENGI202_4_0 −5.2, PES1005_2_0 −3.8, MXEO202_4_0 −1.2 — on each, the run that left the menu is one the GOLD ITSELF PUTS IN THE BODY, so the placement is now right and the cost is composition: the paragraph lands as its own `div.row` where the gold folds it into a neighbouring column (ENGI202_4_0 body rows 15 → 16 against the gold's 13). MXFL203_1_0 −1.6 is the one genuine gold disagreement in the changed set (its gold keeps that sentence in the menu) — a single-page human outlier against the class's 0.976, recorded not chased.
- SCOPED regeneration (`_s36_r435_regen.sh`: the 17 + a 12-module spot-check sample, seed 435): `_content_manifest.py fresh` → 0 truly stale, the 525 unaffected byte-identical, the sample 12 / 12 identical under the fix. `scoped_ship.sh --round 435` reported every gate IMPROVED or HELD except **compare_structure missing container +1**, decomposed to **MXS1004_2_0** (`_s36_r435_cs_before/after.json`, an OFF/ON A/B of `compare_structure.py`): that module's matched pool rises 35 → 39 and its exact chain 31 → 34 because a paragraph that was previously unmatched is now matched — and the gold wraps that paragraph in an `alert` Claude renders plainly, so the newly matched element books one `missing container`. Pure arithmetic of a better match, the r431 / r426 precedent; committed through `_fastloop_diff.py --accept-named "compare_structure missing container" --commit` → **RESULT: MOVED, ACCEPTED AS NAMED**, recorded in the baseline manifest.
- `_s36_r435_postship.sh` (`_s36_r435_gates.log`): `run_all_gates.sh` rc 0 — skeleton state **54.5349 → 54.5579 % @ 2491 pairs (+0.0230pp; movers 41, 37 up / 4 down, +57.3pp-sum, 0 outside the affected set)**; 17 selftests **49 GREEN / 0 FAIL**; feature index GREEN; the miner re-run (9323 classes, **197 CANDIDATE**, one class retired). `_gatecheck.py` declines a verdict after a scoped ship (its mtime test sees the modules a scoped ship deliberately does not rebuild — the r430–r434 message); the decomposition above is the verdict.

### 3. PROTECTED GATES (all HELD or IMPROVED, the one mover NAMED — `_s36_r435_gates.log`, `_s36_r435_skdelta.log`, `_s36_r435_scoped_ship.log`, `_s36_r435_fastloop_accept.log`)

- **Skeleton (PRIMARY)**: SCAFFOLD **54.5579 % @ 2491 pairs** (+0.0230pp; 37 up / 4 down, all four named), median 55.7; ≥50 **1548** (+1), ≥75 **256** (=), ≥90 **23** (=); RAW 38.380 % (+0.015); pairs skipped 0. 54.558 / 91.2 = **59.8 % of achievable**.
- **compare_structure** 15576 / 195 / **794** / 24 (exact **+25**, EXTRA / row-wrap EXACT, **missing +1 ACCEPTED AS NAMED** — MXS1004_2_0's newly matched alert paragraph; the matched pool 18092, +26); **body_compare** 58 / 5 / 203 / **264** EXACT; **structurally clean** 2646 / 2691 = 98.33 % EXACT; **leak** 75 occ / 45 pages EXACT; **tags 9557 / 9557**; every verifier RESULT ✓ and identical to r434.
- Plateau (§4): the PICK predicted a skeleton move and delivered +0.0230pp — above the 0.02pp line, so the window **resets to 0 of 3**.

"""
p = PF + "BUILD_CHANGELOG.md"; s = rd(p)
head, rest = s.split("\n", 1)
assert head.startswith("# BUILD CHANGELOG") and rest.lstrip("\n").startswith("## 2026-09-22 (round 434, build 260620.07)")
wr(p, head + "\n\n" + entry + rest.lstrip("\n"))

p = PF + "app/js/Config.js"; s = rd(p)
old = '\tstatic AppVersion = "260620.07";'; assert s.count(old) == 1
note = ("\t// ROUND 435 (260620.08): THE LESSON MENU ENDS AT THE WRITER'S [Body] — inside a lesson's overview block a `[Body]`-tagged run "
        "(\"Welcome to lesson six. We are learning…\") is the lesson's BODY opening, not menu content: the section-stop's menu-safe test now "
        "refuses the tags listed in menu.lesson_menu_section_stop.body_ends_section (env MENUBODY_OFF), with a guard that keeps the un-stopped "
        "section whenever stopping would leave the menu with no WALT / SC lead line (XDLS901 lesson 4 types its [Body] BEFORE the block). "
        "Measured over every paired lesson page: 120 such runs / 19 modules — the gold places them in the body 80, the menu 2 (0.976), and NONE "
        "of the 120 is itself the lead line. The loop's session 36 Round 3: OFF probe 2699 / 2699 identical, ON 17 modules / 47 pages (37 up / 4 "
        "down, +57.3pp-sum; the four dips named — three are the gold's own body placement re-composed as its own row, one a single-page gold "
        "outlier); scoped regeneration of the 17; skeleton 54.5349 -> 54.5579 % @ 2491 (+0.0230pp), >=50 +1, cs exact +25, missing +1 ACCEPTED AS "
        "NAMED (MXS1004_2_0's newly matched alert paragraph), every other gate EXACT.\n")
wr(p, s.replace(old, note + '\tstatic AppVersion = "260620.08";'))

p = PF + "OPERATING_GUIDE.md"; s = rd(p)
old9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 434 BASELINE ("; assert s.count(old9) == 1
new9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 435 BASELINE (the lesson menu ends at the writer's `[Body]` — "
        "`MENUBODY_OFF`; SCOPED regeneration of the 17, scoped ship #2 since the r433 FULL): SCAFFOLD mean 54.5579% / >=50% 1548 / >=75% 256 / "
        ">=90% 23 / RAW 38.380% @ 2491 pairs, pairs skipped 0 — 37 up / 4 down (ENGI202_4_0 −5.2, PES1005_2_0 −3.8, MXFL203_1_0 −1.6, MXEO202_4_0 "
        "−1.2, all named), +57.3pp-sum; cs 15576 / 195 / 794 / 24 (exact +25, missing +1 accepted as named — MXS1004_2_0's newly matched alert "
        "paragraph), body 58 / 5 / 203 / 264 EXACT, clean 2646 / 2691 = 98.33 %, leak 75 / 45 EXACT.** Previous — ROUND 434 BASELINE (")
s = s.replace(old9, new9)
old11 = "| `PHASETILELABEL_OFF` / `TITLEPAYLOAD_OFF` | 434 |"; assert s.count(old11) == 1
row11 = ("| `MENUBODY_OFF` | 435 | **THE LESSON MENU ENDS AT THE WRITER'S `[Body]`** (the autonomous loop's session 36 Round 3; the module-menu "
         "chrome region; the corpus's own gold at 0.976). `menu.lesson_menu_section_stop.body_ends_section` {tags: [body]}: in the section-stop's "
         "`textish` test a listed tag is NOT menu-safe — it ends the run, so a `[Body]`-tagged paragraph inside a lesson's overview block "
         "(\"Welcome to lesson six…\", \"In this lesson you will learn about…\") and everything after it is ordinary body. Guard: the section is "
         "built twice and the UN-stopped set is kept whenever the stopped one holds no WALT / SC lead line (`lesson_overview_implicit.lead_pattern`) "
         "— XDLS901 lesson 4 types its `[Body]` before the block, and without this the whole block left the menu. Measured over every paired lesson "
         "page: 120 runs / 19 modules, gold body 80 / menu 2 / absent 38, and 0 of the 120 is itself the lead line. OFF probe 2699 / 2699 identical; "
         "ON 17 modules / 47 pages (37 up / 4 down, +57.3pp-sum); skeleton +0.0230pp, ≥50 +1, cs exact +25, missing +1 accepted as named. |\n")
s = s.replace(old11, row11 + old11)
old14 = "- **Build:** `260620.07` (round 434 — **THE ARFUN PHASE-TILE LABELS"; assert s.count(old14) == 1
b14 = ("- **Build:** `260620.08` (round 435 — **THE LESSON MENU ENDS AT THE WRITER'S `[Body]`** — "
       "`menu.lesson_menu_section_stop.body_ends_section`, env `MENUBODY_OFF`; the autonomous loop's session 36 Round 3 (the corpus's gold at "
       "0.976; 120 runs / 19 modules measured); OFF probe 2699 / 2699 identical, ON 17 modules / 47 pages; SCOPED regeneration of the 17 (scoped "
       "ship #2 since the r433 FULL); **ROUND 435 BASELINE: SCAFFOLD mean 54.5579% / >=50% 1548 / >=75% 256 / >=90% 23 / RAW 38.380% @ 2491 "
       "pairs** — +0.0230pp, 37 up / 4 down (named), +57.3pp-sum; cs 15576 / 195 / 794 / 24 (exact +25, missing +1 accepted as named), body 58 / 5 / "
       "203 / 264 EXACT, clean 2646 / 2691, leak 75 / 45; every verifier EXACT; 49 selftest PASS; the miner 197; plateau window RESET to 0 of 3). "
       "Previous: ")
s = s.replace(old14, b14 + old14)
wr(p, s)

p = R + "CONVERTER_V2/reference/tests/gate_baseline.json"; s = rd(p)
def setv(key, old, new):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=1); assert n == 1, key
setv("build", '"260620.07"', '"260620.08"'); setv("round", 434, 435)
setv("mean_scaffold_pct", 54.53, 54.56); setv("raw_mean_pct", 38.36, 38.38)
setv("pages_ge_50", 1547, 1548)
setv("exact_chain", 15551, 15576); setv("claude_missing_container", 793, 794)
a = '    "_note_r434": "Round 434 (session 36 Round 2, 2026-09-22; LOOP §1d exception 1'; assert s.count(a) == 1
s = s.replace(a, '    "_note_r435": "Round 435 (session 36 Round 3, 2026-09-23; the module-menu chrome region): the lesson menu ENDS at the writer\'s [Body] — a `[Body]`-tagged run inside a lesson\'s overview block is the lesson\'s body opening (menu.lesson_menu_section_stop.body_ends_section; env MENUBODY_OFF), with a guard that never leaves the menu lead-less. Gold body 80 / menu 2 over 120 runs on 19 modules = 0.976. SCOPED ship #2 since the r433 FULL: OFF probe 2699 / 2699 identical, ON 17 modules / 47 pages (37 up / 4 down, all four named).",\n' + a)
a2 = '    "_note_r434": "Round 434: SCAFFOLD 54.5311 -> 54.5349'; assert s.count(a2) == 1
s = s.replace(a2, '    "_note_r435": "Round 435: SCAFFOLD 54.5349 -> 54.5579 @ 2491 pairs (+0.0230pp; MXS1004_2_0 32.9 -> 46.6, XDLS908_8_0 44.9 -> 50.0, MXEO202_3_0 61.8 -> 66.7 …; 37 up / 4 down — ENGI202_4_0 -5.2 / PES1005_2_0 -3.8 / MXEO202_4_0 -1.2 are the gold\'s OWN body placement re-composed as its own row, MXFL203_1_0 -1.6 a single-page gold outlier; 0 movers outside the affected set), >=50 1547 -> 1548, >=75 256 / >=90 23 HELD, RAW 38.365 -> 38.380.",\n' + a2)
a3 = '    "_note_r434": "Round 434: exact 15518 -> 15551'; assert s.count(a3) == 1
s = s.replace(a3, '    "_note_r435": "Round 435: exact 15551 -> 15576 (+25) / EXTRA 195 / row-wrap 24 EXACT; MISSING 793 -> 794 ACCEPTED AS NAMED — MXS1004_2_0: that module\'s matched pool rises 35 -> 39 and its exact chain 31 -> 34 because a paragraph that was unmatched is now matched, and the gold wraps that paragraph in an `alert` Claude renders plainly, so the newly matched element books one missing container (the r431 / r426 precedent; _fastloop_diff --accept-named, recorded in the baseline manifest). The matched pool 18066 -> 18092.",\n' + a3)
a4 = '    "_note_r434": "Round 434: over-capture 58'; assert s.count(a4) == 1
s = s.replace(a4, '    "_note_r435": "Round 435: over-capture 58 / runaway 5 / EMPTY 203 / ANY 264 on 2691 pages EXACT.",\n' + a4)
a5 = '    "_note_r434": "Round 434: clean 2646 / 2691'; assert s.count(a5) == 1
s = s.replace(a5, '    "_note_r435": "Round 435: clean 2646 / 2691 = 98.33, leak 75 occ / 45 pages EXACT.",\n' + a5)
json.loads(s); wr(p, s)

p = R + "LOOP__Autonomous_Rounds.md"; s = rd(p)
o = "Current (22 September 2026, build 260620.07 — after the 22 Sept Round 0d and r426–r434:"; assert s.count(o) == 1
s = s.replace(o, "Current (23 September 2026, build 260620.08 — after the 22 Sept Round 0d and r426–r435:")
wr(p, s)

st = rd(R + "LOOP_STATE.md")
o = "- s36-r2 (engine r434, build 260620.07"; assert st.count(o) == 1
line = ("- s36-r3 (engine r435, build 260620.08, 22 Sept 23:40 → 23 Sept ≈00:20) · THE LESSON MENU ENDS AT THE WRITER'S `[Body]` (the module-menu chrome "
        "region; the corpus's own gold 80 body / 2 menu over 120 runs on 19 modules = 0.976; 0 of the 120 is the WALT lead itself) — a `[Body]`-tagged "
        "run inside a lesson's overview block ends the section-stop's menu run (`MENUBODY_OFF`), with a guard that keeps the un-stopped section "
        "whenever stopping would leave the menu lead-less (XDLS901's `[Body]` precedes its block — the ON probe caught it) · OFF probe 2699 / 2699 "
        "identical · ON 17 modules / 47 pages · SCOPED regen of the 17 (scoped #2 since the r433 FULL) · skeleton 54.5349 → 54.5579 % @ 2491 "
        "(+0.0230pp; 37 up / 4 down — ENGI202_4_0 −5.2 / PES1005_2_0 −3.8 / MXEO202_4_0 −1.2 are the gold's own body placement re-composed as its own "
        "row, MXFL203_1_0 −1.6 a single-page gold outlier), ≥50 +1, cs exact +25, **missing +1 ACCEPTED AS NAMED** (MXS1004_2_0's newly matched "
        "alert paragraph — matched 35 → 39, exact 31 → 34; the r431 / r426 precedent) · every other gate EXACT · miner 198 → 197 · plateau RESET 0 of 3\n")
st = st.replace(o, line + o)
o = "- Every shipped round r314–r434 is ONE line"; assert st.count(o) == 1
st = st.replace(o, "- Every shipped round r314–r435 is ONE line")
o = "`DIFF_QUEUE.md` 22 Sept 23:32 on the r434 corpus (2,491 pairs / 533 modules), 198 CANDIDATE rows"; assert st.count(o) == 1
st = st.replace(o, "`DIFF_QUEUE.md` 23 Sept 00:07 on the r435 corpus (2,491 pairs / 533 modules), 197 CANDIDATE rows")
lines = st.split("\n")
idx = [i for i, l in enumerate(lines) if l.startswith("- **ROUND 435 IN FLIGHT — NOT PROVEN**")]
assert len(idx) == 1
lines[idx[0]] = ("- **No round in flight** (23 Sept 2026 ≈00:20, session 36 Round 3: r435 SHIPPED and committed; the corpus on disk IS the r435 state; the "
                 "r435 record is in LOOP_STATE_ARCHIVE.md 'Session 36 — Round 3 (engine r435 …)'). The §3 step-1 rule stands: the next PICK raises "
                 "`ROUND <N> IN FLIGHT — NOT PROVEN` here BEFORE any code is edited.")
st = "\n".join(lines)
o = "- LAST SHIPPED: **r434** (build 260620.07, 22 Sept ≈23:45, session 36 Round 2 — "; assert st.count(o) == 1
st = st.replace(o, ("- LAST SHIPPED: **r435** (build 260620.08, 23 Sept ≈00:20, session 36 Round 3 — the lesson menu ends at the writer's `[Body]`, "
                    "`MENUBODY_OFF`; SCOPED regeneration of the 17, scoped #2 since the r433 FULL (6 of headroom); **skeleton 54.5579 % @ 2491, ≥50 1548, "
                    "≥75 256, ≥90 23, RAW 38.380 %** (+0.0230pp, 37 up / 4 down all named); cs 15576 / 195 / 794 / 24 (exact +25, missing +1 accepted as "
                    "named); body 58 / 5 / 203 / 264; clean 2646 / 2691 = 98.33 %; leak 75 / 45; `gate_baseline.json` at r435 (`_note_r435`); "
                    "`outputs/_s36_r435_sk_final.json` the skeleton state; 54.558 / 91.2 = **59.8 % of achievable**; the miner re-run 23 Sept 00:07, 197 "
                    "CANDIDATE; corpus 2699 pages / 545 dirs / 2491 pairs). Before it **r434** (build 260620.07, 22 Sept ≈23:45, session 36 Round 2 — "))
o = "- Plateau window (§4): **0 of 3** — r434 predicted a sub-0.02pp skeleton move"; assert st.count(o) == 1
st = st.replace(o, "- Plateau window (§4): **0 of 3** — r435 predicted a skeleton move and delivered +0.0230pp (above the line: the window RESETS); r434 predicted a sub-0.02pp skeleton move")
o = "- Standing facts: AppVersion 260620.07 (r434 the ARFUN phase-tile labels + the title-bar payload ownership, session 36 Round 2, 22 Sept); before it"; assert st.count(o) == 1
st = st.replace(o, "- Standing facts: AppVersion 260620.08 (r435 the lesson menu ends at the writer's `[Body]`, session 36 Round 3, 23 Sept); before it 260620.07 (r434 the ARFUN phase-tile labels + the title-bar payload ownership, session 36 Round 2, 22 Sept); before it")
i0 = st.index("## Session 36 — Round 3 (engine r435) — THE LESSON MENU ENDS AT THE WRITER'S")
i1 = st.index("## Session 36 — Round 2 (engine r434, build 260620.07)")
r3 = st[i0:i1]
pointer = ("## Session 36 — Round 3 (engine r435, build 260620.08) — THE LESSON MENU ENDS AT THE WRITER'S `[Body]` — SHIPPED; the PICK + what-shipped record "
           "is in LOOP_STATE_ARCHIVE.md 'Session 36 — Round 3 (engine r435 …) + what shipped'; the one-line summary is the s36-r3 Round-log line below.\n\n")
st = st[:i0] + pointer + st[i1:]
shipped = """**WHAT SHIPPED (22 Sept 23:40 → 23 Sept ≈00:20).** `Emit_Templates.json` `menu.lesson_menu_section_stop.body_ends_section` {enabled, env `MENUBODY_OFF`, tags [body]} + `ContentConverter`: the section-stop's `textish` test refuses a listed tag (split into `textishNoBodyStop` / `textish`), the section is built by a `buildSet(bodyStops)` helper, and the LEAD-LESS GUARD keeps the un-stopped set whenever the stopped one holds no WALT / SC lead line (`menu.lesson_overview_implicit.lead_pattern`). **One in-round repair, found by the ON probe:** the first draft took XDLS901_4_0's whole WALT block out of the menu (−2.8) because that writer types the `[Body]` BEFORE the block; the guard fixed it (37 up / 4 down after, vs 37 up / 5 down before). Probes: OFF 2699 / 2699 identical; ON 17 modules / 47 pages, `_s36_r435_pagescore.py` 37 up / 4 down / 6 same, +57.3pp-sum. The four dips NAMED with `_s36_r3_dips.py`: on ENGI202_4_0 (−5.2), PES1005_2_0 (−3.8) and MXEO202_4_0 (−1.2) the relocated run is one the GOLD ITSELF PUTS IN THE BODY — the placement is right and the cost is composition (the paragraph lands as its own `div.row` where the gold folds it into a neighbouring column: ENGI202_4_0 body rows 15 → 16 against the gold's 13); MXFL203_1_0 (−1.6) is the one real gold disagreement (its gold keeps the sentence in the menu) — a single-page outlier against 0.976, recorded not chased. Scoped regen of the 17 + a 12-module spot-check (seed 435): fresh 0 stale, the 525 unaffected byte-identical, the sample 12 / 12. `scoped_ship.sh --round 435` reported everything IMPROVED / HELD except **compare_structure missing container +1**, decomposed by an OFF/ON A/B of `compare_structure.py` (`_s36_r435_cs_before/after.json`) to **MXS1004_2_0**: its matched pool rises 35 → 39 and its exact chain 31 → 34, and the gold wraps the newly matched paragraph in an `alert` Claude renders plainly — pure arithmetic of a better match (the r431 / r426 precedent). Committed with `_fastloop_diff.py $UNION --accept-named "compare_structure missing container" --commit` → MOVED, ACCEPTED AS NAMED, recorded in the baseline manifest. Post-ship: `run_all_gates.sh` rc 0; skeleton 54.5349 → 54.5579 % @ 2491 (41 movers, 0 outside the affected set); 49 selftests GREEN; feature index GREEN; the miner 198 → 197 CANDIDATE. NOTE for the next session: `scoped_ship.sh` does NOT forward `--accept-named`, so a named acceptance is run as `_fastloop_diff.py $UNION --accept-named "<metric>" --commit` from `reference/tests` (the UNION = the affected file + `outputs/_scoped_spotcheck_sample.txt`); the ledger's scoped counter is recorded by `scoped_ship.sh` even when its step-4 verdict fails, so it is not double-counted afterwards.
"""
ar = rd(R + "LOOP_STATE_ARCHIVE.md")
assert "## Session 36 — Round 3 (engine r435" not in ar
r3_head = "## Session 36 — Round 3 (engine r435, build 260620.08, 22 Sept 23:40 → 23 Sept ≈00:20) — THE LESSON MENU ENDS AT THE WRITER'S `[Body]` + what shipped\n\n"
r3_body = r3.split("\n", 1)[1].strip("\n")
wr(R + "LOOP_STATE_ARCHIVE.md", ar.rstrip("\n") + "\n\n" + r3_head + r3_body + "\n\n" + shipped)
o = "- **(r434) The lesson-menu `[Body]` lead-in (the next candidate in the menu-overrun lane):**"; assert st.count(o) == 1
st = st.replace(o, ("- **(r435) The body's ROW COMPOSITION around a relocated paragraph (the r435 dips' real class).** On ENGI202_4_0, PES1005_2_0 and "
                    "MXEO202_4_0 the paragraph r435 correctly moved into `#body` lands as its own `div.row`, while the gold folds it into the neighbouring "
                    "content column (ENGI202_4_0 body rows 15 → 16 against the gold's 13). This is the same family as the r51 `row_break` work and the "
                    "s25 minor-heading decline: it needs a paired census of what the gold does with a body paragraph that FOLLOWS a menu block (fold vs "
                    "new row), per template. Sized: at least the 4 dip pages, probably the whole `body MOVED div.col-12.col-md-8 p→p` miner row (347 lines "
                    "/ 220 pages).\n" + o))
i = st.rfind("**Next session starts with:**"); assert i > 0
st = st[:i] + ("**Next session starts with:** the standing `/loop-start` (health check — the census is 552 gold / 545 Claude dirs / 2,699 Claude pages; the "
               "\"Amended:\" line; the §7 diff check; `git status` CLEAN at the session-36 commits). No round in flight (r435 shipped by session 36 Round 3 — "
               "see the Position section). **The ship ledger is at scoped #2 since the r433 FULL (6 of headroom).** The menu-overrun lane is now down to "
               "single-module rows (CEDR302's KWL headings 24 elements, ENGJ201's body-alert WALT 14, TWHK901's per-panel WALT 16) — all below floor; the "
               "open leads are the Follow-up section's new top line (the body's ROW COMPOSITION around a relocated paragraph — the r435 dips' class, "
               "possibly the miner's 347-line `body MOVED p→p` row), then the miner's 197 rows re-read on the r435 corpus, the KB queue, the widget census "
               "and the loss ledger. NEEDS CHRIS: the open lines of the \"Needs Chris\" section.\n")
wr(R + "LOOP_STATE.md", st)
print("finalise OK")
