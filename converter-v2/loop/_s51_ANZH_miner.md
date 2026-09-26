# DIFF_QUEUE.md — the diff miner's ranked class queue (LOOP__Autonomous_Rounds.md §1d)

**Produced:** 2026-09-26 13:27 NZST by `reference/tests/_diff_miner.py` on the CURRENT corpus (pageforge-site HEAD 84b660d; Claude corpus 545 dirs). **Population:** the skeleton gate's own — 94 paired pages / 12 modules (compare_exclusions.txt honoured; acks / glossary / references pages excluded); parse errors skipped: 0 (must be 0); modules without a parsed WT: 0. Run time 4.7 s.

**What a row is.** One CLASS = (region, parent element, gold form, Claude form, direction) over every differing skeleton line of every paired page — the same lines, labels, widget collapse and difflib alignment the PRIMARY gate scores (each element its own line so it can be quoted). Direction: MISSING = gold has it, Claude lacks it; EXTRA = Claude has it, gold lacks it; SUBSTITUTED = same position, different tag / class / wrapper; MOVED = same text, different place. Consensus = of the gold pages in the group where the region exists, the share carrying the gold form (for EXTRA: the share NOT carrying Claude's form). Derivable = the gold line's text is in the module's parsed Writers Template (round-110 tolerance); structure-only differences are always derivable.

**Candidate rule (§1d).** modules ≥ 10 for a chrome class (module-code / title / header / module-menu / crumbs / phases-nav / footer / acks), pages ≥ 20 for a body / activity class; gold consensus ≥ 0.60 in at least one template or subject group that itself reaches the floor; structure-only or derivable share ≥ 0.60. A class below the floor is listed, never dropped. A CANDIDATE still goes through the PICK's KB-first check, the triangulation and the §3 corpus-wide measurement before any code — this table is the queue, not the verdict.

## Summary

- differing skeleton lines: 6723 — by direction {'SUBSTITUTED': 751, 'MISSING': 3023, 'EXTRA': 2774, 'MOVED': 175}
- by region: {'title': 33, 'module-menu': 1181, 'footer': 178, 'acks': 61, 'activity': 1926, 'body': 3287, 'root': 57}
- classes: 741 — CANDIDATE 4, below floor 733, the rest below consensus / not derivable

## Completeness census — the repeating chrome (§1d item 4)

| region | pages with region | gold items | gold items in WT | Claude items | derivable misses | pages with misses | modules with misses | status |
|---|---|---|---|---|---|---|---|---|
| module-menu | 56 | 1375 | 1182 | 515 | 766 | 42 | 7 | BELOW FLOOR |
| crumbs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |
| phases-nav | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |
| footer | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |

- **module-menu** by template: Standard 7m/42p/766 misses
  - ANZH404 ANZH404_5_0.html: gold 42 items (36 in WT) / Claude 0 — 36 derivable misses, e.g. h3 «Understand» · span «Understand»
  - ANZH404 ANZH404_6_0.html: gold 42 items (36 in WT) / Claude 0 — 36 derivable misses, e.g. h3 «Understand» · span «Understand»
  - ANZH404 ANZH404_4_0.html: gold 38 items (32 in WT) / Claude 0 — 32 derivable misses, e.g. h3 «Understand» · span «Understand»
  - ANZH401 ANZH401_1_0.html: gold 30 items (30 in WT) / Claude 0 — 30 derivable misses, e.g. h3 «Understand» · span «Understand»
- **crumbs** by template: 
- **phases-nav** by template: 
- **footer** by template: 

## Chrome facts — the header and footer as SETS per page (alignment-free; §1d items 2 + 4)

A fact is one thing a page's chrome has: `header:chip` (the `#module-code` div), `header:chip=module-code` / `=lesson-number` / `=lesson-number(00)`, `header:head-buttons`, `header:menu-content`, `header:title-h1-count=N`, `footer:present`, `footer:ul=<classes>`, `footer:link=prev-lesson` / `next-lesson` / `home-nav`, `footer:links=<order>`, `footer:inside-body`, `nav:crumbs`, `nav:phases`. MISSING = the gold page has the fact and Claude's does not; EXTRA the reverse. Consensus = the share of gold pages in the group that have (MISSING) / lack (EXTRA) the fact. Floor 10 modules.

| # | dir | fact | pages | modules | gold share (all) | consensus (all) | best group | status |
|---|---|---|---|---|---|---|---|---|
| F1 | MISSING | `header:title-h1-count=2` | 31 | 6 | 0.47 | 0.47 | — | BELOW FLOOR |
| F2 | EXTRA | `header:title-h1-count=1` | 31 | 6 | 0.53 | 0.47 | — | BELOW FLOOR |
| F3 | MISSING | `header:chip=lesson-number` | 20 | 4 | 0.21 | 0.21 | — | BELOW FLOOR |
| F4 | EXTRA | `header:chip=decimal-number` | 20 | 4 | 0.47 | 0.53 | — | BELOW FLOOR |
| F5 | MISSING | `header:chip=module-code` | 12 | 1 | 0.26 | 0.26 | — | BELOW FLOOR |
| F6 | EXTRA | `header:chip=other` | 12 | 1 | 0.06 | 0.94 | — | BELOW FLOOR |
| F7 | MISSING | `header:title-h1-count=1` | 2 | 1 | 0.53 | 0.53 | — | BELOW FLOOR |
| F8 | EXTRA | `header:title-h1-count=2` | 2 | 1 | 0.47 | 0.53 | — | BELOW FLOOR |
| F9 | MISSING | `footer:link=next-lesson` | 4 | 4 | 0.90 | 0.90 | — | BELOW FLOOR |
| F10 | MISSING | `footer:links=prev-lesson,next-lesson,home-nav` | 4 | 4 | 0.61 | 0.61 | — | BELOW FLOOR |
| F11 | EXTRA | `footer:links=prev-lesson,home-nav` | 4 | 4 | 0.10 | 0.90 | — | BELOW FLOOR |
| F12 | EXTRA | `footer:links=prev-lesson,next-lesson,home-nav` | 17 | 3 | 0.61 | 0.39 | — | BELOW FLOOR |
| F13 | MISSING | `footer:inside-body` | 7 | 3 | 0.07 | 0.07 | — | BELOW FLOOR |
| F14 | MISSING | `footer:links=prev-lesson,home-nav,next-lesson` | 16 | 2 | 0.17 | 0.17 | — | BELOW FLOOR |
| F15 | MISSING | `footer:links=home-nav,next-lesson` | 2 | 2 | 0.02 | 0.02 | — | BELOW FLOOR |
| F16 | EXTRA | `footer:links=next-lesson,home-nav` | 2 | 2 | 0.11 | 0.89 | — | BELOW FLOOR |
| F17 | MISSING | `footer:links=prev-lesson,home-nav` | 1 | 1 | 0.10 | 0.10 | — | BELOW FLOOR |
| F18 | EXTRA | `footer:link=next-lesson` | 1 | 1 | 0.90 | 0.10 | — | BELOW FLOOR |


## The ranked queue — chrome regions first, then by modules affected

| # | region | dir | parent | gold form | Claude form | pages | modules | consensus (all) | best group | derivable | KB | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | title | MISSING | `div#header` | `h1>span` | `—` | 31 | 6 | 0.47 of 94 | — | 0.32 | yes | BELOW FLOOR |
| 2 | title | EXTRA | `div#header` | `—` | `h1>span` | 2 | 1 | 0.53 of 94 | — | structure | yes | BELOW FLOOR |
| 3 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-6.paddingR` | 16 | 7 | 1.00 of 94 | — | structure | yes | BELOW FLOOR |
| 4 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.offset-md-0` | `div.col-12.col-md-8` | 37 | 5 | 0.53 of 94 | — | structure | yes | BELOW FLOOR |
| 5 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0` | `ul` | `—` | 35 | 5 | 0.36 of 94 | — | 0.84 | yes | BELOW FLOOR |
| 6 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `—` | 35 | 5 | 0.46 of 94 | — | 0.96 | yes | BELOW FLOOR |
| 7 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6.offset-md-0` | `—` | 31 | 4 | 0.46 of 94 | — | 0.94 | yes | BELOW FLOOR |
| 8 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0` | `p` | `—` | 23 | 4 | 0.21 of 94 | — | 0.36 | yes | BELOW FLOOR |
| 9 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.offset-md-0` | `div.col-12.col-md-12.paddingR` | 13 | 4 | 0.53 of 94 | — | structure | yes | BELOW FLOOR |
| 10 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `h4>span` | 13 | 4 | 0.46 of 94 | — | structure | yes | BELOW FLOOR |
| 11 | module-menu | MISSING | `ul` | `li` | `—` | 15 | 3 | 0.15 of 94 | — | 0.43 | — | BELOW FLOOR |
| 12 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.offset-md-0` | `div.col-12.col-md-6.paddingR` | 12 | 3 | 0.53 of 94 | — | structure | yes | BELOW FLOOR |
| 13 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `h5>span` | 9 | 3 | 0.46 of 94 | — | structure | yes | BELOW FLOOR |
| 14 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.paddingR` | `div.col-12.col-md-12.paddingR` | 3 | 3 | 0.03 of 94 | — | structure | yes | BELOW FLOOR |
| 15 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `h4>span` | `h5>span` | 3 | 3 | 0.03 of 94 | — | structure | yes | BELOW FLOOR |
| 16 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.paddingL` | `div.col-12.col-md-6.paddingR` | 3 | 3 | 0.03 of 94 | — | structure | yes | BELOW FLOOR |
| 17 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0` | `p>b` | `—` | 19 | 2 | 0.19 of 94 | — | 0.68 | yes | BELOW FLOOR |
| 18 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `h5` | 13 | 2 | 1.00 of 94 | — | structure | — | BELOW FLOOR |
| 19 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `p` | `h5` | 8 | 2 | 0.34 of 94 | — | structure | yes | BELOW FLOOR |
| 20 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `h5` | 5 | 2 | 0.46 of 94 | — | structure | yes | BELOW FLOOR |
| 21 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 3 | 2 | 1.00 of 94 | — | structure | — | BELOW FLOOR |
| 22 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `ul` | 3 | 2 | 1.00 of 94 | — | structure | — | BELOW FLOOR |
| 23 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `p` | 2 | 2 | 1.00 of 94 | — | structure | yes | BELOW FLOOR |
| 24 | module-menu | EXTRA | `li>b` | `—` | `b` | 2 | 2 | 1.00 of 94 | — | structure | — | BELOW FLOOR |
| 25 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `p` | `—` | 2 | 2 | 0.03 of 94 | — | 1.00 | yes | BELOW FLOOR |
| 26 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingL` | `p` | `h5` | 2 | 2 | 0.02 of 94 | — | structure | yes | BELOW FLOOR |
| 27 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `h4>span` | `h5` | 7 | 1 | 0.07 of 94 | — | structure | yes | BELOW FLOOR |
| 28 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `ul` | `p` | 4 | 1 | 0.53 of 94 | — | structure | yes | BELOW FLOOR |
| 29 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `p` | 4 | 1 | 0.46 of 94 | — | structure | yes | BELOW FLOOR |
| 30 | module-menu | SUBSTITUTED | `div.row` | `WIDGET` | `div.col-12.col-md-8` | 2 | 1 | 0.19 of 94 | — | structure | — | BELOW FLOOR |
| 31 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `p>b` | 1 | 1 | 1.00 of 94 | — | structure | yes | BELOW FLOOR |
| 32 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `h5` | 1 | 1 | 1.00 of 94 | — | structure | yes | BELOW FLOOR |
| 33 | module-menu | MOVED | `div.col-12.col-md-6.paddingR` | `p` | `p` | 1 | 1 | 0.03 of 94 | — | structure | yes | BELOW FLOOR |
| 34 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6` | `div.col-12.col-md-8` | 1 | 1 | 0.01 of 94 | — | structure | yes | BELOW FLOOR |
| 35 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `h4` | `h5` | 1 | 1 | 0.14 of 94 | — | structure | yes | BELOW FLOOR |
| 36 | footer | EXTRA | `body.container-fluid` | `—` | `div#footer` | 11 | 6 | 0.14 of 94 | — | structure | yes | BELOW FLOOR |
| 37 | footer | MISSING | `li>a#next-lesson` | `a#next-lesson` | `—` | 4 | 4 | 0.90 of 94 | — | structure | yes | BELOW FLOOR |
| 38 | footer | EXTRA | `li>a#next-lesson` | `—` | `a#next-lesson` | 19 | 3 | 0.10 of 94 | — | structure | yes | BELOW FLOOR |
| 39 | footer | EXTRA | `ul.footer-nav` | `—` | `li>a.home-nav` | 19 | 3 | 0.00 of 94 | — | structure | yes | BELOW FLOOR |
| 40 | footer | MISSING | `div#body` | `div#footer` | `—` | 5 | 3 | 0.07 of 94 | — | structure | yes | BELOW FLOOR |
| 41 | footer | MISSING | `div#footer` | `ul.footer-nav` | `—` | 4 | 3 | 1.00 of 94 | — | structure | yes | BELOW FLOOR |
| 42 | footer | MISSING | `ul.footer-nav` | `li>a.home-nav` | `—` | 3 | 3 | 1.00 of 94 | — | structure | yes | BELOW FLOOR |
| 43 | footer | MISSING | `ul.footer-nav` | `li>a#next-lesson` | `—` | 18 | 2 | 0.90 of 94 | — | structure | yes | BELOW FLOOR |
| 44 | footer | MISSING | `div.row` | `div#footer` | `—` | 3 | 2 | 0.05 of 94 | — | structure | yes | BELOW FLOOR |
| 45 | footer | EXTRA | `div#footer` | `—` | `ul.footer-nav` | 2 | 1 | 0.00 of 94 | — | structure | yes | BELOW FLOOR |
| 46 | footer | MISSING | `li>a#prev-lesson` | `a#prev-lesson` | `—` | 1 | 1 | 0.87 of 94 | — | structure | yes | BELOW FLOOR |
| 47 | footer | MISSING | `li>a.home-nav` | `a.home-nav` | `—` | 1 | 1 | 1.00 of 94 | — | structure | yes | BELOW FLOOR |
| 48 | footer | MISSING | `div.col-12.col-md-12` | `div#footer` | `—` | 1 | 1 | 0.01 of 94 | — | structure | yes | BELOW FLOOR |
| 49 | footer | SUBSTITUTED | `div.row` | `div#footer` | `div.button.downloadButton` | 1 | 1 | 0.05 of 94 | — | structure | yes | BELOW FLOOR |
| 50 | footer | SUBSTITUTED | `ul.footer-nav` | `li>a#next-lesson` | `li` | 1 | 1 | 0.90 of 94 | — | structure | yes | BELOW FLOOR |
| 51 | footer | SUBSTITUTED | `ul.footer-nav` | `li>a#prev-lesson` | `li>a.home-nav` | 1 | 1 | 0.87 of 94 | — | structure | yes | BELOW FLOOR |
| 52 | footer | SUBSTITUTED | `ul.footer-nav` | `li>a.home-nav` | `li>a#next-lesson` | 1 | 1 | 1.00 of 94 | — | structure | yes | BELOW FLOOR |
| 53 | footer | SUBSTITUTED | `div.row` | `div#footer` | `div.col-12` | 1 | 1 | 0.05 of 94 | — | structure | yes | BELOW FLOOR |
| 54 | footer | SUBSTITUTED | `div#body` | `div#footer` | `div.col-12` | 1 | 1 | 0.07 of 94 | — | structure | yes | BELOW FLOOR |
| 55 | footer | SUBSTITUTED | `div#body` | `div#footer` | `div.activity[number=*]` | 1 | 1 | 0.07 of 94 | — | structure | yes | BELOW FLOOR |
| 56 | acks | SUBSTITUTED | `div.col-12.col-md-8` | `div.acks` | `div.acks.acksTemplate` | 2 | 2 | 0.22 of 94 | — | structure | yes | BELOW FLOOR |
| 57 | acks | EXTRA | `div.acks.acksTemplate` | `—` | `WIDGET` | 1 | 1 | 0.99 of 94 | — | structure | yes | BELOW FLOOR |
| 58 | acks | MISSING | `div.acks` | `WIDGET` | `—` | 1 | 1 | 0.22 of 94 | — | structure | yes | BELOW FLOOR |
| 59 | acks | SUBSTITUTED | `div.col-12.col-md-8` | `div.acks` | `h3` | 1 | 1 | 0.22 of 94 | — | structure | yes | BELOW FLOOR |
| 60 | activity | EXTRA | `div.col-12` | `—` | `p` | 25 | 10 | 0.98 of 94 | template=Standard c=0.98 n=25 | structure | — | CANDIDATE |
| 61 | activity | MISSING | `a` | `div.button` | `—` | 22 | 9 | 0.19 of 94 | — | 0.94 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 62 | activity | MISSING | `div.col-12` | `a` | `—` | 17 | 9 | 0.48 of 94 | — | 0.82 | — | BELOW FLOOR |
| 63 | activity | MISSING | `div.col-12` | `p` | `—` | 19 | 8 | 0.17 of 94 | — | 0.77 | — | BELOW FLOOR |
| 64 | activity | EXTRA | `div.col-12` | `—` | `WIDGET` | 16 | 8 | 0.95 of 94 | — | structure | — | BELOW FLOOR |
| 65 | activity | EXTRA | `div.col-12` | `—` | `img.img-fluid` | 12 | 7 | 0.89 of 94 | — | structure | — | BELOW FLOOR |
| 66 | activity | EXTRA | `div.col-12` | `—` | `p>a` | 7 | 6 | 0.99 of 94 | — | structure | — | BELOW FLOOR |
| 67 | activity | MISSING | `div.col-12` | `h3` | `—` | 7 | 6 | 0.35 of 94 | — | 0.71 | — | BELOW FLOOR |
| 68 | activity | EXTRA | `div.row` | `—` | `div.col-12` | 17 | 5 | 0.83 of 94 | — | structure | — | BELOW FLOOR |
| 69 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.alertPadding[number=*]` | `div.activity[number=*]` | 14 | 5 | 0.31 of 94 | — | structure | yes | BELOW FLOOR |
| 70 | activity | EXTRA | `div.activity[number=*]` | `—` | `div.row` | 9 | 5 | 0.99 of 94 | — | structure | yes | BELOW FLOOR |
| 71 | activity | EXTRA | `div.col-12` | `—` | `p>b` | 9 | 5 | 0.97 of 94 | — | structure | — | BELOW FLOOR |
| 72 | activity | EXTRA | `div.col-12` | `—` | `div.icon.ratio.ratio-16x9.videoSection` | 9 | 5 | 0.99 of 94 | — | structure | yes | BELOW FLOOR |
| 73 | activity | SUBSTITUTED | `div.col-12` | `a` | `h4.goJournal` | 9 | 5 | 0.48 of 94 | — | structure | — | BELOW FLOOR |
| 74 | activity | EXTRA | `div.col-12` | `—` | `ul` | 8 | 5 | 0.84 of 94 | — | structure | — | BELOW FLOOR |
| 75 | activity | MISSING | `div.col-12` | `WIDGET` | `—` | 7 | 5 | 0.05 of 94 | — | structure | — | BELOW FLOOR |
| 76 | activity | MISSING | `div.col-12` | `h4` | `—` | 6 | 5 | 0.03 of 94 | — | 0.57 | — | BELOW FLOOR |
| 77 | activity | MISSING | `ol` | `li` | `—` | 5 | 5 | 0.07 of 94 | — | 0.80 | — | BELOW FLOOR |
| 78 | activity | MOVED | `div.col-12` | `p` | `p` | 5 | 5 | 0.24 of 94 | — | structure | — | BELOW FLOOR |
| 79 | activity | EXTRA | `div.col-12` | `—` | `ol` | 9 | 4 | 0.95 of 94 | — | structure | — | BELOW FLOOR |
| 80 | activity | EXTRA | `div.col-12` | `—` | `a` | 7 | 4 | 0.52 of 94 | — | structure | — | BELOW FLOOR |
| 81 | activity | MOVED | `div.col-12` | `p` | `p` | 7 | 4 | 0.17 of 94 | — | structure | — | BELOW FLOOR |
| 82 | activity | MISSING | `div.col-12` | `ol` | `—` | 6 | 4 | 0.23 of 94 | — | 1.00 | — | BELOW FLOOR |
| 83 | activity | MISSING | `div.col-12` | `ul` | `—` | 6 | 4 | 0.16 of 94 | — | 0.50 | — | BELOW FLOOR |
| 84 | activity | EXTRA | `div.col-12.col-md-8` | `—` | `div.activity[number=*]` | 5 | 4 | 0.99 of 94 | — | structure | yes | BELOW FLOOR |
| 85 | activity | MISSING | `div.row` | `div.col-12` | `—` | 4 | 4 | 0.37 of 94 | — | 0.75 | — | BELOW FLOOR |
| 86 | activity | MISSING | `div.col-12` | `div.hint` | `—` | 4 | 4 | 0.07 of 94 | — | structure | yes | BELOW FLOOR |
| 87 | activity | EXTRA | `div.activity.interactive[number=*]` | `—` | `div.row` | 7 | 3 | 0.83 of 94 | — | structure | yes | BELOW FLOOR |
| 88 | activity | MOVED | `ol` | `li` | `li` | 7 | 3 | 0.17 of 94 | — | structure | — | BELOW FLOOR |
| 89 | activity | EXTRA | `a` | `—` | `div.externalButton` | 6 | 3 | 0.90 of 94 | — | structure | — | BELOW FLOOR |
| 90 | activity | MISSING | `div.col-12` | `h4.goJournal` | `—` | 6 | 3 | 0.03 of 94 | — | 1.00 | — | BELOW FLOOR |
| 91 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `div.activity[number=*]` | 6 | 3 | 0.44 of 94 | — | structure | yes | BELOW FLOOR |
| 92 | activity | EXTRA | `ol` | `—` | `li` | 5 | 3 | 0.93 of 94 | — | structure | — | BELOW FLOOR |
| 93 | activity | MISSING | `div.col-12` | `img.img-fluid` | `—` | 5 | 3 | 0.04 of 94 | — | structure | — | BELOW FLOOR |
| 94 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `div.activity[number=*]` | 5 | 3 | 0.13 of 94 | — | structure | yes | BELOW FLOOR |
| 95 | activity | EXTRA | `div.col-12` | `—` | `h4.goJournal` | 4 | 3 | 0.76 of 94 | — | structure | — | BELOW FLOOR |
| 96 | activity | MISSING | `p` | `br` | `—` | 4 | 3 | 0.07 of 94 | — | structure | — | BELOW FLOOR |
| 97 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `div.activity.interactive[number=*]` | 4 | 3 | 0.44 of 94 | — | structure | yes | BELOW FLOOR |
| 98 | activity | EXTRA | `div.col-12` | `—` | `h3` | 3 | 3 | 0.65 of 94 | — | structure | — | BELOW FLOOR |
| 99 | activity | EXTRA | `div.icon.ratio.ratio-16x9.videoSection` | `—` | `iframe` | 3 | 3 | 0.90 of 94 | — | structure | yes | BELOW FLOOR |
| 100 | activity | MISSING | `div.col-12` | `div.row` | `—` | 3 | 3 | 0.11 of 94 | — | structure | — | BELOW FLOOR |
| 321 | body | EXTRA | `div#body` | `—` | `div.row` | 66 | 12 | 0.84 of 94 | template=Standard c=0.84 n=66 | structure | — | CANDIDATE |
| 323 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 33 | 12 | 0.78 of 94 | template=Standard c=0.78 n=33 | structure | — | CANDIDATE |
| 338 | body | EXTRA | `div.row` | `—` | `div.col-12` | 22 | 5 | 0.99 of 94 | template=Standard c=0.99 n=22 | structure | — | CANDIDATE |

## Details — in the companion file `CONVERTER_V2/outputs/_s51_ANZH_miner_details.md`
Every CANDIDATE and every top-40 row has three quoted examples (WT / gold / Claude) there, plus the
below-floor list. **NEVER read the companion whole** (hundreds of KB): `grep -n '^### #<rank> ' CONVERTER_V2/outputs/_diff_queue_details.md` then `sed -n '<start>,<start+40>p'`. The top 25
candidates' detail blocks are repeated below for convenience.

### #60 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `p` — CANDIDATE
- pages 25 / modules 10 / lines 78; consensus (all) 0.98 of 94 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 10m/25p c=0.98
- by subject: ANZH 10m/25p c=0.98
- by era: Refresh 10m/25p c=0.98
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Waka hourua»`
- **ANZH103** ANZH103_1_0.html ↔ ANZH103_3_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Te Tiriti/the Treaty is an __________ between the __________ and Māori.»`
- **ANZH104** ANZH104_6_0.html ↔ ANZH104_06.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «If using paper, you can take a photo of your finished poster and upload it to the dropbox.»`
- modules: ANZH101, ANZH103, ANZH104, ANZH105, ANZH205, ANZH301, ANZH302, ANZH303, ANZH304, ANZH404

### #321 · body · EXTRA · `div#body` › gold `—` vs Claude `div.row` — CANDIDATE
- pages 66 / modules 12 / lines 252; consensus (all) 0.84 of 94 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 12m/66p c=0.84
- by subject: ANZH 12m/66p c=0.84
- by era: Refresh 12m/66p c=0.84
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Nelly in Aotearoa: Tangata Whenua»`
- **ANZH103** ANZH103_1_0.html ↔ ANZH103_3_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Important Words/Ngā Kupu Nui»`
- **ANZH104** ANZH104_3_0.html ↔ ANZH104_03.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Clothing Word Find»`
- modules: ANZH101, ANZH103, ANZH104, ANZH105, ANZH203, ANZH205, ANZH301, ANZH302, ANZH303, ANZH304, ANZH401, ANZH404

### #323 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `p` — CANDIDATE
- pages 33 / modules 12 / lines 65; consensus (all) 0.78 of 94 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 12m/33p c=0.78
- by subject: ANZH 12m/33p c=0.78
- by era: Refresh 12m/33p c=0.78
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Nelly the Godwit and Tane the Tui discussed lots of words related to finding your way across the ocean and to the people»`
- **ANZH103** ANZH103_0_0.html ↔ ANZH103_0_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «In this module you will be learning about what happened on February 6 in the past and why we have a holiday on this day »`
- **ANZH104** ANZH104_4_0.html ↔ ANZH104_04.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «, , and»`
- modules: ANZH101, ANZH103, ANZH104, ANZH105, ANZH203, ANZH205, ANZH301, ANZH302, ANZH303, ANZH304, ANZH401, ANZH404

### #338 · body · EXTRA · `div.row` › gold `—` vs Claude `div.col-12` — CANDIDATE
- pages 22 / modules 5 / lines 33; consensus (all) 0.99 of 94 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 5m/22p c=0.99
- by subject: ANZH 5m/22p c=0.99
- by era: Refresh 5m/22p c=0.99
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH105** ANZH105_6_0.html ↔ ANZH105_06.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12  «Stories are organised by difficulty. Use the available audio clips to support reading the text.»`
- **ANZH302** ANZH302_2_0.html ↔ ANZH302_2_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12  «Lesson summary»`
- **ANZH303** ANZH303_2_0.html ↔ ANZH303_0.2.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12  «Lesson summary:»`
- modules: ANZH105, ANZH302, ANZH303, ANZH304, ANZH401
