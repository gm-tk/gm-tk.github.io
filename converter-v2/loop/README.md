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
