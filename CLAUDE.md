# CLAUDE.md — PageForge Project Reference

> **Project:** PageForge — Writer Template Parser & HTML Converter
> **Repository:** gm-tk.github.io (GitHub Pages)
> **Runtime:** 100% client-side browser application (no server, no backend)
> **Stack:** Vanilla JavaScript, HTML5, CSS3, JSZip (CDN)

---

## How this documentation is organised

This file is an **index**. The detailed per-section documentation that used to live inline here now lives as per-section files under `docs/`. This root is intentionally slim so it can be updated reliably without stream-idle timeouts. When a development session completes, new logs should be appended to the relevant `docs/NN-*.md` file — **not** to this root. The section index below is the primary navigation; the phase log further down lists completed development phases in chronological order.

---

## Critical Project Rules

- **Privacy model** — 100% client-side processing. No network calls touch user data. This is a GitHub Pages static site by design and must be preserved in all future development. See [`docs/01-project-overview.md`](docs/01-project-overview.md).
- **Content fidelity** — Writer text must pass through the pipeline unchanged. Never modify, rephrase, or auto-correct writer content during conversion. See [`docs/11-html-conversion-rules.md`](docs/11-html-conversion-rules.md).
- **Interactive isolation** — PageForge detects interactive components and extracts their data, but does **not** generate interactive component code. It emits structured placeholders plus a reference document for the downstream Claude AI Project to consume. See [`docs/12-interactive-components.md`](docs/12-interactive-components.md).
- **Tag completeness** — Every writer tag must be normalised against the canonical taxonomy or explicitly flagged as unknown. See [`docs/10-tag-taxonomy.md`](docs/10-tag-taxonomy.md).
- **Structural correctness** — All body content must sit inside the Bootstrap grid (`<div class="row"><div class="col-...">`). Void elements use XHTML self-closing style. Never add inline CSS or JavaScript. See [`docs/11-html-conversion-rules.md`](docs/11-html-conversion-rules.md).
- **Browser compatibility** — Targets the latest two versions of Chrome, Firefox, Safari, and Edge. ES6+ features are allowed. No IE11 support. See [`docs/15-dev-guidelines.md`](docs/15-dev-guidelines.md).

---

## Section Index

| # | Title | File |
|---|-------|------|
| 1 | Project Overview | [docs/01-project-overview.md](docs/01-project-overview.md) |
| 2 | Current Architecture | [docs/02-architecture.md](docs/02-architecture.md) |
| 3 | File Structure | [docs/03-file-structure.md](docs/03-file-structure.md) |
| 4 | How the Parser Works | [docs/04-parser.md](docs/04-parser.md) |
| 5 | How the Formatter Works | [docs/05-formatter.md](docs/05-formatter.md) |
| 6 | How the UI Works | [docs/06-ui.md](docs/06-ui.md) |
| 7 | Current Output Format | [docs/07-output-format.md](docs/07-output-format.md) |
| 8 | The Downstream Pipeline | [docs/08-downstream-pipeline.md](docs/08-downstream-pipeline.md) |
| 9 | Template System Knowledge | [docs/09-template-system.md](docs/09-template-system.md) |
| 10 | Tag Taxonomy & Normalisation | [docs/10-tag-taxonomy.md](docs/10-tag-taxonomy.md) |
| 11 | HTML Conversion Rules | [docs/11-html-conversion-rules.md](docs/11-html-conversion-rules.md) |
| 12 | Interactive Components | [docs/12-interactive-components.md](docs/12-interactive-components.md) |
| 13 | Future Architecture — HTML Conversion Engine | [docs/13-future-architecture.md](docs/13-future-architecture.md) |
| 14 | Template Configuration System | [docs/14-template-config.md](docs/14-template-config.md) |
| 15 | Development Guidelines | [docs/15-dev-guidelines.md](docs/15-dev-guidelines.md) |
| 16 | ENGS301 Inconsistency Fixes | [docs/16-engs301-fixes.md](docs/16-engs301-fixes.md) |
| 17 | LMS Compliance Recalibration (Phase 7) | [docs/17-lms-compliance-phase7.md](docs/17-lms-compliance-phase7.md) |
| 18 | Tag Normalisation Robustness (Phase 1 Patch) | [docs/18-tag-normalisation-patch.md](docs/18-tag-normalisation-patch.md) |
| 19 | UI Overhaul & Rebranding (Phase 8) | [docs/19-ui-overhaul-phase8.md](docs/19-ui-overhaul-phase8.md) |
| 20 | Feature Removal — Visual Comparison Review & Conversion Error Log (Phase 14) | [docs/20-feature-removal-phase14.md](docs/20-feature-removal-phase14.md) |
| 21 | OSAI201 Layout-Table Sidebar Defects (Phase 13) | [docs/21-osai201-defects-phase13.md](docs/21-osai201-defects-phase13.md) |
| 22 | Years 4–6 Lesson Page Recalibration (Phase 13) | [docs/22-years46-recalibration-phase13.md](docs/22-years46-recalibration-phase13.md) |
| 23 | Multi-Template Skeleton Calibration (Phase 15) | [docs/23-multi-template-skeleton-phase15.md](docs/23-multi-template-skeleton-phase15.md) |
| 24 | Documentation Refactor | [docs/24-docs-refactor.md](docs/24-docs-refactor.md) |

---

## Phase Log

Chronological list of completed development phases. Each entry links to the per-phase documentation file.

- **Phase 7 — LMS Compliance Recalibration** — Audit vs D2L/Brightspace reference closed 18 structural gaps (lesson number format, title element, activity classes, table semantics, info trigger, download journal, whakatauki, alt text). [docs/17-lms-compliance-phase7.md](docs/17-lms-compliance-phase7.md)
- **Phase 8 — UI Overhaul & Rebranding** — Renamed ParseMaster → PageForge; decoupled upload from conversion with staged file + Convert button; consolidated summary into debug panel. [docs/19-ui-overhaul-phase8.md](docs/19-ui-overhaul-phase8.md)
- **Phase 13 — OSAI201 Layout-Table Sidebar Defects** — Fixed three content-loss defects in `_createSidebarBlock()` (URL over-capture, lost `[image]` tag, dropped CS paragraph). [docs/21-osai201-defects-phase13.md](docs/21-osai201-defects-phase13.md)
- **Phase 13 — Years 4–6 Lesson Page Recalibration** — Stripped decimal from `<title>`, introduced lesson-specific `<h1>`, dropped tooltip from lesson menu button, rewrote lesson module menu to two-tier structure. [docs/22-years46-recalibration-phase13.md](docs/22-years46-recalibration-phase13.md)
- **Phase 14 — Feature Removal (Visual Comparison Review & Conversion Error Log)** — Removed internal development utilities (`review.html`, `calibrate.html`, supporting JS/CSS, 72 tests). Core pipeline untouched. [docs/20-feature-removal-phase14.md](docs/20-feature-removal-phase14.md)
- **Phase 15 — Multi-Template Skeleton Calibration** — Added `titlePattern` tokenisation, per-template `moduleCodeFormat`, `additionalHeadScripts` (stickyNav + tekuradev for 1-3/7-8), tooltip per-template overrides, and footer link ordering. [docs/23-multi-template-skeleton-phase15.md](docs/23-multi-template-skeleton-phase15.md)
- **Phase 1 Patch — Tag Normalisation Robustness** — Added `defragmentRawText()` pre-processing for fractured Word-XML red-text boundaries; extended `resolveOrdinalOrNumber()` with ordinal suffix stripping. [docs/18-tag-normalisation-patch.md](docs/18-tag-normalisation-patch.md)
- **ENGS301 Inconsistency Fixes** — 13 module-specific fixes across tag normaliser, HTML converter, interactive extractor, formatter, and title extraction. [docs/16-engs301-fixes.md](docs/16-engs301-fixes.md)
- **Documentation Refactor** — Split the monolithic root `CLAUDE.md` (~2625 lines) into a slim index plus per-section files under `docs/`. No source code touched; 476/476 tests still pass. [docs/24-docs-refactor.md](docs/24-docs-refactor.md)

> Earlier phases (0–6.1) are covered implicitly by the structural sections (docs/01–15). Only phases with dedicated recalibration or post-launch log files are listed above.

---

## Convention for Future Development Logs

- When a development session completes, append a new `###` sub-heading documenting the change to the **most relevant existing** `docs/NN-*.md` file — not to this root.
- If the change introduces a new major phase that does not fit any existing file, create a new `docs/NN-phase-name.md` file using the next available two-digit prefix (zero-padded, kebab-case slug) and add a one-line entry to the Phase Log above.
- Never append large logs to this root file. Keep it slim so it remains editable without stream-idle timeouts.
