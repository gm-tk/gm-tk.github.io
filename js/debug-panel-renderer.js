/**
 * DebugPanelRenderer — renders PageForge's collapsible debug panel.
 *
 * Extracted from js/app.js in Session 2 of the app refactor.
 * Consumes a snapshot of App state plus four constructor-injected
 * dependencies. Emits HTML into the provided DOM nodes.
 */

'use strict';

class DebugPanelRenderer {
    /**
     * @param {Object} deps
     * @param {HTMLElement} deps.debugPanel - The `#debug-panel` root element.
     * @param {HTMLElement} deps.debugContent - The inner container that receives `innerHTML`.
     * @param {OutputManager} deps.outputManager - Needed for `getHtmlFileCount()` etc.
     * @param {TemplateEngine} deps.templateEngine - Needed for `getConfig()` / `generateSkeleton()`.
     */
    constructor(deps) {
        this._debugPanel = deps.debugPanel;
        this._debugContent = deps.debugContent;
        this._outputManager = deps.outputManager;
        this._templateEngine = deps.templateEngine;

        this._currentAnalysis = null;
        this._currentMetadata = null;
        this._collectedInteractives = null;
        this._interactiveReferenceDoc = '';
        this._selectedTemplateId = null;
    }

    /**
     * Render the debug panel from a snapshot of App state.
     *
     * @param {Object} snapshot
     * @param {Object} snapshot.analysis - `App.currentAnalysis`
     * @param {Object} snapshot.metadata - `App.currentMetadata`
     * @param {Array}  snapshot.collectedInteractives - `App.collectedInteractives`
     * @param {string} snapshot.interactiveReferenceDoc - `App.interactiveReferenceDoc`
     * @param {string} snapshot.selectedTemplateId - `App.selectedTemplateId`
     */
    render(snapshot) {
        this._currentAnalysis = snapshot.analysis;
        this._currentMetadata = snapshot.metadata;
        this._collectedInteractives = snapshot.collectedInteractives;
        this._interactiveReferenceDoc = snapshot.interactiveReferenceDoc;
        this._selectedTemplateId = snapshot.selectedTemplateId;
        this._renderDebugPanel(snapshot.analysis);
    }
    // ------------------------------------------------------------------
    // Debug Panel rendering
    // ------------------------------------------------------------------

    /**
     * Render the debug panel with conversion summary, tag normalisation,
     * and page boundary results.
     *
     * @param {Object} analysis - Analysis results from _runAnalysis
     */
    _renderDebugPanel(analysis) {
        if (!this._debugPanel || !this._debugContent) return;

        var html = '';

        // --- Conversion Summary (moved from main results area) ---
        html += this._renderDebugConversionSummary();

        // --- Template Configuration Results ---
        html += this._renderDebugTemplateSection(analysis);

        // --- Tag Normalisation Results ---
        html += '<div class="debug-section">';
        html += '<h4 class="debug-section-title">Tag Normalisation Results</h4>';

        // Summary stats
        html += '<div class="debug-stats">';
        html += '<span class="debug-stat">Total tags: <b>' + analysis.totalTags + '</b></span>';
        html += '<span class="debug-stat">Unrecognised: <b>' + analysis.unrecognisedTags.length + '</b></span>';
        html += '<span class="debug-stat">Red text instructions: <b>' + analysis.redTextInstructions.length + '</b></span>';
        html += '<span class="debug-stat">Red-text-only blocks: <b>' + analysis.redTextOnlyCount + '</b></span>';
        html += '<span class="debug-stat">Whitespace-only blocks: <b>' + analysis.whitespaceOnlyCount + '</b></span>';
        html += '</div>';

        // Category breakdown
        var categories = analysis.tagsByCategory;
        var catKeys = Object.keys(categories);
        if (catKeys.length > 0) {
            html += '<div class="debug-categories">';
            html += '<span class="debug-label">By category:</span> ';
            for (var ci = 0; ci < catKeys.length; ci++) {
                html += '<span class="debug-category-badge">' +
                    this._esc(catKeys[ci]) + ': ' + categories[catKeys[ci]] + '</span>';
            }
            html += '</div>';
        }

        // Tag list
        if (analysis.tags.length > 0) {
            html += '<details class="debug-details">';
            html += '<summary>All tags (' + analysis.tags.length + ')</summary>';
            html += '<table class="debug-table"><thead><tr>' +
                '<th>Block</th><th>Raw</th><th>Normalised</th><th>Category</th><th>Details</th>' +
                '</tr></thead><tbody>';
            for (var i = 0; i < analysis.tags.length; i++) {
                var tag = analysis.tags[i];
                var details = '';
                if (tag.level) details += 'level=' + tag.level + ' ';
                if (tag.number) details += 'number=' + tag.number + ' ';
                if (tag.id) details += 'id=' + tag.id + ' ';
                if (tag.modifier) details += 'modifier=' + tag.modifier;
                details = details.trim();

                var rowClass = tag.normalised ? '' : ' class="debug-unrecognised"';
                html += '<tr' + rowClass + '>' +
                    '<td>' + tag.blockIndex + '</td>' +
                    '<td><code>' + this._esc(tag.raw) + '</code></td>' +
                    '<td>' + (tag.normalised ? this._esc(tag.normalised) : '<em>unrecognised</em>') + '</td>' +
                    '<td>' + (tag.category || '-') + '</td>' +
                    '<td>' + (details || '-') + '</td>' +
                    '</tr>';
            }
            html += '</tbody></table>';
            html += '</details>';
        }

        // Unrecognised tags
        if (analysis.unrecognisedTags.length > 0) {
            html += '<details class="debug-details debug-warning">';
            html += '<summary>Unrecognised tags (' + analysis.unrecognisedTags.length + ')</summary>';
            html += '<ul>';
            for (var u = 0; u < analysis.unrecognisedTags.length; u++) {
                html += '<li>Block #' + analysis.unrecognisedTags[u].blockIndex +
                    ': <code>' + this._esc(analysis.unrecognisedTags[u].raw) + '</code></li>';
            }
            html += '</ul>';
            html += '</details>';
        }

        // Red text instructions
        if (analysis.redTextInstructions.length > 0) {
            html += '<details class="debug-details">';
            html += '<summary>Red text instructions (' + analysis.redTextInstructions.length + ')</summary>';
            html += '<ul>';
            for (var ri = 0; ri < analysis.redTextInstructions.length; ri++) {
                html += '<li>Block #' + analysis.redTextInstructions[ri].blockIndex +
                    ': <code>' + this._esc(analysis.redTextInstructions[ri].text) + '</code></li>';
            }
            html += '</ul>';
            html += '</details>';
        }

        html += '</div>';

        // --- Page Boundary Results ---
        html += '<div class="debug-section">';
        html += '<h4 class="debug-section-title">Page Boundary Results</h4>';

        html += '<div class="debug-stats">';
        html += '<span class="debug-stat">Pages detected: <b>' + analysis.pages.length + '</b></span>';
        html += '</div>';

        if (analysis.pages.length > 0) {
            html += '<table class="debug-table"><thead><tr>' +
                '<th>File</th><th>Type</th><th>Lesson</th><th>Blocks</th><th>Rules Applied</th>' +
                '</tr></thead><tbody>';
            for (var pi = 0; pi < analysis.pages.length; pi++) {
                var page = analysis.pages[pi];
                var rulesHtml = '';
                if (page.boundaryDecisions && page.boundaryDecisions.length > 0) {
                    for (var d = 0; d < page.boundaryDecisions.length; d++) {
                        var dec = page.boundaryDecisions[d];
                        rulesHtml += '<span class="debug-rule-badge">Rule ' + dec.rule +
                            ': ' + this._esc(dec.action) + '</span> ';
                    }
                } else {
                    rulesHtml = '-';
                }

                html += '<tr>' +
                    '<td><code>' + this._esc(page.filename) + '</code></td>' +
                    '<td>' + this._esc(page.type) + '</td>' +
                    '<td>' + (page.lessonNumber !== null ? page.lessonNumber : '-') + '</td>' +
                    '<td>' + page.contentBlocks.length + '</td>' +
                    '<td>' + rulesHtml + '</td>' +
                    '</tr>';
            }
            html += '</tbody></table>';

            // Boundary decision details
            var allDecisions = [];
            for (var ai = 0; ai < analysis.pages.length; ai++) {
                var pg = analysis.pages[ai];
                if (pg.boundaryDecisions) {
                    for (var di = 0; di < pg.boundaryDecisions.length; di++) {
                        allDecisions.push({
                            page: pg.filename,
                            decision: pg.boundaryDecisions[di]
                        });
                    }
                }
            }

            if (allDecisions.length > 0) {
                html += '<details class="debug-details">';
                html += '<summary>Boundary rule details (' + allDecisions.length + ' rules fired)</summary>';
                html += '<ul>';
                for (var bd = 0; bd < allDecisions.length; bd++) {
                    var item = allDecisions[bd];
                    html += '<li><b>' + this._esc(item.page) + '</b> &mdash; Rule ' +
                        item.decision.rule + ': ' + this._esc(item.decision.reason) + '</li>';
                }
                html += '</ul>';
                html += '</details>';
            }
        }

        html += '</div>';

        // --- Block Scoping Results ---
        html += this._renderDebugBlockScopeSection(analysis);

        // --- Interactive Components ---
        html += this._renderDebugInteractiveSection();

        this._debugContent.innerHTML = html;
        this._debugPanel.classList.remove('hidden');
    }

    /**
     * Render conversion summary stats for the debug panel.
     * These were previously displayed in the main results area.
     *
     * @returns {string} HTML string
     */
    _renderDebugConversionSummary() {
        var html = '';
        html += '<div class="debug-section">';
        html += '<h4 class="debug-section-title">Conversion Summary</h4>';
        html += '<div class="debug-stats">';

        // Pages generated
        var htmlCount = this._outputManager.getHtmlFileCount();
        if (htmlCount > 0) {
            html += '<span class="debug-stat">Pages: <b>' + htmlCount + ' HTML files generated</b></span>';
        }

        // Template used
        if (this._selectedTemplateId) {
            try {
                var config = this._templateEngine.getConfig(this._selectedTemplateId);
                html += '<span class="debug-stat">Template: <b>' + this._esc(config._templateName) + '</b></span>';
            } catch (e) {
                // Ignore
            }
        }

        // Interactives detected
        if (this._collectedInteractives && this._collectedInteractives.length > 0) {
            html += '<span class="debug-stat">Interactives: <b>' +
                this._collectedInteractives.length + ' interactive components detected</b></span>';
        }

        // Tags normalised
        if (this._currentAnalysis) {
            var tagText = this._currentAnalysis.totalTags + ' tags normalised';
            if (this._currentAnalysis.unrecognisedTags.length > 0) {
                tagText += ' + ' + this._currentAnalysis.unrecognisedTags.length + ' unrecognised';
            }
            html += '<span class="debug-stat">Tags: <b>' + this._esc(tagText) + '</b></span>';
        }

        // Warnings
        if (this._currentAnalysis && this._currentAnalysis.pages) {
            var warningCount = 0;
            for (var pi = 0; pi < this._currentAnalysis.pages.length; pi++) {
                var pg = this._currentAnalysis.pages[pi];
                if (pg.boundaryDecisions && pg.boundaryDecisions.length > 0) {
                    warningCount += pg.boundaryDecisions.length;
                }
            }
            if (warningCount > 0) {
                html += '<span class="debug-stat">Warnings: <b>' + warningCount + ' boundary rules fired</b></span>';
            }
        }

        html += '</div>';
        html += '</div>';
        return html;
    }

    /**
     * Render block scoping analysis for the debug panel.
     *
     * @param {Object} analysis - Analysis results
     * @returns {string} HTML string
     */
    _renderDebugBlockScopeSection(analysis) {
        var html = '';
        html += '<div class="debug-section">';
        html += '<h4 class="debug-section-title">Block Scoping Analysis</h4>';

        if (!analysis.blockScopes || analysis.blockScopes.length === 0) {
            html += '<p style="font-size:0.82rem;color:var(--color-text-secondary);">No block scoping data available.</p>';
            html += '</div>';
            return html;
        }

        var scoped = analysis.blockScopes.filter(function(b) { return b.blockType; });
        var unscoped = analysis.blockScopes.filter(function(b) { return !b.blockType; });

        html += '<div class="debug-stats">';
        html += '<span class="debug-stat">Total entries: <b>' + analysis.blockScopes.length + '</b></span>';
        html += '<span class="debug-stat">Scoped blocks: <b>' + scoped.length + '</b></span>';
        html += '<span class="debug-stat">Unscoped content: <b>' + unscoped.length + '</b></span>';
        if (analysis.blockScopeWarnings && analysis.blockScopeWarnings.length > 0) {
            html += '<span class="debug-stat">Warnings: <b>' + analysis.blockScopeWarnings.length + '</b></span>';
        }
        html += '</div>';

        // Scoped blocks table
        if (scoped.length > 0) {
            html += '<details class="debug-details">';
            html += '<summary>Scoped blocks (' + scoped.length + ')</summary>';
            html += '<table class="debug-table"><thead><tr>' +
                '<th>Type</th><th>Start</th><th>End</th><th>Children</th><th>Closure</th><th>Sub-tags</th>' +
                '</tr></thead><tbody>';
            for (var i = 0; i < scoped.length; i++) {
                var block = scoped[i];
                var childCount = block.children ? block.children.length : 0;
                var subTags = '';
                if (block.children) {
                    var subTagNames = [];
                    for (var j = 0; j < block.children.length; j++) {
                        if (block.children[j].subTagIndex !== undefined) {
                            subTagNames.push('#' + block.children[j].subTagIndex);
                        }
                    }
                    subTags = subTagNames.length > 0 ? subTagNames.join(', ') : '-';
                }

                html += '<tr>' +
                    '<td><code>' + this._esc(block.blockType || '') + '</code></td>' +
                    '<td>' + (block.startIndex !== undefined ? block.startIndex : '-') + '</td>' +
                    '<td>' + (block.endIndex !== undefined ? block.endIndex : '-') + '</td>' +
                    '<td>' + childCount + '</td>' +
                    '<td>' + this._esc(block.closureReason || '-') + '</td>' +
                    '<td>' + subTags + '</td>' +
                    '</tr>';
            }
            html += '</tbody></table>';
            html += '</details>';
        }

        // Warnings
        if (analysis.blockScopeWarnings && analysis.blockScopeWarnings.length > 0) {
            html += '<details class="debug-details debug-warning">';
            html += '<summary>Scoping warnings (' + analysis.blockScopeWarnings.length + ')</summary>';
            html += '<ul>';
            for (var w = 0; w < analysis.blockScopeWarnings.length; w++) {
                html += '<li>' + this._esc(analysis.blockScopeWarnings[w]) + '</li>';
            }
            html += '</ul>';
            html += '</details>';
        }

        html += '</div>';
        return html;
    }

    // ------------------------------------------------------------------
    // Debug — Interactive section
    // ------------------------------------------------------------------

    /**
     * Render interactive component details for the debug panel.
     *
     * @returns {string} HTML string
     */
    _renderDebugInteractiveSection() {
        var html = '';
        html += '<div class="debug-section">';
        html += '<h4 class="debug-section-title">Interactive Components</h4>';

        if (!this._collectedInteractives || this._collectedInteractives.length === 0) {
            html += '<p style="font-size:0.82rem;color:var(--color-text-secondary);">No interactive components detected.</p>';
            html += '</div>';
            return html;
        }

        var total = this._collectedInteractives.length;
        var tier1 = 0;
        var tier2 = 0;
        for (var c = 0; c < total; c++) {
            if (this._collectedInteractives[c].tier === 1) tier1++;
            else tier2++;
        }

        html += '<div class="debug-stats">';
        html += '<span class="debug-stat">Total: <b>' + total + '</b></span>';
        html += '<span class="debug-stat">Tier 1 (PageForge): <b>' + tier1 + '</b></span>';
        html += '<span class="debug-stat">Tier 2 (requires implementation): <b>' + tier2 + '</b></span>';
        html += '</div>';

        // Interactive list table
        html += '<details class="debug-details">';
        html += '<summary>All interactives (' + total + ')</summary>';
        html += '<table class="debug-table"><thead><tr>' +
            '<th>#</th><th>File</th><th>Activity</th><th>Type</th><th>Tier</th><th>Pattern</th><th>Data</th>' +
            '</tr></thead><tbody>';

        for (var j = 0; j < total; j++) {
            var entry = this._collectedInteractives[j];
            var tierLabel = entry.tier === 1 ? '<span style="color:green;">T1</span>' : '<span style="color:red;">T2</span>';
            var dataSummary = '';
            if (entry.tableData) {
                dataSummary = 'Table (' + this._esc(entry.tableData.dimensions) + ')';
            } else if (entry.numberedItems && entry.numberedItems.length > 0) {
                dataSummary = entry.numberedItems.length + ' items';
            } else {
                dataSummary = '-';
            }

            html += '<tr>' +
                '<td>' + (j + 1) + '</td>' +
                '<td><code>' + this._esc(entry.filename) + '</code></td>' +
                '<td>' + (entry.activityId ? this._esc(entry.activityId) : '-') + '</td>' +
                '<td><code>' + this._esc(entry.type) + '</code>' +
                    (entry.modifier ? ' <small>(' + this._esc(entry.modifier) + ')</small>' : '') + '</td>' +
                '<td>' + tierLabel + '</td>' +
                '<td>' + entry.dataPattern + '</td>' +
                '<td>' + dataSummary + '</td>' +
                '</tr>';
        }

        html += '</tbody></table>';
        html += '</details>';

        // Reference document preview
        if (this._interactiveReferenceDoc) {
            html += '<details class="debug-details">';
            html += '<summary>Reference document preview</summary>';
            html += '<pre style="padding:0.5rem;font-size:0.75rem;overflow-x:auto;background:var(--color-bg);margin:0;max-height:400px;overflow-y:auto;">';
            html += this._esc(this._interactiveReferenceDoc.substring(0, 5000));
            if (this._interactiveReferenceDoc.length > 5000) {
                html += '\n... (' + (this._interactiveReferenceDoc.length - 5000) + ' more characters)';
            }
            html += '</pre>';
            html += '</details>';
        }

        html += '</div>';
        return html;
    }

    // ------------------------------------------------------------------
    // Debug — Template section
    // ------------------------------------------------------------------

    /**
     * Render template configuration info for the debug panel.
     *
     * @param {Object} analysis - Analysis results
     * @returns {string} HTML string
     */
    _renderDebugTemplateSection(analysis) {
        var html = '';
        html += '<div class="debug-section">';
        html += '<h4 class="debug-section-title">Template Configuration</h4>';

        if (!this._selectedTemplateId) {
            html += '<p style="font-size:0.82rem;color:var(--color-text-secondary);">No template selected.</p>';
            html += '</div>';
            return html;
        }

        var config;
        try {
            config = this._templateEngine.getConfig(this._selectedTemplateId);
        } catch (e) {
            html += '<p style="font-size:0.82rem;color:var(--color-error);">Error loading template config.</p>';
            html += '</div>';
            return html;
        }

        // Summary stats
        html += '<div class="debug-stats">';
        html += '<span class="debug-stat">Template ID: <b>' + this._esc(this._selectedTemplateId) + '</b></span>';
        html += '<span class="debug-stat">Name: <b>' + this._esc(config._templateName) + '</b></span>';
        html += '<span class="debug-stat">HTML template attr: <b>' + this._esc(config._templateAttribute) + '</b></span>';
        html += '</div>';

        // Key config differences from base
        var diffs = this._getConfigDiffs(config);
        if (diffs.length > 0) {
            html += '<details class="debug-details">';
            html += '<summary>Key configuration (' + diffs.length + ' differences from base)</summary>';
            html += '<table class="debug-table"><thead><tr>' +
                '<th>Property</th><th>Value</th>' +
                '</tr></thead><tbody>';
            for (var i = 0; i < diffs.length; i++) {
                html += '<tr>' +
                    '<td><code>' + this._esc(diffs[i].key) + '</code></td>' +
                    '<td>' + this._esc(diffs[i].value) + '</td>' +
                    '</tr>';
            }
            html += '</tbody></table>';
            html += '</details>';
        }

        // Skeleton preview (first 50 lines for overview page)
        var moduleCode = (this._currentMetadata && this._currentMetadata.moduleCode) || 'MODULE';
        var totalPages = analysis.pages ? analysis.pages.length : 1;

        try {
            var skeleton = this._templateEngine.generateSkeleton(config, {
                type: 'overview',
                lessonNumber: null,
                filename: moduleCode + '-00.html',
                moduleCode: moduleCode,
                englishTitle: 'Module Title',
                tereoTitle: null,
                totalPages: totalPages,
                pageIndex: 0
            });

            var skeletonLines = skeleton.split('\n');
            var previewLines = skeletonLines.slice(0, 50);
            var truncated = skeletonLines.length > 50;

            html += '<details class="debug-details">';
            html += '<summary>Overview page skeleton preview (' + skeletonLines.length + ' lines)</summary>';
            html += '<pre style="padding:0.5rem;font-size:0.75rem;overflow-x:auto;background:var(--color-bg);margin:0;">';
            html += this._esc(previewLines.join('\n'));
            if (truncated) {
                html += '\n... (' + (skeletonLines.length - 50) + ' more lines)';
            }
            html += '</pre>';
            html += '</details>';
        } catch (e) {
            // Skeleton generation failed — skip preview
        }

        // Footer navigation links for each page
        if (analysis.pages && analysis.pages.length > 0) {
            html += '<details class="debug-details">';
            html += '<summary>Footer navigation (' + analysis.pages.length + ' pages)</summary>';
            html += '<table class="debug-table"><thead><tr>' +
                '<th>Page</th><th>Prev</th><th>Next</th><th>Home</th>' +
                '</tr></thead><tbody>';
            for (var pi = 0; pi < analysis.pages.length; pi++) {
                var page = analysis.pages[pi];
                var prevLink = pi > 0
                    ? moduleCode + '-' + String(pi - 1).padStart(2, '0') + '.html'
                    : '-';
                var nextLink = pi < analysis.pages.length - 1
                    ? moduleCode + '-' + String(pi + 1).padStart(2, '0') + '.html'
                    : '-';
                html += '<tr>' +
                    '<td><code>' + this._esc(page.filename) + '</code></td>' +
                    '<td>' + (prevLink !== '-' ? '<code>' + this._esc(prevLink) + '</code>' : '-') + '</td>' +
                    '<td>' + (nextLink !== '-' ? '<code>' + this._esc(nextLink) + '</code>' : '-') + '</td>' +
                    '<td>Yes</td>' +
                    '</tr>';
            }
            html += '</tbody></table>';
            html += '</details>';
        }

        html += '</div>';
        return html;
    }

    /**
     * Get notable differences between a resolved config and base defaults.
     *
     * @param {Object} config - Resolved template config
     * @returns {Array<{key: string, value: string}>}
     */
    _getConfigDiffs(config) {
        var diffs = [];

        // Body class
        if (config.bodyClass !== 'container-fluid') {
            diffs.push({ key: 'bodyClass', value: config.bodyClass });
        }

        // Footer class
        if (config.footerClass !== 'footer-nav') {
            diffs.push({ key: 'footerClass', value: config.footerClass });
        }

        // Header titles
        var overviewTitles = config.headerPattern &&
            config.headerPattern.overviewPage &&
            config.headerPattern.overviewPage.titles;
        if (overviewTitles && overviewTitles.indexOf('tereo') !== -1) {
            diffs.push({ key: 'headerPattern.overviewPage.titles', value: overviewTitles.join(', ') });
        }

        var lessonTitles = config.headerPattern &&
            config.headerPattern.lessonPage &&
            config.headerPattern.lessonPage.titles;
        if (lessonTitles && lessonTitles.indexOf('tereo') !== -1) {
            diffs.push({ key: 'headerPattern.lessonPage.titles', value: lessonTitles.join(', ') });
        }

        // Module menu lesson labels
        var lessonLabels = config.moduleMenu &&
            config.moduleMenu.lessonPage &&
            config.moduleMenu.lessonPage.labels;
        if (lessonLabels) {
            diffs.push({ key: 'moduleMenu.lessonPage.labels.success', value: lessonLabels.success });
        }

        // Overview tabs
        var overviewTabs = config.moduleMenu &&
            config.moduleMenu.overviewPage &&
            config.moduleMenu.overviewPage.tabs;
        if (overviewTabs && overviewTabs.length !== 2) {
            diffs.push({ key: 'moduleMenu.overviewPage.tabs', value: overviewTabs.join(', ') });
        }

        // Navigation
        if (config.navigation) {
            diffs.push({ key: 'navigation', value: config.navigation });
        }

        // Content duplication
        if (config.contentDuplication) {
            diffs.push({ key: 'contentDuplication', value: config.contentDuplication });
        }

        return diffs;
    }

    _esc(str) {
        var div = document.createElement('div');
        div.appendChild(document.createTextNode(str));
        return div.innerHTML;
    }
}
