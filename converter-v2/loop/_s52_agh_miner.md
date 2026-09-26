# DIFF_QUEUE.md — the diff miner's ranked class queue (LOOP__Autonomous_Rounds.md §1d)

**Produced:** 2026-09-26 16:58 NZST by `reference/tests/_diff_miner.py` on the CURRENT corpus (pageforge-site HEAD 3e4beab; Claude corpus 545 dirs). **Population:** the skeleton gate's own — 74 paired pages / 9 modules (compare_exclusions.txt honoured; acks / glossary / references pages excluded); parse errors skipped: 0 (must be 0); modules without a parsed WT: 0. Run time 3.8 s.

**What a row is.** One CLASS = (region, parent element, gold form, Claude form, direction) over every differing skeleton line of every paired page — the same lines, labels, widget collapse and difflib alignment the PRIMARY gate scores (each element its own line so it can be quoted). Direction: MISSING = gold has it, Claude lacks it; EXTRA = Claude has it, gold lacks it; SUBSTITUTED = same position, different tag / class / wrapper; MOVED = same text, different place. Consensus = of the gold pages in the group where the region exists, the share carrying the gold form (for EXTRA: the share NOT carrying Claude's form). Derivable = the gold line's text is in the module's parsed Writers Template (round-110 tolerance); structure-only differences are always derivable.

**Candidate rule (§1d).** modules ≥ 10 for a chrome class (module-code / title / header / module-menu / crumbs / phases-nav / footer / acks), pages ≥ 20 for a body / activity class; gold consensus ≥ 0.60 in at least one template or subject group that itself reaches the floor; structure-only or derivable share ≥ 0.60. A class below the floor is listed, never dropped. A CANDIDATE still goes through the PICK's KB-first check, the triangulation and the §3 corpus-wide measurement before any code — this table is the queue, not the verdict.

## Summary

- differing skeleton lines: 5682 — by direction {'MISSING': 2915, 'SUBSTITUTED': 513, 'EXTRA': 2132, 'MOVED': 122}
- by region: {'title': 1, 'module-menu': 108, 'footer': 6, 'acks': 32, 'activity': 1227, 'body': 4276, 'root': 32}
- classes: 488 — CANDIDATE 2, below floor 478, the rest below consensus / not derivable

## Completeness census — the repeating chrome (§1d item 4)

| region | pages with region | gold items | gold items in WT | Claude items | derivable misses | pages with misses | modules with misses | status |
|---|---|---|---|---|---|---|---|---|
| module-menu | 65 | 411 | 407 | 433 | 9 | 5 | 3 | BELOW FLOOR |
| crumbs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |
| phases-nav | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |
| footer | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |

- **module-menu** by template: Standard 3m/5p/9 misses
  - AGH1009 AGH1009_8_0.html: gold 7 items (7 in WT) / Claude 8 — 4 derivable misses, e.g. li «identify and describe the impact historic primary production practices have had » · b «soil, and soil microbes»
  - AGH1007 AGH1007_9_0.html: gold 4 items (4 in WT) / Claude 5 — 2 derivable misses, e.g. li «to identify the causes of health problems in livestock.» · li «demonstrating knowledge of specific diseases in livestock and their causes.»
  - AGH1004 AGH1004_2_0.html: gold 6 items (6 in WT) / Claude 5 — 1 derivable misses, e.g. h5 «We are learning to:»
  - AGH1007 AGH1007_3_0.html: gold 4 items (4 in WT) / Claude 5 — 1 derivable misses, e.g. li «demonstrating the differences between monogastric and ruminant digestive systems»
- **crumbs** by template: 
- **phases-nav** by template: 
- **footer** by template: 

## Chrome facts — the header and footer as SETS per page (alignment-free; §1d items 2 + 4)

A fact is one thing a page's chrome has: `header:chip` (the `#module-code` div), `header:chip=module-code` / `=lesson-number` / `=lesson-number(00)`, `header:head-buttons`, `header:menu-content`, `header:title-h1-count=N`, `footer:present`, `footer:ul=<classes>`, `footer:link=prev-lesson` / `next-lesson` / `home-nav`, `footer:links=<order>`, `footer:inside-body`, `nav:crumbs`, `nav:phases`. MISSING = the gold page has the fact and Claude's does not; EXTRA the reverse. Consensus = the share of gold pages in the group that have (MISSING) / lack (EXTRA) the fact. Floor 10 modules.

| # | dir | fact | pages | modules | gold share (all) | consensus (all) | best group | status |
|---|---|---|---|---|---|---|---|---|
| F1 | MISSING | `header:title-h1-count=2` | 1 | 1 | 0.11 | 0.11 | — | BELOW FLOOR |
| F2 | EXTRA | `header:title-h1-count=3` | 1 | 1 | 0.01 | 0.99 | — | BELOW FLOOR |
| F3 | MISSING | `footer:links=prev-lesson,next-lesson,home-nav` | 2 | 2 | 0.80 | 0.80 | — | BELOW FLOOR |
| F4 | MISSING | `footer:link=next-lesson` | 2 | 2 | 0.92 | 0.92 | — | BELOW FLOOR |
| F5 | EXTRA | `footer:links=prev-lesson,home-nav` | 2 | 2 | 0.08 | 0.92 | — | BELOW FLOOR |
| F6 | MISSING | `footer:links=prev-lesson,home-nav` | 1 | 1 | 0.08 | 0.08 | — | BELOW FLOOR |
| F7 | EXTRA | `footer:links=prev-lesson,next-lesson,home-nav` | 1 | 1 | 0.80 | 0.20 | — | BELOW FLOOR |
| F8 | EXTRA | `footer:link=next-lesson` | 1 | 1 | 0.92 | 0.08 | — | BELOW FLOOR |


## The ranked queue — chrome regions first, then by modules affected

| # | region | dir | parent | gold form | Claude form | pages | modules | consensus (all) | best group | derivable | KB | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | title | EXTRA | `div#header` | `—` | `h1>span` | 1 | 1 | 0.99 of 74 | — | structure | yes | BELOW FLOOR |
| 2 | module-menu | EXTRA | `ul` | `—` | `li` | 12 | 5 | 0.27 of 74 | — | structure | — | BELOW FLOOR |
| 3 | module-menu | SUBSTITUTED | `div.col-12.col-md-8` | `h4` | `h5` | 14 | 3 | 0.19 of 74 | — | structure | — | BELOW FLOOR |
| 4 | module-menu | SUBSTITUTED | `div.col-12.col-md-8` | `ul` | `ol` | 12 | 3 | 0.85 of 74 | — | structure | — | BELOW FLOOR |
| 5 | module-menu | EXTRA | `li>b` | `—` | `b` | 10 | 3 | 0.89 of 74 | — | structure | — | BELOW FLOOR |
| 6 | module-menu | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `ul` | 7 | 3 | 0.10 of 74 | — | structure | — | BELOW FLOOR |
| 7 | module-menu | MISSING | `ul` | `li` | `—` | 3 | 3 | 0.11 of 74 | — | 0.67 | — | BELOW FLOOR |
| 8 | module-menu | EXTRA | `li` | `—` | `b` | 4 | 2 | 0.97 of 74 | — | structure | — | BELOW FLOOR |
| 9 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `h5` | 3 | 1 | 0.31 of 74 | — | structure | — | BELOW FLOOR |
| 10 | module-menu | MISSING | `div.col-12.col-md-8` | `h4` | `—` | 3 | 1 | 0.18 of 74 | — | 1.00 | — | BELOW FLOOR |
| 11 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 1 | 1 | 0.91 of 74 | — | structure | — | BELOW FLOOR |
| 12 | module-menu | EXTRA | `ul` | `—` | `li>b` | 1 | 1 | 0.96 of 74 | — | structure | — | BELOW FLOOR |
| 13 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `ul` | 1 | 1 | 0.22 of 74 | — | structure | — | BELOW FLOOR |
| 14 | module-menu | MISSING | `div.col-12.col-md-8` | `h5` | `—` | 1 | 1 | 0.69 of 74 | — | 1.00 | — | BELOW FLOOR |
| 15 | module-menu | MISSING | `li` | `p` | `—` | 1 | 1 | 0.03 of 74 | — | 1.00 | — | BELOW FLOOR |
| 16 | module-menu | MISSING | `div.col-12.col-md-8` | `ul` | `—` | 1 | 1 | 0.78 of 74 | — | 1.00 | — | BELOW FLOOR |
| 17 | module-menu | MISSING | `li` | `b` | `—` | 1 | 1 | 0.10 of 74 | — | 1.00 | — | BELOW FLOOR |
| 18 | footer | MISSING | `li>a#next-lesson` | `a#next-lesson` | `—` | 2 | 2 | 0.92 of 74 | — | structure | yes | BELOW FLOOR |
| 19 | footer | MISSING | `ul.footer-nav` | `li>a.home-nav` | `—` | 2 | 2 | 1.00 of 74 | — | structure | yes | BELOW FLOOR |
| 20 | footer | EXTRA | `li>a#next-lesson` | `—` | `a#next-lesson` | 1 | 1 | 0.08 of 74 | — | structure | yes | BELOW FLOOR |
| 21 | footer | EXTRA | `ul.footer-nav` | `—` | `li>a.home-nav` | 1 | 1 | 0.00 of 74 | — | structure | yes | BELOW FLOOR |
| 22 | activity | MISSING | `div.col-12` | `h3` | `—` | 49 | 9 | 0.66 of 74 | ptype=lesson c=0.75 n=49 | 0.47 | — | NOT DERIVABLE (content share < 0.60) |
| 23 | activity | MISSING | `a` | `div.button` | `—` | 30 | 9 | 0.73 of 74 | ptype=lesson c=0.83 n=30 | 0.02 | yes | NOT DERIVABLE (content share < 0.60) |
| 24 | activity | MISSING | `div.col-12` | `a` | `—` | 30 | 8 | 0.73 of 74 | ptype=lesson c=0.83 n=30 | 0.00 | — | NOT DERIVABLE (content share < 0.60) |
| 25 | activity | MISSING | `div.col-12` | `p` | `—` | 21 | 8 | 0.45 of 74 | — | 0.70 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 26 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `div.activity[number=*]` | 11 | 7 | 0.46 of 74 | — | structure | yes | BELOW FLOOR |
| 27 | activity | EXTRA | `div.col-12` | `—` | `p` | 11 | 6 | 0.96 of 74 | — | structure | — | BELOW FLOOR |
| 28 | activity | EXTRA | `div.col-12` | `—` | `WIDGET` | 6 | 6 | 0.76 of 74 | — | structure | — | BELOW FLOOR |
| 29 | activity | MISSING | `div.col-12` | `WIDGET` | `—` | 9 | 5 | 0.24 of 74 | — | structure | — | BELOW FLOOR |
| 30 | activity | MISSING | `div.activity.interactive[number=*]` | `div.row` | `—` | 8 | 5 | 0.15 of 74 | — | 1.00 | yes | BELOW FLOOR |
| 31 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `div.activity[number=*]` | 7 | 5 | 0.64 of 74 | — | structure | yes | BELOW FLOOR |
| 32 | activity | EXTRA | `div.col-12` | `—` | `ol` | 8 | 4 | 1.00 of 74 | — | structure | — | BELOW FLOOR |
| 33 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `div.activity.interactive[number=*]` | 8 | 4 | 0.64 of 74 | — | structure | yes | BELOW FLOOR |
| 34 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `h3` | 6 | 4 | 0.64 of 74 | — | structure | yes | BELOW FLOOR |
| 35 | activity | MISSING | `div.col-12` | `div.hint` | `—` | 4 | 4 | 0.10 of 74 | — | structure | yes | BELOW FLOOR |
| 36 | activity | MISSING | `div.col-12` | `div.row` | `—` | 4 | 4 | 0.12 of 74 | — | structure | — | BELOW FLOOR |
| 37 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `div.activity.interactive[number=*]` | 4 | 4 | 0.46 of 74 | — | structure | yes | BELOW FLOOR |
| 38 | activity | SUBSTITUTED | `div.col-12` | `a` | `h4.goJournal` | 6 | 3 | 0.73 of 74 | — | structure | — | BELOW FLOOR |
| 39 | activity | EXTRA | `ol` | `—` | `li` | 4 | 3 | 0.99 of 74 | — | structure | — | BELOW FLOOR |
| 40 | activity | EXTRA | `div.activity.interactive[number=*]` | `—` | `div.row` | 4 | 3 | 0.85 of 74 | — | structure | yes | BELOW FLOOR |
| 41 | activity | EXTRA | `div.col-12` | `—` | `h4.goJournal` | 3 | 3 | 1.00 of 74 | — | structure | — | BELOW FLOOR |
| 42 | activity | EXTRA | `ul` | `—` | `li` | 3 | 3 | 0.97 of 74 | — | structure | — | BELOW FLOOR |
| 43 | activity | MISSING | `div.icon.ratio.ratio-16x9.videoSection` | `iframe.embed-responsive-item` | `—` | 3 | 3 | 0.08 of 74 | — | structure | yes | BELOW FLOOR |
| 44 | activity | MISSING | `div.activity[number=*]` | `div.row` | `—` | 3 | 3 | 0.19 of 74 | — | 0.33 | yes | BELOW FLOOR |
| 45 | activity | SUBSTITUTED | `div.col-12` | `a` | `p` | 3 | 3 | 0.73 of 74 | — | structure | — | BELOW FLOOR |
| 46 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `p` | 3 | 3 | 0.61 of 74 | — | structure | — | BELOW FLOOR |
| 47 | activity | SUBSTITUTED | `div.col-12` | `div.activity.interactive[number=*]` | `div.activity[number=*]` | 3 | 3 | 0.19 of 74 | — | structure | yes | BELOW FLOOR |
| 48 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.alertPadding[number=*]` | `div.activity[number=*]` | 3 | 3 | 0.10 of 74 | — | structure | yes | BELOW FLOOR |
| 49 | activity | SUBSTITUTED | `a` | `div.button` | `li` | 3 | 3 | 0.73 of 74 | — | structure | yes | BELOW FLOOR |
| 50 | activity | EXTRA | `div.col-12` | `—` | `div.ratio.ratio-16x9.videoSection` | 4 | 2 | 0.99 of 74 | — | structure | yes | BELOW FLOOR |
| 51 | activity | MISSING | `div.activity.interactive[number=*]` | `WIDGET` | `—` | 4 | 2 | 0.03 of 74 | — | structure | yes | BELOW FLOOR |
| 52 | activity | SUBSTITUTED | `div.col-12` | `a` | `WIDGET` | 4 | 2 | 0.73 of 74 | — | structure | — | BELOW FLOOR |
| 53 | activity | EXTRA | `div.col-12` | `—` | `p>span.infoTrigger` | 3 | 2 | 1.00 of 74 | — | structure | — | BELOW FLOOR |
| 54 | activity | EXTRA | `div.col-12.col-md-8` | `—` | `div.activity[number=*]` | 3 | 2 | 0.81 of 74 | — | structure | yes | BELOW FLOOR |
| 55 | activity | MISSING | `div.row` | `div.col-12` | `—` | 3 | 2 | 0.15 of 74 | — | 0.67 | — | BELOW FLOOR |
| 56 | activity | MISSING | `div.col-12` | `div.icon.ratio.ratio-16x9.videoSection` | `—` | 3 | 2 | 0.03 of 74 | — | structure | yes | BELOW FLOOR |
| 57 | activity | SUBSTITUTED | `div.col-12` | `h3` | `WIDGET` | 3 | 2 | 0.86 of 74 | — | structure | — | BELOW FLOOR |
| 58 | activity | SUBSTITUTED | `div.activity.interactive[number=*]` | `WIDGET` | `WIDGET` | 3 | 2 | 0.11 of 74 | — | structure | yes | BELOW FLOOR |
| 59 | activity | EXTRA | `div.col-12` | `—` | `img.img-fluid` | 2 | 2 | 1.00 of 74 | — | structure | — | BELOW FLOOR |
| 60 | activity | EXTRA | `div.col-12` | `—` | `ul` | 2 | 2 | 0.99 of 74 | — | structure | — | BELOW FLOOR |
| 61 | activity | EXTRA | `div.col-12` | `—` | `a` | 2 | 2 | 0.27 of 74 | — | structure | — | BELOW FLOOR |
| 62 | activity | EXTRA | `p>b` | `—` | `b` | 2 | 2 | 1.00 of 74 | — | structure | — | BELOW FLOOR |
| 63 | activity | EXTRA | `div.activity[number=*]` | `—` | `div.row` | 2 | 2 | 0.95 of 74 | — | structure | yes | BELOW FLOOR |
| 64 | activity | MISSING | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `—` | 2 | 2 | 0.01 of 74 | — | 0.50 | yes | BELOW FLOOR |
| 65 | activity | MISSING | `div.col-12` | `div.clickDropContent` | `—` | 2 | 2 | 0.04 of 74 | — | 1.00 | — | BELOW FLOOR |
| 66 | activity | MISSING | `div.col-12.col-md-8` | `div.activity[number=*]` | `—` | 2 | 2 | 0.19 of 74 | — | 1.00 | yes | BELOW FLOOR |
| 67 | activity | MISSING | `div.activity.dropbox[number=*]` | `div.row` | `—` | 2 | 2 | 0.11 of 74 | — | 0.50 | yes | BELOW FLOOR |
| 68 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `h3` | 2 | 2 | 0.46 of 74 | — | structure | yes | BELOW FLOOR |
| 69 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.alertPadding.interactive[number=*]` | `div.activity.interactive[number=*]` | 2 | 2 | 0.04 of 74 | — | structure | yes | BELOW FLOOR |
| 70 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `ul` | 2 | 2 | 0.61 of 74 | — | structure | — | BELOW FLOOR |
| 71 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `div.alert.solid` | 2 | 2 | 0.64 of 74 | — | structure | yes | BELOW FLOOR |
| 72 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.dropbox[number=*]` | `div.alert.solid` | 2 | 2 | 0.11 of 74 | — | structure | yes | BELOW FLOOR |
| 73 | activity | SUBSTITUTED | `div.col-12` | `p` | `WIDGET` | 2 | 2 | 0.85 of 74 | — | structure | — | BELOW FLOOR |
| 74 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `h4` | 2 | 2 | 0.64 of 74 | — | structure | yes | BELOW FLOOR |
| 75 | activity | MISSING | `div.row` | `div.col-12.col-md-8` | `—` | 3 | 1 | 0.04 of 74 | — | 1.00 | — | BELOW FLOOR |
| 76 | activity | SUBSTITUTED | `div.col-12` | `h3` | `h4` | 3 | 1 | 0.86 of 74 | — | structure | — | BELOW FLOOR |
| 77 | activity | MOVED | `div.col-12` | `h3` | `h3` | 2 | 1 | 0.39 of 74 | — | structure | — | BELOW FLOOR |
| 78 | activity | SUBSTITUTED | `div.col-12` | `h3` | `div` | 2 | 1 | 0.86 of 74 | — | structure | — | BELOW FLOOR |
| 79 | activity | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `div.col-12` | 2 | 1 | 0.12 of 74 | — | structure | — | BELOW FLOOR |
| 80 | activity | SUBSTITUTED | `div.col-12` | `p` | `ul` | 2 | 1 | 0.85 of 74 | — | structure | — | BELOW FLOOR |
| 81 | activity | SUBSTITUTED | `a` | `div.button` | `div.col-12.col-md-8` | 2 | 1 | 0.73 of 74 | — | structure | yes | BELOW FLOOR |
| 82 | activity | EXTRA | `div.col-12` | `—` | `h5` | 1 | 1 | 1.00 of 74 | — | structure | — | BELOW FLOOR |
| 83 | activity | EXTRA | `div.col-12.col-md-8` | `—` | `div.activity.interactive[number=*]` | 1 | 1 | 0.99 of 74 | — | structure | yes | BELOW FLOOR |
| 84 | activity | EXTRA | `div.col-12` | `—` | `p>a` | 1 | 1 | 1.00 of 74 | — | structure | — | BELOW FLOOR |
| 85 | activity | EXTRA | `p>i` | `—` | `i` | 1 | 1 | 1.00 of 74 | — | structure | — | BELOW FLOOR |
| 86 | activity | MISSING | `div.activity.alertPadding.interactive[nu` | `WIDGET` | `—` | 1 | 1 | 0.01 of 74 | — | structure | yes | BELOW FLOOR |
| 87 | activity | MISSING | `div.col-12` | `div.ratio.ratio-16x9.videoSection` | `—` | 1 | 1 | 0.01 of 74 | — | structure | yes | BELOW FLOOR |
| 88 | activity | MISSING | `div.col-12` | `h4` | `—` | 1 | 1 | 0.01 of 74 | — | 1.00 | — | BELOW FLOOR |
| 89 | activity | MISSING | `div.col-12.col-md-8` | `h3` | `—` | 1 | 1 | 0.03 of 74 | — | 0.00 | — | BELOW FLOOR |
| 90 | activity | MISSING | `ul` | `li` | `—` | 1 | 1 | 0.03 of 74 | — | 0.00 | — | BELOW FLOOR |
| 91 | activity | MISSING | `div.col-12` | `ul` | `—` | 1 | 1 | 0.01 of 74 | — | 0.00 | — | BELOW FLOOR |
| 92 | activity | MISSING | `div.col-12.col-md-8` | `p` | `—` | 1 | 1 | 0.12 of 74 | — | 1.00 | — | BELOW FLOOR |
| 93 | activity | MISSING | `a` | `div.externalButton` | `—` | 1 | 1 | 0.03 of 74 | — | 0.00 | — | BELOW FLOOR |
| 94 | activity | MISSING | `div.activity.alertPadding[number=*]` | `div.row` | `—` | 1 | 1 | 0.10 of 74 | — | 1.00 | yes | BELOW FLOOR |
| 95 | activity | MISSING | `div.row` | `hr` | `—` | 1 | 1 | 0.01 of 74 | — | structure | — | BELOW FLOOR |
| 96 | activity | MISSING | `div.row` | `p` | `—` | 1 | 1 | 0.03 of 74 | — | 1.00 | — | BELOW FLOOR |
| 97 | activity | MISSING | `div.row` | `a` | `—` | 1 | 1 | 0.01 of 74 | — | 0.00 | — | BELOW FLOOR |
| 98 | activity | MISSING | `div.col-12` | `hr` | `—` | 1 | 1 | 0.01 of 74 | — | structure | — | BELOW FLOOR |
| 99 | activity | MISSING | `div.col-12` | `img.img-fluid` | `—` | 1 | 1 | 0.03 of 74 | — | structure | — | BELOW FLOOR |
| 100 | activity | MOVED | `ol` | `li` | `li` | 1 | 1 | 0.03 of 74 | — | structure | — | BELOW FLOOR |
| 143 | body | EXTRA | `div#body` | `—` | `div.row` | 43 | 9 | 0.61 of 74 | template=Standard c=0.61 n=43 | structure | — | CANDIDATE |
| 160 | body | SUBSTITUTED | `div.row` | `div.col-12` | `div.col-12.col-md-8` | 21 | 5 | 0.88 of 74 | ptype=lesson c=0.98 n=21 | structure | — | CANDIDATE |

## Details — in the companion file `CONVERTER_V2/outputs/_s52_agh_miner_details.md`
Every CANDIDATE and every top-40 row has three quoted examples (WT / gold / Claude) there, plus the
below-floor list. **NEVER read the companion whole** (hundreds of KB): `grep -n '^### #<rank> ' CONVERTER_V2/outputs/_diff_queue_details.md` then `sed -n '<start>,<start+40>p'`. The top 25
candidates' detail blocks are repeated below for convenience.

### #143 · body · EXTRA · `div#body` › gold `—` vs Claude `div.row` — CANDIDATE
- pages 43 / modules 9 / lines 138; consensus (all) 0.61 of 74 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 9m/43p c=0.61
- by subject: NCEA1 9m/43p c=0.61
- by era: Refresh 9m/43p c=0.61
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1001** AGH1001_2_0.html ↔ AGH1001.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Career Example:»`
- **AGH1002** AGH1002_1_0.html ↔ AGH1002.01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Summary»`
- **AGH1003** AGH1003_2_0.html ↔ AGH1003_02.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Irrigation and chemical properties of soil»`
- modules: AGH1001, AGH1002, AGH1003, AGH1004, AGH1005, AGH1006, AGH1007, AGH1008, AGH1009

### #160 · body · SUBSTITUTED · `div.row` › gold `div.col-12` vs Claude `div.col-12.col-md-8` — CANDIDATE
- pages 21 / modules 5 / lines 31; consensus (all) 0.88 of 74 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 5m/21p c=0.88
- by subject: NCEA1 5m/21p c=0.88
- by era: Refresh 5m/21p c=0.88
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1001** AGH1001_1_0.html ↔ AGH1001.01.html (structure, derivable=True)
  - gold: `div.col-12  «What are primary products?»`
  - Claude: `div.col-12.col-md-8`
- **AGH1002** AGH1002_2_0.html ↔ AGH1002.02.html (structure, derivable=True)
  - gold: `div.col-12  «Soil texture»`
  - Claude: `div.col-12.col-md-8  «Soil Texture»`
- **AGH1003** AGH1003_1_0.html ↔ AGH1003_01.0.html (structure, derivable=True)
  - gold: `div.col-12  «Soil Science Recap»`
  - Claude: `div.col-12.col-md-8  «Answer the questions below.»`
- modules: AGH1001, AGH1002, AGH1003, AGH1004, AGH1007
