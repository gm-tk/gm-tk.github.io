# 4. How the Parser Works


### DocxParser (js/docx-parser.js)

The parser is a hand-rolled XML walker that extracts content from `.docx` files. Standard libraries (mammoth.js, python-docx, etc.) silently drop content inside tracked changes and SDT wrappers, so this custom parser was built specifically to handle Writer Template documents.

### Extraction Process

1. **Unzip** — Uses JSZip to extract `word/document.xml` from the `.docx` ZIP archive
2. **Parse relationships** — Reads `word/_rels/document.xml.rels` for hyperlink URLs and image references
3. **Parse numbering** — Reads `word/numbering.xml` for list type definitions (bullet vs ordered)
4. **Parse main document** — Uses DOMParser to parse `word/document.xml` into a DOM tree
5. **Walk body** — Recursively walks `<w:body>` extracting content in document order

### Critical XML Handling Rules

These rules are the foundation of correct extraction and must never be changed:

| XML Element | Action | Reason |
|-------------|--------|--------|
| `<w:del>` | **REMOVE ENTIRELY** — strip tag AND all content including `<w:delText>` | Deleted content must never appear in output |
| `<w:ins>` | **STRIP TAG, KEEP CONTENT** — remove wrapper, retain all `<w:t>` text within | Inserted text is the writer's final intent |
| `<w:sdt>` | **UNWRAP AND TRAVERSE** — descend into `<w:sdtContent>`, process children normally | Google Docs wraps paragraphs in SDT elements |

### Data Structures

The parser produces these key data structures:

#### Content Blocks (this.content array)
```javascript
// Ordered array of content blocks in document order
[
  { type: 'paragraph', data: paragraphObject, index: 0 },
  { type: 'table', data: tableObject },
  { type: 'pageBreak', data: null },
  { type: 'paragraph', data: paragraphObject, index: 1 },
  // ...
]
```

#### Paragraph Object
```javascript
{
  runs: [
    {
      text: "Hello world",
      formatting: {
        bold: false,
        italic: true,
        underline: false,
        strikethrough: false,
        color: "FF0000",      // hex colour (null if auto)
        highlight: null,
        isRed: true            // true if colour matches known red values
      },
      hyperlink: "https://..." // URL if this run is inside a hyperlink (null otherwise)
    }
  ],
  text: "Hello world",        // concatenated text from all runs
  heading: 2,                  // heading level (1-6) or null
  listLevel: 0,                // nesting level (0-based) or null
  listNumId: "1",              // numbering definition ID or null
  listFormat: "bullet",        // "bullet", "decimal", "lowerLetter", etc.
  isListItem: true             // true if this is a list item
}
```

#### Table Object
```javascript
{
  rows: [
    {
      cells: [
        {
          paragraphs: [ /* array of paragraph objects */ ]
        }
      ]
    }
  ]
}
```

### Red Colour Detection

The parser identifies "red text" (writer instructions to CS/developers) using a combination of known hex values and a heuristic:

```javascript
// Known red values used in Writer Templates
const knownReds = [
  'FF0000', 'ED1C24', 'CC0000', 'C00000', 'FF3333',
  'FF1111', 'DD0000', 'EE0000', 'BB0000', 'AA0000',
  'FF2222', 'FF4444', 'E00000', 'D00000', 'B00000'
];

// Heuristic: R > 180 && G < 80 && B < 80
```

### Content Boundary Detection

PageForge detects where actual module content begins by searching for the `[TITLE BAR]` tag. Everything before this is boilerplate (submission checklists, LOT tags, guidance text) and is used only for metadata extraction.

### Metadata Extraction

Metadata is extracted from the boilerplate area (before `[TITLE BAR]`):
- **Module Code** — from filename first (regex: `/[A-Z]{4}\d{3}/`), then boilerplate text, then first few content blocks
- **Subject** — from boilerplate text matching `Subject:\s+...`
- **Course** — from boilerplate text matching `Course:\s+...`
- **Writer** — from boilerplate text matching `Key Contact|Writer|Author:\s+...`
- **Date** — from boilerplate text matching `Date\s*(?:submitted)?:\s+\d{1,2}[/-]\d{1,2}[/-]\d{2,4}`

### Stats Tracking

The parser tracks these statistics:
- `totalParagraphs` — number of paragraphs extracted
- `totalTables` — number of tables extracted
- `totalHyperlinks` — number of hyperlink relationships found
- `deletionsRemoved` — number of `<w:del>` elements removed
- `insertionsKept` — number of `<w:ins>` elements unwrapped
- `sdtUnwrapped` — number of `<w:sdt>` elements unwrapped
- `redTextSegments` — number of text runs with red colour detected
- `contentStartParagraph` — index where content starts

---


---

[← Back to index](../CLAUDE.md)
