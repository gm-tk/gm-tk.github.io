# CLAUDE.md — PageForge V2 (CONVERTER_V2): the short pointer

**The full operating guide is `OPERATING_GUIDE.md` in this folder (1.3 MB, 17 sections).** Until
2026-09-21 that guide WAS this file. The harness auto-loads every `CLAUDE.md` into the model's context at
session start and again after every automatic compaction, so a 1.3 MB `CLAUDE.md` refilled the window the
moment it was compacted and the autonomous loop thrashed (three compactions in a row, then a manual
`/compact`). Chris asked for that to be fixed for good: this pointer is what gets auto-loaded now; the
guide is read BY SECTION ONLY — `grep -n "^## " OPERATING_GUIDE.md`, then `sed -n "A,Bp"` — never whole.
Every "OPERATING_GUIDE.md §N" in the loop docs, the skills and the finalise ritual means that file.

`FINAL_MODULE_DATA/CLAUDE.md`, `CONVERTER_V2/CLAUDE.md`, `CONVERTER_V2/OPERATING_GUIDE.md` and
`CONVERTER_V2/BUILD_CHANGELOG.md` are SYMLINKS into `pageforge-site/converter-v2/` — always edit the real
path, never `sed -i` a symlink (it silently forks the two copies).

## The always-on rules (the guide's non-negotiables, one screen)

1. **REGENERATION IS OPT-IN (§0).** Never regenerate the corpus unless the message carries `REGENERATE
   CORPUS`; the `/loop-start` message carries it for every loop round, scoped by the §0a (whole-type) /
   §0b (tag-family) rules — rebuild the fixed half AND the already-working half, explain every changed
   module, never revert a new rule to silence a verifier.
2. **DATA OVER CODE (§2).** A fix is a data-described shape in `data/*.json` behind a data flag AND an
   env `*_OFF` toggle; the toggle-OFF corpus IS the last proven state. Never `if (moduleCode === …)`.
3. **The human gold is the per-module target (§6), derived from the raw inputs — never read as an
   input.** Marked doc-14 / KB rules outrank the gold (named overrides, never chased back).
4. **MEASURE the class first (§5), judge on the skeleton SCAFFOLD gate (§9); a change ships only when every
   protected gate holds-or-improves, every dip NAMED.** Gates run from `CONVERTER_V2/reference/tests/`
   under WSL — `_gatecheck.py` prints CACHED rows for gates it did not run, so run `cs bc` first.
5. **This machine:** never call `python3`/`python` from the Bash tool (Windows Store stub, hangs 30 min) —
   every Python and every gate runs under `wsl.exe -e bash -lc '…'`; `data/*.json` are TAB-indented LF
   (Edit tool, or `io.open(p, "w", encoding="utf-8", newline="")`); check `git ls-files --eol` before a
   commit.
6. **Git (§16):** commit `pageforge-site` at the end of every shipped round; NEVER push; NEVER
   `git checkout` / `git restore` a file whose work is uncommitted (round 284 lost ten data blocks that
   way). Commit messages end with `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.
7. **The finalise ritual (§12):** a dated BUILD_CHANGELOG.md entry (newest first; it is AUTHORITATIVE and
   ~2 MB — read its top entry only), `app/js/Config.js` `AppVersion` bump, OPERATING_GUIDE §9 baseline /
   §11 toggle row / §14 snapshot, `reference/tests/gate_baseline.json`, the loop mirror in `loop/`, the
   `_MIGRATION/CHECKSUMS__*.txt` refresh, then the commit. Delete a spent kickoff file.

## Where the live numbers are

The current build, gate baselines and toggle table: `OPERATING_GUIDE.md` §14 (top bullet) and §11 (top
rows), `reference/tests/gate_baseline.json`, and the top entry of `BUILD_CHANGELOG.md`. The autonomous
loop's position: `FINAL_MODULE_DATA/LOOP_STATE.md` (its rules: `LOOP__Autonomous_Rounds.md`).

## Section map of OPERATING_GUIDE.md

| § | what it holds |
|---|---|
| 0 / 0a / 0b | regeneration opt-in; the whole-type and tag-family regeneration rules |
| 1–3 | mission (Phase 1 = the scaffold), DATA OVER CODE, the start-of-session checklist |
| 4 | the repository map — the ONE engine copy in `pageforge-site/converter-v2/`, the symlinked harness, `app/js/` pipeline table, `data/` table |
| 5 | the disciplined round: TRIANGULATE → MEASURE → IMPLEMENT → PROVE → FINALISE |
| 6 | conventions & mandates (Level 0 gold target, the doc-14 override, the A/B-i/B-ii/C framework, notes) |
| 7–8 | the three corpora + page pairing; the triangulation cheatsheet |
| 9 | the PROTECTED GATES and every round's baseline line (newest first) |
| 10 / 10a | the regeneration recipe; the SCOPED ship |
| 11 | the env-toggle table — one row per shipped round (newest first) |
| 12 | the finalise ritual |
| 13 | measurement-tools convention (probes, registries, the feature index, the dashboard) |
| 14 | the current-state snapshot (build, gates) — newest first |
| 15 | remaining levers |
| 16 | working discipline / gotchas (symlinks, CRLF, stale checks, void-aware parsers, chained scores) |
