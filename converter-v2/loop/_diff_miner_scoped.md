# DIFF_QUEUE.md — the diff miner's ranked class queue (LOOP__Autonomous_Rounds.md §1d)

**Produced:** 2026-09-22 11:53 NZST by `reference/tests/_diff_miner.py` on the CURRENT corpus (pageforge-site HEAD cb2aa7e; Claude corpus 545 dirs). **Population:** the skeleton gate's own — 115 paired pages / 38 modules (compare_exclusions.txt honoured; acks / glossary / references pages excluded); parse errors skipped: 0 (must be 0); modules without a parsed WT: 0. Run time 9.8 s.

**What a row is.** One CLASS = (region, parent element, gold form, Claude form, direction) over every differing skeleton line of every paired page — the same lines, labels, widget collapse and difflib alignment the PRIMARY gate scores (each element its own line so it can be quoted). Direction: MISSING = gold has it, Claude lacks it; EXTRA = Claude has it, gold lacks it; SUBSTITUTED = same position, different tag / class / wrapper; MOVED = same text, different place. Consensus = of the gold pages in the group where the region exists, the share carrying the gold form (for EXTRA: the share NOT carrying Claude's form). Derivable = the gold line's text is in the module's parsed Writers Template (round-110 tolerance); structure-only differences are always derivable.

**Candidate rule (§1d).** modules ≥ 10 for a chrome class (module-code / title / header / module-menu / crumbs / phases-nav / footer / acks), pages ≥ 20 for a body / activity class; gold consensus ≥ 0.60 in at least one template or subject group that itself reaches the floor; structure-only or derivable share ≥ 0.60. A class below the floor is listed, never dropped. A CANDIDATE still goes through the PICK's KB-first check, the triangulation and the §3 corpus-wide measurement before any code — this table is the queue, not the verdict.

## Summary

- differing skeleton lines: 18610 — by direction {'SUBSTITUTED': 1369, 'EXTRA': 4480, 'MISSING': 11778, 'MOVED': 983}
- by region: {'module-code': 9, 'title': 39, 'module-menu': 1088, 'crumbs': 144, 'footer': 56, 'acks': 36, 'activity': 8258, 'body': 8948, 'root': 32}
- classes: 1380 — CANDIDATE 11, below floor 1358, the rest below consensus / not derivable

## Completeness census — the repeating chrome (§1d item 4)

| region | pages with region | gold items | gold items in WT | Claude items | derivable misses | pages with misses | modules with misses | status |
|---|---|---|---|---|---|---|---|---|
| module-menu | 52 | 1191 | 1171 | 406 | 829 | 29 | 12 | CANDIDATE (verify by eye — text presence, not position) |
| crumbs | 16 | 93 | 91 | 2 | 89 | 16 | 16 | CANDIDATE (verify by eye — text presence, not position) |
| phases-nav | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |
| footer | 1 | 4 | 2 | 0 | 2 | 1 | 1 | BELOW FLOOR |

- **module-menu** by template: Inquiry 8m/8p/226 misses; Standard 4m/21p/603 misses
  - SSOG105 SSOG105_1_0.html: gold 40 items (40 in WT) / Claude 0 — 40 derivable misses, e.g. h3 «Knowledge» · span «Knowledge»
  - SSOG105 SSOG105_2_0.html: gold 40 items (40 in WT) / Claude 0 — 40 derivable misses, e.g. h3 «Knowledge» · span «Knowledge»
  - SSOG105 SSOG105_3_0.html: gold 40 items (40 in WT) / Claude 0 — 40 derivable misses, e.g. h3 «Knowledge» · span «Knowledge»
  - SSOG105 SSOG105_4_0.html: gold 40 items (40 in WT) / Claude 0 — 40 derivable misses, e.g. h3 «Knowledge» · span «Knowledge»
- **crumbs** by template: Inquiry 16m/16p/89 misses
  - CEDK401 CEDK401_2_0.html: gold 9 items (8 in WT) / Claude 0 — 8 derivable misses, e.g. p «People produce food» · p «Research skills»
  - CEDR101 CEDR101_1_0.html: gold 8 items (8 in WT) / Claude 0 — 8 derivable misses, e.g. p «Introduction» · p «Games in Te Ao Māori»
  - BLL260 BLL260_6_1.html: gold 7 items (7 in WT) / Claude 0 — 7 derivable misses, e.g. p «Introduction» · p «str»
  - BLL250 BLL250_2_5.html: gold 6 items (6 in WT) / Claude 0 — 6 derivable misses, e.g. p «Introduction» · p «Silent b»
- **phases-nav** by template: 
- **footer** by template: Standard 1m/1p/2 misses
  - BLL243 BLL243_0_0.html: gold 4 items (2 in WT) / Claude 0 — 2 derivable misses, e.g. li «Next» · a#next-lesson «Next»

## Chrome facts — the header and footer as SETS per page (alignment-free; §1d items 2 + 4)

A fact is one thing a page's chrome has: `header:chip` (the `#module-code` div), `header:chip=module-code` / `=lesson-number` / `=lesson-number(00)`, `header:head-buttons`, `header:menu-content`, `header:title-h1-count=N`, `footer:present`, `footer:ul=<classes>`, `footer:link=prev-lesson` / `next-lesson` / `home-nav`, `footer:links=<order>`, `footer:inside-body`, `nav:crumbs`, `nav:phases`. MISSING = the gold page has the fact and Claude's does not; EXTRA the reverse. Consensus = the share of gold pages in the group that have (MISSING) / lack (EXTRA) the fact. Floor 10 modules.

| # | dir | fact | pages | modules | gold share (all) | consensus (all) | best group | status |
|---|---|---|---|---|---|---|---|---|
| F1 | EXTRA | `header:chip=decimal-number` | 44 | 18 | 0.23 | 0.77 | subject=1-10 Blended Literacy c=0.83 n=14 | CANDIDATE |
| F2 | MISSING | `header:chip=lesson-number` | 41 | 14 | 0.40 | 0.40 | subject+ptype=1-10 Blended Literacy/lesson c=0.67 n=11 | CANDIDATE |
| F3 | MISSING | `header:chip=module-code` | 16 | 12 | 0.23 | 0.23 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F4 | MISSING | `header:title-h1-count=2` | 25 | 7 | 0.37 | 0.37 | — | BELOW FLOOR |
| F5 | EXTRA | `header:title-h1-count=1` | 25 | 7 | 0.63 | 0.37 | — | BELOW FLOOR |
| F6 | MISSING | `header:head-buttons` | 12 | 7 | 0.79 | 0.79 | — | BELOW FLOOR |
| F7 | EXTRA | `header:chip=other` | 12 | 7 | 0.08 | 0.92 | — | BELOW FLOOR |
| F8 | MISSING | `header:menu-content` | 5 | 5 | 0.73 | 0.73 | — | BELOW FLOOR |
| F9 | MISSING | `header:title-h1-count=1` | 5 | 5 | 0.63 | 0.63 | — | BELOW FLOOR |
| F10 | EXTRA | `header:title-h1-count=2` | 5 | 5 | 0.37 | 0.63 | — | BELOW FLOOR |
| F11 | EXTRA | `header:chip` | 4 | 4 | 0.94 | 0.06 | — | BELOW FLOOR |
| F12 | EXTRA | `header:chip=module-code` | 2 | 2 | 0.23 | 0.77 | — | BELOW FLOOR |
| F13 | EXTRA | `header:chip=lesson-number` | 2 | 2 | 0.40 | 0.60 | — | BELOW FLOOR |
| F14 | MISSING | `header:chip` | 1 | 1 | 0.94 | 0.94 | — | BELOW FLOOR |
| F15 | MISSING | `nav:crumbs` | 14 | 14 | 0.14 | 0.14 | template=Inquiry c=1.00 n=14 | CANDIDATE |
| F16 | MISSING | `footer:links=home-nav,prev-lesson,next-lesson` | 10 | 10 | 0.09 | 0.09 | template=Inquiry c=0.62 n=10 | CANDIDATE |
| F17 | MISSING | `footer:link=next-lesson` | 8 | 8 | 0.78 | 0.78 | — | BELOW FLOOR |
| F18 | EXTRA | `footer:links=prev-lesson,home-nav` | 8 | 8 | 0.17 | 0.83 | — | BELOW FLOOR |
| F19 | EXTRA | `footer:links=prev-lesson,next-lesson,home-nav` | 7 | 7 | 0.50 | 0.50 | — | BELOW FLOOR |
| F20 | EXTRA | `footer:link=prev-lesson` | 4 | 4 | 0.76 | 0.24 | — | BELOW FLOOR |
| F21 | MISSING | `footer:ul=footer-nav inquiry-nav` | 4 | 4 | 0.50 | 0.50 | — | BELOW FLOOR |
| F22 | EXTRA | `footer:ul=footer-nav` | 4 | 4 | 0.50 | 0.50 | — | BELOW FLOOR |
| F23 | MISSING | `footer:links=prev-lesson,next-lesson,home-nav` | 3 | 3 | 0.50 | 0.50 | — | BELOW FLOOR |
| F24 | EXTRA | `footer:link=next-lesson` | 3 | 3 | 0.78 | 0.22 | — | BELOW FLOOR |
| F25 | MISSING | `footer:links=home-nav` | 3 | 3 | 0.04 | 0.04 | — | BELOW FLOOR |
| F26 | MISSING | `footer:link=prev-lesson` | 3 | 3 | 0.76 | 0.76 | — | BELOW FLOOR |
| F27 | EXTRA | `footer:links=home-nav` | 2 | 2 | 0.04 | 0.96 | — | BELOW FLOOR |
| F28 | MISSING | `footer:ul=footer-nav` | 3 | 1 | 0.50 | 0.50 | — | BELOW FLOOR |
| F29 | EXTRA | `footer:ul=footer-nav inquiry-nav` | 3 | 1 | 0.50 | 0.50 | — | BELOW FLOOR |
| F30 | MISSING | `footer:link=other` | 1 | 1 | 0.01 | 0.01 | — | BELOW FLOOR |
| F31 | MISSING | `footer:links=other,home-nav` | 1 | 1 | 0.01 | 0.01 | — | BELOW FLOOR |
| F32 | MISSING | `footer:links=prev-lesson,home-nav` | 1 | 1 | 0.17 | 0.17 | — | BELOW FLOOR |
| F33 | EXTRA | `footer:links=next-lesson,home-nav` | 1 | 1 | 0.19 | 0.81 | — | BELOW FLOOR |
| F34 | MISSING | `footer:inside-body` | 1 | 1 | 0.01 | 0.01 | — | BELOW FLOOR |

### F1 · EXTRA `header:chip=decimal-number` — CANDIDATE (pages 44 / modules 18)
- by template+ptype: Standard/lesson 13m/35p gold 0.36 Claude 0.85 c=0.64; Inquiry/lesson 4m/4p gold 0.00 Claude 0.57 c=1.00; Bilingual/lesson 1m/5p gold 0.00 Claude 1.00 c=1.00
- by subject: 1-10 Blended Literacy 14m/25p gold 0.17 Claude 0.69 c=0.83; 1-10 Social Science 2m/13p gold 0.00 Claude 0.59 c=1.00; ConnectED 1m/1p gold 0.00 Claude 0.12 c=1.00; Te Marautanga o Aotearoa TMoA 1m/5p gold 0.00 Claude 0.83 c=1.00
- **BLL250** BLL250_2_5.html ↔ BLL250.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1']
- **BLL255** BLL255_1_0.html ↔ BLL255_1.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1']
- **BLL260** BLL260_6_1.html ↔ BLL260.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1']
- modules: BLL250, BLL255, BLL260, BLL261, BLL264, BLL265, BLL266, BLL270, BLL271, BLL272, BLL273, BLL274, BLL275, BLL276, CEDK401, SSEA203, SSOG105, TRR110

### F2 · MISSING `header:chip=lesson-number` — CANDIDATE (pages 41 / modules 14)
- by template+ptype: Standard/lesson 14m/41p gold 0.64 Claude 0.07 c=0.64
- by subject: 1-10 Blended Literacy 11m/22p gold 0.46 Claude 0.00 c=0.46; 1-10 Social Science 3m/19p gold 0.86 Claude 0.00 c=0.86
- **BLL255** BLL255_1_0.html ↔ BLL255_1.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1']
- **BLL261** BLL261_1_0.html ↔ BLL261_1.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1']
- **BLL264** BLL264_1_0.html ↔ BLL264_1.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1']
- modules: BLL255, BLL261, BLL264, BLL265, BLL266, BLL271, BLL272, BLL273, BLL274, BLL275, BLL276, SSCI104, SSEA203, SSOG105

### F15 · MISSING `nav:crumbs` — CANDIDATE (pages 14 / modules 14)
- by template+ptype: Inquiry/lesson 7m/7p gold 1.00 Claude 0.00 c=1.00; Inquiry/overview 7m/7p gold 1.00 Claude 0.22 c=1.00
- by subject: ConnectED 8m/8p gold 1.00 Claude 0.00 c=1.00; 1-10 Blended Literacy 3m/3p gold 0.06 Claude 0.00 c=0.06; Te ara Whakapuawa -Wellbeing 3m/3p gold 1.00 Claude 0.40 c=1.00
- **BLL250** BLL250_2_5.html ↔ BLL250.html: gold ['nav:crumbs'] · Claude []
- **BLL260** BLL260_6_1.html ↔ BLL260.html: gold ['nav:crumbs'] · Claude []
- **BLL270** BLL270_2_0.html ↔ BLL270.html: gold ['nav:crumbs'] · Claude []
- modules: BLL250, BLL260, BLL270, CEDK401, CEDO201, CEDO402, CEDR101, CEDR203, CEDR401, CEDT102, CEDW303, TWHK902, TWHR905, TWHT903

### F16 · MISSING `footer:links=home-nav,prev-lesson,next-lesson` — CANDIDATE (pages 10 / modules 10)
- by template+ptype: Inquiry/lesson 5m/5p gold 0.71 Claude 0.00 c=0.71; Inquiry/overview 5m/5p gold 0.56 Claude 0.00 c=0.56
- by subject: ConnectED 5m/5p gold 0.62 Claude 0.00 c=0.62; 1-10 Blended Literacy 3m/3p gold 0.06 Claude 0.00 c=0.06; Te ara Whakapuawa -Wellbeing 2m/2p gold 0.40 Claude 0.00 c=0.40
- **BLL250** BLL250_2_5.html ↔ BLL250.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=home-nav,prev-lesson,next-lesson', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL260** BLL260_6_1.html ↔ BLL260.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=home-nav,prev-lesson,next-lesson', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL270** BLL270_2_0.html ↔ BLL270.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=home-nav,prev-lesson,next-lesson', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL250, BLL260, BLL270, CEDK401, CEDO201, CEDO402, CEDR101, CEDT102, TWHK902, TWHK907


## The ranked queue — chrome regions first, then by modules affected

| # | region | dir | parent | gold form | Claude form | pages | modules | consensus (all) | best group | derivable | KB | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | module-code | EXTRA | `div#header` | `—` | `div#module-code` | 3 | 3 | 0.06 of 115 | — | structure | yes | BELOW FLOOR |
| 2 | module-code | EXTRA | `div#module-code` | `—` | `h1` | 1 | 1 | 0.06 of 115 | — | structure | yes | BELOW FLOOR |
| 3 | module-code | MISSING | `div#header` | `div#module-code` | `—` | 1 | 1 | 0.94 of 115 | — | structure | yes | BELOW FLOOR |
| 4 | title | MISSING | `div#header` | `h1>span` | `—` | 24 | 6 | 0.37 of 115 | — | 0.71 | yes | BELOW FLOOR |
| 5 | title | MISSING | `span>span` | `span` | `—` | 9 | 5 | 0.08 of 115 | — | 1.00 | — | BELOW FLOOR |
| 6 | title | EXTRA | `div#header` | `—` | `h1>span` | 5 | 5 | 0.63 of 115 | — | structure | yes | BELOW FLOOR |
| 7 | title | SUBSTITUTED | `div#header` | `h1>span` | `div#module-code` | 1 | 1 | 1.00 of 115 | — | structure | yes | BELOW FLOOR |
| 8 | module-menu | EXTRA | `div.row` | `—` | `WIDGET` | 11 | 11 | 0.82 of 115 | subject=1-10 Blended Literacy c=0.92 n=11 | structure | — | CANDIDATE |
| 9 | module-menu | SUBSTITUTED | `div#module-menu-content.moduleMenu` | `WIDGET` | `div.row` | 11 | 11 | 0.10 of 115 | subject+ptype=1-10 Blended Literacy/overview c=0.73 n=11 | structure | yes | CANDIDATE |
| 10 | module-menu | MISSING | `div#header` | `div#module-head-buttons` | `—` | 11 | 6 | 0.79 of 115 | — | structure | yes | BELOW FLOOR |
| 11 | module-menu | EXTRA | `div.col-12.col-md-6.paddingL` | `—` | `p` | 5 | 5 | 0.99 of 115 | — | structure | yes | BELOW FLOOR |
| 12 | module-menu | EXTRA | `div.col-12.col-md-6.paddingL` | `—` | `ul` | 5 | 5 | 1.00 of 115 | — | structure | yes | BELOW FLOOR |
| 13 | module-menu | EXTRA | `div.col-12.col-md-6.paddingL` | `—` | `h5` | 4 | 4 | 1.00 of 115 | — | structure | yes | BELOW FLOOR |
| 14 | module-menu | MISSING | `div#header` | `div#module-menu-content.moduleMenu` | `—` | 4 | 4 | 0.73 of 115 | — | 1.00 | yes | BELOW FLOOR |
| 15 | module-menu | MISSING | `ul` | `li` | `—` | 4 | 4 | 0.23 of 115 | — | 1.00 | — | BELOW FLOOR |
| 16 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6.paddingL` | `—` | 4 | 4 | 0.09 of 115 | — | 1.00 | yes | BELOW FLOOR |
| 17 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingL` | `p` | `h5` | 4 | 4 | 0.08 of 115 | — | structure | yes | BELOW FLOOR |
| 18 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6.paddingR` | `—` | 3 | 3 | 0.03 of 115 | — | 1.00 | yes | BELOW FLOOR |
| 19 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `ul` | `—` | 3 | 3 | 0.06 of 115 | — | 1.00 | yes | BELOW FLOOR |
| 20 | module-menu | MISSING | `div.col-12.col-md-8` | `h5` | `—` | 13 | 2 | 0.20 of 115 | — | 0.96 | — | BELOW FLOOR |
| 21 | module-menu | MISSING | `div.col-12.col-md-8` | `ul` | `—` | 13 | 2 | 0.20 of 115 | — | 1.00 | — | BELOW FLOOR |
| 22 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6.offset-md-0` | `—` | 9 | 2 | 0.07 of 115 | — | 1.00 | yes | BELOW FLOOR |
| 23 | module-menu | MISSING | `div.col-12.col-md-8` | `p` | `—` | 4 | 2 | 0.07 of 115 | — | 0.00 | — | BELOW FLOOR |
| 24 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `h4>span` | `—` | 2 | 2 | 0.08 of 115 | — | 1.00 | yes | BELOW FLOOR |
| 25 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `p` | `—` | 2 | 2 | 0.03 of 115 | — | 0.75 | yes | BELOW FLOOR |
| 26 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.offset-md-0.paddingR` | `div.col-12.col-md-6.paddingR` | 2 | 2 | 0.02 of 115 | — | structure | yes | BELOW FLOOR |
| 27 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.offset-md-0.paddingL` | `div.col-12.col-md-6.paddingL` | 2 | 2 | 0.02 of 115 | — | structure | yes | BELOW FLOOR |
| 28 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.paddingR` | `div.col-12.col-md-8` | 2 | 2 | 0.11 of 115 | — | structure | yes | BELOW FLOOR |
| 29 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `—` | 8 | 1 | 0.07 of 115 | — | 1.00 | yes | BELOW FLOOR |
| 30 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0` | `ul` | `—` | 7 | 1 | 0.07 of 115 | — | 1.00 | yes | BELOW FLOOR |
| 31 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.offset-md-0` | `div.col-12.col-md-8` | 7 | 1 | 0.08 of 115 | — | structure | yes | BELOW FLOOR |
| 32 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-6.paddingR` | 1 | 1 | 0.97 of 115 | — | structure | yes | BELOW FLOOR |
| 33 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `p` | 1 | 1 | 0.97 of 115 | — | structure | yes | BELOW FLOOR |
| 34 | module-menu | EXTRA | `p>b` | `—` | `b` | 1 | 1 | 0.99 of 115 | — | structure | — | BELOW FLOOR |
| 35 | module-menu | EXTRA | `div.col-12.col-md-6.paddingL` | `—` | `p>b` | 1 | 1 | 0.99 of 115 | — | structure | yes | BELOW FLOOR |
| 36 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-6.offset-md-0` | 1 | 1 | 0.93 of 115 | — | structure | yes | BELOW FLOOR |
| 37 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `ul` | 1 | 1 | 0.94 of 115 | — | structure | yes | BELOW FLOOR |
| 38 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `h4>span` | 1 | 1 | 0.92 of 115 | — | structure | yes | BELOW FLOOR |
| 39 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-6.paddingL` | 1 | 1 | 0.91 of 115 | — | structure | yes | BELOW FLOOR |
| 40 | module-menu | EXTRA | `ul` | `—` | `li` | 1 | 1 | 0.75 of 115 | — | structure | — | BELOW FLOOR |
| 41 | module-menu | MISSING | `h5>span` | `span` | `—` | 1 | 1 | 0.03 of 115 | — | 1.00 | — | BELOW FLOOR |
| 42 | module-menu | MISSING | `li` | `i` | `—` | 1 | 1 | 0.01 of 115 | — | 1.00 | — | BELOW FLOOR |
| 43 | module-menu | MISSING | `h4>span` | `span` | `—` | 1 | 1 | 0.13 of 115 | — | 1.00 | — | BELOW FLOOR |
| 44 | module-menu | MISSING | `div.col-12.col-md-6` | `h4>span` | `—` | 1 | 1 | 0.01 of 115 | — | 1.00 | yes | BELOW FLOOR |
| 45 | module-menu | MISSING | `div.col-12.col-md-6` | `p` | `—` | 1 | 1 | 0.01 of 115 | — | 1.00 | yes | BELOW FLOOR |
| 46 | module-menu | MISSING | `div.col-12.col-md-6` | `ul` | `—` | 1 | 1 | 0.01 of 115 | — | 1.00 | yes | BELOW FLOOR |
| 47 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `p>b` | `—` | 1 | 1 | 0.01 of 115 | — | 1.00 | yes | BELOW FLOOR |
| 48 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `h3>span` | `—` | 1 | 1 | 0.02 of 115 | — | 1.00 | yes | BELOW FLOOR |
| 49 | module-menu | MISSING | `div.row` | `p` | `—` | 1 | 1 | 0.01 of 115 | — | 1.00 | — | BELOW FLOOR |
| 50 | module-menu | MOVED | `p` | `h5` | `h5` | 1 | 1 | 0.01 of 115 | — | structure | — | BELOW FLOOR |
| 51 | module-menu | MOVED | `div.col-12.col-md-6.paddingL` | `p` | `p` | 1 | 1 | 0.07 of 115 | — | structure | yes | BELOW FLOOR |
| 52 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `p` | `h5` | 1 | 1 | 0.09 of 115 | — | structure | yes | BELOW FLOOR |
| 53 | module-menu | SUBSTITUTED | `div#header` | `div#module-head-buttons` | `div.row` | 1 | 1 | 0.79 of 115 | — | structure | yes | BELOW FLOOR |
| 54 | module-menu | SUBSTITUTED | `div#module-head-buttons` | `div#module-menu-button.btn1.circle-button` | `div.col-12.col-md-8` | 1 | 1 | 0.79 of 115 | — | structure | yes | BELOW FLOOR |
| 55 | module-menu | SUBSTITUTED | `div#header` | `div#module-menu-content.moduleMenu` | `div.activity[number=*]` | 1 | 1 | 0.73 of 115 | — | structure | yes | BELOW FLOOR |
| 56 | module-menu | SUBSTITUTED | `div#module-menu-content.moduleMenu` | `div.row` | `div.row` | 1 | 1 | 0.64 of 115 | — | structure | yes | BELOW FLOOR |
| 57 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-12.paddingR` | `div.col-12` | 1 | 1 | 0.03 of 115 | — | structure | yes | BELOW FLOOR |
| 58 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `ul` | `p` | 1 | 1 | 0.11 of 115 | — | structure | yes | BELOW FLOOR |
| 59 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6` | `div.col-12.col-md-8` | 1 | 1 | 0.01 of 115 | — | structure | yes | BELOW FLOOR |
| 60 | module-menu | SUBSTITUTED | `div.col-12.col-md-6` | `p` | `p` | 1 | 1 | 0.01 of 115 | — | structure | yes | BELOW FLOOR |
| 61 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0.paddingL` | `p` | `h5` | 1 | 1 | 0.02 of 115 | — | structure | yes | BELOW FLOOR |
| 62 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0.paddingL` | `p` | `ul` | 1 | 1 | 0.02 of 115 | — | structure | yes | BELOW FLOOR |
| 63 | module-menu | SUBSTITUTED | `p` | `ul` | `li` | 1 | 1 | 0.01 of 115 | — | structure | — | BELOW FLOOR |
| 64 | module-menu | SUBSTITUTED | `ul` | `li` | `li` | 1 | 1 | 0.41 of 115 | — | structure | — | BELOW FLOOR |
| 65 | module-menu | SUBSTITUTED | `p` | `p` | `li` | 1 | 1 | 0.01 of 115 | — | structure | — | BELOW FLOOR |
| 66 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.paddingR` | `WIDGET` | 1 | 1 | 0.11 of 115 | — | structure | yes | BELOW FLOOR |
| 67 | module-menu | SUBSTITUTED | `div.row` | `p` | `WIDGET` | 1 | 1 | 0.01 of 115 | — | structure | — | BELOW FLOOR |
| 68 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `h5` | 1 | 1 | 0.07 of 115 | — | structure | yes | BELOW FLOOR |
| 69 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `p` | `h5` | 1 | 1 | 0.08 of 115 | — | structure | yes | BELOW FLOOR |
| 70 | module-menu | SUBSTITUTED | `ul` | `li` | `div.col-12` | 1 | 1 | 0.41 of 115 | — | structure | — | BELOW FLOOR |
| 71 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `p` | 1 | 1 | 0.07 of 115 | — | structure | yes | BELOW FLOOR |
| 72 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `div.col-12.col-md-6.paddingR` | 1 | 1 | 0.24 of 115 | — | structure | yes | BELOW FLOOR |
| 73 | module-menu | SUBSTITUTED | `div.col-12.col-md-8` | `div.row` | `h4>span` | 1 | 1 | 0.01 of 115 | — | structure | — | BELOW FLOOR |
| 74 | crumbs | MISSING | `div.crumbs` | `div` | `—` | 11 | 11 | 0.07 of 115 | — | 1.00 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 75 | crumbs | SUBSTITUTED | `div#body` | `div.crumbs` | `div.row` | 8 | 8 | 0.14 of 115 | — | structure | yes | BELOW FLOOR |
| 76 | crumbs | SUBSTITUTED | `div.crumbs` | `div.showing` | `div.col-12.col-md-8` | 8 | 8 | 0.14 of 115 | — | structure | yes | BELOW FLOOR |
| 77 | crumbs | SUBSTITUTED | `div.crumbs` | `div` | `div.row` | 2 | 2 | 0.14 of 115 | — | structure | yes | BELOW FLOOR |
| 78 | crumbs | SUBSTITUTED | `div.crumbs` | `div` | `div.col-12.col-md-8` | 2 | 2 | 0.14 of 115 | — | structure | yes | BELOW FLOOR |
| 79 | crumbs | SUBSTITUTED | `div.crumbs` | `div` | `div.ratio.ratio-16x9.videoSection` | 2 | 2 | 0.14 of 115 | — | structure | yes | BELOW FLOOR |
| 80 | crumbs | SUBSTITUTED | `div.crumbs` | `div` | `WIDGET` | 2 | 2 | 0.14 of 115 | — | structure | yes | BELOW FLOOR |
| 81 | crumbs | MISSING | `div` | `p` | `—` | 1 | 1 | 0.03 of 115 | — | 1.00 | — | BELOW FLOOR |
| 82 | crumbs | MISSING | `div.showing` | `p` | `—` | 1 | 1 | 0.14 of 115 | — | 1.00 | yes | BELOW FLOOR |
| 83 | crumbs | SUBSTITUTED | `div.crumbs` | `div` | `div.table-responsive` | 1 | 1 | 0.14 of 115 | — | structure | yes | BELOW FLOOR |
| 84 | crumbs | SUBSTITUTED | `div#body` | `div.crumbs` | `div.row.supervisor` | 1 | 1 | 0.14 of 115 | — | structure | yes | BELOW FLOOR |
| 85 | crumbs | SUBSTITUTED | `div.crumbs` | `div.showing` | `div.col-12.col-md-8.super-content-button` | 1 | 1 | 0.14 of 115 | — | structure | yes | BELOW FLOOR |
| 86 | crumbs | SUBSTITUTED | `div.crumbs` | `div` | `div.buttonD` | 1 | 1 | 0.14 of 115 | — | structure | yes | BELOW FLOOR |
| 87 | crumbs | SUBSTITUTED | `div` | `p` | `div.activity[number=*]` | 1 | 1 | 0.14 of 115 | — | structure | yes | BELOW FLOOR |
| 88 | crumbs | SUBSTITUTED | `div.crumbs` | `div` | `div.button` | 1 | 1 | 0.14 of 115 | — | structure | yes | BELOW FLOOR |
| 89 | crumbs | SUBSTITUTED | `div.crumbs` | `div` | `div.row.supervisor` | 1 | 1 | 0.14 of 115 | — | structure | yes | BELOW FLOOR |
| 90 | crumbs | SUBSTITUTED | `div` | `p` | `div.whakatauki` | 1 | 1 | 0.14 of 115 | — | structure | — | BELOW FLOOR |
| 91 | footer | MISSING | `ul.footer-nav.inquiry-nav` | `li>a.home-nav` | `—` | 7 | 7 | 0.50 of 115 | — | structure | yes | BELOW FLOOR |
| 92 | footer | MISSING | `ul.footer-nav.inquiry-nav` | `li>a#prev-lesson` | `—` | 6 | 6 | 0.33 of 115 | — | structure | yes | BELOW FLOOR |
| 93 | footer | EXTRA | `ul.footer-nav.inquiry-nav` | `—` | `li>a.home-nav` | 5 | 5 | 0.50 of 115 | — | structure | yes | BELOW FLOOR |
| 94 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav.inquiry-nav` | `ul.footer-nav` | 4 | 4 | 0.50 of 115 | — | structure | yes | BELOW FLOOR |
| 95 | footer | MISSING | `li>a.home-nav` | `a.home-nav` | `—` | 3 | 3 | 1.00 of 115 | — | structure | yes | BELOW FLOOR |
| 96 | footer | MISSING | `li>a#next-lesson` | `a#next-lesson` | `—` | 3 | 3 | 0.78 of 115 | — | structure | yes | BELOW FLOOR |
| 97 | footer | MISSING | `ul.footer-nav.inquiry-nav` | `li>a#next-lesson` | `—` | 3 | 3 | 0.36 of 115 | — | structure | yes | BELOW FLOOR |
| 98 | footer | SUBSTITUTED | `li>a#next-lesson` | `a#next-lesson` | `a.home-nav` | 3 | 3 | 0.78 of 115 | — | structure | yes | BELOW FLOOR |
| 99 | footer | EXTRA | `ul.footer-nav` | `—` | `li>a.home-nav` | 2 | 2 | 0.50 of 115 | — | structure | yes | BELOW FLOOR |
| 100 | footer | EXTRA | `li>a#prev-lesson` | `—` | `a#prev-lesson` | 2 | 2 | 0.24 of 115 | — | structure | yes | BELOW FLOOR |
| 112 | activity | EXTRA | `div.col-12` | `—` | `p` | 34 | 19 | 0.81 of 115 | template=Standard c=0.89 n=22 | structure | — | CANDIDATE |
| 113 | activity | EXTRA | `div.col-12` | `—` | `WIDGET` | 24 | 18 | 0.85 of 115 | era=Refresh c=0.85 n=24 | structure | — | CANDIDATE |
| 117 | activity | EXTRA | `div.col-12` | `—` | `img.img-fluid` | 21 | 13 | 0.96 of 115 | ptype=lesson c=0.98 n=21 | structure | — | CANDIDATE |
| 704 | body | EXTRA | `div#body` | `—` | `div.row` | 73 | 31 | 0.72 of 115 | subject=1-10 Blended Literacy c=1.00 n=27 | structure | — | CANDIDATE |
| 705 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 48 | 20 | 0.80 of 115 | template=Standard c=0.88 n=39 | structure | — | CANDIDATE |
| 706 | body | EXTRA | `div.col-12.col-md-8` | `—` | `WIDGET` | 39 | 20 | 0.90 of 115 | template=Standard c=0.90 n=29 | structure | — | CANDIDATE |
| 712 | body | EXTRA | `div.col-12.col-md-8` | `—` | `ul` | 25 | 14 | 0.83 of 115 | era=Refresh c=0.83 n=25 | structure | — | CANDIDATE |
| 714 | body | EXTRA | `div.col-12.col-md-8` | `—` | `h3` | 21 | 14 | 0.88 of 115 | era=Refresh c=0.88 n=21 | structure | — | CANDIDATE |
| 716 | body | EXTRA | `div.col-12.col-md-8` | `—` | `img.img-fluid` | 24 | 11 | 0.96 of 115 | ptype=lesson c=0.98 n=21 | structure | — | CANDIDATE |

## Details — in the companion file `CONVERTER_V2/outputs/_diff_queue_details.md`
Every CANDIDATE and every top-40 row has three quoted examples (WT / gold / Claude) there, plus the
below-floor list. **NEVER read the companion whole** (hundreds of KB): `grep -n '^### #<rank> ' CONVERTER_V2/outputs/_diff_queue_details.md` then `sed -n '<start>,<start+40>p'`. The top 25
candidates' detail blocks are repeated below for convenience.

### #8 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `WIDGET` — CANDIDATE
- pages 11 / modules 11 / lines 11; consensus (all) 0.82 of 115 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 11m/11p c=0.80
- by subject: 1-10 Blended Literacy 11m/11p c=0.92
- by era: Refresh 11m/11p c=0.82
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL255** BLL255_0_0.html ↔ BLL255_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **BLL257** BLL257_0_0.html ↔ BLL257_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **BLL261** BLL261_0_0.html ↔ BLL261_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- modules: BLL255, BLL257, BLL261, BLL264, BLL265, BLL266, BLL271, BLL272, BLL274, BLL275, BLL276

### #9 · module-menu · SUBSTITUTED · `div#module-menu-content.moduleMenu` › gold `WIDGET` vs Claude `div.row` — CANDIDATE
- pages 11 / modules 11 / lines 11; consensus (all) 0.10 of 115 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 11m/11p c=0.12
- by subject: 1-10 Blended Literacy 11m/11p c=0.23
- by era: Refresh 11m/11p c=0.10
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:45 — | Menu content class | `class="bg row"` | `class="moduleMenu"` |
  - KB: 06_TEMPLATE_RECOGNITION.md:94 — **Header:** `#module-code` → `<h1>` (module code or lesson number), then `<h1><span>Title</span></h1>`, then `#module-head-buttons` → `#module-menu-bu
  - KB: 10_CORPUS_VALIDATED_SCAFFOLDING.md:23 — - **Lesson pages → `simplified`** is dominant by a wide margin (plain `<h5>` label menu inside `#module-menu-content`). A minority of series ship **no
- **BLL255** BLL255_0_0.html ↔ BLL255_0.0.html (structure, derivable=True)
  - gold: `WIDGET`
  - Claude: `div.row`
- **BLL257** BLL257_0_0.html ↔ BLL257_0.0.html (structure, derivable=True)
  - gold: `WIDGET`
  - Claude: `div.row`
- **BLL261** BLL261_0_0.html ↔ BLL261_0.0.html (structure, derivable=True)
  - gold: `WIDGET`
  - Claude: `div.row`
- modules: BLL255, BLL257, BLL261, BLL264, BLL265, BLL266, BLL271, BLL272, BLL274, BLL275, BLL276

### #112 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `p` — CANDIDATE
- pages 34 / modules 19 / lines 97; consensus (all) 0.81 of 115 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 11m/22p c=0.89; Inquiry 7m/7p c=0.38; Bilingual 1m/5p c=0.67
- by subject: 1-10 Blended Literacy 8m/9p c=0.88; ConnectED 5m/5p c=0.38; 1-10 Social Science 2m/7p c=0.82; 1-10 Health and PE 1m/4p c=1.00; Te Marautanga o Aotearoa TMoA 1m/5p c=0.67; Te ara Whakapuawa -Wellbeing 1m/1p c=0.60
- by era: Refresh 19m/34p c=0.81
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL243** BLL243_1_1.html ↔ BLL243-2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «, or when»`
- **BLL247** BLL247_2_0.html ↔ BLL247_2_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «, the middle»`
- **BLL255** BLL255_1_0.html ↔ BLL255_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «. If you need to, re-watch the video to remind yourself what a homophone is and see how many you already know.»`
- modules: BLL243, BLL247, BLL255, BLL257, BLL264, BLL266, BLL270, BLL273, CEDK401, CEDO201, CEDR101, CEDR401, CEDT102, HPRE301, SSEA203, SSOG105, TRR110, TWHK907, XMES202

### #113 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `WIDGET` — CANDIDATE
- pages 24 / modules 18 / lines 44; consensus (all) 0.85 of 115 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 11m/13p c=0.90; Inquiry 6m/6p c=0.50; Bilingual 1m/5p c=1.00
- by subject: 1-10 Blended Literacy 9m/9p c=0.85; ConnectED 3m/3p c=0.50; 1-10 Social Science 2m/3p c=0.95; Online Safety (OS9000) 1m/1p c=1.00; Te Marautanga o Aotearoa TMoA 1m/5p c=1.00; Te ara Whakapuawa -Wellbeing 1m/1p c=0.80
- by era: Refresh 18m/24p c=0.85
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL243** BLL243_1_0.html ↔ BLL243-1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **BLL256** BLL256_2_0.html ↔ BLL256_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **BLL257** BLL257_2_0.html ↔ BLL257_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- modules: BLL243, BLL256, BLL257, BLL260, BLL264, BLL265, BLL270, BLL271, BLL276, CEDO402, CEDR101, CEDR203, OSSM501, SSCI104, SSEA203, TRR110, TWHK907, XMES202

### #117 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `img.img-fluid` — CANDIDATE
- pages 21 / modules 13 / lines 44; consensus (all) 0.96 of 115 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 12m/18p c=0.99; Bilingual 1m/3p c=1.00
- by subject: 1-10 Blended Literacy 9m/9p c=1.00; 1-10 Social Science 2m/8p c=0.95; 1-10 Health and PE 1m/1p c=1.00; Te Marautanga o Aotearoa TMoA 1m/3p c=1.00
- by era: Refresh 13m/21p c=0.96
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL243** BLL243_1_1.html ↔ BLL243-2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- **BLL247** BLL247_2_0.html ↔ BLL247_2_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- **BLL255** BLL255_2_0.html ↔ BLL255_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- modules: BLL243, BLL247, BLL255, BLL256, BLL257, BLL265, BLL266, BLL272, BLL273, HPRE301, SSEA203, SSOG105, TRR110

### #704 · body · EXTRA · `div#body` › gold `—` vs Claude `div.row` — CANDIDATE
- pages 73 / modules 31 / lines 305; consensus (all) 0.72 of 115 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 20m/59p c=0.67; Inquiry 10m/10p c=1.00; Bilingual 1m/4p c=0.83
- by subject: 1-10 Blended Literacy 16m/27p c=1.00; ConnectED 6m/6p c=1.00; 1-10 Social Science 3m/19p c=0.46; Te ara Whakapuawa -Wellbeing 2m/2p c=1.00; 1-10 Health and PE 1m/6p c=0.31; Online Safety (OS9000) 1m/4p c=0.17
- by era: Refresh 31m/73p c=0.72
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL243** BLL243_1_0.html ↔ BLL243-1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row`
- **BLL247** BLL247_1_0.html ↔ BLL247_1_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Choose the correct homophone so each sentence makes sense.»`
- **BLL250** BLL250_2_5.html ↔ BLL250.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Sorting the sounds»`
- modules: BLL243, BLL247, BLL250, BLL255, BLL256, BLL257, BLL260, BLL261, BLL264, BLL265, BLL266, BLL272, BLL273, BLL274, BLL275, BLL276, CEDK401, CEDO201, CEDR203, CEDR401, CEDT102, CEDW303, HPRE301, OSSM501 …

### #705 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `p` — CANDIDATE
- pages 48 / modules 20 / lines 167; consensus (all) 0.80 of 115 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 14m/39p c=0.88; Inquiry 5m/5p c=0.25; Bilingual 1m/4p c=1.00
- by subject: 1-10 Blended Literacy 8m/9p c=1.00; 1-10 Social Science 3m/13p c=0.77; Te ara Whakapuawa -Wellbeing 3m/3p c=0.20; ConnectED 2m/2p c=0.00; 1-10 Health and PE 1m/6p c=0.92; Online Safety (OS9000) 1m/5p c=0.67
- by era: Refresh 20m/48p c=0.80
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL247** BLL247_0_0.html ↔ BLL247_0_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «[AI animation script]»`
- **BLL257** BLL257_2_0.html ↔ BLL257_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Tom laughed. “It must have been very hungry, to try that while you were still eating!”»`
- **BLL261** BLL261_2_0.html ↔ BLL261_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «1.»`
- modules: BLL247, BLL257, BLL261, BLL264, BLL271, BLL272, BLL275, BLL276, CEDK401, CEDR401, HPRE301, OSSM501, SSCI104, SSEA203, SSOG105, TRR110, TWHK902, TWHK907, TWHR907, XMES202

### #706 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `WIDGET` — CANDIDATE
- pages 39 / modules 20 / lines 60; consensus (all) 0.90 of 115 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 12m/29p c=0.90; Inquiry 7m/7p c=0.81; Bilingual 1m/3p c=1.00
- by subject: 1-10 Blended Literacy 6m/7p c=1.00; ConnectED 4m/4p c=0.75; 1-10 Social Science 3m/9p c=0.91; Te ara Whakapuawa -Wellbeing 3m/3p c=0.80; 1-10 Health and PE 1m/5p c=0.54; Online Safety (OS9000) 1m/5p c=1.00
- by era: Refresh 20m/39p c=0.90
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL261** BLL261_1_0.html ↔ BLL261_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **BLL265** BLL265_2_0.html ↔ BLL265_2_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **BLL271** BLL271_1_0.html ↔ BLL271_1_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- modules: BLL261, BLL265, BLL271, BLL272, BLL273, BLL274, CEDR203, CEDR401, CEDT102, CEDW303, HPRE301, OSSM501, SSCI104, SSEA203, SSOG105, TRR110, TWHK907, TWHR907, TWHT903, XMES202

### #712 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `ul` — CANDIDATE
- pages 25 / modules 14 / lines 32; consensus (all) 0.83 of 115 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 7m/17p c=0.88; Inquiry 6m/6p c=0.50; Bilingual 1m/2p c=1.00
- by subject: 1-10 Blended Literacy 3m/3p c=1.00; ConnectED 3m/3p c=0.38; 1-10 Social Science 3m/7p c=0.82; Te ara Whakapuawa -Wellbeing 3m/3p c=0.40; 1-10 Health and PE 1m/7p c=0.61; Te Marautanga o Aotearoa TMoA 1m/2p c=1.00
- by era: Refresh 14m/25p c=0.83
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL247** BLL247_2_0.html ↔ BLL247_2_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul  «to help you remember what to say. Pictures and notes are helpful when we speak.»`
- **BLL265** BLL265_0_0.html ↔ BLL265_0_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul  «Written words are made up of letters and letter combinations (graphemes) that match to sounds (phonemes).»`
- **BLL266** BLL266_2_0.html ↔ BLL266_2_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul  «headings are circled in red»`
- modules: BLL247, BLL265, BLL266, CEDK401, CEDR101, CEDR401, HPRE301, SSCI104, SSEA203, SSOG105, TRR110, TWHK902, TWHK907, TWHT903

### #714 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `h3` — CANDIDATE
- pages 21 / modules 14 / lines 25; consensus (all) 0.88 of 115 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 10m/15p c=0.91; Inquiry 3m/3p c=0.62; Bilingual 1m/3p c=1.00
- by subject: 1-10 Blended Literacy 5m/5p c=1.00; 1-10 Social Science 2m/3p c=0.82; Te ara Whakapuawa -Wellbeing 2m/2p c=0.40; ConnectED 1m/1p c=0.62; 1-10 Health and PE 1m/4p c=0.77; Online Safety (OS9000) 1m/2p c=0.83
- by era: Refresh 14m/21p c=0.88
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL266** BLL266_0_0.html ↔ BLL266_0_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h3  «Introduction»`
- **BLL271** BLL271_1_0.html ↔ BLL271_1_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h3  «Three tricky sounds»`
- **BLL272** BLL272_1_0.html ↔ BLL272_1_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h3  «Help sheets»`
- modules: BLL266, BLL271, BLL272, BLL273, BLL275, CEDK401, HPRE301, OSSM501, SSCI104, SSEA203, TRR110, TWHK902, TWHT903, XMES202

### #716 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `img.img-fluid` — CANDIDATE
- pages 24 / modules 11 / lines 55; consensus (all) 0.96 of 115 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 6m/16p c=1.00; Inquiry 4m/4p c=0.69; Bilingual 1m/4p c=1.00
- by subject: 1-10 Social Science 3m/11p c=1.00; ConnectED 2m/2p c=0.50; Te ara Whakapuawa -Wellbeing 2m/2p c=0.80; 1-10 Blended Literacy 1m/1p c=1.00; Online Safety (OS9000) 1m/1p c=1.00; Te Marautanga o Aotearoa TMoA 1m/4p c=1.00
- by era: Refresh 11m/24p c=0.96
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL257** BLL257_2_0.html ↔ BLL257_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- **CEDK401** CEDK401_2_0.html ↔ CEDK401 Food Sustainability.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- **CEDR401** CEDR401_1_0.html ↔ CEDR401 Leadership and Information.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- modules: BLL257, CEDK401, CEDR401, OSSM501, SSCI104, SSEA203, SSOG105, TRR110, TWHK907, TWHR907, XMES202
