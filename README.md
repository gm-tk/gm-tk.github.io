# PageForge

**Client-side Writer Template parser and HTML converter**

---

## What is PageForge?

PageForge is a web-based tool that reads Writer Template `.docx` files and converts them into clean, structured plain text — ready to be used in the HTML conversion pipeline.

It replaces the slow, manual first step of getting content out of a Word document and into a format that can be worked with.

## Why does this exist?

Writer Template documents contain a lot of boilerplate before the actual module content begins (submission checklists, LOT tags, Section A, guidance text, etc.). They also frequently contain tracked changes and Google Docs editing markup that standard Word-to-text tools silently drop — leading to missing content.

PageForge handles all of this automatically:

- **Skips the boilerplate** — automatically detects where your module content starts (at the `[TITLE BAR]` tag) and only outputs the relevant content
- **Handles tracked changes correctly** — deletions are removed, insertions are kept, exactly as the writer intended
- **Handles Google Docs SDT wrappers** — content wrapped in these hidden XML structures is correctly extracted instead of being silently skipped
- **Preserves everything that matters** — square-bracket tags, formatting (bold, italic), hyperlinks, tables, lists, and red text (marked as CS instructions)
- **Extracts module metadata** — module code, subject, course name, and writer details are pulled from the boilerplate and displayed separately

## How to use it

1. Go to **[https://gm-tk.github.io](https://gm-tk.github.io)**
2. Drag and drop your `.docx` file onto the upload area (or click to browse)
3. Wait a few seconds for processing
4. Use the **Copy to Clipboard** or **Download as .txt** buttons to get your output

That's it.

## Privacy and security

**Your files never leave your computer.** PageForge runs entirely in your web browser — there is no server, no upload, no database, and no data retention of any kind. When you close the tab or parse another file, the previous data is gone.

This is not just a policy — it is a technical reality. The app is a static website with no backend whatsoever.

## System requirements

- A modern web browser (Chrome, Firefox, Safari, or Edge)
- Works on both **Mac** and **Windows**
- Works on desktop and tablet
- No installation, no accounts, no plugins

## What the output looks like

The tool produces structured plain text that preserves all of the writer's tags and formatting:

```
=====================================
MODULE METADATA
=====================================
Module Code: OSAI201
Subject: Online Safety
Course: AI Digital Citizenship
=====================================

--- CONTENT START ---

[TITLE BAR] OSAI AI Digital Citizenship  Kirirarautanga Matihiko AI

[H1] Tirohanga Whānui | Overview
Ākonga will define what AI is...

[H2] Learning Intentions
We are learning:
• what AI is
• how to use AI
• to use AI in a responsible way.
```

Square-bracket tags, formatting markers, tables, hyperlinks, and red text instructions are all preserved and clearly marked.

## Questions or issues?

If something isn't parsing correctly, save the `.docx` file that caused the issue so it can be investigated.
