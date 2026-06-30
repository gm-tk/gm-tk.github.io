'use strict';

/**
 * PageStitcher — recombines a SPLIT module (a base homepage + per-section files)
 * back into ONE single-page module HTML, identical to how single-page modules
 * are normally built (e.g. BLL210: all lessons in one #body, delimited by their
 * own <!-- N --> comments).
 *
 * It is used when the downstream HTML Convertor ran in SPLIT MODE — emitting a
 * long single-page module in pieces so each generation stayed within length
 * limits. See SPLIT_MODE_AND_STITCH_CONTRACT.md for the authoritative contract.
 *
 * The INSERTION CONTRACT is explicit (never positional guesswork, spec §8.1):
 *   - The base homepage's #body contains ordered splice markers, one per slot:
 *         <!-- PAGEFORGE-SPLICE id="01" -->
 *   - Each section file carries its id + content between section markers:
 *         <!-- PAGEFORGE-SECTION id="01" -->  …raw #body chunk…  <!-- /PAGEFORGE-SECTION -->
 *   - The stitcher replaces each splice marker with its matching section's
 *     content, preserving document order and the surrounding scaffold untouched.
 *   - Manual-stitch GUIDE blocks the Convertor adds for hand-assembly
 *     (<!-- PAGEFORGE-GUIDE-START --> … <!-- PAGEFORGE-GUIDE-END -->) are stripped,
 *     so the unified output carries none of those developer instructions.
 *
 * Pure, string/regex based (no DOM) → headless-testable; the upload/file-read
 * adapter lives in the Page Stitcher mode controller.
 */
class PageStitcher {
    /** @param {Object} [options] @param {Object} [options.config] marker tags. */
    constructor(options) {
        options = options || {};
        this.config = options.config || PageStitcher.DEFAULTS;
    }

    // ------------------------------------------------------------------
    // Public: stitch over uploaded section files (array of {name, html})
    // ------------------------------------------------------------------

    /**
     * @param {string} baseHtml - the base homepage (with splice markers).
     * @param {Array<{name:string, html:string}>} sections - the section files.
     * @returns {{ok:boolean, html:?string, errors:string[], placements:Array}}
     */
    stitch(baseHtml, sections) {
        var self = this;
        var map = {};
        var errors = [];
        (sections || []).forEach(function (s) {
            var p = self.parseSection(s && s.name, s && s.html);
            if (!p || !p.id) {
                errors.push('Could not identify a section id for "' + ((s && s.name) || 'an uploaded file') +
                    '" (no PAGEFORGE-SECTION marker and no __part-NN / -NN filename).');
                return;
            }
            if (map[p.id] !== undefined) {
                errors.push('Duplicate section id "' + p.id + '" (two uploaded files claim the same slot).');
                return;
            }
            map[p.id] = p.content;
        });
        return this.stitchCore(baseHtml, map, errors);
    }

    // ------------------------------------------------------------------
    // Pure core: stitch over an id → content map
    // ------------------------------------------------------------------

    /**
     * @param {string} baseHtml
     * @param {Object<string,string>} sectionMap - id → section content.
     * @param {string[]} [priorErrors]
     * @returns {{ok:boolean, html:?string, errors:string[], placements:Array}}
     */
    stitchCore(baseHtml, sectionMap, priorErrors) {
        var errors = (priorErrors || []).slice();
        sectionMap = sectionMap || {};

        // Strip manual-stitch GUIDE blocks from the base BEFORE locating markers, so
        // guidance that quotes a splice marker can't be mistaken for a real slot.
        baseHtml = this._stripGuides(baseHtml);

        var markers = this.findSpliceMarkers(baseHtml);
        if (!markers.length) {
            errors.push('No PAGEFORGE-SPLICE markers found in the base homepage — is this a SPLIT-MODE base?');
        }

        var seen = {};
        markers.forEach(function (m) {
            if (seen[m.id]) { errors.push('Duplicate splice slot "' + m.id + '" in the base homepage.'); }
            seen[m.id] = true;
        });
        var baseIds = markers.map(function (m) { return m.id; });

        // Every slot must have a section; every section must match a slot.
        markers.forEach(function (m) {
            if (sectionMap[m.id] === undefined) {
                errors.push('Missing section for slot "' + m.id + '" (no uploaded file fills it).');
            }
        });
        Object.keys(sectionMap).forEach(function (id) {
            if (baseIds.indexOf(id) === -1) {
                errors.push('Extra section "' + id + '" has no matching slot in the base homepage.');
            }
        });

        if (errors.length) {
            return { ok: false, html: null, errors: errors, placements: [] };
        }

        var spliceRe = this._spliceRe();
        var html = baseHtml.replace(spliceRe, function (full, id) {
            return sectionMap[id] !== undefined ? sectionMap[id] : full;
        });
        // Strip any GUIDE blocks carried in from the section content too, so the
        // unified output contains none of the manual-stitch instructions.
        html = this._stripGuides(html);
        var placements = markers.map(function (m) { return { id: m.id, filled: true }; });
        return { ok: true, html: html, errors: [], placements: placements };
    }

    // ------------------------------------------------------------------
    // Parsing helpers
    // ------------------------------------------------------------------

    /** Ordered list of splice markers in the base: [{id, raw, index}]. */
    findSpliceMarkers(baseHtml) {
        var re = this._spliceRe();
        var out = [], m;
        while ((m = re.exec(String(baseHtml || ''))) !== null) {
            out.push({ id: m[1], raw: m[0], index: m.index });
        }
        return out;
    }

    /**
     * Identify a section file's id + content. Precedence:
     *   1. explicit <!-- PAGEFORGE-SECTION id="X" --> … <!-- /PAGEFORGE-SECTION -->
     *   2. a full page → the inner HTML of its #body
     *   3. the whole file (a bare fragment) — id from the filename
     * @returns {{id:?string, content:string, source:string}}
     */
    parseSection(name, html) {
        html = String(html == null ? '' : html);
        var cfg = this.config;

        var startRe = new RegExp('<!--\\s*' + cfg.sectionTag + '\\s+id=["\']?([\\w.\\-]+)["\']?\\s*-->', 'i');
        var sm = startRe.exec(html);
        if (sm) {
            var rest = html.slice(sm.index + sm[0].length);
            var endRe = new RegExp('<!--\\s*/' + cfg.sectionTag + '\\s*-->', 'i');
            var em = endRe.exec(rest);
            var content = em ? rest.slice(0, em.index) : rest;
            return { id: String(sm[1]).toLowerCase(), content: this._trim(content), source: 'marker' };
        }

        var bodyInner = this._extractBodyInner(html);
        if (bodyInner !== null) {
            return { id: this._idFromName(name), content: this._trim(bodyInner), source: 'body' };
        }
        return { id: this._idFromName(name), content: this._trim(html), source: 'whole' };
    }

    /** Section id from a filename: -lesson-NN / -section-NN / __part-NN / trailing -NN. */
    _idFromName(name) {
        var base = String(name || '').replace(/^.*[\\/]/, '').replace(/\.html?$/i, '');
        var m = /(?:__part-|__section-|-lesson-|-section-)([\w.]+)$/i.exec(base) || /-(\d{1,3})$/.exec(base);
        return m ? String(m[1]).toLowerCase() : null;
    }

    /** Inner HTML of the first <div id="body"> … </div> (balanced), or null. */
    _extractBodyInner(html) {
        var m = /<div\b[^>]*\bid="body"[^>]*>/i.exec(html);
        if (!m) { return null; }
        var start = m.index + m[0].length;
        var tagRe = /<div\b|<\/div>/ig;
        tagRe.lastIndex = m.index;
        var depth = 0, mm, end = -1;
        while ((mm = tagRe.exec(html)) !== null) {
            if (mm[0] === '</div>') { depth--; if (depth === 0) { end = mm.index; break; } }
            else { depth++; }
        }
        return end > start ? html.slice(start, end) : html.slice(start);
    }

    _trim(s) {
        return String(s).replace(/^[ \t]*\r?\n/, '').replace(/\s+$/, '');
    }

    _spliceRe() {
        return new RegExp('<!--\\s*' + this.config.spliceTag + '\\s+id=["\']?([\\w.\\-]+)["\']?\\s*-->', 'ig');
    }

    /**
     * Remove the manual-stitch GUIDE blocks the Convertor adds for developers who
     * hand-assemble the split files: everything from <!-- PAGEFORGE-GUIDE-START -->
     * to <!-- PAGEFORGE-GUIDE-END --> (inclusive, plus a trailing blank line), so
     * the automated stitch carries none of the manual instructions. Anchored on the
     * unique END sentinel (non-greedy) → safe even when the guidance text quotes
     * markers that themselves contain "-->".
     */
    _stripGuides(html) {
        var cfg = this.config;
        if (!cfg.guideStartTag || !cfg.guideEndTag) { return String(html == null ? '' : html); }
        var re = new RegExp(
            '[ \\t]*<!--\\s*' + cfg.guideStartTag + '\\s*-->[\\s\\S]*?<!--\\s*' + cfg.guideEndTag + '\\s*-->[ \\t]*(?:\\r?\\n)?',
            'ig');
        return String(html == null ? '' : html).replace(re, '');
    }

    // ------------------------------------------------------------------
    // Convenience for the adapter
    // ------------------------------------------------------------------

    /** Derive the module code from a base homepage (#module-code, <title>, filename). */
    moduleCode(baseHtml, baseName) {
        var mc = /<div\b[^>]*\bid="module-code"[^>]*>\s*<h1[^>]*>([^<]+)<\/h1>/i.exec(String(baseHtml || ''));
        if (mc && mc[1].trim()) { return mc[1].trim(); }
        var t = /<title[^>]*>([^<]+)<\/title>/i.exec(String(baseHtml || ''));
        if (t && t[1].trim()) { return t[1].trim().split(/\s+/)[0]; }
        var fn = /([A-Za-z]{2,}\d{2,}[A-Za-z]?)/.exec(String(baseName || ''));
        return fn ? fn[1].toUpperCase() : 'MODULE';
    }

    /** A short human-readable placement summary for the toast / on-screen note. */
    summary(result) {
        if (!result) { return ''; }
        if (!result.ok) { return 'Stitch failed: ' + result.errors.join(' '); }
        return 'Stitched ' + result.placements.length + ' section' +
            (result.placements.length === 1 ? '' : 's') + ' into one unified page.';
    }
}

PageStitcher.DEFAULTS = {
    spliceTag: 'PAGEFORGE-SPLICE',
    sectionTag: 'PAGEFORGE-SECTION',
    guideStartTag: 'PAGEFORGE-GUIDE-START',
    guideEndTag: 'PAGEFORGE-GUIDE-END'
};


/**
 * PageStitcherMode — the thin DOM/upload adapter for the Page Stitcher front
 * page (#stitch-section): a base-homepage upload, a multi-file section upload, a
 * Stitch action, the unified-HTML download (via OutputManager) and a placement
 * summary. State + the stitch orchestration are pure (dependencies injected) so
 * the Node runner exercises them; every DOM touch no-ops when an element is
 * absent. Mirrors the carried-over ModeToggle adapter conventions.
 */
class PageStitcherMode {
    constructor(options) {
        options = options || {};
        this._document = options.document || null;
        this._stitcher = options.stitcher || null;
        this._outputManager = options.outputManager || null;
        this._notify = options.notify || null;

        /** @type {Array} all staged files — base + sections together (one container) */
        this.files = [];
        this.els = {};

        if (this._document && options.autoInit !== false) { this.init(); }
    }

    // ------------------------------------------------------------------
    // State (pure)
    // ------------------------------------------------------------------

    /** Record (or clear) every staged file (base + sections in one container). */
    setFiles(files) {
        var a = [];
        if (files && files.length) { for (var i = 0; i < files.length; i++) { a.push(files[i]); } }
        this.files = a;
        this._renderFiles();
        this._syncStitch();
        return this.files.length;
    }
    hasFiles() { return Array.isArray(this.files) && this.files.length > 0; }
    /** Stitch is enabled with at least two files (a base homepage + ≥1 section). */
    canStitch() { return this.files.length >= 2; }

    // ------------------------------------------------------------------
    // Stitch orchestration (core — operates on already-read {name,html})
    // ------------------------------------------------------------------

    /**
     * Classify the read files into the base homepage vs section files, then
     * stitch. The base is the file carrying PAGEFORGE-SPLICE markers (or named
     * <CODE>-base.html); everything else is a section.
     * @param {Array<{name:string,html:string}>} readFiles
     * @returns {{result:Object, filename:?string}}
     */
    stitchReadFiles(readFiles) {
        var stitcher = this._getStitcher();
        if (!stitcher) {
            return this._fail(['Stitcher unavailable.'], 'Stitch failed — stitcher unavailable.');
        }
        var c = this._classifyFiles(readFiles, stitcher);
        if (!c.base) {
            return this._fail(
                ['No base homepage found — include the base file (it carries PAGEFORGE-SPLICE markers, or is named <CODE>-base.html).'],
                'Stitch failed — no base homepage in the upload.');
        }
        if (c.extraBases.length) {
            return this._fail(['More than one base homepage uploaded — include exactly one.'],
                'Stitch failed — more than one base homepage.');
        }

        var result = stitcher.stitch(c.base.html, c.sections);
        var filename = null;
        if (result.ok) {
            filename = stitcher.moduleCode(c.base.html, c.base.name) + '.html';
            var om = this._getOutputManager();
            if (om) {
                om.addFile({ filename: filename, content: result.html, type: 'html' });
                try { om.downloadFile(filename); } catch (e) { /* headless / no DOM */ }
            }
        } else {
            this._toast('Stitch failed — see the summary.');
        }
        this._renderSummary(result, filename);
        return { result: result, filename: filename };
    }

    /** Split the read files into {base, extraBases, sections} by marker/filename. */
    _classifyFiles(readFiles, stitcher) {
        var tag = (stitcher && stitcher.config && stitcher.config.spliceTag) || 'PAGEFORGE-SPLICE';
        // Match a REAL splice marker (<!-- PAGEFORGE-SPLICE id=…), not a bare mention
        // of the word: every section file carries a manual-stitch GUIDE block that
        // quotes the marker in its human instructions, so a bare-substring test
        // misclassifies every section as a base (→ ">1 base" error). Strip GUIDE
        // blocks first — exactly as stitchCore does before locating markers — then
        // look for a genuine marker. The <CODE>-base.html filename fallback is kept.
        var markerRe = new RegExp('<!--\\s*' + tag + '\\s+id=', 'i');
        var bases = [], sections = [];
        (readFiles || []).forEach(function (f) {
            if (!f) { return; }
            var cleaned = (stitcher && typeof stitcher._stripGuides === 'function')
                ? stitcher._stripGuides(f.html || '') : (f.html || '');
            var isBase = markerRe.test(cleaned) ||
                /(^|[\\/])[^\\/]*-base\.html?$/i.test(f.name || '');
            if (isBase) { bases.push(f); } else { sections.push(f); }
        });
        return { base: bases[0] || null, extraBases: bases.slice(1), sections: sections };
    }

    _fail(errors, toast) {
        var result = { ok: false, errors: errors, placements: [] };
        this._toast(toast);
        this._renderSummary(result, null);
        return { result: result, filename: null };
    }

    /** Read the staged files then stitch. Returns a Promise in the browser. */
    stitchNow() {
        var self = this;
        if (!this.canStitch()) {
            this._toast('Add the base homepage and its section files (at least two files) first.');
            return null;
        }
        var reads = this.files.map(function (f) { return self._read(f); });
        return this._resolveAll(reads, function (arr) {
            return self.stitchReadFiles(arr.filter(Boolean));
        });
    }

    _read(file) {
        if (!file) { return null; }
        if (typeof file.html === 'string') { return { name: file.name || 'file.html', html: file.html }; }
        if (typeof file.text === 'function') {
            return file.text().then(function (t) { return { name: file.name || 'file.html', html: t }; });
        }
        return null;
    }
    _resolveAll(arr, fn) {
        var any = arr.some(function (v) { return v && typeof v.then === 'function'; });
        if (!any) { return fn(arr); }
        return Promise.all(arr.map(function (v) { return Promise.resolve(v); })).then(fn);
    }
    _getStitcher() {
        if (!this._stitcher && typeof PageStitcher !== 'undefined') { this._stitcher = new PageStitcher(); }
        return this._stitcher;
    }
    _getOutputManager() {
        if (!this._outputManager && typeof OutputManager !== 'undefined') { this._outputManager = new OutputManager(); }
        return this._outputManager;
    }
    _toast(msg) {
        if (typeof this._notify === 'function') { this._notify(msg); return; }
        if (typeof window !== 'undefined' && window.pageForgeToast && window.pageForgeToast.show) {
            window.pageForgeToast.show(msg);
        }
    }

    // ------------------------------------------------------------------
    // DOM adapter (no-ops when unbound / an element is absent)
    // ------------------------------------------------------------------

    init() {
        if (!this._document) { return; }
        var doc = this._document, self = this;
        function get(id) { return doc.getElementById ? doc.getElementById(id) : null; }
        this.els = {
            input: get('stitch-input'), drop: get('stitch-drop'),
            info: get('stitch-info'), name: get('stitch-name'),
            stitchBtn: get('btn-stitch'), summary: get('stitch-summary')
        };
        this._bindFile(this.els.input, this.els.drop, function (files) { self.setFiles(files); });
        if (this.els.stitchBtn && this.els.stitchBtn.addEventListener) {
            this.els.stitchBtn.addEventListener('click', function () { self.stitchNow(); });
        }
        this._syncStitch();
    }
    _bindFile(input, drop, onFiles) {
        if (input && input.addEventListener) {
            input.addEventListener('change', function () { onFiles(input.files); });
        }
        if (drop && drop.addEventListener) {
            drop.addEventListener('click', function () { if (input && input.click) { input.click(); } });
            drop.addEventListener('keydown', function (e) {
                if (e && (e.key === 'Enter' || e.key === ' ')) { if (e.preventDefault) { e.preventDefault(); } if (input && input.click) { input.click(); } }
            });
            drop.addEventListener('dragover', function (e) { if (e && e.preventDefault) { e.preventDefault(); } if (drop.classList) { drop.classList.add('drag-over'); } });
            drop.addEventListener('dragleave', function () { if (drop.classList) { drop.classList.remove('drag-over'); } });
            drop.addEventListener('drop', function (e) {
                if (e && e.preventDefault) { e.preventDefault(); }
                if (drop.classList) { drop.classList.remove('drag-over'); }
                var files = e && e.dataTransfer && e.dataTransfer.files;
                if (files && files.length) { onFiles(files); }
            });
        }
    }
    _renderFiles() {
        if (this.els.name) {
            this.els.name.textContent = this.hasFiles()
                ? (this.files.length + ' file' + (this.files.length === 1 ? '' : 's') + ' selected') : '';
        }
        this._setHidden(this.els.info, !this.hasFiles());
    }
    _syncStitch() { if (this.els.stitchBtn) { this.els.stitchBtn.disabled = !this.canStitch(); } }
    _renderSummary(result, filename) {
        var el = this.els.summary;
        if (!el) { return; }
        var esc = function (s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); };
        if (result && result.ok) {
            el.innerHTML = '<p class="stitch-ok">✓ Stitched ' + result.placements.length + ' section' +
                (result.placements.length === 1 ? '' : 's') + ' into <code>' + esc(filename) + '</code> (downloaded).</p>';
        } else {
            var items = (result && result.errors || []).map(function (e) { return '<li>' + esc(e) + '</li>'; }).join('');
            el.innerHTML = '<p class="stitch-error">Could not stitch — nothing was downloaded:</p><ul class="stitch-errors">' + items + '</ul>';
        }
        this._setHidden(el, false);
    }
    _setHidden(el, hidden) {
        if (el && el.classList) { if (hidden) { el.classList.add('hidden'); } else { el.classList.remove('hidden'); } }
    }
}

// Browser bootstrap — skipped under the DOM-less Node test runner.
if (typeof document !== 'undefined' && document.addEventListener) {
    document.addEventListener('DOMContentLoaded', function () {
        var mode = new PageStitcherMode({ document: document });
        if (typeof window !== 'undefined') { window.pageForgeStitcherMode = mode; }
    });
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = PageStitcher;
}
