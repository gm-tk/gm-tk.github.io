'use strict';

/**
 * HTML Generator mode — the third top-level PageForge mode.
 *
 * PageForge V1.5 ships a two-mode shell (Module Development + Page Stitcher) owned
 * by ModeToggle (js/mode-toggle.js). That shell is a state machine that only knows
 * the values 'module' and 'stitcher' and ONLY binds to those two radios — it
 * IGNORES any other mode value. That is deliberately useful here: it lets us add a
 * third mode WITHOUT touching (or risking) the existing, tested shell.
 *
 * This tiny module owns ONLY the HTML Generator section's visibility:
 *   • when the "HTML Generator" radio is chosen  → show #html-generator-section,
 *     hide the two V1.5 front pages (+ the results screen);
 *   • when either V1.5 mode is chosen            → hide #html-generator-section
 *     (ModeToggle already restores its own sections on that same change event).
 *
 * The embedded converter lives in an <iframe> (converter-v2/app/), so its engine
 * and globals are fully isolated from the two V1.5 engines — no name clashes.
 */
(function () {
    if (typeof document === 'undefined' || !document.addEventListener) { return; }

    document.addEventListener('DOMContentLoaded', function () {
        var radios = document.querySelectorAll('input[name="pageforge-mode"]');
        var hgSection = document.getElementById('html-generator-section');
        // The sections that must be hidden while the HTML Generator is showing.
        var v15SectionIds = ['module-dev-section', 'module-results-section', 'stitch-section'];

        // If the page doesn't have the new pieces (e.g. an older index.html), do
        // nothing — this script is a safe no-op rather than an error.
        if (!hgSection || !radios.length) { return; }

        function setHidden(el, hidden) {
            if (el && el.classList) {
                if (hidden) { el.classList.add('hidden'); }
                else { el.classList.remove('hidden'); }
            }
        }

        function apply() {
            var checked = document.querySelector('input[name="pageforge-mode"]:checked');
            var isHtmlGen = !!checked && checked.value === 'html-generator';

            setHidden(hgSection, !isHtmlGen);
            if (isHtmlGen) {
                // Hide the V1.5 front pages + results while the generator is active.
                v15SectionIds.forEach(function (id) {
                    setHidden(document.getElementById(id), true);
                });
            }
            // When leaving HTML Generator, ModeToggle's own change handler restores
            // the correct V1.5 section on this same 'change' event — nothing to do.
        }

        // React to ANY mode radio (including the two V1.5 ones, so switching AWAY
        // from HTML Generator hides its section).
        for (var i = 0; i < radios.length; i++) {
            if (radios[i].addEventListener) { radios[i].addEventListener('change', apply); }
        }

        // Initial state on load (HTML Generator hidden unless it is the checked mode).
        apply();
    });
})();
