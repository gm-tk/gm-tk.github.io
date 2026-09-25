# DIFF_QUEUE.md — the diff miner's ranked class queue (LOOP__Autonomous_Rounds.md §1d)

**Produced:** 2026-09-25 21:43 NZST by `reference/tests/_diff_miner.py` on the CURRENT corpus (pageforge-site HEAD 840467b; Claude corpus 545 dirs). **Population:** the skeleton gate's own — 41 paired pages / 5 modules (compare_exclusions.txt honoured; acks / glossary / references pages excluded); parse errors skipped: 0 (must be 0); modules without a parsed WT: 0. Run time 3.3 s.

**What a row is.** One CLASS = (region, parent element, gold form, Claude form, direction) over every differing skeleton line of every paired page — the same lines, labels, widget collapse and difflib alignment the PRIMARY gate scores (each element its own line so it can be quoted). Direction: MISSING = gold has it, Claude lacks it; EXTRA = Claude has it, gold lacks it; SUBSTITUTED = same position, different tag / class / wrapper; MOVED = same text, different place. Consensus = of the gold pages in the group where the region exists, the share carrying the gold form (for EXTRA: the share NOT carrying Claude's form). Derivable = the gold line's text is in the module's parsed Writers Template (round-110 tolerance); structure-only differences are always derivable.

**Candidate rule (§1d).** modules ≥ 10 for a chrome class (module-code / title / header / module-menu / crumbs / phases-nav / footer / acks), pages ≥ 20 for a body / activity class; gold consensus ≥ 0.60 in at least one template or subject group that itself reaches the floor; structure-only or derivable share ≥ 0.60. A class below the floor is listed, never dropped. A CANDIDATE still goes through the PICK's KB-first check, the triangulation and the §3 corpus-wide measurement before any code — this table is the queue, not the verdict.

## Summary

- differing skeleton lines: 6690 — by direction {'EXTRA': 2833, 'SUBSTITUTED': 558, 'MISSING': 2961, 'MOVED': 338}
- by region: {'title': 1, 'module-menu': 168, 'footer': 33, 'acks': 17, 'activity': 2051, 'body': 4406, 'root': 14}
- classes: 656 — CANDIDATE 3, below floor 652, the rest below consensus / not derivable

## Completeness census — the repeating chrome (§1d item 4)

| region | pages with region | gold items | gold items in WT | Claude items | derivable misses | pages with misses | modules with misses | status |
|---|---|---|---|---|---|---|---|---|
| module-menu | 12 | 190 | 190 | 150 | 57 | 8 | 2 | BELOW FLOOR |
| crumbs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |
| phases-nav | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |
| footer | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |

- **module-menu** by template: Standard 2m/8p/57 misses
  - XGF9004 XGF9004_1_0.html: gold 15 items (15 in WT) / Claude 0 — 15 derivable misses, e.g. p «We are learning:» · li «to explore and understand key philosophical concepts such as fairness, truth, an»
  - XGF9006 XGF9006_1_0.html: gold 6 items (6 in WT) / Claude 0 — 6 derivable misses, e.g. p «We are learning:» · li «what Genius Hour is and how it helps us follow our passions»
  - XGF9006 XGF9006_2_0.html: gold 6 items (6 in WT) / Claude 0 — 6 derivable misses, e.g. p «We are learning:» · li «how to explore what we care about and what excites us»
  - XGF9006 XGF9006_3_0.html: gold 6 items (6 in WT) / Claude 0 — 6 derivable misses, e.g. p «We are learning:» · li «how to ask big, interesting questions»
- **crumbs** by template: 
- **phases-nav** by template: 
- **footer** by template: 

## Chrome facts — the header and footer as SETS per page (alignment-free; §1d items 2 + 4)

A fact is one thing a page's chrome has: `header:chip` (the `#module-code` div), `header:chip=module-code` / `=lesson-number` / `=lesson-number(00)`, `header:head-buttons`, `header:menu-content`, `header:title-h1-count=N`, `footer:present`, `footer:ul=<classes>`, `footer:link=prev-lesson` / `next-lesson` / `home-nav`, `footer:links=<order>`, `footer:inside-body`, `nav:crumbs`, `nav:phases`. MISSING = the gold page has the fact and Claude's does not; EXTRA the reverse. Consensus = the share of gold pages in the group that have (MISSING) / lack (EXTRA) the fact. Floor 10 modules.

| # | dir | fact | pages | modules | gold share (all) | consensus (all) | best group | status |
|---|---|---|---|---|---|---|---|---|
| F1 | EXTRA | `header:head-buttons` | 2 | 2 | 0.49 | 0.51 | — | BELOW FLOOR |
| F2 | EXTRA | `header:menu-content` | 2 | 2 | 0.49 | 0.51 | — | BELOW FLOOR |
| F3 | MISSING | `header:chip=decimal-number` | 1 | 1 | 0.90 | 0.90 | — | BELOW FLOOR |
| F4 | EXTRA | `header:chip=module-code` | 1 | 1 | 0.10 | 0.90 | — | BELOW FLOOR |
| F5 | MISSING | `header:title-h1-count=1` | 1 | 1 | 0.88 | 0.88 | — | BELOW FLOOR |
| F6 | MISSING | `header:head-buttons` | 1 | 1 | 0.49 | 0.49 | — | BELOW FLOOR |
| F7 | MISSING | `header:menu-content` | 1 | 1 | 0.49 | 0.49 | — | BELOW FLOOR |
| F8 | EXTRA | `header:title-h1-count=2` | 1 | 1 | 0.12 | 0.88 | — | BELOW FLOOR |
| F9 | MISSING | `header:title-h1-count=2` | 1 | 1 | 0.12 | 0.12 | — | BELOW FLOOR |
| F10 | EXTRA | `header:title-h1-count=1` | 1 | 1 | 0.88 | 0.12 | — | BELOW FLOOR |
| F11 | EXTRA | `footer:links=next-lesson,home-nav` | 5 | 5 | 0.00 | 1.00 | — | BELOW FLOOR |
| F12 | MISSING | `footer:links=home-nav,next-lesson` | 4 | 4 | 0.10 | 0.10 | — | BELOW FLOOR |
| F13 | MISSING | `footer:links=prev-lesson,next-lesson,home-nav` | 1 | 1 | 0.78 | 0.78 | — | BELOW FLOOR |
| F14 | MISSING | `footer:link=prev-lesson` | 1 | 1 | 0.90 | 0.90 | — | BELOW FLOOR |
| F15 | MISSING | `footer:links=prev-lesson,home-nav` | 1 | 1 | 0.12 | 0.12 | — | BELOW FLOOR |
| F16 | EXTRA | `footer:links=prev-lesson,next-lesson,home-nav` | 1 | 1 | 0.78 | 0.22 | — | BELOW FLOOR |
| F17 | EXTRA | `footer:link=next-lesson` | 1 | 1 | 0.88 | 0.12 | — | BELOW FLOOR |
| F18 | MISSING | `footer:inside-body` | 1 | 1 | 0.02 | 0.02 | — | BELOW FLOOR |


## The ranked queue — chrome regions first, then by modules affected

| # | region | dir | parent | gold form | Claude form | pages | modules | consensus (all) | best group | derivable | KB | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | title | MISSING | `div#header` | `h1>span` | `—` | 1 | 1 | 0.12 of 41 | — | 0.00 | yes | BELOW FLOOR |
| 2 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-6.paddingR` | 4 | 4 | 1.00 of 41 | — | structure | yes | BELOW FLOOR |
| 3 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6` | `div.col-12.col-md-12.paddingR` | 4 | 4 | 0.10 of 41 | — | structure | yes | BELOW FLOOR |
| 4 | module-menu | SUBSTITUTED | `div.col-12.col-md-6` | `h4>span` | `h5>span` | 4 | 4 | 0.10 of 41 | — | structure | yes | BELOW FLOOR |
| 5 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingL` | `p` | `h5` | 4 | 4 | 0.10 of 41 | — | structure | yes | BELOW FLOOR |
| 6 | module-menu | EXTRA | `p>b` | `—` | `b` | 3 | 3 | 1.00 of 41 | — | structure | — | BELOW FLOOR |
| 7 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.paddingL` | `div.col-12.col-md-6.paddingR` | 3 | 3 | 0.10 of 41 | — | structure | yes | BELOW FLOOR |
| 8 | module-menu | EXTRA | `div#header` | `—` | `div#module-head-buttons` | 2 | 2 | 0.51 of 41 | — | structure | yes | BELOW FLOOR |
| 9 | module-menu | EXTRA | `div#header` | `—` | `div#module-menu-content.moduleMenu` | 2 | 2 | 0.51 of 41 | — | structure | yes | BELOW FLOOR |
| 10 | module-menu | MISSING | `div.col-12.col-md-6` | `h4>span` | `—` | 2 | 2 | 0.10 of 41 | — | 1.00 | yes | BELOW FLOOR |
| 11 | module-menu | MOVED | `div.col-12.col-md-6` | `p` | `p` | 2 | 2 | 0.07 of 41 | — | structure | yes | BELOW FLOOR |
| 12 | module-menu | MISSING | `div.col-12.col-md-12` | `WIDGET` | `—` | 8 | 1 | 0.20 of 41 | — | structure | — | BELOW FLOOR |
| 13 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-12` | `WIDGET` | 8 | 1 | 0.20 of 41 | — | structure | — | BELOW FLOOR |
| 14 | module-menu | MISSING | `div.col-12.col-md-8` | `p` | `—` | 7 | 1 | 0.20 of 41 | — | 1.00 | — | BELOW FLOOR |
| 15 | module-menu | MISSING | `div.col-12.col-md-8` | `ul` | `—` | 7 | 1 | 0.20 of 41 | — | 1.00 | — | BELOW FLOOR |
| 16 | module-menu | EXTRA | `h4>span` | `—` | `span` | 1 | 1 | 0.90 of 41 | — | structure | — | BELOW FLOOR |
| 17 | module-menu | EXTRA | `h5>span` | `—` | `span` | 1 | 1 | 1.00 of 41 | — | structure | — | BELOW FLOOR |
| 18 | module-menu | MISSING | `div.col-12.col-md-6` | `p` | `—` | 1 | 1 | 0.07 of 41 | — | 1.00 | yes | BELOW FLOOR |
| 19 | module-menu | MISSING | `ul` | `li>b` | `—` | 1 | 1 | 0.05 of 41 | — | 1.00 | — | BELOW FLOOR |
| 20 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6.paddingL` | `—` | 1 | 1 | 0.10 of 41 | — | 1.00 | yes | BELOW FLOOR |
| 21 | module-menu | MISSING | `div#module-head-buttons` | `div#module-menu-button.btn1.circle-button` | `—` | 1 | 1 | 0.49 of 41 | — | structure | yes | BELOW FLOOR |
| 22 | module-menu | MISSING | `div#header` | `div#module-menu-content.moduleMenu` | `—` | 1 | 1 | 0.49 of 41 | — | 1.00 | yes | BELOW FLOOR |
| 23 | module-menu | SUBSTITUTED | `div.col-12.col-md-6` | `ul` | `p` | 1 | 1 | 0.10 of 41 | — | structure | yes | BELOW FLOOR |
| 24 | module-menu | SUBSTITUTED | `div#header` | `div#module-head-buttons` | `h1>span` | 1 | 1 | 0.49 of 41 | — | structure | yes | BELOW FLOOR |
| 25 | footer | EXTRA | `li>a#next-lesson` | `—` | `a#next-lesson` | 5 | 4 | 0.12 of 41 | — | structure | yes | BELOW FLOOR |
| 26 | footer | EXTRA | `ul.footer-nav` | `—` | `li>a.home-nav` | 5 | 4 | 0.00 of 41 | — | structure | yes | BELOW FLOOR |
| 27 | footer | MISSING | `ul.footer-nav` | `li>a#next-lesson` | `—` | 4 | 4 | 0.88 of 41 | — | structure | yes | BELOW FLOOR |
| 28 | footer | EXTRA | `body.container-fluid` | `—` | `div#footer` | 2 | 1 | 0.05 of 41 | — | structure | yes | BELOW FLOOR |
| 29 | footer | MISSING | `ul.footer-nav` | `li>a#prev-lesson` | `—` | 1 | 1 | 0.90 of 41 | — | structure | yes | BELOW FLOOR |
| 30 | footer | MISSING | `div#body` | `div#footer` | `—` | 1 | 1 | 0.02 of 41 | — | structure | yes | BELOW FLOOR |
| 31 | acks | MISSING | `div.acks` | `WIDGET` | `—` | 1 | 1 | 0.10 of 41 | — | structure | yes | BELOW FLOOR |
| 32 | acks | SUBSTITUTED | `div.col-12.col-md-8` | `div.acks.acksAI.acksTemplate` | `div.acks.acksTemplate` | 1 | 1 | 0.02 of 41 | — | structure | yes | BELOW FLOOR |
| 33 | acks | SUBSTITUTED | `div.col-12.col-md-8` | `div.acks` | `h3` | 1 | 1 | 0.10 of 41 | — | structure | yes | BELOW FLOOR |
| 34 | activity | MISSING | `div.col-12` | `p` | `—` | 20 | 5 | 0.56 of 41 | ptype=lesson c=0.64 n=20 | 1.00 | — | CANDIDATE |
| 35 | activity | MISSING | `div.col-12` | `WIDGET` | `—` | 19 | 5 | 0.41 of 41 | — | structure | — | BELOW FLOOR |
| 36 | activity | EXTRA | `div.col-12` | `—` | `WIDGET` | 9 | 5 | 0.44 of 41 | — | structure | — | BELOW FLOOR |
| 37 | activity | MOVED | `div.col-12` | `p` | `p` | 17 | 4 | 0.29 of 41 | — | structure | — | BELOW FLOOR |
| 38 | activity | MOVED | `div.col-12` | `h4.goJournal` | `h4.goJournal` | 17 | 4 | 0.37 of 41 | — | structure | — | BELOW FLOOR |
| 39 | activity | EXTRA | `div.col-12` | `—` | `p` | 11 | 4 | 0.71 of 41 | — | structure | — | BELOW FLOOR |
| 40 | activity | MISSING | `div.col-12` | `h3` | `—` | 8 | 4 | 0.29 of 41 | — | 0.56 | — | BELOW FLOOR |
| 41 | activity | EXTRA | `div.col-12` | `—` | `p>b` | 7 | 4 | 0.95 of 41 | — | structure | — | BELOW FLOOR |
| 42 | activity | MISSING | `div.col-12` | `h4` | `—` | 7 | 4 | 0.15 of 41 | — | 0.60 | — | BELOW FLOOR |
| 43 | activity | MISSING | `div.activity.interactive[number=*]` | `div.row` | `—` | 7 | 4 | 0.39 of 41 | — | 1.00 | yes | BELOW FLOOR |
| 44 | activity | MISSING | `div.col-12` | `h4.goJournal` | `—` | 8 | 3 | 0.78 of 41 | — | 0.25 | — | BELOW FLOOR |
| 45 | activity | MOVED | `ul` | `li` | `li` | 8 | 3 | 0.15 of 41 | — | structure | — | BELOW FLOOR |
| 46 | activity | MISSING | `a` | `div.button` | `—` | 7 | 3 | 0.27 of 41 | — | 0.57 | yes | BELOW FLOOR |
| 47 | activity | MOVED | `div.col-12` | `h3` | `h3` | 7 | 3 | 0.61 of 41 | — | structure | — | BELOW FLOOR |
| 48 | activity | MOVED | `div.col-12` | `p` | `p` | 7 | 3 | 0.56 of 41 | — | structure | — | BELOW FLOOR |
| 49 | activity | MISSING | `div.col-12` | `div.row` | `—` | 6 | 3 | 0.10 of 41 | — | 1.00 | — | BELOW FLOOR |
| 50 | activity | MISSING | `p>span.highlight` | `span.highlight` | `—` | 5 | 3 | 0.15 of 41 | — | 0.83 | yes | BELOW FLOOR |
| 51 | activity | MOVED | `div.col-12` | `h3` | `h3` | 5 | 3 | 0.61 of 41 | — | structure | — | BELOW FLOOR |
| 52 | activity | SUBSTITUTED | `div.row` | `div.col-12` | `div.col-12.col-md-8` | 5 | 3 | 0.78 of 41 | — | structure | — | BELOW FLOOR |
| 53 | activity | EXTRA | `p>a` | `—` | `a` | 4 | 3 | 1.00 of 41 | — | structure | — | BELOW FLOOR |
| 54 | activity | MISSING | `div.col-12` | `ul` | `—` | 4 | 3 | 0.17 of 41 | — | 0.43 | — | BELOW FLOOR |
| 55 | activity | MOVED | `div.col-12` | `h4.goJournal` | `h4.goJournal` | 4 | 3 | 0.24 of 41 | — | structure | — | BELOW FLOOR |
| 56 | activity | EXTRA | `div.activity.interactive[number=*]` | `—` | `div.row` | 3 | 3 | 0.61 of 41 | — | structure | yes | BELOW FLOOR |
| 57 | activity | EXTRA | `div.activity[number=*]` | `—` | `div.row` | 3 | 3 | 0.73 of 41 | — | structure | yes | BELOW FLOOR |
| 58 | activity | MISSING | `div.col-12` | `img.img-fluid` | `—` | 3 | 3 | 0.20 of 41 | — | structure | — | BELOW FLOOR |
| 59 | activity | MISSING | `div.col-12` | `p>b` | `—` | 3 | 3 | 0.39 of 41 | — | 0.80 | — | BELOW FLOOR |
| 60 | activity | SUBSTITUTED | `div.col-12` | `p` | `p` | 7 | 2 | 0.78 of 41 | — | structure | — | BELOW FLOOR |
| 61 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.alertPadding[number=*]` | `div.activity[number=*]` | 5 | 2 | 0.37 of 41 | — | structure | yes | BELOW FLOOR |
| 62 | activity | EXTRA | `p>i` | `—` | `i` | 4 | 2 | 1.00 of 41 | — | structure | — | BELOW FLOOR |
| 63 | activity | MISSING | `div.col-12` | `ol` | `—` | 4 | 2 | 0.27 of 41 | — | 1.00 | — | BELOW FLOOR |
| 64 | activity | MOVED | `ol` | `li` | `li` | 4 | 2 | 0.17 of 41 | — | structure | — | BELOW FLOOR |
| 65 | activity | SUBSTITUTED | `div.col-12` | `h3` | `h3` | 4 | 2 | 0.78 of 41 | — | structure | — | BELOW FLOOR |
| 66 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.alertPadding[number=*]` | `p` | 4 | 2 | 0.37 of 41 | — | structure | yes | BELOW FLOOR |
| 67 | activity | EXTRA | `div.col-12` | `—` | `p>i` | 3 | 2 | 1.00 of 41 | — | structure | — | BELOW FLOOR |
| 68 | activity | EXTRA | `p>b` | `—` | `b` | 3 | 2 | 0.61 of 41 | — | structure | — | BELOW FLOOR |
| 69 | activity | EXTRA | `div.col-12` | `—` | `div.activity.interactive[number=*]` | 3 | 2 | 0.81 of 41 | — | structure | yes | BELOW FLOOR |
| 70 | activity | MISSING | `div.col-12` | `div.flipCardsContainer.row` | `—` | 3 | 2 | 0.17 of 41 | — | structure | — | BELOW FLOOR |
| 71 | activity | MISSING | `div.col-12` | `a` | `—` | 3 | 2 | 0.17 of 41 | — | 0.89 | — | BELOW FLOOR |
| 72 | activity | MOVED | `div.col-12` | `h4` | `h4` | 3 | 2 | 0.15 of 41 | — | structure | — | BELOW FLOOR |
| 73 | activity | MOVED | `div.row` | `h4.goJournal` | `h4.goJournal` | 3 | 2 | 0.07 of 41 | — | structure | — | BELOW FLOOR |
| 74 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `div.activity.interactive[number=*]` | 3 | 2 | 0.34 of 41 | — | structure | yes | BELOW FLOOR |
| 75 | activity | EXTRA | `div.col-12.col-md-8` | `—` | `div.activity[number=*]` | 2 | 2 | 0.95 of 41 | — | structure | yes | BELOW FLOOR |
| 76 | activity | EXTRA | `div.col-12.col-md-8` | `—` | `div.activity.interactive[number=*]` | 2 | 2 | 0.90 of 41 | — | structure | yes | BELOW FLOOR |
| 77 | activity | EXTRA | `div.col-12` | `—` | `ul` | 2 | 2 | 0.98 of 41 | — | structure | — | BELOW FLOOR |
| 78 | activity | EXTRA | `p` | `—` | `b` | 2 | 2 | 0.98 of 41 | — | structure | — | BELOW FLOOR |
| 79 | activity | MISSING | `div.activity.interactive[number=*]` | `WIDGET` | `—` | 2 | 2 | 0.05 of 41 | — | structure | yes | BELOW FLOOR |
| 80 | activity | MISSING | `div.row` | `div.col-12` | `—` | 2 | 2 | 0.32 of 41 | — | 1.00 | — | BELOW FLOOR |
| 81 | activity | MISSING | `div.activity[number=*]` | `div.row` | `—` | 2 | 2 | 0.05 of 41 | — | 1.00 | yes | BELOW FLOOR |
| 82 | activity | MISSING | `ul` | `li` | `—` | 2 | 2 | 0.22 of 41 | — | 1.00 | — | BELOW FLOOR |
| 83 | activity | MISSING | `p>b` | `b` | `—` | 2 | 2 | 0.07 of 41 | — | 1.00 | — | BELOW FLOOR |
| 84 | activity | MISSING | `div.col-12` | `div.clickDropContent` | `—` | 2 | 2 | 0.02 of 41 | — | 1.00 | — | BELOW FLOOR |
| 85 | activity | MOVED | `div.col-12.col-md-8` | `h3` | `h3` | 2 | 2 | 0.12 of 41 | — | structure | — | BELOW FLOOR |
| 86 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.alertPadding.interactive[number=*]` | `div.activity[number=*]` | 2 | 2 | 0.15 of 41 | — | structure | yes | BELOW FLOOR |
| 87 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `div.row` | 2 | 2 | 0.73 of 41 | — | structure | — | BELOW FLOOR |
| 88 | activity | SUBSTITUTED | `div.col-12` | `div.activity.interactive[number=*]` | `p` | 2 | 2 | 0.20 of 41 | — | structure | yes | BELOW FLOOR |
| 89 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `p` | 2 | 2 | 0.49 of 41 | — | structure | yes | BELOW FLOOR |
| 90 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `p` | 2 | 2 | 0.34 of 41 | — | structure | yes | BELOW FLOOR |
| 91 | activity | SUBSTITUTED | `div.col-12.col-md-12` | `div.activity.interactive[number=*]` | `h4` | 2 | 2 | 0.24 of 41 | — | structure | yes | BELOW FLOOR |
| 92 | activity | MISSING | `a` | `div.externalButton` | `—` | 5 | 1 | 0.17 of 41 | — | 1.00 | — | BELOW FLOOR |
| 93 | activity | MOVED | `a` | `div.externalButton` | `div.externalButton` | 5 | 1 | 0.17 of 41 | — | structure | — | BELOW FLOOR |
| 94 | activity | SUBSTITUTED | `a` | `div.externalButton` | `div.externalButton` | 5 | 1 | 0.24 of 41 | — | structure | — | BELOW FLOOR |
| 95 | activity | SUBSTITUTED | `ol` | `li` | `li` | 5 | 1 | 0.29 of 41 | — | structure | — | BELOW FLOOR |
| 96 | activity | MISSING | `div.col-12` | `h5` | `—` | 4 | 1 | 0.07 of 41 | — | 1.00 | — | BELOW FLOOR |
| 97 | activity | MISSING | `div.col-12` | `div.row.selectionBox` | `—` | 3 | 1 | 0.15 of 41 | — | 1.00 | — | BELOW FLOOR |
| 98 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `div.activity[number=*]` | 3 | 1 | 0.34 of 41 | — | structure | yes | BELOW FLOOR |
| 99 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `h3` | 3 | 1 | 0.49 of 41 | — | structure | yes | BELOW FLOOR |
| 100 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `div.activity.interactive[number=*]` | 3 | 1 | 0.49 of 41 | — | structure | yes | BELOW FLOOR |
| 286 | body | EXTRA | `div#body` | `—` | `div.row` | 35 | 5 | 0.81 of 41 | template=Standard c=0.81 n=35 | structure | — | CANDIDATE |
| 288 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 27 | 5 | 0.93 of 41 | ptype=lesson c=0.94 n=26 | structure | — | CANDIDATE |

## Details — in the companion file `CONVERTER_V2/outputs/_diff_queue_details.md`
Every CANDIDATE and every top-40 row has three quoted examples (WT / gold / Claude) there, plus the
below-floor list. **NEVER read the companion whole** (hundreds of KB): `grep -n '^### #<rank> ' CONVERTER_V2/outputs/_diff_queue_details.md` then `sed -n '<start>,<start+40>p'`. The top 25
candidates' detail blocks are repeated below for convenience.

### #34 · activity · MISSING · `div.col-12` › gold `p` vs Claude `—` — CANDIDATE
- pages 20 / modules 5 / lines 43; consensus (all) 0.56 of 41 gold pages with the region; derivable 1.00 (0 lines with no WT source)
- by template: Standard 5m/20p c=0.56
- by subject: Leaving to Learn 5m/20p c=0.56
- by era: Refresh 5m/20p c=0.56
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **XGF9001** XGF9001_3_0.html ↔ XGF9001-01.3.html (content, derivable=True)
  - gold: `p  «This is your tribe matcher! It is a drag and drop activity. Drag each tile into the category you think it best fits. Som»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [Body] [/RED TEXT]🔴 Which bird did you connect with the most? How accurate was the quiz? You are going to reflect on this later in your journal.`
- **XGF9002** XGF9002_2_0.html ↔ XGF9002_2_0.html (content, derivable=True)
  - gold: `p  «Through this activity, you have learned how You have seen that reactions such as shutdown, anger, rumination, or self-cr»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [Body] [/RED TEXT]🔴 In this activity, you explored how gifted and twice-exceptional traits can show up in everyday behaviours, especially those that are often misunderstood. You practised `
- **XGF9003** XGF9003_1_0.html ↔ XGF9003-02.0.html (content, derivable=True)
  - gold: `p  «Take a photo of your study space now you have finished decluttering and cleaning. In your journal you are going to compa»`
  - Claude: `—`
  - WT: `Now it’s time to head to your journal to share what you have learned so far.`
- modules: XGF9001, XGF9002, XGF9003, XGF9004, XGF9006

### #286 · body · EXTRA · `div#body` › gold `—` vs Claude `div.row` — CANDIDATE
- pages 35 / modules 5 / lines 257; consensus (all) 0.81 of 41 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 5m/35p c=0.81
- by subject: Leaving to Learn 5m/35p c=0.81
- by era: Refresh 5m/35p c=0.81
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **XGF9001** XGF9001_0_0.html ↔ XGF9001-02.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Mā te kōrero, ka mōhio; mā te mōhio, ka mārama»`
- **XGF9002** XGF9002_0_0.html ↔ XGF9002_0_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Our purpose»`
- **XGF9003** XGF9003_0_0.html ↔ XGF9003-00.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Click on a segment from the image below to learn more about the different executive function skills.»`
- modules: XGF9001, XGF9002, XGF9003, XGF9004, XGF9006

### #288 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `p` — CANDIDATE
- pages 27 / modules 5 / lines 100; consensus (all) 0.93 of 41 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 5m/27p c=0.93
- by subject: Leaving to Learn 5m/27p c=0.93
- by era: Refresh 5m/27p c=0.93
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **XGF9001** XGF9001_1_0.html ↔ XGF9001-03.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Greats and Gripes»`
- **XGF9002** XGF9002_0_0.html ↔ XGF9002_0_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «We recognise and celebrate the richness of»`
- **XGF9003** XGF9003_1_0.html ↔ XGF9003-02.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Being»`
- modules: XGF9001, XGF9002, XGF9003, XGF9004, XGF9006
