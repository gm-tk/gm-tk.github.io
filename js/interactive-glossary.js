/**
 * InteractiveGlossary — Renders the [glossary] interactive as a structured
 * `<table class="table table-fixed">` inside the standard Bootstrap-grid +
 * `alert` wrapper.
 *
 * Boundary semantics mirror the hint_slider termination rules: walk forward
 * from the [glossary] tag's raw block index, capturing consecutive paragraphs
 * whose text matches `Term – Meaning` (space-padded en-dash, U+2013), and
 * terminate at:
 *   • a paragraph whose primary tag puts it in a different category
 *     (heading, interactive, structural, styling, activity, link, body, media)
 *   • a non-paragraph block (e.g. table, page break)
 *   • a paragraph that lacks the en-dash separator
 *
 * Output structure (canonical):
 *
 *   <div class="row">
 *     <div class="col-md-8 col-12">
 *       <div class="alert">
 *         <div class="row">
 *           <div class="col-12">
 *             <h4>Glossary</h4>
 *             <div class="table-responsive">
 *               <table class="table table-fixed">
 *                 <tr class="title-g">
 *                   <th>Term</th>
 *                   <th>Meaning</th>
 *                 </tr>
 *                 <tbody>
 *                   <tr><td>{term}</td><td>{meaning}</td></tr>
 *                   ...
 *                 </tbody>
 *               </table>
 *             </div>
 *           </div>
 *         </div>
 *       </div>
 *     </div>
 *   </div>
 *
 * The header `<tr class="title-g">` deliberately sits OUTSIDE the `<tbody>` —
 * no `<thead>` is emitted.
 */

'use strict';

class InteractiveGlossary {
    /**
     * @param {TagNormaliser} normaliser - For boundary tag detection.
     * @param {Object} coreRef - Object exposing `_buildFormattedText(paraData)`
     *     and `_convertInlineFormatting(text)` (typically the HtmlConverter).
     */
    constructor(normaliser, coreRef) {
        this._normaliser = normaliser;
        this._coreRef = coreRef;
    }

    /**
     * Walk rawBlocks from `tagIndex` and emit the glossary HTML.
     *
     * @param {Array} processedBlocks
     * @param {number} tagIndex - Index of the [glossary] tag in processedBlocks.
     * @param {Array} rawBlocks - Raw content blocks (parser output, before filter).
     * @param {Array<number>} procToRawMap - Mapping from processed → raw indices.
     * @returns {Object|null} `{ html, consumedRawIndices }` when ≥ 1 entry was
     *     captured; `null` when no entries were detected (caller should fall
     *     through to the generic interactive placeholder path).
     */
    render(processedBlocks, tagIndex, rawBlocks, procToRawMap) {
        if (!rawBlocks || procToRawMap[tagIndex] === undefined) return null;

        var startRaw = procToRawMap[tagIndex] + 1;
        var entries = [];
        var consumed = [];

        for (var ri = startRaw; ri < rawBlocks.length; ri++) {
            var block = rawBlocks[ri];
            if (!block || block.type !== 'paragraph' || !block.data) break;

            var text = this._coreRef._buildFormattedText(block.data);
            var tagResult = this._normaliser.processBlock(text);
            var primaryTag = tagResult.tags && tagResult.tags.length > 0
                ? tagResult.tags[0]
                : null;

            if (primaryTag) break;

            var clean = (tagResult.cleanText || '').trim();
            if (!clean) {
                consumed.push(ri);
                continue;
            }

            var entry = this._parseEntry(clean);
            if (!entry) break;

            entries.push(entry);
            consumed.push(ri);
        }

        if (entries.length === 0) return null;

        return {
            html: this._buildHtml(entries),
            consumedRawIndices: consumed
        };
    }

    /**
     * Split an entry line on the FIRST en-dash (U+2013). Surrounding spaces are
     * trimmed but parenthetical abbreviations in the term (e.g. "Generative AI
     * (Gen AI)") are preserved verbatim because parentheses are not part of the
     * separator.
     *
     * @param {string} text
     * @returns {{term: string, meaning: string}|null}
     */
    _parseEntry(text) {
        var idx = text.indexOf('–');
        if (idx === -1) return null;
        var term = text.slice(0, idx).trim();
        var meaning = text.slice(idx + 1).trim();
        if (!term && !meaning) return null;
        return { term: term, meaning: meaning };
    }

    _buildHtml(entries) {
        var inline = this._coreRef._convertInlineFormatting.bind(this._coreRef);

        var rows = '';
        for (var i = 0; i < entries.length; i++) {
            rows += '                  <tr><td>' + inline(entries[i].term) +
                '</td><td>' + inline(entries[i].meaning) + '</td></tr>\n';
        }

        return '    <div class="row">\n' +
            '      <div class="col-md-8 col-12">\n' +
            '        <div class="alert">\n' +
            '          <div class="row">\n' +
            '            <div class="col-12">\n' +
            '              <h4>Glossary</h4>\n' +
            '              <div class="table-responsive">\n' +
            '                <table class="table table-fixed">\n' +
            '                  <tr class="title-g">\n' +
            '                    <th>Term</th>\n' +
            '                    <th>Meaning</th>\n' +
            '                  </tr>\n' +
            '                  <tbody>\n' +
            rows +
            '                  </tbody>\n' +
            '                </table>\n' +
            '              </div>\n' +
            '            </div>\n' +
            '          </div>\n' +
            '        </div>\n' +
            '      </div>\n' +
            '    </div>';
    }
}
