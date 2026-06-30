'use strict';

/**
 * CommentExtractor — reads native Word comments out of a .docx and attaches them
 * to the parsed content blocks. It "drives DocxParser's extended output": the
 * parser calls these helpers to (a) parse the comment bodies from
 * word/comments.xml, (b) capture which block each comment is anchored to (incl.
 * the media-row hyperlink, `rowUrl`), and (c) carry a comment forward off a
 * dropped/empty paragraph so nothing is silently lost.
 *
 * The body parse and the carry-forward are pure string/array operations (no DOM),
 * so they are headless-testable directly. The per-block anchor capture is thin
 * DOM glue used by DocxParser in the browser.
 *
 * Ported from CONVERTER_V2 (DocxExtractor #parseComments / #parseDocument /
 * findComments). See Comment_Capture_Process_Explained.md §1–§2.
 */
class CommentExtractor {

    // ------------------------------------------------------------------
    // 1. Comment bodies — word/comments.xml → Map<id, {author, text}>
    // ------------------------------------------------------------------

    /**
     * @param {string} commentsXml - raw word/comments.xml (may be null/empty).
     * @returns {Map<string,{author:string,text:string}>}
     */
    parseComments(commentsXml) {
        var map = new Map();
        if (!commentsXml) { return map; }

        // Comments never nest, so a non-greedy body capture is unambiguous.
        var re = /<w:comment\b([^>]*)>([\s\S]*?)<\/w:comment>/g;
        var m;
        while ((m = re.exec(commentsXml)) !== null) {
            var attrs = m[1];
            var body = m[2];

            var idM = /\bw:id="([^"]*)"/.exec(attrs);
            if (!idM) { continue; }
            var id = idM[1];

            var authorM = /\bw:author="([^"]*)"/.exec(attrs);
            var author = authorM ? this._decodeXml(authorM[1]) : '';

            // Join ALL inner <w:t> runs, then collapse whitespace.
            var texts = [];
            var tRe = /<w:t\b[^>]*>([\s\S]*?)<\/w:t>/g;
            var tm;
            while ((tm = tRe.exec(body)) !== null) {
                texts.push(this._decodeXml(tm[1]));
            }
            var text = texts.join('').replace(/\s+/g, ' ').trim();

            map.set(id, { author: author, text: text });
        }
        return map;
    }

    /** Decode the handful of XML entities that appear in comment text/authors. */
    _decodeXml(s) {
        return String(s == null ? '' : s)
            .replace(/&lt;/g, '<')
            .replace(/&gt;/g, '>')
            .replace(/&quot;/g, '"')
            .replace(/&apos;/g, "'")
            .replace(/&#(\d+);/g, function (_, n) { return String.fromCharCode(parseInt(n, 10)); })
            .replace(/&#x([0-9a-fA-F]+);/g, function (_, n) { return String.fromCharCode(parseInt(n, 16)); })
            .replace(/&amp;/g, '&'); // ampersand last so it doesn't double-decode
    }

    // ------------------------------------------------------------------
    // 2a. Anchor capture (DOM glue used by DocxParser)
    // ------------------------------------------------------------------

    /**
     * Comment ids whose <w:commentRangeStart> is a descendant of `element`
     * (a paragraph or a table row). DOM-based; used in the browser.
     *
     * @param {Element} element
     * @param {string} wNs - WordprocessingML namespace URI.
     * @returns {string[]} comment ids, in document order.
     */
    anchorIdsInElement(element, wNs) {
        var ids = [];
        if (!element || typeof element.getElementsByTagNameNS !== 'function') { return ids; }
        var starts = element.getElementsByTagNameNS(wNs, 'commentRangeStart');
        for (var i = 0; i < starts.length; i++) {
            var id = starts[i].getAttributeNS(wNs, 'id') || starts[i].getAttribute('w:id');
            if (id != null && id !== '') { ids.push(id); }
        }
        return ids;
    }

    /**
     * The hyperlink target URLs referenced inside a table row (DOM-based). The
     * first is recorded as `rowUrl`; all are kept for robust media-key matching.
     *
     * @param {Element} trElement
     * @param {Object<string,string>} hyperlinks - rId → URL map (DocxParser.hyperlinks).
     * @param {string} wNs
     * @param {string} rNs - relationships namespace URI.
     * @returns {string[]}
     */
    rowHyperlinkUrls(trElement, hyperlinks, wNs, rNs) {
        var urls = [];
        if (!trElement || typeof trElement.getElementsByTagNameNS !== 'function') { return urls; }
        var links = trElement.getElementsByTagNameNS(wNs, 'hyperlink');
        for (var i = 0; i < links.length; i++) {
            var rid = links[i].getAttributeNS(rNs, 'id') || links[i].getAttribute('r:id');
            if (rid && hyperlinks && hyperlinks[rid] && urls.indexOf(hyperlinks[rid]) === -1) {
                urls.push(hyperlinks[rid]);
            }
        }
        return urls;
    }

    // ------------------------------------------------------------------
    // 2b. Anchor capture (pure string helpers — headless-testable)
    // ------------------------------------------------------------------

    /** Comment ids appearing as <w:commentRangeStart w:id="N"> in an XML string. */
    anchorIdsInXml(xml) {
        var ids = [];
        if (!xml) { return ids; }
        var re = /<w:commentRangeStart\b[^>]*\bw:id="([^"]*)"/g;
        var m;
        while ((m = re.exec(xml)) !== null) { ids.push(m[1]); }
        return ids;
    }

    /** Hyperlink target URLs in a row XML string, resolved through the rels map. */
    rowUrlsFromXml(rowXml, hyperlinks) {
        var urls = [];
        if (!rowXml) { return urls; }
        var re = /r:id="([^"]+)"/g;
        var m;
        while ((m = re.exec(rowXml)) !== null) {
            var rid = m[1];
            if (hyperlinks && hyperlinks[rid] && urls.indexOf(hyperlinks[rid]) === -1) {
                urls.push(hyperlinks[rid]);
            }
        }
        return urls;
    }

    // ------------------------------------------------------------------
    // 3. Carry-forward — nothing silently lost
    // ------------------------------------------------------------------

    /**
     * Reassign comments off blocks that won't render. A comment whose anchor is
     * an empty (dropped) paragraph moves to the NEXT renderable block; comments
     * still pending after the last block attach to the LAST renderable block.
     * Operates in place on the ordered content array.
     *
     * @param {Array<Object>} content - DocxParser content blocks.
     * @param {function(Object):boolean} [isRenderable] - defaults to the
     *        text/table predicate matching OutputFormatter's drop rule.
     */
    applyCarryForward(content, isRenderable) {
        if (!Array.isArray(content)) { return; }
        var renderable = isRenderable || CommentExtractor.isRenderableBlock;

        var pending = [];
        var lastRenderable = -1;
        for (var i = 0; i < content.length; i++) {
            var block = content[i];
            var has = block && block.comments && block.comments.length;
            if (renderable(block)) {
                lastRenderable = i;
                if (pending.length) {
                    block.comments = pending.concat(block.comments || []);
                    pending = [];
                }
            } else if (has) {
                // Block won't render → defer its comments to the next kept block.
                pending = pending.concat(block.comments);
                block.comments = [];
            }
        }
        // Trailing comments → the last renderable block (else leave on origin).
        if (pending.length && lastRenderable >= 0) {
            var last = content[lastRenderable];
            last.comments = (last.comments || []).concat(pending);
        }
    }

    /** Default renderable predicate, mirroring OutputFormatter's drop rule. */
    static isRenderableBlock(block) {
        if (!block) { return false; }
        if (block.type === 'table') { return true; }
        if (block.type === 'paragraph') {
            return !!(block.data && block.data.text && block.data.text.trim() !== '');
        }
        return false; // pageBreak / unknown
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = CommentExtractor;
}
