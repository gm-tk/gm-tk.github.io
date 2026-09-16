# PageForge autonomous loop — the decisions waiting on Chris (16 September 2026)

This is a plain-English walkthrough of every question the loop has parked because it could not
settle it on its own. Nothing in this document changes any code, data or module — it only explains.
Read it in any order; each section stands alone and ends with one question you can answer in a sentence.

**Where these came from.** `LOOP_STATE.md` (the loop's own diary: its "Blocked classes", the
"Declined" entries that carry a *needs Chris* note, and every "Decisions from Chris" section already
recorded), `KB_AMALGAMATION_STATUS.md` (the knowledge-base checklist), and the recent
`BUILD_CHANGELOG.md` entries. Nothing you have already answered is re-asked: decisions 2 and 3 from
the 15 September plateau report ("Yes to 2 and 3") were carried out and are not here.

> **ANSWERED 2026-09-16 ≈15:20 NZST — all nine.** Chris's answers, recorded verbatim in `LOOP_STATE.md` under "Decisions from Chris (session 10)" as D10-1 … D10-9,
> with what each authorises; the next `/loop-start` works them in this order: (1) D10-6 exclude the 8 CED briefs from the score and re-baseline;
> (2) D10-1 c47 in full — the human's form ("the lesson number is isolated to the top-right corner and the lesson title is kept as the h1");
> (3) D10-2 English first for Standard bilingual lesson titles (**B**); (4) D10-7 equations as MathML (**A**); (5) D10-5 05D tables everywhere (**A**);
> (6) D10-9 the KB's `<h5>` labels everywhere incl. the overview tab (**A**); (7) D10-3 widget-build rounds in the loop, one type per kickoff (**A**).
> Closed with no round: D10-4 stickyNav — keep the ban everywhere (**C**, the KB to be edited to say so); D10-8 `alertPadding` — leave plain (**B**).
> The KB edits those answers imply (14A/14B/14D, 05A, 06 §6, 00G/01A, 01F note) are listed in LOOP_STATE for an Admin-Mode KB round; the KB is untouched here.

---

## The words used below (each defined once)

- **Writers Template (WT)** — the Word document a subject writer fills in. They type the lesson text
  and mark each piece with a *tag* in red square brackets, e.g. `[H2]`, `[Activity 1A]`, `[video]`.
  The `_parsed.txt` file beside each WT is the same document flattened to plain text so it can be
  quoted; `🔴[RED TEXT] … [/RED TEXT]🔴` in those files just marks what the writer typed in red.
- **The gold** — the finished module a human developer built from that WT by hand. It lives under
  `01-Finalized_Modules_/` and is read-only. It is the best example we have of "what good looks
  like", but it spans years, several template systems, and it contains the developer's own choices and
  mistakes.
- **PageForge's output (Claude)** — what the converter builds automatically from the same WT today.
  It lives under `01-Claude_Modules_/`.
- **The knowledge base (KB)** — the written rulebook for the HTML Convertor
  (`00-Other-TK-Resources/htmlconvertor-kb/`): numbered *constraints* (rules), a *change ledger*
  (`CL-0001` onward — dated decisions), and *family rules* (doc 14) for particular subjects. It has been
  maintained for nine months **after** most of the gold was built, so it is the most recent statement of
  what a finished module should look like.
- **The authority order** (`LOOP__Autonomous_Rounds.md` §1b) — when the KB and the gold disagree, the
  loop follows this order: **1. the KB**, 2. the earlier module of the same series, 3. this module's
  own gold, 4. the consensus of the template/subject group. A gold pattern only counts as a target when
  at least **60%** of its group does it (the "solidify share"); below that it is treated as a human
  one-off and left alone.
- **The gates** — the automatic scorecard. The main number is the **skeleton score**: how closely the
  structure of each PageForge page matches the structure of the matching gold page (currently
  51.1%, of an achievable ceiling of about 91.6%). "**pp**" means percentage points of that score.
  A change is **gate-neutral** when it cannot move that score (e.g. it sits in the invisible `<head>` of
  the page) and **gate-moving** when it can.
- **A named override** — when the loop follows a KB rule the gold does not, the pages that score
  lower are listed by name and excluded from the "must not get worse" test. It is intentional, not a bug.
- **Regeneration** — rebuilding the output pages. **Scoped** = only the modules a change touches;
  **full** = all 416 modules (about 90 minutes of machine time).
- **The 20-page floor** — the loop does not build a rule for a pattern that affects fewer than 20
  pages; it records it instead.
- **h1 / h3 / h5 / p** — HTML heading levels 1, 3, 5 and a plain paragraph. To a learner, `h5` is a small
  bold label; `p` is ordinary text.

---

## Decision 1 — Should a lesson's opening heading be dropped when it just repeats the page title? (KB constraint 47)

**What the issue is.** Many writers open a lesson with a heading that repeats the lesson's title, e.g.
`[H2] Lesson 3: Police Officers` on a page whose header already says "Police Officers". The KB rule
(constraint 47) says: drop that duplicate body heading — the title is already in the header. The
human developers did this consistently when the heading carried a `Lesson N:` label, but only about
half the time when the heading was an exact repeat — and some "kept" cases are actually the title of an
activity box that happens to match the page title, which a blunt rule would wrongly delete. The loop
declined it on measurement (the gold's share is 57%, under the 60% bar, and the `Lesson N` form is only
12 pages, under the 20-page floor) and left the KB-over-gold call to you.

**The real examples.**

*SSOG101, lesson 3 (the `Lesson N:` form — the human dropped it).*
- The writer typed — `01-Finalized_Modules_/Standard/SSOG101/SSOG101 Writers Template + Media List_parsed.txt` line 162:
  `🔴[RED TEXT] [H2] [/RED TEXT]🔴 *Lesson 3:*Police Officers`
  followed at line 164 by `[Body] The police are like community helpers who work to keep us safe. …`
- The human built — `01-Finalized_Modules_/Standard/SSOG101/SSOG101_3.0.html` line 18 then the body:
  `<h1><span> Police Officers</span></h1>` … `<div id="body"> … <p> The police are like community helpers who work to keep us safe. …`
  (no heading in the body at all)
- PageForge builds — `01-Claude_Modules_/Standard/SSOG101/SSOG101_3_0.html` lines 15 and 29:
  `<h1><span>* Police Officers</span></h1>` … `<h3>Lesson 3: Police Officers</h3>` then the paragraph.
- What a learner sees: gold — the title once, in the page header, then the text. PageForge — the title
  in the header, then "Lesson 3: Police Officers" again as a heading, then the text.

*MXFU302, lesson 1 (an exact repeat — the human dropped it).*
- The writer typed — `01-Finalized_Modules_/Standard/MXFU302/MXFU302 Writers Template + Media List_parsed.txt` lines 150 and 162:
  `[LESSON 1] **Statistics and Sports**` … `[H2] **Statistics and Sports**`
- The human built — `01-Finalized_Modules_/Standard/MXFU302/MXFU302_1.0.html` line 18:
  `<h1><span>Statistics and Sports</span></h1>` and no body heading with that text.
- PageForge builds — `01-Claude_Modules_/Standard/MXFU302/MXFU302_1_0.html` lines 15 and 37:
  `<h1><span>**Statistics and Sports**</span></h1>` … `<h3>Statistics and Sports</h3>`
- What a learner sees: the same heading twice on PageForge's page; once on the gold's.

*ENGI101, page 3.0 "Being Frank" (an exact repeat the human KEPT — because it is an activity's title).*
- The writer typed — `01-Finalized_Modules_/Standard/ENGI101/ENGI101 Writers Template + Media List_parsed.txt` line 250:
  `🔴[RED TEXT] [Activity 2A]  [/RED TEXT]🔴*Being Frank*`
- The human built — `01-Finalized_Modules_/Standard/ENGI101/ENGI101_3.0.html` lines 18 and 37:
  `<h1><span>Being Frank</span></h1>` … `<h3>Being Frank</h3>` (inside the activity box)
- PageForge builds — `01-Claude_Modules_/Standard/ENGI101/ENGI101_1_1.html` lines 15 and 28: the same two lines.
- What a learner sees: identical on both — and this is a case a careless "drop every duplicate" rule
  would break, so any rule must skip activity-box titles.

**The numbers.** Measured 15 September (`CONVERTER_V2/outputs/_r320_dupheading.json`): 88 cases on 77
pages in 54 modules. The `Lesson N:`-labelled opening duplicate: **12 pages, the human dropped 12 of 12
(100%)** — but under the 20-page floor. The exact duplicate: 70 cases, of which 41 only matched because
PageForge's own title was wrong at the time (the TRR "Finished!" titles — fixed since by round 321); of
the 14 where both sides carry the same title, the human dropped 8 and kept 6 (57%). Corpus-wide the human
keeps an exact duplicate on 111 lesson pages.
The KB rule — `00_MASTER_INSTRUCTIONS/00D_CONSTRAINTS_1.md` constraint 47: *"(Universal) On a lesson
page, drop a body heading whose text is identical (ignoring case/punctuation, and ignoring a `Lesson N`
prefix) to the `<h1>` header title — the title already shows in the header, so the duplicate body `<h3>`
is omitted and the first body `<p>` follows directly. … A body heading introducing a different sub-topic
is kept."*
The authority order: the KB has a rule (level 1) → it outranks the gold's 57%. The loop did not apply it
unattended because the rule predates the change ledger and the score would dip on the pages where the
human kept the duplicate.

**The choice.**
- **Option A — apply constraint 47 in full.** Drop a lesson page's opening body heading when it repeats
  the header title (with or without a `Lesson N:` label), never touching a heading inside an activity box.
  About 30–35 pages change (the 12 labelled + the exact-duplicate residue). A named override on the ~6
  pages where the human kept the repeat; a small net gain elsewhere. Gate-moving (small, mixed);
  scoped regeneration.
- **Option B — apply only the `Lesson N:`-labelled form.** 12 pages where both the KB and the human
  agree. Gate-moving (up), scoped, but it is under the loop's normal floor so it needs your say-so.
- **Option C — leave it.** PageForge keeps repeating the title. No change.

**My recommendation is A**, because the KB states the rule as universal and explicit, the one thing
that made it risky (the wrong TRR titles) has been fixed since, and the activity-box exception is easy to
honour. The learner-facing result is simply "the title is not printed twice".

**Question 1:** Apply constraint 47 in full (A), only the `Lesson N:` form (B), or leave it (C)?

---

## Decision 2 — When a Standard-module lesson title is bilingual, which language goes first? ("decision 4")

**What the issue is.** Some writers give a lesson title as a pair separated by a bar:
`Pūrākau | Stories`. PageForge splits this into two header lines, in the writer's order. In the
Bilingual (MTK) modules the KB says Māori first, and PageForge already does that. In the ordinary
**Standard** modules the KB is silent on the order, and the human developers went both ways: on the six
Standard pages measured they put English first on four and kept the writer's order on two. Six pages is
far too few to call a convention (and after later rounds only two pages still differ), so the loop left
it as "writer's order" and parked the question.

**The real examples.**

*ANZH101, lesson 2 (the human swapped to English first).*
- The writer typed — `01-Finalized_Modules_/Standard/ANZH101/ANZH101 Writers Template + Media List_parsed.txt` line 174:
  `🔴[RED TEXT] [H2]  [/RED TEXT]🔴*Lesson 2: Pūrākau | Stories*`
- The human built — `01-Finalized_Modules_/Standard/ANZH101/ANZH101_2.0.html` lines 18–19:
  `<h1><span>Stories</span></h1>` / `<h1><span>Pūrākau</span></h1>`
- PageForge builds — `01-Claude_Modules_/Standard/ANZH101/ANZH101_2_0.html` lines 15–16:
  `<h1><span>Pūrākau</span></h1>` / `<h1><span>Stories</span></h1>`
- What a learner sees: gold — "Stories" then "Pūrākau"; PageForge — "Pūrākau" then "Stories".

*MXDB202, lesson 3 (the human swapped to English first).*
- The writer typed — `…/MXDB202/MXDB202 Writers Template + Media List_parsed.txt` line 518: `[H2] Rapa Nui | Easter Island`
- The human built — `01-Finalized_Modules_/Standard/MXDB202/MXDB202_3.0.html` lines 18–19: `<h1><span>Easter Island</span></h1>` / `<h1><span>Rapa Nui </span></h1>`
- PageForge builds — `01-Claude_Modules_/Standard/MXDB202/MXDB202_3_0.html` lines 15–16: `<h1><span>Rapa Nui</span></h1>` / `<h1><span>Easter Island</span></h1>`

*ANZH105, lesson 1 (the human kept the writer's order — the same series as ANZH101).*
- The writer typed — `…/ANZH105/ANZH105 Writers Template + Media List_parsed.txt` line 78: `[H2] *Lesson 1:* Nō Hea Koe? | Where Are You From?`
- The human built — `01-Finalized_Modules_/Standard/ANZH105/ANZH105_01.0.html` lines 18–19: `<h1><span>Nō Hea Koe?</span></h1>` / `<h1><span>Where Are You From?</span></h1>`
- PageForge builds — `01-Claude_Modules_/Standard/ANZH105/ANZH105_1_0.html` lines 15–16: identical.

**The numbers.** Round 316 (`outputs/_r316_lessonpair.json`): 13 Standard-module pages carry a bar-separated
lesson title; on the 6 where the human built the same pair, English-first 4 : as-written 2. The latest
title census (`outputs/_r324_lessontitles.json`, 1,247 paired lesson pages) lists the order difference on
**2 pages**. The KB: constraint 79 (`00G_CONSTRAINTS_3.md`) fixes *which* title goes in the header but says
nothing about order; the only order rule is `07D_MTK_HTML_SKELETONS.md` rule 7, *"Titles in `<h1><span>`
— Māori first, English second"*, scoped to MTK (Bilingual) modules — already applied. The authority
order: no KB rule for Standard → the gold's 4-of-6 is under the 60% bar → the loop keeps the writer's order.

**The choice.**
- **Option A — keep the writer's order (today's behaviour).** No change; the 2 pages stay as they are.
- **Option B — English first in Standard modules.** A house rule the KB does not have; 2 pages move now,
  and every future bar-separated Standard title is swapped. Gate-moving by a hair; scoped.
- **Option C — Māori first everywhere** (extend the MTK rule to all templates). 2 pages today;
  ANZH105-style pages would then be swapped against the writer. Needs a KB line.

**My recommendation is A**, because the writer's order is the only signal the converter has, the gold
disagrees with itself inside one series, and two pages do not justify a rule — unless Te Kura has a
house style, in which case say which (B or C) and the KB should get the sentence.

**Question 2:** Keep the writer's order (A), English first (B), or Māori first everywhere (C)?

---

## Decision 3 — Should the loop start BUILDING the interactives PageForge cannot build yet? ("decision 5")

**What the issue is.** Writers tag interactive widgets: drag-and-drop, click-to-drop, self-check
(click the right word), sliders, hover-definitions, flip cards, and so on. PageForge builds several types
well (speech bubbles 91%, carousels 74%, accordions 64%) but builds only **6.6% of drag-and-drops (58 of
880)**, and three types have **no builder at all**: self-check (153 tagged), slider (47), info-hover (37).
Where it cannot build, it ships a **hand-off box** — an orange dashed panel holding the writer's content
and the line `⚙ INTERACTIVE (un-built) #1: dragAndDrop — see MXDI102_interactives.txt` — plus a worklist
file per module so a developer (or the KB's own "Interactives Build Mode", where the Convertor project
builds them from that worklist and the Page Stitcher drops them in) can finish the job. The loop cannot
decide this itself because (a) a widget type is a multi-round engineering project, not a one-round rule
(drag-and-drop alone appears in 682 distinct authoring shapes); (b) by design these builds are invisible
to the gates — a writer-tagged widget is judged by its own checker, not against the human's version; and
(c) a downstream path (Interactives Build Mode + the Page Stitcher) already exists for exactly this work.

**The real examples.**

*MXDI102, lesson 1 — a drag-and-drop.*
- The writer typed — `01-Finalized_Modules_/Standard/MXDI102/MXDI102 Writers Template + Media List_parsed.txt` line 126:
  `🔴[RED TEXT] [drop and drag]  [/RED TEXT]🔴Label the parts of a fraction. 🔴[RED TEXT] Can you make the words draggable so they can label the correct parts of the fraction please. [/RED TEXT]🔴`
- The human built — `01-Finalized_Modules_/Standard/MXDI102/MXDI102_1.0.html` from line 153:
  `<p>Label the parts of a fraction.</p>` / `<div class="dragAndDrop autoCheck" layout="scatter">` / `<div class="row dropContainer">` / `<div class="drop col-4 priDrop" top="30%" left="35%" option="1"></div>` … (a working widget: two drop targets on a big ½, the words "numerator" / "denominator" to drag)
- PageForge builds — `01-Claude_Modules_/Standard/MXDI102/MXDI102_1_0.html` lines 86–91:
  `<p class="cv2-note" …>Writers Note: Can you make the words draggable …</p>` / `<p …>⚙ INTERACTIVE (un-built) #1: dragAndDrop — Activity (inline) — see MXDI102_interactives.txt</p>` / `<p>Label the parts of a fraction.</p>` / `<p>Go to journal.</p>`
- What a learner sees: gold — a drag-and-drop they can do; PageForge — an orange box with the
  instruction text and a developer note, nothing to drag.

*BLL113, page 2 — a self-check (no builder exists).*
- The writer typed — `01-Finalized_Modules_/Standard/BLL113/BLL113 Writers Template + Media List_parsed.txt` lines 105–109:
  `🔴[RED TEXT] [self check]  [/RED TEXT]🔴Click on the word 'on'.` then a one-row table `on ║ in ║ on ║ on ║ no ║ in ║ no ║ on` with the correct cells typed in red.
- The human built — `01-Finalized_Modules_/Standard/BLL113/BLL113-02.html`:
  `<p><b>Click on the word 'on'.</b></p>` / `<div class="wordSelect autoCheck row" layout="table">` / `<div class="wordSelectButton" colour="blue" value="on">on</div>` … `<td class="sassoonI-text"><span spanValue="on">on</span></td>` (a click-the-word game that marks itself)
- PageForge builds — `01-Claude_Modules_/Standard/BLL113/BLL113_1_0.html`:
  `⚙ INTERACTIVE (un-built) #2: selfCheck + selfCheck + selfCheck — Activity (inline) — see BLL113_interactives.txt` then the plain table.
- What a learner sees: gold — a game; PageForge — a static table inside an orange box.

*MXDI102, activity 1C — a second drag-and-drop on the same page* (`_parsed.txt` line 164, `[Drop and drag] Divide these sets of things into 2 equal groups…`; PageForge line 140 `⚙ INTERACTIVE (un-built) #2: unclassified + dragAndDrop — Activity 1C`) — the same picture.

**The numbers** (`CONVERTER_V2/outputs/COVERAGE_DASHBOARD.md`, refreshed 16 September):

| Type | Writers tagged | Built | Still a box | Modules | Distinct shapes |
|---|--:|--:|--:|--:|--:|
| dragAndDrop | 880 | 58 | 822 | 291 | 682 |
| clickDrop | 509 | 185 | 324 | 108 | 231 |
| accordion | 704 | 449 | 255 | 112 | 218 |
| carousel | 902 | 663 | 239 | 140 | 180 |
| flipCard | 484 | 269 | 215 | 121 | 179 |
| selfCheck | 153 | 0 | 153 | 65 | 98 |
| modal | 355 | 202 | 153 | 59 | 128 |
| tabs | 121 | 46 | 75 | 45 | 70 |
| slider | 47 | 0 | 47 | 30 | 38 |
| infoTrigger | 37 | 0 | 37 | 22 | 31 |

The KB: `15_INTERACTIVES_BUILD_MODE/15A_MODE_CORE_AND_CONTRACT.md` — *"PageForge's HTML Generator … leaves
the interactives it cannot yet build as reference-code placeholders and lists them in a companion
worklist … In this mode the Convertor takes that worklist and returns production-quality HTML for every
un-built interactive … so PageForge's Page Stitcher can drop each build into the exact spot"*. Your
standing ruling (Decision Framework A1): the writer's tag is the target, and a built widget is judged on
its own checker, not on the human's version. The authority order does not settle *who* builds them.

**The choice.**
- **Option A — authorise widget-build rounds inside the loop, one type per kickoff**, biggest first
  (drag-and-drop → click-drop → accordion → carousel → flip card …), each round judged by that widget's
  checker. Learners get working widgets on the pages PageForge builds; the cost is many long rounds
  (drag-and-drop alone is hundreds of shapes), each with a family-wide regeneration (drag-and-drop = 291
  modules ≈ a near-full rebuild), and the skeleton score will not show it.
- **Option B — leave the builds to the downstream path** (Interactives Build Mode / the developer) and
  keep the loop on page structure. No change to the pages; the orange boxes stay.
- **Option C — authorise only the three types that have NO builder** (self-check 153, slider 47,
  info-hover 37 — 237 sites, 117 modules), where today's output is nothing but a box. Smaller, fixed
  shapes (the self-check is a one-row table); a bounded trial of the build machinery.

**My recommendation is B, with C as the bounded version if you want builds at all** — the loop's
strength is structure rules it can prove corpus-wide in one round; the build backlog is a separate,
much larger project that already has its own designed route (Mode 6 + the Stitcher). If you do want
PageForge itself to build more, start with C: the learner-facing gain per site is the largest (a game
instead of a box) and the shapes are the most regular.

**Question 3:** Widget-build rounds in the loop (A), leave builds downstream (B), or only the three
builder-less types (C)?

---

## Decision 4 — The `stickyNav` line in the page head: your project rule says "never", the KB says "add it" in three families

**What the issue is.** `stickyNav` is one line in the invisible `<head>` of a page —
`<script src="js/stickyNav.js" type="text/javascript" class="stickyNav"></script>` — that loads a small
floating-navigation script. Your project instruction says it was a templating error copied between
modules and must never be emitted; the KB's subject-family rules say the opposite for three families
(Languages Phase 1–4, ConnectED Phase 5, Health & PE) and even ask for a "set up the stickyNav.js file"
developer note. The human developers put it on 63% of all gold pages, across far more series than the KB
names. Two of your own instructions disagree, so the loop does not arbitrate. The writer never types
anything about it — this is purely a developer-side line.

**The real examples** (the writer's side is empty in all three: no WT mentions "sticky" or "floating nav").

*CEDT501 (ConnectED Phase 5 — a KB family).*
- The human built — `01-Finalized_Modules_/Standard/CEDT501/CEDT501_0.0.html` lines 8–11: `<title>CEDT501 0.0</title>` then `<script src="js/stickyNav.js" type="text/javascript" class="stickyNav"></script>` (every one of its 15 pages).
- PageForge builds — `01-Claude_Modules_/Standard/CEDT501/CEDT501_0_0.html` lines 7–8: `<title>CEDT501 Kia Māia</title>` then straight to the standard `idoc_scripts.js` line — no stickyNav.

*HES1003 (Health & PE — a KB family).*
- The human built — `01-Finalized_Modules_/Standard/HES1003/HES1003_0.0.html` line 9: `<script src="js/stickyNav.js" type="text/javascript" class="stickyNav"></script>` (all 10 pages).
- PageForge builds — `01-Claude_Modules_/Standard/HES1003/HES1003_0_0.html`: none.

*MXDI101 (Mathematics — NOT a KB family, yet the human added it on all 9 pages).*
- The human built — `01-Finalized_Modules_/Standard/MXDI101/MXDI101_0.0.html` line 9: the same line.
- PageForge builds — `01-Claude_Modules_/Standard/MXDI101/MXDI101_0_0.html`: none.
- What a learner sees: if the `js/stickyNav.js` file is present and set up, a floating arrow/menu
  (in CED Phase 5, links to the Collins and Te Aka dictionaries); if the file is absent, nothing at all —
  the line fails silently. Note the gold module folders here carry no `js/` folder, so the line's effect
  depends on the developer's later set-up, which is exactly what the KB's To Do note asks for.

**The numbers** (`outputs/_r323_stickynav.json`): the gold carries it on **1,504 of 2,385 pages (63%)**,
per module all-or-nothing (253 modules every page, 171 none, 30 mixed); ≥ 60% in 30 series (MX 0.92,
ENGI/ENGR/HIS/AGH/MXDI/MXEO/HES 1.00, CED 0.96, PHE 0.98 …) and 0 in others (Bilingual TRR/PNR 0 of 92,
ARFUN 0, SC 0.05). PageForge: **0 of 2,102**. The KB-named families present in this corpus: CED Phase 5
(5 modules with output), HES (5), PHE (8), HPFUN (15) = **33 modules**; there are no Languages modules in
the corpus.
The rules — `14A_SGP_PURPOSE_FAMILIES_1_5.md` line 54 (Languages): *"Sticky nav on every page. Add
`<script src="js/stickyNav.js" …>` to the `<head>` of every page. At the top of the 0.0 content, emit a
visible `Designer/Developer To Do:` note: set up the `stickyNav.js` file."*; `14B_SGP_FAMILIES_6_11.md`
line 93 (HPE): *"Sticky / floating nav — Fundamentals + Help page only. Add … to the `<head>` …"*;
`14D_…TECHNOLOGY.md` line 11: *"The sticky-nav script recurs across Languages Phase 1–4 (every page), CED
Phase 5 (dictionary links), and HPE"*. Against them — `00_PROJECT_CONTEXT_AND_PHILOSOPHY.md` line 85:
*"`stickyNav` — a templating error that was copied across modules; never emit it."* and
`00_PHASE1_READINESS_BRIEF.md` line 159: *"Never emit `stickyNav.js` … deliberate exclusions"*.
The authority order: the KB family rule is level 1 → add it in those three families; outside them the
gold's 0.92–1.00 in MX/ENG/HIS would ordinarily count as level-4 consensus — but that is exactly the
"copied templating error" your philosophy names, so the loop will not follow it without you.

**The choice.**
- **Option A — the KB families only.** Add the head line (and the KB's To Do note at the top of page
  0.0) in CED Phase 5, HES, PHE, HPFUN — 33 modules; keep the ban everywhere else. Gate-neutral (the
  head is outside every gate; the note is a red developer note the score ignores). Scoped regeneration.
- **Option B — every series where the human did it ≥ 60%.** About 1,300 pages / 250+ modules gain the
  line. Gate-neutral, but close to a full regeneration, and it reinstates the copied error you ruled out.
- **Option C — keep the ban everywhere.** No change; the KB's three family rules stay un-honoured and the
  KB should then be edited to say so.

**My recommendation is A**, because it honours the KB where the KB actually made a decision (three
families with a reason — dictionary links, Fundamentals/Help navigation) and keeps your "never" for the
copies that had no reason. Whatever you choose, one of the two documents should be edited to agree with
the other.

**Question 4:** KB families only (A), every ≥ 60% series (B), or keep the ban (C)?

---

## Decision 5 — Which table style is the default? The KB's two pages disagree (05D vs 06 §6)

**What the issue is.** Every table PageForge builds today is the plain form `<table class="table">`
inside the scrolling wrapper the KB asks for. The KB's component page (05D) says the general default is
`table table-bordered` (visible cell borders) with `tableFixed` (equal column widths) for two-column
comparison tables; the KB's template-recognition page (06 §6) shows a different baseline,
`table noHover tableFixed`. The human developers split almost exactly down the middle in Standard modules
(bordered 51%) — a tie the loop's rule says to leave alone — but lean bordered in Inquiry (72%),
Fundamentals (69%) and Bilingual (86%). Because the KB contradicts itself, the loop could not take the
"KB wins" route without knowing which KB page you mean.

**The real examples.**

*AGH1001, lesson 4 — the human used the bordered form.*
- The writer typed — `01-Finalized_Modules_/Standard/AGH1001/AGH1001 Writers Template + Media List_parsed.txt` line 503: `┌─── TABLE ───` / `│ **Livestock Group** ║ **Gestation Period (Days)** … ║ **Time of Mating** ║ **Time of Birthing**` (an ordinary Word table)
- The human built — `01-Finalized_Modules_/Standard/AGH1001/AGH1001.04.html` lines 178–181: `<div class="table-responsive">` / `<table class="table table-bordered">` / `<tr>` / `<th>Livestock Group</th>`
- PageForge builds — `01-Claude_Modules_/Standard/AGH1001/AGH1001_4_0.html` lines 132–135: `<div class="table-responsive">` / `<table class="table">` / `<tr>` / `<th><b>Livestock Group</b></th>`
- What a learner sees: gold — a grid with lines around every cell; PageForge — the same data with only
  horizontal rules between rows.

*AGH1002, lesson 4 — the same series, same subject, same developer era: the plain form.*
- The human built — `01-Finalized_Modules_/Standard/AGH1002/AGH1002.04.html`: `<div class="table-responsive">` / `<table class="table">` / `<tr>` / `<th>Soil Type</th>` / `<th>Drainage</th>`
- PageForge builds — the plain form too (identical to the gold here).

*BLL230 (Inquiry) — the bordered form.*
- The writer typed — `01-Finalized_Modules_/Inquiry/BLL230/BLL230 Writers Template_parsed.txt` line 296: `┌─── TABLE ───` / `│ List 1 – 'ow' as in snow ║ List 2 – 'ow' as in cow`
- The human built — `01-Finalized_Modules_/Inquiry/BLL230/BLL230.html` line 738: `<table class="table table-bordered">` / `<thead>` / `<tr>` / `<th>List 1 &ndash; 'ow' as in snow</th>`
- PageForge builds — `01-Claude_Modules_/Inquiry/BLL230/BLL230_0_0.html` line 499: `<table class="table">` / `<tr>` / `<th>List 1 – 'ow' as in snow</th>`

**The numbers** (measured inline in session 5, `LOOP_STATE.md` "Blocked classes"): PageForge ships the
plain form on **1,063 tables / 518 pages**. Gold: Standard `table-bordered` **0.51** of 1,432 tables (104
modules all-bordered / 51 none / 78 mixed); Inquiry 0.72; Fundamentals 0.69; Bilingual 0.86; `noHover`
0.09; `tableFixed` 0.30 — and `tableFixed` follows column count (4+ columns 0.51, 2 columns 0.19), not
the KB's "two-column comparison" guidance.
The KB — `05D_COMP14_BUTTONS_TABLES_COLUMNS.md` lines 227–239: `<div class="table-responsive">` /
`<table class="table table-bordered">` … *"`table-bordered`: General default for most table types;
`tableFixed`: Prefer for two-column comparison tables … Use `tableFixed` WITHOUT `table-bordered` for
these cases."* versus `06_TEMPLATE_RECOGNITION.md` lines 407–408: `<div class="table-responsive">` /
`<table class="table noHover tableFixed">`.
The authority order: level 1 would apply — if the KB said one thing. A bordered default is a named
override costing ≈ 133 matched lines in Standard for +74 in Inquiry/Fundamentals (≈ −0.01pp net).

**The choice.**
- **Option A — 05D's `table table-bordered` everywhere** (plus `tableFixed` for true two-column
  comparison tables). Every table gets cell borders. A named override in Standard (the tie), a gain in the
  other three templates. Gate-moving (tiny net), full regeneration in practice (tables are everywhere).
- **Option B — bordered only where the human's template family agrees ≥ 60%** (Inquiry, Fundamentals,
  Bilingual), Standard stays plain until the KB reconciles its two pages. A template-keyed flag, the
  precedent already exists. Gate-moving (up), scoped to those three folders.
- **Option C — leave every table plain.** No change; the KB's 05D default stays un-honoured.

**My recommendation is B**, because it applies the KB rule wherever the evidence confirms it and leaves
the genuine tie alone until you tell the KB which of its own pages is right. If you say "05D is the
rule", A is the honest reading and the Standard dip is small.

**Question 5:** Bordered everywhere per 05D (A), bordered only where the family agrees (B), or leave plain
(C)? And which KB page is right — 05D or 06 §6?

---

## Decision 6 — The eight ConnectED "revision brief" modules whose Writers Template is an edit list, not content

**What the issue is.** CEDR201, CEDR301, CEDR302, CEDT201–204 and CEDW303 (Inquiry template) were
*revisions* of existing modules. Their Word file is an edit brief — lines such as `[Keep rest of
content]`, `[Edit page]`, `Remove first lines of text before 3-2-1`, and ALL-CAPS phase names
WONDER / EXPLORE / CONNECT / ACT / REFLECT — followed by an **unfilled blank** Writers Template. The real
module content mostly lives in the previous version of the module, which is not in the document at all.
PageForge's "where does the content start" logic lands on the blank template and ships its
placeholders. The human's gold is the finished, revised module. Each of the eight pages scores 8–20%
and drags the average; no converter rule can invent content the writer never supplied, so the loop
parked the question of what to do with them.

**The real examples.**

*CEDR201 "Mixing Colours".*
- The writer typed — the docx `01-Finalized_Modules_/Inquiry/CEDR201/CEDR201 Writers Template + Media List.docx` (paragraphs 50–113, read directly): `[H1] Mixing Colours` … `Wonder` / `Explore` / `Connect` / `Act [EDIT]` / `Reflect [EDIT] …` … `[Add the following under the first video and content:]` … `[Edit text]Use the tabs, to begin your exploration of colours…` … `[Keep rest of content]` … `EXPLORE` / `[Keep all content but add another dropdown]` … `CONNECT` / `[Edit page]` … `ACT` / `[Keep all content]` … `REFLECT` / `[Edits]` / `Remove first lines of text before 3-2-1. Edit to:`
  Then the blank template — `…/CEDR201 Writers Template + Media List_parsed.txt` from line 12: `[TITLE BAR] MODULE TITLE` / `Adjust the text below to suit your resource.` / `UNDERSTAND` / `In this module you will:` / `• Learning outcome/intention` ×3 …
- The human built — `01-Finalized_Modules_/Inquiry/CEDR201/CEDR201 Mixing Colours.html` (745 lines): lines 24–25 `<h1><span>Mixing colours</span></h1>` / `<h1><span>Te Whakahanumi tae</span></h1>`; lines 67–73 the six crumbs `Intro / Wonder / Explore / Connect / Act / Reflect`; six `inquiryPanel`s, e.g. line 136 `<div class="inquiryPanel" rel="2"> <!-- Wonder -->` / `<p>When we wonder about geometric shapes and artwork, we can consider the influence that culture, people, places can have.</p>` / `<h4>What do I know?</h4>` …
- PageForge builds — `01-Claude_Modules_/Inquiry/CEDR201/CEDR201_0_0.html` (93 lines): line 12 `<h1><span>Tūhono – Ako whakauru | ConnectED</span></h1>`; line 17 `Writers Note: Adjust the text below to suit your resource.`; lines 18–23 `<p>UNDERSTAND</p>` / `<p>In this module you will:</p>` / `<li>Learning outcome/intention</li>` ×3; line 40 `<h3>Lesson # and title</h3>`.
- What a learner sees: gold — the full six-phase inquiry module; PageForge — one page of template
  placeholders ("Learning outcome/intention", "Lesson # and title").

*CEDT202 "Chemical Reactions in Cooking".*
- The writer typed — the docx paragraphs: `Keep Page 3,4, and 5, but take out drag and drop` … `[H1] Chemical Reactions in Cooking` … `[Body – Edit Page – Keep current content including video]` … `WONDER` / `[Body] Keep current content` … `EXPLORE` / `[Keep current content]` … `CONNECT` / `[Edit page]` … `ACT` / `[Keep all content]` … `REFLECT` / `[Edits]`
- The human built — `01-Finalized_Modules_/Inquiry/CEDT202/CEDT202 Chemical Reactions.html` lines 24–25 `<h1><span>Chemical reactions</span></h1>` / `<h1><span>Ngā Tauhohe Matū</span></h1>`, six crumbs, six panels.
- PageForge builds — `01-Claude_Modules_/Inquiry/CEDT202/CEDT202_0_0.html`: `<h1><span>Tūhono – Ako whakauru | ConnectED</span></h1>` and six `Learning outcome/intention` placeholders.

**The numbers.** 8 modules, 8 pages (one page each), scoring 8–20% against their gold. The KB's Inquiry
form (`06_TEMPLATE_RECOGNITION.md` §3.4: crumbs + `inquiryPanel`s) describes the *output*; no KB rule
covers a Writers Template that is an edit brief for content held elsewhere. The authority order cannot
help: there is no source text to apply any rule to.

**The choice.**
- **Option A — treat the brief as the source.** Start the page at the brief's first `[H1]`, derive the
  six crumbs from the ALL-CAPS phase lines, put each edit instruction on the page as a red Writers Note.
  A developer gets a scaffold with the notes in the right phase; a learner would still see a mostly
  empty module (the "kept" content is not in the document). Gate-moving up a little; scoped to 8 modules.
- **Option B — leave them.** The eight pages keep scoring ~10% and keep pulling the average down by
  roughly 0.3pp; nothing changes for anyone.
- **Option C — exclude revision briefs from the comparison set.** The eight stay in the corpus (so a
  developer still gets whatever PageForge can make) but stop counting in the score. No page changes;
  a one-line change to the gate configuration.

**My recommendation is C, with A as an optional follow-up** — these documents are not Writers
Templates in the sense PageForge is built for, so scoring them as if they were only muddies the number;
and A is worth doing only if developers would actually use the phase scaffold + notes. If they would,
say so and the loop can do both.

**Question 6:** Scaffold from the brief (A), leave them (B), or exclude them from the score (C) — and
if C, do you also want A for the developers?

---

## Decision 7 — Word equations are being dropped: which form should PageForge write them in?

**What the issue is.** Writers type maths as real Word equations (Word's equation editor). PageForge's
current document reader never looks at the part of the file where those live (the technical name is
OMML), so **every equation silently vanishes** from the page — the sentence around it survives with a
hole in it. That half is simply a bug and will be fixed the same way whatever you decide. The decision
is the **output form**: the KB says equations are written as **LaTeX** (a text notation MathJax turns
into maths), the human gold uses **MathML** (the browser's native maths markup), and your own PageForge
V1.5 notes record — from six live tests in MTK on 26 August — that in MTK **MathML renders and LaTeX
does not**. Two of your instructions disagree on the form, so the loop did not pick one unattended.
PageForge V1.5 already holds tested converters for both forms.

**The real examples.**

*MXDI102, lesson 1 — an inline fraction in a sentence.*
- The writer typed — `01-Finalized_Modules_/Standard/MXDI102/MXDI102 Writers Template + Media List_parsed.txt` line 152: `🔴[RED TEXT] [body]  [/RED TEXT]🔴This shows that   of 8 is 4.` (the gap is where the Word equation ½ sits; the docx paragraph carries `<m:oMath>` with `1` over `2`)
- The human built — `01-Finalized_Modules_/Standard/MXDI102/MXDI102_2.0.html` lines 42–49: `<p>This shows that` / `<math xmlns="http://www.w3.org/1998/Math/MathML" display="inline">` / `<mfrac>` / `<mn>1</mn>` / `<mn>2</mn>` / `</mfrac>` / `</math>` / `of 8 is 4.</p>`
- PageForge builds — `01-Claude_Modules_/Standard/MXDI102/MXDI102_1_0.html` line 146: `<p>This shows that   of 8 is 4.</p>`
- What a learner sees: gold — "This shows that ½ of 8 is 4."; PageForge — "This shows that  of 8 is 4."

*MXDI102, lesson 1 — the numerator/denominator display.*
- The writer typed — `_parsed.txt` line 124: ` and  is 1 whole which written as an equation is  +  = 1 whole.` (four equations missing)
- The human built — `MXDI102_1.0.html` lines 75–80: `<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">` / `<mfrac>` / `<mn class="primary-text">1</mn>` / `<mn class="secondary-text">2</mn>` / `</mfrac>` / `</math>` (a large coloured ½ beside "Numerator:" / "Denominator:")
- PageForge builds — `MXDI102_1_0.html` line 77: `<p>and  is 1 whole which written as an equation is  +  = 1 whole.</p>`

*PES1008, page 2 — a physics formula on its own line.*
- The writer typed — the docx `…/PES1008/PES1008 Writers Template + Media List.docx` paragraph 330 is a Word equation reading `specific heat capacity c = amount of heat energy (∆E) / (mass × Temp…)`; the `_parsed.txt` shows only the surrounding lines 142–147 (the equation is invisible there).
- The human built — `01-Finalized_Modules_/Standard/PES1008/PES1008_2.0.html` lines 47–65: `<p class="center-text"><math xmlns="http://www.w3.org/1998/Math/MathML">` / `<mtext>specific heat capacity&nbsp;</mtext>` / `<mi>c</mi>` / `<mo>=</mo>` / `<mfrac>` / `<mrow>` / `<mtext>amount of heat energy</mtext>` / `<mi>(<mo>Δ</mo>E)</mi>` / `</mrow>` / `<mrow>` / `<mtext>mass</mtext>` / `<mo>×</mo>` / `<mtext>Temperature rise</mtext>` …
- PageForge builds — `01-Claude_Modules_/Standard/PES1008/PES1008_3_0.html`: the sentence `The temperature of a substance will normally increase if heat Energy is added to it…` is followed straight by `<p>ΔE (sometimes written as ΔQ) is the heat energy transferred…</p>` — the formula the symbols refer to is gone.
- What a learner sees: gold — the formula, centred; PageForge — a definition of symbols for a formula that is not on the page.

**The numbers.** 12 Writers Templates carry **329 Word equations** (MXDI102 154, MXDI301 69, PES1008 24,
MXEX301 18, PES1007 17, MXFU302 15, MXFU401 12, MXDB301 6, MXDI201 6, CEDK401 6, MXDB202 1, SCCH301 1);
PageForge ships **0** maths markup on any page; the gold ships **2,052 `<math>` elements on 94 pages**
(1,822 bare `<math xmlns=…>`, 105 `display="inline"`, 66 `display="block"`). Reachable: ~10 modules /
~80 pages. The `mathJax` body class rides along (the gold carries it on 115 pages / 20 modules).
The KB — `05A_COMP12_13_LANGUAGE_MEDIA.md` lines 217–223: *"MathJax / Equations — Standard LaTeX syntax.
Inline: `\( \)`. Block: `\[ \]`."* with the example `<p>The quadratic formula is \(x = \frac{-b \pm
\sqrt{b^2 - 4ac}}{2a}\)</p>`. Against it — `pageforge-site/CLAUDE.md` lines 93–101: *"What MTK actually
renders (settled 2026-08-26, six live runs …). MathML renders; LaTeX does not. Two MathJax builds collide
on every module page: Brightspace loads … (MathML input only, no TeX) and the Te Kura template then loads
a TeX-capable … which arrives second and is discarded … the downstream Convertor project turns it into
`<math>` before the HTML ships."*
The authority order: the KB is level 1 and says LaTeX — but your V1.5 finding says that output does not
display in MTK, and the gold (level 3) is 100% MathML. Following the KB to the letter would ship
equations learners cannot see.

**The choice.**
- **Option A — MathML** (the gold's form, the one that renders in MTK). ~80 pages gain their
  equations; the KB's 05A page gets a recorded correction (the "KB delta"). Gate-moving up (the gold has
  2,052 of these); scoped regeneration of the 12 modules.
- **Option B — LaTeX** (the KB's letter). The same 80 pages gain text like `\(\frac{1}{2}\)`; on the
  MTK platform, per your own test, learners would see that raw text. Gate-neutral (the gold has no LaTeX
  lines to match).
- **Option C — both:** MathML on the page with the LaTeX source kept in an HTML comment beside it, so
  the KB's notation is preserved for anyone who needs it. Same gate effect as A.

**My recommendation is A** (or C if you want the LaTeX kept for the record), because the point of the
page is that the learner sees the fraction, and your own six-run test settled which form does that.
The KB should then say MathML.

**Question 7:** MathML (A), LaTeX (B), or MathML with the LaTeX kept in a comment (C)?

---

## Decision 8 — Should every text activity box carry the KB's `alertPadding` class?

**What the issue is.** An *activity box* is the shaded panel around a numbered task (`Activity 1A`).
`alertPadding` is an extra style class that adds inner spacing to that panel — a cosmetic choice. The KB's
tag table (01F) maps a plain text/workbook activity to `<div class="activity alertPadding">`, and the
layout page (05B) shows the same in its example — but 05B also says to "follow the activity's own class
set", and the human developers used the plain `activity` on **81%** of text boxes. It is not a numbered
constraint, not a ledger decision, and has no writer-side signal (the writer just types `[Activity 1A]`).
Applying the table would change ~1,700 boxes against the gold's clear majority; the loop would not do
that on the strength of a table row.

**The real examples.**

*ANZH401, lesson 1 — the human used `alertPadding`.*
- The writer typed — `01-Finalized_Modules_/Standard/ANZH401/ANZH401 Writers Template + Media List_parsed.txt` line 98: `🔴[RED TEXT] [Activity Individual - 1A]  [/RED TEXT]🔴Opening and Closing Doors`
- The human built — `01-Finalized_Modules_/Standard/ANZH401/ANZH401_1.0.html` line 77: `<div class="activity alertPadding" number="1A">` / `<h3>Opening and Closing Doors</h3>`
- PageForge builds — `01-Claude_Modules_/Standard/ANZH401/ANZH401_1_0.html` line 50: `<div class="activity" number="1A">` / `<div class="row">` / `<div class="col-12">` / `<h3>Opening and Closing Doors</h3>`
- What a learner sees: the same box with slightly more breathing room around the text on the gold.

*MXFL101, lesson 1 — the human used the plain form.*
- The writer typed — `…/MXFL101/MXFL101 Writers Template + Media List_parsed.txt` line 119: `🔴[RED TEXT] [Activity 1B]  [/RED TEXT]🔴Activities`
- The human built — `01-Finalized_Modules_/Standard/MXFL101/MXFL101_1.0.html` line 183: `<div class="activity" number="1B">` / `<div class="col-md-8 col-12">` / `<h3>Activities</h3>`
- PageForge builds — `01-Claude_Modules_/Standard/MXFL101/MXFL101_1_0.html` line 99: `<div class="activity" number="1B">` / … / `<h3>Activities</h3>` — identical class.

*HIS1005, lesson 1 — plain form again (`01-Finalized_Modules_/Standard/HIS1005/HIS1005-1.0.html` line 54: `<div class="activity" number="1A">`; PageForge the same).*

**The numbers** (measured inline, session 6): gold non-interactive boxes — plain `activity` **1,773** vs
`activity alertPadding` **411** (0.19); interactive boxes 2,213 plain vs 160 padded; dropbox boxes 439.
PageForge ships plain `activity` on every text box. Applying the table = a named override on ~1,700
boxes, skeleton ≈ −0.5pp on every plain-`activity` gold page.
The KB — `01F_TAG_INTERPRETATION_STYLING_ACTIVITIES.md` line 27: `| activity + ID (text/workbook) |
<div class="activity alertPadding" number="ID"> |`; `05B_COMP14_LAYOUT_STRUCTURE.md` line 39
`<!-- Standard text activity --> <div class="activity alertPadding" number="1D">`, but line 50: *"Do not
force `alertPadding` onto a dropbox activity — follow the activity's own class set and simply append
`dropbox`."* The authority order: a component-doc mapping is arguably level 1, but the gold contradicts it
4:1 and the KB's own wording treats it as "the activity's own class set", i.e. a per-activity choice.

**The choice.**
- **Option A — apply `alertPadding` to every text/workbook activity.** ~1,700 boxes gain the padding;
  a named override with a ≈ −0.5pp skeleton dip; full regeneration.
- **Option B — leave the plain form** (the gold's 81% and 05B's "own class set"). No change.
- **Option C — first make it a numbered KB constraint, then apply it** (A, but with the rulebook
  updated so the override is on the record).

**My recommendation is B**, because `alertPadding` is a developer's padding choice with no writer-side
trigger, the gold is 4:1 against, and the KB itself calls it part of the activity's "own class set"
rather than a rule. If the design team wants the padded look on every text box, C is the clean way.

**Question 8:** Pad every text activity (A), leave plain (B), or make it a KB rule first then apply (C)?

---

## Decision 9 — The lesson-menu labels ("We are learning:" / "I can:"): apply the KB's `<h5>` form everywhere? (KB constraint 23)

**What the issue is.** Every lesson page opens with a small menu holding the learning intentions and
success criteria. The KB (constraint 23, "CRITICAL" in 01B) says those labels are **`<h5>` headings
normalised to standard wording** — `We are learning:` and `I can:` (or `You will show your understanding
by:` for years 1–6) — whatever the writer typed, with **no** separate "Learning intentions" title above
them. PageForge already ships `<h5>` on 1,257 labels (the human agrees 71% of the time). The residue is
206 labels on 176 pages / 42 modules where PageForge ships a plain `<p>` — either because the writer's
wording is a variant its phrase list does not know ("We are learning about…", "Ākonga will:") or because
an older rule (r81) deliberately keeps `<p>` in the English family and on the overview page, where the
human developers used `<p>` 80% of the time. On that residue the human is split **by series**: NCEA1 h5
95%, English h5/h3/p roughly thirds, Mathematics and ConnectED mostly `<p>`. The KB also makes the
**overview** tab's labels `<h5>` — overturning a convention the gold carries at 0.80 on ~296 overview
pages. Whether the KB's wording is meant to overturn that is a design-team call, so the loop stopped.

**The real examples.**

*ENGI202, lesson 1 (English — the human used `<h5>`, PageForge `<p>`).*
- The writer typed — `01-Finalized_Modules_/Standard/ENGI202/ENGI202 Writers Template + Media List_parsed.txt` lines 133–145: `🔴[RED TEXT] [Lesson Overview] [/RED TEXT]🔴` / `We are learning to:` / `• read, listen to and view stories from a variety of different cultures` … / `You will show your understanding by:` / `• reading five traditional stories` …
- The human built — `01-Finalized_Modules_/Standard/ENGI202/ENGI202_1.0.html` lines 76 and 81: `<h5>We are learning to:</h5>` … `<h5>You will show your understanding by:</h5>`
- PageForge builds — `01-Claude_Modules_/Standard/ENGI202/ENGI202_1_0.html` inside `#module-menu-content`: `<p>We are learning to:</p>` … `<p>You will show your understanding by:</p>`
- What a learner sees: gold — two small bold labels over the bullet lists; PageForge — the same words
  as ordinary text. (Note neither side used the KB's normalised wording `We are learning:` here.)

*MXDB202, lesson 1 (Mathematics — the human normalised the wording as the KB asks).*
- The writer typed — `…/MXDB202/MXDB202 Writers Template + Media List_parsed.txt` lines 39–41: `[H2] **Paearu Angitu | How will I know if I've learned it?**` / `*Ākonga will:*` / `• use different multiplication strategies…`
- The human built — `01-Finalized_Modules_/Standard/MXDB202/MXDB202_1.0.html` lines 40–41 and 48–49: `<h3><span>Learning Intentions</span></h3>` / `<h5>We are learning to:</h5>` … `<h3><span>How will I know if I've learned it? </span></h3>` / `<h5>I can:</h5>`
- PageForge builds — `01-Claude_Modules_/Standard/MXDB202/MXDB202_1_0.html` lines 32–33 and 40–41: `<h5>Learning Intentions</h5>` / `<p>Ākonga can:</p>` … `<h5>How will I know if I've learned it?</h5>` / `<p>Ākonga will:</p>`
- What a learner sees: gold — "I can:" as a label; PageForge — "Ākonga will:" as plain text under a
  heading. (The KB would have neither side's section titles, just `<h5>We are learning:</h5>` and
  `<h5>I can:</h5>`.)

*CEDT501, lesson 1 (ConnectED — the human kept `<p>`, and both sides add a title the KB forbids).*
- The writer typed — `01-Finalized_Modules_/Standard/CEDT501/CEDT501 Writers Template_parsed.txt` lines 162–172: `🔴[RED TEXT] [Lesson Overview]  [/RED TEXT]🔴` / `We are learning:` / `• to recognise examples of online bullying…` / `I can:` / `• reflect on and record my online activity` …
- The human built — `01-Finalized_Modules_/Standard/CEDT501/CEDT501_1.0.html` from line 23: `<h5>Learning intentions</h5>` / `<p>We are learning:</p>` / `<ul>…</ul>` / `<h5>How will I know if I've learned it?</h5>` / `<p>I can:</p>`
- PageForge builds — `01-Claude_Modules_/Standard/CEDT501/CEDT501_1_0.html` from line 22: `<h5>Learning intentions</h5>` / `<p>We are learning:</p>` / `<ul>…</ul>` / `<h5>I can:</h5>`
- What a learner sees: near-identical; the KB's form would drop "Learning intentions" and make
  "We are learning:" the bold label.

**The numbers** (`outputs/_r341_menulabels.log`, measured inside `#module-menu-content` on every paired
lesson page): 1,491 PageForge labels on 690 pages / 127 modules; PageForge `<h5>` 1,257 (gold h5 0.71);
PageForge `<p>` **206 labels / 176 pages / 42 modules** (gold h5 0.35, p 0.39). Of the `<p>` residue: gold
`<h5>` on 59 labels / 56 pages / 15 modules (the pages that would improve); gold keeps `<p>` on 80 labels /
80 pages / 20 modules (English 22, ConnectED 20, Mathematics 17, Online Safety 16, Leaving to Learn 5 —
the pages a KB override would dip). By series on the residue: NCEA1 h5 0.95; English h5 27 / h3 24 /
p 22; Mathematics p; ConnectED p 20 / h5 5. The Online Safety "Ākonga will…" sentences are a lead-in
paragraph the KB itself says is a `<p>` (constraint 70) — PageForge is right there. One variant, "We are
learning about/to…", solidifies at 0.69 (17 pages — under the floor).
The KB — `00D_CONSTRAINTS_1.md` constraint 23: *"Lesson page module menus use `<h5>` label headings
normalised to standard patterns (e.g., `<h5>We are learning:</h5>` + `<h5>I can:</h5>`) — NOT writer's
verbatim text, NOT `<h4>` headings, NOT intermediate `<p>` elements"*; `01B_MODULE_MENUS_FOOTER.md`
line 223: *"Lesson pages use a simplified module menu with `<h5>` headings as label text. The `<h5>`
heading IS the label text — do NOT add separate section titles (e.g., "Learning intentions") above
these"*; lines 240–244 the by-level table (`We are learning:` + `You will show your understanding by:`
for years 1–6; `We are learning:` + `I can:` for 7–10); line 246 *"Label Normalisation: Regardless of
what label text the writer uses …"*; and lines 196–197 the overview-tab row: *"Overview tab — "We are
learning:" / "I can:" labels → `<h5>…</h5>` (no span)"*.
The authority order: level 1 — the KB has an explicit, universal rule → apply it, overriding the gold's
per-series split. The loop stopped only because the same rule reaches the overview tab (~296 pages at a
0.80 gold convention) and it would not overturn that unattended.

**The choice.**
- **Option A — apply constraint 23 everywhere:** every lesson-menu label becomes `<h5>` with the KB's
  normalised wording, the section titles above them go, and the overview tab's labels become `<h5>` too.
  ~80 lesson pages + ~296 overview pages change. A named KB-over-gold override, skeleton ≈ −0.1pp; close
  to a full regeneration (the menu is on every page).
- **Option B — lesson menus only:** the ~80 lesson pages, keeping today's overview form. Roughly a
  wash on the score (≈ 60 pages up, ≈ 80 named down); scoped regeneration.
- **Option C — leave it,** adding only the one variant that solidified ("We are learning about/to…",
  17 pages). The KB rule stays partly un-honoured.

**My recommendation is A**, because the rule is the KB's most explicit "CRITICAL" instruction, the
authority order exists precisely so the rulebook beats the older gold, and the cost is a small, named
dip on pages that new modules will never be judged against. The only reason to choose B instead is if the
overview-tab row (01B lines 196–197) is not what the design team intends — you are the one who knows.

**Question 9:** The KB's `<h5>` label form everywhere including the overview tab (A), lesson menus only
(B), or leave it (C)?

---

## Not a decision for you — for completeness

The session-9 Round 2 work (engine r342, the "hyperlinked media tag" rule) is built and switched OFF with
four files uncommitted; its open point ("gap 2", where an audio/video tag's own bracket text is dropped)
is the loop's own call to settle by measurement, not yours. `/loop-start` will pick it up.

---

## The questions in one place

1. **Duplicate opening heading (c47):** apply in full (A), only the `Lesson N:` form (B), or leave (C)? — *I recommend A.*
2. **Bilingual lesson-title order in Standard modules:** writer's order (A), English first (B), Māori first (C)? — *I recommend A.*
3. **Building the un-built interactives:** widget-build rounds in the loop (A), leave to the downstream path (B), only the three builder-less types (C)? — *I recommend B, or C if you want builds.*
4. **stickyNav:** KB families only (A), every ≥ 60% series (B), keep the ban (C)? — *I recommend A.*
5. **Table style:** bordered everywhere per 05D (A), bordered where the family agrees (B), leave plain (C)? and which KB page is right? — *I recommend B.*
6. **CED revision briefs:** scaffold from the brief (A), leave (B), exclude from the score (C)? — *I recommend C (+ A if developers want the scaffold).*
7. **Equations:** MathML (A), LaTeX (B), MathML + LaTeX in a comment (C)? — *I recommend A.*
8. **alertPadding on text activities:** apply (A), leave plain (B), make it a KB rule first (C)? — *I recommend B.*
9. **Lesson-menu labels (c23):** KB `<h5>` form everywhere (A), lesson menus only (B), leave (C)? — *I recommend A.*

Answer in any order, as many or as few as you like; each answer is recorded in `LOOP_STATE.md` under
"Decisions from Chris" the moment it is given, and `/loop-start` actions the recorded ones next session.
