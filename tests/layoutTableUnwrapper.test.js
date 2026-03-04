/**
 * Tests for Layout Table Unwrapper
 *
 * Tests layout table detection, contextual override, unwrapping,
 * column role assignment, and sidebar block creation.
 */

'use strict';

var normaliser = new TagNormaliser();
var unwrapper = new LayoutTableUnwrapper(normaliser);

// ============================================================
// Helper functions to create mock data structures
// ============================================================

/**
 * Create a paragraph content block.
 */
function mkPara(text, opts) {
    opts = opts || {};
    var runs = [];
    if (opts.isRed) {
        runs.push({
            text: text,
            formatting: {
                bold: false, italic: false, underline: false,
                strikethrough: false, color: 'FF0000', highlight: null, isRed: true
            }
        });
    } else {
        runs.push({
            text: text,
            formatting: {
                bold: opts.bold || false,
                italic: opts.italic || false,
                underline: false, strikethrough: false,
                color: null, highlight: null, isRed: false
            }
        });
    }
    var para = {
        runs: runs,
        text: text,
        heading: opts.heading || null,
        listLevel: opts.listLevel !== undefined ? opts.listLevel : null,
        listNumId: opts.listNumId || null,
        listFormat: opts.listFormat || null,
        isListItem: opts.isListItem || false
    };
    return { type: 'paragraph', data: para };
}

/**
 * Create a red-text paragraph content block (for structural tags).
 */
function mkRedPara(text) {
    return mkPara(text, { isRed: true });
}

/**
 * Create a table content block from an array of rows.
 * Each row is an array of cells, each cell is an array of paragraph specs.
 * Paragraph specs: { text, isRed } or just a string for plain text.
 */
function mkTable(rows) {
    return {
        type: 'table',
        data: {
            rows: rows.map(function (row) {
                return {
                    cells: row.map(function (cellParas) {
                        if (!Array.isArray(cellParas)) {
                            cellParas = [cellParas];
                        }
                        return {
                            paragraphs: cellParas.map(function (p) {
                                if (typeof p === 'string') {
                                    return {
                                        runs: [{
                                            text: p,
                                            formatting: {
                                                bold: false, italic: false, underline: false,
                                                strikethrough: false, color: null, highlight: null, isRed: false
                                            }
                                        }],
                                        text: p
                                    };
                                }
                                // Object with text and isRed
                                var fmt = {
                                    bold: false, italic: false, underline: false,
                                    strikethrough: false,
                                    color: p.isRed ? 'FF0000' : null,
                                    highlight: null,
                                    isRed: p.isRed || false
                                };
                                return {
                                    runs: [{ text: p.text, formatting: fmt }],
                                    text: p.text
                                };
                            })
                        };
                    })
                };
            })
        }
    };
}


// ============================================================
// INSTRUCTION 1: Layout Table Detection
// ============================================================

describe('Layout Table Detection — Test 1.6.1: Activity 2A table', function () {
    it('should detect table with [Activity] tag as layout table', function () {
        // Cell 1 has [Activity 2A], [Activity heading], [body], [multichoice dropdown quiz]
        // Cell 2 has [image]
        var table = mkTable([
            [
                [
                    { text: '[Activity 2A]', isRed: true },
                    { text: '[Activity heading]', isRed: true },
                    'Main ideas',
                    { text: '[body]', isRed: true },
                    'Test your understanding of this text.',
                    { text: '[multichoice dropdown quiz]', isRed: true },
                    '1. Where did Kōwhai first appear?',
                    'a. From the waves of the ocean.',
                    'b. From the golden glow of a flower.',
                    'c. From the roots of the great giants.'
                ],
                [
                    { text: '[image]', isRed: true },
                    'https://www.istockphoto.com/photo/example'
                ]
            ]
        ]);

        assertTrue(unwrapper.isLayoutTable(table.data), 'Should detect as layout table');
    });
});

describe('Layout Table Detection — Test 1.6.2: Activity 2B table', function () {
    it('should detect multi-row table with [Activity] tag as layout table', function () {
        var table = mkTable([
            // Row 1: quote text only
            [['Quote text about similes'], ['']],
            // Row 2: Activity + content | Alert sidebar
            [
                [
                    { text: '[Activity 2B]', isRed: true },
                    { text: '[Activity Heading]', isRed: true },
                    'Simile tree poem',
                    { text: '[Body]', isRed: true },
                    'Let us use inspiration...',
                    { text: '[modal]', isRed: true },
                    { text: '[body]', isRed: true },
                    'Write your simile tree poem...',
                    { text: '[Button]', isRed: true },
                    'Go to journal'
                ],
                [
                    { text: '[Alert]', isRed: true },
                    'Simile — Compares two things using like or as.'
                ]
            ]
        ]);

        assertTrue(unwrapper.isLayoutTable(table.data), 'Should detect as layout table');
    });
});

describe('Layout Table Detection — Test 1.6.3: Activity 6B body table', function () {
    it('should detect table with [Body] + [button] + [upload to dropbox] as layout table', function () {
        var table = mkTable([
            [
                [
                    { text: '[Body]', isRed: true },
                    'Now that you have explored...',
                    '1. Introduction',
                    '2. Main ideas',
                    { text: '[button]', isRed: true },
                    'Go to journal',
                    { text: '[body]', isRed: true },
                    'Upload your review...',
                    { text: '[upload to dropbox]', isRed: true }
                ],
                [
                    { text: '[image]', isRed: true },
                    'https://www.istockphoto.com/photo/emoticons'
                ]
            ]
        ]);

        assertTrue(unwrapper.isLayoutTable(table.data), 'Should detect as layout table');
    });
});

describe('Layout Table Detection — Test 1.6.4: Pure data table (no tags)', function () {
    it('should NOT detect plain data table as layout table', function () {
        // Feature / Opinion / Evidence table — no red text tags
        var table = mkTable([
            [['Feature'], ['Opinion'], ['Evidence']],
            [['Character development'], ['I think...'], ['The author uses...']],
            [['Setting'], ['The setting is...'], ['On page 42...']]
        ]);

        assertFalse(unwrapper.isLayoutTable(table.data), 'Should NOT detect as layout table');
    });
});

describe('Layout Table Detection — Test 1.6.5: Flipcard data table (contextual override)', function () {
    it('should NOT unwrap table following [flipcard] tag', function () {
        var contentBlocks = [
            mkRedPara('[flipcard]'),
            mkTable([
                [
                    [
                        { text: '[h5]', isRed: true },
                        'Card front title',
                        { text: '[body]', isRed: true },
                        'Card front content'
                    ],
                    [
                        { text: '[image]', isRed: true },
                        'https://example.com/img.jpg'
                    ]
                ]
            ])
        ];

        assertTrue(
            unwrapper._shouldOverrideAsDataTable(contentBlocks, 1),
            'Should override as data table when preceded by [flipcard]'
        );
    });
});

describe('Layout Table Detection — Test 1.6.6: Hintslider data table (contextual override)', function () {
    it('should NOT unwrap table following [hintslider] tag', function () {
        var contentBlocks = [
            mkRedPara('[hintslider]'),
            mkPara('Some bridging text'),
            mkTable([
                [
                    [
                        { text: '[Image]', isRed: true },
                        'https://example.com/hint1.jpg'
                    ],
                    ['Sight: birds singing']
                ]
            ])
        ];

        assertTrue(
            unwrapper._shouldOverrideAsDataTable(contentBlocks, 2),
            'Should override as data table when preceded by [hintslider]'
        );
    });
});

describe('Layout Table Detection — Test 1.6.7: Body + Alert sidebar table', function () {
    it('should detect [body] + [Alert] two-cell table as layout table', function () {
        var table = mkTable([
            [
                [
                    { text: '[body]', isRed: true },
                    'Forests cover about 31% of the land area.',
                    '• Tropical forests',
                    '• Temperate forests'
                ],
                [
                    { text: '[Alert]', isRed: true },
                    'CE (Common era) is a system for numbering years.'
                ]
            ]
        ]);

        assertTrue(unwrapper.isLayoutTable(table.data), 'Should detect as layout table');
    });
});


// ============================================================
// INSTRUCTION 1: Edge cases
// ============================================================

describe('Layout Table Detection — Edge: Table with only [image] tags', function () {
    it('should NOT detect table with only image tags as layout table', function () {
        var table = mkTable([
            [
                [{ text: '[image]', isRed: true }, 'https://example.com/1.jpg'],
                [{ text: '[image]', isRed: true }, 'https://example.com/2.jpg']
            ]
        ]);

        assertFalse(unwrapper.isLayoutTable(table.data), 'Should NOT detect as layout table');
    });
});

describe('Layout Table Detection — Edge: Table with single [body] tag only', function () {
    it('should NOT detect table with just one [body] tag as layout table', function () {
        var table = mkTable([
            [
                [{ text: '[body]', isRed: true }, 'Some text'],
                ['Other text without tags']
            ]
        ]);

        // Only 1 structural tag — below threshold of 2
        assertFalse(unwrapper.isLayoutTable(table.data), 'Should NOT detect with only 1 structural tag');
    });
});

describe('Layout Table Detection — Edge: Table with [body] + [H3] in same cell', function () {
    it('should detect table with 2 structural tags in single cell', function () {
        var table = mkTable([
            [
                [
                    { text: '[H3]', isRed: true },
                    'Section heading',
                    { text: '[body]', isRed: true },
                    'Some body text'
                ],
                ['Plain sidebar text']
            ]
        ]);

        assertTrue(unwrapper.isLayoutTable(table.data), 'Should detect with 2 structural tags');
    });
});

describe('Layout Table Detection — Contextual override does not apply without preceding interactive', function () {
    it('should NOT override when no interactive tag precedes the table', function () {
        var contentBlocks = [
            mkPara('Some regular text'),
            mkTable([
                [
                    [{ text: '[body]', isRed: true }, { text: '[button]', isRed: true }],
                    [{ text: '[image]', isRed: true }]
                ]
            ])
        ];

        assertFalse(
            unwrapper._shouldOverrideAsDataTable(contentBlocks, 1),
            'Should NOT override when no interactive tag precedes'
        );
    });
});

describe('Layout Table Detection — Contextual override ignored when table has [Activity]', function () {
    it('should NOT override even when interactive precedes if table has [Activity]', function () {
        var contentBlocks = [
            mkRedPara('[flipcard]'),
            mkTable([
                [
                    [
                        { text: '[Activity 3A]', isRed: true },
                        { text: '[body]', isRed: true },
                        'Content'
                    ],
                    [{ text: '[image]', isRed: true }]
                ]
            ])
        ];

        assertFalse(
            unwrapper._shouldOverrideAsDataTable(contentBlocks, 1),
            'Should NOT override when table contains [Activity]'
        );
    });
});


// ============================================================
// INSTRUCTION 2: Layout Table Unwrapping
// ============================================================

describe('Layout Table Unwrapping — Activity 2A', function () {
    it('should unwrap table, extracting paragraphs into content stream', function () {
        var contentBlocks = [
            mkPara('Text before'),
            mkTable([
                [
                    [
                        { text: '[Activity 2A]', isRed: true },
                        { text: '[Activity heading]', isRed: true },
                        'Main ideas',
                        { text: '[body]', isRed: true },
                        'Test your understanding.'
                    ],
                    [
                        { text: '[image]', isRed: true },
                        'https://example.com/img.jpg'
                    ]
                ]
            ]),
            mkPara('Text after')
        ];

        unwrapper.unwrapLayoutTables(contentBlocks, 0);

        // Table should be removed
        var hasTable = false;
        for (var i = 0; i < contentBlocks.length; i++) {
            if (contentBlocks[i].type === 'table') {
                hasTable = true;
                break;
            }
        }
        assertFalse(hasTable, 'Table should be removed after unwrapping');

        // Should have: Text before, [Activity 2A], [Activity heading], Main ideas, [body], Test..., sidebar_image, Text after
        assert(contentBlocks.length >= 7, 'Should have at least 7 blocks after unwrapping, got ' + contentBlocks.length);

        // First block should be original text
        assertEqual(contentBlocks[0].data.text, 'Text before');

        // Check that activity tag was extracted
        var foundActivity = false;
        for (var j = 0; j < contentBlocks.length; j++) {
            if (contentBlocks[j].data && contentBlocks[j].data.text === '[Activity 2A]') {
                foundActivity = true;
                break;
            }
        }
        assertTrue(foundActivity, 'Should find [Activity 2A] tag in content stream');

        // Last real block should be "Text after"
        assertEqual(contentBlocks[contentBlocks.length - 1].data.text, 'Text after');

        // Should have a sidebar image block
        var foundSidebar = false;
        for (var k = 0; k < contentBlocks.length; k++) {
            if (contentBlocks[k]._cellRole === 'sidebar_image') {
                foundSidebar = true;
                break;
            }
        }
        assertTrue(foundSidebar, 'Should have a sidebar image block');
    });
});

describe('Layout Table Unwrapping — Multi-row table', function () {
    it('should unwrap all rows from multi-row layout table', function () {
        var contentBlocks = [
            mkTable([
                // Row 1: quote only
                [['Quote text'], ['']],
                // Row 2: activity + alert sidebar
                [
                    [
                        { text: '[Activity 2B]', isRed: true },
                        'Activity content'
                    ],
                    [
                        { text: '[Alert]', isRed: true },
                        'Alert content'
                    ]
                ]
            ])
        ];

        unwrapper.unwrapLayoutTables(contentBlocks, 0);

        // Table should be replaced
        var hasTable = false;
        for (var i = 0; i < contentBlocks.length; i++) {
            if (contentBlocks[i].type === 'table') hasTable = true;
        }
        assertFalse(hasTable, 'Table should be removed');

        // Should find the quote text
        var foundQuote = false;
        for (var j = 0; j < contentBlocks.length; j++) {
            if (contentBlocks[j].data && contentBlocks[j].data.text === 'Quote text') {
                foundQuote = true;
                break;
            }
        }
        assertTrue(foundQuote, 'Should find quote text from row 1');

        // Should find the activity tag
        var foundActivity = false;
        for (var k = 0; k < contentBlocks.length; k++) {
            if (contentBlocks[k].data && contentBlocks[k].data.text === '[Activity 2B]') {
                foundActivity = true;
                break;
            }
        }
        assertTrue(foundActivity, 'Should find [Activity 2B] tag');

        // Should find alert sidebar
        var foundAlert = false;
        for (var m = 0; m < contentBlocks.length; m++) {
            if (contentBlocks[m]._cellRole === 'sidebar_alert') {
                foundAlert = true;
                break;
            }
        }
        assertTrue(foundAlert, 'Should have sidebar alert block');
    });
});

describe('Layout Table Unwrapping — Activity outside, body inside table', function () {
    it('should unwrap table body content when activity tag is outside', function () {
        var contentBlocks = [
            mkRedPara('[Activity 6B]'),
            mkRedPara('[Activity Heading]'),
            mkPara('Sharing your opinion'),
            mkTable([
                [
                    [
                        { text: '[Body]', isRed: true },
                        'Now that you have explored...',
                        '1. Introduction',
                        { text: '[button]', isRed: true },
                        'Go to journal',
                        { text: '[upload to dropbox]', isRed: true }
                    ],
                    [
                        { text: '[image]', isRed: true },
                        'https://example.com/emoticons.jpg'
                    ]
                ]
            ]),
            mkPara('Text after')
        ];

        unwrapper.unwrapLayoutTables(contentBlocks, 0);

        // Activity tag should still be at position 0
        assertEqual(contentBlocks[0].data.text, '[Activity 6B]');

        // Table should be removed
        var hasTable = false;
        for (var i = 0; i < contentBlocks.length; i++) {
            if (contentBlocks[i].type === 'table') hasTable = true;
        }
        assertFalse(hasTable, 'Table should be removed');

        // Body content should be in the stream after the activity heading
        var foundBody = false;
        for (var j = 0; j < contentBlocks.length; j++) {
            if (contentBlocks[j].data && contentBlocks[j].data.text === '[Body]') {
                foundBody = true;
                break;
            }
        }
        assertTrue(foundBody, 'Should find [Body] tag from unwrapped table');

        // Should find button tag
        var foundButton = false;
        for (var k = 0; k < contentBlocks.length; k++) {
            if (contentBlocks[k].data && contentBlocks[k].data.text === '[button]') {
                foundButton = true;
                break;
            }
        }
        assertTrue(foundButton, 'Should find [button] tag');
    });
});

describe('Layout Table Unwrapping — Body + Alert table', function () {
    it('should unwrap body text and create alert sidebar', function () {
        var contentBlocks = [
            mkTable([
                [
                    [
                        { text: '[body]', isRed: true },
                        'Forests cover about 31%.',
                        '• Tropical forests',
                        '• Temperate forests'
                    ],
                    [
                        { text: '[Alert]', isRed: true },
                        'CE (Common era) is a system.'
                    ]
                ]
            ])
        ];

        unwrapper.unwrapLayoutTables(contentBlocks, 0);

        // Should find body tag
        var foundBody = false;
        for (var i = 0; i < contentBlocks.length; i++) {
            if (contentBlocks[i].data && contentBlocks[i].data.text === '[body]') {
                foundBody = true;
                break;
            }
        }
        assertTrue(foundBody, 'Should find [body] tag');

        // Should find alert sidebar
        var foundAlert = false;
        for (var j = 0; j < contentBlocks.length; j++) {
            if (contentBlocks[j]._cellRole === 'sidebar_alert') {
                foundAlert = true;
                break;
            }
        }
        assertTrue(foundAlert, 'Should find alert sidebar');

        // Alert should contain the text
        for (var k = 0; k < contentBlocks.length; k++) {
            if (contentBlocks[k]._cellRole === 'sidebar_alert') {
                assertNotNull(contentBlocks[k]._sidebarAlertContent, 'Alert should have content');
                assertTrue(
                    contentBlocks[k]._sidebarAlertContent.some(function (t) {
                        return t.indexOf('Common era') !== -1;
                    }),
                    'Alert content should contain "Common era"'
                );
                break;
            }
        }
    });
});

describe('Layout Table Unwrapping — Negative: Flipcard data table preserved', function () {
    it('should NOT unwrap table preceded by [flipcard] tag', function () {
        var contentBlocks = [
            mkRedPara('[flipcard]'),
            mkTable([
                [
                    [
                        { text: '[h5]', isRed: true },
                        'Card title',
                        { text: '[body]', isRed: true },
                        'Card content'
                    ],
                    [{ text: '[image]', isRed: true }, 'https://example.com/img.jpg']
                ]
            ])
        ];

        unwrapper.unwrapLayoutTables(contentBlocks, 0);

        // Table should still exist
        var tableCount = 0;
        for (var i = 0; i < contentBlocks.length; i++) {
            if (contentBlocks[i].type === 'table') tableCount++;
        }
        assertEqual(tableCount, 1, 'Data table should be preserved');
    });
});

describe('Layout Table Unwrapping — Negative: Pure data table preserved', function () {
    it('should NOT unwrap table with no structural tags', function () {
        var contentBlocks = [
            mkTable([
                [['Feature'], ['Opinion'], ['Evidence']],
                [['Character development'], ['I think...'], ['The author uses...']]
            ])
        ];

        unwrapper.unwrapLayoutTables(contentBlocks, 0);

        // Table should still exist
        var tableCount = 0;
        for (var i = 0; i < contentBlocks.length; i++) {
            if (contentBlocks[i].type === 'table') tableCount++;
        }
        assertEqual(tableCount, 1, 'Data table should be preserved');
    });
});


// ============================================================
// INSTRUCTION 2: Column Role Assignment
// ============================================================

describe('Column Role Assignment — Main content vs sidebar image', function () {
    it('should assign main_content to cell with activity tags, sidebar_image to image cell', function () {
        var row = {
            cells: [
                {
                    paragraphs: [
                        {
                            runs: [{ text: '[Activity 2A]', formatting: { isRed: true, color: 'FF0000' } }],
                            text: '[Activity 2A]'
                        },
                        {
                            runs: [{ text: '[body]', formatting: { isRed: true, color: 'FF0000' } }],
                            text: '[body]'
                        }
                    ]
                },
                {
                    paragraphs: [
                        {
                            runs: [{ text: '[image]', formatting: { isRed: true, color: 'FF0000' } }],
                            text: '[image]'
                        },
                        {
                            runs: [{ text: 'https://example.com/photo.jpg', formatting: { isRed: false } }],
                            text: 'https://example.com/photo.jpg'
                        }
                    ]
                }
            ]
        };

        var roles = unwrapper._assignColumnRoles(row);
        assertEqual(roles[0], 'main_content', 'Cell with activity tags should be main_content');
        assertEqual(roles[1], 'sidebar_image', 'Cell with only image tag should be sidebar_image');
    });
});

describe('Column Role Assignment — Main content vs sidebar alert', function () {
    it('should assign sidebar_alert to cell with only [Alert] tag', function () {
        var row = {
            cells: [
                {
                    paragraphs: [
                        {
                            runs: [{ text: '[body]', formatting: { isRed: true, color: 'FF0000' } }],
                            text: '[body]'
                        },
                        {
                            runs: [{ text: 'Body content', formatting: { isRed: false } }],
                            text: 'Body content'
                        }
                    ]
                },
                {
                    paragraphs: [
                        {
                            runs: [{ text: '[Alert]', formatting: { isRed: true, color: 'FF0000' } }],
                            text: '[Alert]'
                        },
                        {
                            runs: [{ text: 'Alert text', formatting: { isRed: false } }],
                            text: 'Alert text'
                        }
                    ]
                }
            ]
        };

        var roles = unwrapper._assignColumnRoles(row);
        assertEqual(roles[0], 'main_content', 'Cell with body tag should be main_content');
        assertEqual(roles[1], 'sidebar_alert', 'Cell with only alert tag should be sidebar_alert');
    });
});

describe('Column Role Assignment — Plain image URL detection', function () {
    it('should assign sidebar_image to cell with only a plain image URL', function () {
        var row = {
            cells: [
                {
                    paragraphs: [{
                        runs: [{ text: '[body]', formatting: { isRed: true, color: 'FF0000' } }],
                        text: '[body]'
                    }]
                },
                {
                    paragraphs: [{
                        runs: [{ text: 'https://www.istockphoto.com/photo/example-123', formatting: { isRed: false } }],
                        text: 'https://www.istockphoto.com/photo/example-123'
                    }]
                }
            ]
        };

        var roles = unwrapper._assignColumnRoles(row);
        assertEqual(roles[1], 'sidebar_image', 'Cell with iStockPhoto URL should be sidebar_image');
    });
});


// ============================================================
// INSTRUCTION 2: Content stream integrity after unwrapping
// ============================================================

describe('Unwrapping — Content stream order preservation', function () {
    it('should maintain correct document order after unwrapping', function () {
        var contentBlocks = [
            mkPara('Before table'),
            mkTable([
                [
                    [
                        { text: '[Activity 1A]', isRed: true },
                        'Activity text'
                    ],
                    [
                        { text: '[image]', isRed: true }
                    ]
                ]
            ]),
            mkPara('After table')
        ];

        unwrapper.unwrapLayoutTables(contentBlocks, 0);

        // Check order
        assertEqual(contentBlocks[0].data.text, 'Before table', 'First block preserved');
        assertEqual(contentBlocks[contentBlocks.length - 1].data.text, 'After table', 'Last block preserved');

        // Middle blocks should be the unwrapped content
        assertTrue(contentBlocks.length >= 4, 'Should have at least 4 blocks (before + 2 unwrapped + after)');
    });
});

describe('Unwrapping — Multiple tables in sequence', function () {
    it('should unwrap multiple layout tables in one pass', function () {
        var contentBlocks = [
            mkTable([
                [[{ text: '[Activity 1A]', isRed: true }, 'Content 1A'], [{ text: '[image]', isRed: true }]]
            ]),
            mkPara('Between tables'),
            mkTable([
                [[{ text: '[Activity 2A]', isRed: true }, 'Content 2A'], [{ text: '[image]', isRed: true }]]
            ])
        ];

        unwrapper.unwrapLayoutTables(contentBlocks, 0);

        // No tables should remain
        var tableCount = 0;
        for (var i = 0; i < contentBlocks.length; i++) {
            if (contentBlocks[i].type === 'table') tableCount++;
        }
        assertEqual(tableCount, 0, 'All layout tables should be unwrapped');
        assertEqual(unwrapper.unwrappedCount, 2, 'Should report 2 unwrapped tables');
    });
});

describe('Unwrapping — Empty paragraphs skipped', function () {
    it('should skip empty paragraphs during unwrapping', function () {
        var contentBlocks = [
            mkTable([
                [
                    [
                        { text: '[Activity 1A]', isRed: true },
                        '',  // empty paragraph
                        'Actual content'
                    ],
                    [{ text: '[image]', isRed: true }]
                ]
            ])
        ];

        unwrapper.unwrapLayoutTables(contentBlocks, 0);

        // Count non-empty paragraph blocks (excluding sidebar)
        var nonEmpty = 0;
        for (var i = 0; i < contentBlocks.length; i++) {
            if (contentBlocks[i].type === 'paragraph' && contentBlocks[i]._cellRole !== 'sidebar_image') {
                if (contentBlocks[i].data.text) {
                    nonEmpty++;
                }
            }
        }
        assertTrue(nonEmpty >= 2, 'Should have at least 2 non-empty paragraphs');
    });
});

describe('Unwrapping — Metadata annotations preserved', function () {
    it('should add _unwrappedFrom metadata to extracted blocks', function () {
        var contentBlocks = [
            mkTable([
                [
                    [
                        { text: '[Activity 1A]', isRed: true },
                        'Content'
                    ],
                    [{ text: '[image]', isRed: true }]
                ]
            ])
        ];

        unwrapper.unwrapLayoutTables(contentBlocks, 0);

        // All unwrapped blocks should have _unwrappedFrom annotation
        for (var i = 0; i < contentBlocks.length; i++) {
            assertEqual(
                contentBlocks[i]._unwrappedFrom, 'layout_table',
                'Block ' + i + ' should have _unwrappedFrom annotation'
            );
        }
    });
});


// ============================================================
// INSTRUCTION 2: Sidebar block creation
// ============================================================

describe('Sidebar Block — Image sidebar has URL', function () {
    it('should create sidebar_image block with image URL', function () {
        var contentBlocks = [
            mkTable([
                [
                    [
                        { text: '[Activity 1A]', isRed: true },
                        'Content'
                    ],
                    [
                        { text: '[image]', isRed: true },
                        'https://www.istockphoto.com/photo/test-123'
                    ]
                ]
            ])
        ];

        unwrapper.unwrapLayoutTables(contentBlocks, 0);

        var sidebar = null;
        for (var i = 0; i < contentBlocks.length; i++) {
            if (contentBlocks[i]._cellRole === 'sidebar_image') {
                sidebar = contentBlocks[i];
                break;
            }
        }

        assertNotNull(sidebar, 'Should have sidebar image block');
        assertTrue(
            sidebar._sidebarImageUrl.indexOf('istockphoto') !== -1,
            'Sidebar should have iStockPhoto URL'
        );
    });
});

describe('Sidebar Block — Alert sidebar has content text', function () {
    it('should create sidebar_alert block with alert text', function () {
        var contentBlocks = [
            mkTable([
                [
                    [
                        { text: '[Activity 2B]', isRed: true },
                        'Activity content'
                    ],
                    [
                        { text: '[Alert]', isRed: true },
                        'Simile — Compares two things using like or as.'
                    ]
                ]
            ])
        ];

        unwrapper.unwrapLayoutTables(contentBlocks, 0);

        var sidebar = null;
        for (var i = 0; i < contentBlocks.length; i++) {
            if (contentBlocks[i]._cellRole === 'sidebar_alert') {
                sidebar = contentBlocks[i];
                break;
            }
        }

        assertNotNull(sidebar, 'Should have sidebar alert block');
        assertTrue(
            sidebar._sidebarAlertContent.length > 0,
            'Sidebar alert should have content'
        );
        assertTrue(
            sidebar._sidebarAlertContent.some(function (t) {
                return t.indexOf('Simile') !== -1;
            }),
            'Sidebar alert should contain "Simile"'
        );
    });
});


// ============================================================
// INSTRUCTION 2: Tag extraction helper
// ============================================================

describe('Tag Extraction — Red text tags', function () {
    it('should extract tag names from red text markers', function () {
        var text = '\uD83D\uDD34[RED TEXT] [Activity 2A] [/RED TEXT]\uD83D\uDD34';
        var tags = unwrapper._extractTagsFromText(text);
        assertTrue(tags.length >= 1, 'Should find at least 1 tag');
        assertTrue(
            tags.some(function (t) { return t === 'Activity 2A'; }),
            'Should find "Activity 2A" tag'
        );
    });
});

describe('Tag Extraction — Multiple tags in red text', function () {
    it('should extract multiple tags from one red text block', function () {
        var text = '\uD83D\uDD34[RED TEXT] [body] [button] text [/RED TEXT]\uD83D\uDD34';
        var tags = unwrapper._extractTagsFromText(text);
        assertTrue(
            tags.some(function (t) { return t === 'body'; }),
            'Should find "body" tag'
        );
        assertTrue(
            tags.some(function (t) { return t === 'button'; }),
            'Should find "button" tag'
        );
    });
});

describe('Tag Extraction — No tags in plain text', function () {
    it('should return empty array for text without tags', function () {
        var text = 'Just plain text without any tags';
        var tags = unwrapper._extractTagsFromText(text);
        assertEqual(tags.length, 0, 'Should find no tags');
    });
});


// ============================================================
// INSTRUCTION 2: Start index respected
// ============================================================

describe('Unwrapping — Start index respected', function () {
    it('should not unwrap tables before startIndex', function () {
        var contentBlocks = [
            // Index 0: layout table in boilerplate — should NOT be unwrapped
            mkTable([
                [
                    [
                        { text: '[Activity 0A]', isRed: true },
                        'Boilerplate content'
                    ],
                    [{ text: '[image]', isRed: true }]
                ]
            ]),
            // Index 1: layout table in content — SHOULD be unwrapped
            mkTable([
                [
                    [
                        { text: '[Activity 1A]', isRed: true },
                        'Real content'
                    ],
                    [{ text: '[image]', isRed: true }]
                ]
            ])
        ];

        unwrapper.unwrapLayoutTables(contentBlocks, 1);

        // First table should still be a table (not unwrapped)
        assertEqual(contentBlocks[0].type, 'table', 'Table before startIndex should be preserved');

        // Second table should be unwrapped
        var foundActivity1A = false;
        for (var i = 1; i < contentBlocks.length; i++) {
            if (contentBlocks[i].data && contentBlocks[i].data.text === '[Activity 1A]') {
                foundActivity1A = true;
                break;
            }
        }
        assertTrue(foundActivity1A, 'Table after startIndex should be unwrapped');
    });
});


// ============================================================
// INSTRUCTION 2: Interactive tag variants
// ============================================================

describe('Layout Table Detection — Drag and drop variant', function () {
    it('should detect table with [drag and drop] tag as layout table', function () {
        var table = mkTable([
            [
                [{ text: '[drag and drop]', isRed: true }, 'Some content'],
                ['Sidebar']
            ]
        ]);

        assertTrue(unwrapper.isLayoutTable(table.data), 'Should detect [drag and drop] as layout table');
    });
});

describe('Layout Table Detection — Accordion variant', function () {
    it('should detect table with [accordion] tag as layout table', function () {
        var table = mkTable([
            [
                [{ text: '[accordion]', isRed: true }, 'Content'],
                ['Sidebar']
            ]
        ]);

        assertTrue(unwrapper.isLayoutTable(table.data), 'Should detect [accordion] as layout table');
    });
});

describe('Layout Table Detection — Speech bubble variant', function () {
    it('should detect table with [speech bubble] tag as layout table', function () {
        var table = mkTable([
            [
                [{ text: '[speech bubble]', isRed: true }, 'Content'],
                ['Sidebar']
            ]
        ]);

        assertTrue(unwrapper.isLayoutTable(table.data), 'Should detect [speech bubble] as layout table');
    });
});

describe('Layout Table Detection — End page in cell', function () {
    it('should detect table with [End page] tag as layout table', function () {
        var table = mkTable([
            [
                [
                    { text: '[body]', isRed: true },
                    'Content',
                    { text: '[End page]', isRed: true }
                ],
                [{ text: '[image]', isRed: true }]
            ]
        ]);

        assertTrue(unwrapper.isLayoutTable(table.data), 'Should detect [End page] as layout table');
    });
});


// ============================================================
// Unwrapper counter tracking
// ============================================================

describe('Unwrapper — Count tracking', function () {
    it('should track unwrapped and preserved table counts', function () {
        var contentBlocks = [
            // Layout table — will be unwrapped
            mkTable([
                [[{ text: '[Activity 1A]', isRed: true }], [{ text: '[image]', isRed: true }]]
            ]),
            // Data table — will be preserved
            mkTable([
                [['Feature'], ['Opinion'], ['Evidence']]
            ])
        ];

        unwrapper.unwrapLayoutTables(contentBlocks, 0);

        assertEqual(unwrapper.unwrappedCount, 1, 'Should unwrap 1 table');
        assertEqual(unwrapper.preservedCount, 1, 'Should preserve 1 table');
    });
});
