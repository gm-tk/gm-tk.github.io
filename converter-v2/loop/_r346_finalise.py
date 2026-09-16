#!/usr/bin/env python3
"""ROUND 346 (loop session 12 Round 3 — Chris's D10-7) — finalise: changelog, AppVersion (260619.16 → 260619.17), CLAUDE.md
§9/§11/§14, CONVERTER_V2_GUIDE B5, gate_baseline.json, KB status row, LOOP_STATE.md. Idempotent; LF kept; never json.dumps a data file."""
import io, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)

SK_B, SK_A, SK_B4, SK_A4, RAW_B, RAW_A = "51.281", "51.282", "51.2809", "51.2820", "35.407", "35.395"
GE50_B, GE50_A, GE75, GE90, PAIRS = 1073, 1074, 198, 15, 1955
CS_B, CS_A, EX, MI, POOL_B, POOL_A = 11461, 11464, 175, 607, 13508, 13513
ELEVEN = "MXDB202 MXDB301 MXDI102 MXDI201 MXDI301 MXEX301 MXFU302 MXFU401 PES1007 PES1008 SCCH301"
MOVERS = ("20 moved — 7 up / 13 down, every mover in the affected set, pp-sum +2.17 scaffold / −22.72 RAW; the gains: PES1008_3_0 +19.58 (20.61 → 40.19), MXEX301_2_0 +4.41 (46.93 → 51.34, crosses ≥50), PES1007_2_0 +4.39 (its four equations are the gold's own, text-identical), MXEX301_4_0 +1.47 …; the 13 dips are NAMED and of two kinds (`_r346_dips.log`): (a) the gold ships NO `<math>` for the writer's equations on the paired page — the human typed or drew them: MXFU302_9_0 −3.72 (13 equations, gold 0), MXFU302_6_0 −0.55 (2 / 0), MXDI201_8_0 −3.32 (6 / 0), SCCH301_7_0 −1.64 (1 / 0), MXDB301_3_0 −0.94 (2 / 0), MXDB202_3_0 −0.77 (1 / 0) — the A1 substitution D10-7 overrides (MathML is the shipped form); (b) the gold carries far FEWER equations than the writer wrote (the human's editorial reduction): MXDI301_1_0 −7.31 (68 ours / gold 32 — its RAW RISES +5.07), MXDI301_5_0 −2.01, MXDI102_4_0 −1.55 (72 / 4), MXDI102_3_0 −1.58 (34 / 4), MXDI102_2_0 −0.72 (36 / 7), PES1007_3_0 −3.92 (11 / 22 — every one of ours is in the gold's set, the gold's `display=\"inline\"` form beside our bare one), PES1007_8_0 −0.90")

CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)" + chr(10) + chr(10)
ENTRY = f"""## 2026-09-16 (round 346, build 260619.17) — WORD EQUATIONS SHIP AS MATHML (Chris's decision D10-7, Option A: "MathML (the gold's form, the one that renders in MTK)"; KB delta — 05A "MathJax / Equations" → MathML is the shipped form; the autonomous loop's session-12 Round 3; SCOPED regeneration of the 11 equation modules with a Claude dir / 22 pages — scoped ship #3 since the r342 full; a NEW protected verifier `_verify_math.cjs`; every gate held-or-improved, the skeleton dips named)

### 1. WHAT CHANGED, IN ONE LINE

**A Word equation — an `<m:oMath>` sitting BESIDE the runs of a paragraph, which the run walk never saw, so every equation silently vanished from the page — now ships as `<math xmlns="http://www.w3.org/1998/Math/MathML">…</math>` at its exact position in the paragraph, and every page that carries one gains the `mathJax` body class.** 329 equations across 12 Writers Templates (MXDI102 154, MXDI301 69, PES1008 24, MXEX301 18, PES1007 17, MXFU302 15, MXFU401 12, CEDK401 6 — no Claude dir, MXDB301 6, MXDI201 6, MXDB202 1, SCCH301 1); MXDI301's "An exponent form of ⟨1/10⟩ × ⟨1/10⟩ = 0.1" is the example — the page said "An exponent form of" and stopped.

### 2. THE MEASUREMENT (`outputs/_measure_r346_omml.py`, every gold dir's docx + every gold and Claude page)

- Every one of the 329 is an INLINE `<m:oMath>` beside runs — there is not one `<m:oMathPara>` in the corpus; the vocabulary is `m:r`/`m:t` 736, `m:f` (fractions) 264, `m:sSup` 70, `m:sSub` 10, `m:d` 5, `m:rad` 1 — exactly the V1.5 converter's measured coverage. The gold ships 2,052 `<math>` on 94 pages: **bare 1,873 / inline 105 / block 70 / inline-block 4** → the shipped form is BARE (the 91% majority; MathJax renders it either way), inline at the writer's position. The gold's `mathJax` body class sits on the pages that carry a `<math>` (0.92 precision; 15 further gold pages carry the class with no `<math>` — not derivable, recorded).
- The gold has six times the writer's equations — MXFL302 alone 874 hand-typed on 15 pages, MXEO301 147, MXFU301 160 … — none with an OMML source: non-derivable (C), never chased.

### 3. THE SEAM (data `Input_Doc_Rules.math` {{enabled, env, body_class_token}}; env `MATHML_OFF`)

- `DocxExtractor.js` gains **`OmmlMathml`** — the V1.5 `pageforge-site/js/omml-to-mathml.js` converter ported with its logic intact (fractions, delimiters, sub/superscripts, radicals, n-ary, accents, matrices; the run tokeniser: one letter → `<mi>`, a word → `<mtext>`, digits → `<mn>`, the rest `<mo>`; an unknown element recursed as `<mrow>` and counted, never dropped) over a plain-object XML tree (`OmmlMathml.Tree` — the V1.5 class only touches childNodes / nodeType / localName / textContent / getAttribute, so V2's regex extractor needs no DOM). In `#parseParagraph`, before the run walk, each `<m:oMath>` is converted, stored in a process-wide registry (`DocxExtractor.MathRegister`) and replaced in place by a synthetic black run `<w:r><w:t>U+E010 id U+E011</w:t></w:r>` — the equation keeps its exact position and the sentinel (a private-use pair like the r75 hover sentinels) flows through tag classification, coalescing, the emoji strip, the typed-number list and every renderer unchanged.
- `PageAssembler`: the LAST post-pass (after OmitPlaceholderResidue / Tidy / EmojiStrip / TypedNumberList / LinkTextDisplay, before the formatter) swaps every sentinel for its markup (`DocxExtractor.MathReplace`) and, when the page now carries a `<math>`, adds `mathJax` to the `<body>` class; the hand-off `.txt` gets the same swap.
- **The paragraph structure is the writer's:** MXDI301's "An exponent form of ⟨eq⟩ × ⟨eq⟩ = 0.1 is" arrives as FOUR `w:p`s in the docx (the gold's one `<p>` is the human's editorial rejoin) and ships as four `<p>`s — faithful, recorded, not chased.

### 4. THE VERIFIER — `reference/tests/_verify_math.cjs`, a NEW protected gate (in `run_all_gates.sh`, `--selftest` GREEN: LIVENESS MXDI301 69, DETECTION an injected missing `<math>` 0 → 2)

- Per module: the docx `<m:oMath>` count == the built pages' `<math>` count; every `<math>` page carries `mathJax`; no sentinel leaks into a page or the `.txt`; every `<math>` well-formed (namespace + balanced tags). **322 of 323 equations ship; defect 1 = PES1007, a PRE-EXISTING content loss, not this round's:** lesson 2's page ends after the soccer-ball worked example — the writer's `[IMAGE: image23.png] [to right of question above]` line (the placement instruction resolves to the quiz `question` SUBTAG, how "embedded") and everything after it to `[End page]` (three paragraphs, `[H2] KINETIC ENERGY DEPENDS ON …`, `[H2] Key points` with its equation) is absent from the page AND the manifest, identical with the toggle OFF — a capture / boundary class for its own round (the r302 `scope_tags` family). Named in the gate's baseline.

### 5. THE PROOF

- In-memory probe over ALL 416 (`_r346_probe.cjs`, 4 shards): **OFF = disk 2110/2110; ON = 22 pages / 11 modules** ({ELEVEN}; CEDK401 has no Claude dir — the r285 ghost-dir class, not regenerated), every other page byte-identical. SCOPED regeneration of the 11 (3 batches rc 0); `_content_manifest.py fresh` 0 truly stale; `diff` = exactly the 22, 0 added / removed.
- **Skeleton (PRIMARY): SCAFFOLD mean {SK_B}% → {SK_A}% (+0.001pp; {SK_B4} → {SK_A4}) / ≥50% {GE50_B} → {GE50_A} (+1, MXEX301_2_0) / ≥75% {GE75} / ≥90% {GE90} EXACT / skipped 0 @ {PAIRS}; RAW {RAW_B}% → {RAW_A}%** (state `outputs/_r346_sk_final.json`, FRESH; `_r346_sk_movers.log`). {MOVERS}. The RAW dip is the same class seen whole: MathML subtrees now stand where the gold's page has plain text — content that was ABSENT is present.
- compare_structure exact **{CS_B} → {CS_A} (+3)** / EXTRA **{EX}** / missing **{MI}** EXACT (the text-matched pool {POOL_B} → {POOL_A}); body 180, clean 2080/2103 = 98.91%, leak 26/23, tags 9557/9557, flipCard / speechBubble / modal / mtkQuiz identical; fast-loop PASS + committed; ledger scoped #3 since the r342 full (5 of headroom); feature index rebuilt (GREEN); 14 selftests GREEN (`_r346_selftests.log`).

### 6. RECORDED

- The PES1007 lesson-2 page-tail loss (above). The gold's hand-typed equations (no OMML source). The 15 gold `mathJax` pages without a `<math>`. The writer's own equation-per-paragraph fragmentation. The `display="block"` / `"inline"` minority forms (the gold's 8.5%).
- KB delta for a KB session: 05A "MathJax / Equations" (lines 217–223) → MathML is the shipped form (Chris's V1.5 finding of 2026-08-26: MathML renders in MTK, LaTeX does not).

**Ledger:** SCOPED ship #3 since the r342 full (5 of headroom) · data `Input_Doc_Rules.math` · env `MATHML_OFF` · engine `DocxExtractor.js` (+ `OmmlMathml`, the registry, the paragraph hook), `PageAssembler.js` · gate tools (outside git, mirrored) `reference/tests/_verify_math.cjs` + `run_all_gates.sh` + `_selftest_core.cjs` · tools `outputs/_measure_r346_omml.py` (+ `_r346_omml.{{json,log}}`), `_r346_splice.py`, `_r346_probe.cjs` + `_r346_probe_{{off,on}}_0*.log`, `_r346_changed_pages.txt`, `_affected_r346.txt`, `_r346_regen.log`, `_r346_gates.log`, `_r346_sk_final.json` / `_r346_sk_full.log`, `_r346_sk_movers.log`, `_r346_dips.py` (+ `.log`), `_r346_fastloop_commit.log`, `_r346_selftests.log`, `_r346_feature_index.log`, `_r346_finalise.py` · AppVersion 260619.17.

"""
if "round 346, build 260619.17" not in s:
    assert s.startswith(head); s = head + ENTRY + s[len(head):]; wr(CL, s); print("changelog prepended")

CF = os.path.join(PF, "app", "js", "Config.js"); c = rd(CF)
OLD = '\tstatic AppVersion = "260619.16";' + chr(10)
NEW = ('\t// ROUND 346 (2026-09-16, build 260619.17): Word equations ship as MathML (Chris\'s D10-7) — the V1.5 OMML converter' + chr(10) +
       '\t// ported into DocxExtractor (OmmlMathml), each <m:oMath> a sentinel run swapped for its <math> in the final' + chr(10) +
       '\t// post-pass + the mathJax body class; a new protected verifier _verify_math.cjs; scoped regeneration of 11 modules.' + chr(10) +
       '\tstatic AppVersion = "260619.17";' + chr(10))
if '"260619.17"' not in c:
    assert c.count(OLD) == 1; c = c.replace(OLD, NEW, 1); wr(CF, c); print("AppVersion bumped")

CM = os.path.join(PF, "CLAUDE.md"); m = rd(CM)
OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 345 BASELINE = r344, page-for-page"
NEW9 = (f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 346 BASELINE (Word equations ship as MathML — Chris's D10-7; SCOPED regeneration of 11 modules / 22 pages, scoped ship #3 since the r342 full; the NEW protected verifier `_verify_math.cjs` — 322 of 323 equations, the 1 = PES1007's pre-existing page-tail loss, named): SCAFFOLD mean {SK_A}% / >=50% {GE50_A} / >=75% {GE75} / >=90% {GE90} / skipped 0 @ {PAIRS}; RAW {RAW_A}%** (state `outputs/_r346_sk_final.json`, FRESH). r346 +0.001 ({SK_B4} → {SK_A4}; {MOVERS}); compare_structure exact {CS_B} → {CS_A} (+3) / EXTRA {EX} / missing {MI} EXACT; clean 2080/2103 / leak 26/23 / body 180 EXACT. Older r345 text: **ROUND 345 BASELINE = r344, page-for-page")
if "ROUND 346 BASELINE" not in m:
    assert m.count(OLD9) == 1, "§9"; m = m.replace(OLD9, NEW9, 1); print("§9")
OLDV = "Adjunct verifiers (run when you touch a widget): `_verify_speechbubble.cjs`, `_verify_accordion.cjs`,"
NEWV = "Adjunct verifiers (run when you touch a widget): `_verify_math.cjs` (round 346 — a PROTECTED gate in `run_all_gates.sh`: docx `m:oMath` count == page `<math>` count, `mathJax` on every math page, no sentinel leak), `_verify_speechbubble.cjs`, `_verify_accordion.cjs`,"
if "`_verify_math.cjs` (round 346" not in m:
    assert m.count(OLDV) == 1, "§9 adjunct"; m = m.replace(OLDV, NEWV, 1); print("§9 adjunct")
A11 = "| `ENGFIRST_OFF` | 345 |"
R11 = ("| `MATHML_OFF` | 346 | **WORD EQUATIONS SHIP AS MATHML** (Chris's D10-7, Option A; KB delta 05A → MathML; the autonomous loop's session-12 Round 3; **SCOPED regeneration of the 11 equation modules with a Claude dir / 22 pages; scoped ship #3 since the r342 full**). Reverts byte-for-byte (OFF in memory = disk 2110/2110 — the equations vanish again). ON (default), `Input_Doc_Rules.math` `{ enabled, env, body_class_token \"mathJax\" }`: `DocxExtractor.#parseParagraph` converts each `<m:oMath>` beside a paragraph's runs through `OmmlMathml` (the V1.5 `omml-to-mathml.js` port over a plain-object XML tree — fractions / delimiters / sub- and superscripts / radicals / n-ary / accents / matrices; one letter → `<mi>`, a word → `<mtext>`, digits → `<mn>`, else `<mo>`; unknown elements recursed as `<mrow>`, never dropped), stores it in a process-wide registry and replaces it in place by a synthetic black run carrying the sentinel U+E010 id U+E011; PageAssembler's LAST post-pass swaps the sentinel for the bare `<math xmlns=…>` (the gold's 91% form) and adds `mathJax` to the body class of a page that carries one; the `.txt` gets the same swap. MEASURED (`outputs/_measure_r346_omml.py`): 329 equations / 12 WTs, all inline beside runs, vocabulary r/t, f, sSup, sSub, d, rad; gold 2,052 `<math>` (bare 1,873). Verifier `_verify_math.cjs` 322/323 (the 1 = PES1007 lesson 2's pre-existing page-tail loss after `[IMAGE: image23.png] [to right of question above]`, named). Skeleton +0.001pp / ≥50 +1 / cs exact +3; the 13 dips named — the gold ships NO `<math>` for the writer's equations (MXFU302_9_0 13 / 0, MXDI201_8_0 6 / 0 …) or far fewer (MXDI301_1_0 68 / 32, MXDI102 pages 34–72 / 4–7) — the human's substitution D10-7 overrides. |\n")
if "| `MATHML_OFF` | 346 |" not in m:
    assert m.count(A11) == 1, "§11"; m = m.replace(A11, R11 + A11, 1); print("§11")
B14 = (f"- **Build:** `260619.17` (round 346 — **Word equations ship as MathML** (Chris's D10-7, Option A: the V1.5 OMML converter ported into `DocxExtractor` as `OmmlMathml`; each `<m:oMath>` beside a paragraph's runs becomes a sentinel run swapped for its bare `<math xmlns=…>` in PageAssembler's last post-pass; the page gains `mathJax`; the `.txt` too; a NEW protected verifier `_verify_math.cjs` in `run_all_gates.sh` — docx count == page count, mathJax on every math page, no leak — selftest GREEN; the autonomous loop's session-12 Round 3; **SCOPED regeneration of 11 modules / 22 pages; scoped ship #3 since the r342 full**). **ROUND 346 BASELINE: SCAFFOLD mean {SK_A}% / ≥50% {GE50_A} / ≥75% {GE75} / ≥90% {GE90} / skipped 0 @ {PAIRS}; RAW {RAW_A}%** (state `outputs/_r346_sk_final.json`, FRESH) = **55.8% of achievable** (ceiling 91.9%). +0.001pp ({SK_B4} → {SK_A4}; 20 moved — 7 up / 13 down, ≥50 +1 MXEX301_2_0; the 13 dips NAMED — see §9: the gold ships no or far fewer `<math>` than the writer wrote, the human's substitution D10-7 overrides). cs exact **{CS_A}** (+3) / EXTRA **{EX}** / missing **{MI}**; clean **2080/2103** / leak **26/23**; body **180**; math verifier **322/323** (the 1 = PES1007's pre-existing page-tail loss, named); 14 selftests GREEN. Corpus 2110 pages / 416 modules, 0 truly stale, **22 pages / 11 modules changed, 0 added/removed**; toggle `MATHML_OFF`; data `Input_Doc_Rules.math`. **Plateau window (both §4 conditions): r346 moved ≥50 +1 and cs exact +3 — the window restarts (0 of 3).**\n")
if "- **Build:** `260619.17` (round 346" not in m:
    A = "- **Build:** `260619.16` (round 345 —"; assert m.count(A) == 1, "§14"; m = m.replace(A, B14 + A, 1); print("§14")
wr(CM, m)

GD = os.path.join(HERE, "..", "..", "pageforge-site", "CONVERTER_V2_GUIDE.md"); g = rd(GD)
AG = "- `Extract(zip)` — the entry point (top of file): reads `document.xml` and its companions, drives the parse, returns `{blocks, rels, mtkFlag, hasContentStart, metadata}`."
NG = AG + "\n- **Equations (round 346).** A Word equation is not a run: it is an `<m:oMath>` element sitting beside the runs of a paragraph, and until round 346 the run walk never saw it — every equation silently vanished. `OmmlMathml` (top of this file, the V1.5 `js/omml-to-mathml.js` converter ported over a plain-object XML tree) turns each one into `<math xmlns=\"http://www.w3.org/1998/Math/MathML\">…</math>`; `#parseParagraph` stores the markup in `DocxExtractor.MathRegister` and drops a synthetic black run carrying a private-use sentinel (U+E010 id U+E011) in its place, so the equation keeps its position through every text rule; `PageAssembler`'s last post-pass (`DocxExtractor.MathReplace`) swaps the sentinel for the markup and adds the `mathJax` body class. Data `Input_Doc_Rules.math`; env `MATHML_OFF`; verifier `_verify_math.cjs`."
if "Equations (round 346)" not in g:
    assert g.count(AG) == 1, "guide"; g = g.replace(AG, NG, 1); wr(GD, g); print("guide")

GB = os.path.join(HERE, "..", "reference", "tests", "gate_baseline.json"); raw = rd(GB); d = json.loads(raw)
d["_meta"]["build"] = "260619.17"; d["_meta"]["round"] = 346; d["_meta"]["date"] = "2026-09-16"
d["skeleton"].update({"mean_scaffold_pct": float(SK_A), "raw_mean_pct": float(RAW_A), "pages_ge_50": GE50_A, "pages_ge_75": GE75, "pages_ge_90": GE90})
if "compare_structure" in d and isinstance(d["compare_structure"], dict) and "exact_chain" in d["compare_structure"]: d["compare_structure"]["exact_chain"] = CS_A
d["math"] = {"equations": 323, "math": 322, "defect": 1, "_note": "Round 346 — _verify_math.cjs over the 11 equation modules with a Claude dir: 322 of 323; the 1 = PES1007 lesson 2's PRE-EXISTING page-tail loss after `[IMAGE: image23.png] [to right of question above]` (the `question` SUBTAG), identical with MATHML_OFF — a capture/boundary class for its own round. Hold-or-improve: defect must not rise above 1; 0 once that class ships."}
d["_meta"]["_round346_note"] = (f"Round 346 (D10-7: Word equations → MathML; scoped 11 modules / 22 pages). skeleton {SK_B4}->{SK_A4} (+0.001pp; 20 moved, 13 named dips = the gold ships no/fewer <math> than the writer wrote); >=50 {GE50_B}->{GE50_A}; cs exact {CS_B}->{CS_A}; EXTRA {EX} / missing {MI} / clean 2080/2103 / body 180 / leak 26/23 EXACT.")
wr(GB, json.dumps(d, ensure_ascii=False) + (chr(10) if raw.endswith(chr(10)) else "")); print("gate_baseline.json refreshed")

KB = os.path.join(HERE, "..", "..", "KB_AMALGAMATION_STATUS.md"); k = rd(KB)
OK = "+ `body.mathJax` | **AUTHORISED — Chris D10-7 (2026-09-16), queued item 4**;"
NK = "+ `body.mathJax` | **SHIPPED round 346 (2026-09-16)** — `OmmlMathml` (the V1.5 port) in `DocxExtractor`, sentinel runs swapped in PageAssembler's last post-pass, `mathJax` on every math page, the new protected verifier `_verify_math.cjs` 322/323 (the 1 = PES1007's pre-existing page-tail loss, named); 22 pages / 11 modules; skeleton +0.001pp, ≥50 +1, cs exact +3, the 13 dips named (the gold ships no / fewer `<math>` than the writer wrote — the human's substitution D10-7 overrides). Was: **AUTHORISED — Chris D10-7 (2026-09-16), queued item 4**;"
if "SHIPPED round 346" not in k:
    assert k.count(OK) == 1, "kb d10-7 row"; k = k.replace(OK, NK, 1); wr(KB, k); print("KB status row")

LS = os.path.join(HERE, "..", "..", "LOOP_STATE.md"); s = rd(LS); nl = chr(13) + chr(10) if chr(13) + chr(10) in s[:3000] else chr(10)
def L(t): return t.replace(chr(10), nl)
SEC = L(f"""## Session 12 · Round 3 (engine r346 — D10-7) — what shipped (Word equations ship as MathML)
- **Fix:** `Input_Doc_Rules.math` {{enabled, env MATHML_OFF, body_class_token "mathJax"}}; `DocxExtractor.js` gains `OmmlMathml` (the V1.5
  `pageforge-site/js/omml-to-mathml.js` converter ported with its logic intact over a plain-object XML tree — `OmmlMathml.Tree`) + a process-wide
  registry (`MathRegister` / `MathReplace` / `MathSentinel`) + the `#parseParagraph` hook (each `<m:oMath>` beside the runs → a synthetic black run
  carrying the sentinel U+E010 id U+E011, in place); `PageAssembler`'s LAST post-pass swaps the sentinels for the bare `<math xmlns=…>` (the gold's
  91% form) and adds `mathJax` to the body class of a page carrying one; the `.txt` gets the same swap. Splice `outputs/_r346_splice.py`.
- **Measured first** (`_measure_r346_omml.py`): 329 equations / 12 WTs — ALL inline `<m:oMath>` beside runs (no `oMathPara` in the corpus), vocabulary
  r/t · f · sSup · sSub · d · rad (= V1.5's coverage); gold 2,052 `<math>` on 94 pages, bare 1,873 / inline 105 / block 70; the gold's hand-typed
  equations (MXFL302 874 …) have no OMML source (C). CEDK401 has no Claude dir.
- **New protected verifier `reference/tests/_verify_math.cjs`** (in `run_all_gates.sh`; `_selftest_core.cjs` spec; `--selftest` GREEN — LIVENESS
  MXDI301 69, DETECTION an injected missing `<math>` 0 → 2): docx `m:oMath` count == page `<math>` count, `mathJax` on every math page, no sentinel
  leak, well-formed. **322 of 323 — the 1 = PES1007 lesson 2's PRE-EXISTING page-tail loss** (after `[IMAGE: image23.png] [to right of question
  above]` — the placement instruction resolves to the quiz `question` SUBTAG, how embedded — three paragraphs + two `[H2]` sections + the Key-points
  equation are absent from page AND manifest, identical with the toggle OFF; a capture / boundary class for its own round, the r302 `scope_tags` family).
- **Regeneration:** SCOPED — probe over ALL 416: OFF = disk 2110/2110, ON = 22 pages / 11 modules ({ELEVEN}); 3 batches rc 0; `fresh` 0 truly stale;
  `diff` = exactly the 22, 0 added / removed.
- **Gates:** skeleton **{SK_B} → {SK_A} (+0.001pp; {SK_B4} → {SK_A4})**; ≥50 {GE50_B} → {GE50_A} (+1, MXEX301_2_0 46.93 → 51.34); ≥75 {GE75} / ≥90 {GE90} EXACT; RAW {RAW_B} → {RAW_A};
  {MOVERS}. cs exact {CS_B} → {CS_A} (+3; pool {POOL_B} → {POOL_A}) / EXTRA {EX} / missing {MI} EXACT; body 180; clean 98.91% / leak 26/23; every verifier
  identical; fast-loop PASS + committed; ledger scoped #3 since the r342 full (5 of headroom); feature index GREEN; 14 selftests GREEN. 55.8% of achievable.
- **Recorded:** the PES1007 page-tail loss (own round); the gold's hand-typed equations; the 15 gold `mathJax`-without-math pages; the writer's
  equation-per-paragraph fragmentation (MXDI301 — the gold's single `<p>` is the human's rejoin); the KB delta 05A → MathML (a KB session).
- **Plateau window (both §4 conditions):** r346 moved ≥50 +1 and cs exact +3 → the window restarts at 0 of 3.

""")
ANCHOR = "## Session 12 · Round 2 (engine r345 — D10-2) — what shipped"
if "## Session 12 · Round 3 (engine r346 — D10-7) — what shipped" not in s:
    assert s.count(ANCHOR) == 1, "state anchor"; s = s.replace(ANCHOR, SEC + ANCHOR, 1); print("LOOP_STATE section")
OLD_P = "- Remaining KB queue (§D):"
NEW_P = (f"- Session 12 Round 3 (engine r346 — Chris's D10-7: Word equations ship as MathML — `OmmlMathml` in `DocxExtractor`, sentinel runs swapped in PageAssembler's last post-pass, `mathJax` on every math page; a NEW protected verifier `_verify_math.cjs`): **SHIPPED 2026-09-16 ≈20:35 (session 12)**. AppVersion 260619.17, CLAUDE.md §9/§11/§14, CONVERTER_V2_GUIDE B5, KB status D10-7 row SHIPPED, `run_all_gates.sh` + `_selftest_core.cjs` + `_MIGRATION/CHECKSUMS__gates.txt` refreshed, **SCOPED regeneration of 11 modules / 22 pages (scoped ship #3 since the r342 full)**. Skeleton +0.001pp, ≥50 +1, cs exact +3 (13 dips named); verifier 322/323 (the 1 = PES1007's pre-existing page-tail loss, named).\n")
if "- Session 12 Round 3 (engine r346" not in s:
    assert s.count(OLD_P) == 1, "position"; s = s.replace(OLD_P, L(NEW_P) + OLD_P, 1); print("position")
OLD_R = "- s12-r2 (engine r345, D10-2)"
i = s.find(OLD_R); assert i > 0, "round log anchor"; j = s.find(nl, i) + len(nl)
NEW_R = (f"- s12-r3 (engine r346, D10-7) · Word equations ship as MathML (the V1.5 OMML converter ported into DocxExtractor as `OmmlMathml`; each `<m:oMath>` a sentinel run swapped for its bare `<math xmlns=…>` in PageAssembler's last post-pass; `mathJax` on every math page; the `.txt` too; NEW protected verifier `_verify_math.cjs`, selftest GREEN) · SHIPPED 2026-09-16 ≈20:35 · SCOPED regeneration 11 modules / 22 pages ({ELEVEN}), 0 added/removed (scoped #3 since the r342 full) · scaffold {SK_B}→{SK_A} (+0.001; {SK_B4}→{SK_A4}; 20 moved — 7 up / 13 down, every mover in the affected set; the dips NAMED = the gold ships NO `<math>` for the writer's equations (MXFU302_9_0 13 / 0, MXDI201_8_0 6 / 0, SCCH301_7_0, MXDB301, MXDB202) or far fewer (MXDI301_1_0 68 / 32, MXDI102 pages 34–72 / 4–7) — the human's substitution D10-7 overrides), ≥50 {GE50_B}→{GE50_A} (MXEX301_2_0), ≥75 {GE75} / ≥90 {GE90} EXACT, cs exact {CS_B}→{CS_A} / EXTRA {EX} / missing {MI}, body 180, clean 98.91% / leak 26/23, every other gate EXACT · verifier 322/323 (the 1 = PES1007 lesson 2's PRE-EXISTING page-tail loss after `[to right of question above]`, named) · 55.8% of achievable · commit (see git log) · **plateau window (both §4 conditions): restarts, 0 of 3**\n")
if "- s12-r3 (engine r346, D10-7)" not in s:
    s = s[:j] + L(NEW_R) + s[j:]; print("round log")
wr(LS, s); print("LOOP_STATE.md written")
