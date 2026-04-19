# 26. Tag Normaliser Refactor & Audit (Session 1 of 4)

## Status

DONE — split executed, audit complete, 571/571 tests passing.

## Goal

Split `js/tag-normaliser.js` (1609 lines) into 5 cohesive sub-modules so:

1. `tag-normaliser.js` drops below the 700-line threshold and can be read
   in full by future sessions.
2. Each new sub-module is below 500 lines.
3. A subsequent read-only audit can surface tag-handling conflicts and
   redundancies that were hidden by the file's previous size.

No behaviour change is permitted. All 571 tests must stay green at every
checkpoint.

## Baseline

| File | Lines |
|---|---|
| `js/tag-normaliser.js` | 1609 |
| `js/block-scoper.js` | 1759 |
| `js/interactive-extractor.js` | 2245 |
| `js/html-converter.js` | 4050 |
| `js/app.js` | 1364 |

Baseline test run: `node tests/test-runner.js` → **571/571 passed, 0 failed**.

## Sub-module design

Five sub-modules, each with a clearly-bounded responsibility.

### 1. `js/ordinal-resolver.js`  (~40 lines)

Owns the ordinal/cardinal word → number map and the `resolveOrdinalOrNumber()`
routine. Extracted first because `subtag-matcher` depends on it.

- Extracted source: `resolveOrdinalOrNumber()` (lines 189-209) plus the body
  of `_buildOrdinalMap()` (lines 1316-1330).
- Public API: `resolveOrdinalOrNumber(word)` returning `number|null`.
- Dependencies: none.

### 2. `js/tag-normaliser-tables.js`  (~210 lines)

Owns the static lookup data: `_simpleTable`, `_categoryMap`,
`_interactiveTags`, `_interactiveNonStartTags`, `_interactiveChildTagsMap`,
`_interactiveEndSignalTags`.

- Extracted source: `_buildNormalisationTable()` body (lines 920-1117).
- Public API: a `TagNormaliserTables` class whose constructor populates
  these six properties. `TagNormaliser` reads them as
  `this._tables.simpleTable`, etc. (existing internal names are kept as
  pass-through references to minimise downstream churn.)
- Dependencies: none.

### 3. `js/tag-defragmenter.js`  (~170 lines)

Owns the Word-XML red-text fragmentation handling — both the Phase 1 Patch
pre-processor (`defragmentRawText`) and the earlier `reassembleFragmentedTags`
merging pass.

- Extracted source: `defragmentRawText()` (lines 211-252) and
  `reassembleFragmentedTags()` (lines 1138-1248).
- Public API: `defragmentRawText(text)`, `reassembleFragmentedTags(text)`.
  Both are forwarded unchanged from `TagNormaliser` for back-compat.
- Dependencies: none.

### 4. `js/subtag-matcher.js`  (~210 lines)

Owns `_matchSubTag()` — the last-resort regex dispatcher for verbose and
ordinal sub-tag forms (`First tab of accordion`, `Accordion one`, `Card N`,
`Slide N suffix`, etc.).

- Extracted source: `_matchSubTag()` (lines 1332-1528).
- Public API: `match(flexCleaned, inner, raw)` returning tag object or null.
- Dependencies: `OrdinalResolver` (injected).

### 5. `js/interactive-tag-matcher.js`  (~380 lines)

Owns the interactive-pattern block of `_normalise()` — the longest
contiguous regex dispatch in the file. Covers `drag_and_drop` through `mcq`
(lines 440-804 inclusive), leaving the structural/heading/lesson/activity
and image/table/button/lookup blocks in the core normaliser.

- Extracted source: `_normalise()` body, lines 440-804.
- Public API: `match(flexCleaned, inner, raw)` returning tag object or null.
- Dependencies: none.

### Core `js/tag-normaliser.js` after split  (~670 lines)

Retains:

- Constructor wiring (instantiates the five sub-modules).
- Regex patterns `_redTextPattern`, `_tagPattern`.
- Public: `processBlock`, `normaliseTag`, `getCategory`,
  `resolveOrdinalOrNumber` (delegates), `defragmentRawText` (delegates),
  `reassembleFragmentedTags` (delegates), `isInteractiveEndSignal`.
- Internal: `_extractRedTextRegions`, `_extractTagsFromText`, the slimmed
  `_normalise()` (retains heading/lesson/activity/image/table/button
  branches plus delegations to video/interactive/sub-tag matchers),
  `_lookupSimple`, `_annotateInteractive`, `_matchVideoTag`,
  `_handleInfoTriggerImageMerge`.

`_matchVideoTag` stays inline — it is tightly coupled to media classification
and too small to warrant its own module (65 lines, just below the
"not-worth-splitting" threshold). This keeps the sub-module count at 5.

## Dependency DAG

```
ordinal-resolver    (no deps)
tables              (no deps)
defragmenter        (no deps)
interactive-matcher (no deps)
subtag-matcher      ──► ordinal-resolver
tag-normaliser      ──► all five
```

Load order in `index.html` and `tests/test-runner.js`:

1. `ordinal-resolver.js`
2. `tag-normaliser-tables.js`
3. `tag-defragmenter.js`
4. `subtag-matcher.js`           (after ordinal-resolver)
5. `interactive-tag-matcher.js`
6. `tag-normaliser.js`           (after all five)

## Constructor / dependency-injection strategy

```js
// TagNormaliser constructor (post-split)
this._ordinalResolver   = new OrdinalResolver();
this._tables            = new TagNormaliserTables();
this._defragmenter      = new TagDefragmenter();
this._interactiveMatcher= new InteractiveTagMatcher();
this._subTagMatcher     = new SubTagMatcher(this._ordinalResolver);

// Expose tables' data as own-properties so existing internal code
// (_lookupSimple, getCategory, _annotateInteractive, isInteractiveEndSignal)
// continues to reference `this._simpleTable`, `this._categoryMap`, etc.
this._simpleTable               = this._tables.simpleTable;
this._categoryMap               = this._tables.categoryMap;
this._interactiveTags           = this._tables.interactiveTags;
this._interactiveNonStartTags   = this._tables.interactiveNonStartTags;
this._interactiveChildTagsMap   = this._tables.interactiveChildTagsMap;
this._interactiveEndSignalTags  = this._tables.interactiveEndSignalTags;
```

Delegations in `TagNormaliser`:

- `resolveOrdinalOrNumber(w)` → `this._ordinalResolver.resolveOrdinalOrNumber(w)`
- `defragmentRawText(t)`      → `this._defragmenter.defragmentRawText(t)`
- `reassembleFragmentedTags(t)`→ `this._defragmenter.reassembleFragmentedTags(t)`
- In `_normalise()`: the interactive block becomes
  ```js
  var interactiveResult = this._interactiveMatcher.match(flexCleaned, inner, raw);
  if (interactiveResult) return interactiveResult;
  ```
- `_matchSubTag(...)` → `this._subTagMatcher.match(flexCleaned, inner, raw)`
  (called from the existing last-resort site in `_normalise`).

## Execution commands

### Sub-module 1: ordinal-resolver

Extract body of `resolveOrdinalOrNumber` (195-209) and `_buildOrdinalMap`
(1322-1330). Write a hand-authored class, not a raw sed paste, because
both fragments are short and the names need to change (`_ordinalMap`
becomes `this._ordinalMap` inside the new class constructor).

### Sub-module 2: tag-normaliser-tables

Extract body of `_buildNormalisationTable` (929-1116) via:

```
sed -n '929,1116p' js/tag-normaliser.js
```

then wrap in a class whose constructor assigns the extracted literals to
`this.simpleTable`, `this.categoryMap`, etc. (Strip leading `this._` so
properties are cleanly-named on the new class.)

### Sub-module 3: tag-defragmenter

Extract `defragmentRawText` body (225-252) and `reassembleFragmentedTags`
body (1155-1248). Wrap in a `TagDefragmenter` class with the two public
methods.

### Sub-module 4: subtag-matcher

Extract `_matchSubTag` body (1346-1527) and rename its internal
`this.resolveOrdinalOrNumber(...)` calls to
`this._ordinalResolver.resolveOrdinalOrNumber(...)`. Wrap in a
`SubTagMatcher` class that takes `ordinalResolver` as a constructor arg.

### Sub-module 5: interactive-tag-matcher

Extract the interactive block of `_normalise` (lines 440-804). Wrap in
an `InteractiveTagMatcher` class with a single `match(flexCleaned, inner, raw)`
method whose body is the extracted `if/return` ladder. No `this.` rewrites
are needed — the block uses only its three arguments plus the local
`modifier` variable (which is declared per-branch).

### Deletion from tag-normaliser.js

After each extraction, remove the source range with `sed -i 'X,Yd'`, then
patch the surrounding code with `Edit` to insert the delegation call.

### index.html wiring

`str_replace` on the block around line 152 to insert the five new
`<script>` tags immediately before `tag-normaliser.js`, in the order
listed above.

### tests/test-runner.js wiring

`str_replace` on the block around line 107 to insert the five new
`loadScript()` calls immediately before `loadScript('js/tag-normaliser.js')`.

## Test checkpoints

- Baseline: 571/571 passing (captured above).
- After Phase A completes (no code changes): must still be 571/571.
- After each sub-module extraction: must be 571/571.
- After wiring index.html and test-runner.js: must be 571/571.

If any checkpoint falls below 571, halt and roll back per the rollback
path in the session brief.

## Audit Results

### Sub-module inventory (final line counts)

| File | Lines | Under target? |
|---|---:|---|
| `js/tag-normaliser.js`         | 720 | slight miss (target 700, +20) |
| `js/interactive-tag-matcher.js`| 403 | yes (< 500) |
| `js/subtag-matcher.js`         | 223 | yes |
| `js/tag-normaliser-tables.js`  | 212 | yes |
| `js/tag-defragmenter.js`       | 173 | yes |
| `js/ordinal-resolver.js`       |  47 | yes |

`tag-normaliser.js` exceeds the 700-line target by 20 lines. Cause: the
core file still owns nine regex/pattern branches inside `_normalise()`
(video, heading × 2, lesson × 2, activity × 3, image, table-wordselect,
table, button-suffix, unrecognised), plus `_handleInfoTriggerImageMerge`
and `isInteractiveEndSignal`. Shaving to 700 would mean splitting
`_matchVideoTag` (65 lines) or the heading/lesson/activity cluster
into a sixth sub-module, which would cross the "5 new sub-modules max"
rule from the session brief. Logged as **R-6** (remediation) below.

### Tag-coverage findings

**Code-only normalised names (not listed in `docs/10-tag-taxonomy.md`'s
variants tables):**

| Name | Producer | Notes |
|---|---|---|
| `word_highlighter`        | `tag-normaliser-tables.js:73`  | Taxonomy collapses `word highlighter` + `word select` → `word_select`; code keeps `word_highlighter` as a separate normalised name *and* emits `word_select`. **Documentation drift.** |
| `translate_section`       | `tag-normaliser-tables.js:80-81` | Not documented in docs/10. |
| `kanji_cards`             | `tag-normaliser-tables.js:82-83` | Not documented in docs/10 (added for ENGS301 — see docs/16 Issue context). |

**Sub-tag normalised names — category:'subtag' names that exist in code
but are not enumerated in the docs/10 variants tables:**
`accordion_tab`, `card_front`, `card_back`, `front`, `back`,
`static_heading`, `static_column`, `story_heading`, `unordered_list`,
`inside_tab`, `new_tab`, `table`.

These are implicitly covered by the "Structural Sub-tags" category but
not individually listed. Low severity — sub-tags are intentionally an
open set.

**Taxonomy names with no producing code path:** none found.

### Multi-path findings

Sites that can produce the same normalised name from more than one
dispatch path. Each site is classified as **Primary**, **Fallback**,
**Dead**, or **Conflicting**.

#### `info_trigger_image` — three producing sites
1. `interactive-tag-matcher.js:297-311` — exact-string match on
   `info trigger image`, `infotrigger image`, `info trigger] image`,
   `info trigger] [image`. **Primary** for the first two; **Dead via
   normal pipeline** for the last two (they contain `]`, so the
   `\[([^\]]+)\]` tag-extractor regex in `_extractTagsFromText` can
   never produce them — the first `]` terminates the match). They are
   only reachable by direct `normaliseTag()` calls with the raw string
   as input.
2. `interactive-tag-matcher.js:329-342` — `info_trigger` regex with
   `suffix === 'image'` redirects to `info_trigger_image`.
   **Fallback** — overlaps with site 1 for `info trigger image` and
   `infotrigger image` (both match `^info\s*trigger\s+image$`).
   Confirmed redundant: if site 1 were removed, site 2 would classify
   these identically.
3. `tag-normaliser.js:_handleInfoTriggerImageMerge` — post-process step
   in `processBlock()` that merges adjacent `[info trigger] [image]`
   tag pairs. **Primary** for the split-tag-pair case; not reachable
   via `normaliseTag()` (which operates on a single tag).

**Minor inconsistency:** the `normaliseTag()` → `_normalise()` path is
not wrapped in `_handleInfoTriggerImageMerge`, so a test that feeds a
single string `"[info trigger] [image]"` to `normaliseTag()` would get
two separate tag objects, whereas feeding the same string to
`processBlock()` merges them. Not currently exercised by any test.

#### `info_trigger` — two producing sites
1. `interactive-tag-matcher.js:282-295` — `hovertrigger` / `hover trigger`.
   **Primary** for those writer variants.
2. `interactive-tag-matcher.js:328-354` — `info trigger` + optional
   suffix (excluding `image`). **Primary** for `info trigger` variants.

Non-overlapping writer surfaces. No conflict.

#### `mcq` — two producing sites
1. `interactive-tag-matcher.js:370-383` — `multichoice dropdown quiz`,
   `multi choice dropdown quiz`, `dropdown quiz` → `mcq` with
   `modifier: 'dropdown'`. **Primary.**
2. `interactive-tag-matcher.js:385-399` — `mcq`, `multi choice quiz`,
   `multichoice quiz`, `multi choice` → `mcq` with `modifier: null`.
   **Primary.**

Non-overlapping literals. Dispatch order is not actually required for
correctness (the strings are disjoint), but the current order matches
the writer-facing intent (dropdown variant flagged before the generic
form).

#### `video` — two producing regions
1. `tag-normaliser.js:_matchVideoTag` (lines 587-638) — `embed video`,
   `imbed video`, `insert video`, `embed film`, `imbed film`,
   `interactive: video[: title]`, `audio animation video`. **Primary.**
2. `tag-normaliser-tables.js:49` — simple lookup `video` → `video`.
   **Fallback** for the bare `video` writer string (not matched by the
   regex patterns in site 1).

Complementary, not conflicting.

#### `word_select` — two producing sites
1. `tag-normaliser.js:435-446` — `table wordselect` / `table word select`
   → `word_select` with `modifier: 'table'`. **Primary** for the table
   variant.
2. `tag-normaliser-tables.js:73` — simple lookup `word select` →
   `word_select` (no modifier). **Primary** for the bare variant.

Non-overlapping; complementary.

#### `card_front` — four producing sites (subtag-matcher only)
`subtag-matcher.js:104-119` (`ordFlipMatch` → front side),
`subtag-matcher.js:135-143` (`frontTitleImgMatch`),
`subtag-matcher.js:145-152` (`cardNMatch` — plain `[Card N]`),
`subtag-matcher.js:155-162` (`flipcardNMatch` — `[Flipcard N]`).
All four handle distinct writer surfaces. Dispatch order is critical:
`ordFlipMatch` → `frontTitleImgMatch` → `cardNMatch` → `flipcardNMatch`.
No conflict; complementary.

#### `carousel_slide` — four producing sites
`interactive-tag-matcher.js:170-182` (plain `[Slide N]`),
`subtag-matcher.js:181-190` (`[Slide N - suffix]` / `[Slide N: suffix]`),
`subtag-matcher.js:192-200` (`[Slide N text-suffix]`),
`subtag-matcher.js:202-211` (`[Carousel Image N]`, `[Foo Slide N]`).
Dispatch order relies on the interactive matcher running before the
subtag matcher (the plain slide form must match its anchored regex
first, since the broader `slide\s+\d+\s+.+` could otherwise swallow it).
No conflict.

#### `back` — three producing sites
`tag-normaliser-tables.js:112` (`back` → back),
`tag-normaliser-tables.js:113` (`drop` → back — alias),
`subtag-matcher.js:214-219` (`drop image` → back with
`modifier: 'image'`). Non-overlapping; complementary.

#### `heading` — two producing sites
`tag-normaliser.js:320-331` (`h1`–`h5`),
`tag-normaliser.js:334-346` (incomplete `[H ]` — ENGS301 addition).
Non-overlapping.

#### `activity` — two producing sites
`tag-normaliser.js:375-387` (with ID),
`tag-normaliser.js:403-414` (without ID). Non-overlapping.

### Dispatch-ordering findings

Observed order inside `TagNormaliser._normalise()`:

```
1.  _matchVideoTag           (regex: embed/imbed/insert/interactive:/audio_animation)
2.  heading (h1-h5)          (inline regex)
3.  incomplete heading        (inline regex, ENGS301)
4.  lesson with number        (inline regex)
5.  lesson (bare)             (inline equality)
6.  activity with ID          (inline regex)
7.  activity heading / title  (inline regex)
8.  activity (bare)           (inline equality)
9.  _interactiveMatcher.match (365 lines of regex ladder)
10. image with number         (inline regex)
11. table wordselect          (inline equality)
12. table                     (inline regex)
13. button with suffix        (inline regex, ENGS301)
14. _lookupSimple             (simple-table)
15. _subTagMatcher.match      (last-resort verbose/ordinal patterns)
16. unrecognised              (return null normalised)
```

`defragmentRawText` (Phase 1 Patch, step 0 of `processBlock`) fires
**before** any of the above.

**Critical ordering dependencies:**

- Video patterns must match before the simple table so that
  `[embed video]` doesn't get caught by any future `video` variant in
  the table. Currently both paths produce `video`, so this ordering is
  defensive rather than load-bearing.
- `table wordselect` must match before the generic `table` regex
  (otherwise `[Table wordselect]` would become `table` with
  `modifier: 'wordselect'` instead of `word_select` with
  `modifier: 'table'`).
- Interactive-matcher's `info_trigger_image` (exact strings) must
  match before `info_trigger` (regex with suffix) — the regex would
  otherwise catch `info trigger image` and route it to the fallback
  path. Current order preserves this (line 297 before line 328).
- Inside `_interactiveMatcher.match`: `flipcard`/`flipcards` as exact
  strings are checked before the regex `^flip\s+cards?`. The exact
  strings catch the single-word form (no space) that the regex
  requires whitespace for. Order preserved.
- Subtag-matcher runs last, so any tag the main ladder would have
  caught is already caught. The subtag-matcher is purely additive.

### Dead-branch findings

| # | Site | Status |
|---|---|---|
| D-1 | `interactive-tag-matcher.js:300-301` — literal `info trigger] image` and `info trigger] [image` | **Dead via pipeline** — strings contain `]`, which the `[^\]]+` tag-extractor regex cannot produce. Reachable only via direct `normaliseTag()` call. |
| D-2 | `tag-normaliser-tables.js:195` — `slide_show: ['carousel_slide', 'tab', 'image']` entry in `interactiveChildTagsMap` | **Dead key.** No code path emits `normalised: 'slide_show'` (`slideshow` and `slide show` both normalise to `carousel`). The child-tags lookup by name `carousel` finds the `carousel` entry on line 193, never the `slide_show` entry. |
| D-3 | `interactive-tag-matcher.js:297-311` — exact-string `info trigger image` and `infotrigger image` branches | **Redundant, not dead.** Overlaps with `interactive-tag-matcher.js:329-342` fallback which would classify identically if these branches were removed. Kept for explicitness; low-priority cleanup. |

### Phase attribution

| Code site | Introduced in |
|---|---|
| `defragmentRawText()` + Step 0 of `processBlock` | Phase 1 Patch (docs/18) |
| Ordinal suffix stripping in `resolveOrdinalOrNumber` | Phase 1 Patch (docs/18) |
| Incomplete heading `[H ]` (tag-normaliser.js:335) | ENGS301 Issue #5 (docs/16) |
| Hovertrigger (interactive-tag-matcher.js:282) | ENGS301 Issue #3 (docs/16) |
| `hintslider` (one-word, `\s*` quantifier) | ENGS301 Issue #10 (docs/16) |
| `flipcard` / `flipcards` exact-string fallback | ENGS301 Issue #12 (docs/16) |
| Button suffix regex (`[button- external link]` etc.) | ENGS301 Issue #6 (docs/16) |
| `go_to_journal` simple-table entry | ENGS301 Issue #9 (docs/16) |
| `multichoice dropdown quiz` → `mcq` modifier='dropdown' | ENGS301 Issue #4 (docs/16) |
| `reassembleFragmentedTags` | Predates the documented phases; called by `interactive-extractor.js:1445` and `html-converter.js:491`; has 10 dedicated tests in `tests/fragmentReassembly.test.js`. Active. |

### Prioritised remediation list

Ranked by severity: **Conflict > Redundancy > Dead code > Documentation drift > Size-target miss**.

| ID | Severity | Finding | Suggested fix | Test coverage before remediation |
|---|---|---|---|---|
| **R-1** | Documentation drift | `word_highlighter` emitted as a distinct normalised name (tables:73); docs/10 says `word highlighter` + `word select` both collapse to `word_select`. | Decide whether `word_highlighter` is a first-class name or an alias. If alias, change table entry to `{ normalised: 'word_select', category: 'interactive' }`. **Add regression test first** locking the current behaviour (`word highlighter` → `word_highlighter`) before changing — there may be downstream consumers (html-converter, interactive-extractor) that key off the distinction. | No direct assertion found for `word_highlighter` name; docs/16 Issue #8 refers to both names. |
| **R-2** | Documentation drift | `translate_section`, `kanji_cards` emitted but absent from docs/10. | Add rows to the taxonomy variants tables in docs/10. No code change. | N/A (docs-only). |
| **R-3** | Dead code | `slide_show` key in `interactiveChildTagsMap` (tables:195) is unreachable because no code produces that normalised name. | Remove the key. Before removing, add a test asserting that `[carousel]`, `[slide show]`, `[slideshow]` all normalise to `carousel` (current behaviour) so a follow-up session has a regression net. | Taxonomy tests cover the three variants; no test asserts the negative (absence of `slide_show`). |
| **R-4** | Dead code (niche) | `interactive-tag-matcher.js:300-301` — `info trigger] image` and `info trigger] [image` exact strings unreachable via the normal pipeline. | Delete the two literal strings. Keep `info trigger image` and `infotrigger image` (still reachable). **Add regression test first** feeding those literals to `normaliseTag()` directly, to confirm no consumer relies on that niche entry point. | None found. |
| **R-5** | Redundancy | Exact-string `info trigger image` branch (matcher:297-311) overlaps with the regex fallback (matcher:329-342); removing the exact branch would still classify identically. | Low priority. Could collapse both into the regex branch. Only remove after a regression test fixes the behaviour for both writer strings. | Not individually asserted. |
| **R-6** | Size-target miss | `tag-normaliser.js` landed at 720 lines (target 700). | Option A — inline `_matchVideoTag` callers and extract the 65-line method into `js/video-tag-matcher.js` (6th sub-module). Option B — extract the heading/lesson/activity cluster (~95 lines) into a `structural-tag-matcher.js`. Defer to a future refactor session; does not affect correctness. | N/A (non-functional). |
| **R-7** | Documentation drift | `isInteractiveEndSignal`'s H4/H5 context-sensitive behaviour (tag-normaliser.js:695-718) is documented in the method docstring and cross-references "Session G", but the `docs/` tree has no Session G file. | Cross-reference the actual session file, or drop the bare "Session G" label. | Functionally correct and well-tested; documentation-only drift. |

### Notes for Sessions 2-4

- Session 2 (block-scoper audit) should read only `js/block-scoper.js`
  in full, not any of the six tag-normaliser files. Spot-check the
  tag-normaliser pieces via `grep -n` if the block-scoper consumes
  them.
- Sessions 2-4 should preserve the five-sub-module boundary created
  here. If `_normalise()` needs further extraction to satisfy any
  future 700-line target, log it as a follow-up **after** that
  session's primary audit is complete.
- The `normaliseTag()` vs `processBlock()` asymmetry noted under
  "Multi-path findings → `info_trigger_image`" is a latent issue worth
  flagging when any session touches `_handleInfoTriggerImageMerge`.

