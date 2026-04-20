# 29. HTML Converter Refactor Plan

## Status
DONE — split executed, audit complete, 571/571 tests passing.

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

## Audit Results

### Sub-module inventory

| File | Lines |
|---|---:|
| `js/html-converter.js`                  | 641 |
| `js/html-converter-block-processor.js`  | 245 |
| `js/html-converter-block-renderer.js`   | 1124 |
| `js/html-converter-content-helpers.js`  | 483 |
| `js/html-converter-lesson-menu.js`      | 386 |
| `js/html-converter-module-menu.js`      | 707 |
| `js/html-converter-renderers.js`        | 798 |

Core file dropped 4050 → 641 (–3409). Six sub-modules total. `block-renderer` and `renderers` both overshoot the 500-line target; `block-renderer` contains the giant `_renderBlocks` orchestrator (per plan). Tests: 571/571.

### Cross-reference with Sessions 1–3 findings

| Tag | Upstream classification | html-converter handling site | Relative classification |
|---|---|---|---|
| `word_highlighter` (S1 R-1, IE-R5) | Doc drift + 3-site downstream | Not referenced anywhere in `js/html-converter*.js` | No impact — html-converter never keys off `word_highlighter` or `word_select`. S1 R-1 does not cascade into this layer. |
| `slide_show` (S1 R-3 / D-2) | Dead key | Not referenced | No impact. |
| `info_trigger_image` (S1 R-4/R-5) | Redundancy in normaliser | Not referenced by name in html-converter (routed through generic interactive handler) | No impact. |
| `speech_bubble` (S2 BS-R2) | Opener but no closer | Generic interactive handler at `block-renderer:366` delegates to `InteractiveExtractor` (table pattern 8 / conversation pattern 9). | Consumer only — boundary signals own termination; no html-converter change if BS-R2 adds an explicit closer. |
| `rotating_banner` (S2 BS-R3) | Opener but no closer | Not referenced by tagName in html-converter; reached via generic interactive handler. | Consumer only — same as speech_bubble. |
| `_matchTabSubTag` shadow (S2 BS-R1) | Internal normaliser shadow | Not referenced | No impact. |
| Patterns 11/12/13 preview drift (IE-R3) | Placeholder preview gap | Not referenced (preview is rendered by `InteractivePlaceholderRenderer`, not html-converter) | No impact. |

### Tag-to-renderer mapping

Every `tagName` branch in `_renderBlocks` (html-converter-block-renderer.js):

| Tag | Renderer site |
|---|---|
| `activity`                 | `block-renderer:213` |
| `end_activity`             | `block-renderer:257` |
| `activity_heading`         | `block-renderer:284` |
| `info_trigger` (interactive) | `block-renderer:305` — inline `<span class="infoTrigger">` |
| `hint_slider` (interactive) | `block-renderer:326` → `renderers._renderHintSlider` |
| `flip_card` (interactive)  | `block-renderer:347` → `renderers._renderFlipCard` |
| `upload_to_dropbox` (interactive) | `block-renderer:370` (sets `activityHasDropbox`) + generic interactive handler |
| Generic `category='interactive'` | `block-renderer:366` → `InteractiveExtractor.processInteractive` |
| `heading`                  | `block-renderer:437` |
| `body` / untagged body text | `block-renderer:552` |
| `alert`                    | `block-renderer:582` (layout-table-paired + standalone) |
| `important`                | `block-renderer:693` |
| `alert_cultural_wananga`/`_talanoa`/`_combined` | `block-renderer:717` |
| `whakatauki`               | `block-renderer:744` |
| `quote`                    | `block-renderer:769` |
| `rhetorical_question`      | `block-renderer:813` |
| `video`                    | `block-renderer:828` → `renderers.renderVideo` |
| `image`                    | `block-renderer:841` → `renderers.renderImage` |
| `audio`                    | `block-renderer:854` |
| `button`                   | `block-renderer:868` |
| `external_link_button`     | `block-renderer:883` |
| `external_link`            | `block-renderer:901` |
| `go_to_journal`            | `block-renderer:926` |
| `download_journal`         | `block-renderer:938` |
| `supervisor_button`        | `block-renderer:954` |
| Sidebar `_cellRole` blocks | `block-renderer:972` → `renderers._renderSidebarBlock` |
| Tagged `[TABLE]`           | `block-renderer:1003` → `renderers.renderTable` |
| Layout table (untagged)    | `block-renderer:1015` → `renderers._renderLayoutTable` |
| Untagged grid table        | `block-renderer:1031` → `renderers._renderTableAsGrid` |
| `category='subtag'`        | `block-renderer:1045` (plain `<p>`) |
| `category='link'`          | `block-renderer:1056` |
| `reo_translate`            | `block-renderer:1070` (skipped — styling pass-through) |

**Tier 1 interactives coverage (per docs/12):**

| Tier 1 type | Dedicated renderer in html-converter? |
|---|---|
| `accordion`       | No — routed through generic interactive handler (`block-renderer:366` → InteractiveExtractor). |
| `flip_card`       | Yes — `block-renderer:347` → `renderers._renderFlipCard` (plus fall-through to generic if renderer returns null). |
| `speech_bubble`   | No — routed through generic interactive handler. |
| `tabs`            | No — routed through generic interactive handler. |

**Zero-renderer tags:** None found. Every normalised tag surfaced by the normaliser has either a dedicated branch or the generic interactive / body / default path catches it.

**Multi-renderer tags:** `flip_card` and `hint_slider` have dedicated branches that *fall through* to the generic interactive handler if the dedicated renderer returns `null` (block-renderer:342, 363). Not a conflict — deliberate fallback. `upload_to_dropbox` hits two branches in the same iteration (`block-renderer:370` sets `activityHasDropbox`, then the generic interactive handler emits the placeholder); these cooperate, not conflict.

### Activity/alert/sidebar class construction

Activity-closing code paths — all four exist and produce identical class strings:

| # | Path | Site | Class-string construction |
|---:|---|---|---|
| 1 | Auto-close on structural boundary | `block-renderer:168-190` | `activityHasDropbox ? 'activity dropbox' : (activityHasInteractive ? 'activity interactive' : 'activity')` + `' alertPadding'` if sidebar. |
| 2 | Duplicate flush when new `[activity]` seen while already in activity | `block-renderer:218-232` | Identical formula. |
| 3 | Explicit `[end activity]` close | `block-renderer:257-281` | Identical formula. |
| 4 | Final close at end-of-loop | `block-renderer:1107-1120` | Identical formula. |

All four paths construct the wrapper markup identically (outer row → col → `div class="..."` with optional `number` attr → inner row → col-12 → parts join). **Redundancy:** the class-string formula and the wrapper-markup template are duplicated verbatim four times — candidate for a private helper `_closeActivityWrapper()`. Flagged HC-R2 below.

Rule application consistency:

| Rule | Applied correctly? |
|---|---|
| `alertPadding` when `activityHasSidebar` | Yes — all 4 paths append `' alertPadding'` after the base class. |
| `dropbox` class for `upload_to_dropbox` interactive | Yes — `activityHasDropbox` set at `block-renderer:370`, consumed by all 4 close paths. |
| `col-md-8` default for body rows | Yes — `colClass` resolved from `config.gridRules.defaultContent` once at loop entry (`block-renderer:30`), used by every `_wrapInRow` call. |
| `alert top` in col-md-4 sidebars | Yes — `renderers._renderSidebarBlock` emits `alert top` for `_cellRole === 'sidebar_alert'` (`renderers:403`). |
| `col-md-8` / `col-md-4` side-by-side | Defaults in `renderers._wrapSideBySide` at `renderers:434-435`; explicit `col-md-6/col-md-3 paddingL/paddingR` override used for alert+sidebar layout-table pairing at `block-renderer:651-652`. |

### Escape-helper usage

`_escContent` vs `_escAttr` spot-checked across every renderer that emits one:

| Site | Helper used | Correct? |
|---|---|---|
| `block-renderer:176,226,267,1114` — activity `number="..."` attr | `_escAttr` | Yes. |
| `block-renderer:311` — `info="..."` attr on infoTrigger span | `_escAttr` | Yes. |
| `block-renderer:312` — visible trigger word | `_escContent` | Yes. |
| `block-renderer:425` — fallback placeholder visible text | `_escContent` | Yes. |
| `block-renderer:857` — `src="audio/..."` attr | `_escAttr` | Yes. |
| `block-renderer:870,885,907,913,940,1058` — `href="..."` attrs | `_escAttr` | Yes. |
| `block-renderer:908,914` — visible URL text | `_escContent` | Yes. |
| `block-renderer:909` — trailing punctuation inside `<p>` | `_escContent` | Yes. |
| `renderers:372` — img `alt="..."` attr | `_escAttr` | Yes. |
| `renderers:375` — HTML comment body `<!-- Reference: ... -->` | `_escContent` | Yes. |
| `renderers:672` — img `src="images/..."` attr | `_escAttr` | Yes. |
| `renderers:738,748,757,764` — iframe `src="..."` attrs | `_escAttr` | Yes. |
| `module-menu:263` — `<span>` inner text (H1 title) | `_escContent` | Yes. |
| `module-menu:266` — `<p>` inner text (description) | `_escContent` | Yes. |
| `module-menu:506` — `info="..."` attr on infoTrigger | `_escAttr` | Yes. |
| `lesson-menu:47,49,196,206,226,228,264,270,314,316,351,357` — `<h5>` / `<p>` inner text | `_escContent` | Yes. |

No misuses found. Escape-helper discipline is clean across all six sub-modules.

Dead helper storage: `html-converter-content-helpers.js:13-14` — constructor stores `_escContent` and `_escAttr` on `this` but neither is referenced anywhere in the class body (ContentHelpers does its own raw replacement in `_escapeContentPreservingTags`). Flagged HC-R3 below.

### Template-engine integration

Single entry path — `HtmlConverter.assemblePage` at `html-converter.js:296`:

- `this._templateEngine.generateSkeleton(config, skeletonData)` called exactly once per page (`html-converter.js:343`).
- Result stored in `skeleton`, then `skeleton.replace('<!-- CONTENT_PLACEHOLDER -->', bodyHtml)` once.
- Module menu content replaced by `this._replaceModuleMenuContent(...)` once (delegates to ModuleMenu sub-module).
- No other TemplateEngine call from any sub-module (grep confirmed).

Clean — one TemplateEngine call per page-assembly.

### Delegation shim inventory

Core `HtmlConverter` owns a large shim surface (44 shims on lines 93–263) so tests and downstream callers can continue to access private helpers through the core reference:

| Shim | Accessed from | Removable when |
|---|---|---|
| `_renderBlocks`, `_processAllBlocks`, `_processBlock`, `_buildFormattedText`, `_applyFormattingMarkers`, `_buildTableTextForTags` | sub-modules via `_coreRef` + existing tests | Tests migrate to the split sub-module classes directly. |
| `_convertInlineFormatting`, `_escapeContentPreservingTags`, `_stripFullHeadingFormatting`, `_stripHeadingInlineTags`, `_splitMultiHeadingText` | sub-modules via `_coreRef` + `block-renderer` uses `this._content.*` directly so core shims are only needed by tests | Test migration. |
| `_collectBlockContent`, `_collectAlertContent`, `_collectMultiLineContent`, `_extractUrlFromContent`, `_extractImageInfo`, `_extractAudioFilename`, `_extractLinkInfo`, `_extractExternalLinkInfo` | Same — sub-modules use `this._content.*`; shims exist for test access. | Test migration. |
| `_generateLessonMenuContent`, `_replaceModuleMenuContent`, `_splitMenuContentIntoTabs`, `_renderModuleMenuBlocks`, `_formatInfoTriggerDefinition` | `assemblePage` (internal) + tests | Call sites stay internal; inline if tests don't touch. |
| `_stripFullItalic`, `_renderMenuList`, `_extractHovertriggerData`, `_extractInfoTriggerData`, `_renderHovertriggerParagraph`, `_splitQuoteAttribution` | `_coreRef` callbacks from lesson-menu and block-renderer | ModuleMenu becomes constructor-injected into the consumers instead of routed via core. |
| `_renderTable`, `_renderCellContent`, `_renderTableAsGrid`, `_detectLayoutTable`, `_renderLayoutTable`, `_renderImagePlaceholder`, `_renderImage`, `_renderVideo`, `_renderSidebarBlock`, `_renderList`, `_wrapInRow`, `_wrapSideBySide`, `_hasTableTag` | Block-renderer uses `this._renderers.*` directly; shims exist for test access. | Test migration. |

All shims are thin one-liners routing to the corresponding sub-module. No shim contains behaviour that diverges from the delegated method. Potentially 30+ removable once the test suite is migrated; out of scope for this session.

### Phase attribution

| Code site | Introduced in |
|---|---|
| Activity class construction (four paths) + `alertPadding` / `dropbox` modifiers | Phase 7 — LMS Compliance (docs/17) |
| `whakatauki`, `download_journal`, `alert_cultural_*`, `quote` attribution split | Phase 7 (docs/17) |
| `hovertrigger`, `info_trigger` inline rendering, `hint_slider`/`flip_card` dedicated renderers, `external_link` / `external_link_button` / button-suffix handling | ENGS301 Issues #3/#6/#10/#12 (docs/16) |
| `_sidebarParagraphs` preservation in block-processor | Phase 13 — OSAI201 defects (docs/21) |
| `suppressDuplicateLessonTitleH2`, `_extractLessonTitle`, lesson-title H1 behaviour | Phase 13 — Years 4–6 (docs/22) |
| `_generateLessonMenuPromoteToH5`, `_generateLessonMenuOverviewBold`, `overviewTabHeadingLevel`, `wrapAllOverviewHeadingsInSpan`, `stripInfoTabTereoPrefix`, `overviewTabColumnClass`, `overviewTitleHeadingBehaviour` | Phase 15 — Multi-template skeleton calibration (docs/23) |
| Split into 6 sub-modules | Session 4b-1 + 4b-2 (docs/29) |
| Duplicate `menuHeadingTag` declaration at module-menu.js:185/190 | Phase 15 addition — earlier single declaration (`var menuHeadingTag = isInfoTab ? 'h5' : 'h4'`) left in place when Phase 15 added the config-driven second declaration. Pre-existing; preserved verbatim by the split. |
| Duplicate activity wrapper template (4 sites) | Predates the split — preserved verbatim. |
| Unused `_escContent` / `_escAttr` in ContentHelpers constructor | Split-introduced — constructor signature was generous; no consumer materialised. |

### Prioritised remediation list

Ranked **Conflict > Redundancy > Dead code > Documentation drift**. No remediation performed in this session.

| ID | Severity | Finding | Suggested fix | Test-coverage note |
|---|---|---|---|---|
| **HC-R1** | Redundancy | `module-menu.js:185` and `:190` both declare `var menuHeadingTag` — the first assignment (`isInfoTab ? 'h5' : 'h4'`) is immediately overwritten by the second (`isInfoTab ? 'h5' : overviewHeadingLevel`). Dead assignment. | Delete line 185 (the earlier declaration). Line 190's value is always correct because `overviewHeadingLevel` defaults to `'h4'` (line 187). | Overview / info tab heading behaviour covered by existing module-menu tests; behaviour is unchanged after removal (line 190 strictly subsumes line 185). |
| **HC-R2** | Redundancy | Activity-closing wrapper template (`'<div class="' + cls + '" number="..."><div class="row"><div class="col-12">` + parts + `</div></div></div>`) duplicated verbatim at `block-renderer:170-180`, `:219-230`, `:266-271`, and `:1113-1118`. Class-string formula is identical. Any future tweak must be mirrored four times. | Extract `_closeActivityWrapper(parts, hasDropbox, hasInteractive, hasSidebar, activityId)` private helper; call from all four sites. Saves ~30 lines. | Fully covered by activity-wrapper tests in `tests/activityClass.test.js` (and equivalent integration tests); any refactor must preserve the four call-site semantics (auto-close, duplicate flush, end_activity, final close). |
| **HC-R3** | Dead code | `html-converter-content-helpers.js:13-14` stores `_escContent` and `_escAttr` on `this` but the class body never references either. | Drop the two lines and the `escContent`/`escAttr` constructor parameters, plus the `this._escContent.bind(this), this._escAttr.bind(this)` at `html-converter.js:44-45`. | No test impact — helpers never called on ContentHelpers. |
| **HC-R4** | Dead code | `_sidebarParagraphs` preserved at `block-processor.js:76-77` (set by `layout-table-unwrapper.js:631,656`) but never consumed by any renderer in the html-converter pipeline. Renderers key off `_sidebarImageUrl` and `_sidebarAlertContent` only. | Either consume `_sidebarParagraphs` in `_renderSidebarBlock` (sidebar-alert uses `_sidebarAlertContent` instead) or stop preserving it. Prefer stop-preserving — drop block-processor.js:76-77 and the two unwrapper assignments. | `tests/osai201Defects.test.js` references `_sidebarParagraphs` — audit test expectations before removal. |
| **HC-R5** | Documentation drift | `block-renderer.js:381-388` references "Session F / Session G" boundary algorithm without pointing to a docs file. Session 1 audit already flagged the same bare label for `isInteractiveEndSignal`. | Cross-reference the actual Session F / G doc (or drop the label). | None — documentation-only. |
| **HC-R6** | Size-target miss | `block-renderer.js` landed at 1124 lines (target ≤1115 per plan). `renderers.js` at 798 lines (no explicit target). Core at 641 (no explicit target; split succeeded at –3409). | Plan already accepts `block-renderer` as the mega-method owner. Future refactor could extract the alert/layout-table pairing block (~60 lines at 588-669) into a dedicated helper. Out of scope for this session. | Non-functional. |
| **HC-R7** | Shim trim | ~30+ delegation shims on the core `HtmlConverter` class exist only for test access; sub-module internal callers already use `this._content.*` / `this._renderers.*` directly. | Future refactor — migrate tests to construct sub-modules directly; delete the shims. Out of scope for this session. | Requires test suite migration; non-trivial. |

No remediation performed in this session.





