# Changelog

Running development record for PageForge V1.5. **Newest first.** Every session that changes
code or docs adds an entry here (what changed, why, files touched, test `pass/total`). See
[`CLAUDE.md`](CLAUDE.md) for the standing logging instruction.

---

## 2026-06-30 — Fix Page Stitcher base/section misclassification

**What.** Page Stitcher mode now correctly tells the base homepage from its section files
even when each section carries a manual-stitch GUIDE block. Repo set up for ongoing
development (this changelog + `CLAUDE.md`).

**Why.** Uploading a valid base plus its section files (e.g. `BLL220-base.html` +
`BLL220-lesson-*.html`) failed with *"More than one base homepage uploaded — include exactly
one."* Root cause: `PageStitcherMode._classifyFiles()` decided "is this the base?" with a
bare-substring test for `PAGEFORGE-SPLICE`. Every section file's GUIDE block *quotes* that
marker in its human instructions, so all files tested positive, all were classed as bases, and
the ">1 base" guard fired. The pure `stitchCore()` already strips GUIDE blocks before locating
markers (and is tested for guide-quoted markers), but the classifier that runs first skipped
that step. The guides quote the **complete** marker, so a stricter pattern alone is not
enough — stripping guides first is the essential part.

**Fix.** `_classifyFiles` now strips GUIDE blocks (reusing the stitcher's `_stripGuides`) and
matches a **real** marker (`<!-- PAGEFORGE-SPLICE id=…`) instead of the bare word, keeping the
`<CODE>-base.html` filename fallback. Validated to yield 1 base + 6 sections on the real
BLL220 upload; the regression test below proves it headlessly.

**Files touched.**
- `js/page-stitcher.js` — `_classifyFiles`: strip guides + real-marker match.
- `tests/page-stitcher.test.js` — new regression test in *"PageStitcherMode — single
  container, auto-classify"*: section files carry a GUIDE block quoting a `PAGEFORGE-SPLICE`
  marker; asserts exactly one base detected and a clean stitch (no ">1 base" error, no marker
  leak). Fails on the old classifier, passes on the fix.
- `SPLIT_MODE_AND_STITCH_CONTRACT.md` — §5 + the §3c note now specify base detection as
  "strip GUIDE blocks first, then match a real `<!-- PAGEFORGE-SPLICE id=… -->` marker", so
  the §3c guarantee that guide text "may safely quote markers" holds at classification time.
- `README.md` — test count corrected to 151/151.
- `CLAUDE.md`, `CHANGELOG.md` — added (repo set up for ongoing development).

**Tests.** `node tests/test-runner.js` → **151/151 passing** (was 150; +1 regression test).

---

## 2026-06-30 — Baseline: PageForge V1.5

State of the repo at the start of structured development (reconstructed from `README.md`,
`SPLIT_MODE_AND_STITCH_CONTRACT.md`, the in-repo change reports, and `git log`). PageForge
V1.5 is an interim production replacement for the online PageForge — a 100% client-side static
web app (no backend, no build step, no dependencies).

**What V1.5 carries:**
- **Module Development conversion (carried over).** Drop the Writer's Template and/or Media
  List `.docx` (1–2 files, auto-classified by content) into one container and Convert; emits
  the parsed `.txt` files, with a ZIP download when more than one file is produced.
- **Native Word comment capture (new).** Actionable Word editor comments from the six
  Creative-Services reviewers are kept (an asymmetric filter drops pure copyright/permission
  boilerplate but keeps anything with an action signal) and re-emitted as red notes in the
  parsed `.txt`, placed before the element they refer to (body match, or media-row match by
  URL / iStock id / YouTube id). Whitelist + filter are data-driven in
  `data/comment-authors.json`.
- **Page Stitcher (new) with SPLIT MODE.** The downstream converter can emit a long
  single-page module as a base homepage + per-section files; the Page Stitcher recombines them
  losslessly via the explicit marker contract in `SPLIT_MODE_AND_STITCH_CONTRACT.md` (splice/
  section markers, GUIDE-block stripping, byte-faithful round-trip).
- **Removed from V1.** The deprecated Standard mode / Example Distiller HTML-conversion
  pipeline was dropped; only the carried-over modules load in the headless runner.

**Tests.** `node tests/test-runner.js` → **150/150 passing** at baseline.
