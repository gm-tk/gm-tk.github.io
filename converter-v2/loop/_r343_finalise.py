#!/usr/bin/env python3
"""ROUND 343 (loop session 11 Round 1 — Chris's D10-6) — finalise: changelog, AppVersion (260619.13 → 260619.14), CLAUDE.md §9/§14,
gate_baseline.json, KB status D-row, LOOP_STATE.md (what shipped + position + round log). Idempotent; LF kept."""
import io, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)

SK_B, SK_A, RAW_B, RAW_A = "51.129", "51.265", "35.309", "35.394"
SK_B4, SK_A4 = "51.1291", "51.2646"
GE50, GE75, GE90, PAIRS_B, PAIRS_A = 1073, 198, 15, 1962, 1955
CS_B, CS_A, EX, MI_B, MI_A = 11482, 11469, 175, 608, 607
CLEAN_B, CLEAN_A = "2087/2110 = 98.91%", "2080/2103 = 98.91%"
PCT = "55.8"; CEIL_B, CEIL_A = "91.6", "91.9"
EIGHT = "CEDR201 / CEDR301 / CEDR302 / CEDT201 / CEDT202 / CEDT203 / CEDT204 / CEDW303"

# ---------------------------------------------------------------- 1. BUILD_CHANGELOG.md
CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)" + chr(10) + chr(10)
ENTRY = f"""## 2026-09-16 (round 343, build 260619.14) — THE EIGHT CED REVISION-BRIEF MODULES LEAVE THE COMPARISON SET (Chris's decision D10-6, Option C; a GATE-CONFIGURATION round — no engine change, no regeneration; every baseline RE-ESTABLISHED on the new population, the ≈ +0.14pp recorded as a POPULATION change, never claimed)

### 1. WHAT CHANGED, IN ONE LINE

**{EIGHT} stay in the corpus — their Claude dirs are regenerated with their families and keep their `_interactives.txt`, so a developer still gets whatever PageForge can make — but stop counting in the score: their Writers Template is an EDIT BRIEF for content held in the previous module version, not a conversion source, so no converter rule can ever reach the human's page and the score only measured that fact. ONE list, honoured by every gate: `reference/tests/compare_exclusions.txt` (the eight codes + the reason) read by the new `_corpus.gate_mods(root)`; `_corpus.mods()` stays INCLUSIVE (batch plans, the content manifest, the registries and the feature index still cover the eight).** Authority: Chris (D10-6, 2026-09-16); overrides nothing.

### 2. THE SEAM

- `_corpus.py` gains `excluded()` (the codes in `compare_exclusions.txt`, `#` comments ignored, empty when the file is absent) and `gate_mods(root)` = `mods(root)` minus that set. The eight scored-population lines switch to it: `_skeleton_compare.py` (the PRIMARY gate), `_structural_defect_audit.py`, `compare_structure.py`, `body_compare.py`, `_discrepancy_audit.py` (the pairing source), `strict_compare.py`, `scaffold_audit.py`, `anchor_compare.py`'s `all_codes()` — and the ceiling instrument `outputs/_measure_ceiling.py`. Nothing else moves: `_batch_plan.py`, `_content_manifest.py`, `_fastloop_diff.py`'s drift list, `_gate_fresh.py`, the registry / feature-index builders keep `mods()`.
- `reference/tests/` is outside the git repo (CLAUDE.md §4), so the change is made DURABLE the r315 way: `outputs/_r343_exclusions.py` re-applies every edit idempotently (LF / CRLF kept per file) and is mirrored with `compare_exclusions.txt` + `_corpus.py` into `converter-v2/loop/`; `_MIGRATION/CHECKSUMS__gates.txt` refreshed (backup `CHECKSUMS__gates.pre-r343.bak`, the exclusions file added — 82 entries), `verify_after_transfer.sh` PASS; `CORPUS_CENSUS.txt` notes the scored population (2103 pages / 409 modules; the corpus itself unchanged at 2110 / 416).

### 3. THE PROOF — a population change and nothing else

- Predicted from the r342 state before any code: the seven paired pages (CEDW303 has no Claude dir) score 8.31 – 19.59% and drop out; every bucket unchanged; mean 51.1291 → 51.2646. Measured (`_r343_sk_final.json` vs `_r342_sk_final.json`): **1962 → 1955 pairs — exactly the seven dropped, none added, ZERO pages score-moved** (every one of the 1955 kept pages identical to the decimal).
- **Skeleton (PRIMARY): SCAFFOLD mean {SK_B}% → {SK_A}% (+0.135pp, a POPULATION change; {SK_B4} → {SK_A4}) / ≥50% {GE50} / ≥75% {GE75} / ≥90% {GE90} EXACT / skipped 0 @ {PAIRS_B} → {PAIRS_A}; RAW {RAW_B}% → {RAW_A}%.** compare_structure exact {CS_B} → {CS_A} (−13 = the seven pages' own matched elements leaving the pool; matched 13532 → 13516) / EXTRA {EX} EXACT / missing {MI_B} → {MI_A} (−1, same); structurally clean {CLEAN_B} → {CLEAN_A} (the seven were clean); literal-tag leak 26 / 23 EXACT; body_compare ANY 180 EXACT (2110 → 2103 pages compared); tags 9557 / 9557; flipCard / speechBubble / modal / mtkQuiz verifiers identical to r342 (`_r343_gates.log`); index-sync 33/28; entry-parity PASS.
- **The ceiling re-measured on the new population** (`_measure_ceiling.py --json _ceiling_r343.json --md _ceiling_r343.md --baseline _r343_sk_final.json`): no-source share net 8.1% → **CEILING {CEIL_B}% → {CEIL_A}%** (loose 94.5%; full-scope 87.3%); **SCAFFOLD {SK_A}% = {PCT}% of achievable** (band 54.3 – 55.8%); RAW = 40.6% of its ceiling; outlier pages 43 → 36. (The Round-0 files `_ceiling_r0.*` were restored from the mirror after the tool's default run overwrote them — quote `_ceiling_r343.*` from here on.)
- Fast-loop baseline re-snapshotted on the new population (`_r343_fastloop_snapshot.log`: sk_pages 1955, cs_matched 13516, body_pages 2103, df_total 2103, df_clean 2080); `gate_baseline.json` refreshed. **Judge every later round against THIS state; the +0.135pp is never a gain and is never re-counted.**

**Ledger:** no ship (no regeneration — the corpus on disk is r342's, byte-for-byte) · data `reference/tests/compare_exclusions.txt` · no env toggle (the reversal is an empty exclusions file) · tools `outputs/_r343_exclusions.py`, `_r343_gates.log`, `_r343_sk_final.json` / `_r343_sk_full.log`, `_r343_fastloop_snapshot.log`, `_r343_ceiling_run.log` + `_ceiling_r343.{{json,md}}`, `_r343_finalise.py` · AppVersion 260619.14.

"""
if "round 343, build 260619.14" not in s:
    assert s.startswith(head); s = head + ENTRY + s[len(head):]; wr(CL, s); print("changelog prepended")

# ---------------------------------------------------------------- 2. Config.js
CF = os.path.join(PF, "app", "js", "Config.js"); c = rd(CF)
OLD = '\tstatic AppVersion = "260619.13";' + chr(10)
NEW = ('\t// ROUND 343 (2026-09-16, build 260619.14): a GATE-CONFIGURATION round, no engine change — the eight CED revision-brief' + chr(10) +
       '\t// modules leave the scored population (Chris\'s D10-6; reference/tests/compare_exclusions.txt + _corpus.gate_mods());' + chr(10) +
       '\t// every baseline re-established on 1955 pairs; the corpus on disk is r342\'s byte-for-byte.' + chr(10) +
       '\tstatic AppVersion = "260619.14";' + chr(10))
if '"260619.14"' not in c:
    assert c.count(OLD) == 1; c = c.replace(OLD, NEW, 1); wr(CF, c); print("AppVersion bumped")

# ---------------------------------------------------------------- 3. CLAUDE.md §9 / §14
CM = os.path.join(PF, "CLAUDE.md"); m = rd(CM)
OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 342 BASELINE (a writer's MEDIA tag typed as a HYPERLINK is still a tag"
NEW9 = (f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 343 BASELINE — RE-ESTABLISHED ON THE D10-6 POPULATION (the eight CED revision-brief modules {EIGHT} leave every scored gate via `reference/tests/compare_exclusions.txt` + `_corpus.gate_mods()`; a gate-configuration round, no engine change, no regeneration): SCAFFOLD mean {SK_A}% / >=50% {GE50} / >=75% {GE75} / >=90% {GE90} / skipped 0 @ {PAIRS_A}; RAW {RAW_A}%** (state `outputs/_r343_sk_final.json`, FRESH) = **{PCT}% of achievable** against the re-measured **CEILING {CEIL_A}%** (`_ceiling_r343.json`; was {CEIL_B}%). The +0.135pp vs r342 ({SK_B4} → {SK_A4}) is a POPULATION change — the seven paired pages (8.3 – 19.6%) left, every one of the 1955 kept pages scores identically — never a gain; buckets EXACT; cs exact {CS_B} → {CS_A} / EXTRA {EX} / missing {MI_B} → {MI_A} (the seven pages' own elements leaving the pool); clean {CLEAN_A}; leak 26/23; body 180 EXACT. **A comparison across round 343 must use the same population on both sides.** Older r342 text: **ROUND 342 BASELINE (a writer's MEDIA tag typed as a HYPERLINK is still a tag")
if "ROUND 343 BASELINE" not in m:
    assert m.count(OLD9) == 1, "§9"; m = m.replace(OLD9, NEW9, 1); print("§9")
B14 = (f"- **Build:** `260619.14` (round 343 — **the eight CED revision-brief modules leave the comparison set** (Chris's D10-6, Option C: `reference/tests/compare_exclusions.txt` + `_corpus.gate_mods()` — ONE list every scored gate honours; `mods()` stays inclusive so the eight are still regenerated, manifested and indexed; a gate-configuration round, no engine change, no regeneration; the durable record is `outputs/_r343_exclusions.py`, mirrored). **ROUND 343 BASELINE: SCAFFOLD mean {SK_A}% / ≥50% {GE50} / ≥75% {GE75} / ≥90% {GE90} / skipped 0 @ {PAIRS_A}; RAW {RAW_A}%** (state `outputs/_r343_sk_final.json`) = **{PCT}% of achievable** (ceiling re-measured {CEIL_A}%, `_ceiling_r343.json`). +0.135pp = a POPULATION change (1962 → 1955 pairs, exactly the seven paired revision-brief pages; 0 pages moved) — never claimed. cs exact **{CS_A}** (−13, the seven pages' elements) / EXTRA **{EX}** / missing **{MI_A}** (−1); clean **{CLEAN_A}** / leak **26/23**; body **180** EXACT; every other gate identical to r342; 13 selftests GREEN. Corpus on disk unchanged: 2110 pages / 416 modules (scored 2103 / 409). No toggle — the reversal is an empty exclusions file.\n")
if "- **Build:** `260619.14` (round 343" not in m:
    A = "- **Build:** `260619.13` (round 342 —"; assert m.count(A) == 1, "§14"; m = m.replace(A, B14 + A, 1); print("§14")
wr(CM, m)

# ---------------------------------------------------------------- 4. gate_baseline.json
GB = os.path.join(HERE, "..", "reference", "tests", "gate_baseline.json"); raw = rd(GB); d = json.loads(raw)
d["_meta"]["build"] = "260619.14"; d["_meta"]["round"] = 343; d["_meta"]["date"] = "2026-09-16"
d["skeleton"].update({"mean_scaffold_pct": float(SK_A), "raw_mean_pct": float(RAW_A), "pages_ge_50": GE50, "pages_ge_75": GE75, "pages_ge_90": GE90})
if "compare_structure" in d and isinstance(d["compare_structure"], dict):
    cs = d["compare_structure"]
    for k, v in (("exact_chain", CS_A), ("missing_container", MI_A), ("claude_missing_container", MI_A)):
        if k in cs: cs[k] = v
for sect in ("defect", "structural_defect", "defect_audit"):
    if sect in d and isinstance(d[sect], dict):
        for k, v in (("clean_pages", 2080), ("total_pages", 2103)):
            if k in d[sect]: d[sect][k] = v
d["_meta"]["_round343_note"] = (f"Round 343 (D10-6: the eight CED revision-brief modules excluded from every scored gate via compare_exclusions.txt; no engine change, no regeneration). "
    f"POPULATION re-baseline: pairs {PAIRS_B}->{PAIRS_A} (exactly the 7 paired briefs; 0 pages score-moved); skeleton {SK_B4}->{SK_A4} (+0.135pp, never a gain); "
    f"buckets {GE50}/{GE75}/{GE90} EXACT; cs exact {CS_B}->{CS_A} / missing {MI_B}->{MI_A} (the 7 pages' elements); clean 2080/2103; body 180; leak 26/23 EXACT. Ceiling 91.6->91.9%.")
wr(GB, json.dumps(d, ensure_ascii=False) + (chr(10) if raw.endswith(chr(10)) else "")); print("gate_baseline.json refreshed")

# ---------------------------------------------------------------- 5. KB_AMALGAMATION_STATUS.md D-row
KB = os.path.join(HERE, "..", "..", "KB_AMALGAMATION_STATUS.md"); k = rd(KB)
anchor = "| ~~—~~ | (not a KB row — KB 05A lists three audio forms"
drow = (f"| ~~—~~ | (not a KB row — Chris's D10-6, Option C) the eight CED revision-brief modules ({EIGHT}) leave the comparison set: `compare_exclusions.txt` + `_corpus.gate_mods()`, honoured by every scored gate; the eight stay in the corpus, regenerated with their families, `_interactives.txt` kept | **SHIPPED round 343** (a gate-configuration round; every baseline re-established on 1955 pairs; ceiling 91.6 → 91.9%) | 0 pages changed (7 paired pages leave the score) | +0.135pp = a POPULATION change, never a gain; buckets / leak / body EXACT | none (an empty exclusions file reverts) | DECIDED (Chris; the durable record `outputs/_r343_exclusions.py`) |\n")
if "leave the comparison set: `compare_exclusions.txt`" not in k:
    assert k.count(anchor) == 1; k = k.replace(anchor, drow + anchor, 1); print("KB status D-row")
wr(KB, k)

# ---------------------------------------------------------------- 6. LOOP_STATE.md
LS = os.path.join(HERE, "..", "..", "LOOP_STATE.md"); s = rd(LS); nl = chr(13) + chr(10) if chr(13) + chr(10) in s[:3000] else chr(10)
def L(t): return t.replace(chr(10), nl)
SEC = L(f"""## Session 11 · Round 1 (gate-config round r343 — D10-6) — what shipped (the eight CED revision-brief modules leave the comparison set)
- **Fix:** `reference/tests/compare_exclusions.txt` ({EIGHT} + the reason) + `_corpus.excluded()` / `gate_mods(root)`; the eight scored-population
  lines switched to `gate_mods` (`_skeleton_compare.py`, `_structural_defect_audit.py`, `compare_structure.py`, `body_compare.py`,
  `_discrepancy_audit.py`, `strict_compare.py`, `scaffold_audit.py`, `anchor_compare.py`) + `outputs/_measure_ceiling.py`; `mods()` stays
  inclusive (batch plans / manifest / registries / feature index). Durable record (the gate tools are outside git): `outputs/_r343_exclusions.py`
  (idempotent, re-applies every edit), mirrored with `compare_exclusions.txt` + `_corpus.py`; `_MIGRATION/CHECKSUMS__gates.txt` refreshed
  (82 entries, backup `.pre-r343.bak`), `verify_after_transfer.sh` PASS; `CORPUS_CENSUS.txt` notes the scored population (2103 / 409).
- **No regeneration, no engine change** (AppVersion 260619.14 bumped for the round ↔ build mapping only). **Proof:** `_r343_sk_final.json` vs
  `_r342_sk_final.json` = 1962 → 1955 pairs, exactly the seven paired briefs dropped (8.31 – 19.59%), 0 added, **0 pages score-moved**.
- **Gates (RE-BASELINED — the population change, never a gain):** skeleton {SK_B} → {SK_A} (+0.135pp; {SK_B4} → {SK_A4}); ≥50 {GE50} / ≥75 {GE75} /
  ≥90 {GE90} EXACT; RAW {RAW_B} → {RAW_A}; cs exact {CS_B} → {CS_A} (−13 = the seven pages' elements) / EXTRA {EX} / missing {MI_B} → {MI_A}; clean
  {CLEAN_B} → {CLEAN_A}; leak 26/23; body 180 EXACT; every verifier identical to r342. **Ceiling re-measured on the new population:
  {CEIL_B}% → {CEIL_A}% (`_ceiling_r343.json`; the tool's default run overwrote `_ceiling_r0.*`, restored from the mirror) → SCAFFOLD {SK_A}% =
  {PCT}% of achievable.** Fast-loop baseline re-snapshotted (`_r343_fastloop_snapshot.log`), `gate_baseline.json` refreshed.
- **The plateau window** ignores this round (a population change moves no page); it stands at r341 +0.021 · r342 −0.003.

""")
ANCHOR = "## Session 11 · Round 1 PICK (gate-config round r343"
if "## Session 11 · Round 1 (gate-config round r343 — D10-6) — what shipped" not in s:
    assert s.count(ANCHOR) == 1; s = s.replace(ANCHOR, SEC + ANCHOR, 1); print("LOOP_STATE section")
OLD_P = "- Remaining KB queue (§D):"
NEW_P = (f"- Session 11 Round 1 (gate-config round r343 — Chris's D10-6: the eight CED revision-brief modules leave the comparison set via `compare_exclusions.txt` + `_corpus.gate_mods()`; no engine change, no regeneration): **SHIPPED 2026-09-16 ≈17:15 (session 11)**. AppVersion 260619.14, CLAUDE.md §9/§14, KB status D-row, `gate_baseline.json` + fast-loop baseline + ceiling RE-ESTABLISHED on 1955 pairs (skeleton {SK_A}%, ceiling {CEIL_A}%, {PCT}% of achievable) — the +0.135pp is a population change, never a gain." + nl)
if "- Session 11 Round 1 (gate-config round r343" not in s:
    assert s.count(OLD_P) == 1, "position"; s = s.replace(OLD_P, NEW_P + OLD_P, 1); print("position")
OLD_R = "- s9-r2 / s11-r0 (engine r342)"
i = s.find(OLD_R); assert i > 0, "round log anchor"; j = s.find(nl, i) + len(nl)
NEW_R = (f"- s11-r1 (gate-config r343, D10-6) · the eight CED revision-brief modules ({EIGHT}) leave every scored gate (`compare_exclusions.txt` + `_corpus.gate_mods()`; the eight stay in the corpus, regenerated with their families) · SHIPPED 2026-09-16 · no regeneration, no engine change · RE-BASELINE: pairs {PAIRS_B}→{PAIRS_A} (exactly the seven paired briefs, 0 pages score-moved), scaffold {SK_B}→{SK_A} (+0.135pp = a POPULATION change, never a gain), buckets {GE50}/{GE75}/{GE90} EXACT, cs {CS_A}/{EX}/{MI_A}, clean {CLEAN_A}, leak 26/23, body 180 · ceiling {CEIL_B}→{CEIL_A}% · {PCT}% of achievable · commit (see git log) · plateau window unchanged (r341 +0.021 · r342 −0.003)" + nl)
if "- s11-r1 (gate-config r343" not in s:
    s = s[:j] + NEW_R + s[j:]; print("round log")
wr(LS, s); print("LOOP_STATE.md written")
