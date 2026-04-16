# 24. Documentation Refactor — Root CLAUDE.md → Per-Section `docs/`

### Overview

A three-session refactor (A, B, C) that split the previously monolithic `CLAUDE.md` (~2625 lines) into a slim root index plus per-section files under `docs/`. Sessions A and B extracted the 23 sections of the original file. Session C (this session) replaced the root `CLAUDE.md` with a slim index, performed a cross-reference sweep, re-ran the full test suite, and recorded this log.

**Status:** DONE — Root reduced from 2625 lines to 78 lines. 23 per-section files live under `docs/`. 476/476 tests pass. No source code was modified.

---

### Motivation

Single-file `CLAUDE.md` updates were routinely hitting stream-idle timeouts because every append required rewriting the full 2625-line file. The file had also become difficult to scan and difficult to update in parallel across sessions — any structural cross-reference change needed a full re-read. Splitting the content into per-section files eliminates the timeout risk, makes each section independently editable, and keeps the root as a navigational index.

---

### Old Structure

- Single root file: `CLAUDE.md` (~2625 lines).
- Twenty-three top-level sections (1. Project Overview through 23. Multi-Template Skeleton Calibration (Phase 15)).
- Every new phase log appended to the same file, steadily inflating its length.

---

### New Structure

- **Slim root** `CLAUDE.md` (~78 lines) containing:
  - Header block (project/repo/runtime/stack).
  - "How this documentation is organised" paragraph.
  - `Critical Project Rules` — six one/two-sentence bullets with links to the detailed sections.
  - `Section Index` — Markdown table with one row per `docs/NN-*.md` file.
  - `Phase Log` — chronological list of completed development phases with one-line summaries.
  - `Convention for Future Development Logs` — short directive for future sessions.
- **Per-section files** under `docs/` — one file per section, numbered `NN-kebab-case-slug.md`.

---

### Naming Convention for `docs/` Files

- Two-digit, zero-padded numeric prefix (`01`, `02`, …, `23`, `24`).
- Kebab-case slug after the prefix (`01-project-overview.md`, `22-years46-recalibration-phase13.md`).
- The numeric prefix preserves chronological ordering in `ls` output without relying on timestamps.
- Phase-log files include the phase identifier in the slug where relevant (`-phase7`, `-phase13`, `-phase14`, `-phase15`).

---

### Workflow Rule for Future Sessions

- When a development session completes, append a new `###` sub-heading to the **most relevant existing** `docs/NN-*.md` file — not to the root `CLAUDE.md`.
- Only create a new numbered `docs/NN-*.md` file when the change is a genuinely new major phase that does not fit under any existing file.
- When a new file is created, add a one-line entry to the `Phase Log` section of the root `CLAUDE.md`.
- Never append large logs to the root file. Keep it slim so stream-idle timeouts do not re-emerge.

---

### Session C Verification Steps

1. Confirmed `docs/01-project-overview.md` through `docs/23-multi-template-skeleton-phase15.md` all present.
2. Verified no intra-file anchor links (`](#...)`) survived the split — `grep -rn "](#" docs/` returned zero hits.
3. Surveyed prose cross-references (`grep -n "Section [0-9]" docs/*.md`) — all remaining hits are either references to external knowledge files (the downstream Claude AI Project's `01_PIPELINE_EXTRACTION_TAGS.md` etc.) or numerically consistent prose pointers that remain correct under the new naming (e.g. "Section 10" now corresponds to `docs/10-tag-taxonomy.md`). No rewrites required.
4. Re-ran the full test suite via `node tests/test-runner.js` — **476/476 passed, 0 failed**, identical to pre-refactor.
5. Wrote this log file.
6. Added the one-line Phase Log entry for this refactor to the root `CLAUDE.md`.

---

### Complete List of Files in `docs/` After Session C

```
01-project-overview.md
02-architecture.md
03-file-structure.md
04-parser.md
05-formatter.md
06-ui.md
07-output-format.md
08-downstream-pipeline.md
09-template-system.md
10-tag-taxonomy.md
11-html-conversion-rules.md
12-interactive-components.md
13-future-architecture.md
14-template-config.md
15-dev-guidelines.md
16-engs301-fixes.md
17-lms-compliance-phase7.md
18-tag-normalisation-patch.md
19-ui-overhaul-phase8.md
20-feature-removal-phase14.md
21-osai201-defects-phase13.md
22-years46-recalibration-phase13.md
23-multi-template-skeleton-phase15.md
24-docs-refactor.md
```

---

### Invariants Locked In By This Refactor

1. **Root `CLAUDE.md` stays slim.** Target under 300 lines; current 78 lines. No large logs are ever appended to it.
2. **Every section of the original monolithic `CLAUDE.md` is preserved** in exactly one `docs/NN-*.md` file. No content was deleted during the split.
3. **Phase documentation is append-only.** A new phase adds either a new `###` sub-heading to the existing most-relevant file, or a new numbered `docs/NN-*.md` file plus a one-line Phase Log entry — never a mass rewrite of existing files.
4. **No source code was modified** during the three-session refactor. Test results are bit-for-bit identical to the pre-refactor run: 476/476 passing.
