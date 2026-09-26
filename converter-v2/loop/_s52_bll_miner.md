# DIFF_QUEUE.md — the diff miner's ranked class queue (LOOP__Autonomous_Rounds.md §1d)

**Produced:** 2026-09-26 17:37 NZST by `reference/tests/_diff_miner.py` on the CURRENT corpus (pageforge-site HEAD 9c0a1af; Claude corpus 545 dirs). **Population:** the skeleton gate's own — 298 paired pages / 109 modules (compare_exclusions.txt honoured; acks / glossary / references pages excluded); parse errors skipped: 0 (must be 0); modules without a parsed WT: 0. Run time 13.6 s.

**What a row is.** One CLASS = (region, parent element, gold form, Claude form, direction) over every differing skeleton line of every paired page — the same lines, labels, widget collapse and difflib alignment the PRIMARY gate scores (each element its own line so it can be quoted). Direction: MISSING = gold has it, Claude lacks it; EXTRA = Claude has it, gold lacks it; SUBSTITUTED = same position, different tag / class / wrapper; MOVED = same text, different place. Consensus = of the gold pages in the group where the region exists, the share carrying the gold form (for EXTRA: the share NOT carrying Claude's form). Derivable = the gold line's text is in the module's parsed Writers Template (round-110 tolerance); structure-only differences are always derivable.

**Candidate rule (§1d).** modules ≥ 10 for a chrome class (module-code / title / header / module-menu / crumbs / phases-nav / footer / acks), pages ≥ 20 for a body / activity class; gold consensus ≥ 0.60 in at least one template or subject group that itself reaches the floor; structure-only or derivable share ≥ 0.60. A class below the floor is listed, never dropped. A CANDIDATE still goes through the PICK's KB-first check, the triangulation and the §3 corpus-wide measurement before any code — this table is the queue, not the verdict.

## Summary

- differing skeleton lines: 29242 — by direction {'SUBSTITUTED': 3887, 'MISSING': 16938, 'EXTRA': 7640, 'MOVED': 777}
- by region: {'module-code': 2, 'title': 14, 'header': 2, 'module-menu': 764, 'footer': 408, 'acks': 305, 'activity': 21173, 'body': 6312, 'root': 262}
- classes: 1809 — CANDIDATE 35, below floor 1738, the rest below consensus / not derivable

## Completeness census — the repeating chrome (§1d item 4)

| region | pages with region | gold items | gold items in WT | Claude items | derivable misses | pages with misses | modules with misses | status |
|---|---|---|---|---|---|---|---|---|
| module-menu | 94 | 2472 | 2319 | 2453 | 114 | 38 | 38 | CANDIDATE (verify by eye — text presence, not position) |
| crumbs | 14 | 99 | 98 | 99 | 5 | 5 | 5 | BELOW FLOOR |
| phases-nav | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |
| footer | 8 | 36 | 20 | 0 | 20 | 8 | 6 | BELOW FLOOR |

- **module-menu** by template: Inquiry 8m/8p/12 misses; Standard 30m/30p/102 misses
  - BLL124 BLL124_0_0.html: gold 23 items (21 in WT) / Claude 2 — 21 derivable misses, e.g. h4 «Learning Intentions» · span «Learning Intentions»
  - BLL122 BLL122_0_0.html: gold 27 items (17 in WT) / Claude 20 — 7 derivable misses, e.g. h5 «Know:» · span «Know:»
  - BLL123 BLL123_0_0.html: gold 23 items (17 in WT) / Claude 23 — 6 derivable misses, e.g. h5 «Understand:» · span «Understand:»
  - BLL114 BLL114_0_0.html: gold 27 items (19 in WT) / Claude 16 — 5 derivable misses, e.g. h5 «Do:» · span «Do:»
- **crumbs** by template: Inquiry 5m/5p/5 misses
  - BLL120 BLL120_0_0.html: gold 9 items (9 in WT) / Claude 9 — 1 derivable misses, e.g. p «The letters ck»
  - BLL160 BLL160_0_0.html: gold 6 items (6 in WT) / Claude 6 — 1 derivable misses, e.g. p «Letter team sh»
  - BLL170 BLL170_0_0.html: gold 7 items (7 in WT) / Claude 7 — 1 derivable misses, e.g. p «Letter team 'ue'»
  - BLL240 BLL240_0_0.html: gold 8 items (8 in WT) / Claude 8 — 1 derivable misses, e.g. p «air»
- **phases-nav** by template: 
- **footer** by template: Standard 6m/8p/20 misses
  - BLL241 BLL241_0_0.html: gold 4 items (4 in WT) / Claude 0 — 4 derivable misses, e.g. li «Next» · a#next-lesson «Next»
  - BLL245 BLL245_0_0.html: gold 4 items (4 in WT) / Claude 0 — 4 derivable misses, e.g. li «Next» · a#next-lesson «Next»
  - BLL236 BLL236_0_0.html: gold 4 items (2 in WT) / Claude 0 — 2 derivable misses, e.g. li «Next» · a#next-lesson «Next»
  - BLL236 BLL236_1_0.html: gold 6 items (2 in WT) / Claude 0 — 2 derivable misses, e.g. li «Next» · a#next-lesson «Next»

## Chrome facts — the header and footer as SETS per page (alignment-free; §1d items 2 + 4)

A fact is one thing a page's chrome has: `header:chip` (the `#module-code` div), `header:chip=module-code` / `=lesson-number` / `=lesson-number(00)`, `header:head-buttons`, `header:menu-content`, `header:title-h1-count=N`, `footer:present`, `footer:ul=<classes>`, `footer:link=prev-lesson` / `next-lesson` / `home-nav`, `footer:links=<order>`, `footer:inside-body`, `nav:crumbs`, `nav:phases`. MISSING = the gold page has the fact and Claude's does not; EXTRA the reverse. Consensus = the share of gold pages in the group that have (MISSING) / lack (EXTRA) the fact. Floor 10 modules.

| # | dir | fact | pages | modules | gold share (all) | consensus (all) | best group | status |
|---|---|---|---|---|---|---|---|---|
| F1 | MISSING | `header:chip=module-code` | 14 | 14 | 0.07 | 0.07 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F2 | EXTRA | `header:chip=other` | 13 | 13 | 0.28 | 0.72 | era=Refresh c=0.72 n=13 | CANDIDATE |
| F3 | MISSING | `header:title-h1-count=1` | 6 | 6 | 1.00 | 1.00 | — | BELOW FLOOR |
| F4 | EXTRA | `header:title-h1-count=2` | 6 | 6 | 0.00 | 1.00 | — | BELOW FLOOR |
| F5 | MISSING | `header:head-buttons` | 10 | 5 | 0.41 | 0.41 | — | BELOW FLOOR |
| F6 | EXTRA | `header:chip=decimal-number` | 8 | 4 | 0.36 | 0.64 | — | BELOW FLOOR |
| F7 | MISSING | `header:chip=lesson-number` | 6 | 3 | 0.27 | 0.27 | — | BELOW FLOOR |
| F8 | MISSING | `header:chip=decimal-number` | 6 | 3 | 0.36 | 0.36 | — | BELOW FLOOR |
| F9 | EXTRA | `header:chip=lesson-number` | 6 | 3 | 0.27 | 0.73 | — | BELOW FLOOR |
| F10 | MISSING | `header:chip=other` | 3 | 2 | 0.28 | 0.28 | — | BELOW FLOOR |
| F11 | MISSING | `header:chip` | 1 | 1 | 0.98 | 0.98 | — | BELOW FLOOR |
| F12 | EXTRA | `header:chip=lesson-number(00)` | 1 | 1 | 0.00 | 1.00 | — | BELOW FLOOR |
| F13 | MISSING | `footer:inside-body` | 44 | 34 | 0.15 | 0.15 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F14 | EXTRA | `footer:links=prev-lesson,home-nav` | 20 | 20 | 0.25 | 0.75 | era=Refresh c=0.75 n=20 | CANDIDATE |
| F15 | MISSING | `footer:link=next-lesson` | 19 | 19 | 0.74 | 0.74 | era=Refresh c=0.74 n=19 | CANDIDATE |
| F16 | MISSING | `footer:links=prev-lesson,next-lesson,home-nav` | 17 | 17 | 0.38 | 0.38 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F17 | MISSING | `footer:ul=footer-nav` | 36 | 12 | 0.12 | 0.12 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F18 | EXTRA | `footer:ul=footer-nav inquiry-nav` | 36 | 12 | 0.88 | 0.12 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F19 | EXTRA | `footer:links=prev-lesson,next-lesson,home-nav` | 12 | 12 | 0.38 | 0.62 | ptype=overview c=0.97 n=11 | CANDIDATE |
| F20 | MISSING | `footer:links=home-nav,prev-lesson,next-lesson` | 8 | 8 | 0.03 | 0.03 | — | BELOW FLOOR |
| F21 | EXTRA | `footer:link=prev-lesson` | 7 | 7 | 0.66 | 0.34 | — | BELOW FLOOR |
| F22 | MISSING | `footer:links=home-nav,next-lesson` | 6 | 6 | 0.02 | 0.02 | — | BELOW FLOOR |
| F23 | EXTRA | `footer:links=next-lesson,home-nav` | 6 | 6 | 0.31 | 0.69 | — | BELOW FLOOR |
| F24 | MISSING | `footer:links=home-nav` | 3 | 3 | 0.01 | 0.01 | — | BELOW FLOOR |
| F25 | EXTRA | `footer:link=next-lesson` | 3 | 3 | 0.74 | 0.26 | — | BELOW FLOOR |
| F26 | MISSING | `footer:links=next-lesson,home-nav` | 3 | 3 | 0.31 | 0.31 | — | BELOW FLOOR |
| F27 | MISSING | `footer:links=other,home-nav` | 1 | 1 | 0.00 | 0.00 | — | BELOW FLOOR |
| F28 | MISSING | `footer:link=other` | 1 | 1 | 0.00 | 0.00 | — | BELOW FLOOR |

### F2 · EXTRA `header:chip=other` — CANDIDATE (pages 13 / modules 13)
- by template+ptype: Standard/overview 13m/13p gold 0.86 Claude 0.99 c=0.14
- by subject: 1-10 Blended Literacy 13m/13p gold 0.28 Claude 0.32 c=0.72
- **BLL172** BLL172_0_0.html ↔ BLL172-00.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **BLL174** BLL174_0_0.html ↔ BLL174-00.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **BLL175** BLL175_0_0.html ↔ BLL175-00.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: BLL172, BLL174, BLL175, BLL176, BLL177, BLL252, BLL253, BLL265, BLL266, BLL271, BLL273, BLL274, BLL276

### F14 · EXTRA `footer:links=prev-lesson,home-nav` — CANDIDATE (pages 20 / modules 20)
- by template+ptype: Standard/lesson 20m/20p gold 0.39 Claude 0.50 c=0.61
- by subject: 1-10 Blended Literacy 20m/20p gold 0.25 Claude 0.32 c=0.75
- **BLL141** BLL141_2_0.html ↔ BLL141-2.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL146** BLL146_2_0.html ↔ BLL146-2.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL151** BLL151_2_0.html ↔ BLL151-2.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL141, BLL146, BLL151, BLL157, BLL167, BLL171, BLL176, BLL177, BLL224, BLL225, BLL226, BLL227, BLL231, BLL234, BLL236, BLL237, BLL266, BLL271, BLL274, BLL276

### F15 · MISSING `footer:link=next-lesson` — CANDIDATE (pages 19 / modules 19)
- by template+ptype: Standard/lesson 19m/19p gold 0.60 Claude 0.50 c=0.60
- by subject: 1-10 Blended Literacy 19m/19p gold 0.74 Claude 0.69 c=0.74
- **BLL141** BLL141_2_0.html ↔ BLL141-2.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL146** BLL146_2_0.html ↔ BLL146-2.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL151** BLL151_2_0.html ↔ BLL151-2.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL141, BLL146, BLL151, BLL157, BLL167, BLL171, BLL176, BLL177, BLL224, BLL225, BLL226, BLL227, BLL231, BLL234, BLL236, BLL237, BLL266, BLL274, BLL276

### F19 · EXTRA `footer:links=prev-lesson,next-lesson,home-nav` — CANDIDATE (pages 12 / modules 12)
- by template+ptype: Inquiry/overview 11m/11p gold 0.21 Claude 1.00 c=0.79; Standard/lesson 1m/1p gold 0.59 Claude 0.50 c=0.41
- by subject: 1-10 Blended Literacy 12m/12p gold 0.38 Claude 0.37 c=0.62
- **BLL120** BLL120_0_0.html ↔ BLL120.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL140** BLL140_0_0.html ↔ BLL140.html: gold ['footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL150** BLL150_0_0.html ↔ BLL150.html: gold ['footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL120, BLL140, BLL150, BLL170, BLL175, BLL210, BLL220, BLL230, BLL240, BLL250, BLL260, BLL270


## The ranked queue — chrome regions first, then by modules affected

| # | region | dir | parent | gold form | Claude form | pages | modules | consensus (all) | best group | derivable | KB | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | module-code | MISSING | `div#header` | `div#module-code` | `—` | 1 | 1 | 0.98 of 298 | — | structure | yes | BELOW FLOOR |
| 2 | title | EXTRA | `div#header` | `—` | `h1>span` | 6 | 6 | 1.00 of 298 | — | structure | yes | BELOW FLOOR |
| 3 | title | MISSING | `span>span` | `span` | `—` | 6 | 2 | 0.07 of 298 | — | 1.00 | — | BELOW FLOOR |
| 4 | title | MISSING | `div.titlebar` | `h1.moduleTitle>span.module-subtitle.text-lowercase` | `—` | 2 | 1 | 0.01 of 298 | — | 1.00 | — | BELOW FLOOR |
| 5 | header | SUBSTITUTED | `div#header` | `div.titlebar` | `h1>span` | 2 | 1 | 0.01 of 298 | — | structure | yes | BELOW FLOOR |
| 6 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `p` | `h5` | 73 | 73 | 0.27 of 298 | template=Inquiry c=0.93 n=11 | structure | yes | CANDIDATE |
| 7 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `p` | `—` | 24 | 24 | 0.24 of 298 | template+ptype=Standard/overview c=0.67 n=20 | 0.48 | yes | NOT DERIVABLE (content share < 0.60) |
| 8 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `p>b` | 22 | 22 | 1.00 of 298 | era=Refresh c=1.00 n=22 | structure | yes | CANDIDATE |
| 9 | module-menu | MISSING | `ul` | `li` | `—` | 21 | 21 | 0.21 of 298 | — | 0.97 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 10 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-6.paddingR` | 17 | 17 | 0.73 of 298 | template=Standard c=0.76 n=12 | structure | yes | CANDIDATE |
| 11 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `ul` | `p>b` | 14 | 14 | 0.27 of 298 | ptype=overview c=0.74 n=14 | structure | yes | CANDIDATE |
| 12 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-12.paddingR` | 12 | 12 | 0.78 of 298 | template=Standard c=0.81 n=12 | structure | yes | CANDIDATE |
| 13 | module-menu | EXTRA | `div.row` | `—` | `WIDGET` | 12 | 12 | 0.98 of 298 | template=Standard c=0.98 n=12 | structure | — | CANDIDATE |
| 14 | module-menu | SUBSTITUTED | `div#module-menu-content.moduleMenu` | `WIDGET` | `div.row` | 12 | 12 | 0.04 of 298 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 15 | module-menu | EXTRA | `ul` | `—` | `li` | 11 | 11 | 0.87 of 298 | era=Refresh c=0.87 n=11 | structure | — | CANDIDATE |
| 16 | module-menu | MISSING | `h5>span` | `span` | `—` | 10 | 10 | 0.26 of 298 | ptype=overview c=0.70 n=10 | 1.00 | — | CANDIDATE |
| 17 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `h5>span` | `—` | 10 | 10 | 0.21 of 298 | — | 1.00 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 18 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `p` | 9 | 9 | 0.73 of 298 | — | structure | yes | BELOW FLOOR |
| 19 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `ul` | `—` | 9 | 9 | 0.22 of 298 | — | 0.50 | yes | BELOW FLOOR |
| 20 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `h4>span` | `h5>span` | 9 | 9 | 0.03 of 298 | — | structure | yes | BELOW FLOOR |
| 21 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.paddingR` | `div.col-12.col-md-12.paddingR` | 8 | 8 | 0.28 of 298 | — | structure | yes | BELOW FLOOR |
| 22 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `h5` | 5 | 5 | 1.00 of 298 | — | structure | yes | BELOW FLOOR |
| 23 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `h5>span` | 5 | 5 | 0.79 of 298 | — | structure | yes | BELOW FLOOR |
| 24 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6.paddingR` | `—` | 5 | 5 | 0.27 of 298 | — | 1.00 | yes | BELOW FLOOR |
| 25 | module-menu | MISSING | `p` | `br` | `—` | 5 | 5 | 0.03 of 298 | — | structure | — | BELOW FLOOR |
| 26 | module-menu | SUBSTITUTED | `div.col-12.col-md-6` | `h4>span` | `h5>span` | 5 | 5 | 0.02 of 298 | — | structure | yes | BELOW FLOOR |
| 27 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.paddingL` | `div.col-12.col-md-6.paddingR` | 5 | 5 | 0.02 of 298 | — | structure | yes | BELOW FLOOR |
| 28 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingL` | `p` | `h5` | 5 | 5 | 0.02 of 298 | — | structure | yes | BELOW FLOOR |
| 29 | module-menu | MISSING | `div#header` | `div#module-head-buttons` | `—` | 8 | 4 | 0.41 of 298 | — | structure | yes | BELOW FLOOR |
| 30 | module-menu | EXTRA | `div.col-12.col-md-12.paddingR` | `—` | `h4>span` | 4 | 4 | 0.80 of 298 | — | structure | yes | BELOW FLOOR |
| 31 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `h4>span` | `—` | 4 | 4 | 0.03 of 298 | — | 1.00 | yes | BELOW FLOOR |
| 32 | module-menu | MISSING | `li` | `ul` | `—` | 4 | 4 | 0.03 of 298 | — | 1.00 | — | BELOW FLOOR |
| 33 | module-menu | MISSING | `div.col-12.col-md-6` | `h4>span` | `—` | 4 | 4 | 0.02 of 298 | — | 1.00 | yes | BELOW FLOOR |
| 34 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-12` | `div.col-12.col-md-12.paddingR` | 4 | 4 | 0.01 of 298 | — | structure | yes | BELOW FLOOR |
| 35 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6` | `div.col-12.col-md-6.paddingR` | 4 | 4 | 0.03 of 298 | — | structure | yes | BELOW FLOOR |
| 36 | module-menu | SUBSTITUTED | `div.col-12.col-md-6` | `p` | `h5>span` | 4 | 4 | 0.03 of 298 | — | structure | yes | BELOW FLOOR |
| 37 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `ul` | 3 | 3 | 1.00 of 298 | — | structure | yes | BELOW FLOOR |
| 38 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6` | `—` | 3 | 3 | 0.03 of 298 | — | 1.00 | yes | BELOW FLOOR |
| 39 | module-menu | MISSING | `div.row` | `div.col-12.col-md-12.paddingR` | `—` | 3 | 3 | 0.01 of 298 | — | 1.00 | yes | BELOW FLOOR |
| 40 | module-menu | SUBSTITUTED | `ul` | `p` | `li` | 3 | 3 | 0.01 of 298 | — | structure | — | BELOW FLOOR |
| 41 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `ul` | `p` | 3 | 3 | 0.27 of 298 | — | structure | yes | BELOW FLOOR |
| 42 | module-menu | MISSING | `div.col-12.col-md-8` | `p` | `—` | 4 | 2 | 0.01 of 298 | — | 0.00 | — | BELOW FLOOR |
| 43 | module-menu | MISSING | `li` | `i` | `—` | 2 | 2 | 0.00 of 298 | — | 1.00 | — | BELOW FLOOR |
| 44 | module-menu | SUBSTITUTED | `div.col-12.col-md-6` | `p` | `h5` | 2 | 2 | 0.03 of 298 | — | structure | yes | BELOW FLOOR |
| 45 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `p` | `ul` | 2 | 2 | 0.27 of 298 | — | structure | yes | BELOW FLOOR |
| 46 | module-menu | SUBSTITUTED | `div.col-12.col-md-12.paddingR` | `p` | `h5` | 2 | 2 | 0.01 of 298 | — | structure | yes | BELOW FLOOR |
| 47 | module-menu | MISSING | `div.titlebar` | `div#module-head-buttons` | `—` | 2 | 1 | 0.01 of 298 | — | structure | yes | BELOW FLOOR |
| 48 | module-menu | EXTRA | `p>b` | `—` | `b` | 1 | 1 | 1.00 of 298 | — | structure | — | BELOW FLOOR |
| 49 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `p>b` | `—` | 1 | 1 | 0.00 of 298 | — | 0.00 | yes | BELOW FLOOR |
| 50 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `h5` | `—` | 1 | 1 | 0.27 of 298 | — | 1.00 | yes | BELOW FLOOR |
| 51 | module-menu | MISSING | `ul` | `li>b` | `—` | 1 | 1 | 0.00 of 298 | — | 1.00 | — | BELOW FLOOR |
| 52 | module-menu | MISSING | `div.col-12.col-md-6` | `p` | `—` | 1 | 1 | 0.02 of 298 | — | 1.00 | yes | BELOW FLOOR |
| 53 | module-menu | MISSING | `li>i` | `i` | `—` | 1 | 1 | 0.00 of 298 | — | 1.00 | — | BELOW FLOOR |
| 54 | module-menu | MISSING | `ul` | `li>i` | `—` | 1 | 1 | 0.01 of 298 | — | 0.50 | — | BELOW FLOOR |
| 55 | module-menu | MOVED | `ul` | `li` | `li>i` | 1 | 1 | 0.28 of 298 | — | structure | — | BELOW FLOOR |
| 56 | module-menu | MOVED | `ul` | `li` | `li` | 1 | 1 | 0.21 of 298 | — | structure | — | BELOW FLOOR |
| 57 | module-menu | SUBSTITUTED | `p` | `ul` | `b` | 1 | 1 | 0.01 of 298 | — | structure | — | BELOW FLOOR |
| 58 | module-menu | SUBSTITUTED | `ul` | `p` | `li>b` | 1 | 1 | 0.01 of 298 | — | structure | — | BELOW FLOOR |
| 59 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `p` | `h5>span` | 1 | 1 | 0.27 of 298 | — | structure | yes | BELOW FLOOR |
| 60 | module-menu | SUBSTITUTED | `p` | `br` | `b` | 1 | 1 | 0.03 of 298 | — | structure | — | BELOW FLOOR |
| 61 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6` | `div.col-12.col-md-12.paddingR` | 1 | 1 | 0.03 of 298 | — | structure | yes | BELOW FLOOR |
| 62 | module-menu | SUBSTITUTED | `div.col-12.col-md-12.paddingR` | `p>i` | `h5` | 1 | 1 | 0.00 of 298 | — | structure | yes | BELOW FLOOR |
| 63 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `p>i` | `h5` | 1 | 1 | 0.00 of 298 | — | structure | yes | BELOW FLOOR |
| 64 | footer | MISSING | `div#body` | `div#footer` | `—` | 24 | 22 | 0.15 of 298 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 65 | footer | MISSING | `ul.footer-nav.inquiry-nav` | `li>a.home-nav` | `—` | 19 | 19 | 0.88 of 298 | era=Refresh c=0.88 n=19 | structure | yes | CANDIDATE |
| 66 | footer | EXTRA | `body.container-fluid` | `—` | `div#footer` | 19 | 18 | 0.20 of 298 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 67 | footer | SUBSTITUTED | `div#body` | `div#footer` | `div#footer` | 18 | 18 | 0.15 of 298 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 68 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav.inquiry-nav` | `ul.footer-nav.inquiry-nav` | 18 | 18 | 0.88 of 298 | ptype=overview c=0.89 n=16 | structure | yes | CANDIDATE |
| 69 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` | `li>a.home-nav` | `li>a.home-nav` | 18 | 18 | 0.88 of 298 | ptype=overview c=0.89 n=16 | structure | yes | CANDIDATE |
| 70 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` | `li>a#next-lesson` | `li>a#next-lesson` | 16 | 16 | 0.64 of 298 | template+ptype=Standard/overview c=0.87 n=15 | structure | yes | CANDIDATE |
| 71 | footer | MISSING | `li>a#next-lesson` | `a#next-lesson` | `—` | 15 | 15 | 0.74 of 298 | era=Refresh c=0.74 n=15 | structure | yes | CANDIDATE |
| 72 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav` | `ul.footer-nav.inquiry-nav` | 36 | 12 | 0.12 of 298 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 73 | footer | EXTRA | `ul.footer-nav.inquiry-nav` | `—` | `li>a.home-nav` | 11 | 11 | 0.12 of 298 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 74 | footer | EXTRA | `div#footer` | `—` | `ul.footer-nav.inquiry-nav` | 10 | 9 | 0.12 of 298 | — | structure | yes | BELOW FLOOR |
| 75 | footer | EXTRA | `ul.footer-nav.inquiry-nav` | `—` | `li>a#next-lesson` | 6 | 6 | 0.36 of 298 | — | structure | yes | BELOW FLOOR |
| 76 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` | `li>a.home-nav` | `li>a#next-lesson` | 5 | 5 | 0.88 of 298 | — | structure | yes | BELOW FLOOR |
| 77 | footer | MISSING | `ul.footer-nav` | `li>a#next-lesson` | `—` | 4 | 4 | 0.10 of 298 | — | structure | yes | BELOW FLOOR |
| 78 | footer | MISSING | `li>a.home-nav` | `a.home-nav` | `—` | 3 | 3 | 1.00 of 298 | — | structure | yes | BELOW FLOOR |
| 79 | footer | MISSING | `ul.footer-nav.inquiry-nav` | `li>a#prev-lesson` | `—` | 3 | 3 | 0.59 of 298 | — | structure | yes | BELOW FLOOR |
| 80 | footer | MISSING | `ul.footer-nav.inquiry-nav` | `li>a#next-lesson` | `—` | 3 | 3 | 0.64 of 298 | — | structure | yes | BELOW FLOOR |
| 81 | footer | MISSING | `div.row` | `div#footer` | `—` | 3 | 3 | 0.01 of 298 | — | structure | yes | BELOW FLOOR |
| 82 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` | `li>a#prev-lesson` | `li>a#prev-lesson` | 3 | 3 | 0.59 of 298 | — | structure | yes | BELOW FLOOR |
| 83 | footer | EXTRA | `ul.footer-nav.inquiry-nav` | `—` | `li>a#prev-lesson` | 2 | 2 | 0.41 of 298 | — | structure | yes | BELOW FLOOR |
| 84 | footer | EXTRA | `li>a#next-lesson` | `—` | `a#next-lesson` | 2 | 2 | 0.26 of 298 | — | structure | yes | BELOW FLOOR |
| 85 | footer | MISSING | `ul.footer-nav` | `li>a.home-nav` | `—` | 2 | 2 | 0.12 of 298 | — | structure | yes | BELOW FLOOR |
| 86 | footer | SUBSTITUTED | `li>a#next-lesson` | `a#next-lesson` | `a#prev-lesson` | 2 | 2 | 0.74 of 298 | — | structure | yes | BELOW FLOOR |
| 87 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` | `li>a#prev-lesson` | `li>a.home-nav` | 2 | 2 | 0.59 of 298 | — | structure | yes | BELOW FLOOR |
| 88 | footer | EXTRA | `li>a#prev-lesson` | `—` | `a#prev-lesson` | 1 | 1 | 0.34 of 298 | — | structure | yes | BELOW FLOOR |
| 89 | footer | MISSING | `div#footer` | `ul.footer-nav.inquiry-nav` | `—` | 1 | 1 | 0.88 of 298 | — | structure | yes | BELOW FLOOR |
| 90 | footer | SUBSTITUTED | `div#body` | `div#footer` | `div.icon.ratio.ratio-16x9.videoSection` | 1 | 1 | 0.15 of 298 | — | structure | yes | BELOW FLOOR |
| 91 | footer | SUBSTITUTED | `div#body` | `div#footer` | `ul.footer-nav.inquiry-nav` | 1 | 1 | 0.15 of 298 | — | structure | yes | BELOW FLOOR |
| 92 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav.inquiry-nav` | `li>a#prev-lesson` | 1 | 1 | 0.88 of 298 | — | structure | yes | BELOW FLOOR |
| 93 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` | `li>a.home-nav` | `div.ratio.ratio-16x9.videoSection` | 1 | 1 | 0.88 of 298 | — | structure | yes | BELOW FLOOR |
| 94 | footer | SUBSTITUTED | `li>a.prev-lesson` | `a.prev-lesson` | `a#prev-lesson` | 1 | 1 | 0.00 of 298 | — | structure | yes | BELOW FLOOR |
| 95 | acks | SUBSTITUTED | `div.col-12.col-md-8` | `div.acks` | `div.acks.acksTemplate` | 23 | 23 | 0.31 of 298 | template=Inquiry c=0.86 n=11 | structure | yes | CANDIDATE |
| 96 | acks | SUBSTITUTED | `div.col-12.col-md-8` | `div.acks.acksAI.acksTemplate` | `div.acks.acksTemplate` | 9 | 9 | 0.03 of 298 | — | structure | yes | BELOW FLOOR |
| 97 | acks | SUBSTITUTED | `div.col-12.col-md-8` | `div.acks` | `div.activity[number=*]` | 2 | 2 | 0.31 of 298 | — | structure | yes | BELOW FLOOR |
| 98 | acks | SUBSTITUTED | `div.acks` | `WIDGET` | `div.row` | 2 | 2 | 0.31 of 298 | — | structure | yes | BELOW FLOOR |
| 99 | acks | SUBSTITUTED | `div.acks` | `WIDGET` | `WIDGET` | 1 | 1 | 0.31 of 298 | — | structure | yes | BELOW FLOOR |
| 100 | acks | SUBSTITUTED | `div.col-12.col-md-8` | `div.acks` | `p` | 1 | 1 | 0.31 of 298 | — | structure | yes | BELOW FLOOR |
| 103 | activity | EXTRA | `div.col-12` | `—` | `p` | 102 | 77 | 0.83 of 298 | template=Standard c=0.87 n=90 | structure | — | CANDIDATE |
| 105 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `div.activity[number=*]` | 70 | 59 | 0.51 of 298 | ptype=lesson c=0.74 n=62 | structure | yes | CANDIDATE |
| 106 | activity | EXTRA | `div.col-12` | `—` | `WIDGET` | 61 | 52 | 0.79 of 298 | template=Standard c=0.83 n=52 | structure | — | CANDIDATE |
| 109 | activity | EXTRA | `div.row` | `—` | `div.col-12` | 58 | 46 | 0.79 of 298 | template=Standard c=0.82 n=51 | structure | — | CANDIDATE |
| 110 | activity | EXTRA | `div.col-12` | `—` | `p>a` | 43 | 40 | 0.99 of 298 | template=Standard c=1.00 n=37 | structure | — | CANDIDATE |
| 111 | activity | EXTRA | `div.col-12` | `—` | `img.img-fluid` | 42 | 40 | 0.95 of 298 | template=Standard c=0.97 n=35 | structure | — | CANDIDATE |
| 119 | activity | EXTRA | `p>a` | `—` | `a` | 34 | 29 | 0.99 of 298 | template=Standard c=1.00 n=32 | structure | — | CANDIDATE |
| 121 | activity | EXTRA | `div.col-12` | `—` | `h3` | 32 | 28 | 0.92 of 298 | template=Standard c=0.96 n=27 | structure | — | CANDIDATE |
| 126 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `div.activity.interactive[number=*]` | 24 | 20 | 0.55 of 298 | ptype=lesson c=0.80 n=23 | structure | yes | CANDIDATE |
| 127 | activity | EXTRA | `p>i` | `—` | `i` | 23 | 20 | 0.88 of 298 | template=Standard c=0.89 n=22 | structure | — | CANDIDATE |
| 129 | activity | SUBSTITUTED | `div.col-12` | `p` | `p` | 22 | 20 | 0.65 of 298 | era=Refresh c=0.65 n=22 | structure | — | CANDIDATE |
| 131 | activity | EXTRA | `div.col-12` | `—` | `audio.audioPlayer.icon` | 22 | 19 | 0.98 of 298 | era=Refresh c=0.98 n=22 | structure | yes | CANDIDATE |
| 132 | activity | EXTRA | `div.col-12` | `—` | `p>i` | 20 | 19 | 0.93 of 298 | template=Standard c=0.94 n=20 | structure | — | CANDIDATE |
| 135 | activity | EXTRA | `div.col-12` | `—` | `p>b` | 20 | 17 | 0.96 of 298 | era=Refresh c=0.96 n=20 | structure | — | CANDIDATE |
| 1374 | body | EXTRA | `div#body` | `—` | `div.row` | 139 | 83 | 0.87 of 298 | ptype=overview c=1.00 n=31 | structure | — | CANDIDATE |
| 1376 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 50 | 47 | 0.97 of 298 | ptype=lesson c=1.00 n=20 | structure | — | CANDIDATE |
| 1380 | body | EXTRA | `div.row` | `—` | `div.col-12.col-md-8` | 39 | 36 | 0.89 of 298 | template=Standard c=0.93 n=28 | structure | — | CANDIDATE |
| 1381 | body | EXTRA | `div.col-12.col-md-8` | `—` | `audio.audioPlayer.icon` | 27 | 27 | 1.00 of 298 | era=Refresh c=1.00 n=27 | structure | yes | CANDIDATE |
| 1382 | body | EXTRA | `p>i` | `—` | `i` | 26 | 26 | 0.98 of 298 | era=Refresh c=0.98 n=26 | structure | — | CANDIDATE |
| 1384 | body | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `div.col-12.col-md-8` | 22 | 20 | 0.97 of 298 | era=Refresh c=0.97 n=22 | structure | — | CANDIDATE |
| 1801 | root | EXTRA | `body.container-fluid` | `—` | `div.row` | 68 | 68 | 0.74 of 298 | ptype=overview c=0.75 n=68 | structure | — | CANDIDATE |

## Details — in the companion file `CONVERTER_V2/outputs/_s52_bll_miner_details.md`
Every CANDIDATE and every top-40 row has three quoted examples (WT / gold / Claude) there, plus the
below-floor list. **NEVER read the companion whole** (hundreds of KB): `grep -n '^### #<rank> ' CONVERTER_V2/outputs/_diff_queue_details.md` then `sed -n '<start>,<start+40>p'`. The top 25
candidates' detail blocks are repeated below for convenience.

### #6 · module-menu · SUBSTITUTED · `div.col-12.col-md-6.paddingR` › gold `p` vs Claude `h5` — CANDIDATE
- pages 73 / modules 73 / lines 143; consensus (all) 0.27 of 298 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 62m/62p c=0.24; Inquiry 11m/11p c=0.93
- by subject: 1-10 Blended Literacy 73m/73p c=0.27
- by era: Refresh 73m/73p c=0.27
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

### #8 · module-menu · EXTRA · `div.col-12.col-md-6.paddingR` › gold `—` vs Claude `p>b` — CANDIDATE
- pages 22 / modules 22 / lines 43; consensus (all) 1.00 of 298 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 19m/19p c=1.00; Inquiry 3m/3p c=1.00
- by subject: 1-10 Blended Literacy 22m/22p c=1.00
- by era: Refresh 22m/22p c=1.00
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
- modules: BLL125, BLL126, BLL127, BLL130, BLL131, BLL132, BLL133, BLL136, BLL137, BLL140, BLL141, BLL143, BLL144, BLL145, BLL146, BLL147, BLL150, BLL151, BLL153, BLL154, BLL213, BLL214

### #10 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `div.col-12.col-md-6.paddingR` — CANDIDATE
- pages 17 / modules 17 / lines 24; consensus (all) 0.73 of 298 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 12m/12p c=0.76; Inquiry 5m/5p c=0.21
- by subject: 1-10 Blended Literacy 17m/17p c=0.73
- by era: Refresh 17m/17p c=0.73
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
- modules: BLL110, BLL111, BLL120, BLL121, BLL134, BLL135, BLL144, BLL152, BLL160, BLL161, BLL172, BLL240, BLL241, BLL244, BLL245, BLL256, BLL270

### #11 · module-menu · SUBSTITUTED · `div.col-12.col-md-6.paddingR` › gold `ul` vs Claude `p>b` — CANDIDATE
- pages 14 / modules 14 / lines 14; consensus (all) 0.27 of 298 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 12m/12p c=0.24; Inquiry 2m/2p c=0.93
- by subject: 1-10 Blended Literacy 14m/14p c=0.27
- by era: Refresh 14m/14p c=0.27
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

### #12 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `div.col-12.col-md-12.paddingR` — CANDIDATE
- pages 12 / modules 12 / lines 12; consensus (all) 0.78 of 298 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 12m/12p c=0.81
- by subject: 1-10 Blended Literacy 12m/12p c=0.78
- by era: Refresh 12m/12p c=0.78
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
- modules: BLL112, BLL113, BLL125, BLL141, BLL142, BLL143, BLL144, BLL162, BLL163, BLL166, BLL236, BLL237

### #13 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `WIDGET` — CANDIDATE
- pages 12 / modules 12 / lines 12; consensus (all) 0.98 of 298 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 12m/12p c=0.98
- by subject: 1-10 Blended Literacy 12m/12p c=0.98
- by era: Refresh 12m/12p c=0.98
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL251** BLL251_0_0.html ↔ BLL251_0_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **BLL255** BLL255_0_0.html ↔ BLL255_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **BLL257** BLL257_0_0.html ↔ BLL257_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- modules: BLL251, BLL255, BLL257, BLL261, BLL264, BLL265, BLL266, BLL271, BLL272, BLL274, BLL275, BLL276

### #15 · module-menu · EXTRA · `ul` › gold `—` vs Claude `li` — CANDIDATE
- pages 11 / modules 11 / lines 27; consensus (all) 0.87 of 298 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 9m/9p c=0.88; Inquiry 2m/2p c=0.71
- by subject: 1-10 Blended Literacy 11m/11p c=0.87
- by era: Refresh 11m/11p c=0.87
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL210** BLL210_0_0.html ↔ BLL210.html (structure, derivable=True)
  - gold: `—`
  - Claude: `li  «say the name of letters and the sound they make»`
- **BLL260** BLL260_0_0.html ↔ BLL260.html (structure, derivable=True)
  - gold: `—`
  - Claude: `li  «whole word is sounded out (continuous blending).»`
- **BLL115** BLL115_0_0.html ↔ BLL115-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `li  «Read nonsense (alien) words»`
- modules: BLL115, BLL122, BLL123, BLL144, BLL145, BLL152, BLL165, BLL210, BLL241, BLL254, BLL260

### #16 · module-menu · MISSING · `h5>span` › gold `span` vs Claude `—` — CANDIDATE
- pages 10 / modules 10 / lines 10; consensus (all) 0.26 of 298 gold pages with the region; derivable 1.00 (0 lines with no WT source)
- by template: Standard 8m/8p c=0.23; Inquiry 2m/2p c=0.71
- by subject: 1-10 Blended Literacy 10m/10p c=0.26
- by era: Refresh 10m/10p c=0.26
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL240** BLL240_0_0.html ↔ BLL240.html (content, derivable=True)
  - gold: `span  «Practices:»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [H2] [/RED TEXT]🔴 **Practices:**`
- **BLL270** BLL270_0_0.html ↔ BLL270.html (content, derivable=True)
  - gold: `span  «Practices:»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [H2] [/RED TEXT]🔴 **Practices****:**`
- **BLL241** BLL241_0_0.html ↔ BLL241-0.0.html (content, derivable=True)
  - gold: `span  «Practices:»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [H2] [/RED TEXT]🔴 **Practices:**`
- modules: BLL240, BLL241, BLL242, BLL244, BLL245, BLL246, BLL252, BLL254, BLL256, BLL270

### #65 · footer · MISSING · `ul.footer-nav.inquiry-nav` › gold `li>a.home-nav` vs Claude `—` — CANDIDATE
- pages 19 / modules 19 / lines 19; consensus (all) 0.88 of 298 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 14m/14p c=0.87; Inquiry 5m/5p c=1.00
- by subject: 1-10 Blended Literacy 19m/19p c=0.88
- by era: Refresh 19m/19p c=0.88
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:40 — | Footer tag | `<nav id="module-foot">` with `<button>` + FA icons | `<div id="footer">` with `<ul class="footer-nav">` |
  - KB: 06_TEMPLATE_RECOGNITION.md:64 — | Footer `<ul>` class | `footer-nav` | `footer-nav` | `footer-nav fundamentals-nav` | `footer-nav inquiry-nav` | `footer-nav` |
  - KB: 06_TEMPLATE_RECOGNITION.md:114 — **Footer:** `<ul class="footer-nav">` with prev + next + home links.
- **BLL170** BLL170_0_0.html ↔ BLL170.html (structure, derivable=True)
  - gold: `li`
  - Claude: `—`
- **BLL210** BLL210_0_0.html ↔ BLL210.html (structure, derivable=True)
  - gold: `li`
  - Claude: `—`
- **BLL250** BLL250_0_0.html ↔ BLL250.html (structure, derivable=True)
  - gold: `li`
  - Claude: `—`
- modules: BLL141, BLL146, BLL151, BLL157, BLL167, BLL170, BLL171, BLL210, BLL224, BLL225, BLL226, BLL227, BLL234, BLL250, BLL260, BLL266, BLL270, BLL274, BLL276

### #68 · footer · SUBSTITUTED · `div#footer` › gold `ul.footer-nav.inquiry-nav` vs Claude `ul.footer-nav.inquiry-nav` — CANDIDATE
- pages 18 / modules 18 / lines 18; consensus (all) 0.88 of 298 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 17m/17p c=0.87; Inquiry 1m/1p c=1.00
- by subject: 1-10 Blended Literacy 18m/18p c=0.88
- by era: Refresh 18m/18p c=0.88
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:40 — | Footer tag | `<nav id="module-foot">` with `<button>` + FA icons | `<div id="footer">` with `<ul class="footer-nav">` |
  - KB: 06_TEMPLATE_RECOGNITION.md:55 — Once confirmed as Refresh, determine which sub-type the reference files represent. This drives structural decisions about navigation, footer classes, 
  - KB: 06_TEMPLATE_RECOGNITION.md:64 — | Footer `<ul>` class | `footer-nav` | `footer-nav` | `footer-nav fundamentals-nav` | `footer-nav inquiry-nav` | `footer-nav` |
- **BLL130** BLL130_0_0.html ↔ BLL130.html (structure, derivable=True)
  - gold: `ul.footer-nav.inquiry-nav`
  - Claude: `ul.footer-nav.inquiry-nav`
- **BLL145** BLL145_1_1.html ↔ BLL145-2.0.html (structure, derivable=True)
  - gold: `ul.footer-nav.inquiry-nav`
  - Claude: `ul.footer-nav.inquiry-nav`
- **BLL154** BLL154_0_0.html ↔ BLL154-0.0.html (structure, derivable=True)
  - gold: `ul.footer-nav.inquiry-nav`
  - Claude: `ul.footer-nav.inquiry-nav`
- modules: BLL130, BLL145, BLL154, BLL156, BLL165, BLL166, BLL171, BLL211, BLL213, BLL216, BLL217, BLL221, BLL222, BLL223, BLL224, BLL231, BLL233, BLL235

### #69 · footer · SUBSTITUTED · `ul.footer-nav.inquiry-nav` › gold `li>a.home-nav` vs Claude `li>a.home-nav` — CANDIDATE
- pages 18 / modules 18 / lines 18; consensus (all) 0.88 of 298 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 17m/17p c=0.87; Inquiry 1m/1p c=1.00
- by subject: 1-10 Blended Literacy 18m/18p c=0.88
- by era: Refresh 18m/18p c=0.88
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:40 — | Footer tag | `<nav id="module-foot">` with `<button>` + FA icons | `<div id="footer">` with `<ul class="footer-nav">` |
  - KB: 06_TEMPLATE_RECOGNITION.md:64 — | Footer `<ul>` class | `footer-nav` | `footer-nav` | `footer-nav fundamentals-nav` | `footer-nav inquiry-nav` | `footer-nav` |
  - KB: 06_TEMPLATE_RECOGNITION.md:114 — **Footer:** `<ul class="footer-nav">` with prev + next + home links.
- **BLL130** BLL130_0_0.html ↔ BLL130.html (structure, derivable=True)
  - gold: `li`
  - Claude: `li`
- **BLL145** BLL145_1_1.html ↔ BLL145-2.0.html (structure, derivable=True)
  - gold: `li`
  - Claude: `li`
- **BLL154** BLL154_0_0.html ↔ BLL154-0.0.html (structure, derivable=True)
  - gold: `li`
  - Claude: `li`
- modules: BLL130, BLL145, BLL154, BLL156, BLL165, BLL166, BLL171, BLL211, BLL213, BLL216, BLL217, BLL221, BLL222, BLL223, BLL224, BLL231, BLL233, BLL235

### #70 · footer · SUBSTITUTED · `ul.footer-nav.inquiry-nav` › gold `li>a#next-lesson` vs Claude `li>a#next-lesson` — CANDIDATE
- pages 16 / modules 16 / lines 16; consensus (all) 0.64 of 298 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 15m/15p c=0.63; Inquiry 1m/1p c=0.79
- by subject: 1-10 Blended Literacy 16m/16p c=0.64
- by era: Refresh 16m/16p c=0.64
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:40 — | Footer tag | `<nav id="module-foot">` with `<button>` + FA icons | `<div id="footer">` with `<ul class="footer-nav">` |
  - KB: 06_TEMPLATE_RECOGNITION.md:64 — | Footer `<ul>` class | `footer-nav` | `footer-nav` | `footer-nav fundamentals-nav` | `footer-nav inquiry-nav` | `footer-nav` |
  - KB: 06_TEMPLATE_RECOGNITION.md:114 — **Footer:** `<ul class="footer-nav">` with prev + next + home links.
- **BLL130** BLL130_0_0.html ↔ BLL130.html (structure, derivable=True)
  - gold: `li`
  - Claude: `li`
- **BLL154** BLL154_0_0.html ↔ BLL154-0.0.html (structure, derivable=True)
  - gold: `li`
  - Claude: `li`
- **BLL156** BLL156_0_0.html ↔ BLL156-0.0.html (structure, derivable=True)
  - gold: `li`
  - Claude: `li`
- modules: BLL130, BLL154, BLL156, BLL165, BLL166, BLL171, BLL211, BLL213, BLL216, BLL217, BLL221, BLL222, BLL223, BLL224, BLL231, BLL235

### #71 · footer · MISSING · `li>a#next-lesson` › gold `a#next-lesson` vs Claude `—` — CANDIDATE
- pages 15 / modules 15 / lines 15; consensus (all) 0.74 of 298 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 15m/15p c=0.74
- by subject: 1-10 Blended Literacy 15m/15p c=0.74
- by era: Refresh 15m/15p c=0.74
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:393 — <li><a href="" id="next-lesson" target="_self"></a></li>
  - KB: 00_MASTER_INSTRUCTIONS/00E_CONSTRAINTS_2.md:20 — 71. **(Universal)** **Footer navigation `href`s are left EMPTY.** Every footer navigation anchor ships with `href=""` — `prev-lesson`, `next-lesson`, 
  - KB: 01_PIPELINE_EXTRACTION_TAGS/01B_MODULE_MENUS_FOOTER.md:388 — - **Overview (-00):** `next-lesson` + `home-nav` only
- **BLL141** BLL141_2_0.html ↔ BLL141-2.0.html (structure, derivable=True)
  - gold: `a#next-lesson`
  - Claude: `—`
- **BLL146** BLL146_2_0.html ↔ BLL146-2.0.html (structure, derivable=True)
  - gold: `a#next-lesson`
  - Claude: `—`
- **BLL151** BLL151_2_0.html ↔ BLL151-2.0.html (structure, derivable=True)
  - gold: `a#next-lesson`
  - Claude: `—`
- modules: BLL141, BLL146, BLL151, BLL157, BLL167, BLL171, BLL224, BLL225, BLL226, BLL234, BLL236, BLL237, BLL266, BLL274, BLL276

### #95 · acks · SUBSTITUTED · `div.col-12.col-md-8` › gold `div.acks` vs Claude `div.acks.acksTemplate` — CANDIDATE
- pages 23 / modules 23 / lines 23; consensus (all) 0.31 of 298 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 12m/12p c=0.28; Inquiry 11m/11p c=0.86
- by subject: 1-10 Blended Literacy 23m/23p c=0.31
- by era: Refresh 23m/23p c=0.31
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:166 — - XFUN01 omits language attributes on `<body>`, has home + next (no `fundamentals-nav`), and places acks after footer
  - KB: 06_TEMPLATE_RECOGNITION.md:193 — - XLP05 lacks `learningSupport` despite being a learning support module
  - KB: 10_CORPUS_VALIDATED_SCAFFOLDING.md:5 — **What this file is.** A small set of scaffolding facts measured *directly* from the finished modules in `01-Finalized_Modules_` (388 developed module
- **BLL110** BLL110_0_0.html ↔ BLL110.html (structure, derivable=True)
  - gold: `div.acks`
  - Claude: `div.acks.acksTemplate`
- **BLL130** BLL130_0_0.html ↔ BLL130.html (structure, derivable=True)
  - gold: `div.acks`
  - Claude: `div.acks.acksTemplate`
- **BLL140** BLL140_0_0.html ↔ BLL140.html (structure, derivable=True)
  - gold: `div.acks`
  - Claude: `div.acks.acksTemplate`
- modules: BLL110, BLL130, BLL140, BLL150, BLL160, BLL170, BLL210, BLL220, BLL224, BLL230, BLL236, BLL240, BLL241, BLL242, BLL243, BLL244, BLL245, BLL246, BLL250, BLL251, BLL254, BLL256, BLL257

### #103 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `p` — CANDIDATE
- pages 102 / modules 77 / lines 371; consensus (all) 0.83 of 298 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 65m/90p c=0.87; Inquiry 12m/12p c=0.00
- by subject: 1-10 Blended Literacy 77m/102p c=0.83
- by era: Refresh 77m/102p c=0.83
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

### #105 · activity · SUBSTITUTED · `div.col-12.col-md-8` › gold `div.activity.interactive[number=*]` vs Claude `div.activity[number=*]` — CANDIDATE
- pages 70 / modules 59 / lines 106; consensus (all) 0.51 of 298 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 51m/62p c=0.49; Inquiry 8m/8p c=0.93
- by subject: 1-10 Blended Literacy 59m/70p c=0.51
- by era: Refresh 59m/70p c=0.51
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
- modules: BLL110, BLL111, BLL115, BLL116, BLL117, BLL120, BLL121, BLL125, BLL126, BLL127, BLL130, BLL133, BLL135, BLL137, BLL141, BLL142, BLL143, BLL144, BLL145, BLL146, BLL147, BLL150, BLL151, BLL153 …

### #106 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `WIDGET` — CANDIDATE
- pages 61 / modules 52 / lines 106; consensus (all) 0.79 of 298 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 43m/52p c=0.83; Inquiry 9m/9p c=0.07
- by subject: 1-10 Blended Literacy 52m/61p c=0.79
- by era: Refresh 52m/61p c=0.79
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
- modules: BLL110, BLL111, BLL112, BLL114, BLL120, BLL127, BLL130, BLL132, BLL133, BLL137, BLL140, BLL141, BLL150, BLL156, BLL160, BLL164, BLL165, BLL172, BLL175, BLL177, BLL211, BLL212, BLL214, BLL215 …

### #109 · activity · EXTRA · `div.row` › gold `—` vs Claude `div.col-12` — CANDIDATE
- pages 58 / modules 46 / lines 97; consensus (all) 0.79 of 298 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 39m/51p c=0.82; Inquiry 7m/7p c=0.00
- by subject: 1-10 Blended Literacy 46m/58p c=0.79
- by era: Refresh 46m/58p c=0.79
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
- modules: BLL110, BLL113, BLL114, BLL116, BLL120, BLL121, BLL123, BLL125, BLL126, BLL127, BLL130, BLL131, BLL134, BLL135, BLL136, BLL137, BLL140, BLL142, BLL143, BLL144, BLL146, BLL147, BLL150, BLL151 …

### #110 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `p>a` — CANDIDATE
- pages 43 / modules 40 / lines 81; consensus (all) 0.99 of 298 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 34m/37p c=1.00; Inquiry 6m/6p c=0.86
- by subject: 1-10 Blended Literacy 40m/43p c=0.99
- by era: Refresh 40m/43p c=0.99
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL120** BLL120_0_0.html ↔ BLL120.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «https://www.istockphoto.com/vector/letter-k-uppercase-and-lowercase-icon-on-red-background-with-shadow-gm1441596634-4812»`
- **BLL130** BLL130_0_0.html ↔ BLL130.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «https://tekura.desire2learn.com/content/enforced/18210-ECHOnline/ECH%20Extra%20Resources/Alphabet-ECH/media/o.mp4»`
- **BLL210** BLL210_0_0.html ↔ BLL210.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «https://www.youtube.com/watch?v=dGIxNzMCcGk»`
- modules: BLL111, BLL112, BLL114, BLL115, BLL120, BLL122, BLL126, BLL130, BLL131, BLL144, BLL154, BLL156, BLL163, BLL166, BLL171, BLL172, BLL174, BLL210, BLL212, BLL213, BLL214, BLL226, BLL227, BLL230 …

### #111 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `img.img-fluid` — CANDIDATE
- pages 42 / modules 40 / lines 124; consensus (all) 0.95 of 298 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 33m/35p c=0.97; Inquiry 7m/7p c=0.50
- by subject: 1-10 Blended Literacy 40m/42p c=0.95
- by era: Refresh 40m/42p c=0.95
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
- modules: BLL110, BLL116, BLL117, BLL120, BLL130, BLL132, BLL134, BLL137, BLL140, BLL142, BLL145, BLL147, BLL150, BLL153, BLL157, BLL160, BLL162, BLL163, BLL164, BLL170, BLL173, BLL174, BLL177, BLL217 …

### #119 · activity · EXTRA · `p>a` › gold `—` vs Claude `a` — CANDIDATE
- pages 34 / modules 29 / lines 47; consensus (all) 0.99 of 298 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 27m/32p c=1.00; Inquiry 2m/2p c=0.86
- by subject: 1-10 Blended Literacy 29m/34p c=0.99
- by era: Refresh 29m/34p c=0.99
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL110** BLL110_0_0.html ↔ BLL110.html (structure, derivable=True)
  - gold: `—`
  - Claude: `a  «https://tekura.desire2learn.com/content/enforced/18210-ECHOnline/ECH%20Extra%20Resources/Alphabet-ECH/media/a.mp4»`
- **BLL120** BLL120_0_0.html ↔ BLL120.html (structure, derivable=True)
  - gold: `—`
  - Claude: `a  «https://www.istockphoto.com/photo/heart-letter-c-gm164026278-22732384?searchscope=image%2Cfilm»`
- **BLL126** BLL126_1_0.html ↔ BLL126-02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `a  «https://www.istockphoto.com/vector/monster-boy-gm1567933348-527709443»`
- modules: BLL110, BLL120, BLL126, BLL131, BLL135, BLL144, BLL153, BLL161, BLL167, BLL173, BLL174, BLL175, BLL177, BLL212, BLL214, BLL221, BLL227, BLL231, BLL235, BLL236, BLL237, BLL243, BLL245, BLL251 …

### #121 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `h3` — CANDIDATE
- pages 32 / modules 28 / lines 44; consensus (all) 0.92 of 298 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 23m/27p c=0.96; Inquiry 5m/5p c=0.00
- by subject: 1-10 Blended Literacy 28m/32p c=0.92
- by era: Refresh 28m/32p c=0.92
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL120** BLL120_0_0.html ↔ BLL120.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h3  «Recap»`
- **BLL150** BLL150_0_0.html ↔ BLL150.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h3  «Optional activities»`
- **BLL160** BLL160_0_0.html ↔ BLL160.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h3  «The different sounds of ‘y’»`
- modules: BLL113, BLL115, BLL117, BLL120, BLL121, BLL131, BLL132, BLL143, BLL144, BLL147, BLL150, BLL151, BLL156, BLL157, BLL160, BLL175, BLL177, BLL217, BLL230, BLL234, BLL235, BLL251, BLL260, BLL262 …

### #126 · activity · SUBSTITUTED · `div.col-12.col-md-8` › gold `div.activity[number=*]` vs Claude `div.activity.interactive[number=*]` — CANDIDATE
- pages 24 / modules 20 / lines 27; consensus (all) 0.55 of 298 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 19m/23p c=0.54; Inquiry 1m/1p c=0.86
- by subject: 1-10 Blended Literacy 20m/24p c=0.55
- by era: Refresh 20m/24p c=0.55
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:46 — | Activity class | `content activity activity-bg` | `activity` |
  - KB: 06_TEMPLATE_RECOGNITION.md:181 — - TWHA902–904 use `choicePage` activity grids and dual titles + `whakatauki` — these are content patterns, safe to use if the new module needs them
  - KB: 06_TEMPLATE_RECOGNITION.md:265 — **The X-prefix test governs THIS CLASS ONLY.** The wider LS look-and-feel conventions of `14_SUBJECT_GLOBAL_PARAMETERS.md` § 14.6 — terminology and br
- **BLL230** BLL230_0_0.html ↔ BLL230.html (structure, derivable=True)
  - gold: `div.activity[number=4A]  «Recap»`
  - Claude: `div.activity.interactive[number=4A]  «Recap»`
- **BLL115** BLL115_2_0.html ↔ BLL115-03.html (structure, derivable=True)
  - gold: `div.activity[number=2D]  «Sentence building»`
  - Claude: `div.activity.interactive[number=2D]  «Sentence building»`
- **BLL123** BLL123_2_0.html ↔ BLL123-03.html (structure, derivable=True)
  - gold: `div.activity[number=2C]  «Sentence building»`
  - Claude: `div.activity.interactive[number=2C]  «Sentence building»`
- modules: BLL115, BLL123, BLL131, BLL132, BLL135, BLL147, BLL152, BLL153, BLL154, BLL156, BLL163, BLL164, BLL165, BLL173, BLL176, BLL213, BLL214, BLL230, BLL242, BLL261

### #127 · activity · EXTRA · `p>i` › gold `—` vs Claude `i` — CANDIDATE
- pages 23 / modules 20 / lines 24; consensus (all) 0.88 of 298 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 19m/22p c=0.89; Inquiry 1m/1p c=0.64
- by subject: 1-10 Blended Literacy 20m/23p c=0.88
- by era: Refresh 20m/23p c=0.88
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL120** BLL120_0_0.html ↔ BLL120.html (structure, derivable=True)
  - gold: `—`
  - Claude: `i  «Supervisor note – if your ākonga is having difficulty remembering both the name of the letter and the sound of the lette»`
- **BLL114** BLL114_1_0.html ↔ BLL114-02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `i  «Sant the Ant»`
- **BLL115** BLL115_2_0.html ↔ BLL115-03.html (structure, derivable=True)
  - gold: `—`
  - Claude: `i  «During reading the student will sound out and blend the sounds to read the words. Allow enough time for this and encoura»`
- modules: BLL114, BLL115, BLL120, BLL123, BLL134, BLL137, BLL141, BLL144, BLL146, BLL151, BLL156, BLL164, BLL173, BLL175, BLL176, BLL214, BLL221, BLL233, BLL234, BLL241

### #129 · activity · SUBSTITUTED · `div.col-12` › gold `p` vs Claude `p` — CANDIDATE
- pages 22 / modules 20 / lines 42; consensus (all) 0.65 of 298 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 17m/19p c=0.63; Inquiry 3m/3p c=1.00
- by subject: 1-10 Blended Literacy 20m/22p c=0.65
- by era: Refresh 20m/22p c=0.65
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL220** BLL220_0_0.html ↔ BLL220.html (structure, derivable=True)
  - gold: `p  «Some ākonga need more practise than others when learning the letters and sounds. Work through this module at your own pa»`
  - Claude: `p  «Some ākonga need more practice than others when learning the letters and sounds. Work through this module at your own pa»`
- **BLL230** BLL230_0_0.html ↔ BLL230.html (structure, derivable=True)
  - gold: `p  «Some ākonga need more practice than others when learning the letters and sounds. Work through this module at your own pa»`
  - Claude: `p  «Some ākonga need more practice than others when learning the letters and sounds. Work through this module at your own pa»`
- **BLL270** BLL270_0_0.html ↔ BLL270.html (structure, derivable=True)
  - gold: `p  «Choose one or more of these activities to do. Click on the picture to view the activity. Take photos of the activity(s) »`
  - Claude: `p  «Whiore piupiu e»`
- modules: BLL145, BLL152, BLL177, BLL220, BLL221, BLL222, BLL225, BLL227, BLL230, BLL231, BLL247, BLL252, BLL253, BLL254, BLL255, BLL256, BLL257, BLL270, BLL275, BLL276
