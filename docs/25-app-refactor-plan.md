# 25. App Refactor Plan — Debug Panel Extraction

## 1. Status

DONE — extracted in Session 2.

## 2. Baseline measurements

Current `wc -l` of every file in `js/` (run on the pre-extraction HEAD):

| File | Lines |
|---|---:|
| **js/app.js** (extraction target) | **1936** |
| js/block-scoper.js | 1759 |
| js/docx-parser.js | 883 |
| js/formatter.js | 282 |
| js/html-converter.js | 4050 |
| js/interactive-extractor.js | 2245 |
| js/layout-table-unwrapper.js | 700 |
| js/output-manager.js | 225 |
| js/page-boundary.js | 560 |
| js/tag-normaliser.js | 1609 |
| js/template-engine.js | 858 |
| **Total** | **15107** |

After Session 2, `js/app.js` should drop by 584 lines (the extracted block) minus the ~15 lines Session 2 adds for the instantiation + replacement call site, i.e. to roughly `1936 − 584 + 15 ≈ 1367` lines. The new `js/debug-panel-renderer.js` should weigh roughly `584 + ~35` (constructor, render(), duplicated `_esc`, class wrapper) ≈ **~620 lines**.

## 3. Extraction range

**Lines 1133–1716 of `js/app.js`, confirmed contiguous** — this span contains only debug-panel-related section dividers and methods. No non-debug methods fall inside. Verified by:

- `grep -nE "^\s+[a-zA-Z_][a-zA-Z0-9_]*\("` between those bounds returns only the six debug methods listed in Section 4.
- Line 1717 is a blank line and line 1718 is the `// HTML conversion pipeline` section header; the first non-debug method (`_runHtmlConversion`) starts at line 1729.
- Line 1132 is the closing `}` of `_getBlockTextForAnalysis` (non-debug), and line 1133 is the first line of the `// Debug Panel rendering` section header comment.

Confidence: high — single contiguous block.

## 4. Methods being moved

Bullet list of every method in lines 1133–1716 by starting line (JSDoc opening) and signature line:

- `_renderDebugPanel(analysis)` — JSDoc starts line 1137, signature line 1143
- `_renderDebugConversionSummary()` — JSDoc starts line 1312, signature line 1318
- `_renderDebugBlockScopeSection(analysis)` — JSDoc starts line 1374, signature line 1380
- `_renderDebugInteractiveSection()` — JSDoc starts line 1457, signature line 1462
- `_renderDebugTemplateSection(analysis)` — JSDoc starts line 1542, signature line 1548
- `_getConfigDiffs(config)` — JSDoc starts line 1655, signature line 1662

Also moved (inside the range): the three section-divider comment blocks at lines 1133–1135, 1453–1455, and 1538–1540.

## 5. Dependencies table

Every `this.<member>` reference found by `sed -n '1133,1716p' js/app.js | grep -oE "this\.[a-zA-Z_]+" | sort -u`:

| Reference | Classification | Passed via |
|---|---|---|
| `this.debugPanel` | DOM node | constructor dep |
| `this.debugContent` | DOM node | constructor dep |
| `this.outputManager` | collaborator instance | constructor dep |
| `this.templateEngine` | collaborator instance | constructor dep |
| `this.currentAnalysis` | state data | `render()` snapshot field |
| `this.currentMetadata` | state data | `render()` snapshot field |
| `this.collectedInteractives` | state data | `render()` snapshot field |
| `this.interactiveReferenceDoc` | state data | `render()` snapshot field |
| `this.selectedTemplateId` | state data | `render()` snapshot field |
| `this._esc` | helper method | duplicated helper (see note) |
| `this._getConfigDiffs` | helper method | not passed (local — moved into new class) |
| `this._renderDebugBlockScopeSection` | helper method | not passed (local — moved) |
| `this._renderDebugConversionSummary` | helper method | not passed (local — moved) |
| `this._renderDebugInteractiveSection` | helper method | not passed (local — moved) |
| `this._renderDebugTemplateSection` | helper method | not passed (local — moved) |

**`_esc` duplication note.** Total `this._esc(` hits in `js/app.js` = 35. Hits inside the extraction range (lines 1133–1716) = 30. Remaining outside = 5. Because `_esc` is still called from outside the range, it **must be kept on `App`** AND **duplicated verbatim** into `DebugPanelRenderer`.

## 6. Constructor signature (literal JavaScript block for the new module header)

```javascript
/**
 * DebugPanelRenderer — renders PageForge's collapsible debug panel.
 *
 * Extracted from js/app.js in Session 2 of the app refactor.
 * Consumes a snapshot of App state plus four constructor-injected
 * dependencies. Emits HTML into the provided DOM nodes.
 */

'use strict';

class DebugPanelRenderer {
    /**
     * @param {Object} deps
     * @param {HTMLElement} deps.debugPanel - The `#debug-panel` root element.
     * @param {HTMLElement} deps.debugContent - The inner container that receives `innerHTML`.
     * @param {OutputManager} deps.outputManager - Needed for `getHtmlFileCount()` etc.
     * @param {TemplateEngine} deps.templateEngine - Needed for `getConfig()` / `generateSkeleton()`.
     */
    constructor(deps) {
        this._debugPanel = deps.debugPanel;
        this._debugContent = deps.debugContent;
        this._outputManager = deps.outputManager;
        this._templateEngine = deps.templateEngine;

        this._currentAnalysis = null;
        this._currentMetadata = null;
        this._collectedInteractives = null;
        this._interactiveReferenceDoc = '';
        this._selectedTemplateId = null;
    }
```

## 7. `render()` signature (literal JavaScript block)

```javascript
    /**
     * Render the debug panel from a snapshot of App state.
     *
     * @param {Object} snapshot
     * @param {Object} snapshot.analysis - `App.currentAnalysis`
     * @param {Object} snapshot.metadata - `App.currentMetadata`
     * @param {Array}  snapshot.collectedInteractives - `App.collectedInteractives`
     * @param {string} snapshot.interactiveReferenceDoc - `App.interactiveReferenceDoc`
     * @param {string} snapshot.selectedTemplateId - `App.selectedTemplateId`
     */
    render(snapshot) {
        this._currentAnalysis = snapshot.analysis;
        this._currentMetadata = snapshot.metadata;
        this._collectedInteractives = snapshot.collectedInteractives;
        this._interactiveReferenceDoc = snapshot.interactiveReferenceDoc;
        this._selectedTemplateId = snapshot.selectedTemplateId;
        this._renderDebugPanel(snapshot.analysis);
    }
```

## 8. Field-rename `sed` commands

Run in this exact order on `js/debug-panel-renderer.js` after the extracted block has been appended. Each rename uses extended regex with `\b` word boundaries to avoid accidental prefix matches. No earlier rename produces a substring that a later rename would corrupt — all source names are disjoint.

1. `sed -i -E 's/\bthis\.templateEngine\b/this._templateEngine/g' js/debug-panel-renderer.js`
2. `sed -i -E 's/\bthis\.outputManager\b/this._outputManager/g' js/debug-panel-renderer.js`
3. `sed -i -E 's/\bthis\.debugContent\b/this._debugContent/g' js/debug-panel-renderer.js`
4. `sed -i -E 's/\bthis\.debugPanel\b/this._debugPanel/g' js/debug-panel-renderer.js`
5. `sed -i -E 's/\bthis\.collectedInteractives\b/this._collectedInteractives/g' js/debug-panel-renderer.js`
6. `sed -i -E 's/\bthis\.currentAnalysis\b/this._currentAnalysis/g' js/debug-panel-renderer.js`
7. `sed -i -E 's/\bthis\.currentMetadata\b/this._currentMetadata/g' js/debug-panel-renderer.js`
8. `sed -i -E 's/\bthis\.interactiveReferenceDoc\b/this._interactiveReferenceDoc/g' js/debug-panel-renderer.js`
9. `sed -i -E 's/\bthis\.selectedTemplateId\b/this._selectedTemplateId/g' js/debug-panel-renderer.js`

**Do not** rename `this._esc`, `this._getConfigDiffs`, or any `this._renderDebugXxx` — those are methods that stay on the new class. Their `this.` prefix is already correct for the new class context.

## 9. `app.js` edits

### 9a. Add instantiation to the `App` constructor

- **old_str** (copied verbatim from js/app.js lines 59–62):

```
        this._bindElements();
        this._bindEvents();
        this._initTemplateEngine();
    }
```

- **new_str**:

```
        this._bindElements();
        this._bindEvents();
        this._initTemplateEngine();

        this._debugPanelRenderer = new DebugPanelRenderer({
            debugPanel: this.debugPanel,
            debugContent: this.debugContent,
            outputManager: this.outputManager,
            templateEngine: this.templateEngine
        });
    }
```

### 9b. Replace the single debug-invocation call site

Located inside `showResults()` at lines 510–513 (copied verbatim).

- **old_str**:

```
        // Render debug panel (now includes conversion summary)
        if (this.currentAnalysis) {
            this._renderDebugPanel(this.currentAnalysis);
        }
```

- **new_str**:

```
        // Render debug panel (now includes conversion summary)
        if (this.currentAnalysis) {
            this._debugPanelRenderer.render({
                analysis: this.currentAnalysis,
                metadata: this.currentMetadata,
                collectedInteractives: this.collectedInteractives,
                interactiveReferenceDoc: this.interactiveReferenceDoc,
                selectedTemplateId: this.selectedTemplateId
            });
        }
```

### 9c. Remove the extracted block from `app.js`

After the two str_replace edits above are in place (neither of which intersects the extraction range), run:

```bash
sed -i '1133,1716d' js/app.js
```

Verify immediately after: `wc -l js/app.js` should report roughly `1936 − 584 + (added lines from 9a + 9b) ≈ 1367` lines, and `grep -n "_renderDebugPanel\|_renderDebugConversionSummary\|_renderDebugBlockScopeSection\|_renderDebugInteractiveSection\|_renderDebugTemplateSection\|_getConfigDiffs" js/app.js` should return **no matches**.

## 10. `index.html` edit

Add the new `<script>` tag immediately before the existing `js/app.js` tag. Copied verbatim from lines 159–160.

- **old_str**:

```
    <script src="js/output-manager.js"></script>
    <script src="js/app.js"></script>
```

- **new_str**:

```
    <script src="js/output-manager.js"></script>
    <script src="js/debug-panel-renderer.js"></script>
    <script src="js/app.js"></script>
```

## 11. `test-runner.js` edit

**Not required.** `tests/test-runner.js` (lines 107–113) loads the non-DOM pipeline modules only (`tag-normaliser`, `block-scoper`, `layout-table-unwrapper`, `formatter`, `template-engine`, `interactive-extractor`, `html-converter`). It does not load `js/app.js`, and `DebugPanelRenderer` uses `document.createElement` (via the duplicated `_esc`), which is unavailable in the Node runner. No test-runner change is necessary for Session 2's mechanical extraction.

## 12. Execution order (mechanical steps for Session 2)

Run in this exact order. Do not skip verification steps.

1. **Create scaffolding file.** `cat > js/debug-panel-renderer.js <<'EOF'` with the literal JavaScript block from Section 6 (header + class opening + constructor), followed by a blank line and the `render()` block from Section 7. Terminate with `EOF`. **Do not** close the class yet.
2. **Append the extracted block.** `sed -n '1133,1716p' js/app.js >> js/debug-panel-renderer.js`.
3. **Append the duplicated `_esc` helper and close the class.**

   ```bash
   cat >> js/debug-panel-renderer.js <<'EOF'

       _esc(str) {
           var div = document.createElement('div');
           div.appendChild(document.createTextNode(str));
           return div.innerHTML;
       }
   }
   EOF
   ```

4. **Syntax-check the new file.** `node -c js/debug-panel-renderer.js` must exit 0. If not, stop and roll back (Section 13).
5. **Run every `sed` field-rename command from Section 8 in order.** After each run, `node -c js/debug-panel-renderer.js` must still pass.
6. **Apply Section 9a** — `str_replace` on `js/app.js` inserting the `DebugPanelRenderer` instantiation into the constructor.
7. **Apply Section 9b** — `str_replace` on `js/app.js` replacing the debug-invocation call site inside `showResults()`.
8. **Remove the extracted block from `app.js`** — `sed -i '1133,1716d' js/app.js`.
9. **Syntax-check `app.js`.** `node -c js/app.js` must exit 0 (`node -c` parses without executing). `grep -n "_renderDebugPanel\b" js/app.js` must return no matches.
10. **Apply Section 10** — `str_replace` on `index.html` adding the new `<script>` tag.
11. **Run the test suite.** `node tests/test-runner.js` — all 476 tests must still pass. The extraction does not touch any tested module, so this must be a green run.
12. **Smoke-test in a browser.** Serve `index.html`, upload a sample `.docx`, click Convert, verify the debug panel renders all six sections (Conversion Summary, Tag Normalisation, Page Boundaries, Block Scoping, Interactive Components, Template Configuration) identically to the pre-refactor build.
13. **Line-count sanity check.** `wc -l js/app.js js/debug-panel-renderer.js` — expect app.js around 1367 and debug-panel-renderer.js around 620.
14. **Append the Phase Log entry** to `CLAUDE.md` (one line, linking to this file, renamed to reflect the completed phase). **Only after steps 1–13 are fully green.**

## 13. Rollback commands

If any step above fails and the failure cannot be diagnosed and fixed in place, restore the working tree with:

```bash
git checkout -- js/app.js index.html tests/test-runner.js
rm -f js/debug-panel-renderer.js
```

If `DebugPanelRenderer` instantiation has already been committed before the failure, use `git reset --hard <pre-extraction-sha>` instead — but confirm no unrelated work is staged first. Never force-push. After rollback, re-open this runbook and diagnose before retrying.

## Execution Log

- **Final line counts:** `js/app.js` = **1364 lines**, `js/debug-panel-renderer.js` = **641 lines**. Both within the runbook's expected envelope (~1367 and ~620 respectively).
- **Post-extraction test run:** `node tests/test-runner.js` → **571/571 passed, 0 failed**. Baseline (pre-extraction) was also 571/571, so the extraction is behaviour-neutral against the test suite.
- **Deviations from the runbook:**
    1. **Off-by-one in extraction range.** The runbook claimed line 1716 was the last line of the debug block and line 1717 was blank. In fact line 1716 is `        return diffs;` and line 1717 is the closing `    }` of `_getConfigDiffs`. The `sed -n '1133,1716p'` extraction therefore omitted the method's closing brace, producing a syntax error at Section 12 step 4. Fixed in-flight by inserting the missing `    }` between `return diffs;` and the appended `_esc` helper in `js/debug-panel-renderer.js` (single targeted Edit).
    2. **Shifted deletion range.** Sections 9a and 9b added +7 and +6 lines respectively above the extraction block, shifting it to lines 1146–1729. Combined with the off-by-one fix above (extending end by 1), the actual deletion command run was `sed -i '1146,1730d' js/app.js` instead of the runbook's `sed -i '1133,1716d' js/app.js`. Verified by `sed -n` spot-checks of the new boundaries before and after deletion. The post-deletion `grep` for the six debug method names returned no matches, confirming a clean cut.
- All other steps (scaffolding, append, `_esc` duplication, the nine field-rename `sed` commands, both `str_replace` edits in `js/app.js`, the `index.html` `<script>` insertion) were executed exactly as specified.
