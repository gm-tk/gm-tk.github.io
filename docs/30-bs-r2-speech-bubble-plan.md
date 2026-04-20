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

---

### BS-R2 Execute — Speech Bubble Leaf Conversion

Status: EXECUTED. Plan carried out end-to-end on branch
`claude/read-project-docs-6nniz`. Final test count: **571 → 607 passing**
(589 at the pre-execute baseline, +18 permanent tests from this session).

#### Single-line deletion

The only production-code change in this session was the removal of one
line from `js/block-tag-matcher.js` — the `'speech_bubble': 'speech_bubble'`
entry in the `typeMap` inside `_getBlockTypeFromNormalised`. The line
was at **`js/block-tag-matcher.js:102`** at the start of the session
(confirmed by `sed -n '95,115p'`); post-fix the typeMap entries below it
shifted up by one line so `'activity': 'activity'` now sits at line 102.

The deletion was applied via a scoped `str_replace` using one unique
line above (`'tabs': 'tabs',`) and one unique line below (`'activity':
'activity',`) as context anchors, per the plan's "Exact str_replace-
ready deletion" block. The syntax was verified with `node --check
js/block-tag-matcher.js` before the test suite was re-run.

File-size snapshots:

| File | Pre-execute | Post-execute |
|---|---:|---:|
| `js/block-tag-matcher.js` | 454 | 453 |
| `js/block-scoper.js` | 992 | 992 (unchanged) |
| `js/block-scoper-tables.js` | 103 | 103 (unchanged) |
| `js/interactive-data-extractor.js` | 872 | 872 (unchanged) |
| `js/interactive-cell-parser.js` | 397 | 397 (unchanged) |
| `js/interactive-extractor-tables.js` | 106 | 106 (unchanged) |
| `js/html-converter-block-renderer.js` | 1124 | 1124 (unchanged) |

No other `js/` file was edited.

#### Test files

Three new test files were authored, with the split rationale chosen to
mirror the BS-R3 remediation convention (`rotatingBannerCloserPreFix.test.js`
/ `rotatingBannerCloserPostFix.test.js` /
`rotatingBannerInteractiveIntegration.test.js`):

| File | Case count | Role |
|---|---:|---|
| `tests/speechBubbleLeafPreFix.test.js` | 6 | Group A adjacent-path regression guards (accordion / tabs / activity / flip cards / alert openers + [end accordion] closer). Group B — 2 PRE-DELETE cases documenting the shape of the speech_bubble opener result — was deleted in the same commit that applied the fix. |
| `tests/speechBubbleLeafPostFix.test.js` | 7 | POST-FIX contract: `_matchOpeningTag` on `[speech bubble]` returns null; `_getBlockTypeFromNormalised({normalised:'speech_bubble'})` returns null; `scopeBlocks` emits three unscoped entries for the orphan-closer fixture (no `speech_bubble` wrapper); tag-normaliser still emits `tagInfo.normalised === 'speech_bubble'`; IE `_detectTablePattern` still returns 8 for speech_bubble; static `typeToPrimaryPattern['speech_bubble']` still equals 8; orphan `[end speech bubble]` still returns null via `_fuzzyMatchCloser`. |
| `tests/speechBubbleLeafIntegration.test.js` | 5 | Full-pipeline integration: two [speech bubble] tags are both unscoped (leaf-only, no implicit-close); pattern-9 Conversation layout captures all Prompt/Response entries; pattern-8 with a data table returns `dataPattern === 8` and `referenceEntry.type === 'speech_bubble'`; `[speech bubble]` + H2 terminates at H2 via `isInteractiveEndSignal`; `referenceEntry` carries type / tier / dataPattern / non-empty placeholderHtml for the HC generic-delegate consumer. |

Pre-fix / post-fix / integration split rationale:

* **Pre-fix** — Group A (adjacent paths) stays permanently to catch future
  refactors that drift the typeMap for other block types. Group B was
  authored as short-lived "PRE-DELETE BEHAVIOUR" scaffolding that locks
  the baseline before the deletion lands, then is deleted in the fix
  commit. Keeping Group B as explicit pre-delete scaffolding makes the
  git history legible: commit 1 documents what's being removed; commit 2
  removes both the code and the scaffolding; commit 2's diff shows the
  intent transferring to the post-fix file as inverted assertions.
* **Post-fix** — The inverted-assertion equivalents of Group B
  (`_matchOpeningTag` returns null; `_getBlockTypeFromNormalised`
  returns null; `scopeBlocks` emits unscoped entries) plus four
  orthogonality guards (tag-normaliser classifier, IE pattern-8
  cell-parser, IE pattern-8 static table, orphan closer). These are
  permanent — they are the contract the fix creates.
* **Integration** — Full-pipeline exercises that verify no observable
  output change: two tags independent, pattern-9 capture, pattern-8
  with table, H2 boundary termination, and referenceEntry well-formedness
  (the positive confirmation for the HC generic-delegate path).

#### Group B deletion step

The two Group B cases in `tests/speechBubbleLeafPreFix.test.js`
(`_matchOpeningTag on a normalised speech_bubble tag returns blockType
"speech_bubble"` and `scopeBlocks on [speech bubble]...[end speech bubble]
emits a speech_bubble scope (implicit-close)`) were DELETED — not
commented out — in the same commit that applied the fix. Rationale: their
intent is now expressed by the inverted assertions in
`tests/speechBubbleLeafPostFix.test.js`, so preserving them would either
duplicate the assertions (if left unchanged) or silently document dead
pre-fix behaviour (if commented out). Deletion keeps the test suite a
source-of-truth document for the current contract. The same convention
was followed by BS-R3 (see `tests/rotatingBannerCloserPreFix.test.js`'s
top-of-file docstring).

#### Four-site IE cross-audit findings

Per the docs/30 "Cross-audit verification steps" table, the four IE
sites that read the speech_bubble type were audited empirically
(`grep -n` + `sed -n` ±10 lines):

| # | Site | Expression read | Scoper-dependent? |
|---|---|---|---|
| 1 | `interactive-data-extractor.js:217` | `if (interactiveType === 'speech_bubble')` — `interactiveType` is set at `interactive-extractor.js:54` from `tagInfo.normalised` (the tag-normaliser output) | **No.** The branch reads the tag-normaliser's classification, not any scoper-produced field. |
| 2 | `interactive-data-extractor.js:722` | `tagInfo.normalised === 'speech_bubble' && modifier.indexOf('conversation') !== -1` inside the `_consumeInteractiveBoundary` walker | **No.** `tagInfo` is threaded in from `InteractiveExtractor.processInteractive` line 48 via `_getInteractiveTag(block)` — it is the tag-normaliser's output, not a scoper-state field. |
| 3 | `interactive-cell-parser.js:212` | `if (interactiveType === 'speech_bubble')` inside `_detectTablePattern`; `interactiveType` is an argument passed in by the caller at `interactive-cell-parser.js:178` | **No.** The function signature `_detectTablePattern(tableData, interactiveType)` takes a string, not a scoper record. Callers pass the tag-normaliser's normalised name. |
| 4 | `interactive-extractor-tables.js:53` | Static map literal `'speech_bubble': 8` inside `typeToPrimaryPattern` | **No.** Compile-time lookup table; keys are normalised tag names, not scoper block types. |

All four verdicts are "No". Option B (leaf) holds: removing the opener
declaration in the scoper cannot affect any IE pathway because no IE
pathway reads scoper state for speech_bubble.

#### html-converter negative confirmation

`grep -n "speech_bubble\|speech bubble\|speechbubble" js/html-converter*.js`
returns exactly one hit:

```
js/html-converter-block-processor.js:88:            // If a table contains an interactive tag (e.g., speech_bubble) in its
```

The hit is in a code comment describing the "promote interactive tag to
primary position" rule at `html-converter-block-processor.js:85-95`;
the surrounding code actually dispatches on `category === 'interactive'`
(the tag-normaliser's classifier output), not on the string
`speech_bubble`. The generic interactive handler at
`html-converter-block-renderer.js:365-395` then consumes the
`referenceEntry` payload produced by `InteractiveExtractor.processInteractive`
— a consumer-only path that never string-matches a specific interactive
name. Confirmed: html-converter is insensitive to the scoper's typeMap
for speech_bubble.

#### Final pass count

| Step | Commit | Delta | Total |
|---|---|---:|---:|
| Pre-execute baseline | — | — | **589/589** |
| Step 1 | `BS-R2 pre-fix tests: lock speech_bubble leaf baseline` | +8 (6 Group A + 2 Group B) | **597/597** |
| Step 3 | `BS-R2 fix: remove speech_bubble from block-tag-matcher typeMap` | +7 post-fix − 2 Group B deleted = +5 net | **602/602** |
| Step 4 | `BS-R2: cross-audit verify IE sites + integration test` | +5 integration | **607/607** |

Net: **+18 permanent tests**. Matches the plan's Test Checkpoints
table row-for-row.

#### Cross-links — BS-R2 conflict now closed

BS-R2 is the second of the two conflicts flagged by the `docs/27`
Opener/Closer Pairing Audit (row 191). BS-R3 (`rotating_banner`) was
closed earlier on the same branch (Option A — symmetric closer paths
added); BS-R2 (`speech_bubble`) is now closed here (Option B — opener
path removed). The remaining audit findings on `docs/27` are
non-conflict observations — duplicated maps (BS-R7), shadowed/dead
fields (BS-R4, BS-R5, BS-R6), and removable internal-only shims —
none of which block correctness.

Remediation: **Tag Pipeline Remediation — BS-R2 (Speech Bubble Leaf Conversion)**.
