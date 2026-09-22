#!/usr/bin/env python3
"""r433 finalise (OPERATING_GUIDE §12) — session 36 Round 1 (22 Sept 2026): changelog entry, Config.js 260620.05 -> 260620.06,
OPERATING_GUIDE §9 / §11 / §14, gate_baseline.json (round 433 — every field), LOOP_STATE.md (Round-log line, the Position bullets — the
IN-FLIGHT marker CLEARED, LAST SHIPPED + LAST FULL — plateau window, standing facts, the miner line, the next-session line; the Round 1
PICK section MOVED to the archive with the what-shipped record; the Declined-classes entry; the follow-up line), LOOP__Autonomous_Rounds.md
§0 (the census-table build). Exact-text edits only; every anchor asserted. Run under WSL: python3 _s36_r433_finalise.py
"""
import re, json
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
PF = R + "pageforge-site/converter-v2/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

entry = """## 2026-09-22 (round 433, build 260620.06) — THE MXFUN CODE-CONTENT PHASE DIALECT: a single-file Fundamentals Writers Template whose `[<CODE> Content - PHASE N]` marker opens each phase and repeats the front matter builds the fundamentals PHASES shell — the loop's session 36 Round 1 (LOOP §1d exception 1, the MXFUN family dialect); THE FULL-REGENERATION BACKSTOP (scoped #7 → 0)

### 1. WHAT CHANGED

**The class (a Writers Template dialect the resolver mis-read — class B-ii; authority §1b level 3, the family's own gold 2 / 2 on the shell, under LOOP §1d exception 1).** The MXFUN02 / MXFUN03 Writers Templates (exactly 2 of 762 docx carry the marker) author ONE single-file Fundamentals module as four PHASES: each phase opens with `[MXFUN203 Content - PHASE 2]` (the per-phase deliverable code + "Content - PHASE N") and REPEATS the front matter — `[Fundamental 1 code] MXFUN203`, `[Title] Measurement`, `[Fundamental content]` — before its `[Page N]` + `[Side tab N] label` sections; an `[Intro page]` / `[Front page]` … `[End page]` block before `[Page 1]` is the introduction. The human's page (2 / 2) is the ordinary fundamentals PHASES shell: `div.phases` (one item per phase), `div.introduction` (the intro page's paragraphs + the `row.phaseContainer` of four `col-md-3 col-6` phaseLink tiles), one `div.fundamentalsPanel[phase=N]` per phase with its pages FLAT inside (no sub-panels, no crumbs), the side-tab labels rendered on 0 of 5 (the two h1s are the writer's `[Lesson N title H1]`), the overview menu an empty simplified shell. Three mechanisms mis-fired at once: `#partitionItems` took the SECOND `[Title]` (Phase 2's repeat) as the overview's intro marker, so the whole of Phase 1 sat in `#module-menu-content` (the s35 / s36 menu-overrun census's two largest rows, 32 + 31 elements); the labelled side tabs plus ≥ 3 `[Page N]` openers fired the r100 `_pageDelimited` inquiry mode (11 crumbs + inquiryPanels); and the `\\btab\\b` fundamentals sentinel wrapped every side tab in its own fundamentalsPanel — two shells nested, neither the gold's. MXFUN01_0_0 (0.7 %), MXFUN02 (5.8 %) and MXFUN03 (8.1 %) were the three lowest-scoring pages in the corpus.

**The fix.** `Emit_Templates.json` `body_region.fundamentals_panels.phase_text.code_content_delimiter` {enabled, env `CODEPHASE_OFF`, marker_pattern, intro_page_pattern, consume_repeat_tags [lesson content, title bar], consume_side_tabs, side_tab_pattern, scanner_hard_terminator}. `ContentConverter.#codePhasePrepass(page, run)` — called at the top of `#partitionItems`, on a fundamentals-class single-file page carrying ≥ 1 marker with N ≥ 2 — marks every marker `_codePhase = N` (an N = 1 marker, or one before the first page opener, is consumed: the first phase opens at the first NON-intro `[Page N]` opener, flagged `_codePhaseBreak`, so the intro page stays in the introduction segment), the per-phase front-matter repeats after each marker (the page's FIRST title bar kept as the header opener; a `[Fundamental 1 code]` line before the first marker too), every `[Intro page]` / `[Front page]` opener and every `[Side tab N]` tag `_codePhaseConsume` (rendered nowhere), and sets `page._codePhase`. The overview intro-marker search and the partition loop skip consumed items (no menu region → the empty simplified shell); the phase-text detection counts and the pre-pass converts the breaks into `phasebreak` items (`isCodePhaseBreak`, the red-span path — PanelsBuilder's plain phase-text branch then builds the nav, the tiles and the panels unchanged); `_bllInquiry`, `_headingLabelOn`, `sideTabMode` and `detectInquiryCed` are vetoed on a code-phase page. `InteractiveScanner.#redPhaseDelimiter` treats the marker as a hard terminator (without it the widget open at the end of Phase 3 swallowed MXFUN02's Phase 4 marker and the fourth panel never opened). MXFUN01 (the same family, a bare `[PHASE N]` marker) is multi-file (`page_model_exceptions`; the dual-build gold, Needs Chris #6) and is untouched; SCES201's `[phase N]` are moon-phase table cells inside a widget (never a tag item — a fence). Measured and DECLINED in the same round: a `keep_writer_digit.digits_by_prefix["2"]` row for MXFUN — MXFUN03's gold keeps every free-body `[H2]` at h2 (14 / 14) and MXFUN02's likewise, but BOTH of MXFUN01's golds follow the shift and the prefix pin scored MXFUN01's six paired pages DOWN (−0.8 to −3.4pp) for +0.1pp on MXFUN03; recorded in the data block's `_note_r433_mxfun`.

**What it builds:** MXFUN03_0_0 8.1 → 28.4 (+20.3; the gold is a human WORK-IN-PROGRESS: Phase 1 partial, phases 2–4 empty panels, empty LI / SC bullets — the remaining gap is the gold's), MXFUN02_0_0 5.8 → 8.0 (+2.2; its gold is a ~130-line stub of Phase 1 against a full four-phase build — the ceiling for that page). The module-menu overrun census (`_s36_r1_menuover.log`) loses its two largest rows (63 elements).

### 2. PROOF

- `_s36_r433_probe_run.sh` (all 545 modules, 4 shards; OFF = `CODEPHASE_OFF=1`): **OFF = 2699 / 2699 identical, 0 changed**; **ON = exactly MXFUN02 + MXFUN03 (2 pages / 2 modules)**, pre-scored with the gate's own `match()` (`_s36_r433_pagescore.py`: 2 up / 0 down, +22.5pp-sum).
- **THE FULL-REGENERATION BACKSTOP** (the ledger stood at scoped #7 since the 22 Sept intake FULL; OPERATING_GUIDE §10a cadence 8): `_s36_r433_fullship_par.sh` — `_batch_plan.py`'s 42 batches as `batch_convert.cjs … --force`, 4 parallel workers under WSL, 6 min, **all rc 0**; `_stalecheck.sh` **0 stale**; `_content_manifest.py fresh --affected _affected_r433.txt` → **the 540 unaffected modules byte-identical to the r432 manifest** (identical bytes cannot move a metric); `_content_manifest.py changed` = **exactly MXFUN02, MXFUN03**. `_ship_ledger.py record-full --round 433 --build 260620.06` (counter → 0).
- `_s36_r433_postship.sh` (`_s36_r433_gates.log`): `run_all_gates.sh` rc 0 — skeleton state `_s36_r433_sk_final.json` **54.5220 → 54.5311 % @ 2491 pairs (+0.0090pp; movers exactly 2, both up, +22.5pp-sum, 0 outside the affected set, new-only 0, gone 0)**; `_gatecheck.py cs bc` then `skeleton defect` (the cached-row trap: the first call printed r-old skeleton rows — the second shows the truth): skeleton IMPROVED, ≥50 / ≥75 HELD, compare_structure exact **+56 IMPROVED**, EXTRA / missing HELD, body ANY HELD; 17 selftests **49 GREEN / 0 FAIL**; feature index GREEN; `_fastloop_snapshot.py` + `_content_manifest.py snapshot` re-based; the DIFF MINER re-run on the r433 corpus (2491 pairs / 533 modules, 9318 classes, **198 CANDIDATE** — unchanged).

### 3. PROTECTED GATES (all HELD or IMPROVED — `_s36_r433_gates.log`, `_s36_r433_skdelta.log`, `_s36_r433_gatecheck*.log`)

- **Skeleton (PRIMARY)**: SCAFFOLD **54.5311 % @ 2491 pairs** (+0.0090pp; 2 up / 0 down), median 55.7; ≥50 **1546** (=), ≥75 **256** (=), ≥90 **23** (=); RAW 38.362 % (+0.004); pairs skipped 0. 54.531 / 91.2 = **59.8 % of achievable**.
- **compare_structure** 15518 / 195 / 793 / 24 (exact **+56**, EXTRA / missing / row-wrap EXACT; the matched pool 18030, +57); **body_compare** 58 / 5 / 203 / **264** EXACT; **structurally clean** 2646 / 2691 = 98.33 % EXACT; **leak** 75 occ / 45 pages EXACT; **tags 9557 / 9557**; every verifier RESULT ✓ and identical to r432 (flipcard 61 / 32 / 11 / 18 / divergence 0; speech bubbles 62 built, defect 4 at baseline; pop-outs, MTK quiz shells, MathML, lesson-menu labels, dragAndDrop, bingo ✓).
- Plateau (§4): the PICK predicted a skeleton move of +0.02 to +0.04pp and delivered +0.0090pp — BUT compare_structure exact moved +56, so the round neither counts toward nor resets the window (the r430 precedent) — the window stays **0 of 3**.

"""
p = PF + "BUILD_CHANGELOG.md"; s = rd(p)
head, rest = s.split("\n", 1)
assert head.startswith("# BUILD CHANGELOG") and rest.lstrip("\n").startswith("## 2026-09-22 (round 432, build 260620.05)")
wr(p, head + "\n\n" + entry + rest.lstrip("\n"))

p = PF + "app/js/Config.js"; s = rd(p)
old = '\tstatic AppVersion = "260620.05";'; assert s.count(old) == 1
note = ("\t// ROUND 433 (260620.06): THE MXFUN CODE-CONTENT PHASE DIALECT — a single-file Fundamentals Writers Template whose `[<CODE> Content - PHASE N]` "
        "marker opens each phase and repeats the front matter per phase (MXFUN02 / MXFUN03, exactly 2 of 762 docx) builds the fundamentals PHASES shell: "
        "ContentConverter.#codePhasePrepass marks the markers (the first phase opens at the first non-intro [Page N]), the per-phase [Fundamental 1 code] / "
        "[Title] / [Fundamental content] repeats, the [Intro page] / [Front page] openers and every [Side tab N] as consumed; the overview intro-marker search "
        "skips them (Phase 1 no longer lands in the module menu), the phase-text pre-pass turns the breaks into phasebreaks, the r100 / CED / heading-label / "
        "side-tab-nav inquiry modes are vetoed, and InteractiveScanner treats the marker as a hard terminator "
        "(fundamentals_panels.phase_text.code_content_delimiter; env CODEPHASE_OFF). The loop's session 36 Round 1 (LOOP §1d exception 1): OFF probe "
        "2699 / 2699 identical, ON = exactly the 2 pages; THE FULL-REGENERATION BACKSTOP (42 batches, 0 stale, the 540 untouched modules byte-identical); "
        "skeleton 54.5220 -> 54.5311 % @ 2491 (+0.0090pp, MXFUN03 +20.3 / MXFUN02 +2.2), cs exact +56, every other gate EXACT.\n")
wr(p, s.replace(old, note + '\tstatic AppVersion = "260620.06";'))

p = PF + "OPERATING_GUIDE.md"; s = rd(p)
old9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 432 BASELINE ("; assert s.count(old9) == 1
new9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 433 BASELINE (the MXFUN code-content phase dialect — `CODEPHASE_OFF`; "
        "THE FULL-REGENERATION BACKSTOP, scoped #7 → 0): SCAFFOLD mean 54.5311% / >=50% 1546 / >=75% 256 / >=90% 23 / RAW 38.362% @ 2491 "
        "pairs, pairs skipped 0 — 2 up / 0 down (MXFUN03 +20.3, MXFUN02 +2.2), +22.5pp-sum, 0 movers elsewhere; cs 15518 / 195 / 793 / 24 (exact +56), "
        "body 58 / 5 / 203 / 264 EXACT, clean 2646 / 2691 = 98.33 %, leak 75 / 45 EXACT.** Previous — ROUND 432 BASELINE (")
s = s.replace(old9, new9)
old11 = "| `LESSONWALT_OFF` | 432 |"; assert s.count(old11) == 1
row11 = ("| `CODEPHASE_OFF` | 433 | **THE MXFUN CODE-CONTENT PHASE DIALECT** (the autonomous loop's session 36 Round 1; LOOP §1d exception 1 — the MXFUN family "
         "dialect; the family's own gold 2 / 2 on the shell). `fundamentals_panels.phase_text.code_content_delimiter`: on a fundamentals-class single-file page "
         "carrying ≥ 1 `[<CODE> Content - PHASE N]` marker with N ≥ 2, `ContentConverter.#codePhasePrepass` (at the top of `#partitionItems`) marks the markers "
         "(N ≥ 2 = a phase break; N = 1 consumed — the first phase opens at the first non-intro `[Page N]` opener), the per-phase `[Fundamental 1 code]` / `[Title]` / "
         "`[Fundamental content]` repeats (the page's first title bar kept), the `[Intro page]` / `[Front page]` openers and every `[Side tab N]` as consumed; the "
         "intro-marker search and the partition skip them, the phase-text pre-pass converts the breaks (`isCodePhaseBreak`), the r100 / CED / heading-label / "
         "side-tab-nav inquiry modes are vetoed (`page._codePhase`), and `InteractiveScanner.#redPhaseDelimiter` treats the marker as a hard terminator. "
         "PanelsBuilder's plain phase-text branch builds the gold's `div.phases` + `div.introduction` (tiles) + one `fundamentalsPanel` per phase, pages flat. "
         "Exactly MXFUN02 + MXFUN03 of 762 docx; MXFUN01 (a bare `[PHASE N]`, multi-file) untouched; SCES201's `[phase N]` table cells a fence. OFF probe "
         "2699 / 2699 identical; ON exactly 2 pages; the FULL backstop regeneration; skeleton +0.0090pp (MXFUN03 +20.3 / MXFUN02 +2.2), cs exact +56, every "
         "other gate EXACT. A MXFUN `digits_by_prefix[\"2\"]` row measured and DECLINED (MXFUN01's golds follow the shift; −0.8 to −3.4pp on six pages). |\n")
s = s.replace(old11, row11 + old11)
old14 = "- **Build:** `260620.05` (round 432 — **THE LESSON PAGE'S UNMARKED WALT / SC BLOCK IS ITS MENU**"; assert s.count(old14) == 1
b14 = ("- **Build:** `260620.06` (round 433 — **THE MXFUN CODE-CONTENT PHASE DIALECT** — `fundamentals_panels.phase_text.code_content_delimiter`, env "
       "`CODEPHASE_OFF`; the autonomous loop's session 36 Round 1 (LOOP §1d exception 1); OFF probe 2699 / 2699 identical, ON = exactly MXFUN02 + MXFUN03; "
       "**THE FULL-REGENERATION BACKSTOP (42 batches, 0 stale, the 540 untouched modules byte-identical; the ledger scoped #7 → 0)**; **ROUND 433 BASELINE: "
       "SCAFFOLD mean 54.5311% / >=50% 1546 / >=75% 256 / >=90% 23 / RAW 38.362% @ 2491 pairs** — +0.0090pp, 2 up / 0 down, +22.5pp-sum; cs 15518 / 195 / 793 / "
       "24 (exact +56), body 58 / 5 / 203 / 264 EXACT, clean 2646 / 2691, leak 75 / 45; every verifier EXACT; 49 selftest PASS; the miner 198; plateau window "
       "0 of 3). Previous: ")
s = s.replace(old14, b14 + old14)
wr(p, s)

p = R + "CONVERTER_V2/reference/tests/gate_baseline.json"; s = rd(p)
def setv(key, old, new):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=1); assert n == 1, key
setv("build", '"260620.05"', '"260620.06"'); setv("round", 432, 433)
setv("mean_scaffold_pct", 54.52, 54.53); setv("median_scaffold_pct", 55.3, 55.7)
setv("exact_chain", 15462, 15518); setv("row_wrap_missing", 23, 24)
setv("over_capture", 56, 58)
setv("literal_tag_leak_occ", 73, 75); setv("leak_pages", 44, 45)
a = '    "_note_r432": "Round 432 (session 35 Round 3, 2026-09-22; the module-menu chrome region, KB 01B)'; assert s.count(a) == 1
s = s.replace(a, '    "_note_r433": "Round 433 (session 36 Round 1, 2026-09-22; LOOP §1d exception 1 — the MXFUN family dialect): the MXFUN code-content phase dialect — a single-file Fundamentals Writers Template whose [<CODE> Content - PHASE N] marker opens each phase builds the fundamentals phases shell (fundamentals_panels.phase_text.code_content_delimiter; env CODEPHASE_OFF). THE FULL-REGENERATION BACKSTOP (scoped #7 -> 0): 42 batches all rc 0, 0 stale, the 540 untouched modules byte-identical to the r432 manifest, changed = exactly MXFUN02 / MXFUN03. Every field below re-based to the r433 full corpus; median 55.7, row-wrap 24, over-capture 58, leak 75 / 45 were stale carry-overs corrected here (their notes already said so).",\n' + a)
a2 = '    "_note_r432": "Round 432: SCAFFOLD 54.4248 -> 54.5220'; assert s.count(a2) == 1
s = s.replace(a2, '    "_note_r433": "Round 433: SCAFFOLD 54.5220 -> 54.5311 @ 2491 pairs (+0.0090pp; MXFUN03_0_0 8.1 -> 28.4, MXFUN02_0_0 5.8 -> 8.0; 2 up / 0 down, 0 movers outside the affected set), >=50 1546 / >=75 256 / >=90 23 HELD, RAW 38.358 -> 38.362.",\n' + a2)
a3 = '    "_note_r432": "Round 432: exact 15462 / EXTRA 195'; assert s.count(a3) == 1
s = s.replace(a3, '    "_note_r433": "Round 433: exact 15462 -> 15518 (+56) / EXTRA 195 / missing 793 / row-wrap 24 EXACT; the matched pool 17973 -> 18030.",\n' + a3)
a4 = '    "_note_r432": "Round 432: over-capture 56 -> 58'; assert s.count(a4) == 1
s = s.replace(a4, '    "_note_r433": "Round 433: over-capture 58 / runaway 5 / EMPTY 203 / ANY 264 on 2691 pages EXACT.",\n' + a4)
a5 = '    "_note_r432": "Round 432: clean 2646 / 2691'; assert s.count(a5) == 1
s = s.replace(a5, '    "_note_r433": "Round 433: clean 2646 / 2691 = 98.33, leak 75 occ / 45 pages EXACT.",\n' + a5)
json.loads(s); wr(p, s)

p = R + "LOOP__Autonomous_Rounds.md"; s = rd(p)
o = "Current (22 September 2026, build 260620.05 — after the 22 Sept Round 0d and r426–r432:"; assert s.count(o) == 1
s = s.replace(o, "Current (22 September 2026, build 260620.06 — after the 22 Sept Round 0d and r426–r433:")
wr(p, s)

st = rd(R + "LOOP_STATE.md")
o = "- s35-r3 (engine r432, build 260620.05"; assert st.count(o) == 1
line = ("- s36-r1 (engine r433, build 260620.06, 22 Sept 21:40 → ≈23:05) · THE MXFUN CODE-CONTENT PHASE DIALECT (§1d exception 1 — the MXFUN family; the family's gold "
        "2 / 2 on the phases shell) — a single-file Fundamentals WT whose `[<CODE> Content - PHASE N]` marker opens each phase and repeats the front matter builds "
        "`div.phases` + `div.introduction` (tiles) + one `fundamentalsPanel` per phase, pages flat, side tabs consumed (`CODEPHASE_OFF`; Phase 1 no longer in the "
        "module menu, the r100 inquiry mode vetoed, the marker a scanner hard stop) · OFF probe 2699 / 2699 identical · ON exactly MXFUN02 + MXFUN03 · SHIPPED as "
        "THE FULL-REGENERATION BACKSTOP (42 batches rc 0, 0 stale, 540 modules byte-identical; ledger scoped #7 → 0) · skeleton 54.5220 → 54.5311 % @ 2491 "
        "(+0.0090pp; MXFUN03 +20.3 / MXFUN02 +2.2, 0 down) · cs exact +56 · every other gate EXACT · a MXFUN `[H2]`-keeps-h2 row measured and DECLINED · plateau "
        "0 of 3 (cs moved — neither counts nor resets)\n")
st = st.replace(o, line + o)
o = "- Every shipped round r314–r432 is ONE line"; assert st.count(o) == 1
st = st.replace(o, "- Every shipped round r314–r433 is ONE line")
o = "`DIFF_QUEUE.md` 22 Sept 19:24 on the r432 corpus (2,491 pairs / 533 modules), 198 CANDIDATE rows"; assert st.count(o) == 1
st = st.replace(o, "`DIFF_QUEUE.md` 22 Sept 22:48 on the r433 corpus (2,491 pairs / 533 modules), 198 CANDIDATE rows")
lines = st.split("\n")
idx = [i for i, l in enumerate(lines) if l.startswith("- **ROUND 433 IN FLIGHT — NOT PROVEN**")]
assert len(idx) == 1
lines[idx[0]] = ("- **No round in flight** (22 Sept 2026 ≈23:05, session 36 Round 1: r433 SHIPPED and committed; the corpus on disk IS the r433 state — a FULL "
                 "regeneration; the r433 record is in LOOP_STATE_ARCHIVE.md 'Session 36 — Round 1 (engine r433 …)'). The §3 step-1 rule stands: the next PICK raises "
                 "`ROUND <N> IN FLIGHT — NOT PROVEN` here BEFORE any code is edited.")
st = "\n".join(lines)
o = "- LAST SHIPPED: **r432** (build 260620.05, 22 Sept ≈19:30, session 35 Round 3 — "; assert st.count(o) == 1
st = st.replace(o, ("- LAST SHIPPED: **r433** (build 260620.06, 22 Sept ≈23:05, session 36 Round 1 — the MXFUN code-content phase dialect, `CODEPHASE_OFF`; "
                    "**THE FULL-REGENERATION BACKSTOP — LAST FULL = r433, ledger counter 0 (8 of headroom)**; **skeleton 54.5311 % @ 2491, ≥50 1546, "
                    "≥75 256, ≥90 23, RAW 38.362 %** (+0.0090pp, 2 up / 0 down); cs 15518 / 195 / 793 / 24 (exact +56); body 58 / 5 / 203 / 264; "
                    "clean 2646 / 2691 = 98.33 %; leak 75 / 45; `gate_baseline.json` at r433 (`_note_r433`, every field re-based); `outputs/_s36_r433_sk_final.json` "
                    "the skeleton state; 54.531 / 91.2 = **59.8 % of achievable**; the miner re-run 22 Sept 22:48, 198 CANDIDATE; corpus 2699 pages / 545 dirs / "
                    "2491 pairs). Before it **r432** (build 260620.05, 22 Sept ≈19:30, session 35 Round 3 — "))
o = "- Plateau window (§4): **0 of 3** — r432 predicted a skeleton move and delivered +0.0972pp;"; assert st.count(o) == 1
st = st.replace(o, "- Plateau window (§4): **0 of 3** — r433 predicted a skeleton move and delivered +0.0090pp BUT cs exact moved +56 (neither counts nor resets, the r430 precedent); r432 predicted a skeleton move and delivered +0.0972pp;")
o = "- Standing facts: AppVersion 260620.05 (r432 the lesson page's unmarked WALT / SC block is its menu, session 35 Round 3, 22 Sept); before it"; assert st.count(o) == 1
st = st.replace(o, "- Standing facts: AppVersion 260620.06 (r433 the MXFUN code-content phase dialect + the FULL backstop, session 36 Round 1, 22 Sept); before it 260620.05 (r432 the lesson page's unmarked WALT / SC block is its menu, session 35 Round 3, 22 Sept); before it")
i0 = st.index("## Session 36 — Round 1 (engine r433) — THE MXFUN CODE-CONTENT PHASE DIALECT — IN FLIGHT")
i1 = st.index("## Session 35 — Round 3 (engine r432, build 260620.05)")
r1 = st[i0:i1]
pointer = ("## Session 36 — Round 1 (engine r433, build 260620.06) — THE MXFUN CODE-CONTENT PHASE DIALECT + THE FULL-REGENERATION BACKSTOP — SHIPPED; the PICK + what-shipped "
           "record is in LOOP_STATE_ARCHIVE.md 'Session 36 — Round 1 (engine r433 …) + what shipped'; the one-line summary is the s36-r1 Round-log line below.\n\n")
st = st[:i0] + pointer + st[i1:]
shipped = """**WHAT SHIPPED (22 Sept ≈22:05 → ≈23:05).** `Emit_Templates.json` `body_region.fundamentals_panels.phase_text.code_content_delimiter` {enabled, env `CODEPHASE_OFF`, marker_pattern `^\\[?\\s*[a-z]{2,6}\\d{2,4}\\s+content\\s*[-–—:]\\s*phase\\s+(\\d+)\\s*\\]?$`, intro_page_pattern, consume_repeat_tags [lesson content, title bar], consume_side_tabs, side_tab_pattern, scanner_hard_terminator}. `ContentConverter.#codePhasePrepass(page, run)` at the top of `#partitionItems` (fundamentals body class + single-file + ≥ 1 marker with N ≥ 2): markers `_codePhase = N` (N = 1 / before the first page opener consumed), the first non-intro `[Page N]` opener `_codePhaseBreak`, the front-matter repeats after each marker (the page's first title bar kept), a `[Fundamental 1 code]` before the first marker, every `[Intro page]` / `[Front page]` opener and every `[Side tab N]` `_codePhaseConsume`; `page._codePhase = true`; a run note. The intro-marker search and the partition loop skip consumed items; `isCodePhaseBreak` joins the phase-text count and pre-pass (the red-span path); `_bllInquiry` / `_headingLabelOn` / `sideTabMode` / `detectInquiryCed` vetoed on a code-phase page; `InteractiveScanner.#redPhaseDelimiter` gains the marker as a hard terminator (MXFUN02's Phase 4 marker had been swallowed by the widget open at the end of Phase 3). Two in-round findings: (1) the `[H2]`-keeps-h2 prefix row for MXFUN (r373's `digits_by_prefix["2"]`) measured — MXFUN03 14 / 14, MXFUN02 likewise, but BOTH MXFUN01 golds shift; the pin scored MXFUN01's six paired pages −0.8 to −3.4pp for +0.1pp on MXFUN03 → DECLINED, `_note_r433_mxfun` in the data; (2) the `[Front page]` opener printed an orphan `[front]` flag per phase → consumed. Probes: `_s36_r433_probe_run.sh` OFF 2699 / 2699 identical, ON exactly MXFUN02 + MXFUN03; `_s36_r433_pagescore.py` 2 up / 0 down +22.5pp-sum (MXFUN03 8.1 → 28.4, MXFUN02 5.8 → 8.0 — both golds are human work-in-progress builds: MXFUN03 Phase 1 partial with phases 2–4 empty and empty LI / SC bullets, MXFUN02 a ~130-line stub). THE FULL BACKSTOP: `_s36_r433_fullship_par.sh` 42 batches / 4 workers / 6 min / all rc 0; `_stalecheck.sh` 0; `_content_manifest.py fresh` the 540 unaffected byte-identical, `changed` = exactly the 2. `_s36_r433_postship.sh`: `run_all_gates.sh` rc 0; skeleton 54.5220 → 54.5311 % @ 2491 (+0.0090pp; movers 2 up / 0 down, 0 outside the affected set); `_gatecheck.py cs bc` (the cached skeleton rows read 54.12 / 1531 / 254 — the documented trap) then `skeleton defect` (54.53 IMPROVED, ≥50 / ≥75 HELD); cs 15518 / 195 / 793 / 24 (exact +56); body 58 / 5 / 203 / 264 EXACT; clean 2646 / 2691; leak 75 / 45; tags 9557 / 9557; every verifier RESULT ✓ identical to r432; `record-full --round 433` (counter 0); fastloop + manifest snapshots; 49 selftests GREEN; feature index GREEN; the miner 198 CANDIDATE. Finalise: `_s36_r433_finalise.py` (this record), Config.js 260620.06, OPERATING_GUIDE §9 / §11 / §14, `gate_baseline.json` every field (median 55.7, row-wrap 24, over-capture 58, leak 75 / 45 were stale carry-overs corrected), the loop file's §0 census build, the checksum manifests, the mirror. Residue: MXFUN01 (the same dialect with a bare `[PHASE N]` marker) is multi-file against a dual-build gold — Needs Chris #6 (its line updated); the lesson-title h1 kept 2 / 4 by the gold (a tie, the engine's h2 stands).
"""
ar = rd(R + "LOOP_STATE_ARCHIVE.md")
assert "## Session 36 — Round 1 (engine r433" not in ar
r1_head = "## Session 36 — Round 1 (engine r433, build 260620.06, 22 Sept 21:40 → ≈23:05) — THE MXFUN CODE-CONTENT PHASE DIALECT + THE FULL-REGENERATION BACKSTOP + what shipped\n\n"
r1_body = r1.split("\n", 1)[1].strip("\n")
wr(R + "LOOP_STATE_ARCHIVE.md", ar.rstrip("\n") + "\n\n" + r1_head + r1_body + "\n\n" + shipped)
# the Declined-classes entry (the HIS lead-in) + the follow-up line
o = "## Declined classes\n"; assert st.count(o) == 1
st = st.replace(o, o + ("- **Session 36 Round 1 PICK pass (22 Sept ≈21:45) — THE `[Lesson Overview]` MARKER'S OWN TRAILING SENTENCE + the `[Alert box]` lead that follows it, "
    "in the lesson menu (the HIS1003 / HIS1004 form, 13 pages; `_s36_r1_lomarker.py` / `.log`, `_s36_r1_menuwhat.py` / `.log`) — DECLINED: KB-CORRECT.** Corpus-wide 42 markers "
    "with trailing text / 13 modules — the gold keeps it in the menu 14, DROPS it 20, body 1 (0.40); the alert form 20 / 2 modules (HIS only). **Constraint 70 (CL-0043) "
    "makes the lead-in `<p>` an OSSC-series rule and says \"All other series: no lead-in\"** — Claude's drop on every non-OSSC page is the KB form; the 14 gold-kept "
    "pages (HIS 8, CEDW 3, MXDI 2, MXFL 1) and the HIS alert-as-`<p>` form are a NAMED KB OVERRIDE (§1b). Note for a future KB question: the engine drops the "
    "sentence SILENTLY (the marker item is skipped at render) — a disclosure flag would be constraint-1-consistent; not a converter rule to invent here. Also "
    "below floor on the same pass: XGF9002's tabbed lesson menu (one module's form — XGF9001 / 9003 / 9004 lesson pages carry no menu), TEDC401's 2-row-table "
    "WALT block (1 module), MXEX101's U / K / D headings (1 module).\n"))
o = "- **(r432) The lesson-menu residue:**"; assert st.count(o) == 1
st = st.replace(o, ("- **(r433) The MXFUN family's heading levels + MXFUN01:** MXFUN02 / MXFUN03's gold keeps the writer's `[H2]` at h2 (14 / 14 on MXFUN03) but both of "
    "MXFUN01's golds follow the shift — a `digits_by_prefix` row keyed by PREFIX scores MXFUN01's six paired pages down (measured, declined, `_note_r433_mxfun`); "
    "a key by page model (single-file only) would fit 2 / 2 but is one family's 2 pages. The `[Lesson N title H1]` h1 is kept 2 / 4 by the gold (a tie). "
    "MXFUN01 itself is the same dialect with a bare `[PHASE N]` marker, multi-file (`page_model_exceptions`) against a DUAL-BUILD gold (a full single-file "
    "phases build `MXFUN01.html` + a Standard-template split `_0.0`–`_7.0` the gate pairs) — its 0.7 % overview is the corpus's lowest page; Needs Chris #6.\n" + o))
o = "6. **18 Sept (s21)** — the dual-build gold directories' gate pairing (the MXFUN family;"; assert st.count(o) == 1
st = st.replace(o, "6. **18 Sept (s21)** — the dual-build gold directories' gate pairing (the MXFUN family — 22 Sept s36: MXFUN01's full single-file phases gold `MXFUN01.html` vs the Standard split `_0.0`–`_7.0` the gate pairs; r433's code-content dialect would build the phases shell for it if it were single-file;")
i = st.rfind("**Next session starts with:**"); assert i > 0
st = st[:i] + ("**Next session starts with:** the standing `/loop-start` (health check — the census is 552 gold / 545 Claude dirs / 2,699 Claude pages; the \"Amended:\" line; "
               "the §7 diff check; `git status` CLEAN at the session-36 commits). No round in flight (r433 shipped by session 36 Round 1 — see the Position section). "
               "**The ship ledger is at 0 since the r433 FULL (8 of headroom).** Session 36 continues after r433 with the lanes (the miner's 198 rows re-read on the r433 "
               "corpus; the menu-overrun census's next rows — CEDR302 24 / ENGJ201 14 / MXEO202 8 / ARFUN03 + ARFUN05 7; the KB queue; the widget census; the loss "
               "ledger); if it stops on §4, its STOPPED entry above names the lanes. NEEDS CHRIS: the open lines of the \"Needs Chris\" section.\n")
wr(R + "LOOP_STATE.md", st)
print("finalise OK")
