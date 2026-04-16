# 15. Development Guidelines


### Code Style

- **Vanilla JavaScript** — no frameworks, no build system
- **ES6+ class syntax** — `class ClassName { }` with `'use strict';`
- **No arrow functions in class methods** — use `function` for browser compatibility
- **JSDoc comments** — document all public methods with `@param` and `@returns`
- **Descriptive variable names** — `contentBlocks` not `cb`
- **Error handling** — throw named errors, catch in App with user-friendly messages

### Testing Approach

- **Automated unit tests** — `node tests/test-runner.js` runs 476 tests across 19 test files covering tag normalisation, block scoping, ordinal normalization, compound tag splitting, layout direction, writer instructions, fragment reassembly, interactive inference, video normalization, alert normalization, `[Inside tab]` handling, comprehensive sub-tag normalization (verbose ordinals, copy-paste mismatch detection, contentHint, carousel slides, flip card patterns), layout table detection/unwrapping (detection heuristics, contextual override, column role assignment, sidebar creation, content stream integrity), ENGS301 inconsistency fixes (heading level extraction, incomplete heading fallback, title case conversion, unrecognized tag implementations, hintslider/flipcard tag recognition, multichoice dropdown quiz, interactive data capture), LMS compliance recalibration (lesson number decimal format, title element format, activity classes, table header semantics, info trigger definition formatting, download journal, whakatauki author, image alt text), tag de-fragmentation (red-text boundary stitching, bracket space collapsing, bracket whitespace trimming, processBlock integration, ordinal suffix stripping), Phase 13 OSAI201 layout-table sidebar defects (H2 heading preservation, `[image]` tag + URL survival in sidebar_image blocks, `_sidebarImageUrl` cleanliness, fully-red CS paragraph preservation as `sidebar_extra` blocks, red-text wrapper balance checks, writer-instruction classification, pipeline integrity through unwrap + block-scope), Phase 13 years 4-6 lesson page recalibration (title element format, lesson h1, menu button tooltip, two-tier module menu, end-to-end calibration snapshot), and Phase 15 multi-template skeleton calibration (titlePattern token substitution, moduleCodeFormat per template, additionalHeadScripts with stickyNav/tekuradev, tooltip per-template overrides, footer link ordering, cross-template calibration snapshots)
- **Test runner** — minimal Node.js runner (`tests/test-runner.js`) with `describe()`, `it()`, `assert*()` functions; uses `vm.runInThisContext()` to load source files (tag-normaliser, block-scoper, layout-table-unwrapper, formatter, template-engine, interactive-extractor, html-converter) with class declarations in global scope; no external dependencies
- Test with real Writer Template `.docx` files (like the OSAI201 example)
- Verify tag normalisation against the complete normalisation table
- Verify page boundary detection against the 4 rules
- Verify HTML output structure against the document shell baseline
- Compare generated HTML visually with known-good reference modules

### Key Invariants

1. **Privacy** — No network requests for user data. All processing in-browser.
2. **Content fidelity** — Writer text must pass through unchanged.
3. **Tag completeness** — Every tag must be normalised or flagged.
4. **Structural correctness** — All HTML must follow the grid rules.
5. **Interactive isolation** — Interactive code is NEVER generated; only placeholders.

### Browser Compatibility

Target modern browsers: Chrome, Firefox, Safari, Edge (latest 2 versions). No IE11 support needed. Can use ES6 features (classes, template literals, const/let, destructuring, async/await).

---


---

[← Back to index](../CLAUDE.md)
