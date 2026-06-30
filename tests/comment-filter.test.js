/**
 * Tests for CommentFilter — the Word-comment whitelist/normalisation and the
 * asymmetric actionable-vs-boilerplate filter (spec §6.2–§6.3). Validated against
 * the REAL shipped data/comment-authors.json (exposed as COMMENT_AUTHORS_DATA).
 */

'use strict';

(function () {
    var DATA = global.COMMENT_AUTHORS_DATA;

    function filter(overrides) {
        var data = JSON.parse(JSON.stringify(DATA));
        if (overrides) {
            for (var k in overrides) { data[k] = overrides[k]; }
        }
        return new CommentFilter(data);
    }

    describe('CommentFilter — data file loads', function () {
        it('the canonical data file was found and parsed', function () {
            assertNotNull(DATA, 'COMMENT_AUTHORS_DATA available to tests');
            assertEqual(DATA.authors.length, 6, 'six whitelisted authors');
        });
    });

    describe('CommentFilter — author normalisation + whitelist (§6.2)', function () {
        it('resolves the six authors from their real-world variants', function () {
            var f = filter();
            assertEqual(f.resolveAuthor('Kate.Scanlon'), 'Kate Scanlon', 'dot/username form');
            assertEqual(f.resolveAuthor('Kate Scanlon [2]'), 'Kate Scanlon', 'trailing [N] disambiguator');
            assertEqual(f.resolveAuthor('caroline schwer'), 'Caroline Schwer', 'lower-case');
            assertEqual(f.resolveAuthor('SIMON  VITA'), 'Simon Vita', 'caps + double space');
            assertEqual(f.resolveAuthor('amanda griffiths'), 'Amanda Griffiths', 'lower-case');
            assertEqual(f.resolveAuthor('Creative Services'), 'Creative Services', 'exact');
        });

        it('accepts reversed "Last First" order', function () {
            var f = filter();
            assertEqual(f.resolveAuthor('Stanton Nadia'), 'Nadia Stanton', 'reversed name order');
            assertEqual(f.resolveAuthor('Scanlon, Kate'.replace(',', '')), 'Kate Scanlon', 'reversed (comma stripped)');
        });

        it('always returns the canonical display name, not the input form', function () {
            assertEqual(filter().resolveAuthor('kate.scanlon'), 'Kate Scanlon');
        });

        it('rejects non-whitelisted authors and empty input', function () {
            var f = filter();
            assertNull(f.resolveAuthor('Random Writer'), 'non-whitelisted dropped');
            assertNull(f.resolveAuthor('Microsoft Office User'), 'generic Office name dropped');
            assertNull(f.resolveAuthor(''), 'empty dropped');
            assertNull(f.resolveAuthor(null), 'null dropped');
        });

        it('honours a per-author enable flag and the master switch', function () {
            var off = filter();
            off.data.authors[0].enabled = false; // Kate Scanlon
            assertNull(off.resolveAuthor('Kate.Scanlon'), 'disabled author dropped');
            assertEqual(off.resolveAuthor('simon vita'), 'Simon Vita', 'others unaffected');

            var master = filter({ enabled: false });
            assertNull(master.resolveAuthor('Creative Services'), 'master off → nothing resolves');
        });
    });

    describe('CommentFilter — asymmetric content filter (§6.3)', function () {
        it('drops pure copyright/permission boilerplate', function () {
            var f = filter();
            assertTrue(f.isOmittable('Used with permission.'), 'used with permission');
            assertTrue(f.isOmittable("Infographic 'Moving on', copyright © Interactionz. Used with permission."),
                '© + used with permission');
            assertTrue(f.isOmittable('Te Kura created.'), 'Te Kura created');
            assertTrue(f.isOmittable('link'), 'bare link');
            assertTrue(f.isOmittable('All iStock.'), 'all iStock');
        });

        it('KEEPS a note that mixes boilerplate with an action signal', function () {
            var f = filter();
            assertFalse(f.isOmittable('Replace with iStock image if possible, otherwise - Used with permission.'),
                'action signal (replace) wins over boilerplate');
        });

        it('keeps actionable designer instructions', function () {
            var f = filter();
            assertFalse(f.isOmittable('Designer to recreate.'), 'designer to / recreate');
            assertFalse(f.isOmittable('Please crop this image.'), 'please / crop');
            assertFalse(f.isOmittable('Can you embed this video?'), 'can you / embed / trailing ?');
            assertFalse(f.isOmittable('Is this the right one?'), 'trailing question mark alone');
        });

        it('disabling the content filter omits nothing (surface all)', function () {
            var f = filter();
            f.data.content_filter.enabled = false;
            f._omitRe = undefined; f._keepRe = undefined; // reset lazy cache
            assertFalse(f.isOmittable('Used with permission.'), 'filter off → keep boilerplate too');
        });
    });

    describe('CommentFilter — combined decision', function () {
        it('surfaces only whitelisted + actionable comments', function () {
            var f = filter();
            var a = f.decide('Nadia Stanton', 'Replace with iStock.');
            assertTrue(a.surface, 'whitelisted + actionable surfaces');
            assertEqual(a.author, 'Nadia Stanton', 'canonical author returned');

            var b = f.decide('Nadia Stanton', 'Used with permission.');
            assertFalse(b.surface, 'whitelisted but boilerplate → dropped');

            var c = f.decide('Random Writer', 'Please replace this.');
            assertFalse(c.surface, 'actionable but non-whitelisted → dropped');
        });
    });
})();
