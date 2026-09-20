# DIFF_QUEUE.md — the diff miner's ranked class queue (LOOP__Autonomous_Rounds.md §1d)

**Produced:** 2026-09-20 20:58 NZST by `reference/tests/_diff_miner.py` on the CURRENT corpus (pageforge-site HEAD 1ea8fb4; Claude corpus 494 dirs). **Population:** the skeleton gate's own — 2349 paired pages / 483 modules (compare_exclusions.txt honoured; acks / glossary / references pages excluded); parse errors skipped: 0 (must be 0); modules without a parsed WT: 2. Run time 81.8 s.

**What a row is.** One CLASS = (region, parent element, gold form, Claude form, direction) over every differing skeleton line of every paired page — the same lines, labels, widget collapse and difflib alignment the PRIMARY gate scores (each element its own line so it can be quoted). Direction: MISSING = gold has it, Claude lacks it; EXTRA = Claude has it, gold lacks it; SUBSTITUTED = same position, different tag / class / wrapper; MOVED = same text, different place. Consensus = of the gold pages in the group where the region exists, the share carrying the gold form (for EXTRA: the share NOT carrying Claude's form). Derivable = the gold line's text is in the module's parsed Writers Template (round-110 tolerance); structure-only differences are always derivable.

**Candidate rule (§1d).** modules ≥ 10 for a chrome class (module-code / title / header / module-menu / crumbs / phases-nav / footer / acks), pages ≥ 20 for a body / activity class; gold consensus ≥ 0.60 in at least one template or subject group that itself reaches the floor; structure-only or derivable share ≥ 0.60. A class below the floor is listed, never dropped. A CANDIDATE still goes through the PICK's KB-first check, the triangulation and the §3 corpus-wide measurement before any code — this table is the queue, not the verdict.

## Summary

- differing skeleton lines: 265050 — by direction {'MISSING': 140933, 'SUBSTITUTED': 23684, 'EXTRA': 91788, 'MOVED': 8645}
- by region: {'module-code': 15, 'title': 352, 'header': 5, 'module-menu': 13322, 'phases-nav': 108, 'crumbs': 202, 'footer': 2412, 'acks': 1310, 'activity': 95209, 'body': 150522, 'root': 1593}
- classes: 8850 — CANDIDATE 181, below floor 8384, the rest below consensus / not derivable

## Completeness census — the repeating chrome (§1d item 4)

| region | pages with region | gold items | gold items in WT | Claude items | derivable misses | pages with misses | modules with misses | status |
|---|---|---|---|---|---|---|---|---|
| module-menu | 1469 | 15805 | 14565 | 11568 | 5154 | 741 | 198 | CANDIDATE (verify by eye — text presence, not position) |
| crumbs | 57 | 300 | 285 | 207 | 115 | 28 | 24 | CANDIDATE (verify by eye — text presence, not position) |
| phases-nav | 90 | 356 | 323 | 262 | 108 | 34 | 25 | CANDIDATE (verify by eye — text presence, not position) |
| footer | 14 | 70 | 56 | 0 | 56 | 14 | 6 | BELOW FLOOR |

- **module-menu** by template: Fundamentals 12m/22p/89 misses; Inquiry 27m/49p/302 misses; Standard 159m/670p/4763 misses
  - MXFL202 MXFL202_1_0.html: gold 53 items (51 in WT) / Claude 0 — 51 derivable misses, e.g. h3 «Understand» · span «Understand»
  - MXFL202 MXFL202_2_0.html: gold 53 items (51 in WT) / Claude 0 — 51 derivable misses, e.g. h3 «Understand» · span «Understand»
  - MXFL202 MXFL202_4_0.html: gold 53 items (51 in WT) / Claude 0 — 51 derivable misses, e.g. h3 «Understand» · span «Understand»
  - MXFL202 MXFL202_6_0.html: gold 53 items (51 in WT) / Claude 0 — 51 derivable misses, e.g. h3 «Understand» · span «Understand»
- **crumbs** by template: Fundamentals 0m/0p/0 misses; Inquiry 22m/22p/83 misses; Standard 2m/6p/32 misses
  - BLL240 BLL240_1_0.html: gold 8 items (8 in WT) / Claude 0 — 8 derivable misses, e.g. p «Introduction» · p «wh»
  - CEDK501 CEDK501_0_0.html: gold 8 items (7 in WT) / Claude 0 — 7 derivable misses, e.g. p «Dream it, plan it, do it» · p «Costing it out: budgeting for success»
  - CEDT104 CEDT104_0_0.html: gold 8 items (7 in WT) / Claude 0 — 7 derivable misses, e.g. p «Introduction» · p «Pepeha»
  - TWHA902 TWHA902_0_0.html: gold 9 items (8 in WT) / Claude 1 — 7 derivable misses, e.g. p «Listening, speaking, reading, writing» · p «Active listening»
- **phases-nav** by template: Fundamentals 24m/33p/104 misses; Standard 1m/1p/4 misses
  - FRFUN06 FRFUN06_0_0.html: gold 8 items (8 in WT) / Claude 0 — 8 derivable misses, e.g. p «Introduction» · p «a»
  - FRFUN06 FRFUN06_2_0.html: gold 8 items (8 in WT) / Claude 0 — 8 derivable misses, e.g. p «Introduction» · p «c (hard)»
  - FRFUN06 FRFUN06_6_0.html: gold 6 items (6 in WT) / Claude 0 — 6 derivable misses, e.g. p «Introduction» · p «Handwriting é»
  - FRFUN06 FRFUN06_7_0.html: gold 6 items (6 in WT) / Claude 0 — 6 derivable misses, e.g. p «Introduction» · p «Phone or tablet»
- **footer** by template: Inquiry 1m/7p/38 misses; Standard 5m/7p/18 misses
  - BLL240 BLL240_1_2.html: gold 6 items (6 in WT) / Claude 0 — 6 derivable misses, e.g. li «Previous» · a#prev-lesson «Previous»
  - BLL240 BLL240_1_3.html: gold 6 items (6 in WT) / Claude 0 — 6 derivable misses, e.g. li «Previous» · a#prev-lesson «Previous»
  - BLL240 BLL240_1_4.html: gold 6 items (6 in WT) / Claude 0 — 6 derivable misses, e.g. li «Previous» · a#prev-lesson «Previous»
  - BLL240 BLL240_1_5.html: gold 6 items (6 in WT) / Claude 0 — 6 derivable misses, e.g. li «Previous» · a#prev-lesson «Previous»

## Chrome facts — the header and footer as SETS per page (alignment-free; §1d items 2 + 4)

A fact is one thing a page's chrome has: `header:chip` (the `#module-code` div), `header:chip=module-code` / `=lesson-number` / `=lesson-number(00)`, `header:head-buttons`, `header:menu-content`, `header:title-h1-count=N`, `footer:present`, `footer:ul=<classes>`, `footer:link=prev-lesson` / `next-lesson` / `home-nav`, `footer:links=<order>`, `footer:inside-body`, `nav:crumbs`, `nav:phases`. MISSING = the gold page has the fact and Claude's does not; EXTRA the reverse. Consensus = the share of gold pages in the group that have (MISSING) / lack (EXTRA) the fact. Floor 10 modules.

| # | dir | fact | pages | modules | gold share (all) | consensus (all) | best group | status |
|---|---|---|---|---|---|---|---|---|
| F1 | MISSING | `header:title-h1-count=2` | 259 | 127 | 0.23 | 0.23 | subject+ptype=Online Safety (OS9000)/overview c=0.93 n=12 | CANDIDATE |
| F2 | EXTRA | `header:title-h1-count=1` | 256 | 124 | 0.76 | 0.24 | subject+ptype=Online Safety (OS9000)/overview c=0.93 n=12 | CANDIDATE |
| F3 | MISSING | `header:chip=decimal-number` | 119 | 52 | 0.57 | 0.57 | subject=NCEA1 c=0.81 n=10 | CANDIDATE |
| F4 | EXTRA | `header:chip=decimal-number` | 197 | 48 | 0.57 | 0.43 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F5 | EXTRA | `header:menu-content` | 76 | 39 | 0.75 | 0.25 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F6 | MISSING | `header:chip=module-code` | 72 | 39 | 0.17 | 0.17 | ptype=overview c=0.69 n=11 | CANDIDATE |
| F7 | EXTRA | `header:head-buttons` | 70 | 36 | 0.77 | 0.23 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F8 | EXTRA | `header:chip=lesson-number` | 83 | 35 | 0.19 | 0.81 | era=Refresh c=0.81 n=35 | CANDIDATE |
| F9 | MISSING | `header:chip=lesson-number` | 161 | 29 | 0.19 | 0.19 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F10 | EXTRA | `header:chip=module-code` | 27 | 27 | 0.17 | 0.83 | template=Standard c=0.86 n=14 | CANDIDATE |
| F11 | EXTRA | `header:chip=other` | 72 | 25 | 0.04 | 0.96 | ptype=lesson c=0.99 n=15 | CANDIDATE |
| F12 | EXTRA | `header:title-h1-count=2` | 22 | 21 | 0.23 | 0.77 | template=Standard c=0.81 n=15 | CANDIDATE |
| F13 | MISSING | `header:head-buttons` | 34 | 19 | 0.77 | 0.77 | template=Standard c=0.78 n=12 | CANDIDATE |
| F14 | MISSING | `header:title-h1-count=1` | 19 | 18 | 0.76 | 0.76 | template=Standard c=0.81 n=13 | CANDIDATE |
| F15 | MISSING | `header:chip=other` | 26 | 15 | 0.04 | 0.04 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F16 | MISSING | `header:menu-content` | 7 | 6 | 0.75 | 0.75 | — | BELOW FLOOR |
| F17 | MISSING | `header:title-h1-count=3` | 6 | 6 | 0.00 | 0.00 | — | BELOW FLOOR |
| F18 | EXTRA | `header:title-h1-count=0` | 5 | 5 | 0.00 | 1.00 | — | BELOW FLOOR |
| F19 | EXTRA | `header:chip` | 5 | 5 | 0.97 | 0.03 | — | BELOW FLOOR |
| F20 | MISSING | `header:chip` | 3 | 3 | 0.97 | 0.97 | — | BELOW FLOOR |
| F21 | EXTRA | `header:title-h1-count=3` | 1 | 1 | 0.00 | 1.00 | — | BELOW FLOOR |
| F22 | EXTRA | `header:chip=lesson-number(00)` | 1 | 1 | 0.00 | 1.00 | — | BELOW FLOOR |
| F23 | MISSING | `nav:phases` | 20 | 11 | 0.04 | 0.04 | template+ptype=Fundamentals/overview c=0.99 n=10 | CANDIDATE |
| F24 | MISSING | `nav:crumbs` | 11 | 11 | 0.02 | 0.02 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F25 | EXTRA | `nav:crumbs` | 12 | 3 | 0.02 | 0.98 | — | BELOW FLOOR |
| F26 | MISSING | `footer:inside-body` | 169 | 127 | 0.07 | 0.07 | subject+ptype=1-10 Languages/overview c=0.62 n=10 | CANDIDATE |
| F27 | EXTRA | `footer:links=prev-lesson,next-lesson,home-nav` | 276 | 121 | 0.61 | 0.39 | template+ptype=Standard/overview c=0.97 n=12 | CANDIDATE |
| F28 | EXTRA | `footer:links=next-lesson,home-nav` | 101 | 100 | 0.12 | 0.88 | template=Fundamentals c=0.99 n=11 | CANDIDATE |
| F29 | EXTRA | `footer:links=prev-lesson,home-nav` | 73 | 73 | 0.13 | 0.87 | subject=1-10 English c=0.90 n=12 | CANDIDATE |
| F30 | EXTRA | `footer:link=next-lesson` | 122 | 70 | 0.82 | 0.18 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F31 | MISSING | `footer:links=home-nav,next-lesson` | 69 | 68 | 0.03 | 0.03 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F32 | MISSING | `footer:links=prev-lesson,next-lesson,home-nav` | 66 | 63 | 0.61 | 0.61 | template+ptype=Bilingual/lesson c=0.81 n=10 | CANDIDATE |
| F33 | MISSING | `footer:link=next-lesson` | 62 | 62 | 0.82 | 0.82 | template=Bilingual c=0.86 n=10 | CANDIDATE |
| F34 | MISSING | `footer:links=prev-lesson,home-nav` | 78 | 48 | 0.13 | 0.13 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F35 | MISSING | `footer:links=home-nav,prev-lesson,next-lesson` | 112 | 47 | 0.05 | 0.05 | subject+ptype=1-10 Health and PE/overview c=0.75 n=12 | CANDIDATE |
| F36 | EXTRA | `footer:link=prev-lesson` | 56 | 39 | 0.81 | 0.19 | template+ptype=Standard/overview c=0.97 n=12 | CANDIDATE |
| F37 | MISSING | `footer:ul=footer-nav` | 84 | 28 | 0.85 | 0.85 | ptype=lesson c=0.90 n=18 | CANDIDATE |
| F38 | MISSING | `footer:links=home-nav` | 37 | 24 | 0.04 | 0.04 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F39 | EXTRA | `footer:ul=footer-nav inquiry-nav` | 85 | 22 | 0.12 | 0.88 | ptype=lesson c=0.91 n=19 | CANDIDATE |
| F40 | MISSING | `footer:links=next-lesson,home-nav` | 22 | 22 | 0.12 | 0.12 | template+ptype=Standard/overview c=0.76 n=11 | CANDIDATE |
| F41 | EXTRA | `footer:ul=footer-nav` | 26 | 18 | 0.85 | 0.15 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F42 | MISSING | `footer:link=prev-lesson` | 17 | 16 | 0.81 | 0.81 | era=Refresh c=0.81 n=16 | CANDIDATE |
| F43 | MISSING | `footer:ul=footer-nav fundamentals-nav` | 19 | 10 | 0.02 | 0.02 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F44 | EXTRA | `footer:ul=footer-nav fundamentals-nav` | 16 | 9 | 0.02 | 0.98 | — | BELOW FLOOR |
| F45 | MISSING | `footer:ul=footer-nav inquiry-nav` | 14 | 7 | 0.12 | 0.12 | — | BELOW FLOOR |
| F46 | MISSING | `footer:links=home-nav,prev-lesson` | 7 | 7 | 0.00 | 0.00 | — | BELOW FLOOR |
| F47 | EXTRA | `footer:link=home-nav` | 11 | 5 | 0.99 | 0.01 | — | BELOW FLOOR |
| F48 | MISSING | `footer:links=prev-lesson,home-nav,next-lesson` | 30 | 4 | 0.01 | 0.01 | — | BELOW FLOOR |
| F49 | MISSING | `footer:link=other` | 19 | 3 | 0.01 | 0.01 | — | BELOW FLOOR |
| F50 | MISSING | `footer:links=prev-lesson,other,next-lesson,home-nav` | 14 | 3 | 0.01 | 0.01 | — | BELOW FLOOR |
| F51 | EXTRA | `footer:present` | 9 | 3 | 1.00 | 0.00 | — | BELOW FLOOR |
| F52 | MISSING | `footer:links=other,next-lesson,home-nav` | 3 | 3 | 0.00 | 0.00 | — | BELOW FLOOR |
| F53 | MISSING | `footer:links=prev-lesson,other,home-nav` | 2 | 2 | 0.00 | 0.00 | — | BELOW FLOOR |
| F54 | MISSING | `footer:links=prev-lesson,next-lesson` | 1 | 1 | 0.00 | 0.00 | — | BELOW FLOOR |
| F55 | MISSING | `footer:links=none` | 1 | 1 | 0.00 | 0.00 | — | BELOW FLOOR |
| F56 | EXTRA | `footer:links=home-nav` | 1 | 1 | 0.04 | 0.96 | — | BELOW FLOOR |

### F1 · MISSING `header:title-h1-count=2` — CANDIDATE (pages 259 / modules 127)
- by template+ptype: Standard/overview 54m/54p gold 0.65 Claude 0.53 c=0.65; Standard/lesson 41m/144p gold 0.10 Claude 0.02 c=0.10; Fundamentals/overview 29m/29p gold 0.69 Claude 0.38 c=0.69; Inquiry/overview 6m/6p gold 0.53 Claude 0.44 c=0.53; Bilingual/overview 5m/5p gold 1.00 Claude 0.72 c=1.00; Bilingual/lesson 5m/15p gold 1.00 Claude 0.72 c=1.00; Inquiry/lesson 3m/6p gold 0.14 Claude 0.02 c=0.14
- by subject: NCEA1 22m/56p gold 0.20 Claude 0.11 c=0.20; 1-10 English 21m/32p gold 0.18 Claude 0.09 c=0.18; Leaving to Learn 15m/23p gold 0.26 Claude 0.17 c=0.26; Online Safety (OS9000) 13m/29p gold 0.33 Claude 0.11 c=0.33; 1-10 Mathematics 11m/11p gold 0.14 Claude 0.11 c=0.14; 1-10 Technology 7m/19p gold 1.00 Claude 0.24 c=1.00; ANZH 6m/31p gold 0.49 Claude 0.17 c=0.49; ConnectED 6m/6p gold 0.23 Claude 0.18 c=0.23
- **AGH1005** AGH1005_0_0.html ↔ AGH1005.00.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=3']
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ANZH103** ANZH103_0_0.html ↔ ANZH103_0_0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: AGH1005, ANZH101, ANZH103, ANZH104, ANZH301, ANZH401, ANZH404, ARFUN01, ARFUN02, ARFUN03, ARFUN04, ARFUN05, ART1006, CEDK102, CEDK501, CEDO202, CEDO502, CEDR204, CEDT301, CHI1004, CHI1005, DTC1005, ENFUN01, ENFUN02 …

### F2 · EXTRA `header:title-h1-count=1` — CANDIDATE (pages 256 / modules 124)
- by template+ptype: Standard/overview 53m/53p gold 0.33 Claude 0.46 c=0.67; Standard/lesson 40m/143p gold 0.90 Claude 0.98 c=0.10; Fundamentals/overview 27m/27p gold 0.31 Claude 0.59 c=0.69; Inquiry/overview 7m/7p gold 0.42 Claude 0.56 c=0.58; Bilingual/overview 5m/5p gold 0.00 Claude 0.28 c=1.00; Bilingual/lesson 5m/15p gold 0.00 Claude 0.28 c=1.00; Inquiry/lesson 3m/6p gold 0.86 Claude 0.98 c=0.14
- by subject: 1-10 English 21m/32p gold 0.82 Claude 0.91 c=0.18; NCEA1 20m/54p gold 0.80 Claude 0.88 c=0.20; Leaving to Learn 15m/23p gold 0.74 Claude 0.83 c=0.26; Online Safety (OS9000) 13m/29p gold 0.67 Claude 0.89 c=0.33; 1-10 Mathematics 11m/11p gold 0.85 Claude 0.89 c=0.14; 1-10 Technology 7m/19p gold 0.00 Claude 0.76 c=1.00; ANZH 6m/31p gold 0.51 Claude 0.83 c=0.49; ConnectED 6m/6p gold 0.77 Claude 0.81 c=0.23
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ANZH103** ANZH103_0_0.html ↔ ANZH103_0_0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ANZH104** ANZH104_4_0.html ↔ ANZH104_04.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1']
- modules: ANZH101, ANZH103, ANZH104, ANZH301, ANZH401, ANZH404, ARFUN02, ARFUN03, ARFUN04, ARFUN05, ART1006, CEDK102, CEDK501, CEDO202, CEDO502, CEDR204, CEDT301, CHI1004, CHI1005, CHWHA, DTC1005, ENFUN01, ENFUN02, ENFUN03 …

### F3 · MISSING `header:chip=decimal-number` — CANDIDATE (pages 119 / modules 52)
- by template+ptype: Standard/lesson 41m/107p gold 0.71 Claude 0.75 c=0.71; Standard/overview 6m/6p gold 0.02 Claude 0.00 c=0.02; Bilingual/overview 3m/3p gold 0.17 Claude 0.00 c=0.17; Inquiry/overview 2m/2p gold 0.04 Claude 0.00 c=0.04; Fundamentals/overview 1m/1p gold 0.01 Claude 0.00 c=0.01
- by subject: 1-10 Blended Literacy 24m/46p gold 0.43 Claude 0.32 c=0.43; NCEA1 10m/35p gold 0.81 Claude 0.79 c=0.81; 1-10 Mathematics 6m/10p gold 0.72 Claude 0.74 c=0.72; Leaving to Learn 4m/12p gold 0.41 Claude 0.53 c=0.41; Te Marautanga o Aotearoa TMoA 3m/3p gold 0.62 Claude 0.65 c=0.62; 1-10 English 2m/9p gold 0.60 Claude 0.69 c=0.60; ConnectED 1m/1p gold 0.70 Claude 0.72 c=0.70; 1-10 Languages 1m/1p gold 0.48 Claude 0.63 c=0.48
- **ART1004** ART1004_0_0.html ↔ ART1004_4.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **ART1005** ART1005_0_0.html ↔ ART1005_3.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **BLL141** BLL141_1_0.html ↔ BLL141-1.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- modules: ART1004, ART1005, BLL141, BLL142, BLL143, BLL144, BLL145, BLL146, BLL147, BLL151, BLL152, BLL154, BLL156, BLL157, BLL161, BLL162, BLL163, BLL164, BLL165, BLL166, BLL167, BLL171, BLL172, BLL173 …

### F6 · MISSING `header:chip=module-code` — CANDIDATE (pages 72 / modules 39)
- by template+ptype: Standard/lesson 21m/47p gold 0.03 Claude 0.00 c=0.03; Standard/overview 7m/7p gold 0.74 Claude 0.76 c=0.74; Bilingual/lesson 4m/11p gold 0.21 Claude 0.00 c=0.21; Inquiry/overview 3m/3p gold 0.33 Claude 0.38 c=0.33; Inquiry/lesson 3m/3p gold 0.06 Claude 0.00 c=0.06; Fundamentals/overview 1m/1p gold 0.64 Claude 0.69 c=0.64
- by subject: 1-10 Blended Literacy 9m/9p gold 0.05 Claude 0.03 c=0.05; NCEA1 7m/7p gold 0.14 Claude 0.14 c=0.14; 1-10 Mathematics 5m/18p gold 0.16 Claude 0.11 c=0.16; Te Marautanga o Aotearoa TMoA 4m/11p gold 0.37 Claude 0.25 c=0.37; Leaving to Learn 3m/5p gold 0.15 Claude 0.17 c=0.15; ANZH 2m/13p gold 0.27 Claude 0.13 c=0.27; ConnectED 2m/2p gold 0.09 Claude 0.07 c=0.09; 1-10 Languages 2m/2p gold 0.23 Claude 0.21 c=0.23
- **ANZH401** ANZH401_1_0.html ↔ ANZH401_1.0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ANZHFUN05** MODULE_0_0.html ↔ ANZHFUN05_0_0.html: gold ['header:chip', 'header:chip=module-code', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2']
- **BLL170** BLL170_0_0.html ↔ BLL170.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: ANZH401, ANZHFUN05, BLL170, BLL172, BLL174, BLL175, BLL176, BLL177, BLL240, BLL252, BLL253, CEDK501, CEDT207, CHI1004, CHWHA, ENGR102, ENGS401, EXBP901, EXIP901, GEO1004, GEWHA, HES1006, HIS1002, HIS1003 …

### F8 · EXTRA `header:chip=lesson-number` — CANDIDATE (pages 83 / modules 35)
- by template+ptype: Standard/lesson 32m/77p gold 0.24 Claude 0.21 c=0.76; Bilingual/lesson 3m/6p gold 0.02 Claude 0.13 c=0.98
- by subject: 1-10 Blended Literacy 22m/44p gold 0.23 Claude 0.34 c=0.77; Leaving to Learn 5m/15p gold 0.40 Claude 0.30 c=0.60; Te Marautanga o Aotearoa TMoA 3m/6p gold 0.01 Claude 0.10 c=0.99; 1-10 English 2m/9p gold 0.23 Claude 0.16 c=0.77; ConnectED 1m/1p gold 0.07 Claude 0.07 c=0.94; NCEA1 1m/5p gold 0.04 Claude 0.02 c=0.95; 1-10 Mathematics 1m/3p gold 0.10 Claude 0.11 c=0.90
- **BLL141** BLL141_1_0.html ↔ BLL141-1.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- **BLL142** BLL142_1_0.html ↔ BLL142-1.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- **BLL143** BLL143_1_0.html ↔ BLL143-1.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- modules: BLL141, BLL142, BLL143, BLL144, BLL145, BLL146, BLL147, BLL151, BLL152, BLL154, BLL156, BLL157, BLL161, BLL162, BLL163, BLL164, BLL165, BLL166, BLL167, BLL171, BLL172, BLL173, CEDR501, ENGJ101 …

### F10 · EXTRA `header:chip=module-code` — CANDIDATE (pages 27 / modules 27)
- by template+ptype: Standard/overview 12m/12p gold 0.74 Claude 0.76 c=0.26; Inquiry/overview 5m/5p gold 0.33 Claude 0.38 c=0.67; Fundamentals/overview 5m/5p gold 0.64 Claude 0.69 c=0.36; Bilingual/overview 3m/3p gold 0.83 Claude 1.00 c=0.17; Standard/lesson 2m/2p gold 0.03 Claude 0.00 c=0.97
- by subject: Leaving to Learn 9m/9p gold 0.15 Claude 0.17 c=0.85; NCEA1 7m/7p gold 0.14 Claude 0.14 c=0.86; Te Marautanga o Aotearoa TMoA 3m/3p gold 0.37 Claude 0.25 c=0.63; 1-10 Health and PE 2m/2p gold 0.61 Claude 0.70 c=0.39; 1-10 Social Science 2m/2p gold 0.26 Claude 0.29 c=0.74; 1-10 Blended Literacy 1m/1p gold 0.05 Claude 0.03 c=0.95; 1-10 Languages 1m/1p gold 0.23 Claude 0.21 c=0.77; 1-10 Mathematics 1m/1p gold 0.16 Claude 0.11 c=0.84
- **ART1004** ART1004_0_0.html ↔ ART1004_4.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **ART1005** ART1005_0_0.html ↔ ART1005_3.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **BLL240** BLL240_0_0.html ↔ BLL240-0.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: ART1004, ART1005, BLL240, COM1002, ENG1004, ENGFUN02, FRFUN06, GEO1004, GER1002, HPFUN201, HPFUN302, MXDB201, OSOH101, SSFUN01, SSFUN07, TRR112, TRR113, TRR116, XDLS901, XDLS902, XDLS903, XDLS909, XFUN01, XGF9001 …

### F11 · EXTRA `header:chip=other` — CANDIDATE (pages 72 / modules 25)
- by template+ptype: Standard/lesson 15m/62p gold 0.01 Claude 0.04 c=0.99; Standard/overview 7m/7p gold 0.24 Claude 0.24 c=0.76; Inquiry/overview 2m/2p gold 0.07 Claude 0.04 c=0.93; Fundamentals/overview 1m/1p gold 0.00 Claude 0.01 c=1.00
- by subject: 1-10 Blended Literacy 8m/8p gold 0.27 Claude 0.29 c=0.73; 1-10 Mathematics 5m/7p gold 0.00 Claude 0.02 c=1.00; NCEA1 5m/30p gold 0.01 Claude 0.05 c=0.99; ANZH 2m/13p gold 0.07 Claude 0.21 c=0.94; 1-10 Languages 2m/2p gold 0.00 Claude 0.03 c=1.00; 1-10 Social Science 2m/11p gold 0.00 Claude 0.29 c=1.00; Leaving to Learn 1m/1p gold 0.04 Claude 0.01 c=0.96
- **ANZH401** ANZH401_1_0.html ↔ ANZH401_1.0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ANZHFUN05** MODULE_0_0.html ↔ ANZHFUN05_0_0.html: gold ['header:chip', 'header:chip=module-code', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2']
- **BLL172** BLL172_0_0.html ↔ BLL172-00.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: ANZH401, ANZHFUN05, BLL172, BLL174, BLL175, BLL176, BLL177, BLL252, BLL253, BLLR203, CHWHA, GEWHA, MXDB301, MXEO301, MXEX301, MXFL302, MXFU302, PWY1001, PWY1002, PWY1008, PWY1009, PWYWHA1, SSCI205, SSFUN07 …

### F12 · EXTRA `header:title-h1-count=2` — CANDIDATE (pages 22 / modules 21)
- by template+ptype: Standard/overview 12m/12p gold 0.65 Claude 0.53 c=0.35; Standard/lesson 4m/4p gold 0.10 Claude 0.02 c=0.90; Fundamentals/overview 4m/4p gold 0.69 Claude 0.38 c=0.31; Inquiry/overview 2m/2p gold 0.53 Claude 0.44 c=0.47
- by subject: NCEA1 7m/7p gold 0.20 Claude 0.11 c=0.80; Leaving to Learn 4m/4p gold 0.26 Claude 0.17 c=0.74; 1-10 Languages 3m/3p gold 0.28 Claude 0.23 c=0.72; 1-10 Writing (MiW) 2m/2p gold 0.62 Claude 0.52 c=0.38; ANZH 1m/2p gold 0.49 Claude 0.17 c=0.51; 1-10 Blended Literacy 1m/1p gold 0.01 Claude 0.01 c=0.99; ConnectED 1m/1p gold 0.23 Claude 0.18 c=0.77; 1-10 English 1m/1p gold 0.18 Claude 0.09 c=0.82
- **ANZH302** ANZH302_0_0.html ↔ ANZH302_0_0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2']
- **BLL246** BLL246_0_0.html ↔ BLL246_0.0.html: gold ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2']
- **CEDO105** CEDO105_0_0.html ↔ CEDO105.0.0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2']
- modules: ANZH302, BLL246, CEDO105, ENGFUN02, ENGI103, FRFUN06, GENO901, GEWHA, HIS1002, JPN1004, PHE1004, PWY1002, PWYWHA1, SPA1004, SSFUN07, WJFUN105, WJFUN116, XDLS904, XDLS906, XFUN02, XGF9004

### F13 · MISSING `header:head-buttons` — CANDIDATE (pages 34 / modules 19)
- by template+ptype: Standard/lesson 11m/17p gold 0.75 Claude 0.76 c=0.75; Bilingual/lesson 5m/12p gold 0.23 Claude 0.00 c=0.23; Inquiry/lesson 2m/3p gold 0.71 Claude 0.69 c=0.71; Standard/overview 2m/2p gold 0.98 Claude 0.99 c=0.98
- by subject: Te Marautanga o Aotearoa TMoA 5m/12p gold 0.38 Claude 0.25 c=0.38; 1-10 Blended Literacy 4m/8p gold 0.46 Claude 0.43 c=0.46; NCEA1 4m/4p gold 0.73 Claude 0.75 c=0.73; ConnectED 2m/3p gold 0.76 Claude 0.87 c=0.76; Leaving to Learn 2m/4p gold 0.88 Claude 0.87 c=0.88; EXPlore 1m/1p gold 1.00 Claude 0.93 c=1.00; 1-10 Mathematics 1m/2p gold 0.78 Claude 0.78 c=0.78
- **BLL114** BLL114_1_0.html ↔ BLL114-02.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- **BLL116** BLL116_1_0.html ↔ BLL116-02.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- **BLL153** BLL153_1_0.html ↔ BLL153-1.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- modules: BLL114, BLL116, BLL153, BLL236, CEDT207, CEDT301, EXPFUN07, GEO1004, HES1002, HES1006, MUS1004, MXFL401, PNR101, PNR102, PNR104, PNR107, TRR109, XGF9004, XLP06

### F14 · MISSING `header:title-h1-count=1` — CANDIDATE (pages 19 / modules 18)
- by template+ptype: Standard/overview 10m/10p gold 0.33 Claude 0.46 c=0.33; Standard/lesson 4m/4p gold 0.90 Claude 0.98 c=0.90; Fundamentals/overview 4m/4p gold 0.31 Claude 0.59 c=0.31; Inquiry/overview 1m/1p gold 0.42 Claude 0.56 c=0.42
- by subject: NCEA1 6m/6p gold 0.80 Claude 0.88 c=0.80; Leaving to Learn 4m/4p gold 0.74 Claude 0.83 c=0.74; 1-10 Writing (MiW) 2m/2p gold 0.38 Claude 0.48 c=0.38; ANZH 1m/2p gold 0.51 Claude 0.83 c=0.51; 1-10 Blended Literacy 1m/1p gold 0.99 Claude 0.99 c=0.99; ConnectED 1m/1p gold 0.77 Claude 0.81 c=0.77; 1-10 English 1m/1p gold 0.82 Claude 0.91 c=0.82; 1-10 Languages 1m/1p gold 0.68 Claude 0.77 c=0.68
- **ANZH302** ANZH302_0_0.html ↔ ANZH302_0_0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2']
- **ART1004** ART1004_0_0.html ↔ ART1004_4.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **ART1005** ART1005_0_0.html ↔ ART1005_3.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- modules: ANZH302, ART1004, ART1005, BLL246, CEDO105, ENGFUN02, ENGI103, FRFUN06, HIS1002, PWY1002, PWYWHA1, SSFUN07, WJFUN105, WJFUN116, XDLS904, XDLS906, XFUN02, XGF9004

### F23 · MISSING `nav:phases` — CANDIDATE (pages 20 / modules 11)
- by template+ptype: Fundamentals/overview 10m/10p gold 0.99 Claude 0.86 c=0.99; Fundamentals/lesson 1m/9p gold 0.25 Claude 0.00 c=0.25; Standard/lesson 1m/1p gold 0.00 Claude 0.00 c=0.00
- by subject: 1-10 Languages 5m/14p gold 0.31 Claude 0.09 c=0.31; 1-10 Mathematics 3m/3p gold 0.01 Claude 0.00 c=0.01; ANZH 1m/1p gold 0.01 Claude 0.00 c=0.01; 1-10 Arts 1m/1p gold 1.00 Claude 0.80 c=1.00; 1-10 Social Science 1m/1p gold 0.18 Claude 0.16 c=0.18
- **ANZHFUN05** MODULE_0_0.html ↔ ANZHFUN05_0_0.html: gold ['nav:phases'] · Claude []
- **ARFUN04** ARFUN04_0_0.html ↔ ARFUN04_0.00.html: gold ['nav:phases'] · Claude []
- **FRFUN06** FRFUN06_0_0.html ↔ FRFUN06_1_0_Novice.html: gold ['nav:phases'] · Claude ['nav:crumbs']
- modules: ANZHFUN05, ARFUN04, FRFUN06, FRFUN07, FRFUN08, JPFUN01, JPFUN02, MXFUN01, MXFUN02, MXFUN03, SSFUN07

### F26 · MISSING `footer:inside-body` — CANDIDATE (pages 169 / modules 127)
- by template+ptype: Standard/lesson 65m/88p gold 0.05 Claude 0.00 c=0.05; Standard/overview 45m/45p gold 0.14 Claude 0.00 c=0.14; Fundamentals/overview 19m/19p gold 0.23 Claude 0.00 c=0.23; Inquiry/overview 10m/10p gold 0.22 Claude 0.00 c=0.22; Inquiry/lesson 2m/2p gold 0.04 Claude 0.00 c=0.04; Fundamentals/lesson 2m/3p gold 0.08 Claude 0.00 c=0.08; Bilingual/lesson 1m/1p gold 0.02 Claude 0.00 c=0.02; Bilingual/overview 1m/1p gold 0.06 Claude 0.00 c=0.06
- by subject: 1-10 Blended Literacy 35m/46p gold 0.17 Claude 0.00 c=0.17; 1-10 English 16m/22p gold 0.06 Claude 0.00 c=0.06; 1-10 Mathematics 15m/28p gold 0.08 Claude 0.00 c=0.08; NCEA1 12m/18p gold 0.03 Claude 0.00 c=0.03; 1-10 Languages 11m/12p gold 0.18 Claude 0.00 c=0.18; Leaving to Learn 10m/11p gold 0.05 Claude 0.00 c=0.05; Te ara Whakapuawa -Wellbeing 5m/5p gold 0.62 Claude 0.00 c=0.62; 1-10 Arts 4m/4p gold 0.80 Claude 0.00 c=0.80
- **ANZH101** ANZH101_0_0.html ↔ ANZH101_0.0.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH103** ANZH103_0_0.html ↔ ANZH103_0_0.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH302** ANZH302_3_0.html ↔ ANZH302_3_0.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: ANZH101, ANZH103, ANZH302, ARFUN02, ARFUN03, ARFUN04, ARFUN05, BLL113, BLL120, BLL122, BLL124, BLL125, BLL130, BLL145, BLL154, BLL156, BLL162, BLL164, BLL165, BLL166, BLL171, BLL173, BLL211, BLL212 …

### F27 · EXTRA `footer:links=prev-lesson,next-lesson,home-nav` — CANDIDATE (pages 276 / modules 121)
- by template+ptype: Standard/lesson 75m/203p gold 0.75 Claude 0.84 c=0.25; Inquiry/overview 23m/23p gold 0.18 Claude 0.69 c=0.82; Standard/overview 12m/12p gold 0.03 Claude 0.05 c=0.97; Fundamentals/overview 12m/12p gold 0.05 Claude 0.18 c=0.95; Inquiry/lesson 6m/16p gold 0.53 Claude 0.84 c=0.47; Bilingual/lesson 2m/2p gold 0.81 Claude 0.66 c=0.19; Fundamentals/lesson 1m/8p gold 0.69 Claude 0.89 c=0.31
- by subject: NCEA1 36m/60p gold 0.74 Claude 0.82 c=0.26; 1-10 Health and PE 12m/12p gold 0.39 Claude 0.91 c=0.61; 1-10 Blended Literacy 11m/14p gold 0.43 Claude 0.43 c=0.57; ConnectED 11m/17p gold 0.68 Claude 0.81 c=0.32; Leaving to Learn 10m/39p gold 0.52 Claude 0.69 c=0.48; 1-10 English 9m/35p gold 0.64 Claude 0.72 c=0.36; 1-10 Mathematics 9m/52p gold 0.62 Claude 0.77 c=0.38; Te ara Whakapuawa -Wellbeing 6m/6p gold 0.00 Claude 0.75 c=1.00
- **AGH1008** AGH1008_8_0.html ↔ AGH1008.08.html: gold ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH401** ANZH401_1_0.html ↔ ANZH401_1.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH404** ANZH404_1_0.html ↔ ANZH404_1.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: AGH1008, ANZH401, ANZH404, ART1002, BLL120, BLL140, BLL150, BLL170, BLL175, BLL210, BLL220, BLL230, BLL240, BLLR202, BLLR203, CBI1004, CBI1005, CBI1008, CBI1009, CEDK101, CEDK102, CEDK501, CEDO102, CEDO202 …

### F28 · EXTRA `footer:links=next-lesson,home-nav` — CANDIDATE (pages 101 / modules 100)
- by template+ptype: Standard/overview 74m/74p gold 0.76 Claude 0.95 c=0.24; Fundamentals/overview 11m/11p gold 0.01 Claude 0.15 c=0.99; Inquiry/overview 10m/10p gold 0.02 Claude 0.22 c=0.98; Standard/lesson 3m/3p gold 0.01 Claude 0.00 c=0.99; Bilingual/overview 3m/3p gold 0.83 Claude 1.00 c=0.17
- by subject: Leaving to Learn 27m/27p gold 0.03 Claude 0.17 c=0.97; NCEA1 14m/15p gold 0.11 Claude 0.12 c=0.89; 1-10 Mathematics 13m/13p gold 0.07 Claude 0.11 c=0.93; Online Safety (OS9000) 9m/9p gold 0.15 Claude 0.21 c=0.85; 1-10 English 8m/8p gold 0.11 Claude 0.13 c=0.89; 1-10 Blended Literacy 6m/6p gold 0.29 Claude 0.29 c=0.71; 1-10 Social Science 6m/6p gold 0.13 Claude 0.29 c=0.87; ConnectED 5m/5p gold 0.07 Claude 0.09 c=0.94
- **ANZH401** ANZH401_0_0.html ↔ ANZH401_0.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH404** ANZH404_0_0.html ↔ ANZH404_0.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZHFUN05** MODULE_0_0.html ↔ ANZHFUN05_0_0.html: gold ['footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav fundamentals-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: ANZH401, ANZH404, ANZHFUN05, ART1004, ART1005, BLL114, BLL116, BLL174, BLL175, BLL176, BLL177, CEDO301, CEDT104, CEDT207, CEDT208, CEDT301, CHWHA, COM1002, ENG1004, ENGFUN02, ENGI101, ENGI102, ENGJ101, ENGJ102 …

### F29 · EXTRA `footer:links=prev-lesson,home-nav` — CANDIDATE (pages 73 / modules 73)
- by template+ptype: Standard/lesson 57m/57p gold 0.16 Claude 0.16 c=0.84; Bilingual/lesson 11m/11p gold 0.15 Claude 0.34 c=0.85; Inquiry/lesson 3m/3p gold 0.22 Claude 0.16 c=0.78; Fundamentals/lesson 2m/2p gold 0.06 Claude 0.11 c=0.94
- by subject: 1-10 Blended Literacy 16m/16p gold 0.24 Claude 0.29 c=0.76; 1-10 English 12m/12p gold 0.10 Claude 0.13 c=0.90; Te Marautanga o Aotearoa TMoA 11m/11p gold 0.11 Claude 0.25 c=0.89; NCEA1 8m/8p gold 0.11 Claude 0.06 c=0.89; 1-10 Mathematics 8m/8p gold 0.09 Claude 0.11 c=0.91; ANZH 5m/5p gold 0.08 Claude 0.13 c=0.92; Leaving to Learn 4m/4p gold 0.29 Claude 0.15 c=0.71; ConnectED 3m/3p gold 0.05 Claude 0.07 c=0.95
- **AGH1004** AGH1004_6_0.html ↔ AGH1004.07.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **AGH1009** AGH1009_9_0.html ↔ AGH1009.09.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH103** ANZH103_1_0.html ↔ ANZH103_3_0.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: AGH1004, AGH1009, ANZH103, ANZH205, ANZH301, ANZH302, ANZH303, BLL141, BLL146, BLL151, BLL157, BLL167, BLL171, BLL176, BLL177, BLL224, BLL225, BLL226, BLL227, BLL231, BLL234, BLL236, BLL237, CEDO501 …

### F32 · MISSING `footer:links=prev-lesson,next-lesson,home-nav` — CANDIDATE (pages 66 / modules 63)
- by template+ptype: Standard/lesson 45m/45p gold 0.75 Claude 0.84 c=0.75; Bilingual/lesson 10m/10p gold 0.81 Claude 0.66 c=0.81; Standard/overview 5m/5p gold 0.03 Claude 0.05 c=0.03; Bilingual/overview 3m/3p gold 0.17 Claude 0.00 c=0.17; Inquiry/lesson 1m/1p gold 0.53 Claude 0.84 c=0.53; Fundamentals/lesson 1m/1p gold 0.69 Claude 0.89 c=0.69; Fundamentals/overview 1m/1p gold 0.05 Claude 0.18 c=0.05
- by subject: 1-10 Blended Literacy 14m/14p gold 0.43 Claude 0.43 c=0.43; NCEA1 12m/13p gold 0.74 Claude 0.82 c=0.74; Te Marautanga o Aotearoa TMoA 11m/13p gold 0.65 Claude 0.49 c=0.65; 1-10 English 7m/7p gold 0.64 Claude 0.72 c=0.64; ANZH 5m/5p gold 0.61 Claude 0.73 c=0.61; Leaving to Learn 4m/4p gold 0.52 Claude 0.69 c=0.52; 1-10 Mathematics 3m/3p gold 0.62 Claude 0.77 c=0.62; ConnectED 2m/2p gold 0.68 Claude 0.81 c=0.68
- **AGH1004** AGH1004_6_0.html ↔ AGH1004.07.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **AGH1009** AGH1009_9_0.html ↔ AGH1009.09.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH103** ANZH103_1_0.html ↔ ANZH103_3_0.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: AGH1004, AGH1009, ANZH103, ANZH205, ANZH301, ANZH302, ANZH303, ART1005, BLL141, BLL146, BLL151, BLL157, BLL167, BLL171, BLL224, BLL225, BLL226, BLL227, BLL231, BLL234, BLL236, BLL237, CEDO501, CEDT207 …

### F33 · MISSING `footer:link=next-lesson` — CANDIDATE (pages 62 / modules 62)
- by template+ptype: Standard/lesson 49m/49p gold 0.83 Claude 0.84 c=0.83; Bilingual/lesson 10m/10p gold 0.81 Claude 0.66 c=0.81; Inquiry/lesson 2m/2p gold 0.69 Claude 0.84 c=0.69; Fundamentals/lesson 1m/1p gold 0.69 Claude 0.89 c=0.69
- by subject: 1-10 Blended Literacy 16m/16p gold 0.75 Claude 0.71 c=0.75; Te Marautanga o Aotearoa TMoA 10m/10p gold 0.86 Claude 0.75 c=0.86; 1-10 English 8m/8p gold 0.86 Claude 0.85 c=0.86; 1-10 Mathematics 7m/7p gold 0.90 Claude 0.88 c=0.90; NCEA1 6m/6p gold 0.88 Claude 0.94 c=0.88; ANZH 5m/5p gold 0.91 Claude 0.87 c=0.91; ConnectED 3m/3p gold 0.94 Claude 0.93 c=0.94; Leaving to Learn 3m/3p gold 0.65 Claude 0.85 c=0.65
- **AGH1004** AGH1004_6_0.html ↔ AGH1004.07.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **AGH1009** AGH1009_9_0.html ↔ AGH1009.09.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH103** ANZH103_1_0.html ↔ ANZH103_3_0.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: AGH1004, AGH1009, ANZH103, ANZH205, ANZH301, ANZH302, ANZH303, BLL141, BLL146, BLL151, BLL157, BLL167, BLL171, BLL176, BLL177, BLL224, BLL225, BLL226, BLL227, BLL231, BLL234, BLL236, BLL237, CEDO501 …

### F35 · MISSING `footer:links=home-nav,prev-lesson,next-lesson` — CANDIDATE (pages 112 / modules 47)
- by template+ptype: Inquiry/overview 22m/22p gold 0.53 Claude 0.04 c=0.53; Fundamentals/overview 12m/12p gold 0.15 Claude 0.00 c=0.15; Standard/lesson 11m/76p gold 0.04 Claude 0.00 c=0.04; Inquiry/lesson 2m/2p gold 0.04 Claude 0.00 c=0.04
- by subject: ConnectED 12m/12p gold 0.13 Claude 0.02 c=0.13; 1-10 Health and PE 12m/12p gold 0.52 Claude 0.00 c=0.52; Te ara Whakapuawa -Wellbeing 6m/6p gold 0.75 Claude 0.00 c=0.75; 1-10 Blended Literacy 5m/5p gold 0.02 Claude 0.00 c=0.02; 1-10 English 5m/32p gold 0.09 Claude 0.00 c=0.09; 1-10 Mathematics 5m/40p gold 0.12 Claude 0.00 c=0.12; EXPlore 1m/1p gold 0.07 Claude 0.00 c=0.07; Online Safety (OS9000) 1m/4p gold 0.03 Claude 0.00 c=0.03
- **BLL170** BLL170_0_0.html ↔ BLL170.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=home-nav,prev-lesson,next-lesson', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL210** BLL210_0_0.html ↔ BLL210.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=home-nav,prev-lesson,next-lesson', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL220** BLL220_0_0.html ↔ BLL220.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=home-nav,prev-lesson,next-lesson', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL170, BLL210, BLL220, BLL230, BLL240, CEDK101, CEDK102, CEDK501, CEDO102, CEDO202, CEDO204, CEDR204, CEDT104, CEDT207, CEDT208, CEDT301, CEDW201, ENGJ101, ENGJ301, ENGJ302, ENGJ402, ENGJ403, EXPFUN06, HPFUN101 …

### F36 · EXTRA `footer:link=prev-lesson` — CANDIDATE (pages 56 / modules 39)
- by template+ptype: Standard/lesson 18m/23p gold 0.99 Claude 1.00 c=0.01; Standard/overview 12m/12p gold 0.03 Claude 0.05 c=0.97; Inquiry/overview 4m/4p gold 0.71 Claude 0.73 c=0.29; Inquiry/lesson 3m/6p gold 0.88 Claude 1.00 c=0.12; Fundamentals/lesson 1m/9p gold 0.75 Claude 1.00 c=0.25; Bilingual/lesson 1m/2p gold 0.96 Claude 1.00 c=0.04
- by subject: NCEA1 17m/21p gold 0.86 Claude 0.89 c=0.14; 1-10 Blended Literacy 9m/9p gold 0.68 Claude 0.71 c=0.32; EXPlore 3m/3p gold 0.73 Claude 0.93 c=0.27; ConnectED 2m/2p gold 0.92 Claude 0.91 c=0.08; 1-10 Mathematics 2m/2p gold 0.88 Claude 0.88 c=0.12; Leaving to Learn 2m/6p gold 0.81 Claude 0.83 c=0.19; 1-10 English 1m/1p gold 0.84 Claude 0.85 c=0.15; 1-10 Languages 1m/9p gold 0.61 Claude 0.75 c=0.39
- **BLL120** BLL120_0_0.html ↔ BLL120.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL140** BLL140_0_0.html ↔ BLL140.html: gold ['footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL150** BLL150_0_0.html ↔ BLL150.html: gold ['footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL120, BLL140, BLL150, BLL175, BLL176, BLL177, BLL240, BLLR202, BLLR203, CBI1005, CBI1008, CBI1009, CEDK501, CEDT207, CHI1003, CHI1004, CHI1005, COM1005, ENGFUN02, ENGR102, EXBP901, EXIP901, EXPFUN07, FRFUN06 …

### F37 · MISSING `footer:ul=footer-nav` — CANDIDATE (pages 84 / modules 28)
- by template+ptype: Standard/lesson 15m/44p gold 0.90 Claude 0.88 c=0.90; Standard/overview 11m/11p gold 0.76 Claude 0.73 c=0.76; Fundamentals/overview 9m/9p gold 0.48 Claude 0.47 c=0.48; Inquiry/overview 3m/3p gold 0.16 Claude 0.18 c=0.16; Inquiry/lesson 3m/17p gold 0.96 Claude 0.61 c=0.96
- by subject: 1-10 Blended Literacy 12m/41p gold 0.15 Claude 0.00 c=0.15; 1-10 Technology 5m/5p gold 0.88 Claude 0.68 c=0.88; ConnectED 4m/21p gold 0.86 Claude 0.69 c=0.86; EXPlore 2m/5p gold 0.53 Claude 0.27 c=0.53; 1-10 Mathematics 2m/2p gold 0.98 Claude 0.99 c=0.98; 1-10 Health and PE 1m/1p gold 0.52 Claude 0.48 c=0.52; NCEA1 1m/8p gold 1.00 Claude 0.98 c=1.00; 1-10 Writing (MiW) 1m/1p gold 0.62 Claude 0.71 c=0.62
- **BLL121** BLL121_0_0.html ↔ BLL121-01.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL172** BLL172_0_0.html ↔ BLL172-00.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL174** BLL174_0_0.html ↔ BLL174-00.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL121, BLL172, BLL174, BLL175, BLL176, BLL177, BLL236, BLL237, BLL240, BLL241, BLL244, BLL245, CEDR501, CEDT207, CEDT301, CEDW101, EXBP901, EXIP901, HPFUN301, MXFUN02, MXFUN03, MXS1004, TEFUN01, TEFUN02 …

### F39 · EXTRA `footer:ul=footer-nav inquiry-nav` — CANDIDATE (pages 85 / modules 22)
- by template+ptype: Standard/lesson 15m/41p gold 0.10 Claude 0.11 c=0.91; Standard/overview 12m/12p gold 0.23 Claude 0.27 c=0.77; Inquiry/overview 3m/3p gold 0.84 Claude 0.82 c=0.16; Inquiry/lesson 3m/17p gold 0.04 Claude 0.39 c=0.96; Fundamentals/overview 3m/3p gold 0.00 Claude 0.04 c=1.00; Fundamentals/lesson 1m/9p gold 0.00 Claude 0.25 c=1.00
- by subject: 1-10 Blended Literacy 12m/41p gold 0.85 Claude 1.00 c=0.15; ConnectED 4m/21p gold 0.14 Claude 0.32 c=0.86; EXPlore 2m/5p gold 0.47 Claude 0.73 c=0.53; 1-10 Mathematics 2m/2p gold 0.02 Claude 0.01 c=0.98; 1-10 Languages 1m/10p gold 0.03 Claude 0.15 c=0.97; Leaving to Learn 1m/6p gold 0.02 Claude 0.04 c=0.98
- **BLL121** BLL121_0_0.html ↔ BLL121-01.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL172** BLL172_0_0.html ↔ BLL172-00.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL174** BLL174_0_0.html ↔ BLL174-00.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL121, BLL172, BLL174, BLL175, BLL176, BLL177, BLL236, BLL237, BLL240, BLL241, BLL244, BLL245, CEDR501, CEDT207, CEDT301, CEDW101, EXBP901, EXIP901, FRFUN06, MXFUN02, MXFUN03, XWHA02

### F40 · MISSING `footer:links=next-lesson,home-nav` — CANDIDATE (pages 22 / modules 22)
- by template+ptype: Standard/overview 11m/11p gold 0.76 Claude 0.95 c=0.76; Standard/lesson 8m/8p gold 0.01 Claude 0.00 c=0.01; Inquiry/lesson 2m/2p gold 0.04 Claude 0.00 c=0.04; Inquiry/overview 1m/1p gold 0.02 Claude 0.22 c=0.02
- by subject: NCEA1 13m/13p gold 0.11 Claude 0.12 c=0.11; 1-10 Blended Literacy 6m/6p gold 0.29 Claude 0.29 c=0.29; ConnectED 2m/2p gold 0.07 Claude 0.09 c=0.07; 1-10 English 1m/1p gold 0.11 Claude 0.13 c=0.11
- **BLL175** BLL175_1_1.html ↔ BLL175-02.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL176** BLL176_1_1.html ↔ BLL176-2.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL177** BLL177_2_0.html ↔ BLL177-2.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL175, BLL176, BLL177, BLL240, BLLR202, BLLR203, CBI1005, CBI1008, CBI1009, CEDK501, CEDT207, CHI1003, CHI1004, CHI1005, ENGR102, GEO1004, GEO1005, GEO1006, HES1006, JPN1004, MXS1004, PES1005

### F42 · MISSING `footer:link=prev-lesson` — CANDIDATE (pages 17 / modules 16)
- by template+ptype: Standard/overview 7m/7p gold 0.03 Claude 0.05 c=0.03; Inquiry/overview 3m/3p gold 0.71 Claude 0.73 c=0.71; Standard/lesson 3m/3p gold 0.99 Claude 1.00 c=0.99; Bilingual/overview 3m/3p gold 0.17 Claude 0.00 c=0.17; Fundamentals/overview 1m/1p gold 0.20 Claude 0.18 c=0.20
- by subject: NCEA1 7m/8p gold 0.86 Claude 0.89 c=0.86; ConnectED 3m/3p gold 0.92 Claude 0.91 c=0.92; Te Marautanga o Aotearoa TMoA 3m/3p gold 0.76 Claude 0.75 c=0.76; 1-10 Mathematics 1m/1p gold 0.88 Claude 0.88 c=0.88; 1-10 Social Science 1m/1p gold 0.71 Claude 0.71 c=0.71; Leaving to Learn 1m/1p gold 0.81 Claude 0.83 c=0.81
- **ART1004** ART1004_0_0.html ↔ ART1004_4.0.html: gold ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ART1005** ART1005_0_0.html ↔ ART1005_3.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **CEDT104** CEDT104_0_0.html ↔ CEDT104 Waiata In Motion.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=home-nav,prev-lesson,next-lesson', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: ART1004, ART1005, CEDT104, CEDT207, CEDT208, COM1002, ENG1004, GER1002, MXFL101, PES1002, PWYWHA1, SSFUN02, TRR112, TRR113, TRR116, XGF9001


## The ranked queue — chrome regions first, then by modules affected

| # | region | dir | parent | gold form | Claude form | pages | modules | consensus (all) | best group | derivable | KB | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | module-code | EXTRA | `div#header` | `—` | `div#module-code` | 4 | 4 | 0.03 of 2349 | — | structure | yes | BELOW FLOOR |
| 2 | module-code | MISSING | `div#header` | `div#module-code` | `—` | 3 | 3 | 0.97 of 2349 | — | structure | yes | BELOW FLOOR |
| 3 | module-code | EXTRA | `div#module-code` | `—` | `h1` | 1 | 1 | 0.03 of 2349 | — | structure | yes | BELOW FLOOR |
| 4 | title | MISSING | `div#header` | `h1>span` | `—` | 246 | 127 | 0.23 of 2349 | subject+ptype=Online Safety (OS9000)/overview c=0.93 n=12 | 0.76 | yes | CANDIDATE |
| 5 | title | EXTRA | `div#header` | `—` | `h1>span` | 17 | 16 | 0.77 of 2349 | template=Standard c=0.82 n=11 | structure | yes | CANDIDATE |
| 6 | title | SUBSTITUTED | `div#header` | `h1>span` | `div#module-head-buttons` | 5 | 5 | 1.00 of 2349 | — | structure | yes | BELOW FLOOR |
| 7 | title | MISSING | `span>span.sassoonI-text` | `span.sassoonI-text` | `—` | 14 | 4 | 0.01 of 2349 | — | 0.79 | — | BELOW FLOOR |
| 8 | title | MISSING | `div#header` | `h1>span.ch-text` | `—` | 14 | 2 | 0.01 of 2349 | — | 0.00 | yes | BELOW FLOOR |
| 9 | title | MISSING | `span` | `apan.jp-text` | `—` | 10 | 1 | 0.00 of 2349 | — | 0.90 | yes | BELOW FLOOR |
| 10 | title | SUBSTITUTED | `h1>span.ch-text` | `span.ch-text` | `span` | 7 | 1 | 0.01 of 2349 | — | structure | yes | BELOW FLOOR |
| 11 | title | MISSING | `div.titlebar` | `h1.moduleTitle>span.module-subtitle.text-lowercase` | `—` | 2 | 1 | 0.00 of 2349 | — | 1.00 | — | BELOW FLOOR |
| 12 | title | EXTRA | `span>span` | `—` | `span` | 1 | 1 | 0.99 of 2349 | — | structure | — | BELOW FLOOR |
| 13 | title | EXTRA | `h1>span` | `—` | `span` | 1 | 1 | 0.01 of 2349 | — | structure | — | BELOW FLOOR |
| 14 | title | EXTRA | `msub` | `—` | `mrow` | 1 | 1 | 1.00 of 2349 | — | structure | — | BELOW FLOOR |
| 15 | title | EXTRA | `mfrac` | `—` | `mrow` | 1 | 1 | 1.00 of 2349 | — | structure | — | BELOW FLOOR |
| 16 | title | EXTRA | `mrow` | `—` | `mi` | 1 | 1 | 1.00 of 2349 | — | structure | — | BELOW FLOOR |
| 17 | title | EXTRA | `msup` | `—` | `mrow` | 1 | 1 | 1.00 of 2349 | — | structure | — | BELOW FLOOR |
| 18 | title | MISSING | `span>span` | `span` | `—` | 1 | 1 | 0.01 of 2349 | — | 1.00 | — | BELOW FLOOR |
| 19 | title | MISSING | `span>span.ch-text` | `span.ch-text` | `—` | 1 | 1 | 0.00 of 2349 | — | 0.00 | yes | BELOW FLOOR |
| 20 | title | MISSING | `span>span.text-lowercase` | `span.text-lowercase` | `—` | 1 | 1 | 0.00 of 2349 | — | 1.00 | — | BELOW FLOOR |
| 21 | title | MISSING | `div#header` | `h1>span.jp-text` | `—` | 1 | 1 | 0.00 of 2349 | — | 1.00 | yes | BELOW FLOOR |
| 22 | title | MISSING | `msup` | `mn` | `—` | 1 | 1 | 0.00 of 2349 | — | 1.00 | — | BELOW FLOOR |
| 23 | title | SUBSTITUTED | `msub` | `mi` | `mrow` | 1 | 1 | 0.00 of 2349 | — | structure | — | BELOW FLOOR |
| 24 | title | SUBSTITUTED | `msub` | `mi` | `mi` | 1 | 1 | 0.00 of 2349 | — | structure | — | BELOW FLOOR |
| 25 | title | SUBSTITUTED | `mfrac` | `mn` | `mrow` | 1 | 1 | 0.00 of 2349 | — | structure | — | BELOW FLOOR |
| 26 | title | SUBSTITUTED | `mfrac` | `mn` | `mn` | 1 | 1 | 0.00 of 2349 | — | structure | — | BELOW FLOOR |
| 27 | title | SUBSTITUTED | `msup` | `mi` | `mrow` | 1 | 1 | 0.00 of 2349 | — | structure | — | BELOW FLOOR |
| 28 | title | SUBSTITUTED | `div#header` | `h1>span` | `div#module-code` | 1 | 1 | 1.00 of 2349 | — | structure | yes | BELOW FLOOR |
| 29 | header | MISSING | `div#header` | `p` | `—` | 3 | 1 | 0.00 of 2349 | — | 0.00 | yes | BELOW FLOOR |
| 30 | header | SUBSTITUTED | `div#header` | `div.titlebar` | `h1>span` | 2 | 1 | 0.00 of 2349 | — | structure | yes | BELOW FLOOR |
| 31 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `p` | `h5` | 83 | 83 | 0.06 of 2349 | subject+ptype=1-10 Health and PE/overview c=0.88 n=14 | structure | yes | CANDIDATE |
| 32 | module-menu | MISSING | `ul` | `li` | `—` | 127 | 77 | 0.10 of 2349 | subject+ptype=1-10 Blended Literacy/overview c=0.64 n=21 | 0.84 | — | CANDIDATE |
| 33 | module-menu | MISSING | `div.col-12.col-md-8` | `ul` | `—` | 202 | 53 | 0.29 of 2349 | subject+ptype=1-10 English/lesson c=0.72 n=11 | 0.92 | — | CANDIDATE |
| 34 | module-menu | MISSING | `div.col-12.col-md-8` | `h5` | `—` | 200 | 45 | 0.24 of 2349 | subject+ptype=1-10 English/lesson c=0.64 n=12 | 0.83 | — | CANDIDATE |
| 35 | module-menu | MISSING | `div.col-12.col-md-8` | `p` | `—` | 207 | 44 | 0.10 of 2349 | — | 0.84 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 36 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-6.paddingR` | 64 | 44 | 0.97 of 2349 | era=Refresh c=0.97 n=44 | structure | yes | CANDIDATE |
| 37 | module-menu | EXTRA | `ul` | `—` | `li` | 80 | 42 | 0.79 of 2349 | ptype=lesson c=0.83 n=14 | structure | — | CANDIDATE |
| 38 | module-menu | EXTRA | `div#header` | `—` | `div#module-menu-content.moduleMenu` | 75 | 39 | 0.25 of 2349 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 39 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingL` | `p` | `h5` | 38 | 38 | 0.03 of 2349 | subject+ptype=1-10 Health and PE/overview c=0.88 n=14 | structure | yes | CANDIDATE |
| 40 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `p` | `—` | 50 | 36 | 0.04 of 2349 | subject+ptype=1-10 Blended Literacy/overview c=0.76 n=23 | 0.72 | yes | CANDIDATE |
| 41 | module-menu | EXTRA | `div#header` | `—` | `div#module-head-buttons` | 63 | 31 | 0.23 of 2349 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 42 | module-menu | MOVED | `ul` | `li` | `li>i` | 75 | 29 | 0.26 of 2349 | — | structure | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 43 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `h5` | 81 | 25 | 0.76 of 2349 | era=Refresh c=0.76 n=25 | structure | — | CANDIDATE |
| 44 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 55 | 25 | 0.87 of 2349 | era=Refresh c=0.87 n=25 | structure | — | CANDIDATE |
| 45 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `ul` | `—` | 33 | 22 | 0.05 of 2349 | — | 0.79 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 46 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `p>b` | 22 | 22 | 1.00 of 2349 | era=Refresh c=1.00 n=22 | structure | yes | CANDIDATE |
| 47 | module-menu | SUBSTITUTED | `ul` | `li` | `li` | 87 | 20 | 0.58 of 2349 | template+ptype=Standard/lesson c=0.64 n=16 | structure | — | CANDIDATE |
| 48 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6.paddingL` | `—` | 39 | 20 | 0.04 of 2349 | — | 1.00 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 49 | module-menu | MISSING | `p` | `br` | `—` | 35 | 20 | 0.01 of 2349 | — | structure | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 50 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `p` | `h5` | 26 | 20 | 0.04 of 2349 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 51 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `—` | 88 | 19 | 0.03 of 2349 | — | 0.96 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 52 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6.offset-md-0` | `—` | 79 | 19 | 0.05 of 2349 | — | 0.86 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 53 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `h4>span` | `—` | 19 | 19 | 0.01 of 2349 | — | 1.00 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 54 | module-menu | EXTRA | `div.col-12.col-md-6.offset-md-0` | `—` | `p` | 24 | 18 | 0.99 of 2349 | era=Refresh c=0.99 n=18 | structure | yes | CANDIDATE |
| 55 | module-menu | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `h5` | 62 | 17 | 0.13 of 2349 | — | structure | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 56 | module-menu | MISSING | `div#header` | `div#module-head-buttons` | `—` | 31 | 17 | 0.77 of 2349 | template=Standard c=0.78 n=10 | structure | yes | CANDIDATE |
| 57 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `p` | 17 | 17 | 0.95 of 2349 | template=Standard c=0.95 n=14 | structure | yes | CANDIDATE |
| 58 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-8` | 98 | 16 | 0.66 of 2349 | subject=1-10 Mathematics c=0.77 n=12 | structure | — | CANDIDATE |
| 59 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `ul` | 43 | 16 | 0.71 of 2349 | era=Refresh c=0.71 n=16 | structure | — | CANDIDATE |
| 60 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `h4>span` | `h5>span` | 15 | 15 | 0.03 of 2349 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 61 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0` | `ul` | `—` | 72 | 14 | 0.02 of 2349 | — | 0.89 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 62 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-6.offset-md-0` | 30 | 14 | 0.95 of 2349 | era=Refresh c=0.95 n=14 | structure | yes | CANDIDATE |
| 63 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-12.paddingR` | 16 | 14 | 0.96 of 2349 | template=Standard c=0.96 n=14 | structure | yes | CANDIDATE |
| 64 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `ul` | `p>b` | 14 | 14 | 0.06 of 2349 | subject+ptype=1-10 Blended Literacy/overview c=0.82 n=14 | structure | yes | CANDIDATE |
| 65 | module-menu | MISSING | `div#module-menu-content.moduleMenu` | `ul` | `—` | 88 | 13 | 0.04 of 2349 | — | 0.91 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 66 | module-menu | SUBSTITUTED | `div#module-menu-content.moduleMenu` | `h5` | `div.row` | 82 | 13 | 0.04 of 2349 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 67 | module-menu | SUBSTITUTED | `div#module-menu-content.moduleMenu` | `div.item` | `div.row` | 82 | 12 | 0.04 of 2349 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 68 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `h5` | 14 | 12 | 0.99 of 2349 | ptype=overview c=1.00 n=10 | structure | yes | CANDIDATE |
| 69 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6.offset-md-0.paddingL` | `—` | 12 | 12 | 0.01 of 2349 | — | 0.42 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 70 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.paddingR` | `div.col-12.col-md-12.paddingR` | 12 | 12 | 0.07 of 2349 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 71 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.offset-md-0` | `div.col-12.col-md-8` | 68 | 11 | 0.05 of 2349 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 72 | module-menu | EXTRA | `li>b` | `—` | `b` | 24 | 11 | 0.99 of 2349 | ptype=lesson c=1.00 n=10 | structure | — | CANDIDATE |
| 73 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `h5` | 18 | 11 | 0.04 of 2349 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 74 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.paddingL` | `div.col-12.col-md-6.paddingR` | 11 | 11 | 0.04 of 2349 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 75 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0` | `p` | `—` | 49 | 10 | 0.02 of 2349 | — | 0.72 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 76 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-8.paddingR` | `div.col-12.col-md-8` | 70 | 9 | 0.03 of 2349 | — | structure | yes | BELOW FLOOR |
| 77 | module-menu | MISSING | `div.col-12.col-md-8.paddingR` | `ul` | `—` | 48 | 9 | 0.02 of 2349 | — | 0.99 | yes | BELOW FLOOR |
| 78 | module-menu | MISSING | `div#module-menu-content.moduleMenu` | `h5` | `—` | 45 | 9 | 0.04 of 2349 | — | 0.71 | yes | BELOW FLOOR |
| 79 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `h5>span` | 9 | 9 | 0.97 of 2349 | — | structure | yes | BELOW FLOOR |
| 80 | module-menu | EXTRA | `div.col-12.col-md-6.paddingL` | `—` | `h5` | 9 | 9 | 1.00 of 2349 | — | structure | yes | BELOW FLOOR |
| 81 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `h5>span` | `—` | 9 | 9 | 0.03 of 2349 | — | 1.00 | yes | BELOW FLOOR |
| 82 | module-menu | SUBSTITUTED | `div.col-12.col-md-6` | `h4>span` | `h5>span` | 9 | 9 | 0.01 of 2349 | — | structure | yes | BELOW FLOOR |
| 83 | module-menu | MOVED | `ul` | `li` | `li` | 36 | 8 | 0.35 of 2349 | — | structure | — | BELOW FLOOR |
| 84 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `h4>span` | 11 | 8 | 0.04 of 2349 | — | structure | yes | BELOW FLOOR |
| 85 | module-menu | SUBSTITUTED | `div.row` | `WIDGET` | `div.col-12.col-md-8` | 9 | 8 | 0.12 of 2349 | — | structure | — | BELOW FLOOR |
| 86 | module-menu | EXTRA | `p>b` | `—` | `b` | 8 | 8 | 0.99 of 2349 | — | structure | — | BELOW FLOOR |
| 87 | module-menu | MISSING | `h5>span` | `span` | `—` | 8 | 8 | 0.03 of 2349 | — | 1.00 | — | BELOW FLOOR |
| 88 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0.paddingR` | `p` | `h5` | 8 | 8 | 0.01 of 2349 | — | structure | yes | BELOW FLOOR |
| 89 | module-menu | SUBSTITUTED | `div.row` | `div.col-12` | `div.col-12.col-md-8` | 51 | 7 | 0.02 of 2349 | — | structure | — | BELOW FLOOR |
| 90 | module-menu | SUBSTITUTED | `div.item` | `div.row` | `div.col-12.col-md-8` | 42 | 7 | 0.03 of 2349 | — | structure | yes | BELOW FLOOR |
| 91 | module-menu | MOVED | `div#module-menu-content.moduleMenu` | `h5` | `h5` | 35 | 7 | 0.04 of 2349 | — | structure | yes | BELOW FLOOR |
| 92 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `ul` | `p` | 15 | 7 | 0.05 of 2349 | — | structure | yes | BELOW FLOOR |
| 93 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.offset-md-0` | `div.col-12.col-md-12.paddingR` | 10 | 7 | 0.05 of 2349 | — | structure | yes | BELOW FLOOR |
| 94 | module-menu | EXTRA | `div.col-12.col-md-6.offset-md-0` | `—` | `ul` | 7 | 7 | 0.98 of 2349 | — | structure | yes | BELOW FLOOR |
| 95 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-12` | `div.col-12.col-md-12.paddingR` | 7 | 7 | 0.01 of 2349 | — | structure | yes | BELOW FLOOR |
| 96 | module-menu | SUBSTITUTED | `div#module-menu-content.moduleMenu` | `WIDGET` | `div.row` | 7 | 7 | 0.01 of 2349 | — | structure | yes | BELOW FLOOR |
| 97 | module-menu | MISSING | `div.col-12.col-md-8.paddingR` | `h5` | `—` | 30 | 6 | 0.02 of 2349 | — | 1.00 | yes | BELOW FLOOR |
| 98 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-12.paddingR` | `div.col-12.col-md-8` | 30 | 6 | 0.04 of 2349 | — | structure | yes | BELOW FLOOR |
| 99 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6` | `—` | 21 | 6 | 0.01 of 2349 | — | 1.00 | yes | BELOW FLOOR |
| 100 | module-menu | SUBSTITUTED | `div.col-12.col-md-8` | `p>b` | `h5` | 16 | 6 | 0.02 of 2349 | — | structure | — | BELOW FLOOR |
| 441 | footer | MISSING | `ul.footer-nav` | `li>a#next-lesson` | `—` | 97 | 60 | 0.73 of 2349 | subject+ptype=1-10 Mathematics/overview c=0.93 n=12 | structure | yes | CANDIDATE |
| 442 | footer | MISSING | `ul.footer-nav` | `li>a.home-nav` | `—` | 100 | 57 | 0.85 of 2349 | subject=1-10 English c=1.00 n=13 | structure | yes | CANDIDATE |
| 443 | footer | MISSING | `li>a#next-lesson` | `a#next-lesson` | `—` | 49 | 49 | 0.82 of 2349 | template=Bilingual c=0.86 n=10 | structure | yes | CANDIDATE |
| 444 | footer | MISSING | `ul.footer-nav.inquiry-nav` | `li>a.home-nav` | `—` | 38 | 33 | 0.12 of 2349 | subject+ptype=1-10 Blended Literacy/overview c=0.87 n=20 | structure | yes | CANDIDATE |
| 447 | footer | MISSING | `ul.footer-nav` | `li>a#prev-lesson` | `—` | 37 | 20 | 0.72 of 2349 | template+ptype=Standard/lesson c=0.89 n=14 | structure | yes | CANDIDATE |
| 448 | footer | EXTRA | `ul.footer-nav.inquiry-nav` | `—` | `li>a.home-nav` | 20 | 20 | 0.88 of 2349 | era=Refresh c=0.88 n=20 | structure | yes | CANDIDATE |
| 449 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav` | `ul.footer-nav.inquiry-nav` | 64 | 18 | 0.85 of 2349 | template+ptype=Standard/lesson c=0.90 n=12 | structure | yes | CANDIDATE |
| 450 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav` | `ul.footer-nav` | 18 | 17 | 0.85 of 2349 | template+ptype=Standard/lesson c=0.90 n=10 | structure | yes | CANDIDATE |
| 451 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` | `li>a#next-lesson` | `li>a.home-nav` | 16 | 16 | 0.09 of 2349 | subject+ptype=1-10 Blended Literacy/overview c=0.84 n=15 | structure | yes | CANDIDATE |
| 454 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav.inquiry-nav` | `li>a#next-lesson` | 15 | 15 | 0.12 of 2349 | subject+ptype=1-10 Blended Literacy/overview c=0.87 n=15 | structure | yes | CANDIDATE |
| 455 | footer | MISSING | `li>a.home-nav` | `a.home-nav` | `—` | 25 | 14 | 0.99 of 2349 | era=Refresh c=0.99 n=14 | structure | yes | CANDIDATE |
| 456 | footer | EXTRA | `div#footer` | `—` | `ul.footer-nav.inquiry-nav` | 15 | 13 | 0.88 of 2349 | template=Standard c=0.88 n=10 | structure | yes | CANDIDATE |
| 457 | footer | SUBSTITUTED | `ul.footer-nav` | `li>a#next-lesson` | `li>a#next-lesson` | 14 | 13 | 0.73 of 2349 | ptype=lesson c=0.77 n=11 | structure | yes | CANDIDATE |
| 460 | footer | SUBSTITUTED | `ul.footer-nav` | `li>a.home-nav` | `li>a.home-nav` | 13 | 11 | 0.85 of 2349 | era=Refresh c=0.85 n=11 | structure | yes | CANDIDATE |
| 461 | footer | EXTRA | `ul.footer-nav.fundamentals-nav` | `—` | `li>a.home-nav` | 11 | 11 | 0.98 of 2349 | era=Refresh c=0.98 n=11 | structure | yes | CANDIDATE |
| 462 | footer | MISSING | `div#footer` | `ul.footer-nav` | `—` | 10 | 10 | 0.85 of 2349 | era=Refresh c=0.85 n=10 | structure | yes | CANDIDATE |
| 549 | acks | SUBSTITUTED | `div.col-12.col-md-8` | `div.acks` | `div.acks.acksTemplate` | 89 | 89 | 0.15 of 2349 | template+ptype=Inquiry/overview c=0.82 n=29 | structure | yes | CANDIDATE |
| 579 | activity | MISSING | `div.col-12` | `p` | `—` | 728 | 348 | 0.29 of 2342 | template+ptype=Inquiry/overview c=0.73 n=24 | 0.81 | — | CANDIDATE |
| 580 | activity | EXTRA | `div.col-12` | `—` | `p` | 572 | 280 | 0.88 of 2342 | series=XDLS90 c=1.00 n=22 | structure | — | CANDIDATE |
| 583 | activity | MISSING | `div.col-12` | `a` | `—` | 431 | 218 | 0.29 of 2342 | series=HIS10 c=0.71 n=40 | 0.63 | — | CANDIDATE |
| 584 | activity | EXTRA | `div.col-12` | `—` | `WIDGET` | 323 | 195 | 0.82 of 2342 | subject=NCEA1 c=0.94 n=33 | structure | — | CANDIDATE |
| 585 | activity | MISSING | `div.col-12` | `h3` | `—` | 376 | 187 | 0.43 of 2342 | template+ptype=Fundamentals/overview c=0.88 n=30 | 0.69 | — | CANDIDATE |
| 587 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `div.activity[number=*]` | 248 | 168 | 0.42 of 2342 | template=Fundamentals c=0.73 n=20 | structure | yes | CANDIDATE |
| 589 | activity | MISSING | `div.activity.interactive[number=*]` | `div.row` | `—` | 270 | 156 | 0.12 of 2342 | template+ptype=Fundamentals/overview c=0.65 n=35 | 0.92 | yes | CANDIDATE |
| 590 | activity | EXTRA | `div.col-12` | `—` | `img.img-fluid` | 228 | 140 | 0.97 of 2342 | subject+ptype=1-10 English/lesson c=0.99 n=22 | structure | — | CANDIDATE |
| 591 | activity | MOVED | `div.col-12` | `p` | `p` | 152 | 121 | 0.15 of 2342 | template+ptype=Inquiry/overview c=0.71 n=20 | structure | — | CANDIDATE |
| 592 | activity | EXTRA | `div.row` | `—` | `div.col-12` | 160 | 115 | 0.90 of 2342 | series=XDLS90 c=0.97 n=20 | structure | — | CANDIDATE |
| 596 | activity | EXTRA | `div.activity[number=*]` | `—` | `div.row` | 144 | 101 | 0.94 of 2342 | subject=1-10 English c=0.98 n=23 | structure | yes | CANDIDATE |
| 597 | activity | EXTRA | `div.col-12` | `—` | `p>a` | 125 | 101 | 1.00 of 2342 | subject+ptype=1-10 Blended Literacy/lesson c=1.00 n=33 | structure | — | CANDIDATE |
| 602 | activity | EXTRA | `div.col-12` | `—` | `ol` | 133 | 85 | 0.96 of 2342 | subject=1-10 Mathematics c=0.98 n=31 | structure | — | CANDIDATE |
| 603 | activity | EXTRA | `div.col-12` | `—` | `p>b` | 125 | 84 | 0.95 of 2342 | subject=1-10 Blended Literacy c=0.97 n=22 | structure | — | CANDIDATE |
| 604 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `div.activity[number=*]` | 115 | 83 | 0.46 of 2342 | subject+ptype=1-10 Mathematics/lesson c=0.68 n=23 | structure | yes | CANDIDATE |
| 605 | activity | SUBSTITUTED | `div.col-12` | `p` | `p` | 108 | 83 | 0.75 of 2342 | template+ptype=Standard/lesson c=0.88 n=69 | structure | — | CANDIDATE |
| 606 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `div.activity.interactive[number=*]` | 114 | 82 | 0.46 of 2342 | subject+ptype=1-10 Blended Literacy/lesson c=0.86 n=23 | structure | yes | CANDIDATE |
| 610 | activity | EXTRA | `div.col-12` | `—` | `h3` | 104 | 79 | 0.87 of 2342 | template=Standard c=0.92 n=62 | structure | — | CANDIDATE |
| 611 | activity | EXTRA | `div.col-12` | `—` | `ul` | 103 | 77 | 0.94 of 2342 | template=Standard c=0.96 n=87 | structure | — | CANDIDATE |
| 612 | activity | EXTRA | `div.col-12` | `—` | `a` | 113 | 73 | 0.87 of 2342 | series=XDLS90 c=0.95 n=21 | structure | — | CANDIDATE |
| 613 | activity | EXTRA | `div.activity.interactive[number=*]` | `—` | `div.row` | 85 | 71 | 0.65 of 2342 | template=Standard c=0.68 n=69 | structure | yes | CANDIDATE |
| 614 | activity | EXTRA | `p>b` | `—` | `b` | 93 | 70 | 0.93 of 2342 | template=Standard c=0.94 n=60 | structure | — | CANDIDATE |
| 617 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `p` | 83 | 68 | 0.60 of 2342 | subject+ptype=1-10 Mathematics/lesson c=0.78 n=31 | structure | — | CANDIDATE |
| 618 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `div.activity.interactive[number=*]` | 94 | 67 | 0.42 of 2342 | subject+ptype=1-10 Mathematics/lesson c=0.65 n=21 | structure | yes | CANDIDATE |
| 619 | activity | EXTRA | `a` | `—` | `div.button` | 103 | 66 | 0.77 of 2342 | series=XDLS90 c=0.92 n=31 | structure | yes | CANDIDATE |
| 622 | activity | EXTRA | `p>a` | `—` | `a` | 78 | 66 | 0.98 of 2342 | subject+ptype=1-10 Blended Literacy/lesson c=1.00 n=28 | structure | — | CANDIDATE |
| 625 | activity | SUBSTITUTED | `div.col-12` | `p` | `WIDGET` | 70 | 59 | 0.75 of 2342 | template+ptype=Standard/lesson c=0.88 n=49 | structure | — | CANDIDATE |
| 628 | activity | EXTRA | `div.col-12` | `—` | `h4.goJournal` | 130 | 56 | 0.95 of 2342 | series=HIS10 c=1.00 n=32 | structure | — | CANDIDATE |
| 630 | activity | EXTRA | `div.col-12.col-md-8` | `—` | `div.activity[number=*]` | 65 | 55 | 0.95 of 2342 | template=Standard c=0.98 n=52 | structure | yes | CANDIDATE |
| 631 | activity | SUBSTITUTED | `div.col-12` | `a` | `h4.goJournal` | 117 | 54 | 0.56 of 2342 | series=HIS10 c=0.83 n=20 | structure | — | CANDIDATE |
| 633 | activity | EXTRA | `ol` | `—` | `li` | 69 | 53 | 0.96 of 2342 | template=Standard c=0.96 n=53 | structure | — | CANDIDATE |
| 635 | activity | SUBSTITUTED | `div.col-12` | `a` | `p` | 72 | 50 | 0.56 of 2342 | subject+ptype=1-10 Mathematics/lesson c=0.80 n=20 | structure | — | CANDIDATE |
| 637 | activity | EXTRA | `div.col-12` | `—` | `p>i` | 55 | 49 | 0.98 of 2342 | template=Standard c=0.98 n=46 | structure | — | CANDIDATE |
| 643 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `div.row` | 45 | 43 | 0.60 of 2342 | ptype=lesson c=0.69 n=35 | structure | — | CANDIDATE |
| 648 | activity | EXTRA | `p>i` | `—` | `i` | 48 | 40 | 0.89 of 2342 | template=Standard c=0.90 n=44 | structure | — | CANDIDATE |
| 653 | activity | EXTRA | `a` | `—` | `div.externalButton` | 48 | 37 | 0.91 of 2342 | template=Standard c=0.91 n=35 | structure | — | CANDIDATE |
| 659 | activity | EXTRA | `div.col-12` | `—` | `div.icon.ratio.ratio-16x9.videoSection` | 50 | 35 | 0.98 of 2342 | template=Standard c=0.98 n=42 | structure | yes | CANDIDATE |
| 660 | activity | SUBSTITUTED | `div.col-12` | `a` | `WIDGET` | 41 | 35 | 0.56 of 2342 | template+ptype=Standard/lesson c=0.66 n=37 | structure | — | CANDIDATE |
| 669 | activity | EXTRA | `div.col-12.col-md-8` | `—` | `div.activity.interactive[number=*]` | 34 | 32 | 0.89 of 2342 | template=Standard c=0.92 n=26 | structure | yes | CANDIDATE |
| 671 | activity | EXTRA | `p` | `—` | `b` | 39 | 31 | 0.96 of 2342 | template=Standard c=0.97 n=35 | structure | — | CANDIDATE |
| 674 | activity | EXTRA | `div.col-12` | `—` | `audio.audioPlayer.icon` | 46 | 30 | 1.00 of 2342 | subject=1-10 Blended Literacy c=1.00 n=22 | structure | yes | CANDIDATE |
| 675 | activity | SUBSTITUTED | `div.col-12` | `h3` | `WIDGET` | 38 | 30 | 0.76 of 2342 | template+ptype=Standard/lesson c=0.89 n=27 | structure | — | CANDIDATE |
| 678 | activity | EXTRA | `ul` | `—` | `li` | 30 | 29 | 0.93 of 2342 | template=Standard c=0.95 n=25 | structure | — | CANDIDATE |
| 680 | activity | EXTRA | `div.col-12` | `—` | `div.ratio.ratio-16x9.videoSection` | 49 | 27 | 0.99 of 2342 | template=Standard c=0.99 n=40 | structure | yes | CANDIDATE |
| 682 | activity | SUBSTITUTED | `div.row` | `div.col-12` | `div.col-12.col-md-8` | 30 | 27 | 0.79 of 2342 | template+ptype=Standard/lesson c=0.92 n=20 | structure | — | CANDIDATE |
| 686 | activity | EXTRA | `div.col-12` | `—` | `h5` | 29 | 25 | 0.99 of 2342 | template=Standard c=0.99 n=24 | structure | — | CANDIDATE |
| 687 | activity | SUBSTITUTED | `div.row` | `div.col-12` | `WIDGET` | 26 | 25 | 0.79 of 2342 | ptype=lesson c=0.92 n=20 | structure | — | CANDIDATE |
| 693 | activity | EXTRA | `div.icon.ratio.ratio-16x9.videoSection` | `—` | `iframe` | 28 | 24 | 0.99 of 2342 | template=Standard c=0.99 n=21 | structure | yes | CANDIDATE |
| 694 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `ol` | 26 | 24 | 0.60 of 2342 | ptype=lesson c=0.69 n=22 | structure | — | CANDIDATE |
| 697 | activity | SUBSTITUTED | `div.activity.interactive[number=*]` | `div.row` | `WIDGET` | 26 | 23 | 0.55 of 2342 | ptype=lesson c=0.63 n=22 | structure | yes | CANDIDATE |
| 704 | activity | SUBSTITUTED | `div.row` | `div.col-12` | `div.row` | 23 | 22 | 0.79 of 2342 | era=Refresh c=0.79 n=23 | structure | — | CANDIDATE |
| 716 | activity | SUBSTITUTED | `div.col-12` | `p` | `p>b` | 25 | 19 | 0.75 of 2342 | ptype=lesson c=0.88 n=21 | structure | — | CANDIDATE |
| 720 | activity | EXTRA | `div.col-12` | `—` | `div.button` | 29 | 18 | 1.00 of 2342 | template=Standard c=1.00 n=25 | structure | yes | CANDIDATE |
| 721 | activity | SUBSTITUTED | `div.col-12` | `h3` | `h3` | 26 | 18 | 0.76 of 2342 | template+ptype=Standard/lesson c=0.89 n=20 | structure | — | CANDIDATE |
| 729 | activity | SUBSTITUTED | `div.row` | `div.col-12` | `div.button` | 20 | 18 | 0.79 of 2342 | era=Refresh c=0.79 n=20 | structure | yes | CANDIDATE |
| 732 | activity | EXTRA | `div.ratio.ratio-16x9.videoSection` | `—` | `iframe` | 25 | 17 | 0.99 of 2342 | ptype=lesson c=0.99 n=24 | structure | yes | CANDIDATE |
| 768 | activity | SUBSTITUTED | `div.col-12` | `p` | `h4.goJournal` | 22 | 13 | 0.75 of 2342 | template+ptype=Standard/lesson c=0.88 n=21 | structure | — | CANDIDATE |
| 3682 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 1055 | 386 | 0.82 of 2342 | subject+ptype=NCEA1/overview c=1.00 n=29 | structure | — | CANDIDATE |
| 3683 | body | EXTRA | `div#body` | `—` | `div.row` | 1397 | 374 | 0.73 of 2342 | subject+ptype=1-10 Blended Literacy/overview c=1.00 n=29 | structure | — | CANDIDATE |
| 3684 | body | MISSING | `div#body` | `div.row` | `—` | 1292 | 322 | 0.34 of 2342 | series=CEDO50 c=0.76 n=20 | 0.86 | — | CANDIDATE |
| 3685 | body | MISSING | `div.col-12.col-md-8` | `p` | `—` | 590 | 274 | 0.25 of 2342 | template+ptype=Fundamentals/overview c=0.91 n=45 | 0.81 | — | CANDIDATE |
| 3686 | body | EXTRA | `div.col-12.col-md-8` | `—` | `img.img-fluid` | 538 | 242 | 0.96 of 2342 | template+ptype=Standard/overview c=1.00 n=25 | structure | — | CANDIDATE |
| 3687 | body | EXTRA | `div.col-12.col-md-8` | `—` | `WIDGET` | 358 | 224 | 0.93 of 2342 | subject+ptype=NCEA1/lesson c=0.99 n=51 | structure | — | CANDIDATE |
| 3688 | body | MOVED | `div.col-12.col-md-8` | `p` | `p` | 321 | 204 | 0.18 of 2342 | template+ptype=Fundamentals/overview c=0.84 n=40 | structure | — | CANDIDATE |
| 3689 | body | EXTRA | `div.row` | `—` | `div.col-12.col-md-8` | 285 | 195 | 0.85 of 2342 | subject+ptype=1-10 Blended Literacy/lesson c=0.96 n=23 | structure | — | CANDIDATE |
| 3690 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p>b` | 317 | 192 | 0.97 of 2342 | subject=1-10 Blended Literacy c=1.00 n=41 | structure | — | CANDIDATE |
| 3691 | body | SUBSTITUTED | `div.row` | `div.col-12` | `div.col-12.col-md-8` | 315 | 180 | 0.55 of 2342 | subject+ptype=1-10 Blended Literacy/overview c=0.96 n=64 | structure | — | CANDIDATE |
| 3692 | body | EXTRA | `div.col-12.col-md-8` | `—` | `h3` | 290 | 179 | 0.82 of 2342 | template+ptype=Standard/overview c=0.98 n=33 | structure | — | CANDIDATE |
| 3693 | body | EXTRA | `div.col-12.col-md-8` | `—` | `ul` | 295 | 172 | 0.95 of 2342 | subject=1-10 Mathematics c=0.98 n=21 | structure | — | CANDIDATE |
| 3694 | body | MISSING | `div.col-12.col-md-8` | `WIDGET` | `—` | 260 | 169 | 0.19 of 2342 | template+ptype=Fundamentals/overview c=0.65 n=31 | structure | — | CANDIDATE |
| 3695 | body | MISSING | `div.row` | `div.col-12.col-md-8` | `—` | 307 | 165 | 0.29 of 2342 | template+ptype=Fundamentals/overview c=0.94 n=20 | 0.95 | — | CANDIDATE |
| 3698 | body | MISSING | `div.col-12.col-md-8` | `h3` | `—` | 223 | 145 | 0.18 of 2342 | template+ptype=Fundamentals/overview c=0.75 n=21 | 0.89 | — | CANDIDATE |
| 3699 | body | EXTRA | `div.col-12.col-md-8` | `—` | `a` | 221 | 144 | 0.98 of 2342 | subject=ConnectED c=1.00 n=28 | structure | — | CANDIDATE |
| 3702 | body | EXTRA | `p>b` | `—` | `b` | 182 | 114 | 0.94 of 2342 | subject=1-10 Mathematics c=0.97 n=33 | structure | — | CANDIDATE |
| 3703 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.table-responsive` | 162 | 111 | 0.98 of 2342 | subject+ptype=1-10 English/lesson c=0.99 n=21 | structure | — | CANDIDATE |
| 3707 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.ratio.ratio-16x9.videoSection` | 169 | 109 | 0.94 of 2342 | subject=NCEA1 c=0.98 n=23 | structure | yes | CANDIDATE |
| 3709 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p>a` | 162 | 108 | 0.99 of 2342 | subject=1-10 English c=1.00 n=20 | structure | — | CANDIDATE |
| 3710 | body | EXTRA | `a` | `—` | `div.button` | 171 | 103 | 0.96 of 2342 | subject=NCEA1 c=0.98 n=36 | structure | — | CANDIDATE |
| 3715 | body | EXTRA | `p` | `—` | `b` | 117 | 91 | 0.93 of 2342 | subject=NCEA1 c=0.96 n=29 | structure | — | CANDIDATE |
| 3716 | body | EXTRA | `div.table-responsive` | `—` | `table.table.table-bordered` | 136 | 89 | 0.96 of 2342 | subject=NCEA1 c=0.97 n=28 | structure | yes | CANDIDATE |
| 3719 | body | SUBSTITUTED | `div.icon.ratio.ratio-16x9.videoSection` | `iframe.embed-responsive-item` | `iframe` | 211 | 81 | 0.20 of 2342 | series=PES10 c=0.68 n=35 | structure | yes | CANDIDATE |
| 3720 | body | EXTRA | `p>i` | `—` | `i` | 107 | 80 | 0.97 of 2342 | subject+ptype=1-10 Blended Literacy/overview c=1.00 n=26 | structure | — | CANDIDATE |
| 3724 | body | EXTRA | `div.col-12.col-md-8` | `—` | `ol` | 105 | 78 | 0.99 of 2342 | template=Standard c=0.99 n=86 | structure | — | CANDIDATE |
| 3725 | body | EXTRA | `p>a` | `—` | `a` | 99 | 73 | 0.99 of 2342 | template=Standard c=1.00 n=78 | structure | — | CANDIDATE |
| 3726 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p>i` | 99 | 71 | 0.98 of 2342 | subject=NCEA1 c=0.99 n=26 | structure | — | CANDIDATE |
| 3729 | body | EXTRA | `div.row` | `—` | `div.col-12` | 125 | 70 | 0.71 of 2342 | subject=ANZH c=0.74 n=21 | structure | — | CANDIDATE |
| 3731 | body | EXTRA | `div.col-12.col-md-8` | `—` | `audio.audioPlayer.icon` | 124 | 69 | 1.00 of 2342 | subject=Leaving to Learn c=1.00 n=34 | structure | yes | CANDIDATE |
| 3735 | body | SUBSTITUTED | `div#body` | `div.row` | `WIDGET` | 112 | 67 | 0.94 of 2342 | subject=Online Safety (OS9000) c=1.00 n=25 | structure | — | CANDIDATE |
| 3738 | body | EXTRA | `div.fundamentalsPanel` | `—` | `div.row` | 67 | 67 | 0.98 of 2342 | era=Refresh c=0.98 n=67 | structure | — | CANDIDATE |
| 3740 | body | MOVED | `div.col-12.col-md-8` | `h3` | `h3` | 80 | 66 | 0.11 of 2342 | template+ptype=Fundamentals/overview c=0.67 n=23 | structure | — | CANDIDATE |
| 3741 | body | EXTRA | `table.table.table-bordered` | `—` | `tr` | 91 | 65 | 0.98 of 2342 | template=Standard c=0.98 n=78 | structure | yes | CANDIDATE |
| 3748 | body | EXTRA | `a` | `—` | `div.externalButton` | 86 | 60 | 0.92 of 2342 | template=Standard c=0.92 n=74 | structure | — | CANDIDATE |
| 3751 | body | EXTRA | `ul` | `—` | `li` | 72 | 59 | 0.94 of 2342 | template=Standard c=0.95 n=55 | structure | — | CANDIDATE |
| 3752 | body | EXTRA | `div.col-12.col-md-8` | `—` | `h4` | 67 | 59 | 0.97 of 2342 | template=Standard c=0.98 n=32 | structure | — | CANDIDATE |
| 3753 | body | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `div.col-12.col-md-8` | 67 | 58 | 0.98 of 2342 | ptype=lesson c=0.99 n=38 | structure | — | CANDIDATE |
| 3756 | body | EXTRA | `div.ratio.ratio-16x9.videoSection` | `—` | `iframe` | 74 | 56 | 0.92 of 2342 | template=Standard c=0.93 n=53 | structure | yes | CANDIDATE |
| 3758 | body | EXTRA | `div.col-12` | `—` | `p` | 87 | 51 | 0.93 of 2342 | template=Standard c=0.94 n=75 | structure | — | CANDIDATE |
| 3759 | body | EXTRA | `div.alert` | `—` | `div.row` | 65 | 51 | 0.91 of 2342 | template=Standard c=0.92 n=46 | structure | — | CANDIDATE |
| 3760 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `p` | 65 | 51 | 0.85 of 2342 | template+ptype=Standard/lesson c=0.86 n=46 | structure | — | CANDIDATE |
| 3761 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `div.activity[number=*]` | 57 | 50 | 0.85 of 2342 | template+ptype=Standard/lesson c=0.86 n=49 | structure | yes | CANDIDATE |
| 3764 | body | EXTRA | `tr` | `—` | `td` | 55 | 47 | 0.94 of 2342 | template=Standard c=0.95 n=51 | structure | — | CANDIDATE |
| 3767 | body | EXTRA | `div.row` | `—` | `div.col-12.col-md-6` | 65 | 45 | 0.99 of 2342 | subject=Online Safety (OS9000) c=1.00 n=21 | structure | — | CANDIDATE |
| 3769 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.alert` | 60 | 45 | 0.91 of 2342 | template=Standard c=0.92 n=46 | structure | — | CANDIDATE |
| 3771 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.icon.ratio.ratio-16x9.videoSection` | 62 | 44 | 0.92 of 2342 | template=Standard c=0.93 n=54 | structure | yes | CANDIDATE |
| 3778 | body | EXTRA | `div#body` | `—` | `WIDGET` | 77 | 41 | 0.93 of 2342 | era=Refresh c=0.93 n=77 | structure | — | CANDIDATE |
| 3781 | body | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `WIDGET` | 44 | 41 | 0.98 of 2342 | ptype=lesson c=0.99 n=37 | structure | — | CANDIDATE |
| 3782 | body | MISSING | `div#body` | `div.fundamentalsPanel` | `—` | 48 | 40 | 0.02 of 2342 | template+ptype=Fundamentals/overview c=0.60 n=39 | 0.98 | yes | CANDIDATE |
| 3784 | body | EXTRA | `p` | `—` | `i` | 44 | 38 | 0.96 of 2342 | template=Standard c=0.97 n=40 | structure | — | CANDIDATE |
| 3785 | body | EXTRA | `tr` | `—` | `th` | 41 | 38 | 0.99 of 2342 | template=Standard c=1.00 n=34 | structure | — | CANDIDATE |
| 3793 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `WIDGET` | 36 | 35 | 0.85 of 2342 | template+ptype=Standard/lesson c=0.86 n=23 | structure | — | CANDIDATE |
| 3795 | body | EXTRA | `div#body` | `—` | `div.row.supervisor` | 43 | 33 | 0.90 of 2342 | ptype=lesson c=0.91 n=38 | structure | yes | CANDIDATE |
| 3796 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p>span.infoTrigger` | 37 | 33 | 0.86 of 2342 | template=Standard c=0.87 n=31 | structure | — | CANDIDATE |
| 3798 | body | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `div.row` | 34 | 33 | 0.98 of 2342 | era=Refresh c=0.98 n=34 | structure | — | CANDIDATE |
| 3799 | body | EXTRA | `div.row` | `—` | `div.col-12.col-md-4.offset-md-0` | 33 | 33 | 0.80 of 2342 | template=Standard c=0.80 n=21 | structure | — | CANDIDATE |
| 3805 | body | EXTRA | `div.col-12.col-md-8` | `—` | `h4.goJournal` | 40 | 31 | 1.00 of 2342 | era=Refresh c=1.00 n=40 | structure | — | CANDIDATE |
| 3806 | body | EXTRA | `div.col-12.col-md-8` | `—` | `h5` | 40 | 31 | 0.98 of 2342 | subject=NCEA1 c=0.99 n=21 | structure | — | CANDIDATE |
| 3807 | body | EXTRA | `div.alert.solid` | `—` | `div.row` | 42 | 30 | 0.99 of 2342 | template=Standard c=0.99 n=37 | structure | yes | CANDIDATE |
| 3808 | body | EXTRA | `div.icon.ratio.ratio-16x9.videoSection` | `—` | `iframe` | 37 | 30 | 0.97 of 2342 | ptype=lesson c=0.98 n=31 | structure | yes | CANDIDATE |
| 3816 | body | EXTRA | `div#body` | `—` | `div.fundamentalsPanel` | 29 | 29 | 0.98 of 2342 | era=Refresh c=0.98 n=29 | structure | yes | CANDIDATE |
| 3818 | body | EXTRA | `div.inquiryPanel` | `—` | `div.row` | 31 | 28 | 0.99 of 2342 | era=Refresh c=0.99 n=31 | structure | — | CANDIDATE |
| 3819 | body | EXTRA | `div.introduction` | `—` | `div.row` | 28 | 28 | 0.99 of 2342 | era=Refresh c=0.99 n=28 | structure | — | CANDIDATE |
| 3822 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.flipCardsContainer.row` | 30 | 27 | 0.94 of 2342 | template=Standard c=0.95 n=24 | structure | — | CANDIDATE |
| 3831 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `img.img-fluid` | 26 | 25 | 0.85 of 2342 | era=Refresh c=0.85 n=26 | structure | — | CANDIDATE |
| 3837 | body | EXTRA | `div.row` | `—` | `div.col-12.col-md-4` | 31 | 24 | 0.95 of 2342 | template=Standard c=0.95 n=25 | structure | — | CANDIDATE |
| 3841 | body | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `div.col-12.col-md-6` | 27 | 24 | 0.98 of 2342 | ptype=lesson c=0.99 n=23 | structure | — | CANDIDATE |
| 3845 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.alert.solid` | 29 | 23 | 0.99 of 2342 | era=Refresh c=0.99 n=29 | structure | yes | CANDIDATE |
| 3849 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.clickDropContent` | 26 | 22 | 0.95 of 2342 | template=Standard c=0.95 n=23 | structure | — | CANDIDATE |
| 3852 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `div.activity.interactive[number=*]` | 24 | 22 | 0.85 of 2342 | template+ptype=Standard/lesson c=0.86 n=22 | structure | yes | CANDIDATE |
| 3853 | body | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `p` | 23 | 22 | 0.98 of 2342 | era=Refresh c=0.98 n=23 | structure | — | CANDIDATE |
| 3854 | body | EXTRA | `div#body` | `—` | `div.inquiryPanel` | 29 | 21 | 0.98 of 2342 | era=Refresh c=0.98 n=29 | structure | — | CANDIDATE |
| 3858 | body | EXTRA | `p>span.infoTrigger` | `—` | `span.infoTrigger` | 21 | 21 | 0.84 of 2342 | era=Refresh c=0.84 n=21 | structure | — | CANDIDATE |
| 3860 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `div.alert` | 28 | 20 | 0.85 of 2342 | era=Refresh c=0.85 n=28 | structure | — | CANDIDATE |
| 3878 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `h3` | 20 | 19 | 0.85 of 2342 | era=Refresh c=0.85 n=20 | structure | — | CANDIDATE |
| 3890 | body | SUBSTITUTED | `div#body` | `div.row` | `div.table-responsive` | 23 | 17 | 0.94 of 2342 | ptype=lesson c=0.98 n=21 | structure | — | CANDIDATE |
| 3913 | body | MISSING | `div#body` | `div.clickDropContent.noBorder.row` | `—` | 50 | 15 | 0.02 of 2342 | series=XDLS90 c=0.64 n=38 | 0.93 | yes | CANDIDATE |
| 3915 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p.captionText` | 21 | 15 | 1.00 of 2342 | era=Refresh c=1.00 n=21 | structure | — | CANDIDATE |
| 3922 | body | EXTRA | `div.col-12.col-md-6` | `—` | `p` | 23 | 14 | 1.00 of 2342 | ptype=lesson c=1.00 n=21 | structure | — | CANDIDATE |
| 4374 | body | SUBSTITUTED | `div.col-12.col-md-8` | `div.alert` | `div.activity.clickDropContent.dropbox[number=*]` | 20 | 4 | 0.31 of 2342 | series=XDLS90 c=0.80 n=20 | structure | yes | CANDIDATE |
| 8775 | root | EXTRA | `body.container-fluid` | `—` | `div.row` | 261 | 261 | 0.88 of 2349 | subject+ptype=1-10 Mathematics/overview c=0.97 n=33 | structure | — | CANDIDATE |
| 8779 | root | SUBSTITUTED | `#root` | `body` | `body.container-fluid` | 138 | 15 | 0.06 of 2349 | series=PWY10 c=1.00 n=44 | structure | yes | CANDIDATE |

## Details — in the companion file `CONVERTER_V2/outputs/_diff_queue_details.md`
Every CANDIDATE and every top-40 row has three quoted examples (WT / gold / Claude) there, plus the
below-floor list. **NEVER read the companion whole** (hundreds of KB): `grep -n '^### #<rank> ' CONVERTER_V2/outputs/_diff_queue_details.md` then `sed -n '<start>,<start+40>p'`. The top 25
candidates' detail blocks are repeated below for convenience.

### #4 · title · MISSING · `div#header` › gold `h1>span` vs Claude `—` — CANDIDATE
- pages 246 / modules 127 / lines 249; consensus (all) 0.23 of 2349 gold pages with the region; derivable 0.76 (61 lines with no WT source)
- by template: Standard 84m/186p c=0.18; Fundamentals 27m/27p c=0.48; Inquiry 11m/14p c=0.35; Bilingual 5m/19p c=1.00
- by subject: NCEA1 22m/44p c=0.17; 1-10 English 21m/32p c=0.18; Leaving to Learn 14m/22p c=0.26; Online Safety (OS9000) 13m/29p c=0.33; 1-10 Mathematics 11m/11p c=0.14; ANZH 6m/31p c=0.49
- by era: Refresh 127m/246p c=0.23
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:94 — **Header:** `#module-code` → `<h1>` (module code or lesson number), then `<h1><span>Title</span></h1>`, then `#module-head-buttons` → `#module-menu-bu
  - KB: 00_MASTER_INSTRUCTIONS/00B_CONVERSION_PIPELINE.md:204 — - Lesson pages: use THAT LESSON'S OWN title in the header <h1><span> (never the module title) and the zero-padded lesson number (not the module code) 
  - KB: 00_MASTER_INSTRUCTIONS/00D_CONSTRAINTS_1.md:24 — 16. Lesson pages: zero-padded lesson number (e.g., `01`, `02`) in `#module-code`; **that lesson's own title** in `<h1><span>` — NOT the module title, 
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html (content, derivable=False)
  - gold: `h1  «Ko ngā Ingoa Waahi ngā Kōrero ake»`
  - Claude: `—`
- **ANZH103** ANZH103_0_0.html ↔ ANZH103_0_0.html (content, derivable=False)
  - gold: `h1  «6 o Whiringa-ā-rangi – He Rā Whakahirahira»`
  - Claude: `—`
- **ANZH104** ANZH104_4_0.html ↔ ANZH104_04.0.html (content, derivable=True)
  - gold: `h1  «Hunting for Food in the Water»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [H2]  [/RED TEXT]🔴Lesson 4 – Hunting for Food in the Water`
- modules: ANZH101, ANZH103, ANZH104, ANZH301, ANZH401, ANZH404, ARFUN01, ARFUN02, ARFUN03, ARFUN04, ARFUN05, ART1004, ART1006, CEDK102, CEDK501, CEDO202, CEDR204, CEDT301, CHI1005, CHWHA, DTC1005, ENFUN01, ENFUN02, ENFUN03 …

### #5 · title · EXTRA · `div#header` › gold `—` vs Claude `h1>span` — CANDIDATE
- pages 17 / modules 16 / lines 17; consensus (all) 0.77 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 11m/12p c=0.82; Fundamentals 4m/4p c=0.52; Inquiry 1m/1p c=0.65
- by subject: NCEA1 5m/5p c=0.83; Leaving to Learn 3m/3p c=0.74; 1-10 Writing (MiW) 2m/2p c=0.38; ANZH 1m/2p c=0.51; 1-10 Blended Literacy 1m/1p c=0.99; ConnectED 1m/1p c=0.77
- by era: Refresh 16m/17p c=0.77
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:94 — **Header:** `#module-code` → `<h1>` (module code or lesson number), then `<h1><span>Title</span></h1>`, then `#module-head-buttons` → `#module-menu-bu
  - KB: 00_MASTER_INSTRUCTIONS/00B_CONVERSION_PIPELINE.md:204 — - Lesson pages: use THAT LESSON'S OWN title in the header <h1><span> (never the module title) and the zero-padded lesson number (not the module code) 
  - KB: 00_MASTER_INSTRUCTIONS/00D_CONSTRAINTS_1.md:24 — 16. Lesson pages: zero-padded lesson number (e.g., `01`, `02`) in `#module-code`; **that lesson's own title** in `<h1><span>` — NOT the module title, 
- **AGH1005** AGH1005_0_0.html ↔ AGH1005.00.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h1  «Unlocking Plant Magic: Exploring plant growth and processes in Aotearoa, New Zealand.»`
- **ANZH302** ANZH302_0_0.html ↔ ANZH302_0_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h1  «Big City Lights»`
- **BLL246** BLL246_0_0.html ↔ BLL246_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h1  «Module»`
- modules: AGH1005, ANZH302, BLL246, CEDO105, ENGFUN02, ENGI103, FRFUN06, HIS1002, PWY1002, PWYWHA1, SSFUN07, WJFUN105, WJFUN116, XDLS904, XDLS906, XFUN02

### #31 · module-menu · SUBSTITUTED · `div.col-12.col-md-6.paddingR` › gold `p` vs Claude `h5` — CANDIDATE
- pages 83 / modules 83 / lines 150; consensus (all) 0.06 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 61m/61p c=0.05; Fundamentals 14m/14p c=0.12; Inquiry 8m/8p c=0.35
- by subject: 1-10 Blended Literacy 69m/69p c=0.28; 1-10 Health and PE 14m/14p c=0.61
- by era: Refresh 83m/83p c=0.06
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:158 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **BLL111** BLL111_0_0.html ↔ BLL111-01.html (structure, derivable=True)
  - gold: `p  «We are learning:»`
  - Claude: `h5  «Ākonga will:»`
- **BLL112** BLL112_0_0.html ↔ BLL112-01.html (structure, derivable=True)
  - gold: `p  «We are learning:»`
  - Claude: `h5  «Ākonga will:»`
- **BLL113** BLL113_0_0.html ↔ BLL113-01.html (structure, derivable=True)
  - gold: `p  «We are learning:»`
  - Claude: `h5  «Ākonga will:»`
- modules: BLL111, BLL112, BLL113, BLL114, BLL115, BLL116, BLL117, BLL121, BLL122, BLL123, BLL125, BLL126, BLL127, BLL130, BLL131, BLL132, BLL133, BLL134, BLL135, BLL136, BLL137, BLL140, BLL141, BLL142 …

### #32 · module-menu · MISSING · `ul` › gold `li` vs Claude `—` — CANDIDATE
- pages 127 / modules 77 / lines 357; consensus (all) 0.10 of 2349 gold pages with the region; derivable 0.84 (57 lines with no WT source)
- by template: Standard 58m/108p c=0.10; Inquiry 11m/11p c=0.26; Fundamentals 8m/8p c=0.01
- by subject: 1-10 English 22m/39p c=0.11; 1-10 Blended Literacy 21m/21p c=0.22; NCEA1 9m/15p c=0.01; 1-10 Mathematics 8m/23p c=0.09; Te ara Whakapuawa -Wellbeing 5m/5p c=0.88; ANZH 3m/15p c=0.45
- by era: Refresh 77m/127p c=0.10
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1003** AGH1003_3_0.html ↔ AGH1003_03.0.html (content, derivable=True)
  - gold: `li  «I can justify the use of key management practices due to the positive impact that they have on soil properties and plant»`
  - Claude: `—`
  - WT: `• *Explain how soil management practices impact plant growing processes and plant growth.*`
- **AGH1007** AGH1007_7_0.html ↔ AGH1007.01.html (content, derivable=False)
  - gold: `li  «to identify the connection between animals and their taiao (environment).»`
  - Claude: `—`
- **AGH1008** AGH1008_3_0.html ↔ AGH1008.03.html (content, derivable=True)
  - gold: `li  «digestion, and immunity/health.»`
  - Claude: `—`
  - WT: `• *I can explain how management practices carried out by farmers/growers impact the life processes of reproduction, digestion, and immunity/health.*`
- modules: AGH1003, AGH1007, AGH1008, ANZH101, ANZH103, ANZH302, BLL110, BLL125, BLL126, BLL127, BLL130, BLL134, BLL136, BLL137, BLL140, BLL141, BLL143, BLL146, BLL147, BLL150, BLL151, BLL153, BLL154, BLL173 …

### #33 · module-menu · MISSING · `div.col-12.col-md-8` › gold `ul` vs Claude `—` — CANDIDATE
- pages 202 / modules 53 / lines 369; consensus (all) 0.29 of 2349 gold pages with the region; derivable 0.92 (31 lines with no WT source)
- by template: Standard 48m/185p c=0.32; Inquiry 4m/16p c=0.26; Fundamentals 1m/1p c=0.01
- by subject: NCEA1 13m/50p c=0.21; 1-10 English 11m/36p c=0.61; Leaving to Learn 11m/32p c=0.47; 1-10 Blended Literacy 4m/11p c=0.09; ConnectED 4m/17p c=0.44; 1-10 Languages 4m/12p c=0.40
- by era: Refresh 53m/202p c=0.29
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1009** AGH1009_7_0.html ↔ AGH1009.07.html (content, derivable=True)
  - gold: `ul  «identify and describe ways farmers have adopted sustainable practices to the impact of agricultural and horticultural pr»`
  - Claude: `—`
  - WT: `• *Explain how* ***Māori values of kaitiakitanga and manaakitanga*** *are integral to* ***sustainable practices*** *within agricultural and horticultural production within Aotearoa.*`
- **BLL240** BLL240_1_2.html ↔ BLL240-2.0.html (content, derivable=True)
  - gold: `ul  «the sounds and how to read, spell and write words that use the letter patterns wh, tch, dge, air, ear, ere and eer.»`
  - Claude: `—`
  - WT: `• *the sounds and how to read, spell and write words that use the letter patterns wh, tch,* *dge**, air, ear, ere and eer.*`
- **BLLR201** BLLR201_2_0.html ↔ BLLR201_1_1.html (content, derivable=True)
  - gold: `ul  «to use strategies to find a good book to read»`
  - Claude: `—`
  - WT: `• *to use strategies to find a good book to read*`
- modules: AGH1009, BLL240, BLLR201, BLLR202, BLLR203, CBI1008, CEDK501, CEDR501, CEDT501, CEDW501, CHI1003, CHI1004, CHI1005, ENGC102, ENGC201, ENGC403, ENGI301, ENGI405, ENGJ302, ENGR102, ENGR202, ENGS101, ENGS302, ENGS404 …

### #34 · module-menu · MISSING · `div.col-12.col-md-8` › gold `h5` vs Claude `—` — CANDIDATE
- pages 200 / modules 45 / lines 359; consensus (all) 0.24 of 2349 gold pages with the region; derivable 0.83 (61 lines with no WT source)
- by template: Standard 40m/185p c=0.27; Inquiry 4m/14p c=0.19; Fundamentals 1m/1p c=0.01
- by subject: NCEA1 13m/59p c=0.23; 1-10 English 12m/57p c=0.55; ConnectED 4m/17p c=0.44; 1-10 Languages 4m/12p c=0.40; Leaving to Learn 4m/9p c=0.14; 1-10 Blended Literacy 3m/10p c=0.07
- by era: Refresh 45m/200p c=0.24
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1004** AGH1004_2_0.html ↔ AGH1004.06.html (content, derivable=True)
  - gold: `h5  «We are learning to:»`
  - Claude: `—`
  - WT: `We are learning to ...`
- **BLL240** BLL240_1_2.html ↔ BLL240-2.0.html (content, derivable=True)
  - gold: `h5  «We are learning:»`
  - Claude: `—`
  - WT: `*We are learning:*`
- **BLLR201** BLLR201_2_0.html ↔ BLLR201_1_1.html (content, derivable=True)
  - gold: `h5  «We are learning:»`
  - Claude: `—`
  - WT: `*We are learning:*`
- modules: AGH1004, BLL240, BLLR201, BLLR202, CBI1008, CEDK501, CEDR501, CEDT501, CEDW501, COM1002, COM1005, COM1006, ENGC102, ENGC201, ENGC202, ENGC403, ENGJ302, ENGJ402, ENGJ403, ENGR102, ENGR202, ENGS101, ENGS302, ENGS404 …

### #36 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `div.col-12.col-md-6.paddingR` — CANDIDATE
- pages 64 / modules 44 / lines 101; consensus (all) 0.97 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 37m/57p c=0.97; Inquiry 4m/4p c=0.90; Fundamentals 3m/3p c=1.00
- by subject: 1-10 Blended Literacy 15m/15p c=0.73; ANZH 7m/10p c=1.00; 1-10 Mathematics 7m/18p c=1.00; 1-10 English 4m/4p c=1.00; Leaving to Learn 4m/4p c=1.00; 1-10 Arts 3m/3p c=1.00
- by era: Refresh 44m/64p c=0.97
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:158 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **ANZH101** ANZH101_0_0.html ↔ ANZH101_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-6.paddingR  «Understand»`
- **ANZH103** ANZH103_0_0.html ↔ ANZH103_0_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-6.paddingR  «UNDERSTAND»`
- **ANZH104** ANZH104_0_0.html ↔ ANZH104_00.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-6.paddingR`
- modules: ANZH101, ANZH103, ANZH104, ANZH105, ANZH203, ANZH205, ANZH401, ARFUN02, ARFUN03, ARFUN05, BLL110, BLL111, BLL120, BLL121, BLL134, BLL135, BLL144, BLL152, BLL160, BLL161, BLL172, BLL240, BLL241, BLL244 …

### #37 · module-menu · EXTRA · `ul` › gold `—` vs Claude `li` — CANDIDATE
- pages 80 / modules 42 / lines 165; consensus (all) 0.79 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 30m/68p c=0.79; Inquiry 10m/10p c=0.46; Fundamentals 2m/2p c=0.77
- by subject: 1-10 Blended Literacy 10m/10p c=0.60; 1-10 English 8m/11p c=0.75; ConnectED 7m/7p c=0.56; NCEA1 6m/16p c=0.97; Te ara Whakapuawa -Wellbeing 4m/4p c=0.12; 1-10 Science 3m/24p c=0.70
- by era: Refresh 42m/80p c=0.79
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1001** AGH1001_1_0.html ↔ AGH1001.01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `li  «to identify and describe New Zealand Agricultural and Horticultural primary production and production systems.»`
- **AGH1004** AGH1004_1_0.html ↔ AGH1004.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `li  «to demonstrate that place and purpose of production is influenced by interrelated environmental, social, cultural, and e»`
- **AGH1006** AGH1006_1_0.html ↔ AGH1006.01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `li  «to understand and identify Matauranga Māori values of kaitiakitanga and manaakitanga related to plant management practic»`
- modules: AGH1001, AGH1004, AGH1006, AGH1007, AGH1008, BLL115, BLL122, BLL123, BLL144, BLL145, BLL152, BLL165, BLL210, BLL241, BLL254, CEDK101, CEDO202, CEDO204, CEDO301, CEDR501, CEDT104, CEDT207, ENFUN03, ENFUN09 …

### #39 · module-menu · SUBSTITUTED · `div.col-12.col-md-6.paddingL` › gold `p` vs Claude `h5` — CANDIDATE
- pages 38 / modules 38 / lines 57; consensus (all) 0.03 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Fundamentals 14m/14p c=0.12; Standard 13m/13p c=0.02; Inquiry 11m/11p c=0.20
- by subject: 1-10 Health and PE 14m/14p c=0.61; ConnectED 7m/7p c=0.09; 1-10 Blended Literacy 5m/5p c=0.02; Te ara Whakapuawa -Wellbeing 4m/4p c=0.88; Leaving to Learn 4m/4p c=0.02; ANZH 2m/2p c=0.02
- by era: Refresh 38m/38p c=0.03
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:158 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **ANZH105** ANZH105_0_0.html ↔ ANZH105_00.0.html (structure, derivable=True)
  - gold: `p  «Ākonga will:»`
  - Claude: `h5  «Ākonga will:»`
- **ANZH205** ANZH205_0_0.html ↔ ANZH205_00.0.html (structure, derivable=True)
  - gold: `p  «You will:»`
  - Claude: `h5  «Ākonga will:»`
- **BLL172** BLL172_0_0.html ↔ BLL172-00.html (structure, derivable=True)
  - gold: `p  «We are learning:»`
  - Claude: `h5  «We are learning:»`
- modules: ANZH105, ANZH205, BLL172, BLL174, BLL175, BLL176, BLL177, CEDK102, CEDO102, CEDO202, CEDR204, CEDT404, CEDW101, CEDW201, ENGC302, ENGC401, HPFUN101, HPFUN102, HPFUN103, HPFUN201, HPFUN202, HPFUN203, HPFUN301, HPFUN303 …

### #40 · module-menu · MISSING · `div.col-12.col-md-6.paddingR` › gold `p` vs Claude `—` — CANDIDATE
- pages 50 / modules 36 / lines 67; consensus (all) 0.04 of 2349 gold pages with the region; derivable 0.72 (19 lines with no WT source)
- by template: Standard 28m/42p c=0.04; Inquiry 8m/8p c=0.18
- by subject: 1-10 Blended Literacy 23m/23p c=0.25; EXPlore 5m/8p c=0.00; ConnectED 3m/3p c=0.10; ANZH 2m/2p c=0.00; 1-10 Mathematics 2m/10p c=0.04; NCEA1 1m/4p c=0.00
- by era: Refresh 36m/50p c=0.04
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:158 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **ANZH104** ANZH104_0_0.html ↔ ANZH104_00.0.html (content, derivable=True)
  - gold: `p  «The ways different groups of people have lived and worked in this rohe have changed over time.»`
  - Claude: `—`
  - WT: `*The ways different groups of people have lived and worked in this rohe have changed over time.*`
- **ANZH105** ANZH105_0_0.html ↔ ANZH105_00.0.html (content, derivable=True)
  - gold: `p  «Relationships and connections between people and across boundaries have shaped the course of Aotearoa New Zealand’s hist»`
  - Claude: `—`
  - WT: `Relationships and connections between people and across boundaries have shaped the course of Aotearoa New Zealand’s histories.`
- **BLL110** BLL110_0_0.html ↔ BLL110.html (content, derivable=False)
  - gold: `p  «Shared codes and conventions enable us to make sense of what is heard, read, and seen.»`
  - Claude: `—`
- modules: ANZH104, ANZH105, BLL110, BLL111, BLL112, BLL113, BLL114, BLL115, BLL116, BLL117, BLL120, BLL121, BLL122, BLL124, BLL134, BLL135, BLL145, BLL146, BLL147, BLL153, BLL154, BLL160, BLL161, BLL214 …

### #43 · module-menu · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `h5` — CANDIDATE
- pages 81 / modules 25 / lines 107; consensus (all) 0.76 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 23m/78p c=0.73; Fundamentals 1m/1p c=0.99; Inquiry 1m/2p c=0.81
- by subject: Leaving to Learn 7m/15p c=0.86; 1-10 English 6m/13p c=0.46; NCEA1 3m/9p c=0.77; 1-10 Science 3m/24p c=0.88; ANZH 2m/13p c=1.00; Online Safety (OS9000) 2m/2p c=0.41
- by era: Refresh 25m/81p c=0.76
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1009** AGH1009_6_0.html ↔ AGH1009.06.1.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «You will show your understanding by:»`
- **ANZH301** ANZH301_1_0.html ↔ ANZH301_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «You will show your understanding by:»`
- **ANZH302** ANZH302_0_0.html ↔ ANZH302_0_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «Know:»`
- modules: AGH1009, ANZH301, ANZH302, CEDO501, ENFUN07, ENGC201, ENGC202, ENGI102, ENGI301, ENGS302, JPN1004, MXEO102, MXS1004, OSAI301, OSBY301, SCBI301, SCCH301, SCPH301, XDLS901, XDLS908, XLP01, XLP02, XLP03, XLP04 …

### #44 · module-menu · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `p` — CANDIDATE
- pages 55 / modules 25 / lines 70; consensus (all) 0.87 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 24m/53p c=0.86; Inquiry 1m/2p c=0.84
- by subject: Leaving to Learn 9m/20p c=0.64; NCEA1 7m/18p c=0.86; Online Safety (OS9000) 4m/8p c=0.81; ANZH 2m/3p c=1.00; 1-10 Mathematics 2m/5p c=0.93; 1-10 English 1m/1p c=0.84
- by era: Refresh 25m/55p c=0.87
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1003** AGH1003_3_0.html ↔ AGH1003_03.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «I can justify the use of key management practices due to the positive impact that they have on soil properties and plant»`
- **ANZH301** ANZH301_1_0.html ↔ ANZH301_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «In this lesson we are learning about the push and pull factors/reasons why more Māori moved to the cities before, during»`
- **ANZH302** ANZH302_0_0.html ↔ ANZH302_0_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Allow 10 hours for the learning in this module.»`
- modules: AGH1003, ANZH301, ANZH302, ENGC201, GEO1005, HIS1005, HIS1006, MXDI201, MXEO202, MXS1004, OSAI101, OSBY301, OSGM201, OSOH101, PES1002, PES1005, XDLS903, XDLS904, XDLS905, XDLS906, XDLS908, XLP01, XLP02, XLP03 …

### #46 · module-menu · EXTRA · `div.col-12.col-md-6.paddingR` › gold `—` vs Claude `p>b` — CANDIDATE
- pages 22 / modules 22 / lines 43; consensus (all) 1.00 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 19m/19p c=1.00; Inquiry 3m/3p c=1.00
- by subject: 1-10 Blended Literacy 22m/22p c=1.00
- by era: Refresh 22m/22p c=1.00
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:158 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **BLL125** BLL125_0_0.html ↔ BLL125-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Students develop basic literacy capability to read fluently and accurately. They engage with a variety of written texts,»`
- **BLL126** BLL126_0_0.html ↔ BLL126-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Students develop basic literacy capability to read fluently and accurately. They engage with a variety of written texts,»`
- **BLL127** BLL127_0_0.html ↔ BLL127-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Students develop basic literacy capability to read fluently and accurately. They engage with a variety of written texts,»`
- modules: BLL125, BLL126, BLL127, BLL130, BLL131, BLL132, BLL133, BLL136, BLL137, BLL140, BLL141, BLL143, BLL144, BLL145, BLL146, BLL147, BLL150, BLL151, BLL153, BLL154, BLL213, BLL214

### #47 · module-menu · SUBSTITUTED · `ul` › gold `li` vs Claude `li` — CANDIDATE
- pages 87 / modules 20 / lines 293; consensus (all) 0.58 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 20m/87p c=0.60
- by subject: 1-10 Mathematics 9m/28p c=0.54; NCEA1 4m/17p c=0.49; 1-10 English 3m/20p c=0.88; 1-10 Science 3m/21p c=0.85; Leaving to Learn 1m/1p c=0.72
- by era: Refresh 20m/87p c=0.58
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ENGC201** ENGC201_0_0.html ↔ ENGC201_0.0.html (structure, derivable=True)
  - gold: `li  «Being able to recognise and use the code, conventions, and features of diverse types of texts allows for a greater preci»`
  - Claude: `li  «People use language in diverse ways in different situations. This helps to signal social roles and relationships.»`
- **ENGC202** ENGC202_1_0.html ↔ ENGC202_1.0.html (structure, derivable=True)
  - gold: `li  «drawing what you hear from instructions»`
  - Claude: `li  «identify what makes a good instruction»`
- **ENGI103** ENGI103_0_0.html ↔ ENGI103_0.0.html (structure, derivable=True)
  - gold: `li  «Ākonga can communicate effectively, using appropriate words, tone, and gestures for different contexts.»`
  - Claude: `li  «Draw on my imagination and what is familiar to me to craft and share oral, written, visual, and multimodal texts as a wa»`
- modules: ENGC201, ENGC202, ENGI103, ENO2060, JPN1004, MXDB301, MXDB302, MXEX301, MXFL101, MXFL102, MXFL201, MXFL202, MXFU301, MXFU402, MXS1004, PES1004, SCBI301, SCCH301, SCPH301, XWHA02

### #54 · module-menu · EXTRA · `div.col-12.col-md-6.offset-md-0` › gold `—` vs Claude `p` — CANDIDATE
- pages 24 / modules 18 / lines 59; consensus (all) 0.99 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 18m/24p c=0.98
- by subject: 1-10 English 15m/16p c=0.94; 1-10 Social Science 2m/2p c=1.00; 1-10 Mathematics 1m/6p c=1.00
- by era: Refresh 18m/24p c=0.99
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:158 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **ENGC101** ENGC101_0_0.html ↔ ENGC101_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Communication depends on shared codes and conventions.»`
- **ENGC202** ENGC202_0_0.html ↔ ENGC202_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Students learn the rules of different types of texts and how to use these rules in various situations. They understand t»`
- **ENGI101** ENGI101_0_0.html ↔ ENGI101_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «These ideas include themes, messages, and opinions. I have my own ideas and stories that are worth sharing.»`
- modules: ENGC101, ENGC202, ENGI101, ENGI102, ENGI103, ENGI201, ENGI202, ENGI203, ENGI301, ENGI302, ENGI400, ENGI405, ENGS201, ENGS301, ENGS302, MXDB202, SSOG101, SSOG103

### #56 · module-menu · MISSING · `div#header` › gold `div#module-head-buttons` vs Claude `—` — CANDIDATE
- pages 31 / modules 17 / lines 31; consensus (all) 0.77 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 10m/16p c=0.78; Bilingual 5m/12p c=0.38; Inquiry 2m/3p c=0.83
- by subject: Te Marautanga o Aotearoa TMoA 5m/12p c=0.38; NCEA1 4m/4p c=0.73; 1-10 Blended Literacy 3m/6p c=0.45; ConnectED 2m/3p c=0.76; EXPlore 1m/1p c=1.00; 1-10 Mathematics 1m/2p c=0.78
- by era: Refresh 17m/31p c=0.77
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:94 — **Header:** `#module-code` → `<h1>` (module code or lesson number), then `<h1><span>Title</span></h1>`, then `#module-head-buttons` → `#module-menu-bu
  - KB: 13_SPLIT_MODE.md:70 — <div id="header"> … module-code, title h1(s), menu button, full #module-menu-content … </div>
  - KB: INDEX.md:115 — - Sections: 10 — Corpus-Validated Scaffolding Reference · 1. Header title casing · 2. Menu archetype — safe fallbacks (only when no reference/series p
- **BLL114** BLL114_1_0.html ↔ BLL114-02.html (structure, derivable=True)
  - gold: `div#module-head-buttons`
  - Claude: `—`
- **BLL116** BLL116_1_0.html ↔ BLL116-02.html (structure, derivable=True)
  - gold: `div#module-head-buttons`
  - Claude: `—`
- **BLL153** BLL153_1_0.html ↔ BLL153-1.0.html (structure, derivable=True)
  - gold: `div#module-head-buttons`
  - Claude: `—`
- modules: BLL114, BLL116, BLL153, CEDT207, CEDT301, EXPFUN07, GEO1004, HES1002, HES1006, MUS1004, MXFL401, PNR101, PNR102, PNR104, PNR107, TRR109, XLP06

### #57 · module-menu · EXTRA · `div.col-12.col-md-6.paddingR` › gold `—` vs Claude `p` — CANDIDATE
- pages 17 / modules 17 / lines 40; consensus (all) 0.95 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 14m/14p c=0.95; Inquiry 3m/3p c=0.74
- by subject: 1-10 Blended Literacy 8m/8p c=0.72; ConnectED 3m/3p c=0.88; 1-10 English 3m/3p c=0.99; ANZH 1m/1p c=0.97; 1-10 Mathematics 1m/1p c=0.95; Leaving to Learn 1m/1p c=1.00
- by era: Refresh 17m/17p c=0.95
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:158 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **ANZH401** ANZH401_0_0.html ↔ ANZH401_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Allow 15 hours for the learning in this module.»`
- **BLL123** BLL123_0_0.html ↔ BLL123-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Writing: Students use phonics and morphological knowledge to spell new, regular words and a growing number of irregular »`
- **BLL131** BLL131_0_0.html ↔ BLL131-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Students are familiar with the core conventions of written texts. This includes knowledge of letters, words, and the par»`
- modules: ANZH401, BLL123, BLL131, BLL174, BLL175, BLL176, BLL177, BLL242, BLL252, CEDK101, CEDK102, CEDT104, ENGC301, ENGC302, ENGC401, MXEX202, XWHA02

### #58 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `div.col-12.col-md-8` — CANDIDATE
- pages 98 / modules 16 / lines 98; consensus (all) 0.66 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 15m/97p c=0.62; Fundamentals 1m/1p c=0.99
- by subject: 1-10 Mathematics 12m/81p c=0.77; 1-10 English 2m/11p c=0.38; ConnectED 1m/5p c=0.54; 1-10 Languages 1m/1p c=0.60
- by era: Refresh 16m/98p c=0.66
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **CEDO105** CEDO105_1_0.html ↔ CEDO105.1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-8`
- **ENGI102** ENGI102_2_0.html ↔ ENGI102_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-8  «We are learning:»`
- **ENGI103** ENGI103_1_0.html ↔ ENGI103_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-8  «We are learning:»`
- modules: CEDO105, ENGI102, ENGI103, FRFUN06, MXDB301, MXDB302, MXDI301, MXEX101, MXEX301, MXEX302, MXFL204, MXFU201, MXFU202, MXFU301, MXFU302, MXFU402

### #59 · module-menu · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `ul` — CANDIDATE
- pages 43 / modules 16 / lines 75; consensus (all) 0.71 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 15m/42p c=0.68; Fundamentals 1m/1p c=0.99
- by subject: 1-10 English 4m/15p c=0.39; Leaving to Learn 4m/8p c=0.53; NCEA1 3m/11p c=0.79; ANZH 2m/3p c=1.00; ConnectED 1m/1p c=0.56; 1-10 Mathematics 1m/4p c=0.85
- by era: Refresh 16m/43p c=0.71
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1009** AGH1009_7_0.html ↔ AGH1009.07.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul  «identifying and describing sustainable practices to the impact of agricultural and horticultural production on water qua»`
- **ANZH301** ANZH301_1_0.html ↔ ANZH301_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul  «using multiple sources of information to help you answer the question: What were some of the reasons why Māori migrated »`
- **ANZH302** ANZH302_0_0.html ↔ ANZH302_0_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul  «Māori history is the foundational and continuous history of Aotearoa New Zealand.»`
- modules: AGH1009, ANZH301, ANZH302, CEDO501, ENFUN07, ENGC201, ENGC202, ENGI102, GEO1005, JPN1004, MXEO102, OSBY301, XLP01, XLP02, XLP03, XLP04

### #62 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `div.col-12.col-md-6.offset-md-0` — CANDIDATE
- pages 30 / modules 14 / lines 30; consensus (all) 0.95 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 12m/28p c=0.95; Fundamentals 2m/2p c=0.95
- by subject: 1-10 English 11m/27p c=0.90; 1-10 Mathematics 2m/2p c=0.94; 1-10 Social Science 1m/1p c=0.68
- by era: Refresh 14m/30p c=0.95
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:158 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **ENGC101** ENGC101_0_0.html ↔ ENGC101_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-6.offset-md-0  «In this module, we delve into the diverse tools and techniques we use to communicate effectively in various contexts. Fr»`
- **ENGC102** ENGC102_0_0.html ↔ ENGC102_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-6.offset-md-0  «Learning Intentions»`
- **ENGC201** ENGC201_0_0.html ↔ ENGC201_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-6.offset-md-0  «Learning Intentions»`
- modules: ENGC101, ENGC102, ENGC201, ENGI103, ENGI201, ENGI202, ENGI203, ENGI400, ENGJ102, ENGS202, ENGS301, MXFUN02, MXFUN03, SSOG101

### #63 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `div.col-12.col-md-12.paddingR` — CANDIDATE
- pages 16 / modules 14 / lines 16; consensus (all) 0.96 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 14m/16p c=0.96
- by subject: 1-10 Blended Literacy 12m/12p c=0.77; EXPlore 2m/4p c=1.00
- by era: Refresh 14m/16p c=0.96
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:158 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **BLL112** BLL112_0_0.html ↔ BLL112-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-12.paddingR  «Overview»`
- **BLL113** BLL113_0_0.html ↔ BLL113-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-12.paddingR  «Overview»`
- **BLL125** BLL125_0_0.html ↔ BLL125-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-12.paddingR  «Overview»`
- modules: BLL112, BLL113, BLL125, BLL141, BLL142, BLL143, BLL144, BLL162, BLL163, BLL166, BLL236, BLL237, EXBP901, EXIP901

### #64 · module-menu · SUBSTITUTED · `div.col-12.col-md-6.paddingR` › gold `ul` vs Claude `p>b` — CANDIDATE
- pages 14 / modules 14 / lines 14; consensus (all) 0.06 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 12m/12p c=0.05; Inquiry 2m/2p c=0.33
- by subject: 1-10 Blended Literacy 14m/14p c=0.28
- by era: Refresh 14m/14p c=0.06
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:158 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **BLL125** BLL125_0_0.html ↔ BLL125-01.html (structure, derivable=True)
  - gold: `ul  «Ākonga can use their basic literacy capability and can read fluently and accurately. They engage with a variety of writt»`
  - Claude: `p  «Students interpret texts by drawing on various elements and recognise different perspectives, sharing their own opinions»`
- **BLL126** BLL126_0_0.html ↔ BLL126-01.html (structure, derivable=True)
  - gold: `ul  «Ākonga can use their basic literacy capability and can read fluently and accurately. They engage with a variety of writt»`
  - Claude: `p  «Students interpret texts by drawing on various elements and recognise different perspectives, sharing their own opinions»`
- **BLL127** BLL127_0_0.html ↔ BLL127-01.html (structure, derivable=True)
  - gold: `ul  «Ākonga can use their basic literacy capability and can read fluently and accurately. They engage with a variety of writt»`
  - Claude: `p  «Students interpret texts by drawing on various elements and recognise different perspectives, sharing their own opinions»`
- modules: BLL125, BLL126, BLL127, BLL136, BLL137, BLL140, BLL141, BLL143, BLL146, BLL147, BLL150, BLL151, BLL153, BLL154

### #68 · module-menu · EXTRA · `div.col-12.col-md-6.paddingR` › gold `—` vs Claude `h5` — CANDIDATE
- pages 14 / modules 12 / lines 27; consensus (all) 0.99 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 10m/12p c=0.99; Inquiry 1m/1p c=1.00; Fundamentals 1m/1p c=1.00
- by subject: 1-10 Blended Literacy 4m/4p c=1.00; EXPlore 2m/4p c=1.00; ANZH 1m/1p c=1.00; ConnectED 1m/1p c=1.00; 1-10 English 1m/1p c=1.00; 1-10 Health and PE 1m/1p c=1.00
- by era: Refresh 12m/14p c=0.99
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:158 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **ANZH401** ANZH401_0_0.html ↔ ANZH401_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «Whakamaheretia tō wā | Planning your time»`
- **BLL145** BLL145_0_0.html ↔ BLL145-0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «Success Criteria»`
- **BLL153** BLL153_0_0.html ↔ BLL153-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «Success Criteria»`
- modules: ANZH401, BLL145, BLL153, BLL154, BLL236, CEDT104, ENGC302, EXBP901, EXIP901, HPFUN302, MXEX202, XWHA02

### #72 · module-menu · EXTRA · `li>b` › gold `—` vs Claude `b` — CANDIDATE
- pages 24 / modules 11 / lines 44; consensus (all) 0.99 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 11m/24p c=0.99
- by subject: NCEA1 3m/10p c=0.99; ConnectED 3m/8p c=0.98; ANZH 2m/2p c=1.00; 1-10 English 2m/3p c=1.00; Leaving to Learn 1m/1p c=0.99
- by era: Refresh 11m/24p c=0.99
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1004** AGH1004_4_0.html ↔ AGH1004.04.html (structure, derivable=True)
  - gold: `—`
  - Claude: `b  «soil types»`
- **AGH1005** AGH1005_2_0.html ↔ AGH1005.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `b  «plant anatomy»`
- **AGH1006** AGH1006_2_0.html ↔ AGH1006.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `b  «propagation practices»`
- modules: AGH1004, AGH1005, AGH1006, ANZH301, ANZH302, CEDO501, CEDO502, CEDT501, ENGC401, ENGS302, XLP01

### #441 · footer · MISSING · `ul.footer-nav` › gold `li>a#next-lesson` vs Claude `—` — CANDIDATE
- pages 97 / modules 60 / lines 97; consensus (all) 0.73 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 56m/93p c=0.76; Fundamentals 2m/2p c=0.27; Inquiry 2m/2p c=0.39
- by subject: Leaving to Learn 19m/20p c=0.65; 1-10 Mathematics 12m/24p c=0.88; Online Safety (OS9000) 9m/9p c=0.80; 1-10 English 7m/7p c=0.86; NCEA1 5m/12p c=0.88; 1-10 Blended Literacy 4m/4p c=0.12
- by era: Refresh 60m/97p c=0.73
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:40 — | Footer tag | `<nav id="module-foot">` with `<button>` + FA icons | `<div id="footer">` with `<ul class="footer-nav">` |
  - KB: 06_TEMPLATE_RECOGNITION.md:64 — | Footer `<ul>` class | `footer-nav` | `footer-nav` | `footer-nav fundamentals-nav` | `footer-nav inquiry-nav` | `footer-nav` |
  - KB: 06_TEMPLATE_RECOGNITION.md:114 — **Footer:** `<ul class="footer-nav">` with prev + next + home links.
- **ANZH401** ANZH401_0_0.html ↔ ANZH401_0.0.html (structure, derivable=True)
  - gold: `li`
  - Claude: `—`
- **ANZH404** ANZH404_0_0.html ↔ ANZH404_0.0.html (structure, derivable=True)
  - gold: `li`
  - Claude: `—`
- **BLL174** BLL174_0_0.html ↔ BLL174-00.html (structure, derivable=True)
  - gold: `li`
  - Claude: `—`
- modules: ANZH401, ANZH404, BLL174, BLL175, BLL176, BLL177, CEDO301, ENGJ101, ENGJ201, ENGJ301, ENGJ302, ENGJ402, ENGJ403, ENGR302, HIS1001, HIS1003, HIS1004, HIS1007, MXDB301, MXDB302, MXDI102, MXDI103, MXDI301, MXEX202 …
