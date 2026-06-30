# PageForge V1.5

A **100% client-side** static web app that prepares the inputs for Te Kura's downstream module-conversion workflow. It takes a writer's **Writer's Template** `.docx` (and optional Media List), and produces the parsed `.txt` files — now carrying reviewers' actionable Word comments — plus a separate **Page Stitcher** for recombining split modules.

PageForge V1.5 is an **interim production replacement** for the current online PageForge. Everything runs in the browser: nothing is uploaded, stored, or sent to a server.

---

## Two modes

A single switch in the header toggles between the two top-level modes.

### 1. Module Development (default)

Drop the Writer's Template and/or the Media List into the **one** Word-documents container (1–2 `.docx`) and press **Convert**:

| Upload area | Accepts | Produces |
|---|---|---|
| **Word documents** | the Writer's Template and/or the Media List `.docx` (1–2 files, **auto-classified** by content) | `<CODE> Writers Template_parsed.txt` and/or `<CODE> Media List_parsed.txt` (the module `<CODE>` is detected in the file; all other filename parts are dropped) |

Both `.docx` go in the one container in any order — PageForge detects which is the Writer's Template (it has a `[TITLE BAR]`) and which is the Media List (it has a media table), and **converts every document you provide**, listing each produced file with its own download — plus a **Download all as a ZIP** button when more than one file is produced. Upload these into the downstream HTML Convertor Claude Project to generate the finished module HTML.

### 2. Page Stitcher

For modules the converter had to emit in pieces (SPLIT MODE). Drop the **base homepage and all of its section files together into one container**, press **Stitch**, and download one unified single-page module HTML (named `<CODE>.html`, matching how single-page modules are built) — PageForge tells the base from the sections automatically. See [`SPLIT_MODE_AND_STITCH_CONTRACT.md`](SPLIT_MODE_AND_STITCH_CONTRACT.md).

---

## The two features

**1. Native Word comment capture.** When a writer's `.docx` carries native Word editor comments, PageForge keeps only the **actionable** ones from the six Creative-Services reviewers (an asymmetric filter drops pure copyright/permission boilerplate but keeps anything with an action signal) and re-emits each as a **red note** in the parsed `.txt`, immediately before the thing it refers to. A comment anchored to a Media List row is matched to the body element that uses the same media (by URL, iStock id, or YouTube id). Whitelist + filter are data-driven in [`data/comment-authors.json`](data/comment-authors.json).

**2. Page Stitcher (with SPLIT MODE).** The downstream converter can emit a long single-page module as a base homepage + per-section files (so each generation stays within length limits); the Page Stitcher recombines them losslessly via an explicit marker contract.

---

## Privacy model

- **100% client-side.** All parsing, conversion and stitching happen in the browser.
- **Nothing is uploaded, stored, or transmitted** — no backend, no `localStorage` / `sessionStorage`; session state is held in memory only.
- **Content fidelity.** Writer-supplied text passes through unchanged; comment notes are *additive metadata*, never edits to the source.

---

## Project structure

```
index.html              The single-page app (both modes)
css/styles.css          Styles
data/
  comment-authors.json    Comment whitelist + asymmetric content filter + media-match config
js/
  docx-parser.js          .docx reader (JSZip); extended for native comment extraction
  comment-extractor.js    comments.xml parse + anchor/rowUrl capture + carry-forward
  comment-filter.js       author whitelist/normalisation + asymmetric omit filter
  comment-inserter.js     body + media-match placement; red-note rendering
  comment-config.js       loads data/comment-authors.json (browser)
  formatter.js            parsed-.txt formatter (red-text marker reused for comment notes)
  page-stitcher.js        SPLIT-MODE reassembly (pure core + the stitch-mode adapter)
  media-list-converter.js structural Media List → .txt
  module-results-page.js  results / download screen
  mode-toggle.js          the two-mode shell + Module Development conversion orchestrator
  mode-toggle-filename.js  output-filename derivation
  output-manager.js       download primitive (Blob + object URL)
  toast.js                standalone toast
tests/                  headless test suite (test-runner.js + *.test.js)
SPLIT_MODE_AND_STITCH_CONTRACT.md   the SPLIT/STITCH contract + downstream instructions
.nojekyll               GitHub Pages marker
```

---

## Running the tests

No dependencies — the runner is plain Node:

```bash
node tests/test-runner.js
```

It loads every `js/` module and auto-discovers `tests/*.test.js`, printing a pass/total summary. The suite is **135/135 passing**. A full Page Stitcher round-trip on a real module runs automatically when the finalized-module corpus is present beside the app, and skips cleanly when it isn't.

---

## Deploying

This is a static site. Deploy by serving the directory (or pushing to a GitHub Pages repo); `.nojekyll` is already present so the `js/` and `data/` folders are served as-is. No build step.

> The browser loads `data/*.json` via `fetch`, so use an `http(s)` origin (e.g. GitHub Pages or any static server) rather than opening `index.html` from `file://`. Each data-driven module also carries a built-in fallback, so the app degrades gracefully if a data file can't be fetched.
