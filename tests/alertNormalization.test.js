/**
 * Tests for Alert / Boxout Container Normalization (Instruction 9)
 */

'use strict';

var normaliser = new TagNormaliser();
var scoper = new BlockScoper(normaliser);

describe('Alert Normalization — Test 9.3.1: Box out to the right', function() {
    it('should normalise [Box out to the right] to alert variant box_right', function() {
        var result = scoper.normaliseAlertTag('Box out to the right');
        assertNotNull(result);
        assertEqual(result.type, 'alert');
        assertEqual(result.variant, 'box_right');
    });
});

describe('Alert Normalization — Test 9.3.2: Alert default', function() {
    it('should normalise [Alert] to default variant', function() {
        var result = scoper.normaliseAlertTag('Alert');
        assertNotNull(result);
        assertEqual(result.type, 'alert');
        assertEqual(result.variant, 'default');
    });
});

describe('Alert Normalization — Test 9.3.3: Thought bubble with colour', function() {
    it('should normalise [Thought bubble green] with colour', function() {
        var result = scoper.normaliseAlertTag('Thought bubble green');
        assertNotNull(result);
        assertEqual(result.type, 'alert');
        assertEqual(result.variant, 'thought_bubble');
        assertEqual(result.colour, 'green');
    });
});

describe('Alert Normalization — Test 9.3.4: Important', function() {
    it('should normalise [Important] to important variant', function() {
        var result = scoper.normaliseAlertTag('Important');
        assertNotNull(result);
        assertEqual(result.type, 'alert');
        assertEqual(result.variant, 'important');
    });
});

describe('Alert Normalization — Test 9.3.5: End of box closes alert', function() {
    it('should match [End of box] as alert closer', function() {
        // This is tested through block scoping fuzzy closer matching
        var scoperInst = new BlockScoper(normaliser);
        var result = scoperInst._fuzzyMatchCloser('end of box');
        assertEqual(result, 'alert', 'Should match alert block type');
    });
});

describe('Alert Normalization — Alert top variant', function() {
    it('should normalise [alert top] to top variant', function() {
        var result = scoper.normaliseAlertTag('alert top');
        assertNotNull(result);
        assertEqual(result.variant, 'top');
    });

    it('should normalise [alert.top] to top variant', function() {
        var result = scoper.normaliseAlertTag('alert.top');
        assertNotNull(result);
        assertEqual(result.variant, 'top');
    });

    it('should normalise [alert.top.] to top variant', function() {
        var result = scoper.normaliseAlertTag('alert.top.');
        assertNotNull(result);
        assertEqual(result.variant, 'top');
    });
});

describe('Alert Normalization — Coloured box', function() {
    it('should normalise [purple coloured box] with colour purple', function() {
        var result = scoper.normaliseAlertTag('purple coloured box');
        assertNotNull(result);
        assertEqual(result.variant, 'coloured_box');
        assertEqual(result.colour, 'purple');
    });

    it('should normalise [red coloured box] with colour red', function() {
        var result = scoper.normaliseAlertTag('red coloured box');
        assertNotNull(result);
        assertEqual(result.variant, 'coloured_box');
        assertEqual(result.colour, 'red');
    });

    it('should normalise [coloured box] without colour', function() {
        var result = scoper.normaliseAlertTag('coloured box');
        assertNotNull(result);
        assertEqual(result.variant, 'coloured_box');
        assertNull(result.colour);
    });
});

describe('Alert Normalization — Supervisor note', function() {
    it('should normalise [Supervisor note]', function() {
        var result = scoper.normaliseAlertTag('Supervisor note');
        assertNotNull(result);
        assertEqual(result.variant, 'supervisor_note');
    });

    it('should normalise [Supervisor\'s Note]', function() {
        var result = scoper.normaliseAlertTag("Supervisor's Note");
        assertNotNull(result);
        assertEqual(result.variant, 'supervisor_note');
    });
});

describe('Alert Normalization — Box variants', function() {
    it('should normalise [Box 1]', function() {
        var result = scoper.normaliseAlertTag('Box 1');
        assertNotNull(result);
        assertEqual(result.variant, 'box');
    });

    it('should normalise [Box to the right with an exemplar]', function() {
        var result = scoper.normaliseAlertTag('Box to the right with an exemplar');
        assertNotNull(result);
        assertEqual(result.variant, 'box_right_exemplar');
    });

    it('should normalise [Right hand side alert box]', function() {
        var result = scoper.normaliseAlertTag('Right hand side alert box');
        assertNotNull(result);
        assertEqual(result.variant, 'alert_right');
    });
});

describe('Alert Normalization — Thought bubble plain', function() {
    it('should normalise [Thought bubble] without colour', function() {
        var result = scoper.normaliseAlertTag('Thought bubble');
        assertNotNull(result);
        assertEqual(result.variant, 'thought_bubble');
        assertNull(result.colour);
    });
});

describe('Alert Normalization — Definition', function() {
    it('should normalise [definition]', function() {
        var result = scoper.normaliseAlertTag('definition');
        assertNotNull(result);
        assertEqual(result.variant, 'definition');
    });
});

describe('Alert Normalization — Equation', function() {
    it('should normalise [Equation]', function() {
        var result = scoper.normaliseAlertTag('Equation');
        assertNotNull(result);
        assertEqual(result.variant, 'equation');
    });
});

describe('Alert Normalization — Summary box', function() {
    it('should normalise [alert/summary box]', function() {
        var result = scoper.normaliseAlertTag('alert/summary box');
        assertNotNull(result);
        assertEqual(result.variant, 'summary');
    });
});
