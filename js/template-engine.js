/**
 * TemplateEngine — Loads, resolves, and applies template configurations.
 *
 * Reads template definitions from templates/templates.json (with an embedded
 * fallback for file:// usage) and provides deep-merge resolution, auto-detection
 * from module codes, and complete HTML skeleton generation.
 */

'use strict';

class TemplateEngine {
    constructor() {
        /** @type {Object|null} Raw template data (baseConfig + templates) */
        this._data = null;

        /** @type {boolean} Whether templates have been loaded */
        this._loaded = false;

        /** @type {Map<string, Object>} Cached resolved configs */
        this._configCache = new Map();
    }

    // ------------------------------------------------------------------
    // Loading
    // ------------------------------------------------------------------

    /**
     * Load templates from templates.json (via fetch) or use embedded fallback.
     * Safe to call multiple times — subsequent calls are no-ops.
     *
     * @returns {Promise<void>}
     */
    async loadTemplates() {
        if (this._loaded) return;

        try {
            var response = await fetch('templates/templates.json');
            if (!response.ok) {
                throw new Error('HTTP ' + response.status);
            }
            this._data = await response.json();
        } catch (err) {
            console.warn('TemplateEngine: Could not fetch templates.json (' +
                err.message + '), using embedded fallback.');
            this._data = TemplateEngine._embeddedData();
        }

        this._loaded = true;
        this._configCache.clear();
    }

    // ------------------------------------------------------------------
    // Public API — template list
    // ------------------------------------------------------------------

    /**
     * Get the ordered list of available templates for UI dropdown population.
     *
     * @returns {Array<{id: string, name: string}>}
     */
    getTemplateList() {
        this._ensureLoaded();
        var templates = this._data.templates;
        var list = [];
        var keys = Object.keys(templates);
        for (var i = 0; i < keys.length; i++) {
            list.push({
                id: keys[i],
                name: templates[keys[i]].name
            });
        }
        return list;
    }

    // ------------------------------------------------------------------
    // Public API — auto-detection
    // ------------------------------------------------------------------

    /**
     * Detect the most likely template ID from a module code.
     *
     * @param {string} moduleCode - e.g. 'OSAI201'
     * @returns {string|null} Template ID or null if not detectable
     */
    detectTemplate(moduleCode) {
        if (!moduleCode) return null;
        var match = moduleCode.match(/(\d{3})$/);
        if (!match) return null;

        var suffix = match[1];
        var suffixMap = {
            '101': '1-3',
            '201': '4-6',
            '301': '7-8',
            '401': '9-10',
            '501': 'NCEA'
        };
        return suffixMap[suffix] || null;
    }

    // ------------------------------------------------------------------
    // Public API — configuration resolution
    // ------------------------------------------------------------------

    /**
     * Get the fully resolved (merged) configuration for a template.
     *
     * @param {string} templateId - Template key (e.g. '4-6', 'NCEA')
     * @returns {Object} Merged configuration
     * @throws {Error} If template ID is unknown
     */
    getConfig(templateId) {
        this._ensureLoaded();

        if (this._configCache.has(templateId)) {
            return this._configCache.get(templateId);
        }

        var template = this._data.templates[templateId];
        if (!template) {
            throw new Error('TemplateEngine: Unknown template "' + templateId + '"');
        }

        // Clone baseConfig deeply
        var config = TemplateEngine._deepClone(this._data.baseConfig);

        // Deep-merge overrides
        if (template.overrides) {
            TemplateEngine._deepMerge(config, template.overrides);
        }

        // Attach template-level metadata
        config._templateId = templateId;
        config._templateName = template.name;
        config._templateAttribute = template.templateAttribute;

        this._configCache.set(templateId, config);
        return config;
    }

    // ------------------------------------------------------------------
    // Public API — skeleton generation
    // ------------------------------------------------------------------

    /**
     * Generate a complete HTML skeleton for a page.
     *
     * @param {Object} config   - Resolved template config from getConfig()
     * @param {Object} pageData - Page-specific data
     * @param {string} pageData.type           - 'overview' or 'lesson'
     * @param {number|null} pageData.lessonNumber - Lesson number (null for overview)
     * @param {string} pageData.filename       - e.g. 'OSAI201-00.html'
     * @param {string} pageData.moduleCode     - e.g. 'OSAI201'
     * @param {string} pageData.englishTitle   - e.g. 'AI Digital Citizenship'
     * @param {string|null} pageData.tereoTitle - Te Reo title or null
     * @param {number} pageData.totalPages     - Total number of pages
     * @param {number} pageData.pageIndex      - 0-based index of this page
     * @returns {string} Complete HTML string with <!-- CONTENT_PLACEHOLDER -->
     */
    generateSkeleton(config, pageData) {
        var isOverview = pageData.type === 'overview';
        var lessonNum = pageData.lessonNumber;
        var lessonPadded = lessonNum !== null
            ? String(lessonNum).padStart(2, '0')
            : null;

        // Strip module code prefix from title for <title> element
        var rawTitle = pageData.englishTitle || '';
        var modulePrefix = pageData.moduleCode
            ? pageData.moduleCode.replace(/\d+$/, '')
            : '';
        if (modulePrefix && rawTitle) {
            var prefixRegex = new RegExp('^' + modulePrefix.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\s*', 'i');
            rawTitle = rawTitle.replace(prefixRegex, '');
        }
        // Split on double-space and take English only
        var englishOnlyTitle = rawTitle.split(/  +/)[0].trim();

        // Title element (English only — NEVER Te Reo)
        var titleContent = isOverview
            ? pageData.moduleCode + ' ' + englishOnlyTitle
            : pageData.moduleCode + ' ' + (lessonPadded || '');

        // HTML attributes
        var htmlAttrs = config.htmlAttributes;
        var templateAttr = config._templateAttribute;

        // Build the document
        var lines = [];
        lines.push(config.doctype);
        lines.push('<html lang="' + htmlAttrs.lang +
            '" level="' + htmlAttrs.level +
            '" template="' + templateAttr +
            '" class="' + htmlAttrs.class +
            '" translate="' + htmlAttrs.translate + '">');

        // <head>
        lines.push('<head>');
        lines.push('  <meta charset="utf-8" />');
        lines.push('  <meta content="IE=edge" http-equiv="X-UA-Compatible" />');
        lines.push('  <meta content="width=device-width, initial-scale=1" name="viewport" />');
        lines.push('  <title>' + this._escHtml(titleContent.trim()) + '</title>');
        lines.push('  <script type="text/javascript" src="' + config.scriptUrl + '"><\/script>');
        lines.push('</head>');

        // <body>
        lines.push('<body class="' + config.bodyClass + '">');

        // Header
        lines.push(this._generateHeader(config, pageData, isOverview, lessonPadded));

        // Body (content placeholder)
        lines.push('  <div id="body">');
        lines.push('    <!-- CONTENT_PLACEHOLDER -->');
        lines.push('  </div>');

        // Footer
        lines.push(this._generateFooter(config, pageData));

        lines.push('</body>');
        lines.push('</html>');

        return lines.join('\n');
    }

    // ------------------------------------------------------------------
    // Skeleton helpers — header
    // ------------------------------------------------------------------

    /**
     * @private
     */
    _generateHeader(config, pageData, isOverview, lessonPadded) {
        var lines = [];
        var headerPattern = isOverview
            ? config.headerPattern.overviewPage
            : config.headerPattern.lessonPage;

        // Module code content
        var moduleCodeContent = isOverview
            ? pageData.moduleCode
            : (lessonPadded || '01');

        // Title(s)
        var englishTitle = pageData.englishTitle || '';
        var tereoTitle = pageData.tereoTitle || '';
        var titles = headerPattern.titles || ['english'];

        // Strip module code prefix from titles if present
        var modulePrefix = pageData.moduleCode
            ? pageData.moduleCode.replace(/\d+$/, '')
            : '';
        if (modulePrefix && englishTitle) {
            // Strip prefix (e.g. "OSAI") from start of title
            var prefixRegex = new RegExp('^' + modulePrefix.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\s*', 'i');
            englishTitle = englishTitle.replace(prefixRegex, '');
        }

        // Split English and Te Reo titles on double-space
        var splitTitles = englishTitle.split(/  +/);
        var englishOnly = (splitTitles[0] || '').trim();
        var tereoFromTitle = splitTitles.length > 1 ? splitTitles.slice(1).join('  ').trim() : '';

        // Use tereoFromTitle if no separate tereoTitle was provided
        if (tereoFromTitle && !tereoTitle) {
            tereoTitle = tereoFromTitle;
        }

        // For lesson pages, title source is 'module' (uses module title, not lesson-specific)
        var titleText = englishOnly || englishTitle;

        lines.push('  <div id="header">');
        lines.push('    <div id="module-code"><h1>' + this._escHtml(moduleCodeContent) + '</h1></div>');

        // English h1
        lines.push('    <h1><span>' + this._escHtml(titleText) + ' </span></h1>');

        // Te Reo h1 (if dual titles OR if title was split from double-space)
        if ((titles.indexOf('tereo') !== -1 || tereoTitle) && tereoTitle) {
            lines.push('    <h1><span>' + this._escHtml(tereoTitle) + ' </span></h1>');
        }

        // Module head buttons + module menu
        lines.push(this._generateModuleMenu(config, pageData, isOverview));

        lines.push('  </div>');
        return lines.join('\n');
    }

    /**
     * @private
     */
    _generateModuleMenu(config, pageData, isOverview) {
        var lines = [];
        var menuConfig = isOverview
            ? config.moduleMenu.overviewPage
            : config.moduleMenu.lessonPage;

        // Module head buttons wrapper
        lines.push('    <div id="module-head-buttons">');

        if (isOverview) {
            // Overview page: NO tooltip on button (tooltip goes on module-menu-content only)
            lines.push('      <div id="module-menu-button" class="circle-button btn1"></div>');
        } else {
            // Lesson page: tooltip on button
            var btnTooltip = menuConfig.tooltipOn === 'module-menu-button'
                ? ' tooltip="Overview"'
                : '';
            lines.push('      <div id="module-menu-button" class="circle-button btn1"' + btnTooltip + '></div>');
        }

        lines.push('    </div>');

        // Module menu content
        if (isOverview) {
            var tooltipAttr = menuConfig.tooltipOn === 'module-menu-content'
                ? ' tooltip="Overview"'
                : '';
            lines.push('    <div id="module-menu-content" class="moduleMenu"' + tooltipAttr + '>');

            // Full tabbed menu — wrapped in row
            var tabs = menuConfig.tabs || ['Overview', 'Information'];
            lines.push('      <div class="row">');
            lines.push('        <div class="tabs col-12">');
            lines.push('          <ul class="nav nav-tabs">');
            for (var t = 0; t < tabs.length; t++) {
                // No class, no data-toggle, no href on tab elements
                lines.push('            <li><a>' + this._escHtml(tabs[t]) + '</a></li>');
            }
            lines.push('          </ul>');
            lines.push('          <div class="tab-content">');
            for (var tp = 0; tp < tabs.length; tp++) {
                // No id, no fade, no active, no in — just tab-pane
                lines.push('            <div class="tab-pane">');
                lines.push('              <!-- MODULE_MENU_CONTENT: ' +
                    this._escHtml(tabs[tp]) + ' -->');
                lines.push('            </div>');
            }
            lines.push('          </div>');
            lines.push('        </div>');
            lines.push('      </div>');
        } else {
            // Lesson page: simplified menu (no tabs)
            lines.push('    <div id="module-menu-content" class="moduleMenu">');
            lines.push('      <div class="row">');
            lines.push('        <div class="col-md-8 col-12">');
            lines.push('          <!-- MODULE_MENU_CONTENT -->');
            lines.push('        </div>');
            lines.push('      </div>');
        }

        lines.push('    </div>');
        return lines.join('\n');
    }

    // ------------------------------------------------------------------
    // Skeleton helpers — footer
    // ------------------------------------------------------------------

    /**
     * @private
     */
    _generateFooter(config, pageData) {
        var lines = [];
        var footerClass = config.footerClass;
        var moduleCode = pageData.moduleCode;
        var pageIndex = pageData.pageIndex;
        var totalPages = pageData.totalPages;
        var isFirst = pageIndex === 0;
        var isLast = pageIndex === totalPages - 1;

        lines.push('  <div id="footer">');
        lines.push('    <ul class="' + footerClass + '">');

        // prev-lesson (not on overview page)
        if (!isFirst) {
            var prevPage = String(pageIndex - 1).padStart(2, '0');
            lines.push('      <li><a href="' + moduleCode + '-' + prevPage +
                '.html" id="prev-lesson" target="_self"></a></li>');
        }

        // next-lesson (not on final page)
        if (!isLast) {
            var nextPage = String(pageIndex + 1).padStart(2, '0');
            lines.push('      <li><a href="' + moduleCode + '-' + nextPage +
                '.html" id="next-lesson" target="_self"></a></li>');
        }

        // home-nav (always present)
        lines.push('      <li><a href="" class="home-nav" target="_parent"></a></li>');

        lines.push('    </ul>');
        lines.push('  </div>');
        return lines.join('\n');
    }

    // ------------------------------------------------------------------
    // Deep merge utilities
    // ------------------------------------------------------------------

    /**
     * Deep-clone a plain object/array.
     *
     * @param {*} obj
     * @returns {*}
     */
    static _deepClone(obj) {
        if (obj === null || typeof obj !== 'object') return obj;
        if (Array.isArray(obj)) {
            var arr = [];
            for (var i = 0; i < obj.length; i++) {
                arr.push(TemplateEngine._deepClone(obj[i]));
            }
            return arr;
        }
        var clone = {};
        var keys = Object.keys(obj);
        for (var k = 0; k < keys.length; k++) {
            clone[keys[k]] = TemplateEngine._deepClone(obj[keys[k]]);
        }
        return clone;
    }

    /**
     * Deep-merge source into target (mutates target).
     * Arrays and primitives replace entirely; objects merge recursively.
     *
     * @param {Object} target
     * @param {Object} source
     */
    static _deepMerge(target, source) {
        var keys = Object.keys(source);
        for (var i = 0; i < keys.length; i++) {
            var key = keys[i];
            var srcVal = source[key];
            var tgtVal = target[key];

            if (srcVal !== null &&
                typeof srcVal === 'object' &&
                !Array.isArray(srcVal) &&
                tgtVal !== null &&
                typeof tgtVal === 'object' &&
                !Array.isArray(tgtVal)) {
                // Both are plain objects — recurse
                TemplateEngine._deepMerge(tgtVal, srcVal);
            } else {
                // Primitives, arrays, or null — replace entirely
                target[key] = TemplateEngine._deepClone(srcVal);
            }
        }
    }

    // ------------------------------------------------------------------
    // Internal helpers
    // ------------------------------------------------------------------

    /**
     * @private
     */
    _ensureLoaded() {
        if (!this._loaded) {
            throw new Error('TemplateEngine: Templates not loaded. Call loadTemplates() first.');
        }
    }

    /**
     * @private
     */
    _escHtml(str) {
        if (!str) return '';
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    // ------------------------------------------------------------------
    // Embedded fallback data
    // ------------------------------------------------------------------

    /**
     * Returns the embedded template data as a fallback when fetch fails.
     *
     * @returns {Object}
     */
    static _embeddedData() {
        return {
            "version": "1.0",
            "baseConfig": {
                "doctype": "<!doctype html>",
                "htmlAttributes": {
                    "lang": "en",
                    "level": "",
                    "class": "notranslate",
                    "translate": "no"
                },
                "scriptUrl": "https://tekura.desire2learn.com/shared/refresh_template/js/idoc_scripts.js",
                "bodyClass": "container-fluid",
                "voidElementStyle": "xhtml",
                "defaultColumnClass": "col-md-8 col-12",
                "headingSpanRule": "h1-header-only",
                "footerClass": "footer-nav",
                "moduleMenu": {
                    "overviewPage": {
                        "type": "full-tabs",
                        "tabs": ["Overview", "Information"],
                        "tooltipOn": "module-menu-content",
                        "headingLevel": "h4",
                        "overviewTitleTag": "h4-span",
                        "successCriteriaHeading": "How will I know if I've learned it?"
                    },
                    "lessonPage": {
                        "type": "simplified",
                        "tooltipOn": "module-menu-button",
                        "headingLevel": "h5",
                        "labels": {
                            "learning": "We are learning:",
                            "success": "I can:"
                        }
                    }
                },
                "titlePattern": {
                    "overviewPage": "{moduleCode} {englishTitle}",
                    "lessonPage": "{moduleCode} {lessonNumber}"
                },
                "headerPattern": {
                    "overviewPage": {
                        "moduleCodeContent": "{moduleCode}",
                        "titles": ["english"]
                    },
                    "lessonPage": {
                        "moduleCodeContent": "{lessonNumberZeroPadded}",
                        "titleSource": "module",
                        "titles": ["english"]
                    }
                },
                "imageDefaults": {
                    "class": "img-fluid",
                    "loading": "lazy",
                    "placeholderBase": "https://placehold.co"
                },
                "videoEmbed": {
                    "youtube": "youtube-nocookie.com/embed",
                    "wrapperClass": "videoSection ratio ratio-16x9"
                },
                "gridRules": {
                    "defaultContent": "col-md-8 col-12",
                    "wideInteractive": "col-md-12 col-12",
                    "wideInteractiveImages": "col-md-10 col-12",
                    "carousel": "col-md-8 col-12"
                },
                "interactivePlaceholder": true
            },
            "templates": {
                "1-3": {
                    "name": "Years 1\u20133",
                    "templateAttribute": "1-3",
                    "inherits": "baseConfig",
                    "overrides": {
                        "moduleMenu": {
                            "lessonPage": {
                                "labels": {
                                    "learning": "We are learning:",
                                    "success": "You will show your understanding by:"
                                }
                            }
                        }
                    }
                },
                "4-6": {
                    "name": "Years 4\u20136",
                    "templateAttribute": "4-6",
                    "inherits": "baseConfig",
                    "overrides": {
                        "moduleMenu": {
                            "lessonPage": {
                                "labels": {
                                    "learning": "We are learning:",
                                    "success": "You will show your understanding by:"
                                }
                            }
                        }
                    }
                },
                "7-8": {
                    "name": "Years 7\u20138",
                    "templateAttribute": "7-8",
                    "inherits": "baseConfig",
                    "overrides": {
                        "moduleMenu": {
                            "lessonPage": {
                                "labels": {
                                    "learning": "We are learning:",
                                    "success": "I can:"
                                }
                            }
                        }
                    }
                },
                "9-10": {
                    "name": "Years 9\u201310",
                    "templateAttribute": "9-10",
                    "inherits": "baseConfig",
                    "overrides": {
                        "headerPattern": {
                            "overviewPage": {
                                "titles": ["english", "tereo"]
                            },
                            "lessonPage": {
                                "titles": ["english", "tereo"]
                            }
                        },
                        "moduleMenu": {
                            "lessonPage": {
                                "labels": {
                                    "learning": "We are learning:",
                                    "success": "I can:"
                                }
                            }
                        }
                    }
                },
                "NCEA": {
                    "name": "NCEA",
                    "templateAttribute": "NCEA",
                    "inherits": "baseConfig",
                    "overrides": {
                        "headerPattern": {
                            "overviewPage": {
                                "titles": ["english", "tereo"]
                            },
                            "lessonPage": {
                                "titles": ["english", "tereo"]
                            }
                        },
                        "moduleMenu": {
                            "overviewPage": {
                                "tabs": ["Overview", "Information", "Standards"],
                                "tooltipOn": null
                            },
                            "lessonPage": {
                                "labels": {
                                    "learning": "We are learning:",
                                    "success": "I can:"
                                }
                            }
                        }
                    }
                },
                "bilingual": {
                    "name": "Bilingual",
                    "templateAttribute": "1-3",
                    "inherits": "baseConfig",
                    "overrides": {
                        "bodyClass": "container-fluid reoTranslate",
                        "contentDuplication": "eng-reo",
                        "headerPattern": {
                            "overviewPage": { "titles": ["english", "tereo"] },
                            "lessonPage": { "titles": ["english", "tereo"] }
                        }
                    }
                },
                "fundamentals": {
                    "name": "Fundamentals",
                    "templateAttribute": "combo",
                    "inherits": "baseConfig",
                    "overrides": {
                        "bodyClass": "fundamentals container-fluid",
                        "navigation": "phases",
                        "footerClass": "footer-nav fundamentals-nav"
                    }
                },
                "inquiry": {
                    "name": "Inquiry",
                    "templateAttribute": "combo",
                    "inherits": "baseConfig",
                    "overrides": {
                        "bodyClass": "inquiry container-fluid",
                        "navigation": "crumbs",
                        "footerClass": "footer-nav inquiry-nav"
                    }
                },
                "combo": {
                    "name": "Combo (Standalone)",
                    "templateAttribute": "combo",
                    "inherits": "baseConfig"
                }
            }
        };
    }
}
