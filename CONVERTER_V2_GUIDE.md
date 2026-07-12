# Converter V2 — The Complete File Guide

**A plain-English map of everything inside the `converter-v2` folder: what each file does, how the pieces fit together, and exactly where to make changes when the converter needs to learn a new rule.**

*Written for a developer with a basic working knowledge of JavaScript. Last updated: 10 July 2026 (build 260617.84). If a file has been renamed or split since then, the loader manifest `converter-v2/app/js/_modules.json` is always the up-to-date list of engine files.*

---

## Table of contents

1. [The big picture — how the converter works](#1-the-big-picture--how-the-converter-works)
2. [The golden rule — data over code](#2-the-golden-rule--data-over-code)
3. [Folder and file structure](#3-folder-and-file-structure)
4. [Quick reference — every file in one line](#4-quick-reference--every-file-in-one-line)
5. [Part A — The data files (where most updates happen)](#part-a--the-data-files)
6. [Part B — The engine files (the JavaScript)](#part-b--the-engine-files)
7. [Part C — Common update recipes, step by step](#part-c--common-update-recipes)
8. [Part D — The safety net: toggles, checks, and testing](#part-d--the-safety-net)

---

## 1. The big picture — how the converter works

Converter V2 (shown in the browser as "HTML Generator V2") takes two Word documents — a **Writers Template** (`.docx`) and its **Media List** (`.docx`, or one combined file) — and produces the finished HTML pages for an online learning module, plus a text file listing the interactive widgets a developer still needs to build by hand.

The conversion runs as a **pipeline**: each stage takes the previous stage's output, does one job, and hands the result on. In plain terms:

1. **Unzip the Word file.** A `.docx` is secretly a zip archive. `ZipReader` opens it and pulls out the XML inside.
2. **Read the document.** `DocxExtractor` walks the XML and turns it into a simple list of "blocks" — paragraphs and tables — carefully preserving the writer's **red text** (which is where all the `[tags]` and instructions live), bold/italic, bullet levels, hyperlinks, and any Word comments.
3. **Find the media table.** `MediaListParser` locates the media list table and reads out each media item (images, videos, audio) with its real URL.
4. **Work out which module this is.** `ModuleResolver` detects the module code (e.g. `ENGC102`) and looks up that module family's house style — page layout, menu type, footer style — from the style registries. It also runs `PrepareRun`, the one shared set-up routine both the browser and the batch tool must use.
5. **Split into pages.** `PageSplitter` cuts the document into the separate HTML pages the finished module needs (overview page, lesson pages), following the `[end page]` / `[LESSON]` markers.
6. **Understand the tags.** `TagNormaliser` reads every red span and decides: is this a known `[tag]`? A writer's note to the design team? Or just noise? All tag knowledge comes from `Tag_Lexicon.json`.
7. **Find the interactives.** `InteractiveScanner` spots interactive widgets (flip cards, accordions, tab groups...) and bundles up everything that belongs to each one, so the rest of the converter knows to step around that content. Since round 214: when a writer numbers an accordion's panels ([Accordion 1] ... [Accordion 4]), everything between one numbered tag and the next stays inside that panel — even another interactive typed inside it (a modal set, a tab group, a click-drop table). Those nested widgets ride along as sub-bundles and are built in place when possible, or shown as a clearly-marked placeholder inside the panel.
8. **Convert the content.** `ContentConverter` — the heart of the engine — walks each page's content and emits the body HTML: headings, paragraphs, lists, tables, callout boxes, activity boxes, media embeds, menus. Eight helper classes (`ListsAndRuns`, `TablesAndGrids`, `MenuBuilder`, and so on) each own one slice of that work.
9. **Build the easy widgets.** `InteractiveBuilder` turns the widget types it knows how to build (about a dozen) into real working HTML. Anything it can't build cleanly stays as an honest, clearly-marked orange placeholder box.
10. **Wrap each page in the shell.** `SkeletonBuilder` adds the standard page frame: `<head>`, the header with the module title and menu, the footer with prev/next links.
11. **Add the acknowledgements.** `AcksBuilder` writes the acknowledgements section from the media list (on the first page only).
12. **Finish and hand over.** `PageAssembler` runs the whole thing per module, `HtmlFormatter` tidies the indentation, `ManifestBuilder` writes `{CODE}_interactives.txt` (the developer's to-do list of un-built widgets), and the browser UI (`App.js`) offers everything for download.

Two things run this pipeline:

- **The browser page** — `converter-v2/app/index.html` + `App.js`. This is what a human uses: drag in the files, click Convert, download the results.
- **The batch tool** — a Node.js script that lives in the development harness (outside this repo) and converts the whole module library at once for testing.

Both are forced through the **same** preparation routine (`ModuleResolver.PrepareRun`) so they can never produce different output for the same module.

---

## 2. The golden rule — data over code

**Almost everything you will ever need to change lives in the `data/*.json` files, not in the JavaScript.**

The engine's design principle is called *data over code*: the JavaScript holds the general logic ("find the tag, look up its shape, fill in the blanks"), while all the actual knowledge — which words count as a tag, what HTML an alert box uses, which menu style each subject gets — lives in editable JSON files.

In practice this means:

- The writer starts spelling a tag a new way? → **edit `Tag_Lexicon.json`** (add one alias). No code change.
- An alert box should get a new CSS class? → **edit `Emit_Templates.json`** (change one template string). No code change.
- A new phrase should be recognised as a note to the design team? → **edit `Instruction_Cues.json`** (add one phrase). No code change.
- A new website needs its own acknowledgement wording? → **edit `Acks_Formats.json`**. No code change.

Only genuinely *new behaviour* (a new kind of widget builder, a new structural rule) needs JavaScript — and even then, the shape of the output still goes in the JSON, and the code just applies it.

**One more rule, and it is non-negotiable:** never write module-specific code like `if (moduleCode === "OSAI201")`. If one module seems to need special treatment, the correct fix is a general rule (in data) that the module happens to trigger. Several file headers repeat this warning — it is how the first version of the converter died.

Nearly every behaviour also has an **environment toggle** (an "off switch" with a name like `LISTNEST_OFF`) so any single rule can be temporarily reverted for comparison testing without touching code or data. See [Part D](#part-d--the-safety-net).

---

## 3. Folder and file structure

```
pageforge-site/
└── converter-v2/
    ├── CLAUDE.md                  ← operating guide for AI-assisted development sessions
    ├── BUILD_CHANGELOG.md         ← round-by-round history of every change (newest first)
    │
    ├── app/                       ← THE ENGINE + the browser page
    │   ├── index.html             ← the converter web page (upload, convert, download)
    │   ├── css/
    │   │   └── styles.css         ← styling for the converter page itself (not the output)
    │   └── js/                    ← 32 JavaScript files — the whole engine
    │       ├── _modules.json      ← loader manifest: the master list of engine files,
    │       │                        their load order, and the data-file map
    │       ├── Config.js          ← app version + list of data files to load
    │       ├── DataService.js     ← loads all the data files at startup
    │       ├── Utils.js           ← small shared helper functions
    │       ├── ZipReader.js       ← opens .docx files (they are zip archives)
    │       ├── ZipWriter.js       ← builds the "download all" zip
    │       ├── DocxExtractor.js   ← Word XML → simple content blocks
    │       ├── MediaListParser.js ← finds + reads the media list table
    │       ├── ConversionRun.js   ← the shared "clipboard" object for one conversion
    │       ├── TagNormaliser.js   ← recognises the writer's [tags]
    │       ├── ModuleResolver.js  ← detects the module code + looks up house style
    │       ├── ConventionResolver.js  ← looks up menu/callout/video conventions
    │       ├── PageSplitter.js    ← cuts the document into output pages
    │       ├── InteractiveScanner.js  ← finds + bundles interactive widgets
    │       ├── InteractiveBuilder.js  ← builds the known widget types as real HTML
    │       ├── ListsAndRuns.js    ← paragraphs, bullet lists, inline bold/italic/links
    │       ├── NotesAndComments.js    ← "Writers Note:" / "Red Flag:" notes + Word comments
    │       ├── TablesAndGrids.js  ← tables, and layout-tables → column grids
    │       ├── MenuBuilder.js     ← the module menu (tabs / simplified / two-column)
    │       ├── PanelsBuilder.js   ← Fundamentals phase panels + Inquiry tab panels
    │       ├── BilingualBuilder.js    ← Māori/English bilingual page bodies
    │       ├── ActivitiesBuilder.js   ← the green activity boxes
    │       ├── MediaBuilder.js    ← image placeholders, video/audio embeds
    │       ├── PrecedenceResolver.js  ← "copy the nearest sibling module" lookup (dormant)
    │       ├── ContentConverter.js    ← THE HEART: walks a page and emits the body HTML
    │       ├── TemplateModeResolver.js ← tidies the <body> class token order
    │       ├── SkeletonBuilder.js ← page shell: <head>, header, footer
    │       ├── AcksBuilder.js     ← the acknowledgements section
    │       ├── ManifestBuilder.js ← writes {CODE}_interactives.txt
    │       ├── HtmlFormatter.js   ← re-indents the finished HTML
    │       ├── PageAssembler.js   ← runs the whole pipeline for one module
    │       ├── SummaryReporter.js ← the conversion summary panel in the UI
    │       └── App.js             ← the browser UI wiring (loads last)
    │
    └── data/                      ← THE RULES — where most updates happen
        ├── Tag_Lexicon.json               ← the tag vocabulary (aliases → canonical tags)
        ├── Tag_Exceptions.json            ← rare one-off tag overrides
        ├── Instruction_Cues.json          ← "note to the design team" vocabulary
        ├── Input_Doc_Rules.json           ← how to read the Word documents
        ├── Emit_Templates.json            ← ★ THE central file: every HTML output shape
        ├── Interactive_Boundary_ChildTag_Bank.json ← where each widget starts/ends
        ├── Interactive_Wrapper_Catalogue.json      ← reference: widget wrapper HTML (not loaded)
        ├── Manifest_Patterns.json         ← widget data-pattern signatures for the .txt
        ├── Menu_Scaffold_Registry.json    ← which menu type each module family uses
        ├── Module_Menu_Scaffold.json      ← menu analysis notes (reference only)
        ├── Html_Convention_Registry.json  ← measured menu/callout/video conventions
        ├── Style_Anchor_Registry.json     ← per-family page structure (body class, footer…)
        ├── Style_Anchor_Registry_Majority_And_Deviations.json ← fallback for new series
        ├── Acks_Formats.json              ← acknowledgement wording + rules
        ├── Comment_Authors.json           ← whose Word comments get surfaced
        ├── Template_Modes.json            ← <body> class ordering rules
        ├── Overview_Menu_Heading_Lexicon.json ← known overview-menu heading phrases
        ├── Precedence_Cascade.json        ← the sibling-inheritance cascade (dormant)
        ├── Subject_Global_Parameters.json ← per-subject house-style defaults (dormant)
        ├── Module_Structure_Index.json    ← per-module measured structure (machine-built)
        ├── Granular_Scaffold_Registry.json ← fine-grained measurements (diagnostic only)
        ├── Scaffold_Consensus.json        ← older consensus measurements (diagnostic only)
        ├── Tag_Interpretation_Rules.md    ← the master tag-behaviour specification (prose)
        ├── Tag_Normalisation_Spec.md      ← how tag matching works (prose)
        └── Interactive_Boundary_Rules.md  ← how widget boundaries work (prose)
```

Two notes on this layout:

- **This is the only copy of the engine.** The development harness (`CONVERTER_V2/` in the project folder, outside this repo) reaches these exact files through symbolic links. Editing the engine through either path edits the same file.
- The converter's **output** styling (what the finished module pages look like) is not in `app/css/styles.css` — that file only styles the converter page itself. The finished pages rely on Te Kura's own site CSS.

---

## 4. Quick reference — every file in one line

### The data files (`converter-v2/data/`)

| File | What it holds | Edit it when… |
|---|---|---|
| **Tag_Lexicon.json** | Every known writer tag + all its spellings | A writer spells a tag a new way, or a new tag is invented |
| **Tag_Exceptions.json** | One-off overrides for unresolvable tag spans | A single bizarre tag string needs a hand answer (rare) |
| **Instruction_Cues.json** | Words that mark a red span as a note to the team | A new "please can you…" phrasing needs recognising |
| **Input_Doc_Rules.json** | How the Word docs are read (red shades, markers, media-table columns) | A new red text shade, new front-matter boilerplate, or new media-list column heading appears |
| **Emit_Templates.json** ★ | Every HTML shape the converter outputs | Any output HTML needs to change: boxes, headings, menus, placeholders, buttons, footers… |
| **Interactive_Boundary_ChildTag_Bank.json** | Per-widget capture rules — where a widget's content starts and stops | A widget swallows too much (or too little) of the page |
| **Interactive_Wrapper_Catalogue.json** | Reference list of the human developers' widget wrapper HTML | Reference reading only — not loaded by the engine |
| **Manifest_Patterns.json** | The 13 widget data-pattern signatures | A new widget data shape should be named in the .txt hand-off |
| **Menu_Scaffold_Registry.json** | Menu type (tabs/simplified/none) per module family | A family's menu type is wrong |
| **Html_Convention_Registry.json** | Measured menu/callout/video conventions per family | Rebuilt by script from the finished library |
| **Style_Anchor_Registry.json** | Page structure per subject/series (body class, page model…) | A family's page shell or page-splitting model is wrong |
| **Style_Anchor_Registry_Majority_And_Deviations.json** | The "best guess" fallback for never-seen series | Same — for brand-new series |
| **Acks_Formats.json** | All acknowledgement wording + source rules | A new media source needs its own credit line |
| **Comment_Authors.json** | Whitelisted Word-comment authors | A new team member's comments should appear in output |
| **Template_Modes.json** | `<body>` class token ordering | A new body-class token (like `mathJax`) appears |
| **Overview_Menu_Heading_Lexicon.json** | Known overview-menu heading phrases + counts | Rebuilt by script; hand-add a phrase if needed |
| **Precedence_Cascade.json** | The 6-level "inherit from sibling module" rules | Dormant — leave unless reviving that feature |
| **Subject_Global_Parameters.json** | Per-subject house-style defaults ("doc 14") | Dormant — per-family switches, master off |
| **Module_Structure_Index.json** | Machine-built index of every module's structure | Regenerated by tooling — don't hand-edit |
| **Granular_Scaffold_Registry.json / Scaffold_Consensus.json / Module_Menu_Scaffold.json** | Measurement data for the test tooling | Diagnostic only — not read by the engine |
| **The three .md files** | The human-readable specifications behind the JSON | Update alongside major rule changes, for the record |

### The engine files (`converter-v2/app/js/`) — in pipeline order

| File | One-line job |
|---|---|
| **Config.js** | The app version number and the list of data files to load |
| **DataService.js** | Loads every data file at startup; the only file that fetches anything |
| **Utils.js** | Small pure helpers: text folding, HTML escaping, template filling |
| **ZipReader.js** | Opens a `.docx` (zip) in the browser, no libraries |
| **ZipWriter.js** | Builds the "Download all as .zip" file |
| **DocxExtractor.js** | Word XML → ordered list of paragraph/table blocks with red-text markers |
| **MediaListParser.js** | Finds the media table and reads its rows into clean items |
| **ConversionRun.js** | The shared state object one conversion carries through every stage |
| **TagNormaliser.js** | Decides what every red span means (tag / instruction / noise) |
| **ModuleResolver.js** | Detects the module code, resolves house style, runs the shared `PrepareRun` |
| **ConventionResolver.js** | Attaches the measured menu/callout/video conventions to the run |
| **PageSplitter.js** | Splits the content into output pages |
| **InteractiveScanner.js** | Finds each interactive widget and bundles its content |
| **InteractiveBuilder.js** | Builds the ~12 known widget types as real HTML (or declines safely) |
| **ListsAndRuns.js** | Plain text → paragraphs, nested bullet/numbered lists, inline markup |
| **NotesAndComments.js** | The red+bold designer notes ("Writers Note:" / "Red Flag:" / "Designer/Developer To Do:") and surfaced Word comments ("Note from {author}:") |
| **TablesAndGrids.js** | Kept `<table>`s, and layout-tables converted to row/column grids |
| **MenuBuilder.js** | The module menu in all its shapes |
| **PanelsBuilder.js** | Fundamentals phase panels and Inquiry tab panels |
| **BilingualBuilder.js** | Māori/English bilingual body rendering |
| **ActivitiesBuilder.js** | The activity boxes (opening, numbering, supervisor-note variant) |
| **MediaBuilder.js** | Images (placeholder or direct), video/audio embeds |
| **PrecedenceResolver.js** | The dormant "copy the sibling module's layout" lookup |
| **ContentConverter.js** ★ | The heart — walks a page's items and emits the body HTML |
| **TemplateModeResolver.js** | Puts `<body>` class tokens in the canonical order |
| **SkeletonBuilder.js** | Wraps the body in the page shell: head, header, footer |
| **AcksBuilder.js** | Builds the acknowledgements section from the media list |
| **ManifestBuilder.js** | Writes `{CODE}_interactives.txt` — the developer's widget to-do list |
| **HtmlFormatter.js** | Re-indents the finished HTML with tabs |
| **PageAssembler.js** | The conductor: runs every stage for one module, in order |
| **SummaryReporter.js** | Renders the conversion summary panel in the browser |
| **App.js** | The browser UI: upload, options, convert button, downloads |
| **_modules.json** | The master file list: load order for browser and Node, plus the data map |

---

# Part A — The data files

These are documented first because **this is where nearly all future updates belong.** Each section explains what the file holds, how it is structured, and gives a worked example of adding a new rule.

A shared convention across all of them: keys and matching are done on **"folded" text** — lowercased, accents stripped, punctuation normalised — so `[Hint Slider]`, `[hint slider]` and `[HINT SLIDER]` are all the same thing. But the *content* the reader sees is never folded; original capitalisation is always preserved in output.

---

## A1. Tag_Lexicon.json — the tag vocabulary ★

**What it holds.** The complete list of structural tags a writer can use (about 83 of them), with every spelling of each tag seen in the wild, and what each tag *does*. This is the single most likely file you will ever edit: when a writer types a tag in a new way, one line here teaches the whole converter.

**Structure.** Two top-level sections:

- `_meta` — housekeeping: a glossary of the "directives" (see below), the extension rule, and three special adjustment blocks (`condition_primary_demote`, `qualifier_alias_demote`, `tag_promote` — explained under "Advanced" below).
- `tags` — the vocabulary itself. Each entry is keyed by the tag's canonical name and looks like:

```json
"hint slider": {
  "directive": "INTERACTIVE",
  "aliases": ["hint slider", "hintslider"],
  "rules_family": "5.10",
  "widget_types": ["hintSlider"]
}
```

The fields mean:

- **`directive`** — what kind of thing this tag is. The main values:
  - `ELEMENT` — produces one piece of output (a heading, an image, a button).
  - `CONTAINER_OPEN` / `CONTAINER_CLOSE` — opens or closes a box that other content flows into (an activity, an alert).
  - `INTERACTIVE` — an interactive widget; hands over to the widget pipeline.
  - `SUBTAG` — a child tag that only means something inside a widget (`[front]`, `[back]`, `[Tab 2]`).
  - `PAGE_BOUNDARY` — ends the current output page (`[end page]`, `[LESSON]`).
  - `SECTION_MARKER` — marks a document region (`[MODULE INTRODUCTION]`).
  - `INLINE` — woven into the surrounding sentence (`[external link]`).
  - `DROP` — recognised and deliberately produces nothing.
- **`aliases`** — every folded spelling that should resolve to this tag. Matching is smart: it already copes with trailing numbers (`[Tab 3]` matches the alias `tab`), colons, and tags embedded in longer red sentences — so you only need a new alias when the *wording* itself is new.
- **`rules_family`** — a pointer into the prose specification `Tag_Interpretation_Rules.md` (section 5.x) describing this tag family's full behaviour. Keep it accurate; it is the documentation trail.
- **`widget_types`** — for `INTERACTIVE` tags only: which widget builder(s) this tag invokes. The value must match a key under `interactive_builders` in `Emit_Templates.json` and an entry in `Interactive_Boundary_ChildTag_Bank.json`.

**How to update — the three common cases:**

1. **A new spelling of an existing tag.** Find the tag in `tags`, add one string to its `aliases` array:

```json
"aliases": ["hint slider", "hintslider", "sliding hints"]
```

2. **A brand-new tag that renders like an existing element.** Add a new entry to `tags` with the right `directive`. If it should render identically to an existing tag, you can instead just add its wording as an alias of that tag.

3. **A brand-new interactive widget.** Add the entry here with `directive: "INTERACTIVE"` and a new `widget_types` name — then see [Recipe 3 in Part C](#recipe-3--add-a-brand-new-interactive-widget) for the two other files that complete the job.

**Advanced — the `_meta` adjustment blocks.** Near the top of the file, inside `_meta`, live three small rule engines that adjust how compound tags resolve:

- `tag_promote` — rewrites one resolved tag into another before anything renders. Today it holds one rule: `supervisor button` → `supervisor note` (so the supervisor reveal-panel machinery handles it). To redirect another tag the same way, add a rule object to `_meta.tag_promote.rules` with `from`, `to`, and optionally `to_directive` and an `env` off-switch name.
- `condition_primary_demote` — stops a modifier word (like "self check") from being mistaken for the main tag in a compound like `[Activity 3A - self check]`.
- `qualifier_alias_demote` — stops the lone word "interactive" from opening an activity box when no real widget is named. Since round 217 it also carries `standalone_becomes: "interactive"`: when the demoted word is the span's *only* tag and matches the bracket exactly — the writer typed just `[Interactive]` as a generic "a widget goes here" invocation — it is re-tagged as a generic widget opener instead of dropped, so the following instruction line and data table are captured into a placeholder (and wrapped in the invented activity box, see ActivitiesBuilder). Qualifier phrases like `[Interactive Stop Watch]` still demote exactly as before. Env `INTALIAS_OFF` reverts the bare form.

**Gotcha.** Aliases shorter than three characters must match exactly (this stops `p` matching inside ordinary words); `h1`–`h5` are the deliberate exception. After any lexicon change, the tag regression test in the development harness should still resolve ≥ 99.9% of the 9,557 historical tag variations.

---

## A2. Tag_Exceptions.json — rare one-off overrides

**What it holds.** A deliberately tiny escape hatch: literal answers for the rare red span the general matching genuinely cannot resolve. It currently holds exactly one entry (a quadruple-compound tag seen once in the whole library).

**Structure.**

```json
{
  "exceptions": [
    {
      "fragment": "h4 activity 5a - accordion (type the answer)",
      "resolution": { "primary": "h4", "also": ["activity", "accordion", "typing quiz"] },
      "note": "Quadruple-compound one-off. Found once in the corpus."
    }
  ]
}
```

The `fragment` is compared against the **folded** text of the whole bracket. If it matches, the pipeline uses the `resolution` verbatim: `primary` is the tag that drives rendering, `also` lists the other tags present.

**How to update.** Append another object to `exceptions`. **But pause first:** the file's own header warns that if this list starts growing, the real fix is almost always a new alias or rule in `Tag_Lexicon.json`. An exception is a patch; the lexicon is the cure.

---

## A3. Instruction_Cues.json — spotting notes to the design team

**What it holds.** The vocabulary that separates a *tag* from an *instruction*. Writers often type notes to the Creative Services team in red text — "CS: please crop this image", "Dev team – can you make this a dropdown?" — and these must become visible red+bold "Writers Note:" notes in the output (the note-prefix scheme in A5, `Emit_Templates.red_flag`), never be mistaken for tags or silently dropped. This file lists the words that give an instruction away. The Python test harness reads the exact same file, so the two always agree.

**Structure.** Three lists:

```json
{
  "addressee_prefixes": ["cs", "csc", "dev", "developer", "note to designer", "note", "creative services"],
  "addressee_separators": ":-–—,",
  "cue_patterns": ["cs", "please", "can you", "could you", "is it possible", "rhs", "right.hand column"]
}
```

- `addressee_prefixes` — openings that address someone ("Dev:", "Note to designer –").
- `addressee_separators` — the punctuation allowed after a prefix.
- `cue_patterns` — words/phrases anywhere in the span that signal an instruction. These are joined into one word-boundary regular expression, so plain words are safe to add; a `.` matches any single character (used in `right.hand` to cover both "right hand" and "right-hand").

**How to update.** Add one string to `cue_patterns` (or a new prefix to `addressee_prefixes`). For example, to catch "would it be possible":

```json
"cue_patterns": ["cs", "please", "can you", "could you", "would it be possible", ...]
```

**Gotcha.** Be conservative: an over-broad cue (a common word) would start converting genuine tags into notes. Prefer multi-word phrases.

---

## A4. Input_Doc_Rules.json — how the Word documents are read

**What it holds.** Everything about *reading* the input files (as opposed to writing output): which shades of red count as "red text", how red spans and tables are marked internally, which front-matter is boilerplate, how the media-list columns are recognised, and the repair rules for damaged tags. Read by `DocxExtractor.js` and `MediaListParser.js`.

**Structure — the top-level keys you will actually touch:**

- **`red_runs`** — the red-text rules:

```json
"red_runs": {
  "red_hex_values": ["ff0000", "ee0000"],
  "marker_open": "🔴[RED TEXT] ",
  "marker_close": " [/RED TEXT]🔴",
  "collapse_whitespace_only": true,
  "repair_missing_bracket": { "enabled": true, "clean_hows": ["exact", "denumbered", "denumbered_head"] }
}
```

  - `red_hex_values` — **if a writer uses a new shade of red** and their tags stop being recognised, add the six-digit hex colour here. This is the single most common fix in this file.
  - `repair_missing_bracket` — the rule that heals a tag typed as `H2]` instead of `[H2]`.
- **`formatting_markers`** — how bold (`**`), italic (`*`) and bullets (`• `) are encoded internally. Do not change these; the whole pipeline expects them.
- **`content_start`** — the phrases that mark where real content begins (everything before `[TITLE BAR]` is template boilerplate and gets trimmed). If a new template revision changes the front matter, extend `content_start_fragments`. The MTK "Te Aka Taumatua" bilingual template (the PNR family) has its own opener list, `content_start_fragments_dropdown` — kept separate so the `REODROPMENU_OFF` toggle can revert that whole round; `TrimFrontMatter` only uses it as a *rescue* when the standard start would otherwise be a `[LESSON N CONTENT]` marker (i.e. the overview would be thrown away).
- **`front_matter_metadata.fields`** — the labelled front-matter fields harvested before trimming (Subject, Course, Module Code…). Add a field here if the template gains a new labelled line worth capturing. The PNR family's front matter is a TABLE, not labelled lines — `table_row_fields` lists which fields may also be read from two-column table rows (currently only `moduleName`, deliberately not `course`, so the Course-is-title-backup rule can never start firing where it didn't before).
- **`media_table`** — how the media list is recognised:

```json
"media_table": {
  "min_header_matches": 3,
  "columns": {
    "itemNo":      { "aliases": ["item no", "item number", "no."] },
    "description": { "aliases": ["description", "description of item"] }
  }
}
```

  **If the media-list template gains a renamed column heading**, add the new heading to that column family's `aliases`. This is the second most common fix here.
- **`unsupported_pathways`** — template types the converter politely refuses (with the message shown to the user).
- **`table_markers`, `wt_page_tracking`, `input_shapes`, `trailing_content`** — internal serialisation and page-tracking rules; rarely touched.

**How to update.** The file's own extension rule says it plainly: *"New boilerplate block, new media-table column heading, new red shade, new template signature = a data edit HERE."*

---

## A5. Emit_Templates.json — every HTML output shape ★★

**What it holds.** The central file of the whole system. Every piece of HTML the converter can emit is a template string in here, with `{curly}` placeholders the engine fills in. If you want to change what any output *looks like* — a box, a heading, a menu, a placeholder, a footer — the change is in this file. It is large (~340 KB) but almost entirely self-documenting: most sections carry `_comment` fields explaining themselves.

**The top-level map.** These are all the top-level keys and what each governs:

| Key | Governs |
|---|---|
| `red_flag` | The red+bold designer-note paragraphs ("Writers Note:" / "Red Flag:" / "Designer/Developer To Do:") |
| `elements` | Headings, paragraphs, lists, tables, inline links, hover definitions, bilingual rendering, media-related text rules |
| `callouts` | The callout boxes: alert, important, whakataukī, quote, supervisor note… |
| `activity_wrapper` | The activity boxes: opening markup, numbering, supervisor-note variant |
| `image` / `video` / `audio` | Media embeds and image placeholder forms |
| `buttons` | Every button form (plain, linked, dropbox, download, external link…) |
| `embeds` | Embedded iframes (padlet, forms…) |
| `interactive_placeholder` | The orange dashed "un-built widget" box, and the interactives.txt options |
| `interactive_builders` | The markup for each widget type the converter can actually build |
| `skeleton` | Doctype, `<html>` attributes, `<head>`, body open/close |
| `header` | The page header: module-code chip, title `<h1>`s, title-splitting rules, menu buttons |
| `menu` | Every module-menu shape and transformation |
| `footer` | The footer nav and prev/next/home links |
| `body_region` | Page-body-wide behaviours: heading re-levelling, row grouping, panels, list nesting |
| `container_auto_close` | When an open box (activity, callout) closes automatically |
| `page_split_rules` | Special page-splitting behaviours |
| `output_naming` | The output filename patterns (`{code}-{NN}.html`) |

**Reading a template.** A typical entry:

```json
"red_flag": {
  "form":      "<p class=\"cv2-note\" style=\"color: red; font-weight: bold;\">Red Flag: {text}</p>",
  "cs_form":   "<p class=\"cv2-note\" style=\"color: red; font-weight: bold;\">Writers Note: {text}</p>",
  "todo_form": "<p class=\"cv2-note\" style=\"color: red; font-weight: bold;\">Designer/Developer To Do: {text}</p>"
}
```

The engine fills `{text}`. An unknown placeholder is deliberately left visible in the output rather than silently blanked — so a typo in a template announces itself.

**The note-prefix scheme (design-team rule, July 2026).** Every designer-facing note is red **and bold**, prefixed by its *source*: **"Writers Note:"** = something the writer typed for the team; **"Red Flag:"** = a problem the converter itself found; **"Designer/Developer To Do:"** = a deferred asset/URL/setup of a correctly-built pattern; **"Note from {author}:"** = a captured Word comment from a whitelisted reviewer (that one lives in `Comment_Authors.json`, not here). The old "CS:" / "RED FLAG:" wording is kept in-file as `legacy_form`/`legacy_cs_form` and the whole scheme reverts with the env toggle `NOTESCHEME_OFF` — do not delete the legacy forms. These prefixes are a *forward-looking design-team decision*: the human-built reference library predates them, so never "correct" the wording back toward what an old finished module shows (the rule is recorded with an `overrides_gold` marker in `Subject_Global_Parameters.json → _universal_conventions`).

**The sections you will edit most:**

1. **`callouts.by_tag`** — one entry per callout box type. To change the alert box's markup, edit:

```json
"callouts": {
  "by_tag": {
    "alert": {
      "open": "<div class=\"alert{modifiers}\">",
      "close": "</div>",
      "lead_element": "h4",
      "wrap_content": true
    }
  }
}
```

   **To add a whole new callout type** (say the writers invent `[reminder]`): add a `"reminder": { "open": ..., "close": ... }` entry here, and add the tag itself to `Tag_Lexicon.json` with directive `CONTAINER_OPEN`. The converter's callout dispatcher is fully data-driven — no code change. (An unknown container tag currently produces a visible red note saying exactly this: "add it to Emit_Templates callouts".)

2. **`elements.heading`** — how writer heading tags map to real heading levels:

```json
"heading": {
  "form": "<{tag}>{content}</{tag}>",
  "logical_to_element": { "body_shift": 1, "min_tag": "h2", "max_tag": "h5" }
}
```

   `body_shift: 1` means a writer's `[H2]` becomes an `<h3>` (shifted down one), because `<h1>`/`<h2>` are reserved for the page header. A separate page-wide "re-levelling" pass (configured under `body_region.heading_relevel`) then tidies the whole page's heading ranks.

3. **`interactive_builders`** — the markup for each widget the converter can build: `modal`, `selfCheck`, `dragAndDrop`, `glossary`, `hintSlider`, `accordion`, `speechBubble`, `flipCard`, `tabs`, `carousel`, `clickDrop`, `shapeHover`. Each entry carries a `_comment` block describing exactly what input shape it accepts, its template strings, and usually an `enabled` flag. The stated principle at the top of the section: *"Never half-build: build cleanly or keep the honest placeholder."*

4. **`menu`** — the largest and most intricate section, because module menus are the most varied part of the human-built library. Key sub-parts: `shells` (the outer HTML for each menu archetype — `tabs`, `simplified`, `two_col_li`, `two_col_offset`, `fundamentals_li`…), `tab_map` (which headings route to which tab), `extra_tabs` (sections promoted to their own tab, per family), `two_col_li` / `tab2_cols` (the two-column layouts, per family), `bilingual_heading_reduce` (which families reduce "reo | English" headings to English). Most of these are gated by small **registries keyed by subject-and-phase group** (like `"AGH|NCEA"`) that were *measured* from the finished library — when adding a family to one of these registries, follow the pattern of the existing rows.

5. **`interactive_placeholder`** — the orange dashed box for un-built widgets, plus three flags controlling the `{CODE}_interactives.txt` file (`manifest_unbuilt_only`, `manifest_raw_verbatim`, `manifest_faithful_content`).

**How to update, in general.** Find the section that owns the output you want to change (searching this file for a distinctive class name from the output HTML almost always lands you in the right place), edit the template string, reload the converter page, convert a test module. The file's own extension rule: *"New style / class / menu shape / footer arrangement = a data edit here. If a change seems to need engine code, stop — design error."*

---

## A6. Interactive_Boundary_ChildTag_Bank.json — where widgets start and stop

**What it holds.** For every interactive widget type, the rules deciding **which content belongs to the widget** — where its capture starts, what counts as a member, and what ends it. When a widget "swallows" a following section that should have rendered normally (or stops too early and leaks its own content), this is the file to tune.

**Structure.** Two parts:

- **`_meta`** — the global boundary rules shared by all widgets:
  - `opener_rule.opener_tags` — tags that can precede and belong to a widget (like `[Activity]`).
  - `member_rule` — the big one: `terminators_absolute` (tags that always end a widget), `terminators_conditional`, `callout_tags_terminate`, and ~30 measured special-case sub-rules (things like `lone_heading_section_break`, `body_terminates_after_face`, `trailing_media_extract`) each documented with the module that motivated it.
  - `widget_type_taxonomy.variant_of` — folds a variant tag onto its parent builder (e.g. `rotateBanner` → `carousel`).
- **`interactives`** — one entry per widget type (~45):

```json
"flipCard": {
  "heading_is_terminator": false,
  "uses_data_table": true,
  "signature_subtags": ["back", "data marker", "front", "shape n"]
}
```

The most important field is **`heading_is_terminator`**: does a `[H2]`–`[H5]` heading END this widget (`true` — the safe default) or is it legitimate *internal* content, like a slide title (`false`)? If unsure, use `true`: the failure mode is "the heading renders as a normal section", which is safe.

**How to update.**

- **New widget type:** add an entry under `interactives` with at least `heading_is_terminator`, plus `uses_data_table` and `signature_subtags` if it has child tags.
- **A widget over-captures:** first check its `heading_is_terminator`; then look through `_meta.member_rule` for an existing rule that nearly fits before inventing a new one — most over-capture classes have already been measured and named.
- **A new tag should always end widgets:** simplest path — if it is a callout, adding it to `Emit_Templates.json → callouts.by_tag` is enough (callout tags are automatically treated as terminators). Otherwise add it to `terminators_absolute`.

**The round-217 additions (the boundary-audit round).**

- **`interactives.interactive`** — the entry for the *bare generic invocation*: a writer who types just `[Interactive]` (no widget name) and follows it with an instruction line and a data table. It is conservative on purpose: `heading_is_terminator: true` and `uses_data_table: true`, so a `[Body]` element appearing after the captured table ends the capture (the writer is resuming normal prose).
- **`_meta.member_rule.bare_invocation_dissolve_empty`** — the safety valve for that same invocation: if the bundle it opens captures **no table and under 40 characters of member text**, the bundle dissolves and the span goes back to being an ordinary red note (there is nothing buildable to hand off). Raise/lower `min_member_chars` or empty the `types` list to tune it; env `INTALIAS_OFF` turns the whole invocation feature off.

---

## A7. Interactive_Wrapper_Catalogue.json — reference only

**What it holds.** A catalogue of the outer wrapper HTML (`tag`, `classes`, `attributes`, known `modifiers` and `variants`) the human developers use for each of the 49 widget types. **It is deliberately not loaded by the engine** — it is reference reading for a person deciding how a new widget builder should look. (A comment in `Config.js` explicitly says not to re-add it to runtime loading.)

**How to update.** Append an object to the `interactives` array when a new widget type is catalogued. Purely for the record.

---

## A8. Manifest_Patterns.json — naming the widget data shapes

**What it holds.** The 13 named "data pattern" signatures used in `{CODE}_interactives.txt` to tell the developer what shape of captured data a widget has (e.g. pattern 8 "Speech Bubble in Table Row"). Purely descriptive labels for the hand-off file — they change no HTML.

**Structure and update.** An array of `patterns`, each:

```json
{ "id": 8, "name": "Speech Bubble in Table Row", "used_by": ["speechBubble"],
  "signals": { "table": true, "type_required": true } }
```

To add a pattern, append an object with a new `id`, a `name`, the widget `used_by` list, and `signals` (`table`: true/false/null, optional `subtags_any` list, optional `type_required: true` as a hard gate). The scoring is: matching type +2, matching table shape +1 (wrong shape −2), matching subtag +2; highest score wins, and a zero score falls to "unclassified" with a visible red flag. The file's own rule: new shapes are a data edit here, never a code change.

---

## A9. Menu_Scaffold_Registry.json — which menu each family gets

**What it holds.** For every subject-and-phase group (keys like `"AGH|NCEA"`) and for individual module series, the menu **type** used on overview pages and lesson pages: `tabs`, `simplified`, or `none`. Measured from the human-built library, with the vote counts kept as `_evidence`.

```json
"AGH|NCEA": {
  "overview": "tabs", "lesson": "simplified",
  "_evidence": { "overview": { "tabs": 9, "simplified": 0, "none": 0, "n": 9 } }
}
```

**Resolution order:** a `series` entry beats its `groups` entry, which beats `global_default`. The older, superseded values are preserved in-file under `legacy_groups`/`legacy_series` (an off-switch can revert to them) — leave those alone.

**How to update.** If a family's menu type is wrong, edit its group (or add a series override). Because this is a *measured* registry, the better path when many rows need changing is to re-run the mining script in the development harness (`derive_menu_type.cjs`), which regenerates it from the finished library.

---

## A10. Html_Convention_Registry.json — measured house conventions

**What it holds.** Per subject-and-phase group: the dominant menu *archetype* (the layout within the menu type, e.g. `two_col_li`), the callout lead element, and the video host — each with its measured share (e.g. `"12/12"`), plus per-series deviations. Read by `ConventionResolver.js`; the resolution order is series deviation → group dominant → global default.

**How to update.** Rebuilt by the harness script `build_convention_registry.py` from the finished library. Hand-edit only for a quick targeted fix; regeneration is the proper maintenance path after new modules ship.

---

## A11. Style_Anchor_Registry.json (+ the Majority/Deviations companion) — page structure per family

**What it holds.** The structural rulebook per subject → base code → level: the `<body>` class, footer class, menu type, page model (single-file vs multi-file), `<html>` level attributes, and which modules belong to each level. `ModuleResolver.Resolve` walks it top-down — `defaults`, then the subject's rules, then the base's, then the level's `delta` — each layer overriding the last:

```json
"defaults": { "body_class": "container-fluid", "footer_class": "footer-nav",
              "menu_type": { "overview": "tabs", "lesson": "simplified" } },
"1-10 Arts": { "bases": { "ARFUN": { "levels": { "ARFUN0": {
  "members": ["ARFUN01", "ARFUN02"],
  "delta": { "page_model": "single-file", "page_model_exceptions": ["ARFUN04"] } } } } } }
```

**The companion file** (`..._Majority_And_Deviations.json`) is the fallback for a module code the main registry has never seen: per subject and phase band, the "majority" instruction set a brand-new series most likely follows.

**How to update.** To fix one family's page shell (e.g. its `page_model` is wrong), edit that level's `delta`. Both files are measured from the finished library and are normally *regenerated* rather than hand-edited at scale. Special registry values are meaningful: `"—"` / `"n/a"` / `"absent"` mean "this element is deliberately absent" — not missing data.

---

## A12. Acks_Formats.json — acknowledgement wording and rules

**What it holds.** Everything about the acknowledgements section: the container markup, the fixed standing legal text, one entry template per media source, how a URL is classified into a source, the extraction patterns (YouTube video id, iStock asset id), and the "ACK-TODO" contract (anything that cannot be honestly derived becomes a visible ❗ marker, never a guessed field).

**Structure highlights:**

```json
"entry_templates": {
  "istock":  "{TypePrefix}: {Title}, iStock {AssetId}, Getty Images.{Adapted} Used with permission.",
  "youtube": "Video: {Title}, {Channel}, <a href=\"{URL}\" target=\"_blank\">{URL}</a>, retrieved {RetrievedDate}. Used in online learning within the exception for education."
},
"source_classification": { "by_domain": { "istockphoto.com": "istock" }, "by_source_keyword": {} },
"type_prefix_map": { "image": "Image", "video": "Video" }
```

**How to update — the common case, a new media source:**

1. Add its wording to `entry_templates` (a new key, e.g. `"canva"`).
2. Point its domain at that key in `source_classification.by_domain` (e.g. `"canva.com": "canva"`).
3. If the wording reuses an existing template's structure, step 1 can be skipped and step 2 just points at the existing key.

If the new source needs *logic* no template can express (like YouTube's title lookup), it also needs a small builder function in `AcksBuilder.js` — see that file's section in Part B.

---

## A13. Comment_Authors.json — whose Word comments appear

**What it holds.** The whitelist of Creative Services team members whose native Word comments (the margin bubbles) get surfaced as red notes in the output, how those notes render, and a content filter that drops non-actionable boilerplate (routine copyright commentary). Since July 2026 a surfaced comment renders **"Note from {author}: {text}"** in red + bold — the author and text verbatim, never reworded (the design team's rule; the old bare "{author}:" lead is kept as `render.legacy_form` and returns under the env toggle `NOTESCHEME_OFF`).

**How to update — a new team member:**

```json
"authors": [
  { "display": "Kate Scanlon", "enabled": true, "seen_as": ["Kate.Scanlon"] },
  { "display": "New Person",   "enabled": true, "seen_as": [] }
]
```

Matching already normalises case, dots, and "Last, First" order, so `seen_as` only needs genuinely different spellings Word might record. Setting the top-level `enabled` to `false` (or the env toggle `COMMENTS_OFF`) switches the whole feature off.

---

## A14. Template_Modes.json — body class ordering

**What it holds.** The rules that put a page's `<body>` class tokens in the canonical order: base tokens (`fundamentals`, `inquiry`) come *before* `container-fluid`, modifiers (`mathJax`, `reoTranslate`) come *after*, and some tokens carry body attributes (like `language="reo"`).

**How to update.** Add a key under `bases` or `modifiers` (with optional `body_attrs`). This file only *orders* tokens the style registry already assigns; it does not invent new page modes.

---

## A15. Overview_Menu_Heading_Lexicon.json — known menu headings

**What it holds.** A frequency count of overview-menu heading phrases across the whole human library ("learning intentions": 190, "success criteria": 73, …). The menu builder uses "is this phrase a known heading, seen at least `min_count` times?" as a confidence signal when deciding whether a bold lead-in like `**Connections:** some text` is a menu heading that should be split from its content. Important design point: it is a *general vocabulary of phrases*, never keyed by module code — so it guides without copying any one module's answers.

**How to update.** Rebuilt by the harness script `build_menu_heading_lexicon.py`. To hand-add a phrase quickly, insert `"the folded phrase": 3` (any count ≥ `min_count`, which is 3) into `headings`.

---

## A16. The dormant pair — Precedence_Cascade.json and Subject_Global_Parameters.json

Both are loaded by the engine but currently **switched off**, so they change nothing today. They exist so a future round can turn each on, one measured scope at a time.

- **Precedence_Cascade.json** defines the six-level "authority cascade": when a layout detail isn't derivable from the Writers Template, ask what the nearest previously-built *sibling module* did (same series and template → same subject/phase/template → … → whole library), only accepting an answer where the group is solidly consistent. The live switch is `engine_inherit.enabled` (currently `false`).
- **Subject_Global_Parameters.json** ("doc 14") holds per-subject house-style defaults — e.g. "all BLL activity boxes are green" — each family with its own `active` flag under a master switch `_meta.master_enabled` (currently `false`). It also carries two record blocks the audit tooling reads: `_cross_cutting` (rules spanning several families) and `_universal_conventions` (the design team's *universal* rules taken from their Change Ledger — note prefixes, "never col-md-10 activity wrappers", alt-text and acknowledgement rules). Every family and both blocks are marked `overrides_gold: true`: these rules are **newer than the finished human-built library**, so where a converted module follows a rule and an old finished module doesn't, the converted module is *correct* — a stocktake or audit must record the difference as intentional, never "fix" the converter back toward the old module.

**How to update.** Leave both alone in normal maintenance. Turning either on is a deliberate, tested change, not a routine edit. A new design-team ruling belongs in `_universal_conventions` (universal) or the right family section (subject-scoped), always with `overrides_gold` semantics stated.

---

## A17. The machine-built measurement files — do not hand-edit

- **Module_Structure_Index.json** (engine-loaded) — for every module in the library: its metadata (subject, template type, phase, series) and the measured HTML structure of each of its elements. The data substrate for the cascade above and a couple of small lookups. Regenerated by the harness tooling whenever the library grows.
- **Granular_Scaffold_Registry.json**, **Scaffold_Consensus.json**, **Module_Menu_Scaffold.json** — measurement outputs read only by the Python test tooling in the development harness, **not by the engine**. Safe to ignore in day-to-day work; regenerated by their build scripts.

---

## A18. The three prose specifications (`.md` files)

These are the human-readable design authority *behind* the JSON; the engine never reads them, but they are the best explanation of *why* the rules are what they are:

- **Tag_Interpretation_Rules.md** — the master specification of how each tag family behaves, section by section (the `rules_family` numbers in the lexicon point here). The core mental model: *a tag is a typed boundary marker; its content is the black text that follows, up to the next marker.*
- **Tag_Normalisation_Spec.md** — exactly how tag matching works: fold the text → extract the bracket fragments (repairing damage) → resolve each against the lexicon (exceptions first, then exact / de-numbered / embedded matching).
- **Interactive_Boundary_Rules.md** — the widget block model: `[openers] → [interactive tag] → [members…] ‖ [terminator]`, and how the scanner decides where a widget ends.

**When you make a significant rule change in the JSON, add a line to the matching spec** so the paper trail stays honest.

---

# Part B — The engine files

Every engine file follows the same shape, which makes them easy to read:

- A **plain-English header comment** at the top explaining the file's job, its place in the pipeline, and its "never do this here" rules. **Always read the header first** — it is the most reliable documentation and it is kept up to date.
- One class of **static methods** (no objects are created; you call `ClassName.MethodName(...)`). Methods whose names start with `#` are private to the file.
- All shared state travels in the **`run`** object (a `ConversionRun`) passed from method to method.
- All rules are read from **`DataService.Data.<Key>`**, which is the loaded content of the data files.
- Environment **off-switches** are read defensively: `typeof process !== "undefined" && process.env && process.env.SOMETHING_OFF` (this pattern is safe in both the browser, where `process` doesn't exist, and Node).
- The last line of each file is a small `module.exports` hook so the Node batch tool can load it; browsers ignore it.

The sections below run in pipeline order. Position hints ("about a third of the way down") are given instead of line numbers, since lines shift as files evolve — searching for the quoted function names is the reliable way to land in the right place.

---

## B1. Config.js — version and addresses

**What it does.** The single home for app-level plumbing: the version number, the list of data files to load, the DOM element ids, and the UI strings. It holds *no* module knowledge — the header calls it "the address book".

**Main contents, top to bottom:** `AppVersion` (near the top) → `DataFiles` (the key-to-path map) → `Selectors` (element ids used by `index.html`) → `Strings` (user-facing wording) → `FULL_BREAK(message)` (the last-resort error screen).

**How to update — the two jobs you'll do here:**

1. **Bump the version after any shipped change.** Near the top:

```js
static AppVersion = 260617.84;
```

   The format is `YYMMDD.iteration`. It shows in the UI badge and the summary; it is never written into converted pages, so bumping it never changes output.

2. **Register a new data file.** In the `DataFiles` map, add one line following the pattern:

```js
static DataFiles = {
    TagLexicon:     "../data/Tag_Lexicon.json",
    TagExceptions:  "../data/Tag_Exceptions.json",
    // ...
    YourNewKey:     "../data/Your_New_File.json",
};
```

   **Also add the matching entry to `_modules.json` → `data_map`** (`"YourNewKey": "Your_New_File.json"`) so the batch tool loads it too. From then on the file is available everywhere as `DataService.Data.YourNewKey`.

**Gotcha.** A comment in `DataFiles` says `Interactive_Wrapper_Catalogue.json` is deliberately NOT loaded — don't re-add it.

---

## B2. DataService.js — the loader

**What it does.** The only file that talks to the outside world. At startup, `Init()` fetches every file listed in `Config.DataFiles` (in parallel) into the global `DataService.Data` store, then runs a few sanity checks that stop the app loudly if a critical file is missing or malformed. It also owns `FetchOembed`, the one runtime web request: looking up a YouTube video's title for the acknowledgements.

**Main methods:** `Init()` (top) → `#fetchJSON(url)` (middle) → `FetchOembed(videoUrl, videoId)` (bottom, with a per-video cache).

**How to update.** Normally you don't — adding a data file is done in `Config.js` (above) and this file picks it up automatically. The one edit that belongs here: if a new data file is *critical* (the app should refuse to start without it), add a guard alongside the existing ones inside `Init()`, which look like:

```js
if (!this.Data.TagLexicon?.tags) throw new Error("Tag_Lexicon.json loaded but has no tags");
if (!this.Data.EmitTemplates?.red_flag) throw new Error("Emit_Templates.json loaded but has no red_flag form");
```

**Gotcha.** Data files are "load or die" by design — a converter running on partial rules and quietly "coping" is exactly the failure mode this project bans. The oEmbed fetch is the opposite: it degrades gracefully into a visible ACK-TODO marker, never a made-up title. Files are fetched with caching off, so the workflow *edit a JSON file → reload the page → convert again* always sees your change.

---

## B3. Utils.js — shared helpers

**What it does.** Small, pure helper functions used everywhere: `Fold` (the text-normalising step behind all matching), `EscapeHtml`, `FillTemplate` (fills `{token}` slots in the data templates), `Slugify`, `TitleCaseWords`, `Pad2`, `TodayStamp`, `MapSeries` (a polite one-at-a-time async loop used for the YouTube lookups).

**How to update.** Add new *pure* helpers here (same input → same output, no DOM, no fetching). Two contracts to preserve:

- `Fold` must keep behaving exactly like its Python twin in the test harness — and folded text is for **matching only**, never for content the reader sees.
- `FillTemplate` deliberately leaves an unknown `{token}` visible in the output instead of blanking it — several files rely on that as a typo alarm:

```js
return template.replace(/\{(\w+)\}/g, (whole, key) =>
    values[key] ?? whole
);
```

---

## B4. ZipReader.js and ZipWriter.js — the zip plumbing

**What they do.** A `.docx` is a zip archive. `ZipReader` opens one in the browser with no libraries (using the built-in `DecompressionStream`) and hands out the XML files inside as text. `ZipWriter` does the reverse for the "Download all as .zip" button, storing the output pages uncompressed.

**How to update.** Almost never. The one realistic change — a writer's docx using an exotic compression method — goes in `ZipReader.ReadText`, where the two supported methods are handled:

```js
if (entry.method === 0) return new TextDecoder().decode(compressed);
if (entry.method === 8) {
    const stream = new Blob([compressed]).stream()
        .pipeThrough(new DecompressionStream("deflate-raw"));
    ...
}
throw new Error(`ZipReader: unsupported compression method ${entry.method} for "${name}"`);
```

Add a new `if (entry.method === N)` branch before the `throw`.

---

## B5. DocxExtractor.js — reading the Word document

**What it does.** Turns the raw Word XML into the converter's working material: an ordered list of **blocks** (paragraphs and tables). Each paragraph block's text encodes everything downstream needs: red spans wrapped in `🔴[RED TEXT] … [/RED TEXT]🔴` markers, bold as `**`, italic as `*`, bullets as `• ` (indented two spaces per nesting level), plus hyperlink targets, the Word page number, and any margin comments. This marker format matches the validated historical corpus exactly, so a fresh upload runs the identical downstream pipeline.

**Main methods, top to bottom:**

- `Extract(zip)` — the entry point (top of file): reads `document.xml` and its companions, drives the parse, returns `{blocks, rels, mtkFlag, hasContentStart, metadata}`.
- `IsContentStart` / `#extractMetadata` / `LooksLikeWritersTemplate` — the front-matter helpers (first third): find where real content begins, harvest the labelled front-matter fields, and classify "is this upload even a Writers Template?".
- `TrimFrontMatter` and `RepairContentTags` (middle) — drop the boilerplate before the title bar, then heal red tags typed with a missing opening bracket (`H2]` → `[H2]`). `TrimFrontMatter` is the one shared choke point both entry points call. Since round 212 `TrimFrontMatter` also carries the drop-down-menu *rescue*: when the standard chain's first content start is a `[LESSON N CONTENT]` block (not a `[TITLE BAR]` one) and a `[Content for DROP DOWN MENU]` paragraph exists earlier, the document opens there instead — this is how the PNR bilingual family keeps its overview (menu + title + introduction) out of the discarded front matter. `#extractMetadata` reads the PNR family's metadata TABLE rows for the fields in `front_matter_metadata.table_row_fields` (only `moduleName`).
- `#parseDocument`, then `#parseParagraph` and `#parseTable` (the final third) — the actual XML walking. `#parseParagraph` is called "the heart of the extractor" in its comment: it merges the runs of one paragraph into the marker text, deciding red vs black per run.

**Where the rules live.** Almost all behaviour is driven by `Input_Doc_Rules.json` (see A4): red shades, markers, content-start phrases, front-matter fields. Change those there, not here.

**Extension point — a new repair pass.** If a new class of "damaged tag" needs healing at source (like the missing-bracket repair), model it on the existing one: add a private helper next to `#repairLeadingBracket` and call it from the loop inside `RepairContentTags`, which looks like:

```js
for (const b of blocks) {
    if (b.kind !== "para" || !b.text || b.text.indexOf("]") < 0) continue;
    b.text = b.text.replace(RED, (whole, inner) => {
        const fixed = this.#repairLeadingBracket(inner, normaliser, cleanHows, excludeTags);
        return fixed === null ? whole : "\u{1f534}[RED TEXT]" + fixed + "[/RED TEXT]\u{1f534}";
    });
}
```

**Gotchas from the file's own comments.**

- Hyperlink URLs live in a separate part of the docx (`word/_rels/document.xml.rels`), never in the visible text — "the single most important extraction rule".
- Google-Docs exports mark nearly every paragraph with a "page break = no" flag; only a bare or true flag is a real page break.
- The "MTK WRITERS TEMPLATE" heading appears in ordinary templates too — on its own it is *not* proof of a bilingual module.
- `<w:b w:val="0"/>` in Word XML means bold explicitly OFF.

---

## B6. MediaListParser.js — reading the media list

**What it does.** Finds the media table among the extracted blocks (whether the media list is its own file or embedded in a combined document), maps its columns by the header aliases in `Input_Doc_Rules.json`, throws away header/reminder/example rows, and returns clean media items for the acknowledgements builder.

**Main methods:** `FindMediaTable(blocks)` (upper half — recognises the table by matching at least three column-heading families) and `ParseItems(found)` (lower half — walks the rows, resolving each row's real URL).

**How to update.** A renamed column heading → add the alias in `Input_Doc_Rules.json → media_table.columns` (see A4). A new kind of junk row to skip → add a `continue` guard in `ParseItems` next to the existing ones:

```js
if (cells.length <= 1) continue;
const firstFolded = Utils.Fold(this.#cleanCell(cells[0]));
if (firstFolded.startsWith("reminder")) continue;
```

**Gotcha (their words: "THE ONE RULE THAT BURNS PEOPLE").** The URL a writer pasted lives in the document's link registry, not the visible cell text — Word truncates the visible text. Always prefer the row's link target.

---

## B7. ConversionRun.js — the shared clipboard

**What it does.** One instance is created per conversion, and every stage reads from and writes to it: the module code, the resolved rules, the parsed blocks, the produced pages, and the running tallies (red flags, ACK-TODOs, notes). It also holds the two user options — `imageMode` (`"P"` placeholder images or `"D"` direct) and `interactiveMode` (`"inline"` or `"extract"`) — and the browser-only progress callback.

**The surfacing contract (its most important rule).** Nothing ambiguous may ever be swallowed silently. If a stage "handles" something odd, it must say so via `run.AddNote(level, stage, text)`, `run.CountRedFlag()`, or `run.CountAckTodo()` — those feed the summary panel the user sees.

**How to update.** Add new fields (for a later stage to read) or new tally kinds here — but put no decision logic in this file; it is a plain data container. To surface a new number in the summary panel, add it to the object returned by `Summary()` (bottom of the file) and render it in `SummaryReporter.js`.

---

## B8. TagNormaliser.js — understanding the red spans

**What it does.** The only tag-matching code in the engine. Given one red span, it answers: which tags are in here, which one is in charge (the "primary"), and is this really a tag at all — or a writer's instruction, or noise? It is a faithful port of the validated Python reference pipeline, tested against all 9,557 historical tag variations (99.99% resolved).

**Main methods, top to bottom:**

- The `constructor` (top) compiles the lexicon: alias matching tables, exception lookups, and the instruction-cue regular expressions. It throws loudly on malformed data.
- `GetWidgetTypes(canon)` — which widget(s) a tag invokes.
- `RenderText(raw)` (upper middle) — extracts the *display* text embedded in a span, in original capitalisation (never folded).
- `#matchOne` and `#resolveFragment` (middle) — the matching machinery for one bracket fragment: exact match, then match-ignoring-numbers, then head-of-fragment, then embedded.
- **`Parse(raw)`** (lower half) — the main entry point everything else calls: folds the span, extracts the bracket fragments (repairing damage), resolves each, applies the precedence rules and the `_meta` adjustments (demotes/promotes), and classifies the whole span as `tag` / `instruction` / `noise`.
- `IsInstructionDominant` (after Parse) — a second-opinion check the widget scanner uses.

**How to update.** Practically never in this file — its header says: *"If a tag change seems to need an edit in THIS file, stop — that is the v1 death spiral."* Tag knowledge goes in `Tag_Lexicon.json` / `Tag_Exceptions.json` / `Instruction_Cues.json` (Part A). The one data-driven mechanism worth knowing lives near the end of `Parse` — the `tag_promote` loop that rewrites one tag into another, driven entirely by lexicon data:

```js
const tpr = this.#lexicon?._meta?.tag_promote;
if (tpr && tpr.enabled !== false && primary) {
    for (const rule of (tpr.rules ?? [])) {
        ...
        for (const t of tags) {
            if (t.tag === rule.from) {
                t.tag = rule.to;
```

Add rules to `Tag_Lexicon.json → _meta.tag_promote.rules` — no code change.

**Gotcha.** If this file *is* ever changed, both regression harnesses (JS and Python) must be re-run — the two implementations are kept in exact agreement.

---

## B9. ModuleResolver.js — who is this module?

**What it does.** Three jobs: detect the module code (from filenames first, then the front matter); resolve that code's house style through the Style Anchor Registry cascade (defaults → subject → base → level, with a majority-based fallback for brand-new series); and provide **`PrepareRun`** — the one shared preparation routine both the browser and the batch tool must call, so the two entry points can never drift apart (they once did, and produced different output for the same module).

**Main methods, top to bottom:** `DetectModuleCode` → `Resolve` (the registry cascade walk) → `PrepareRun` (the choke point: classify the uploads, detect + resolve, apply the unsupported-template refusal, parse the media list, trim the front matter) → `PhaseKeyFor` → the private registry-walk helpers.

**How to update.**

- **A family's structure is wrong** → edit the registry data (A11), not this file.
- **A new template pathway must be refused** → add an entry to `Input_Doc_Rules.json → unsupported_pathways`; the matcher here reads it generically.
- **A new resolution layer** (rare) → the cascade merge in `Resolve` is a sequence of overlay steps you can extend; later overlays win:

```js
Object.assign(rules, structuredClone(subject.subject_rules ?? {}));
Object.assign(rules, structuredClone(base.base_rules ?? {}));
if (level) {
    Object.assign(rules, structuredClone(level.delta ?? {}));
}
```

**Gotchas.** The header bans `if (moduleCode === "…")` outright. And the statement *order* inside `PrepareRun` is load-bearing — reordering seemingly independent steps risks changing the output of already-converted modules. A parity test (`_verify_entry_parity.cjs` in the harness) guards this file's contract.

---

## B10. ConventionResolver.js — attach the measured conventions

**What it does.** A small stage that reads `Html_Convention_Registry.json` for the module's group and attaches the results to `run.conventions`: the menu archetype for overview and lesson pages, the callout lead element, the video host. Series deviations override the group's dominant values.

**How to update.** To track a *new* convention dimension, add one read line in `Resolve` (the file's only method) next to the existing ones, and populate the registry:

```js
out.menu.overview = group.menu?.overview?.dominant ?? null;
out.menu.lesson   = group.menu?.lesson?.dominant ?? null;
out.calloutLead   = group.callout_lead?.element ?? null;
out.videoHost     = group.video_host?.host ?? null;
```

---

## B11. TemplateModeResolver.js — body class ordering

**What it does.** Composes the final `<body>` class string in the canonical token order (bases like `fundamentals` before `container-fluid`, modifiers like `mathJax` after) and merges any body attributes — all driven by `Template_Modes.json`. One method, `Resolve(bodyClassRaw, run)`.

**How to update.** New tokens are a data edit (A14). The only code-level knob is the canonical order itself, one line near the bottom of `Resolve`:

```js
const bodyClass = [...baseTok, core, ...otherTok, ...modTok].join(" ");
```

---

## B12. PageSplitter.js — cutting the document into pages

**What it does.** Two steps. `BuildItemStream` (top of file) splits each paragraph block into an ordered stream of **items** — parsed red tag spans (each carrying the black text that follows it), plain black runs, and tables. This item stream is what the whole rest of the converter walks. Then `Split` (the bulk of the file) groups the items into output pages, applying the validated assembly rules: `[end page]` and `[LESSON]` boundaries, the single-file vs multi-file page model from the registry, bilingual page conventions, plus post-passes that harvest each page's title and de-duplicate repeated labels.

**How to update.**

- **A page splits (or doesn't) where it shouldn't:** first check the module family's `page_model` in `Style_Anchor_Registry.json` — the registry *decides* single vs multi-file; the code only falls back to guessing when the registry is silent.
- **A new boundary behaviour:** the main item loop in `Split` handles boundaries in a block that starts like this — add a new branch here, gated behind a new flag under `Emit_Templates.json → page_split_rules`:

```js
if (primary?.directive === "PAGE_BOUNDARY") {
    const tag = primary.tag;
    if (tag === "lesson" || tag === "page") {
        if (singleFile) {
            current.items.push(it);
            ...
```

- **Title harvesting rules** live in the post-pass loop near the end of `Split`, gated by `Emit_Templates.json → body_region.lesson_title_dedup`.
- **The MTK drop-down-menu template (round 212):** on a bilingual module whose stream carried a standalone `[Content for DROP DOWN MENU]` opener, a `[MODULE CONTENT: PAGE n]` boundary does *not* start a new page — that content **is** the overview's body (the marker's own table is flagged `_reoModuleContent` so the bilingual unfold accepts it without an English|Māori header row). Pattern + gating: `Emit_Templates.json → elements.dual_language.dropdown_menu`; env `REODROPMENU_OFF`.

**Gotcha.** A page title is only harvested from a heading that appears *before* the first `[Activity]` — a heading after that is section content, and using it produced wrong titles (a module once titled a page "Fog" from a widget's panel label).

---

## B13. InteractiveScanner.js — finding the widgets

**What it does.** Before the page body is converted, this file walks the item stream and finds every **interactive widget block**: the opener tags, the widget tag itself, and every following item that belongs to it (its "members"), up to whatever terminates it. Each becomes a "bundle" with its item range marked as consumed, so the content converter steps around it. The scanner **never builds anything** — bundles feed the placeholder box, the widget builder, and the hand-off `.txt`. All boundary knowledge comes from `Interactive_Boundary_ChildTag_Bank.json` (A6); the code holds no tag lists of its own.

**Main methods, top to bottom:**

- **`ScanPage(page, normaliser, run)`** — the only public method, right at the top. Walks the items, opens a bundle at each interactive tag, and afterwards assigns activity numbers.
- A run of small detectors (first third): bilingual content-table guards, phase-delimiter recognisers for the Fundamentals families, activity-number helpers.
- **`#swallowMembers(...)`** — the core capture loop, roughly 40% of the way down. Swallows each following item until the first terminator, applying all the measured section-break rules (a heading after content ends the widget; a `[body]` after a card face means the writer resumed normal prose; and so on).
- `#trimTrailingMedia` and `#absorbLeadingPattern` (around three-quarters down) — post-adjustments: push a trailing standalone video back out of the bundle; and, when a widget is a repeating (label, widget) series, walk *up* to recover the first label that sat above the widget tag.
- **`#widgetTypeFor`** (about 80% down) — resolves a tag to its widget type and folds variants onto their parent (`rotateBanner` → `carousel`).
- The hover-definition weaving machinery and `#interactiveInTable` (near the end) — inline hover definitions woven into their sentence, and widgets invoked from inside a table cell.

**How to update.** Nearly always via the data file (A6): a widget swallowing too much or too little is a boundary-bank edit. The scanner also automatically treats every callout type in `Emit_Templates.json → callouts.by_tag` as a widget terminator — that wiring is near the top of `ScanPage`:

```js
if (bank._meta.member_rule.callout_tags_terminate !== false
    && !(... process.env.CALLOUTTERM_OFF)) {
    const _byTag = DataService.Data.EmitTemplates?.callouts?.by_tag || {};
    for (const _t of Object.keys(_byTag)) absolute.add(_t);
}
```

So a new callout type added in Part A automatically ends widgets too — no scanner edit.

One suppression to know about (round 212): on a bilingual module, a `[Content for DROP DOWN MENU]` marker directly followed by a table parses as a "dropdown" widget invocation but is really the PNR family's module-menu section marker — `#dropdownMenuMarker` stops it opening a bundle so the menu table can be routed to the module menu instead (`elements.dual_language.dropdown_menu`; env `REODROPMENU_OFF`).

**Gotchas.** A widget's own trailing number (`[Flipcard 1]`) is a *panel index*, not an activity id — confusing the two once made a widget swallow a whole page. When `heading_is_terminator` is unknown, headings terminate — the safe failure is "the heading renders normally".

---

## B14. InteractiveBuilder.js — building the known widgets

**What it does.** Just before the converter would emit an orange placeholder for a widget bundle, it asks this file: "can you build this one for real?" The file dispatches on the widget type to a conservative per-widget builder that maps the captured data into markup templates from `Emit_Templates.json → interactive_builders`. If the data fits the shape cleanly, it returns real HTML and the widget ships live. If *anything* is unexpected — a stray table, red instruction text, a missing face — it returns `null` and the honest placeholder stays. The ruling principle, stated in the header: **never half-build a widget.**

**Layout of the file, top to bottom:**

- **`Build({bundle, run, ...})`** — the public entry at the top: a `switch` on `bundle.type`, wrapped so any error or missing template quietly resolves to `null` (placeholder).
- The builders, in order: `#glossary`, `#selfCheck`, `#dragAndDrop`, `#hintSlider` (first eighth) → `#accordion` and its three sub-forms (around an eighth in) → `#speechBubble` + conversation form (just over a quarter) → `#shapeHover`, `#flipCard` and its five capture forms (a third to 40%) → `#modal`, then the large `#tabs` family (`#tabsStrictText`, `#tabsFromList`, `#tabsRich`, `#tabsHeadingPanes`, `#tabsTablePanes` — 45% to 70%) → `#carousel` + `#rotateBanner` (around 72%) → `#clickDrop` (about 82%) → shared cell/image/flip helpers (the final sixth).
- Several of the richer forms (the rich tabs, the accordion-as-phases) are additionally gated by **registries in the data** listing which module families the human developers actually build that way — because the `[tabs]` tag alone is not a reliable signal (some families build the same content as an accordion).

**How to add a new widget builder.** Two steps (the header documents this):

1. Add the markup templates to `Emit_Templates.json → interactive_builders.<yourType>` (with an `enabled: true` flag and a `_comment` describing the accepted input shape).
2. Add a `case` to the `switch` inside `Build`, and a private builder method modelled on `#glossary` (the simplest):

```js
case "clickDrop":
    html = this.#clickDrop({ bundle, tpl, renderInline });
    break;
case "glossary":
    html = this.#glossary({ bundle, tpl, renderInline });
    break;
// add yours here, following the same pattern
```

Inside the builder: pull the captured members/table out of `bundle`, fill the template slots with `Utils.FillTemplate`, and **return `null` the instant the data doesn't fit** — that is what keeps a wrong-but-live widget from ever shipping. Note the `default: return null;` at the bottom of the switch: a type with a template but no case simply stays a placeholder, which is always safe.

---

## B15. ManifestBuilder.js — the developer hand-off file

**What it does.** Writes `{CODE}_interactives.txt` — the developer's to-do list. For every still-un-built widget: which file it is in, the placeholder marker to search for (`data-cv2-index="N"`), its activity, its type, and the writer's raw source content reproduced verbatim (tags, red words and all) so nothing the writer configured is lost. Deliberately includes answer keys — this file never ships inside a page. By default, already-built widgets are omitted (they are live in the HTML, so they are not work).

**Main methods:** `Build(run)` (top — assembles the whole file) → `#identifyPattern` (scores the bundle against `Manifest_Patterns.json`) → `#clean` and `#rawContent` (the two content renderers) near the end.

**How to update.** To add or reorder the fields shown per widget, edit the `out.push(...)` sequence in the middle of `Build`:

```js
out.push(`File: ${b.targetFile}`);
out.push(`Placeholder marker: data-cv2-index="${b.index}" (the placeholder div to replace)`);
out.push(`Activity: ${b.activityId ?? "(none — inline component)"}`);
out.push(`Type: ${[b.type, ...(b.extraTypes ?? [])].join(" + ")}`);
```

The three display modes (un-built-only, raw-verbatim content, faithful content) are data flags under `Emit_Templates.json → interactive_placeholder`, each with an off-switch (`MANIFESTALL_OFF`, `MANIFESTRAW_OFF`, `MANIFESTFAITHFUL_OFF`). New data-pattern names are a pure data edit in `Manifest_Patterns.json` (A8).

---

## B16. ContentConverter.js — the heart ★★

**What it does.** The largest file (~4,900 lines) and the centre of the pipeline. For one page it takes the item stream (with widget bundles already marked) and emits the finished **body HTML**: every tag becomes its element, writer instructions become red notes, each un-built widget becomes one placeholder box, and the menu content is separated out for the page header. It returns `{ bodyHtml, menu, titleBar }` per page. Since the "engine split" refactor, eight collaborator classes (B17–B24) do the specialised rendering; this file is the conductor that decides *what* to render *when*.

**A map of the file, top to bottom** (percentages are approximate — search for the method names):

| Where | What | Job |
|---|---|---|
| Top | `ConvertPage(page, bundles, run, normaliser)` | The entry point: partitions the items, merges consecutive plain-text items, then runs the main loop |
| ~20% | The **main dispatch loop** (`for (let i = 0; i < bodyItems.length; i++)`) | Walks every item: black text → paragraphs/lists; a tag → the element dispatcher; a container tag → the callout/activity opener; a consumed range → the widget placeholder |
| ~46% | The **post-pass chain** (a nested call ending in `PanelsBuilder.fundamentalsPanels(...)`) | After the loop: re-level headings → promote named headings (WALT/WILF) → activity interactive class fix-up → alert title headings → residue clean-ups → wrap Fundamentals/Inquiry panels |
| ~50% | `#relevelHeadings(html)` | Re-ranks the page's heading levels into the h3–h5 band, page-wide |
| ~53–57% | `#normaliseTitleCase` + the `#bilingual…Split` family | The title-bar splitters: how a `[TITLE BAR]` payload divides into the English and Te Reo `<h1>`s (dash, slash, colon, pipe, case-change, and boilerplate-marker rules) |
| ~57% | **`#partitionItems(page, menuType, run)`** | The big three-way split of a page's items into title bar / menu content / body content — where menus are captured |
| ~73% | **`#element(it, ...)`** | The tag-to-HTML dispatcher: headings, captions, buttons, media (via MediaBuilder), tables (via TablesAndGrids), embeds… |
| ~82% | The style-strip helpers | The measured bold/italic strips for alert boxes, activities, headings |
| ~84% | **`#calloutOpen(...)`** and `#sideAlertCol` | The callout-box opener: looks up the tag in `callouts.by_tag`, wraps the content, absorbs same-sentence buttons/links, pairs side-alerts alongside their content |
| ~91% | `#inline` and `#interactivePlaceholder` | Inline tags woven into sentences; the orange un-built-widget box |
| End | The residue cleaners | Drop leftover bullets/closers that would otherwise leak |

**Where your change probably goes — quick router:**

- Output *shape* wrong (markup, classes) → not here; `Emit_Templates.json`.
- A **heading** renders at the wrong level → the heading branch inside `#element` (which reads `elements.heading.logical_to_element` from data) or the page-wide `#relevelHeadings`. The branch starts:

```js
if (["h1", "h2", "h3", "h4", "h5", "heading", "activity heading"].includes(tag)) {
    const digit = /^h\d$/.test(tag) ? parseInt(tag[1], 10) : 2;
    ...
    const l2e = tpl.elements.heading.logical_to_element;
    const shifted = Math.min(Math.max(digit + l2e.body_shift, 2), ...);
```

- A **callout box** behaves wrongly (not just looks wrongly) → `#calloutOpen`. Note its friendly failure: an unknown container tag emits a red note telling you to add the tag to `Emit_Templates callouts` — which is usually the entire fix:

```js
let def = tpl.callouts.by_tag[tag];
if (!def) {
    return [NotesAndComments.redFlag(
        `Unknown container [${tag}] — content kept below without a wrapper; add it to Emit_Templates callouts.`, run)];
}
```

- The **title bar** splits languages wrongly → the `#bilingual…Split` family; the separator characters are data (`Emit_Templates.json → header.title_split`).
- The **menu** captures the wrong items → `#partitionItems`; how the captured menu *renders* → `MenuBuilder` (B20).

**Gotchas.** This file holds a handful of per-page state fields (the page's English title, the current lesson number, the per-lesson activity-letter counter) — they are private statics reset per page; treat them carefully. And the file's header repeats the ban: never `if (moduleCode === …)`.

---

## B17. ListsAndRuns.js — paragraphs, lists, inline markup

**What it does.** The plain-text rendering primitives: ordinary writer prose → `<p>` paragraphs and *nested* `<ul>`/`<ol>` lists (the nesting depth comes from Word's own bullet levels, encoded as two spaces of indent per level), plus `inlineMarkup` which handles bold, italic, bare-URL links, the hyperlink weave (a phrase becomes a link when the docx carried a hyperlink), and hover-definition stitching.

**Main methods:** `coalesceBlackRuns(items)` (top — merges consecutive plain-text items in place, carrying hyperlinks along) → `hoverStitch` (middle) → **`renderBlackText(text, run, links, stitch)`** (the workhorse, lower middle) → `inlineMarkup(line, links, stitch)` (bottom). Last in the file sits `LinkTextDisplay(html)` (round 213) — a full-page post-pass that shows a domain-listed link's canonical display text ("https://speldsa.org.au") while the href keeps the full deep URL; PageAssembler calls it on the pre-acknowledgements part of each page, and it skips `cv2-interactive` placeholder subtrees (developer hand-off content stays raw). Domains live in `Emit_Templates.json → elements.link_text_display.domains` — add a domain by adding one key; env `LINKTEXT_OFF`.

**How to update.** List behaviour (indent size, dropping empty bullets, bold-led manual bullets) is data under `Emit_Templates.json → body_region.list_nesting`; the `<li>` markup itself is `elements.list`. The read happens at the top of `renderBlackText`:

```js
const L = tpl.elements.list;
const cfg = tpl.body_region?.list_nesting ?? {};
...
const indentPer = cfg.indent_spaces_per_level ?? 2;
```

**Gotcha.** The `stitch` flag is deliberately `false` for widget-placeholder content, so the raw hand-off text stays byte-faithful for the developer.

---

## B18. NotesAndComments.js — the red notes

**What it does.** The single home of both developer-facing note types: **writer instructions** rendered as bold-red paragraphs ("CS: …" for writer→team notes, "RED FLAG: …" for converter diagnostics), and surfaced **Word comments** from whitelisted authors. Also the page-level tidy pass that relocates notes out of menus, merges consecutive notes, and strips leftover template prompts.

**Main methods:** **`redFlag(text, run, kind)`** (top — THE one instruction emitter; every note in the whole engine comes through here) → the cue-folding helpers (`stripCsCue`, `stripAddresseeCue`) → the Word-comment quartet (middle) → `OmitPlaceholderResidue` and `TidyDeveloperNotes` (bottom — the whole-page post-passes).

**How to update.** Note wording/prefix rules → `redFlag` and the `red_flag` section of `Emit_Templates.json`. Trusted comment authors → `Comment_Authors.json` (A13), no code.

**Critical rule.** Every note carries the class `cv2-note` (or `cv2-comment`). The comparison tooling ignores those classes on both sides — human developers strip all such notes from finished pages, so notes must stay invisible to the structural tests. **Any new kind of note must get one of these classes too**, or the test gates will wrongly report structural differences.

---

## B19. TablesAndGrids.js — tables and layout grids

**What it does.** Renders writer tables. A genuine data table becomes a kept `<table>`; a table that is really a *layout* (side-by-side image and text, every cell led by a structural tag) becomes the human convention instead: a Bootstrap row/column grid. Also renders tags and images that appear inside table cells.

**Main methods:** **`contentTable(block, run, insidePlaceholder, norm)`** (top — the emitter; it first offers the table to the grid detector, then falls back to a normal `<table>`) → `renderCellInline` → `layoutTableGrid` (middle — the grid conversion, deliberately limited to single-row tables so a real data table is never destroyed) → `cellParts` / `renderCellParts` / `cellImage` (bottom).

**How to update.** Table markup → `Emit_Templates.json → elements.table`; the grid rule's gate → `body_region.layout_table_grid`. The decision point at the top of `contentTable`:

```js
static contentTable(block, run, insidePlaceholder = false, norm) {
    const t = DataService.Data.EmitTemplates.elements.table;
    ...
    const grid = this.layoutTableGrid(rows, run, insidePlaceholder, norm);
    if (grid) return grid;
    const html = [t.open];
```

**Gotcha.** The tag normaliser is not stored here — it arrives as the trailing `norm` argument on every method that needs it. Keep that pattern when adding methods.

---

## B20. MenuBuilder.js — the module menu

**What it does.** Builds the module menu — the tabbed or simplified navigation block in the page header holding Learning Intentions, Success Criteria, the Understand/Know/Do curriculum block, lesson links, and (per family) extra tabs like Standards or Connections. Menu shapes are the most varied part of the human library, so nearly everything here is gated by measured, per-family registries in the data.

**Main methods, top to bottom:** `menuTypeFor(page, run)` (top — tabs / simplified / none, from `Menu_Scaffold_Registry.json`) → **`buildMenu(menuItems, menuType, run, page, norm)`** (from ~12% down, the bulk of the file — the emitter, with all the family transformations: two-column layouts, bilingual heading reduction, extra tabs, the "Learning" tab, curriculum splitting) → the private helpers (~60% down) → `isReoModule`, `stripTextItalic`, `stripTextBold`, `curriculumLevel`, `dropEmptyHeadings` (the last tenth — small public utilities other files reuse).

**How to update.** Most menu fixes are data edits: the menu *type* → `Menu_Scaffold_Registry.json` (A9); the *layout registries* (two-column forms, extra tabs, heading reduction) → the `menu` section of `Emit_Templates.json` (A5, point 4). A genuinely new menu archetype needs a branch where the archetype is chosen, early in `buildMenu`:

```js
const pageType = page.isOverview ? "overview" : "lesson";
const convention = run.conventions?.menu?.[pageType] ?? null;
const archetype = menuType === "tabs" ? "tabs"
    : (convention?.archetype === "two_col_li" ? "two_col_li" : "flat");
```

…plus a matching shell in `Emit_Templates.json → menu.shells`.

One self-contained archetype to know about (round 212): `#reoDropdownTabs` composes the PNR bilingual family's whole menu from the `[Content for DROP DOWN MENU]` table that `ContentConverter.#partitionItems` flagged `_reoDropdown` — one pane per `[TABn]` row, `<span reo>/<span eng>` nav labels, `<h4><span>`/`<h5>` heading levels, a Connections-family split into two columns — rendered through the `menu.shells.reo_tabs` shell. All its shapes live in `elements.dual_language.dropdown_menu`; env `REODROPMENU_OFF`.

**Gotchas.** Bilingual (reo) modules keep their italic and their two-language headings — every strip/reduce rule must skip them via `isReoModule`. And two related behaviours deliberately live in `ContentConverter`, not here: deciding *which items* count as menu content (`#partitionItems`), and the named-heading promotion.

---

## B21. PanelsBuilder.js — Fundamentals and Inquiry panels

**What it does.** Builds the multi-panel page scaffolding for two template families: **Fundamentals** modules (a phases navigation bar, picture tiles, and one panel per phase) and **Inquiry** modules (breadcrumb tabs with one panel per step). It works on the already-built body HTML: `ContentConverter` inserts invisible sentinel markers at each panel boundary during conversion, and this file cuts the body at those markers and wraps the pieces.

**Main methods:** `fundamentalsPanels(body, {...})` (top) → the phase-dialect helpers and `newTabNav` / `phaseNavTiles` (middle) → `inquiryPanels` and `detectInquiryCed` (bottom).

**How to update.** Panel/nav/tile markup is data under `Emit_Templates.json → body_region.fundamentals_panels` and `body_region.inquiry_tabs`. The sentinel wiring at the top of `fundamentalsPanels` shows the design:

```js
const cfg = DataService.Data.EmitTemplates.body_region.fundamentals_panels;
const sent  = sentinel       || (cfg && cfg.sentinel)        || "<!--CV2_FUNDPANEL-->";
const lsent = lessonSentinel || (cfg && cfg.lesson_sentinel) || "<!--CV2_FUNDPHASE-->";
...
if (!on || !cfg || cfg.enabled === false) return strip(body);
```

**Gotcha.** Sentinels are *always* consumed, even when panels are off — they can never leak into final HTML. The decisions about *when* to insert a sentinel (the five measured "phase delimiter" dialects different writer families use) live in `ContentConverter` and `InteractiveScanner`, not here.

---

## B22. BilingualBuilder.js — Māori/English bodies

**What it does.** Renders a bilingual ("reoTranslate") module body. Writers author these as two-column tables (Māori | English); the finished page interleaves them element by element — Māori first, English second, each carrying a language attribute so the site's language toggle works — with media emitted only once (it isn't language-specific). Also handles bilingual section boxes, callouts, activities, and the phonics audio-image grid.

**Main methods:** the core unfold (`bilingualTable`, `bilingualRows`, `bilingualSplit`, `langAttr`) in the first half; section grouping and lesson boxes in the middle; callout/activity/audio-image handling in the second half. `bilingualTable` normally requires an English|Māori header row; the one exception (round 212) is the table a `[MODULE CONTENT: PAGE n]` marker introduced — `PageSplitter` flags it `_reoModuleContent` and the caller passes `forceNoHeader=true` (PNR102/104 open theirs with "Module Introduction | Kōwae Ako Whakataki" instead of the header).

**How to update.** The wrappers and behaviour flags are data under `Emit_Templates.json → elements.dual_language`. The entry check at the top of `bilingualTable` shows the shape:

```js
const cfg = DataService.Data.EmitTemplates.elements?.dual_language;
if (!cfg || cfg.enabled === false) return null;
...
if (!this.bilingualHeader(block)) return null;   // requires an English|Māori header row
```

**Gotcha.** This file never decides whether a module *is* bilingual — that decision (genuine bilingual = the reoTranslate body class or a TRR/PNR module-code prefix) happens upstream, and getting it wrong historically routed hundreds of ordinary modules through this path.

---

## B23. ActivitiesBuilder.js — the activity boxes

**What it does.** Builds the activity box — the one container that legitimately spans many tags: `[Activity 1A]` opens a box that content keeps flowing into until `[end activity]` or a structural boundary closes it. Handles the modifier classes, the `.interactive` class (added when the box owns an interactive task), activity numbering (a bare `[Activity 3]` becomes "3A/3B/…" within its lesson), and the supervisor-note reveal-panel variant.

**Main methods:** `activityInteractivePostpass(html)` (top — a whole-page fix-up adding `.interactive` where it was missed) → `containerModifiers` (middle — sorts a tag's extra words into known modifier classes vs visible notes; deliberately public so the callout path reuses it) → **`activityOpen(...)`** (bottom — the opener).

**How to update.** All the knobs are data under `Emit_Templates.json → activity_wrapper`: `modifier_classes` (which words map to which CSS classes), `interactive_widget_types` (which widget types force `.interactive`), `lesson_letter_number` (the numbering rule), `super_content` (the supervisor-note box), and — since round 217 — `standalone_widget_box` (below). The decision code in `activityOpen` reads them generically:

```js
if (forceInteractive && !/(^| )interactive( |$)/.test(modifiers)) {
    modifiers += tpl.activity_wrapper.modifier_classes.interactive;
}
...
const llRule = tpl.activity_wrapper.lesson_letter_number;
```

**The invented box (round 217 — `standalone_widget_box`).** The human developer wraps a *stand-alone* task interactive (a drag-and-drop, quiz or self-check the writer never put inside an `[Activity]`) in its own `<div class="activity interactive" number="1B">`, numbered in sequence with the tagged activities — the gold library has ~1,200 more activity boxes than the writers ever tagged. The converter now does the same. Everything about it is data:

```json
"standalone_widget_box": {
  "enabled": true,
  "types": ["dragAndDrop", "unclassified", "multiChoiceQuiz", "radioQuiz", "selfCheck", "interactive"],
  "force_interactive": true
}
```

- **A widget type is being boxed that shouldn't be** (or vice versa): edit the `types` list — but *measure first* with `outputs/_measure_standalone_boxing.py`, which reports, for every standalone widget in the converter's output, whether the human's page puts that same content inside a box. The listed types measured ≥ 0.83; the deliberately-excluded ones (accordion, carousel, tabs, flip cards, modals…) measured ≤ 0.16.
- The box takes the **next positional letter** via `activityOpen`'s `positionalId` argument (it advances the same per-lesson counter as tagged activities, so the letters interleave correctly).
- The rule only fires on pages with a lesson number. Single-file fundamentals pages number their boxes **by phase** (1A/1B in phase 1, 2A/2B in phase 2) — that derivation doesn't exist yet, so the rule stands down there rather than ship un-numbered boxes.
- Env `ACTWRAP_OFF` turns the whole thing off.

**Gotcha.** Only a bare-digit id gets re-lettered; an id the writer already lettered (`1B`) is kept as-is. That keep rule now has a known cost: the human sometimes *re-letters* the writer's own ids to make room for its invented boxes (AGH1001's writer-typed 1A ships as gold's 1C), so a kept letter can sit one or two positions off gold — a recorded follow-up question. The lesson-number state lives in `ContentConverter` and is passed in as arguments — this file stores nothing.

---

## B24. MediaBuilder.js — images, video, audio

**What it does.** The media emitters. An `[image]`/`[video]`/`[audio]` tag's pasted URL is a *reference* to an asset, never visible text. Images become either **Mode P** (a visible placeholder box plus an HTML comment holding the real reference, for the developer to swap in) or **Mode D** (a direct `<img>`), per the user's choice at convert time. YouTube URLs become the site-standard embed; other video URLs a generic iframe; audio the standard player. Leftover reference-URLs and now-empty brackets are stripped from captions.

**Main methods:** `image(...)` (top) → **`media(...)`** (the video/audio dispatcher, upper middle) → `stripMediaResidue` → `gatherFollowing` (bottom — collects the caption text following a media tag; shared by several callers in ContentConverter, so change it with care).

**How to update.** Embed markup → `Emit_Templates.json` → `video.youtube` / `video.generic_iframe` / `audio.form` / `image.mode_P`. The YouTube branch inside `media` shows where an embed is chosen:

```js
const videoId = url.match(new RegExp(acks.youtube_id))?.[1] ?? null;
if (videoId) {
    let embed = Utils.FillTemplate(tpl.video.youtube, { videoId, params: "" });
    if (run.conventions?.videoHost === "youtube") {
        embed = embed.replace("youtube-nocookie.com", "youtube.com");
    }
```

A new video host would get its own branch here plus a template in the data.

**Gotcha.** The Mode-P image comment is one of only two places the whole engine deliberately emits an HTML comment. And `gatherFollowing` marks the items it collects as consumed so they don't render twice — four different call sites rely on its exact behaviour.

---

## B25. PrecedenceResolver.js — the dormant sibling-lookup

**What it does.** The engine-side implementation of the six-level "authority cascade" (see A16): when a small layout detail isn't derivable from the Writers Template, ask what the nearest previously-built related module did, widening the circle until a solidly consistent answer is found — or honestly refuse (`escalate`) rather than guess. **Currently dormant:** its one live hook (`inheritMenu`, applied to the overview menu) is gated off by the data flag `Precedence_Cascade.json → engine_inherit.enabled: false`, so today it changes nothing.

**How to update.** Cascade level definitions and thresholds are data (`Precedence_Cascade.json`) — never edited here. If it is ever changed, its Python twin in the test harness must change identically (a parity test enforces this). The gate is the first line of `inheritMenu`:

```js
static inheritMenu(menu, code, opts) {
    if (!menu || !this.inheritEnabled(opts)) return menu;   // INERT default → output unchanged
```

---

## B26. TemplateModeResolver / SkeletonBuilder — the page shell

*(TemplateModeResolver was covered at B11; SkeletonBuilder here.)*

**SkeletonBuilder.js — what it does.** Wraps the finished body in the standard page frame: the doctype and `<html>` attributes, the `<head>` (page title + the iDoc script), the `#header` (module-code chip, the title `<h1>`s, the menu button and menu content), the `#body` wrapper, and the `#footer` (prev/next/home navigation). Every shape is a template from `Emit_Templates.json` filled with values from the module's resolved registry rules.

**Main methods:** `BuildPage({...})` (top — one full document) → `#buildHeader` (middle — the chip, titles, and menu shell; the *only* place a `<span>` is allowed inside a heading) → `#buildFooter` (bottom — the nav links; the final page gets the "final" pattern: home only, never a next link).

**How to update.** Header/footer/head markup → the `skeleton`, `header`, and `footer` sections of `Emit_Templates.json`. The title-rendering sequence inside `#buildHeader` (about halfway down the file) is where the header `<h1>` logic lives:

```js
if (content.titleBar.english) titles.push(content.titleBar.english);
if (content.titleBar.teReoLines?.length) titles.push(...content.titleBar.teReoLines);
else if (content.titleBar.teReo) titles.push(content.titleBar.teReo);
```

**Gotchas (locked rules, sourced from data):** never emit `stickyNav.js`; the iDoc host is always `tekura`; a registry value of `"—"` / `"n/a"` / `"absent"` means "this element is deliberately absent". When a lookup map is missing an entry, the builder emits a visible warning note telling you which map in `Emit_Templates.json` to extend — follow that instruction rather than editing code.

---

## B27. AcksBuilder.js — the acknowledgements

**What it does.** Builds the acknowledgements section from the media list: one credit line (or one visible ❗ ACK-TODO marker) per media item, grouped under its lesson, wrapped in the fixed standing legal items. Generated for **every** module, unconditionally — even a module with no media gets the standing items (a locked policy). YouTube titles are fetched live (the one runtime web request); iStock titles are derived from the URL slug; anything that can't be honestly derived becomes a visible TODO, never a guessed field.

**Main methods:** `Build(run)` (top — resolve every item, group by lesson, assemble) → `#buildEntry` (the per-item dispatcher, about a quarter down) → the per-source builders (`#istockEntry`, `#youtubeEntry`, `#pixabayEntry`, `#wikiEntry`, `#websiteEntry` — the middle of the file) → `#todo` (THE ACK-TODO emitter) → `#classify` and `#groupByLesson` (the final third).

**How to update.** A new media source is *usually* pure data (`Acks_Formats.json`, see A12). Only if the new source needs logic (like YouTube's live title lookup) does it also need a builder method plus a route in the dispatcher inside `#buildEntry`:

```js
switch (sourceClass) {
    case "istock":   entry = this.#istockEntry(item, prefix, adapted, run); break;
    case "youtube":  entry = await this.#youtubeEntry(item, run); break;
    case "pixabay":  entry = this.#pixabayEntry(item, prefix, run); break;
```

**Gotcha.** Never guess a licence name or a title — the honest, visible ACK-TODO is always the correct fallback.

---

## B28. HtmlFormatter.js — the indenter

**What it does.** Re-indents the finished page with tabs so the HTML is readable and matches the human-built modules. Pure text-in, text-out; it never changes content or order.

**How to update.** Only one realistic edit: if the emitters ever produce a new self-closing element, add it to the void-element set near the top:

```js
static #VOID = new Set(["img", "br", "meta", "link", "input", "hr",
    "source", "wbr", "area", "base", "col", "embed", "track"]);
```

**Gotcha.** It works line by line and assumes the emitters produce one tag per line — a template that packs several tags onto one line will mis-indent.

---

## B29. PageAssembler.js — the conductor

**What it does.** Runs the whole pipeline for one module, in order: resolve conventions → build the item stream and split into pages → per page, scan widgets then convert content → resolve the module's titles → build the acknowledgements → wrap each page in the skeleton (with prev/next links chained) → tidy notes and indentation → write the outputs and the interactives manifest. Everything reads and writes the shared `run`. The per-page output step chains three clean-up passes — OmitPlaceholderResidue, TidyDeveloperNotes, then (round 213) ListsAndRuns.LinkTextDisplay on the pre-acknowledgements part of the page (domain link texts canonicalise to the site root; the acks keep full URLs, matching the human builds). The title-resolution step also holds the round-212 rule: when NO title was derived anywhere, the front-matter metadata "Module Name" value (the PNR family's table row) pipe-splits into the two header titles in payload order — this is what recovers the PNR titles and TRR301/TRR304's missing ones (`elements.dual_language.dropdown_menu.title_from_module_name`; env `REODROPMENU_OFF`).

**How to update.** Rarely edited; two locked policies live here and must not be "fixed": output filenames follow `Emit_Templates.json → output_naming`, and the acknowledgements go on the **first page only**, after the footer (the naming/acks block sits about three-quarters down `AssembleModule`):

```js
const filenames = pageProducts.map((_, i) =>
    Utils.FillTemplate(naming.page_file, { code, NN: Utils.Pad2(i) }));
pageProducts.forEach(({ page, content }, i) => {
    const html = SkeletonBuilder.BuildPage({
        page, content, run,
        acksHtml: i === 0 ? acksHtml : "",
```

**Gotcha.** The two clean-up passes must keep their order — placeholder-residue removal runs *before* the developer-note tidy.

---

## B30. SummaryReporter.js and ConversionRun's summary

**What it does.** Renders the collapsible conversion-summary panel in the browser: the stat bar (pages / interactives / red flags / ack-todos), the module identity line, and every note any stage surfaced, worst first. Pure presentation — it decides nothing.

**How to update.** To surface a new number: add it to `ConversionRun.Summary()` (B7), then render it here — the identity line in `Render` shows the pattern:

```js
<p class="summary-identity">
    <strong>${s.moduleCode ?? "UNKNOWN MODULE"}</strong>
    — code from ${s.codeSource ?? "n/a"} · image mode ${s.imageMode}
    · media list ${s.mediaListFound ? "found" : "<strong>NOT FOUND</strong>"}
</p>
```

---

## B31. App.js — the browser UI

**What it does.** The browser entry point, loaded last. Wires the upload drop-zone, the image-mode radios, the interactive-extract checkbox, the Convert button, the progress bar, the output download links, and the reset button. One conversion per click: read the options → build a `ConversionRun` → unzip and extract the docx files → **`ModuleResolver.PrepareRun`** → `PageAssembler.AssembleModule` → render outputs and summary.

**How to update.** New UI control: add the element in `index.html`, its id in `Config.Selectors`, wire it in `#wireUi()` (upper part of the file), and read it at the start of `#convert()` (middle of the file), where the existing options are read:

```js
const imageMode = document.getElementById(Config.Selectors.ModeP).checked ? "P" : "D";
const extractEl = document.getElementById(Config.Selectors.ModeExtract);
const interactiveMode = (extractEl && extractEl.checked) ? "extract" : "inline";
const run = new ConversionRun({ imageMode, interactiveMode });
```

**Gotchas.** Never add a preparation step here directly — extend `ModuleResolver.PrepareRun` instead, so the batch tool stays identical (a test gate enforces this). The reset button rebuilds state in place rather than reloading the page, because the converter runs inside an iframe on the site and a reload would dump the user back at the landing page.

---

## B32. index.html and _modules.json — the page and the manifest

**`app/index.html`** is the converter web page: the upload zone, the options, the Convert button, the outputs list. It must be served over HTTP (e.g. `python3 -m http.server` then open `/app/`); opened as a plain file it shows an instruction screen instead, because browsers block local data loading. Its `<script>` tags load every engine file **in dependency order**, ending with `App.js`.

**`app/js/_modules.json`** is the master manifest keeping everything in sync. Three lists:

- `browser_order` — must match `index.html`'s script tags exactly.
- `node_order` — the load order for the Node batch tool (browser-only files excluded).
- `data_map` — the canonical data-file map (mirrors `Config.DataFiles`).

**The iron rule:** adding, renaming, or splitting an engine file means editing **both** `_modules.json` and `index.html` (and `Config.DataFiles` + `data_map` for a data file). An automated check in the development harness (`_check_index_sync.cjs`) fails loudly if these ever drift from the actual files on disk.

---

# Part C — Common update recipes

Step-by-step walkthroughs of the most likely maintenance jobs, in rough order of likelihood.

### Recipe 1 — A writer spelled a tag a new way

*Symptom: a red `[tag]` leaks into the page as literal text, or renders as a "CS:" note when it should be an element.*

1. Open `data/Tag_Lexicon.json`. Find the tag's entry under `tags` and add the new folded spelling to its `aliases` array (lowercase, accents stripped).
2. If the wording is instruction-like ("please add a slider here"), check `Instruction_Cues.json` isn't claiming it first — instructions win over tags by design.
3. Reload the converter page, re-convert a module that uses the new spelling, confirm it renders.
4. If the string is a genuine one-off monstrosity that alias matching cannot express, use `Tag_Exceptions.json` — but treat that as a last resort.

### Recipe 2 — An output shape needs to change (box, heading, button, footer…)

1. Convert a module and copy a distinctive class name or attribute from the wrong output.
2. Search `data/Emit_Templates.json` for it — that lands you in the owning section.
3. Edit the template string. Placeholders in `{curly}` are filled by the engine; leave them in place.
4. Reload, re-convert, inspect. (If a placeholder name is typoed, it will show up literally in the output — that's the built-in alarm.)

### Recipe 3 — Add a brand-new interactive widget

Three files, in this order:

1. **`data/Tag_Lexicon.json`** — add the tag: `"directive": "INTERACTIVE"`, its aliases, and a new name in `widget_types` (e.g. `"timelineSlider"`).
2. **`data/Interactive_Boundary_ChildTag_Bank.json`** — add a `"timelineSlider"` entry under `interactives` with `heading_is_terminator` (use `true` if unsure) and any `signature_subtags`.
3. That alone makes the widget **captured and placeholdered** correctly — it appears as an orange box and in the `.txt` hand-off. If the converter should also *build* it:
4. **`data/Emit_Templates.json`** — add `interactive_builders.timelineSlider` with the markup templates and a `_comment` describing the exact accepted input shape.
5. **`app/js/InteractiveBuilder.js`** — add a `case "timelineSlider":` to the `switch` in `Build` (near the top of the file) and a private builder modelled on `#glossary`. Return `null` whenever the captured data doesn't fit — never half-build.

### Recipe 4 — A widget swallows the section after it (or leaks its own content)

1. Open `data/Interactive_Boundary_ChildTag_Bank.json`.
2. Check the widget's `heading_is_terminator` under `interactives` — this fixes most cases.
3. Otherwise scan `_meta.member_rule` for the named rule closest to your case (they are individually documented with the module that motivated each) and tune it.
4. Only touch `InteractiveScanner.js` (`#swallowMembers`) if the situation is genuinely a new *kind* of boundary — and then add it as a new data-driven rule, not a hard-coded case.

### Recipe 5 — A new red-text phrasing should become a "CS:" note

Add the phrase to `data/Instruction_Cues.json → cue_patterns`. Prefer a multi-word phrase over a single common word so genuine tags never get demoted to notes.

### Recipe 6 — Writers' tags stopped being detected entirely in one document

Most likely a new shade of red. Add its six-digit hex value to `data/Input_Doc_Rules.json → red_runs.red_hex_values`. (To find the hex: unzip the docx and look at a `<w:color w:val="…">` on one of the affected runs in `word/document.xml`.)

### Recipe 7 — A new media source needs an acknowledgement line

Edit `data/Acks_Formats.json`: add the wording under `entry_templates` and map the domain in `source_classification.by_domain`. Only add code (in `AcksBuilder.js`) if the source needs live logic like a title lookup.

### Recipe 8 — A module family's menu / page shell is wrong

- Menu **type** (tabs vs simplified vs none) → `data/Menu_Scaffold_Registry.json`.
- Menu **layout** (two-column, extra tabs, heading language) → the per-family registries in `data/Emit_Templates.json → menu`.
- Page **shell** (body class, footer, single-vs-multi-file) → `data/Style_Anchor_Registry.json` (that family's `delta`).

### Recipe 9 — Add a whole new data file

1. Create `data/Your_New_File.json` (include a `_meta` or `_doc` block explaining it — every existing file does).
2. Add it to `app/js/Config.js → DataFiles`.
3. Add it to `app/js/_modules.json → data_map`.
4. It is now readable everywhere as `DataService.Data.YourNewKey`.

### Recipe 10 — Ship the change

1. Bump `Config.js → AppVersion` and add a matching comment line above it.
2. Add an entry to `converter-v2/BUILD_CHANGELOG.md` (newest first) describing what changed and why.
3. If a convention or recipe changed, update `converter-v2/CLAUDE.md` — and this guide.
4. Re-convert a handful of representative modules and compare against their previous output before committing. (The full test gates live in the development harness; for hand edits, at minimum eyeball a converted module of the affected family.)

---

# Part D — The safety net

### The off-switches (env toggles)

Nearly every behaviour shipped since the early rounds carries an **environment-variable off-switch** — a name ending in `_OFF` (e.g. `LISTNEST_OFF` reverts nested lists to flat ones; `CELLTAG_OFF` reverts in-cell tag rendering). Setting the variable when running the **batch tool** reverts exactly that one behaviour, which is how changes are A/B-tested against the previous output. They have no effect in the browser (there is no `process.env` there) — they are a testing facility, not a user feature. The full catalogue of toggles, with what each reverts, is in `converter-v2/CLAUDE.md` (section 11) and `BUILD_CHANGELOG.md`.

When you add a significant new behaviour, follow the house pattern: put the shape in data with an `enabled: true` flag, **and** check an off-switch in the code:

```js
const on = cfg && cfg.enabled !== false
    && !(typeof process !== "undefined" && process.env && process.env.MYRULE_OFF);
```

### The sync check

`_check_index_sync.cjs` (in the development harness's test folder) verifies that `index.html`, `_modules.json`, and the actual files in `app/js/` all agree. Run it after adding/renaming any engine file.

### The test gates

The development harness (the `CONVERTER_V2` folder that sits alongside this repo, reaching this engine through symlinks) holds the full regression suite: the tag regression (9,557 historical variations), the structural comparison against the human-built library, per-widget verifiers, and the batch converter. Any change beyond a trivial data tweak should be proven there before it ships. The workflow, the current baselines, and the discipline around them are documented in `converter-v2/CLAUDE.md`.

### Reading order for a new maintainer

1. This guide, sections 1–4.
2. The header comment of `ContentConverter.js` and `Emit_Templates.json`'s `_meta`.
3. `data/Tag_Interpretation_Rules.md` — the mental model of tags.
4. `converter-v2/CLAUDE.md` — the deeper development discipline.
5. `converter-v2/BUILD_CHANGELOG.md`, newest few entries — what changed lately and why.

---

*End of guide. If a section here disagrees with a file's own header comment, trust the header comment (it travels with the code) and please fix this guide to match.*




