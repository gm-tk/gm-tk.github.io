# New module intake — 3 August 2026

24 signed-off modules from `new-html-files-and-wt` staged into the corpus and run
through Converter V2. Source folder left untouched.

## What was created

Per module, in `01-Finalized_Modules_/{Template}/{CODE}/`:

- `{CODE} Writers Template.docx` + `{CODE} Writers Template_parsed.txt`
- `{CODE} Media List.docx` + `{CODE} Media List_parsed.txt`
- human HTML renamed to the r243 library form `{CODE}_{lesson}_{part}.html`

and the matching Claude build in `01-Claude_Modules_/{Template}/{CODE}/`.

**Placement:** 15 Standard, 9 Fundamentals. Family was read from the container
class in the human HTML (`inquiry` / `fundamentals` / `reoTranslate`), cross-checked
against sibling placement — BLL251/253/262/263 and BLLR201 sit in Standard beside
BLL252/BLL261/BLL264; CEDO502 in Standard beside CEDO501.

This also satisfies the standing rule that **a module code containing `FUN` is a
Fundamentals template**: all nine FUN-coded modules here (CHFUN01/04/05/06/07,
HPFUN301/402/403/901) went to Fundamentals, and no FUN-coded module went elsewhere.

Eight *pre-existing* modules break that rule and, per Chris (3 Aug 2026), **stay where
they are** — their gold HTML was built with another template, and the gold is the
per-module target: `Inquiry/` ENGFUN02, EXPFUN02–06 (`class="inquiry container-fluid"`)
and `Standard/` EXPFUN07, SSFUN07 (no family class). Re-filing them would shift their
cascade grouping away from what the artefacts say.

**Parsed txt:** regenerated with the original PageForge V1 parser (`docx-parser.js` +
`formatter.js`) run under Node. Proven exact — **17/17 byte-identical** when replayed
against existing corpus modules across all four template families. Harness kept at
`CONVERTER_V2/outputs/parse_docx.cjs`.

## Results — gold vs Claude

Mean SCAFFOLD match across the 99 paired pages is **53.0%**, against a corpus
baseline of 49.6%. 0 pairs skipped.

| Module | Family | Gold | Claude | SCAFFOLD |
|---|---|---:|---:|---:|
| SCPH301 | Standard | 9 | 9 | 70.9% |
| SSCI205 | Standard | 10 | 10 | 68.9% |
| SCCH301 | Standard | 9 | 9 | 68.1% |
| HPRE203 | Standard | 8 | 8 | 63.7% |
| OSSM401 | Standard | 5 | 5 | 61.3% |
| BLL251 | Standard | 3 | 3 | 57.7% |
| HPFUN403 | Fundamentals | 1 | 1 | 54.5% |
| OSSC401 | Standard | 5 | 5 | 53.0% |
| ENGS405 | Standard | 20 | 1 | 52.4% |
| XGF9002 | Standard | 10 | 10 | 50.4% |
| BLLR201 | Standard | 7 | 8 | 49.9% |
| BLL253 | Standard | 3 | 3 | 49.3% |
| OSSC501 | Standard | 6 | 6 | 48.5% |
| BLL263 | Standard | 3 | 3 | 46.2% |
| HPFUN402 | Fundamentals | 1 | 1 | 40.4% |
| CEDO502 | Standard | 13 | 10 | 37.3% |
| HPFUN301 | Fundamentals | 1 | 1 | 36.1% |
| BLL262 | Standard | 3 | 3 | 33.0% |
| HPFUN901 | Fundamentals | 1 | 1 | 23.0% |
| CHFUN01 | Fundamentals | 1 | 2 | 17.2% |
| CHFUN04 | Fundamentals | 1 | 3 | 14.8% |
| CHFUN06 | Fundamentals | 1 | 10 | 12.1% |
| CHFUN07 | Fundamentals | 1 | 1 | 11.0% |
| CHFUN05 | Fundamentals | 1 | 52 | 1.0% |

**16 of 24 reproduce the human page set exactly.**

## Findings worth a round

1. **CHFUN family single-file page model (5 modules).** The CHFUN writers use
   `[End page]` to delimit *in-page sections*, not files — 37 of them in CHFUN05
   alone. The converter honours each as a page boundary, so CHFUN05 ships 52 files
   against the human's 1. This is the documented `page_model: "single-file"` class
   (r106 / r186 `MTKPAGE_OFF`); the CHFUN family simply has no registry entry
   declaring it. Template attributes are all correct (`combo` via the r245
   last-resort default) — this is purely pagination.

2. **CEDO502 sub-pagination (−3).** Every lesson number is right; three sub-pages
   are missing (`1_2`, `3_1`, `4_1`). Structurally close otherwise.

3. **BLLR201 (+1).** One extra trailing page `6_0`.

4. **ENGS405 is not a converter fault.** Its Writers Template is the landing page
   only — about 10 KB of text against a 20-page human build. The lesson content is
   not in the supplied document.

## Skipped (per your call)

- **SCBI202** — Writers Template + Media List, no human HTML to compare against
- **CEDO204** — HTML + Writers Template, no Media List
- **SCFUN09** — HTML + Writers Template, no Media List

Their files remain in `new-html-files-and-wt`.

## Two things to note

- **HPFUN301** already existed. Its Word docs were byte-identical, so only the HTML
  was refreshed to the newer build; the old one is kept beside it as
  `HPFUN301.html.superseded.bak` (not a `.html`, so no gate sees it).

- **The gate population has grown.** `_skeleton_compare.py` and friends score every
  module directory they find, so the corpus is now 416 Claude module dirs / 2158
  pages (was 390 / 1994) and 454 gold dirs (was 431). The next full gate run will
  therefore report different absolute numbers than the round-245 baselines — not a
  regression, the same re-baselining that happened when TEDC401/402 joined at r197
  and ENGJ403 at r221. The new modules are **not** in `compare_set.txt`, so nothing
  that reads that list is affected.
