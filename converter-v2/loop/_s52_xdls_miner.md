# DIFF_QUEUE.md — the diff miner's ranked class queue (LOOP__Autonomous_Rounds.md §1d)

**Produced:** 2026-09-26 16:58 NZST by `reference/tests/_diff_miner.py` on the CURRENT corpus (pageforge-site HEAD 3e4beab; Claude corpus 545 dirs). **Population:** the skeleton gate's own — 75 paired pages / 12 modules (compare_exclusions.txt honoured; acks / glossary / references pages excluded); parse errors skipped: 0 (must be 0); modules without a parsed WT: 0. Run time 5.0 s.

**What a row is.** One CLASS = (region, parent element, gold form, Claude form, direction) over every differing skeleton line of every paired page — the same lines, labels, widget collapse and difflib alignment the PRIMARY gate scores (each element its own line so it can be quoted). Direction: MISSING = gold has it, Claude lacks it; EXTRA = Claude has it, gold lacks it; SUBSTITUTED = same position, different tag / class / wrapper; MOVED = same text, different place. Consensus = of the gold pages in the group where the region exists, the share carrying the gold form (for EXTRA: the share NOT carrying Claude's form). Derivable = the gold line's text is in the module's parsed Writers Template (round-110 tolerance); structure-only differences are always derivable.

**Candidate rule (§1d).** modules ≥ 10 for a chrome class (module-code / title / header / module-menu / crumbs / phases-nav / footer / acks), pages ≥ 20 for a body / activity class; gold consensus ≥ 0.60 in at least one template or subject group that itself reaches the floor; structure-only or derivable share ≥ 0.60. A class below the floor is listed, never dropped. A CANDIDATE still goes through the PICK's KB-first check, the triangulation and the §3 corpus-wide measurement before any code — this table is the queue, not the verdict.

## Summary

- differing skeleton lines: 8066 — by direction {'SUBSTITUTED': 652, 'MOVED': 236, 'EXTRA': 3055, 'MISSING': 4123}
- by region: {'title': 13, 'module-menu': 178, 'footer': 122, 'acks': 36, 'activity': 3087, 'body': 4598, 'root': 32}
- classes: 710 — CANDIDATE 7, below floor 700, the rest below consensus / not derivable

## Completeness census — the repeating chrome (§1d item 4)

| region | pages with region | gold items | gold items in WT | Claude items | derivable misses | pages with misses | modules with misses | status |
|---|---|---|---|---|---|---|---|---|
| module-menu | 62 | 406 | 365 | 314 | 69 | 25 | 6 | BELOW FLOOR |
| crumbs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |
| phases-nav | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |
| footer | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |

- **module-menu** by template: Inquiry 2m/6p/25 misses; Standard 4m/19p/44 misses
  - XDLS909 XDLS909_1_0.html: gold 9 items (8 in WT) / Claude 0 — 8 derivable misses, e.g. li «to understand what the Aotearoa New Zealand Census is and how it helps us learn » · li «what a census is and how it is used to gather information about the diversity of»
  - XDLS502 XDLS502_3_0.html: gold 7 items (7 in WT) / Claude 0 — 7 derivable misses, e.g. h5 «We are learning to:» · li «to identify what facilities and services are»
  - XDLS501 XDLS501_2_0.html: gold 10 items (6 in WT) / Claude 0 — 6 derivable misses, e.g. li «to be mindful of the way you live your life» · li «how to mindfully listen to others»
  - XDLS909 XDLS909_3_0.html: gold 8 items (6 in WT) / Claude 0 — 6 derivable misses, e.g. li «what are the rights and responsibilities of a resident and citizen of Aotearoa N» · li «ways that we can have our say in Aotearoa New Zealand as residents and citizens.»
- **crumbs** by template: 
- **phases-nav** by template: 
- **footer** by template: 

## Chrome facts — the header and footer as SETS per page (alignment-free; §1d items 2 + 4)

A fact is one thing a page's chrome has: `header:chip` (the `#module-code` div), `header:chip=module-code` / `=lesson-number` / `=lesson-number(00)`, `header:head-buttons`, `header:menu-content`, `header:title-h1-count=N`, `footer:present`, `footer:ul=<classes>`, `footer:link=prev-lesson` / `next-lesson` / `home-nav`, `footer:links=<order>`, `footer:inside-body`, `nav:crumbs`, `nav:phases`. MISSING = the gold page has the fact and Claude's does not; EXTRA the reverse. Consensus = the share of gold pages in the group that have (MISSING) / lack (EXTRA) the fact. Floor 10 modules.

| # | dir | fact | pages | modules | gold share (all) | consensus (all) | best group | status |
|---|---|---|---|---|---|---|---|---|
| F1 | EXTRA | `header:chip=decimal-number` | 37 | 7 | 0.27 | 0.73 | — | BELOW FLOOR |
| F2 | MISSING | `header:chip=lesson-number` | 36 | 6 | 0.56 | 0.56 | — | BELOW FLOOR |
| F3 | MISSING | `header:chip=other` | 5 | 5 | 0.07 | 0.07 | — | BELOW FLOOR |
| F4 | EXTRA | `header:chip=module-code` | 4 | 4 | 0.11 | 0.89 | — | BELOW FLOOR |
| F5 | MISSING | `header:title-h1-count=2` | 11 | 3 | 0.25 | 0.25 | — | BELOW FLOOR |
| F6 | EXTRA | `header:title-h1-count=1` | 11 | 3 | 0.75 | 0.25 | — | BELOW FLOOR |
| F7 | MISSING | `header:title-h1-count=1` | 2 | 2 | 0.75 | 0.75 | — | BELOW FLOOR |
| F8 | EXTRA | `header:title-h1-count=2` | 2 | 2 | 0.25 | 0.75 | — | BELOW FLOOR |
| F9 | EXTRA | `footer:links=next-lesson,home-nav` | 11 | 11 | 0.01 | 0.99 | era=Refresh c=0.99 n=11 | CANDIDATE |
| F10 | EXTRA | `footer:link=next-lesson` | 37 | 7 | 0.37 | 0.63 | — | BELOW FLOOR |
| F11 | MISSING | `footer:links=prev-lesson,home-nav` | 31 | 6 | 0.55 | 0.55 | — | BELOW FLOOR |
| F12 | EXTRA | `footer:links=prev-lesson,next-lesson,home-nav` | 31 | 6 | 0.29 | 0.71 | — | BELOW FLOOR |
| F13 | MISSING | `footer:links=home-nav` | 6 | 6 | 0.08 | 0.08 | — | BELOW FLOOR |
| F14 | MISSING | `footer:links=home-nav,next-lesson` | 5 | 5 | 0.07 | 0.07 | — | BELOW FLOOR |
| F15 | MISSING | `footer:inside-body` | 3 | 3 | 0.04 | 0.04 | — | BELOW FLOOR |
| F16 | MISSING | `footer:ul=footer-nav inquiry-nav` | 2 | 1 | 0.03 | 0.03 | — | BELOW FLOOR |
| F17 | EXTRA | `footer:ul=footer-nav` | 2 | 1 | 0.97 | 0.03 | — | BELOW FLOOR |
| F18 | MISSING | `footer:link=next-lesson` | 1 | 1 | 0.37 | 0.37 | — | BELOW FLOOR |
| F19 | MISSING | `footer:links=prev-lesson,next-lesson,home-nav` | 1 | 1 | 0.29 | 0.29 | — | BELOW FLOOR |
| F20 | EXTRA | `footer:links=prev-lesson,home-nav` | 1 | 1 | 0.55 | 0.45 | — | BELOW FLOOR |

### F9 · EXTRA `footer:links=next-lesson,home-nav` — CANDIDATE (pages 11 / modules 11)
- by template+ptype: Standard/overview 8m/8p gold 0.11 Claude 1.00 c=0.89; Inquiry/overview 3m/3p gold 0.00 Claude 1.00 c=1.00
- by subject: Leaving to Learn 11m/11p gold 0.01 Claude 0.16 c=0.99
- **XDLS501** XDLS501_0_0.html ↔ XDLS501.00.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **XDLS502** XDLS502_0_0.html ↔ XDLS502.00.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **XDLS901** XDLS901_0_0.html ↔ XDLS901.00.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: XDLS501, XDLS502, XDLS901, XDLS902, XDLS903, XDLS904, XDLS905, XDLS906, XDLS908, XDLS909, XDLS911


## The ranked queue — chrome regions first, then by modules affected

| # | region | dir | parent | gold form | Claude form | pages | modules | consensus (all) | best group | derivable | KB | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | title | MISSING | `div#header` | `h1>span` | `—` | 11 | 3 | 0.25 of 75 | — | 0.82 | yes | BELOW FLOOR |
| 2 | title | EXTRA | `div#header` | `—` | `h1>span` | 2 | 2 | 0.75 of 75 | — | structure | yes | BELOW FLOOR |
| 3 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-12.paddingR` | `div.col-12.col-md-8` | 29 | 5 | 0.39 of 75 | — | structure | yes | BELOW FLOOR |
| 4 | module-menu | MISSING | `div.col-12.col-md-8` | `p` | `—` | 6 | 4 | 0.21 of 75 | — | 0.70 | — | BELOW FLOOR |
| 5 | module-menu | MISSING | `div.col-12.col-md-12.paddingR` | `p` | `—` | 9 | 3 | 0.39 of 75 | — | 1.00 | yes | BELOW FLOOR |
| 6 | module-menu | MISSING | `div.col-12.col-md-8` | `ul` | `—` | 8 | 3 | 0.33 of 75 | — | 0.69 | — | BELOW FLOOR |
| 7 | module-menu | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `h5` | 12 | 2 | 0.21 of 75 | — | structure | — | BELOW FLOOR |
| 8 | module-menu | MISSING | `div.col-12.col-md-8` | `h5` | `—` | 5 | 2 | 0.13 of 75 | — | 0.80 | — | BELOW FLOOR |
| 9 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `h5` | 3 | 2 | 0.87 of 75 | — | structure | — | BELOW FLOOR |
| 10 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 2 | 2 | 0.79 of 75 | — | structure | — | BELOW FLOOR |
| 11 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-8.paddingR` | `div.col-12.col-md-8` | 6 | 1 | 0.08 of 75 | — | structure | yes | BELOW FLOOR |
| 12 | module-menu | MISSING | `div.col-12.col-md-8` | `p>b` | `—` | 3 | 1 | 0.04 of 75 | — | 0.00 | — | BELOW FLOOR |
| 13 | module-menu | MISSING | `div.col-12.col-md-8.paddingR` | `p` | `—` | 3 | 1 | 0.08 of 75 | — | 1.00 | yes | BELOW FLOOR |
| 14 | module-menu | MOVED | `ul` | `li` | `li` | 2 | 1 | 0.08 of 75 | — | structure | — | BELOW FLOOR |
| 15 | module-menu | EXTRA | `p>b` | `—` | `b` | 1 | 1 | 0.95 of 75 | — | structure | — | BELOW FLOOR |
| 16 | module-menu | EXTRA | `li` | `—` | `ul` | 1 | 1 | 1.00 of 75 | — | structure | — | BELOW FLOOR |
| 17 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `ul` | 1 | 1 | 0.67 of 75 | — | structure | — | BELOW FLOOR |
| 18 | module-menu | MISSING | `p` | `br` | `—` | 1 | 1 | 0.01 of 75 | — | structure | — | BELOW FLOOR |
| 19 | module-menu | MISSING | `div.col-12.col-md-12.paddingR` | `h5` | `—` | 1 | 1 | 0.39 of 75 | — | 1.00 | yes | BELOW FLOOR |
| 20 | module-menu | MISSING | `div.col-12.col-md-12.paddingR` | `ul` | `—` | 1 | 1 | 0.39 of 75 | — | 1.00 | yes | BELOW FLOOR |
| 21 | module-menu | MISSING | `li>span.infoTrigger` | `span.infoTrigger` | `—` | 1 | 1 | 0.04 of 75 | — | 0.00 | — | BELOW FLOOR |
| 22 | module-menu | MISSING | `div.col-12.col-md-8.paddingR` | `p>b` | `—` | 1 | 1 | 0.01 of 75 | — | 1.00 | yes | BELOW FLOOR |
| 23 | module-menu | MISSING | `ul` | `li` | `—` | 1 | 1 | 0.20 of 75 | — | 1.00 | — | BELOW FLOOR |
| 24 | module-menu | MOVED | `ul` | `li` | `li` | 1 | 1 | 0.79 of 75 | — | structure | — | BELOW FLOOR |
| 25 | module-menu | MOVED | `div.col-12.col-md-12.paddingR` | `p` | `p` | 1 | 1 | 0.39 of 75 | — | structure | yes | BELOW FLOOR |
| 26 | module-menu | MOVED | `div.col-12.col-md-8.paddingR` | `p` | `p` | 1 | 1 | 0.08 of 75 | — | structure | yes | BELOW FLOOR |
| 27 | module-menu | SUBSTITUTED | `li` | `ol` | `b` | 1 | 1 | 0.01 of 75 | — | structure | — | BELOW FLOOR |
| 28 | footer | EXTRA | `li>a#next-lesson` | `—` | `a#next-lesson` | 38 | 9 | 0.63 of 75 | — | structure | yes | BELOW FLOOR |
| 29 | footer | EXTRA | `ul.footer-nav` | `—` | `li>a.home-nav` | 38 | 9 | 0.03 of 75 | — | structure | yes | BELOW FLOOR |
| 30 | footer | MISSING | `ul.footer-nav` | `li>a#next-lesson` | `—` | 4 | 4 | 0.37 of 75 | — | structure | yes | BELOW FLOOR |
| 31 | footer | EXTRA | `body.container-fluid` | `—` | `div#footer` | 2 | 2 | 0.11 of 75 | — | structure | yes | BELOW FLOOR |
| 32 | footer | EXTRA | `div#footer` | `—` | `ul.footer-nav` | 2 | 2 | 0.03 of 75 | — | structure | yes | BELOW FLOOR |
| 33 | footer | MISSING | `div#body` | `div#footer` | `—` | 2 | 2 | 0.04 of 75 | — | structure | yes | BELOW FLOOR |
| 34 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav.inquiry-nav` | `ul.footer-nav` | 2 | 1 | 0.03 of 75 | — | structure | yes | BELOW FLOOR |
| 35 | footer | EXTRA | `ul.footer-nav` | `—` | `li>a#next-lesson` | 1 | 1 | 0.63 of 75 | — | structure | yes | BELOW FLOOR |
| 36 | footer | MISSING | `body.container-fluid` | `div#footer` | `—` | 1 | 1 | 0.89 of 75 | — | structure | yes | BELOW FLOOR |
| 37 | footer | SUBSTITUTED | `div#body` | `div#footer` | `div#footer` | 1 | 1 | 0.04 of 75 | — | structure | yes | BELOW FLOOR |
| 38 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav` | `ul.footer-nav` | 1 | 1 | 0.97 of 75 | — | structure | yes | BELOW FLOOR |
| 39 | footer | SUBSTITUTED | `ul.footer-nav` | `li>a.home-nav` | `li>a#next-lesson` | 1 | 1 | 0.97 of 75 | — | structure | yes | BELOW FLOOR |
| 40 | footer | SUBSTITUTED | `ul.footer-nav` | `li>a#next-lesson` | `li>a.home-nav` | 1 | 1 | 0.37 of 75 | — | structure | yes | BELOW FLOOR |
| 41 | acks | SUBSTITUTED | `div.col-12.col-md-8` | `div.acks` | `div.acks.acksTemplate` | 2 | 2 | 0.11 of 75 | — | structure | yes | BELOW FLOOR |
| 42 | acks | SUBSTITUTED | `div.col-12.col-md-8` | `div.acks.acksAI.acksTemplate` | `div.acks.acksTemplate` | 2 | 2 | 0.04 of 75 | — | structure | yes | BELOW FLOOR |
| 43 | acks | MISSING | `div.acks` | `WIDGET` | `—` | 1 | 1 | 0.11 of 75 | — | structure | yes | BELOW FLOOR |
| 44 | acks | SUBSTITUTED | `div.col-12.col-md-8` | `div.acks` | `p` | 1 | 1 | 0.11 of 75 | — | structure | yes | BELOW FLOOR |
| 45 | activity | MISSING | `div.col-12.col-md-8` | `div.activity.dropbox[number=*]` | `—` | 23 | 6 | 0.60 of 75 | ptype=lesson c=0.71 n=23 | 1.00 | yes | CANDIDATE |
| 46 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.dropbox[number=*]` | `div.activity[number=*]` | 13 | 6 | 0.64 of 75 | — | structure | yes | BELOW FLOOR |
| 47 | activity | MISSING | `div.col-12` | `p` | `—` | 12 | 6 | 0.12 of 75 | — | 0.91 | — | BELOW FLOOR |
| 48 | activity | EXTRA | `a` | `—` | `div.button` | 10 | 6 | 0.96 of 75 | — | structure | yes | BELOW FLOOR |
| 49 | activity | MISSING | `div.activity.dropbox[number=*]` | `p` | `—` | 10 | 6 | 0.12 of 75 | — | 0.91 | yes | BELOW FLOOR |
| 50 | activity | MISSING | `div.activity.clickDropContent.dropbox[nu` | `p` | `—` | 15 | 5 | 0.16 of 75 | — | 1.00 | yes | BELOW FLOOR |
| 51 | activity | EXTRA | `div.col-12` | `—` | `WIDGET` | 11 | 5 | 0.97 of 75 | — | structure | — | BELOW FLOOR |
| 52 | activity | EXTRA | `div.col-12` | `—` | `p` | 10 | 5 | 0.97 of 75 | — | structure | — | BELOW FLOOR |
| 53 | activity | MOVED | `div.col-12` | `p` | `p` | 8 | 5 | 0.12 of 75 | — | structure | — | BELOW FLOOR |
| 54 | activity | EXTRA | `p>b` | `—` | `b` | 5 | 5 | 0.92 of 75 | — | structure | — | BELOW FLOOR |
| 55 | activity | EXTRA | `div.activity.clickDropContent.dropbox[nu` | `—` | `a` | 27 | 4 | 0.95 of 75 | template=Standard c=1.00 n=21 | structure | yes | CANDIDATE |
| 56 | activity | MISSING | `a` | `div.buttonD` | `—` | 26 | 4 | 0.37 of 75 | — | 0.73 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 57 | activity | EXTRA | `div.activity.dropbox[number=*]` | `—` | `a` | 24 | 4 | 0.83 of 75 | era=Refresh c=0.83 n=24 | structure | yes | CANDIDATE |
| 58 | activity | EXTRA | `p>span.infoTrigger` | `—` | `span.infoTrigger` | 19 | 4 | 0.97 of 75 | — | structure | — | BELOW FLOOR |
| 59 | activity | EXTRA | `div.activity.clickDropContent.dropbox[nu` | `—` | `p` | 11 | 4 | 0.60 of 75 | — | structure | yes | BELOW FLOOR |
| 60 | activity | MOVED | `div.activity.clickDropContent.dropbox[nu` | `p` | `p` | 10 | 4 | 0.12 of 75 | — | structure | yes | BELOW FLOOR |
| 61 | activity | MISSING | `div.activity.dropbox[number=*]` | `div.ratio.ratio-16x9.videoSection` | `—` | 8 | 4 | 0.07 of 75 | — | structure | yes | BELOW FLOOR |
| 62 | activity | EXTRA | `div.activity[number=*]` | `—` | `div.row` | 7 | 4 | 1.00 of 75 | — | structure | yes | BELOW FLOOR |
| 63 | activity | EXTRA | `div.row` | `—` | `div.col-12` | 7 | 4 | 0.95 of 75 | — | structure | — | BELOW FLOOR |
| 64 | activity | MISSING | `div.col-12` | `h3` | `—` | 7 | 4 | 0.11 of 75 | — | 0.80 | — | BELOW FLOOR |
| 65 | activity | MISSING | `div.col-12` | `WIDGET` | `—` | 6 | 4 | 0.09 of 75 | — | structure | — | BELOW FLOOR |
| 66 | activity | MISSING | `div.col-12` | `a` | `—` | 6 | 4 | 0.11 of 75 | — | 0.91 | — | BELOW FLOOR |
| 67 | activity | MISSING | `a` | `div.button.buttonD.iconCentral` | `—` | 10 | 3 | 0.17 of 75 | — | 0.91 | yes | BELOW FLOOR |
| 68 | activity | MOVED | `div.activity.dropbox[number=*]` | `p` | `p` | 8 | 3 | 0.08 of 75 | — | structure | yes | BELOW FLOOR |
| 69 | activity | EXTRA | `p>a` | `—` | `a` | 7 | 3 | 0.93 of 75 | — | structure | — | BELOW FLOOR |
| 70 | activity | MISSING | `a` | `div.button` | `—` | 6 | 3 | 0.04 of 75 | — | 0.12 | yes | BELOW FLOOR |
| 71 | activity | MISSING | `div.col-12` | `ul` | `—` | 5 | 3 | 0.04 of 75 | — | 0.78 | — | BELOW FLOOR |
| 72 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.clickDropContent.dropbox[number=*]` | `div.activity.clickDropContent[number=*]` | 5 | 3 | 0.44 of 75 | — | structure | yes | BELOW FLOOR |
| 73 | activity | EXTRA | `div.col-12.col-md-8` | `—` | `div.activity[number=*]` | 4 | 3 | 1.00 of 75 | — | structure | yes | BELOW FLOOR |
| 74 | activity | MISSING | `a` | `div.externalButton` | `—` | 4 | 3 | 0.04 of 75 | — | 0.17 | — | BELOW FLOOR |
| 75 | activity | MISSING | `div.activity.dropbox[number=*]` | `ul` | `—` | 4 | 3 | 0.03 of 75 | — | 1.00 | yes | BELOW FLOOR |
| 76 | activity | MISSING | `div.activity.dropbox[number=*]` | `WIDGET` | `—` | 4 | 3 | 0.04 of 75 | — | structure | yes | BELOW FLOOR |
| 77 | activity | MOVED | `a` | `div.button` | `div.button` | 4 | 3 | 0.11 of 75 | — | structure | yes | BELOW FLOOR |
| 78 | activity | MOVED | `ul` | `li` | `li` | 4 | 3 | 0.09 of 75 | — | structure | — | BELOW FLOOR |
| 79 | activity | EXTRA | `div.col-12` | `—` | `img.img-fluid` | 3 | 3 | 0.97 of 75 | — | structure | — | BELOW FLOOR |
| 80 | activity | EXTRA | `div.activity.clickDropContent.dropbox[nu` | `—` | `div.ratio.ratio-16x9.videoSection` | 3 | 3 | 0.83 of 75 | — | structure | yes | BELOW FLOOR |
| 81 | activity | MISSING | `div.activity.dropbox[number=*]` | `h3` | `—` | 3 | 3 | 0.11 of 75 | — | 0.33 | yes | BELOW FLOOR |
| 82 | activity | MISSING | `div.activity.clickDropContent.dropbox[nu` | `div.ratio.ratio-16x9.videoSection` | `—` | 3 | 3 | 0.05 of 75 | — | structure | yes | BELOW FLOOR |
| 83 | activity | MOVED | `div.activity.dropbox[number=*]` | `p` | `p` | 3 | 3 | 0.27 of 75 | — | structure | yes | BELOW FLOOR |
| 84 | activity | SUBSTITUTED | `div.activity.clickDropContent.dropbox[nu` | `h3` | `div.row` | 3 | 3 | 0.44 of 75 | — | structure | yes | BELOW FLOOR |
| 85 | activity | SUBSTITUTED | `div.activity.clickDropContent.dropbox[nu` | `p` | `p` | 3 | 3 | 0.44 of 75 | — | structure | yes | BELOW FLOOR |
| 86 | activity | MISSING | `a` | `div.button.iconCentral` | `—` | 7 | 2 | 0.05 of 75 | — | 0.65 | yes | BELOW FLOOR |
| 87 | activity | EXTRA | `div.activity.clickDropContent[number=*]` | `—` | `p` | 5 | 2 | 1.00 of 75 | — | structure | yes | BELOW FLOOR |
| 88 | activity | MISSING | `div.activity.dropbox[number=*]` | `img.img-fluid` | `—` | 5 | 2 | 0.11 of 75 | — | structure | yes | BELOW FLOOR |
| 89 | activity | MOVED | `ul` | `li` | `li` | 4 | 2 | 0.03 of 75 | — | structure | — | BELOW FLOOR |
| 90 | activity | SUBSTITUTED | `a` | `div.button.buttonD.iconCentral` | `div.button` | 4 | 2 | 0.17 of 75 | — | structure | yes | BELOW FLOOR |
| 91 | activity | EXTRA | `div.col-12` | `—` | `ul` | 3 | 2 | 0.89 of 75 | — | structure | — | BELOW FLOOR |
| 92 | activity | EXTRA | `a` | `—` | `div.externalButton` | 3 | 2 | 1.00 of 75 | — | structure | — | BELOW FLOOR |
| 93 | activity | EXTRA | `div.col-12` | `—` | `h3` | 3 | 2 | 0.89 of 75 | — | structure | — | BELOW FLOOR |
| 94 | activity | MISSING | `div.activity.dropbox[number=*]` | `br` | `—` | 3 | 2 | 0.03 of 75 | — | structure | yes | BELOW FLOOR |
| 95 | activity | MISSING | `div.activity.dropbox[number=*]` | `div.flipCardsContainer.row` | `—` | 3 | 2 | 0.04 of 75 | — | structure | yes | BELOW FLOOR |
| 96 | activity | MOVED | `div.activity.clickDropContent.dropbox[nu` | `p` | `p` | 3 | 2 | 0.16 of 75 | — | structure | yes | BELOW FLOOR |
| 97 | activity | SUBSTITUTED | `div.activity.clickDropContent.dropbox[nu` | `p` | `a` | 3 | 2 | 0.44 of 75 | — | structure | yes | BELOW FLOOR |
| 98 | activity | EXTRA | `div.col-12` | `—` | `p>i` | 2 | 2 | 1.00 of 75 | — | structure | — | BELOW FLOOR |
| 99 | activity | EXTRA | `div.col-12` | `—` | `p>a` | 2 | 2 | 1.00 of 75 | — | structure | — | BELOW FLOOR |
| 100 | activity | EXTRA | `div.col-12` | `—` | `ol` | 2 | 2 | 0.99 of 75 | — | structure | — | BELOW FLOOR |
| 349 | body | MISSING | `div#body` | `div.row` | `—` | 61 | 11 | 0.52 of 75 | template+ptype=Standard/lesson c=0.62 n=43 | 0.75 | — | CANDIDATE |
| 350 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 43 | 11 | 0.68 of 75 | series=XDLS90 c=0.81 n=38 | structure | — | CANDIDATE |
| 351 | body | EXTRA | `div.col-12.col-md-8` | `—` | `WIDGET` | 20 | 10 | 0.79 of 75 | era=Refresh c=0.79 n=20 | structure | — | CANDIDATE |
| 357 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.ratio.ratio-16x9.videoSection` | 23 | 6 | 0.88 of 75 | ptype=lesson c=0.91 n=21 | structure | yes | CANDIDATE |

## Details — in the companion file `CONVERTER_V2/outputs/_s52_xdls_miner_details.md`
Every CANDIDATE and every top-40 row has three quoted examples (WT / gold / Claude) there, plus the
below-floor list. **NEVER read the companion whole** (hundreds of KB): `grep -n '^### #<rank> ' CONVERTER_V2/outputs/_diff_queue_details.md` then `sed -n '<start>,<start+40>p'`. The top 25
candidates' detail blocks are repeated below for convenience.

### #45 · activity · MISSING · `div.col-12.col-md-8` › gold `div.activity.dropbox[number=*]` vs Claude `—` — CANDIDATE
- pages 23 / modules 6 / lines 23; consensus (all) 0.60 of 75 gold pages with the region; derivable 1.00 (0 lines with no WT source)
- by template: Standard 5m/17p c=0.65; Inquiry 1m/6p c=0.44
- by subject: Leaving to Learn 6m/23p c=0.60
- by era: Refresh 6m/23p c=0.60
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:46 — | Activity class | `content activity activity-bg` | `activity` |
  - KB: 06_TEMPLATE_RECOGNITION.md:181 — - TWHA902–904 use `choicePage` activity grids and dual titles + `whakatauki` — these are content patterns, safe to use if the new module needs them
  - KB: 06_TEMPLATE_RECOGNITION.md:265 — **The X-prefix test governs THIS CLASS ONLY.** The wider LS look-and-feel conventions of `14_SUBJECT_GLOBAL_PARAMETERS.md` § 14.6 — terminology and br
- **XDLS903** XDLS903_2_0.html ↔ XDLS903.02.html (content, derivable=True)
  - gold: `div.activity.dropbox[number=2G]  «Share your learning!»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [body] [/RED TEXT]🔴 Share your learning with your kaiako.`
- **XDLS904** XDLS904_1_0.html ↔ XDLS904_01.0.html (content, derivable=True)
  - gold: `div.activity.dropbox[number=1G]  «Share your learning!»`
  - Claude: `—`
  - WT: `Share your learning with your kaiako.`
- **XDLS905** XDLS905_1_0.html ↔ XDLS905.01.html (content, derivable=True)
  - gold: `div.activity.dropbox[number=1G]  «Share your learning!»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [body] [/RED TEXT]🔴 Share your learning with your kaiako.`
- modules: XDLS903, XDLS904, XDLS905, XDLS906, XDLS908, XDLS912

### #55 · activity · EXTRA · `div.activity.clickDropContent.dropbox[number=*]` › gold `—` vs Claude `a` — CANDIDATE
- pages 27 / modules 4 / lines 104; consensus (all) 0.95 of 75 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 3m/21p c=1.00; Inquiry 1m/6p c=0.78
- by subject: Leaving to Learn 4m/27p c=0.95
- by era: Refresh 4m/27p c=0.95
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:46 — | Activity class | `content activity activity-bg` | `activity` |
  - KB: 06_TEMPLATE_RECOGNITION.md:181 — - TWHA902–904 use `choicePage` activity grids and dual titles + `whakatauki` — these are content patterns, safe to use if the new module needs them
  - KB: 06_TEMPLATE_RECOGNITION.md:265 — **The X-prefix test governs THIS CLASS ONLY.** The wider LS look-and-feel conventions of `14_SUBJECT_GLOBAL_PARAMETERS.md` § 14.6 — terminology and br
- **XDLS903** XDLS903_2_0.html ↔ XDLS903.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `a  «Upload to dropbox»`
- **XDLS904** XDLS904_1_0.html ↔ XDLS904_01.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `a  «Upload to dropbox»`
- **XDLS905** XDLS905_1_0.html ↔ XDLS905.01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `a  «Upload to dropbox»`
- modules: XDLS903, XDLS904, XDLS905, XDLS906

### #57 · activity · EXTRA · `div.activity.dropbox[number=*]` › gold `—` vs Claude `a` — CANDIDATE
- pages 24 / modules 4 / lines 24; consensus (all) 0.83 of 75 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 3m/18p c=0.82; Inquiry 1m/6p c=0.83
- by subject: Leaving to Learn 4m/24p c=0.83
- by era: Refresh 4m/24p c=0.83
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:46 — | Activity class | `content activity activity-bg` | `activity` |
  - KB: 06_TEMPLATE_RECOGNITION.md:181 — - TWHA902–904 use `choicePage` activity grids and dual titles + `whakatauki` — these are content patterns, safe to use if the new module needs them
  - KB: 06_TEMPLATE_RECOGNITION.md:265 — **The X-prefix test governs THIS CLASS ONLY.** The wider LS look-and-feel conventions of `14_SUBJECT_GLOBAL_PARAMETERS.md` § 14.6 — terminology and br
- **XDLS903** XDLS903_2_0.html ↔ XDLS903.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `a  «Upload to dropbox»`
- **XDLS904** XDLS904_1_0.html ↔ XDLS904_01.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `a  «Upload to dropbox»`
- **XDLS905** XDLS905_1_0.html ↔ XDLS905.01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `a  «Upload to dropbox»`
- modules: XDLS903, XDLS904, XDLS905, XDLS906

### #349 · body · MISSING · `div#body` › gold `div.row` vs Claude `—` — CANDIDATE
- pages 61 / modules 11 / lines 229; consensus (all) 0.52 of 75 gold pages with the region; derivable 0.75 (57 lines with no WT source)
- by template: Standard 8m/45p c=0.53; Inquiry 3m/16p c=0.50
- by subject: Leaving to Learn 11m/61p c=0.52
- by era: Refresh 11m/61p c=0.52
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **XDLS501** XDLS501_1_0.html ↔ XDLS501.01.html (content, derivable=True)
  - gold: `div.row  «What public distance looks and feels like»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [H3]  [/RED TEXT]🔴Activity 1A: What public distance looks and feels like`
- **XDLS502** XDLS502_3_0.html ↔ XDLS502.02.html (content, derivable=True)
  - gold: `div.row  «Why do people need facilities?»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [H3]  [/RED TEXT]🔴**Why do people need facilities?**`
- **XDLS901** XDLS901_0_0.html ↔ XDLS901.00.html (content, derivable=True)
  - gold: `div.row  «A good life is fun and busy. Building a life we can enjoy means knowing how to solve problems when they happen, as well »`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [body]  [/RED TEXT]🔴A good life is fun and busy. A life we can enjoy, know how to solve problems when they happen and how to ask others for help to cope with the change that life can bring`
- modules: XDLS501, XDLS502, XDLS901, XDLS902, XDLS903, XDLS904, XDLS905, XDLS906, XDLS908, XDLS909, XDLS912

### #350 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `p` — CANDIDATE
- pages 43 / modules 11 / lines 126; consensus (all) 0.68 of 75 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 8m/29p c=0.63; Inquiry 3m/14p c=0.83
- by subject: Leaving to Learn 11m/43p c=0.68
- by era: Refresh 11m/43p c=0.68
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **XDLS502** XDLS502_4_0.html ↔ XDLS502.03.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Anxiety New Zealand»`
- **XDLS901** XDLS901_0_0.html ↔ XDLS901.00.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «By doing this, we can grow, learn new things, and enjoy special moments with the people we love.»`
- **XDLS902** XDLS902_5_0.html ↔ XDLS902.05.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Need someone safe to talk to?»`
- modules: XDLS502, XDLS901, XDLS902, XDLS903, XDLS904, XDLS905, XDLS906, XDLS908, XDLS909, XDLS911, XDLS912

### #351 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `WIDGET` — CANDIDATE
- pages 20 / modules 10 / lines 35; consensus (all) 0.79 of 75 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 8m/16p c=0.79; Inquiry 2m/4p c=0.78
- by subject: Leaving to Learn 10m/20p c=0.79
- by era: Refresh 10m/20p c=0.79
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **XDLS502** XDLS502_4_0.html ↔ XDLS502.03.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **XDLS901** XDLS901_2_0.html ↔ XDLS901.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **XDLS902** XDLS902_3_0.html ↔ XDLS902.03.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- modules: XDLS502, XDLS901, XDLS902, XDLS903, XDLS904, XDLS905, XDLS906, XDLS908, XDLS911, XDLS912

### #357 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `div.ratio.ratio-16x9.videoSection` — CANDIDATE
- pages 23 / modules 6 / lines 34; consensus (all) 0.88 of 75 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 4m/17p c=0.86; Inquiry 2m/6p c=0.94
- by subject: Leaving to Learn 6m/23p c=0.88
- by era: Refresh 6m/23p c=0.88
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:43 — | Video wrapper | `embed-responsive embed-responsive-16by9` | `ratio ratio-16x9` |
  - KB: 06_TEMPLATE_RECOGNITION.md:376 — <div class="videoSection ratio ratio-16x9">
  - KB: 01_PIPELINE_EXTRACTION_TAGS/01E_TAG_INTERPRETATION.md:59 — <div class="videoSection ratio ratio-16x9">
- **XDLS901** XDLS901_3_0.html ↔ XDLS901.03.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.ratio.ratio-16x9.videoSection`
- **XDLS903** XDLS903_1_0.html ↔ XDLS903.01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.ratio.ratio-16x9.videoSection`
- **XDLS904** XDLS904_1_0.html ↔ XDLS904_01.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.ratio.ratio-16x9.videoSection`
- modules: XDLS901, XDLS903, XDLS904, XDLS905, XDLS906, XDLS908
