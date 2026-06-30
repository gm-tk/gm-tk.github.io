/**
 * Tests for PageStitcher — the SPLIT-MODE reassembly (spec §8.3): a marker is
 * replaced by the correct section in order, missing/extra/duplicate reported,
 * the scaffold is untouched, and a full split→stitch round-trip is byte-faithful.
 */

'use strict';

(function () {
    function stitcher() { return new PageStitcher(); }

    function base(ids) {
        var markers = ids.map(function (id) { return '        <!-- PAGEFORGE-SPLICE id="' + id + '" -->'; }).join('\n');
        return '<!DOCTYPE html>\n<html lang="en" template="1-3" class="notranslate">\n<head><title>DEMO101</title>' +
            '<script src="https://tekura.desire2learn.com/x/idoc_scripts.js"></script></head>\n' +
            '<body class="inquiry container-fluid">\n' +
            '    <div id="header"><div id="module-code"><h1>DEMO101</h1></div><h1><span>Title</span></h1></div>\n' +
            '    <!-- colourlevel="1-3" -->\n' +
            '    <div id="body">\n' + markers + '\n    </div>\n' +
            '    <div id="footer"><ul class="footer-nav"><li class="home-nav"></li></ul></div>\n' +
            '</body>\n</html>';
    }
    function section(id, inner) {
        return {
            name: 'DEMO101__part-' + id + '.html',
            html: '<!-- PAGEFORGE-SECTION id="' + id + '" -->\n<!-- ' + id + ' -->\n' + inner + '\n<!-- /PAGEFORGE-SECTION -->'
        };
    }

    describe('PageStitcher — marker replacement + order', function () {
        it('replaces a single marker with its section content', function () {
            var r = stitcher().stitch(base(['01']), [section('01', '<div class="row"><p>Lesson one.</p></div>')]);
            assertTrue(r.ok, 'stitch ok: ' + r.errors.join(' '));
            assert(r.html.indexOf('<p>Lesson one.</p>') !== -1, 'section content spliced in');
            assert(r.html.indexOf('PAGEFORGE-SPLICE') === -1, 'no splice markers remain');
            assert(r.html.indexOf('PAGEFORGE-SECTION') === -1, 'no section markers remain');
        });

        it('places multiple sections in the base\'s slot order, regardless of upload order', function () {
            var sections = [
                section('03', '<div class="row"><p>three</p></div>'),
                section('01', '<div class="row"><p>one</p></div>'),
                section('02', '<div class="row"><p>two</p></div>')
            ];
            var r = stitcher().stitch(base(['01', '02', '03']), sections);
            assertTrue(r.ok, 'ok');
            var pOne = r.html.indexOf('<p>one</p>'), pTwo = r.html.indexOf('<p>two</p>'), pThree = r.html.indexOf('<p>three</p>');
            assert(pOne < pTwo && pTwo < pThree, 'sections appear in base slot order, not upload order');
            assertEqual(r.placements.length, 3, 'three placements');
        });
    });

    describe('PageStitcher — guards (never emit a broken file)', function () {
        it('reports a missing section for a slot', function () {
            var r = stitcher().stitch(base(['01', '02']), [section('01', '<p>x</p>')]);
            assertFalse(r.ok, 'not ok when a slot is unfilled');
            assertNull(r.html, 'no html emitted');
            assert(r.errors.join(' ').indexOf('Missing section for slot "02"') !== -1, 'names the missing slot');
        });
        it('reports an extra/orphan section with no matching slot', function () {
            var r = stitcher().stitch(base(['01']), [section('01', '<p>x</p>'), section('09', '<p>y</p>')]);
            assertFalse(r.ok, 'not ok with an orphan section');
            assert(r.errors.join(' ').indexOf('Extra section "09"') !== -1, 'names the orphan');
        });
        it('reports a duplicate section id', function () {
            var r = stitcher().stitch(base(['01']), [section('01', '<p>a</p>'), section('01', '<p>b</p>')]);
            assertFalse(r.ok, 'not ok with a duplicate section');
            assert(r.errors.join(' ').toLowerCase().indexOf('duplicate section') !== -1, 'flags the duplicate');
        });
        it('reports a base with no splice markers', function () {
            var r = stitcher().stitch('<html><body><div id="body"></div></body></html>', [section('01', '<p>x</p>')]);
            assertFalse(r.ok, 'not ok');
            assert(r.errors.join(' ').indexOf('No PAGEFORGE-SPLICE markers') !== -1, 'explains why');
        });
    });

    describe('PageStitcher — scaffold preserved', function () {
        it('leaves the header, footer and head includes untouched', function () {
            var r = stitcher().stitch(base(['01']), [section('01', '<p>content</p>')]);
            assert(r.html.indexOf('<div id="module-code"><h1>DEMO101</h1></div>') !== -1, 'header kept');
            assert(r.html.indexOf('<div id="footer">') !== -1, 'footer kept');
            assert(r.html.indexOf('idoc_scripts.js') !== -1, 'idoc include kept');
            assert(r.html.indexOf('template="1-3"') !== -1, '<html template> attr kept');
        });
    });

    describe('PageStitcher — strips manual-stitch GUIDE blocks', function () {
        var GS = '<!-- PAGEFORGE-GUIDE-START -->';
        var GE = '<!-- PAGEFORGE-GUIDE-END -->';

        it('removes GUIDE blocks (base + section) from the unified output, keeping real content', function () {
            var b =
                '<!DOCTYPE html>\n<html><head><title>G101</title></head>\n<body>\n' +
                '  <div id="header"><div id="module-code"><h1>G101</h1></div></div>\n' +
                '  <div id="body">\n' +
                '    ' + GS + '\n    <!-- MANUAL STITCH: replace the next marker with the lesson-01 file. -->\n    ' + GE + '\n' +
                '    <!-- PAGEFORGE-SPLICE id="01" -->\n' +
                '  </div>\n</body></html>';
            var sec = {
                name: 'G101-lesson-01.html',
                html: GS + '\n<!-- MANUAL STITCH: this is lesson 01; it fills the 01 splice point. -->\n' + GE + '\n' +
                      '<!-- PAGEFORGE-SECTION id="01" -->\n<!-- 1 -->\n<div class="row"><p>Lesson one.</p></div>\n<!-- /PAGEFORGE-SECTION -->'
            };
            var r = stitcher().stitch(b, [sec]);
            assertTrue(r.ok, 'stitch ok: ' + r.errors.join(' '));
            assert(r.html.indexOf('<p>Lesson one.</p>') !== -1, 'lesson content kept');
            assert(r.html.indexOf('<!-- 1 -->') !== -1, 'lesson delimiter comment kept');
            assert(r.html.indexOf('PAGEFORGE-GUIDE') === -1, 'no GUIDE sentinels remain');
            assert(r.html.indexOf('MANUAL STITCH') === -1, 'no manual-stitch guidance text remains');
            assert(r.html.indexOf('PAGEFORGE-SPLICE') === -1 && r.html.indexOf('PAGEFORGE-SECTION') === -1, 'no markers remain');
        });

        it('strips a GUIDE block whose text quotes a marker containing "-->" (no mis-detected slot)', function () {
            var b = '<div id="body">\n' +
                GS + '\n<!-- To stitch by hand, replace <!-- PAGEFORGE-SPLICE id="01" --> with the section content. -->\n' + GE + '\n' +
                '<!-- PAGEFORGE-SPLICE id="01" -->\n</div>';
            var r = stitcher().stitch(b, [section('01', '<p>x</p>')]);
            assertTrue(r.ok, 'ok despite the guide quoting a marker: ' + r.errors.join(' '));
            assertEqual(r.placements.length, 1, 'exactly one real slot detected (the quoted one was stripped first)');
            assert(r.html.indexOf('PAGEFORGE-GUIDE') === -1, 'guide stripped');
            assert(r.html.indexOf('stitch by hand') === -1, 'guidance text fully removed despite the nested -->');
            assert(r.html.indexOf('<p>x</p>') !== -1, 'section content present');
        });
    });

    describe('PageStitcher — parseSection precedence', function () {
        it('uses PAGEFORGE-SECTION markers when present', function () {
            var p = stitcher().parseSection('whatever.html', '<!-- PAGEFORGE-SECTION id="07" -->\n<p>z</p>\n<!-- /PAGEFORGE-SECTION -->');
            assertEqual(p.id, '07'); assertEqual(p.source, 'marker');
            assert(p.content.indexOf('<p>z</p>') !== -1);
        });
        it('falls back to a full page\'s #body inner', function () {
            var p = stitcher().parseSection('CODE__part-02.html', '<html><body><div id="body"><div class="row">B</div></div></body></html>');
            assertEqual(p.id, '02', 'id from filename'); assertEqual(p.source, 'body');
            assert(p.content.indexOf('<div class="row">B</div>') !== -1, '#body inner extracted');
        });
        it('falls back to the whole fragment with id from filename', function () {
            var p = stitcher().parseSection('X-03.html', '<div class="row">frag</div>');
            assertEqual(p.id, '03'); assertEqual(p.source, 'whole');
        });
        it('derives the module code from the base', function () {
            assertEqual(stitcher().moduleCode(base(['01']), 'DEMO101__BASE.html'), 'DEMO101');
        });
    });

    // ---- split→stitch round-trip ------------------------------------------------
    // Emulates SPLIT MODE: split a single-page module's #body at its <!-- N -->
    // lesson comments into a base + section files, then stitch it back.
    function splitSinglePage(html) {
        var ps = new PageStitcher();
        var openM = /<div\b[^>]*\bid="body"[^>]*>/i.exec(html);
        var openEnd = openM.index + openM[0].length;
        // balanced close of #body
        var tagRe = /<div\b|<\/div>/ig; tagRe.lastIndex = openM.index;
        var depth = 0, mm, closeStart = -1;
        while ((mm = tagRe.exec(html)) !== null) {
            if (mm[0] === '</div>') { depth--; if (depth === 0) { closeStart = mm.index; break; } } else { depth++; }
        }
        var inner = html.slice(openEnd, closeStart);
        var prefix = html.slice(0, openEnd), suffix = html.slice(closeStart);
        var re = /<!--\s*(intro|\d+)\s*-->/ig, marks = [], m;
        while ((m = re.exec(inner)) !== null) { marks.push({ id: m[1].toLowerCase(), at: m.index }); }
        // Lossless: keep everything before the first lesson marker (shared page
        // scaffold, e.g. the crumbs nav) IN the base, and replace each lesson chunk
        // with a splice marker IN PLACE. Each chunk becomes a section file.
        var newInner = inner.slice(0, marks.length ? marks[0].at : inner.length);
        var sections = [], ids = [];
        for (var i = 0; i < marks.length; i++) {
            var from = marks[i].at, to = (i + 1 < marks.length) ? marks[i + 1].at : inner.length;
            var chunk = inner.slice(from, to);
            var id = marks[i].id;
            ids.push(id);
            newInner += '\n        <!-- PAGEFORGE-SPLICE id="' + id + '" -->';
            sections.push({ name: 'M__part-' + id + '.html', html: '<!-- PAGEFORGE-SECTION id="' + id + '" -->\n' + chunk + '\n<!-- /PAGEFORGE-SECTION -->' });
        }
        return { base: prefix + newInner + suffix, sections: sections, ids: ids };
    }
    // Compare on content modulo whitespace: the stitcher tidies section whitespace,
    // so we assert the non-whitespace content is preserved (this still catches real
    // content loss, e.g. a dropped crumbs nav).
    function norm(s) { return String(s).replace(/\s+/g, ''); }

    describe('PageStitcher — split→stitch round-trip', function () {
        var single =
            '<!DOCTYPE html>\n<html lang="en" template="1-3" class="notranslate">\n<head><title>RT101</title></head>\n' +
            '<body class="inquiry container-fluid">\n' +
            '    <div id="header"><div id="module-code"><h1>RT101</h1></div></div>\n' +
            '    <div id="body">\n' +
            '        <!-- Intro -->\n        <div class="row"><p>Welcome</p></div>\n' +
            '        <!-- 1 -->\n        <div class="row"><p>Lesson one</p></div><div class="activity"><p>do</p></div>\n' +
            '        <!-- 2 -->\n        <div class="row"><p>Lesson two</p></div>\n' +
            '    </div>\n' +
            '    <div id="footer"><ul class="footer-nav"></ul></div>\n</body>\n</html>';

        it('round-trips a synthetic single-page module byte-faithfully (normalised)', function () {
            var ps = new PageStitcher();
            var origInner = ps._extractBodyInner(single);
            var split = splitSinglePage(single);
            assertDeepEqual(split.ids, ['intro', '1', '2'], 'split at the lesson comments');
            var r = ps.stitch(split.base, split.sections);
            assertTrue(r.ok, 'stitch ok: ' + r.errors.join(' '));
            assert(r.html.indexOf('PAGEFORGE') === -1, 'no markers survive');
            assertEqual(norm(ps._extractBodyInner(r.html)), norm(origInner), '#body restored (normalised)');
            assert(r.html.indexOf('<div id="module-code"><h1>RT101</h1></div>') !== -1, 'header intact');
            assert(r.html.indexOf('<div id="footer">') !== -1, 'footer intact');
        });

        it('round-trips the real BLL210 corpus module (skips if corpus absent)', function () {
            if (typeof global.__readText !== 'function') { assert(true, 'no corpus accessor — skipped'); return; }
            var html = global.__readText(global.__corpusDir + '/01-Finalized_Modules_/Inquiry/BLL210/BLL210.html');
            if (!html) { assert(true, 'BLL210 not present — skipped'); return; }
            var ps = new PageStitcher();
            var origInner = ps._extractBodyInner(html);
            var split = splitSinglePage(html);
            assert(split.ids.length >= 2, 'BLL210 split into multiple lesson sections (' + split.ids.length + ')');
            var r = ps.stitch(split.base, split.sections);
            assertTrue(r.ok, 'stitch ok: ' + r.errors.join(' '));
            assert(r.html.indexOf('PAGEFORGE') === -1, 'no markers survive');
            assertEqual(norm(ps._extractBodyInner(r.html)), norm(origInner), 'BLL210 #body restored (normalised)');
            assert(r.html.indexOf('stickyNav') === -1 || html.indexOf('stickyNav') !== -1,
                'stitcher introduces no stickyNav of its own');
        });
    });

    describe('PageStitcherMode — single container, auto-classify (headless)', function () {
        function mockOM() {
            return {
                added: [], downloaded: [],
                addFile: function (f) { this.added.push(f); },
                downloadFile: function (n) { this.downloaded.push(n); }
            };
        }

        it('canStitch requires at least two files (a base + ≥1 section)', function () {
            var m = new PageStitcherMode({ stitcher: new PageStitcher() });
            assertFalse(m.canStitch(), 'nothing staged');
            m.setFiles([{ name: 'DEMO101-base.html' }]);
            assertFalse(m.canStitch(), 'one file is not enough');
            m.setFiles([{ name: 'DEMO101-base.html' }, { name: 'DEMO101-lesson-01.html' }]);
            assertTrue(m.canStitch(), 'two files enable stitch');
        });

        it('auto-classifies the base + sections (any order) and downloads the unified page', function () {
            var om = mockOM();
            var m = new PageStitcherMode({ stitcher: new PageStitcher(), outputManager: om });
            // Mixed order: a section, then the base, then another section.
            var files = [
                section('02', '<p>two</p>'),
                { name: 'DEMO101-base.html', html: base(['01', '02']) },
                section('01', '<p>one</p>')
            ];
            var out = m.stitchReadFiles(files);
            assertTrue(out.result.ok, 'ok: ' + out.result.errors.join(' '));
            assertEqual(out.filename, 'DEMO101.html', 'unified file named from the module code');
            assertEqual(om.added.length, 1, 'one file handed to OutputManager');
            assert(om.added[0].content.indexOf('<p>one</p>') !== -1 && om.added[0].content.indexOf('<p>two</p>') !== -1,
                'both sections spliced in');
            assertEqual(om.downloaded[0], 'DEMO101.html', 'download triggered');
        });

        it('classifies section files that carry a GUIDE block quoting a SPLICE marker (regression)', function () {
            // The downstream converter adds a manual-stitch GUIDE block to every
            // section file, and that guidance quotes the splice marker verbatim
            // (e.g. "paste it in place of the matching <!-- PAGEFORGE-SPLICE id="01" -->").
            // A bare-substring base test would class every such section as a base and
            // fail with "More than one base homepage". Base detection must strip GUIDE
            // blocks first, then match a REAL marker — this is the classifier-level
            // gap the pure-core guide-quoting test never exercised.
            var GS = '<!-- PAGEFORGE-GUIDE-START -->', GE = '<!-- PAGEFORGE-GUIDE-END -->';
            function guided(id, inner) {
                return {
                    name: 'BLL220-lesson-' + id + '.html',
                    html: GS + '\n<!-- MANUAL STITCH: paste this in place of the matching ' +
                          '<!-- PAGEFORGE-SPLICE id="' + id + '" --> marker in the base. -->\n' + GE + '\n' +
                          '<!-- PAGEFORGE-SECTION id="' + id + '" -->\n<!-- ' + id + ' -->\n' + inner +
                          '\n<!-- /PAGEFORGE-SECTION -->'
                };
            }
            var om = mockOM();
            var m = new PageStitcherMode({ stitcher: new PageStitcher(), outputManager: om, notify: function () {} });
            var files = [
                { name: 'BLL220-base.html', html: base(['01', '02', '03']) },
                guided('01', '<p>one</p>'), guided('02', '<p>two</p>'), guided('03', '<p>three</p>')
            ];

            // The classifier must see exactly one base + three sections (not 4 bases).
            var c = m._classifyFiles(files, new PageStitcher());
            assertNotNull(c.base, 'the real base is detected');
            assertEqual(c.extraBases.length, 0, 'no extra bases — guide-quoted markers are not real bases');
            assertEqual(c.sections.length, 3, 'all three guided files classed as sections');

            // ...and the full stitch succeeds with no ">1 base" error or marker leak.
            var out = m.stitchReadFiles(files);
            assertTrue(out.result.ok, 'ok despite guide-quoted markers: ' + out.result.errors.join(' '));
            assert(out.result.errors.join(' ').indexOf('More than one base homepage') === -1,
                'no spurious "More than one base homepage" error');
            assertEqual(om.added.length, 1, 'one unified file emitted');
            assert(om.added[0].content.indexOf('PAGEFORGE') === -1,
                'no splice/section/guide markers leak into the stitched output');
        });

        it('reports when no base homepage is present and emits nothing', function () {
            var om = mockOM(); var toasts = [];
            var m = new PageStitcherMode({ stitcher: new PageStitcher(), outputManager: om, notify: function (t) { toasts.push(t); } });
            var out = m.stitchReadFiles([section('01', '<p>x</p>'), section('02', '<p>y</p>')]);
            assertFalse(out.result.ok, 'no base → fails');
            assert(out.result.errors.join(' ').indexOf('No base homepage') !== -1, 'explains the missing base');
            assertEqual(om.added.length, 0, 'nothing emitted');
            assert(toasts.length >= 1, 'a toast surfaced');
        });

        it('reports a missing section (validation) and emits nothing', function () {
            var om = mockOM();
            var m = new PageStitcherMode({ stitcher: new PageStitcher(), outputManager: om });
            var out = m.stitchReadFiles([{ name: 'M-base.html', html: base(['01', '02']) }, section('01', '<p>x</p>')]);
            assertFalse(out.result.ok, 'missing slot 02 → fails');
            assert(out.result.errors.join(' ').indexOf('Missing section for slot "02"') !== -1, 'names the missing slot');
            assertEqual(om.added.length, 0, 'nothing emitted');
        });
    });
})();
