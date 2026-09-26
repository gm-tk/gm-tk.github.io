# DIFF_QUEUE.md — the diff miner's ranked class queue (LOOP__Autonomous_Rounds.md §1d)

**Produced:** 2026-09-26 13:27 NZST by `reference/tests/_diff_miner.py` on the CURRENT corpus (pageforge-site HEAD 84b660d; Claude corpus 545 dirs). **Population:** the skeleton gate's own — 84 paired pages / 12 modules (compare_exclusions.txt honoured; acks / glossary / references pages excluded); parse errors skipped: 0 (must be 0); modules without a parsed WT: 0. Run time 4.4 s.

**What a row is.** One CLASS = (region, parent element, gold form, Claude form, direction) over every differing skeleton line of every paired page — the same lines, labels, widget collapse and difflib alignment the PRIMARY gate scores (each element its own line so it can be quoted). Direction: MISSING = gold has it, Claude lacks it; EXTRA = Claude has it, gold lacks it; SUBSTITUTED = same position, different tag / class / wrapper; MOVED = same text, different place. Consensus = of the gold pages in the group where the region exists, the share carrying the gold form (for EXTRA: the share NOT carrying Claude's form). Derivable = the gold line's text is in the module's parsed Writers Template (round-110 tolerance); structure-only differences are always derivable.

**Candidate rule (§1d).** modules ≥ 10 for a chrome class (module-code / title / header / module-menu / crumbs / phases-nav / footer / acks), pages ≥ 20 for a body / activity class; gold consensus ≥ 0.60 in at least one template or subject group that itself reaches the floor; structure-only or derivable share ≥ 0.60. A class below the floor is listed, never dropped. A CANDIDATE still goes through the PICK's KB-first check, the triangulation and the §3 corpus-wide measurement before any code — this table is the queue, not the verdict.

## Summary

- differing skeleton lines: 6978 — by direction {'SUBSTITUTED': 726, 'MISSING': 4106, 'EXTRA': 2009, 'MOVED': 137}
- by region: {'title': 3, 'module-menu': 1066, 'footer': 60, 'acks': 38, 'activity': 2134, 'body': 3501, 'root': 176}
- classes: 781 — CANDIDATE 4, below floor 774, the rest below consensus / not derivable

## Completeness census — the repeating chrome (§1d item 4)

| region | pages with region | gold items | gold items in WT | Claude items | derivable misses | pages with misses | modules with misses | status |
|---|---|---|---|---|---|---|---|---|
| module-menu | 79 | 1272 | 1223 | 863 | 423 | 25 | 8 | BELOW FLOOR |
| crumbs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |
| phases-nav | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |
| footer | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |

- **module-menu** by template: Standard 8m/25p/423 misses
  - ENGI201 ENGI201_2_0.html: gold 52 items (52 in WT) / Claude 6 — 49 derivable misses, e.g. p «This module focuses on ākonga engaging with stories from diverse backgrounds, wh» · h3 «Understand»
  - ENGI201 ENGI201_3_0.html: gold 52 items (52 in WT) / Claude 6 — 49 derivable misses, e.g. p «This module focuses on ākonga engaging with stories from diverse backgrounds, wh» · h3 «Understand»
  - ENGI201 ENGI201_4_0.html: gold 52 items (52 in WT) / Claude 6 — 48 derivable misses, e.g. h3 «Understand» · span «Understand»
  - ENGI201 ENGI201_1_0.html: gold 52 items (52 in WT) / Claude 6 — 47 derivable misses, e.g. p «This module focuses on ākonga engaging with stories from diverse backgrounds, wh» · h3 «Understand»
- **crumbs** by template: 
- **phases-nav** by template: 
- **footer** by template: 

## Chrome facts — the header and footer as SETS per page (alignment-free; §1d items 2 + 4)

A fact is one thing a page's chrome has: `header:chip` (the `#module-code` div), `header:chip=module-code` / `=lesson-number` / `=lesson-number(00)`, `header:head-buttons`, `header:menu-content`, `header:title-h1-count=N`, `footer:present`, `footer:ul=<classes>`, `footer:link=prev-lesson` / `next-lesson` / `home-nav`, `footer:links=<order>`, `footer:inside-body`, `nav:crumbs`, `nav:phases`. MISSING = the gold page has the fact and Claude's does not; EXTRA the reverse. Consensus = the share of gold pages in the group that have (MISSING) / lack (EXTRA) the fact. Floor 10 modules.

| # | dir | fact | pages | modules | gold share (all) | consensus (all) | best group | status |
|---|---|---|---|---|---|---|---|---|
| F1 | MISSING | `header:chip=lesson-number` | 9 | 2 | 0.34 | 0.34 | — | BELOW FLOOR |
| F2 | EXTRA | `header:chip=decimal-number` | 9 | 2 | 0.51 | 0.49 | — | BELOW FLOOR |
| F3 | MISSING | `header:title-h1-count=2` | 2 | 2 | 0.14 | 0.14 | — | BELOW FLOOR |
| F4 | EXTRA | `header:title-h1-count=1` | 2 | 2 | 0.86 | 0.14 | — | BELOW FLOOR |
| F5 | EXTRA | `header:menu-content` | 2 | 2 | 0.94 | 0.06 | — | BELOW FLOOR |
| F6 | MISSING | `header:title-h1-count=1` | 1 | 1 | 0.86 | 0.86 | — | BELOW FLOOR |
| F7 | EXTRA | `header:title-h1-count=2` | 1 | 1 | 0.14 | 0.86 | — | BELOW FLOOR |
| F8 | EXTRA | `header:head-buttons` | 1 | 1 | 0.95 | 0.05 | — | BELOW FLOOR |
| F9 | MISSING | `footer:inside-body` | 7 | 6 | 0.08 | 0.08 | — | BELOW FLOOR |
| F10 | MISSING | `footer:links=prev-lesson,next-lesson,home-nav` | 3 | 3 | 0.74 | 0.74 | — | BELOW FLOOR |
| F11 | MISSING | `footer:link=next-lesson` | 3 | 3 | 0.88 | 0.88 | — | BELOW FLOOR |
| F12 | EXTRA | `footer:links=prev-lesson,home-nav` | 3 | 3 | 0.12 | 0.88 | — | BELOW FLOOR |
| F13 | MISSING | `footer:links=home-nav,next-lesson` | 2 | 2 | 0.02 | 0.02 | — | BELOW FLOOR |
| F14 | EXTRA | `footer:links=next-lesson,home-nav` | 2 | 2 | 0.12 | 0.88 | — | BELOW FLOOR |
| F15 | MISSING | `footer:links=prev-lesson,home-nav` | 1 | 1 | 0.12 | 0.12 | — | BELOW FLOOR |
| F16 | EXTRA | `footer:links=prev-lesson,next-lesson,home-nav` | 1 | 1 | 0.74 | 0.26 | — | BELOW FLOOR |
| F17 | EXTRA | `footer:link=next-lesson` | 1 | 1 | 0.88 | 0.12 | — | BELOW FLOOR |


## The ranked queue — chrome regions first, then by modules affected

| # | region | dir | parent | gold form | Claude form | pages | modules | consensus (all) | best group | derivable | KB | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | title | MISSING | `div#header` | `h1>span` | `—` | 2 | 2 | 0.14 of 84 | — | 1.00 | yes | BELOW FLOOR |
| 2 | title | EXTRA | `div#header` | `—` | `h1>span` | 1 | 1 | 0.86 of 84 | — | structure | yes | BELOW FLOOR |
| 3 | module-menu | EXTRA | `div.col-12.col-md-6.offset-md-0` | `—` | `p` | 11 | 10 | 0.83 of 84 | template=Standard c=0.83 n=10 | structure | yes | CANDIDATE |
| 4 | module-menu | MISSING | `p` | `br` | `—` | 14 | 7 | 0.17 of 84 | — | structure | — | BELOW FLOOR |
| 5 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `p` | `h5` | 7 | 7 | 0.24 of 84 | — | structure | yes | BELOW FLOOR |
| 6 | module-menu | SUBSTITUTED | `div.col-12.col-md-8` | `h3>span` | `h5` | 23 | 5 | 0.27 of 84 | — | structure | — | BELOW FLOOR |
| 7 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-6.offset-md-0` | 21 | 5 | 0.76 of 84 | — | structure | yes | BELOW FLOOR |
| 8 | module-menu | MISSING | `ul` | `li` | `—` | 8 | 5 | 0.07 of 84 | — | 0.57 | — | BELOW FLOOR |
| 9 | module-menu | EXTRA | `div.col-12.col-md-6.offset-md-0` | `—` | `ul` | 5 | 5 | 0.93 of 84 | — | structure | yes | BELOW FLOOR |
| 10 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `—` | 13 | 4 | 0.14 of 84 | — | 1.00 | yes | BELOW FLOOR |
| 11 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `h5` | 8 | 4 | 0.17 of 84 | — | structure | yes | BELOW FLOOR |
| 12 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `p` | `ul` | 7 | 4 | 0.24 of 84 | — | structure | yes | BELOW FLOOR |
| 13 | module-menu | EXTRA | `ul` | `—` | `li` | 5 | 4 | 0.80 of 84 | — | structure | — | BELOW FLOOR |
| 14 | module-menu | EXTRA | `div.col-12.col-md-6.offset-md-0` | `—` | `h5` | 4 | 4 | 1.00 of 84 | — | structure | yes | BELOW FLOOR |
| 15 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0` | `p` | `—` | 11 | 3 | 0.15 of 84 | — | 1.00 | yes | BELOW FLOOR |
| 16 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6.offset-md-0` | `—` | 10 | 3 | 0.24 of 84 | — | 1.00 | yes | BELOW FLOOR |
| 17 | module-menu | SUBSTITUTED | `p` | `br` | `li` | 6 | 3 | 0.20 of 84 | — | structure | — | BELOW FLOOR |
| 18 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-8` | 11 | 2 | 0.57 of 84 | — | structure | — | BELOW FLOOR |
| 19 | module-menu | MISSING | `div#module-menu-content.moduleMenu` | `p` | `—` | 10 | 2 | 0.06 of 84 | — | 1.00 | yes | BELOW FLOOR |
| 20 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0` | `ul` | `—` | 10 | 2 | 0.06 of 84 | — | 1.00 | yes | BELOW FLOOR |
| 21 | module-menu | SUBSTITUTED | `div#module-menu-content.moduleMenu` | `h5` | `div.row` | 8 | 2 | 0.10 of 84 | — | structure | yes | BELOW FLOOR |
| 22 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `h5` | 3 | 2 | 0.84 of 84 | — | structure | — | BELOW FLOOR |
| 23 | module-menu | MISSING | `div.col-12.col-md-8` | `h3>span` | `—` | 3 | 2 | 0.27 of 84 | — | 0.33 | — | BELOW FLOOR |
| 24 | module-menu | EXTRA | `div.col-12.col-md-6.offset-md-0` | `—` | `h4>span` | 2 | 2 | 0.93 of 84 | — | structure | yes | BELOW FLOOR |
| 25 | module-menu | EXTRA | `div.col-12.col-md-6.offset-md-0` | `—` | `p>b` | 2 | 2 | 1.00 of 84 | — | structure | yes | BELOW FLOOR |
| 26 | module-menu | EXTRA | `div#header` | `—` | `div#module-menu-content.moduleMenu` | 2 | 2 | 0.06 of 84 | — | structure | yes | BELOW FLOOR |
| 27 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-8.offset-md-0` | `div.col-12.col-md-6.offset-md-0` | 9 | 1 | 0.11 of 84 | — | structure | yes | BELOW FLOOR |
| 28 | module-menu | MISSING | `div.col-12.col-md-8.offset-md-0` | `h3>span` | `—` | 8 | 1 | 0.10 of 84 | — | 1.00 | — | BELOW FLOOR |
| 29 | module-menu | SUBSTITUTED | `div.col-12.col-md-8.offset-md-0` | `h3>span` | `h5` | 8 | 1 | 0.10 of 84 | — | structure | — | BELOW FLOOR |
| 30 | module-menu | MISSING | `div#module-menu-content.moduleMenu` | `ul` | `—` | 6 | 1 | 0.07 of 84 | — | 1.00 | yes | BELOW FLOOR |
| 31 | module-menu | MISSING | `div#module-menu-content.moduleMenu` | `h5` | `—` | 6 | 1 | 0.10 of 84 | — | 0.00 | yes | BELOW FLOOR |
| 32 | module-menu | MISSING | `div.col-12.col-md-8` | `p` | `—` | 6 | 1 | 0.07 of 84 | — | 0.00 | — | BELOW FLOOR |
| 33 | module-menu | SUBSTITUTED | `ul` | `li` | `li` | 6 | 1 | 0.87 of 84 | — | structure | — | BELOW FLOOR |
| 34 | module-menu | SUBSTITUTED | `div#module-menu-content.moduleMenu` | `p` | `div.row` | 4 | 1 | 0.13 of 84 | — | structure | yes | BELOW FLOOR |
| 35 | module-menu | SUBSTITUTED | `div#module-menu-content.moduleMenu` | `h5` | `h5` | 2 | 1 | 0.10 of 84 | — | structure | yes | BELOW FLOOR |
| 36 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `ul` | 1 | 1 | 0.57 of 84 | — | structure | — | BELOW FLOOR |
| 37 | module-menu | EXTRA | `div.col-12.col-md-6.offset-md-0` | `—` | `h3>span` | 1 | 1 | 0.83 of 84 | — | structure | yes | BELOW FLOOR |
| 38 | module-menu | EXTRA | `p>b` | `—` | `b` | 1 | 1 | 1.00 of 84 | — | structure | — | BELOW FLOOR |
| 39 | module-menu | EXTRA | `div#header` | `—` | `div#module-head-buttons` | 1 | 1 | 0.05 of 84 | — | structure | yes | BELOW FLOOR |
| 40 | module-menu | EXTRA | `li>a` | `—` | `a` | 1 | 1 | 1.00 of 84 | — | structure | — | BELOW FLOOR |
| 41 | module-menu | MISSING | `div.col-12.col-md-6` | `p` | `—` | 1 | 1 | 0.01 of 84 | — | 1.00 | yes | BELOW FLOOR |
| 42 | module-menu | MISSING | `div.col-12.col-md-6` | `h3>span` | `—` | 1 | 1 | 0.01 of 84 | — | 1.00 | yes | BELOW FLOOR |
| 43 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6.offset-md-0.paddingR` | `—` | 1 | 1 | 0.01 of 84 | — | 1.00 | yes | BELOW FLOOR |
| 44 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0.paddingL` | `p` | `—` | 1 | 1 | 0.01 of 84 | — | 0.50 | yes | BELOW FLOOR |
| 45 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0.paddingL` | `ul` | `—` | 1 | 1 | 0.01 of 84 | — | 1.00 | yes | BELOW FLOOR |
| 46 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0.paddingL` | `h5` | `—` | 1 | 1 | 0.01 of 84 | — | 0.00 | yes | BELOW FLOOR |
| 47 | module-menu | MISSING | `li>span.infoTrigger` | `span.infoTrigger` | `—` | 1 | 1 | 0.01 of 84 | — | 1.00 | — | BELOW FLOOR |
| 48 | module-menu | MOVED | `div.col-12.col-md-6.offset-md-0.paddingL` | `h5` | `h5` | 1 | 1 | 0.01 of 84 | — | structure | yes | BELOW FLOOR |
| 49 | module-menu | MOVED | `ul` | `li` | `li` | 1 | 1 | 0.27 of 84 | — | structure | — | BELOW FLOOR |
| 50 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `h4>span` | 1 | 1 | 0.17 of 84 | — | structure | yes | BELOW FLOOR |
| 51 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6` | `div.col-12.col-md-6.offset-md-0` | 1 | 1 | 0.01 of 84 | — | structure | yes | BELOW FLOOR |
| 52 | module-menu | SUBSTITUTED | `div.col-12.col-md-6` | `h3>span` | `h5` | 1 | 1 | 0.01 of 84 | — | structure | yes | BELOW FLOOR |
| 53 | module-menu | SUBSTITUTED | `p` | `br` | `div.col-12.col-md-8` | 1 | 1 | 0.20 of 84 | — | structure | — | BELOW FLOOR |
| 54 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-12` | `div.col-12.col-md-6.offset-md-0` | 1 | 1 | 0.01 of 84 | — | structure | yes | BELOW FLOOR |
| 55 | module-menu | SUBSTITUTED | `div.col-12.col-md-12` | `div.row` | `h4>span` | 1 | 1 | 0.01 of 84 | — | structure | — | BELOW FLOOR |
| 56 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0.paddingR` | `h4>span` | `h4>span` | 1 | 1 | 0.01 of 84 | — | structure | yes | BELOW FLOOR |
| 57 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0.paddingR` | `p` | `p>b` | 1 | 1 | 0.01 of 84 | — | structure | yes | BELOW FLOOR |
| 58 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0.paddingR` | `ul` | `ul` | 1 | 1 | 0.01 of 84 | — | structure | yes | BELOW FLOOR |
| 59 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.offset-md-0.paddingL` | `li` | 1 | 1 | 0.01 of 84 | — | structure | yes | BELOW FLOOR |
| 60 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `p` | 1 | 1 | 0.17 of 84 | — | structure | yes | BELOW FLOOR |
| 61 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `div.col-12.col-md-6.offset-md-0` | 1 | 1 | 0.43 of 84 | — | structure | yes | BELOW FLOOR |
| 62 | module-menu | SUBSTITUTED | `p` | `br` | `b` | 1 | 1 | 0.20 of 84 | — | structure | — | BELOW FLOOR |
| 63 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `ul` | `p` | 1 | 1 | 0.24 of 84 | — | structure | yes | BELOW FLOOR |
| 64 | footer | MISSING | `div#body` | `div#footer` | `—` | 5 | 5 | 0.08 of 84 | — | structure | yes | BELOW FLOOR |
| 65 | footer | EXTRA | `body.container-fluid` | `—` | `div#footer` | 3 | 3 | 0.08 of 84 | — | structure | yes | BELOW FLOOR |
| 66 | footer | MISSING | `li>a#next-lesson` | `a#next-lesson` | `—` | 3 | 3 | 0.88 of 84 | — | structure | yes | BELOW FLOOR |
| 67 | footer | MISSING | `ul.footer-nav` | `li>a.home-nav` | `—` | 3 | 3 | 1.00 of 84 | — | structure | yes | BELOW FLOOR |
| 68 | footer | EXTRA | `div#footer` | `—` | `ul.footer-nav` | 2 | 2 | 0.00 of 84 | — | structure | yes | BELOW FLOOR |
| 69 | footer | SUBSTITUTED | `div#body` | `div#footer` | `div#footer` | 2 | 2 | 0.08 of 84 | — | structure | yes | BELOW FLOOR |
| 70 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav` | `ul.footer-nav` | 2 | 2 | 1.00 of 84 | — | structure | yes | BELOW FLOOR |
| 71 | footer | EXTRA | `li>a#next-lesson` | `—` | `a#next-lesson` | 1 | 1 | 0.12 of 84 | — | structure | yes | BELOW FLOOR |
| 72 | footer | EXTRA | `ul.footer-nav` | `—` | `li>a.home-nav` | 1 | 1 | 0.00 of 84 | — | structure | yes | BELOW FLOOR |
| 73 | footer | SUBSTITUTED | `ul.footer-nav` | `li>a.home-nav` | `li>a#next-lesson` | 1 | 1 | 1.00 of 84 | — | structure | yes | BELOW FLOOR |
| 74 | footer | SUBSTITUTED | `ul.footer-nav` | `li>a#next-lesson` | `li>a.home-nav` | 1 | 1 | 0.88 of 84 | — | structure | yes | BELOW FLOOR |
| 75 | footer | SUBSTITUTED | `ul.footer-nav` | `li>a#prev-lesson` | `li>a#prev-lesson` | 1 | 1 | 0.86 of 84 | — | structure | yes | BELOW FLOOR |
| 76 | footer | SUBSTITUTED | `ul.footer-nav` | `li>a#next-lesson` | `li>a#next-lesson` | 1 | 1 | 0.88 of 84 | — | structure | yes | BELOW FLOOR |
| 77 | footer | SUBSTITUTED | `ul.footer-nav` | `li>a.home-nav` | `li>a.home-nav` | 1 | 1 | 1.00 of 84 | — | structure | yes | BELOW FLOOR |
| 78 | acks | SUBSTITUTED | `div.col-12.col-md-8` | `div.acks` | `div.acks.acksTemplate` | 1 | 1 | 0.11 of 84 | — | structure | yes | BELOW FLOOR |
| 79 | activity | EXTRA | `div.col-12` | `—` | `p` | 25 | 10 | 0.89 of 84 | template=Standard c=0.89 n=25 | structure | — | CANDIDATE |
| 80 | activity | MISSING | `div.col-12` | `p` | `—` | 20 | 9 | 0.23 of 84 | — | 0.89 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 81 | activity | MISSING | `a` | `div.button` | `—` | 16 | 8 | 0.15 of 84 | — | 0.80 | yes | BELOW FLOOR |
| 82 | activity | EXTRA | `div.col-12` | `—` | `ul` | 13 | 8 | 0.95 of 84 | — | structure | — | BELOW FLOOR |
| 83 | activity | MISSING | `div.col-12` | `a` | `—` | 16 | 7 | 0.32 of 84 | — | 0.78 | — | BELOW FLOOR |
| 84 | activity | MISSING | `div.col-12` | `div.row` | `—` | 10 | 7 | 0.19 of 84 | — | 1.00 | — | BELOW FLOOR |
| 85 | activity | MOVED | `div.col-12` | `p` | `p` | 9 | 7 | 0.15 of 84 | — | structure | — | BELOW FLOOR |
| 86 | activity | MISSING | `div.col-12` | `div.hint` | `—` | 10 | 6 | 0.17 of 84 | — | structure | yes | BELOW FLOOR |
| 87 | activity | MISSING | `div.col-12` | `WIDGET` | `—` | 9 | 6 | 0.15 of 84 | — | structure | — | BELOW FLOOR |
| 88 | activity | MISSING | `p` | `br` | `—` | 8 | 6 | 0.24 of 84 | — | structure | — | BELOW FLOOR |
| 89 | activity | MOVED | `div.col-12` | `p` | `p` | 7 | 6 | 0.46 of 84 | — | structure | — | BELOW FLOOR |
| 90 | activity | MISSING | `div.col-12` | `h4.goJournal` | `—` | 11 | 5 | 0.30 of 84 | — | 0.50 | — | BELOW FLOOR |
| 91 | activity | EXTRA | `div.col-12` | `—` | `h4.goJournal` | 7 | 5 | 0.70 of 84 | — | structure | — | BELOW FLOOR |
| 92 | activity | EXTRA | `div.col-12` | `—` | `WIDGET` | 6 | 5 | 0.93 of 84 | — | structure | — | BELOW FLOOR |
| 93 | activity | EXTRA | `p>b` | `—` | `b` | 5 | 5 | 0.88 of 84 | — | structure | — | BELOW FLOOR |
| 94 | activity | MISSING | `a` | `div.externalButton` | `—` | 9 | 4 | 0.08 of 84 | — | 0.60 | — | BELOW FLOOR |
| 95 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.alertPadding[number=*]` | `div.activity[number=*]` | 7 | 4 | 0.14 of 84 | — | structure | yes | BELOW FLOOR |
| 96 | activity | MISSING | `div.col-12` | `h3` | `—` | 6 | 4 | 0.45 of 84 | — | 0.83 | — | BELOW FLOOR |
| 97 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `div.activity[number=*]` | 6 | 4 | 0.52 of 84 | — | structure | yes | BELOW FLOOR |
| 98 | activity | SUBSTITUTED | `div.col-12` | `a` | `p` | 6 | 4 | 0.61 of 84 | — | structure | — | BELOW FLOOR |
| 99 | activity | EXTRA | `div.col-12` | `—` | `a` | 5 | 4 | 0.39 of 84 | — | structure | — | BELOW FLOOR |
| 100 | activity | EXTRA | `div.col-12` | `—` | `img.img-fluid` | 5 | 4 | 1.00 of 84 | — | structure | — | BELOW FLOOR |
| 347 | body | EXTRA | `div#body` | `—` | `div.row` | 46 | 12 | 0.67 of 84 | template=Standard c=0.67 n=46 | structure | — | CANDIDATE |
| 349 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 33 | 11 | 0.64 of 84 | template=Standard c=0.64 n=33 | structure | — | CANDIDATE |

## Details — in the companion file `CONVERTER_V2/outputs/_s51_ENGI_miner_details.md`
Every CANDIDATE and every top-40 row has three quoted examples (WT / gold / Claude) there, plus the
below-floor list. **NEVER read the companion whole** (hundreds of KB): `grep -n '^### #<rank> ' CONVERTER_V2/outputs/_diff_queue_details.md` then `sed -n '<start>,<start+40>p'`. The top 25
candidates' detail blocks are repeated below for convenience.

### #3 · module-menu · EXTRA · `div.col-12.col-md-6.offset-md-0` › gold `—` vs Claude `p` — CANDIDATE
- pages 11 / modules 10 / lines 30; consensus (all) 0.83 of 84 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 10m/11p c=0.83
- by subject: 1-10 English 10m/11p c=0.83
- by era: Refresh 10m/11p c=0.83
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:160 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **ENGI101** ENGI101_0_0.html ↔ ENGI101_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «These ideas include themes, messages, and opinions. I have my own ideas and stories that are worth sharing.»`
- **ENGI102** ENGI102_0_0.html ↔ ENGI102_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «There are stories and ideas from Aotearoa New Zealand that matter to me. Those from te ao Māori help me to understand my»`
- **ENGI103** ENGI103_0_0.html ↔ ENGI103_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Language and literature give us insights into ourselves and others.»`
- modules: ENGI101, ENGI102, ENGI103, ENGI201, ENGI202, ENGI203, ENGI301, ENGI302, ENGI400, ENGI405

### #79 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `p` — CANDIDATE
- pages 25 / modules 10 / lines 42; consensus (all) 0.89 of 84 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 10m/25p c=0.89
- by subject: 1-10 English 10m/25p c=0.89
- by era: Refresh 10m/25p c=0.89
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ENGI101** ENGI101_1_2.html ↔ ENGI101_5.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «In your journal, brainstorm a list of special things you and your whānau do.»`
- **ENGI102** ENGI102_2_0.html ↔ ENGI102_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «If you like the look of more than one activity, please feel free to complete it and add it to your journal too.»`
- **ENGI103** ENGI103_2_0.html ↔ ENGI103_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «The_____is_______.»`
- modules: ENGI101, ENGI102, ENGI103, ENGI201, ENGI202, ENGI203, ENGI302, ENGI303, ENGI401, ENGI405

### #347 · body · EXTRA · `div#body` › gold `—` vs Claude `div.row` — CANDIDATE
- pages 46 / modules 12 / lines 125; consensus (all) 0.67 of 84 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 12m/46p c=0.67
- by subject: 1-10 English 12m/46p c=0.67
- by era: Refresh 12m/46p c=0.67
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ENGI101** ENGI101_1_0.html ↔ ENGI101_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «The Bomb»`
- **ENGI102** ENGI102_2_0.html ↔ ENGI102_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Fairytales»`
- **ENGI103** ENGI103_1_0.html ↔ ENGI103_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «First, then, next, finally»`
- modules: ENGI101, ENGI102, ENGI103, ENGI201, ENGI202, ENGI203, ENGI301, ENGI302, ENGI303, ENGI400, ENGI401, ENGI405

### #349 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `p` — CANDIDATE
- pages 33 / modules 11 / lines 73; consensus (all) 0.64 of 84 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 11m/33p c=0.64
- by subject: 1-10 English 11m/33p c=0.64
- by era: Refresh 11m/33p c=0.64
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ENGI101** ENGI101_0_0.html ↔ ENGI101_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «In this module, we will look closely at three different texts that all have a different storyline and message in them. T»`
- **ENGI102** ENGI102_0_0.html ↔ ENGI102_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «We will learn about traditional pūrākau (stories) from Aotearoa and around the world, to help us better understand ourse»`
- **ENGI103** ENGI103_3_0.html ↔ ENGI103_3.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «The boys in the story work hard at waka ama and are proud of winning a gold medal. Watch this video to learn about the f»`
- modules: ENGI101, ENGI102, ENGI103, ENGI201, ENGI202, ENGI203, ENGI301, ENGI302, ENGI303, ENGI400, ENGI405
