# 27 — Block Scoper Refactor Plan (Session 2a)

## 1. Status

Plan complete — ready for Session 2b execution.

## 2. Baseline

- **File:** `js/block-scoper.js` — 1759 lines
- **Tests:** 571/571 passing
- **Branch:** `claude/read-project-docs-bLLDX`
- **Session 1 reference:** [`docs/26-tag-normaliser-refactor-plan.md`](26-tag-normaliser-refactor-plan.md) (pattern to mirror: constructor-injected `_tables`, dedicated sub-matcher module, delegation shims on the core class)

Session 2 is split into three parts — 2a plan (this file), 2b execute, 2c audit.

## 3. Target sub-modules

| New file | Responsibility | Source line range | Moved methods | Est. lines |
|---|---|---|---|---|
| `js/block-scoper-tables.js` | Static lookup tables (ordinals, block-type keywords, closer types, hard-boundary tags, prefix-strip list) | 841–931 | `_buildOrdinalMap`, `_buildBlockPatterns` (bodies inlined into constructor) | ~100 |
| `js/block-subtag-matcher.js` | Sub-tag normalisation (accordion tab, flip card, carousel slide, tab) + `_lastCardFrontIndex` state | 230–266, 1462–1692 | `normaliseSubTag`, `_matchAccordionTab`, `_matchFlipCardSubTag`, `_matchCarouselSlide`, `_matchTabSubTag` | ~300 |
| `js/block-tag-matcher.js` | Opener/closer/boundary matching | 987–1419 | `_matchOpeningTag`, `_getBlockTypeFromNormalised`, `_fuzzyMatchOpener`, `_extractWriterNotesFromTag`, `_getTextAfterBlockKeyword`, `_matchClosingTag`, `_fuzzyMatchCloser`, `_isHardBoundary` | ~440 |

Note: `normaliseSubTag` (230–266) and the four `_match*SubTag` helpers (1462–1692) are non-contiguous in the source but belong to the same logical module.

## 4. Extraction order

Extract in this order so each deletion minimally invalidates subsequent line ranges:

1. **`block-subtag-matcher.js` first** — its helpers occupy the highest tail range (1462–1692) plus `normaliseSubTag` at 230–266. Deleting the tail first (bottom-up) keeps earlier line numbers stable during the operation; the head deletion of `normaliseSubTag` happens last within the same step. After this extraction the tag-matcher and tables ranges shift up by ~37 lines (the size of the deleted `normaliseSubTag` block), but the tail-helper deletion has no effect on their positions.
2. **`block-tag-matcher.js` second** — its range (originally 998–1419) sits between tables and the already-removed subtag helpers. Extracting it before tables avoids reshuffling tables' position during the operation.
3. **`block-scoper-tables.js` last** — lowest starting line (841). Extracting it last means its range has been unaffected by the two prior extractions (both deletions occur below line 931). Session 2b should still re-run `grep -n "_buildOrdinalMap\|_buildBlockPatterns"` to confirm the updated range before extracting.

## 5. Dependency graph

- `BlockScoperTables` — no dependencies; constructor builds all lookup data.
- `BlockSubtagMatcher` — depends on `BlockScoperTables` (reads `ordinalMap`); owns mutable `_lastCardFrontIndex` state.
- `BlockTagMatcher` — depends on `BlockScoperTables` (reads `blockTypeKeywords`, `closerTypeMap`) and on a callable reference to the core class's `detectWriterInstruction`.
- Core `BlockScoper` — owns the three instances, exposes delegation shims, retains all other public methods unchanged.

`detectWriterInstruction` stays on the core class because (a) it has no dependency on the new sub-modules, (b) tests access it directly on the core class, and (c) moving it would expand scope beyond this refactor.

## 6. Constructor signatures

```js
class BlockScoperTables {
    constructor() { /* builds ordinalMap, blockTypeKeywords, closerTypeMap, hardBoundaryTags, blockOpenPrefixStrip */ }
}

class BlockSubtagMatcher {
    constructor(tables) { /* stores this._tables; initialises this._lastCardFrontIndex = null */ }
}

class BlockTagMatcher {
    constructor(tables, detectWriterInstructionFn) { /* stores this._tables and this._detectWriterInstructionFn */ }
}
```

In the core `BlockScoper` constructor (currently lines 19–38), replace the two `_build*()` calls and the `_lastCardFrontIndex = null` assignment with, in order:

```js
this._tables = new BlockScoperTables();
this._subtagMatcher = new BlockSubtagMatcher(this._tables);
this._tagMatcher = new BlockTagMatcher(this._tables, this.detectWriterInstruction.bind(this));
```

## 7. External API preservation

| Symbol | Accessed from | Treatment |
|---|---|---|
| `normaliseSubTag` | `tests/*.test.js`, `_matchSubElement` (line 1436) | Delegation shim on core class → `return this._subtagMatcher.normaliseSubTag(...)` |
| `_lastCardFrontIndex` | `tests/normalizeSubtags.test.js` (read & write), `scopeBlocks` (line 56 reset) | Getter/setter on core class forwarding to `this._subtagMatcher._lastCardFrontIndex` |
| `detectWriterInstruction` | `tests/writerInstructions.test.js`, `tests/osai201Defects.test.js`, `_matchOpeningTag` (line 1027) | Stays on core class unchanged; tag-matcher receives bound reference |
| `scopeBlocks`, `splitCompoundTags`, `extractLayoutDirection`, `detectLayoutPairs`, `inferInteractiveFromTable`, `normaliseVideoTag`, `extractVideoTiming`, `normaliseAlertTag` | public | Stay on core class; unchanged |
| `_matchOpeningTag`, `_matchClosingTag`, `_isHardBoundary` | core `scopeBlocks` only; no test access | Delegation shims on core class |
| `ORDINAL_MAP`, `_blockTypeKeywords`, `_closerTypeMap`, `_hardBoundaryTags`, `_blockOpenPrefixStrip` | internal only; no test access | Moved onto `this._tables`; no shims needed |

## 8. Internal-reference renames

Apply after each sub-module is extracted, using `sed -i` on the new file. Session 2b writes the actual commands; the table below lists only the pairs. **Ordering principle: longest match first, so no shorter rename corrupts a longer one.**

| In file | Old | New |
|---|---|---|
| `block-subtag-matcher.js` | `this.ORDINAL_MAP` | `this._tables.ordinalMap` |
| `block-subtag-matcher.js` | `this._lastCardFrontIndex` | *(unchanged — stays on sub-matcher instance)* |
| `block-tag-matcher.js` | `this._blockTypeKeywords` | `this._tables.blockTypeKeywords` |
| `block-tag-matcher.js` | `this._closerTypeMap` | `this._tables.closerTypeMap` |
| `block-tag-matcher.js` | `this._hardBoundaryTags` | `this._tables.hardBoundaryTags` |
| `block-tag-matcher.js` | `this._blockOpenPrefixStrip` | `this._tables.blockOpenPrefixStrip` |
| `block-tag-matcher.js` | `this.detectWriterInstruction(` | `this._detectWriterInstructionFn(` |

Dead-field note: `_hardBoundaryTags` and `_blockOpenPrefixStrip` are declared in `_buildBlockPatterns` but never referenced anywhere in the codebase — flag for Session 2c audit; **preserve as-is in tables module** (no behavior change in this session).

Inside `block-scoper-tables.js`, the two private builder helpers can be inlined into the constructor body with internal names like `this.ordinalMap`, `this.blockTypeKeywords`, `this.closerTypeMap`, `this.hardBoundaryTags`, `this.blockOpenPrefixStrip` (no `_` prefix on the tables instance since they are the module's public surface).

## 9. Core class delegation edits

After all three extractions, `js/block-scoper.js` must be modified as follows (method bodies replaced, signatures preserved):

- Constructor: replace `this._lastCardFrontIndex = null; this._buildOrdinalMap(); this._buildBlockPatterns();` with the three instantiations listed in §6.
- Add getter/setter for `_lastCardFrontIndex` that forward to `this._subtagMatcher._lastCardFrontIndex`.
- `normaliseSubTag(tagText, parentBlockType, lastIndex)` body → `return this._subtagMatcher.normaliseSubTag(tagText, parentBlockType, lastIndex);`
- `_matchOpeningTag(tags, block)` body → `return this._tagMatcher._matchOpeningTag(tags, block);`
- `_matchClosingTag(tags, blockStack)` body → `return this._tagMatcher._matchClosingTag(tags, blockStack);`
- `_isHardBoundary(tags)` body → `return this._tagMatcher._isHardBoundary(tags);`
- Delete `_buildOrdinalMap`, `_buildBlockPatterns`, `_getBlockTypeFromNormalised`, `_fuzzyMatchOpener`, `_extractWriterNotesFromTag`, `_getTextAfterBlockKeyword`, `_fuzzyMatchCloser`, `_matchAccordionTab`, `_matchFlipCardSubTag`, `_matchCarouselSlide`, `_matchTabSubTag` — all fully moved.
- Keep method names underscored within sub-modules to minimise churn in cross-method calls (e.g. `_fuzzyMatchOpener` → `_extractWriterNotesFromTag` within `block-tag-matcher.js`).

## 10. Wiring

Mirror Session 1 pattern (already established at `index.html:152–158` and `tests/test-runner.js:107–113`).

- **`index.html`** — add three `<script>` tags **before** the existing `<script src="js/block-scoper.js">` at line 158, in this order: tables → subtag-matcher → tag-matcher.
- **`tests/test-runner.js`** — add three `loadScript()` calls **before** the existing `loadScript('js/block-scoper.js')` at line 113, in the same order.

## 11. Test checkpoints for Session 2b

- After each of the three extractions, run `node tests/test-runner.js`. Must report `571/571 passed`.
- Commit and push after every successful checkpoint — **do not batch**.
- Commit message format: `Session 2b: extract <module-name> from block-scoper.js (<pass-count>/<total> passing)`
  - e.g. `Session 2b: extract block-subtag-matcher from block-scoper.js (571/571 passing)`

Recommended checkpoint order (matches §4):

1. After extracting `block-subtag-matcher.js` — `block-scoper.js` should be ~1490 lines.
2. After extracting `block-tag-matcher.js` — `block-scoper.js` should be ~1060 lines.
3. After extracting `block-scoper-tables.js` — `block-scoper.js` should be ~970 lines.

(Line estimates are approximate and assume delegation shims add back ~30 lines total.)

## 12. Rollback for Session 2b

**Single failed extraction (fixable mid-session):**

```
git checkout -- js/block-scoper.js index.html tests/test-runner.js
rm js/<in-flight-new-module>.js
```

**Unrecoverable (abandon session):**

```
git reset --hard origin/main
```

Do not force-push. Do not skip hooks. If tests fail after rename, first verify the rename table in §8 was applied longest-match-first; a shorter substring rename applied first is the most likely cause.
