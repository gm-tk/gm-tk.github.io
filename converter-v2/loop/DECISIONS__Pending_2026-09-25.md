# PageForge autonomous loop — the decisions waiting on Chris (25 September 2026)

> Written by the `/loop-decisions` session of 25 Sept 2026 (session 48, Opus 5.5). Read-only: no code, data or module was
> changed. **Chris reads the visual version, `EXPLAINER__Pending_Decisions_2026-09-25.html`**. This markdown is the
> evidence record it is built from (D15-S1). Every quote below was taken from the real files with `sed -n` line ranges
> and re-checked by hand. Engine at the time: r500 (build 260620.63). Match score (skeleton mean): 55.4588 % over 2,491
> page pairs.

## The words used below (each defined once)

- **Writers Template (WT).** The Word document the subject writer fills in, with red `[tags]` saying what each piece is.
  PageForge reads the parsed text copy, `<CODE> Writers Template…_parsed.txt`.
- **The gold.** The finished module a human developer built by hand (`01-Finalized_Modules_/`). It is the target, but it
  spans years and contains one-offs.
- **PageForge / Claude's output.** What the converter builds automatically from the same WT (`01-Claude_Modules_/`).
- **Knowledge base (KB).** The written rulebook for converting modules (`00-Other-TK-Resources/htmlconvertor-kb/`, HEAD
  910a9cb). The loop may read it but never edits it (D13-1: Chris runs the rulebook sessions).
- **Rule order (§1b).** When sources disagree, the loop follows (1) the KB, (2) the earlier module of the same series,
  (3) this module's own gold, (4) what at least 60 % of similar modules do (`LOOP__Autonomous_Rounds.md` l.159–197).
- **Match score.** How closely PageForge's page structure matches its paired gold page. "Gate-moving" = the change
  raises or lowers it; "gate-neutral" = it doesn't.
- **Rebuild (regeneration).** Re-making the output pages; "scoped" = only the modules a change touches.
- **Hand-off box.** The rainbow-bordered placeholder PageForge leaves where it could not build a widget, holding the
  writer's text for a developer.
- **Labelled exception (named override).** A page where PageForge deliberately follows a rule instead of the human's
  page. Its lower score is expected and the page is listed by name.

## At a glance

| # | Raised | The question | Size | My recommendation |
|---|---|---|---|---|
| 17 | 23 Sept | CEDT301: one tabbed page or separate pages? | 1 module · 6 scored pages | **A**, one tabbed page like every other CEDT module |
| 18 | 24 Sept | What an `[RHS alert]` tag becomes | 176 tags · 73 modules | **B**, the right-hand side column (Standard + Fundamentals) |
| 19 | 24 Sept | Quiz answers the writer highlighted without saying so | ≈ 190 hand-off boxes (the biggest) | **B**, trust yellow ✅ ticks with strict guards; multiple choice first |
| 22 | 24 Sept | BLL overview: Knowledge / Practices in their own tabs? | 19 modules | **A**, their own tabs; the empty Information tab removed |
| 23 | 25 Sept | The Maths series' lesson menu without the extra wrapper | 91 pages · 13 modules | **B**, a named Maths-series convention |

Two older items are still open, but as **actions, not decisions**. They are not repeated here. **#1**: Chris's own
rulebook (Admin-Mode) session. It is still owed: `14A_…:54` still says to add stickyNav, and `05D_…:239` still says
`tableFixed` WITHOUT `table-bordered`. **#10**: the seven modules with no Writers Template (GER1003–1007, SAM1005,
SAM1006). Still no Claude folder for any of them.

## Corrections to the loop's own notes (found while preparing this)

1. **#19: the "typing ≈ 77, mostly Maths" group is neither mostly typing nor Maths.** Re-counted from
   `CONVERTER_V2/outputs/_s40_typing.jsonl`: 78 bundles / 12 modules. Of those, 50 are French / Chinese / Japanese
   (FRNO902 29, FRNO901 8, CHFUN05 5, JPFUN01 5, JPN1004 2, CHFUN07 1) and 27 are Pathways (PWY1001/1002/1007/1008/1009).
   Maths accounts for **1** (MXEO301, where the green is emphasis, not an answer). Most of them are not typing quizzes at all: the
   writer's tags include drag and drop ×16, reorder ×10, multichoice ×10, dropdown ×9 and radio ×6. **Cause:**
   `CONVERTER_V2/data/Tag_Lexicon.json` makes "autocheck" an alias of "typing quiz" (l.20–27). So a nested
   `[radioquiz [autocheck]]` (PWY1008 WT l.262) is labelled typing (`01-Claude_Modules_/Standard/PWY1008/PWY1008_1_3_0.html:153`
   "⚙ INTERACTIVE (un-built) #9: typing"), while the gold is a `radioQuiz` (`PWY1008_1_3.html:155`). About 107 of the
   270 typing hand-offs carry another widget's name. **This is a recognition fault the loop can fix under its own
   authority** (KB rule 14: the writer's tag decides the component). It is not a decision for Chris.
2. **#19: green answers leave no trace.** Round 448 turns only YELLOW highlights into ✅ ticks (`BUILD_CHANGELOG.md`
   l.1034, l.1040: "Green is left unticked"). Green highlighter and green text show no mark in the `_parsed.txt` or in
   the hand-off box. That is roughly half of the ≈ 190 (the whole "typing" group, most radio and reorder).
3. **#19: two guards the loop's note didn't have.** OSAI101 is not an unannounced trap: the writer wrote "answer options in
   green – no correct answers" (WT l.289). Its green is also ONE run over the whole option list, so a guard must count marked
   OPTIONS, not marked runs. And ≈ 10 of the 23 multiple-choice line bundles are D2L quiz questions under the writer's
   `[Button] Go to quiz` (TEFUN01 ×4, TEFUN03 ×1, TEFUN04 ×4, ENGR202 ×1). The human deliberately built no on-page quiz
   there, only a quiz-link button (gold `TEFUN01.html:235`, `ENGR202_5.0.html:229`). ENGR202 5B has exactly one ✅ per
   question, so it would pass a one-per-question guard.
4. **#18: the 24 Sept measurement miscounted.** `_rhsalert_measure.py` l.41 counts only `col-md-3` / `col-md-4` as a side
   column, but the humans also write a plain `col-4` (r333 itself counted both). The seven "speech bubbles" are not bubbles:
   six are TEDC402 tags whose text was the table marker `┌─── TABLE ───`, and one is an `alert solid` box. Corrected:
   the side column holds **92 of 139 = 0.66** (Standard **0.70**, Fundamentals 0.66, Inquiry 0.30), not 0.58 / 0.62. PageForge
   matches the human on **64**, not 55. Re-running the unchanged script on today's pages gives a byte-identical log,
   so the error is in the script, not the date.
5. **#18: some right-hand boxes vanish.** In XGF9001 (9 tags) and SCBI301, PageForge drops the writer's box entirely,
   with no red flag. XGF9001's `[Alert RHS] [H3] Key questions` becomes a plain heading and list in the main column
   (`XGF9001_2_0.html:39–46`). That is a bug to fix whatever is decided.
6. **#17: the scores are out of date.** The split build scores **61.5 %** today (r500, 6 pages: 34.8 / 58.2 / 64.0 /
   64.3 / 67.2 / 80.8), not 57.7 % (which included a 7.4 % mis-pair r440 removed) or 67.7 %. The human's
   separate-pages version is the rougher copy (see #17).
7. **#22: one module missed, and an always-empty tab.** BLL243 has its own Knowledge and Practices tabs and was left
   out: own-tab Knowledge golds are 11, not "10–11". BLL265 is a hybrid (Knowledge in its own tab, Practices in
   "Information"). In BLL265 PageForge puts the lists in the page body, not the menu (a separate fault). PageForge's
   "Information" tab is an **empty pane in all 19**, which matches no human page and breaks the KB's "omit an empty
   Information tab" rule (01B l.117).
8. **#23: 13 modules, not 12; empty menus.** The count "12m" (`_s45_r4_menuwrap.log` l.5) included MXFL204 and left out
   MXEX201/202. PageForge's row/column shell is **empty on 37 of its 81 row-form pages**, and on 10 MXEX201/202 pages it
   builds no menu at all. Menu text ships on 44. The "0.92" is 1 minus the bare share, and it counts the `div.item` form as row.
   The true row share is 0.86 corpus-wide, or ≈ 0.95 outside 1-10 Mathematics.

---

## Decision 17 — CEDT301: one tabbed page or separate pages? (Needs Chris #17, 23 Sept)

**What the issue is.** CEDT301 "My place and me" has two complete human versions: one page with seven clickable
tabs (`CEDT301 My place and me.html`), and eight separate pages (`CEDT301_0.0` … `_7.0`). On 23 Sept you decided (D13-6)
that the four modules with two versions (MXFUN01, BLL240, CEDT207, CEDT301) should be built as one tabbed page. A
caveat was recorded with that answer (`LOOP_STATE_ARCHIVE.md` l.4267): *"If the single-file build scores clearly worse
there, record it rather than force it."* Built as one page, CEDT301 scored 45.0 % against the one-page human version.
The separate-pages build scores about 62 % against the separate human pages. So the loop kept it split and stopped to
ask, as the caveat told it to.

**The real example: the start of the module (the introduction).**

- **The writer typed.** `01-Finalized_Modules_/Inquiry/CEDT301/CEDT301 Writers Template + Media List_parsed.txt`
  l.61–79 and l.81–97:
  ```
  Side Tabs:
  Tab 1 – Introduction
  Tab 2 – Mauri
  …
  Tab 8 – Map it out
  Tab 9 – Digital Collage
  🔴[RED TEXT] [Page 1] [/RED TEXT]🔴
  🔴[RED TEXT] [H2]  [/RED TEXT]🔴Introduction
  🔴[RED TEXT] [Important]  [/RED TEXT]🔴
  E kore au e ngaro; he kākano i ruia mai i Rangiātea.
  ```
  *What it says:* nine side tabs, then six marked pages.
- **The human built (one page).** `01-Finalized_Modules_/Inquiry/CEDT301/CEDT301 My place and me.html` l.59–82:
  ```html
  <div class="crumbs">
    <div crumb="0" class="showing"><p>Intro</p></div>
    <div crumb="1"><p>Mauri</p></div>
    … <div crumb="6"><p>Collage</p></div>
  </div>
  <div class="inquiryPanel showing" rel="0">
    … <div class="whakatauki"><p>E kore au e ngaro; he kākano i ruia mai i rangiātea. </p> …
  ```
  *A learner sees:* one page with seven tabs across the top. The Intro tab shows the proverb, three paragraphs and a video.
- **The human built (separate pages).** `CEDT301_0.0.html` l.60–75: the same proverb, paragraphs and video on the landing page.
  *A learner sees:* a landing page, then "next" to separate Mauri / Mana / … pages.
- **PageForge makes today.** `01-Claude_Modules_/Inquiry/CEDT301/CEDT301_0_0.html` l.60–72:
  ```html
  <p>Side Tabs:</p>
  <p>Tab 1 – Introduction</p>
  … <p>Tab 9 – Digital Collage</p>
  ```
  then `CEDT301_1_0.html` l.12–27 (a separate "Introduction" page, the proverb in an `alert solid` box).
  *A learner sees:* an overview listing nine "Tab N" lines that do nothing, then seven separate pages.

**Which human version is the finished one.** The separate-pages set looks like the rougher copy. It is Standard-style
(`<body class="container-fluid">`, no crumbs). It has no 7.0 page: `CEDT301_7.0.html` l.7 is titled "8.0". Pages 4.0–7.0
carry a hidden menu from another art module ("patterns and symbols in art … creating a visual pepeha"). The one-page
version is Inquiry-style (`inquiry container-fluid`, crumbs, `footer-nav inquiry-nav`), and both hold the same content
(133 vs 130 paragraphs, 18 videos, 21 images each).

**The numbers.**
- `CONVERTER_V2/outputs/_r440_prescore.log` l.7: `CEDT301  ON CEDT301_0_0.html <-> CEDT301 My place and me.html  scaffold 45.0`.
- `_r440_decompose.log` l.11–13: split `57.7 -> 62.2` (the 7.4 mis-pair became 35.0). Today (r500): 61.5 % over 6 pairs.
- "6 pairs": six of PageForge's seven split pages are scored. The Introduction page `_1_0` and the gold `_5.0` / `_7.0` are unpaired.
- The siblings: every other CEDT gold is one tabbed page (CEDT101, 102, 104, 201–204, 207, 208, 404). CEDT207 and MXFUN01
  also scored lower as one page (36.7 → 30.9 and 36.6 → 5.5, `_r440_decompose.log` l.2, l.8) and were switched anyway.
- Effect on the overall score if switched: 6 pairs become 1, so the mean moves by about −0.02 points (a labelled population change).

**What the KB says.** `06_TEMPLATE_RECOGNITION.md` l.63: Inquiry navigation is `div.crumbs → div.inquiryPanel`. l.173 (§3.4):
"Breadcrumb/tab-based — `div.crumbs` containing crumb tabs, then `div.inquiryPanel[rel]` content panels." There is no
CEDT-specific rule.

**What the rule order says.** (1) The KB describes Inquiry modules as one tabbed page. (2) Every earlier sibling in the
series is one tabbed page. Both point to one page. Only the D13-6 caveat stopped the loop.

**The choice.**
- **Option A: one tabbed page, like every other CEDT module.** Switch the CEDT3 row to single-file
  (`pageforge-site/converter-v2/data/Style_Anchor_Registry.json` l.2722 `"page_model": "multi-file"`) and score against
  the one-page gold (`compare_gold_pages.txt` l.23 `exclude` → `only`). Learners get seven real tabs instead of nine dead
  "Tab N" lines. *Cost:* this module's score drops (≈ 45 % vs 61.5 %), about −0.02 points overall, labelled. **Gate-moving;
  1 module regenerated** (the CEDT3 row also covers CEDT302 / 303, which have no gold or build yet). The single-file
  build needs re-probing first (the r440 probe output is gone).
- **Option B: keep separate pages (today).** Nothing changes. The nine "Tab N" lines stay, and the module stays unlike every
  other CEDT module. Gate-neutral, no rebuild.
- **Option C: leave CEDT301 out of scoring** until someone confirms what went live. Score changes slightly, no rebuild.

**My recommendation is A** because the rulebook, all nine earlier CEDT modules and the human's more finished version
all say one tabbed page, and it is what you chose for the other three. The lower number compares one whole module
against one whole page rather than a worse page, and CEDT207 and MXFUN01 dropped the same way.

---

## Decision 18 — What an `[RHS alert]` tag becomes (Needs Chris #18, 24 Sept)

**What the issue is.** Writers type `[RHS alert]` (also `[Alert RHS]`, `[Alert box RHS]`, `[right-hand alert]` …) to ask for
a note box on the right-hand side of the page: 176 tags in 73 modules. The rulebook never says what this tag becomes.
It defines a side box (`05B_COMP14_LAYOUT_STRUCTURE.md` l.100–107) but never links the tag to it. The humans mostly built a side
column, sometimes a full-width box, sometimes an ordinary paragraph. On 24 Sept the loop measured it against its
brief's rule ("build only if one form holds 60 %"), found 0.58, and declined. That measurement was wrong (see
correction 4): corrected, the side column holds 0.66 (Standard 0.70). Two things stop the loop acting on the corrected
figure. The brief counts the two box styles inside the column as separate forms (largest 0.36), and the KB is silent.

**The real examples.**

1. **ANZH101 lesson 1: the human built a side column and PageForge matches.**
   - WT `01-Finalized_Modules_/Standard/ANZH101/ANZH101 Writers Template + Media List_parsed.txt` l.115–124:
     `🔴[RED TEXT] [Activity] 1B [/RED TEXT]🔴` … `🔴[RED TEXT] [RHS Alert]  [/RED TEXT]🔴It is important to remember that iwi have varied stories about their origins and arrival. …`
   - Gold `ANZH101_1.0.html` l.131–150: `<div class="col-md-8 col-12"><div class="activity alertPadding" number="1B">` … `<div class="col-md-4 col-12"><div class="alertActivity">` … `<p>It is important to remember that iwi have varied stories …`
   - PageForge `01-Claude_Modules_/Standard/ANZH101/ANZH101_1_0.html` l.112–128: `<div class="col-md-8 col-12"><div class="activity" number="1B">` … `<div class="col-md-4 offset-md-0 col-12"><div class="alertActivity"><p>It is important to remember …`
   - *A learner sees (both):* a tinted note box in a narrow column to the right of activity 1B.
2. **XGF9001: the human built a side column; PageForge loses the box.**
   - WT `…/Standard/XGF9001/XGF9001 Writers Template_parsed.txt` l.213–217: `🔴[RED TEXT] [Alert RHS] [H3]  [/RED TEXT]🔴Key questions` / `• What qualities, strengths, and interests make me unique as a gifted ākonga?` …
   - Gold `XGF9001-01.1.html` l.56–61: `<div class="col-md-3 offset-md-1 col-6 offset-3"><div class="alertActivity"><h3>Key Questions</h3><ul><li>What qualities, strengths …`
   - PageForge `01-Claude_Modules_/Standard/XGF9001/XGF9001_2_0.html` l.39–46: `<div class="col-md-8 col-12"><h4>Key questions</h4><ul><li>What qualities, strengths …`
   - *A learner sees:* gold, a small boxed "Key Questions" panel to the right; PageForge, an ordinary heading and list in the main text, no box.
3. **ANZH301 lesson 8: the human made it a paragraph; PageForge makes a side box.**
   - WT `…/Standard/ANZH301/ANZH301 Writers Template + Media List_parsed.txt` l.979–981: `🔴[RED TEXT] [Alert box RHS]  [/RED TEXT]🔴Watch this video of another event … having some fun with it:` / `[Video link] https://player.vimeo.com/video/923114174…`
   - Gold `ANZH301_8.0.html` l.45–46: `<p>Watch this video of another event that shows retaining a connection … having some fun with it.</p>` / `<p style="color: red">Designer note: video needs embedding</p>`
   - PageForge `ANZH301_8_0.html` l.52–54: `<div class="col-md-4 offset-md-0 col-12"><div class="alertActivity"><p>Watch this video of another event …`
   - *A learner sees:* gold, a normal sentence introducing the video; PageForge, the sentence in a side box, separated from its video.

**The numbers** (139 tags whose text was found on the human's page; corrected). Human: side column + `alert top` 50
(0.36), side column + `alertActivity` 42 (0.30), full-width 19 (0.14), paragraph 18 (0.13), other 10. Side column together
**0.66**: Standard 68/97 = **0.70**, Fundamentals 21/32 = 0.66, Inquiry 3/10 = 0.30. PageForge today: side column 66, full-width
34, paragraph 38, absent 1. It matches the human on **64**. In Standard, **22** tags the human put in a side column are
full-width or plain text in PageForge (9 of them XGF9001's lost boxes). **20** Standard tags are full-width / paragraph on both
sides, and 11 of those match exactly today.

**What the KB says.** Nothing about the tag. `05B_COMP14_LAYOUT_STRUCTURE.md` l.100–107 gives the activity sidebar
(`col-md-4 offset-md-0 col-12` > `alertActivity`). `00E_CONSTRAINTS_2.md` l.17 (constraint 68): "`[side alert]` affects
placement only". `07B_MTK_CONTENT_PATTERNS.md` l.175–189 (Word-document conversion only): a `[Side Alert]` is that sidebar.

**What the rule order says.** (1) The KB is silent on the RHS spellings. (3) Each module has its own gold, so strictly each
module's own choice is its target, which the writer's tag cannot predict. (4) The group convention (Standard 0.70) passes
0.60 only if "side column" counts as one form. That is how round 333 framed it (box style chosen by position, 56/70 = 0.80
at the time, `BUILD_CHANGELOG.md` l.4359).

**The choice.**
- **Option A: leave it as it is.** Round 333's side column where it can; otherwise full-width or plain text. The 22 Standard
  mismatches stay. Gate-neutral, no rebuild. (The lost XGF9001 / SCBI301 boxes should be fixed either way.)
- **Option B: an RHS tag always becomes the right-hand side column** (Standard and Fundamentals; not Inquiry). The box
  style is still chosen by position (round 333), and the lost boxes are fixed. Moves ≈ 22 Standard tags (plus some Fundamentals)
  to match the human, and ≈ 11 that match today away. Net more matches. **Gate-moving, scoped rebuild** of the modules
  with an RHS tag.
- **Option C: B, and write it into the rulebook** ("an `[RHS alert]` is the activity sidebar") at your next Admin-Mode
  session, so Claude chat conversions do the same. Same page changes as B, plus one rulebook line for you.

**My recommendation is B** (C if you are doing the rulebook session anyway) because the writer literally asks for the
right-hand side, the humans did it two times in three once the measurement is corrected, and PageForge already builds the
exact box. The writer's tag is the signal, so this follows the writer, not a guess. One refinement for the loop's own
check: when the RHS text is only a lead-in to the next video or link (ANZH301), it may stay with that item.

---

## Decision 19 — Quiz answers the writer highlighted without saying so (Needs Chris #19, 24 Sept) — THE LARGEST

**What the issue is.** On 23 Sept (D13-4) you let the loop build quizzes only where the writer marked the right answer,
and trust a coloured highlight only where the writer said so, e.g. `[answers are highlighted]`. That rule is round
309's guard, because in one module a colour marked every option. Under it, one typing shape was built (r449: 8 quizzes, 57
answers, 55 exactly the human's), and every other quiz type was declined on measurement (largest group 10, floor 20).
What is left: **≈ 190 hand-off boxes** where the writer highlighted the answer but never said so (multiple choice ≈ 63,
dropdown ≈ 29, radio ≈ 16, reorder ≈ 9, the "typing" group ≈ 77, plus ≈ 10 selection boxes not in the ≈ 190). The loop
cannot widen your rule itself.

**The real examples.**

1. **CEDW501 5B "The bubble": multiple choice with a ✅ (yellow), unannounced.**
   - WT `01-Finalized_Modules_/Standard/CEDW501/CEDW501 Writers Template_parsed.txt` l.1227–1238:
     ```
     🔴[RED TEXT] [Activity 5B]  [/RED TEXT]🔴The bubble
     🔴[RED TEXT] [Quiz] [/RED TEXT]🔴
     **1. Understanding the extract**
      What does the word *bubble* mean in this context?
     a. ✅A group of people you live with during lockdown.
     b. A protective shield against Covid-19.
     ```
   - Gold `CEDW501_5.0.html` l.464–472: `<div class="multiChoiceQuiz">` … `<p class="mcqOption" value="correct">A group of people you live with during lockdown.</p>` / `<p class="mcqOption">A protective shield against Covid-19.</p>`
   - PageForge `01-Claude_Modules_/Standard/CEDW501/CEDW501_5_0.html` l.350–364: the rainbow box `⚙ INTERACTIVE (un-built) #34: multiChoiceQuiz — Activity 5B` … `<li>✅A group of people you live with during lockdown.</li>`
   - *A learner sees:* gold, a working quiz that marks their choice; PageForge, a placeholder box (the ✅ visible inside it for the developer).
2. **CHFUN05 6C "Type the number": green-highlighted answers, unannounced.**
   - WT `…/Fundamentals/CHFUN05/CHFUN05 Writers Template_parsed.txt` l.408–426: `🔴[RED TEXT] [typing short answers] [autocheck]  [/RED TEXT]🔴6C Type the number` … `1. **三十八**               **38**` … `8. **九十九**           **99**` (the green shows only as bold. There is no ✅.)
   - Gold `CHFUN05_0_0.html` l.869–875: `<div class="typing autoCheck" layout="standardNoBorder">` … `<p><span class="ch-text">三十八</span> = <input class="form-control" type="text" answer="38" …`
   - PageForge `01-Claude_Modules_/Fundamentals/CHFUN05/CHFUN05_0_0.html` l.846–863: `⚙ INTERACTIVE (un-built) #15: typing (short)` … `<li><b><span class="ch-text">三十八</span>               38</b></li>`
   - *A learner sees:* gold, eight numbers each with a checked answer box; PageForge, a placeholder with the answers printed beside the questions.
3. **OSAI101 1C: green marks EVERY option (the trap).**
   - WT `…/Standard/OSAI101/OSAI101 Writers Template_parsed.txt` l.289–293: `🔴[RED TEXT] [drop down paragraph quiz] answer options in green – no correct answers [/RED TEXT]🔴` … `Q1:Starlight the [dropdown] unicorn, dragon, fawn was galloping …`
   - Gold `OSAI101-01.html` l.606–616: `<div class="dropQuiz autoCheck" layout="paragraph">` … `<div class="dropDown" answer="1 2 3">` (every choice accepted).
   - PageForge `OSAI101_1_0.html` l.559–568: a hand-off box, `Q1: Starlight the` / `unicorn, dragon, fawn was galloping …`
   - *A learner sees:* gold, a story game where any word works. If the green were read as "the answer", the quiz would mark two of three choices wrong.

**The numbers.** Sources: `CONVERTER_V2/outputs/_s40_r449_mcqcross.log` l.3 (23 yellow lines), `_s40_r449_mcqtables.log`
l.30 (40 yellow tables), `_s40_r6_quizsignals.log` l.4–5, 19–20, 30–37, 46–50 (dropdown 29, reorder 9, radio 16, selectionBox 10),
`LOOP_STATE_ARCHIVE.md` l.3868 (green ≈ 77). Today's un-built quiz boxes: multiChoiceQuiz 385, typing 253, dropDown 256,
reorder 103, radioQuiz 89, selectionBox 79 (no quiz type has been built since r449, so the ≈ 190 still stands).
**Yellow vs green:** the whole multiple-choice group (63) is yellow and already shows ✅. Dropdown is mostly yellow.
The "typing" group, and most of radio and reorder, are green, which leaves no mark.

**What the KB says.** `03_COMP_CORE_INTERACTIVES/03D_COMP02_QUIZZES_2.md` l.23: "The writer marks one (or more) options as the
**correct answer** — e.g. a ✅ tick, "(correct answer)", bold, or a separate answer key." The KB has no rule about green or
about highlights as answers.

**What the rule order says.** (1) The KB names the ✅ tick as an answer signal, and the parser turns a yellow highlight into
exactly that tick. The KB says nothing about green. Your D13-4 decision (a narrower rule) currently outranks both.

**The choice.**
- **Option A: keep your 23 Sept rule.** Only answers the writer typed in red or announced are built. The ≈ 190 stay hand-off
  boxes. Gate-neutral, no rebuild. (The loop still fixes the "autocheck = typing" mislabel on its own.)
- **Option B: trust yellow ✅ ticks when the page structure proves it.** Build only where exactly one OPTION per question
  carries a ✅ (counting options, not highlighted runs), never under the writer's `[Button] Go to quiz` (a D2L quiz),
  never where the writer says "no correct answers". Multiple choice first (≈ 63 boxes, ≈ 53 after the D2L ones), then
  dropdown. One type per session, each checked against the human's own quizzes before it ships. Green stays a hand-off box.
  Judged on each widget's own verifier (the match score barely moves); **scoped rebuild, one type at a time.**
- **Option C: B, and trust green too,** with the same guards. Adds the green-marked language and Pathways activities (≈ 80),
  where green is sometimes emphasis (MXEO301) or every option (OSAI101). Higher risk of a quiz that marks a right answer wrong.

**My recommendation is B** because the ✅ tick is the answer signal the rulebook names, the multiple-choice group is both
the largest and entirely ticked, and the added guards cover every trap found (OSAI101's all-options green, the D2L quiz
questions). Green is too mixed to trust yet.

---

## Decision 22 — BLL overview: Knowledge and Practices in their own tabs? (Needs Chris #22, 24 Sept)

**What the issue is.** In 19 Blended Literacy modules (BLL243–276) the module overview menu has tabs. The humans always
move the Knowledge and Practices lists out of the first "Overview" tab. They go into their own tabs in 10 modules
(11 for Knowledge), into the "Information" tab in 7, or into one combined tab (BLL250). PageForge leaves both lists in the
Overview tab and shows an empty Information tab. The rulebook's standard tab set (constraint 67) gives each its own tab,
and round 460 already does this everywhere else. But the rulebook's CL-0040 entry deliberately left the Blended Literacy
question open ("the open BLL263 D2 … question is NOT touched"), so r460 excludes BLL and the loop may not choose. The
writer's document is the same either way.

**The real examples.**

1. **BLL261: the human used own tabs.**
   - WT `01-Finalized_Modules_/Standard/BLL261/BLL261 Writers Template_parsed.txt` l.11 `[H3] Knowledge`, l.43 `[H3] Practices`, l.65 `[H3] Learning Intentions`, l.119 `CS: If content is too large, please put the "Learning Intentions" and "How will I know I have learned it" in Tab 1 - Overview and the "Knowledge" and "Practices" into Tab 2 – Information`
   - Gold `BLL261_0.0.html` l.25–36, 64–67: `<ul class="nav nav-tabs"><li><a>Overview</a></li><li><a>Knowledge</a></li><li><a>Practices</a></li></ul>` … the first pane opens `<h4><span>Learning Intentions</span></h4>`; `<div class="tab-pane overflowYScroll" scroll="500">` … `<h4><span>Knowledge</span></h4>`
   - PageForge `01-Claude_Modules_/Standard/BLL261/BLL261_0_0.html` l.21–32, 95–100, 107: `<li><a>Overview</a></li><li><a>Information</a></li>` … the first pane opens `<h4><span>Knowledge</span></h4>`; the second pane is empty; the writer's CS note printed as a red "Writers Note" in the page body.
   - *A learner sees:* gold, three tabs, with the learning intentions first and Knowledge and Practices behind their own tabs. PageForge shows two tabs: one long Overview column starting with Knowledge, and an Information tab that opens blank.
2. **BLL263: the human used Information.**
   - WT `…/BLL263/BLL263 Writers Template_parsed.txt` l.11 Knowledge, l.51 Practices, l.73 Learning Intentions, l.113 the same CS note.
   - Gold `BLL263_0_0.html` l.33–46, 133–136: tabs `Overview` / `Information`; Overview holds the learning intentions; `<div class="tab-pane overflowYScroll" scroll="500">` … `<h4><span>Knowledge</span></h4>`.
   - PageForge `BLL263_0_0.html` l.21–31: the same two tab names, but Knowledge first in Overview; Information blank.
   - *A learner sees:* gold, learning intentions in Overview and the lists under Information; PageForge, everything in Overview and a blank Information tab.
3. **BLL250 (Inquiry): one combined tab.** Gold `01-Finalized_Modules_/Inquiry/BLL250/BLL250.html` l.33–34: tabs "Learning Intentions and Success Criteria" / "Knowledge and Practices".

**The numbers** (19 tabbed BLL overviews; 11 more BLL2xx modules have a flat menu, where PageForge already matches).

| Series | Own tabs | Information | Other |
|---|---|---|---|
| BLL24 (243, 247) | 2 | 0 | — |
| BLL25 (250, 251, 253, 255, 257) | 1 (253) | 3 (251, 255, 257) | 250 combined |
| BLL26 (261–266) | 2 (261, 262) | 3 (263, 264, 266) | 265 hybrid |
| BLL27 (271–276) | 5 (271–274, 276) | 1 (275) | — |

Knowledge in its own tab: 11 of 18 = **0.61** (0.63 counting BLL250). Practices in its own tab: 10 of 18 = 0.56. The census
(`CONVERTER_V2/outputs/_placement_census_s46.md` l.121, l.155, l.76) flags the same rows.

**What the KB says.** `01B_MODULE_MENUS_FOOTER.md` l.39: "The `<li>` order is fixed: **Overview → Knowledge → Practices →
Information → Standards/Assessment.**" l.117: the Information tab "holds **Planning your time**, **What do I need to get
started?**, and **Want to know where to start?** … if NONE are supplied, omit the whole tab". `12C_CHANGE_HISTORY_CL0029_0040.md`
l.20 (CL-0040): "series with legitimately simplified/absent overview menus … keep that archetype, so the open BLL263 D2 (BLL
overview tab-split) question is NOT touched".

**What the rule order says.** (1) The KB's tab set points to own tabs, but CL-0040 explicitly leaves BLL open, so rank 1 is
contested. (2) Siblings disagree across series. (4) Knowledge 0.61 is just over the line and Practices 0.56 is under. Only
BLL25's Information (3 of 4) and BLL27's own tabs (5 of 6) are clear series conventions.

**The choice.**
- **Option A: own tabs (the rulebook's standard set).** Overview / Knowledge / Practices; the empty Information tab removed
  (r460's rule with BLL taken off its exclusion list, `pageforge-site/converter-v2/data/Emit_Templates.json` ≈ l.3810–3823).
  Matches 10 of 19 fully (11 for Knowledge); the 7 Information golds become labelled exceptions. **Gate-moving (up);
  19 modules' overview page rebuilt.**
- **Option B: everything into Information.** Overview / Information with both lists in Information. Matches 7 of 19. Gate-moving; 19 rebuilt.
- **Option C: by series.** BLL25 → Information; the other series → own tabs. Matches 12 of 19, but it is a special case the
  rulebook doesn't have. Gate-moving; 19 rebuilt.
- **Option D: leave it.** Matches no human page, and learners keep an empty tab.

**My recommendation is A** because it is the rulebook's own tab set (the Information tab is defined for other content), it
matches the majority and the newest series, and it removes the blank tab learners click on today. C is two modules closer to
the humans, but it adds a rule the rulebook doesn't have.

---

## Decision 23 — The Maths lesson menu without the extra wrapper (Needs Chris #23, 25 Sept)

**What the issue is.** Every lesson page has a pop-out menu with "We are learning" and "You will show your understanding
by / I can". KB 01B says its content goes inside `<div class="row"><div class="col-md-8 col-12">`. That is an invisible
layout box that makes the content two-thirds wide on a tablet or computer. PageForge builds it and most modules use it. But
in four Maths series (MXFU, MXEX, MXDB3, MXDI3) the human left the wrapper out on every paired lesson page (91 of 91). The KB
outranks the gold, so the loop can't follow the Maths humans unless you name it as a series convention. KB 10 §3 has a
"series conventions — preserve" list for exactly this.

**The real examples.**

1. **MXFU301 lesson 1.**
   - WT `01-Finalized_Modules_/Standard/MXFU301/MXFU301 Writers Template + Media List_parsed.txt` l.90–104: `🔴[RED TEXT] [Lesson Overview] [/RED TEXT]🔴` / `We are learning:` / `• *to* *identify words and phrases used to predict the probability of an event happening*` … `You will show your understanding by:` …
   - Gold `MXFU301_1.0.html` l.22–34: `<div id="module-menu-content" class="moduleMenu">` / `<h5>We are learning to:</h5>` / `<ul><li>to identify words and phrases …</li>` …
   - PageForge `01-Claude_Modules_/Standard/MXFU301/MXFU301_1_0.html` l.19–35: `<div id="module-menu-content" class="moduleMenu">` / `<div class="row">` / `<div class="col-md-8 col-12">` / `<h5>We are learning:</h5>` …
   - *A learner sees:* gold, two headings and five bullets across the full width of the menu panel. PageForge shows the same words in the left two-thirds on a tablet or computer, so long bullets wrap a line sooner. On a phone the two look the same.
2. **MXDB302 lesson 1.** Gold `MXDB302_1.0.html` l.23–32 (bare `h5 + ul`); PageForge `MXDB302_1_0.html` l.19–32 (the same inside `row > col-md-8`). *A learner sees:* two short bullets, with almost no visible difference.
3. **MXEX302 lesson 1: the separate, bigger problem.** The WT has no `[Lesson Overview]` for this lesson (l.73–77). The human
   wrote one (`MXEX302_1.0.html` l.23–32: "about the importance of statistics in sport and everyday life." / "I can:" …).
   PageForge `MXEX302_1_0.html` l.19–24 ships an empty `row > col-md-8`. *A learner sees:* a menu button that opens a blank panel.
   Removing the wrapper does not fix this. 37 of the 81 row-form pages are like it (a source gap; KB 10 l.63 says build the
   empty shell with a red note).

**The numbers.** `CONVERTER_V2/outputs/_s45_r4_menuwrap.log` l.27–32: MXDB bare 14 (MXDB3), MXDI bare 7 (MXDI3), MXEX bare 26
(+1 row, a pairing mistake: PageForge's MXEX101_5_0 paired with the gold overview page), MXFU bare 44. **13 modules:** MXFU201,
202, 301, 302, 402; MXEX101, 201, 202, 301, 302; MXDB301, 302; MXDI301. A read-only what-if removed only the wrapper and
re-scored with the gate's own comparer: **+0.086 points on the corpus mean, +11 pages over 50 %.** That is about the size
of session 46's ten rounds together (+0.0883). It falls on 81 pages in 11 modules.

**What the KB says.** `01B_MODULE_MENUS_FOOTER.md` l.296–301: "**Key structural rules for lesson page simplified menus:** …
Content goes directly inside `<div class="row"><div class="col-md-8 col-12">`". `10_CORPUS_VALIDATED_SCAFFOLDING.md`
l.30–32: "## 3. Lesson-menu *style* deviations (series conventions — preserve, don't "correct") … When you see these in a
reference, they are CORRECT for that series". Its existing tables cover lead-in labels (l.34–40) and title headings
(l.43–48), so the wrapper would be a new sub-table.

**What the rule order says.** (1) KB 01B's rule fires, so the row form wins today. With a series-scoped KB 10 §3 entry (or
your named decision, as D14-20 was for KB 07D), the bare form becomes the target for these four series only.

**The choice.**
- **Option A: keep the rulebook's wrapper (today).** The 91 pages stay labelled exceptions. Gate-neutral, no rebuild.
- **Option B: a named Maths-series convention.** PageForge leaves out the wrapper on MXFU / MXEX / MXDB3 / MXDI3 lesson
  pages, authorised by your decision now. The matching KB 10 §3 line is added at your next rulebook session (#1). **Gate-moving
  (≈ +0.09 points); 11 modules regenerated.**

**My recommendation is B** because the humans did it on every single page in those four series, the rulebook already keeps a
"series conventions — preserve" list for exactly this, and it is worth about as much score as a whole session of loop
rounds. Learners will barely see the difference. The empty and missing Maths menus are a separate job the loop will record.

---

## The questions — one per decision, each answerable in a sentence

1. **#17.** Should CEDT301 be built as one tabbed page like every other CEDT module, accepting a lower score for that one module?
2. **#18.** Should a writer's `[RHS alert]` always become the right-hand side box (Standard and Fundamentals), and do you also want it written into the rulebook?
3. **#19.** May the loop build a quiz from the writer's yellow ✅ ticks when each question has exactly one ticked option, multiple choice first, while green highlights stay hand-off boxes?
4. **#22.** In the 19 tabbed Blended Literacy overviews, should Knowledge and Practices each get their own tab (the rulebook's set), with the empty Information tab removed?
5. **#23.** Should the four Maths series (MXFU, MXEX, MXDB3, MXDI3) keep their lesson menu without the extra wrapper, as a named series convention?
