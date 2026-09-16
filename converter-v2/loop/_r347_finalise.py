#!/usr/bin/env python3
"""ROUND 347 (loop session 12 Round 4 — Chris's D10-5) — finalise: changelog, AppVersion (260619.17 → 260619.18), CLAUDE.md
§9/§11/§14, CONVERTER_V2_GUIDE (TablesAndGrids "How to update"), gate_baseline.json, KB status row, LOOP_STATE.md.
Idempotent; LF kept; never json.dumps a data file (gate_baseline.json is a gate-tool file). Run under WSL from anywhere."""
import io, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    data = s.encode("utf-8")
    with io.open(p, "wb") as f: f.write(data)

SK_B, SK_A, SK_B4, SK_A4, RAW_B, RAW_A = "51.282", "51.283", "51.2820", "51.2832", "35.395", "35.409"
GE50, GE75, GE90, PAIRS = 1074, 198, 15, 1955
CS, EX, MI, POOL = 11464, 175, 607, 13513
MOVERS = ("52 moved — 28 up / 24 down, every mover inside the regenerated set, pp-sum +2.24 scaffold / +25.83 RAW; by template: Fundamentals +4.46 (3 up / 2 down — ENFUN04_0_0 +5.11, CHFUN04_0_0 +0.54 …), "
          "Inquiry −0.26 (2 / 2), **Standard −1.94 (23 up / 20 down) = the NAMED override on the tie** — the largest dips MXFU402_3_0 −8.37, MXEO202_3_0 −6.61, MXDI301_5_0 −1.47, AGH1008_7_0 −1.41 are Standard pages whose gold tables are plain `table`; "
          "the largest gains OSBY201_1_0 +5.56, ENFUN04_0_0 +5.11, ENGJ403_4_0 +3.23, XGF9003_1_4 +1.80 are pages whose gold tables are bordered")
LEX = ("the gold's two-column contrast-header tables are 13 in the whole corpus and split FOUR ways (plain `table` 4 / `table-bordered` 3 / bordered+`tableFixed` 5 / `tableFixed` 1), and the gold's "
       "two-column tables overall are plain `table` 229 vs any `tableFixed` 85 — no lexicon the corpus confirms")

CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)" + chr(10) + chr(10)
ENTRY = f"""## 2026-09-16 (round 347, build 260619.18) — EVERY CONTENT TABLE SHIPS THE KB 05D CLASS FORM `table table-bordered` (Chris's decision D10-5, Option A: "05D's table table-bordered everywhere (plus tableFixed for true two-column comparison tables)"; the tableFixed half measured and DECLINED — no lexicon the corpus confirms — and left as a data-ready hook shipped OFF; the autonomous loop's session-12 Round 4; FULL regeneration of all 416 gated dirs — the ledger's full-ship backstop, scoped counter reset to 0) + a CARRIED FIX to round 346 (Word's Unicode math-italic letters shipped as two U+FFFD each — now the plain letter the gold carries).

### 1. WHAT CHANGED, IN ONE LINE

**Every table the converter renders — free-body, inside an accordion / tabs panel, and the hand-off dumps — opens as `<div class="table-responsive"><table class="table table-bordered">` instead of bare `table`; the `th` header-row rule and the wrapper are unchanged; a KB session still owes 05D ↔ 06 §6 the reconciliation (06's `table noHover tableFixed` is superseded by D10-5).**

### 2. THE MEASUREMENT (`outputs/_measure_r347_tables.py --all`, every gold and Claude page, hand-off boxes stripped)

- The gold ships 1,819 tables: **`table-bordered` on 1,011 (0.56)** — Standard 735 / 1,435 = **0.51 (the tie)**, Inquiry 163 / 226 = 0.72, Fundamentals 94 / 136 = 0.69, Bilingual 19 / 22 = 0.86; `tableFixed` (any spelling) on 551 (0.30), 87 distinct class sets in all (`noHover`, `center-text`, `td-hover`, `mathTable`, `sassoon-text` … — the developers' per-page dressings, none derivable from the writer's docx).
- **The tableFixed half:** {LEX}. Per the PICK's own rule the tableFixed half is declined; the hook `elements.table.kb_class_form.comparison` {{enabled false, class, lexicon}} ships OFF, data-ready for a KB session that settles a lexicon.
- Claude before: 1,113 free-body tables on 226 modules, every one bare `table` (+ the glossary's own `search-table table table-fixed`); after: **1,113 `table table-bordered` / 1 glossary — every table's class set ∈ {{`table table-bordered`, the glossary's}}** (the verifier = the same tool's census, re-run after the ship).

### 3. THE SEAM (data `Emit_Templates.elements.table.kb_class_form` {{enabled, env, default_class, comparison}}; env `TBLBORDER_OFF`)

- `TablesAndGrids.contentTable`, right after the layout-table→grid attempt: when the flag is on the `<table class="table">` opener is swapped for `default_class` (`table table-bordered`); with `comparison.enabled` a table whose every row has exactly two cells AND whose header pair matches a lexicon pair (either order, folded, tags / `[tag]` markers / `*` stripped) would take `comparison.class` — shipped OFF. Splice `outputs/_r347_splice.py` (idempotent). No other emitter writes a `<table>` (the glossary's wrapper lives in its own widget template).
- **Carried fix (r346's own defect, found by this round's OFF probe):** the V1.5 OMML port walked a run's text by UTF-16 unit, so a Word math-italic letter (Mathematical Alphanumeric Symbols, U+1D400–U+1D7FF — 𝑥 U+1D465) shipped as `<mi>\\uD835</mi><mi>\\uDC65</mi>` = two `<mi>�</mi>` on disk (MXDB301_3_0 3 letters, MXFU401_2_0 14 — 34 replacement characters); the gold ships `<mi>x</mi>`. `OmmlMathml._foldMathAlpha` folds the block to its plain Latin / Greek letter / digit before the tokeniser and the `<mi>` loop walks by code point; `_verify_math.cjs` now counts a U+FFFD or a lone surrogate inside a `<math>` as malformed (selftest GREEN; 322 of 323 held, the 1 = PES1007's pre-existing page-tail loss).

### 4. THE PROOF

- In-memory probe over ALL 416 (`_r347_probe.cjs`, 4 shards): **OFF (`TBLBORDER_OFF`) = disk on 2,108 of 2,110 — the two exceptions are exactly the two math pages above, and their only diff is `<mi>�</mi><mi>�</mi>` → `<mi>x</mi>`**; ON = **1,225 pages / 373 modules** (`_r347_on_changed.txt`). FULL regeneration of all 416 gated dirs (`_r347_fullship_par.sh`, 36 batches × 4 workers, 19:58–20:03; batches 15 / 21 / 26 hit the oembed-cache write race and were re-run singly, rc 0); `_stalecheck.sh` 0 stale; `_content_manifest.py diff` = **exactly the 1,225 predicted pages / 373 modules, 0 added / removed** (the §0b whole-family proof: the probe's ON set and the regenerated set are the same set); no `<mi>�</mi>` remains; disk census 4,473 `<table class="table table-bordered">` + 1 glossary.
- **Skeleton (PRIMARY): SCAFFOLD mean {SK_B}% → {SK_A}% (+0.001pp; {SK_B4} → {SK_A4}) / ≥50% {GE50} / ≥75% {GE75} / ≥90% {GE90} EXACT / skipped 0 @ {PAIRS}; RAW {RAW_B}% → {RAW_A}% (+0.014pp)** (state `outputs/_r347_sk_final.json`, FRESH; movers `_r347_sk_movers.log`): {MOVERS}. **The net is the prediction: a named override in Standard (the 0.51 tie), a gain in the other templates, tiny net positive.**
- compare_structure exact **{CS}** / EXTRA **{EX}** / missing **{MI}** EXACT (pool {POOL}); body 180; clean 2080/2103 = 98.91%; leak 26/23; tags 9557/9557; flipCard / speechBubble (defect 4 = baseline) / modal / mtkQuiz / math (322/323 = baseline) identical; fast-loop baseline re-snapshotted (`_r347_fastloop_snapshot.log`); manifest snapshot 2110 / 413; `_ship_ledger.py record-full --round 347 --build 260619.18` (scoped counter 0, 8 of headroom); feature index `--rehtml` 678 + `--merge`, selftest GREEN; 14 selftests GREEN. **55.8% of achievable** (ceiling 91.9%).

### 5. RECORDED

- The tableFixed half (declined, hook OFF). The gold's 87 class dressings (`noHover`, `center-text`, `td-hover`, `mathTable` …) — non-derivable (C). The Standard tie's 20 named dips. KB delta for a KB session: 06 §6 (lines 405–411) `table noHover tableFixed` → reconcile to 05D per D10-5.

**Ledger:** FULL ship (round 347; counter reset) · data `Emit_Templates.elements.table.kb_class_form` · env `TBLBORDER_OFF` · engine `TablesAndGrids.js` (`contentTable`), `DocxExtractor.js` (`_foldMathAlpha`, the `<mi>` loop) · gate tools (outside git, mirrored to `loop/`) `_verify_math.cjs` · tools `outputs/_measure_r347_tables.py`, `_r347_splice.py`, `_r347_probe.cjs` (+ `_r347_probe_run.sh`), `_r347_fullship_par.sh`, `_r347_sk_movers.py`, `_r347_finalise.py`.

"""
if "round 347, build 260619.18" not in s:
    assert s.startswith(head); s = head + ENTRY + s[len(head):]; wr(CL, s); print("changelog prepended")

CF = os.path.join(PF, "app", "js", "Config.js"); c = rd(CF)
OLD = '\tstatic AppVersion = "260619.17";' + chr(10)
NEW = ('\t// ROUND 347 (2026-09-16, build 260619.18): every content table ships the KB 05D class form table table-bordered' + chr(10) +
       '\t// (Chris\'s D10-5; the tableFixed half measured and declined, a data-ready hook shipped OFF); FULL regeneration of all' + chr(10) +
       '\t// 416 gated dirs; carried fix — Word\'s math-italic letters (U+1D400 block) fold to the plain letter instead of two U+FFFD.' + chr(10) +
       '\tstatic AppVersion = "260619.18";' + chr(10))
if '"260619.18"' not in c:
    assert c.count(OLD) == 1; c = c.replace(OLD, NEW, 1); wr(CF, c); print("AppVersion bumped")

CM = os.path.join(PF, "CLAUDE.md"); m = rd(CM)
OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 346 BASELINE (Word equations ship as MathML — Chris's D10-7; SCOPED"
NEW9 = (f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 347 BASELINE (every content table ships the KB 05D class form `table table-bordered` — Chris's D10-5; the tableFixed half declined, hook OFF; FULL regeneration of all 416 gated dirs, the ledger's full-ship backstop, scoped counter 0; the r346 math-italic-letter fix carried): SCAFFOLD mean {SK_A}% / >=50% {GE50} / >=75% {GE75} / >=90% {GE90} / skipped 0 @ {PAIRS}; RAW {RAW_A}%** (state `outputs/_r347_sk_final.json`, FRESH). r347 +0.001 ({SK_B4} → {SK_A4}; {MOVERS}); compare_structure exact {CS} / EXTRA {EX} / missing {MI} EXACT; clean 2080/2103 / leak 26/23 / body 180 EXACT. Older r346 text: **ROUND 346 BASELINE (Word equations ship as MathML — Chris's D10-7; SCOPED")
if "ROUND 347 BASELINE" not in m:
    assert m.count(OLD9) == 1, "§9"; m = m.replace(OLD9, NEW9, 1); print("§9")
A11 = "| `MATHML_OFF` | 346 |"
R11 = (f"| `TBLBORDER_OFF` | 347 | **EVERY CONTENT TABLE SHIPS `table table-bordered`** (Chris's D10-5, Option A — KB 05D level 1 over the gold's Standard tie 0.51; the tableFixed half for two-column comparison tables measured and DECLINED — {LEX} — and shipped as a data-ready hook `elements.table.kb_class_form.comparison` OFF; the autonomous loop's session-12 Round 4; **FULL regeneration of all 416 gated dirs, the ledger's full-ship backstop**; a carried fix to r346: Word's math-italic letters fold to the plain letter instead of two U+FFFD, `_verify_math.cjs` now flags a U+FFFD / lone surrogate). Data `Emit_Templates.elements.table.kb_class_form` {{enabled, env, default_class, comparison}}; engine `TablesAndGrids.contentTable` (the opener swap), `DocxExtractor.OmmlMathml._foldMathAlpha`. Probe OFF = disk (2108/2110 + the two math pages' letter fix), ON = 1,225 pages / 373 modules = the regenerated set exactly. Skeleton {SK_B4} → {SK_A4} (+0.001pp; {MOVERS}); ≥50 / ≥75 / ≥90 / cs / clean / leak / body EXACT. | `TBLBORDER_OFF=1` restores the bare `table` class (the r346 output, byte-identical but for the two math pages). |" + chr(10))
if "| `TBLBORDER_OFF` | 347 |" not in m:
    assert m.count(A11) == 1, "§11"; m = m.replace(A11, R11 + A11, 1); print("§11")
B14 = (f"- **Build:** `260619.18` (round 347 — **every content table ships the KB 05D class form `table table-bordered`** (Chris's D10-5, Option A; the tableFixed half measured and declined — {LEX} — a data-ready hook shipped OFF; `TablesAndGrids.contentTable` swaps the opener behind `Emit_Templates.elements.table.kb_class_form`, env `TBLBORDER_OFF`; the autonomous loop's session-12 Round 4; **FULL regeneration of all 416 gated dirs — the ledger's full-ship backstop, scoped counter 0**; carried fix: Word's math-italic letters (U+1D400 block) fold to the plain letter — r346 had shipped 34 `<mi>�</mi>` on two pages). **ROUND 347 BASELINE: SCAFFOLD mean {SK_A}% / ≥50% {GE50} / ≥75% {GE75} / ≥90% {GE90} / skipped 0 @ {PAIRS}; RAW {RAW_A}%** (state `outputs/_r347_sk_final.json`, FRESH) = **55.8% of achievable** (ceiling 91.9%). +0.001pp ({SK_B4} → {SK_A4}; 52 moved — 28 up / 24 down; Standard −1.94 pp-sum = the NAMED override on the tie, Fundamentals +4.46, Inquiry −0.26). cs exact **{CS}** / EXTRA **{EX}** / missing **{MI}**; clean **2080/2103** / leak **26/23**; body **180**; math 322/323 — all EXACT.)" + chr(10))
if "- **Build:** `260619.18` (round 347" not in m:
    A = "- **Build:** `260619.17` (round 346 —"; assert m.count(A) == 1, "§14"; m = m.replace(A, B14 + A, 1); print("§14")
wr(CM, m)

GD = os.path.join(HERE, "..", "..", "pageforge-site", "CONVERTER_V2_GUIDE.md"); g = rd(GD)
AG = "**How to update.** Table markup → `Emit_Templates.json → elements.table`; the grid rule's gate → `body_region.layout_table_grid`. The decision point at the top of `contentTable`:"
NG = ("**How to update.** Table markup → `Emit_Templates.json → elements.table`; the grid rule's gate → `body_region.layout_table_grid`. **The class form (round 347, Chris's D10-5):** `elements.table.kb_class_form` — `default_class` (`table table-bordered`, the KB 05D default) replaces the opener's bare `table` for every kept table; `comparison` {enabled, class, lexicon} would give a two-column table with a contrast-lexicon header pair `table tableFixed` and ships OFF (the corpus confirms no lexicon); env `TBLBORDER_OFF` restores the bare class. The decision point at the top of `contentTable`:")
if "The class form (round 347" not in g:
    assert g.count(AG) == 1, "guide"; g = g.replace(AG, NG, 1); wr(GD, g); print("guide")

GB = os.path.join(HERE, "..", "reference", "tests", "gate_baseline.json"); raw = rd(GB); d = json.loads(raw)
d["_meta"]["build"] = "260619.18"; d["_meta"]["round"] = 347; d["_meta"]["date"] = "2026-09-16"
d["skeleton"].update({"mean_scaffold_pct": float(SK_A), "raw_mean_pct": float(RAW_A), "pages_ge_50": GE50, "pages_ge_75": GE75, "pages_ge_90": GE90})
if "compare_structure" in d and isinstance(d["compare_structure"], dict) and "exact_chain" in d["compare_structure"]: d["compare_structure"]["exact_chain"] = CS
d["_meta"]["_round347_note"] = (f"Round 347 (D10-5: every content table `table table-bordered`; FULL regeneration of all 416, ledger counter 0; r346's math-italic-letter fix carried). skeleton {SK_B4}->{SK_A4} (+0.001pp; 52 moved, Standard -1.94 pp-sum = the named override on the 0.51 tie, Fundamentals +4.46); >=50 {GE50} / >=75 {GE75} / >=90 {GE90} / cs {CS}/{EX}/{MI} / clean 2080/2103 / leak 26/23 / body 180 / math 322/323 all EXACT.")
wr(GB, json.dumps(d, ensure_ascii=False) + (chr(10) if raw.endswith(chr(10)) else "")); print("gate_baseline.json refreshed")

KB = os.path.join(HERE, "..", "..", "KB_AMALGAMATION_STATUS.md"); k = rd(KB)
OK = "superseded | **AUTHORISED — Chris D10-5 (2026-09-16), queued item 5**; 1,063 tables / 518 pages at r331 (re-measure) |"
NK = ("superseded | **SHIPPED round 347 (2026-09-16)** — `table table-bordered` on every kept table (1,113 free-body tables / 226 modules, + every in-widget and hand-off table; 4,473 on disk) behind `Emit_Templates.elements.table.kb_class_form`, env `TBLBORDER_OFF`; the tableFixed half DECLINED (the gold's 13 contrast-header tables split four ways; hook shipped OFF); FULL regeneration of all 416; skeleton +0.001pp (Standard −1.94 pp-sum = the named override on the tie, Fundamentals +4.46) |")
if "SHIPPED round 347" not in k:
    assert k.count(OK) == 1, "kb d10-5 row"; k = k.replace(OK, NK, 1); wr(KB, k); print("KB status row")

LS = os.path.join(HERE, "..", "..", "LOOP_STATE.md"); s = rd(LS); nl = chr(13) + chr(10) if chr(13) + chr(10) in s[:3000] else chr(10)
def L(t): return t.replace(chr(10), nl)
SEC = L(f"""## Session 12 · Round 4 (engine r347 — D10-5) — what shipped (every content table ships the KB 05D class form)
- **Fix:** `Emit_Templates.elements.table.kb_class_form` {{enabled, env TBLBORDER_OFF, default_class "table table-bordered", comparison {{enabled false,
  class "table tableFixed", lexicon}}}}; `TablesAndGrids.contentTable` swaps the `<table class="table">` opener for the class form right after the
  layout-table→grid attempt (free-body, in-widget panels and hand-off dumps alike — one rule, no exceptions); wrapper and `th` rule unchanged.
  Splice `outputs/_r347_splice.py` (idempotent).
- **Measured first** (`_measure_r347_tables.py --all`): gold 1,819 tables, `table-bordered` 1,011 = 0.56 (Standard 735/1,435 = 0.51 the tie; Inquiry 0.72;
  Fundamentals 0.69; Bilingual 0.86); 87 distinct class sets (the developers' dressings — C). **The tableFixed half DECLINED per the PICK's own rule:**
  {LEX}; the hook ships OFF, data-ready.
- **Carried fix (r346's own, found by this round's OFF probe):** Word's math-italic letters (U+1D400 block, e.g. 𝑥) were walked by UTF-16 unit →
  two `<mi>�</mi>` each (MXDB301_3_0 3 letters, MXFU401_2_0 14); `OmmlMathml._foldMathAlpha` folds the block to the plain letter (the gold's
  `<mi>x</mi>`), the `<mi>` loop walks by code point; `_verify_math.cjs` flags a U+FFFD / lone surrogate as malformed (selftest GREEN, 322/323 held).
  A lesson recorded in the tools: `_r347_splice.py`'s writer encodes BEFORE opening the target (an earlier draft's encode error truncated
  `DocxExtractor.js` to 0 bytes — rewritten from the HEAD blob with `git show`, no checkout, nothing lost).
- **Regeneration:** FULL — probe over ALL 416: OFF = disk 2108/2110 (+ the two math pages, letter fix only), ON = 1,225 pages / 373 modules; all 416
  gated dirs regenerated (36 batches × 4 workers 19:58–20:03; 15 / 21 / 26 re-run singly after the oembed-cache race, rc 0); `_stalecheck.sh` 0 stale;
  manifest `diff` = exactly the 1,225 / 373, 0 added / removed (the §0b whole-family proof); disk 4,473 bordered + 1 glossary, 0 `<mi>�</mi>`.
- **Gates:** skeleton **{SK_B} → {SK_A} (+0.001pp; {SK_B4} → {SK_A4})**; ≥50 {GE50} / ≥75 {GE75} / ≥90 {GE90} EXACT; RAW {RAW_B} → {RAW_A};
  {MOVERS}. cs exact {CS} / EXTRA {EX} / missing {MI} EXACT; body 180; clean 98.91% / leak 26/23; every verifier identical; fast-loop baseline
  re-snapshotted; manifest snapshot 2110 / 413; ledger FULL (counter 0, 8 of headroom); feature index rehtml 678 + merge GREEN; 14 selftests GREEN.
  55.8% of achievable.
- **Recorded:** the tableFixed half (declined); the gold's class dressings (C); the 20 Standard named dips; the KB delta 06 §6 → 05D (a KB session).
- **Plateau window (both §4 conditions):** r347 +0.001pp with no other protected gate moved (≥50 / ≥75 / cs all EXACT) → **1 of 3** under-0.02 rounds.

""")
ANCHOR = "## Session 12 · Round 3 (engine r346 — D10-7) — what shipped"
if "## Session 12 · Round 4 (engine r347 — D10-5) — what shipped" not in s:
    assert s.count(ANCHOR) == 1, "state anchor"; s = s.replace(ANCHOR, SEC + ANCHOR, 1); print("LOOP_STATE section")
OLD_P = "- Remaining KB queue (§D):"
NEW_P = (f"- Session 12 Round 4 (engine r347 — Chris's D10-5: every content table ships the KB 05D class form `table table-bordered`; the tableFixed half declined, hook OFF; FULL regeneration of all 416, ledger counter 0; r346's math-italic-letter fix carried): **SHIPPED 2026-09-16 ≈20:30 (session 12, build 260619.18)** — skeleton {SK_B4} → {SK_A4} (+0.001pp), every other protected gate EXACT; plateau window 1 of 3.\n")
if "- Session 12 Round 4 (engine r347" not in s:
    assert s.count(OLD_P) == 1, "position"; s = s.replace(OLD_P, L(NEW_P) + OLD_P, 1); print("position")
OLD_R = "- s12-r3 (engine r346, D10-7)"
i = s.find(OLD_R); assert i > 0, "round log anchor"; j = s.find(nl, i) + len(nl)
NEW_R = (f"- s12-r4 (engine r347, D10-5) · every content table ships `table table-bordered` (KB 05D; `Emit_Templates.elements.table.kb_class_form`, env `TBLBORDER_OFF`; the tableFixed half measured and declined — the gold's 13 contrast-header tables split four ways — hook OFF); FULL regeneration of all 416 (ledger counter 0); carried fix: Word's math-italic letters fold to the plain letter (r346 shipped 34 `<mi>�</mi>`); skeleton {SK_B4} → {SK_A4} (+0.001pp; 52 moved, Standard −1.94 = the named override on the 0.51 tie, Fundamentals +4.46); ≥50 {GE50} / ≥75 {GE75} / cs {CS} / clean / leak / body EXACT; plateau window 1 of 3. Build 260619.18.\n")
if "- s12-r4 (engine r347, D10-5)" not in s:
    s = s[:j] + L(NEW_R) + s[j:]; print("round log")
wr(LS, s); print("LOOP_STATE.md written")
