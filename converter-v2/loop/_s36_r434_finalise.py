#!/usr/bin/env python3
"""r434 finalise (OPERATING_GUIDE §12) — session 36 Round 2 (22 Sept 2026): changelog entry, Config.js 260620.06 -> 260620.07,
OPERATING_GUIDE §9 / §11 / §14, gate_baseline.json (round 434), LOOP_STATE.md (Round-log line, the Position bullets — the IN-FLIGHT
marker CLEARED — plateau window, standing facts, the miner line, the next-session line; the Round 2 PICK section MOVED to the archive
with the what-shipped record; the follow-up line), LOOP__Autonomous_Rounds.md §0 (the census-table build). Exact-text edits only;
every anchor asserted. Run under WSL: python3 _s36_r434_finalise.py"""
import re, json
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
PF = R + "pageforge-site/converter-v2/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

entry = """## 2026-09-22 (round 434, build 260620.07) — THE ARFUN PHASE-TILE LABELS: a `[Title: Phase one]` line is a phaseLink tile's label, never the page opener nor the menu boundary — and a head-matched `[Title: …]` owns its payload — the loop's session 36 Round 2 (LOOP §1d exception 1, the ARFUN family dialect)

### 1. WHAT CHANGED

**The class (the module-menu chrome region; authority §1b level 3 — the ARFUN family's own gold 3 / 3 — under LOOP §1d exception 1).** The ARFUN Writers Templates follow the overview's `[Insert links to the 4 individual phases]` instruction with four `[Title: Phase one] Emoji for thumb nail 🎸` lines — the labels of the phaseLink tiles the human builds. They parse as title-bar aliases, so the FIRST of them became the overview's menu/body boundary and the module's whole introduction (the welcome prose, the `[Insert as alert box on right hand side]` box, the `[H2]` elements list) landed in `#module-menu-content`, where the gold ships `div.introduction` (`.col-md-8.col-12` rows + the `.alert.top` side box); the other three rendered as stray `<h4>`s in the menu. On ARFUN02 the first one was even the PAGE OPENER — its header read "Phase one Emoji for thumb nail" — because the real `[Title: Puoro me te Oro| Music and Sound]` resolved to `audio`: the normaliser's multi-pass found the embedded alias "sound" inside the payload and ELEMENT (6) outranks SECTION_MARKER (3). These were the menu-overrun census's ARFUN rows (7 + 7 + 5 elements) and, with r433's MXFUN rows, the last of its family-sized entries.

**The fix, in three parts.** (1) `Emit_Templates.json` `body_region.fundamentals_panels.phase_nav_tiles.writer_tile_labels` {enabled, env `PHASETILELABEL_OFF`, payload_pattern, black_line_pattern, menu_bound_exclude_alias_words}: in `#partitionItems`, on a fundamentals-class page, a title-bar item whose colon payload matches `Phase <ordinal>` — and a black line of the same shape (ARFUN04) — is marked `_phaseTileLabel`: never the page opener, never the intro marker, rendered nowhere (PanelsBuilder generates the tiles). (2) The menu is the FRONT MATTER: a mid-document `[Title]` alias that sits INSIDE phase 1 is that phase's own title, not the menu/body boundary — `#firstPhaseDelimiterIdx` (reading the same four phase-delimiter patterns the phase-text pre-pass uses: the ARFUN bracketed opener, the ENFUN bare red span, r433's MXFUN code-content marker, the TEFUN black line) bounds `introIdx`, and the rule stands down whenever the writer marked an `[Overview]` alias at or ahead of that index, because there the front matter IS the menu (the ENFUN / HPFUN `menu.fundamentals_overview_li` capture reads it through this very index — tested against the ALIAS, not the first phase break, since the ENFUN dialect's opening red "Phase 1" span sits BEFORE its `[Overview]` marker). (3) `Tag_Lexicon.json` `_meta.head_section_marker_owns_payload` (env `TITLEPAYLOAD_OFF`): when a fragment's FIRST alias hit came from its head and that tag is a SECTION_MARKER, the payload is the marker's own text and is never re-scanned. Measured over every red span with a colon (3,283 of 159,171 — `_s36_r2_headpayload.cjs`): 139 head-matched spans spawn a higher-ranked payload tag, 138 of them the DESIGNED activity + widget compound (`[interactive: carousel + captions]`, a CONTAINER_OPEN head) which the rule leaves untouched, and exactly one a SECTION_MARKER head — ARFUN02's title.

**Two in-round corrections the probes caught, both worth recording.** The first draft named the new toggle `HEADPAYLOAD_OFF` — which is **already round 303's accordion member rule** (`InteractiveBuilder.#accHeadPayload`): the OFF probe was not byte-identical (EXBP901_3_0 lost its built accordion, XDLS902_5_0 its `<h2>`) because setting the toggle disabled that other rule. Renamed `TITLEPAYLOAD_OFF`; the OFF leg went clean. The second draft bounded the menu on every fundamentals page and emptied the eight ENFUN overviews' Learning-intentions menus (−0.8 to −1.8pp each); the `[Overview]`-alias guard above fixed it, and a third draft that tested the guard against the first phase break instead of the alias re-broke the same eight — the ON probe caught all three.

**What it builds:** ARFUN05_0_0 35.7 → 40.0 (+4.3), ARFUN02_0_0 20.4 → 23.1 (+2.7; and its header now carries the gold's own pair, "Puoro me te Oro" | "Music and Sound"), ARFUN03_0_0 49.6 → 52.2 (+2.6).

### 2. PROOF

- `_s36_r434_probe_run.sh` (all 545 modules, 4 shards; OFF = `PHASETILELABEL_OFF=1 TITLEPAYLOAD_OFF=1`): **OFF = 2699 / 2699 identical, 0 changed**; **ON = exactly ARFUN02 / ARFUN03 / ARFUN05 (3 pages / 3 modules)**, pre-scored with the gate's own `match()` (`_s36_r434_pagescore.py`: 3 up / 0 down, +9.6pp-sum).
- SCOPED regeneration (`_s36_r434_regen.sh`: the 3 + a 12-module spot-check sample, seed 434): `_content_manifest.py fresh` → 0 truly stale, the 539 unaffected byte-identical; the spot-check 12 / 12 byte-identical under the fix. `scoped_ship.sh --affected _affected_r434.txt --toggle PHASETILELABEL_OFF --round 434 --no-regen --commit`: **PASS — skeleton mean IMPROVED, ≥50 +1, ≥75 HELD, compare_structure exact +33 IMPROVED, EXTRA / missing / body ANY / clean / leak HELD** (exact, decomposition-proven over the 15 re-scored modules).
- `_s36_r434_postship.sh` (`_s36_r434_gates.log`): `run_all_gates.sh` rc 0 — skeleton state `_s36_r434_sk_final.json` **54.5311 → 54.5349 % @ 2491 pairs (+0.0039pp; movers exactly 3, all up, +9.6pp-sum, 0 outside the affected set, new-only 0, gone 0)**; 17 selftests **49 GREEN / 0 FAIL**; feature index GREEN; the miner re-run on the r434 corpus (9307 classes, **198 CANDIDATE** — unchanged). `_gatecheck.py` declines a verdict after a SCOPED ship (its mtime freshness test sees the 527 modules the scoped ship deliberately did not rebuild — the same message r430 / r431 / r432 logged); the scoped-ship decomposition above IS the verdict, and `_content_manifest.py` is the byte-level proof behind it.

### 3. PROTECTED GATES (all HELD or IMPROVED — `_s36_r434_gates.log`, `_s36_r434_skdelta.log`, `_s36_r434_scoped_ship.log`)

- **Skeleton (PRIMARY)**: SCAFFOLD **54.5349 % @ 2491 pairs** (+0.0039pp; 3 up / 0 down), median 55.7; ≥50 **1547** (+1), ≥75 **256** (=), ≥90 **23** (=); RAW 38.365 % (+0.003); pairs skipped 0. 54.535 / 91.2 = **59.8 % of achievable**.
- **compare_structure** 15551 / 195 / 793 / 24 (exact **+33**, the rest EXACT; the matched pool 18066, +36); **body_compare** 58 / 5 / 203 / **264** EXACT; **structurally clean** 2646 / 2691 = 98.33 % EXACT; **leak** 75 occ / 45 pages EXACT; **tags 9557 / 9557**; every verifier RESULT ✓ and identical to r433.
- Plateau (§4): the PICK predicted a skeleton move under 0.02pp and delivered +0.0039pp — but ≥50 and compare_structure exact both moved, so the round neither counts toward nor resets the window (the r430 precedent) — it stays **0 of 3**.

"""
p = PF + "BUILD_CHANGELOG.md"; s = rd(p)
head, rest = s.split("\n", 1)
assert head.startswith("# BUILD CHANGELOG") and rest.lstrip("\n").startswith("## 2026-09-22 (round 433, build 260620.06)")
wr(p, head + "\n\n" + entry + rest.lstrip("\n"))

p = PF + "app/js/Config.js"; s = rd(p)
old = '\tstatic AppVersion = "260620.06";'; assert s.count(old) == 1
note = ("\t// ROUND 434 (260620.07): THE ARFUN PHASE-TILE LABELS — on a fundamentals page a title-bar alias whose colon payload is "
        "'Phase <ordinal>' (`[Title: Phase one] Emoji for thumb nail`, the lines after `[Insert links to the 4 individual phases]`) is a "
        "phaseLink tile's LABEL: never the page opener, never the overview's menu/body boundary, rendered nowhere (the tiles are "
        "generated). A mid-document `[Title]` alias INSIDE phase 1 is likewise not the boundary (#firstPhaseDelimiterIdx bounds it) "
        "unless the writer marked an `[Overview]` alias at or ahead of it — there the front matter IS the menu (the ENFUN / HPFUN "
        "fundamentals_overview_li capture). Riding along: a head-matched SECTION_MARKER owns its payload, so "
        "`[Title: Puoro me te Oro| Music and Sound]` no longer resolves to `audio` on the embedded word 'sound' "
        "(phase_nav_tiles.writer_tile_labels / PHASETILELABEL_OFF; Tag_Lexicon _meta.head_section_marker_owns_payload / "
        "TITLEPAYLOAD_OFF — NOT HEADPAYLOAD_OFF, which is round 303's accordion rule). The loop's session 36 Round 2: OFF probe "
        "2699 / 2699 identical, ON = exactly ARFUN02 / 03 / 05 (3 up / 0 down, +9.6pp-sum); scoped regeneration of the 3; skeleton "
        "54.5311 -> 54.5349 % @ 2491 (+0.0039pp), >=50 +1, cs exact +33, every other gate EXACT.\n")
wr(p, s.replace(old, note + '\tstatic AppVersion = "260620.07";'))

p = PF + "OPERATING_GUIDE.md"; s = rd(p)
old9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 433 BASELINE ("; assert s.count(old9) == 1
new9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 434 BASELINE (the ARFUN phase-tile labels + the title-bar payload "
        "ownership — `PHASETILELABEL_OFF` / `TITLEPAYLOAD_OFF`; SCOPED regeneration of the 3, scoped ship #1 since the r433 FULL): SCAFFOLD mean "
        "54.5349% / >=50% 1547 / >=75% 256 / >=90% 23 / RAW 38.365% @ 2491 pairs, pairs skipped 0 — 3 up / 0 down (ARFUN05 +4.3, ARFUN02 +2.7, "
        "ARFUN03 +2.6), +9.6pp-sum, 0 movers elsewhere; cs 15551 / 195 / 793 / 24 (exact +33), body 58 / 5 / 203 / 264 EXACT, clean 2646 / 2691 = "
        "98.33 %, leak 75 / 45 EXACT.** Previous — ROUND 433 BASELINE (")
s = s.replace(old9, new9)
old11 = "| `CODEPHASE_OFF` | 433 |"; assert s.count(old11) == 1
row11 = ("| `PHASETILELABEL_OFF` / `TITLEPAYLOAD_OFF` | 434 | **THE ARFUN PHASE-TILE LABELS + THE TITLE-BAR PAYLOAD OWNERSHIP** (the autonomous "
         "loop's session 36 Round 2; LOOP §1d exception 1 — the ARFUN family's own gold 3 / 3). `phase_nav_tiles.writer_tile_labels`: on a "
         "fundamentals-class page a title-bar item whose colon payload matches `Phase <ordinal>` (and a black line of the same shape — ARFUN04) is a "
         "phaseLink tile LABEL — `_phaseTileLabel`: not the page opener, not the overview's intro marker, rendered nowhere; and a mid-document "
         "`[Title]` alias that sits after the first phase delimiter (`#firstPhaseDelimiterIdx`, the four delimiter patterns) is not the menu/body "
         "boundary either — UNLESS an `[Overview]` alias sits at or ahead of it (`menu_bound_exclude_alias_words`; the ENFUN / HPFUN front matter IS "
         "the menu, and that dialect's red `Phase 1` span precedes its `[Overview]`, so the guard keys on the alias, not the break). "
         "`Tag_Lexicon _meta.head_section_marker_owns_payload` (`TITLEPAYLOAD_OFF`): a head-matched SECTION_MARKER's payload is its own text, never "
         "re-scanned — 139 head-matched colon spans corpus-wide spawn a higher-ranked payload tag, 138 of them the designed activity + widget "
         "compound (untouched: a CONTAINER_OPEN head), one the ARFUN02 title. **`HEADPAYLOAD_OFF` is round 303's accordion member rule — a different "
         "toggle; the first draft's name collision was caught by the OFF probe (EXBP901 / XDLS902).** OFF probe 2699 / 2699 identical; ON exactly 3 "
         "pages; skeleton +0.0039pp (3 up / 0 down), ≥50 +1, cs exact +33, every other gate EXACT. |\n")
s = s.replace(old11, row11 + old11)
old14 = "- **Build:** `260620.06` (round 433 — **THE MXFUN CODE-CONTENT PHASE DIALECT**"; assert s.count(old14) == 1
b14 = ("- **Build:** `260620.07` (round 434 — **THE ARFUN PHASE-TILE LABELS + THE TITLE-BAR PAYLOAD OWNERSHIP** — "
       "`phase_nav_tiles.writer_tile_labels` / `PHASETILELABEL_OFF` and `Tag_Lexicon _meta.head_section_marker_owns_payload` / `TITLEPAYLOAD_OFF`; "
       "the autonomous loop's session 36 Round 2 (LOOP §1d exception 1); OFF probe 2699 / 2699 identical, ON = exactly ARFUN02 / 03 / 05; SCOPED "
       "regeneration of the 3 (scoped ship #1 since the r433 FULL); **ROUND 434 BASELINE: SCAFFOLD mean 54.5349% / >=50% 1547 / >=75% 256 / >=90% 23 / "
       "RAW 38.365% @ 2491 pairs** — +0.0039pp, 3 up / 0 down, +9.6pp-sum; cs 15551 / 195 / 793 / 24 (exact +33), body 58 / 5 / 203 / 264 EXACT, clean "
       "2646 / 2691, leak 75 / 45; every verifier EXACT; 49 selftest PASS; the miner 198; plateau window 0 of 3). Previous: ")
s = s.replace(old14, b14 + old14)
wr(p, s)

p = R + "CONVERTER_V2/reference/tests/gate_baseline.json"; s = rd(p)
def setv(key, old, new):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=1); assert n == 1, key
setv("build", '"260620.06"', '"260620.07"'); setv("round", 433, 434)
setv("mean_scaffold_pct", 54.53, 54.53); setv("pages_ge_50", 1546, 1547)
setv("exact_chain", 15518, 15551)
a = '    "_note_r433": "Round 433 (session 36 Round 1, 2026-09-22; LOOP §1d exception 1'; assert s.count(a) == 1
s = s.replace(a, '    "_note_r434": "Round 434 (session 36 Round 2, 2026-09-22; LOOP §1d exception 1 — the ARFUN family dialect): a `[Title: Phase one]` line is a phaseLink tile label, never the page opener nor the overview menu boundary; a mid-document [Title] inside phase 1 is not the boundary either (unless an [Overview] alias sits at or ahead of it — the ENFUN / HPFUN front matter IS the menu); a head-matched SECTION_MARKER owns its payload (phase_nav_tiles.writer_tile_labels / PHASETILELABEL_OFF; Tag_Lexicon _meta.head_section_marker_owns_payload / TITLEPAYLOAD_OFF). SCOPED ship #1 since the r433 FULL: OFF probe 2699 / 2699 identical, ON exactly ARFUN02 / 03 / 05.",\n' + a)
a2 = '    "_note_r433": "Round 433: SCAFFOLD 54.5220 -> 54.5311'; assert s.count(a2) == 1
s = s.replace(a2, '    "_note_r434": "Round 434: SCAFFOLD 54.5311 -> 54.5349 @ 2491 pairs (+0.0039pp; ARFUN05_0_0 35.7 -> 40.0, ARFUN02_0_0 20.4 -> 23.1, ARFUN03_0_0 49.6 -> 52.2; 3 up / 0 down, 0 movers outside the affected set), >=50 1546 -> 1547, >=75 256 / >=90 23 HELD, RAW 38.362 -> 38.365.",\n' + a2)
a3 = '    "_note_r433": "Round 433: exact 15462 -> 15518'; assert s.count(a3) == 1
s = s.replace(a3, '    "_note_r434": "Round 434: exact 15518 -> 15551 (+33) / EXTRA 195 / missing 793 / row-wrap 24 EXACT; the matched pool 18030 -> 18066.",\n' + a3)
a4 = '    "_note_r433": "Round 433: over-capture 58'; assert s.count(a4) == 1
s = s.replace(a4, '    "_note_r434": "Round 434: over-capture 58 / runaway 5 / EMPTY 203 / ANY 264 on 2691 pages EXACT.",\n' + a4)
a5 = '    "_note_r433": "Round 433: clean 2646 / 2691'; assert s.count(a5) == 1
s = s.replace(a5, '    "_note_r434": "Round 434: clean 2646 / 2691 = 98.33, leak 75 occ / 45 pages EXACT.",\n' + a5)
json.loads(s); wr(p, s)

p = R + "LOOP__Autonomous_Rounds.md"; s = rd(p)
o = "Current (22 September 2026, build 260620.06 — after the 22 Sept Round 0d and r426–r433:"; assert s.count(o) == 1
s = s.replace(o, "Current (22 September 2026, build 260620.07 — after the 22 Sept Round 0d and r426–r434:")
wr(p, s)

st = rd(R + "LOOP_STATE.md")
o = "- s36-r1 (engine r433, build 260620.06"; assert st.count(o) == 1
line = ("- s36-r2 (engine r434, build 260620.07, 22 Sept 23:05 → ≈23:45) · THE ARFUN PHASE-TILE LABELS + THE TITLE-BAR PAYLOAD OWNERSHIP (§1d "
        "exception 1 — the ARFUN family; its gold 3 / 3) — a `[Title: Phase one]` line is a phaseLink tile's label (not the opener, not the menu "
        "boundary, rendered nowhere), a mid-document `[Title]` inside phase 1 is not the boundary either unless an `[Overview]` alias sits at or "
        "ahead of it, and a head-matched SECTION_MARKER owns its payload (`PHASETILELABEL_OFF` / `TITLEPAYLOAD_OFF`) · OFF probe 2699 / 2699 "
        "identical · ON exactly 3 pages / 3 modules (three in-round repairs: the `HEADPAYLOAD_OFF` name COLLISION with r303's accordion rule caught "
        "by the OFF probe; the ENFUN menus emptied twice, fixed by the `[Overview]`-alias guard keyed on the alias, not the phase break) · SCOPED "
        "regen of the 3 (scoped #1 since the r433 FULL) · skeleton 54.5311 → 54.5349 % @ 2491 (+0.0039pp; ARFUN05 +4.3 / ARFUN02 +2.7 / ARFUN03 "
        "+2.6, 0 down), ≥50 +1, cs exact +33 · every other gate EXACT · plateau 0 of 3 (≥50 and cs moved — neither counts nor resets)\n")
st = st.replace(o, line + o)
o = "- Every shipped round r314–r433 is ONE line"; assert st.count(o) == 1
st = st.replace(o, "- Every shipped round r314–r434 is ONE line")
o = "`DIFF_QUEUE.md` 22 Sept 22:48 on the r433 corpus (2,491 pairs / 533 modules), 198 CANDIDATE rows"; assert st.count(o) == 1
st = st.replace(o, "`DIFF_QUEUE.md` 22 Sept 23:32 on the r434 corpus (2,491 pairs / 533 modules), 198 CANDIDATE rows")
lines = st.split("\n")
idx = [i for i, l in enumerate(lines) if l.startswith("- **ROUND 434 IN FLIGHT — NOT PROVEN**")]
assert len(idx) == 1
lines[idx[0]] = ("- **No round in flight** (22 Sept 2026 ≈23:45, session 36 Round 2: r434 SHIPPED and committed; the corpus on disk IS the r434 state; the "
                 "r434 record is in LOOP_STATE_ARCHIVE.md 'Session 36 — Round 2 (engine r434 …)'). The §3 step-1 rule stands: the next PICK raises "
                 "`ROUND <N> IN FLIGHT — NOT PROVEN` here BEFORE any code is edited.")
st = "\n".join(lines)
o = "- LAST SHIPPED: **r433** (build 260620.06, 22 Sept ≈23:05, session 36 Round 1 — "; assert st.count(o) == 1
st = st.replace(o, ("- LAST SHIPPED: **r434** (build 260620.07, 22 Sept ≈23:45, session 36 Round 2 — the ARFUN phase-tile labels + the title-bar payload "
                    "ownership, `PHASETILELABEL_OFF` / `TITLEPAYLOAD_OFF`; SCOPED regeneration of the 3, scoped #1 since the r433 FULL (7 of headroom); "
                    "**skeleton 54.5349 % @ 2491, ≥50 1547, ≥75 256, ≥90 23, RAW 38.365 %** (+0.0039pp, 3 up / 0 down); cs 15551 / 195 / 793 / 24 (exact "
                    "+33); body 58 / 5 / 203 / 264; clean 2646 / 2691 = 98.33 %; leak 75 / 45; `gate_baseline.json` at r434 (`_note_r434`); "
                    "`outputs/_s36_r434_sk_final.json` the skeleton state; 54.535 / 91.2 = **59.8 % of achievable**; the miner re-run 22 Sept 23:32, 198 "
                    "CANDIDATE; corpus 2699 pages / 545 dirs / 2491 pairs). Before it **r433** (build 260620.06, 22 Sept ≈23:05, session 36 Round 1 — "))
o = "- Plateau window (§4): **0 of 3** — r433 predicted a skeleton move and delivered +0.0090pp"; assert st.count(o) == 1
st = st.replace(o, "- Plateau window (§4): **0 of 3** — r434 predicted a sub-0.02pp skeleton move and delivered +0.0039pp BUT ≥50 +1 and cs exact +33 (neither counts nor resets); r433 predicted a skeleton move and delivered +0.0090pp")
o = "- Standing facts: AppVersion 260620.06 (r433 the MXFUN code-content phase dialect + the FULL backstop, session 36 Round 1, 22 Sept); before it"; assert st.count(o) == 1
st = st.replace(o, "- Standing facts: AppVersion 260620.07 (r434 the ARFUN phase-tile labels + the title-bar payload ownership, session 36 Round 2, 22 Sept); before it 260620.06 (r433 the MXFUN code-content phase dialect + the FULL backstop, session 36 Round 1, 22 Sept); before it")
i0 = st.index("## Session 36 — Round 2 (engine r434) — THE ARFUN PHASE-TILE LABELS")
i1 = st.index("## Session 36 — Round 1 (engine r433, build 260620.06)")
r2 = st[i0:i1]
pointer = ("## Session 36 — Round 2 (engine r434, build 260620.07) — THE ARFUN PHASE-TILE LABELS + THE TITLE-BAR PAYLOAD OWNERSHIP — SHIPPED; the PICK + "
           "what-shipped record is in LOOP_STATE_ARCHIVE.md 'Session 36 — Round 2 (engine r434 …) + what shipped'; the one-line summary is the s36-r2 "
           "Round-log line below.\n\n")
st = st[:i0] + pointer + st[i1:]
shipped = """**WHAT SHIPPED (22 Sept 23:05 → ≈23:45).** `Emit_Templates.json` `body_region.fundamentals_panels.phase_nav_tiles.writer_tile_labels` {enabled, env `PHASETILELABEL_OFF`, payload_pattern `^phase\\s+(?:one|two|…|\\d+)\\b`, black_line_pattern, menu_bound_exclude_alias_words [overview, module introduction]} + `Tag_Lexicon.json` `_meta.head_section_marker_owns_payload` {enabled, env `TITLEPAYLOAD_OFF`}. `ContentConverter.#partitionItems`: the tile-label marking pass (`_phaseTileLabel` on a title-bar item whose colon payload matches, and on a black line of the same shape — ARFUN04's form), skipped by the opener/title branch, the intro-marker search and the render loop; the menu-boundary bound (`#firstPhaseDelimiterIdx` — the ARFUN bracketed opener, the ENFUN red span, r433's MXFUN marker, the TEFUN black line — clears `introIdx` when it sits after the first phase break, unless an `[Overview]` alias sits at or ahead of it). `TagNormaliser.#resolveFragment`: a first-pass HEAD hit on a SECTION_MARKER ends the multi-pass and hands the payload to the remainder. **Three in-round repairs, each caught by a probe:** (1) the toggle was first named `HEADPAYLOAD_OFF` — already round 303's accordion member rule (`InteractiveBuilder.#accHeadPayload`) — so the OFF leg was NOT byte-identical (EXBP901_3_0 lost a built accordion, XDLS902_5_0 an `<h2>`); renamed `TITLEPAYLOAD_OFF`. (2) The first menu-bound draft emptied the eight ENFUN overviews' Learning-intentions menus (−0.8 to −1.8pp each); (3) the second tested the `[Overview]` guard against the first phase BREAK, which re-broke the same eight because the ENFUN dialect's opening red "Phase 1" span precedes its `[Overview]` marker — the guard now keys on the alias. Probes: OFF 2699 / 2699 identical; ON exactly ARFUN02 / ARFUN03 / ARFUN05; `_s36_r434_pagescore.py` 3 up / 0 down +9.6pp-sum (ARFUN05 35.7 → 40.0, ARFUN02 20.4 → 23.1 with the gold's own h1 pair restored, ARFUN03 49.6 → 52.2). Scoped regen of the 3 + a 12-module spot-check (seed 434): fresh 0 stale, the 539 unaffected byte-identical, the sample 12 / 12 identical; `scoped_ship.sh --round 434` PASS (skeleton IMPROVED, ≥50 +1, cs exact +33, everything else HELD — decomposition-proven over 15 modules). Post-ship: `run_all_gates.sh` rc 0, skeleton 54.5311 → 54.5349 % @ 2491 (movers 3, 0 outside the affected set), 49 selftests GREEN, feature index GREEN, the miner 198 CANDIDATE. `_gatecheck.py` declines a verdict after a scoped ship (its mtime test sees the 527 modules the scoped ship deliberately did not rebuild — the r430 / r431 / r432 message); the decomposition is the verdict. Residue: the XDLS902–908 / MXEO202 `[Body]` "Welcome to Lesson N" paragraph flowing into the lesson menu (10 pages / 5 modules) is the next candidate in this lane; ARFUN04 (a 50-file human split against Claude's one file) is not derivable; ARFUN01 has no tile labels and is untouched.
"""
ar = rd(R + "LOOP_STATE_ARCHIVE.md")
assert "## Session 36 — Round 2 (engine r434" not in ar
r2_head = "## Session 36 — Round 2 (engine r434, build 260620.07, 22 Sept 23:05 → ≈23:45) — THE ARFUN PHASE-TILE LABELS + THE TITLE-BAR PAYLOAD OWNERSHIP + what shipped\n\n"
r2_body = r2.split("\n", 1)[1].strip("\n")
wr(R + "LOOP_STATE_ARCHIVE.md", ar.rstrip("\n") + "\n\n" + r2_head + r2_body + "\n\n" + shipped)
o = "- **(r433) The MXFUN family's heading levels + MXFUN01:**"; assert st.count(o) == 1
st = st.replace(o, ("- **(r434) The lesson-menu `[Body]` lead-in (the next candidate in the menu-overrun lane):** XDLS902 / 903 / 904 / 905 / 906 / 908 and MXEO202 "
                    "(10 pages / 5–7 modules, `_s36_r2_overwhat.log`) write a `[Body]` \"Welcome to Lesson N. In this lesson we are learning…\" paragraph after the "
                    "WALT block; the section-stop's `body` safe tag carries it into the lesson menu while the gold keeps it in `#body`. Measure the menu-safe `body` "
                    "rule against the gold corpus-wide (it was proven at r?? on the WALT block alone) before touching it — it is one entry in "
                    "`menu.lesson_menu_section_stop.menu_section_safe_tags`. ARFUN04 (a 50-file human split against Claude's single file; already a "
                    "`page_model_exceptions` row) and ENGJ201's body-`.alert` WALT (1 module / 6 pages) are below floor.\n" + o))
i = st.rfind("**Next session starts with:**"); assert i > 0
st = st[:i] + ("**Next session starts with:** the standing `/loop-start` (health check — the census is 552 gold / 545 Claude dirs / 2,699 Claude pages; the "
               "\"Amended:\" line; the §7 diff check; `git status` CLEAN at the session-36 commits). No round in flight (r434 shipped by session 36 Round 2 — "
               "see the Position section). **The ship ledger is at scoped #1 since the r433 FULL (7 of headroom).** The open lane is the menu-overrun residue: "
               "the XDLS / MXEO202 `[Body]` lesson-menu lead-in (10 pages / 5 modules — the Follow-up section's top line), then CEDR302's KWL headings (24 "
               "elements), ENGJ201 (14), MXEO202 (8); then the miner's 198 rows re-read on the r434 corpus, the KB queue, the widget census and the loss ledger. "
               "NEEDS CHRIS: the open lines of the \"Needs Chris\" section.\n")
wr(R + "LOOP_STATE.md", st)
print("finalise OK")
