'use strict';

/**
 * MediaListConverter — structural media-table extraction for the Module
 * Development mode "Media List" slot. A Media List .docx is mostly generic,
 * per-module boilerplate (template heading, submission checklist, "Before
 * starting…" guidance, "Please supply details for ALL external media…",
 * early-copyright notes) wrapped around a SINGLE data table holding the actual
 * media list. The downloadable .txt must contain ONLY that table's data.
 *
 * The exclusion is content-agnostic and STRUCTURAL — the boilerplate differs
 * from module to module, so nothing is string-matched against intro phrases.
 * Instead the genuine media table is located by its HEADER ROW: a table whose
 * first row carries the media column labels (Item No., WTPg No., Item Type,
 * Description, Source, URL, and an optional trailing ECR approval), matched
 * case-insensitively and whitespace/punctuation-tolerantly, by content not by
 * position. Only that table's data rows are emitted (the column header once at
 * the top, the conventional "Example" sample row and any horizontally-merged
 * boilerplate row skipped, the auto-numbered Item No. column reconstructed as a
 * sequential ordinal); everything outside the table — every preceding paragraph,
 * heading, checklist and hyperlink guidance — is excluded entirely.
 *
 * It reuses the shared DocxParser for .docx reading rather than re-implementing
 * any docx parsing. If no media table is found (malformed / empty input) it
 * emits an empty-but-valid result rather than throwing, and surfaces a
 * user-facing error via the shared toast (injectable `notify`; falls back to
 * window.app.showToast in the browser).
 *
 * Headless-testable: convertParsedResult() is a pure, synchronous function over
 * an already-parsed DocxParser result, so the Node test runner (which has no
 * DOM / JSZip and never loads DocxParser) can exercise the extraction directly.
 */
class MediaListConverter {
    /**
     * @param {Object} [options]
     * @param {DocxParser} [options.parser] - shared .docx reader (injected in tests).
     * @param {function(string)} [options.notify] - optional error sink (injected
     *        in tests). When absent, _notifyError falls back to the shared
     *        app-wide toast (window.app.showToast) in the browser.
     */
    constructor(options) {
        options = options || {};
        this._parser = options.parser || null;
        this._notify = options.notify || null;
    }

    /**
     * Read + convert a .docx File. Returns a Promise of the output text in the
     * browser; when injected with a synchronous parser (tests) it returns the
     * text directly. Reuses the shared DocxParser — no docx parsing is
     * re-implemented here.
     *
     * @param {File} file
     * @returns {(string|Promise<string>)}
     */
    convert(file) {
        var self = this;
        var parser = this._getParser();
        if (!parser) {
            throw new Error('MediaListConverter requires a DocxParser (none injected and no global available)');
        }
        var parsed = parser.parse(file);
        return (parsed && typeof parsed.then === 'function')
            ? parsed.then(function (result) { return self.convertParsedResult(result); })
            : self.convertParsedResult(parsed);
    }

    /**
     * Extract the media-list table from an already-parsed DocxParser result and
     * return ONLY its data rows as plain text: the column header rendered once
     * at the top, then one tab-separated line per data row (every cell in
     * column order). The conventional "Example" sample row is skipped, any
     * horizontally-merged boilerplate row (e.g. a "Reminder: …" note spanning the
     * table width) is dropped, and all boilerplate outside the table — intro
     * paragraphs, headings, the submission checklist, hyperlink guidance — is
     * excluded structurally. The Item No. column is reconstructed as a sequential
     * ordinal per retained data row (Word auto-numbers it, so its literal text is
     * empty); the header row keeps its literal labels.
     *
     * When no media table is found (malformed / empty input) this returns an
     * empty string (it never throws) and surfaces a user-facing error via the
     * shared toast, so the caller still receives a valid, downloadable result.
     *
     * @param {Object} result - DocxParser.parse() result (or a partial/empty one).
     * @returns {string}
     */
    convertParsedResult(result) {
        result = result || {};
        var content = Array.isArray(result.content) ? result.content : [];

        var table = this._findMediaTable(content);
        if (!table) {
            this._notifyError('Media List: no media table found. The document did not contain a recognised media-list header row (Item No., WTPg No., Item Type, Description, Source, URL).');
            return '';
        }

        var rows = table.data.rows;
        var header = this._rowCellTexts(rows[0]);
        var columnCount = header.length;
        var lines = [header.join('\t')]; // header — literal labels, once, at the top
        var itemNo = 0;                  // sequential Item No. across RETAINED data rows
        for (var r = 1; r < rows.length; r++) {
            var cells = this._rowCellTexts(rows[r]);
            // Skip the conventional Example/sample row (literal label in the Item No. col).
            if (this._normaliseHeader(cells[0]).indexOf('example') === 0) { continue; }
            // Skip horizontally-merged boilerplate rows (e.g. the "Reminder: …" note):
            // a single grid-spanning cell across the table width, never a data row.
            if (this._isMergedSpanRow(cells, columnCount)) { continue; }
            // Skip fully-empty rows (no content-bearing cell).
            if (!cells.some(function (c) { return c && c.trim() !== ''; })) { continue; }
            // Reconstruct the auto-numbered Item No. column: genuine data rows carry
            // it as a Word <w:numPr> list number, so the literal cell text is empty
            // and the displayed 1./2./3. is lost by plain-text extraction. Re-derive
            // it as a sequential ordinal in document order (Word-style trailing dot).
            itemNo++;
            cells[0] = itemNo + '.';
            // Guarantee the full column structure incl. the trailing ECR approval cell.
            while (cells.length < columnCount) { cells.push(''); }
            lines.push(cells.join('\t'));
        }
        return lines.join('\n');
    }

    // ------------------------------------------------------------------
    // Structural media-table extraction
    // ------------------------------------------------------------------

    /**
     * Locate the genuine media-list table by its HEADER ROW (by content, not by
     * position): the first table block whose first row carries every required
     * media column label. Returns the table block, or null when none matches.
     */
    _findMediaTable(content) {
        for (var i = 0; i < content.length; i++) {
            var block = content[i];
            if (!block || block.type !== 'table' || !block.data ||
                !Array.isArray(block.data.rows) || block.data.rows.length === 0) {
                continue;
            }
            if (this._isMediaHeaderRow(this._rowCellTexts(block.data.rows[0]))) {
                return block;
            }
        }
        return null;
    }

    /**
     * True when a row's cell labels include every REQUIRED media column (the
     * optional trailing ECR approval column may be absent). Matching is
     * case-insensitive and whitespace/punctuation tolerant.
     */
    _isMediaHeaderRow(cellTexts) {
        var present = {};
        for (var i = 0; i < cellTexts.length; i++) {
            var key = this._normaliseHeader(cellTexts[i]);
            if (key) { present[key] = true; }
        }
        var required = MediaListConverter.REQUIRED_HEADERS;
        for (var r = 0; r < required.length; r++) {
            if (!present[required[r]]) { return false; }
        }
        return true;
    }

    /**
     * True when a row is a horizontally-merged / grid-spanning boilerplate row
     * rather than a genuine data row. In OOXML such a row is a single <w:tc> with
     * a <w:gridSpan> covering the table width (the shared parser surfaces it as
     * ONE cell); some inputs instead repeat the merged text across every spanned
     * cell. Either shape collapses to a single logical cell — never a data row —
     * so it is dropped. A genuine data row keeps one distinct cell per column.
     *
     * @param {string[]} cells - the row's cell texts, in column order.
     * @param {number} columnCount - the header row's column count.
     * @returns {boolean}
     */
    _isMergedSpanRow(cells, columnCount) {
        var nonEmpty = [];
        for (var i = 0; i < cells.length; i++) {
            var t = (cells[i] == null ? '' : String(cells[i])).trim();
            if (t !== '') { nonEmpty.push(t); }
        }
        if (nonEmpty.length === 0) { return false; } // empty row — handled separately
        // (a) The row's cells collapse to a single merged cell spanning a
        //     multi-column table (a horizontal gridSpan → one <w:tc>).
        if (columnCount > 1 && cells.length === 1) { return true; }
        // (b) Every non-empty cell repeats the SAME merged text across the row.
        if (nonEmpty.length > 1) {
            for (var k = 1; k < nonEmpty.length; k++) {
                if (nonEmpty[k] !== nonEmpty[0]) { return false; }
            }
            return true;
        }
        return false;
    }

    /** Cell texts of a table row, in column order (empty array when malformed). */
    _rowCellTexts(row) {
        var cells = (row && Array.isArray(row.cells)) ? row.cells : [];
        var self = this;
        return cells.map(function (cell) { return self._extractCellText(cell); });
    }

    /** Plain text of one table cell — its paragraph texts, joined and trimmed. */
    _extractCellText(cell) {
        if (!cell || !Array.isArray(cell.paragraphs)) { return ''; }
        var parts = [];
        for (var p = 0; p < cell.paragraphs.length; p++) {
            var para = cell.paragraphs[p];
            var text = (para && typeof para.text === 'string') ? para.text.trim() : '';
            if (text) { parts.push(text); }
        }
        return parts.join(' ').trim();
    }

    /** Lower-case, punctuation/whitespace-collapsed header key for matching. */
    _normaliseHeader(s) {
        return String(s == null ? '' : s)
            .toLowerCase()
            .replace(/[^a-z0-9]+/g, ' ')
            .trim()
            .replace(/\s+/g, ' ');
    }

    /**
     * Surface a user-facing error via the injected sink (tests) or the shared
     * app-wide toast (browser). No-ops headlessly when neither is available.
     */
    _notifyError(message) {
        if (typeof this._notify === 'function') { this._notify(message); return; }
        if (typeof window !== 'undefined' && window.app &&
            typeof window.app.showToast === 'function') {
            window.app.showToast(message);
        }
    }

    // ------------------------------------------------------------------
    // Lazy dependency accessors — injected instance wins, else browser global.
    // ------------------------------------------------------------------

    _getParser() {
        if (!this._parser && typeof DocxParser !== 'undefined') {
            this._parser = new DocxParser();
        }
        return this._parser;
    }
}

// Expected media-list column header keys (normalised). The first six are
// REQUIRED; ECR approval is an optional trailing column that may be absent.
MediaListConverter.REQUIRED_HEADERS = ['item no', 'wtpg no', 'item type', 'description', 'source', 'url'];
MediaListConverter.OPTIONAL_HEADERS = ['ecr approval'];
