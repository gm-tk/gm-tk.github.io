# DIFF_QUEUE.md — the diff miner's ranked class queue (LOOP__Autonomous_Rounds.md §1d)

**Produced:** 2026-09-24 16:23 NZST by `reference/tests/_diff_miner.py` on the CURRENT corpus (pageforge-site HEAD 68a9ac9; Claude corpus 545 dirs). **Population:** the skeleton gate's own — 150 paired pages / 55 modules (compare_exclusions.txt honoured; acks / glossary / references pages excluded); parse errors skipped: 0 (must be 0); modules without a parsed WT: 0. Run time 9.4 s.

**What a row is.** One CLASS = (region, parent element, gold form, Claude form, direction) over every differing skeleton line of every paired page — the same lines, labels, widget collapse and difflib alignment the PRIMARY gate scores (each element its own line so it can be quoted). Direction: MISSING = gold has it, Claude lacks it; EXTRA = Claude has it, gold lacks it; SUBSTITUTED = same position, different tag / class / wrapper; MOVED = same text, different place. Consensus = of the gold pages in the group where the region exists, the share carrying the gold form (for EXTRA: the share NOT carrying Claude's form). Derivable = the gold line's text is in the module's parsed Writers Template (round-110 tolerance); structure-only differences are always derivable.

**Candidate rule (§1d).** modules ≥ 10 for a chrome class (module-code / title / header / module-menu / crumbs / phases-nav / footer / acks), pages ≥ 20 for a body / activity class; gold consensus ≥ 0.60 in at least one template or subject group that itself reaches the floor; structure-only or derivable share ≥ 0.60. A class below the floor is listed, never dropped. A CANDIDATE still goes through the PICK's KB-first check, the triangulation and the §3 corpus-wide measurement before any code — this table is the queue, not the verdict.

## Summary

- differing skeleton lines: 14942 — by direction {'SUBSTITUTED': 1952, 'MISSING': 8571, 'EXTRA': 4046, 'MOVED': 373}
- by region: {'module-code': 2, 'module-menu': 532, 'footer': 189, 'acks': 200, 'activity': 11157, 'body': 2659, 'root': 203}
- classes: 1081 — CANDIDATE 20, below floor 1049, the rest below consensus / not derivable

## Completeness census — the repeating chrome (§1d item 4)

| region | pages with region | gold items | gold items in WT | Claude items | derivable misses | pages with misses | modules with misses | status |
|---|---|---|---|---|---|---|---|---|
| module-menu | 55 | 1368 | 1252 | 1383 | 101 | 31 | 31 | CANDIDATE (verify by eye — text presence, not position) |
| crumbs | 7 | 50 | 50 | 50 | 3 | 3 | 3 | BELOW FLOOR |
| phases-nav | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |
| footer | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |

- **module-menu** by template: Inquiry 6m/6p/9 misses; Standard 25m/25p/92 misses
  - BLL124 BLL124_0_0.html: gold 23 items (21 in WT) / Claude 2 — 21 derivable misses, e.g. h4 «Learning Intentions» · span «Learning Intentions»
  - BLL122 BLL122_0_0.html: gold 27 items (17 in WT) / Claude 20 — 7 derivable misses, e.g. h5 «Know:» · span «Know:»
  - BLL123 BLL123_0_0.html: gold 23 items (17 in WT) / Claude 23 — 6 derivable misses, e.g. h5 «Understand:» · span «Understand:»
  - BLL114 BLL114_0_0.html: gold 27 items (19 in WT) / Claude 16 — 5 derivable misses, e.g. h5 «Do:» · span «Do:»
- **crumbs** by template: Inquiry 3m/3p/3 misses
  - BLL120 BLL120_0_0.html: gold 9 items (9 in WT) / Claude 9 — 1 derivable misses, e.g. p «The letters ck»
  - BLL160 BLL160_0_0.html: gold 6 items (6 in WT) / Claude 6 — 1 derivable misses, e.g. p «Letter team sh»
  - BLL170 BLL170_0_0.html: gold 7 items (7 in WT) / Claude 7 — 1 derivable misses, e.g. p «Letter team 'ue'»
- **phases-nav** by template: 
- **footer** by template: 

## Chrome facts — the header and footer as SETS per page (alignment-free; §1d items 2 + 4)

A fact is one thing a page's chrome has: `header:chip` (the `#module-code` div), `header:chip=module-code` / `=lesson-number` / `=lesson-number(00)`, `header:head-buttons`, `header:menu-content`, `header:title-h1-count=N`, `footer:present`, `footer:ul=<classes>`, `footer:link=prev-lesson` / `next-lesson` / `home-nav`, `footer:links=<order>`, `footer:inside-body`, `nav:crumbs`, `nav:phases`. MISSING = the gold page has the fact and Claude's does not; EXTRA the reverse. Consensus = the share of gold pages in the group that have (MISSING) / lack (EXTRA) the fact. Floor 10 modules.

| # | dir | fact | pages | modules | gold share (all) | consensus (all) | best group | status |
|---|---|---|---|---|---|---|---|---|
| F1 | MISSING | `header:chip=module-code` | 6 | 6 | 0.04 | 0.04 | — | BELOW FLOOR |
| F2 | EXTRA | `header:chip=other` | 5 | 5 | 0.29 | 0.71 | — | BELOW FLOOR |
| F3 | MISSING | `header:head-buttons` | 6 | 3 | 0.41 | 0.41 | — | BELOW FLOOR |
| F4 | MISSING | `header:chip=decimal-number` | 6 | 3 | 0.29 | 0.29 | — | BELOW FLOOR |
| F5 | EXTRA | `header:chip=lesson-number` | 6 | 3 | 0.34 | 0.66 | — | BELOW FLOOR |
| F6 | MISSING | `header:chip=lesson-number` | 2 | 1 | 0.34 | 0.34 | — | BELOW FLOOR |
| F7 | EXTRA | `header:chip=decimal-number` | 2 | 1 | 0.29 | 0.71 | — | BELOW FLOOR |
| F8 | MISSING | `header:chip` | 1 | 1 | 0.96 | 0.96 | — | BELOW FLOOR |
| F9 | MISSING | `header:chip=other` | 1 | 1 | 0.29 | 0.29 | — | BELOW FLOOR |
| F10 | EXTRA | `header:chip=lesson-number(00)` | 1 | 1 | 0.00 | 1.00 | — | BELOW FLOOR |
| F11 | MISSING | `footer:inside-body` | 17 | 15 | 0.11 | 0.11 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F12 | MISSING | `footer:link=next-lesson` | 8 | 8 | 0.72 | 0.72 | — | BELOW FLOOR |
| F13 | EXTRA | `footer:links=prev-lesson,home-nav` | 8 | 8 | 0.26 | 0.74 | — | BELOW FLOOR |
| F14 | MISSING | `footer:ul=footer-nav` | 18 | 6 | 0.12 | 0.12 | — | BELOW FLOOR |
| F15 | EXTRA | `footer:ul=footer-nav inquiry-nav` | 18 | 6 | 0.88 | 0.12 | — | BELOW FLOOR |
| F16 | EXTRA | `footer:link=prev-lesson` | 6 | 6 | 0.64 | 0.36 | — | BELOW FLOOR |
| F17 | MISSING | `footer:links=home-nav,next-lesson` | 6 | 6 | 0.04 | 0.04 | — | BELOW FLOOR |
| F18 | EXTRA | `footer:links=next-lesson,home-nav` | 6 | 6 | 0.30 | 0.70 | — | BELOW FLOOR |
| F19 | MISSING | `footer:links=prev-lesson,next-lesson,home-nav` | 6 | 6 | 0.37 | 0.37 | — | BELOW FLOOR |
| F20 | EXTRA | `footer:links=prev-lesson,next-lesson,home-nav` | 5 | 5 | 0.37 | 0.63 | — | BELOW FLOOR |
| F21 | MISSING | `footer:links=home-nav` | 3 | 3 | 0.02 | 0.02 | — | BELOW FLOOR |
| F22 | EXTRA | `footer:link=next-lesson` | 3 | 3 | 0.72 | 0.28 | — | BELOW FLOOR |
| F23 | MISSING | `footer:links=next-lesson,home-nav` | 3 | 3 | 0.30 | 0.30 | — | BELOW FLOOR |
| F24 | MISSING | `footer:links=home-nav,prev-lesson,next-lesson` | 1 | 1 | 0.01 | 0.01 | — | BELOW FLOOR |


## The ranked queue — chrome regions first, then by modules affected

| # | region | dir | parent | gold form | Claude form | pages | modules | consensus (all) | best group | derivable | KB | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | module-code | MISSING | `div#header` | `div#module-code` | `—` | 1 | 1 | 0.96 of 150 | — | structure | yes | BELOW FLOOR |
| 2 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `p` | `h5` | 43 | 43 | 0.33 of 150 | ptype=overview c=0.91 n=43 | structure | yes | CANDIDATE |
| 3 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `p` | `—` | 21 | 21 | 0.32 of 150 | template+ptype=Standard/overview c=0.90 n=18 | 0.43 | yes | NOT DERIVABLE (content share < 0.60) |
| 4 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `p>b` | 20 | 20 | 0.99 of 150 | era=Refresh c=0.99 n=20 | structure | yes | CANDIDATE |
| 5 | module-menu | MISSING | `ul` | `li` | `—` | 18 | 18 | 0.22 of 150 | template+ptype=Standard/overview c=0.62 n=14 | 0.93 | — | CANDIDATE |
| 6 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `ul` | `p>b` | 14 | 14 | 0.33 of 150 | ptype=overview c=0.89 n=14 | structure | yes | CANDIDATE |
| 7 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-6.paddingR` | 11 | 11 | 0.69 of 150 | era=Refresh c=0.69 n=11 | structure | yes | CANDIDATE |
| 8 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-12.paddingR` | 10 | 10 | 0.79 of 150 | template=Standard c=0.80 n=10 | structure | yes | CANDIDATE |
| 9 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `h5>span` | `—` | 9 | 9 | 0.27 of 150 | — | 1.00 | yes | BELOW FLOOR |
| 10 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `h4>span` | `h5>span` | 9 | 9 | 0.06 of 150 | — | structure | yes | BELOW FLOOR |
| 11 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `ul` | `—` | 8 | 8 | 0.23 of 150 | — | 0.44 | yes | BELOW FLOOR |
| 12 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.paddingR` | `div.col-12.col-md-12.paddingR` | 8 | 8 | 0.33 of 150 | — | structure | yes | BELOW FLOOR |
| 13 | module-menu | EXTRA | `ul` | `—` | `li` | 7 | 7 | 0.89 of 150 | — | structure | — | BELOW FLOOR |
| 14 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `p` | 6 | 6 | 0.67 of 150 | — | structure | yes | BELOW FLOOR |
| 15 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `h5>span` | 5 | 5 | 0.73 of 150 | — | structure | yes | BELOW FLOOR |
| 16 | module-menu | MISSING | `p` | `br` | `—` | 5 | 5 | 0.05 of 150 | — | structure | — | BELOW FLOOR |
| 17 | module-menu | SUBSTITUTED | `div.col-12.col-md-6` | `h4>span` | `h5>span` | 5 | 5 | 0.04 of 150 | — | structure | yes | BELOW FLOOR |
| 18 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.paddingL` | `div.col-12.col-md-6.paddingR` | 5 | 5 | 0.03 of 150 | — | structure | yes | BELOW FLOOR |
| 19 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingL` | `p` | `h5` | 5 | 5 | 0.03 of 150 | — | structure | yes | BELOW FLOOR |
| 20 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `h4>span` | `—` | 4 | 4 | 0.05 of 150 | — | 1.00 | yes | BELOW FLOOR |
| 21 | module-menu | MISSING | `div.col-12.col-md-6` | `h4>span` | `—` | 4 | 4 | 0.04 of 150 | — | 1.00 | yes | BELOW FLOOR |
| 22 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-12` | `div.col-12.col-md-12.paddingR` | 4 | 4 | 0.03 of 150 | — | structure | yes | BELOW FLOOR |
| 23 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6` | `div.col-12.col-md-6.paddingR` | 4 | 4 | 0.05 of 150 | — | structure | yes | BELOW FLOOR |
| 24 | module-menu | SUBSTITUTED | `div.col-12.col-md-6` | `p` | `h5>span` | 4 | 4 | 0.05 of 150 | — | structure | yes | BELOW FLOOR |
| 25 | module-menu | MISSING | `div#header` | `div#module-head-buttons` | `—` | 6 | 3 | 0.41 of 150 | — | structure | yes | BELOW FLOOR |
| 26 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `h5` | 3 | 3 | 1.00 of 150 | — | structure | yes | BELOW FLOOR |
| 27 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6` | `—` | 3 | 3 | 0.05 of 150 | — | 1.00 | yes | BELOW FLOOR |
| 28 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6.paddingR` | `—` | 2 | 2 | 0.31 of 150 | — | 1.00 | yes | BELOW FLOOR |
| 29 | module-menu | SUBSTITUTED | `div.col-12.col-md-6` | `p` | `h5` | 2 | 2 | 0.05 of 150 | — | structure | yes | BELOW FLOOR |
| 30 | module-menu | SUBSTITUTED | `ul` | `p` | `li` | 2 | 2 | 0.01 of 150 | — | structure | — | BELOW FLOOR |
| 31 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `ul` | `p` | 2 | 2 | 0.33 of 150 | — | structure | yes | BELOW FLOOR |
| 32 | module-menu | EXTRA | `p>b` | `—` | `b` | 1 | 1 | 0.99 of 150 | — | structure | — | BELOW FLOOR |
| 33 | module-menu | EXTRA | `div.col-12.col-md-12.paddingR` | `—` | `h4>span` | 1 | 1 | 0.79 of 150 | — | structure | yes | BELOW FLOOR |
| 34 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `p>b` | `—` | 1 | 1 | 0.01 of 150 | — | 0.00 | yes | BELOW FLOOR |
| 35 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `h5` | `—` | 1 | 1 | 0.31 of 150 | — | 1.00 | yes | BELOW FLOOR |
| 36 | module-menu | MISSING | `ul` | `li>b` | `—` | 1 | 1 | 0.01 of 150 | — | 1.00 | — | BELOW FLOOR |
| 37 | module-menu | MISSING | `div.col-12.col-md-6` | `p` | `—` | 1 | 1 | 0.05 of 150 | — | 1.00 | yes | BELOW FLOOR |
| 38 | module-menu | MOVED | `ul` | `li` | `li>i` | 1 | 1 | 0.34 of 150 | — | structure | — | BELOW FLOOR |
| 39 | module-menu | SUBSTITUTED | `p` | `ul` | `b` | 1 | 1 | 0.01 of 150 | — | structure | — | BELOW FLOOR |
| 40 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `p` | `h5>span` | 1 | 1 | 0.33 of 150 | — | structure | yes | BELOW FLOOR |
| 41 | module-menu | SUBSTITUTED | `p` | `br` | `b` | 1 | 1 | 0.05 of 150 | — | structure | — | BELOW FLOOR |
| 42 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `p` | `ul` | 1 | 1 | 0.33 of 150 | — | structure | yes | BELOW FLOOR |
| 43 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6` | `div.col-12.col-md-12.paddingR` | 1 | 1 | 0.05 of 150 | — | structure | yes | BELOW FLOOR |
| 44 | footer | EXTRA | `body.container-fluid` | `—` | `div#footer` | 11 | 11 | 0.17 of 150 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 45 | footer | MISSING | `ul.footer-nav.inquiry-nav` | `li>a.home-nav` | `—` | 11 | 10 | 0.88 of 150 | era=Refresh c=0.88 n=10 | structure | yes | CANDIDATE |
| 46 | footer | MISSING | `div#body` | `div#footer` | `—` | 8 | 8 | 0.11 of 150 | — | structure | yes | BELOW FLOOR |
| 47 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav` | `ul.footer-nav.inquiry-nav` | 18 | 6 | 0.12 of 150 | — | structure | yes | BELOW FLOOR |
| 48 | footer | EXTRA | `ul.footer-nav.inquiry-nav` | `—` | `li>a#next-lesson` | 6 | 6 | 0.38 of 150 | — | structure | yes | BELOW FLOOR |
| 49 | footer | MISSING | `li>a#next-lesson` | `a#next-lesson` | `—` | 6 | 6 | 0.72 of 150 | — | structure | yes | BELOW FLOOR |
| 50 | footer | EXTRA | `div#footer` | `—` | `ul.footer-nav.inquiry-nav` | 5 | 5 | 0.12 of 150 | — | structure | yes | BELOW FLOOR |
| 51 | footer | MISSING | `ul.footer-nav` | `li>a#next-lesson` | `—` | 4 | 4 | 0.10 of 150 | — | structure | yes | BELOW FLOOR |
| 52 | footer | SUBSTITUTED | `div#body` | `div#footer` | `ul.footer-nav.inquiry-nav` | 4 | 4 | 0.11 of 150 | — | structure | yes | BELOW FLOOR |
| 53 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav.inquiry-nav` | `li>a#next-lesson` | 4 | 4 | 0.88 of 150 | — | structure | yes | BELOW FLOOR |
| 54 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` | `li>a#next-lesson` | `li>a.home-nav` | 4 | 4 | 0.62 of 150 | — | structure | yes | BELOW FLOOR |
| 55 | footer | EXTRA | `ul.footer-nav.inquiry-nav` | `—` | `li>a#prev-lesson` | 3 | 3 | 0.42 of 150 | — | structure | yes | BELOW FLOOR |
| 56 | footer | EXTRA | `ul.footer-nav.inquiry-nav` | `—` | `li>a.home-nav` | 3 | 3 | 0.12 of 150 | — | structure | yes | BELOW FLOOR |
| 57 | footer | SUBSTITUTED | `div#body` | `div#footer` | `div#footer` | 3 | 3 | 0.11 of 150 | — | structure | yes | BELOW FLOOR |
| 58 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav.inquiry-nav` | `ul.footer-nav.inquiry-nav` | 3 | 3 | 0.88 of 150 | — | structure | yes | BELOW FLOOR |
| 59 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` | `li>a.home-nav` | `li>a.home-nav` | 3 | 3 | 0.88 of 150 | — | structure | yes | BELOW FLOOR |
| 60 | footer | EXTRA | `li>a#next-lesson` | `—` | `a#next-lesson` | 2 | 2 | 0.28 of 150 | — | structure | yes | BELOW FLOOR |
| 61 | footer | MISSING | `ul.footer-nav.inquiry-nav` | `li>a#next-lesson` | `—` | 2 | 2 | 0.62 of 150 | — | structure | yes | BELOW FLOOR |
| 62 | footer | MISSING | `div.row` | `div#footer` | `—` | 2 | 2 | 0.01 of 150 | — | structure | yes | BELOW FLOOR |
| 63 | footer | MISSING | `div#footer` | `ul.footer-nav.inquiry-nav` | `—` | 2 | 2 | 0.88 of 150 | — | structure | yes | BELOW FLOOR |
| 64 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` | `li>a#next-lesson` | `li>a#next-lesson` | 2 | 2 | 0.62 of 150 | — | structure | yes | BELOW FLOOR |
| 65 | footer | SUBSTITUTED | `li>a#next-lesson` | `a#next-lesson` | `a#prev-lesson` | 2 | 2 | 0.72 of 150 | — | structure | yes | BELOW FLOOR |
| 66 | footer | SUBSTITUTED | `div#body` | `div#footer` | `div.icon.ratio.ratio-16x9.videoSection` | 1 | 1 | 0.11 of 150 | — | structure | yes | BELOW FLOOR |
| 67 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` | `li>a#prev-lesson` | `li>a#prev-lesson` | 1 | 1 | 0.58 of 150 | — | structure | yes | BELOW FLOOR |
| 68 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` | `li>a.home-nav` | `li>a#next-lesson` | 1 | 1 | 0.88 of 150 | — | structure | yes | BELOW FLOOR |
| 69 | footer | SUBSTITUTED | `div#body` | `div#footer` | `div.col-12.col-md-8` | 1 | 1 | 0.11 of 150 | — | structure | yes | BELOW FLOOR |
| 70 | acks | SUBSTITUTED | `div.col-12.col-md-8` | `div.acks` | `div.acks.acksTemplate` | 5 | 5 | 0.36 of 150 | — | structure | yes | BELOW FLOOR |
| 71 | acks | EXTRA | `div.col-12.col-md-8` | `—` | `div.acks.acksTemplate` | 1 | 1 | 1.00 of 150 | — | structure | yes | BELOW FLOOR |
| 72 | acks | SUBSTITUTED | `div.col-12.col-md-8` | `div.acks` | `p` | 1 | 1 | 0.36 of 150 | — | structure | yes | BELOW FLOOR |
| 73 | acks | SUBSTITUTED | `div.acks` | `WIDGET` | `div#footer` | 1 | 1 | 0.36 of 150 | — | structure | yes | BELOW FLOOR |
| 74 | acks | SUBSTITUTED | `div.col-12.col-md-8` | `div.acks` | `div.activity[number=*]` | 1 | 1 | 0.36 of 150 | — | structure | yes | BELOW FLOOR |
| 75 | acks | SUBSTITUTED | `div.acks` | `WIDGET` | `div.row` | 1 | 1 | 0.36 of 150 | — | structure | yes | BELOW FLOOR |
| 76 | activity | MISSING | `div.col-12` | `p` | `—` | 64 | 46 | 0.35 of 150 | — | 0.95 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 77 | activity | EXTRA | `div.col-12` | `—` | `p` | 58 | 40 | 0.81 of 150 | template=Standard c=0.85 n=51 | structure | — | CANDIDATE |
| 78 | activity | MISSING | `div.col-12` | `WIDGET` | `—` | 49 | 38 | 0.18 of 150 | — | structure | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 79 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `div.activity[number=*]` | 41 | 33 | 0.53 of 150 | ptype=lesson c=0.77 n=37 | structure | yes | CANDIDATE |
| 80 | activity | EXTRA | `div.row` | `—` | `div.col-12` | 38 | 31 | 0.89 of 150 | template=Standard c=0.94 n=32 | structure | — | CANDIDATE |
| 81 | activity | MISSING | `div.col-12` | `a` | `—` | 35 | 28 | 0.29 of 150 | — | 0.71 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 82 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.alertPadding[number=*]` | `div.activity[number=*]` | 26 | 25 | 0.20 of 150 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 83 | activity | MISSING | `div.col-12` | `div.row` | `—` | 25 | 23 | 0.15 of 150 | — | 0.95 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 84 | activity | SUBSTITUTED | `div.col-12` | `div.table-responsive` | `WIDGET` | 24 | 23 | 0.23 of 150 | — | structure | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 85 | activity | EXTRA | `div.col-12` | `—` | `img.img-fluid` | 23 | 21 | 0.96 of 150 | era=Refresh c=0.96 n=23 | structure | — | CANDIDATE |
| 86 | activity | EXTRA | `div.col-12` | `—` | `WIDGET` | 20 | 19 | 0.77 of 150 | era=Refresh c=0.77 n=20 | structure | — | CANDIDATE |
| 87 | activity | MISSING | `a` | `div.buttonD` | `—` | 20 | 17 | 0.35 of 150 | — | 0.46 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 88 | activity | EXTRA | `div.col-12` | `—` | `p>a` | 17 | 17 | 0.98 of 150 | — | structure | — | BELOW FLOOR |
| 89 | activity | SUBSTITUTED | `div.icon.ratio.ratio-16x9.videoSection` | `iframe.embed-responsive-item` | `iframe` | 20 | 16 | 0.18 of 150 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 90 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `div.activity.interactive[number=*]` | 20 | 16 | 0.60 of 150 | ptype=lesson c=0.87 n=20 | structure | yes | CANDIDATE |
| 91 | activity | EXTRA | `p>i` | `—` | `i` | 19 | 16 | 0.61 of 150 | — | structure | — | BELOW FLOOR |
| 92 | activity | MOVED | `div.col-12` | `h3` | `h3` | 19 | 16 | 0.17 of 150 | — | structure | — | BELOW FLOOR |
| 93 | activity | MISSING | `div.col-12` | `img.img-fluid` | `—` | 18 | 16 | 0.07 of 150 | — | structure | — | BELOW FLOOR |
| 94 | activity | MOVED | `div.col-12` | `p` | `p` | 17 | 16 | 0.26 of 150 | — | structure | — | BELOW FLOOR |
| 95 | activity | EXTRA | `div.col-12` | `—` | `h3` | 16 | 15 | 0.91 of 150 | — | structure | — | BELOW FLOOR |
| 96 | activity | SUBSTITUTED | `div.col-12` | `div.row` | `WIDGET` | 16 | 15 | 0.35 of 150 | — | structure | — | BELOW FLOOR |
| 97 | activity | EXTRA | `div.col-12` | `—` | `p>b` | 16 | 14 | 0.95 of 150 | — | structure | — | BELOW FLOOR |
| 98 | activity | EXTRA | `div.col-12` | `—` | `ul` | 14 | 14 | 0.94 of 150 | — | structure | — | BELOW FLOOR |
| 99 | activity | MOVED | `a` | `div.buttonD` | `div.buttonD` | 14 | 13 | 0.35 of 150 | — | structure | — | BELOW FLOOR |
| 100 | activity | EXTRA | `div.col-12` | `—` | `a` | 13 | 13 | 0.71 of 150 | — | structure | — | BELOW FLOOR |
| 846 | body | SUBSTITUTED | `div.row` | `div.col-12` | `div.col-12.col-md-8` | 54 | 43 | 0.51 of 150 | template+ptype=Standard/overview c=1.00 n=38 | structure | — | CANDIDATE |
| 847 | body | EXTRA | `div#body` | `—` | `div.row` | 68 | 40 | 0.69 of 150 | ptype=overview c=1.00 n=22 | structure | — | CANDIDATE |
| 849 | body | EXTRA | `p>i` | `—` | `i` | 26 | 26 | 1.00 of 150 | template=Standard c=1.00 n=26 | structure | — | CANDIDATE |
| 850 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 21 | 21 | 0.97 of 150 | era=Refresh c=0.97 n=21 | structure | — | CANDIDATE |
| 851 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p>b` | 21 | 21 | 1.00 of 150 | era=Refresh c=1.00 n=21 | structure | — | CANDIDATE |
| 852 | body | EXTRA | `div.row` | `—` | `div.col-12.col-md-8` | 20 | 19 | 0.86 of 150 | era=Refresh c=0.86 n=20 | structure | — | CANDIDATE |
| 1073 | root | EXTRA | `body.container-fluid` | `—` | `div.row` | 48 | 48 | 0.72 of 150 | ptype=overview c=1.00 n=48 | structure | — | CANDIDATE |

## Details — in the companion file `CONVERTER_V2/outputs/_diff_queue_details.md`
Every CANDIDATE and every top-40 row has three quoted examples (WT / gold / Claude) there, plus the
below-floor list. **NEVER read the companion whole** (hundreds of KB): `grep -n '^### #<rank> ' CONVERTER_V2/outputs/_diff_queue_details.md` then `sed -n '<start>,<start+40>p'`. The top 25
candidates' detail blocks are repeated below for convenience.

### #2 · module-menu · SUBSTITUTED · `div.col-12.col-md-6.paddingR` › gold `p` vs Claude `h5` — CANDIDATE
- pages 43 / modules 43 / lines 85; consensus (all) 0.33 of 150 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 38m/38p c=0.30; Inquiry 5m/5p c=1.00
- by subject: 1-10 Blended Literacy 43m/43p c=0.33
- by era: Refresh 43m/43p c=0.33
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:160 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **BLL130** BLL130_0_0.html ↔ BLL130.html (structure, derivable=True)
  - gold: `p  «We are learning:»`
  - Claude: `h5  «Ākonga will:»`
- **BLL140** BLL140_0_0.html ↔ BLL140.html (structure, derivable=True)
  - gold: `p  «We are learning:»`
  - Claude: `h5  «We are learning:»`
- **BLL150** BLL150_0_0.html ↔ BLL150.html (structure, derivable=True)
  - gold: `p  «We are learning:»`
  - Claude: `h5  «We are learning:»`
- modules: BLL111, BLL112, BLL113, BLL114, BLL115, BLL116, BLL117, BLL121, BLL122, BLL123, BLL125, BLL126, BLL127, BLL130, BLL131, BLL132, BLL133, BLL134, BLL135, BLL136, BLL137, BLL140, BLL141, BLL142 …

### #4 · module-menu · EXTRA · `div.col-12.col-md-6.paddingR` › gold `—` vs Claude `p>b` — CANDIDATE
- pages 20 / modules 20 / lines 41; consensus (all) 0.99 of 150 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 17m/17p c=0.99; Inquiry 3m/3p c=1.00
- by subject: 1-10 Blended Literacy 20m/20p c=0.99
- by era: Refresh 20m/20p c=0.99
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:160 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **BLL130** BLL130_0_0.html ↔ BLL130.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «ākonga develop basic literacy capability to read fluently and accurately. They engage with a variety of written texts, d»`
- **BLL140** BLL140_0_0.html ↔ BLL140.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Ākonga develop basic literacy capability to read fluently and accurately. They engage with a variety of written texts, d»`
- **BLL150** BLL150_0_0.html ↔ BLL150.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Students develop basic literacy capability to read fluently and accurately. They engage with a variety of written texts,»`
- modules: BLL125, BLL126, BLL127, BLL130, BLL131, BLL132, BLL133, BLL136, BLL137, BLL140, BLL141, BLL143, BLL144, BLL145, BLL146, BLL147, BLL150, BLL151, BLL153, BLL154

### #5 · module-menu · MISSING · `ul` › gold `li` vs Claude `—` — CANDIDATE
- pages 18 / modules 18 / lines 58; consensus (all) 0.22 of 150 gold pages with the region; derivable 0.93 (4 lines with no WT source)
- by template: Standard 14m/14p c=0.21; Inquiry 4m/4p c=0.43
- by subject: 1-10 Blended Literacy 18m/18p c=0.22
- by era: Refresh 18m/18p c=0.22
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL110** BLL110_0_0.html ↔ BLL110.html (content, derivable=False)
  - gold: `li  «When reading aloud, ākonga use appropriate intonation and phrasing. They can use appropriate strategies when they are co»`
  - Claude: `—`
- **BLL130** BLL130_0_0.html ↔ BLL130.html (content, derivable=True)
  - gold: `li  «Ākonga can use their basic literacy capability and can read fluently and accurately. They engage with a variety of writt»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [H2] [/RED TEXT]🔴 **Understand:**  As ākonga  develop their literacy capabilities and knowledge of written texts, they come to understand how language works and that it follows shared code`
- **BLL140** BLL140_0_0.html ↔ BLL140.html (content, derivable=True)
  - gold: `li  «Ākonga can use their basic literacy capability and can read fluently and accurately. They engage with a variety of writt»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [H2] [/RED TEXT]🔴 **Understand:**  As ākonga develop their literacy capabilities and knowledge of written texts, they come to understand how language works and that it follows shared codes`
- modules: BLL110, BLL125, BLL126, BLL127, BLL130, BLL134, BLL136, BLL137, BLL140, BLL141, BLL143, BLL146, BLL147, BLL150, BLL151, BLL153, BLL154, BLL173

### #6 · module-menu · SUBSTITUTED · `div.col-12.col-md-6.paddingR` › gold `ul` vs Claude `p>b` — CANDIDATE
- pages 14 / modules 14 / lines 14; consensus (all) 0.33 of 150 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 12m/12p c=0.29; Inquiry 2m/2p c=1.00
- by subject: 1-10 Blended Literacy 14m/14p c=0.33
- by era: Refresh 14m/14p c=0.33
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:160 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **BLL140** BLL140_0_0.html ↔ BLL140.html (structure, derivable=True)
  - gold: `ul  «Ākonga can use their basic literacy capability and can read fluently and accurately. They engage with a variety of writt»`
  - Claude: `p  «Ākonga interpret texts by drawing on various elements and recognise different perspectives, sharing their own opinions a»`
- **BLL150** BLL150_0_0.html ↔ BLL150.html (structure, derivable=True)
  - gold: `ul  «Ākonga can use their basic literacy capability and can read fluently and accurately. They engage with a variety of writt»`
  - Claude: `p  «Students interpret texts by drawing on various elements and recognise different perspectives, sharing their own opinions»`
- **BLL125** BLL125_0_0.html ↔ BLL125-01.html (structure, derivable=True)
  - gold: `ul  «Ākonga can use their basic literacy capability and can read fluently and accurately. They engage with a variety of writt»`
  - Claude: `p  «Students interpret texts by drawing on various elements and recognise different perspectives, sharing their own opinions»`
- modules: BLL125, BLL126, BLL127, BLL136, BLL137, BLL140, BLL141, BLL143, BLL146, BLL147, BLL150, BLL151, BLL153, BLL154

### #7 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `div.col-12.col-md-6.paddingR` — CANDIDATE
- pages 11 / modules 11 / lines 15; consensus (all) 0.69 of 150 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 8m/8p c=0.71; Inquiry 3m/3p c=0.29
- by subject: 1-10 Blended Literacy 11m/11p c=0.69
- by era: Refresh 11m/11p c=0.69
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:160 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **BLL110** BLL110_0_0.html ↔ BLL110.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-6.paddingR  «Understand»`
- **BLL120** BLL120_0_0.html ↔ BLL120.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-6.paddingR  «Understand»`
- **BLL160** BLL160_0_0.html ↔ BLL160.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-6.paddingR  «Understand»`
- modules: BLL110, BLL111, BLL120, BLL121, BLL134, BLL135, BLL144, BLL152, BLL160, BLL161, BLL172

### #8 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `div.col-12.col-md-12.paddingR` — CANDIDATE
- pages 10 / modules 10 / lines 10; consensus (all) 0.79 of 150 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 10m/10p c=0.80
- by subject: 1-10 Blended Literacy 10m/10p c=0.79
- by era: Refresh 10m/10p c=0.79
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:160 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **BLL112** BLL112_0_0.html ↔ BLL112-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-12.paddingR  «Overview»`
- **BLL113** BLL113_0_0.html ↔ BLL113-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-12.paddingR  «Overview»`
- **BLL125** BLL125_0_0.html ↔ BLL125-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-12.paddingR  «Overview»`
- modules: BLL112, BLL113, BLL125, BLL141, BLL142, BLL143, BLL144, BLL162, BLL163, BLL166

### #45 · footer · MISSING · `ul.footer-nav.inquiry-nav` › gold `li>a.home-nav` vs Claude `—` — CANDIDATE
- pages 11 / modules 10 / lines 11; consensus (all) 0.88 of 150 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 9m/10p c=0.87; Inquiry 1m/1p c=1.00
- by subject: 1-10 Blended Literacy 10m/11p c=0.88
- by era: Refresh 10m/11p c=0.88
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:40 — | Footer tag | `<nav id="module-foot">` with `<button>` + FA icons | `<div id="footer">` with `<ul class="footer-nav">` |
  - KB: 06_TEMPLATE_RECOGNITION.md:64 — | Footer `<ul>` class | `footer-nav` | `footer-nav` | `footer-nav fundamentals-nav` | `footer-nav inquiry-nav` | `footer-nav` |
  - KB: 06_TEMPLATE_RECOGNITION.md:114 — **Footer:** `<ul class="footer-nav">` with prev + next + home links.
- **BLL170** BLL170_0_0.html ↔ BLL170.html (structure, derivable=True)
  - gold: `li`
  - Claude: `—`
- **BLL141** BLL141_2_0.html ↔ BLL141-2.0.html (structure, derivable=True)
  - gold: `li`
  - Claude: `—`
- **BLL146** BLL146_2_0.html ↔ BLL146-2.0.html (structure, derivable=True)
  - gold: `li`
  - Claude: `—`
- modules: BLL141, BLL146, BLL151, BLL154, BLL156, BLL157, BLL166, BLL167, BLL170, BLL171

### #77 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `p` — CANDIDATE
- pages 58 / modules 40 / lines 260; consensus (all) 0.81 of 150 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 33m/51p c=0.85; Inquiry 7m/7p c=0.00
- by subject: 1-10 Blended Literacy 40m/58p c=0.81
- by era: Refresh 40m/58p c=0.81
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL110** BLL110_0_0.html ↔ BLL110.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Here is a printable worksheet to practise writing the letter ‘a’. If you do not have a printer at home, you can use this»`
- **BLL120** BLL120_0_0.html ↔ BLL120.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «For more practice and tips watch the following video.»`
- **BLL130** BLL130_0_0.html ↔ BLL130.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Here is a printable worksheet to practise writing the letter ‘g’. If you do not have a printer at home, you can use this»`
- modules: BLL110, BLL111, BLL113, BLL114, BLL115, BLL116, BLL117, BLL120, BLL122, BLL123, BLL126, BLL130, BLL131, BLL132, BLL133, BLL134, BLL135, BLL137, BLL140, BLL141, BLL142, BLL144, BLL145, BLL146 …

### #79 · activity · SUBSTITUTED · `div.col-12.col-md-8` › gold `div.activity.interactive[number=*]` vs Claude `div.activity[number=*]` — CANDIDATE
- pages 41 / modules 33 / lines 52; consensus (all) 0.53 of 150 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 29m/37p c=0.51; Inquiry 4m/4p c=1.00
- by subject: 1-10 Blended Literacy 33m/41p c=0.53
- by era: Refresh 33m/41p c=0.53
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:46 — | Activity class | `content activity activity-bg` | `activity` |
  - KB: 06_TEMPLATE_RECOGNITION.md:181 — - TWHA902–904 use `choicePage` activity grids and dual titles + `whakatauki` — these are content patterns, safe to use if the new module needs them
  - KB: 06_TEMPLATE_RECOGNITION.md:265 — **The X-prefix test governs THIS CLASS ONLY.** The wider LS look-and-feel conventions of `14_SUBJECT_GLOBAL_PARAMETERS.md` § 14.6 — terminology and br
- **BLL110** BLL110_0_0.html ↔ BLL110.html (structure, derivable=True)
  - gold: `div.activity.interactive[number=4B]  «Sound guess ...»`
  - Claude: `div.activity[number=4B]  «Sound guess …»`
- **BLL120** BLL120_0_0.html ↔ BLL120.html (structure, derivable=True)
  - gold: `div.activity.interactive[number=1F]  «Look at each picture and say the word out loud and then break the word down into each sound. Click where you hear the /k»`
  - Claude: `div.activity[number=1F]  «Self check activity»`
- **BLL130** BLL130_0_0.html ↔ BLL130.html (structure, derivable=True)
  - gold: `div.activity.interactive[number=1F]  «Find the sound»`
  - Claude: `div.activity[number=1F]  «Find the sound»`
- modules: BLL110, BLL111, BLL115, BLL116, BLL117, BLL120, BLL121, BLL125, BLL126, BLL127, BLL130, BLL133, BLL135, BLL137, BLL141, BLL142, BLL144, BLL145, BLL146, BLL147, BLL150, BLL151, BLL153, BLL154 …

### #80 · activity · EXTRA · `div.row` › gold `—` vs Claude `div.col-12` — CANDIDATE
- pages 38 / modules 31 / lines 51; consensus (all) 0.89 of 150 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 25m/32p c=0.94; Inquiry 6m/6p c=0.00
- by subject: 1-10 Blended Literacy 31m/38p c=0.89
- by era: Refresh 31m/38p c=0.89
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL110** BLL110_0_0.html ↔ BLL110.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12  «Build the letter»`
- **BLL120** BLL120_0_0.html ↔ BLL120.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12  «Build the letter»`
- **BLL130** BLL130_0_0.html ↔ BLL130.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12  «Find the letter o»`
- modules: BLL110, BLL113, BLL114, BLL116, BLL117, BLL120, BLL121, BLL123, BLL125, BLL126, BLL130, BLL131, BLL134, BLL135, BLL136, BLL137, BLL140, BLL142, BLL143, BLL144, BLL146, BLL147, BLL150, BLL151 …

### #85 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `img.img-fluid` — CANDIDATE
- pages 23 / modules 21 / lines 100; consensus (all) 0.96 of 150 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 14m/16p c=0.99; Inquiry 7m/7p c=0.43
- by subject: 1-10 Blended Literacy 21m/23p c=0.96
- by era: Refresh 21m/23p c=0.96
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL110** BLL110_0_0.html ↔ BLL110.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- **BLL120** BLL120_0_0.html ↔ BLL120.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- **BLL130** BLL130_0_0.html ↔ BLL130.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- modules: BLL110, BLL116, BLL120, BLL130, BLL132, BLL134, BLL137, BLL140, BLL142, BLL145, BLL147, BLL150, BLL153, BLL160, BLL162, BLL163, BLL164, BLL170, BLL173, BLL174, BLL177

### #86 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `WIDGET` — CANDIDATE
- pages 20 / modules 19 / lines 45; consensus (all) 0.77 of 150 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 13m/14p c=0.80; Inquiry 6m/6p c=0.14
- by subject: 1-10 Blended Literacy 19m/20p c=0.77
- by era: Refresh 19m/20p c=0.77
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL110** BLL110_0_0.html ↔ BLL110.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **BLL120** BLL120_0_0.html ↔ BLL120.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **BLL130** BLL130_0_0.html ↔ BLL130.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- modules: BLL110, BLL111, BLL112, BLL114, BLL120, BLL127, BLL130, BLL132, BLL133, BLL137, BLL140, BLL141, BLL150, BLL156, BLL160, BLL164, BLL165, BLL172, BLL177

### #90 · activity · SUBSTITUTED · `div.col-12.col-md-8` › gold `div.activity[number=*]` vs Claude `div.activity.interactive[number=*]` — CANDIDATE
- pages 20 / modules 16 / lines 23; consensus (all) 0.60 of 150 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 16m/20p c=0.58
- by subject: 1-10 Blended Literacy 16m/20p c=0.60
- by era: Refresh 16m/20p c=0.60
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:46 — | Activity class | `content activity activity-bg` | `activity` |
  - KB: 06_TEMPLATE_RECOGNITION.md:181 — - TWHA902–904 use `choicePage` activity grids and dual titles + `whakatauki` — these are content patterns, safe to use if the new module needs them
  - KB: 06_TEMPLATE_RECOGNITION.md:265 — **The X-prefix test governs THIS CLASS ONLY.** The wider LS look-and-feel conventions of `14_SUBJECT_GLOBAL_PARAMETERS.md` § 14.6 — terminology and br
- **BLL115** BLL115_2_0.html ↔ BLL115-03.html (structure, derivable=True)
  - gold: `div.activity[number=2D]  «Sentence building»`
  - Claude: `div.activity.interactive[number=2D]  «Sentence building»`
- **BLL123** BLL123_2_0.html ↔ BLL123-03.html (structure, derivable=True)
  - gold: `div.activity[number=2C]  «Sentence building»`
  - Claude: `div.activity.interactive[number=2C]  «Sentence building»`
- **BLL131** BLL131_1_0.html ↔ BLL131-02.html (structure, derivable=True)
  - gold: `div.activity[number=1A]  «Match the letters»`
  - Claude: `div.activity.interactive[number=1A]  «Match the letters»`
- modules: BLL115, BLL123, BLL131, BLL132, BLL135, BLL143, BLL147, BLL152, BLL153, BLL154, BLL156, BLL163, BLL164, BLL165, BLL173, BLL176

### #846 · body · SUBSTITUTED · `div.row` › gold `div.col-12` vs Claude `div.col-12.col-md-8` — CANDIDATE
- pages 54 / modules 43 / lines 58; consensus (all) 0.51 of 150 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 42m/53p c=0.49; Inquiry 1m/1p c=0.86
- by subject: 1-10 Blended Literacy 43m/54p c=0.51
- by era: Refresh 43m/54p c=0.51
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL150** BLL150_0_0.html ↔ BLL150.html (structure, derivable=True)
  - gold: `div.col-12  «Find the sound»`
  - Claude: `div.col-12.col-md-8  «Find the sound»`
- **BLL111** BLL111_0_0.html ↔ BLL111-01.html (structure, derivable=True)
  - gold: `div.col-12  «Introduction»`
  - Claude: `div.col-12.col-md-8  «Module 1 – s, a, t, p, i, n.»`
- **BLL112** BLL112_0_0.html ↔ BLL112-01.html (structure, derivable=True)
  - gold: `div.col-12  «Introduction»`
  - Claude: `div.col-12.col-md-8  «Introduction»`
- modules: BLL111, BLL112, BLL113, BLL114, BLL115, BLL116, BLL117, BLL121, BLL122, BLL123, BLL124, BLL125, BLL126, BLL127, BLL131, BLL132, BLL133, BLL134, BLL135, BLL136, BLL137, BLL144, BLL145, BLL146 …

### #847 · body · EXTRA · `div#body` › gold `—` vs Claude `div.row` — CANDIDATE
- pages 68 / modules 40 / lines 102; consensus (all) 0.69 of 150 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 40m/68p c=0.67
- by subject: 1-10 Blended Literacy 40m/68p c=0.69
- by era: Refresh 40m/68p c=0.69
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL111** BLL111_0_0.html ↔ BLL111-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Introduction»`
- **BLL113** BLL113_1_0.html ↔ BLL113-02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Decoding words»`
- **BLL114** BLL114_0_0.html ↔ BLL114-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Introduction»`
- modules: BLL111, BLL113, BLL114, BLL115, BLL116, BLL117, BLL121, BLL123, BLL124, BLL125, BLL127, BLL131, BLL132, BLL133, BLL134, BLL135, BLL136, BLL137, BLL141, BLL142, BLL143, BLL144, BLL145, BLL146 …

### #849 · body · EXTRA · `p>i` › gold `—` vs Claude `i` — CANDIDATE
- pages 26 / modules 26 / lines 29; consensus (all) 1.00 of 150 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 26m/26p c=1.00
- by subject: 1-10 Blended Literacy 26m/26p c=1.00
- by era: Refresh 26m/26p c=1.00
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL114** BLL114_0_0.html ↔ BLL114-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `i  «Welcome to Module 4. We are continuing to learn about the ‘s, a, t, p, i, and n’ and blending these letters and sounds t»`
- **BLL115** BLL115_0_0.html ↔ BLL115-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `i  «Welcome to Module 5. We are continuing to learn about the ‘s, a, t, p, i, and n’ and blending these letters and sounds t»`
- **BLL116** BLL116_0_0.html ↔ BLL116-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `i  «Welcome to Module 6. We are continuing to learn about ‘s, a, t, p, i, and n’ and blending these letters and sounds toget»`
- modules: BLL114, BLL115, BLL116, BLL117, BLL124, BLL131, BLL132, BLL133, BLL134, BLL135, BLL136, BLL137, BLL142, BLL144, BLL153, BLL154, BLL156, BLL157, BLL161, BLL162, BLL163, BLL164, BLL165, BLL174 …

### #850 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `p` — CANDIDATE
- pages 21 / modules 21 / lines 62; consensus (all) 0.97 of 150 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 16m/16p c=1.00; Inquiry 5m/5p c=0.43
- by subject: 1-10 Blended Literacy 21m/21p c=0.97
- by era: Refresh 21m/21p c=0.97
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL110** BLL110_0_0.html ↔ BLL110.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «My name is s, my sound is /s/.»`
- **BLL120** BLL120_0_0.html ↔ BLL120.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «We'll get to know each letter and the sound it makes. We'll have fun singing songs, playing games, and watching some coo»`
- **BLL130** BLL130_0_0.html ↔ BLL130.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «My name is u, my sound is /u/.»`
- modules: BLL110, BLL111, BLL112, BLL113, BLL115, BLL116, BLL117, BLL120, BLL121, BLL123, BLL130, BLL144, BLL145, BLL146, BLL147, BLL150, BLL152, BLL157, BLL160, BLL162, BLL164

### #851 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `p>b` — CANDIDATE
- pages 21 / modules 21 / lines 31; consensus (all) 1.00 of 150 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 16m/16p c=1.00; Inquiry 5m/5p c=1.00
- by subject: 1-10 Blended Literacy 21m/21p c=1.00
- by era: Refresh 21m/21p c=1.00
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL110** BLL110_0_0.html ↔ BLL110.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Audio»`
- **BLL130** BLL130_0_0.html ↔ BLL130.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Audio»`
- **BLL140** BLL140_0_0.html ↔ BLL140.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Audio»`
- modules: BLL110, BLL112, BLL122, BLL130, BLL140, BLL143, BLL150, BLL152, BLL154, BLL156, BLL157, BLL160, BLL161, BLL162, BLL163, BLL164, BLL165, BLL166, BLL167, BLL171, BLL173

### #852 · body · EXTRA · `div.row` › gold `—` vs Claude `div.col-12.col-md-8` — CANDIDATE
- pages 20 / modules 19 / lines 46; consensus (all) 0.86 of 150 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 12m/13p c=0.90; Inquiry 7m/7p c=0.00
- by subject: 1-10 Blended Literacy 19m/20p c=0.86
- by era: Refresh 19m/20p c=0.86
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL110** BLL110_0_0.html ↔ BLL110.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-8  «The letter p»`
- **BLL120** BLL120_0_0.html ↔ BLL120.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-8  «Supervisor note:»`
- **BLL130** BLL130_0_0.html ↔ BLL130.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-8  «When a letter is written as ‘g’ we want you to say its name. When it is written as /g/ it means we want you to say its s»`
- modules: BLL110, BLL113, BLL114, BLL115, BLL120, BLL121, BLL125, BLL126, BLL127, BLL130, BLL133, BLL137, BLL140, BLL147, BLL150, BLL156, BLL160, BLL170, BLL171

### #1073 · root · EXTRA · `body.container-fluid` › gold `—` vs Claude `div.row` — CANDIDATE
- pages 48 / modules 48 / lines 48; consensus (all) 0.72 of 150 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 48m/48p c=0.71
- by subject: 1-10 Blended Literacy 48m/48p c=0.72
- by era: Refresh 48m/48p c=0.72
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL111** BLL111_0_0.html ↔ BLL111-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row`
- **BLL112** BLL112_0_0.html ↔ BLL112-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row`
- **BLL113** BLL113_0_0.html ↔ BLL113-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row`
- modules: BLL111, BLL112, BLL113, BLL114, BLL115, BLL116, BLL117, BLL121, BLL122, BLL123, BLL124, BLL125, BLL126, BLL127, BLL131, BLL132, BLL133, BLL134, BLL135, BLL136, BLL137, BLL141, BLL142, BLL143 …
