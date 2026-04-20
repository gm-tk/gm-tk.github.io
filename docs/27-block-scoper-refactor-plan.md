# 27 — Block Scoper Refactor Plan (Session 2a)

## 1. Status

DONE — split executed, audit complete, 571/571 tests passing.

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

## Audit Results

### Sub-module inventory (final line counts)

| File | Lines |
|---|---:|
| `js/block-scoper.js`         | 992 |
| `js/block-tag-matcher.js`    | 452 |
| `js/block-subtag-matcher.js` | 296 |
| `js/block-scoper-tables.js`  | 102 |

Core file dropped from 1759 → 992 (–767). All three new sub-modules sit well under the 500-line threshold. Core overshoots the 700-line target by ~290 lines but is no longer the largest file in the pipeline; further splits are out of scope for this session.

### Cross-reference with Session 1 findings

Block-scoper consumes `tag.normalised` values that Session 1's tag-normaliser produces. Only genuine overlaps are listed.

| Session 1 tag | Session 1 classification | Block-scoper handling site | Relative classification |
|---|---|---|---|
| `carousel` | Primary (interactive-matcher) + Fallback (tables) | `block-tag-matcher.js:96` typeMap; `block-scoper-tables.js:35-38,67-69` | Consumer only — both producers funnel through same `typeMap` entry. No new conflict. |
| `rotating_banner` | Not flagged by Session 1 | `block-tag-matcher.js:97` typeMap; `block-scoper-tables.js:38` (opener keyword) | **Opener-only coverage** — see BS-R3 below. |
| `flip_card` | Session 1 covered multi-path in subtag-matcher | `block-tag-matcher.js:98` typeMap | Consumer only. |
| `click_drop`, `drag_and_drop`, `speech_bubble`, `activity`, `alert`, `important` | Session 1 did not flag as conflicting | `block-tag-matcher.js:99-105` typeMap | `speech_bubble` has **no closer path** — see BS-R2. |
| `slide_show` (dead key, Session 1 D-2) | Dead code | Not referenced | No impact on block-scoper. |
| `word_highlighter`, `translate_section`, `kanji_cards`, `info_trigger*` | Session 1 drift/dead | Not referenced | No impact on block-scoper. |

### Block-type coverage

Handled-but-not-documented (in a sub-module but no phase doc mentions the blockType):

| BlockType | Opener site | Closer site | Notes |
|---|---|---|---|
| `speech_bubble` | `block-tag-matcher.js:102` (typeMap only) | *(none)* | No entry in `blockTypeKeywords`, `closerTypeMap`, `_fuzzyMatchCloser.compactedMap`, or `_getTextAfterBlockKeyword.keywordMap`. Opens but cannot close explicitly. |
| `modal` | `block-scoper-tables.js:57` + `closerTypeMap:87-88` | `closerTypeMap:87-88` | Fully paired; not mentioned in phase docs. Low risk. |

Documented-but-not-handled: none — every blockType referenced in `docs/` is matched by at least an opener path.

### Opener/closer pairing

Asymmetric cases:

| BlockType | Opener | Closer | Gap |
|---|---|---|---|
| `speech_bubble` | typeMap (normalised-name path only) | none | Cannot be explicitly closed; relies on implicit close (same-type reopen, hard boundary, end-of-document). |
| `rotating_banner` / `rotating banner` | `blockTypeKeywords:38` (writer keyword); `typeMap:97` (normalised name) | none (`rotating banner`/`rotatingbanner` absent from `closerTypeMap`, `compactedMap`, and the containment fallbacks in `_fuzzyMatchCloser:402-413`) | Writers cannot type `[end rotating banner]` and have it close the block. |

All other blockTypes (`accordion`, `carousel`, `flipcards`, `clickdrop`, `dragdrop`, `alert`, `tabs`, `modal`, `activity`) have both opener and closer paths.

### Sub-tag pattern overlap

| Pattern | First matcher (wins) | Second matcher (shadowed) |
|---|---|---|
| `tab N` / `tab N suffix` | `_matchAccordionTab.numAccMatch` (block-subtag-matcher.js:97) covers the full `^(?:accordion\s+tab\|accordion\|tab)\s+(\d+)\s*:?\s*(.*)$` surface with `(.*)` optional | `_matchTabSubTag` (block-subtag-matcher.js:288) `^tab\s+(\d+)\s*:?\s*(.*)$` — strictly a subset; never reached. |

`_matchTabSubTag` is completely shadowed by `_matchAccordionTab.numAccMatch`. Confirmed by dispatch order in `normaliseSubTag()` (accordion → flip → carousel → tab). Flagged BS-R1 below.

No other overlaps between `_matchAccordionTab`, `_matchFlipCardSubTag`, `_matchCarouselSlide` — each owns a disjoint keyword/format family.

### Lookahead hygiene

- `LOOKAHEAD_LIMIT = 200` declared once in `block-scoper.js:28` and read once in `scopeBlocks` (line 213). Single source.
- Minor drift: the warning string on `block-scoper.js:216` hardcodes the literal `'200-line'` instead of interpolating `this.LOOKAHEAD_LIMIT`. Cosmetic; if the constant is ever tuned the message will lie. Flagged BS-R6.
- No duplicated lookahead constants across sub-modules.

### Delegation shim inventory

| Shim on core `BlockScoper` | Accessed from | Removable when |
|---|---|---|
| `_lastCardFrontIndex` (get/set) | `scopeBlocks:90` (reset); `tests/normalizeSubtags.test.js` indirectly via `normaliseSubTag` | Tests stop relying on BlockScoper as a facade for sub-matcher state. Low priority — single state field. |
| `normaliseSubTag` | `_matchSubElement:900`; 60+ direct calls across `normalizeSubtags.test.js`, `ordinalNormalization.test.js`, `insideTab.test.js` | Test suite migrates to `new BlockSubtagMatcher(new BlockScoperTables())`. Medium effort. |
| `_extractWriterNotesFromTag` | `tests/writerInstructions.test.js:65` | Test instantiates `BlockTagMatcher` directly. One test file. |
| `_fuzzyMatchCloser` | `tests/alertNormalization.test.js:51` | Test instantiates `BlockTagMatcher` directly. One test file. |
| `_matchOpeningTag` | `scopeBlocks:120` only (no test access) | **Removable now** — inline `this._tagMatcher._matchOpeningTag(...)` at the single call site. |
| `_matchClosingTag` | `scopeBlocks:100` only (no test access) | **Removable now** — inline `this._tagMatcher._matchClosingTag(...)` at the single call site. |
| `_isHardBoundary` | `scopeBlocks:178` only (no test access) | **Removable now** — inline `this._tagMatcher._isHardBoundary(...)` at the single call site. |

Three internal-only shims (`_matchOpeningTag`, `_matchClosingTag`, `_isHardBoundary`) could be removed immediately; the other four carry test dependencies. See BS-R8.

### State-leak check

Clean. `_lastCardFrontIndex` is the only mutable cross-call state in the block-scoper pipeline and is owned exclusively by `BlockSubtagMatcher`. Reset sites:

- `scopeBlocks:90` — via the core setter shim (routes to sub-matcher).

Write sites (all inside `block-subtag-matcher.js`): lines 194, 204, 215, 223, 231, 239. No writes elsewhere. No divergence.

### Phase attribution

| Finding | Introduced in |
|---|---|
| Sub-module split (tables / tag-matcher / subtag-matcher) | Session 2b — Split Executed (docs/27) |
| `rotating banner` opener keyword (no closer) | phase unclear — predates the documented phase log |
| `speech_bubble` typeMap entry (no closer) | phase unclear — predates the documented phase log |
| `_matchTabSubTag` shadowed by `_matchAccordionTab.numAccMatch` | phase unclear — both matchers predate the split; the shadowing is a pre-existing condition preserved verbatim by Session 2b |
| `hardBoundaryTags` + `blockOpenPrefixStrip` declared as dead data | Session 2b — §8 already flags "Dead-field note"; preserved for behaviour-parity in that session |
| Hardcoded `'200-line'` in warning string | phase unclear — predates the split |
| `compactedMap` duplication inside `_fuzzyMatchCloser` | phase unclear — predates the split |

### Prioritised remediation list

Ranked by severity: **Conflict > Redundancy > Dead code > Documentation drift**. No remediation performed in this session.

| ID | Severity | Finding | Suggested fix | Test-coverage note |
|---|---|---|---|---|
| **BS-R1** | Redundancy | `_matchTabSubTag` (block-subtag-matcher.js:286-295) is completely shadowed by `_matchAccordionTab.numAccMatch` — all `tab N[...]` inputs are caught earlier in dispatch. | Delete `_matchTabSubTag` and its call site at line 50-51. Add a regression test feeding `[Tab 1]` / `[Tab 1 body]` via `normaliseSubTag()` first to lock current behaviour. | Covered indirectly by existing `tab N` assertions in `normalizeSubtags.test.js:138-168`; none asserts the dispatch path. |
| **BS-R2** | Conflict (coverage gap) | `speech_bubble` has opener path via `typeMap:102` but zero closer paths — no writer can explicitly close a speech-bubble block. | Decide whether `speech_bubble` is a block (needs closer entries in `closerTypeMap`, `compactedMap`, and `_getTextAfterBlockKeyword.keywordMap`) or a leaf node (remove from `typeMap` and handle inline). | No test exercises speech-bubble block open/close. Add a regression test first. |
| **BS-R3** | Conflict (coverage gap) | `rotating banner` has opener coverage (tables + typeMap) but no closer path; writers typing `[end rotating banner]` will fall through to `null`. | Add `'rotating banner': 'carousel'` to `closerTypeMap`, `'rotatingbanner': 'carousel'` to `compactedMap`, and a containment check in `_fuzzyMatchCloser`. | No test asserts the closer path for rotating banner. Add one. |
| **BS-R4** | Dead code | `hardBoundaryTags` array declared in `block-scoper-tables.js:98-100` but never referenced; `_isHardBoundary` uses literal string comparisons on `tag.normalised` instead. | Delete the array, or convert `_isHardBoundary` to consult it. Latter is cleaner — single source of boundary names. | Hard-boundary behaviour covered by `scopeBlocks`-level tests; refactor must preserve `page_break`/`end_lesson`/`end_module`/`lesson_overview` return values. |
| **BS-R5** | Dead code | `blockOpenPrefixStrip` array declared in `block-scoper-tables.js:28` but never referenced; `_fuzzyMatchOpener` hardcodes its own `prefixes` array at line 117-118. | Route `_fuzzyMatchOpener` through `this._tables.blockOpenPrefixStrip`, or delete the table entry. Prefer the former. | Covered by existing opener tests. |
| **BS-R6** | Documentation drift | `block-scoper.js:216` warning message hardcodes `'200-line'`; if `LOOKAHEAD_LIMIT` is tuned, the message will misreport. | Interpolate `this.LOOKAHEAD_LIMIT` into the warning string. | No test asserts the warning text. |
| **BS-R7** | Redundancy | `_fuzzyMatchCloser.compactedMap` (block-tag-matcher.js:371-395) duplicates `tables.closerTypeMap` with spaces removed. Two maps must be kept in sync manually. | Derive `compactedMap` at construction time from `closerTypeMap` via key compaction, or collapse both into a single normalisation step. | Closer behaviour well-covered by `alertNormalization.test.js` and scopeBlocks integration tests. |
| **BS-R8** | Shim trim | Three internal-only shims on `BlockScoper` (`_matchOpeningTag`, `_matchClosingTag`, `_isHardBoundary`) have no test consumers. | Inline the three `this._tagMatcher.*()` calls directly into `scopeBlocks`; delete the shims. Saves ~12 lines. | No test impact. |

No remediation performed in this session.
