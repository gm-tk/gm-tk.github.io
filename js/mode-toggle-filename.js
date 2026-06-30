'use strict';

/**
 * ModeToggleFilename — pure, DOM-free helpers for the Module Development mode
 * standardised download filename convention.
 *
 * Module Development conversion names each downloadable .txt as
 *   `<MODULE_CODE> <label>_parsed.txt`
 * where <label> is "Writers Template" or "Media List". The module code is
 * detected by SHAPE — an alphabetic cluster immediately followed by a numeric
 * cluster (e.g. OSAI501, CEDO501) — found anywhere in the source .docx filename
 * (even glued to other text by underscores/hyphens, e.g. "Copy_CEDO501_WT" →
 * "CEDO501"), preferring a code the parser read from the document itself. Every
 * other part of the original filename is discarded.
 *
 * Extracted from js/mode-toggle.js (ModeToggle._deriveFilename) to keep the
 * host module under its 500-line ceiling, following the extraction pattern in
 * docs/26–docs/30. ModeToggle delegates to this via a thin shim. Exposed as a
 * global class with static methods so it persists across the headless test
 * runner's per-file vm scope and is reachable as the browser-global fallback.
 *
 * See docs/31-module-development-mode.md.
 */

class ModeToggleFilename {
    /**
     * Resolve the module code for a download filename. Resolution order:
     *   1. a code the parser read from the document itself
     *      (result.metadata.moduleCode), when code-shaped — most reliable;
     *   2. else the FIRST code-shaped run found ANYWHERE in the source filename —
     *      letters immediately followed by digits, regardless of separators such
     *      as spaces, underscores or hyphens, so "Copy_CEDO501_WT" → "CEDO501";
     *   3. else the leading whitespace token; else 'Module'.
     * Code matches (1 and 2) are upper-cased to the house convention; the
     * leading-token fallback keeps its original casing.
     *
     * @param {string} stem - filename with the .docx extension stripped + trimmed.
     * @param {string} [preferredCode] - a code already extracted from the document.
     * @returns {string} The resolved module code.
     */
    static deriveModuleCode(stem, preferredCode) {
        var pref = String(preferredCode == null ? '' : preferredCode).match(ModeToggleFilename.CODE_SUBSTRING);
        if (pref) { return pref[0].toUpperCase(); }
        var s = String(stem || '');
        var m = s.match(ModeToggleFilename.CODE_SUBSTRING);
        if (m) { return m[0].toUpperCase(); }
        var tokens = s.split(/\s+/).filter(Boolean);
        return tokens.length ? tokens[0] : 'Module';
    }

    /**
     * Build the standardised `<MODULE_CODE> <label>_parsed.txt` filename. The
     * module code is taken from the document (result.metadata.moduleCode) when
     * available, else detected anywhere in the source filename — every OTHER part
     * of the original filename is discarded.
     *
     * @param {{name?: string}} file - the uploaded source .docx descriptor.
     * @param {string} label - "Writers Template" or "Media List".
     * @param {Object} [result] - the DocxParser parse result (supplies metadata.moduleCode).
     * @returns {string} The standardised download filename.
     */
    static deriveFilename(file, label, result) {
        var stem = ((file && file.name) ? String(file.name) : '').replace(/\.docx$/i, '').trim();
        var preferred = (result && result.metadata) ? result.metadata.moduleCode : null;
        var code = ModeToggleFilename.deriveModuleCode(stem, preferred);
        return code + ' ' + label + '_parsed.txt';
    }
}

/**
 * Module-code shape: an alphabetic cluster (2–6) immediately followed by a
 * numeric cluster (2–4), matching the established codes (OSAI501, CEDO501,
 * BLL210, XLP03, HPFUN201, AGH1008 …). Used as a SUBSTRING search so a code is
 * found wherever it sits in a filename, even glued to other text by underscores
 * or hyphens. Case-insensitive; matches are upper-cased by deriveModuleCode.
 */
ModeToggleFilename.CODE_SUBSTRING = /[A-Za-z]{2,6}\d{2,4}/;
