# DIFF_QUEUE.md — the diff miner's ranked class queue (LOOP__Autonomous_Rounds.md §1d)

**Produced:** 2026-09-24 15:50 NZST by `reference/tests/_diff_miner.py` on the CURRENT corpus (pageforge-site HEAD 7fd11eb; Claude corpus 545 dirs). **Population:** the skeleton gate's own — 77 paired pages / 8 modules (compare_exclusions.txt honoured; acks / glossary / references pages excluded); parse errors skipped: 0 (must be 0); modules without a parsed WT: 0. Run time 4.5 s.

**What a row is.** One CLASS = (region, parent element, gold form, Claude form, direction) over every differing skeleton line of every paired page — the same lines, labels, widget collapse and difflib alignment the PRIMARY gate scores (each element its own line so it can be quoted). Direction: MISSING = gold has it, Claude lacks it; EXTRA = Claude has it, gold lacks it; SUBSTITUTED = same position, different tag / class / wrapper; MOVED = same text, different place. Consensus = of the gold pages in the group where the region exists, the share carrying the gold form (for EXTRA: the share NOT carrying Claude's form). Derivable = the gold line's text is in the module's parsed Writers Template (round-110 tolerance); structure-only differences are always derivable.

**Candidate rule (§1d).** modules ≥ 10 for a chrome class (module-code / title / header / module-menu / crumbs / phases-nav / footer / acks), pages ≥ 20 for a body / activity class; gold consensus ≥ 0.60 in at least one template or subject group that itself reaches the floor; structure-only or derivable share ≥ 0.60. A class below the floor is listed, never dropped. A CANDIDATE still goes through the PICK's KB-first check, the triangulation and the §3 corpus-wide measurement before any code — this table is the queue, not the verdict.

## Summary

- differing skeleton lines: 7422 — by direction {'MISSING': 3417, 'SUBSTITUTED': 847, 'EXTRA': 2891, 'MOVED': 267}
- by region: {'title': 3, 'module-menu': 154, 'footer': 109, 'acks': 28, 'activity': 2990, 'body': 4112, 'root': 26}
- classes: 774 — CANDIDATE 7, below floor 757, the rest below consensus / not derivable

## Completeness census — the repeating chrome (§1d item 4)

| region | pages with region | gold items | gold items in WT | Claude items | derivable misses | pages with misses | modules with misses | status |
|---|---|---|---|---|---|---|---|---|
| module-menu | 69 | 345 | 329 | 276 | 75 | 31 | 5 | BELOW FLOOR |
| crumbs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |
| phases-nav | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |
| footer | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |

- **module-menu** by template: Standard 5m/31p/75 misses
  - HIS1003 HIS1003_7_0.html: gold 7 items (7 in WT) / Claude 0 — 7 derivable misses, e.g. p «Exploring a range of perspectives on the 1951 Waterfront Dispute» · p «In this lesson you are learning to understand that there are a related to the 19»
  - HIS1001 HIS1001_5_0.html: gold 8 items (5 in WT) / Claude 0 — 5 derivable misses, e.g. h3 «Lesson Overview» · p «We are learning to:»
  - HIS1001 HIS1001_7_0.html: gold 6 items (5 in WT) / Claude 0 — 5 derivable misses, e.g. h3 «Lesson Overview» · p «We are learning to:»
  - HIS1003 HIS1003_2_0.html: gold 5 items (5 in WT) / Claude 0 — 5 derivable misses, e.g. p «This lesson covers the whakapapa of protest in Aotearoa New Zealand.» · p «In this lesson you are learning to understand that there are (political, economi»
- **crumbs** by template: 
- **phases-nav** by template: 
- **footer** by template: 

## Chrome facts — the header and footer as SETS per page (alignment-free; §1d items 2 + 4)

A fact is one thing a page's chrome has: `header:chip` (the `#module-code` div), `header:chip=module-code` / `=lesson-number` / `=lesson-number(00)`, `header:head-buttons`, `header:menu-content`, `header:title-h1-count=N`, `footer:present`, `footer:ul=<classes>`, `footer:link=prev-lesson` / `next-lesson` / `home-nav`, `footer:links=<order>`, `footer:inside-body`, `nav:crumbs`, `nav:phases`. MISSING = the gold page has the fact and Claude's does not; EXTRA the reverse. Consensus = the share of gold pages in the group that have (MISSING) / lack (EXTRA) the fact. Floor 10 modules.

| # | dir | fact | pages | modules | gold share (all) | consensus (all) | best group | status |
|---|---|---|---|---|---|---|---|---|
| F1 | EXTRA | `header:chip=decimal-number` | 18 | 3 | 0.68 | 0.33 | — | BELOW FLOOR |
| F2 | MISSING | `header:chip=lesson-number` | 17 | 2 | 0.22 | 0.22 | — | BELOW FLOOR |
| F3 | MISSING | `header:title-h1-count=2` | 2 | 2 | 0.12 | 0.12 | — | BELOW FLOOR |
| F4 | EXTRA | `header:title-h1-count=1` | 2 | 2 | 0.88 | 0.12 | — | BELOW FLOOR |
| F5 | MISSING | `header:title-h1-count=1` | 1 | 1 | 0.88 | 0.88 | — | BELOW FLOOR |
| F6 | EXTRA | `header:title-h1-count=2` | 1 | 1 | 0.12 | 0.88 | — | BELOW FLOOR |
| F7 | MISSING | `header:chip=module-code` | 1 | 1 | 0.10 | 0.10 | — | BELOW FLOOR |
| F8 | MISSING | `footer:links=home-nav,next-lesson` | 7 | 7 | 0.09 | 0.09 | — | BELOW FLOOR |
| F9 | EXTRA | `footer:links=next-lesson,home-nav` | 7 | 7 | 0.00 | 1.00 | — | BELOW FLOOR |
| F10 | MISSING | `footer:inside-body` | 8 | 4 | 0.10 | 0.10 | — | BELOW FLOOR |
| F11 | EXTRA | `footer:links=prev-lesson,home-nav` | 3 | 3 | 0.07 | 0.94 | — | BELOW FLOOR |
| F12 | EXTRA | `footer:links=prev-lesson,next-lesson,home-nav` | 10 | 2 | 0.71 | 0.29 | — | BELOW FLOOR |
| F13 | MISSING | `footer:link=next-lesson` | 2 | 2 | 0.92 | 0.92 | — | BELOW FLOOR |
| F14 | MISSING | `footer:links=prev-lesson,next-lesson,home-nav` | 2 | 2 | 0.71 | 0.71 | — | BELOW FLOOR |
| F15 | MISSING | `footer:link=other` | 10 | 1 | 0.13 | 0.13 | — | BELOW FLOOR |
| F16 | MISSING | `footer:links=prev-lesson,other,next-lesson,home-nav` | 8 | 1 | 0.10 | 0.10 | — | BELOW FLOOR |
| F17 | MISSING | `footer:links=other,next-lesson,home-nav` | 1 | 1 | 0.01 | 0.01 | — | BELOW FLOOR |
| F18 | EXTRA | `footer:link=prev-lesson` | 1 | 1 | 0.90 | 0.10 | — | BELOW FLOOR |
| F19 | MISSING | `footer:links=prev-lesson,other,home-nav` | 1 | 1 | 0.01 | 0.01 | — | BELOW FLOOR |
| F20 | MISSING | `footer:links=prev-lesson,home-nav` | 1 | 1 | 0.07 | 0.07 | — | BELOW FLOOR |
| F21 | EXTRA | `footer:link=next-lesson` | 1 | 1 | 0.92 | 0.08 | — | BELOW FLOOR |


## The ranked queue — chrome regions first, then by modules affected

| # | region | dir | parent | gold form | Claude form | pages | modules | consensus (all) | best group | derivable | KB | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | title | MISSING | `div#header` | `h1>span` | `—` | 2 | 2 | 0.12 of 77 | — | 1.00 | yes | BELOW FLOOR |
| 2 | title | EXTRA | `div#header` | `—` | `h1>span` | 1 | 1 | 0.88 of 77 | — | structure | yes | BELOW FLOOR |
| 3 | module-menu | SUBSTITUTED | `div.row` | `div.col-12` | `div.col-12.col-md-8` | 50 | 6 | 0.65 of 77 | — | structure | — | BELOW FLOOR |
| 4 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 14 | 2 | 0.75 of 77 | — | structure | — | BELOW FLOOR |
| 5 | module-menu | MISSING | `div.col-12.col-md-8` | `p` | `—` | 14 | 2 | 0.25 of 77 | — | 1.00 | — | BELOW FLOOR |
| 6 | module-menu | MOVED | `div.col-12.col-md-8` | `p` | `p` | 5 | 2 | 0.25 of 77 | — | structure | — | BELOW FLOOR |
| 7 | module-menu | MISSING | `ul` | `li` | `—` | 2 | 2 | 0.42 of 77 | — | 1.00 | — | BELOW FLOOR |
| 8 | module-menu | MISSING | `div.col-12` | `p` | `—` | 7 | 1 | 0.09 of 77 | — | 1.00 | — | BELOW FLOOR |
| 9 | module-menu | MISSING | `div.col-12` | `h3` | `—` | 6 | 1 | 0.09 of 77 | — | 1.00 | — | BELOW FLOOR |
| 10 | module-menu | MISSING | `div.col-12` | `ul` | `—` | 6 | 1 | 0.65 of 77 | — | 0.42 | — | BELOW FLOOR |
| 11 | module-menu | MISSING | `div.col-12.col-md-8` | `p>b` | `—` | 3 | 1 | 0.04 of 77 | — | 1.00 | — | BELOW FLOOR |
| 12 | module-menu | SUBSTITUTED | `div.col-12` | `h5` | `p` | 2 | 1 | 0.56 of 77 | — | structure | — | BELOW FLOOR |
| 13 | module-menu | SUBSTITUTED | `div.col-12` | `h3` | `h5` | 1 | 1 | 0.09 of 77 | — | structure | — | BELOW FLOOR |
| 14 | module-menu | SUBSTITUTED | `div.col-12` | `p` | `h5` | 1 | 1 | 0.09 of 77 | — | structure | — | BELOW FLOOR |
| 15 | module-menu | SUBSTITUTED | `div.row` | `WIDGET` | `div.col-12.col-md-8` | 1 | 1 | 0.10 of 77 | — | structure | — | BELOW FLOOR |
| 16 | module-menu | SUBSTITUTED | `div.col-12` | `ul` | `p` | 1 | 1 | 0.65 of 77 | — | structure | — | BELOW FLOOR |
| 17 | footer | MISSING | `ul.footer-nav` | `li>a#next-lesson` | `—` | 11 | 4 | 0.92 of 77 | — | structure | yes | BELOW FLOOR |
| 18 | footer | EXTRA | `body.container-fluid` | `—` | `div#footer` | 8 | 4 | 0.12 of 77 | — | structure | yes | BELOW FLOOR |
| 19 | footer | EXTRA | `li>a#next-lesson` | `—` | `a#next-lesson` | 4 | 4 | 0.08 of 77 | — | structure | yes | BELOW FLOOR |
| 20 | footer | EXTRA | `ul.footer-nav` | `—` | `li>a.home-nav` | 4 | 4 | 0.00 of 77 | — | structure | yes | BELOW FLOOR |
| 21 | footer | MISSING | `div#body` | `div#footer` | `—` | 5 | 3 | 0.10 of 77 | — | structure | yes | BELOW FLOOR |
| 22 | footer | MISSING | `div#footer` | `ul.footer-nav` | `—` | 2 | 2 | 1.00 of 77 | — | structure | yes | BELOW FLOOR |
| 23 | footer | MISSING | `ul.footer-nav` | `li>a.home-nav` | `—` | 2 | 2 | 1.00 of 77 | — | structure | yes | BELOW FLOOR |
| 24 | footer | SUBSTITUTED | `div#body` | `div#footer` | `div.col-12.col-md-8` | 2 | 2 | 0.10 of 77 | — | structure | yes | BELOW FLOOR |
| 25 | footer | SUBSTITUTED | `ul.footer-nav` | `li>a#prev-lesson` | `p` | 2 | 2 | 0.90 of 77 | — | structure | yes | BELOW FLOOR |
| 26 | footer | SUBSTITUTED | `ul.footer-nav` | `li>a#next-lesson` | `div.activity` | 2 | 2 | 0.92 of 77 | — | structure | yes | BELOW FLOOR |
| 27 | footer | MISSING | `li>a.active` | `a.active` | `—` | 9 | 1 | 0.13 of 77 | — | structure | yes | BELOW FLOOR |
| 28 | footer | MISSING | `div.row` | `div#footer` | `—` | 1 | 1 | 0.01 of 77 | — | structure | yes | BELOW FLOOR |
| 29 | footer | MISSING | `li>a#next-lesson` | `a#next-lesson` | `—` | 1 | 1 | 0.92 of 77 | — | structure | yes | BELOW FLOOR |
| 30 | footer | SUBSTITUTED | `ul.footer-nav` | `li>a#prev-lesson` | `li` | 1 | 1 | 0.90 of 77 | — | structure | yes | BELOW FLOOR |
| 31 | footer | SUBSTITUTED | `ul.footer-nav` | `li>a#next-lesson` | `h4.goJournal` | 1 | 1 | 0.92 of 77 | — | structure | yes | BELOW FLOOR |
| 32 | footer | SUBSTITUTED | `li>a.active` | `a.active` | `a#prev-lesson` | 1 | 1 | 0.13 of 77 | — | structure | yes | BELOW FLOOR |
| 33 | footer | SUBSTITUTED | `div#body` | `div#footer` | `div#footer` | 1 | 1 | 0.10 of 77 | — | structure | yes | BELOW FLOOR |
| 34 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav` | `ul.footer-nav` | 1 | 1 | 1.00 of 77 | — | structure | yes | BELOW FLOOR |
| 35 | footer | SUBSTITUTED | `ul.footer-nav` | `li>a.home-nav` | `li>a#next-lesson` | 1 | 1 | 1.00 of 77 | — | structure | yes | BELOW FLOOR |
| 36 | footer | SUBSTITUTED | `ul.footer-nav` | `li>a#next-lesson` | `li>a.home-nav` | 1 | 1 | 0.92 of 77 | — | structure | yes | BELOW FLOOR |
| 37 | acks | MISSING | `div.acks` | `WIDGET` | `—` | 1 | 1 | 0.10 of 77 | — | structure | yes | BELOW FLOOR |
| 38 | acks | SUBSTITUTED | `div.col-12.col-md-8` | `div.acks` | `h3` | 1 | 1 | 0.10 of 77 | — | structure | yes | BELOW FLOOR |
| 39 | activity | MISSING | `div.col-12` | `a` | `—` | 42 | 8 | 0.38 of 77 | — | 0.81 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 40 | activity | MISSING | `a` | `div.button` | `—` | 40 | 8 | 0.48 of 77 | — | 0.86 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 41 | activity | MISSING | `div.col-12` | `p` | `—` | 26 | 8 | 0.31 of 77 | — | 0.91 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 42 | activity | EXTRA | `div.col-12` | `—` | `p` | 36 | 7 | 0.82 of 77 | template=Standard c=0.82 n=36 | structure | — | CANDIDATE |
| 43 | activity | EXTRA | `div.col-12` | `—` | `h4.goJournal` | 27 | 7 | 1.00 of 77 | template=Standard c=1.00 n=27 | structure | — | CANDIDATE |
| 44 | activity | SUBSTITUTED | `div.col-12` | `a` | `h4.goJournal` | 25 | 6 | 0.83 of 77 | ptype=lesson c=0.91 n=25 | structure | — | CANDIDATE |
| 45 | activity | MISSING | `div.col-12` | `WIDGET` | `—` | 15 | 6 | 0.18 of 77 | — | structure | — | BELOW FLOOR |
| 46 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.alertPadding[number=*]` | `div.activity[number=*]` | 12 | 6 | 0.33 of 77 | — | structure | yes | BELOW FLOOR |
| 47 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `div.activity[number=*]` | 11 | 6 | 0.65 of 77 | — | structure | yes | BELOW FLOOR |
| 48 | activity | EXTRA | `p` | `—` | `b` | 10 | 6 | 0.95 of 77 | — | structure | — | BELOW FLOOR |
| 49 | activity | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `div.col-12` | 9 | 6 | 0.20 of 77 | — | structure | — | BELOW FLOOR |
| 50 | activity | SUBSTITUTED | `div.icon.ratio.ratio-16x9.videoSection` | `iframe.embed-responsive-item` | `iframe` | 23 | 5 | 0.43 of 77 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 51 | activity | EXTRA | `div.col-12` | `—` | `WIDGET` | 15 | 5 | 0.82 of 77 | — | structure | — | BELOW FLOOR |
| 52 | activity | EXTRA | `div.col-12` | `—` | `ol` | 13 | 5 | 0.79 of 77 | — | structure | — | BELOW FLOOR |
| 53 | activity | EXTRA | `div.col-12` | `—` | `div.icon.ratio.ratio-16x9.videoSection` | 11 | 5 | 0.78 of 77 | — | structure | yes | BELOW FLOOR |
| 54 | activity | MISSING | `div.col-12` | `ol` | `—` | 11 | 5 | 0.21 of 77 | — | 1.00 | — | BELOW FLOOR |
| 55 | activity | MISSING | `div.col-12` | `h5` | `—` | 11 | 5 | 0.21 of 77 | — | 1.00 | — | BELOW FLOOR |
| 56 | activity | MISSING | `div.col-12` | `div.clickDropContent` | `—` | 7 | 5 | 0.07 of 77 | — | 0.88 | — | BELOW FLOOR |
| 57 | activity | MOVED | `div.col-12` | `h3` | `h3` | 7 | 5 | 0.51 of 77 | — | structure | — | BELOW FLOOR |
| 58 | activity | MISSING | `div.row` | `div.col-12` | `—` | 6 | 5 | 0.29 of 77 | — | 1.00 | — | BELOW FLOOR |
| 59 | activity | MOVED | `div.col-12` | `p` | `p` | 9 | 4 | 0.18 of 77 | — | structure | — | BELOW FLOOR |
| 60 | activity | MISSING | `div.col-12` | `br` | `—` | 8 | 4 | 0.22 of 77 | — | structure | — | BELOW FLOOR |
| 61 | activity | EXTRA | `p>b` | `—` | `b` | 7 | 4 | 0.82 of 77 | — | structure | — | BELOW FLOOR |
| 62 | activity | MISSING | `div.col-12` | `div.icon.ratio.ratio-16x9.videoSection` | `—` | 7 | 4 | 0.22 of 77 | — | structure | yes | BELOW FLOOR |
| 63 | activity | MISSING | `a` | `div.externalButton` | `—` | 6 | 4 | 0.30 of 77 | — | 0.67 | — | BELOW FLOOR |
| 64 | activity | MISSING | `div.col-12` | `h3` | `—` | 6 | 4 | 0.26 of 77 | — | 0.67 | — | BELOW FLOOR |
| 65 | activity | MISSING | `p` | `b` | `—` | 6 | 4 | 0.18 of 77 | — | 1.00 | — | BELOW FLOOR |
| 66 | activity | MOVED | `div.col-12` | `p` | `p` | 6 | 4 | 0.57 of 77 | — | structure | — | BELOW FLOOR |
| 67 | activity | SUBSTITUTED | `a` | `div.button` | `div.externalButton` | 6 | 4 | 0.86 of 77 | — | structure | yes | BELOW FLOOR |
| 68 | activity | MISSING | `li` | `br` | `—` | 5 | 4 | 0.05 of 77 | — | structure | — | BELOW FLOOR |
| 69 | activity | MISSING | `p>b` | `b` | `—` | 5 | 4 | 0.18 of 77 | — | 1.00 | — | BELOW FLOOR |
| 70 | activity | EXTRA | `div.col-12` | `—` | `p>a` | 4 | 4 | 1.00 of 77 | — | structure | — | BELOW FLOOR |
| 71 | activity | EXTRA | `div.activity` | `—` | `div.row` | 4 | 4 | 0.95 of 77 | — | structure | yes | BELOW FLOOR |
| 72 | activity | MISSING | `div.col-12` | `ul` | `—` | 4 | 4 | 0.21 of 77 | — | 0.75 | — | BELOW FLOOR |
| 73 | activity | MISSING | `p>span.infoTrigger` | `span.infoTrigger` | `—` | 4 | 4 | 0.13 of 77 | — | 1.00 | — | BELOW FLOOR |
| 74 | activity | MISSING | `div.col-12` | `div.row` | `—` | 4 | 4 | 0.08 of 77 | — | structure | — | BELOW FLOOR |
| 75 | activity | EXTRA | `div.activity[number=*]` | `—` | `div.row` | 11 | 3 | 1.00 of 77 | — | structure | yes | BELOW FLOOR |
| 76 | activity | EXTRA | `div.col-12` | `—` | `p>b` | 9 | 3 | 0.86 of 77 | — | structure | — | BELOW FLOOR |
| 77 | activity | EXTRA | `a` | `—` | `div.externalButton` | 8 | 3 | 0.90 of 77 | — | structure | — | BELOW FLOOR |
| 78 | activity | EXTRA | `div.activity.interactive[number=*]` | `—` | `div.row` | 6 | 3 | 0.95 of 77 | — | structure | yes | BELOW FLOOR |
| 79 | activity | EXTRA | `div.col-12` | `—` | `p>i` | 6 | 3 | 0.95 of 77 | — | structure | — | BELOW FLOOR |
| 80 | activity | EXTRA | `div.col-12` | `—` | `img.img-fluid` | 6 | 3 | 1.00 of 77 | — | structure | — | BELOW FLOOR |
| 81 | activity | MISSING | `p` | `br` | `—` | 6 | 3 | 0.08 of 77 | — | structure | — | BELOW FLOOR |
| 82 | activity | SUBSTITUTED | `a` | `div.button` | `div.button` | 6 | 3 | 0.86 of 77 | — | structure | yes | BELOW FLOOR |
| 83 | activity | EXTRA | `p>a` | `—` | `a` | 5 | 3 | 1.00 of 77 | — | structure | — | BELOW FLOOR |
| 84 | activity | MISSING | `div.activity.interactive[number=*]` | `div.row` | `—` | 5 | 3 | 0.13 of 77 | — | 1.00 | yes | BELOW FLOOR |
| 85 | activity | MISSING | `ol` | `li` | `—` | 5 | 3 | 0.39 of 77 | — | 1.00 | — | BELOW FLOOR |
| 86 | activity | EXTRA | `ol` | `—` | `li` | 4 | 3 | 0.95 of 77 | — | structure | — | BELOW FLOOR |
| 87 | activity | MISSING | `div.clickDropContent` | `p` | `—` | 4 | 3 | 0.08 of 77 | — | 0.79 | — | BELOW FLOOR |
| 88 | activity | MISSING | `div.col-12.col-md-8` | `p` | `—` | 4 | 3 | 0.05 of 77 | — | 1.00 | — | BELOW FLOOR |
| 89 | activity | MISSING | `p` | `span.infoTrigger` | `—` | 4 | 3 | 0.05 of 77 | — | 1.00 | — | BELOW FLOOR |
| 90 | activity | MOVED | `div.col-12` | `h3` | `h3` | 4 | 3 | 0.51 of 77 | — | structure | — | BELOW FLOOR |
| 91 | activity | MOVED | `ol` | `li` | `li` | 4 | 3 | 0.13 of 77 | — | structure | — | BELOW FLOOR |
| 92 | activity | MOVED | `a` | `div.button` | `div.button` | 4 | 3 | 0.09 of 77 | — | structure | yes | BELOW FLOOR |
| 93 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `p` | 4 | 3 | 0.60 of 77 | — | structure | — | BELOW FLOOR |
| 94 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `div.activity[number=*]` | 4 | 3 | 0.21 of 77 | — | structure | yes | BELOW FLOOR |
| 95 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.alertPadding.dropbox[number=*]` | `div.activity[number=*]` | 4 | 3 | 0.10 of 77 | — | structure | yes | BELOW FLOOR |
| 96 | activity | SUBSTITUTED | `div.col-12` | `p` | `WIDGET` | 4 | 3 | 0.90 of 77 | — | structure | — | BELOW FLOOR |
| 97 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.dropbox[number=*]` | `div.activity[number=*]` | 4 | 3 | 0.18 of 77 | — | structure | yes | BELOW FLOOR |
| 98 | activity | EXTRA | `div.col-12` | `—` | `div.button` | 3 | 3 | 1.00 of 77 | — | structure | yes | BELOW FLOOR |
| 99 | activity | MISSING | `div.activity.dropbox[number=*]` | `div.row` | `—` | 3 | 3 | 0.03 of 77 | — | 1.00 | yes | BELOW FLOOR |
| 100 | activity | MISSING | `b>i` | `i` | `—` | 3 | 3 | 0.04 of 77 | — | 1.00 | — | BELOW FLOOR |
| 375 | body | EXTRA | `div#body` | `—` | `div.row` | 64 | 8 | 0.87 of 77 | template=Standard c=0.87 n=64 | structure | — | CANDIDATE |
| 377 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 38 | 8 | 0.81 of 77 | template=Standard c=0.81 n=38 | structure | — | CANDIDATE |
| 383 | body | EXTRA | `div.col-12.col-md-8` | `—` | `img.img-fluid` | 23 | 6 | 1.00 of 77 | template=Standard c=1.00 n=23 | structure | — | CANDIDATE |
| 384 | body | SUBSTITUTED | `div.col-12.col-md-8` | `div.alert.solid` | `div.alert` | 21 | 6 | 0.58 of 77 | ptype=lesson c=0.64 n=21 | structure | yes | CANDIDATE |

## Details — in the companion file `CONVERTER_V2/outputs/_diff_queue_details.md`
Every CANDIDATE and every top-40 row has three quoted examples (WT / gold / Claude) there, plus the
below-floor list. **NEVER read the companion whole** (hundreds of KB): `grep -n '^### #<rank> ' CONVERTER_V2/outputs/_diff_queue_details.md` then `sed -n '<start>,<start+40>p'`. The top 25
candidates' detail blocks are repeated below for convenience.

### #42 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `p` — CANDIDATE
- pages 36 / modules 7 / lines 72; consensus (all) 0.82 of 77 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 7m/36p c=0.82
- by subject: NCEA1 7m/36p c=0.82
- by era: Refresh 7m/36p c=0.82
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **HIS1002** HIS1002_1_0.html ↔ HIS1002-1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «1.»`
- **HIS1003** HIS1003_2_0.html ↔ HIS1003_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «When analysing people’s actions, it is important to consider someone took action and not another kind of action. Using t»`
- **HIS1004** HIS1004_4_0.html ↔ HIS1004_4.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Drag and drop the following quoted evidence from this documentary into the appropriate column.»`
- modules: HIS1002, HIS1003, HIS1004, HIS1005, HIS1006, HIS1007, HIS1008

### #43 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `h4.goJournal` — CANDIDATE
- pages 27 / modules 7 / lines 32; consensus (all) 1.00 of 77 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 7m/27p c=1.00
- by subject: NCEA1 7m/27p c=1.00
- by era: Refresh 7m/27p c=1.00
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **HIS1002** HIS1002_3_0.html ↔ HIS1002-3.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h4.goJournal  «Go to your journal»`
- **HIS1003** HIS1003_6_0.html ↔ HIS1003_6.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h4.goJournal  «Go to your journal»`
- **HIS1004** HIS1004_5_0.html ↔ HIS1004_5.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h4.goJournal  «Go to your journal»`
- modules: HIS1002, HIS1003, HIS1004, HIS1005, HIS1006, HIS1007, HIS1008

### #44 · activity · SUBSTITUTED · `div.col-12` › gold `a` vs Claude `h4.goJournal` — CANDIDATE
- pages 25 / modules 6 / lines 43; consensus (all) 0.83 of 77 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 6m/25p c=0.83
- by subject: NCEA1 6m/25p c=0.83
- by era: Refresh 6m/25p c=0.83
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **HIS1002** HIS1002_1_0.html ↔ HIS1002-1.0.html (structure, derivable=True)
  - gold: `a  «Go to journal»`
  - Claude: `h4.goJournal  «Go to your journal»`
- **HIS1004** HIS1004_9_0.html ↔ HIS1004_9.0.html (structure, derivable=True)
  - gold: `a  «Go to journal»`
  - Claude: `h4.goJournal  «Go to your journal»`
- **HIS1005** HIS1005_1_0.html ↔ HIS1005-1.0.html (structure, derivable=True)
  - gold: `a  «NZ Archives»`
  - Claude: `h4.goJournal  «Go to your journal»`
- modules: HIS1002, HIS1004, HIS1005, HIS1006, HIS1007, HIS1008

### #375 · body · EXTRA · `div#body` › gold `—` vs Claude `div.row` — CANDIDATE
- pages 64 / modules 8 / lines 318; consensus (all) 0.87 of 77 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 8m/64p c=0.87
- by subject: NCEA1 8m/64p c=0.87
- by era: Refresh 8m/64p c=0.87
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **HIS1001** HIS1001_8_0.html ↔ HIS1001-8.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «History never stays in the past»`
- **HIS1002** HIS1002_1_0.html ↔ HIS1002-1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «In 1963, the United Kingdom (UK), United States (US) and Union of Soviet Socialist Republics (USSR) signed an agreement »`
- **HIS1003** HIS1003_1_0.html ↔ HIS1003_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «The United Nations and the Universal Declaration of Human Rights»`
- modules: HIS1001, HIS1002, HIS1003, HIS1004, HIS1005, HIS1006, HIS1007, HIS1008

### #377 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `p` — CANDIDATE
- pages 38 / modules 8 / lines 116; consensus (all) 0.81 of 77 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 8m/38p c=0.81
- by subject: NCEA1 8m/38p c=0.81
- by era: Refresh 8m/38p c=0.81
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **HIS1001** HIS1001_0_0.html ↔ HIS1001-0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «You can see that there are many factors that influence perspective. When investigating different perspectives, we need t»`
- **HIS1002** HIS1002_1_0.html ↔ HIS1002-1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «1.»`
- **HIS1003** HIS1003_3_0.html ↔ HIS1003_3.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «The learning in this lesson links to the previous lesson and the fundamental lesson, HISFUN05. If you have not yet compl»`
- modules: HIS1001, HIS1002, HIS1003, HIS1004, HIS1005, HIS1006, HIS1007, HIS1008

### #383 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `img.img-fluid` — CANDIDATE
- pages 23 / modules 6 / lines 50; consensus (all) 1.00 of 77 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 6m/23p c=1.00
- by subject: NCEA1 6m/23p c=1.00
- by era: Refresh 6m/23p c=1.00
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **HIS1001** HIS1001_5_0.html ↔ HIS1001-5.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- **HIS1002** HIS1002_3_0.html ↔ HIS1002-3.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- **HIS1005** HIS1005_9_0.html ↔ HIS1005-9.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- modules: HIS1001, HIS1002, HIS1005, HIS1006, HIS1007, HIS1008

### #384 · body · SUBSTITUTED · `div.col-12.col-md-8` › gold `div.alert.solid` vs Claude `div.alert` — CANDIDATE
- pages 21 / modules 6 / lines 21; consensus (all) 0.58 of 77 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 6m/21p c=0.58
- by subject: NCEA1 6m/21p c=0.58
- by era: Refresh 6m/21p c=0.58
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: INDEX.md:81 — - Sections: COMP_14 — Layout & Structure · Activities · Alerts (Cultural Alert · Translate Section in Alert Solid · Activity Image Sidebar · Activity 
  - KB: 01_PIPELINE_EXTRACTION_TAGS/01F_TAG_INTERPRETATION_STYLING_ACTIVITIES.md:11 — | `important` | `<div class="alert solid"><div class="row"><div class="col-12"><p>content</p></div></div></div>` |
  - KB: 05_COMP_LANGUAGE_MEDIA_LAYOUT/05B_COMP14_LAYOUT_STRUCTURE.md:119 — <div class="alert solid"><div class="row"><div class="col-12"><p>Content</p></div></div></div>
- **HIS1003** HIS1003_1_0.html ↔ HIS1003_1.0.html (structure, derivable=True)
  - gold: `div.alert.solid  «Lesson Summary»`
  - Claude: `div.alert  «You can explain the overall purpose and whakapapa of the United Nations Organisation and the Universal Declaration of Hu»`
- **HIS1004** HIS1004_3_0.html ↔ HIS1004_3.0.html (structure, derivable=True)
  - gold: `div.alert.solid  «Lesson summary»`
  - Claude: `div.alert  «You can select and quote relevant evidence from a source and use the 5 Ws and H to summarise a key event in the resistan»`
- **HIS1005** HIS1005_4_0.html ↔ HIS1005-4.0.html (structure, derivable=True)
  - gold: `div.alert.solid  «Lesson summary»`
  - Claude: `div.alert  «Lesson Summary»`
- modules: HIS1003, HIS1004, HIS1005, HIS1006, HIS1007, HIS1008
