# DIFF_QUEUE.md — the diff miner's ranked class queue (LOOP__Autonomous_Rounds.md §1d)

**Produced:** 2026-09-22 11:52 NZST by `reference/tests/_diff_miner.py` on the CURRENT corpus (pageforge-site HEAD cb2aa7e; Claude corpus 545 dirs). **Population:** the skeleton gate's own — 2491 paired pages / 533 modules (compare_exclusions.txt honoured; acks / glossary / references pages excluded); parse errors skipped: 0 (must be 0); modules without a parsed WT: 2. Run time 110.4 s.

**What a row is.** One CLASS = (region, parent element, gold form, Claude form, direction) over every differing skeleton line of every paired page — the same lines, labels, widget collapse and difflib alignment the PRIMARY gate scores (each element its own line so it can be quoted). Direction: MISSING = gold has it, Claude lacks it; EXTRA = Claude has it, gold lacks it; SUBSTITUTED = same position, different tag / class / wrapper; MOVED = same text, different place. Consensus = of the gold pages in the group where the region exists, the share carrying the gold form (for EXTRA: the share NOT carrying Claude's form). Derivable = the gold line's text is in the module's parsed Writers Template (round-110 tolerance); structure-only differences are always derivable.

**Candidate rule (§1d).** modules ≥ 10 for a chrome class (module-code / title / header / module-menu / crumbs / phases-nav / footer / acks), pages ≥ 20 for a body / activity class; gold consensus ≥ 0.60 in at least one template or subject group that itself reaches the floor; structure-only or derivable share ≥ 0.60. A class below the floor is listed, never dropped. A CANDIDATE still goes through the PICK's KB-first check, the triangulation and the §3 corpus-wide measurement before any code — this table is the queue, not the verdict.

## Summary

- differing skeleton lines: 283631 — by direction {'MISSING': 152921, 'SUBSTITUTED': 25199, 'EXTRA': 96012, 'MOVED': 9499}
- by region: {'module-code': 24, 'title': 400, 'header': 6, 'module-menu': 14616, 'phases-nav': 74, 'crumbs': 329, 'footer': 2594, 'acks': 1394, 'activity': 103208, 'body': 159349, 'root': 1637}
- classes: 9367 — CANDIDATE 190, below floor 8878, the rest below consensus / not derivable

## Completeness census — the repeating chrome (§1d item 4)

| region | pages with region | gold items | gold items in WT | Claude items | derivable misses | pages with misses | modules with misses | status |
|---|---|---|---|---|---|---|---|---|
| module-menu | 1544 | 17500 | 16160 | 12269 | 6131 | 781 | 215 | CANDIDATE (verify by eye — text presence, not position) |
| crumbs | 62 | 387 | 371 | 199 | 199 | 43 | 39 | CANDIDATE (verify by eye — text presence, not position) |
| phases-nav | 90 | 356 | 323 | 305 | 71 | 33 | 25 | CANDIDATE (verify by eye — text presence, not position) |
| footer | 15 | 74 | 58 | 0 | 58 | 15 | 7 | BELOW FLOOR |

- **module-menu** by template: Fundamentals 12m/22p/89 misses; Inquiry 34m/56p/520 misses; Standard 169m/703p/5522 misses
  - MXFL202 MXFL202_1_0.html: gold 53 items (51 in WT) / Claude 0 — 51 derivable misses, e.g. h3 «Understand» · span «Understand»
  - MXFL202 MXFL202_2_0.html: gold 53 items (51 in WT) / Claude 0 — 51 derivable misses, e.g. h3 «Understand» · span «Understand»
  - MXFL202 MXFL202_4_0.html: gold 53 items (51 in WT) / Claude 0 — 51 derivable misses, e.g. h3 «Understand» · span «Understand»
  - MXFL202 MXFL202_6_0.html: gold 53 items (51 in WT) / Claude 0 — 51 derivable misses, e.g. h3 «Understand» · span «Understand»
- **crumbs** by template: Fundamentals 0m/0p/0 misses; Inquiry 37m/37p/167 misses; Standard 2m/6p/32 misses
  - BLL240 BLL240_1_0.html: gold 8 items (8 in WT) / Claude 0 — 8 derivable misses, e.g. p «Introduction» · p «wh»
  - CEDK401 CEDK401_2_0.html: gold 9 items (8 in WT) / Claude 0 — 8 derivable misses, e.g. p «People produce food» · p «Research skills»
  - CEDR101 CEDR101_1_0.html: gold 8 items (8 in WT) / Claude 0 — 8 derivable misses, e.g. p «Introduction» · p «Games in Te Ao Māori»
  - BLL260 BLL260_6_1.html: gold 7 items (7 in WT) / Claude 0 — 7 derivable misses, e.g. p «Introduction» · p «str»
- **phases-nav** by template: Fundamentals 24m/32p/67 misses; Standard 1m/1p/4 misses
  - ANZHFUN05 ANZHFUN05_0_0.html: gold 4 items (4 in WT) / Claude 0 — 4 derivable misses, e.g. p «Phase 1» · p «Phase 2»
  - ARFUN04 ARFUN04_0_0.html: gold 4 items (4 in WT) / Claude 0 — 4 derivable misses, e.g. p «Phase 1» · p «Phase 2»
  - FRFUN06 FRFUN06_6_0.html: gold 6 items (6 in WT) / Claude 6 — 4 derivable misses, e.g. p «Handwriting è» · p «Handwriting ê â î ô û»
  - FRFUN06 FRFUN06_7_0.html: gold 6 items (6 in WT) / Claude 2 — 4 derivable misses, e.g. p «Chromebook» · p «Mac»
- **footer** by template: Inquiry 1m/7p/38 misses; Standard 6m/8p/20 misses
  - BLL240 BLL240_1_2.html: gold 6 items (6 in WT) / Claude 0 — 6 derivable misses, e.g. li «Previous» · a#prev-lesson «Previous»
  - BLL240 BLL240_1_3.html: gold 6 items (6 in WT) / Claude 0 — 6 derivable misses, e.g. li «Previous» · a#prev-lesson «Previous»
  - BLL240 BLL240_1_4.html: gold 6 items (6 in WT) / Claude 0 — 6 derivable misses, e.g. li «Previous» · a#prev-lesson «Previous»
  - BLL240 BLL240_1_5.html: gold 6 items (6 in WT) / Claude 0 — 6 derivable misses, e.g. li «Previous» · a#prev-lesson «Previous»

## Chrome facts — the header and footer as SETS per page (alignment-free; §1d items 2 + 4)

A fact is one thing a page's chrome has: `header:chip` (the `#module-code` div), `header:chip=module-code` / `=lesson-number` / `=lesson-number(00)`, `header:head-buttons`, `header:menu-content`, `header:title-h1-count=N`, `footer:present`, `footer:ul=<classes>`, `footer:link=prev-lesson` / `next-lesson` / `home-nav`, `footer:links=<order>`, `footer:inside-body`, `nav:crumbs`, `nav:phases`. MISSING = the gold page has the fact and Claude's does not; EXTRA the reverse. Consensus = the share of gold pages in the group that have (MISSING) / lack (EXTRA) the fact. Floor 10 modules.

| # | dir | fact | pages | modules | gold share (all) | consensus (all) | best group | status |
|---|---|---|---|---|---|---|---|---|
| F1 | MISSING | `header:title-h1-count=2` | 288 | 135 | 0.25 | 0.25 | subject+ptype=Online Safety (OS9000)/overview c=0.93 n=12 | CANDIDATE |
| F2 | EXTRA | `header:title-h1-count=1` | 285 | 132 | 0.75 | 0.25 | subject+ptype=Online Safety (OS9000)/overview c=0.93 n=12 | CANDIDATE |
| F3 | EXTRA | `header:chip=decimal-number` | 241 | 66 | 0.55 | 0.45 | template=Inquiry c=0.76 n=11 | CANDIDATE |
| F4 | MISSING | `header:chip=decimal-number` | 119 | 52 | 0.55 | 0.55 | subject=NCEA1 c=0.81 n=10 | CANDIDATE |
| F5 | MISSING | `header:chip=module-code` | 84 | 47 | 0.18 | 0.18 | template+ptype=Standard/overview c=0.73 n=13 | CANDIDATE |
| F6 | MISSING | `header:chip=lesson-number` | 202 | 43 | 0.20 | 0.20 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F7 | EXTRA | `header:chip=lesson-number` | 85 | 37 | 0.20 | 0.80 | era=Refresh c=0.80 n=37 | CANDIDATE |
| F8 | EXTRA | `header:menu-content` | 64 | 36 | 0.75 | 0.25 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F9 | EXTRA | `header:head-buttons` | 59 | 34 | 0.77 | 0.23 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F10 | EXTRA | `header:chip=module-code` | 30 | 30 | 0.18 | 0.82 | template=Standard c=0.85 n=16 | CANDIDATE |
| F11 | EXTRA | `header:chip=other` | 80 | 28 | 0.05 | 0.95 | ptype=lesson c=0.99 n=15 | CANDIDATE |
| F12 | MISSING | `header:head-buttons` | 50 | 28 | 0.77 | 0.77 | template=Standard c=0.78 n=14 | CANDIDATE |
| F13 | EXTRA | `header:title-h1-count=2` | 28 | 27 | 0.25 | 0.75 | template=Standard c=0.80 n=21 | CANDIDATE |
| F14 | MISSING | `header:title-h1-count=1` | 25 | 24 | 0.75 | 0.75 | template=Standard c=0.80 n=19 | CANDIDATE |
| F15 | MISSING | `header:chip=other` | 28 | 17 | 0.05 | 0.05 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F16 | MISSING | `header:menu-content` | 12 | 11 | 0.75 | 0.75 | era=Refresh c=0.75 n=11 | CANDIDATE |
| F17 | EXTRA | `header:chip` | 8 | 8 | 0.97 | 0.03 | — | BELOW FLOOR |
| F18 | MISSING | `header:title-h1-count=3` | 6 | 6 | 0.00 | 0.00 | — | BELOW FLOOR |
| F19 | EXTRA | `header:title-h1-count=0` | 5 | 5 | 0.00 | 1.00 | — | BELOW FLOOR |
| F20 | MISSING | `header:chip` | 4 | 4 | 0.97 | 0.97 | — | BELOW FLOOR |
| F21 | EXTRA | `header:title-h1-count=3` | 1 | 1 | 0.00 | 1.00 | — | BELOW FLOOR |
| F22 | EXTRA | `header:chip=lesson-number(00)` | 1 | 1 | 0.00 | 1.00 | — | BELOW FLOOR |
| F23 | MISSING | `nav:crumbs` | 24 | 24 | 0.02 | 0.02 | template+ptype=Inquiry/overview c=0.85 n=14 | CANDIDATE |
| F24 | MISSING | `nav:phases` | 10 | 10 | 0.04 | 0.04 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F25 | EXTRA | `nav:crumbs` | 2 | 2 | 0.02 | 0.98 | — | BELOW FLOOR |
| F26 | MISSING | `footer:inside-body` | 186 | 138 | 0.07 | 0.07 | subject+ptype=1-10 Languages/overview c=0.62 n=10 | CANDIDATE |
| F27 | EXTRA | `footer:links=prev-lesson,next-lesson,home-nav` | 283 | 128 | 0.60 | 0.40 | template+ptype=Standard/overview c=0.97 n=12 | CANDIDATE |
| F28 | EXTRA | `footer:links=next-lesson,home-nav` | 111 | 109 | 0.12 | 0.88 | template=Fundamentals c=0.99 n=10 | CANDIDATE |
| F29 | EXTRA | `footer:link=next-lesson` | 134 | 82 | 0.82 | 0.18 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F30 | EXTRA | `footer:links=prev-lesson,home-nav` | 81 | 81 | 0.14 | 0.86 | subject=1-10 English c=0.90 n=12 | CANDIDATE |
| F31 | MISSING | `footer:link=next-lesson` | 70 | 70 | 0.82 | 0.82 | template=Bilingual c=0.86 n=10 | CANDIDATE |
| F32 | MISSING | `footer:links=home-nav,next-lesson` | 70 | 69 | 0.03 | 0.03 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F33 | MISSING | `footer:links=prev-lesson,next-lesson,home-nav` | 68 | 65 | 0.60 | 0.60 | template+ptype=Bilingual/lesson c=0.82 n=10 | CANDIDATE |
| F34 | MISSING | `footer:links=prev-lesson,home-nav` | 91 | 61 | 0.14 | 0.14 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F35 | MISSING | `footer:links=home-nav,prev-lesson,next-lesson` | 122 | 57 | 0.05 | 0.05 | subject+ptype=1-10 Health and PE/overview c=0.71 n=12 | CANDIDATE |
| F36 | EXTRA | `footer:link=prev-lesson` | 60 | 43 | 0.80 | 0.20 | template+ptype=Standard/overview c=0.97 n=12 | CANDIDATE |
| F37 | MISSING | `footer:link=prev-lesson` | 31 | 30 | 0.80 | 0.80 | template+ptype=Standard/lesson c=0.98 n=14 | CANDIDATE |
| F38 | MISSING | `footer:ul=footer-nav` | 87 | 29 | 0.83 | 0.83 | template+ptype=Standard/lesson c=0.88 n=16 | CANDIDATE |
| F39 | MISSING | `footer:links=home-nav` | 37 | 24 | 0.04 | 0.04 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F40 | EXTRA | `footer:ul=footer-nav inquiry-nav` | 78 | 22 | 0.14 | 0.85 | ptype=lesson c=0.89 n=19 | CANDIDATE |
| F41 | MISSING | `footer:links=next-lesson,home-nav` | 22 | 22 | 0.12 | 0.12 | template+ptype=Standard/overview c=0.77 n=11 | CANDIDATE |
| F42 | EXTRA | `footer:ul=footer-nav` | 26 | 18 | 0.83 | 0.17 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F43 | EXTRA | `footer:ul=footer-nav fundamentals-nav` | 16 | 9 | 0.02 | 0.98 | — | BELOW FLOOR |
| F44 | MISSING | `footer:ul=footer-nav inquiry-nav` | 15 | 8 | 0.14 | 0.14 | — | BELOW FLOOR |
| F45 | MISSING | `footer:ul=footer-nav fundamentals-nav` | 8 | 8 | 0.02 | 0.02 | — | BELOW FLOOR |
| F46 | MISSING | `footer:links=home-nav,prev-lesson` | 7 | 7 | 0.00 | 0.00 | — | BELOW FLOOR |
| F47 | EXTRA | `footer:link=home-nav` | 11 | 5 | 1.00 | 0.00 | — | BELOW FLOOR |
| F48 | MISSING | `footer:links=prev-lesson,home-nav,next-lesson` | 30 | 4 | 0.01 | 0.01 | — | BELOW FLOOR |
| F49 | MISSING | `footer:link=other` | 20 | 4 | 0.01 | 0.01 | — | BELOW FLOOR |
| F50 | MISSING | `footer:links=prev-lesson,other,next-lesson,home-nav` | 14 | 3 | 0.01 | 0.01 | — | BELOW FLOOR |
| F51 | EXTRA | `footer:present` | 9 | 3 | 1.00 | 0.00 | — | BELOW FLOOR |
| F52 | MISSING | `footer:links=other,next-lesson,home-nav` | 3 | 3 | 0.00 | 0.00 | — | BELOW FLOOR |
| F53 | EXTRA | `footer:links=home-nav` | 3 | 3 | 0.04 | 0.96 | — | BELOW FLOOR |
| F54 | MISSING | `footer:links=prev-lesson,other,home-nav` | 2 | 2 | 0.00 | 0.00 | — | BELOW FLOOR |
| F55 | MISSING | `footer:links=other,home-nav` | 1 | 1 | 0.00 | 0.00 | — | BELOW FLOOR |
| F56 | MISSING | `footer:links=prev-lesson,next-lesson` | 1 | 1 | 0.00 | 0.00 | — | BELOW FLOOR |
| F57 | MISSING | `footer:links=none` | 1 | 1 | 0.00 | 0.00 | — | BELOW FLOOR |

### F1 · MISSING `header:title-h1-count=2` — CANDIDATE (pages 288 / modules 135)
- by template+ptype: Standard/overview 55m/55p gold 0.63 Claude 0.53 c=0.63; Standard/lesson 43m/163p gold 0.12 Claude 0.03 c=0.12; Fundamentals/overview 29m/29p gold 0.69 Claude 0.38 c=0.69; Inquiry/overview 7m/7p gold 0.58 Claude 0.49 c=0.58; Inquiry/lesson 7m/10p gold 0.20 Claude 0.02 c=0.20; Bilingual/overview 6m/6p gold 1.00 Claude 0.70 c=1.00; Bilingual/lesson 6m/18p gold 1.00 Claude 0.70 c=1.00
- by subject: NCEA1 22m/56p gold 0.20 Claude 0.11 c=0.20; 1-10 English 21m/32p gold 0.18 Claude 0.09 c=0.18; Leaving to Learn 15m/23p gold 0.33 Claude 0.25 c=0.33; Online Safety (OS9000) 13m/29p gold 0.32 Claude 0.11 c=0.32; 1-10 Mathematics 11m/11p gold 0.14 Claude 0.11 c=0.14; ConnectED 9m/9p gold 0.28 Claude 0.21 c=0.28; 1-10 Technology 7m/19p gold 1.00 Claude 0.24 c=1.00; ANZH 6m/31p gold 0.49 Claude 0.17 c=0.49
- **AGH1005** AGH1005_0_0.html ↔ AGH1005.00.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=3']
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ANZH103** ANZH103_0_0.html ↔ ANZH103_0_0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: AGH1005, ANZH101, ANZH103, ANZH104, ANZH301, ANZH401, ANZH404, ARFUN01, ARFUN02, ARFUN03, ARFUN04, ARFUN05, ART1006, CEDK102, CEDK401, CEDK501, CEDO202, CEDO502, CEDR101, CEDR204, CEDR401, CEDT301, CHI1004, CHI1005 …

### F2 · EXTRA `header:title-h1-count=1` — CANDIDATE (pages 285 / modules 132)
- by template+ptype: Standard/overview 54m/54p gold 0.35 Claude 0.46 c=0.65; Standard/lesson 42m/162p gold 0.88 Claude 0.97 c=0.12; Fundamentals/overview 27m/27p gold 0.31 Claude 0.59 c=0.69; Inquiry/overview 8m/8p gold 0.38 Claude 0.51 c=0.62; Inquiry/lesson 7m/10p gold 0.80 Claude 0.98 c=0.20; Bilingual/overview 6m/6p gold 0.00 Claude 0.30 c=1.00; Bilingual/lesson 6m/18p gold 0.00 Claude 0.29 c=1.00
- by subject: 1-10 English 21m/32p gold 0.82 Claude 0.91 c=0.18; NCEA1 20m/54p gold 0.80 Claude 0.88 c=0.20; Leaving to Learn 15m/23p gold 0.68 Claude 0.75 c=0.33; Online Safety (OS9000) 13m/29p gold 0.68 Claude 0.89 c=0.32; 1-10 Mathematics 11m/11p gold 0.85 Claude 0.89 c=0.14; ConnectED 9m/9p gold 0.72 Claude 0.79 c=0.28; 1-10 Technology 7m/19p gold 0.00 Claude 0.76 c=1.00; ANZH 6m/31p gold 0.51 Claude 0.83 c=0.49
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ANZH103** ANZH103_0_0.html ↔ ANZH103_0_0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ANZH104** ANZH104_4_0.html ↔ ANZH104_04.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1']
- modules: ANZH101, ANZH103, ANZH104, ANZH301, ANZH401, ANZH404, ARFUN02, ARFUN03, ARFUN04, ARFUN05, ART1006, CEDK102, CEDK401, CEDK501, CEDO202, CEDO502, CEDR101, CEDR204, CEDR401, CEDT301, CHI1004, CHI1005, CHWHA, DTC1005 …

### F3 · EXTRA `header:chip=decimal-number` — CANDIDATE (pages 241 / modules 66)
- by template+ptype: Standard/lesson 53m/202p gold 0.69 Claude 0.74 c=0.31; Inquiry/lesson 11m/29p gold 0.43 Claude 0.95 c=0.57; Bilingual/lesson 2m/10p gold 0.67 Claude 0.84 c=0.33
- by subject: 1-10 Blended Literacy 19m/40p gold 0.39 Claude 0.37 c=0.61; 1-10 English 9m/41p gold 0.60 Claude 0.69 c=0.40; NCEA1 8m/24p gold 0.81 Claude 0.79 c=0.19; Leaving to Learn 8m/38p gold 0.38 Claude 0.49 c=0.62; 1-10 Mathematics 5m/18p gold 0.72 Claude 0.74 c=0.28; ANZH 4m/19p gold 0.46 Claude 0.66 c=0.54; ConnectED 4m/4p gold 0.66 Claude 0.69 c=0.34; 1-10 Languages 2m/11p gold 0.48 Claude 0.63 c=0.52
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ANZH103** ANZH103_1_0.html ↔ ANZH103_3_0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ANZH203** ANZH203_1_0.html ↔ ANZH203_1.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: ANZH101, ANZH103, ANZH203, ANZH302, BLL236, BLL240, BLL250, BLL253, BLL255, BLL260, BLL261, BLL262, BLL263, BLL264, BLL265, BLL266, BLL270, BLL271, BLL272, BLL273, BLL274, BLL275, BLL276, CEDK401 …

### F4 · MISSING `header:chip=decimal-number` — CANDIDATE (pages 119 / modules 52)
- by template+ptype: Standard/lesson 41m/107p gold 0.69 Claude 0.74 c=0.69; Standard/overview 6m/6p gold 0.02 Claude 0.00 c=0.02; Bilingual/overview 3m/3p gold 0.15 Claude 0.00 c=0.15; Inquiry/overview 2m/2p gold 0.04 Claude 0.00 c=0.04; Fundamentals/overview 1m/1p gold 0.01 Claude 0.00 c=0.01
- by subject: 1-10 Blended Literacy 24m/46p gold 0.39 Claude 0.37 c=0.39; NCEA1 10m/35p gold 0.81 Claude 0.79 c=0.81; 1-10 Mathematics 6m/10p gold 0.72 Claude 0.74 c=0.72; Leaving to Learn 4m/12p gold 0.38 Claude 0.49 c=0.38; Te Marautanga o Aotearoa TMoA 3m/3p gold 0.54 Claude 0.63 c=0.54; 1-10 English 2m/9p gold 0.60 Claude 0.69 c=0.60; ConnectED 1m/1p gold 0.66 Claude 0.69 c=0.66; 1-10 Languages 1m/1p gold 0.48 Claude 0.63 c=0.48
- **ART1004** ART1004_0_0.html ↔ ART1004_4.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **ART1005** ART1005_0_0.html ↔ ART1005_3.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **BLL141** BLL141_1_0.html ↔ BLL141-1.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- modules: ART1004, ART1005, BLL141, BLL142, BLL143, BLL144, BLL145, BLL146, BLL147, BLL151, BLL152, BLL154, BLL156, BLL157, BLL161, BLL162, BLL163, BLL164, BLL165, BLL166, BLL167, BLL171, BLL172, BLL173 …

### F5 · MISSING `header:chip=module-code` — CANDIDATE (pages 84 / modules 47)
- by template+ptype: Standard/lesson 20m/46p gold 0.04 Claude 0.01 c=0.04; Standard/overview 13m/13p gold 0.73 Claude 0.73 c=0.73; Inquiry/lesson 8m/8p gold 0.14 Claude 0.00 c=0.14; Bilingual/lesson 5m/16p gold 0.31 Claude 0.05 c=0.31; Inquiry/overview 1m/1p gold 0.36 Claude 0.45 c=0.36
- by subject: 1-10 Blended Literacy 18m/18p gold 0.07 Claude 0.02 c=0.07; NCEA1 6m/6p gold 0.14 Claude 0.14 c=0.14; 1-10 Mathematics 5m/18p gold 0.16 Claude 0.11 c=0.16; Te Marautanga o Aotearoa TMoA 5m/16p gold 0.44 Claude 0.28 c=0.44; ConnectED 3m/3p gold 0.10 Claude 0.08 c=0.10; Leaving to Learn 3m/5p gold 0.22 Claude 0.25 c=0.22; 1-10 English 2m/2p gold 0.13 Claude 0.13 c=0.13; EXPlore 2m/2p gold 0.27 Claude 0.13 c=0.27
- **ANZH401** ANZH401_1_0.html ↔ ANZH401_1.0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **BLL170** BLL170_0_0.html ↔ BLL170.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **BLL172** BLL172_0_0.html ↔ BLL172-00.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: ANZH401, BLL170, BLL172, BLL174, BLL175, BLL176, BLL177, BLL240, BLL250, BLL252, BLL253, BLL260, BLL265, BLL266, BLL270, BLL271, BLL273, BLL274, BLL276, CEDK501, CEDR101, CEDT207, CHI1004, ENGR102 …

### F7 · EXTRA `header:chip=lesson-number` — CANDIDATE (pages 85 / modules 37)
- by template+ptype: Standard/lesson 32m/77p gold 0.26 Claude 0.20 c=0.74; Bilingual/lesson 3m/6p gold 0.02 Claude 0.12 c=0.98; Inquiry/lesson 2m/2p gold 0.38 Claude 0.04 c=0.62
- by subject: 1-10 Blended Literacy 22m/44p gold 0.26 Claude 0.29 c=0.74; Leaving to Learn 5m/15p gold 0.35 Claude 0.26 c=0.65; ConnectED 3m/3p gold 0.06 Claude 0.09 c=0.94; Te Marautanga o Aotearoa TMoA 3m/6p gold 0.01 Claude 0.09 c=0.99; 1-10 English 2m/9p gold 0.23 Claude 0.16 c=0.77; NCEA1 1m/5p gold 0.04 Claude 0.02 c=0.95; 1-10 Mathematics 1m/3p gold 0.10 Claude 0.11 c=0.90
- **BLL141** BLL141_1_0.html ↔ BLL141-1.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- **BLL142** BLL142_1_0.html ↔ BLL142-1.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- **BLL143** BLL143_1_0.html ↔ BLL143-1.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- modules: BLL141, BLL142, BLL143, BLL144, BLL145, BLL146, BLL147, BLL151, BLL152, BLL154, BLL156, BLL157, BLL161, BLL162, BLL163, BLL164, BLL165, BLL166, BLL167, BLL171, BLL172, BLL173, CEDR101, CEDR401 …

### F10 · EXTRA `header:chip=module-code` — CANDIDATE (pages 30 / modules 30)
- by template+ptype: Standard/overview 12m/12p gold 0.73 Claude 0.73 c=0.27; Inquiry/overview 6m/6p gold 0.36 Claude 0.45 c=0.64; Fundamentals/overview 5m/5p gold 0.64 Claude 0.70 c=0.36; Standard/lesson 4m/4p gold 0.04 Claude 0.01 c=0.96; Bilingual/overview 3m/3p gold 0.85 Claude 1.00 c=0.15
- by subject: Leaving to Learn 11m/11p gold 0.22 Claude 0.25 c=0.78; NCEA1 7m/7p gold 0.14 Claude 0.14 c=0.86; Te Marautanga o Aotearoa TMoA 3m/3p gold 0.44 Claude 0.28 c=0.56; 1-10 Health and PE 2m/2p gold 0.42 Claude 0.47 c=0.58; 1-10 Social Science 2m/2p gold 0.22 Claude 0.23 c=0.78; 1-10 Blended Literacy 1m/1p gold 0.07 Claude 0.02 c=0.93; ConnectED 1m/1p gold 0.10 Claude 0.08 c=0.90; 1-10 Languages 1m/1p gold 0.23 Claude 0.25 c=0.77
- **ART1004** ART1004_0_0.html ↔ ART1004_4.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **ART1005** ART1005_0_0.html ↔ ART1005_3.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **BLL240** BLL240_0_0.html ↔ BLL240-0.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: ART1004, ART1005, BLL240, CEDO402, COM1002, ENG1004, ENGFUN02, FRFUN06, GEO1004, GER1002, HPFUN201, HPFUN302, MXDB201, OSOH101, SSFUN01, SSFUN07, TRR112, TRR113, TRR116, XDLS901, XDLS902, XDLS903, XDLS909, XFUN01 …

### F11 · EXTRA `header:chip=other` — CANDIDATE (pages 80 / modules 28)
- by template+ptype: Standard/lesson 15m/67p gold 0.01 Claude 0.04 c=0.99; Standard/overview 13m/13p gold 0.25 Claude 0.27 c=0.75
- by subject: 1-10 Blended Literacy 14m/14p gold 0.26 Claude 0.29 c=0.74; 1-10 Mathematics 5m/7p gold 0.00 Claude 0.02 c=1.00; NCEA1 4m/29p gold 0.01 Claude 0.05 c=0.99; 1-10 Social Science 3m/17p gold 0.00 Claude 0.28 c=1.00; ANZH 1m/12p gold 0.07 Claude 0.20 c=0.94; Leaving to Learn 1m/1p gold 0.04 Claude 0.00 c=0.96
- **ANZH401** ANZH401_1_0.html ↔ ANZH401_1.0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **BLL172** BLL172_0_0.html ↔ BLL172-00.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **BLL174** BLL174_0_0.html ↔ BLL174-00.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: ANZH401, BLL172, BLL174, BLL175, BLL176, BLL177, BLL252, BLL253, BLL265, BLL266, BLL271, BLL273, BLL274, BLL276, BLLR203, MXDB301, MXEO301, MXEX301, MXFL302, MXFU302, PWY1001, PWY1002, PWY1008, PWY1009 …

### F12 · MISSING `header:head-buttons` — CANDIDATE (pages 50 / modules 28)
- by template+ptype: Standard/lesson 12m/19p gold 0.75 Claude 0.75 c=0.75; Inquiry/lesson 7m/8p gold 0.75 Claude 0.64 c=0.75; Bilingual/lesson 7m/20p gold 0.33 Claude 0.00 c=0.33; Standard/overview 3m/3p gold 0.98 Claude 0.99 c=0.98
- by subject: 1-10 Blended Literacy 8m/13p gold 0.46 Claude 0.42 c=0.46; Te Marautanga o Aotearoa TMoA 7m/20p gold 0.46 Claude 0.25 c=0.46; NCEA1 5m/5p gold 0.73 Claude 0.75 c=0.73; ConnectED 3m/4p gold 0.77 Claude 0.87 c=0.77; Leaving to Learn 2m/4p gold 0.90 Claude 0.89 c=0.90; EXPlore 1m/1p gold 1.00 Claude 0.93 c=1.00; 1-10 Mathematics 1m/2p gold 0.78 Claude 0.78 c=0.78; Te ara Whakapuawa -Wellbeing 1m/1p gold 1.00 Claude 0.92 c=1.00
- **BLL114** BLL114_1_0.html ↔ BLL114-02.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- **BLL116** BLL116_1_0.html ↔ BLL116-02.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- **BLL153** BLL153_1_0.html ↔ BLL153-1.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- modules: BLL114, BLL116, BLL153, BLL236, BLL250, BLL260, BLL270, BLL272, CEDK401, CEDT207, CEDT301, EXPFUN07, GEO1004, HES1002, HES1006, MUS1004, MXFL401, PMT101, PNR101, PNR102, PNR104, PNR107, PWYWHA1, TRR109 …

### F13 · EXTRA `header:title-h1-count=2` — CANDIDATE (pages 28 / modules 27)
- by template+ptype: Standard/overview 18m/18p gold 0.63 Claude 0.53 c=0.37; Standard/lesson 4m/4p gold 0.12 Claude 0.03 c=0.88; Fundamentals/overview 4m/4p gold 0.69 Claude 0.38 c=0.31; Inquiry/overview 2m/2p gold 0.58 Claude 0.49 c=0.41
- by subject: NCEA1 7m/7p gold 0.20 Claude 0.11 c=0.80; 1-10 Blended Literacy 6m/6p gold 0.01 Claude 0.03 c=0.99; Leaving to Learn 5m/5p gold 0.33 Claude 0.25 c=0.68; 1-10 Languages 3m/3p gold 0.28 Claude 0.23 c=0.72; 1-10 Writing (MiW) 2m/2p gold 0.62 Claude 0.52 c=0.38; ANZH 1m/2p gold 0.49 Claude 0.17 c=0.51; ConnectED 1m/1p gold 0.28 Claude 0.21 c=0.72; 1-10 English 1m/1p gold 0.18 Claude 0.09 c=0.82
- **ANZH302** ANZH302_0_0.html ↔ ANZH302_0_0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2']
- **BLL246** BLL246_0_0.html ↔ BLL246_0.0.html: gold ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2']
- **BLL271** BLL271_0_0.html ↔ BLL271_0_0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2']
- modules: ANZH302, BLL246, BLL271, BLL272, BLL273, BLL274, BLL276, CEDO105, ENGFUN02, ENGI103, FRFUN06, GENO901, GEWHA, HIS1002, JPN1004, PHE1004, PWY1002, PWYWHA1, SPA1004, SSFUN07, WJFUN105, WJFUN116, XDLS904, XDLS906 …

### F14 · MISSING `header:title-h1-count=1` — CANDIDATE (pages 25 / modules 24)
- by template+ptype: Standard/overview 16m/16p gold 0.35 Claude 0.46 c=0.35; Standard/lesson 4m/4p gold 0.88 Claude 0.97 c=0.88; Fundamentals/overview 4m/4p gold 0.31 Claude 0.59 c=0.31; Inquiry/overview 1m/1p gold 0.38 Claude 0.51 c=0.38
- by subject: NCEA1 6m/6p gold 0.80 Claude 0.88 c=0.80; 1-10 Blended Literacy 6m/6p gold 0.99 Claude 0.97 c=0.99; Leaving to Learn 5m/5p gold 0.68 Claude 0.75 c=0.68; 1-10 Writing (MiW) 2m/2p gold 0.38 Claude 0.48 c=0.38; ANZH 1m/2p gold 0.51 Claude 0.83 c=0.51; ConnectED 1m/1p gold 0.72 Claude 0.79 c=0.72; 1-10 English 1m/1p gold 0.82 Claude 0.91 c=0.82; 1-10 Languages 1m/1p gold 0.68 Claude 0.77 c=0.68
- **ANZH302** ANZH302_0_0.html ↔ ANZH302_0_0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2']
- **ART1004** ART1004_0_0.html ↔ ART1004_4.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **ART1005** ART1005_0_0.html ↔ ART1005_3.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- modules: ANZH302, ART1004, ART1005, BLL246, BLL271, BLL272, BLL273, BLL274, BLL276, CEDO105, ENGFUN02, ENGI103, FRFUN06, HIS1002, PWY1002, PWYWHA1, SSFUN07, WJFUN105, WJFUN116, XDLS904, XDLS906, XFUN02, XGF9004, XOTPB08

### F16 · MISSING `header:menu-content` — CANDIDATE (pages 12 / modules 11)
- by template+ptype: Inquiry/lesson 7m/8p gold 0.75 Claude 0.64 c=0.75; Standard/lesson 4m/4p gold 0.73 Claude 0.75 c=0.73
- by subject: 1-10 Blended Literacy 3m/3p gold 0.43 Claude 0.42 c=0.43; ConnectED 3m/4p gold 0.77 Claude 0.87 c=0.77; NCEA1 3m/3p gold 0.73 Claude 0.75 c=0.73; Te ara Whakapuawa -Wellbeing 1m/1p gold 1.00 Claude 0.92 c=1.00; Leaving to Learn 1m/1p gold 0.89 Claude 0.89 c=0.89
- **BLL250** BLL250_2_5.html ↔ BLL250.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1']
- **BLL260** BLL260_6_1.html ↔ BLL260.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1']
- **BLL270** BLL270_2_0.html ↔ BLL270.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1']
- modules: BLL250, BLL260, BLL270, CEDK401, CEDT207, CEDT301, GEO1004, HES1006, MUS1004, TWHT903, XGF9004

### F23 · MISSING `nav:crumbs` — CANDIDATE (pages 24 / modules 24)
- by template+ptype: Inquiry/overview 14m/14p gold 0.85 Claude 0.58 c=0.85; Inquiry/lesson 9m/9p gold 0.16 Claude 0.00 c=0.16; Standard/lesson 1m/1p gold 0.00 Claude 0.00 c=0.00
- by subject: ConnectED 14m/14p gold 0.19 Claude 0.07 c=0.19; Te ara Whakapuawa -Wellbeing 5m/5p gold 1.00 Claude 0.61 c=1.00; 1-10 Blended Literacy 4m/4p gold 0.04 Claude 0.03 c=0.04; EXPlore 1m/1p gold 0.73 Claude 0.67 c=0.73
- **BLL240** BLL240_1_0.html ↔ BLL240.html: gold ['nav:crumbs'] · Claude []
- **BLL250** BLL250_2_5.html ↔ BLL250.html: gold ['nav:crumbs'] · Claude []
- **BLL260** BLL260_6_1.html ↔ BLL260.html: gold ['nav:crumbs'] · Claude []
- modules: BLL240, BLL250, BLL260, BLL270, CEDK401, CEDK501, CEDO201, CEDO204, CEDO402, CEDR101, CEDR203, CEDR401, CEDT102, CEDT104, CEDT207, CEDT208, CEDT301, CEDW201, EXIP901, TWHA905, TWHK901, TWHK902, TWHR905, TWHT903

### F26 · MISSING `footer:inside-body` — CANDIDATE (pages 186 / modules 138)
- by template+ptype: Standard/lesson 75m/104p gold 0.06 Claude 0.00 c=0.06; Standard/overview 46m/46p gold 0.13 Claude 0.00 c=0.13; Fundamentals/overview 19m/19p gold 0.23 Claude 0.00 c=0.23; Inquiry/overview 10m/10p gold 0.19 Claude 0.00 c=0.19; Inquiry/lesson 2m/2p gold 0.04 Claude 0.00 c=0.04; Fundamentals/lesson 2m/3p gold 0.08 Claude 0.00 c=0.08; Bilingual/lesson 1m/1p gold 0.02 Claude 0.00 c=0.02; Bilingual/overview 1m/1p gold 0.05 Claude 0.00 c=0.05
- by subject: 1-10 Blended Literacy 35m/46p gold 0.14 Claude 0.00 c=0.14; Leaving to Learn 20m/27p gold 0.11 Claude 0.00 c=0.11; 1-10 English 16m/22p gold 0.06 Claude 0.00 c=0.06; 1-10 Mathematics 15m/28p gold 0.08 Claude 0.00 c=0.08; NCEA1 12m/18p gold 0.03 Claude 0.00 c=0.03; 1-10 Languages 11m/12p gold 0.18 Claude 0.00 c=0.18; 1-10 Social Science 5m/5p gold 0.08 Claude 0.00 c=0.08; Te ara Whakapuawa -Wellbeing 5m/5p gold 0.39 Claude 0.00 c=0.39
- **ANZH101** ANZH101_0_0.html ↔ ANZH101_0.0.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH103** ANZH103_0_0.html ↔ ANZH103_0_0.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH302** ANZH302_3_0.html ↔ ANZH302_3_0.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: ANZH101, ANZH103, ANZH302, ARFUN02, ARFUN03, ARFUN04, ARFUN05, BLL113, BLL120, BLL122, BLL124, BLL125, BLL130, BLL145, BLL154, BLL156, BLL162, BLL164, BLL165, BLL166, BLL171, BLL173, BLL211, BLL212 …

### F27 · EXTRA `footer:links=prev-lesson,next-lesson,home-nav` — CANDIDATE (pages 283 / modules 128)
- by template+ptype: Standard/lesson 75m/203p gold 0.74 Claude 0.83 c=0.26; Inquiry/overview 26m/26p gold 0.15 Claude 0.64 c=0.85; Fundamentals/overview 13m/13p gold 0.05 Claude 0.20 c=0.95; Standard/overview 12m/12p gold 0.03 Claude 0.05 c=0.97; Inquiry/lesson 9m/19p gold 0.46 Claude 0.79 c=0.54; Bilingual/lesson 2m/2p gold 0.82 Claude 0.69 c=0.18; Fundamentals/lesson 1m/8p gold 0.69 Claude 0.89 c=0.31
- by subject: NCEA1 36m/60p gold 0.74 Claude 0.82 c=0.26; ConnectED 15m/21p gold 0.64 Claude 0.80 c=0.36; 1-10 Blended Literacy 12m/15p gold 0.42 Claude 0.41 c=0.58; 1-10 Health and PE 12m/12p gold 0.56 Claude 0.89 c=0.44; Leaving to Learn 10m/39p gold 0.47 Claude 0.62 c=0.53; 1-10 English 9m/35p gold 0.64 Claude 0.72 c=0.36; 1-10 Mathematics 9m/52p gold 0.62 Claude 0.77 c=0.38; Te ara Whakapuawa -Wellbeing 7m/7p gold 0.00 Claude 0.54 c=1.00
- **AGH1008** AGH1008_8_0.html ↔ AGH1008.08.html: gold ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH401** ANZH401_1_0.html ↔ ANZH401_1.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH404** ANZH404_1_0.html ↔ ANZH404_1.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: AGH1008, ANZH401, ANZH404, ANZHFUN05, ART1002, BLL120, BLL140, BLL150, BLL170, BLL175, BLL210, BLL220, BLL230, BLL240, BLL270, BLLR202, BLLR203, CBI1004, CBI1005, CBI1008, CBI1009, CEDK101, CEDK102, CEDK401 …

### F28 · EXTRA `footer:links=next-lesson,home-nav` — CANDIDATE (pages 111 / modules 109)
- by template+ptype: Standard/overview 74m/74p gold 0.77 Claude 0.95 c=0.23; Standard/lesson 14m/15p gold 0.01 Claude 0.01 c=0.99; Fundamentals/overview 10m/10p gold 0.01 Claude 0.14 c=0.99; Inquiry/overview 9m/9p gold 0.02 Claude 0.17 c=0.98; Bilingual/overview 3m/3p gold 0.85 Claude 1.00 c=0.15
- by subject: Leaving to Learn 39m/40p gold 0.08 Claude 0.25 c=0.92; NCEA1 13m/14p gold 0.11 Claude 0.11 c=0.89; 1-10 Mathematics 13m/13p gold 0.07 Claude 0.11 c=0.93; Online Safety (OS9000) 9m/9p gold 0.15 Claude 0.21 c=0.85; 1-10 English 8m/8p gold 0.11 Claude 0.13 c=0.89; 1-10 Blended Literacy 6m/6p gold 0.29 Claude 0.29 c=0.71; ConnectED 6m/6p gold 0.06 Claude 0.10 c=0.94; 1-10 Social Science 6m/6p gold 0.13 Claude 0.23 c=0.87
- **ANZH401** ANZH401_0_0.html ↔ ANZH401_0.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH404** ANZH404_0_0.html ↔ ANZH404_0.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ART1004** ART1004_0_0.html ↔ ART1004_4.0.html: gold ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: ANZH401, ANZH404, ART1004, ART1005, BLL114, BLL116, BLL174, BLL175, BLL176, BLL177, CEDO301, CEDT102, CEDT104, CEDT207, CEDT208, CEDT301, COM1002, ENG1004, ENGFUN02, ENGI101, ENGI102, ENGJ101, ENGJ102, ENGJ301 …

### F30 · EXTRA `footer:links=prev-lesson,home-nav` — CANDIDATE (pages 81 / modules 81)
- by template+ptype: Standard/lesson 61m/61p gold 0.17 Claude 0.16 c=0.83; Bilingual/lesson 11m/11p gold 0.15 Claude 0.31 c=0.85; Inquiry/lesson 7m/7p gold 0.20 Claude 0.21 c=0.80; Fundamentals/lesson 2m/2p gold 0.06 Claude 0.11 c=0.94
- by subject: 1-10 Blended Literacy 22m/22p gold 0.23 Claude 0.30 c=0.77; 1-10 English 12m/12p gold 0.10 Claude 0.13 c=0.90; Te Marautanga o Aotearoa TMoA 11m/11p gold 0.11 Claude 0.23 c=0.89; NCEA1 8m/8p gold 0.11 Claude 0.06 c=0.89; 1-10 Mathematics 8m/8p gold 0.09 Claude 0.11 c=0.91; ANZH 5m/5p gold 0.08 Claude 0.13 c=0.92; ConnectED 5m/5p gold 0.05 Claude 0.09 c=0.95; Leaving to Learn 4m/4p gold 0.31 Claude 0.13 c=0.69
- **AGH1004** AGH1004_6_0.html ↔ AGH1004.07.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **AGH1009** AGH1009_9_0.html ↔ AGH1009.09.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH103** ANZH103_1_0.html ↔ ANZH103_3_0.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: AGH1004, AGH1009, ANZH103, ANZH205, ANZH301, ANZH302, ANZH303, BLL141, BLL146, BLL151, BLL157, BLL167, BLL171, BLL176, BLL177, BLL224, BLL225, BLL226, BLL227, BLL231, BLL234, BLL236, BLL237, BLL250 …

### F31 · MISSING `footer:link=next-lesson` — CANDIDATE (pages 70 / modules 70)
- by template+ptype: Standard/lesson 52m/52p gold 0.82 Claude 0.84 c=0.82; Bilingual/lesson 10m/10p gold 0.82 Claude 0.69 c=0.82; Inquiry/lesson 5m/5p gold 0.70 Claude 0.79 c=0.70; Inquiry/overview 2m/2p gold 0.77 Claude 0.85 c=0.77; Fundamentals/lesson 1m/1p gold 0.69 Claude 0.89 c=0.69
- by subject: 1-10 Blended Literacy 21m/21p gold 0.75 Claude 0.70 c=0.75; Te Marautanga o Aotearoa TMoA 10m/10p gold 0.86 Claude 0.77 c=0.86; 1-10 English 8m/8p gold 0.86 Claude 0.85 c=0.86; 1-10 Mathematics 7m/7p gold 0.90 Claude 0.88 c=0.90; NCEA1 6m/6p gold 0.88 Claude 0.94 c=0.88; ANZH 5m/5p gold 0.91 Claude 0.87 c=0.91; ConnectED 4m/4p gold 0.93 Claude 0.91 c=0.93; Leaving to Learn 3m/3p gold 0.64 Claude 0.87 c=0.64
- **AGH1004** AGH1004_6_0.html ↔ AGH1004.07.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **AGH1009** AGH1009_9_0.html ↔ AGH1009.09.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH103** ANZH103_1_0.html ↔ ANZH103_3_0.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: AGH1004, AGH1009, ANZH103, ANZH205, ANZH301, ANZH302, ANZH303, BLL141, BLL146, BLL151, BLL157, BLL167, BLL171, BLL176, BLL177, BLL224, BLL225, BLL226, BLL227, BLL231, BLL234, BLL236, BLL237, BLL250 …

### F33 · MISSING `footer:links=prev-lesson,next-lesson,home-nav` — CANDIDATE (pages 68 / modules 65)
- by template+ptype: Standard/lesson 47m/47p gold 0.74 Claude 0.83 c=0.74; Bilingual/lesson 10m/10p gold 0.82 Claude 0.69 c=0.82; Standard/overview 5m/5p gold 0.03 Claude 0.05 c=0.03; Bilingual/overview 3m/3p gold 0.15 Claude 0.00 c=0.15; Inquiry/lesson 1m/1p gold 0.46 Claude 0.79 c=0.46; Fundamentals/lesson 1m/1p gold 0.69 Claude 0.89 c=0.69; Fundamentals/overview 1m/1p gold 0.05 Claude 0.20 c=0.05
- by subject: 1-10 Blended Literacy 17m/17p gold 0.42 Claude 0.41 c=0.42; NCEA1 11m/12p gold 0.74 Claude 0.82 c=0.74; Te Marautanga o Aotearoa TMoA 11m/13p gold 0.65 Claude 0.52 c=0.65; 1-10 English 7m/7p gold 0.64 Claude 0.72 c=0.64; ANZH 5m/5p gold 0.61 Claude 0.74 c=0.61; Leaving to Learn 4m/4p gold 0.47 Claude 0.62 c=0.47; 1-10 Mathematics 3m/3p gold 0.62 Claude 0.77 c=0.62; ConnectED 2m/2p gold 0.64 Claude 0.80 c=0.64
- **AGH1004** AGH1004_6_0.html ↔ AGH1004.07.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **AGH1009** AGH1009_9_0.html ↔ AGH1009.09.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH103** ANZH103_1_0.html ↔ ANZH103_3_0.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: AGH1004, AGH1009, ANZH103, ANZH205, ANZH301, ANZH302, ANZH303, ART1005, BLL141, BLL146, BLL151, BLL157, BLL167, BLL171, BLL224, BLL225, BLL226, BLL227, BLL231, BLL234, BLL236, BLL237, BLL266, BLL274 …

### F35 · MISSING `footer:links=home-nav,prev-lesson,next-lesson` — CANDIDATE (pages 122 / modules 57)
- by template+ptype: Inquiry/overview 27m/27p gold 0.55 Claude 0.04 c=0.55; Fundamentals/overview 12m/12p gold 0.15 Claude 0.00 c=0.15; Standard/lesson 11m/76p gold 0.04 Claude 0.00 c=0.04; Inquiry/lesson 7m/7p gold 0.12 Claude 0.00 c=0.12
- by subject: ConnectED 17m/17p gold 0.17 Claude 0.02 c=0.17; 1-10 Health and PE 12m/12p gold 0.33 Claude 0.00 c=0.33; 1-10 Blended Literacy 8m/8p gold 0.02 Claude 0.00 c=0.02; Te ara Whakapuawa -Wellbeing 8m/8p gold 0.61 Claude 0.00 c=0.61; 1-10 English 5m/32p gold 0.09 Claude 0.00 c=0.09; 1-10 Mathematics 5m/40p gold 0.12 Claude 0.00 c=0.12; EXPlore 1m/1p gold 0.07 Claude 0.00 c=0.07; Online Safety (OS9000) 1m/4p gold 0.03 Claude 0.00 c=0.03
- **BLL170** BLL170_0_0.html ↔ BLL170.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=home-nav,prev-lesson,next-lesson', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL210** BLL210_0_0.html ↔ BLL210.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=home-nav,prev-lesson,next-lesson', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL220** BLL220_0_0.html ↔ BLL220.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=home-nav,prev-lesson,next-lesson', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL170, BLL210, BLL220, BLL230, BLL240, BLL250, BLL260, BLL270, CEDK101, CEDK102, CEDK401, CEDK501, CEDO102, CEDO201, CEDO202, CEDO204, CEDO402, CEDR101, CEDR204, CEDT102, CEDT104, CEDT207, CEDT208, CEDT301 …

### F36 · EXTRA `footer:link=prev-lesson` — CANDIDATE (pages 60 / modules 43)
- by template+ptype: Standard/lesson 19m/24p gold 0.98 Claude 0.98 c=0.02; Standard/overview 12m/12p gold 0.03 Claude 0.05 c=0.97; Inquiry/lesson 5m/8p gold 0.86 Claude 1.00 c=0.14; Inquiry/overview 4m/4p gold 0.72 Claude 0.68 c=0.28; Fundamentals/overview 1m/1p gold 0.20 Claude 0.20 c=0.80; Fundamentals/lesson 1m/9p gold 0.75 Claude 1.00 c=0.25; Bilingual/lesson 1m/2p gold 0.97 Claude 1.00 c=0.03
- by subject: NCEA1 17m/21p gold 0.86 Claude 0.89 c=0.14; 1-10 Blended Literacy 10m/10p gold 0.68 Claude 0.71 c=0.32; ConnectED 3m/3p gold 0.91 Claude 0.90 c=0.09; EXPlore 3m/3p gold 0.73 Claude 0.93 c=0.27; 1-10 Mathematics 2m/2p gold 0.88 Claude 0.88 c=0.12; Leaving to Learn 2m/6p gold 0.78 Claude 0.75 c=0.22; ANZH 1m/1p gold 0.86 Claude 0.87 c=0.14; 1-10 English 1m/1p gold 0.84 Claude 0.85 c=0.15
- **ANZHFUN05** ANZHFUN05_0_0.html ↔ ANZHFUN05_0_0.html: gold ['footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav fundamentals-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav fundamentals-nav']
- **BLL120** BLL120_0_0.html ↔ BLL120.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL140** BLL140_0_0.html ↔ BLL140.html: gold ['footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: ANZHFUN05, BLL120, BLL140, BLL150, BLL175, BLL176, BLL177, BLL240, BLL271, BLLR202, BLLR203, CBI1005, CBI1008, CBI1009, CEDK501, CEDR401, CEDT207, CHI1003, CHI1004, CHI1005, COM1005, ENGFUN02, ENGR102, EXBP901 …

### F37 · MISSING `footer:link=prev-lesson` — CANDIDATE (pages 31 / modules 30)
- by template+ptype: Standard/lesson 14m/14p gold 0.98 Claude 0.98 c=0.98; Standard/overview 7m/7p gold 0.03 Claude 0.05 c=0.03; Inquiry/overview 6m/6p gold 0.72 Claude 0.68 c=0.72; Bilingual/overview 3m/3p gold 0.15 Claude 0.00 c=0.15; Fundamentals/overview 1m/1p gold 0.20 Claude 0.20 c=0.20
- by subject: Leaving to Learn 13m/13p gold 0.78 Claude 0.75 c=0.78; NCEA1 6m/7p gold 0.86 Claude 0.89 c=0.86; ConnectED 4m/4p gold 0.91 Claude 0.90 c=0.91; Te Marautanga o Aotearoa TMoA 3m/3p gold 0.77 Claude 0.75 c=0.77; Te ara Whakapuawa -Wellbeing 2m/2p gold 0.61 Claude 0.54 c=0.61; 1-10 Mathematics 1m/1p gold 0.88 Claude 0.88 c=0.88; 1-10 Social Science 1m/1p gold 0.77 Claude 0.77 c=0.77
- **ART1004** ART1004_0_0.html ↔ ART1004_4.0.html: gold ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ART1005** ART1005_0_0.html ↔ ART1005_3.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **CEDT102** CEDT102_0_0.html ↔ CEDT102.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=home-nav,prev-lesson,next-lesson', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: ART1004, ART1005, CEDT102, CEDT104, CEDT207, CEDT208, COM1002, ENG1004, GER1002, MXFL101, PES1002, SSFUN02, TRR112, TRR113, TRR116, TWHK902, TWHK907, XGF9001, XOTPB08, XOTPB09, XOTPB10, XOTPB11, XOTPB12, XOTPB13 …

### F38 · MISSING `footer:ul=footer-nav` — CANDIDATE (pages 87 / modules 29)
- by template+ptype: Standard/lesson 16m/46p gold 0.88 Claude 0.86 c=0.88; Standard/overview 12m/12p gold 0.74 Claude 0.70 c=0.74; Fundamentals/overview 9m/9p gold 0.48 Claude 0.46 c=0.48; Inquiry/overview 3m/3p gold 0.13 Claude 0.15 c=0.13; Inquiry/lesson 3m/17p gold 0.84 Claude 0.55 c=0.84
- by subject: 1-10 Blended Literacy 13m/44p gold 0.14 Claude 0.00 c=0.14; 1-10 Technology 5m/5p gold 0.88 Claude 0.68 c=0.88; ConnectED 4m/21p gold 0.81 Claude 0.67 c=0.81; EXPlore 2m/5p gold 0.53 Claude 0.27 c=0.53; 1-10 Mathematics 2m/2p gold 0.98 Claude 0.99 c=0.98; 1-10 Health and PE 1m/1p gold 0.69 Claude 0.67 c=0.69; NCEA1 1m/8p gold 1.00 Claude 0.98 c=1.00; 1-10 Writing (MiW) 1m/1p gold 0.62 Claude 0.71 c=0.62
- **BLL121** BLL121_0_0.html ↔ BLL121-01.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL172** BLL172_0_0.html ↔ BLL172-00.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL174** BLL174_0_0.html ↔ BLL174-00.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL121, BLL172, BLL174, BLL175, BLL176, BLL177, BLL236, BLL237, BLL240, BLL241, BLL243, BLL244, BLL245, CEDR501, CEDT207, CEDT301, CEDW101, EXBP901, EXIP901, HPFUN301, MXFUN02, MXFUN03, MXS1004, TEFUN01 …

### F40 · EXTRA `footer:ul=footer-nav inquiry-nav` — CANDIDATE (pages 78 / modules 22)
- by template+ptype: Standard/lesson 16m/43p gold 0.12 Claude 0.14 c=0.88; Standard/overview 13m/13p gold 0.26 Claude 0.29 c=0.74; Inquiry/overview 3m/3p gold 0.87 Claude 0.85 c=0.13; Inquiry/lesson 3m/17p gold 0.16 Claude 0.45 c=0.84; Fundamentals/overview 2m/2p gold 0.00 Claude 0.03 c=1.00
- by subject: 1-10 Blended Literacy 13m/44p gold 0.86 Claude 1.00 c=0.14; ConnectED 4m/21p gold 0.19 Claude 0.33 c=0.81; EXPlore 2m/5p gold 0.47 Claude 0.73 c=0.53; 1-10 Mathematics 2m/2p gold 0.02 Claude 0.01 c=0.98; Leaving to Learn 1m/6p gold 0.12 Claude 0.14 c=0.88
- **BLL121** BLL121_0_0.html ↔ BLL121-01.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL172** BLL172_0_0.html ↔ BLL172-00.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL174** BLL174_0_0.html ↔ BLL174-00.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL121, BLL172, BLL174, BLL175, BLL176, BLL177, BLL236, BLL237, BLL240, BLL241, BLL243, BLL244, BLL245, CEDR501, CEDT207, CEDT301, CEDW101, EXBP901, EXIP901, MXFUN02, MXFUN03, XWHA02

### F41 · MISSING `footer:links=next-lesson,home-nav` — CANDIDATE (pages 22 / modules 22)
- by template+ptype: Standard/overview 11m/11p gold 0.77 Claude 0.95 c=0.77; Standard/lesson 8m/8p gold 0.01 Claude 0.01 c=0.01; Inquiry/lesson 2m/2p gold 0.04 Claude 0.00 c=0.04; Inquiry/overview 1m/1p gold 0.02 Claude 0.17 c=0.02
- by subject: NCEA1 13m/13p gold 0.11 Claude 0.11 c=0.11; 1-10 Blended Literacy 6m/6p gold 0.29 Claude 0.29 c=0.29; ConnectED 2m/2p gold 0.06 Claude 0.10 c=0.06; 1-10 English 1m/1p gold 0.11 Claude 0.13 c=0.11
- **BLL175** BLL175_1_1.html ↔ BLL175-02.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL176** BLL176_1_1.html ↔ BLL176-2.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL177** BLL177_2_0.html ↔ BLL177-2.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL175, BLL176, BLL177, BLL240, BLLR202, BLLR203, CBI1005, CBI1008, CBI1009, CEDK501, CEDT207, CHI1003, CHI1004, CHI1005, ENGR102, GEO1004, GEO1005, GEO1006, HES1006, JPN1004, MXS1004, PES1005


## The ranked queue — chrome regions first, then by modules affected

| # | region | dir | parent | gold form | Claude form | pages | modules | consensus (all) | best group | derivable | KB | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | module-code | EXTRA | `div#header` | `—` | `div#module-code` | 6 | 6 | 0.03 of 2491 | — | structure | yes | BELOW FLOOR |
| 2 | module-code | MISSING | `div#header` | `div#module-code` | `—` | 5 | 5 | 0.97 of 2491 | — | structure | yes | BELOW FLOOR |
| 3 | module-code | EXTRA | `div#module-code` | `—` | `h1` | 2 | 2 | 0.03 of 2491 | — | structure | yes | BELOW FLOOR |
| 4 | title | MISSING | `div#header` | `h1>span` | `—` | 275 | 134 | 0.24 of 2491 | subject+ptype=Online Safety (OS9000)/overview c=0.93 n=12 | 0.76 | yes | CANDIDATE |
| 5 | title | EXTRA | `div#header` | `—` | `h1>span` | 22 | 21 | 0.76 of 2491 | template=Standard c=0.81 n=16 | structure | yes | CANDIDATE |
| 6 | title | MISSING | `span>span` | `span` | `—` | 10 | 6 | 0.01 of 2491 | — | 1.00 | — | BELOW FLOOR |
| 7 | title | MISSING | `span>span.sassoonI-text` | `span.sassoonI-text` | `—` | 14 | 4 | 0.01 of 2491 | — | 0.79 | — | BELOW FLOOR |
| 8 | title | SUBSTITUTED | `div#header` | `h1>span` | `div#module-head-buttons` | 4 | 4 | 1.00 of 2491 | — | structure | yes | BELOW FLOOR |
| 9 | title | MISSING | `div#header` | `h1>span.ch-text` | `—` | 14 | 2 | 0.01 of 2491 | — | 0.00 | yes | BELOW FLOOR |
| 10 | title | SUBSTITUTED | `div#header` | `h1>span` | `div#module-code` | 2 | 2 | 1.00 of 2491 | — | structure | yes | BELOW FLOOR |
| 11 | title | SUBSTITUTED | `span` | `apan.jp-text` | `span.jp-text` | 10 | 1 | 0.00 of 2491 | — | structure | yes | BELOW FLOOR |
| 12 | title | SUBSTITUTED | `h1>span.ch-text` | `span.ch-text` | `span` | 7 | 1 | 0.01 of 2491 | — | structure | yes | BELOW FLOOR |
| 13 | title | MISSING | `div.titlebar` | `h1.moduleTitle>span.module-subtitle.text-lowercase` | `—` | 2 | 1 | 0.00 of 2491 | — | 1.00 | — | BELOW FLOOR |
| 14 | title | EXTRA | `span>span` | `—` | `span` | 1 | 1 | 0.99 of 2491 | — | structure | — | BELOW FLOOR |
| 15 | title | EXTRA | `span>span.ch-text` | `—` | `span.ch-text` | 1 | 1 | 1.00 of 2491 | — | structure | yes | BELOW FLOOR |
| 16 | title | EXTRA | `span>span.jp-text` | `—` | `span.jp-text` | 1 | 1 | 1.00 of 2491 | — | structure | yes | BELOW FLOOR |
| 17 | title | EXTRA | `h1>span` | `—` | `span` | 1 | 1 | 0.01 of 2491 | — | structure | — | BELOW FLOOR |
| 18 | title | EXTRA | `msub` | `—` | `mrow` | 1 | 1 | 1.00 of 2491 | — | structure | — | BELOW FLOOR |
| 19 | title | EXTRA | `mfrac` | `—` | `mrow` | 1 | 1 | 1.00 of 2491 | — | structure | — | BELOW FLOOR |
| 20 | title | EXTRA | `mrow` | `—` | `mi` | 1 | 1 | 1.00 of 2491 | — | structure | — | BELOW FLOOR |
| 21 | title | EXTRA | `msup` | `—` | `mrow` | 1 | 1 | 1.00 of 2491 | — | structure | — | BELOW FLOOR |
| 22 | title | MISSING | `span>span.ch-text` | `span.ch-text` | `—` | 1 | 1 | 0.00 of 2491 | — | 0.00 | yes | BELOW FLOOR |
| 23 | title | MISSING | `span>span.text-lowercase` | `span.text-lowercase` | `—` | 1 | 1 | 0.00 of 2491 | — | 1.00 | — | BELOW FLOOR |
| 24 | title | MISSING | `h1>span.jp-text` | `span.jp-text` | `—` | 1 | 1 | 0.00 of 2491 | — | 1.00 | yes | BELOW FLOOR |
| 25 | title | MISSING | `msup` | `mn` | `—` | 1 | 1 | 0.00 of 2491 | — | 1.00 | — | BELOW FLOOR |
| 26 | title | MISSING | `h1>span` | `span` | `—` | 1 | 1 | 0.98 of 2491 | — | 1.00 | — | BELOW FLOOR |
| 27 | title | SUBSTITUTED | `msub` | `mi` | `mrow` | 1 | 1 | 0.00 of 2491 | — | structure | — | BELOW FLOOR |
| 28 | title | SUBSTITUTED | `msub` | `mi` | `mi` | 1 | 1 | 0.00 of 2491 | — | structure | — | BELOW FLOOR |
| 29 | title | SUBSTITUTED | `mfrac` | `mn` | `mrow` | 1 | 1 | 0.00 of 2491 | — | structure | — | BELOW FLOOR |
| 30 | title | SUBSTITUTED | `mfrac` | `mn` | `mn` | 1 | 1 | 0.00 of 2491 | — | structure | — | BELOW FLOOR |
| 31 | title | SUBSTITUTED | `msup` | `mi` | `mrow` | 1 | 1 | 0.00 of 2491 | — | structure | — | BELOW FLOOR |
| 32 | header | MISSING | `div#header` | `p` | `—` | 3 | 1 | 0.00 of 2491 | — | 0.00 | yes | BELOW FLOOR |
| 33 | header | SUBSTITUTED | `div#header` | `div.titlebar` | `h1>span` | 2 | 1 | 0.00 of 2491 | — | structure | yes | BELOW FLOOR |
| 34 | header | SUBSTITUTED | `div#header` | `div#header` | `div#module-code` | 1 | 1 | 0.00 of 2491 | — | structure | yes | BELOW FLOOR |
| 35 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `p` | `h5` | 84 | 84 | 0.06 of 2491 | subject+ptype=1-10 Health and PE/overview c=0.82 n=14 | structure | yes | CANDIDATE |
| 36 | module-menu | MISSING | `ul` | `li` | `—` | 132 | 82 | 0.10 of 2491 | — | 0.85 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 37 | module-menu | MISSING | `div.col-12.col-md-8` | `ul` | `—` | 215 | 55 | 0.29 of 2491 | subject+ptype=1-10 English/lesson c=0.72 n=11 | 0.92 | — | CANDIDATE |
| 38 | module-menu | MISSING | `div.col-12.col-md-8` | `h5` | `—` | 213 | 47 | 0.24 of 2491 | subject+ptype=1-10 English/lesson c=0.64 n=12 | 0.84 | — | CANDIDATE |
| 39 | module-menu | MISSING | `div.col-12.col-md-8` | `p` | `—` | 211 | 46 | 0.09 of 2491 | — | 0.83 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 40 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-6.paddingR` | 65 | 45 | 0.97 of 2491 | template=Standard c=0.97 n=38 | structure | yes | CANDIDATE |
| 41 | module-menu | EXTRA | `ul` | `—` | `li` | 81 | 43 | 0.78 of 2491 | ptype=lesson c=0.82 n=14 | structure | — | CANDIDATE |
| 42 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingL` | `p` | `h5` | 42 | 42 | 0.03 of 2491 | subject+ptype=1-10 Health and PE/overview c=0.82 n=14 | structure | yes | CANDIDATE |
| 43 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `p` | `—` | 51 | 37 | 0.04 of 2491 | subject+ptype=1-10 Blended Literacy/overview c=0.65 n=23 | 0.73 | yes | CANDIDATE |
| 44 | module-menu | EXTRA | `div#header` | `—` | `div#module-menu-content.moduleMenu` | 64 | 36 | 0.25 of 2491 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 45 | module-menu | EXTRA | `div#header` | `—` | `div#module-head-buttons` | 54 | 30 | 0.23 of 2491 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 46 | module-menu | MOVED | `ul` | `li` | `li>i` | 75 | 29 | 0.28 of 2491 | — | structure | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 47 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `h5` | 81 | 25 | 0.76 of 2491 | era=Refresh c=0.76 n=25 | structure | — | CANDIDATE |
| 48 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 55 | 25 | 0.88 of 2491 | era=Refresh c=0.88 n=25 | structure | — | CANDIDATE |
| 49 | module-menu | MISSING | `div#header` | `div#module-head-buttons` | `—` | 46 | 25 | 0.77 of 2491 | template=Standard c=0.78 n=12 | structure | yes | CANDIDATE |
| 50 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `ul` | `—` | 35 | 24 | 0.05 of 2491 | — | 0.81 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 51 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6.paddingL` | `—` | 42 | 23 | 0.04 of 2491 | — | 1.00 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 52 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `p>b` | 22 | 22 | 1.00 of 2491 | era=Refresh c=1.00 n=22 | structure | yes | CANDIDATE |
| 53 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6.offset-md-0` | `—` | 88 | 21 | 0.05 of 2491 | — | 0.88 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 54 | module-menu | SUBSTITUTED | `ul` | `li` | `li` | 88 | 21 | 0.57 of 2491 | template+ptype=Standard/lesson c=0.64 n=16 | structure | — | CANDIDATE |
| 55 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `p` | `h5` | 27 | 21 | 0.04 of 2491 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 56 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `h4>span` | `—` | 21 | 21 | 0.02 of 2491 | — | 1.00 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 57 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `—` | 96 | 20 | 0.02 of 2491 | — | 0.96 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 58 | module-menu | MISSING | `p` | `br` | `—` | 35 | 20 | 0.01 of 2491 | — | structure | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 59 | module-menu | EXTRA | `div.col-12.col-md-6.offset-md-0` | `—` | `p` | 24 | 18 | 0.99 of 2491 | era=Refresh c=0.99 n=18 | structure | yes | CANDIDATE |
| 60 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `p` | 18 | 18 | 0.96 of 2491 | template=Standard c=0.96 n=14 | structure | yes | CANDIDATE |
| 61 | module-menu | SUBSTITUTED | `div#module-menu-content.moduleMenu` | `WIDGET` | `div.row` | 18 | 18 | 0.01 of 2491 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 62 | module-menu | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `h5` | 62 | 17 | 0.12 of 2491 | — | structure | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 63 | module-menu | EXTRA | `div.row` | `—` | `WIDGET` | 17 | 17 | 0.88 of 2491 | subject=1-10 Blended Literacy c=0.97 n=13 | structure | — | CANDIDATE |
| 64 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `ul` | 43 | 16 | 0.71 of 2491 | era=Refresh c=0.71 n=16 | structure | — | CANDIDATE |
| 65 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-8` | 97 | 15 | 0.67 of 2491 | subject=1-10 Mathematics c=0.77 n=12 | structure | — | CANDIDATE |
| 66 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0` | `ul` | `—` | 79 | 15 | 0.02 of 2491 | — | 0.90 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 67 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-6.offset-md-0` | 31 | 15 | 0.95 of 2491 | era=Refresh c=0.95 n=15 | structure | yes | CANDIDATE |
| 68 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `h4>span` | `h5>span` | 15 | 15 | 0.03 of 2491 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 69 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-12.paddingR` | 16 | 14 | 0.96 of 2491 | template=Standard c=0.96 n=14 | structure | yes | CANDIDATE |
| 70 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `ul` | `p>b` | 14 | 14 | 0.06 of 2491 | subject+ptype=1-10 Blended Literacy/overview c=0.72 n=14 | structure | yes | CANDIDATE |
| 71 | module-menu | MISSING | `div#module-menu-content.moduleMenu` | `ul` | `—` | 88 | 13 | 0.04 of 2491 | — | 0.91 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 72 | module-menu | SUBSTITUTED | `div#module-menu-content.moduleMenu` | `h5` | `div.row` | 82 | 13 | 0.03 of 2491 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 73 | module-menu | EXTRA | `div.col-12.col-md-6.paddingL` | `—` | `h5` | 13 | 13 | 1.00 of 2491 | era=Refresh c=1.00 n=13 | structure | yes | CANDIDATE |
| 74 | module-menu | SUBSTITUTED | `div#module-menu-content.moduleMenu` | `div.item` | `div.row` | 82 | 12 | 0.03 of 2491 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 75 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.offset-md-0` | `div.col-12.col-md-8` | 75 | 12 | 0.05 of 2491 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 76 | module-menu | MISSING | `div.item` | `p>b` | `—` | 23 | 12 | 0.01 of 2491 | — | 0.58 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 77 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `h5` | 19 | 12 | 0.04 of 2491 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 78 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `h5` | 14 | 12 | 0.99 of 2491 | ptype=overview c=1.00 n=10 | structure | yes | CANDIDATE |
| 79 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6.offset-md-0.paddingL` | `—` | 12 | 12 | 0.01 of 2491 | — | 0.42 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 80 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.paddingR` | `div.col-12.col-md-12.paddingR` | 12 | 12 | 0.07 of 2491 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 81 | module-menu | EXTRA | `li>b` | `—` | `b` | 24 | 11 | 1.00 of 2491 | ptype=lesson c=1.00 n=10 | structure | — | CANDIDATE |
| 82 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.paddingL` | `div.col-12.col-md-6.paddingR` | 11 | 11 | 0.04 of 2491 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 83 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0` | `p` | `—` | 49 | 10 | 0.02 of 2491 | — | 0.72 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 84 | module-menu | MISSING | `div.item` | `ul` | `—` | 40 | 10 | 0.01 of 2491 | — | 1.00 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 85 | module-menu | EXTRA | `div.col-12.col-md-6.paddingL` | `—` | `p` | 10 | 10 | 1.00 of 2491 | template=Inquiry c=1.00 n=10 | structure | yes | CANDIDATE |
| 86 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-8.paddingR` | `div.col-12.col-md-8` | 70 | 9 | 0.03 of 2491 | — | structure | yes | BELOW FLOOR |
| 87 | module-menu | MISSING | `div.col-12.col-md-8.paddingR` | `ul` | `—` | 48 | 9 | 0.02 of 2491 | — | 0.99 | yes | BELOW FLOOR |
| 88 | module-menu | MISSING | `div#module-menu-content.moduleMenu` | `h5` | `—` | 45 | 9 | 0.03 of 2491 | — | 0.71 | yes | BELOW FLOOR |
| 89 | module-menu | MISSING | `div#header` | `div#module-menu-content.moduleMenu` | `—` | 10 | 9 | 0.75 of 2491 | — | 1.00 | yes | BELOW FLOOR |
| 90 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `h5>span` | 9 | 9 | 0.97 of 2491 | — | structure | yes | BELOW FLOOR |
| 91 | module-menu | EXTRA | `p>b` | `—` | `b` | 9 | 9 | 0.98 of 2491 | — | structure | — | BELOW FLOOR |
| 92 | module-menu | EXTRA | `div.col-12.col-md-6.paddingL` | `—` | `ul` | 9 | 9 | 0.99 of 2491 | — | structure | yes | BELOW FLOOR |
| 93 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `h5>span` | `—` | 9 | 9 | 0.03 of 2491 | — | 1.00 | yes | BELOW FLOOR |
| 94 | module-menu | MISSING | `h5>span` | `span` | `—` | 9 | 9 | 0.03 of 2491 | — | 1.00 | — | BELOW FLOOR |
| 95 | module-menu | SUBSTITUTED | `div.col-12.col-md-6` | `h4>span` | `h5>span` | 9 | 9 | 0.01 of 2491 | — | structure | yes | BELOW FLOOR |
| 96 | module-menu | MOVED | `ul` | `li` | `li` | 36 | 8 | 0.36 of 2491 | — | structure | — | BELOW FLOOR |
| 97 | module-menu | MISSING | `div.item` | `p` | `—` | 18 | 8 | 0.01 of 2491 | — | 0.77 | yes | BELOW FLOOR |
| 98 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6.paddingR` | `—` | 12 | 8 | 0.07 of 2491 | — | 1.00 | yes | BELOW FLOOR |
| 99 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `h4>span` | 11 | 8 | 0.04 of 2491 | — | structure | yes | BELOW FLOOR |
| 100 | module-menu | SUBSTITUTED | `div.row` | `WIDGET` | `div.col-12.col-md-8` | 9 | 8 | 0.12 of 2491 | — | structure | — | BELOW FLOOR |
| 438 | crumbs | MISSING | `div.crumbs` | `div` | `—` | 23 | 20 | 0.02 of 2484 | template+ptype=Inquiry/overview c=0.60 n=11 | 0.97 | yes | CANDIDATE |
| 480 | footer | MISSING | `ul.footer-nav` | `li>a#next-lesson` | `—` | 97 | 60 | 0.71 of 2491 | subject+ptype=1-10 Mathematics/overview c=0.93 n=12 | structure | yes | CANDIDATE |
| 481 | footer | MISSING | `ul.footer-nav` | `li>a.home-nav` | `—` | 100 | 57 | 0.83 of 2491 | subject=1-10 English c=1.00 n=13 | structure | yes | CANDIDATE |
| 482 | footer | MISSING | `li>a#next-lesson` | `a#next-lesson` | `—` | 52 | 52 | 0.82 of 2491 | template=Bilingual c=0.86 n=10 | structure | yes | CANDIDATE |
| 483 | footer | MISSING | `ul.footer-nav.inquiry-nav` | `li>a.home-nav` | `—` | 53 | 48 | 0.14 of 2491 | subject+ptype=1-10 Blended Literacy/overview c=0.88 n=20 | structure | yes | CANDIDATE |
| 486 | footer | EXTRA | `ul.footer-nav.inquiry-nav` | `—` | `li>a.home-nav` | 26 | 26 | 0.85 of 2491 | era=Refresh c=0.85 n=26 | structure | yes | CANDIDATE |
| 488 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav.inquiry-nav` | `li>a#next-lesson` | 22 | 22 | 0.14 of 2491 | subject+ptype=1-10 Blended Literacy/overview c=0.88 n=15 | structure | yes | CANDIDATE |
| 489 | footer | MISSING | `ul.footer-nav` | `li>a#prev-lesson` | `—` | 37 | 20 | 0.70 of 2491 | template+ptype=Standard/lesson c=0.87 n=14 | structure | yes | CANDIDATE |
| 490 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav` | `ul.footer-nav.inquiry-nav` | 67 | 19 | 0.82 of 2491 | template+ptype=Standard/lesson c=0.87 n=13 | structure | yes | CANDIDATE |
| 491 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` | `li>a#next-lesson` | `li>a.home-nav` | 18 | 18 | 0.11 of 2491 | subject+ptype=1-10 Blended Literacy/overview c=0.85 n=15 | structure | yes | CANDIDATE |
| 492 | footer | MISSING | `li>a.home-nav` | `a.home-nav` | `—` | 28 | 17 | 1.00 of 2491 | era=Refresh c=1.00 n=17 | structure | yes | CANDIDATE |
| 493 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav` | `ul.footer-nav` | 18 | 17 | 0.82 of 2491 | template+ptype=Standard/lesson c=0.87 n=10 | structure | yes | CANDIDATE |
| 494 | footer | EXTRA | `div#footer` | `—` | `ul.footer-nav.inquiry-nav` | 18 | 16 | 0.85 of 2491 | template=Standard c=0.86 n=13 | structure | yes | CANDIDATE |
| 496 | footer | MISSING | `ul.footer-nav.inquiry-nav` | `li>a#prev-lesson` | `—` | 15 | 15 | 0.10 of 2491 | template+ptype=Inquiry/overview c=0.70 n=10 | structure | yes | CANDIDATE |
| 498 | footer | SUBSTITUTED | `ul.footer-nav` | `li>a#next-lesson` | `li>a#next-lesson` | 14 | 13 | 0.71 of 2491 | ptype=lesson c=0.74 n=11 | structure | yes | CANDIDATE |
| 499 | footer | EXTRA | `ul.footer-nav.fundamentals-nav` | `—` | `li>a.home-nav` | 21 | 12 | 0.98 of 2491 | era=Refresh c=0.98 n=12 | structure | yes | CANDIDATE |
| 502 | footer | SUBSTITUTED | `ul.footer-nav` | `li>a.home-nav` | `li>a.home-nav` | 13 | 11 | 0.83 of 2491 | era=Refresh c=0.83 n=11 | structure | yes | CANDIDATE |
| 504 | footer | MISSING | `div#footer` | `ul.footer-nav` | `—` | 10 | 10 | 0.82 of 2491 | era=Refresh c=0.82 n=10 | structure | yes | CANDIDATE |
| 592 | acks | SUBSTITUTED | `div.col-12.col-md-8` | `div.acks` | `div.acks.acksTemplate` | 99 | 99 | 0.15 of 2491 | template+ptype=Inquiry/overview c=0.81 n=35 | structure | yes | CANDIDATE |
| 622 | activity | MISSING | `div.col-12` | `p` | `—` | 764 | 367 | 0.30 of 2484 | template+ptype=Inquiry/overview c=0.76 n=26 | 0.81 | — | CANDIDATE |
| 623 | activity | EXTRA | `div.col-12` | `—` | `p` | 593 | 298 | 0.87 of 2484 | subject=ANZH c=0.99 n=32 | structure | — | CANDIDATE |
| 626 | activity | MISSING | `div.col-12` | `a` | `—` | 442 | 224 | 0.29 of 2484 | series=HIS10 c=0.71 n=40 | 0.63 | — | CANDIDATE |
| 627 | activity | EXTRA | `div.col-12` | `—` | `WIDGET` | 349 | 214 | 0.82 of 2484 | subject=NCEA1 c=0.94 n=35 | structure | — | CANDIDATE |
| 628 | activity | MOVED | `div.col-12` | `p` | `p` | 315 | 211 | 0.19 of 2484 | template+ptype=Bilingual/lesson c=0.64 n=20 | structure | — | CANDIDATE |
| 629 | activity | MISSING | `div.col-12` | `h3` | `—` | 384 | 193 | 0.43 of 2484 | template+ptype=Fundamentals/overview c=0.88 n=30 | 0.69 | — | CANDIDATE |
| 630 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `div.activity[number=*]` | 271 | 186 | 0.44 of 2484 | subject+ptype=1-10 Blended Literacy/lesson c=0.73 n=66 | structure | yes | CANDIDATE |
| 632 | activity | MISSING | `div.activity.interactive[number=*]` | `div.row` | `—` | 284 | 162 | 0.12 of 2484 | template+ptype=Fundamentals/overview c=0.65 n=35 | 0.93 | yes | CANDIDATE |
| 633 | activity | EXTRA | `div.col-12` | `—` | `img.img-fluid` | 249 | 153 | 0.97 of 2484 | subject+ptype=1-10 English/lesson c=0.99 n=22 | structure | — | CANDIDATE |
| 634 | activity | MOVED | `div.col-12` | `p` | `p` | 166 | 135 | 0.15 of 2484 | template+ptype=Inquiry/overview c=0.72 n=26 | structure | — | CANDIDATE |
| 635 | activity | EXTRA | `div.row` | `—` | `div.col-12` | 168 | 126 | 0.90 of 2484 | template=Standard c=0.93 n=132 | structure | — | CANDIDATE |
| 638 | activity | EXTRA | `div.col-12` | `—` | `p>a` | 130 | 106 | 1.00 of 2484 | subject+ptype=1-10 Blended Literacy/lesson c=1.00 n=37 | structure | — | CANDIDATE |
| 639 | activity | EXTRA | `div.activity[number=*]` | `—` | `div.row` | 148 | 105 | 0.94 of 2484 | subject=1-10 English c=0.98 n=23 | structure | yes | CANDIDATE |
| 643 | activity | SUBSTITUTED | `div.col-12` | `p` | `p` | 131 | 98 | 0.75 of 2484 | subject+ptype=1-10 Blended Literacy/lesson c=0.93 n=22 | structure | — | CANDIDATE |
| 646 | activity | EXTRA | `div.col-12` | `—` | `ol` | 132 | 85 | 0.96 of 2484 | subject=1-10 Mathematics c=0.98 n=31 | structure | — | CANDIDATE |
| 647 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `div.activity.interactive[number=*]` | 117 | 85 | 0.47 of 2484 | subject+ptype=1-10 Blended Literacy/lesson c=0.81 n=24 | structure | yes | CANDIDATE |
| 648 | activity | EXTRA | `div.col-12` | `—` | `h3` | 106 | 85 | 0.86 of 2484 | template=Standard c=0.92 n=68 | structure | — | CANDIDATE |
| 649 | activity | EXTRA | `div.col-12` | `—` | `p>b` | 126 | 84 | 0.97 of 2484 | template=Standard c=0.98 n=94 | structure | — | CANDIDATE |
| 650 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `div.activity[number=*]` | 115 | 83 | 0.47 of 2484 | subject+ptype=1-10 Mathematics/lesson c=0.68 n=23 | structure | yes | CANDIDATE |
| 653 | activity | EXTRA | `p>b` | `—` | `b` | 106 | 81 | 0.92 of 2484 | template=Standard c=0.94 n=70 | structure | — | CANDIDATE |
| 655 | activity | EXTRA | `div.col-12` | `—` | `ul` | 103 | 79 | 0.93 of 2484 | template=Standard c=0.96 n=85 | structure | — | CANDIDATE |
| 657 | activity | EXTRA | `div.activity.interactive[number=*]` | `—` | `div.row` | 89 | 75 | 0.65 of 2484 | template=Standard c=0.68 n=73 | structure | yes | CANDIDATE |
| 659 | activity | MOVED | `div.col-12` | `h3` | `h3` | 104 | 74 | 0.14 of 2484 | template+ptype=Bilingual/lesson c=0.75 n=21 | structure | — | CANDIDATE |
| 660 | activity | EXTRA | `p>a` | `—` | `a` | 86 | 72 | 0.98 of 2484 | subject+ptype=1-10 Blended Literacy/lesson c=1.00 n=32 | structure | — | CANDIDATE |
| 661 | activity | EXTRA | `div.col-12` | `—` | `a` | 95 | 71 | 0.71 of 2484 | template=Standard c=0.73 n=81 | structure | — | CANDIDATE |
| 663 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `div.activity.interactive[number=*]` | 94 | 69 | 0.44 of 2484 | subject+ptype=1-10 Mathematics/lesson c=0.65 n=21 | structure | yes | CANDIDATE |
| 664 | activity | EXTRA | `a` | `—` | `div.button` | 90 | 69 | 0.77 of 2484 | ptype=overview c=0.87 n=20 | structure | yes | CANDIDATE |
| 665 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `p` | 82 | 67 | 0.59 of 2484 | subject+ptype=1-10 Mathematics/lesson c=0.78 n=31 | structure | — | CANDIDATE |
| 670 | activity | EXTRA | `div.col-12.col-md-8` | `—` | `div.activity[number=*]` | 71 | 61 | 0.95 of 2484 | template=Standard c=0.98 n=55 | structure | yes | CANDIDATE |
| 671 | activity | SUBSTITUTED | `div.col-12` | `p` | `WIDGET` | 71 | 60 | 0.75 of 2484 | template+ptype=Standard/lesson c=0.88 n=51 | structure | — | CANDIDATE |
| 675 | activity | EXTRA | `div.col-12` | `—` | `h4.goJournal` | 130 | 56 | 0.95 of 2484 | series=HIS10 c=1.00 n=32 | structure | — | CANDIDATE |
| 676 | activity | SUBSTITUTED | `div.col-12` | `a` | `h4.goJournal` | 118 | 55 | 0.55 of 2484 | series=HIS10 c=0.83 n=20 | structure | — | CANDIDATE |
| 678 | activity | EXTRA | `ol` | `—` | `li` | 70 | 54 | 0.96 of 2484 | template=Standard c=0.97 n=54 | structure | — | CANDIDATE |
| 679 | activity | SUBSTITUTED | `div.col-12` | `a` | `p` | 73 | 52 | 0.55 of 2484 | subject+ptype=1-10 Mathematics/lesson c=0.80 n=20 | structure | — | CANDIDATE |
| 680 | activity | EXTRA | `div.col-12` | `—` | `p>i` | 58 | 52 | 0.98 of 2484 | template=Standard c=0.98 n=48 | structure | — | CANDIDATE |
| 689 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `div.row` | 48 | 46 | 0.59 of 2484 | ptype=lesson c=0.69 n=38 | structure | — | CANDIDATE |
| 696 | activity | EXTRA | `a` | `—` | `div.externalButton` | 52 | 41 | 0.91 of 2484 | template=Standard c=0.92 n=36 | structure | — | CANDIDATE |
| 699 | activity | EXTRA | `p>i` | `—` | `i` | 48 | 40 | 0.89 of 2484 | template=Standard c=0.89 n=44 | structure | — | CANDIDATE |
| 709 | activity | EXTRA | `div.col-12` | `—` | `div.icon.ratio.ratio-16x9.videoSection` | 50 | 35 | 0.98 of 2484 | template=Standard c=0.98 n=42 | structure | yes | CANDIDATE |
| 710 | activity | SUBSTITUTED | `div.col-12` | `a` | `WIDGET` | 41 | 35 | 0.55 of 2484 | template+ptype=Standard/lesson c=0.65 n=37 | structure | — | CANDIDATE |
| 713 | activity | EXTRA | `p` | `—` | `b` | 42 | 34 | 0.96 of 2484 | template=Standard c=0.96 n=37 | structure | — | CANDIDATE |
| 716 | activity | SUBSTITUTED | `div.row` | `div.col-12` | `div.col-12.col-md-8` | 36 | 33 | 0.78 of 2484 | ptype=lesson c=0.92 n=26 | structure | — | CANDIDATE |
| 717 | activity | EXTRA | `div.col-12` | `—` | `audio.audioPlayer.icon` | 52 | 32 | 1.00 of 2484 | template=Bilingual c=1.00 n=24 | structure | yes | CANDIDATE |
| 718 | activity | EXTRA | `div.col-12.col-md-8` | `—` | `div.activity.interactive[number=*]` | 34 | 32 | 0.89 of 2484 | template=Standard c=0.92 n=26 | structure | yes | CANDIDATE |
| 721 | activity | SUBSTITUTED | `div.col-12` | `h3` | `WIDGET` | 38 | 31 | 0.76 of 2484 | template+ptype=Standard/lesson c=0.89 n=27 | structure | — | CANDIDATE |
| 724 | activity | EXTRA | `ul` | `—` | `li` | 32 | 31 | 0.93 of 2484 | template=Standard c=0.95 n=27 | structure | — | CANDIDATE |
| 733 | activity | SUBSTITUTED | `div.row` | `div.col-12` | `WIDGET` | 28 | 27 | 0.78 of 2484 | ptype=lesson c=0.92 n=21 | structure | — | CANDIDATE |
| 741 | activity | EXTRA | `div.icon.ratio.ratio-16x9.videoSection` | `—` | `iframe` | 28 | 24 | 0.99 of 2484 | template=Standard c=0.99 n=21 | structure | yes | CANDIDATE |
| 743 | activity | SUBSTITUTED | `div.activity.interactive[number=*]` | `div.row` | `WIDGET` | 27 | 24 | 0.55 of 2484 | ptype=lesson c=0.63 n=22 | structure | yes | CANDIDATE |
| 744 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `ol` | 26 | 24 | 0.59 of 2484 | ptype=lesson c=0.69 n=22 | structure | — | CANDIDATE |
| 745 | activity | EXTRA | `div.col-12` | `—` | `div.ratio.ratio-16x9.videoSection` | 37 | 23 | 0.95 of 2484 | template=Standard c=0.96 n=30 | structure | yes | CANDIDATE |
| 747 | activity | EXTRA | `div.col-12` | `—` | `h5` | 27 | 23 | 0.99 of 2484 | template=Standard c=0.99 n=22 | structure | — | CANDIDATE |
| 755 | activity | SUBSTITUTED | `div.row` | `div.col-12` | `div.row` | 23 | 22 | 0.78 of 2484 | era=Refresh c=0.78 n=23 | structure | — | CANDIDATE |
| 770 | activity | SUBSTITUTED | `div.col-12` | `h3` | `h3` | 27 | 19 | 0.76 of 2484 | template+ptype=Standard/lesson c=0.89 n=20 | structure | — | CANDIDATE |
| 773 | activity | EXTRA | `div.ratio.ratio-16x9.videoSection` | `—` | `iframe` | 23 | 19 | 0.97 of 2484 | era=Refresh c=0.97 n=23 | structure | yes | CANDIDATE |
| 777 | activity | SUBSTITUTED | `div.row` | `div.col-12` | `div.button` | 21 | 19 | 0.78 of 2484 | era=Refresh c=0.78 n=21 | structure | yes | CANDIDATE |
| 781 | activity | EXTRA | `div.col-12` | `—` | `div.button` | 29 | 18 | 1.00 of 2484 | template=Standard c=1.00 n=25 | structure | yes | CANDIDATE |
| 789 | activity | SUBSTITUTED | `div.col-12` | `p` | `p>b` | 23 | 17 | 0.75 of 2484 | era=Refresh c=0.75 n=23 | structure | — | CANDIDATE |
| 821 | activity | SUBSTITUTED | `div.col-12` | `p` | `h4.goJournal` | 22 | 13 | 0.75 of 2484 | template+ptype=Standard/lesson c=0.88 n=21 | structure | — | CANDIDATE |
| 919 | activity | MISSING | `div.col-12.col-md-8` | `div.activity.dropbox[number=*]` | `—` | 23 | 8 | 0.03 of 2484 | series=XDLS90 c=0.68 n=20 | 0.96 | yes | CANDIDATE |
| 1117 | activity | EXTRA | `div.activity.clickDropContent.dropbox[nu` | `—` | `a` | 23 | 4 | 1.00 of 2484 | era=Refresh c=1.00 n=23 | structure | yes | CANDIDATE |
| 1118 | activity | EXTRA | `div.activity.dropbox[number=*]` | `—` | `a` | 21 | 4 | 0.99 of 2484 | era=Refresh c=0.99 n=21 | structure | yes | CANDIDATE |
| 3980 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 1108 | 409 | 0.82 of 2484 | subject+ptype=1-10 Blended Literacy/lesson c=0.99 n=26 | structure | — | CANDIDATE |
| 3981 | body | EXTRA | `div#body` | `—` | `div.row` | 1457 | 404 | 0.73 of 2484 | subject+ptype=1-10 Blended Literacy/overview c=1.00 n=31 | structure | — | CANDIDATE |
| 3982 | body | MISSING | `div#body` | `div.row` | `—` | 1383 | 355 | 0.34 of 2484 | series=CEDO50 c=0.76 n=20 | 0.86 | — | CANDIDATE |
| 3983 | body | MISSING | `div.col-12.col-md-8` | `p` | `—` | 617 | 289 | 0.26 of 2484 | template+ptype=Fundamentals/overview c=0.91 n=45 | 0.82 | — | CANDIDATE |
| 3984 | body | EXTRA | `div.col-12.col-md-8` | `—` | `img.img-fluid` | 566 | 254 | 0.96 of 2484 | template+ptype=Standard/overview c=1.00 n=26 | structure | — | CANDIDATE |
| 3985 | body | EXTRA | `div.col-12.col-md-8` | `—` | `WIDGET` | 395 | 241 | 0.93 of 2484 | subject+ptype=NCEA1/lesson c=0.99 n=49 | structure | — | CANDIDATE |
| 3986 | body | MOVED | `div.col-12.col-md-8` | `p` | `p` | 346 | 219 | 0.16 of 2484 | template+ptype=Fundamentals/overview c=0.83 n=40 | structure | — | CANDIDATE |
| 3987 | body | EXTRA | `div.row` | `—` | `div.col-12.col-md-8` | 298 | 211 | 0.84 of 2484 | subject+ptype=1-10 Blended Literacy/lesson c=0.95 n=30 | structure | — | CANDIDATE |
| 3988 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p>b` | 329 | 201 | 0.97 of 2484 | subject=1-10 Blended Literacy c=1.00 n=45 | structure | — | CANDIDATE |
| 3989 | body | EXTRA | `div.col-12.col-md-8` | `—` | `h3` | 309 | 196 | 0.82 of 2484 | subject+ptype=1-10 Blended Literacy/overview c=1.00 n=20 | structure | — | CANDIDATE |
| 3990 | body | SUBSTITUTED | `div.row` | `div.col-12` | `div.col-12.col-md-8` | 330 | 190 | 0.55 of 2484 | subject+ptype=1-10 Blended Literacy/overview c=0.96 n=67 | structure | — | CANDIDATE |
| 3991 | body | EXTRA | `div.col-12.col-md-8` | `—` | `ul` | 325 | 187 | 0.95 of 2484 | subject=1-10 Mathematics c=0.98 n=21 | structure | — | CANDIDATE |
| 3992 | body | MISSING | `div.row` | `div.col-12.col-md-8` | `—` | 323 | 181 | 0.23 of 2484 | template+ptype=Fundamentals/overview c=0.94 n=20 | 0.94 | — | CANDIDATE |
| 3994 | body | MISSING | `div.col-12.col-md-8` | `WIDGET` | `—` | 268 | 174 | 0.19 of 2484 | template+ptype=Fundamentals/overview c=0.65 n=31 | structure | — | CANDIDATE |
| 3996 | body | EXTRA | `div.col-12.col-md-8` | `—` | `a` | 236 | 157 | 0.98 of 2484 | subject=1-10 English c=0.99 n=27 | structure | — | CANDIDATE |
| 3997 | body | MISSING | `div.col-12.col-md-8` | `h3` | `—` | 240 | 153 | 0.18 of 2484 | template+ptype=Fundamentals/overview c=0.75 n=21 | 0.89 | — | CANDIDATE |
| 4000 | body | EXTRA | `p>b` | `—` | `b` | 191 | 122 | 0.94 of 2484 | subject=1-10 Mathematics c=0.97 n=33 | structure | — | CANDIDATE |
| 4001 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.table-responsive` | 168 | 116 | 0.92 of 2484 | template=Standard c=0.92 n=146 | structure | — | CANDIDATE |
| 4002 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.ratio.ratio-16x9.videoSection` | 177 | 115 | 0.93 of 2484 | subject=NCEA1 c=0.98 n=21 | structure | yes | CANDIDATE |
| 4005 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p>a` | 170 | 113 | 0.99 of 2484 | subject=1-10 English c=1.00 n=20 | structure | — | CANDIDATE |
| 4007 | body | EXTRA | `a` | `—` | `div.button` | 181 | 110 | 0.97 of 2484 | subject=NCEA1 c=0.98 n=38 | structure | — | CANDIDATE |
| 4014 | body | EXTRA | `p` | `—` | `b` | 119 | 93 | 0.93 of 2484 | subject=NCEA1 c=0.96 n=29 | structure | — | CANDIDATE |
| 4016 | body | EXTRA | `div.table-responsive` | `—` | `table.table.table-bordered` | 137 | 91 | 0.96 of 2484 | subject=NCEA1 c=0.97 n=28 | structure | yes | CANDIDATE |
| 4020 | body | EXTRA | `p>i` | `—` | `i` | 109 | 82 | 0.97 of 2484 | subject+ptype=1-10 Blended Literacy/overview c=1.00 n=26 | structure | — | CANDIDATE |
| 4021 | body | SUBSTITUTED | `div.icon.ratio.ratio-16x9.videoSection` | `iframe.embed-responsive-item` | `iframe` | 214 | 81 | 0.19 of 2484 | series=PES10 c=0.68 n=35 | structure | yes | CANDIDATE |
| 4022 | body | EXTRA | `div.col-12.col-md-8` | `—` | `ol` | 107 | 81 | 0.99 of 2484 | template=Standard c=0.99 n=86 | structure | — | CANDIDATE |
| 4024 | body | SUBSTITUTED | `div#body` | `div.row` | `WIDGET` | 123 | 75 | 0.94 of 2484 | subject=Online Safety (OS9000) c=1.00 n=27 | structure | — | CANDIDATE |
| 4027 | body | EXTRA | `div.row` | `—` | `div.col-12` | 136 | 74 | 0.71 of 2484 | subject=ANZH c=0.74 n=21 | structure | — | CANDIDATE |
| 4028 | body | EXTRA | `div.col-12.col-md-8` | `—` | `audio.audioPlayer.icon` | 133 | 74 | 1.00 of 2484 | ptype=overview c=1.00 n=35 | structure | yes | CANDIDATE |
| 4029 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p>i` | 101 | 73 | 0.98 of 2484 | subject=NCEA1 c=0.99 n=26 | structure | — | CANDIDATE |
| 4030 | body | EXTRA | `p>a` | `—` | `a` | 99 | 73 | 0.99 of 2484 | template=Standard c=1.00 n=78 | structure | — | CANDIDATE |
| 4033 | body | MOVED | `div.col-12.col-md-8` | `h3` | `h3` | 85 | 71 | 0.11 of 2484 | template+ptype=Fundamentals/overview c=0.67 n=23 | structure | — | CANDIDATE |
| 4040 | body | EXTRA | `div.fundamentalsPanel` | `—` | `div.row` | 73 | 68 | 0.98 of 2484 | era=Refresh c=0.98 n=73 | structure | — | CANDIDATE |
| 4045 | body | EXTRA | `a` | `—` | `div.externalButton` | 91 | 65 | 0.92 of 2484 | template=Standard c=0.93 n=78 | structure | — | CANDIDATE |
| 4046 | body | EXTRA | `table.table.table-bordered` | `—` | `tr` | 89 | 65 | 0.98 of 2484 | template=Standard c=0.98 n=77 | structure | yes | CANDIDATE |
| 4047 | body | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `div.col-12.col-md-8` | 74 | 65 | 0.98 of 2484 | ptype=lesson c=0.99 n=44 | structure | — | CANDIDATE |
| 4050 | body | EXTRA | `div.col-12.col-md-8` | `—` | `h4` | 74 | 64 | 0.97 of 2484 | template=Standard c=0.98 n=34 | structure | — | CANDIDATE |
| 4052 | body | EXTRA | `ul` | `—` | `li` | 75 | 62 | 0.93 of 2484 | template=Standard c=0.94 n=57 | structure | — | CANDIDATE |
| 4054 | body | EXTRA | `div.ratio.ratio-16x9.videoSection` | `—` | `iframe` | 79 | 61 | 0.92 of 2484 | template=Standard c=0.93 n=55 | structure | yes | CANDIDATE |
| 4055 | body | EXTRA | `div.col-12` | `—` | `p` | 95 | 58 | 0.92 of 2484 | template=Standard c=0.94 n=82 | structure | — | CANDIDATE |
| 4056 | body | EXTRA | `div.alert` | `—` | `div.row` | 71 | 56 | 0.91 of 2484 | template=Standard c=0.92 n=51 | structure | — | CANDIDATE |
| 4058 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `p` | 70 | 55 | 0.84 of 2484 | era=Refresh c=0.84 n=70 | structure | — | CANDIDATE |
| 4060 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `div.activity[number=*]` | 60 | 53 | 0.84 of 2484 | era=Refresh c=0.84 n=60 | structure | yes | CANDIDATE |
| 4063 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.alert` | 64 | 49 | 0.90 of 2484 | template=Standard c=0.91 n=49 | structure | — | CANDIDATE |
| 4066 | body | EXTRA | `div.row` | `—` | `div.col-12.col-md-6` | 71 | 47 | 0.99 of 2484 | subject=Online Safety (OS9000) c=1.00 n=26 | structure | — | CANDIDATE |
| 4068 | body | EXTRA | `tr` | `—` | `td` | 54 | 47 | 0.94 of 2484 | template=Standard c=0.95 n=50 | structure | — | CANDIDATE |
| 4069 | body | EXTRA | `div#body` | `—` | `WIDGET` | 82 | 46 | 0.93 of 2484 | era=Refresh c=0.93 n=82 | structure | — | CANDIDATE |
| 4074 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.icon.ratio.ratio-16x9.videoSection` | 62 | 44 | 0.92 of 2484 | template=Standard c=0.93 n=54 | structure | yes | CANDIDATE |
| 4077 | body | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `WIDGET` | 46 | 43 | 0.98 of 2484 | ptype=lesson c=0.99 n=38 | structure | — | CANDIDATE |
| 4082 | body | EXTRA | `div#body` | `—` | `div.row.supervisor` | 50 | 40 | 0.90 of 2484 | ptype=lesson c=0.91 n=41 | structure | yes | CANDIDATE |
| 4083 | body | MISSING | `div#body` | `div.fundamentalsPanel` | `—` | 46 | 40 | 0.02 of 2484 | template+ptype=Fundamentals/overview c=0.60 n=39 | 0.98 | yes | CANDIDATE |
| 4088 | body | EXTRA | `p` | `—` | `i` | 44 | 38 | 0.96 of 2484 | template=Standard c=0.97 n=40 | structure | — | CANDIDATE |
| 4091 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `WIDGET` | 39 | 38 | 0.84 of 2484 | era=Refresh c=0.84 n=39 | structure | — | CANDIDATE |
| 4093 | body | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `div.row` | 38 | 37 | 0.98 of 2484 | ptype=lesson c=0.99 n=21 | structure | — | CANDIDATE |
| 4095 | body | EXTRA | `tr` | `—` | `th` | 39 | 36 | 0.99 of 2484 | template=Standard c=1.00 n=33 | structure | — | CANDIDATE |
| 4096 | body | EXTRA | `div.alert.solid` | `—` | `div.row` | 47 | 35 | 0.94 of 2484 | era=Refresh c=0.94 n=47 | structure | yes | CANDIDATE |
| 4097 | body | EXTRA | `div.col-12.col-md-8` | `—` | `h5` | 44 | 35 | 0.98 of 2484 | subject=NCEA1 c=0.99 n=21 | structure | — | CANDIDATE |
| 4098 | body | MISSING | `div#body` | `div.inquiryPanel` | `—` | 38 | 35 | 0.02 of 2484 | template+ptype=Inquiry/overview c=0.60 n=26 | 0.93 | — | CANDIDATE |
| 4101 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p>span.infoTrigger` | 38 | 34 | 0.87 of 2484 | template=Standard c=0.87 n=32 | structure | — | CANDIDATE |
| 4105 | body | EXTRA | `div.row` | `—` | `div.col-12.col-md-4.offset-md-0` | 33 | 33 | 0.80 of 2484 | template=Standard c=0.81 n=21 | structure | — | CANDIDATE |
| 4107 | body | EXTRA | `div.col-12.col-md-8` | `—` | `h4.goJournal` | 40 | 32 | 1.00 of 2484 | template=Standard c=1.00 n=38 | structure | — | CANDIDATE |
| 4113 | body | EXTRA | `div.icon.ratio.ratio-16x9.videoSection` | `—` | `iframe` | 38 | 31 | 0.97 of 2484 | ptype=lesson c=0.98 n=31 | structure | yes | CANDIDATE |
| 4116 | body | EXTRA | `div#body` | `—` | `div.fundamentalsPanel` | 37 | 30 | 0.98 of 2484 | era=Refresh c=0.98 n=37 | structure | yes | CANDIDATE |
| 4119 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.flipCardsContainer.row` | 32 | 29 | 0.93 of 2484 | template=Standard c=0.94 n=27 | structure | — | CANDIDATE |
| 4120 | body | EXTRA | `div.inquiryPanel` | `—` | `div.row` | 30 | 29 | 0.99 of 2484 | era=Refresh c=0.99 n=30 | structure | — | CANDIDATE |
| 4122 | body | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `p` | 30 | 29 | 0.98 of 2484 | ptype=lesson c=0.99 n=21 | structure | — | CANDIDATE |
| 4125 | body | EXTRA | `div.introduction` | `—` | `div.row` | 28 | 28 | 0.99 of 2484 | era=Refresh c=0.99 n=28 | structure | — | CANDIDATE |
| 4128 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.clickDropContent` | 32 | 27 | 0.94 of 2484 | template=Standard c=0.94 n=29 | structure | — | CANDIDATE |
| 4130 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `img.img-fluid` | 28 | 27 | 0.84 of 2484 | era=Refresh c=0.84 n=28 | structure | — | CANDIDATE |
| 4132 | body | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `div.col-12.col-md-6` | 33 | 26 | 0.98 of 2484 | ptype=lesson c=0.99 n=29 | structure | — | CANDIDATE |
| 4138 | body | EXTRA | `div.row` | `—` | `div.col-12.col-md-4` | 32 | 25 | 0.95 of 2484 | template=Standard c=0.95 n=26 | structure | — | CANDIDATE |
| 4143 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.alert.solid` | 30 | 24 | 0.99 of 2484 | template=Standard c=0.99 n=25 | structure | yes | CANDIDATE |
| 4149 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `h3` | 24 | 23 | 0.84 of 2484 | era=Refresh c=0.84 n=24 | structure | — | CANDIDATE |
| 4155 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `div.activity.interactive[number=*]` | 24 | 22 | 0.84 of 2484 | era=Refresh c=0.84 n=24 | structure | yes | CANDIDATE |
| 4164 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `div.alert` | 28 | 20 | 0.84 of 2484 | era=Refresh c=0.84 n=28 | structure | — | CANDIDATE |
| 4172 | body | EXTRA | `p>span.infoTrigger` | `—` | `span.infoTrigger` | 20 | 20 | 0.95 of 2484 | era=Refresh c=0.95 n=20 | structure | — | CANDIDATE |
| 4173 | body | EXTRA | `div#body` | `—` | `div.inquiryPanel` | 20 | 20 | 0.98 of 2484 | era=Refresh c=0.98 n=20 | structure | — | CANDIDATE |
| 4177 | body | EXTRA | `div.col-12.col-md-6` | `—` | `img.img-fluid` | 23 | 19 | 0.99 of 2484 | template=Standard c=0.99 n=22 | structure | — | CANDIDATE |
| 4194 | body | SUBSTITUTED | `div#body` | `div.row` | `div.table-responsive` | 23 | 17 | 0.94 of 2484 | template=Standard c=0.98 n=21 | structure | — | CANDIDATE |
| 4224 | body | EXTRA | `div.col-12.col-md-6` | `—` | `p` | 23 | 14 | 1.00 of 2484 | ptype=lesson c=1.00 n=21 | structure | — | CANDIDATE |
| 4262 | body | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `div.button` | 25 | 12 | 0.98 of 2484 | ptype=lesson c=0.99 n=23 | structure | — | CANDIDATE |
| 9290 | root | EXTRA | `body.container-fluid` | `—` | `div.row` | 273 | 273 | 0.88 of 2491 | subject+ptype=1-10 Mathematics/overview c=0.97 n=33 | structure | — | CANDIDATE |
| 9295 | root | SUBSTITUTED | `#root` | `body` | `body.container-fluid` | 138 | 15 | 0.06 of 2491 | series=PWY10 c=1.00 n=44 | structure | yes | CANDIDATE |

## Details — in the companion file `CONVERTER_V2/outputs/_diff_queue_details.md`
Every CANDIDATE and every top-40 row has three quoted examples (WT / gold / Claude) there, plus the
below-floor list. **NEVER read the companion whole** (hundreds of KB): `grep -n '^### #<rank> ' CONVERTER_V2/outputs/_diff_queue_details.md` then `sed -n '<start>,<start+40>p'`. The top 25
candidates' detail blocks are repeated below for convenience.

### #4 · title · MISSING · `div#header` › gold `h1>span` vs Claude `—` — CANDIDATE
- pages 275 / modules 134 / lines 279; consensus (all) 0.24 of 2491 gold pages with the region; derivable 0.76 (68 lines with no WT source)
- by template: Standard 86m/207p c=0.20; Fundamentals 27m/27p c=0.48; Inquiry 15m/18p c=0.40; Bilingual 6m/23p c=1.00
- by subject: NCEA1 22m/45p c=0.17; 1-10 English 21m/32p c=0.18; Leaving to Learn 14m/22p c=0.33; Online Safety (OS9000) 13m/29p c=0.32; 1-10 Mathematics 11m/11p c=0.14; ConnectED 7m/7p c=0.28
- by era: Refresh 134m/275p c=0.24
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
- modules: ANZH101, ANZH103, ANZH104, ANZH301, ANZH401, ANZH404, ARFUN01, ARFUN02, ARFUN03, ARFUN04, ARFUN05, ART1004, ART1006, CEDK102, CEDK401, CEDK501, CEDO202, CEDR101, CEDR204, CEDT301, CHI1005, CHWHA, DTC1005, ENFUN01 …

### #5 · title · EXTRA · `div#header` › gold `—` vs Claude `h1>span` — CANDIDATE
- pages 22 / modules 21 / lines 23; consensus (all) 0.76 of 2491 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 16m/17p c=0.81; Fundamentals 4m/4p c=0.52; Inquiry 1m/1p c=0.60
- by subject: 1-10 Blended Literacy 6m/6p c=0.99; NCEA1 4m/4p c=0.83; Leaving to Learn 4m/4p c=0.68; 1-10 Writing (MiW) 2m/2p c=0.38; ANZH 1m/2p c=0.51; ConnectED 1m/1p c=0.72
- by era: Refresh 21m/22p c=0.76
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
- modules: AGH1005, ANZH302, BLL246, BLL271, BLL272, BLL273, BLL274, BLL276, CEDO105, ENGFUN02, ENGI103, FRFUN06, HIS1002, PWY1002, SSFUN07, WJFUN105, WJFUN116, XDLS904, XDLS906, XFUN02, XOTPB08

### #35 · module-menu · SUBSTITUTED · `div.col-12.col-md-6.paddingR` › gold `p` vs Claude `h5` — CANDIDATE
- pages 84 / modules 84 / lines 152; consensus (all) 0.06 of 2491 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 62m/62p c=0.05; Fundamentals 14m/14p c=0.12; Inquiry 8m/8p c=0.38
- by subject: 1-10 Blended Literacy 70m/70p c=0.25; 1-10 Health and PE 14m/14p c=0.39
- by era: Refresh 84m/84p c=0.06
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

### #37 · module-menu · MISSING · `div.col-12.col-md-8` › gold `ul` vs Claude `—` — CANDIDATE
- pages 215 / modules 55 / lines 394; consensus (all) 0.29 of 2491 gold pages with the region; derivable 0.92 (31 lines with no WT source)
- by template: Standard 50m/198p c=0.32; Inquiry 4m/16p c=0.22; Fundamentals 1m/1p c=0.01
- by subject: NCEA1 13m/50p c=0.21; Leaving to Learn 12m/33p c=0.43; 1-10 English 11m/36p c=0.61; 1-10 Blended Literacy 4m/11p c=0.07; ConnectED 4m/17p c=0.42; 1-10 Languages 4m/12p c=0.40
- by era: Refresh 55m/215p c=0.29
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

### #38 · module-menu · MISSING · `div.col-12.col-md-8` › gold `h5` vs Claude `—` — CANDIDATE
- pages 213 / modules 47 / lines 385; consensus (all) 0.24 of 2491 gold pages with the region; derivable 0.84 (62 lines with no WT source)
- by template: Standard 42m/198p c=0.27; Inquiry 4m/14p c=0.17; Fundamentals 1m/1p c=0.01
- by subject: NCEA1 13m/59p c=0.23; 1-10 English 12m/57p c=0.55; Leaving to Learn 5m/10p c=0.14; ConnectED 4m/17p c=0.42; 1-10 Languages 4m/12p c=0.40; 1-10 Blended Literacy 3m/10p c=0.06
- by era: Refresh 47m/213p c=0.24
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

### #40 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `div.col-12.col-md-6.paddingR` — CANDIDATE
- pages 65 / modules 45 / lines 102; consensus (all) 0.97 of 2491 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 38m/58p c=0.97; Inquiry 4m/4p c=0.90; Fundamentals 3m/3p c=1.00
- by subject: 1-10 Blended Literacy 16m/16p c=0.76; ANZH 7m/10p c=1.00; 1-10 Mathematics 7m/18p c=1.00; 1-10 English 4m/4p c=1.00; Leaving to Learn 4m/4p c=1.00; 1-10 Arts 3m/3p c=1.00
- by era: Refresh 45m/65p c=0.97
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

### #41 · module-menu · EXTRA · `ul` › gold `—` vs Claude `li` — CANDIDATE
- pages 81 / modules 43 / lines 166; consensus (all) 0.78 of 2491 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 30m/68p c=0.79; Inquiry 11m/11p c=0.40; Fundamentals 2m/2p c=0.77
- by subject: 1-10 Blended Literacy 10m/10p c=0.65; 1-10 English 8m/11p c=0.75; ConnectED 7m/7p c=0.52; NCEA1 6m/16p c=0.97; Te ara Whakapuawa -Wellbeing 5m/5p c=0.08; 1-10 Science 3m/24p c=0.70
- by era: Refresh 43m/81p c=0.78
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

### #42 · module-menu · SUBSTITUTED · `div.col-12.col-md-6.paddingL` › gold `p` vs Claude `h5` — CANDIDATE
- pages 42 / modules 42 / lines 63; consensus (all) 0.03 of 2491 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Inquiry 15m/15p c=0.25; Fundamentals 14m/14p c=0.12; Standard 13m/13p c=0.02
- by subject: 1-10 Health and PE 14m/14p c=0.39; ConnectED 9m/9p c=0.12; Te ara Whakapuawa -Wellbeing 6m/6p c=0.85; 1-10 Blended Literacy 5m/5p c=0.01; Leaving to Learn 4m/4p c=0.02; ANZH 2m/2p c=0.02
- by era: Refresh 42m/42p c=0.03
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
- modules: ANZH105, ANZH205, BLL172, BLL174, BLL175, BLL176, BLL177, CEDK102, CEDO102, CEDO201, CEDO202, CEDO402, CEDR204, CEDT404, CEDW101, CEDW201, ENGC302, ENGC401, HPFUN101, HPFUN102, HPFUN103, HPFUN201, HPFUN202, HPFUN203 …

### #43 · module-menu · MISSING · `div.col-12.col-md-6.paddingR` › gold `p` vs Claude `—` — CANDIDATE
- pages 51 / modules 37 / lines 70; consensus (all) 0.04 of 2491 gold pages with the region; derivable 0.73 (19 lines with no WT source)
- by template: Standard 28m/42p c=0.04; Inquiry 9m/9p c=0.18
- by subject: 1-10 Blended Literacy 23m/23p c=0.22; EXPlore 5m/8p c=0.00; ConnectED 4m/4p c=0.11; ANZH 2m/2p c=0.00; 1-10 Mathematics 2m/10p c=0.04; NCEA1 1m/4p c=0.00
- by era: Refresh 37m/51p c=0.04
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

### #47 · module-menu · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `h5` — CANDIDATE
- pages 81 / modules 25 / lines 107; consensus (all) 0.76 of 2491 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 23m/78p c=0.73; Fundamentals 1m/1p c=0.99; Inquiry 1m/2p c=0.83
- by subject: Leaving to Learn 7m/15p c=0.86; 1-10 English 6m/13p c=0.46; NCEA1 3m/9p c=0.77; 1-10 Science 3m/24p c=0.88; ANZH 2m/13p c=1.00; Online Safety (OS9000) 2m/2p c=0.40
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

### #48 · module-menu · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `p` — CANDIDATE
- pages 55 / modules 25 / lines 70; consensus (all) 0.88 of 2491 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 24m/53p c=0.87; Inquiry 1m/2p c=0.86
- by subject: Leaving to Learn 9m/20p c=0.69; NCEA1 7m/18p c=0.86; Online Safety (OS9000) 4m/8p c=0.79; ANZH 2m/3p c=1.00; 1-10 Mathematics 2m/5p c=0.93; 1-10 English 1m/1p c=0.84
- by era: Refresh 25m/55p c=0.88
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

### #49 · module-menu · MISSING · `div#header` › gold `div#module-head-buttons` vs Claude `—` — CANDIDATE
- pages 46 / modules 25 / lines 46; consensus (all) 0.77 of 2491 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 12m/19p c=0.78; Bilingual 7m/20p c=0.46; Inquiry 6m/7p c=0.85
- by subject: Te Marautanga o Aotearoa TMoA 7m/20p c=0.46; 1-10 Blended Literacy 6m/10p c=0.46; NCEA1 4m/4p c=0.73; ConnectED 3m/4p c=0.77; Leaving to Learn 2m/4p c=0.90; EXPlore 1m/1p c=1.00
- by era: Refresh 25m/46p c=0.77
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
- modules: BLL114, BLL116, BLL153, BLL250, BLL260, BLL272, CEDK401, CEDT207, CEDT301, EXPFUN07, GEO1004, HES1002, HES1006, MUS1004, MXFL401, PMT101, PNR101, PNR102, PNR104, PNR107, TRR109, TRR110, TWHT903, XLP06 …

### #52 · module-menu · EXTRA · `div.col-12.col-md-6.paddingR` › gold `—` vs Claude `p>b` — CANDIDATE
- pages 22 / modules 22 / lines 43; consensus (all) 1.00 of 2491 gold pages with the region; derivable structure-only (0 lines with no WT source)
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

### #54 · module-menu · SUBSTITUTED · `ul` › gold `li` vs Claude `li` — CANDIDATE
- pages 88 / modules 21 / lines 298; consensus (all) 0.57 of 2491 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 20m/87p c=0.60; Inquiry 1m/1p c=0.80
- by subject: 1-10 Mathematics 9m/28p c=0.54; NCEA1 4m/17p c=0.49; 1-10 English 3m/20p c=0.88; 1-10 Science 3m/21p c=0.85; ConnectED 1m/1p c=0.69; Leaving to Learn 1m/1p c=0.76
- by era: Refresh 21m/88p c=0.57
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **CEDT102** CEDT102_0_0.html ↔ CEDT102.html (structure, derivable=True)
  - gold: `li  «about who we are and how we are all unique»`
  - Claude: `li  «We are learning to celebrate diversity by noticing and embracing the differences between other people and us.»`
- **ENGC201** ENGC201_0_0.html ↔ ENGC201_0.0.html (structure, derivable=True)
  - gold: `li  «Being able to recognise and use the code, conventions, and features of diverse types of texts allows for a greater preci»`
  - Claude: `li  «People use language in diverse ways in different situations. This helps to signal social roles and relationships.»`
- **ENGC202** ENGC202_1_0.html ↔ ENGC202_1.0.html (structure, derivable=True)
  - gold: `li  «drawing what you hear from instructions»`
  - Claude: `li  «identify what makes a good instruction»`
- modules: CEDT102, ENGC201, ENGC202, ENGI103, ENO2060, JPN1004, MXDB301, MXDB302, MXEX301, MXFL101, MXFL102, MXFL201, MXFL202, MXFU301, MXFU402, MXS1004, PES1004, SCBI301, SCCH301, SCPH301, XWHA02

### #59 · module-menu · EXTRA · `div.col-12.col-md-6.offset-md-0` › gold `—` vs Claude `p` — CANDIDATE
- pages 24 / modules 18 / lines 59; consensus (all) 0.99 of 2491 gold pages with the region; derivable structure-only (0 lines with no WT source)
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

### #60 · module-menu · EXTRA · `div.col-12.col-md-6.paddingR` › gold `—` vs Claude `p` — CANDIDATE
- pages 18 / modules 18 / lines 41; consensus (all) 0.96 of 2491 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 14m/14p c=0.96; Inquiry 4m/4p c=0.82
- by subject: 1-10 Blended Literacy 8m/8p c=0.78; ConnectED 4m/4p c=0.89; 1-10 English 3m/3p c=1.00; ANZH 1m/1p c=1.00; 1-10 Mathematics 1m/1p c=0.95; Leaving to Learn 1m/1p c=1.00
- by era: Refresh 18m/18p c=0.96
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
- modules: ANZH401, BLL123, BLL131, BLL174, BLL175, BLL176, BLL177, BLL242, BLL252, CEDK101, CEDK102, CEDO402, CEDT104, ENGC301, ENGC302, ENGC401, MXEX202, XWHA02

### #63 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `WIDGET` — CANDIDATE
- pages 17 / modules 17 / lines 17; consensus (all) 0.88 of 2491 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 13m/13p c=0.88; Fundamentals 4m/4p c=0.80
- by subject: 1-10 Blended Literacy 13m/13p c=0.97; 1-10 Languages 2m/2p c=0.94; 1-10 Social Science 2m/2p c=0.58
- by era: Refresh 17m/17p c=0.88
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
- modules: BLL251, BLL255, BLL257, BLL261, BLL264, BLL265, BLL266, BLL271, BLL272, BLL274, BLL275, BLL276, BLLR201, JPFUN01, JPFUN02, SSFUN05, SSFUN08

### #64 · module-menu · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `ul` — CANDIDATE
- pages 43 / modules 16 / lines 75; consensus (all) 0.71 of 2491 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 15m/42p c=0.69; Fundamentals 1m/1p c=0.99
- by subject: 1-10 English 4m/15p c=0.39; Leaving to Learn 4m/8p c=0.57; NCEA1 3m/11p c=0.79; ANZH 2m/3p c=1.00; ConnectED 1m/1p c=0.58; 1-10 Mathematics 1m/4p c=0.85
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

### #65 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `div.col-12.col-md-8` — CANDIDATE
- pages 97 / modules 15 / lines 97; consensus (all) 0.67 of 2491 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 15m/97p c=0.63
- by subject: 1-10 Mathematics 12m/81p c=0.77; 1-10 English 2m/11p c=0.38; ConnectED 1m/5p c=0.56
- by era: Refresh 15m/97p c=0.67
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
- modules: CEDO105, ENGI102, ENGI103, MXDB301, MXDB302, MXDI301, MXEX101, MXEX301, MXEX302, MXFL204, MXFU201, MXFU202, MXFU301, MXFU302, MXFU402

### #67 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `div.col-12.col-md-6.offset-md-0` — CANDIDATE
- pages 31 / modules 15 / lines 31; consensus (all) 0.95 of 2491 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 13m/29p c=0.95; Fundamentals 2m/2p c=0.95
- by subject: 1-10 English 11m/27p c=0.90; 1-10 Mathematics 2m/2p c=0.94; 1-10 Social Science 2m/2p c=0.67
- by era: Refresh 15m/31p c=0.95
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
- modules: ENGC101, ENGC102, ENGC201, ENGI103, ENGI201, ENGI202, ENGI203, ENGI400, ENGJ102, ENGS202, ENGS301, MXFUN02, MXFUN03, SSOG101, SSOG105

### #69 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `div.col-12.col-md-12.paddingR` — CANDIDATE
- pages 16 / modules 14 / lines 16; consensus (all) 0.96 of 2491 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 14m/16p c=0.96
- by subject: 1-10 Blended Literacy 12m/12p c=0.80; EXPlore 2m/4p c=1.00
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

### #70 · module-menu · SUBSTITUTED · `div.col-12.col-md-6.paddingR` › gold `ul` vs Claude `p>b` — CANDIDATE
- pages 14 / modules 14 / lines 14; consensus (all) 0.06 of 2491 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 12m/12p c=0.05; Inquiry 2m/2p c=0.39
- by subject: 1-10 Blended Literacy 14m/14p c=0.25
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

### #73 · module-menu · EXTRA · `div.col-12.col-md-6.paddingL` › gold `—` vs Claude `h5` — CANDIDATE
- pages 13 / modules 13 / lines 31; consensus (all) 1.00 of 2491 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Inquiry 12m/12p c=0.99; Fundamentals 1m/1p c=1.00
- by subject: ConnectED 7m/7p c=1.00; Te ara Whakapuawa -Wellbeing 5m/5p c=0.92; 1-10 Health and PE 1m/1p c=1.00
- by era: Refresh 13m/13p c=1.00
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:158 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **CEDO202** CEDO202_0_0.html ↔ CEDO202_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «Whakamaheretia tō wā | Planning your time»`
- **CEDO204** CEDO204_0_0.html ↔ CEDO204_0_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «Success Criteria»`
- **CEDO402** CEDO402_0_0.html ↔ CEDO402_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «Whakamaheretia tō wā | Planning your time»`
- modules: CEDO202, CEDO204, CEDO402, CEDR203, CEDT101, CEDT207, CEDT301, HPFUN302, TWHA902, TWHK901, TWHK903, TWHK907, TWHR907

### #78 · module-menu · EXTRA · `div.col-12.col-md-6.paddingR` › gold `—` vs Claude `h5` — CANDIDATE
- pages 14 / modules 12 / lines 27; consensus (all) 0.99 of 2491 gold pages with the region; derivable structure-only (0 lines with no WT source)
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

### #81 · module-menu · EXTRA · `li>b` › gold `—` vs Claude `b` — CANDIDATE
- pages 24 / modules 11 / lines 44; consensus (all) 1.00 of 2491 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 11m/24p c=0.99
- by subject: NCEA1 3m/10p c=0.99; ConnectED 3m/8p c=0.98; ANZH 2m/2p c=1.00; 1-10 English 2m/3p c=1.00; Leaving to Learn 1m/1p c=0.99
- by era: Refresh 11m/24p c=1.00
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
