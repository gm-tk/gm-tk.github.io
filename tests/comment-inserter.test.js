/**
 * Tests for CommentInserter — media keys, body + media-match placement, the
 * guards, the media-only fallback, and an end-to-end pass through the real
 * OutputFormatter (spec §6.3–§6.4, §6.6).
 */

'use strict';

(function () {
    var DATA = global.COMMENT_AUTHORS_DATA;

    function inserter() {
        return new CommentInserter({
            filter: new CommentFilter(DATA),
            formatter: new OutputFormatter(),
            mediaMatch: DATA.media_match
        });
    }
    function paraBlock(text, hyperlink) {
        return {
            type: 'paragraph',
            data: { runs: [{ text: text, formatting: {}, hyperlink: hyperlink || null }], text: text, isListItem: false }
        };
    }
    function tableBlock(url, comments) {
        var b = {
            type: 'table',
            data: { rows: [{ cells: [{ paragraphs: [{ runs: [{ text: 'img', hyperlink: url }], text: 'img' }] }] }] }
        };
        if (comments) { b.comments = comments; }
        return b;
    }
    var RED = '🔴[RED TEXT] ';

    describe('CommentInserter — media keys (§6.4)', function () {
        it('extracts the iStock id from the gm- form and the /id/ CDN form', function () {
            var ins = inserter();
            assert(ins.mediaKeys('https://www.istockphoto.com/photo/x-gm1382010801-17', true)
                .indexOf('istock:1382010801') !== -1, 'gm- form');
            assert(ins.mediaKeys('https://media.istockphoto.com/id/1382010801/photo.jpg', true)
                .indexOf('istock:1382010801') !== -1, '/id/ form');
        });
        it('extracts the YouTube id from share, watch and embed forms', function () {
            var ins = inserter();
            assert(ins.mediaKeys('https://youtu.be/dQw4w9WgXcQ', true).indexOf('yt:dQw4w9WgXcQ') !== -1, 'youtu.be');
            assert(ins.mediaKeys('https://www.youtube.com/watch?v=dQw4w9WgXcQ', true).indexOf('yt:dQw4w9WgXcQ') !== -1, 'watch?v=');
            assert(ins.mediaKeys('https://www.youtube.com/embed/dQw4w9WgXcQ', true).indexOf('yt:dQw4w9WgXcQ') !== -1, 'embed');
        });
        it('always includes the exact URL; id_match:false drops the id keys', function () {
            var ins = inserter();
            var url = 'https://media.istockphoto.com/id/1382010801/x.jpg';
            assert(ins.mediaKeys(url, true).indexOf(url) !== -1, 'exact url present');
            assertDeepEqual(ins.mediaKeys(url, false), [url], 'id_match off → exact url only');
        });
    });

    describe('CommentInserter — body placement (§6.4)', function () {
        it('attaches a surviving body comment as a red note, once, before its block', function () {
            var blk = paraBlock('Body line');
            blk.comments = [{ author: 'Simon Vita', text: 'Please fix this' }];
            var s = inserter().captureIntoTemplate({ content: [blk] }, []);
            assertEqual(s.body, 1, 'one body comment placed');
            assertEqual(blk.commentNotes.length, 1, 'one note attached to the block');
            assert(blk.commentNotes[0].indexOf(RED + 'Note from Simon Vita: Please fix this') === 0, 'red note, "Note from {author}:" prefixed');
        });

        it('prefixes every whitelisted author with "Note from {author}:"', function () {
            var ins = inserter();
            assert(ins.renderNote('Creative Services', 'use the Chrome logo').indexOf(RED + 'Note from Creative Services: use the Chrome logo') === 0,
                'Creative Services → "Note from Creative Services:"');
            assert(ins.renderNote('Simon Vita', 'Comment goes here').indexOf('Note from Simon Vita: Comment goes here') !== -1,
                'Simon Vita → "Note from Simon Vita:"');
        });

        it('emits all of a block\'s comments once, in order', function () {
            var blk = paraBlock('Body');
            blk.comments = [
                { author: 'Kate Scanlon', text: 'Please replace A' },
                { author: 'Nadia Stanton', text: 'Please crop B' }
            ];
            inserter().captureIntoTemplate({ content: [blk] }, []);
            assertEqual(blk.commentNotes.length, 2, 'both notes once');
            assert(blk.commentNotes[0].indexOf('Kate Scanlon') !== -1, 'order preserved (1st)');
            assert(blk.commentNotes[1].indexOf('Nadia Stanton') !== -1, 'order preserved (2nd)');
        });

        it('drops boilerplate and non-whitelisted body comments', function () {
            var blk = paraBlock('Body');
            blk.comments = [
                { author: 'Nadia Stanton', text: 'Used with permission.' },
                { author: 'Random Writer', text: 'Please replace this' }
            ];
            var s = inserter().captureIntoTemplate({ content: [blk] }, []);
            assertEqual(s.body, 0, 'neither surfaces');
            assert(!blk.commentNotes, 'no notes attached');
        });
    });

    describe('CommentInserter — media match (§6.4)', function () {
        it('matches a Media List comment to the body element by iStock id (cross-form)', function () {
            var body = paraBlock('See the picture', 'https://www.istockphoto.com/photo/x-gm1382010801-17');
            var ext = [{ author: 'Nadia Stanton', text: 'Replace this image', rowUrl: 'https://media.istockphoto.com/id/1382010801/p.jpg' }];
            var s = inserter().captureIntoTemplate({ content: [body] }, ext);
            assertEqual(s.media, 1, 'matched once by shared iStock id');
            assert(body.commentNotes && body.commentNotes[0].indexOf('Nadia Stanton: Replace this image') !== -1,
                'note before the body element using the same media');
        });

        it('matches by YouTube id and prefixes the author', function () {
            var body = paraBlock('Watch this', 'https://youtu.be/dQw4w9WgXcQ');
            var ext = [{ author: 'Simon Vita', text: 'Please embed the captioned version', rowUrls: ['https://www.youtube.com/watch?v=dQw4w9WgXcQ'] }];
            var s = inserter().captureIntoTemplate({ content: [body] }, ext);
            assertEqual(s.media, 1, 'matched once by shared YouTube id');
            assert(body.commentNotes && body.commentNotes[0].indexOf('Simon Vita: Please embed the captioned version') !== -1,
                'author-prefixed note placed before the video element');
        });

        it('surfaces a media comment once even if several body elements use it', function () {
            var b1 = paraBlock('first use', 'https://media.istockphoto.com/id/55555555/a.jpg');
            var b2 = paraBlock('second use', 'https://media.istockphoto.com/id/55555555/a.jpg');
            var ext = [{ author: 'Caroline Schwer', text: 'Please resize', rowUrl: 'https://media.istockphoto.com/id/55555555/a.jpg' }];
            var s = inserter().captureIntoTemplate({ content: [b1, b2] }, ext);
            assertEqual(s.media, 1, 'surfaced once');
            assert(b1.commentNotes && b1.commentNotes.length === 1, 'on the first matching element');
            assert(!b2.commentNotes, 'not repeated on the second');
        });

        it('never surfaces a media comment against its own anchor block (self-match guard)', function () {
            var url = 'https://media.istockphoto.com/id/66666666/a.jpg';
            var anchor = tableBlock(url, [{ author: 'Nadia Stanton', text: 'Please replace', rowUrl: url }]);
            var body = paraBlock('uses the same image', url);
            var s = inserter().captureIntoTemplate({ content: [anchor, body] }, []);
            assertEqual(s.media, 1, 'placed once, on the other element');
            assert(!anchor.commentNotes, 'not on its own anchor row');
            assert(body.commentNotes && body.commentNotes.length === 1, 'on the body element instead');
        });

        it('reports unplaced media comments (no body element uses the media)', function () {
            var body = paraBlock('unrelated', 'https://example.com/other.jpg');
            var ext = [{ author: 'Nadia Stanton', text: 'Please replace', rowUrl: 'https://media.istockphoto.com/id/77777777/a.jpg' }];
            var s = inserter().captureIntoTemplate({ content: [body] }, ext);
            assertEqual(s.media, 0, 'nothing matched');
            assertEqual(s.unplacedMedia.length, 1, 'reported as unplaced');
        });
    });

    describe('CommentInserter — media-only fallback (§6.4)', function () {
        it('renders only surviving comments and a toast message', function () {
            var fb = inserter().renderMediaOnly([
                { author: 'Nadia Stanton', text: 'Replace with iStock' },
                { author: 'Random Writer', text: 'Please replace' },
                { author: 'Caroline Schwer', text: 'Used with permission.' }
            ]);
            assertEqual(fb.notes.length, 1, 'only the whitelisted + actionable one');
            assert(fb.notes[0].indexOf('Nadia Stanton: Replace with iStock') !== -1, 'author-prefixed red note');
            assert(fb.toast && fb.toast.length > 0, 'a toast message is produced');
        });

        it('produces no notes and no toast when nothing survives', function () {
            var fb = inserter().renderMediaOnly([{ author: 'Nadia Stanton', text: 'Used with permission.' }]);
            assertEqual(fb.notes.length, 0, 'no notes');
            assertEqual(fb.toast, '', 'no toast');
        });
    });

    describe('CommentInserter — end-to-end through OutputFormatter', function () {
        it('the red note appears immediately before the anchored block in the .txt', function () {
            var blk = paraBlock('The body line');
            blk.comments = [{ author: 'Simon Vita', text: 'Please fix' }];
            var wt = { content: [blk], contentStartIndex: 0, contentStartFound: true, metadata: {} };
            inserter().captureIntoTemplate(wt, []);
            var full = new OutputFormatter().formatAll(wt).full;
            var note = RED + 'Note from Simon Vita: Please fix [/RED TEXT]🔴';
            assert(full.indexOf(note) !== -1, 'note present in the .txt');
            assert(full.indexOf(note) < full.indexOf('The body line'), 'note precedes the block text');
        });
    });
})();
