/**
 * DocxParser — Custom XML parser for Writer Template .docx files.
 *
 * Handles tracked changes (<w:del> / <w:ins>), Google Docs SDT wrappers
 * (<w:sdt>), formatting extraction, hyperlink resolution, tables, lists,
 * and automatic content-boundary detection via the [TITLE BAR] marker.
 *
 * IMPORTANT: This is a hand-rolled parser because third-party libraries
 * (mammoth.js, docx2txt, etc.) silently drop content inside tracked
 * changes and SDT wrappers.
 */

'use strict';

class DocxParser {
    constructor() {
        /** @type {Array<Object>} Extracted paragraph objects */
        this.paragraphs = [];

        /** @type {Array<Object>} Extracted table objects (in document order) */
        this.tables = [];

        /**
         * Ordered list of content blocks in document order.
         * Each entry is { type: 'paragraph' | 'table' | 'pageBreak', data: ... }
         */
        this.content = [];

        /** @type {Object<string, string>} rId → URL mapping from rels */
        this.hyperlinks = {};

        /** @type {Object<string, string>} rId → target mapping for images */
        this.imageRels = {};

        /** @type {Object} Extracted module metadata */
        this.metadata = {};

        /** @type {Object} Numbering definitions from numbering.xml */
        this.numberingDefs = {};

        /** @type {Object<string, number>} Tracks current count per numId+ilvl */
        this.listCounters = {};

        /** @type {Object} Processing statistics */
        this.stats = {
            totalParagraphs: 0,
            totalTables: 0,
            totalHyperlinks: 0,
            deletionsRemoved: 0,
            insertionsKept: 0,
            sdtUnwrapped: 0,
            redTextSegments: 0,
            contentStartParagraph: 0
        };

        /** WordprocessingML namespace */
        this.W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main';

        /** Relationships namespace */
        this.R_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships';

        /** Progress callback */
        this.onProgress = null;
    }

    // ------------------------------------------------------------------
    // Public API
    // ------------------------------------------------------------------

    /**
     * Parse a .docx File object and return structured content.
     * @param {File} file
     * @returns {Promise<Object>}
     */
    async parse(file) {
        this._reset();
        this._filename = file.name || '';

        this._progress('Unzipping document...');
        const zip = await JSZip.loadAsync(file);

        // Validate: must contain word/document.xml
        if (!zip.file('word/document.xml')) {
            throw new Error('MISSING_DOCUMENT_XML');
        }

        // Read required files
        this._progress('Reading document structure...');
        const documentXml = await zip.file('word/document.xml').async('string');

        // Read optional rels file for hyperlinks / images
        let relsXml = null;
        const relsFile = zip.file('word/_rels/document.xml.rels');
        if (relsFile) {
            relsXml = await relsFile.async('string');
        }

        // Read optional numbering.xml for list definitions
        let numberingXml = null;
        const numberingFile = zip.file('word/numbering.xml');
        if (numberingFile) {
            numberingXml = await numberingFile.async('string');
        }

        // Parse hyperlinks / image rels
        this._progress('Resolving hyperlinks...');
        if (relsXml) {
            this._parseRels(relsXml);
        }

        // Parse numbering definitions
        if (numberingXml) {
            this._parseNumbering(numberingXml);
        }

        // Parse the main document body
        this._progress('Parsing XML structure...');
        const parser = new DOMParser();
        const doc = parser.parseFromString(documentXml, 'application/xml');

        // Check for parser errors
        const parserError = doc.querySelector('parsererror');
        if (parserError) {
            throw new Error('INVALID_XML');
        }

        const body = doc.getElementsByTagNameNS(this.W_NS, 'body')[0];
        if (!body) {
            throw new Error('MISSING_BODY');
        }

        this._progress('Extracting formatted text...');
        this._walkBody(body);

        // Detect content boundaries
        this._progress('Detecting content boundaries...');
        const contentStart = this._findContentStart();
        this.stats.contentStartParagraph = contentStart.index;

        // Extract metadata from boilerplate
        this._extractMetadata(contentStart.index);

        this._progress(
            'Done! Found ' + this.stats.totalParagraphs + ' paragraphs, ' +
            this.stats.totalTables + ' tables, ' +
            this.stats.totalHyperlinks + ' hyperlinks'
        );

        return {
            content: this.content,
            paragraphs: this.paragraphs,
            tables: this.tables,
            metadata: this.metadata,
            stats: this.stats,
            contentStartIndex: contentStart.index,
            contentStartFound: contentStart.found
        };
    }

    // ------------------------------------------------------------------
    // Internal: reset state
    // ------------------------------------------------------------------

    _reset() {
        this.paragraphs = [];
        this.tables = [];
        this.content = [];
        this.hyperlinks = {};
        this.imageRels = {};
        this.metadata = {};
        this.numberingDefs = {};
        this.listCounters = {};
        this.stats = {
            totalParagraphs: 0,
            totalTables: 0,
            totalHyperlinks: 0,
            deletionsRemoved: 0,
            insertionsKept: 0,
            sdtUnwrapped: 0,
            redTextSegments: 0,
            contentStartParagraph: 0
        };
    }

    // ------------------------------------------------------------------
    // Internal: progress reporting
    // ------------------------------------------------------------------

    _progress(message) {
        if (typeof this.onProgress === 'function') {
            this.onProgress(message);
        }
    }

    // ------------------------------------------------------------------
    // Internal: parse relationships
    // ------------------------------------------------------------------

    _parseRels(relsXml) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(relsXml, 'application/xml');
        const rels = doc.getElementsByTagName('Relationship');

        for (let i = 0; i < rels.length; i++) {
            const rel = rels[i];
            const id = rel.getAttribute('Id');
            const target = rel.getAttribute('Target');
            const type = rel.getAttribute('Type') || '';

            if (type.endsWith('/hyperlink')) {
                this.hyperlinks[id] = target;
                this.stats.totalHyperlinks++;
            } else if (type.endsWith('/image')) {
                this.imageRels[id] = target;
            }
        }
    }

    // ------------------------------------------------------------------
    // Internal: parse numbering definitions
    // ------------------------------------------------------------------

    _parseNumbering(numberingXml) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(numberingXml, 'application/xml');

        // Build abstract numbering map: abstractNumId → levels
        const abstractNums = {};
        const abstractNumEls = doc.getElementsByTagNameNS(this.W_NS, 'abstractNum');
        for (let i = 0; i < abstractNumEls.length; i++) {
            const an = abstractNumEls[i];
            const anId = an.getAttributeNS(this.W_NS, 'abstractNumId') || an.getAttribute('w:abstractNumId');
            const levels = {};
            const lvls = an.getElementsByTagNameNS(this.W_NS, 'lvl');
            for (let j = 0; j < lvls.length; j++) {
                const lvl = lvls[j];
                const ilvl = lvl.getAttributeNS(this.W_NS, 'ilvl') || lvl.getAttribute('w:ilvl');
                const numFmt = lvl.getElementsByTagNameNS(this.W_NS, 'numFmt')[0];
                const fmt = numFmt
                    ? (numFmt.getAttributeNS(this.W_NS, 'val') || numFmt.getAttribute('w:val'))
                    : 'bullet';
                levels[ilvl] = fmt;
            }
            abstractNums[anId] = levels;
        }

        // Build numId → abstractNumId mapping
        const numEls = doc.getElementsByTagNameNS(this.W_NS, 'num');
        for (let i = 0; i < numEls.length; i++) {
            const num = numEls[i];
            const numId = num.getAttributeNS(this.W_NS, 'numId') || num.getAttribute('w:numId');
            const absRef = num.getElementsByTagNameNS(this.W_NS, 'abstractNumId')[0];
            if (absRef) {
                const absId = absRef.getAttributeNS(this.W_NS, 'val') || absRef.getAttribute('w:val');
                if (abstractNums[absId]) {
                    this.numberingDefs[numId] = abstractNums[absId];
                }
            }
        }
    }

    // ------------------------------------------------------------------
    // Internal: walk the document body
    // ------------------------------------------------------------------

    /**
     * Recursively walk <w:body> and its children, extracting paragraphs
     * and tables in document order.
     */
    _walkBody(node) {
        for (let i = 0; i < node.childNodes.length; i++) {
            const child = node.childNodes[i];
            if (child.nodeType !== 1) continue; // element nodes only

            const localName = child.localName;

            if (localName === 'p' && this._isWNS(child)) {
                this._handleParagraph(child);
            } else if (localName === 'tbl' && this._isWNS(child)) {
                this._handleTable(child);
            } else if (localName === 'sdt' && this._isWNS(child)) {
                // SDT wrapper: unwrap and recurse into sdtContent
                this.stats.sdtUnwrapped++;
                const sdtContent = this._getChildNS(child, 'sdtContent');
                if (sdtContent) {
                    this._walkBody(sdtContent);
                }
            } else if (localName === 'del' && this._isWNS(child)) {
                // Tracked deletion at body level: skip entirely
                this.stats.deletionsRemoved++;
            } else if (localName === 'ins' && this._isWNS(child)) {
                // Tracked insertion at body level: strip wrapper, process children
                this.stats.insertionsKept++;
                this._walkBody(child);
            } else if (localName === 'sectPr' && this._isWNS(child)) {
                // Section properties — check for page break
                // (section breaks between content blocks)
            }
        }
    }

    // ------------------------------------------------------------------
    // Internal: paragraph handling
    // ------------------------------------------------------------------

    _handleParagraph(pElement) {
        // Check for section/page break in paragraph properties
        const pPr = this._getChildNS(pElement, 'pPr');
        let isPageBreak = false;

        if (pPr) {
            // Check for section break
            const sectPr = this._getChildNS(pPr, 'sectPr');
            if (sectPr) {
                isPageBreak = true;
            }
            // Check for page break before
            const pageBreakBefore = this._getChildNS(pPr, 'pageBreakBefore');
            if (pageBreakBefore) {
                isPageBreak = true;
            }
        }

        const para = this._extractParagraph(pElement);
        this.paragraphs.push(para);
        this.stats.totalParagraphs++;

        if (isPageBreak) {
            this.content.push({ type: 'pageBreak', data: null });
        }
        this.content.push({ type: 'paragraph', data: para, index: this.paragraphs.length - 1 });
    }

    _handleTable(tblElement) {
        const table = this._extractTable(tblElement);
        this.tables.push(table);
        this.stats.totalTables++;
        this.content.push({ type: 'table', data: table });
    }

    // ------------------------------------------------------------------
    // Internal: extract paragraph
    // ------------------------------------------------------------------

    _extractParagraph(pElement) {
        const result = {
            runs: [],
            text: '',
            heading: null,
            listLevel: null,
            listNumId: null,
            listFormat: null,
            isListItem: false
        };

        // Check paragraph properties
        const pPr = this._getChildNS(pElement, 'pPr');
        if (pPr) {
            // Heading style
            const pStyle = this._getChildNS(pPr, 'pStyle');
            if (pStyle) {
                const styleVal = pStyle.getAttributeNS(this.W_NS, 'val') || pStyle.getAttribute('w:val');
                if (styleVal && /^Heading[1-6]$/i.test(styleVal)) {
                    result.heading = parseInt(styleVal.replace(/\D/g, ''), 10);
                }
            }

            // List properties
            const numPr = this._getChildNS(pPr, 'numPr');
            if (numPr) {
                const ilvl = this._getChildNS(numPr, 'ilvl');
                const numId = this._getChildNS(numPr, 'numId');
                if (ilvl) {
                    result.listLevel = parseInt(
                        ilvl.getAttributeNS(this.W_NS, 'val') || ilvl.getAttribute('w:val') || '0',
                        10
                    );
                }
                if (numId) {
                    result.listNumId = numId.getAttributeNS(this.W_NS, 'val') || numId.getAttribute('w:val');
                }

                // Determine list format from numbering definitions
                if (result.listNumId && this.numberingDefs[result.listNumId]) {
                    const lvlDef = this.numberingDefs[result.listNumId];
                    const lvlKey = String(result.listLevel || 0);
                    result.listFormat = lvlDef[lvlKey] || 'bullet';
                } else {
                    result.listFormat = 'bullet';
                }

                // numId of "0" means list numbering is explicitly removed
                if (result.listNumId && result.listNumId !== '0') {
                    result.isListItem = true;
                }
            }
        }

        // Walk paragraph children to extract runs, hyperlinks, etc.
        this._extractParagraphContent(pElement, result);

        // Build combined text
        result.text = result.runs.map(function (r) { return r.text; }).join('');

        return result;
    }

    /**
     * Walk the children of a paragraph (or hyperlink, ins, sdt, etc.)
     * and extract runs into the result.
     */
    _extractParagraphContent(node, result) {
        for (let i = 0; i < node.childNodes.length; i++) {
            const child = node.childNodes[i];
            if (child.nodeType !== 1) continue;

            const localName = child.localName;

            if (localName === 'r' && this._isWNS(child)) {
                // Del-ancestor safety check
                if (this._hasDelAncestor(child)) {
                    this.stats.deletionsRemoved++;
                    continue;
                }
                const run = this._extractRun(child);
                if (run) {
                    result.runs.push(run);
                }
            } else if (localName === 'hyperlink' && this._isWNS(child)) {
                this._extractHyperlink(child, result);
            } else if (localName === 'del' && this._isWNS(child)) {
                // Tracked deletion: skip entirely
                this.stats.deletionsRemoved++;
            } else if (localName === 'ins' && this._isWNS(child)) {
                // Tracked insertion: strip wrapper, keep content
                this.stats.insertionsKept++;
                this._extractParagraphContent(child, result);
            } else if (localName === 'sdt' && this._isWNS(child)) {
                // SDT wrapper inside paragraph: unwrap
                this.stats.sdtUnwrapped++;
                const sdtContent = this._getChildNS(child, 'sdtContent');
                if (sdtContent) {
                    this._extractParagraphContent(sdtContent, result);
                }
            } else if (localName === 'bookmarkStart' || localName === 'bookmarkEnd') {
                // Skip bookmark markers
            } else if (localName === 'pPr') {
                // Already handled above
            }
        }
    }

    // ------------------------------------------------------------------
    // Internal: extract a run
    // ------------------------------------------------------------------

    _extractRun(rElement) {
        let text = '';
        const formatting = {
            bold: false,
            italic: false,
            underline: false,
            strikethrough: false,
            color: null,
            highlight: null,
            isRed: false
        };

        // Extract formatting from <w:rPr>
        const rPr = this._getChildNS(rElement, 'rPr');
        if (rPr) {
            formatting.bold = this._checkBoolProp(rPr, 'b');
            formatting.italic = this._checkBoolProp(rPr, 'i');
            formatting.strikethrough = this._checkBoolProp(rPr, 'strike');

            // Underline
            const u = this._getChildNS(rPr, 'u');
            if (u) {
                const uVal = u.getAttributeNS(this.W_NS, 'val') || u.getAttribute('w:val');
                formatting.underline = uVal !== 'none';
            }

            // Color
            const color = this._getChildNS(rPr, 'color');
            if (color) {
                const colorVal = color.getAttributeNS(this.W_NS, 'val') || color.getAttribute('w:val');
                if (colorVal && colorVal !== 'auto') {
                    formatting.color = colorVal.toUpperCase();
                    formatting.isRed = this._isRedColor(colorVal);
                    if (formatting.isRed) {
                        this.stats.redTextSegments++;
                    }
                }
            }

            // Highlight
            const highlight = this._getChildNS(rPr, 'highlight');
            if (highlight) {
                formatting.highlight = highlight.getAttributeNS(this.W_NS, 'val') || highlight.getAttribute('w:val');
            }
        }

        // Extract text content from children
        for (let i = 0; i < rElement.childNodes.length; i++) {
            const child = rElement.childNodes[i];
            if (child.nodeType !== 1) continue;

            const localName = child.localName;

            if (localName === 't' && this._isWNS(child)) {
                text += child.textContent || '';
            } else if (localName === 'br' && this._isWNS(child)) {
                text += '\n';
            } else if (localName === 'tab' && this._isWNS(child)) {
                text += '\t';
            } else if (localName === 'drawing' || localName === 'pict') {
                // Check for image
                const imageRef = this._extractImageRef(child);
                if (imageRef) {
                    text += '[IMAGE: ' + imageRef + ']';
                }
            }
        }

        if (text === '' && !formatting.isRed) {
            return null;
        }

        return {
            text: text,
            formatting: formatting
        };
    }

    // ------------------------------------------------------------------
    // Internal: extract image reference
    // ------------------------------------------------------------------

    _extractImageRef(drawingEl) {
        // Look for blip elements which reference images
        const blips = drawingEl.getElementsByTagName('a:blip');
        if (blips.length > 0) {
            const embed = blips[0].getAttribute('r:embed');
            if (embed && this.imageRels[embed]) {
                const target = this.imageRels[embed];
                // Extract just the filename
                return target.split('/').pop();
            }
        }
        // Also check for v:imagedata (VML images)
        const imgData = drawingEl.getElementsByTagName('v:imagedata');
        if (imgData.length > 0) {
            const rId = imgData[0].getAttribute('r:id');
            if (rId && this.imageRels[rId]) {
                return this.imageRels[rId].split('/').pop();
            }
        }
        return null;
    }

    // ------------------------------------------------------------------
    // Internal: extract hyperlink
    // ------------------------------------------------------------------

    _extractHyperlink(hyperlinkEl, result) {
        const rId = hyperlinkEl.getAttributeNS(this.R_NS, 'id') || hyperlinkEl.getAttribute('r:id');
        const url = rId ? (this.hyperlinks[rId] || null) : null;

        // Extract runs inside the hyperlink
        const linkRuns = [];
        this._extractParagraphContent(hyperlinkEl, { runs: linkRuns });

        // Mark runs with the URL
        for (let i = 0; i < linkRuns.length; i++) {
            linkRuns[i].hyperlink = url;
            result.runs.push(linkRuns[i]);
        }
    }

    // ------------------------------------------------------------------
    // Internal: extract table
    // ------------------------------------------------------------------

    _extractTable(tblElement) {
        const rows = [];
        const trElements = this._getChildrenNS(tblElement, 'tr');

        for (let i = 0; i < trElements.length; i++) {
            const tr = trElements[i];

            // Del-ancestor check for rows
            if (this._hasDelAncestor(tr)) {
                this.stats.deletionsRemoved++;
                continue;
            }

            const cells = [];
            const tcElements = this._getChildrenNS(tr, 'tc');

            for (let j = 0; j < tcElements.length; j++) {
                const tc = tcElements[j];
                const cellParagraphs = [];

                // Each cell can contain paragraphs, tables, SDTs
                for (let k = 0; k < tc.childNodes.length; k++) {
                    const child = tc.childNodes[k];
                    if (child.nodeType !== 1) continue;

                    const localName = child.localName;

                    if (localName === 'p' && this._isWNS(child)) {
                        cellParagraphs.push(this._extractParagraph(child));
                    } else if (localName === 'sdt' && this._isWNS(child)) {
                        this.stats.sdtUnwrapped++;
                        const sdtContent = this._getChildNS(child, 'sdtContent');
                        if (sdtContent) {
                            for (let m = 0; m < sdtContent.childNodes.length; m++) {
                                const sc = sdtContent.childNodes[m];
                                if (sc.nodeType === 1 && sc.localName === 'p' && this._isWNS(sc)) {
                                    cellParagraphs.push(this._extractParagraph(sc));
                                }
                            }
                        }
                    } else if (localName === 'del' && this._isWNS(child)) {
                        this.stats.deletionsRemoved++;
                    } else if (localName === 'ins' && this._isWNS(child)) {
                        this.stats.insertionsKept++;
                        for (let m = 0; m < child.childNodes.length; m++) {
                            const ic = child.childNodes[m];
                            if (ic.nodeType === 1 && ic.localName === 'p' && this._isWNS(ic)) {
                                cellParagraphs.push(this._extractParagraph(ic));
                            }
                        }
                    }
                }

                cells.push({ paragraphs: cellParagraphs });
            }

            // Handle inserted rows (strip <w:ins> wrapper around <w:tr>)
            if (tr.localName === 'ins') {
                this.stats.insertionsKept++;
            }

            rows.push({ cells: cells });
        }

        return { rows: rows };
    }

    // ------------------------------------------------------------------
    // Internal: get table rows, handling ins/del wrappers around rows
    // ------------------------------------------------------------------

    _getChildrenNS(parent, localName) {
        const results = [];
        for (let i = 0; i < parent.childNodes.length; i++) {
            const child = parent.childNodes[i];
            if (child.nodeType !== 1) continue;

            if (child.localName === localName && this._isWNS(child)) {
                results.push(child);
            } else if (child.localName === 'ins' && this._isWNS(child)) {
                // Insertion wrapper: look for the target elements inside
                for (let j = 0; j < child.childNodes.length; j++) {
                    const inner = child.childNodes[j];
                    if (inner.nodeType === 1 && inner.localName === localName && this._isWNS(inner)) {
                        results.push(inner);
                    }
                }
            } else if (child.localName === 'del' && this._isWNS(child)) {
                // Deletion wrapper: skip entirely
                this.stats.deletionsRemoved++;
            } else if (child.localName === 'sdt' && this._isWNS(child)) {
                // SDT wrapper: unwrap
                this.stats.sdtUnwrapped++;
                const sdtContent = this._getChildNS(child, 'sdtContent');
                if (sdtContent) {
                    for (let j = 0; j < sdtContent.childNodes.length; j++) {
                        const inner = sdtContent.childNodes[j];
                        if (inner.nodeType === 1 && inner.localName === localName && this._isWNS(inner)) {
                            results.push(inner);
                        }
                    }
                }
            }
        }
        return results;
    }

    // ------------------------------------------------------------------
    // Internal: content boundary detection
    // ------------------------------------------------------------------

    _findContentStart() {
        for (let i = 0; i < this.content.length; i++) {
            const block = this.content[i];
            if (block.type === 'paragraph') {
                const text = block.data.text;
                if (text && text.toUpperCase().indexOf('[TITLE BAR]') !== -1) {
                    return { index: i, found: true };
                }
            }
        }
        // Not found — return 0 (show everything)
        return { index: 0, found: false };
    }

    // ------------------------------------------------------------------
    // Internal: metadata extraction from boilerplate
    // ------------------------------------------------------------------

    _extractMetadata(contentStartIndex) {
        this.metadata = {
            moduleCode: '',
            subject: '',
            course: '',
            writer: '',
            date: ''
        };

        // Scan all content before the content start for metadata
        const boilerplateText = [];
        for (let i = 0; i < contentStartIndex && i < this.content.length; i++) {
            const block = this.content[i];
            if (block.type === 'paragraph') {
                boilerplateText.push(block.data.text);
            } else if (block.type === 'table') {
                // Tables in boilerplate often contain the metadata
                const table = block.data;
                for (let r = 0; r < table.rows.length; r++) {
                    for (let c = 0; c < table.rows[r].cells.length; c++) {
                        const cell = table.rows[r].cells[c];
                        for (let p = 0; p < cell.paragraphs.length; p++) {
                            boilerplateText.push(cell.paragraphs[p].text);
                        }
                    }
                }
            }
        }

        const fullText = boilerplateText.join('\n');

        // Look for Module Code — try filename first (most reliable)
        const filenameCodeMatch = this._filename
            ? this._filename.match(/[A-Z]{4}\d{3}/)
            : null;
        if (filenameCodeMatch) {
            this.metadata.moduleCode = filenameCodeMatch[0];
        }

        // Fall back to boilerplate text
        if (!this.metadata.moduleCode) {
            const codeMatch = fullText.match(/Module\s*Code[:\s]*([A-Z]{2,6}\d{2,4})/i);
            if (codeMatch) {
                this.metadata.moduleCode = codeMatch[1].toUpperCase();
            }
        }

        // Fall back to scanning content after [TITLE BAR]
        if (!this.metadata.moduleCode) {
            for (let i = contentStartIndex; i < this.content.length && i < contentStartIndex + 5; i++) {
                const block = this.content[i];
                if (block.type === 'paragraph' && block.data.text) {
                    const titleBarMatch = block.data.text.match(/[A-Z]{4}\d{3}/);
                    if (titleBarMatch) {
                        this.metadata.moduleCode = titleBarMatch[0];
                        break;
                    }
                }
            }
        }

        // Look for Subject
        const subjectMatch = fullText.match(/Subject[:\s]+([^\n\r]+)/i);
        if (subjectMatch) {
            this.metadata.subject = subjectMatch[1].trim();
        }

        // Look for Course
        const courseMatch = fullText.match(/Course[:\s]+([^\n\r]+)/i);
        if (courseMatch) {
            this.metadata.course = courseMatch[1].trim();
        }

        // Look for Writer/Key Contact
        const writerMatch = fullText.match(/(?:Key\s*Contact|Writer|Author)[:\s]+([^\n\r]+)/i);
        if (writerMatch) {
            this.metadata.writer = writerMatch[1].trim();
        }

        // Look for Date
        const dateMatch = fullText.match(/Date\s*(?:submitted)?[:\s]+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})/i);
        if (dateMatch) {
            this.metadata.date = dateMatch[1].trim();
        }
    }

    // ------------------------------------------------------------------
    // Internal: del-ancestor safety check
    // ------------------------------------------------------------------

    /**
     * Walk up the ancestor chain from node. If ANY ancestor is <w:del>,
     * return true. Stops at block-level boundaries (w:p, w:tbl, w:body).
     */
    _hasDelAncestor(node) {
        let current = node.parentNode;
        while (current && current.nodeType === 1) {
            const localName = current.localName;
            // Stop at block-level boundaries
            if (localName === 'p' || localName === 'tbl' || localName === 'body') {
                return false;
            }
            if (localName === 'del' && this._isWNS(current)) {
                return true;
            }
            current = current.parentNode;
        }
        return false;
    }

    // ------------------------------------------------------------------
    // Internal: XML helpers
    // ------------------------------------------------------------------

    /** Check if an element is in the WordprocessingML namespace */
    _isWNS(el) {
        return !el.namespaceURI || el.namespaceURI === this.W_NS;
    }

    /** Get the first child element with the given local name in W namespace */
    _getChildNS(parent, localName) {
        for (let i = 0; i < parent.childNodes.length; i++) {
            const child = parent.childNodes[i];
            if (child.nodeType === 1 && child.localName === localName && this._isWNS(child)) {
                return child;
            }
        }
        return null;
    }

    /**
     * Check a boolean formatting property like <w:b>, <w:i>, <w:strike>.
     * Returns true if the element is present AND its value is not explicitly
     * "false" or "0".
     */
    _checkBoolProp(rPr, propName) {
        const el = this._getChildNS(rPr, propName);
        if (!el) return false;
        const val = el.getAttributeNS(this.W_NS, 'val') || el.getAttribute('w:val');
        if (val === 'false' || val === '0') return false;
        return true;
    }

    /**
     * Determine if a hex colour value represents "red".
     * Common red values in Writer Template documents.
     */
    _isRedColor(hex) {
        if (!hex) return false;
        hex = hex.toUpperCase().replace('#', '');

        // Known red values used in Writer Templates
        const knownReds = [
            'FF0000', 'ED1C24', 'CC0000', 'C00000', 'FF3333',
            'FF1111', 'DD0000', 'EE0000', 'BB0000', 'AA0000',
            'FF2222', 'FF4444', 'E00000', 'D00000', 'B00000'
        ];

        if (knownReds.indexOf(hex) !== -1) return true;

        // Heuristic: if red channel is high and green/blue are low
        if (hex.length === 6) {
            const r = parseInt(hex.substring(0, 2), 16);
            const g = parseInt(hex.substring(2, 4), 16);
            const b = parseInt(hex.substring(4, 6), 16);
            if (r > 180 && g < 80 && b < 80) return true;
        }

        return false;
    }
}
