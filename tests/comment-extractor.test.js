/**
 * Tests for CommentExtractor — comments.xml body parsing, anchor/rowUrl helpers
 * and carry-forward (spec §6.1). Pure string/array operations, headless.
 */

'use strict';

(function () {
    var ex = new CommentExtractor();

    describe('CommentExtractor — parseComments (word/comments.xml)', function () {
        var xml =
            '<w:comments xmlns:w="x">' +
            // attribute order varies (author before id), multiple <w:t> runs
            '<w:comment w:author="Nadia Stanton" w:id="0" w:date="d">' +
            '<w:p><w:r><w:t>Replace with </w:t></w:r><w:r><w:t>iStock.</w:t></w:r></w:p></w:comment>' +
            // entities + dot-form author
            '<w:comment w:id="1" w:author="Kate.Scanlon">' +
            '<w:p><w:r><w:t xml:space="preserve">Used &amp; noted &lt;ok&gt;</w:t></w:r></w:p></w:comment>' +
            '</w:comments>';

        it('returns a Map keyed by comment id', function () {
            var m = ex.parseComments(xml);
            assertEqual(m.size, 2, 'two comments parsed');
        });

        it('joins all inner <w:t> runs and collapses whitespace', function () {
            var m = ex.parseComments(xml);
            assertEqual(m.get('0').text, 'Replace with iStock.', 'runs joined + collapsed');
        });

        it('decodes the author and XML entities in the text (order-independent attrs)', function () {
            var m = ex.parseComments(xml);
            assertEqual(m.get('0').author, 'Nadia Stanton', 'author when it precedes id');
            assertEqual(m.get('1').author, 'Kate.Scanlon', 'dot-form author preserved verbatim');
            assertEqual(m.get('1').text, 'Used & noted <ok>', 'entities decoded');
        });

        it('returns an empty map for null / empty input', function () {
            assertEqual(ex.parseComments(null).size, 0, 'null');
            assertEqual(ex.parseComments('').size, 0, 'empty');
        });
    });

    describe('CommentExtractor — anchor + rowUrl helpers', function () {
        it('finds commentRangeStart ids in an XML chunk', function () {
            var xml = '<w:p><w:commentRangeStart w:id="0"/>text<w:commentRangeStart w:id="3"/></w:p>';
            assertDeepEqual(ex.anchorIdsInXml(xml), ['0', '3'], 'ids in document order');
        });

        it('resolves a table row hyperlink to its target URL via the rels map', function () {
            var rowXml = '<w:tr><w:tc><w:hyperlink r:id="rId7"><w:r><w:t>img</w:t></w:r></w:hyperlink></w:tc></w:tr>';
            var rels = { rId7: 'https://media.istockphoto.com/id/1382010801/photo.jpg' };
            assertDeepEqual(ex.rowUrlsFromXml(rowXml, rels),
                ['https://media.istockphoto.com/id/1382010801/photo.jpg'], 'rowUrl resolved');
        });

        it('returns no rowUrl when the row has no resolvable hyperlink', function () {
            assertDeepEqual(ex.rowUrlsFromXml('<w:tr><w:tc/></w:tr>', {}), [], 'no hyperlink → empty');
        });
    });

    describe('CommentExtractor — carry-forward (§6.1)', function () {
        function para(text, comments) {
            var b = { type: 'paragraph', data: { text: text } };
            if (comments) { b.comments = comments; }
            return b;
        }

        it('moves a comment off an empty paragraph onto the next kept block', function () {
            var c = { author: 'Simon Vita', text: 'Please fix' };
            var content = [para('', [c]), para('Body text')];
            ex.applyCarryForward(content);
            assertTrue(!content[0].comments || content[0].comments.length === 0, 'origin cleared');
            assertEqual(content[1].comments.length, 1, 'attached to next kept block');
            assertEqual(content[1].comments[0], c, 'same comment object');
        });

        it('attaches a trailing comment (no kept block after it) to the last block', function () {
            var c = { author: 'Kate Scanlon', text: 'Please review' };
            var content = [para('Body text'), para('', [c])];
            ex.applyCarryForward(content);
            assertEqual(content[0].comments.length, 1, 'trailing comment → last renderable block');
            assertEqual(content[0].comments[0], c, 'same comment object');
        });

        it('leaves comments on already-renderable blocks in place', function () {
            var c = { author: 'Nadia Stanton', text: 'Replace' };
            var content = [para('Body', [c])];
            ex.applyCarryForward(content);
            assertEqual(content[0].comments.length, 1, 'untouched');
        });

        it('treats a table as renderable (image-only / media rows kept)', function () {
            assertTrue(CommentExtractor.isRenderableBlock({ type: 'table', data: {} }), 'table renderable');
            assertFalse(CommentExtractor.isRenderableBlock({ type: 'paragraph', data: { text: '   ' } }),
                'whitespace paragraph not renderable');
        });
    });
})();
