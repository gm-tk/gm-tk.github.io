/**
 * Minimal test runner for PageForge tests.
 * Runs in Node.js without any external dependencies.
 *
 * Usage: node tests/test-runner.js
 */

'use strict';

// Track test results
var totalTests = 0;
var passedTests = 0;
var failedTests = 0;
var currentSuite = '';
var failedDetails = [];

function describe(name, fn) {
    currentSuite = name;
    console.log('\n\x1b[1m' + name + '\x1b[0m');
    fn();
}

function it(name, fn) {
    totalTests++;
    try {
        fn();
        passedTests++;
        console.log('  \x1b[32m✓\x1b[0m ' + name);
    } catch (e) {
        failedTests++;
        console.log('  \x1b[31m✗\x1b[0m ' + name);
        console.log('    \x1b[31m' + e.message + '\x1b[0m');
        failedDetails.push({ suite: currentSuite, test: name, error: e.message });
    }
}

function assert(condition, message) {
    if (!condition) {
        throw new Error(message || 'Assertion failed');
    }
}

function assertEqual(actual, expected, message) {
    if (actual !== expected) {
        throw new Error((message || 'Values not equal') +
            ': expected ' + JSON.stringify(expected) + ', got ' + JSON.stringify(actual));
    }
}

function assertDeepEqual(actual, expected, message) {
    if (JSON.stringify(actual) !== JSON.stringify(expected)) {
        throw new Error((message || 'Objects not equal') +
            ':\n  expected: ' + JSON.stringify(expected) +
            '\n  actual:   ' + JSON.stringify(actual));
    }
}

function assertNotNull(value, message) {
    if (value === null || value === undefined) {
        throw new Error(message || 'Expected non-null value');
    }
}

function assertNull(value, message) {
    if (value !== null && value !== undefined) {
        throw new Error((message || 'Expected null') + ', got: ' + JSON.stringify(value));
    }
}

function assertTrue(value, message) {
    if (value !== true) {
        throw new Error((message || 'Expected true') + ', got: ' + JSON.stringify(value));
    }
}

function assertFalse(value, message) {
    if (value !== false) {
        throw new Error((message || 'Expected false') + ', got: ' + JSON.stringify(value));
    }
}

// Make functions global
global.describe = describe;
global.it = it;
global.assert = assert;
global.assertEqual = assertEqual;
global.assertDeepEqual = assertDeepEqual;
global.assertNotNull = assertNotNull;
global.assertNull = assertNull;
global.assertTrue = assertTrue;
global.assertFalse = assertFalse;

// Load source files
var fs = require('fs');
var path = require('path');

function loadScript(filePath) {
    var code = fs.readFileSync(path.resolve(__dirname, '..', filePath), 'utf8');
    // Remove 'use strict' at top level since we're evaluating in global scope
    code = code.replace(/^'use strict';\s*/m, '');
    // Use vm module to run in global context so class declarations are available
    var vm = require('vm');
    vm.runInThisContext(code, { filename: filePath });
}

// Load modules in dependency order (Module Development carry-over set + toast).
// The Standard-mode HTML-conversion pipeline was dropped in this build, so only
// the carried-over modules are loaded here. DocxParser / OutputManager need
// browser APIs (JSZip / DOM / Blob) and are mocked by the tests, so -- as in V1 --
// they are intentionally not loaded by this headless runner.
loadScript('js/toast.js');
loadScript('js/formatter.js');
loadScript('js/comment-extractor.js');
loadScript('js/comment-filter.js');
loadScript('js/comment-inserter.js');
loadScript('js/comment-config.js');
loadScript('js/page-stitcher.js');
loadScript('js/media-list-converter.js');
loadScript('js/module-results-page.js');
loadScript('js/mode-toggle-filename.js');
loadScript('js/mode-toggle.js');

// Expose the canonical comment-capture data to tests (so they validate the real
// shipped whitelist + regexes, not a hand-copied fixture).
try {
    global.COMMENT_AUTHORS_DATA = JSON.parse(
        fs.readFileSync(path.resolve(__dirname, '..', 'data/comment-authors.json'), 'utf8')
    );
} catch (e) {
    global.COMMENT_AUTHORS_DATA = null;
}

// Corpus access for the Page Stitcher's round-trip check (validation oracle).
// The corpus lives one level above the app dir; tests skip gracefully if absent.
global.__readText = function (p) { try { return fs.readFileSync(p, 'utf8'); } catch (e) { return null; } };
// Probe for the corpus root (the app dir may be a sibling of, or nested under,
// FINAL_MODULE_DATA depending on how the tree is mounted).
(function () {
    var candidates = [
        path.resolve(__dirname, '..', '..'),
        path.resolve(__dirname, '..', '..', 'FINAL_MODULE_DATA'),
        path.resolve(__dirname, '..', '..', '..'),
        path.resolve(__dirname, '..', '..', '..', 'FINAL_MODULE_DATA')
    ];
    global.__corpusDir = candidates.filter(function (d) {
        try { return fs.existsSync(path.join(d, '01-Finalized_Modules_')); } catch (e) { return false; }
    })[0] || candidates[0];
})();

// Load test files
var testFiles = fs.readdirSync(__dirname).filter(function(f) {
    return f.match(/\.test\.js$/) && f !== 'test-runner.js';
}).sort();

console.log('PageForge Test Suite');
console.log('======================');
console.log('Loading ' + testFiles.length + ' test file(s)...\n');

for (var i = 0; i < testFiles.length; i++) {
    loadScript('tests/' + testFiles[i]);
}

// Print summary
console.log('\n======================');
console.log('Results: ' + passedTests + '/' + totalTests + ' passed, ' + failedTests + ' failed');

if (failedDetails.length > 0) {
    console.log('\n\x1b[31mFailed tests:\x1b[0m');
    for (var f = 0; f < failedDetails.length; f++) {
        console.log('  ' + failedDetails[f].suite + ' > ' + failedDetails[f].test);
        console.log('    ' + failedDetails[f].error);
    }
    process.exit(1);
} else {
    console.log('\x1b[32mAll tests passed!\x1b[0m');
    process.exit(0);
}
