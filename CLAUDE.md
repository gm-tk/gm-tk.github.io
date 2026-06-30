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
baseline: **151/151 passing** — update this number here and in `README.md` whenever it moves.

## Conventions

- **Reuse the carried-over modules** — extend them additively; do not reinvent or break their
  contracts. The pieces: `docx-parser.js`, `comment-extractor.js`, `comment-filter.js`,
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

## Authoritative contract

[`SPLIT_MODE_AND_STITCH_CONTRACT.md`](SPLIT_MODE_AND_STITCH_CONTRACT.md) governs **SPLIT MODE**
and the **Page Stitcher** (base/section classification, marker contract, GUIDE-block
stripping, the round-trip guarantee). When changing stitch behaviour, change the contract in
the same commit and keep the two in sync.

## Working agreement

Work on a feature branch and open a PR; leave pushing/merging to the maintainer. Do not push
to `main`.
