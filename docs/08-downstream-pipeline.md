# 8. The Downstream Pipeline


### Current Pipeline (Claude AI Project)

After PageForge produces the `.txt` file, it is fed into a Claude AI Project that has extensive knowledge files defining how to convert the text into HTML. The key knowledge files are:

#### 00_MASTER_INSTRUCTIONS.md
- Defines the role, core philosophy, input requirements
- Outlines the 7-phase conversion pipeline
- Lists all 44 constraints
- References all other knowledge files

#### 01_PIPELINE_EXTRACTION_TAGS.md
Contains 5 sections:
- **Section 01 — Template Levels:** HTML tag patterns, head sections, heading patterns, module menu structures, title patterns, footer patterns per year level
- **Section 02 — PageForge Text Format:** File structure, metadata block, format conventions
- **Section 03 — Page Boundaries:** 4 validation rules, page-to-file mapping, lesson numbering
- **Section 04 — Tag Taxonomy:** Complete normalisation table (all writer tag variants → normalised forms)
- **Section 05 — Tag Interpretation:** How each normalised tag maps to HTML output

#### 02_DATA_CONTENT_VERIFICATION.md
Contains 3 sections:
- **Section 06 — Interactive Data Patterns:** 13 data patterns writers use for interactive content
- **Section 07 — Content Rules:** Text preservation, grid structure, merging rules
- **Section 08 — Verification:** Full checklist, red flag protocol, 44 constraints, edge cases

#### 06_TEMPLATE_RECOGNITION.md
- Legacy vs Refresh template detection
- Refresh sub-type identification (Standard, Bilingual, Fundamentals, Inquiry, Combo)
- Structural norms by sub-type
- Known pitfalls in reference files
- Mode B validation checklist

#### Component Files (03, 04, 05 — not uploaded but referenced)
- COMP_00–COMP_14 covering all interactive components
- These define exact HTML structures for each interactive type
- NOT needed for Phase 1 of the HTML converter (interactive placeholders only)

---


---

[← Back to index](../CLAUDE.md)
