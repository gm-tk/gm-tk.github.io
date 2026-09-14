# CLAUDE.md — operating guide for PageForge V1.5

Read this first, every session. It is the standing contract for working in this repo.

## Purpose

PageForge V1.5 is a **100% client-side** static web app (no backend, no build step, no
dependencies) that prepares inputs for Te Kura's downstream module-conversion workflow: it
parses a writer's `.docx` (Writer's Template and/or Media List) into `_parsed.txt` files —
now carrying reviewers' actionable Word comments — and provides a **Page Stitcher** that
recombines SPLIT-MODE modules. See [`README.md`](README.md) for the full feature description;
don't duplicate it here.

## Standing logging instruction (do not skip)

> **Every session that changes code or docs MUST add a dated, newest-first entry to
> [`CHANGELOG.md`](CHANGELOG.md)** — what changed, why, the files touched, and the test
> result (`pass/total`). **And update this `CLAUDE.md` whenever a convention, invariant, or
> the test baseline changes.** This is the point of the repo setup: the changelog is the
> running development record. No code/doc change ships without its changelog entry.

## Invariants (preserve all of these)

- **100% client-side** — all parsing, conversion and stitching happen in the browser;
  nothing is uploaded, stored, or transmitted. No backend.
- **No `localStorage` / `sessionStorage`** — session state lives in memory only.
- **Content fidelity** — writer-supplied content passes through unchanged; anything PageForge
  adds (comment notes, splice metadata) is **additive metadata**, never an edit to the source.
- **Headless-testable logic** — new logic must run under the plain-Node test runner: DOM
  access sits behind an injected `document` that no-ops when an element is absent;
  dependencies are constructor-injected; filenames are kebab-case.
- **Wire every new JS module in two places** — a `<script>` tag in `index.html` **and** a
  `loadScript()` line in `tests/test-runner.js` (in dependency order).

## Test gate

```bash
node tests/test-runner.js
```

Plain Node, no install. **Keep it green** and run it after every change. Add a small,
focused test per feature/fix (and make sure it would fail without your change). Current
baseline: **243/243 passing** — update this number here and in `README.md` whenever it moves.

## Conventions

- **Reuse the carried-over modules** — extend them additively; do not reinvent or break their
  contracts. The pieces: `docx-parser.js`, `omml-to-latex.js`, `omml-to-mathml.js`,
  `comment-extractor.js`, `comment-filter.js`,
  `comment-inserter.js`, `comment-config.js`, `formatter.js`, `page-stitcher.js`,
  `media-list-converter.js`, `module-results-page.js`, `mode-toggle.js`,
  `mode-toggle-filename.js`, `output-manager.js`, `toast.js`.
- **Headless-testable modules** — pure core (string/regex, no DOM) + a thin DOM/upload
  adapter that no-ops without a `document`. Mirror the existing `PageStitcher` /
  `PageStitcherMode` and `ModeToggle` split.
- **Constructor-injected dependencies** — pass `document`, `outputManager`, `stitcher`,
  `notify`, etc. into the constructor so the Node runner can exercise them.
- **kebab-case filenames** for JS modules.
- **Wire new modules** in `index.html` + `tests/test-runner.js` (see invariants).

## Equations (OMML -> LaTeX)

A Word equation is **not** a `<w:r>` run: it lives in `<m:oMath>` (inline) or
`<m:oMathPara>` (own line) **beside** the runs inside a `<w:p>`. `js/omml-to-latex.js`
converts it and `DocxParser` emits it as a run flagged `isMath`, which the formatter
prints **verbatim** — never trimmed, never wrapped in `**`/`*`/`__`, never given the
highlight tick or a `[LINK: …]` suffix, all of which corrupt the markup.

**LaTeX is the carrier, and it is regenerated, not retained.** Creative Services tells
writers to produce equations as LaTeX and then press **Alt + =** — which makes Word swallow
the LaTeX and store OMML, so no LaTeX survives in the `.docx` to keep. Regenerating it
gives the parsed `.txt` one carrier whichever route the writer took (Alt + = or LaTeX left
as plain text), so the Convertor has a single job. Delimiters are the ones its `COMP_12`
"MathJax / Equations" rule already specifies: `\(…\)` inline, `\[…\]` display. Word
records which the writer chose — never guess it.

**Rules that are easy to get wrong, and were:**

- **A 2-letter run is variables, not a word.** `E=mc` is m times c; `P=VI` is volts times
  amps. One letter is always a variable, 3+ is prose, and exactly two is a variable pair
  *unless* a word of 3+ letters sits one space away ("amount **of** heat energy").
- **Word's equations contain typographic spaces** — U+2008 PUNCTUATION SPACE and U+2009
  THIN SPACE as well as U+00A0. Treat `/\s/` (plus U+200B) as whitespace; anything
  narrower leaves stray characters inside the markup, and it only shows up on real writer
  content.
- **A writer's own typo passes through.** `29ºC` uses U+00BA, not the degree sign. Do not
  "correct" it — content fidelity, and a silent fix means nobody ever fixes the source.

An OMML element the converter does not recognise is recursed into and counted in
`ommlConverter.stats.unknownElements` — **never dropped**; a silent drop is the bug this
module exists to prevent. Counter: `parser.stats.mathEquations`.

**What MTK actually renders (settled 2026-08-26, six live runs + a local reproduction —
`PageForge_Test_Material/MTK_Equation_Rendering_Test__RESULTS.md`).** MathML renders; **LaTeX
does not**. Two MathJax builds collide on every module page: Brightspace loads
`s.brightspace.com/lib/mathjax/3.2.2/mml-chtml.js` (MathML input only, no TeX) and the Te Kura
template then loads a TeX-capable `tex-mml-chtml.js` from jsDelivr, which arrives second and is
discarded — MathJax 3 will not initialise twice. Nothing is blocked by CSP; the browser also
draws MathML natively. So the parsed `.txt` staying LaTeX is **deliberate and not the end of the
story**: the downstream Convertor project turns it into `<math>` before the HTML ships. Do not
"fix" this by having a module page load its own MathJax — that only works if it wins a timing
race against the platform (415 ms won; 885 ms and 1054 ms lost).

`js/omml-to-mathml.js` is the same converter targeting MathML. It is **not in the parse
path** — it is kept, wired and tested as the deterministic alternative if the downstream
LaTeX-to-markup step ever needs replacing with code. Any fix to one belongs in both.

## Authoritative contract

[`SPLIT_MODE_AND_STITCH_CONTRACT.md`](SPLIT_MODE_AND_STITCH_CONTRACT.md) governs **SPLIT MODE**
and the **Page Stitcher** (base/section classification, marker contract, GUIDE-block
stripping, the round-trip guarantee). When changing stitch behaviour, change the contract in
the same commit and keep the two in sync.

## Working agreement

Work on a feature branch and open a PR; leave pushing/merging to the maintainer. Do not push
to `main`.
