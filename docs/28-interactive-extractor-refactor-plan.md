# 28. Interactive Extractor Refactor Plan (Session 3a)

## Status

Plan complete — ready for Session 3b execution.

## Baseline

- `js/interactive-extractor.js` — **2245 lines**
- Test suite — **571/571 passing** (`node tests/test-runner.js`)
- Branch — `claude/read-claude-index-ZW4lk`
- Prior plan files (audit results cross-referenced below):
  - [`docs/26-tag-normaliser-refactor-plan.md`](26-tag-normaliser-refactor-plan.md) — Session 1 normaliser split
  - [`docs/27-block-scoper-refactor-plan.md`](27-block-scoper-refactor-plan.md) — Session 2 block-scoper split

## Target sub-modules

Survey shows a clean four-way seam — an extra split of cell/table parsing from the main block-stream orchestrator keeps every new file under the 500-line ceiling Session 2 achieved. Three-way splits were rejected because either the data-extractor (~820 lines) or the core (~700 lines) overshoots. Four sub-modules is within the "max five new" budget Sessions 1–2 observed.

| New file | Responsibility | Source line range | Moved methods | Est. lines |
|---|---|---|---|---:|
| `js/interactive-extractor-tables.js` | Pure data constants: tier membership, 13 data-pattern names, type→pattern map, sub-tag type list, wide-column types | 24–113 | _none — five instance fields only_ | ~75 |
| `js/interactive-cell-parser.js` | Paragraph/run → formatted-text conversion; cell/table text extraction; inline media extraction; table-pattern classification | 1184–1553 (plus 1413–1505 text helpers) | `_buildFormattedText`, `_applyFormattingMarkers`, `_buildTableText`, `_extractTableData`, `_extractCellText`, `_extractCellContentClean`, `_detectTablePattern`, `_extractMediaFromTable`, `_extractMediaFromText` | ~290 |
| `js/interactive-data-extractor.js` | Block-stream orchestration: the 13-pattern `_extractData` flow, numbered-item collection, sub-tag/boundary predicates, Session F/G boundary walker | 549–1172, 1561–1566, 2112–2244 | `_extractData`, `_collectNumberedItems`, `_isSubTagFor`, `_isEndBoundary`, `_extractBlockInstructions`, `_consumeInteractiveBoundary` | ~640 |
| `js/interactive-placeholder-renderer.js` | Placeholder HTML assembly: dashed-border shell, tier colour classes, content-preview body, `_escContent`, col-class decision, data-summary string | 1616–1652, 1664–2005, 2062–2068 | `_generatePlaceholderHtml`, `_generateContentPreview`, `_getColumnClass`, `_buildDataSummary`, `_escContent` | ~395 |

### What stays in core `js/interactive-extractor.js`

- Constructor (instantiates the four sub-modules).
- `processInteractive` — public orchestrator, preserved unchanged from the caller's perspective.
- `generateReferenceDocument` — public text-reference-document builder; retained in core because it spans every entry's metadata and uses both the cell-parser text helpers and `_formatReferenceData`.
- `_formatReferenceData` — per-entry helper for the reference document only.
- `_buildPositionContext` — called only by `processInteractive` for the "After heading …" string; small and local.
- Tag-detection helpers: `_getInteractiveTag`, `_getBlockTag`, `_getBlockPrimaryTag`, `_getBlockTagResult` (facade over `TagNormaliser.processBlock` that every sub-module reaches into via their own paragraph/table → tag-result flow). `_getBlockTag` and `_getBlockPrimaryTag` are unreferenced internally — flagged for Session 3c.
- Dead helper `_escAttr` (unused everywhere) — flagged for Session 3c.

Expected post-split size of core: **~430 lines**.

## Extraction order

Work from the highest line ranges downward so earlier deletions do not shift later ranges. Session 3b commits after each sub-module extraction.

1. **Extract tables** first so later sub-modules can depend on it via constructor injection (though tables lives low in the file, it has no intra-class dependencies and is trivial to move).
2. **Extract placeholder renderer** next — it sits at the bottom of the file (lines 1616–2068). Taking it out early shrinks the remaining line range the data-extractor regex/sed will have to operate on.
3. **Extract cell-parser** — mid-file (1184–1553) plus the text-helper block (1413–1505). Safe to move after renderer because nothing above line 1184 depends on anything inside the cell-parser block.
4. **Extract data-extractor** last — spans from line 549 up to the trailing `_consumeInteractiveBoundary` at 2112. Most state-rich; also the largest. Extracting it last means the core's remaining shape is already visible when we design its delegations.

## Dependency graph

```
                     ┌───────────────────────────┐
                     │ interactive-extractor-tables│ (no deps)
                     └────────────┬───────────────┘
                                  │
          ┌──────────────────────┬┴───────────────────────────┐
          │                      │                            │
          ▼                      ▼                            ▼
 ┌──────────────────┐ ┌────────────────────────┐ ┌─────────────────────────────┐
 │ interactive-cell │ │ interactive-data-      │ │ interactive-placeholder-    │
 │ parser           │ │ extractor              │ │ renderer                    │
 │ (tagNormaliser)  │ │ (tagNormaliser, tables,│ │ (tables, cellParser)        │
 └────────┬─────────┘ │  cellParser)           │ └─────────────┬───────────────┘
          │           └────────────┬───────────┘               │
          │                        │                           │
          └───────────┬────────────┴──────────┬────────────────┘
                      │                       │
                      ▼                       ▼
               ┌───────────────────────────────────┐
               │  InteractiveExtractor (core)      │
               │  owns: processInteractive,        │
               │         generateReferenceDocument │
               └───────────────────────────────────┘
```

- `interactive-extractor-tables` — zero deps; pure data export.
- `interactive-cell-parser` — needs `tagNormaliser` for `processBlock` (inside `_extractCellText`, `_extractCellContentClean`) and for `reassembleFragmentedTags` (inside `_buildFormattedText`). No coupling to tables.
- `interactive-data-extractor` — needs `tagNormaliser` (pervasive `processBlock` / `isInteractiveEndSignal` calls), `tables` (`_typeToPrimaryPattern` lookups in `_extractData` for `expectsSubTags` and type→pattern mapping), and `cellParser` (for `_extractTableData`, `_extractMediaFromTable`, `_extractMediaFromText`, plus `_buildFormattedText` reused in boundary capture).
- `interactive-placeholder-renderer` — needs `tables` (`_patternNames` for labels, `_wideColTypes` for `_getColumnClass`) and `cellParser` (for `_buildFormattedText` / `_buildTableText` used inside the `childBlocks` render loop at current lines 1753/1755).
- Core `InteractiveExtractor` — wires the four sub-modules, delegates everything moved, and keeps `processInteractive` / `generateReferenceDocument` as the two public entry points.

## Constructor signatures

```js
// js/interactive-extractor-tables.js
class InteractiveExtractorTables {
    constructor() { /* TIER_1_TYPES, patternNames, typeToPrimaryPattern, subTagTypes, wideColTypes */ }
}
```

```js
// js/interactive-cell-parser.js
class InteractiveCellParser {
    constructor(tagNormaliser) { /* retains tagNormaliser for processBlock / reassembleFragmentedTags */ }
}
```

```js
// js/interactive-data-extractor.js
class InteractiveDataExtractor {
    constructor(tagNormaliser, tables, cellParser) { /* block-stream walker */ }
}
```

```js
// js/interactive-placeholder-renderer.js
class InteractivePlaceholderRenderer {
    constructor(tables, cellParser) { /* HTML emitter */ }
}
```

```js
// js/interactive-extractor.js (core — constructor only)
class InteractiveExtractor {
    constructor(tagNormaliser) {
        this._normaliser = tagNormaliser;
        this._tables = new InteractiveExtractorTables();
        this._cellParser = new InteractiveCellParser(tagNormaliser);
        this._dataExtractor = new InteractiveDataExtractor(tagNormaliser, this._tables, this._cellParser);
        this._renderer = new InteractivePlaceholderRenderer(this._tables, this._cellParser);
    }
}
```

## External API preservation

Grep against `js/*.js` and `tests/*.test.js` surfaced only two externally-called symbols — both stay as public methods on the core class, so no delegation shims are required.

| Symbol | External consumer(s) | Treatment |
|---|---|---|
| `new InteractiveExtractor(tagNormaliser)` | `js/app.js:20`; four test files instantiate directly | **Preserved** — constructor signature unchanged; sub-modules wired inside. |
| `processInteractive(blocks, startIndex, filename, activityId, insideActivity)` | `js/html-converter.js:930`; `tests/interactiveBoundaryAlgorithm.test.js` (×6), `tests/interactivePlaceholderFidelity.test.js` (×5), `tests/activityWrapperBoundary.test.js` (×6), `tests/interactiveBoundaryIntegration.test.js` (×6) | **Preserved as public method on core.** Body delegates to sub-modules. |
| `generateReferenceDocument(allInteractives, moduleCode)` | `js/app.js:1205`; `tests/interactiveBoundaryIntegration.test.js` (×2) | **Preserved as public method on core.** Body remains in core. |

`collectedInteractives` is a property of `HtmlConverter` (and mirrored on `App`), not of `InteractiveExtractor`, so it is unaffected by this refactor.

No test accesses any private helper (`_extractData`, `_generatePlaceholderHtml`, `_consumeInteractiveBoundary`, etc.) directly — confirmed by grep. Session 3b therefore does **not** need the kind of test-facing delegation shims that Sessions 1–2 retained (`normaliseSubTag`, `_matchOpeningTag`, etc.). This is a clean refactor.

## Internal-reference renames

Session 3b's `sed -i` pass rewrites every intra-class reference to route through the new sub-modules. Pairs listed below; ordering principle: **longest match first** so a shorter prefix cannot consume a later rename (e.g., `this._extractMediaFromTable` must run before `this._extractMedia`, and table-field renames like `this._typeToPrimaryPattern` must run before `this._type`).

**Tables field rewrites (run before any method rewrite):**

| From | To |
|---|---|
| `this._typeToPrimaryPattern` | `this._tables.typeToPrimaryPattern` |
| `this._patternNames` | `this._tables.patternNames` |
| `this._subTagTypes` | `this._tables.subTagTypes` |
| `this._wideColTypes` | `this._tables.wideColTypes` |
| `this.TIER_1_TYPES` | `this._tables.TIER_1_TYPES` |

**Cell-parser method rewrites (longest-first):**

| From | To |
|---|---|
| `this._extractCellContentClean(` | `this._cellParser._extractCellContentClean(` |
| `this._extractMediaFromTable(` | `this._cellParser._extractMediaFromTable(` |
| `this._extractMediaFromText(` | `this._cellParser._extractMediaFromText(` |
| `this._applyFormattingMarkers(` | `this._cellParser._applyFormattingMarkers(` |
| `this._detectTablePattern(` | `this._cellParser._detectTablePattern(` |
| `this._extractTableData(` | `this._cellParser._extractTableData(` |
| `this._extractCellText(` | `this._cellParser._extractCellText(` |
| `this._buildFormattedText(` | `this._cellParser._buildFormattedText(` |
| `this._buildTableText(` | `this._cellParser._buildTableText(` |

**Data-extractor method rewrites (longest-first):**

| From | To |
|---|---|
| `this._consumeInteractiveBoundary(` | `this._dataExtractor._consumeInteractiveBoundary(` |
| `this._extractBlockInstructions(` | `this._dataExtractor._extractBlockInstructions(` |
| `this._collectNumberedItems(` | `this._dataExtractor._collectNumberedItems(` |
| `this._isEndBoundary(` | `this._dataExtractor._isEndBoundary(` |
| `this._isSubTagFor(` | `this._dataExtractor._isSubTagFor(` |
| `this._extractData(` | `this._dataExtractor._extractData(` |

**Placeholder-renderer method rewrites:**

| From | To |
|---|---|
| `this._generatePlaceholderHtml(` | `this._renderer._generatePlaceholderHtml(` |
| `this._generateContentPreview(` | `this._renderer._generateContentPreview(` |
| `this._buildDataSummary(` | `this._renderer._buildDataSummary(` |
| `this._getColumnClass(` | `this._renderer._getColumnClass(` |
| `this._escContent(` | `this._renderer._escContent(` |

Within each new sub-module, `this._X(…)` calls that stay inside the same sub-module need no rewrite. Calls that cross sub-modules become `this._cellParser.X(…)` etc. inside the caller sub-module's constructor-injected reference.

## Core class delegation edits

After the sed pass, Session 3b replaces (or leaves as single-line delegations) the following in-place method bodies on the core class:

- `processInteractive` — body retained; all `this._X(…)` calls already rewritten to sub-module references by sed.
- `generateReferenceDocument` — body retained; `_buildFormattedText` / `_buildTableText` calls rewritten.
- `_formatReferenceData` — stays; no rewrites needed (uses only `this._patternNames` → `this._tables.patternNames`).
- `_buildPositionContext` — stays; no rewrites needed (uses only `this._getBlockTagResult` which also stays in core).
- Tag-detection helpers (`_getInteractiveTag`, `_getBlockTag`, `_getBlockPrimaryTag`, `_getBlockTagResult`) — stay in core; `_buildFormattedText` / `_buildTableText` calls rewritten to `this._cellParser.*`.

No methods are collapsed into shims — the core class simply calls into sub-module references. Sections `// Internal: Data extraction`, `// Internal: Table data extraction`, `// Internal: Text building helpers`, `// Internal: Media extraction`, `// Internal: Placeholder HTML generation`, and `// Boundary detection (Session F)` are removed from core along with their method bodies.

## Wiring

- `index.html` — add the new `<script>` tags in dependency order **before** `<script src="js/interactive-extractor.js">`:
  1. `js/interactive-extractor-tables.js`
  2. `js/interactive-cell-parser.js`
  3. `js/interactive-data-extractor.js`
  4. `js/interactive-placeholder-renderer.js`

- `tests/test-runner.js` — add matching `loadScript('…')` calls in the same dependency order **before** `loadScript('js/interactive-extractor.js')`.

## Test checkpoints for Session 3b

After each sub-module extraction: run `node tests/test-runner.js`, confirm **571/571** still pass, then commit and push. Commit message format:

```
Session 3b: extract <module-name> from interactive-extractor.js (571/571 passing)
```

Order of commits mirrors the extraction order above:

1. `Session 3b: extract interactive-extractor-tables.js from interactive-extractor.js (571/571 passing)`
2. `Session 3b: extract interactive-placeholder-renderer.js from interactive-extractor.js (571/571 passing)`
3. `Session 3b: extract interactive-cell-parser.js from interactive-extractor.js (571/571 passing)`
4. `Session 3b: extract interactive-data-extractor.js from interactive-extractor.js (571/571 passing)`

## Rollback commands for Session 3b

- **Single-module rollback** (revert the most recent extraction commit only):
  ```
  git reset --hard HEAD~1
  ```
- **Full-session rollback** (revert all Session 3b commits back to the Session 3a baseline):
  ```
  git reset --hard <Session 3a plan commit sha>
  ```

## Cross-reference notes for Session 3c

When Session 3c audits the split, the following Session 1/2 remediation items may have downstream handling inside `js/interactive-extractor.js` that warrants verification:

- **Session 1 R-1 / R-3 / R-4** (`word_highlighter`, `slide_show` dead key, `info_trigger] image` niche literals) — `_typeToPrimaryPattern` keys `word_highlighter` and `info_trigger_image`, plus the boundary/sub-tag handling in `_extractData` and `_isSubTagFor`, should be cross-checked so a taxonomy cleanup does not strand extractor paths.
- **Session 1 R-2** (`translate_section`, `kanji_cards` drift) — both types already have rows in `_typeToPrimaryPattern`. Confirm no extractor-side branches exist that the docs/10 update would invalidate.
- **Session 2 BS-R2 / BS-R3** (`speech_bubble` and `rotating banner` missing closer paths) — both types participate in `_extractData` and `_consumeInteractiveBoundary`. If the block-scoper ever gains a closer path, audit whether `_isEndBoundary` and the `_consumeInteractiveBoundary` end-signal rule still trigger correctly.
- **Dead-helper flags local to this file** — `_getBlockTag`, `_getBlockPrimaryTag`, `_escAttr` appear defined but never called from anywhere in `js/*.js` or `tests/*.test.js`. Session 3c should formally classify and decide whether to remove.

[← Back to index](../CLAUDE.md)
