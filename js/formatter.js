/**
 * OutputFormatter — Converts parsed DocxParser output into structured
 * plain text for display, clipboard copy, and file download.
 */

'use strict';

class OutputFormatter {

    /**
     * Format everything: metadata header + content.
     * @param {Object} parserResult - Result from DocxParser.parse()
     * @returns {{ full: string, metadataOnly: string, contentOnly: string }}
     */
    formatAll(parserResult) {
        const metadataBlock = this.formatMetadata(parserResult.metadata);
        const contentBlock = this.formatContent(
            parserResult.content,
            parserResult.contentStartIndex,
            parserResult.contentStartFound
        );

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

        lines.push('');
        lines.push('--- CONTENT START ---');

        if (!startFound) {
            lines.push('');
            lines.push('⚠ [TITLE BAR] marker not found. Showing all extracted content.');
        }

        lines.push('');

        for (let i = startIndex; i < content.length; i++) {
            const block = content[i];

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
                lines.push('--- PAGE BREAK ---');
                lines.push('');
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

            const fmt = run.formatting || {};

            // Red text wrapping (takes priority)
            if (fmt.isRed) {
                chunk = '\uD83D\uDD34[RED TEXT] ' + chunk + ' [/RED TEXT]\uD83D\uDD34';
            } else {
                // Apply formatting markers
                chunk = this._applyFormatting(chunk, fmt);
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
                // For ordered lists, we'd need counters — use a simple marker
                text = indent + '1. ' + text;
            } else {
                text = indent + '\u2022 ' + text;
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

            for (let c = 0; c < row.cells.length; c++) {
                const cell = row.cells[c];
                const cellContent = [];

                for (let p = 0; p < cell.paragraphs.length; p++) {
                    const formatted = this.formatParagraph(cell.paragraphs[p]);
                    if (formatted !== null) {
                        cellContent.push(formatted);
                    }
                }

                cellTexts.push(cellContent.join(' / '));
            }

            lines.push('\u2502 ' + cellTexts.join(' \u2551 '));
        }

        lines.push('\u2514\u2500\u2500\u2500 END TABLE \u2500\u2500\u2500');
        return lines.join('\n');
    }
}
