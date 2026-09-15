#!/usr/bin/env python3
"""ROUND 336 (loop session 6, Round 2) — finalise: changelog, AppVersion (260619.06 → 260619.07), CLAUDE.md §9/§14 (no new
toggle — a registry DATA correction, so §11 gets a one-line note under the r335 row), gate_baseline.json, KB status (no KB row —
a family convention), LOOP_STATE.md (what shipped + position + round log). Idempotent; every repo write keeps LF."""
import io, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)

SK_B, SK_A, RAW_B, RAW_A = "51.078", "51.078", "35.256", "35.256"
GE50_B, GE50_A, GE75_B, GE75_A, GE90 = 1066, 1066, 200, 200, 15
DELTA = "+0.000"; MOVED = "31 moved — 9 up / 22 down, every mover in the affected set, pp-sum +0.62; the 22 dips ≤ 0.32pp NAMED = the scorer's alignment artefact: the phantom chip's `h1` line had been coincidentally matching the gold's second (Te Reo) `h1`, which Claude never ships — the element sequence is now the gold's; SSFUN07_0_0 +2.52 the largest gain"; PCT = "55.8"

CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
ENTRY = f"""## 2026-09-15 (round 336, build 260619.07) — THE FUNDAMENTALS OVERVIEW CHIP IS A FAMILY CONVENTION THE REGISTRY HAD NO EVIDENCE FOR (a `Style_Anchor_Registry.json` correction — ARFUN / ENFUN / TEFUN / MXFUN0 drop the `#module-code` chip, SSFUN gains it; the autonomous loop's session-6 Round 2; **SCOPED regeneration of the 31 affected modules; skeleton {DELTA}pp, every other gate EXACT; scoped ship #2 since the round-334 full-ship backstop**)

### 1. WHAT CHANGED, IN ONE LINE

**Five Fundamentals families resolved their overview `#module-code` chip from a tier that had no evidence for them — ARFUN / ENFUN / TEFUN from the `defaults` (`full-code`, no base row at all), MXFUN0 from a mis-mined `free-text:"MXFUN01"` literal, SSFUN from the em-dash no-evidence marker (element omitted) — while their own golds are unanimous the other way: ARFUN 54/54 pages, ENFUN 8/8, TEFUN 8/8 and MXFUN01–03 3/3 ship NO chip, SSFUN ships the full-code chip on 5 of 6. The registry now says so.**

### 2. THE EVIDENCE (docx → human → Claude)

- **ARFUN02** — WT `[Title] …`; gold header `<h1><span>…</span></h1>` with no `#module-code`; Claude before: `<div id="module-code"><h1>ARFUN02</h1></div>` + the h1; after: the h1 alone.
- **ENFUN02 / TEFUN02 / MXFUN01** — the same shape (gold: no chip; Claude before: the chip). **SSFUN05** — gold `<div id="module-code"><h1>SSFUN05</h1></div>` then the two h1 spans; Claude before: no chip; after: the chip + the spans.
- **The KB:** 06 §3.1 describes the chip for the Standard header; §3.3 (Fundamentals) is silent on it — the authority is the family's own siblings (LOOP §1b level 2/4, unanimous), carried by the registry as every family convention is (the r263 / r285 / r332 registry-correction precedent).

### 3. THE MEASUREMENT (`outputs/_r336_resolve_all.cjs` → `_r336_resolved.json` + `_measure_r336_funchip.py` → `_r336_funchip.json`; surfaced by the re-run substitution instrument `_measure_r336_subst.py` → `_r336_subst.json` — Fundamentals `┌ 2× repeated ⇐ div#module-code` 22 occ / 22 pages / 22 modules)

- For every registry base with Claude output, the gold's overview chip FORM (absent / full-code / padded-number / free-text) against the value the registry RESOLVES: the class = the bases whose gold form solidifies (≥ 0.60) and whose resolved value differs — **ARFUN absent 1.00 (5) · ENFUN absent 1.00 (8) · TEFUN absent 1.00 (8) · MXFUN0 absent 1.00 (3) · SSFUN full-code 0.83 (6)**. Named, not chased: the Inquiry XDLS chips (the gold's chip reads the LMS code `XDLS9003` — the r194 code-variant class, text-only, both sides ship the chip), TEDC 2 modules (padded-number, n = 2), CEDO Inquiry 2, and the singletons SCFUN01 / EXPFUN / BLLR201. The families' second h1 (the ENFUN / TEFUN Te Reo title) is in NO Writers Template — editorial, declined; SSFUN's is in the WT and already ships (r177).
- The affected set is derived from the RESOLVED RULES, not by hand: `_r336_resolve_all.cjs` before and after the edit over all 416 modules → **31 modules** whose resolved `module_code` changed (the five bases' every member with a Claude dir; `_r336_affected.txt`). `Style_Anchor_Registry.json` is read only by `ModuleResolver.Resolve` (and the browser-only reference picker), so identical resolved rules = identical output by construction for the other 385.

### 4. THE FIX — DATA ONLY: five `Style_Anchor_Registry.json` rows, each carrying a `_note`

- `1-10 Arts / ARFUN / base_rules.module_code` → `{{overview: absent, lesson: absent}}` (new); `1-10 English / ENFUN / base_rules.module_code` → the same (new); `1-10 Technology / TEFUN / base_rules.module_code` → the same (new); `1-10 Mathematics / MXFUN / levels.MXFUN0.delta.module_code.overview` → `absent` (was `free-text:"MXFUN01"`); `1-10 Social Science / SSFUN / base_rules.module_code.overview` → `full-code` (was `—`). No engine change, no new env toggle — the reversal is the committed pre-round registry (`git show HEAD~1:converter-v2/data/Style_Anchor_Registry.json`) and the blast radius is proven by the resolved-rules diff + the manifest.

### 5. THE PROOF AND THE GATES

- Scoped regeneration in the planner's 4 batches (`_r336_batches_run.sh`, all rc 0; `_r336_regen.log`); `_content_manifest.py fresh --affected` → **0 truly stale**; `diff` = **exactly 31 pages / 31 modules, 0 added/removed** (one overview page per module; ARFUN04's lesson-like single file and SSFUN07's Standard-folder overview included).
- **Skeleton (PRIMARY): SCAFFOLD mean {SK_B}% → {SK_A}% ({DELTA}pp) / ≥50% {GE50_B} → {GE50_A} / ≥75% {GE75_B} → {GE75_A} / ≥90% {GE90} / skipped 0 @ 1954; RAW {RAW_B}% → {RAW_A}%** (state `outputs/_r336_sk_final.json`, FRESH). {MOVED}.
- Every other gate EXACT (`_fastloop_diff.py` on the 31 PASS; full suite `_r336_gates.log` line-for-line identical to r335 outside the skeleton block): cs exact 11375 / EXTRA 171 / missing 593 · clean 2056/2102 / leak 288/46 · body 191 · tags 9557/9557 · flipCard TOTAL 61 divergence 0 · entry-parity PASS · index-sync 33/28 · **13 selftests GREEN** (`_r336_selftests.log`). **Ceiling:** SCAFFOLD {SK_A}% = **{PCT}% of achievable** (ceiling 91.6%).
- **Verifier:** Fundamentals overview chips Claude vs gold — ARFUN 0/5 = gold, ENFUN 0/8, TEFUN 0/8, MXFUN01–03 0/3, SSFUN 6/6 (gold 5/6, SSFUN0x's absent chip = the family's 1-of-6 deviation, the family form ships).

### 6. NAMED, NOT CHASED

- SSFUN07's gold overview chip is a lesson NUMBER (its Standard-folder multi-file form); the family's full-code chip ships — 1 page. The ENFUN / TEFUN second h1 (Te Reo, not in the WT). The XDLS LMS-code chip text (r194). TEDC / CEDO / the singletons (n < 3).
- Also DECLINED this round on measurement (LOOP_STATE Declined classes): the activity box's SUB-heading level (text-paired agreement already 0.957 in Standard — the r334 note's 655-vs-657 was a position-wise artefact); the outside-box heading LADDER (per-module, no subject shift solidifies in any group ≥ 20 pages); `paddingR` (0.22 even in paired rows); `p ⇐ h5` (25 cases / 17 pages). BLOCKED for Chris: the `alertPadding` activity class (KB 01F table vs the gold's 0.81 plain majority + 05B's "follow the activity's own class set").

**Ledger:** scoped ship #2 since the r334 full-ship backstop · data `Style_Anchor_Registry.json` (five `module_code` rows) · no env toggle (registry correction) · tools `outputs/_measure_r336_subst.py` (+ `_r336_subst.json`), `_measure_r336_subhead.py` (+ `_r336_subhead.json`), `_r336_resolve.cjs`, `_r336_resolve_all.cjs` (+ `_r336_resolved.json` / `_r336_resolved_after.json`), `_measure_r336_funchip.py` (+ `_r336_funchip.json`), `_r336_headladder.json`, `_r336_affected.txt`, `_r336_batches_plan.txt` / `_r336_batches_run.sh`, `_r336_proof.sh`, `_r336_finalise.py` · state `outputs/_r336_sk_final.json` (FRESH) · logs `_r336_regen.log`, `_r336_fastloop.log`, `_r336_gates.log`, `_r336_sk_full.log`, `_r336_selftests.log`, `_r336_fastloop_commit.log`.

"""
if "round 336, build 260619.07" not in s:
    assert s.startswith(head); s = head + ENTRY + s[len(head):]; wr(CL, s); print("changelog prepended")

CF = os.path.join(PF, "app", "js", "Config.js"); c = rd(CF)
OLD = '\tstatic AppVersion = "260619.06";\n'
NEW = ('\t// ROUND 336 (2026-09-15, build 260619.07): the Fundamentals overview #module-code chip is a family convention —\n'
       '\t// Style_Anchor_Registry rows for ARFUN / ENFUN / TEFUN / MXFUN0 (absent) and SSFUN (full-code) mined from the golds\n'
       '\t// (unanimous / 0.83); a data-only registry correction, scoped regeneration of 31 modules; no new toggle.\n'
       '\tstatic AppVersion = "260619.07";\n')
if '"260619.07"' not in c:
    assert c.count(OLD) == 1; c = c.replace(OLD, NEW, 1); wr(CF, c); print("AppVersion bumped")

CM = os.path.join(PF, "CLAUDE.md"); m = rd(CM)
OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 335 BASELINE (the [Engagement quiz button] is the KB's external quiz link button — KB 01F + constraint 65; scoped 28 modules)"
NEW9 = (f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 336 BASELINE (the Fundamentals overview chip is a family convention — a registry correction; scoped 31 modules): SCAFFOLD mean {SK_A}% / >=50% {GE50_A} / >=75% {GE75_A} / >=90% {GE90} / skipped 0 @ 1954; RAW {RAW_A}%** (state `outputs/_r336_sk_final.json`, FRESH). r336 {DELTA} ({MOVED}); every other gate EXACT. Older r335 text: **ROUND 335 BASELINE (the [Engagement quiz button] is the KB's external quiz link button — KB 01F + constraint 65; scoped 28 modules)")
if "ROUND 336 BASELINE" not in m:
    assert m.count(OLD9) == 1, "§9"; m = m.replace(OLD9, NEW9, 1); print("§9")
ROW = ("| *(no toggle)* | 336 | **THE FUNDAMENTALS OVERVIEW CHIP IS A FAMILY CONVENTION** (a `Style_Anchor_Registry.json` correction; the autonomous loop's session-6 Round 2; **SCOPED regeneration of the 31 affected modules; scoped ship #2 since the r334 full backstop**). No engine change and no env toggle — the reversal is the committed pre-round registry. The ARFUN / ENFUN / TEFUN bases had no `module_code` row (the `defaults` `full-code` chip shipped) and MXFUN0 carried a mis-mined `free-text:\"MXFUN01\"` literal, while their golds carry NO chip (54/54, 8/8, 8/8, 3/3 pages); SSFUN's overview value was the em-dash no-evidence marker (chip omitted) while its golds ship the full-code chip 5/6. Rows corrected to `absent` / `full-code` with a `_note` each; the affected set derived from the resolved-rules diff over all 416 modules (`outputs/_r336_resolve_all.cjs`). " + f"Skeleton {DELTA}pp ({MOVED}); every other gate EXACT; 13 selftests GREEN. |\n")
if "| *(no toggle)* | 336 |" not in m:
    A = "| `ENGQUIZ_OFF` | 335 |"; assert m.count(A) == 1, "§11"; m = m.replace(A, ROW + A, 1); print("§11")
B14 = (f"- **Build:** `260619.07` (round 336 — **the Fundamentals overview chip is a family convention** (a registry correction — ARFUN / ENFUN / TEFUN / MXFUN0 drop the `#module-code` chip, SSFUN gains it; the autonomous loop's session-6 Round 2; **SCOPED regeneration of 31 modules; scoped ship #2 since the r334 full backstop**). **ROUND 336 BASELINE: SCAFFOLD mean {SK_A}% / ≥50% {GE50_A} / ≥75% {GE75_A} / ≥90% {GE90} / skipped 0 @ 1954; RAW {RAW_A}%** (state `outputs/_r336_sk_final.json`, FRESH) = **{PCT}% of achievable** (ceiling 91.6%). Every other gate EXACT: cs exact **11375** / EXTRA **171** / missing **593** · clean **2056/2102** / leak **288/46** · body **191** · tags **9557/9557** · flipCard TOTAL 61 divergence 0 · index-sync 33/28 · entry-parity PASS · mtkQuiz shell defect 0 · all THIRTEEN selftests GREEN. Corpus 2102 pages / 413 modules, 0-stale, **31 pages / 31 modules changed, 0 added/removed**; no toggle (data `Style_Anchor_Registry.json`, five `module_code` rows). **Plateau window: r334 +0.167 · r335 +0.018 · r336 {DELTA}.**)\n")
if "- **Build:** `260619.07` (round 336" not in m:
    A = "- **Build:** `260619.06` (round 335 —"; assert m.count(A) == 1, "§14"; m = m.replace(A, B14 + A, 1); print("§14")
wr(CM, m)

GB = os.path.join(HERE, "..", "reference", "tests", "gate_baseline.json"); raw = rd(GB); d = json.loads(raw)
d["_meta"]["build"] = "260619.07"; d["_meta"]["round"] = 336; d["_meta"]["date"] = "2026-09-15"
d["skeleton"].update({"mean_scaffold_pct": float(SK_A), "raw_mean_pct": float(RAW_A), "pages_ge_50": GE50_A, "pages_ge_75": GE75_A})
d["_meta"]["_round336_note"] = f"Round 336 (the Fundamentals overview chip is a family convention — a Style_Anchor_Registry correction; scoped 31-module regeneration, scoped ship #2 since the r334 full backstop). Skeleton {SK_B}->{SK_A} ({DELTA}pp; {MOVED}; >=50 {GE50_B}->{GE50_A}, >=75 {GE75_B}->{GE75_A}, >=90 {GE90}); every other gate EXACT; 13 selftests GREEN."
wr(GB, json.dumps(d, ensure_ascii=False) + ("\n" if raw.endswith("\n") else "")); print("gate_baseline.json refreshed")

LS = os.path.join(HERE, "..", "..", "LOOP_STATE.md"); s = rd(LS); nl = "\r\n" if "\r\n" in s[:3000] else "\n"
def L(t): return t.replace("\n", nl)
SEC = L(f"""## Session 6 · Round 2 (engine r336) — what shipped (the Fundamentals overview chip is a family convention)
- **Fix (DATA only, no toggle):** five `Style_Anchor_Registry.json` `module_code` rows — ARFUN / ENFUN / TEFUN base_rules `{{overview: absent,
  lesson: absent}}` (new rows; the chip had resolved from the `defaults` tier), MXFUN0 delta overview `absent` (was the mis-mined
  `free-text:"MXFUN01"`), SSFUN base_rules overview `full-code` (was the em-dash no-evidence marker → element omitted); a `_note` on each.
  The reversal is the committed pre-round registry; the blast radius is the resolved-rules diff over all 416 modules (`_r336_resolve_all.cjs`).
- **Regeneration:** scoped — exactly the 31 modules whose resolved `module_code` changed (the five bases' every member with a Claude dir);
  4 planner batches all rc 0; 0 truly stale; manifest diff = exactly 31 pages / 31 modules, 0 added/removed.
- **Gates:** skeleton {SK_B} → {SK_A} ({DELTA}pp; {MOVED}); ≥50 {GE50_B} → {GE50_A}; ≥75 {GE75_B} → {GE75_A}; ≥90 {GE90}; every other gate
  line-for-line EXACT with r335 (fastloop PASS; full suite `_r336_gates.log`); 13 selftests GREEN. **{PCT}% of achievable.**
- **Verifier:** Fundamentals overview chips = the gold's family form on 30 of 31 (SSFUN07's gold chip is a lesson number — named).
  Ship ledger: scoped #2 since the r334 full-ship backstop. **Plateau window: r334 +0.167 · r335 +0.018 · r336 {DELTA}.**

""")
ANCHOR = "## Session 6 · Round 2 PICK (engine r336)"
if "## Session 6 · Round 2 (engine r336) — what shipped" not in s:
    assert s.count(ANCHOR) == 1; s = s.replace(ANCHOR, SEC + ANCHOR, 1); print("LOOP_STATE section")
OLD_P = "- Remaining KB queue (§D):"
NEW_P = f"- Session 6 Round 2 (engine r336 — the Fundamentals overview chip is a family convention, a registry correction): SHIPPED 2026-09-15 (session 6). AppVersion 260619.07, CLAUDE.md §9/§11/§14, scoped ship #2 since the r334 full backstop. Skeleton {DELTA}pp; every other gate EXACT." + nl + OLD_P
if "- Session 6 Round 2 (engine r336" not in s:
    assert s.count(OLD_P) == 1, "position"; s = s.replace(OLD_P, NEW_P, 1); print("position")
OLD_R = "- s5-r6 / s6-r1 (engine r335)"
i = s.find(OLD_R); assert i > 0, "round log anchor"; j = s.find(nl, i) + len(nl)
NEW_R = f"- s6-r2 (engine r336) · the Fundamentals overview `#module-code` chip is a family convention (a `Style_Anchor_Registry.json` correction: ARFUN / ENFUN / TEFUN / MXFUN0 drop the chip the golds never ship, SSFUN gains the chip its golds ship 5/6) · SHIPPED 2026-09-15 · scoped regeneration, 31 pages / 31 modules · scaffold {SK_B}→{SK_A} ({DELTA}; {MOVED}), ≥50 {GE50_B}→{GE50_A}, ≥75 {GE75_B}→{GE75_A}, every other gate EXACT · chips = the family form on 30/31 · {PCT}% of achievable · scoped ship #2 since the r334 full · sub-heading level / heading ladder / paddingR / p⇐h5 DECLINED on measurement; alertPadding → needs Chris · commit (see git log)" + nl
if "- s6-r2 (engine r336)" not in s:
    s = s[:j] + NEW_R + s[j:]; print("round log")
wr(LS, s); print("LOOP_STATE.md written")
