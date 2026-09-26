# DIFF_QUEUE.md — the diff miner's ranked class queue (LOOP__Autonomous_Rounds.md §1d)

**Produced:** 2026-09-26 16:58 NZST by `reference/tests/_diff_miner.py` on the CURRENT corpus (pageforge-site HEAD 3e4beab; Claude corpus 545 dirs). **Population:** the skeleton gate's own — 251 paired pages / 33 modules (compare_exclusions.txt honoured; acks / glossary / references pages excluded); parse errors skipped: 0 (must be 0); modules without a parsed WT: 1. Run time 9.7 s.

**What a row is.** One CLASS = (region, parent element, gold form, Claude form, direction) over every differing skeleton line of every paired page — the same lines, labels, widget collapse and difflib alignment the PRIMARY gate scores (each element its own line so it can be quoted). Direction: MISSING = gold has it, Claude lacks it; EXTRA = Claude has it, gold lacks it; SUBSTITUTED = same position, different tag / class / wrapper; MOVED = same text, different place. Consensus = of the gold pages in the group where the region exists, the share carrying the gold form (for EXTRA: the share NOT carrying Claude's form). Derivable = the gold line's text is in the module's parsed Writers Template (round-110 tolerance); structure-only differences are always derivable.

**Candidate rule (§1d).** modules ≥ 10 for a chrome class (module-code / title / header / module-menu / crumbs / phases-nav / footer / acks), pages ≥ 20 for a body / activity class; gold consensus ≥ 0.60 in at least one template or subject group that itself reaches the floor; structure-only or derivable share ≥ 0.60. A class below the floor is listed, never dropped. A CANDIDATE still goes through the PICK's KB-first check, the triangulation and the §3 corpus-wide measurement before any code — this table is the queue, not the verdict.

## Summary

- differing skeleton lines: 18247 — by direction {'EXTRA': 5824, 'SUBSTITUTED': 2142, 'MISSING': 9833, 'MOVED': 448}
- by region: {'title': 22, 'module-menu': 1019, 'footer': 215, 'acks': 106, 'activity': 5827, 'body': 10938, 'root': 120}
- classes: 1757 — CANDIDATE 14, below floor 1720, the rest below consensus / not derivable

## Completeness census — the repeating chrome (§1d item 4)

| region | pages with region | gold items | gold items in WT | Claude items | derivable misses | pages with misses | modules with misses | status |
|---|---|---|---|---|---|---|---|---|
| module-menu | 222 | 1945 | 1768 | 1681 | 335 | 120 | 21 | CANDIDATE (verify by eye — text presence, not position) |
| crumbs | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |
| phases-nav | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |
| footer | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |

- **module-menu** by template: Standard 21m/120p/335 misses
  - ENGC403 ENGC403_12_0.html: gold 18 items (18 in WT) / Claude 0 — 18 derivable misses, e.g. h5 «We are learning:» · li «about how to argue and discuss a point of view in a logical way»
  - ENGS302 ENGS302_4_0.html: gold 11 items (9 in WT) / Claude 0 — 9 derivable misses, e.g. h5 «Learning intentions» · p «We are learning about cinematography and how it contributes to storytelling in f»
  - ENGS101 ENGS101_1_0.html: gold 10 items (8 in WT) / Claude 0 — 8 derivable misses, e.g. h5 «Learning intentions» · p «We are learning:»
  - ENGC206 ENGC206_4_0.html: gold 7 items (7 in WT) / Claude 0 — 7 derivable misses, e.g. h5 «We are learning:» · li «to understand how recipes are structured»
- **crumbs** by template: 
- **phases-nav** by template: 
- **footer** by template: 

## Chrome facts — the header and footer as SETS per page (alignment-free; §1d items 2 + 4)

A fact is one thing a page's chrome has: `header:chip` (the `#module-code` div), `header:chip=module-code` / `=lesson-number` / `=lesson-number(00)`, `header:head-buttons`, `header:menu-content`, `header:title-h1-count=N`, `footer:present`, `footer:ul=<classes>`, `footer:link=prev-lesson` / `next-lesson` / `home-nav`, `footer:links=<order>`, `footer:inside-body`, `nav:crumbs`, `nav:phases`. MISSING = the gold page has the fact and Claude's does not; EXTRA the reverse. Consensus = the share of gold pages in the group that have (MISSING) / lack (EXTRA) the fact. Floor 10 modules.

| # | dir | fact | pages | modules | gold share (all) | consensus (all) | best group | status |
|---|---|---|---|---|---|---|---|---|
| F1 | MISSING | `header:title-h1-count=2` | 22 | 11 | 0.16 | 0.16 | ptype=overview c=0.88 n=10 | CANDIDATE |
| F2 | EXTRA | `header:title-h1-count=1` | 22 | 11 | 0.84 | 0.16 | ptype=overview c=0.88 n=10 | CANDIDATE |
| F3 | EXTRA | `header:chip=decimal-number` | 31 | 6 | 0.65 | 0.35 | — | BELOW FLOOR |
| F4 | MISSING | `header:chip=lesson-number` | 24 | 4 | 0.20 | 0.20 | — | BELOW FLOOR |
| F5 | MISSING | `header:chip=decimal-number` | 9 | 2 | 0.65 | 0.65 | — | BELOW FLOOR |
| F6 | EXTRA | `header:chip=lesson-number` | 9 | 2 | 0.20 | 0.81 | — | BELOW FLOOR |
| F7 | EXTRA | `header:menu-content` | 2 | 2 | 0.97 | 0.03 | — | BELOW FLOOR |
| F8 | EXTRA | `header:head-buttons` | 2 | 2 | 0.97 | 0.03 | — | BELOW FLOOR |
| F9 | MISSING | `header:chip=other` | 6 | 1 | 0.02 | 0.02 | — | BELOW FLOOR |
| F10 | MISSING | `header:chip=module-code` | 1 | 1 | 0.14 | 0.14 | — | BELOW FLOOR |
| F11 | MISSING | `footer:inside-body` | 15 | 10 | 0.06 | 0.06 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F12 | EXTRA | `footer:links=prev-lesson,home-nav` | 9 | 9 | 0.10 | 0.90 | — | BELOW FLOOR |
| F13 | EXTRA | `footer:links=prev-lesson,next-lesson,home-nav` | 33 | 7 | 0.62 | 0.38 | — | BELOW FLOOR |
| F14 | MISSING | `footer:links=home-nav,next-lesson` | 6 | 6 | 0.02 | 0.02 | — | BELOW FLOOR |
| F15 | EXTRA | `footer:links=next-lesson,home-nav` | 6 | 6 | 0.11 | 0.89 | — | BELOW FLOOR |
| F16 | MISSING | `footer:links=home-nav,prev-lesson,next-lesson` | 32 | 5 | 0.13 | 0.13 | — | BELOW FLOOR |
| F17 | MISSING | `footer:link=next-lesson` | 5 | 5 | 0.88 | 0.88 | — | BELOW FLOOR |
| F18 | MISSING | `footer:links=prev-lesson,next-lesson,home-nav` | 4 | 4 | 0.62 | 0.62 | — | BELOW FLOOR |
| F19 | MISSING | `footer:links=home-nav,prev-lesson` | 4 | 4 | 0.02 | 0.02 | — | BELOW FLOOR |
| F20 | MISSING | `footer:links=prev-lesson,home-nav` | 2 | 2 | 0.10 | 0.10 | — | BELOW FLOOR |
| F21 | EXTRA | `footer:link=next-lesson` | 2 | 2 | 0.88 | 0.12 | — | BELOW FLOOR |

### F1 · MISSING `header:title-h1-count=2` — CANDIDATE (pages 22 / modules 11)
- by template+ptype: Standard/overview 10m/10p gold 0.88 Claude 0.58 c=0.88; Standard/lesson 2m/12p gold 0.06 Claude 0.00 c=0.06
- by subject: 1-10 English 11m/22p gold 0.16 Claude 0.08 c=0.16
- **ENGC102** ENGC102_0_0.html ↔ ENGC102_0.0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ENGC301** ENGC301_0_0.html ↔ ENGC301_0.0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ENGC302** ENGC302_0_0.html ↔ ENGC302_0.0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: ENGC102, ENGC301, ENGC302, ENGC401, ENGC403, ENGR302, ENGS102, ENGS202, ENGS302, ENGS401, ENGS404

### F2 · EXTRA `header:title-h1-count=1` — CANDIDATE (pages 22 / modules 11)
- by template+ptype: Standard/overview 10m/10p gold 0.12 Claude 0.42 c=0.88; Standard/lesson 2m/12p gold 0.94 Claude 1.00 c=0.06
- by subject: 1-10 English 11m/22p gold 0.84 Claude 0.92 c=0.16
- **ENGC102** ENGC102_0_0.html ↔ ENGC102_0.0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ENGC301** ENGC301_0_0.html ↔ ENGC301_0.0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ENGC302** ENGC302_0_0.html ↔ ENGC302_0.0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: ENGC102, ENGC301, ENGC302, ENGC401, ENGC403, ENGR302, ENGS102, ENGS202, ENGS302, ENGS401, ENGS404


## The ranked queue — chrome regions first, then by modules affected

| # | region | dir | parent | gold form | Claude form | pages | modules | consensus (all) | best group | derivable | KB | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | title | MISSING | `div#header` | `h1>span` | `—` | 22 | 11 | 0.16 of 251 | ptype=overview c=0.88 n=10 | 0.86 | yes | CANDIDATE |
| 2 | module-menu | MISSING | `div.col-12.col-md-8` | `h5` | `—` | 59 | 13 | 0.69 of 251 | ptype=lesson c=0.80 n=13 | 0.69 | — | CANDIDATE |
| 3 | module-menu | MISSING | `ul` | `li` | `—` | 29 | 13 | 0.33 of 251 | — | 0.94 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 4 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `p` | `h5` | 10 | 10 | 0.06 of 251 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 5 | module-menu | MISSING | `div.col-12.col-md-8` | `ul` | `—` | 33 | 9 | 0.69 of 251 | — | 0.81 | — | BELOW FLOOR |
| 6 | module-menu | MISSING | `div.col-12.col-md-8` | `p` | `—` | 47 | 8 | 0.17 of 251 | — | 1.00 | — | BELOW FLOOR |
| 7 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-6.offset-md-0` | 6 | 6 | 0.94 of 251 | — | structure | yes | BELOW FLOOR |
| 8 | module-menu | EXTRA | `div.col-12.col-md-6.offset-md-0` | `—` | `p` | 5 | 5 | 0.98 of 251 | — | structure | yes | BELOW FLOOR |
| 9 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-6.paddingR` | 5 | 5 | 1.00 of 251 | — | structure | yes | BELOW FLOOR |
| 10 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6.offset-md-0` | `—` | 5 | 5 | 0.06 of 251 | — | 1.00 | yes | BELOW FLOOR |
| 11 | module-menu | SUBSTITUTED | `div.row` | `div.col-md-8` | `div.col-12.col-md-8` | 25 | 4 | 0.10 of 251 | — | structure | — | BELOW FLOOR |
| 12 | module-menu | EXTRA | `p>b` | `—` | `b` | 4 | 4 | 1.00 of 251 | — | structure | — | BELOW FLOOR |
| 13 | module-menu | SUBSTITUTED | `div#module-menu-content.moduleMenu` | `div.item` | `div.row` | 19 | 3 | 0.08 of 251 | — | structure | yes | BELOW FLOOR |
| 14 | module-menu | SUBSTITUTED | `div.item` | `div.row` | `div.col-12.col-md-8` | 19 | 3 | 0.08 of 251 | — | structure | yes | BELOW FLOOR |
| 15 | module-menu | SUBSTITUTED | `ul` | `li` | `li` | 17 | 3 | 0.88 of 251 | — | structure | — | BELOW FLOOR |
| 16 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `ul` | 16 | 3 | 0.31 of 251 | — | structure | — | BELOW FLOOR |
| 17 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `h5` | 16 | 3 | 0.70 of 251 | — | structure | — | BELOW FLOOR |
| 18 | module-menu | SUBSTITUTED | `div.col-12.col-md-8` | `ul` | `li` | 16 | 3 | 0.70 of 251 | — | structure | — | BELOW FLOOR |
| 19 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `h5` | 10 | 3 | 0.31 of 251 | — | structure | — | BELOW FLOOR |
| 20 | module-menu | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `h5` | 7 | 3 | 0.20 of 251 | — | structure | — | BELOW FLOOR |
| 21 | module-menu | EXTRA | `ul` | `—` | `li` | 5 | 3 | 0.67 of 251 | — | structure | — | BELOW FLOOR |
| 22 | module-menu | MISSING | `li>i` | `i` | `—` | 4 | 3 | 0.02 of 251 | — | 0.83 | — | BELOW FLOOR |
| 23 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `h5>span` | 3 | 3 | 1.00 of 251 | — | structure | yes | BELOW FLOOR |
| 24 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `p` | 3 | 3 | 1.00 of 251 | — | structure | yes | BELOW FLOOR |
| 25 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `h4>span` | `—` | 3 | 3 | 0.02 of 251 | — | 1.00 | yes | BELOW FLOOR |
| 26 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `—` | 3 | 3 | 0.03 of 251 | — | 1.00 | yes | BELOW FLOOR |
| 27 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-12` | `div.col-12.col-md-12.paddingR` | 3 | 3 | 0.01 of 251 | — | structure | yes | BELOW FLOOR |
| 28 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `h4>span` | `h5>span` | 3 | 3 | 0.02 of 251 | — | structure | yes | BELOW FLOOR |
| 29 | module-menu | MOVED | `div.col-12.col-md-8` | `h5` | `h5` | 7 | 2 | 0.69 of 251 | — | structure | — | BELOW FLOOR |
| 30 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `h5` | 6 | 2 | 0.06 of 251 | — | structure | yes | BELOW FLOOR |
| 31 | module-menu | EXTRA | `li>b` | `—` | `b` | 3 | 2 | 1.00 of 251 | — | structure | — | BELOW FLOOR |
| 32 | module-menu | EXTRA | `div.col-12.col-md-6.offset-md-0` | `—` | `p>b` | 2 | 2 | 1.00 of 251 | — | structure | yes | BELOW FLOOR |
| 33 | module-menu | EXTRA | `div.col-12.col-md-6.offset-md-0` | `—` | `ul` | 2 | 2 | 1.00 of 251 | — | structure | yes | BELOW FLOOR |
| 34 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `h5` | 2 | 2 | 1.00 of 251 | — | structure | yes | BELOW FLOOR |
| 35 | module-menu | EXTRA | `div#header` | `—` | `div#module-head-buttons` | 2 | 2 | 0.03 of 251 | — | structure | yes | BELOW FLOOR |
| 36 | module-menu | EXTRA | `div#header` | `—` | `div#module-menu-content.moduleMenu` | 2 | 2 | 0.03 of 251 | — | structure | yes | BELOW FLOOR |
| 37 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6.paddingL` | `—` | 2 | 2 | 0.02 of 251 | — | 1.00 | yes | BELOW FLOOR |
| 38 | module-menu | MISSING | `p` | `br` | `—` | 2 | 2 | 0.00 of 251 | — | structure | — | BELOW FLOOR |
| 39 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0` | `ul` | `—` | 2 | 2 | 0.02 of 251 | — | 1.00 | yes | BELOW FLOOR |
| 40 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0.paddingR` | `h3>span` | `—` | 2 | 2 | 0.01 of 251 | — | 1.00 | yes | BELOW FLOOR |
| 41 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `p` | `h5>span` | 2 | 2 | 0.02 of 251 | — | structure | yes | BELOW FLOOR |
| 42 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingL` | `p` | `h5` | 2 | 2 | 0.02 of 251 | — | structure | yes | BELOW FLOOR |
| 43 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.offset-md-0.paddingR` | `div.col-12.col-md-12.paddingR` | 2 | 2 | 0.01 of 251 | — | structure | yes | BELOW FLOOR |
| 44 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0.paddingR` | `h3>span` | `h4>span` | 2 | 2 | 0.01 of 251 | — | structure | yes | BELOW FLOOR |
| 45 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0.paddingL` | `p>b` | `h5` | 2 | 2 | 0.01 of 251 | — | structure | yes | BELOW FLOOR |
| 46 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0.paddingL` | `p` | `h5` | 2 | 2 | 0.01 of 251 | — | structure | yes | BELOW FLOOR |
| 47 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `ul` | `p` | 2 | 2 | 0.06 of 251 | — | structure | yes | BELOW FLOOR |
| 48 | module-menu | MISSING | `div.col-md-8` | `p` | `—` | 7 | 1 | 0.03 of 251 | — | 1.00 | — | BELOW FLOOR |
| 49 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0` | `p` | `—` | 4 | 1 | 0.05 of 251 | — | 1.00 | yes | BELOW FLOOR |
| 50 | module-menu | MISSING | `div.row` | `div.col-12.col-md-8` | `—` | 2 | 1 | 0.70 of 251 | — | 1.00 | — | BELOW FLOOR |
| 51 | module-menu | SUBSTITUTED | `div.col-12.col-md-8` | `h5` | `li` | 2 | 1 | 0.70 of 251 | — | structure | — | BELOW FLOOR |
| 52 | module-menu | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `ul` | 2 | 1 | 0.20 of 251 | — | structure | — | BELOW FLOOR |
| 53 | module-menu | EXTRA | `div.col-12.col-md-6.offset-md-0` | `—` | `h4>span` | 1 | 1 | 1.00 of 251 | — | structure | yes | BELOW FLOOR |
| 54 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 1 | 1 | 0.80 of 251 | — | structure | — | BELOW FLOOR |
| 55 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `ul` | 1 | 1 | 1.00 of 251 | — | structure | yes | BELOW FLOOR |
| 56 | module-menu | EXTRA | `div.col-12.col-md-6.offset-md-0` | `—` | `h3>span` | 1 | 1 | 0.94 of 251 | — | structure | yes | BELOW FLOOR |
| 57 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6.offset-md-0.paddingL` | `—` | 1 | 1 | 0.01 of 251 | — | 1.00 | yes | BELOW FLOOR |
| 58 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0.paddingL` | `p>b` | `—` | 1 | 1 | 0.01 of 251 | — | 1.00 | yes | BELOW FLOOR |
| 59 | module-menu | MISSING | `p>i` | `i` | `—` | 1 | 1 | 0.00 of 251 | — | 1.00 | — | BELOW FLOOR |
| 60 | module-menu | MISSING | `p>b` | `b` | `—` | 1 | 1 | 0.02 of 251 | — | 1.00 | — | BELOW FLOOR |
| 61 | module-menu | MISSING | `li>span` | `span>i` | `—` | 1 | 1 | 0.00 of 251 | — | 1.00 | — | BELOW FLOOR |
| 62 | module-menu | MISSING | `li` | `span>i` | `—` | 1 | 1 | 0.00 of 251 | — | 1.00 | — | BELOW FLOOR |
| 63 | module-menu | MISSING | `ul` | `li>i` | `—` | 1 | 1 | 0.02 of 251 | — | 1.00 | — | BELOW FLOOR |
| 64 | module-menu | MISSING | `div.row` | `WIDGET` | `—` | 1 | 1 | 0.08 of 251 | — | structure | — | BELOW FLOOR |
| 65 | module-menu | MOVED | `div.col-12.col-md-6.paddingR` | `p` | `p` | 1 | 1 | 0.01 of 251 | — | structure | yes | BELOW FLOOR |
| 66 | module-menu | MOVED | `div.col-12.col-md-6.paddingL` | `h5` | `h5` | 1 | 1 | 0.02 of 251 | — | structure | yes | BELOW FLOOR |
| 67 | module-menu | MOVED | `ul` | `li` | `li` | 1 | 1 | 0.33 of 251 | — | structure | — | BELOW FLOOR |
| 68 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `h5` | `p>b` | 1 | 1 | 0.03 of 251 | — | structure | yes | BELOW FLOOR |
| 69 | module-menu | SUBSTITUTED | `div.row` | `div.row` | `div.col-12.col-md-6.offset-md-0` | 1 | 1 | 0.00 of 251 | — | structure | yes | BELOW FLOOR |
| 70 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.paddingR` | `h4>span` | 1 | 1 | 0.02 of 251 | — | structure | yes | BELOW FLOOR |
| 71 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `ul` | `li` | 1 | 1 | 0.02 of 251 | — | structure | yes | BELOW FLOOR |
| 72 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `p` | `li` | 1 | 1 | 0.02 of 251 | — | structure | yes | BELOW FLOOR |
| 73 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.paddingL` | `h5` | 1 | 1 | 0.02 of 251 | — | structure | yes | BELOW FLOOR |
| 74 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingL` | `p` | `li` | 1 | 1 | 0.02 of 251 | — | structure | yes | BELOW FLOOR |
| 75 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingL` | `ul` | `li` | 1 | 1 | 0.02 of 251 | — | structure | yes | BELOW FLOOR |
| 76 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `p` | 1 | 1 | 0.70 of 251 | — | structure | — | BELOW FLOOR |
| 77 | module-menu | SUBSTITUTED | `div.col-12.col-md-8` | `h5` | `h5` | 1 | 1 | 0.70 of 251 | — | structure | — | BELOW FLOOR |
| 78 | module-menu | SUBSTITUTED | `div.col-12.col-md-8` | `ul` | `ul` | 1 | 1 | 0.70 of 251 | — | structure | — | BELOW FLOOR |
| 79 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `ul` | `p>b` | 1 | 1 | 0.06 of 251 | — | structure | yes | BELOW FLOOR |
| 80 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `h4>span` | `h5` | 1 | 1 | 0.02 of 251 | — | structure | yes | BELOW FLOOR |
| 81 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.paddingL` | `div.col-12.col-md-6.paddingR` | 1 | 1 | 0.02 of 251 | — | structure | yes | BELOW FLOOR |
| 82 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0.paddingR` | `h3>span` | `h5>span` | 1 | 1 | 0.01 of 251 | — | structure | yes | BELOW FLOOR |
| 83 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0.paddingR` | `ul` | `h5` | 1 | 1 | 0.01 of 251 | — | structure | yes | BELOW FLOOR |
| 84 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.offset-md-0.paddingL` | `div.col-12.col-md-6.paddingR` | 1 | 1 | 0.01 of 251 | — | structure | yes | BELOW FLOOR |
| 85 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.offset-md-0` | `div.col-12.col-md-12.paddingR` | 1 | 1 | 0.06 of 251 | — | structure | yes | BELOW FLOOR |
| 86 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `h4>span` | 1 | 1 | 0.06 of 251 | — | structure | yes | BELOW FLOOR |
| 87 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `h5>span` | 1 | 1 | 0.06 of 251 | — | structure | yes | BELOW FLOOR |
| 88 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.offset-md-0` | `div.col-12.col-md-6.paddingR` | 1 | 1 | 0.06 of 251 | — | structure | yes | BELOW FLOOR |
| 89 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `p>b` | `h5` | 1 | 1 | 0.01 of 251 | — | structure | yes | BELOW FLOOR |
| 90 | module-menu | SUBSTITUTED | `li>i` | `i` | `b` | 1 | 1 | 0.03 of 251 | — | structure | — | BELOW FLOOR |
| 91 | module-menu | SUBSTITUTED | `div#module-menu-content.moduleMenu` | `div.row` | `WIDGET` | 1 | 1 | 0.89 of 251 | — | structure | yes | BELOW FLOOR |
| 92 | footer | MISSING | `ul.footer-nav` | `li>a.home-nav` | `—` | 24 | 10 | 1.00 of 251 | template=Standard c=1.00 n=10 | structure | yes | CANDIDATE |
| 93 | footer | EXTRA | `ul.footer-nav` | `—` | `li>a.home-nav` | 40 | 7 | 0.00 of 251 | — | structure | yes | BELOW FLOOR |
| 94 | footer | EXTRA | `li>a#next-lesson` | `—` | `a#next-lesson` | 7 | 7 | 0.12 of 251 | — | structure | yes | BELOW FLOOR |
| 95 | footer | MISSING | `ul.footer-nav` | `li>a#next-lesson` | `—` | 7 | 7 | 0.88 of 251 | — | structure | yes | BELOW FLOOR |
| 96 | footer | MISSING | `ul.footer-nav` | `li>a#prev-lesson` | `—` | 16 | 5 | 0.87 of 251 | — | structure | yes | BELOW FLOOR |
| 97 | footer | EXTRA | `body.container-fluid` | `—` | `div#footer` | 6 | 5 | 0.13 of 251 | — | structure | yes | BELOW FLOOR |
| 98 | footer | SUBSTITUTED | `div#body` | `div#footer` | `div#footer` | 5 | 5 | 0.06 of 251 | — | structure | yes | BELOW FLOOR |
| 99 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav` | `ul.footer-nav` | 5 | 5 | 1.00 of 251 | — | structure | yes | BELOW FLOOR |
| 100 | footer | MISSING | `li>a.home-nav` | `a.home-nav` | `—` | 12 | 4 | 1.00 of 251 | — | structure | yes | BELOW FLOOR |
| 126 | activity | MISSING | `a` | `div.button` | `—` | 67 | 27 | 0.53 of 251 | ptype=lesson c=0.61 n=67 | 0.71 | yes | CANDIDATE |
| 127 | activity | EXTRA | `div.col-12` | `—` | `p` | 54 | 23 | 0.82 of 251 | template=Standard c=0.82 n=54 | structure | — | CANDIDATE |
| 129 | activity | EXTRA | `div.col-12` | `—` | `WIDGET` | 35 | 21 | 0.85 of 251 | template=Standard c=0.85 n=35 | structure | — | CANDIDATE |
| 135 | activity | EXTRA | `div.col-12` | `—` | `h4.goJournal` | 25 | 14 | 0.75 of 251 | template=Standard c=0.75 n=25 | structure | — | CANDIDATE |
| 142 | activity | SUBSTITUTED | `div.col-12` | `a` | `h4.goJournal` | 20 | 10 | 0.55 of 251 | ptype=lesson c=0.63 n=20 | structure | — | CANDIDATE |
| 673 | body | EXTRA | `div#body` | `—` | `div.row` | 148 | 33 | 0.63 of 251 | template=Standard c=0.63 n=148 | structure | — | CANDIDATE |
| 675 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 70 | 28 | 0.88 of 251 | template=Standard c=0.88 n=70 | structure | — | CANDIDATE |
| 677 | body | EXTRA | `div.col-12.col-md-8` | `—` | `WIDGET` | 33 | 20 | 0.80 of 251 | template=Standard c=0.80 n=33 | structure | — | CANDIDATE |
| 679 | body | EXTRA | `div.col-12.col-md-8` | `—` | `img.img-fluid` | 50 | 18 | 0.99 of 251 | template=Standard c=0.99 n=50 | structure | — | CANDIDATE |
| 684 | body | EXTRA | `div.col-12.col-md-8` | `—` | `ul` | 21 | 14 | 0.92 of 251 | template=Standard c=0.92 n=21 | structure | — | CANDIDATE |
| 1749 | root | EXTRA | `body.container-fluid` | `—` | `div.row` | 25 | 25 | 0.88 of 251 | template=Standard c=0.88 n=25 | structure | — | CANDIDATE |

## Details — in the companion file `CONVERTER_V2/outputs/_s52_engc_engs_engj_engr_miner_details.md`
Every CANDIDATE and every top-40 row has three quoted examples (WT / gold / Claude) there, plus the
below-floor list. **NEVER read the companion whole** (hundreds of KB): `grep -n '^### #<rank> ' CONVERTER_V2/outputs/_diff_queue_details.md` then `sed -n '<start>,<start+40>p'`. The top 25
candidates' detail blocks are repeated below for convenience.

### #1 · title · MISSING · `div#header` › gold `h1>span` vs Claude `—` — CANDIDATE
- pages 22 / modules 11 / lines 22; consensus (all) 0.16 of 251 gold pages with the region; derivable 0.86 (3 lines with no WT source)
- by template: Standard 11m/22p c=0.16
- by subject: 1-10 English 11m/22p c=0.16
- by era: Refresh 11m/22p c=0.16
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:94 — **Header:** `#module-code` → `<h1>` (module code or lesson number), then `<h1><span>Title</span></h1>`, then `#module-head-buttons` → `#module-menu-bu
  - KB: 00_MASTER_INSTRUCTIONS/00B_CONVERSION_PIPELINE.md:204 — - Lesson pages: use THAT LESSON'S OWN title in the header <h1><span> (never the module title) and the zero-padded lesson number (not the module code) 
  - KB: 00_MASTER_INSTRUCTIONS/00D_CONSTRAINTS_1.md:24 — 16. Lesson pages: zero-padded lesson number (e.g., `01`, `02`) in `#module-code`; **that lesson's own title** in `<h1><span>` — NOT the module title, 
- **ENGC102** ENGC102_0_0.html ↔ ENGC102_0.0.html (content, derivable=True)
  - gold: `h1  «Keeping it real»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [TITLE BAR]   [/RED TEXT]🔴 *KEEPING IT REAL*`
- **ENGC301** ENGC301_0_0.html ↔ ENGC301_0.0.html (content, derivable=False)
  - gold: `h1  «He Wā Ka Whakatairanga»`
  - Claude: `—`
- **ENGC302** ENGC302_0_0.html ↔ ENGC302_0.0.html (content, derivable=False)
  - gold: `h1  «Īmēra Mai»`
  - Claude: `—`
- modules: ENGC102, ENGC301, ENGC302, ENGC401, ENGC403, ENGR302, ENGS102, ENGS202, ENGS302, ENGS401, ENGS404

### #2 · module-menu · MISSING · `div.col-12.col-md-8` › gold `h5` vs Claude `—` — CANDIDATE
- pages 59 / modules 13 / lines 98; consensus (all) 0.69 of 251 gold pages with the region; derivable 0.69 (30 lines with no WT source)
- by template: Standard 13m/59p c=0.69
- by subject: 1-10 English 13m/59p c=0.69
- by era: Refresh 13m/59p c=0.69
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ENGC102** ENGC102_1_0.html ↔ ENGC102_1.0.html (content, derivable=True)
  - gold: `h5  «We are learning:»`
  - Claude: `—`
  - WT: `*We are learning to:*`
- **ENGC201** ENGC201_2_0.html ↔ ENGC201_2.0.html (content, derivable=True)
  - gold: `h5  «We are learning to:»`
  - Claude: `—`
  - WT: `*We are learning to:*`
- **ENGC202** ENGC202_1_0.html ↔ ENGC202_1.0.html (content, derivable=True)
  - gold: `h5  «We are learning to:»`
  - Claude: `—`
  - WT: `*We are learning to:*`
- modules: ENGC102, ENGC201, ENGC202, ENGC206, ENGC403, ENGJ302, ENGJ402, ENGJ403, ENGR102, ENGR202, ENGS101, ENGS302, ENGS404

### #92 · footer · MISSING · `ul.footer-nav` › gold `li>a.home-nav` vs Claude `—` — CANDIDATE
- pages 24 / modules 10 / lines 24; consensus (all) 1.00 of 251 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 10m/24p c=1.00
- by subject: 1-10 English 10m/24p c=1.00
- by era: Refresh 10m/24p c=1.00
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:40 — | Footer tag | `<nav id="module-foot">` with `<button>` + FA icons | `<div id="footer">` with `<ul class="footer-nav">` |
  - KB: 06_TEMPLATE_RECOGNITION.md:64 — | Footer `<ul>` class | `footer-nav` | `footer-nav` | `footer-nav fundamentals-nav` | `footer-nav inquiry-nav` | `footer-nav` |
  - KB: 06_TEMPLATE_RECOGNITION.md:114 — **Footer:** `<ul class="footer-nav">` with prev + next + home links.
- **ENGC403** ENGC403_12_0.html ↔ ENGC403_9_0.html (structure, derivable=True)
  - gold: `li`
  - Claude: `—`
- **ENGJ101** ENGJ101_1_0.html ↔ ENGJ101_1.0.html (structure, derivable=True)
  - gold: `li`
  - Claude: `—`
- **ENGJ201** ENGJ201_4_0.html ↔ ENGJ201_4.0.html (structure, derivable=True)
  - gold: `li`
  - Claude: `—`
- modules: ENGC403, ENGJ101, ENGJ201, ENGJ301, ENGJ302, ENGJ402, ENGJ403, ENGR102, ENGR302, ENGS302

### #126 · activity · MISSING · `a` › gold `div.button` vs Claude `—` — CANDIDATE
- pages 67 / modules 27 / lines 82; consensus (all) 0.53 of 251 gold pages with the region; derivable 0.71 (24 lines with no WT source)
- by template: Standard 27m/67p c=0.53
- by subject: 1-10 English 27m/67p c=0.53
- by era: Refresh 27m/67p c=0.53
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: INDEX.md:84 — - **`05_COMP_LANGUAGE_MEDIA_LAYOUT/05D_COMP14_BUTTONS_TABLES_COLUMNS.md`** (21 KB) — COMP_14 Layout & Structure, second half: Buttons (incl. the "Go t
  - KB: INDEX.md:85 — - Sections: Buttons (MTK Quiz — the activity shell `[MTKquiz]` builds) · Supervisor Button (Shape A/B/C · the reveal panel · edge cases) · Tables · Co
  - KB: _project_instructions_.md:28 — - **`ASSESSMENT MODE`** phrase (any capitalisation), **or** an uploaded `.docx` that is an **NCEA Assessment Activity** document (details table `Activ
- **ENGC101** ENGC101_2_0.html ↔ ENGC101_2.0.html (content, derivable=True)
  - gold: `div.button  «Go to journal»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [Button]  [/RED TEXT]🔴Go to journal`
- **ENGC102** ENGC102_2_0.html ↔ ENGC102_2.0.html (content, derivable=True)
  - gold: `div.button  «Go to journal»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [Button] [/RED TEXT]🔴 Go to journal`
- **ENGC201** ENGC201_6_0.html ↔ ENGC201_6.0.html (content, derivable=True)
  - gold: `div.button  «Go to journal»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [link to journal]  [/RED TEXT]🔴Go to journal https://docs.google.com/document/d/1nSQ-mwdxDYhLiBvhXpHFsNjqoN5xrJXDtY85-ItndMw/edit?usp=sharing`
- modules: ENGC101, ENGC102, ENGC201, ENGC202, ENGC204, ENGC206, ENGC301, ENGC302, ENGC401, ENGC403, ENGJ101, ENGJ102, ENGJ201, ENGJ202, ENGJ301, ENGJ402, ENGJ403, ENGR101, ENGR102, ENGR201, ENGR302, ENGS101, ENGS102, ENGS201 …

### #127 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `p` — CANDIDATE
- pages 54 / modules 23 / lines 169; consensus (all) 0.82 of 251 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 23m/54p c=0.82
- by subject: 1-10 English 23m/54p c=0.82
- by era: Refresh 23m/54p c=0.82
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ENGC101** ENGC101_1_0.html ↔ ENGC101_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «In the video in the introduction, you saw some different of communication. When we talk about means, we are talking abou»`
- **ENGC102** ENGC102_1_0.html ↔ ENGC102_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Read each of these cards and then drag them into the correct column to show that they would come from a fiction book or »`
- **ENGC202** ENGC202_1_0.html ↔ ENGC202_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «What to do:»`
- modules: ENGC101, ENGC102, ENGC202, ENGC204, ENGC206, ENGC301, ENGC401, ENGC403, ENGJ101, ENGJ102, ENGJ301, ENGJ302, ENGJ402, ENGJ403, ENGR102, ENGR201, ENGS102, ENGS201, ENGS202, ENGS301, ENGS302, ENGS401, ENGS404

### #129 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `WIDGET` — CANDIDATE
- pages 35 / modules 21 / lines 50; consensus (all) 0.85 of 251 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 21m/35p c=0.85
- by subject: 1-10 English 21m/35p c=0.85
- by era: Refresh 21m/35p c=0.85
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ENGC101** ENGC101_4_0.html ↔ ENGC101_4.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **ENGC102** ENGC102_1_0.html ↔ ENGC102_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **ENGC202** ENGC202_7_0.html ↔ ENGC202_7.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- modules: ENGC101, ENGC102, ENGC202, ENGC301, ENGC403, ENGJ102, ENGJ202, ENGJ301, ENGJ302, ENGR101, ENGR102, ENGR201, ENGR301, ENGR302, ENGS101, ENGS201, ENGS202, ENGS301, ENGS302, ENGS401, ENGS404

### #135 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `h4.goJournal` — CANDIDATE
- pages 25 / modules 14 / lines 29; consensus (all) 0.75 of 251 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 14m/25p c=0.75
- by subject: 1-10 English 14m/25p c=0.75
- by era: Refresh 14m/25p c=0.75
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ENGC101** ENGC101_5_0.html ↔ ENGC101_5.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h4.goJournal  «Go to your journal»`
- **ENGC102** ENGC102_4_0.html ↔ ENGC102_4.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h4.goJournal  «Go to your journal»`
- **ENGC202** ENGC202_4_0.html ↔ ENGC202_4.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h4.goJournal  «Go to your journal»`
- modules: ENGC101, ENGC102, ENGC202, ENGC401, ENGJ101, ENGJ102, ENGJ202, ENGJ301, ENGJ402, ENGR101, ENGR201, ENGS101, ENGS201, ENGS202

### #142 · activity · SUBSTITUTED · `div.col-12` › gold `a` vs Claude `h4.goJournal` — CANDIDATE
- pages 20 / modules 10 / lines 22; consensus (all) 0.55 of 251 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 10m/20p c=0.55
- by subject: 1-10 English 10m/20p c=0.55
- by era: Refresh 10m/20p c=0.55
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ENGC101** ENGC101_2_0.html ↔ ENGC101_2.0.html (structure, derivable=True)
  - gold: `a  «Go to journal»`
  - Claude: `h4.goJournal  «Go to your journal»`
- **ENGC102** ENGC102_3_0.html ↔ ENGC102_3.0.html (structure, derivable=True)
  - gold: `a  «Go to journal»`
  - Claude: `h4.goJournal  «Go to your journal»`
- **ENGC202** ENGC202_3_0.html ↔ ENGC202_3.0.html (structure, derivable=True)
  - gold: `a  «Go to journal»`
  - Claude: `h4.goJournal  «Go to your journal»`
- modules: ENGC101, ENGC102, ENGC202, ENGJ101, ENGJ201, ENGR101, ENGR201, ENGR202, ENGS201, ENGS202

### #673 · body · EXTRA · `div#body` › gold `—` vs Claude `div.row` — CANDIDATE
- pages 148 / modules 33 / lines 434; consensus (all) 0.63 of 251 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 33m/148p c=0.63
- by subject: 1-10 English 33m/148p c=0.63
- by era: Refresh 33m/148p c=0.63
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ENGC101** ENGC101_0_0.html ↔ ENGC101_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «He waka eke noa.»`
- **ENGC102** ENGC102_1_0.html ↔ ENGC102_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Go to your journal to complete some fiction versus nonfiction activities.»`
- **ENGC201** ENGC201_0_0.html ↔ ENGC201_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Ko te reo me ōna tikanga te hā o te whakawhitiwhiti kōrero.»`
- modules: ENGC101, ENGC102, ENGC201, ENGC202, ENGC204, ENGC206, ENGC301, ENGC302, ENGC401, ENGC403, ENGJ101, ENGJ102, ENGJ201, ENGJ202, ENGJ301, ENGJ302, ENGJ402, ENGJ403, ENGR101, ENGR102, ENGR201, ENGR202, ENGR301, ENGR302 …

### #675 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `p` — CANDIDATE
- pages 70 / modules 28 / lines 270; consensus (all) 0.88 of 251 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 28m/70p c=0.88
- by subject: 1-10 English 28m/70p c=0.88
- by era: Refresh 28m/70p c=0.88
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ENGC101** ENGC101_0_0.html ↔ ENGC101_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Welcome to our exciting online module all about how we talk and share ideas. We're going to discover different ways peop»`
- **ENGC201** ENGC201_1_0.html ↔ ENGC201_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Our faces are the best indicators to other people of how we are feeling. Scroll through the images to see how we may sho»`
- **ENGC202** ENGC202_0_0.html ↔ ENGC202_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Can you help each contestant to write the clearest, most easy to follow instructions so that they can take home the vict»`
- modules: ENGC101, ENGC201, ENGC202, ENGC204, ENGC206, ENGC301, ENGC302, ENGC401, ENGC403, ENGJ101, ENGJ201, ENGJ202, ENGJ301, ENGJ302, ENGJ402, ENGJ403, ENGR101, ENGR102, ENGR201, ENGR202, ENGR301, ENGR302, ENGS101, ENGS201 …

### #677 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `WIDGET` — CANDIDATE
- pages 33 / modules 20 / lines 55; consensus (all) 0.80 of 251 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 20m/33p c=0.80
- by subject: 1-10 English 20m/33p c=0.80
- by era: Refresh 20m/33p c=0.80
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ENGC101** ENGC101_2_0.html ↔ ENGC101_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **ENGC202** ENGC202_1_0.html ↔ ENGC202_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **ENGC204** ENGC204_5_0.html ↔ ENGC204_5_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- modules: ENGC101, ENGC202, ENGC204, ENGC302, ENGC403, ENGJ101, ENGJ201, ENGJ202, ENGJ301, ENGJ302, ENGJ402, ENGR101, ENGR202, ENGR301, ENGR302, ENGS101, ENGS202, ENGS401, ENGS404, ENGS405

### #679 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `img.img-fluid` — CANDIDATE
- pages 50 / modules 18 / lines 64; consensus (all) 0.99 of 251 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 18m/50p c=0.99
- by subject: 1-10 English 18m/50p c=0.99
- by era: Refresh 18m/50p c=0.99
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ENGC101** ENGC101_2_0.html ↔ ENGC101_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- **ENGC206** ENGC206_5_0.html ↔ ENGC206_3_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- **ENGC401** ENGC401_1_0.html ↔ ENGC401_0.1.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- modules: ENGC101, ENGC206, ENGC401, ENGC403, ENGJ202, ENGJ402, ENGJ403, ENGR101, ENGR102, ENGR202, ENGR301, ENGS101, ENGS102, ENGS201, ENGS301, ENGS302, ENGS401, ENGS404

### #684 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `ul` — CANDIDATE
- pages 21 / modules 14 / lines 48; consensus (all) 0.92 of 251 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 14m/21p c=0.92
- by subject: 1-10 English 14m/21p c=0.92
- by era: Refresh 14m/21p c=0.92
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ENGC101** ENGC101_4_0.html ↔ ENGC101_4.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul  «Have you seen these symbols anywhere?»`
- **ENGC204** ENGC204_1_0.html ↔ ENGC204_1_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul  «be in the wrong order»`
- **ENGC206** ENGC206_1_0.html ↔ ENGC206_1_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul  «pan → pan (1)»`
- modules: ENGC101, ENGC204, ENGC206, ENGC301, ENGC403, ENGJ202, ENGJ302, ENGJ402, ENGR101, ENGR202, ENGR301, ENGS101, ENGS302, ENGS404

### #1749 · root · EXTRA · `body.container-fluid` › gold `—` vs Claude `div.row` — CANDIDATE
- pages 25 / modules 25 / lines 25; consensus (all) 0.88 of 251 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 25m/25p c=0.88
- by subject: 1-10 English 25m/25p c=0.88
- by era: Refresh 25m/25p c=0.88
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ENGC101** ENGC101_0_0.html ↔ ENGC101_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row`
- **ENGC102** ENGC102_0_0.html ↔ ENGC102_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row`
- **ENGC201** ENGC201_0_0.html ↔ ENGC201_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row`
- modules: ENGC101, ENGC102, ENGC201, ENGC202, ENGC301, ENGC302, ENGC401, ENGJ101, ENGJ102, ENGJ201, ENGJ202, ENGJ301, ENGJ302, ENGJ402, ENGR101, ENGR102, ENGR201, ENGR202, ENGR301, ENGR302, ENGS101, ENGS102, ENGS201, ENGS301 …
