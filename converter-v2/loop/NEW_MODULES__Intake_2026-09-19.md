# New module intake — 19 September 2026

The 98 modules collected in `00-NEW_NEW_NEW` are now in the corpus, parsed, and converted.
No engine change was made, so nothing in `pageforge-site` was touched and no round was shipped.

## 1. What was created

Per module, in `01-Finalized_Modules_/{Template}/{CODE}/`:

- `{CODE} Writers Template.docx` (+ `{CODE} Media List.docx`, or the combined
  `{CODE} Writers Template + Media List.docx`)
- `{CODE} …_parsed.txt` beside each — **143 generated, 0 failed**
- the human HTML on the r243 library form `{CODE}_{lesson}_{part}.html`

and the matching PageForge build in `01-Claude_Modules_/{Template}/{CODE}/` for the 78 that
converted.

**Placement:** 64 Standard, 28 Fundamentals, 3 Inquiry, 3 Bilingual. Family read from the
container class in the human HTML, cross-checked against sibling placement. Chris's standing
FUN rule held perfectly — all 28 FUN-coded modules were independently classed Fundamentals
by their body class, so no exception was needed. Detail in
`00-NEW_NEW_NEW/_INTAKE_AUDIT_2026-09-19.md` Part 4.

**Parsed txt:** regenerated with the original PageForge V1 parser via
`CONVERTER_V2/outputs/parse_docx.cjs`. **Proven byte-identical 5/5** when replayed against
existing corpus modules (SCCH301, CHFUN01, PNR101 Media List, OSSC401, BLL251) across three
template families — the same proof standard the 3 Aug intake used.

**Harness repair.** `parse_docx.cjs` carried absolute paths from a retired session
(`/sessions/inspiring-ecstatic-edison/...`) and could not run at all. It now resolves its two
dependencies from `PF_NODE_MODULES` (default `$HOME/pfdeps/node_modules`) and its JS directory
from its own location, so it survives a machine change. `jszip` + `@xmldom/xmldom` are
installed outside the connected folder. `outputs/` is not in the git repo, so there is nothing
to commit.

## 2. Results — gold vs Claude

**78 of 98 converted. 504 Claude pages against 492 gold pages on those modules.**

Skeleton SCAFFOLD match (the project's primary metric), 0 pairs skipped:

| Population | Pairs | Mean SCAFFOLD | Median |
|---|---:|---:|---:|
| **Pre-existing corpus** | 1956 | **54.08 %** | 54.72 % |
| **This intake** | 393 | **48.41 %** | 50.00 % |
| Combined | 2349 | 53.13 % | 54.03 % |

The pre-existing 1956 pairs read **54.08 %** — the round-407 baseline exactly (54.084 %).
**That is the proof that this intake changed nothing that already worked**: no existing module
was rebuilt, and the corpus mean moved 54.084 → 53.13 % purely because 393 never-tuned pairs
joined the population. A re-baselining, not a regression — the same thing that happened at
r197 (TEDC401/402), r221 (ENGJ403) and the 3 Aug intake.

Of the new 393 pairs: 197 are ≥50 %, 26 are ≥75 %, 1 is ≥90 %.

**Best of the intake:** SCBI301 76.6 %, CBI1005 70.0 %, ENGC204 65.9 %, ENGC403 62.9 %,
SCES201 62.5 %, PWY1009 62.5 %, PWY1007 61.4 %, PWY1002 60.1 %, COM1006 60.0 %.

**19 of 78 reproduce the human page set exactly.**

## 3. The 20 that did not convert

| Count | Modules | Why |
|---:|---|---|
| 12 | XOTPB08–13, XOTPG01, XOTPG03–06, XOTPO01 | the activity-table dialect — no `[TITLE BAR]`, so the input is refused. Expected; spec in `_SPEC__XOTP_Activity_Table_Template.md` |
| 7 | GER1003–1007, SAM1005, SAM1006 | **no Writers Template exists at all** — not a converter fault |
| 1 | PMT101 | a genuine converter gap, diagnosed below |

Their empty `01-Claude_Modules_` folders were removed, so no ghost directory can skew pairing
(the r285 trap). Claude corpus: **494 module dirs** (416 before).

## 4. Findings worth a round

### 4.1 PMT101 — the fully table-laid-out Te Aka Taumatua template is refused

`ModuleResolver.PrepareRun` accepts a document as a Writers Template only when
`DocxExtractor.LooksLikeWritersTemplate` finds a **paragraph-level** red span resolving to a
content opener (`[TITLE BAR]` / `[LESSON … CONTENT]`) or to an `ELEMENT` / `CONTAINER_OPEN`
directive. Measured, red bracket runs inside tables vs at paragraph level:

| Module | in tables | at paragraph level | paragraph-level tags | converts |
|---|---:|---:|---|---|
| PMT101 | 450 | **3** | `[tags]`, `[Content for DROP DOWN MENU]` | **no** |
| PNR107 | 241 | 11 | … `[MODULE CONTENT: PAGE 1]`, `[END OF PAGE]` | yes |
| TRR116 | 1057 | 22 | … `[Lesson 2]`, `[End Page]` | yes |

PMT101 lays its **entire** bilingual content in a two-column table (te reo left, English
right), so every one of its 450 real tags is in a table cell. Its only paragraph-level tags are
front-matter `[tags]` and the menu marker `[Content for DROP DOWN MENU]` — neither is an
opener. Round 212 already recorded this family's shape ("its `[TITLE BAR]` tags live inside
TABLE cells, which the standard chain never sees") and added a rescue to the *trim* step —
but the *recognition* step still requires a paragraph-level opener.

**Fix direction:** either let `LooksLikeWritersTemplate` look inside table cells for a
`[TITLE BAR]`, or admit `[Content for DROP DOWN MENU]` as an opener for this family — r212
already treats it as the rescue anchor, so the second is the smaller change. Its own round,
behind a data flag and an env toggle.

**Ruled out along the way:** a UTF-8 BOM before the XML declaration. PMT101's Writers Template
does carry one, but **30 of the corpus's 762 docx carry a BOM** and almost all convert
(WJFUN106–308, CHFUN06–08, FRFUN07, HPFUN403, BLL251/256/257/264/266/274, TRR203 …), so the
BOM is handled. Also ruled out: red-hex case (`FF0000` vs `ff0000`) — `DocxExtractor` line 1477
already lower-cases it.

### 4.2 The WJFUN family is a single-file page model — the intake's biggest lever

21 WJFUN modules plus JPFUN01/02 ship **one** human page each, and the converter builds 2–5.
Their mean SCAFFOLD is **10.4 %**, and they occupy 17 of the worst 25 module scores in the
whole corpus.

This is the documented `page_model: "single-file"` class (r106 / r186 `MTKPAGE_OFF`) — the same
finding the 3 Aug intake recorded for CHFUN, which was then fixed. The WJFUN writers use
`[End page]` to delimit **in-page sections**, not files, and the family simply has no registry
entry declaring it. Excluding these 23 modules, the intake's remaining 55 modules mean 45.8 %.

**This is a data-only change** — a registry entry per family, no code — and it would lift the
weakest 23 modules of the intake at once. It is the highest-value next round by a wide margin.

### 4.3 XOTP needs an input adapter, not a new engine

Covered in full in `00-NEW_NEW_NEW/_SPEC__XOTP_Activity_Table_Template.md`. No new builders
and no new template mode: every page is plain Standard (`container-fluid`) and every widget it
uses already exists. The work is a doc-shape detector, a section-heading lexicon, an implicit
page break, and one fix so a `CS: Create a …` line is consumed as a build instruction rather
than printed as a red Writers Note.

## 5. What was NOT done — read this before trusting any gate number

- **No engine change of any kind.** `pageforge-site` is clean; no `data/*.json`, no `app/js`,
  no `Config.js` AppVersion bump, no changelog round entry. The only file edited was the
  out-of-repo `outputs/parse_docx.cjs` path repair, which cannot affect output.
- **No corpus regeneration.** Chris did not write `REGENERATE CORPUS`, and none was run. The
  78 builds are first-time conversions of modules that had no Claude directory; not one
  pre-existing module was rebuilt, which the 1956-pair 54.08 % reading proves.
- **Only the skeleton gate was measured.** `compare_structure`, `body_compare`, the
  structural-defect scan, the tag gate and the eight widget verifiers were **not** re-run.
  Their round-407 baselines still describe the pre-intake population and will all shift when
  next run, because the population grew from 1956 to 2349 pairs.
- **`compare_set.txt` is untouched** — 200 entries, unchanged since 13 July; none of the 98
  appear in it, so anything reading that list is unaffected.
- **File deletion was enabled** for the connected folder this session, because
  `batch_convert` removes each module's output folder before rewriting it (the known EPERM
  trap). It was used only for conversion outputs and the 20 empty ghost directories.

## 6. Recommended order of work

1. **The WJFUN / JPFUN single-file page model** — a data-only registry entry; lifts 23
   modules off ~10 %.
2. **PMT101's table-only opener** — small, precedented by r212, unblocks the last refused
   module that has a template.
3. **XOTP round 1** (recognition) then **round 2** (the adapter) — both output-inert for the
   existing corpus, since nothing else carries a `Section heading | Text/Activity` table.
4. Chase the missing source files in `_INTAKE_AUDIT_2026-09-19.md` Part 1 — 7 modules still
   have no Writers Template, and XOTPB08 needs its author to type out a pasted image.
