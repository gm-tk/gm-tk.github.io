#!/usr/bin/env python3
"""r419 finalise (CLAUDE.md §12): changelog entry, Config.js bump, CLAUDE.md §9 / §11 / §14, gate_baseline.json. Run under WSL."""
import re, json
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
PF = R + "pageforge-site/converter-v2/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

entry = """## 2026-09-21 (round 419, build 260619.90) — THE LANGUAGE-FONT WRAP: every run of Chinese / Japanese text takes `span.ch-text` / `span.jp-text` (KB constraint 92 / CL-0093 — the CJK half; the autonomous loop's session 30 Round 1; SCOPED regeneration of the 13 language modules, the probe proving the other 481 byte-identical)

### 1. WHAT CHANGED

**The class.** The KB's constraint 92 (CL-0093, 13 September 2026, locked admin): *the language-font classes `jp-text`, `ch-text` and `pinyin` are MANDATORY on every occurrence — the conversion applies them, not the designer afterwards.* The gold does exactly that — every run of Chinese or Japanese text is `<span class="ch-text">…</span>` / `<span class="jp-text">…</span>` — and Claude shipped every run bare. Found by the session-29 position-free label census (`span.ch-text` gold 494 / Claude 0 on the skeleton's collapsed count) and the KB status row 92, whose "< 20 pages" verdict was pre-intake (CHI1003–1005, JPN1004 and CHWHA arrived on 19 September).

**Measured** (`outputs/_s30_r1_langfont.py` → `_s30_r1_langfont.out`, the gate's own pairing): the gold's paired pages carry **5,512 CJK runs, 5,437 wrapped = 0.99**; **Claude shipped 3,812 runs bare on 26 pages / 14 modules** (JPN1004 11 pages / 2,190 runs, CHFUN05 1,136, CHFUN07 119, JPFUN02 93, CHFUN08 88, JPFUN01 67, CHFUN06 53, CHI1004 21, CHI1005 15, CHWHA 12, CHFUN01 6, CHI1003 5, CHFUN04 5, MXFL202 2). 3,277 of the gold's runs have their text on Claude's page; the CHI1003–1005 lesson dialogues do NOT (7 / 199 / 116 CJK characters in those WTs against 3.1k / 4.0k / 3.6k in the gold — class C, no source, those pages stay low by design). The gold's FORM (`_s30_r1_langspans.py` → `_s30_r1_langspans.out`, 4,573 ch / jp spans): the carrier is `span` 98 % (the KB's four equivalent forms all present), text-only inside (96 %), in EVERY context — td 1,271 / p 1,005 / li 389 / b 206 / after a `<br>` 115 / h3–h5 224 — the `<b>` OUTSIDE the span; a run starts and ends on a CJK character (4,331 : 64 start on a character rather than a CJK punctuation mark; 4,424 of 4,600 end on one; a trailing ASCII `:` / `)` / `?` sits inside in 115 — a minority, not taken); inside a run: spaces, CJK punctuation (1,916 spans) and ASCII brackets / slashes / stops BETWEEN two CJK blocks (183 spans — the KB's `他(她)是我的(哥哥/弟弟/姐姐/妹妹`). The acknowledgements: the gold leaves its CJK credits bare (CHFUN05 17 / 0, JPN1004 5 / 0, JPFUN01 3 / 2). Non-language modules: the gold's seven stray runs (ENGS202 `(大阪)`, MXFL202 `動物折り紙`, AGH1005 ×4) are video titles, unwrapped; the KB decides a Han-only run by the MODULE's language and any kana as Japanese always.

**The fix (DATA OVER CODE).** `Emit_Templates.body_region.language_fonts {enabled, env LANGFONT_OFF, wrapper, classes, module_language, kana_is_japanese, han_needs_module_language, cjk_chars, han_chars, kana_chars, internal_joiners, lead_open_chars, skip_zones}` + `ListsAndRuns.LanguageFontWrap(html, run)` at the PageAssembler whole-page seam — after `LinkTextDisplay`, before `MathReplace`, the pre-acks slice only (the r213 / r234 / r337 / r392 precedent; the acks stay verbatim) — so every emitter is covered at one seam: the header `<h1>` title span (the KB's nested form `<h1><span><span class="ch-text">`), the module menu, prose, lists, table cells, callouts, the built widgets and the hand-off boxes alike. A RUN = blocks of CJK characters (Han, kana, CJK punctuation, fullwidth forms) joined by internal whitespace and by the ASCII brackets / slashes / stops that sit between two CJK blocks, starting on a Han / kana character or an opening bracket / quote (a leading `：` / `、` / `。` stays outside — `Sachiko： かず` keeps the colon with the name), ending on a CJK character, holding at least one Han or kana (a punctuation-only stretch is never a run). The CLASS: a run with any kana → `jp-text` regardless of the module; a Han-only run → the MODULE's language from `module_language` (longest code-prefix match on `run.moduleCode`: CHI / CHIFUN / CHFUN / CHWHA → ch, JPN / JPNFUN / JPFUN / JAP / JAPFUN → jp); a Han-only run in a module with no language entry is left bare — the KB says raise a `Red Flag:` rather than guess, and that half is NOT built (5 runs on 4 non-language modules, all video titles the gold also leaves bare; recorded). Verbatim: `<script>` / `<style>` / `<title>` / the `cv2-note` / `cv2-comment` developer quotes; a text segment already inside an element carrying one of the three classes is never re-wrapped (idempotent — a future builder that emits the class keeps it). Only the text between tags is touched: attributes, tags and entities are copied through.

**Not this round (recorded):** (a) **pinyin** — the gold's 2,116 `span.pinyin` (1,897 with a non-macron tone mark = the KB's discriminator, 134 macron-only `zhū` / `Xīngqīyī` = the pairing rule, 85 tone-less `Ann:` speaker labels on CHI1003's Texts page — a gold oddity), 1,053 derivable (CHFUN05 918); its own detector next round. (b) The **cross-tag run** — a run partly bold (`もう <b>じゅんび しました</b> ね`) ships as three KB-correct spans (`span`, `b > span`, `span`) where the gold's 4 % form is one span with the `<b>` inside; the KB permits both. (c) **CHWHA** — its Claude build is `MODULE_0_0.html` (the module code is not detected from its docx — a pre-existing recognition gap), so its 12 Han runs stay bare under `han_needs_module_language`; a code-detection fix, not a wrap fix.

### 2. PROOF

- `_s30_r419_unit.cjs` — 22 synthetic cases (the KB's four forms, the joiners, the verbatim zones, kana anywhere, Han needs a module, the leading punctuation, idempotence, the OFF toggle): **22 / 22**.
- `_s30_r419_probe_run.sh` (the r410 in-memory harness over all 494 Claude-dir modules, 4 shards): **OFF (`LANGFONT_OFF`) = the disk on every page, 2555 / 2555**; **ON = exactly 25 pages / 13 modules** (the 26th, CHWHA, is the recorded code-detection gap) — every changed line a `<span class="ch-text">` / `<span class="jp-text">` wrap, nothing else.
- `_s30_r419_pagescore.py` (the gate's own `match()` BEFORE regenerating): **24 paired pages, 13 up / 7 down / 4 same, SCAFFOLD pp-sum +49.7 (mean +2.07pp), RAW +54.4** — CHFUN08 +30.1, JPN1004_8_0 +10.3, JPN1004_7_0 +8.3, CHI1005_0_0 +7.8, CHFUN05 +6.5; the seven dips (JPN1004_9_0 −7.4, _0_0 −5.1, _4_0 −4.9, _1_0 −4.3, _10_0 −2.7, _5_0 −0.4, CHFUN04 −0.6) inspected line by line (`_s30_r419_dipdiff.py`): the wrap is the gold's own form on every one; the pages are structurally far from the gold (the gold's vocabulary and dialogue TABLES against Claude's paragraphs, the gold's `<apan class="jp-text">` typo in the JPN1004 title on all 11 pages) and difflib's ratio falls when correct lines are added to a page whose neighbours cannot align — a KB-driven round is judged on its own verifier and the OTHER gates holding (LOOP §1b), and the corpus mean, the ≥50 bucket and compare_structure all rise.
- SCOPED regeneration (`_s30_r419_regen.sh`: the 13 + a fresh 12-module spot-check sample, 3 batches rc 0): `_content_manifest.py fresh` **0 truly stale**; `_scoped_spotcheck.py verify` **12 / 12 byte-identical under the fix**; the disk == the probe's ON pages 52 / 52.
- `scoped_ship.sh --affected _affected_r419.txt --toggle LANGFONT_OFF --no-regen --commit --round 419` (`_s30_r419_scoped_ship.log`): containment **13 ⊆ 13**, the decomposition gate proof — skeleton 54.19 → 54.21 IMPROVED, ≥50 1439 → 1441 IMPROVED, compare_structure exact 14168 → 14170 IMPROVED, every other row HELD; **RESULT: PASS**; the fast-loop baseline patched, the manifest refreshed, the ledger at scoped #3 since the r416 FULL.
- `run_all_gates.sh` (`_s30_r419_gates.log`): every row HELD-or-IMPROVED; every verifier RESULT ✓ identical to r418 (the dragAndDrop verifier's CHFUN05 — its Chinese drags now wrapped — 21 widgets / 148 drags / defect 0); entry parity PASS; index-sync OK. `_gatecheck.py` refuses on the mtime staleness of the untouched modules (the manifest proves them byte-identical) — the decomposition proof above is the verdict.
- `_s29_skdelta.py _s29_r418_sk_final.json _s30_r419_sk_final.json --affected _affected_r419.txt`: **20 movers, 13 up / 7 down, 0 outside the affected set; 0 pages added / gone**.
- 16 selftests GREEN (46 / 0); feature index GREEN; DIFF MINER **183 → 182 CANDIDATE rows** (count wobbles of ±1–3 on the language pages; the `ch-text` / `jp-text` title rows #8 / #9 / #10 / #13 / #20 / #22 stay below the floor — #9 is the gold's `apan` typo).

### 3. PROTECTED GATES (all HELD-or-IMPROVED — `_s30_r419_gates.log`, `_s30_r419_scoped_ship.log`)

- **Skeleton (PRIMARY)**: SCAFFOLD **54.186 → 54.207 % (+0.0212pp)**; ≥50 **1439 → 1441**, ≥75 **238**, ≥90 **20** EXACT; RAW **38.204 → 38.227 %**; 2349 pairs, skipped 0 (state `outputs/_s30_r419_sk_final.json`).
- **compare_structure** exact **14168 → 14170** (= the text-matched pool 16456 → 16458) / EXTRA **186** / MISSING **683** / row-wrap **23** EXACT; **body_compare** 54 / 5 / 190 / 247 EXACT; **defect** clean 2504 / 2548 = 98.27 %, leak 73 / 44 EXACT; tags **9557 / 9557**; every verifier EXACT.
- Plateau (§4): **+0.0212pp with ≥50 +2 — the window stays at 0 of 3**.

"""
p = PF + "BUILD_CHANGELOG.md"; s = rd(p)
head, rest = s.split("\n", 1)
assert head.startswith("# BUILD CHANGELOG") and rest.lstrip("\n").startswith("## 2026-09-20 (round 418")
wr(p, head + "\n\n" + entry + rest.lstrip("\n"))

p = PF + "app/js/Config.js"; s = rd(p)
old = '\tstatic AppVersion = "260619.89";'; assert s.count(old) == 1
note = ("\t// ROUND 419 (260619.90): THE LANGUAGE-FONT WRAP — KB constraint 92 / CL-0093: every run of Chinese / Japanese text takes `span.ch-text` / "
        "`span.jp-text` (ListsAndRuns.LanguageFontWrap at the PageAssembler whole-page seam, the pre-acks slice; data body_region.language_fonts, env "
        "LANGFONT_OFF; a run = CJK blocks joined by internal whitespace / brackets / slashes, starting on a character; kana → jp-text anywhere, Han → the "
        "module's language from the code-prefix map, bare where the module has none). The loop's session 30 Round 1: the gold wraps 5,437 of 5,512 runs "
        "(0.99), Claude shipped 3,812 bare on 26 pages / 14 modules; OFF = disk 2555 / 2555, ON 25 pages / 13 modules (13 up / 7 down, +49.7pp-sum); SCOPED "
        "regeneration of the 13 (scoped #3 since the r416 FULL); skeleton 54.186 -> 54.207 % (+0.0212pp), >=50 1439 -> 1441, cs exact +2, every other gate "
        "EXACT; miner 183 -> 182. Pinyin is the next round.\n")
wr(p, s.replace(old, note + '\tstatic AppVersion = "260619.90";'))

p = PF + "CLAUDE.md"; s = rd(p)
old9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 418 BASELINE ("; assert s.count(old9) == 1
new9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 419 BASELINE (the language-font wrap — every CJK run takes `span.ch-text` / "
        "`span.jp-text`, KB constraint 92 / CL-0093; `body_region.language_fonts`, env `LANGFONT_OFF`; 13 modules / 25 pages; SCOPED regeneration of the 13, "
        "the probe proving the other 481 byte-identical; scoped ship #3 since the r416 FULL): SCAFFOLD mean 54.207% / >=50% 1441 / >=75% 238 / >=90% 20 / "
        "RAW 38.227% @ 2349 pairs, pairs skipped 0 — hold-or-improve; 20 movers (13 up, 7 down — CHFUN08 +30.1, the JPN1004 dips named; 0 outside the "
        "affected set); the 2329 unaffected pairs EXACT. compare_structure 14170 / 186 / 683 / 23 (exact +2 = the text-matched pool +2); body_compare 54 / 5 "
        "/ 190 / 247 EXACT; defect clean 2504 / 2548 = 98.27%, leak 73 / 44 EXACT.** Previous — ROUND 418 BASELINE (")
s = s.replace(old9, new9)
old11 = "| `CDFIRSTROW_OFF` | 418 | **THE FIRST TILE PANEL TAKES"; assert s.count(old11) == 1
row11 = ("| `LANGFONT_OFF` | 419 | **THE LANGUAGE-FONT WRAP — every run of Chinese / Japanese text takes `span.ch-text` / `span.jp-text`** (KB constraint 92 / "
         "CL-0093, 13 Sept 2026, locked admin: the classes are MANDATORY on every occurrence and the conversion applies them; the autonomous loop's session 30 "
         "Round 1). `ListsAndRuns.LanguageFontWrap(html, run)` at the PageAssembler whole-page seam — after `LinkTextDisplay`, before `MathReplace`, the "
         "pre-acks slice only (the gold's acks credits stay bare 23 / 25) — so every emitter is covered at one seam (the `<h1>` title span, the menu, prose, "
         "lists, cells, callouts, built widgets, hand-off boxes). A RUN = blocks of CJK characters (Han, kana, CJK punctuation, fullwidth) joined by internal "
         "whitespace and the ASCII brackets / slashes / stops between two CJK blocks, starting on a Han / kana character or an opening bracket (a leading `：` "
         "stays outside), ending on a CJK character, holding ≥ 1 Han / kana. CLASS: any kana → `jp-text` regardless of module; Han-only → the module's "
         "language (`module_language`, longest code-prefix match: CHI / CHIFUN / CHFUN / CHWHA → ch, JPN / JPNFUN / JPFUN / JAP / JAPFUN → jp); Han-only in "
         "a module with no entry → bare (the KB's Red-Flag half not built; 5 runs / 4 non-language modules, video titles). Verbatim `<script>` / `<style>` / "
         "`<title>` / cv2-note / cv2-comment; idempotent inside an element already carrying the class. Measured (`_s30_r1_langfont.py`, `_s30_r1_langspans.py`): "
         "the gold 5,437 / 5,512 runs wrapped = 0.99, carrier span 98 %, every context, the `<b>` outside; Claude 3,812 bare runs on 26 pages / 14 modules. "
         "OFF = the r418 output (2555 / 2555). ON = 25 pages / 13 modules, 13 up / 7 down (+49.7pp-sum; the JPN1004 dips are alignment artefacts on pages "
         "structurally far from the gold — the form is the gold's own). Next: pinyin (its own detector); the cross-tag run (4 %); CHWHA's code detection. |\n")
s = s.replace(old11, row11 + old11)
old14 = "- **Build:** `260619.89` (round 418 — **the first tile panel takes"; assert s.count(old14) == 1
b14 = ("- **Build:** `260619.90` (round 419 — **the language-font wrap: every run of Chinese / Japanese text takes `span.ch-text` / `span.jp-text`** — KB "
       "constraint 92 / CL-0093, the CJK half (`body_region.language_fonts`, env `LANGFONT_OFF`; `ListsAndRuns.LanguageFontWrap` at the PageAssembler "
       "whole-page seam, the pre-acks slice); the autonomous loop's session 30 Round 1; the gold wraps 5,437 of 5,512 runs (0.99), Claude shipped 3,812 bare "
       "on 26 pages / 14 modules; the probe OFF = disk 2555 / 2555, ON 25 pages / 13 modules (13 up / 7 down, +49.7pp-sum, 0 outside the set); **SCOPED "
       "regeneration of the 13 (scoped ship #3 since the r416 FULL)**; **ROUND 419 BASELINE: SCAFFOLD mean 54.207% / >=50% 1441 / >=75% 238 / >=90% 20 / "
       "RAW 38.227% @ 2349 pairs** (+0.0212pp); compare_structure 14170 / 186 / 683 / 23 (exact +2), body 54 / 5 / 190 / 247, clean 2504 / 2548, leak 73 / "
       "44 — all EXACT; every verifier EXACT; 16 selftests GREEN; the miner 183 → 182; plateau window 0 of 3; pinyin next). Previous: ")
s = s.replace(old14, b14 + old14)
wr(p, s)

p = R + "CONVERTER_V2/reference/tests/gate_baseline.json"; s = rd(p)
def setv(key, old, new):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=1); assert n == 1, key
setv("build", '"260619.89"', '"260619.90"'); setv("round", 418, 419)
setv("mean_scaffold_pct", 54.19, 54.21); setv("pages_ge_50", 1439, 1441); setv("exact_chain", 14168, 14170)
a = '    "_note_r418": "Round 418 (session 29 Round 9)'; assert s.count(a) == 1
s = s.replace(a, '    "_note_r419": "Round 419 (session 30 Round 1): the language-font wrap — every CJK run takes span.ch-text / span.jp-text (KB constraint 92 / CL-0093; body_region.language_fonts, env LANGFONT_OFF; ListsAndRuns.LanguageFontWrap at the PageAssembler seam). SCOPED regeneration of the 13 language modules (scoped #3 since the r416 FULL); the probe proving the other 481 byte-identical.",\n' + a)
a2 = '    "_note_r417b": "Round 418: SCAFFOLD 54.1231'; assert s.count(a2) == 1
s = s.replace(a2, '    "_note_r418b": "Round 419: SCAFFOLD 54.1860 -> 54.2072 (+0.0212pp; 20 movers, 13 up / 7 down — CHFUN08 +30.1, JPN1004_8_0 +10.3; the JPN1004 dips are alignment artefacts, the form is the gold\'s; 0 outside the 13-module affected set), 1441 / 238 / 20, RAW 38.227; 2349 pairs. Plateau window 0 of 3.",\n' + a2)
b2 = '    "_note_r418": "Round 418: 14168 / 186 / 683 / 23 EXACT.",'; assert s.count(b2) == 1
s = s.replace(b2, '    "_note_r419": "Round 419: exact 14168 -> 14170 (+2 = the text-matched pool 16456 -> 16458); EXTRA 186 / MISSING 683 / row-wrap 23 EXACT.",\n' + b2)
b3 = '    "_note_r418": "Round 418: over-capture 54 / runaway 5 / EMPTY 190 / ANY 247 EXACT.",'; assert s.count(b3) == 1
s = s.replace(b3, '    "_note_r419": "Round 419: over-capture 54 / runaway 5 / EMPTY 190 / ANY 247 EXACT.",\n' + b3)
wr(p, s); json.load(open(p, encoding="utf-8"))
print("r419 finalise: changelog + Config.js 260619.90 + CLAUDE.md §9/§11/§14 + gate_baseline.json done")
