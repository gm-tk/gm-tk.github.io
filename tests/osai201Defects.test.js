/**
 * Tests for OSAI201 writer-template snippet defects.
 *
 * Covers three concrete defects reported against the Phase 6 layout-table
 * unwrapping pipeline:
 *
 *   Defect 1: A standalone [H2] red paragraph immediately preceding a layout
 *             table is dropped from the final content stream.
 *
 *   Defect 2: The [image] red tag in a sidebar cell (that contains [image]
 *             + hyperlink URL + optional trailing red space) is lost during
 *             sidebar_image unwrapping — only the bare URL survives.
 *
 *   Defect 3: A fully-red paragraph in a sidebar cell (a writer/CS
 *             instruction) is dropped entirely, leaving a truncated
 *             red-text wrapper fragment glued to the preceding content.
 *
 * The scenario is modelled directly on the OSAI201 document snippet:
 *
 *     [H2] Lesson 1: What is AI?                          ← red paragraph
 *     ┌─────────────────────────────────┬───────────────┐
 *     │ [speech bubble] Kia ora! I'm …  │ [image] URL … │
 *     │                                 │ CS: can a …   │  ← all-red para
 *     └─────────────────────────────────┴───────────────┘
 *     [body] AI stands for artificial …                    ← red + plain
 */

'use strict';

var _normaliserForOsai = new TagNormaliser();
var _unwrapperForOsai = new LayoutTableUnwrapper(_normaliserForOsai);

// ============================================================
// Helpers — build paragraphs with multiple runs (red / plain /
// hyperlink runs) mirroring what DocxParser actually produces.
// ============================================================

function _mkRun(text, opts) {
    opts = opts || {};
    return {
        text: text,
        formatting: {
            bold: opts.bold || false,
            italic: opts.italic || false,
            underline: false,
            strikethrough: false,
            color: opts.isRed ? 'FF0000' : (opts.color || null),
            highlight: null,
            isRed: opts.isRed || false
        },
        hyperlink: opts.hyperlink || null
    };
}

function _mkParaFromRuns(runs, opts) {
    opts = opts || {};
    var text = runs.map(function (r) { return r.text; }).join('');
    return {
        runs: runs,
        text: text,
        heading: opts.heading || null,
        listLevel: opts.listLevel !== undefined ? opts.listLevel : null,
        listNumId: opts.listNumId || null,
        listFormat: opts.listFormat || null,
        isListItem: opts.isListItem || false
    };
}

function _mkBlockParaFromRuns(runs, opts) {
    return { type: 'paragraph', data: _mkParaFromRuns(runs, opts) };
}

function _mkBlockTable(rowsSpec) {
    return {
        type: 'table',
        data: {
            rows: rowsSpec.map(function (row) {
                return {
                    cells: row.map(function (cellSpec) {
                        return {
                            paragraphs: cellSpec.map(function (paraRuns) {
                                return _mkParaFromRuns(paraRuns);
                            })
                        };
                    })
                };
            })
        }
    };
}

// ------------------------------------------------------------------
// Build the OSAI201 snippet as a content-block array that mirrors
// what DocxParser.parse() produces for the document.
// ------------------------------------------------------------------
function _buildOsaiSnippet() {
    // Block 1: the [H2] Lesson 1 red paragraph (stand-alone, before table)
    var h2Block = _mkBlockParaFromRuns([
        _mkRun('[H2] Lesson 1: What is AI?', { isRed: true })
    ]);

    // Block 2: two-column layout table
    //   Left cell paragraph: red [speech bubble] + plain Kia ora text
    //   Right cell para 1  : red [image] + hyperlink URL + trailing red space
    //   Right cell para 2  : fully-red CS writer instruction
    var leftParaRuns = [
        _mkRun('[speech bubble]', { isRed: true }),
        _mkRun(" Kia ora! I'm Ariā. Unicorns are magical and in ancient times their horns were thought to heal people. AI can seem magical too, but it is just a tool programmed to help. AI is NOT like a human brain. To use AI properly, we must understand it. Let's find out more about AI.")
    ];
    var imageUrl = 'https://www.istockphoto.com/photo/fun-unicorn-3d-illustration-gm978974888-266040224';
    var rightPara1Runs = [
        _mkRun('[image]', { isRed: true }),
        _mkRun(' ', { isRed: true }),
        _mkRun(imageUrl, { hyperlink: imageUrl }),
        _mkRun(' ', { isRed: true })
    ];
    var rightPara2Runs = [
        _mkRun('CS: can a cross be put through the brain image to show it is AI is not a brain.', { isRed: true })
    ];
    var tableBlock = _mkBlockTable([
        [
            [leftParaRuns],
            [rightPara1Runs, rightPara2Runs]
        ]
    ]);

    // Block 3: [body] paragraph — red tag run + plain prose run.
    //   Mirrors the SDT-wrapped tracked-change case: DocxParser's
    //   ins-unwrap / del-strip logic resolves the text by the time
    //   it arrives here, so we model only the resolved text.
    var bodyBlock = _mkBlockParaFromRuns([
        _mkRun('[body]', { isRed: true }),
        _mkRun(' AI stands for artificial intelligence. It is a type of computer technology that uses information and patterns to form responses. It helps do smart tasks, like answering questions, making images and videos or sorting pictures.')
    ]);

    return [h2Block, tableBlock, bodyBlock];
}

function _blockText(block) {
    if (!block) return '';
    if (block.type === 'paragraph' && block.data) {
        var runs = block.data.runs || [];
        var out = '';
        for (var i = 0; i < runs.length; i++) {
            var run = runs[i];
            if (!run.text) continue;
            var chunk = run.text;
            var fmt = run.formatting || {};
            if (fmt.isRed) {
                chunk = '\uD83D\uDD34[RED TEXT] ' + chunk + ' [/RED TEXT]\uD83D\uDD34';
            }
            out += chunk;
        }
        return out;
    }
    return '';
}


// ============================================================
// Defect 1 — The [H2] heading before the layout table must survive
// ============================================================
describe('OSAI201 Defect 1 — [H2] heading before layout table', function () {
    it('should preserve the [H2] Lesson 1 heading after layout-table unwrapping', function () {
        var blocks = _buildOsaiSnippet();
        _unwrapperForOsai.unwrapLayoutTables(blocks, 0);

        // The H2 heading should still be present as a paragraph block
        var found = false;
        for (var i = 0; i < blocks.length; i++) {
            var t = _blockText(blocks[i]);
            if (t && t.indexOf('[H2]') !== -1 && t.indexOf('Lesson 1: What is AI?') !== -1) {
                found = true;
                break;
            }
        }
        assertTrue(found, 'H2 heading paragraph should survive layout-table unwrapping');
    });

    it('should not accidentally consume the paragraph preceding the layout table', function () {
        // A preceding unrelated paragraph should NEVER be swallowed
        var h2Block = _mkBlockParaFromRuns([
            _mkRun('[H2] Lesson 1: What is AI?', { isRed: true })
        ]);
        var table = _mkBlockTable([
            [
                [[_mkRun('[body]', { isRed: true }), _mkRun(' cell one')]],
                [[_mkRun('[image]', { isRed: true }), _mkRun(' '), _mkRun('https://example.com/img.jpg', { hyperlink: 'https://example.com/img.jpg' })]]
            ]
        ]);
        var blocks = [h2Block, table];
        _unwrapperForOsai.unwrapLayoutTables(blocks, 0);

        // First block must still be the H2 (unmodified)
        assertEqual(blocks[0].type, 'paragraph', 'first block should still be a paragraph');
        var t = _blockText(blocks[0]);
        assertTrue(t.indexOf('[H2]') !== -1, 'first block should still contain the [H2] tag');
        assertTrue(t.indexOf('Lesson 1') !== -1, 'first block should still contain the heading text');
    });
});


// ============================================================
// Defect 2 — The [image] tag must survive through sidebar_image unwrap
// ============================================================
describe('OSAI201 Defect 2 — [image] red tag survives sidebar unwrapping', function () {
    it('should preserve the [image] red tag when the cell is [image] + hyperlink URL', function () {
        var blocks = _buildOsaiSnippet();
        _unwrapperForOsai.unwrapLayoutTables(blocks, 0);

        // Find any block whose text contains the istock URL
        var foundImageTagWithUrl = false;
        for (var i = 0; i < blocks.length; i++) {
            var b = blocks[i];
            if (b.type !== 'paragraph') continue;
            var t = _blockText(b);
            var hasUrl = t && t.indexOf('istockphoto.com') !== -1;
            var hasImageTag = t && /\[image\]/i.test(t);
            if (hasUrl && hasImageTag) {
                foundImageTagWithUrl = true;
                break;
            }
        }
        assertTrue(foundImageTagWithUrl,
            '[image] tag must survive alongside the hyperlink URL in sidebar_image block');
    });

    it('should annotate the sidebar_image block with the correct URL', function () {
        var blocks = _buildOsaiSnippet();
        _unwrapperForOsai.unwrapLayoutTables(blocks, 0);

        var found = null;
        for (var i = 0; i < blocks.length; i++) {
            if (blocks[i]._cellRole === 'sidebar_image') {
                found = blocks[i];
                break;
            }
        }
        assertNotNull(found, 'a sidebar_image block should be produced');
        assertEqual(found._sidebarImageUrl,
            'https://www.istockphoto.com/photo/fun-unicorn-3d-illustration-gm978974888-266040224',
            'sidebar_image block should carry the iStock URL');
    });
});


// ============================================================
// Defect 3 — Fully-red CS paragraph must be captured, not dropped
// ============================================================
describe('OSAI201 Defect 3 — fully-red CS paragraph is preserved', function () {
    it('should not drop the fully-red "CS: can a cross …" writer instruction', function () {
        var blocks = _buildOsaiSnippet();
        _unwrapperForOsai.unwrapLayoutTables(blocks, 0);

        // The CS text must appear SOMEWHERE in the unwrapped stream —
        // either as its own block, as annotated sidebar content, or
        // as a separate writer-instruction capture.
        var found = false;
        for (var i = 0; i < blocks.length; i++) {
            var b = blocks[i];
            if (b.type !== 'paragraph') continue;
            // Direct block text
            var t = _blockText(b);
            if (t && t.indexOf('can a cross be put through') !== -1) {
                found = true;
                break;
            }
            // Or preserved in sidebar annotation metadata
            if (b._sidebarParagraphs && b._sidebarParagraphs.length) {
                for (var p = 0; p < b._sidebarParagraphs.length; p++) {
                    var tp = b._sidebarParagraphs[p].text || '';
                    if (tp.indexOf('can a cross be put through') !== -1) {
                        found = true;
                        break;
                    }
                }
                if (found) break;
            }
            if (b._sidebarAlertContent && b._sidebarAlertContent.join(' ').indexOf('can a cross be put through') !== -1) {
                found = true;
                break;
            }
        }
        assertTrue(found, 'fully-red CS paragraph must NOT be dropped during sidebar unwrapping');
    });

    it('should not emit a truncated "🔴[RED" fragment glued to another block', function () {
        var blocks = _buildOsaiSnippet();
        _unwrapperForOsai.unwrapLayoutTables(blocks, 0);

        for (var i = 0; i < blocks.length; i++) {
            var t = _blockText(blocks[i]);
            if (!t) continue;
            // A bare '🔴[RED' fragment (opening a red wrapper that is never
            // closed) indicates a text-concatenation bug.
            var openCount = (t.match(/\uD83D\uDD34\[RED TEXT\]/g) || []).length;
            var closeCount = (t.match(/\[\/RED TEXT\]\uD83D\uDD34/g) || []).length;
            assertEqual(openCount, closeCount,
                'block ' + i + ' has mismatched red-text wrappers: ' + JSON.stringify(t));
            // And no dangling start token like '🔴[RED' without the full marker.
            assertFalse(/\uD83D\uDD34\[RED(?!\s*TEXT\])/.test(t),
                'block ' + i + ' contains a truncated red-text fragment: ' + JSON.stringify(t));
        }
    });

    it('should flag the fully-red CS paragraph as a writer instruction per Phase 6', function () {
        // A red-only paragraph whose content is a full CS/instruction
        // sentence should be classified as a writer instruction by
        // BlockScoper.detectWriterInstruction.
        var scoper = new BlockScoper(_normaliserForOsai);
        // detectWriterInstruction accepts the raw tag text (inner, no brackets)
        var inner = 'CS: can a cross be put through the brain image to show it is AI is not a brain.';
        var result = scoper.detectWriterInstruction(inner);
        assertTrue(result.isWriterNote,
            'CS-prefixed red instruction must be classified as a writer note');
    });
});


// ============================================================
// Pipeline — H2 + layout table + [body] through unwrapper and block-scoper
// ============================================================
describe('OSAI201 — full pipeline (unwrap + scope) preserves H2 and [body]', function () {
    it('should keep the H2 heading and [body] paragraph after scope analysis', function () {
        var blocks = _buildOsaiSnippet();
        _unwrapperForOsai.unwrapLayoutTables(blocks, 0);
        // Block-scoper shouldn't drop untagged or differently-tagged
        // paragraphs that sit before / after an interactive block.
        var scoper = new BlockScoper(_normaliserForOsai);
        // scopeBlocks returns a tree; but it shouldn't throw nor consume the
        // H2 or [body] paragraphs entirely. We just ensure the call succeeds
        // and that the source content array still contains those paragraphs.
        scoper.scopeBlocks(blocks);

        var h2Found = false;
        var bodyFound = false;
        for (var i = 0; i < blocks.length; i++) {
            var t = _blockText(blocks[i]);
            if (!t) continue;
            if (/\[H2\]/i.test(t) && t.indexOf('Lesson 1') !== -1) h2Found = true;
            if (/\[body\]/i.test(t) && t.indexOf('AI stands for') !== -1) bodyFound = true;
        }
        assertTrue(h2Found, '[H2] Lesson 1 heading should still be present after scope analysis');
        assertTrue(bodyFound, '[body] AI stands for … paragraph should still be present');
    });
});

// ============================================================
// Defect 4 — SDT-wrapped [body] paragraph still resolves correctly
// ============================================================
describe('OSAI201 — [body] paragraph after layout table', function () {
    it('should preserve the [body] tag and the prose that follows it', function () {
        var blocks = _buildOsaiSnippet();
        _unwrapperForOsai.unwrapLayoutTables(blocks, 0);

        var found = false;
        for (var i = 0; i < blocks.length; i++) {
            var t = _blockText(blocks[i]);
            if (t && /\[body\]/i.test(t) &&
                t.indexOf('AI stands for artificial intelligence') !== -1) {
                found = true;
                break;
            }
        }
        assertTrue(found, '[body] paragraph should survive unwrapping intact');
    });
});
