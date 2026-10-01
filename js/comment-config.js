'use strict';

/**
 * comment-config.js — browser bootstrap that loads the comment-capture data.
 *
 * Publishes the whitelist/filter config to `window.PageForgeCommentAuthors`, which
 * ModeToggle reads when it lazily builds the CommentInserter. Mirrors V1's
 * TemplateEngine pattern: fetch the canonical, editable data/comment-authors.json
 * and, if the fetch can't run (e.g. file://), fall back to the embedded copy so
 * the feature still works. Editing data/comment-authors.json takes effect (fetch
 * wins); keep the embedded FALLBACK below in sync with it.
 *
 * Browser-only: a clean no-op under the DOM-less Node test runner (which injects
 * data directly into the modules instead).
 */
(function () {
    if (typeof window === 'undefined') { return; }

    // Embedded fallback — keep in sync with data/comment-authors.json (canonical).
    var FALLBACK = {
        enabled: true,
        render: { prefix: "Note from {author}: {text}" },
        content_filter: {
            enabled: true,
            omit_boilerplate: "(used\\s+(with|by|under)\\b|with permission\\b|used in online learning|public domain|creative commons|crown copyright|copyright act|all rights reserved|cc0\\b|©|\\bte kura (created|produced|made|owned)|links?\\s+only\\b|extract only|okay to use|\\ball (istock|you ?tube|shutterstock)\\b|licen[cs]e\\.?\\s*$|^link$|^links?\\b)",
            action_keep: "(\\bplease\\b|\\breplace\\b|\\brecreate\\b|\\bre-create\\b|\\bembed\\b|\\binsert\\b|\\bremove\\b|\\bcrop\\b|\\bresize\\b|\\bswap\\b|\\bdelete\\b|\\boverlay\\b|\\bjumble\\b|\\bsource\\b|can you\\b|can we\\b|could you\\b|could we\\b|designer to\\b|we (cannot|can'?t|are unable|need)\\b|\\?\\s*$)"
        },
        media_match: { enabled: true, id_match: true },
        match: {
            case_insensitive: true,
            dot_space_equivalent: true,
            strip_disambiguator: true,
            accept_reversed_order: true
        },
        authors: [
            { display: "Kate Scanlon",      enabled: true, seen_as: ["Kate.Scanlon"] },
            { display: "Nadia Stanton",     enabled: true, seen_as: ["Nadia Stanton"] },
            { display: "Caroline Schwer",   enabled: true, seen_as: ["caroline schwer"] },
            { display: "Simon Vita",        enabled: true, seen_as: ["simon vita"] },
            { display: "Amanda Griffiths",  enabled: true, seen_as: ["amanda griffiths"] },
            { display: "Creative Services", enabled: true, seen_as: ["Creative Services"] }
        ]
    };

    // Available synchronously from load (so a conversion right away still works).
    if (!window.PageForgeCommentAuthors) {
        window.PageForgeCommentAuthors = FALLBACK;
    }

    // Upgrade to the canonical file when fetch is available.
    if (typeof fetch === 'function') {
        fetch('data/comment-authors.json')
            .then(function (r) { return r.ok ? r.json() : null; })
            .then(function (data) { if (data) { window.PageForgeCommentAuthors = data; } })
            .catch(function () { /* keep the embedded fallback */ });
    }
})();
