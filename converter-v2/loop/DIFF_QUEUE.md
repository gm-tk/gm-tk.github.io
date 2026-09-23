# DIFF_QUEUE.md — the diff miner's ranked class queue (LOOP__Autonomous_Rounds.md §1d)

**Produced:** 2026-09-24 11:42 NZST by `reference/tests/_diff_miner.py` on the CURRENT corpus (pageforge-site HEAD f0a1ae8; Claude corpus 545 dirs). **Population:** the skeleton gate's own — 2524 paired pages / 533 modules (compare_exclusions.txt honoured; acks / glossary / references pages excluded); parse errors skipped: 0 (must be 0); modules without a parsed WT: 2. Run time 84.6 s.

**What a row is.** One CLASS = (region, parent element, gold form, Claude form, direction) over every differing skeleton line of every paired page — the same lines, labels, widget collapse and difflib alignment the PRIMARY gate scores (each element its own line so it can be quoted). Direction: MISSING = gold has it, Claude lacks it; EXTRA = Claude has it, gold lacks it; SUBSTITUTED = same position, different tag / class / wrapper; MOVED = same text, different place. Consensus = of the gold pages in the group where the region exists, the share carrying the gold form (for EXTRA: the share NOT carrying Claude's form). Derivable = the gold line's text is in the module's parsed Writers Template (round-110 tolerance); structure-only differences are always derivable.

**Candidate rule (§1d).** modules ≥ 10 for a chrome class (module-code / title / header / module-menu / crumbs / phases-nav / footer / acks), pages ≥ 20 for a body / activity class; gold consensus ≥ 0.60 in at least one template or subject group that itself reaches the floor; structure-only or derivable share ≥ 0.60. A class below the floor is listed, never dropped. A CANDIDATE still goes through the PICK's KB-first check, the triangulation and the §3 corpus-wide measurement before any code — this table is the queue, not the verdict.

## Summary

- differing skeleton lines: 280601 — by direction {'MISSING': 148238, 'SUBSTITUTED': 25947, 'EXTRA': 97239, 'MOVED': 9177}
- by region: {'module-code': 23, 'title': 398, 'header': 6, 'module-menu': 13402, 'phases-nav': 57, 'crumbs': 57, 'footer': 2573, 'acks': 1402, 'activity': 101741, 'body': 159336, 'root': 1606}
- classes: 9406 — CANDIDATE 197, below floor 8906, the rest below consensus / not derivable

## Completeness census — the repeating chrome (§1d item 4)

| region | pages with region | gold items | gold items in WT | Claude items | derivable misses | pages with misses | modules with misses | status |
|---|---|---|---|---|---|---|---|---|
| module-menu | 1548 | 17511 | 16211 | 13733 | 4342 | 707 | 200 | CANDIDATE (verify by eye — text presence, not position) |
| crumbs | 58 | 372 | 358 | 332 | 75 | 30 | 26 | CANDIDATE (verify by eye — text presence, not position) |
| phases-nav | 90 | 356 | 323 | 313 | 63 | 31 | 23 | CANDIDATE (verify by eye — text presence, not position) |
| footer | 8 | 36 | 20 | 0 | 20 | 8 | 6 | BELOW FLOOR |

- **module-menu** by template: Fundamentals 11m/15p/46 misses; Inquiry 30m/42p/262 misses; Standard 159m/650p/4034 misses
  - ENGI201 ENGI201_2_0.html: gold 52 items (52 in WT) / Claude 6 — 49 derivable misses, e.g. p «This module focuses on ākonga engaging with stories from diverse backgrounds, wh» · h3 «Understand»
  - ENGI201 ENGI201_3_0.html: gold 52 items (52 in WT) / Claude 6 — 49 derivable misses, e.g. p «This module focuses on ākonga engaging with stories from diverse backgrounds, wh» · h3 «Understand»
  - ENGI201 ENGI201_4_0.html: gold 52 items (52 in WT) / Claude 6 — 48 derivable misses, e.g. h3 «Understand» · span «Understand»
  - ENGI201 ENGI201_1_0.html: gold 52 items (52 in WT) / Claude 6 — 47 derivable misses, e.g. p «This module focuses on ākonga engaging with stories from diverse backgrounds, wh» · h3 «Understand»
- **crumbs** by template: Inquiry 24m/24p/43 misses; Standard 2m/6p/32 misses
  - EXBP901 EXBP901_1_0.html: gold 6 items (6 in WT) / Claude 1 — 6 derivable misses, e.g. p «Intro» · p «Ideas»
  - EXBP901 EXBP901_3_0.html: gold 6 items (6 in WT) / Claude 1 — 6 derivable misses, e.g. p «Intro» · p «Learning Goals»
  - EXIP901 EXIP901_4_0.html: gold 6 items (6 in WT) / Claude 0 — 6 derivable misses, e.g. p «Intro» · p «Learning Goals»
  - CEDO402 CEDO402_0_0.html: gold 6 items (6 in WT) / Claude 3 — 5 derivable misses, e.g. p «Intro: History/Culture» · p «Timing a race»
- **phases-nav** by template: Fundamentals 22m/30p/59 misses; Standard 1m/1p/4 misses
  - ANZHFUN05 ANZHFUN05_0_0.html: gold 4 items (4 in WT) / Claude 0 — 4 derivable misses, e.g. p «Phase 1» · p «Phase 2»
  - ARFUN04 ARFUN04_0_0.html: gold 4 items (4 in WT) / Claude 0 — 4 derivable misses, e.g. p «Phase 1» · p «Phase 2»
  - FRFUN06 FRFUN06_6_0.html: gold 6 items (6 in WT) / Claude 6 — 4 derivable misses, e.g. p «Handwriting è» · p «Handwriting ê â î ô û»
  - FRFUN06 FRFUN06_7_0.html: gold 6 items (6 in WT) / Claude 2 — 4 derivable misses, e.g. p «Chromebook» · p «Mac»
- **footer** by template: Standard 6m/8p/20 misses
  - BLL241 BLL241_0_0.html: gold 4 items (4 in WT) / Claude 0 — 4 derivable misses, e.g. li «Next» · a#next-lesson «Next»
  - BLL245 BLL245_0_0.html: gold 4 items (4 in WT) / Claude 0 — 4 derivable misses, e.g. li «Next» · a#next-lesson «Next»
  - BLL236 BLL236_0_0.html: gold 4 items (2 in WT) / Claude 0 — 2 derivable misses, e.g. li «Next» · a#next-lesson «Next»
  - BLL236 BLL236_1_0.html: gold 6 items (2 in WT) / Claude 0 — 2 derivable misses, e.g. li «Next» · a#next-lesson «Next»

## Chrome facts — the header and footer as SETS per page (alignment-free; §1d items 2 + 4)

A fact is one thing a page's chrome has: `header:chip` (the `#module-code` div), `header:chip=module-code` / `=lesson-number` / `=lesson-number(00)`, `header:head-buttons`, `header:menu-content`, `header:title-h1-count=N`, `footer:present`, `footer:ul=<classes>`, `footer:link=prev-lesson` / `next-lesson` / `home-nav`, `footer:links=<order>`, `footer:inside-body`, `nav:crumbs`, `nav:phases`. MISSING = the gold page has the fact and Claude's does not; EXTRA the reverse. Consensus = the share of gold pages in the group that have (MISSING) / lack (EXTRA) the fact. Floor 10 modules.

| # | dir | fact | pages | modules | gold share (all) | consensus (all) | best group | status |
|---|---|---|---|---|---|---|---|---|
| F1 | MISSING | `header:title-h1-count=2` | 289 | 129 | 0.25 | 0.25 | subject+ptype=Online Safety (OS9000)/overview c=0.93 n=12 | CANDIDATE |
| F2 | EXTRA | `header:title-h1-count=1` | 286 | 126 | 0.75 | 0.25 | subject+ptype=Online Safety (OS9000)/overview c=0.93 n=12 | CANDIDATE |
| F3 | EXTRA | `header:chip=decimal-number` | 205 | 44 | 0.56 | 0.44 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F4 | MISSING | `header:chip=module-code` | 77 | 35 | 0.18 | 0.18 | template+ptype=Standard/overview c=0.74 n=13 | CANDIDATE |
| F5 | MISSING | `header:chip=lesson-number` | 174 | 31 | 0.19 | 0.19 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F6 | EXTRA | `header:menu-content` | 59 | 31 | 0.75 | 0.25 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F7 | EXTRA | `header:head-buttons` | 55 | 30 | 0.76 | 0.24 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F8 | EXTRA | `header:chip=other` | 80 | 28 | 0.05 | 0.95 | ptype=lesson c=0.99 n=15 | CANDIDATE |
| F9 | MISSING | `header:chip=decimal-number` | 76 | 28 | 0.56 | 0.56 | ptype=lesson c=0.70 n=22 | CANDIDATE |
| F10 | EXTRA | `header:title-h1-count=2` | 28 | 27 | 0.25 | 0.75 | template=Standard c=0.80 n=21 | CANDIDATE |
| F11 | EXTRA | `header:chip=module-code` | 27 | 27 | 0.18 | 0.82 | template=Standard c=0.85 n=15 | CANDIDATE |
| F12 | MISSING | `header:title-h1-count=1` | 25 | 24 | 0.75 | 0.75 | template=Standard c=0.80 n=19 | CANDIDATE |
| F13 | MISSING | `header:head-buttons` | 41 | 20 | 0.76 | 0.76 | template=Standard c=0.78 n=12 | CANDIDATE |
| F14 | MISSING | `header:chip=other` | 28 | 17 | 0.05 | 0.05 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F15 | EXTRA | `header:chip=lesson-number` | 45 | 15 | 0.19 | 0.81 | era=Refresh c=0.81 n=15 | CANDIDATE |
| F16 | EXTRA | `header:chip` | 7 | 7 | 0.97 | 0.03 | — | BELOW FLOOR |
| F17 | MISSING | `header:title-h1-count=3` | 6 | 6 | 0.00 | 0.00 | — | BELOW FLOOR |
| F18 | EXTRA | `header:title-h1-count=0` | 5 | 5 | 0.00 | 1.00 | — | BELOW FLOOR |
| F19 | MISSING | `header:chip` | 4 | 4 | 0.97 | 0.97 | — | BELOW FLOOR |
| F20 | MISSING | `header:menu-content` | 2 | 2 | 0.75 | 0.75 | — | BELOW FLOOR |
| F21 | EXTRA | `header:title-h1-count=3` | 1 | 1 | 0.00 | 1.00 | — | BELOW FLOOR |
| F22 | EXTRA | `header:chip=lesson-number(00)` | 1 | 1 | 0.00 | 1.00 | — | BELOW FLOOR |
| F23 | MISSING | `nav:phases` | 8 | 8 | 0.04 | 0.04 | — | BELOW FLOOR |
| F24 | MISSING | `nav:crumbs` | 1 | 1 | 0.02 | 0.02 | — | BELOW FLOOR |
| F25 | MISSING | `footer:inside-body` | 186 | 138 | 0.07 | 0.07 | subject+ptype=1-10 Languages/overview c=0.62 n=10 | CANDIDATE |
| F26 | EXTRA | `footer:links=prev-lesson,next-lesson,home-nav` | 288 | 127 | 0.60 | 0.40 | template+ptype=Standard/overview c=0.97 n=13 | CANDIDATE |
| F27 | EXTRA | `footer:links=next-lesson,home-nav` | 111 | 109 | 0.12 | 0.88 | ptype=lesson c=0.99 n=14 | CANDIDATE |
| F28 | EXTRA | `footer:link=next-lesson` | 137 | 85 | 0.82 | 0.18 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F29 | EXTRA | `footer:links=prev-lesson,home-nav` | 75 | 75 | 0.14 | 0.86 | template=Bilingual c=0.90 n=11 | CANDIDATE |
| F30 | MISSING | `footer:links=home-nav,next-lesson` | 70 | 69 | 0.03 | 0.03 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F31 | MISSING | `footer:link=next-lesson` | 64 | 64 | 0.82 | 0.82 | template=Bilingual c=0.88 n=10 | CANDIDATE |
| F32 | MISSING | `footer:links=prev-lesson,home-nav` | 93 | 63 | 0.14 | 0.14 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F33 | MISSING | `footer:links=prev-lesson,next-lesson,home-nav` | 64 | 62 | 0.60 | 0.60 | template+ptype=Bilingual/lesson c=0.83 n=10 | CANDIDATE |
| F34 | MISSING | `footer:links=home-nav,prev-lesson,next-lesson` | 122 | 55 | 0.05 | 0.05 | subject+ptype=1-10 Health and PE/overview c=0.71 n=12 | CANDIDATE |
| F35 | EXTRA | `footer:link=prev-lesson` | 54 | 37 | 0.81 | 0.20 | template+ptype=Standard/overview c=0.97 n=13 | CANDIDATE |
| F36 | MISSING | `footer:link=prev-lesson` | 29 | 28 | 0.81 | 0.81 | template+ptype=Standard/lesson c=0.98 n=14 | CANDIDATE |
| F37 | MISSING | `footer:ul=footer-nav` | 72 | 25 | 0.83 | 0.83 | ptype=lesson c=0.88 n=17 | CANDIDATE |
| F38 | MISSING | `footer:links=home-nav` | 36 | 23 | 0.04 | 0.04 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F39 | EXTRA | `footer:ul=footer-nav inquiry-nav` | 63 | 18 | 0.14 | 0.86 | ptype=lesson c=0.89 n=17 | CANDIDATE |
| F40 | MISSING | `footer:links=next-lesson,home-nav` | 18 | 18 | 0.12 | 0.12 | subject+ptype=NCEA1/overview c=0.80 n=10 | CANDIDATE |
| F41 | EXTRA | `footer:ul=footer-nav` | 22 | 14 | 0.83 | 0.17 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F42 | EXTRA | `footer:ul=footer-nav fundamentals-nav` | 16 | 9 | 0.02 | 0.98 | — | BELOW FLOOR |
| F43 | MISSING | `footer:links=home-nav,prev-lesson` | 8 | 8 | 0.00 | 0.00 | — | BELOW FLOOR |
| F44 | MISSING | `footer:ul=footer-nav fundamentals-nav` | 8 | 8 | 0.02 | 0.02 | — | BELOW FLOOR |
| F45 | EXTRA | `footer:link=home-nav` | 12 | 6 | 0.99 | 0.01 | — | BELOW FLOOR |
| F46 | MISSING | `footer:links=prev-lesson,home-nav,next-lesson` | 33 | 4 | 0.01 | 0.01 | — | BELOW FLOOR |
| F47 | MISSING | `footer:link=other` | 21 | 4 | 0.01 | 0.01 | — | BELOW FLOOR |
| F48 | EXTRA | `footer:present` | 10 | 4 | 1.00 | 0.00 | — | BELOW FLOOR |
| F49 | MISSING | `footer:links=prev-lesson,other,next-lesson,home-nav` | 15 | 3 | 0.01 | 0.01 | — | BELOW FLOOR |
| F50 | MISSING | `footer:ul=footer-nav inquiry-nav` | 10 | 3 | 0.14 | 0.14 | — | BELOW FLOOR |
| F51 | MISSING | `footer:links=other,next-lesson,home-nav` | 3 | 3 | 0.00 | 0.00 | — | BELOW FLOOR |
| F52 | EXTRA | `footer:links=home-nav` | 3 | 3 | 0.04 | 0.96 | — | BELOW FLOOR |
| F53 | MISSING | `footer:links=prev-lesson,other,home-nav` | 2 | 2 | 0.00 | 0.00 | — | BELOW FLOOR |
| F54 | MISSING | `footer:links=other,home-nav` | 1 | 1 | 0.00 | 0.00 | — | BELOW FLOOR |
| F55 | MISSING | `footer:links=prev-lesson,next-lesson` | 1 | 1 | 0.00 | 0.00 | — | BELOW FLOOR |
| F56 | MISSING | `footer:links=none` | 1 | 1 | 0.00 | 0.00 | — | BELOW FLOOR |

### F1 · MISSING `header:title-h1-count=2` — CANDIDATE (pages 289 / modules 129)
- by template+ptype: Standard/overview 57m/57p gold 0.64 Claude 0.53 c=0.64; Standard/lesson 41m/162p gold 0.12 Claude 0.03 c=0.12; Fundamentals/overview 28m/28p gold 0.69 Claude 0.40 c=0.69; Inquiry/overview 8m/8p gold 0.58 Claude 0.48 c=0.58; Bilingual/overview 6m/6p gold 1.00 Claude 0.70 c=1.00; Bilingual/lesson 6m/24p gold 1.00 Claude 0.66 c=1.00; Inquiry/lesson 1m/4p gold 0.12 Claude 0.00 c=0.12
- by subject: NCEA1 21m/56p gold 0.19 Claude 0.10 c=0.19; 1-10 English 21m/32p gold 0.18 Claude 0.09 c=0.18; Leaving to Learn 15m/23p gold 0.32 Claude 0.24 c=0.32; Online Safety (OS9000) 13m/29p gold 0.32 Claude 0.11 c=0.32; 1-10 Mathematics 12m/12p gold 0.16 Claude 0.12 c=0.16; 1-10 Technology 7m/19p gold 1.00 Claude 0.21 c=1.00; ANZH 6m/31p gold 0.47 Claude 0.17 c=0.47; Te Marautanga o Aotearoa TMoA 6m/30p gold 1.00 Claude 0.67 c=1.00
- **AGH1005** AGH1005_0_0.html ↔ AGH1005.00.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=3']
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ANZH103** ANZH103_0_0.html ↔ ANZH103_0_0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: AGH1005, ANZH101, ANZH103, ANZH104, ANZH301, ANZH401, ANZH404, ARFUN01, ARFUN03, ARFUN04, ARFUN05, ART1006, CEDK102, CEDO202, CEDO502, CEDR204, CHI1004, CHI1005, DTC1005, ENFUN01, ENFUN02, ENFUN03, ENFUN04, ENFUN05 …

### F2 · EXTRA `header:title-h1-count=1` — CANDIDATE (pages 286 / modules 126)
- by template+ptype: Standard/overview 56m/56p gold 0.35 Claude 0.46 c=0.65; Standard/lesson 40m/161p gold 0.88 Claude 0.97 c=0.12; Fundamentals/overview 26m/26p gold 0.31 Claude 0.58 c=0.69; Inquiry/overview 9m/9p gold 0.38 Claude 0.52 c=0.62; Bilingual/overview 6m/6p gold 0.00 Claude 0.30 c=1.00; Bilingual/lesson 6m/24p gold 0.00 Claude 0.34 c=1.00; Inquiry/lesson 1m/4p gold 0.88 Claude 1.00 c=0.12
- by subject: 1-10 English 21m/32p gold 0.82 Claude 0.91 c=0.18; NCEA1 19m/54p gold 0.80 Claude 0.89 c=0.20; Leaving to Learn 15m/23p gold 0.68 Claude 0.76 c=0.32; Online Safety (OS9000) 13m/29p gold 0.68 Claude 0.89 c=0.32; 1-10 Mathematics 12m/12p gold 0.84 Claude 0.88 c=0.16; 1-10 Technology 7m/19p gold 0.00 Claude 0.79 c=1.00; ANZH 6m/31p gold 0.53 Claude 0.83 c=0.47; Te Marautanga o Aotearoa TMoA 6m/30p gold 0.00 Claude 0.33 c=1.00
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ANZH103** ANZH103_0_0.html ↔ ANZH103_0_0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ANZH104** ANZH104_4_0.html ↔ ANZH104_04.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1']
- modules: ANZH101, ANZH103, ANZH104, ANZH301, ANZH401, ANZH404, ARFUN03, ARFUN04, ARFUN05, ART1006, CEDK102, CEDO202, CEDO502, CEDR204, CHI1004, CHI1005, CHWHA, DTC1005, ENFUN01, ENFUN02, ENFUN03, ENFUN04, ENFUN05, ENFUN07 …

### F4 · MISSING `header:chip=module-code` — CANDIDATE (pages 77 / modules 35)
- by template+ptype: Standard/lesson 14m/45p gold 0.04 Claude 0.01 c=0.04; Standard/overview 13m/13p gold 0.74 Claude 0.73 c=0.74; Bilingual/lesson 6m/17p gold 0.28 Claude 0.04 c=0.28; Inquiry/overview 2m/2p gold 0.43 Claude 0.52 c=0.43
- by subject: 1-10 Blended Literacy 14m/14p gold 0.07 Claude 0.03 c=0.07; Te Marautanga o Aotearoa TMoA 6m/17p gold 0.44 Claude 0.25 c=0.44; 1-10 Mathematics 5m/22p gold 0.17 Claude 0.11 c=0.17; NCEA1 2m/2p gold 0.13 Claude 0.14 c=0.13; EXPlore 2m/2p gold 0.27 Claude 0.13 c=0.27; Leaving to Learn 2m/5p gold 0.22 Claude 0.25 c=0.22; ANZH 1m/12p gold 0.26 Claude 0.14 c=0.26; ConnectED 1m/1p gold 0.09 Claude 0.11 c=0.09
- **ANZH401** ANZH401_1_0.html ↔ ANZH401_1.0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **BLL170** BLL170_0_0.html ↔ BLL170.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **BLL172** BLL172_0_0.html ↔ BLL172-00.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: ANZH401, BLL170, BLL172, BLL174, BLL175, BLL176, BLL177, BLL252, BLL253, BLL265, BLL266, BLL271, BLL273, BLL274, BLL276, CEDK501, CHI1004, ENGS401, EXBP901, EXIP901, HIS1003, MXEX101, MXFL101, MXFL102 …

### F8 · EXTRA `header:chip=other` — CANDIDATE (pages 80 / modules 28)
- by template+ptype: Standard/lesson 15m/67p gold 0.01 Claude 0.04 c=0.99; Standard/overview 13m/13p gold 0.25 Claude 0.27 c=0.75
- by subject: 1-10 Blended Literacy 14m/14p gold 0.26 Claude 0.30 c=0.74; 1-10 Mathematics 5m/7p gold 0.00 Claude 0.02 c=1.00; NCEA1 4m/29p gold 0.01 Claude 0.05 c=0.99; 1-10 Social Science 3m/17p gold 0.00 Claude 0.28 c=1.00; ANZH 1m/12p gold 0.06 Claude 0.19 c=0.94; Leaving to Learn 1m/1p gold 0.04 Claude 0.00 c=0.96
- **ANZH401** ANZH401_1_0.html ↔ ANZH401_1.0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **BLL172** BLL172_0_0.html ↔ BLL172-00.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **BLL174** BLL174_0_0.html ↔ BLL174-00.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: ANZH401, BLL172, BLL174, BLL175, BLL176, BLL177, BLL252, BLL253, BLL265, BLL266, BLL271, BLL273, BLL274, BLL276, BLLR203, MXDB301, MXEO301, MXEX301, MXFL302, MXFU302, PWY1001, PWY1002, PWY1008, PWY1009 …

### F9 · MISSING `header:chip=decimal-number` — CANDIDATE (pages 76 / modules 28)
- by template+ptype: Standard/lesson 22m/69p gold 0.70 Claude 0.76 c=0.70; Standard/overview 5m/5p gold 0.01 Claude 0.00 c=0.01; Inquiry/overview 1m/1p gold 0.02 Claude 0.00 c=0.02; Fundamentals/overview 1m/1p gold 0.01 Claude 0.00 c=0.01
- by subject: NCEA1 9m/34p gold 0.82 Claude 0.79 c=0.82; 1-10 Mathematics 6m/10p gold 0.73 Claude 0.77 c=0.73; 1-10 Blended Literacy 4m/7p gold 0.40 Claude 0.40 c=0.40; Leaving to Learn 4m/12p gold 0.39 Claude 0.49 c=0.39; 1-10 English 2m/9p gold 0.60 Claude 0.69 c=0.60; ConnectED 1m/1p gold 0.67 Claude 0.66 c=0.67; 1-10 Languages 1m/1p gold 0.48 Claude 0.63 c=0.48; 1-10 Social Science 1m/2p gold 0.31 Claude 0.49 c=0.31
- **ART1004** ART1004_0_0.html ↔ ART1004_4.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **ART1005** ART1005_0_0.html ↔ ART1005_3.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **BLL171** BLL171_1_0.html ↔ BLL171-1.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- modules: ART1004, ART1005, BLL171, BLL172, BLL173, BLLR203, CEDR501, COM1002, ENG1004, ENGFUN02, ENGJ101, ENGS101, FRFUN06, MXDB301, MXDI102, MXEO301, MXEX301, MXFL302, MXFU302, PWY1001, PWY1002, PWY1008, PWY1009, SSFUN07 …

### F10 · EXTRA `header:title-h1-count=2` — CANDIDATE (pages 28 / modules 27)
- by template+ptype: Standard/overview 18m/18p gold 0.64 Claude 0.53 c=0.36; Standard/lesson 4m/4p gold 0.12 Claude 0.03 c=0.88; Fundamentals/overview 4m/4p gold 0.69 Claude 0.40 c=0.31; Inquiry/overview 2m/2p gold 0.58 Claude 0.48 c=0.42
- by subject: NCEA1 7m/7p gold 0.19 Claude 0.10 c=0.81; 1-10 Blended Literacy 6m/6p gold 0.01 Claude 0.03 c=0.99; Leaving to Learn 5m/5p gold 0.32 Claude 0.24 c=0.68; 1-10 Languages 3m/3p gold 0.28 Claude 0.23 c=0.72; 1-10 Writing (MiW) 2m/2p gold 0.62 Claude 0.52 c=0.38; ANZH 1m/2p gold 0.47 Claude 0.17 c=0.53; ConnectED 1m/1p gold 0.27 Claude 0.24 c=0.73; 1-10 English 1m/1p gold 0.18 Claude 0.09 c=0.82
- **ANZH302** ANZH302_0_0.html ↔ ANZH302_0_0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2']
- **BLL246** BLL246_0_0.html ↔ BLL246_0.0.html: gold ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2']
- **BLL271** BLL271_0_0.html ↔ BLL271_0_0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2']
- modules: ANZH302, BLL246, BLL271, BLL272, BLL273, BLL274, BLL276, CEDO105, ENGFUN02, ENGI103, FRFUN06, GENO901, GEWHA, HIS1002, JPN1004, PHE1004, PWY1002, PWYWHA1, SPA1004, SSFUN07, WJFUN105, WJFUN116, XDLS904, XDLS906 …

### F11 · EXTRA `header:chip=module-code` — CANDIDATE (pages 27 / modules 27)
- by template+ptype: Standard/overview 11m/11p gold 0.74 Claude 0.73 c=0.26; Inquiry/overview 7m/7p gold 0.43 Claude 0.52 c=0.57; Fundamentals/overview 5m/5p gold 0.64 Claude 0.70 c=0.36; Standard/lesson 4m/4p gold 0.04 Claude 0.01 c=0.96
- by subject: Leaving to Learn 11m/11p gold 0.22 Claude 0.25 c=0.78; NCEA1 6m/6p gold 0.13 Claude 0.14 c=0.87; ConnectED 3m/3p gold 0.09 Claude 0.11 c=0.91; 1-10 Health and PE 2m/2p gold 0.42 Claude 0.47 c=0.58; 1-10 Social Science 2m/2p gold 0.21 Claude 0.23 c=0.79; 1-10 Languages 1m/1p gold 0.23 Claude 0.25 c=0.77; 1-10 Mathematics 1m/1p gold 0.17 Claude 0.11 c=0.83; Online Safety (OS9000) 1m/1p gold 0.21 Claude 0.21 c=0.79
- **ART1004** ART1004_0_0.html ↔ ART1004_4.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **ART1005** ART1005_0_0.html ↔ ART1005_3.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **CEDK401** CEDK401_0_0.html ↔ CEDK401 Food Sustainability.html: gold ['header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2']
- modules: ART1004, ART1005, CEDK401, CEDO402, CEDR401, COM1002, ENG1004, ENGFUN02, FRFUN06, GER1002, HPFUN201, HPFUN302, MXDB201, OSOH101, SSFUN01, SSFUN07, XDLS901, XDLS902, XDLS903, XDLS909, XFUN01, XGF9001, XLP01, XLP02 …

### F12 · MISSING `header:title-h1-count=1` — CANDIDATE (pages 25 / modules 24)
- by template+ptype: Standard/overview 16m/16p gold 0.35 Claude 0.46 c=0.35; Standard/lesson 4m/4p gold 0.88 Claude 0.97 c=0.88; Fundamentals/overview 4m/4p gold 0.31 Claude 0.58 c=0.31; Inquiry/overview 1m/1p gold 0.38 Claude 0.52 c=0.38
- by subject: NCEA1 6m/6p gold 0.80 Claude 0.89 c=0.80; 1-10 Blended Literacy 6m/6p gold 0.99 Claude 0.97 c=0.99; Leaving to Learn 5m/5p gold 0.68 Claude 0.76 c=0.68; 1-10 Writing (MiW) 2m/2p gold 0.38 Claude 0.48 c=0.38; ANZH 1m/2p gold 0.53 Claude 0.83 c=0.53; ConnectED 1m/1p gold 0.73 Claude 0.76 c=0.73; 1-10 English 1m/1p gold 0.82 Claude 0.91 c=0.82; 1-10 Languages 1m/1p gold 0.68 Claude 0.77 c=0.68
- **ANZH302** ANZH302_0_0.html ↔ ANZH302_0_0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2']
- **ART1004** ART1004_0_0.html ↔ ART1004_4.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **ART1005** ART1005_0_0.html ↔ ART1005_3.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- modules: ANZH302, ART1004, ART1005, BLL246, BLL271, BLL272, BLL273, BLL274, BLL276, CEDO105, ENGFUN02, ENGI103, FRFUN06, HIS1002, PWY1002, PWYWHA1, SSFUN07, WJFUN105, WJFUN116, XDLS904, XDLS906, XFUN02, XGF9004, XOTPB08

### F13 · MISSING `header:head-buttons` — CANDIDATE (pages 41 / modules 20)
- by template+ptype: Standard/lesson 10m/17p gold 0.74 Claude 0.75 c=0.74; Bilingual/lesson 8m/21p gold 0.30 Claude 0.00 c=0.30; Standard/overview 3m/3p gold 0.99 Claude 0.99 c=0.99
- by subject: Te Marautanga o Aotearoa TMoA 8m/21p gold 0.45 Claude 0.22 c=0.45; 1-10 Blended Literacy 5m/10p gold 0.45 Claude 0.42 c=0.45; NCEA1 3m/3p gold 0.72 Claude 0.73 c=0.72; Leaving to Learn 2m/4p gold 0.89 Claude 0.88 c=0.89; EXPlore 1m/1p gold 1.00 Claude 0.93 c=1.00; 1-10 Mathematics 1m/2p gold 0.78 Claude 0.79 c=0.78
- **BLL114** BLL114_1_0.html ↔ BLL114-02.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- **BLL116** BLL116_1_0.html ↔ BLL116-02.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- **BLL153** BLL153_1_0.html ↔ BLL153-1.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1']
- modules: BLL114, BLL116, BLL153, BLL236, BLL272, EXPFUN07, HES1002, MUS1004, MXFL401, PMT101, PNR101, PNR102, PNR104, PNR107, PWYWHA1, TRR107, TRR109, TRR110, XGF9004, XLP06

### F15 · EXTRA `header:chip=lesson-number` — CANDIDATE (pages 45 / modules 15)
- by template+ptype: Standard/lesson 12m/39p gold 0.25 Claude 0.19 c=0.75; Bilingual/lesson 3m/6p gold 0.01 Claude 0.10 c=0.99
- by subject: Leaving to Learn 4m/15p gold 0.34 Claude 0.25 c=0.66; 1-10 Blended Literacy 3m/6p gold 0.25 Claude 0.25 c=0.75; Te Marautanga o Aotearoa TMoA 3m/6p gold 0.01 Claude 0.08 c=0.99; 1-10 English 2m/9p gold 0.23 Claude 0.16 c=0.77; ConnectED 1m/1p gold 0.07 Claude 0.07 c=0.94; NCEA1 1m/5p gold 0.04 Claude 0.02 c=0.96; 1-10 Mathematics 1m/3p gold 0.09 Claude 0.10 c=0.91
- **BLL171** BLL171_1_0.html ↔ BLL171-1.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- **BLL172** BLL172_1_0.html ↔ BLL172-01.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- **BLL173** BLL173_1_0.html ↔ BLL173-01.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- modules: BLL171, BLL172, BLL173, CEDR501, ENGJ101, ENGS101, ENO2060, MXDI102, PNR102, PNR104, PNR107, XLP01, XLP05, XTAS101, XTAS103

### F25 · MISSING `footer:inside-body` — CANDIDATE (pages 186 / modules 138)
- by template+ptype: Standard/lesson 74m/103p gold 0.06 Claude 0.00 c=0.06; Standard/overview 48m/48p gold 0.14 Claude 0.00 c=0.14; Fundamentals/overview 19m/19p gold 0.23 Claude 0.00 c=0.23; Inquiry/overview 10m/10p gold 0.17 Claude 0.00 c=0.17; Inquiry/lesson 2m/2p gold 0.06 Claude 0.00 c=0.06; Bilingual/lesson 2m/2p gold 0.03 Claude 0.00 c=0.03; Fundamentals/lesson 1m/2p gold 0.07 Claude 0.00 c=0.07
- by subject: 1-10 Blended Literacy 35m/46p gold 0.14 Claude 0.00 c=0.14; Leaving to Learn 20m/27p gold 0.11 Claude 0.00 c=0.11; 1-10 English 16m/22p gold 0.06 Claude 0.00 c=0.06; 1-10 Mathematics 15m/28p gold 0.08 Claude 0.00 c=0.08; NCEA1 12m/18p gold 0.03 Claude 0.00 c=0.03; 1-10 Languages 11m/12p gold 0.18 Claude 0.00 c=0.18; 1-10 Social Science 5m/5p gold 0.08 Claude 0.00 c=0.08; Te ara Whakapuawa -Wellbeing 5m/5p gold 0.39 Claude 0.00 c=0.39
- **ANZH101** ANZH101_0_0.html ↔ ANZH101_0.0.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH103** ANZH103_0_0.html ↔ ANZH103_0_0.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH302** ANZH302_3_0.html ↔ ANZH302_3_0.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: ANZH101, ANZH103, ANZH302, ARFUN02, ARFUN03, ARFUN04, ARFUN05, BLL113, BLL120, BLL122, BLL124, BLL125, BLL130, BLL145, BLL154, BLL156, BLL162, BLL164, BLL165, BLL166, BLL171, BLL173, BLL211, BLL212 …

### F26 · EXTRA `footer:links=prev-lesson,next-lesson,home-nav` — CANDIDATE (pages 288 / modules 127)
- by template+ptype: Standard/lesson 72m/206p gold 0.74 Claude 0.83 c=0.26; Inquiry/overview 32m/32p gold 0.13 Claude 0.67 c=0.87; Fundamentals/overview 13m/13p gold 0.05 Claude 0.20 c=0.95; Standard/overview 13m/13p gold 0.03 Claude 0.05 c=0.97; Inquiry/lesson 3m/13p gold 0.44 Claude 0.82 c=0.56; Bilingual/lesson 3m/3p gold 0.83 Claude 0.73 c=0.17; Fundamentals/lesson 1m/8p gold 0.63 Claude 0.87 c=0.37
- by subject: NCEA1 33m/59p gold 0.74 Claude 0.82 c=0.26; ConnectED 16m/21p gold 0.63 Claude 0.81 c=0.37; 1-10 Blended Literacy 14m/16p gold 0.41 Claude 0.41 c=0.59; 1-10 Health and PE 12m/12p gold 0.56 Claude 0.89 c=0.44; Leaving to Learn 10m/38p gold 0.48 Claude 0.62 c=0.52; 1-10 Mathematics 9m/59p gold 0.60 Claude 0.77 c=0.40; 1-10 English 8m/34p gold 0.64 Claude 0.72 c=0.36; Te ara Whakapuawa -Wellbeing 6m/6p gold 0.00 Claude 0.46 c=1.00
- **AGH1008** AGH1008_8_0.html ↔ AGH1008.08.html: gold ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH105** ANZH105_7_0.html ↔ ANZH105_07.0.html: gold ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH401** ANZH401_1_0.html ↔ ANZH401_1.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: AGH1008, ANZH105, ANZH401, ANZH404, ANZHFUN05, ART1002, BLL120, BLL140, BLL150, BLL170, BLL175, BLL210, BLL220, BLL230, BLL240, BLL250, BLL260, BLL270, BLLR202, BLLR203, CBI1004, CBI1005, CBI1008, CBI1009 …

### F27 · EXTRA `footer:links=next-lesson,home-nav` — CANDIDATE (pages 111 / modules 109)
- by template+ptype: Standard/overview 76m/76p gold 0.77 Claude 0.95 c=0.23; Standard/lesson 14m/15p gold 0.01 Claude 0.01 c=0.99; Fundamentals/overview 10m/10p gold 0.01 Claude 0.14 c=0.99; Inquiry/overview 9m/9p gold 0.02 Claude 0.15 c=0.98; Bilingual/overview 1m/1p gold 0.95 Claude 1.00 c=0.05
- by subject: Leaving to Learn 40m/41p gold 0.08 Claude 0.25 c=0.92; NCEA1 14m/15p gold 0.11 Claude 0.11 c=0.89; 1-10 Mathematics 13m/13p gold 0.07 Claude 0.11 c=0.93; Online Safety (OS9000) 9m/9p gold 0.15 Claude 0.21 c=0.85; 1-10 English 8m/8p gold 0.11 Claude 0.13 c=0.89; 1-10 Blended Literacy 6m/6p gold 0.29 Claude 0.30 c=0.70; ConnectED 6m/6p gold 0.06 Claude 0.10 c=0.94; 1-10 Social Science 6m/6p gold 0.13 Claude 0.23 c=0.87
- **ANZH401** ANZH401_0_0.html ↔ ANZH401_0.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH404** ANZH404_0_0.html ↔ ANZH404_0.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ART1004** ART1004_0_0.html ↔ ART1004_4.0.html: gold ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: ANZH401, ANZH404, ART1004, ART1005, BLL114, BLL116, BLL174, BLL175, BLL176, BLL177, CEDO301, CEDT102, CEDT104, CEDT207, CEDT208, CEDT301, COM1002, ENG1004, ENGFUN02, ENGI101, ENGI102, ENGJ101, ENGJ102, ENGJ301 …

### F29 · EXTRA `footer:links=prev-lesson,home-nav` — CANDIDATE (pages 75 / modules 75)
- by template+ptype: Standard/lesson 60m/60p gold 0.17 Claude 0.16 c=0.83; Bilingual/lesson 11m/11p gold 0.13 Claude 0.27 c=0.87; Inquiry/lesson 2m/2p gold 0.29 Claude 0.18 c=0.71; Fundamentals/lesson 2m/2p gold 0.07 Claude 0.13 c=0.93
- by subject: 1-10 Blended Literacy 20m/20p gold 0.24 Claude 0.29 c=0.76; 1-10 English 12m/12p gold 0.10 Claude 0.13 c=0.90; Te Marautanga o Aotearoa TMoA 11m/11p gold 0.10 Claude 0.21 c=0.90; NCEA1 9m/9p gold 0.10 Claude 0.06 c=0.90; 1-10 Mathematics 7m/7p gold 0.09 Claude 0.11 c=0.91; ANZH 4m/4p gold 0.10 Claude 0.13 c=0.91; Leaving to Learn 4m/4p gold 0.30 Claude 0.13 c=0.70; Online Safety (OS9000) 3m/3p gold 0.19 Claude 0.21 c=0.81
- **AGH1004** AGH1004_6_0.html ↔ AGH1004.07.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **AGH1009** AGH1009_9_0.html ↔ AGH1009.09.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH103** ANZH103_1_0.html ↔ ANZH103_3_0.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: AGH1004, AGH1009, ANZH103, ANZH301, ANZH302, ANZH303, BLL141, BLL146, BLL151, BLL157, BLL167, BLL171, BLL176, BLL177, BLL224, BLL225, BLL226, BLL227, BLL231, BLL234, BLL236, BLL237, BLL266, BLL271 …

### F31 · MISSING `footer:link=next-lesson` — CANDIDATE (pages 64 / modules 64)
- by template+ptype: Standard/lesson 50m/50p gold 0.82 Claude 0.84 c=0.82; Bilingual/lesson 10m/10p gold 0.84 Claude 0.73 c=0.84; Inquiry/overview 2m/2p gold 0.77 Claude 0.85 c=0.77; Inquiry/lesson 1m/1p gold 0.59 Claude 0.82 c=0.59; Fundamentals/lesson 1m/1p gold 0.63 Claude 0.87 c=0.63
- by subject: 1-10 Blended Literacy 19m/19p gold 0.75 Claude 0.70 c=0.75; Te Marautanga o Aotearoa TMoA 10m/10p gold 0.88 Claude 0.79 c=0.88; 1-10 English 8m/8p gold 0.86 Claude 0.85 c=0.86; NCEA1 7m/7p gold 0.88 Claude 0.94 c=0.88; 1-10 Mathematics 5m/5p gold 0.89 Claude 0.88 c=0.89; ANZH 4m/4p gold 0.90 Claude 0.87 c=0.90; Leaving to Learn 3m/3p gold 0.65 Claude 0.87 c=0.65; ConnectED 2m/2p gold 0.93 Claude 0.94 c=0.93
- **AGH1004** AGH1004_6_0.html ↔ AGH1004.07.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **AGH1009** AGH1009_9_0.html ↔ AGH1009.09.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH103** ANZH103_1_0.html ↔ ANZH103_3_0.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: AGH1004, AGH1009, ANZH103, ANZH301, ANZH302, ANZH303, BLL141, BLL146, BLL151, BLL157, BLL167, BLL171, BLL176, BLL177, BLL224, BLL225, BLL226, BLL227, BLL231, BLL234, BLL236, BLL237, BLL266, BLL274 …

### F33 · MISSING `footer:links=prev-lesson,next-lesson,home-nav` — CANDIDATE (pages 64 / modules 62)
- by template+ptype: Standard/lesson 46m/46p gold 0.74 Claude 0.83 c=0.74; Bilingual/lesson 10m/10p gold 0.83 Claude 0.73 c=0.83; Standard/overview 5m/5p gold 0.03 Claude 0.05 c=0.03; Fundamentals/lesson 1m/1p gold 0.63 Claude 0.87 c=0.63; Fundamentals/overview 1m/1p gold 0.05 Claude 0.20 c=0.05; Bilingual/overview 1m/1p gold 0.05 Claude 0.00 c=0.05
- by subject: 1-10 Blended Literacy 17m/17p gold 0.41 Claude 0.41 c=0.41; NCEA1 12m/13p gold 0.74 Claude 0.82 c=0.74; Te Marautanga o Aotearoa TMoA 10m/11p gold 0.66 Claude 0.57 c=0.66; 1-10 English 7m/7p gold 0.64 Claude 0.72 c=0.64; ANZH 4m/4p gold 0.60 Claude 0.75 c=0.60; Leaving to Learn 4m/4p gold 0.48 Claude 0.62 c=0.48; 1-10 Mathematics 2m/2p gold 0.60 Claude 0.77 c=0.60; Online Safety (OS9000) 2m/2p gold 0.56 Claude 0.57 c=0.56
- **AGH1004** AGH1004_6_0.html ↔ AGH1004.07.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **AGH1009** AGH1009_9_0.html ↔ AGH1009.09.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH103** ANZH103_1_0.html ↔ ANZH103_3_0.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: AGH1004, AGH1009, ANZH103, ANZH301, ANZH302, ANZH303, ART1005, BLL141, BLL146, BLL151, BLL157, BLL167, BLL171, BLL224, BLL225, BLL226, BLL227, BLL231, BLL234, BLL236, BLL237, BLL266, BLL274, BLL276 …

### F34 · MISSING `footer:links=home-nav,prev-lesson,next-lesson` — CANDIDATE (pages 122 / modules 55)
- by template+ptype: Inquiry/overview 32m/32p gold 0.57 Claude 0.03 c=0.57; Fundamentals/overview 12m/12p gold 0.15 Claude 0.00 c=0.15; Standard/lesson 11m/78p gold 0.04 Claude 0.00 c=0.04
- by subject: ConnectED 15m/15p gold 0.16 Claude 0.02 c=0.16; 1-10 Health and PE 12m/12p gold 0.33 Claude 0.00 c=0.33; 1-10 Blended Literacy 8m/8p gold 0.03 Claude 0.00 c=0.03; Te ara Whakapuawa -Wellbeing 8m/8p gold 0.61 Claude 0.00 c=0.61; 1-10 English 5m/32p gold 0.09 Claude 0.00 c=0.09; 1-10 Mathematics 5m/42p gold 0.12 Claude 0.00 c=0.12; EXPlore 1m/1p gold 0.07 Claude 0.00 c=0.07; Online Safety (OS9000) 1m/4p gold 0.03 Claude 0.00 c=0.03
- **BLL170** BLL170_0_0.html ↔ BLL170.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=home-nav,prev-lesson,next-lesson', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL210** BLL210_0_0.html ↔ BLL210.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=home-nav,prev-lesson,next-lesson', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL220** BLL220_0_0.html ↔ BLL220.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=home-nav,prev-lesson,next-lesson', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL170, BLL210, BLL220, BLL230, BLL240, BLL250, BLL260, BLL270, CEDK101, CEDK102, CEDK401, CEDO102, CEDO201, CEDO202, CEDO204, CEDO402, CEDR101, CEDR204, CEDT102, CEDT104, CEDT207, CEDT208, CEDW201, ENGJ101 …

### F35 · EXTRA `footer:link=prev-lesson` — CANDIDATE (pages 54 / modules 37)
- by template+ptype: Standard/lesson 14m/19p gold 0.98 Claude 0.99 c=0.02; Standard/overview 13m/13p gold 0.03 Claude 0.05 c=0.97; Inquiry/overview 5m/5p gold 0.72 Claude 0.70 c=0.28; Bilingual/lesson 2m/3p gold 0.96 Claude 1.00 c=0.04; Fundamentals/overview 1m/1p gold 0.20 Claude 0.20 c=0.80; Inquiry/lesson 1m/4p gold 0.88 Claude 1.00 c=0.12; Fundamentals/lesson 1m/9p gold 0.70 Claude 1.00 c=0.30
- by subject: NCEA1 14m/18p gold 0.87 Claude 0.89 c=0.13; 1-10 Blended Literacy 9m/9p gold 0.67 Claude 0.70 c=0.33; EXPlore 3m/3p gold 0.73 Claude 0.93 c=0.27; 1-10 Mathematics 3m/3p gold 0.88 Claude 0.88 c=0.12; ConnectED 2m/2p gold 0.92 Claude 0.90 c=0.08; Te Marautanga o Aotearoa TMoA 2m/3p gold 0.76 Claude 0.78 c=0.24; ANZH 1m/1p gold 0.86 Claude 0.87 c=0.14; 1-10 Languages 1m/9p gold 0.61 Claude 0.75 c=0.39
- **ANZHFUN05** ANZHFUN05_0_0.html ↔ ANZHFUN05_0_0.html: gold ['footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav fundamentals-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav fundamentals-nav']
- **BLL120** BLL120_0_0.html ↔ BLL120.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL140** BLL140_0_0.html ↔ BLL140.html: gold ['footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: ANZHFUN05, BLL120, BLL140, BLL150, BLL175, BLL176, BLL177, BLL271, BLLR202, BLLR203, CBI1005, CBI1008, CBI1009, CEDK501, CEDR401, CHI1003, CHI1004, CHI1005, COM1005, ENGFUN02, EXBP901, EXIP901, EXPFUN07, FRFUN06 …

### F36 · MISSING `footer:link=prev-lesson` — CANDIDATE (pages 29 / modules 28)
- by template+ptype: Standard/lesson 14m/14p gold 0.98 Claude 0.99 c=0.98; Standard/overview 7m/7p gold 0.03 Claude 0.05 c=0.03; Inquiry/overview 6m/6p gold 0.72 Claude 0.70 c=0.72; Fundamentals/overview 1m/1p gold 0.20 Claude 0.20 c=0.20; Bilingual/overview 1m/1p gold 0.05 Claude 0.00 c=0.05
- by subject: Leaving to Learn 13m/13p gold 0.78 Claude 0.75 c=0.78; NCEA1 6m/7p gold 0.87 Claude 0.89 c=0.87; ConnectED 4m/4p gold 0.92 Claude 0.90 c=0.92; Te ara Whakapuawa -Wellbeing 2m/2p gold 0.61 Claude 0.46 c=0.61; 1-10 Mathematics 1m/1p gold 0.88 Claude 0.88 c=0.88; 1-10 Social Science 1m/1p gold 0.77 Claude 0.77 c=0.77; Te Marautanga o Aotearoa TMoA 1m/1p gold 0.76 Claude 0.78 c=0.76
- **ART1004** ART1004_0_0.html ↔ ART1004_4.0.html: gold ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ART1005** ART1005_0_0.html ↔ ART1005_3.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **CEDT102** CEDT102_0_0.html ↔ CEDT102.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=home-nav,prev-lesson,next-lesson', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: ART1004, ART1005, CEDT102, CEDT104, CEDT207, CEDT208, COM1002, ENG1004, GER1002, MXFL101, PES1002, SSFUN02, TRR112, TWHK902, TWHK907, XGF9001, XOTPB08, XOTPB09, XOTPB10, XOTPB11, XOTPB12, XOTPB13, XOTPG01, XOTPG03 …

### F37 · MISSING `footer:ul=footer-nav` — CANDIDATE (pages 72 / modules 25)
- by template+ptype: Standard/lesson 16m/46p gold 0.88 Claude 0.86 c=0.88; Standard/overview 12m/12p gold 0.74 Claude 0.71 c=0.74; Fundamentals/overview 7m/7p gold 0.48 Claude 0.48 c=0.48; Inquiry/overview 2m/2p gold 0.12 Claude 0.08 c=0.12; Inquiry/lesson 1m/5p gold 1.00 Claude 0.85 c=1.00
- by subject: 1-10 Blended Literacy 12m/36p gold 0.11 Claude 0.00 c=0.11; 1-10 Technology 5m/5p gold 0.88 Claude 0.67 c=0.88; ConnectED 3m/16p gold 0.81 Claude 0.67 c=0.81; EXPlore 2m/5p gold 0.53 Claude 0.27 c=0.53; 1-10 Health and PE 1m/1p gold 0.69 Claude 0.67 c=0.69; NCEA1 1m/8p gold 1.00 Claude 0.98 c=1.00; 1-10 Writing (MiW) 1m/1p gold 0.62 Claude 0.71 c=0.62
- **BLL121** BLL121_0_0.html ↔ BLL121-01.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL172** BLL172_0_0.html ↔ BLL172-00.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL174** BLL174_0_0.html ↔ BLL174-00.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL121, BLL172, BLL174, BLL175, BLL176, BLL177, BLL236, BLL237, BLL241, BLL243, BLL244, BLL245, CEDR501, CEDT301, CEDW101, EXBP901, EXIP901, HPFUN301, MXS1004, TEFUN01, TEFUN02, TEFUN05, TEFUN06, TEFUN07 …

### F39 · EXTRA `footer:ul=footer-nav inquiry-nav` — CANDIDATE (pages 63 / modules 18)
- by template+ptype: Standard/lesson 16m/43p gold 0.12 Claude 0.13 c=0.88; Standard/overview 13m/13p gold 0.25 Claude 0.29 c=0.75; Inquiry/overview 2m/2p gold 0.88 Claude 0.92 c=0.12; Inquiry/lesson 1m/5p gold 0.00 Claude 0.15 c=1.00
- by subject: 1-10 Blended Literacy 12m/36p gold 0.89 Claude 1.00 c=0.11; ConnectED 3m/16p gold 0.18 Claude 0.33 c=0.81; EXPlore 2m/5p gold 0.47 Claude 0.73 c=0.53; Leaving to Learn 1m/6p gold 0.12 Claude 0.13 c=0.88
- **BLL121** BLL121_0_0.html ↔ BLL121-01.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL172** BLL172_0_0.html ↔ BLL172-00.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL174** BLL174_0_0.html ↔ BLL174-00.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL121, BLL172, BLL174, BLL175, BLL176, BLL177, BLL236, BLL237, BLL241, BLL243, BLL244, BLL245, CEDR501, CEDT301, CEDW101, EXBP901, EXIP901, XWHA02

### F40 · MISSING `footer:links=next-lesson,home-nav` — CANDIDATE (pages 18 / modules 18)
- by template+ptype: Standard/overview 12m/12p gold 0.77 Claude 0.95 c=0.77; Standard/lesson 4m/4p gold 0.01 Claude 0.01 c=0.01; Inquiry/overview 1m/1p gold 0.02 Claude 0.15 c=0.02; Bilingual/lesson 1m/1p gold 0.01 Claude 0.00 c=0.01
- by subject: NCEA1 11m/11p gold 0.11 Claude 0.11 c=0.11; 1-10 Blended Literacy 5m/5p gold 0.29 Claude 0.30 c=0.29; ConnectED 1m/1p gold 0.06 Claude 0.10 c=0.06; Te Marautanga o Aotearoa TMoA 1m/1p gold 0.22 Claude 0.22 c=0.22
- **BLL175** BLL175_1_1.html ↔ BLL175-02.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL176** BLL176_1_1.html ↔ BLL176-2.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL177** BLL177_2_0.html ↔ BLL177-2.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL175, BLL176, BLL177, BLLR202, BLLR203, CBI1005, CBI1008, CBI1009, CEDK501, CHI1003, CHI1004, CHI1005, GEO1004, GEO1005, GEO1006, JPN1004, MXS1004, TRR107


## The ranked queue — chrome regions first, then by modules affected

| # | region | dir | parent | gold form | Claude form | pages | modules | consensus (all) | best group | derivable | KB | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | module-code | EXTRA | `div#header` | `—` | `div#module-code` | 6 | 6 | 0.03 of 2524 | — | structure | yes | BELOW FLOOR |
| 2 | module-code | MISSING | `div#header` | `div#module-code` | `—` | 5 | 5 | 0.97 of 2524 | — | structure | yes | BELOW FLOOR |
| 3 | module-code | EXTRA | `div#module-code` | `—` | `h1` | 1 | 1 | 0.03 of 2524 | — | structure | yes | BELOW FLOOR |
| 4 | title | MISSING | `div#header` | `h1>span` | `—` | 278 | 129 | 0.24 of 2524 | subject+ptype=Online Safety (OS9000)/overview c=0.93 n=12 | 0.74 | yes | CANDIDATE |
| 5 | title | EXTRA | `div#header` | `—` | `h1>span` | 22 | 21 | 0.76 of 2524 | template=Standard c=0.81 n=16 | structure | yes | CANDIDATE |
| 6 | title | MISSING | `span>span.sassoonI-text` | `span.sassoonI-text` | `—` | 15 | 4 | 0.01 of 2524 | — | 0.80 | — | BELOW FLOOR |
| 7 | title | SUBSTITUTED | `div#header` | `h1>span` | `div#module-head-buttons` | 3 | 3 | 1.00 of 2524 | — | structure | yes | BELOW FLOOR |
| 8 | title | MISSING | `div#header` | `h1>span.ch-text` | `—` | 14 | 2 | 0.01 of 2524 | — | 0.00 | yes | BELOW FLOOR |
| 9 | title | MISSING | `span>span` | `span` | `—` | 6 | 2 | 0.01 of 2524 | — | 1.00 | — | BELOW FLOOR |
| 10 | title | SUBSTITUTED | `span` | `apan.jp-text` | `span.jp-text` | 10 | 1 | 0.00 of 2524 | — | structure | yes | BELOW FLOOR |
| 11 | title | SUBSTITUTED | `h1>span.ch-text` | `span.ch-text` | `span` | 7 | 1 | 0.01 of 2524 | — | structure | yes | BELOW FLOOR |
| 12 | title | MISSING | `div.titlebar` | `h1.moduleTitle>span.module-subtitle.text-lowercase` | `—` | 2 | 1 | 0.00 of 2524 | — | 1.00 | — | BELOW FLOOR |
| 13 | title | EXTRA | `span>span.ch-text` | `—` | `span.ch-text` | 1 | 1 | 1.00 of 2524 | — | structure | yes | BELOW FLOOR |
| 14 | title | EXTRA | `span>span.jp-text` | `—` | `span.jp-text` | 1 | 1 | 1.00 of 2524 | — | structure | yes | BELOW FLOOR |
| 15 | title | EXTRA | `h1>span` | `—` | `span` | 1 | 1 | 0.01 of 2524 | — | structure | — | BELOW FLOOR |
| 16 | title | EXTRA | `msub` | `—` | `mrow` | 1 | 1 | 1.00 of 2524 | — | structure | — | BELOW FLOOR |
| 17 | title | EXTRA | `mfrac` | `—` | `mrow` | 1 | 1 | 1.00 of 2524 | — | structure | — | BELOW FLOOR |
| 18 | title | EXTRA | `mrow` | `—` | `mi` | 1 | 1 | 1.00 of 2524 | — | structure | — | BELOW FLOOR |
| 19 | title | EXTRA | `msup` | `—` | `mrow` | 1 | 1 | 1.00 of 2524 | — | structure | — | BELOW FLOOR |
| 20 | title | MISSING | `span>span.ch-text` | `span.ch-text` | `—` | 1 | 1 | 0.00 of 2524 | — | 0.00 | yes | BELOW FLOOR |
| 21 | title | MISSING | `span>span.text-lowercase` | `span.text-lowercase` | `—` | 1 | 1 | 0.00 of 2524 | — | 1.00 | — | BELOW FLOOR |
| 22 | title | MISSING | `h1>span.jp-text` | `span.jp-text` | `—` | 1 | 1 | 0.00 of 2524 | — | 1.00 | yes | BELOW FLOOR |
| 23 | title | MISSING | `msup` | `mn` | `—` | 1 | 1 | 0.00 of 2524 | — | 1.00 | — | BELOW FLOOR |
| 24 | title | MISSING | `h1>span` | `span` | `—` | 1 | 1 | 0.98 of 2524 | — | 1.00 | — | BELOW FLOOR |
| 25 | title | SUBSTITUTED | `msub` | `mi` | `mrow` | 1 | 1 | 0.00 of 2524 | — | structure | — | BELOW FLOOR |
| 26 | title | SUBSTITUTED | `msub` | `mi` | `mi` | 1 | 1 | 0.00 of 2524 | — | structure | — | BELOW FLOOR |
| 27 | title | SUBSTITUTED | `mfrac` | `mn` | `mrow` | 1 | 1 | 0.00 of 2524 | — | structure | — | BELOW FLOOR |
| 28 | title | SUBSTITUTED | `mfrac` | `mn` | `mn` | 1 | 1 | 0.00 of 2524 | — | structure | — | BELOW FLOOR |
| 29 | title | SUBSTITUTED | `msup` | `mi` | `mrow` | 1 | 1 | 0.00 of 2524 | — | structure | — | BELOW FLOOR |
| 30 | title | SUBSTITUTED | `div#header` | `h1>span` | `div#module-code` | 1 | 1 | 1.00 of 2524 | — | structure | yes | BELOW FLOOR |
| 31 | header | MISSING | `div#header` | `p` | `—` | 3 | 1 | 0.00 of 2524 | — | 0.00 | yes | BELOW FLOOR |
| 32 | header | SUBSTITUTED | `div#header` | `div.titlebar` | `h1>span` | 2 | 1 | 0.00 of 2524 | — | structure | yes | BELOW FLOOR |
| 33 | header | SUBSTITUTED | `div#header` | `div#header` | `div#module-code` | 1 | 1 | 0.00 of 2524 | — | structure | yes | BELOW FLOOR |
| 34 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `p` | `h5` | 87 | 87 | 0.06 of 2524 | subject+ptype=1-10 Health and PE/overview c=0.82 n=14 | structure | yes | CANDIDATE |
| 35 | module-menu | MISSING | `ul` | `li` | `—` | 153 | 84 | 0.10 of 2524 | — | 0.87 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 36 | module-menu | EXTRA | `ul` | `—` | `li` | 85 | 47 | 0.78 of 2524 | ptype=lesson c=0.83 n=17 | structure | — | CANDIDATE |
| 37 | module-menu | MISSING | `div.col-12.col-md-8` | `p` | `—` | 211 | 45 | 0.09 of 2524 | — | 0.83 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 38 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-6.paddingR` | 87 | 44 | 0.97 of 2524 | template=Standard c=0.97 n=39 | structure | yes | CANDIDATE |
| 39 | module-menu | MISSING | `div.col-12.col-md-8` | `ul` | `—` | 166 | 43 | 0.28 of 2524 | — | 0.90 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 40 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingL` | `p` | `h5` | 43 | 43 | 0.03 of 2524 | subject+ptype=1-10 Health and PE/overview c=0.82 n=14 | structure | yes | CANDIDATE |
| 41 | module-menu | MISSING | `div.col-12.col-md-8` | `h5` | `—` | 177 | 41 | 0.24 of 2524 | subject+ptype=1-10 English/lesson c=0.65 n=13 | 0.86 | — | CANDIDATE |
| 42 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `p` | `—` | 58 | 38 | 0.04 of 2524 | subject+ptype=1-10 Blended Literacy/overview c=0.64 n=24 | 0.74 | yes | CANDIDATE |
| 43 | module-menu | EXTRA | `div#header` | `—` | `div#module-menu-content.moduleMenu` | 59 | 31 | 0.25 of 2524 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 44 | module-menu | EXTRA | `div#header` | `—` | `div#module-head-buttons` | 52 | 28 | 0.24 of 2524 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 45 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `h5` | 80 | 25 | 0.76 of 2524 | era=Refresh c=0.76 n=25 | structure | — | CANDIDATE |
| 46 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `ul` | `—` | 36 | 24 | 0.05 of 2524 | — | 0.82 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 47 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `p>b` | 23 | 23 | 1.00 of 2524 | era=Refresh c=1.00 n=23 | structure | yes | CANDIDATE |
| 48 | module-menu | SUBSTITUTED | `ul` | `li` | `li` | 105 | 22 | 0.57 of 2524 | template+ptype=Standard/lesson c=0.63 n=19 | structure | — | CANDIDATE |
| 49 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6.paddingL` | `—` | 37 | 22 | 0.04 of 2524 | — | 1.00 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 50 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `p` | `h5` | 27 | 21 | 0.04 of 2524 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 51 | module-menu | MISSING | `p` | `br` | `—` | 40 | 20 | 0.01 of 2524 | — | structure | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 52 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `p` | 20 | 20 | 0.96 of 2524 | template=Standard c=0.96 n=15 | structure | yes | CANDIDATE |
| 53 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `h4>span` | `—` | 20 | 20 | 0.02 of 2524 | — | 1.00 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 54 | module-menu | MOVED | `ul` | `li` | `li>i` | 31 | 19 | 0.22 of 2524 | — | structure | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 55 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `ul` | 45 | 18 | 0.72 of 2524 | era=Refresh c=0.72 n=18 | structure | — | CANDIDATE |
| 56 | module-menu | MISSING | `div#header` | `div#module-head-buttons` | `—` | 38 | 18 | 0.76 of 2524 | template=Standard c=0.78 n=10 | structure | yes | CANDIDATE |
| 57 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 36 | 18 | 0.88 of 2524 | era=Refresh c=0.88 n=18 | structure | — | CANDIDATE |
| 58 | module-menu | EXTRA | `div.col-12.col-md-6.offset-md-0` | `—` | `p` | 28 | 18 | 0.99 of 2524 | era=Refresh c=0.99 n=18 | structure | yes | CANDIDATE |
| 59 | module-menu | SUBSTITUTED | `div#module-menu-content.moduleMenu` | `WIDGET` | `div.row` | 18 | 18 | 0.01 of 2524 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 60 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `—` | 81 | 17 | 0.02 of 2524 | — | 0.95 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 61 | module-menu | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `h5` | 66 | 17 | 0.12 of 2524 | — | structure | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 62 | module-menu | EXTRA | `div.row` | `—` | `WIDGET` | 17 | 17 | 0.88 of 2524 | subject=1-10 Blended Literacy c=0.97 n=13 | structure | — | CANDIDATE |
| 63 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6.offset-md-0` | `—` | 63 | 16 | 0.04 of 2524 | — | 0.92 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 64 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `h4>span` | `h5>span` | 16 | 16 | 0.03 of 2524 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 65 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-8` | 103 | 15 | 0.67 of 2524 | subject=1-10 Mathematics c=0.77 n=12 | structure | — | CANDIDATE |
| 66 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `ul` | `p>b` | 15 | 15 | 0.06 of 2524 | subject+ptype=1-10 Blended Literacy/overview c=0.72 n=14 | structure | yes | CANDIDATE |
| 67 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-6.offset-md-0` | 30 | 14 | 0.95 of 2524 | era=Refresh c=0.95 n=14 | structure | yes | CANDIDATE |
| 68 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-12.paddingR` | 16 | 14 | 0.96 of 2524 | template=Standard c=0.96 n=14 | structure | yes | CANDIDATE |
| 69 | module-menu | MISSING | `div#module-menu-content.moduleMenu` | `ul` | `—` | 94 | 13 | 0.04 of 2524 | — | 0.90 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 70 | module-menu | SUBSTITUTED | `div#module-menu-content.moduleMenu` | `h5` | `div.row` | 88 | 13 | 0.04 of 2524 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 71 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `h5` | 15 | 13 | 0.99 of 2524 | ptype=overview c=1.00 n=11 | structure | yes | CANDIDATE |
| 72 | module-menu | EXTRA | `div.col-12.col-md-6.paddingL` | `—` | `h5` | 13 | 13 | 1.00 of 2524 | era=Refresh c=1.00 n=13 | structure | yes | CANDIDATE |
| 73 | module-menu | SUBSTITUTED | `div#module-menu-content.moduleMenu` | `div.item` | `div.row` | 87 | 12 | 0.03 of 2524 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 74 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `h5` | 27 | 12 | 0.04 of 2524 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 75 | module-menu | MISSING | `div.item` | `p>b` | `—` | 23 | 12 | 0.01 of 2524 | — | 0.58 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 76 | module-menu | EXTRA | `p>b` | `—` | `b` | 12 | 12 | 0.99 of 2524 | ptype=overview c=0.99 n=10 | structure | — | CANDIDATE |
| 77 | module-menu | EXTRA | `div.col-12.col-md-6.paddingL` | `—` | `p` | 12 | 12 | 1.00 of 2524 | era=Refresh c=1.00 n=12 | structure | yes | CANDIDATE |
| 78 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6.offset-md-0.paddingL` | `—` | 12 | 12 | 0.01 of 2524 | — | 0.33 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 79 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.paddingR` | `div.col-12.col-md-12.paddingR` | 12 | 12 | 0.07 of 2524 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 80 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.paddingL` | `div.col-12.col-md-6.paddingR` | 12 | 12 | 0.04 of 2524 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 81 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0` | `ul` | `—` | 60 | 11 | 0.02 of 2524 | — | 0.87 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 82 | module-menu | MOVED | `ul` | `li` | `li` | 39 | 11 | 0.35 of 2524 | — | structure | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 83 | module-menu | EXTRA | `li>b` | `—` | `b` | 24 | 11 | 1.00 of 2524 | ptype=lesson c=1.00 n=10 | structure | — | CANDIDATE |
| 84 | module-menu | MISSING | `div.item` | `ul` | `—` | 40 | 10 | 0.01 of 2524 | — | 1.00 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 85 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `h5>span` | `—` | 10 | 10 | 0.03 of 2524 | — | 1.00 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 86 | module-menu | MISSING | `h5>span` | `span` | `—` | 10 | 10 | 0.03 of 2524 | subject+ptype=1-10 Blended Literacy/overview c=0.68 n=10 | 1.00 | — | CANDIDATE |
| 87 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-8.paddingR` | `div.col-12.col-md-8` | 71 | 9 | 0.03 of 2524 | — | structure | yes | BELOW FLOOR |
| 88 | module-menu | MISSING | `div#module-menu-content.moduleMenu` | `h5` | `—` | 51 | 9 | 0.04 of 2524 | — | 0.74 | yes | BELOW FLOOR |
| 89 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0` | `p` | `—` | 42 | 9 | 0.01 of 2524 | — | 0.71 | yes | BELOW FLOOR |
| 90 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `h5>span` | 9 | 9 | 0.97 of 2524 | — | structure | yes | BELOW FLOOR |
| 91 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-6.paddingL` | 9 | 9 | 0.96 of 2524 | — | structure | yes | BELOW FLOOR |
| 92 | module-menu | EXTRA | `div.col-12.col-md-6.paddingL` | `—` | `ul` | 9 | 9 | 0.99 of 2524 | — | structure | yes | BELOW FLOOR |
| 93 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0.paddingR` | `h5` | `—` | 9 | 9 | 0.01 of 2524 | — | 0.00 | yes | BELOW FLOOR |
| 94 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.offset-md-0.paddingR` | `div.col-12.col-md-8` | 9 | 9 | 0.01 of 2524 | — | structure | yes | BELOW FLOOR |
| 95 | module-menu | SUBSTITUTED | `div.col-12.col-md-6` | `h4>span` | `h5>span` | 9 | 9 | 0.01 of 2524 | — | structure | yes | BELOW FLOOR |
| 96 | module-menu | MISSING | `div.item` | `p` | `—` | 18 | 8 | 0.01 of 2524 | — | 0.65 | yes | BELOW FLOOR |
| 97 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `h4>span` | 17 | 8 | 0.04 of 2524 | — | structure | yes | BELOW FLOOR |
| 98 | module-menu | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `ul` | 15 | 8 | 0.12 of 2524 | — | structure | — | BELOW FLOOR |
| 99 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `ul` | 8 | 8 | 1.00 of 2524 | — | structure | yes | BELOW FLOOR |
| 100 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0.paddingR` | `p` | `h5` | 8 | 8 | 0.01 of 2524 | — | structure | yes | BELOW FLOOR |
| 418 | crumbs | MISSING | `div.crumbs` | `div` | `—` | 15 | 12 | 0.02 of 2517 | template+ptype=Inquiry/overview c=0.62 n=10 | 0.92 | yes | CANDIDATE |
| 434 | footer | MISSING | `ul.footer-nav` | `li>a#next-lesson` | `—` | 101 | 61 | 0.71 of 2524 | subject+ptype=1-10 Mathematics/overview c=0.93 n=12 | structure | yes | CANDIDATE |
| 435 | footer | MISSING | `ul.footer-nav` | `li>a.home-nav` | `—` | 100 | 55 | 0.83 of 2524 | subject=1-10 English c=1.00 n=13 | structure | yes | CANDIDATE |
| 436 | footer | MISSING | `ul.footer-nav.inquiry-nav` | `li>a.home-nav` | `—` | 55 | 50 | 0.14 of 2524 | subject+ptype=1-10 Blended Literacy/overview c=0.89 n=24 | structure | yes | CANDIDATE |
| 437 | footer | MISSING | `li>a#next-lesson` | `a#next-lesson` | `—` | 49 | 49 | 0.82 of 2524 | template=Bilingual c=0.88 n=10 | structure | yes | CANDIDATE |
| 438 | footer | EXTRA | `ul.footer-nav.inquiry-nav` | `—` | `li>a.home-nav` | 31 | 31 | 0.86 of 2524 | era=Refresh c=0.86 n=31 | structure | yes | CANDIDATE |
| 442 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav.inquiry-nav` | `li>a#next-lesson` | 22 | 22 | 0.14 of 2524 | subject+ptype=1-10 Blended Literacy/overview c=0.89 n=15 | structure | yes | CANDIDATE |
| 443 | footer | MISSING | `ul.footer-nav` | `li>a#prev-lesson` | `—` | 37 | 20 | 0.70 of 2524 | ptype=lesson c=0.88 n=15 | structure | yes | CANDIDATE |
| 444 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` | `li>a#next-lesson` | `li>a.home-nav` | 18 | 18 | 0.10 of 2524 | subject+ptype=1-10 Blended Literacy/overview c=0.87 n=15 | structure | yes | CANDIDATE |
| 445 | footer | EXTRA | `div#footer` | `—` | `ul.footer-nav.inquiry-nav` | 19 | 16 | 0.86 of 2524 | template=Standard c=0.86 n=13 | structure | yes | CANDIDATE |
| 446 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav` | `ul.footer-nav` | 17 | 16 | 0.83 of 2524 | template=Standard c=0.85 n=15 | structure | yes | CANDIDATE |
| 447 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav` | `ul.footer-nav.inquiry-nav` | 52 | 15 | 0.83 of 2524 | ptype=lesson c=0.88 n=14 | structure | yes | CANDIDATE |
| 449 | footer | MISSING | `li>a.home-nav` | `a.home-nav` | `—` | 24 | 13 | 0.99 of 2524 | era=Refresh c=0.99 n=13 | structure | yes | CANDIDATE |
| 450 | footer | EXTRA | `ul.footer-nav.fundamentals-nav` | `—` | `li>a.home-nav` | 21 | 12 | 0.98 of 2524 | era=Refresh c=0.98 n=12 | structure | yes | CANDIDATE |
| 454 | footer | MISSING | `ul.footer-nav.inquiry-nav` | `li>a#prev-lesson` | `—` | 11 | 11 | 0.10 of 2524 | template+ptype=Inquiry/overview c=0.70 n=10 | structure | yes | CANDIDATE |
| 455 | footer | SUBSTITUTED | `ul.footer-nav` | `li>a#next-lesson` | `li>a.home-nav` | 11 | 11 | 0.71 of 2524 | template=Standard c=0.75 n=11 | structure | yes | CANDIDATE |
| 456 | footer | SUBSTITUTED | `ul.footer-nav` | `li>a.home-nav` | `li>a.home-nav` | 12 | 10 | 0.83 of 2524 | era=Refresh c=0.83 n=10 | structure | yes | CANDIDATE |
| 457 | footer | MISSING | `div#footer` | `ul.footer-nav` | `—` | 11 | 10 | 0.83 of 2524 | era=Refresh c=0.83 n=10 | structure | yes | CANDIDATE |
| 458 | footer | SUBSTITUTED | `ul.footer-nav` | `li>a#next-lesson` | `li>a#next-lesson` | 11 | 10 | 0.71 of 2524 | era=Refresh c=0.71 n=10 | structure | yes | CANDIDATE |
| 542 | acks | SUBSTITUTED | `div.col-12.col-md-8` | `div.acks` | `div.acks.acksTemplate` | 105 | 105 | 0.16 of 2524 | template+ptype=Inquiry/overview c=0.82 n=41 | structure | yes | CANDIDATE |
| 572 | activity | MISSING | `div.col-12` | `p` | `—` | 777 | 378 | 0.29 of 2517 | template+ptype=Inquiry/overview c=0.80 n=40 | 0.81 | — | CANDIDATE |
| 573 | activity | EXTRA | `div.col-12` | `—` | `p` | 612 | 305 | 0.88 of 2517 | subject=ANZH c=0.99 n=24 | structure | — | CANDIDATE |
| 574 | activity | MISSING | `div.col-12` | `WIDGET` | `—` | 425 | 263 | 0.18 of 2517 | template+ptype=Inquiry/overview c=0.67 n=27 | structure | — | CANDIDATE |
| 576 | activity | MISSING | `div.col-12` | `a` | `—` | 458 | 235 | 0.29 of 2517 | template+ptype=Inquiry/overview c=0.75 n=27 | 0.65 | — | CANDIDATE |
| 577 | activity | MOVED | `div.col-12` | `p` | `p` | 326 | 216 | 0.19 of 2517 | template+ptype=Inquiry/overview c=0.77 n=25 | structure | — | CANDIDATE |
| 578 | activity | EXTRA | `div.col-12` | `—` | `WIDGET` | 349 | 213 | 0.82 of 2517 | subject=NCEA1 c=0.95 n=38 | structure | — | CANDIDATE |
| 579 | activity | MISSING | `div.col-12` | `h3` | `—` | 402 | 199 | 0.30 of 2517 | template+ptype=Fundamentals/overview c=0.85 n=31 | 0.71 | — | CANDIDATE |
| 580 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `div.activity[number=*]` | 280 | 193 | 0.43 of 2517 | template=Fundamentals c=0.77 n=20 | structure | yes | CANDIDATE |
| 581 | activity | MISSING | `div.activity.interactive[number=*]` | `div.row` | `—` | 293 | 172 | 0.12 of 2517 | template+ptype=Fundamentals/overview c=0.65 n=35 | 0.93 | yes | CANDIDATE |
| 582 | activity | MISSING | `div.col-12` | `div.row` | `—` | 237 | 172 | 0.20 of 2517 | template+ptype=Bilingual/lesson c=0.61 n=21 | 0.96 | — | CANDIDATE |
| 583 | activity | EXTRA | `div.col-12` | `—` | `img.img-fluid` | 259 | 156 | 0.97 of 2517 | subject+ptype=1-10 English/lesson c=0.99 n=22 | structure | — | CANDIDATE |
| 584 | activity | MOVED | `div.col-12` | `p` | `p` | 164 | 130 | 0.15 of 2517 | template+ptype=Inquiry/overview c=0.77 n=21 | structure | — | CANDIDATE |
| 585 | activity | EXTRA | `div.row` | `—` | `div.col-12` | 167 | 122 | 0.90 of 2517 | template=Standard c=0.93 n=136 | structure | — | CANDIDATE |
| 586 | activity | EXTRA | `div.col-12` | `—` | `p>a` | 138 | 116 | 1.00 of 2517 | subject+ptype=1-10 Blended Literacy/lesson c=1.00 n=37 | structure | — | CANDIDATE |
| 592 | activity | EXTRA | `div.activity[number=*]` | `—` | `div.row` | 149 | 104 | 0.94 of 2517 | subject=1-10 English c=0.98 n=22 | structure | yes | CANDIDATE |
| 594 | activity | SUBSTITUTED | `div.col-12` | `p` | `p` | 135 | 99 | 0.75 of 2517 | subject+ptype=1-10 Blended Literacy/lesson c=0.92 n=21 | structure | — | CANDIDATE |
| 596 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `div.activity.interactive[number=*]` | 125 | 92 | 0.47 of 2517 | subject+ptype=1-10 Blended Literacy/lesson c=0.81 n=24 | structure | yes | CANDIDATE |
| 597 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `div.activity[number=*]` | 124 | 90 | 0.47 of 2517 | subject+ptype=1-10 Mathematics/lesson c=0.66 n=21 | structure | yes | CANDIDATE |
| 599 | activity | EXTRA | `div.col-12` | `—` | `ol` | 130 | 85 | 0.96 of 2517 | subject=1-10 Mathematics c=0.98 n=31 | structure | — | CANDIDATE |
| 600 | activity | EXTRA | `div.col-12` | `—` | `p>b` | 128 | 85 | 0.97 of 2517 | template=Standard c=0.98 n=88 | structure | — | CANDIDATE |
| 601 | activity | EXTRA | `p>b` | `—` | `b` | 113 | 85 | 0.92 of 2517 | template=Standard c=0.94 n=72 | structure | — | CANDIDATE |
| 603 | activity | EXTRA | `div.col-12` | `—` | `h3` | 103 | 82 | 0.87 of 2517 | template=Standard c=0.92 n=67 | structure | — | CANDIDATE |
| 604 | activity | EXTRA | `div.col-12` | `—` | `ul` | 106 | 81 | 0.94 of 2517 | template=Standard c=0.96 n=87 | structure | — | CANDIDATE |
| 606 | activity | EXTRA | `p>a` | `—` | `a` | 91 | 77 | 0.98 of 2517 | subject+ptype=1-10 Blended Literacy/lesson c=1.00 n=32 | structure | — | CANDIDATE |
| 609 | activity | EXTRA | `div.activity.interactive[number=*]` | `—` | `div.row` | 91 | 73 | 0.79 of 2517 | template=Standard c=0.83 n=71 | structure | yes | CANDIDATE |
| 610 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `p` | 88 | 72 | 0.59 of 2517 | subject+ptype=1-10 Mathematics/lesson c=0.77 n=28 | structure | — | CANDIDATE |
| 612 | activity | EXTRA | `div.col-12` | `—` | `a` | 85 | 69 | 0.71 of 2517 | template=Standard c=0.73 n=67 | structure | — | CANDIDATE |
| 615 | activity | EXTRA | `div.col-12` | `—` | `h4.goJournal` | 149 | 66 | 0.95 of 2517 | series=HIS10 c=1.00 n=27 | structure | — | CANDIDATE |
| 616 | activity | MOVED | `div.col-12` | `h3` | `h3` | 96 | 66 | 0.21 of 2517 | template+ptype=Bilingual/lesson c=0.76 n=24 | structure | — | CANDIDATE |
| 620 | activity | SUBSTITUTED | `div.col-12` | `p` | `WIDGET` | 69 | 62 | 0.75 of 2517 | template+ptype=Standard/lesson c=0.88 n=53 | structure | — | CANDIDATE |
| 621 | activity | SUBSTITUTED | `div.col-12` | `a` | `h4.goJournal` | 141 | 61 | 0.55 of 2517 | series=HIS10 c=0.83 n=25 | structure | — | CANDIDATE |
| 625 | activity | EXTRA | `ol` | `—` | `li` | 74 | 56 | 0.96 of 2517 | template=Standard c=0.97 n=57 | structure | — | CANDIDATE |
| 626 | activity | EXTRA | `a` | `—` | `div.button` | 72 | 56 | 0.77 of 2517 | template=Standard c=0.79 n=51 | structure | yes | CANDIDATE |
| 628 | activity | SUBSTITUTED | `div.col-12` | `a` | `p` | 79 | 53 | 0.55 of 2517 | subject+ptype=1-10 Mathematics/lesson c=0.80 n=23 | structure | — | CANDIDATE |
| 630 | activity | EXTRA | `div.col-12.col-md-8` | `—` | `div.activity[number=*]` | 58 | 52 | 0.96 of 2517 | template=Standard c=0.98 n=44 | structure | yes | CANDIDATE |
| 634 | activity | EXTRA | `div.col-12` | `—` | `p>i` | 56 | 50 | 0.98 of 2517 | template=Standard c=0.98 n=47 | structure | — | CANDIDATE |
| 640 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `div.row` | 45 | 45 | 0.59 of 2517 | ptype=lesson c=0.68 n=34 | structure | — | CANDIDATE |
| 645 | activity | EXTRA | `p>i` | `—` | `i` | 51 | 42 | 0.89 of 2517 | template=Standard c=0.90 n=45 | structure | — | CANDIDATE |
| 657 | activity | SUBSTITUTED | `div.col-12` | `a` | `WIDGET` | 46 | 39 | 0.55 of 2517 | template+ptype=Standard/lesson c=0.65 n=43 | structure | — | CANDIDATE |
| 659 | activity | EXTRA | `a` | `—` | `div.externalButton` | 50 | 38 | 0.92 of 2517 | template=Standard c=0.92 n=37 | structure | — | CANDIDATE |
| 660 | activity | EXTRA | `div.col-12` | `—` | `div.icon.ratio.ratio-16x9.videoSection` | 49 | 37 | 0.98 of 2517 | template=Standard c=0.98 n=41 | structure | yes | CANDIDATE |
| 661 | activity | EXTRA | `p` | `—` | `b` | 45 | 37 | 0.96 of 2517 | template=Standard c=0.96 n=38 | structure | — | CANDIDATE |
| 662 | activity | SUBSTITUTED | `div.col-12` | `h3` | `WIDGET` | 45 | 37 | 0.76 of 2517 | template+ptype=Standard/lesson c=0.89 n=33 | structure | — | CANDIDATE |
| 667 | activity | EXTRA | `ul` | `—` | `li` | 35 | 34 | 0.93 of 2517 | template=Standard c=0.95 n=28 | structure | — | CANDIDATE |
| 668 | activity | EXTRA | `div.col-12` | `—` | `audio.audioPlayer.icon` | 55 | 33 | 1.00 of 2517 | template=Bilingual c=1.00 n=27 | structure | yes | CANDIDATE |
| 673 | activity | EXTRA | `div.col-12.col-md-8` | `—` | `div.activity.interactive[number=*]` | 34 | 32 | 0.89 of 2517 | template=Standard c=0.92 n=27 | structure | yes | CANDIDATE |
| 682 | activity | EXTRA | `div.col-12` | `—` | `div.ratio.ratio-16x9.videoSection` | 40 | 28 | 0.99 of 2517 | template=Standard c=0.99 n=27 | structure | yes | CANDIDATE |
| 684 | activity | SUBSTITUTED | `div.row` | `div.col-12` | `WIDGET` | 29 | 28 | 0.78 of 2517 | ptype=lesson c=0.92 n=21 | structure | — | CANDIDATE |
| 695 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `ol` | 27 | 24 | 0.59 of 2517 | ptype=lesson c=0.68 n=22 | structure | — | CANDIDATE |
| 696 | activity | EXTRA | `div.icon.ratio.ratio-16x9.videoSection` | `—` | `iframe` | 26 | 24 | 0.99 of 2517 | era=Refresh c=0.99 n=26 | structure | yes | CANDIDATE |
| 699 | activity | EXTRA | `div.col-12` | `—` | `h5` | 27 | 23 | 0.99 of 2517 | template=Standard c=0.99 n=21 | structure | — | CANDIDATE |
| 702 | activity | SUBSTITUTED | `div.activity.interactive[number=*]` | `div.row` | `WIDGET` | 26 | 23 | 0.54 of 2517 | ptype=lesson c=0.62 n=21 | structure | yes | CANDIDATE |
| 707 | activity | SUBSTITUTED | `div.row` | `div.col-12` | `div.row` | 24 | 22 | 0.78 of 2517 | era=Refresh c=0.78 n=24 | structure | — | CANDIDATE |
| 708 | activity | SUBSTITUTED | `div.row` | `div.col-12` | `div.col-12.col-md-8` | 24 | 22 | 0.78 of 2517 | era=Refresh c=0.78 n=24 | structure | — | CANDIDATE |
| 721 | activity | EXTRA | `div.ratio.ratio-16x9.videoSection` | `—` | `iframe` | 26 | 20 | 0.98 of 2517 | template=Standard c=0.98 n=22 | structure | yes | CANDIDATE |
| 734 | activity | EXTRA | `div.col-12` | `—` | `div.TKmodal` | 23 | 18 | 1.00 of 2517 | era=Refresh c=1.00 n=23 | structure | — | CANDIDATE |
| 739 | activity | EXTRA | `div.col-12` | `—` | `div.button` | 34 | 17 | 1.00 of 2517 | template=Standard c=1.00 n=30 | structure | yes | CANDIDATE |
| 740 | activity | SUBSTITUTED | `div.col-12` | `p` | `p>b` | 25 | 17 | 0.75 of 2517 | ptype=lesson c=0.88 n=23 | structure | — | CANDIDATE |
| 742 | activity | SUBSTITUTED | `div.col-12` | `h3` | `h3` | 24 | 17 | 0.76 of 2517 | template+ptype=Standard/lesson c=0.89 n=20 | structure | — | CANDIDATE |
| 750 | activity | SUBSTITUTED | `div.col-12` | `p` | `h4.goJournal` | 26 | 16 | 0.75 of 2517 | template+ptype=Standard/lesson c=0.88 n=24 | structure | — | CANDIDATE |
| 844 | activity | MISSING | `div.col-12.col-md-8` | `div.activity.dropbox[number=*]` | `—` | 24 | 9 | 0.03 of 2517 | series=XDLS90 c=0.68 n=20 | 1.00 | yes | CANDIDATE |
| 1082 | activity | EXTRA | `div.activity.clickDropContent.dropbox[nu` | `—` | `a` | 23 | 4 | 1.00 of 2517 | era=Refresh c=1.00 n=23 | structure | yes | CANDIDATE |
| 1083 | activity | EXTRA | `div.activity.dropbox[number=*]` | `—` | `a` | 21 | 4 | 0.99 of 2517 | era=Refresh c=0.99 n=21 | structure | yes | CANDIDATE |
| 4057 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 1130 | 419 | 0.82 of 2517 | series=DAN10 c=1.00 n=20 | structure | — | CANDIDATE |
| 4058 | body | EXTRA | `div#body` | `—` | `div.row` | 1447 | 391 | 0.67 of 2517 | subject+ptype=1-10 Blended Literacy/overview c=1.00 n=30 | structure | — | CANDIDATE |
| 4059 | body | MISSING | `div#body` | `div.row` | `—` | 1410 | 353 | 0.33 of 2517 | series=CEDO50 c=0.76 n=20 | 0.86 | — | CANDIDATE |
| 4060 | body | MISSING | `div.col-12.col-md-8` | `p` | `—` | 616 | 296 | 0.25 of 2517 | template+ptype=Fundamentals/overview c=0.91 n=46 | 0.80 | — | CANDIDATE |
| 4061 | body | EXTRA | `div.col-12.col-md-8` | `—` | `img.img-fluid` | 568 | 256 | 0.96 of 2517 | template+ptype=Standard/overview c=1.00 n=27 | structure | — | CANDIDATE |
| 4062 | body | EXTRA | `div.col-12.col-md-8` | `—` | `WIDGET` | 400 | 245 | 0.93 of 2517 | subject+ptype=NCEA1/lesson c=0.99 n=48 | structure | — | CANDIDATE |
| 4063 | body | MOVED | `div.col-12.col-md-8` | `p` | `p` | 358 | 224 | 0.16 of 2517 | template+ptype=Fundamentals/overview c=0.83 n=43 | structure | — | CANDIDATE |
| 4064 | body | EXTRA | `div.row` | `—` | `div.col-12.col-md-8` | 299 | 212 | 0.85 of 2517 | subject+ptype=1-10 Blended Literacy/lesson c=0.97 n=24 | structure | — | CANDIDATE |
| 4065 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p>b` | 346 | 209 | 0.97 of 2517 | subject=1-10 Blended Literacy c=1.00 n=46 | structure | — | CANDIDATE |
| 4066 | body | SUBSTITUTED | `div.row` | `div.col-12` | `div.col-12.col-md-8` | 335 | 193 | 0.54 of 2517 | subject+ptype=1-10 Blended Literacy/overview c=0.96 n=67 | structure | — | CANDIDATE |
| 4067 | body | EXTRA | `div.col-12.col-md-8` | `—` | `h3` | 314 | 186 | 0.89 of 2517 | subject+ptype=1-10 Blended Literacy/overview c=1.00 n=20 | structure | — | CANDIDATE |
| 4068 | body | EXTRA | `div.col-12.col-md-8` | `—` | `ul` | 309 | 184 | 0.95 of 2517 | subject=1-10 Mathematics c=0.98 n=21 | structure | — | CANDIDATE |
| 4070 | body | MISSING | `div.col-12.col-md-8` | `WIDGET` | `—` | 273 | 178 | 0.19 of 2517 | template+ptype=Fundamentals/overview c=0.65 n=32 | structure | — | CANDIDATE |
| 4071 | body | MISSING | `div.row` | `div.col-12.col-md-8` | `—` | 318 | 173 | 0.28 of 2517 | template=Fundamentals c=0.78 n=22 | 0.94 | — | CANDIDATE |
| 4073 | body | EXTRA | `div.col-12.col-md-8` | `—` | `a` | 227 | 154 | 0.98 of 2517 | subject+ptype=ConnectED/lesson c=1.00 n=25 | structure | — | CANDIDATE |
| 4074 | body | MISSING | `div.col-12.col-md-8` | `h3` | `—` | 246 | 152 | 0.18 of 2517 | template+ptype=Fundamentals/overview c=0.75 n=21 | 0.90 | — | CANDIDATE |
| 4076 | body | EXTRA | `p>b` | `—` | `b` | 194 | 129 | 0.93 of 2517 | subject=1-10 Mathematics c=0.97 n=31 | structure | — | CANDIDATE |
| 4078 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p>a` | 178 | 122 | 0.99 of 2517 | subject=1-10 English c=1.00 n=20 | structure | — | CANDIDATE |
| 4079 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.table-responsive` | 169 | 120 | 0.92 of 2517 | ptype=overview c=0.95 n=21 | structure | — | CANDIDATE |
| 4080 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.ratio.ratio-16x9.videoSection` | 189 | 119 | 0.93 of 2517 | subject=NCEA1 c=0.98 n=23 | structure | yes | CANDIDATE |
| 4090 | body | EXTRA | `p` | `—` | `b` | 124 | 96 | 0.93 of 2517 | subject=NCEA1 c=0.96 n=30 | structure | — | CANDIDATE |
| 4091 | body | EXTRA | `div.table-responsive` | `—` | `table.table.table-bordered` | 145 | 95 | 0.96 of 2517 | subject=NCEA1 c=0.97 n=30 | structure | yes | CANDIDATE |
| 4092 | body | MOVED | `div.col-12.col-md-8` | `p` | `p` | 131 | 95 | 0.18 of 2517 | template+ptype=Inquiry/overview c=0.62 n=20 | structure | — | CANDIDATE |
| 4094 | body | EXTRA | `a` | `—` | `div.button` | 151 | 91 | 0.97 of 2517 | subject=NCEA1 c=0.98 n=25 | structure | — | CANDIDATE |
| 4097 | body | EXTRA | `div.col-12.col-md-8` | `—` | `ol` | 111 | 84 | 0.99 of 2517 | template=Standard c=0.99 n=87 | structure | — | CANDIDATE |
| 4098 | body | EXTRA | `p>i` | `—` | `i` | 110 | 84 | 0.97 of 2517 | subject+ptype=1-10 Blended Literacy/overview c=1.00 n=26 | structure | — | CANDIDATE |
| 4100 | body | SUBSTITUTED | `div.icon.ratio.ratio-16x9.videoSection` | `iframe.embed-responsive-item` | `iframe` | 217 | 81 | 0.19 of 2517 | series=PES10 c=0.67 n=37 | structure | yes | CANDIDATE |
| 4102 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p>i` | 108 | 78 | 0.98 of 2517 | subject=NCEA1 c=0.99 n=30 | structure | — | CANDIDATE |
| 4103 | body | EXTRA | `p>a` | `—` | `a` | 105 | 78 | 0.99 of 2517 | template=Standard c=1.00 n=81 | structure | — | CANDIDATE |
| 4104 | body | EXTRA | `div.col-12.col-md-8` | `—` | `audio.audioPlayer.icon` | 133 | 77 | 1.00 of 2517 | ptype=overview c=1.00 n=35 | structure | yes | CANDIDATE |
| 4105 | body | EXTRA | `div.row` | `—` | `div.col-12` | 140 | 75 | 0.71 of 2517 | subject=ANZH c=0.75 n=22 | structure | — | CANDIDATE |
| 4106 | body | SUBSTITUTED | `div#body` | `div.row` | `WIDGET` | 123 | 75 | 0.94 of 2517 | subject=Online Safety (OS9000) c=1.00 n=27 | structure | — | CANDIDATE |
| 4108 | body | MOVED | `div.col-12.col-md-8` | `h3` | `h3` | 89 | 74 | 0.11 of 2517 | template+ptype=Fundamentals/overview c=0.67 n=24 | structure | — | CANDIDATE |
| 4112 | body | EXTRA | `table.table.table-bordered` | `—` | `tr` | 99 | 70 | 0.98 of 2517 | template=Standard c=0.98 n=85 | structure | yes | CANDIDATE |
| 4115 | body | EXTRA | `div.fundamentalsPanel` | `—` | `div.row` | 74 | 69 | 0.99 of 2517 | era=Refresh c=0.99 n=74 | structure | — | CANDIDATE |
| 4123 | body | EXTRA | `a` | `—` | `div.externalButton` | 91 | 66 | 0.93 of 2517 | template=Standard c=0.93 n=78 | structure | — | CANDIDATE |
| 4125 | body | EXTRA | `div.col-12` | `—` | `p` | 101 | 64 | 0.92 of 2517 | template=Standard c=0.94 n=84 | structure | — | CANDIDATE |
| 4126 | body | EXTRA | `div.col-12.col-md-8` | `—` | `h4` | 76 | 64 | 0.97 of 2517 | template=Standard c=0.98 n=37 | structure | — | CANDIDATE |
| 4130 | body | EXTRA | `ul` | `—` | `li` | 70 | 60 | 0.95 of 2517 | template=Standard c=0.96 n=49 | structure | — | CANDIDATE |
| 4131 | body | EXTRA | `div.ratio.ratio-16x9.videoSection` | `—` | `iframe` | 75 | 59 | 0.92 of 2517 | template=Standard c=0.94 n=57 | structure | yes | CANDIDATE |
| 4132 | body | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `div.col-12.col-md-8` | 65 | 57 | 0.98 of 2517 | ptype=lesson c=0.99 n=39 | structure | — | CANDIDATE |
| 4134 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `p` | 71 | 54 | 0.84 of 2517 | template+ptype=Standard/lesson c=0.84 n=50 | structure | — | CANDIDATE |
| 4135 | body | EXTRA | `div.alert` | `—` | `div.row` | 66 | 54 | 0.91 of 2517 | template=Standard c=0.92 n=47 | structure | — | CANDIDATE |
| 4137 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.alert` | 67 | 53 | 0.90 of 2517 | template=Standard c=0.91 n=51 | structure | — | CANDIDATE |
| 4138 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `div.activity[number=*]` | 59 | 53 | 0.84 of 2517 | template+ptype=Standard/lesson c=0.84 n=51 | structure | yes | CANDIDATE |
| 4143 | body | EXTRA | `tr` | `—` | `td` | 58 | 49 | 0.94 of 2517 | template=Standard c=0.95 n=52 | structure | — | CANDIDATE |
| 4147 | body | EXTRA | `div.inquiryPanel` | `—` | `div.row` | 49 | 48 | 0.99 of 2517 | era=Refresh c=0.99 n=49 | structure | — | CANDIDATE |
| 4149 | body | EXTRA | `div.col-12.col-md-8` | `—` | `h4.goJournal` | 62 | 47 | 1.00 of 2517 | subject=NCEA1 c=1.00 n=23 | structure | — | CANDIDATE |
| 4152 | body | EXTRA | `div.row` | `—` | `div.col-12.col-md-6` | 70 | 46 | 0.99 of 2517 | subject=Online Safety (OS9000) c=1.00 n=25 | structure | — | CANDIDATE |
| 4155 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.icon.ratio.ratio-16x9.videoSection` | 62 | 44 | 0.92 of 2517 | template=Standard c=0.93 n=54 | structure | yes | CANDIDATE |
| 4158 | body | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `WIDGET` | 46 | 43 | 0.98 of 2517 | ptype=lesson c=0.99 n=38 | structure | — | CANDIDATE |
| 4159 | body | EXTRA | `div#body` | `—` | `WIDGET` | 82 | 42 | 0.93 of 2517 | template=Bilingual c=0.97 n=21 | structure | — | CANDIDATE |
| 4162 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `WIDGET` | 42 | 41 | 0.84 of 2517 | template+ptype=Standard/lesson c=0.84 n=25 | structure | — | CANDIDATE |
| 4164 | body | EXTRA | `div.alert.solid` | `—` | `div.row` | 49 | 39 | 0.99 of 2517 | template=Standard c=0.99 n=40 | structure | yes | CANDIDATE |
| 4165 | body | MISSING | `div#body` | `div.fundamentalsPanel` | `—` | 45 | 39 | 0.02 of 2517 | template+ptype=Fundamentals/overview c=0.60 n=38 | 0.98 | yes | CANDIDATE |
| 4166 | body | EXTRA | `p` | `—` | `i` | 44 | 39 | 0.96 of 2517 | template=Standard c=0.97 n=40 | structure | — | CANDIDATE |
| 4172 | body | EXTRA | `div.col-12.col-md-8` | `—` | `h5` | 45 | 37 | 0.99 of 2517 | template=Standard c=0.99 n=28 | structure | — | CANDIDATE |
| 4173 | body | EXTRA | `div#body` | `—` | `div.row.supervisor` | 46 | 36 | 0.90 of 2517 | ptype=lesson c=0.91 n=39 | structure | yes | CANDIDATE |
| 4175 | body | MISSING | `div#body` | `div.inquiryPanel` | `—` | 39 | 36 | 0.02 of 2517 | template+ptype=Inquiry/overview c=0.62 n=34 | 0.92 | — | CANDIDATE |
| 4178 | body | EXTRA | `tr` | `—` | `th` | 38 | 34 | 0.99 of 2517 | template=Standard c=1.00 n=33 | structure | — | CANDIDATE |
| 4179 | body | EXTRA | `div.row` | `—` | `div.col-12.col-md-4.offset-md-0` | 34 | 34 | 0.80 of 2517 | template=Standard c=0.81 n=20 | structure | — | CANDIDATE |
| 4184 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p>span.infoTrigger` | 36 | 32 | 0.87 of 2517 | template=Standard c=0.87 n=30 | structure | — | CANDIDATE |
| 4187 | body | EXTRA | `div#body` | `—` | `div.fundamentalsPanel` | 38 | 31 | 0.98 of 2517 | era=Refresh c=0.98 n=38 | structure | yes | CANDIDATE |
| 4191 | body | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `div.row` | 32 | 31 | 0.98 of 2517 | era=Refresh c=0.98 n=32 | structure | — | CANDIDATE |
| 4192 | body | EXTRA | `div#body` | `—` | `div.inquiryPanel` | 31 | 31 | 0.98 of 2517 | era=Refresh c=0.98 n=31 | structure | — | CANDIDATE |
| 4196 | body | EXTRA | `div.introduction` | `—` | `div.row` | 30 | 30 | 0.99 of 2517 | era=Refresh c=0.99 n=30 | structure | — | CANDIDATE |
| 4199 | body | EXTRA | `div.icon.ratio.ratio-16x9.videoSection` | `—` | `iframe` | 38 | 29 | 0.97 of 2517 | template=Standard c=0.98 n=33 | structure | yes | CANDIDATE |
| 4202 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.flipCardsContainer.row` | 33 | 29 | 0.93 of 2517 | template=Standard c=0.95 n=27 | structure | — | CANDIDATE |
| 4207 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.clickDropContent` | 32 | 27 | 0.94 of 2517 | template=Standard c=0.95 n=29 | structure | — | CANDIDATE |
| 4210 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `img.img-fluid` | 28 | 27 | 0.84 of 2517 | era=Refresh c=0.84 n=28 | structure | — | CANDIDATE |
| 4213 | body | EXTRA | `div.row` | `—` | `div.col-12.col-md-4` | 33 | 26 | 0.94 of 2517 | template=Standard c=0.95 n=26 | structure | — | CANDIDATE |
| 4215 | body | EXTRA | `div.inquiryPanel.showing` | `—` | `div.row` | 28 | 26 | 0.99 of 2517 | era=Refresh c=0.99 n=28 | structure | yes | CANDIDATE |
| 4217 | body | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `div.col-12.col-md-6` | 32 | 25 | 0.98 of 2517 | ptype=lesson c=0.99 n=28 | structure | — | CANDIDATE |
| 4226 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.alert.solid` | 28 | 23 | 0.99 of 2517 | template=Standard c=0.99 n=22 | structure | yes | CANDIDATE |
| 4230 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `h3` | 25 | 23 | 0.84 of 2517 | template+ptype=Standard/lesson c=0.84 n=21 | structure | — | CANDIDATE |
| 4231 | body | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `p` | 25 | 23 | 0.98 of 2517 | ptype=lesson c=0.99 n=21 | structure | — | CANDIDATE |
| 4234 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `div.alert` | 32 | 22 | 0.84 of 2517 | template+ptype=Standard/lesson c=0.84 n=22 | structure | — | CANDIDATE |
| 4238 | body | EXTRA | `p>span.infoTrigger` | `—` | `span.infoTrigger` | 24 | 22 | 0.95 of 2517 | era=Refresh c=0.95 n=24 | structure | — | CANDIDATE |
| 4239 | body | EXTRA | `div.col-12.col-md-8` | `—` | `h2` | 24 | 22 | 0.98 of 2517 | era=Refresh c=0.98 n=24 | structure | — | CANDIDATE |
| 4254 | body | EXTRA | `div.flipCardsContainer.row` | `—` | `div.col-12.col-md-4.paddingLR` | 21 | 20 | 0.97 of 2517 | era=Refresh c=0.97 n=21 | structure | — | CANDIDATE |
| 4263 | body | SUBSTITUTED | `div#body` | `div.row` | `div.table-responsive` | 24 | 18 | 0.94 of 2517 | template+ptype=Standard/lesson c=0.98 n=20 | structure | — | CANDIDATE |
| 4265 | body | EXTRA | `div.col-12.col-md-6` | `—` | `img.img-fluid` | 22 | 18 | 0.99 of 2517 | era=Refresh c=0.99 n=22 | structure | — | CANDIDATE |
| 4270 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `div.activity.interactive[number=*]` | 21 | 18 | 0.84 of 2517 | template+ptype=Standard/lesson c=0.84 n=20 | structure | yes | CANDIDATE |
| 4307 | body | EXTRA | `div.col-12.col-md-6` | `—` | `p` | 23 | 14 | 1.00 of 2517 | ptype=lesson c=1.00 n=21 | structure | — | CANDIDATE |
| 4340 | body | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `div.button` | 24 | 12 | 0.98 of 2517 | ptype=lesson c=0.99 n=23 | structure | — | CANDIDATE |
| 9333 | root | EXTRA | `body.container-fluid` | `—` | `div.row` | 275 | 275 | 0.88 of 2524 | subject+ptype=1-10 Mathematics/overview c=0.97 n=33 | structure | — | CANDIDATE |
| 9337 | root | SUBSTITUTED | `#root` | `body` | `body.container-fluid` | 139 | 15 | 0.06 of 2524 | series=PWY10 c=1.00 n=45 | structure | yes | CANDIDATE |

## Details — in the companion file `CONVERTER_V2/outputs/_diff_queue_details.md`
Every CANDIDATE and every top-40 row has three quoted examples (WT / gold / Claude) there, plus the
below-floor list. **NEVER read the companion whole** (hundreds of KB): `grep -n '^### #<rank> ' CONVERTER_V2/outputs/_diff_queue_details.md` then `sed -n '<start>,<start+40>p'`. The top 25
candidates' detail blocks are repeated below for convenience.

### #4 · title · MISSING · `div#header` › gold `h1>span` vs Claude `—` — CANDIDATE
- pages 278 / modules 129 / lines 282; consensus (all) 0.24 of 2524 gold pages with the region; derivable 0.74 (72 lines with no WT source)
- by template: Standard 86m/208p c=0.19; Fundamentals 26m/26p c=0.51; Inquiry 11m/14p c=0.44; Bilingual 6m/30p c=1.00
- by subject: NCEA1 21m/45p c=0.16; 1-10 English 21m/32p c=0.18; Leaving to Learn 14m/22p c=0.32; Online Safety (OS9000) 13m/29p c=0.32; 1-10 Mathematics 12m/12p c=0.16; ANZH 6m/31p c=0.47
- by era: Refresh 129m/278p c=0.24
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
- modules: ANZH101, ANZH103, ANZH104, ANZH301, ANZH401, ANZH404, ARFUN01, ARFUN03, ARFUN04, ARFUN05, ART1004, ART1006, CEDK102, CEDO202, CEDR204, CHI1005, CHWHA, DTC1005, ENFUN01, ENFUN02, ENFUN03, ENFUN04, ENFUN05, ENFUN07 …

### #5 · title · EXTRA · `div#header` › gold `—` vs Claude `h1>span` — CANDIDATE
- pages 22 / modules 21 / lines 23; consensus (all) 0.76 of 2524 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 16m/17p c=0.81; Fundamentals 4m/4p c=0.49; Inquiry 1m/1p c=0.56
- by subject: 1-10 Blended Literacy 6m/6p c=0.99; NCEA1 4m/4p c=0.84; Leaving to Learn 4m/4p c=0.68; 1-10 Writing (MiW) 2m/2p c=0.38; ANZH 1m/2p c=0.53; ConnectED 1m/1p c=0.73
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

### #34 · module-menu · SUBSTITUTED · `div.col-12.col-md-6.paddingR` › gold `p` vs Claude `h5` — CANDIDATE
- pages 87 / modules 87 / lines 157; consensus (all) 0.06 of 2524 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 62m/62p c=0.05; Fundamentals 14m/14p c=0.13; Inquiry 11m/11p c=0.40
- by subject: 1-10 Blended Literacy 73m/73p c=0.25; 1-10 Health and PE 14m/14p c=0.39
- by era: Refresh 87m/87p c=0.06
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:160 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
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

### #36 · module-menu · EXTRA · `ul` › gold `—` vs Claude `li` — CANDIDATE
- pages 85 / modules 47 / lines 171; consensus (all) 0.78 of 2524 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 33m/71p c=0.79; Inquiry 12m/12p c=0.43; Fundamentals 2m/2p c=0.76
- by subject: 1-10 Blended Literacy 11m/11p c=0.67; 1-10 English 9m/12p c=0.75; NCEA1 8m/18p c=0.97; ConnectED 7m/7p c=0.53; Te ara Whakapuawa -Wellbeing 5m/5p c=0.08; 1-10 Science 3m/24p c=0.70
- by era: Refresh 47m/85p c=0.78
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
- modules: AGH1001, AGH1004, AGH1006, AGH1007, AGH1008, BLL115, BLL122, BLL123, BLL144, BLL145, BLL152, BLL165, BLL210, BLL241, BLL254, BLL260, CEDK101, CEDK501, CEDO202, CEDO301, CEDR203, CEDR501, CEDT207, ENFUN03 …

### #38 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `div.col-12.col-md-6.paddingR` — CANDIDATE
- pages 87 / modules 44 / lines 137; consensus (all) 0.97 of 2524 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 39m/82p c=0.97; Inquiry 5m/5p c=0.88
- by subject: 1-10 Blended Literacy 17m/17p c=0.75; ANZH 7m/16p c=1.00; 1-10 Mathematics 7m/35p c=1.00; 1-10 English 5m/5p c=1.00; Leaving to Learn 4m/4p c=1.00; EXPlore 2m/5p c=1.00
- by era: Refresh 44m/87p c=0.97
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:160 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **ANZH101** ANZH101_0_0.html ↔ ANZH101_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-6.paddingR  «Understand»`
- **ANZH103** ANZH103_0_0.html ↔ ANZH103_0_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-6.paddingR  «UNDERSTAND»`
- **ANZH104** ANZH104_0_0.html ↔ ANZH104_00.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-6.paddingR  «Understand»`
- modules: ANZH101, ANZH103, ANZH104, ANZH105, ANZH203, ANZH205, ANZH401, BLL110, BLL111, BLL120, BLL121, BLL134, BLL135, BLL144, BLL152, BLL160, BLL161, BLL172, BLL240, BLL241, BLL244, BLL245, BLL256, BLL270 …

### #40 · module-menu · SUBSTITUTED · `div.col-12.col-md-6.paddingL` › gold `p` vs Claude `h5` — CANDIDATE
- pages 43 / modules 43 / lines 64; consensus (all) 0.03 of 2524 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Inquiry 16m/16p c=0.28; Fundamentals 14m/14p c=0.13; Standard 13m/13p c=0.02
- by subject: 1-10 Health and PE 14m/14p c=0.39; ConnectED 10m/10p c=0.12; Te ara Whakapuawa -Wellbeing 6m/6p c=0.85; 1-10 Blended Literacy 5m/5p c=0.02; Leaving to Learn 4m/4p c=0.02; ANZH 2m/2p c=0.02
- by era: Refresh 43m/43p c=0.03
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:160 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **ANZH105** ANZH105_0_0.html ↔ ANZH105_00.0.html (structure, derivable=True)
  - gold: `p  «Ākonga will:»`
  - Claude: `h5  «Ākonga will:»`
- **ANZH205** ANZH205_0_0.html ↔ ANZH205_00.0.html (structure, derivable=True)
  - gold: `p  «You will:»`
  - Claude: `h5  «Ākonga will:»`
- **BLL172** BLL172_0_0.html ↔ BLL172-00.html (structure, derivable=True)
  - gold: `p  «We are learning:»`
  - Claude: `h5  «We are learning:»`
- modules: ANZH105, ANZH205, BLL172, BLL174, BLL175, BLL176, BLL177, CEDK102, CEDK401, CEDO102, CEDO201, CEDO202, CEDO402, CEDR204, CEDT404, CEDW101, CEDW201, ENGC302, ENGC401, HPFUN101, HPFUN102, HPFUN103, HPFUN201, HPFUN202 …

### #41 · module-menu · MISSING · `div.col-12.col-md-8` › gold `h5` vs Claude `—` — CANDIDATE
- pages 177 / modules 41 / lines 308; consensus (all) 0.24 of 2524 gold pages with the region; derivable 0.86 (44 lines with no WT source)
- by template: Standard 37m/169p c=0.26; Inquiry 3m/7p c=0.13; Fundamentals 1m/1p c=0.01
- by subject: NCEA1 13m/61p c=0.23; 1-10 English 13m/59p c=0.55; ConnectED 3m/7p c=0.44; 1-10 Languages 3m/4p c=0.40; Leaving to Learn 3m/6p c=0.14; 1-10 Health and PE 2m/19p c=0.53
- by era: Refresh 41m/177p c=0.24
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1004** AGH1004_2_0.html ↔ AGH1004.06.html (content, derivable=True)
  - gold: `h5  «We are learning to:»`
  - Claude: `—`
  - WT: `We are learning to ...`
- **CBI1008** CBI1008_1_0.html ↔ CBI1008_1_0.html (content, derivable=True)
  - gold: `h5  «We are learning about:»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [H2]  [/RED TEXT]🔴✅We are learning about:`
- **CEDK501** CEDK501_3_1.html ↔ CEDK501_3.1.html (content, derivable=True)
  - gold: `h5  «Learning intentions»`
  - Claude: `—`
- modules: AGH1004, CBI1008, CEDK501, CEDR501, CEDT501, COM1002, COM1005, COM1006, ENGC102, ENGC201, ENGC202, ENGC206, ENGC403, ENGJ302, ENGJ402, ENGJ403, ENGR102, ENGR202, ENGS101, ENGS302, ENGS404, FRFUN08, FRNO901, GEO1005 …

### #42 · module-menu · MISSING · `div.col-12.col-md-6.paddingR` › gold `p` vs Claude `—` — CANDIDATE
- pages 58 / modules 38 / lines 77; consensus (all) 0.04 of 2524 gold pages with the region; derivable 0.74 (20 lines with no WT source)
- by template: Standard 28m/48p c=0.04; Inquiry 10m/10p c=0.19
- by subject: 1-10 Blended Literacy 24m/24p c=0.23; EXPlore 5m/8p c=0.00; ConnectED 4m/4p c=0.10; ANZH 2m/2p c=0.00; 1-10 Mathematics 2m/16p c=0.05; NCEA1 1m/4p c=0.00
- by era: Refresh 38m/58p c=0.04
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:160 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **ANZH104** ANZH104_0_0.html ↔ ANZH104_00.0.html (content, derivable=True)
  - gold: `p  «Māori history is the foundational and continuous history of Aotearoa New Zealand.»`
  - Claude: `—`
  - WT: `*Māori history is the foundational and continuous history of Aotearoa New Zealand.*`
- **ANZH105** ANZH105_0_0.html ↔ ANZH105_00.0.html (content, derivable=True)
  - gold: `p  «Relationships and connections between people and across boundaries have shaped the course of Aotearoa New Zealand’s hist»`
  - Claude: `—`
  - WT: `Relationships and connections between people and across boundaries have shaped the course of Aotearoa New Zealand’s histories.`
- **BLL110** BLL110_0_0.html ↔ BLL110.html (content, derivable=False)
  - gold: `p  «Shared codes and conventions enable us to make sense of what is heard, read, and seen.»`
  - Claude: `—`
- modules: ANZH104, ANZH105, BLL110, BLL111, BLL112, BLL113, BLL114, BLL115, BLL116, BLL117, BLL120, BLL121, BLL122, BLL124, BLL134, BLL135, BLL145, BLL146, BLL147, BLL153, BLL154, BLL160, BLL161, BLL214 …

### #45 · module-menu · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `h5` — CANDIDATE
- pages 80 / modules 25 / lines 106; consensus (all) 0.76 of 2524 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 23m/77p c=0.74; Fundamentals 1m/1p c=0.99; Inquiry 1m/2p c=0.87
- by subject: Leaving to Learn 7m/13p c=0.85; 1-10 English 6m/14p c=0.46; NCEA1 3m/9p c=0.77; 1-10 Science 3m/24p c=0.88; ANZH 2m/13p c=1.00; Online Safety (OS9000) 2m/2p c=0.40
- by era: Refresh 25m/80p c=0.76
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

### #47 · module-menu · EXTRA · `div.col-12.col-md-6.paddingR` › gold `—` vs Claude `p>b` — CANDIDATE
- pages 23 / modules 23 / lines 44; consensus (all) 1.00 of 2524 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 20m/20p c=1.00; Inquiry 3m/3p c=1.00
- by subject: 1-10 Blended Literacy 22m/22p c=1.00; ANZH 1m/1p c=1.00
- by era: Refresh 23m/23p c=1.00
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:160 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **ANZH104** ANZH104_0_0.html ↔ ANZH104_00.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «[MODULE INTRODUCTION]»`
- **BLL125** BLL125_0_0.html ↔ BLL125-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Students develop basic literacy capability to read fluently and accurately. They engage with a variety of written texts,»`
- **BLL126** BLL126_0_0.html ↔ BLL126-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Students develop basic literacy capability to read fluently and accurately. They engage with a variety of written texts,»`
- modules: ANZH104, BLL125, BLL126, BLL127, BLL130, BLL131, BLL132, BLL133, BLL136, BLL137, BLL140, BLL141, BLL143, BLL144, BLL145, BLL146, BLL147, BLL150, BLL151, BLL153, BLL154, BLL213, BLL214

### #48 · module-menu · SUBSTITUTED · `ul` › gold `li` vs Claude `li` — CANDIDATE
- pages 105 / modules 22 / lines 419; consensus (all) 0.57 of 2524 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 21m/104p c=0.59; Inquiry 1m/1p c=0.81
- by subject: 1-10 Mathematics 9m/42p c=0.56; 1-10 English 4m/23p c=0.88; NCEA1 4m/17p c=0.48; 1-10 Science 3m/21p c=0.85; Te ara Whakapuawa -Wellbeing 1m/1p c=1.00; Leaving to Learn 1m/1p c=0.75
- by era: Refresh 22m/105p c=0.57
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ENGC201** ENGC201_0_0.html ↔ ENGC201_0.0.html (structure, derivable=True)
  - gold: `li  «Being able to recognise and use the code, conventions, and features of diverse types of texts allows for a greater preci»`
  - Claude: `li  «People use language in diverse ways in different situations. This helps to signal social roles and relationships.»`
- **ENGC202** ENGC202_1_0.html ↔ ENGC202_1.0.html (structure, derivable=True)
  - gold: `li  «drawing what you hear from instructions»`
  - Claude: `li  «identify what makes a good instruction»`
- **ENGC206** ENGC206_1_0.html ↔ ENGC206_1_0.html (structure, derivable=True)
  - gold: `li  «to understand and use precise and topic-related vocabulary»`
  - Claude: `li  «to decode multi-syllable words.»`
- modules: ENGC201, ENGC202, ENGC206, ENGI103, ENO2060, JPN1004, MXDB301, MXDB302, MXEX301, MXFL101, MXFL102, MXFL201, MXFL202, MXFU301, MXFU402, MXS1004, PES1004, SCBI301, SCCH301, SCPH301, TWHR905, XWHA02

### #52 · module-menu · EXTRA · `div.col-12.col-md-6.paddingR` › gold `—` vs Claude `p` — CANDIDATE
- pages 20 / modules 20 / lines 41; consensus (all) 0.96 of 2524 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 15m/15p c=0.96; Inquiry 5m/5p c=0.81
- by subject: 1-10 Blended Literacy 9m/9p c=0.77; ConnectED 4m/4p c=0.90; 1-10 English 3m/3p c=1.00; ANZH 2m/2p c=1.00; 1-10 Mathematics 1m/1p c=0.95; Leaving to Learn 1m/1p c=1.00
- by era: Refresh 20m/20p c=0.96
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:160 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **ANZH104** ANZH104_0_0.html ↔ ANZH104_00.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «IROO292»`
- **ANZH401** ANZH401_0_0.html ↔ ANZH401_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Allow 15 hours for the learning in this module.»`
- **BLL123** BLL123_0_0.html ↔ BLL123-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Writing: Students use phonics and morphological knowledge to spell new, regular words and a growing number of irregular »`
- modules: ANZH104, ANZH401, BLL123, BLL131, BLL174, BLL175, BLL176, BLL177, BLL240, BLL242, BLL252, CEDK101, CEDK102, CEDO402, CEDT104, ENGC301, ENGC302, ENGC401, MXEX202, XWHA02

### #55 · module-menu · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `ul` — CANDIDATE
- pages 45 / modules 18 / lines 80; consensus (all) 0.72 of 2524 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 16m/43p c=0.69; Fundamentals 1m/1p c=0.99; Inquiry 1m/1p c=0.81
- by subject: 1-10 English 5m/18p c=0.39; Leaving to Learn 5m/7p c=0.57; NCEA1 3m/11p c=0.79; ANZH 2m/3p c=1.00; ConnectED 1m/1p c=0.56; 1-10 Mathematics 1m/4p c=0.85
- by era: Refresh 18m/45p c=0.72
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
- modules: AGH1009, ANZH301, ANZH302, CEDO501, ENFUN07, ENGC201, ENGC202, ENGC206, ENGI102, GEO1005, JPN1004, MXEO102, OSBY301, XDLS903, XLP01, XLP02, XLP03, XLP04

### #56 · module-menu · MISSING · `div#header` › gold `div#module-head-buttons` vs Claude `—` — CANDIDATE
- pages 38 / modules 18 / lines 38; consensus (all) 0.76 of 2524 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 10m/17p c=0.78; Bilingual 8m/21p c=0.45
- by subject: Te Marautanga o Aotearoa TMoA 8m/21p c=0.45; 1-10 Blended Literacy 4m/8p c=0.45; NCEA1 2m/2p c=0.72; Leaving to Learn 2m/4p c=0.89; EXPlore 1m/1p c=1.00; 1-10 Mathematics 1m/2p c=0.78
- by era: Refresh 18m/38p c=0.76
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
- modules: BLL114, BLL116, BLL153, BLL272, EXPFUN07, HES1002, MUS1004, MXFL401, PMT101, PNR101, PNR102, PNR104, PNR107, TRR107, TRR109, TRR110, XLP06, XOTPB08

### #57 · module-menu · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `p` — CANDIDATE
- pages 36 / modules 18 / lines 45; consensus (all) 0.88 of 2524 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 17m/35p c=0.87; Inquiry 1m/1p c=0.84
- by subject: Leaving to Learn 6m/6p c=0.69; NCEA1 5m/18p c=0.86; Online Safety (OS9000) 3m/7p c=0.79; ANZH 2m/3p c=1.00; 1-10 English 1m/1p c=0.84; 1-10 Mathematics 1m/1p c=0.93
- by era: Refresh 18m/36p c=0.88
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
- modules: AGH1003, ANZH301, ANZH302, ENGC201, GEO1005, HIS1005, HIS1006, MXDI201, MXS1004, OSBY301, OSGM201, OSOH101, XDLS903, XDLS908, XLP01, XLP02, XLP03, XLP04

### #58 · module-menu · EXTRA · `div.col-12.col-md-6.offset-md-0` › gold `—` vs Claude `p` — CANDIDATE
- pages 28 / modules 18 / lines 83; consensus (all) 0.99 of 2524 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 18m/28p c=0.99
- by subject: 1-10 English 15m/16p c=0.95; 1-10 Social Science 2m/6p c=1.00; 1-10 Mathematics 1m/6p c=1.00
- by era: Refresh 18m/28p c=0.99
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:160 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
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

### #62 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `WIDGET` — CANDIDATE
- pages 17 / modules 17 / lines 17; consensus (all) 0.88 of 2524 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 13m/13p c=0.89; Fundamentals 4m/4p c=0.78
- by subject: 1-10 Blended Literacy 13m/13p c=0.97; 1-10 Languages 2m/2p c=0.94; 1-10 Social Science 2m/2p c=0.59
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

### #65 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `div.col-12.col-md-8` — CANDIDATE
- pages 103 / modules 15 / lines 103; consensus (all) 0.67 of 2524 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 15m/103p c=0.64
- by subject: 1-10 Mathematics 12m/87p c=0.77; 1-10 English 2m/11p c=0.38; ConnectED 1m/5p c=0.54
- by era: Refresh 15m/103p c=0.67
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

### #66 · module-menu · SUBSTITUTED · `div.col-12.col-md-6.paddingR` › gold `ul` vs Claude `p>b` — CANDIDATE
- pages 15 / modules 15 / lines 15; consensus (all) 0.06 of 2524 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 12m/12p c=0.04; Inquiry 3m/3p c=0.43
- by subject: 1-10 Blended Literacy 14m/14p c=0.25; Te ara Whakapuawa -Wellbeing 1m/1p c=1.00
- by era: Refresh 15m/15p c=0.06
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:160 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **BLL125** BLL125_0_0.html ↔ BLL125-01.html (structure, derivable=True)
  - gold: `ul  «Ākonga can use their basic literacy capability and can read fluently and accurately. They engage with a variety of writt»`
  - Claude: `p  «Students interpret texts by drawing on various elements and recognise different perspectives, sharing their own opinions»`
- **BLL126** BLL126_0_0.html ↔ BLL126-01.html (structure, derivable=True)
  - gold: `ul  «Ākonga can use their basic literacy capability and can read fluently and accurately. They engage with a variety of writt»`
  - Claude: `p  «Students interpret texts by drawing on various elements and recognise different perspectives, sharing their own opinions»`
- **BLL127** BLL127_0_0.html ↔ BLL127-01.html (structure, derivable=True)
  - gold: `ul  «Ākonga can use their basic literacy capability and can read fluently and accurately. They engage with a variety of writt»`
  - Claude: `p  «Students interpret texts by drawing on various elements and recognise different perspectives, sharing their own opinions»`
- modules: BLL125, BLL126, BLL127, BLL136, BLL137, BLL140, BLL141, BLL143, BLL146, BLL147, BLL150, BLL151, BLL153, BLL154, TWHT903

### #67 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `div.col-12.col-md-6.offset-md-0` — CANDIDATE
- pages 30 / modules 14 / lines 30; consensus (all) 0.95 of 2524 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 13m/29p c=0.95; Fundamentals 1m/1p c=1.00
- by subject: 1-10 English 11m/27p c=0.90; 1-10 Social Science 2m/2p c=0.67; 1-10 Mathematics 1m/1p c=0.96
- by era: Refresh 14m/30p c=0.95
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:160 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **ENGC101** ENGC101_0_0.html ↔ ENGC101_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-6.offset-md-0  «In this module, we delve into the diverse tools and techniques we use to communicate effectively in various contexts. Fr»`
- **ENGC102** ENGC102_0_0.html ↔ ENGC102_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-6.offset-md-0  «Learning Intentions»`
- **ENGC201** ENGC201_0_0.html ↔ ENGC201_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12.col-md-6.offset-md-0  «Learning Intentions»`
- modules: ENGC101, ENGC102, ENGC201, ENGI103, ENGI201, ENGI202, ENGI203, ENGI400, ENGJ102, ENGS202, ENGS301, MXFUN01, SSOG101, SSOG105

### #68 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `div.col-12.col-md-12.paddingR` — CANDIDATE
- pages 16 / modules 14 / lines 16; consensus (all) 0.96 of 2524 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 14m/16p c=0.96
- by subject: 1-10 Blended Literacy 12m/12p c=0.80; EXPlore 2m/4p c=1.00
- by era: Refresh 14m/16p c=0.96
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
- modules: BLL112, BLL113, BLL125, BLL141, BLL142, BLL143, BLL144, BLL162, BLL163, BLL166, BLL236, BLL237, EXBP901, EXIP901

### #71 · module-menu · EXTRA · `div.col-12.col-md-6.paddingR` › gold `—` vs Claude `h5` — CANDIDATE
- pages 15 / modules 13 / lines 29; consensus (all) 0.99 of 2524 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 11m/13p c=0.99; Inquiry 1m/1p c=1.00; Fundamentals 1m/1p c=1.00
- by subject: 1-10 Blended Literacy 5m/5p c=1.00; 1-10 English 2m/2p c=1.00; EXPlore 2m/4p c=1.00; ANZH 1m/1p c=1.00; 1-10 Health and PE 1m/1p c=1.00; 1-10 Mathematics 1m/1p c=0.95
- by era: Refresh 13m/15p c=0.99
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:160 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **ANZH401** ANZH401_0_0.html ↔ ANZH401_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «Whakamaheretia tō wā | Planning your time»`
- **BLL145** BLL145_0_0.html ↔ BLL145-0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «Success Criteria»`
- **BLL153** BLL153_0_0.html ↔ BLL153-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «Success Criteria»`
- modules: ANZH401, BLL145, BLL153, BLL154, BLL236, BLL260, ENGC302, ENGR102, EXBP901, EXIP901, HPFUN302, MXEX202, XWHA02

### #72 · module-menu · EXTRA · `div.col-12.col-md-6.paddingL` › gold `—` vs Claude `h5` — CANDIDATE
- pages 13 / modules 13 / lines 31; consensus (all) 1.00 of 2524 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Inquiry 12m/12p c=0.99; Fundamentals 1m/1p c=1.00
- by subject: ConnectED 7m/7p c=1.00; Te ara Whakapuawa -Wellbeing 5m/5p c=0.92; 1-10 Health and PE 1m/1p c=1.00
- by era: Refresh 13m/13p c=1.00
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:160 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **CEDK401** CEDK401_0_0.html ↔ CEDK401 Food Sustainability.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «AROMATAWAI»`
- **CEDO202** CEDO202_0_0.html ↔ CEDO202_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «Whakamaheretia tō wā | Planning your time»`
- **CEDO402** CEDO402_0_0.html ↔ CEDO402_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «Whakamaheretia tō wā | Planning your time»`
- modules: CEDK401, CEDO202, CEDO402, CEDR203, CEDT101, CEDT207, CEDT301, HPFUN302, TWHA902, TWHK901, TWHK903, TWHK907, TWHR907

### #76 · module-menu · EXTRA · `p>b` › gold `—` vs Claude `b` — CANDIDATE
- pages 12 / modules 12 / lines 16; consensus (all) 0.99 of 2524 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 10m/10p c=0.99; Inquiry 2m/2p c=0.99
- by subject: 1-10 English 5m/5p c=1.00; Leaving to Learn 4m/4p c=1.00; 1-10 Blended Literacy 1m/1p c=1.00; ConnectED 1m/1p c=0.99; 1-10 Mathematics 1m/1p c=1.00
- by era: Refresh 12m/12p c=0.99
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL142** BLL142_0_0.html ↔ BLL142-0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `b  «Oral Language:»`
- **CEDR203** CEDR203_0_0.html ↔ CEDR203_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `b  «ENGLISH»`
- **ENGC101** ENGC101_0_0.html ↔ ENGC101_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `b  «Ko te reo me ōna tikanga te hā o te whakawhitiwhiti korero.»`
- modules: BLL142, CEDR203, ENGC101, ENGI301, ENGR102, ENGS101, ENGS301, MXFL202, XDLS901, XGF9002, XGF9004, XGF9006

### #77 · module-menu · EXTRA · `div.col-12.col-md-6.paddingL` › gold `—` vs Claude `p` — CANDIDATE
- pages 12 / modules 12 / lines 55; consensus (all) 1.00 of 2524 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Inquiry 12m/12p c=0.98
- by subject: ConnectED 7m/7p c=1.00; Te ara Whakapuawa -Wellbeing 5m/5p c=0.85
- by era: Refresh 12m/12p c=1.00
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:160 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **CEDK401** CEDK401_0_0.html ↔ CEDK401 Food Sustainability.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «in your area or create your own community initiative based around sustainable food production. For whichever option you »`
- **CEDO201** CEDO201_0_0.html ↔ CEDO201_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «This module integrates the learning areas of science and technology for phase 2. Throughout the module, ākonga will appl»`
- **CEDO202** CEDO202_0_0.html ↔ CEDO202_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «In this module you will learn about the seasons and their traits. You will also learn about why we have the seasons and »`
- modules: CEDK401, CEDO201, CEDO202, CEDO402, CEDT101, CEDT102, CEDT207, TWHA902, TWHK901, TWHK903, TWHK907, TWHR907
