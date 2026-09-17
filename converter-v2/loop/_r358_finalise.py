#!/usr/bin/env python3
"""ROUND 358 (loop session 19 Round 2 — the Te Reo half of a bilingual title is recognised by the Māori alphabet, not only by
a macron) — finalise: changelog, AppVersion (260619.28 → 260619.29), CLAUDE.md §9 / §11 / §14, gate_baseline.json,
loop/README.md rows. Idempotent; LF via wr()."""
import io, os, json
ROOT = r"C:\Users\Gavin\TeKura\FINAL_MODULE_DATA"
PF = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)

CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)" + chr(10) + chr(10)
ENTRY = """## 2026-09-17 (round 358, build 260619.29) — THE TE REO HALF OF A BILINGUAL TITLE IS RECOGNISED BY THE MĀORI ALPHABET, NOT ONLY BY A MACRON: `Utils.LooksMaori` (macron OR Māori orthography — every word vowel-final, no consonant cluster but ng / wh, a lone word ≥ 5 letters, a short English stoplist, no hyphenated token) is the guard every overview bilingual splitter shares (`ContentConverter.#oneHalfTeReo` — the dash r86, slash / colon r168 / r177, punct-pair splitters) and lets a LESSON'S own pair split on the soft separators (`lesson_bilingual_pair.soft_separators`: spaced dash / slash / colon, after the unconditional pipe); two consequences of knowing the English half: the `<title>` element and a lesson page's module-title FALLBACK take the ENGLISH half of a Māori-first pair (`SkeletonBuilder.#englishOf`; the overview h1 order stays the writer's) and a pair split from an ALL-CAPS title is sentence-cased per half — the autonomous loop's session-19 Round 2, the DIFF MINER's TITLE class (DIFF_QUEUE F1 / #4); **FULL regeneration of all 416 (36 batches, all rc 0), 37 modules / 74 pages changed; skeleton SCAFFOLD 52.013 → 52.052 % (+0.039pp; 16 movers, 14 up, the 2 dips named), ≥50 1094 → 1095, every other gate EXACT; ledger FULL (counter 0)**

### 1. WHAT CHANGED, IN ONE LINE

**A bilingual title the writer joined with a dash, slash or colon — "Te Tautoko Ako – Learning Partnership Whakatau", "Ethical Citizenship / Matatika Kirirarau", "Whaikaha: Use your strengths", the lesson name "Ngā Whare - Housing" — shipped as ONE `<h1>` whenever the Te Reo half carried no macron, because every splitter's "exactly one half is Te Reo" guard was a macron test; the guard now also reads Māori orthography, the lesson pair gains the overview's soft separators, and the two places that need the ENGLISH half by name (the `<title>`, the lesson fallback) ask for it by language instead of by slot.**

### 2. THE EVIDENCE (docx → human → Claude)

- **XWHA01 overview** — WT `[TITLE BAR] **Te Tautoko Ako – Learning Partnership Whakatau**`; gold `<h1><span>Learning Partnership Whakatau</span></h1><h1><span>Te Tautoko Ako</span></h1>`; Claude before `<h1><span>Te Tautoko Ako – Learning Partnership Whakatau</span></h1>`; after the two h1 (writer's order, 01A) and `<title>XWHA01 Learning Partnership Whakatau</title>` (01A: the `<title>` is English-only).
- **ANZH104 lesson 2** — WT `[H2] Lesson 2 – Ngā Whare - Housing`; gold `<h1><span>Ngā Whare</span></h1><h1><span>Housing</span></h1>`; Claude before `<h1><span>Ngā Whare - Housing</span></h1>`; after `Housing` + `Ngā Whare` (D10-2: English first on a Standard lesson pair — the gold's Māori-first order is the same NAMED override as ANZH105 / HIS1006 at r345).
- **SSFUN06 / MXDB301 / XDLS502 / XWHA02 / CEDR501 / CEDK501 / XTAS101–103** — the same shape on the overview (slash / dash / colon); **HES1005 lesson 5** — WT `KAITIAKITANGA – BE A KAITIAKI`, gold `Guardianship` + `Kaitiakitanga`, Claude after `Be a kaitiaki` + `Kaitiakitanga` (sentence-cased per half, the r327 red flag kept). **SSCI205 / SSOG103** — the placeholder half (`/ te reo`, `/ TE REO`) now recognised as a bilingual boundary is DROPPED by the r76 placeholder rule: the glued `Ancient greece / te reo` becomes `Ancient greece` (the gold's Māori title is the human's own — not in the WT).
- **What the guards keep whole (verified on disk after the full regeneration):** CEDT501 lesson 7 `Assertiveness in Action – One-to-one` (the hyphenated token), XMES101 lesson 2 (a three-sentence title), MXFL103 `Time – Quarter Past` and PES1005 `Our home: Planet Earth` (the stoplist / vowel-final rule), TRR111 lesson 2's phonics half `io` (a single-word half is never capitalised).

### 3. THE MEASUREMENT (before coding — `outputs/_measure_r358_titlepair.py` → `_r358_titlepair.{json,log}`; `_measure_r358_seps.py` → `_r358_seps.{json,log}`; the in-memory probe `_r358_probe.cjs` over all 416)

- **The queue:** `DIFF_QUEUE.md` (the diff miner, Round 0c) — chrome fact F1 `header:title-h1-count=2` MISSING on 114 modules / 204 pages; ranked class #4 (`div#header › h1>span` MISSING, 112 modules, derivable 0.73). Decomposed: the gold has more title h1s than Claude on 206 pages / 116 modules — **101 not-in-wt** (the human's own Te Reo module title, absent from every WT — class C, recorded), **16 placeholder** (the developer's red `TE REO required` h1 on the Fundamentals overviews — a to-do, never a target), **84 derivable** — 37 'wt-separated' mostly the gold repeating the MODULE pair on lesson pages (ANZH301 ×8, TEDC401 ×6, TEDC402 ×8 — the convention constraint 79 / CL-0069 superseded; Claude's lesson title is KB-correct, named), 16 'wt-elsewhere' (no rule), **31 'glued-in-claude'** — the pair on Claude's page as ONE h1.
- **The solidify test (r182):** over 650 WT title lines with a separator, with EXACTLY ONE Māori-looking half the gold SPLITS a non-pipe pair **27 : 3** (dash 15 : 2, slash 10 : 0, colon 4 : 1, hyphen 2 : 0; the pipe 100 : 0); the three glued are the loose alphabet test's false positives on short English words ("Time – Quarter Past", "Our home: Planet Earth") — the discriminator the rule carries (Māori orthography + the stoplist).
- **The in-memory probe (three iterations, `_r358_probe_on_0*.log`; `REODETECT_OFF=1` = disk 2110/2110 every time):** 27 → 75 → **74 changed pages / 37 modules** — 14 pair splits the gold has, 2 placeholder drops, the English `<title>` on 18 overviews (HIS1003 / HIS1004 / HIS1005 / HIS1006 / HIS1008 / CEDO501 / CEDT501 / CEDW501 / BLLR201 / MXDI201 / MXFL201 / PNR101 / 102 / 104 / TRR107 / 108 / XDLS501 / XLP06 …), the English lesson fallback on 34 lesson pages (HIS1003 `Mana Tangata` → `People Power: The 1951 waterfront dispute` — constraint 79 (5) 'the module English title'), and the three false splits of the first iteration removed (CEDT501, XMES101 — the hyphen / sentence guards) plus the two casing defects of the second (TRR111 `io`, the lost red flag).
- **§1b authority:** KB level 1 — 01A 'TITLE BAR PARSING RULE: English and Te Reo titles MUST be split into two separate `<h1><span>` elements. Never merge into one'; constraint 79 / 02C line 62 (a lesson's own bilingual name, 'split by the same TITLE BAR parsing rule'); 01A '`<title>` … is English-only'; constraint 79 (5) (the fallback is the module ENGLISH title); constraint 1 (casing normalisation permitted). The gold: 0.90.

### 4. THE MECHANISM (`outputs/_r358_splice.py` + `_r358b_splice.py` + the casing patch)

- **`Utils.LooksMaori(text, cfg)`** (data `Emit_Templates.header.te_reo_detect` {enabled, env `REODETECT_OFF`, mode, min_letters_single_word 5, digraphs, english_stopwords (bite only on ≤ 3-token halves — a long Māori title may carry the particle "me"), english_slot_by_language + `ENGSLOT_OFF`, pair_half_casing}).
- **`ContentConverter.#oneHalfTeReo(a, b)`** — the one guard behind `#bilingualTwoLangGuard` (the char_separators slash / colon + the case-transition split), `#bilingualDashSplit`, `#bilingualPunctSplit`; OFF = the macron-only test.
- **`SkeletonBuilder.#lessonPair`** — after the unconditional pipe, the first `soft_separators` entry that occurs exactly once, leaves two non-empty halves with no sentence break, and exactly one Te Reo half. **`#englishOf(a, b, tpl)`** — the `<title>` (overview) and the lesson fallback. **Per-half casing** — an ALL-CAPS pair sentence-cased per half in the emit loop (the red flag kept); a multi-word half never starts lowercase.

### 5. THE PROOF

- **OFF = disk** on all 416 (2110 / 2110 identical, three probe iterations). **FULL regeneration** (`_r358_fullship_par.sh`, 36 batches, all rc 0, 4 m 50 s): `_stalecheck.sh` 0 stale; `_content_manifest.py changed` = exactly the probe's 37 modules.
- **Gates (`_r358_gates.log`, every RESULT ✓, 0 ✗, pairs skipped 0):** **skeleton SCAFFOLD 52.0125 → 52.0516 % (+0.039pp; 16 movers — 14 up, pp-sum +61.8), ≥50 1094 → 1095 (ANZH104_2_0 crosses), ≥75 160 / ≥90 14 EXACT, RAW 36.728 → 36.748 %**; the two dips NAMED — XGF9004_1_0 49.66 → 46.67 (the writer's pair `Puna Mātauranga – Spring of Knowledge` split per the KB; the gold retitled the page `Introduction`) and HIS1002_7_0 42.38 → 40.92 (`Taking Action: Ngā Toa o Te Moana-nui-a-Kiwa` split on the colon; the gold retitled `Taking Action in Aotearoa`). compare_structure exact 11617 / EXTRA 175 / missing 617 EXACT; body_compare 182 EXACT; structural defect clean 98.9 % (26 occ / 23 pages) EXACT; tags 9557 / 9557; flipCard divergence 0, speechBubble ✓, modal ✓, MTK shell ✓, math ✓, menu labels ✓, dragAndDrop ✓, entry parity PASS. `_r358_sk_final.json` is the chain state.

**Ledger:** FULL regeneration of all 416, `_ship_ledger.py record-full --round 358` (counter 0) · selftests 16 GREEN, fast-loop baseline, content manifest, feature index refreshed (`_r358_postship.sh`) · data `header.te_reo_detect`, `lesson_bilingual_pair.soft_separators` · engine `Utils.LooksMaori`, `ContentConverter.#oneHalfTeReo`, `SkeletonBuilder.#lessonPair` / `#englishOf` / `#teReoDetectOn` + the per-half casing · env `REODETECT_OFF` (the round), `ENGSLOT_OFF` (the English-slot consequence) · KB delta: none (01A already states every rule applied).

"""
if "round 358, build 260619.29" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r358 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.29"' not in s:
    old = '\tstatic AppVersion = "260619.28";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, '\t// ROUND 358 (260619.29): the Te Reo half of a bilingual title is recognised by the Māori alphabet, not only by a macron (Utils.LooksMaori; the overview splitters\' shared guard + the lesson pair\'s soft separators; the English <title> / lesson fallback by language; env REODETECT_OFF / ENGSLOT_OFF); the diff miner\'s TITLE class.\n\tstatic AppVersion = "260619.29";')
    wr(P, s); print("Config.js: 260619.29")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "ROUND 358 BASELINE" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 357 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 358 BASELINE (the Te Reo half of a bilingual title is recognised by the Māori alphabet — the splitters' shared guard, the lesson pair's soft separators, the English <title> / fallback; FULL regeneration of all 416, ledger 0): SCAFFOLD mean 52.052% / >=50% 1095 / >=75% 160 / >=90% 14 / RAW 36.748% @ 1955 pairs, pairs skipped 0 — hold-or-improve; the two r358 dips named (XGF9004_1_0, HIS1002_7_0).** Previous — ROUND 357 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `TMPLDELTA_OFF` | 357 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `REODETECT_OFF` | 358 | **THE TE REO HALF OF A BILINGUAL TITLE IS RECOGNISED BY THE MĀORI ALPHABET, NOT ONLY BY A MACRON.** `Utils.LooksMaori` (a macron, OR every word vowel-final with no consonant cluster but ng / wh, a lone word ≥ 5 letters, a short English stoplist on ≤ 3-token halves, never a hyphenated token) is the 'exactly one half is Te Reo' guard behind every overview bilingual splitter (`ContentConverter.#oneHalfTeReo` — dash / slash / colon / case-transition / punct-pair) and behind the lesson pair's NEW soft separators (`lesson_bilingual_pair.soft_separators`, after the unconditional pipe; no sentence break in a half). Also: a pair split from an ALL-CAPS title is sentence-cased per half (the red flag kept), a multi-word half never starts lowercase. OFF = the macron-only guard + pipe-only lesson pairs (the r357 output, proven 2110 / 2110 by the in-memory probe). Data `header.te_reo_detect`. |\n"
             "| `ENGSLOT_OFF` | 358 | **THE `<title>` ELEMENT AND A LESSON PAGE'S MODULE-TITLE FALLBACK TAKE THE ENGLISH HALF BY LANGUAGE.** The title-bar slots keep the writer's order (so the overview h1s do), which leaves the 'english' slot holding the Māori half of a Māori-first pair; `SkeletonBuilder.#englishOf` returns the English one when exactly one of the two reads as Te Reo (01A: the `<title>` is English-only; constraint 79 (5): the fallback is the module ENGLISH title — HIS1003's lessons `Mana Tangata` → `People Power: The 1951 waterfront dispute`). OFF = the first slot, as before. Data `header.te_reo_detect.english_slot_by_language`. |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.28` (round 357"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.29` (round 358 — **the Te Reo half of a bilingual title is recognised by the Māori alphabet, not only by a macron** (`Utils.LooksMaori`; the overview splitters' shared guard `ContentConverter.#oneHalfTeReo`; the lesson pair's soft separators; the English `<title>` / lesson fallback by language; per-half casing; env `REODETECT_OFF` / `ENGSLOT_OFF`); the autonomous loop's session-19 Round 2, the DIFF MINER's TITLE class; FULL regeneration of all 416, 37 modules / 74 pages changed; skeleton 52.013 → 52.052 % (+0.039pp, ≥50 +1, two dips named), every other gate EXACT; ledger FULL, counter 0).\n"
             + OLD14)
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r358" not in d["skeleton"]:
    d["skeleton"]["mean_scaffold_pct"] = 52.052
    d["skeleton"]["pages_ge_50"] = 1095
    d["skeleton"]["raw_mean_pct"] = 36.748
    d["skeleton"]["_note_r358"] = "Round 358: the Māori-alphabet title test — SCAFFOLD 52.0125 → 52.0516 (+0.039pp; 16 movers, 14 up; dips NAMED: XGF9004_1_0 and HIS1002_7_0 — the writer's pair split per the KB where the gold retitled the page), ≥50 1094 → 1095, ≥75 160 / ≥90 14 EXACT, RAW 36.728 → 36.748. Hold-or-improve from here."
    d["_meta"]["build"] = "260619.29"; d["_meta"]["round"] = 358
    d["_meta"]["_note_r358"] = "Round 358: the TITLE class — skeleton +0.039pp (named dips), every other gate EXACT; FULL regeneration of all 416, 37 modules / 74 pages; ledger FULL (counter 0)."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r358")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_r358_finalise.py" not in s:
    A = "| `_measure_r357_chip.py`"
    assert s.count(A) == 1, "README anchor"
    ROWS = ("| `_measure_r358_titlepair.py` / `_r358_titlepair.{json,log}` / `_measure_r358_seps.py` / `_r358_seps.{json,log}` / `_r358_splice.py` / `_r358b_splice.py` / `_r358_probe.cjs` / `_r358_probe_run.sh` / `_r358_probe_{off,on}_0*.log` / `_r358_changed_modules_probe.txt` / `_r358_fullship_par.sh` / `_r358_fullship_run.sh` / `_r358_fullship_regen.log` / `_r358_changed_modules.txt` / `_r358_gates.log` / `_r358_sk_full.log` / `_r358_sk_final.json` / `_r358_postship.sh` / `_r358_selftests.log` / `_r358_fastloop_snapshot.log` / `_r358_manifest_snapshot.log` / `_r358_ledger.log` / `_r358_index.log` / `_r358_finalise.py` | `CONVERTER_V2/outputs/` | Session 19 Round 2 (engine r358 — the diff miner's TITLE class: the Te Reo half of a bilingual title recognised by the Māori alphabet; the overview splitters' shared guard, the lesson pair's soft separators, the English <title> / fallback by language) — the title-pair decomposition (206 pages: 101 class C, 16 placeholders, 84 derivable), the separator solidify test (27 : 3), the two anchored splices, the in-memory ON / OFF probe over all 416 (three iterations), the full regeneration, the gate suite, the fresh skeleton score, the post-ship housekeeping, the finalise |\n")
    s = s.replace(A, ROWS + A, 1)
    wr(P, s); print("README: r358 rows")
print("finalise done")
