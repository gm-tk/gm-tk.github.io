#!/usr/bin/env python3
"""ROUND 331 — finalise: changelog, AppVersion (260619.01 → 260619.02), CLAUDE.md §9/§11/§14, gate_baseline.json,
LOOP_STATE.md (what shipped + position + round log; the PICK timestamp corrected). Idempotent."""
import io, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)
SK_B, SK_A, RAW_B, RAW_A = "50.536", "50.558", "34.859", "34.881"

CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
ENTRY = f"""## 2026-09-15 (round 331, build 260619.02) — A BILINGUAL SECTION BOX'S HEADINGS RENDER AT THE KB'S ACTIVITY LEVEL (KB 07B_MTK_CONTENT_PATTERNS "Activity Structure" + 05B activities; the autonomous loop, session 5, Round 2; **SCOPED regeneration of the 5 affected modules; skeleton +0.022pp / ≥50% +1, every other gate EXACT; scoped ship #5 since the round-326 full**)

### 1. WHAT CHANGED, IN ONE LINE

**Inside a bilingual (TRR-dialect) section box the writer's `[H2]` heading now renders at h3 — the KB's activity heading level (`<h3 reo>…</h3><h3 eng>…</h3>`) — instead of the writer's h2: the round-55 re-leveller excludes activity-anchored headings from its pool (right for the Standard template, whose `[Activity]` box title is the writer's `[H3]`), but the round-135 keystone box opens on `[H1] N.M` with the writer's `[H2]` section title inside it, so Claude kept h2 there. 157 headings on 21 pages / 5 modules; Claude's TRR in-box h2 155 → 0. The PNR dialect (its own gold keeps h2) is excluded by data.**

### 2. THE EVIDENCE (docx → human → Claude)

- **TRR111 lesson 1 §1.2** — docx: `| [H2] The sound: ia | [H2] Te oro: ia |` inside the boxed section → gold: `<h3 reo>Te oro: ia</h3><h3 eng>The sound: ia</h3>` inside `number="1.2"` → Claude before: `<h2 reo>Te oro: ia</h2><h2 eng>The sound: ia</h2>`; after: the gold's h3 pair.
- **TRR112 lesson 1 §1.3** — docx `[H2] The sound: oa` → gold `<h3 reo>Te oro: oa</h3>` inside `number="1C"` → Claude after: h3.
- **The KB:** 07B "Activity Structure" — `<div class="activity" number="1.1"> … <h3 reo>…</h3><h3 eng>…</h3>`; 05B "Activities" — the box's title at `<h3>`.

### 3. THE MEASUREMENT (an inline census over the whole Bilingual family: reo/eng headings INSIDE an activity box, gold vs Claude)

- Gold on the 8 writer-id modules: **h3 348 / h2 42** (0.89; the box's FIRST heading h3 117 : h2 21 = 0.85); TRR109/110/111/112/113 carry **0** in-box h2; the label-form family (TRR102/108/114/203/301) is h3/h4 only, and Claude already ships h3 there. **The 42 gold h2 are the PNR family** (PNR101 12 / PNR102 12 / PNR104 14 — the newer "Te Aka Taumatua" MTK template whose `[H1] Lesson Title:` section row the gold keeps at h2, 0.72; 07B does not describe that dialect → its own gold governs, LOOP §1b level 3) → `exclude_code_prefixes: ["PNR"]`.
- Claude before: in-box **h2 211 / h3 24** (TRR ≈ 155 + PNR 56). After (the round's verifier, the same census): TRR in-box **h2 0**, h3 209 (the 10 TRR108 h5 are a separate, pre-existing item).
- **How this PICK was found:** the new corpus-wide instrument `outputs/_measure_r331_skelgaps.py` (the PRIMARY gate's own difflib opcodes tallied per template — which skeleton lines are most often missing / extra). Its larger signals were KB-checked and set aside on the record: `iframe.embed-responsive-item` + `videoSection.icon` (the KB's canonical embed is what Claude ships; the KB is silent on `icon`), the table class `table-bordered` (a KB-internal conflict 05D vs 06 §6 + a Standard gold tie 0.51 → needs Chris), and the activity image sidebar `alertImage` (388 gold sidebars, Claude 0 → MEASURED DECLINE: 56% of the sidebar images are absent from the writer's document, the derivable signal predicts at 0.13; `_measure_r331_alertimage.py`, `_r331_alertimage_pos.py`).

### 4. THE FIX — one data block `elements.dual_language.section_grouping.boxed_heading_level` `{{ enabled, env: "REOBOXH_OFF", from_level: 2, to_level: 3, exclude_code_prefixes: ["PNR"] }}`

- `BilingualBuilder.boxedHeadingRelevel(html, run)`: when a section is BOXED, every `<h2 …>` / `</h2>` open-close pair in the gathered inner HTML becomes h3; h1 and h3+ untouched (the gold keeps the writer's `[H3]` at h3). Called from `bilingualSection` at the box emit; an un-boxed section is untouched (its headings already re-level to h3 outside).
- **Env toggle `REOBOXH_OFF`** reverts byte-for-byte.

### 5. THE PROOF AND THE GATES

- The in-memory probe over the whole Bilingual family (`_r331_probe.cjs`, 19 modules / 63 pages): OFF = disk 63/63; ON names **21 pages / 5 modules** (TRR109/111/112/113 + TRR301's 2) and every differing line is a `<h2 reo|eng>` → `<h3 …>` pair — **157 lines, nothing else** (`_r331_probe_on.log`); PNR untouched. Scoped regeneration (`_r331_batches_run.sh`); `_content_manifest.py fresh --affected` → **0 truly stale**; `diff` = exactly the 21 pages, 0 added/removed; ON in memory = disk 63/63 afterwards.
- **Skeleton (PRIMARY): SCAFFOLD mean {SK_B}% → {SK_A}% (+0.022pp) IMPROVED / ≥50% 1033 → 1034 / ≥75% 196 / ≥90% 15 / skipped 0 @ 1954; RAW {RAW_B}% → {RAW_A}%.** 21 pages moved — **18 up / 3 down**, pp-sum +42.72 (TRR111_4_0 +8.10, TRR111_2_0 +6.01 — its r330 alignment dip reversed exactly, TRR111_1_0 +5.36, TRR113_5_0 +4.82 …); the dips NAMED (`_r331_bagcheck.py`): TRR113_0_0 −6.25, TRR109_3_0 −4.38, TRR112_0_0 −2.61 — the scorer's alignment artefact, position-free line overlap with the gold RISING on all three (89→91, 88→92, 96→99).
- Every other gate EXACT (`_fastloop_diff.py` PASS; full suite `_r331_gates.log` line-for-line identical to r330 outside the skeleton block): cs exact 11360 / EXTRA 186 / missing 591 · clean 2056/2102 / leak 288/46 · body 191 · tags 9557/9557 · flipCard TOTAL 61 divergence 0 · mtkQuiz 17 shells defect 0 · entry-parity PASS · index-sync 33/28 · **13 selftests GREEN**.
- **Ceiling:** SCAFFOLD {SK_A}% = **55.2% of achievable** (55.19).

### 6. NAMED, NOT CHASED

- TRR108's in-box h5 (10) and the PNR dialect's own defects (the `[H1] TRR900` module-code rows rendered as headings, the `Lesson Title:` label prefix kept) — 3 modules / 8 pages, under the floor; the table-class KB conflict and the `alertImage` decline are recorded in `LOOP_STATE.md`.

**Ledger:** scoped ship #5 since the r326 full · data `elements.dual_language.section_grouping.boxed_heading_level` · env `REOBOXH_OFF` · tools `outputs/_measure_r331_skelgaps.py` (+ `_r331_skelgaps.json`), `_measure_r331_alertimage.py` + `_r331_alertimage_pos.py` (+ `_r331_alertimage.json`), `_measure_r331_reotitle.py`, `_r331_probe.cjs`, `_r331_bagcheck.py`, `_r331_finalise.py` · state `outputs/_r331_sk_final.json` (FRESH) · logs `_r331_gates.log`, `_r331_sk_full.log`, `_r331_fastloop.log`, `_r331_fastloop_commit.log`, `_r331_selftests.log`, `_r331_probe_on.log`, `_r331_regen.log`, `_r331_fresh.log`, `_r331_affected.txt`, `_r331_off_pages/` (the dip check).

"""
if "round 331, build 260619.02" not in s:
    assert s.startswith(head); s = head + ENTRY + s[len(head):]; wr(CL, s); print("changelog prepended")

CF = os.path.join(PF, "app", "js", "Config.js"); c = rd(CF)
OLD = '\tstatic AppVersion = "260619.01";\n'
NEW = ('\t// ROUND 331 (2026-09-15, build 260619.02): a bilingual section box\'s [H2] heading renders at the KB\'s\n'
       '\t// activity level h3 (07B "Activity Structure"), not the writer\'s h2 — 157 headings on 21 pages / 5 TRR\n'
       '\t// modules, scoped; the PNR dialect keeps its own gold\'s h2 (data-excluded). Env REOBOXH_OFF; data\n'
       '\t// elements.dual_language.section_grouping.boxed_heading_level. Skeleton +0.022pp, >=50% +1.\n'
       '\tstatic AppVersion = "260619.02";\n')
if '"260619.02"' not in c:
    assert c.count(OLD) == 1; c = c.replace(OLD, NEW, 1); wr(CF, c); print("AppVersion bumped")

CM = os.path.join(PF, "CLAUDE.md"); m = rd(CM)
OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 330 BASELINE (the bilingual section id is the activity number, not a heading — KB 07B; scoped)"
NEW9 = (f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 331 BASELINE (a bilingual section box's headings render at the KB's activity level — KB 07B; scoped): SCAFFOLD mean {SK_A}% / >=50% 1034 / >=75% 196 / >=90% 15 / skipped 0 @ 1954; RAW {RAW_A}%** (state `outputs/_r331_sk_final.json`, FRESH). r331 +0.022 (21 moved, 18 up; dips NAMED TRR113_0_0 −6.25 / TRR109_3_0 −4.38 / TRR112_0_0 −2.61 = the scorer's alignment artefact, position-free overlap rising on each). Older r330 text: **ROUND 330 BASELINE (the bilingual section id is the activity number, not a heading — KB 07B; scoped)")
if "ROUND 331 BASELINE" not in m:
    assert m.count(OLD9) == 1, "§9"; m = m.replace(OLD9, NEW9, 1); print("§9")
ROW = ("| `REOBOXH_OFF` | 331 | **A BILINGUAL SECTION BOX'S HEADINGS RENDER AT THE KB'S ACTIVITY LEVEL** (KB 07B_MTK_CONTENT_PATTERNS \"Activity Structure\" + 05B — `<h3 reo>…</h3><h3 eng>…</h3>` inside the box; the autonomous loop's session-5 Round 2; **SCOPED regeneration of the 5 affected modules; scoped ship #5 since the r326 full**). Reverts byte-for-byte. ON (default), `elements.dual_language.section_grouping.boxed_heading_level`: `BilingualBuilder.boxedHeadingRelevel` re-levels every `<h{from_level}>` open/close tag in a BOXED section's gathered inner HTML to `to_level` (h2 → h3; h1 and h3+ untouched — the gold keeps the writer's `[H3]` at h3); an un-boxed section is untouched; `exclude_code_prefixes` (`PNR` — the newer MTK dialect whose `[H1] Lesson Title:` row its own gold keeps at h2, 0.72; 07B does not describe it). MEASURED (in-box reo/eng headings over the Bilingual family): gold h3 348 / h2 42 (0.89; the 42 = PNR), TRR modules 0 in-box h2; Claude h2 211 / h3 24 → TRR in-box h2 155 → 0. 157 headings on 21 pages / 5 modules changed. Skeleton +0.022pp (≥50% +1; 18 up / 3 down, dips named as alignment artefacts); every other gate EXACT; 13 selftests GREEN. |\n")
if "| `REOBOXH_OFF` | 331 |" not in m:
    A = "| `REOSECID_OFF` | 330 |"; assert m.count(A) == 1, "§11"; m = m.replace(A, ROW + A, 1); print("§11")
B14 = (f"- **Build:** `260619.02` (round 331 — **a bilingual section box's headings render at the KB's activity level** (KB 07B; the autonomous loop's session-5 Round 2; **SCOPED regeneration of 5 modules; scoped ship #5 since the r326 full**). **ROUND 331 BASELINE: SCAFFOLD mean {SK_A}% / ≥50% 1034 / ≥75% 196 / ≥90% 15 / skipped 0 @ 1954; RAW {RAW_A}%** (state `outputs/_r331_sk_final.json`, FRESH) = **55.2% of achievable** (ceiling 91.6%). Every other gate EXACT: cs exact **11360** / EXTRA **186** / missing **591** · clean **2056/2102** / leak **288/46** · body **191** · tags **9557/9557** · flipCard TOTAL 61 divergence 0 · index-sync 33/28 · entry-parity PASS · mtkQuiz shell defect 0 · all THIRTEEN selftests GREEN. Corpus 2102 pages / 413 modules, 0-stale, **21 pages / 5 modules changed, 0 added/removed**; toggle `REOBOXH_OFF`; data `elements.dual_language.section_grouping.boxed_heading_level`. TRR in-box h2 headings 155 → 0. **Plateau window: r330 +0.040 · r331 +0.022.**)\n")
if "- **Build:** `260619.02` (round 331" not in m:
    A = "- **Build:** `260619.01` (round 330 —"; assert m.count(A) == 1, "§14"; m = m.replace(A, B14 + A, 1); print("§14")
wr(CM, m)

GB = os.path.join(HERE, "..", "reference", "tests", "gate_baseline.json"); raw = rd(GB); d = json.loads(raw)
d["_meta"]["build"] = "260619.02"; d["_meta"]["round"] = 331; d["_meta"]["date"] = "2026-09-15"
d["skeleton"].update({"mean_scaffold_pct": float(SK_A), "raw_mean_pct": float(RAW_A), "pages_ge_50": 1034})
d["_meta"]["_round331_note"] = f"Round 331 (a bilingual section box's headings render at the KB's activity level h3 — KB 07B; scoped 5-module regeneration, scoped ship #5 since the r326 full). Skeleton {SK_B}->{SK_A} (+0.022pp; 21 moved, 18 up; >=50 1033->1034; dips named as alignment artefacts); every other gate EXACT."
wr(GB, json.dumps(d, ensure_ascii=False) + ("\n" if raw.endswith("\n") else "")); print("gate_baseline.json refreshed")

LS = os.path.join(HERE, "..", "..", "LOOP_STATE.md"); s = rd(LS); nl = "\r\n" if "\r\n" in s[:3000] else "\n"
def L(t): return t.replace("\n", nl)
s = s.replace("## Session 5 · Round 2 PICK (engine r331) — written before any code, 2026-09-15 17:35 NZST", "## Session 5 · Round 2 PICK (engine r331) — written before any code, 2026-09-15 16:50 NZST")
SEC = L(f"""## Session 5 · Round 2 (engine r331) — what shipped (a bilingual section box's headings render at the KB's activity level)
- **Fix:** `elements.dual_language.section_grouping.boxed_heading_level` {{enabled, env REOBOXH_OFF, from_level 2, to_level 3, exclude_code_prefixes
  [PNR]}}: `BilingualBuilder.boxedHeadingRelevel` moves every `<h2>` open/close pair inside a BOXED section's inner HTML to h3; un-boxed sections
  and h1 / h3+ untouched; PNR excluded (its own gold keeps h2).
- **Regeneration:** scoped — the in-memory probe over the whole Bilingual family (19 modules / 63 pages) named 21 pages / 5 modules (TRR109/111/
  112/113 + TRR301's 2 lines); OFF = disk 63/63; every diff line = 157 `<h2 reo|eng>` → `<h3>`; regenerated; 0 truly stale; manifest diff =
  exactly the 21; ON = disk 63/63.
- **Gates:** skeleton {SK_B} → {SK_A} (+0.022pp; 21 moved, 18 up / 3 down — dips NAMED TRR113_0_0 −6.25, TRR109_3_0 −4.38, TRR112_0_0 −2.61 =
  the scorer's alignment artefact, position-free overlap RISING on each; TRR111_2_0's r330 dip reversed exactly); ≥50 1033 → 1034; every
  other gate line-for-line EXACT with r330; 13 selftests GREEN. **55.2% of achievable.**
- **Verifier:** the in-box census after → TRR in-box h2 0 (h3 209). **Plateau window: r330 +0.040 · r331 +0.022.**

""")
ANCHOR = "## Session 5 · Round 2 PICK (engine r331)"
if "## Session 5 · Round 2 (engine r331) — what shipped" not in s:
    assert s.count(ANCHOR) == 1; s = s.replace(ANCHOR, SEC + ANCHOR, 1); print("LOOP_STATE section")
OLD_P = "- Session 5 Round 1 (engine r330 — the bilingual section id is the activity number, not a heading, KB 07B): SHIPPED 2026-09-15 ≈16:40 (session 5). AppVersion 260619.01, CLAUDE.md §9/§11/§14, KB status D-row added, scoped ship #4 since the r326 full. Skeleton +0.040pp — the plateau window restarts."
NEW_P = OLD_P + nl + "- Session 5 Round 2 (engine r331 — a bilingual section box's headings render at the KB's activity level h3, KB 07B): SHIPPED 2026-09-15 ≈17:10 (session 5). AppVersion 260619.02, CLAUDE.md §9/§11/§14, scoped ship #5 since the r326 full. Skeleton +0.022pp."
if "- Session 5 Round 2 (engine r331" not in s:
    assert s.count(OLD_P) == 1, "position"; s = s.replace(OLD_P, NEW_P, 1); print("position")
OLD_R = "- s5-r1 (engine r330) · the bilingual section id is the activity number"
i = s.find(OLD_R); assert i > 0; j = s.find(nl, i) + len(nl)
NEW_R = f"- s5-r2 (engine r331) · a bilingual section box's headings render at the KB's activity level (KB 07B: the writer's `[H2]` inside a TRR section box → h3; PNR excluded by data) · SHIPPED 2026-09-15 · scoped regeneration, 21 pages / 5 modules · scaffold {SK_B}→{SK_A} (+0.022; 18 up / 3 down, dips named), ≥50 +1, every other gate EXACT · TRR in-box h2 155→0 · alertImage sidebar DECLINED, table-class KB conflict → needs Chris · 55.2% of achievable · commit (see git log)" + nl
if "- s5-r2 (engine r331)" not in s:
    s = s[:j] + NEW_R + s[j:]; print("round log")
old_h = "**Session 5 so far: r330 (Bilingual section-id numbers, scoped, +0.040pp — the plateau window restarts) · SHIPPED ≈16:45.**"
new_h = "**Session 5 so far: r330 (Bilingual section-id numbers, scoped, +0.040pp — the plateau window restarts; commit 0e068c6) · r331 (Bilingual in-box heading level, scoped, +0.022pp) · SHIPPED ≈17:10.**"
if old_h in s: s = s.replace(old_h, new_h, 1); print("header")
wr(LS, s); print("LOOP_STATE.md written")
