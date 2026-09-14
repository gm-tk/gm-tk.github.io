# Changelog

Running development record for PageForge V1.5. **Newest first.** Every session that changes
code or docs adds an entry here (what changed, why, files touched, test `pass/total`). See
[`CLAUDE.md`](CLAUDE.md) for the standing logging instruction.

---

## 2026-08-26 (later still) — measured: MTK renders MathML, not LaTeX (docs only)

**What.** No code change. `PageForge_Test_Material/MTK_Equation_Rendering_Test.html` was run six
times in the live MTK environment and the result is recorded in `CLAUDE.md` and in
`PageForge_Test_Material/MTK_Equation_Rendering_Test__RESULTS.md`.

**The finding.** MathML renders in MTK; LaTeX does not — and not because anything is blocked.
Two MathJax builds collide. Brightspace loads
`https://s.brightspace.com/lib/mathjax/3.2.2/mml-chtml.js`, the **MathML-input-only** component
build with no TeX input jax. The Te Kura template's `packages/mathJax/script.js` then loads
`https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js`, which *is* TeX-capable — but it
arrives second, and MathJax 3 will not initialise twice. First one wins, so `\(…\)` is never
typeset and the Te Kura package's ~1 MB download does nothing.

**Reproduced** in headless Chromium with the two real component builds, which matches every run:
`mml-chtml` then `tex-mml-chtml` → LaTeX NOT typeset, `startup.input` has no TeX; the reverse
order → typeset. That also explains why the test page's own jsDelivr load *did* typeset (415 ms,
before Brightspace's) while cdnjs (885 ms) and unpkg (1054 ms) did not. A timing race is not a
basis for production, so a module page must never load its own MathJax.

**Also established.** Native MathML support is present, so MathML renders even with no MathJax at
all. **Zero CSP violations across all six runs** — jsDelivr, cdnjs and unpkg all load fine;
nothing in MTK is blocking CDNs. The corpus's existing 2,018 `<math>` elements are vindicated.

**What it does NOT change.** The parser still emits LaTeX only. Chris's call: the downstream
Convertor project converts it to `<math>` before the HTML ships, keeping one carrier in the
parsed `.txt` and one job for the knowledge base.

**Follow-up owed elsewhere (not this repo).** The `/kb` `COMP_12` rule — *"MathJax / Equations —
Standard LaTeX syntax. Inline: `\( \)`. Block: `\[ \]`"* — is **wrong as written for MTK
today**: LaTeX left in a finished page will not render. It needs rewriting in a `/kb` round to
say the output must be MathML.

**Files.** `CLAUDE.md`, `PageForge_Test_Material/MTK_Equation_Rendering_Test__RESULTS.md` (new,
outside this repo).

**Tests.** 243/243 passing, unchanged — no code was touched.

---

## 2026-08-26 (later) — the equation carrier is LaTeX, not MathML

**What.** The parsed `.txt` now carries each Word equation as LaTeX — `\(…\)` where the
writer put it inline, `\[…\]` where they put it on its own line — instead of the MathML
shipped in the entry below. Same recovery of the same 315 lost equations; different
carrier.

**Why.** Creative Services' instruction to writers (Persephone Samuels, 26 Aug 2026, "FW:
Math Pātai") is: screenshot the equation, ask an AI to *"convert the equation in this
image to latex for word"*, paste the LaTeX into Word, then press **Alt + =**. Maths content
is not to use images at all, so this is the standard route. Two things follow.

1. **The LaTeX cannot be "retained".** Alt + = makes Word *swallow* it: the file stores
   OMML and keeps no copy of what was typed. Checked directly against MathMLTest.docx —
   there is not one backslash-command anywhere in `word/document.xml`. So the LaTeX in the
   parsed `.txt` has to be regenerated from the equation object, whichever carrier we pick.
2. **Given that, one carrier beats two.** A writer who skips Alt + = leaves raw LaTeX
   sitting in the paragraph as plain text, which already passes through the parser
   untouched. Emitting MathML for the converted equations and LaTeX for the unconverted
   ones would hand the downstream Convertor two shapes to recognise. Emitting LaTeX for
   both gives it one job — LaTeX to the page's maths markup — which is what its existing
   `COMP_12` **"MathJax / Equations — Standard LaTeX syntax. Inline: `\( \)`. Block:
   `\[ \]`"** rule already describes. Chris's call; the delimiters are that rule's.

**How.** New `js/omml-to-latex.js` (`OmmlToLatex`), the same shape as `OmmlToMathml` and
covering the same grammar. `DocxParser.ommlConverter` is now an `OmmlToLatex`; nothing else
in the parser changed, and the formatter's verbatim `isMath` rule is unchanged — it already
protects backslashes and braces exactly as it protected angle brackets.

Word tells us inline from display, so we do not guess: `<m:oMath>` is `\(…\)`,
`<m:oMathPara>` is `\[…\]`.

**Token rules.** A symbol command always carries a guard space *only where a letter
follows*, because a LaTeX command name is letters only — `\Delta E` keeps its space,
`\times4200` tightens up, which is the shape the writers' own AI produces
(`\frac{8\times15}{2\times3}`). Greek letters become their commands. Function names
become `\sin` and friends.

**Two real bugs the tests and the corpus flushed out — both were in the MathML converter
too, and both are fixed in both.**

1. **"mc" is not a word.** Any letter run of 2+ characters was being treated as prose, so
   `E=mc` came out as `\text{mc}` and `P=VI` as `\text{VI}`. Word gives no signal —
   "specific heat capacity" and "mc" are both just letters in a run — so the rule is now:
   one letter is always a variable; three or more is prose; **exactly two** is a variable
   pair *unless* it sits one space from a word of 3+ letters, which makes it part of a
   phrase ("amount **of** heat energy"). Checked against every equation in
   PES1007/PES1008/MXFU401: every phrase lands in prose, every variable product in maths.
2. **Word's equations are full of typographic spaces.** `_isSpace` knew about space, tab,
   newline and NO-BREAK SPACE — but the equation editor also writes **U+2008 PUNCTUATION
   SPACE** and **U+2009 THIN SPACE**. Those were falling through as letters, leaving stray
   characters inside the markup (`\frac{1}{2 }m {v}^{2}`). Now `/\s/` plus U+200B, which
   covers the lot. This one only showed up on real writer content, not on fixtures.

**Verified.** Real parser and formatter over MathMLTest.docx with a real XML DOM: 32 of 32
equations, **15 inline + 17 display**, zero unrecognised OMML. An A/B with the converter
disabled, with the equations stripped back out of the ON side, is **byte-identical** to the
OFF side — the only difference is the one bullet whose entire content was an equation and
which therefore used to be dropped as an empty paragraph. A character sweep of all 32
equations leaves exactly one non-ASCII character: `º` (U+00BA MASCULINE ORDINAL) in
`29ºC`, which is the **writer's** typo for `°` and passes through uncorrected, per the
content-fidelity invariant. Against the real PES1008 Writers Template: 24 of 24, zero
unknown elements.

**`OmmlToMathml` stays.** It is no longer in the parse path, but it remains wired, tested
and carrying both fixes above — it is the deterministic alternative for the day the
downstream LaTeX-to-markup step wants replacing with code. `tests/omml-mathml.test.js`
says so at the top.

**Files.** `js/omml-to-latex.js` (new), `js/omml-to-mathml.js`, `js/docx-parser.js`,
`index.html`, `tests/test-runner.js`, `tests/omml-latex.test.js` (new),
`tests/omml-fixtures.js` (new), `tests/omml-mathml.test.js`, `CLAUDE.md`, `README.md`.

**Test fixtures.** The tiny XML reader that lets the equation tests be written as the OMML
Word actually emits now lives in `tests/omml-fixtures.js`, loaded by the runner before the
test files (it is not a `*.test.js`, so auto-discovery skips it) and shared by both suites.

**Tests.** 243/243 passing (was 204/204).

---

## 2026-08-26 — Word equations reach the parsed output as MathML

**What.** A writer's equations — anything typed with Word's equation editor — now come
through the Module Development parse as MathML instead of vanishing.

**Why.** Word does not store an equation in a `<w:r>` run. It stores it in `<m:oMath>`
(inline) or `<m:oMathPara>` (its own line), which sit BESIDE the runs inside the
paragraph. `DocxParser._extractParagraphContent` had branches for `w:r`, `w:hyperlink`,
`w:ins`, `w:del`, `w:sdt`, `w:bookmarkStart/End` and `w:pPr` — and nothing else, so every
equation fell through the gap. The failure was silent: no marker, no warning, no
placeholder, just a sentence ending in "…using the following formula:" followed by
nothing. Measured over the 26 Writers Templates whose finished HTML carries real MathML,
8 ship OMML — MXDB301, MXDI102, MXDI301, MXEX301, MXFU302, MXFU401, PES1007, PES1008 —
315 equations, all of them lost.

**Output shape.** A bare `<math xmlns="http://www.w3.org/1998/Math/MathML">…</math>`,
emitted inline where the equation sat. That is the form the human developers hand-wrote:
1822 of the ~2009 `<math>` tags across `01-Finalized_Modules_` are exactly it (105 add
`display="inline"`, 66 `display="block"`), so the downstream HTML build can pass the
equation straight through. The token conventions follow the same corpus — a single letter
is `<mi>`, digits are `<mn>` (a thousands separator or decimal point stays inside one
number), prose inside an equation is one `<mtext>`, and everything else including both
deltas is `<mo>` (the corpus has 45 `<mo>Δ</mo>`).

**How.** New `js/omml-to-mathml.js` (`OmmlToMathml`): a pure string-producing converter
that walks DOM-shaped nodes and covers the whole vocabulary the corpus contains —
`m:r`/`m:t`, `m:f`, `m:d`, `m:sSup`, `m:sSub`, `m:rad` — plus the rest of the common OMML
grammar (n-ary operators, roots with degrees, matrices, equation arrays, accents, bars,
limits, function application, pre-scripts) so a future template cannot reintroduce the
bug. Anything still unrecognised is recursed into as an `<mrow>` and counted in
`stats.unknownElements`, so a new construct surfaces instead of disappearing. Tracked
changes inside an equation follow the parser's existing rule: insertions kept, deletions
dropped.

`DocxParser` gains `M_NS`, an optional `ommlConverter` (null when the script is not
loaded — the parser then behaves exactly as before), `_extractMath` / `_extractMathPara` /
`_makeMathRun`, `_isMNS`, and a `stats.mathEquations` counter. The equation becomes a run
flagged `isMath`. `OutputFormatter.formatParagraph` emits such a run verbatim: no
bold/italic markers, no whitespace trim, no highlight tick, no hyperlink suffix — each of
those would corrupt the markup.

**Verified.** Driving the real parser and formatter over Chris's MathMLTest.docx with a
real XML DOM: 32 of 32 equations converted, 32 `<math>` elements in the output, zero
unrecognised OMML elements. An A/B of the same run with the converter disabled shows the
non-equation output is **byte-identical** — the only difference is the recovered
equations, plus one bullet that had nothing but an equation in it and so used to be
dropped as an empty paragraph. Against the real PES1008 Writers Template: 24 of 24
equations converted, zero unknown elements, structurally matching the human developer's
gold MathML in `01-Finalized_Modules_/Standard/PES1008` (and better-formed in places —
the gold has `<mi>(<mo>Δ</mo>E)</mi>`).

**Known, deliberately not "fixed".** Word writes ∆ (U+2206 INCREMENT); the finished
modules use Δ (U+0394 GREEK CAPITAL DELTA). Both render identically and both become
`<mo>`. The writer's character passes through unchanged, per the content-fidelity
invariant — normalise downstream if the HTML build ever wants one of them.

**Files.** `js/omml-to-mathml.js` (new), `js/docx-parser.js`, `js/formatter.js`,
`index.html`, `tests/test-runner.js`, `tests/omml-mathml.test.js` (new), `CLAUDE.md`,
`README.md`.

**Test runner.** Now also loads `js/docx-parser.js`. Only its `parse(file)` entry point
touches JSZip and the DOM; the paragraph/run walk underneath works on plain node objects,
so it can be driven directly from a test. `OutputManager` stays mocked as before.

**Tests.** 204/204 passing (was 174/174; 30 added). Removing the two production branches
fails 5 of them.

---

## 2026-07-30 — Page Stitcher upload container: ADDITIVE drops + a removable file list

**What.** Three changes to the Page Stitcher's one upload container, plus refreshed intro copy.

1. **Each drop ADDS instead of replacing.** Dropping a second batch used to wipe the first — so
   an interactive-insertion upload was impossible in practice, because the module pages and the
   built interactives arrive as two separate zips extracted to two different folders and
   therefore take two drag-and-drop actions. `addFiles()` now appends; re-adding the same
   filename replaces just that entry (newest wins). Browsing via the hidden input clears its
   `value` afterwards so the same file can be re-picked after a removal.
2. **The staged files are listed and editable.** Every file appears in a list under the drop
   zone with a **✕** that removes only that file, plus a *Remove all files* link — the set can be
   corrected BEFORE Stitch is pressed. The chip above it reads "N files ready to stitch — drop
   more to add them."
3. **`*_interactives.txt` is silently ignored.** The HTML Generator ships that worklist in the
   same zip as the pages, so a "select all" sweeps it in; by stitch time the interactives are
   already built and it has nothing to do. It is dropped at the door — never staged, never
   counted, and never mentioned anywhere in the UI (the old ".txt worklist ignored" summary line
   is gone). The same filter runs again inside `_partitionUploads()` for callers that hand read
   files straight to `stitchReadFiles()`. Other `.txt` files are untouched by the rule.
4. **Intro copy** rewritten to Chris's wording ("PageForge automatically detects which of the two
   modes to activate based on the files you upload…"), and a drop-zone hint added telling the
   user that drops accumulate. The stale "converted with *Extract un-built interactives* ticked"
   phrase went with it — that switch was retired at V2 round 235.

**Why.** Chris hit the replace-on-second-drop behaviour while testing interactive insertion on
OSAI201; without accumulation the feature cannot be used with real downloads.

**How.** `PageStitcherMode`: new `addFiles` / `removeFile` / `clearFiles` / `_indexOfName` /
`_normaliseIncoming` + `static isIgnoredUpload(name)`; `setFiles` keeps its replace semantics
(and the same filter) so existing callers and tests are unchanged; `_renderFiles` now builds the
per-file rows and binds each ✕; `init` binds the drop/browse to `addFiles` and the new
*Remove all files* button. UI: `#stitch-file-list`, `#btn-stitch-clear`, a `.drop-zone-hint`, and
`.staged-file-list` / `.staged-file-row` / `.staged-file-remove` / `.btn-link-clear` styles.

**Files touched.** `js/page-stitcher.js`, `index.html`, `css/styles.css`,
`tests/page-stitcher.test.js` (+5 tests; also refreshed the one stale assertion that still
expected the retired "Extract un-built interactives" wording),
`SPLIT_MODE_AND_STITCH_CONTRACT.md` (§5 pointer + new §10a-bis), `README.md`. **Tests 168/168.**
**No V2 engine or data file touched** — the module-conversion corpus is unaffected, so no
regeneration and no converter round.

---

## 2026-07-28 — Page Stitcher second job: INTERACTIVE INSERTION (auto-detected)

**What.** The Page Stitcher now has a dual purpose behind the one Stitch button. New mode:
upload the module pages generated by the HTML Generator in EXTRACT mode (each un-built
interactive a `cv2-int-ref` marker with a unique reference code) together with the built
interactives from the new **Interactives Claude project** (each build wrapped
`<section class="cv2-built" data-cv2-ref="CODE-INT-NN-SS-type">`). Every build replaces its
marker in place, both anchors are removed, and the finished pages download (single file, or
`<CODE>-final.zip` when the module has several pages). Which job runs is auto-detected from the
uploaded files; the original split-mode lesson stitch is behaviourally unchanged, and `.txt`
worklists dropped in by mistake are set aside with a note. Full contract:
`SPLIT_MODE_AND_STITCH_CONTRACT.md` §10. The Claude-project package (instructions + knowledge
files) lives at the corpus root in `CLAUDE_PROJECT__Interactives/`.

**Why.** Step 2/3 of the module build process: developers hand the `{CODE}_interactives.txt`
worklist to a dedicated Claude project and need the finished builds placed back into the pages
without hand-splicing. The reference codes the V2 converter already emits (extract mode, r138/
r205) are the placement contract.

**How.** Pure string/regex core on `PageStitcher` (`bareRefId`, `findIntRefMarkers`,
`parseBuiltSections`, `insertInteractives`, `stitchInteractives` + a generic balanced
class-element scanner) — full-code and bare-id refs normalise to one key; unmatched markers are
LEFT IN PLACE (warned, page stays re-stitchable), duplicate codes fail hard, nothing downloads
on a setup error. Adapter: `_partitionUploads` (detection) + `_stitchInteractiveUploads`
(OutputManager clear → addFile → downloadFile / downloadAsZip) + `_renderInteractiveSummary`
(per-page counts, warnings). UI: stitcher intro copy + drop-zone label + `accept=".html,.htm,.txt"`.

**Files touched.** `js/page-stitcher.js`, `index.html` (stitch section copy/accept only),
`tests/page-stitcher.test.js` (+11 tests), `SPLIT_MODE_AND_STITCH_CONTRACT.md` (§10),
`CONVERTER_V2/outputs/_probe_stitcher_e2e.cjs` (new, outside the repo). **No V2 engine file
touched** — converter output is byte-identical by construction; no converter round.

**Tests.** `node tests/test-runner.js` → **162/162 passed** (was 151). End-to-end probe on real
modules: ENFUN05 (1 page / 21 codes) and XDLS908 (9 pages / 65 codes) — ALL LEGS PASS (markers
== txt codes, all placed exactly once, zero anchors remain).

**Same-day addendum — All_Interactives alignment.** Chris supplied `FINAL_MODULE_DATA/
All_Interactives/` (the design team's template library — the source of truth for widget markup;
its `_other_info/Te kura interactive components v2.txt` catalogue + 90 refresh_* demo pages).
Analysis outcome: (1) the stitcher gained **head-include injection** for the library's only two
script-dependency widgets — a placed build carrying class `crossword`/`wordFind` gets
`js/crossword.js`/`js/wordFind.js` inserted before `</head>` once, never duplicated
(`PageStitcher.INTERACTIVES.headIncludes`, `_injectHeadIncludes`; +1 test → **163/163**;
contract §10c updated); (2) the Claude-project package was corrected against the library —
worked example now mirrors the shipped XDLS908 1A gold form (no autoCheck/images/blanks;
three-button row; meaningful alts), radioQuiz `answer="true|false"`, selfCheck
`checkOn`/`sCAnswerContainer` semantics, clickDrop's two forms, autoCheck ⇒ Reset-only,
deprecated list, shuffle default — and the v2 catalogue itself joined the knowledge as
`05_TK_Interactive_Components_Catalogue_v2.md` with an errata banner (MCQ + memoryGame sections
lag the live demos; demos win).

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
