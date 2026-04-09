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

// Expose fs, path, __dirname to test scripts loaded via vm.runInThisContext
global.__testFs = fs;
global.__testPath = path;
global.__testRootDir = path.resolve(__dirname, '..');

function loadScript(filePath) {
    var code = fs.readFileSync(path.resolve(__dirname, '..', filePath), 'utf8');
    // Remove 'use strict' at top level since we're evaluating in global scope
    code = code.replace(/^'use strict';\s*/m, '');
    // Use vm module to run in global context so class declarations are available
    var vm = require('vm');
    vm.runInThisContext(code, { filename: filePath });
}

// Load modules in dependency order
loadScript('js/tag-normaliser.js');
loadScript('js/block-scoper.js');
loadScript('js/layout-table-unwrapper.js');
loadScript('js/formatter.js');
loadScript('js/template-engine.js');
loadScript('js/interactive-extractor.js');
loadScript('js/html-converter.js');

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
