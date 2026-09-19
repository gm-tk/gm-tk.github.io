/**
 * OutputFormatter — Converts parsed DocxParser output into structured
 * plain text for display, clipboard copy, and file download.
 */

'use strict';

class OutputFormatter {

    /**
     * The activity-table template notice (session 28, Task 2 — the XOTP dialect).
     * A data-shaped switch: `enabled` false (or `window.PF_ACTIVITY_TABLE_NOTICE_OFF`
     * set, the A/B toggle) restores the plain "[TITLE BAR] marker not found" warning
     * for every document. `header` is the folded two-cell header row that identifies
     * the shape; `scan_rows` is how deep into a table the header row may sit (the
     * XOTP tables open with a merged title row, so the header is the SECOND row).
     */
    static ACTIVITY_TABLE_NOTICE = {
        enabled: true,
        header: ['section heading', 'text/activity'],
        scan_rows: 3,
        message: 'ℹ Activity-table template detected (a "Section heading | Text/Activity" table, no red tags) — no [TITLE BAR] expected. Showing all extracted content.'
    };

    /**
     * Is this document the activity-table dialect? True when any table's first
     * `scan_rows` rows hold exactly two cells whose folded text is the header pair.
     * @param {Array} content - the parser's content blocks
     * @returns {boolean}
     */
    _isActivityTableDoc(content) {
        const cfg = OutputFormatter.ACTIVITY_TABLE_NOTICE;
        if (!cfg || cfg.enabled === false) return false;
        if (typeof window !== 'undefined' && window.PF_ACTIVITY_TABLE_NOTICE_OFF) return false;
        const fold = (cell) => {
            const parts = [];
            for (let p = 0; p < (cell.paragraphs || []).length; p++) {
                const para = cell.paragraphs[p];
                if (!para || para.nestedTable) continue;
                let t = para.text;
                if ((t === undefined || t === null) && para.runs) {
                    t = para.runs.map((r) => r.text || '').join('');
                }
                if (t) parts.push(t);
            }
            return parts.join(' ').replace(/[*_]/g, '').replace(/\s+/g, ' ').trim().toLowerCase();
        };
        const want = cfg.header.map((h) => String(h).toLowerCase());
        for (let i = 0; i < (content || []).length; i++) {
            const block = content[i];
            if (!block || block.type !== 'table' || !block.data || !block.data.rows) continue;
            const rows = block.data.rows;
            for (let r = 0; r < Math.min(rows.length, cfg.scan_rows || 3); r++) {
                const cells = rows[r].cells || [];
                if (cells.length !== want.length) continue;
                let ok = true;
                for (let c = 0; c < want.length; c++) {
                    if (fold(cells[c]) !== want[c]) { ok = false; break; }
                }
                if (ok) return true;
            }
        }
        return false;
    }

    /**
     * Format everything: metadata header + content.
     * @param {Object} parserResult - Result from DocxParser.parse()
     * @returns {{ full: string, metadataOnly: string, contentOnly: string }}
     */
    formatAll(parserResult) {
        const metadataBlock = this.formatMetadata(parserResult.metadata);
        let contentBlock = this.formatContent(
            parserResult.content,
            parserResult.contentStartIndex,
            parserResult.contentStartFound
        );

        // Post-processing: strip red text markers that wrap only whitespace
        contentBlock = this._stripEmptyRedText(contentBlock);

        return {
            full: metadataBlock + '\n' + contentBlock,
            metadataOnly: metadataBlock,
            contentOnly: contentBlock
        };
    }

    /**
     * Format the metadata header block.
     */
    formatMetadata(metadata) {
        const lines = [];
        lines.push('=====================================');
        lines.push('MODULE METADATA');
        lines.push('=====================================');

        if (metadata.moduleCode) {
            lines.push('Module Code: ' + metadata.moduleCode);
        }
        if (metadata.subject) {
            lines.push('Subject: ' + metadata.subject);
        }
        if (metadata.course) {
            lines.push('Course: ' + metadata.course);
        }
        if (metadata.writer) {
            lines.push('Writer: ' + metadata.writer);
        }
        if (metadata.date) {
            lines.push('Date: ' + metadata.date);
        }

        // If no metadata was found, say so
        if (!metadata.moduleCode && !metadata.subject && !metadata.course) {
            lines.push('(No metadata detected in boilerplate)');
        }

        lines.push('=====================================');
        return lines.join('\n');
    }

    /**
     * Format the content blocks from contentStartIndex to end of document.
     */
    formatContent(content, startIndex, startFound) {
        const lines = [];

        // Reset list counters for fresh content formatting
        this._listCounters = {};
        this._lastListNumId = null;

        lines.push('');
        lines.push('--- CONTENT START ---');

        if (!startFound) {
            lines.push('');
            // The XOTP activity-table dialect (12 modules, September 2026 intake) carries
            // NO red tags at all: its structure is a two-column "Section heading | Text/
            // Activity" table, so "[TITLE BAR] not found" is the expected shape, not a
            // failure. Say so plainly instead of a warning that reads like breakage.
            // The header row is the detector (present in all 12, nothing else in the
            // 762-docx corpus) — never the CS: line (the six G / O modules have none).
            if (this._isActivityTableDoc(content)) {
                lines.push(OutputFormatter.ACTIVITY_TABLE_NOTICE.message);
            } else {
                lines.push('⚠ [TITLE BAR] marker not found. Showing all extracted content.');
            }
        }

        lines.push('');

        for (let i = startIndex; i < content.length; i++) {
            const block = content[i];

            // Additive (comment capture): emit any captured comment notes
            // immediately before the block they were anchored/matched to, once
            // per block and in order. Blocks without notes are unaffected, so the
            // existing output contract is preserved.
            if (block.commentNotes && block.commentNotes.length) {
                for (let n = 0; n < block.commentNotes.length; n++) {
                    lines.push(block.commentNotes[n]);
                }
                lines.push('');
            }

            if (block.type === 'paragraph') {
                const formatted = this.formatParagraph(block.data);
                if (formatted !== null) {
                    lines.push(formatted);
                    lines.push(''); // blank line between paragraphs
                }
            } else if (block.type === 'table') {
                const formatted = this.formatTable(block.data);
                lines.push(formatted);
                lines.push('');
            } else if (block.type === 'pageBreak') {
                // Page breaks stripped — no useful info for downstream processing
            }
        }

        return lines.join('\n').replace(/\n{3,}/g, '\n\n');
    }

    /**
     * Format a single paragraph object.
     * Returns null for completely empty paragraphs.
     */
    formatParagraph(para) {
        if (!para.runs || para.runs.length === 0) {
            // Skip empty paragraphs
            if (!para.text || para.text.trim() === '') {
                return null;
            }
        }

        let text = '';

        // Process runs with inline formatting
        for (let i = 0; i < para.runs.length; i++) {
            const run = para.runs[i];
            let chunk = run.text;

            if (!chunk) continue;

            // A converted Word equation. Its text is already MathML, so it goes
            // through untouched: no bold/italic markers, no whitespace trim, no
            // hyperlink suffix — every one of those would corrupt the markup.
            if (run.isMath) {
                text += chunk;
                continue;
            }

            const fmt = run.formatting || {};

            // Red text wrapping (takes priority)
            if (fmt.isRed) {
                chunk = this.wrapRedText(chunk);
            } else {
                // Apply formatting markers
                chunk = this._applyFormatting(chunk, fmt);

                // Yellow highlight marker (correct answer indicator)
                if (fmt.highlight === 'yellow') {
                    chunk = '\u2705' + chunk;
                }
            }

            // Hyperlink
            if (run.hyperlink) {
                // If the link text IS the URL (or close to it), just show URL
                const linkText = run.text.trim();
                if (linkText === run.hyperlink || linkText.replace(/\s/g, '') === run.hyperlink) {
                    chunk = run.hyperlink;
                } else {
                    chunk = chunk + ' [LINK: ' + run.hyperlink + ']';
                }
            }

            text += chunk;
        }

        // Skip if all whitespace after processing
        if (!text || text.trim() === '') {
            return null;
        }

        // List item formatting
        if (para.isListItem) {
            const indent = '  '.repeat(para.listLevel || 0);
            const isOrdered = para.listFormat && (
                para.listFormat === 'decimal' ||
                para.listFormat === 'lowerLetter' ||
                para.listFormat === 'upperLetter' ||
                para.listFormat === 'lowerRoman' ||
                para.listFormat === 'upperRoman'
            );

            if (isOrdered) {
                // Track list counters per numId for correct numbering
                var numId = para.listNumId || 'default';
                if (!this._listCounters) this._listCounters = {};
                if (!this._listCounters[numId]) this._listCounters[numId] = 0;
                this._listCounters[numId]++;
                var count = this._listCounters[numId];

                if (para.listFormat === 'lowerLetter') {
                    text = indent + String.fromCharCode(96 + count) + '. ' + text;
                } else if (para.listFormat === 'upperLetter') {
                    text = indent + String.fromCharCode(64 + count) + '. ' + text;
                } else {
                    text = indent + count + '. ' + text;
                }
                this._lastListNumId = numId;
            } else {
                text = indent + '\u2022 ' + text;
            }
        } else {
            // Reset counters when we leave a list context
            if (this._lastListNumId) {
                this._lastListNumId = null;
            }
        }

        return text;
    }

    /**
     * Apply bold/italic/underline formatting markers to text.
     */
    _applyFormatting(text, fmt) {
        if (!text.trim()) return text;

        // Preserve leading/trailing whitespace
        const leadMatch = text.match(/^(\s*)/);
        const trailMatch = text.match(/(\s*)$/);
        const leading = leadMatch ? leadMatch[1] : '';
        const trailing = trailMatch ? trailMatch[1] : '';
        const inner = text.trim();

        if (!inner) return text;

        let result = inner;

        if (fmt.bold && fmt.italic) {
            result = '***' + result + '***';
        } else if (fmt.bold) {
            result = '**' + result + '**';
        } else if (fmt.italic) {
            result = '*' + result + '*';
        }

        if (fmt.underline) {
            result = '__' + result + '__';
        }

        if (fmt.strikethrough) {
            result = '~~' + result + '~~';
        }

        return leading + result + trailing;
    }

    /**
     * Strip red text markers that wrap only whitespace.
     * e.g. "🔴[RED TEXT]   [/RED TEXT]🔴" → removed entirely.
     */
    _stripEmptyRedText(text) {
        return text.replace(/\uD83D\uDD34\[RED TEXT\]\s*\[\/RED TEXT\]\uD83D\uDD34/g, '');
    }

    /**
     * Wrap text in PageForge's parsed-.txt RED-TEXT marker. Single source of
     * truth for the marker (U+1F534 \uD83D\uDD34) so additive features \u2014 e.g. the Word
     * comment notes \u2014 reuse the exact convention rather than re-inventing it.
     * The bytes match _stripEmptyRedText's regex.
     * @param {string} text
     * @returns {string}
     */
    wrapRedText(text) {
        return '\uD83D\uDD34[RED TEXT] ' + text + ' [/RED TEXT]\uD83D\uDD34';
    }

    /**
     * Format a table into ASCII art.
     */
    formatTable(table) {
        if (!table.rows || table.rows.length === 0) {
            return '';
        }

        const lines = [];
        lines.push('\u250C\u2500\u2500\u2500 TABLE \u2500\u2500\u2500');

        for (let r = 0; r < table.rows.length; r++) {
            const row = table.rows[r];
            const cellTexts = [];
            // Nested tables found in this row, emitted directly beneath it so
            // that reading order is preserved and the row line itself is
            // unchanged (a table with no nested table is byte-identical to the
            // pre-fix output).
            const nestedBlocks = [];

            for (let c = 0; c < row.cells.length; c++) {
                const cell = row.cells[c];
                const cellContent = [];

                for (let p = 0; p < cell.paragraphs.length; p++) {
                    const para = cell.paragraphs[p];

                    if (para && para.nestedTable) {
                        nestedBlocks.push({ cell: c + 1, table: para.nestedTable });
                        continue;
                    }

                    const formatted = this.formatParagraph(para);
                    if (formatted !== null) {
                        cellContent.push(formatted);
                    }
                }

                cellTexts.push(cellContent.join(' / '));
            }

            lines.push('\u2502 ' + cellTexts.join(' \u2551 '));

            for (let n = 0; n < nestedBlocks.length; n++) {
                lines.push.apply(lines, this._formatNestedTable(
                    nestedBlocks[n].table, r + 1, nestedBlocks[n].cell
                ));
            }
        }

        lines.push('\u2514\u2500\u2500\u2500 END TABLE \u2500\u2500\u2500');
        return lines.join('\n');
    }

    /**
     * Format a table that sits inside a cell of another table.
     *
     * Returned as an indented block of lines carrying the parent row/cell it
     * belongs to, so a writer's quiz grid or vocabulary table nested inside a
     * layout cell reads in its proper place. Recurses, so a table nested inside
     * a nested table is handled too.
     */
    _formatNestedTable(table, parentRow, parentCell) {
        const out = [];
        const label = ' (in row ' + parentRow + ', cell ' + parentCell + ') ';
        out.push('\u2502 \u250c\u2500\u2500\u2500 NESTED TABLE' + label + '\u2500\u2500\u2500');

        if (table && table.rows && table.rows.length) {
            const inner = this.formatTable(table).split('\n');
            // Drop the recursive call's own TABLE / END TABLE frame; this block
            // supplies its own, labelled with the parent position. A cell whose
            // text carries a line break of its own arrives here as a line with
            // no frame character, so it is indented to stay inside the block.
            for (let i = 1; i < inner.length - 1; i++) {
                out.push(inner[i].charAt(0) === '\u2502' ? '\u2502 ' + inner[i] : '\u2502 \u2502   ' + inner[i]);
            }
        }

        out.push('\u2502 \u2514\u2500\u2500\u2500 END NESTED TABLE \u2500\u2500\u2500');
        return out;
    }
}
