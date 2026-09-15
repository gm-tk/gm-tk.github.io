#!/usr/bin/env python3
"""ROUND 327 — finalise: changelog, AppVersion, CLAUDE.md §9/§11/§14, KB status row 1 (both copies), gate_baseline.json,
LOOP_STATE.md (what shipped + position + round log). Idempotent."""
import io, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)
SK, RAW = "50.492", "34.831"

CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
ENTRY = f"""## 2026-09-15 (round 327, build 260618.98) — A MULTI-WORD ALL-CAPS TITLE RENDERS IN SENTENCE CASE (the KB's title-casing rule — 01A_TEMPLATE_LEVELS_CORE, 10_CORPUS_VALIDATED_SCAFFOLDING §1, constraint 1's permitted normalisations; the autonomous loop, session 4, Round 2; **SCOPED regeneration of the 15 affected modules; gate-neutral — every protected gate EXACT; scoped ship #1 since the round-326 full**)

### 1. WHAT CHANGED, IN ONE LINE

**A writer's multi-word ALL-CAPS header title (`DREAM IT, PLAN IT, DO IT`, `TE TIRITI O WAITANGI`) now renders in sentence case — `Dream it, plan it, do it` — with macrons kept, a code token like `(US7121)` left alone, a single all-caps token (`STOMP`) untouched, and ONE red flag quoting the original so the designer can restore any proper-noun capitals. 47 pages / 15 modules changed; Claude's all-caps multi-word header spans 47 → 0.**

### 2. THE EVIDENCE (docx → human → Claude)

- **CEDK501 lesson 1** — docx: `DREAM IT, PLAN IT, DO IT` → gold: `<h1><span>Dream it, plan it, do it</span></h1>` → Claude before: `<h1><span>DREAM IT, PLAN IT, DO IT</span></h1>`; after: the gold's form + `Red Flag: The writer's title is ALL CAPS ("DREAM IT, PLAN IT, DO IT") — rendered in sentence case per the KB's title-casing rule; restore any proper-noun or acronym capitals the writer intended.`
- **HIS1005 lesson 2** — docx: `TE TIRITI O WAITANGI` → gold: `Te tiriti o waitangi` (the human lost the proper-noun capitals too — exactly what the KB's flag exists for) → Claude after: `Te tiriti o waitangi` + the flag.
- **PES1007 lesson 4** — docx: `INTRODUCTION TO POTENTIAL ENERGY AND WORK` → gold: `Introduction to potential energy and work` → Claude after: the same.
- **The KB:** `01A_TEMPLATE_LEVELS_CORE.md` "Title casing — normalise a MULTI-WORD ALL-CAPS title (corpus-validated)": sentence case, the Te Reo span the same with macrons preserved, a single all-caps token left as written, a proper-noun caution with a visible red flag quoting the original; titles already in sentence / title / mixed case rendered exactly as written. `10_CORPUS_VALIDATED_SCAFFOLDING.md` §1: 0 of 105 finished multi-word header spans are all-caps. Constraint 1 lists "ALL-CAPS title → sentence case" among the permitted normalisations; `KB_AMALGAMATION_STATUS.md` row 1 had it UNVERIFIED.

### 3. THE MEASUREMENT (every header `<h1><span>`, acks / glossary pages excluded)

- Gold 3,047 spans — 15 all-caps multi-word, every one an unreplaced placeholder (`TE REO TRANSLATION HERE`, `MODULE TITLE TE REO`, `TRANSLATION NEEDED`): 0 real titles. **Claude 2,345 spans — 47 all-caps multi-word on 47 pages / 15 modules** (Standard 44 / Inquiry 3; HIS1005 9, HIS1001 6, CEDO502 6, HES1003 5, HIS1007 4, CEDK501 3, HIS1006 3, HIS1008 3, HES1004 2, PES1007 2, CEDO501 / ENGS101 / HES1005 / MXEO401 / PES1008 1), all the writer's own capitals carried verbatim. The gold re-cases every paired one but is era-mixed in HOW (sentence case 26, Title Case 14, lowercase 2 — `a mule, a wizard and jim crow`); the KB's sentence case is the target.
- The wider case-only title class (r324's classifier: 88 pages) is otherwise the gold's editorial Title-Case / sentence-case choices on titles the writer typed in mixed case — the KB says render those as written → class C. After this round the classifier reads **exact 550 → 567, case/ws/macron-only 88 → 71** (`_r327_lessontitles_after.json`).

### 4. THE FIX — one data block `Emit_Templates.header.title_casing` `{{ enabled, env: "TITLECASE_OFF", min_words: 2, keep_tokens_with_digits: true, red_flag }}`

- **`SkeletonBuilder.#titleCasing`** at the header title fill (the plain `title_h1` and the lowercase-span templates; the BLL phonics template is the round-125 mechanism and is untouched): a title whose letter-tokens (≥ `min_words`, a token carrying a digit excluded) are ALL upper-case and include at least one token longer than one letter is lower-cased (macrons survive — `HARURUTANGA ME NGĀ KŌHIMUHIMU` → `Harurutanga me ngā kōhimuhimu`) and its first letter capitalised; `(US7121)` keeps its case; `STOMP` / `A B` / `EXPFUN02` are untouched. One `NotesAndComments.redFlag(…, "diagnostic")` cv2-note follows the `<h1>` on every normalised title — the KB's proper-noun caution applied to all of them, because the converter cannot tell `Castle Bravo` from `castle bravo`.
- **Env toggle `TITLECASE_OFF`** reverts byte-for-byte.

### 5. THE PROOF AND THE GATES

- The in-memory ON probe over ALL 416 modules (`_r327_probe_on_0*.log`) names exactly **47 pages / 15 modules** = the measured population; scoped regeneration of the 15 (`_r327_batches_run.sh`, 2 batches); `_content_manifest.py fresh --affected` → **0 truly stale** (398 untouched modules byte-identical to the r326 manifest); OFF in memory vs disk on the 15 = exactly the 47 changed pages, ON in memory = disk on 160/160.
- **Every protected gate EXACT** (`_fastloop_diff.py` on the 15 → PASS, every metric delta 0; the full suite `_r327_gates.log` identical to r326): skeleton SCAFFOLD mean **{SK}%** / ≥50% 1030 / ≥75% 196 / ≥90% 15 / skipped 0 @ 1954, RAW {RAW}% (`_r327_sk_final.json`: 0 pages moved — the skeleton is text-stripped, the note is a cv2-note) · cs exact 11360 / EXTRA 186 / missing 591 · clean 2056/2102 / leak 288/46 · body 191 · tags 9557/9557 · flipCard TOTAL 61 divergence 0 · mtkQuiz 17 shells defect 0 · entry-parity PASS · index-sync 33/28 · **13 selftests GREEN**.
- Claude all-caps multi-word header spans **47 → 0**; 47 red flags emitted (one per title).
- **Ceiling:** SCAFFOLD {SK}% = **55.1% of achievable** (unchanged).

### 6. NAMED, NOT CHASED

- The gold's own Title-Case and lowercase re-casings of mixed-case writer titles (the remaining 71 case-only pages) — the KB says render as written; class C.
- `*SPECIFIC LATENT HEAT*` (PES1008 5) keeps its asterisks — a Word emphasis residue in the title source, a separate mechanism.
- The KB's proper-noun heuristic ("likely contains a proper noun") is applied as "always flag" — recorded as the deliberate reading.

**Ledger:** scoped ship #1 since the r326 full · data `header.title_casing` · env `TITLECASE_OFF` · tools `outputs/_r327_finalise.py` (the measurement is the inline probe recorded in `LOOP_STATE.md`; the r324 classifier re-run → `_r327_lessontitles_after.json` / `_r327_lessontitles.log`) · state `outputs/_r327_sk_final.json` (FRESH, identical to r326) · logs `_r327_gates.log`, `_r327_sk_full.log`, `_r327_fastloop.log`, `_r327_selftests.log`, `_r327_probe_on_0*.log`, `_r327_probe_off.log`, `_r327_probe_on.log`, `_r327_regen.log`, `_r327_affected.txt`.

"""
if "round 327, build 260618.98" not in s:
    assert s.startswith(head); s = head + ENTRY + s[len(head):]; wr(CL, s); print("changelog prepended")

CF = os.path.join(PF, "app", "js", "Config.js"); c = rd(CF)
OLD = '\tstatic AppVersion = "260618.97";\n'
NEW = ('\t// ROUND 327 (2026-09-15, build 260618.98): a multi-word ALL-CAPS header title renders in sentence\n'
       '\t// case (the KB\'s title-casing rule) + one red flag quoting the original; a single all-caps token\n'
       '\t// and a code token keep their case. 47 pages / 15 modules, scoped. Env TITLECASE_OFF; data\n'
       '\t// header.title_casing.\n'
       '\tstatic AppVersion = "260618.98";\n')
if '"260618.98"' not in c:
    assert c.count(OLD) == 1; c = c.replace(OLD, NEW, 1); wr(CF, c); print("AppVersion bumped")

CM = os.path.join(PF, "CLAUDE.md"); m = rd(CM)
OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 326 BASELINE (a call-to-action button is an anchor — the KB's universal button form; FULL regeneration)"
NEW9 = (f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 327 BASELINE (a multi-word ALL-CAPS title renders in sentence case — the KB's title-casing rule; scoped, gate-neutral): SCAFFOLD mean {SK}% / >=50% 1030 / >=75% 196 / >=90% 15 / skipped 0 @ 1954; RAW {RAW}%** (state `outputs/_r327_sk_final.json`, FRESH; 0 pages moved — identical to r326). Older r326 text: **ROUND 326 BASELINE (a call-to-action button is an anchor — the KB's universal button form; FULL regeneration)")
if "ROUND 327 BASELINE" not in m:
    assert m.count(OLD9) == 1, "§9"; m = m.replace(OLD9, NEW9, 1); print("§9")
ROW = ("| `TITLECASE_OFF` | 327 | **A MULTI-WORD ALL-CAPS TITLE RENDERS IN SENTENCE CASE** (the KB's title-casing rule — `01A_TEMPLATE_LEVELS_CORE` / `10_CORPUS_VALIDATED_SCAFFOLDING` §1 / constraint 1; the autonomous loop's session-4 Round 2; **SCOPED regeneration of the 15 affected modules; scoped ship #1 since the r326 full**). Reverts byte-for-byte. ON (default), `header.title_casing`: at `SkeletonBuilder`'s header title fill (`#titleCasing`; the plain and lowercase-span templates, never the BLL phonics template) a title whose letter-tokens (≥ 2, digit-carrying tokens excluded) are all upper-case is lower-cased (macrons kept) with its first letter capitalised — `DREAM IT, PLAN IT, DO IT` → `Dream it, plan it, do it`, `(US7121)` untouched, `STOMP` untouched — and ONE red flag (cv2-note, gate-neutral) quoting the original follows the h1 (the KB's proper-noun caution, applied to every normalised title). MEASURED: gold 0 real all-caps multi-word header spans of 3,047 (15 = unreplaced placeholders); Claude 47 on 47 pages / 15 modules → 0. Gate-neutral: every gate EXACT, skeleton page-for-page identical, 13 selftests GREEN; the r324 title classifier exact 550 → 567. |\n")
if "| `TITLECASE_OFF` | 327 |" not in m:
    A = "| `BTNANCHOR_OFF` | 326 |"; assert m.count(A) == 1, "§11"; m = m.replace(A, ROW + A, 1); print("§11")
B14 = (f"- **Build:** `260618.98` (round 327 — **a multi-word ALL-CAPS title renders in sentence case** (the KB's title-casing rule; the autonomous loop's session-4 Round 2; **SCOPED regeneration of 15 modules; scoped ship #1 since the r326 full**). **ROUND 327 BASELINE = r326: SCAFFOLD mean {SK}% / ≥50% 1030 / ≥75% 196 / ≥90% 15 / skipped 0 @ 1954; RAW {RAW}%** (state `outputs/_r327_sk_final.json`, FRESH, 0 pages moved) = **55.1% of achievable** (ceiling 91.6%). Every gate EXACT: cs exact **11360** / EXTRA **186** / missing **591** · clean **2056/2102** / leak **288/46** · body **191** · tags **9557/9557** · flipCard TOTAL 61 divergence 0 · index-sync 33/28 · entry-parity PASS · mtkQuiz shell defect 0 · all THIRTEEN selftests GREEN. Corpus 2102 pages / 413 modules, 0-stale, **47 pages / 15 modules changed, 0 added/removed**; toggle `TITLECASE_OFF`; data `header.title_casing`. Claude all-caps multi-word header titles 47 → 0.)\n")
if "- **Build:** `260618.98` (round 327" not in m:
    A = "- **Build:** `260618.97` (round 326 —"; assert m.count(A) == 1, "§14"; m = m.replace(A, B14 + A, 1); print("§14")
wr(CM, m)

# ---------------------------------------------------------------- KB status row 1 (both copies)
for P in (os.path.join(HERE, "..", "..", "KB_AMALGAMATION_STATUS.md"), os.path.join(PF, "loop", "KB_AMALGAMATION_STATUS.md")):
    k = rd(P)
    OLD1 = "ALL-CAPS title UNVERIFIED;"
    NEW1 = "ALL-CAPS title → sentence case **CAPTURED-LIVE (round 327, 2026-09-15, the loop's session-4 Round 2: `header.title_casing`, `TITLECASE_OFF`; Claude 47 all-caps multi-word header titles on 47 pages / 15 modules → 0, one red flag each quoting the original)**;"
    if NEW1 not in k:
        assert k.count(OLD1) == 1, P; k = k.replace(OLD1, NEW1, 1); wr(P, k); print("KB row 1:", os.path.basename(os.path.dirname(P)))

# ---------------------------------------------------------------- gate_baseline.json
GB = os.path.join(HERE, "..", "reference", "tests", "gate_baseline.json"); raw = rd(GB); d = json.loads(raw)
d["_meta"]["build"] = "260618.98"; d["_meta"]["round"] = 327; d["_meta"]["date"] = "2026-09-15"
d["_meta"]["_round327_note"] = "Round 327 (a multi-word ALL-CAPS title renders in sentence case — the KB's title-casing rule; scoped 15-module regeneration, scoped ship #1 since the r326 full). Gate-neutral: every gate EXACT to round 326, skeleton page-for-page identical (47 pages changed text only + a cv2-note)."
wr(GB, json.dumps(d, ensure_ascii=False) + ("\n" if raw.endswith("\n") else "")); print("gate_baseline.json refreshed")

# ---------------------------------------------------------------- LOOP_STATE.md
LS = os.path.join(HERE, "..", "..", "LOOP_STATE.md"); s = rd(LS); nl = "\r\n" if "\r\n" in s[:3000] else "\n"
def L(t): return t.replace("\n", nl)
SEC = L(f"""## Session 4 · Round 2 (engine r327) — what shipped (the KB's title-casing rule)
- **Fix:** `header.title_casing` {{enabled, env TITLECASE_OFF, min_words 2, keep_tokens_with_digits true, red_flag}} — `SkeletonBuilder.#titleCasing`
  at the header title fill (plain / lowercase-span templates; the BLL phonics template untouched): a multi-word all-caps title → sentence case
  (macrons kept, digit tokens kept, single token untouched) + ONE red flag quoting the original (the KB's proper-noun caution applied to all).
- **Regeneration:** scoped — the in-memory ON probe over all 416 named 47 pages / 15 modules (= the measured population); regenerated; 0 truly
  stale; OFF vs disk on the 15 = exactly the 47 pages; ON = disk 160/160. Claude all-caps multi-word header spans 47 → 0; 47 flags.
- **Gates:** every gate EXACT (fastloop PASS, all deltas 0; full suite identical; skeleton {SK} page-for-page identical, 0 moved); 13 selftests
  GREEN; the r324 title classifier exact 550 → 567 / case-only 88 → 71. **55.1% of achievable** (unchanged). KB status row 1 → the
  ALL-CAPS normalisation CAPTURED-LIVE.
- **Plateau window:** r326 +0.057 · r327 0.000 (gate-neutral, KB-driven) — one sub-threshold round.

""")
ANCHOR = "## Session 4 · Round 2 PICK (engine r327)"
if "## Session 4 · Round 2 (engine r327) — what shipped" not in s:
    assert s.count(ANCHOR) == 1; s = s.replace(ANCHOR, SEC + ANCHOR, 1); print("LOOP_STATE section")
OLD_P = "- Session 4 Round 1 (engine r326 — a call-to-action button is an anchor, the KB's universal button form): SHIPPED 2026-09-15 ≈15:05 (session 4). AppVersion 260618.97, CLAUDE.md §9/§11/§14, KB status D-row added, FULL regeneration (scoped-ship counter reset)."
NEW_P = OLD_P + nl + "- Session 4 Round 2 (engine r327 — a multi-word ALL-CAPS title renders in sentence case, the KB's title-casing rule): SHIPPED 2026-09-15 ≈15:15 (session 4). AppVersion 260618.98, CLAUDE.md §9/§11/§14, KB status row 1 → ALL-CAPS normalisation CAPTURED-LIVE, scoped ship #1 since the r326 full. Gate-neutral."
if "- Session 4 Round 2 (engine r327" not in s:
    assert s.count(OLD_P) == 1, "position"; s = s.replace(OLD_P, NEW_P, 1); print("position")
OLD_R = "- s4-r1 (engine r326) · a call-to-action button is an anchor"
i = s.find(OLD_R); assert i > 0; j = s.find(nl, i) + len(nl)
NEW_R = f"- s4-r2 (engine r327) · a multi-word ALL-CAPS header title renders in sentence case (the KB's title-casing rule: macrons kept, code tokens kept, single token untouched, one red flag quoting the original) · SHIPPED 2026-09-15 · scoped regeneration, 47 pages / 15 modules · gate-neutral, every gate EXACT (scaffold {SK}, 0 moved) · all-caps titles 47→0, titles exact 550→567 · 55.1% of achievable · commit (see git log)" + nl
if "- s4-r2 (engine r327)" not in s:
    s = s[:j] + NEW_R + s[j:]; print("round log")
wr(LS, s); print("LOOP_STATE.md written")
