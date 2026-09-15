#!/usr/bin/env python3
"""ROUND 330 — finalise: changelog, AppVersion (260619.00 → 260619.01), CLAUDE.md §9/§11/§14, gate_baseline.json,
LOOP_STATE.md (what shipped + position + round log). Idempotent."""
import io, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)
SK_B, SK_A, RAW_B, RAW_A = "50.496", "50.536", "34.832", "34.859"

CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
ENTRY = f"""## 2026-09-15 (round 330, build 260619.01) — THE BILINGUAL SECTION ID IS THE ACTIVITY NUMBER, NOT A HEADING (KB 07B_MTK_CONTENT_PATTERNS "Activity Structure"; the autonomous loop, session 5, Round 1; **SCOPED regeneration of the 7 affected modules; skeleton +0.040pp / ≥50% +3, every other gate EXACT; scoped ship #4 since the round-326 full**)

### 1. WHAT CHANGED, IN ONE LINE

**The bilingual writer's bare section-id heading — `| [H1] 1.1 | [H1] 1.1 |`, a numbered section label with no words — no longer ships as a phantom `<h3 reo>1.1</h3><h3 eng>1.1</h3>` pair: the KB's MTK content patterns read it as the section's activity NUMBER in decimal form (`<div class="activity" number="1.1">`, "Preferred approach: use decimal format"), the finished modules carry a bare-id heading on 0 of 2,385 pages, and the round-135 keystone already opened its section on that very tag. The id is stripped from the rendered rows and, where the section is boxed and carries no `Activity NX:` label, becomes the box's `number=` as written. 25 pages / 7 modules changed; 234 phantom headings → 0, 72 unnumbered boxes → 72 numbered.**

### 2. THE EVIDENCE (docx → human → Claude)

- **TRR111 lesson 1** — docx: `| [H1] 1.1 | [H1] 1.1 |` → `| [H2] Oropuare pūrua: ia | … |` → prose → `[Activity: Embedded] Wordselect` → gold: `<h3 reo>Oropuare pūrua: ia</h3>…<div class="activity interactive" number="1.1">` and NO `1.1` heading anywhere → Claude before: `<h3 reo>1.1</h3><h3 eng>1.1</h3>` + `<div class="activity interactive">`; after: the title pair + `<div class="activity interactive" number="1.1">`.
- **PNR104 lesson 1** — docx: `| [H1] 1.1 | [H1] 1.1 |` → gold: `<div class="activity interactive" number="1.1">` → Claude before: the box unnumbered with `<h2 reo>1.1</h2><h2 eng>1.1</h2>` inside it; after: `number="1.1"`, the phantom gone.
- **TRR112 lesson 1** — docx: `| [H1] 1.1 | [H1] 1.1 |` → gold: `number="1A"` (this developer re-lettered the writer's ids) → Claude before: the phantom `1.1` + an unnumbered box; after: `number="1.1"` — the KB's stated preference over the human's letter form, NAMED (TRR112 / TRR113).
- **The KB:** `07B_MTK_CONTENT_PATTERNS` "Activity Structure" — `<div class="activity" number="1.1">`; "some finalized modules (TRR108) retain the writer's letter format … **Preferred approach: use decimal format** (1.1, 1.2, 1.3) for consistency with TRR104/TRR105 precedent."

### 3. THE MEASUREMENT (`outputs/_measure_r330_sectionid.py` → `_r330_sectionid.json`; all 454 gold dirs, the Writers Template .docx read directly — 13 TRR modules ship no parsed WT)

- The tagged `[H1] N.M` form lives ONLY in the Bilingual folder: 8 modules / 298 tagged cells (PNR101 12, PNR102 14, PNR104 14, TRR109 60, TRR110 48, TRR111 48, TRR112 50, TRR113 52); 0 in Standard / Fundamentals / Inquiry (an untagged bare `N.M` cell in a Standard WT is a maths decimal — MXFU202's `505.5` — and is NOT the signal).
- Gold on those 8: decimal `number="N.M"` on 6 (PNR101/102/104, TRR109/110/111 — 82 boxes; the writer's ids reappear as the gold's numbers on TRR111 22/24, TRR110 15/24, PNR104 7/7, PNR102 6/7) and the human's LETTER form on 2 (TRR112 39, TRR113 26); bare-id headings 0. **Share 6/8 = 0.75 ≥ 0.60, and the KB names decimal the preferred form — the two letter modules are a NAMED KB-over-gold override** (today Claude ships NO number there, so the skeleton line was already mismatched: neutral, not a dip).
- Claude before: **234 phantom section-id headings on 25 pages / 7 modules** (TRR110 has no Claude dir), **72 unnumbered activity boxes** in the family, 0 decimal numbers. After: phantoms **0**, unnumbered **0**, decimal `number=` **72**.

### 4. THE FIX — one data block `elements.dual_language.section_grouping.section_id_number` `{{ enabled, env: "REOSECID_OFF", strip_heading, number_from_section, id_pattern }}`

- `BilingualBuilder.bilingualRows` (the interleave path): the strip that already drops the `Activity NX:` label line also drops a rendered heading whose whole text matches `id_pattern` (a bare `N.M`, optional trailing colon) — `strip_heading`.
- `BilingualBuilder.bilingualSection`: a section opened by `[H1] N.M` that is boxed (has a widget) and found no `Activity NX:` label takes the section id as its `number=` — `number_from_section`; the label keeps priority (0 label modules carry `[H1] N.M`). An un-boxed prose section simply loses its phantom (the gold leaves it un-boxed and un-numbered).
- **Env toggle `REOSECID_OFF`** reverts byte-for-byte (`REONEST_OFF`, the keystone, still reverts everything above it).

### 5. THE PROOF AND THE GATES

- The in-memory probe over the whole Bilingual family (`_r330_probe.cjs`, 19 modules / 63 pages): OFF = disk 63/63; ON names **25 pages / 7 modules** and every differing line is one of three kinds — 234 phantom headings removed, 72 `<div class="activity …">` → `<div class="activity …" number="N.M">` — nothing else (`_r330_probe_on.log`). Scoped regeneration (`_r330_batches_run.sh`); `_content_manifest.py fresh --affected` → **0 truly stale**; `diff` = exactly the 25 pages, 0 added/removed; ON in memory = disk 63/63 afterwards.
- **Skeleton (PRIMARY): SCAFFOLD mean {SK_B}% → {SK_A}% (+0.040pp) IMPROVED / ≥50% 1030 → 1033 / ≥75% 196 / ≥90% 15 / skipped 0 @ 1954; RAW {RAW_B}% → {RAW_A}%.** 21 pages moved — **17 up / 4 down**, pp-sum +77.52 (TRR111_1_0 +16.52, TRR109_5_0 +10.43, TRR112_0_0 +7.84, PNR104_1_0 +7.55, PNR102_1_0 +6.85 …); the dips NAMED (`_r330_bagcheck.py`): TRR111_2_0 −6.01, PNR102_2_0 −3.73, TRR109_1_0 −0.51 are the scorer's repeat-collapse artefact — a `┌ 4× repeated:` line (two phantom + two title headings) that coincidentally matched the gold's own `4×` becomes `2×` and difflib re-aligns; position-free line overlap with the gold RISES on all three (113→121, 42→44, 131→139); TRR113_3_0 −0.81 is the named override module (gold `3A/3B/3C`, Claude `3.2/3.4/3.5`, overlap 80→74).
- Every other gate EXACT (`_fastloop_diff.py` PASS; full suite `_r330_gates.log` line-for-line identical to r329 outside the skeleton block): cs exact 11360 / EXTRA 186 / missing 591 · clean 2056/2102 / leak 288/46 · body 191 · tags 9557/9557 · flipCard TOTAL 61 divergence 0 · mtkQuiz 17 shells defect 0 · entry-parity PASS · index-sync 33/28 · **13 selftests GREEN**.
- **Ceiling:** SCAFFOLD {SK_A}% = **55.2% of achievable** (55.17).

### 6. NAMED, NOT CHASED

- The section TITLE placement (Claude renders the `[H2]` section title inside the box; the TRR111 gold puts it outside, the TRR112 gold inside — measure per module group before touching); the `Activity NX:` letter labels → decimal (KB 07B over the 5 label modules' gold letters — its own KB-over-gold measure); TRR109's own duplicate `1.1` (a human error, not chased); Claude's TRR112/TRR113 pagination (lesson-1 content on `_0_0`, a pre-existing class).

**Ledger:** scoped ship #4 since the r326 full · data `elements.dual_language.section_grouping.section_id_number` · env `REOSECID_OFF` · tools `outputs/_measure_r330_sectionid.py` (+ `_r330_sectionid.json` after, `_r330_sectionid_pre.json` before), `_r330_probe.cjs`, `_r330_bagcheck.py`, `_r330_finalise.py` · state `outputs/_r330_sk_final.json` (FRESH) · logs `_r330_gates.log`, `_r330_sk_full.log`, `_r330_fastloop.log`, `_r330_fastloop_commit.log`, `_r330_selftests.log`, `_r330_probe_off.log`, `_r330_probe_on.log`, `_r330_regen.log`, `_r330_fresh.log`, `_r330_affected.txt`, `_r330_family.txt`, `_r330_off_pages/` (the dip check).

"""
if "round 330, build 260619.01" not in s:
    assert s.startswith(head); s = head + ENTRY + s[len(head):]; wr(CL, s); print("changelog prepended")

CF = os.path.join(PF, "app", "js", "Config.js"); c = rd(CF)
OLD = '\tstatic AppVersion = "260619.00";\n'
NEW = ('\t// ROUND 330 (2026-09-15, build 260619.01): the bilingual section id is the activity NUMBER, not a heading\n'
       '\t// (KB 07B "Activity Structure": <div class="activity" number="1.1">, decimal preferred) — the phantom\n'
       '\t// <h3 reo>1.1</h3><h3 eng>1.1</h3> pair no longer ships (234 -> 0) and the boxed section carries the\n'
       '\t// writer\'s own id as number= (72 boxes; 25 pages / 7 modules, scoped). Env REOSECID_OFF; data\n'
       '\t// elements.dual_language.section_grouping.section_id_number. Skeleton +0.040pp, >=50% +3.\n'
       '\tstatic AppVersion = "260619.01";\n')
if '"260619.01"' not in c:
    assert c.count(OLD) == 1; c = c.replace(OLD, NEW, 1); wr(CF, c); print("AppVersion bumped")

CM = os.path.join(PF, "CLAUDE.md"); m = rd(CM)
OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 329 BASELINE (`[trigger engagement]` is a marker, not a button; scoped)"
NEW9 = (f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 330 BASELINE (the bilingual section id is the activity number, not a heading — KB 07B; scoped): SCAFFOLD mean {SK_A}% / >=50% 1033 / >=75% 196 / >=90% 15 / skipped 0 @ 1954; RAW {RAW_A}%** (state `outputs/_r330_sk_final.json`, FRESH). r330 +0.040 (21 moved, 17 up; dips NAMED TRR111_2_0 −6.01 / PNR102_2_0 −3.73 / TRR109_1_0 −0.51 = the scorer's repeat-collapse artefact with position-free overlap RISING on each, TRR113_3_0 −0.81 = the named KB-over-gold letter→decimal override). Older r329 text: **ROUND 329 BASELINE (`[trigger engagement]` is a marker, not a button; scoped)")
if "ROUND 330 BASELINE" not in m:
    assert m.count(OLD9) == 1, "§9"; m = m.replace(OLD9, NEW9, 1); print("§9")
ROW = ("| `REOSECID_OFF` | 330 | **THE BILINGUAL SECTION ID IS THE ACTIVITY NUMBER, NOT A HEADING** (KB 07B_MTK_CONTENT_PATTERNS \"Activity Structure\" — `<div class=\"activity\" number=\"1.1\">`, decimal preferred; the autonomous loop's session-5 Round 1; **SCOPED regeneration of the 7 affected modules; scoped ship #4 since the r326 full**). Reverts byte-for-byte. ON (default), `elements.dual_language.section_grouping.section_id_number`: `BilingualBuilder.bilingualRows`' interleave strip (the seam that already drops the `Activity NX:` label line) also drops a rendered heading whose whole text is a bare `N.M` section id (`strip_heading`, `id_pattern`); `bilingualSection`, when the section was opened by `[H1] N.M`, is boxed and found no `Activity NX:` label, numbers the box with the section id as written (`number_from_section`). MEASURED over all 454 gold dirs (the .docx read directly): the tagged `[H1] N.M` form lives ONLY in the Bilingual folder (8 modules / 298 cells); the gold numbers the boxed section with the writer's decimal id on 6 of the 8 (PNR101/102/104, TRR109/110/111) and re-letters it on 2 (TRR112/113 — the KB's preference overrides, NAMED); a bare-id heading on 0 of 2,385 gold pages. Claude phantom `<h3 reo>1.1</h3><h3 eng>1.1</h3>` pairs 234 → 0; unnumbered family boxes 72 → 0 (72 decimal numbers). 25 pages / 7 modules changed. Skeleton +0.040pp (≥50% +3; 17 up / 4 down, dips named as the scorer's repeat-collapse artefact + the override module); every other gate EXACT; 13 selftests GREEN. |\n")
if "| `REOSECID_OFF` | 330 |" not in m:
    A = "| `ENGMARKER_OFF` | 329 |"; assert m.count(A) == 1, "§11"; m = m.replace(A, ROW + A, 1); print("§11")
B14 = (f"- **Build:** `260619.01` (round 330 — **the bilingual section id is the activity number, not a heading** (KB 07B; the autonomous loop's session-5 Round 1; **SCOPED regeneration of 7 modules; scoped ship #4 since the r326 full**). **ROUND 330 BASELINE: SCAFFOLD mean {SK_A}% / ≥50% 1033 / ≥75% 196 / ≥90% 15 / skipped 0 @ 1954; RAW {RAW_A}%** (state `outputs/_r330_sk_final.json`, FRESH) = **55.2% of achievable** (ceiling 91.6%). Every other gate EXACT: cs exact **11360** / EXTRA **186** / missing **591** · clean **2056/2102** / leak **288/46** · body **191** · tags **9557/9557** · flipCard TOTAL 61 divergence 0 · index-sync 33/28 · entry-parity PASS · mtkQuiz shell defect 0 · all THIRTEEN selftests GREEN. Corpus 2102 pages / 413 modules, 0-stale, **25 pages / 7 modules changed, 0 added/removed**; toggle `REOSECID_OFF`; data `elements.dual_language.section_grouping.section_id_number`. Phantom section-id headings 234 → 0; unnumbered Bilingual boxes 72 → 0. **Plateau window restarted this session: r330 +0.040.**)\n")
if "- **Build:** `260619.01` (round 330" not in m:
    A = "- **Build:** `260619.00` (round 329 —"; assert m.count(A) == 1, "§14"; m = m.replace(A, B14 + A, 1); print("§14")
wr(CM, m)

# ---------------------------------------------------------------- gate_baseline.json
GB = os.path.join(HERE, "..", "reference", "tests", "gate_baseline.json"); raw = rd(GB); d = json.loads(raw)
d["_meta"]["build"] = "260619.01"; d["_meta"]["round"] = 330; d["_meta"]["date"] = "2026-09-15"
d["skeleton"].update({"mean_scaffold_pct": float(SK_A), "raw_mean_pct": float(RAW_A), "pages_ge_50": 1033})
d["_meta"]["_round330_note"] = f"Round 330 (the bilingual section id is the activity number, not a heading — KB 07B; scoped 7-module regeneration, scoped ship #4 since the r326 full). Skeleton {SK_B}->{SK_A} (+0.040pp; 21 moved, 17 up; >=50 1030->1033; dips named as the scorer's repeat-collapse artefact + the TRR112/113 KB-over-gold override); every other gate EXACT."
wr(GB, json.dumps(d, ensure_ascii=False) + ("\n" if raw.endswith("\n") else "")); print("gate_baseline.json refreshed")

# ---------------------------------------------------------------- LOOP_STATE.md
LS = os.path.join(HERE, "..", "..", "LOOP_STATE.md"); s = rd(LS); nl = "\r\n" if "\r\n" in s[:3000] else "\n"
def L(t): return t.replace("\n", nl)
SEC = L(f"""## Session 5 · Round 1 (engine r330) — what shipped (the bilingual section id is the activity number, not a heading)
- **Fix:** `elements.dual_language.section_grouping.section_id_number` {{enabled, env REOSECID_OFF, strip_heading, number_from_section, id_pattern}}
  in `BilingualBuilder`: the interleave strip drops a rendered heading whose whole text is a bare `N.M`; a `[H1] N.M`-opened boxed section with no
  `Activity NX:` label takes the id as its `number=`.
- **Regeneration:** scoped — the in-memory probe over the whole Bilingual family (19 modules / 63 pages) named 25 pages / 7 modules; OFF = disk
  63/63; every diff line = 234 phantom headings out + 72 boxes numbered; regenerated; 0 truly stale; manifest diff = exactly the 25; ON = disk 63/63.
- **Gates:** skeleton {SK_B} → {SK_A} (+0.040pp; 21 moved, 17 up / 4 down — dips NAMED TRR111_2_0 −6.01, PNR102_2_0 −3.73, TRR109_1_0 −0.51 = the
  scorer's repeat-collapse artefact (position-free overlap with the gold RISES on each), TRR113_3_0 −0.81 = the named letter→decimal override);
  ≥50 1030 → 1033; every other gate line-for-line EXACT with r329; 13 selftests GREEN. **55.2% of achievable.**
- **Verifier:** `_measure_r330_sectionid.py` after → phantoms 0 / unnumbered 0 / decimal 72. **Plateau window: r330 +0.040 (restarted).**

""")
ANCHOR = "## Session 5 · Round 1 PICK (engine r330)"
if "## Session 5 · Round 1 (engine r330) — what shipped" not in s:
    assert s.count(ANCHOR) == 1; s = s.replace(ANCHOR, SEC + ANCHOR, 1); print("LOOP_STATE section")
OLD_P = "- Session 4 Round 4 (engine r329 — `[trigger engagement]` is a marker, not a button, KB constraint 43): SHIPPED 2026-09-15 ≈15:45 (session 4). AppVersion 260619.00, CLAUDE.md §9/§11/§14, scoped ship #3 since the r326 full. **THE LOOP STOPPED after it (plateau rule: r327 0.000 / r328 0.000 / r329 +0.004).**"
NEW_P = OLD_P + nl + "- Session 5 Round 1 (engine r330 — the bilingual section id is the activity number, not a heading, KB 07B): SHIPPED 2026-09-15 ≈16:40 (session 5). AppVersion 260619.01, CLAUDE.md §9/§11/§14, KB status D-row added, scoped ship #4 since the r326 full. Skeleton +0.040pp — the plateau window restarts."
if "- Session 5 Round 1 (engine r330" not in s:
    assert s.count(OLD_P) == 1, "position"; s = s.replace(OLD_P, NEW_P, 1); print("position")
OLD_R = "- s4-r4 (engine r329) · `[trigger engagement]` is a marker, not a button"
i = s.find(OLD_R); assert i > 0; j = s.find(nl, i) + len(nl)
NEW_R = f"- s5-r1 (engine r330) · the bilingual section id is the activity number, not a heading (KB 07B: the writer's bare `[H1] N.M` → `number=\"N.M\"` on the boxed section, decimal preferred; the phantom `<h3>1.1</h3>` pair no longer ships) · SHIPPED 2026-09-15 · scoped regeneration, 25 pages / 7 modules · scaffold {SK_B}→{SK_A} (+0.040; 17 up / 4 down, dips named), ≥50 +3, every other gate EXACT · phantoms 234→0, unnumbered boxes 72→0 · 55.2% of achievable · commit (see git log)" + nl
if "- s5-r1 (engine r330)" not in s:
    s = s[:j] + NEW_R + s[j:]; print("round log")
wr(LS, s); print("LOOP_STATE.md written")
