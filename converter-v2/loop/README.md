# converter-v2/loop — the committed mirror of the autonomous loop's artefacts

The development harness (`../../../CONVERTER_V2/`, with its `outputs/` probes and
`reference/tests/` gates) lives OUTSIDE this repository by design (see `../CLAUDE.md` §4).
The unattended improvement loop (`FINAL_MODULE_DATA/LOOP__Autonomous_Rounds.md`) requires its
instruments and their first outputs to be COMMITTED so nothing is lost between sessions, so
this folder holds a byte-for-byte copy of each loop artefact at the time of its commit.

The canonical, runnable copy of every tool stays in `CONVERTER_V2/outputs/` (dynamic paths,
per CLAUDE.md §13); the files here are snapshots refreshed at each loop commit — do not run
them from here.

| file | canonical location | what it is |
|---|---|---|
| `_measure_ceiling.py` | `CONVERTER_V2/outputs/` | Round 0 — the ceiling instrument (share of the human's structure with NO source in the Writers Template) |
| `_ceiling_r0.md` / `_ceiling_r0.json` | `CONVERTER_V2/outputs/` | Round 0 — its first full-corpus output (2026-09-14) |
| `_measure_r0b_kbstatus.py` | `CONVERTER_V2/outputs/` | Round 0b — the KB amalgamation facts probe (gold vs Claude signatures per KB rule, scopes from the WTs) |
| `_r0b_kbfacts.json` | `CONVERTER_V2/outputs/` | Round 0b — its output |
| `KB_AMALGAMATION_STATUS.md` | `FINAL_MODULE_DATA/` (folder root) | Round 0b — one row per front-facing KB decision with its PageForge status |
| `LOOP_STATE.md` | `FINAL_MODULE_DATA/` (folder root) | the loop's position, declined/blocked classes, round log |
| `_measure_r314_dbxplace.py` / `_r314_dbxplace.json` / `_r314_affected.txt` | `CONVERTER_V2/outputs/` | Round 1 (engine r314) — the dropbox-placement probe and its results (121 affected modules) |
| `_r314_splice_UNAPPLIED.py` / `_r314_splice_APPLIED.py` | `CONVERTER_V2/outputs/` | Round 1 — the anchored engine/data edit; the session-1 draft (owner-close anchor one tab too deep) and the applied version |
| `_r314_bundledump.cjs` | `CONVERTER_V2/outputs/` | Round 1 — bundle-state diagnostic |
| `_r314_regen_set.txt` / `_r314_family_dropdown.txt` / `_r314_changed_modules.txt` | `CONVERTER_V2/outputs/` | Round 1 — the 243-module regeneration set (121 affected ∪ 212 dropDown family), the family list, and the 43 modules whose bytes changed |
| `_r314_gates.log` / `_r314_sk_full.log` / `_r314_verify_dropdown.log` / `_r314_fastloop.log` | `CONVERTER_V2/outputs/` | Round 1 — the gate suite, the fresh full skeleton score, the dropDown family verifier, the decomposition proof |
| `_r315_splice.py` / `_r315_unit.cjs` | `CONVERTER_V2/outputs/` | Round 2 (engine r315) — the XHTML-shell splice (KB constraint 28) and the 18-case unit test that drives the real `HtmlFormatter.Indent` |
| `_r315_repair_anchor_compare.py` / `_r315_anchor_compare_BEFORE.py` / `_r315_anchor_compare_AFTER.py` | `CONVERTER_V2/outputs/` + `reference/tests/anchor_compare.py` | Round 2 — the void-aware repair of the gate suite's page-pairing parsers, with the before/after copies of the tool (reference/tests is outside git) |
| `_r315_gates.log` / `_r315_sk_full.log` / `_r315_sk_prerepair.json` / `_r315_fastloop_snapshot.log` / `_r315_selftests.log` / `_ceiling_r315.md` | `CONVERTER_V2/outputs/` | Round 2 — the gate suite, the fresh skeleton score (repaired pairing; the pre-repair state kept for the record), the full-ship baseline snapshot, the selftests, the ceiling under the repaired pairing |
| `_measure_r316_lessonpair.py` / `_r316_lessonpair.json` / `_r316_affected.txt` / `_r316_regen_set.txt` | `CONVERTER_V2/outputs/` | Round 3 (engine r316) — the lesson bilingual-pair probe and its results; the 17 affected and the 179-module regeneration set |
| `_r316_splice.py` | `CONVERTER_V2/outputs/` | Round 3 — the anchored engine/data edit (SkeletonBuilder + Emit_Templates) |
| `_r316_gates.log` / `_r316_sk_full.log` / `_r316_fastloop.log` / `_r316_selftests.log` | `CONVERTER_V2/outputs/` | Round 3 — the gate suite, the fresh skeleton score, the decomposition proof, the selftests |
| `_measure_r317_acks.py` / `_r317_acks.json` / `_r317_splice.py` | `CONVERTER_V2/outputs/` | Round 4 (engine r317) — the acks probe (the KB form simulated + scored before coding: the named override list) and the splice |
| `_r317_gates.log` / `_r317_sk_full.log` / `_r317_fastloop_snapshot.log` / `_r317_selftests.log` | `CONVERTER_V2/outputs/` | Round 4 — the gate suite, the fresh skeleton score, the full-ship baseline snapshot, the selftests |
| `_measure_r318_lazyhosts.py` / `_r318_lazyhosts.json` / `_r318_splice.py` / `_r318_unit.cjs` | `CONVERTER_V2/outputs/` | Round 5 (engine r318) — the lazy-in-moving-hosts probe (post-regeneration result; `_r318_lazyhosts_pre.json` is the before), the splice, the 9-case unit test |
| `_r318_gates.log` / `_r318_sk_full.log` / `_r318_fastloop_snapshot.log` / `_r318_selftests.log` | `CONVERTER_V2/outputs/` | Round 5 — the gate suite, the fresh skeleton score, the full-ship baseline snapshot, the selftests |
| `_r319_splice.py` / `_r319_affected.txt` / `_r319_gates.log` / `_r319_sk_full.log` / `_r319_fastloop.log` / `_r319_selftests.log` | `CONVERTER_V2/outputs/` | Round 6 (engine r319) — the learningSupport cohort splice, the 35 X modules, the gate suite, the fresh skeleton score, the decomposition proof, the selftests |
| `_measure_r320_dupheading.py` / `_r320_dupheading.json` | `CONVERTER_V2/outputs/` | Round 7 (engine r320) — the constraint-47/95 duplicate-heading probe: the DECLINED candidate's measurement |
| `_r320_splice.py` / `_r320_memberdump.cjs` / `_r320_gates.log` / `_r320_sk_full.log` / `_r320_fastloop.log` | `CONVERTER_V2/outputs/` | Round 7 — the release-order splice, the bundle member dump, the gate suite, the fresh skeleton score, the decomposition proof |
| `_r321_splice.py` / `_r321_titledump.cjs` / `_r321_affected.txt` / `_r321_gates.log` / `_r321_sk_full.log` / `_r321_fastloop.log` / `_r321_selftests.log` | `CONVERTER_V2/outputs/` | Round 8 (engine r321) — the MTK title-source splice, the run/page title dump, the 19 Bilingual modules, the gate suite, the fresh skeleton score, the decomposition proof, the selftests |
| `_r322_mtkquiz_shells.json` | `CONVERTER_V2/outputs/` | The c65 / CL-0082 kickoff measurement (68 MTK-quiz shells, 39 carrying quiz content) — the authorised next round, not started |
| `_measure_r322_mtkquiz.cjs` / `_r322_splice.py` / `_r322_probe.cjs` / `_verify_mtkquiz.cjs` | `CONVERTER_V2/outputs/` (the verifier: `reference/tests/`) | Round 9 (engine r322) — the marker-window probe (64 markers / 33 pages / 25 modules → `_r322_mtkquiz_windows.json`), the 22-step anchored engine/data splice, the in-memory A/B probe vs disk, and the new MTK-quiz SHELL gate (mirrored here because `reference/tests/` is outside git) |
| `_r322_gates.log` / `_r322_sk_full.log` / `_r322_sk_final.json` / `_r322_fastloop.log` / `_r322_selftests.log` / `_r322_probe_{off,on}.log` / `_r322_verify_*_{on,off}.log` / `_r322_family_regen.txt` / `_r322_changed_modules.txt` | `CONVERTER_V2/outputs/` | Round 9 — the gate suite, the fresh full skeleton score, the decomposition proof, the 13 selftests, the OFF/ON probes over the 58-module family, the verifier A/B logs, the regeneration set and the changed set |
| `_r323_splice.py` / `_measure_r323_buttonstop.py` / `_measure_r323_stickynav.py` | `CONVERTER_V2/outputs/` | Round 10 (engine r323) — the trailing-full-stop splice (3 steps), the button-label probe (gold 9 / 5,553 vs Claude 441 / 3,052 → 29 after), and the stickyNav `<head>` probe (gold 1,504 / 2,385 pages; the class is BLOCKED — needs Chris) |
| `_r323_gates.log` / `_r323_sk_full.log` / `_r323_sk_final.json` / `_r323_fastloop.log` / `_r323_selftests.log` / `_r323_probe_off_0*.log` / `_r323_regen.log` / `_r323_buttonstop{,_after}.json` / `_r323_stickynav.json` | `CONVERTER_V2/outputs/` | Round 10 — the gate suite, the fresh full skeleton score, the decomposition proof, the 13 selftests, the whole-corpus OFF probe, the full regeneration log, the measurements |
| `_r324_splice.py` / `_measure_r324_lessontitles.py` | `CONVERTER_V2/outputs/` | Round 11 (engine r324) — the `Lesson N` label-title splice (5 steps) and the paired-lesson-title classifier (before/after: `_r324_lessontitles{,_before,_after}.json`) |
| `_r324_gates.log` / `_r324_sk_full.log` / `_r324_sk_final.json` / `_r324_fastloop.log` / `_r324_selftests.log` / `_r324_probe_{off,on}_0*.log` / `_r324_regen.log` / `_r324_affected.txt` | `CONVERTER_V2/outputs/` | Round 11 — the gate suite, the fresh full skeleton score, the decomposition proof, the 13 selftests, the whole-corpus OFF/ON probes, the scoped regeneration |
| `_r325_splice.py` / `_measure_r325_phasenumbers.py` / `_measure_r325_emptyboxes.py` | `CONVERTER_V2/outputs/` | Round 12 (engine r325) — the phase-numbering splice (9 steps), the box-by-box phase-number probe (before/after: `_r325_phasenumbers{,_on}.json`; also drives the ON-probe measurement via CLAUDE_ROOT) and the empty hand-off-box sizing (172 boxes / 15 shapes, no class ≥ 20) |
| `_r325_gates.log` / `_r325_sk_full.log` / `_r325_sk_final.json` / `_r325_fastloop.log` / `_r325_selftests.log` / `_r325_probe_off_0*.log` / `_r325_probe_on.log` / `_r325_regen.log` / `_r325_affected.txt` | `CONVERTER_V2/outputs/` | Round 12 — the gate suite, the fresh full skeleton score, the decomposition proof, the 13 selftests, the whole-corpus OFF probe, the family ON probe, the scoped regeneration — the round the loop STOPPED on (plateau) |
| *(not mirrored)* `batch_results.json.corrupt-2026-09-15-powercut` | `CONVERTER_V2/reference/tests/` | Round 3 — the batch runner's results ledger as the power cut left it (a 48-byte NUL run); 4.5 MB, kept on disk beside the repaired working copy, deliberately not committed |
