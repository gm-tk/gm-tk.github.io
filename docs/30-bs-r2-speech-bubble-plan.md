# 30. BS-R2 Remediation Plan — Speech Bubble Opener/Closer Asymmetry

## Status

PLAN — ready for execute session.

## Baseline

| Item | Value |
|---|---|
| Test count (pre-plan) | 589/589 passing |
| Branch | `claude/read-project-docs-zQAZe` |
| Source audit | [docs/27 BS-R2](27-block-scoper-refactor-plan.md) row 253; [docs/27 Opener/closer pairing](27-block-scoper-refactor-plan.md) row 191 |
| `js/block-scoper.js` | 992 lines |
| `js/block-tag-matcher.js` | 454 lines |
| `js/block-scoper-tables.js` | 103 lines |
| `js/interactive-data-extractor.js` | 872 lines |
| `js/interactive-cell-parser.js` | 397 lines |
| `js/interactive-extractor-tables.js` | 106 lines |
| `js/html-converter-block-renderer.js` | 1124 lines |

## Investigation Summary

### Block-scoper opener/closer coverage for `speech_bubble`

| Path | File:Line | Present? | Content |
|---|---|---|---|
| `typeMap` (normalised-name opener) | `block-tag-matcher.js:102` | **Yes** | `'speech_bubble': 'speech_bubble'` |
| `blockTypeKeywords` (writer keyword opener) | `block-scoper-tables.js:31-60` | No | — |
| `closerTypeMap` | `block-scoper-tables.js:63-97` | No | — |
| `_fuzzyMatchCloser.compactedMap` | `block-tag-matcher.js:370-395` | No | — |
| `_getTextAfterBlockKeyword.keywordMap` | `block-tag-matcher.js:225-235` | No | — |
| Containment fallbacks in `_fuzzyMatchCloser` | `block-tag-matcher.js:402-413` | No | — |

Opener covers the single case `tag.normalised === 'speech_bubble'`. No path exists for `[end speech bubble]`; the block, once opened, can only implicit-close (hard boundary, same-type reopen, EOF).

### Interactive-extractor consumption sites (four IE-audit sites)

| # | File:Line | Pattern | Reads from | Scope-state assumption | Impact if block-closer added |
|---|---|---|---|---|---|
| 1 | `interactive-data-extractor.js:217` | Pattern 9 — conversation special-case | `interactiveType` (= `tagInfo.normalised`) | Treats start block as the interactive-start tag; walks forward collecting `conversationEntries`. No dependence on block-scoper scope state. | None — no scope-state read. `_consumeInteractiveBoundary` (line 701) terminates via `_isEndBoundary` + `isInteractiveEndSignal`, not a scoper closer. |
| 2 | `interactive-data-extractor.js:722` | `isConversationStyle` flag inside `_consumeInteractiveBoundary` | `tagInfo.normalised === 'speech_bubble'` + modifier | Walker-local flag; no scope-state read. | None — flag is derived from the tag-normaliser snapshot, not the scoper. |
| 3 | `interactive-cell-parser.js:212` | Pattern 8 — table-cell detection | `interactiveType` | Assumes `speech_bubble` interactives may appear as a table block; returns pattern 8. No scope-state read. | None. |
| 4 | `interactive-extractor-tables.js:53` | `typeToPrimaryPattern` lookup | Keyed on normalised tag name | Static table; independent of block-scoper. | None. |

All four IE sites key on `tagInfo.normalised` (the tag-normaliser output), not on `blockType` (the block-scoper output). They are insensitive to the typeMap entry at `block-tag-matcher.js:102`.

### html-converter delegation posture

| Layer | File:Line | Posture |
|---|---|---|
| Generic interactive handler | `html-converter-block-renderer.js:365-395` | Keys on `category === 'interactive'`; never string-matches `speech_bubble`; delegates to `InteractiveExtractor.processInteractive` and consumes `referenceEntry`. Consumer-only — unaffected by either BS-R2 option. |

### docs/12 guidance

docs/12 describes `speech_bubble` as a Tier 1 interactive (accordion, flip_card, speech_bubble, tabs) with optional "Conversation layout" modifier (Pattern 9). `tag-normaliser-tables.js:199` declares `speech_bubble: []` in `interactiveChildTagsMap` — explicitly no structural children. No writer-facing `[end speech bubble]` convention is documented.

### Test coverage reality check

Nine test files mention `speech bubble` / `speech_bubble`: `defragmentation.test.js`, `interactiveBoundaryAlgorithm.test.js`, `interactiveBoundaryIntegration.test.js`, `interactivePlaceholderFidelity.test.js`, `layoutTableUnwrapper.test.js`, `osai201Defects.test.js`, `tagClassifierInteractiveMeta.test.js`, `tagNormaliserExisting.test.js`. **Zero** assert the block-scoper opener/closer path (no `BlockScoper.scopeBlocks` call emits or asserts `blockType === 'speech_bubble'`). All existing tests exercise the tag-normaliser or IE layer.

### Downstream consumer of `blockType === 'speech_bubble'`

`grep -rn "blockType === 'speech_bubble'" js/ tests/` → zero hits. The scope object the opener would produce is silent dead code.

## Design Decision

| Option | Shape | Evidence for | Evidence against |
|---|---|---|---|
| **A — Block path** | Keep `typeMap:102`; add `speech bubble`→`speech_bubble` to `closerTypeMap`, `speechbubble`→`speech_bubble` to `compactedMap`, `speech_bubble`→regex to `keywordMap`; add containment fallback | Symmetric opener/closer; writers *could* type `[end speech bubble]` | Introduces new writer-facing surface with **zero demonstrated demand** in templates/tests/docs; `_consumeInteractiveBoundary:701-790` already owns termination via `isInteractiveEndSignal` — a mid-walk explicit closer would require audit of lines 783-790 to ensure no double-termination; new scope output still has no consumer |
| **B — Leaf path** | Delete `'speech_bubble': 'speech_bubble'` from `block-tag-matcher.js:102` | No downstream reads `blockType === 'speech_bubble'` (zero grep hits); all four IE sites key on `tagInfo.normalised` and are unaffected; html-converter is consumer-only; `tag-normaliser-tables.js:199` already declares `speech_bubble: []` children → not a true scoping block; docs/12 does not document an `[end speech bubble]` convention | Removes the only opener path — if a writer ever types `[speech bubble] … [end speech bubble]`, the closer still falls to `null` (pre-existing behaviour, preserved) |

**Chosen: Option B (leaf).**

Justification: speech_bubble is, by every downstream consumer's lens, a tag-normaliser-level interactive, not a block-scoper-level scoping block. `block-tag-matcher.js:102` is the sole site that claims otherwise; zero consumers read the resulting `blockType`, all four IE sites (`interactive-data-extractor.js:217`, `:722`; `interactive-cell-parser.js:212`; `interactive-extractor-tables.js:53`) key on `tagInfo.normalised`, `html-converter-block-renderer.js:365-395` is consumer-only, and `tag-normaliser-tables.js:199` explicitly declares the child list empty. Option A would introduce writer-facing surface (`[end speech bubble]`) with no demonstrated demand and require careful re-audit of `_consumeInteractiveBoundary` termination semantics. Option B removes silent dead code with no behavioural regression — termination semantics remain owned by `isInteractiveEndSignal`, identical to today.

BS-R3 (`rotating_banner`) chose Option A because `rotating banner` had pre-existing keyword-opener coverage at `block-scoper-tables.js:38` (writers *already* could open with the keyword); adding the closer was symmetric. `speech_bubble` has **no** keyword-opener path, so the asymmetry is one-sided — removal is symmetric, not addition.

## Execute-Session Scope

### Files the execute session will edit

| File | Change | Anchor |
|---|---|---|
| `js/block-tag-matcher.js` | Delete line `'speech_bubble': 'speech_bubble',` (line 102) from `typeMap` inside `_matchOpeningTag` | grep-anchor: `'speech_bubble': 'speech_bubble'` (unique literal) |

No other `js/` file edits.

### Exact str_replace-ready deletion

```
OLD:
            'tabs': 'tabs',
            'speech_bubble': 'speech_bubble',
            'activity': 'activity',

NEW:
            'tabs': 'tabs',
            'activity': 'activity',
```

### Pre-fix test file

**Filename:** `tests/blockScoperSpeechBubble.test.js` (new file)

**Group A — adjacent behaviour that MUST remain unchanged post-fix** (4 assertions):
1. `[accordion]` opener still returns `blockType: 'accordion'` via typeMap.
2. `[tabs]` opener still returns `blockType: 'tabs'` via typeMap.
3. `[activity]` opener still returns `blockType: 'activity'` via typeMap.
4. `[flip card]` opener still returns `blockType: 'flipcards'` via typeMap.
5. `[alert]` opener still returns `blockType: 'alert'` via typeMap.
6. `[end accordion]` closer still resolves to `'accordion'` via closerTypeMap.

**Group B — current pre-fix behaviour that will be intentionally inverted post-fix** (2 assertions):
1. Pre-fix: `_matchOpeningTag` on a normalised `speech_bubble` tag returns `blockType: 'speech_bubble'`. Post-fix: returns `null` (leaf — no scoping).
2. Pre-fix: `scopeBlocks` on `[speech bubble] … [end speech bubble]` emits a scope with `blockType: 'speech_bubble'` (implicit-close). Post-fix: emits `unscoped` entries for both blocks.

### Post-fix test file (same file, new `describe` block)

**5 assertions:**
1. `scopeBlocks([paragraph '[speech bubble]', paragraph 'content'])` emits no block scope for speech_bubble — both blocks are `unscoped`.
2. `tagInfo.normalised === 'speech_bubble'` is still produced by the tag-normaliser (classifier unaffected).
3. IE pattern-8 table path: a block of type `table` containing `[speech bubble]` in a cell still produces `detectedPattern === 8` via `interactive-cell-parser.js:212` (verifies IE unaffected).
4. IE pattern-9 conversation path: `[speech bubble Conversation layout]` start tag still routes into `_extractData`'s special-case branch at `interactive-data-extractor.js:216` (verifies IE unaffected).
5. `InteractiveExtractor.processInteractive` boundary: `[speech bubble]` start followed by H2 still terminates at H2 via `isInteractiveEndSignal` (verifies termination still owned by boundary walker).

### Cross-audit verification steps

| Site | Command | Prose check |
|---|---|---|
| IE #1 `data-extractor.js:217` | `grep -n "interactiveType === 'speech_bubble'" js/interactive-data-extractor.js` | Confirm hit count = 1; confirm the branch still runs because `interactiveType` is derived from `tagInfo.normalised`, not the (now-removed) scoper blockType. |
| IE #2 `data-extractor.js:722` | `grep -n "tagInfo.normalised === 'speech_bubble'" js/interactive-data-extractor.js` | Confirm hit count = 1; confirm `_consumeInteractiveBoundary` path uses normalised tag, not scoper. |
| IE #3 `cell-parser.js:212` | `grep -n "interactiveType === 'speech_bubble'" js/interactive-cell-parser.js` | Confirm hit count = 1; pattern-8 branch untouched. |
| IE #4 `tables.js:53` | `grep -n "'speech_bubble': 8" js/interactive-extractor-tables.js` | Confirm entry present; lookup table untouched. |
| HC consumer | `grep -n "speech_bubble\|speech bubble\|speechbubble" js/html-converter*.js` | Must return zero hits — negative confirmation that html-converter remains ignorant of speech_bubble by name. |

### Integration test file

**Filename:** `tests/speechBubbleLeafIntegration.test.js` (new file)

**5 assertions** (end-to-end through parser → normaliser → block-scoper → IE → html-converter):
1. OSAI201-style layout table with `[speech bubble]` in a cell → html-converter emits the layout-table row correctly and the `speech_bubble` tag is consumed by the IE table-pattern-8 path.
2. OSAI401-style `[speech bubble Conversation layout]` followed by numbered `Prompt:` / `AI response:` entries → IE pattern-9 path emits conversation entries inside the placeholder; html-converter wraps with the generic interactive handler.
3. `[speech bubble]` followed by H2 → IE boundary terminates at H2; html-converter renders the heading outside the interactive placeholder.
4. Two `[speech bubble]` tags in the same page (no explicit closer) → each is treated as an independent interactive; neither consumes the other.
5. Body-level `[speech bubble]` at top of page (no activity wrapper) → produces a single interactive placeholder + reference-doc entry; no block-scoper warning about implicit close.

### Total expected test-count delta

+ 6 Group A cases + 2 Group B pre-fix cases + 5 post-fix cases + 5 integration cases = **+18 tests**. Expected post-execute total: **607/607**.

## Rollback

| Scope | Command |
|---|---|
| Full-session rollback (from execute session) | `git reset --hard <plan-commit-sha>` (the commit this plan lands in) |
| Single-step rollback | `git reset --hard HEAD~1` |

## Test Checkpoints

| # | Commit | Scope |
|---|---|---|
| 1 | Group A + Group B pre-fix tests land; code unchanged | Baseline 589 → 597; Group B cases currently pass (pre-fix behaviour documented). |
| 2 | Post-fix tests land + `block-tag-matcher.js:102` deleted | Group B cases flip to assert the new leaf behaviour; all 5 post-fix cases pass. Total 597 → 602. |
| 3 | Cross-audit integration tests land | 602 → 607. All five integration cases pass. Run the five cross-audit greps from the Verification Steps table; confirm IE/HC sites unchanged. |
| 4 | Doc-log append to this file + Phase Log update in root CLAUDE.md | No functional change; 607/607. |
