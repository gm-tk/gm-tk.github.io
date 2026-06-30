'use strict';

/**
 * CommentInserter — places surviving Word comments into the parsed Writer's
 * Template .txt as red notes, and builds the media-match keys that let a Media
 * List row comment find the body element that uses the same media.
 *
 * Two placement paths (ported from CONVERTER_V2; see
 * Comment_Capture_Process_Explained.md §5):
 *   - BODY-anchored (no rowUrl): the note is attached to its own anchor block,
 *     emitted immediately before that block's text (once per block).
 *   - MEDIA-anchored (rowUrl): the comment is keyed by its row URL — plus the
 *     extracted iStock / YouTube reference id — and surfaced before the body
 *     element that references the same media item (never its own anchor block,
 *     once per comment).
 *
 * Notes are attached to `block.commentNotes` (an additive array); OutputFormatter
 * emits them before the block. Rendering reuses OutputFormatter's existing
 * red-text marker via `formatter.wrapRedText` — no new marker, no raw HTML.
 *
 * Pure logic, DOM-free, dependencies injected → headless-testable.
 */
class CommentInserter {
    /**
     * @param {Object} [options]
     * @param {CommentFilter} [options.filter] - whitelist + actionable filter.
     * @param {OutputFormatter} [options.formatter] - supplies the red-text marker.
     * @param {Object} [options.mediaMatch] - the data.media_match config
     *        ({ enabled, id_match }). Defaults to enabled + id_match.
     * @param {string} [options.notePrefix] - the note-line template
     *        (data.render.prefix); {author}/{text} placeholders. Defaults to
     *        "Note from {author}: {text}".
     */
    constructor(options) {
        options = options || {};
        this.filter = options.filter || null;
        this.formatter = options.formatter || null;
        this.mediaMatch = options.mediaMatch || null;
        // Note-line template (data-driven via data.render.prefix); {author}/{text}
        // are filled per comment. Defaults to the shipped convention so the
        // file:// fallback and the headless tests match the canonical data file.
        this.notePrefix = options.notePrefix || 'Note from {author}: {text}';
    }

    _mediaEnabled() {
        return this.mediaMatch ? this.mediaMatch.enabled !== false : true;
    }

    _idMatch() {
        return this.mediaMatch ? this.mediaMatch.id_match !== false : true;
    }

    // ------------------------------------------------------------------
    // Note rendering — reuse the formatter's red-text marker
    // ------------------------------------------------------------------

    /** Render one comment as a red note line from the (data-driven) template,
     *  e.g. "Note from {author}: {text}". split/join is used so a literal "$" in
     *  the author or comment text is never treated as a replacement special. */
    renderNote(author, text) {
        var line = this.notePrefix
            .split('{author}').join(String(author))
            .split('{text}').join(String(text));
        if (this.formatter && typeof this.formatter.wrapRedText === 'function') {
            return this.formatter.wrapRedText(line);
        }
        // Fallback: the same marker convention OutputFormatter uses.
        return '🔴[RED TEXT] ' + line + ' [/RED TEXT]🔴';
    }

    _attachNote(block, author, text) {
        if (!block) { return; }
        if (!block.commentNotes) { block.commentNotes = []; }
        block.commentNotes.push(this.renderNote(author, text));
    }

    // ------------------------------------------------------------------
    // Media keys
    // ------------------------------------------------------------------

    /**
     * Media keys for a URL: the exact URL, plus (when id_match is on) the iStock
     * reference (gm-form or /id/ CDN form) and the YouTube video id, so a
     * placeholder image with no live link still matches by its shared id.
     *
     * @param {string} url
     * @param {boolean} [idMatch=true]
     * @returns {string[]}
     */
    mediaKeys(url, idMatch) {
        var keys = [];
        if (!url) { return keys; }
        if (idMatch === undefined) { idMatch = true; }
        keys.push(url);
        if (idMatch) {
            var gm = /gm-?(\d{6,})/i.exec(url);
            if (gm) { keys.push('istock:' + gm[1]); }
            var cdn = /\/id\/(\d{4,})/.exec(url);
            if (cdn) { keys.push('istock:' + cdn[1]); }
            var yt = this._youTubeId(url);
            if (yt) { keys.push('yt:' + yt); }
        }
        return keys.filter(function (k, i) { return keys.indexOf(k) === i; });
    }

    _youTubeId(url) {
        var pats = [
            /youtu\.be\/([A-Za-z0-9_-]{6,})/,
            /[?&]v=([A-Za-z0-9_-]{6,})/,
            /\/embed\/([A-Za-z0-9_-]{6,})/,
            /\/vi?\/([A-Za-z0-9_-]{6,})/
        ];
        for (var i = 0; i < pats.length; i++) {
            var m = pats[i].exec(url);
            if (m) { return m[1]; }
        }
        return null;
    }

    // ------------------------------------------------------------------
    // URLs referenced by a body block / by a comment row
    // ------------------------------------------------------------------

    /** URLs a block references — run hyperlinks plus any bare URLs in run text. */
    _blockUrls(block) {
        var urls = [];
        var add = function (u) { if (u && urls.indexOf(u) === -1) { urls.push(u); } };
        var scanRuns = function (runs) {
            if (!runs) { return; }
            for (var i = 0; i < runs.length; i++) {
                var r = runs[i];
                if (r && r.hyperlink) { add(r.hyperlink); }
                if (r && r.text) {
                    var found = r.text.match(/https?:\/\/[^\s\])]+/g);
                    if (found) { for (var f = 0; f < found.length; f++) { add(found[f]); } }
                }
            }
        };
        if (!block || !block.data) { return urls; }
        if (block.type === 'paragraph') {
            scanRuns(block.data.runs);
        } else if (block.type === 'table' && block.data.rows) {
            for (var r = 0; r < block.data.rows.length; r++) {
                var cells = block.data.rows[r].cells || [];
                for (var c = 0; c < cells.length; c++) {
                    var paras = cells[c].paragraphs || [];
                    for (var p = 0; p < paras.length; p++) { scanRuns(paras[p].runs); }
                }
            }
        }
        return urls;
    }

    _blockKeys(block, idMatch) {
        var keys = [];
        var urls = this._blockUrls(block);
        for (var i = 0; i < urls.length; i++) {
            var ks = this.mediaKeys(urls[i], idMatch);
            for (var k = 0; k < ks.length; k++) {
                if (keys.indexOf(ks[k]) === -1) { keys.push(ks[k]); }
            }
        }
        return keys;
    }

    _commentUrls(comment) {
        if (comment && comment.rowUrls && comment.rowUrls.length) { return comment.rowUrls.slice(); }
        if (comment && comment.rowUrl) { return [comment.rowUrl]; }
        return [];
    }

    _hasRowUrl(comment) {
        return !!(comment && (comment.rowUrl || (comment.rowUrls && comment.rowUrls.length)));
    }

    _renderable(block) {
        if (typeof CommentExtractor !== 'undefined' && CommentExtractor.isRenderableBlock) {
            return CommentExtractor.isRenderableBlock(block);
        }
        if (!block) { return false; }
        if (block.type === 'table') { return true; }
        if (block.type === 'paragraph') {
            return !!(block.data && block.data.text && block.data.text.trim() !== '');
        }
        return false;
    }

    // ------------------------------------------------------------------
    // The coordinator — annotate a Writer's Template result in place
    // ------------------------------------------------------------------

    /**
     * Capture comments into a parsed Writer's Template result: attach red notes
     * to `block.commentNotes` for body-anchored comments and for media-row
     * comments matched to the body element that uses the same media. Mutates
     * `wtResult.content` in place (additive) and returns a placement summary.
     *
     * @param {Object} wtResult - DocxParser result (content blocks carry .comments).
     * @param {Array<Object>} [externalMediaComments] - media-row comments parsed
     *        from a SEPARATE Media List .docx (each carries rowUrl/rowUrls).
     * @returns {{surfaced:number, body:number, media:number, unplacedMedia:Array}}
     */
    captureIntoTemplate(wtResult, externalMediaComments) {
        var summary = { surfaced: 0, body: 0, media: 0, unplacedMedia: [] };
        if (!this.filter || !wtResult || !Array.isArray(wtResult.content)) { return summary; }
        var content = wtResult.content;
        var idMatch = this._idMatch();

        // 1. Partition this document's comments into body vs. media-anchored.
        var bodyComments = [];
        var mediaComments = [];
        for (var i = 0; i < content.length; i++) {
            var block = content[i];
            var cs = block && block.comments;
            if (!cs || !cs.length) { continue; }
            for (var j = 0; j < cs.length; j++) {
                var c = cs[j];
                if (this._hasRowUrl(c)) {
                    mediaComments.push({ comment: c, anchorBlock: block });
                } else {
                    bodyComments.push({ comment: c, block: block });
                }
            }
        }
        // External Media List comments are always media-anchored (no WT anchor).
        if (Array.isArray(externalMediaComments)) {
            for (var e = 0; e < externalMediaComments.length; e++) {
                mediaComments.push({ comment: externalMediaComments[e], anchorBlock: null });
            }
        }

        // 2. Body placement — note attaches to its own (renderable) anchor block.
        for (var b = 0; b < bodyComments.length; b++) {
            var bc = bodyComments[b];
            var d = this.filter.decide(bc.comment.author, bc.comment.text);
            if (!d.surface) { continue; }
            this._attachNote(bc.block, d.author, bc.comment.text);
            summary.body++; summary.surfaced++;
        }

        // 3. Media match — key surviving media comments, scan body blocks.
        if (!this._mediaEnabled()) { return summary; }

        var keyMap = {};
        var surviving = [];
        for (var mi = 0; mi < mediaComments.length; mi++) {
            var mc = mediaComments[mi];
            var dd = this.filter.decide(mc.comment.author, mc.comment.text);
            if (!dd.surface) { continue; }
            mc._display = dd.author;
            mc._emitted = false;
            surviving.push(mc);
            var urls = this._commentUrls(mc.comment);
            for (var u = 0; u < urls.length; u++) {
                var ks = this.mediaKeys(urls[u], idMatch);
                for (var k = 0; k < ks.length; k++) {
                    (keyMap[ks[k]] = keyMap[ks[k]] || []).push(mc);
                }
            }
        }
        for (var ci = 0; ci < content.length; ci++) {
            var blk = content[ci];
            if (!this._renderable(blk)) { continue; }
            var bKeys = this._blockKeys(blk, idMatch);
            for (var bk = 0; bk < bKeys.length; bk++) {
                var entries = keyMap[bKeys[bk]];
                if (!entries) { continue; }
                for (var en = 0; en < entries.length; en++) {
                    var entry = entries[en];
                    if (entry._emitted || entry.anchorBlock === blk) { continue; }
                    this._attachNote(blk, entry._display, entry.comment.text);
                    entry._emitted = true; summary.media++; summary.surfaced++;
                }
            }
        }
        for (var s = 0; s < surviving.length; s++) {
            if (!surviving[s]._emitted) { summary.unplacedMedia.push(surviving[s].comment); }
        }
        return summary;
    }

    /**
     * Media-only fallback: a Media List was uploaded with no Writer's Template,
     * so media comments have no body element to attach to. Render the surviving
     * ones as red notes to append to the Media List .txt, with a toast message.
     *
     * @param {Array<Object>} mediaComments
     * @returns {{notes:string[], header:string, toast:string}}
     */
    renderMediaOnly(mediaComments) {
        var notes = [];
        if (this.filter && Array.isArray(mediaComments)) {
            for (var i = 0; i < mediaComments.length; i++) {
                var c = mediaComments[i];
                var d = this.filter.decide(c.author, c.text);
                if (d.surface) { notes.push(this.renderNote(d.author, c.text)); }
            }
        }
        return {
            notes: notes,
            header: '--- REVIEWER COMMENTS (no Writer’s Template uploaded — could not be placed in context) ---',
            toast: notes.length
                ? (notes.length + ' reviewer comment' + (notes.length === 1 ? '' : 's') +
                   ' could not be placed in context and were appended to the Media List output.')
                : ''
        };
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = CommentInserter;
}
