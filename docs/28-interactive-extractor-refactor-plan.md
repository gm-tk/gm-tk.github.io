# 28. Interactive Extractor Refactor Plan (Session 3a)

## Status

DONE — split executed, audit complete, 571/571 tests passing.

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

## Audit Results

### Sub-module inventory

| File | Lines |
|---|---:|
| `js/interactive-extractor.js`          | 559 |
| `js/interactive-data-extractor.js`     | 872 |
| `js/interactive-placeholder-renderer.js` | 430 |
| `js/interactive-cell-parser.js`        | 397 |
| `js/interactive-extractor-tables.js`   | 106 |

Core dropped from 2245 → 559 (–1686). `interactive-data-extractor.js` overshoots the 500-line ceiling Session 2 achieved by +372 lines (pattern-4 DQP + pattern-9 speech_bubble + main walker + boundary walker all co-reside). Further splitting out of scope for 3c. Tests: 571/571.

### Cross-reference with Sessions 1–2 findings

| Tag | Upstream classification | Interactive-extractor handling site | Relative classification |
|---|---|---|---|
| `word_highlighter` (S1 R-1) | Documentation drift — emitted as distinct name vs docs/10 alias | `tables.js:63` (pattern 10); `cell-parser.js:192` (`_detectTablePattern` alias of `word_select`); `data-extractor.js:423` (plain-text capture branch) | **Three-site downstream** — if R-1 collapses `word_highlighter` → `word_select`, all three sites simplify to the `word_select` branch. Cell-parser and data-extractor already treat them identically; the tables.js distinct row is the only behavioural differentiator (none). |
| `translate_section`, `kanji_cards` (S1 R-2) | Documentation drift — absent from docs/10 | `tables.js:88-89` (pattern 1 each) | Consumer only — both route through pattern-1 default. R-2 is docs-only; no extractor change needed. |
| `slide_show` (S1 R-3 / D-2) | Dead key in `interactiveChildTagsMap` | Not referenced — extractor consumes `tagInfo.interactiveChildTags` via the live `carousel` entry, never the dead `slide_show` entry | No impact. |
| `info_trigger] image` literals (S1 R-4 / D-1) | Dead via pipeline | Not referenced — extractor keys on normalised names, not raw strings | No impact. |
| `info_trigger_image` / `info_trigger` redundancy (S1 R-5) | Redundancy internal to normaliser | `tables.js:68-69` (patterns 1 and 12); `cell-parser.js:202` (pattern 12) | Consumer only — both producers funnel through one `typeToPrimaryPattern` entry per name. |
| `speech_bubble` (S2 BS-R2) | Conflict — opener but no block-scoper closer | `data-extractor.js:217` (pattern-9 conversation); `data-extractor.js:722` (`isConversationStyle` flag in boundary walker); `cell-parser.js:212` (pattern 8); `tables.js:53` | Downstream depends on `_isEndBoundary` + `TagNormaliser.isInteractiveEndSignal` rather than a block-scoper closer. If BS-R2 adds an explicit closer, audit `_consumeInteractiveBoundary` line 783 still triggers correctly. |
| `rotating_banner` (S2 BS-R3) | Conflict — opener but no block-scoper closer | `tables.js:51` (pattern 5); `data-extractor.js:479` (`_isSubTagFor` — `carousel_slide` belongs to `rotating_banner`); `data-extractor.js:567` (pattern-5 assignment in `_collectNumberedItems`) | Same as above — relies on boundary signals, not explicit closer. If BS-R3 adds closer, re-verify `_isEndBoundary` and the numbered-items walker still terminate correctly. |

### Interactive type coverage

`typeToPrimaryPattern` enumerates 45 interactive types. `TIER_1_TYPES` lists 4. `subTagTypes` lists 5. `wideColTypes` lists 2.

Types in code not documented in docs/12 taxonomy (cross-reference S1 findings):

| Type | Source | Notes |
|---|---|---|
| `word_highlighter` | `tables.js:63` | S1 R-1 — docs/10 collapses into `word_select`. |
| `translate_section` | `tables.js:88` | S1 R-2 — absent from docs/10. |
| `kanji_cards` | `tables.js:89` | S1 R-2 — absent from docs/10. |

Types in docs/12 not in code: none — every type enumerated in the docs/12 pattern table has a matching `typeToPrimaryPattern` entry.

### Data pattern coverage

Per docs/12 the writer surface defines 13 data patterns. Each pattern's reachability in the extractor sub-modules:

| Pattern | Detected by | Rendered by | Status |
|---:|---|---|---|
| 1  | `typeToPrimaryPattern` fallback (20+ types); `cell-parser.js:217` default | `renderer.js:277` default table branch | Reachable |
| 2  | `cell-parser.js:182` (flip_card/click_drop); `data-extractor.js:573` | `renderer.js:269` (table), `renderer.js:380` (numbered) | Reachable |
| 3  | `cell-parser.js:187` (hint_slider); `data-extractor.js:575` | `renderer.js:271` | Reachable |
| 4  | `data-extractor.js:94-214` (dropdown_quiz_paragraph special block); `data-extractor.js:434` (word_highlighter/word_select plain-text) | `renderer.js:311` (DQP-specific); falls through to default for word-select Pattern-4 | Reachable |
| 5  | `data-extractor.js:567` (carousel/rotating_banner) | `renderer.js:399` default numbered-items branch | Reachable |
| 6  | `data-extractor.js:569` (shape_hover/tabs) | `renderer.js:399` default numbered-items branch | Reachable |
| 7  | `data-extractor.js:571` (accordion) | `renderer.js:399` default numbered-items branch | Reachable |
| 8  | `cell-parser.js:212` (speech_bubble table) | `renderer.js:273` | Reachable |
| 9  | `data-extractor.js:238` (speech_bubble + conversation modifier) | `renderer.js:357` | Reachable |
| 10 | `cell-parser.js:192` (word_select/word_highlighter) | `renderer.js:275` | Reachable |
| 11 | `cell-parser.js:197` (slider_chart) | **No dedicated renderer branch** — falls through to `renderer.js:277` default "Data: Table (dims)" label. Not a dead branch (pattern still detected and stored) but preview label omits "Axis Labels" semantics. **Minor drift** — flagged IE-R3 below. |
| 12 | `cell-parser.js:202` (info_trigger_image) | **No dedicated renderer branch** — falls through to `renderer.js:277` default. Minor drift — flagged IE-R3. |
| 13 | `cell-parser.js:207` (multichoice_quiz_survey) | **No dedicated renderer branch** — falls through to `renderer.js:277` default. Minor drift — flagged IE-R3. |

No pattern branch is unreachable. Patterns 11/12/13 are detected but their preview labels collapse to the generic table label.

### Tier classification consistency

Sole assignment site: `interactive-extractor.js:56` — `this._tables.TIER_1_TYPES.indexOf(interactiveType) !== -1 ? 1 : 2`. Membership source: `tables.js:19` — `['accordion', 'flip_card', 'speech_bubble', 'tabs']`.

| Type | Tier (code) | Tier (docs/12 §Tier table) | Match |
|---|---:|---:|---|
| `accordion`       | 1 | 1 | yes |
| `flip_card`       | 1 | 1 | yes |
| `speech_bubble`   | 1 | 1 | yes |
| `tabs`            | 1 | 1 | yes |
| All other types   | 2 | 2 | yes (blanket "Everything else" rule) |

Single assignment path. No ambiguous or conflicting tier cases.

### Placeholder rendering path overlap

Single public entry: `InteractivePlaceholderRenderer._generatePlaceholderHtml`. Internal dispatch is a two-level decision — (1) `tableData` vs `numberedItems` vs fallback; (2) within each, a `dataPattern`/`type` switch.

| Type | Dispatch path |
|---|---|
| `dropdown_quiz_paragraph` (pattern 4) | `renderer.js:263` guard skips the `tableData`-only branch even when a table was captured, so the numbered-items branch at `renderer.js:311` handles both story text **and** the options table in one place. |
| `speech_bubble` (pattern 8) | `renderer.js:273` table branch. |
| `speech_bubble` + conversation (pattern 9) | `renderer.js:357` numbered-items branch. |
| `flip_card` / `click_drop` (pattern 2) | If `tableData` → `renderer.js:269`; if `numberedItems` → `renderer.js:380`. Mutually exclusive: `_extractData` sets either `tableData` (table layout) or `numberedItems` (per-card sub-tag layout), never both for the same interactive. |
| Everything else | Single default path per branch. |

No type has two paths that could both render it in a single invocation. The flip_card/click_drop dual-form case is a valid writer-surface choice, not an ambiguity.

### Delegation shim inventory

Session 3b deliberately avoided creating test-facing shims because no test touches private helpers of `InteractiveExtractor`. Surviving shims / duplicates on the core class:

| Shim / duplicate | Accessed from | Removable when |
|---|---|---|
| `_getInteractiveTag` on core (`interactive-extractor.js:365`) | `processInteractive:48` only | Now — single call site. Duplicated verbatim as `_getInteractiveTag` inside `interactive-data-extractor.js:835`; consolidating would save ~27 lines. |
| `_getBlockTagResult` on core (`interactive-extractor.js:438`) | `_buildPositionContext:467` only | Now — single call site. Duplicated verbatim as `_getBlockTagResult` inside `interactive-data-extractor.js:861`; consolidating would save ~11 lines. |
| `_getBlockTag` on core (`interactive-extractor.js:400`) | Nowhere (grepped `js/*.js` + `tests/*.test.js`) | **Removable now** — confirmed dead. Plan §4 already flagged. |
| `_getBlockPrimaryTag` on core (`interactive-extractor.js:421`) | Nowhere | **Removable now** — confirmed dead. Plan §4 already flagged. |
| `_escAttr` on core (`interactive-extractor.js:550`) | Nowhere | **Removable now** — confirmed dead. Plan §4 already flagged. |

Duplicated helpers in `interactive-data-extractor.js` (lines 835 and 861) exist because Session 3b's sed pass left `this._getInteractiveTag(...)` / `this._getBlockTagResult(...)` intra-class calls untouched inside the extracted data-extractor body; re-routing them through a constructor-injected reference to the core (or lifting both helpers into a shared sub-module) would eliminate the duplication.

### Phase attribution

| Finding | Introduced in |
|---|---|
| `_getInteractiveTag` / `_getBlockTagResult` duplicated in core + data-extractor | Session 3b split (docs/28) — created by the extraction sed pass. |
| `_getBlockTag`, `_getBlockPrimaryTag`, `_escAttr` dead on core | phase unclear — predate the split. Plan §4 already flagged at 3a time. |
| `word_highlighter` pattern-10 entry + plain-text branch | ENGS301 (docs/16 Issue #8). |
| `translate_section`, `kanji_cards` pattern-1 entries | ENGS301 (docs/16). |
| Pattern-4 DQP special block (`data-extractor.js:94-214`) | "Bug 3 fix Round 3C" — phase unclear; comment references Round 3C directly. |
| Pattern-9 conversation layout | Session F / G (docs/12 §§Session F, Session G). |
| `_consumeInteractiveBoundary` + `isInteractiveEndSignal` threading | Session F (boundary core) + Session G (activity context). |
| Patterns 11/12/13 lacking dedicated renderer branches | phase unclear — pattern detection added without matching preview branch. |

### Prioritised remediation list

Ranked **Conflict > Redundancy > Dead code > Documentation drift**. No remediation performed in this session.

| ID | Severity | Finding | Suggested fix | Test-coverage note |
|---|---|---|---|---|
| **IE-R1** | Redundancy | `_getInteractiveTag` and `_getBlockTagResult` duplicated in `interactive-extractor.js` (core) and `interactive-data-extractor.js`. Two copies must be kept in sync manually. | Inject a reference to either the core or a shared helper sub-module into `InteractiveDataExtractor`'s constructor; delete the duplicated private copies at `data-extractor.js:835,861`. Saves ~40 lines. | No test accesses either helper directly; behaviour covered by every `processInteractive` integration test in `interactiveBoundaryIntegration.test.js`, `interactiveBoundaryAlgorithm.test.js`, `interactivePlaceholderFidelity.test.js`. |
| **IE-R2** | Dead code | `_getBlockTag` (`interactive-extractor.js:400`), `_getBlockPrimaryTag` (`interactive-extractor.js:421`), `_escAttr` (`interactive-extractor.js:550`) defined but never called from `js/*.js` or `tests/*.test.js`. | Delete all three methods. ~25 lines saved. | No test impact — confirmed by grep. |
| **IE-R3** | Documentation drift | Patterns 11 (axis labels), 12 (info trigger image), 13 (self-assessment/survey) are assigned by `_detectTablePattern` but `_generateContentPreview` has no pattern-specific preview branch for them; they fall through to the generic "Data: Table (dims)" label. | Add explicit preview branches for patterns 11/12/13 mirroring patterns 2/3/8/10, or document the fallback behaviour in docs/12. | Preview text asserted by `interactivePlaceholderFidelity.test.js`; any label change needs a regression lock first. |
| **IE-R4** | Size-target miss | `interactive-data-extractor.js` landed at 872 lines (target ≤500). Three orthogonal concerns co-reside: DQP pattern-4 block, speech_bubble pattern-9 block, main `_extractData` walker plus `_consumeInteractiveBoundary`. | Future refactor — extract DQP and speech_bubble special-handling blocks into their own helper objects; keep the main walker core. Out of scope for 3c. | Non-functional. Fully covered by integration tests. |
| **IE-R5** | Downstream coupling | `word_highlighter` occupies three sites (tables, cell-parser, data-extractor plain-text branch) that all behave identically to `word_select`. If S1 R-1 collapses the normaliser, all three sites simplify to the `word_select` branch. | Done as part of S1 R-1 follow-up — tables entry becomes redundant alias, cell-parser and data-extractor branches can drop the `word_highlighter` disjunct. Add regression test first locking current behaviour per S1 R-1 note. | Gated by S1 R-1 regression lock. |




