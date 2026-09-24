# DIFF_QUEUE.md — the diff miner's ranked class queue (LOOP__Autonomous_Rounds.md §1d)

**Produced:** 2026-09-24 16:22 NZST by `reference/tests/_diff_miner.py` on the CURRENT corpus (pageforge-site HEAD 68a9ac9; Claude corpus 545 dirs). **Population:** the skeleton gate's own — 148 paired pages / 54 modules (compare_exclusions.txt honoured; acks / glossary / references pages excluded); parse errors skipped: 0 (must be 0); modules without a parsed WT: 0. Run time 9.3 s.

**What a row is.** One CLASS = (region, parent element, gold form, Claude form, direction) over every differing skeleton line of every paired page — the same lines, labels, widget collapse and difflib alignment the PRIMARY gate scores (each element its own line so it can be quoted). Direction: MISSING = gold has it, Claude lacks it; EXTRA = Claude has it, gold lacks it; SUBSTITUTED = same position, different tag / class / wrapper; MOVED = same text, different place. Consensus = of the gold pages in the group where the region exists, the share carrying the gold form (for EXTRA: the share NOT carrying Claude's form). Derivable = the gold line's text is in the module's parsed Writers Template (round-110 tolerance); structure-only differences are always derivable.

**Candidate rule (§1d).** modules ≥ 10 for a chrome class (module-code / title / header / module-menu / crumbs / phases-nav / footer / acks), pages ≥ 20 for a body / activity class; gold consensus ≥ 0.60 in at least one template or subject group that itself reaches the floor; structure-only or derivable share ≥ 0.60. A class below the floor is listed, never dropped. A CANDIDATE still goes through the PICK's KB-first check, the triangulation and the §3 corpus-wide measurement before any code — this table is the queue, not the verdict.

## Summary

- differing skeleton lines: 14575 — by direction {'SUBSTITUTED': 1871, 'MISSING': 8627, 'EXTRA': 3650, 'MOVED': 427}
- by region: {'title': 14, 'header': 2, 'module-menu': 232, 'footer': 224, 'acks': 106, 'activity': 10132, 'body': 3805, 'root': 60}
- classes: 1120 — CANDIDATE 16, below floor 1088, the rest below consensus / not derivable

## Completeness census — the repeating chrome (§1d item 4)

| region | pages with region | gold items | gold items in WT | Claude items | derivable misses | pages with misses | modules with misses | status |
|---|---|---|---|---|---|---|---|---|
| module-menu | 39 | 1104 | 1067 | 1070 | 13 | 7 | 7 | BELOW FLOOR |
| crumbs | 7 | 49 | 48 | 49 | 2 | 2 | 2 | BELOW FLOOR |
| phases-nav | 0 | 0 | 0 | 0 | 0 | 0 | 0 | BELOW FLOOR |
| footer | 8 | 36 | 20 | 0 | 20 | 8 | 6 | BELOW FLOOR |

- **module-menu** by template: Inquiry 2m/2p/3 misses; Standard 5m/5p/10 misses
  - BLL270 BLL270_0_0.html: gold 36 items (36 in WT) / Claude 35 — 2 derivable misses, e.g. h4 «Tirohanga Whānui | Overview» · span «Tirohanga Whānui | Overview»
  - BLL214 BLL214_0_0.html: gold 27 items (25 in WT) / Claude 28 — 2 derivable misses, e.g. h5 «Success Criteria» · p «I can:»
  - BLL233 BLL233_0_0.html: gold 27 items (24 in WT) / Claude 27 — 2 derivable misses, e.g. h4 «Tirohanga Whānui | Overview» · span «Tirohanga Whānui | Overview»
  - BLL246 BLL246_0_0.html: gold 46 items (46 in WT) / Claude 45 — 2 derivable misses, e.g. h4 «Tirohanga Whānui | Overview» · span «Tirohanga Whānui | Overview»
- **crumbs** by template: Inquiry 2m/2p/2 misses
  - BLL240 BLL240_0_0.html: gold 8 items (8 in WT) / Claude 8 — 1 derivable misses, e.g. p «air»
  - BLL270 BLL270_0_0.html: gold 5 items (5 in WT) / Claude 5 — 1 derivable misses, e.g. p «Blended vowels»
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
| F1 | MISSING | `header:chip=module-code` | 8 | 8 | 0.10 | 0.10 | — | BELOW FLOOR |
| F2 | EXTRA | `header:chip=other` | 8 | 8 | 0.28 | 0.72 | — | BELOW FLOOR |
| F3 | MISSING | `header:title-h1-count=1` | 6 | 6 | 0.99 | 0.99 | — | BELOW FLOOR |
| F4 | EXTRA | `header:title-h1-count=2` | 6 | 6 | 0.01 | 0.99 | — | BELOW FLOOR |
| F5 | EXTRA | `header:chip=decimal-number` | 6 | 3 | 0.43 | 0.57 | — | BELOW FLOOR |
| F6 | MISSING | `header:head-buttons` | 4 | 2 | 0.42 | 0.42 | — | BELOW FLOOR |
| F7 | MISSING | `header:chip=lesson-number` | 4 | 2 | 0.19 | 0.19 | — | BELOW FLOOR |
| F8 | MISSING | `header:chip=other` | 2 | 1 | 0.28 | 0.28 | — | BELOW FLOOR |
| F9 | MISSING | `footer:inside-body` | 27 | 19 | 0.18 | 0.18 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F10 | EXTRA | `footer:links=prev-lesson,home-nav` | 12 | 12 | 0.24 | 0.76 | era=Refresh c=0.76 n=12 | CANDIDATE |
| F11 | MISSING | `footer:link=next-lesson` | 11 | 11 | 0.76 | 0.76 | era=Refresh c=0.76 n=11 | CANDIDATE |
| F12 | MISSING | `footer:links=prev-lesson,next-lesson,home-nav` | 11 | 11 | 0.39 | 0.39 | ptype=lesson c=0.62 n=11 | CANDIDATE |
| F13 | MISSING | `footer:links=home-nav,prev-lesson,next-lesson` | 7 | 7 | 0.05 | 0.05 | — | BELOW FLOOR |
| F14 | EXTRA | `footer:links=prev-lesson,next-lesson,home-nav` | 7 | 7 | 0.39 | 0.61 | — | BELOW FLOOR |
| F15 | MISSING | `footer:ul=footer-nav` | 18 | 6 | 0.12 | 0.12 | — | BELOW FLOOR |
| F16 | EXTRA | `footer:ul=footer-nav inquiry-nav` | 18 | 6 | 0.88 | 0.12 | — | BELOW FLOOR |
| F17 | MISSING | `footer:link=other` | 1 | 1 | 0.01 | 0.01 | — | BELOW FLOOR |
| F18 | MISSING | `footer:links=other,home-nav` | 1 | 1 | 0.01 | 0.01 | — | BELOW FLOOR |
| F19 | EXTRA | `footer:link=prev-lesson` | 1 | 1 | 0.68 | 0.32 | — | BELOW FLOOR |

### F10 · EXTRA `footer:links=prev-lesson,home-nav` — CANDIDATE (pages 12 / modules 12)
- by template+ptype: Standard/lesson 12m/12p gold 0.37 Claude 0.50 c=0.63
- by subject: 1-10 Blended Literacy 12m/12p gold 0.24 Claude 0.32 c=0.76
- **BLL224** BLL224_2_0.html ↔ BLL224-2.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL225** BLL225_2_0.html ↔ BLL225-2.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL226** BLL226_2_0.html ↔ BLL226-2.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL224, BLL225, BLL226, BLL227, BLL231, BLL234, BLL236, BLL237, BLL266, BLL271, BLL274, BLL276

### F11 · MISSING `footer:link=next-lesson` — CANDIDATE (pages 11 / modules 11)
- by template+ptype: Standard/lesson 11m/11p gold 0.62 Claude 0.50 c=0.62
- by subject: 1-10 Blended Literacy 11m/11p gold 0.76 Claude 0.68 c=0.76
- **BLL224** BLL224_2_0.html ↔ BLL224-2.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL225** BLL225_2_0.html ↔ BLL225-2.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL226** BLL226_2_0.html ↔ BLL226-2.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL224, BLL225, BLL226, BLL227, BLL231, BLL234, BLL236, BLL237, BLL266, BLL274, BLL276

### F12 · MISSING `footer:links=prev-lesson,next-lesson,home-nav` — CANDIDATE (pages 11 / modules 11)
- by template+ptype: Standard/lesson 11m/11p gold 0.62 Claude 0.50 c=0.62
- by subject: 1-10 Blended Literacy 11m/11p gold 0.39 Claude 0.36 c=0.39
- **BLL224** BLL224_2_0.html ↔ BLL224-2.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL225** BLL225_2_0.html ↔ BLL225-2.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL226** BLL226_2_0.html ↔ BLL226-2.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL224, BLL225, BLL226, BLL227, BLL231, BLL234, BLL236, BLL237, BLL266, BLL274, BLL276


## The ranked queue — chrome regions first, then by modules affected

| # | region | dir | parent | gold form | Claude form | pages | modules | consensus (all) | best group | derivable | KB | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | title | EXTRA | `div#header` | `—` | `h1>span` | 6 | 6 | 0.99 of 148 | — | structure | yes | BELOW FLOOR |
| 2 | title | MISSING | `span>span` | `span` | `—` | 6 | 2 | 0.09 of 148 | — | 1.00 | — | BELOW FLOOR |
| 3 | title | MISSING | `div.titlebar` | `h1.moduleTitle>span.module-subtitle.text-lowercase` | `—` | 2 | 1 | 0.01 of 148 | — | 1.00 | — | BELOW FLOOR |
| 4 | header | SUBSTITUTED | `div#header` | `div.titlebar` | `h1>span` | 2 | 1 | 0.01 of 148 | — | structure | yes | BELOW FLOOR |
| 5 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `p` | `h5` | 30 | 30 | 0.21 of 148 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 6 | module-menu | EXTRA | `div.row` | `—` | `WIDGET` | 12 | 12 | 0.95 of 148 | template=Standard c=0.96 n=12 | structure | — | CANDIDATE |
| 7 | module-menu | SUBSTITUTED | `div#module-menu-content.moduleMenu` | `WIDGET` | `div.row` | 12 | 12 | 0.08 of 148 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 8 | module-menu | MISSING | `h5>span` | `span` | `—` | 10 | 10 | 0.24 of 148 | ptype=overview c=0.65 n=10 | 1.00 | — | CANDIDATE |
| 9 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-6.paddingR` | 6 | 6 | 0.78 of 148 | — | structure | yes | BELOW FLOOR |
| 10 | module-menu | EXTRA | `ul` | `—` | `li` | 4 | 4 | 0.95 of 148 | — | structure | — | BELOW FLOOR |
| 11 | module-menu | MISSING | `li` | `ul` | `—` | 4 | 4 | 0.06 of 148 | — | 1.00 | — | BELOW FLOOR |
| 12 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `p` | 3 | 3 | 0.79 of 148 | — | structure | yes | BELOW FLOOR |
| 13 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `ul` | 3 | 3 | 0.99 of 148 | — | structure | yes | BELOW FLOOR |
| 14 | module-menu | EXTRA | `div.col-12.col-md-12.paddingR` | `—` | `h4>span` | 3 | 3 | 0.80 of 148 | — | structure | yes | BELOW FLOOR |
| 15 | module-menu | MISSING | `ul` | `li` | `—` | 3 | 3 | 0.05 of 148 | — | 1.00 | — | BELOW FLOOR |
| 16 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6.paddingR` | `—` | 3 | 3 | 0.22 of 148 | — | 1.00 | yes | BELOW FLOOR |
| 17 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `p` | `—` | 3 | 3 | 0.15 of 148 | — | 1.00 | yes | BELOW FLOOR |
| 18 | module-menu | MISSING | `div.row` | `div.col-12.col-md-12.paddingR` | `—` | 3 | 3 | 0.02 of 148 | — | 1.00 | yes | BELOW FLOOR |
| 19 | module-menu | MISSING | `div.col-12.col-md-8` | `p` | `—` | 4 | 2 | 0.03 of 148 | — | 0.00 | — | BELOW FLOOR |
| 20 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `h5` | 2 | 2 | 1.00 of 148 | — | structure | yes | BELOW FLOOR |
| 21 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `p>b` | 2 | 2 | 1.00 of 148 | — | structure | yes | BELOW FLOOR |
| 22 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-12.paddingR` | 2 | 2 | 0.78 of 148 | — | structure | yes | BELOW FLOOR |
| 23 | module-menu | MISSING | `li` | `i` | `—` | 2 | 2 | 0.01 of 148 | — | 1.00 | — | BELOW FLOOR |
| 24 | module-menu | SUBSTITUTED | `div.col-12.col-md-12.paddingR` | `p` | `h5` | 2 | 2 | 0.01 of 148 | — | structure | yes | BELOW FLOOR |
| 25 | module-menu | MISSING | `div.titlebar` | `div#module-head-buttons` | `—` | 2 | 1 | 0.01 of 148 | — | structure | yes | BELOW FLOOR |
| 26 | module-menu | MISSING | `div#header` | `div#module-head-buttons` | `—` | 2 | 1 | 0.41 of 148 | — | structure | yes | BELOW FLOOR |
| 27 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `h5>span` | `—` | 1 | 1 | 0.22 of 148 | — | 1.00 | yes | BELOW FLOOR |
| 28 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `ul` | `—` | 1 | 1 | 0.06 of 148 | — | 1.00 | yes | BELOW FLOOR |
| 29 | module-menu | MISSING | `li>i` | `i` | `—` | 1 | 1 | 0.01 of 148 | — | 1.00 | — | BELOW FLOOR |
| 30 | module-menu | MISSING | `ul` | `li>i` | `—` | 1 | 1 | 0.01 of 148 | — | 0.50 | — | BELOW FLOOR |
| 31 | module-menu | MOVED | `ul` | `li` | `li` | 1 | 1 | 0.20 of 148 | — | structure | — | BELOW FLOOR |
| 32 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `ul` | `p` | 1 | 1 | 0.22 of 148 | — | structure | yes | BELOW FLOOR |
| 33 | module-menu | SUBSTITUTED | `ul` | `p` | `li>b` | 1 | 1 | 0.01 of 148 | — | structure | — | BELOW FLOOR |
| 34 | module-menu | SUBSTITUTED | `ul` | `p` | `li` | 1 | 1 | 0.01 of 148 | — | structure | — | BELOW FLOOR |
| 35 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `p` | `ul` | 1 | 1 | 0.21 of 148 | — | structure | yes | BELOW FLOOR |
| 36 | module-menu | SUBSTITUTED | `div.col-12.col-md-12.paddingR` | `p>i` | `h5` | 1 | 1 | 0.01 of 148 | — | structure | yes | BELOW FLOOR |
| 37 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `p>i` | `h5` | 1 | 1 | 0.01 of 148 | — | structure | yes | BELOW FLOOR |
| 38 | footer | MISSING | `ul.footer-nav.inquiry-nav` | `li>a.home-nav` | `—` | 27 | 23 | 0.88 of 148 | ptype=overview c=0.89 n=19 | structure | yes | CANDIDATE |
| 39 | footer | EXTRA | `body.container-fluid` | `—` | `div#footer` | 19 | 15 | 0.24 of 148 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 40 | footer | MISSING | `div#body` | `div#footer` | `—` | 13 | 11 | 0.18 of 148 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 41 | footer | SUBSTITUTED | `div#body` | `div#footer` | `ul.footer-nav.inquiry-nav` | 12 | 11 | 0.18 of 148 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 42 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav.inquiry-nav` | `li>a#next-lesson` | 11 | 11 | 0.88 of 148 | ptype=overview c=0.89 n=11 | structure | yes | CANDIDATE |
| 43 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` | `li>a#next-lesson` | `li>a.home-nav` | 11 | 11 | 0.66 of 148 | ptype=overview c=0.89 n=11 | structure | yes | CANDIDATE |
| 44 | footer | MISSING | `li>a#next-lesson` | `a#next-lesson` | `—` | 9 | 9 | 0.76 of 148 | — | structure | yes | BELOW FLOOR |
| 45 | footer | EXTRA | `ul.footer-nav.inquiry-nav` | `—` | `li>a.home-nav` | 7 | 7 | 0.12 of 148 | — | structure | yes | BELOW FLOOR |
| 46 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav` | `ul.footer-nav.inquiry-nav` | 18 | 6 | 0.12 of 148 | — | structure | yes | BELOW FLOOR |
| 47 | footer | EXTRA | `div#footer` | `—` | `ul.footer-nav.inquiry-nav` | 7 | 6 | 0.12 of 148 | — | structure | yes | BELOW FLOOR |
| 48 | footer | MISSING | `ul.footer-nav.inquiry-nav` | `li>a#next-lesson` | `—` | 2 | 2 | 0.66 of 148 | — | structure | yes | BELOW FLOOR |
| 49 | footer | MISSING | `ul.footer-nav` | `li>a.home-nav` | `—` | 2 | 2 | 0.12 of 148 | — | structure | yes | BELOW FLOOR |
| 50 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` | `li>a#prev-lesson` | `li>a.home-nav` | 2 | 2 | 0.59 of 148 | — | structure | yes | BELOW FLOOR |
| 51 | footer | SUBSTITUTED | `div#body` | `div#footer` | `div#footer` | 2 | 2 | 0.18 of 148 | — | structure | yes | BELOW FLOOR |
| 52 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav.inquiry-nav` | `ul.footer-nav.inquiry-nav` | 2 | 2 | 0.88 of 148 | — | structure | yes | BELOW FLOOR |
| 53 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` | `li>a.home-nav` | `li>a.home-nav` | 2 | 2 | 0.88 of 148 | — | structure | yes | BELOW FLOOR |
| 54 | footer | MISSING | `div.row` | `div#footer` | `—` | 1 | 1 | 0.01 of 148 | — | structure | yes | BELOW FLOOR |
| 55 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav.inquiry-nav` | `li>a.home-nav` | 1 | 1 | 0.88 of 148 | — | structure | yes | BELOW FLOOR |
| 56 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav.inquiry-nav` | `li>a#prev-lesson` | 1 | 1 | 0.88 of 148 | — | structure | yes | BELOW FLOOR |
| 57 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` | `li>a.home-nav` | `p>b` | 1 | 1 | 0.88 of 148 | — | structure | yes | BELOW FLOOR |
| 58 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` | `li>a#prev-lesson` | `li>a#prev-lesson` | 1 | 1 | 0.59 of 148 | — | structure | yes | BELOW FLOOR |
| 59 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` | `li>a#next-lesson` | `li>a#next-lesson` | 1 | 1 | 0.66 of 148 | — | structure | yes | BELOW FLOOR |
| 60 | footer | SUBSTITUTED | `li>a.prev-lesson` | `a.prev-lesson` | `a#prev-lesson` | 1 | 1 | 0.01 of 148 | — | structure | yes | BELOW FLOOR |
| 61 | acks | SUBSTITUTED | `div.col-12.col-md-8` | `div.acks` | `div.acks.acksTemplate` | 17 | 17 | 0.26 of 148 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 62 | acks | SUBSTITUTED | `div.col-12.col-md-8` | `div.acks.acksAI.acksTemplate` | `div.acks.acksTemplate` | 9 | 9 | 0.06 of 148 | — | structure | yes | BELOW FLOOR |
| 63 | acks | SUBSTITUTED | `div.col-12.col-md-8` | `div.acks` | `div.activity[number=*]` | 1 | 1 | 0.26 of 148 | — | structure | yes | BELOW FLOOR |
| 64 | acks | SUBSTITUTED | `div.acks` | `WIDGET` | `div.row` | 1 | 1 | 0.26 of 148 | — | structure | yes | BELOW FLOOR |
| 65 | activity | MISSING | `div.col-12` | `p` | `—` | 51 | 35 | 0.20 of 148 | — | 0.76 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 66 | activity | EXTRA | `div.col-12` | `—` | `p` | 43 | 35 | 0.80 of 148 | template=Standard c=0.84 n=38 | structure | — | CANDIDATE |
| 67 | activity | EXTRA | `div.col-12` | `—` | `WIDGET` | 40 | 32 | 0.82 of 148 | template=Standard c=0.86 n=37 | structure | — | CANDIDATE |
| 68 | activity | MISSING | `div.col-12` | `WIDGET` | `—` | 34 | 29 | 0.18 of 148 | — | structure | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 69 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `div.activity[number=*]` | 28 | 25 | 0.49 of 148 | ptype=lesson c=0.71 n=24 | structure | yes | CANDIDATE |
| 70 | activity | MISSING | `div.col-12` | `a` | `—` | 30 | 24 | 0.21 of 148 | — | 0.98 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 71 | activity | MISSING | `div.col-12` | `div.row` | `—` | 25 | 24 | 0.10 of 148 | — | 0.93 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 72 | activity | EXTRA | `div.col-12` | `—` | `p>a` | 26 | 23 | 1.00 of 148 | era=Refresh c=1.00 n=26 | structure | — | CANDIDATE |
| 73 | activity | SUBSTITUTED | `div.col-12` | `div.row` | `WIDGET` | 26 | 23 | 0.39 of 148 | — | structure | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 74 | activity | MISSING | `div.col-12` | `div.clickDropContent` | `—` | 24 | 22 | 0.12 of 148 | — | 0.97 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 75 | activity | MOVED | `div.col-12` | `p` | `p` | 24 | 20 | 0.10 of 148 | — | structure | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 76 | activity | MOVED | `a` | `div.buttonD` | `div.buttonD` | 20 | 20 | 0.16 of 148 | — | structure | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 77 | activity | SUBSTITUTED | `div.col-12` | `p` | `p` | 19 | 17 | 0.62 of 148 | — | structure | — | BELOW FLOOR |
| 78 | activity | MOVED | `div.col-12` | `p` | `p` | 18 | 17 | 0.32 of 148 | — | structure | — | BELOW FLOOR |
| 79 | activity | EXTRA | `div.col-12` | `—` | `img.img-fluid` | 17 | 17 | 0.89 of 148 | — | structure | — | BELOW FLOOR |
| 80 | activity | EXTRA | `p>a` | `—` | `a` | 19 | 16 | 1.00 of 148 | — | structure | — | BELOW FLOOR |
| 81 | activity | EXTRA | `div.row` | `—` | `div.col-12` | 20 | 15 | 0.79 of 148 | era=Refresh c=0.79 n=20 | structure | — | CANDIDATE |
| 82 | activity | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `div.col-12` | 17 | 15 | 0.17 of 148 | — | structure | — | BELOW FLOOR |
| 83 | activity | SUBSTITUTED | `div.col-12.col-md-12` | `div.activity.interactive[number=*]` | `div.activity[number=*]` | 17 | 15 | 0.22 of 148 | — | structure | yes | BELOW FLOOR |
| 84 | activity | SUBSTITUTED | `div.col-12` | `div.table-responsive` | `WIDGET` | 14 | 13 | 0.19 of 148 | — | structure | — | BELOW FLOOR |
| 85 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.alertPadding[number=*]` | `div.activity[number=*]` | 14 | 12 | 0.11 of 148 | — | structure | yes | BELOW FLOOR |
| 86 | activity | MOVED | `div.col-12` | `h3` | `h3` | 13 | 12 | 0.21 of 148 | — | structure | — | BELOW FLOOR |
| 87 | activity | MISSING | `div.activity.interactive[number=*]` | `WIDGET` | `—` | 16 | 11 | 0.07 of 148 | — | structure | yes | BELOW FLOOR |
| 88 | activity | EXTRA | `div.col-12` | `—` | `h3` | 14 | 11 | 0.92 of 148 | — | structure | — | BELOW FLOOR |
| 89 | activity | MISSING | `p` | `br` | `—` | 14 | 11 | 0.05 of 148 | — | structure | — | BELOW FLOOR |
| 90 | activity | MISSING | `a` | `div.button.buttonD` | `—` | 12 | 10 | 0.07 of 148 | — | 1.00 | yes | BELOW FLOOR |
| 91 | activity | SUBSTITUTED | `div.row` | `WIDGET` | `WIDGET` | 12 | 10 | 0.15 of 148 | — | structure | — | BELOW FLOOR |
| 92 | activity | MISSING | `p` | `i` | `—` | 11 | 10 | 0.11 of 148 | — | 1.00 | — | BELOW FLOOR |
| 93 | activity | SUBSTITUTED | `div.col-12.col-md-10` | `div.activity.interactive[number=*]` | `div.activity[number=*]` | 11 | 10 | 0.18 of 148 | — | structure | yes | BELOW FLOOR |
| 94 | activity | MISSING | `div.row` | `div.col-12.col-md-4` | `—` | 10 | 10 | 0.06 of 148 | — | 1.00 | — | BELOW FLOOR |
| 95 | activity | MISSING | `div.row` | `WIDGET` | `—` | 10 | 10 | 0.04 of 148 | — | structure | — | BELOW FLOOR |
| 96 | activity | MOVED | `div.col-12` | `a` | `a` | 10 | 10 | 0.07 of 148 | — | structure | — | BELOW FLOOR |
| 97 | activity | EXTRA | `a` | `—` | `div.buttonD` | 12 | 9 | 0.84 of 148 | — | structure | — | BELOW FLOOR |
| 98 | activity | EXTRA | `div.col-12` | `—` | `p>i` | 10 | 9 | 0.92 of 148 | — | structure | — | BELOW FLOOR |
| 99 | activity | MISSING | `p` | `b` | `—` | 10 | 9 | 0.07 of 148 | — | 0.93 | — | BELOW FLOOR |
| 100 | activity | EXTRA | `div.clickDropContent` | `—` | `img.img-fluid` | 9 | 9 | 1.00 of 148 | — | structure | — | BELOW FLOOR |
| 825 | body | EXTRA | `div#body` | `—` | `div.row` | 69 | 42 | 0.94 of 148 | era=Refresh c=0.94 n=69 | structure | — | CANDIDATE |
| 826 | body | SUBSTITUTED | `div.row` | `div.col-12` | `div.col-12.col-md-8` | 53 | 35 | 0.59 of 148 | ptype=overview c=1.00 n=28 | structure | — | CANDIDATE |
| 829 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 29 | 26 | 0.99 of 148 | template=Standard c=1.00 n=23 | structure | — | CANDIDATE |
| 830 | body | MISSING | `div#body` | `div.row` | `—` | 31 | 25 | 0.43 of 148 | ptype=lesson c=0.67 n=25 | 0.93 | — | CANDIDATE |
| 831 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p>b` | 21 | 20 | 1.00 of 148 | template=Standard c=1.00 n=21 | structure | — | CANDIDATE |
| 1118 | root | EXTRA | `body.container-fluid` | `—` | `div.row` | 20 | 20 | 0.76 of 148 | era=Refresh c=0.76 n=20 | structure | — | CANDIDATE |

## Details — in the companion file `CONVERTER_V2/outputs/_diff_queue_details.md`
Every CANDIDATE and every top-40 row has three quoted examples (WT / gold / Claude) there, plus the
below-floor list. **NEVER read the companion whole** (hundreds of KB): `grep -n '^### #<rank> ' CONVERTER_V2/outputs/_diff_queue_details.md` then `sed -n '<start>,<start+40>p'`. The top 25
candidates' detail blocks are repeated below for convenience.

### #6 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `WIDGET` — CANDIDATE
- pages 12 / modules 12 / lines 12; consensus (all) 0.95 of 148 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 12m/12p c=0.96
- by subject: 1-10 Blended Literacy 12m/12p c=0.95
- by era: Refresh 12m/12p c=0.95
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

### #8 · module-menu · MISSING · `h5>span` › gold `span` vs Claude `—` — CANDIDATE
- pages 10 / modules 10 / lines 10; consensus (all) 0.24 of 148 gold pages with the region; derivable 1.00 (0 lines with no WT source)
- by template: Standard 8m/8p c=0.21; Inquiry 2m/2p c=0.86
- by subject: 1-10 Blended Literacy 10m/10p c=0.24
- by era: Refresh 10m/10p c=0.24
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

### #38 · footer · MISSING · `ul.footer-nav.inquiry-nav` › gold `li>a.home-nav` vs Claude `—` — CANDIDATE
- pages 27 / modules 23 / lines 27; consensus (all) 0.88 of 148 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 16m/20p c=0.87; Inquiry 7m/7p c=1.00
- by subject: 1-10 Blended Literacy 23m/27p c=0.88
- by era: Refresh 23m/27p c=0.88
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:40 — | Footer tag | `<nav id="module-foot">` with `<button>` + FA icons | `<div id="footer">` with `<ul class="footer-nav">` |
  - KB: 06_TEMPLATE_RECOGNITION.md:64 — | Footer `<ul>` class | `footer-nav` | `footer-nav` | `footer-nav fundamentals-nav` | `footer-nav inquiry-nav` | `footer-nav` |
  - KB: 06_TEMPLATE_RECOGNITION.md:114 — **Footer:** `<ul class="footer-nav">` with prev + next + home links.
- **BLL210** BLL210_0_0.html ↔ BLL210.html (structure, derivable=True)
  - gold: `li`
  - Claude: `—`
- **BLL220** BLL220_0_0.html ↔ BLL220.html (structure, derivable=True)
  - gold: `li`
  - Claude: `—`
- **BLL230** BLL230_0_0.html ↔ BLL230.html (structure, derivable=True)
  - gold: `li`
  - Claude: `—`
- modules: BLL210, BLL211, BLL213, BLL216, BLL217, BLL220, BLL221, BLL222, BLL223, BLL224, BLL225, BLL226, BLL227, BLL230, BLL231, BLL234, BLL240, BLL250, BLL260, BLL266, BLL270, BLL274, BLL276

### #42 · footer · SUBSTITUTED · `div#footer` › gold `ul.footer-nav.inquiry-nav` vs Claude `li>a#next-lesson` — CANDIDATE
- pages 11 / modules 11 / lines 11; consensus (all) 0.88 of 148 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 11m/11p c=0.87
- by subject: 1-10 Blended Literacy 11m/11p c=0.88
- by era: Refresh 11m/11p c=0.88
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:40 — | Footer tag | `<nav id="module-foot">` with `<button>` + FA icons | `<div id="footer">` with `<ul class="footer-nav">` |
  - KB: 06_TEMPLATE_RECOGNITION.md:55 — Once confirmed as Refresh, determine which sub-type the reference files represent. This drives structural decisions about navigation, footer classes, 
  - KB: 06_TEMPLATE_RECOGNITION.md:64 — | Footer `<ul>` class | `footer-nav` | `footer-nav` | `footer-nav fundamentals-nav` | `footer-nav inquiry-nav` | `footer-nav` |
- **BLL211** BLL211_0_0.html ↔ BLL211-0.0.html (structure, derivable=True)
  - gold: `ul.footer-nav.inquiry-nav`
  - Claude: `li`
- **BLL213** BLL213_0_0.html ↔ BLL213-0.0.html (structure, derivable=True)
  - gold: `ul.footer-nav.inquiry-nav`
  - Claude: `li`
- **BLL216** BLL216_0_0.html ↔ BLL216-0.0.html (structure, derivable=True)
  - gold: `ul.footer-nav.inquiry-nav`
  - Claude: `li`
- modules: BLL211, BLL213, BLL216, BLL217, BLL221, BLL222, BLL224, BLL225, BLL226, BLL227, BLL231

### #43 · footer · SUBSTITUTED · `ul.footer-nav.inquiry-nav` › gold `li>a#next-lesson` vs Claude `li>a.home-nav` — CANDIDATE
- pages 11 / modules 11 / lines 11; consensus (all) 0.66 of 148 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 11m/11p c=0.65
- by subject: 1-10 Blended Literacy 11m/11p c=0.66
- by era: Refresh 11m/11p c=0.66
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:40 — | Footer tag | `<nav id="module-foot">` with `<button>` + FA icons | `<div id="footer">` with `<ul class="footer-nav">` |
  - KB: 06_TEMPLATE_RECOGNITION.md:64 — | Footer `<ul>` class | `footer-nav` | `footer-nav` | `footer-nav fundamentals-nav` | `footer-nav inquiry-nav` | `footer-nav` |
  - KB: 06_TEMPLATE_RECOGNITION.md:114 — **Footer:** `<ul class="footer-nav">` with prev + next + home links.
- **BLL211** BLL211_0_0.html ↔ BLL211-0.0.html (structure, derivable=True)
  - gold: `li`
  - Claude: `li`
- **BLL213** BLL213_0_0.html ↔ BLL213-0.0.html (structure, derivable=True)
  - gold: `li`
  - Claude: `li`
- **BLL216** BLL216_0_0.html ↔ BLL216-0.0.html (structure, derivable=True)
  - gold: `li`
  - Claude: `li`
- modules: BLL211, BLL213, BLL216, BLL217, BLL221, BLL222, BLL224, BLL225, BLL226, BLL227, BLL231

### #66 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `p` — CANDIDATE
- pages 43 / modules 35 / lines 115; consensus (all) 0.80 of 148 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 30m/38p c=0.84; Inquiry 5m/5p c=0.00
- by subject: 1-10 Blended Literacy 35m/43p c=0.80
- by era: Refresh 35m/43p c=0.80
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL210** BLL210_0_0.html ↔ BLL210.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «English Pronunciation | The Letter U | 11 Ways to Pronounce U in English!»`
- **BLL220** BLL220_0_0.html ↔ BLL220.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Watch these videos to learn more about the /oy/ sound.»`
- **BLL230** BLL230_0_0.html ↔ BLL230.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Can you think of some other letter teams or vowel teams that make the long /ō/ vowel sound?»`
- modules: BLL210, BLL211, BLL212, BLL213, BLL214, BLL215, BLL220, BLL221, BLL222, BLL226, BLL227, BLL230, BLL231, BLL232, BLL235, BLL236, BLL241, BLL242, BLL243, BLL244, BLL245, BLL246, BLL247, BLL251 …

### #67 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `WIDGET` — CANDIDATE
- pages 40 / modules 32 / lines 58; consensus (all) 0.82 of 148 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 29m/37p c=0.86; Inquiry 3m/3p c=0.00
- by subject: 1-10 Blended Literacy 32m/40p c=0.82
- by era: Refresh 32m/40p c=0.82
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL240** BLL240_0_0.html ↔ BLL240.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **BLL260** BLL260_0_0.html ↔ BLL260.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **BLL270** BLL270_0_0.html ↔ BLL270.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- modules: BLL211, BLL212, BLL214, BLL215, BLL221, BLL226, BLL227, BLL231, BLL232, BLL233, BLL234, BLL235, BLL236, BLL237, BLL240, BLL241, BLL243, BLL244, BLL246, BLL252, BLL253, BLL254, BLL256, BLL257 …

### #69 · activity · SUBSTITUTED · `div.col-12.col-md-8` › gold `div.activity.interactive[number=*]` vs Claude `div.activity[number=*]` — CANDIDATE
- pages 28 / modules 25 / lines 53; consensus (all) 0.49 of 148 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 21m/24p c=0.47; Inquiry 4m/4p c=0.86
- by subject: 1-10 Blended Literacy 25m/28p c=0.49
- by era: Refresh 25m/28p c=0.49
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:46 — | Activity class | `content activity activity-bg` | `activity` |
  - KB: 06_TEMPLATE_RECOGNITION.md:181 — - TWHA902–904 use `choicePage` activity grids and dual titles + `whakatauki` — these are content patterns, safe to use if the new module needs them
  - KB: 06_TEMPLATE_RECOGNITION.md:265 — **The X-prefix test governs THIS CLASS ONLY.** The wider LS look-and-feel conventions of `14_SUBJECT_GLOBAL_PARAMETERS.md` § 14.6 — terminology and br
- **BLL210** BLL210_0_0.html ↔ BLL210.html (structure, derivable=True)
  - gold: `div.activity.interactive[number=3B]  «Silent or not?»`
  - Claude: `div.activity[number=3B]  «Silent or not?»`
- **BLL220** BLL220_0_0.html ↔ BLL220.html (structure, derivable=True)
  - gold: `div.activity.interactive[number=1F]  «Optional activities»`
  - Claude: `div.activity[number=1H]  «Optional activities»`
- **BLL260** BLL260_0_0.html ↔ BLL260.html (structure, derivable=True)
  - gold: `div.activity.interactive[number=1E]  «Write the words»`
  - Claude: `div.activity[number=1E]  «Write the words»`
- modules: BLL210, BLL211, BLL215, BLL217, BLL220, BLL221, BLL222, BLL225, BLL231, BLL232, BLL234, BLL236, BLL245, BLL247, BLL255, BLL256, BLL260, BLL263, BLL264, BLL265, BLL270, BLL271, BLL274, BLL275 …

### #72 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `p>a` — CANDIDATE
- pages 26 / modules 23 / lines 48; consensus (all) 1.00 of 148 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 19m/22p c=1.00; Inquiry 4m/4p c=1.00
- by subject: 1-10 Blended Literacy 23m/26p c=1.00
- by era: Refresh 23m/26p c=1.00
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL210** BLL210_0_0.html ↔ BLL210.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «https://www.youtube.com/watch?v=dGIxNzMCcGk»`
- **BLL230** BLL230_0_0.html ↔ BLL230.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «https://www.youtube.com/watch?v=e3rnxjGbC0w»`
- **BLL260** BLL260_0_0.html ↔ BLL260.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «https://www.istockphoto.com/vector/detective-holding-a-magnifying-glass-with-circle-shape-gm607776188-104228297»`
- modules: BLL210, BLL212, BLL213, BLL214, BLL226, BLL227, BLL230, BLL232, BLL233, BLL235, BLL236, BLL242, BLL246, BLL251, BLL252, BLL253, BLL254, BLL256, BLL260, BLL265, BLL270, BLL272, BLL276

### #81 · activity · EXTRA · `div.row` › gold `—` vs Claude `div.col-12` — CANDIDATE
- pages 20 / modules 15 / lines 46; consensus (all) 0.79 of 148 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 14m/19p c=0.83; Inquiry 1m/1p c=0.00
- by subject: 1-10 Blended Literacy 15m/20p c=0.79
- by era: Refresh 15m/20p c=0.79
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL230** BLL230_0_0.html ↔ BLL230.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12  «Optional activities»`
- **BLL213** BLL213_2_0.html ↔ BLL213-2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12  «Decodable text»`
- **BLL216** BLL216_1_0.html ↔ BLL216-1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12  «These texts should be reasonably easy for the reader. The purpose of this activity is to encourage the ākonga to read fo»`
- modules: BLL213, BLL216, BLL221, BLL222, BLL230, BLL251, BLL261, BLL262, BLL263, BLL264, BLL265, BLL271, BLL274, BLL275, BLL276

### #825 · body · EXTRA · `div#body` › gold `—` vs Claude `div.row` — CANDIDATE
- pages 69 / modules 42 / lines 146; consensus (all) 0.94 of 148 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 42m/69p c=0.94
- by subject: 1-10 Blended Literacy 42m/69p c=0.94
- by era: Refresh 42m/69p c=0.94
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL211** BLL211_2_0.html ↔ BLL211-2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Remembering things.»`
- **BLL212** BLL212_0_0.html ↔ BLL212-0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Animation Script»`
- **BLL213** BLL213_0_0.html ↔ BLL213-0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Introduction»`
- modules: BLL211, BLL212, BLL213, BLL214, BLL215, BLL216, BLL217, BLL221, BLL222, BLL223, BLL224, BLL226, BLL227, BLL231, BLL232, BLL234, BLL235, BLL236, BLL242, BLL243, BLL244, BLL245, BLL246, BLL247 …

### #826 · body · SUBSTITUTED · `div.row` › gold `div.col-12` vs Claude `div.col-12.col-md-8` — CANDIDATE
- pages 53 / modules 35 / lines 62; consensus (all) 0.59 of 148 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 35m/53p c=0.57
- by subject: 1-10 Blended Literacy 35m/53p c=0.59
- by era: Refresh 35m/53p c=0.59
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL211** BLL211_0_0.html ↔ BLL211-0.0.html (structure, derivable=True)
  - gold: `div.col-12  «Introduction»`
  - Claude: `div.col-12.col-md-8  «Introduction»`
- **BLL212** BLL212_0_0.html ↔ BLL212-0.0.html (structure, derivable=True)
  - gold: `div.col-12  «Introduction»`
  - Claude: `div.col-12.col-md-8  «Introduction»`
- **BLL213** BLL213_0_0.html ↔ BLL213-0.0.html (structure, derivable=True)
  - gold: `div.col-12  «Introduction»`
  - Claude: `div.col-12.col-md-8  «Module 3 - y, long vowels, silent e»`
- modules: BLL211, BLL212, BLL213, BLL214, BLL215, BLL216, BLL217, BLL221, BLL222, BLL223, BLL224, BLL225, BLL226, BLL227, BLL231, BLL232, BLL233, BLL234, BLL235, BLL242, BLL246, BLL247, BLL251, BLL252 …

### #829 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `p` — CANDIDATE
- pages 29 / modules 26 / lines 103; consensus (all) 0.99 of 148 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 20m/23p c=1.00; Inquiry 6m/6p c=0.86
- by subject: 1-10 Blended Literacy 26m/29p c=0.99
- by era: Refresh 26m/29p c=0.99
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL210** BLL210_0_0.html ↔ BLL210.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Watch these videos to learn more:»`
- **BLL220** BLL220_0_0.html ↔ BLL220.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «boy, toy, soy, coy,»`
- **BLL230** BLL230_0_0.html ↔ BLL230.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Vowel team oe»`
- modules: BLL210, BLL211, BLL217, BLL220, BLL224, BLL226, BLL230, BLL231, BLL236, BLL242, BLL247, BLL250, BLL251, BLL252, BLL253, BLL257, BLL260, BLL261, BLL263, BLL264, BLL270, BLL271, BLL272, BLL274 …

### #830 · body · MISSING · `div#body` › gold `div.row` vs Claude `—` — CANDIDATE
- pages 31 / modules 25 / lines 42; consensus (all) 0.43 of 148 gold pages with the region; derivable 0.93 (3 lines with no WT source)
- by template: Standard 25m/31p c=0.45
- by subject: 1-10 Blended Literacy 25m/31p c=0.43
- by era: Refresh 25m/31p c=0.43
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL211** BLL211_2_0.html ↔ BLL211-2.0.html (content, derivable=False)
  - gold: `div.row  «Congratulations on completing Module 1. Go back to the landing page and click on Module 2 when you are ready to move on.»`
  - Claude: `—`
- **BLL214** BLL214_1_0.html ↔ BLL214-1.0.html (content, derivable=True)
  - gold: `div.row  «Decode, encode and decode»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [Activity 1B]  [/RED TEXT]🔴Decode, encode and decode`
- **BLL215** BLL215_1_0.html ↔ BLL215-1.0.html (content, derivable=True)
  - gold: `div.row  «Cloze activity»`
  - Claude: `—`
- modules: BLL211, BLL214, BLL215, BLL216, BLL221, BLL224, BLL232, BLL233, BLL235, BLL236, BLL247, BLL252, BLL253, BLL254, BLL256, BLL261, BLL264, BLL265, BLL266, BLL271, BLL272, BLL273, BLL274, BLL275 …

### #831 · body · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `p>b` — CANDIDATE
- pages 21 / modules 20 / lines 29; consensus (all) 1.00 of 148 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 20m/21p c=1.00
- by subject: 1-10 Blended Literacy 20m/21p c=1.00
- by era: Refresh 20m/21p c=1.00
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL211** BLL211_0_0.html ↔ BLL211-0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Animation Script»`
- **BLL213** BLL213_0_0.html ↔ BLL213-0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Animation Script»`
- **BLL216** BLL216_0_0.html ↔ BLL216-0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Animation Script»`
- modules: BLL211, BLL213, BLL216, BLL217, BLL221, BLL222, BLL224, BLL225, BLL226, BLL227, BLL231, BLL234, BLL235, BLL236, BLL237, BLL261, BLL262, BLL271, BLL273, BLL276

### #1118 · root · EXTRA · `body.container-fluid` › gold `—` vs Claude `div.row` — CANDIDATE
- pages 20 / modules 20 / lines 20; consensus (all) 0.76 of 148 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 20m/20p c=0.74
- by subject: 1-10 Blended Literacy 20m/20p c=0.76
- by era: Refresh 20m/20p c=0.76
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL211** BLL211_0_0.html ↔ BLL211-0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row`
- **BLL212** BLL212_0_0.html ↔ BLL212-0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row`
- **BLL213** BLL213_0_0.html ↔ BLL213-0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row`
- modules: BLL211, BLL212, BLL213, BLL214, BLL215, BLL216, BLL217, BLL221, BLL222, BLL223, BLL224, BLL225, BLL226, BLL227, BLL231, BLL232, BLL233, BLL234, BLL235, BLL237
