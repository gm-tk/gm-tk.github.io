#!/usr/bin/env python3
"""r416 finalise (CLAUDE.md §12): changelog entry, Config.js bump, CLAUDE.md §9 / §11 / §14, gate_baseline.json. Run under WSL."""
import re, json
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
PF = R + "pageforge-site/converter-v2/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

entry = """## 2026-09-20 (round 416, build 260619.87) — THE ACTIVITY TITLE TYPED INSIDE THE RED SPAN: `[Activity 2A] Concrete poems` all red is the box's `<h3>` (the autonomous loop's session 29 Round 7; THE FULL REGENERATION of all 494 gated dirs — the ledger's backstop after seven scoped ships, 0 stale, the manifest diff = the probe's 44 pages exactly, NO residue from r409–r415; every protected gate HELD-or-IMPROVED, `--accept-named` neither used nor needed)

### 1. WHAT CHANGED

**The class.** A writer types the box title in the SAME red run as the opener — `🔴[RED TEXT] [Activity 2A] Concrete poems [/RED TEXT]🔴`, `[Activity] Calculating soil type.`, `[Activity box:] Ka pai!`, `[Activity individual - 3A] What was Wakefield Thinking?` — so the words are the span's FREE text (`parse.free`), not `blackAfter`. The r66 standalone title rule (`activity_wrapper.standalone_title_heading`) and the owner-lead `addLead` both read `blackAfter` alone, so the title was DROPPED SILENTLY: Claude's box opened with its first content paragraph (or, on the r66 path, promoted the black tail's first sentence to the `<h3>`) and the words appeared nowhere on the page (CEDW201 2A / 2B / 2C / 4D, AGH1002 2A, CEDK101 3A, XLP01 4A–4D, TWHA903 / 904 / 905's eleven `Ka pai!` boxes, MXFL202 2A / 2B / 2C / 7A) — a §6 silent strip the gold contradicts: its box opens `<h3>Concrete poems</h3>` then the paragraphs. Found through DIFF_QUEUE #585 (`activity MISSING h3`, 384 pages / 190 modules) decomposed by `outputs/_s29_r7_boxtitle.py` → `_s29_r7_boxtitle.out` (7582 gold box titles on the paired pages: Claude MATCH 3275; the non-match = the r369 numbering class — `_s29_r7_boxnum.py`: 631 / 3540 title-paired boxes carry a different number, letter drift from Claude's own extra / missing boxes 386, phase drift 150, HPFUN numberless 23 — the gold's INVENTED titles (WT source absent 1486, class C), the Bilingual PNR / TRR table dialect (1129), and the `opener red-embedded` rows) and measured by `_s29_r7_redtitle.py` → `_s29_r7_redtitle.out` (216 red-embedded opener spans / 86 modules).

**Measured** (`outputs/_s29_r7_titlerule.cjs` — the candidate rule applied with the LIVE TagNormaliser to every span): the rule selects **48 sites / 30 modules; the gold's box opens with that `<h3>` on 40 = 0.83** (Te ara Whakapuawa 11 / 11, Leaving to Learn 5 / 5, ConnectED 3 / 3, Blended Literacy 4 / 4, English 4 / 5, Mathematics 10 / 15, NCEA1 3 / 4; absent 4 = MXDI101 / MXFL104 / ENGC204 / OSAH — the A1 minority). Every exclusion measured: `[Activity: Embedded] <widget>` (remainder `embedded`, 59 sites — gold absent 52), widget names 37 (gold absent 27), digit-led 10 (`[Activity] 4A Perspectives` — gold absent), parenthesised / colon-ended / cues 18. NEW-FAMILY CHECK: no intake family in the class (WJFUN 0) — it holds across the Inquiry / Standard families. The first probe (49 pages) then showed three shapes the `[activity`-anchored census had not seen and the rule gained a guard for each: the `[interactive activity] type and check` / `[interactive tool] …` openers (alias `interactive` — the MXDI / MXFU / MXFL dialect names the WIDGET after the bracket, r364) → `exclude_alias_words`; a Word run split MID-WORD (`[Activity 5A] L` + `ooking at precise word choice`) or mid-sentence (`[Activity 1] Click` + ` on the link below…`) → the continuation rule (joined and short = the title `Looking at precise word choice`, mode "join"; joined and long = the red words PREPENDED to the black tail so the r66 rule reads the whole line, mode "prefix" — never dropped); a lowercase aside (`[activity 5b] wide`, `tick the pictures that show fractions.`) → `require_capital` (every gold-titled site is capitalised); `Calculating soil type.` → `strip_trailing_stop`; a broken bracket (`Activity: individual]`) → rejected; `Activity 3A Finding the Perimeter` → `strip_leading_id`. The lexicon test is by DIRECTIVE, not by match: a text the lexicon reads as an INTERACTIVE / ELEMENT tag (`[True False Quiz]` → radio quiz, `[Wordfind- no backwards words]` → word find, `[Trigger Engagement]`, `[Video]`) names a widget, never a title; a SUBTAG / container hit inside a phrase (`[Looking at precise word choice]` → option via `choice`, `[Word art]` → data marker, `[Matching activity]` → activity) is a title that happens to contain a tag word.

**The fix (DATA OVER CODE).** `activity_wrapper.standalone_title_heading.embedded_free_text {enabled, env EMBTITLE_OFF, max_words 8, min_chars 3, require_capital, strip_trailing_stop, exclude_alias_words [interactive], remainder_allow [individual, independent, group], widget_directives [INTERACTIVE, ELEMENT], strip_leading_id}`: ONE helper `ContentConverter.#embeddedOpenerTitle(it, tpl)` (the rule above; `RenderText(it.text)` for the original-case words; the NEW `TagNormaliser.HasInstructionCue(text)` scans the free text with the Instruction_Cues vocabulary exactly as `Parse` does) consulted at BOTH opener sites — the plain path sets `it._embeddedTitle` and `ActivitiesBuilder.activityOpen` emits it as the `<h{level}>` (a self-titled box: `titledOpener`; the WHOLE black tail then renders as content, its first line no longer promoted); the bundle-owned path pushes it FIRST into `leadStream` as an `_ownerTitle` black item (so `addLead` promotes it and the owner's black tail joins the lead prose). `ACTTITLE_OFF` turns it off with the parent rule. OFF = the r415 output byte-for-byte.

### 2. PROOF

- `_s29_r416_probe_run.sh` (the r410 harness over all 494 Claude-dir modules, 4 shards): **OFF (`EMBTITLE_OFF`) = disk 2555 / 2555**; **ON = 44 pages / 37 modules** (`_affected_r416.txt`).
- `_s29_r416_pagescore.py` (the gate's own `match()` on the probe's ON pages BEFORE regenerating): **41 paired pages, 22 up / 12 down / 7 same, SCAFFOLD pp-sum +33.1, RAW +11.4**; MXEO102_2_0 +10.4, BLL172_1_0 +7.3, TWHA903_0_0 +2.3; the dips ≤ 0.7 are the scorer's alignment artefact on a strictly closer element set — MXDB202_4_0 −0.7 now matches its gold box byte-for-byte (`<h3>Making pyramids</h3>` + `<p>Imagine you are…`), ENGC102_1_0 −0.4 / ENGS101 / ANZH401 ×2 / ENGI101 the same class on gold-titled sites; MXFL104_1_0 −0.1 the A1 minority (the gold dropped the title).
- **THE FULL REGENERATION** (`_s29_r416_fullship_par.sh`: `_batch_plan.py`'s 39 weights-aware batches, 4 parallel workers, all rc 0 — 494 dirs in 6 min): `_stalecheck.sh` **0 stale**; `_content_manifest.py diff` vs the r415 snapshot = **44 pages / 37 modules changed, 0 added / 0 removed = the probe's ON set EXACTLY** — the seven scoped ships since the 19 Sept FULL (r409–r415) left **NO residue** (`_s29_r416_stale_manifest.log`).
- `run_all_gates.sh` (`_s29_r416_gates.log`) + `_gatecheck.py` vs the committed r415 baseline (`_s29_r416_gatecheck.log`): every row HELD-or-IMPROVED; every verifier RESULT ✓ identical to r415 (flipCard 61 / divergence 0, speechBubble 62 ✓, modal 13 groups defect 0, mtkQuiz 17 shells ✓, math 323 / 323, menulabels 99 ✓, dragAndDrop 21 ✓); entry parity PASS; index-sync 33 / 28.
- `_s29_skdelta.py _s29_r415_sk_final.json _s29_r416_sk_final.json --affected _affected_r416.txt`: **33 movers, 22 up / 11 down, 0 outside the affected set**; the pairing ladder re-resolved on TWO modules (the r186 / r222 / r303 class, 0 pages added or removed on disk): ENGI101_1_0 40.5 → 30.1 (its `Adjectives` box now matches the gold's LESSON-2 box, so the content-order pairing moved it from gold 1.0 to gold 2.0 — Claude's lesson 1 spans the gold's lessons 1–5, the r341 pagination class) and MXDI101 (the pair `_1_0` @ 27.3 replaced by `_1_2` @ 44.9) — named.
- The ship ledger: **FULL ship recorded (round 416); scoped-since counter reset to 0**; the fast-loop baseline re-snapshot, the content manifest snapshot (2555 pages / 491 modules), the feature index `--rehtml` / `--merge` / `--selftest` GREEN, **16 selftests GREEN (46 PASS / GREEN lines, 0 FAIL)**.
- DIFF MINER re-mined on the r416 corpus (`_diff_miner_s29_r416.log`): **181 → 181 CANDIDATE rows**.

### 3. PROTECTED GATES (all HELD-or-IMPROVED — `_s29_r416_gates.log`, `_s29_r416_gatecheck.log`)

- **Skeleton (PRIMARY)**: SCAFFOLD **53.911 → 53.928 % (+0.0174pp)**; ≥50 **1415**, ≥75 **238**, ≥90 **20** EXACT; RAW **37.996 → 38.000 %**; 2349 pairs, skipped 0 (state `outputs/_s29_r416_sk_final.json`).
- **compare_structure** exact **14168** / EXTRA **186** / MISSING **683** / row-wrap **23** EXACT; **body_compare** 54 / 5 / 190 / 247 EXACT; **defect** clean 2504 / 2548 = 98.27 %, leak 73 / 44 EXACT; tags **9557 / 9557**.
- Plateau (§4): **+0.0174pp with no other protected gate moved — the window opens at 1 of 3** (the two pairing re-resolutions above carry −10.4 and +17.6 of the round's movement).

### 4. RECORDED, NOT TAKEN (the Round 7 PICK's measurements — `LOOP_STATE.md`)

- The empty writer-owned box residue after r415 (`_s29_r7_emptybox.out`: 64 boxes / 52 pages / 32 modules — the gold has NO box with that number on 34; the `[Go to your Learners Journal and complete activity 1A and 1B]` journal-instruction openers 12 / 3 AGH modules, under the floor; the HPFUN numberless boxes 6 — the [New tab] path has no phase numbering; CEDT207's 2D–2F).
- The activity-number mismatch (`_s29_r7_boxnum.out`: 631 / 3540 title-paired boxes = 0.18 on 331 pages / 173 modules — letter drift 386 from Claude's own extra / missing boxes (the r369 declined class: fix the boxes, never renumber), phase drift 150 (WJFUN108 / 105 = the gold's REORDERED tiles, editorial; the TRR `1C` vs `1.2` = the r330 KB-preference override), HPFUN numberless 23).
- DIFF_QUEUE #585's `inside a longer line` rows (1361: 1129 the Bilingual PNR / TRR `[H2] English ║ [H2] Māori` table cells — the TMoA family's rendering, recorded); the gold's invented box titles (1486, class C).

"""
p = PF + "BUILD_CHANGELOG.md"; s = rd(p)
head, rest = s.split("\n", 1)
assert head.startswith("# BUILD CHANGELOG") and rest.lstrip("\n").startswith("## 2026-09-20 (round 415")
wr(p, head + "\n\n" + entry + rest.lstrip("\n"))

p = PF + "app/js/Config.js"; s = rd(p)
old = '\tstatic AppVersion = "260619.86";'; assert s.count(old) == 1
note = ("\t// ROUND 416 (260619.87): THE ACTIVITY TITLE TYPED INSIDE THE RED SPAN — `[Activity 2A] Concrete poems` all red: the span's free text is the box's "
        "<h3> (the r66 rule and the owner lead read blackAfter alone, so the title was dropped silently; the gold's box opens with it on 40 / 48 = 0.83). "
        "`standalone_title_heading.embedded_free_text`, env EMBTITLE_OFF; ContentConverter.#embeddedOpenerTitle at both opener sites, TagNormaliser.HasInstructionCue. "
        "The loop's session 29 Round 7: OFF = disk 2555 / 2555, ON 44 pages / 37 modules (22 up / 12 down, +33.1pp-sum); THE FULL REGENERATION of all 494 "
        "(the ledger backstop after seven scoped ships — 0 stale, the manifest diff = the probe's 44 pages, no residue); skeleton 53.911 → 53.928 % (+0.0174pp), "
        "every other gate EXACT; miner 181 → 181.\n")
wr(p, s.replace(old, note + '\tstatic AppVersion = "260619.87";'))

p = PF + "CLAUDE.md"; s = rd(p)
old9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 415 BASELINE ("; assert s.count(old9) == 1
new9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 416 BASELINE (the activity title typed inside the red span is the box's <h3> — "
        "`standalone_title_heading.embedded_free_text`, env `EMBTITLE_OFF`; 37 modules / 44 pages; a FULL regeneration of all 494 (the ledger's backstop after seven "
        "scoped ships, 0 stale, the manifest diff = the probe's 44 pages exactly — no residue): SCAFFOLD mean 53.928% / >=50% 1415 / >=75% 238 / >=90% 20 / RAW 38.000% "
        "@ 2349 pairs, pairs skipped 0 — hold-or-improve; 33 movers (22 up, 11 down — the pairing ladder re-resolved on ENGI101_1_0 −10.4 and MXDI101 (+17.6 net), "
        "the rest ≤ 0.7; 0 outside the affected set); the 2316 unaffected pairs EXACT. compare_structure 14168 / 186 / 683 / 23 EXACT; body_compare 54 / 5 / 190 / 247 "
        "EXACT; defect clean 2504 / 2548 = 98.27%, leak 73 / 44 EXACT.** Previous — ROUND 415 BASELINE (")
s = s.replace(old9, new9)
old11 = "| `NOTABLEOWNED_OFF` | 415 | **THE OWNED HEADING-LED BUNDLE WITH NO TABLE"; assert s.count(old11) == 1
row11 = ("| `EMBTITLE_OFF` | 416 | **THE ACTIVITY TITLE TYPED INSIDE THE RED SPAN — `[Activity 2A] Concrete poems` all red is the box's `<h3>`** (the autonomous loop's "
         "session 29 Round 7 — the ledger's FULL-regeneration backstop). A writer types the box title in the SAME red run as the opener, so the words are the span's FREE "
         "text (`parse.free`), which neither the r66 rule (`blackAfter`'s first line) nor the owner-lead `addLead` read: the title was dropped silently (CEDW201, AGH1002, "
         "CEDK101, XLP01, the TWHA `Ka pai!` boxes). Measured (`_s29_r7_titlerule.cjs` over the 216 red-embedded opener spans / 86 modules): the rule selects 48 sites / 30 "
         "modules, the gold's box opening with that `<h3>` on 40 = 0.83 (every family group ≥ 0.67, most 1.00). `ContentConverter.#embeddedOpenerTitle` at BOTH opener sites "
         "(the plain path → `it._embeddedTitle` → `ActivitiesBuilder.activityOpen`; the bundle-owned path → the first `_ownerTitle` lead item): an activity CONTAINER_OPEN "
         "opener whose alias is not `interactive` (`[interactive activity] type and check` names the widget), whose remainder is empty or a mode word, whose free text is no "
         "instruction fragment / cue (`TagNormaliser.HasInstructionCue`), not parenthesised / digit-led / colon-ended, ≤ 8 words, CAPITALISED, and that the lexicon does not "
         "read as an INTERACTIVE / ELEMENT tag (`[True False Quiz]` → radio quiz; a SUBTAG hit inside a phrase is fine) → `RenderText` of the span is the `<h3>`; a black tail "
         "opening with a lowercase letter CONTINUES the red words (a Word run split — joined and short = the title, mode join; joined and long = the red words prepended to "
         "the tail, mode prefix — never dropped). OFF = the r415 output byte-for-byte (2555 / 2555). ON = 44 pages / 37 modules, 22 up / 12 down (+33.1pp-sum). |\n")
s = s.replace(old11, row11 + old11)
old14 = "- **Build:** `260619.86` (round 415 — **the owned heading-led bundle"; assert s.count(old14) == 1
b14 = ("- **Build:** `260619.87` (round 416 — **the activity title typed inside the red span is the box's `<h3>`: `[Activity 2A] Concrete poems` all red — the span's "
       "free text, which the r66 rule and the owner lead never read, so the title was dropped silently; the gold's box opens with it on 40 / 48 = 0.83** "
       "(`standalone_title_heading.embedded_free_text`, env `EMBTITLE_OFF`; `ContentConverter.#embeddedOpenerTitle` at both opener sites; `TagNormaliser.HasInstructionCue`); "
       "the autonomous loop's session 29 Round 7; the probe OFF = disk 2555 / 2555, ON 44 pages / 37 modules (22 up / 12 down, +33.1pp-sum, 0 outside the set); "
       "**THE FULL REGENERATION of all 494 gated dirs (the ledger's backstop after seven scoped ships — 39 batches rc 0, 0 stale, the manifest diff = the probe's 44 pages "
       "exactly, NO residue from r409–r415; the scoped counter reset to 0)**; **ROUND 416 BASELINE: SCAFFOLD mean 53.928% / >=50% 1415 / >=75% 238 / >=90% 20 / RAW 38.000% "
       "@ 2349 pairs** (+0.0174pp; buckets EXACT); compare_structure 14168 / 186 / 683 / 23, body 54 / 5 / 190 / 247, clean 2504 / 2548, leak 73 / 44 — all EXACT; every "
       "verifier EXACT; 16 selftests GREEN; the miner 181 → 181; plateau window 1 of 3). Previous: ")
s = s.replace(old14, b14 + old14)
wr(p, s)

p = R + "CONVERTER_V2/reference/tests/gate_baseline.json"; s = rd(p)
def setv(key, old, new):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=1); assert n == 1, key
setv("build", '"260619.86"', '"260619.87"'); setv("round", 415, 416)
setv("mean_scaffold_pct", 53.91, 53.93)
a = '    "_note_r415": "Round 415 (session 29 Round 6)'; assert s.count(a) == 1
s = s.replace(a, '    "_note_r416": "Round 416 (session 29 Round 7): the activity title typed inside the red span is the box\'s h3 (standalone_title_heading.embedded_free_text, env EMBTITLE_OFF; 37 modules / 44 pages; THE FULL regeneration of all 494 — the ledger backstop, 0 stale, manifest diff = the probe\'s 44 pages, no residue from r409-r415; skeleton 53.9110 -> 53.9284, buckets EXACT, RAW 37.996 -> 38.000; every other gate EXACT).",\n' + a)
a2 = '    "_note_r414b": "Round 415: SCAFFOLD 53.8864'; assert s.count(a2) == 1
s = s.replace(a2, '    "_note_r415b": "Round 416: SCAFFOLD 53.9110 -> 53.9284 (+0.0174pp; 33 movers 22 up / 11 down — MXEO102_2_0 +10.4, BLL172_1_0 +7.3; the pairing ladder re-resolved on ENGI101_1_0 -10.4 (gold 1.0 -> 2.0) and MXDI101 (_1_0 27.3 -> _1_2 44.9); 0 outside the 37-module affected set), 1415 / 238 / 20 EXACT, RAW 38.000; 2349 pairs. Plateau window 1 of 3.",\n' + a2)
b2 = '    "_note_r415": "Round 415: exact 14174 -> 14168'; assert s.count(b2) == 1
s = s.replace(b2, '    "_note_r416": "Round 416: 14168 / 186 / 683 / 23 EXACT (the FULL regeneration of all 494 — no residue from the seven scoped ships).",\n' + b2)
b3 = '    "_note_r415": "Round 415: over-capture 54 / runaway 6 -> 5'; assert s.count(b3) == 1
s = s.replace(b3, '    "_note_r416": "Round 416: over-capture 54 / runaway 5 / EMPTY 190 / ANY 247 EXACT (the FULL regeneration).",\n' + b3)
wr(p, s); json.load(open(p, encoding="utf-8"))
print("r416 finalise: changelog + Config.js 260619.87 + CLAUDE.md §9/§11/§14 + gate_baseline.json done")
