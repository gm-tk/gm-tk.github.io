# PageForge autonomous loop — the decisions waiting on Chris (23 September 2026)

This is a plain-English walkthrough of every question the loop has parked because it could not settle it on its own. **Nothing in this document changes any code, data or module** — it only explains. Each section stands alone, shows real examples from the files, and ends with a recommendation; the numbered questions are at the bottom.

> **ANSWERED 2026-09-23 — all fourteen**, via the click-through's answer sheet. Recorded as D13-1 … D13-15 in `LOOP_STATE.md` under "Decisions from Chris (session 38)". Ten went as recommended (1, 3, 4, 5, 6, 9, 10, 11, 12, 14). Four went differently: **2 → C** (borders + equal columns), **7 → C** (fully consecutive everywhere, accepting the known score dip as a named override), **8 → A** (copy the overview into the twelve named modules), **15 → B** (a To Do placeholder). #1 (Chris's own KB session) and #10 (collecting seven Writers Templates) stay open as human actions.

**Why now.** The loop's last two sessions (36 and 37) both stopped on *exhaustion*: every lever it is allowed to pull by itself is used up, and session 37 shipped nothing in four rounds. The remaining improvement sits almost entirely in the decisions below — above all **Decision 4 (the quiz widgets)**.

**Where these came from.** `LOOP_STATE.md` — its "Needs Chris — open decisions" list (14 open items, numbered 1–15; number 13 was closed earlier and number 16 was settled on 22 Sept by your standing instruction D12-1), the Blocked classes (all six decided on 16 Sept — nothing open), the Declined classes (none carries an open needs-Chris note beyond this list), and every "Decisions from Chris" record so nothing already answered is re-asked; `KB_AMALGAMATION_STATUS.md` (its only open row is the KB edits owed — Decision 1); and the recent `BUILD_CHANGELOG.md` entries (every BLOCKED item there was decided on 16 Sept). The decisions keep their "Needs Chris" numbers so the loop can match your answers.

**Three corrections found while preparing this report** (the loop's diary will be updated when your answers are recorded):
- **Decision 4 is re-counted.** The quiz-engine hand-off boxes on disk today number **≈ 1,159** (not 844 — that was only three of six quiz types). The session-37 figure of 1,935 counts *every* un-built widget type, and its "gold built no widget" bucket was mislabelled by a faulty class-name list.
- **Decision 9 is partly a converter fault, not a policy gap:** in several cases the writer *did* put a picture beside the speech bubble and PageForge dropped it.
- **Decision 6 found a stray file:** `BLL240 claude.html`, a Claude-made page sitting in the human gold folder, which the scorer can mistake for human work.

---

## The words used below (each defined once)

- **Writers Template (WT)** — the Word document a subject writer fills in, marking each piece with a tag in red square brackets (e.g. `[H2]`, `[Activity 1A]`, `[Button]`). The `_parsed.txt` file beside it is the same document flattened to plain text so it can be quoted; `🔴[RED TEXT] … [/RED TEXT]🔴` marks what the writer typed in red.
- **The gold** — the finished module a human developer built by hand, under `01-Finalized_Modules_/` (read-only). The best example of "what good looks like", but it spans years and template systems and contains the developers' own choices and mistakes.
- **PageForge's output (Claude)** — what the converter builds automatically from the same WT, under `01-Claude_Modules_/`.
- **The knowledge base (KB)** — the written rulebook for the HTML Convertor (`00-Other-TK-Resources/htmlconvertor-kb/`): numbered *constraints*, a *change ledger* (`CL-0001` onward) and subject *family rules*. It is the most recent statement of what a finished module should look like, and the Claude chat conversion modes follow it directly.
- **The authority order** (`LOOP__Autonomous_Rounds.md` §1b) — when sources disagree the loop follows: **1. the KB**, 2. the earlier module of the same series, 3. this module's own gold, 4. the consensus of its template/subject group. A gold habit only counts as a target when at least **60 %** of its group does it (the "share"); below that it is a human one-off.
- **The gates / the skeleton score** — the automatic scorecard: how closely each PageForge page's structure matches its paired gold page (now **54.61 %** over 2,491 paired pages). **Gate-neutral** = cannot move that score; **gate-moving** = can. **pp** = percentage points.
- **A named override** — when the loop follows a KB rule the gold doesn't, the pages that score lower are listed by name and excused from the "must not get worse" test. Intentional, not a bug.
- **Regeneration** — rebuilding output pages: **scoped** = only the modules a change touches; **full** = all ≈ 545 modules.
- **Widget / interactive** — a live, clickable element (tabs, flip cards, quizzes). **Hand-off box** — the rainbow-bordered placeholder PageForge leaves where it could not build a widget, holding the writer's raw text for a developer (also listed in the module's `{CODE}_interactives.txt`).
- **Red note / To Do** — a red line of text on the page addressed to the designer or developer, removed before a module goes live.
- **h1 / h3 / h4 / h5 / p** — HTML heading levels and a plain paragraph. To a learner `h5` is a small bold label; `p` is ordinary text.

---

## At a glance

| # | Decision | Size | My recommendation | Moves the score? |
|---|---|---|---|---|
| 1 | Bring the KB's wording up to date with your 16 Sept decisions | 0 pages; 5 KB passages + 4 status lines | You (or the loop, for your approval) do one Admin-Mode KB session | No |
| 2 | Equal-width comparison tables (`tableFixed`) | ≈ 13 tables | Accept the decline — every table stays bordered | No |
| 3 | Lesson-menu "success" label wording | ≈ 130 modules, text only | Keep the writer's wording; document it in the KB | No |
| 4 | **Build the quiz widgets** | **≈ 1,159 boxes** | **Yes — only where the writer marked the answer; carry the answer into every hand-off box** | Neutral by design |
| 5 | The journal button | ≈ 120 modules | Standardise buttons the writer asked for; never invent one | Yes (up) |
| 6 | Which version is real when a module has two | 5 modules | Tabbed single page for 4; split pages for CEDK501; remove the stray Claude file | Yes (small) |
| 7 | Renumbering duplicate / foreign activity numbers | ≈ 279 pages | Renumber only boxes PageForge made, if a trial scores net-positive | Yes (untested) |
| 8 | Empty lesson menus where the human repeated the overview | 12 modules | Keep empty (KB rule) but add the KB's missing red "please supply" flag | No |
| 9 | Character picture beside a speech bubble | 454 bubbles | Use the writer's picture where given; grey placeholder in Online Safety and TEDC only | Yes (up) |
| 10 | Seven modules with no Writers Template | 7 modules | Try to collect them, with a deadline; otherwise close as gold-only | Yes (when added) |
| 11 | XOTPB08's pasted picture | 1 module | Accept the flagged gap | No |
| 12 | Subject labels for the language modules | 12 prefixes, 0 pages | Confirm the proposed split (NCEA1 vs 1-10 Languages) | No |
| 14 | XOTP reader book material | 12 modules | Flagged placeholders now; supply the material only if re-issued | Barely |
| 15 | XOTPB Overview text in a Google Doc | 6 modules | Paste the text once; a To Do note until then | Slightly (up) |

---

## Decision 1 — Bring the knowledge base's wording up to date with what PageForge already does (Needs Chris #1, 16 Sept)

**What the issue is.** On 16 September you made nine decisions (D10-1 … D10-9). PageForge now follows five of them — but the knowledge base (the KB, the written rulebook in the `htmlconvertor-kb` repository, which the Claude chat conversion modes also follow) still *says* the old thing in those five places. Separately, one KB file (`12G`) keeps a "PageForge status" line for each recent rule change, meant to say whether PageForge has caught up; all six still read *"Not yet amalgamated"* ("amalgamated" = PageForge has built it), and four of them are now wrong. You chose on 16 Sept to make these KB edits yourself, in an **Admin-Mode** session (the KB's authorised-change mode). The loop is not allowed to write to the KB, so it can only list what is owed. It matters because the loop's authority order ranks the KB *first*; only your recorded decisions stop a later session "correcting" PageForge back to the stale wording, and a designer converting in Claude chat has no such protection — chat reads the KB directly.

**The real examples** (KB repository at `00-Other-TK-Resources/htmlconvertor-kb/`, HEAD `3d0d646`)

*1. stickyNav — D10-4 said "never emit it".* (stickyNav is a small navigation script tag in each page's invisible `<head>`.)
- The KB still says — `14_SUBJECT_GLOBAL_PARAMETERS/14A_SGP_PURPOSE_FAMILIES_1_5.md:54`: *"**Sticky nav on every page.** Add `<script src="js/stickyNav.js" … class="stickyNav"></script>` to the `<head>` of **every** page."* (similar wording at `14B…:93` and `14D…:11`). The project's own rule file, `00_PROJECT_CONTEXT_AND_PHILOSOPHY.md:85`, says the opposite: *"`stickyNav` — a templating error that was copied across modules; never emit it."*
- The human built — `01-Finalized_Modules_/Fundamentals/CHFUN01/CHFUN01_0_0.html:9`: `<script src="js/stickyNav.js" type="text/javascript" class="stickyNav"></script>` (on 1,943 of 2,993 gold pages).
- PageForge produces — `01-Claude_Modules_/Fundamentals/CHFUN01/CHFUN01_0_0.html` lines 3–9: a `<head>` with no stickyNav script (0 of 2,699 pages).
- What a learner sees: nothing different in any version — it is invisible. The risk is that a chat conversion following 14A today adds the script you banned.

*2. Equations — D10-7 said "MathML".* (MathML is the web's standard markup for maths; LaTeX is a typed maths notation that does not display in MTK.)
- The KB still says — `05_COMP_LANGUAGE_MEDIA_LAYOUT/05A_COMP12_13_LANGUAGE_MEDIA.md:217–219`: *"## MathJax / Equations — Standard LaTeX syntax. Inline: `\( \)`. Block: `\[ \]`."*
- The human built — `01-Finalized_Modules_/Standard/MXDI102/MXDI102_1.0.html:75`: `<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">` (93 gold pages).
- PageForge produces — `01-Claude_Modules_/Standard/MXDI102/MXDI102_1_0.html:77`: `<p><math xmlns="http://www.w3.org/1998/Math/MathML"><mfrac>…<mn>1</mn>…<mn>2</mn>…` (24 pages MathML, 0 LaTeX).
- What a learner sees: a properly drawn fraction in gold and PageForge; anyone following 05A would give them raw code instead.

*3. Bilingual lesson-title order — D10-2 said "Standard English first, MTK Māori first".*
- The KB still says — `01_PIPELINE_EXTRACTION_TAGS/01A_TEMPLATE_LEVELS_CORE.md:271–276`, its worked Standard example: `<h1><span>Ngā Whare </span></h1>` then `<h1><span>Housing </span></h1>` (Māori first); constraint 79 in `00G` (line 11) is silent on order.
- The human built — `01-Finalized_Modules_/Standard/ANZH104/ANZH104_02.0.html:18–19`: `Ngā Whare` then `Housing`.
- PageForge produces — `01-Claude_Modules_/Standard/ANZH104/ANZH104_2_0.html:15–16`: `Housing` then `Ngā Whare` (English first, shipped round 345).
- What a learner sees: the two title lines in opposite order. Note: here the KB's own example agrees with the gold, and only 13 of 23 gold pairs match PageForge's order — so this one is a genuine design choice you already made, not just a typo fix.

The other two owed edits: **D10-5 tables** — `06_TEMPLATE_RECOGNITION.md:405–412` still shows `<table class="table noHover tableFixed">`; should match `05D` ("`table-bordered`: General default"); PageForge ships `table table-bordered` on 5,603 of 5,604 tables. **D10-8 `alertPadding`** (an extra style class on activity boxes) — `01F_TAG_INTERPRETATION_STYLING_ACTIVITIES.md:27` gives `<div class="activity alertPadding" number="ID">` as the rule; should say "an example, not the default"; PageForge ships plain `activity` (4,341 boxes); gold 3,062 plain vs 707 with alertPadding.

The six `12G` status lines (`12_CHANGE_LEDGER/12G_PAGEFORGE_AMALGAMATION_LOG.md`, the only field that file lets you edit in place):

| Line | Rule | Should read |
|---|---|---|
| 87 | CL-0089 `learningSupport` class on X-prefixed modules | Amalgamated (15 Sept, round 319) |
| 107 | CL-0090 acknowledgement statements generated, not typed | Amalgamated (15 Sept, round 317) |
| 117 | CL-0091 iStock ID is the first number | Amalgamated (live before the loop) |
| 127 | CL-0093 CJK / pinyin language fonts | Partly: Chinese and Japanese wrapped since round 419 (21 Sept); pinyin not yet |
| 145 | CL-0094 AI Guidelines PDF rename | Not yet amalgamated (0 pages in scope) — correct as is |
| 155 | CL-0095 heading label-prefix strip | Partly: the `Lesson N` half built (rounds 324 / 344); the `FUNdamental:` half not (12 pages) |

**The numbers.** 0 pages affected — PageForge already does the decided thing everywhere. Five places of stale KB wording plus four wrong status lines. §1b (KB first) would, taken literally, make PageForge follow the stale text; only your recorded decisions override it.

**The choice.**
- **Option A — you run one Admin-Mode KB session now**: five wording changes (one change-log row each) + four status lines. About one short session, very low risk. Gate-neutral (no score moves), no regeneration.
- **Option B — let the loop draft the KB edits** as one Admin-Mode change for you to approve (this reverses your 16 Sept "I'll do it myself"). Same effect and cost.
- **Option C — leave it.** No cost now, but chat-mode conversions keep producing stickyNav, LaTeX and the old table class, and the contradiction stays.

**My recommendation is Option A (or B if you'd rather not do it by hand)** because it is small, moves no score, needs no regeneration, and removes the only way a later session or a chat conversion could undo decisions you've already made.



---

## Decision 2 — Comparison tables with equal-width columns: the unfinished `tableFixed` half of D10-5 (Needs Chris #2, 16 Sept)

**What the issue is.** A `class` is a style label on a table: `table-bordered` draws a line round every cell; `tableFixed` makes all columns the same width. On 16 Sept (D10-5) you chose "05D's `table table-bordered` everywhere (plus `tableFixed` for true two-column comparison tables)". Round 347 shipped the first half — every PageForge table is now bordered. The second half was declined: the KB's rule for comparison tables is "`table tableFixed`, *without* borders", and to recognise a "comparison" table PageForge would need a list of opposite word pairs (Advantages/Disadvantages, Can/Cannot…). The loop looked in the gold for one such convention and found the 13 comparison-header tables styled four different ways; the hook was left built but switched OFF. The KB rule is a soft "Prefer" that never defines "comparison", and writers sometimes type these tables sideways (headings down the first column), so there is no reliable signal.

**The real examples.**

*AGH1003, lesson 6 — Advantages / Disadvantages, typed sideways.*
- The writer typed — `01-Finalized_Modules_/Standard/AGH1003/AGH1003 Writers Template + Media List_parsed.txt` lines 1121–1123: `┌─── TABLE ───` / `│ Advantages of direct drilling ║ • Quicker and easier than cultivation. …` / `│ Disadvantages of direct drilling ║ • No opportunity to fix compaction …`
- The human built — `01-Finalized_Modules_/Standard/AGH1003/AGH1003_06.0.html` lines 338–342: `<table class="table table-bordered tableFixed">` … `<tr class="rowSolid">` / `<th>Advantages of direct drilling</th>` / `<th>Disadvantages of direct drilling</th>`
- PageForge produces — `01-Claude_Modules_/Standard/AGH1003/AGH1003_6_0.html` lines 60–63: `<table class="table table-bordered">` / `<tr>` / `<td>Advantages of direct drilling</td>` / `<td>• Quicker and easier than cultivation. …`
- What a learner sees: gold — two equal columns with coloured headings side by side; PageForge — two rows (label cell + text cell), exactly as the writer typed. The human turned the table on its side, so no header-word test would ever have caught this one.

*MXFU401, lesson 2 — Input / Output.*
- The writer typed — `01-Finalized_Modules_/Standard/MXFU401/MXFU401 Writers Template + Media List_parsed.txt` lines 317–320: `┌─── TABLE ───` / `│ **INPUT** ║ **OUTPUT**` / `│ 1 ║ 17` / `│ 2 ║ 20`
- The human built — `01-Finalized_Modules_/Standard/MXFU401/MXFU401_2.0.html` lines 640–643: `<table class="table table-bordered tableFixed">` / `<tr class="rowSolid">` / `<th><b>Input</b></th>` / `<th><b>Output</b></th>`
- PageForge produces — `01-Claude_Modules_/Standard/MXFU401/MXFU401_2_0.html` lines 230–233: `<table class="table table-bordered">` / `<tr>` / `<th>INPUT</th>` / `<th>OUTPUT</th>`
- What a learner sees: both bordered grids; the gold's two columns are equal widths, PageForge's size to their contents.

*BLL254, lesson 1 — Present tense / Past tense (PageForge already matches the gold).*
- The writer typed — `01-Finalized_Modules_/Standard/BLL254/BLL254 Writers Template_parsed.txt` lines 163–166: `┌─── TABLE ───` / `│ **Present tense** ║ **Past tense**` / `│ bring ║ brought` / `│ buy ║ bought`
- The human built — `01-Finalized_Modules_/Standard/BLL254/BLL254_1.0.html` lines 224–228: `<table class="table table-bordered">` / `<thead>` / `<tr>` / `<th>Present tense</th>` / `<th>Past tense</th>`
- PageForge produces — `01-Claude_Modules_/Standard/BLL254/BLL254_1_0.html` lines 84–87: `<table class="table table-bordered">` / `<tr>` / `<th>Present tense</th>` / `<th>Past tense</th>`
- What a learner sees: the same bordered grid in both. The KB's rule would *remove* the borders here — moving the page away from the gold.

**The numbers.** Tiny: 13 two-column contrast-header tables in the whole gold (`CONVERTER_V2/outputs/_r347_tables.json`); about 13 PageForge tables whose headers match the hook's word list (measured 16 Sept, before the two module intakes — would need re-measuring). The gold's 13: plain `table` 4, bordered only 3, bordered + `tableFixed` 5, the KB's exact form (`table tableFixed`, no borders) 1 (share 0.08); any bordered form 8 (0.62). Across all gold tables `tableFixed` is on 551 of 1,819 (0.30) and tracks column count rather than meaning. The KB — `05_COMP_LANGUAGE_MEDIA_LAYOUT/05D_COMP14_BUTTONS_TABLES_COLUMNS.md` line 239: *"`tableFixed`: Prefer for two-column comparison tables (e.g., "Can" vs "Cannot", "Pros" vs "Cons", "Advantages" vs "Disadvantages") where equal column widths are desirable. Use `tableFixed` WITHOUT `table-bordered` for these cases."* §1b: the KB (level 1) has a rule, but a soft "Prefer" with no definition; the only style clearing the 0.60 group share (level 4) is "bordered" at 0.62 — which is what ships today.

**The choice.**
- **Option A — accept the decline.** Every table stays `table table-bordered`; at the Admin-Mode KB session (Decision 1) 05D line 239 is reworded to "optional". No page changes; gate-neutral; no regeneration.
- **Option B — re-specify in the KB's own form**: only a two-column table whose header row is a true opposite pair (can/cannot, pros/cons, advantages/disadvantages, similarities/differences…) gets `table tableFixed` (equal widths, *no* borders). About 5–6 tables lose their borders — most moving *away* from the gold (a named KB-over-gold override); the AGH1003 sideways kind is still missed. Slightly gate-moving (down); scoped regeneration.
- **Option C — "bordered + `tableFixed`"** on true comparison tables: keeps borders, adds equal widths — the gold's single most common form here (5 of 13). Contradicts 05D's "WITHOUT `table-bordered`", so 05D needs editing first. Tiny gate move (up); scoped regeneration.

**My recommendation is Option A** because the whole question covers about a dozen tables, the only visible difference is column width, the writer gives no reliable signal, and the gold's majority (bordered, 0.62) is what already ships; rewording 05D closes the item for good. If you *want* equal-width comparison tables as a house style from now on, C is the honest version, not B.



---

## Decision 3 — The wording of the "success" label in lesson menus: the unfinished half of D10-9 (Needs Chris #3, 16 Sept)

**What the issue is.** Each lesson page has a drop-down **module menu** with two labels: what we are learning, and how the student shows they have learned it (the *success* label). In D10-9 you chose to make both labels `<h5>` headings (a small bold label) in the KB's standard wording. Round 349 shipped the heading form and normalised the learning label to "We are learning:". But the KB's success wording depends on year level — "You will show your understanding by:" for Years 1–6, "I can:" for Years 7–10 — and the loop had no year table, so it kept the writer's own success wording everywhere. It then found the gold doesn't follow the year rule either: each module is consistent with itself (only 6 of ≈ 130 mix both), but level doesn't predict which wording a module uses. **New finding for this report:** a year source *does* exist — every PageForge page already carries its year band in its `template="…"` attribute (e.g. `template="7-8"`), matching the gold on all 6 modules checked. So the real question is no longer "supply a year list"; it is whether the KB's year rule should override the writer's wording, given that the gold only half-follows it.

**The real examples.**

*ENGR302, lesson 1 (Years 7–8) — the KB rule would move this page toward the gold.*
- The writer typed — `01-Finalized_Modules_/Standard/ENGR302/ENGR302 Writers Template + Media List_parsed.txt` lines 95–103: `🔴[RED TEXT] [Lesson Overview] [/RED TEXT]🔴` / `We are learning to:` / `• *explore and identify power relationships in various texts.*` / `You will show your understanding by:` / `• *identifying* *and matching examples of power relationships …*`
- The human built — `01-Finalized_Modules_/Standard/ENGR302/ENGR302_1.0.html` lines 32–42: `<h5>We are learning:</h5>` … `to explore and identify power relationships in various texts.` … `<h5>I can:</h5>` … `identify and match examples of power relationships in everyday` …
- PageForge produces — `01-Claude_Modules_/Standard/ENGR302/ENGR302_1_0.html` lines 22–28: `<h5>We are learning:</h5>` … `<h5>You will show your understanding by:</h5>` / `<ul>` / `<li>identifying and matching examples of power relationships in everyday life and literature.</li>`
- What a learner sees: gold — "I can: identify and match…"; PageForge — "You will show your understanding by: identifying and matching…". Note the human changed the list item's grammar as well as the label.

*ANZH301, lesson 1 (Years 7–8) — the KB rule would move this page away from the gold, and break its grammar.*
- The writer typed — `01-Finalized_Modules_/Standard/ANZH301/…_parsed.txt` lines 122–126: `🔴[RED TEXT] [Lesson Overview] [/RED TEXT]🔴` / `In this lesson we are learning about the push and pull factors/reasons why more Māori moved to the cities …` / `You will show your understanding by:`
- The human built — `01-Finalized_Modules_/Standard/ANZH301/ANZH301_1.0.html` lines 32–35: `<p>In this lesson we are learning about the push and pull factors …</p>` / `<p>You will show your understanding by:</p>` / `<ul>` / `<li>using multiple sources of information to help you answer the question: …`
- PageForge produces — `01-Claude_Modules_/Standard/ANZH301/ANZH301_1_0.html` lines 22–25: `<p>In this lesson we are learning about the push and pull factors …</p>` / `<h5>You will show your understanding by:</h5>` / `<ul>` / `<li>using multiple sources of information …`
- What a learner sees: gold and PageForge say the same words. The KB's 7–8 rule would give "I can: using multiple sources…" — ungrammatical unless PageForge also machine-rewrites the writer's list items.

**The numbers.** About 130 modules have a lesson-menu success label; text only, no layout change. A quick first-lesson-page check this session (53 modules with a label on both sides — not a loop instrument; to be re-run properly if you pick B or C): the writer's wording (today's output) matches the gold on 40 of 53 (0.75). On the 40 with a Years 1–10 template, the writer's wording matches on 27 — and the KB year table *also* matches on 27; switching would change 22 modules, 11 toward the gold and 11 away. Gold by level:

| Level | Gold "You will show…" | Gold "I can:" | KB table says |
|---|---|---|---|
| Years 1–3 | 5 of 7 | — | "You will show…" |
| Years 4–6 | 6 of 9 | — | "You will show…" |
| Years 7–8 | 7 of 15 | 8 of 15 | "I can:" |
| Years 9–10 | — | 8 of 9 | "I can:" |
| NCEA | 5 of 12 | 7 of 12 | *no row* |

The KB — `01_PIPELINE_EXTRACTION_TAGS/01B_MODULE_MENUS_FOOTER.md` lines 240–244 (the year table) and line 246: *"Regardless of what label text the writer uses … ALWAYS normalise to the standard pattern for the template level shown in the table above."*; constraint 23 (`00_MASTER_INSTRUCTIONS/00D_CONSTRAINTS_1.md` line 31): *"normalised to standard patterns … NOT writer's verbatim text"*. §1b: level 1 (the KB) has an explicit rule and outranks the gold — arguing for B — but the gold only half-follows it, it has no NCEA row, and applying it properly means rewriting writers' list items.

**The choice.**
- **Option A — keep the writer's wording** (status quo); the KB edit changes 01B line 246 to "the writer's success wording is kept; the year table is the default when the writer gives none". No page changes; gate-neutral; no regeneration.
- **Option B — apply the KB year table** from the page's existing `template` attribute (NCEA left as the writer's wording). Roughly half the modules' labels change; score roughly a wash (gate-moving both ways, ≈ net zero); to be correct the list items would also need rewording ("identifying" → "identify") — automated rewriting of writer text; scoped regeneration plus a new rewording rule.
- **Option C — you supply a per-module list** ("I can:" or "You will show…" for each of ≈ 130 modules), reproducing the gold's per-module choice. Costs your time and a hand-kept list new modules must join. Gate-moving (up); scoped regeneration.

**My recommendation is Option A** because the writer's wording already matches the human's final choice 75 % of the time, the KB's year rule does no better against the gold and can't cover NCEA, and doing it properly means machine-rewriting writers' list items; a one-line KB edit makes "writer's wording kept" the documented rule and closes the item.



---

## Decision 4 — Should the loop also build the quiz widgets? (Needs Chris #4, 17 Sept — THE LARGEST ITEM)

**What the issue is.** Some activities are meant to be live exercises — the learner ticks, types or picks an answer and the page marks it. Each is a **widget**; a **quiz engine** is a widget that *checks answers*: multiple choice (`multiChoiceQuiz`), type-the-answer (`typing`), dropdown (`dropQuiz` / `dropDown`), radio buttons (`radioQuiz`), put-in-order (`reorder`) and `selectionBox`. When PageForge can't build a widget it leaves a **hand-off box** where the widget should go: a rainbow-bordered box with a pink code such as `ARFUN04-INT-00-52-multiChoiceQuiz ▼`, which opens to an orange dashed panel headed "⚙ INTERACTIVE (un-built)" holding the writer's raw text; the same item goes into the module's `{CODE}_interactives.txt` worklist for a developer to build by hand. On 16 Sept (D10-3) you authorised *"widget-build rounds inside the loop, one type per kickoff"* — but the list of types that went with that decision came from the coverage dashboard, which filed quiz engines as "Phase-1 placeholders", so no quiz type was on it, and the loop reads the list literally. Quiz engines also differ from display widgets (accordions, flip cards) in one way that matters: they need a **correct answer**, and the loop's standing rule is "an answer is never invented". Writers mark answers inconsistently — a ✅ tick or highlight, red text, green text, a `[correct]` bracket, or nothing — and today's multiple-choice builder reads only `[correct]`.

**A correction to the numbers in the loop's diary.** The session-37 probe that sized #4 at "1,935 boxes, 1,062 of them where the gold shipped no widget" used a class-name list that misses `typing`, `reorder` and `wordFind` and mis-spells `dragAndDrop` — four of its "no gold widget" examples, opened by hand, all *did* have a built gold widget (BLL244 `typing`, AGH1004 `dragAndDrop`, BLL243 `reorder`, ANZH104 `wordFind`). And the 1,935 counts *every* un-built widget type, not just quiz engines. The figures below are re-counted straight from disk.

**The real examples.**

*ARFUN04 activity 4L — multiple choice (Fundamentals).*
- The writer typed — `01-Finalized_Modules_/Fundamentals/ARFUN04/ARFUN04 Writers Template + Media List_parsed.txt`:
  ```
  2728  🔴[RED TEXT] [Activity 4L] [H3]  [/RED TEXT]🔴**Test your knowledge** 🔴[RED TEXT] [create a tick box quiz] [answers are highlighted] [/RED TEXT]🔴
  2730  Tick the correct answer:
  2734  │ 1. What does contrast in art mean? ║ a. When everything looks the same.
  2735  ✅b. When two things are very different from each other.
  ```
- The human built — `01-Finalized_Modules_/Fundamentals/ARFUN04/ARFUN04_4.08.html`:
  ```
  45  <h3>Test your knowledge</h3>
  47  <div class="multiChoiceQuiz"> <!-- autoCheck --> <!-- mcqSomeSelected --> …
  50  <p class="mcqQuestionText">What does contrast in art mean?</p>
  53  <p class="mcqOption" value="correct">When two things are very different from each other. </p>
  90  <div class=" activityButton hidden mcqAswers">Check answers</div>
  ```
- PageForge produces — `01-Claude_Modules_/Fundamentals/ARFUN04/ARFUN04_0_0.html`:
  ```
  3723  <h3>Test your knowledge</h3>
  3730  <p style="color: #d9480f; font-weight: bold">⚙ INTERACTIVE (un-built) #64: multiChoiceQuiz (create a tick are highlighted) — Activity 4L — see ARFUN04_interactives.txt</p>
  3740  <td>1. What does contrast in art mean?</td>
  3742      b. When two things are very different from each other.
  ```
- What a learner sees: writer — four questions, right answers ticked; human — clickable options and a "Check answers" button; PageForge — a code box that opens to a static table. **The ✅ ticks are lost everywhere** (0 on the Claude page and in the worklist, `ARFUN04_interactives.txt:1288–1289`), so the developer can't see the answers from the hand-off.

*BLL244 activity 2D — type the answer (Standard).*
- The writer typed — `01-Finalized_Modules_/Standard/BLL244/BLL244 Writers Template_parsed.txt`:
  ```
  349  🔴[RED TEXT] [type the answer + autocheck] [/RED TEXT]🔴
  351  🔴[RED TEXT] What [/RED TEXT]🔴 game are Zack and Kev playing at the local school?
  361  🔴[RED TEXT] Why [/RED TEXT]🔴 does Zack glare at Kev?
  ```
- The human built — `01-Finalized_Modules_/Standard/BLL244/BLL244-2.0.html`:
  ```
  239  <div class="typing autoCheck autoShow" layout="standardNoBorder">
  241  <p><input type="text" answer="What" class="form-control" placeholder="Type here"> game are Zack and Kev playing at the local school?</p>
  250  <div class="activityButton checkAnswer hidden">Check answers</div>
  ```
- PageForge produces — `01-Claude_Modules_/Standard/BLL244/BLL244_2_0.html`:
  ```
  109  <p style="color: #d9480f; font-weight: bold">⚙ INTERACTIVE (un-built) #6: typing — Activity 2D — see BLL244_interactives.txt</p>
  111  <p>game are Zack and Kev playing at the local school?</p>
  116  <p>does Zack glare at Kev?</p>
  ```
- What a learner sees: human — a type-in box before each sentence, checked automatically; PageForge — a code box whose sentences have lost their first word (the red answer words were treated as developer notes and dropped; they survive only in `BLL244_interactives.txt:106`).

*ENGI303 activity 1A — dropdown quiz with no answer marked (Standard).*
- The writer typed — `01-Finalized_Modules_/Standard/ENGI303/ENGI303 Writers Template + Media List_parsed.txt`:
  ```
  124  🔴[RED TEXT] [Dropdown quiz] [/RED TEXT]🔴
  126  1. What is Piper’s main challenge?
  128  Learning to fly.
  130  Finding food on the beach.
  ```
  (no answer mark anywhere in lines 126–150; line 138 reads `Brave and confident.`)
- The human built — `01-Finalized_Modules_/Standard/ENGI303/ENGI303_1.0.html`:
  ```
  67  <div class="dropQuiz">
  75  <div class="dropDown" answer="2">
  79  <p>Finding food on the beach.</p>
  94  <p>Curious and confident.</p>
  ```
- PageForge produces — `01-Claude_Modules_/Standard/ENGI303/ENGI303_1_0.html`:
  ```
  83  … ⚙ INTERACTIVE (un-built) #2: dropDown — Activity 1A — see ENGI303_interactives.txt
  86  <li>What is Piper’s main challenge?</li>
  89  <p>Finding food on the beach.</p>
  ```
- What a learner sees: human — a "Select one" dropdown per question that marks the choice; PageForge — a code box with a plain list. The human supplied the answer key and even reworded an option ("Brave" → "Curious"); no converter can derive that, so here the hand-off box is the honest result.

**The numbers.** Quiz-engine hand-off boxes on disk today (counted from `01-Claude_Modules_`):

| Type | Boxes | Modules |
|---|---|---|
| multiChoiceQuiz | 386 | 178 |
| typing | 260 | 84 |
| dropDown | 248 | 132 |
| reorder | 103 | 64 |
| radioQuiz | 87 | 58 |
| selectionBox | 75 | 37 |
| **Total** | **≈ 1,159** | |

(The recorded 844 was only the first three types.) The gold builds these widely; PageForge almost never does:

| Widget | Gold pages / modules | PageForge pages |
|---|---|---|
| `multiChoiceQuiz` | 538 / 289 | 11 |
| `typing` | 348 / 152 | 0 |
| `dropQuiz` | 275 / 179 | 23 |
| `radioQuiz` | 192 / 135 | 0 |
| `reorder` | 177 / 120 | 0 |

Is the answer written down? Multiple choice: of 294 bundles, the largest clearly marked group is 24 sites; 50 have no marks and 98 are unmarked tables. Dropdown: of 123, 51 have no answer anywhere — but where the answer *was* marked, round 309 built 6 pages with 45 of 45 answers matching the human. The KB specifies these widgets in full — `03_COMP_CORE_INTERACTIVES/03D_COMP02_QUIZZES_2.md:23` (Writer Intent Signals): *"The writer marks one (or more) options as the **correct answer** — e.g. a ✅ tick, "(correct answer)", bold, or a separate answer key."*; `typing` from line 243; dropdown and multiple choice in `03C_COMP02_QUIZZES_1.md`. (KB constraint 65 is different — it covers `[MTKquiz]`, a quiz built in D2L's own quiz tool, and doesn't apply to in-page quizzes.) Answer-checking verifiers already exist for multiple choice and dropdown; none yet for typing, radio or reorder. §1b: level 1 (the KB) already names the form, so building is KB-correct and needs no gold consensus — the only open question is your permission.

**The choice.**
- **Option A — extend D10-3 to the quiz engines**, largest first (multiChoiceQuiz → typing → dropDown → radioQuiz → reorder → selectionBox), building *only* where the writer's answer is on the page (✅ / highlight, red, green, `[correct]`); anything else keeps its hand-off box. Hand-off boxes become working quizzes with Check / Reset buttons. Cost: new builders and verifiers for typing, radio, reorder, and a scoped regeneration per type — no full regeneration. Risk: misreading a mark as an answer (OSAI101's green text marks *options*, not answers) — guarded by round 309's per-activity check. Skeleton-neutral by design (a built widget is judged on its own verifier); progress shows as the dashboard's "Still a box" count falling.
- **Option B — no; quizzes stay with the developer or Interactives Build Mode.** Nothing changes; ≈ 1,159 boxes stay manual; the loop stays at exhaustion, because this is the largest item left. Gate-neutral.
- **Option C — don't build, but make the hand-off box carry the answer key** (keep the ✅ ticks and red answer words visible in the box and worklist, so the developer isn't re-reading the Word document). Cheap; scoped regeneration; expected gate-neutral (the loop would confirm).

**My recommendation is Option A with C folded in**, because the KB already specifies each quiz and names ✅ as the answer signal, the gold builds these in hundreds of modules while PageForge builds none of typing / radio / reorder, and carrying the answer mark through is needed for building anyway — and it fixes a real defect today (the hand-off loses the answers). The "never invent an answer" rule keeps cases like ENGI303 as hand-off boxes.



---

## Decision 5 — The "Go to your journal" button (Needs Chris #5, 18 Sept)

**What the issue is.** Many modules send the learner to a separate learning journal. The gold shows this in one of two house styles, by series: a green **button** "Go to journal" linked to the learner's Google Drive (older series — AGH, HIS, PES, PHE, MXFL, MXDB), or a styled **heading** `<h4 class="goJournal">Go to your journal</h4>` (newer series — ENGI30/40, ENGC30, ENGS30, XGF90, ANZH30). PageForge builds a journal element only when the writer typed a `[Button]` tag, and keeps the writer's own label and link. The "≈ 58" on your list is the gold headings added where the writer asked for nothing. The loop can't settle it because (1) the KB has no module journal-button rule; (2) the human practice splits by series and era; (3) following the gold means *inventing* a button (KB constraint 3, `00D_CONSTRAINTS_1.md`: *"NEVER invent CSS classes or HTML structures"*) or *rewriting* the writer's label (constraint 1: *"NEVER modify writer **wording**"*).

**The real examples.**

*ENGS302 activity 1C — a pure invention (heading style).*
- The writer typed — `01-Finalized_Modules_/Standard/ENGS302/ENGS302 Writers Template + Media List_parsed.txt` lines 249 / 253: `🔴[RED TEXT] [Activity 1C Learning Journal]  [/RED TEXT]🔴**Identifying the Conflict**` … `Return to your Learning Journal and write a short paragraph describing the main conflict in *Under the Skin (Soccer Ball)*.` (no `[Button]` tag)
- The human built — `01-Finalized_Modules_/Standard/ENGS302/ENGS302_1.0.html` lines 475 / 489 / 493: `<h3>Identifying the conflict</h3>` … `Return to your journal and write a short paragraph describing the` … `<h4 class="goJournal">Go to your journal</h4>`
- PageForge produces — `01-Claude_Modules_/Standard/ENGS302/ENGS302_1_0.html` lines 183–189: `<p class="cv2-note" style="color: red; font-weight: bold;">Writers Note: activity note: learning journal</p>` … `<h3>Identifying the Conflict</h3>` … `<p>Return to your Learning Journal and write a short paragraph …</p>`
- What a learner sees: human — the activity ends with the styled "Go to your journal" heading; PageForge — the instruction as plain text and a red developer note.

*HES1005 task 2B — the writer's button, relabelled and linked by the human (button style).*
- The writer typed — `01-Finalized_Modules_/Standard/HES1005/HES1005 Writers Template + Media List_parsed.txt` lines 207–209: `[Body] Click on the Learning journal button below and complete task 2B.` / `🔴[RED TEXT] [Button]  [/RED TEXT]🔴Go to Learning journal.`
- The human built — `01-Finalized_Modules_/Standard/HES1005/HES1005_2.0.html` lines 216–217: `<p>Click on the Learning journal button below and complete task 2B.</p>` / `<a href="https://drive.google.com/drive/u/0/my-drive" target="_blank"><div class="button">Go to journal</div></a`
- PageForge produces — `01-Claude_Modules_/Standard/HES1005/HES1005_2_0.html` lines 82–83: `<a href="" target="_blank"><div class="button">Go to Learning journal</div></a>` / `<p class="cv2-note" …>Designer/Developer To Do: Wire this button's link to the module's learning journal document (the href is intentionally blank — …`
- What a learner sees: human — a working "Go to journal" button opening their Drive; PageForge — a "Go to Learning journal" button that goes nowhere yet, plus a red To Do.

*AGH1004 activity 3B — a red instruction line the human turned into a sentence plus a button.*
- The writer typed — `01-Finalized_Modules_/Standard/AGH1004/AGH1004 Writers Template + Media List_parsed.txt` lines 475 / 479: `Watch the video below and answer the questions in your learning journal.` … `🔴[RED TEXT] [Button] Complete activity 3B in your learning journal [/RED TEXT]🔴`
- The human built — `01-Finalized_Modules_/Standard/AGH1004/AGH1004.03.html` lines 206–208: `<h3>Climate challenges in the Waikato</h3>` / `<p>Complete activity 3C in your learning journal.</p>` / `<a href="https://drive.google.com/drive/u/0/my-drive" target="_blank"><div class="button">Go to journal</div></a>`
- PageForge produces — `01-Claude_Modules_/Standard/AGH1004/AGH1004_3_0.html` line 130: `<a href="" target="_blank"><div class="button">Complete activity 3B in your learning journal</div></a>`
- What a learner sees: human — a titled box, a short instruction and a "Go to journal" button (the human also invented the heading and renumbered it 3C); PageForge — a button whose label is the whole sentence, with a blank link.

**The numbers.** Gold: `Go to journal` buttons ≈ 1,201; `h4.goJournal` headings ≈ 651; 151 modules have a gold journal element (button on 573 pages, heading on 263); per series the form is 1.00 one way or the other; Standard modules use the button at 0.71. PageForge: `h4.goJournal` 985 (from converter rule r239); `div.button` "Go to your journal" 160; "Go to journal" 22; the writer's own labels ("Learning journal" 42, "Go to learning journal" 35, others). **The loop's census under-counted the writer's tags** (it only recognised "go to (your) journal"): AGH1004, HES1005, MXFL203 and MXFL401 were listed as "untagged" but all have `[Button]` journal tags. So the true inventions (like ENGS302) are the small, diffuse part (≈ 58); the bigger part is label-and-link normalisation of buttons the writer *did* ask for. The KB: nothing about a module journal button (the nearest, `05D_COMP14_BUTTONS_TABLES_COLUMNS.md:55`, keeps the "Go to" prefix for dropbox and portfolio buttons). The converter's own rule r239 (`Subject_Global_Parameters.json:1664`, from developer feedback on SCCH302): *"A [button] whose EXPLICIT label folds to 'go to (your) journal' … renders as the design team's templated <h4 class="goJournal">Go to your journal</h4> INSIDE the open activity box"* — deliberately a forward-looking convention. §1b: level 1 is silent; levels 2 and 4 point to each series' form (1.00 per series) — but inventing an element with no writer signal conflicts with constraints 1 and 3, so consensus alone can't carry it.

**The choice.**
- **Option A — leave it.** A journal element only where the writer tagged a button, with the writer's label and link. No change; gate-neutral; no regeneration. Learners keep getting odd labels ("Complete activity 3B in your learning journal") and blank links with To Do notes.
- **Option B — normalise the buttons the writer did ask for**: any journal-label variant on a `[Button]` becomes *the* journal element in the house form — r239's heading everywhere, or (to match the gold) the Drive-linked "Go to journal" button in the older button-style series. Consistent labels and working links. A label rewrite, so it needs your authorisation under constraint 1. Scoped regeneration of roughly 120 journal-carrying modules; gate-moving, mostly up.
- **Option C — B, plus invent**: also add "Go to your journal" at the end of any activity that tells the learner to go to their journal but has no button (the ENGS302 case, ≈ 58 sites). Small gate move; risk of false positives on passing mentions; directly overrides constraint 3 and needs a new KB rule.

**My recommendation is Option B without C** (keeping r239's heading form unless you want the older series to match their button-style gold), because in B the writer *asked* for a button — normalising its label and link is presentation, not invention — and it fixes the learner-visible faults (odd labels, dead links); C's inventions are small, diffuse and against a KB constraint, better left to the developer.

---

## Decision 6 — When a module has two human versions, which one is the real target? (Needs Chris #6, 18 Sept)

**What the issue is.** The **gate** (the automatic scorer) **pairs** each PageForge page with one gold page and scores how closely their structure matches. Five gold folders — **MXFUN01, BLL240, CEDK501, CEDT207, CEDT301** (every gold folder was checked; no others) — hold *two* complete human builds of the same module: a **single-file** version (the whole module on one page with tabs — Inquiry "crumbs" and panels, or Fundamentals "phases" and panels) and a **split** version (separate pages `_0.0`, `_1.0` … in the Standard style). The gate can't know which is real; in practice it scores against the split pages, so a module built as one tabbed page can never be scored — and neither can the writer's black **"Tab N – label" list** (the plain-text tab list that should become the tabs across the top of the page). The loop's rules say "match the gold", and here the gold contradicts itself; which version Te Kura actually published is a fact only you can supply.

**The real examples.**

*MXFUN01 — the tabbed-phases version looks like the target.*
- Gold folder `01-Finalized_Modules_/Fundamentals/MXFUN01/`: `MXFUN01.html` (10,030 lines, single-file, `fundamentals` body) **and** `MXFUN01_0.0.html … _7.0.html` (8 split pages). PageForge (`01-Claude_Modules_/Fundamentals/MXFUN01/`): 19 split pages.
- The writer typed — `…/MXFUN01 Writers Template + Media List_parsed.txt` l.113 `[PHASE 1]`, l.115 `[Fundamental 1 code] MXFUN01`, l.117 `[Title] Number`, l.938 `[PHASE 2]` … and l.1965 `Note to developer: we want an intro page that allows ākonga to guide themselves to the skill they require. They should be able to click on the image and go to that section.`
- The human built (single file) — `MXFUN01.html` l.46 `<div class="phases">`, l.72–73 `<div class="phaseLink" phase="1"> <h3>Number Sense</h3>`, l.97–100 `<div class="fundamentalsPanel" phase="1"> … <h2>Phase 1 - Number Sense</h2>`. (The split overview, `MXFUN01_0.0.html`, has l.18 `<h1><span>Māori title here</span></h1>` and l.48 `Designer note: Need to add the phase 1,2,3,4 template`.)
- PageForge produces — `MXFUN01_0_0.html` l.12 `<h1><span>Number</span></h1>`, l.26 `<p>MXFUN01</p>`; no phase tiles.
- What a learner sees: single-file gold — one page with four clickable phase tiles; split gold — an intro paragraph, a red "need to add the phase template" note and a "Māori title here" placeholder; PageForge — a title, the bare code, then separate pages. This PageForge page scores **0.7 %, the lowest in the corpus**.

*CEDK501 — here the split version is the real one.*
- Gold folder `01-Finalized_Modules_/Inquiry/CEDK501/`: `CEDK501 Kia Mahitahi – Idea to Action.html` (255 lines, single-file) **and** `CEDK501_0.0 … _7.0` (11 split pages).
- The writer typed — `CEDK501 Writers Template_parsed.txt` l.1034 `[lesson 6] Working together for the win`, l.1188 `[Lesson 6.1]`, l.1375 `[Lesson 7]` — seven lessons, matching the 11 split pages exactly.
- The human built — the single file is an unfinished template: l.92 `Designer note: Find out the correct phase colour.`, panels 2–8 empty stubs `<h3>Heading</h3> <p>Body</p>`. The split `CEDK501_6.0.html`: l.13 `<h1>6.0</h1>`, l.15 `<h1><span>Working together for the win</span></h1>`.
- PageForge produces — `CEDK501_8_0.html` l.13 `<h1>8.0</h1>`, l.15 `<h1><span>Working together for the win</span></h1>`.
- What a learner sees: single file — "Heading / Body" in seven tabs; split gold — the finished lesson 6; PageForge — the same lesson, labelled 8.0.

*CEDT207 — the tab-list form nobody can score.*
- Gold folder `01-Finalized_Modules_/Inquiry/CEDT207/`: `CEDT207 Me, my selfie and I.html` (single-file, 7 tabs) **and** `CEDT207_0.0 … _6.0` (7 split pages).
- The writer typed — `…_parsed.txt` l.80–94: `[Page 1]` / `[Side Tabs]` / `Tab 1 – Introduction` / `Tab 2 – About Me` / … / `Tab 6 – Visual Pepeha`
- The human built (single file) — l.51–52 `<div class="crumbs"> <div crumb="1" class="showing"><p>Introduction</p></div>`, l.61 `<div class="inquiryPanel showing" rel="1">`. (Split: `CEDT207_1.0.html` l.17 is `About me`.)
- PageForge produces — `01-Claude_Modules_/Inquiry/CEDT207/CEDT207_1_0.html` l.15 `<h1><span>Introduction</span></h1>`, l.22 `⚙ INTERACTIVE (un-built) #1: tabs (side) …`, l.28–33 `<p>Tab 1 – Introduction</p> … <p>Tab 6 – Visual Pepeha</p>`
- What a learner sees: single-file gold — seven clickable tabs across the top; split gold — seven pages starting "About me"; PageForge — page 1 "Introduction" with the writer's tab list inside a striped "un-built" box. Everything after is shifted one page, so this page isn't paired or scored at all. CEDT301 is the same (`Tab 1 – Introduction` … `Tab 9 – Digital Collage`, `_parsed.txt` l.63–79).

**The numbers.** 5 modules, 41 paired pages of 2,491; their average scores 0.37 / 0.47 / 0.47 / 0.37 / 0.58 against a corpus average of 0.546 — even if all five reached the average the overall score would move only ≈ 0.1–0.2 points. (The "48 of 128 footer mismatches" figure in the loop's diary is looser than it sounds — most of those are ordinary page-count differences in non-dual modules.) A second hazard found: `Inquiry/BLL240/BLL240 claude.html` (`<title>BLL240 *CLAUDE*</title>`) is a *Claude-made* file sitting in the gold folder, which the gate can pair against as if it were human gold; BLL240_1_0 is the second-lowest page (4.5 %). The KB — `htmlconvertor-kb/06_TEMPLATE_RECOGNITION.md` l.63 *"Navigation system — Fundamentals `div.phases` → `div.fundamentalsPanel`; Inquiry `div.crumbs` → `div.inquiryPanel`"* — describes one tabbed page; `00_Module_Template_Map.md` l.302 lists all five as "Inquiry — tabbed" (*"The whole module packed into one tabbed page"*). The earlier siblings are all single-file (MXFUN02/03, BLL210/220/230/250, CEDT201–204/208); PageForge builds MXFUN01 and CEDT207 split only because they are listed as exceptions (`Style_Anchor_Registry.json`). §1b: the KB (1) and the earlier sibling (2) both say single-file, outranking the module's own gold (3) — except CEDK501, whose single file is an empty stub.

**The choice.**
- **Option A — the tabbed single-file version is the target.** The gate pairs against the single files; PageForge drops the exceptions and builds these as one tabbed page (learners get phase tiles / tabs). A gate-configuration change plus regeneration of only these 4–5 modules; gate-moving (the compared set changes — labelled as such); makes the CEDO402 / CEDT207 / CEDT301 tab-list form scoreable. Doesn't fit CEDK501.
- **Option B — the split pages are the target (today's build).** The gate ignores the single files (and `BLL240 claude.html`). No page changes; gate-only, no regeneration; the tab-list form stays unscoreable, and MXFUN01 stays measured against a gold overview that says "need to add the phase template".
- **Option C — leave all five out of scoring** (as the CED revision briefs were under D10-6). No page change; a small labelled score change; the loop learns nothing from them until someone says which version went live.

**My recommendation is Option A for MXFUN01, BLL240, CEDT207 and CEDT301, and Option B for CEDK501 — with `BLL240 claude.html` removed from pairing in every case**, because for those four the KB, every earlier sibling and the template map all say "one tabbed page" (and MXFUN01's writer asked for a clickable intro page), while CEDK501's single file is an unfilled template and its seven lessons match the split pages exactly.



---

## Decision 7 — Renumbering an activity when the writer's number is repeated or belongs to another lesson (Needs Chris #7, 18 Sept)

**What the issue is.** Each activity box carries a number badge such as 5A or 5B. The KB and the gold number boxes consecutively on each page; PageForge keeps whatever number is attached to a box, word for word — so when a page ends up with two boxes numbered 5A, or a "2A" on the Lesson 4 page, PageForge ships it as is. Round r369 built a rule to make numbers consecutive, then switched it off: it changed 279 pages and scored 46 up, 77 down. The reason: the repeated number is often on a box **PageForge added itself** (e.g. a box made from a "go to your journal" instruction, or split off from the writer's activity), so renumbering "the second 5A" renames the wrong box. The fix the loop identified is **provenance** — recording where each box came from: the writer's typed `[Activity 4C]` keeps its number; only PageForge-made boxes take the next free letter. It is a policy question — should PageForge ever change a number the writer's text implies? — so it came to you.

**The real examples.**

*AGH1001, Lesson 5 — a PageForge-made box repeats 5A.*
- The writer typed — `01-Finalized_Modules_/Standard/AGH1001/AGH1001 Writers Template + Media List_parsed.txt` l.640 `[Activity: Embedded]`, l.692 `[Complete activity 5A and 5B in your Learners Journal]`
- The human built — `AGH1001.05.html` l.120 `<div class="activity interactive" number="5A">`, l.339 `<div class="activity dropbox" number="5B">`, l.342 `<p>Go to your learning journal and complete activities 5B and 5C.</p>`
- PageForge produces — `01-Claude_Modules_/Standard/AGH1001/AGH1001_5_0.html` l.96 `number="5A"`, l.177 `Writers Note: activity note: complete and in your learners journal`, l.178 `<div class="activity" number="5A">` (l.179–183: empty)
- What a learner sees: gold — 5A (a video task) then 5B with journal and dropbox buttons; PageForge — two boxes both labelled 5A, the second empty apart from a red note.

*AGH1007, Lesson 4 — the writer's number belongs to a different lesson.*
- The writer typed — `…/AGH1007/AGH1007 Writers Template + Media List_parsed.txt` l.487 (on the Lesson 4 page): `[Go to your Leaners Journal and complete activity 2A, 2B and 2C]`
- The human built — `AGH1007.04.html` l.47 `number="4A"`, l.209 `number="4B"`, l.298 `number="4C"`, l.302 `<p>Go to your journal and complete activity 4C, 4D and 4E.</p>`
- PageForge produces — `AGH1007_4_0.html` l.43 `number="4A"`, l.170 `number="4B"`, l.245 `Writers Note: activity note: go to your leaners journal and complete , and`, l.246 `<div class="activity" number="2A">`
- What a learner sees: gold — 4A, 4B, 4C with a journal button (the developer also rewrote the numbers in the sentence); PageForge — 4A, 4B, then a box labelled 2A after a red note whose numbers have been stripped.

*ENGJ102, Lesson 4 — a box PageForge split off collides with the writer's 4C.*
- The writer typed — `…/ENGJ102/ENGJ102 Writers Template + Media List_parsed.txt` l.437 `[Activity 4B] Contractions`, l.445–446 `[body] Match these contractions…` / `[drop and drag] …`, l.462 `[Activity 4C] ' … I like, but I don't like' poems`
- The human built — `ENGJ102_4.0.html` l.129 `number="4B"` (holding the drag-and-drop), l.177 `number="4C"` (the poem)
- PageForge produces — `ENGJ102_4_0.html` l.77 `number="4B"`, l.113 `number="4C"` (the drag-and-drop, split into its own box), l.158 `number="4C"` (the writer's poem)
- What a learner sees: gold — 4A, 4B, 4C; PageForge — 4A, 4B, 4C, 4C. (Under r369 the poem became 4D and stopped matching; under provenance the split box would become 4D and sit *before* 4C: 4A, 4B, 4D, 4C.)

**The numbers.** r369 changed 279 pages across 136 modules; on the 266 paired, 46 up / 77 down, net −106. Every variant tried was net-negative (smallest unused letter −106.4; look-ahead −66.6; majority digit only −5.9; letters only −59.0). The gold numbers Standard lesson pages `{page}{A, B, C…}` on 1,327 of 1,540 (0.86), Inquiry 47 of 50. The KB — `00_MASTER_INSTRUCTIONS/00E_CONSTRAINTS_2.md` constraint 62: *"the first interactive keeps the writer's activity number; each subsequent interactive becomes the next activity letter — and renumber the following activities accordingly"*; constraint 65 gives an MTK quiz box *"the next consecutive activity number — even where the writer assigned none"*; **no rule** for a writer's duplicate or foreign-lesson number. §1b: the KB covers only split boxes and quiz boxes; for everything else the module's gold (3) and group consensus (4, at 0.86) both say "consecutive" — the scorer disagrees only because PageForge's boxes don't always line up with the gold's. Today: `Emit_Templates.json` `page_number_normalise` is `"enabled": false`.

**The choice.**
- **Option A — keep the writer's numbers exactly (today).** Duplicates (5A / 5A) and foreign numbers (2A on Lesson 4) stay. Gate-neutral; no regeneration.
- **Option B — a provenance round**: PageForge marks the boxes it creates (journal-instruction, synthetic, split-off); only those take the next free letter; every number the writer typed stays. AGH1001 → 5A, 5B and AGH1007 → 4A, 4B, 4C (matching the gold); ENGJ102 → 4A, 4B, 4D, 4C (out of order, but the poem matches). One engine round, probed with the gate's own scorer *before* shipping, then a **full regeneration** (every box carries a number). Gate-moving, direction untested — it could still come out net-negative.
- **Option C — fully consecutive (switch r369 on).** Every page reads 4A, 4B, 4C, 4D as the KB and gold describe. Full regeneration; the gate is known to drop (−106, 77 pages down); numbers the writer's instructions refer to could change.

**My recommendation is Option B, shipping only if its pre-regeneration probe comes out net-positive (otherwise stay on A)**, because it fixes the clearest learner-facing errors — an empty duplicate 5A, a "2A" on Lesson 4 — without overriding any number the writer typed.

---

## Decision 8 — The 12 modules whose lesson menus are empty where the human repeated the module overview (Needs Chris #8, 19 Sept)

**What the issue is.** On a lesson page the menu normally holds that lesson's own learning intentions, from the writer's `[Lesson Overview]` block. In some modules the writer supplied no such block, and in 12 of them the human developer copied the *module overview's* whole menu (Knowledge / Practices or Understand / Know / Do, plus Learning Intentions) onto every lesson page. PageForge leaves those lesson menus empty. History: in June (round 110) the same thing in 3 modules (MXFL201, MXDB202, ANZH101) was handled with a hand-kept per-module list, because it's a per-module editorial choice (MXFL201 repeats; MXFL204, with indistinguishable input, doesn't). Session 24 found these 12 more and parked them as "a NEEDS-CHRIS list extension, never a rule". Then session 36 measured the wider pattern (126 pages / 30 modules) and **declared it a named KB override**: the KB says a lesson menu is *that lesson's* `[Lesson Overview]`, never the module overview — so PageForge's empty menu is KB-correct. The loop's latest position therefore conflicts with the round-110 list, and only you can say which way the house convention goes.

**The real examples.**

*SSOG103, lesson 2 "Ollie's Greeting Postcards".*
- The writer typed — `01-Finalized_Modules_/Standard/SSOG103/SSOG103 Writers Template_parsed.txt` lines 14–16 (module overview only): `🔴[RED TEXT] [Overview] [/RED TEXT]🔴` / `🔴[RED TEXT] [H3]  [/RED TEXT]🔴Knowledge`; lines 285–289, lesson 2 with no `[Lesson Overview]`: `[LESSON  2]` / `[Lesson content]` / `[H1] *Lesson* *2* *Ollie's* *Greeting Postcards*`
- The human built — `01-Finalized_Modules_/Standard/SSOG103/SSOG103_2.0.html` lines 22–28 (continuing to 73), the overview page's menu repeated word for word: `<div id="module-menu-content" class="moduleMenu">` … `<h3><span>Knowledge</span></h3>` / `<ul>` / `<li>People belong to groups (e.g. family, school class, team, culture).</li>` … then Practices, Learning Intentions / `<p>I am learning:</p>`, `How will I know I have learned it?` / `<p>I can:</p>`
- PageForge produces — `01-Claude_Modules_/Standard/SSOG103/SSOG103_2_0.html` lines 19–23: `<div id="module-menu-content" class="moduleMenu">` / `<div class="row">` / `<div class="col-md-8 col-12">` / `</div>` / `</div>`
- What a learner sees: gold — the menu button opens the module's full Knowledge / Practices / Learning Intentions summary; PageForge — it opens an empty panel.

*ANZH203, lesson 1 "First European Explorers".*
- The writer typed — `01-Finalized_Modules_/Standard/ANZH203/ANZH203 Writers Template + Media List_parsed.txt` line 17: `🔴[RED TEXT] [H2] [/RED TEXT]🔴 **Understand:**  Colonisation and settlement have been central to …`; lines 65–67, lesson 1 with no `[Lesson Overview]`: `[LESSON] Lesson 1` / `[H2]  *First European Explorers*`
- The human built — `01-Finalized_Modules_/Standard/ANZH203/ANZH203_1.0.html` lines 23–36: `<h3><span>Understand</span></h3>` / `<p> Colonisation and settlement have been central …` / `<h3><span>Know</span></h3>` … `<h3><span>Do</span></h3>` / `<li>Use appropriate and relevant sources.</li>` … then `<h4><span>Learning Intentions</span></h4>` (line 40)
- PageForge produces — `01-Claude_Modules_/Standard/ANZH203/ANZH203_1_0.html` lines 19–23: `<div id="module-menu-content" class="moduleMenu">` / `<div class="row">` / `<div class="col-md-8 col-12">` / `</div>`
- What a learner sees: gold — Understand / Know / Do on every lesson; PageForge — an empty panel.

*ANZH303 — the "tabbed but empty" variant.* `01-Claude_Modules_/Standard/ANZH303/ANZH303_2_0.html` builds `<li><a>Overview</a></li>` / `<li><a>Information</a></li>` tabs whose panes contain nothing — a learner sees two tab names and blank content.

**The numbers.** The 12: ANZH203, ANZH303, ANZH304, ENGJ101, HES1005, MXDB201, MXFL101, MXFL202, SSCI205, SSOG103, XLP05, XWHA01 (`CONVERTER_V2/outputs/_s24_menurepeat.log`) — re-checked today: all still empty on every lesson page, 73 PageForge lesson pages. The wider pattern: 126 pages / 30 modules (`_s36_r4_menurepeat.log`). Gold share: only 18 of 291 modules repeat the overview menu on at least half their lessons (0.06); no subject group reaches 0.60 except MXDB2 (2 of 2); and the Writers Template can't predict it — on pages with no menu source the gold repeats 53 times and writes its own menu 56 times (`_s36_r4_disc.log`). The KB — `01B_MODULE_MENUS_FOOTER.md` line 223: lesson pages use *"a simplified module menu"* built from the lesson's `[Lesson Overview]`; `10_CORPUS_VALIDATED_SCAFFOLDING.md` line 63: *"When the source has no such wording and no reference supplies it, you **cannot** invent it: build the empty `#module-menu-content` shell the skeleton requires and raise a visible red flag telling the designer the lesson-menu copy needs to be supplied."* **Gap found:** PageForge builds the empty shell but does *not* raise that red flag. §1b: level 1 (the KB) decides it — empty shell + red flag; the module's own gold (level 3) is outranked.

**The choice.**
- **Option A — extend the round-110 list** with these 12 (or all 30). Those lesson menus show the module overview's menu, matching the gold. Goes against the KB, contradicts the session-36 ruling, and is a hand-kept list every future module needs a human call on. Gate-moving (up); scoped regeneration (data only).
- **Option B — accept the empty menu as KB-correct and add the KB's missing red flag; close #8.** Empty lesson menus gain a visible red "lesson-menu copy needs to be supplied" note for the designer. Also say whether round 110's 3 existing exceptions stay (historic) or are retired for consistency (retiring moves those 3 modules down). Learners still see an empty panel until a designer fills it, but it is flagged, not silent. Red notes are excluded from the score, so gate-neutral; scoped regeneration.
- **Option C — make "repeat the module overview when a lesson has none" a rule for everyone.** Round 110 measured it fires correctly on only 30 % of pages (139 of 199 over-fire). Gate-moving (down); full regeneration. Not recommended.

**My recommendation is Option B** (keeping round 110's 3 as historic exceptions) because the KB already answers this exactly, the human repetition is a 6 %-of-modules habit no rule can predict, and the red flag turns a silent empty panel into a visible to-do at no cost to the score. If you *want* the overview repeated in particular modules as house style, A is safe only for exactly the modules you name.

---

## Decision 9 — The character picture beside a speech bubble (Needs Chris #9, 19 Sept)

**What the issue is.** A **speech bubble** is a cartoon-style text box that looks like a character is talking. In the finished modules (the gold), the developer usually puts a small picture of the character beside it; PageForge builds bubbles with no picture — 454 bubbles on 129 pages across 62 modules (`CONVERTER_V2/outputs/_s26_r397_entry.md` line 24). The loop may copy a layout most of a group shares, but it may not invent content, and the gold's pictures are stock photos and mascots the developer chose; so it recorded the picture as "the developer's asset choice, not in the WT" and stopped. **A correction found while preparing this report:** in real cases the writer often *did* ask for a picture, and PageForge dropped it or printed its title as text — so part of the 454 is a PageForge reading mistake under a rule the KB already has, not a policy gap. (Only the examples below were checked, not all 454.)

**The real examples.**

*OSOH201 — the writer gives a picture, PageForge drops it.*
- The writer typed — `01-Finalized_Modules_/Standard/OSOH201/OSOH201 Writers Template_parsed.txt` line 294: `│ 🔴[RED TEXT] [image]  [/RED TEXT]🔴https://www.istockphoto.com/photo/fun-cow-3d-illustration-gm864532370-143429689 ║ 🔴[RED TEXT] [speech bubble]  [/RED TEXT]🔴When I’m not using my superpowers…`
- The human built — `01-Finalized_Modules_/Standard/OSOH201/OSOH201_2.0.html` lines 47–51: `<img class="img-fluid" src="images/lesson 2.0/iStock-864532370.jpg" alt="Cowvin the cow">` … `<div class="bubble-basic bubble-right">`
- PageForge produces — `01-Claude_Modules_/Standard/OSOH201/OSOH201_2_0.html` lines 38–39: `<div class="col-12">` / `<div class="bubble-basic no-hover bubble-top"><p>When I’m not using my superpowers…` (the cow survives only in the acknowledgements, `OSOH201_0_0.html` line 183).
- What a learner sees: gold — a cow character "saying" the line; PageForge — a floating bubble with no speaker.

*TEDC402 — the writer gives an avatar link, PageForge prints its title as a sentence.*
- The writer typed — `01-Finalized_Modules_/Standard/TEDC402/TEDC402 Writers Template_parsed.txt` line 680: `[Image]  [/RED TEXT]🔴avatar Tina 🔴[RED TEXT] sitting on laptop [/RED TEXT]🔴 / __Young Beautiful Student Woman Set Stock Illustration…__ [LINK: https://www.istockphoto.com/vector/young-beautiful-student-woman-set-gm2235638824-650974740] / 🔴[RED TEXT] [speech bubble …] / Binary looks scary…`
- The human built — `01-Finalized_Modules_/Standard/TEDC402/TEDC402-3.0.html` lines 680–690: `alt="Tina — sitting on laptop"` … `src="images/iStock-2235638824-typing.jpg"` … `<div class="bubble-basic no-hover bubble-right">`
- PageForge produces — `01-Claude_Modules_/Standard/TEDC402/TEDC402_4_0.html` line 260: `<p>Young Beautiful Student Woman Set Stock Illustration - Download Image Now - Adult, Adults Only, Beautiful Woman - iStock</p>`, then (lines 267–269) a text-only bubble. (On the same page PageForge builds the picture correctly elsewhere, line 208.)
- What a learner sees: a stray line of iStock catalogue text, then a bubble with no Tina.

*OSBY301 — the writer only says "Person 1 / Person 2"; the gold invents the characters.*
- The writer typed — `01-Finalized_Modules_/Standard/OSBY301/OSBY301 Writers Template_parsed.txt` lines 155 / 161: `[speech bubbles- conversation layout] keep speech bubble static – 4 separate speech bubbles/people.` … `🔴[RED TEXT] Person 1 [/RED TEXT]🔴 / Be proactive! Use strong passwords and change them often.`
- The human built — `01-Finalized_Modules_/Standard/OSBY301/OSBY301-02.html` lines 43–48: `<img class="img-fluid bubble-img imageCentral" alt="" src="Character_assets/babyface.png" />` … `<p>Be proactive! Use strong passwords…`
- PageForge produces — `01-Claude_Modules_/Standard/OSBY301/OSBY301_2_0.html` lines 40–41: `<div class="col-12">` / `<div class="bubble-basic no-hover bubble-top"><p>Be proactive! Use strong passwords…`
- What a learner sees: gold — two cartoon kids talking; PageForge — bubbles with nobody speaking them. This is the only one of the three where the writer truly named no picture.

**The numbers.** 454 bubbles / 129 pages / 62 modules. The gold adds a picture at share 0.95 in Online Safety, 0.91 in TEDC, 0.65 in Inquiry Leaving-to-Learn; Standard Leaving-to-Learn is mostly text-only (0.68); English and Maths are split; no single column layout reaches 0.60. The KB — `htmlconvertor-kb/04_COMP_SEGMENTS_OVERLAYS/04C_COMP09_10_11_BUBBLES_DIAGRAMS_TOOLS.md` line 156: *"The positional class is determined by the layout in the Writers Template"*; lines 73–74 give the approved placeholder character, `<img class="img-fluid bubble-img" alt="" loading="lazy" src="https://placehold.co/200x200?text=Character">`; it never says to add a character the writer did not ask for. §1b: the KB (follow the writer's layout) already covers the cases where the writer placed a picture; where the writer gave none, the KB is silent, and group consensus (≥ 0.60) supports a picture column only in Online Safety and TEDC — but nothing says *which* picture.

**The choice.**
- **Option A — keep bubbles text-only.** No page changes; gate-neutral; no regeneration. Online Safety and TEDC stay unlike their finished pages, and the writers' dropped pictures stay dropped.
- **Option B — use the writer's own picture whenever the writer put one next to the bubble** (fixes OSOH201 and TEDC402; shows a placeholder carrying the real iStock number; removes the stray iStock-title line). Follows an existing KB rule, so the loop could arguably do it anyway. Gate-moving (up); scoped regeneration of the affected modules; one loop round, whose first step is counting how many of the 454 have a writer picture.
- **Option C — B, plus a grey "Character" placeholder and a red To Do note in Online Safety and TEDC only** where the writer named no picture; the designer picks the real character later, as they do now. Gate-moving (up); scoped regeneration. Risk: a grey box until replaced.

**My recommendation is Option B now, plus Option C for Online Safety and TEDC**, because B fixes a mistake under a rule the KB already has, and C copies what the finished pages do in the two groups where it is almost universal, without guessing the actual picture.



---

## Decision 10 — Seven modules have finished pages but no Writers Template (Needs Chris #10, 19 Sept intake)

**What the issue is.** The Writers Template (WT) is PageForge's only input. Seven modules — GER1003, GER1004, GER1005, GER1006, GER1007, SAM1005, SAM1006 — have a complete human-built module (the gold) but no Writers Template anywhere in the project, so there is nothing to convert, no PageForge output, and nothing to compare. The loop cannot invent a writer's document; someone has to find it.

**The real examples.**
- *GER1003* — `01-Finalized_Modules_/Standard/GER1003/` holds 11 files, all HTML (`GER1003-Glossary.html`, `GER1003_0_0.html` … `GER1003_9_0.html`), no `.docx`, no `_parsed.txt`; no `01-Claude_Modules_/*/GER1003` folder. The raw download `04-Newly-Developed-Modules-Raw-Info/DriveDownload/German/Modules/Level 1 - Completed/GER1003/` has 17 working files (e.g. `GER1003_3A_superlative_drag_drop.docx`, `GER1003_all_vocab_list.docx`) — pieces, not a template. Compare its sibling GER1002, whose gold folder does have `GER1002 Writers Template + Media List.docx` and a PageForge folder.
- *SAM1005* — `01-Finalized_Modules_/Standard/SAM1005/` holds 15 HTML pages and no template; the only source files are a teacher-notes document (`…/Samoan/Kaimahi Notes/SAM1005 Kaimahi Guide Notes Template SAM1005.docx`) and `Old Content Review SAM1005 - edit sheet.xlsx`. SAM1006 is the same (18 pages + a Kaimahi notes doc).
- *GER1005 / GER1007* — gold folders of 13 and 10 pages; no raw folder at all (the German download holds only GER1001–1004, 1006, 1008); no PageForge folder.
- What a learner sees: the finished modules are live and fine; this only affects whether PageForge can be tested on them.

**The numbers.** 7 modules, 94 gold pages, 0 PageForge pages — five of the six German and both Samoan NCEA-level modules. Scores unaffected (the gates skip them). The KB and §1b have nothing to say — there is no source document to apply a rule to. The 19 Sept intake (`LOOP_INTAKE__2026-09-19_98_Modules.md:208`) records it as a source-collection gap, not a converter fault.

**The choice.**
- **Option A — collect the templates** from the German / Samoan writers or the curriculum team. Once filed, the loop converts and scores them in its standing new-module intake. Adds ≈ 94 comparison pages; gate-moving only in the sense that new pages join the score (named when they do).
- **Option B — close them as "gold only"**: keep the gold as reference for sibling modules, stop tracking the item. No cost; you lose 7 test modules, including the only Samoan NCEA ones.
- **Option C — rebuild templates backwards from the gold.** Not recommended: the gold would be both the question and the answer, so the score would mean nothing.

**My recommendation is Option A with a deadline, falling back to B** because the Samoan notes and GER1003's working files suggest the material existed — but if these modules were revised in place and never templated, closing them costs less than keeping them open.



---

## Decision 11 — XOTPB08's pasted picture (Needs Chris #11, 19 Sept intake)

**What the issue is.** XOTPB08, *Hannah Makes a Pavlova*, is one module in the XOTP reader family. For two drag-and-drop activities (the learner drags words or sentences into place) the writer pasted a *screenshot* of the activity into the Word document instead of typing its content. A converter can only read typed text: 8 of the activity's 12 items (the six matching sentences plus the words "beater" and "oven") exist only as a picture (`00-NEW_NEW_NEW/_SPEC__XOTP_Activity_Table_Template.md` lines 150–155). The loop cannot make content up. A finished human version already exists; this affects only PageForge's version.

**The real examples** (all in XOTPB08, `01-Finalized_Modules_/Standard/XOTPB08/` and `01-Claude_Modules_/Standard/XOTPB08/`)

*Activity 1, "Fill the gaps".*
- The writer typed — `XOTPB08 Writers Template_parsed.txt` line 18: `**Fill the gaps** / Instruction: Use the words in the box to fill the gaps. Read the sentences. / 🔴[RED TEXT] CS: Create a drag and drop activity: [/RED TEXT]🔴 / [IMAGE: image2.png]`
- The human built — `XOTPB08_1_0.html` lines 134–157: `<p><span class="drop" option="1"></span> is the <span class="drop" option="2"></span>mixture.</p>` with drag words `Here`, `pavlova`, `mixture`, `oven`, `Hannah`, `beater`.
- PageForge produces — `XOTPB08_1_0.html` lines 76–78: `<h3>Fill the gaps</h3>` … `<p class="cv2-note" …>Writers Note: Create a drag and drop activity:</p>`
- What a learner sees: gold — a working fill-the-gap game; PageForge — the instruction and a red developer note.

*Activity 1B, matching pictures to sentences.*
- The writer typed — line 19: `Instruction: Match the six pictures and sentences from the story and put them in the correct order. / __Sequence__ [LINK: https://docs.google.com/document/d/1kzQt60…] / [IMAGE: image3.png]`
- The human built — lines 192–211: `<p>Here is the vanilla essence and the castor sugar and the eggs.</p>` … `<p>Here is the pavlova ready to eat. Yum!</p>`
- PageForge produces — lines 93–95: `⚙ INTERACTIVE (un-built) #3: dragAndDrop … see XOTPB08_interactives.txt`, whose only content is `<p>Sequence</p>`.
- What a learner sees: gold — six story pictures to match; PageForge — a hand-off box for the developer containing the word "Sequence".

*Activity 1C, "What's next?"* — writer line 20 `[IMAGE: image1.png] / (Please position the think bubble above the cake photo at left)`; gold lines 228–238 a thought bubble over `images/Pavlova.png`; PageForge lines 108–110 the heading and a red "Writers Note". A learner sees text and a note, no photo.

**The numbers.** One module, two pages; 8 of 12 items only in the pasted image — XOTPB08's text coverage is 33 %, against 100 % for seven sibling XOTP modules. The KB (`01_PIPELINE_EXTRACTION_TAGS/01C_CONTENT_SOURCE_FORMATS.md` line 330): where content is missing, *"raise a VISIBLE red flag … for the developer to complete — not a hidden HTML comment"* — PageForge already does this. §1b: nothing applies; no rule can recover text that exists only as a picture.

**The choice.**
- **Option A — ask the writer to type the 8 items into the Word document.** PageForge then builds both activities like its siblings; one module rebuilt; tiny gate move (2 pages). Cost: one message to the author.
- **Option B — accept the gap**: keep the red note and hand-off box, add a clearer "To Do: content is only in a pasted picture". No regeneration needed.
- **Option C — take XOTPB08 out of PageForge's test set.**

**My recommendation is Option B** because it is one module, the finished page already exists, and PageForge already flags the gap visibly as the KB asks; A is worth doing only if this module will ever be rebuilt from its Word document.



---

## Decision 12 — Which subject label the language modules sit under (Needs Chris #12, 20 Sept)

**What the issue is.** PageForge groups modules by a **subject label** (e.g. "NCEA1", "1-10 Languages"); the label decides which modules count as "the same subject" when the loop looks for patterns, and it is what the HTML Generator's reference-module Subject filter shows a designer. Thirty module-code **prefixes** (the letters at the start of a code, like `GER` or `CHFUN`) had no folder to take a label from, so round 408 proposed labels in `pageforge-site/converter-v2/data/Subject_Prefix_Map.json`, marked "PROPOSED — awaiting Chris's approval". The languages are the uncertain ones. This is a curriculum judgement, not something the pages can settle, and the loop may not build any rule on these labels until you confirm them.

**The real examples** (all from `Subject_Prefix_Map.json`)
- *NCEA-level language courses → NCEA1* — lines 33–37: `"CHI": "NCEA1"`, `"GER": "NCEA1"`, `"JPN": "NCEA1"`, `"SAM": "NCEA1"`, `"SPA": "NCEA1"`. Example: `01-Finalized_Modules_/Standard/GER1002/GER1002_0_0.html:2` is `<html … template="NCEA" …>`, titled "Where I live / Ko Taku ao"; `00_Server_Module_Map.md:548` files GER1000 under `## NCEA1`. In practice these group with History, Geography and other NCEA Level 1 courses.
- *Beginner / foundation language modules → 1-10 Languages* — lines 40–46: `"CHFUN"`, `"FRFUN"`, `"JPFUN"`, `"FRNO"`, `"GENO"`, `"CHWHA"`, `"GEWHA"` all `"1-10 Languages"`. Example: `01-Finalized_Modules_/Standard/GENO901/GENO901_0_0.html:2` is `template="combo"`, "Hallo, Deutsch! / Hello, German!". In practice German beginner (GENO901) and German NCEA (GER1002) land in different groups.
- *The welcome modules are the least certain* — line 13 of the file: *"CHWHA / GEWHA proposed with the Phase 1-4 language families ('1-10 Languages'); alternative: with their NCEA1 course prefixes."* Example: `01-Finalized_Modules_/Inquiry/GEWHA/GEWHA_0_0.html` — an Inquiry-template welcome module ("Begrüßung und Vorstellung") into a course that sits under NCEA1.

**The numbers.** 12 prefixes: the NCEA1 group has 13 gold modules (CHI 3, GER 6, JPN 1, SAM 2, SPA 1) and 6 PageForge modules; the 1-10 Languages group 16 gold / 16 PageForge. 0 pages change today — the label is "output-inert". The KB's Languages family (§14.4) treats CHI, FRE, SAM, GER, JAP, SPA as one cohort — but for fonts and characters, not page structure. Evidence for the split: the server folders and the gold's own `template="NCEA"` vs `template="combo"` split. §1b does not strictly apply (a grouping key is not a page rule).

**The choice.**
- **Option A — confirm the split as proposed** (NCEA-level languages under NCEA1; beginner and welcome modules under 1-10 Languages). Follows the server folders and the gold's template split. No page change, gate-neutral, no regeneration; unlocks future subject-keyed rules.
- **Option B — one Languages label for all twelve** (optionally a new plain "Languages"). Follows the KB cohort. A one-line data edit, no page change — but mixes NCEA-template and combo-template modules whose pages are built differently.
- **Option C — the split, but CHWHA / GEWHA move to NCEA1** with their courses. Same cost as A.

**My recommendation is Option A** because the server filing and the gold's own template split both agree with it, it changes nothing today, and the KB's single cohort is about fonts, not page structure, so it does not conflict.

---

## Decision 14 — The XOTP reader book: story pages, matching pictures, credits (Needs Chris #14, 21 Sept)

**What the issue is.** The 12 XOTP modules are early-reader lessons built around a story book (the "reader"). Their finished pages rely on three things that are in none of the Word documents: the book's page images, shown in a **carousel** (a click-through slideshow); the pictures for the picture-and-sentence matching activities; and the **acknowledgements** (credit lines for the story's author and illustrator). Normally a **Media List** (a list of every image and its source) supplies these; none of the 12 has one — the documents only link to a Google Drive folder PageForge cannot open. Round 425's "text adapter" now converts all 12 modules' *text* (their average score against the gold rose from 58.76 % to 60.28 %), but it cannot conjure up the book.

**The real examples.**

*XOTPB09 — the story slideshow.*
- The writer typed — `01-Finalized_Modules_/Standard/XOTPB09/XOTPB09 Writers Template_parsed.txt` line 16: `│ Online book ║ link to reader here / __TEXT__ [LINK: https://drive.google.com/drive/u/0/folders/1AyBommTY3LM2uiefgulhPZORzrAhG00J] / CS: Please change ‘crunch’ to crunchy…`
- The human built — `XOTPB09_1_0.html` lines 61–64: `<div class="row carousel">` … `<img … src="images/Where do my Beans Come from_01.png" alt="Page 1">` (15 page images).
- PageForge produces — `01-Claude_Modules_/Standard/XOTPB09/XOTPB09_1_0.html` lines 47–51: `⚙ INTERACTIVE (un-built) #1: carousel …` / `<p>TEXT</p>` / `<p>CS: Please change ‘crunch’ to crunchy…</p>`
- What a learner sees: gold — the whole storybook to click through; PageForge — a developer hand-off box with the word "TEXT".

*XOTPB09 — the story credits.*
- The writer typed — no credit line anywhere.
- The human built — `XOTPB09_2_0.html` lines 180–183: `<p>Story: Where do my Beans Come from? by Anne Russell and Rosemary Emery, © Off The Page. Used with permission. </p>`
- PageForge produces — `XOTPB09_1_0.html` lines 134–141: `<h4>Acknowledgements</h4>` … `<!-- Lesson 1.0 -->` … `<!-- Lesson 2.0 -->` — empty, with no visible red flag.
- What a learner sees: gold — the author and copyright credit; PageForge — an empty Acknowledgements panel.

*XOTPG04 — the other half of the family.*
- The writer typed — `XOTPG04 Writers Template_parsed.txt` line 16: `│ Online book ║ **Insert as per Feeding Time at the Pet Shop (link below)** / __My Drum Kit__ [LINK: https://drive.google.com/drive/folders/1EEuU40…]`
- The human built — `XOTPG04_1_0.html` lines 71–74: `<div class="row carousel">` … `src="images/My Drum Kit_Page_01.jpg"`
- PageForge produces — `XOTPG04_1_0.html` lines 61–64: `⚙ INTERACTIVE (un-built) #1: carousel …` / `<p><b>Insert as per Feeding Time at the Pet Shop (link below)</b></p>` / `<p>My Drum Kit</p>`
- What a learner sees: as above — a hand-off box instead of the book.

**The numbers.** 12 modules, 24 pages; no Media List in any of the 12 folders (checked). The KB: `00_MASTER_INSTRUCTIONS/00A_CONTROL_CORE.md` line 66 *"If no media list is provided, proceed normally"*; `05_COMP_LANGUAGE_MEDIA_LAYOUT/05C_COMP14_ACKNOWLEDGEMENTS.md` line 139 *"Where a title or byline is unavailable, raise a VISIBLE red flag for the developer to complete — not a hidden HTML comment"* — PageForge's empty block with hidden comments does not meet that yet (a small fix under an existing rule). The gold: all 12 have the slideshow, the matching pictures and the credits, in one two-line credit pattern (story by …, © Off The Page; illustrations © Te Aho o Te Kura Pounamu). §1b: follow the KB — placeholders plus visible flags; no rule can supply the images.

**The choice.**
- **Option A — supply the reader material** (one Media List for the family, or the Drive page images plus each story's author and illustrator). The loop then builds the carousels, matching activities and credits; the 12 modules rebuilt; gate-moving (up). Cost: someone gathers 12 sets of images and 12 credit lines.
- **Option B — flagged placeholders**: keep the carousel hand-off box; give the acknowledgements a visible red "credit needed" flag (as the KB requires), optionally with the family's standard illustration line. Barely moves the gates; the 12 modules rebuilt; the designer adds the book by hand, as today.
- **Option C — leave the family text-only as it is now.**

**My recommendation is Option B now, and Option A only if these modules will be re-issued**, because B is what the KB already prescribes, costs one small round, and makes the gap obvious to the designer — the book images are artwork a person must place anyway.



---

## Decision 15 — The XOTPB Overview text lives in a Google Doc (Needs Chris #15, 21 Sept)

**What the issue is.** The six B-series reader modules (XOTPB08–13) have an **Overview** panel in their module menu (what the learner will understand, know and do). The writer didn't type this text into the Word document — they linked to a shared Google Doc. PageForge can't open external links, so it shows the link's label as if it were content. The six G/O-series modules typed their overview in, and PageForge converts those correctly.

**The real examples.**

*XOTPB09.*
- The writer typed — `01-Finalized_Modules_/Standard/XOTPB09/XOTPB09 Writers Template_parsed.txt` line 14: `│  Overview / (dropdown at top right) ║ In this module, ākonga will: / __Overview Set 2-Emergent__ [LINK: https://docs.google.com/document/d/1z7AC1k0GDvBP3wqfCtKRnHO3Y3hZBODTJoKKk_WeCIk/edit]`
- The human built — `XOTPB09_1_0.html` lines 27–31: `<p>This resource provides a reading text and activities for beginning readers (of all ages) working at early Phase One…</p>` / `<h4><span>Understand</span></h4>` / `<p>Communication helps us to share our ideas…</p>`, then a six-item "I can:" list (lines 33–41).
- PageForge produces — `01-Claude_Modules_/Standard/XOTPB09/XOTPB09_1_0.html` lines 24–26: `<h3><span>Overview</span></h3>` / `<p>In this module, ākonga will:</p>` / `<p>Overview Set 2-Emergent</p>`
- What a learner sees: gold — a full overview with goals; PageForge — "In this module, ākonga will:" followed by the meaningless line "Overview Set 2-Emergent".

*XOTPB08* — the same link on WT line 14; the gold overview has the same wording as XOTPB09's (only a line break differs).

*For contrast, XOTPG04, where the writer typed the text* — WT line 14: `This resource provides a reading text and activities for beginning readers (of all ages) working at early phase one…`; PageForge `01-Claude_Modules_/Standard/XOTPG04/XOTPG04_1_0.html` lines 25–38 builds the full Overview / Understand / Know / Do sections with the "I can:" list, matching the gold.

**The numbers.** 6 modules, one overview panel each; all six contain the same Google Doc link, and all six gold overviews use the same wording — so one piece of text serves all six. The KB has no rule about external documents; the general missing-content rule is the visible red flag (`01C_CONTENT_SOURCE_FORMATS.md` line 330). §1b: nothing can supply this — it is content, not layout.

**The choice.**
- **Option A — supply the Google Doc text once** (paste it into the six Word documents, or give it to the loop as one shared family text). All 6 overviews match the gold; small gate rise; the 6 modules rebuilt. Cost: one copy-paste.
- **Option B — a red "To Do: paste the overview from the linked Google Doc" note** in place of "Overview Set 2-Emergent". Barely moves the gates; the 6 modules rebuilt.
- **Option C — reuse the G-series wording.** Not advised: the first paragraphs match, but the B "I can" list has different goals ("match sentences and pictures", "recall some key information…"), so learners would see the wrong goals.

**My recommendation is Option A, with B as the stop-gap until the text arrives**, because a single paste fixes all six modules exactly, and until then the note stops learners seeing a meaningless link label.

---

## The questions — one per decision, each answerable in a sentence

1. **KB wording:** Will you run the Admin-Mode KB session for the five wording fixes and four status lines yourself, or should the loop draft it for your approval?
2. **Comparison tables:** Should comparison tables stay bordered like every other table (A), lose their borders and get equal columns as the KB says (B), or keep borders *and* get equal columns (C)?
3. **Success label:** Should the lesson-menu success label keep the writer's own wording (A), be forced to the KB's year-level wording (B), or follow a per-module list you provide (C)?
4. **Quiz widgets:** Should the loop build the quiz widgets itself (multiple choice, type-the-answer, dropdown, radio, reorder, selection box) — only where the writer marked the right answer, leaving the hand-off box (now carrying the answer key) everywhere else?
5. **Journal button:** When a writer tags a journal button in their own words, should PageForge rewrite it to the standard "Go to your journal" form — and never add one the writer didn't ask for?
6. **Two versions:** For MXFUN01, BLL240, CEDT207 and CEDT301, did students actually get the one-page tabbed version — and for CEDK501, was it the separate pages?
7. **Activity numbers:** When PageForge adds an activity box of its own, may that box take the next free letter (only if a trial shows the score improves), leaving every number the writer typed alone?
8. **Empty lesson menus:** For lessons whose writer gave no lesson overview, should PageForge leave the menu empty with a red "please supply" flag as the KB says (B), or copy the module overview's menu for the 12 named modules as the humans did (A)?
9. **Speech-bubble pictures:** Beyond using the writer's own picture where one was given, should PageForge add a grey "Character" placeholder beside speech bubbles in Online Safety and TEDC only, or leave bubbles with no picture text-only?
10. **Missing templates:** Can someone find the Writers Templates for GER1003–1007, SAM1005 and SAM1006 — or should these seven be treated as gold-only and closed?
11. **XOTPB08:** Is XOTPB08 ever likely to be rebuilt from its Word document — if not, can we accept PageForge's flagged gap and close the item?
12. **Language labels:** Should the NCEA-level language courses (CHI, GER, JPN, SAM, SPA) stay under "NCEA1", separate from the beginner and welcome language modules under "1-10 Languages" — or should all twelve share one Languages label?
14. **XOTP reader book:** Will you supply the book images and author credits for the 12 XOTP modules, or should PageForge leave clearly flagged placeholders for the designer?
15. **XOTPB Overview:** Can you paste the text of the "Overview Set 2-Emergent" Google Doc once (for all six XOTPB modules), or should PageForge show a To Do placeholder instead?

*Prepared 23 September 2026 by the `/loop-decisions` session. Read-only: no converter code, data or module was changed to produce it. Answers are recorded in `LOOP_STATE.md` under "Decisions from Chris" as they arrive, and the next `/loop-start` actions them.*
