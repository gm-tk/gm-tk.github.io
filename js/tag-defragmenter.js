/**
 * TagDefragmenter — Word-XML red-text fragmentation handling.
 *
 * Extracted from `TagNormaliser` (Session 1 of the tag-pipeline audit series).
 *
 * Owns two passes that repair tags split across Word XML formatting runs:
 *
 *   1. `defragmentRawText(text)` — Phase 1 Patch pre-processor that strips
 *      redundant `[/RED TEXT]🔴…🔴[RED TEXT]` boundary pairs and cleans up
 *      whitespace inside square brackets. Called as Step 0 of
 *      `TagNormaliser.processBlock()`.
 *   2. `reassembleFragmentedTags(text)` — Multi-way merge pass that joins
 *      adjacent red-text markers whose combined content spells out a valid
 *      `[tag]` (handles the "speech bubble" split-across-italic cases).
 *
 * @see CLAUDE.md Section 10 — Tag Taxonomy & Normalisation
 * @see docs/18-tag-normalisation-patch.md (Phase 1 Patch)
 */

'use strict';

class TagDefragmenter {
    /**
     * Pre-process raw text to de-fragment fractured red-text boundaries
     * caused by Microsoft Word splitting a single tag across multiple
     * XML formatting runs.
     *
     * Handles three classes of artifact:
     * 1. Redundant close/re-open boundaries:
     *    `[/RED TEXT]🔴` + whitespace + `🔴[RED TEXT]` → stripped
     * 2. Multiple spaces inside square brackets: collapsed to single space
     * 3. Leading/trailing spaces inside square brackets: trimmed
     *
     * @param {string} text - Raw text content potentially with fractured markers
     * @returns {string} Cleaned text with fractured boundaries stitched
     */
    defragmentRawText(text) {
        if (!text || typeof text !== 'string') return text;

        // 1. Stitch fractured red-text boundaries:
        //    [/RED TEXT]🔴 <whitespace> 🔴[RED TEXT] → removed
        text = text.replace(
            /\[\/RED TEXT\]\uD83D\uDD34\s*\uD83D\uDD34\[RED TEXT\]/g,
            ''
        );

        // 2. Collapse multiple spaces inside square brackets to single space
        text = text.replace(/\[([^\]]+)\]/g, function(match, inner) {
            var cleaned = inner.replace(/\s{2,}/g, ' ');
            return '[' + cleaned + ']';
        });

        // 3. Trim leading/trailing whitespace inside square brackets
        //    e.g. [ tags ] → [tags], [ H2 ] → [H2]
        text = text.replace(/\[\s+([^\]]*?)\s*\]/g, function(match, inner) {
            return '[' + inner.trim() + ']';
        });
        // Also handle trailing-only: [tags ] → [tags]
        text = text.replace(/\[([^\]]*?)\s+\]/g, function(match, inner) {
            return '[' + inner.trim() + ']';
        });

        return text;
    }

    /**
     * Reassemble fragmented red-text tags that were split across multiple
     * Word formatting runs.
     *
     * When a writer types [speech bubble] in red but Word splits it across
     * two XML runs (e.g., one with italic, one without), the parser outputs:
     *   🔴[RED TEXT] [ [/RED TEXT]🔴🔴[RED TEXT] speech bubble] [/RED TEXT]🔴
     * This method detects such adjacent markers and merges them when their
     * combined content forms a valid [tag] pattern.
     *
     * @param {string} text - Text with red-text markers
     * @returns {string} Text with fragmented tags reassembled
     */
    reassembleFragmentedTags(text) {
        if (!text || typeof text !== 'string') return text;

        // Use a non-trimming regex to preserve inner whitespace for reassembly
        var redMarkerRe = /\uD83D\uDD34\[RED TEXT\]([\s\S]*?)\[\/RED TEXT\]\uD83D\uDD34/g;

        // Collect all red-text markers and their positions
        var markers = [];
        var match;
        while ((match = redMarkerRe.exec(text)) !== null) {
            markers.push({
                fullMatch: match[0],
                innerContent: match[1],  // preserves original whitespace
                innerTrimmed: match[1].trim(),
                startIndex: match.index,
                endIndex: match.index + match[0].length
            });
        }

        if (markers.length < 2) return text;

        // Scan for consecutive markers that should be merged
        var merges = [];

        for (var i = 0; i < markers.length - 1; i++) {
            // Skip markers already consumed by a merge
            var alreadyConsumed = false;
            for (var mc = 0; mc < merges.length; mc++) {
                if (i >= merges[mc].startIdx && i <= merges[mc].endIdx) {
                    alreadyConsumed = true;
                    break;
                }
            }
            if (alreadyConsumed) continue;

            // Try merging N consecutive markers (4, 3, 2) — longest match first
            var maxLookahead = Math.min(markers.length - i, 6); // up to 6-way merge

            var merged = false;
            for (var span = maxLookahead; span >= 2; span--) {
                if (i + span - 1 >= markers.length) continue;

                // Check all gaps between markers are empty
                var allGapsEmpty = true;
                for (var g = 0; g < span - 1; g++) {
                    var gap = text.substring(markers[i + g].endIndex, markers[i + g + 1].startIndex).trim();
                    if (gap !== '') {
                        allGapsEmpty = false;
                        break;
                    }
                }

                if (!allGapsEmpty) continue;

                // Concatenate all inner contents preserving original whitespace
                var parts = [];
                for (var c = 0; c < span; c++) {
                    parts.push(markers[i + c].innerContent);
                }
                // Direct concatenation preserves original spacing
                // (e.g., "[End " + "tab]" = "[End tab]")
                // Then normalise multiple spaces to single
                var combined = parts.join('').replace(/\s+/g, ' ').trim();

                // Check if combined text contains or forms a valid tag
                var tagMatch = combined.match(/\[([^\]]+)\]/);
                // Also check if it contains an incomplete bracket that would complete
                var hasOpenBracket = combined.indexOf('[') !== -1;
                var hasCloseBracket = combined.indexOf(']') !== -1;

                if (tagMatch || (hasOpenBracket && hasCloseBracket)) {
                    merges.push({
                        startIdx: i,
                        endIdx: i + span - 1,
                        replacement: '\uD83D\uDD34[RED TEXT] ' + combined + ' [/RED TEXT]\uD83D\uDD34'
                    });
                    merged = true;
                    break;
                }
            }

            // If no multi-way merge worked, skip to next marker
        }

        // Apply merges in reverse order so indices don't shift
        for (var m = merges.length - 1; m >= 0; m--) {
            var merge = merges[m];
            var startPos = markers[merge.startIdx].startIndex;
            var endPos = markers[merge.endIdx].endIndex;
            text = text.substring(0, startPos) + merge.replacement + text.substring(endPos);
        }

        return text;
    }
}
