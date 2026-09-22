#!/usr/bin/env python3
"""r428 finalise (OPERATING_GUIDE §12) — session 34 Round 2 (22 Sept 2026): changelog entry, Config.js 260620.00 -> 260620.01,
OPERATING_GUIDE §9 / §11 / §14, gate_baseline.json (round 428), LOOP_STATE.md (Round-log line, the Position bullets — the
IN-FLIGHT marker CLEARED — plateau, standing facts, the next-session line; the PICK section MOVED to the archive as the
what-shipped record), LOOP__Autonomous_Rounds.md §0 (the census-table build). Exact-text edits only; every anchor asserted.
Run under WSL: python3 _s34_r428_finalise.py
"""
import re, json
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
PF = R + "pageforge-site/converter-v2/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

entry = """## 2026-09-22 (round 428, build 260620.01) — THE INQUIRY-TEMPLATE FALLBACK SHELL: a registry-known Inquiry module on a single-file page whose Writers Template delimits its panels in any of the un-handled dialects builds the KB's `div.crumbs` + `div.inquiryPanel` shell (`inquiry_tabs.template_fallback`, `INQFALLBACK_OFF`) — the autonomous loop's session 34 Round 2; 17 modules / 17 pages, 17 up / 0 down, +513.6pp-sum; SCOPED regeneration of the 17, scoped ship #3 since the intake FULL

### 1. WHAT CHANGED

**The class (the diff miner's rows #4158 `body MISSING div#body › div.inquiryPanel` 37 pages / 34 modules, #9363 `root body.container-fluid.inquiry` 27 / 26, #435 `crumbs MISSING div.crumbs › div` 21 / 18; the 22 Sept intake handover's §4.1 family; authority §1b level 1 — the KB's Inquiry template rule, `06_TEMPLATE_RECOGNITION.md` lines 63 / 169 / 171: body `inquiry container-fluid`, navigation `div.crumbs` → `div.inquiryPanel[rel]`).** The inquiry shell completeness census (`outputs/_s34_r2_inqshell.py` / `.log`, every gold page carrying `div.crumbs` + `inquiryPanel`): **72 gold pages — Claude SHELL-OK 25, PANELS-DIFF 7, SHELL-MISSING 40** (31 Inquiry modules' single pages + EXBP901 / EXIP901's 9 sub-pages, the multi-file EX family the r112 guard excludes). Every SHELL-MISSING page has `<body class="container-fluid">` where the gold has `inquiry container-fluid`; every SHELL-OK page has the gold's — the body class follows the build. The dialect census (`_s34_r2_inqdialects.py` / `.log`): 7 of the 31 are EMPTY Writers Templates (CEDR201 / 301 / 302, CEDT201 / 202 / 203 / 204 — the unfilled template with "Learning outcome/intention" placeholders; no source); the other 24 delimit their panels in ways none of the five inquiry modes (r100 empty `[Tab N]` openers, r102 CED page-split, r111 heading-label, r361 section-nav, r422 side-tab) accept: **(a)** a labelled `[Tab N] label` LIST then labelled REPEATED openers — BLL250 / 260, CEDR101 / 401 (the r100 mode had fired on their "side tabs" instruction, captured the labels and opened NO panel); **(b)** labelled openers with no list — CEDR203, CEDT208, CEDW201 (the list eaten by the scanner as a `[tabs]` / `[Side Tabs]` WIDGET), TWHR907's `[New side tab] Values`; **(c)** the label INSIDE the red span — `[Tab 1: MODULE INTRODUCTION]`, `[Tab 2 – Scenario]`, `[Tab 3 Social Scientist]` (TWHA905 / 904 / 902), `[Tab 1] Biotechnology` (CEDO201), `[Insert Right click tab – ‘The seasons’]` (CEDO202); **(d)** SECTION markers — `[LESSON N] LABEL` (CEDK401), `[LESSON N]` + an `[H2] Lesson N: label` (TWHK901 / 902, TWHT903), `[Lesson N content] label` (CEDT104), `[page N]` + `[H2]` (CEDT102, CEDO204), an `[H2]` per list label after the `[End page]` closers vanished from the stream (CEDW201). The 6 Inquiry golds with NO shell (CHWHA, GEWHA — one page, no openers; ENGFUN02, XDLS901 / 903 / 909 — multi-file) cannot fire a rule that needs ≥ 2 openers on a single-file page.

**The fix — one generic fallback behind the five modes.** `ContentConverter` (after the r361 section-nav detection): `inquiry_tabs.template_fallback` fires when `Module_Structure_Index.module_meta.template_type` is in `template_types` (Inquiry), the page model is single-file, none of the five modes fired — or the r100 mode fired on a "side tabs" instruction with LABELLED tabs only (`_trueOpeners === 0`: it would capture labels and open no panel; it yields, and the effective `inquiryMode` is settled after the check) — and the body holds ≥ `min_openers` (2) panel openers. OPENERS (top level; an open activity closed first, the r100 idiom): an unconsumed `[Tab N …]` item in one of `tab_opener_patterns` (`[Tab N …]`, `[New side tab]`, `[Insert Right click tab – …]`, `[Side Tab N]`; `[Template tab here]` is an instruction) that is not part of the writer's crumb LIST; a `lesson` / `page` PAGE_BOUNDARY carrying a digit (`[Lesson Summary]` is not one); a `lesson content` SECTION_MARKER only when the page has neither ≥ 2 tab openers nor ≥ 2 boundaries; with a list in hand, a top-level `[H1–H3]` whose text is one of the list's labels. THE LIST: the first run of ≥ `list_min` (3) consecutive labelled tabs (blank runs between allowed) — the r100 capture: its labels are the crumbs, the items render nothing (`_inquiryCrumb`); a list the scanner read as a bare `tabs` / `[Side Tabs]` bundle (only labelled tabs, blanks, the opener and at most one trailing swallowed heading — CEDW201's `[H2] Introduction`, released back to the body) is taken as the list and the bundle suppressed (the r102 consumed-crumb-list rule). PAIRS: a `[Tab N] label` and its `[page N]` twin are ONE opener whichever comes first, even with a writer note between them (BLL250 / 260 write both on every panel); a repeated label continues its panel (BLL260's second `[Tab 7] thr`, CEDO201's second `[Tab 5] Antibacterial`). LABELS, in order: the list's entry for that panel; the opener's own words — the red span's words after the tag words (`[Tab 2 – Scenario]` → Scenario; `[LESSON 6] A COMMUNITY INITIATIVE` → A community initiative, ALL-CAPS folded to sentence case; a descriptive bracket that strips to nothing, `[Tab 1: MODULE INTRODUCTION]`, names no label), else a black tail of ≤ `label_max_words`; else, in `PanelsBuilder.inquiryPanels` `fallbackMode`, the panel's first TITLE heading (a colon-ended lead-in "We are learning to:" and a bare "Lesson N" skipped; the English part before ' | '; a leading "Lesson N:" stripped; ALL-CAPS folded), else — panel 1 only — `intro_label` (`Introduction`; `Intro` for the CEDK / CEDO prefixes, `intro_label_by_prefix`). PANELS: the lead segment before the first opener is its own intro panel when it holds real content (`intro_min_chars` 40 of text, a heading or media — CEDK401's module introduction) and folds into panel 1 otherwise (TWHA905's `[Tab 1: MODULE INTRODUCTION]` IS the introduction); an empty trailing segment is dropped. The built page takes the inquiry body class + footer class through `content.inquiryActive` as every other mode does; its footer LINKS stay the registry's own (BLL250 / CEDO201 / TWHK901 already carried the r360 inquiry set). Data `body_region.inquiry_tabs.template_fallback`; env **`INQFALLBACK_OFF`** (or `INQUIRYTABS_OFF`).

**What it builds, against the gold (`_s34_r428_shellprobe.cjs`, crumbs / panels).** BLL250 6 / 6 — `Introduction | Silent b | sc | eigh | augh | ough` = the gold; BLL260 7 / 7 = the gold; CEDR101 8 / 8 (the gold's `Choice – Follow-the-leader` typed `Follow-the-leader`); CEDW201 5 / 5 = the gold; CEDT208 4 / 4 = the gold; CEDO201 6 / 6 = the gold; CEDT102 5 / 5 (the developer renamed two: `Celebrating Differences` → `Diversity`); TWHT903 5 / 5 (renamed); CEDO202 9 / 10; CEDK401 8 / 9 (`[LESSON 5]` is not typed in the WT); CEDR401 5 / 6 (`[Tab 5]` swallowed by a widget); TWHA905 6 / 7 (the gold's `Reflection` has no marker); CEDO204 5 / 6; CEDT104 7 / 8; CEDR203 4 / 5; TWHK901 4 / 5; TWHK902 3 / 5 (its markers are `[Lesson content]` ×2 + `[LESSON] 3`); CEDO402 3 / 6 (the gold's six panels are the WT's `[Side Tabs]` WIDGET with content in each tab — a sixth dialect, recorded, not this round).

**Three gate-tool corrections found by this round's proof (mirrored in `loop/`).** (1) `_scoped_spotcheck.py plan` never samples a `compare_exclusions.txt` module (D10-6): seed 428 drew CEDW303 (an excluded CED revision brief), which entered the scoped decomposition as a NEW PAIR with its own +1 missing container and read as a regression the corpus gates never see. (2) `_fastloop_diff.py run_scoped` honours the same exclusions, and its mtime staleness guard now treats a "drifted" unaffected module whose pages are byte-identical to the content manifest as not drifted (the first spot-check sample, regenerated with the fix ON and proven identical, had blocked the re-run by mtime alone). (3) `_ship_ledger.py record-scoped` is idempotent per round — `scoped_ship.sh` had recorded a scoped ship on EVERY run (three for r428 while the decomposition was being repaired, two for r425 on 21 Sept); the ledger is corrected (`_s34_r428_ledger_fix.py`, `.pre-r428fix.json` kept): scoped #3 since the intake FULL, 5 of headroom.

### 2. PROOF

- `_s34_r428_probe_run.sh` (the r410 in-memory harness over all 545 Claude-dir modules, 4 shards): **OFF (`INQFALLBACK_OFF=1`) = 2699 / 2699 identical, 0 changed** — the toggle-OFF corpus IS the r427 corpus byte-for-byte; **ON = exactly 17 pages in 17 modules changed** (BLL250, BLL260, CEDK401, CEDO201, CEDO204, CEDO402, CEDR101, CEDR203, CEDR401, CEDT102, CEDT104, CEDT208, CEDW201, TWHA905, TWHK901, TWHK902, TWHT903 — every one an Inquiry single page; the 25 SHELL-OK pages, the 7 PANELS-DIFF pages, CHWHA / GEWHA, the 7 empty-WT modules and every non-Inquiry module untouched; 2682 identical).
- SCOPED regeneration (`_s34_r428_regen.sh`: the 17 + a 12-module spot-check sample, 4 batches, 29 / 29 fresh; a second sample after the exclusion fix, 12 / 12 fresh): `scoped_ship.sh --affected _affected_r428.txt --toggle INQFALLBACK_OFF --round 428 --no-regen --commit` (`_s34_r428_scoped_ship.log`) — toggle-exists ✓, content-hash **0 truly stale** (17 affected regenerated; the 525 untouched byte-identical to the manifest), containment **17 ⊆ 17** ✓, spot-check **12 / 12 byte-identical** ✓, the exact decomposition: **skeleton 54.14 → 54.35 IMPROVED, ≥50 1531 → 1536 IMPROVED, ≥75 254 HELD, cs exact 15372 → 15431 IMPROVED (+59), EXTRA 195 / missing 790 HELD, body 262 HELD, clean 98.33 HELD, leak 75 / 45 HELD** (context: pairs 2491, the matched pool 17901 → 17938); baseline PATCHED + manifest refreshed. Per module (`_s34_r428_decomp.log`): cs matched / exact / EXTRA / missing +37 / +59 / 0 / 0 on the 17 alone (BLL250 −3 matched / +5 exact, BLL260 −5 / +7 — the panel wrappers re-pair the same text more exactly).
- `_s34_r428_postship.sh` (`_s34_r428_gates.log`): `run_all_gates.sh` rc 0 — skeleton state `_s34_r428_sk_final.json` **54.1406 → 54.3468 % @ 2491 pairs (+0.2062pp; 17 up / 0 down, +513.6pp-sum, 0 movers outside the set, new-only 0 / gone 0)**, ≥50 1531 → **1536**, ≥75 254, ≥90 23, RAW 38.069 → **38.217 %**, median 55.0 → 55.3; per page CEDR101 11.0 → 68.1, CEDO201 19.7 → 67.8, BLL250 6.7 → 54.1, CEDT208 14.9 → 58.3, TWHT903 12.6 → 52.9, CEDW201 13.7 → 48.6, CEDR401 9.7 → 40.6, BLL260 7.3 → 36.6, CEDT102 13.9 → 42.3, CEDK401 10.1 → 35.2, CEDO402 11.8 → 34.3, TWHK902 11.0 → 32.8, TWHA905 10.5 → 30.2, CEDR203 13.4 → 32.3, CEDO204 17.0 → 28.7, TWHK901 9.3 → 25.7, CEDT104 7.0 → 24.6; compare_structure **15431** / 195 / 790 / 23; body_compare 56 / 5 / 203 / 262 EXACT; clean 2646 / 2691 = 98.33 %; leak 75 occ / 45 pages; tags 9557 / 9557; every verifier ✓ (entry parity, flipCard divergence 0, speechBubble 4 at baseline, pop-outs, MTK quiz shells, MathML, menu labels, dragAndDrop, bingo); 49 selftest PASS / 0 FAIL; feature index GREEN (552 modules); the ledger scoped #3 since the intake FULL; `_gatecheck.py` refused on its mtime assertion (a scoped round — the content-hash proof above is the honest one); the miner re-run 15:03 → 196 CANDIDATE (281,145 diff lines / 9,381 classes, from 285,420 / 9,437): the inquiry rows re-shape — `body MISSING div.inquiryPanel` 37 / 34 → 40 / 37 and `EXTRA` 20 / 20 → 31 / 31 (the miner keys a panel line by its label TEXT: the shells now exist and the writer's / developer's labels differ — the skeleton scorer credits the structure), `crumbs MISSING` 21 / 18 → 22 / 19, the `root body.inquiry` row gone from the candidates.

### 3. PROTECTED GATES (all HELD or IMPROVED — `_s34_r428_gates.log`, `_s34_r428_scoped_ship.log`, `_s34_r428_skdelta.log`)

- **Skeleton (PRIMARY)**: SCAFFOLD **54.3468 % @ 2491 pairs** (+0.2062pp; 17 up / 0 down); ≥50 **1536** (+5), ≥75 **254**, ≥90 **23**, RAW **38.217 %** (+0.148); skipped 0.
- **compare_structure** 15431 / 195 / 790 / 23 (exact +59, the pool +37; EXTRA / missing / row-wrap EXACT); **body_compare** 56 / 5 / 203 / 262 EXACT; **defect** clean 2646 / 2691 = 98.33 %, leak 75 / 45 EXACT; tags 9557 / 9557; every verifier EXACT.
- Plateau (§4): the PICK predicted a skeleton move; +0.2062pp ≥ 0.02 — the window resets to 0 of 3.

"""
p = PF + "BUILD_CHANGELOG.md"; s = rd(p)
head, rest = s.split("\n", 1)
assert head.startswith("# BUILD CHANGELOG") and rest.lstrip("\n").startswith("## 2026-09-22 (round 427, build 260620.00)")
wr(p, head + "\n\n" + entry + rest.lstrip("\n"))

p = PF + "app/js/Config.js"; s = rd(p)
old = '\tstatic AppVersion = "260620.00";'; assert s.count(old) == 1
note = ("\t// ROUND 428 (260620.01): THE INQUIRY-TEMPLATE FALLBACK SHELL — a registry-known Inquiry module (Module_Structure_Index template_type) on a "
        "single-file page whose Writers Template delimits its panels in a dialect none of the five inquiry modes accept (a labelled [Tab N] list + "
        "labelled repeated openers; labelled openers with no list; the label inside the red span; [LESSON N] / [page N] / [Lesson N content] "
        "sections; an [H2] per list label) builds the KB's div.crumbs + div.inquiryPanel shell: ContentConverter's inqFallbackMode pushes the "
        "panel sentinel at every top-level opener (the writer's list captured as the crumbs, a bare tabs bundle of it suppressed; a tab + its "
        "[page N] twin one opener; a repeated label continues its panel), PanelsBuilder.inquiryPanels fallbackMode labels each panel from the "
        "list, the opener's own words or its first title heading. Data inquiry_tabs.template_fallback, env INQFALLBACK_OFF. The loop's "
        "session 34 Round 2: OFF probe 2699 / 2699 identical, ON = exactly 17 pages / 17 modules; scoped regeneration of the 17; skeleton "
        "54.1406 -> 54.3468 % @ 2491 (+0.2062pp, 17 up / 0 down, +513.6pp-sum), >=50 +5, cs exact +59, every other gate EXACT.\n")
wr(p, s.replace(old, note + '\tstatic AppVersion = "260620.01";'))

p = PF + "OPERATING_GUIDE.md"; s = rd(p)
old9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 427 BASELINE ("; assert s.count(old9) == 1
new9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 428 BASELINE (the Inquiry-template fallback shell — "
        "`inquiry_tabs.template_fallback`, `INQFALLBACK_OFF`; SCOPED regeneration of the 17, scoped ship #3 since the intake FULL): SCAFFOLD mean "
        "54.3468% / >=50% 1536 / >=75% 254 / >=90% 23 / RAW 38.217% @ 2491 pairs, pairs skipped 0 — 17 up / 0 down on the 17 alone, +513.6pp-sum "
        "(CEDR101 11.0 → 68.1, CEDO201 19.7 → 67.8, BLL250 6.7 → 54.1 …), 0 movers elsewhere; cs 15431 / 195 / 790 / 23 (exact +59, the pool +37), "
        "body 56 / 5 / 203 / 262 EXACT, clean 2646 / 2691 = 98.33 %, leak 75 / 45 EXACT.** Previous — ROUND 427 BASELINE (")
s = s.replace(old9, new9)
old11 = "| `PREFIXDELTA_OFF` | 427 |"; assert s.count(old11) == 1
row11 = ("| `INQFALLBACK_OFF` | 428 | **THE INQUIRY-TEMPLATE FALLBACK SHELL — a registry-known Inquiry module on a single-file page whose Writers "
         "Template delimits its panels in any of the un-handled dialects builds the KB's `div.crumbs` + `div.inquiryPanel` shell** (the autonomous "
         "loop's session 34 Round 2; KB 06 lines 63 / 169 / 171). `ContentConverter`: `inquiry_tabs.template_fallback` fires when "
         "`module_meta.template_type` is Inquiry, the page is single-file, none of the five modes fired (the r100 mode fired on a \"side tabs\" "
         "instruction with labelled tabs only yields) and the body holds ≥ 2 openers — an unconsumed `[Tab N …]` / `[New side tab]` / `[Insert "
         "Right click tab – …]` / `[Side Tab N]` item outside the writer's crumb LIST (the first run of ≥ 3 consecutive labelled tabs — captured, "
         "never rendered; a bare `tabs` / `[Side Tabs]` bundle of it suppressed, a swallowed heading released), a `[LESSON N]` / `[page N]` "
         "boundary with a digit, a `[Lesson N content]` marker when the page has no other openers, an `[H1–H3]` repeating a list label; a tab + "
         "its `[page N]` twin is ONE opener, a repeated label continues its panel. `PanelsBuilder.inquiryPanels` fallbackMode: the labels from the "
         "list, the opener's own words (`[Tab 2 – Scenario]` → Scenario; `[LESSON 6] A COMMUNITY INITIATIVE` → sentence case) or the panel's first "
         "title heading (colon lead-ins skipped, `Lesson N:` stripped); the intro panel when the lead segment is real (`Introduction`; `Intro` for "
         "CEDK / CEDO). OFF probe 2699 / 2699 identical; ON exactly 17 pages / 17 modules; skeleton +0.2062pp (17 up / 0 down, +513.6pp-sum), "
         "≥50 +5, cs exact +59; every other gate EXACT. |\n")
s = s.replace(old11, row11 + old11)
old14 = "- **Build:** `260620.00` (round 427 — **THE CODE-PREFIX CHIP DELTAS**"; assert s.count(old14) == 1
b14 = ("- **Build:** `260620.01` (round 428 — **THE INQUIRY-TEMPLATE FALLBACK SHELL** — `inquiry_tabs.template_fallback` in `ContentConverter` + "
       "`PanelsBuilder.inquiryPanels` fallbackMode, env `INQFALLBACK_OFF`; the autonomous loop's session 34 Round 2; OFF probe 2699 / 2699 identical, "
       "ON = exactly 17 pages / 17 modules; **SCOPED regeneration of the 17 (scoped ship #3 since the intake FULL)**; **ROUND 428 BASELINE: SCAFFOLD "
       "mean 54.3468% / >=50% 1536 / >=75% 254 / >=90% 23 / RAW 38.217% @ 2491 pairs** — +0.2062pp, 17 up / 0 down, +513.6pp-sum, 0 movers elsewhere; "
       "cs 15431 / 195 / 790 / 23 (exact +59), body 56 / 5 / 203 / 262, clean 2646 / 2691, leak 75 / 45; every verifier EXACT; 49 selftest PASS; the "
       "miner 196; three gate-tool corrections — `_scoped_spotcheck.py` / `_fastloop_diff.py` honour `compare_exclusions.txt`, the fast-loop "
       "staleness guard reads content hashes, `_ship_ledger.py` one ship per round). Previous: ")
s = s.replace(old14, b14 + old14)
wr(p, s)

p = R + "CONVERTER_V2/reference/tests/gate_baseline.json"; s = rd(p)
def setv(key, old, new):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=1); assert n == 1, key
setv("build", '"260620.00"', '"260620.01"'); setv("round", 427, 428)
setv("mean_scaffold_pct", 54.14, 54.35); setv("median_scaffold_pct", 55.0, 55.3); setv("pages_ge_50", 1531, 1536); setv("raw_mean_pct", 38.07, 38.22)
setv("exact_chain", 15372, 15431)
a = '    "_note_r427": "Round 427 (session 33 Round 5, 2026-09-22'; assert s.count(a) == 1
s = s.replace(a, '    "_note_r428": "Round 428 (session 34 Round 2, 2026-09-22): the Inquiry-template fallback shell — a registry-known Inquiry module on a single-file page whose Writers Template delimits its panels in an un-handled dialect builds the KB\'s div.crumbs + div.inquiryPanel shell (ContentConverter inqFallbackMode + PanelsBuilder.inquiryPanels fallbackMode; data inquiry_tabs.template_fallback, env INQFALLBACK_OFF). OFF probe 2699 / 2699 identical, ON = exactly 17 pages / 17 modules; SCOPED regeneration of the 17 (scoped #3 since the intake FULL). Skeleton 54.1406 -> 54.3468 @ 2491 (+0.2062pp; 17 up / 0 down, +513.6pp-sum; 0 movers outside the set), >=50 1531 -> 1536, RAW 38.069 -> 38.217; cs exact 15372 -> 15431 (+59; the matched pool 17901 -> 17938), EXTRA / missing / row-wrap EXACT; body, defect, leak, every verifier EXACT. Three gate-tool corrections in the same round: _scoped_spotcheck.py and _fastloop_diff.py honour compare_exclusions.txt (a sampled excluded module had entered the decomposition as a new pair), the fast-loop staleness guard reads content hashes, _ship_ledger.py records one ship per round.",\n' + a)
a2 = '    "_note_r427": "Round 427: SCAFFOLD 54.1406 -> 54.1406'; assert s.count(a2) == 1
s = s.replace(a2, '    "_note_r428": "Round 428: SCAFFOLD 54.1406 -> 54.3468 @ 2491 pairs (+0.2062pp; 17 up / 0 down: CEDR101 11.0 -> 68.1, CEDO201 19.7 -> 67.8, BLL250 6.7 -> 54.1, CEDT208 14.9 -> 58.3, TWHT903 12.6 -> 52.9, CEDW201 13.7 -> 48.6, CEDR401 9.7 -> 40.6, BLL260 7.3 -> 36.6, CEDT102 13.9 -> 42.3, CEDK401 10.1 -> 35.2, CEDO402 11.8 -> 34.3, TWHK902 11.0 -> 32.8, TWHA905 10.5 -> 30.2, CEDR203 13.4 -> 32.3, CEDO204 17.0 -> 28.7, TWHK901 9.3 -> 25.7, CEDT104 7.0 -> 24.6); >=50 1531 -> 1536 / >=75 254 / >=90 23; RAW 38.069 -> 38.217; median 55.0 -> 55.3. State outputs/_s34_r428_sk_final.json.",\n' + a2)
a3 = '    "_note_r427": "Round 427: exact 15372 / EXTRA 195'; assert s.count(a3) == 1
s = s.replace(a3, '    "_note_r428": "Round 428: exact 15372 -> 15431 (+59), the matched pool 17901 -> 17938 (+37) — all on the 17 fallback-shell pages (BLL250 -3 matched / +5 exact, BLL260 -5 / +7: the panel wrappers re-pair the same text more exactly); EXTRA 195 / missing 790 / row-wrap 23 EXACT.",\n' + a3)
a4 = '    "_note_r427": "Round 427: over-capture 56'; assert s.count(a4) == 1
s = s.replace(a4, '    "_note_r428": "Round 428: over-capture 56 / runaway 5 / EMPTY 203 / ANY 262 EXACT on 2691 pages.",\n' + a4)
a5 = '    "_note_r427": "Round 427: clean 2646 / 2691'; assert s.count(a5) == 1
s = s.replace(a5, '    "_note_r428": "Round 428: clean 2646 / 2691 = 98.33, leak 75 occ / 45 pages EXACT.",\n' + a5)
json.loads(s); wr(p, s)

p = R + "LOOP__Autonomous_Rounds.md"; s = rd(p)
o = "Current (22 September 2026, build 260620.00 — after the 22 Sept Round 0d, r426 and r427:"; assert s.count(o) == 1
s = s.replace(o, "Current (22 September 2026, build 260620.01 — after the 22 Sept Round 0d, r426, r427 and r428:")
wr(p, s)

st = rd(R + "LOOP_STATE.md")
o = "- s33-r5 / s34-r1 (engine r427, build 260620.00"; assert st.count(o) == 1
line = ("- s34-r2 (engine r428, build 260620.01, 22 Sept 14:15 → ≈15:20) · THE INQUIRY-TEMPLATE FALLBACK SHELL — a registry-known Inquiry module on a "
        "single-file page whose WT delimits its panels in an un-handled dialect (a labelled `[Tab N]` list + repeated labelled openers; labelled openers "
        "with no list; the label inside the red span; `[LESSON N]` / `[page N]` / `[Lesson N content]` sections; an `[H2]` per list label) builds the "
        "KB's `div.crumbs` + `div.inquiryPanel` shell (`inquiry_tabs.template_fallback`, `INQFALLBACK_OFF`; KB 06 lines 63 / 169 / 171) · OFF probe "
        "2699 / 2699 identical · ON exactly 17 pages / 17 modules · SCOPED regen of the 17 (scoped #3 since the intake FULL) · skeleton 54.1406 → "
        "54.3468 % @ 2491 (+0.2062pp; 17 up / 0 down, +513.6pp-sum), ≥50 +5, cs exact +59, all else EXACT · three gate-tool corrections (exclusions "
        "in the spot-check / fast-loop, the content-hash staleness guard, one ledger entry per round) · #4235 DECLINED (the half-column image) · "
        "plateau window 0 of 3 (reset)\n")
st = st.replace(o, line + o)
o = "- Every shipped round r314–r427 is ONE line"; assert st.count(o) == 1
st = st.replace(o, "- Every shipped round r314–r428 is ONE line")
o = "`DIFF_QUEUE.md` 22 Sept 12:52 on the r427 corpus (2,491 pairs / 533 modules), 196 CANDIDATE rows"; assert st.count(o) == 1
st = st.replace(o, "`DIFF_QUEUE.md` 22 Sept 15:03 on the r428 corpus (2,491 pairs / 533 modules), 196 CANDIDATE rows")
lines = st.split("\n")
idx = [i for i, l in enumerate(lines) if l.startswith("- **ROUND 428 IN FLIGHT — NOT PROVEN**")]
assert len(idx) == 1
lines[idx[0]] = ("- **No round in flight** (22 Sept 2026 ≈15:20, session 34 Round 2: r428 SHIPPED and committed; the corpus on disk IS the r428 state; the r428 "
                 "record is in LOOP_STATE_ARCHIVE.md 'Session 34 — Round 2 (engine r428 …)'). The §3 step-1 rule stands: the next PICK raises "
                 "`ROUND <N> IN FLIGHT — NOT PROVEN` here BEFORE any code is edited.")
st = "\n".join(lines)
o = "- LAST SHIPPED: **r427** (build 260620.00, 22 Sept 12:52 / finalised ≈14:05, session 33 Round 5 finished by session 34 Round 1 — "; assert st.count(o) == 1
st = st.replace(o, ("- LAST SHIPPED: **r428** (build 260620.01, 22 Sept ≈15:20, session 34 Round 2 — the Inquiry-template fallback shell, `inquiry_tabs.template_fallback` + "
                    "`INQFALLBACK_OFF`; SCOPED regeneration of the 17, scoped #3 since the intake FULL; **skeleton 54.3468 % @ 2491, ≥50 1536, ≥75 254, ≥90 23, RAW "
                    "38.217 %** (+0.2062pp, 17 up / 0 down, +513.6pp-sum); cs 15431 / 195 / 790 / 23; body 56 / 5 / 203 / 262; clean 2646 / 2691 = 98.33 %; leak 75 / 45; "
                    "`gate_baseline.json` at r428 (`_note_r428`); `outputs/_s34_r428_sk_final.json` the skeleton state; 54.347 / 91.2 = **59.6 % of achievable**; the miner "
                    "re-run 22 Sept 15:03, 196 CANDIDATE; corpus 2699 pages / 545 dirs / 2491 pairs). Before it **r427** (build 260620.00, 22 Sept 12:52 / finalised "
                    "≈14:05, session 33 Round 5 finished by session 34 Round 1 — "))
o = "- Plateau window (§4): **0 of 3** — r427 is gate-neutral by design"; assert st.count(o) == 1
st = st.replace(o, "- Plateau window (§4): **0 of 3** — r428 predicted a skeleton move and delivered +0.2062pp (the window resets); r427 is gate-neutral by design")
o = "- Standing facts: AppVersion 260620.00 (r427 the code-prefix chip deltas, session 33 Round 5 finished by session 34 Round 1, 22 Sept); before it"; assert st.count(o) == 1
st = st.replace(o, "- Standing facts: AppVersion 260620.01 (r428 the Inquiry-template fallback shell, session 34 Round 2, 22 Sept); before it 260620.00 (r427 the code-prefix chip deltas, session 33 Round 5 finished by session 34 Round 1, 22 Sept); before it")
# the PICK section → the archive (with the what-shipped record appended), a pointer line stays
i0 = st.index("## Session 34 — Round 2 (engine r428, IN FLIGHT from 14:15 NZST 22 Sept)")
i1 = st.index("## Session 33 — Round 5 (engine r427, crashed after its post-ship suite)")
pick = st[i0:i1]
pointer = ("## Session 34 — Round 2 (engine r428, build 260620.01) — THE INQUIRY-TEMPLATE FALLBACK SHELL — SHIPPED; the PICK-pass record (#4235 declined), "
           "the PICK + what-shipped record are in LOOP_STATE_ARCHIVE.md 'Session 34 — Round 2 (engine r428 …) + what shipped'; the one-line summary is the s34-r2 Round-log line below.\n\n")
st = st[:i0] + pointer + st[i1:]
shipped = """**WHAT SHIPPED (22 Sept 14:15 → ≈15:20).** `Emit_Templates.json` `body_region.inquiry_tabs.template_fallback` (enabled, env `INQFALLBACK_OFF`, `template_types` [Inquiry], `min_openers` 2, `list_min` 3, `label_max_words` 8, `intro_min_chars` 40, `intro_label` Introduction + `intro_label_by_prefix` CEDK / CEDO → Intro, `tab_opener_patterns`, `strip_label_words`, `strip_label_prefix`). `ContentConverter.js`: the fallback detection after the r361 section-nav check (`_fbOn` → `inqFallbackMode`; the r100 `inquiryMode0` yields when it fired on a "side tabs" instruction with labelled tabs only, and the effective `inquiryMode` is settled after the check); the crumb-LIST capture (`fbList` / `fbListLabels`, `_inquiryCrumb`, a bare `tabs` / `[Side Tabs]` bundle of it suppressed via `fbSuppress`, one swallowed trailing heading released); `fbOpen(label, kind)` — the sentinel push with the tab + `[page N]` pairing, the adjacent-opener reuse and the repeated-label continuation; the opener branches in the PAGE_BOUNDARY, SECTION_MARKER (`[Lesson N content]`), ELEMENT (an `[H1–H3]` repeating a list label) and SUBTAG (every `[Tab N …]` form, a long black tail rendered as content) cases; `inquiryActive` includes the fallback. `PanelsBuilder.inquiryPanels` `fallbackMode` (labels from the list / the opener / the first title heading; the intro panel when the lead segment is real; an empty trailing segment dropped). Probe OFF = 2699 / 2699 identical; ON = exactly 17 pages / 17 modules (`_s34_r428_probe_run.sh`, `_s34_r428_shellprobe.cjs`). `_s34_r428_regen.sh` (the 17 + 12 spot-checks, 29 / 29 fresh; a second sample 12 / 12 after the exclusion fix); `scoped_ship.sh … --round 428 --commit` PASS (0 truly stale, containment 17 ⊆ 17, spot-check 12 / 12, every gate HELD or IMPROVED). `_s34_r428_postship.sh`: `run_all_gates.sh` rc 0 — **skeleton 54.1406 → 54.3468 % @ 2491 (+0.2062pp; 17 up / 0 down, +513.6pp-sum; 0 outside the set)**, ≥50 1531 → 1536, ≥75 254 / ≥90 23, RAW 38.069 → 38.217; cs 15372 → 15431 exact (+59), 195 / 790 / 23 EXACT; body 56 / 5 / 203 / 262 EXACT; clean 2646 / 2691 = 98.33 %; leak 75 / 45; every verifier ✓; 49 selftest PASS / 0 FAIL; feature index GREEN; the ledger scoped #3 since the intake FULL (corrected from a triple count — `_s34_r428_ledger_fix.py`); the miner 15:03 → 196 CANDIDATE (the inquiry rows re-shape: `body MISSING inquiryPanel` 37 / 34 → 40 / 37 and `EXTRA` 20 / 20 → 31 / 31 — the miner keys a panel by its label text; `root body.inquiry` gone). **Three gate-tool corrections shipped with it:** `_scoped_spotcheck.py plan` never samples a `compare_exclusions.txt` module (seed 428 drew CEDW303 — a NEW PAIR with a +1 missing container the corpus gates never see); `_fastloop_diff.py run_scoped` honours the exclusions and its staleness guard reads content hashes (the first sample, regenerated and byte-identical, had blocked the re-run by mtime); `_ship_ledger.py record-scoped` one ship per round. **Built vs the gold (crumbs / panels):** BLL250 6 / 6, BLL260 7 / 7, CEDW201 5 / 5, CEDT208 4 / 4, CEDO201 6 / 6 (all the gold's labels); CEDR101 8 / 8, CEDT102 5 / 5, TWHT903 5 / 5 (developer renames); CEDO202 9 / 10, CEDK401 8 / 9, CEDR401 5 / 6, TWHA905 6 / 7, CEDO204 5 / 6, CEDT104 7 / 8, CEDR203 4 / 5, TWHK901 4 / 5, TWHK902 3 / 5; CEDO402 3 / 6 — its gold's six panels are the WT's `[Side Tabs]` WIDGET with content in every tab (a sixth dialect, recorded under Follow-up candidates). Finalise: `_s34_r428_finalise.py` (the changelog entry, Config.js 260620.01, OPERATING_GUIDE §9 / §11 / §14, `gate_baseline.json` `_note_r428`, LOOP §0's census-table build, this record), `_s34_r428_checksums.sh`, `_s34_r428_mirror.sh`, the commit. Plateau window 0 of 3 (reset).
"""
ar = rd(R + "LOOP_STATE_ARCHIVE.md")
sec_head = "## Session 34 — Round 2 (engine r428, build 260620.01, 22 Sept 14:15 → ≈15:20) — THE INQUIRY-TEMPLATE FALLBACK SHELL + what shipped\n\n"
assert "## Session 34 — Round 2 (engine r428" not in ar
pick_body = pick.split("\n", 1)[1].strip("\n")
wr(R + "LOOP_STATE_ARCHIVE.md", ar.rstrip("\n") + "\n\n" + sec_head + pick_body + "\n\n" + shipped)
i = st.rfind("**Next session starts with:**"); assert i > 0
st = st[:i] + ("**Next session starts with:** the standing `/loop-start` (health check — the census is 552 gold / 545 Claude dirs / 2,699 Claude pages; the \"Amended:\" line; "
               "the §7 diff check; `git status` CLEAN at the session-34 commits). No round in flight (r428 shipped by session 34 Round 2 — see the Position section). "
               "Then: the miner's 196-row queue on the r428 corpus under §3 / §4 (chrome first — the remaining chip facts F7 MISSING decimal 81 / 33 NCEA1 c = 0.81 and "
               "F15 EXTRA lesson-number 45 / 16 Refresh c = 0.80; the inquiry panel rows now keyed by LABEL text; then title / module-menu / crumbs / footer), the "
               "Follow-up candidates the r428 record added (the `[Side Tabs]`-widget-as-shell dialect CEDO402; the r100 mode's `[New side tab] label` openers on "
               "TWHR907 / TWHK907 / TWHA902 — PANELS-DIFF 7 pages), the ghost-dir / recognition lane, and the §4 exhaustion test only with every lane tried. "
               "NEEDS CHRIS: the open lines of the \"Needs Chris\" section.\n")
wr(R + "LOOP_STATE.md", st)
print("finalise OK")
