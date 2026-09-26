# DIFF_QUEUE.md — the diff miner's ranked class queue (LOOP__Autonomous_Rounds.md §1d)

**Produced:** 2026-09-26 13:27 NZST by `reference/tests/_diff_miner.py` on the CURRENT corpus (pageforge-site HEAD 84b660d; Claude corpus 545 dirs). **Population:** the skeleton gate's own — 76 paired pages / 7 modules (compare_exclusions.txt honoured; acks / glossary / references pages excluded); parse errors skipped: 0 (must be 0); modules without a parsed WT: 0. Run time 4.0 s.

**What a row is.** One CLASS = (region, parent element, gold form, Claude form, direction) over every differing skeleton line of every paired page — the same lines, labels, widget collapse and difflib alignment the PRIMARY gate scores (each element its own line so it can be quoted). Direction: MISSING = gold has it, Claude lacks it; EXTRA = Claude has it, gold lacks it; SUBSTITUTED = same position, different tag / class / wrapper; MOVED = same text, different place. Consensus = of the gold pages in the group where the region exists, the share carrying the gold form (for EXTRA: the share NOT carrying Claude's form). Derivable = the gold line's text is in the module's parsed Writers Template (round-110 tolerance); structure-only differences are always derivable.

**Candidate rule (§1d).** modules ≥ 10 for a chrome class (module-code / title / header / module-menu / crumbs / phases-nav / footer / acks), pages ≥ 20 for a body / activity class; gold consensus ≥ 0.60 in at least one template or subject group that itself reaches the floor; structure-only or derivable share ≥ 0.60. A class below the floor is listed, never dropped. A CANDIDATE still goes through the PICK's KB-first check, the triangulation and the §3 corpus-wide measurement before any code — this table is the queue, not the verdict.

## Summary

- differing skeleton lines: 5015 — by direction {'MISSING': 2992, 'EXTRA': 1424, 'SUBSTITUTED': 500, 'MOVED': 99}
- by region: {'title': 15, 'module-menu': 173, 'footer': 9, 'acks': 26, 'activity': 1094, 'body': 3650, 'root': 48}
- classes: 450 — CANDIDATE 4, below floor 441, the rest below consensus / not derivable

## Completeness census — the repeating chrome (§1d item 4)

| region | pages with region | gold items | gold items in WT | Claude items | derivable misses | pages with misses | modules with misses | status |
|---|---|---|---|---|---|---|---|---|
| module-menu | 45 | 251 | 243 | 192 | 42 | 10 | 4 | BELOW FLOOR |
| crumbs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |
| phases-nav | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |
| footer | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |

- **module-menu** by template: Standard 4m/10p/42 misses
  - PES1004 PES1004_4_0.html: gold 6 items (6 in WT) / Claude 0 — 6 derivable misses, e.g. h5 «We are learning about:» · li «how to calculate the gradient of a line»
  - PES1005 PES1005_2_0.html: gold 5 items (5 in WT) / Claude 0 — 5 derivable misses, e.g. h5 «We are learning about:» · li «how Polynesian navigators used objects in the sky to navigate the open ocean.»
  - PES1005 PES1005_9_0.html: gold 5 items (5 in WT) / Claude 0 — 5 derivable misses, e.g. h5 «We are learning about:» · li «how the Sun affects planet Earth.»
  - PES1007 PES1007_7_0.html: gold 5 items (5 in WT) / Claude 0 — 5 derivable misses, e.g. h5 «We are learning about:» · li «Describe the meaning of the term ‘gravitational potential energy’.»
- **crumbs** by template: 
- **phases-nav** by template: 
- **footer** by template: 

## Chrome facts — the header and footer as SETS per page (alignment-free; §1d items 2 + 4)

A fact is one thing a page's chrome has: `header:chip` (the `#module-code` div), `header:chip=module-code` / `=lesson-number` / `=lesson-number(00)`, `header:head-buttons`, `header:menu-content`, `header:title-h1-count=N`, `footer:present`, `footer:ul=<classes>`, `footer:link=prev-lesson` / `next-lesson` / `home-nav`, `footer:links=<order>`, `footer:inside-body`, `nav:crumbs`, `nav:phases`. MISSING = the gold page has the fact and Claude's does not; EXTRA the reverse. Consensus = the share of gold pages in the group that have (MISSING) / lack (EXTRA) the fact. Floor 10 modules.

| # | dir | fact | pages | modules | gold share (all) | consensus (all) | best group | status |
|---|---|---|---|---|---|---|---|---|
| F1 | EXTRA | `header:menu-content` | 5 | 3 | 0.67 | 0.33 | — | BELOW FLOOR |
| F2 | EXTRA | `header:head-buttons` | 5 | 3 | 0.67 | 0.33 | — | BELOW FLOOR |
| F3 | MISSING | `header:title-h1-count=2` | 2 | 2 | 0.07 | 0.07 | — | BELOW FLOOR |
| F4 | EXTRA | `header:title-h1-count=1` | 2 | 2 | 0.93 | 0.07 | — | BELOW FLOOR |
| F5 | MISSING | `footer:inside-body` | 1 | 1 | 0.01 | 0.01 | — | BELOW FLOOR |
| F6 | MISSING | `footer:link=prev-lesson` | 1 | 1 | 0.92 | 0.92 | — | BELOW FLOOR |
| F7 | MISSING | `footer:links=prev-lesson,next-lesson,home-nav` | 1 | 1 | 0.84 | 0.84 | — | BELOW FLOOR |
| F8 | EXTRA | `footer:links=next-lesson,home-nav` | 1 | 1 | 0.08 | 0.92 | — | BELOW FLOOR |


## The ranked queue — chrome regions first, then by modules affected

| # | region | dir | parent | gold form | Claude form | pages | modules | consensus (all) | best group | derivable | KB | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | title | MISSING | `div#header` | `h1>span` | `—` | 2 | 2 | 0.07 of 76 | — | 1.00 | yes | BELOW FLOOR |
| 2 | title | EXTRA | `msub` | `—` | `mrow` | 1 | 1 | 1.00 of 76 | — | structure | — | BELOW FLOOR |
| 3 | title | EXTRA | `mfrac` | `—` | `mrow` | 1 | 1 | 1.00 of 76 | — | structure | — | BELOW FLOOR |
| 4 | title | EXTRA | `mrow` | `—` | `mi` | 1 | 1 | 1.00 of 76 | — | structure | — | BELOW FLOOR |
| 5 | title | EXTRA | `msup` | `—` | `mrow` | 1 | 1 | 1.00 of 76 | — | structure | — | BELOW FLOOR |
| 6 | title | MISSING | `msup` | `mn` | `—` | 1 | 1 | 0.01 of 76 | — | 1.00 | — | BELOW FLOOR |
| 7 | title | SUBSTITUTED | `msub` | `mi` | `mrow` | 1 | 1 | 0.01 of 76 | — | structure | — | BELOW FLOOR |
| 8 | title | SUBSTITUTED | `msub` | `mi` | `mi` | 1 | 1 | 0.01 of 76 | — | structure | — | BELOW FLOOR |
| 9 | title | SUBSTITUTED | `mfrac` | `mn` | `mrow` | 1 | 1 | 0.01 of 76 | — | structure | — | BELOW FLOOR |
| 10 | title | SUBSTITUTED | `mfrac` | `mn` | `mn` | 1 | 1 | 0.01 of 76 | — | structure | — | BELOW FLOOR |
| 11 | title | SUBSTITUTED | `msup` | `mi` | `mrow` | 1 | 1 | 0.01 of 76 | — | structure | — | BELOW FLOOR |
| 12 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-8.paddingR` | `div.col-12.col-md-8` | 44 | 5 | 0.58 of 76 | — | structure | yes | BELOW FLOOR |
| 13 | module-menu | MISSING | `div.col-12.col-md-8.paddingR` | `h5` | `—` | 12 | 4 | 0.58 of 76 | — | 1.00 | yes | BELOW FLOOR |
| 14 | module-menu | MISSING | `div.col-12.col-md-8.paddingR` | `ul` | `—` | 11 | 3 | 0.58 of 76 | — | 0.90 | yes | BELOW FLOOR |
| 15 | module-menu | EXTRA | `div#header` | `—` | `div#module-head-buttons` | 5 | 3 | 0.33 of 76 | — | structure | yes | BELOW FLOOR |
| 16 | module-menu | EXTRA | `div#header` | `—` | `div#module-menu-content.moduleMenu` | 5 | 3 | 0.33 of 76 | — | structure | yes | BELOW FLOOR |
| 17 | module-menu | MISSING | `li` | `math` | `—` | 3 | 1 | 0.03 of 76 | — | 1.00 | — | BELOW FLOOR |
| 18 | module-menu | SUBSTITUTED | `div.col-12.col-md-8.paddingR` | `h5` | `p` | 2 | 1 | 0.58 of 76 | — | structure | yes | BELOW FLOOR |
| 19 | module-menu | MOVED | `ul` | `li` | `li` | 1 | 1 | 0.24 of 76 | — | structure | — | BELOW FLOOR |
| 20 | module-menu | MOVED | `div.col-12.col-md-8.paddingR` | `h5` | `h5` | 1 | 1 | 0.58 of 76 | — | structure | yes | BELOW FLOOR |
| 21 | module-menu | SUBSTITUTED | `ul` | `ul` | `ul` | 1 | 1 | 0.01 of 76 | — | structure | — | BELOW FLOOR |
| 22 | module-menu | SUBSTITUTED | `ul` | `li` | `li` | 1 | 1 | 0.58 of 76 | — | structure | — | BELOW FLOOR |
| 23 | footer | MISSING | `ul.footer-nav` | `li>a#prev-lesson` | `—` | 2 | 2 | 0.92 of 76 | — | structure | yes | BELOW FLOOR |
| 24 | footer | EXTRA | `div#footer` | `—` | `ul.footer-nav` | 1 | 1 | 0.00 of 76 | — | structure | yes | BELOW FLOOR |
| 25 | footer | MISSING | `div#body` | `div#footer` | `—` | 1 | 1 | 0.01 of 76 | — | structure | yes | BELOW FLOOR |
| 26 | footer | MISSING | `ul.footer-nav` | `li>a#next-lesson` | `—` | 1 | 1 | 0.92 of 76 | — | structure | yes | BELOW FLOOR |
| 27 | footer | MISSING | `ul.footer-nav` | `li>a.home-nav` | `—` | 1 | 1 | 1.00 of 76 | — | structure | yes | BELOW FLOOR |
| 28 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav` | `li>a.home-nav` | 1 | 1 | 1.00 of 76 | — | structure | yes | BELOW FLOOR |
| 29 | activity | MISSING | `a` | `div.button` | `—` | 40 | 7 | 0.30 of 76 | — | 0.17 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 30 | activity | MISSING | `div.col-12` | `p` | `—` | 18 | 5 | 0.42 of 76 | — | 0.61 | — | BELOW FLOOR |
| 31 | activity | MISSING | `div.col-12` | `a` | `—` | 16 | 5 | 0.30 of 76 | — | 0.00 | — | BELOW FLOOR |
| 32 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `h3` | 6 | 5 | 0.49 of 76 | — | structure | yes | BELOW FLOOR |
| 33 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `div.activity[number=*]` | 14 | 4 | 0.35 of 76 | — | structure | yes | BELOW FLOOR |
| 34 | activity | MISSING | `div.activity.interactive[number=*]` | `div.row` | `—` | 8 | 4 | 0.20 of 76 | — | 0.82 | yes | BELOW FLOOR |
| 35 | activity | MISSING | `div.col-12` | `WIDGET` | `—` | 7 | 4 | 0.28 of 76 | — | structure | — | BELOW FLOOR |
| 36 | activity | MISSING | `div.activity[number=*]` | `div.row` | `—` | 5 | 4 | 0.49 of 76 | — | 0.80 | yes | BELOW FLOOR |
| 37 | activity | MISSING | `a` | `div.externalButton` | `—` | 5 | 4 | 0.08 of 76 | — | 0.33 | — | BELOW FLOOR |
| 38 | activity | MISSING | `div.activity.dropbox[number=*]` | `div.row` | `—` | 4 | 4 | 0.12 of 76 | — | 0.75 | yes | BELOW FLOOR |
| 39 | activity | MISSING | `div.col-12` | `div.row` | `—` | 4 | 4 | 0.14 of 76 | — | structure | — | BELOW FLOOR |
| 40 | activity | EXTRA | `ol` | `—` | `li` | 9 | 3 | 1.00 of 76 | — | structure | — | BELOW FLOOR |
| 41 | activity | MISSING | `div.row` | `div.col-12` | `—` | 7 | 3 | 0.41 of 76 | — | 0.50 | — | BELOW FLOOR |
| 42 | activity | EXTRA | `div.col-12` | `—` | `p` | 5 | 3 | 0.99 of 76 | — | structure | — | BELOW FLOOR |
| 43 | activity | EXTRA | `div.col-12` | `—` | `ol` | 4 | 3 | 1.00 of 76 | — | structure | — | BELOW FLOOR |
| 44 | activity | EXTRA | `div.col-12` | `—` | `ul` | 4 | 3 | 0.95 of 76 | — | structure | — | BELOW FLOOR |
| 45 | activity | MISSING | `div.col-12` | `ul` | `—` | 4 | 3 | 0.05 of 76 | — | 0.50 | — | BELOW FLOOR |
| 46 | activity | EXTRA | `h3>a` | `—` | `a` | 3 | 3 | 1.00 of 76 | — | structure | — | BELOW FLOOR |
| 47 | activity | MISSING | `div.col-12` | `div.hint` | `—` | 3 | 3 | 0.14 of 76 | — | structure | yes | BELOW FLOOR |
| 48 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `h3` | 3 | 3 | 0.35 of 76 | — | structure | yes | BELOW FLOOR |
| 49 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.dropbox[number=*]` | `p` | 3 | 3 | 0.12 of 76 | — | structure | yes | BELOW FLOOR |
| 50 | activity | SUBSTITUTED | `div.row` | `div.col-md-12` | `div.col-12` | 14 | 2 | 0.26 of 76 | — | structure | yes | BELOW FLOOR |
| 51 | activity | MISSING | `div.col-12` | `h3` | `—` | 5 | 2 | 0.24 of 76 | — | 0.80 | — | BELOW FLOOR |
| 52 | activity | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `div.col-12` | 4 | 2 | 0.09 of 76 | — | structure | — | BELOW FLOOR |
| 53 | activity | EXTRA | `div.col-12` | `—` | `h4.goJournal` | 3 | 2 | 1.00 of 76 | — | structure | — | BELOW FLOOR |
| 54 | activity | MISSING | `div.col-12` | `div.icon.ratio.ratio-16x9.videoSection` | `—` | 3 | 2 | 0.09 of 76 | — | structure | yes | BELOW FLOOR |
| 55 | activity | SUBSTITUTED | `div.activity[number=*]` | `div.row` | `li` | 3 | 2 | 0.49 of 76 | — | structure | yes | BELOW FLOOR |
| 56 | activity | EXTRA | `div.col-12` | `—` | `h3` | 2 | 2 | 0.41 of 76 | — | structure | — | BELOW FLOOR |
| 57 | activity | EXTRA | `ul` | `—` | `li` | 2 | 2 | 1.00 of 76 | — | structure | — | BELOW FLOOR |
| 58 | activity | EXTRA | `div.activity[number=*]` | `—` | `div.row` | 2 | 2 | 0.96 of 76 | — | structure | yes | BELOW FLOOR |
| 59 | activity | EXTRA | `div.col-12` | `—` | `p>b` | 2 | 2 | 0.99 of 76 | — | structure | — | BELOW FLOOR |
| 60 | activity | EXTRA | `div.activity.interactive[number=*]` | `—` | `div.row` | 2 | 2 | 0.80 of 76 | — | structure | yes | BELOW FLOOR |
| 61 | activity | EXTRA | `div.col-12` | `—` | `img.img-fluid` | 2 | 2 | 1.00 of 76 | — | structure | — | BELOW FLOOR |
| 62 | activity | MISSING | `div.col-md-12` | `h3` | `—` | 2 | 2 | 0.18 of 76 | — | 0.50 | yes | BELOW FLOOR |
| 63 | activity | MISSING | `div.col-12` | `ol` | `—` | 2 | 2 | 0.03 of 76 | — | 0.00 | — | BELOW FLOOR |
| 64 | activity | MISSING | `div.activity.alertPadding[number=*]` | `div.row` | `—` | 2 | 2 | 0.07 of 76 | — | 0.50 | yes | BELOW FLOOR |
| 65 | activity | MISSING | `div.col-12` | `h5` | `—` | 2 | 2 | 0.01 of 76 | — | 0.33 | — | BELOW FLOOR |
| 66 | activity | MISSING | `div.col-12` | `div.clickDropContent` | `—` | 2 | 2 | 0.05 of 76 | — | 0.50 | — | BELOW FLOOR |
| 67 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `ul` | 2 | 2 | 0.28 of 76 | — | structure | — | BELOW FLOOR |
| 68 | activity | SUBSTITUTED | `div.row` | `div.col-12.col-md-12` | `div.col-12` | 2 | 2 | 0.10 of 76 | — | structure | yes | BELOW FLOOR |
| 69 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.alertPadding[number=*]` | `div.activity[number=*]` | 2 | 2 | 0.07 of 76 | — | structure | yes | BELOW FLOOR |
| 70 | activity | SUBSTITUTED | `a` | `div.button` | `div.button` | 2 | 2 | 0.68 of 76 | — | structure | yes | BELOW FLOOR |
| 71 | activity | MISSING | `div.col-md-12` | `p` | `—` | 5 | 1 | 0.07 of 76 | — | 1.00 | yes | BELOW FLOOR |
| 72 | activity | MISSING | `div.col-md-12` | `WIDGET` | `—` | 4 | 1 | 0.05 of 76 | — | structure | yes | BELOW FLOOR |
| 73 | activity | SUBSTITUTED | `div.col-md-12` | `h3` | `ol` | 3 | 1 | 0.26 of 76 | — | structure | yes | BELOW FLOOR |
| 74 | activity | SUBSTITUTED | `div.col-12` | `p` | `ol` | 3 | 1 | 0.66 of 76 | — | structure | — | BELOW FLOOR |
| 75 | activity | EXTRA | `p>b` | `—` | `b` | 2 | 1 | 0.97 of 76 | — | structure | — | BELOW FLOOR |
| 76 | activity | MISSING | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `—` | 2 | 1 | 0.09 of 76 | — | 0.50 | yes | BELOW FLOOR |
| 77 | activity | MISSING | `div.icon.ratio.ratio-16x9.videoSection` | `iframe.embed-responsive-item` | `—` | 2 | 1 | 0.08 of 76 | — | structure | yes | BELOW FLOOR |
| 78 | activity | MISSING | `div.col-12.col-md-8` | `p>a` | `—` | 2 | 1 | 0.03 of 76 | — | 1.00 | — | BELOW FLOOR |
| 79 | activity | MISSING | `div.col-12.col-md-8` | `h3` | `—` | 2 | 1 | 0.08 of 76 | — | 1.00 | — | BELOW FLOOR |
| 80 | activity | SUBSTITUTED | `div.col-11` | `div.activity.interactive[number=*]` | `div.activity[number=*]` | 2 | 1 | 0.04 of 76 | — | structure | yes | BELOW FLOOR |
| 81 | activity | SUBSTITUTED | `div.col-12` | `div.icon.ratio.ratio-16x9.videoSection` | `h4.goJournal` | 2 | 1 | 0.09 of 76 | — | structure | yes | BELOW FLOOR |
| 82 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `h3` | `WIDGET` | 2 | 1 | 0.08 of 76 | — | structure | — | BELOW FLOOR |
| 83 | activity | EXTRA | `ol` | `—` | `li>b` | 1 | 1 | 1.00 of 76 | — | structure | — | BELOW FLOOR |
| 84 | activity | EXTRA | `div.col-12.col-md-8` | `—` | `div.activity[number=*]` | 1 | 1 | 0.84 of 76 | — | structure | yes | BELOW FLOOR |
| 85 | activity | EXTRA | `div.col-12` | `—` | `div.icon.ratio.ratio-16x9.videoSection` | 1 | 1 | 0.91 of 76 | — | structure | yes | BELOW FLOOR |
| 86 | activity | EXTRA | `div.col-12.col-md-8` | `—` | `div.activity.interactive[number=*]` | 1 | 1 | 0.65 of 76 | — | structure | yes | BELOW FLOOR |
| 87 | activity | EXTRA | `div.col-12` | `—` | `p>a` | 1 | 1 | 1.00 of 76 | — | structure | — | BELOW FLOOR |
| 88 | activity | EXTRA | `li` | `—` | `b` | 1 | 1 | 1.00 of 76 | — | structure | — | BELOW FLOOR |
| 89 | activity | MISSING | `div.row` | `div.col-12.col-md-8` | `—` | 1 | 1 | 0.09 of 76 | — | 1.00 | — | BELOW FLOOR |
| 90 | activity | MISSING | `div.row` | `div.col-md-12` | `—` | 1 | 1 | 0.18 of 76 | — | 1.00 | yes | BELOW FLOOR |
| 91 | activity | MISSING | `div.col-md-12` | `div.hint` | `—` | 1 | 1 | 0.03 of 76 | — | structure | yes | BELOW FLOOR |
| 92 | activity | MISSING | `div.col-md-12` | `div.row` | `—` | 1 | 1 | 0.03 of 76 | — | structure | yes | BELOW FLOOR |
| 93 | activity | MISSING | `div.col-12.col-md-12` | `p` | `—` | 1 | 1 | 0.01 of 76 | — | 0.50 | yes | BELOW FLOOR |
| 94 | activity | MISSING | `div.col-12.col-md-12` | `WIDGET` | `—` | 1 | 1 | 0.03 of 76 | — | structure | yes | BELOW FLOOR |
| 95 | activity | MISSING | `div.col-12` | `p>b` | `—` | 1 | 1 | 0.01 of 76 | — | 0.00 | — | BELOW FLOOR |
| 96 | activity | MISSING | `div.col-12` | `div.activity.interactive[number=*]` | `—` | 1 | 1 | 0.01 of 76 | — | 1.00 | yes | BELOW FLOOR |
| 97 | activity | MISSING | `div.row` | `WIDGET` | `—` | 1 | 1 | 0.01 of 76 | — | structure | — | BELOW FLOOR |
| 98 | activity | MISSING | `div.row` | `div.clickDropContent` | `—` | 1 | 1 | 0.01 of 76 | — | 1.00 | — | BELOW FLOOR |
| 99 | activity | MISSING | `div.col-12.col-md-12` | `img.img-fluid` | `—` | 1 | 1 | 0.01 of 76 | — | structure | yes | BELOW FLOOR |
| 100 | activity | MISSING | `h3` | `br` | `—` | 1 | 1 | 0.01 of 76 | — | structure | — | BELOW FLOOR |
| 145 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 43 | 7 | 0.75 of 76 | template=Standard c=0.75 n=43 | structure | — | CANDIDATE |
| 147 | body | SUBSTITUTED | `div.icon.ratio.ratio-16x9.videoSection` | `iframe.embed-responsive-item` | `iframe` | 37 | 7 | 0.67 of 76 | template=Standard c=0.67 n=37 | structure | yes | CANDIDATE |
| 148 | body | EXTRA | `div#body` | `—` | `div.row` | 30 | 7 | 0.70 of 76 | template=Standard c=0.70 n=30 | structure | — | CANDIDATE |
| 151 | body | EXTRA | `div.col-12.col-md-8` | `—` | `ul` | 31 | 6 | 0.80 of 76 | ptype=lesson c=0.83 n=28 | structure | — | CANDIDATE |

## Details — in the companion file `CONVERTER_V2/outputs/_s51_PES_miner_details.md`
Every CANDIDATE and every top-40 row has three quoted examples (WT / gold / Claude) there, plus the
below-floor list. **NEVER read the companion whole** (hundreds of KB): `grep -n '^### #<rank> ' CONVERTER_V2/outputs/_diff_queue_details.md` then `sed -n '<start>,<start+40>p'`. The top 25
candidates' detail blocks are repeated below for convenience.

### #145 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `p` — CANDIDATE
- pages 43 / modules 7 / lines 97; consensus (all) 0.75 of 76 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 7m/43p c=0.75
- by subject: NCEA1 7m/43p c=0.75
- by era: Refresh 7m/43p c=0.75
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **PES1001** PES1001_0_0.html ↔ PES1001_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «The spheres of the Earth System interact with each other, and affect living things, landforms and the climate. At the sa»`
- **PES1002** PES1002_0_0.html ↔ PES1002_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «What we do matters. Human activity has big impacts on the Earth system. The bad news is that some of these impacts are r»`
- **PES1003** PES1003_4_0.html ↔ PES1003_4.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «All materials conduct heat, but some substances conduct heat more easily than others. The denser the material, the close»`
- modules: PES1001, PES1002, PES1003, PES1004, PES1005, PES1007, PES1008

### #147 · body · SUBSTITUTED · `div.icon.ratio.ratio-16x9.videoSection` › gold `iframe.embed-responsive-item` vs Claude `iframe` — CANDIDATE
- pages 37 / modules 7 / lines 51; consensus (all) 0.67 of 76 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 7m/37p c=0.67
- by subject: NCEA1 7m/37p c=0.67
- by era: Refresh 7m/37p c=0.67
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:43 — | Video wrapper | `embed-responsive embed-responsive-16by9` | `ratio ratio-16x9` |
  - KB: 06_TEMPLATE_RECOGNITION.md:376 — <div class="videoSection ratio ratio-16x9">
  - KB: INDEX.md:168 — - **`14_SUBJECT_GLOBAL_PARAMETERS/14D_SGP_CROSSCUTTING_AND_TECHNOLOGY.md`** (6 KB) — Cross-cutting notes (14.11) and the Technology family (14.12 — fi
- **PES1001** PES1001_1_0.html ↔ PES1001_1.0.html (structure, derivable=True)
  - gold: `iframe.embed-responsive-item`
  - Claude: `iframe`
- **PES1002** PES1002_0_0.html ↔ PES1002_0.0.html (structure, derivable=True)
  - gold: `iframe.embed-responsive-item`
  - Claude: `iframe`
- **PES1003** PES1003_2_0.html ↔ PES1003_2.0.html (structure, derivable=True)
  - gold: `iframe.embed-responsive-item`
  - Claude: `iframe`
- modules: PES1001, PES1002, PES1003, PES1004, PES1005, PES1007, PES1008

### #148 · body · EXTRA · `div#body` › gold `—` vs Claude `div.row` — CANDIDATE
- pages 30 / modules 7 / lines 69; consensus (all) 0.70 of 76 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 7m/30p c=0.70
- by subject: NCEA1 7m/30p c=0.70
- by era: Refresh 7m/30p c=0.70
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **PES1001** PES1001_1_0.html ↔ PES1001_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row`
- **PES1002** PES1002_1_0.html ↔ PES1002_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «The impact of humans in Aotearoa New Zealand»`
- **PES1003** PES1003_2_0.html ↔ PES1003_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «measuring temperature of snow – or something similar»`
- modules: PES1001, PES1002, PES1003, PES1004, PES1005, PES1007, PES1008

### #151 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `ul` — CANDIDATE
- pages 31 / modules 6 / lines 39; consensus (all) 0.80 of 76 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 6m/31p c=0.80
- by subject: NCEA1 6m/31p c=0.80
- by era: Refresh 6m/31p c=0.80
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **PES1001** PES1001_0_0.html ↔ PES1001_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul  «The Geosphere – the solid Earth, rocks, and structure of the Earth»`
- **PES1003** PES1003_1_0.html ↔ PES1003_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul  «Learning outcome/intentions for the lesson.»`
- **PES1004** PES1004_0_0.html ↔ PES1004_00.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul  «interpreting data (using: tables, graphs and calculations)»`
- modules: PES1001, PES1003, PES1004, PES1005, PES1007, PES1008
