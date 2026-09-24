# DIFF_QUEUE.md — the diff miner's ranked class queue (LOOP__Autonomous_Rounds.md §1d)

**Produced:** 2026-09-24 20:09 NZST by `reference/tests/_diff_miner.py` on the CURRENT corpus (pageforge-site HEAD adede3b; Claude corpus 545 dirs). **Population:** the skeleton gate's own — 66 paired pages / 10 modules (compare_exclusions.txt honoured; acks / glossary / references pages excluded); parse errors skipped: 0 (must be 0); modules without a parsed WT: 0. Run time 3.9 s.

**What a row is.** One CLASS = (region, parent element, gold form, Claude form, direction) over every differing skeleton line of every paired page — the same lines, labels, widget collapse and difflib alignment the PRIMARY gate scores (each element its own line so it can be quoted). Direction: MISSING = gold has it, Claude lacks it; EXTRA = Claude has it, gold lacks it; SUBSTITUTED = same position, different tag / class / wrapper; MOVED = same text, different place. Consensus = of the gold pages in the group where the region exists, the share carrying the gold form (for EXTRA: the share NOT carrying Claude's form). Derivable = the gold line's text is in the module's parsed Writers Template (round-110 tolerance); structure-only differences are always derivable.

**Candidate rule (§1d).** modules ≥ 10 for a chrome class (module-code / title / header / module-menu / crumbs / phases-nav / footer / acks), pages ≥ 20 for a body / activity class; gold consensus ≥ 0.60 in at least one template or subject group that itself reaches the floor; structure-only or derivable share ≥ 0.60. A class below the floor is listed, never dropped. A CANDIDATE still goes through the PICK's KB-first check, the triangulation and the §3 corpus-wide measurement before any code — this table is the queue, not the verdict.

## Summary

- differing skeleton lines: 7094 — by direction {'SUBSTITUTED': 624, 'MISSING': 3381, 'MOVED': 242, 'EXTRA': 2847}
- by region: {'title': 13, 'module-menu': 123, 'footer': 97, 'acks': 28, 'activity': 2813, 'body': 3992, 'root': 28}
- classes: 672 — CANDIDATE 5, below floor 664, the rest below consensus / not derivable

## Completeness census — the repeating chrome (§1d item 4)

| region | pages with region | gold items | gold items in WT | Claude items | derivable misses | pages with misses | modules with misses | status |
|---|---|---|---|---|---|---|---|---|
| module-menu | 55 | 355 | 339 | 314 | 43 | 18 | 4 | BELOW FLOOR |
| crumbs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |
| phases-nav | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |
| footer | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |

- **module-menu** by template: flat 4m/18p/43 misses
  - XDLS909/ XDLS909_1_0.html: gold 9 items (8 in WT) / Claude 0 — 8 derivable misses, e.g. li «to understand what the Aotearoa New Zealand Census is and how it helps us learn » · li «what a census is and how it is used to gather information about the diversity of»
  - XDLS909/ XDLS909_3_0.html: gold 8 items (6 in WT) / Claude 0 — 6 derivable misses, e.g. li «what are the rights and responsibilities of a resident and citizen of Aotearoa N» · li «ways that we can have our say in Aotearoa New Zealand as residents and citizens.»
  - XDLS902/ XDLS902_2_0.html: gold 5 items (5 in WT) / Claude 0 — 5 derivable misses, e.g. h5 «We are learning:» · li «how food is important for our bodies and for spending time with loved ones»
  - XDLS909/ XDLS909_4_0.html: gold 8 items (5 in WT) / Claude 0 — 5 derivable misses, e.g. li «to understand what rights and responsibilities we have when living in Aotearoa N» · li «to know what our human rights are and what our rights as consumers are when purc»
- **crumbs** by template: 
- **phases-nav** by template: 
- **footer** by template: 

## Chrome facts — the header and footer as SETS per page (alignment-free; §1d items 2 + 4)

A fact is one thing a page's chrome has: `header:chip` (the `#module-code` div), `header:chip=module-code` / `=lesson-number` / `=lesson-number(00)`, `header:head-buttons`, `header:menu-content`, `header:title-h1-count=N`, `footer:present`, `footer:ul=<classes>`, `footer:link=prev-lesson` / `next-lesson` / `home-nav`, `footer:links=<order>`, `footer:inside-body`, `nav:crumbs`, `nav:phases`. MISSING = the gold page has the fact and Claude's does not; EXTRA the reverse. Consensus = the share of gold pages in the group that have (MISSING) / lack (EXTRA) the fact. Floor 10 modules.

| # | dir | fact | pages | modules | gold share (all) | consensus (all) | best group | status |
|---|---|---|---|---|---|---|---|---|
| F1 | EXTRA | `header:chip=decimal-number` | 36 | 7 | 0.30 | 0.70 | — | BELOW FLOOR |
| F2 | MISSING | `header:chip=lesson-number` | 35 | 6 | 0.53 | 0.53 | — | BELOW FLOOR |
| F3 | MISSING | `header:title-h1-count=2` | 11 | 4 | 0.24 | 0.24 | — | BELOW FLOOR |
| F4 | EXTRA | `header:title-h1-count=1` | 11 | 4 | 0.76 | 0.24 | — | BELOW FLOOR |
| F5 | MISSING | `header:title-h1-count=1` | 2 | 2 | 0.76 | 0.76 | — | BELOW FLOOR |
| F6 | EXTRA | `header:title-h1-count=2` | 2 | 2 | 0.24 | 0.76 | — | BELOW FLOOR |
| F7 | MISSING | `header:chip=other` | 1 | 1 | 0.17 | 0.17 | — | BELOW FLOOR |
| F8 | EXTRA | `footer:links=next-lesson,home-nav` | 9 | 9 | 0.01 | 0.98 | — | BELOW FLOOR |
| F9 | EXTRA | `footer:link=next-lesson` | 36 | 6 | 0.30 | 0.70 | — | BELOW FLOOR |
| F10 | MISSING | `footer:links=home-nav` | 6 | 6 | 0.09 | 0.09 | — | BELOW FLOOR |
| F11 | MISSING | `footer:links=prev-lesson,home-nav` | 30 | 5 | 0.61 | 0.61 | — | BELOW FLOOR |
| F12 | EXTRA | `footer:links=prev-lesson,next-lesson,home-nav` | 30 | 5 | 0.24 | 0.76 | — | BELOW FLOOR |
| F13 | MISSING | `footer:links=home-nav,next-lesson` | 3 | 3 | 0.04 | 0.04 | — | BELOW FLOOR |
| F14 | MISSING | `footer:ul=footer-nav inquiry-nav` | 2 | 1 | 0.03 | 0.03 | — | BELOW FLOOR |
| F15 | EXTRA | `footer:ul=footer-nav` | 2 | 1 | 0.97 | 0.03 | — | BELOW FLOOR |
| F16 | MISSING | `footer:inside-body` | 1 | 1 | 0.01 | 0.01 | — | BELOW FLOOR |


## The ranked queue — chrome regions first, then by modules affected

| # | region | dir | parent | gold form | Claude form | pages | modules | consensus (all) | best group | derivable | KB | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | title | MISSING | `div#header` | `h1>span` | `—` | 11 | 4 | 0.24 of 66 | — | 0.82 | yes | BELOW FLOOR |
| 2 | title | EXTRA | `div#header` | `—` | `h1>span` | 2 | 2 | 0.76 of 66 | — | structure | yes | BELOW FLOOR |
| 3 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-12.paddingR` | `div.col-12.col-md-8` | 29 | 5 | 0.44 of 66 | — | structure | yes | BELOW FLOOR |
| 4 | module-menu | MISSING | `div.col-12.col-md-12.paddingR` | `p` | `—` | 9 | 3 | 0.44 of 66 | — | 1.00 | yes | BELOW FLOOR |
| 5 | module-menu | MISSING | `div.col-12.col-md-8` | `p` | `—` | 4 | 3 | 0.21 of 66 | — | 0.67 | — | BELOW FLOOR |
| 6 | module-menu | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `h5` | 12 | 2 | 0.21 of 66 | — | structure | — | BELOW FLOOR |
| 7 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `h5` | 3 | 2 | 0.91 of 66 | — | structure | — | BELOW FLOOR |
| 8 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 2 | 2 | 0.79 of 66 | — | structure | — | BELOW FLOOR |
| 9 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-8.paddingR` | `div.col-12.col-md-8` | 6 | 1 | 0.09 of 66 | — | structure | yes | BELOW FLOOR |
| 10 | module-menu | MISSING | `div.col-12.col-md-8.paddingR` | `p` | `—` | 3 | 1 | 0.09 of 66 | — | 1.00 | yes | BELOW FLOOR |
| 11 | module-menu | MISSING | `div.col-12.col-md-8` | `ul` | `—` | 3 | 1 | 0.30 of 66 | — | 0.83 | — | BELOW FLOOR |
| 12 | module-menu | MOVED | `ul` | `li` | `li` | 2 | 1 | 0.09 of 66 | — | structure | — | BELOW FLOOR |
| 13 | module-menu | EXTRA | `p>b` | `—` | `b` | 1 | 1 | 0.98 of 66 | — | structure | — | BELOW FLOOR |
| 14 | module-menu | EXTRA | `li` | `—` | `ul` | 1 | 1 | 1.00 of 66 | — | structure | — | BELOW FLOOR |
| 15 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `ul` | 1 | 1 | 0.70 of 66 | — | structure | — | BELOW FLOOR |
| 16 | module-menu | MISSING | `p` | `br` | `—` | 1 | 1 | 0.01 of 66 | — | structure | — | BELOW FLOOR |
| 17 | module-menu | MISSING | `div.col-12.col-md-12.paddingR` | `h5` | `—` | 1 | 1 | 0.44 of 66 | — | 1.00 | yes | BELOW FLOOR |
| 18 | module-menu | MISSING | `div.col-12.col-md-12.paddingR` | `ul` | `—` | 1 | 1 | 0.44 of 66 | — | 1.00 | yes | BELOW FLOOR |
| 19 | module-menu | MISSING | `li>span.infoTrigger` | `span.infoTrigger` | `—` | 1 | 1 | 0.04 of 66 | — | 0.00 | — | BELOW FLOOR |
| 20 | module-menu | MISSING | `div.col-12.col-md-8.paddingR` | `p>b` | `—` | 1 | 1 | 0.01 of 66 | — | 1.00 | yes | BELOW FLOOR |
| 21 | module-menu | MISSING | `ul` | `li` | `—` | 1 | 1 | 0.20 of 66 | — | 1.00 | — | BELOW FLOOR |
| 22 | module-menu | MISSING | `div.col-12.col-md-8` | `h5` | `—` | 1 | 1 | 0.09 of 66 | — | 0.50 | — | BELOW FLOOR |
| 23 | module-menu | MOVED | `ul` | `li` | `li` | 1 | 1 | 0.82 of 66 | — | structure | — | BELOW FLOOR |
| 24 | module-menu | MOVED | `div.col-12.col-md-12.paddingR` | `p` | `p` | 1 | 1 | 0.44 of 66 | — | structure | yes | BELOW FLOOR |
| 25 | module-menu | MOVED | `div.col-12.col-md-8.paddingR` | `p` | `p` | 1 | 1 | 0.09 of 66 | — | structure | yes | BELOW FLOOR |
| 26 | module-menu | SUBSTITUTED | `li` | `ol` | `b` | 1 | 1 | 0.01 of 66 | — | structure | — | BELOW FLOOR |
| 27 | footer | EXTRA | `li>a#next-lesson` | `—` | `a#next-lesson` | 37 | 8 | 0.70 of 66 | — | structure | yes | BELOW FLOOR |
| 28 | footer | EXTRA | `ul.footer-nav` | `—` | `li>a.home-nav` | 37 | 8 | 0.03 of 66 | — | structure | yes | BELOW FLOOR |
| 29 | footer | MISSING | `ul.footer-nav` | `li>a#next-lesson` | `—` | 3 | 3 | 0.30 of 66 | — | structure | yes | BELOW FLOOR |
| 30 | footer | EXTRA | `div#footer` | `—` | `ul.footer-nav` | 2 | 2 | 0.03 of 66 | — | structure | yes | BELOW FLOOR |
| 31 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav.inquiry-nav` | `ul.footer-nav` | 2 | 1 | 0.03 of 66 | — | structure | yes | BELOW FLOOR |
| 32 | footer | EXTRA | `ul.footer-nav` | `—` | `li>a#next-lesson` | 1 | 1 | 0.70 of 66 | — | structure | yes | BELOW FLOOR |
| 33 | footer | MISSING | `body.container-fluid` | `div#footer` | `—` | 1 | 1 | 0.92 of 66 | — | structure | yes | BELOW FLOOR |
| 34 | footer | MISSING | `div#body` | `div#footer` | `—` | 1 | 1 | 0.01 of 66 | — | structure | yes | BELOW FLOOR |
| 35 | acks | SUBSTITUTED | `div.col-12.col-md-8` | `div.acks` | `div.acks.acksTemplate` | 2 | 2 | 0.09 of 66 | — | structure | yes | BELOW FLOOR |
| 36 | acks | SUBSTITUTED | `div.col-12.col-md-8` | `div.acks.acksAI.acksTemplate` | `div.acks.acksTemplate` | 2 | 2 | 0.04 of 66 | — | structure | yes | BELOW FLOOR |
| 37 | activity | EXTRA | `a` | `—` | `div.button` | 14 | 7 | 0.95 of 66 | — | structure | yes | BELOW FLOOR |
| 38 | activity | EXTRA | `div.col-12` | `—` | `p` | 13 | 7 | 1.00 of 66 | — | structure | — | BELOW FLOOR |
| 39 | activity | MISSING | `div.col-12.col-md-8` | `div.activity.dropbox[number=*]` | `—` | 21 | 6 | 0.64 of 66 | template=flat c=0.64 n=21 | 1.00 | yes | CANDIDATE |
| 40 | activity | MISSING | `div.activity.clickDropContent.dropbox[nu` | `p` | `—` | 18 | 6 | 0.17 of 66 | — | 1.00 | yes | BELOW FLOOR |
| 41 | activity | EXTRA | `div.col-12` | `—` | `WIDGET` | 12 | 6 | 0.98 of 66 | — | structure | — | BELOW FLOOR |
| 42 | activity | EXTRA | `div.row` | `—` | `div.col-12` | 10 | 6 | 0.98 of 66 | — | structure | — | BELOW FLOOR |
| 43 | activity | MOVED | `div.activity.clickDropContent.dropbox[nu` | `p` | `p` | 12 | 5 | 0.12 of 66 | — | structure | yes | BELOW FLOOR |
| 44 | activity | MOVED | `div.activity.dropbox[number=*]` | `p` | `p` | 10 | 5 | 0.09 of 66 | — | structure | yes | BELOW FLOOR |
| 45 | activity | EXTRA | `div.activity[number=*]` | `—` | `div.row` | 8 | 5 | 1.00 of 66 | — | structure | yes | BELOW FLOOR |
| 46 | activity | EXTRA | `p>b` | `—` | `b` | 6 | 5 | 0.91 of 66 | — | structure | — | BELOW FLOOR |
| 47 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.clickDropContent.dropbox[number=*]` | `div.activity[number=*]` | 6 | 5 | 0.48 of 66 | — | structure | yes | BELOW FLOOR |
| 48 | activity | MISSING | `a` | `div.buttonD` | `—` | 24 | 4 | 0.42 of 66 | — | 0.71 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 49 | activity | EXTRA | `div.activity.clickDropContent.dropbox[nu` | `—` | `a` | 23 | 4 | 0.95 of 66 | template=flat c=0.95 n=23 | structure | yes | CANDIDATE |
| 50 | activity | EXTRA | `div.activity.dropbox[number=*]` | `—` | `a` | 21 | 4 | 0.83 of 66 | template=flat c=0.83 n=21 | structure | yes | CANDIDATE |
| 51 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.dropbox[number=*]` | `div.activity[number=*]` | 12 | 4 | 0.67 of 66 | — | structure | yes | BELOW FLOOR |
| 52 | activity | MISSING | `div.activity.dropbox[number=*]` | `p` | `—` | 10 | 4 | 0.08 of 66 | — | 0.92 | yes | BELOW FLOOR |
| 53 | activity | MISSING | `div.col-12` | `p` | `—` | 10 | 4 | 0.09 of 66 | — | 1.00 | — | BELOW FLOOR |
| 54 | activity | MISSING | `div.activity.dropbox[number=*]` | `div.ratio.ratio-16x9.videoSection` | `—` | 7 | 4 | 0.08 of 66 | — | structure | yes | BELOW FLOOR |
| 55 | activity | MISSING | `div.col-12` | `a` | `—` | 6 | 4 | 0.12 of 66 | — | 0.88 | — | BELOW FLOOR |
| 56 | activity | MOVED | `ul` | `li` | `li` | 5 | 4 | 0.11 of 66 | — | structure | — | BELOW FLOOR |
| 57 | activity | SUBSTITUTED | `div.activity.clickDropContent.dropbox[nu` | `h3` | `div.row` | 5 | 4 | 0.48 of 66 | — | structure | yes | BELOW FLOOR |
| 58 | activity | EXTRA | `div.activity.clickDropContent.dropbox[nu` | `—` | `p` | 11 | 3 | 0.65 of 66 | — | structure | yes | BELOW FLOOR |
| 59 | activity | MISSING | `a` | `div.button.buttonD.iconCentral` | `—` | 10 | 3 | 0.20 of 66 | — | 0.91 | yes | BELOW FLOOR |
| 60 | activity | MISSING | `div.activity.clickDropContent.dropbox[nu` | `h3` | `—` | 5 | 3 | 0.46 of 66 | — | 0.80 | yes | BELOW FLOOR |
| 61 | activity | MISSING | `a` | `div.button` | `—` | 5 | 3 | 0.04 of 66 | — | 0.08 | yes | BELOW FLOOR |
| 62 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.clickDropContent.dropbox[number=*]` | `div.activity.clickDropContent[number=*]` | 5 | 3 | 0.48 of 66 | — | structure | yes | BELOW FLOOR |
| 63 | activity | EXTRA | `div.col-12.col-md-8` | `—` | `div.activity[number=*]` | 4 | 3 | 1.00 of 66 | — | structure | yes | BELOW FLOOR |
| 64 | activity | MISSING | `div.activity.dropbox[number=*]` | `WIDGET` | `—` | 4 | 3 | 0.04 of 66 | — | structure | yes | BELOW FLOOR |
| 65 | activity | MISSING | `div.activity.clickDropContent.dropbox[nu` | `div.ratio.ratio-16x9.videoSection` | `—` | 4 | 3 | 0.06 of 66 | — | structure | yes | BELOW FLOOR |
| 66 | activity | MOVED | `div.col-12` | `p` | `p` | 4 | 3 | 0.09 of 66 | — | structure | — | BELOW FLOOR |
| 67 | activity | MOVED | `div.activity.clickDropContent.dropbox[nu` | `p` | `p` | 4 | 3 | 0.12 of 66 | — | structure | yes | BELOW FLOOR |
| 68 | activity | EXTRA | `div.col-12` | `—` | `img.img-fluid` | 3 | 3 | 0.98 of 66 | — | structure | — | BELOW FLOOR |
| 69 | activity | MISSING | `div.ratio.ratio-16x9.videoSection` | `iframe` | `—` | 3 | 3 | 0.30 of 66 | — | structure | yes | BELOW FLOOR |
| 70 | activity | MOVED | `div.activity.dropbox[number=*]` | `p` | `p` | 3 | 3 | 0.27 of 66 | — | structure | yes | BELOW FLOOR |
| 71 | activity | SUBSTITUTED | `div.activity.clickDropContent.dropbox[nu` | `p` | `p` | 3 | 3 | 0.48 of 66 | — | structure | yes | BELOW FLOOR |
| 72 | activity | MISSING | `a` | `div.button.iconCentral` | `—` | 7 | 2 | 0.06 of 66 | — | 0.65 | yes | BELOW FLOOR |
| 73 | activity | MISSING | `a` | `div.button.externalButton` | `—` | 7 | 2 | 0.12 of 66 | — | 0.92 | yes | BELOW FLOOR |
| 74 | activity | EXTRA | `p>span.infoTrigger` | `—` | `span.infoTrigger` | 5 | 2 | 0.97 of 66 | — | structure | — | BELOW FLOOR |
| 75 | activity | MISSING | `div.row` | `div.col-12` | `—` | 5 | 2 | 0.77 of 66 | — | 0.20 | — | BELOW FLOOR |
| 76 | activity | MISSING | `div.col-12` | `h3` | `—` | 5 | 2 | 0.08 of 66 | — | 0.88 | — | BELOW FLOOR |
| 77 | activity | MISSING | `div.activity.dropbox[number=*]` | `h3` | `—` | 4 | 2 | 0.09 of 66 | — | 0.60 | yes | BELOW FLOOR |
| 78 | activity | MOVED | `ul` | `li` | `li` | 4 | 2 | 0.03 of 66 | — | structure | — | BELOW FLOOR |
| 79 | activity | SUBSTITUTED | `div.col-12` | `p` | `p` | 4 | 2 | 0.74 of 66 | — | structure | — | BELOW FLOOR |
| 80 | activity | SUBSTITUTED | `a` | `div.button.buttonD.iconCentral` | `div.button` | 4 | 2 | 0.20 of 66 | — | structure | yes | BELOW FLOOR |
| 81 | activity | EXTRA | `a` | `—` | `div.externalButton` | 3 | 2 | 1.00 of 66 | — | structure | — | BELOW FLOOR |
| 82 | activity | EXTRA | `div.col-12` | `—` | `h3` | 3 | 2 | 0.92 of 66 | — | structure | — | BELOW FLOOR |
| 83 | activity | MISSING | `div.activity.dropbox[number=*]` | `br` | `—` | 3 | 2 | 0.03 of 66 | — | structure | yes | BELOW FLOOR |
| 84 | activity | MISSING | `div.activity.dropbox[number=*]` | `ul` | `—` | 3 | 2 | 0.03 of 66 | — | 1.00 | yes | BELOW FLOOR |
| 85 | activity | MISSING | `div.col-12` | `WIDGET` | `—` | 3 | 2 | 0.06 of 66 | — | structure | — | BELOW FLOOR |
| 86 | activity | EXTRA | `div.col-12` | `—` | `p>i` | 2 | 2 | 1.00 of 66 | — | structure | — | BELOW FLOOR |
| 87 | activity | EXTRA | `div.col-12` | `—` | `p>a` | 2 | 2 | 1.00 of 66 | — | structure | — | BELOW FLOOR |
| 88 | activity | EXTRA | `div.col-12` | `—` | `ul` | 2 | 2 | 0.94 of 66 | — | structure | — | BELOW FLOOR |
| 89 | activity | EXTRA | `div.col-12` | `—` | `ol` | 2 | 2 | 1.00 of 66 | — | structure | — | BELOW FLOOR |
| 90 | activity | EXTRA | `div.col-12` | `—` | `div.ratio.ratio-16x9.videoSection` | 2 | 2 | 1.00 of 66 | — | structure | yes | BELOW FLOOR |
| 91 | activity | EXTRA | `div.activity.clickDropContent.dropbox[nu` | `—` | `div.ratio.ratio-16x9.videoSection` | 2 | 2 | 0.94 of 66 | — | structure | yes | BELOW FLOOR |
| 92 | activity | EXTRA | `div.activity.dropbox[number=*]` | `—` | `h5` | 2 | 2 | 1.00 of 66 | — | structure | yes | BELOW FLOOR |
| 93 | activity | EXTRA | `div.activity.dropbox[number=*]` | `—` | `p` | 2 | 2 | 0.89 of 66 | — | structure | yes | BELOW FLOOR |
| 94 | activity | MISSING | `div.activity.dropbox[number=*]` | `div.icon.ratio.ratio-16x9.videoSection` | `—` | 2 | 2 | 0.11 of 66 | — | structure | yes | BELOW FLOOR |
| 95 | activity | MISSING | `div.col-12` | `h4` | `—` | 2 | 2 | 0.03 of 66 | — | 1.00 | — | BELOW FLOOR |
| 96 | activity | MISSING | `div.col-12` | `br` | `—` | 2 | 2 | 0.01 of 66 | — | structure | — | BELOW FLOOR |
| 97 | activity | MISSING | `div.activity.clickDropContent.dropbox[nu` | `img.img-fluid` | `—` | 2 | 2 | 0.01 of 66 | — | structure | yes | BELOW FLOOR |
| 98 | activity | MISSING | `p>b` | `b` | `—` | 2 | 2 | 0.09 of 66 | — | 1.00 | — | BELOW FLOOR |
| 99 | activity | MISSING | `p>span.infoTrigger` | `span.infoTrigger` | `—` | 2 | 2 | 0.12 of 66 | — | 1.00 | — | BELOW FLOOR |
| 100 | activity | MISSING | `div.col-12.col-md-8` | `div.activity.clickDropContent.dropbox[number=*]` | `—` | 2 | 2 | 0.46 of 66 | — | 0.75 | yes | BELOW FLOOR |
| 333 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 43 | 10 | 0.77 of 66 | template=flat c=0.77 n=43 | structure | — | CANDIDATE |
| 338 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.ratio.ratio-16x9.videoSection` | 23 | 6 | 0.86 of 66 | template=flat c=0.86 n=23 | structure | yes | CANDIDATE |

## Details — in the companion file `CONVERTER_V2/outputs/_diff_queue_details.md`
Every CANDIDATE and every top-40 row has three quoted examples (WT / gold / Claude) there, plus the
below-floor list. **NEVER read the companion whole** (hundreds of KB): `grep -n '^### #<rank> ' CONVERTER_V2/outputs/_diff_queue_details.md` then `sed -n '<start>,<start+40>p'`. The top 25
candidates' detail blocks are repeated below for convenience.

### #39 · activity · MISSING · `div.col-12.col-md-8` › gold `div.activity.dropbox[number=*]` vs Claude `—` — CANDIDATE
- pages 21 / modules 6 / lines 21; consensus (all) 0.64 of 66 gold pages with the region; derivable 1.00 (0 lines with no WT source)
- by template: flat 6m/21p c=0.64
- by subject: None 6m/21p c=0.64
- by era: Refresh 6m/21p c=0.64
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:46 — | Activity class | `content activity activity-bg` | `activity` |
  - KB: 06_TEMPLATE_RECOGNITION.md:181 — - TWHA902–904 use `choicePage` activity grids and dual titles + `whakatauki` — these are content patterns, safe to use if the new module needs them
  - KB: 06_TEMPLATE_RECOGNITION.md:265 — **The X-prefix test governs THIS CLASS ONLY.** The wider LS look-and-feel conventions of `14_SUBJECT_GLOBAL_PARAMETERS.md` § 14.6 — terminology and br
- **XDLS903/** XDLS903_2_0.html ↔ XDLS903.02.html (content, derivable=True)
  - gold: `div.activity.dropbox[number=2G]  «Share your learning!»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [body] [/RED TEXT]🔴 Share your learning with your kaiako.`
- **XDLS904/** XDLS904_1_0.html ↔ XDLS904_01.0.html (content, derivable=True)
  - gold: `div.activity.dropbox[number=1G]  «Share your learning!»`
  - Claude: `—`
  - WT: `Share your learning with your kaiako.`
- **XDLS905/** XDLS905_1_0.html ↔ XDLS905.01.html (content, derivable=True)
  - gold: `div.activity.dropbox[number=1G]  «Share your learning!»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [body] [/RED TEXT]🔴 Share your learning with your kaiako.`
- modules: XDLS903/, XDLS904/, XDLS905/, XDLS906/, XDLS908/, XDLS912/

### #49 · activity · EXTRA · `div.activity.clickDropContent.dropbox[number=*]` › gold `—` vs Claude `a` — CANDIDATE
- pages 23 / modules 4 / lines 88; consensus (all) 0.95 of 66 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: flat 4m/23p c=0.95
- by subject: None 4m/23p c=0.95
- by era: Refresh 4m/23p c=0.95
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:46 — | Activity class | `content activity activity-bg` | `activity` |
  - KB: 06_TEMPLATE_RECOGNITION.md:181 — - TWHA902–904 use `choicePage` activity grids and dual titles + `whakatauki` — these are content patterns, safe to use if the new module needs them
  - KB: 06_TEMPLATE_RECOGNITION.md:265 — **The X-prefix test governs THIS CLASS ONLY.** The wider LS look-and-feel conventions of `14_SUBJECT_GLOBAL_PARAMETERS.md` § 14.6 — terminology and br
- **XDLS903/** XDLS903_2_0.html ↔ XDLS903.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `a  «Upload to dropbox»`
- **XDLS904/** XDLS904_1_0.html ↔ XDLS904_01.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `a  «Upload to dropbox»`
- **XDLS905/** XDLS905_1_0.html ↔ XDLS905.01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `a  «Upload to dropbox»`
- modules: XDLS903/, XDLS904/, XDLS905/, XDLS906/

### #50 · activity · EXTRA · `div.activity.dropbox[number=*]` › gold `—` vs Claude `a` — CANDIDATE
- pages 21 / modules 4 / lines 21; consensus (all) 0.83 of 66 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: flat 4m/21p c=0.83
- by subject: None 4m/21p c=0.83
- by era: Refresh 4m/21p c=0.83
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:46 — | Activity class | `content activity activity-bg` | `activity` |
  - KB: 06_TEMPLATE_RECOGNITION.md:181 — - TWHA902–904 use `choicePage` activity grids and dual titles + `whakatauki` — these are content patterns, safe to use if the new module needs them
  - KB: 06_TEMPLATE_RECOGNITION.md:265 — **The X-prefix test governs THIS CLASS ONLY.** The wider LS look-and-feel conventions of `14_SUBJECT_GLOBAL_PARAMETERS.md` § 14.6 — terminology and br
- **XDLS903/** XDLS903_2_0.html ↔ XDLS903.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `a  «Upload to dropbox»`
- **XDLS904/** XDLS904_1_0.html ↔ XDLS904_01.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `a  «Upload to dropbox»`
- **XDLS905/** XDLS905_1_0.html ↔ XDLS905.01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `a  «Upload to dropbox»`
- modules: XDLS903/, XDLS904/, XDLS905/, XDLS906/

### #333 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `p` — CANDIDATE
- pages 43 / modules 10 / lines 118; consensus (all) 0.77 of 66 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: flat 10m/43p c=0.77
- by subject: None 10m/43p c=0.77
- by era: Refresh 10m/43p c=0.77
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **XDLS901/** XDLS901_0_0.html ↔ XDLS901.00.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «By doing this, we can grow, learn new things, and enjoy special moments with the people we love.»`
- **XDLS902/** XDLS902_3_0.html ↔ XDLS902.03.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «(my/his/her own time and space) / autistic and have your own time and space you prefer to sleep. Maybe you just struggle»`
- **XDLS903/** XDLS903_1_0.html ↔ XDLS903.01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Below there are three tabs. Can you see them? One says introduction, the next safety and lastly, you will see the word r»`
- modules: XDLS901/, XDLS902/, XDLS903/, XDLS904/, XDLS905/, XDLS906/, XDLS908/, XDLS909/, XDLS911/, XDLS912/

### #338 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `div.ratio.ratio-16x9.videoSection` — CANDIDATE
- pages 23 / modules 6 / lines 34; consensus (all) 0.86 of 66 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: flat 6m/23p c=0.86
- by subject: None 6m/23p c=0.86
- by era: Refresh 6m/23p c=0.86
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:43 — | Video wrapper | `embed-responsive embed-responsive-16by9` | `ratio ratio-16x9` |
  - KB: 06_TEMPLATE_RECOGNITION.md:376 — <div class="videoSection ratio ratio-16x9">
  - KB: 01_PIPELINE_EXTRACTION_TAGS/01E_TAG_INTERPRETATION.md:59 — <div class="videoSection ratio ratio-16x9">
- **XDLS901/** XDLS901_3_0.html ↔ XDLS901.03.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.ratio.ratio-16x9.videoSection`
- **XDLS903/** XDLS903_1_0.html ↔ XDLS903.01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.ratio.ratio-16x9.videoSection`
- **XDLS904/** XDLS904_1_0.html ↔ XDLS904_01.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.ratio.ratio-16x9.videoSection`
- modules: XDLS901/, XDLS903/, XDLS904/, XDLS905/, XDLS906/, XDLS908/
