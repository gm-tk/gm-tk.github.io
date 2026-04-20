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

---

### BS-R3 Remediation — Rotating Banner Explicit Closer Path

Remediates the opener/closer asymmetry flagged above for `rotating_banner`. The block type had two opener paths (`block-scoper-tables.js:38` writer-keyword and `block-tag-matcher.js:97` normalised-name typeMap) but zero closer paths — writers typing `[end rotating banner]` or `[end rotatingbanner]` would see the closer fall through to `null`, leaving the block to terminate only via implicit mechanisms (hard boundary, same-type reopen, end-of-document, or an interactive-extractor boundary signal).

#### Files touched

**`js/block-scoper-tables.js`** — one-line addition to `closerTypeMap` (the block-scoper's canonical closer-keyword table). A new entry `'rotating banner': 'carousel'` was inserted on the line immediately after `'slide show': 'carousel'` so the diff sits with the other carousel-group closer keywords. No surrounding lines moved; the file grew by one line.

**`js/block-tag-matcher.js`** — two additions inside `_fuzzyMatchCloser()`:

1. The `compactedMap` object literal (whose keys strip all whitespace/hyphens from the stripped closer text) gained a new `'rotatingbanner': 'carousel'` entry, placed directly below the existing `'slideshow': 'carousel'` entry. This closes the no-space form `[end rotatingbanner]`.
2. A new containment-check branch was inserted directly after the `slideshow` / `slide show` branch:

   ```js
   if (stripped.indexOf('rotating banner') !== -1 || stripped.indexOf('rotatingbanner') !== -1) return 'carousel';
   ```

   This mirrors the exact pattern used by sibling containment fallbacks (`accordion`, `carousel`, `slideshow`, `flip`, `clickdrop`, `click drop`, …) and ensures that even unusual close-tag prefixes like `[Close rotating banner]` or `[End of rotating-banner]` resolve to the carousel group.

No existing branches were modified. Both files remained in the post-refactor size range documented by Session 2.

#### Test files added

Three test files were authored across the remediation. All three live under `tests/` and are auto-discovered by `tests/test-runner.js`.

1. **`tests/rotatingBannerCloserPreFix.test.js`** — Group A regression guards (5 cases). Retained permanently.
   - `[end carousel]` still closes a carousel block explicitly.
   - `[end accordion]` still closes an accordion block explicitly.
   - `[end flipcards]` still closes a flipcards block explicitly.
   - `[rotating banner]` opener still opens a carousel-typed block.
   - Unrelated orphan closer `[end nonexistent-block]` returns `null` via `_fuzzyMatchCloser`.

   Originally the file also contained a Group B describe-block ("PRE-FIX BEHAVIOUR — will be inverted in post-fix file") with 3 cases asserting the pre-fix return values (`_fuzzyMatchCloser('end rotating banner')` → `null`; `_fuzzyMatchCloser('end rotatingbanner')` → `null`; `[rotating banner] … [end rotating banner]` with a trailing `[End page]` closed implicitly). Per the Group-B-deletion step of the task, that describe-block was **deleted** (not commented) in the same commit that applied the fix, because its intent became the post-fix file's contract.

2. **`tests/rotatingBannerCloserPostFix.test.js`** — post-fix contract (6 cases). Expected to fail pre-fix, pass post-fix.
   - `[end rotating banner]` closes a rotating_banner block explicitly.
   - `[end rotatingbanner]` (no space) also closes a rotating_banner block explicitly.
   - `[End Rotating Banner]` mixed case still closes (normalisation-consistent).
   - `_fuzzyMatchCloser` routes `"end rotating banner"` and `"end rotatingbanner"` to the carousel group.
   - Orphan `[end rotating banner]` outside any active block does not crash or mis-close (no carousel / rotating_banner wrapper materialises).
   - Explicit `[end rotating banner]` wins over the hard-boundary LOOKAHEAD fallback — content after the closer is emitted as a top-level `{ type: 'unscoped', … }` block by `BlockScoper.scopeBlocks()`.

   Running the file before the fix produced 5 failing tests (the orphan case passes regardless because an empty block stack short-circuits `_matchClosingTag` at its guard). Running the file after the fix produced 6/6 passing.

3. **`tests/rotatingBannerInteractiveIntegration.test.js`** — full-pipeline integration (7 cases). The fixture is a synthetic 8-block sequence: `[rotating banner], [Slide 1], body, [Slide 2], body, [end rotating banner], Post content, [End page]`.
   - BlockScoper side (4 cases): exactly one carousel-typed block emitted; `implicitClose === false` with `lineEnd === 5`; exactly two `carousel_slide` subtag children; `Post content` stays as a top-level unscoped block.
   - InteractiveExtractor side (3 cases): `processInteractive` returns exactly one rotating_banner placeholder with one `INTERACTIVE_START:` and one `INTERACTIVE_END:` delimiter; the IE walker routes to pattern 5 (numbered slides) and collects both slides; `processInteractive` returns a well-formed record with non-empty `placeholderHtml` and `blocksConsumed >= 1` (regression guard for the three audit-flagged IE sites).

#### Group B deletion — rationale

The pre-fix file was authored with two clearly-labelled groups so that the file could land green before the fix (locking the pre-fix baseline) and be trimmed cleanly after the fix. Once `BS-R3` was applied, the three Group B assertions became incorrect (they now described behaviour that the fix deliberately inverted). Commenting them out would leave dead assertions in the tree and invite future contributors to "fix" them by re-inverting. Deletion is the unambiguous signal that the pre-fix baseline has served its purpose and the post-fix contract is the sole forward-compatible reference. The Group A regression guards (which pass identically before and after the fix) remain in place as permanent regression coverage for the surrounding closer/opener paths.

#### IE cross-audit findings — site by site

Per the docs/28 cross-reference on BS-R3, three interactive-extractor sites were spot-checked with `grep -n` followed by ±5-line `sed` reads. For each site, the conclusion is **no regression, no code change required**.

- **`js/interactive-extractor-tables.js:51`** — the `patternMap` entry `'rotating_banner': 5`. This is a static pattern-number lookup. BS-R3 does not modify the table; rotating_banner placeholders still route through pattern 5 (numbered-items dispatch) in the placeholder renderer. Unchanged.
- **`js/interactive-data-extractor.js:479`** — `_isSubTagFor` predicate that maps `carousel_slide` → either `carousel` or `rotating_banner`. This predicate operates on the flat raw-block sequence inside the IE walker; it is independent of the block-scoper's children array. A `carousel_slide` is still a subtag of a `rotating_banner` interactive type regardless of whether the scoper now closes explicitly or implicitly. Unchanged.
- **`js/interactive-data-extractor.js:567`** — pattern-5 dispatch inside `_collectNumberedItems`: when `interactiveType === 'carousel' || 'rotating_banner'`, set `detectedPattern = 5`. The walker's termination logic relies on `_isEndBoundary(primaryTag)` (category-based: `structural`, `heading`, `body`, `styling`, `media`, `link`, plus `activity`/`end_activity` names). The BS-R3 change affects neither the category table nor the boundary name list — `[end rotating banner]` still normalises to a tag with `category: null, normalised: null`, which means the IE walker does NOT treat it as an IE-layer boundary. This was the pre-fix behaviour and remains the post-fix behaviour; the IE walker continues to terminate via the next true boundary downstream (here, `[End page]` which is a structural tag). Unchanged.

Empirical verification: a probe run against the full fixture confirms that `processInteractive` returns the same `blocksConsumed`, `interactiveType`, `dataPattern`, and numbered-items shape both before and after the fix. The IE walker's behaviour is stable.

#### HC-audit negative confirmation

Per the docs/29 cross-reference row for BS-R3: *"Opener but no closer | Not referenced by tagName in html-converter; reached via generic interactive handler. | Consumer only — same as speech_bubble. | No html-converter change if BS-R3 adds an explicit closer."* Confirmed — `rotating_banner` is never string-matched in any html-converter sub-module (`html-converter.js`, `html-converter-block-processor.js`, `html-converter-block-renderer.js`, `html-converter-content-helpers.js`, `html-converter-lesson-menu.js`, `html-converter-module-menu.js`, `html-converter-renderers.js`). The type reaches the renderer exclusively through the generic interactive handler path, which operates on the `referenceEntry` record produced by `InteractiveExtractor.processInteractive`. No html-converter integration test was required.

#### Pre-flight file sizes (for the record)

```
992 js/block-scoper.js
452 js/block-tag-matcher.js        (→ 453 post-fix)
102 js/block-scoper-tables.js      (→ 103 post-fix)
296 js/block-subtag-matcher.js
1364 js/app.js
641 js/html-converter.js
```

All files are in the post-refactor range documented by Sessions 1–4.

#### Test totals

- Baseline at the start of the remediation: **571/571** passing.
- After Step 1 (pre-fix tests committed, 8 new cases — 5 Group A + 3 Group B): **579/579**.
- After Step 3 (fix applied, 6 post-fix tests added, 3 Group B tests deleted): **579 + 6 − 3 = 582/582**.
- After Step 4 (integration test added, 7 new cases): **582 + 7 = 589/589**.
- Final: **571/571 → 589/589** (+18 permanent tests).

#### Scope boundary — BS-R3 vs BS-R7

The `compactedMap` / `closerTypeMap` duplication flagged by **BS-R7** was explicitly left untouched by this remediation. BS-R3 added one entry to each map (which is the minimal surgical change needed to close the opener/closer asymmetry) and is deliberately not rolling in the structural deduplication that BS-R7 prescribes. A future BS-R7 remediation will collapse the two maps into a single normalisation step — at that point the BS-R3 entries will migrate to the unified source without behaviour change. Until then, adding entries to both maps is the correct, audit-consistent pattern.
