#!/usr/bin/env python3
"""ROUND 357 (loop session 19 Round 1 — the #module-code chip's presence follows the family's own convention on both page
types: six no-evidence registry values corrected + the template_deltas tier) — finalise: changelog, AppVersion
(260619.27 → 260619.28), CLAUDE.md §9 / §11 / §14, gate_baseline.json, loop/README.md rows. Idempotent; LF via wr()."""
import io, os, json
ROOT = r"C:\Users\Gavin\TeKura\FINAL_MODULE_DATA"
PF = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)

CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)" + chr(10) + chr(10)
ENTRY = """## 2026-09-17 (round 357, build 260619.28) — THE `#module-code` CHIP'S PRESENCE FOLLOWS THE FAMILY'S OWN CONVENTION ON BOTH PAGE TYPES: six no-evidence registry values corrected (PNR / SCFUN / CEDT2 / CEDT3 / OSSC / CEDK5, the r336 shape) + a NEW `template_deltas` cascade tier for the levels that hold two template families (BLL1's seven Inquiry parents beside 56 Standard children, CEDO1, EXPFUN) — the autonomous loop's session-19 Round 1, the DIFF MINER's first chrome class (DIFF_QUEUE F15 / F14); **SCOPED regeneration of the 89-module family (6 batches, all rc 0), 18 modules / 36 pages changed; skeleton SCAFFOLD 51.982 → 52.013 % (+0.031pp; 37 movers, 35 up, the 2 dips named), ≥50 1092 → 1094, every other gate EXACT; scoped ship #1 since the r356 full**

### 1. WHAT CHANGED, IN ONE LINE

**Eighteen modules shipped the header chip the wrong way round from their own family's gold — nine lacked it where every sibling's gold carries it (OSSC401 / OSSC501 lessons `01`, PNR101 / 102 / 104 lessons, CEDT207 / CEDT301 lessons `N.0`, CEDT301 / EXPFUN07 / SCFUN01 overviews), nine shipped it where the family's gold has none (the BLL110–170 Inquiry parents' `00`, CEDK501, CEDO102) — because the mined registry value was a no-evidence marker (`—` / `(empty)`, omitted with a warn note), a default the family never had, or a level delta mined from the OTHER template family sharing that level. The registry now says what the golds say, and a level can say two things when it holds two templates.**

### 2. THE EVIDENCE (docx → human → Claude)

- **OSSC401 lesson 1** — WT `[LESSON 1] What are online scams?`; gold `<div id="module-code"><h1>01</h1></div><h1><span>What are online scams?</span></h1>` + the menu button + menu; Claude before: the title h1 ALONE (registry OSSC `base_rules.module_code.lesson = "—"`, the OSSC3 delta's `decimal` reaching only OSSC301); after: `<h1>01</h1>` chip + title (the KB's padded form, constraint 16 / 01A; the gold's 9/9).
- **PNR101 lesson 1** — gold `<div id="module-code"><h1>01</h1></div>` then the Māori / English h1 pair; Claude before: the pair alone (the TMoA subject tier's `—`); after: the chip + the pair (07C §12: the chip on every MTK page; PNR102 / PNR104's golds read the full code on lesson pages — a FORM difference, recorded, gate-invisible, KB row 16).
- **BLL110 overview** — gold `<div id="header"><h1><span>…` with NO chip (6 of the 7 BLL1 parents; BLL170 the exception); Claude before: `<div id="module-code"><h1>00</h1></div>` first (the BLL1 level delta `padded-number`, mined from the 56 Standard children); after: no chip — the children (BLL111 … BLL177) untouched, `01` on every lesson as before.
- **CEDT301 lesson 2** — gold `<h1>2.0</h1>` chip; Claude before none (`(empty)`); after `2.0`. **CEDK501 / CEDO102 overview** — gold no chip; Claude before `CEDK501` / `CEDO102` (the `defaults` tier's `full-code`); after none. **EXPFUN07 (Standard) overview** — gold `EXPFUN07`; the five Inquiry EXPFUNs' golds none — after: the chip on EXPFUN07 only.

### 3. THE MEASUREMENT (before coding — `outputs/_measure_r357_chip.py` → `_r357_chip.{json,log}` over the gate's own 1955 pairs / 409 modules, resolved values from `_r336_resolve_all.cjs` → `_r357_resolved.json`)

- **The queue:** `DIFF_QUEUE.md` (Round 0c, the diff miner) ranks the module-code region first — chrome fact F15 `header:chip` MISSING 11 modules / 30 pages (gold 0.97) and F14 EXTRA 12 modules (gold 0.03 for Claude's form). Re-measured per (template, base, level, page-type) group: **11 CLASS groups / 18 modules / 36 pages** where the gold's presence solidifies (≥ 0.60 — every group ≥ 0.86, most unanimous) and Claude disagrees on ≥ 0.50 of the group's pages: PNR1 lesson 1.00 (5 pages), SCFUN0 overview 1.00, CEDT2 lesson 1.00 (6), CEDT3 lesson 1.00 (5) + overview 1.00, EXPFUN0 Standard overview 1.00, OSSC4 / OSSC5 lesson 1.00 (9); the EXTRA half BLL1 Inquiry overview absent 0.86 (7 modules), CEDK5 overview absent 1.00, CEDO1 Inquiry overview absent 1.00. Partials named, not chased: HPFUN201 / HPFUN302 / SSFUN01 / XFUN01 (a gold-absent singleton in a present-majority family), EXBP901 / EXIP901 lessons (gold 1 of 4 present, Claude agrees with the majority).
- **§1b authority:** KB level 1 for the MISSING half — 01A 'Overview Page (-00) Header' / 'Lesson Page Header' (the chip on both), 07C §12 (MTK: the chip on every page), constraint 16; the KB is SILENT on the Inquiry / Fundamentals overview chip (06 §3.3 / §3.4 — r336's finding), so the EXTRA half follows the family's own gold (level 2 / 3). Only PRESENCE is in play: the chip's text FORM (`1.0` vs `01`) is KB-status row 16's settled PARTIAL (CL-0069 deliberately did not codify the padding) and the skeleton strips text.

### 4. THE MECHANISM (DATA OVER CODE — `data/Style_Anchor_Registry.json` + 27 lines in `ModuleResolver.Resolve`; `outputs/_r357_splice.py`)

- **Six registry corrections (the r263 / r285 / r332 / r336 precedent):** `PNR.base_rules.module_code = {overview: full-code, lesson: padded-number}`; `SCFUN.base_rules.module_code = {full-code, padded-number}`; `CEDT2.delta.module_code = {absent, decimal}`; `CEDT3.delta.module_code = {full-code, decimal}`; `OSSC.base_rules.module_code.lesson = padded-number` (OSSC3's own `decimal` delta untouched); `CEDK5.delta.module_code = {absent, decimal}`; `EXPFUN.base_rules.module_code = {absent, decimal}` (explicit instead of the `—` omission — byte-identical output on EXPFUN02–06).
- **The `template_deltas` tier (`_meta.template_deltas` {enabled, env `TMPLDELTA_OFF`, source}; `_how_to_edit.template_override`):** at a base or a level, `{"<template_type>": {field: value}}` — Standard / Inquiry / Fundamentals / Bilingual — overlaid AFTER the level delta when `Module_Structure_Index.module_meta[code].template_type` is known (the index Resolve already reads for the evidence floor); a module the index does not know gets no template delta and keeps the level's value, exactly as before. Pattern fields resolve as whole objects; unknown literals are skipped (`#overlayRules`); the resolution path gains `template <type>`. Used by `BLL1.template_deltas.Inquiry.module_code = {absent, padded-number}`, `CEDO1.template_deltas.Inquiry.module_code = {absent, decimal}`, `EXPFUN.template_deltas.Standard.module_code = {full-code, decimal}`. The same tier is the carrier for the queue's other mixed-level classes (F37 / F38 — the BLL Standard children's `footer-nav inquiry-nav`).

### 5. THE PROOF

- **The resolved-rules dump of ALL 416 before / after (`_r357_resolved.json` → `_r357_resolved_after.json`):** `module_code` changed on exactly 28 modules — the 18 class modules, the four CEDT2 revision briefs (same level, out of the gate population, unchanged bytes) and the five Inquiry EXPFUNs (explicit `absent`, unchanged bytes) — and **no other field on any module**; `TMPLDELTA_OFF=1` (`_r357_resolved_off.json`) reverts exactly the nine template-delta modules (BLL110–170, CEDO102, EXPFUN07) to the level's value.
- **Regeneration (`_r357_regen_par.sh`, the 89-module family = every member of every edited tier: BLL1 63 / CEDT 11 / CEDK 3 / CEDO 6 / EXPFUN 6 / PNR 3 / OSSC 3 / SCFUN 1; 6 batches, all rc 0, 45 s):** `_content_manifest.py fresh --affected` → 0 truly stale, 324 untouched modules byte-identical; `changed` → exactly the 18 class modules (`_r357_changed_modules.txt`).
- **A/B (`_r357_ab.log`, `_ab.py TMPLDELTA_OFF=1 BLL110 CEDO102 EXPFUN07`):** skeleton SCAFFOLD 39.57 → 40.22 % on the three (+0.65pp), every other metric identical.
- **Gates (`_r357_gates.log`, every RESULT ✓, 0 ✗, pairs skipped 0):** **skeleton SCAFFOLD 51.9819 → 52.0125 % (+0.031pp; 37 movers — 35 up, pp-sum +59.8, every mover inside the changed set), ≥50 1092 → 1094 (PNR104_2_0, OSSC501_1_0 cross), ≥75 160 / ≥90 14 EXACT, RAW 36.705 → 36.728 %**; the two dips NAMED: BLL170_0_0 58.19 → 57.95 (the one BLL1 parent whose gold keeps the chip — the family exception) and CEDK501_0_0 18.29 → 17.28 (the gold has no chip and Claude's phantom is gone; difflib re-aligns an 18 % page — correct output, lower score). compare_structure exact 11617 / EXTRA 175 / missing 617 EXACT; body_compare 182 EXACT; structural defect clean 98.91 % (26 occ / 23 pages) EXACT; tags 9557 / 9557; flipCard divergence 0, speechBubble ✓, modal ✓, MTK shell ✓, math ✓, menu labels ✓, dragAndDrop ✓, entry parity PASS. `_r357_sk_final.json` is the new chain state.

**Ledger:** scoped ship #1 since the r356 full (`_ship_ledger.py record-scoped --round 357`) · selftests + fast-loop baseline + content manifest + feature index refreshed (`_r357_postship.sh`) · data `_meta.template_deltas` {enabled, env, source}, the six values, the three template deltas · engine `ModuleResolver.Resolve` (the template-delta overlay) · env `TMPLDELTA_OFF` · KB row 16 unchanged (PARTIAL — presence LIVE, form uncodified) · the diff miner re-runs at the next session start.

"""
if "round 357, build 260619.28" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r357 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.28"' not in s:
    old = '\tstatic AppVersion = "260619.27";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, '\t// ROUND 357 (260619.28): the #module-code chip\'s presence follows the family\'s own convention on both page types — six no-evidence registry values corrected + the template_deltas cascade tier (ModuleResolver.Resolve; env TMPLDELTA_OFF); the diff miner\'s first chrome class.\n\tstatic AppVersion = "260619.28";')
    wr(P, s); print("Config.js: 260619.28")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "ROUND 357 BASELINE" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 356 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 357 BASELINE (the #module-code chip's presence follows the family's own convention on both page types — six no-evidence registry values corrected + the `template_deltas` tier; SCOPED regeneration of the 89-module family, ledger 1): SCAFFOLD mean 52.013% / >=50% 1094 / >=75% 160 / >=90% 14 / RAW 36.728% @ 1955 pairs, pairs skipped 0 — hold-or-improve; the two r357 dips named (BLL170_0_0, CEDK501_0_0).** Previous — ROUND 356 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `WIDGETMEMBERS_OFF` | 356 | **NO BUILT WIDGET DISCARDS A MEMBER IT NEVER READ"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `TMPLDELTA_OFF` | 357 | **THE TEMPLATE-SCOPED REGISTRY DELTA TIER — a level that holds two template families can say two things.** `Style_Anchor_Registry.json` gains an optional `template_deltas` object at a base or a level (`{\"<template_type>\": {field: value}}`, the 01-Finalized_Modules_ folder names) that `ModuleResolver.Resolve` overlays AFTER the level delta when `Module_Structure_Index.module_meta[code].template_type` is known; a module the index does not know keeps the level's value. First use: the BLL1 Inquiry parents' overview chip `absent` (their 56 Standard siblings keep `padded-number`), CEDO102, EXPFUN07. OFF = the level's value for every module (the r356 output on those nine). Data flag `_meta.template_deltas.enabled`. The six plain registry corrections of the same round (PNR / SCFUN / CEDT2 / CEDT3 / OSSC / CEDK5 `module_code`) have no toggle — the r336 precedent; their A/B is the resolved-rules dump before / after (`outputs/_r357_resolved*.json`). |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.27` (round 356"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.28` (round 357 — **the #module-code chip's presence follows the family's own convention on both page types** (six no-evidence `Style_Anchor_Registry.json` values corrected — PNR / SCFUN / CEDT2 / CEDT3 / OSSC / CEDK5 — plus the new `template_deltas` cascade tier in `ModuleResolver.Resolve` for the mixed-template levels BLL1 / CEDO1 / EXPFUN; env `TMPLDELTA_OFF`); the autonomous loop's session-19 Round 1, the DIFF MINER's first chrome class; SCOPED regeneration of the 89-module family, 18 modules / 36 pages changed; skeleton 51.982 → 52.013 % (+0.031pp, ≥50 +2, two dips named), every other gate EXACT; scoped ship #1 since the r356 full).\n"
             + OLD14)
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r357" not in d["skeleton"]:
    d["skeleton"]["mean_scaffold_pct"] = 52.013
    d["skeleton"]["pages_ge_50"] = 1094
    d["skeleton"]["raw_mean_pct"] = 36.728
    d["skeleton"]["_note_r357"] = "Round 357: the #module-code chip's presence (six registry corrections + the template_deltas tier) — SCAFFOLD 51.9819 → 52.0125 (+0.031pp; 37 movers, 35 up; dips NAMED: BLL170_0_0 the BLL1 family exception, CEDK501_0_0 an 18 % page re-aligned), ≥50 1092 → 1094, ≥75 160 / ≥90 14 EXACT, RAW 36.705 → 36.728. Hold-or-improve from here."
    d["_meta"]["build"] = "260619.28"; d["_meta"]["round"] = 357
    d["_meta"]["_note_r357"] = "Round 357: the chip presence class — skeleton +0.031pp (named dips), every other gate EXACT; SCOPED regeneration of the 89-module family, 18 modules / 36 pages; scoped ship #1 since the r356 full."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r357")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_r357_finalise.py" not in s:
    A = "| `_measure_r356_consumed.cjs`"
    assert s.count(A) == 1, "README anchor"
    ROWS = ("| `_measure_r357_chip.py` / `_r357_chip.{json,log}` / `_r357_resolved.json` / `_r357_resolved_after.json` / `_r357_resolved_off.json` / `_r357_splice.py` / `_r357_family.txt` / `_r357_plan_raw.txt` / `_r357_regen_run.sh` / `_r357_regen_par.sh` / `_r357_regen.log` / `_r357_changed_modules.txt` / `_r357_ab.log` / `_r357_gates.log` / `_r357_sk_full.log` / `_r357_sk_final.json` / `_r357_postship.sh` / `_r357_selftests.log` / `_r357_fastloop_snapshot.log` / `_r357_manifest_snapshot.log` / `_r357_ledger.log` / `_r357_index.log` / `_r357_finalise.py` | `CONVERTER_V2/outputs/` | Session 19 Round 1 (engine r357 — the diff miner's first chrome class: the #module-code chip's presence per family on both page types; six registry corrections + the `template_deltas` tier) — the probe (the r336 instrument generalised to both page types and every group), the resolved-rules dumps before / after / toggle-OFF, the anchored splice, the 89-module family regeneration, the A/B, the gate suite, the fresh skeleton score, the post-ship housekeeping, the finalise |\n")
    s = s.replace(A, ROWS + A, 1)
    wr(P, s); print("README: r357 rows")
print("finalise done")
