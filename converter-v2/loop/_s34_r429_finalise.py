#!/usr/bin/env python3
"""r429 finalise (OPERATING_GUIDE §12) — session 34 Round 4 (22 Sept 2026): changelog entry, Config.js 260620.01 -> 260620.02,
OPERATING_GUIDE §9 / §11 / §14, gate_baseline.json (round 429), LOOP_STATE.md (Round-log line, the Position bullets — the IN-FLIGHT
marker CLEARED — plateau 1 of 3, standing facts, the next-session line; the Round 3 PICK-pass record and the Round 4 PICK section
MOVED to the archive with the what-shipped record; a follow-up line added), LOOP__Autonomous_Rounds.md §0 (the census-table build).
Exact-text edits only; every anchor asserted. Run under WSL: python3 _s34_r429_finalise.py
"""
import re, json
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
PF = R + "pageforge-site/converter-v2/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

entry = """## 2026-09-22 (round 429, build 260620.02) — THE r100 INQUIRY MODE'S OPENER ROBUSTNESS + the TWHR9 registry row: a `[Tabs]` widget's consumed members never fire the mode, a labelled tab with no number in its bracket OPENS a panel, an EMPTY lead segment folds into the first opener's panel, an empty crumb takes its panel's heading (`inquiry_tabs.openers_unconsumed_only` / `empty_intro_folds`, `INQCONSUMED_OFF` / `INQEMPTYINTRO_OFF`); TWHR9 single-file (+ TWHR905 / TWHR907) — the autonomous loop's session 34 Round 4 (§1d exception 1, the Inquiry-template dialect); 11 modules / 11 pages, 6 up / 1 down (named), +33.6pp-sum; SCOPED regeneration of the 11, scoped ship #4 since the intake FULL

### 1. WHAT CHANGED

**The class (§1d exception 1 — the Inquiry template's own r100 mode on the PANELS-DIFF pages the r428 census left: CEDK102 7 vs the gold's 6 panels, CEDR204 7 vs 6, TWHR907 2 vs 4, TWHK907 2 vs 5, TWHA902 5 vs 9, and TWHR905 with no shell at all; authority §1b level 1 — KB 06_TEMPLATE_RECOGNITION.md lines 169 / 171, the same rule as r428).** Four defects, each measured on the item stream (`_s34_r2_items.cjs`): **(a)** the r100 detection counted EVERY `tab n` item — a `[Tabs]` WIDGET's consumed `[Tab]` members (TWHR907 items 115 / 123 / 151) counted as "empty openers", so the mode fired on pages whose real openers carry no digit; **(b)** a labelled tab with NO number in its bracket (`[New tab] 2` — the index typed outside the bracket; `[New side tab] Values` — the panel named there) was "captured" as a list label with no index (`inquiryLabels[n]` needs a digit) and opened nothing — 2 panels with an empty crumb where the gold has 4 / 5; **(c)** the r100 default build always prepended a synthetic `Introduction` panel (`crumb_intro`, `rel="intro"`) even when the lead segment before the first opener was EMPTY (CEDK102 / CEDR204 / TWHA902's `[TAB 1]` at the very start — the writer's first opener IS the introduction), giving N + 1 panels where the gold has N; and a lead segment holding only a writer's note (TWHR907's DEV note) read as content; **(d)** TWHR905 / TWHR907 (the 22 Sept intake's two TWHR golds, both ONE Inquiry page) were not members of the `TWHR9` registry level (whose four July members have no gold) and resolved multi-file — no inquiry mode could fire on them.

**The fix.** `ContentConverter`: `inquiry_tabs.openers_unconsumed_only` — `_tabItems` (so `_labeledTabs` / `_emptyOpeners` / `_trueOpeners`) counts UNCONSUMED tab items only (a widget's members are the widget's); `nodigit_labelled_opens` — in the r100 body branch, on a single-file page in the BLL-form mode (not the r422 side-tab mode; the EX multi-file family stays the r112-deferred structure), a labelled tab whose bracket carries no number closes any open activity and OPENS a panel: a bare number is no label (the panel's heading decides), any other label becomes that panel's crumb. `PanelsBuilder.inquiryPanels`: `inquiry_tabs.empty_intro_folds` — in the r100 default build a lead segment with no text and no media (writers' notes and red flags stripped first) is not a panel: the first opener's panel takes crumb 1 (the list's label for index 1, else `intro_label`) and the panels run 1..N in the page_split form (`rel="1"` showing); an empty crumb takes its panel's first title heading (colon lead-ins and bare numbers skipped, the English part before ' | '); the r428 fallback's `hasIntro` test strips the same notes, and an opener worded "Introduction" at the very start takes `intro_label`; single-file pages only (`foldEmptyIntro`). `Style_Anchor_Registry`: the TWHR9 level gains TWHR905 / TWHR907 as members and `page_model: single-file` (`_r429_note`; the pre-round file in `_s34_r429_pre/` is the data reversal). Env `INQCONSUMED_OFF` (both ContentConverter rules) and `INQEMPTYINTRO_OFF` (the build rules).

**What it builds (`_s34_r428_shellprobe.cjs`, crumbs / panels vs the gold):** CEDK102 6 / 6 = the gold's set; CEDR204 6 / 6 = the gold's; TWHR907 4 / 4 (`Introduction | Values | Communication | Leadership styles` = the gold); TWHK907 4 / 5 (the WT's `[Tab 1] [MODULE INTRODUCTION]` + `[New tab] 2 / 3 / 4` — the gold's fifth has no marker); TWHR905 2 / 5 (the r428 fallback on the now single-file page — the WT carries few markers); TWHA902 4 / 9 (the empty intro folded; three labelled openers the scanner swallowed into widgets stay lost — the r101 recovery covers empty trailing openers only); CEDW101 5 / 5 = the gold's (its `[Side tabs]` list, no longer counted, lets the fallback take the list and suppress the widget box). Crumb text only on BLL170, MXFUN02 / 03 (empty crumbs now carry their headings); CBI1004 page 8 (a Standard module): two orphan `[Tab N] label` items the r100 mode used to swallow silently now render as the writer's text with the standing orphan red flag — content fidelity, gate-neutral on the page.

### 2. PROOF

- `_s34_r429_probe_run.sh` (all 545 modules, 4 shards; OFF = `INQCONSUMED_OFF=1 INQEMPTYINTRO_OFF=1` with the pre-round registry `--pre _s34_r429_pre`): **OFF = 2699 / 2699 identical, 0 changed** — the toggle-OFF corpus IS the r428 corpus; **ON = exactly 11 pages in 11 modules** (BLL170, CBI1004, CEDK102, CEDR204, CEDW101, MXFUN02, MXFUN03, TWHA902, TWHK907, TWHR905, TWHR907; 2688 identical — every r428 page, every BLL / CED / EX page untouched).
- SCOPED regeneration (`_s34_r429_regen.sh`: the 11 + a 12-module spot-check sample seed 429, 23 / 23 fresh): `scoped_ship.sh --affected _affected_r429.txt --toggle INQCONSUMED_OFF --round 429 --no-regen --commit` (`_s34_r429_scoped_ship.log`) — toggle-exists ✓, content-hash **0 truly stale**, containment **11 ⊆ 11** ✓, spot-check **12 / 12 byte-identical** ✓, the exact decomposition: **skeleton 54.35 → 54.36 IMPROVED, ≥50 1536 / ≥75 254 HELD, cs exact 15431 → 15442 IMPROVED (+11), EXTRA 195 / missing 790 HELD, body 262 HELD, clean 98.33 HELD, leak 75 / 45 HELD**; baseline PATCHED + manifest refreshed. Per page (`_s34_r429_decomp.log`): TWHR905 12.2 → 49.1, TWHA902 26.8 → 27.5, TWHK907 40.3 → 40.8, CEDW101 69.7 → 70.1, CEDK102 41.5 → 41.8, CEDR204 37.3 → 37.6, **TWHR907 39.1 → 33.7 NAMED** — its four panels now match the gold's four, but the r385 panel-title post-pass promotes each panel's first heading to `h2` (three `h3` → `h2`: "What do values have to do with leadership?", "3. Listening", "Styles of Leadership") where the TWH gold keeps them `h3`, and the old two-panel build paid that on one heading only; the companion rises — compare_structure matched / exact 12 / 12 → 15 / 15 (+3 / +3) on the page, RAW 25.8 → 21.5 with it. The panel-title level by family (TWH keeps h3) is recorded under Follow-up candidates.
- `_s34_r429_postship.sh` (`_s34_r429_gates.log`): `run_all_gates.sh` rc 0 — skeleton state `_s34_r429_sk_final.json` **54.3468 → 54.3603 % @ 2491 pairs (+0.0135pp; 6 up / 1 down, +33.6pp-sum, 0 movers outside the set)**, ≥50 1536, ≥75 254, ≥90 23, RAW 38.217 → 38.225 %, median 55.3; compare_structure **15442** / 195 / 790 / 23; body_compare 56 / 5 / 203 / 262 EXACT; clean 2646 / 2691 = 98.33 %; leak 75 / 45; tags 9557 / 9557; every verifier ✓; 49 selftest PASS / 0 FAIL; feature index GREEN; the ledger scoped #4 since the intake FULL (4 of headroom); `_gatecheck.py` refused on its mtime assertion (a scoped round); the miner re-run 16:00 → 196 CANDIDATE.

### 3. PROTECTED GATES (all HELD or IMPROVED, the one page dip NAMED — `_s34_r429_gates.log`, `_s34_r429_scoped_ship.log`, `_s34_r429_skdelta.log`)

- **Skeleton (PRIMARY)**: SCAFFOLD **54.3603 % @ 2491 pairs** (+0.0135pp; 6 up / 1 down, TWHR907 −5.4 named with its companion cs exact +3); ≥50 **1536**, ≥75 **254**, ≥90 **23**, RAW **38.225 %**; skipped 0.
- **compare_structure** 15442 / 195 / 790 / 23 (exact +11); **body_compare** 56 / 5 / 203 / 262 EXACT; **defect** clean 2646 / 2691 = 98.33 %, leak 75 / 45 EXACT; tags 9557 / 9557; every verifier EXACT.
- Plateau (§4): the PICK predicted a skeleton move; +0.0135pp < 0.02pp and no other protected gate moved — the window is **1 of 3** (r428 had reset it).

"""
p = PF + "BUILD_CHANGELOG.md"; s = rd(p)
head, rest = s.split("\n", 1)
assert head.startswith("# BUILD CHANGELOG") and rest.lstrip("\n").startswith("## 2026-09-22 (round 428, build 260620.01)")
wr(p, head + "\n\n" + entry + rest.lstrip("\n"))

p = PF + "app/js/Config.js"; s = rd(p)
old = '\tstatic AppVersion = "260620.01";'; assert s.count(old) == 1
note = ("\t// ROUND 429 (260620.02): THE r100 INQUIRY MODE'S OPENER ROBUSTNESS + the TWHR9 registry row — a [Tabs] widget's consumed members never count as "
        "the mode's openers, a labelled tab with no number in its bracket ([New tab] 2, [New side tab] Values) OPENS a panel, an EMPTY lead segment (notes "
        "stripped) folds into the first opener's panel instead of a synthetic intro, an empty crumb takes its panel's heading (inquiry_tabs."
        "openers_unconsumed_only / empty_intro_folds; env INQCONSUMED_OFF / INQEMPTYINTRO_OFF); TWHR9 single-file with TWHR905 / TWHR907 as members. The "
        "loop's session 34 Round 4 (LOOP §1d exception 1 — the Inquiry-template dialect): OFF probe 2699 / 2699 identical, ON = exactly 11 pages / 11 "
        "modules; scoped regeneration of the 11; skeleton 54.3468 -> 54.3603 % @ 2491 (+0.0135pp, 6 up / 1 down named), cs exact +11, every other gate EXACT.\n")
wr(p, s.replace(old, note + '\tstatic AppVersion = "260620.02";'))

p = PF + "OPERATING_GUIDE.md"; s = rd(p)
old9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 428 BASELINE ("; assert s.count(old9) == 1
new9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 429 BASELINE (the r100 inquiry mode's opener robustness + the TWHR9 row — "
        "`INQCONSUMED_OFF` / `INQEMPTYINTRO_OFF`; SCOPED regeneration of the 11, scoped ship #4 since the intake FULL): SCAFFOLD mean 54.3603% / >=50% 1536 / "
        ">=75% 254 / >=90% 23 / RAW 38.225% @ 2491 pairs, pairs skipped 0 — 6 up / 1 down (TWHR907 −5.4 named: the r385 h2 promotion on three panel headings the "
        "TWH gold keeps h3; cs exact +3 on the page), +33.6pp-sum, 0 movers elsewhere; cs 15442 / 195 / 790 / 23 (exact +11), body 56 / 5 / 203 / 262 EXACT, clean "
        "2646 / 2691 = 98.33 %, leak 75 / 45 EXACT.** Previous — ROUND 428 BASELINE (")
s = s.replace(old9, new9)
old11 = "| `INQFALLBACK_OFF` | 428 |"; assert s.count(old11) == 1
row11 = ("| `INQCONSUMED_OFF` / `INQEMPTYINTRO_OFF` | 429 | **THE r100 INQUIRY MODE'S OPENER ROBUSTNESS + the TWHR9 registry row** (the autonomous loop's "
         "session 34 Round 4; LOOP §1d exception 1 — the Inquiry-template dialect; KB 06 lines 169 / 171). `inquiry_tabs.openers_unconsumed_only`: the r100 "
         "detection's `_tabItems` counts UNCONSUMED tab items only — a `[Tabs]` widget's members never fire the mode (TWHR907 / TWHK907 fall to the r428 "
         "fallback); `nodigit_labelled_opens`: on a single-file page in the BLL-form mode a labelled tab whose bracket carries no number OPENS a panel "
         "(`[New tab] 2` — a bare number is no label; `[New side tab] Values` — the panel's crumb). `inquiry_tabs.empty_intro_folds`: the r100 default "
         "build's lead segment with no text / media (notes stripped) is not a panel — the first opener's panel takes crumb 1 and the panels run 1..N "
         "(`rel=\"1\"` showing); an empty crumb takes its panel's first title heading; the r428 fallback's `hasIntro` strips notes too; single-file pages "
         "only. `Style_Anchor_Registry` TWHR9: members += TWHR905 / TWHR907, `page_model: single-file` (both golds one page). OFF probe 2699 / 2699 "
         "identical; ON exactly 11 pages / 11 modules; skeleton +0.0135pp (TWHR905 12.2 → 49.1; TWHR907 −5.4 named), cs exact +11; every other gate EXACT. |\n")
s = s.replace(old11, row11 + old11)
old14 = "- **Build:** `260620.01` (round 428 — **THE INQUIRY-TEMPLATE FALLBACK SHELL**"; assert s.count(old14) == 1
b14 = ("- **Build:** `260620.02` (round 429 — **THE r100 INQUIRY MODE'S OPENER ROBUSTNESS + the TWHR9 registry row** — `inquiry_tabs.openers_unconsumed_only` "
       "(+ `nodigit_labelled_opens`) and `inquiry_tabs.empty_intro_folds`, env `INQCONSUMED_OFF` / `INQEMPTYINTRO_OFF`; TWHR9 single-file with TWHR905 / TWHR907; "
       "the autonomous loop's session 34 Round 4 under §1d exception 1; OFF probe 2699 / 2699 identical, ON = exactly 11 pages / 11 modules; **SCOPED regeneration "
       "of the 11 (scoped ship #4 since the intake FULL)**; **ROUND 429 BASELINE: SCAFFOLD mean 54.3603% / >=50% 1536 / >=75% 254 / >=90% 23 / RAW 38.225% @ 2491 "
       "pairs** — +0.0135pp, 6 up / 1 down (TWHR907 named), +33.6pp-sum; cs 15442 / 195 / 790 / 23 (exact +11), body 56 / 5 / 203 / 262, clean 2646 / 2691, leak "
       "75 / 45; every verifier EXACT; 49 selftest PASS; the miner 196; plateau window 1 of 3). Previous: ")
s = s.replace(old14, b14 + old14)
wr(p, s)

p = R + "CONVERTER_V2/reference/tests/gate_baseline.json"; s = rd(p)
def setv(key, old, new):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=1); assert n == 1, key
setv("build", '"260620.01"', '"260620.02"'); setv("round", 428, 429)
setv("mean_scaffold_pct", 54.35, 54.36); setv("raw_mean_pct", 38.22, 38.23); setv("exact_chain", 15431, 15442)
a = '    "_note_r428": "Round 428 (session 34 Round 2, 2026-09-22)'; assert s.count(a) == 1
s = s.replace(a, '    "_note_r429": "Round 429 (session 34 Round 4, 2026-09-22; LOOP §1d exception 1 — the Inquiry-template dialect): the r100 inquiry mode\'s opener robustness — a [Tabs] widget\'s consumed members never count as openers, a labelled tab with no number in its bracket opens a panel, an EMPTY lead segment (notes stripped) folds into the first opener\'s panel, an empty crumb takes its panel\'s heading (inquiry_tabs.openers_unconsumed_only / empty_intro_folds; env INQCONSUMED_OFF / INQEMPTYINTRO_OFF) + the TWHR9 registry row (single-file, TWHR905 / TWHR907 members). OFF probe 2699 / 2699 identical, ON = exactly 11 pages / 11 modules; SCOPED regeneration of the 11 (scoped #4 since the intake FULL). Skeleton 54.3468 -> 54.3603 @ 2491 (+0.0135pp; 6 up / 1 down — TWHR907 39.1 -> 33.7 NAMED: the r385 h2 promotion on three panel headings the TWH gold keeps h3, cs exact +3 on the page; TWHR905 12.2 -> 49.1), RAW 38.217 -> 38.225; cs exact 15431 -> 15442 (+11), EXTRA / missing / row-wrap EXACT; body, defect, leak, every verifier EXACT. Plateau window 1 of 3.",\n' + a)
a2 = '    "_note_r428": "Round 428: SCAFFOLD 54.1406 -> 54.3468'; assert s.count(a2) == 1
s = s.replace(a2, '    "_note_r429": "Round 429: SCAFFOLD 54.3468 -> 54.3603 @ 2491 pairs (+0.0135pp; TWHR905 12.2 -> 49.1, TWHA902 26.8 -> 27.5, TWHK907 40.3 -> 40.8, CEDW101 69.7 -> 70.1, CEDK102 41.5 -> 41.8, CEDR204 37.3 -> 37.6, TWHR907 39.1 -> 33.7 named); >=50 1536 / >=75 254 / >=90 23 EXACT; RAW 38.217 -> 38.225; median 55.3. State outputs/_s34_r429_sk_final.json.",\n' + a2)
a3 = '    "_note_r428": "Round 428: exact 15372 -> 15431'; assert s.count(a3) == 1
s = s.replace(a3, '    "_note_r429": "Round 429: exact 15431 -> 15442 (+11), the matched pool 17938 -> 17953 (+15) on the 11 pages (TWHR905 +5 / +1, CEDW101 +4 / +4, TWHR907 +3 / +3); EXTRA 195 / missing 790 / row-wrap 23 EXACT.",\n' + a3)
a4 = '    "_note_r428": "Round 428: over-capture 56'; assert s.count(a4) == 1
s = s.replace(a4, '    "_note_r429": "Round 429: over-capture 56 / runaway 5 / EMPTY 203 / ANY 262 EXACT on 2691 pages.",\n' + a4)
a5 = '    "_note_r428": "Round 428: clean 2646 / 2691'; assert s.count(a5) == 1
s = s.replace(a5, '    "_note_r429": "Round 429: clean 2646 / 2691 = 98.33, leak 75 occ / 45 pages EXACT.",\n' + a5)
json.loads(s); wr(p, s)

p = R + "LOOP__Autonomous_Rounds.md"; s = rd(p)
o = "Current (22 September 2026, build 260620.01 — after the 22 Sept Round 0d, r426, r427 and r428:"; assert s.count(o) == 1
s = s.replace(o, "Current (22 September 2026, build 260620.02 — after the 22 Sept Round 0d and r426–r429:")
wr(p, s)

st = rd(R + "LOOP_STATE.md")
o = "- s34-r2 (engine r428, build 260620.01"; assert st.count(o) == 1
line = ("- s34-r4 (engine r429, build 260620.02, 22 Sept 15:30 → ≈16:10) · THE r100 INQUIRY MODE'S OPENER ROBUSTNESS + the TWHR9 row (§1d exception 1, the "
        "Inquiry-template dialect) — a `[Tabs]` widget's consumed members never fire the mode, a labelled tab with no number in its bracket opens a panel, an "
        "EMPTY lead segment (notes stripped) folds into the first opener's panel, an empty crumb takes its heading (`INQCONSUMED_OFF` / `INQEMPTYINTRO_OFF`); "
        "TWHR9 single-file + TWHR905 / TWHR907 · OFF probe 2699 / 2699 identical · ON exactly 11 pages / 11 modules · SCOPED regen of the 11 (scoped #4) · "
        "skeleton 54.3468 → 54.3603 % @ 2491 (+0.0135pp; 6 up / 1 down — TWHR907 −5.4 NAMED, the r385 h2 promotion vs the TWH gold's h3, cs exact +3), cs "
        "exact +11, all else EXACT · CEDK102 / CEDR204 / TWHR907 / CEDW101 = the gold's panel sets · plateau window 1 of 3\n"
        "- s34-r3 (no engine change, 22 Sept ≈15:10 → 15:28) · PICK PASS on the r428 corpus — every §4 lane: the miner's re-mined queue (the new rows are r428 "
        "re-alignments; #4196 a difflib artefact; the chip facts F7 / F15 a per-module scatter), the dashboard rebuilt (coverage 50.7 %; the 50 intake modules' "
        "largest un-built shape 11 sites), the loss ledger re-run (46.94pp; Bilingual 63.68 = the quiz-engine types), the image row (8 pages, declined), the KB "
        "queue (none ≥ 20), recognition (the 7 no-source) → the one Inquiry-family dialect taken as r429. Full text: archive 'Session 34 — Round 3 PICK pass'.\n")
st = st.replace(o, line + o)
o = "- Every shipped round r314–r428 is ONE line"; assert st.count(o) == 1
st = st.replace(o, "- Every shipped round r314–r429 is ONE line")
o = "`DIFF_QUEUE.md` 22 Sept 15:03 on the r428 corpus (2,491 pairs / 533 modules), 196 CANDIDATE rows"; assert st.count(o) == 1
st = st.replace(o, "`DIFF_QUEUE.md` 22 Sept 16:00 on the r429 corpus (2,491 pairs / 533 modules), 196 CANDIDATE rows")
lines = st.split("\n")
idx = [i for i, l in enumerate(lines) if l.startswith("- **ROUND 429 IN FLIGHT — NOT PROVEN**")]
assert len(idx) == 1
lines[idx[0]] = ("- **No round in flight** (22 Sept 2026 ≈16:10, session 34 Round 4: r429 SHIPPED and committed; the corpus on disk IS the r429 state; the r429 "
                 "record is in LOOP_STATE_ARCHIVE.md 'Session 34 — Round 4 (engine r429 …)'). The §3 step-1 rule stands: the next PICK raises "
                 "`ROUND <N> IN FLIGHT — NOT PROVEN` here BEFORE any code is edited.")
st = "\n".join(lines)
o = "- LAST SHIPPED: **r428** (build 260620.01, 22 Sept ≈15:20, session 34 Round 2 — "; assert st.count(o) == 1
st = st.replace(o, ("- LAST SHIPPED: **r429** (build 260620.02, 22 Sept ≈16:10, session 34 Round 4 — the r100 inquiry mode's opener robustness + the TWHR9 row, "
                    "`INQCONSUMED_OFF` / `INQEMPTYINTRO_OFF`; SCOPED regeneration of the 11, scoped #4 since the intake FULL; **skeleton 54.3603 % @ 2491, ≥50 1536, "
                    "≥75 254, ≥90 23, RAW 38.225 %** (+0.0135pp, 6 up / 1 down named); cs 15442 / 195 / 790 / 23; body 56 / 5 / 203 / 262; clean 2646 / 2691 = 98.33 %; "
                    "leak 75 / 45; `gate_baseline.json` at r429 (`_note_r429`); `outputs/_s34_r429_sk_final.json` the skeleton state; 54.360 / 91.2 = **59.6 % of "
                    "achievable**; the miner re-run 22 Sept 16:00, 196 CANDIDATE; corpus 2699 pages / 545 dirs / 2491 pairs). Before it **r428** (build 260620.01, "
                    "22 Sept ≈15:20, session 34 Round 2 — "))
o = "- Plateau window (§4): **0 of 3** — r428 predicted a skeleton move and delivered +0.2062pp (the window resets);"; assert st.count(o) == 1
st = st.replace(o, "- Plateau window (§4): **1 of 3** — r429 predicted a skeleton move and delivered +0.0135pp with no other gate moving (counts); r428 predicted a skeleton move and delivered +0.2062pp (the window had reset);")
o = "- Standing facts: AppVersion 260620.01 (r428 the Inquiry-template fallback shell, session 34 Round 2, 22 Sept); before it"; assert st.count(o) == 1
st = st.replace(o, "- Standing facts: AppVersion 260620.02 (r429 the r100 opener robustness + the TWHR9 row, session 34 Round 4, 22 Sept); before it 260620.01 (r428 the Inquiry-template fallback shell, session 34 Round 2, 22 Sept); before it")
# the Round 3 PICK-pass record + the Round 4 PICK section → the archive
i0 = st.index("## Session 34 — Round 3 PICK pass (no engine change; 22 Sept ≈15:10 → 15:28)")
i1 = st.index("## Session 34 — Round 4 (engine r429, IN FLIGHT from 15:30 NZST 22 Sept)")
i2 = st.index("## Session 34 — Round 2 (engine r428, build 260620.01)")
r3 = st[i0:i1]; r4 = st[i1:i2]
pointer = ("## Session 34 — Round 3 PICK pass (no engine change) and Round 4 (engine r429, build 260620.02) — THE r100 INQUIRY MODE'S OPENER ROBUSTNESS + the TWHR9 row — SHIPPED; "
           "the PICK-pass record, the PICK + what-shipped record are in LOOP_STATE_ARCHIVE.md 'Session 34 — Round 3 PICK pass' / 'Session 34 — Round 4 (engine r429 …) + what shipped'; "
           "the one-line summaries are the s34-r3 / s34-r4 Round-log lines below.\n\n")
st = st[:i0] + pointer + st[i2:]
shipped = """**WHAT SHIPPED (22 Sept 15:30 → ≈16:10).** `Emit_Templates.json` `inquiry_tabs.openers_unconsumed_only` (enabled, env `INQCONSUMED_OFF`, `nodigit_labelled_opens`) + `inquiry_tabs.empty_intro_folds` (enabled, env `INQEMPTYINTRO_OFF`, `heading_fallback`). `ContentConverter.js`: `_tabItems` counts unconsumed tab items only; the r100 body branch opens a panel on a labelled no-digit tab (BLL-form mode, single-file, not the side-tab mode — a bare number is no label); `foldEmptyIntro: _singleFile` passed to the builder. `PanelsBuilder.js`: the r100 default build's empty-lead fold (notes stripped; page_split form, `rel="1"` showing; an empty crumb takes its first title heading), the fallback's `hasIntro` strips notes and an intro-worded first opener takes `intro_label`. `Style_Anchor_Registry.json`: TWHR9 members += TWHR905 / TWHR907, `page_model: single-file` (`_r429_note`; `_s34_r429_pre/` the pre-round file). Probe OFF (both envs + `--pre`) = 2699 / 2699 identical; ON = exactly 11 pages / 11 modules (`_s34_r429_probe_run.sh`); the first ON pass had also touched FRFUN06 (an extra empty phase — the side-tab mode) and EXBP901 / EXIP901 (new empty panels — the EX multi-file family): both scoped out (`_bllInquiry && !sideTabMode && _singleFile`, `foldEmptyIntro`) before the ship. `_s34_r429_regen.sh` (the 11 + 12 spot-checks seed 429, 23 / 23 fresh); `scoped_ship.sh … --round 429 --commit` PASS (0 truly stale, containment 11 ⊆ 11, spot-check 12 / 12, every gate HELD or IMPROVED). `_s34_r429_postship.sh`: `run_all_gates.sh` rc 0 — **skeleton 54.3468 → 54.3603 % @ 2491 (+0.0135pp; 6 up / 1 down, +33.6pp-sum; 0 outside the set)**: TWHR905 12.2 → 49.1, TWHA902 +0.7, TWHK907 +0.5, CEDW101 +0.4, CEDK102 +0.3, CEDR204 +0.3, **TWHR907 39.1 → 33.7 NAMED** (its four panels = the gold's four, but the r385 panel-title post-pass promotes three `h3` panel headings to `h2` where the TWH gold keeps `h3`; the companion cs matched / exact 12 → 15 on the page; RAW 25.8 → 21.5); ≥50 1536 / ≥75 254 / ≥90 23 EXACT; RAW 38.217 → 38.225; cs 15431 → 15442 exact (+11; the pool +15), 195 / 790 / 23 EXACT; body 56 / 5 / 203 / 262 EXACT; clean 2646 / 2691; leak 75 / 45; every verifier ✓; 49 selftest PASS / 0 FAIL; feature index GREEN; the ledger scoped #4 since the intake FULL; the miner 16:00 → 196 CANDIDATE. Built vs the gold: CEDK102 6 / 6, CEDR204 6 / 6, TWHR907 4 / 4, CEDW101 5 / 5 (the gold's sets); TWHK907 4 / 5, TWHR905 2 / 5, TWHA902 4 / 9. Finalise: `_s34_r429_finalise.py` (the changelog entry, Config.js 260620.02, OPERATING_GUIDE §9 / §11 / §14, `gate_baseline.json` `_note_r429`, LOOP §0's census-table build, this record), `_s34_r429_checksums.sh`, `_s34_r429_mirror.sh`, the commit. Plateau window 1 of 3.
"""
ar = rd(R + "LOOP_STATE_ARCHIVE.md")
assert "## Session 34 — Round 3 PICK pass" not in ar and "## Session 34 — Round 4 (engine r429" not in ar
r3_body = r3.rstrip("\n")
r4_head = "## Session 34 — Round 4 (engine r429, build 260620.02, 22 Sept 15:30 → ≈16:10) — THE r100 INQUIRY MODE'S OPENER ROBUSTNESS + the TWHR9 row + what shipped\n\n"
r4_body = r4.split("\n", 1)[1].strip("\n")
wr(R + "LOOP_STATE_ARCHIVE.md", ar.rstrip("\n") + "\n\n" + r3_body + "\n\n" + r4_head + r4_body + "\n\n" + shipped)
# a follow-up line
o = "- **(r428) The `[Side Tabs]` WIDGET as the inquiry shell (CEDO402).**"; assert st.count(o) == 1
st = st.replace(o, ("- **(r429) The panel's first-heading level by family.** The r385 post-pass promotes every inquiry panel's first own heading to `h2`; the TWH golds keep "
                    "`h3` (TWHR907: three headings, −5.4pp on the page once its four panels matched the gold's four). A per-family `panel_title_level` (the `Style_Anchor_Registry` "
                    "form) needs a census of the panel-heading level per family before a row is written — the BLL golds (the r385 evidence) say h2.\n" + o))
i = st.rfind("**Next session starts with:**"); assert i > 0
st = st[:i] + ("**Next session starts with:** the standing `/loop-start` (health check — the census is 552 gold / 545 Claude dirs / 2,699 Claude pages; the \"Amended:\" line; "
               "the §7 diff check; `git status` CLEAN at the session-34 commits). No round in flight (r429 shipped by session 34 Round 4 — see the Position section). "
               "The session-34 §4 EXHAUSTION verdict (if the STOPPED entry above records one) stands until NEW evidence: an intake (§1f), a KB change, a Needs-Chris "
               "decision (the quiz-engine types #4 are the largest lever — 844 boxes; the lesson-menu repeaters; the dual-build pairing), or a lane no session has "
               "tried. First measurements if a new session runs anyway: the panel first-heading level by family (the r429 follow-up — a registry row if the TWH / CED "
               "golds keep h3), CEDO402's `[Side Tabs]`-widget shell (1 module), and the miner's 196 rows re-read on the r429 corpus. NEEDS CHRIS: the open lines "
               "of the \"Needs Chris\" section.\n")
wr(R + "LOOP_STATE.md", st)
print("finalise OK")
