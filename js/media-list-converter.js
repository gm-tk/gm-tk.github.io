'use strict';

/**
 * MediaListConverter — straight, full-document .docx → plain-text conversion for
 * the Module Development mode "Media List" slot.
 *
 * A Media List is NOT a module Writer's Template: it has no [TITLE BAR], no
 * leading generic statements / submission checklists to discard, and no
 * phase / template / HTML processing. This converter therefore performs a
 * STRAIGHT FULL conversion of the ENTIRE document — every block from index 0 —
 * into the SAME plain-text output format the Writer's Template pipeline already
 * produces, by reusing the shared OutputFormatter. It reuses the shared
 * DocxParser for .docx reading rather than re-implementing any docx parsing.
 *
 * Contrast with the Writer's Template path (ModeToggle._convertSlot):
 *   • Writer's Template → DocxParser.parse() (runs _findContentStart, the
 *     [TITLE BAR] intro-skipper) + OutputFormatter.formatAll() (emits from
 *     contentStartIndex, discarding the leading boilerplate).
 *   • Media List       → DocxParser.parse() + this.convertParsedResult(), which
 *     ALWAYS starts at block 0 — nothing is skipped.
 *
 * Headless-testable: convertParsedResult() is a pure, synchronous function over
 * an already-parsed DocxParser result, so the Node test runner (which has no
 * DOM / JSZip and never loads DocxParser) can exercise the full conversion and
 * the output format through the real OutputFormatter, without the file layer.
 */
class MediaListConverter {
    /**
     * @param {Object} [options]
     * @param {DocxParser} [options.parser] - shared .docx reader (injected in tests).
     * @param {OutputFormatter} [options.formatter] - shared text formatter.
     */
    constructor(options) {
        options = options || {};
        this._parser = options.parser || null;
        this._formatter = options.formatter || null;
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
     * Convert an already-parsed DocxParser result to output text.
     *
     * FULL document, NO [TITLE BAR] skipping (always starts at block 0), NO
     * phase / template processing. Emits the SAME envelope and format as
     * OutputFormatter.formatAll() (metadata header + content), differing ONLY in
     * that it never skips leading blocks. Malformed / empty results degrade
     * gracefully to an empty content body rather than throwing.
     *
     * @param {Object} result - DocxParser.parse() result (or a partial/empty one).
     * @returns {string}
     */
    convertParsedResult(result) {
        result = result || {};
        var content = Array.isArray(result.content) ? result.content : [];
        var formatter = this._getFormatter();
        if (!formatter) {
            throw new Error('MediaListConverter requires an OutputFormatter');
        }

        var metadataBlock = formatter.formatMetadata(result.metadata || {});
        // startIndex 0 → no skipping; startFound true → suppress the
        // "[TITLE BAR] not found" warning, which is irrelevant for a media list
        // (it is not a module template and has no title bar).
        var contentBlock = formatter.formatContent(content, 0, true);
        // Mirror formatAll()'s post-processing exactly so the format is identical.
        contentBlock = formatter._stripEmptyRedText(contentBlock);

        return metadataBlock + '\n' + contentBlock;
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

    _getFormatter() {
        if (!this._formatter && typeof OutputFormatter !== 'undefined') {
            this._formatter = new OutputFormatter();
        }
        return this._formatter;
    }
}
