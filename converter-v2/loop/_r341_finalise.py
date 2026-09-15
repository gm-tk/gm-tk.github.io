#!/usr/bin/env python3
"""ROUND 341 (loop session 9, Round 1) — finalise: changelog, AppVersion (260619.11 → 260619.12), CLAUDE.md §9/§11/§14,
gate_baseline.json, KB status D-row, CONVERTER_V2_GUIDE.md A4, LOOP_STATE.md (what shipped + position + round log). Idempotent; LF kept."""
import io, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)

SK_B, SK_A, RAW_B, RAW_A = "51.112", "51.133", "35.285", "35.323"
SK_B4, SK_A4 = "51.1120", "51.1325"
GE50_B, GE50_A, GE75_B, GE75_A, GE90 = 1066, 1073, 201, 200, 15
CS_B, CS_A, EX_B, EX_A, MI_B, MI_A = 11379, 11482, 171, 175, 593, 608
PAIRS_B, PAIRS_A = 1954, 1962
DELTA = "+0.021"; PCT = "55.8"
MOVED = ("39 moved — 20 up / 19 down, every mover in the affected set, pp-sum +70.06 scaffold AND +68.51 RAW; per MODULE (the honest view where a "
         "page set changed) HIS1005 41.45 → 50.69 (+9.24; its page set is now the gold's own 15 — the 5.1 / 6.1 / 9.1 sub-page boundaries were "
         "near-red), ENGFUN02 11.71 → 26.76 (+15.05; 1 → 5 pairs toward the gold's 6), CEDO501 +1.16, HIS1002 +1.57, TRR102 +1.18, HIS1006 −0.33 "
         "(its per-page −43.05 / −19.15 are pure RENUMBERING — an earlier near-red boundary now splits, so `_9_0` is a different lesson; the "
         "r186 / r243 pairing class); the NAMED dips: OSGM501_5_0 −2.98 (77.01 → 74.03, the ≥75 down-crosser), OSAH501_5_0 −1.23, OSGM301_2_0 "
         "−2.59, OSGM401_1_0 −0.77, OSOH301_1_0 −2.11, OSOH401_1_0 −1.38 = the near-red `[Click drop]` cells now BUILD the real clickDrop "
         "(4 buttons + 4 panels; the gold's own widget — OSGM501 lesson 5 gold ships 11 clickDrop buttons) where a `bilingual-unbuilt` dump with "
         "literal tags stood — the dump had collapsed to ONE widget marker that coincidentally matched the gold's, the r176 / r186 net-positive "
         "class (RAW rises on five of the six: OSGM501 53.6 → 57.1, OSGM301 39.8 → 42.7, OSGM401 41.7 → 44.9, OSOH301 23.6 → 25.5, OSOH401 "
         "20.0 → 20.4); HIS1005_2_0 −17.27 = the writer's `[Interactive] Please insert this image with the caption` tag (invisible before) now "
         "opens the hand-off box the tag asks for, where the gold shipped an image + caption (an A1 gold substitution); TRR109_5_0 −4.35 = the "
         "writer's `[Button] [Checklist]` now opens a widget box where the gold hand-built a drag-and-drop (48 `drag` / 29 `drop` — decision 5's "
         "population); ARFUN05_0_0 −5.04 = its two `[Insert video]` lines now embed the gold's OWN videos (YfNmlY1-t5k, MlXi8LfKv-0 — both in "
         "the gold page) on the single-page r322-named module, the alignment artefact; CEDO501_2_1 −2.65, HIS1005_0_0 −3.90, HIS1002_3_0 / "
         "_11_0, HIS1006_0_0, XDLS904/905 ≤ 0.4 = the same alignment class on pages whose literal `<p>[tag] …</p>` lines had matched gold `<p>`s "
         "by coincidence")
CSDEC = ("EXTRA +4 and missing +15 are ENTIRELY HIS1005 (matched +133 / exact +107 — its page set is now the gold's, so 133 more elements "
         "text-match; the EXTRA sites are the now-built overview whakataukī box's `row > col` around what the gold puts straight in a `col`, the "
         "r61 greenlit class on newly-matched elements; the missing are the gold's editorial `alert` wrappers on the same pages) with HIS1006 "
         "missing −2; TRR109 matched −14 / exact −14 = the checklist section moving inside a widget subtree the comparator excludes (the r57 / "
         "r147 relocation artefact); no module outside the 23 moved (`_r341_cs_decomp.log`)")
VER = ("the literal-tag-leak gate's own predicate over the 23 changed modules (`_r341_quality.py`): **269 → 7** leaks, no module worse; "
       "corpus-wide **288 / 46 → 26 / 23** — the 26 left are the plain-BLACK tag class (~20 sites: XGF9004's `000000` `[H3]`, ANZH401's `[H3]` "
       "inside an alert's black text, HIS1002 / MXDI201 `[Body Text]`, ENGI102's `[image]` asset briefs …), the three bilingual-cell "
       "`[Item N] [Image]` lines (TRR102 / TRR106 / TRR304 — the r167 reoMode class) and AGH1006's widget-release `[H3] Knowledge Check`; "
       "the word-loss check over the 23 (`_r341_quality.log`, every word incl. notes / dumps / attribute values): the only losses are the "
       "literal tag tokens themselves, URL fragments consumed into asset placeholders / embeds, the old dumps' `Empty` cells, duplicated "
       "instruction text, and ENGFUN02's trailing SUBMISSION-CHECKLIST boilerplate (the gold never ships it — a near-red end marker is now "
       "honoured)")

# ---------------------------------------------------------------- 1. BUILD_CHANGELOG.md
CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)" + chr(10) + chr(10)
ENTRY = f"""## 2026-09-16 (round 341, build 260619.12) — A WRITER'S TAG TYPED IN A NON-STANDARD RED IS STILL A TAG (the near-red run rule: `ed0000` / `fa0000` / `c00000` … count as red when they carry a bracket; the literal-tag-leak gate 288 / 46 → 26 / 23; the autonomous loop's session-9 Round 1 — the loop's first fresh PICK after the session-8 EXHAUSTION stop; **FULL regeneration of all 416 gated dirs, doubling as the full-ship backstop — the ledger resets to 0**)

### 1. WHAT CHANGED, IN ONE LINE

**The engine scanned ONLY a run whose Word colour was exactly `ff0000` or `ee0000` for tags, so a writer whose red was a different shade — the HIS NCEA1 writer's `ed0000`, ENGFUN02's `fa0000`, Word's standard "Dark Red" `c00000` in the OS* / CED / ARFUN / TEFUN modules — had every tag ship as literal text (`<p>[H3] Using browser controls to navigate the web</p>`). A run in the red hue band (r ≥ 176, g ≤ 64, b ≤ 64) now counts as red — but ONLY when it carries a `[` or `]` (or continues a bracket an earlier near-red run of the same paragraph opened), because `c00000` is also used for CONTENT and a blanket rule would strip it as an instruction. Strictly additive: no run that is red today changes, no bracket-less run changes. Riding on the same toggle family: the r299 definition weave learns the parenthesised-tail form (`aroha [definition] (Love, concern, compassion.) is important.` → the parenthesis is the tooltip, the sentence continues) and lets a paragraph's 4th definition still find its sentence.** Data `Input_Doc_Rules.red_runs.near_red_tag_runs` · env `NEARRED_OFF`; data `orphan_definition_weave.paren_tail_def` + `lookback_skips_consumed` · env `DEFPAREN_OFF`.

### 2. THE EVIDENCE (docx → human → Claude)

- **HIS1005 overview** — WT `[H1] Ātete | Resist – Part A` (run colour `ed0000`) / `[Body text] The whakataukī chosen…` / `[H2] The past shapes the present` → gold `<h2>Ātete | Resist – Part A`, `<p>The whakataukī chosen…`, `<h2>The past shapes the present` → Claude before `<p>[H1] Ātete | Resist – Part A</p>`, `<p>[Body text]</p>`; after the headings and paragraphs — and its lesson pages 5.1 / 6.1 / 9.1 (near-red boundaries) appear: **the module now ships the gold's exact 15-page set**.
- **CEDO501 lesson 3** — WT `[H3] Using browser controls to navigate the web` (`c00000`) → gold `<h3>Using browser controls to navigate the web</h3>` → Claude before `<p>[H3] Using browser controls to navigate the web</p>`; after the `<h3>`.
- **ENGFUN02** — WT `[H1] Lesson 1 Basic Camera Shots [H2] Close-up [H3] Definition: [Body] A close-up shot is…` (every tag `fa0000`) → gold `<h2>Close-up</h2>` … → Claude before ONE paragraph carrying 150 literal tags on 2 pages; after 5 pages of headings and prose (the gold has 6).
- **XDLS905 lesson 7** — WT `standard of living adequate [definition] (amount needed) for the health…` (`c00000`) → gold `<span class="infoTrigger" info="amount needed">adequate</span> for the health…` → Claude before the literal `[definition] (amount needed)…`; after the gold's own span, sentence intact.
- **The KB:** silent on the SHADE of red — its own raw-docx path reads bare `[tag]` brackets as tags with no colour at all (00B line 125; 02B "Red Text Rules" parses red text for embedded tags). LOOP §1b level 3 / 4 — the gold renders every near-red tag as its tag on every triangulated site. Class B-i (a derivable input the converter dropped).

### 3. THE MEASUREMENT (`outputs/_measure_r342_blacktags.py` → `_r342_blacktags.{{json,log}}` — every bracket group in every Writers Template that folds to a Tag_Lexicon alias, tallied by the colour of the run holding its `[`; the risk side `_measure_r342_nearred_content.py` → `_r342_nearred_content.log`; the split-tag count inline)

- **96,817 tag brackets are `ff0000` / `ee0000`; 1,169 are not** — NEAR-RED (hue red, not on the list) **598**: `ed0000` 311 · `fa0000` 165 · `c00000` 120 · `ed1c24` 1 · `f72b2b` 1, on **30 modules (28 gated)** — Standard 17 (HIS1005 97, HIS1002 83, CEDO501 27, HIS1006 15, OSGM301/401/501 + OSAH501 + OSOH301/401 32, HIS1001 3, XDLS904/905/912, ENGS101, ENGI102, PES1008), Bilingual 8 (TRR102 72, TRR111 20, TRR103/106/109/112/113 33), Fundamentals 3 (ARFUN05 15, TEFUN03 10, TEFUN05), Inquiry 2 (ENGFUN02 164, CEDK401 5); link-BLUE 250 (the BLL writers' hyperlinked `[audio N]` — a hyperlinked-tag mechanism, recorded); plain BLACK ≈ 300 (`auto` 192 / `000000` 101 — a content-vs-tag ambiguity the r73 strip already handles for `[body]`, recorded). 887 paragraph-leading / 282 mid-paragraph.
- **The risk that shaped the rule:** near-red runs with NO bracket — `ed0000` 170 paragraphs (HIS1002's drag-and-drop label lists and instructions, HIS1005 "Please place this original image…", TRR102 answer keys), `c00000` 46 — and **`c00000` is CONTENT in MXFU302 ("+ 5 = 9" ×7), ENGI401 ("tone" / "pace"), ENGS301, MXEX401, CEDO501's own word list ("Internet" / "Website"), OSGM301/501's option lines**. A blanket "near-red = red" would have turned that content into stripped red-text instructions → the bracket fence. Every one of the 598 bracket-bearing near-red runs resolves to a lexicon tag (1.00; no template or subject group below 0.60).
- **The split-tag case (51 sites, HIS1002 32):** Word breaks one tag across runs (`[Can the white space … ` + `be decorated…]`) and the middle piece carries no bracket — a per-run test would fragment the tag. A paragraph-scoped bracket DEPTH keeps every near-red run red while an earlier near-red run's bracket is open; a black run with real text ends the context — exactly what the standard red does inside a bracket.
- **The two weave refinements the probe forced (debug, never revert — §0b):** the now-red `[definition]` markers of XDLS904 / XDLS905 reached the r299 weave, which took the WHOLE tail as the definition (`info="(Love, concern, compassion.) is important."` — the sentence's end swallowed into the tooltip). (a) `paren_tail_def`: a closed empty `[definition]` whose tail OPENS with a parenthesised phrase and then continues takes the parenthesis as the definition (parens dropped — the gold's `info="amount needed"` form) and lets the prose resume; a full-tail `(def)` keeps the standing form. (b) `lookback_skips_consumed`: a marker this pre-pass already consumed spends no lookback budget — but ONLY within the same source paragraph (`block`): the first cut reached the PREVIOUS paragraph and the named-anchor shape then matched the literal word "Hover" inside that paragraph's earlier tooltip (CEDT104-0.0 lost four hovers; the fence restored it byte-for-byte). On standard-red sites the pair moves exactly ONE page, gold-ward: PES1003_8_0 `info="(adiabatic …"` → `info="adiabatic …"` (gold: `info="Adiabatic means no thermal energy…"`, no parens).

### 4. THE FIX — one extractor seam + one weave branch, all data-fenced

- **`DocxExtractor.#parseParagraph`:** `listRed = red_hex_values.includes(color)`; `nearRed = !listRed && nearRedOn && #nearRed(color, nr) && (!require_bracket || nearOpen > 0 || /[\\[\\]]/.test(text))`; `red = listRed || nearRed`; a paragraph-scoped `nearOpen` counter tracks the bracket depth left open by near-red runs (a black run with real text resets it). `static #nearRed(hex, nr)` = the hue band from the data (`min_r` 176 / `max_g` 64 / `max_b` 64; `c0504d`, Word's Accent-2, falls outside on g). The exact list stays the primary rule — `red_hex_values` is untouched. Data `Input_Doc_Rules.red_runs.near_red_tag_runs` {{enabled, env NEARRED_OFF, min_r, max_g, max_b, require_bracket}}.
- **`ContentConverter.#definitionWeavePrepass`:** in the empty-inner branch, `paren_tail_pattern` (`^\\s*\\(([^()]{{1,400}})\\)\\s*([\\s\\S]*)$`) on the tail when no closer span follows — group 1 the definition, group 2 the continuation (only when non-empty); `carriersBehind` skips a `_defWeaveConsumed` item of the same `block` without spending budget. Data `elements.hover_definition_inline.orphan_definition_weave.paren_tail_def` + `lookback_skips_consumed`; env `DEFPAREN_OFF` (both refinements; `DEFWEAVE_OFF` still reverts the whole pre-pass).

### 5. THE PROOF AND THE GATES

- The in-memory probe over ALL 416 modules in THREE legs (`_r341_probe.cjs` / `_r341_probe_run.sh`): **ALL-OFF (`NEARRED_OFF` + `DEFPAREN_OFF`) = disk 2102 / 2102; `NEARRED_OFF` alone = disk on 2101 (PES1003_8_0 — the weave refinement's one standard-red site, gold-ward, named above); ON = 76 pages changed + 10 new pages across 23 modules** (`_r341_affected.txt` = the 22 near-red modules with a Claude dir that carry a fired bracket + PES1003; TRR103/111/112/113, TEFUN05, CEDK401 carry near-red brackets whose recognition changes no byte). **FULL regeneration** of all 416 gated dirs (the r335 batch list, 36 batches, 4 workers, `_r341_fullship_par.sh`; three batches returned rc 1 under the parallel run with empty logs and rc 0 alone — a transient on the mounted filesystem; `_r341_fullship_regen.log`); `_stalecheck.sh` **0 stale**; `_content_manifest.py diff` = **88 pages: 76 changed / 10 added / 2 removed, exactly the 23 modules; the other 393 byte-identical**; the regenerated disk == the probe's ON pages on all 184 pages of the 23.
- **Skeleton (PRIMARY): SCAFFOLD mean {SK_B}% → {SK_A}% ({DELTA}pp; {SK_B4} → {SK_A4}) / ≥50% {GE50_B} → {GE50_A} (+7) / ≥75% {GE75_B} → {GE75_A} (−1 NAMED) / ≥90% {GE90} / skipped 0 @ {PAIRS_B} → {PAIRS_A} pairs; RAW {RAW_B}% → {RAW_A}%** (state `outputs/_r341_sk_final.json`, FRESH). {MOVED}. The ≥50 arithmetic: 4 crossers up (HIS1005_5_0 / _6_0 / _9_0, HIS1006_10_0) + 6 added pages above 50 − 2 down (HIS1006_9_0 / _11_0, the renumbering) − 1 dropped page above 50 = +7 (`_r341_sk_movers.log`). The fast-loop's `--accept-named` used for the ≥75 −1 and the two compare_structure counters (the r289 named-movement override).
- **compare_structure exact {CS_B} → {CS_A} (+103) / EXTRA {EX_B} → {EX_A} / missing {MI_B} → {MI_A}** — {CSDEC}.
- **Structurally clean 2056 / 2102 (97.81%) → 2087 / 2110 (98.91%); literal-tag leak 288 / 46 → 26 / 23** (the corpus is 2110 pages now: +10 −2). Every other gate EXACT (full suite `_r341_gates.log`): body **191** · tags **9557 / 9557** · flipCard TOTAL 61 divergence 0 · index-sync 33/28 · entry-parity PASS · mtkQuiz shells defect 0 · the modal / dropdown / accordion / tabs / carousel / hintSlider / speechBubble verifiers over the 23 (`_r341_verify_*.log`) — accordion 32 panels / 9 modules every panel matching the human, defect 0; clickDrop 41 items defect 0 (the new OSGM / OSOH / OSAH builds included); flipCard over the 23 = the tracked baseline; 13 selftests GREEN (`_r341_selftests.log`).
- **Verifier:** {VER}.
- **The fresh PICK that found the class:** the session opened on the session-8 EXHAUSTION stop with no decision from Chris, so §3 step 1 was re-run from scratch — the r340 substitution ranking row by row (the one un-named Standard row, `div.col-md-8.col-12 ⇐ div.col-12` 140 sites / 112 pages, is the activity box's INNER column where Claude is KB-correct, c63), the 16-shard census + `_coverage_dashboard.py --refresh` (`_r342_dashboard.log`; rows 1–21 are the un-built interactives = decision 5, the advisory aggregates, the empty boxes sized at r325, over-capture — and **row 15, the literal-tag LEAK, a PROTECTED GATE that had sat at 288 / 46 through every round and never had a PICK**), and KB §D (nothing ≥ 20 pages left unblocked). The leak decomposed (`_r342_leaks.py`) to the near-red class above.

### 6. NAMED, NOT CHASED

- The plain-BLACK tag class (≈ 300 brackets; the 26 residual leaks are mostly it — XGF9004's `000000` `[H3]`, ANZH401's `[H3]` inside an alert's black text, `[Body Text]` / `[body text]` lines in HIS1002 / MXDI201, ENGI102's `[image]` asset briefs): a black bracket is legitimately content sometimes (`[sic]`, `[1]`, `[Item 41]`), so it needs its own measured discriminator — a follow-up PICK if it clears 20 pages. The link-BLUE `[audio N]` class (250 brackets, the BLL writers' hyperlinked tags; 3 of the 5 heaviest modules have no Claude dir). The bilingual-cell `[Item N] [Image]` leaks (TRR102 / 106 / 304 — the r167 reoMode class). AGH1006's `[H3] Knowledge Check` (a standard-red tag released from an `[interactive: true/false]` capture as raw text — the widget-release class). HIS1002 / HIS1006's over-pagination (gold 11 / 5 pages vs Claude 21 / 15 — pre-existing; the writer's near-red `[LESSON]` / `[End page]` markers now behave exactly as the red ones, +1 page each). The A1 substitutions named in §5 (HIS1005_2_0's `[Interactive]` instruction, TRR109_5_0's hand-built drag-and-drop).

**Ledger:** FULL ship — counter reset to 0 (the r334 backstop's successor; the six scoped ships r335–r340 proven complete: the manifest diff is exactly this round's 23 modules) · data `Input_Doc_Rules.red_runs.near_red_tag_runs` + `Emit_Templates.elements.hover_definition_inline.orphan_definition_weave.paren_tail_def` / `lookback_skips_consumed` · env `NEARRED_OFF` / `DEFPAREN_OFF` · tools `outputs/_measure_r342_blacktags.py` (+ `_r342_blacktags.{{json,log}}`), `_measure_r342_nearred_content.py` (+ `.log`), `_r342_leaks.py` (+ `_r342_leaks.{{json,log}}`), `_r342_col12_sites.py` (+ `.log`), `_r342_census.sh` + `_r342_dashboard.log`, `_r341_probe.cjs` + `_r341_probe_run.sh` + `_r341_shard_0*` + `_r341_probe_{{alloff,off,on}}_0*.log`, `_r341_affected.txt`, `_r341_quality.py` (+ `.log`), `_r341_fullship_run.sh` + `_r341_fullship_par.sh` + `_r341_fullship_regen.log`, `_r341_manifest_changed.txt`, `_r341_proof.sh`, `_r341_fastloop.log`, `_r341_gates.log`, `_r341_sk_final.json` / `_r341_sk_full.log`, `_r341_sk_movers.log`, `_r341_cs_decomp.log`, `_r341_selftests.log`, `_r341_verify_*.log`, `_r341_leaks_after.py` (+ `.log`), `_r341_feature_index.log`, `_r341_fastloop_snapshot.log`, `_r341_finalise.py` · AppVersion 260619.12.

"""
if "round 341, build 260619.12" not in s:
    assert s.startswith(head); s = head + ENTRY + s[len(head):]; wr(CL, s); print("changelog prepended")

# ---------------------------------------------------------------- 2. Config.js
CF = os.path.join(PF, "app", "js", "Config.js"); c = rd(CF)
OLD = '\tstatic AppVersion = "260619.11";' + chr(10)
NEW = ('\t// ROUND 341 (2026-09-16, build 260619.12): a writer\'s tag typed in a NON-STANDARD RED is still a tag — a run in the red hue' + chr(10) +
       '\t// band (ed0000 / fa0000 / c00000 …) counts as red when it carries a bracket or continues an open one (DocxExtractor,' + chr(10) +
       '\t// Input_Doc_Rules.red_runs.near_red_tag_runs, env NEARRED_OFF); the r299 definition weave learns the parenthesised-tail' + chr(10) +
       '\t// form + a same-paragraph lookback (env DEFPAREN_OFF). Leak gate 288/46 -> 26/23; FULL regeneration (the backstop).' + chr(10) +
       '\tstatic AppVersion = "260619.12";' + chr(10))
if '"260619.12"' not in c:
    assert c.count(OLD) == 1; c = c.replace(OLD, NEW, 1); wr(CF, c); print("AppVersion bumped")

# ---------------------------------------------------------------- 3. CLAUDE.md §9 / §11 / §14
CM = os.path.join(PF, "CLAUDE.md"); m = rd(CM)
OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 340 BASELINE (a standalone [link]-family paragraph whose text is nothing but a video url is the embedded video"
NEW9 = (f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 341 BASELINE (a writer's tag typed in a NON-STANDARD RED is still a tag — the near-red run rule; FULL regeneration, the backstop): SCAFFOLD mean {SK_A}% / >=50% {GE50_A} / >=75% {GE75_A} / >=90% {GE90} / skipped 0 @ {PAIRS_A}; RAW {RAW_A}%** (state `outputs/_r341_sk_final.json`, FRESH; the corpus is 2110 pages now — 10 added / 2 removed by near-red page boundaries; pairs {PAIRS_B} → {PAIRS_A}). r341 {DELTA} ({MOVED}); compare_structure exact {CS_B} → {CS_A} / EXTRA {EX_B} → {EX_A} / missing {MI_B} → {MI_A} ({CSDEC}); clean 97.81% → 98.91%; leak 288/46 → 26/23; every other gate EXACT. Older r340 text: **ROUND 340 BASELINE (a standalone [link]-family paragraph whose text is nothing but a video url is the embedded video")
if "ROUND 341 BASELINE" not in m:
    assert m.count(OLD9) == 1, "§9"; m = m.replace(OLD9, NEW9, 1); print("§9")
ROW = ("| `NEARRED_OFF` | 341 | **A WRITER'S TAG TYPED IN A NON-STANDARD RED IS STILL A TAG** (the autonomous loop's session-9 Round 1 — the fresh PICK after the session-8 exhaustion stop; the literal-tag-leak gate 288/46 → 26/23; **FULL regeneration, the backstop**). Reverts byte-for-byte (ALL-OFF in memory = disk 2102/2102). ON (default), `Input_Doc_Rules.red_runs.near_red_tag_runs` `{ enabled, env, min_r 176, max_g 64, max_b 64, require_bracket true }`: in `DocxExtractor.#parseParagraph` a run whose `w:color` is in the red hue band but not on `red_hex_values` (`ed0000` the HIS NCEA1 writer / `fa0000` ENGFUN02 / `c00000` Word's Dark Red in the OS* / CED / ARFUN / TEFUN modules — 598 tag brackets on 30 modules, measured `outputs/_measure_r342_blacktags.py`) counts as RED when it carries a `[` or `]`, or continues a bracket an earlier near-red run of the SAME paragraph left open (`nearOpen` depth — Word splits a tag across runs 51 times, HIS1002 32); a bracket-less near-red run outside any bracket stays black, because `c00000` is also writer CONTENT (MXFU302 \"+ 5 = 9\", ENGI401 \"tone\" / \"pace\"). Strictly additive; the exact list stays primary. OFF: every near-red tag ships as literal text again. |\n"
       "| `DEFPAREN_OFF` | 341 | **THE PARENTHESISED-TAIL DEFINITION + the same-paragraph lookback** (two refinements of the r299 definition weave, surfaced when the near-red rule let XDLS904 / XDLS905's `c00000` `[definition]` markers reach it). Reverts both. ON (default), `orphan_definition_weave.paren_tail_def` + `paren_tail_pattern` + `lookback_skips_consumed`: a closed empty `[definition]` whose black tail OPENS with a parenthesised phrase and then CONTINUES — `aroha [definition] (Love, concern, compassion.) is important.` — takes the parenthesis as the definition (parens dropped, the gold's `info=\"amount needed\"` form) and lets the prose after it resume the sentence (a full-tail `(def)` keeps the standing form); and a marker the pre-pass already consumed spends no lookback budget WITHIN the same source paragraph (so the 4th definition of one sentence still finds it — XDLS905-7.0), never across paragraphs (the first cut reached the previous paragraph and the named-anchor shape matched the word \"Hover\" inside its tooltip, CEDT104-0.0). Standard-red reach: exactly ONE page, PES1003_8_0, gold-ward. `DEFWEAVE_OFF` still reverts the whole pre-pass. |\n")
if "| `NEARRED_OFF` | 341 |" not in m:
    A = "| `LINKVID_OFF` | 340 |"; assert m.count(A) == 1, "§11"; m = m.replace(A, ROW + A, 1); print("§11")
B14 = (f"- **Build:** `260619.12` (round 341 — **a writer's tag typed in a NON-STANDARD RED is still a tag** (the near-red run rule — `ed0000` / `fa0000` / `c00000` count as red when they carry a bracket; the r299 weave's parenthesised-tail form; the autonomous loop's session-9 Round 1; **FULL regeneration of all 416 dirs — the full-ship backstop, ledger reset to 0**). **ROUND 341 BASELINE: SCAFFOLD mean {SK_A}% / ≥50% {GE50_A} / ≥75% {GE75_A} / ≥90% {GE90} / skipped 0 @ {PAIRS_A}; RAW {RAW_A}%** (state `outputs/_r341_sk_final.json`, FRESH) = **{PCT}% of achievable** (ceiling 91.6%). {DELTA}pp ({SK_B4} → {SK_A4}; ≥50 +7, ≥75 −1 NAMED — OSGM501_5_0's real clickDrop build replacing a coincidentally-matching dump; 39 moved, per-module HIS1005 +9.24 with the gold's exact 15-page set, ENGFUN02 +15.05, every dip named — see §9). cs exact **{CS_A}** (+103) / EXTRA **{EX_A}** (+4) / missing **{MI_A}** (+15 — both entirely HIS1005's +133 matched pool, named); **clean 2087/2110 = 98.91%** (was 97.81%) / **leak 26/23** (was 288/46); every other gate EXACT: body **191** · tags **9557/9557** · flipCard TOTAL 61 divergence 0 · index-sync 33/28 · entry-parity PASS · mtkQuiz shell defect 0 · all THIRTEEN selftests GREEN. Corpus **2110 pages / 413 modules** (+10 −2 pages: near-red page boundaries), 0-stale, **76 pages changed / 10 added / 2 removed across 23 modules, the other 393 byte-identical**. Env `NEARRED_OFF` / `DEFPAREN_OFF`.\n")
if "- **Build:** `260619.12` (round 341" not in m:
    A = "- **Build:** `260619.11` (round 340 —"; assert m.count(A) == 1, "§14"; m = m.replace(A, B14 + A, 1); print("§14")
wr(CM, m)

# ---------------------------------------------------------------- 4. gate_baseline.json
GB = os.path.join(HERE, "..", "reference", "tests", "gate_baseline.json"); raw = rd(GB); d = json.loads(raw)
d["_meta"]["build"] = "260619.12"; d["_meta"]["round"] = 341; d["_meta"]["date"] = "2026-09-16"
d["skeleton"].update({"mean_scaffold_pct": float(SK_A), "raw_mean_pct": float(RAW_A), "pages_ge_50": GE50_A, "pages_ge_75": GE75_A, "pages_ge_90": GE90})
if "compare_structure" in d and isinstance(d["compare_structure"], dict):
    cs = d["compare_structure"]
    if "exact_chain" in cs: cs["exact_chain"] = CS_A
    for k, v in (("extra_container", EX_A), ("claude_extra_container", EX_A), ("missing_container", MI_A), ("claude_missing_container", MI_A)):
        if k in cs: cs[k] = v
for sect in ("defect", "structural_defect", "defect_audit"):
    if sect in d and isinstance(d[sect], dict):
        for k, v in (("leak_occ", 26), ("leak_pages", 23), ("literal_tag_leak_occ", 26), ("literal_tag_leak_pages", 23), ("clean_pages", 2087), ("total_pages", 2110), ("clean_pct", 98.91)):
            if k in d[sect]: d[sect][k] = v
d["_meta"]["_round341_note"] = (f"Round 341 (a writer's tag typed in a non-standard red is still a tag — the near-red run rule; FULL regeneration, the backstop). "
    f"Skeleton {SK_B4}->{SK_A4} ({DELTA}pp; >=50 {GE50_A}, >=75 {GE75_A} (-1 named: OSGM501_5_0), >=90 {GE90}; pairs {PAIRS_B}->{PAIRS_A}); cs exact {CS_B}->{CS_A}, "
    f"EXTRA {EX_B}->{EX_A} / missing {MI_B}->{MI_A} (HIS1005's matched-pool growth, named); clean 97.81->98.91%; leak 288/46->26/23; every other gate EXACT. Corpus 2110 pages.")
wr(GB, json.dumps(d, ensure_ascii=False) + (chr(10) if raw.endswith(chr(10)) else "")); print("gate_baseline.json refreshed")

# ---------------------------------------------------------------- 5. KB_AMALGAMATION_STATUS.md D-row
KB = os.path.join(HERE, "..", "..", "KB_AMALGAMATION_STATUS.md"); k = rd(KB)
anchor = "| ~~—~~ | 01E `[video]` → `videoSection` extended to a STANDALONE `[link]`-family paragraph"
drow = (f"| ~~—~~ | (not a KB row — the KB is silent on the SHADE of red; its raw-docx path reads bare `[tag]` brackets with no colour at all, 00B line 125) a writer's tag typed in a NON-STANDARD RED is still a tag — the near-red run rule (`ed0000` / `fa0000` / `c00000` … count as red when they carry a bracket or continue an open one) | **SHIPPED round 341** (the literal-tag-leak gate 288 / 46 → 26 / 23; 598 near-red tag brackets on 30 modules; HIS1005 ships the gold's exact 15-page set; FULL regeneration — the backstop) | 76 pages changed + 10 added / 23 modules | {DELTA}pp / ≥50 +7 / ≥75 −1 named / cs exact +103 / clean 97.81 → 98.91% | `NEARRED_OFF` (+ `DEFPAREN_OFF` for the r299 weave's parenthesised-tail form) | CAPTURED-LIVE (gold, §1b level 3 — the writer's tag is the writer's tag whatever its shade) |\n")
if "the near-red run rule" not in k:
    assert k.count(anchor) == 1; k = k.replace(anchor, drow + anchor, 1); print("KB status D-row")
wr(KB, k)

# ---------------------------------------------------------------- 6. CONVERTER_V2_GUIDE.md A4
GD = os.path.join(PF, "..", "CONVERTER_V2_GUIDE.md"); g = rd(GD)
OLDG = "  - `red_hex_values` — **if a writer uses a new shade of red** and their tags stop being recognised, add the six-digit hex colour here. This is the single most common fix in this file."
NEWG = ("  - `red_hex_values` — the exact shades the converter treats as \"red text\" in every case. **Since round 341 a near-red shade is caught automatically** — see `near_red_tag_runs` below — so this list only needs a new entry for a shade OUTSIDE the red band (or when a writer's red must count as red even on runs that carry no bracket).\n"
        "  - `near_red_tag_runs` (round 341) — `{ \"enabled\": true, \"env\": \"NEARRED_OFF\", \"min_r\": 176, \"max_g\": 64, \"max_b\": 64, \"require_bracket\": true }`. Writers do not all use the template's exact red: the History writer's tags are `ed0000`, ENGFUN02's are `fa0000`, and many use Word's standard \"Dark Red\" `c00000`. A run in that hue band now counts as red **only when it carries a square bracket** (or continues a bracket an earlier near-red run of the same paragraph opened) — because dark red is also used for ordinary content (`+ 5 = 9`, a highlighted word), and treating that as red would strip it as an instruction. Before this rule those writers' tags shipped as literal text on the page (`<p>[H3] Using browser controls…</p>` — the bulk of the literal-tag leak). Widen the band only with a measurement (`outputs/_measure_r342_blacktags.py` tallies every bracket by run colour).")
if "near_red_tag_runs" not in g:
    assert g.count(OLDG) == 1, "guide A4"; g = g.replace(OLDG, NEWG, 1); wr(GD, g); print("guide A4")

# ---------------------------------------------------------------- 7. LOOP_STATE.md
LS = os.path.join(HERE, "..", "..", "LOOP_STATE.md"); s = rd(LS); nl = chr(13) + chr(10) if chr(13) + chr(10) in s[:3000] else chr(10)
def L(t): return t.replace(chr(10), nl)
SEC = L(f"""## Session 9 · Round 1 (engine r341) — what shipped (a writer's tag typed in a NON-STANDARD RED is still a tag — the near-red run rule)
- **Fix:** `Input_Doc_Rules.red_runs.near_red_tag_runs` {{enabled, env NEARRED_OFF, min_r 176, max_g 64, max_b 64, require_bracket true}} +
  `DocxExtractor.#nearRed` + a paragraph-scoped `nearOpen` bracket depth in `#parseParagraph`: a run whose colour is in the red hue band but
  not on `red_hex_values` counts as red when it carries a `[` / `]` or continues a bracket an earlier near-red run of the same paragraph
  opened; a bracket-less near-red run outside any bracket stays black (the content fence — `c00000` is writer content in MXFU302 / ENGI401 /
  ENGS301). The exact list stays primary; strictly additive. **Riding on `DEFPAREN_OFF`:** the r299 definition weave's parenthesised-tail
  form (`paren_tail_def` — `aroha [definition] (Love, concern, compassion.) is important.` → the parenthesis is the tooltip, the sentence
  continues; XDLS904 / XDLS905 now match the gold's own `info="amount needed"` spans) + `lookback_skips_consumed` (a consumed marker spends
  no lookback budget within the SAME paragraph — the 4th definition of one sentence still finds it; the first cut crossed into the previous
  paragraph and mis-anchored CEDT104's hovers on the word "Hover" inside an earlier tooltip → fenced to the same `block`, byte-identical).
- **Regeneration:** FULL (all 416 gated dirs, 36 batches / 4 workers, `_r341_fullship_par.sh`; 3 batches rc 1 under the parallel run with
  empty logs, rc 0 alone — a mounted-filesystem transient; 0 stale). The three-leg in-memory probe over ALL 416 modules first: ALL-OFF = disk
  2102/2102; `NEARRED_OFF` alone = disk on 2101 (PES1003_8_0 = the weave refinement's one standard-red site, gold-ward, named); ON = 76
  changed + 10 new pages / 23 modules (`_r341_affected.txt`: ARFUN05 CEDO501 ENGFUN02 ENGS101 HIS1001 HIS1002 HIS1005 HIS1006 OSAH501 OSGM301
  OSGM401 OSGM501 OSOH301 OSOH401 PES1003 PES1008 TEFUN03 TRR102 TRR106 TRR109 XDLS904 XDLS905 XDLS912). Manifest diff = exactly those 23
  (76 / 10 / 2 removed), the other 393 byte-identical — the six scoped ships r335–r340 proven complete (the backstop); disk == probe ON on all
  184 pages of the 23. Quality (`_r341_quality.py`): leaks over the 23 by the gate's own predicate 269 → 7, no module worse; word-loss = tag
  tokens, URL fragments consumed into assets, the old dumps' "Empty" cells, duplicated instruction text, ENGFUN02's submission-checklist
  boilerplate (gold never ships it). Pagination: HIS1005 12 → 15 = the gold's exact page set; ENGFUN02 2 → 5 (gold 6); HIS1002 20 → 21 and
  HIS1006 14 → 15 (both over-paginated before; the near-red boundary tags now behave like the red ones — named).
- **Gates:** skeleton {SK_B} → {SK_A} ({DELTA}pp; {SK_B4} → {SK_A4}; pairs {PAIRS_B} → {PAIRS_A}); ≥50 {GE50_B} → {GE50_A} (+7); ≥75 {GE75_B} → {GE75_A} (−1 NAMED:
  OSGM501_5_0 77.01 → 74.03 — the near-red `[Click drop]` cells now BUILD the real 4-button clickDrop where a dump with literal tags had
  collapsed to a coincidentally-matching marker; RAW +3.5); ≥90 {GE90}; RAW {RAW_B} → {RAW_A}; {MOVED}. cs exact {CS_B} → {CS_A} (+103) / EXTRA
  {EX_B} → {EX_A} / missing {MI_B} → {MI_A} — {CSDEC}. clean 2056/2102 → 2087/2110 (98.91%); leak 288/46 → 26/23; body 191; tags 9557/9557; flipCard
  divergence 0; every widget verifier over the 23 defect 0 (accordion 32 panels / 9 modules; clickDrop 41 items incl. the new OS builds);
  13 selftests GREEN. The fast-loop's `--accept-named` for ≥75 / EXTRA / missing (the r289 override, every mover decomposed —
  `_r341_sk_movers.log`, `_r341_cs_decomp.log`). Fast-loop baseline re-snapshotted from the fresh corpus (values = the gate suite's), manifest
  snapshot (2110 pages / 413 modules), `_ship_ledger.py record-full --round 341` (counter 0), feature index rebuilt (8 shards + merge,
  selftest GREEN). **{PCT}% of achievable.**
- **Verifier:** {VER}.
- **Named:** the plain-BLACK tag class (≈ 300 brackets — the 26 residual leaks are mostly it; a content-vs-tag ambiguity, its own PICK if it
  clears 20 pages); the link-BLUE `[audio N]` class (250, BLL, hyperlinked tags); the bilingual-cell `[Item N] [Image]` leaks (r167 class);
  AGH1006's widget-release `[H3]`; HIS1005_2_0 (the writer's `[Interactive]` instruction now opens the hand-off box the tag asks for; gold =
  image + caption, A1) and TRR109_5_0 (the writer's `[Checklist]` → a widget box; gold hand-built a drag-and-drop, decision 5); ARFUN05_0_0
  (its two `[Insert video]` lines now embed the gold's own videos; the r322-named single page's alignment artefact). Ship ledger: FULL —
  counter 0. **Plateau window restarts (Chris's session-9 "continue" after the exhaustion stop): r341 +0.021.**

""")
ANCHOR = "## Session 9 · Round 1 PICK (engine r341)"
if "## Session 9 · Round 1 (engine r341) — what shipped" not in s:
    assert s.count(ANCHOR) == 1; s = s.replace(ANCHOR, SEC + ANCHOR, 1); print("LOOP_STATE section")
OLD_P = "- Remaining KB queue (§D):"
NEW_P = (f"- Session 9 Round 1 (engine r341 — a writer's tag typed in a NON-STANDARD RED is still a tag: the near-red run rule + the r299 weave's parenthesised-tail form; the loop's first fresh PICK after the session-8 exhaustion stop — the literal-tag-leak PROTECTED GATE had never had a PICK): **SHIPPED 2026-09-16 ≈10:40 (session 9)**. AppVersion 260619.12, CLAUDE.md §9/§11/§14, KB status D-row, CONVERTER_V2_GUIDE A4, **FULL regeneration (the backstop; ledger 0)**. Skeleton {DELTA}pp, ≥50 +7, ≥75 −1 named, cs exact +103, clean 97.81 → 98.91%, leak 288/46 → 26/23; HIS1005 ships the gold's exact 15-page set." + nl)
if "- Session 9 Round 1 (engine r341" not in s:
    assert s.count(OLD_P) == 1, "position"; s = s.replace(OLD_P, NEW_P + OLD_P, 1); print("position")
OLD_R = "- s8-pick2 (no engine round)"
i = s.find(OLD_R); assert i > 0, "round log anchor"; j = s.find(nl, i) + len(nl)
NEW_R = (f"- s9-r1 (engine r341) · a writer's tag typed in a NON-STANDARD RED is still a tag (the engine scanned only `ff0000` / `ee0000` runs for tags; the HIS writer's `ed0000`, ENGFUN02's `fa0000` and Word's Dark Red `c00000` shipped every tag as literal text — 598 brackets on 30 modules; a run in the red hue band now counts as red when it carries a bracket or continues an open one, never on bare content; + the r299 weave's parenthesised-tail definition form) · SHIPPED 2026-09-16 · FULL regeneration (the backstop, ledger 0), 76 pages changed + 10 added − 2 removed / 23 modules · scaffold {SK_B}→{SK_A} ({DELTA}; {SK_B4}→{SK_A4}; pairs {PAIRS_B}→{PAIRS_A}; 39 moved — 20 up / 19 down, pp-sum +70.06, every mover in the affected set; per module HIS1005 +9.24 (the gold's exact 15-page set), ENGFUN02 +15.05; the dips NAMED: the OS* clickDrop BUILDS replacing coincidentally-matching dumps (RAW up), HIS1006's renumbering, HIS1005_2_0 / TRR109_5_0 A1 substitutions, ARFUN05 alignment), ≥50 {GE50_B}→{GE50_A} (+7), ≥75 {GE75_B}→{GE75_A} (−1 NAMED OSGM501_5_0), ≥90 {GE90}, cs exact +103 (EXTRA +4 / missing +15 = HIS1005's +133 matched pool, named), clean 97.81→98.91%, **leak 288/46→26/23**, every other gate EXACT · {PCT}% of achievable · commit (see git log) · **plateau window restarts: r341 +0.021**" + nl)
if "- s9-r1 (engine r341" not in s:
    s = s[:j] + NEW_R + s[j:]; print("round log")
wr(LS, s); print("LOOP_STATE.md written")
