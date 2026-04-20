# 29. HTML Converter Refactor Plan

## Status
Plan complete — ready for Session 4b-1 / 4b-2 execution.

## Baseline
- `js/html-converter.js`: 4,050 lines
- `js/app.js`: 1,364 lines
- Tests: 571/571 passing
- Branch: `claude/read-project-docs-OEUix`
- Prior-session plan files: `docs/26-tag-normaliser-refactor-plan.md` (Session 1), `docs/27-block-scoper-refactor-plan.md` (Session 2), `docs/28-interactive-extractor-refactor-plan.md` (Session 3). Audit Results sections of all three were read; they flagged residual size-target misses (S1 R-6, S3 IE-R4) but no remediation that blocks this refactor.

## Execute-strategy decision

**Split execute** — 6 sub-modules exceed the 3-module single-session ceiling, and the core file's 4,050-line bulk leaves no margin for one-shot extraction without context exhaustion.

- **Session 4b-1** (highest-line-range modules, bottom of file first): `html-converter-lesson-menu.js`, `html-converter-module-menu.js`, `html-converter-renderers.js`.
- **Session 4b-2** (mid + top of file): `html-converter-content-helpers.js`, `html-converter-block-renderer.js`, `html-converter-block-processor.js`.

Bottom-up extraction order means line numbers above the cut-point stay stable across sub-extractions within each session.

## Target sub-modules

| New file | Responsibility | Source line range | Moved methods | Est. lines |
|---|---|---:|---|---:|
| `js/html-converter-lesson-menu.js`     | Lesson-page menu generation (three style variants) | 3651–4017 | `_generateLessonMenuContent`, `_generateLessonMenuPromoteToH5`, `_generateLessonMenuOverviewBold` | ~370 |
| `js/html-converter-module-menu.js`     | Module-page menu (overview/info tabs) + menu helpers | 2939–3650 | `_replaceModuleMenuContent`, `_splitMenuContentIntoTabs`, `_getOriginalBlockIndex`, `_generateOverviewTabContent`, `_generateInfoTabContent`, `_renderModuleMenuBlocks`, `_splitH1HeadingAndDescription`, `_normaliseMenuHeading`, `_extractInfoTriggerData`, `_formatInfoTriggerDefinition`, `_renderHovertriggerParagraph`, `_extractHovertriggerData`, `_splitQuoteAttribution`, `_stripFullItalic`, `_renderMenuList`, `_buildMenuNestedList` | ~715 |
| `js/html-converter-renderers.js`       | Tables, lists, layout-table, image, video, sidebar, hint-slider, flip-card | 2148–2938 | `_wrapInRow`, `_renderList`, `_buildNestedList`, `_renderTable`, `_renderCellContent`, `_renderTableAsGrid`, `_detectLayoutTable`, `_getTableCellTags`, `_renderLayoutTable`, `_renderImagePlaceholder`, `_renderSidebarBlock`, `_wrapSideBySide`, `_hasTableTag`, `_renderHintSlider`, `_renderFlipCard`, `_getCellPlainText`, `_getCellFormattedText`, `_renderVideo`, `_renderImage` | ~790 |
| `js/html-converter-content-helpers.js` | Inline formatting + content-collection helpers (URL/image/audio/link extraction) | 1670–2147 | `_convertInlineFormatting`, `_escapeContentPreservingTags`, `_stripFullHeadingFormatting`, `_stripHeadingInlineTags`, `_splitMultiHeadingText`, `_collectBlockContent`, `_collectAlertContent`, `_collectMultiLineContent`, `_extractUrlFromContent`, `_extractImageInfo`, `_extractAudioFilename`, `_extractLinkInfo`, `_extractExternalLinkInfo` | ~480 |
| `js/html-converter-block-renderer.js`  | The single giant `_renderBlocks` orchestrator (per-block-type dispatch) | 554–1669 | `_renderBlocks` | ~1115 |
| `js/html-converter-block-processor.js` | Tag normalisation + formatted-text build for raw blocks | 313–553 | `_processAllBlocks`, `_processBlock`, `_buildFormattedText`, `_applyFormattingMarkers`, `_buildTableTextForTags` | ~240 |

Core `js/html-converter.js` retains: constructor (22–42), `convertPage` (54–73), `assemblePage` (74–139), `_splitOverviewContent` (140–179), `_splitLessonContent` (180–287), `_extractLessonTitle` (288–312), `_escContent` + `_escAttr` (4018–4050), plus thin delegations. Estimated post-split core: ~350 lines plus delegation shims.

`html-converter-block-renderer.js` exceeds the 700-line target by ~415 lines — `_renderBlocks` is a single 1,115-line method that cannot be split mid-body without rewriting dispatch. `html-converter-module-menu.js` lands at ~715, slight miss. Both flagged as known size overshoots — see Session 4b post-split remediation note.

## Extraction order

Within each session, extract bottom-up so source line numbers above the cut stay stable.

**Session 4b-1:**
1. `html-converter-lesson-menu.js` (lines 3651–4017)
2. `html-converter-module-menu.js` (lines 2939–3650)
3. `html-converter-renderers.js` (lines 2148–2938)

**Session 4b-2:**
4. `html-converter-content-helpers.js` (lines 1670–2147)
5. `html-converter-block-renderer.js` (lines 554–1669)
6. `html-converter-block-processor.js` (lines 313–553)

## Dependency graph

- `block-processor` → no sub-module deps. Consumes `tagNormaliser`.
- `content-helpers` → no sub-module deps. Pure string + processed-block utilities.
- `renderers` → consumes `content-helpers` (escaping, formatting). `_renderHintSlider`/`_renderFlipCard` also call `_getCellPlainText`/`_getCellFormattedText` which co-reside in this same module.
- `block-renderer` → consumes `content-helpers`, `renderers`, plus `tagNormaliser` and `interactiveExtractor` from core. The largest cross-module surface; injection covers it.
- `module-menu` → consumes `content-helpers` (escape, strip-italic, link-info), `renderers` (`_renderImage`, `_renderImagePlaceholder`, `_renderVideo`), and `tagNormaliser`.
- `lesson-menu` → consumes `content-helpers` (escape, inline formatting) and `tagNormaliser`. No `renderers` dep.

No cycles. Wiring order in `index.html` and `tests/test-runner.js`: `block-processor` → `content-helpers` → `renderers` → `block-renderer` → `module-menu` → `lesson-menu` → `html-converter`.

## Constructor signatures

```js
class HtmlConverterBlockProcessor {
    constructor(tagNormaliser) { ... }
}
```

```js
class HtmlConverterContentHelpers {
    constructor() { ... }
}
```

```js
class HtmlConverterRenderers {
    constructor(contentHelpers, escContent, escAttr) { ... }
}
```

```js
class HtmlConverterBlockRenderer {
    constructor(tagNormaliser, interactiveExtractor, contentHelpers, renderers, escContent, escAttr) { ... }
}
```

```js
class HtmlConverterModuleMenu {
    constructor(tagNormaliser, contentHelpers, renderers, escContent, escAttr) { ... }
}
```

```js
class HtmlConverterLessonMenu {
    constructor(tagNormaliser, contentHelpers, escContent, escAttr) { ... }
}
```

Core `HtmlConverter` constructor instantiates them in dependency order, passing bound references to its own `_escContent` / `_escAttr` (kept on core because they are referenced by tests indirectly via the rendering surface and by every sub-module). The `interactiveExtractor` argument is forwarded to `block-renderer` only.

## External API preservation

| Symbol | Accessed from | Treatment |
|---|---|---|
| `new HtmlConverter(tagNormaliser, templateEngine, interactiveExtractor)` | `js/app.js:21`; 30+ test files | Unchanged. |
| `convertPage(pageData, config)` | `js/app.js`; `tests/suppressDuplicateLessonTitleH2.test.js`, `tests/alertWithSidebarImage.test.js`, others | Unchanged on core; orchestrates `block-processor.processAll` + `block-renderer.renderBlocks`. |
| `assemblePage(pageData, config, moduleInfo)` | `js/app.js:1190` | Unchanged on core. |
| `collectedInteractives` (property) | `js/app.js:1183`, `1201` | Stays as a public property on core; `block-renderer` mutates it through an injected reference. |
| `_extractLessonTitle(blocks)` | `tests/years46LessonRecalibration.test.js:256` | Stays on core (already part of public-API section). |
| `_renderTable(tableData)` | `tests/lmsCompliance.test.js` (×6) | Delegate shim on core → `renderers.renderTable`. |
| `_renderCellContent(cell)` | `tests/lmsCompliance.test.js` (×2) | Delegate shim on core → `renderers.renderCellContent`. |
| `_renderVideo(url, config)` | `tests/lmsCompliance.test.js:559` | Delegate shim on core → `renderers.renderVideo`. |
| `_renderImage(imgInfo, config)` | `tests/lmsCompliance.test.js` (×2) | Delegate shim on core → `renderers.renderImage`. |
| `_renderImagePlaceholder(imageRef, config)` | `tests/lmsCompliance.test.js` (×2) | Delegate shim on core → `renderers.renderImagePlaceholder`. |
| `_formatInfoTriggerDefinition(string)` | `tests/lmsCompliance.test.js` (×5) | Delegate shim on core → `moduleMenu.formatInfoTriggerDefinition`. |
| `_renderModuleMenuBlocks(blocks, config, indent, isOverviewTab, isInfoTab)` | `tests/overviewTabScaffolding.test.js` (×2) | Delegate shim on core → `moduleMenu.renderModuleMenuBlocks`. |
| `_generateLessonMenuContent(pageData, config, moduleInfo, blocks)` | `tests/lessonMenuOverviewBold.test.js` (×5), `tests/lessonMenuPromoteAndBaseline.test.js` (×5), `tests/years46LessonRecalibration.test.js` (×5) | Delegate shim on core → `lessonMenu.generateLessonMenuContent`. |
| `_buildFormattedText`-style mirror | Comments in `js/layout-table-unwrapper.js:666`, `js/interactive-cell-parser.js:251` only | No live cross-call; comment update optional. |

## Internal-reference renames

Within each extracted sub-module body, intra-class `this.X(...)` calls must be rewritten to point at the new owner. Apply per-module, longest-match-first within each pass.

| In file | Old | New |
|---|---|---|
| `block-renderer` | `this._renderTable(`             | `this._renderers.renderTable(` |
| `block-renderer` | `this._renderCellContent(`       | `this._renderers.renderCellContent(` |
| `block-renderer` | `this._renderTableAsGrid(`       | `this._renderers.renderTableAsGrid(` |
| `block-renderer` | `this._detectLayoutTable(`       | `this._renderers.detectLayoutTable(` |
| `block-renderer` | `this._renderLayoutTable(`       | `this._renderers.renderLayoutTable(` |
| `block-renderer` | `this._renderImagePlaceholder(`  | `this._renderers.renderImagePlaceholder(` |
| `block-renderer` | `this._renderImage(`             | `this._renderers.renderImage(` |
| `block-renderer` | `this._renderVideo(`             | `this._renderers.renderVideo(` |
| `block-renderer` | `this._renderSidebarBlock(`      | `this._renderers.renderSidebarBlock(` |
| `block-renderer` | `this._renderHintSlider(`        | `this._renderers.renderHintSlider(` |
| `block-renderer` | `this._renderFlipCard(`          | `this._renderers.renderFlipCard(` |
| `block-renderer` | `this._renderList(`              | `this._renderers.renderList(` |
| `block-renderer` | `this._wrapInRow(`               | `this._renderers.wrapInRow(` |
| `block-renderer` | `this._wrapSideBySide(`          | `this._renderers.wrapSideBySide(` |
| `block-renderer` | `this._hasTableTag(`             | `this._renderers.hasTableTag(` |
| `block-renderer` | `this._convertInlineFormatting(` | `this._content.convertInlineFormatting(` |
| `block-renderer` | `this._escapeContentPreservingTags(` | `this._content.escapeContentPreservingTags(` |
| `block-renderer` | `this._stripFullHeadingFormatting(` | `this._content.stripFullHeadingFormatting(` |
| `block-renderer` | `this._stripHeadingInlineTags(`  | `this._content.stripHeadingInlineTags(` |
| `block-renderer` | `this._splitMultiHeadingText(`   | `this._content.splitMultiHeadingText(` |
| `block-renderer` | `this._collectBlockContent(`     | `this._content.collectBlockContent(` |
| `block-renderer` | `this._collectAlertContent(`     | `this._content.collectAlertContent(` |
| `block-renderer` | `this._collectMultiLineContent(` | `this._content.collectMultiLineContent(` |
| `block-renderer` | `this._extractUrlFromContent(`   | `this._content.extractUrlFromContent(` |
| `block-renderer` | `this._extractImageInfo(`        | `this._content.extractImageInfo(` |
| `block-renderer` | `this._extractAudioFilename(`    | `this._content.extractAudioFilename(` |
| `block-renderer` | `this._extractLinkInfo(`         | `this._content.extractLinkInfo(` |
| `block-renderer` | `this._extractExternalLinkInfo(` | `this._content.extractExternalLinkInfo(` |
| `block-renderer` | `this.collectedInteractives`     | `this._coreRef.collectedInteractives` |
| `module-menu`    | `this._renderImage(` / `this._renderImagePlaceholder(` / `this._renderVideo(` | `this._renderers.render*(` |
| `module-menu`    | `this._convertInlineFormatting(` / `this._escapeContentPreservingTags(` / `this._stripFullItalic(` / `this._splitQuoteAttribution(` (when called from another module-menu method) | `this._content.*` for the cross-cutting helpers; intra-module calls (e.g., `_renderMenuList` → `_buildMenuNestedList`) stay as `this._method(`. |
| `lesson-menu`    | `this._convertInlineFormatting(` / `this._escapeContentPreservingTags(`        | `this._content.*` |
| `renderers`      | `this._convertInlineFormatting(` / `this._escapeContentPreservingTags(` / `this._stripFullHeadingFormatting(` / `this._stripHeadingInlineTags(` | `this._content.*` |
| `renderers`      | `this._escContent(` / `this._escAttr(`                                          | `this._escContent(` / `this._escAttr(` (bound at construction; same ident locally) |
| `block-processor`| `this._buildFormattedText(` / `this._applyFormattingMarkers(` / `this._buildTableTextForTags(` | unchanged (intra-module) |

Apply renames longest-match-first so `this._renderTableAsGrid` is rewritten before `this._renderTable`.

## Core class delegation edits

In post-split `js/html-converter.js`:

- `convertPage` body: replace `this._processAllBlocks(...)` with `this._blockProcessor.processAllBlocks(...)` and `this._renderBlocks(...)` with `this._blockRenderer.renderBlocks(...)`.
- `assemblePage` body: replace `this._splitMenuContentIntoTabs(...)` and `this._replaceModuleMenuContent(...)` with the corresponding `this._moduleMenu.*` calls; replace `this._generateLessonMenuContent(...)` with `this._lessonMenu.generateLessonMenuContent(...)`.
- Add thin shim methods on core for every symbol in the External API Preservation table (one-line bodies returning the delegated call).
- Keep `_escContent` / `_escAttr` on core unchanged. Pass them as bound functions to sub-module constructors so each sub-module can use them via `this._escContent(...)` without a wider this-coupling.

## Wiring

- `index.html`: insert `<script src="js/html-converter-block-processor.js"></script>` and one tag per sub-module in the dependency-graph order, all *before* `<script src="js/html-converter.js">`.
- `tests/test-runner.js`: add a matching `loadScript('js/html-converter-<name>.js')` line per sub-module before `loadScript('js/html-converter.js')`, in the same dependency-graph order.

## Test checkpoints for Session 4b

After each sub-module extraction: run `node tests/test-runner.js`, commit, push. Commit format: `Session 4b<-N>: extract <module-name> from html-converter.js (<pass>/<total> passing)`.

Baseline before any extraction: 571/571. Any test regression at a checkpoint must block the next extraction until resolved.

## Range verification instruction for Session 4b

Line ranges in the target sub-modules table were derived from grep, not from a full read. Before each extraction, verify:

- `sed -n '<START-2>,<START+3>p' js/html-converter.js` to confirm the range starts at the expected method signature.
- `sed -n '<END-3>,<END+2>p' js/html-converter.js` to confirm the range ends at the expected closing brace (and that the next non-blank line is either a section divider or the next method's docstring).

If either verification fails, pause and re-derive the range with a fresh `grep -nE '^\s+[_a-zA-Z][a-zA-Z0-9_]*\s*\('` before extracting. Do not proceed on a stale range.

## Rollback commands for Session 4b

Single-module rollback (prior sub-modules already committed):

- `git reset --hard HEAD~1` to drop the last extraction commit.
- Manually revert `index.html` and `tests/test-runner.js` `<script>` / `loadScript` additions for that one module if they were part of the same commit.

Full-session rollback:

- `git reset --hard origin/claude/read-project-docs-OEUix` to return to the plan-commit state (this very session's commit).
- Or `git reset --hard origin/main` if a deeper revert is required.





