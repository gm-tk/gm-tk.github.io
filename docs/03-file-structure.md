# 3. File Structure


```
gm-tk.github.io/
├── index.html              # Single-page application shell
├── css/
│   └── styles.css          # All application styles (including debug panel, template selector, multi-file layout)
├── js/
│   ├── docx-parser.js      # .docx XML parser (core extraction engine)
│   ├── formatter.js         # Plain text output formatter (legacy)
│   ├── tag-normaliser.js    # Tag taxonomy & normalisation engine (Phase 1, enhanced Phase 6, Phase 1 Patch)
│   ├── block-scoper.js      # Block scoping engine — hierarchical grouping & analysis (Phase 6)
│   ├── layout-table-unwrapper.js # Layout table detection & unwrapping (Phase 6.1)
│   ├── page-boundary.js     # Page boundary detection & validation (Phase 1)
│   ├── template-engine.js   # Template config loading, resolution & skeleton generation (Phase 2)
│   ├── interactive-extractor.js # Interactive data extraction, placeholder generation & reference doc (Phase 4)
│   ├── html-converter.js    # Core HTML conversion engine (Phase 3, updated Phase 4)
│   ├── output-manager.js    # Multi-file output management, ZIP download, clipboard copy (Phase 5)
│   └── app.js              # UI controller (with file list, preview, ZIP download, debug panel, template selection)
├── tests/
│   ├── test-runner.js       # Minimal Node.js test runner (no external dependencies)
│   ├── tagNormaliserExisting.test.js # Regression tests for existing tag normalisation
│   ├── blockScoping.test.js # Block scoping engine tests
│   ├── ordinalNormalization.test.js # Ordinal-to-number sub-tag normalization tests
│   ├── compoundTags.test.js # Compound tag splitting tests
│   ├── layoutDirection.test.js # Layout direction extraction tests
│   ├── writerInstructions.test.js # Writer instruction detection tests
│   ├── fragmentReassembly.test.js # Red-text fragment reassembly tests
│   ├── interactiveInference.test.js # Interactive type inference from table structure tests
│   ├── videoNormalization.test.js # Video tag normalization tests
│   ├── alertNormalization.test.js # Alert/boxout container normalization tests
│   ├── insideTab.test.js   # [Inside tab] marker handling tests
│   ├── normalizeSubtags.test.js # Comprehensive ordinal & verbose sub-tag normalization tests
│   ├── layoutTableUnwrapper.test.js # Layout table detection, unwrapping, column role assignment tests
│   ├── engs301Fixes.test.js # ENGS301 inconsistency fixes: heading levels, incomplete headings, tag recognition, interactive rendering, data capture
│   ├── lmsCompliance.test.js # LMS compliance recalibration tests: lesson number format, title element, activity classes, table semantics, info trigger, download journal, whakatauki, image alt text
│   ├── defragmentation.test.js # Tag de-fragmentation tests: red-text boundary stitching, bracket space collapsing, whitespace trimming, processBlock integration, ordinal suffix stripping
│   ├── osai201Defects.test.js # Phase 13 OSAI201 layout-table sidebar defects: H2 heading preservation, [image] tag + URL survival in sidebar_image blocks, _sidebarImageUrl cleanliness (no 🔴[RED fragment), fully-red CS paragraph preservation as sidebar_extra blocks, red-text wrapper balance, writer-instruction classification, pipeline integrity through unwrap + block-scope
│   ├── years46LessonRecalibration.test.js # Phase 13 years 4-6 lesson page recalibration tests: title element format, lesson h1, menu button tooltip, two-tier module menu, end-to-end calibration snapshot
│   └── skeletonCalibration.test.js # Phase 15 multi-template skeleton calibration tests: titlePattern token substitution, moduleCodeFormat per template, additionalHeadScripts (stickyNav/tekuradev), tooltip per-template overrides, footer link ordering, cross-template calibration snapshots
├── templates/
│   └── templates.json       # Template configuration (Phase 2)
├── CLAUDE.md               # Project reference & instructions
├── README.md               # Project documentation
└── .nojekyll               # Disables Jekyll processing on GitHub Pages
```

---


---

[← Back to index](../CLAUDE.md)
