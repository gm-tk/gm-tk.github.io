'use strict';

/**
 * CommentFilter — the whitelist + actionable-vs-boilerplate decision for native
 * Word comments. Pure and data-driven: all authors, normalisation switches and
 * filter regexes come from data/comment-authors.json (injected), so the policy
 * is editable without code changes. No DOM, no I/O — headless-testable.
 *
 * Ported from CONVERTER_V2 (ContentConverter #commentAuthorDisplay /
 * #commentIsOmittable). See Comment_Capture_Process_Explained.md §3–§4.
 */
class CommentFilter {
    /**
     * @param {Object} [data] - parsed data/comment-authors.json. When absent the
     *        filter resolves no authors and surfaces nothing (safe no-op), which
     *        is what keeps comment capture inert until the data file is loaded.
     */
    constructor(data) {
        this.data = data || null;
        this._omitRe = undefined;   // lazily compiled
        this._keepRe = undefined;
    }

    /** @returns {boolean} Master switch — capture is enabled and data present. */
    isEnabled() {
        return !!(this.data && this.data.enabled !== false && Array.isArray(this.data.authors));
    }

    /**
     * Normalise an author name for comparison per the `match` config:
     * strip a trailing ` [N]` disambiguator, lowercase, treat `.`/`_` as a space,
     * collapse whitespace.
     *
     * @param {string} name
     * @returns {string}
     */
    normalizeAuthor(name) {
        var m = (this.data && this.data.match) || {};
        var s = String(name == null ? '' : name);
        if (m.strip_disambiguator !== false) {
            s = s.replace(/\s*\[\d+\]\s*$/, '');
        }
        if (m.case_insensitive !== false) {
            s = s.toLowerCase();
        }
        if (m.dot_space_equivalent !== false) {
            s = s.replace(/[._]/g, ' ');
        }
        return s.replace(/\s+/g, ' ').trim();
    }

    /** Reverse a two-token "first last" / "last first" name, else return as-is. */
    _reverseName(normalized) {
        var parts = normalized.split(' ');
        if (parts.length === 2) {
            return parts[1] + ' ' + parts[0];
        }
        return normalized;
    }

    /**
     * Resolve a raw `w:author` to the canonical display name to print, or null
     * if the author isn't whitelisted / enabled (→ the comment is dropped).
     *
     * @param {string} rawAuthor
     * @returns {?string}
     */
    resolveAuthor(rawAuthor) {
        if (!this.isEnabled()) { return null; }
        var match = (this.data && this.data.match) || {};
        var acceptReversed = match.accept_reversed_order !== false;
        var n = this.normalizeAuthor(rawAuthor);
        if (!n) { return null; }
        var nReversed = acceptReversed ? this._reverseName(n) : null;

        for (var i = 0; i < this.data.authors.length; i++) {
            var a = this.data.authors[i];
            if (!a || a.enabled === false) { continue; }

            // Candidate normalised forms: the display name + any seen_as variants.
            var candidates = [a.display];
            if (Array.isArray(a.seen_as)) { candidates = candidates.concat(a.seen_as); }

            for (var c = 0; c < candidates.length; c++) {
                var cand = this.normalizeAuthor(candidates[c]);
                if (!cand) { continue; }
                if (n === cand) { return a.display; }
                if (acceptReversed && (nReversed === cand || this._reverseName(cand) === n)) {
                    return a.display;
                }
            }
        }
        return null;
    }

    // ------------------------------------------------------------------
    // Actionable vs. boilerplate (the asymmetric content filter)
    // ------------------------------------------------------------------

    _omit() {
        if (this._omitRe === undefined) {
            var cf = (this.data && this.data.content_filter) || {};
            this._omitRe = cf.omit_boilerplate ? new RegExp(cf.omit_boilerplate, 'i') : null;
        }
        return this._omitRe;
    }

    _keep() {
        if (this._keepRe === undefined) {
            var cf = (this.data && this.data.content_filter) || {};
            this._keepRe = cf.action_keep ? new RegExp(cf.action_keep, 'i') : null;
        }
        return this._keepRe;
    }

    /**
     * A comment is OMITTABLE iff it matches the boilerplate family AND carries no
     * action signal — `omit.test(text) && !(keep && keep.test(text))`. So a note
     * mixing both ("Replace with iStock. Used with permission.") is kept.
     * When the content filter is disabled, nothing is omittable (surface all).
     *
     * @param {string} text
     * @returns {boolean}
     */
    isOmittable(text) {
        var cf = (this.data && this.data.content_filter) || {};
        if (cf.enabled === false) { return false; }
        var omit = this._omit();
        if (!omit) { return false; }
        var t = String(text == null ? '' : text);
        var keep = this._keep();
        return omit.test(t) && !(keep && keep.test(t));
    }

    /**
     * Combined decision for one comment.
     *
     * @param {string} rawAuthor
     * @param {string} text
     * @returns {{ surface: boolean, author: ?string }}
     *          `surface` is true only when the author is whitelisted AND the text
     *          is actionable; `author` is the canonical display name (or null).
     */
    decide(rawAuthor, text) {
        var author = this.resolveAuthor(rawAuthor);
        if (!author) { return { surface: false, author: null }; }
        if (this.isOmittable(text)) { return { surface: false, author: author }; }
        return { surface: true, author: author };
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = CommentFilter;
}
