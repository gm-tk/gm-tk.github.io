#!/usr/bin/env python3
"""r436 finalise (OPERATING_GUIDE §12) — session 36 Round 4 (23 Sept 2026). Run under WSL: python3 _s36_r436_finalise.py"""
import re, json
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
PF = R + "pageforge-site/converter-v2/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

entry = """## 2026-09-23 (round 436, build 260620.09) — THE LESSON CONTINUATION PAGE INHERITS ITS LESSON'S MENU: a `[Lesson 3.1] … continued` page belongs to lesson 3, so it carries lesson 3's simplified menu — the loop's session 36 Round 4 (KB 01B; the corpus at 0.66 / 0.77)

### 1. WHAT CHANGED

**The PICK pass first — the queue's largest chrome row, decomposed (the miner's module-menu COMPLETENESS row: 5,656 derivable misses / 748 pages / 210 modules).** Reading it by content split it into two classes, and the KB decides both.

**(a) DECLINED as a KB override — the repeated module overview menu.** 20 modules carry the module's WHOLE overview menu (the Understand / Know / Do block, 20–51 elements) on every lesson page; Claude ships it on the overview alone. Measured over 1,352 paired lesson pages of modules with a substantial gold overview menu (`outputs/_s36_r4_menurepeat.py`): gold repeats + Claude empty **126 pages / 30 modules**, gold repeats + Claude repeats 134, gold's own lesson menu + Claude's own 526. The Writers Template cannot decide it — on the pages with NO menu source in the WT the gold repeats 53 times and writes its own 56 (`_s36_r4_disc.py`), a coin flip — so it is a per-module house convention, not a derivable rule. **KB 01B "Lesson Pages — Simplified Module Menu" is explicit that a lesson page's menu is THAT LESSON's `[Lesson Overview]` block** (level-keyed labels, constraint 70's OSSC-only lead-in) and nowhere repeats the module overview, so §1b level 1 outranks the gold: an empty menu on a lesson with no block of its own is KB-correct, and the 30 modules' repetition is a NAMED PRE-KB OVERRIDE. Recorded, not chased.

**(b) TAKEN — the lesson continuation page.** A writer who splits one lesson across pages writes `[Lesson 3.0] Tools – show and not tell` and then `[Lesson 3.1] Show and not tell continued`. The lesson's `[Lesson Overview]` block sits at the lesson's START, so Claude built the menu on the first page and shipped the empty shell on every continuation page — while the gold carries the lesson's menu on all of them. KB 01B settles it: a continuation page is part of the same lesson, so the lesson's block is its menu too. Measured over every paired continuation page whose lesson's first page has a gold menu (42 pages; `_s36_r4_contpage.py`): **the gold repeats the lesson's menu on 23, partly on 4, ships a different one on 8 and is empty on 7 — 0.66 of the menus that exist, 0.77 once BLL240's five pages are set aside** (the dual-build gold the gate pairs by position, Needs Chris #6). Claude was EMPTY on 21 of them across 10 modules.

**The fix.** `Emit_Templates.json` `menu.lesson_continuation_inherits` {enabled, env `CONTMENU_OFF`, label_pattern `^(\\d+)\\.(\\d+)$`, exclude_code_prefixes [CEDO]}. In `ContentConverter.Convert`, after the partition and the black-run coalesce: a page whose `lessonLabel` matches the pattern stores its menu items on the run when the fraction is 0, and re-uses that lesson's stored items when the fraction is non-zero and its own menu is empty. The items are stored and re-used as SHALLOW COPIES, so no per-page state (consumed flags, `_funLi`, the round-432 marks) is ever shared between pages, and MenuBuilder renders them exactly as it did on the first page. **The CEDO exclusion is the measured counter-example:** on 6 of its 6 continuation pages (CEDO501 ×5, CEDO502 ×1) the gold's continuation menu is EMPTY and no CEDO page is in the gain set — the first ON probe scored those six −0.4 to −2.1, the prefix row removed them (the r373 `exclude_code_prefixes` pattern).

### 2. PROOF

- `_s36_r436_probe_run.sh` (all 545 modules, 4 shards; OFF = `CONTMENU_OFF=1`): **OFF = 2699 / 2699 identical, 0 changed**; **ON = 17 modules / 28 paired pages**, pre-scored with the gate's own `match()` (`_s36_r436_pagescore.py`): **27 up / 1 down, +110.9pp-sum** — CEDW501_3_1 54.8 → 63.9, CEDT501_1_1 51.5 → 59.0, CEDW501_2_1 39.3 → 46.4, BLLR202_3_1 77.3 → 84.3, HIS1008_1_2 61.6 → 68.3, CEDT501_3_1 / _6_1 +5.9 each, HIS1005_5_1 +5.6 … The ONE dip is **CEDK501_5_1 −2.6**, the scrambled dual-build gold pairing (Needs Chris #6) whose gold menu has 8 items to the inherited 7.
- SCOPED regeneration (`_s36_r436_regen.sh`: the 17 + a 12-module spot-check sample, seed 436): `_content_manifest.py fresh` → 0 truly stale, the 525 unaffected byte-identical, the sample 12 / 12 identical. `scoped_ship.sh --affected _affected_r436.txt --toggle CONTMENU_OFF --round 436 --no-regen --commit`: **PASS — skeleton +0.05 IMPROVED, ≥50 +1 IMPROVED, and compare_structure (exact / EXTRA / missing), body_compare, structurally-clean and the leak ALL HELD EXACTLY** (decomposition-proven over the 29 re-scored modules).
- `_s36_r436_postship.sh` (`_s36_r436_gates.log`): `run_all_gates.sh` rc 0 — skeleton state **54.5579 → 54.6077 % @ 2491 pairs (+0.0498pp; movers 28, 27 up / 1 down, +110.9pp-sum, 0 outside the affected set)**; 17 selftests **49 GREEN / 0 FAIL**; feature index GREEN; the miner re-run (9326 classes, **196 CANDIDATE**, another class retired). **Three pages RE-PAIRED** (new-only BLLR201_1_1, GENO901_4_1, GENO901_7_3; gone BLLR201_1_0, GENO901_4_0, GENO901_7_0): giving the continuation page a menu made IT the better match for that gold page — the pair count is unchanged at 2491 and both sides are the same module, the r431 pair-swap pattern. `_gatecheck.py` declines a verdict after a scoped ship (the r430–r435 mtime message); the decomposition is the verdict.

### 3. PROTECTED GATES (all HELD or IMPROVED — `_s36_r436_gates.log`, `_s36_r436_skdelta.log`, `_s36_r436_scoped_ship.log`)

- **Skeleton (PRIMARY)**: SCAFFOLD **54.6077 % @ 2491 pairs** (+0.0498pp; 27 up / 1 down named), median 55.7; ≥50 **1549** (+1), ≥75 **256** (=), ≥90 **23** (=); RAW 38.418 % (+0.038); pairs skipped 0. 54.608 / 91.2 = **59.9 % of achievable**.
- **compare_structure** 15576 / 195 / 794 / 24 EXACT; **body_compare** 58 / 5 / 203 / 264 EXACT; **structurally clean** 2646 / 2691 = 98.33 % EXACT; **leak** 75 occ / 45 pages EXACT; **tags 9557 / 9557**; every verifier RESULT ✓ and identical to r435.
- Plateau (§4): the PICK predicted a skeleton move and delivered +0.0498pp — the window stays **0 of 3**.

"""
p = PF + "BUILD_CHANGELOG.md"; s = rd(p)
head, rest = s.split("\n", 1)
assert head.startswith("# BUILD CHANGELOG") and rest.lstrip("\n").startswith("## 2026-09-23 (round 435, build 260620.08)")
wr(p, head + "\n\n" + entry + rest.lstrip("\n"))

p = PF + "app/js/Config.js"; s = rd(p)
old = '\tstatic AppVersion = "260620.08";'; assert s.count(old) == 1
note = ("\t// ROUND 436 (260620.09): THE LESSON CONTINUATION PAGE INHERITS ITS LESSON'S MENU — a page whose lessonLabel is `N.M` with "
        "M >= 1 (`[Lesson 3.1] … continued`) belongs to lesson N, whose `[Lesson Overview]` block sat at the lesson's start, so it carries "
        "that same simplified menu (KB 01B). ContentConverter.Convert stores a lesson's menu items on the run at `N.0` and re-uses them "
        "(shallow copies — no per-page state shared) when a continuation page's own menu is empty; the CEDO family is excluded as the "
        "measured counter-example (6 of 6 of its continuation golds carry no menu). Data menu.lesson_continuation_inherits; env CONTMENU_OFF. "
        "Measured over every paired continuation page: the gold repeats the lesson's menu on 23 of the 35 that have one (0.66; 0.77 without "
        "BLL240's dual-build pairing). The loop's session 36 Round 4: OFF probe 2699 / 2699 identical, ON 17 modules / 28 pages (27 up / 1 "
        "down — CEDK501_5_1, the scrambled dual-build pairing — +110.9pp-sum); scoped regeneration of the 17; skeleton 54.5579 -> 54.6077 % "
        "@ 2491 (+0.0498pp), >=50 +1, every other gate EXACT. The SAME PICK pass DECLINED the repeated module-overview menu (126 pages / 30 "
        "modules): the WT cannot decide it (53 repeat / 56 own) and KB 01B does not endorse it — a named pre-KB override.\n")
wr(p, s.replace(old, note + '\tstatic AppVersion = "260620.09";'))

p = PF + "OPERATING_GUIDE.md"; s = rd(p)
old9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 435 BASELINE ("; assert s.count(old9) == 1
new9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 436 BASELINE (the lesson continuation page inherits its lesson's menu — "
        "`CONTMENU_OFF`; SCOPED regeneration of the 17, scoped ship #3 since the r433 FULL): SCAFFOLD mean 54.6077% / >=50% 1549 / >=75% 256 / >=90% 23 / "
        "RAW 38.418% @ 2491 pairs, pairs skipped 0 — 27 up / 1 down (CEDK501_5_1 −2.6, the dual-build pairing), +110.9pp-sum, 0 movers elsewhere, three "
        "pages re-paired inside their own module; cs 15576 / 195 / 794 / 24 EXACT, body 58 / 5 / 203 / 264 EXACT, clean 2646 / 2691 = 98.33 %, leak 75 / 45 "
        "EXACT.** Previous — ROUND 435 BASELINE (")
s = s.replace(old9, new9)
old11 = "| `MENUBODY_OFF` | 435 |"; assert s.count(old11) == 1
row11 = ("| `CONTMENU_OFF` | 436 | **THE LESSON CONTINUATION PAGE INHERITS ITS LESSON'S MENU** (the autonomous loop's session 36 Round 4; KB 01B — a "
         "continuation page is part of the same lesson; the corpus at 0.66 / 0.77). `menu.lesson_continuation_inherits` {label_pattern `^(\\d+)\\.(\\d+)$`, "
         "exclude_code_prefixes [CEDO]}: in `Convert`, after the partition, a page whose `lessonLabel` fraction is 0 stores its menu items on the run, and a "
         "continuation page with an empty menu re-uses that lesson's stored items (shallow copies — no per-page state shared). CEDO is the measured "
         "counter-example (6 of 6 continuation golds carry no menu; the first ON probe scored them −0.4 to −2.1). Same PICK pass, DECLINED: the REPEATED "
         "MODULE-OVERVIEW menu (126 pages / 30 modules) — the WT cannot decide it (53 repeat / 56 own on identical evidence) and KB 01B makes the lesson's "
         "own block the menu, so Claude's empty menu is KB-correct and the gold's repetition is a named pre-KB override. OFF probe 2699 / 2699 identical; "
         "ON 17 modules / 28 pages (27 up / 1 down); skeleton +0.0498pp, ≥50 +1, every other gate EXACT. |\n")
s = s.replace(old11, row11 + old11)
old14 = "- **Build:** `260620.08` (round 435 — **THE LESSON MENU ENDS AT THE WRITER'S"; assert s.count(old14) == 1
b14 = ("- **Build:** `260620.09` (round 436 — **THE LESSON CONTINUATION PAGE INHERITS ITS LESSON'S MENU** — `menu.lesson_continuation_inherits`, env "
       "`CONTMENU_OFF`; the autonomous loop's session 36 Round 4 (KB 01B; 42 continuation pages measured, the gold repeating on 23 of the 35 that have a "
       "menu); OFF probe 2699 / 2699 identical, ON 17 modules / 28 pages; SCOPED regeneration of the 17 (scoped ship #3 since the r433 FULL); **ROUND 436 "
       "BASELINE: SCAFFOLD mean 54.6077% / >=50% 1549 / >=75% 256 / >=90% 23 / RAW 38.418% @ 2491 pairs** — +0.0498pp, 27 up / 1 down, +110.9pp-sum; cs "
       "15576 / 195 / 794 / 24 EXACT, body 58 / 5 / 203 / 264 EXACT, clean 2646 / 2691, leak 75 / 45; every verifier EXACT; 49 selftest PASS; the miner 196; "
       "plateau window 0 of 3). Previous: ")
s = s.replace(old14, b14 + old14)
wr(p, s)

p = R + "CONVERTER_V2/reference/tests/gate_baseline.json"; s = rd(p)
def setv(key, old, new):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=1); assert n == 1, key
setv("build", '"260620.08"', '"260620.09"'); setv("round", 435, 436)
setv("mean_scaffold_pct", 54.56, 54.61); setv("raw_mean_pct", 38.38, 38.42)
setv("pages_ge_50", 1548, 1549)
a = '    "_note_r435": "Round 435 (session 36 Round 3, 2026-09-23; the module-menu chrome region)'; assert s.count(a) == 1
s = s.replace(a, '    "_note_r436": "Round 436 (session 36 Round 4, 2026-09-23; the module-menu chrome region; KB 01B): the lesson CONTINUATION page inherits its lesson\'s simplified menu (menu.lesson_continuation_inherits; env CONTMENU_OFF; CEDO excluded as the measured counter-example). The gold repeats the lesson\'s menu on 23 of the 35 continuation pages that have one (0.66; 0.77 without BLL240\'s dual-build pairing). SCOPED ship #3 since the r433 FULL: OFF probe 2699 / 2699 identical, ON 17 modules / 28 pages (27 up / 1 down). The same PICK pass DECLINED the repeated module-overview menu (126 pages / 30 modules) as a named pre-KB override.",\n' + a)
a2 = '    "_note_r435": "Round 435: SCAFFOLD 54.5349 -> 54.5579'; assert s.count(a2) == 1
s = s.replace(a2, '    "_note_r436": "Round 436: SCAFFOLD 54.5579 -> 54.6077 @ 2491 pairs (+0.0498pp; CEDW501_3_1 54.8 -> 63.9, CEDT501_1_1 51.5 -> 59.0, CEDW501_2_1 39.3 -> 46.4, BLLR202_3_1 77.3 -> 84.3, HIS1008_1_2 61.6 -> 68.3 …; 27 up / 1 down — CEDK501_5_1 -2.6, the scrambled dual-build pairing; 0 movers outside the affected set; three pages re-paired inside their own module — BLLR201_1_0 -> _1_1, GENO901_4_0 -> _4_1, GENO901_7_0 -> _7_3, pair count unchanged), >=50 1548 -> 1549, >=75 256 / >=90 23 HELD, RAW 38.380 -> 38.418.",\n' + a2)
a3 = '    "_note_r435": "Round 435: exact 15551 -> 15576'; assert s.count(a3) == 1
s = s.replace(a3, '    "_note_r436": "Round 436: exact 15576 / EXTRA 195 / missing 794 / row-wrap 24 — every compare_structure row EXACT; the matched pool 18092 unchanged.",\n' + a3)
a4 = '    "_note_r435": "Round 435: over-capture 58'; assert s.count(a4) == 1
s = s.replace(a4, '    "_note_r436": "Round 436: over-capture 58 / runaway 5 / EMPTY 203 / ANY 264 on 2691 pages EXACT.",\n' + a4)
a5 = '    "_note_r435": "Round 435: clean 2646 / 2691'; assert s.count(a5) == 1
s = s.replace(a5, '    "_note_r436": "Round 436: clean 2646 / 2691 = 98.33, leak 75 occ / 45 pages EXACT.",\n' + a5)
json.loads(s); wr(p, s)

p = R + "LOOP__Autonomous_Rounds.md"; s = rd(p)
o = "Current (23 September 2026, build 260620.08 — after the 22 Sept Round 0d and r426–r435:"; assert s.count(o) == 1
s = s.replace(o, "Current (23 September 2026, build 260620.09 — after the 22 Sept Round 0d and r426–r436:")
wr(p, s)

st = rd(R + "LOOP_STATE.md")
o = "- s36-r3 (engine r435, build 260620.08"; assert st.count(o) == 1
line = ("- s36-r4 (engine r436, build 260620.09, 23 Sept 01:00 → ≈01:45) · THE LESSON CONTINUATION PAGE INHERITS ITS LESSON'S MENU (KB 01B — a "
        "`[Lesson 3.1] … continued` page belongs to lesson 3; the gold repeats on 23 of the 35 continuation menus that exist = 0.66, 0.77 without "
        "BLL240) — the lesson's items are stored at `N.0` and re-used as shallow copies when a continuation page's own menu is empty, CEDO excluded "
        "(6 / 6 of its continuation golds carry none) (`CONTMENU_OFF`) · OFF probe 2699 / 2699 identical · ON 17 modules / 28 pages · SCOPED regen of "
        "the 17 (scoped #3 since the r433 FULL) · skeleton 54.5579 → 54.6077 % @ 2491 (+0.0498pp; 27 up / 1 down — CEDK501_5_1 −2.6 NAMED, the "
        "dual-build pairing; +110.9pp-sum; three pages re-paired inside their own module, pair count unchanged), ≥50 +1 · EVERY other gate EXACT · "
        "miner 197 → 196 · **the same PICK pass DECLINED the repeated module-overview menu (126 pages / 30 modules) as a named pre-KB override — the "
        "WT cannot decide it (53 repeat / 56 own) and KB 01B makes the lesson's own block the menu** · plateau 0 of 3\n")
st = st.replace(o, line + o)
o = "- Every shipped round r314–r435 is ONE line"; assert st.count(o) == 1
st = st.replace(o, "- Every shipped round r314–r436 is ONE line")
o = "`DIFF_QUEUE.md` 23 Sept 00:07 on the r435 corpus (2,491 pairs / 533 modules), 197 CANDIDATE rows"; assert st.count(o) == 1
st = st.replace(o, "`DIFF_QUEUE.md` 23 Sept 00:43 on the r436 corpus (2,491 pairs / 533 modules), 196 CANDIDATE rows")
lines = st.split("\n")
idx = [i for i, l in enumerate(lines) if l.startswith("- **ROUND 436 IN FLIGHT — NOT PROVEN**")]
assert len(idx) == 1
lines[idx[0]] = ("- **No round in flight** (23 Sept 2026 ≈01:45, session 36 Round 4: r436 SHIPPED and committed; the corpus on disk IS the r436 state; the "
                 "r436 record is in LOOP_STATE_ARCHIVE.md 'Session 36 — Round 4 (engine r436 …)'). The §3 step-1 rule stands: the next PICK raises "
                 "`ROUND <N> IN FLIGHT — NOT PROVEN` here BEFORE any code is edited.")
st = "\n".join(lines)
o = "- LAST SHIPPED: **r435** (build 260620.08, 23 Sept ≈00:20, session 36 Round 3 — "; assert st.count(o) == 1
st = st.replace(o, ("- LAST SHIPPED: **r436** (build 260620.09, 23 Sept ≈01:45, session 36 Round 4 — the lesson continuation page inherits its lesson's menu, "
                    "`CONTMENU_OFF`; SCOPED regeneration of the 17, scoped #3 since the r433 FULL (5 of headroom); **skeleton 54.6077 % @ 2491, ≥50 1549, "
                    "≥75 256, ≥90 23, RAW 38.418 %** (+0.0498pp, 27 up / 1 down named); cs 15576 / 195 / 794 / 24 EXACT; body 58 / 5 / 203 / 264; clean "
                    "2646 / 2691 = 98.33 %; leak 75 / 45; `gate_baseline.json` at r436 (`_note_r436`); `outputs/_s36_r436_sk_final.json` the skeleton state; "
                    "54.608 / 91.2 = **59.9 % of achievable**; the miner re-run 23 Sept 00:43, 196 CANDIDATE; corpus 2699 pages / 545 dirs / 2491 pairs). "
                    "Before it **r435** (build 260620.08, 23 Sept ≈00:20, session 36 Round 3 — "))
o = "- Plateau window (§4): **0 of 3** — r435 predicted a skeleton move and delivered +0.0230pp"; assert st.count(o) == 1
st = st.replace(o, "- Plateau window (§4): **0 of 3** — r436 predicted a skeleton move and delivered +0.0498pp; r435 predicted a skeleton move and delivered +0.0230pp")
o = "- Standing facts: AppVersion 260620.08 (r435 the lesson menu ends at the writer's `[Body]`, session 36 Round 3, 23 Sept); before it"; assert st.count(o) == 1
st = st.replace(o, "- Standing facts: AppVersion 260620.09 (r436 the lesson continuation page inherits its lesson's menu, session 36 Round 4, 23 Sept); before it 260620.08 (r435 the lesson menu ends at the writer's `[Body]`, session 36 Round 3, 23 Sept); before it")
i0 = st.index("## Session 36 — Round 4 (engine r436) — THE LESSON CONTINUATION PAGE")
i1 = st.index("## Session 36 — Round 3 (engine r435, build 260620.08)")
r4 = st[i0:i1]
pointer = ("## Session 36 — Round 4 (engine r436, build 260620.09) — THE LESSON CONTINUATION PAGE INHERITS ITS LESSON'S MENU — SHIPPED; the PICK "
           "(including the DECLINED repeated-module-overview class) + what-shipped record is in LOOP_STATE_ARCHIVE.md 'Session 36 — Round 4 (engine r436 …) "
           "+ what shipped'; the one-line summary is the s36-r4 Round-log line below.\n\n")
st = st[:i0] + pointer + st[i1:]
shipped = """**WHAT SHIPPED (23 Sept 01:00 → ≈01:45).** `Emit_Templates.json` `menu.lesson_continuation_inherits` {enabled, env `CONTMENU_OFF`, label_pattern `^(\\d+)\\.(\\d+)$`, exclude_code_prefixes [CEDO]} + `ContentConverter.Convert` (after `#partitionItems` and the black-run coalesce): a page whose `lessonLabel` fraction is 0 stores its menu items on `run._lessonMenuItems[major]`; a continuation page whose own menu is empty re-uses them. Both directions copy the items shallowly, so no per-page state (consumed flags, `_funLi`, the r432 marks) is shared; MenuBuilder then renders them exactly as on the first page, and the page logs a note naming the source page. **One in-round repair, found by the ON probe:** the first draft moved six CEDO pages DOWN (−0.4 to −2.1) because that family's continuation golds carry no menu at all — 6 of 6, and no CEDO page is in the gain set — so the whole prefix is excluded (`exclude_code_prefixes`, the r373 pattern); the re-probe went 27 up / 1 down. Probes: OFF 2699 / 2699 identical; ON 17 modules / 28 paired pages; `_s36_r436_pagescore.py` +110.9pp-sum (CEDW501_3_1 +9.1, CEDT501_1_1 +7.5, CEDW501_2_1 +7.1, BLLR202_3_1 +7.0, HIS1008_1_2 +6.6 …). The one dip, NAMED: CEDK501_5_1 −2.6 — the scrambled dual-build gold pairing (Needs Chris #6), whose gold menu holds 8 items against the inherited 7. Scoped regen of the 17 + a 12-module spot-check (seed 436): fresh 0 stale, the 525 unaffected byte-identical, the sample 12 / 12. `scoped_ship.sh --round 436` PASS — skeleton +0.05 and ≥50 +1 IMPROVED, **every other protected gate HELD EXACTLY**. Post-ship: `run_all_gates.sh` rc 0; skeleton 54.5579 → 54.6077 % @ 2491; 49 selftests GREEN; feature index GREEN; the miner 197 → 196 CANDIDATE. Three pages RE-PAIRED inside their own modules (BLLR201_1_0 → _1_1, GENO901_4_0 → _4_1, GENO901_7_0 → _7_3): giving the continuation page a menu made it the better match for that gold page — the pair count is unchanged at 2491 (the r431 pair-swap pattern).

**THE PICK PASS'S OTHER HALF — DECLINED, and why it matters.** The same measurement pass covered the miner's largest chrome row (module-menu completeness: 5,656 derivable misses / 748 pages / 210 modules). Its dominant class is the REPEATED MODULE-OVERVIEW MENU: 20 modules carry the module's whole Understand / Know / Do block (20–51 elements) on every lesson page, and on 126 pages / 30 modules Claude's lesson menu is empty where the gold repeats it (`_s36_r4_menurepeat.py`: gold repeats + Claude repeats 134, gold's own + Claude's own 526, so the mechanism is not simply missing). The Writers Template cannot decide it — among the pages with no menu source in the WT the gold repeats 53 times and writes its own 56 (`_s36_r4_disc.py`) — so it is a per-module house convention that only a mined registry row could carry. **KB 01B "Lesson Pages — Simplified Module Menu" makes a lesson page's menu that LESSON's `[Lesson Overview]` block** (level-keyed labels; constraint 70's OSSC-only lead-in) and nowhere repeats the module overview, so §1b level 1 outranks the gold: Claude's empty menu on a lesson with no block of its own is KB-CORRECT, and the 30 modules' repetition is a NAMED PRE-KB OVERRIDE — recorded here, never chased. That retires the queue's biggest chrome row with a reason rather than a rule.
"""
ar = rd(R + "LOOP_STATE_ARCHIVE.md")
assert "## Session 36 — Round 4 (engine r436" not in ar
r4_head = "## Session 36 — Round 4 (engine r436, build 260620.09, 23 Sept 01:00 → ≈01:45) — THE LESSON CONTINUATION PAGE INHERITS ITS LESSON'S MENU + what shipped\n\n"
r4_body = r4.split("\n", 1)[1].strip("\n")
wr(R + "LOOP_STATE_ARCHIVE.md", ar.rstrip("\n") + "\n\n" + r4_head + r4_body + "\n\n" + shipped)
o = "- **(r435) The body's ROW COMPOSITION around a relocated paragraph"; assert st.count(o) == 1
st = st.replace(o, ("- **(r436) The REPEATED MODULE-OVERVIEW MENU — DECLINED as a KB override, recorded here so no session re-measures it.** 20 modules carry the "
                    "module's whole overview menu on every lesson page; 126 pages / 30 modules have an empty Claude menu where the gold repeats it (ANZH401 12, "
                    "HPRE301 12, ENGC102 / MXFL101 / MXFL102 / SSOG105 7 each …). The WT cannot decide it (53 repeat / 56 own on identical evidence — "
                    "`_s36_r4_disc.py`), and KB 01B makes the lesson page's menu that lesson's own `[Lesson Overview]` block, so the empty menu is KB-correct. "
                    "It would need a mined registry row (a `derive_menu_repeat` sibling of `derive_menu_type.cjs`) AND a KB decision to overturn constraint-level "
                    "guidance — a question for Chris, not a loop round.\n" + o))
i = st.rfind("**Next session starts with:**"); assert i > 0
st = st[:i] + ("**Next session starts with:** the standing `/loop-start` (health check — the census is 552 gold / 545 Claude dirs / 2,699 Claude pages; the "
               "\"Amended:\" line; the §7 diff check; `git status` CLEAN at the session-36 commits). No round in flight (r436 shipped by session 36 Round 4 — "
               "see the Position section). **The ship ledger is at scoped #3 since the r433 FULL (5 of headroom).** The module-menu chrome row is now "
               "dispositioned end to end (r432 the implicit block, r435 the `[Body]` stop, r436 the continuation page; the repeated module-overview class "
               "DECLINED as a KB override — see the Follow-up section). The open leads: the miner's 196 rows re-read on the r436 corpus, the body's ROW "
               "COMPOSITION class (the r435 dips), the KB queue, the widget census and the loss ledger. NEEDS CHRIS: the open lines of the \"Needs Chris\" "
               "section.\n")
wr(R + "LOOP_STATE.md", st)
print("finalise OK")
