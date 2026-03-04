/**
 * Tests for Writer Instruction / Developer Note Detection (Instruction 5)
 */

'use strict';

var normaliser = new TagNormaliser();
var scoper = new BlockScoper(normaliser);

describe('Writer Instructions — Test 5.4.1: Conditional instruction', function() {
    it('should detect "If correct please..." as writer note', function() {
        var result = scoper.detectWriterInstruction(
            'If correct please let the person know by having \'Well done\' pop up'
        );
        assertTrue(result.isWriterNote, 'Should be a writer note');
    });
});

describe('Writer Instructions — Test 5.4.2: Button Check', function() {
    it('should detect [Button] Check as button label', function() {
        var result = scoper.detectWriterInstruction('Button Check');
        assertTrue(result.isButtonLabel, 'Should be a button label');
        assertEqual(result.label, 'Check');
    });
});

describe('Writer Instructions — Test 5.4.3: Button Reset', function() {
    it('should detect [Button] Reset as button label', function() {
        var result = scoper.detectWriterInstruction('Button Reset');
        assertTrue(result.isButtonLabel);
        assertEqual(result.label, 'Reset');
    });
});

describe('Writer Instructions — Test 5.4.4: Self-marking button', function() {
    it('should detect [Self-marking button] as writer note', function() {
        var result = scoper.detectWriterInstruction('Self-marking button');
        assertTrue(result.isWriterNote, 'Should be a writer note');
    });
});

describe('Writer Instructions — Test 5.4.5: Reset button instruction', function() {
    it('should detect [Reset button to take the test again] as writer note', function() {
        var result = scoper.detectWriterInstruction('Reset button to take the test again');
        assertTrue(result.isWriterNote, 'Should be a writer note');
    });
});

describe('Writer Instructions — Test 5.4.6: D&D with embedded instruction', function() {
    it('should NOT detect as writer note when tag starts with block keyword', function() {
        var result = scoper.detectWriterInstruction(
            'Drag and drop activity with correct answers. Please random shuffle the answers and include a button to self mark and a button to reset'
        );
        // The tag starts with "Drag" which is a recognized block-opening keyword.
        // The block scoper handles extracting the instruction portion.
        // detectWriterInstruction correctly returns false because it starts with
        // a recognized element tag word.
        assertFalse(result.isWriterNote, 'Should not flag as writer note — block scoper extracts instructions');
    });

    it('should detect instruction portion extracted by block scoper', function() {
        // The block scoper would extract the D&D part as block type and
        // "Please random shuffle..." as a writer note via _extractWriterNotesFromTag
        var scoperInst = new BlockScoper(normaliser);
        var noteResult = scoperInst._extractWriterNotesFromTag(
            'Drag and drop activity with correct answers. Please random shuffle the answers',
            'dragdrop'
        );
        assert(noteResult.notes.length > 0, 'Block scoper should extract writer notes');
    });
});

describe('Writer Instructions — Test 5.4.7: Dev team note', function() {
    it('should detect [Dev team to recreate] as writer note', function() {
        var result = scoper.detectWriterInstruction('Dev team to recreate');
        assertTrue(result.isWriterNote);
    });
});

describe('Writer Instructions — Test 5.4.8: CS note', function() {
    it('should detect [CS – choices below...] as writer note', function() {
        var result = scoper.detectWriterInstruction('CS – choices below with additional feedback pop-outs');
        assertTrue(result.isWriterNote);
    });
});

describe('Writer Instructions — Test 5.4.9: Image + CS instruction', function() {
    it('should NOT detect bare image tag as writer note', function() {
        // "image" starts with a recognized element keyword, so it shouldn't be a writer note
        var result = scoper.detectWriterInstruction('image');
        assertFalse(result.isWriterNote, 'Bare image should not be writer note');
    });
});

describe('Writer Instructions — Test 5.4.10: Full sentence instruction', function() {
    it('should detect full sentence with "please" as writer note', function() {
        var result = scoper.detectWriterInstruction(
            'Please make a drop and drag activity where the theme is written on the page and the student needs to drag and drop'
        );
        assertTrue(result.isWriterNote, 'Should detect as writer note');
    });
});

describe('Writer Instructions — Button with long instruction', function() {
    it('should detect [Button] followed by long instruction as writer note', function() {
        var result = scoper.detectWriterInstruction(
            'Button Please create a mindmap template that students can interact with and fill in'
        );
        assertTrue(result.isWriterNote, 'Long instruction after Button should be writer note');
    });
});

describe('Writer Instructions — Note prefix', function() {
    it('should detect [Note: some instruction] as writer note', function() {
        var result = scoper.detectWriterInstruction('Note: This should be highlighted');
        assertTrue(result.isWriterNote);
    });
});

describe('Writer Instructions — Copyright notice', function() {
    it('should detect tag with copyright as writer note', function() {
        var result = scoper.detectWriterInstruction('Check copyright permissions for this image');
        assertTrue(result.isWriterNote);
    });
});

describe('Writer Instructions — Students to select', function() {
    it('should detect [Students to select...] as writer note', function() {
        var result = scoper.detectWriterInstruction('Students to select the correct answer');
        assertTrue(result.isWriterNote);
    });
});

describe('Writer Instructions — Learning Journal button', function() {
    it('should detect [Learning Journal button...] as writer note', function() {
        var result = scoper.detectWriterInstruction(
            'Learning Journal button that links with journal 1 for this module'
        );
        assertTrue(result.isWriterNote);
    });
});

describe('Writer Instructions — Short button labels', function() {
    it('should detect "Go to journal" as button label (3 words)', function() {
        var result = scoper.detectWriterInstruction('Button Go to journal');
        assertTrue(result.isButtonLabel);
        assertEqual(result.label, 'Go to journal');
    });

    it('should detect "Upload to dropbox" as button label (3 words)', function() {
        var result = scoper.detectWriterInstruction('Button Upload to dropbox');
        assertTrue(result.isButtonLabel);
        assertEqual(result.label, 'Upload to dropbox');
    });
});
