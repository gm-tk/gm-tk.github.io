/**
 * Tests for the rewritten Module Development "Next steps" instructions on the
 * Conversion-complete results screen. Locks in the five-step structure, the
 * nested (a)/(b)/(c) upload sub-list, and the updated wording — driven purely
 * off the author-controlled ModuleResultsPage.NEXT_STEPS constants (no DOM, so
 * these run headlessly in the Node runner). Helper names are prefixed `mdns` to
 * avoid collisions with the other module-dev test files sharing the vm scope.
 */

'use strict';

function mdnsSteps() {
    return ModuleResultsPage.NEXT_STEPS;
}
function mdnsJoined() {
    return ModuleResultsPage.NEXT_STEPS.join('\n');
}

describe('ModuleResultsPage — rewritten next-steps content', function () {

    it('exposes exactly five top-level next-steps', function () {
        assertEqual(mdnsSteps().length, 5, 'the list ends at step 5 (the old sixth step is removed)');
    });

    it('keeps the unchanged next-steps heading', function () {
        assertEqual(ModuleResultsPage.NEXT_STEPS_HEADING,
            'Next steps — convert these files into finalized HTML',
            'heading text is preserved verbatim');
    });

    it('sign-in step uses the new "email option" wording, not "email address and password"', function () {
        var step1 = mdnsSteps()[0];
        assertTrue(step1.indexOf('do not sign in with the email option') !== -1,
            'uses the new "do not sign in with the email option" phrasing');
        assertTrue(step1.indexOf('email address and password') === -1,
            'the old "email address and password" phrasing is gone');
    });

    it('sign-in step still offers the Continue with Google option in <code>', function () {
        assertTrue(mdnsSteps()[0].indexOf('<code>Continue with Google</code>') !== -1,
            'Continue with Google retained inside a <code> element');
    });

    it('upload step renders a nested lettered (type="a") sub-list of exactly two items', function () {
        var step4 = mdnsSteps()[3];
        assertTrue(step4.indexOf('<ol type="a" class="next-steps-sublist">') !== -1,
            'nested ordered sub-list with type="a" and the .next-steps-sublist class is present');
        assertEqual(step4.split('<li>').length - 1, 2, 'exactly two nested (a/b) sub-items');
    });

    it('upload sub-list names the two exact files in (a) Writer, (b) Media order', function () {
        var step4 = mdnsSteps()[3];
        var aPos = step4.indexOf('the Writer');
        var bPos = step4.indexOf('the Media List');
        var cPos = step4.indexOf('example module');
        assertTrue(aPos !== -1 && bPos !== -1, 'both sub-items are present');
        assertTrue(aPos < bPos, 'sub-items appear in (a) Writer, (b) Media order');
        assertTrue(cPos === -1, 'the old example-module reference sub-item is gone');
    });

    it('drops the old single-paragraph "example completed module" reference phrasing', function () {
        assertTrue(mdnsJoined().indexOf('example completed module to use as a formatting reference') === -1,
            'old formatting-reference phrasing replaced by the (a)/(b)/(c) sub-list');
    });

    it('final step says "Submit the message" and there is no old "Review and download" step', function () {
        var steps = mdnsSteps();
        assertTrue(steps[4].indexOf('Submit the message') !== -1,
            'step 5 uses the "Submit the message" wording');
        assertTrue(mdnsJoined().indexOf('Review and download') === -1,
            'the old sixth "Review and download" step is gone');
    });
});
