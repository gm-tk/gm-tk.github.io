# DIFF_QUEUE.md — the diff miner's ranked class queue (LOOP__Autonomous_Rounds.md §1d)

**Produced:** 2026-09-17 21:56 NZST by `reference/tests/_diff_miner.py` on the CURRENT corpus (pageforge-site HEAD f54cbec; Claude corpus 416 dirs). **Population:** the skeleton gate's own — 1956 paired pages / 405 modules (compare_exclusions.txt honoured; acks / glossary / references pages excluded); parse errors skipped: 0 (must be 0); modules without a parsed WT: 2. Run time 63.1 s.

**What a row is.** One CLASS = (region, parent element, gold form, Claude form, direction) over every differing skeleton line of every paired page — the same lines, labels, widget collapse and difflib alignment the PRIMARY gate scores (each element its own line so it can be quoted). Direction: MISSING = gold has it, Claude lacks it; EXTRA = Claude has it, gold lacks it; SUBSTITUTED = same position, different tag / class / wrapper; MOVED = same text, different place. Consensus = of the gold pages in the group where the region exists, the share carrying the gold form (for EXTRA: the share NOT carrying Claude's form). Derivable = the gold line's text is in the module's parsed Writers Template (round-110 tolerance); structure-only differences are always derivable.

**Candidate rule (§1d).** modules ≥ 10 for a chrome class (module-code / title / header / module-menu / crumbs / phases-nav / footer / acks), pages ≥ 20 for a body / activity class; gold consensus ≥ 0.60 in at least one template or subject group that itself reaches the floor; structure-only or derivable share ≥ 0.60. A class below the floor is listed, never dropped. A CANDIDATE still goes through the PICK's KB-first check, the triangulation and the §3 corpus-wide measurement before any code — this table is the queue, not the verdict.

## Summary

- differing skeleton lines: 237174 — by direction {'MISSING': 122145, 'SUBSTITUTED': 21053, 'EXTRA': 85783, 'MOVED': 8193}
- by region: {'module-code': 17, 'title': 253, 'header': 6, 'module-menu': 11990, 'phases-nav': 48, 'crumbs': 180, 'footer': 2092, 'acks': 1175, 'activity': 85613, 'body': 133908, 'root': 1892}
- classes: 10980 — CANDIDATE 167, below floor 10593, the rest below consensus / not derivable

## Completeness census — the repeating chrome (§1d item 4)

| region | pages with region | gold items | gold items in WT | Claude items | derivable misses | pages with misses | modules with misses | status |
|---|---|---|---|---|---|---|---|---|
| module-menu | 1246 | 13989 | 13016 | 11001 | 4402 | 618 | 168 | CANDIDATE (verify by eye — text presence, not position) |
| crumbs | 46 | 294 | 280 | 195 | 113 | 27 | 23 | CANDIDATE (verify by eye — text presence, not position) |
| phases-nav | 53 | 233 | 201 | 213 | 29 | 15 | 15 | CANDIDATE (verify by eye — text presence, not position) |
| footer | 14 | 70 | 56 | 0 | 56 | 14 | 6 | BELOW FLOOR |

- **module-menu** by template: Fundamentals 11m/21p/80 misses; Inquiry 26m/48p/285 misses; Standard 131m/549p/4037 misses
  - MXFL202 MXFL202_1_0.html: gold 53 items (51 in WT) / Claude 0 — 51 derivable misses, e.g. h3 «Understand» · span «Understand»
  - MXFL202 MXFL202_2_0.html: gold 53 items (51 in WT) / Claude 0 — 51 derivable misses, e.g. h3 «Understand» · span «Understand»
  - MXFL202 MXFL202_4_0.html: gold 53 items (51 in WT) / Claude 0 — 51 derivable misses, e.g. h3 «Understand» · span «Understand»
  - MXFL202 MXFL202_6_0.html: gold 53 items (51 in WT) / Claude 0 — 51 derivable misses, e.g. h3 «Understand» · span «Understand»
- **crumbs** by template: Fundamentals 0m/0p/0 misses; Inquiry 21m/21p/81 misses; Standard 2m/6p/32 misses
  - BLL240 BLL240_1_0.html: gold 8 items (8 in WT) / Claude 0 — 8 derivable misses, e.g. p «Introduction» · p «wh»
  - CEDK501 CEDK501_0_0.html: gold 8 items (7 in WT) / Claude 0 — 7 derivable misses, e.g. p «Dream it, plan it, do it» · p «Costing it out: budgeting for success»
  - CEDT104 CEDT104_0_0.html: gold 8 items (7 in WT) / Claude 0 — 7 derivable misses, e.g. p «Introduction» · p «Pepeha»
  - TWHA902 TWHA902_0_0.html: gold 9 items (8 in WT) / Claude 1 — 7 derivable misses, e.g. p «Listening, speaking, reading, writing» · p «Active listening»
- **phases-nav** by template: Fundamentals 14m/14p/25 misses; Standard 1m/1p/4 misses
  - ARFUN04 ARFUN04_0_0.html: gold 4 items (4 in WT) / Claude 0 — 4 derivable misses, e.g. p «Phase 1» · p «Phase 2»
  - MXFUN01 MXFUN01_0_0.html: gold 4 items (4 in WT) / Claude 0 — 4 derivable misses, e.g. p «Number Sense» · p «Place Value»
  - SSFUN07 SSFUN07_3_0.html: gold 4 items (4 in WT) / Claude 0 — 4 derivable misses, e.g. p «Phase 1» · p «Phase 2»
  - MXFUN03 MXFUN03_0_0.html: gold 4 items (4 in WT) / Claude 1 — 3 derivable misses, e.g. p «Phase 2» · p «Phase 3»
- **footer** by template: Inquiry 1m/7p/38 misses; Standard 5m/7p/18 misses
  - BLL240 BLL240_1_2.html: gold 6 items (6 in WT) / Claude 0 — 6 derivable misses, e.g. li «Previous» · a#prev-lesson «Previous»
  - BLL240 BLL240_1_3.html: gold 6 items (6 in WT) / Claude 0 — 6 derivable misses, e.g. li «Previous» · a#prev-lesson «Previous»
  - BLL240 BLL240_1_4.html: gold 6 items (6 in WT) / Claude 0 — 6 derivable misses, e.g. li «Previous» · a#prev-lesson «Previous»
  - BLL240 BLL240_1_5.html: gold 6 items (6 in WT) / Claude 0 — 6 derivable misses, e.g. li «Previous» · a#prev-lesson «Previous»

## Chrome facts — the header and footer as SETS per page (alignment-free; §1d items 2 + 4)

A fact is one thing a page's chrome has: `header:chip` (the `#module-code` div), `header:chip=module-code` / `=lesson-number` / `=lesson-number(00)`, `header:head-buttons`, `header:menu-content`, `header:title-h1-count=N`, `footer:present`, `footer:ul=<classes>`, `footer:link=prev-lesson` / `next-lesson` / `home-nav`, `footer:links=<order>`, `footer:inside-body`, `nav:crumbs`, `nav:phases`. MISSING = the gold page has the fact and Claude's does not; EXTRA the reverse. Consensus = the share of gold pages in the group that have (MISSING) / lack (EXTRA) the fact. Floor 10 modules.

| # | dir | fact | pages | modules | gold share (all) | consensus (all) | best group | status |
|---|---|---|---|---|---|---|---|---|
| F1 | MISSING | `header:title-h1-count=2` | 191 | 107 | 0.22 | 0.22 | subject+ptype=1-10 English/overview c=0.94 n=17 | CANDIDATE |
| F2 | EXTRA | `header:title-h1-count=1` | 188 | 104 | 0.78 | 0.22 | subject+ptype=1-10 English/overview c=0.94 n=17 | CANDIDATE |
| F3 | MISSING | `header:chip=decimal-number` | 85 | 43 | 0.56 | 0.56 | template+ptype=Standard/lesson c=0.70 n=35 | CANDIDATE |
| F4 | EXTRA | `header:chip=decimal-number` | 161 | 39 | 0.56 | 0.44 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F5 | EXTRA | `header:chip=lesson-number` | 76 | 33 | 0.20 | 0.80 | era=Refresh c=0.80 n=33 | CANDIDATE |
| F6 | MISSING | `header:chip=module-code` | 65 | 33 | 0.16 | 0.16 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F7 | EXTRA | `header:menu-content` | 39 | 25 | 0.75 | 0.25 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F8 | MISSING | `header:chip=lesson-number` | 128 | 23 | 0.20 | 0.20 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F9 | EXTRA | `header:head-buttons` | 34 | 23 | 0.76 | 0.24 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F10 | EXTRA | `header:chip=module-code` | 22 | 22 | 0.16 | 0.84 | template=Standard c=0.86 n=11 | CANDIDATE |
| F11 | MISSING | `header:head-buttons` | 52 | 19 | 0.76 | 0.76 | template=Standard c=0.77 n=13 | CANDIDATE |
| F12 | EXTRA | `header:chip=other` | 39 | 17 | 0.05 | 0.95 | era=Refresh c=0.95 n=17 | CANDIDATE |
| F13 | MISSING | `header:chip=other` | 19 | 13 | 0.05 | 0.05 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F14 | MISSING | `header:title-h1-count=1` | 12 | 12 | 0.78 | 0.78 | template=Standard c=0.83 n=10 | CANDIDATE |
| F15 | EXTRA | `header:title-h1-count=2` | 11 | 11 | 0.22 | 0.78 | era=Refresh c=0.78 n=11 | CANDIDATE |
| F16 | MISSING | `header:menu-content` | 28 | 8 | 0.75 | 0.75 | — | BELOW FLOOR |
| F17 | EXTRA | `header:chip` | 5 | 5 | 0.97 | 0.03 | — | BELOW FLOOR |
| F18 | EXTRA | `header:title-h1-count=0` | 4 | 4 | 0.00 | 1.00 | — | BELOW FLOOR |
| F19 | MISSING | `header:chip` | 3 | 3 | 0.97 | 0.97 | — | BELOW FLOOR |
| F20 | EXTRA | `header:title-h1-count=3` | 1 | 1 | 0.00 | 1.00 | — | BELOW FLOOR |
| F21 | EXTRA | `header:chip=lesson-number(00)` | 1 | 1 | 0.00 | 1.00 | — | BELOW FLOOR |
| F22 | MISSING | `header:title-h1-count=3` | 1 | 1 | 0.00 | 0.00 | — | BELOW FLOOR |
| F23 | MISSING | `nav:crumbs` | 10 | 10 | 0.02 | 0.02 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F24 | MISSING | `nav:phases` | 3 | 3 | 0.03 | 0.03 | — | BELOW FLOOR |
| F25 | EXTRA | `nav:crumbs` | 2 | 2 | 0.02 | 0.98 | — | BELOW FLOOR |
| F26 | MISSING | `footer:inside-body` | 144 | 111 | 0.07 | 0.07 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F27 | EXTRA | `footer:links=next-lesson,home-nav` | 91 | 91 | 0.12 | 0.88 | subject=Leaving to Learn c=0.97 n=27 | CANDIDATE |
| F28 | EXTRA | `footer:links=prev-lesson,next-lesson,home-nav` | 222 | 85 | 0.59 | 0.41 | ptype=overview c=0.95 n=35 | CANDIDATE |
| F29 | MISSING | `footer:links=home-nav,next-lesson` | 69 | 68 | 0.04 | 0.04 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F30 | EXTRA | `footer:links=prev-lesson,home-nav` | 67 | 67 | 0.14 | 0.86 | subject=1-10 English c=0.90 n=11 | CANDIDATE |
| F31 | MISSING | `footer:link=next-lesson` | 57 | 57 | 0.82 | 0.82 | template=Standard c=0.84 n=46 | CANDIDATE |
| F32 | MISSING | `footer:links=prev-lesson,next-lesson,home-nav` | 57 | 54 | 0.59 | 0.59 | template+ptype=Standard/lesson c=0.73 n=39 | CANDIDATE |
| F33 | MISSING | `footer:links=home-nav,prev-lesson,next-lesson` | 111 | 46 | 0.06 | 0.06 | subject=1-10 Health and PE c=0.80 n=12 | CANDIDATE |
| F34 | EXTRA | `footer:link=next-lesson` | 77 | 35 | 0.82 | 0.17 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F35 | MISSING | `footer:ul=footer-nav` | 75 | 26 | 0.85 | 0.85 | ptype=lesson c=0.90 n=17 | CANDIDATE |
| F36 | EXTRA | `footer:link=prev-lesson` | 32 | 24 | 0.81 | 0.19 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F37 | EXTRA | `footer:ul=footer-nav inquiry-nav` | 75 | 21 | 0.14 | 0.86 | ptype=lesson c=0.90 n=18 | CANDIDATE |
| F38 | MISSING | `footer:links=prev-lesson,home-nav` | 49 | 19 | 0.14 | 0.14 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F39 | MISSING | `footer:links=home-nav` | 21 | 17 | 0.03 | 0.03 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F40 | MISSING | `footer:link=prev-lesson` | 13 | 13 | 0.81 | 0.81 | era=Refresh c=0.81 n=13 | CANDIDATE |
| F41 | EXTRA | `footer:ul=footer-nav` | 17 | 9 | 0.85 | 0.15 | — | BELOW FLOOR |
| F42 | MISSING | `footer:links=next-lesson,home-nav` | 9 | 9 | 0.12 | 0.12 | — | BELOW FLOOR |
| F43 | MISSING | `footer:links=home-nav,prev-lesson` | 7 | 7 | 0.00 | 0.00 | — | BELOW FLOOR |
| F44 | EXTRA | `footer:ul=footer-nav fundamentals-nav` | 7 | 7 | 0.01 | 0.99 | — | BELOW FLOOR |
| F45 | MISSING | `footer:ul=footer-nav inquiry-nav` | 12 | 5 | 0.14 | 0.14 | — | BELOW FLOOR |
| F46 | MISSING | `footer:links=prev-lesson,home-nav,next-lesson` | 30 | 4 | 0.01 | 0.01 | — | BELOW FLOOR |
| F47 | MISSING | `footer:link=other` | 19 | 3 | 0.01 | 0.01 | — | BELOW FLOOR |
| F48 | MISSING | `footer:links=prev-lesson,other,next-lesson,home-nav` | 14 | 3 | 0.01 | 0.01 | — | BELOW FLOOR |
| F49 | EXTRA | `footer:link=home-nav` | 9 | 3 | 0.99 | 0.01 | — | BELOW FLOOR |
| F50 | MISSING | `footer:links=other,next-lesson,home-nav` | 3 | 3 | 0.00 | 0.00 | — | BELOW FLOOR |
| F51 | MISSING | `footer:ul=footer-nav fundamentals-nav` | 3 | 3 | 0.01 | 0.01 | — | BELOW FLOOR |
| F52 | EXTRA | `footer:present` | 8 | 2 | 1.00 | 0.00 | — | BELOW FLOOR |
| F53 | MISSING | `footer:links=prev-lesson,other,home-nav` | 2 | 2 | 0.00 | 0.00 | — | BELOW FLOOR |
| F54 | MISSING | `footer:links=none` | 1 | 1 | 0.00 | 0.00 | — | BELOW FLOOR |
| F55 | EXTRA | `footer:links=home-nav` | 1 | 1 | 0.03 | 0.97 | — | BELOW FLOOR |

### F1 · MISSING `header:title-h1-count=2` — CANDIDATE (pages 191 / modules 107)
- by template+ptype: Standard/overview 47m/47p gold 0.64 Claude 0.50 c=0.64; Standard/lesson 30m/92p gold 0.08 Claude 0.02 c=0.08; Fundamentals/overview 25m/25p gold 0.70 Claude 0.24 c=0.70; Inquiry/overview 6m/6p gold 0.55 Claude 0.43 c=0.55; Bilingual/overview 4m/4p gold 1.00 Claude 0.75 c=1.00; Bilingual/lesson 4m/11p gold 1.00 Claude 0.77 c=1.00; Inquiry/lesson 3m/6p gold 0.14 Claude 0.02 c=0.14
- by subject: 1-10 English 19m/19p gold 0.15 Claude 0.10 c=0.15; Leaving to Learn 15m/23p gold 0.26 Claude 0.17 c=0.26; Online Safety (OS9000) 13m/29p gold 0.33 Claude 0.11 c=0.33; NCEA1 12m/18p gold 0.13 Claude 0.09 c=0.13; 1-10 Mathematics 11m/11p gold 0.14 Claude 0.11 c=0.14; ConnectED 6m/6p gold 0.22 Claude 0.18 c=0.22; ANZH 5m/30p gold 0.55 Claude 0.17 c=0.55; 1-10 Arts 5m/5p gold 1.00 Claude 0.00 c=1.00
- **AGH1005** AGH1005_0_0.html ↔ AGH1005.00.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=3']
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ANZH104** ANZH104_4_0.html ↔ ANZH104_04.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1']
- modules: AGH1005, ANZH101, ANZH104, ANZH301, ANZH401, ANZH404, ARFUN01, ARFUN02, ARFUN03, ARFUN04, ARFUN05, ART1006, CEDK102, CEDK501, CEDO202, CEDO502, CEDR204, CEDT301, ENFUN01, ENFUN02, ENFUN03, ENFUN04, ENFUN05, ENFUN07 …

### F2 · EXTRA `header:title-h1-count=1` — CANDIDATE (pages 188 / modules 104)
- by template+ptype: Standard/overview 46m/46p gold 0.35 Claude 0.49 c=0.65; Standard/lesson 30m/92p gold 0.92 Claude 0.98 c=0.08; Fundamentals/overview 23m/23p gold 0.30 Claude 0.72 c=0.70; Inquiry/overview 6m/6p gold 0.45 Claude 0.57 c=0.55; Bilingual/overview 4m/4p gold 0.00 Claude 0.25 c=1.00; Bilingual/lesson 4m/11p gold 0.00 Claude 0.23 c=1.00; Inquiry/lesson 3m/6p gold 0.86 Claude 0.98 c=0.14
- by subject: 1-10 English 19m/19p gold 0.84 Claude 0.91 c=0.15; Leaving to Learn 15m/23p gold 0.74 Claude 0.83 c=0.26; Online Safety (OS9000) 13m/29p gold 0.67 Claude 0.89 c=0.33; NCEA1 11m/17p gold 0.86 Claude 0.90 c=0.14; 1-10 Mathematics 11m/11p gold 0.85 Claude 0.89 c=0.14; ConnectED 6m/6p gold 0.78 Claude 0.82 c=0.22; ANZH 5m/30p gold 0.45 Claude 0.83 c=0.55; 1-10 Technology 5m/5p gold 0.00 Claude 0.62 c=1.00
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ANZH104** ANZH104_4_0.html ↔ ANZH104_04.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1']
- **ANZH301** ANZH301_3_0.html ↔ ANZH301_3.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: ANZH101, ANZH104, ANZH301, ANZH401, ANZH404, ARFUN02, ARFUN03, ARFUN04, ARFUN05, ART1006, CEDK102, CEDK501, CEDO202, CEDO502, CEDR204, CEDT301, ENFUN01, ENFUN02, ENFUN03, ENFUN04, ENFUN05, ENFUN07, ENFUN08, ENFUN09 …

### F3 · MISSING `header:chip=decimal-number` — CANDIDATE (pages 85 / modules 43)
- by template+ptype: Standard/lesson 35m/76p gold 0.70 Claude 0.74 c=0.70; Standard/overview 5m/5p gold 0.02 Claude 0.00 c=0.02; Inquiry/overview 2m/2p gold 0.05 Claude 0.00 c=0.05; Bilingual/overview 2m/2p gold 0.12 Claude 0.00 c=0.12
- by subject: 1-10 Blended Literacy 23m/45p gold 0.40 Claude 0.28 c=0.40; 1-10 Mathematics 6m/10p gold 0.72 Claude 0.74 c=0.72; NCEA1 4m/4p gold 0.82 Claude 0.87 c=0.82; Leaving to Learn 4m/12p gold 0.41 Claude 0.53 c=0.41; 1-10 English 2m/9p gold 0.59 Claude 0.66 c=0.59; Te Marautanga o Aotearoa TMoA 2m/2p gold 0.62 Claude 0.67 c=0.62; ConnectED 1m/1p gold 0.71 Claude 0.73 c=0.71; 1-10 Social Science 1m/2p gold 0.47 Claude 0.42 c=0.47
- **ART1004** ART1004_0_0.html ↔ ART1004_4.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **ART1005** ART1005_0_0.html ↔ ART1005_3.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **BLL141** BLL141_1_0.html ↔ BLL141-1.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- modules: ART1004, ART1005, BLL141, BLL142, BLL143, BLL144, BLL145, BLL146, BLL147, BLL151, BLL152, BLL154, BLL156, BLL157, BLL161, BLL162, BLL163, BLL164, BLL165, BLL166, BLL167, BLL171, BLL172, BLL173 …

### F4 · EXTRA `header:chip=decimal-number` — BELOW CONSENSUS (no group ≥ 0.60 at the floor) (pages 161 / modules 39)
- by template+ptype: Standard/lesson 31m/131p gold 0.70 Claude 0.74 c=0.30; Inquiry/lesson 7m/25p gold 0.49 Claude 1.00 c=0.51; Bilingual/lesson 1m/5p gold 0.79 Claude 0.89 c=0.21
- by subject: Leaving to Learn 8m/38p gold 0.41 Claude 0.53 c=0.59; 1-10 English 7m/30p gold 0.59 Claude 0.66 c=0.41; 1-10 Blended Literacy 5m/15p gold 0.40 Claude 0.28 c=0.60; NCEA1 5m/21p gold 0.82 Claude 0.87 c=0.18; 1-10 Mathematics 5m/18p gold 0.72 Claude 0.74 c=0.28; ConnectED 3m/3p gold 0.71 Claude 0.73 c=0.29; None 3m/23p gold 0.28 Claude 0.78 c=0.72; ANZH 2m/8p gold 0.54 Claude 0.64 c=0.46
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ANZH203** ANZH203_1_0.html ↔ ANZH203_1.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **BLL236** BLL236_1_0.html ↔ BLL236-1.0.html: gold ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1']
- modules: ANZH101, ANZH203, BLL236, BLL240, BLL253, BLL262, BLL263, CEDK501, CEDT207, CEDT301, ENGI101, ENGI102, ENGJ201, ENGR102, ENGR201, ENGS301, ENGS401, HES1006, HIS1001, HIS1002, HIS1003, MXEX101, MXFL101, MXFL102 …

### F5 · EXTRA `header:chip=lesson-number` — CANDIDATE (pages 76 / modules 33)
- by template+ptype: Standard/lesson 31m/72p gold 0.26 Claude 0.23 c=0.74; Bilingual/lesson 2m/4p gold 0.02 Claude 0.11 c=0.98
- by subject: 1-10 Blended Literacy 22m/44p gold 0.24 Claude 0.37 c=0.76; Leaving to Learn 5m/15p gold 0.40 Claude 0.30 c=0.60; 1-10 English 2m/9p gold 0.22 Claude 0.18 c=0.78; Te Marautanga o Aotearoa TMoA 2m/4p gold 0.02 Claude 0.08 c=0.98; ConnectED 1m/1p gold 0.07 Claude 0.07 c=0.94; 1-10 Mathematics 1m/3p gold 0.10 Claude 0.11 c=0.90
- **BLL141** BLL141_1_0.html ↔ BLL141-1.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- **BLL142** BLL142_1_0.html ↔ BLL142-1.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- **BLL143** BLL143_1_0.html ↔ BLL143-1.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- modules: BLL141, BLL142, BLL143, BLL144, BLL145, BLL146, BLL147, BLL151, BLL152, BLL154, BLL156, BLL157, BLL161, BLL162, BLL163, BLL164, BLL165, BLL166, BLL167, BLL171, BLL172, BLL173, CEDR501, ENGJ101 …

### F6 · MISSING `header:chip=module-code` — BELOW CONSENSUS (no group ≥ 0.60 at the floor) (pages 65 / modules 33)
- by template+ptype: Standard/lesson 18m/44p gold 0.03 Claude 0.00 c=0.03; Standard/overview 8m/8p gold 0.70 Claude 0.72 c=0.70; Inquiry/lesson 3m/3p gold 0.06 Claude 0.00 c=0.06; Bilingual/lesson 3m/9p gold 0.19 Claude 0.00 c=0.19; Inquiry/overview 1m/1p gold 0.31 Claude 0.41 c=0.31
- by subject: 1-10 Blended Literacy 9m/9p gold 0.05 Claude 0.02 c=0.05; 1-10 Mathematics 5m/18p gold 0.16 Claude 0.11 c=0.16; NCEA1 4m/4p gold 0.13 Claude 0.13 c=0.13; Te Marautanga o Aotearoa TMoA 3m/9p gold 0.36 Claude 0.25 c=0.36; Leaving to Learn 3m/5p gold 0.15 Claude 0.17 c=0.15; ConnectED 2m/2p gold 0.09 Claude 0.07 c=0.09; 1-10 English 2m/2p gold 0.14 Claude 0.13 c=0.14; EXPlore 2m/2p gold 0.27 Claude 0.13 c=0.27
- **ANZH401** ANZH401_1_0.html ↔ ANZH401_1.0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **BLL170** BLL170_0_0.html ↔ BLL170.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **BLL172** BLL172_0_0.html ↔ BLL172-00.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: ANZH401, BLL170, BLL172, BLL174, BLL175, BLL176, BLL177, BLL240, BLL252, BLL253, BLLR201, CEDK501, CEDT207, ENGR102, ENGS401, EXBP901, EXIP901, HES1006, HIS1002, HIS1003, MXEX101, MXFL101, MXFL102, MXFL104 …

### F7 · EXTRA `header:menu-content` — BELOW CONSENSUS (no group ≥ 0.60 at the floor) (pages 39 / modules 25)
- by template+ptype: Standard/lesson 17m/31p gold 0.72 Claude 0.72 c=0.28; Standard/overview 3m/3p gold 0.97 Claude 0.99 c=0.03; Bilingual/overview 3m/3p gold 0.81 Claude 1.00 c=0.19; Inquiry/lesson 2m/2p gold 0.71 Claude 0.69 c=0.29
- by subject: ConnectED 6m/15p gold 0.76 Claude 0.87 c=0.24; NCEA1 5m/7p gold 0.71 Claude 0.73 c=0.29; 1-10 Mathematics 5m/8p gold 0.76 Claude 0.78 c=0.24; 1-10 English 4m/4p gold 0.96 Claude 0.97 c=0.04; Te Marautanga o Aotearoa TMoA 3m/3p gold 0.21 Claude 0.25 c=0.79; 1-10 Blended Literacy 1m/1p gold 0.38 Claude 0.38 c=0.62; Leaving to Learn 1m/1p gold 0.87 Claude 0.83 c=0.13
- **ART1005** ART1005_0_0.html ↔ ART1005_3.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **BLL240** BLL240_1_1.html ↔ BLL240-1.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **CEDK501** CEDK501_6_0.html ↔ CEDK501_4.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: ART1005, BLL240, CEDK501, CEDO501, CEDO502, CEDR501, CEDT501, CEDW501, ENG1004, ENGC302, ENGI401, ENGI405, ENGS201, MXEO201, MXEO301, MXEX301, MXFL104, MXFU201, PES1002, PES1004, PES1008, TRR107, TRR112, TRR113 …

### F8 · MISSING `header:chip=lesson-number` — BELOW CONSENSUS (no group ≥ 0.60 at the floor) (pages 128 / modules 23)
- by template+ptype: Standard/lesson 19m/107p gold 0.26 Claude 0.23 c=0.26; Inquiry/lesson 4m/21p gold 0.43 Claude 0.00 c=0.43
- by subject: Leaving to Learn 7m/37p gold 0.40 Claude 0.30 c=0.40; 1-10 Blended Literacy 4m/12p gold 0.24 Claude 0.37 c=0.24; 1-10 English 4m/22p gold 0.22 Claude 0.18 c=0.22; None 3m/23p gold 0.50 Claude 0.00 c=0.50; ANZH 2m/8p gold 0.10 Claude 0.00 c=0.10; NCEA1 2m/17p gold 0.05 Claude 0.00 c=0.05; 1-10 Social Science 1m/9p gold 0.24 Claude 0.00 c=0.24
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ANZH203** ANZH203_1_0.html ↔ ANZH203_1.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **BLL240** BLL240_1_2.html ↔ BLL240-2.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: ANZH101, ANZH203, BLL240, BLL253, BLL262, BLL263, ENGI101, ENGI102, ENGR201, ENGS301, HIS1001, HIS1002, SCPH301, SSCI205, TEDC401, TEDC402, XDLS901, XDLS902, XDLS903, XDLS904, XDLS905, XDLS909, XLP01

### F9 · EXTRA `header:head-buttons` — BELOW CONSENSUS (no group ≥ 0.60 at the floor) (pages 34 / modules 23)
- by template+ptype: Standard/lesson 15m/26p gold 0.73 Claude 0.72 c=0.27; Standard/overview 3m/3p gold 0.98 Claude 0.99 c=0.02; Inquiry/lesson 2m/2p gold 0.71 Claude 0.69 c=0.29; Bilingual/overview 2m/2p gold 0.88 Claude 1.00 c=0.12; Fundamentals/overview 1m/1p gold 0.77 Claude 0.79 c=0.23
- by subject: ConnectED 6m/15p gold 0.76 Claude 0.87 c=0.24; NCEA1 5m/7p gold 0.71 Claude 0.73 c=0.29; 1-10 Mathematics 4m/4p gold 0.78 Claude 0.78 c=0.22; 1-10 English 3m/3p gold 0.96 Claude 0.97 c=0.04; Te Marautanga o Aotearoa TMoA 2m/2p gold 0.38 Claude 0.25 c=0.62; 1-10 Blended Literacy 1m/1p gold 0.41 Claude 0.38 c=0.59; 1-10 Technology 1m/1p gold 0.00 Claude 0.12 c=1.00; Leaving to Learn 1m/1p gold 0.88 Claude 0.83 c=0.12
- **ART1005** ART1005_0_0.html ↔ ART1005_3.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **BLL240** BLL240_1_1.html ↔ BLL240-1.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **CEDK501** CEDK501_6_0.html ↔ CEDK501_4.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: ART1005, BLL240, CEDK501, CEDO501, CEDO502, CEDR501, CEDT501, CEDW501, ENG1004, ENGC302, ENGI401, ENGS201, MXEO301, MXEX301, MXFL104, MXFU201, PES1002, PES1004, PES1008, TEFUN07, TRR112, TRR113, XGF9001

### F10 · EXTRA `header:chip=module-code` — CANDIDATE (pages 22 / modules 22)
- by template+ptype: Standard/overview 11m/11p gold 0.70 Claude 0.72 c=0.29; Inquiry/overview 5m/5p gold 0.31 Claude 0.41 c=0.69; Fundamentals/overview 4m/4p gold 0.47 Claude 0.55 c=0.53; Bilingual/overview 2m/2p gold 0.88 Claude 1.00 c=0.12
- by subject: Leaving to Learn 9m/9p gold 0.15 Claude 0.17 c=0.85; NCEA1 4m/4p gold 0.13 Claude 0.13 c=0.87; 1-10 Health and PE 2m/2p gold 0.87 Claude 1.00 c=0.13; 1-10 Social Science 2m/2p gold 0.26 Claude 0.29 c=0.74; Te Marautanga o Aotearoa TMoA 2m/2p gold 0.36 Claude 0.25 c=0.64; 1-10 Blended Literacy 1m/1p gold 0.05 Claude 0.02 c=0.95; 1-10 Mathematics 1m/1p gold 0.16 Claude 0.11 c=0.84; Online Safety (OS9000) 1m/1p gold 0.21 Claude 0.21 c=0.79
- **ART1004** ART1004_0_0.html ↔ ART1004_4.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **ART1005** ART1005_0_0.html ↔ ART1005_3.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **BLL240** BLL240_0_0.html ↔ BLL240-0.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: ART1004, ART1005, BLL240, ENG1004, ENGFUN02, HPFUN201, HPFUN302, MXDB201, OSOH101, SSFUN01, SSFUN07, TRR112, TRR113, XDLS901, XDLS902, XDLS903, XDLS909, XFUN01, XGF9001, XLP01, XLP02, XLP06

### F11 · MISSING `header:head-buttons` — CANDIDATE (pages 52 / modules 19)
- by template+ptype: Standard/lesson 12m/37p gold 0.73 Claude 0.72 c=0.73; Bilingual/lesson 4m/10p gold 0.21 Claude 0.00 c=0.21; Inquiry/lesson 2m/3p gold 0.71 Claude 0.69 c=0.71; Standard/overview 2m/2p gold 0.98 Claude 0.99 c=0.98
- by subject: 1-10 Blended Literacy 4m/8p gold 0.41 Claude 0.38 c=0.41; Te Marautanga o Aotearoa TMoA 4m/10p gold 0.38 Claude 0.25 c=0.38; Leaving to Learn 3m/12p gold 0.88 Claude 0.83 c=0.88; ConnectED 2m/3p gold 0.76 Claude 0.87 c=0.76; Online Safety (OS9000) 2m/9p gold 1.00 Claude 0.93 c=1.00; None 1m/6p gold 1.00 Claude 0.87 c=1.00; EXPlore 1m/1p gold 1.00 Claude 0.93 c=1.00; NCEA1 1m/1p gold 0.71 Claude 0.73 c=0.71
- **BLL114** BLL114_1_0.html ↔ BLL114-02.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- **BLL116** BLL116_1_0.html ↔ BLL116-02.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- **BLL153** BLL153_1_0.html ↔ BLL153-1.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- modules: BLL114, BLL116, BLL153, BLL236, BLLR201, CEDT207, CEDT301, EXPFUN07, HES1006, MXFL401, OSSC401, OSSC501, PNR101, PNR102, PNR104, TRR109, XGF9002, XGF9004, XLP06

### F12 · EXTRA `header:chip=other` — CANDIDATE (pages 39 / modules 17)
- by template+ptype: Standard/lesson 9m/31p gold 0.01 Claude 0.03 c=0.99; Standard/overview 8m/8p gold 0.28 Claude 0.28 c=0.72
- by subject: 1-10 Blended Literacy 7m/7p gold 0.29 Claude 0.31 c=0.71; 1-10 Mathematics 5m/7p gold 0.00 Claude 0.02 c=1.00; 1-10 Social Science 2m/11p gold 0.00 Claude 0.29 c=1.00; ANZH 1m/12p gold 0.08 Claude 0.23 c=0.92; None 1m/1p gold 0.00 Claude 0.02 c=1.00; Leaving to Learn 1m/1p gold 0.04 Claude 0.01 c=0.96
- **ANZH401** ANZH401_1_0.html ↔ ANZH401_1.0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **BLL172** BLL172_0_0.html ↔ BLL172-00.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **BLL174** BLL174_0_0.html ↔ BLL174-00.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: ANZH401, BLL172, BLL174, BLL175, BLL176, BLL177, BLL252, BLL253, BLLR201, MXDB301, MXEO301, MXEX301, MXFL302, MXFU302, SSCI205, SSFUN07, XLP01

### F13 · MISSING `header:chip=other` — BELOW CONSENSUS (no group ≥ 0.60 at the floor) (pages 19 / modules 13)
- by template+ptype: Standard/overview 7m/7p gold 0.28 Claude 0.28 c=0.28; Standard/lesson 3m/9p gold 0.01 Claude 0.03 c=0.01; Inquiry/overview 3m/3p gold 0.07 Claude 0.00 c=0.07
- by subject: Leaving to Learn 8m/8p gold 0.04 Claude 0.01 c=0.04; 1-10 Blended Literacy 2m/3p gold 0.29 Claude 0.31 c=0.29; 1-10 English 1m/6p gold 0.02 Claude 0.00 c=0.02; 1-10 Mathematics 1m/1p gold 0.00 Claude 0.02 c=0.00; Online Safety (OS9000) 1m/1p gold 0.01 Claude 0.00 c=0.01
- **BLL111** BLL111_0_0.html ↔ BLL111-01.html: gold ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number(00)', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **BLL236** BLL236_1_0.html ↔ BLL236-1.0.html: gold ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1']
- **ENGJ201** ENGJ201_1_0.html ↔ ENGJ201_1.0.html: gold ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: BLL111, BLL236, ENGJ201, MXDB201, OSOH101, XDLS901, XDLS902, XDLS903, XDLS909, XDLS911, XLP01, XLP02, XLP06

### F14 · MISSING `header:title-h1-count=1` — CANDIDATE (pages 12 / modules 12)
- by template+ptype: Standard/overview 8m/8p gold 0.35 Claude 0.49 c=0.35; Standard/lesson 2m/2p gold 0.92 Claude 0.98 c=0.92; Inquiry/overview 1m/1p gold 0.45 Claude 0.57 c=0.45; Fundamentals/overview 1m/1p gold 0.30 Claude 0.72 c=0.30
- by subject: NCEA1 4m/4p gold 0.86 Claude 0.90 c=0.86; Leaving to Learn 4m/4p gold 0.74 Claude 0.83 c=0.74; 1-10 Blended Literacy 1m/1p gold 1.00 Claude 1.00 c=1.00; ConnectED 1m/1p gold 0.78 Claude 0.82 c=0.78; 1-10 English 1m/1p gold 0.84 Claude 0.91 c=0.84; 1-10 Social Science 1m/1p gold 0.71 Claude 0.79 c=0.71
- **ART1004** ART1004_0_0.html ↔ ART1004_4.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **ART1005** ART1005_0_0.html ↔ ART1005_3.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **BLL246** BLL246_0_0.html ↔ BLL246_0.0.html: gold ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2']
- modules: ART1004, ART1005, BLL246, CEDO105, ENGFUN02, ENGI103, HIS1002, SSFUN07, XDLS904, XDLS906, XFUN02, XGF9004

### F15 · EXTRA `header:title-h1-count=2` — CANDIDATE (pages 11 / modules 11)
- by template+ptype: Standard/overview 7m/7p gold 0.64 Claude 0.50 c=0.36; Standard/lesson 2m/2p gold 0.08 Claude 0.02 c=0.92; Inquiry/overview 1m/1p gold 0.55 Claude 0.43 c=0.45; Fundamentals/overview 1m/1p gold 0.70 Claude 0.24 c=0.30
- by subject: Leaving to Learn 4m/4p gold 0.26 Claude 0.17 c=0.74; NCEA1 3m/3p gold 0.13 Claude 0.09 c=0.87; 1-10 Blended Literacy 1m/1p gold 0.00 Claude 0.00 c=1.00; ConnectED 1m/1p gold 0.22 Claude 0.18 c=0.78; 1-10 English 1m/1p gold 0.15 Claude 0.10 c=0.84; 1-10 Social Science 1m/1p gold 0.29 Claude 0.18 c=0.71
- **BLL246** BLL246_0_0.html ↔ BLL246_0.0.html: gold ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2']
- **CEDO105** CEDO105_0_0.html ↔ CEDO105.0.0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2']
- **ENGFUN02** ENGFUN02_0_0.html ↔ ENGFUN02_0.1.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:title-h1-count=2']
- modules: BLL246, CEDO105, ENGFUN02, ENGI103, HIS1002, PHE1004, SSFUN07, XDLS904, XDLS906, XFUN02, XGF9004

### F23 · MISSING `nav:crumbs` — BELOW CONSENSUS (no group ≥ 0.60 at the floor) (pages 10 / modules 10)
- by template+ptype: Inquiry/overview 7m/7p gold 0.86 Claude 0.69 c=0.86; Inquiry/lesson 2m/2p gold 0.04 Claude 0.00 c=0.04; Standard/lesson 1m/1p gold 0.00 Claude 0.00 c=0.00
- by subject: ConnectED 6m/6p gold 0.13 Claude 0.07 c=0.13; Te ara Whakapuawa -Wellbeing 2m/2p gold 1.00 Claude 0.75 c=1.00; 1-10 Blended Literacy 1m/1p gold 0.04 Claude 0.04 c=0.04; EXPlore 1m/1p gold 0.73 Claude 0.67 c=0.73
- **BLL240** BLL240_1_0.html ↔ BLL240.html: gold ['nav:crumbs'] · Claude []
- **CEDK501** CEDK501_0_0.html ↔ CEDK501 Kia Mahitahi – Idea to Action.html: gold ['nav:crumbs'] · Claude []
- **CEDT104** CEDT104_0_0.html ↔ CEDT104 Waiata In Motion.html: gold ['nav:crumbs'] · Claude []
- modules: BLL240, CEDK501, CEDT104, CEDT207, CEDT208, CEDT301, CEDW201, EXIP901, TWHA905, TWHK901

### F26 · MISSING `footer:inside-body` — BELOW CONSENSUS (no group ≥ 0.60 at the floor) (pages 144 / modules 111)
- by template+ptype: Standard/lesson 56m/75p gold 0.05 Claude 0.00 c=0.05; Standard/overview 41m/41p gold 0.14 Claude 0.00 c=0.14; Fundamentals/overview 15m/15p gold 0.28 Claude 0.00 c=0.28; Inquiry/overview 9m/9p gold 0.21 Claude 0.00 c=0.21; Inquiry/lesson 2m/2p gold 0.04 Claude 0.00 c=0.04; Fundamentals/lesson 1m/1p gold 0.09 Claude 0.00 c=0.09; Bilingual/lesson 1m/1p gold 0.02 Claude 0.00 c=0.02
- by subject: 1-10 Blended Literacy 34m/44p gold 0.17 Claude 0.00 c=0.17; 1-10 English 16m/21p gold 0.07 Claude 0.00 c=0.07; 1-10 Mathematics 15m/28p gold 0.08 Claude 0.00 c=0.08; Leaving to Learn 10m/11p gold 0.05 Claude 0.00 c=0.05; None 7m/7p gold 0.15 Claude 0.00 c=0.15; NCEA1 6m/10p gold 0.03 Claude 0.00 c=0.03; Te ara Whakapuawa -Wellbeing 5m/5p gold 0.62 Claude 0.00 c=0.62; 1-10 Arts 4m/4p gold 0.80 Claude 0.00 c=0.80
- **ANZH101** ANZH101_0_0.html ↔ ANZH101_0.0.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ARFUN02** ARFUN02_0_0.html ↔ ARFUN02.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav fundamentals-nav'] · Claude ['footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav fundamentals-nav']
- **ARFUN03** ARFUN03_0_0.html ↔ ARFUN03.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav fundamentals-nav'] · Claude ['footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav fundamentals-nav']
- modules: ANZH101, ARFUN02, ARFUN03, ARFUN04, ARFUN05, BLL113, BLL120, BLL122, BLL124, BLL125, BLL130, BLL145, BLL154, BLL156, BLL162, BLL164, BLL165, BLL166, BLL171, BLL173, BLL211, BLL212, BLL213, BLL214 …

### F27 · EXTRA `footer:links=next-lesson,home-nav` — CANDIDATE (pages 91 / modules 91)
- by template+ptype: Standard/overview 74m/74p gold 0.73 Claude 0.99 c=0.27; Inquiry/overview 8m/8p gold 0.02 Claude 0.19 c=0.98; Fundamentals/overview 7m/7p gold 0.02 Claude 0.15 c=0.98; Bilingual/overview 2m/2p gold 0.88 Claude 1.00 c=0.12
- by subject: Leaving to Learn 27m/27p gold 0.03 Claude 0.17 c=0.97; 1-10 Mathematics 13m/13p gold 0.07 Claude 0.11 c=0.93; NCEA1 11m/11p gold 0.10 Claude 0.13 c=0.90; Online Safety (OS9000) 9m/9p gold 0.15 Claude 0.21 c=0.85; 1-10 English 8m/8p gold 0.11 Claude 0.13 c=0.89; 1-10 Blended Literacy 6m/6p gold 0.30 Claude 0.31 c=0.70; 1-10 Social Science 6m/6p gold 0.13 Claude 0.29 c=0.87; ConnectED 5m/5p gold 0.07 Claude 0.09 c=0.94
- **ANZH401** ANZH401_0_0.html ↔ ANZH401_0.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH404** ANZH404_0_0.html ↔ ANZH404_0.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ART1004** ART1004_0_0.html ↔ ART1004_4.0.html: gold ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: ANZH401, ANZH404, ART1004, ART1005, BLL114, BLL116, BLL174, BLL175, BLL176, BLL177, BLLR201, CEDO301, CEDT104, CEDT207, CEDT208, CEDT301, ENG1004, ENGFUN02, ENGI101, ENGI102, ENGJ101, ENGJ102, ENGJ301, ENGJ302 …

### F28 · EXTRA `footer:links=prev-lesson,next-lesson,home-nav` — CANDIDATE (pages 222 / modules 85)
- by template+ptype: Standard/lesson 44m/169p gold 0.73 Claude 0.82 c=0.27; Inquiry/overview 22m/22p gold 0.19 Claude 0.71 c=0.81; Fundamentals/overview 12m/12p gold 0.07 Claude 0.28 c=0.93; Inquiry/lesson 6m/16p gold 0.53 Claude 0.84 c=0.47; Bilingual/lesson 2m/2p gold 0.81 Claude 0.66 c=0.19; Standard/overview 1m/1p gold 0.02 Claude 0.01 c=0.98
- by subject: 1-10 Health and PE 12m/12p gold 0.20 Claude 1.00 c=0.80; NCEA1 10m/25p gold 0.72 Claude 0.77 c=0.28; ConnectED 10m/16p gold 0.68 Claude 0.81 c=0.32; Leaving to Learn 10m/39p gold 0.52 Claude 0.69 c=0.48; 1-10 Blended Literacy 9m/10p gold 0.40 Claude 0.38 c=0.60; 1-10 Mathematics 9m/52p gold 0.62 Claude 0.77 c=0.38; 1-10 English 8m/34p gold 0.62 Claude 0.71 c=0.38; Te ara Whakapuawa -Wellbeing 6m/6p gold 0.00 Claude 0.75 c=1.00
- **AGH1008** AGH1008_8_0.html ↔ AGH1008.08.html: gold ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH401** ANZH401_1_0.html ↔ ANZH401_1.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH404** ANZH404_1_0.html ↔ ANZH404_1.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: AGH1008, ANZH401, ANZH404, ART1002, BLL120, BLL140, BLL150, BLL170, BLL175, BLL210, BLL220, BLL230, BLL240, CEDK101, CEDK102, CEDK501, CEDO102, CEDO202, CEDO301, CEDR204, CEDT207, CEDT301, CEDW201, ENGFUN02 …

### F29 · MISSING `footer:links=home-nav,next-lesson` — BELOW CONSENSUS (no group ≥ 0.60 at the floor) (pages 69 / modules 68)
- by template+ptype: Standard/overview 60m/60p gold 0.21 Claude 0.00 c=0.21; Standard/lesson 6m/6p gold 0.00 Claude 0.00 c=0.00; Inquiry/overview 2m/2p gold 0.05 Claude 0.00 c=0.05; Fundamentals/overview 1m/1p gold 0.02 Claude 0.00 c=0.02
- by subject: Leaving to Learn 20m/20p gold 0.10 Claude 0.00 c=0.10; 1-10 Mathematics 14m/14p gold 0.04 Claude 0.00 c=0.04; Online Safety (OS9000) 9m/9p gold 0.07 Claude 0.00 c=0.07; 1-10 English 8m/8p gold 0.03 Claude 0.00 c=0.03; NCEA1 7m/7p gold 0.02 Claude 0.00 c=0.02; 1-10 Blended Literacy 6m/6p gold 0.02 Claude 0.00 c=0.02; ANZH 2m/2p gold 0.03 Claude 0.00 c=0.03; EXPlore 2m/3p gold 0.20 Claude 0.00 c=0.20
- **ANZH401** ANZH401_0_0.html ↔ ANZH401_0.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH404** ANZH404_0_0.html ↔ ANZH404_0.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **BLL114** BLL114_0_0.html ↔ BLL114-01.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: ANZH401, ANZH404, BLL114, BLL116, BLL174, BLL175, BLL176, BLL177, ENGI101, ENGI102, ENGJ101, ENGJ102, ENGJ301, ENGJ302, ENGJ402, ENGJ403, EXBP901, EXIP901, HIS1001, HIS1002, HIS1004, HIS1005, HIS1006, HIS1007 …

### F30 · EXTRA `footer:links=prev-lesson,home-nav` — CANDIDATE (pages 67 / modules 67)
- by template+ptype: Standard/lesson 54m/54p gold 0.17 Claude 0.18 c=0.83; Bilingual/lesson 10m/10p gold 0.15 Claude 0.34 c=0.85; Inquiry/lesson 3m/3p gold 0.22 Claude 0.16 c=0.78
- by subject: 1-10 Blended Literacy 16m/16p gold 0.25 Claude 0.31 c=0.75; 1-10 English 11m/11p gold 0.10 Claude 0.13 c=0.90; Te Marautanga o Aotearoa TMoA 10m/10p gold 0.11 Claude 0.25 c=0.89; 1-10 Mathematics 8m/8p gold 0.09 Claude 0.11 c=0.91; NCEA1 7m/7p gold 0.11 Claude 0.10 c=0.89; Leaving to Learn 4m/4p gold 0.29 Claude 0.15 c=0.71; ANZH 3m/3p gold 0.09 Claude 0.13 c=0.91; ConnectED 3m/3p gold 0.05 Claude 0.07 c=0.95
- **AGH1004** AGH1004_6_0.html ↔ AGH1004.07.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **AGH1009** AGH1009_9_0.html ↔ AGH1009.09.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH205** ANZH205_6_0.html ↔ ANZH205_06.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: AGH1004, AGH1009, ANZH205, ANZH301, ANZH303, BLL141, BLL146, BLL151, BLL157, BLL167, BLL171, BLL176, BLL177, BLL224, BLL225, BLL226, BLL227, BLL231, BLL234, BLL236, BLL237, BLLR201, CEDO501, CEDT207 …

### F31 · MISSING `footer:link=next-lesson` — CANDIDATE (pages 57 / modules 57)
- by template+ptype: Standard/lesson 46m/46p gold 0.82 Claude 0.82 c=0.82; Bilingual/lesson 9m/9p gold 0.81 Claude 0.66 c=0.81; Inquiry/lesson 2m/2p gold 0.69 Claude 0.84 c=0.69
- by subject: 1-10 Blended Literacy 16m/16p gold 0.74 Claude 0.69 c=0.74; Te Marautanga o Aotearoa TMoA 9m/9p gold 0.86 Claude 0.75 c=0.86; 1-10 English 7m/7p gold 0.86 Claude 0.84 c=0.86; 1-10 Mathematics 7m/7p gold 0.90 Claude 0.88 c=0.90; NCEA1 5m/5p gold 0.87 Claude 0.90 c=0.87; ANZH 3m/3p gold 0.91 Claude 0.87 c=0.91; ConnectED 3m/3p gold 0.94 Claude 0.93 c=0.94; Leaving to Learn 3m/3p gold 0.65 Claude 0.85 c=0.65
- **AGH1004** AGH1004_6_0.html ↔ AGH1004.07.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **AGH1009** AGH1009_9_0.html ↔ AGH1009.09.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH205** ANZH205_6_0.html ↔ ANZH205_06.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: AGH1004, AGH1009, ANZH205, ANZH301, ANZH303, BLL141, BLL146, BLL151, BLL157, BLL167, BLL171, BLL176, BLL177, BLL224, BLL225, BLL226, BLL227, BLL231, BLL234, BLL236, BLL237, BLLR201, CEDO501, CEDT207 …

### F32 · MISSING `footer:links=prev-lesson,next-lesson,home-nav` — CANDIDATE (pages 57 / modules 54)
- by template+ptype: Standard/lesson 39m/39p gold 0.73 Claude 0.82 c=0.73; Bilingual/lesson 9m/9p gold 0.81 Claude 0.66 c=0.81; Standard/overview 5m/5p gold 0.02 Claude 0.01 c=0.02; Bilingual/overview 2m/2p gold 0.12 Claude 0.00 c=0.12; Inquiry/lesson 1m/1p gold 0.53 Claude 0.84 c=0.53; Fundamentals/overview 1m/1p gold 0.07 Claude 0.28 c=0.07
- by subject: 1-10 Blended Literacy 14m/14p gold 0.40 Claude 0.38 c=0.40; Te Marautanga o Aotearoa TMoA 9m/11p gold 0.64 Claude 0.49 c=0.64; NCEA1 8m/8p gold 0.72 Claude 0.77 c=0.72; 1-10 English 6m/6p gold 0.62 Claude 0.71 c=0.62; Leaving to Learn 4m/4p gold 0.52 Claude 0.69 c=0.52; ANZH 3m/3p gold 0.58 Claude 0.74 c=0.58; 1-10 Mathematics 3m/3p gold 0.62 Claude 0.77 c=0.62; ConnectED 2m/2p gold 0.68 Claude 0.81 c=0.68
- **AGH1004** AGH1004_6_0.html ↔ AGH1004.07.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **AGH1009** AGH1009_9_0.html ↔ AGH1009.09.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH205** ANZH205_6_0.html ↔ ANZH205_06.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: AGH1004, AGH1009, ANZH205, ANZH301, ANZH303, ART1005, BLL141, BLL146, BLL151, BLL157, BLL167, BLL171, BLL224, BLL225, BLL226, BLL227, BLL231, BLL234, BLL236, BLL237, BLLR201, CEDO501, CEDT207, ENG1004 …

### F33 · MISSING `footer:links=home-nav,prev-lesson,next-lesson` — CANDIDATE (pages 111 / modules 46)
- by template+ptype: Inquiry/overview 21m/21p gold 0.55 Claude 0.05 c=0.55; Fundamentals/overview 12m/12p gold 0.23 Claude 0.00 c=0.23; Standard/lesson 11m/76p gold 0.05 Claude 0.00 c=0.05; Inquiry/lesson 2m/2p gold 0.04 Claude 0.00 c=0.04
- by subject: 1-10 Health and PE 12m/12p gold 0.80 Claude 0.00 c=0.80; ConnectED 11m/11p gold 0.12 Claude 0.02 c=0.12; Te ara Whakapuawa -Wellbeing 6m/6p gold 0.75 Claude 0.00 c=0.75; 1-10 Blended Literacy 5m/5p gold 0.02 Claude 0.00 c=0.02; 1-10 English 5m/32p gold 0.10 Claude 0.00 c=0.10; 1-10 Mathematics 5m/40p gold 0.12 Claude 0.00 c=0.12; EXPlore 1m/1p gold 0.07 Claude 0.00 c=0.07; Online Safety (OS9000) 1m/4p gold 0.03 Claude 0.00 c=0.03
- **BLL170** BLL170_0_0.html ↔ BLL170.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=home-nav,prev-lesson,next-lesson', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL210** BLL210_0_0.html ↔ BLL210.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=home-nav,prev-lesson,next-lesson', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL220** BLL220_0_0.html ↔ BLL220.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=home-nav,prev-lesson,next-lesson', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL170, BLL210, BLL220, BLL230, BLL240, CEDK101, CEDK102, CEDK501, CEDO102, CEDO202, CEDR204, CEDT104, CEDT207, CEDT208, CEDT301, CEDW201, ENGJ101, ENGJ301, ENGJ302, ENGJ402, ENGJ403, EXPFUN06, HPFUN101, HPFUN102 …

### F34 · EXTRA `footer:link=next-lesson` — BELOW CONSENSUS (no group ≥ 0.60 at the floor) (pages 77 / modules 35)
- by template+ptype: Standard/lesson 20m/48p gold 0.82 Claude 0.82 c=0.18; Standard/overview 8m/8p gold 0.97 Claude 1.00 c=0.03; Inquiry/overview 5m/5p gold 0.83 Claude 0.95 c=0.17; Fundamentals/overview 5m/5p gold 0.34 Claude 0.43 c=0.66; Inquiry/lesson 2m/9p gold 0.69 Claude 0.84 c=0.31; Bilingual/lesson 2m/2p gold 0.81 Claude 0.66 c=0.19
- by subject: Leaving to Learn 11m/45p gold 0.65 Claude 0.85 c=0.35; NCEA1 7m/15p gold 0.87 Claude 0.90 c=0.13; 1-10 Social Science 6m/6p gold 0.79 Claude 0.95 c=0.21; 1-10 Blended Literacy 3m/3p gold 0.74 Claude 0.69 c=0.26; 1-10 English 2m/2p gold 0.86 Claude 0.84 c=0.14; Te Marautanga o Aotearoa TMoA 2m/2p gold 0.86 Claude 0.75 c=0.14; ConnectED 1m/1p gold 0.94 Claude 0.93 c=0.06; EXPlore 1m/1p gold 0.93 Claude 0.93 c=0.07
- **AGH1008** AGH1008_8_0.html ↔ AGH1008.08.html: gold ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ART1002** ART1002_5_0.html ↔ ART1002_2.0.html: gold ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ART1004** ART1004_0_0.html ↔ ART1004_4.0.html: gold ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: AGH1008, ART1002, ART1004, BLL120, BLL140, BLL150, CEDO301, ENGFUN02, ENGI401, ENGS201, EXPFUN07, HES1005, HES1007, HIS1005, MXFU202, SSFUN01, SSFUN03, SSFUN05, SSFUN06, SSFUN07, SSFUN08, TEDC402, TRR102, TRR203 …

### F35 · MISSING `footer:ul=footer-nav` — CANDIDATE (pages 75 / modules 26)
- by template+ptype: Standard/lesson 14m/36p gold 0.89 Claude 0.87 c=0.89; Standard/overview 11m/11p gold 0.74 Claude 0.70 c=0.74; Fundamentals/overview 8m/8p gold 0.49 Claude 0.38 c=0.49; Inquiry/overview 3m/3p gold 0.17 Claude 0.14 c=0.17; Inquiry/lesson 3m/17p gold 0.96 Claude 0.61 c=0.96
- by subject: 1-10 Blended Literacy 12m/41p gold 0.16 Claude 0.00 c=0.16; 1-10 Technology 5m/5p gold 0.62 Claude 0.00 c=0.62; ConnectED 4m/21p gold 0.87 Claude 0.69 c=0.87; EXPlore 2m/5p gold 0.53 Claude 0.27 c=0.53; 1-10 Mathematics 2m/2p gold 0.98 Claude 0.99 c=0.98; 1-10 Health and PE 1m/1p gold 0.27 Claude 0.20 c=0.27
- **BLL121** BLL121_0_0.html ↔ BLL121-01.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL172** BLL172_0_0.html ↔ BLL172-00.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL174** BLL174_0_0.html ↔ BLL174-00.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL121, BLL172, BLL174, BLL175, BLL176, BLL177, BLL236, BLL237, BLL240, BLL241, BLL244, BLL245, CEDR501, CEDT207, CEDT301, CEDW101, EXBP901, EXIP901, HPFUN301, MXFUN02, MXFUN03, TEFUN01, TEFUN02, TEFUN05 …

### F36 · EXTRA `footer:link=prev-lesson` — BELOW CONSENSUS (no group ≥ 0.60 at the floor) (pages 32 / modules 24)
- by template+ptype: Standard/lesson 15m/19p gold 0.99 Claude 1.00 c=0.01; Inquiry/overview 4m/4p gold 0.74 Claude 0.76 c=0.26; Inquiry/lesson 3m/6p gold 0.88 Claude 1.00 c=0.12; Standard/overview 1m/1p gold 0.03 Claude 0.01 c=0.97; Bilingual/lesson 1m/2p gold 0.96 Claude 1.00 c=0.04
- by subject: 1-10 Blended Literacy 7m/7p gold 0.66 Claude 0.69 c=0.34; NCEA1 5m/8p gold 0.86 Claude 0.87 c=0.14; EXPlore 3m/3p gold 0.73 Claude 0.93 c=0.27; ConnectED 2m/2p gold 0.92 Claude 0.91 c=0.08; 1-10 Mathematics 2m/2p gold 0.88 Claude 0.88 c=0.12; Leaving to Learn 2m/6p gold 0.81 Claude 0.83 c=0.19; 1-10 English 1m/1p gold 0.84 Claude 0.84 c=0.16; 1-10 Social Science 1m/1p gold 0.71 Claude 0.71 c=0.29
- **BLL120** BLL120_0_0.html ↔ BLL120.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL140** BLL140_0_0.html ↔ BLL140.html: gold ['footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL150** BLL150_0_0.html ↔ BLL150.html: gold ['footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL120, BLL140, BLL150, BLL175, BLL176, BLL177, BLL240, CEDK501, CEDT207, ENGFUN02, ENGR102, EXBP901, EXIP901, EXPFUN07, HES1006, HIS1002, HIS1003, MXEX101, MXFL201, PES1005, SSFUN07, TRR102, XDLS501, XWHA02

### F37 · EXTRA `footer:ul=footer-nav inquiry-nav` — CANDIDATE (pages 75 / modules 21)
- by template+ptype: Standard/lesson 15m/41p gold 0.10 Claude 0.13 c=0.90; Standard/overview 12m/12p gold 0.26 Claude 0.30 c=0.74; Inquiry/overview 3m/3p gold 0.83 Claude 0.86 c=0.17; Inquiry/lesson 3m/17p gold 0.04 Claude 0.39 c=0.96; Fundamentals/overview 2m/2p gold 0.00 Claude 0.04 c=1.00
- by subject: 1-10 Blended Literacy 12m/41p gold 0.84 Claude 1.00 c=0.16; ConnectED 4m/21p gold 0.13 Claude 0.31 c=0.87; EXPlore 2m/5p gold 0.47 Claude 0.73 c=0.53; 1-10 Mathematics 2m/2p gold 0.02 Claude 0.01 c=0.98; Leaving to Learn 1m/6p gold 0.02 Claude 0.04 c=0.98
- **BLL121** BLL121_0_0.html ↔ BLL121-01.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL172** BLL172_0_0.html ↔ BLL172-00.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL174** BLL174_0_0.html ↔ BLL174-00.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL121, BLL172, BLL174, BLL175, BLL176, BLL177, BLL236, BLL237, BLL240, BLL241, BLL244, BLL245, CEDR501, CEDT207, CEDT301, CEDW101, EXBP901, EXIP901, MXFUN02, MXFUN03, XWHA02

### F38 · MISSING `footer:links=prev-lesson,home-nav` — BELOW CONSENSUS (no group ≥ 0.60 at the floor) (pages 49 / modules 19)
- by template+ptype: Standard/lesson 16m/41p gold 0.17 Claude 0.18 c=0.17; Standard/overview 1m/1p gold 0.00 Claude 0.00 c=0.00; Bilingual/lesson 1m/1p gold 0.15 Claude 0.34 c=0.15; Inquiry/lesson 1m/6p gold 0.22 Claude 0.16 c=0.22
- by subject: Leaving to Learn 9m/34p gold 0.29 Claude 0.15 c=0.29; NCEA1 6m/11p gold 0.11 Claude 0.10 c=0.11; 1-10 English 2m/2p gold 0.10 Claude 0.13 c=0.10; None 1m/1p gold 0.07 Claude 0.07 c=0.07; Te Marautanga o Aotearoa TMoA 1m/1p gold 0.11 Claude 0.25 c=0.11
- **AGH1008** AGH1008_8_0.html ↔ AGH1008.08.html: gold ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ART1002** ART1002_5_0.html ↔ ART1002_2.0.html: gold ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ART1004** ART1004_0_0.html ↔ ART1004_4.0.html: gold ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: AGH1008, ART1002, ART1004, ENGI401, ENGS201, HES1005, HES1007, HIS1005, TEDC402, TRR203, XDLS501, XDLS902, XDLS903, XDLS904, XDLS905, XDLS906, XGF9004, XLP02, XMES102

### F39 · MISSING `footer:links=home-nav` — BELOW CONSENSUS (no group ≥ 0.60 at the floor) (pages 21 / modules 17)
- by template+ptype: Standard/overview 6m/6p gold 0.02 Claude 0.00 c=0.02; Inquiry/overview 5m/5p gold 0.17 Claude 0.05 c=0.17; Fundamentals/overview 5m/5p gold 0.64 Claude 0.57 c=0.64; Inquiry/lesson 1m/4p gold 0.08 Claude 0.00 c=0.08; Standard/lesson 1m/1p gold 0.00 Claude 0.00 c=0.00
- by subject: 1-10 Social Science 6m/6p gold 0.16 Claude 0.00 c=0.16; Leaving to Learn 6m/6p gold 0.03 Claude 0.00 c=0.03; 1-10 Blended Literacy 3m/3p gold 0.01 Claude 0.00 c=0.01; NCEA1 1m/5p gold 0.01 Claude 0.00 c=0.01; EXPlore 1m/1p gold 0.07 Claude 0.00 c=0.07
- **BLL120** BLL120_0_0.html ↔ BLL120.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL140** BLL140_0_0.html ↔ BLL140.html: gold ['footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL150** BLL150_0_0.html ↔ BLL150.html: gold ['footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL120, BLL140, BLL150, ENGFUN02, EXPFUN07, SSFUN01, SSFUN03, SSFUN05, SSFUN06, SSFUN07, SSFUN08, XDLS902, XDLS903, XDLS904, XDLS905, XDLS906, XDLS911

### F40 · MISSING `footer:link=prev-lesson` — CANDIDATE (pages 13 / modules 13)
- by template+ptype: Standard/overview 7m/7p gold 0.03 Claude 0.01 c=0.03; Inquiry/overview 3m/3p gold 0.74 Claude 0.76 c=0.74; Bilingual/overview 2m/2p gold 0.12 Claude 0.00 c=0.12; Fundamentals/overview 1m/1p gold 0.30 Claude 0.28 c=0.30
- by subject: NCEA1 4m/4p gold 0.86 Claude 0.87 c=0.86; ConnectED 3m/3p gold 0.92 Claude 0.91 c=0.92; Te Marautanga o Aotearoa TMoA 2m/2p gold 0.75 Claude 0.75 c=0.75; None 1m/1p gold 0.80 Claude 0.78 c=0.80; 1-10 Mathematics 1m/1p gold 0.88 Claude 0.88 c=0.88; 1-10 Social Science 1m/1p gold 0.71 Claude 0.71 c=0.71; Leaving to Learn 1m/1p gold 0.81 Claude 0.83 c=0.81
- **ART1004** ART1004_0_0.html ↔ ART1004_4.0.html: gold ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ART1005** ART1005_0_0.html ↔ ART1005_3.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **BLLR201** BLLR201_0_0.html ↔ BLLR201_0_0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: ART1004, ART1005, BLLR201, CEDT104, CEDT207, CEDT208, ENG1004, MXFL101, PES1002, SSFUN02, TRR112, TRR113, XGF9001


## The ranked queue — chrome regions first, then by modules affected

| # | region | dir | parent | gold form | Claude form | pages | modules | consensus (all) | best group | derivable | KB | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | module-code | EXTRA | `div#header` | `—` | `div#module-code` | 4 | 4 | 0.03 of 1956 | — | structure | yes | BELOW FLOOR |
| 2 | module-code | MISSING | `div#header` | `div#module-code` | `—` | 3 | 3 | 0.97 of 1956 | — | structure | yes | BELOW FLOOR |
| 3 | module-code | EXTRA | `div#module-code` | `—` | `h1` | 1 | 1 | 0.03 of 1956 | — | structure | yes | BELOW FLOOR |
| 4 | title | MISSING | `div#header` | `h1>span` | `—` | 189 | 105 | 0.22 of 1956 | subject+ptype=1-10 English/overview c=0.94 n=17 | 0.72 | yes | CANDIDATE |
| 5 | title | EXTRA | `div#header` | `—` | `h1>span` | 11 | 11 | 0.78 of 1956 | era=Refresh c=0.78 n=11 | structure | yes | CANDIDATE |
| 6 | title | MISSING | `span>span.sassoonI-text` | `span.sassoonI-text` | `—` | 14 | 4 | 0.01 of 1956 | — | 0.79 | — | BELOW FLOOR |
| 7 | title | SUBSTITUTED | `div#header` | `h1>span` | `div#module-head-buttons` | 3 | 3 | 1.00 of 1956 | — | structure | yes | BELOW FLOOR |
| 8 | title | MISSING | `div.titlebar` | `h1.moduleTitle>span.module-subtitle.text-lowercase` | `—` | 2 | 1 | 0.00 of 1956 | — | 1.00 | — | BELOW FLOOR |
| 9 | title | EXTRA | `span>span` | `—` | `span` | 1 | 1 | 0.99 of 1956 | — | structure | — | BELOW FLOOR |
| 10 | title | EXTRA | `h1>span` | `—` | `span` | 1 | 1 | 0.01 of 1956 | — | structure | — | BELOW FLOOR |
| 11 | title | EXTRA | `msub` | `—` | `mrow` | 1 | 1 | 1.00 of 1956 | — | structure | — | BELOW FLOOR |
| 12 | title | EXTRA | `mfrac` | `—` | `mrow` | 1 | 1 | 1.00 of 1956 | — | structure | — | BELOW FLOOR |
| 13 | title | EXTRA | `mrow` | `—` | `mi` | 1 | 1 | 1.00 of 1956 | — | structure | — | BELOW FLOOR |
| 14 | title | EXTRA | `msup` | `—` | `mrow` | 1 | 1 | 1.00 of 1956 | — | structure | — | BELOW FLOOR |
| 15 | title | MISSING | `h1>span` | `span` | `—` | 1 | 1 | 0.99 of 1956 | — | 1.00 | — | BELOW FLOOR |
| 16 | title | MISSING | `span>span` | `span` | `—` | 1 | 1 | 0.01 of 1956 | — | 1.00 | — | BELOW FLOOR |
| 17 | title | MISSING | `msup` | `mn` | `—` | 1 | 1 | 0.00 of 1956 | — | 1.00 | — | BELOW FLOOR |
| 18 | title | SUBSTITUTED | `msub` | `mi` | `mrow` | 1 | 1 | 0.00 of 1956 | — | structure | — | BELOW FLOOR |
| 19 | title | SUBSTITUTED | `msub` | `mi` | `mi` | 1 | 1 | 0.00 of 1956 | — | structure | — | BELOW FLOOR |
| 20 | title | SUBSTITUTED | `mfrac` | `mn` | `mrow` | 1 | 1 | 0.00 of 1956 | — | structure | — | BELOW FLOOR |
| 21 | title | SUBSTITUTED | `mfrac` | `mn` | `mn` | 1 | 1 | 0.00 of 1956 | — | structure | — | BELOW FLOOR |
| 22 | title | SUBSTITUTED | `msup` | `mi` | `mrow` | 1 | 1 | 0.00 of 1956 | — | structure | — | BELOW FLOOR |
| 23 | title | SUBSTITUTED | `div#header` | `h1>span` | `div#module-code` | 1 | 1 | 1.00 of 1956 | — | structure | yes | BELOW FLOOR |
| 24 | header | MISSING | `div#header` | `p` | `—` | 3 | 1 | 0.00 of 1956 | — | 0.00 | yes | BELOW FLOOR |
| 25 | header | SUBSTITUTED | `div#header` | `div.titlebar` | `h1>span` | 2 | 1 | 0.00 of 1956 | — | structure | yes | BELOW FLOOR |
| 26 | module-menu | SUBSTITUTED | `div.col-md-6.col-12.paddingR` | `p` | `h5` | 83 | 83 | 0.07 of 1956 | subject=1-10 Health and PE c=0.93 n=14 | structure | yes | CANDIDATE |
| 27 | module-menu | MISSING | `ul` | `li` | `—` | 107 | 72 | 0.11 of 1956 | subject+ptype=1-10 Blended Literacy/overview c=0.66 n=21 | 0.88 | — | CANDIDATE |
| 28 | module-menu | EXTRA | `div.row` | `—` | `div.col-md-6.col-12.paddingR` | 64 | 47 | 0.96 of 1956 | template=Standard c=0.96 n=40 | structure | yes | CANDIDATE |
| 29 | module-menu | EXTRA | `ul` | `—` | `li` | 67 | 39 | 0.77 of 1956 | ptype=lesson c=0.83 n=12 | structure | — | CANDIDATE |
| 30 | module-menu | SUBSTITUTED | `div.col-md-6.col-12.paddingL` | `p` | `h5` | 38 | 38 | 0.03 of 1956 | subject=1-10 Health and PE c=0.93 n=14 | structure | yes | CANDIDATE |
| 31 | module-menu | MISSING | `div.col-md-8.col-12` | `p` | `—` | 157 | 35 | 0.09 of 1956 | — | 0.97 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 32 | module-menu | MISSING | `div.col-md-6.col-12.paddingR` | `p` | `—` | 46 | 35 | 0.05 of 1956 | subject+ptype=1-10 Blended Literacy/overview c=0.78 n=23 | 0.68 | yes | CANDIDATE |
| 33 | module-menu | MISSING | `div.col-md-8.col-12` | `ul` | `—` | 130 | 32 | 0.29 of 1956 | — | 0.92 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 34 | module-menu | MISSING | `div.col-md-8.col-12` | `h5` | `—` | 120 | 25 | 0.22 of 1956 | — | 0.72 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 35 | module-menu | EXTRA | `div#header` | `—` | `div#module-menu-content.moduleMenu` | 39 | 25 | 0.25 of 1956 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 36 | module-menu | EXTRA | `div.col-md-8.col-12` | `—` | `h5` | 62 | 24 | 0.78 of 1956 | era=Refresh c=0.78 n=24 | structure | — | CANDIDATE |
| 37 | module-menu | EXTRA | `div.col-md-8.col-12` | `—` | `p` | 57 | 24 | 0.87 of 1956 | era=Refresh c=0.87 n=24 | structure | — | CANDIDATE |
| 38 | module-menu | EXTRA | `div.col-md-6.col-12.paddingR` | `—` | `p>b` | 22 | 22 | 1.00 of 1956 | era=Refresh c=1.00 n=22 | structure | yes | CANDIDATE |
| 39 | module-menu | MISSING | `div.col-md-6.col-12.paddingR` | `ul` | `—` | 29 | 21 | 0.05 of 1956 | — | 0.77 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 40 | module-menu | MOVED | `ul` | `li` | `li>i` | 64 | 20 | 0.37 of 1956 | — | structure | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 41 | module-menu | MISSING | `p` | `br` | `—` | 35 | 20 | 0.01 of 1956 | — | structure | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 42 | module-menu | EXTRA | `div#header` | `—` | `div#module-head-buttons` | 30 | 20 | 0.24 of 1956 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 43 | module-menu | SUBSTITUTED | `div.col-md-6.offset-md-0.col-12` | `p` | `h5` | 26 | 20 | 0.04 of 1956 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 44 | module-menu | MISSING | `div.row` | `div.col-md-6.col-12.paddingL` | `—` | 34 | 19 | 0.04 of 1956 | — | 1.00 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 45 | module-menu | MISSING | `div.col-md-6.col-12.paddingR` | `h4>span` | `—` | 19 | 19 | 0.02 of 1956 | — | 1.00 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 46 | module-menu | EXTRA | `div.col-md-6.offset-md-0.col-12` | `—` | `p` | 24 | 18 | 0.99 of 1956 | era=Refresh c=0.99 n=18 | structure | yes | CANDIDATE |
| 47 | module-menu | MISSING | `div.col-md-6.offset-md-0.col-12` | `h3>span` | `—` | 75 | 17 | 0.02 of 1956 | — | 0.95 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 48 | module-menu | MISSING | `div.row` | `div.col-md-6.offset-md-0.col-12` | `—` | 66 | 17 | 0.05 of 1956 | — | 0.86 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 49 | module-menu | SUBSTITUTED | `div.col-md-8.col-12` | `p` | `h5` | 62 | 17 | 0.13 of 1956 | — | structure | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 50 | module-menu | MISSING | `div#header` | `div#module-head-buttons` | `—` | 49 | 17 | 0.76 of 1956 | template=Standard c=0.77 n=11 | structure | yes | CANDIDATE |
| 51 | module-menu | EXTRA | `div.col-md-6.col-12.paddingR` | `—` | `p` | 17 | 17 | 0.94 of 1956 | template=Standard c=0.95 n=14 | structure | yes | CANDIDATE |
| 52 | module-menu | SUBSTITUTED | `ul` | `li` | `li` | 63 | 16 | 0.59 of 1956 | template+ptype=Standard/lesson c=0.63 n=12 | structure | — | CANDIDATE |
| 53 | module-menu | EXTRA | `div.row` | `—` | `div.col-md-12.col-12.paddingR` | 18 | 16 | 0.95 of 1956 | template=Standard c=0.96 n=16 | structure | yes | CANDIDATE |
| 54 | module-menu | EXTRA | `div.row` | `—` | `div.col-md-8.col-12` | 97 | 15 | 0.68 of 1956 | subject=1-10 Mathematics c=0.77 n=12 | structure | — | CANDIDATE |
| 55 | module-menu | EXTRA | `div.col-md-8.col-12` | `—` | `ul` | 37 | 15 | 0.71 of 1956 | era=Refresh c=0.71 n=15 | structure | — | CANDIDATE |
| 56 | module-menu | SUBSTITUTED | `div.col-md-6.col-12.paddingR` | `h4>span` | `h5>span` | 15 | 15 | 0.03 of 1956 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 57 | module-menu | EXTRA | `div.row` | `—` | `div.col-md-6.offset-md-0.col-12` | 30 | 14 | 0.95 of 1956 | era=Refresh c=0.95 n=14 | structure | yes | CANDIDATE |
| 58 | module-menu | SUBSTITUTED | `div.col-md-6.col-12.paddingR` | `ul` | `p>b` | 14 | 14 | 0.07 of 1956 | subject+ptype=1-10 Blended Literacy/overview c=0.85 n=14 | structure | yes | CANDIDATE |
| 59 | module-menu | MISSING | `div#module-menu-content.moduleMenu` | `ul` | `—` | 88 | 13 | 0.04 of 1956 | — | 0.91 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 60 | module-menu | SUBSTITUTED | `div#module-menu-content.moduleMenu` | `h5` | `div.row` | 82 | 13 | 0.04 of 1956 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 61 | module-menu | MISSING | `div.col-md-6.offset-md-0.col-12` | `ul` | `—` | 59 | 12 | 0.02 of 1956 | — | 0.98 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 62 | module-menu | EXTRA | `div.col-md-6.col-12.paddingR` | `—` | `h5` | 14 | 12 | 0.99 of 1956 | ptype=overview c=1.00 n=10 | structure | yes | CANDIDATE |
| 63 | module-menu | MISSING | `div.row` | `div.col-md-6.offset-md-0.col-12.paddingL` | `—` | 12 | 12 | 0.01 of 1956 | — | 0.42 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 64 | module-menu | SUBSTITUTED | `div.row` | `div.col-md-6.col-12.paddingR` | `div.col-md-12.col-12.paddingR` | 12 | 12 | 0.08 of 1956 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 65 | module-menu | SUBSTITUTED | `div.row` | `WIDGET` | `div.col-md-8.col-12` | 24 | 11 | 0.11 of 1956 | — | structure | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 66 | module-menu | SUBSTITUTED | `div.row` | `div.col-md-6.col-12.paddingL` | `div.col-md-6.col-12.paddingR` | 11 | 11 | 0.04 of 1956 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 67 | module-menu | SUBSTITUTED | `div#module-menu-content.moduleMenu` | `div.item` | `div.row` | 68 | 10 | 0.04 of 1956 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 68 | module-menu | EXTRA | `li>b` | `—` | `b` | 23 | 10 | 0.99 of 1956 | era=Refresh c=0.99 n=10 | structure | — | CANDIDATE |
| 69 | module-menu | SUBSTITUTED | `div.col-md-6.offset-md-0.col-12` | `h3>span` | `h5` | 17 | 10 | 0.05 of 1956 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 70 | module-menu | SUBSTITUTED | `div.row` | `div.col-md-6.offset-md-0.col-12` | `div.col-md-8.col-12` | 56 | 9 | 0.05 of 1956 | — | structure | yes | BELOW FLOOR |
| 71 | module-menu | MISSING | `div#module-menu-content.moduleMenu` | `h5` | `—` | 45 | 9 | 0.04 of 1956 | — | 0.71 | yes | BELOW FLOOR |
| 72 | module-menu | EXTRA | `div.col-md-12.col-12.paddingR` | `—` | `h4>span` | 9 | 9 | 0.97 of 1956 | — | structure | yes | BELOW FLOOR |
| 73 | module-menu | EXTRA | `div.col-md-6.col-12.paddingR` | `—` | `h5>span` | 9 | 9 | 0.97 of 1956 | — | structure | yes | BELOW FLOOR |
| 74 | module-menu | MISSING | `div.col-md-6.col-12.paddingR` | `h5>span` | `—` | 9 | 9 | 0.03 of 1956 | — | 1.00 | yes | BELOW FLOOR |
| 75 | module-menu | SUBSTITUTED | `div.col-md-6.col-12` | `h4>span` | `h5>span` | 9 | 9 | 0.01 of 1956 | — | structure | yes | BELOW FLOOR |
| 76 | module-menu | MISSING | `div.col-md-6.offset-md-0.col-12` | `p` | `—` | 36 | 8 | 0.02 of 1956 | — | 0.91 | yes | BELOW FLOOR |
| 77 | module-menu | MOVED | `ul` | `li` | `li` | 36 | 8 | 0.37 of 1956 | — | structure | — | BELOW FLOOR |
| 78 | module-menu | MISSING | `div#header` | `div#module-menu-content.moduleMenu` | `—` | 28 | 8 | 0.75 of 1956 | — | 1.00 | yes | BELOW FLOOR |
| 79 | module-menu | EXTRA | `p>b` | `—` | `b` | 8 | 8 | 0.99 of 1956 | — | structure | — | BELOW FLOOR |
| 80 | module-menu | EXTRA | `div.col-md-6.col-12.paddingL` | `—` | `h5` | 8 | 8 | 1.00 of 1956 | — | structure | yes | BELOW FLOOR |
| 81 | module-menu | MISSING | `h5>span` | `span` | `—` | 8 | 8 | 0.04 of 1956 | — | 1.00 | — | BELOW FLOOR |
| 82 | module-menu | SUBSTITUTED | `div.col-md-6.offset-md-0.col-12.paddingR` | `p` | `h5` | 8 | 8 | 0.01 of 1956 | — | structure | yes | BELOW FLOOR |
| 83 | module-menu | MOVED | `div#module-menu-content.moduleMenu` | `h5` | `h5` | 35 | 7 | 0.04 of 1956 | — | structure | yes | BELOW FLOOR |
| 84 | module-menu | SUBSTITUTED | `div.col-md-6.offset-md-0.col-12` | `h3>span` | `h4>span` | 10 | 7 | 0.05 of 1956 | — | structure | yes | BELOW FLOOR |
| 85 | module-menu | EXTRA | `div.col-md-6.offset-md-0.col-12` | `—` | `ul` | 7 | 7 | 0.98 of 1956 | — | structure | yes | BELOW FLOOR |
| 86 | module-menu | SUBSTITUTED | `div.row` | `div.col-md-12.col-12` | `div.col-md-12.col-12.paddingR` | 7 | 7 | 0.01 of 1956 | — | structure | yes | BELOW FLOOR |
| 87 | module-menu | SUBSTITUTED | `div.row` | `div.col-12` | `div.col-md-8.col-12` | 50 | 6 | 0.03 of 1956 | — | structure | — | BELOW FLOOR |
| 88 | module-menu | SUBSTITUTED | `div.row` | `div.col-md-8.col-12.paddingR` | `div.col-md-8.col-12` | 50 | 6 | 0.03 of 1956 | — | structure | yes | BELOW FLOOR |
| 89 | module-menu | SUBSTITUTED | `div.item` | `div.row` | `div.col-md-8.col-12` | 36 | 6 | 0.03 of 1956 | — | structure | yes | BELOW FLOOR |
| 90 | module-menu | MISSING | `div.col-md-8.col-12.paddingR` | `h5` | `—` | 30 | 6 | 0.02 of 1956 | — | 1.00 | yes | BELOW FLOOR |
| 91 | module-menu | SUBSTITUTED | `div.row` | `div.col-md-12.col-12.paddingR` | `div.col-md-8.col-12` | 30 | 6 | 0.05 of 1956 | — | structure | yes | BELOW FLOOR |
| 92 | module-menu | MISSING | `div.col-md-8.col-12.paddingR` | `ul` | `—` | 28 | 6 | 0.02 of 1956 | — | 0.98 | yes | BELOW FLOOR |
| 93 | module-menu | MISSING | `div.row` | `div.col-md-6.col-12` | `—` | 21 | 6 | 0.01 of 1956 | — | 1.00 | yes | BELOW FLOOR |
| 94 | module-menu | SUBSTITUTED | `div.col-md-8.col-12` | `p>b` | `h5` | 17 | 6 | 0.02 of 1956 | — | structure | — | BELOW FLOOR |
| 95 | module-menu | SUBSTITUTED | `div.col-md-6.offset-md-0.col-12` | `ul` | `p` | 14 | 6 | 0.05 of 1956 | — | structure | yes | BELOW FLOOR |
| 96 | module-menu | SUBSTITUTED | `div.col-md-8.col-12` | `p` | `ul` | 13 | 6 | 0.13 of 1956 | — | structure | — | BELOW FLOOR |
| 97 | module-menu | SUBSTITUTED | `div.row` | `div.col-md-6.offset-md-0.col-12` | `div.col-md-12.col-12.paddingR` | 9 | 6 | 0.05 of 1956 | — | structure | yes | BELOW FLOOR |
| 98 | module-menu | EXTRA | `div.col-md-6.col-12.paddingR` | `—` | `ul` | 6 | 6 | 1.00 of 1956 | — | structure | yes | BELOW FLOOR |
| 99 | module-menu | EXTRA | `div.row` | `—` | `div.col-md-6.col-12.paddingL` | 6 | 6 | 0.96 of 1956 | — | structure | yes | BELOW FLOOR |
| 100 | module-menu | MISSING | `div.col-md-6.col-12` | `h4>span` | `—` | 6 | 6 | 0.01 of 1956 | — | 1.00 | yes | BELOW FLOOR |
| 101 | module-menu | SUBSTITUTED | `div.row` | `div.col-md-6.offset-md-0.col-12.paddingR` | `div.col-md-8.col-12` | 6 | 6 | 0.01 of 1956 | — | structure | yes | BELOW FLOOR |
| 102 | module-menu | SUBSTITUTED | `div.col-md-6.col-12.paddingR` | `ul` | `p` | 6 | 6 | 0.07 of 1956 | — | structure | yes | BELOW FLOOR |
| 103 | module-menu | SUBSTITUTED | `div.row` | `div.col-md-6.col-12.paddingR` | `div.col-md-8.col-12` | 6 | 6 | 0.08 of 1956 | — | structure | yes | BELOW FLOOR |
| 104 | module-menu | SUBSTITUTED | `div.col-md-8.col-12` | `h3>span` | `h5` | 21 | 5 | 0.01 of 1956 | — | structure | — | BELOW FLOOR |
| 105 | module-menu | SUBSTITUTED | `div.col-md-8.col-12` | `h4` | `h5` | 19 | 5 | 0.01 of 1956 | — | structure | — | BELOW FLOOR |
| 106 | module-menu | SUBSTITUTED | `div.item` | `div.row` | `div.col-md-12.col-12.paddingR` | 16 | 5 | 0.03 of 1956 | — | structure | yes | BELOW FLOOR |
| 107 | module-menu | MISSING | `div.col-md-8.col-12` | `p>b` | `—` | 14 | 5 | 0.01 of 1956 | — | 0.67 | — | BELOW FLOOR |
| 108 | module-menu | MOVED | `div.col-md-8.col-12` | `p` | `p` | 10 | 5 | 0.09 of 1956 | — | structure | — | BELOW FLOOR |
| 109 | module-menu | SUBSTITUTED | `div.row` | `div.col-md-6.offset-md-0.col-12` | `div.col-md-6.col-12.paddingR` | 8 | 5 | 0.05 of 1956 | — | structure | yes | BELOW FLOOR |
| 110 | module-menu | MISSING | `li>i` | `i` | `—` | 6 | 5 | 0.00 of 1956 | — | 0.96 | — | BELOW FLOOR |
| 111 | module-menu | EXTRA | `div.col-md-6.offset-md-0.col-12` | `—` | `h5` | 5 | 5 | 1.00 of 1956 | — | structure | yes | BELOW FLOOR |
| 112 | module-menu | MISSING | `div.col-md-6.offset-md-0.col-12.paddingR` | `h5` | `—` | 5 | 5 | 0.01 of 1956 | — | 0.00 | yes | BELOW FLOOR |
| 113 | module-menu | MISSING | `div.col-md-6.col-12` | `p` | `—` | 5 | 5 | 0.01 of 1956 | — | 0.71 | yes | BELOW FLOOR |
| 114 | module-menu | SUBSTITUTED | `div.col-md-6.offset-md-0.col-12` | `h3>span` | `h5>span` | 5 | 5 | 0.05 of 1956 | — | structure | yes | BELOW FLOOR |
| 115 | module-menu | SUBSTITUTED | `div.row` | `div.col-md-6.col-12` | `div.col-md-12.col-12.paddingR` | 5 | 5 | 0.02 of 1956 | — | structure | yes | BELOW FLOOR |
| 116 | module-menu | SUBSTITUTED | `div#module-menu-content.moduleMenu` | `WIDGET` | `div.row` | 5 | 5 | 0.01 of 1956 | — | structure | yes | BELOW FLOOR |
| 117 | module-menu | SUBSTITUTED | `div.row` | `div.col-md-8` | `div.col-md-8.col-12` | 25 | 4 | 0.01 of 1956 | — | structure | — | BELOW FLOOR |
| 118 | module-menu | MISSING | `div.col-12` | `ul` | `—` | 15 | 4 | 0.03 of 1956 | — | 0.77 | — | BELOW FLOOR |
| 119 | module-menu | MISSING | `div.row` | `div.col-md-6.col-12.paddingR` | `—` | 8 | 4 | 0.08 of 1956 | — | 1.00 | yes | BELOW FLOOR |
| 120 | module-menu | SUBSTITUTED | `div.col-md-6.offset-md-0.col-12` | `p` | `ul` | 7 | 4 | 0.04 of 1956 | — | structure | yes | BELOW FLOOR |
| 121 | module-menu | SUBSTITUTED | `p` | `br` | `li` | 7 | 4 | 0.03 of 1956 | — | structure | — | BELOW FLOOR |
| 122 | module-menu | EXTRA | `li` | `—` | `b` | 6 | 4 | 1.00 of 1956 | — | structure | — | BELOW FLOOR |
| 123 | module-menu | EXTRA | `div#module-head-buttons` | `—` | `div#module-menu-button.circle-button.btn1` | 4 | 4 | 0.24 of 1956 | — | structure | — | BELOW FLOOR |
| 124 | module-menu | EXTRA | `div.col-md-6.col-12.paddingL` | `—` | `p` | 4 | 4 | 1.00 of 1956 | — | structure | — | BELOW FLOOR |
| 125 | module-menu | EXTRA | `div.col-md-6.col-12.paddingL` | `—` | `ul` | 4 | 4 | 0.99 of 1956 | — | structure | — | BELOW FLOOR |
| 126 | module-menu | EXTRA | `div.col-md-6.offset-md-0.col-12` | `—` | `p>b` | 4 | 4 | 0.99 of 1956 | — | structure | — | BELOW FLOOR |
| 127 | module-menu | EXTRA | `div.col-md-8.col-12` | `—` | `p>b` | 4 | 4 | 1.00 of 1956 | — | structure | — | BELOW FLOOR |
| 128 | module-menu | MISSING | `div.row` | `div.col-md-12.col-12.paddingR` | `—` | 4 | 4 | 0.00 of 1956 | — | 1.00 | — | BELOW FLOOR |
| 129 | module-menu | MISSING | `div#module-menu-content.moduleMenu` | `div.row` | `—` | 4 | 4 | 0.00 of 1956 | — | 0.75 | — | BELOW FLOOR |
| 130 | module-menu | MISSING | `div.col-md-6.offset-md-0.col-12.paddingR` | `ul` | `—` | 4 | 4 | 0.01 of 1956 | — | 0.75 | — | BELOW FLOOR |
| 131 | module-menu | SUBSTITUTED | `div.row` | `div.col-md-6.offset-md-0.col-12.paddingR` | `div.col-md-12.col-12.paddingR` | 4 | 4 | 0.01 of 1956 | — | structure | — | BELOW FLOOR |
| 132 | module-menu | SUBSTITUTED | `div.col-md-6.col-12.paddingR` | `p` | `ul` | 4 | 4 | 0.07 of 1956 | — | structure | — | BELOW FLOOR |
| 133 | module-menu | SUBSTITUTED | `div.row` | `div.col-md-6.col-12` | `div.col-md-6.col-12.paddingR` | 4 | 4 | 0.02 of 1956 | — | structure | — | BELOW FLOOR |
| 134 | module-menu | SUBSTITUTED | `div.col-md-6.col-12` | `p` | `h5>span` | 4 | 4 | 0.02 of 1956 | — | structure | — | BELOW FLOOR |
| 135 | module-menu | SUBSTITUTED | `div.col-md-6.col-12.paddingL` | `h4>span` | `h5` | 4 | 4 | 0.01 of 1956 | — | structure | — | BELOW FLOOR |
| 136 | module-menu | SUBSTITUTED | `div.col-md-6.offset-md-0.col-12.paddingL` | `p` | `h5` | 4 | 4 | 0.00 of 1956 | — | structure | — | BELOW FLOOR |
| 137 | module-menu | MISSING | `div.item` | `ul` | `—` | 21 | 3 | 0.01 of 1956 | — | 1.00 | — | BELOW FLOOR |
| 138 | module-menu | MOVED | `div.item` | `h5` | `h5` | 17 | 3 | 0.01 of 1956 | — | structure | — | BELOW FLOOR |
| 139 | module-menu | SUBSTITUTED | `div.col-md-8.col-12` | `ul` | `li` | 17 | 3 | 0.29 of 1956 | — | structure | — | BELOW FLOOR |
| 140 | module-menu | MISSING | `div#module-menu-content.moduleMenu` | `p` | `—` | 14 | 3 | 0.01 of 1956 | — | 1.00 | — | BELOW FLOOR |
| 141 | module-menu | MOVED | `div.col-md-8.col-12.paddingR` | `h5` | `h5` | 12 | 3 | 0.02 of 1956 | — | structure | — | BELOW FLOOR |
| 142 | module-menu | SUBSTITUTED | `div.col-md-8.col-12` | `ul` | `ol` | 12 | 3 | 0.29 of 1956 | — | structure | — | BELOW FLOOR |
| 143 | module-menu | MISSING | `div.col-md-6.col-12.paddingR` | `h5` | `—` | 11 | 3 | 0.01 of 1956 | — | 1.00 | — | BELOW FLOOR |
| 144 | module-menu | SUBSTITUTED | `div.row` | `div.col-md-6.col-12.paddingR` | `h4>span` | 11 | 3 | 0.08 of 1956 | — | structure | — | BELOW FLOOR |
| 145 | module-menu | SUBSTITUTED | `div.col-md-6.col-12.paddingL` | `ul` | `li` | 11 | 3 | 0.04 of 1956 | — | structure | — | BELOW FLOOR |
| 146 | module-menu | MISSING | `p>b` | `b` | `—` | 10 | 3 | 0.03 of 1956 | — | 1.00 | — | BELOW FLOOR |
| 147 | module-menu | MISSING | `div.col-md-12.col-12.paddingR` | `h5` | `—` | 10 | 3 | 0.02 of 1956 | — | 1.00 | — | BELOW FLOOR |
| 148 | module-menu | MISSING | `div.col-md-12.col-12.paddingR` | `ul` | `—` | 10 | 3 | 0.02 of 1956 | — | 1.00 | — | BELOW FLOOR |
| 149 | module-menu | MISSING | `div.col-12` | `h5` | `—` | 9 | 3 | 0.02 of 1956 | — | 1.00 | — | BELOW FLOOR |
| 150 | module-menu | MOVED | `div.col-md-12.col-12.paddingR` | `p` | `p` | 9 | 3 | 0.02 of 1956 | — | structure | — | BELOW FLOOR |
| 396 | footer | MISSING | `ul.footer-nav` | `li>a#next-lesson` | `—` | 94 | 57 | 0.72 of 1956 | subject+ptype=1-10 Mathematics/overview c=0.93 n=11 | structure | yes | CANDIDATE |
| 397 | footer | MISSING | `ul.footer-nav` | `li>a.home-nav` | `—` | 87 | 49 | 0.85 of 1956 | subject=1-10 English c=1.00 n=12 | structure | yes | CANDIDATE |
| 398 | footer | MISSING | `li>a#next-lesson` | `a#next-lesson` | `—` | 45 | 45 | 0.82 of 1956 | template=Standard c=0.84 n=35 | structure | yes | CANDIDATE |
| 399 | footer | MISSING | `ul.footer-nav.inquiry-nav` | `li>a.home-nav` | `—` | 44 | 38 | 0.14 of 1956 | subject+ptype=1-10 Blended Literacy/overview c=0.87 n=20 | structure | yes | CANDIDATE |
| 402 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav` | `ul.footer-nav.inquiry-nav` | 64 | 18 | 0.84 of 1956 | ptype=lesson c=0.89 n=15 | structure | yes | CANDIDATE |
| 403 | footer | MISSING | `ul.footer-nav` | `li>a#prev-lesson` | `—` | 38 | 18 | 0.71 of 1956 | ptype=lesson c=0.88 n=11 | structure | yes | CANDIDATE |
| 404 | footer | EXTRA | `ul.footer-nav.inquiry-nav` | `—` | `li>a.home-nav` | 17 | 17 | 0.86 of 1956 | era=Refresh c=0.86 n=17 | structure | yes | CANDIDATE |
| 406 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` | `li>a#next-lesson` | `li>a.home-nav` | 16 | 16 | 0.10 of 1956 | subject+ptype=1-10 Blended Literacy/overview c=0.83 n=15 | structure | yes | CANDIDATE |
| 407 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav.inquiry-nav` | `li>a#next-lesson` | 15 | 15 | 0.14 of 1956 | subject+ptype=1-10 Blended Literacy/overview c=0.87 n=15 | structure | yes | CANDIDATE |
| 408 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav` | `ul.footer-nav` | 13 | 13 | 0.84 of 1956 | ptype=lesson c=0.89 n=10 | structure | yes | CANDIDATE |
| 409 | footer | MISSING | `div#footer` | `ul.footer-nav` | `—` | 12 | 12 | 0.84 of 1956 | ptype=lesson c=0.89 n=11 | structure | yes | CANDIDATE |
| 410 | footer | EXTRA | `div#footer` | `—` | `ul.footer-nav.inquiry-nav` | 12 | 11 | 0.86 of 1956 | template=Standard c=0.87 n=10 | structure | yes | CANDIDATE |
| 411 | footer | EXTRA | `ul.footer-nav.fundamentals-nav` | `—` | `li>a.home-nav` | 10 | 10 | 0.99 of 1956 | era=Refresh c=0.99 n=10 | structure | yes | CANDIDATE |
| 412 | footer | SUBSTITUTED | `ul.footer-nav` | `li>a#next-lesson` | `li>a#next-lesson` | 10 | 10 | 0.72 of 1956 | template=Standard c=0.75 n=10 | structure | yes | CANDIDATE |
| 506 | acks | SUBSTITUTED | `div.col-md-8.col-12` | `div.acks` | `div.acks.acksTemplate` | 84 | 84 | 0.17 of 1956 | template+ptype=Inquiry/overview c=0.83 n=27 | structure | yes | CANDIDATE |
| 534 | activity | MISSING | `div.col-12` | `p` | `—` | 705 | 299 | 0.31 of 1950 | subject+ptype=1-10 Blended Literacy/lesson c=0.78 n=106 | 0.83 | — | CANDIDATE |
| 535 | activity | EXTRA | `div.col-12` | `—` | `p` | 463 | 236 | 0.88 of 1950 | series=XDLS90 c=1.00 n=21 | structure | — | CANDIDATE |
| 537 | activity | MISSING | `div.col-12` | `a` | `—` | 423 | 208 | 0.29 of 1950 | series=HIS10 c=0.71 n=41 | 0.65 | — | CANDIDATE |
| 538 | activity | MISSING | `a` | `div.button` | `—` | 529 | 194 | 0.23 of 1950 | series=HIS10 c=0.71 n=36 | 0.63 | yes | CANDIDATE |
| 539 | activity | MISSING | `div.col-12` | `h3` | `—` | 394 | 183 | 0.32 of 1950 | template+ptype=Fundamentals/overview c=0.87 n=26 | 0.75 | — | CANDIDATE |
| 540 | activity | MOVED | `div.col-12` | `p` | `p` | 280 | 152 | 0.19 of 1950 | template+ptype=Fundamentals/overview c=0.62 n=20 | structure | — | CANDIDATE |
| 541 | activity | EXTRA | `div.col-12` | `—` | `WIDGET` | 225 | 146 | 0.82 of 1950 | subject=1-10 English c=0.92 n=29 | structure | — | CANDIDATE |
| 543 | activity | EXTRA | `div.row` | `—` | `div.col-12` | 155 | 110 | 0.89 of 1950 | template=Standard c=0.92 n=129 | structure | — | CANDIDATE |
| 544 | activity | EXTRA | `div.col-12` | `—` | `p>a` | 119 | 100 | 0.99 of 1950 | subject+ptype=1-10 Blended Literacy/lesson c=1.00 n=33 | structure | — | CANDIDATE |
| 546 | activity | EXTRA | `div.col-12` | `—` | `img.img-fluid` | 138 | 92 | 0.97 of 1950 | template=Standard c=0.98 n=92 | structure | — | CANDIDATE |
| 550 | activity | MOVED | `div.col-12` | `h3` | `h3` | 98 | 80 | 0.23 of 1950 | subject+ptype=1-10 Blended Literacy/lesson c=0.77 n=24 | structure | — | CANDIDATE |
| 551 | activity | EXTRA | `div.col-12` | `—` | `ul` | 92 | 76 | 0.94 of 1950 | subject=1-10 Blended Literacy c=0.96 n=22 | structure | — | CANDIDATE |
| 552 | activity | EXTRA | `div.col-12` | `—` | `p>b` | 108 | 75 | 0.97 of 1950 | template=Standard c=0.98 n=75 | structure | — | CANDIDATE |
| 553 | activity | EXTRA | `div.col-12` | `—` | `ol` | 104 | 74 | 0.96 of 1950 | template=Standard c=0.97 n=86 | structure | — | CANDIDATE |
| 557 | activity | SUBSTITUTED | `div.col-12` | `p` | `p` | 92 | 70 | 0.76 of 1950 | template+ptype=Standard/lesson c=0.89 n=64 | structure | — | CANDIDATE |
| 558 | activity | EXTRA | `div.col-12` | `—` | `h3` | 89 | 65 | 0.86 of 1950 | template=Standard c=0.91 n=53 | structure | — | CANDIDATE |
| 560 | activity | EXTRA | `p>a` | `—` | `a` | 71 | 64 | 0.98 of 1950 | subject+ptype=1-10 Blended Literacy/lesson c=1.00 n=27 | structure | — | CANDIDATE |
| 562 | activity | EXTRA | `p>b` | `—` | `b` | 80 | 58 | 0.93 of 1950 | template=Standard c=0.94 n=52 | structure | — | CANDIDATE |
| 566 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `div.row` | 62 | 52 | 0.60 of 1950 | ptype=lesson c=0.70 n=55 | structure | — | CANDIDATE |
| 569 | activity | EXTRA | `div.col-12` | `—` | `h4.goJournal` | 120 | 50 | 0.95 of 1950 | series=HIS10 c=1.00 n=33 | structure | — | CANDIDATE |
| 570 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `p` | 56 | 50 | 0.60 of 1950 | subject+ptype=1-10 Mathematics/lesson c=0.78 n=22 | structure | — | CANDIDATE |
| 571 | activity | SUBSTITUTED | `div.col-12` | `a` | `h4.goJournal` | 108 | 48 | 0.57 of 1950 | series=HIS10 c=0.83 n=20 | structure | — | CANDIDATE |
| 572 | activity | EXTRA | `div.col-12` | `—` | `a` | 80 | 48 | 0.86 of 1950 | template=Standard c=0.87 n=72 | structure | — | CANDIDATE |
| 574 | activity | EXTRA | `ol` | `—` | `li` | 66 | 48 | 0.96 of 1950 | template=Standard c=0.97 n=52 | structure | — | CANDIDATE |
| 575 | activity | SUBSTITUTED | `div.col-12` | `h3` | `WIDGET` | 83 | 47 | 0.76 of 1950 | subject+ptype=1-10 Mathematics/lesson c=0.95 n=21 | structure | — | CANDIDATE |
| 576 | activity | EXTRA | `a` | `—` | `div.button` | 82 | 47 | 0.77 of 1950 | series=XDLS90 c=0.92 n=31 | structure | yes | CANDIDATE |
| 579 | activity | EXTRA | `div.col-12` | `—` | `p>i` | 48 | 42 | 0.97 of 1950 | template=Standard c=0.98 n=40 | structure | — | CANDIDATE |
| 582 | activity | SUBSTITUTED | `div.col-12` | `p` | `WIDGET` | 51 | 40 | 0.76 of 1950 | template+ptype=Standard/lesson c=0.89 n=36 | structure | — | CANDIDATE |
| 585 | activity | EXTRA | `p>i` | `—` | `i` | 44 | 38 | 0.96 of 1950 | template=Standard c=0.97 n=43 | structure | — | CANDIDATE |
| 586 | activity | SUBSTITUTED | `div.col-12` | `a` | `p` | 50 | 37 | 0.57 of 1950 | template+ptype=Standard/lesson c=0.68 n=49 | structure | — | CANDIDATE |
| 594 | activity | EXTRA | `div.col-12` | `—` | `div.videoSection.ratio.ratio-16x9` | 43 | 31 | 0.99 of 1950 | template=Standard c=0.99 n=33 | structure | yes | CANDIDATE |
| 598 | activity | EXTRA | `ul` | `—` | `li` | 31 | 30 | 0.93 of 1950 | template=Standard c=0.95 n=26 | structure | — | CANDIDATE |
| 600 | activity | SUBSTITUTED | `div.col-12` | `a` | `WIDGET` | 33 | 29 | 0.57 of 1950 | template+ptype=Standard/lesson c=0.68 n=28 | structure | — | CANDIDATE |
| 603 | activity | EXTRA | `div.activity` | `—` | `div.row` | 40 | 27 | 1.00 of 1950 | era=Refresh c=1.00 n=40 | structure | yes | CANDIDATE |
| 608 | activity | EXTRA | `div.videoSection.ratio.ratio-16x9` | `—` | `iframe` | 35 | 26 | 0.97 of 1950 | template=Standard c=0.98 n=22 | structure | yes | CANDIDATE |
| 610 | activity | EXTRA | `div.col-12` | `—` | `audio.audioPlayer.icon` | 41 | 25 | 1.00 of 1950 | era=Refresh c=1.00 n=41 | structure | yes | CANDIDATE |
| 612 | activity | EXTRA | `div.col-12` | `—` | `h5` | 31 | 25 | 0.98 of 1950 | template=Standard c=0.99 n=26 | structure | — | CANDIDATE |
| 614 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `div.col-md-8.col-12` | 25 | 24 | 0.60 of 1950 | era=Refresh c=0.60 n=25 | structure | — | CANDIDATE |
| 616 | activity | EXTRA | `p` | `—` | `b` | 31 | 23 | 0.96 of 1950 | template=Standard c=0.96 n=28 | structure | — | CANDIDATE |
| 621 | activity | EXTRA | `div.col-12` | `—` | `div.videoSection.icon.ratio.ratio-16x9` | 38 | 22 | 0.97 of 1950 | template=Standard c=0.98 n=32 | structure | yes | CANDIDATE |
| 624 | activity | SUBSTITUTED | `div.row` | `div.col-12` | `div.col-md-8.col-12` | 25 | 22 | 0.79 of 1950 | era=Refresh c=0.79 n=25 | structure | — | CANDIDATE |
| 629 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `ol` | 22 | 21 | 0.60 of 1950 | era=Refresh c=0.60 n=22 | structure | — | CANDIDATE |
| 631 | activity | SUBSTITUTED | `div.row` | `div.col-12` | `div.row` | 21 | 21 | 0.79 of 1950 | era=Refresh c=0.79 n=21 | structure | — | CANDIDATE |
| 636 | activity | EXTRA | `a` | `—` | `div.externalButton` | 26 | 19 | 0.91 of 1950 | era=Refresh c=0.91 n=26 | structure | — | CANDIDATE |
| 638 | activity | EXTRA | `div.col-12` | `—` | `div.button` | 30 | 18 | 1.00 of 1950 | template=Standard c=1.00 n=26 | structure | yes | CANDIDATE |
| 639 | activity | SUBSTITUTED | `div.row` | `div.col-12` | `WIDGET` | 20 | 18 | 0.79 of 1950 | era=Refresh c=0.79 n=20 | structure | — | CANDIDATE |
| 642 | activity | SUBSTITUTED | `div.col-12` | `p` | `h4.goJournal` | 30 | 17 | 0.76 of 1950 | template+ptype=Standard/lesson c=0.89 n=29 | structure | — | CANDIDATE |
| 644 | activity | EXTRA | `div.col-12` | `—` | `div.TKmodal` | 20 | 17 | 0.99 of 1950 | era=Refresh c=0.99 n=20 | structure | — | CANDIDATE |
| 650 | activity | EXTRA | `div.row` | `—` | `div.clickDropContent` | 23 | 15 | 0.99 of 1950 | template=Standard c=1.00 n=23 | structure | — | CANDIDATE |
| 651 | activity | EXTRA | `div.row` | `—` | `WIDGET` | 22 | 15 | 1.00 of 1950 | era=Refresh c=1.00 n=22 | structure | — | CANDIDATE |
| 660 | activity | EXTRA | `div.col-md-8.col-12` | `—` | `div.activity` | 20 | 14 | 1.00 of 1950 | era=Refresh c=1.00 n=20 | structure | yes | CANDIDATE |
| 6047 | body | EXTRA | `div#body` | `—` | `div.row` | 1262 | 324 | 0.73 of 1950 | subject+ptype=1-10 Blended Literacy/overview c=1.00 n=29 | structure | — | CANDIDATE |
| 6048 | body | EXTRA | `div.col-md-8.col-12` | `—` | `p` | 868 | 321 | 0.82 of 1950 | subject=1-10 Blended Literacy c=1.00 n=35 | structure | — | CANDIDATE |
| 6049 | body | MISSING | `div#body` | `div.row` | `—` | 1074 | 279 | 0.34 of 1950 | series=MXDI20 c=0.83 n=21 | 0.87 | — | CANDIDATE |
| 6050 | body | MISSING | `div.col-md-8.col-12` | `p` | `—` | 503 | 240 | 0.29 of 1950 | template+ptype=Fundamentals/overview c=0.93 n=32 | 0.83 | — | CANDIDATE |
| 6051 | body | EXTRA | `div.col-md-8.col-12` | `—` | `img.img-fluid` | 459 | 195 | 0.97 of 1950 | template+ptype=Standard/overview c=1.00 n=25 | structure | — | CANDIDATE |
| 6052 | body | MOVED | `div.col-md-8.col-12` | `p` | `p` | 303 | 190 | 0.18 of 1950 | template+ptype=Fundamentals/overview c=0.87 n=37 | structure | — | CANDIDATE |
| 6053 | body | EXTRA | `div.col-md-8.col-12` | `—` | `WIDGET` | 269 | 171 | 0.89 of 1950 | subject=NCEA1 c=0.96 n=23 | structure | — | CANDIDATE |
| 6054 | body | SUBSTITUTED | `div.row` | `div.col-12` | `div.col-md-8.col-12` | 285 | 160 | 0.55 of 1950 | subject+ptype=1-10 Blended Literacy/overview c=0.99 n=64 | structure | — | CANDIDATE |
| 6055 | body | EXTRA | `div.col-md-8.col-12` | `—` | `ul` | 281 | 158 | 0.96 of 1950 | subject=1-10 English c=0.99 n=24 | structure | — | CANDIDATE |
| 6056 | body | EXTRA | `div.row` | `—` | `div.col-md-8.col-12` | 240 | 157 | 0.89 of 1950 | subject+ptype=1-10 Blended Literacy/lesson c=0.99 n=20 | structure | — | CANDIDATE |
| 6057 | body | EXTRA | `div.col-md-8.col-12` | `—` | `p>b` | 263 | 156 | 0.95 of 1950 | subject=1-10 Blended Literacy c=1.00 n=37 | structure | — | CANDIDATE |
| 6058 | body | MISSING | `div.col-md-8.col-12` | `WIDGET` | `—` | 229 | 140 | 0.19 of 1950 | subject+ptype=Online Safety (OS9000)/lesson c=0.65 n=22 | structure | — | CANDIDATE |
| 6059 | body | EXTRA | `div.col-md-8.col-12` | `—` | `h3` | 211 | 140 | 0.72 of 1950 | subject=1-10 Blended Literacy c=1.00 n=20 | structure | — | CANDIDATE |
| 6062 | body | MISSING | `div.col-md-8.col-12` | `h3` | `—` | 218 | 129 | 0.17 of 1950 | template+ptype=Fundamentals/overview c=0.81 n=20 | 0.92 | — | CANDIDATE |
| 6065 | body | EXTRA | `div.col-md-8.col-12` | `—` | `a` | 190 | 107 | 0.98 of 1950 | subject=ConnectED c=1.00 n=28 | structure | — | CANDIDATE |
| 6067 | body | EXTRA | `div.col-md-8.col-12` | `—` | `div.videoSection.ratio.ratio-16x9` | 176 | 103 | 0.94 of 1950 | subject=1-10 English c=0.97 n=32 | structure | yes | CANDIDATE |
| 6068 | body | EXTRA | `div.col-md-8.col-12` | `—` | `div.table-responsive` | 174 | 103 | 0.98 of 1950 | subject+ptype=1-10 English/lesson c=0.99 n=22 | structure | — | CANDIDATE |
| 6070 | body | EXTRA | `p>b` | `—` | `b` | 152 | 96 | 0.91 of 1950 | subject=1-10 Mathematics c=0.94 n=30 | structure | — | CANDIDATE |
| 6072 | body | EXTRA | `a` | `—` | `div.button` | 170 | 88 | 0.97 of 1950 | subject=NCEA1 c=0.98 n=20 | structure | — | CANDIDATE |
| 6073 | body | EXTRA | `div.col-md-8.col-12` | `—` | `h4` | 117 | 87 | 0.98 of 1950 | template=Standard c=0.99 n=77 | structure | — | CANDIDATE |
| 6075 | body | EXTRA | `div.col-md-8.col-12` | `—` | `p>a` | 126 | 83 | 0.99 of 1950 | subject=1-10 Mathematics c=1.00 n=26 | structure | — | CANDIDATE |
| 6079 | body | EXTRA | `p` | `—` | `b` | 99 | 79 | 0.93 of 1950 | template=Standard c=0.94 n=84 | structure | — | CANDIDATE |
| 6080 | body | SUBSTITUTED | `div.col-md-8.col-12` | `h3` | `h4` | 112 | 76 | 0.48 of 1950 | template+ptype=Fundamentals/overview c=0.93 n=20 | structure | — | CANDIDATE |
| 6082 | body | EXTRA | `div.table-responsive` | `—` | `table.table.table-bordered` | 118 | 73 | 0.96 of 1950 | template=Standard c=0.97 n=105 | structure | yes | CANDIDATE |
| 6083 | body | EXTRA | `p>i` | `—` | `i` | 98 | 73 | 0.97 of 1950 | subject=1-10 Blended Literacy c=1.00 n=26 | structure | — | CANDIDATE |
| 6088 | body | EXTRA | `div.col-md-8.col-12` | `—` | `ol` | 99 | 68 | 0.99 of 1950 | ptype=overview c=0.99 n=24 | structure | — | CANDIDATE |
| 6089 | body | SUBSTITUTED | `div.videoSection.icon.ratio.ratio-16x9` | `iframe.embed-responsive-item` | `iframe` | 172 | 66 | 0.21 of 1950 | series=PES10 c=0.68 n=35 | structure | yes | CANDIDATE |
| 6092 | body | EXTRA | `table.table.table-bordered` | `—` | `tr` | 98 | 63 | 0.98 of 1950 | template=Standard c=0.99 n=87 | structure | yes | CANDIDATE |
| 6094 | body | EXTRA | `div.col-md-8.col-12` | `—` | `p>i` | 89 | 63 | 0.98 of 1950 | subject=NCEA1 c=0.99 n=23 | structure | — | CANDIDATE |
| 6096 | body | EXTRA | `div.col-md-8.col-12` | `—` | `audio.audioPlayer.icon` | 106 | 62 | 1.00 of 1950 | subject=Leaving to Learn c=1.00 n=34 | structure | yes | CANDIDATE |
| 6099 | body | EXTRA | `div.row` | `—` | `div.col-12` | 110 | 60 | 0.84 of 1950 | subject=ANZH c=0.87 n=20 | structure | — | CANDIDATE |
| 6101 | body | EXTRA | `div.videoSection.ratio.ratio-16x9` | `—` | `iframe` | 80 | 60 | 0.93 of 1950 | subject=1-10 Mathematics c=0.95 n=25 | structure | yes | CANDIDATE |
| 6107 | body | EXTRA | `ul` | `—` | `li` | 68 | 56 | 0.93 of 1950 | template=Standard c=0.94 n=49 | structure | — | CANDIDATE |
| 6110 | body | EXTRA | `p>a` | `—` | `a` | 62 | 54 | 0.99 of 1950 | template=Standard c=1.00 n=44 | structure | — | CANDIDATE |
| 6114 | body | SUBSTITUTED | `div.row` | `div.col-md-8.col-12` | `div.col-md-8.col-12` | 56 | 49 | 0.98 of 1950 | ptype=lesson c=0.99 n=28 | structure | — | CANDIDATE |
| 6116 | body | SUBSTITUTED | `div#body` | `div.row` | `WIDGET` | 58 | 48 | 0.94 of 1950 | template+ptype=Standard/lesson c=0.98 n=51 | structure | — | CANDIDATE |
| 6118 | body | EXTRA | `div.fundamentalsPanel` | `—` | `div.row` | 45 | 45 | 0.99 of 1950 | era=Refresh c=0.99 n=45 | structure | — | CANDIDATE |
| 6122 | body | EXTRA | `div.alert` | `—` | `div.row` | 55 | 42 | 0.91 of 1950 | template=Standard c=0.92 n=41 | structure | — | CANDIDATE |
| 6125 | body | EXTRA | `div.col-12` | `—` | `p` | 68 | 41 | 0.86 of 1950 | template=Standard c=0.88 n=59 | structure | — | CANDIDATE |
| 6126 | body | EXTRA | `div.row` | `—` | `div.col-md-6.col-12` | 58 | 41 | 0.99 of 1950 | subject=Online Safety (OS9000) c=1.00 n=20 | structure | — | CANDIDATE |
| 6128 | body | SUBSTITUTED | `div.col-md-8.col-12` | `p` | `p` | 55 | 41 | 0.85 of 1950 | template+ptype=Standard/lesson c=0.85 n=37 | structure | — | CANDIDATE |
| 6129 | body | EXTRA | `a` | `—` | `div.externalButton` | 63 | 40 | 0.92 of 1950 | template=Standard c=0.93 n=57 | structure | — | CANDIDATE |
| 6131 | body | EXTRA | `tr` | `—` | `th` | 45 | 40 | 0.98 of 1950 | template=Standard c=0.99 n=40 | structure | — | CANDIDATE |
| 6133 | body | EXTRA | `div#body` | `—` | `div.row.supervisor` | 50 | 38 | 0.88 of 1950 | ptype=lesson c=0.89 n=45 | structure | yes | CANDIDATE |
| 6134 | body | EXTRA | `tr` | `—` | `td` | 42 | 38 | 0.95 of 1950 | template=Standard c=0.95 n=35 | structure | — | CANDIDATE |
| 6140 | body | MISSING | `div#body` | `div.fundamentalsPanel` | `—` | 36 | 36 | 0.02 of 1950 | template+ptype=Fundamentals/overview c=0.87 n=35 | 1.00 | yes | CANDIDATE |
| 6144 | body | EXTRA | `p` | `—` | `i` | 43 | 35 | 0.97 of 1950 | template=Standard c=0.97 n=41 | structure | — | CANDIDATE |
| 6151 | body | SUBSTITUTED | `div.row` | `div.col-md-8.col-12` | `WIDGET` | 33 | 32 | 0.98 of 1950 | ptype=lesson c=0.99 n=28 | structure | — | CANDIDATE |
| 6152 | body | EXTRA | `div#body` | `—` | `WIDGET` | 50 | 31 | 0.94 of 1950 | era=Refresh c=0.94 n=50 | structure | — | CANDIDATE |
| 6154 | body | EXTRA | `div.col-md-8.col-12` | `—` | `h5` | 37 | 31 | 1.00 of 1950 | template=Standard c=1.00 n=21 | structure | — | CANDIDATE |
| 6155 | body | EXTRA | `div#body` | `—` | `div.fundamentalsPanel` | 31 | 31 | 0.98 of 1950 | era=Refresh c=0.98 n=31 | structure | yes | CANDIDATE |
| 6156 | body | EXTRA | `div.col-md-8.col-12` | `—` | `h4.goJournal` | 41 | 30 | 1.00 of 1950 | subject=1-10 Mathematics c=1.00 n=22 | structure | — | CANDIDATE |
| 6160 | body | EXTRA | `div.inquiryPanel` | `—` | `div.row` | 29 | 29 | 0.99 of 1950 | era=Refresh c=0.99 n=29 | structure | — | CANDIDATE |
| 6161 | body | SUBSTITUTED | `div.row` | `div.col-md-8.col-12` | `div.row` | 29 | 29 | 0.98 of 1950 | era=Refresh c=0.98 n=29 | structure | — | CANDIDATE |
| 6162 | body | EXTRA | `div.col-md-8.col-12` | `—` | `div.videoSection.icon.ratio.ratio-16x9` | 43 | 28 | 0.91 of 1950 | template=Standard c=0.93 n=33 | structure | yes | CANDIDATE |
| 6163 | body | EXTRA | `div.col-md-8.col-12` | `—` | `div.alert` | 36 | 28 | 0.91 of 1950 | template=Standard c=0.92 n=29 | structure | — | CANDIDATE |
| 6168 | body | EXTRA | `div.row` | `—` | `div.col-md-4.offset-md-0.col-12` | 27 | 27 | 0.79 of 1950 | era=Refresh c=0.79 n=27 | structure | — | CANDIDATE |
| 6180 | body | EXTRA | `div#body` | `—` | `div.inquiryPanel` | 24 | 24 | 0.99 of 1950 | era=Refresh c=0.99 n=24 | structure | — | CANDIDATE |
| 6183 | body | EXTRA | `div.col-md-8.col-12` | `—` | `p>span.infoTrigger` | 29 | 23 | 0.86 of 1950 | template=Standard c=0.87 n=26 | structure | — | CANDIDATE |
| 6185 | body | SUBSTITUTED | `div.col-md-8.col-12` | `p` | `WIDGET` | 24 | 23 | 0.85 of 1950 | era=Refresh c=0.85 n=24 | structure | — | CANDIDATE |
| 6192 | body | EXTRA | `div.row.flipCardsContainer` | `—` | `div.col-md-4.col-12.paddingLR` | 23 | 22 | 0.97 of 1950 | era=Refresh c=0.97 n=23 | structure | — | CANDIDATE |
| 6195 | body | EXTRA | `div.alert.solid` | `—` | `div.row` | 30 | 21 | 0.99 of 1950 | template=Standard c=0.99 n=25 | structure | yes | CANDIDATE |
| 6197 | body | EXTRA | `div.col-md-8.col-12` | `—` | `div.row.flipCardsContainer` | 26 | 21 | 0.93 of 1950 | template=Standard c=0.94 n=23 | structure | — | CANDIDATE |
| 6201 | body | SUBSTITUTED | `div.col-md-8.col-12` | `p` | `img.img-fluid` | 21 | 21 | 0.85 of 1950 | era=Refresh c=0.85 n=21 | structure | — | CANDIDATE |
| 6205 | body | EXTRA | `div.videoSection.icon.ratio.ratio-16x9` | `—` | `iframe` | 26 | 20 | 0.97 of 1950 | ptype=lesson c=0.98 n=21 | structure | yes | CANDIDATE |
| 6207 | body | SUBSTITUTED | `div.row` | `div.col-md-8.col-12` | `p` | 20 | 20 | 0.98 of 1950 | era=Refresh c=0.98 n=20 | structure | — | CANDIDATE |
| 6210 | body | EXTRA | `div.col-md-8.col-12` | `—` | `div.alert.solid` | 25 | 19 | 0.99 of 1950 | era=Refresh c=0.99 n=25 | structure | yes | CANDIDATE |
| 6213 | body | EXTRA | `div.row` | `—` | `div.col-md-4.col-12` | 23 | 19 | 0.95 of 1950 | era=Refresh c=0.95 n=23 | structure | — | CANDIDATE |
| 6215 | body | EXTRA | `div.row` | `—` | `div.clickDropContent` | 21 | 19 | 1.00 of 1950 | era=Refresh c=1.00 n=21 | structure | — | CANDIDATE |
| 6216 | body | EXTRA | `div.col-md-8.col-12` | `—` | `div.row` | 21 | 19 | 0.75 of 1950 | era=Refresh c=0.75 n=21 | structure | — | CANDIDATE |
| 6218 | body | SUBSTITUTED | `div.col-md-8.col-12` | `p` | `ul` | 21 | 19 | 0.85 of 1950 | era=Refresh c=0.85 n=21 | structure | — | CANDIDATE |
| 6225 | body | SUBSTITUTED | `div.col-md-8.col-12` | `p` | `h3` | 20 | 18 | 0.85 of 1950 | era=Refresh c=0.85 n=20 | structure | — | CANDIDATE |
| 6226 | body | SUBSTITUTED | `div.row` | `div.col-md-8.col-12` | `div.col-md-6.col-12` | 20 | 18 | 0.98 of 1950 | era=Refresh c=0.98 n=20 | structure | — | CANDIDATE |
| 6229 | body | SUBSTITUTED | `div.col-md-8.col-12` | `p` | `div.alert` | 26 | 17 | 0.85 of 1950 | era=Refresh c=0.85 n=26 | structure | — | CANDIDATE |
| 6236 | body | EXTRA | `th>b` | `—` | `b` | 22 | 16 | 1.00 of 1950 | era=Refresh c=1.00 n=22 | structure | — | CANDIDATE |
| 6254 | body | MISSING | `div#body` | `div.row.clickDropContent.noBorder` | `—` | 49 | 14 | 0.03 of 1950 | series=XDLS90 c=0.64 n=38 | 0.94 | yes | CANDIDATE |
| 6255 | body | EXTRA | `div.col-12` | `—` | `ul` | 20 | 14 | 0.88 of 1950 | era=Refresh c=0.88 n=20 | structure | — | CANDIDATE |
| 10907 | root | EXTRA | `body.container-fluid` | `—` | `div.row` | 233 | 233 | 0.87 of 1956 | subject+ptype=NCEA1/overview c=0.98 n=41 | structure | — | CANDIDATE |
| 10912 | root | SUBSTITUTED | `#root` | `html.notranslate` | `body.container-fluid` | 95 | 11 | 0.05 of 1956 | series=CEDO50 c=1.00 n=25 | structure | yes | CANDIDATE |

## Candidate and top-row details (three example modules each — WT / gold / Claude quoted)

### #1 · module-code · EXTRA · `div#header` › gold `—` vs Claude `div#module-code` — BELOW FLOOR
- pages 4 / modules 4 / lines 4; consensus (all) 0.03 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Fundamentals 3m/3p c=0.44; Inquiry 1m/1p c=0.28
- by subject: 1-10 Health and PE 2m/2p c=0.13; ConnectED 1m/1p c=0.13; 1-10 Social Science 1m/1p c=0.03
- by era: Refresh 4m/4p c=0.03
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:94 — **Header:** `#module-code` → `<h1>` (module code or lesson number), then `<h1><span>Title</span></h1>`, then `#module-head-buttons` → `#module-menu-bu
  - KB: 13_SPLIT_MODE.md:70 — <div id="header"> … module-code, title h1(s), menu button, full #module-menu-content … </div>
  - KB: INDEX.md:26 — - **`00_MASTER_INSTRUCTIONS/00H_CONSTRAINTS_4.md`** (18 KB) — Constraints quick reference, part 4 of 4 — **constraints 86 onward** (86 `ADMIN MODE` pr
- **CEDT301** CEDT301_6_0.html ↔ CEDT301 My place and me.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div#module-code  «6.0»`
- **HPFUN201** HPFUN201_0_0.html ↔ HPFUN201.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div#module-code  «HPFUN201»`
- **HPFUN302** HPFUN302_0_0.html ↔ HPFUN302.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div#module-code  «HPFUN302»`
- modules: CEDT301, HPFUN201, HPFUN302, SSFUN01

### #2 · module-code · MISSING · `div#header` › gold `div#module-code` vs Claude `—` — BELOW FLOOR
- pages 3 / modules 3 / lines 3; consensus (all) 0.97 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 2m/2p c=1.00; Inquiry 1m/1p c=0.72
- by subject: EXPlore 2m/2p c=0.27; 1-10 Blended Literacy 1m/1p c=0.98
- by era: Refresh 3m/3p c=0.97
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:94 — **Header:** `#module-code` → `<h1>` (module code or lesson number), then `<h1><span>Title</span></h1>`, then `#module-head-buttons` → `#module-menu-bu
  - KB: 13_SPLIT_MODE.md:70 — <div id="header"> … module-code, title h1(s), menu button, full #module-menu-content … </div>
  - KB: INDEX.md:26 — - **`00_MASTER_INSTRUCTIONS/00H_CONSTRAINTS_4.md`** (18 KB) — Constraints quick reference, part 4 of 4 — **constraints 86 onward** (86 `ADMIN MODE` pr
- **BLL170** BLL170_0_0.html ↔ BLL170.html (structure, derivable=True)
  - gold: `div#module-code  «BLL170»`
  - Claude: `—`
- **EXBP901** EXBP901_2_0.html ↔ EXBP901_1.1.html (structure, derivable=True)
  - gold: `div#module-code  «EXBP901»`
  - Claude: `—`
- **EXIP901** EXIP901_1_0.html ↔ EXIP901_0.0.html (structure, derivable=True)
  - gold: `div#module-code  «EXIP901»`
  - Claude: `—`
- modules: BLL170, EXBP901, EXIP901

### #3 · module-code · EXTRA · `div#module-code` › gold `—` vs Claude `h1` — BELOW FLOOR
- pages 1 / modules 1 / lines 1; consensus (all) 0.03 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Fundamentals 1m/1p c=0.44
- by subject: Leaving to Learn 1m/1p c=0.01
- by era: Refresh 1m/1p c=0.03
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:94 — **Header:** `#module-code` → `<h1>` (module code or lesson number), then `<h1><span>Title</span></h1>`, then `#module-head-buttons` → `#module-menu-bu
  - KB: 13_SPLIT_MODE.md:70 — <div id="header"> … module-code, title h1(s), menu button, full #module-menu-content … </div>
  - KB: INDEX.md:26 — - **`00_MASTER_INSTRUCTIONS/00H_CONSTRAINTS_4.md`** (18 KB) — Constraints quick reference, part 4 of 4 — **constraints 86 onward** (86 `ADMIN MODE` pr
- **XFUN01** XFUN01_0_0.html ↔ XFUN01.00.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h1  «XFUN01»`
- modules: XFUN01

### #4 · title · MISSING · `div#header` › gold `h1>span` vs Claude `—` — CANDIDATE
- pages 189 / modules 105 / lines 191; consensus (all) 0.22 of 1956 gold pages with the region; derivable 0.72 (54 lines with no WT source)
- by template: Standard 69m/139p c=0.17; Fundamentals 23m/23p c=0.58; Inquiry 9m/12p c=0.33; Bilingual 4m/15p c=1.00
- by subject: 1-10 English 19m/19p c=0.15; Leaving to Learn 14m/22p c=0.26; NCEA1 13m/19p c=0.14; Online Safety (OS9000) 13m/29p c=0.33; 1-10 Mathematics 11m/11p c=0.14; ANZH 5m/30p c=0.55
- by era: Refresh 105m/189p c=0.22
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:94 — **Header:** `#module-code` → `<h1>` (module code or lesson number), then `<h1><span>Title</span></h1>`, then `#module-head-buttons` → `#module-menu-bu
  - KB: 00_MASTER_INSTRUCTIONS/00B_CONVERSION_PIPELINE.md:204 — - Lesson pages: use THAT LESSON'S OWN title in the header <h1><span> (never the module title) and the zero-padded lesson number (not the module code) 
  - KB: 00_MASTER_INSTRUCTIONS/00D_CONSTRAINTS_1.md:24 — 16. Lesson pages: zero-padded lesson number (e.g., `01`, `02`) in `#module-code`; **that lesson's own title** in `<h1><span>` — NOT the module title, 
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html (content, derivable=False)
  - gold: `h1  «Ko ngā Ingoa Waahi ngā Kōrero ake»`
  - Claude: `—`
- **ANZH104** ANZH104_4_0.html ↔ ANZH104_04.0.html (content, derivable=True)
  - gold: `h1  «Hunting for Food in the Water»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [H2]  [/RED TEXT]🔴Lesson 4 – Hunting for Food in the Water`
- **ANZH301** ANZH301_3_0.html ↔ ANZH301_3.0.html (content, derivable=True)
  - gold: `h1  «Ngā Raiti Nui o te Tāone»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [TITLE BAR] [/RED TEXT]🔴 **Ngā Raiti Nui o te Tāone** **| Big City Lights**`
- modules: ANZH101, ANZH104, ANZH301, ANZH401, ANZH404, ARFUN01, ARFUN02, ARFUN03, ARFUN04, ARFUN05, ART1004, ART1006, CEDK102, CEDK501, CEDO202, CEDR204, CEDT301, ENFUN01, ENFUN02, ENFUN03, ENFUN04, ENFUN05, ENFUN07, ENFUN08 …

### #5 · title · EXTRA · `div#header` › gold `—` vs Claude `h1>span` — CANDIDATE
- pages 11 / modules 11 / lines 11; consensus (all) 0.78 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 9m/9p c=0.83; Inquiry 1m/1p c=0.67; Fundamentals 1m/1p c=0.42
- by subject: NCEA1 3m/3p c=0.86; Leaving to Learn 3m/3p c=0.74; 1-10 Blended Literacy 2m/2p c=1.00; ConnectED 1m/1p c=0.78; 1-10 English 1m/1p c=0.84; 1-10 Social Science 1m/1p c=0.71
- by era: Refresh 11m/11p c=0.78
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:94 — **Header:** `#module-code` → `<h1>` (module code or lesson number), then `<h1><span>Title</span></h1>`, then `#module-head-buttons` → `#module-menu-bu
  - KB: 00_MASTER_INSTRUCTIONS/00B_CONVERSION_PIPELINE.md:204 — - Lesson pages: use THAT LESSON'S OWN title in the header <h1><span> (never the module title) and the zero-padded lesson number (not the module code) 
  - KB: 00_MASTER_INSTRUCTIONS/00D_CONSTRAINTS_1.md:24 — 16. Lesson pages: zero-padded lesson number (e.g., `01`, `02`) in `#module-code`; **that lesson's own title** in `<h1><span>` — NOT the module title, 
- **AGH1005** AGH1005_0_0.html ↔ AGH1005.00.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h1  «Unlocking Plant Magic: Exploring plant growth and processes in Aotearoa, New Zealand.»`
- **BLL144** BLL144_1_0.html ↔ BLL144-1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h1  «j, ai, oa, ie, ee, or»`
- **BLL246** BLL246_0_0.html ↔ BLL246_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h1  «Module»`
- modules: AGH1005, BLL144, BLL246, CEDO105, ENGFUN02, ENGI103, HIS1002, SSFUN07, XDLS904, XDLS906, XFUN02

### #6 · title · MISSING · `span>span.sassoonI-text` › gold `span.sassoonI-text` vs Claude `—` — BELOW FLOOR
- pages 14 / modules 4 / lines 28; consensus (all) 0.01 of 1956 gold pages with the region; derivable 0.79 (6 lines with no WT source)
- by template: Bilingual 4m/14p c=0.22
- by subject: Te Marautanga o Aotearoa TMoA 4m/14p c=0.22
- by era: Refresh 4m/14p c=0.01
- authority (§1b): 4/none — no KB rule, no group consensus ≥ 0.60 at the floor
- **TRR103** TRR103_0_0.html ↔ TRR103_0.0.html (content, derivable=True)
  - gold: `span.sassoonI-text  «Ee»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] Module Code:  [/RED TEXT]🔴TRR103 Ngā Oropuare -Ee		🔴[RED TEXT] Resource Developer: [/RED TEXT]🔴 **Arohanui Allen | Tracy Krivan**`
- **TRR106** TRR106_0_0.html ↔ TRR106_0.0.html (content, derivable=True)
  - gold: `span.sassoonI-text  «Uu»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] Module Code:  [/RED TEXT]🔴	TRR 1002 Ngā Oropuare Uu	🔴[RED TEXT] Resource Developer: [/RED TEXT]🔴 **Tracy Krivan| Arohanui Allen**`
- **TRR107** TRR107_2_0.html ↔ TRR107_2.0.html (content, derivable=False)
  - gold: `span.sassoonI-text  «Aa»`
  - Claude: `—`
- modules: TRR103, TRR106, TRR107, TRR111

### #7 · title · SUBSTITUTED · `div#header` › gold `h1>span` vs Claude `div#module-head-buttons` — BELOW FLOOR
- pages 3 / modules 3 / lines 3; consensus (all) 1.00 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 2m/2p c=1.00; Fundamentals 1m/1p c=1.00
- by subject: NCEA1 1m/1p c=1.00; ConnectED 1m/1p c=1.00; 1-10 Technology 1m/1p c=1.00
- by era: Refresh 3m/3p c=1.00
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:94 — **Header:** `#module-code` → `<h1>` (module code or lesson number), then `<h1><span>Title</span></h1>`, then `#module-head-buttons` → `#module-menu-bu
  - KB: 00_MASTER_INSTRUCTIONS/00B_CONVERSION_PIPELINE.md:204 — - Lesson pages: use THAT LESSON'S OWN title in the header <h1><span> (never the module title) and the zero-padded lesson number (not the module code) 
  - KB: 00_MASTER_INSTRUCTIONS/00D_CONSTRAINTS_1.md:24 — 16. Lesson pages: zero-padded lesson number (e.g., `01`, `02`) in `#module-code`; **that lesson's own title** in `<h1><span>` — NOT the module title, 
- **ART1005** ART1005_0_0.html ↔ ART1005_3.0.html (structure, derivable=True)
  - gold: `h1  «Create portfolio artworks»`
  - Claude: `div#module-head-buttons`
- **CEDO502** CEDO502_8_0.html ↔ CEDO502_8_0.html (structure, derivable=True)
  - gold: `h1  «Making More Decisions»`
  - Claude: `div#module-head-buttons`
- **TEFUN07** TEFUN07_0_0.html ↔ TEFUN07.html (structure, derivable=True)
  - gold: `h1  «PLACEHOLDER»`
  - Claude: `div#module-head-buttons`
- modules: ART1005, CEDO502, TEFUN07

### #8 · title · MISSING · `div.titlebar` › gold `h1.moduleTitle>span.module-subtitle.text-lowercase` vs Claude `—` — BELOW FLOOR
- pages 2 / modules 1 / lines 2; consensus (all) 0.00 of 1956 gold pages with the region; derivable 1.00 (0 lines with no WT source)
- by template: Standard 1m/2p c=0.00
- by subject: 1-10 Blended Literacy 1m/2p c=0.01
- by era: Refresh 1m/2p c=0.00
- authority (§1b): 4/none — no KB rule, no group consensus ≥ 0.60 at the floor
- **BLL236** BLL236_1_0.html ↔ BLL236-1.0.html (content, derivable=True)
  - gold: `h1.moduleTitle  «oe, ow, ir, ur, ui, ew, au, aw, al, ph, kn, wr»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [TITLE BAR]   [/RED TEXT]🔴 *Module 6 - oe, ow, ir, ur, ui, ew, au, aw, al, ph, kn, wr*`
- modules: BLL236

### #9 · title · EXTRA · `span>span` › gold `—` vs Claude `span` — BELOW FLOOR
- pages 1 / modules 1 / lines 1; consensus (all) 0.99 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Inquiry 1m/1p c=0.88
- by subject: 1-10 Blended Literacy 1m/1p c=0.96
- by era: Refresh 1m/1p c=0.99
- authority (§1b): 4/none — no KB rule, no group consensus ≥ 0.60 at the floor
- **BLL240** BLL240_0_0.html ↔ BLL240-0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `span  «wh, tch, dge, air, ear, ere, eer»`
- modules: BLL240

### #10 · title · EXTRA · `h1>span` › gold `—` vs Claude `span` — BELOW FLOOR
- pages 1 / modules 1 / lines 1; consensus (all) 0.01 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 1m/1p c=0.00
- by subject: 1-10 Mathematics 1m/1p c=0.00
- by era: Refresh 1m/1p c=0.01
- authority (§1b): 4/none — no KB rule, no group consensus ≥ 0.60 at the floor
- **MXFL104** MXFL104_1_0.html ↔ MXFL104_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `span  «1.0 Am I Staying Hydrated?»`
- modules: MXFL104

### #11 · title · EXTRA · `msub` › gold `—` vs Claude `mrow` — BELOW FLOOR
- pages 1 / modules 1 / lines 1; consensus (all) 1.00 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 1m/1p c=1.00
- by subject: NCEA1 1m/1p c=1.00
- by era: Refresh 1m/1p c=1.00
- authority (§1b): 4/none — no KB rule, no group consensus ≥ 0.60 at the floor
- **PES1007** PES1007_3_0.html ↔ PES1007_3.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `mrow  «k»`
- modules: PES1007

### #12 · title · EXTRA · `mfrac` › gold `—` vs Claude `mrow` — BELOW FLOOR
- pages 1 / modules 1 / lines 1; consensus (all) 1.00 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 1m/1p c=1.00
- by subject: NCEA1 1m/1p c=1.00
- by era: Refresh 1m/1p c=1.00
- authority (§1b): 4/none — no KB rule, no group consensus ≥ 0.60 at the floor
- **PES1007** PES1007_3_0.html ↔ PES1007_3.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `mrow  «2»`
- modules: PES1007

### #13 · title · EXTRA · `mrow` › gold `—` vs Claude `mi` — BELOW FLOOR
- pages 1 / modules 1 / lines 1; consensus (all) 1.00 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 1m/1p c=1.00
- by subject: NCEA1 1m/1p c=1.00
- by era: Refresh 1m/1p c=1.00
- authority (§1b): 4/none — no KB rule, no group consensus ≥ 0.60 at the floor
- **PES1007** PES1007_3_0.html ↔ PES1007_3.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `mi  «v»`
- modules: PES1007

### #14 · title · EXTRA · `msup` › gold `—` vs Claude `mrow` — BELOW FLOOR
- pages 1 / modules 1 / lines 1; consensus (all) 1.00 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 1m/1p c=1.00
- by subject: NCEA1 1m/1p c=1.00
- by era: Refresh 1m/1p c=1.00
- authority (§1b): 4/none — no KB rule, no group consensus ≥ 0.60 at the floor
- **PES1007** PES1007_3_0.html ↔ PES1007_3.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `mrow  «2»`
- modules: PES1007

### #15 · title · MISSING · `h1>span` › gold `span` vs Claude `—` — BELOW FLOOR
- pages 1 / modules 1 / lines 1; consensus (all) 0.99 of 1956 gold pages with the region; derivable 1.00 (0 lines with no WT source)
- by template: Standard 1m/1p c=1.00
- by subject: 1-10 Blended Literacy 1m/1p c=0.95
- by era: Refresh 1m/1p c=0.99
- authority (§1b): 4/none — no KB rule, no group consensus ≥ 0.60 at the floor
- **BLL144** BLL144_1_0.html ↔ BLL144-1.0.html (content, derivable=True)
  - gold: `span  «j, ai, oa, ie, ee, or»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [TITLE BAR]   [/RED TEXT]🔴 *Module 4 - j, ai, oa, ie, ee, or*`
- modules: BLL144

### #16 · title · MISSING · `span>span` › gold `span` vs Claude `—` — BELOW FLOOR
- pages 1 / modules 1 / lines 1; consensus (all) 0.01 of 1956 gold pages with the region; derivable 1.00 (0 lines with no WT source)
- by template: Inquiry 1m/1p c=0.12
- by subject: 1-10 Blended Literacy 1m/1p c=0.04
- by era: Refresh 1m/1p c=0.01
- authority (§1b): 4/none — no KB rule, no group consensus ≥ 0.60 at the floor
- **BLL240** BLL240_1_0.html ↔ BLL240.html (content, derivable=True)
  - gold: `span  «wh, tch, dge, air, ear, ere, eer»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [TITLE BAR]  [/RED TEXT]🔴 *LEARNING THE SOUNDS – wh, tch,* *dge**, air, ear, ere, eer*`
- modules: BLL240

### #17 · title · MISSING · `msup` › gold `mn` vs Claude `—` — BELOW FLOOR
- pages 1 / modules 1 / lines 1; consensus (all) 0.00 of 1956 gold pages with the region; derivable 1.00 (0 lines with no WT source)
- by template: Standard 1m/1p c=0.00
- by subject: NCEA1 1m/1p c=0.00
- by era: Refresh 1m/1p c=0.00
- authority (§1b): 4/none — no KB rule, no group consensus ≥ 0.60 at the floor
- **PES1007** PES1007_3_0.html ↔ PES1007_3.0.html (content, derivable=True)
  - gold: `mn  «2»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [LESSON] 2  [/RED TEXT]🔴`
- modules: PES1007

### #18 · title · SUBSTITUTED · `msub` › gold `mi` vs Claude `mrow` — BELOW FLOOR
- pages 1 / modules 1 / lines 1; consensus (all) 0.00 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 1m/1p c=0.00
- by subject: NCEA1 1m/1p c=0.00
- by era: Refresh 1m/1p c=0.00
- authority (§1b): 4/none — no KB rule, no group consensus ≥ 0.60 at the floor
- **PES1007** PES1007_3_0.html ↔ PES1007_3.0.html (structure, derivable=True)
  - gold: `mi  «E»`
  - Claude: `mrow  «E»`
- modules: PES1007

### #19 · title · SUBSTITUTED · `msub` › gold `mi` vs Claude `mi` — BELOW FLOOR
- pages 1 / modules 1 / lines 1; consensus (all) 0.00 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 1m/1p c=0.00
- by subject: NCEA1 1m/1p c=0.00
- by era: Refresh 1m/1p c=0.00
- authority (§1b): 4/none — no KB rule, no group consensus ≥ 0.60 at the floor
- **PES1007** PES1007_3_0.html ↔ PES1007_3.0.html (structure, derivable=True)
  - gold: `mi  «k»`
  - Claude: `mi  «E»`
- modules: PES1007

### #20 · title · SUBSTITUTED · `mfrac` › gold `mn` vs Claude `mrow` — BELOW FLOOR
- pages 1 / modules 1 / lines 1; consensus (all) 0.00 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 1m/1p c=0.00
- by subject: NCEA1 1m/1p c=0.00
- by era: Refresh 1m/1p c=0.00
- authority (§1b): 4/none — no KB rule, no group consensus ≥ 0.60 at the floor
- **PES1007** PES1007_3_0.html ↔ PES1007_3.0.html (structure, derivable=True)
  - gold: `mn  «1»`
  - Claude: `mrow  «1»`
- modules: PES1007

### #21 · title · SUBSTITUTED · `mfrac` › gold `mn` vs Claude `mn` — BELOW FLOOR
- pages 1 / modules 1 / lines 1; consensus (all) 0.00 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 1m/1p c=0.00
- by subject: NCEA1 1m/1p c=0.00
- by era: Refresh 1m/1p c=0.00
- authority (§1b): 4/none — no KB rule, no group consensus ≥ 0.60 at the floor
- **PES1007** PES1007_3_0.html ↔ PES1007_3.0.html (structure, derivable=True)
  - gold: `mn  «2»`
  - Claude: `mn  «1»`
- modules: PES1007

### #22 · title · SUBSTITUTED · `msup` › gold `mi` vs Claude `mrow` — BELOW FLOOR
- pages 1 / modules 1 / lines 1; consensus (all) 0.00 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 1m/1p c=0.00
- by subject: NCEA1 1m/1p c=0.00
- by era: Refresh 1m/1p c=0.00
- authority (§1b): 4/none — no KB rule, no group consensus ≥ 0.60 at the floor
- **PES1007** PES1007_3_0.html ↔ PES1007_3.0.html (structure, derivable=True)
  - gold: `mi  «v»`
  - Claude: `mrow  «v»`
- modules: PES1007

### #23 · title · SUBSTITUTED · `div#header` › gold `h1>span` vs Claude `div#module-code` — BELOW FLOOR
- pages 1 / modules 1 / lines 1; consensus (all) 1.00 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Fundamentals 1m/1p c=1.00
- by subject: Leaving to Learn 1m/1p c=1.00
- by era: Refresh 1m/1p c=1.00
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:94 — **Header:** `#module-code` → `<h1>` (module code or lesson number), then `<h1><span>Title</span></h1>`, then `#module-head-buttons` → `#module-menu-bu
  - KB: 00_MASTER_INSTRUCTIONS/00B_CONVERSION_PIPELINE.md:204 — - Lesson pages: use THAT LESSON'S OWN title in the header <h1><span> (never the module title) and the zero-padded lesson number (not the module code) 
  - KB: 00_MASTER_INSTRUCTIONS/00D_CONSTRAINTS_1.md:24 — 16. Lesson pages: zero-padded lesson number (e.g., `01`, `02`) in `#module-code`; **that lesson's own title** in `<h1><span>` — NOT the module title, 
- **XFUN01** XFUN01_0_0.html ↔ XFUN01.00.html (structure, derivable=True)
  - gold: `h1  «Let Technology assist»`
  - Claude: `div#module-code  «XFUN01»`
- modules: XFUN01

### #24 · header · MISSING · `div#header` › gold `p` vs Claude `—` — BELOW FLOOR
- pages 3 / modules 1 / lines 3; consensus (all) 0.00 of 1956 gold pages with the region; derivable 0.00 (3 lines with no WT source)
- by template: Bilingual 1m/3p c=0.05
- by subject: Te Marautanga o Aotearoa TMoA 1m/3p c=0.05
- by era: Refresh 1m/3p c=0.00
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:39 — | Header tag | `<nav id="module-head">` | `<div id="header">` |
  - KB: 06_TEMPLATE_RECOGNITION.md:94 — **Header:** `#module-code` → `<h1>` (module code or lesson number), then `<h1><span>Title</span></h1>`, then `#module-head-buttons` → `#module-menu-bu
  - KB: 06_TEMPLATE_RECOGNITION.md:130 — **Header:** Always has dual `<h1>` titles (English + te reo).
- **TRR114** TRR114_0_0.html ↔ TRR114_0.0.html (content, derivable=False)
  - gold: `p  «Designer note: title please»`
  - Claude: `—`
- modules: TRR114

### #25 · header · SUBSTITUTED · `div#header` › gold `div.titlebar` vs Claude `h1>span` — BELOW FLOOR
- pages 2 / modules 1 / lines 2; consensus (all) 0.00 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 1m/2p c=0.00
- by subject: 1-10 Blended Literacy 1m/2p c=0.01
- by era: Refresh 1m/2p c=0.00
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:39 — | Header tag | `<nav id="module-head">` | `<div id="header">` |
  - KB: 06_TEMPLATE_RECOGNITION.md:94 — **Header:** `#module-code` → `<h1>` (module code or lesson number), then `<h1><span>Title</span></h1>`, then `#module-head-buttons` → `#module-menu-bu
  - KB: 06_TEMPLATE_RECOGNITION.md:130 — **Header:** Always has dual `<h1>` titles (English + te reo).
- **BLL236** BLL236_1_0.html ↔ BLL236-1.0.html (structure, derivable=True)
  - gold: `div.titlebar  «oe, ow, ir, ur, ui, ew, au, aw, al, ph, kn, wr»`
  - Claude: `h1  «oe, ow, ir, ur, ui, ew, au, aw, al, ph, kn, wr»`
- modules: BLL236

### #26 · module-menu · SUBSTITUTED · `div.col-md-6.col-12.paddingR` › gold `p` vs Claude `h5` — CANDIDATE
- pages 83 / modules 83 / lines 150; consensus (all) 0.07 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 61m/61p c=0.06; Fundamentals 14m/14p c=0.22; Inquiry 8m/8p c=0.35
- by subject: 1-10 Blended Literacy 69m/69p c=0.30; 1-10 Health and PE 14m/14p c=0.93
- by era: Refresh 83m/83p c=0.07
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

### #27 · module-menu · MISSING · `ul` › gold `li` vs Claude `—` — CANDIDATE
- pages 107 / modules 72 / lines 309; consensus (all) 0.11 of 1956 gold pages with the region; derivable 0.88 (37 lines with no WT source)
- by template: Standard 53m/88p c=0.11; Inquiry 11m/11p c=0.25; Fundamentals 8m/8p c=0.02
- by subject: 1-10 English 22m/39p c=0.12; 1-10 Blended Literacy 21m/21p c=0.24; 1-10 Mathematics 8m/23p c=0.09; NCEA1 7m/7p c=0.02; Te ara Whakapuawa -Wellbeing 5m/5p c=0.88; Leaving to Learn 3m/3p c=0.05
- by era: Refresh 72m/107p c=0.11
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
- modules: AGH1003, AGH1007, AGH1008, ANZH101, BLL110, BLL125, BLL126, BLL127, BLL130, BLL134, BLL136, BLL137, BLL140, BLL141, BLL143, BLL146, BLL147, BLL150, BLL151, BLL153, BLL154, BLL173, BLL210, BLL241 …

### #28 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `div.col-md-6.col-12.paddingR` — CANDIDATE
- pages 64 / modules 47 / lines 101; consensus (all) 0.96 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 40m/57p c=0.96; Inquiry 4m/4p c=0.90; Fundamentals 3m/3p c=1.00
- by subject: 1-10 Blended Literacy 19m/19p c=0.70; 1-10 Mathematics 7m/18p c=1.00; ANZH 6m/9p c=1.00; 1-10 English 4m/4p c=1.00; Leaving to Learn 4m/4p c=1.00; 1-10 Arts 3m/3p c=1.00
- by era: Refresh 47m/64p c=0.96
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:158 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **ANZH101** ANZH101_0_0.html ↔ ANZH101_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-6.col-12.paddingR  «Understand»`
- **ANZH104** ANZH104_0_0.html ↔ ANZH104_00.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-6.col-12.paddingR`
- **ANZH105** ANZH105_0_0.html ↔ ANZH105_00.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-6.col-12.paddingR  «Understand»`
- modules: ANZH101, ANZH104, ANZH105, ANZH203, ANZH205, ANZH401, ARFUN02, ARFUN03, ARFUN05, BLL110, BLL111, BLL120, BLL121, BLL134, BLL135, BLL144, BLL152, BLL160, BLL161, BLL172, BLL240, BLL241, BLL244, BLL245 …

### #29 · module-menu · EXTRA · `ul` › gold `—` vs Claude `li` — CANDIDATE
- pages 67 / modules 39 / lines 136; consensus (all) 0.77 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 28m/56p c=0.78; Inquiry 9m/9p c=0.46; Fundamentals 2m/2p c=0.59
- by subject: 1-10 Blended Literacy 10m/10p c=0.64; 1-10 English 8m/11p c=0.73; ConnectED 6m/6p c=0.56; NCEA1 5m/12p c=0.96; Te ara Whakapuawa -Wellbeing 4m/4p c=0.12; 1-10 Mathematics 2m/4p c=0.79
- by era: Refresh 39m/67p c=0.77
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
- modules: AGH1001, AGH1004, AGH1006, AGH1007, AGH1008, BLL115, BLL122, BLL123, BLL144, BLL145, BLL152, BLL165, BLL210, BLL241, BLL254, CEDK101, CEDO202, CEDO301, CEDR501, CEDT104, CEDT207, ENFUN03, ENFUN09, ENGC301 …

### #30 · module-menu · SUBSTITUTED · `div.col-md-6.col-12.paddingL` › gold `p` vs Claude `h5` — CANDIDATE
- pages 38 / modules 38 / lines 57; consensus (all) 0.03 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Fundamentals 14m/14p c=0.22; Standard 13m/13p c=0.02; Inquiry 11m/11p c=0.20
- by subject: 1-10 Health and PE 14m/14p c=0.93; ConnectED 7m/7p c=0.08; 1-10 Blended Literacy 5m/5p c=0.02; Te ara Whakapuawa -Wellbeing 4m/4p c=0.88; Leaving to Learn 4m/4p c=0.02; ANZH 2m/2p c=0.03
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

### #31 · module-menu · MISSING · `div.col-md-8.col-12` › gold `p` vs Claude `—` — BELOW CONSENSUS (no group ≥ 0.60 at the floor)
- pages 157 / modules 35 / lines 269; consensus (all) 0.09 of 1956 gold pages with the region; derivable 0.97 (9 lines with no WT source)
- by template: Standard 32m/145p c=0.10; Inquiry 3m/12p c=0.17
- by subject: Leaving to Learn 12m/30p c=0.36; 1-10 English 9m/53p c=0.14; ConnectED 5m/41p c=0.38; 1-10 Mathematics 5m/15p c=0.03; NCEA1 2m/14p c=0.02; Online Safety (OS9000) 1m/3p c=0.02
- by era: Refresh 35m/157p c=0.09
- authority (§1b): 4/none — no KB rule, no group consensus ≥ 0.60 at the floor
- **CEDK501** CEDK501_1_0.html ↔ CEDK501_1.0.html (content, derivable=True)
  - gold: `p  «We are learning:»`
  - Claude: `—`
  - WT: `*We are learning:*`
- **CEDO501** CEDO501_2_0.html ↔ CEDO501_2.0.html (content, derivable=True)
  - gold: `p  «We are learning:»`
  - Claude: `—`
  - WT: `*We are learning:*`
- **CEDR501** CEDR501_1_0.html ↔ CEDR501_1.0.html (structure, derivable=True)
  - gold: `p`
  - Claude: `—`
- modules: CEDK501, CEDO501, CEDR501, CEDT501, CEDW501, ENGI302, ENGJ202, ENGJ301, ENGJ302, ENGJ402, ENGR202, ENGS101, ENGS302, ENGS401, HIS1003, HIS1004, MXDI201, MXDI202, MXEO301, MXFL203, MXFL204, OSAI201, TEDC401, XDLS502 …

### #32 · module-menu · MISSING · `div.col-md-6.col-12.paddingR` › gold `p` vs Claude `—` — CANDIDATE
- pages 46 / modules 35 / lines 59; consensus (all) 0.05 of 1956 gold pages with the region; derivable 0.68 (19 lines with no WT source)
- by template: Standard 27m/38p c=0.05; Inquiry 8m/8p c=0.18
- by subject: 1-10 Blended Literacy 23m/23p c=0.28; EXPlore 5m/8p c=0.00; ConnectED 3m/3p c=0.09; ANZH 2m/2p c=0.00; 1-10 Mathematics 2m/10p c=0.04
- by era: Refresh 35m/46p c=0.05
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

### #33 · module-menu · MISSING · `div.col-md-8.col-12` › gold `ul` vs Claude `—` — BELOW CONSENSUS (no group ≥ 0.60 at the floor)
- pages 130 / modules 32 / lines 246; consensus (all) 0.29 of 1956 gold pages with the region; derivable 0.92 (21 lines with no WT source)
- by template: Standard 29m/115p c=0.31; Inquiry 3m/15p c=0.25
- by subject: Leaving to Learn 11m/32p c=0.47; 1-10 English 9m/30p c=0.58; ConnectED 4m/17p c=0.45; None 3m/22p c=0.56; 1-10 Mathematics 3m/22p c=0.15; NCEA1 1m/1p c=0.20
- by era: Refresh 32m/130p c=0.29
- authority (§1b): 4/none — no KB rule, no group consensus ≥ 0.60 at the floor
- **AGH1009** AGH1009_7_0.html ↔ AGH1009.07.html (content, derivable=True)
  - gold: `ul  «identify and describe ways farmers have adopted sustainable practices to the impact of agricultural and horticultural pr»`
  - Claude: `—`
  - WT: `• *Explain how* ***Māori values of kaitiakitanga and manaakitanga*** *are integral to* ***sustainable practices*** *within agricultural and horticultural production within Aotearoa.*`
- **BLL240** BLL240_1_2.html ↔ BLL240-2.0.html (content, derivable=True)
  - gold: `ul  «the sounds and how to read, spell and write words that use the letter patterns wh, tch, dge, air, ear, ere and eer.»`
  - Claude: `—`
  - WT: `• *the sounds and how to read, spell and write words that use the letter patterns wh, tch,* *dge**, air, ear, ere and eer.*`
- **CEDK501** CEDK501_3_1.html ↔ CEDK501_3.1.html (content, derivable=True)
  - gold: `ul  «to recognise when financial goals are realistic and achievable»`
  - Claude: `—`
  - WT: `• how to check and refine a SMART goal so it is clear, realistic, and achievable.`
- modules: AGH1009, BLL240, CEDK501, CEDR501, CEDT501, CEDW501, ENGC102, ENGC201, ENGI301, ENGI405, ENGJ302, ENGR102, ENGR202, ENGS101, ENGS302, HPRE203, MXDI202, MXEO202, MXFL104, TEDC401, TEDC402, XDLS501, XDLS502, XDLS909 …

### #34 · module-menu · MISSING · `div.col-md-8.col-12` › gold `h5` vs Claude `—` — BELOW CONSENSUS (no group ≥ 0.60 at the floor)
- pages 120 / modules 25 / lines 217; consensus (all) 0.22 of 1956 gold pages with the region; derivable 0.72 (60 lines with no WT source)
- by template: Standard 22m/107p c=0.24; Inquiry 3m/13p c=0.19
- by subject: 1-10 English 10m/51p c=0.50; ConnectED 4m/17p c=0.45; Leaving to Learn 4m/9p c=0.14; None 3m/22p c=0.56; 1-10 Mathematics 2m/14p c=0.12; NCEA1 1m/1p c=0.18
- by era: Refresh 25m/120p c=0.22
- authority (§1b): 4/none — no KB rule, no group consensus ≥ 0.60 at the floor
- **AGH1004** AGH1004_2_0.html ↔ AGH1004.06.html (content, derivable=True)
  - gold: `h5  «We are learning to:»`
  - Claude: `—`
  - WT: `We are learning to ...`
- **BLL240** BLL240_1_2.html ↔ BLL240-2.0.html (content, derivable=True)
  - gold: `h5  «We are learning:»`
  - Claude: `—`
  - WT: `*We are learning:*`
- **CEDK501** CEDK501_3_1.html ↔ CEDK501_3.1.html (content, derivable=True)
  - gold: `h5  «Learning intentions»`
  - Claude: `—`
- modules: AGH1004, BLL240, CEDK501, CEDR501, CEDT501, CEDW501, ENGC102, ENGC201, ENGC202, ENGJ302, ENGJ402, ENGJ403, ENGR102, ENGR202, ENGS101, ENGS302, HPRE203, MXDI202, MXFL104, TEDC401, TEDC402, XDLS502, XDLS909, XLP03 …

### #35 · module-menu · EXTRA · `div#header` › gold `—` vs Claude `div#module-menu-content.moduleMenu` — BELOW CONSENSUS (no group ≥ 0.60 at the floor)
- pages 39 / modules 25 / lines 39; consensus (all) 0.25 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 20m/34p c=0.24; Bilingual 3m/3p c=0.79; Inquiry 2m/2p c=0.17
- by subject: ConnectED 6m/15p c=0.24; NCEA1 5m/7p c=0.29; 1-10 Mathematics 5m/8p c=0.24; 1-10 English 4m/4p c=0.04; Te Marautanga o Aotearoa TMoA 3m/3p c=0.79; 1-10 Blended Literacy 1m/1p c=0.62
- by era: Refresh 25m/39p c=0.25
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:45 — | Menu content class | `class="bg row"` | `class="moduleMenu"` |
  - KB: 06_TEMPLATE_RECOGNITION.md:94 — **Header:** `#module-code` → `<h1>` (module code or lesson number), then `<h1><span>Title</span></h1>`, then `#module-head-buttons` → `#module-menu-bu
  - KB: 10_CORPUS_VALIDATED_SCAFFOLDING.md:23 — - **Lesson pages → `simplified`** is dominant by a wide margin (plain `<h5>` label menu inside `#module-menu-content`). A minority of series ship **no
- **ART1005** ART1005_0_0.html ↔ ART1005_3.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div#module-menu-content.moduleMenu`
- **BLL240** BLL240_1_1.html ↔ BLL240-1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div#module-menu-content.moduleMenu`
- **CEDK501** CEDK501_6_0.html ↔ CEDK501_4.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div#module-menu-content.moduleMenu`
- modules: ART1005, BLL240, CEDK501, CEDO501, CEDO502, CEDR501, CEDT501, CEDW501, ENG1004, ENGC302, ENGI401, ENGI405, ENGS201, MXEO201, MXEO301, MXEX301, MXFL104, MXFU201, PES1002, PES1004, PES1008, TRR107, TRR112, TRR113 …

### #36 · module-menu · EXTRA · `div.col-md-8.col-12` › gold `—` vs Claude `h5` — CANDIDATE
- pages 62 / modules 24 / lines 91; consensus (all) 0.78 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 22m/59p c=0.76; Fundamentals 1m/1p c=1.00; Inquiry 1m/2p c=0.81
- by subject: 1-10 English 7m/14p c=0.50; Leaving to Learn 7m/15p c=0.86; Online Safety (OS9000) 3m/6p c=0.41; NCEA1 1m/3p c=0.82; ANZH 1m/2p c=1.00; ConnectED 1m/1p c=0.55
- by era: Refresh 24m/62p c=0.78
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1009** AGH1009_6_0.html ↔ AGH1009.06.1.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «You will show your understanding by:»`
- **ANZH301** ANZH301_1_0.html ↔ ANZH301_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «You will show your understanding by:»`
- **CEDO501** CEDO501_1_0.html ↔ CEDO501_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «We are learning:»`
- modules: AGH1009, ANZH301, CEDO501, ENFUN07, ENGC201, ENGC202, ENGI102, ENGI301, ENGS302, ENGS405, MXEO102, OSAI301, OSBY301, OSSM401, SCCH301, SCPH301, SSCI205, XDLS901, XDLS908, XLP01, XLP02, XLP03, XLP04, XMES102

### #37 · module-menu · EXTRA · `div.col-md-8.col-12` › gold `—` vs Claude `p` — CANDIDATE
- pages 57 / modules 24 / lines 71; consensus (all) 0.87 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 23m/55p c=0.87; Inquiry 1m/2p c=0.83
- by subject: Leaving to Learn 9m/20p c=0.64; NCEA1 5m/14p c=0.92; Online Safety (OS9000) 5m/12p c=0.81; 1-10 English 2m/2p c=0.82; 1-10 Mathematics 2m/7p c=0.93; ANZH 1m/2p c=1.00
- by era: Refresh 24m/57p c=0.87
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1003** AGH1003_3_0.html ↔ AGH1003_03.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «I can justify the use of key management practices due to the positive impact that they have on soil properties and plant»`
- **ANZH301** ANZH301_1_0.html ↔ ANZH301_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «In this lesson we are learning about the push and pull factors/reasons why more Māori moved to the cities before, during»`
- **ENGC201** ENGC201_3_0.html ↔ ENGC201_3.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «se open and closed questions in communication»`
- modules: AGH1003, ANZH301, ENGC201, ENGS405, HIS1005, HIS1006, MXDI201, MXEO202, OSAI101, OSBY301, OSGM201, OSOH101, OSSM401, PES1002, PES1005, XDLS903, XDLS904, XDLS905, XDLS906, XDLS908, XLP01, XLP02, XLP03, XLP04

### #38 · module-menu · EXTRA · `div.col-md-6.col-12.paddingR` › gold `—` vs Claude `p>b` — CANDIDATE
- pages 22 / modules 22 / lines 43; consensus (all) 1.00 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
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

### #39 · module-menu · MISSING · `div.col-md-6.col-12.paddingR` › gold `ul` vs Claude `—` — BELOW CONSENSUS (no group ≥ 0.60 at the floor)
- pages 29 / modules 21 / lines 43; consensus (all) 0.05 of 1956 gold pages with the region; derivable 0.77 (10 lines with no WT source)
- by template: Standard 11m/19p c=0.05; Inquiry 10m/10p c=0.21
- by subject: 1-10 Blended Literacy 8m/8p c=0.29; EXPlore 5m/5p c=0.00; Te ara Whakapuawa -Wellbeing 4m/4p c=0.88; 1-10 Mathematics 2m/10p c=0.04; ANZH 1m/1p c=0.00; ConnectED 1m/1p c=0.03
- by era: Refresh 21m/29p c=0.05
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:158 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **ANZH104** ANZH104_0_0.html ↔ ANZH104_00.0.html (content, derivable=True)
  - gold: `ul  «Generate questions that reflect my curiosity about people and communities and that can’t be answered by a simple yes or »`
  - Claude: `—`
  - WT: `• *G**enerate questions that reflect my curiosity about people and communities and that can’t be answered by a simple yes or no.*`
- **BLL111** BLL111_0_0.html ↔ BLL111-01.html (content, derivable=False)
  - gold: `ul  «Ākonga can use their basic literacy capability and can read fluently and accurately. They engage with a variety of writt»`
  - Claude: `—`
- **BLL112** BLL112_0_0.html ↔ BLL112-01.html (content, derivable=False)
  - gold: `ul  «Ākonga can use their basic literacy capability and can read fluently and accurately. They engage with a variety of writt»`
  - Claude: `—`
- modules: ANZH104, BLL111, BLL112, BLL113, BLL116, BLL120, BLL124, BLL153, BLL154, CEDK501, EXBP901, EXPFUN02, EXPFUN03, EXPFUN04, EXPFUN05, MXFL201, MXFL202, TWHA901, TWHA902, TWHA903, TWHA904

### #40 · module-menu · MOVED · `ul` › gold `li` vs Claude `li>i` — BELOW CONSENSUS (no group ≥ 0.60 at the floor)
- pages 64 / modules 20 / lines 285; consensus (all) 0.37 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 15m/58p c=0.37; Inquiry 4m/5p c=0.68; Fundamentals 1m/1p c=0.42
- by subject: Leaving to Learn 5m/17p c=0.39; None 3m/16p c=0.74; ConnectED 2m/3p c=0.60; EXPlore 2m/2p c=0.60; Online Safety (OS9000) 2m/9p c=0.01; NCEA1 2m/10p c=0.24
- by era: Refresh 20m/64p c=0.37
- authority (§1b): 4/none — no KB rule, no group consensus ≥ 0.60 at the floor
- **ANZH104** ANZH104_0_0.html ↔ ANZH104_00.0.html (structure, derivable=True)
  - gold: `li  «Generate questions that reflect my curiosity about people and communities and that can’t be answered by a simple yes or »`
  - Claude: `li  «Generate questions that reflect my curiosity about people and communities and that can’t be answered by a simple yes or »`
- **BLL124** BLL124_0_0.html ↔ BLL124-01.html (structure, derivable=True)
  - gold: `li  «blend letters to make words.»`
  - Claude: `li  «Blend letters to make words.»`
- **BLLR201** BLLR201_4_0.html ↔ BLLR201_3_0.html (structure, derivable=True)
  - gold: `li  «to use what we already know»`
  - Claude: `li  «to use what we already know»`
- modules: ANZH104, BLL124, BLLR201, CEDT207, CEDT501, ENFUN01, EXPFUN02, EXPFUN03, MXEX101, OSSC401, OSSC501, PES1002, PES1004, TEDC401, TEDC402, XDLS902, XDLS903, XDLS904, XLP01, XLP04

### #46 · module-menu · EXTRA · `div.col-md-6.offset-md-0.col-12` › gold `—` vs Claude `p` — CANDIDATE
- pages 24 / modules 18 / lines 60; consensus (all) 0.99 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 18m/24p c=0.99
- by subject: 1-10 English 15m/16p c=0.93; 1-10 Social Science 2m/2p c=1.00; 1-10 Mathematics 1m/6p c=1.00
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

### #50 · module-menu · MISSING · `div#header` › gold `div#module-head-buttons` vs Claude `—` — CANDIDATE
- pages 49 / modules 17 / lines 49; consensus (all) 0.76 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 11m/36p c=0.77; Bilingual 4m/10p c=0.38; Inquiry 2m/3p c=0.83
- by subject: Te Marautanga o Aotearoa TMoA 4m/10p c=0.38; 1-10 Blended Literacy 3m/6p c=0.40; ConnectED 2m/3p c=0.76; Online Safety (OS9000) 2m/9p c=1.00; Leaving to Learn 2m/11p c=0.88; None 1m/6p c=1.00
- by era: Refresh 17m/49p c=0.76
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
- modules: BLL114, BLL116, BLL153, BLLR201, CEDT207, CEDT301, EXPFUN07, HES1006, MXFL401, OSSC401, OSSC501, PNR101, PNR102, PNR104, TRR109, XGF9002, XLP06

### #51 · module-menu · EXTRA · `div.col-md-6.col-12.paddingR` › gold `—` vs Claude `p` — CANDIDATE
- pages 17 / modules 17 / lines 40; consensus (all) 0.94 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 14m/14p c=0.95; Inquiry 3m/3p c=0.75
- by subject: 1-10 Blended Literacy 8m/8p c=0.70; ConnectED 3m/3p c=0.89; 1-10 English 3m/3p c=0.99; ANZH 1m/1p c=0.96; 1-10 Mathematics 1m/1p c=0.95; Leaving to Learn 1m/1p c=1.00
- by era: Refresh 17m/17p c=0.94
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

### #52 · module-menu · SUBSTITUTED · `ul` › gold `li` vs Claude `li` — CANDIDATE
- pages 63 / modules 16 / lines 241; consensus (all) 0.59 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 16m/63p c=0.60
- by subject: 1-10 Mathematics 9m/28p c=0.54; 1-10 English 3m/20p c=0.88; NCEA1 1m/1p c=0.49; 1-10 Science 1m/7p c=0.80; None 1m/6p c=0.78; Leaving to Learn 1m/1p c=0.72
- by era: Refresh 16m/63p c=0.59
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
- modules: ENGC201, ENGC202, ENGI103, MXDB301, MXDB302, MXEX301, MXFL101, MXFL102, MXFL201, MXFL202, MXFU301, MXFU402, PES1004, SCCH301, SCPH301, XWHA02

### #53 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `div.col-md-12.col-12.paddingR` — CANDIDATE
- pages 18 / modules 16 / lines 18; consensus (all) 0.95 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 16m/18p c=0.96
- by subject: 1-10 Blended Literacy 13m/13p c=0.76; EXPlore 2m/4p c=1.00; None 1m/1p c=1.00
- by era: Refresh 16m/18p c=0.95
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:158 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **BLL112** BLL112_0_0.html ↔ BLL112-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-12.col-12.paddingR  «Overview»`
- **BLL113** BLL113_0_0.html ↔ BLL113-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-12.col-12.paddingR  «Overview»`
- **BLL125** BLL125_0_0.html ↔ BLL125-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-12.col-12.paddingR  «Overview»`
- modules: BLL112, BLL113, BLL125, BLL141, BLL142, BLL143, BLL144, BLL162, BLL163, BLL166, BLL236, BLL237, BLL251, BLLR201, EXBP901, EXIP901

### #54 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `div.col-md-8.col-12` — CANDIDATE
- pages 97 / modules 15 / lines 97; consensus (all) 0.68 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 15m/97p c=0.66
- by subject: 1-10 Mathematics 12m/81p c=0.77; 1-10 English 2m/11p c=0.42; ConnectED 1m/5p c=0.53
- by era: Refresh 15m/97p c=0.68
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **CEDO105** CEDO105_1_0.html ↔ CEDO105.1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-8.col-12`
- **ENGI102** ENGI102_2_0.html ↔ ENGI102_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-8.col-12  «We are learning:»`
- **ENGI103** ENGI103_1_0.html ↔ ENGI103_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-8.col-12  «We are learning:»`
- modules: CEDO105, ENGI102, ENGI103, MXDB301, MXDB302, MXDI301, MXEX101, MXEX301, MXEX302, MXFL204, MXFU201, MXFU202, MXFU301, MXFU302, MXFU402

### #55 · module-menu · EXTRA · `div.col-md-8.col-12` › gold `—` vs Claude `ul` — CANDIDATE
- pages 37 / modules 15 / lines 70; consensus (all) 0.71 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 14m/36p c=0.69; Fundamentals 1m/1p c=1.00
- by subject: 1-10 English 5m/16p c=0.42; Leaving to Learn 4m/8p c=0.53; NCEA1 1m/1p c=0.80; ANZH 1m/2p c=1.00; ConnectED 1m/1p c=0.55; 1-10 Mathematics 1m/4p c=0.85
- by era: Refresh 15m/37p c=0.71
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1009** AGH1009_7_0.html ↔ AGH1009.07.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul  «identifying and describing sustainable practices to the impact of agricultural and horticultural production on water qua»`
- **ANZH301** ANZH301_1_0.html ↔ ANZH301_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul  «using multiple sources of information to help you answer the question: What were some of the reasons why Māori migrated »`
- **CEDO501** CEDO501_1_0.html ↔ CEDO501_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul  «to identify what people do at different life stages and how their experiences or priorities might differ.»`
- modules: AGH1009, ANZH301, CEDO501, ENFUN07, ENGC201, ENGC202, ENGI102, ENGS405, MXEO102, OSSM401, SSCI205, XLP01, XLP02, XLP03, XLP04

### #57 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `div.col-md-6.offset-md-0.col-12` — CANDIDATE
- pages 30 / modules 14 / lines 30; consensus (all) 0.95 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 12m/28p c=0.95; Fundamentals 2m/2p c=0.91
- by subject: 1-10 English 11m/27p c=0.89; 1-10 Mathematics 2m/2p c=0.94; 1-10 Social Science 1m/1p c=0.68
- by era: Refresh 14m/30p c=0.95
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:158 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **ENGC101** ENGC101_0_0.html ↔ ENGC101_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-6.offset-md-0.col-12  «In this module, we delve into the diverse tools and techniques we use to communicate effectively in various contexts. Fr»`
- **ENGC102** ENGC102_0_0.html ↔ ENGC102_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-6.offset-md-0.col-12  «Learning Intentions»`
- **ENGC201** ENGC201_0_0.html ↔ ENGC201_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-6.offset-md-0.col-12  «Learning Intentions»`
- modules: ENGC101, ENGC102, ENGC201, ENGI103, ENGI201, ENGI202, ENGI203, ENGI400, ENGJ102, ENGS202, ENGS301, MXFUN02, MXFUN03, SSOG101

### #58 · module-menu · SUBSTITUTED · `div.col-md-6.col-12.paddingR` › gold `ul` vs Claude `p>b` — CANDIDATE
- pages 14 / modules 14 / lines 14; consensus (all) 0.07 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 12m/12p c=0.05; Inquiry 2m/2p c=0.34
- by subject: 1-10 Blended Literacy 14m/14p c=0.30
- by era: Refresh 14m/14p c=0.07
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

### #62 · module-menu · EXTRA · `div.col-md-6.col-12.paddingR` › gold `—` vs Claude `h5` — CANDIDATE
- pages 14 / modules 12 / lines 27; consensus (all) 0.99 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
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

### #68 · module-menu · EXTRA · `li>b` › gold `—` vs Claude `b` — CANDIDATE
- pages 23 / modules 10 / lines 43; consensus (all) 0.99 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 10m/23p c=0.99
- by subject: NCEA1 3m/10p c=0.99; ConnectED 3m/8p c=0.98; 1-10 English 2m/3p c=1.00; ANZH 1m/1p c=1.00; Leaving to Learn 1m/1p c=0.99
- by era: Refresh 10m/23p c=0.99
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
- modules: AGH1004, AGH1005, AGH1006, ANZH301, CEDO501, CEDO502, CEDT501, ENGC401, ENGS302, XLP01

### #396 · footer · MISSING · `ul.footer-nav` › gold `li>a#next-lesson` vs Claude `—` — CANDIDATE
- pages 94 / modules 57 / lines 94; consensus (all) 0.72 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 54m/91p c=0.75; Inquiry 2m/2p c=0.41; Fundamentals 1m/1p c=0.27
- by subject: Leaving to Learn 19m/20p c=0.65; 1-10 Mathematics 11m/23p c=0.88; Online Safety (OS9000) 9m/9p c=0.80; 1-10 English 7m/7p c=0.86; 1-10 Blended Literacy 4m/4p c=0.13; NCEA1 4m/11p c=0.87
- by era: Refresh 57m/94p c=0.72
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
- modules: ANZH401, ANZH404, BLL174, BLL175, BLL176, BLL177, CEDO301, ENGJ101, ENGJ102, ENGJ201, ENGJ301, ENGJ302, ENGJ402, ENGJ403, HIS1001, HIS1003, HIS1004, HIS1007, MXDB302, MXDI102, MXDI103, MXDI301, MXEX202, MXFL101 …

### #397 · footer · MISSING · `ul.footer-nav` › gold `li>a.home-nav` vs Claude `—` — CANDIDATE
- pages 87 / modules 49 / lines 87; consensus (all) 0.85 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 38m/76p c=0.86; Bilingual 9m/9p c=0.97; Inquiry 1m/1p c=0.59; Fundamentals 1m/1p c=0.58
- by subject: 1-10 English 12m/21p c=1.00; Te Marautanga o Aotearoa TMoA 9m/9p c=0.97; 1-10 Mathematics 8m/34p c=0.98; NCEA1 6m/6p c=1.00; ANZH 3m/3p c=1.00; Online Safety (OS9000) 3m/6p c=1.00
- by era: Refresh 49m/87p c=0.85
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:40 — | Footer tag | `<nav id="module-foot">` with `<button>` + FA icons | `<div id="footer">` with `<ul class="footer-nav">` |
  - KB: 06_TEMPLATE_RECOGNITION.md:64 — | Footer `<ul>` class | `footer-nav` | `footer-nav` | `footer-nav fundamentals-nav` | `footer-nav inquiry-nav` | `footer-nav` |
  - KB: 06_TEMPLATE_RECOGNITION.md:114 — **Footer:** `<ul class="footer-nav">` with prev + next + home links.
- **AGH1004** AGH1004_6_0.html ↔ AGH1004.07.html (structure, derivable=True)
  - gold: `li`
  - Claude: `—`
- **AGH1009** AGH1009_9_0.html ↔ AGH1009.09.html (structure, derivable=True)
  - gold: `li`
  - Claude: `—`
- **ANZH205** ANZH205_6_0.html ↔ ANZH205_06.0.html (structure, derivable=True)
  - gold: `li`
  - Claude: `—`
- modules: AGH1004, AGH1009, ANZH205, ANZH301, ANZH303, BLL236, BLL237, CEDO501, CEDT207, ENGI101, ENGI400, ENGI401, ENGJ101, ENGJ102, ENGJ201, ENGJ301, ENGJ302, ENGJ402, ENGJ403, ENGR102, ENGS302, HES1005, HIS1003, HIS1004 …

### #398 · footer · MISSING · `li>a#next-lesson` › gold `a#next-lesson` vs Claude `—` — CANDIDATE
- pages 45 / modules 45 / lines 45; consensus (all) 0.82 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 35m/35p c=0.84; Bilingual 9m/9p c=0.86; Inquiry 1m/1p c=0.76
- by subject: 1-10 Blended Literacy 12m/12p c=0.74; Te Marautanga o Aotearoa TMoA 9m/9p c=0.86; NCEA1 5m/5p c=0.87; 1-10 English 5m/5p c=0.86; ANZH 4m/4p c=0.91; ConnectED 2m/2p c=0.94
- by era: Refresh 45m/45p c=0.82
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:391 — <li><a href="" id="next-lesson" target="_self"></a></li>
  - KB: 18_ASSESSMENT_MODE.md:158 — <!-- <li><a href="" id="next-lesson" target="_self"></a></li> -->
  - KB: 18_ASSESSMENT_MODE.md:174 — Everything else in the skeleton is **verbatim**: the `{{orgUnitId}}` token, the `&amp;` entities, the commented-out `next-lesson` line, `level=""` (st
- **AGH1004** AGH1004_6_0.html ↔ AGH1004.07.html (structure, derivable=True)
  - gold: `a#next-lesson`
  - Claude: `—`
- **AGH1009** AGH1009_9_0.html ↔ AGH1009.09.html (structure, derivable=True)
  - gold: `a#next-lesson`
  - Claude: `—`
- **ANZH105** ANZH105_5_0.html ↔ ANZH105_05.0.html (structure, derivable=True)
  - gold: `a#next-lesson`
  - Claude: `—`
- modules: AGH1004, AGH1009, ANZH105, ANZH205, ANZH301, ANZH303, BLL141, BLL146, BLL151, BLL157, BLL167, BLL171, BLL224, BLL225, BLL226, BLL234, BLL236, BLL237, BLLR201, CEDO501, CEDT207, ENGI101, ENGI400, ENGI401 …

### #399 · footer · MISSING · `ul.footer-nav.inquiry-nav` › gold `li>a.home-nav` vs Claude `—` — CANDIDATE
- pages 44 / modules 38 / lines 44; consensus (all) 0.14 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 24m/30p c=0.13; Inquiry 14m/14p c=0.41
- by subject: 1-10 Blended Literacy 28m/34p c=0.84; ConnectED 5m/5p c=0.13; Te ara Whakapuawa -Wellbeing 3m/3p c=1.00; None 1m/1p c=0.15; EXPlore 1m/1p c=0.47
- by era: Refresh 38m/44p c=0.14
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:40 — | Footer tag | `<nav id="module-foot">` with `<button>` + FA icons | `<div id="footer">` with `<ul class="footer-nav">` |
  - KB: 06_TEMPLATE_RECOGNITION.md:64 — | Footer `<ul>` class | `footer-nav` | `footer-nav` | `footer-nav fundamentals-nav` | `footer-nav inquiry-nav` | `footer-nav` |
  - KB: 06_TEMPLATE_RECOGNITION.md:114 — **Footer:** `<ul class="footer-nav">` with prev + next + home links.
- **BLL141** BLL141_2_0.html ↔ BLL141-2.0.html (structure, derivable=True)
  - gold: `li`
  - Claude: `—`
- **BLL146** BLL146_2_0.html ↔ BLL146-2.0.html (structure, derivable=True)
  - gold: `li`
  - Claude: `—`
- **BLL151** BLL151_2_0.html ↔ BLL151-2.0.html (structure, derivable=True)
  - gold: `li`
  - Claude: `—`
- modules: BLL141, BLL146, BLL151, BLL154, BLL156, BLL157, BLL166, BLL167, BLL170, BLL171, BLL210, BLL211, BLL213, BLL215, BLL216, BLL217, BLL220, BLL221, BLL222, BLL223, BLL224, BLL225, BLL226, BLL227 …

### #402 · footer · SUBSTITUTED · `div#footer` › gold `ul.footer-nav` vs Claude `ul.footer-nav.inquiry-nav` — CANDIDATE
- pages 64 / modules 18 / lines 64; consensus (all) 0.84 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 12m/42p c=0.86; Inquiry 4m/20p c=0.54; Fundamentals 2m/2p c=0.58
- by subject: 1-10 Blended Literacy 12m/41p c=0.16; ConnectED 4m/21p c=0.87; 1-10 Mathematics 2m/2p c=0.98
- by era: Refresh 18m/64p c=0.84
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:40 — | Footer tag | `<nav id="module-foot">` with `<button>` + FA icons | `<div id="footer">` with `<ul class="footer-nav">` |
  - KB: 06_TEMPLATE_RECOGNITION.md:55 — Once confirmed as Refresh, determine which sub-type the reference files represent. This drives structural decisions about navigation, footer classes, 
  - KB: 06_TEMPLATE_RECOGNITION.md:64 — | Footer `<ul>` class | `footer-nav` | `footer-nav` | `footer-nav fundamentals-nav` | `footer-nav inquiry-nav` | `footer-nav` |
- **BLL121** BLL121_0_0.html ↔ BLL121-01.html (structure, derivable=True)
  - gold: `ul.footer-nav`
  - Claude: `ul.footer-nav.inquiry-nav`
- **BLL172** BLL172_0_0.html ↔ BLL172-00.html (structure, derivable=True)
  - gold: `ul.footer-nav`
  - Claude: `ul.footer-nav.inquiry-nav`
- **BLL174** BLL174_0_0.html ↔ BLL174-00.html (structure, derivable=True)
  - gold: `ul.footer-nav`
  - Claude: `ul.footer-nav.inquiry-nav`
- modules: BLL121, BLL172, BLL174, BLL175, BLL176, BLL177, BLL236, BLL237, BLL240, BLL241, BLL244, BLL245, CEDR501, CEDT207, CEDT301, CEDW101, MXFUN02, MXFUN03

### #403 · footer · MISSING · `ul.footer-nav` › gold `li>a#prev-lesson` vs Claude `—` — CANDIDATE
- pages 38 / modules 18 / lines 38; consensus (all) 0.71 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 15m/35p c=0.74; Bilingual 2m/2p c=0.75; Fundamentals 1m/1p c=0.25
- by subject: 1-10 English 5m/21p c=0.84; 1-10 Mathematics 4m/8p c=0.85; NCEA1 3m/3p c=0.86; Te Marautanga o Aotearoa TMoA 2m/2p c=0.75; Leaving to Learn 2m/2p c=0.80; Online Safety (OS9000) 1m/1p c=0.79
- by era: Refresh 18m/38p c=0.71
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:40 — | Footer tag | `<nav id="module-foot">` with `<button>` + FA icons | `<div id="footer">` with `<ul class="footer-nav">` |
  - KB: 06_TEMPLATE_RECOGNITION.md:64 — | Footer `<ul>` class | `footer-nav` | `footer-nav` | `footer-nav fundamentals-nav` | `footer-nav inquiry-nav` | `footer-nav` |
  - KB: 06_TEMPLATE_RECOGNITION.md:114 — **Footer:** `<ul class="footer-nav">` with prev + next + home links.
- **ART1005** ART1005_0_0.html ↔ ART1005_3.0.html (structure, derivable=True)
  - gold: `li`
  - Claude: `—`
- **ENG1004** ENG1004_0_0.html ↔ ENG1004_0.1.html (structure, derivable=True)
  - gold: `li`
  - Claude: `—`
- **ENGJ101** ENGJ101_4_0.html ↔ ENGJ101_4.0.html (structure, derivable=True)
  - gold: `li`
  - Claude: `—`
- modules: ART1005, ENG1004, ENGJ101, ENGJ301, ENGJ302, ENGJ402, ENGJ403, MXFU201, MXFU202, MXFU301, MXFU302, OSBY501, PES1002, SSFUN02, TRR112, TRR113, XGF9001, XLP06

### #404 · footer · EXTRA · `ul.footer-nav.inquiry-nav` › gold `—` vs Claude `li>a.home-nav` — CANDIDATE
- pages 17 / modules 17 / lines 17; consensus (all) 0.86 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Inquiry 15m/15p c=0.59; Standard 2m/2p c=0.87
- by subject: 1-10 Blended Literacy 7m/7p c=0.16; ConnectED 6m/6p c=0.87; Te ara Whakapuawa -Wellbeing 3m/3p c=0.00; EXPlore 1m/1p c=0.53
- by era: Refresh 17m/17p c=0.86
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:40 — | Footer tag | `<nav id="module-foot">` with `<button>` + FA icons | `<div id="footer">` with `<ul class="footer-nav">` |
  - KB: 06_TEMPLATE_RECOGNITION.md:64 — | Footer `<ul>` class | `footer-nav` | `footer-nav` | `footer-nav fundamentals-nav` | `footer-nav inquiry-nav` | `footer-nav` |
  - KB: 06_TEMPLATE_RECOGNITION.md:114 — **Footer:** `<ul class="footer-nav">` with prev + next + home links.
- **BLL114** BLL114_0_0.html ↔ BLL114-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `li`
- **BLL116** BLL116_0_0.html ↔ BLL116-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `li`
- **BLL170** BLL170_0_0.html ↔ BLL170.html (structure, derivable=True)
  - gold: `—`
  - Claude: `li`
- modules: BLL114, BLL116, BLL170, BLL210, BLL220, BLL230, BLL240, CEDK101, CEDO202, CEDR204, CEDT207, CEDT208, CEDW201, EXPFUN06, TWHA901, TWHA902, TWHA904

### #406 · footer · SUBSTITUTED · `ul.footer-nav.inquiry-nav` › gold `li>a#next-lesson` vs Claude `li>a.home-nav` — CANDIDATE
- pages 16 / modules 16 / lines 16; consensus (all) 0.10 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 15m/15p c=0.10; Inquiry 1m/1p c=0.35
- by subject: 1-10 Blended Literacy 15m/15p c=0.61; ConnectED 1m/1p c=0.13
- by era: Refresh 16m/16p c=0.10
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:40 — | Footer tag | `<nav id="module-foot">` with `<button>` + FA icons | `<div id="footer">` with `<ul class="footer-nav">` |
  - KB: 06_TEMPLATE_RECOGNITION.md:64 — | Footer `<ul>` class | `footer-nav` | `footer-nav` | `footer-nav fundamentals-nav` | `footer-nav inquiry-nav` | `footer-nav` |
  - KB: 06_TEMPLATE_RECOGNITION.md:114 — **Footer:** `<ul class="footer-nav">` with prev + next + home links.
- **BLL154** BLL154_0_0.html ↔ BLL154-0.0.html (structure, derivable=True)
  - gold: `li`
  - Claude: `li`
- **BLL156** BLL156_0_0.html ↔ BLL156-0.0.html (structure, derivable=True)
  - gold: `li`
  - Claude: `li`
- **BLL166** BLL166_0_0.html ↔ BLL166-0.0.html (structure, derivable=True)
  - gold: `li`
  - Claude: `li`
- modules: BLL154, BLL156, BLL166, BLL171, BLL211, BLL213, BLL216, BLL217, BLL221, BLL222, BLL224, BLL225, BLL226, BLL227, BLL231, CEDK102

### #407 · footer · SUBSTITUTED · `div#footer` › gold `ul.footer-nav.inquiry-nav` vs Claude `li>a#next-lesson` — CANDIDATE
- pages 15 / modules 15 / lines 15; consensus (all) 0.14 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 15m/15p c=0.13
- by subject: 1-10 Blended Literacy 15m/15p c=0.84
- by era: Refresh 15m/15p c=0.14
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:40 — | Footer tag | `<nav id="module-foot">` with `<button>` + FA icons | `<div id="footer">` with `<ul class="footer-nav">` |
  - KB: 06_TEMPLATE_RECOGNITION.md:55 — Once confirmed as Refresh, determine which sub-type the reference files represent. This drives structural decisions about navigation, footer classes, 
  - KB: 06_TEMPLATE_RECOGNITION.md:64 — | Footer `<ul>` class | `footer-nav` | `footer-nav` | `footer-nav fundamentals-nav` | `footer-nav inquiry-nav` | `footer-nav` |
- **BLL154** BLL154_0_0.html ↔ BLL154-0.0.html (structure, derivable=True)
  - gold: `ul.footer-nav.inquiry-nav`
  - Claude: `li`
- **BLL156** BLL156_0_0.html ↔ BLL156-0.0.html (structure, derivable=True)
  - gold: `ul.footer-nav.inquiry-nav`
  - Claude: `li`
- **BLL166** BLL166_0_0.html ↔ BLL166-0.0.html (structure, derivable=True)
  - gold: `ul.footer-nav.inquiry-nav`
  - Claude: `li`
- modules: BLL154, BLL156, BLL166, BLL171, BLL211, BLL213, BLL216, BLL217, BLL221, BLL222, BLL224, BLL225, BLL226, BLL227, BLL231

### #408 · footer · SUBSTITUTED · `div#footer` › gold `ul.footer-nav` vs Claude `ul.footer-nav` — CANDIDATE
- pages 13 / modules 13 / lines 13; consensus (all) 0.84 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 13m/13p c=0.86
- by subject: 1-10 English 5m/5p c=1.00; 1-10 Mathematics 4m/4p c=0.98; NCEA1 2m/2p c=0.98; ConnectED 1m/1p c=0.87; Leaving to Learn 1m/1p c=0.95
- by era: Refresh 13m/13p c=0.84
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:40 — | Footer tag | `<nav id="module-foot">` with `<button>` + FA icons | `<div id="footer">` with `<ul class="footer-nav">` |
  - KB: 06_TEMPLATE_RECOGNITION.md:55 — Once confirmed as Refresh, determine which sub-type the reference files represent. This drives structural decisions about navigation, footer classes, 
  - KB: 06_TEMPLATE_RECOGNITION.md:64 — | Footer `<ul>` class | `footer-nav` | `footer-nav` | `footer-nav fundamentals-nav` | `footer-nav inquiry-nav` | `footer-nav` |
- **CEDO105** CEDO105_4_0.html ↔ CEDO105.4.0.html (structure, derivable=True)
  - gold: `ul.footer-nav`
  - Claude: `ul.footer-nav`
- **ENGI101** ENGI101_0_0.html ↔ ENGI101_0.0.html (structure, derivable=True)
  - gold: `ul.footer-nav`
  - Claude: `ul.footer-nav`
- **ENGI303** ENGI303_1_0.html ↔ ENGI303_1.0.html (structure, derivable=True)
  - gold: `ul.footer-nav`
  - Claude: `ul.footer-nav`
- modules: CEDO105, ENGI101, ENGI303, ENGJ301, ENGR302, ENGS102, HIS1002, HIS1005, MXDB202, MXEX301, MXFL401, MXFU402, XDLS501

### #409 · footer · MISSING · `div#footer` › gold `ul.footer-nav` vs Claude `—` — CANDIDATE
- pages 12 / modules 12 / lines 12; consensus (all) 0.84 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 11m/11p c=0.86; Fundamentals 1m/1p c=0.58
- by subject: 1-10 English 3m/3p c=1.00; NCEA1 3m/3p c=0.98; 1-10 Mathematics 3m/3p c=0.98; ANZH 2m/2p c=1.00; Online Safety (OS9000) 1m/1p c=1.00
- by era: Refresh 12m/12p c=0.84
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:40 — | Footer tag | `<nav id="module-foot">` with `<button>` + FA icons | `<div id="footer">` with `<ul class="footer-nav">` |
  - KB: 06_TEMPLATE_RECOGNITION.md:55 — Once confirmed as Refresh, determine which sub-type the reference files represent. This drives structural decisions about navigation, footer classes, 
  - KB: 06_TEMPLATE_RECOGNITION.md:64 — | Footer `<ul>` class | `footer-nav` | `footer-nav` | `footer-nav fundamentals-nav` | `footer-nav inquiry-nav` | `footer-nav` |
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html (structure, derivable=True)
  - gold: `ul.footer-nav`
  - Claude: `—`
- **ANZH301** ANZH301_1_0.html ↔ ANZH301_1.0.html (structure, derivable=True)
  - gold: `ul.footer-nav`
  - Claude: `—`
- **ENGJ201** ENGJ201_1_0.html ↔ ENGJ201_1.0.html (structure, derivable=True)
  - gold: `ul.footer-nav`
  - Claude: `—`
- modules: ANZH101, ANZH301, ENGJ201, ENGR302, ENGS202, HES1007, HIS1002, HIS1005, MXDI103, MXEO301, MXFUN01, OSAH501

### #410 · footer · EXTRA · `div#footer` › gold `—` vs Claude `ul.footer-nav.inquiry-nav` — CANDIDATE
- pages 12 / modules 11 / lines 12; consensus (all) 0.86 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 10m/11p c=0.87; Inquiry 1m/1p c=0.59
- by subject: 1-10 Blended Literacy 10m/11p c=0.16; EXPlore 1m/1p c=0.53
- by era: Refresh 11m/12p c=0.86
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:40 — | Footer tag | `<nav id="module-foot">` with `<button>` + FA icons | `<div id="footer">` with `<ul class="footer-nav">` |
  - KB: 06_TEMPLATE_RECOGNITION.md:55 — Once confirmed as Refresh, determine which sub-type the reference files represent. This drives structural decisions about navigation, footer classes, 
  - KB: 06_TEMPLATE_RECOGNITION.md:64 — | Footer `<ul>` class | `footer-nav` | `footer-nav` | `footer-nav fundamentals-nav` | `footer-nav inquiry-nav` | `footer-nav` |
- **BLL115** BLL115_1_0.html ↔ BLL115-02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul.footer-nav.inquiry-nav`
- **BLL122** BLL122_1_0.html ↔ BLL122-02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul.footer-nav.inquiry-nav`
- **BLL130** BLL130_0_0.html ↔ BLL130.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul.footer-nav.inquiry-nav`
- modules: BLL115, BLL122, BLL130, BLL171, BLL212, BLL214, BLL215, BLL216, BLL223, BLL232, EXBP901

### #411 · footer · EXTRA · `ul.footer-nav.fundamentals-nav` › gold `—` vs Claude `li>a.home-nav` — CANDIDATE
- pages 10 / modules 10 / lines 10; consensus (all) 0.99 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Fundamentals 10m/10p c=0.70
- by subject: 1-10 Health and PE 10m/10p c=0.27
- by era: Refresh 10m/10p c=0.99
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:40 — | Footer tag | `<nav id="module-foot">` with `<button>` + FA icons | `<div id="footer">` with `<ul class="footer-nav">` |
  - KB: 06_TEMPLATE_RECOGNITION.md:64 — | Footer `<ul>` class | `footer-nav` | `footer-nav` | `footer-nav fundamentals-nav` | `footer-nav inquiry-nav` | `footer-nav` |
  - KB: 06_TEMPLATE_RECOGNITION.md:114 — **Footer:** `<ul class="footer-nav">` with prev + next + home links.
- **HPFUN101** HPFUN101_0_0.html ↔ HPFUN101.html (structure, derivable=True)
  - gold: `—`
  - Claude: `li`
- **HPFUN103** HPFUN103_0_0.html ↔ HPFUN103.html (structure, derivable=True)
  - gold: `—`
  - Claude: `li`
- **HPFUN201** HPFUN201_0_0.html ↔ HPFUN201.html (structure, derivable=True)
  - gold: `—`
  - Claude: `li`
- modules: HPFUN101, HPFUN103, HPFUN201, HPFUN202, HPFUN301, HPFUN302, HPFUN303, HPFUN401, HPFUN402, HPFUN403

### #412 · footer · SUBSTITUTED · `ul.footer-nav` › gold `li>a#next-lesson` vs Claude `li>a#next-lesson` — CANDIDATE
- pages 10 / modules 10 / lines 10; consensus (all) 0.72 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 10m/10p c=0.75
- by subject: 1-10 Mathematics 4m/4p c=0.88; 1-10 English 3m/3p c=0.86; ConnectED 1m/1p c=0.81; NCEA1 1m/1p c=0.87; Leaving to Learn 1m/1p c=0.65
- by era: Refresh 10m/10p c=0.72
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:40 — | Footer tag | `<nav id="module-foot">` with `<button>` + FA icons | `<div id="footer">` with `<ul class="footer-nav">` |
  - KB: 06_TEMPLATE_RECOGNITION.md:64 — | Footer `<ul>` class | `footer-nav` | `footer-nav` | `footer-nav fundamentals-nav` | `footer-nav inquiry-nav` | `footer-nav` |
  - KB: 06_TEMPLATE_RECOGNITION.md:114 — **Footer:** `<ul class="footer-nav">` with prev + next + home links.
- **CEDO105** CEDO105_4_0.html ↔ CEDO105.4.0.html (structure, derivable=True)
  - gold: `li`
  - Claude: `li`
- **ENGI303** ENGI303_1_0.html ↔ ENGI303_1.0.html (structure, derivable=True)
  - gold: `li`
  - Claude: `li`
- **ENGR302** ENGR302_5_0.html ↔ ENGR302_6.0.html (structure, derivable=True)
  - gold: `li`
  - Claude: `li`
- modules: CEDO105, ENGI303, ENGR302, ENGS102, HIS1002, MXDB202, MXEX301, MXFL401, MXFU402, XDLS501

### #506 · acks · SUBSTITUTED · `div.col-md-8.col-12` › gold `div.acks` vs Claude `div.acks.acksTemplate` — CANDIDATE
- pages 84 / modules 84 / lines 84; consensus (all) 0.17 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Fundamentals 29m/29p c=0.62; Standard 28m/28p c=0.14; Inquiry 27m/27p c=0.47
- by subject: 1-10 Blended Literacy 17m/17p c=0.34; ConnectED 13m/13p c=0.20; 1-10 English 10m/10p c=0.14; Online Safety (OS9000) 8m/8p c=0.12; 1-10 Technology 8m/8p c=1.00; 1-10 Health and PE 6m/6p c=0.80
- by era: Refresh 84m/84p c=0.17
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:164 — - XFUN01 omits language attributes on `<body>`, has home + next (no `fundamentals-nav`), and places acks after footer
  - KB: 06_TEMPLATE_RECOGNITION.md:191 — - XLP05 lacks `learningSupport` despite being a learning support module
  - KB: 10_CORPUS_VALIDATED_SCAFFOLDING.md:5 — **What this file is.** A small set of scaffolding facts measured *directly* from the finished modules in `01-Finalized_Modules_` (388 developed module
- **ANZH401** ANZH401_0_0.html ↔ ANZH401_0.0.html (structure, derivable=True)
  - gold: `div.acks`
  - Claude: `div.acks.acksTemplate`
- **ANZH404** ANZH404_0_0.html ↔ ANZH404_0.0.html (structure, derivable=True)
  - gold: `div.acks`
  - Claude: `div.acks.acksTemplate`
- **ARFUN01** ARFUN01_0_0.html ↔ ARFUN01.html (structure, derivable=True)
  - gold: `div.acks`
  - Claude: `div.acks.acksTemplate`
- modules: ANZH401, ANZH404, ARFUN01, ARFUN03, ARFUN05, BLL110, BLL140, BLL150, BLL160, BLL170, BLL210, BLL220, BLL224, BLL230, BLL236, BLL241, BLL242, BLL244, BLL245, BLL246, BLL251, BLL254, CEDK101, CEDK102 …

### #534 · activity · MISSING · `div.col-12` › gold `p` vs Claude `—` — CANDIDATE
- pages 705 / modules 299 / lines 1561; consensus (all) 0.31 of 1950 gold pages with the region; derivable 0.83 (263 lines with no WT source)
- by template: Standard 229m/613p c=0.28; Fundamentals 36m/42p c=0.69; Inquiry 26m/35p c=0.48; Bilingual 8m/15p c=0.52
- by subject: 1-10 Blended Literacy 74m/116p c=0.54; 1-10 English 44m/108p c=0.19; 1-10 Mathematics 38m/145p c=0.38; NCEA1 33m/113p c=0.18; Leaving to Learn 21m/63p c=0.35; ConnectED 17m/32p c=0.25
- by era: Refresh 299m/705p c=0.31
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1001** AGH1001_1_0.html ↔ AGH1001.01.html (content, derivable=True)
  - gold: `p  «Select the primary products below which you think are produced in New Zealand or Pacific Islands.»`
  - Claude: `—`
  - WT: `This module “From the Ground Up” is an introduction to Agricultural and Horticultural Production in New Zealand. It introduces some key terms and concepts that you will need as you move through future`
- **AGH1002** AGH1002_2_0.html ↔ AGH1002.02.html (content, derivable=True)
  - gold: `p  «Go to your learning journal and complete activity 2C.»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [Go to your learning journal and complete activity 2B} [/RED TEXT]🔴`
- **AGH1003** AGH1003_2_0.html ↔ AGH1003_02.0.html (content, derivable=True)
  - gold: `p  «For each production type, identify the irrigation system which would be best suited.»`
  - Claude: `—`
  - WT: `│ [IMAGE: image25.jpg] ║ **Dripline irrigators** are used on many orchards across New Zealand. They are very precise and apply water directly to the base of the tree or vine, reducing water loss throu`
- modules: AGH1001, AGH1002, AGH1003, AGH1004, AGH1005, AGH1006, AGH1007, AGH1008, AGH1009, ANZH101, ANZH104, ANZH105, ANZH203, ANZH301, ANZH304, ARFUN01, ARFUN02, ARFUN03, ARFUN05, ART1004, ART1006, BLL110, BLL111, BLL112 …

### #535 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `p` — CANDIDATE
- pages 463 / modules 236 / lines 1999; consensus (all) 0.88 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 181m/388p c=0.92; Inquiry 23m/28p c=0.54; Fundamentals 21m/21p c=0.59; Bilingual 11m/26p c=0.56
- by subject: 1-10 Blended Literacy 68m/92p c=0.82; 1-10 Mathematics 31m/86p c=0.89; 1-10 English 30m/58p c=0.96; NCEA1 23m/72p c=0.93; Leaving to Learn 22m/52p c=0.84; ConnectED 14m/16p c=0.85
- by era: Refresh 236m/463p c=0.88
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1002** AGH1002_2_0.html ↔ AGH1002.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Answers»`
- **AGH1003** AGH1003_1_0.html ↔ AGH1003_01.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «5.0–5.5»`
- **AGH1004** AGH1004_1_0.html ↔ AGH1004.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Mountain ranges, Lake Wanaka, hot and dry summers, low rainfall, diurnal, mesoclimate, soil types.»`
- modules: AGH1002, AGH1003, AGH1004, AGH1008, AGH1009, ANZH101, ANZH104, ANZH105, ANZH205, ANZH301, ANZH303, ANZH304, ANZH404, ARFUN03, ARFUN04, ART1005, BLL110, BLL111, BLL113, BLL115, BLL116, BLL117, BLL120, BLL122 …

### #537 · activity · MISSING · `div.col-12` › gold `a` vs Claude `—` — CANDIDATE
- pages 423 / modules 208 / lines 651; consensus (all) 0.29 of 1950 gold pages with the region; derivable 0.65 (225 lines with no WT source)
- by template: Standard 169m/379p c=0.28; Inquiry 24m/29p c=0.54; Fundamentals 12m/12p c=0.33; Bilingual 3m/3p c=0.25
- by subject: 1-10 Blended Literacy 53m/66p c=0.27; 1-10 Mathematics 34m/100p c=0.41; 1-10 English 31m/68p c=0.24; NCEA1 30m/104p c=0.38; ConnectED 18m/25p c=0.40; Leaving to Learn 17m/28p c=0.24
- by era: Refresh 208m/423p c=0.29
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1001** AGH1001_1_0.html ↔ AGH1001.01.html (content, derivable=False)
  - gold: `a  «Download journal»`
  - Claude: `—`
- **AGH1002** AGH1002_2_0.html ↔ AGH1002.02.html (content, derivable=False)
  - gold: `a  «Go to journal»`
  - Claude: `—`
- **AGH1003** AGH1003_3_0.html ↔ AGH1003_03.0.html (content, derivable=False)
  - gold: `a  «Go to journal»`
  - Claude: `—`
- modules: AGH1001, AGH1002, AGH1003, AGH1004, AGH1005, AGH1006, AGH1007, AGH1008, AGH1009, ANZH104, ANZH105, ANZH205, ANZH301, ANZH404, ARFUN01, ART1005, BLL111, BLL112, BLL113, BLL114, BLL115, BLL116, BLL117, BLL120 …

### #538 · activity · MISSING · `a` › gold `div.button` vs Claude `—` — CANDIDATE
- pages 529 / modules 194 / lines 924; consensus (all) 0.23 of 1950 gold pages with the region; derivable 0.63 (339 lines with no WT source)
- by template: Standard 152m/461p c=0.21; Inquiry 17m/28p c=0.44; Fundamentals 13m/13p c=0.28; Bilingual 12m/27p c=0.29
- by subject: NCEA1 39m/139p c=0.38; 1-10 Mathematics 39m/152p c=0.40; 1-10 English 33m/80p c=0.19; ConnectED 13m/34p c=0.24; Leaving to Learn 13m/31p c=0.12; Te Marautanga o Aotearoa TMoA 12m/27p c=0.29
- by era: Refresh 194m/529p c=0.23
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: INDEX.md:84 — - **`05_COMP_LANGUAGE_MEDIA_LAYOUT/05D_COMP14_BUTTONS_TABLES_COLUMNS.md`** (21 KB) — COMP_14 Layout & Structure, second half: Buttons (incl. the "Go t
  - KB: INDEX.md:85 — - Sections: Buttons (MTK Quiz — the activity shell `[MTKquiz]` builds) · Supervisor Button (Shape A/B/C · the reveal panel · edge cases) · Tables · Co
  - KB: _project_instructions_.md:28 — - **`ASSESSMENT MODE`** phrase (any capitalisation), **or** an uploaded `.docx` that is an **NCEA Assessment Activity** document (details table `Activ
- **AGH1001** AGH1001_2_0.html ↔ AGH1001.02.html (content, derivable=False)
  - gold: `div.button  «Go to journal»`
  - Claude: `—`
- **AGH1002** AGH1002_2_0.html ↔ AGH1002.02.html (content, derivable=False)
  - gold: `div.button  «Download journal»`
  - Claude: `—`
- **AGH1003** AGH1003_2_0.html ↔ AGH1003_02.0.html (content, derivable=False)
  - gold: `div.button  «Download journal»`
  - Claude: `—`
- modules: AGH1001, AGH1002, AGH1003, AGH1004, AGH1005, AGH1006, AGH1008, AGH1009, ANZH101, ANZH104, ANZH105, ANZH203, ANZH205, ANZH301, ANZH304, ANZH401, ART1002, ART1004, ART1005, ART1006, BLL240, BLL253, BLL263, CEDK501 …

### #539 · activity · MISSING · `div.col-12` › gold `h3` vs Claude `—` — CANDIDATE
- pages 394 / modules 183 / lines 617; consensus (all) 0.32 of 1950 gold pages with the region; derivable 0.75 (154 lines with no WT source)
- by template: Standard 135m/340p c=0.29; Fundamentals 27m/27p c=0.81; Inquiry 15m/16p c=0.46; Bilingual 6m/11p c=0.60
- by subject: 1-10 English 35m/66p c=0.19; 1-10 Mathematics 35m/124p c=0.45; NCEA1 29m/84p c=0.13; 1-10 Blended Literacy 14m/14p c=0.63; Leaving to Learn 14m/25p c=0.33; ConnectED 10m/14p c=0.21
- by era: Refresh 183m/394p c=0.32
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1001** AGH1001_1_0.html ↔ AGH1001.01.html (content, derivable=True)
  - gold: `h3  «Primary Products»`
  - Claude: `—`
  - WT: `• *Recognise management practices and the role they play in the production of primary products.*`
- **AGH1002** AGH1002_2_0.html ↔ AGH1002.02.html (content, derivable=False)
  - gold: `h3  «A smashed structure experiment»`
  - Claude: `—`
- **AGH1003** AGH1003_1_0.html ↔ AGH1003_01.0.html (content, derivable=True)
  - gold: `h3  «What are soil management practices»`
  - Claude: `—`
  - WT: `•  *Describe how soil management practices are carried out on a range of primary production systems.*`
- modules: AGH1001, AGH1002, AGH1003, AGH1004, AGH1005, AGH1006, AGH1007, AGH1008, AGH1009, ANZH101, ANZH104, ANZH105, ANZH203, ARFUN02, ARFUN03, ARFUN05, ART1006, BLL110, BLL115, BLL117, BLL120, BLL130, BLL137, BLL143 …

### #540 · activity · MOVED · `div.col-12` › gold `p` vs Claude `p` — CANDIDATE
- pages 280 / modules 152 / lines 704; consensus (all) 0.19 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 103m/216p c=0.15; Fundamentals 21m/22p c=0.58; Inquiry 21m/28p c=0.47; Bilingual 7m/14p c=0.48
- by subject: 1-10 Blended Literacy 20m/21p c=0.31; 1-10 English 20m/27p c=0.10; 1-10 Mathematics 19m/60p c=0.19; Leaving to Learn 19m/41p c=0.27; NCEA1 13m/30p c=0.12; ConnectED 11m/28p c=0.21
- by era: Refresh 152m/280p c=0.19
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1003** AGH1003_2_0.html ↔ AGH1003_02.0.html (structure, derivable=True)
  - gold: `p  «From the list below, select the soil properties you think may be altered through adding irrigation. We will revisit thes»`
  - Claude: `p  «From the list below, select the soil properties you think may be altered through adding irrigation. We will revisit thes»`
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html (structure, derivable=True)
  - gold: `p  «Read the paragraph below and then complete the activity to identify the important words.»`
  - Claude: `p  «Read the paragraph below and then complete the activity to identify the important words.»`
- **ANZH203** ANZH203_6_0.html ↔ ANZH203_7.0.html (structure, derivable=True)
  - gold: `p  «Well done! You have completed this module. Now is a good time to share everything you have done with you kaiako by uploa»`
  - Claude: `p  «Well done! You have completed this module. Now is a good time to share everything you have done with you kaiako by uploa»`
- modules: AGH1003, ANZH101, ANZH203, ANZH304, ARFUN02, ARFUN03, ARFUN05, ART1004, ART1005, ART1006, BLL110, BLL120, BLL135, BLL152, BLL153, BLL160, BLL162, BLL170, BLL177, BLL216, BLL217, BLL230, BLL234, BLL240 …

### #541 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `WIDGET` — CANDIDATE
- pages 225 / modules 146 / lines 305; consensus (all) 0.82 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 112m/168p c=0.85; Inquiry 12m/17p c=0.64; Fundamentals 11m/11p c=0.56; Bilingual 11m/29p c=0.78
- by subject: 1-10 Blended Literacy 39m/48p c=0.67; 1-10 English 20m/29p c=0.92; 1-10 Mathematics 20m/32p c=0.72; Leaving to Learn 19m/33p c=0.82; Te Marautanga o Aotearoa TMoA 11m/29p c=0.78; NCEA1 10m/18p c=0.97
- by era: Refresh 146m/225p c=0.82
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1002** AGH1002_3_0.html ↔ AGH1002.03.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **AGH1008** AGH1008_3_0.html ↔ AGH1008.03.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **AGH1009** AGH1009_3_0.html ↔ AGH1009.03.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- modules: AGH1002, AGH1008, AGH1009, ANZH101, ANZH105, ANZH304, ANZH401, ANZH404, ARFUN04, BLL110, BLL111, BLL114, BLL120, BLL127, BLL130, BLL132, BLL133, BLL137, BLL140, BLL141, BLL144, BLL146, BLL150, BLL153 …

### #543 · activity · EXTRA · `div.row` › gold `—` vs Claude `div.col-12` — CANDIDATE
- pages 155 / modules 110 / lines 209; consensus (all) 0.89 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 88m/129p c=0.92; Inquiry 15m/19p c=0.64; Fundamentals 6m/6p c=0.47; Bilingual 1m/1p c=0.94
- by subject: 1-10 Blended Literacy 43m/53p c=0.78; 1-10 Mathematics 17m/24p c=0.85; Leaving to Learn 12m/22p c=0.91; 1-10 English 11m/18p c=0.95; NCEA1 8m/10p c=1.00; ANZH 5m/13p c=0.99
- by era: Refresh 110m/155p c=0.89
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1005** AGH1005_5_0.html ↔ AGH1005.05.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12  «Factors that influence the rate of transpiration are:»`
- **AGH1007** AGH1007_8_0.html ↔ AGH1007.08.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12  «In the space below, brainstorm some advantages of adaptive immunity for both the animal and the farmer.»`
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12  «The activities in this module will be completed in a journal. Please download the file by clicking on the ‘Download Jour»`
- modules: AGH1005, AGH1007, ANZH101, ANZH301, ANZH304, ANZH401, ANZH404, BLL110, BLL113, BLL114, BLL116, BLL117, BLL120, BLL121, BLL123, BLL124, BLL125, BLL126, BLL130, BLL131, BLL134, BLL135, BLL136, BLL137 …

### #544 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `p>a` — CANDIDATE
- pages 119 / modules 100 / lines 213; consensus (all) 0.99 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 82m/99p c=0.99; Inquiry 8m/8p c=0.96; Fundamentals 7m/7p c=1.00; Bilingual 3m/5p c=1.00
- by subject: 1-10 Blended Literacy 33m/37p c=0.99; 1-10 English 14m/19p c=0.99; 1-10 Mathematics 11m/15p c=0.99; NCEA1 9m/9p c=0.98; Leaving to Learn 8m/8p c=0.99; ANZH 6m/8p c=0.99
- by era: Refresh 100m/119p c=0.99
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1008** AGH1008_8_0.html ↔ AGH1008.08.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «https://www.dairynz.co.nz/biosecurity/mycoplasma-bovis/overview-of-mycoplasma-bovis/»`
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Please add images of these things and a label on the image as has been done in the ISTO410 Outdoor Adventures Activity I»`
- **ANZH104** ANZH104_5_0.html ↔ ANZH104_05.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Cartoon»`
- modules: AGH1008, ANZH101, ANZH104, ANZH105, ANZH205, ANZH304, ANZH404, ARFUN03, BLL111, BLL112, BLL114, BLL115, BLL120, BLL122, BLL126, BLL130, BLL131, BLL163, BLL166, BLL171, BLL172, BLL174, BLL175, BLL210 …

### #546 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `img.img-fluid` — CANDIDATE
- pages 138 / modules 92 / lines 403; consensus (all) 0.97 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 61m/92p c=0.98; Inquiry 12m/12p c=0.85; Fundamentals 10m/10p c=0.92; Bilingual 9m/24p c=0.92
- by subject: 1-10 Blended Literacy 23m/26p c=0.95; 1-10 Mathematics 13m/28p c=0.93; NCEA1 9m/13p c=0.99; 1-10 English 9m/10p c=0.99; Te Marautanga o Aotearoa TMoA 9m/24p c=0.92; 1-10 Health and PE 6m/6p c=0.93
- by era: Refresh 92m/138p c=0.97
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1002** AGH1002_3_0.html ↔ AGH1002.03.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- **AGH1008** AGH1008_1_0.html ↔ AGH1008.01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- **ANZH104** ANZH104_4_0.html ↔ ANZH104_04.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- modules: AGH1002, AGH1008, ANZH104, ANZH205, ANZH303, ANZH404, ART1004, BLL110, BLL116, BLL120, BLL130, BLL132, BLL134, BLL137, BLL140, BLL142, BLL145, BLL147, BLL150, BLL160, BLL162, BLL163, BLL170, BLL174 …

### #550 · activity · MOVED · `div.col-12` › gold `h3` vs Claude `h3` — CANDIDATE
- pages 98 / modules 80 / lines 173; consensus (all) 0.23 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 59m/75p c=0.19; Fundamentals 10m/11p c=0.70; Inquiry 9m/9p c=0.44; Bilingual 2m/3p c=0.56
- by subject: 1-10 Blended Literacy 24m/28p c=0.54; 1-10 Mathematics 13m/18p c=0.31; Leaving to Learn 10m/11p c=0.19; ConnectED 6m/7p c=0.17; NCEA1 5m/7p c=0.06; 1-10 Social Science 5m/5p c=0.18
- by era: Refresh 80m/98p c=0.23
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH301** ANZH301_1_0.html ↔ ANZH301_1.0.html (structure, derivable=True)
  - gold: `h3  «Statistics; so, what?»`
  - Claude: `h3  «Statistics; so, what?»`
- **ANZH304** ANZH304_1_0.html ↔ ANZH304_0.1.html (structure, derivable=True)
  - gold: `h3  «Extend your learning»`
  - Claude: `h3  «Extend your learning»`
- **ARFUN02** ARFUN02_0_0.html ↔ ARFUN02.html (structure, derivable=True)
  - gold: `h3  «Motivic Development: Growing Your Musical Ideas»`
  - Claude: `h3  «Motivic Development: Growing Your Musical Ideas»`
- modules: ANZH301, ANZH304, ARFUN02, BLL117, BLL120, BLL122, BLL123, BLL124, BLL125, BLL132, BLL144, BLL145, BLL152, BLL160, BLL161, BLL164, BLL171, BLL213, BLL214, BLL216, BLL220, BLL221, BLL222, BLL224 …

### #551 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `ul` — CANDIDATE
- pages 92 / modules 76 / lines 159; consensus (all) 0.94 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 56m/71p c=0.96; Inquiry 14m/15p c=0.77; Fundamentals 5m/5p c=0.89; Bilingual 1m/1p c=0.59
- by subject: 1-10 Blended Literacy 21m/22p c=0.96; 1-10 English 13m/16p c=0.95; NCEA1 11m/12p c=0.98; Leaving to Learn 11m/16p c=0.90; ConnectED 5m/5p c=0.88; 1-10 Social Science 4m/4p c=0.79
- by era: Refresh 76m/92p c=0.94
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1002** AGH1002_4_0.html ↔ AGH1002.04.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul  «Sand soil»`
- **AGH1003** AGH1003_4_0.html ↔ AGH1003_04.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul  «It is a free fertiliser because it is a waste product. While adding it to the soil may have some cost involved for farme»`
- **AGH1008** AGH1008_1_0.html ↔ AGH1008.01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul  «Manaakitanga is about care and respect toward people, living things and places.»`
- modules: AGH1002, AGH1003, AGH1008, ANZH303, ANZH404, ARFUN04, BLL110, BLL113, BLL114, BLL115, BLL117, BLL122, BLL126, BLL130, BLL131, BLL132, BLL133, BLL135, BLL140, BLL150, BLL160, BLL162, BLL170, BLL171 …

### #552 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `p>b` — CANDIDATE
- pages 108 / modules 75 / lines 352; consensus (all) 0.97 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 52m/75p c=0.98; Inquiry 11m/11p c=0.92; Bilingual 9m/19p c=0.73; Fundamentals 3m/3p c=0.97
- by subject: 1-10 Blended Literacy 18m/20p c=0.97; Leaving to Learn 12m/19p c=0.95; NCEA1 9m/16p c=0.98; Te Marautanga o Aotearoa TMoA 9m/19p c=0.73; 1-10 Mathematics 7m/9p c=1.00; ANZH 4m/7p c=0.99
- by era: Refresh 75m/108p c=0.97
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH301** ANZH301_2_0.html ↔ ANZH301_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «: For example, …»`
- **ANZH303** ANZH303_2_0.html ↔ ANZH303_0.2.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Option 1: Questions to answer.»`
- **ANZH304** ANZH304_5_0.html ↔ ANZH304_0.5.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «‘In what ways did Eruera Patuone influence people (both Māori and Pākehā) over a long period of time?’»`
- modules: ANZH301, ANZH303, ANZH304, ANZH404, ART1004, BLL110, BLL111, BLL113, BLL120, BLL121, BLL130, BLL133, BLL142, BLL150, BLL154, BLL156, BLL157, BLL174, BLL176, BLL212, BLL214, BLL240, BLL262, BLLR201 …

### #553 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `ol` — CANDIDATE
- pages 104 / modules 74 / lines 221; consensus (all) 0.96 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 56m/86p c=0.97; Fundamentals 11m/11p c=0.95; Inquiry 6m/6p c=0.82; Bilingual 1m/1p c=0.97
- by subject: NCEA1 16m/28p c=0.95; 1-10 Mathematics 11m/18p c=0.98; 1-10 English 9m/11p c=0.98; Leaving to Learn 8m/13p c=0.95; 1-10 Health and PE 7m/7p c=1.00; 1-10 Blended Literacy 4m/4p c=0.98
- by era: Refresh 74m/104p c=0.96
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1002** AGH1002_2_0.html ↔ AGH1002.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ol  «Silty Clay Loam»`
- **AGH1003** AGH1003_1_0.html ↔ AGH1003_01.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ol  «Soil is made up of:»`
- **AGH1005** AGH1005_2_0.html ↔ AGH1005.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ol  «Create a new generation of plants»`
- modules: AGH1002, AGH1003, AGH1005, AGH1008, ANZH205, ANZH303, ANZH304, ARFUN04, BLL111, BLL120, BLL142, BLL214, CEDK102, CEDO301, CEDO501, CEDO502, ENGC202, ENGI103, ENGI201, ENGI301, ENGJ302, ENGJ402, ENGR101, ENGR301 …

### #557 · activity · SUBSTITUTED · `div.col-12` › gold `p` vs Claude `p` — CANDIDATE
- pages 92 / modules 70 / lines 198; consensus (all) 0.76 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 49m/65p c=0.75; Bilingual 9m/15p c=0.64; Inquiry 8m/8p c=0.83; Fundamentals 4m/4p c=0.94
- by subject: 1-10 Blended Literacy 14m/15p c=0.67; 1-10 Mathematics 10m/15p c=0.84; Te Marautanga o Aotearoa TMoA 9m/15p c=0.64; NCEA1 8m/11p c=0.78; Leaving to Learn 8m/14p c=0.73; ConnectED 5m/5p c=0.81
- by era: Refresh 70m/92p c=0.76
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1006** AGH1006_5_0.html ↔ AGH1006.06.html (structure, derivable=True)
  - gold: `p  «Drag the benefit of each of the training practices to the corresponding pictures.»`
  - Claude: `p  «Here is a video showing how a hydrangea is pruned.»`
- **ANZH203** ANZH203_6_0.html ↔ ANZH203_7.0.html (structure, derivable=True)
  - gold: `p  «Go to your journal to find the source analysis template to complete for one of the images above.»`
  - Claude: `p  «☐Checked that the hyperlinks work?»`
- **ANZH301** ANZH301_1_0.html ↔ ANZH301_1.0.html (structure, derivable=True)
  - gold: `p  «Download your Learning Journal for this module using the button below.»`
  - Claude: `p  «Look at the statistics in the two tables above and think about what information you could take from them about Māori urb»`
- modules: AGH1006, ANZH203, ANZH301, ART1002, ART1006, BLL130, BLL145, BLL152, BLL177, BLL220, BLL221, BLL222, BLL225, BLL227, BLL230, BLL231, BLL252, BLL253, BLL254, CEDO502, CEDT104, CEDT208, CEDT501, CEDW201 …

### #558 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `h3` — CANDIDATE
- pages 89 / modules 65 / lines 135; consensus (all) 0.86 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 44m/53p c=0.91; Inquiry 9m/14p c=0.57; Bilingual 8m/18p c=0.44; Fundamentals 4m/4p c=0.42
- by subject: 1-10 Blended Literacy 25m/29p c=0.78; Te Marautanga o Aotearoa TMoA 8m/18p c=0.44; Leaving to Learn 8m/13p c=0.88; 1-10 Mathematics 7m/8p c=0.80; 1-10 English 5m/5p c=0.95; ConnectED 3m/4p c=0.86
- by era: Refresh 65m/89p c=0.86
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH304** ANZH304_2_0.html ↔ ANZH304_0.2.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h3  «Some of the why?»`
- **BLL113** BLL113_1_0.html ↔ BLL113-02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h3  «Decoding words»`
- **BLL115** BLL115_1_0.html ↔ BLL115-02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h3  «Alien words»`
- modules: ANZH304, BLL113, BLL115, BLL120, BLL121, BLL131, BLL132, BLL136, BLL137, BLL144, BLL147, BLL150, BLL151, BLL153, BLL156, BLL160, BLL175, BLL177, BLL217, BLL230, BLL234, BLL235, BLL240, BLL251 …

### #560 · activity · EXTRA · `p>a` › gold `—` vs Claude `a` — CANDIDATE
- pages 71 / modules 64 / lines 87; consensus (all) 0.98 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 56m/62p c=0.98; Inquiry 5m/6p c=0.94; Fundamentals 2m/2p c=1.00; Bilingual 1m/1p c=0.98
- by subject: 1-10 Blended Literacy 26m/29p c=0.99; 1-10 Mathematics 11m/12p c=0.99; 1-10 English 10m/10p c=0.98; Leaving to Learn 5m/5p c=0.96; ConnectED 2m/3p c=0.99; NCEA1 2m/4p c=0.97
- by era: Refresh 64m/71p c=0.98
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
- modules: BLL110, BLL120, BLL126, BLL131, BLL135, BLL144, BLL153, BLL161, BLL164, BLL167, BLL174, BLL175, BLL177, BLL212, BLL214, BLL227, BLL231, BLL233, BLL236, BLL241, BLL242, BLL245, BLL251, BLL252 …

### #562 · activity · EXTRA · `p>b` › gold `—` vs Claude `b` — CANDIDATE
- pages 80 / modules 58 / lines 112; consensus (all) 0.93 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 43m/52p c=0.94; Bilingual 6m/16p c=0.64; Inquiry 5m/8p c=0.88; Fundamentals 4m/4p c=0.92
- by subject: 1-10 Blended Literacy 12m/15p c=0.94; 1-10 English 8m/8p c=0.94; Leaving to Learn 8m/13p c=0.89; NCEA1 7m/10p c=0.95; 1-10 Mathematics 6m/6p c=0.98; Te Marautanga o Aotearoa TMoA 6m/16p c=0.64
- by era: Refresh 58m/80p c=0.93
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1009** AGH1009_3_0.html ↔ AGH1009.03.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `b  «Hint:»`
- **ANZH301** ANZH301_9_0.html ↔ ANZH301_9.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `b  «Name? Location? When established? Why established? Purpose? How does it serve its people and the wider community?»`
- **ANZH404** ANZH404_2_0.html ↔ ANZH404_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `b  «Rātana:»`
- modules: AGH1009, ANZH301, ANZH404, BLL112, BLL120, BLL133, BLL142, BLL147, BLL150, BLL156, BLL157, BLL164, BLL173, BLL176, BLL240, CEDK101, ENGC201, ENGC202, ENGC301, ENGI201, ENGI400, ENGI401, ENGJ101, ENGS101 …

### #566 · activity · SUBSTITUTED · `div.col-12` › gold `WIDGET` vs Claude `div.row` — CANDIDATE
- pages 62 / modules 52 / lines 75; consensus (all) 0.60 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 43m/53p c=0.59; Inquiry 5m/5p c=0.63; Fundamentals 4m/4p c=0.81
- by subject: 1-10 Blended Literacy 18m/18p c=0.66; 1-10 Mathematics 13m/15p c=0.70; NCEA1 4m/9p c=0.49; Online Safety (OS9000) 4m/4p c=0.65; ConnectED 3m/3p c=0.58; Leaving to Learn 3m/3p c=0.46
- by era: Refresh 52m/62p c=0.60
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH304** ANZH304_3_0.html ↔ ANZH304_0.3.html (structure, derivable=True)
  - gold: `WIDGET`
  - Claude: `div.row  «Hobson did a good job of making sure all rangatira of Aotearoa had agreed with the Treaty before telling Queen Victoria »`
- **BLL120** BLL120_0_0.html ↔ BLL120.html (structure, derivable=True)
  - gold: `WIDGET`
  - Claude: `div.row`
- **BLL123** BLL123_1_0.html ↔ BLL123-02.html (structure, derivable=True)
  - gold: `WIDGET`
  - Claude: `div.row  «Make a word»`
- modules: ANZH304, BLL120, BLL123, BLL124, BLL140, BLL144, BLL145, BLL162, BLL163, BLL166, BLL212, BLL216, BLL230, BLL234, BLL235, BLL241, BLL245, BLL251, BLL254, CEDK501, CEDO501, CEDT208, ENFUN04, ENGC201 …

### #569 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `h4.goJournal` — CANDIDATE
- pages 120 / modules 50 / lines 149; consensus (all) 0.95 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 47m/117p c=0.95; Inquiry 3m/3p c=0.92
- by subject: 1-10 English 17m/29p c=0.95; 1-10 Mathematics 17m/46p c=0.93; NCEA1 8m/37p c=0.98; ConnectED 4m/4p c=0.94; ANZH 2m/2p c=0.86; EXPlore 1m/1p c=1.00
- by era: Refresh 50m/120p c=0.95
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH104** ANZH104_5_0.html ↔ ANZH104_05.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h4.goJournal  «Go to your journal»`
- **ANZH205** ANZH205_4_0.html ↔ ANZH205_04.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h4.goJournal  «Go to your journal»`
- **CEDK102** CEDK102_0_0.html ↔ CEDK102.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h4.goJournal  «Go to your journal»`
- modules: ANZH104, ANZH205, CEDK102, CEDO301, CEDT207, CEDW201, ENGC101, ENGC102, ENGC202, ENGI101, ENGI102, ENGI201, ENGI202, ENGJ101, ENGJ102, ENGJ201, ENGJ202, ENGJ301, ENGJ402, ENGR101, ENGR201, ENGR302, ENGS101, EXBP901 …

### #570 · activity · SUBSTITUTED · `div.col-12` › gold `WIDGET` vs Claude `p` — CANDIDATE
- pages 56 / modules 50 / lines 62; consensus (all) 0.60 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 41m/47p c=0.59; Inquiry 5m/5p c=0.63; Fundamentals 3m/3p c=0.81; Bilingual 1m/1p c=0.67
- by subject: 1-10 Mathematics 17m/22p c=0.70; 1-10 Blended Literacy 12m/12p c=0.66; NCEA1 7m/8p c=0.49; 1-10 English 5m/5p c=0.64; 1-10 Health and PE 3m/3p c=0.87; ConnectED 2m/2p c=0.58
- by era: Refresh 50m/56p c=0.60
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1002** AGH1002_4_0.html ↔ AGH1002.04.html (structure, derivable=True)
  - gold: `WIDGET`
  - Claude: `p  «Based on your knowledge of soil particle size, order the soils on the continuum below.»`
- **AGH1004** AGH1004_5_0.html ↔ AGH1004.05.html (structure, derivable=True)
  - gold: `WIDGET`
  - Claude: `p  «From the above information in the paragraphs and video, identify some of the positive and negative impacts of irrigation»`
- **AGH1005** AGH1005_2_0.html ↔ AGH1005.02.html (structure, derivable=True)
  - gold: `WIDGET`
  - Claude: `p  «The main functions of fruits and seeds are to:»`
- modules: AGH1002, AGH1004, AGH1005, BLL111, BLL112, BLL135, BLL142, BLL145, BLL153, BLL157, BLL175, BLL176, BLL213, BLL220, BLL251, CEDO102, CEDT207, ENGC101, ENGI103, ENGJ301, ENGJ302, ENGS301, HES1006, HIS1002 …

### #571 · activity · SUBSTITUTED · `div.col-12` › gold `a` vs Claude `h4.goJournal` — CANDIDATE
- pages 108 / modules 48 / lines 135; consensus (all) 0.57 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 47m/106p c=0.57; Inquiry 1m/2p c=0.71
- by subject: 1-10 Mathematics 18m/48p c=0.71; 1-10 English 15m/25p c=0.55; NCEA1 8m/24p c=0.67; ANZH 5m/8p c=0.44; ConnectED 1m/2p c=0.60; None 1m/1p c=0.37
- by era: Refresh 48m/108p c=0.57
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH101** ANZH101_2_0.html ↔ ANZH101_2.0.html (structure, derivable=True)
  - gold: `a  «Go to journal»`
  - Claude: `h4.goJournal  «Go to your journal»`
- **ANZH104** ANZH104_4_0.html ↔ ANZH104_04.0.html (structure, derivable=True)
  - gold: `a  «Go to journal»`
  - Claude: `h4.goJournal  «Go to your journal»`
- **ANZH105** ANZH105_4_0.html ↔ ANZH105_04.0.html (structure, derivable=True)
  - gold: `a  «Go to journal»`
  - Claude: `h4.goJournal  «Go to your journal»`
- modules: ANZH101, ANZH104, ANZH105, ANZH203, ANZH205, CEDT301, ENGC101, ENGC102, ENGC202, ENGI101, ENGI102, ENGI103, ENGI201, ENGI202, ENGJ101, ENGJ201, ENGR101, ENGR201, ENGR202, ENGS201, ENGS202, HES1003, HES1004, HES1006 …

### #572 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `a` — CANDIDATE
- pages 80 / modules 48 / lines 98; consensus (all) 0.86 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 44m/72p c=0.87; Inquiry 3m/7p c=0.68; Fundamentals 1m/1p c=0.72
- by subject: 1-10 English 10m/11p c=0.87; 1-10 Blended Literacy 9m/9p c=0.93; NCEA1 8m/17p c=0.80; 1-10 Mathematics 8m/13p c=0.83; Leaving to Learn 7m/20p c=0.82; ANZH 2m/5p c=0.92
- by era: Refresh 48m/80p c=0.86
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1001** AGH1001_3_0.html ↔ AGH1001.03.html (structure, derivable=True)
  - gold: `—`
  - Claude: `a  «Ranginui – Sky father»`
- **AGH1003** AGH1003_1_0.html ↔ AGH1003_01.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `a  «Need some extra help? Have a look at FUNdamentals 01»`
- **AGH1004** AGH1004_2_0.html ↔ AGH1004.06.html (structure, derivable=True)
  - gold: `—`
  - Claude: `a  «New Zealand Topographical Map»`
- modules: AGH1001, AGH1003, AGH1004, ANZH303, ANZH304, BLL115, BLL117, BLL122, BLL126, BLL131, BLL133, BLL151, BLL214, BLL227, CEDT101, ENFUN04, ENGC202, ENGI201, ENGI301, ENGI303, ENGI400, ENGJ202, ENGJ301, ENGJ403 …

### #574 · activity · EXTRA · `ol` › gold `—` vs Claude `li` — CANDIDATE
- pages 66 / modules 48 / lines 264; consensus (all) 0.96 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 34m/52p c=0.97; Fundamentals 8m/8p c=0.95; Inquiry 6m/6p c=0.83
- by subject: 1-10 Mathematics 11m/17p c=0.98; NCEA1 10m/17p c=0.97; 1-10 Health and PE 4m/4p c=1.00; Leaving to Learn 4m/4p c=0.91; ANZH 3m/6p c=0.97; ConnectED 3m/3p c=0.94
- by era: Refresh 48m/66p c=0.96
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1002** AGH1002_2_0.html ↔ AGH1002.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `li  «35% Clay 50% Silt 15%Sand»`
- **AGH1003** AGH1003_8_0.html ↔ AGH1003_08.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `li  «True»`
- **ANZH303** ANZH303_2_0.html ↔ ANZH303_0.2.html (structure, derivable=True)
  - gold: `—`
  - Claude: `li  «Explain the role of mauri in the presence of mana.»`
- modules: AGH1002, AGH1003, ANZH303, ANZH304, ANZH404, ARFUN04, BLL120, BLLR201, CEDK102, CEDO501, CEDT101, ENGI103, ENGJ302, EXIP901, HIS1005, HIS1006, HIS1008, HPFUN203, HPFUN401, HPFUN402, HPFUN403, MXDB302, MXDI201, MXDI202 …

### #575 · activity · SUBSTITUTED · `div.col-12` › gold `h3` vs Claude `WIDGET` — CANDIDATE
- pages 83 / modules 47 / lines 104; consensus (all) 0.76 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 38m/74p c=0.76; Fundamentals 6m/6p c=0.94; Inquiry 3m/3p c=0.77
- by subject: 1-10 English 20m/41p c=0.82; 1-10 Mathematics 11m/21p c=0.85; NCEA1 6m/9p c=0.77; 1-10 Technology 2m/2p c=1.00; Leaving to Learn 2m/3p c=0.73; ANZH 1m/1p c=0.64
- by era: Refresh 47m/83p c=0.76
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1001** AGH1001_1_0.html ↔ AGH1001.01.html (structure, derivable=True)
  - gold: `h3  «What are primary products?»`
  - Claude: `WIDGET`
- **AGH1004** AGH1004_2_0.html ↔ AGH1004.06.html (structure, derivable=True)
  - gold: `h3  «Regional topography»`
  - Claude: `WIDGET`
- **AGH1005** AGH1005_6_0.html ↔ AGH1005.06.html (structure, derivable=True)
  - gold: `h3  «Plant nutrient scenario»`
  - Claude: `WIDGET`
- modules: AGH1001, AGH1004, AGH1005, AGH1008, AGH1009, ANZH104, ARFUN01, BLL240, CEDT207, ENFUN03, ENFUN07, ENFUN09, ENGC201, ENGC202, ENGC301, ENGC302, ENGC401, ENGI103, ENGI302, ENGI303, ENGI400, ENGR201, ENGR202, ENGR302 …

### #576 · activity · EXTRA · `a` › gold `—` vs Claude `div.button` — CANDIDATE
- pages 82 / modules 47 / lines 177; consensus (all) 0.77 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 34m/63p c=0.79; Inquiry 9m/15p c=0.56; Fundamentals 4m/4p c=0.72
- by subject: Leaving to Learn 10m/37p c=0.88; 1-10 Mathematics 8m/14p c=0.60; 1-10 English 7m/9p c=0.81; ConnectED 5m/5p c=0.76; NCEA1 4m/4p c=0.62; 1-10 Blended Literacy 3m/3p c=0.96
- by era: Refresh 47m/82p c=0.77
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: INDEX.md:84 — - **`05_COMP_LANGUAGE_MEDIA_LAYOUT/05D_COMP14_BUTTONS_TABLES_COLUMNS.md`** (21 KB) — COMP_14 Layout & Structure, second half: Buttons (incl. the "Go t
  - KB: INDEX.md:85 — - Sections: Buttons (MTK Quiz — the activity shell `[MTKquiz]` builds) · Supervisor Button (Shape A/B/C · the reveal panel · edge cases) · Tables · Co
  - KB: _project_instructions_.md:28 — - **`ASSESSMENT MODE`** phrase (any capitalisation), **or** an uploaded `.docx` that is an **NCEA Assessment Activity** document (details table `Activ
- **ARFUN04** ARFUN04_0_0.html ↔ ARFUN04_0.00.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.button  «Go to quiz»`
- **BLL110** BLL110_0_0.html ↔ BLL110.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.button  «Go to quiz»`
- **BLL113** BLL113_1_0.html ↔ BLL113-02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.button  «Go to check in. (»`
- modules: ARFUN04, BLL110, BLL113, BLL160, BLLR201, CEDK501, CEDO301, CEDT104, CEDT208, CEDW201, ENGI303, ENGI400, ENGI401, ENGI405, ENGJ101, ENGJ402, ENGR301, HIS1002, HIS1003, HIS1008, HPRE203, MXEO401, MXEX401, MXFL102 …

### #579 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `p>i` — CANDIDATE
- pages 48 / modules 42 / lines 87; consensus (all) 0.97 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 34m/40p c=0.98; Inquiry 5m/5p c=0.90; Fundamentals 3m/3p c=0.92
- by subject: 1-10 Blended Literacy 18m/19p c=0.92; 1-10 English 8m/8p c=0.97; ConnectED 4m/4p c=0.97; NCEA1 4m/9p c=0.98; Leaving to Learn 3m/3p c=1.00; ANZH 2m/2p c=1.00
- by era: Refresh 42m/48p c=0.97
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH303** ANZH303_1_0.html ↔ ANZH303_0.1.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Eruera Maihi Patuone was the eldest son of Tapua, leader and of Ngāti Hao of Hokianga. Through his father he was descend»`
- **ANZH304** ANZH304_5_0.html ↔ ANZH304_0.5.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «It would be a good idea to refresh your memory on how to write a well-structured paragraph in History by looking at the »`
- **BLL111** BLL111_2_0.html ↔ BLL111-03.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «To develop fluency the students need to re-read the same book multiple times. We are wanting them to go from sounding ou»`
- modules: ANZH303, ANZH304, BLL111, BLL113, BLL114, BLL115, BLL117, BLL126, BLL132, BLL133, BLL135, BLL136, BLL231, BLL233, BLL234, BLL235, BLL236, BLL237, BLL254, BLL263, CEDK101, CEDT101, CEDW101, CEDW201 …

### #582 · activity · SUBSTITUTED · `div.col-12` › gold `p` vs Claude `WIDGET` — CANDIDATE
- pages 51 / modules 40 / lines 60; consensus (all) 0.76 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 29m/36p c=0.75; Fundamentals 7m/7p c=0.94; Inquiry 4m/8p c=0.83
- by subject: 1-10 Blended Literacy 8m/12p c=0.67; 1-10 English 7m/11p c=0.81; Leaving to Learn 6m/6p c=0.73; NCEA1 4m/4p c=0.78; None 4m/5p c=0.89; 1-10 Mathematics 3m/4p c=0.84
- by era: Refresh 40m/51p c=0.76
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1003** AGH1003_3_0.html ↔ AGH1003_03.0.html (structure, derivable=True)
  - gold: `p  «Go to your journal and complete Activity 3B.»`
  - Claude: `WIDGET`
- **AGH1006** AGH1006_3_0.html ↔ AGH1006.04.html (structure, derivable=True)
  - gold: `p  «Go to your journal to anwser questions about this scenario.»`
  - Claude: `WIDGET`
- **ANZH301** ANZH301_3_0.html ↔ ANZH301_3.0.html (structure, derivable=True)
  - gold: `p  «Look at and read the text in the diagram below about the impacts of city life on loss of Māori identity as Māori.»`
  - Claude: `WIDGET`
- modules: AGH1003, AGH1006, ANZH301, BLL110, BLL114, BLL226, BLL230, BLL235, BLL237, BLL240, BLL254, CEDR501, CHFUN01, CHFUN05, ENGC101, ENGJ301, ENGJ302, ENGR101, ENGR102, ENGR302, ENGS301, HIS1003, HIS1004, HPFUN103 …

### #585 · activity · EXTRA · `p>i` › gold `—` vs Claude `i` — CANDIDATE
- pages 44 / modules 38 / lines 50; consensus (all) 0.96 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 37m/43p c=0.97; Inquiry 1m/1p c=0.87
- by subject: 1-10 Blended Literacy 21m/23p c=0.90; 1-10 English 8m/8p c=0.95; Leaving to Learn 3m/4p c=0.99; NCEA1 2m/2p c=0.97; ANZH 2m/2p c=1.00; 1-10 Mathematics 2m/5p c=0.99
- by era: Refresh 38m/44p c=0.96
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1009** AGH1009_3_0.html ↔ AGH1009.03.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `i  «Low fertility which increases the amount of fertiliser that needs to applied.»`
- **ANZH303** ANZH303_1_0.html ↔ ANZH303_0.1.html (structure, derivable=True)
  - gold: `—`
  - Claude: `i  «He kakano ahau.»`
- **ANZH404** ANZH404_3_0.html ↔ ANZH404_3.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `i  «alongside»`
- modules: AGH1009, ANZH303, ANZH404, BLL114, BLL115, BLL120, BLL123, BLL134, BLL137, BLL141, BLL143, BLL144, BLL146, BLL151, BLL156, BLL164, BLL173, BLL175, BLL176, BLL214, BLL221, BLL233, BLL234, BLL241 …

### #586 · activity · SUBSTITUTED · `div.col-12` › gold `a` vs Claude `p` — CANDIDATE
- pages 50 / modules 37 / lines 52; consensus (all) 0.57 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 36m/49p c=0.57; Fundamentals 1m/1p c=0.59
- by subject: 1-10 Mathematics 12m/17p c=0.71; NCEA1 11m/13p c=0.67; 1-10 English 5m/10p c=0.55; Leaving to Learn 4m/5p c=0.57; 1-10 Blended Literacy 2m/2p c=0.55; ANZH 1m/1p c=0.44
- by era: Refresh 37m/50p c=0.57
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1002** AGH1002_3_0.html ↔ AGH1002.03.html (structure, derivable=True)
  - gold: `a  «Go to journal»`
  - Claude: `p  «Remember how photosynthesis used carbon dioxide and water to produce glucose and oxygen.»`
- **AGH1005** AGH1005_4_0.html ↔ AGH1005.04.html (structure, derivable=True)
  - gold: `a  «Go to journal»`
  - Claude: `p  «These factors include:»`
- **AGH1008** AGH1008_1_0.html ↔ AGH1008.01.html (structure, derivable=True)
  - gold: `a  «Who's eating NZ»`
  - Claude: `p  «New Zealand farmers and growers show care, or manaakitanga in a range of different ways. Farmers are guardians, or kaiti»`
- modules: AGH1002, AGH1005, AGH1008, ANZH105, BLL122, BLL232, ENGI101, ENGI401, ENGI405, ENGJ403, ENGR102, EXIP901, HES1003, HES1005, HES1006, HES1007, HIS1003, HIS1004, HPFUN303, MXDB102, MXDB201, MXDB302, MXEO202, MXEX201 …

### #594 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `div.videoSection.ratio.ratio-16x9` — CANDIDATE
- pages 43 / modules 31 / lines 53; consensus (all) 0.99 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 23m/33p c=0.99; Inquiry 6m/8p c=0.91; Bilingual 2m/2p c=0.98
- by subject: Leaving to Learn 8m/16p c=0.96; 1-10 Mathematics 7m/8p c=0.99; 1-10 English 5m/6p c=1.00; ConnectED 4m/4p c=0.98; NCEA1 2m/4p c=1.00; 1-10 Blended Literacy 2m/2p c=0.97
- by era: Refresh 31m/43p c=0.99
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:43 — | Video wrapper | `embed-responsive embed-responsive-16by9` | `ratio ratio-16x9` |
  - KB: 06_TEMPLATE_RECOGNITION.md:374 — <div class="videoSection ratio ratio-16x9">
  - KB: 00_MASTER_INSTRUCTIONS/00C_FILE_REFERENCE_INDEX.md:26 — | Subject Global Parameters | `14_SUBJECT_GLOBAL_PARAMETERS.md` | The design team's per-subject **global-parameter** conventions, folded in so the Con
- **AGH1003** AGH1003_1_0.html ↔ AGH1003_01.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.videoSection.ratio.ratio-16x9`
- **AGH1008** AGH1008_1_0.html ↔ AGH1008.01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.videoSection.ratio.ratio-16x9`
- **BLL216** BLL216_2_0.html ↔ BLL216-2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.videoSection.ratio.ratio-16x9`
- modules: AGH1003, AGH1008, BLL216, BLL233, CEDK101, CEDO102, CEDR204, CEDT101, ENGC202, ENGJ201, ENGJ302, ENGR102, ENGR302, MXDB302, MXDI102, MXDI103, MXEO201, MXEX401, MXFL302, MXFU202, OSBY201, PNR102, PNR104, XDLS902 …

### #598 · activity · EXTRA · `ul` › gold `—` vs Claude `li` — CANDIDATE
- pages 31 / modules 30 / lines 168; consensus (all) 0.93 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 25m/26p c=0.95; Inquiry 5m/5p c=0.74
- by subject: NCEA1 9m/9p c=0.97; ConnectED 6m/6p c=0.85; 1-10 Mathematics 4m/4p c=0.97; 1-10 Blended Literacy 3m/3p c=0.95; Leaving to Learn 3m/3p c=0.87; ANZH 1m/2p c=1.00
- by era: Refresh 30m/31p c=0.93
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1003** AGH1003_8_0.html ↔ AGH1003_08.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `li  «Crop rotation can add nitrogen to soils.»`
- **AGH1004** AGH1004_1_0.html ↔ AGH1004.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `li  «Mountain ranges□»`
- **AGH1007** AGH1007_7_0.html ↔ AGH1007.01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `li  «The male reproductive tract is responsible creating and releasing sperm.»`
- modules: AGH1003, AGH1004, AGH1007, ANZH303, BLL134, BLL137, BLL151, CEDO102, CEDT101, CEDT104, CEDT207, CEDT404, CEDT501, ENGC101, HES1007, HIS1004, MXDB201, MXFL102, MXFL204, MXFU202, OSSC401, PES1001, PES1002, PHE1005 …

### #600 · activity · SUBSTITUTED · `div.col-12` › gold `a` vs Claude `WIDGET` — CANDIDATE
- pages 33 / modules 29 / lines 33; consensus (all) 0.57 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 24m/28p c=0.57; Inquiry 2m/2p c=0.71; Fundamentals 2m/2p c=0.59; Bilingual 1m/1p c=0.43
- by subject: 1-10 English 9m/11p c=0.55; 1-10 Blended Literacy 8m/8p c=0.55; Leaving to Learn 4m/4p c=0.57; ConnectED 2m/4p c=0.60; 1-10 Mathematics 2m/2p c=0.71; Online Safety (OS9000) 1m/1p c=0.20
- by era: Refresh 29m/33p c=0.57
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL112** BLL112_1_0.html ↔ BLL112-02.html (structure, derivable=True)
  - gold: `a  «Upload to dropbox»`
  - Claude: `WIDGET`
- **BLL123** BLL123_2_0.html ↔ BLL123-03.html (structure, derivable=True)
  - gold: `a  «Upload to dropbox»`
  - Claude: `WIDGET`
- **BLL126** BLL126_1_0.html ↔ BLL126-02.html (structure, derivable=True)
  - gold: `a  «Upload to dropbox»`
  - Claude: `WIDGET`
- modules: BLL112, BLL123, BLL126, BLL131, BLL162, BLL175, BLL210, BLL220, CEDT501, CEDW501, ENGC101, ENGC102, ENGC301, ENGI101, ENGI401, ENGJ201, ENGR102, ENGS101, ENGS201, MXEO202, MXFL102, OSBY401, SSFUN08, TEDC402 …

### #603 · activity · EXTRA · `div.activity` › gold `—` vs Claude `div.row` — CANDIDATE
- pages 40 / modules 27 / lines 54; consensus (all) 1.00 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 18m/31p c=1.00; Fundamentals 5m/5p c=1.00; Inquiry 3m/3p c=1.00; Bilingual 1m/1p c=1.00
- by subject: NCEA1 8m/15p c=1.00; 1-10 Mathematics 6m/10p c=1.00; 1-10 Social Science 3m/3p c=1.00; ANZH 2m/4p c=1.00; ConnectED 2m/2p c=1.00; 1-10 Arts 1m/1p c=1.00
- by era: Refresh 27m/40p c=1.00
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:46 — | Activity class | `content activity activity-bg` | `activity` |
  - KB: 06_TEMPLATE_RECOGNITION.md:179 — - TWHA902–904 use `choicePage` activity grids and dual titles + `whakatauki` — these are content patterns, safe to use if the new module needs them
  - KB: 06_TEMPLATE_RECOGNITION.md:263 — **The X-prefix test governs THIS CLASS ONLY.** The wider LS look-and-feel conventions of `14_SUBJECT_GLOBAL_PARAMETERS.md` § 14.6 — terminology and br
- **AGH1008** AGH1008_5_0.html ↔ AGH1008.05.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Select the visual signs below which show a cow is on heat.»`
- **ANZH301** ANZH301_3_0.html ↔ ANZH301_3.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Assimilation means one culture is taken over and completely absorbed by another, leaving little or nothing of its tradit»`
- **ANZH304** ANZH304_2_0.html ↔ ANZH304_0.2.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «In the early 1800s, New Zealand was seen as a good place for a British colony. Māori were admired for their organised so»`
- modules: AGH1008, ANZH301, ANZH304, ARFUN04, CEDK101, CEDR204, ENGJ402, HIS1003, HIS1004, HIS1005, HIS1006, HIS1007, HIS1008, HPFUN901, MXDI201, MXDI202, MXEO102, MXFL104, MXFL203, MXFL204, PHE1006, SSFUN02, SSFUN05, SSFUN06 …

### #608 · activity · EXTRA · `div.videoSection.ratio.ratio-16x9` › gold `—` vs Claude `iframe` — CANDIDATE
- pages 35 / modules 26 / lines 50; consensus (all) 0.97 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 17m/22p c=0.98; Inquiry 8m/12p c=0.80; Fundamentals 1m/1p c=1.00
- by subject: 1-10 Mathematics 9m/11p c=0.99; 1-10 Blended Literacy 7m/7p c=0.94; ConnectED 4m/4p c=0.97; Leaving to Learn 4m/9p c=0.85; 1-10 English 2m/4p c=0.99
- by era: Refresh 26m/35p c=0.97
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:43 — | Video wrapper | `embed-responsive embed-responsive-16by9` | `ratio ratio-16x9` |
  - KB: 06_TEMPLATE_RECOGNITION.md:374 — <div class="videoSection ratio ratio-16x9">
  - KB: 00_MASTER_INSTRUCTIONS/00C_FILE_REFERENCE_INDEX.md:26 — | Subject Global Parameters | `14_SUBJECT_GLOBAL_PARAMETERS.md` | The design team's per-subject **global-parameter** conventions, folded in so the Con
- **BLL110** BLL110_0_0.html ↔ BLL110.html (structure, derivable=True)
  - gold: `—`
  - Claude: `iframe`
- **BLL120** BLL120_0_0.html ↔ BLL120.html (structure, derivable=True)
  - gold: `—`
  - Claude: `iframe`
- **BLL130** BLL130_0_0.html ↔ BLL130.html (structure, derivable=True)
  - gold: `—`
  - Claude: `iframe`
- modules: BLL110, BLL120, BLL130, BLL216, BLL221, BLL225, BLL233, CEDK101, CEDR204, CEDT207, CEDT208, ENGJ102, ENGR302, MXDB102, MXDI101, MXDI103, MXEO202, MXFL102, MXFL103, MXFL302, MXFU302, MXFUN01, XDLS903, XDLS905 …

### #610 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `audio.audioPlayer.icon` — CANDIDATE
- pages 41 / modules 25 / lines 271; consensus (all) 1.00 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 15m/18p c=1.00; Bilingual 6m/19p c=1.00; Inquiry 4m/4p c=1.00
- by subject: 1-10 Blended Literacy 15m/17p c=1.00; Te Marautanga o Aotearoa TMoA 6m/19p c=1.00; 1-10 English 2m/2p c=1.00; 1-10 Mathematics 1m/2p c=1.00; 1-10 Social Science 1m/1p c=1.00
- by era: Refresh 25m/41p c=1.00
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:381 — <audio preload="none" class="audioPlayer" title="...">
  - KB: INDEX.md:159 — - Sections: 14C — Languages Audiovisual Package: the complete asset registry · 1. Delivery forms (the supplied markup shapes) · 2. Language icons · 3.
  - KB: 00_MASTER_INSTRUCTIONS/00C_FILE_REFERENCE_INDEX.md:26 — | Subject Global Parameters | `14_SUBJECT_GLOBAL_PARAMETERS.md` | The design team's per-subject **global-parameter** conventions, folded in so the Con
- **BLL110** BLL110_0_0.html ↔ BLL110.html (structure, derivable=True)
  - gold: `—`
  - Claude: `audio.audioPlayer.icon`
- **BLL111** BLL111_1_0.html ↔ BLL111-02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `audio.audioPlayer.icon`
- **BLL113** BLL113_1_0.html ↔ BLL113-02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `audio.audioPlayer.icon`
- modules: BLL110, BLL111, BLL113, BLL115, BLL120, BLL121, BLL131, BLL162, BLL212, BLL220, BLL222, BLL227, BLL230, BLL241, BLL251, ENGI202, ENGI203, MXEO301, PNR104, SSOG101, TRR109, TRR111, TRR112, TRR113 …

### #612 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `h5` — CANDIDATE
- pages 31 / modules 25 / lines 55; consensus (all) 0.98 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 20m/26p c=0.99; Inquiry 2m/2p c=0.94; Fundamentals 2m/2p c=0.95; Bilingual 1m/1p c=1.00
- by subject: 1-10 Mathematics 9m/12p c=0.99; 1-10 English 7m/9p c=0.99; ANZH 2m/2p c=1.00; Leaving to Learn 2m/2p c=0.97; ConnectED 1m/1p c=0.97; NCEA1 1m/2p c=0.99
- by era: Refresh 25m/31p c=0.98
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH101** ANZH101_2_0.html ↔ ANZH101_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «Paikea»`
- **ANZH303** ANZH303_6_0.html ↔ ANZH303_0.6.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «Activity 2: Significance»`
- **CEDW201** CEDW201_0_0.html ↔ CEDW201 The Language of Kindness and Caring.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «Found poems»`
- modules: ANZH101, ANZH303, CEDW201, ENFUN01, ENGI202, ENGI203, ENGI302, ENGJ301, ENGJ302, ENGR302, HIS1005, HPRE203, MXDB302, MXEO201, MXEO301, MXFL104, MXFL203, MXFL302, MXFU202, MXFU301, MXFU302, SSFUN05, TRR108, XDLS903 …

### #614 · activity · SUBSTITUTED · `div.col-12` › gold `WIDGET` vs Claude `div.col-md-8.col-12` — CANDIDATE
- pages 25 / modules 24 / lines 26; consensus (all) 0.60 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 16m/16p c=0.59; Inquiry 4m/5p c=0.63; Fundamentals 3m/3p c=0.81; Bilingual 1m/1p c=0.67
- by subject: 1-10 Mathematics 6m/6p c=0.70; 1-10 Blended Literacy 3m/3p c=0.66; NCEA1 3m/4p c=0.49; Leaving to Learn 3m/3p c=0.46; ConnectED 2m/2p c=0.58; None 2m/2p c=0.83
- by era: Refresh 24m/25p c=0.60
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH105** ANZH105_1_0.html ↔ ANZH105_01.0.html (structure, derivable=True)
  - gold: `WIDGET`
  - Claude: `div.col-md-8.col-12`
- **BLL150** BLL150_0_0.html ↔ BLL150.html (structure, derivable=True)
  - gold: `WIDGET`
  - Claude: `div.col-md-8.col-12  «room, moon, zoom, roof, food (please note the double up of letters)»`
- **BLL170** BLL170_0_0.html ↔ BLL170.html (structure, derivable=True)
  - gold: `WIDGET`
  - Claude: `div.col-md-8.col-12`
- modules: ANZH105, BLL150, BLL170, BLL254, CEDO501, CEDO502, CHFUN05, ENGFUN02, HIS1002, HIS1004, MXDI103, MXEX401, MXFL202, MXFL203, MXFU301, MXFUN03, OSSM401, SCFUN01, TEDC402, TRR102, TWHA906, XGF9001, XGF9006, XTAS101

### #616 · activity · EXTRA · `p` › gold `—` vs Claude `b` — CANDIDATE
- pages 31 / modules 23 / lines 59; consensus (all) 0.96 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 20m/28p c=0.96; Fundamentals 2m/2p c=0.95; Bilingual 1m/1p c=0.89
- by subject: NCEA1 6m/9p c=0.97; 1-10 Blended Literacy 4m/5p c=0.93; Leaving to Learn 4m/4p c=0.94; 1-10 English 2m/2p c=0.96; 1-10 Mathematics 2m/3p c=0.99; 1-10 Social Science 2m/2p c=0.97
- by era: Refresh 23m/31p c=0.96
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH301** ANZH301_2_0.html ↔ ANZH301_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `b  «integration»`
- **BLL154** BLL154_1_1.html ↔ BLL154-2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `b  «,»`
- **BLL164** BLL164_1_0.html ↔ BLL164-1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `b  «Meaning 1: Cool (as in popular or trendy)»`
- modules: ANZH301, BLL154, BLL164, BLL214, BLL254, CEDR501, ENGC101, ENGS301, HIS1002, HIS1003, HIS1004, HIS1005, HIS1007, HIS1008, MXDI103, MXFL104, SSFUN02, SSFUN08, TRR112, XDLS502, XGF9002, XMES103, XTAS103

### #621 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `div.videoSection.icon.ratio.ratio-16x9` — CANDIDATE
- pages 38 / modules 22 / lines 63; consensus (all) 0.97 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 16m/32p c=0.98; Inquiry 3m/3p c=0.89; Fundamentals 3m/3p c=0.91
- by subject: 1-10 Blended Literacy 6m/6p c=0.98; NCEA1 5m/16p c=0.94; ANZH 4m/7p c=0.99; 1-10 English 3m/3p c=0.99; 1-10 Mathematics 2m/4p c=0.97; 1-10 Social Science 2m/2p c=0.92
- by era: Refresh 22m/38p c=0.97
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:43 — | Video wrapper | `embed-responsive embed-responsive-16by9` | `ratio ratio-16x9` |
  - KB: 06_TEMPLATE_RECOGNITION.md:374 — <div class="videoSection ratio ratio-16x9">
  - KB: INDEX.md:160 — - **`14_SUBJECT_GLOBAL_PARAMETERS/14D_SGP_CROSSCUTTING_AND_TECHNOLOGY.md`** (6 KB) — Cross-cutting notes (14.11) and the Technology family (14.12 — fi
- **ANZH301** ANZH301_2_0.html ↔ ANZH301_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.videoSection.icon.ratio.ratio-16x9`
- **ANZH303** ANZH303_4_0.html ↔ ANZH303_0.4.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.videoSection.icon.ratio.ratio-16x9`
- **ANZH304** ANZH304_3_0.html ↔ ANZH304_0.3.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.videoSection.icon.ratio.ratio-16x9`
- modules: ANZH301, ANZH303, ANZH304, ANZH404, BLL110, BLL113, BLL120, BLL130, BLL161, BLL177, ENFUN01, ENGI202, ENGI203, HIS1004, HIS1005, HIS1006, HIS1007, HIS1008, MXFL203, MXFL204, SSFUN02, SSFUN08

### #624 · activity · SUBSTITUTED · `div.row` › gold `div.col-12` vs Claude `div.col-md-8.col-12` — CANDIDATE
- pages 25 / modules 22 / lines 36; consensus (all) 0.79 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 14m/17p c=0.78; Inquiry 4m/4p c=0.86; Fundamentals 3m/3p c=0.94; Bilingual 1m/1p c=0.68
- by subject: 1-10 Mathematics 6m/6p c=0.86; 1-10 English 4m/4p c=0.84; 1-10 Blended Literacy 3m/3p c=0.67; Leaving to Learn 3m/6p c=0.75; 1-10 Health and PE 2m/2p c=1.00; ANZH 1m/1p c=0.64
- by era: Refresh 22m/25p c=0.79
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH404** ANZH404_5_0.html ↔ ANZH404_5.0.html (structure, derivable=True)
  - gold: `div.col-12`
  - Claude: `div.col-md-8.col-12  «Kohimarama conference, 1860»`
- **BLL110** BLL110_0_0.html ↔ BLL110.html (structure, derivable=True)
  - gold: `div.col-12  «Sometimes ‘s’ makes a /z/ sound. This happens when your voice is turned on. If you say the /s/ sound like at the start o»`
  - Claude: `div.col-md-8.col-12  «Find the letter S»`
- **BLL120** BLL120_0_0.html ↔ BLL120.html (structure, derivable=True)
  - gold: `div.col-12  «If your ākonga is having difficulty remembering both the name of the letter and the sound of the letter, tell them the n»`
  - Claude: `div.col-md-8.col-12  «if your ākonga is having difficulty remembering both the name of the letter and the sound of the letter, tell them the n»`
- modules: ANZH404, BLL110, BLL120, BLL130, ENGC401, ENGI405, ENGJ202, ENGR302, HPFUN201, HPFUN903, MXDB201, MXDB202, MXDI103, MXEX201, MXFU401, MXFUN03, TEDC401, TRR114, TWHA904, XDLS501, XGF9002, XGF9006

### #629 · activity · SUBSTITUTED · `div.col-12` › gold `WIDGET` vs Claude `ol` — CANDIDATE
- pages 22 / modules 21 / lines 24; consensus (all) 0.60 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 17m/18p c=0.59; Fundamentals 3m/3p c=0.81; Inquiry 1m/1p c=0.63
- by subject: 1-10 Mathematics 5m/6p c=0.70; ANZH 3m/3p c=0.36; NCEA1 2m/2p c=0.49; 1-10 English 2m/2p c=0.64; 1-10 Science 2m/2p c=0.90; ConnectED 1m/1p c=0.58
- by era: Refresh 21m/22p c=0.60
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1002** AGH1002_5_0.html ↔ AGH1002.05.html (structure, derivable=True)
  - gold: `WIDGET`
  - Claude: `ol  «Name your three key nutrients that are essential for plant growth.»`
- **ANZH303** ANZH303_5_0.html ↔ ANZH303_0.5.html (structure, derivable=True)
  - gold: `WIDGET`
  - Claude: `ol  «The flag was designed by King William IV.»`
- **ANZH304** ANZH304_1_0.html ↔ ANZH304_0.1.html (structure, derivable=True)
  - gold: `WIDGET`
  - Claude: `ol  «How many decades does this interactive map cover?»`
- modules: AGH1002, ANZH303, ANZH304, ANZH404, CEDO501, ENGI103, ENGJ302, EXIP901, HPFUN403, MXDB302, MXEO202, MXFL201, MXFL202, MXFL204, OSOH401, PES1001, SCCH301, SCFUN01, SSFUN02, TWHA904, XMES203

### #631 · activity · SUBSTITUTED · `div.row` › gold `div.col-12` vs Claude `div.row` — CANDIDATE
- pages 21 / modules 21 / lines 25; consensus (all) 0.79 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 15m/15p c=0.78; Inquiry 3m/3p c=0.86; Fundamentals 3m/3p c=0.94
- by subject: 1-10 Mathematics 6m/6p c=0.86; Leaving to Learn 5m/5p c=0.75; 1-10 Blended Literacy 4m/4p c=0.67; 1-10 English 2m/2p c=0.84; ANZH 1m/1p c=0.64; ConnectED 1m/1p c=0.83
- by era: Refresh 21m/21p c=0.79
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html (structure, derivable=True)
  - gold: `div.col-12  «Skills»`
  - Claude: `div.row  «Ngā Kupu Nui | Important Words»`
- **BLL124** BLL124_1_0.html ↔ BLL124-02.html (structure, derivable=True)
  - gold: `div.col-12  «Writing using punctuation»`
  - Claude: `div.row`
- **BLL160** BLL160_0_0.html ↔ BLL160.html (structure, derivable=True)
  - gold: `div.col-12  «Make the words»`
  - Claude: `div.row  «Read the words»`
- modules: ANZH101, BLL124, BLL160, BLL222, BLL230, CEDT104, ENGC102, ENGI202, HES1003, MXDI103, MXFL101, MXFL103, MXFL104, MXFUN01, MXFUN03, TEFUN08, XDLS902, XGF9002, XGF9006, XMES103, XMES203

### #636 · activity · EXTRA · `a` › gold `—` vs Claude `div.externalButton` — CANDIDATE
- pages 26 / modules 19 / lines 34; consensus (all) 0.91 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 12m/19p c=0.91; Fundamentals 4m/4p c=0.84; Inquiry 3m/3p c=0.82
- by subject: 1-10 English 5m/6p c=0.93; NCEA1 3m/7p c=0.88; 1-10 Mathematics 3m/3p c=0.84; ANZH 2m/3p c=0.92; 1-10 Social Science 2m/2p c=0.79; Leaving to Learn 2m/3p c=0.87
- by era: Refresh 19m/26p c=0.91
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH301** ANZH301_5_0.html ↔ ANZH301_5.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.externalButton  «Go to website»`
- **ANZH401** ANZH401_4_0.html ↔ ANZH401_4.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.externalButton  «Button – National Library Source]»`
- **CEDT104** CEDT104_0_0.html ↔ CEDT104 Waiata In Motion.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.externalButton  «here, ākonga can tap the buttons with emojis, to hear the sounds]»`
- modules: ANZH301, ANZH401, CEDT104, ENFUN04, ENGI400, ENGI401, ENGJ202, ENGS101, HIS1003, HIS1004, HIS1005, MXDI201, MXDI202, MXFUN01, SSFUN02, SSFUN06, TWHA906, XDLS902, XDLS909

### #638 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `div.button` — CANDIDATE
- pages 30 / modules 18 / lines 50; consensus (all) 1.00 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 14m/26p c=1.00; Fundamentals 4m/4p c=1.00
- by subject: 1-10 Mathematics 7m/17p c=1.00; NCEA1 4m/5p c=1.00; ANZH 2m/3p c=1.00; 1-10 Health and PE 2m/2p c=1.00; 1-10 English 1m/1p c=1.00; 1-10 Science 1m/1p c=1.00
- by era: Refresh 18m/30p c=1.00
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: INDEX.md:84 — - **`05_COMP_LANGUAGE_MEDIA_LAYOUT/05D_COMP14_BUTTONS_TABLES_COLUMNS.md`** (21 KB) — COMP_14 Layout & Structure, second half: Buttons (incl. the "Go t
  - KB: INDEX.md:85 — - Sections: Buttons (MTK Quiz — the activity shell `[MTKquiz]` builds) · Supervisor Button (Shape A/B/C · the reveal panel · edge cases) · Tables · Co
  - KB: _project_instructions_.md:28 — - **`ASSESSMENT MODE`** phrase (any capitalisation), **or** an uploaded `.docx` that is an **NCEA Assessment Activity** document (details table `Activ
- **ANZH304** ANZH304_1_0.html ↔ ANZH304_0.1.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.button  «Check answer and reset buttons»`
- **ANZH404** ANZH404_2_0.html ↔ ANZH404_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.button  «Check answer button»`
- **ENGC101** ENGC101_2_0.html ↔ ENGC101_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.button  «Check»`
- modules: ANZH304, ANZH404, ENGC101, HIS1003, HIS1004, HIS1005, HIS1008, HPFUN402, HPFUN901, MXDB302, MXDI201, MXDI202, MXFL204, MXFU201, MXFU202, MXFUN03, SCCH301, SSFUN02

### #639 · activity · SUBSTITUTED · `div.row` › gold `div.col-12` vs Claude `WIDGET` — CANDIDATE
- pages 20 / modules 18 / lines 20; consensus (all) 0.79 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 11m/13p c=0.78; Fundamentals 5m/5p c=0.94; Inquiry 1m/1p c=0.86; Bilingual 1m/1p c=0.68
- by subject: 1-10 Blended Literacy 4m/4p c=0.67; 1-10 Health and PE 4m/4p c=1.00; NCEA1 2m/2p c=0.81; 1-10 English 2m/2p c=0.84; Leaving to Learn 2m/3p c=0.75; ConnectED 1m/2p c=0.83
- by era: Refresh 18m/20p c=0.79
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ART1006** ART1006_2_0.html ↔ ART1006_1.0.html (structure, derivable=True)
  - gold: `div.col-12  «Your portfolio»`
  - Claude: `WIDGET`
- **BLL110** BLL110_0_0.html ↔ BLL110.html (structure, derivable=True)
  - gold: `div.col-12  «Write the letter ‘a’ in the air with your finger.»`
  - Claude: `WIDGET`
- **BLL146** BLL146_2_0.html ↔ BLL146-2.0.html (structure, derivable=True)
  - gold: `div.col-12  «These activities are all about the word ‘jeep’. A jeep is a type of vehicle which is usually a 4-wheel drive.»`
  - Claude: `WIDGET`
- modules: ART1006, BLL110, BLL146, BLL217, BLL235, CEDT501, ENFUN04, ENGR101, HES1006, HPFUN201, HPFUN302, HPFUN402, HPFUN901, MXFU201, TEDC401, TRR102, XLP06, XMES103

### #642 · activity · SUBSTITUTED · `div.col-12` › gold `p` vs Claude `h4.goJournal` — CANDIDATE
- pages 30 / modules 17 / lines 30; consensus (all) 0.76 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 16m/29p c=0.75; Inquiry 1m/1p c=0.83
- by subject: 1-10 Mathematics 7m/12p c=0.84; 1-10 English 6m/10p c=0.81; NCEA1 2m/6p c=0.78; ANZH 1m/1p c=0.60; ConnectED 1m/1p c=0.81
- by era: Refresh 17m/30p c=0.76
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH104** ANZH104_2_0.html ↔ ANZH104_02.0.html (structure, derivable=True)
  - gold: `p  «You can draw your picture using the drawing tool in your journal or you can draw it on paper!»`
  - Claude: `h4.goJournal  «Go to your journal»`
- **CEDK102** CEDK102_0_0.html ↔ CEDK102.html (structure, derivable=True)
  - gold: `p  «A caption is a short sentence or phrase that describes what is happening in a photo.»`
  - Claude: `h4.goJournal  «Go to your journal»`
- **ENGC302** ENGC302_1_0.html ↔ ENGC302_0.1.html (structure, derivable=True)
  - gold: `p  «Kahu is excited to get a reply from you and get to know you! Write an email to your new e-pal, telling them all about yo»`
  - Claude: `h4.goJournal  «Go to your journal»`
- modules: ANZH104, CEDK102, ENGC302, ENGC401, ENGI103, ENGR201, ENGS201, ENGS202, HIS1005, HIS1008, MXDB102, MXDB201, MXDB202, MXDI101, MXEO201, MXFL102, MXFU301

### #644 · activity · EXTRA · `div.col-12` › gold `—` vs Claude `div.TKmodal` — CANDIDATE
- pages 20 / modules 17 / lines 84; consensus (all) 0.99 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 12m/13p c=1.00; Inquiry 5m/7p c=0.93
- by subject: 1-10 Blended Literacy 10m/10p c=0.98; 1-10 Mathematics 5m/6p c=0.99; ConnectED 2m/4p c=1.00
- by era: Refresh 17m/20p c=0.99
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL110** BLL110_0_0.html ↔ BLL110.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.TKmodal  «Find things in your home or in your neighbourhood that have the letter ‘s’ written on them.»`
- **BLL111** BLL111_2_0.html ↔ BLL111-03.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.TKmodal  «These activities are all about the word ‘ant’.»`
- **BLL112** BLL112_2_0.html ↔ BLL112-03.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.TKmodal  «These activities are all about the word ‘tap’.»`
- modules: BLL110, BLL111, BLL112, BLL120, BLL122, BLL130, BLL143, BLL161, BLL171, BLL172, CEDT208, CEDT301, MXDB201, MXDB302, MXFL101, MXFL103, MXFL301

### #650 · activity · EXTRA · `div.row` › gold `—` vs Claude `div.clickDropContent` — CANDIDATE
- pages 23 / modules 15 / lines 47; consensus (all) 0.99 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 15m/23p c=1.00
- by subject: 1-10 Blended Literacy 10m/11p c=0.98; NCEA1 2m/8p c=1.00; 1-10 English 1m/1p c=1.00; 1-10 Mathematics 1m/1p c=1.00; None 1m/2p c=1.00
- by era: Refresh 15m/23p c=0.99
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL217** BLL217_2_0.html ↔ BLL217_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.clickDropContent  «https://www.istockphoto.com/photo/afl-ball-and-trophy-held-aloft-gm182177761-10456123»`
- **BLL221** BLL221_2_0.html ↔ BLL221-2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.clickDropContent  «https://www.istockphoto.com/photo/mesmerizing-full-moon-over-sea-3d-background-gm1712822359-539896437»`
- **BLL231** BLL231_2_0.html ↔ BLL231-2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.clickDropContent  «https://www.istockphoto.com/photo/dog-running-free-in-park-with-leash-trailing-behind-on-green-grass-gm1468031731-499668»`
- modules: BLL217, BLL221, BLL231, BLL235, BLL237, BLL241, BLL244, BLL246, BLL253, BLL254, ENGJ302, HES1005, HES1007, MXEO301, SCPH301

### #651 · activity · EXTRA · `div.row` › gold `—` vs Claude `WIDGET` — CANDIDATE
- pages 22 / modules 15 / lines 30; consensus (all) 1.00 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 15m/22p c=1.00
- by subject: 1-10 Blended Literacy 8m/8p c=0.99; NCEA1 2m/8p c=1.00; 1-10 English 1m/1p c=0.99; 1-10 Mathematics 1m/1p c=1.00; Online Safety (OS9000) 1m/1p c=1.00; None 1m/2p c=1.00
- by era: Refresh 15m/22p c=1.00
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL221** BLL221_2_0.html ↔ BLL221-2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **BLL231** BLL231_2_0.html ↔ BLL231-2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **BLL235** BLL235_2_0.html ↔ BLL235-2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- modules: BLL221, BLL231, BLL235, BLL237, BLL241, BLL244, BLL246, BLL253, ENGJ302, HES1005, HES1007, MXEO301, OSSC401, SCPH301, XMES103

### #660 · activity · EXTRA · `div.col-md-8.col-12` › gold `—` vs Claude `div.activity` — CANDIDATE
- pages 20 / modules 14 / lines 24; consensus (all) 1.00 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 11m/17p c=1.00; Fundamentals 2m/2p c=1.00; Inquiry 1m/1p c=1.00
- by subject: NCEA1 4m/6p c=1.00; 1-10 Mathematics 3m/4p c=1.00; 1-10 Health and PE 2m/2p c=1.00; Leaving to Learn 2m/2p c=1.00; ANZH 1m/4p c=1.00; 1-10 English 1m/1p c=1.00
- by era: Refresh 14m/20p c=1.00
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:46 — | Activity class | `content activity activity-bg` | `activity` |
  - KB: 06_TEMPLATE_RECOGNITION.md:179 — - TWHA902–904 use `choicePage` activity grids and dual titles + `whakatauki` — these are content patterns, safe to use if the new module needs them
  - KB: 06_TEMPLATE_RECOGNITION.md:263 — **The X-prefix test governs THIS CLASS ONLY.** The wider LS look-and-feel conventions of `14_SUBJECT_GLOBAL_PARAMETERS.md` § 14.6 — terminology and br
- **AGH1001** AGH1001_4_0.html ↔ AGH1001.04.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.activity  «In the space below, brainstorm the key features of each of New Zealand’s four seasons.»`
- **ANZH301** ANZH301_1_0.html ↔ ANZH301_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.activity  «Post-war blues»`
- **ENGI201** ENGI201_4_0.html ↔ ENGI201_4.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.activity  «A reflection on what they've learned in a unit could typically range from 150 to 300 words. However, it's important to e»`
- modules: AGH1001, ANZH301, ENGI201, HIS1003, HIS1004, HIS1008, HPFUN103, HPFUN202, MXFL203, MXFL204, MXFU202, TWHA906, XDLS906, XWHA02

### #6047 · body · EXTRA · `div#body` › gold `—` vs Claude `div.row` — CANDIDATE
- pages 1262 / modules 324 / lines 5165; consensus (all) 0.73 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 279m/1151p c=0.73; Bilingual 16m/38p c=0.60; Inquiry 15m/54p c=0.83; Fundamentals 14m/19p c=0.88
- by subject: 1-10 Blended Literacy 69m/122p c=0.99; NCEA1 44m/212p c=0.74; 1-10 English 41m/176p c=0.79; 1-10 Mathematics 40m/232p c=0.64; Leaving to Learn 34m/171p c=0.58; Online Safety (OS9000) 27m/87p c=0.60
- by era: Refresh 324m/1262p c=0.73
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1001** AGH1001_2_0.html ↔ AGH1001.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Career Example:»`
- **AGH1002** AGH1002_1_0.html ↔ AGH1002.01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Te toto o tetangatahe kai, teorangao tetangata, he whenua, he oneone»`
- **AGH1003** AGH1003_2_0.html ↔ AGH1003_02.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Irrigation and chemical properties of soil»`
- modules: AGH1001, AGH1002, AGH1003, AGH1004, AGH1005, AGH1006, AGH1007, AGH1008, AGH1009, ANZH101, ANZH104, ANZH105, ANZH203, ANZH205, ANZH301, ANZH303, ANZH304, ANZH401, ANZH404, ARFUN04, ART1003, ART1004, ART1005, ART1006 …

### #6048 · body · EXTRA · `div.col-md-8.col-12` › gold `—` vs Claude `p` — CANDIDATE
- pages 868 / modules 321 / lines 3650; consensus (all) 0.82 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 222m/722p c=0.86; Fundamentals 50m/55p c=0.22; Inquiry 35m/55p c=0.69; Bilingual 14m/36p c=0.52
- by subject: NCEA1 44m/183p c=0.80; 1-10 English 41m/97p c=0.94; 1-10 Mathematics 40m/174p c=0.85; Leaving to Learn 34m/107p c=0.81; 1-10 Blended Literacy 33m/35p c=1.00; Online Safety (OS9000) 26m/48p c=0.83
- by era: Refresh 321m/868p c=0.82
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1001** AGH1001_1_0.html ↔ AGH1001.01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Cheese»`
- **AGH1002** AGH1002_1_0.html ↔ AGH1002.01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «When the Māori people arrived in New Zealand during the late 13th century they discovered a land that was very different»`
- **AGH1003** AGH1003_3_0.html ↔ AGH1003_03.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Organic matter acts like a sponge and will hold water. This improves the of sandy soils, decreasing the rate.»`
- modules: AGH1001, AGH1002, AGH1003, AGH1004, AGH1005, AGH1006, AGH1007, AGH1008, AGH1009, ANZH101, ANZH104, ANZH105, ANZH203, ANZH205, ANZH301, ANZH303, ANZH304, ANZH401, ANZH404, ARFUN01, ARFUN02, ARFUN03, ARFUN04, ARFUN05 …

### #6049 · body · MISSING · `div#body` › gold `div.row` vs Claude `—` — CANDIDATE
- pages 1074 / modules 279 / lines 3225; consensus (all) 0.34 of 1950 gold pages with the region; derivable 0.87 (433 lines with no WT source)
- by template: Standard 243m/969p c=0.35; Bilingual 14m/50p c=0.46; Inquiry 13m/38p c=0.20; Fundamentals 9m/17p c=0.12
- by subject: 1-10 Blended Literacy 44m/61p c=0.04; NCEA1 41m/196p c=0.34; 1-10 Mathematics 40m/217p c=0.43; 1-10 English 39m/179p c=0.32; Leaving to Learn 32m/146p c=0.53; Online Safety (OS9000) 28m/87p c=0.47
- by era: Refresh 279m/1074p c=0.34
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1001** AGH1001_2_0.html ↔ AGH1001.02.html (structure, derivable=True)
  - gold: `div.row`
  - Claude: `—`
- **AGH1002** AGH1002_1_0.html ↔ AGH1002.01.html (content, derivable=True)
  - gold: `div.row  «This process of soil formation takes years and soil that is lost will take a long time to reform to replace the soil tha»`
  - Claude: `—`
  - WT: `Adding organic matter is the second stage of soil formation. As rock particles become finer, more plants start to grow and animals will appear as they now have something to eat. When plants and animal`
- **AGH1003** AGH1003_1_0.html ↔ AGH1003_01.0.html (content, derivable=True)
  - gold: `div.row  «Soil management practices are the focus of this module. They are the management practices used by farmers and growers in»`
  - Claude: `—`
  - WT: `Subject: Course: Agricultural and Horticultural Science`
- modules: AGH1001, AGH1002, AGH1003, AGH1004, AGH1005, AGH1006, AGH1007, AGH1008, AGH1009, ANZH101, ANZH104, ANZH105, ANZH203, ANZH205, ANZH303, ANZH304, ANZH401, ANZH404, ARFUN02, ART1002, ART1004, ART1005, ART1006, BLL112 …

### #6050 · body · MISSING · `div.col-md-8.col-12` › gold `p` vs Claude `—` — CANDIDATE
- pages 503 / modules 240 / lines 1068; consensus (all) 0.29 of 1950 gold pages with the region; derivable 0.83 (186 lines with no WT source)
- by template: Standard 178m/429p c=0.25; Fundamentals 34m/35p c=0.86; Inquiry 22m/27p c=0.39; Bilingual 6m/12p c=0.56
- by subject: NCEA1 40m/119p c=0.35; 1-10 English 37m/79p c=0.14; 1-10 Mathematics 35m/94p c=0.26; Leaving to Learn 28m/61p c=0.36; Online Safety (OS9000) 23m/32p c=0.38; ConnectED 16m/30p c=0.45
- by era: Refresh 240m/503p c=0.29
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1001** AGH1001_0_0.html ↔ AGH1001.00.html (content, derivable=False)
  - gold: `p  «Watch this video about turning a childhood dream into a farming reality.»`
  - Claude: `—`
- **AGH1002** AGH1002_2_0.html ↔ AGH1002.02.html (content, derivable=True)
  - gold: `p  «Let’s work through an example together based on the percentages below:»`
  - Claude: `—`
  - WT: `Let’s work through an example together based on the percentages below:`
- **AGH1003** AGH1003_3_0.html ↔ AGH1003_03.0.html (content, derivable=True)
  - gold: `p  «Soil naturally contains nutrients, although the type and amount can vary depending on the region or soil type. Low level»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] Depending on the size and complexity of your module, it may or may not be relevant for you to add additional Learning Intentions and Success Criteria to frame each lesson.   [/RED TEXT]🔴`
- modules: AGH1001, AGH1002, AGH1003, AGH1004, AGH1005, AGH1006, AGH1007, AGH1008, AGH1009, ANZH101, ANZH104, ANZH203, ANZH205, ANZH301, ANZH303, ANZH304, ANZH401, ANZH404, ARFUN01, ARFUN02, ARFUN03, ARFUN04, ARFUN05, ART1002 …

### #6051 · body · EXTRA · `div.col-md-8.col-12` › gold `—` vs Claude `img.img-fluid` — CANDIDATE
- pages 459 / modules 195 / lines 955; consensus (all) 0.97 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 134m/374p c=0.97; Fundamentals 38m/42p c=0.86; Inquiry 14m/19p c=0.91; Bilingual 9m/24p c=0.98
- by subject: NCEA1 35m/93p c=0.96; 1-10 Mathematics 30m/119p c=0.96; 1-10 English 25m/55p c=0.99; Leaving to Learn 22m/46p c=0.98; 1-10 Health and PE 14m/14p c=0.93; 1-10 Social Science 9m/18p c=0.92
- by era: Refresh 195m/459p c=0.97
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1001** AGH1001_5_0.html ↔ AGH1001.05.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- **AGH1002** AGH1002_1_0.html ↔ AGH1002.01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- **AGH1003** AGH1003_1_0.html ↔ AGH1003_01.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `img.img-fluid`
- modules: AGH1001, AGH1002, AGH1003, AGH1007, AGH1008, AGH1009, ANZH101, ANZH105, ANZH203, ANZH205, ANZH301, ANZH304, ANZH404, ARFUN01, ARFUN03, ARFUN05, ART1002, ART1003, ART1004, ART1005, ART1006, BLL111, BLL120, BLL121 …

### #6052 · body · MOVED · `div.col-md-8.col-12` › gold `p` vs Claude `p` — CANDIDATE
- pages 303 / modules 190 / lines 754; consensus (all) 0.18 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 122m/225p c=0.14; Fundamentals 39m/43p c=0.78; Inquiry 24m/28p c=0.31; Bilingual 5m/7p c=0.48
- by subject: 1-10 English 25m/40p c=0.06; 1-10 Mathematics 24m/47p c=0.15; NCEA1 22m/39p c=0.20; Leaving to Learn 20m/31p c=0.19; Online Safety (OS9000) 18m/27p c=0.17; ConnectED 15m/36p c=0.33
- by era: Refresh 190m/303p c=0.18
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1002** AGH1002_3_0.html ↔ AGH1002.03.html (structure, derivable=True)
  - gold: `p  «The following factors can impact the rate of photosynthesis:»`
  - Claude: `p  «The following factors can impact the rate of photosynthesis:»`
- **AGH1004** AGH1004_1_0.html ↔ AGH1004.02.html (structure, derivable=True)
  - gold: `p  «Watch the video below and listen for the geographical features we have already mentioned.»`
  - Claude: `p  «Watch the video below and listen for the geographical features we have already mentioned.»`
- **AGH1005** AGH1005_2_0.html ↔ AGH1005.02.html (structure, derivable=True)
  - gold: `p  «The main function of the stem is to:»`
  - Claude: `p  «The main function of the stem is to:»`
- modules: AGH1002, AGH1004, AGH1005, AGH1006, AGH1008, AGH1009, ANZH101, ANZH104, ANZH205, ANZH301, ANZH303, ANZH304, ANZH404, ARFUN01, ARFUN02, ARFUN03, ARFUN04, ARFUN05, BLL110, BLL120, BLL135, BLL157, BLL161, BLL171 …

### #6053 · body · EXTRA · `div.col-md-8.col-12` › gold `—` vs Claude `WIDGET` — CANDIDATE
- pages 269 / modules 171 / lines 523; consensus (all) 0.89 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 122m/212p c=0.91; Fundamentals 30m/30p c=0.62; Inquiry 15m/19p c=0.74; Bilingual 4m/8p c=0.98
- by subject: 1-10 English 27m/40p c=0.91; Leaving to Learn 24m/43p c=0.83; Online Safety (OS9000) 22m/38p c=0.73; NCEA1 17m/23p c=0.96; 1-10 Health and PE 14m/14p c=0.80; 1-10 Mathematics 14m/24p c=0.87
- by era: Refresh 171m/269p c=0.89
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1001** AGH1001_4_0.html ↔ AGH1001.04.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **AGH1004** AGH1004_4_0.html ↔ AGH1004.04.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **AGH1005** AGH1005_3_0.html ↔ AGH1005.03.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- modules: AGH1001, AGH1004, AGH1005, AGH1009, ANZH105, ANZH205, ANZH301, ANZH304, ARFUN01, BLL140, BLL141, BLL160, BLL210, BLL230, BLL234, BLL246, BLL253, BLL262, BLL263, BLLR201, CEDK102, CEDK501, CEDO202, CEDO301 …

### #6054 · body · SUBSTITUTED · `div.row` › gold `div.col-12` vs Claude `div.col-md-8.col-12` — CANDIDATE
- pages 285 / modules 160 / lines 351; consensus (all) 0.55 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 152m/277p c=0.55; Inquiry 5m/5p c=0.61; Fundamentals 3m/3p c=0.62
- by subject: 1-10 Blended Literacy 69m/94p c=0.52; NCEA1 20m/57p c=0.68; 1-10 English 20m/41p c=0.41; 1-10 Mathematics 12m/28p c=0.40; Online Safety (OS9000) 10m/19p c=0.52; Leaving to Learn 9m/17p c=0.79
- by era: Refresh 160m/285p c=0.55
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1001** AGH1001_1_0.html ↔ AGH1001.01.html (structure, derivable=True)
  - gold: `div.col-12  «What are primary products?»`
  - Claude: `div.col-md-8.col-12`
- **AGH1002** AGH1002_2_0.html ↔ AGH1002.02.html (structure, derivable=True)
  - gold: `div.col-12  «Soil texture»`
  - Claude: `div.col-md-8.col-12  «Soil Texture»`
- **AGH1003** AGH1003_1_0.html ↔ AGH1003_01.0.html (structure, derivable=True)
  - gold: `div.col-12  «Soil Science Recap»`
  - Claude: `div.col-md-8.col-12  «Answer the questions below.»`
- modules: AGH1001, AGH1002, AGH1003, AGH1004, AGH1007, ANZH104, ANZH205, ANZH301, ANZH304, ANZH401, ARFUN02, ART1003, BLL111, BLL112, BLL113, BLL114, BLL115, BLL116, BLL117, BLL121, BLL122, BLL123, BLL124, BLL125 …

### #6055 · body · EXTRA · `div.col-md-8.col-12` › gold `—` vs Claude `ul` — CANDIDATE
- pages 281 / modules 158 / lines 595; consensus (all) 0.96 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 112m/225p c=0.97; Fundamentals 26m/27p c=0.73; Inquiry 16m/20p c=0.90; Bilingual 4m/9p c=0.98
- by subject: NCEA1 30m/71p c=0.96; Leaving to Learn 21m/52p c=0.95; 1-10 English 20m/24p c=0.99; 1-10 Blended Literacy 16m/16p c=1.00; 1-10 Mathematics 16m/26p c=0.98; ConnectED 10m/17p c=0.97
- by era: Refresh 158m/281p c=0.96
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1001** AGH1001_1_0.html ↔ AGH1001.01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul  «Sheep and Beef»`
- **AGH1002** AGH1002_1_0.html ↔ AGH1002.01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul  «Soils importance to Māori goes back to the creation story and the first humans.»`
- **AGH1003** AGH1003_4_0.html ↔ AGH1003_04.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul  «Organic matter helps the soil structure by improving the pore spaces and the amount of water and air in the soil.»`
- modules: AGH1001, AGH1002, AGH1003, AGH1006, AGH1007, AGH1008, AGH1009, ANZH105, ANZH205, ARFUN01, ARFUN02, ARFUN04, ART1002, ART1003, ART1006, BLL113, BLL115, BLL116, BLL120, BLL131, BLL134, BLL136, BLL143, BLL146 …

### #6056 · body · EXTRA · `div.row` › gold `—` vs Claude `div.col-md-8.col-12` — CANDIDATE
- pages 240 / modules 157 / lines 314; consensus (all) 0.89 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 116m/191p c=0.92; Inquiry 22m/29p c=0.59; Fundamentals 18m/19p c=0.25; Bilingual 1m/1p c=0.95
- by subject: NCEA1 27m/44p c=0.96; 1-10 Blended Literacy 27m/31p c=0.96; 1-10 Mathematics 21m/28p c=0.90; Leaving to Learn 18m/34p c=0.91; 1-10 English 15m/22p c=0.94; ConnectED 12m/24p c=0.72
- by era: Refresh 157m/240p c=0.89
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1002** AGH1002_1_0.html ↔ AGH1002.01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-8.col-12  «Cultural Significance of Soil»`
- **AGH1003** AGH1003_5_0.html ↔ AGH1003_05.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-8.col-12  «Other than carbon, lime adds NO nutrients to the soil. Although it is applied in a similar way to fertiliser, it is not »`
- **AGH1004** AGH1004_5_0.html ↔ AGH1004.05.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-8.col-12  «Take a look at this farm and its plan to improve production through the quality of its waterways.»`
- modules: AGH1002, AGH1003, AGH1004, AGH1005, AGH1006, AGH1007, AGH1008, AGH1009, ANZH101, ANZH303, ANZH304, ANZH401, ANZH404, ARFUN01, ARFUN02, ARFUN05, ART1003, ART1005, BLL110, BLL115, BLL120, BLL121, BLL124, BLL125 …

### #6057 · body · EXTRA · `div.col-md-8.col-12` › gold `—` vs Claude `p>b` — CANDIDATE
- pages 263 / modules 156 / lines 628; consensus (all) 0.95 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 117m/211p c=0.97; Inquiry 15m/17p c=0.91; Fundamentals 13m/13p c=0.84; Bilingual 11m/22p c=0.73
- by subject: 1-10 Blended Literacy 37m/37p c=1.00; 1-10 Mathematics 21m/64p c=0.97; NCEA1 15m/25p c=0.95; Leaving to Learn 15m/29p c=0.93; 1-10 English 14m/26p c=0.98; Te Marautanga o Aotearoa TMoA 11m/22p c=0.73
- by era: Refresh 156m/263p c=0.95
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1003** AGH1003_3_0.html ↔ AGH1003_03.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «When broken down this will add nutrients, increasing the of soils»`
- **AGH1005** AGH1005_3_0.html ↔ AGH1005.03.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Tick ✔»`
- **AGH1009** AGH1009_2_0.html ↔ AGH1009.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Nitrogen gas (N2) from the atmosphere is converted into ammonia (NH3) or related compounds through nitrogen fixation.»`
- modules: AGH1003, AGH1005, AGH1009, ANZH104, ANZH105, ANZH203, ANZH205, ANZH404, ARFUN02, ART1002, ART1005, BLL110, BLL112, BLL122, BLL130, BLL140, BLL143, BLL150, BLL152, BLL154, BLL156, BLL157, BLL160, BLL161 …

### #6058 · body · MISSING · `div.col-md-8.col-12` › gold `WIDGET` vs Claude `—` — CANDIDATE
- pages 229 / modules 140 / lines 372; consensus (all) 0.19 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 109m/193p c=0.18; Inquiry 15m/20p c=0.33; Fundamentals 13m/13p c=0.47; Bilingual 3m/3p c=0.08
- by subject: 1-10 Mathematics 26m/61p c=0.22; 1-10 English 23m/31p c=0.20; NCEA1 20m/35p c=0.09; Leaving to Learn 19m/32p c=0.25; Online Safety (OS9000) 14m/22p c=0.51; None 6m/9p c=0.48
- by era: Refresh 140m/229p c=0.19
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1002** AGH1002_1_0.html ↔ AGH1002.01.html (structure, derivable=True)
  - gold: `WIDGET`
  - Claude: `—`
- **AGH1003** AGH1003_4_0.html ↔ AGH1003_04.0.html (structure, derivable=True)
  - gold: `WIDGET`
  - Claude: `—`
- **AGH1005** AGH1005_3_0.html ↔ AGH1005.03.html (structure, derivable=True)
  - gold: `WIDGET`
  - Claude: `—`
- modules: AGH1002, AGH1003, AGH1005, AGH1006, AGH1007, AGH1008, AGH1009, ANZH104, ANZH301, ANZH304, ARFUN02, BLL130, BLL150, BLL210, BLLR201, CEDK501, CEDO102, CEDO501, CEDR501, CEDT501, CHFUN04, CHFUN05, CHFUN06, ENFUN01 …

### #6059 · body · EXTRA · `div.col-md-8.col-12` › gold `—` vs Claude `h3` — CANDIDATE
- pages 211 / modules 140 / lines 255; consensus (all) 0.72 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 103m/162p c=0.75; Bilingual 14m/25p c=0.49; Fundamentals 12m/12p c=0.14; Inquiry 11m/12p c=0.70
- by subject: 1-10 Mathematics 26m/44p c=0.72; NCEA1 20m/29p c=0.72; 1-10 Blended Literacy 20m/20p c=1.00; Leaving to Learn 17m/31p c=0.66; Te Marautanga o Aotearoa TMoA 14m/25p c=0.49; ConnectED 10m/11p c=0.59
- by era: Refresh 140m/211p c=0.72
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1004** AGH1004_1_0.html ↔ AGH1004.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h3  «Knowledge Self-check»`
- **AGH1007** AGH1007_9_0.html ↔ AGH1007.09.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h3  «Bacteria»`
- **AGH1008** AGH1008_2_0.html ↔ AGH1008.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h3  «Digestibility of feed»`
- modules: AGH1004, AGH1007, AGH1008, AGH1009, ANZH104, ANZH301, ANZH303, ANZH304, ARFUN03, ARFUN04, ART1005, BLL111, BLL114, BLL115, BLL116, BLL117, BLL121, BLL131, BLL132, BLL133, BLL134, BLL135, BLL136, BLL137 …

### #6062 · body · MISSING · `div.col-md-8.col-12` › gold `h3` vs Claude `—` — CANDIDATE
- pages 218 / modules 129 / lines 313; consensus (all) 0.17 of 1950 gold pages with the region; derivable 0.92 (25 lines with no WT source)
- by template: Standard 92m/175p c=0.14; Fundamentals 21m/21p c=0.75; Inquiry 11m/16p c=0.20; Bilingual 5m/6p c=0.30
- by subject: 1-10 Mathematics 22m/34p c=0.14; NCEA1 18m/36p c=0.14; 1-10 English 17m/21p c=0.11; Leaving to Learn 14m/29p c=0.19; ConnectED 10m/22p c=0.30; Online Safety (OS9000) 10m/12p c=0.18
- by era: Refresh 129m/218p c=0.17
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1003** AGH1003_2_0.html ↔ AGH1003_02.0.html (content, derivable=True)
  - gold: `h3  «Irrigation and physical properties of soil»`
  - Claude: `—`
  - WT: `• *I can explain how soil management practices alter physical, chemical, and biological properties of soil.*`
- **AGH1005** AGH1005_1_0.html ↔ AGH1005.01.html (content, derivable=True)
  - gold: `h3  «Mauri model»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [H2]  [/RED TEXT]🔴*Lesson 1: Exploring the Mauri Model and interrelationships between plants and primary production systems*`
- **AGH1006** AGH1006_3_0.html ↔ AGH1006.04.html (content, derivable=True)
  - gold: `h3  «Crop rotation»`
  - Claude: `—`
  - WT: `│ [IMAGE: image14.png] ║ **Crop Rotation:** Implement crop rotation cycles to break pest and disease cycles, improve soil fertility, and reduce the need for chemical inputs.`
- modules: AGH1003, AGH1005, AGH1006, AGH1009, ANZH101, ANZH104, ANZH301, ANZH304, ANZH401, ARFUN02, ARFUN03, ARFUN04, BLL240, BLLR201, CEDK102, CEDK501, CEDO102, CEDO301, CEDO501, CEDO502, CEDR501, CEDT104, CEDT501, CEDW501 …

### #6065 · body · EXTRA · `div.col-md-8.col-12` › gold `—` vs Claude `a` — CANDIDATE
- pages 190 / modules 107 / lines 297; consensus (all) 0.98 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 84m/165p c=0.98; Fundamentals 17m/17p c=0.97; Inquiry 6m/8p c=0.98
- by subject: NCEA1 20m/45p c=0.98; 1-10 Mathematics 18m/36p c=0.97; 1-10 English 15m/23p c=0.99; Leaving to Learn 10m/14p c=0.94; 1-10 Health and PE 9m/9p c=1.00; ConnectED 6m/28p c=1.00
- by era: Refresh 107m/190p c=0.98
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1003** AGH1003_1_0.html ↔ AGH1003_01.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `a  «Need some extra help? Have a look at FUNdamentals 05»`
- **AGH1004** AGH1004_1_0.html ↔ AGH1004.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `a  «Complete activity 1A in your learning journal»`
- **AGH1005** AGH1005_3_0.html ↔ AGH1005.03.html (structure, derivable=True)
  - gold: `—`
  - Claude: `a  «Complete activity 3A in your learning journal»`
- modules: AGH1003, AGH1004, AGH1005, AGH1006, AGH1008, AGH1009, ANZH205, ANZH404, BLL115, BLL116, BLL123, BLL157, BLL164, CEDK501, CEDO501, CEDO502, CEDR501, CEDT501, CEDW501, ENFUN03, ENFUN09, ENGC301, ENGC302, ENGI102 …

### #6067 · body · EXTRA · `div.col-md-8.col-12` › gold `—` vs Claude `div.videoSection.ratio.ratio-16x9` — CANDIDATE
- pages 176 / modules 103 / lines 226; consensus (all) 0.94 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 74m/140p c=0.94; Inquiry 12m/16p c=0.89; Fundamentals 9m/10p c=0.94; Bilingual 8m/10p c=0.95
- by subject: 1-10 Mathematics 28m/61p c=0.95; 1-10 English 18m/32p c=0.97; Leaving to Learn 15m/32p c=0.92; ConnectED 10m/12p c=0.90; Online Safety (OS9000) 8m/12p c=0.81; Te Marautanga o Aotearoa TMoA 8m/10p c=0.95
- by era: Refresh 103m/176p c=0.94
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:43 — | Video wrapper | `embed-responsive embed-responsive-16by9` | `ratio ratio-16x9` |
  - KB: 06_TEMPLATE_RECOGNITION.md:374 — <div class="videoSection ratio ratio-16x9">
  - KB: 01_PIPELINE_EXTRACTION_TAGS/01E_TAG_INTERPRETATION.md:59 — <div class="videoSection ratio ratio-16x9">
- **AGH1001** AGH1001_5_0.html ↔ AGH1001.05.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.videoSection.ratio.ratio-16x9`
- **AGH1008** AGH1008_7_0.html ↔ AGH1008.07.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.videoSection.ratio.ratio-16x9`
- **ARFUN04** ARFUN04_0_0.html ↔ ARFUN04_0.00.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.videoSection.ratio.ratio-16x9`
- modules: AGH1001, AGH1008, ARFUN04, BLL234, BLL240, CEDO105, CEDO301, CEDO501, CEDR204, CEDR501, CEDT101, CEDT207, CEDT404, CEDT501, CEDW101, ENGC101, ENGC102, ENGC201, ENGC202, ENGC301, ENGC302, ENGI301, ENGI303, ENGI405 …

### #6068 · body · EXTRA · `div.col-md-8.col-12` › gold `—` vs Claude `div.table-responsive` — CANDIDATE
- pages 174 / modules 103 / lines 233; consensus (all) 0.98 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 84m/152p c=0.99; Fundamentals 10m/10p c=0.91; Inquiry 9m/12p c=0.97
- by subject: 1-10 Mathematics 24m/50p c=0.96; 1-10 English 19m/25p c=0.99; NCEA1 17m/28p c=0.99; Leaving to Learn 10m/16p c=1.00; ConnectED 6m/26p c=0.93; Online Safety (OS9000) 5m/5p c=1.00
- by era: Refresh 103m/174p c=0.98
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1001** AGH1001_2_0.html ↔ AGH1001.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.table-responsive  «Image»`
- **AGH1003** AGH1003_2_0.html ↔ AGH1003_02.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.table-responsive  «are large irrigators which are used on large pastoral production systems like dairy farms, sheep and beef farms or arabl»`
- **AGH1004** AGH1004_5_0.html ↔ AGH1004.05.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.table-responsive  «Positive Impact»`
- modules: AGH1001, AGH1003, AGH1004, AGH1005, AGH1006, AGH1007, AGH1008, AGH1009, ANZH104, ANZH105, ANZH205, ART1005, BLL210, BLL216, BLL234, BLL235, CEDK501, CEDO501, CEDO502, CEDR501, CEDT501, CEDW501, ENFUN01, ENFUN03 …

### #6070 · body · EXTRA · `p>b` › gold `—` vs Claude `b` — CANDIDATE
- pages 152 / modules 96 / lines 216; consensus (all) 0.91 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 79m/131p c=0.93; Fundamentals 8m/8p c=0.73; Bilingual 6m/10p c=0.67; Inquiry 3m/3p c=0.87
- by subject: NCEA1 17m/30p c=0.93; 1-10 Mathematics 17m/30p c=0.94; Online Safety (OS9000) 14m/15p c=0.89; Leaving to Learn 13m/26p c=0.90; 1-10 English 6m/6p c=0.93; Te Marautanga o Aotearoa TMoA 6m/10p c=0.67
- by era: Refresh 96m/152p c=0.91
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1001** AGH1001_2_0.html ↔ AGH1001.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `b  «Timeline of primary production in Aotearoa:»`
- **AGH1002** AGH1002_2_0.html ↔ AGH1002.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `b  «loam soil.»`
- **AGH1003** AGH1003_2_0.html ↔ AGH1003_02.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `b  «drainage»`
- modules: AGH1001, AGH1002, AGH1003, AGH1005, AGH1006, AGH1008, AGH1009, ANZH101, ANZH203, ANZH301, ANZH303, ANZH404, ARFUN02, ARFUN04, ART1002, BLL142, CEDO501, CEDR501, CEDT104, CEDW501, CHFUN01, ENGC301, ENGI303, ENGI400 …

### #6072 · body · EXTRA · `a` › gold `—` vs Claude `div.button` — CANDIDATE
- pages 170 / modules 88 / lines 311; consensus (all) 0.97 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 68m/143p c=0.96; Fundamentals 11m/11p c=0.98; Inquiry 9m/16p c=0.97
- by subject: Leaving to Learn 15m/38p c=0.91; NCEA1 12m/20p c=0.98; 1-10 Mathematics 12m/27p c=0.97; 1-10 English 10m/11p c=0.98; ConnectED 8m/33p c=0.94; EXPlore 6m/9p c=0.67
- by era: Refresh 88m/170p c=0.97
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1001** AGH1001_4_0.html ↔ AGH1001.04.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.button  «Complete activity 4A and 4B in your Learners Journal»`
- **AGH1004** AGH1004_3_0.html ↔ AGH1004.03.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.button  «Complete activity 3B in your learning journal»`
- **AGH1005** AGH1005_4_0.html ↔ AGH1005.04.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.button  «Complete activity 4A in your learning journal»`
- modules: AGH1001, AGH1004, AGH1005, AGH1006, ANZH303, ANZH401, ANZH404, ARFUN01, ARFUN04, BLL113, BLL114, BLL117, BLL131, BLL141, CEDK102, CEDK501, CEDO501, CEDO502, CEDR501, CEDT104, CEDT501, CEDW501, ENFUN08, ENFUN09 …

### #6073 · body · EXTRA · `div.col-md-8.col-12` › gold `—` vs Claude `h4` — CANDIDATE
- pages 117 / modules 87 / lines 170; consensus (all) 0.98 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 50m/77p c=0.99; Fundamentals 21m/21p c=0.80; Inquiry 8m/8p c=0.98; Bilingual 8m/11p c=0.89
- by subject: Leaving to Learn 12m/16p c=0.98; NCEA1 11m/17p c=0.99; 1-10 Mathematics 10m/16p c=0.99; 1-10 English 9m/10p c=0.98; 1-10 Health and PE 9m/9p c=1.00; Te Marautanga o Aotearoa TMoA 8m/11p c=0.89
- by era: Refresh 87m/117p c=0.98
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1009** AGH1009_8_0.html ↔ AGH1009.03.1.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h4  «Know your numbers»`
- **ANZH101** ANZH101_2_0.html ↔ ANZH101_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h4  «Te Waka o Aoraki»`
- **ANZH301** ANZH301_1_0.html ↔ ANZH301_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h4  «Can statistics tell a part of this story?»`
- modules: AGH1009, ANZH101, ANZH301, ANZH303, ANZH304, ARFUN02, ARFUN04, ARFUN05, CEDR501, CEDT104, CEDT501, ENFUN02, ENFUN03, ENFUN09, ENGI102, ENGI203, ENGI405, ENGJ402, ENGR102, ENGR302, EXBP901, EXIP901, EXPFUN03, EXPFUN04 …

### #6075 · body · EXTRA · `div.col-md-8.col-12` › gold `—` vs Claude `p>a` — CANDIDATE
- pages 126 / modules 83 / lines 218; consensus (all) 0.99 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 62m/103p c=0.99; Inquiry 11m/12p c=0.98; Fundamentals 9m/9p c=0.95; Bilingual 1m/2p c=0.98
- by subject: 1-10 English 14m/17p c=1.00; 1-10 Mathematics 13m/26p c=1.00; NCEA1 12m/22p c=0.98; ConnectED 8m/19p c=0.99; Leaving to Learn 6m/8p c=0.98; ANZH 5m/8p c=1.00
- by era: Refresh 83m/126p c=0.99
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1001** AGH1001_3_0.html ↔ AGH1001.03.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Kiwi Kai interactive game»`
- **AGH1008** AGH1008_8_0.html ↔ AGH1008.08.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «&list=PLz0cBEzB_J_KI_XQbQRr0E7KTqyj_YL7a&index=2&ab_channel=OSPRI»`
- **ANZH104** ANZH104_1_0.html ↔ ANZH104_01.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Edit: trigger hover translation “ngā manu’': text (Birds) and if possible, also audio, like in French000»`
- modules: AGH1001, AGH1008, ANZH104, ANZH203, ANZH303, ANZH304, ANZH404, ARFUN02, ARFUN03, ARFUN04, BLL152, BLL234, BLL236, BLL254, BLL263, CEDK501, CEDO202, CEDO501, CEDO502, CEDT104, CEDT404, CEDT501, CEDW501, CHFUN05 …

### #6079 · body · EXTRA · `p` › gold `—` vs Claude `b` — CANDIDATE
- pages 99 / modules 79 / lines 237; consensus (all) 0.93 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 66m/84p c=0.94; Fundamentals 7m/7p c=0.73; Bilingual 4m/6p c=0.78; Inquiry 2m/2p c=0.94
- by subject: NCEA1 14m/17p c=0.96; 1-10 Mathematics 14m/15p c=0.90; 1-10 English 11m/11p c=0.94; Leaving to Learn 10m/14p c=0.94; Online Safety (OS9000) 6m/8p c=0.92; 1-10 Blended Literacy 5m/5p c=0.99
- by era: Refresh 79m/99p c=0.93
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1001** AGH1001_2_0.html ↔ AGH1001.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `b  «income»`
- **AGH1003** AGH1003_5_0.html ↔ AGH1003_05.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `b  «nutrient status»`
- **AGH1005** AGH1005_4_0.html ↔ AGH1005.04.html (structure, derivable=True)
  - gold: `—`
  - Claude: `b  «photosynthesis»`
- modules: AGH1001, AGH1003, AGH1005, AGH1006, ART1003, BLL143, BLL152, BLL173, BLL177, BLL244, BLLR201, CEDO501, CEDO502, CEDR501, CEDW501, CHFUN01, CHFUN05, ENGC401, ENGI103, ENGI303, ENGI400, ENGI401, ENGJ301, ENGJ302 …

### #6080 · body · SUBSTITUTED · `div.col-md-8.col-12` › gold `h3` vs Claude `h4` — CANDIDATE
- pages 112 / modules 76 / lines 181; consensus (all) 0.48 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 51m/87p c=0.46; Fundamentals 20m/20p c=0.92; Inquiry 4m/4p c=0.53; Bilingual 1m/1p c=0.51
- by subject: 1-10 English 18m/21p c=0.51; 1-10 Mathematics 10m/16p c=0.50; Leaving to Learn 9m/15p c=0.53; 1-10 Health and PE 7m/7p c=0.93; NCEA1 6m/6p c=0.47; ConnectED 4m/9p c=0.67
- by era: Refresh 76m/112p c=0.48
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1006** AGH1006_5_0.html ↔ AGH1006.06.html (structure, derivable=True)
  - gold: `h3  «Pruning»`
  - Claude: `h4  «Evergreen Shrubs»`
- **AGH1009** AGH1009_2_0.html ↔ AGH1009.02.html (structure, derivable=True)
  - gold: `h3  «Nutrient cycling»`
  - Claude: `h4  «Nutrient cycling»`
- **ANZH101** ANZH101_2_0.html ↔ ANZH101_2.0.html (structure, derivable=True)
  - gold: `h3  «Te Waka o Aoraki»`
  - Claude: `h4  «Ranginui and Papatūānuku»`
- modules: AGH1006, AGH1009, ANZH101, ANZH404, ARFUN02, ARFUN05, CEDO501, CEDO502, CEDT501, CEDW501, ENFUN01, ENFUN02, ENFUN04, ENFUN07, ENGFUN02, ENGI102, ENGI202, ENGI302, ENGI400, ENGI405, ENGJ301, ENGJ402, ENGR202, ENGR301 …

### #6082 · body · EXTRA · `div.table-responsive` › gold `—` vs Claude `table.table.table-bordered` — CANDIDATE
- pages 118 / modules 73 / lines 133; consensus (all) 0.96 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 64m/105p c=0.97; Inquiry 4m/8p c=0.91; Fundamentals 3m/3p c=0.91; Bilingual 2m/2p c=1.00
- by subject: 1-10 English 14m/20p c=0.94; 1-10 Mathematics 14m/25p c=0.93; NCEA1 10m/15p c=0.98; Leaving to Learn 8m/13p c=0.99; ConnectED 7m/25p c=0.95; Online Safety (OS9000) 7m/7p c=0.95
- by era: Refresh 73m/118p c=0.96
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:407 — <div class="table-responsive">
  - KB: 18_ASSESSMENT_MODE.md:220 — <table class="table table-bordered" style="margin-bottom: 30px;">…</table>
  - KB: 18_ASSESSMENT_MODE.md:245 — 1. every content table: `<table class="table table-bordered" style="margin-bottom: 30px;">` — Bootstrap's table classes (the page already uses Bootstr
- **AGH1001** AGH1001_5_0.html ↔ AGH1001.05.html (structure, derivable=True)
  - gold: `—`
  - Claude: `table.table.table-bordered  «Milking – using machinery to take milk from a cow’s udder.»`
- **AGH1002** AGH1002_3_0.html ↔ AGH1002.03.html (structure, derivable=True)
  - gold: `—`
  - Claude: `table.table.table-bordered  «Carbon dioxide»`
- **AGH1003** AGH1003_1_0.html ↔ AGH1003_01.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `table.table.table-bordered  «Before Europeans arrived, Māori hunted the moa bird to extinction and burnt large areas of forest.»`
- modules: AGH1001, AGH1002, AGH1003, AGH1004, AGH1005, AGH1007, AGH1008, AGH1009, ANZH104, BLL162, BLL245, CEDK501, CEDO501, CEDO502, CEDR501, CEDT104, CEDT501, CEDW501, CHFUN05, ENGC202, ENGC302, ENGC401, ENGI102, ENGI103 …

### #6083 · body · EXTRA · `p>i` › gold `—` vs Claude `i` — CANDIDATE
- pages 98 / modules 73 / lines 118; consensus (all) 0.97 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 69m/93p c=0.97; Inquiry 2m/3p c=0.97; Bilingual 1m/1p c=0.98; Fundamentals 1m/1p c=0.97
- by subject: 1-10 Blended Literacy 26m/26p c=1.00; NCEA1 11m/18p c=0.98; 1-10 English 9m/14p c=0.94; 1-10 Mathematics 9m/14p c=0.99; ANZH 4m/7p c=0.99; Online Safety (OS9000) 4m/4p c=0.97
- by era: Refresh 73m/98p c=0.97
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1005** AGH1005_1_0.html ↔ AGH1005.01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `i  «Taiao ora, whenua ora, tāngata ora – healthy nature, healthy land, healthy people. When the environment and the land are»`
- **ANZH104** ANZH104_0_0.html ↔ ANZH104_00.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `i  «The ways different groups of people have lived and worked in this rohe have changed over time.»`
- **ANZH203** ANZH203_1_0.html ↔ ANZH203_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `i  «Heemskerck»`
- modules: AGH1005, ANZH104, ANZH203, ANZH301, ANZH404, BLL114, BLL115, BLL116, BLL117, BLL124, BLL131, BLL132, BLL133, BLL134, BLL135, BLL136, BLL137, BLL142, BLL144, BLL153, BLL154, BLL156, BLL157, BLL161 …

### #6088 · body · EXTRA · `div.col-md-8.col-12` › gold `—` vs Claude `ol` — CANDIDATE
- pages 99 / modules 68 / lines 192; consensus (all) 0.99 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 53m/84p c=0.99; Inquiry 8m/8p c=0.99; Fundamentals 6m/6p c=0.98; Bilingual 1m/1p c=0.98
- by subject: 1-10 Mathematics 13m/24p c=0.99; NCEA1 12m/23p c=0.99; 1-10 Blended Literacy 9m/9p c=1.00; 1-10 English 9m/14p c=0.99; Leaving to Learn 7m/8p c=0.99; ConnectED 5m/7p c=1.00
- by era: Refresh 68m/99p c=0.99
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1001** AGH1001_3_0.html ↔ AGH1001.03.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ol  «Kaitiakitanga is about guardianship over the land »`
- **AGH1002** AGH1002_4_0.html ↔ AGH1002.04.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ol  «Drainage»`
- **AGH1003** AGH1003_3_0.html ↔ AGH1003_03.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ol  «they know what nutrients they are adding»`
- modules: AGH1001, AGH1002, AGH1003, AGH1005, ANZH105, ANZH205, ART1006, BLL111, BLL112, BLL113, BLL114, BLL115, BLL116, BLL117, BLL120, BLL253, CEDK501, CEDO202, CEDO501, CEDT104, CEDT404, CHFUN06, ENFUN07, ENGC202 …

### #6089 · body · SUBSTITUTED · `div.videoSection.icon.ratio.ratio-16x9` › gold `iframe.embed-responsive-item` vs Claude `iframe` — CANDIDATE
- pages 172 / modules 66 / lines 210; consensus (all) 0.21 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 54m/157p c=0.22; Fundamentals 10m/10p c=0.39; Inquiry 2m/5p c=0.22
- by subject: 1-10 Mathematics 20m/47p c=0.39; 1-10 English 18m/37p c=0.24; NCEA1 15m/63p c=0.42; ANZH 3m/6p c=0.15; ConnectED 3m/9p c=0.17; 1-10 Social Science 3m/3p c=0.24
- by era: Refresh 66m/172p c=0.21
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:43 — | Video wrapper | `embed-responsive embed-responsive-16by9` | `ratio ratio-16x9` |
  - KB: 06_TEMPLATE_RECOGNITION.md:374 — <div class="videoSection ratio ratio-16x9">
  - KB: INDEX.md:160 — - **`14_SUBJECT_GLOBAL_PARAMETERS/14D_SGP_CROSSCUTTING_AND_TECHNOLOGY.md`** (6 KB) — Cross-cutting notes (14.11) and the Technology family (14.12 — fi
- **AGH1003** AGH1003_2_0.html ↔ AGH1003_02.0.html (structure, derivable=True)
  - gold: `iframe.embed-responsive-item`
  - Claude: `iframe`
- **AGH1008** AGH1008_3_0.html ↔ AGH1008.03.html (structure, derivable=True)
  - gold: `iframe.embed-responsive-item`
  - Claude: `iframe`
- **AGH1009** AGH1009_3_0.html ↔ AGH1009.03.0.html (structure, derivable=True)
  - gold: `iframe.embed-responsive-item`
  - Claude: `iframe`
- modules: AGH1003, AGH1008, AGH1009, ANZH101, ANZH203, ANZH205, CEDO105, CEDT207, CEDT301, ENFUN01, ENFUN02, ENFUN03, ENFUN04, ENFUN05, ENFUN08, ENFUN09, ENGC201, ENGI102, ENGI201, ENGI202, ENGI203, ENGI303, ENGJ201, ENGR102 …

### #6092 · body · EXTRA · `table.table.table-bordered` › gold `—` vs Claude `tr` — CANDIDATE
- pages 98 / modules 63 / lines 269; consensus (all) 0.98 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 54m/87p c=0.99; Inquiry 5m/7p c=0.93; Fundamentals 4m/4p c=0.94
- by subject: 1-10 Mathematics 20m/33p c=0.98; 1-10 English 11m/13p c=0.97; NCEA1 9m/17p c=0.99; ConnectED 6m/14p c=0.98; Leaving to Learn 5m/6p c=0.99; None 3m/6p c=0.94
- by era: Refresh 63m/98p c=0.98
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 18_ASSESSMENT_MODE.md:220 — <table class="table table-bordered" style="margin-bottom: 30px;">…</table>
  - KB: 18_ASSESSMENT_MODE.md:245 — 1. every content table: `<table class="table table-bordered" style="margin-bottom: 30px;">` — Bootstrap's table classes (the page already uses Bootstr
  - KB: _project_instructions_.md:28 — - **`ASSESSMENT MODE`** phrase (any capitalisation), **or** an uploaded `.docx` that is an **NCEA Assessment Activity** document (details table `Activ
- **AGH1002** AGH1002_1_0.html ↔ AGH1002.01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `tr  «Soils from areas where the water table is high are more likely to have higher levels of water and lower levels of air. T»`
- **AGH1003** AGH1003_2_0.html ↔ AGH1003_02.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `tr  «are large irrigators which are used on large pastoral production systems like dairy farms, sheep and beef farms or arabl»`
- **AGH1006** AGH1006_6_0.html ↔ AGH1006.07.html (structure, derivable=True)
  - gold: `—`
  - Claude: `tr  «Paspalum (Kikuyu)»`
- modules: AGH1002, AGH1003, AGH1006, AGH1007, AGH1008, ARFUN03, BLLR201, CEDK501, CEDO501, CEDO502, CEDR501, CEDT501, CEDW501, CHFUN05, ENGC202, ENGI102, ENGI303, ENGI405, ENGJ201, ENGJ301, ENGJ403, ENGR201, ENGR301, ENGS301 …

### #6094 · body · EXTRA · `div.col-md-8.col-12` › gold `—` vs Claude `p>i` — CANDIDATE
- pages 89 / modules 63 / lines 153; consensus (all) 0.98 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 54m/80p c=0.98; Inquiry 4m/4p c=0.97; Fundamentals 3m/3p c=0.97; Bilingual 2m/2p c=0.95
- by subject: NCEA1 15m/23p c=0.99; 1-10 Mathematics 11m/18p c=1.00; 1-10 English 10m/14p c=0.96; Leaving to Learn 9m/12p c=0.99; ANZH 5m/7p c=0.99; 1-10 Social Science 3m/4p c=0.97
- by era: Refresh 63m/89p c=0.98
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH101** ANZH101_2_0.html ↔ ANZH101_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «(Creative Services – can we embed the Google Slides into this module?)»`
- **ANZH105** ANZH105_2_0.html ↔ ANZH105_02.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «The Way It Was»`
- **ANZH203** ANZH203_1_0.html ↔ ANZH203_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Section 1.0 – First Europeans – Te Ara Tipu (desire2learn.com)»`
- modules: ANZH101, ANZH105, ANZH203, ANZH303, ANZH304, ART1003, ART1005, BLL116, CEDT301, CEDT404, ENFUN04, ENG1004, ENGI102, ENGI202, ENGJ302, ENGJ402, ENGR102, ENGR302, ENGS101, ENGS102, ENGS302, EXBP901, HES1006, HIS1001 …

### #6096 · body · EXTRA · `div.col-md-8.col-12` › gold `—` vs Claude `audio.audioPlayer.icon` — CANDIDATE
- pages 106 / modules 62 / lines 232; consensus (all) 1.00 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 41m/76p c=1.00; Inquiry 11m/11p c=1.00; Bilingual 9m/18p c=1.00; Fundamentals 1m/1p c=1.00
- by subject: 1-10 Blended Literacy 22m/22p c=1.00; Leaving to Learn 18m/34p c=1.00; Te Marautanga o Aotearoa TMoA 9m/18p c=1.00; ConnectED 4m/10p c=0.98; 1-10 English 4m/4p c=0.99; 1-10 Mathematics 3m/16p c=1.00
- by era: Refresh 62m/106p c=1.00
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:381 — <audio preload="none" class="audioPlayer" title="...">
  - KB: INDEX.md:159 — - Sections: 14C — Languages Audiovisual Package: the complete asset registry · 1. Delivery forms (the supplied markup shapes) · 2. Language icons · 3.
  - KB: 00_MASTER_INSTRUCTIONS/00C_FILE_REFERENCE_INDEX.md:26 — | Subject Global Parameters | `14_SUBJECT_GLOBAL_PARAMETERS.md` | The design team's per-subject **global-parameter** conventions, folded in so the Con
- **ANZH105** ANZH105_2_0.html ↔ ANZH105_02.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `audio.audioPlayer.icon`
- **BLL110** BLL110_0_0.html ↔ BLL110.html (structure, derivable=True)
  - gold: `—`
  - Claude: `audio.audioPlayer.icon`
- **BLL120** BLL120_0_0.html ↔ BLL120.html (structure, derivable=True)
  - gold: `—`
  - Claude: `audio.audioPlayer.icon`
- modules: ANZH105, BLL110, BLL120, BLL123, BLL130, BLL133, BLL140, BLL146, BLL150, BLL157, BLL160, BLL161, BLL162, BLL170, BLL211, BLL220, BLL226, BLL235, BLL242, BLL244, BLL245, BLL246, BLL251, CEDK501 …

### #6099 · body · EXTRA · `div.row` › gold `—` vs Claude `div.col-12` — CANDIDATE
- pages 110 / modules 60 / lines 140; consensus (all) 0.84 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 41m/89p c=0.84; Fundamentals 12m/14p c=0.67; Inquiry 7m/7p c=0.76
- by subject: 1-10 English 9m/11p c=0.90; Leaving to Learn 9m/23p c=0.83; 1-10 Mathematics 8m/17p c=0.93; Online Safety (OS9000) 6m/11p c=0.87; NCEA1 4m/5p c=0.81; ANZH 4m/20p c=0.87
- by era: Refresh 60m/110p c=0.84
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1004** AGH1004_2_0.html ↔ AGH1004.06.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12  «Key points from the lesson:»`
- **ANZH105** ANZH105_6_0.html ↔ ANZH105_06.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12  «Stories are organised by difficulty. Use the available audio clips to support reading the text.»`
- **ANZH303** ANZH303_2_0.html ↔ ANZH303_0.2.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-12  «Lesson summary:»`
- modules: AGH1004, ANZH105, ANZH303, ANZH304, ANZH401, ARFUN01, BLL110, BLL130, CEDK102, CEDO105, CEDT207, CEDT501, ENFUN01, ENFUN02, ENFUN04, ENGC101, ENGI201, ENGI203, ENGJ201, ENGS101, ENGS302, EXBP901, EXIP901, HIS1004 …

### #6101 · body · EXTRA · `div.videoSection.ratio.ratio-16x9` › gold `—` vs Claude `iframe` — CANDIDATE
- pages 80 / modules 60 / lines 82; consensus (all) 0.93 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 50m/67p c=0.94; Inquiry 6m/8p c=0.87; Fundamentals 4m/5p c=0.92
- by subject: 1-10 Mathematics 16m/25p c=0.95; 1-10 English 13m/14p c=0.94; Leaving to Learn 12m/19p c=0.92; ConnectED 8m/9p c=0.90; NCEA1 4m/5p c=0.96; Online Safety (OS9000) 3m/3p c=0.82
- by era: Refresh 60m/80p c=0.93
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:43 — | Video wrapper | `embed-responsive embed-responsive-16by9` | `ratio ratio-16x9` |
  - KB: 06_TEMPLATE_RECOGNITION.md:374 — <div class="videoSection ratio ratio-16x9">
  - KB: 01_PIPELINE_EXTRACTION_TAGS/01E_TAG_INTERPRETATION.md:59 — <div class="videoSection ratio ratio-16x9">
- **AGH1003** AGH1003_3_0.html ↔ AGH1003_03.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `iframe`
- **AGH1008** AGH1008_6_0.html ↔ AGH1008.06.html (structure, derivable=True)
  - gold: `—`
  - Claude: `iframe`
- **AGH1009** AGH1009_7_0.html ↔ AGH1009.07.html (structure, derivable=True)
  - gold: `—`
  - Claude: `iframe`
- modules: AGH1003, AGH1008, AGH1009, CEDK501, CEDO102, CEDO501, CEDR501, CEDT208, CEDT301, CEDW201, CEDW501, ENGC102, ENGC201, ENGC401, ENGI405, ENGJ101, ENGJ201, ENGJ301, ENGR101, ENGR102, ENGR201, ENGR302, ENGS102, ENGS201 …

### #6107 · body · EXTRA · `ul` › gold `—` vs Claude `li` — CANDIDATE
- pages 68 / modules 56 / lines 230; consensus (all) 0.93 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 37m/49p c=0.94; Inquiry 10m/10p c=0.87; Fundamentals 8m/8p c=0.62; Bilingual 1m/1p c=0.98
- by subject: NCEA1 10m/15p c=0.91; Leaving to Learn 9m/13p c=0.91; 1-10 English 6m/6p c=0.97; 1-10 Mathematics 5m/6p c=0.98; Online Safety (OS9000) 5m/6p c=0.95; ConnectED 4m/4p c=0.90
- by era: Refresh 56m/68p c=0.93
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1004** AGH1004_1_0.html ↔ AGH1004.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `li  «New Zealand’s agricultural and horticultural regions have influenced and shaped what is grown for primary production.»`
- **AGH1006** AGH1006_0_0.html ↔ AGH1006.00.html (structure, derivable=True)
  - gold: `—`
  - Claude: `li  «Propagation techniques such as seed sowing, cuttings and grafting.»`
- **AGH1009** AGH1009_2_0.html ↔ AGH1009.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `li  «The natural environment is made up of living organisms and nonliving factors working together.»`
- modules: AGH1004, AGH1006, AGH1009, ANZH303, BLL153, CEDK501, CEDO501, CEDO502, CEDT104, ENFUN01, ENFUN03, ENFUN09, ENG1005, ENGI201, ENGJ301, ENGJ402, EXPFUN02, EXPFUN03, EXPFUN04, EXPFUN06, HES1005, HIS1004, HIS1005, HIS1007 …

### #6110 · body · EXTRA · `p>a` › gold `—` vs Claude `a` — CANDIDATE
- pages 62 / modules 54 / lines 76; consensus (all) 0.99 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 36m/44p c=1.00; Fundamentals 11m/11p c=0.95; Inquiry 7m/7p c=0.99
- by subject: NCEA1 8m/10p c=1.00; 1-10 Mathematics 8m/8p c=1.00; ConnectED 7m/11p c=0.99; Leaving to Learn 5m/6p c=0.98; 1-10 Arts 4m/4p c=1.00; 1-10 Blended Literacy 4m/4p c=1.00
- by era: Refresh 54m/62p c=0.99
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1009** AGH1009_5_0.html ↔ AGH1009.05.html (structure, derivable=True)
  - gold: `—`
  - Claude: `a  «Lesson 1.0 - Using chemical sprays – Primary Production NCEA Level 1 (desire2learn.com)»`
- **ANZH104** ANZH104_3_0.html ↔ ANZH104_03.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `a  «image (crop just faces)»`
- **ANZH301** ANZH301_6_0.html ↔ ANZH301_6.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `a  «https://docs.google.com/presentation/d/1d8cMYi3P5mTe7oLsL06u9yPonAVOJKRF55-c0XtYve4/present?slide=id.ged87af0212_0_167»`
- modules: AGH1009, ANZH104, ANZH301, ARFUN01, ARFUN02, ARFUN03, ARFUN05, BLL122, BLL132, BLL141, BLL240, CEDK501, CEDO502, CEDR501, CEDT404, CEDT501, CEDW201, CEDW501, CHFUN06, ENFUN09, ENGI201, ENGR202, ENGS102, EXBP901 …

### #6114 · body · SUBSTITUTED · `div.row` › gold `div.col-md-8.col-12` vs Claude `div.col-md-8.col-12` — CANDIDATE
- pages 56 / modules 49 / lines 63; consensus (all) 0.98 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 35m/42p c=0.98; Fundamentals 9m/9p c=1.00; Inquiry 5m/5p c=0.98
- by subject: 1-10 Blended Literacy 21m/24p c=0.97; 1-10 Mathematics 6m/8p c=0.99; None 4m/4p c=1.00; ConnectED 4m/4p c=1.00; 1-10 English 4m/4p c=0.98; ANZH 3m/4p c=0.99
- by era: Refresh 49m/56p c=0.98
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html (structure, derivable=True)
  - gold: `div.col-md-8.col-12  «Important Words»`
  - Claude: `div.col-md-8.col-12  «Important Words»`
- **ANZH301** ANZH301_1_0.html ↔ ANZH301_1.0.html (structure, derivable=True)
  - gold: `div.col-md-8.col-12  «War. What is it good for?»`
  - Claude: `div.col-md-8.col-12  «War. What is it good for?»`
- **ANZH401** ANZH401_4_0.html ↔ ANZH401_4.0.html (structure, derivable=True)
  - gold: `div.col-md-8.col-12  «Want to Travel Back in Time?»`
  - Claude: `div.col-md-8.col-12  «Go to your journal and share with your kaiako which item of evidence you chose and why it interested you.»`
- modules: ANZH101, ANZH301, ANZH401, ARFUN03, ARFUN05, BLL115, BLL124, BLL144, BLL152, BLL160, BLL166, BLL167, BLL171, BLL211, BLL213, BLL216, BLL217, BLL221, BLL222, BLL223, BLL224, BLL225, BLL226, BLL227 …

### #6116 · body · SUBSTITUTED · `div#body` › gold `div.row` vs Claude `WIDGET` — CANDIDATE
- pages 58 / modules 48 / lines 63; consensus (all) 0.94 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 45m/55p c=0.98; Inquiry 1m/1p c=0.65; Bilingual 1m/1p c=1.00; Fundamentals 1m/1p c=0.41
- by subject: Online Safety (OS9000) 13m/18p c=1.00; 1-10 English 10m/10p c=0.97; NCEA1 8m/8p c=1.00; Leaving to Learn 6m/7p c=0.98; ConnectED 3m/5p c=0.89; ANZH 2m/2p c=1.00
- by era: Refresh 48m/58p c=0.94
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1002** AGH1002_5_0.html ↔ AGH1002.05.html (structure, derivable=True)
  - gold: `div.row  «Two chemical properties are impacted by the amount of nutrients in soil:»`
  - Claude: `WIDGET`
- **AGH1003** AGH1003_3_0.html ↔ AGH1003_03.0.html (structure, derivable=True)
  - gold: `div.row  «When soils become low in nutrients it can have a negative impact on the growth rate of plants and the quality of the pro»`
  - Claude: `WIDGET`
- **AGH1009** AGH1009_1_0.html ↔ AGH1009.01.html (structure, derivable=True)
  - gold: `div.row  «Māori world view»`
  - Claude: `WIDGET`
- modules: AGH1002, AGH1003, AGH1009, ANZH105, ANZH205, BLL161, BLLR201, CEDK501, CEDO501, CEDT501, ENGC401, ENGI202, ENGI301, ENGI401, ENGJ301, ENGJ302, ENGJ403, ENGR101, ENGS201, ENGS301, HES1005, HES1006, MXDB302, MXFU401 …

### #6118 · body · EXTRA · `div.fundamentalsPanel` › gold `—` vs Claude `div.row` — CANDIDATE
- pages 45 / modules 45 / lines 509; consensus (all) 0.99 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Fundamentals 45m/45p c=0.62
- by subject: 1-10 Health and PE 11m/11p c=0.80; 1-10 English 8m/8p c=0.97; 1-10 Technology 8m/8p c=0.62; 1-10 Social Science 6m/6p c=0.87; 1-10 Arts 5m/5p c=0.40; None 5m/5p c=0.98
- by era: Refresh 45m/45p c=0.99
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ARFUN01** ARFUN01_0_0.html ↔ ARFUN01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Identity»`
- **ARFUN02** ARFUN02_0_0.html ↔ ARFUN02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Ngā āhuatanga o te puoro | The elements of music»`
- **ARFUN03** ARFUN03_0_0.html ↔ ARFUN03.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Give it a try: tinana parts»`
- modules: ARFUN01, ARFUN02, ARFUN03, ARFUN04, ARFUN05, CHFUN01, CHFUN04, CHFUN05, CHFUN06, CHFUN07, ENFUN01, ENFUN02, ENFUN03, ENFUN04, ENFUN05, ENFUN07, ENFUN08, ENFUN09, HPFUN101, HPFUN102, HPFUN103, HPFUN202, HPFUN203, HPFUN302 …

### #6122 · body · EXTRA · `div.alert` › gold `—` vs Claude `div.row` — CANDIDATE
- pages 55 / modules 42 / lines 65; consensus (all) 0.91 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 28m/41p c=0.92; Fundamentals 8m/8p c=0.77; Inquiry 6m/6p c=0.89
- by subject: Leaving to Learn 9m/12p c=0.84; NCEA1 8m/12p c=0.94; 1-10 Mathematics 6m/9p c=0.97; 1-10 English 4m/4p c=0.95; ConnectED 3m/3p c=0.77; 1-10 Technology 3m/3p c=0.88
- by era: Refresh 42m/55p c=0.91
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL240** BLL240_1_1.html ↔ BLL240-1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row`
- **CEDO105** CEDO105_1_0.html ↔ CEDO105.1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «You can try this activity again, but this time let someone else choose your movements. Can you and your supervisor make »`
- **CEDT207** CEDT207_5_0.html ↔ CEDT207_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «What colour are you? Do the fun quiz below and see what colour you are!»`
- modules: BLL240, CEDO105, CEDT207, CEDT301, ENFUN05, ENG1007, ENGI203, ENGI302, ENGS101, HIS1002, HIS1003, HIS1004, HIS1005, HIS1006, HIS1007, HIS1008, HPFUN202, MXDB202, MXDB302, MXEO202, MXEO401, MXFL201, MXFU302, OSAI501 …

### #6125 · body · EXTRA · `div.col-12` › gold `—` vs Claude `p` — CANDIDATE
- pages 68 / modules 41 / lines 102; consensus (all) 0.86 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 32m/59p c=0.88; Inquiry 5m/5p c=0.81; Fundamentals 4m/4p c=0.62
- by subject: Leaving to Learn 9m/20p c=0.85; 1-10 Mathematics 6m/7p c=0.90; NCEA1 5m/7p c=0.85; 1-10 English 5m/5p c=0.92; 1-10 Social Science 4m/4p c=0.53; ANZH 3m/13p c=0.87
- by era: Refresh 41m/68p c=0.86
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1001** AGH1001_3_0.html ↔ AGH1001.03.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Key points from today’s lesson:»`
- **AGH1006** AGH1006_7_0.html ↔ AGH1006.08.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «There are macronutrients and micronutrients required for healthy growth, flowering and fruiting. These include:»`
- **ANZH303** ANZH303_1_0.html ↔ ANZH303_0.1.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «In this lesson we are learning to understand the concept of mana in Māori culture and society.»`
- modules: AGH1001, AGH1006, ANZH303, ANZH304, ANZH401, CEDO102, CEDR501, ENGC201, ENGI301, ENGJ201, ENGJ202, ENGS302, EXBP901, EXIP901, EXPFUN06, HIS1003, HIS1004, HPFUN101, MXDI103, MXEX202, MXEX301, MXEX401, MXFL201, MXFU302 …

### #6126 · body · EXTRA · `div.row` › gold `—` vs Claude `div.col-md-6.col-12` — CANDIDATE
- pages 58 / modules 41 / lines 83; consensus (all) 0.99 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 35m/52p c=0.99; Fundamentals 5m/5p c=0.95; Inquiry 1m/1p c=1.00
- by subject: Online Safety (OS9000) 16m/20p c=1.00; 1-10 English 14m/23p c=0.99; ConnectED 5m/7p c=1.00; None 2m/2p c=0.96; 1-10 Mathematics 2m/3p c=0.98; NCEA1 1m/2p c=1.00
- by era: Refresh 41m/58p c=0.99
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **CEDK501** CEDK501_2_0.html ↔ CEDK501_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-6.col-12  «is the money you receive. It can come from different sources.»`
- **CEDO501** CEDO501_4_1.html ↔ CEDO501_4.1.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-6.col-12  «Attachment Orders»`
- **CEDO502** CEDO502_1_1.html ↔ CEDO502_1_2.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-6.col-12  «Tips to keep debt healthy»`
- modules: CEDK501, CEDO501, CEDO502, CEDR501, CEDW501, CHFUN01, ENFUN01, ENFUN08, ENFUN09, ENGC201, ENGC202, ENGC401, ENGI103, ENGI303, ENGI401, ENGR101, ENGR301, ENGS201, ENGS301, ENGS401, MXFU301, MXFU402, OSAH301, OSAI201 …

### #6128 · body · SUBSTITUTED · `div.col-md-8.col-12` › gold `p` vs Claude `p` — CANDIDATE
- pages 55 / modules 41 / lines 87; consensus (all) 0.85 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 28m/41p c=0.85; Bilingual 5m/6p c=0.67; Fundamentals 4m/4p c=1.00; Inquiry 4m/4p c=0.86
- by subject: 1-10 Mathematics 9m/12p c=0.93; Leaving to Learn 7m/10p c=0.97; Te Marautanga o Aotearoa TMoA 5m/6p c=0.67; 1-10 English 4m/4p c=0.90; NCEA1 4m/8p c=0.93; ConnectED 3m/4p c=0.94
- by era: Refresh 41m/55p c=0.85
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH303** ANZH303_3_0.html ↔ ANZH303_0.3.html (structure, derivable=True)
  - gold: `p  «Mana was a kind of spiritual power that people, groups, and things could have. It made them effective and respected. Peo»`
  - Claude: `p  «In this lesson you are learning more about social groupings in Māori society and the mana within them.»`
- **ANZH304** ANZH304_4_0.html ↔ ANZH304_0.4.html (structure, derivable=True)
  - gold: `p  «Within a very short time of Te Tiriti being signed, there were incidents that indicated to Māori that all was not as the»`
  - Claude: `p  «In this lesson we are learning about reactions to the Treaty by different rangatira, hapū and iwi in the early 1840s.»`
- **ARFUN04** ARFUN04_0_0.html ↔ ARFUN04_0.00.html (structure, derivable=True)
  - gold: `p  «In Phase Four, we will learn more about the seven essential elements of art and how to use them in our creative projects»`
  - Claude: `p  «What have I learned?»`
- modules: ANZH303, ANZH304, ARFUN04, BLL223, BLL226, CEDR501, CEDT104, CEDW201, ENFUN01, ENGJ301, ENGR201, ENGR202, HIS1002, HIS1004, HIS1005, MXDB302, MXDI201, MXEO301, MXFL203, MXFL301, MXFL302, MXFL401, MXFU202, MXFUN03 …

### #6129 · body · EXTRA · `a` › gold `—` vs Claude `div.externalButton` — CANDIDATE
- pages 63 / modules 40 / lines 117; consensus (all) 0.92 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 34m/57p c=0.93; Fundamentals 4m/4p c=0.80; Inquiry 2m/2p c=0.92
- by subject: 1-10 Mathematics 8m/15p c=0.93; ANZH 7m/9p c=0.82; Online Safety (OS9000) 5m/6p c=0.89; Leaving to Learn 5m/11p c=0.93; NCEA1 4m/8p c=0.90; ConnectED 3m/3p c=0.86
- by era: Refresh 40m/63p c=0.92
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH101** ANZH101_2_0.html ↔ ANZH101_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.externalButton  «Go to website»`
- **ANZH105** ANZH105_2_0.html ↔ ANZH105_02.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.externalButton  «Go to website»`
- **ANZH203** ANZH203_2_0.html ↔ ANZH203_3.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.externalButton  «Go to website»`
- modules: ANZH101, ANZH105, ANZH203, ANZH301, ANZH303, ANZH401, ANZH404, BLL234, CEDO105, CEDO301, CEDT104, ENFUN01, ENGR201, HIS1002, HIS1005, HIS1006, HPRE203, MXEO401, MXEX302, MXEX401, MXFL104, MXFL401, MXFU401, MXFU402 …

### #6131 · body · EXTRA · `tr` › gold `—` vs Claude `th` — CANDIDATE
- pages 45 / modules 40 / lines 132; consensus (all) 0.98 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 35m/40p c=0.99; Inquiry 3m/3p c=0.96; Fundamentals 2m/2p c=0.92
- by subject: 1-10 Mathematics 14m/18p c=0.96; 1-10 English 10m/10p c=0.98; ConnectED 5m/5p c=0.99; NCEA1 4m/4p c=0.99; None 2m/2p c=0.94; EXPlore 2m/2p c=0.67
- by era: Refresh 40m/45p c=0.98
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1002** AGH1002_1_0.html ↔ AGH1002.01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `th`
- **AGH1004** AGH1004_6_0.html ↔ AGH1004.07.html (structure, derivable=True)
  - gold: `—`
  - Claude: `th  «Milking occurs 1–2 times daily on farms across New Zealand.»`
- **AGH1005** AGH1005_4_0.html ↔ AGH1005.04.html (structure, derivable=True)
  - gold: `—`
  - Claude: `th  «Stomata»`
- modules: AGH1002, AGH1004, AGH1005, AGH1006, BLLR201, CEDK501, CEDO502, CEDR501, CEDT501, CEDW501, CHFUN05, ENFUN04, ENGC202, ENGI302, ENGI303, ENGI405, ENGJ201, ENGJ301, ENGJ302, ENGR302, ENGS102, EXPFUN02, EXPFUN07, MXDB301 …

### #6133 · body · EXTRA · `div#body` › gold `—` vs Claude `div.row.supervisor` — CANDIDATE
- pages 50 / modules 38 / lines 60; consensus (all) 0.88 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 33m/42p c=0.87; Inquiry 4m/6p c=0.91; Fundamentals 1m/2p c=0.98
- by subject: 1-10 Blended Literacy 17m/17p c=0.48; Leaving to Learn 5m/11p c=0.74; 1-10 English 4m/7p c=0.95; Online Safety (OS9000) 4m/4p c=0.95; ConnectED 3m/3p c=0.97; 1-10 Mathematics 3m/6p c=0.93
- by era: Refresh 38m/50p c=0.88
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 16_PAGEFORGE_COMPARE_MODE/16C_REPORT_FORMAT.md:219 — **Page:** SCCH302_2_0.html ↔ SCCH302-02.html   **Writer tag(s):** `[Activity 2B]`, `[Supervisor note]`, `[body]`   **Confidence:** high
- **ANZH104** ANZH104_6_0.html ↔ ANZH104_06.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row.supervisor  «Supervisor note»`
- **ANZH105** ANZH105_5_0.html ↔ ANZH105_05.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row.supervisor  «Supervisor note»`
- **BLL112** BLL112_2_0.html ↔ BLL112-03.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row.supervisor  «Supervisor note»`
- modules: ANZH104, ANZH105, BLL112, BLL113, BLL123, BLL124, BLL125, BLL126, BLL137, BLL142, BLL143, BLL164, BLL214, BLL216, BLL221, BLL246, BLL254, BLL262, BLL263, CEDO105, CEDT207, CEDW201, ENGI201, ENGJ101 …

### #6134 · body · EXTRA · `tr` › gold `—` vs Claude `td` — CANDIDATE
- pages 42 / modules 38 / lines 129; consensus (all) 0.95 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 31m/35p c=0.95; Fundamentals 4m/4p c=0.91; Inquiry 3m/3p c=0.94
- by subject: 1-10 Mathematics 12m/14p c=0.87; 1-10 English 7m/8p c=0.97; Online Safety (OS9000) 4m/4p c=0.97; NCEA1 3m/4p c=0.97; EXPlore 3m/3p c=0.67; Leaving to Learn 3m/3p c=0.99
- by era: Refresh 38m/42p c=0.95
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1006** AGH1006_6_0.html ↔ AGH1006.07.html (structure, derivable=True)
  - gold: `—`
  - Claude: `td  «Dock weed»`
- **AGH1007** AGH1007_5_0.html ↔ AGH1007.05.html (structure, derivable=True)
  - gold: `—`
  - Claude: `td  «[Click information] Feed requirements are highest during lactation and peak between 40 and 90 days after calving. Dairy »`
- **AGH1008** AGH1008_7_0.html ↔ AGH1008.07.html (structure, derivable=True)
  - gold: `—`
  - Claude: `td  «There are many roundworms. Some of the ones that impact sheep are Barbers Pole and Intestinal Roundworms. Most roundworm»`
- modules: AGH1006, AGH1007, AGH1008, BLLR201, CEDK501, CEDW501, ENFUN04, ENGC202, ENGI405, ENGJ201, ENGJ301, ENGS202, ENGS401, EXIP901, EXPFUN02, EXPFUN07, HPFUN201, MXDB201, MXDI202, MXDI301, MXEO102, MXEO202, MXEX301, MXFL102 …

### #6140 · body · MISSING · `div#body` › gold `div.fundamentalsPanel` vs Claude `—` — CANDIDATE
- pages 36 / modules 36 / lines 79; consensus (all) 0.02 of 1950 gold pages with the region; derivable 1.00 (0 lines with no WT source)
- by template: Fundamentals 35m/35p c=0.72; Standard 1m/1p c=0.00
- by subject: 1-10 Health and PE 12m/12p c=0.93; 1-10 English 7m/7p c=0.03; 1-10 Social Science 6m/6p c=0.18; 1-10 Mathematics 3m/3p c=0.01; 1-10 Technology 3m/3p c=1.00; 1-10 Arts 2m/2p c=1.00
- by era: Refresh 36m/36p c=0.02
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:140 — > **Subject cohort refinement.** The **Health & PE FUNdamentals** cohort (16 FUNs) adds content conventions on top of this recognised structure — 5–6 
  - KB: 14_SUBJECT_GLOBAL_PARAMETERS/14A_SGP_PURPOSE_FAMILIES_1_5.md:148 — > Sub-type **recognition** (body class `fundamentals container-fluid`, `div.phases` → `div.fundamentalsPanel` navigation, `footer-nav fundamentals-nav
  - KB: 14_SUBJECT_GLOBAL_PARAMETERS/14B_SGP_FAMILIES_6_11.md:188 — - **FUN vs module — trailing-digit test.** Within the `WJ` prefix, a **FUNdamentals templated resource ends in `0`** (e.g. `WJ200`, `WJ210`); a **norm
- **ARFUN01** ARFUN01_0_0.html ↔ ARFUN01.html (content, derivable=True)
  - gold: `div.fundamentalsPanel  «Making Change: Who we want to become»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [Text for link: Phase Four: Who we want to become] image for thumb nail  [/RED TEXT]🔴https://www.istockphoto.com/photo/funky-bass-player-gm1185857817-334353204`
- **ARFUN04** ARFUN04_0_0.html ↔ ARFUN04_0.00.html (content, derivable=True)
  - gold: `div.fundamentalsPanel  «Introduction»`
  - Claude: `—`
  - WT: `1. Watch this Introduction to overlapping: 🔴[RED TEXT] [insert item #21: video]  [/RED TEXT]🔴https://www.youtube.com/watch?v=HlpWhtA9ACA`
- **CHFUN05** CHFUN05_0_0.html ↔ CHFUN05_0_0.html (content, derivable=True)
  - gold: `div.fundamentalsPanel  «( ) + adjective»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [body] [/RED TEXT]🔴不 (bù) is a little word in Chinese that means “not.”  Think of it like a “no” sticker you put in front of a **verb** or **adjective**.`
- modules: ARFUN01, ARFUN04, CHFUN05, ENFUN01, ENFUN02, ENFUN04, ENFUN05, ENFUN07, ENFUN08, ENFUN09, HPFUN101, HPFUN201, HPFUN202, HPFUN203, HPFUN301, HPFUN303, HPFUN401, HPFUN402, HPFUN403, HPFUN901, HPFUN902, HPFUN903, MXFUN01, MXFUN02 …

### #6144 · body · EXTRA · `p` › gold `—` vs Claude `i` — CANDIDATE
- pages 43 / modules 35 / lines 86; consensus (all) 0.97 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 33m/41p c=0.97; Fundamentals 2m/2p c=0.91
- by subject: NCEA1 8m/13p c=0.96; 1-10 English 7m/7p c=0.93; 1-10 Blended Literacy 5m/5p c=0.99; Leaving to Learn 5m/5p c=0.97; ANZH 3m/3p c=1.00; 1-10 Mathematics 2m/5p c=0.99
- by era: Refresh 35m/43p c=0.97
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1005** AGH1005_4_0.html ↔ AGH1005.04.html (structure, derivable=True)
  - gold: `—`
  - Claude: `i  «at the same time»`
- **ANZH303** ANZH303_1_0.html ↔ ANZH303_0.1.html (structure, derivable=True)
  - gold: `—`
  - Claude: `i  «National Geographic New Zealand article ‘The meaning of mana’,»`
- **ANZH304** ANZH304_1_0.html ↔ ANZH304_0.1.html (structure, derivable=True)
  - gold: `—`
  - Claude: `i  «"Many people thought the missionaries came to prepare the Māori for the white land grabbers,"... "This is just not true.»`
- modules: AGH1005, ANZH303, ANZH304, ANZH404, ART1003, BLL143, BLL152, BLL173, BLL233, BLL234, CEDT501, CHFUN05, ENGI202, ENGJ301, ENGJ302, ENGJ402, ENGR301, ENGR302, ENGS301, HIS1002, HIS1003, HIS1004, HIS1005, HIS1008 …

### #6151 · body · SUBSTITUTED · `div.row` › gold `div.col-md-8.col-12` vs Claude `WIDGET` — CANDIDATE
- pages 33 / modules 32 / lines 34; consensus (all) 0.98 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 27m/28p c=0.98; Fundamentals 3m/3p c=1.00; Inquiry 1m/1p c=0.98; Bilingual 1m/1p c=1.00
- by subject: Leaving to Learn 6m/6p c=0.99; NCEA1 5m/5p c=0.99; 1-10 English 5m/6p c=0.98; Online Safety (OS9000) 5m/5p c=1.00; 1-10 Mathematics 4m/4p c=0.99; ConnectED 2m/2p c=1.00
- by era: Refresh 32m/33p c=0.98
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1007** AGH1007_3_0.html ↔ AGH1007.02.html (structure, derivable=True)
  - gold: `div.col-md-8.col-12  «There are three main types of digestion:»`
  - Claude: `WIDGET`
- **ANZH301** ANZH301_1_0.html ↔ ANZH301_1.0.html (structure, derivable=True)
  - gold: `div.col-md-8.col-12  «Lesson summary»`
  - Claude: `WIDGET`
- **BLLR201** BLLR201_1_1.html ↔ BLLR201_1_0.html (structure, derivable=True)
  - gold: `div.col-md-8.col-12  «If you can't visit a library or bookshop in person, you can still find information about books online. Te Kura has a lib»`
  - Claude: `WIDGET`
- modules: AGH1007, ANZH301, BLLR201, CEDK501, CEDO501, ENFUN09, ENGC301, ENGI202, ENGR202, ENGS401, HES1006, HES1007, HIS1002, MXDB302, MXDI103, MXFL204, MXFL302, OSBY101, OSGM401, OSGM501, OSOH201, OSOH401, PES1005, SSFUN05 …

### #6152 · body · EXTRA · `div#body` › gold `—` vs Claude `WIDGET` — CANDIDATE
- pages 50 / modules 31 / lines 77; consensus (all) 0.94 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 24m/37p c=0.93; Bilingual 4m/10p c=1.00; Inquiry 2m/2p c=0.96; Fundamentals 1m/1p c=0.95
- by subject: 1-10 English 9m/17p c=0.90; 1-10 Mathematics 7m/8p c=0.98; ConnectED 5m/9p c=0.99; Te Marautanga o Aotearoa TMoA 4m/10p c=1.00; 1-10 Blended Literacy 2m/2p c=0.98; Online Safety (OS9000) 2m/2p c=0.88
- by era: Refresh 31m/50p c=0.94
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL127** BLL127_1_0.html ↔ BLL127-02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **BLL263** BLL263_1_0.html ↔ BLL263_1_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- **CEDK501** CEDK501_5_0.html ↔ CEDK501_3.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `WIDGET`
- modules: BLL127, BLL263, CEDK501, CEDO501, CEDO502, CEDT104, CEDT501, ENGC202, ENGC301, ENGI303, ENGI400, ENGI401, ENGR201, ENGR301, ENGS102, ENGS202, MXDB201, MXDB301, MXEX101, MXFL202, MXFL204, MXFU402, MXFUN01, OSGM201 …

### #6154 · body · EXTRA · `div.col-md-8.col-12` › gold `—` vs Claude `h5` — CANDIDATE
- pages 37 / modules 31 / lines 59; consensus (all) 1.00 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 16m/21p c=1.00; Fundamentals 10m/10p c=0.97; Inquiry 5m/6p c=1.00
- by subject: NCEA1 11m/14p c=1.00; 1-10 English 7m/7p c=0.99; EXPlore 4m/4p c=1.00; 1-10 Arts 2m/2p c=1.00; ConnectED 2m/2p c=1.00; 1-10 Mathematics 2m/2p c=1.00
- by era: Refresh 31m/37p c=1.00
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ARFUN04** ARFUN04_0_0.html ↔ ARFUN04_0.00.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «Drawing and painting techniques»`
- **ARFUN05** ARFUN05_0_0.html ↔ ARFUN05.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «Facial expressions»`
- **CEDK102** CEDK102_0_0.html ↔ CEDK102.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «Storytelling»`
- modules: ARFUN04, ARFUN05, CEDK102, CEDT501, ENFUN01, ENFUN02, ENFUN03, ENFUN04, ENFUN05, ENFUN09, ENG1004, ENGFUN02, ENGI301, EXIP901, EXPFUN02, EXPFUN05, EXPFUN06, HES1004, HES1006, HIS1005, HIS1007, HIS1008, MXDI202, MXFL201 …

### #6155 · body · EXTRA · `div#body` › gold `—` vs Claude `div.fundamentalsPanel` — CANDIDATE
- pages 31 / modules 31 / lines 72; consensus (all) 0.98 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Fundamentals 31m/31p c=0.28
- by subject: 1-10 Health and PE 12m/12p c=0.07; 1-10 English 6m/6p c=0.97; 1-10 Social Science 4m/4p c=0.82; 1-10 Technology 3m/3p c=0.00; 1-10 Arts 2m/2p c=0.00; None 2m/2p c=1.00
- by era: Refresh 31m/31p c=0.98
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:140 — > **Subject cohort refinement.** The **Health & PE FUNdamentals** cohort (16 FUNs) adds content conventions on top of this recognised structure — 5–6 
  - KB: 14_SUBJECT_GLOBAL_PARAMETERS/14A_SGP_PURPOSE_FAMILIES_1_5.md:148 — > Sub-type **recognition** (body class `fundamentals container-fluid`, `div.phases` → `div.fundamentalsPanel` navigation, `footer-nav fundamentals-nav
  - KB: 14_SUBJECT_GLOBAL_PARAMETERS/14B_SGP_FAMILIES_6_11.md:188 — - **FUN vs module — trailing-digit test.** Within the `WJ` prefix, a **FUNdamentals templated resource ends in `0`** (e.g. `WJ200`, `WJ210`); a **norm
- **ARFUN01** ARFUN01_0_0.html ↔ ARFUN01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.fundamentalsPanel  «Making Change: Who we want to become»`
- **ARFUN04** ARFUN04_0_0.html ↔ ARFUN04_0.00.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.fundamentalsPanel  «In visual arts, we look at that help us make and talk about art.»`
- **CHFUN05** CHFUN05_0_0.html ↔ CHFUN05_0_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.fundamentalsPanel  «(both…and…)»`
- modules: ARFUN01, ARFUN04, CHFUN05, CHFUN06, ENFUN02, ENFUN03, ENFUN05, ENFUN07, ENFUN08, ENFUN09, HPFUN101, HPFUN102, HPFUN201, HPFUN202, HPFUN203, HPFUN301, HPFUN303, HPFUN401, HPFUN402, HPFUN901, HPFUN902, HPFUN903, SCFUN01, SSFUN01 …

### #6156 · body · EXTRA · `div.col-md-8.col-12` › gold `—` vs Claude `h4.goJournal` — CANDIDATE
- pages 41 / modules 30 / lines 45; consensus (all) 1.00 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 29m/40p c=1.00; Inquiry 1m/1p c=1.00
- by subject: 1-10 Mathematics 14m/22p c=1.00; 1-10 English 5m/6p c=1.00; NCEA1 4m/6p c=1.00; ANZH 2m/2p c=1.00; Leaving to Learn 2m/2p c=0.99; ConnectED 1m/1p c=1.00
- by era: Refresh 30m/41p c=1.00
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH101** ANZH101_3_0.html ↔ ANZH101_4.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h4.goJournal  «Go to your journal»`
- **ANZH105** ANZH105_2_0.html ↔ ANZH105_02.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h4.goJournal  «Go to your journal»`
- **CEDT207** CEDT207_6_0.html ↔ CEDT207_5.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h4.goJournal  «Go to your journal»`
- modules: ANZH101, ANZH105, CEDT207, ENGC101, ENGC102, ENGI202, ENGJ101, ENGJ102, HES1006, HIS1002, HIS1005, HIS1008, MXDB202, MXDI101, MXDI103, MXDI201, MXDI202, MXDI301, MXEO102, MXEO401, MXEX201, MXEX202, MXEX302, MXFL201 …

### #6160 · body · EXTRA · `div.inquiryPanel` › gold `—` vs Claude `div.row` — CANDIDATE
- pages 29 / modules 29 / lines 321; consensus (all) 0.99 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Inquiry 26m/26p c=0.88; Standard 2m/2p c=1.00; Fundamentals 1m/1p c=1.00
- by subject: 1-10 Blended Literacy 9m/9p c=0.97; ConnectED 7m/7p c=0.99; EXPlore 6m/6p c=1.00; Te ara Whakapuawa -Wellbeing 6m/6p c=0.62; 1-10 Mathematics 1m/1p c=1.00
- by era: Refresh 29m/29p c=0.99
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL120** BLL120_0_0.html ↔ BLL120.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Watch the following videos:»`
- **BLL130** BLL130_0_0.html ↔ BLL130.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Find the letter g»`
- **BLL140** BLL140_0_0.html ↔ BLL140.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row`
- modules: BLL120, BLL130, BLL140, BLL150, BLL160, BLL170, BLL210, BLL220, BLL230, CEDK102, CEDO102, CEDO202, CEDR204, CEDT101, CEDT404, CEDW101, EXBP901, EXIP901, EXPFUN02, EXPFUN03, EXPFUN04, EXPFUN05, MXFUN03, TWHA901 …

### #6161 · body · SUBSTITUTED · `div.row` › gold `div.col-md-8.col-12` vs Claude `div.row` — CANDIDATE
- pages 29 / modules 29 / lines 33; consensus (all) 0.98 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 22m/22p c=0.98; Fundamentals 4m/4p c=1.00; Inquiry 2m/2p c=0.98; Bilingual 1m/1p c=1.00
- by subject: 1-10 Blended Literacy 8m/8p c=0.97; 1-10 Mathematics 6m/6p c=0.99; 1-10 English 3m/3p c=0.98; Leaving to Learn 3m/3p c=0.99; ANZH 2m/2p c=0.99; ConnectED 2m/2p c=1.00
- by era: Refresh 29m/29p c=0.98
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH203** ANZH203_1_0.html ↔ ANZH203_1.0.html (structure, derivable=True)
  - gold: `div.col-md-8.col-12  «Comprehension activity»`
  - Claude: `div.row`
- **ANZH301** ANZH301_1_0.html ↔ ANZH301_1.0.html (structure, derivable=True)
  - gold: `div.col-md-8.col-12  «Statistics; so, what?»`
  - Claude: `div.row  «Can statistics tell a part of this story?»`
- **BLL135** BLL135_0_0.html ↔ BLL135-01.html (structure, derivable=True)
  - gold: `div.col-md-8.col-12  «Get ready to continue on your literacy journey.»`
  - Claude: `div.row  «Get ready to continue on your literacy journey.»`
- modules: ANZH203, ANZH301, BLL135, BLL154, BLL156, BLL157, BLL161, BLL162, BLL163, BLL164, CEDT104, CEDW201, ENFUN09, ENGJ402, ENGR201, HIS1002, MXDI103, MXEX301, MXFL103, MXFL203, MXFUN01, MXFUN03, OSAI101, SSFUN02 …

### #6162 · body · EXTRA · `div.col-md-8.col-12` › gold `—` vs Claude `div.videoSection.icon.ratio.ratio-16x9` — CANDIDATE
- pages 43 / modules 28 / lines 63; consensus (all) 0.91 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 18m/33p c=0.93; Fundamentals 9m/9p c=0.47; Inquiry 1m/1p c=0.87
- by subject: NCEA1 10m/21p c=0.85; ANZH 4m/7p c=0.96; 1-10 English 4m/4p c=0.92; 1-10 Arts 3m/3p c=0.00; 1-10 Social Science 3m/3p c=0.87; 1-10 Mathematics 2m/3p c=0.88
- by era: Refresh 28m/43p c=0.91
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:43 — | Video wrapper | `embed-responsive embed-responsive-16by9` | `ratio ratio-16x9` |
  - KB: 06_TEMPLATE_RECOGNITION.md:374 — <div class="videoSection ratio ratio-16x9">
  - KB: INDEX.md:160 — - **`14_SUBJECT_GLOBAL_PARAMETERS/14D_SGP_CROSSCUTTING_AND_TECHNOLOGY.md`** (6 KB) — Cross-cutting notes (14.11) and the Technology family (14.12 — fi
- **ANZH101** ANZH101_2_0.html ↔ ANZH101_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.videoSection.icon.ratio.ratio-16x9`
- **ANZH105** ANZH105_0_0.html ↔ ANZH105_00.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.videoSection.icon.ratio.ratio-16x9`
- **ANZH203** ANZH203_1_0.html ↔ ANZH203_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.videoSection.icon.ratio.ratio-16x9`
- modules: ANZH101, ANZH105, ANZH203, ANZH205, ARFUN01, ARFUN03, ARFUN04, ART1003, ENFUN01, ENFUN05, ENGI103, ENGI201, EXPFUN02, HIS1002, HIS1005, HIS1007, HIS1008, HPFUN102, MXFL201, MXFL204, PES1001, PES1002, PES1003, PES1005 …

### #6163 · body · EXTRA · `div.col-md-8.col-12` › gold `—` vs Claude `div.alert` — CANDIDATE
- pages 36 / modules 28 / lines 37; consensus (all) 0.91 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 21m/29p c=0.92; Fundamentals 5m/5p c=0.70; Inquiry 2m/2p c=0.87
- by subject: NCEA1 5m/12p c=0.95; Online Safety (OS9000) 4m/4p c=0.89; ConnectED 3m/3p c=0.79; 1-10 Mathematics 3m/3p c=0.97; 1-10 Social Science 3m/3p c=0.58; 1-10 Blended Literacy 2m/2p c=1.00
- by era: Refresh 28m/36p c=0.91
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH401** ANZH401_8_0.html ↔ ANZH401_8.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.alert  «To turn on captions in Chinese or English, click the 'CC' button in the player's toolbar.»`
- **ARFUN01** ARFUN01_0_0.html ↔ ARFUN01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.alert  «In this module there is learning for each of the different phases. Click the phase you will be working on to see more ab»`
- **BLL242** BLL242_1_1.html ↔ BLL242_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.alert  «Remember to start each sentence with a capital letter and finish each sentence with a full stop, a question mark or an e»`
- modules: ANZH401, ARFUN01, BLL242, BLL251, CEDO502, CEDR501, CEDT207, ENGS101, ENGS302, HIS1003, HIS1004, HIS1005, HIS1007, MXDB302, MXEX301, MXEX401, OSAH301, OSAI301, OSGM101, OSGM201, PES1007, SSCI205, SSFUN01, SSFUN08 …

### #6168 · body · EXTRA · `div.row` › gold `—` vs Claude `div.col-md-4.offset-md-0.col-12` — CANDIDATE
- pages 27 / modules 27 / lines 33; consensus (all) 0.79 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 18m/18p c=0.79; Inquiry 7m/7p c=0.79; Fundamentals 2m/2p c=0.84
- by subject: 1-10 Blended Literacy 17m/17p c=0.87; 1-10 Mathematics 2m/2p c=0.74; Online Safety (OS9000) 2m/2p c=0.80; 1-10 Technology 2m/2p c=0.75; ANZH 1m/1p c=0.74; NCEA1 1m/1p c=0.81
- by era: Refresh 27m/27p c=0.79
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH101** ANZH101_2_0.html ↔ ANZH101_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-4.offset-md-0.col-12  «Visit a library with your supervisor to find a book about this pūrākau. While you are there, try to find other stories. »`
- **BLL110** BLL110_0_0.html ↔ BLL110.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-4.offset-md-0.col-12  «Some students need more practice than others when learning the letters and sounds. Work through this module at your own »`
- **BLL120** BLL120_0_0.html ↔ BLL120.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-4.offset-md-0.col-12  «In the last lesson we introduced the letter 'c' to the ākonga and taught them how it makes the /k/ sound, as in words li»`
- modules: ANZH101, BLL110, BLL120, BLL123, BLL127, BLL131, BLL140, BLL156, BLL160, BLL162, BLL170, BLL177, BLL210, BLL211, BLL216, BLL220, BLL224, BLL231, HIS1004, MXDI103, MXFL201, OSBY301, OSBY401, SCCH301 …

### #6180 · body · EXTRA · `div#body` › gold `—` vs Claude `div.inquiryPanel` — CANDIDATE
- pages 24 / modules 24 / lines 60; consensus (all) 0.99 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Inquiry 22m/22p c=0.75; Standard 2m/2p c=1.00
- by subject: ConnectED 7m/7p c=0.95; EXPlore 7m/7p c=0.73; Te ara Whakapuawa -Wellbeing 6m/6p c=0.25; 1-10 Blended Literacy 4m/4p c=0.97
- by era: Refresh 24m/24p c=0.99
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **BLL110** BLL110_0_0.html ↔ BLL110.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.inquiryPanel  «The letter s»`
- **BLL120** BLL120_0_0.html ↔ BLL120.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.inquiryPanel  «The letter k»`
- **BLL160** BLL160_0_0.html ↔ BLL160.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.inquiryPanel  «Supervisor note»`
- modules: BLL110, BLL120, BLL160, BLL230, CEDK101, CEDK102, CEDO102, CEDO202, CEDR204, CEDT101, CEDT404, EXBP901, EXIP901, EXPFUN02, EXPFUN03, EXPFUN04, EXPFUN05, EXPFUN06, TWHA901, TWHA902, TWHA903, TWHA904, TWHA906, TWHK903

### #6183 · body · EXTRA · `div.col-md-8.col-12` › gold `—` vs Claude `p>span.infoTrigger` — CANDIDATE
- pages 29 / modules 23 / lines 46; consensus (all) 0.86 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 20m/26p c=0.87; Fundamentals 2m/2p c=0.62; Inquiry 1m/1p c=0.85
- by subject: 1-10 English 6m/7p c=0.84; NCEA1 5m/7p c=0.77; 1-10 Mathematics 5m/6p c=0.88; 1-10 Social Science 3m/5p c=0.82; Leaving to Learn 3m/3p c=0.88; ANZH 1m/1p c=0.77
- by era: Refresh 23m/29p c=0.86
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1001** AGH1001_2_0.html ↔ AGH1001.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Pre-European settlement:»`
- **ANZH205** ANZH205_1_0.html ↔ ANZH205_01.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Image of the letter Link to Check out Aotearoa New Zealand’s Declaration of Independence!»`
- **ENFUN01** ENFUN01_0_0.html ↔ ENFUN01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `p  «Purpose is used in reading and writing. It tells us what genre, style, tone and we should use.»`
- modules: AGH1001, ANZH205, ENFUN01, ENGI202, ENGI405, ENGJ302, ENGR302, ENGS101, HIS1005, HIS1007, MXDI202, MXEO301, MXFL302, MXFL401, MXFU301, PHE1007, PHE1008, SSCI205, SSFUN01, SSFUN07, XDLS502, XDLS909, XLP04

### #6185 · body · SUBSTITUTED · `div.col-md-8.col-12` › gold `p` vs Claude `WIDGET` — CANDIDATE
- pages 24 / modules 23 / lines 25; consensus (all) 0.85 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 17m/18p c=0.85; Inquiry 3m/3p c=0.86; Fundamentals 2m/2p c=1.00; Bilingual 1m/1p c=0.67
- by subject: NCEA1 6m/6p c=0.93; Online Safety (OS9000) 4m/4p c=1.00; None 3m/3p c=0.98; 1-10 English 3m/4p c=0.90; ConnectED 2m/2p c=0.94; 1-10 Blended Literacy 1m/1p c=0.38
- by era: Refresh 23m/24p c=0.85
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1003** AGH1003_5_0.html ↔ AGH1003_05.0.html (structure, derivable=True)
  - gold: `p  «Dolomite lime can also be used. It is a kind of limestone that contains magnesium as well as calcium.»`
  - Claude: `WIDGET`
- **BLL221** BLL221_2_0.html ↔ BLL221-2.0.html (structure, derivable=True)
  - gold: `p  «Congratulations on completing Module 1. You are now ready to start Module 2. Go back to the landing page and click on Mo»`
  - Claude: `WIDGET`
- **CEDT404** CEDT404_0_0.html ↔ CEDT404.html (structure, derivable=True)
  - gold: `p  «In the next section, you will be writing instructions explaining how to play your game, so make sure you are thinking ab»`
  - Claude: `WIDGET`
- modules: AGH1003, BLL221, CEDT404, CEDT501, CHFUN05, ENGI303, ENGS101, ENGS202, HES1005, HIS1001, HPFUN402, OSAH401, OSAI101, OSAI401, OSSC501, PES1004, PES1008, PHE1007, TEDC401, TEDC402, TRR301, TWHA902, XDLS903

### #6192 · body · EXTRA · `div.row.flipCardsContainer` › gold `—` vs Claude `div.col-md-4.col-12.paddingLR` — CANDIDATE
- pages 23 / modules 22 / lines 66; consensus (all) 0.97 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 16m/17p c=0.97; Fundamentals 5m/5p c=0.88; Inquiry 1m/1p c=0.97
- by subject: 1-10 English 8m/8p c=0.97; None 3m/3p c=0.94; Leaving to Learn 3m/3p c=0.97; NCEA1 2m/3p c=1.00; ConnectED 1m/1p c=0.90; 1-10 Health and PE 1m/1p c=1.00
- by era: Refresh 22m/23p c=0.97
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1006** AGH1006_2_0.html ↔ AGH1006.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-4.col-12.paddingLR`
- **CEDR501** CEDR501_3_0.html ↔ CEDR501_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-4.col-12.paddingLR`
- **CHFUN05** CHFUN05_0_0.html ↔ CHFUN05_0_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-4.col-12.paddingLR`
- modules: AGH1006, CEDR501, CHFUN05, ENFUN03, ENFUN04, ENFUN05, ENGC301, ENGI102, ENGI202, ENGJ302, ENGS301, HPFUN201, MXEX201, PES1003, SCCH301, SSCI205, TEDC401, TEDC402, TWHK903, XDLS502, XLP02, XMES201

### #6195 · body · EXTRA · `div.alert.solid` › gold `—` vs Claude `div.row` — CANDIDATE
- pages 30 / modules 21 / lines 35; consensus (all) 0.99 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 16m/25p c=0.99; Inquiry 4m/4p c=0.99; Bilingual 1m/1p c=1.00
- by subject: NCEA1 6m/10p c=0.99; 1-10 Mathematics 5m/8p c=0.99; 1-10 Blended Literacy 3m/3p c=1.00; ConnectED 3m/4p c=0.96; ANZH 1m/1p c=1.00; 1-10 English 1m/2p c=0.99
- by era: Refresh 21m/30p c=0.99
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: INDEX.md:81 — - Sections: COMP_14 — Layout & Structure · Activities · Alerts (Cultural Alert · Translate Section in Alert Solid · Activity Image Sidebar · Activity 
  - KB: 01_PIPELINE_EXTRACTION_TAGS/01F_TAG_INTERPRETATION_STYLING_ACTIVITIES.md:11 — | `important` | `<div class="alert solid"><div class="row"><div class="col-12"><p>content</p></div></div></div>` |
  - KB: 05_COMP_LANGUAGE_MEDIA_LAYOUT/05B_COMP14_LAYOUT_STRUCTURE.md:119 — <div class="alert solid"><div class="row"><div class="col-12"><p>Content</p></div></div></div>
- **AGH1002** AGH1002_2_0.html ↔ AGH1002.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «The combined percentage of sand, silt and clay in a soil should always add up to 100.»`
- **ANZH401** ANZH401_6_0.html ↔ ANZH401_6.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «Use the quiz button below to share what you noticed. You can do this using the audio, or by writing sentence(s).»`
- **BLL110** BLL110_0_0.html ↔ BLL110.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «When a letter is written as ‘t’ we want you to say its name. When it is written as /t/ it means we want you to say its s»`
- modules: AGH1002, ANZH401, BLL110, BLL130, BLL140, CEDR204, CEDT501, CEDW501, ENGI303, HIS1002, HIS1005, HIS1006, HIS1007, MXDB201, MXDI101, MXFL102, MXFL401, MXFU302, PHE1008, TRR108, XGF9006

### #6197 · body · EXTRA · `div.col-md-8.col-12` › gold `—` vs Claude `div.row.flipCardsContainer` — CANDIDATE
- pages 26 / modules 21 / lines 26; consensus (all) 0.93 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 18m/23p c=0.94; Fundamentals 2m/2p c=0.67; Inquiry 1m/1p c=0.88
- by subject: 1-10 English 8m/11p c=0.92; Leaving to Learn 3m/3p c=0.91; NCEA1 2m/2p c=0.99; Online Safety (OS9000) 2m/3p c=0.78; None 2m/3p c=0.85; ANZH 1m/1p c=0.97
- by era: Refresh 21m/26p c=0.93
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1006** AGH1006_2_0.html ↔ AGH1006.02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row.flipCardsContainer`
- **ANZH205** ANZH205_3_0.html ↔ ANZH205_03.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row.flipCardsContainer`
- **CEDO202** CEDO202_0_0.html ↔ CEDO202_0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row.flipCardsContainer`
- modules: AGH1006, ANZH205, CEDO202, ENGI102, ENGI202, ENGI405, ENGJ202, ENGJ402, ENGR102, ENGR301, ENGS102, HPFUN101, OSAH501, OSBY501, PES1007, TEDC401, TEDC402, TEFUN02, XGF9001, XGF9006, XLP03

### #6201 · body · SUBSTITUTED · `div.col-md-8.col-12` › gold `p` vs Claude `img.img-fluid` — CANDIDATE
- pages 21 / modules 21 / lines 21; consensus (all) 0.85 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 10m/10p c=0.85; Fundamentals 7m/7p c=1.00; Bilingual 3m/3p c=0.67; Inquiry 1m/1p c=0.86
- by subject: 1-10 English 4m/4p c=0.90; 1-10 Health and PE 4m/4p c=1.00; NCEA1 3m/3p c=0.93; Te Marautanga o Aotearoa TMoA 3m/3p c=0.67; None 2m/2p c=0.98; 1-10 Mathematics 2m/2p c=0.93
- by era: Refresh 21m/21p c=0.85
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **CEDO102** CEDO102_0_0.html ↔ CEDO102_0.0.html (structure, derivable=True)
  - gold: `p  «Click on the side tabs and get ready for an adventure where science and art come together to make learning a splash of f»`
  - Claude: `img.img-fluid`
- **CHFUN05** CHFUN05_0_0.html ↔ CHFUN05_0_0.html (structure, derivable=True)
  - gold: `p  «Using ( ) to show doing an activity with someone»`
  - Claude: `img.img-fluid`
- **ENGI103** ENGI103_4_0.html ↔ ENGI103_4.0.html (structure, derivable=True)
  - gold: `p  «Watch the video below to learn more about what a kaihautū does.»`
  - Claude: `img.img-fluid`
- modules: CEDO102, CHFUN05, ENGI103, ENGI405, ENGJ403, ENGS302, HIS1008, HPFUN202, HPFUN302, HPFUN402, HPFUN901, MXFL203, MXFU202, PES1001, PHE1007, SCPH301, TEFUN04, TEFUN07, TRR106, TRR109, TRR111

### #6205 · body · EXTRA · `div.videoSection.icon.ratio.ratio-16x9` › gold `—` vs Claude `iframe` — CANDIDATE
- pages 26 / modules 20 / lines 29; consensus (all) 0.97 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 17m/23p c=0.98; Fundamentals 3m/3p c=0.77
- by subject: NCEA1 9m/14p c=1.00; ANZH 6m/7p c=1.00; 1-10 English 2m/2p c=0.99; 1-10 Arts 1m/1p c=0.00; 1-10 Blended Literacy 1m/1p c=1.00; 1-10 Social Science 1m/1p c=0.95
- by era: Refresh 20m/26p c=0.97
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:43 — | Video wrapper | `embed-responsive embed-responsive-16by9` | `ratio ratio-16x9` |
  - KB: 06_TEMPLATE_RECOGNITION.md:374 — <div class="videoSection ratio ratio-16x9">
  - KB: INDEX.md:160 — - **`14_SUBJECT_GLOBAL_PARAMETERS/14D_SGP_CROSSCUTTING_AND_TECHNOLOGY.md`** (6 KB) — Cross-cutting notes (14.11) and the Technology family (14.12 — fi
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `iframe`
- **ANZH105** ANZH105_1_0.html ↔ ANZH105_01.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `iframe`
- **ANZH205** ANZH205_2_0.html ↔ ANZH205_02.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `iframe`
- modules: ANZH101, ANZH105, ANZH205, ANZH303, ANZH304, ANZH401, ARFUN04, BLL122, ENFUN01, ENGI202, HIS1001, HIS1002, HIS1005, HIS1008, PES1001, PES1002, PES1003, PES1005, PES1008, SSFUN01

### #6207 · body · SUBSTITUTED · `div.row` › gold `div.col-md-8.col-12` vs Claude `p` — CANDIDATE
- pages 20 / modules 20 / lines 23; consensus (all) 0.98 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 13m/13p c=0.98; Fundamentals 4m/4p c=1.00; Inquiry 3m/3p c=0.98
- by subject: 1-10 English 4m/4p c=0.98; NCEA1 3m/3p c=0.99; 1-10 Mathematics 3m/3p c=0.99; ConnectED 2m/2p c=1.00; Online Safety (OS9000) 2m/2p c=1.00; Leaving to Learn 2m/2p c=0.99
- by era: Refresh 20m/20p c=0.98
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html (structure, derivable=True)
  - gold: `div.col-md-8.col-12  «Skills»`
  - Claude: `p  «Here you can see where the different waka landed and how people moved around Aotearoa.»`
- **ARFUN02** ARFUN02_0_0.html ↔ ARFUN02.html (structure, derivable=True)
  - gold: `div.col-md-8.col-12  «Inversion: Flipping the Music Upside Down!»`
  - Claude: `p  «* BOOM - BOOM - CLAP»`
- **CEDT104** CEDT104_0_0.html ↔ CEDT104 Waiata In Motion.html (structure, derivable=True)
  - gold: `div.col-md-8.col-12  «Let's learn pepeha through movement»`
  - Claude: `p  «Tau kē. (Awesome.)»`
- modules: ANZH101, ARFUN02, CEDT104, CEDT208, ENFUN01, ENGI102, ENGR201, ENGS102, HES1003, HIS1002, MXDB301, MXFUN01, MXFUN03, OSAI501, OSBY101, PES1008, SSFUN07, TWHA902, XDLS911, XGF9002

### #6210 · body · EXTRA · `div.col-md-8.col-12` › gold `—` vs Claude `div.alert.solid` — CANDIDATE
- pages 25 / modules 19 / lines 30; consensus (all) 0.99 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 14m/20p c=0.99; Inquiry 3m/3p c=1.00; Fundamentals 1m/1p c=0.98; Bilingual 1m/1p c=1.00
- by subject: NCEA1 4m/6p c=0.99; 1-10 Mathematics 4m/6p c=0.99; Leaving to Learn 3m/3p c=0.97; 1-10 Blended Literacy 2m/2p c=1.00; ConnectED 2m/2p c=0.98; 1-10 English 2m/2p c=1.00
- by era: Refresh 19m/25p c=0.99
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: INDEX.md:81 — - Sections: COMP_14 — Layout & Structure · Activities · Alerts (Cultural Alert · Translate Section in Alert Solid · Activity Image Sidebar · Activity 
  - KB: 01_PIPELINE_EXTRACTION_TAGS/01F_TAG_INTERPRETATION_STYLING_ACTIVITIES.md:11 — | `important` | `<div class="alert solid"><div class="row"><div class="col-12"><p>content</p></div></div></div>` |
  - KB: 05_COMP_LANGUAGE_MEDIA_LAYOUT/05B_COMP14_LAYOUT_STRUCTURE.md:119 — <div class="alert solid"><div class="row"><div class="col-12"><p>Content</p></div></div></div>
- **AGH1002** AGH1002_1_0.html ↔ AGH1002.01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.alert.solid  «Te toto o tetangatahe kai, teorangao tetangata, he whenua, he oneone»`
- **AGH1007** AGH1007_6_0.html ↔ AGH1007.06.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.alert.solid  «An egg that “dies” before the sperm reach it cannot be fertilised and the farmer must wait another cycle before that ani»`
- **ANZH401** ANZH401_4_0.html ↔ ANZH401_4.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.alert.solid  «Go to your journal and share with your kaiako which item of evidence you chose and why it interested you.»`
- modules: AGH1002, AGH1007, ANZH401, BLL170, BLL230, CEDO502, CEDT404, ENFUN04, ENG1004, ENG1005, ENGJ402, MXDB201, MXEX401, MXFU302, MXFU401, TRR114, XDLS501, XDLS902, XGF9006

### #6213 · body · EXTRA · `div.row` › gold `—` vs Claude `div.col-md-4.col-12` — CANDIDATE
- pages 23 / modules 19 / lines 27; consensus (all) 0.95 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 15m/19p c=0.95; Fundamentals 4m/4p c=0.88
- by subject: ANZH 4m/5p c=0.97; 1-10 Mathematics 4m/5p c=0.97; 1-10 English 3m/3p c=0.94; 1-10 Technology 3m/3p c=0.75; Leaving to Learn 2m/3p c=0.96; EXPlore 1m/2p c=0.60
- by era: Refresh 19m/23p c=0.95
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH203** ANZH203_2_0.html ↔ ANZH203_3.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-4.col-12  «https://www.youtube.com/embed/316F1A8c09k?si=ec4_dYHL9zZsS26C»`
- **ANZH301** ANZH301_2_0.html ↔ ANZH301_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-4.col-12  «Sensitivity: Some of the content in this lesson and in this module may bring up certain emotions and feelings. We all ha»`
- **ANZH303** ANZH303_2_0.html ↔ ANZH303_0.2.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.col-md-4.col-12  «If you can make contact with mana whenua and kaumatua in your rōhe, you might like to ask them about special kai in your»`
- modules: ANZH203, ANZH301, ANZH303, ANZH404, ENGC401, ENGI102, ENGI103, EXIP901, HIS1004, MXFL104, MXFL202, MXFL301, MXFU301, SSFUN01, TEFUN02, TEFUN03, TEFUN05, XDLS908, XGF9006

### #6215 · body · EXTRA · `div.row` › gold `—` vs Claude `div.clickDropContent` — CANDIDATE
- pages 21 / modules 19 / lines 47; consensus (all) 1.00 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 17m/19p c=1.00; Fundamentals 1m/1p c=1.00; Inquiry 1m/1p c=1.00
- by subject: Online Safety (OS9000) 11m/12p c=0.98; Leaving to Learn 3m/4p c=1.00; 1-10 Arts 1m/1p c=1.00; None 1m/1p c=0.98; 1-10 English 1m/1p c=1.00; 1-10 Mathematics 1m/1p c=1.00
- by era: Refresh 19m/21p c=1.00
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ARFUN04** ARFUN04_0_0.html ↔ ARFUN04_0.00.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.clickDropContent  «Match the technique to its correct description by dragging and dropping each term into the right box.»`
- **BLLR201** BLLR201_2_0.html ↔ BLLR201_1_1.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.clickDropContent  «Ending with»`
- **ENGR202** ENGR202_1_0.html ↔ ENGR202_1.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.clickDropContent  «Size refers to how big or small something is.»`
- modules: ARFUN04, BLLR201, ENGR202, MXFL302, OSBY101, OSBY201, OSBY401, OSBY501, OSGM401, OSGM501, OSOH201, OSOH401, OSOH501, OSSC401, OSSC501, SCCH301, XDLS901, XLP02, XTAS102

### #6216 · body · EXTRA · `div.col-md-8.col-12` › gold `—` vs Claude `div.row` — CANDIDATE
- pages 21 / modules 19 / lines 22; consensus (all) 0.75 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 16m/18p c=0.77; Inquiry 1m/1p c=0.74; Fundamentals 1m/1p c=0.34; Bilingual 1m/1p c=0.68
- by subject: Online Safety (OS9000) 7m/7p c=0.72; 1-10 Mathematics 3m/4p c=0.66; Leaving to Learn 3m/3p c=0.77; 1-10 English 2m/2p c=0.74; ConnectED 1m/1p c=0.77; EXPlore 1m/1p c=0.47
- by era: Refresh 19m/21p c=0.75
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **CEDO502** CEDO502_2_0.html ↔ CEDO502_2_0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «/ A business that keeps people’s money and lends money»`
- **ENGJ302** ENGJ302_8_0.html ↔ ENGJ302_7.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «In this rhyme scheme, consecutive lines rhyme with each other. They are often called ‘couplets’.»`
- **ENGR202** ENGR202_7_0.html ↔ ENGR202_7.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row  «: In an infographic, things that are bigger catch your eye first. For example, if the title is big, you know it’s import»`
- modules: CEDO502, ENGJ302, ENGR202, EXPFUN04, MXDB302, MXFU301, MXFUN02, OSAH501, OSGM301, OSOH101, OSOH301, OSOH401, OSSC301, OSSM401, SCCH301, TRR102, XLP02, XTAS101, XTAS103

### #6218 · body · SUBSTITUTED · `div.col-md-8.col-12` › gold `p` vs Claude `ul` — CANDIDATE
- pages 21 / modules 19 / lines 21; consensus (all) 0.85 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 14m/16p c=0.85; Inquiry 3m/3p c=0.86; Fundamentals 1m/1p c=1.00; Bilingual 1m/1p c=0.67
- by subject: 1-10 Blended Literacy 9m/9p c=0.38; 1-10 English 3m/3p c=0.90; NCEA1 2m/3p c=0.93; ConnectED 2m/2p c=0.94; EXPlore 1m/1p c=1.00; 1-10 Mathematics 1m/2p c=0.93
- by era: Refresh 19m/21p c=0.85
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1009** AGH1009_6_0.html ↔ AGH1009.06.1.html (structure, derivable=True)
  - gold: `p  «This video explains how one farm is using composting and mulching to nurture their soil ecosystem through the use of cow»`
  - Claude: `ul  «precision agriculture and soil testing»`
- **BLL142** BLL142_1_1.html ↔ BLL142-2.0.html (structure, derivable=True)
  - gold: `p  «Congratulations on completing Module 2. You are now ready to start Module 3. Go back to the landing page and click on Mo»`
  - Claude: `ul  «If a specific third-party item/image is crucial to your writing, then please submit this for early copyright clearance n»`
- **BLL144** BLL144_1_1.html ↔ BLL144-2.0.html (structure, derivable=True)
  - gold: `p  «Congratulations on completing Module 4. Tino pai, you are tracking so well! You are now ready to start Module 5. Go back»`
  - Claude: `ul  «If a specific third-party item/image is crucial to your writing, then please submit this for early copyright clearance n»`
- modules: AGH1009, BLL142, BLL144, BLL145, BLL153, BLL154, BLL156, BLL165, BLL174, BLL176, CEDK501, CEDT207, ENFUN09, ENGI201, ENGI301, EXPFUN05, HIS1005, MXEX101, TRR111

### #6225 · body · SUBSTITUTED · `div.col-md-8.col-12` › gold `p` vs Claude `h3` — CANDIDATE
- pages 20 / modules 18 / lines 21; consensus (all) 0.85 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 16m/18p c=0.85; Inquiry 1m/1p c=0.86; Bilingual 1m/1p c=0.67
- by subject: NCEA1 8m/9p c=0.93; Leaving to Learn 4m/4p c=0.97; 1-10 English 2m/2p c=0.90; ANZH 1m/1p c=0.90; 1-10 Blended Literacy 1m/1p c=0.38; 1-10 Mathematics 1m/2p c=0.93
- by era: Refresh 18m/20p c=0.85
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1007** AGH1007_4_0.html ↔ AGH1007.04.html (structure, derivable=True)
  - gold: `p  «Sheep, cattle and deer mainly digest food through microbial digestion. You will remember that our monogastric livestock »`
  - Claude: `h3  «The Amazing Cow: An introduction to ruminant digestive systems.»`
- **AGH1008** AGH1008_4_0.html ↔ AGH1008.04.html (structure, derivable=True)
  - gold: `p  «Genetics are important in agriculture as when farmers are selecting stock for breeding it is important they know what ge»`
  - Claude: `h3  «Genetics»`
- **ANZH303** ANZH303_6_0.html ↔ ANZH303_0.6.html (structure, derivable=True)
  - gold: `p  «Read through the following slides about motivations, the signing and the significance of this document.»`
  - Claude: `h3  «Motives for a Declaration»`
- modules: AGH1007, AGH1008, ANZH303, BLL120, ENGC301, ENGI405, HES1003, HIS1007, HIS1008, MXFL201, PES1007, PES1008, PHE1004, TRR102, XGF9003, XGF9004, XLP03, XMES101

### #6226 · body · SUBSTITUTED · `div.row` › gold `div.col-md-8.col-12` vs Claude `div.col-md-6.col-12` — CANDIDATE
- pages 20 / modules 18 / lines 20; consensus (all) 0.98 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 15m/17p c=0.98; Fundamentals 2m/2p c=1.00; Bilingual 1m/1p c=1.00
- by subject: 1-10 English 10m/11p c=0.98; Online Safety (OS9000) 5m/5p c=1.00; ConnectED 2m/3p c=1.00; Te Marautanga o Aotearoa TMoA 1m/1p c=1.00
- by era: Refresh 18m/20p c=0.98
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **CEDO501** CEDO501_4_1.html ↔ CEDO501_4.1.html (structure, derivable=True)
  - gold: `div.col-md-8.col-12`
  - Claude: `div.col-md-6.col-12  «Taxes»`
- **CEDO502** CEDO502_1_1.html ↔ CEDO502_1_2.html (structure, derivable=True)
  - gold: `div.col-md-8.col-12  «Tips to keep debt healthy»`
  - Claude: `div.col-md-6.col-12`
- **ENFUN01** ENFUN01_0_0.html ↔ ENFUN01.html (structure, derivable=True)
  - gold: `div.col-md-8.col-12  «Why do I need to an audience to share my ideas with?»`
  - Claude: `div.col-md-6.col-12`
- modules: CEDO501, CEDO502, ENFUN01, ENFUN09, ENGC201, ENGI401, ENGR201, ENGR202, ENGR301, ENGS102, ENGS201, ENGS301, OSAH301, OSAI101, OSAI201, OSGM401, OSSC301, TRR102

### #6229 · body · SUBSTITUTED · `div.col-md-8.col-12` › gold `p` vs Claude `div.alert` — CANDIDATE
- pages 26 / modules 17 / lines 26; consensus (all) 0.85 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 10m/19p c=0.85; Fundamentals 5m/5p c=1.00; Inquiry 2m/2p c=0.86
- by subject: NCEA1 5m/12p c=0.93; 1-10 Technology 5m/5p c=1.00; ANZH 1m/1p c=0.90; ConnectED 1m/1p c=0.94; 1-10 English 1m/2p c=0.90; EXPlore 1m/1p c=1.00
- by era: Refresh 17m/26p c=0.85
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **ANZH205** ANZH205_4_0.html ↔ ANZH205_04.0.html (structure, derivable=True)
  - gold: `p  «Kai pai! Now, let’s find out which copy of the treaty was brought to your rohe or iwi.»`
  - Claude: `div.alert  «Did you know the Waikato-Manukau sheet was the only signed copy that was written in English?»`
- **CEDT207** CEDT207_5_0.html ↔ CEDT207_0.0.html (structure, derivable=True)
  - gold: `p  «No two people are exactly alike. Each of us is an individual with unique talents, interests, and values and learning abo»`
  - Claude: `div.alert  «What colour are you? Do the fun quiz below and see what colour you are!»`
- **ENGC201** ENGC201_1_0.html ↔ ENGC201_1.0.html (structure, derivable=True)
  - gold: `p  «Researchers have found that people across the world share similar facial expressions for emotions. This means that no ma»`
  - Claude: `div.alert  «The are believed to be:»`
- modules: ANZH205, CEDT207, ENGC201, EXBP901, HIS1002, HIS1003, HIS1004, HIS1007, HIS1008, MXDB302, TEDC402, TEFUN01, TEFUN03, TEFUN06, TEFUN07, TEFUN08, XDLS909

### #6236 · body · EXTRA · `th>b` › gold `—` vs Claude `b` — CANDIDATE
- pages 22 / modules 16 / lines 82; consensus (all) 1.00 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 12m/16p c=1.00; Fundamentals 3m/3p c=1.00; Inquiry 1m/3p c=1.00
- by subject: ConnectED 4m/7p c=1.00; 1-10 Mathematics 4m/7p c=1.00; NCEA1 3m/3p c=1.00; None 1m/1p c=1.00; 1-10 English 1m/1p c=0.99; Online Safety (OS9000) 1m/1p c=0.99
- by era: Refresh 16m/22p c=1.00
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1002** AGH1002_4_0.html ↔ AGH1002.04.html (structure, derivable=True)
  - gold: `—`
  - Claude: `b  «Soil Type»`
- **AGH1008** AGH1008_1_0.html ↔ AGH1008.01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `b  «Way of increasing profit»`
- **CEDK501** CEDK501_2_0.html ↔ CEDK501_2.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `b  «Expenses (weekly)»`
- modules: AGH1002, AGH1008, CEDK501, CEDO501, CEDO502, CEDR501, CHFUN05, ENGJ302, MXDI301, MXEO401, MXFU301, MXFU302, OSOH501, PHE1007, SCFUN01, TEFUN08

### #6254 · body · MISSING · `div#body` › gold `div.row.clickDropContent.noBorder` vs Claude `—` — CANDIDATE
- pages 49 / modules 14 / lines 112; consensus (all) 0.03 of 1950 gold pages with the region; derivable 0.94 (7 lines with no WT source)
- by template: Standard 10m/36p c=0.02; Inquiry 3m/12p c=0.13; Bilingual 1m/1p c=0.02
- by subject: Leaving to Learn 8m/40p c=0.20; 1-10 English 2m/2p c=0.01; ConnectED 1m/2p c=0.02; NCEA1 1m/3p c=0.01; 1-10 Mathematics 1m/1p c=0.00; Te Marautanga o Aotearoa TMoA 1m/1p c=0.02
- by era: Refresh 14m/49p c=0.03
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:425 — | `noBorder` | Remove border (on `clickDropContent`) |
- **CEDT207** CEDT207_2_0.html ↔ CEDT207_1.0.html (content, derivable=True)
  - gold: `div.row.clickDropContent.noBorder  «Me, my selfie and I»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [TITLE BAR]  [/RED TEXT]🔴**ME, MY SELFIE AND I** *|* *AHAU, TAKU WHAKAAHUA MATIHIKO, ME AU*`
- **ENG1004** ENG1004_0_0.html ↔ ENG1004_0.1.html (content, derivable=True)
  - gold: `div.row.clickDropContent.noBorder  «Context and presentation mode selection»`
  - Claude: `—`
  - WT: `🔴[RED TEXT] [H4]  [/RED TEXT]🔴Context and presentation mode selection`
- **ENGR101** ENGR101_7_0.html ↔ ENGR101_07.0.html (content, derivable=True)
  - gold: `div.row.clickDropContent.noBorder  «Write a news report»`
  - Claude: `—`
  - WT: `│ 🔴[RED TEXT] [image]  [/RED TEXT]🔴https://pixabay.com/photos/butterfly-monarch-butterfly-macro-3886065/ ║ 🔴[RED TEXT] [body]  [/RED TEXT]🔴Retell the news story to your supervisor. What were the main `
- modules: CEDT207, ENG1004, ENGR101, ENGS301, MXFL102, TRR114, XDLS501, XDLS901, XDLS902, XDLS903, XDLS904, XDLS905, XDLS906, XTAS101

### #6255 · body · EXTRA · `div.col-12` › gold `—` vs Claude `ul` — CANDIDATE
- pages 20 / modules 14 / lines 27; consensus (all) 0.88 of 1950 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 12m/18p c=0.87; Inquiry 1m/1p c=0.92; Fundamentals 1m/1p c=0.86
- by subject: Leaving to Learn 7m/12p c=0.77; ConnectED 2m/2p c=0.81; NCEA1 1m/2p c=0.72; 1-10 English 1m/1p c=0.96; 1-10 Mathematics 1m/1p c=0.93; Online Safety (OS9000) 1m/1p c=0.84
- by era: Refresh 14m/20p c=0.88
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1004** AGH1004_3_0.html ↔ AGH1004.03.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul  «The annual pattern of rainfall, temperature, frosts, wind speed and direction are called climatic factors.»`
- **CEDO501** CEDO501_2_1.html ↔ CEDO501_2.1.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul  «are 18–65 and studying full-time»`
- **CEDT104** CEDT104_0_0.html ↔ CEDT104 Waiata In Motion.html (structure, derivable=True)
  - gold: `—`
  - Claude: `ul  «Everyone learns rhythm differently.»`
- modules: AGH1004, CEDO501, CEDT104, ENGS302, MXEX301, OSAI301, TEFUN08, XDLS904, XDLS906, XDLS912, XGF9003, XGF9006, XLP01, XMES203

### #10907 · root · EXTRA · `body.container-fluid` › gold `—` vs Claude `div.row` — CANDIDATE
- pages 233 / modules 233 / lines 233; consensus (all) 0.87 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 225m/225p c=0.86; Inquiry 8m/8p c=0.94
- by subject: 1-10 Blended Literacy 69m/69p c=0.76; NCEA1 41m/41p c=0.91; 1-10 English 35m/35p c=0.88; 1-10 Mathematics 33m/33p c=0.90; Leaving to Learn 26m/26p c=0.87; Online Safety (OS9000) 10m/10p c=0.80
- by era: Refresh 233m/233p c=0.87
- authority (§1b): 3 — the module's own gold (group consensus ≥ 0.60)
- **AGH1001** AGH1001_0_0.html ↔ AGH1001.00.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row`
- **AGH1002** AGH1002_0_0.html ↔ AGH1002.00.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row`
- **AGH1003** AGH1003_0_0.html ↔ AGH1003_00.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `div.row`
- modules: AGH1001, AGH1002, AGH1003, AGH1004, AGH1005, AGH1006, AGH1007, AGH1008, AGH1009, ANZH101, ANZH104, ANZH105, ANZH203, ANZH205, ANZH301, ANZH303, ANZH304, ART1002, ART1003, ART1004, ART1005, ART1006, BLL111, BLL112 …

### #10912 · root · SUBSTITUTED · `#root` › gold `html.notranslate` vs Claude `body.container-fluid` — CANDIDATE
- pages 95 / modules 11 / lines 95; consensus (all) 0.05 of 1956 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 10m/84p c=0.05; Inquiry 1m/11p c=0.12
- by subject: ConnectED 5m/62p c=0.58; 1-10 English 2m/17p c=0.06; 1-10 Mathematics 2m/10p c=0.03; 1-10 Blended Literacy 1m/1p c=0.00; Leaving to Learn 1m/5p c=0.02
- by era: Refresh 11m/95p c=0.05
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:259 — **Action — the test is the MODULE CODE, not the reference files (constraint 89).** A module whose code begins with the letter **`X`** is a **learning 
  - KB: 06_TEMPLATE_RECOGNITION.md:281 — - [ ] **Cross-cutting modifiers:** `learningSupport` on `<html>`? **Required whenever the NEW module code begins with `X`** — derived from the code, n
  - KB: 06_TEMPLATE_RECOGNITION.md:313 — <html lang="en" level="" template="..." class="notranslate" translate="no">
- **BLL144** BLL144_1_0.html ↔ BLL144-1.0.html (structure, derivable=True)
  - gold: `html.notranslate  «Blended Literacy | BBL144»`
  - Claude: `body.container-fluid  «01»`
- **CEDK501** CEDK501_1_0.html ↔ CEDK501_1.0.html (structure, derivable=True)
  - gold: `html.notranslate  «CEDK501 1.0»`
  - Claude: `body.container-fluid  «1.0»`
- **CEDO501** CEDO501_0_0.html ↔ CEDO501_0.0.html (structure, derivable=True)
  - gold: `html.notranslate  «CEDO501 0.0»`
  - Claude: `body.container-fluid  «CEDO501»`
- modules: BLL144, CEDK501, CEDO501, CEDO502, CEDT501, CEDW501, ENGR202, ENGR301, MXEO401, MXFU401, XTAS101

## Below the floor (every remaining class with ≥ 2 modules — recorded, never dropped)

| # | region | dir | parent › gold › Claude | pages | modules | consensus | derivable |
|---|---|---|---|---|---|---|---|
| 151 | module-menu | MOVED | `div.col-md-8.col-12` › `h5` › `h5` | 7 | 3 | 0.22 | structure-only |
| 152 | module-menu | SUBSTITUTED | `div#module-menu-content.module` › `p` › `div.row` | 7 | 3 | 0.01 | structure-only |
| 153 | module-menu | SUBSTITUTED | `div.col-md-6.col-12.paddingR` › `h4>span` › `h5` | 5 | 3 | 0.03 | structure-only |
| 154 | module-menu | MISSING | `div.col-md-8.col-12` › `h3>span` › `—` | 4 | 3 | 0.01 | 0.67 |
| 155 | module-menu | EXTRA | `div.col-md-6.offset-md-0.col-1` › `—` › `h4>span` | 3 | 3 | 1.00 | structure-only |
| 156 | module-menu | EXTRA | `div.col-md-6.offset-md-0.col-1` › `—` › `h3>span` | 3 | 3 | 0.96 | structure-only |
| 157 | module-menu | MISSING | `ul` › `li>b` › `—` | 3 | 3 | 0.00 | 0.87 |
| 158 | module-menu | MISSING | `li` › `ul` › `—` | 3 | 3 | 0.01 | 1.00 |
| 159 | module-menu | MISSING | `div.col-md-6.col-12` › `h3>span` › `—` | 3 | 3 | 0.01 | 1.00 |
| 160 | module-menu | MISSING | `div.col-md-6.offset-md-0.col-1` › `p` › `—` | 3 | 3 | 0.00 | 0.75 |
| 161 | module-menu | MOVED | `div.col-md-6.col-12` › `p` › `p` | 3 | 3 | 0.01 | structure-only |
| 162 | module-menu | SUBSTITUTED | `div.col-md-6.col-12.paddingR` › `p` › `h5>span` | 3 | 3 | 0.07 | structure-only |
| 163 | module-menu | SUBSTITUTED | `ul` › `p` › `li` | 3 | 3 | 0.00 | structure-only |
| 164 | module-menu | SUBSTITUTED | `div.col-md-12.col-12.paddingR` › `p` › `h5` | 3 | 3 | 0.02 | structure-only |
| 165 | module-menu | SUBSTITUTED | `div.row` › `WIDGET` › `div.col-md-12.col-12.paddingR` | 3 | 3 | 0.11 | structure-only |
| 166 | module-menu | MISSING | `div.col-md-6.offset-md-0.col-1` › `p>b` › `—` | 19 | 2 | 0.01 | 0.68 |
| 167 | module-menu | SUBSTITUTED | `div.item` › `h5` › `div.col-md-8.col-12` | 16 | 2 | 0.01 | structure-only |
| 168 | module-menu | SUBSTITUTED | `ul` › `li` › `ul` | 16 | 2 | 0.59 | structure-only |
| 169 | module-menu | SUBSTITUTED | `div.row` › `div.col-md-8.col-12` › `h5` | 13 | 2 | 0.32 | structure-only |
| 170 | module-menu | MISSING | `div.col-md-6.col-12.paddingR` › `h3>span` › `—` | 10 | 2 | 0.01 | 1.00 |
| 171 | module-menu | SUBSTITUTED | `div.col-md-6.col-12.paddingL` › `p` › `li` | 10 | 2 | 0.03 | structure-only |
| 172 | module-menu | SUBSTITUTED | `div.col-md-6.col-12.paddingR` › `h5` › `h5>span` | 10 | 2 | 0.05 | structure-only |
| 173 | module-menu | SUBSTITUTED | `div.col-md-6.col-12.paddingR` › `p` › `p` | 10 | 2 | 0.07 | structure-only |
| 174 | module-menu | SUBSTITUTED | `div.col-md-6.col-12.paddingL` › `h3>span` › `li` | 10 | 2 | 0.01 | structure-only |
| 175 | module-menu | SUBSTITUTED | `div.row` › `div.col-md-6.col-sm-12` › `div.col-md-8.col-12` | 7 | 2 | 0.00 | structure-only |
| 176 | module-menu | MISSING | `div.col-md-6.col-sm-12` › `div.item` › `—` | 5 | 2 | 0.00 | 0.60 |
| 177 | module-menu | SUBSTITUTED | `div.col-md-6.offset-md-0.col-1` › `h3>span` › `p` | 5 | 2 | 0.05 | structure-only |
| 178 | module-menu | SUBSTITUTED | `div.col-md-8.col-12` › `h5` › `li` | 4 | 2 | 0.23 | structure-only |
| 179 | module-menu | EXTRA | `div.col-md-8.col-12` › `—` › `p>span.infoTrigger` | 3 | 2 | 1.00 | structure-only |
| 180 | module-menu | MISSING | `div.row` › `div.col-md-8.col-12` › `—` | 3 | 2 | 0.32 | 1.00 |
| 181 | module-menu | MISSING | `p>i` › `i` › `—` | 3 | 2 | 0.01 | 1.00 |
| 182 | module-menu | SUBSTITUTED | `div.col-md-8.col-12` › `h5` › `p` | 3 | 2 | 0.23 | structure-only |
| 183 | module-menu | SUBSTITUTED | `div.col-md-8.col-12` › `ul` › `p` | 3 | 2 | 0.29 | structure-only |
| 184 | module-menu | EXTRA | `h4>span` › `—` › `span` | 2 | 2 | 0.95 | structure-only |
| 185 | module-menu | EXTRA | `div.row` › `—` › `WIDGET` | 2 | 2 | 0.89 | structure-only |
| 186 | module-menu | EXTRA | `div.table-responsive` › `—` › `table.table.table-bordered` | 2 | 2 | 1.00 | structure-only |
| 187 | module-menu | EXTRA | `li` › `—` › `ul` | 2 | 2 | 1.00 | structure-only |
| 188 | module-menu | MISSING | `li` › `b` › `—` | 2 | 2 | 0.00 | 1.00 |
| 189 | module-menu | MISSING | `div.col-md-6.offset-md-0.col-1` › `h5` › `—` | 2 | 2 | 0.00 | 0.00 |
| 190 | module-menu | MISSING | `ul` › `li>i` › `—` | 2 | 2 | 0.00 | 0.67 |
| 191 | module-menu | MISSING | `div.col-md-6.col-12.paddingL` › `p` › `—` | 2 | 2 | 0.01 | 0.50 |
| 192 | module-menu | MISSING | `li>b` › `b` › `—` | 2 | 2 | 0.01 | 1.00 |
| 193 | module-menu | MISSING | `div.col-md-6.offset-md-0.col-1` › `h3>span` › `—` | 2 | 2 | 0.00 | 1.00 |
| 194 | module-menu | MISSING | `div.col-md-6.col-12.paddingL` › `ul` › `—` | 2 | 2 | 0.00 | 1.00 |
| 195 | module-menu | MISSING | `li` › `math` › `—` | 2 | 2 | 0.00 | 1.00 |
| 196 | module-menu | MOVED | `div.col-md-6.col-12.paddingR` › `p` › `p>i` | 2 | 2 | 0.06 | structure-only |
| 197 | module-menu | MOVED | `div.col-md-6.col-12.paddingL` › `h4>span` › `h4` | 2 | 2 | 0.01 | structure-only |
| 198 | module-menu | SUBSTITUTED | `div.col-md-6.offset-md-0.col-1` › `h5` › `p` | 2 | 2 | 0.01 | structure-only |
| 199 | module-menu | SUBSTITUTED | `div.col-md-6.col-12` › `p` › `h5` | 2 | 2 | 0.02 | structure-only |
| 200 | module-menu | SUBSTITUTED | `p` › `br` › `b` | 2 | 2 | 0.03 | structure-only |
| 201 | module-menu | SUBSTITUTED | `div.row` › `div.col-md-6.offset-md-0.col-12.padd` › `div.col-md-6.col-12.paddingR` | 2 | 2 | 0.01 | structure-only |
| 202 | module-menu | SUBSTITUTED | `div.row` › `div.col-md-6.col-12.paddingL` › `h5` | 2 | 2 | 0.04 | structure-only |
| 203 | module-menu | SUBSTITUTED | `div.row` › `div.col-md-6.col-12` › `h4>span` | 2 | 2 | 0.02 | structure-only |
| 204 | module-menu | SUBSTITUTED | `div.row` › `div.col-md-6.offset-md-0.col-12.padd` › `div.col-md-6.offset-md-0.col-12` | 2 | 2 | 0.01 | structure-only |
| 205 | module-menu | SUBSTITUTED | `div.col-md-6.offset-md-0.col-1` › `ul` › `p` | 2 | 2 | 0.01 | structure-only |
| 206 | module-menu | SUBSTITUTED | `div.row` › `div.col-md-12.col-12` › `div.col-md-8.col-12` | 2 | 2 | 0.01 | structure-only |
| 207 | module-menu | SUBSTITUTED | `div.col-md-6.col-12.paddingL` › `ul` › `p` | 2 | 2 | 0.04 | structure-only |
| 208 | module-menu | SUBSTITUTED | `div.col-md-6.col-12.paddingR` › `h4>span` › `p>b` | 2 | 2 | 0.03 | structure-only |
| 366 | crumbs | MISSING | `div.crumbs` › `div` › `—` | 13 | 10 | 0.02 | 0.95 |
| 367 | crumbs | SUBSTITUTED | `div#body` › `div.crumbs` › `div.row` | 5 | 5 | 0.02 | structure-only |
| 368 | crumbs | SUBSTITUTED | `div.crumbs` › `div.showing` › `div.col-md-8.col-12` | 5 | 5 | 0.02 | structure-only |
| 369 | crumbs | EXTRA | `div.crumbs` › `—` › `div` | 4 | 4 | 1.00 | structure-only |
| 370 | phases-nav | MISSING | `div` › `p` › `—` | 4 | 4 | 0.01 | 1.00 |
| 371 | phases-nav | SUBSTITUTED | `div.phases` › `div` › `div.row` | 4 | 4 | 0.03 | structure-only |
| 372 | phases-nav | MISSING | `div.phases` › `div` › `—` | 3 | 3 | 0.03 | 1.00 |
| 373 | phases-nav | SUBSTITUTED | `div#body` › `div.phases` › `div.row` | 3 | 3 | 0.03 | structure-only |
| 374 | phases-nav | SUBSTITUTED | `div.phases` › `div` › `div.col-md-8.col-12` | 3 | 3 | 0.03 | structure-only |
| 375 | crumbs | SUBSTITUTED | `div.crumbs` › `div` › `div.row` | 3 | 3 | 0.02 | structure-only |
| 376 | crumbs | EXTRA | `div.crumbs` › `—` › `div.showing` | 2 | 2 | 0.98 | structure-only |
| 377 | crumbs | SUBSTITUTED | `div.crumbs` › `div` › `div.videoSection.ratio.ratio-16x9` | 2 | 2 | 0.02 | structure-only |
| 378 | phases-nav | SUBSTITUTED | `div#body` › `div.phases` › `div.crumbs` | 2 | 2 | 0.03 | structure-only |
| 392 | footer | EXTRA | `ul.footer-nav` › `—` › `li>a.home-nav` | 213 | 71 | 0.15 | structure-only |
| 393 | footer | MISSING | `div#body` › `div#footer` › `—` | 83 | 70 | 0.07 | structure-only |
| 394 | footer | EXTRA | `li>a#next-lesson` › `—` › `a#next-lesson` | 132 | 68 | 0.17 | structure-only |
| 395 | footer | EXTRA | `body.container-fluid` › `—` › `div#footer` | 92 | 68 | 0.26 | structure-only |
| 400 | footer | EXTRA | `div#footer` › `—` › `ul.footer-nav` | 31 | 27 | 0.16 | structure-only |
| 401 | footer | SUBSTITUTED | `div#body` › `div#footer` › `div#footer` | 23 | 23 | 0.07 | structure-only |
| 405 | footer | SUBSTITUTED | `div#body` › `div#footer` › `ul.footer-nav.inquiry-nav` | 17 | 16 | 0.07 | structure-only |
| 413 | footer | MISSING | `li>a.home-nav` › `a.home-nav` › `—` | 25 | 9 | 0.99 | structure-only |
| 414 | footer | EXTRA | `li>a#prev-lesson` › `—` › `a#prev-lesson` | 12 | 9 | 0.19 | structure-only |
| 415 | footer | EXTRA | `ul.footer-nav` › `—` › `li>a#next-lesson` | 11 | 9 | 0.28 | structure-only |
| 416 | footer | MISSING | `div.row` › `div#footer` › `—` | 10 | 9 | 0.01 | structure-only |
| 417 | footer | MISSING | `ul.footer-nav.inquiry-nav` › `li>a#next-lesson` › `—` | 9 | 9 | 0.10 | structure-only |
| 418 | footer | MISSING | `ul.footer-nav.fundamentals-nav` › `li>a.home-nav` › `—` | 9 | 9 | 0.01 | structure-only |
| 419 | footer | SUBSTITUTED | `ul.footer-nav` › `li>a.home-nav` › `li>a.home-nav` | 8 | 8 | 0.85 | structure-only |
| 420 | footer | EXTRA | `body.inquiry.container-fluid` › `—` › `div#footer` | 9 | 7 | 0.98 | structure-only |
| 421 | footer | EXTRA | `ul.footer-nav.inquiry-nav` › `—` › `li>a#next-lesson` | 7 | 7 | 0.90 | structure-only |
| 422 | footer | MISSING | `ul.footer-nav.inquiry-nav` › `li>a#prev-lesson` › `—` | 7 | 7 | 0.10 | structure-only |
| 423 | footer | SUBSTITUTED | `ul.footer-nav` › `li>a#prev-lesson` › `li>a#prev-lesson` | 7 | 7 | 0.71 | structure-only |
| 424 | footer | EXTRA | `body.fundamentals.container-fl` › `—` › `div#footer` | 6 | 6 | 0.98 | structure-only |
| 425 | footer | EXTRA | `ul.footer-nav.inquiry-nav` › `—` › `li>a#prev-lesson` | 6 | 6 | 0.90 | structure-only |
| 426 | footer | SUBSTITUTED | `ul.footer-nav` › `li>a#next-lesson` › `li>a.home-nav` | 6 | 6 | 0.72 | structure-only |
| 427 | footer | SUBSTITUTED | `div#footer` › `ul.footer-nav` › `ul.footer-nav.fundamentals-nav` | 6 | 6 | 0.84 | structure-only |
| 428 | footer | SUBSTITUTED | `div#footer` › `ul.footer-nav.inquiry-nav` › `ul.footer-nav` | 12 | 5 | 0.14 | structure-only |
| 429 | footer | MISSING | `div#footer` › `ul.footer-nav.inquiry-nav` › `—` | 5 | 5 | 0.14 | structure-only |
| 430 | footer | SUBSTITUTED | `div#footer` › `ul.fundamentals-nav.footer-nav` › `ul.footer-nav.fundamentals-nav` | 5 | 5 | 0.00 | structure-only |
| 431 | footer | SUBSTITUTED | `div#footer` › `ul.footer-nav.inquiry-nav` › `ul.footer-nav.inquiry-nav` | 5 | 5 | 0.14 | structure-only |
| 432 | footer | SUBSTITUTED | `div#body` › `div#footer` › `div.col-md-8.col-12` | 5 | 5 | 0.07 | structure-only |
| 433 | footer | EXTRA | `ul.footer-nav` › `—` › `li>a#prev-lesson` | 4 | 4 | 0.29 | structure-only |
| 434 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` › `li>a.home-nav` › `li>a.home-nav` | 4 | 4 | 0.14 | structure-only |
| 435 | footer | SUBSTITUTED | `li>a#next-lesson` › `a#next-lesson` › `a.home-nav` | 4 | 4 | 0.82 | structure-only |
| 436 | footer | SUBSTITUTED | `ul.footer-nav` › `li>a.home-nav` › `li>a#next-lesson` | 4 | 4 | 0.85 | structure-only |
| 437 | footer | SUBSTITUTED | `ul.footer-nav` › `li>a.home-nav` › `li>a#prev-lesson` | 4 | 4 | 0.85 | structure-only |
| 438 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` › `li>a#next-lesson` › `li>a#next-lesson` | 3 | 3 | 0.10 | structure-only |
| 439 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` › `li>a#prev-lesson` › `li>a.home-nav` | 3 | 3 | 0.10 | structure-only |
| 440 | footer | SUBSTITUTED | `div#footer` › `ul.footer-nav.fundamentals-nav` › `ul.footer-nav.fundamentals-nav` | 3 | 3 | 0.01 | structure-only |
| 441 | footer | SUBSTITUTED | `ul.footer-nav.fundamentals-nav` › `li>a.home-nav` › `li>a.home-nav` | 3 | 3 | 0.01 | structure-only |
| 442 | footer | SUBSTITUTED | `ul.footer-nav` › `li>a#prev-lesson` › `li>a#next-lesson` | 3 | 3 | 0.71 | structure-only |
| 443 | footer | SUBSTITUTED | `li>a.home-nav` › `a.home-nav` › `a#prev-lesson` | 3 | 3 | 0.99 | structure-only |
| 444 | footer | SUBSTITUTED | `ul.footer-nav` › `li>a#next-lesson` › `li>a#prev-lesson` | 3 | 3 | 0.72 | structure-only |
| 445 | footer | SUBSTITUTED | `ul.footer-nav` › `li>a#prev-lesson` › `p` | 3 | 3 | 0.71 | structure-only |
| 446 | footer | MISSING | `li>a.active` › `a.active` › `—` | 11 | 2 | 0.01 | structure-only |
| 447 | footer | MISSING | `ul.footer-nav` › `li>a.active` › `—` | 6 | 2 | 0.01 | structure-only |
| 448 | footer | MISSING | `body.inquiry.container-fluid` › `div#footer.inquiry-footer` › `—` | 4 | 2 | 0.00 | structure-only |
| 449 | footer | EXTRA | `body.container-fluid.mathJax` › `—` › `div#footer` | 3 | 2 | 0.95 | structure-only |
| 450 | footer | SUBSTITUTED | `div#body` › `div#footer` › `ul.footer-nav` | 3 | 2 | 0.07 | structure-only |
| 451 | footer | EXTRA | `div#footer` › `—` › `ul.footer-nav.fundamentals-nav` | 2 | 2 | 0.99 | structure-only |
| 452 | footer | MISSING | `div#footer.inquiry-footer` › `ul.footer-nav` › `—` | 2 | 2 | 0.00 | structure-only |
| 453 | footer | SUBSTITUTED | `ul.fundamentals-nav.footer-nav` › `li>a.home-nav` › `li>a.home-nav` | 2 | 2 | 0.00 | structure-only |
| 454 | footer | SUBSTITUTED | `li>a#prev-lesson` › `a#prev-lesson` › `a#next-lesson` | 2 | 2 | 0.81 | structure-only |
| 455 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` › `li>a.home-nav` › `li>a#prev-lesson` | 2 | 2 | 0.14 | structure-only |
| 456 | footer | SUBSTITUTED | `li>a#next-lesson` › `a#next-lesson` › `a#prev-lesson` | 2 | 2 | 0.82 | structure-only |
| 457 | footer | SUBSTITUTED | `div#footer` › `ul.footer-nav.inquiry-nav` › `li>a#prev-lesson` | 2 | 2 | 0.14 | structure-only |
| 458 | footer | SUBSTITUTED | `div#footer` › `ul.footer-nav.inquiry-nav` › `li>a.home-nav` | 2 | 2 | 0.14 | structure-only |
| 459 | footer | SUBSTITUTED | `div#footer` › `ul.footer-nav` › `li>a.home-nav` | 2 | 2 | 0.84 | structure-only |
| 460 | footer | SUBSTITUTED | `div#body` › `div#footer` › `div.acks.acksTemplate` | 2 | 2 | 0.07 | structure-only |
| 461 | footer | SUBSTITUTED | `div#body` › `div#footer` › `div.row` | 2 | 2 | 0.07 | structure-only |
| 462 | footer | SUBSTITUTED | `div#footer` › `ul.footer-nav` › `div.col-md-8.col-12` | 2 | 2 | 0.84 | structure-only |
| 463 | footer | SUBSTITUTED | `div#body` › `div#footer` › `div.col-12` | 2 | 2 | 0.07 | structure-only |
| 464 | footer | SUBSTITUTED | `div#footer` › `ul.footer-nav.fundamentals-nav` › `ul.footer-nav` | 2 | 2 | 0.01 | structure-only |
| 465 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` › `li>a#next-lesson` › `li>a#prev-lesson` | 2 | 2 | 0.10 | structure-only |
| 507 | acks | SUBSTITUTED | `div.col-md-8.col-12` › `div.acks.acksTemplate.acksAI` › `div.acks.acksTemplate` | 17 | 17 | 0.01 | structure-only |
| 508 | acks | EXTRA | `div.col-md-8.col-12` › `—` › `div.acks.acksTemplate` | 5 | 5 | 0.99 | structure-only |
| 509 | acks | MISSING | `div.acks` › `WIDGET` › `—` | 5 | 5 | 0.17 | structure-only |
| 510 | acks | SUBSTITUTED | `div.col-md-8.col-12` › `div.acks` › `div.acks.acksTemplate.acksAI` | 5 | 5 | 0.17 | structure-only |
| 511 | acks | SUBSTITUTED | `div.acks` › `WIDGET` › `div.col-md-8.col-12` | 4 | 4 | 0.17 | structure-only |
| 512 | acks | EXTRA | `div.acks.acksTemplate` › `—` › `WIDGET` | 3 | 3 | 0.99 | structure-only |
| 513 | acks | SUBSTITUTED | `div.acks` › `WIDGET` › `WIDGET` | 3 | 3 | 0.17 | structure-only |
| 514 | acks | SUBSTITUTED | `div.acks` › `WIDGET` › `div.row` | 3 | 3 | 0.17 | structure-only |
| 515 | acks | SUBSTITUTED | `div.col-md-8.col-12` › `div.acks.acksTemplate` › `div.acks.acksTemplate` | 3 | 3 | 0.01 | structure-only |
| 516 | acks | SUBSTITUTED | `div.acks.acksTemplate` › `WIDGET` › `WIDGET` | 3 | 3 | 0.01 | structure-only |
| 517 | acks | SUBSTITUTED | `div.col-md-8.col-12` › `div.acks` › `div.row` | 3 | 3 | 0.17 | structure-only |
| 518 | acks | SUBSTITUTED | `div.col-md-8.col-12` › `div.acks` › `h4` | 2 | 2 | 0.17 | structure-only |
| 519 | acks | SUBSTITUTED | `div.col-md-8.col-12` › `div.acks` › `WIDGET` | 2 | 2 | 0.17 | structure-only |
| 520 | acks | SUBSTITUTED | `div.col-md-8.col-12` › `div.acks` › `p` | 2 | 2 | 0.17 | structure-only |
| 521 | acks | SUBSTITUTED | `div.col-md-8.col-12` › `div.acks` › `div.activity[number=2D]` | 2 | 2 | 0.17 | structure-only |
| 536 | activity | MISSING | `div.col-12` › `WIDGET` › `—` | 345 | 211 | 0.17 | structure-only |
| 542 | activity | MISSING | `div.col-12` › `div.row` › `—` | 202 | 146 | 0.22 | 0.95 |
| 545 | activity | MOVED | `div.col-12` › `p` › `p` | 119 | 98 | 0.15 | structure-only |
| 547 | activity | MISSING | `div.row` › `div.col-12` › `—` | 108 | 85 | 0.27 | 0.88 |
| 548 | activity | MISSING | `div.col-12` › `img.img-fluid` › `—` | 105 | 82 | 0.12 | structure-only |
| 549 | activity | MISSING | `div.col-12` › `div.clickDropContent` › `—` | 98 | 80 | 0.05 | 0.96 |
| 554 | activity | SUBSTITUTED | `div.row` › `div.col-md-8.col-12` › `div.col-12` | 109 | 73 | 0.14 | structure-only |
| 555 | activity | MISSING | `div.col-12` › `ul` › `—` | 89 | 73 | 0.06 | 0.76 |
| 556 | activity | MISSING | `a` › `div.externalButton` › `—` | 105 | 71 | 0.10 | 0.52 |
| 559 | activity | MISSING | `div.col-12` › `div.hint` › `—` | 74 | 65 | 0.07 | structure-only |
| 561 | activity | MISSING | `div.col-12` › `ol` › `—` | 86 | 58 | 0.13 | 0.95 |
| 563 | activity | MISSING | `p` › `br` › `—` | 76 | 54 | 0.04 | structure-only |
| 564 | activity | MOVED | `a` › `div.button` › `div.button` | 68 | 53 | 0.23 | structure-only |
| 565 | activity | MOVED | `div.col-12` › `h3` › `h3` | 76 | 52 | 0.23 | structure-only |
| 567 | activity | MISSING | `div.col-12` › `br` › `—` | 75 | 51 | 0.03 | structure-only |
| 568 | activity | MISSING | `div.col-12` › `h4` › `—` | 65 | 51 | 0.07 | 0.80 |
| 573 | activity | MOVED | `ul` › `li` › `li` | 70 | 48 | 0.08 | structure-only |
| 577 | activity | MISSING | `div.col-12` › `div.table-responsive` › `—` | 57 | 46 | 0.08 | 0.93 |
| 578 | activity | SUBSTITUTED | `div.col-12` › `div.row` › `WIDGET` | 49 | 44 | 0.22 | structure-only |
| 580 | activity | MISSING | `div.col-12` › `p>b` › `—` | 50 | 41 | 0.05 | 0.76 |
| 581 | activity | SUBSTITUTED | `div.row` › `div.col-md-12.col-12` › `div.col-12` | 53 | 40 | 0.11 | structure-only |
| 583 | activity | MISSING | `div.row` › `div.col-md-8.col-12` › `—` | 53 | 39 | 0.06 | 0.94 |
| 584 | activity | SUBSTITUTED | `div.col-12` › `div.table-responsive` › `WIDGET` | 41 | 39 | 0.08 | structure-only |
| 587 | activity | MOVED | `ol` › `li` › `li` | 58 | 36 | 0.07 | structure-only |
| 588 | activity | MOVED | `ul` › `li` › `li` | 41 | 36 | 0.05 | structure-only |
| 589 | activity | MISSING | `div.row` › `div.col-md-12.col-12` › `—` | 44 | 35 | 0.05 | 0.97 |
| 590 | activity | MISSING | `a` › `div.buttonD` › `—` | 44 | 35 | 0.04 | 0.59 |
| 591 | activity | SUBSTITUTED | `div.videoSection.icon.ratio.ra` › `iframe.embed-responsive-item` › `iframe` | 68 | 34 | 0.08 | structure-only |
| 592 | activity | MISSING | `div.col-12` › `h4.goJournal` › `—` | 64 | 34 | 0.12 | 0.55 |
| 593 | activity | MISSING | `ol` › `li` › `—` | 41 | 34 | 0.06 | 0.95 |
| 595 | activity | MOVED | `div.col-md-8.col-12` › `p` › `p` | 39 | 30 | 0.04 | structure-only |
| 596 | activity | MISSING | `div.col-md-8.col-12` › `p` › `—` | 37 | 30 | 0.04 | 0.73 |
| 597 | activity | MISSING | `p>i` › `i` › `—` | 32 | 30 | 0.12 | 1.00 |
| 599 | activity | MOVED | `a` › `div.buttonD` › `div.buttonD` | 31 | 30 | 0.04 | structure-only |
| 601 | activity | SUBSTITUTED | `ul` › `li` › `li` | 33 | 28 | 0.20 | structure-only |
| 602 | activity | MISSING | `ul` › `li` › `—` | 32 | 28 | 0.07 | 0.81 |
| 604 | activity | MISSING | `div.col-12` › `div.hintDropContent` › `—` | 35 | 27 | 0.08 | 0.94 |
| 605 | activity | MISSING | `div.col-12` › `div.row.flipCardsContainer` › `—` | 32 | 27 | 0.04 | structure-only |
| 606 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 27 | 27 | 0.01 | 0.88 |
| 607 | activity | MISSING | `div.col-12` › `div.videoSection.icon.ratio.ratio-16` › `—` | 40 | 26 | 0.09 | structure-only |
| 609 | activity | MOVED | `div.col-md-8.col-12` › `p` › `p` | 31 | 26 | 0.08 | structure-only |
| 611 | activity | MISSING | `div.col-12` › `h5` › `—` | 36 | 25 | 0.04 | 0.86 |
| 613 | activity | SUBSTITUTED | `div.col-12` › `div.row` › `p` | 26 | 24 | 0.22 | structure-only |
| 615 | activity | MISSING | `div.row` › `WIDGET` › `—` | 24 | 24 | 0.04 | structure-only |
| 617 | activity | MOVED | `div.clickDropContent` › `p` › `p` | 30 | 23 | 0.04 | structure-only |
| 618 | activity | MOVED | `div.col-md-8.col-12` › `h3` › `h3` | 27 | 23 | 0.04 | structure-only |
| 619 | activity | SUBSTITUTED | `a` › `div.button` › `div.row` | 27 | 23 | 0.48 | structure-only |
| 620 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 23 | 23 | 0.01 | 0.92 |
| 622 | activity | SUBSTITUTED | `ol` › `li` › `li` | 32 | 22 | 0.17 | structure-only |
| 623 | activity | MISSING | `div.col-12` › `p>i` › `—` | 29 | 22 | 0.10 | 0.72 |
| 625 | activity | MISSING | `p>b` › `b` › `—` | 23 | 22 | 0.07 | 0.93 |
| 626 | activity | MISSING | `a` › `div.button.downloadButton` › `—` | 32 | 21 | 0.03 | 0.36 |
| 627 | activity | MOVED | `ol` › `li` › `li` | 25 | 21 | 0.04 | structure-only |
| 628 | activity | MISSING | `div.videoSection.icon.ratio.ra` › `iframe.embed-responsive-item` › `—` | 24 | 21 | 0.03 | structure-only |
| 630 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 21 | 21 | 0.01 | 0.77 |
| 632 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=1A]` › `div.activity[number=1A]` | 21 | 21 | 0.05 | structure-only |
| 633 | activity | MISSING | `div.col-md-8.col-12` › `h3` › `—` | 24 | 20 | 0.12 | 0.70 |
| 634 | activity | SUBSTITUTED | `a` › `div.button` › `div.col-md-8.col-12` | 21 | 20 | 0.48 | structure-only |
| 635 | activity | MOVED | `div.col-12` › `h4.goJournal` › `h4.goJournal` | 50 | 19 | 0.05 | structure-only |
| 637 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=2A]` › `div.activity[number=2A]` | 19 | 19 | 0.06 | structure-only |
| 640 | activity | MISSING | `div.col-12` › `div.videoSection.ratio.ratio-16x9` › `—` | 19 | 18 | 0.05 | structure-only |
| 641 | activity | MISSING | `div.row` › `div.col-md-4.col-12` › `—` | 19 | 18 | 0.01 | 0.98 |
| 643 | activity | MISSING | `p` › `b` › `—` | 21 | 17 | 0.07 | 0.96 |
| 645 | activity | SUBSTITUTED | `a` › `div.button` › `WIDGET` | 18 | 17 | 0.48 | structure-only |
| 646 | activity | SUBSTITUTED | `div.clickDropContent` › `p` › `p` | 18 | 17 | 0.07 | structure-only |
| 647 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 17 | 17 | 0.01 | 0.87 |
| 648 | activity | MOVED | `div.col-12` › `a` › `a` | 22 | 16 | 0.29 | structure-only |
| 649 | activity | SUBSTITUTED | `div.col-12` › `div.videoSection.icon.ratio.ratio-16` › `div.videoSection.ratio.ratio-16x9` | 29 | 15 | 0.09 | structure-only |
| 652 | activity | MOVED | `div.col-12` › `p>b` › `p>b` | 21 | 15 | 0.05 | structure-only |
| 653 | activity | SUBSTITUTED | `div.row` › `div.col-12` › `div.button` | 18 | 15 | 0.79 | structure-only |
| 654 | activity | MISSING | `div.col-md-12.col-12` › `WIDGET` › `—` | 17 | 15 | 0.04 | structure-only |
| 655 | activity | SUBSTITUTED | `div.row` › `div.col-8` › `div.col-12` | 16 | 15 | 0.02 | structure-only |
| 656 | activity | EXTRA | `div.col-12` › `—` › `div.ratio.ratio-16x9` | 15 | 15 | 1.00 | structure-only |
| 657 | activity | MISSING | `div.row.flipCardsContainer` › `div.col-md-4.col-12.paddingLR` › `—` | 15 | 15 | 0.01 | structure-only |
| 658 | activity | MOVED | `a` › `div.button` › `div.button` | 15 | 15 | 0.06 | structure-only |
| 659 | activity | SUBSTITUTED | `div.col-12` › `h4.goJournal` › `p` | 28 | 14 | 0.12 | structure-only |
| 661 | activity | MISSING | `div.col-md-12.col-12` › `p` › `—` | 19 | 14 | 0.03 | 0.76 |
| 662 | activity | SUBSTITUTED | `div.col-12` › `WIDGET` › `WIDGET` | 18 | 14 | 0.60 | structure-only |
| 663 | activity | SUBSTITUTED | `div.col-12` › `img.img-fluid` › `p>a` | 17 | 14 | 0.12 | structure-only |
| 664 | activity | EXTRA | `div.videoSection.icon.ratio.ra` › `—` › `iframe` | 16 | 14 | 0.99 | structure-only |
| 665 | activity | MISSING | `div.table-responsive` › `table.table.table-bordered` › `—` | 16 | 14 | 0.03 | 0.95 |
| 666 | activity | SUBSTITUTED | `div.col-12` › `p` › `p>b` | 16 | 14 | 0.76 | structure-only |
| 667 | activity | MOVED | `div.clickDropContent` › `p` › `p` | 15 | 14 | 0.05 | structure-only |
| 668 | activity | EXTRA | `div.activity[number=3A]` › `—` › `div.row` | 14 | 14 | 0.97 | structure-only |
| 669 | activity | EXTRA | `div.activity.interactive[numbe` › `—` › `div.row` | 14 | 14 | 0.90 | structure-only |
| 670 | activity | MISSING | `div.row` › `div.row` › `—` | 14 | 14 | 0.02 | 0.79 |
| 671 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 14 | 14 | 0.01 | 0.93 |
| 672 | activity | SUBSTITUTED | `div.col-12` › `ul` › `p` | 18 | 13 | 0.17 | structure-only |
| 673 | activity | MOVED | `div.col-12` › `h4.goJournal` › `h4.goJournal` | 17 | 13 | 0.03 | structure-only |
| 674 | activity | SUBSTITUTED | `a` › `div.button` › `div.externalButton` | 17 | 13 | 0.48 | structure-only |
| 675 | activity | MISSING | `div.clickDropContent` › `p` › `—` | 16 | 13 | 0.02 | 0.91 |
| 676 | activity | SUBSTITUTED | `div.col-12` › `p` › `h3` | 16 | 13 | 0.76 | structure-only |
| 677 | activity | MISSING | `div.col-12` › `div.slider` › `—` | 15 | 13 | 0.01 | 0.67 |
| 678 | activity | SUBSTITUTED | `div.row` › `WIDGET` › `WIDGET` | 15 | 13 | 0.04 | structure-only |
| 679 | activity | MISSING | `p` › `span.infoTrigger` › `—` | 14 | 13 | 0.01 | 0.91 |
| 680 | activity | MISSING | `div.row` › `a` › `—` | 13 | 13 | 0.01 | 0.69 |
| 681 | activity | SUBSTITUTED | `div.col-12` › `div.row` › `img.img-fluid` | 13 | 13 | 0.22 | structure-only |
| 682 | activity | MISSING | `div.col-12` › `div.row.selectionBox` › `—` | 15 | 12 | 0.02 | 0.82 |
| 683 | activity | SUBSTITUTED | `div.col-12` › `WIDGET` › `img.img-fluid` | 15 | 12 | 0.60 | structure-only |
| 684 | activity | SUBSTITUTED | `a` › `div.button` › `div.button` | 14 | 12 | 0.48 | structure-only |
| 685 | activity | MOVED | `div.col-md-12.col-12` › `p` › `p` | 13 | 12 | 0.03 | structure-only |
| 686 | activity | MOVED | `tr` › `td` › `td` | 13 | 12 | 0.05 | structure-only |
| 687 | activity | EXTRA | `table.table.table-bordered` › `—` › `tr` | 12 | 12 | 0.99 | structure-only |
| 688 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 12 | 12 | 0.01 | 1.00 |
| 689 | activity | MISSING | `div.activity[number=1A]` › `div.row` › `—` | 12 | 12 | 0.05 | 0.83 |
| 690 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 12 | 12 | 0.01 | 1.00 |
| 691 | activity | MOVED | `a` › `div.buttonD` › `div.buttonD` | 12 | 12 | 0.04 | structure-only |
| 692 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=1B]` › `div.activity[number=1B]` | 12 | 12 | 0.01 | structure-only |
| 693 | activity | SUBSTITUTED | `div.row` › `div.col-12` › `div.col-12` | 12 | 12 | 0.79 | structure-only |
| 694 | activity | MOVED | `div.col-12` › `p>i` › `p` | 15 | 11 | 0.03 | structure-only |
| 695 | activity | EXTRA | `div.clickDropContent` › `—` › `p` | 13 | 11 | 0.95 | structure-only |
| 696 | activity | SUBSTITUTED | `div.col-12` › `h3` › `h3` | 13 | 11 | 0.76 | structure-only |
| 697 | activity | MISSING | `div.table-responsive` › `table.table.tableFixed.table-bordere` › `—` | 12 | 11 | 0.01 | 0.92 |
| 698 | activity | MISSING | `div.videoSection.ratio.ratio-1` › `iframe` › `—` | 12 | 11 | 0.07 | structure-only |
| 699 | activity | EXTRA | `div.col-12` › `—` › `div.table-responsive` | 11 | 11 | 0.92 | structure-only |
| 700 | activity | EXTRA | `div.activity.interactive[numbe` › `—` › `div.row` | 11 | 11 | 0.93 | structure-only |
| 701 | activity | MISSING | `div.row` › `div.col-4` › `—` | 11 | 11 | 0.00 | structure-only |
| 702 | activity | MISSING | `div.col-12` › `audio.audioPlayer.icon` › `—` | 11 | 11 | 0.01 | structure-only |
| 703 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=3A]` › `div.activity[number=3A]` | 11 | 11 | 0.04 | structure-only |
| 704 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=2C]` › `div.activity[number=2C]` | 11 | 11 | 0.03 | structure-only |
| 705 | activity | SUBSTITUTED | `tr` › `td` › `td` | 11 | 11 | 0.09 | structure-only |
| 706 | activity | SUBSTITUTED | `div.col-12` › `h3` › `h4` | 16 | 10 | 0.76 | structure-only |
| 707 | activity | EXTRA | `p` › `—` › `i` | 12 | 10 | 0.98 | structure-only |
| 708 | activity | SUBSTITUTED | `div.col-12` › `WIDGET` › `p>b` | 12 | 10 | 0.60 | structure-only |
| 709 | activity | SUBSTITUTED | `div.col-12` › `div.clickDropContent` › `div.row` | 12 | 10 | 0.10 | structure-only |
| 710 | activity | MISSING | `div.row` › `p` › `—` | 11 | 10 | 0.02 | 0.92 |
| 711 | activity | MISSING | `div.col-12` › `div.TKmodal` › `—` | 11 | 10 | 0.01 | 1.00 |
| 712 | activity | SUBSTITUTED | `a` › `div.button` › `li` | 11 | 10 | 0.48 | structure-only |
| 713 | activity | SUBSTITUTED | `div.row` › `div.col-12` › `p` | 11 | 10 | 0.79 | structure-only |
| 714 | activity | SUBSTITUTED | `div.col-12` › `div.clickDropContent` › `WIDGET` | 11 | 10 | 0.10 | structure-only |
| 715 | activity | SUBSTITUTED | `div.row` › `div.col-12` › `div.table-responsive` | 11 | 10 | 0.79 | structure-only |
| 716 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 10 | 10 | 0.00 | 0.92 |
| 717 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 10 | 10 | 0.04 | 0.82 |
| 718 | activity | MISSING | `p` › `i` › `—` | 10 | 10 | 0.02 | 1.00 |
| 719 | activity | MISSING | `p>span.infoTrigger` › `span.infoTrigger` › `—` | 10 | 10 | 0.04 | 0.82 |
| 720 | activity | SUBSTITUTED | `div.col-12` › `WIDGET` › `ul` | 10 | 10 | 0.60 | structure-only |
| 721 | activity | SUBSTITUTED | `div.col-12` › `div.row` › `div.row` | 10 | 10 | 0.22 | structure-only |
| 722 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=2A]` › `div.activity[number=2A]` | 10 | 10 | 0.01 | structure-only |
| 723 | activity | SUBSTITUTED | `div.col-12` › `h3` › `ol` | 10 | 10 | 0.76 | structure-only |
| 724 | activity | MISSING | `li` › `ol` › `—` | 14 | 9 | 0.01 | 1.00 |
| 725 | activity | SUBSTITUTED | `div.col-12` › `br` › `p` | 13 | 9 | 0.06 | structure-only |
| 726 | activity | MOVED | `div.col-12` › `h4` › `h4` | 12 | 9 | 0.03 | structure-only |
| 727 | activity | MISSING | `div.col-12` › `div.col-12` › `—` | 11 | 9 | 0.02 | 1.00 |
| 728 | activity | SUBSTITUTED | `a` › `div.externalButton` › `div.button` | 11 | 9 | 0.10 | structure-only |
| 729 | activity | EXTRA | `div.col-md-4.col-12.paddingLR` › `—` › `WIDGET` | 10 | 9 | 0.98 | structure-only |
| 730 | activity | EXTRA | `div.table-responsive` › `—` › `table.table.table-bordered` | 10 | 9 | 0.97 | structure-only |
| 731 | activity | EXTRA | `tr` › `—` › `th` | 10 | 9 | 0.99 | structure-only |
| 732 | activity | EXTRA | `div.row` › `—` › `div.col-md-8.col-12` | 10 | 9 | 0.94 | structure-only |
| 733 | activity | SUBSTITUTED | `div.col-12` › `h3` › `p` | 10 | 9 | 0.76 | structure-only |
| 734 | activity | SUBSTITUTED | `div.col-12` › `img.img-fluid` › `p` | 10 | 9 | 0.12 | structure-only |
| 735 | activity | SUBSTITUTED | `div.col-12` › `ol` › `p` | 10 | 9 | 0.13 | structure-only |
| 736 | activity | SUBSTITUTED | `div.col-12` › `div.row.flipCardsContainer` › `WIDGET` | 10 | 9 | 0.04 | structure-only |
| 737 | activity | SUBSTITUTED | `div.col-12` › `WIDGET` › `a` | 10 | 9 | 0.60 | structure-only |
| 738 | activity | SUBSTITUTED | `div.col-12` › `div.row` › `p>a` | 10 | 9 | 0.22 | structure-only |
| 739 | activity | EXTRA | `div.row.flipCardsContainer` › `—` › `div.col-md-4.col-12.paddingLR` | 9 | 9 | 0.99 | structure-only |
| 740 | activity | MISSING | `div.row` › `div.col` › `—` | 9 | 9 | 0.01 | 1.00 |
| 741 | activity | MISSING | `div.col-12` › `p>span.infoTrigger` › `—` | 9 | 9 | 0.03 | 1.00 |
| 742 | activity | MISSING | `div.activity[number=1D]` › `div.row` › `—` | 9 | 9 | 0.04 | 1.00 |
| 743 | activity | MISSING | `div.col-md-4.col-12.paddingLR` › `WIDGET` › `—` | 9 | 9 | 0.01 | structure-only |
| 744 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 9 | 9 | 0.01 | 0.88 |
| 745 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 9 | 9 | 0.01 | 1.00 |
| 746 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=4A]` › `h3` | 9 | 9 | 0.04 | structure-only |
| 747 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=1E]` › `div.activity[number=1E]` | 9 | 9 | 0.01 | structure-only |
| 748 | activity | SUBSTITUTED | `div.col-12` › `div.row` › `audio.audioPlayer.icon` | 9 | 9 | 0.22 | structure-only |
| 749 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=2D]` › `div.activity[number=2D]` | 9 | 9 | 0.02 | structure-only |
| 750 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `p` | 9 | 9 | 0.14 | structure-only |
| 751 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=2B]` › `div.activity[number=2B]` | 9 | 9 | 0.04 | structure-only |
| 752 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=4A]` › `div.activity[number=4A]` | 9 | 9 | 0.03 | structure-only |
| 753 | activity | MISSING | `a` › `div.button.externalButton` › `—` | 23 | 8 | 0.01 | 0.81 |
| 754 | activity | SUBSTITUTED | `a` › `div.buttonD` › `div.button` | 22 | 8 | 0.09 | structure-only |
| 755 | activity | MISSING | `div.col-12` › `hr` › `—` | 16 | 8 | 0.01 | structure-only |
| 756 | activity | SUBSTITUTED | `div.col-12` › `br` › `h4.goJournal` | 12 | 8 | 0.06 | structure-only |
| 757 | activity | SUBSTITUTED | `a` › `div.button.downloadButton` › `div.button` | 11 | 8 | 0.03 | structure-only |
| 758 | activity | MISSING | `div.videoSection.icon.ratio.ra` › `iframe` › `—` | 10 | 8 | 0.03 | structure-only |
| 759 | activity | MISSING | `div.col-md-12.col-12` › `div.row` › `—` | 10 | 8 | 0.01 | 1.00 |
| 760 | activity | SUBSTITUTED | `div.col-12` › `h3` › `ul` | 10 | 8 | 0.76 | structure-only |
| 761 | activity | SUBSTITUTED | `div.col-12` › `p` › `ol` | 10 | 8 | 0.76 | structure-only |
| 762 | activity | EXTRA | `div.TKmodal` › `—` › `ul` | 9 | 8 | 1.00 | structure-only |
| 763 | activity | EXTRA | `a` › `—` › `div.buttonD` | 9 | 8 | 0.96 | structure-only |
| 764 | activity | MISSING | `li` › `br` › `—` | 9 | 8 | 0.01 | structure-only |
| 765 | activity | MISSING | `div.row` › `div.col-md-4.col-12.paddingLR` › `—` | 9 | 8 | 0.00 | structure-only |
| 766 | activity | MISSING | `div.col-12` › `div.button.TKmodalButton` › `—` | 9 | 8 | 0.00 | 0.94 |
| 767 | activity | SUBSTITUTED | `div.col-12` › `div.col-12` › `WIDGET` | 9 | 8 | 0.02 | structure-only |
| 768 | activity | SUBSTITUTED | `div.col-12` › `p` › `a` | 9 | 8 | 0.76 | structure-only |
| 769 | activity | SUBSTITUTED | `div.col-12` › `WIDGET` › `div.videoSection.ratio.ratio-16x9` | 9 | 8 | 0.60 | structure-only |
| 770 | activity | SUBSTITUTED | `div.col-12` › `ul` › `ol` | 9 | 8 | 0.17 | structure-only |
| 771 | activity | SUBSTITUTED | `div.col-12` › `h4.goJournal` › `a` | 9 | 8 | 0.12 | structure-only |
| 772 | activity | SUBSTITUTED | `div.col-12` › `a` › `p>a` | 9 | 8 | 0.57 | structure-only |
| 773 | activity | EXTRA | `div.col-12` › `—` › `img.img-fluid.TKmodalButton` | 8 | 8 | 1.00 | structure-only |
| 774 | activity | EXTRA | `div.activity.interactive[numbe` › `—` › `div.row` | 8 | 8 | 0.99 | structure-only |
| 775 | activity | EXTRA | `div.activity.interactive[numbe` › `—` › `div.row` | 8 | 8 | 0.95 | structure-only |
| 776 | activity | MISSING | `div.activity[number=2A]` › `div.row` › `—` | 8 | 8 | 0.05 | 0.89 |
| 777 | activity | MISSING | `div.activity[number=2E]` › `div.row` › `—` | 8 | 8 | 0.04 | 1.00 |
| 778 | activity | MISSING | `div.col-4` › `WIDGET` › `—` | 8 | 8 | 0.00 | structure-only |
| 779 | activity | MISSING | `div.row` › `div.col-md-6.col-12` › `—` | 8 | 8 | 0.01 | 0.90 |
| 780 | activity | MISSING | `div.clickDropContent` › `ul` › `—` | 8 | 8 | 0.01 | 0.90 |
| 781 | activity | MISSING | `div.activity[number=4B]` › `div.row` › `—` | 8 | 8 | 0.04 | 0.89 |
| 782 | activity | MISSING | `div.activity[number=4A]` › `div.row` › `—` | 8 | 8 | 0.04 | 0.89 |
| 783 | activity | MOVED | `div.col-12` › `a` › `a` | 8 | 8 | 0.04 | structure-only |
| 784 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=3A]` › `div.activity` | 8 | 8 | 0.04 | structure-only |
| 785 | activity | SUBSTITUTED | `div.col-12` › `h3` › `img.img-fluid` | 8 | 8 | 0.76 | structure-only |
| 786 | activity | SUBSTITUTED | `div.col-12` › `a` › `a` | 8 | 8 | 0.57 | structure-only |
| 787 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=4B]` › `div.activity[number=4B]` | 8 | 8 | 0.02 | structure-only |
| 788 | activity | SUBSTITUTED | `div.col-12` › `WIDGET` › `div.button` | 8 | 8 | 0.60 | structure-only |
| 789 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=2D]` › `div.activity.interactive[number=2D]` | 8 | 8 | 0.03 | structure-only |
| 790 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=5A]` › `div.activity[number=5A]` | 8 | 8 | 0.03 | structure-only |
| 791 | activity | SUBSTITUTED | `div.col-12` › `h4` › `p>b` | 8 | 8 | 0.07 | structure-only |
| 792 | activity | EXTRA | `div.col-12` › `—` › `p>span.infoTrigger` | 11 | 7 | 1.00 | structure-only |
| 793 | activity | MISSING | `div.col-md-12.col-12` › `div.clickDropContent` › `—` | 10 | 7 | 0.01 | 0.85 |
| 794 | activity | EXTRA | `div.ratio.ratio-16x9` › `—` › `iframe` | 9 | 7 | 1.00 | structure-only |
| 795 | activity | MISSING | `div.col-12` › `div.alert` › `—` | 9 | 7 | 0.02 | 0.89 |
| 796 | activity | MISSING | `div.col-md-4.col-12` › `WIDGET` › `—` | 8 | 7 | 0.00 | structure-only |
| 797 | activity | MOVED | `ol` › `li>b` › `li>b` | 8 | 7 | 0.01 | structure-only |
| 798 | activity | EXTRA | `div.activity.interactive[numbe` › `—` › `div.row` | 7 | 7 | 0.99 | structure-only |
| 799 | activity | EXTRA | `li>b` › `—` › `b` | 7 | 7 | 0.96 | structure-only |
| 800 | activity | EXTRA | `div.col-md-8.col-12` › `—` › `div.activity[number=1B]` | 7 | 7 | 0.95 | structure-only |
| 801 | activity | EXTRA | `div.TKmodal` › `—` › `p` | 7 | 7 | 1.00 | structure-only |
| 802 | activity | EXTRA | `div.activity[number=1B]` › `—` › `div.row` | 7 | 7 | 0.95 | structure-only |
| 803 | activity | EXTRA | `div.col-12` › `—` › `div.row` | 7 | 7 | 0.78 | structure-only |
| 804 | activity | EXTRA | `div.activity[number=1A]` › `—` › `div.row` | 7 | 7 | 0.95 | structure-only |
| 805 | activity | EXTRA | `h3>a` › `—` › `a` | 7 | 7 | 1.00 | structure-only |
| 806 | activity | MISSING | `div.activity[number=6B]` › `div.row` › `—` | 7 | 7 | 0.00 | 0.90 |
| 807 | activity | MISSING | `div.activity[number=1C]` › `div.row` › `—` | 7 | 7 | 0.04 | 1.00 |
| 808 | activity | MISSING | `div.super-content.row` › `div.row` › `—` | 7 | 7 | 0.02 | 1.00 |
| 809 | activity | MISSING | `div.table-responsive` › `table.table` › `—` | 7 | 7 | 0.02 | 1.00 |
| 810 | activity | MISSING | `div.row` › `div.col-md-4.offset-md-0.col-12.padd` › `—` | 7 | 7 | 0.01 | 1.00 |
| 811 | activity | MOVED | `div.col-md-12.col-12` › `h3` › `h3` | 7 | 7 | 0.01 | structure-only |
| 812 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=1A]` › `h3` | 7 | 7 | 0.05 | structure-only |
| 813 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=2D]` › `div.activity[number=2D]` | 7 | 7 | 0.01 | structure-only |
| 814 | activity | SUBSTITUTED | `div.col-12` › `WIDGET` › `div.col-md-4.offset-md-0.col-12` | 7 | 7 | 0.60 | structure-only |
| 815 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=1B]` › `div.activity[number=1B]` | 7 | 7 | 0.04 | structure-only |
| 816 | activity | SUBSTITUTED | `div.col-12` › `div.col-12` › `div.col-12` | 7 | 7 | 0.02 | structure-only |
| 817 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=2B]` › `div.activity[number=2B]` | 7 | 7 | 0.01 | structure-only |
| 818 | activity | SUBSTITUTED | `div.col-md-12.col-12` › `div.activity.interactive[number=1A]` › `div.activity[number=1A]` | 7 | 7 | 0.01 | structure-only |
| 819 | activity | SUBSTITUTED | `div.row` › `div.col-md-4.col-12` › `WIDGET` | 7 | 7 | 0.02 | structure-only |
| 820 | activity | SUBSTITUTED | `div.col-12` › `WIDGET` › `th` | 7 | 7 | 0.60 | structure-only |
| 821 | activity | EXTRA | `div.col-12` › `—` › `div.button.TKmodalButton` | 8 | 6 | 1.00 | structure-only |
| 822 | activity | EXTRA | `li` › `—` › `b` | 8 | 6 | 0.99 | structure-only |
| 823 | activity | MISSING | `div.clickDropContent` › `ol` › `—` | 8 | 6 | 0.01 | 1.00 |
| 824 | activity | SUBSTITUTED | `div.row` › `div.col-12` › `div.videoSection.ratio.ratio-16x9` | 8 | 6 | 0.79 | structure-only |
| 825 | activity | EXTRA | `p>span.infoTrigger` › `—` › `span.infoTrigger` | 7 | 6 | 0.96 | structure-only |
| 826 | activity | MISSING | `div.col-12` › `div.col-md-8.col-12` › `—` | 7 | 6 | 0.01 | 0.88 |
| 827 | activity | MISSING | `div.col-8` › `p` › `—` | 7 | 6 | 0.01 | 1.00 |
| 828 | activity | MISSING | `div.clickDropContent` › `img.img-fluid` › `—` | 7 | 6 | 0.02 | structure-only |
| 829 | activity | MOVED | `div.col-12` › `p>i` › `p>i` | 7 | 6 | 0.10 | structure-only |
| 830 | activity | MOVED | `div.col-md-12.col-12` › `p` › `p` | 7 | 6 | 0.03 | structure-only |
| 831 | activity | SUBSTITUTED | `div.col-12` › `div.videoSection.icon.ratio.ratio-16` › `p>a` | 7 | 6 | 0.09 | structure-only |
| 832 | activity | SUBSTITUTED | `div.col-12` › `p` › `p>i` | 7 | 6 | 0.76 | structure-only |
| 833 | activity | SUBSTITUTED | `div.col-12` › `p` › `th` | 7 | 6 | 0.76 | structure-only |
| 834 | activity | EXTRA | `div.activity[number=4A]` › `—` › `div.row` | 6 | 6 | 0.96 | structure-only |
| 835 | activity | EXTRA | `div.activity.super-content-but` › `—` › `div.super-content.row` | 6 | 6 | 0.99 | structure-only |
| 836 | activity | MISSING | `div.activity.interactive[numbe` › `WIDGET` › `—` | 6 | 6 | 0.01 | structure-only |
| 837 | activity | MISSING | `div.activity.dropbox[number=3C` › `div.row` › `—` | 6 | 6 | 0.01 | 0.83 |
| 838 | activity | MISSING | `p` › `a` › `—` | 6 | 6 | 0.00 | 0.92 |
| 839 | activity | MISSING | `p>a` › `a` › `—` | 6 | 6 | 0.02 | 1.00 |
| 840 | activity | MISSING | `div.row` › `div.col-md-4.col-xs-6` › `—` | 6 | 6 | 0.00 | structure-only |
| 841 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 6 | 6 | 0.01 | 1.00 |
| 842 | activity | MISSING | `span.audioTrigger` › `img.img-fluid` › `—` | 6 | 6 | 0.00 | structure-only |
| 843 | activity | MISSING | `div.clickDropContent` › `div.row` › `—` | 6 | 6 | 0.01 | 1.00 |
| 844 | activity | MISSING | `div.col-md-12.col-12` › `img.img-fluid` › `—` | 6 | 6 | 0.01 | structure-only |
| 845 | activity | MISSING | `tr` › `td` › `—` | 6 | 6 | 0.01 | 1.00 |
| 846 | activity | MISSING | `div.row` › `div.col-md-4.offset-md-0.col-12` › `—` | 6 | 6 | 0.01 | 1.00 |
| 847 | activity | MISSING | `b>i` › `i` › `—` | 6 | 6 | 0.01 | 1.00 |
| 848 | activity | MISSING | `div.activity[number=2C]` › `div.row` › `—` | 6 | 6 | 0.04 | 0.67 |
| 849 | activity | MOVED | `div.col-12` › `p>b` › `p>b` | 6 | 6 | 0.01 | structure-only |
| 850 | activity | MOVED | `div.activity.dropbox[number=1A` › `p` › `p` | 6 | 6 | 0.00 | structure-only |
| 851 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 6 | 6 | 0.00 | structure-only |
| 852 | activity | SUBSTITUTED | `div.row` › `div.col-12` › `tr` | 6 | 6 | 0.79 | structure-only |
| 853 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=3B]` › `div.activity` | 6 | 6 | 0.04 | structure-only |
| 854 | activity | SUBSTITUTED | `div.col-12` › `h4` › `p` | 6 | 6 | 0.07 | structure-only |
| 855 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=1A]` › `div.activity[number=1A]` | 6 | 6 | 0.01 | structure-only |
| 856 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=1A]` › `div.activity.interactive[number=1A]` | 6 | 6 | 0.05 | structure-only |
| 857 | activity | SUBSTITUTED | `div.col-12` › `WIDGET` › `audio.audioPlayer.icon` | 6 | 6 | 0.60 | structure-only |
| 858 | activity | SUBSTITUTED | `div.col-12` › `WIDGET` › `p>a` | 6 | 6 | 0.60 | structure-only |
| 859 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=1D]` › `div.activity[number=1D]` | 6 | 6 | 0.02 | structure-only |
| 860 | activity | SUBSTITUTED | `div.col-12` › `div.clickDropContent` › `div.col-md-8.col-12` | 6 | 6 | 0.10 | structure-only |
| 861 | activity | SUBSTITUTED | `div.col-12` › `WIDGET` › `div.videoSection.icon.ratio.ratio-16` | 6 | 6 | 0.60 | structure-only |
| 862 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=3A]` › `h4` | 6 | 6 | 0.04 | structure-only |
| 863 | activity | SUBSTITUTED | `div.col-12` › `WIDGET` › `h4.goJournal` | 6 | 6 | 0.60 | structure-only |
| 864 | activity | SUBSTITUTED | `a` › `div.button.buttonD.iconCentral` › `div.button` | 21 | 5 | 0.01 | structure-only |
| 865 | activity | MISSING | `a` › `div.button.iconCentral` › `—` | 13 | 5 | 0.01 | 0.50 |
| 866 | activity | EXTRA | `tr` › `—` › `td` | 6 | 5 | 0.99 | structure-only |
| 867 | activity | MISSING | `div.clickDropContent` › `h4` › `—` | 6 | 5 | 0.01 | 1.00 |
| 868 | activity | MISSING | `div.slideContainer` › `input.slide` › `—` | 6 | 5 | 0.01 | structure-only |
| 869 | activity | SUBSTITUTED | `div.col-12` › `h3` › `div` | 6 | 5 | 0.76 | structure-only |
| 870 | activity | SUBSTITUTED | `div.col-12` › `a` › `img.img-fluid` | 6 | 5 | 0.57 | structure-only |
| 871 | activity | SUBSTITUTED | `div.col-12` › `p` › `ul` | 6 | 5 | 0.76 | structure-only |
| 872 | activity | SUBSTITUTED | `div.clickDropContent` › `ul` › `ul` | 6 | 5 | 0.02 | structure-only |
| 873 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.col-12` | 6 | 5 | 0.12 | structure-only |
| 874 | activity | SUBSTITUTED | `div.col-12` › `p` › `img.img-fluid` | 6 | 5 | 0.76 | structure-only |
| 875 | activity | SUBSTITUTED | `div.col-12` › `WIDGET` › `div.table-responsive` | 6 | 5 | 0.60 | structure-only |
| 876 | activity | SUBSTITUTED | `a` › `div.button.buttonD` › `div.buttonD` | 6 | 5 | 0.01 | structure-only |
| 877 | activity | SUBSTITUTED | `div.col-12` › `WIDGET` › `h3` | 6 | 5 | 0.60 | structure-only |
| 878 | activity | SUBSTITUTED | `div.col-12` › `WIDGET` › `div.ratio.ratio-16x9` | 6 | 5 | 0.60 | structure-only |
| 879 | activity | EXTRA | `li>i` › `—` › `i` | 5 | 5 | 0.99 | structure-only |
| 880 | activity | EXTRA | `div.activity.interactive[numbe` › `—` › `div.row` | 5 | 5 | 0.99 | structure-only |
| 881 | activity | EXTRA | `div.activity[number=1D]` › `—` › `div.row` | 5 | 5 | 0.96 | structure-only |
| 882 | activity | EXTRA | `div.activity[number=2A]` › `—` › `div.row` | 5 | 5 | 0.95 | structure-only |
| 883 | activity | EXTRA | `div.activity.interactive[numbe` › `—` › `div.row` | 5 | 5 | 0.99 | structure-only |
| 884 | activity | EXTRA | `div.activity.interactive[numbe` › `—` › `div.row` | 5 | 5 | 0.99 | structure-only |
| 885 | activity | EXTRA | `div.activity[number=4B]` › `—` › `div.row` | 5 | 5 | 0.96 | structure-only |
| 886 | activity | EXTRA | `div.activity[number=5B]` › `—` › `div.row` | 5 | 5 | 0.97 | structure-only |
| 887 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 5 | 5 | 0.00 | 0.83 |
| 888 | activity | MISSING | `ul` › `li>b` › `—` | 5 | 5 | 0.02 | 0.69 |
| 889 | activity | MISSING | `div.table-responsive` › `table.table.table-bordered.tableFixe` › `—` | 5 | 5 | 0.01 | 1.00 |
| 890 | activity | MISSING | `div.activity[number=3A]` › `div.row` › `—` | 5 | 5 | 0.03 | 0.60 |
| 891 | activity | MISSING | `div.activity[number=3B]` › `div.row` › `—` | 5 | 5 | 0.04 | 0.80 |
| 892 | activity | MISSING | `div.activity[number=4F]` › `div.row` › `—` | 5 | 5 | 0.00 | 1.00 |
| 893 | activity | MISSING | `p>span.sassoonI-text` › `span.sassoonI-text` › `—` | 5 | 5 | 0.00 | 1.00 |
| 894 | activity | MISSING | `div.row` › `div.clickDropContent` › `—` | 5 | 5 | 0.01 | 0.80 |
| 895 | activity | MISSING | `div.row` › `div.col-md-6.offset-md-0.col-12` › `—` | 5 | 5 | 0.01 | 1.00 |
| 896 | activity | MISSING | `div.activity[number=1B]` › `div.row` › `—` | 5 | 5 | 0.05 | 1.00 |
| 897 | activity | MISSING | `div.row` › `div.col-md-6.col-12.paddingL` › `—` | 5 | 5 | 0.01 | 1.00 |
| 898 | activity | MISSING | `div.col-md-8.col-12` › `div.activity[number=3A]` › `—` | 5 | 5 | 0.03 | 1.00 |
| 899 | activity | MISSING | `div.row` › `div.col-md-3.col-12` › `—` | 5 | 5 | 0.01 | 0.77 |
| 900 | activity | MISSING | `div.TKmodal` › `h4` › `—` | 5 | 5 | 0.00 | 0.80 |
| 901 | activity | MISSING | `div.activity[number=5C]` › `div.row` › `—` | 5 | 5 | 0.02 | 1.00 |
| 902 | activity | MISSING | `ol` › `br` › `—` | 5 | 5 | 0.00 | structure-only |
| 903 | activity | MISSING | `div.col-md-8.col-12` › `ol` › `—` | 5 | 5 | 0.00 | 0.71 |
| 904 | activity | MISSING | `div.slider` › `div.slideContainer` › `—` | 5 | 5 | 0.01 | 0.70 |
| 905 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 5 | 5 | 0.01 | 1.00 |
| 906 | activity | MOVED | `div.row` › `p` › `p` | 5 | 5 | 0.02 | structure-only |
| 907 | activity | MOVED | `div.activity.alertPadding.inte` › `h3` › `h3` | 5 | 5 | 0.00 | structure-only |
| 908 | activity | MOVED | `div.alert` › `p` › `p` | 5 | 5 | 0.00 | structure-only |
| 909 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 5 | 5 | 0.00 | structure-only |
| 910 | activity | MOVED | `div.activity.dropbox[number=2A` › `p` › `p` | 5 | 5 | 0.00 | structure-only |
| 911 | activity | MOVED | `div.activity.dropbox[number=3A` › `p` › `p` | 5 | 5 | 0.00 | structure-only |
| 912 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 5 | 5 | 0.00 | structure-only |
| 913 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=2A]` › `h3` | 5 | 5 | 0.06 | structure-only |
| 914 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=1B]` › `div.activity` | 5 | 5 | 0.04 | structure-only |
| 915 | activity | SUBSTITUTED | `div.col-12` › `div.hint` › `p` | 5 | 5 | 0.07 | structure-only |
| 916 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=5A]` › `h3` | 5 | 5 | 0.03 | structure-only |
| 917 | activity | SUBSTITUTED | `div.col-12` › `img.img-fluid` › `WIDGET` | 5 | 5 | 0.12 | structure-only |
| 918 | activity | SUBSTITUTED | `a` › `div.button` › `div.button.downloadButton` | 5 | 5 | 0.48 | structure-only |
| 919 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=4A]` › `div.activity[number=4A]` | 5 | 5 | 0.01 | structure-only |
| 920 | activity | SUBSTITUTED | `a` › `div.button` › `div.button.externalButton` | 5 | 5 | 0.48 | structure-only |
| 921 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=1A]` › `h4` | 5 | 5 | 0.05 | structure-only |
| 922 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=4B]` › `h4` | 5 | 5 | 0.04 | structure-only |
| 923 | activity | SUBSTITUTED | `div.col-12` › `div.row` › `img.img-fluid.TKmodalButton` | 5 | 5 | 0.22 | structure-only |
| 924 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=1C]` › `div.activity[number=1C]` | 5 | 5 | 0.04 | structure-only |
| 925 | activity | SUBSTITUTED | `div.col-12` › `div.table-responsive` › `div.row` | 5 | 5 | 0.08 | structure-only |
| 926 | activity | SUBSTITUTED | `div.row.flipCardsContainer` › `div.col-md-4.col-12.paddingLR` › `WIDGET` | 5 | 5 | 0.02 | structure-only |
| 927 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=1A]` › `div.activity.super-content-button[nu` | 5 | 5 | 0.05 | structure-only |
| 928 | activity | SUBSTITUTED | `div.col-12` › `WIDGET` › `div.col-12` | 5 | 5 | 0.60 | structure-only |
| 929 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=2C]` › `div.activity.interactive[number=2C]` | 5 | 5 | 0.04 | structure-only |
| 930 | activity | SUBSTITUTED | `a` › `div.buttonD` › `div.col-md-8.col-12` | 5 | 5 | 0.09 | structure-only |
| 931 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=2E]` › `div.activity.interactive[number=2E]` | 5 | 5 | 0.04 | structure-only |
| 932 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=3B]` › `div.activity[number=3B]` | 5 | 5 | 0.03 | structure-only |
| 933 | activity | SUBSTITUTED | `div.col-md-4.col-12` › `img.img-fluid` › `img.img-fluid` | 5 | 5 | 0.01 | structure-only |
| 934 | activity | SUBSTITUTED | `div.row` › `div.col-md-4.col-12` › `img.img-fluid` | 5 | 5 | 0.02 | structure-only |
| 935 | activity | SUBSTITUTED | `div.row.flipCardsContainer` › `div.col-md-6.col-12.paddingLR` › `div.col-md-4.col-12.paddingLR` | 5 | 5 | 0.01 | structure-only |
| 936 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=4A]` › `div.activity.interactive[number=4A]` | 5 | 5 | 0.04 | structure-only |
| 937 | activity | SUBSTITUTED | `div.clickDropContent` › `p` › `div.clickDropContent` | 5 | 5 | 0.07 | structure-only |
| 938 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `WIDGET` | 5 | 5 | 0.14 | structure-only |
| 939 | activity | SUBSTITUTED | `div.col-12` › `div.clickDropContent` › `div.clickDropContent` | 5 | 5 | 0.10 | structure-only |
| 940 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=2B]` › `div.activity.interactive[number=2B]` | 5 | 5 | 0.05 | structure-only |
| 941 | activity | SUBSTITUTED | `div.col-md-12.col-12` › `p` › `p` | 5 | 5 | 0.05 | structure-only |
| 942 | activity | SUBSTITUTED | `div.col-12` › `div.row` › `div.col-md-8.col-12` | 5 | 5 | 0.22 | structure-only |
| 943 | activity | SUBSTITUTED | `div.row` › `div.col-md-12.col-12` › `div.col-md-8.col-12` | 5 | 5 | 0.11 | structure-only |
| 944 | activity | SUBSTITUTED | `p>i` › `i` › `a` | 5 | 5 | 0.12 | structure-only |
| 945 | activity | SUBSTITUTED | `div.col-12` › `div.activity.interactive[number=5A]` › `div.activity[number=5A]` | 5 | 5 | 0.01 | structure-only |
| 946 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=6A]` › `div.activity[number=6A]` | 5 | 5 | 0.02 | structure-only |
| 947 | activity | SUBSTITUTED | `div.col-12` › `div.activity.interactive[number=3A]` › `div.activity[number=3A]` | 5 | 5 | 0.01 | structure-only |
| 948 | activity | SUBSTITUTED | `div.col-12` › `div.clickDropContent` › `h4.goJournal` | 5 | 5 | 0.10 | structure-only |
| 949 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=3A]` › `h3` | 5 | 5 | 0.04 | structure-only |
| 950 | activity | MISSING | `div.col-12` › `div.row.justify-content-center.slide` › `—` | 14 | 4 | 0.01 | 0.14 |
| 951 | activity | SUBSTITUTED | `div.row` › `div.col-md-12` › `div.col-12` | 13 | 4 | 0.02 | structure-only |
| 952 | activity | MISSING | `a` › `div.button.buttonD.iconCentral` › `—` | 10 | 4 | 0.01 | 0.93 |
| 953 | activity | MISSING | `div.clickDropContent` › `h3` › `—` | 8 | 4 | 0.00 | 0.88 |
| 954 | activity | MOVED | `a` › `div.externalButton` › `div.externalButton` | 8 | 4 | 0.01 | structure-only |
| 955 | activity | MISSING | `h3>em` › `em` › `—` | 7 | 4 | 0.01 | 1.00 |
| 956 | activity | SUBSTITUTED | `div.col-12` › `ol` › `ul` | 7 | 4 | 0.13 | structure-only |
| 957 | activity | MISSING | `div.row` › `div.col-md-6.offset-md-0.col-12.padd` › `—` | 6 | 4 | 0.00 | 1.00 |
| 958 | activity | MOVED | `tr.rowSolid` › `th` › `th` | 6 | 4 | 0.00 | structure-only |
| 959 | activity | SUBSTITUTED | `div.row` › `div.col-md-10.col-12` › `div.col-12` | 6 | 4 | 0.01 | structure-only |
| 960 | activity | SUBSTITUTED | `div.col-12` › `a` › `p>b` | 6 | 4 | 0.57 | structure-only |
| 961 | activity | EXTRA | `div.activity.interactive` › `—` › `div.row` | 5 | 4 | 1.00 | structure-only |
| 962 | activity | EXTRA | `div.clickDropContent` › `—` › `ul` | 5 | 4 | 0.98 | structure-only |
| 963 | activity | EXTRA | `ol` › `—` › `li>b` | 5 | 4 | 0.99 | structure-only |
| 964 | activity | MISSING | `a` › `div.button.buttonD` › `—` | 5 | 4 | 0.00 | 1.00 |
| 965 | activity | MISSING | `div.table-responsive` › `table.table.table-bordered.td-hover` › `—` | 5 | 4 | 0.01 | 1.00 |
| 966 | activity | MISSING | `div.row.justify-content-center` › `div.col-11` › `—` | 5 | 4 | 0.01 | structure-only |
| 967 | activity | MISSING | `div.row.justify-content-center` › `div.col-12` › `—` | 5 | 4 | 0.01 | 0.80 |
| 968 | activity | MISSING | `div.col-12` › `div.alert.solid` › `—` | 5 | 4 | 0.01 | 1.00 |
| 969 | activity | MISSING | `div.col-md-8.col-12` › `p>b` › `—` | 5 | 4 | 0.01 | 1.00 |
| 970 | activity | MISSING | `p>span.highlight` › `span.highlight` › `—` | 5 | 4 | 0.00 | 0.83 |
| 971 | activity | MISSING | `div.col-12` › `p.quoteText` › `—` | 5 | 4 | 0.01 | 1.00 |
| 972 | activity | MISSING | `div.col-8` › `h3` › `—` | 5 | 4 | 0.01 | 1.00 |
| 973 | activity | MISSING | `div.slideContainer` › `div.slidePoints` › `—` | 5 | 4 | 0.00 | 0.67 |
| 974 | activity | SUBSTITUTED | `div.col-12` › `p` › `td` | 5 | 4 | 0.76 | structure-only |
| 975 | activity | SUBSTITUTED | `div.row` › `p` › `p` | 5 | 4 | 0.02 | structure-only |
| 976 | activity | SUBSTITUTED | `div.col-12` › `WIDGET` › `h5` | 5 | 4 | 0.60 | structure-only |
| 977 | activity | SUBSTITUTED | `ul` › `li>b` › `li>b` | 5 | 4 | 0.03 | structure-only |
| 978 | activity | SUBSTITUTED | `div.col-12` › `div.col-md-12.col-12` › `WIDGET` | 5 | 4 | 0.01 | structure-only |
| 979 | activity | SUBSTITUTED | `div.col-12` › `p>b` › `p` | 5 | 4 | 0.11 | structure-only |
| 980 | activity | SUBSTITUTED | `a` › `div.button` › `iframe` | 5 | 4 | 0.48 | structure-only |
| 981 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `WIDGET` | 5 | 4 | 0.12 | structure-only |
| 982 | activity | EXTRA | `div.col-md-8.col-12` › `—` › `div.activity.interactive[number=4B]` | 4 | 4 | 0.98 | structure-only |
| 983 | activity | EXTRA | `div.activity.interactive[numbe` › `—` › `div.row` | 4 | 4 | 0.96 | structure-only |
| 984 | activity | EXTRA | `div.activity.interactive[numbe` › `—` › `div.row` | 4 | 4 | 0.99 | structure-only |
| 985 | activity | EXTRA | `div.col-md-8.col-12` › `—` › `div.activity[number=1C]` | 4 | 4 | 0.96 | structure-only |
| 986 | activity | EXTRA | `div.activity[number=3C]` › `—` › `div.row` | 4 | 4 | 0.97 | structure-only |
| 987 | activity | EXTRA | `div.activity.interactive[numbe` › `—` › `div.row` | 4 | 4 | 0.94 | structure-only |
| 988 | activity | EXTRA | `div.col-12` › `—` › `div.row.flipCardsContainer` | 4 | 4 | 0.96 | structure-only |
| 989 | activity | EXTRA | `div.col-12` › `—` › `div.activity.interactive[number=2C]` | 4 | 4 | 0.99 | structure-only |
| 990 | activity | EXTRA | `div.col-12` › `—` › `div.activity.interactive[number=1C]` | 4 | 4 | 1.00 | structure-only |
| 991 | activity | EXTRA | `div.activity.interactive[numbe` › `—` › `div.row` | 4 | 4 | 0.99 | structure-only |
| 992 | activity | EXTRA | `div.activity[number=1C]` › `—` › `div.row` | 4 | 4 | 0.96 | structure-only |
| 993 | activity | EXTRA | `div.col-12` › `—` › `textarea.form-control` | 4 | 4 | 1.00 | structure-only |
| 994 | activity | EXTRA | `div.activity[number=3B]` › `—` › `div.row` | 4 | 4 | 0.96 | structure-only |
| 995 | activity | EXTRA | `div.activity.interactive[numbe` › `—` › `div.row` | 4 | 4 | 1.00 | structure-only |
| 996 | activity | EXTRA | `div.activity[number=5A]` › `—` › `div.row` | 4 | 4 | 0.97 | structure-only |
| 997 | activity | EXTRA | `a` › `—` › `div.button.externalButton` | 4 | 4 | 0.99 | structure-only |
| 998 | activity | MISSING | `div.activity.interactive[numbe` › `WIDGET` › `—` | 4 | 4 | 0.00 | structure-only |
| 999 | activity | MISSING | `div.activity.interactive[numbe` › `WIDGET` › `—` | 4 | 4 | 0.00 | structure-only |
| 1000 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 4 | 4 | 0.00 | 1.00 |
| 1001 | activity | MISSING | `div.activity[number=3F]` › `div.row` › `—` | 4 | 4 | 0.00 | 0.75 |
| 1002 | activity | MISSING | `div.activity[number=2B]` › `div.row` › `—` | 4 | 4 | 0.00 | 1.00 |
| 1003 | activity | MISSING | `div.activity[number=5E]` › `div.row` › `—` | 4 | 4 | 0.00 | 1.00 |
| 1004 | activity | MISSING | `div.activity.alertPadding.inte` › `WIDGET` › `—` | 4 | 4 | 0.00 | structure-only |
| 1005 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 4 | 4 | 0.00 | 0.75 |
| 1006 | activity | MISSING | `div.row` › `div.col-md-6.offset-md-0.col-12.padd` › `—` | 4 | 4 | 0.00 | structure-only |
| 1007 | activity | MISSING | `p` › `span.sassoonI-text` › `—` | 4 | 4 | 0.00 | 1.00 |
| 1008 | activity | MISSING | `div.activity.alertPadding.inte` › `WIDGET` › `—` | 4 | 4 | 0.00 | structure-only |
| 1009 | activity | MISSING | `div.row` › `div.col-md-4.col-12.paddingL` › `—` | 4 | 4 | 0.00 | 1.00 |
| 1010 | activity | MISSING | `div.col-12` › `div.clearDiv` › `—` | 4 | 4 | 0.00 | structure-only |
| 1011 | activity | MISSING | `div.table-responsive.sassoonI-` › `table.table` › `—` | 4 | 4 | 0.00 | 1.00 |
| 1012 | activity | MISSING | `div.alert` › `div.row` › `—` | 4 | 4 | 0.01 | 1.00 |
| 1013 | activity | MISSING | `div.col` › `WIDGET` › `—` | 4 | 4 | 0.00 | structure-only |
| 1014 | activity | MISSING | `div.row` › `div.col-md-6.col-12.paddingR` › `—` | 4 | 4 | 0.01 | 1.00 |
| 1015 | activity | MISSING | `i` › `br` › `—` | 4 | 4 | 0.00 | structure-only |
| 1016 | activity | MISSING | `div.col-md-4.col-12` › `img.img-fluid` › `—` | 4 | 4 | 0.00 | structure-only |
| 1017 | activity | MISSING | `div.row` › `div.col-md-2.col-12` › `—` | 4 | 4 | 0.00 | 0.08 |
| 1018 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 4 | 4 | 0.02 | 1.00 |
| 1019 | activity | MISSING | `div.activity[number=5A]` › `div.row` › `—` | 4 | 4 | 0.03 | 1.00 |
| 1020 | activity | MISSING | `div.col-md-12.col-12` › `h3` › `—` | 4 | 4 | 0.01 | 1.00 |
| 1021 | activity | MISSING | `div.activity[number=3D]` › `div.row` › `—` | 4 | 4 | 0.02 | 1.00 |
| 1022 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 4 | 4 | 0.01 | 1.00 |
| 1023 | activity | MISSING | `p` › `ul` › `—` | 4 | 4 | 0.01 | 0.75 |
| 1024 | activity | MISSING | `div.activity[number=8C]` › `div.row` › `—` | 4 | 4 | 0.01 | 1.00 |
| 1025 | activity | MISSING | `div.col-md-8.col-12` › `h4` › `—` | 4 | 4 | 0.00 | 0.20 |
| 1026 | activity | MISSING | `div.col-md-12.col-12` › `ol` › `—` | 4 | 4 | 0.01 | 1.00 |
| 1027 | activity | MOVED | `tr` › `th` › `th` | 4 | 4 | 0.01 | structure-only |
| 1028 | activity | MOVED | `div.clickDropContent` › `p>b` › `p>b` | 4 | 4 | 0.00 | structure-only |
| 1029 | activity | MOVED | `div.col-md-10.col-12` › `p` › `p` | 4 | 4 | 0.00 | structure-only |
| 1030 | activity | MOVED | `div.activity[number=2B]` › `p` › `p` | 4 | 4 | 0.00 | structure-only |
| 1031 | activity | MOVED | `div.activity.dropbox[number=6A` › `p` › `p` | 4 | 4 | 0.00 | structure-only |
| 1032 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 4 | 4 | 0.00 | structure-only |
| 1033 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 4 | 4 | 0.00 | structure-only |
| 1034 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 4 | 4 | 0.00 | structure-only |
| 1035 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 4 | 4 | 0.00 | structure-only |
| 1036 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 4 | 4 | 0.00 | structure-only |
| 1037 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 4 | 4 | 0.00 | structure-only |
| 1038 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 4 | 4 | 0.00 | structure-only |
| 1039 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 4 | 4 | 0.00 | structure-only |
| 1040 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 4 | 4 | 0.00 | structure-only |
| 1041 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 4 | 4 | 0.00 | structure-only |
| 1042 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 4 | 4 | 0.00 | structure-only |
| 1043 | activity | MOVED | `div.activity.dropbox[number=7A` › `p` › `p` | 4 | 4 | 0.00 | structure-only |
| 1044 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 4 | 4 | 0.00 | structure-only |
| 1045 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 4 | 4 | 0.00 | structure-only |
| 1046 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=3B]` › `h3` | 4 | 4 | 0.04 | structure-only |
| 1047 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=4B]` › `div.activity.interactive[number=4B]` | 4 | 4 | 0.04 | structure-only |
| 1048 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=5A]` › `div.activity` | 4 | 4 | 0.03 | structure-only |
| 1049 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=1B]` › `h3` | 4 | 4 | 0.04 | structure-only |
| 1050 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=2A]` › `div.activity` | 4 | 4 | 0.04 | structure-only |
| 1051 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=2B]` › `div.activity` | 4 | 4 | 0.01 | structure-only |
| 1052 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=4B]` › `div.activity` | 4 | 4 | 0.04 | structure-only |
| 1053 | activity | SUBSTITUTED | `div.col-12` › `h4.goJournal` › `ul` | 4 | 4 | 0.12 | structure-only |
| 1054 | activity | SUBSTITUTED | `div.col-12` › `div.row` › `div.col-12` | 4 | 4 | 0.22 | structure-only |
| 1055 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=5B]` › `div.activity[number=5B]` | 4 | 4 | 0.02 | structure-only |
| 1056 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=2A]` › `div.activity.interactive[number=2A]` | 4 | 4 | 0.04 | structure-only |
| 1057 | activity | SUBSTITUTED | `div.col-12` › `ol` › `p>a` | 4 | 4 | 0.13 | structure-only |
| 1058 | activity | SUBSTITUTED | `div.row` › `div.col-4` › `div.TKmodal` | 4 | 4 | 0.01 | structure-only |
| 1059 | activity | SUBSTITUTED | `div.col-4` › `WIDGET` › `img.img-fluid.TKmodalButton` | 4 | 4 | 0.01 | structure-only |
| 1060 | activity | SUBSTITUTED | `div.col-12` › `div.row` › `div.TKmodal` | 4 | 4 | 0.22 | structure-only |
| 1061 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=2C]` › `div.activity[number=2C]` | 4 | 4 | 0.01 | structure-only |
| 1062 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=1F]` › `div.activity[number=1F]` | 4 | 4 | 0.01 | structure-only |
| 1063 | activity | SUBSTITUTED | `div.row` › `div.col-4` › `WIDGET` | 4 | 4 | 0.01 | structure-only |
| 1064 | activity | SUBSTITUTED | `div.col-12` › `div.row` › `ol` | 4 | 4 | 0.22 | structure-only |
| 1065 | activity | SUBSTITUTED | `div.row` › `div.col-md-8.col-12` › `div.row` | 4 | 4 | 0.14 | structure-only |
| 1066 | activity | SUBSTITUTED | `div.row.flipCardsContainer` › `div.col-md-4.col-12.paddingLR` › `div.row` | 4 | 4 | 0.02 | structure-only |
| 1067 | activity | SUBSTITUTED | `div.row` › `div.col-md-4.offset-md-0.col-12` › `WIDGET` | 4 | 4 | 0.01 | structure-only |
| 1068 | activity | SUBSTITUTED | `div.col-md-12.col-12` › `div.activity.interactive[number=2B]` › `div.activity[number=2B]` | 4 | 4 | 0.01 | structure-only |
| 1069 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=5A]` › `div.activity[number=5A]` | 4 | 4 | 0.01 | structure-only |
| 1070 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=7A]` › `div.activity[number=7A]` | 4 | 4 | 0.00 | structure-only |
| 1071 | activity | SUBSTITUTED | `div.col-12` › `div.row` › `div.col-md-4.offset-md-0.col-12` | 4 | 4 | 0.22 | structure-only |
| 1072 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=3C]` › `div.activity[number=3C]` | 4 | 4 | 0.02 | structure-only |
| 1073 | activity | SUBSTITUTED | `div.col-12` › `div.activity.interactive[number=1A]` › `div.activity[number=1A]` | 4 | 4 | 0.02 | structure-only |
| 1074 | activity | SUBSTITUTED | `div.col-12` › `h3` › `div.col-12` | 4 | 4 | 0.76 | structure-only |
| 1075 | activity | SUBSTITUTED | `div.col-md-4.col-12` › `WIDGET` › `p` | 4 | 4 | 0.01 | structure-only |
| 1076 | activity | SUBSTITUTED | `div.row` › `div.col-md-12.col-12` › `div.row` | 4 | 4 | 0.11 | structure-only |
| 1077 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=1B]` › `h4` | 4 | 4 | 0.04 | structure-only |
| 1078 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=1C]` › `h4` | 4 | 4 | 0.04 | structure-only |
| 1079 | activity | SUBSTITUTED | `div.col-12` › `div.videoSection.ratio.ratio-16x9` › `div.row` | 4 | 4 | 0.05 | structure-only |
| 1080 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=2C]` › `h3` | 4 | 4 | 0.04 | structure-only |
| 1081 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=4A]` › `h4` | 4 | 4 | 0.03 | structure-only |
| 1082 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=5A]` › `h4` | 4 | 4 | 0.03 | structure-only |
| 1083 | activity | SUBSTITUTED | `div.col-12` › `h3` › `th` | 4 | 4 | 0.76 | structure-only |
| 1084 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=2A]` › `h4` | 4 | 4 | 0.04 | structure-only |
| 1085 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=2A]` › `div.activity` | 4 | 4 | 0.06 | structure-only |
| 1086 | activity | SUBSTITUTED | `div.col-12` › `div.videoSection.icon.ratio.ratio-16` › `img.img-fluid` | 4 | 4 | 0.09 | structure-only |
| 1087 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=4C]` › `h3` | 4 | 4 | 0.03 | structure-only |
| 1088 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=1A]` › `div.activity` | 4 | 4 | 0.05 | structure-only |
| 1089 | activity | SUBSTITUTED | `div.col-12` › `div.hint` › `div.row` | 4 | 4 | 0.07 | structure-only |
| 1090 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=5A]` › `div.activity` | 4 | 4 | 0.03 | structure-only |
| 1091 | activity | SUBSTITUTED | `div.col-12` › `div.row` › `div.button` | 4 | 4 | 0.22 | structure-only |
| 1092 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=2B]` › `div.activity.interactive[number=2A]` | 4 | 4 | 0.04 | structure-only |
| 1093 | activity | SUBSTITUTED | `div.clickDropContent.activity.` › `h3` › `div.row` | 4 | 4 | 0.00 | structure-only |
| 1094 | activity | SUBSTITUTED | `a` › `div.externalButton` › `div.externalButton` | 7 | 3 | 0.10 | structure-only |
| 1095 | activity | EXTRA | `div.col-12` › `—` › `h2` | 5 | 3 | 1.00 | structure-only |
| 1096 | activity | SUBSTITUTED | `div.col-12` › `ul` › `p>b` | 5 | 3 | 0.17 | structure-only |
| 1097 | activity | SUBSTITUTED | `div.col-12` › `div.clickDropContent` › `p` | 5 | 3 | 0.10 | structure-only |
| 1098 | activity | SUBSTITUTED | `div.row` › `div.col-md-12.col-12` › `div.TKmodal` | 5 | 3 | 0.11 | structure-only |
| 1099 | activity | MISSING | `div.col-12` › `h4.center-text` › `—` | 4 | 3 | 0.01 | 1.00 |
| 1100 | activity | MISSING | `li` › `ul` › `—` | 4 | 3 | 0.00 | 0.67 |
| 1101 | activity | MOVED | `ul` › `li>b` › `li>b` | 4 | 3 | 0.01 | structure-only |
| 1102 | activity | MOVED | `ul` › `li>b` › `li>b` | 4 | 3 | 0.01 | structure-only |
| 1103 | activity | SUBSTITUTED | `div.col-12` › `a` › `div.videoSection.icon.ratio.ratio-16` | 4 | 3 | 0.57 | structure-only |
| 1104 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `p>i` | 4 | 3 | 0.14 | structure-only |
| 1105 | activity | SUBSTITUTED | `div.col-md-12.col-12` › `h3` › `div.col-12` | 4 | 3 | 0.03 | structure-only |
| 1106 | activity | SUBSTITUTED | `div.col-12` › `h5` › `p>b` | 4 | 3 | 0.04 | structure-only |
| 1107 | activity | SUBSTITUTED | `div.col-12` › `h3` › `a` | 4 | 3 | 0.76 | structure-only |
| 1108 | activity | SUBSTITUTED | `div.col-12` › `div.table-responsive` › `p` | 4 | 3 | 0.08 | structure-only |
| 1109 | activity | SUBSTITUTED | `div.col-12` › `h4.goJournal` › `td` | 4 | 3 | 0.12 | structure-only |
| 1110 | activity | SUBSTITUTED | `a` › `div.button.iconCentral` › `div.button` | 4 | 3 | 0.01 | structure-only |
| 1111 | activity | EXTRA | `div.activity[number=2C]` › `—` › `div.row` | 3 | 3 | 0.96 | structure-only |
| 1112 | activity | EXTRA | `div.col-md-8.col-12` › `—` › `div.activity[number=3A]` | 3 | 3 | 0.97 | structure-only |
| 1113 | activity | EXTRA | `div.col-md-8.col-12` › `—` › `div.activity[number=2C]` | 3 | 3 | 0.96 | structure-only |
| 1114 | activity | EXTRA | `div.TKmodal` › `—` › `p>a` | 3 | 3 | 1.00 | structure-only |
| 1115 | activity | EXTRA | `div.activity.super-content-but` › `—` › `div.row` | 3 | 3 | 0.99 | structure-only |
| 1116 | activity | EXTRA | `div.activity.super-content-but` › `—` › `div.row` | 3 | 3 | 1.00 | structure-only |
| 1117 | activity | EXTRA | `div.col-12` › `—` › `div.activity.interactive[number=1D]` | 3 | 3 | 1.00 | structure-only |
| 1118 | activity | EXTRA | `div.activity.super-content-but` › `—` › `div.row` | 3 | 3 | 0.99 | structure-only |
| 1119 | activity | EXTRA | `div.col-12` › `—` › `div.activity.interactive[number=1B]` | 3 | 3 | 0.99 | structure-only |
| 1120 | activity | EXTRA | `div.col-md-8.col-12` › `—` › `div.activity[number=2A]` | 3 | 3 | 0.96 | structure-only |
| 1121 | activity | EXTRA | `div.activity[number=2E]` › `—` › `div.row` | 3 | 3 | 0.96 | structure-only |
| 1122 | activity | EXTRA | `div.clickDropContent` › `—` › `p>a` | 3 | 3 | 1.00 | structure-only |
| 1123 | activity | EXTRA | `div.clickDropContent` › `—` › `img.img-fluid` | 3 | 3 | 1.00 | structure-only |
| 1124 | activity | EXTRA | `div.activity.interactive[numbe` › `—` › `div.row` | 3 | 3 | 0.98 | structure-only |
| 1125 | activity | EXTRA | `h3>span.infoTrigger` › `—` › `span.infoTrigger` | 3 | 3 | 1.00 | structure-only |
| 1126 | activity | EXTRA | `div.col-md-8.col-12` › `—` › `p` | 3 | 3 | 0.99 | structure-only |
| 1127 | activity | EXTRA | `div.activity[number=2B]` › `—` › `div.row` | 3 | 3 | 0.95 | structure-only |
| 1128 | activity | EXTRA | `div.activity.interactive[numbe` › `—` › `div.row` | 3 | 3 | 0.99 | structure-only |
| 1129 | activity | MISSING | `div.activity.interactive[numbe` › `WIDGET` › `—` | 3 | 3 | 0.00 | structure-only |
| 1130 | activity | MISSING | `p` › `span` › `—` | 3 | 3 | 0.00 | 1.00 |
| 1131 | activity | MISSING | `li>b` › `b` › `—` | 3 | 3 | 0.02 | 1.00 |
| 1132 | activity | MISSING | `div.col-md-8.col-12` › `div.activity[number=4A]` › `—` | 3 | 3 | 0.04 | 1.00 |
| 1133 | activity | MISSING | `div.activity.alertPadding[numb` › `div.row` › `—` | 3 | 3 | 0.01 | 1.00 |
| 1134 | activity | MISSING | `div.activity` › `div.row` › `—` | 3 | 3 | 0.00 | 0.67 |
| 1135 | activity | MISSING | `div.activity.alertPadding[numb` › `div.row` › `—` | 3 | 3 | 0.01 | 1.00 |
| 1136 | activity | MISSING | `div.col-md-4.col-xs-6` › `img.img-fluid` › `—` | 3 | 3 | 0.00 | structure-only |
| 1137 | activity | MISSING | `div.activity[number=2F]` › `div.row` › `—` | 3 | 3 | 0.01 | 0.67 |
| 1138 | activity | MISSING | `div.col-12` › `p>a` › `—` | 3 | 3 | 0.00 | 0.71 |
| 1139 | activity | MISSING | `div.activity[number=2H]` › `div.row` › `—` | 3 | 3 | 0.00 | 0.67 |
| 1140 | activity | MISSING | `div.row` › `div.col-md-4.col-xs-6.paddingR` › `—` | 3 | 3 | 0.00 | structure-only |
| 1141 | activity | MISSING | `div.activity[number=3E]` › `div.row` › `—` | 3 | 3 | 0.00 | 1.00 |
| 1142 | activity | MISSING | `div.activity[number=4E]` › `div.row` › `—` | 3 | 3 | 0.00 | 0.67 |
| 1143 | activity | MISSING | `div.activity[number=5F]` › `div.row` › `—` | 3 | 3 | 0.00 | 1.00 |
| 1144 | activity | MISSING | `div.row` › `div.col-md-8.col-12.offset-2` › `—` | 3 | 3 | 0.00 | structure-only |
| 1145 | activity | MISSING | `div.activity.alertPadding.inte` › `WIDGET` › `—` | 3 | 3 | 0.00 | structure-only |
| 1146 | activity | MISSING | `div.col-4` › `div.audioButton` › `—` | 3 | 3 | 0.00 | structure-only |
| 1147 | activity | MISSING | `div.row` › `div.col-8` › `—` | 3 | 3 | 0.00 | 1.00 |
| 1148 | activity | MISSING | `div.activity.super-content-but` › `div.super-content.row` › `—` | 3 | 3 | 0.01 | 0.67 |
| 1149 | activity | MISSING | `div.col-12` › `div.col-md-8.col-12.offset-md-2` › `—` | 3 | 3 | 0.00 | structure-only |
| 1150 | activity | MISSING | `div.col-md-8.col-12` › `div.activity[number=2B]` › `—` | 3 | 3 | 0.05 | 0.67 |
| 1151 | activity | MISSING | `div.activity[number=2B]` › `p` › `—` | 3 | 3 | 0.00 | 0.33 |
| 1152 | activity | MISSING | `td` › `img.img-fluid` › `—` | 3 | 3 | 0.01 | structure-only |
| 1153 | activity | MISSING | `div.activity.alertPadding.inte` › `p` › `—` | 3 | 3 | 0.00 | 1.00 |
| 1154 | activity | MISSING | `div.activity[number=5B]` › `div.row` › `—` | 3 | 3 | 0.03 | 1.00 |
| 1155 | activity | MISSING | `div.col-12` › `p.sassoonI-text` › `—` | 3 | 3 | 0.00 | 1.00 |
| 1156 | activity | MISSING | `div.row` › `div.col-md-4.offset-md-0.col-12.padd` › `—` | 3 | 3 | 0.00 | 1.00 |
| 1157 | activity | MISSING | `div.table-responsive` › `table.table.table-bordered.tableFixe` › `—` | 3 | 3 | 0.00 | 1.00 |
| 1158 | activity | MISSING | `div.row` › `div.col-md-8.col-12.paddingR` › `—` | 3 | 3 | 0.01 | 1.00 |
| 1159 | activity | MISSING | `div.row` › `div#WF.col-12.wordFind.sassoonI-text` › `—` | 3 | 3 | 0.01 | structure-only |
| 1160 | activity | MISSING | `div.col-md-6.col-12.paddingLR` › `WIDGET` › `—` | 3 | 3 | 0.00 | structure-only |
| 1161 | activity | MISSING | `div.activity[number=2B]` › `WIDGET` › `—` | 3 | 3 | 0.00 | structure-only |
| 1162 | activity | MISSING | `div.activity.super-content-but` › `div.super-content.row` › `—` | 3 | 3 | 0.01 | 1.00 |
| 1163 | activity | MISSING | `div.col-md-2.col-12` › `p` › `—` | 3 | 3 | 0.00 | 0.00 |
| 1164 | activity | MISSING | `div.table-responsive` › `table.table.sassoonI-text` › `—` | 3 | 3 | 0.00 | 1.00 |
| 1165 | activity | MISSING | `div.col-12` › `div.col-md-12.col-12` › `—` | 3 | 3 | 0.00 | structure-only |
| 1166 | activity | MISSING | `div.col-md-4.offset-md-0.col-1` › `WIDGET` › `—` | 3 | 3 | 0.01 | structure-only |
| 1167 | activity | MISSING | `table.table.table-bordered` › `tr` › `—` | 3 | 3 | 0.01 | 1.00 |
| 1168 | activity | MISSING | `div.col-12` › `h2` › `—` | 3 | 3 | 0.00 | 0.50 |
| 1169 | activity | MISSING | `div.activity.dropbox[number=4A` › `div.row` › `—` | 3 | 3 | 0.00 | 1.00 |
| 1170 | activity | MISSING | `ol` › `ul` › `—` | 3 | 3 | 0.00 | 0.75 |
| 1171 | activity | MISSING | `ol` › `ol` › `—` | 3 | 3 | 0.00 | 1.00 |
| 1172 | activity | MISSING | `div.col-1` › `img.img-fluid.imageCentral` › `—` | 3 | 3 | 0.01 | structure-only |
| 1173 | activity | MISSING | `div.row.justify-content-betwee` › `div.col-1` › `—` | 3 | 3 | 0.01 | structure-only |
| 1174 | activity | MISSING | `div.hintDropContent` › `p` › `—` | 3 | 3 | 0.02 | 1.00 |
| 1175 | activity | MISSING | `a` › `img.img-fluid` › `—` | 3 | 3 | 0.00 | structure-only |
| 1176 | activity | MISSING | `div.activity.interactive[numbe` › `WIDGET` › `—` | 3 | 3 | 0.00 | structure-only |
| 1177 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 3 | 3 | 0.00 | structure-only |
| 1178 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 3 | 3 | 0.01 | 1.00 |
| 1179 | activity | MISSING | `div.activity[number=7E]` › `div.row` › `—` | 3 | 3 | 0.01 | 0.67 |
| 1180 | activity | MISSING | `div.embedPDF[layout=portrait]` › `object` › `—` | 3 | 3 | 0.00 | 0.33 |
| 1181 | activity | MISSING | `div.activity[number=4C]` › `div.row` › `—` | 3 | 3 | 0.03 | 1.00 |
| 1182 | activity | MISSING | `div.activity.interactive.alert` › `div.row` › `—` | 3 | 3 | 0.01 | 1.00 |
| 1183 | activity | MISSING | `div.activity[number=8A]` › `div.row` › `—` | 3 | 3 | 0.01 | 1.00 |
| 1184 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 3 | 3 | 0.00 | 1.00 |
| 1185 | activity | MISSING | `div.activity.interactive.alert` › `div.row` › `—` | 3 | 3 | 0.00 | 1.00 |
| 1186 | activity | MISSING | `div.activity.interactive[numbe` › `p` › `—` | 3 | 3 | 0.00 | 0.80 |
| 1187 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 3 | 3 | 0.00 | 1.00 |
| 1188 | activity | MISSING | `div.col-md-8.col-12` › `div.activity[number=9B]` › `—` | 3 | 3 | 0.01 | 0.67 |
| 1189 | activity | MISSING | `div.activity.interactive[numbe` › `WIDGET` › `—` | 3 | 3 | 0.01 | structure-only |
| 1190 | activity | MISSING | `div.alert` › `p` › `—` | 3 | 3 | 0.00 | 0.60 |
| 1191 | activity | MISSING | `div.activity.dropbox[number=10` › `div.row` › `—` | 3 | 3 | 0.00 | 0.67 |
| 1192 | activity | MISSING | `div.clickDropContent.activity.` › `p` › `—` | 3 | 3 | 0.00 | 1.00 |
| 1193 | activity | MOVED | `div.col-8` › `h3` › `h3` | 3 | 3 | 0.00 | structure-only |
| 1194 | activity | MOVED | `div.activity.interactive[numbe` › `p` › `p` | 3 | 3 | 0.00 | structure-only |
| 1195 | activity | MOVED | `div.col-12` › `p>span.infoTrigger` › `p>span.infoTrigger` | 3 | 3 | 0.03 | structure-only |
| 1196 | activity | MOVED | `div.col-md-8.col-12` › `p>b` › `p>b` | 3 | 3 | 0.00 | structure-only |
| 1197 | activity | MOVED | `div.row` › `h4.goJournal` › `h4.goJournal` | 3 | 3 | 0.00 | structure-only |
| 1198 | activity | MOVED | `div.activity.dropbox[number=6A` › `h3` › `h3` | 3 | 3 | 0.00 | structure-only |
| 1199 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 3 | 3 | 0.00 | structure-only |
| 1200 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 3 | 3 | 0.00 | structure-only |
| 1201 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 3 | 3 | 0.00 | structure-only |
| 1202 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 3 | 3 | 0.00 | structure-only |
| 1203 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 3 | 3 | 0.00 | structure-only |
| 1204 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 3 | 3 | 0.00 | structure-only |
| 1205 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 3 | 3 | 0.00 | structure-only |
| 1206 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 3 | 3 | 0.00 | structure-only |
| 1207 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 3 | 3 | 0.00 | structure-only |
| 1208 | activity | MOVED | `div.clickDropContent.activity.` › `h3` › `h3` | 3 | 3 | 0.00 | structure-only |
| 1209 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 3 | 3 | 0.00 | structure-only |
| 1210 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 3 | 3 | 0.00 | structure-only |
| 1211 | activity | SUBSTITUTED | `div.row` › `div.col-12` › `li` | 3 | 3 | 0.79 | structure-only |
| 1212 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=4A]` › `div.activity` | 3 | 3 | 0.03 | structure-only |
| 1213 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=3B]` › `div.alert.solid` | 3 | 3 | 0.04 | structure-only |
| 1214 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=1A]` › `h3` | 3 | 3 | 0.05 | structure-only |
| 1215 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=4A]` › `div.activity` | 3 | 3 | 0.04 | structure-only |
| 1216 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=8A]` › `h3` | 3 | 3 | 0.01 | structure-only |
| 1217 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `li` | 3 | 3 | 0.14 | structure-only |
| 1218 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.dropbox[number=3C]` › `h3` | 3 | 3 | 0.01 | structure-only |
| 1219 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=4C]` › `h4` | 3 | 3 | 0.03 | structure-only |
| 1220 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=5B]` › `div.activity` | 3 | 3 | 0.03 | structure-only |
| 1221 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=6B]` › `div.activity` | 3 | 3 | 0.02 | structure-only |
| 1222 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=3A]` › `div.activity` | 3 | 3 | 0.01 | structure-only |
| 1223 | activity | SUBSTITUTED | `div.row` › `div.col-12` › `iframe` | 3 | 3 | 0.79 | structure-only |
| 1224 | activity | SUBSTITUTED | `div.col-12` › `div.button.TKmodalButton` › `p` | 3 | 3 | 0.01 | structure-only |
| 1225 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=4B]` › `div.activity[number=4A]` | 3 | 3 | 0.04 | structure-only |
| 1226 | activity | SUBSTITUTED | `div.col-12` › `h5` › `p` | 3 | 3 | 0.04 | structure-only |
| 1227 | activity | SUBSTITUTED | `div.col-12` › `a` › `div.ratio.ratio-16x9` | 3 | 3 | 0.57 | structure-only |
| 1228 | activity | SUBSTITUTED | `a` › `div.externalButton` › `iframe` | 3 | 3 | 0.10 | structure-only |
| 1229 | activity | SUBSTITUTED | `div.col-12` › `h4.goJournal` › `img.img-fluid` | 3 | 3 | 0.12 | structure-only |
| 1230 | activity | SUBSTITUTED | `a` › `div.button` › `a` | 3 | 3 | 0.48 | structure-only |
| 1231 | activity | SUBSTITUTED | `div.col-md-12.col-12` › `div.activity.interactive[number=2A]` › `div.activity[number=2A]` | 3 | 3 | 0.01 | structure-only |
| 1232 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=3D]` › `div.activity[number=3C]` | 3 | 3 | 0.02 | structure-only |
| 1233 | activity | SUBSTITUTED | `div.col-md-12.col-12` › `WIDGET` › `p` | 3 | 3 | 0.09 | structure-only |
| 1234 | activity | SUBSTITUTED | `div.row` › `div.col-md-4.col-xs-6` › `WIDGET` | 3 | 3 | 0.00 | structure-only |
| 1235 | activity | SUBSTITUTED | `div.row` › `div.col-md-4.col-xs-6` › `div.col-md-8.col-12` | 3 | 3 | 0.00 | structure-only |
| 1236 | activity | SUBSTITUTED | `div.row` › `div.col-md-4.col-xs-6` › `div.col-12` | 3 | 3 | 0.00 | structure-only |
| 1237 | activity | SUBSTITUTED | `div.col-md-4.col-xs-6` › `img.img-fluid` › `h3` | 3 | 3 | 0.00 | structure-only |
| 1238 | activity | SUBSTITUTED | `div.super-content.row` › `div.row` › `div.col-12` | 3 | 3 | 0.06 | structure-only |
| 1239 | activity | SUBSTITUTED | `div.row` › `div.col-8` › `WIDGET` | 3 | 3 | 0.02 | structure-only |
| 1240 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.super-content-button[nu` › `div.activity[number=2A]` | 3 | 3 | 0.01 | structure-only |
| 1241 | activity | SUBSTITUTED | `div.col-md-4.col-xs-6` › `img.img-fluid` › `WIDGET` | 3 | 3 | 0.00 | structure-only |
| 1242 | activity | SUBSTITUTED | `div.col-12` › `div.row.selectionBox` › `WIDGET` | 3 | 3 | 0.02 | structure-only |
| 1243 | activity | SUBSTITUTED | `div.row` › `div.col-4` › `p` | 3 | 3 | 0.01 | structure-only |
| 1244 | activity | SUBSTITUTED | `div.col-12` › `div.clickDropContent` › `div.TKmodal` | 3 | 3 | 0.10 | structure-only |
| 1245 | activity | SUBSTITUTED | `div.col-12` › `div.clickDropContent` › `div.videoSection.ratio.ratio-16x9` | 3 | 3 | 0.10 | structure-only |
| 1246 | activity | SUBSTITUTED | `div.clickDropContent` › `div.videoSection.icon.ratio.ratio-16` › `div.row` | 3 | 3 | 0.01 | structure-only |
| 1247 | activity | SUBSTITUTED | `div.row` › `div.col-md-4.col-xs-6.paddingR` › `div.col-12` | 3 | 3 | 0.00 | structure-only |
| 1248 | activity | SUBSTITUTED | `div.col-md-4.col-xs-6.paddingR` › `img.img-fluid` › `h3` | 3 | 3 | 0.00 | structure-only |
| 1249 | activity | SUBSTITUTED | `div.col-md-4.col-xs-6.paddingR` › `img.img-fluid` › `WIDGET` | 3 | 3 | 0.00 | structure-only |
| 1250 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=1E]` › `div.activity[number=1E]` | 3 | 3 | 0.02 | structure-only |
| 1251 | activity | SUBSTITUTED | `div.row` › `div.row` › `WIDGET` | 3 | 3 | 0.02 | structure-only |
| 1252 | activity | SUBSTITUTED | `div.col-12` › `div.activity.interactive[number=1B]` › `div.activity[number=1B]` | 3 | 3 | 0.01 | structure-only |
| 1253 | activity | SUBSTITUTED | `div.col-12` › `div.videoSection.icon.ratio.ratio-16` › `div.col-md-8.col-12` | 3 | 3 | 0.09 | structure-only |
| 1254 | activity | SUBSTITUTED | `div.col-12` › `div.videoSection.icon.ratio.ratio-16` › `WIDGET` | 3 | 3 | 0.09 | structure-only |
| 1255 | activity | SUBSTITUTED | `div.row` › `div.col-md-4.col-12` › `p` | 3 | 3 | 0.02 | structure-only |
| 1256 | activity | SUBSTITUTED | `div.col-12` › `div.row` › `div.alertActivity` | 3 | 3 | 0.22 | structure-only |
| 1257 | activity | SUBSTITUTED | `div.row` › `div.col-12` › `h3` | 3 | 3 | 0.79 | structure-only |
| 1258 | activity | SUBSTITUTED | `div.col-md-12.col-12` › `div.activity.interactive[number=1C]` › `div.activity[number=1C]` | 3 | 3 | 0.01 | structure-only |
| 1259 | activity | SUBSTITUTED | `div.col-md-4.col-12.paddingLR` › `WIDGET` › `div.col-12` | 3 | 3 | 0.03 | structure-only |
| 1260 | activity | SUBSTITUTED | `div.col-md-4.col-12.paddingLR` › `WIDGET` › `div.row` | 3 | 3 | 0.03 | structure-only |
| 1261 | activity | SUBSTITUTED | `div.row` › `div.col-11` › `div.col-12` | 3 | 3 | 0.00 | structure-only |
| 1262 | activity | SUBSTITUTED | `a` › `div.buttonD` › `div.buttonD` | 3 | 3 | 0.09 | structure-only |
| 1263 | activity | SUBSTITUTED | `div.col-12` › `div.row.flipCardsContainer` › `p` | 3 | 3 | 0.04 | structure-only |
| 1264 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding.interactiv` › `p` | 3 | 3 | 0.01 | structure-only |
| 1265 | activity | SUBSTITUTED | `div.activity.alertPadding.inte` › `p>span.sassoonI-text` › `p` | 3 | 3 | 0.00 | structure-only |
| 1266 | activity | SUBSTITUTED | `div.activity.alertPadding.inte` › `WIDGET` › `div.row` | 3 | 3 | 0.00 | structure-only |
| 1267 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=2F]` › `div.activity[number=2F]` | 3 | 3 | 0.00 | structure-only |
| 1268 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive.alertPaddin` › `div.activity[number=5A]` | 3 | 3 | 0.01 | structure-only |
| 1269 | activity | SUBSTITUTED | `div.row` › `div.col-md-12.col-12` › `p` | 3 | 3 | 0.11 | structure-only |
| 1270 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `h3` | 3 | 3 | 0.12 | structure-only |
| 1271 | activity | SUBSTITUTED | `div.col-12` › `div.row` › `div.button.audioButton` | 3 | 3 | 0.22 | structure-only |
| 1272 | activity | SUBSTITUTED | `p` › `br` › `a` | 3 | 3 | 0.09 | structure-only |
| 1273 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=3A]` › `div.activity[number=3A]` | 3 | 3 | 0.01 | structure-only |
| 1274 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=5B]` › `div.activity[number=5B]` | 3 | 3 | 0.01 | structure-only |
| 1275 | activity | SUBSTITUTED | `a` › `div.buttonD` › `a` | 3 | 3 | 0.09 | structure-only |
| 1276 | activity | SUBSTITUTED | `div.col-12` › `div.table-responsive` › `th` | 3 | 3 | 0.08 | structure-only |
| 1277 | activity | SUBSTITUTED | `div.activity[number=2B]` › `h3` › `div.row` | 3 | 3 | 0.00 | structure-only |
| 1278 | activity | SUBSTITUTED | `div.activity[number=2E]` › `h3` › `div.row` | 3 | 3 | 0.00 | structure-only |
| 1279 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive.alertPaddin` › `div.activity[number=2A]` | 3 | 3 | 0.01 | structure-only |
| 1280 | activity | SUBSTITUTED | `div.super-content.row` › `div.row` › `div.col-md-8.col-12` | 3 | 3 | 0.06 | structure-only |
| 1281 | activity | SUBSTITUTED | `div.col-md-10.col-12` › `div.activity.interactive[number=1B]` › `div.activity[number=1B]` | 3 | 3 | 0.01 | structure-only |
| 1282 | activity | SUBSTITUTED | `div.row` › `div.col` › `WIDGET` | 3 | 3 | 0.01 | structure-only |
| 1283 | activity | SUBSTITUTED | `div.col-md-2.col-12` › `p` › `p` | 3 | 3 | 0.00 | structure-only |
| 1284 | activity | SUBSTITUTED | `div.col-12` › `div.table-responsive.sassoonI-text` › `WIDGET` | 3 | 3 | 0.00 | structure-only |
| 1285 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=3C]` › `div.activity[number=3C]` | 3 | 3 | 0.01 | structure-only |
| 1286 | activity | SUBSTITUTED | `div.clickDropContent` › `div.row` › `div.clickDropContent` | 3 | 3 | 0.01 | structure-only |
| 1287 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=2E]` › `div.activity[number=2E]` | 3 | 3 | 0.01 | structure-only |
| 1288 | activity | SUBSTITUTED | `div.col-12` › `div.row` › `p>b` | 3 | 3 | 0.22 | structure-only |
| 1289 | activity | SUBSTITUTED | `div.col-md-4.offset-md-0.col-1` › `WIDGET` › `p` | 3 | 3 | 0.01 | structure-only |
| 1290 | activity | SUBSTITUTED | `div.table-responsive` › `table.table.table-bordered` › `div.table-responsive` | 3 | 3 | 0.03 | structure-only |
| 1291 | activity | SUBSTITUTED | `div.col-12` › `div.alert` › `div.alert` | 3 | 3 | 0.02 | structure-only |
| 1292 | activity | SUBSTITUTED | `div.col-12` › `div.row` › `h3` | 3 | 3 | 0.22 | structure-only |
| 1293 | activity | SUBSTITUTED | `div.activity.interactive[numbe` › `h3` › `div.row` | 3 | 3 | 0.00 | structure-only |
| 1294 | activity | SUBSTITUTED | `div.col-12` › `div.activity.interactive[number=2C]` › `div.activity[number=2C]` | 3 | 3 | 0.01 | structure-only |
| 1295 | activity | SUBSTITUTED | `div.col-md-12.col-12` › `WIDGET` › `WIDGET` | 3 | 3 | 0.09 | structure-only |
| 1296 | activity | SUBSTITUTED | `div.col-12` › `div.row` › `div.videoSection.ratio.ratio-16x9` | 3 | 3 | 0.22 | structure-only |
| 1297 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=1B]` › `p` | 3 | 3 | 0.04 | structure-only |
| 1298 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=2E]` › `h3` | 3 | 3 | 0.04 | structure-only |
| 1299 | activity | SUBSTITUTED | `ol` › `li>i` › `li` | 3 | 3 | 0.01 | structure-only |
| 1300 | activity | SUBSTITUTED | `div.col-12` › `div.videoSection.icon.ratio.ratio-16` › `p` | 3 | 3 | 0.09 | structure-only |
| 1301 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=5A]` › `p` | 3 | 3 | 0.03 | structure-only |
| 1302 | activity | SUBSTITUTED | `a` › `div.button` › `div.videoSection.ratio.ratio-16x9` | 3 | 3 | 0.48 | structure-only |
| 1303 | activity | SUBSTITUTED | `div.col-12` › `p` › `p>a` | 3 | 3 | 0.76 | structure-only |
| 1304 | activity | SUBSTITUTED | `div.col-12` › `p.quoteText` › `p>i` | 3 | 3 | 0.01 | structure-only |
| 1305 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive.alertPaddin` › `div.activity[number=3A]` | 3 | 3 | 0.01 | structure-only |
| 1306 | activity | SUBSTITUTED | `div.col-12` › `div.videoSection.icon.ratio.ratio-16` › `div.row` | 3 | 3 | 0.09 | structure-only |
| 1307 | activity | SUBSTITUTED | `a` › `div.button` › `div.col-md-8.col-12>a` | 3 | 3 | 0.48 | structure-only |
| 1308 | activity | SUBSTITUTED | `div.col-12` › `div.row` › `a` | 3 | 3 | 0.22 | structure-only |
| 1309 | activity | SUBSTITUTED | `div.row` › `div.col-12` › `div.externalButton` | 3 | 3 | 0.79 | structure-only |
| 1310 | activity | SUBSTITUTED | `ul` › `li` › `div.button` | 3 | 3 | 0.20 | structure-only |
| 1311 | activity | SUBSTITUTED | `ul` › `li` › `li>b` | 3 | 3 | 0.20 | structure-only |
| 1312 | activity | SUBSTITUTED | `div.col-12` › `div.slider` › `WIDGET` | 3 | 3 | 0.01 | structure-only |
| 1313 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=2B]` › `div.activity` | 3 | 3 | 0.05 | structure-only |
| 1314 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=2C]` › `h4` | 3 | 3 | 0.04 | structure-only |
| 1315 | activity | SUBSTITUTED | `div.col-12` › `p` › `li` | 3 | 3 | 0.76 | structure-only |
| 1316 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=4B]` › `div.activity[number=4B]` | 3 | 3 | 0.01 | structure-only |
| 1317 | activity | SUBSTITUTED | `a` › `div.externalButton` › `div.row` | 3 | 3 | 0.10 | structure-only |
| 1318 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=3A]` › `h5` | 3 | 3 | 0.03 | structure-only |
| 1319 | activity | SUBSTITUTED | `ol` › `p` › `p` | 3 | 3 | 0.00 | structure-only |
| 1320 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=2B]` › `h4` | 3 | 3 | 0.04 | structure-only |
| 1321 | activity | SUBSTITUTED | `div.row` › `div.col-md-12.col-12` › `WIDGET` | 3 | 3 | 0.11 | structure-only |
| 1322 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=1C]` › `h4` | 3 | 3 | 0.04 | structure-only |
| 1323 | activity | SUBSTITUTED | `ol` › `li` › `li>b` | 3 | 3 | 0.17 | structure-only |
| 1324 | activity | SUBSTITUTED | `div.col-12` › `div.row.flipCardsContainer` › `div.row` | 3 | 3 | 0.04 | structure-only |
| 1325 | activity | SUBSTITUTED | `div.col-12` › `div.alert` › `img.img-fluid` | 3 | 3 | 0.02 | structure-only |
| 1326 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.dropbox[number=10A]` › `p` | 3 | 3 | 0.00 | structure-only |
| 1327 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.dropbox[number=2G]` › `div.clickDropContent.activity.dropbo` | 3 | 3 | 0.01 | structure-only |
| 1328 | activity | SUBSTITUTED | `div.col-12.col-md-8` › `div.clickDropContent.activity.dropbo` › `div.clickDropContent.activity.dropbo` | 3 | 3 | 0.00 | structure-only |
| 1329 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.dropbox[number=3G]` › `div.clickDropContent.activity.dropbo` | 3 | 3 | 0.00 | structure-only |
| 1330 | activity | SUBSTITUTED | `div.clickDropContent.activity.` › `h3` › `div.row` | 3 | 3 | 0.00 | structure-only |
| 1331 | activity | MOVED | `ol` › `li>b` › `li>b` | 5 | 2 | 0.00 | structure-only |
| 1332 | activity | SUBSTITUTED | `div.row` › `div.col-12` › `div.alertActivity` | 5 | 2 | 0.79 | structure-only |
| 1333 | activity | MISSING | `div.row` › `div.col-md-3.col-6.paddingLR` › `—` | 4 | 2 | 0.00 | structure-only |
| 1334 | activity | MISSING | `div.col-12` › `div.audioImage` › `—` | 4 | 2 | 0.00 | structure-only |
| 1335 | activity | MISSING | `h3>i` › `i` › `—` | 4 | 2 | 0.00 | 0.75 |
| 1336 | activity | SUBSTITUTED | `div.col-12` › `h4.goJournal` › `WIDGET` | 4 | 2 | 0.12 | structure-only |
| 1337 | activity | SUBSTITUTED | `div.row` › `div.col-12.paddingR` › `div.col-12` | 4 | 2 | 0.00 | structure-only |
| 1338 | activity | SUBSTITUTED | `a` › `div.button` › `div.button.TKmodalButton` | 4 | 2 | 0.48 | structure-only |
| 1339 | activity | SUBSTITUTED | `div.col-12` › `div.selfReflection` › `p` | 4 | 2 | 0.01 | structure-only |
| 1340 | activity | EXTRA | `div.clickDropContent` › `—` › `p>b` | 3 | 2 | 1.00 | structure-only |
| 1341 | activity | MISSING | `div.row` › `div.col-md-10.col-12.offset-md-1` › `—` | 3 | 2 | 0.00 | structure-only |
| 1342 | activity | MISSING | `div.row.flipCardsContainer` › `div.col-md-6.col-12.paddingLR` › `—` | 3 | 2 | 0.01 | structure-only |
| 1343 | activity | MISSING | `div.row` › `div.col-md-10.col-12` › `—` | 3 | 2 | 0.01 | 1.00 |
| 1344 | activity | MISSING | `div.col-md-8.col-12` › `WIDGET` › `—` | 3 | 2 | 0.00 | structure-only |
| 1345 | activity | MISSING | `div.col-md-12` › `h3` › `—` | 3 | 2 | 0.01 | 0.67 |
| 1346 | activity | MISSING | `div.col-12.paddingR` › `h3` › `—` | 3 | 2 | 0.00 | 1.00 |
| 1347 | activity | MISSING | `div.row` › `div.col-md-3.offset-md-1.col-12` › `—` | 3 | 2 | 0.00 | structure-only |
| 1348 | activity | MISSING | `div.col-12` › `h3>em` › `—` | 3 | 2 | 0.01 | 0.75 |
| 1349 | activity | MISSING | `div.col-12` › `div.row.choicePage.choiceHeightMatch` › `—` | 3 | 2 | 0.00 | 1.00 |
| 1350 | activity | MISSING | `div.clickDropContent` › `p.captionText` › `—` | 3 | 2 | 0.00 | 0.00 |
| 1351 | activity | MISSING | `b>span.sassoonI-text` › `span.sassoonI-text` › `—` | 3 | 2 | 0.00 | 1.00 |
| 1352 | activity | SUBSTITUTED | `div.col-12` › `div.videoSection.ratio.ratio-16x9` › `p` | 3 | 2 | 0.05 | structure-only |
| 1353 | activity | SUBSTITUTED | `p>em` › `em` › `i` | 3 | 2 | 0.00 | structure-only |
| 1354 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=6B]` › `h4` | 3 | 2 | 0.01 | structure-only |
| 1355 | activity | SUBSTITUTED | `div.col-12` › `div.row.justify-content-center.slide` › `WIDGET` | 3 | 2 | 0.01 | structure-only |
| 1356 | activity | EXTRA | `div.col-12` › `—` › `div.activity.interactive[number=5B]` | 2 | 2 | 0.99 | structure-only |
| 1357 | activity | EXTRA | `div.activity[number=8A]` › `—` › `div.row` | 2 | 2 | 1.00 | structure-only |
| 1358 | activity | EXTRA | `div.col-12` › `—` › `h3>a` | 2 | 2 | 1.00 | structure-only |
| 1359 | activity | EXTRA | `div.activity[number=1E]` › `—` › `div.row` | 2 | 2 | 1.00 | structure-only |
| 1360 | activity | EXTRA | `div.TKmodal` › `—` › `div.videoSection.ratio.ratio-16x9` | 2 | 2 | 1.00 | structure-only |
| 1361 | activity | EXTRA | `div.col-12` › `—` › `div.activity.interactive[number=1E]` | 2 | 2 | 1.00 | structure-only |
| 1362 | activity | EXTRA | `div.col-md-8.col-12` › `—` › `div.activity.interactive[number=1B]` | 2 | 2 | 0.96 | structure-only |
| 1363 | activity | EXTRA | `div.activity.super-content-but` › `—` › `div.super-content.row` | 2 | 2 | 0.99 | structure-only |
| 1364 | activity | EXTRA | `div.TKmodal` › `—` › `ol` | 2 | 2 | 1.00 | structure-only |
| 1365 | activity | EXTRA | `div.col-md-8.col-12` › `—` › `div.activity[number=5A]` | 2 | 2 | 0.97 | structure-only |
| 1366 | activity | EXTRA | `ul` › `—` › `li>i` | 2 | 2 | 1.00 | structure-only |
| 1367 | activity | EXTRA | `div.col-md-8.col-12` › `—` › `div.activity[number=2B]` | 2 | 2 | 0.95 | structure-only |
| 1368 | activity | EXTRA | `div.col-md-8.col-12` › `—` › `div.activity[number=3C]` | 2 | 2 | 0.97 | structure-only |
| 1369 | activity | EXTRA | `div.activity.interactive.super` › `—` › `div.row` | 2 | 2 | 1.00 | structure-only |
| 1370 | activity | EXTRA | `div.activity.interactive.super` › `—` › `div.row` | 2 | 2 | 1.00 | structure-only |
| 1371 | activity | EXTRA | `div.activity.interactive[numbe` › `—` › `div.row` | 2 | 2 | 0.99 | structure-only |
| 1372 | activity | EXTRA | `div.col-md-8.col-12` › `—` › `div.activity[number=5C]` | 2 | 2 | 0.98 | structure-only |
| 1373 | activity | EXTRA | `div.col-md-8.col-12` › `—` › `div.activity[number=1D]` | 2 | 2 | 0.97 | structure-only |
| 1374 | activity | EXTRA | `div.activity[number=4F]` › `—` › `div.row` | 2 | 2 | 1.00 | structure-only |
| 1375 | activity | EXTRA | `tr` › `—` › `th>b` | 2 | 2 | 1.00 | structure-only |
| 1376 | activity | EXTRA | `div.clickDropContent` › `—` › `h3` | 2 | 2 | 0.99 | structure-only |
| 1377 | activity | EXTRA | `div.col-md-8.col-12` › `—` › `div.activity.dropbox` | 2 | 2 | 1.00 | structure-only |
| 1378 | activity | EXTRA | `div.col-md-8.col-12` › `—` › `div.activity[number=1A]` | 2 | 2 | 1.00 | structure-only |
| 1379 | activity | EXTRA | `a` › `—` › `div.button.downloadButton` | 2 | 2 | 0.97 | structure-only |
| 1380 | activity | EXTRA | `div.col-md-8.col-12` › `—` › `div.activity.interactive[number=2A]` | 2 | 2 | 0.94 | structure-only |
| 1381 | activity | EXTRA | `div.row` › `—` › `div.col-md-6.col-12` | 2 | 2 | 1.00 | structure-only |
| 1382 | activity | EXTRA | `div.activity.interactive[numbe` › `—` › `div.row` | 2 | 2 | 0.99 | structure-only |
| 1383 | activity | EXTRA | `div.col-12` › `—` › `div.activity.interactive[number=7B]` | 2 | 2 | 1.00 | structure-only |
| 1384 | activity | EXTRA | `div.col-md-8.col-12` › `—` › `div.activity.interactive[number=2B]` | 2 | 2 | 0.95 | structure-only |
| 1385 | activity | EXTRA | `div.activity.interactive[numbe` › `—` › `div.row` | 2 | 2 | 1.00 | structure-only |
| 1386 | activity | EXTRA | `div.activity[number=9D]` › `—` › `div.row` | 2 | 2 | 1.00 | structure-only |
| 1387 | activity | EXTRA | `div.activity.interactive[numbe` › `—` › `div.row` | 2 | 2 | 1.00 | structure-only |
| 1388 | activity | EXTRA | `div.col-12` › `—` › `p.captionText` | 2 | 2 | 1.00 | structure-only |
| 1389 | activity | EXTRA | `div.activity[number=7C]` › `—` › `div.row` | 2 | 2 | 0.99 | structure-only |
| 1390 | activity | EXTRA | `div.activity.interactive[numbe` › `—` › `div.row` | 2 | 2 | 0.97 | structure-only |
| 1391 | activity | EXTRA | `div.col-md-8.col-12` › `—` › `div.activity.interactive[number=8C]` | 2 | 2 | 0.99 | structure-only |
| 1392 | activity | EXTRA | `ul` › `—` › `li>a` | 2 | 2 | 1.00 | structure-only |
| 1393 | activity | EXTRA | `div.activity[number=4C]` › `—` › `div.row` | 2 | 2 | 0.97 | structure-only |
| 1394 | activity | EXTRA | `div.col-md-8.col-12` › `—` › `div.activity[number=6C]` | 2 | 2 | 0.99 | structure-only |
| 1395 | activity | EXTRA | `ul` › `—` › `li>b` | 2 | 2 | 0.98 | structure-only |
| 1396 | activity | EXTRA | `div.clickDropContent.activity.` › `—` › `div.row` | 2 | 2 | 1.00 | structure-only |
| 1397 | activity | EXTRA | `div.clickDropContent.activity.` › `—` › `div.row` | 2 | 2 | 1.00 | structure-only |
| 1398 | activity | EXTRA | `div.clickDropContent.activity.` › `—` › `div.row` | 2 | 2 | 1.00 | structure-only |
| 1399 | activity | MISSING | `div.activity.interactive[numbe` › `WIDGET` › `—` | 2 | 2 | 0.00 | structure-only |
| 1400 | activity | MISSING | `div.activity.interactive[numbe` › `WIDGET` › `—` | 2 | 2 | 0.00 | structure-only |
| 1401 | activity | MISSING | `div.activity[number=7B]` › `div.row` › `—` | 2 | 2 | 0.01 | 0.50 |
| 1402 | activity | MISSING | `div.activity.dropbox[number=8D` › `div.row` › `—` | 2 | 2 | 0.00 | 0.00 |
| 1403 | activity | MISSING | `div.activity[number=6A]` › `div.row` › `—` | 2 | 2 | 0.02 | 1.00 |
| 1404 | activity | MISSING | `div.activity[number=7A]` › `div.row` › `—` | 2 | 2 | 0.01 | 0.50 |
| 1405 | activity | MISSING | `div.activity[number=5D]` › `div.row` › `—` | 2 | 2 | 0.01 | 1.00 |
| 1406 | activity | MISSING | `li` › `a` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1407 | activity | MISSING | `ol.activityList` › `li` › `—` | 2 | 2 | 0.00 | 0.71 |
| 1408 | activity | MISSING | `li` › `i` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1409 | activity | MISSING | `ol` › `a` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1410 | activity | MISSING | `p>span` › `span` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1411 | activity | MISSING | `div.col` › `p` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1412 | activity | MISSING | `div.typingSlides` › `WIDGET` › `—` | 2 | 2 | 0.00 | structure-only |
| 1413 | activity | MISSING | `div.col-12` › `div.clickDropContent.noBorder` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1414 | activity | MISSING | `div.clickDropContent.noBorder` › `WIDGET` › `—` | 2 | 2 | 0.00 | structure-only |
| 1415 | activity | MISSING | `div.row` › `div.col-md-5.col-xs-6` › `—` | 2 | 2 | 0.00 | structure-only |
| 1416 | activity | MISSING | `div.row` › `div.col-3` › `—` | 2 | 2 | 0.00 | structure-only |
| 1417 | activity | MISSING | `div.activity[number=6E]` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1418 | activity | MISSING | `div.activity.alertPadding[numb` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1419 | activity | MISSING | `div.activity[number=6H]` › `div.row` › `—` | 2 | 2 | 0.00 | 0.50 |
| 1420 | activity | MISSING | `div.activity.super-content-but` › `div.super-content.row` › `—` | 2 | 2 | 0.01 | 1.00 |
| 1421 | activity | MISSING | `div.col-md-8.col-12` › `div.activity[number=1D]` › `—` | 2 | 2 | 0.03 | 1.00 |
| 1422 | activity | MISSING | `div.col-md-8.col-12` › `div.activity.interactive[number=1E]` › `—` | 2 | 2 | 0.02 | 1.00 |
| 1423 | activity | MISSING | `div.col-12` › `div.row>a` › `—` | 2 | 2 | 0.00 | 0.50 |
| 1424 | activity | MISSING | `div.activity.super-content-but` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1425 | activity | MISSING | `div.table-responsive.sassoonI-` › `table.table.table-bordered` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1426 | activity | MISSING | `div.row.supervisor` › `div.col-md-12.col-12.super-content-b` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1427 | activity | MISSING | `div.activity.super-content-but` › `div.row` › `—` | 2 | 2 | 0.01 | 1.00 |
| 1428 | activity | MISSING | `div.activity.alertPadding.inte` › `p` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1429 | activity | MISSING | `div.activity[number=2F]` › `ol` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1430 | activity | MISSING | `div.activity.alertPadding[numb` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1431 | activity | MISSING | `div.row` › `div.table-responsive` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1432 | activity | MISSING | `table.table` › `tr` › `—` | 2 | 2 | 0.01 | 1.00 |
| 1433 | activity | MISSING | `div.col-md-6.col-12` › `h5` › `—` | 2 | 2 | 0.00 | 0.50 |
| 1434 | activity | MISSING | `div.row` › `div.col-md-3.offset-md-0.col-12` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1435 | activity | MISSING | `div.activity.alertPadding.inte` › `p` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1436 | activity | MISSING | `div.activity.alertPadding.inte` › `WIDGET` › `—` | 2 | 2 | 0.00 | structure-only |
| 1437 | activity | MISSING | `div.activity[number=4H]` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1438 | activity | MISSING | `div.col-12` › `p.center-text` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1439 | activity | MISSING | `div.activity[number=3G]` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1440 | activity | MISSING | `div.activity[number=4G]` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1441 | activity | MISSING | `div.activity[number=5G]` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1442 | activity | MISSING | `div.row` › `div.col-md-4.col-xs-6.paddingLR` › `—` | 2 | 2 | 0.00 | structure-only |
| 1443 | activity | MISSING | `div.col-12` › `div.table-responsive.sassoonI-text` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1444 | activity | MISSING | `div.col-12` › `audio.audioPlayer` › `—` | 2 | 2 | 0.00 | structure-only |
| 1445 | activity | MISSING | `div.col-md-8.col-12` › `div.activity.interactive[number=5D]` › `—` | 2 | 2 | 0.01 | 1.00 |
| 1446 | activity | MISSING | `div.row` › `div.col-md-6.offset-md-3.col-12` › `—` | 2 | 2 | 0.01 | 1.00 |
| 1447 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1448 | activity | MISSING | `div.activity.interactive.super` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1449 | activity | MISSING | `div.col-md-8.col-12` › `div.activity[number=1A]` › `—` | 2 | 2 | 0.05 | 1.00 |
| 1450 | activity | MISSING | `div.activity[number=2A]` › `p` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1451 | activity | MISSING | `div.activity[number=2A]` › `ul` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1452 | activity | MISSING | `div.table-responsive` › `table.table.table-bordered.tableFixe` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1453 | activity | MISSING | `div.col-md-6.offset-md-0.col-1` › `img.img-fluid` › `—` | 2 | 2 | 0.00 | structure-only |
| 1454 | activity | MISSING | `div.activity.super-content-but` › `div.super-content.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1455 | activity | MISSING | `div.col-md-6.col-12` › `WIDGET` › `—` | 2 | 2 | 0.00 | structure-only |
| 1456 | activity | MISSING | `div.row` › `div.col-6` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1457 | activity | MISSING | `div.activity.interactive[numbe` › `div.clearDiv` › `—` | 2 | 2 | 0.00 | structure-only |
| 1458 | activity | MISSING | `div.col-8` › `h5` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1459 | activity | MISSING | `div.col-8` › `br` › `—` | 2 | 2 | 0.00 | structure-only |
| 1460 | activity | MISSING | `div.row.paddingB.paddingT` › `div.audioImage` › `—` | 2 | 2 | 0.00 | structure-only |
| 1461 | activity | MISSING | `div.activity.alertPadding.supe` › `div.super-content.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1462 | activity | MISSING | `div.col-12` › `div.row.flipCardsContainer.sassoon-t` › `—` | 2 | 2 | 0.00 | structure-only |
| 1463 | activity | MISSING | `div.activity.alertPadding.supe` › `p` › `—` | 2 | 2 | 0.00 | 0.67 |
| 1464 | activity | MISSING | `div.activity.alertPadding.supe` › `WIDGET` › `—` | 2 | 2 | 0.00 | structure-only |
| 1465 | activity | MISSING | `div.col-md-8.col-12` › `div.activity.interactive[number=1C]` › `—` | 2 | 2 | 0.04 | 0.50 |
| 1466 | activity | MISSING | `div.row` › `div` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1467 | activity | MISSING | `div.activity[number=2E]` › `a` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1468 | activity | MISSING | `div.col-md-2.col-12` › `div.audioButton` › `—` | 2 | 2 | 0.00 | structure-only |
| 1469 | activity | MISSING | `div.row.super-content` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1470 | activity | MISSING | `div.clickDropContent` › `WIDGET` › `—` | 2 | 2 | 0.00 | structure-only |
| 1471 | activity | MISSING | `p` › `em` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1472 | activity | MISSING | `div.col-md-8.col-12` › `div.activity[number=2A]` › `—` | 2 | 2 | 0.04 | 0.50 |
| 1473 | activity | MISSING | `div.col-md-8.col-12` › `div.activity[number=6A]` › `—` | 2 | 2 | 0.02 | 1.00 |
| 1474 | activity | MISSING | `div.col-md-4.offset-md-0.col-1` › `img.img-fluid` › `—` | 2 | 2 | 0.00 | structure-only |
| 1475 | activity | MISSING | `table.table.table-bordered` › `tbody` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1476 | activity | MISSING | `div.activity.interactive[numbe` › `WIDGET` › `—` | 2 | 2 | 0.00 | structure-only |
| 1477 | activity | MISSING | `div.activity.interactive[numbe` › `img.img-fluid` › `—` | 2 | 2 | 0.00 | structure-only |
| 1478 | activity | MISSING | `div.activity[number=2B]` › `a` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1479 | activity | MISSING | `div.activity.interactive[numbe` › `p` › `—` | 2 | 2 | 0.00 | 0.50 |
| 1480 | activity | MISSING | `div.activity[number=2E]` › `WIDGET` › `—` | 2 | 2 | 0.00 | structure-only |
| 1481 | activity | MISSING | `div.activity[number=2E]` › `p` › `—` | 2 | 2 | 0.00 | 0.50 |
| 1482 | activity | MISSING | `div.col-12` › `p.red-text` › `—` | 2 | 2 | 0.00 | 0.00 |
| 1483 | activity | MISSING | `div.col-md-8.col-12` › `div.activity[number=2D]` › `—` | 2 | 2 | 0.03 | 1.00 |
| 1484 | activity | MISSING | `div.activity.alertPadding.inte` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1485 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1486 | activity | MISSING | `div.activity.alertPadding[numb` › `div.row` › `—` | 2 | 2 | 0.01 | 1.00 |
| 1487 | activity | MISSING | `div.activity.dropbox[number=7A` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1488 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1489 | activity | MISSING | `div.activity.dropbox[number=4C` › `div.row` › `—` | 2 | 2 | 0.01 | 1.00 |
| 1490 | activity | MISSING | `div.activity.alertPadding[numb` › `div.row` › `—` | 2 | 2 | 0.01 | 1.00 |
| 1491 | activity | MISSING | `div.clickDropContent` › `h5` › `—` | 2 | 2 | 0.01 | 1.00 |
| 1492 | activity | MISSING | `div.activity.dropbox[number=1B` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1493 | activity | MISSING | `div.activity.dropbox[number=3A` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1494 | activity | MISSING | `li>span.infoTrigger` › `span.infoTrigger` › `—` | 2 | 2 | 0.01 | 1.00 |
| 1495 | activity | MISSING | `div.activity.dropbox[number=1A` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1496 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1497 | activity | MISSING | `div.activity.interactive[numbe` › `br` › `—` | 2 | 2 | 0.00 | structure-only |
| 1498 | activity | MISSING | `div.activity.dropbox[number=8A` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1499 | activity | MISSING | `div.col-12` › `p>span.ch-text` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1500 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 2 | 2 | 0.00 | 0.50 |
| 1501 | activity | MISSING | `div.activity.alertPadding[numb` › `div.row` › `—` | 2 | 2 | 0.01 | 1.00 |
| 1502 | activity | MISSING | `li` › `b` › `—` | 2 | 2 | 0.01 | 1.00 |
| 1503 | activity | MISSING | `div.col-12` › `div.alert.solid.margL0` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1504 | activity | MISSING | `div.activity[number=7C]` › `div.row` › `—` | 2 | 2 | 0.01 | 1.00 |
| 1505 | activity | MISSING | `div.col-md-8.col-12` › `div.activity[number=9C]` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1506 | activity | MISSING | `div.TKmodal` › `p` › `—` | 2 | 2 | 0.01 | 1.00 |
| 1507 | activity | MISSING | `span.infoTrigger>b` › `b` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1508 | activity | MISSING | `div.alert.solid` › `p` › `—` | 2 | 2 | 0.00 | 0.20 |
| 1509 | activity | MISSING | `div.activity[number=2E]` › `div.clickDropContent` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1510 | activity | MISSING | `div.col-md-8.col-12` › `div.activity.interactive[number=4B]` › `—` | 2 | 2 | 0.02 | 1.00 |
| 1511 | activity | MISSING | `div.col-md-12.col-12` › `ul` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1512 | activity | MISSING | `p` › `p` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1513 | activity | MISSING | `div.activity[number=6D]` › `div.row` › `—` | 2 | 2 | 0.01 | 1.00 |
| 1514 | activity | MISSING | `div.activity.interactive[numbe` › `p` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1515 | activity | MISSING | `div.activity.interactive[numbe` › `p` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1516 | activity | MISSING | `div.activity.alertPadding` › `div.row` › `—` | 2 | 2 | 0.00 | 0.50 |
| 1517 | activity | MISSING | `div.col-md-8.col-12` › `div.activity[number=7B]` › `—` | 2 | 2 | 0.01 | 1.00 |
| 1518 | activity | MISSING | `div.activity.alertPadding[numb` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1519 | activity | MISSING | `li>a` › `a` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1520 | activity | MISSING | `div.activity.alertPadding[numb` › `div.row` › `—` | 2 | 2 | 0.01 | 1.00 |
| 1521 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 2 | 2 | 0.01 | 0.50 |
| 1522 | activity | MISSING | `div.clickDropContent` › `p>b` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1523 | activity | MISSING | `div.alert.solid` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1524 | activity | MISSING | `div.activity[number=4D]` › `div.row` › `—` | 2 | 2 | 0.02 | 0.50 |
| 1525 | activity | MISSING | `div.activity.interactive[numbe` › `WIDGET` › `—` | 2 | 2 | 0.00 | structure-only |
| 1526 | activity | MISSING | `div.clickDropContent` › `p.quoteText` › `—` | 2 | 2 | 0.00 | 0.00 |
| 1527 | activity | MISSING | `ol` › `p>i` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1528 | activity | MISSING | `p` › `h5` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1529 | activity | MISSING | `p` › `div.videoSection.icon.ratio.ratio-16` › `—` | 2 | 2 | 0.00 | structure-only |
| 1530 | activity | MISSING | `li` › `b.primary-text` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1531 | activity | MISSING | `ol` › `p` › `—` | 2 | 2 | 0.00 | 0.50 |
| 1532 | activity | MISSING | `div.activity.dropbox` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1533 | activity | MISSING | `div.activity.alertPadding[numb` › `div.row` › `—` | 2 | 2 | 0.01 | 1.00 |
| 1534 | activity | MISSING | `div.activity.interactive[numbe` › `p` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1535 | activity | MISSING | `li>strong` › `strong` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1536 | activity | MISSING | `div.slideContainer` › `p.slideQuestion` › `—` | 2 | 2 | 0.00 | 0.67 |
| 1537 | activity | MISSING | `div.row` › `br` › `—` | 2 | 2 | 0.00 | structure-only |
| 1538 | activity | MISSING | `div.activity[number=3C]` › `div.row` › `—` | 2 | 2 | 0.03 | 1.00 |
| 1539 | activity | MISSING | `div.activity.alertPadding.drop` › `div.row` › `—` | 2 | 2 | 0.00 | 0.50 |
| 1540 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1541 | activity | MISSING | `div.activity.interactive.alert` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1542 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 2 | 2 | 0.00 | structure-only |
| 1543 | activity | MISSING | `div.activity[number=8G]` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1544 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1545 | activity | MISSING | `div.col-12` › `div.alert.blank` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1546 | activity | MISSING | `div.col-md-8.col-12` › `div.activity.interactive[number=4A]` › `—` | 2 | 2 | 0.03 | 0.50 |
| 1547 | activity | MISSING | `div.activity.interactive[numbe` › `WIDGET` › `—` | 2 | 2 | 0.00 | structure-only |
| 1548 | activity | MISSING | `div.activity.interactive[numbe` › `p` › `—` | 2 | 2 | 0.00 | 0.50 |
| 1549 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1550 | activity | MISSING | `div.activity[number=7F]` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1551 | activity | MISSING | `div.col-md-8.col-12` › `div.activity[number=5A]` › `—` | 2 | 2 | 0.03 | 1.00 |
| 1552 | activity | MISSING | `div.row` › `div.col-md-8.col-12.offset-md-2` › `—` | 2 | 2 | 0.01 | structure-only |
| 1553 | activity | MISSING | `ol` › `li>b` › `—` | 2 | 2 | 0.00 | 0.25 |
| 1554 | activity | MISSING | `div.col-md-8.col-12` › `div.activity.interactive[number=2A]` › `—` | 2 | 2 | 0.06 | 0.50 |
| 1555 | activity | MISSING | `div.col-12` › `div.col-md-6.offset-md-3.col-12` › `—` | 2 | 2 | 0.00 | structure-only |
| 1556 | activity | MISSING | `div.col-md-6.offset-md-0.col-1` › `img.img-fluid` › `—` | 2 | 2 | 0.00 | structure-only |
| 1557 | activity | MISSING | `div.activity.alertPadding[numb` › `div.row` › `—` | 2 | 2 | 0.01 | 0.50 |
| 1558 | activity | MISSING | `div.col-md-12.col-12` › `h2` › `—` | 2 | 2 | 0.00 | 0.67 |
| 1559 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 1560 | activity | MISSING | `div.col-md-8.col-12` › `div.activity[number=2C]` › `—` | 2 | 2 | 0.04 | 1.00 |
| 1561 | activity | MISSING | `div.col-md-8.col-12` › `div.activity[number=8B]` › `—` | 2 | 2 | 0.01 | 1.00 |
| 1562 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 2 | 2 | 0.00 | 0.67 |
| 1563 | activity | MISSING | `div.activity.dropbox[number=2A` › `div.row` › `—` | 2 | 2 | 0.01 | 0.50 |
| 1564 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 2 | 2 | 0.00 | 0.00 |
| 1565 | activity | MISSING | `div.activity.interactive[numbe` › `div.row` › `—` | 2 | 2 | 0.00 | 0.00 |
| 1566 | activity | MISSING | `div.row` › `div.col.paddingR` › `—` | 2 | 2 | 0.00 | 0.92 |
| 1567 | activity | MISSING | `div.clickDropContent.activity.` › `div.videoSection.ratio.ratio-16x9` › `—` | 2 | 2 | 0.00 | structure-only |
| 1568 | activity | MISSING | `div.col-12` › `div.selfReflection` › `—` | 2 | 2 | 0.01 | structure-only |
| 1569 | activity | MOVED | `div.row` › `h3` › `h3` | 2 | 2 | 0.00 | structure-only |
| 1570 | activity | MOVED | `div.col-md-8.col-12` › `p>b` › `p` | 2 | 2 | 0.00 | structure-only |
| 1571 | activity | MOVED | `div.activity[number=2F]` › `p` › `p` | 2 | 2 | 0.00 | structure-only |
| 1572 | activity | MOVED | `div.col-8` › `p` › `p` | 2 | 2 | 0.00 | structure-only |
| 1573 | activity | MOVED | `div.activity.super-content-but` › `p` › `p` | 2 | 2 | 0.00 | structure-only |
| 1574 | activity | MOVED | `div.col-12` › `h5` › `h5` | 2 | 2 | 0.01 | structure-only |
| 1575 | activity | MOVED | `div.activity[number=2E]` › `a` › `a` | 2 | 2 | 0.00 | structure-only |
| 1576 | activity | MOVED | `div.row` › `a` › `a` | 2 | 2 | 0.01 | structure-only |
| 1577 | activity | MOVED | `tr` › `td>b` › `td>b` | 2 | 2 | 0.01 | structure-only |
| 1578 | activity | MOVED | `div.activity[number=1E]` › `p` › `p` | 2 | 2 | 0.00 | structure-only |
| 1579 | activity | MOVED | `div.activity[number=5C]` › `p` › `p` | 2 | 2 | 0.00 | structure-only |
| 1580 | activity | MOVED | `div.col-md-12` › `h3` › `h3` | 2 | 2 | 0.01 | structure-only |
| 1581 | activity | MOVED | `ol` › `p` › `p` | 2 | 2 | 0.00 | structure-only |
| 1582 | activity | MOVED | `div.activity.interactive[numbe` › `h3` › `h3` | 2 | 2 | 0.00 | structure-only |
| 1583 | activity | MOVED | `div.col-md-8.col-12.paddingR` › `p` › `p` | 2 | 2 | 0.00 | structure-only |
| 1584 | activity | MOVED | `div.alert.solid` › `p` › `p` | 2 | 2 | 0.00 | structure-only |
| 1585 | activity | MOVED | `div.col-md-12.col-12` › `h2` › `h2` | 2 | 2 | 0.00 | structure-only |
| 1586 | activity | MOVED | `div.activity.dropbox[number=1A` › `h3` › `h3` | 2 | 2 | 0.00 | structure-only |
| 1587 | activity | MOVED | `div.activity.dropbox[number=3A` › `h3` › `h3` | 2 | 2 | 0.00 | structure-only |
| 1588 | activity | MOVED | `div.activity.dropbox[number=4A` › `h3` › `h3` | 2 | 2 | 0.00 | structure-only |
| 1589 | activity | MOVED | `div.activity.dropbox[number=5A` › `h3` › `h3` | 2 | 2 | 0.00 | structure-only |
| 1590 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 2 | 2 | 0.00 | structure-only |
| 1591 | activity | MOVED | `div.activity.dropbox[number=7A` › `h3` › `h3` | 2 | 2 | 0.00 | structure-only |
| 1592 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 2 | 2 | 0.00 | structure-only |
| 1593 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 2 | 2 | 0.00 | structure-only |
| 1594 | activity | MOVED | `div.activity.dropbox[number=4A` › `p` › `p` | 2 | 2 | 0.00 | structure-only |
| 1595 | activity | MOVED | `div.activity.dropbox[number=5A` › `p` › `p` | 2 | 2 | 0.00 | structure-only |
| 1596 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 2 | 2 | 0.00 | structure-only |
| 1597 | activity | MOVED | `div.clickDropContent.activity.` › `h3` › `h3` | 2 | 2 | 0.00 | structure-only |
| 1598 | activity | MOVED | `div.clickDropContent.activity.` › `h3` › `h3` | 2 | 2 | 0.00 | structure-only |
| 1599 | activity | MOVED | `div.clickDropContent.activity.` › `h3` › `h3` | 2 | 2 | 0.00 | structure-only |
| 1600 | activity | MOVED | `div.clickDropContent.activity.` › `h3` › `h3` | 2 | 2 | 0.00 | structure-only |
| 1601 | activity | MOVED | `div.clickDropContent.activity.` › `p` › `p` | 2 | 2 | 0.00 | structure-only |
| 1602 | activity | MOVED | `div.clickDropContent.activity.` › `h3` › `h3` | 2 | 2 | 0.00 | structure-only |
| 1603 | activity | MOVED | `div.clickDropContent.activity.` › `h3` › `h3` | 2 | 2 | 0.00 | structure-only |
| 1604 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=2B]` › `h3` | 2 | 2 | 0.04 | structure-only |
| 1605 | activity | SUBSTITUTED | `div.clickDropContent` › `ol` › `li` | 2 | 2 | 0.02 | structure-only |
| 1606 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=1B]` › `div.activity` | 2 | 2 | 0.01 | structure-only |
| 1607 | activity | SUBSTITUTED | `div.col-12` › `h3` › `td` | 2 | 2 | 0.76 | structure-only |
| 1608 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive.alertPaddin` › `div.activity.interactive[number=5A]` | 2 | 2 | 0.01 | structure-only |
| 1609 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=7A]` › `div.activity.interactive[number=6A]` | 2 | 2 | 0.01 | structure-only |
| 1610 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=2A]` › `div.activity.interactive` | 2 | 2 | 0.06 | structure-only |
| 1611 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=6B]` › `div.activity.interactive` | 2 | 2 | 0.01 | structure-only |
| 1612 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=2A]` › `h3` | 2 | 2 | 0.01 | structure-only |
| 1613 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=4A]` › `div.activity.interactive` | 2 | 2 | 0.04 | structure-only |
| 1614 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=5A]` › `div.activity.interactive` | 2 | 2 | 0.03 | structure-only |
| 1615 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=6A]` › `h4` | 2 | 2 | 0.02 | structure-only |
| 1616 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=9A]` › `h3` | 2 | 2 | 0.01 | structure-only |
| 1617 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=1A]` › `div.activity` | 2 | 2 | 0.05 | structure-only |
| 1618 | activity | SUBSTITUTED | `div.videoSection.icon.ratio.ra` › `iframe.embed-responsive-item` › `li` | 2 | 2 | 0.08 | structure-only |
| 1619 | activity | SUBSTITUTED | `a` › `div.button` › `div.activity[number=2C]` | 2 | 2 | 0.48 | structure-only |
| 1620 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=4C]` › `div.activity.interactive[number=4C]` | 2 | 2 | 0.03 | structure-only |
| 1621 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=8A]` › `div.activity` | 2 | 2 | 0.01 | structure-only |
| 1622 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=4A]` › `div.activity.interactive[number=4A]` | 2 | 2 | 0.01 | structure-only |
| 1623 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=6C]` › `div.activity.interactive[number=6A]` | 2 | 2 | 0.01 | structure-only |
| 1624 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.dropbox[number=7A]` › `p` | 2 | 2 | 0.00 | structure-only |
| 1625 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=1A]` › `p` | 2 | 2 | 0.05 | structure-only |
| 1626 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=1A]` › `div.col-md-8.col-12` | 2 | 2 | 0.05 | structure-only |
| 1627 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=4B]` › `div.activity[number=3B]` | 2 | 2 | 0.04 | structure-only |
| 1628 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=4C]` › `div.activity[number=3C]` | 2 | 2 | 0.03 | structure-only |
| 1629 | activity | SUBSTITUTED | `div.col-12` › `div.row` › `div.videoSection.icon.ratio.ratio-16` | 2 | 2 | 0.22 | structure-only |
| 1630 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=3C]` › `div.activity` | 2 | 2 | 0.01 | structure-only |
| 1631 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=6B]` › `div.activity[number=6B]` | 2 | 2 | 0.01 | structure-only |
| 1632 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=9A]` › `div.activity[number=9A]` | 2 | 2 | 0.00 | structure-only |
| 1633 | activity | SUBSTITUTED | `div.col-12` › `div.hint` › `h4.goJournal` | 2 | 2 | 0.07 | structure-only |
| 1634 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=1A]` › `h4` | 2 | 2 | 0.05 | structure-only |
| 1635 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=1D]` › `div.activity[number=1C]` | 2 | 2 | 0.00 | structure-only |
| 1636 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive.alertPaddin` › `div.activity.interactive[number=4A]` | 2 | 2 | 0.00 | structure-only |
| 1637 | activity | SUBSTITUTED | `div.col-md-12.col-12` › `WIDGET` › `p>a` | 2 | 2 | 0.09 | structure-only |
| 1638 | activity | SUBSTITUTED | `ul` › `li` › `p` | 2 | 2 | 0.20 | structure-only |
| 1639 | activity | SUBSTITUTED | `p>span` › `span` › `b` | 2 | 2 | 0.01 | structure-only |
| 1640 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=7A]` › `h3` | 2 | 2 | 0.00 | structure-only |
| 1641 | activity | SUBSTITUTED | `a` › `div.button` › `div.videoSection.icon.ratio.ratio-16` | 2 | 2 | 0.48 | structure-only |
| 1642 | activity | SUBSTITUTED | `div.col-md-12.col-12` › `div.activity.interactive[number=3A]` › `div.activity[number=3A]` | 2 | 2 | 0.01 | structure-only |
| 1643 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=2C]` › `div.activity.interactive[number=2B]` | 2 | 2 | 0.04 | structure-only |
| 1644 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=3C]` › `h4` | 2 | 2 | 0.03 | structure-only |
| 1645 | activity | SUBSTITUTED | `div.col-12` › `div.row` › `div.col-md-8.col-12.paddingR` | 2 | 2 | 0.22 | structure-only |
| 1646 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding.super-cont` › `div.alert.solid` | 2 | 2 | 0.00 | structure-only |
| 1647 | activity | SUBSTITUTED | `div.activity.alertPadding.supe` › `div.super-content.row` › `div.row` | 2 | 2 | 0.00 | structure-only |
| 1648 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=2H]` › `h3` | 2 | 2 | 0.01 | structure-only |
| 1649 | activity | SUBSTITUTED | `div.row` › `div.col-12` › `div.TKmodal` | 2 | 2 | 0.79 | structure-only |
| 1650 | activity | SUBSTITUTED | `div.col-12` › `div.clickDropContent` › `div.alertActivity` | 2 | 2 | 0.10 | structure-only |
| 1651 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding.super-cont` › `div.alert.solid` | 2 | 2 | 0.00 | structure-only |
| 1652 | activity | SUBSTITUTED | `div.activity.alertPadding.supe` › `div.super-content.row` › `div.row` | 2 | 2 | 0.00 | structure-only |
| 1653 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=6F]` › `div.activity[number=6F]` | 2 | 2 | 0.00 | structure-only |
| 1654 | activity | SUBSTITUTED | `div.row` › `div.col-12` › `ul` | 2 | 2 | 0.79 | structure-only |
| 1655 | activity | SUBSTITUTED | `div.col-12` › `h3` › `li` | 2 | 2 | 0.76 | structure-only |
| 1656 | activity | SUBSTITUTED | `div.activity.interactive[numbe` › `div.row` › `WIDGET` | 2 | 2 | 0.03 | structure-only |
| 1657 | activity | SUBSTITUTED | `div.row` › `div.col-12` › `div#footer` | 2 | 2 | 0.79 | structure-only |
| 1658 | activity | SUBSTITUTED | `div.col-12` › `p.sassoon-text` › `p` | 2 | 2 | 0.00 | structure-only |
| 1659 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=2B]` › `div.activity.super-content-button[nu` | 2 | 2 | 0.05 | structure-only |
| 1660 | activity | SUBSTITUTED | `div.col-md-12.col-12.super-con` › `div.super-content.row` › `WIDGET` | 2 | 2 | 0.00 | structure-only |
| 1661 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.super-content-button[nu` › `h3` | 2 | 2 | 0.01 | structure-only |
| 1662 | activity | SUBSTITUTED | `div.row` › `div.col-md-4.col-12` › `div.TKmodal` | 2 | 2 | 0.02 | structure-only |
| 1663 | activity | SUBSTITUTED | `div.activity[number=2F]` › `h3` › `div.row` | 2 | 2 | 0.00 | structure-only |
| 1664 | activity | SUBSTITUTED | `div.row` › `div.col-4` › `li` | 2 | 2 | 0.01 | structure-only |
| 1665 | activity | SUBSTITUTED | `div.clickDropContent` › `div.videoSection.icon.ratio.ratio-16` › `div.videoSection.ratio.ratio-16x9` | 2 | 2 | 0.01 | structure-only |
| 1666 | activity | SUBSTITUTED | `div.col-12` › `div.row.flipCardsContainer` › `p>a` | 2 | 2 | 0.04 | structure-only |
| 1667 | activity | SUBSTITUTED | `div.row.flipCardsContainer` › `div.col-md-4.col-12.paddingLR` › `li` | 2 | 2 | 0.02 | structure-only |
| 1668 | activity | SUBSTITUTED | `div.row` › `div.col-12` › `p>b` | 2 | 2 | 0.79 | structure-only |
| 1669 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=7B]` › `p` | 2 | 2 | 0.01 | structure-only |
| 1670 | activity | SUBSTITUTED | `div.col-4` › `WIDGET` › `p` | 2 | 2 | 0.01 | structure-only |
| 1671 | activity | SUBSTITUTED | `div.row` › `div.col-4` › `img.img-fluid.TKmodalButton` | 2 | 2 | 0.01 | structure-only |
| 1672 | activity | SUBSTITUTED | `div.row` › `div.row` › `div.TKmodal` | 2 | 2 | 0.02 | structure-only |
| 1673 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=8F]` › `div.activity[number=8F]` | 2 | 2 | 0.00 | structure-only |
| 1674 | activity | SUBSTITUTED | `div.col-4` › `WIDGET` › `li` | 2 | 2 | 0.01 | structure-only |
| 1675 | activity | SUBSTITUTED | `div.col-12` › `div.clickDropContent` › `li` | 2 | 2 | 0.10 | structure-only |
| 1676 | activity | SUBSTITUTED | `tr` › `td.sassoonI-text` › `td` | 2 | 2 | 0.01 | structure-only |
| 1677 | activity | SUBSTITUTED | `div.col-12` › `p` › `div.buttonD` | 2 | 2 | 0.76 | structure-only |
| 1678 | activity | SUBSTITUTED | `div.row.flipCardsContainer` › `div.col-md-4.col-12.paddingLR` › `div.col-md-8.col-12` | 2 | 2 | 0.02 | structure-only |
| 1679 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=2E]` › `audio.audioPlayer.icon` | 2 | 2 | 0.04 | structure-only |
| 1680 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.super-content-button.in` › `div.activity.interactive.super-conte` | 2 | 2 | 0.00 | structure-only |
| 1681 | activity | SUBSTITUTED | `div.row` › `div.col-md-6.col-12` › `div.col-md-8.col-12` | 2 | 2 | 0.01 | structure-only |
| 1682 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding.interactiv` › `div.activity[number=1D]` | 2 | 2 | 0.00 | structure-only |
| 1683 | activity | SUBSTITUTED | `div.col-md-12.col-12` › `div.activity.interactive[number=2D]` › `div.activity[number=2D]` | 2 | 2 | 0.00 | structure-only |
| 1684 | activity | SUBSTITUTED | `div.table-responsive` › `table.table` › `table.table.table-bordered` | 2 | 2 | 0.02 | structure-only |
| 1685 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding.interactiv` › `div.activity[number=2A]` | 2 | 2 | 0.00 | structure-only |
| 1686 | activity | SUBSTITUTED | `div.activity.alertPadding.inte` › `WIDGET` › `div.row` | 2 | 2 | 0.00 | structure-only |
| 1687 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=4C]` › `div.alert.solid` | 2 | 2 | 0.01 | structure-only |
| 1688 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=2C]` › `p` | 2 | 2 | 0.03 | structure-only |
| 1689 | activity | SUBSTITUTED | `div.col-md-12.col-12` › `p>i` › `p>i` | 2 | 2 | 0.00 | structure-only |
| 1690 | activity | SUBSTITUTED | `div.col-12` › `div.row.sassoonI-text` › `p` | 2 | 2 | 0.00 | structure-only |
| 1691 | activity | SUBSTITUTED | `div.col-md-4.col-xs-6` › `img.img-fluid` › `img.img-fluid` | 2 | 2 | 0.00 | structure-only |
| 1692 | activity | SUBSTITUTED | `p` › `span.sassoonI-text` › `li` | 2 | 2 | 0.00 | structure-only |
| 1693 | activity | SUBSTITUTED | `div.col-12` › `div.alert` › `div.row` | 2 | 2 | 0.02 | structure-only |
| 1694 | activity | SUBSTITUTED | `div.row` › `div.col-12` › `div.alert.solid` | 2 | 2 | 0.79 | structure-only |
| 1695 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding.interactiv` › `div.activity.interactive[number=3D]` | 2 | 2 | 0.00 | structure-only |
| 1696 | activity | SUBSTITUTED | `div.activity.alertPadding.inte` › `h3` › `div.row` | 2 | 2 | 0.00 | structure-only |
| 1697 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=6A]` › `div.activity[number=6A]` | 2 | 2 | 0.00 | structure-only |
| 1698 | activity | SUBSTITUTED | `div.col-12` › `p` › `div.activity.interactive[number=1H]` | 2 | 2 | 0.76 | structure-only |
| 1699 | activity | SUBSTITUTED | `div.col-12` › `div.activity.interactive[number=2A]` › `div.activity[number=2A]` | 2 | 2 | 0.01 | structure-only |
| 1700 | activity | SUBSTITUTED | `ol` › `li` › `td` | 2 | 2 | 0.17 | structure-only |
| 1701 | activity | SUBSTITUTED | `div.col-md-4.col-xs-6.paddingL` › `img.img-fluid` › `img.img-fluid` | 2 | 2 | 0.00 | structure-only |
| 1702 | activity | SUBSTITUTED | `div.row` › `div.col-4` › `div.row` | 2 | 2 | 0.01 | structure-only |
| 1703 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive.alertPaddin` › `div.activity.interactive[number=4C]` | 2 | 2 | 0.00 | structure-only |
| 1704 | activity | SUBSTITUTED | `div.col-12` › `br` › `WIDGET` | 2 | 2 | 0.06 | structure-only |
| 1705 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=2D]` › `div.activity.super-content-button[nu` | 2 | 2 | 0.03 | structure-only |
| 1706 | activity | SUBSTITUTED | `div.col-12` › `p>i` › `p>i` | 2 | 2 | 0.10 | structure-only |
| 1707 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=1C]` › `div.activity[number=1C]` | 2 | 2 | 0.01 | structure-only |
| 1708 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=2E]` › `div.activity.interactive[number=2E]` | 2 | 2 | 0.01 | structure-only |
| 1709 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=1B]` › `div.activity.interactive[number=1A]` | 2 | 2 | 0.04 | structure-only |
| 1710 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=1E]` › `p` | 2 | 2 | 0.02 | structure-only |
| 1711 | activity | SUBSTITUTED | `div.col-12` › `div.row` › `div.button.TKmodalButton` | 2 | 2 | 0.22 | structure-only |
| 1712 | activity | SUBSTITUTED | `p` › `br` › `i` | 2 | 2 | 0.09 | structure-only |
| 1713 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=1B]` › `p` | 2 | 2 | 0.04 | structure-only |
| 1714 | activity | SUBSTITUTED | `div.activity[number=1B]` › `WIDGET` › `WIDGET` | 2 | 2 | 0.00 | structure-only |
| 1715 | activity | SUBSTITUTED | `div.col-md-6.col-12.paddingLR` › `WIDGET` › `WIDGET` | 2 | 2 | 0.01 | structure-only |
| 1716 | activity | SUBSTITUTED | `div.col-12` › `ol` › `p>b` | 2 | 2 | 0.13 | structure-only |
| 1717 | activity | SUBSTITUTED | `div.activity[number=2A]` › `h3` › `div.row` | 2 | 2 | 0.00 | structure-only |
| 1718 | activity | SUBSTITUTED | `div.activity[number=2A]` › `p` › `p` | 2 | 2 | 0.00 | structure-only |
| 1719 | activity | SUBSTITUTED | `div.row.flipCardsContainer.jus` › `div.col-md-3.col-12.paddingLR` › `table.table.table-bordered` | 2 | 2 | 0.00 | structure-only |
| 1720 | activity | SUBSTITUTED | `div.col-md-3.col-12.paddingLR` › `WIDGET` › `tr` | 2 | 2 | 0.00 | structure-only |
| 1721 | activity | SUBSTITUTED | `div.col-12` › `p` › `div.activity.interactive[number=1B]` | 2 | 2 | 0.76 | structure-only |
| 1722 | activity | SUBSTITUTED | `div.col-12` › `audio.audioPlayer.icon` › `p` | 2 | 2 | 0.01 | structure-only |
| 1723 | activity | SUBSTITUTED | `div.col-12` › `div.table-responsive` › `p>a` | 2 | 2 | 0.08 | structure-only |
| 1724 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.super-content-button[nu` › `div.activity[number=1A]` | 2 | 2 | 0.01 | structure-only |
| 1725 | activity | SUBSTITUTED | `div.row` › `div.col-md-6.offset-md-0.col-12.padd` › `div.col-md-8.col-12` | 2 | 2 | 0.00 | structure-only |
| 1726 | activity | SUBSTITUTED | `a` › `div.button.buttonD` › `div.button` | 2 | 2 | 0.01 | structure-only |
| 1727 | activity | SUBSTITUTED | `div.row` › `div.col-md-4.col-12` › `div.row` | 2 | 2 | 0.02 | structure-only |
| 1728 | activity | SUBSTITUTED | `div.col-12` › `div.clickDropContent` › `img.img-fluid.TKmodalButton` | 2 | 2 | 0.10 | structure-only |
| 1729 | activity | SUBSTITUTED | `div.col-md-4.col-12.paddingLR` › `WIDGET` › `div.col-md-8.col-12` | 2 | 2 | 0.03 | structure-only |
| 1730 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding.interactiv` › `div.activity.interactive[number=1D]` | 2 | 2 | 0.00 | structure-only |
| 1731 | activity | SUBSTITUTED | `div.col-12` › `div.row.justify-content-center` › `p>a` | 2 | 2 | 0.00 | structure-only |
| 1732 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding.interactiv` › `div.activity.interactive[number=1A]` | 2 | 2 | 0.00 | structure-only |
| 1733 | activity | SUBSTITUTED | `a` › `div.buttonD` › `WIDGET` | 2 | 2 | 0.09 | structure-only |
| 1734 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=1D]` › `div.activity.interactive[number=1D]` | 2 | 2 | 0.03 | structure-only |
| 1735 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=2E]` › `div.activity[number=2E]` | 2 | 2 | 0.01 | structure-only |
| 1736 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=4D]` › `div.activity[number=4D]` | 2 | 2 | 0.01 | structure-only |
| 1737 | activity | SUBSTITUTED | `div.clickDropContent` › `p` › `p>a` | 2 | 2 | 0.07 | structure-only |
| 1738 | activity | SUBSTITUTED | `div.col-12` › `div.row.paddingB.paddingT` › `audio.audioPlayer.icon` | 2 | 2 | 0.00 | structure-only |
| 1739 | activity | SUBSTITUTED | `div.col-12` › `div.row.flipCardsContainer.sassoon-t` › `WIDGET` | 2 | 2 | 0.00 | structure-only |
| 1740 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding.super-cont` › `div.activity[number=2A]` | 2 | 2 | 0.00 | structure-only |
| 1741 | activity | SUBSTITUTED | `div.col-md-12.col-12` › `p.sassoon-text` › `p` | 2 | 2 | 0.00 | structure-only |
| 1742 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding.super-cont` › `div.activity.super-content-button[nu` | 2 | 2 | 0.00 | structure-only |
| 1743 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding.super-cont` › `div.activity.super-content-button[nu` | 2 | 2 | 0.00 | structure-only |
| 1744 | activity | SUBSTITUTED | `div.activity.alertPadding.supe` › `div.row.super-content` › `div.super-content.row` | 2 | 2 | 0.00 | structure-only |
| 1745 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding.super-cont` › `div.activity.super-content-button[nu` | 2 | 2 | 0.00 | structure-only |
| 1746 | activity | SUBSTITUTED | `div.activity.alertPadding.supe` › `div.row.super-content` › `div.super-content.row` | 2 | 2 | 0.00 | structure-only |
| 1747 | activity | SUBSTITUTED | `div.row` › `div.col-md-4.col-12` › `div.clickDropContent` | 2 | 2 | 0.02 | structure-only |
| 1748 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=1C]` › `div.activity[number=1C]` | 2 | 2 | 0.04 | structure-only |
| 1749 | activity | SUBSTITUTED | `div.activity[number=1C]` › `div.row` › `div.row` | 2 | 2 | 0.04 | structure-only |
| 1750 | activity | SUBSTITUTED | `div.col-md-12.col-12` › `div.activity.interactive[number=1B]` › `div.activity[number=1B]` | 2 | 2 | 0.01 | structure-only |
| 1751 | activity | SUBSTITUTED | `div.activity[number=2D]` › `div.row` › `div.row` | 2 | 2 | 0.04 | structure-only |
| 1752 | activity | SUBSTITUTED | `div.col-12` › `WIDGET` › `div.buttonD` | 2 | 2 | 0.60 | structure-only |
| 1753 | activity | SUBSTITUTED | `div.col-12` › `p` › `div.videoSection.ratio.ratio-16x9` | 2 | 2 | 0.76 | structure-only |
| 1754 | activity | SUBSTITUTED | `div.activity.interactive[numbe` › `div.row` › `div.row` | 2 | 2 | 0.03 | structure-only |
| 1755 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=2E]` › `div.row` | 2 | 2 | 0.04 | structure-only |
| 1756 | activity | SUBSTITUTED | `div.row` › `div.col-4` › `div.col-md-8.col-12` | 2 | 2 | 0.01 | structure-only |
| 1757 | activity | SUBSTITUTED | `div.row` › `div.col-md-4.col-12` › `div.col-12` | 2 | 2 | 0.02 | structure-only |
| 1758 | activity | SUBSTITUTED | `div.col-12` › `div#WF.col-12.wordFind.sassoonI-text` › `WIDGET` | 2 | 2 | 0.00 | structure-only |
| 1759 | activity | SUBSTITUTED | `div.col-12` › `ul` › `ul` | 2 | 2 | 0.17 | structure-only |
| 1760 | activity | SUBSTITUTED | `div.col-md-10.col-12` › `div.activity.interactive.alertPaddin` › `div.activity[number=1E]` | 2 | 2 | 0.00 | structure-only |
| 1761 | activity | SUBSTITUTED | `div.row` › `div.col-md-4.col-12` › `p>a` | 2 | 2 | 0.02 | structure-only |
| 1762 | activity | SUBSTITUTED | `div.col-md-4.col-12.paddingLR` › `WIDGET` › `p` | 2 | 2 | 0.03 | structure-only |
| 1763 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=1D]` › `div.activity[number=1D]` | 2 | 2 | 0.00 | structure-only |
| 1764 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=4C]` › `div.activity[number=4C]` | 2 | 2 | 0.01 | structure-only |
| 1765 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=7C]` › `div.activity[number=7C]` | 2 | 2 | 0.00 | structure-only |
| 1766 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=7E]` › `div.activity[number=7E]` | 2 | 2 | 0.00 | structure-only |
| 1767 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive.alertPaddin` › `div.activity[number=1B]` | 2 | 2 | 0.00 | structure-only |
| 1768 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.dropbox[number=2E]` › `div.activity[number=2E]` | 2 | 2 | 0.00 | structure-only |
| 1769 | activity | SUBSTITUTED | `div.clickDropContent` › `p>i` › `p` | 2 | 2 | 0.01 | structure-only |
| 1770 | activity | SUBSTITUTED | `table.table.table-bordered` › `tr` › `table.table.table-bordered` | 2 | 2 | 0.02 | structure-only |
| 1771 | activity | SUBSTITUTED | `tr` › `td` › `tr` | 2 | 2 | 0.09 | structure-only |
| 1772 | activity | SUBSTITUTED | `div.col-12` › `div.clickDropContent` › `ul` | 2 | 2 | 0.10 | structure-only |
| 1773 | activity | SUBSTITUTED | `div.row` › `div.col-md-6.col-12` › `div.row` | 2 | 2 | 0.01 | structure-only |
| 1774 | activity | SUBSTITUTED | `div.alert` › `div.row` › `div.row` | 2 | 2 | 0.01 | structure-only |
| 1775 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive.alertPaddin` › `WIDGET` | 2 | 2 | 0.00 | structure-only |
| 1776 | activity | SUBSTITUTED | `a` › `div.button.buttonD` › `WIDGET` | 2 | 2 | 0.01 | structure-only |
| 1777 | activity | SUBSTITUTED | `div.col-md-12.col-12` › `WIDGET` › `div.row` | 2 | 2 | 0.09 | structure-only |
| 1778 | activity | SUBSTITUTED | `tr` › `td>b` › `td` | 2 | 2 | 0.01 | structure-only |
| 1779 | activity | SUBSTITUTED | `div.col-12` › `WIDGET` › `td` | 2 | 2 | 0.60 | structure-only |
| 1780 | activity | SUBSTITUTED | `p` › `br` › `li` | 2 | 2 | 0.09 | structure-only |
| 1781 | activity | SUBSTITUTED | `div.col-12` › `div.button` › `a` | 2 | 2 | 0.00 | structure-only |
| 1782 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=4B]` › `h3` | 2 | 2 | 0.04 | structure-only |
| 1783 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=1A]` › `h5` | 2 | 2 | 0.05 | structure-only |
| 1784 | activity | SUBSTITUTED | `div.col-12` › `div.row` › `h5` | 2 | 2 | 0.22 | structure-only |
| 1785 | activity | SUBSTITUTED | `div.col-12` › `h2` › `h3` | 2 | 2 | 0.00 | structure-only |
| 1786 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding.interactiv` › `h3` | 2 | 2 | 0.00 | structure-only |
| 1787 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=3A]` › `p` | 2 | 2 | 0.04 | structure-only |
| 1788 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.dropbox[number=4A]` › `p` | 2 | 2 | 0.00 | structure-only |
| 1789 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.dropbox[number=7A]` › `h3` | 2 | 2 | 0.00 | structure-only |
| 1790 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=1B]` › `div.activity[number=1A]` | 2 | 2 | 0.04 | structure-only |
| 1791 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.dropbox[number=5C]` › `div.activity[number=5C]` | 2 | 2 | 0.01 | structure-only |
| 1792 | activity | SUBSTITUTED | `div.videoSection.ratio.ratio-1` › `iframe` › `li` | 2 | 2 | 0.07 | structure-only |
| 1793 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=5B]` › `h4` | 2 | 2 | 0.02 | structure-only |
| 1794 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=5D]` › `h3` | 2 | 2 | 0.01 | structure-only |
| 1795 | activity | SUBSTITUTED | `p` › `br` › `iframe` | 2 | 2 | 0.09 | structure-only |
| 1796 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=3C]` › `div.activity.interactive[number=3D]` | 2 | 2 | 0.02 | structure-only |
| 1797 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=3D]` › `h3` | 2 | 2 | 0.01 | structure-only |
| 1798 | activity | SUBSTITUTED | `ol` › `ul` › `li` | 2 | 2 | 0.00 | structure-only |
| 1799 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=4A]` › `h4` | 2 | 2 | 0.01 | structure-only |
| 1800 | activity | SUBSTITUTED | `div.col-12` › `a` › `ul` | 2 | 2 | 0.57 | structure-only |
| 1801 | activity | SUBSTITUTED | `div.col-12` › `div.hint` › `div.col-md-8.col-12` | 2 | 2 | 0.07 | structure-only |
| 1802 | activity | SUBSTITUTED | `div.col-12` › `div.hintDropContent` › `WIDGET` | 2 | 2 | 0.08 | structure-only |
| 1803 | activity | SUBSTITUTED | `div.row` › `div.col-md-8.col-12` › `WIDGET` | 2 | 2 | 0.14 | structure-only |
| 1804 | activity | SUBSTITUTED | `div.col-md-12.col-12` › `div.activity.interactive[number=3C]` › `div.activity[number=3C]` | 2 | 2 | 0.01 | structure-only |
| 1805 | activity | SUBSTITUTED | `div.col-12` › `WIDGET` › `div.fundamentalsPanel` | 2 | 2 | 0.60 | structure-only |
| 1806 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=2D]` › `div.activity.interactive[number=2C]` | 2 | 2 | 0.02 | structure-only |
| 1807 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=3D]` › `div.activity` | 2 | 2 | 0.01 | structure-only |
| 1808 | activity | SUBSTITUTED | `h3>em` › `em` › `i` | 2 | 2 | 0.01 | structure-only |
| 1809 | activity | SUBSTITUTED | `div.col-12` › `div.hintDropContent` › `div.col-12` | 2 | 2 | 0.08 | structure-only |
| 1810 | activity | SUBSTITUTED | `div.col-md-12.col-12` › `div.row` › `p` | 2 | 2 | 0.01 | structure-only |
| 1811 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive.alertPaddin` › `div.activity.interactive[number=2A]` | 2 | 2 | 0.01 | structure-only |
| 1812 | activity | SUBSTITUTED | `div.col-md-10.col-12` › `div.activity.interactive[number=3A]` › `div.activity[number=3A]` | 2 | 2 | 0.01 | structure-only |
| 1813 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=5C]` › `div.activity[number=5B]` | 2 | 2 | 0.01 | structure-only |
| 1814 | activity | SUBSTITUTED | `div.col-12` › `div.activity.interactive[number=3B]` › `div.activity[number=3B]` | 2 | 2 | 0.00 | structure-only |
| 1815 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=7A]` › `div.activity.interactive[number=7A]` | 2 | 2 | 0.01 | structure-only |
| 1816 | activity | SUBSTITUTED | `div.col-12` › `h4` › `h3` | 2 | 2 | 0.07 | structure-only |
| 1817 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=1B]` › `div.activity[number=1A]` | 2 | 2 | 0.04 | structure-only |
| 1818 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=3C]` › `div.activity` | 2 | 2 | 0.03 | structure-only |
| 1819 | activity | SUBSTITUTED | `div.col-12` › `a` › `h5` | 2 | 2 | 0.57 | structure-only |
| 1820 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.dropbox[number=4D]` › `h3` | 2 | 2 | 0.00 | structure-only |
| 1821 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=5B]` › `h4` | 2 | 2 | 0.03 | structure-only |
| 1822 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=8C]` › `h4` | 2 | 2 | 0.01 | structure-only |
| 1823 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=10A]` › `div.activity.interactive` | 2 | 2 | 0.00 | structure-only |
| 1824 | activity | SUBSTITUTED | `div.col-12` › `p` › `th>b` | 2 | 2 | 0.76 | structure-only |
| 1825 | activity | SUBSTITUTED | `p>b` › `b` › `a` | 2 | 2 | 0.14 | structure-only |
| 1826 | activity | SUBSTITUTED | `div.col-12` › `div.TKmodal` › `p` | 2 | 2 | 0.01 | structure-only |
| 1827 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.dropbox[number=3C]` › `p` | 2 | 2 | 0.01 | structure-only |
| 1828 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=3D]` › `div.activity[number=3D]` | 2 | 2 | 0.01 | structure-only |
| 1829 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=5F]` › `h4` | 2 | 2 | 0.00 | structure-only |
| 1830 | activity | SUBSTITUTED | `div.col-12` › `div.alert.solid` › `WIDGET` | 2 | 2 | 0.01 | structure-only |
| 1831 | activity | SUBSTITUTED | `a` › `div.externalButton` › `div#footer` | 2 | 2 | 0.10 | structure-only |
| 1832 | activity | SUBSTITUTED | `div.col-12` › `WIDGET` › `p>i` | 2 | 2 | 0.60 | structure-only |
| 1833 | activity | SUBSTITUTED | `div.col-12` › `p>b` › `li` | 2 | 2 | 0.11 | structure-only |
| 1834 | activity | SUBSTITUTED | `div.col-12` › `div.alert` › `p` | 2 | 2 | 0.02 | structure-only |
| 1835 | activity | SUBSTITUTED | `div.alert` › `p` › `p` | 2 | 2 | 0.01 | structure-only |
| 1836 | activity | SUBSTITUTED | `div.col-12` › `ul` › `WIDGET` | 2 | 2 | 0.17 | structure-only |
| 1837 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=2E]` › `p` | 2 | 2 | 0.04 | structure-only |
| 1838 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=2B]` › `h3` | 2 | 2 | 0.05 | structure-only |
| 1839 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive.alertPaddin` › `div.activity.interactive[number=3A]` | 2 | 2 | 0.01 | structure-only |
| 1840 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=2A]` › `img.img-fluid` | 2 | 2 | 0.06 | structure-only |
| 1841 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=3B]` › `h3` | 2 | 2 | 0.01 | structure-only |
| 1842 | activity | SUBSTITUTED | `div.col-12` › `img.img-fluid` › `div.videoSection.ratio.ratio-16x9` | 2 | 2 | 0.12 | structure-only |
| 1843 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=7C]` › `div.activity[number=6C]` | 2 | 2 | 0.01 | structure-only |
| 1844 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=8B]` › `h4` | 2 | 2 | 0.01 | structure-only |
| 1845 | activity | SUBSTITUTED | `div.col-12` › `p` › `iframe` | 2 | 2 | 0.76 | structure-only |
| 1846 | activity | SUBSTITUTED | `div.col-12` › `div.activity.interactive[number=4A]` › `div.activity[number=4A]` | 2 | 2 | 0.01 | structure-only |
| 1847 | activity | SUBSTITUTED | `div.col-12` › `p` › `li>b` | 2 | 2 | 0.76 | structure-only |
| 1848 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=3B]` › `div.activity[number=3A]` | 2 | 2 | 0.01 | structure-only |
| 1849 | activity | SUBSTITUTED | `div.col-md-12.col-12` › `div.activity.interactive[number=6A]` › `div.activity[number=6A]` | 2 | 2 | 0.01 | structure-only |
| 1850 | activity | SUBSTITUTED | `td` › `img.img-fluid` › `img.img-fluid` | 2 | 2 | 0.02 | structure-only |
| 1851 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=3C]` › `div.activity` | 2 | 2 | 0.02 | structure-only |
| 1852 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=1A]` › `div.alert` | 2 | 2 | 0.05 | structure-only |
| 1853 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=4B]` › `div.activity` | 2 | 2 | 0.02 | structure-only |
| 1854 | activity | SUBSTITUTED | `div.col-12` › `div.activity.interactive[number=5A]` › `div.activity` | 2 | 2 | 0.01 | structure-only |
| 1855 | activity | SUBSTITUTED | `div.activity.dropbox[number=6B` › `div.row` › `WIDGET` | 2 | 2 | 0.01 | structure-only |
| 1856 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=1C]` › `h3` | 2 | 2 | 0.04 | structure-only |
| 1857 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.dropbox[number=2A]` › `div.activity.interactive[number=2A]` | 2 | 2 | 0.00 | structure-only |
| 1858 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=5C]` › `h3` | 2 | 2 | 0.02 | structure-only |
| 1859 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=5D]` › `h3` | 2 | 2 | 0.00 | structure-only |
| 1860 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=10A]` › `h4` | 2 | 2 | 0.00 | structure-only |
| 1861 | activity | SUBSTITUTED | `div.row` › `div.col-12` › `div.videoSection.icon.ratio.ratio-16` | 2 | 2 | 0.79 | structure-only |
| 1862 | activity | SUBSTITUTED | `div.col-12` › `WIDGET` › `li` | 2 | 2 | 0.60 | structure-only |
| 1863 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.button` | 2 | 2 | 0.12 | structure-only |
| 1864 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=1D]` › `div.activity` | 2 | 2 | 0.03 | structure-only |
| 1865 | activity | SUBSTITUTED | `a` › `div.externalButton` › `WIDGET` | 2 | 2 | 0.10 | structure-only |
| 1866 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=3C]` › `div.activity[number=3B]` | 2 | 2 | 0.03 | structure-only |
| 1867 | activity | SUBSTITUTED | `div.col-12` › `p` › `div.button` | 2 | 2 | 0.76 | structure-only |
| 1868 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=6A]` › `div.activity` | 2 | 2 | 0.02 | structure-only |
| 1869 | activity | SUBSTITUTED | `div.col-12` › `p>b` › `ol` | 2 | 2 | 0.11 | structure-only |
| 1870 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=2A]` › `div.activity.interactive[number=2A]` | 2 | 2 | 0.01 | structure-only |
| 1871 | activity | SUBSTITUTED | `div.col-12` › `div.button.TKmodalButton` › `a` | 2 | 2 | 0.01 | structure-only |
| 1872 | activity | SUBSTITUTED | `div.col-12` › `div.TKmodal` › `div.externalButton` | 2 | 2 | 0.01 | structure-only |
| 1873 | activity | SUBSTITUTED | `div.TKmodal` › `p` › `div.externalButton` | 2 | 2 | 0.01 | structure-only |
| 1874 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=4A]` › `div.activity` | 2 | 2 | 0.01 | structure-only |
| 1875 | activity | SUBSTITUTED | `ol` › `p` › `li` | 2 | 2 | 0.00 | structure-only |
| 1876 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.dropbox` › `h4` | 2 | 2 | 0.00 | structure-only |
| 1877 | activity | SUBSTITUTED | `div.col-md-11.col-12` › `div.activity.interactive[number=1A]` › `h4` | 2 | 2 | 0.00 | structure-only |
| 1878 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=3B]` › `h4` | 2 | 2 | 0.03 | structure-only |
| 1879 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=5A]` › `h4` | 2 | 2 | 0.01 | structure-only |
| 1880 | activity | SUBSTITUTED | `div.col-md-12.col-12` › `div.activity.interactive[number=1A]` › `h4` | 2 | 2 | 0.01 | structure-only |
| 1881 | activity | SUBSTITUTED | `div.slider` › `div.slideContainer` › `li` | 2 | 2 | 0.02 | structure-only |
| 1882 | activity | SUBSTITUTED | `div.slidePoints` › `p` › `p` | 2 | 2 | 0.01 | structure-only |
| 1883 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=4D]` › `h4` | 2 | 2 | 0.01 | structure-only |
| 1884 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=6B]` › `div.activity.interactive[number=6C]` | 2 | 2 | 0.01 | structure-only |
| 1885 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=9B]` › `div.activity[number=9B]` | 2 | 2 | 0.00 | structure-only |
| 1886 | activity | SUBSTITUTED | `div.col-12` › `div.table-responsive` › `ul` | 2 | 2 | 0.08 | structure-only |
| 1887 | activity | SUBSTITUTED | `div.row` › `div.col-md-4.col-12` › `div.col-md-8.col-12` | 2 | 2 | 0.02 | structure-only |
| 1888 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=4D]` › `h3` | 2 | 2 | 0.01 | structure-only |
| 1889 | activity | SUBSTITUTED | `div.row` › `div.col-12` › `th` | 2 | 2 | 0.79 | structure-only |
| 1890 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=2B]` › `div.activity[number=2C]` | 2 | 2 | 0.04 | structure-only |
| 1891 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=8A]` › `div.activity[number=8A]` | 2 | 2 | 0.01 | structure-only |
| 1892 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=2A]` › `div.activity.interactive[number=1A]` | 2 | 2 | 0.06 | structure-only |
| 1893 | activity | SUBSTITUTED | `a` › `div.button` › `p` | 2 | 2 | 0.48 | structure-only |
| 1894 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=2F]` › `h3` | 2 | 2 | 0.01 | structure-only |
| 1895 | activity | SUBSTITUTED | `div.col-12` › `div.row` › `td` | 2 | 2 | 0.22 | structure-only |
| 1896 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive.alertPaddin` › `h4` | 2 | 2 | 0.00 | structure-only |
| 1897 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=7A]` › `h4` | 2 | 2 | 0.01 | structure-only |
| 1898 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=3D]` › `h4` | 2 | 2 | 0.02 | structure-only |
| 1899 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=6C]` › `h4` | 2 | 2 | 0.01 | structure-only |
| 1900 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=8G]` › `h4` | 2 | 2 | 0.00 | structure-only |
| 1901 | activity | SUBSTITUTED | `div.col-12` › `ol` › `th` | 2 | 2 | 0.13 | structure-only |
| 1902 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=6B]` › `h3` | 2 | 2 | 0.02 | structure-only |
| 1903 | activity | SUBSTITUTED | `div.col-12` › `div.hint` › `td` | 2 | 2 | 0.07 | structure-only |
| 1904 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=4B]` › `h4` | 2 | 2 | 0.02 | structure-only |
| 1905 | activity | SUBSTITUTED | `a` › `div.button` › `b` | 2 | 2 | 0.48 | structure-only |
| 1906 | activity | SUBSTITUTED | `div.row` › `div.col-md-4.col-12.paddingLR` › `div.col-12` | 2 | 2 | 0.01 | structure-only |
| 1907 | activity | SUBSTITUTED | `div.row` › `div.col-md-8.col-12.paddingR` › `div.col-12` | 2 | 2 | 0.01 | structure-only |
| 1908 | activity | SUBSTITUTED | `div.activity.interactive[numbe` › `h3` › `div.row` | 2 | 2 | 0.00 | structure-only |
| 1909 | activity | SUBSTITUTED | `div.col-12` › `div.clickDropContent` › `ol` | 2 | 2 | 0.10 | structure-only |
| 1910 | activity | SUBSTITUTED | `div.activity.interactive[numbe` › `h3` › `div.row` | 2 | 2 | 0.00 | structure-only |
| 1911 | activity | SUBSTITUTED | `div.col-12` › `div.clickDropContent` › `div.button.TKmodalButton` | 2 | 2 | 0.10 | structure-only |
| 1912 | activity | SUBSTITUTED | `div.col-12` › `div.clickDropContent` › `div.col-12` | 2 | 2 | 0.10 | structure-only |
| 1913 | activity | SUBSTITUTED | `div.activity.interactive[numbe` › `h3` › `div.row` | 2 | 2 | 0.00 | structure-only |
| 1914 | activity | SUBSTITUTED | `div.col-12` › `div.hintDropContent` › `div.row` | 2 | 2 | 0.08 | structure-only |
| 1915 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=4C]` › `div.activity` | 2 | 2 | 0.01 | structure-only |
| 1916 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=4D]` › `div.activity` | 2 | 2 | 0.01 | structure-only |
| 1917 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=7D]` › `div.activity[number=7C]` | 2 | 2 | 0.00 | structure-only |
| 1918 | activity | SUBSTITUTED | `div.col-12` › `img.img-fluid` › `img.img-fluid` | 2 | 2 | 0.12 | structure-only |
| 1919 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=3B]` › `h4` | 2 | 2 | 0.01 | structure-only |
| 1920 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=1B]` › `div.row` | 2 | 2 | 0.04 | structure-only |
| 1921 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.alertPadding[number=3B]` › `div.activity[number=3B]` | 2 | 2 | 0.01 | structure-only |
| 1922 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=3C]` › `div.activity.interactive[number=3C]` | 2 | 2 | 0.03 | structure-only |
| 1923 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=2B]` › `h4` | 2 | 2 | 0.05 | structure-only |
| 1924 | activity | SUBSTITUTED | `div.col-12` › `div.slider` › `p` | 2 | 2 | 0.01 | structure-only |
| 1925 | activity | SUBSTITUTED | `div.col-12` › `div.videoSection.youtubeShort.ratio.` › `div.videoSection.ratio.ratio-16x9` | 2 | 2 | 0.00 | structure-only |
| 1926 | activity | SUBSTITUTED | `div.col-12` › `div.col-md-8.col-12` › `p` | 2 | 2 | 0.01 | structure-only |
| 1927 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=1B]` › `h3` | 2 | 2 | 0.04 | structure-only |
| 1928 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.dropbox[number=4A]` › `h3` | 2 | 2 | 0.00 | structure-only |
| 1929 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=2.1]` › `h3` | 2 | 2 | 0.00 | structure-only |
| 1930 | activity | SUBSTITUTED | `div.row` › `div.col-md-12.col-12` › `h2` | 2 | 2 | 0.11 | structure-only |
| 1931 | activity | SUBSTITUTED | `div.activity.interactive[numbe` › `div.row` › `WIDGET` | 2 | 2 | 0.00 | structure-only |
| 1932 | activity | SUBSTITUTED | `div.col-md-12.col-12` › `p>b` › `p` | 2 | 2 | 0.00 | structure-only |
| 1933 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity[number=3E]` › `div.activity[number=3D]` | 2 | 2 | 0.01 | structure-only |
| 1934 | activity | SUBSTITUTED | `div.row` › `div.col-md-3.offset-md-0.col-12` › `div.col-md-8.col-12` | 2 | 2 | 0.00 | structure-only |
| 1935 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive[number=1A]` › `div.row` | 2 | 2 | 0.05 | structure-only |
| 1936 | activity | SUBSTITUTED | `div.col-12` › `h3` › `div.table-responsive` | 2 | 2 | 0.76 | structure-only |
| 1937 | activity | SUBSTITUTED | `div.col-12` › `ul` › `audio.audioPlayer.icon` | 2 | 2 | 0.17 | structure-only |
| 1938 | activity | SUBSTITUTED | `div.col-12` › `div.audioImage` › `audio.audioPlayer.icon` | 2 | 2 | 0.01 | structure-only |
| 1939 | activity | SUBSTITUTED | `div.super-content.row` › `div.row` › `div.row` | 2 | 2 | 0.06 | structure-only |
| 1940 | activity | SUBSTITUTED | `div.col-12` › `div.videoSection.ratio.ratio-16x9` › `div.col-md-8.col-12` | 2 | 2 | 0.05 | structure-only |
| 1941 | activity | SUBSTITUTED | `div.clickDropContent.activity.` › `h3` › `div.row` | 2 | 2 | 0.00 | structure-only |
| 1942 | activity | SUBSTITUTED | `div.clickDropContent.activity.` › `h3` › `div.row` | 2 | 2 | 0.00 | structure-only |
| 1943 | activity | SUBSTITUTED | `div.col-12.col-md-8` › `div.clickDropContent.activity.dropbo` › `div.clickDropContent.activity.dropbo` | 2 | 2 | 0.00 | structure-only |
| 1944 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.dropbox[number=4G]` › `div.clickDropContent.activity.dropbo` | 2 | 2 | 0.00 | structure-only |
| 1945 | activity | SUBSTITUTED | `div.col-12.col-md-8` › `div.clickDropContent.activity.dropbo` › `div.clickDropContent.activity.dropbo` | 2 | 2 | 0.00 | structure-only |
| 1946 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.dropbox[number=7G]` › `div.clickDropContent.activity.dropbo` | 2 | 2 | 0.00 | structure-only |
| 1947 | activity | SUBSTITUTED | `div.clickDropContent.activity.` › `p` › `p` | 2 | 2 | 0.00 | structure-only |
| 1948 | activity | SUBSTITUTED | `div.clickDropContent.activity.` › `h3` › `div.row` | 2 | 2 | 0.00 | structure-only |
| 1949 | activity | SUBSTITUTED | `div.col-12` › `a` › `div.videoSection.ratio.ratio-16x9` | 2 | 2 | 0.57 | structure-only |
| 1950 | activity | SUBSTITUTED | `div.col-md-12.col-12` › `div.activity.interactive[number=3C]` › `h4` | 2 | 2 | 0.01 | structure-only |
| 1951 | activity | SUBSTITUTED | `div.col-md-8.col-12` › `div.activity.interactive.dropbox[num` › `div.activity.dropbox[number=4A]` | 2 | 2 | 0.00 | structure-only |
| 6060 | body | MISSING | `div.row` › `div.col-md-8.col-12` › `—` | 238 | 134 | 0.27 | 0.96 |
| 6061 | body | MISSING | `div.row` › `div.col-md-4.offset-md-0.col-12` › `—` | 272 | 132 | 0.21 | 0.93 |
| 6063 | body | SUBSTITUTED | `div.row` › `div.col-md-12.col-12` › `div.col-md-8.col-12` | 224 | 128 | 0.25 | structure-only |
| 6064 | body | MISSING | `div.col-md-8.col-12` › `div.row` › `—` | 176 | 119 | 0.10 | 0.94 |
| 6066 | body | MISSING | `div.col-md-8.col-12` › `img.img-fluid` › `—` | 158 | 104 | 0.24 | structure-only |
| 6069 | body | MISSING | `div.col-md-8.col-12` › `div.videoSection.icon.ratio.ratio-16` › `—` | 178 | 100 | 0.26 | 0.99 |
| 6071 | body | MISSING | `div.col-md-8.col-12` › `h4` › `—` | 129 | 90 | 0.10 | 0.80 |
| 6074 | body | MOVED | `ul` › `li` › `li` | 157 | 83 | 0.17 | structure-only |
| 6076 | body | MISSING | `div.row` › `div.col-md-4.offset-md-0.col-12.padd` › `—` | 188 | 81 | 0.14 | 0.93 |
| 6077 | body | MISSING | `p` › `br` › `—` | 150 | 80 | 0.07 | structure-only |
| 6078 | body | MOVED | `div.col-md-8.col-12` › `p` › `p` | 110 | 80 | 0.21 | structure-only |
| 6081 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12.paddingR` › `div.col-md-8.col-12` | 150 | 74 | 0.14 | structure-only |
| 6084 | body | SUBSTITUTED | `div.row` › `div.col-md-10.col-12` › `div.col-md-8.col-12` | 107 | 72 | 0.08 | structure-only |
| 6085 | body | MISSING | `div.row` › `div.row` › `—` | 94 | 71 | 0.03 | 0.94 |
| 6086 | body | MISSING | `div.col-md-8.col-12` › `ul` › `—` | 93 | 69 | 0.09 | 0.86 |
| 6087 | body | MISSING | `div.row` › `div.col-12` › `—` | 103 | 68 | 0.16 | 0.95 |
| 6090 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h2` › `h3` | 128 | 66 | 0.15 | structure-only |
| 6091 | body | MISSING | `a` › `div.externalButton` › `—` | 78 | 66 | 0.08 | 0.62 |
| 6093 | body | MOVED | `div.col-12` › `p` › `p` | 95 | 63 | 0.14 | structure-only |
| 6095 | body | MISSING | `div.col-md-8.col-12` › `div.videoSection.ratio.ratio-16x9` › `—` | 76 | 63 | 0.21 | 0.99 |
| 6097 | body | MISSING | `div.videoSection.icon.ratio.ra` › `iframe.embed-responsive-item` › `—` | 93 | 61 | 0.21 | structure-only |
| 6098 | body | MISSING | `div.col-md-8.col-12` › `div.alert` › `—` | 77 | 61 | 0.30 | 0.89 |
| 6100 | body | MISSING | `div.col-md-8.col-12` › `div.clickDropContent` › `—` | 88 | 60 | 0.04 | 0.96 |
| 6102 | body | MISSING | `p>b` › `b` › `—` | 78 | 60 | 0.15 | 0.93 |
| 6103 | body | MISSING | `ul` › `li` › `—` | 67 | 57 | 0.12 | 0.84 |
| 6104 | body | MISSING | `div.col-md-8.col-12` › `h2` › `—` | 108 | 56 | 0.08 | 0.93 |
| 6105 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.icon.ratio.ratio-16` › `div.videoSection.ratio.ratio-16x9` | 103 | 56 | 0.26 | structure-only |
| 6106 | body | MISSING | `p>span.infoTrigger` › `span.infoTrigger` › `—` | 73 | 56 | 0.15 | 0.98 |
| 6108 | body | MISSING | `div.col-md-8.col-12` › `p>b` › `—` | 62 | 56 | 0.09 | 0.80 |
| 6109 | body | MISSING | `p` › `b` › `—` | 69 | 54 | 0.10 | 0.93 |
| 6111 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row` › `img.img-fluid` | 71 | 53 | 0.25 | structure-only |
| 6112 | body | MISSING | `div.videoSection.ratio.ratio-1` › `iframe` › `—` | 68 | 52 | 0.22 | structure-only |
| 6113 | body | MISSING | `div.whakatauki` › `p` › `—` | 59 | 52 | 0.09 | 0.76 |
| 6115 | body | MISSING | `div.row` › `div.col-md-12.col-12` › `—` | 66 | 48 | 0.08 | 0.94 |
| 6117 | body | MISSING | `div.col-12` › `p` › `—` | 77 | 45 | 0.08 | 0.81 |
| 6119 | body | MISSING | `p` › `span.infoTrigger` › `—` | 59 | 44 | 0.07 | 0.94 |
| 6120 | body | MOVED | `div.col-md-8.col-12` › `h3` › `h3` | 51 | 44 | 0.17 | structure-only |
| 6121 | body | MISSING | `div#body` › `WIDGET` › `—` | 82 | 43 | 0.06 | structure-only |
| 6123 | body | MISSING | `div.col-md-8.col-12` › `a` › `—` | 45 | 42 | 0.07 | 0.45 |
| 6124 | body | MISSING | `div.fundamentalsPanel` › `div.row` › `—` | 42 | 42 | 0.01 | 0.98 |
| 6127 | body | MISSING | `div.alert` › `div.row` › `—` | 55 | 41 | 0.09 | 0.82 |
| 6130 | body | MISSING | `div.row` › `div.col-md-4.col-12` › `—` | 52 | 40 | 0.05 | 0.99 |
| 6132 | body | MISSING | `div.row` › `div.col-md-4.col-12.paddingL` › `—` | 58 | 39 | 0.06 | 0.99 |
| 6135 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row` › `p` | 42 | 38 | 0.25 | structure-only |
| 6136 | body | MISSING | `div.col-md-8.col-12` › `p>span.infoTrigger` › `—` | 41 | 38 | 0.14 | 0.89 |
| 6137 | body | MISSING | `div.row` › `div.col-md-3.offset-md-0.col-12` › `—` | 40 | 38 | 0.02 | 1.00 |
| 6138 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `p` | 46 | 37 | 0.40 | structure-only |
| 6139 | body | MISSING | `div.col-md-8.col-12` › `h5` › `—` | 47 | 36 | 0.05 | 0.91 |
| 6141 | body | SUBSTITUTED | `div.whakatauki` › `p` › `p` | 36 | 36 | 0.10 | structure-only |
| 6142 | body | MISSING | `div.col-md-8.col-12` › `br` › `—` | 55 | 35 | 0.02 | structure-only |
| 6143 | body | MISSING | `div#body` › `div.row.supervisor` › `—` | 51 | 35 | 0.12 | 0.85 |
| 6145 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row` › `WIDGET` | 43 | 34 | 0.25 | structure-only |
| 6146 | body | MISSING | `div.col-12` › `h4` › `—` | 48 | 33 | 0.16 | 0.60 |
| 6147 | body | SUBSTITUTED | `ul` › `li` › `li` | 45 | 33 | 0.35 | structure-only |
| 6148 | body | MOVED | `div.whakatauki` › `p` › `p` | 35 | 33 | 0.09 | structure-only |
| 6149 | body | MISSING | `div.row` › `div.col-md-8.col-12.paddingR` › `—` | 41 | 32 | 0.14 | 0.96 |
| 6150 | body | SUBSTITUTED | `div.row` › `div.row` › `div.row` | 37 | 32 | 0.07 | structure-only |
| 6153 | body | MISSING | `div.row` › `div.col-md-4.offset-md-0.col-6.offse` › `—` | 40 | 31 | 0.03 | 0.88 |
| 6157 | body | MOVED | `div.col-md-8.col-12` › `p>b` › `p>b` | 37 | 30 | 0.09 | structure-only |
| 6158 | body | MISSING | `div#body` › `div.inquiryPanel` › `—` | 33 | 30 | 0.01 | 0.91 |
| 6159 | body | MOVED | `div.alertActivity` › `p` › `p` | 38 | 29 | 0.10 | structure-only |
| 6164 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.icon.ratio.ratio-16` › `p` | 34 | 28 | 0.26 | structure-only |
| 6165 | body | MISSING | `div.col-md-8.col-12` › `div.row.flipCardsContainer` › `—` | 30 | 28 | 0.01 | structure-only |
| 6166 | body | MOVED | `div.alert` › `p` › `p` | 31 | 27 | 0.02 | structure-only |
| 6167 | body | MISSING | `div.inquiryPanel` › `div.row` › `—` | 28 | 27 | 0.01 | 0.94 |
| 6169 | body | MISSING | `div.col-md-8.col-12` › `div.table-responsive` › `—` | 27 | 26 | 0.08 | 0.85 |
| 6170 | body | MISSING | `div.videoSection.icon.ratio.ra` › `iframe` › `—` | 34 | 25 | 0.09 | structure-only |
| 6171 | body | SUBSTITUTED | `div#body` › `WIDGET` › `WIDGET` | 34 | 25 | 0.06 | structure-only |
| 6172 | body | MISSING | `a` › `div.button` › `—` | 32 | 25 | 0.01 | 0.73 |
| 6173 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `div.row` | 30 | 25 | 0.40 | structure-only |
| 6174 | body | MISSING | `tr` › `td` › `—` | 28 | 25 | 0.04 | 0.81 |
| 6175 | body | SUBSTITUTED | `div.row` › `div.col-md-11.col-12` › `div.col-md-8.col-12` | 25 | 25 | 0.02 | structure-only |
| 6176 | body | MISSING | `div.col-12` › `ul` › `—` | 32 | 24 | 0.12 | 0.91 |
| 6177 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row` › `div.row` | 32 | 24 | 0.25 | structure-only |
| 6178 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `p` | 28 | 24 | 0.48 | structure-only |
| 6179 | body | MOVED | `tr` › `td` › `td` | 26 | 24 | 0.04 | structure-only |
| 6181 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h2` › `h4` | 36 | 23 | 0.15 | structure-only |
| 6182 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `h5` | 31 | 23 | 0.48 | structure-only |
| 6184 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert` › `p` | 26 | 23 | 0.30 | structure-only |
| 6186 | body | MOVED | `div.col-12` › `h3` › `h3` | 34 | 22 | 0.06 | structure-only |
| 6187 | body | SUBSTITUTED | `div#body` › `div.row.supervisor` › `div.row` | 27 | 22 | 0.12 | structure-only |
| 6188 | body | MISSING | `div.row` › `div.col-md-3.offset-md-0.col-12.padd` › `—` | 26 | 22 | 0.01 | 0.98 |
| 6189 | body | MISSING | `div.row.flipCardsContainer` › `div.col-md-4.col-12.paddingLR` › `—` | 25 | 22 | 0.03 | structure-only |
| 6190 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `img.img-fluid` | 25 | 22 | 0.40 | structure-only |
| 6191 | body | MISSING | `div#body` › `div.col-md-8.col-12` › `—` | 24 | 22 | 0.02 | 1.00 |
| 6193 | body | MISSING | `div.row.flipCardsContainer` › `div.col-md-6.col-12.paddingLR` › `—` | 23 | 22 | 0.02 | structure-only |
| 6194 | body | MISSING | `div#body` › `br` › `—` | 31 | 21 | 0.01 | structure-only |
| 6196 | body | MOVED | `div.clickDropContent` › `p` › `p` | 29 | 21 | 0.05 | structure-only |
| 6198 | body | MISSING | `td` › `img.img-fluid` › `—` | 26 | 21 | 0.02 | structure-only |
| 6199 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.icon.ratio.ratio-16` › `div.row` | 24 | 21 | 0.26 | structure-only |
| 6200 | body | MISSING | `div.col-md-8.col-12` › `div.whakatauki` › `—` | 21 | 21 | 0.06 | 0.86 |
| 6202 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.col-md-12.col-12` › `div.whakatauki` | 21 | 21 | 0.03 | structure-only |
| 6203 | body | MISSING | `div.col-12` › `h3` › `—` | 37 | 20 | 0.17 | 0.95 |
| 6204 | body | SUBSTITUTED | `div.row` › `div.col-8` › `div.col-md-8.col-12` | 35 | 20 | 0.04 | structure-only |
| 6206 | body | MOVED | `div.col-md-8.col-12.paddingR` › `p` › `p` | 24 | 20 | 0.04 | structure-only |
| 6208 | body | SUBSTITUTED | `div.col-md-12.col-12` › `div.whakatauki` › `p` | 20 | 20 | 0.04 | structure-only |
| 6209 | body | SUBSTITUTED | `div.alert` › `p` › `div.row` | 36 | 19 | 0.06 | structure-only |
| 6211 | body | SUBSTITUTED | `div.row` › `div.col-12` › `div.row` | 25 | 19 | 0.55 | structure-only |
| 6212 | body | SUBSTITUTED | `div.col-12` › `p` › `p` | 24 | 19 | 0.26 | structure-only |
| 6214 | body | MISSING | `div.alertImage` › `img.img-fluid` › `—` | 23 | 19 | 0.13 | structure-only |
| 6217 | body | MOVED | `div.col-md-8.col-12` › `h4` › `h4` | 21 | 19 | 0.01 | structure-only |
| 6219 | body | EXTRA | `p>span.infoTrigger` › `—` › `span.infoTrigger` | 19 | 19 | 0.84 | structure-only |
| 6220 | body | EXTRA | `div.col-md-6.col-12` › `—` › `img.img-fluid` | 19 | 19 | 0.99 | structure-only |
| 6221 | body | MISSING | `div.row` › `div.col-md-3.col-12` › `—` | 29 | 18 | 0.03 | 0.91 |
| 6222 | body | MISSING | `div.row` › `div.col-4` › `—` | 24 | 18 | 0.02 | 0.92 |
| 6223 | body | MISSING | `p>i` › `i` › `—` | 23 | 18 | 0.09 | 0.92 |
| 6224 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert` › `div.row` | 23 | 18 | 0.30 | structure-only |
| 6227 | body | EXTRA | `div.alertActivity` › `—` › `p` | 18 | 18 | 0.97 | structure-only |
| 6228 | body | SUBSTITUTED | `div.row` › `div.col-12` › `WIDGET` | 18 | 18 | 0.55 | structure-only |
| 6230 | body | MOVED | `div.col-12` › `h4` › `h4` | 25 | 17 | 0.16 | structure-only |
| 6231 | body | MISSING | `div.row` › `div.col-md-6.offset-md-0.col-12.padd` › `—` | 20 | 17 | 0.01 | 0.88 |
| 6232 | body | MISSING | `div.row.supervisor` › `div.row` › `—` | 18 | 17 | 0.02 | 0.95 |
| 6233 | body | MISSING | `div.row` › `div.col-md-6.col-12` › `—` | 17 | 17 | 0.02 | 1.00 |
| 6234 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert` › `div.alert.solid` | 25 | 16 | 0.30 | structure-only |
| 6235 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h4` › `h3` | 25 | 16 | 0.19 | structure-only |
| 6237 | body | MISSING | `div.row` › `div.col-md-4.col-12.paddingLR` › `—` | 19 | 16 | 0.01 | 1.00 |
| 6238 | body | MOVED | `div.col-12` › `p>b` › `p>b` | 19 | 16 | 0.02 | structure-only |
| 6239 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row` › `div.table-responsive` | 19 | 16 | 0.25 | structure-only |
| 6240 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.activity` | 19 | 16 | 0.85 | structure-only |
| 6241 | body | MISSING | `li>b` › `b` › `—` | 18 | 16 | 0.04 | 0.94 |
| 6242 | body | MISSING | `div.row` › `div.col-md-3.offset-md-0.col-6.offse` › `—` | 17 | 16 | 0.01 | 1.00 |
| 6243 | body | SUBSTITUTED | `div.col-md-8.col-12` › `img.img-fluid` › `p` | 17 | 16 | 0.24 | structure-only |
| 6244 | body | MISSING | `div` › `iframe` › `—` | 16 | 16 | 0.02 | structure-only |
| 6245 | body | MISSING | `div.col-md-8.col-12` › `div` › `—` | 16 | 16 | 0.02 | 1.00 |
| 6246 | body | SUBSTITUTED | `div.row.supervisor` › `div.row` › `div.row` | 16 | 16 | 0.02 | structure-only |
| 6247 | body | SUBSTITUTED | `div.row.flipCardsContainer` › `div.col-md-6.col-12.paddingLR` › `div.col-md-4.col-12.paddingLR` | 16 | 16 | 0.03 | structure-only |
| 6248 | body | EXTRA | `div.col-md-8.col-12` › `—` › `div.ratio.ratio-16x9` | 17 | 15 | 1.00 | structure-only |
| 6249 | body | MISSING | `div.alertActivity` › `h4` › `—` | 16 | 15 | 0.05 | 0.56 |
| 6250 | body | MOVED | `ul` › `li` › `li` | 16 | 15 | 0.09 | structure-only |
| 6251 | body | MISSING | `div.col-md-12.col-12` › `div.whakatauki` › `—` | 15 | 15 | 0.04 | 0.60 |
| 6252 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h4` › `p` | 15 | 15 | 0.19 | structure-only |
| 6253 | body | SUBSTITUTED | `div#body` › `div.row` › `div.row` | 15 | 15 | 0.94 | structure-only |
| 6256 | body | MISSING | `div#body` › `div.row.flipCardsContainer` › `—` | 19 | 14 | 0.01 | structure-only |
| 6257 | body | MISSING | `table.table.table-bordered` › `tr` › `—` | 18 | 14 | 0.01 | 0.78 |
| 6258 | body | MISSING | `div.alert` › `p` › `—` | 17 | 14 | 0.02 | 0.92 |
| 6259 | body | MOVED | `div.alert.top` › `p` › `p` | 17 | 14 | 0.03 | structure-only |
| 6260 | body | EXTRA | `div.inquiryPanel.showing` › `—` › `div.row` | 16 | 14 | 1.00 | structure-only |
| 6261 | body | EXTRA | `div.clickDropContent` › `—` › `p` | 16 | 14 | 0.97 | structure-only |
| 6262 | body | MISSING | `p` › `i` › `—` | 16 | 14 | 0.02 | 0.97 |
| 6263 | body | SUBSTITUTED | `p>span.infoTrigger` › `span.infoTrigger` › `b` | 16 | 14 | 0.15 | structure-only |
| 6264 | body | SUBSTITUTED | `div.col-md-8.col-12` › `ul` › `p` | 16 | 14 | 0.23 | structure-only |
| 6265 | body | SUBSTITUTED | `div.col-12` › `p.margB0` › `p` | 15 | 14 | 0.04 | structure-only |
| 6266 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12` › `div.col-12` | 15 | 14 | 0.98 | structure-only |
| 6267 | body | SUBSTITUTED | `div.row` › `div.col-md-4.offset-md-0.col-12` › `div.row` | 15 | 14 | 0.21 | structure-only |
| 6268 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.alert` | 15 | 14 | 0.48 | structure-only |
| 6269 | body | EXTRA | `li>b` › `—` › `b` | 14 | 14 | 0.94 | structure-only |
| 6270 | body | MISSING | `div.alert` › `ul` › `—` | 27 | 13 | 0.03 | 1.00 |
| 6271 | body | MISSING | `div.col-md-8.col-12.paddingR` › `p` › `—` | 19 | 13 | 0.04 | 0.85 |
| 6272 | body | SUBSTITUTED | `div#body` › `div.row` › `div.table-responsive` | 19 | 13 | 0.94 | structure-only |
| 6273 | body | SUBSTITUTED | `div.table-responsive` › `table.table` › `table.table.table-bordered` | 18 | 13 | 0.03 | structure-only |
| 6274 | body | MISSING | `td` › `br` › `—` | 17 | 13 | 0.01 | structure-only |
| 6275 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `a` | 17 | 13 | 0.85 | structure-only |
| 6276 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `h4` | 17 | 13 | 0.40 | structure-only |
| 6277 | body | MOVED | `div.col-md-8.col-12` › `h3` › `h3` | 16 | 13 | 0.10 | structure-only |
| 6278 | body | MOVED | `ul` › `li>b` › `li>b` | 16 | 13 | 0.02 | structure-only |
| 6279 | body | MISSING | `div.alert.top` › `div.row` › `—` | 15 | 13 | 0.07 | 0.67 |
| 6280 | body | MISSING | `div.row` › `div.col-md-3.col-12.paddingL` › `—` | 14 | 13 | 0.01 | 0.94 |
| 6281 | body | EXTRA | `ul` › `—` › `li>a` | 13 | 13 | 0.98 | structure-only |
| 6282 | body | EXTRA | `div.row.supervisor` › `—` › `div.col-md-8.col-12.paddingR` | 13 | 13 | 0.98 | structure-only |
| 6283 | body | MISSING | `div.col-md-8.col-12` › `div.col-md-12.col-12` › `—` | 13 | 13 | 0.03 | 0.92 |
| 6284 | body | MISSING | `div.col-md-4.col-12.paddingLR` › `WIDGET` › `—` | 13 | 13 | 0.03 | structure-only |
| 6285 | body | MISSING | `div.col-md-6.col-12.paddingLR` › `WIDGET` › `—` | 13 | 13 | 0.03 | structure-only |
| 6286 | body | SUBSTITUTED | `div.row` › `div.col-md-12.col-12` › `div.col-12` | 30 | 12 | 0.25 | structure-only |
| 6287 | body | MISSING | `div.alert.solid` › `div.row` › `—` | 25 | 12 | 0.07 | 0.92 |
| 6288 | body | MISSING | `div.col-md-8.col-12` › `p.quoteText` › `—` | 23 | 12 | 0.03 | 1.00 |
| 6289 | body | SUBSTITUTED | `div.table-responsive` › `table.table.table-bordered.tableFixe` › `table.table.table-bordered` | 16 | 12 | 0.01 | structure-only |
| 6290 | body | MISSING | `div.col-md-4.offset-md-0.col-1` › `img.img-fluid` › `—` | 15 | 12 | 0.10 | structure-only |
| 6291 | body | MISSING | `div.row` › `div.col` › `—` | 15 | 12 | 0.02 | 0.97 |
| 6292 | body | EXTRA | `div.ratio.ratio-16x9` › `—` › `iframe` | 14 | 12 | 1.00 | structure-only |
| 6293 | body | MISSING | `ul` › `li>b` › `—` | 14 | 12 | 0.03 | 0.69 |
| 6294 | body | SUBSTITUTED | `div.row` › `div.col-md-9.col-12` › `div.col-md-8.col-12` | 14 | 12 | 0.02 | structure-only |
| 6295 | body | SUBSTITUTED | `div.clickDropContent` › `p` › `p` | 14 | 12 | 0.08 | structure-only |
| 6296 | body | MISSING | `div.table-responsive` › `table.table.table-bordered` › `—` | 13 | 12 | 0.04 | 1.00 |
| 6297 | body | EXTRA | `div.introduction` › `—` › `div.row` | 12 | 12 | 0.99 | structure-only |
| 6298 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.icon.ratio.ratio-16` › `p>a` | 12 | 12 | 0.26 | structure-only |
| 6299 | body | SUBSTITUTED | `div.row.supervisor` › `div.col-md-8.col-12.paddingR` › `div.col-md-8.col-12` | 12 | 12 | 0.02 | structure-only |
| 6300 | body | MISSING | `div.col-md-8.col-12` › `p.captionText` › `—` | 16 | 11 | 0.02 | 0.84 |
| 6301 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.alert.solid` | 15 | 11 | 0.85 | structure-only |
| 6302 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h2` › `p` | 15 | 11 | 0.15 | structure-only |
| 6303 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `div.table-responsive` | 13 | 11 | 0.40 | structure-only |
| 6304 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.ratio.ratio-16x9` › `img.img-fluid` | 13 | 11 | 0.21 | structure-only |
| 6305 | body | SUBSTITUTED | `div#body` › `div.row` › `div.button` | 13 | 11 | 0.94 | structure-only |
| 6306 | body | EXTRA | `ol` › `—` › `li` | 12 | 11 | 0.99 | structure-only |
| 6307 | body | MISSING | `div.row` › `div.col.paddingLR` › `—` | 12 | 11 | 0.01 | 0.88 |
| 6308 | body | MISSING | `div.col-md-8.col-12` › `ol` › `—` | 12 | 11 | 0.04 | 0.53 |
| 6309 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert` › `h3` | 12 | 11 | 0.30 | structure-only |
| 6310 | body | SUBSTITUTED | `tr` › `td` › `th` | 12 | 11 | 0.12 | structure-only |
| 6311 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.videoSection.ratio.ratio-16x9` | 12 | 11 | 0.85 | structure-only |
| 6312 | body | EXTRA | `ul` › `—` › `li>b` | 11 | 11 | 0.98 | structure-only |
| 6313 | body | MISSING | `div.row` › `div.col-md-10.col-12` › `—` | 11 | 11 | 0.08 | 1.00 |
| 6314 | body | MISSING | `li>span.infoTrigger` › `span.infoTrigger` › `—` | 11 | 11 | 0.02 | 0.94 |
| 6315 | body | MISSING | `div.alert.solid.padding0` › `div.videoSection.icon.ratio.ratio-16` › `—` | 11 | 11 | 0.01 | structure-only |
| 6316 | body | MISSING | `div.col-md-8.col-12` › `p>i` › `—` | 11 | 11 | 0.07 | 0.64 |
| 6317 | body | MOVED | `div.col-md-8.col-12` › `p>i` › `p>i` | 11 | 11 | 0.02 | structure-only |
| 6318 | body | SUBSTITUTED | `div.col-md-8.col-12` › `a` › `p` | 11 | 11 | 0.07 | structure-only |
| 6319 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `div.videoSection.ratio.ratio-16x9` | 11 | 11 | 0.40 | structure-only |
| 6320 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `div.col-md-8.col-12` | 11 | 11 | 0.40 | structure-only |
| 6321 | body | SUBSTITUTED | `div.col-md-8.col-12.super-cont` › `div.row.super-content` › `div.super-content.row` | 21 | 10 | 0.02 | structure-only |
| 6322 | body | MISSING | `p` › `math` › `—` | 18 | 10 | 0.01 | 1.00 |
| 6323 | body | SUBSTITUTED | `div.row` › `div.col-12.col-md-8` › `div.col-md-8.col-12` | 18 | 10 | 0.03 | structure-only |
| 6324 | body | EXTRA | `div.col-md-6.col-12` › `—` › `p` | 17 | 10 | 1.00 | structure-only |
| 6325 | body | SUBSTITUTED | `div.alert` › `h4` › `div.row` | 16 | 10 | 0.03 | structure-only |
| 6326 | body | MISSING | `div.row` › `WIDGET` › `—` | 14 | 10 | 0.02 | structure-only |
| 6327 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.ratio.ratio-16x9` › `p` | 13 | 10 | 0.21 | structure-only |
| 6328 | body | SUBSTITUTED | `div.row` › `div.col-md-4.offset-md-0.col-12.padd` › `div.row` | 13 | 10 | 0.14 | structure-only |
| 6329 | body | MISSING | `div.clickDropContent` › `p` › `—` | 12 | 10 | 0.03 | 0.86 |
| 6330 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `h4` | 12 | 10 | 0.85 | structure-only |
| 6331 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.icon.ratio.ratio-16` › `img.img-fluid` | 12 | 10 | 0.26 | structure-only |
| 6332 | body | MISSING | `div.shapeHover` › `div.hoverContent` › `—` | 11 | 10 | 0.01 | 0.92 |
| 6333 | body | MISSING | `div.row` › `div.col-md-6.col-12.paddingL` › `—` | 11 | 10 | 0.01 | 1.00 |
| 6334 | body | MISSING | `div.col-md-8.col-12.paddingR` › `h3` › `—` | 11 | 10 | 0.04 | 1.00 |
| 6335 | body | MOVED | `ol` › `li` › `li` | 11 | 10 | 0.03 | structure-only |
| 6336 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.activity` | 11 | 10 | 0.48 | structure-only |
| 6337 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h2` › `div.activity` | 11 | 10 | 0.15 | structure-only |
| 6338 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert` › `h5` | 11 | 10 | 0.30 | structure-only |
| 6339 | body | EXTRA | `tr` › `—` › `th>b` | 10 | 10 | 1.00 | structure-only |
| 6340 | body | EXTRA | `div.fundamentalsPanel` › `—` › `WIDGET` | 10 | 10 | 0.99 | structure-only |
| 6341 | body | MISSING | `div.col-12` › `a` › `—` | 10 | 10 | 0.02 | 0.57 |
| 6342 | body | MISSING | `div.introduction` › `br` › `—` | 10 | 10 | 0.01 | structure-only |
| 6343 | body | MISSING | `div.row` › `div.col-md-4.offset-md-0.col-12.alig` › `—` | 10 | 10 | 0.01 | 1.00 |
| 6344 | body | MISSING | `div.row` › `div.col-md-6.offset-md-0.col-12` › `—` | 10 | 10 | 0.01 | 0.80 |
| 6345 | body | MISSING | `div.alert` › `h4` › `—` | 10 | 10 | 0.03 | 0.75 |
| 6346 | body | MISSING | `div.introduction` › `div.row` › `—` | 10 | 10 | 0.02 | 0.70 |
| 6347 | body | MISSING | `div.introduction.fundamentalsP` › `div.row` › `—` | 10 | 10 | 0.01 | 1.00 |
| 6348 | body | SUBSTITUTED | `div.row` › `div.col-12` › `div.col-12` | 10 | 10 | 0.55 | structure-only |
| 6349 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row` › `ul` | 10 | 10 | 0.25 | structure-only |
| 6350 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h4` › `WIDGET` | 10 | 10 | 0.19 | structure-only |
| 6351 | body | SUBSTITUTED | `div.col-md-8.col-12.paddingR` › `h2` › `h3` | 10 | 10 | 0.01 | structure-only |
| 6352 | body | SUBSTITUTED | `div.row` › `div.col-11` › `div.col-md-8.col-12` | 10 | 10 | 0.01 | structure-only |
| 6353 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert.solid` › `div.alert` | 25 | 9 | 0.07 | structure-only |
| 6354 | body | MOVED | `div.col-md-12.col-12` › `p` › `p` | 23 | 9 | 0.01 | structure-only |
| 6355 | body | SUBSTITUTED | `body.container-fluid` › `div#body.container-fluid` › `div#body` | 23 | 9 | 0.01 | structure-only |
| 6356 | body | MISSING | `div.col-md-8.col-12` › `p.quoteAck` › `—` | 19 | 9 | 0.02 | 0.92 |
| 6357 | body | MOVED | `div.col-md-8.col-12` › `p` › `p` | 13 | 9 | 0.40 | structure-only |
| 6358 | body | SUBSTITUTED | `div#body` › `div.row` › `div.row.supervisor` | 13 | 9 | 0.94 | structure-only |
| 6359 | body | EXTRA | `div.col-md-8.col-12` › `—` › `div.TKmodal` | 12 | 9 | 1.00 | structure-only |
| 6360 | body | MISSING | `td` › `p` › `—` | 12 | 9 | 0.01 | 1.00 |
| 6361 | body | SUBSTITUTED | `div.row` › `div.col-md-4.offset-md-0.col-12` › `WIDGET` | 12 | 9 | 0.21 | structure-only |
| 6362 | body | EXTRA | `div.col-md-4.col-12.paddingLR` › `—` › `WIDGET` | 11 | 9 | 0.97 | structure-only |
| 6363 | body | SUBSTITUTED | `div.row` › `div.row` › `div.col-md-8.col-12` | 11 | 9 | 0.07 | structure-only |
| 6364 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.ratio.ratio-16x9` › `div.row` | 11 | 9 | 0.21 | structure-only |
| 6365 | body | EXTRA | `p` › `—` › `span.infoTrigger` | 10 | 9 | 0.93 | structure-only |
| 6366 | body | EXTRA | `div.row` › `—` › `WIDGET` | 10 | 9 | 0.99 | structure-only |
| 6367 | body | MISSING | `div.table-responsive` › `table.table` › `—` | 10 | 9 | 0.03 | 0.90 |
| 6368 | body | MISSING | `div.col-12` › `p>b` › `—` | 10 | 9 | 0.02 | 0.67 |
| 6369 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert` › `h4` | 10 | 9 | 0.30 | structure-only |
| 6370 | body | SUBSTITUTED | `a` › `div.externalButton` › `div.button` | 10 | 9 | 0.08 | structure-only |
| 6371 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.icon.ratio.ratio-16` › `WIDGET` | 10 | 9 | 0.26 | structure-only |
| 6372 | body | SUBSTITUTED | `div.col-md-8.col-12.paddingR` › `h3` › `h4` | 10 | 9 | 0.04 | structure-only |
| 6373 | body | MISSING | `p` › `ul` › `—` | 9 | 9 | 0.01 | 0.90 |
| 6374 | body | MISSING | `div.fundamentalsPanel` › `WIDGET` › `—` | 9 | 9 | 0.00 | structure-only |
| 6375 | body | SUBSTITUTED | `div.col-md-4.offset-md-0.col-1` › `img.img-fluid` › `p` | 9 | 9 | 0.10 | structure-only |
| 6376 | body | SUBSTITUTED | `div.row` › `div.col-md-12.col-12` › `WIDGET` | 9 | 9 | 0.25 | structure-only |
| 6377 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h2` › `h5` | 9 | 9 | 0.15 | structure-only |
| 6378 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `h3` | 9 | 9 | 0.40 | structure-only |
| 6379 | body | SUBSTITUTED | `p` › `br` › `b` | 9 | 9 | 0.14 | structure-only |
| 6380 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row` › `div.col-md-8.col-12` | 9 | 9 | 0.25 | structure-only |
| 6381 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `ul` | 9 | 9 | 0.40 | structure-only |
| 6382 | body | SUBSTITUTED | `div.col-12` › `p` › `h4` | 17 | 8 | 0.26 | structure-only |
| 6383 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert.solid` › `h3` | 17 | 8 | 0.07 | structure-only |
| 6384 | body | EXTRA | `a` › `—` › `div.button.externalButton` | 12 | 8 | 0.99 | structure-only |
| 6385 | body | MISSING | `a` › `div.button.externalButton` › `—` | 12 | 8 | 0.01 | 0.24 |
| 6386 | body | SUBSTITUTED | `div#body` › `div.row` › `div.col-12` | 12 | 8 | 0.94 | structure-only |
| 6387 | body | MISSING | `p>span.highlight` › `span.highlight` › `—` | 11 | 8 | 0.01 | 1.00 |
| 6388 | body | MISSING | `div.row` › `div.col-4.paddingL` › `—` | 10 | 8 | 0.01 | 1.00 |
| 6389 | body | MISSING | `div.clickDropContent` › `h4` › `—` | 10 | 8 | 0.01 | 1.00 |
| 6390 | body | MOVED | `div.col-md-8.col-12.super-cont` › `p` › `p` | 10 | 8 | 0.01 | structure-only |
| 6391 | body | MOVED | `div.alertActivity` › `h4` › `h4>b` | 10 | 8 | 0.05 | structure-only |
| 6392 | body | MOVED | `tr` › `th` › `th` | 10 | 8 | 0.02 | structure-only |
| 6393 | body | SUBSTITUTED | `tr` › `td` › `td` | 10 | 8 | 0.12 | structure-only |
| 6394 | body | SUBSTITUTED | `div.col-md-4.col-12.paddingLR` › `WIDGET` › `WIDGET` | 10 | 8 | 0.06 | structure-only |
| 6395 | body | EXTRA | `a` › `—` › `div.buttonD` | 9 | 8 | 1.00 | structure-only |
| 6396 | body | EXTRA | `tr` › `—` › `td>b` | 9 | 8 | 0.99 | structure-only |
| 6397 | body | MISSING | `ol` › `li` › `—` | 9 | 8 | 0.01 | 0.36 |
| 6398 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h4` › `img.img-fluid` | 9 | 8 | 0.19 | structure-only |
| 6399 | body | SUBSTITUTED | `p` › `span.infoTrigger` › `b` | 9 | 8 | 0.09 | structure-only |
| 6400 | body | EXTRA | `div.row.supervisor` › `—` › `div.col-md-8.col-12.super-content-bu` | 8 | 8 | 0.93 | structure-only |
| 6401 | body | EXTRA | `h4>b` › `—` › `b` | 8 | 8 | 1.00 | structure-only |
| 6402 | body | EXTRA | `p>b` › `—` › `b>a` | 8 | 8 | 1.00 | structure-only |
| 6403 | body | EXTRA | `div.col-md-8.col-12` › `—` › `div.button` | 8 | 8 | 1.00 | structure-only |
| 6404 | body | EXTRA | `div.clickDropContent` › `—` › `p>b` | 8 | 8 | 0.99 | structure-only |
| 6405 | body | MISSING | `div.row` › `div.col-6.paddingL` › `—` | 8 | 8 | 0.01 | 1.00 |
| 6406 | body | MISSING | `div.row` › `div.col-md-8.offset-md-2.col-12` › `—` | 8 | 8 | 0.01 | 0.78 |
| 6407 | body | MISSING | `div.inquiryPanel.showing` › `div.row` › `—` | 8 | 8 | 0.01 | 0.92 |
| 6408 | body | MISSING | `div.row` › `div.col-md-9.col-12` › `—` | 8 | 8 | 0.02 | 1.00 |
| 6409 | body | MISSING | `div.row` › `div.col-md-2.col-12` › `—` | 8 | 8 | 0.01 | structure-only |
| 6410 | body | MISSING | `div.clickDropContent` › `ul` › `—` | 8 | 8 | 0.01 | 1.00 |
| 6411 | body | MOVED | `div.col-md-8.col-12.paddingR` › `h3` › `h3` | 8 | 8 | 0.01 | structure-only |
| 6412 | body | MOVED | `div.col-md-8.col-12` › `p>span.infoTrigger` › `p>span.infoTrigger` | 8 | 8 | 0.14 | structure-only |
| 6413 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.table-responsive` › `div.row` | 8 | 8 | 0.08 | structure-only |
| 6414 | body | SUBSTITUTED | `div.col-md-12.col-12` › `div.whakatauki` › `div.col-md-8.col-12` | 8 | 8 | 0.04 | structure-only |
| 6415 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h4` › `h5` | 8 | 8 | 0.19 | structure-only |
| 6416 | body | SUBSTITUTED | `div#body` › `div.col-md-8.col-12` › `div.row` | 8 | 8 | 0.02 | structure-only |
| 6417 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h2` › `WIDGET` | 8 | 8 | 0.15 | structure-only |
| 6418 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.clickDropContent` › `p` | 8 | 8 | 0.08 | structure-only |
| 6419 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `p>b` | 8 | 8 | 0.85 | structure-only |
| 6420 | body | MISSING | `div.col-12` › `WIDGET` › `—` | 14 | 7 | 0.03 | structure-only |
| 6421 | body | SUBSTITUTED | `div.col-12` › `h4` › `h3` | 11 | 7 | 0.16 | structure-only |
| 6422 | body | MISSING | `div.row` › `div.col-md-6.offset-md-3.col-12` › `—` | 9 | 7 | 0.01 | 0.89 |
| 6423 | body | MISSING | `div.col-12` › `img.img-fluid` › `—` | 9 | 7 | 0.04 | structure-only |
| 6424 | body | SUBSTITUTED | `div.col-12` › `h4` › `p` | 9 | 7 | 0.16 | structure-only |
| 6425 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row` › `p>b` | 9 | 7 | 0.25 | structure-only |
| 6426 | body | SUBSTITUTED | `div.col-md-8.col-12.paddingR` › `div.videoSection.icon.ratio.ratio-16` › `div.videoSection.ratio.ratio-16x9` | 9 | 7 | 0.02 | structure-only |
| 6427 | body | EXTRA | `div.col-md-8.col-12` › `—` › `p.captionText` | 8 | 7 | 1.00 | structure-only |
| 6428 | body | MISSING | `div.row` › `div.col-3` › `—` | 8 | 7 | 0.01 | 0.92 |
| 6429 | body | MISSING | `div.row` › `div.col-md-6.offset-md-0.col-12.padd` › `—` | 8 | 7 | 0.01 | 0.89 |
| 6430 | body | MISSING | `div.col-md-4.col-12.paddingL` › `img.img-fluid` › `—` | 8 | 7 | 0.04 | structure-only |
| 6431 | body | MOVED | `div.clickDropContent` › `p>b` › `p>b` | 8 | 7 | 0.01 | structure-only |
| 6432 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert` › `WIDGET` | 8 | 7 | 0.30 | structure-only |
| 6433 | body | SUBSTITUTED | `div.row` › `div.col-md-4.col-12.paddingL` › `div.row` | 8 | 7 | 0.06 | structure-only |
| 6434 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.icon.ratio.ratio-16` › `div.col-12` | 8 | 7 | 0.26 | structure-only |
| 6435 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `img.img-fluid` | 8 | 7 | 0.48 | structure-only |
| 6436 | body | SUBSTITUTED | `div.row.supervisor` › `div.col-md-8.col-12.super-content-bu` › `div.col-md-8.col-12` | 8 | 7 | 0.07 | structure-only |
| 6437 | body | SUBSTITUTED | `div.col-12` › `h3` › `h4` | 8 | 7 | 0.17 | structure-only |
| 6438 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h2` › `div.alert` | 8 | 7 | 0.15 | structure-only |
| 6439 | body | EXTRA | `li>i` › `—` › `i` | 7 | 7 | 1.00 | structure-only |
| 6440 | body | EXTRA | `div.col-md-8.col-12` › `—` › `div.whakatauki` | 7 | 7 | 0.94 | structure-only |
| 6441 | body | EXTRA | `div.col-12` › `—` › `p>a` | 7 | 7 | 0.96 | structure-only |
| 6442 | body | EXTRA | `body.container-fluid` › `—` › `div#body` | 7 | 7 | 0.20 | structure-only |
| 6443 | body | EXTRA | `div.col-12` › `—` › `h3` | 7 | 7 | 0.83 | structure-only |
| 6444 | body | MISSING | `div.shapeHover` › `div.outerContent` › `—` | 7 | 7 | 0.00 | 0.86 |
| 6445 | body | MISSING | `div.col-md-8.col-12` › `div.col-md-8.col-12` › `—` | 7 | 7 | 0.00 | 0.89 |
| 6446 | body | MISSING | `div.alertActivity` › `img.img-fluid` › `—` | 7 | 7 | 0.03 | structure-only |
| 6447 | body | MISSING | `a` › `div.choiceImg` › `—` | 7 | 7 | 0.01 | 0.97 |
| 6448 | body | MISSING | `a` › `div.choiceText` › `—` | 7 | 7 | 0.01 | 0.84 |
| 6449 | body | MISSING | `div.inquiryPanel` › `div.row.supervisor` › `—` | 7 | 7 | 0.00 | 1.00 |
| 6450 | body | MISSING | `li` › `b` › `—` | 7 | 7 | 0.02 | 0.84 |
| 6451 | body | MOVED | `ol` › `li>b` › `li>b` | 7 | 7 | 0.01 | structure-only |
| 6452 | body | SUBSTITUTED | `div.col-md-8.col-12` › `img.img-fluid` › `p>a` | 7 | 7 | 0.24 | structure-only |
| 6453 | body | SUBSTITUTED | `a` › `div.externalButton` › `div.row` | 7 | 7 | 0.08 | structure-only |
| 6454 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.col-md-12.col-12` › `div.row` | 7 | 7 | 0.03 | structure-only |
| 6455 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert.solid.padding0` › `p>b` | 7 | 7 | 0.01 | structure-only |
| 6456 | body | SUBSTITUTED | `div.row.flipCardsContainer` › `div.col-md-4.col-12.paddingLR` › `WIDGET` | 7 | 7 | 0.05 | structure-only |
| 6457 | body | MISSING | `div.col-md-12.col-12` › `p` › `—` | 14 | 6 | 0.01 | 0.94 |
| 6458 | body | SUBSTITUTED | `div.col-12` › `h4` › `div` | 14 | 6 | 0.16 | structure-only |
| 6459 | body | SUBSTITUTED | `div.alert` › `p.margB0` › `div.row` | 13 | 6 | 0.01 | structure-only |
| 6460 | body | SUBSTITUTED | `div.col-md-8.col-12` › `img.img-fluid` › `ul` | 11 | 6 | 0.24 | structure-only |
| 6461 | body | EXTRA | `div.col-md-8.col-12` › `—` › `div.button.TKmodalButton` | 10 | 6 | 1.00 | structure-only |
| 6462 | body | MISSING | `div.row` › `div.col-md-4.offset-md-0.col-12.padd` › `—` | 10 | 6 | 0.01 | 1.00 |
| 6463 | body | MISSING | `div.row` › `div.col-md-4.offset-md-0.col-12.padd` › `—` | 10 | 6 | 0.01 | 1.00 |
| 6464 | body | MISSING | `div.col-md-8.col-12` › `div.TKmodal` › `—` | 9 | 6 | 0.01 | 1.00 |
| 6465 | body | SUBSTITUTED | `div.row` › `div.col-md-4.offset-md-0.col-12.padd` › `div.col-md-8.col-12` | 9 | 6 | 0.14 | structure-only |
| 6466 | body | MISSING | `div.row.supervisor` › `div.col-md-4.offset-md-0.col-12` › `—` | 8 | 6 | 0.01 | 1.00 |
| 6467 | body | MISSING | `div.row` › `div.col.paddingL` › `—` | 8 | 6 | 0.01 | 0.92 |
| 6468 | body | MISSING | `math` › `mi` › `—` | 8 | 6 | 0.00 | 0.93 |
| 6469 | body | MOVED | `div.alert` › `h4` › `h4` | 8 | 6 | 0.03 | structure-only |
| 6470 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h5` › `p` | 8 | 6 | 0.05 | structure-only |
| 6471 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `WIDGET` | 8 | 6 | 0.48 | structure-only |
| 6472 | body | EXTRA | `td` › `—` › `b` | 7 | 6 | 1.00 | structure-only |
| 6473 | body | EXTRA | `div.col-12` › `—` › `h4` | 7 | 6 | 0.84 | structure-only |
| 6474 | body | MISSING | `div.col-12` › `p.margB0` › `—` | 7 | 6 | 0.04 | 1.00 |
| 6475 | body | MISSING | `div.col-md-6.offset-md-0.col-1` › `img.img-fluid` › `—` | 7 | 6 | 0.01 | structure-only |
| 6476 | body | MISSING | `div.row` › `div.col-md-2.offset-md-0.col-12` › `—` | 7 | 6 | 0.00 | 1.00 |
| 6477 | body | MISSING | `div.alertActivity` › `p` › `—` | 7 | 6 | 0.03 | 0.55 |
| 6478 | body | MISSING | `div.col` › `WIDGET` › `—` | 7 | 6 | 0.01 | structure-only |
| 6479 | body | MISSING | `div.row` › `div.col.paddingR` › `—` | 7 | 6 | 0.00 | 0.88 |
| 6480 | body | MISSING | `div.col-md-8.col-12.paddingR` › `ul` › `—` | 7 | 6 | 0.01 | 0.67 |
| 6481 | body | MISSING | `div.col-md-4.offset-md-0.col-1` › `div.alertImage` › `—` | 7 | 6 | 0.09 | structure-only |
| 6482 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert` › `a` | 7 | 6 | 0.30 | structure-only |
| 6483 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.row` | 7 | 6 | 0.85 | structure-only |
| 6484 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12.paddingLR` › `div.col-md-8.col-12` | 7 | 6 | 0.01 | structure-only |
| 6485 | body | SUBSTITUTED | `div.table-responsive` › `table.table.tableFixed` › `table.table.table-bordered` | 7 | 6 | 0.01 | structure-only |
| 6486 | body | SUBSTITUTED | `table.table` › `tr.rowSolid` › `tr` | 7 | 6 | 0.01 | structure-only |
| 6487 | body | SUBSTITUTED | `div#body` › `div.row` › `div.videoSection.ratio.ratio-16x9` | 7 | 6 | 0.94 | structure-only |
| 6488 | body | EXTRA | `div.col-12` › `—` › `ol` | 6 | 6 | 0.99 | structure-only |
| 6489 | body | EXTRA | `div.col-md-6.col-12` › `—` › `p>a` | 6 | 6 | 1.00 | structure-only |
| 6490 | body | EXTRA | `li` › `—` › `b` | 6 | 6 | 0.99 | structure-only |
| 6491 | body | EXTRA | `div.TKmodal` › `—` › `p` | 6 | 6 | 1.00 | structure-only |
| 6492 | body | MISSING | `div.row` › `div.col-md-6.col-12.paddingR` › `—` | 6 | 6 | 0.01 | 1.00 |
| 6493 | body | MISSING | `table.table` › `tr` › `—` | 6 | 6 | 0.02 | 1.00 |
| 6494 | body | MISSING | `div.inquiryPanel` › `WIDGET` › `—` | 6 | 6 | 0.00 | structure-only |
| 6495 | body | MISSING | `div.row` › `div.row.supervisor` › `—` | 6 | 6 | 0.01 | 0.83 |
| 6496 | body | MISSING | `div.col-md-2.col-12` › `img.img-fluid` › `—` | 6 | 6 | 0.01 | structure-only |
| 6497 | body | MISSING | `tr` › `th` › `—` | 6 | 6 | 0.01 | 1.00 |
| 6498 | body | MISSING | `table.table.table-bordered.tab` › `tr` › `—` | 6 | 6 | 0.01 | 0.88 |
| 6499 | body | MISSING | `div.col-12` › `div.row` › `—` | 6 | 6 | 0.01 | 1.00 |
| 6500 | body | MISSING | `div.row.selectionBox` › `div.col-md-12.col-12` › `—` | 6 | 6 | 0.01 | 0.83 |
| 6501 | body | MISSING | `div.col-12` › `br` › `—` | 6 | 6 | 0.01 | structure-only |
| 6502 | body | MISSING | `div.alert.top` › `p` › `—` | 6 | 6 | 0.01 | 0.67 |
| 6503 | body | MISSING | `div.row` › `div.col-6.paddingR` › `—` | 6 | 6 | 0.00 | 1.00 |
| 6504 | body | MISSING | `div.alert` › `p.margB0` › `—` | 6 | 6 | 0.01 | 0.83 |
| 6505 | body | MISSING | `b>i` › `i` › `—` | 6 | 6 | 0.01 | 0.88 |
| 6506 | body | MISSING | `div.col-md-4.col-12.paddingLR` › `img.img-fluid` › `—` | 6 | 6 | 0.01 | structure-only |
| 6507 | body | MISSING | `div.phaseLink` › `img.phaseImg` › `—` | 6 | 6 | 0.01 | structure-only |
| 6508 | body | MOVED | `div.alert.solid` › `p` › `p` | 6 | 6 | 0.00 | structure-only |
| 6509 | body | SUBSTITUTED | `ul` › `li` › `table.table.table-bordered` | 6 | 6 | 0.35 | structure-only |
| 6510 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.icon.ratio.ratio-16` › `ul` | 6 | 6 | 0.26 | structure-only |
| 6511 | body | SUBSTITUTED | `div.videoSection.icon.ratio.ra` › `iframe.embed-responsive-item` › `li` | 6 | 6 | 0.21 | structure-only |
| 6512 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row` › `p>a` | 6 | 6 | 0.25 | structure-only |
| 6513 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.col-md-12.col-12` › `h3` | 6 | 6 | 0.03 | structure-only |
| 6514 | body | SUBSTITUTED | `p` › `br` › `i` | 6 | 6 | 0.14 | structure-only |
| 6515 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row` › `h3` | 6 | 6 | 0.25 | structure-only |
| 6516 | body | SUBSTITUTED | `div.col-12` › `p` › `WIDGET` | 6 | 6 | 0.26 | structure-only |
| 6517 | body | SUBSTITUTED | `div.alertActivity` › `p` › `p` | 6 | 6 | 0.10 | structure-only |
| 6518 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `h5` | 6 | 6 | 0.85 | structure-only |
| 6519 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert.solid.padding0` › `div.col-md-8.col-12` | 6 | 6 | 0.01 | structure-only |
| 6520 | body | SUBSTITUTED | `div.row.supervisor` › `div.col-md-12.col-12` › `div.col-md-8.col-12` | 6 | 6 | 0.01 | structure-only |
| 6521 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12` › `div#footer` | 6 | 6 | 0.98 | structure-only |
| 6522 | body | SUBSTITUTED | `div.row` › `div.row` › `div.col-12` | 6 | 6 | 0.07 | structure-only |
| 6523 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12` › `div.videoSection.ratio.ratio-16x9` | 6 | 6 | 0.98 | structure-only |
| 6524 | body | SUBSTITUTED | `div.super-content` › `div.row` › `div.row` | 6 | 6 | 0.01 | structure-only |
| 6525 | body | SUBSTITUTED | `div.col-12` › `h3` › `h3` | 6 | 6 | 0.17 | structure-only |
| 6526 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.ratio.ratio-16x9` › `audio.audioPlayer.icon` | 6 | 6 | 0.21 | structure-only |
| 6527 | body | SUBSTITUTED | `div.col-md-4.offset-md-0.col-1` › `div.alertActivity` › `div.col-md-8.col-12` | 6 | 6 | 0.09 | structure-only |
| 6528 | body | SUBSTITUTED | `div.col-md-8.col-12` › `ul` › `WIDGET` | 6 | 6 | 0.23 | structure-only |
| 6529 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12.paddingR` › `div.col-md-6.col-12` | 6 | 6 | 0.14 | structure-only |
| 6530 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.table-responsive` › `p` | 6 | 6 | 0.08 | structure-only |
| 6531 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12.alertPadding` › `div.col-md-8.col-12` | 6 | 6 | 0.00 | structure-only |
| 6532 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.ratio.ratio-16x9` › `WIDGET` | 6 | 6 | 0.21 | structure-only |
| 6533 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h5` › `h4` | 6 | 6 | 0.05 | structure-only |
| 6534 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `ul` | 6 | 6 | 0.48 | structure-only |
| 6535 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.whakatauki` › `h3` | 6 | 6 | 0.06 | structure-only |
| 6536 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.ratio.ratio-16x9` › `h4` | 6 | 6 | 0.21 | structure-only |
| 6537 | body | SUBSTITUTED | `div.introduction.fundamentalsP` › `div.row.phaseContainer.justify-conte` › `div.row.phaseContainer` | 6 | 6 | 0.00 | structure-only |
| 6538 | body | SUBSTITUTED | `p` › `math` › `b` | 6 | 6 | 0.02 | structure-only |
| 6539 | body | MISSING | `div.row` › `div.col-12.col-md-8` › `—` | 14 | 5 | 0.01 | 1.00 |
| 6540 | body | EXTRA | `div.col-md-8.col-12` › `—` › `div.alert.top` | 10 | 5 | 1.00 | structure-only |
| 6541 | body | MISSING | `div.row` › `div.col-8` › `—` | 9 | 5 | 0.04 | 1.00 |
| 6542 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h2` › `div.alert.top` | 9 | 5 | 0.15 | structure-only |
| 6543 | body | SUBSTITUTED | `p` › `br` › `iframe` | 9 | 5 | 0.14 | structure-only |
| 6544 | body | SUBSTITUTED | `div#body` › `div.row.flipCardsContainer` › `div.row.flipCardsContainer` | 9 | 5 | 0.01 | structure-only |
| 6545 | body | EXTRA | `div.alert.top` › `—` › `div.row` | 8 | 5 | 0.93 | structure-only |
| 6546 | body | MISSING | `div.col-md-8.col-12` › `audio.audioPlayer.icon` › `—` | 8 | 5 | 0.01 | structure-only |
| 6547 | body | MISSING | `p` › `u` › `—` | 8 | 5 | 0.01 | 0.96 |
| 6548 | body | MISSING | `div.alert.cultural[layout=comb` › `div.row` › `—` | 8 | 5 | 0.01 | 1.00 |
| 6549 | body | SUBSTITUTED | `div.row` › `WIDGET` › `div.col-md-8.col-12` | 8 | 5 | 0.02 | structure-only |
| 6550 | body | SUBSTITUTED | `div.row` › `div.col-md-12.col-12` › `div.row` | 8 | 5 | 0.25 | structure-only |
| 6551 | body | SUBSTITUTED | `div.col-md-8.col-12` › `br` › `WIDGET` | 8 | 5 | 0.05 | structure-only |
| 6552 | body | MISSING | `div.col-md-8.col-12` › `div.alert.solid` › `—` | 7 | 5 | 0.07 | 0.89 |
| 6553 | body | MISSING | `div.col-md-8.col-12.paddingR` › `div.videoSection.icon.ratio.ratio-16` › `—` | 7 | 5 | 0.02 | structure-only |
| 6554 | body | MISSING | `div.col-md-8.col-12.paddingR` › `img.img-fluid` › `—` | 7 | 5 | 0.01 | structure-only |
| 6555 | body | MOVED | `div.col-12` › `p` › `p` | 7 | 5 | 0.04 | structure-only |
| 6556 | body | MOVED | `div.col-md-8.col-12` › `p>b` › `p>b` | 7 | 5 | 0.03 | structure-only |
| 6557 | body | SUBSTITUTED | `div.table-responsive` › `table.table.tableFixed.table-bordere` › `table.table.table-bordered` | 7 | 5 | 0.01 | structure-only |
| 6558 | body | SUBSTITUTED | `p` › `br` › `table.table.table-bordered` | 7 | 5 | 0.14 | structure-only |
| 6559 | body | SUBSTITUTED | `div.clickDropContent` › `p` › `div.clickDropContent` | 7 | 5 | 0.08 | structure-only |
| 6560 | body | EXTRA | `tr` › `—` › `td>a` | 6 | 5 | 1.00 | structure-only |
| 6561 | body | EXTRA | `div.col-12` › `—` › `h4>b` | 6 | 5 | 1.00 | structure-only |
| 6562 | body | MISSING | `div.row` › `div.col-md-4.col-12.paddingR` › `—` | 6 | 5 | 0.01 | 1.00 |
| 6563 | body | MISSING | `i` › `br` › `—` | 6 | 5 | 0.00 | structure-only |
| 6564 | body | MISSING | `div.col-12` › `p.quoteAck` › `—` | 6 | 5 | 0.01 | 0.83 |
| 6565 | body | MISSING | `div.shapeHover[layout=clockwis` › `div.hoverContent` › `—` | 6 | 5 | 0.01 | 1.00 |
| 6566 | body | MOVED | `tr.rowSolid` › `th` › `th` | 6 | 5 | 0.01 | structure-only |
| 6567 | body | MOVED | `div.col-md-12.col-12` › `h3` › `h3` | 6 | 5 | 0.01 | structure-only |
| 6568 | body | MOVED | `td` › `p` › `p` | 6 | 5 | 0.01 | structure-only |
| 6569 | body | MOVED | `div.row` › `p` › `p` | 6 | 5 | 0.00 | structure-only |
| 6570 | body | SUBSTITUTED | `div.col-md-8.col-12` › `ul` › `ol` | 6 | 5 | 0.23 | structure-only |
| 6571 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.table-responsive` › `WIDGET` | 6 | 5 | 0.08 | structure-only |
| 6572 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `p>a` | 6 | 5 | 0.40 | structure-only |
| 6573 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h2` › `img.img-fluid` | 6 | 5 | 0.15 | structure-only |
| 6574 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `a` | 6 | 5 | 0.48 | structure-only |
| 6575 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `audio.audioPlayer.icon` | 6 | 5 | 0.40 | structure-only |
| 6576 | body | SUBSTITUTED | `div.row.supervisor` › `div.col-12` › `div.col-md-8.col-12` | 6 | 5 | 0.00 | structure-only |
| 6577 | body | SUBSTITUTED | `div.col-12` › `ul.marg0` › `ul` | 6 | 5 | 0.00 | structure-only |
| 6578 | body | SUBSTITUTED | `div.col-12` › `ul` › `p` | 6 | 5 | 0.12 | structure-only |
| 6579 | body | SUBSTITUTED | `ol` › `li` › `li` | 6 | 5 | 0.06 | structure-only |
| 6580 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.clickDropContent` › `WIDGET` | 6 | 5 | 0.08 | structure-only |
| 6581 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `a` | 6 | 5 | 0.40 | structure-only |
| 6582 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p.quoteAck` › `p` | 6 | 5 | 0.02 | structure-only |
| 6583 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p.quoteAck` › `p>i` | 6 | 5 | 0.02 | structure-only |
| 6584 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h4` › `p>b` | 6 | 5 | 0.19 | structure-only |
| 6585 | body | SUBSTITUTED | `td` › `img.img-fluid` › `b` | 6 | 5 | 0.04 | structure-only |
| 6586 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.clickDropContent` › `div.clickDropContent` | 6 | 5 | 0.08 | structure-only |
| 6587 | body | EXTRA | `div.col-md-8.col-12.super-cont` › `—` › `div.super-content.row` | 5 | 5 | 1.00 | structure-only |
| 6588 | body | EXTRA | `div.col-md-4.col-12` › `—` › `div.alert.top` | 5 | 5 | 0.99 | structure-only |
| 6589 | body | EXTRA | `div.col-12` › `—` › `div` | 5 | 5 | 1.00 | structure-only |
| 6590 | body | EXTRA | `td>i` › `—` › `i` | 5 | 5 | 1.00 | structure-only |
| 6591 | body | EXTRA | `td>b` › `—` › `b` | 5 | 5 | 0.99 | structure-only |
| 6592 | body | EXTRA | `div.clickDropContent` › `—` › `ul` | 5 | 5 | 0.98 | structure-only |
| 6593 | body | EXTRA | `div.whakatauki` › `—` › `p` | 5 | 5 | 0.91 | structure-only |
| 6594 | body | EXTRA | `div.col-md-8.col-12` › `—` › `h5>i` | 5 | 5 | 1.00 | structure-only |
| 6595 | body | EXTRA | `div.alert.top` › `—` › `p` | 5 | 5 | 1.00 | structure-only |
| 6596 | body | EXTRA | `div.clickDropContent` › `—` › `img.img-fluid` | 5 | 5 | 1.00 | structure-only |
| 6597 | body | MISSING | `td>b` › `b` › `—` | 5 | 5 | 0.01 | 1.00 |
| 6598 | body | MISSING | `p>a` › `a` › `—` | 5 | 5 | 0.06 | 0.86 |
| 6599 | body | MISSING | `div.alertActivity` › `a` › `—` | 5 | 5 | 0.01 | 0.33 |
| 6600 | body | MISSING | `div.row` › `div.col-md-11.col-12` › `—` | 5 | 5 | 0.01 | 1.00 |
| 6601 | body | MISSING | `div.row` › `div.col-md-3.offset-md-0.col-12.padd` › `—` | 5 | 5 | 0.00 | 1.00 |
| 6602 | body | MISSING | `div.col-md-8.col-12` › `div.alert.solid.padding0` › `—` | 5 | 5 | 0.01 | structure-only |
| 6603 | body | MISSING | `div.row` › `div.col-md-10.col-12.paddingL` › `—` | 5 | 5 | 0.01 | 1.00 |
| 6604 | body | MISSING | `p>strong` › `strong` › `—` | 5 | 5 | 0.00 | 1.00 |
| 6605 | body | MISSING | `div.col-md-8.col-12.paddingR` › `div.alert` › `—` | 5 | 5 | 0.01 | 0.83 |
| 6606 | body | MISSING | `ul` › `li>span.infoTrigger` › `—` | 5 | 5 | 0.02 | 1.00 |
| 6607 | body | MISSING | `div.col-md-8.col-12` › `div.row.selectionBox` › `—` | 5 | 5 | 0.01 | 0.80 |
| 6608 | body | MISSING | `body.inquiry.container-fluid` › `div#body` › `—` | 5 | 5 | 0.03 | 1.00 |
| 6609 | body | MISSING | `div.col-md-3.offset-md-0.col-1` › `img.img-fluid` › `—` | 5 | 5 | 0.02 | structure-only |
| 6610 | body | MISSING | `div.col-md-8.col-12.paddingR` › `h2` › `—` | 5 | 5 | 0.01 | 0.80 |
| 6611 | body | MISSING | `div.row` › `div.col-md-8.col-12.choicePage.choic` › `—` | 5 | 5 | 0.02 | structure-only |
| 6612 | body | MISSING | `div.col-md-8.col-12.paddingR` › `WIDGET` › `—` | 5 | 5 | 0.01 | structure-only |
| 6613 | body | MISSING | `div.outerContent` › `div.shape` › `—` | 5 | 5 | 0.00 | 1.00 |
| 6614 | body | MISSING | `math` › `mfrac` › `—` | 5 | 5 | 0.02 | 1.00 |
| 6615 | body | MISSING | `div.row.flipCardsContainer` › `div.col-md-3.col-12.paddingLR` › `—` | 5 | 5 | 0.01 | structure-only |
| 6616 | body | MOVED | `div.alertActivity` › `p` › `p` | 5 | 5 | 0.03 | structure-only |
| 6617 | body | MOVED | `div` › `p` › `p` | 5 | 5 | 0.01 | structure-only |
| 6618 | body | SUBSTITUTED | `div.col-md-8.col-12` › `ul` › `img.img-fluid` | 5 | 5 | 0.23 | structure-only |
| 6619 | body | SUBSTITUTED | `div.col-md-4.offset-md-0.col-1` › `div.alert.top` › `p` | 5 | 5 | 0.04 | structure-only |
| 6620 | body | SUBSTITUTED | `ul` › `li` › `div.col-12` | 5 | 5 | 0.35 | structure-only |
| 6621 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row` › `div.col-12` | 5 | 5 | 0.25 | structure-only |
| 6622 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.alert.solid` | 5 | 5 | 0.48 | structure-only |
| 6623 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert` › `ul` | 5 | 5 | 0.30 | structure-only |
| 6624 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.icon.ratio.ratio-16` › `div.alert` | 5 | 5 | 0.26 | structure-only |
| 6625 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `div.activity` | 5 | 5 | 0.40 | structure-only |
| 6626 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row.flipCardsContainer` › `p` | 5 | 5 | 0.07 | structure-only |
| 6627 | body | SUBSTITUTED | `div.row.flipCardsContainer` › `div.col-md-4.col-12.paddingLR` › `div.row` | 5 | 5 | 0.05 | structure-only |
| 6628 | body | SUBSTITUTED | `div.alert` › `div.row` › `div.col-md-8.col-12` | 5 | 5 | 0.27 | structure-only |
| 6629 | body | SUBSTITUTED | `div.row` › `div.col-md-3.offset-md-0.col-12` › `div.row` | 5 | 5 | 0.04 | structure-only |
| 6630 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row` › `h4` | 5 | 5 | 0.25 | structure-only |
| 6631 | body | SUBSTITUTED | `div.row.supervisor` › `div.col-md-8.col-12.paddingL.super-c` › `div.col-md-8.col-12.super-content-bu` | 5 | 5 | 0.00 | structure-only |
| 6632 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div` › `p>a` | 5 | 5 | 0.02 | structure-only |
| 6633 | body | SUBSTITUTED | `div.col-md-8.col-12.paddingR` › `h2` › `h4` | 5 | 5 | 0.01 | structure-only |
| 6634 | body | SUBSTITUTED | `div.row` › `div.col-8.col-12` › `div.col-md-8.col-12` | 5 | 5 | 0.00 | structure-only |
| 6635 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12.paddingR` › `div.row` | 5 | 5 | 0.14 | structure-only |
| 6636 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row.supervisor` › `div.row.supervisor` | 5 | 5 | 0.01 | structure-only |
| 6637 | body | SUBSTITUTED | `div.row.supervisor` › `div.col-12.super-content-button` › `div.col-md-8.col-12.super-content-bu` | 5 | 5 | 0.00 | structure-only |
| 6638 | body | SUBSTITUTED | `div.col-12.super-content-butto` › `div.super-content` › `div.super-content.row` | 5 | 5 | 0.00 | structure-only |
| 6639 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.button.TKmodalButton` › `a` | 5 | 5 | 0.01 | structure-only |
| 6640 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.TKmodal` › `div.button` | 5 | 5 | 0.01 | structure-only |
| 6641 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row.flipCardsContainer` › `WIDGET` | 5 | 5 | 0.07 | structure-only |
| 6642 | body | SUBSTITUTED | `div.row` › `div.col-md-3.offset-md-0.col-12.padd` › `div.row` | 5 | 5 | 0.02 | structure-only |
| 6643 | body | SUBSTITUTED | `div.row` › `div.col-md-4.col-12` › `div.row` | 5 | 5 | 0.05 | structure-only |
| 6644 | body | SUBSTITUTED | `div.row` › `div.row` › `WIDGET` | 5 | 5 | 0.07 | structure-only |
| 6645 | body | SUBSTITUTED | `div.row.flipCardsContainer` › `div.col-md-6.col-12.paddingLR` › `WIDGET` | 5 | 5 | 0.03 | structure-only |
| 6646 | body | SUBSTITUTED | `div.row` › `div.col-md-4.col-12` › `WIDGET` | 5 | 5 | 0.05 | structure-only |
| 6647 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.icon.ratio.ratio-16` › `h4` | 5 | 5 | 0.26 | structure-only |
| 6648 | body | SUBSTITUTED | `div.row` › `div.col-md-4.col-12.paddingLR` › `WIDGET` | 5 | 5 | 0.02 | structure-only |
| 6649 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12` › `div.button` | 5 | 5 | 0.98 | structure-only |
| 6650 | body | SUBSTITUTED | `ul` › `li` › `ul` | 5 | 5 | 0.35 | structure-only |
| 6651 | body | SUBSTITUTED | `div.col-12` › `p.margB0` › `h3` | 16 | 4 | 0.04 | structure-only |
| 6652 | body | MISSING | `div.row` › `div.col-md-2.col-12.paddingL` › `—` | 13 | 4 | 0.01 | 1.00 |
| 6653 | body | MISSING | `div.col-md-12.col-12` › `ul` › `—` | 13 | 4 | 0.01 | 1.00 |
| 6654 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert.cultural[layout=combined]` › `div.wananga` | 10 | 4 | 0.02 | structure-only |
| 6655 | body | SUBSTITUTED | `div.row` › `div.col-12` › `div.col-md-6.col-12` | 10 | 4 | 0.55 | structure-only |
| 6656 | body | MISSING | `div.row` › `div.col-md-8.col-12.offset-md-2` › `—` | 9 | 4 | 0.01 | structure-only |
| 6657 | body | EXTRA | `div.col-md-8.col-12` › `—` › `div.button.audioButton` | 6 | 4 | 1.00 | structure-only |
| 6658 | body | EXTRA | `div.col-md-8.col-12` › `—` › `div.quoteText` | 6 | 4 | 1.00 | structure-only |
| 6659 | body | MISSING | `div#body.container-fluid` › `div.row` › `—` | 6 | 4 | 0.01 | 1.00 |
| 6660 | body | MISSING | `div.row` › `div.col-md-8.col-12.paddingL` › `—` | 6 | 4 | 0.01 | 1.00 |
| 6661 | body | MISSING | `div.col-md-8.offset-md-2.col-1` › `img.img-fluid` › `—` | 6 | 4 | 0.01 | structure-only |
| 6662 | body | MISSING | `div.row` › `div.col-3.paddingL` › `—` | 6 | 4 | 0.01 | structure-only |
| 6663 | body | SUBSTITUTED | `div#body` › `WIDGET` › `div.row` | 6 | 4 | 0.06 | structure-only |
| 6664 | body | SUBSTITUTED | `div.row.flipCardsContainer` › `div.col-md-3.col-12.paddingLR` › `div.col-md-4.col-12.paddingLR` | 6 | 4 | 0.01 | structure-only |
| 6665 | body | SUBSTITUTED | `div.col-md-8.col-12` › `br` › `p` | 6 | 4 | 0.05 | structure-only |
| 6666 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row` › `audio.audioPlayer.icon` | 6 | 4 | 0.25 | structure-only |
| 6667 | body | SUBSTITUTED | `div.col-md-4.offset-md-0.col-1` › `WIDGET` › `WIDGET` | 6 | 4 | 0.01 | structure-only |
| 6668 | body | EXTRA | `td` › `—` › `i` | 5 | 4 | 1.00 | structure-only |
| 6669 | body | MISSING | `div.captionTrigger` › `div.caption` › `—` | 5 | 4 | 0.00 | 0.88 |
| 6670 | body | MISSING | `div.col-md-8.col-12` › `p.quoteAck>i` › `—` | 5 | 4 | 0.00 | 0.80 |
| 6671 | body | MISSING | `div.col-12` › `h5` › `—` | 5 | 4 | 0.01 | 1.00 |
| 6672 | body | MISSING | `th` › `img.img-fluid` › `—` | 5 | 4 | 0.00 | structure-only |
| 6673 | body | MISSING | `td` › `div.row` › `—` | 5 | 4 | 0.00 | structure-only |
| 6674 | body | MISSING | `div.col-md-8.col-12` › `h4.center-text` › `—` | 5 | 4 | 0.00 | 0.86 |
| 6675 | body | MISSING | `tr.rowSolid` › `th` › `—` | 5 | 4 | 0.01 | 0.57 |
| 6676 | body | MISSING | `div.table-responsive` › `table.table.tableFixed` › `—` | 5 | 4 | 0.01 | 0.60 |
| 6677 | body | MISSING | `div.col-md-8.col-12.super-cont` › `p` › `—` | 5 | 4 | 0.01 | 0.50 |
| 6678 | body | MISSING | `div.shapeHover[layout=clockwis` › `div.outerContent` › `—` | 5 | 4 | 0.01 | 1.00 |
| 6679 | body | MISSING | `li>a` › `a` › `—` | 5 | 4 | 0.01 | 1.00 |
| 6680 | body | MOVED | `div.col-md-8.col-12` › `h5` › `h5` | 5 | 4 | 0.01 | structure-only |
| 6681 | body | SUBSTITUTED | `div.row` › `div.col-12` › `tr` | 5 | 4 | 0.55 | structure-only |
| 6682 | body | SUBSTITUTED | `div.col-md-4.offset-md-0.col-1` › `div.alert.top` › `div.col-md-8.col-12` | 5 | 4 | 0.04 | structure-only |
| 6683 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.icon.ratio.ratio-16` › `div.col-md-8.col-12` | 5 | 4 | 0.26 | structure-only |
| 6684 | body | SUBSTITUTED | `div#body` › `div.row` › `div.row.flipCardsContainer` | 5 | 4 | 0.94 | structure-only |
| 6685 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.icon.ratio.ratio-16` › `a` | 5 | 4 | 0.26 | structure-only |
| 6686 | body | SUBSTITUTED | `div.col-md-8.col-12.choicePage` › `WIDGET` › `p` | 5 | 4 | 0.03 | structure-only |
| 6687 | body | SUBSTITUTED | `div.col-md-8.col-12.paddingR` › `div.videoSection.icon.ratio.ratio-16` › `p` | 5 | 4 | 0.02 | structure-only |
| 6688 | body | SUBSTITUTED | `div.col-md-4.offset-md-0.col-1` › `div.alertImage` › `div.col-md-8.col-12` | 5 | 4 | 0.09 | structure-only |
| 6689 | body | SUBSTITUTED | `ul` › `li>a` › `li` | 5 | 4 | 0.01 | structure-only |
| 6690 | body | EXTRA | `div.col-md-8.col-12` › `—` › `textarea.form-control` | 4 | 4 | 1.00 | structure-only |
| 6691 | body | EXTRA | `div.col-md-4.offset-md-0.col-1` › `—` › `div.alertActivity` | 4 | 4 | 0.99 | structure-only |
| 6692 | body | EXTRA | `div.col-md-6.col-12` › `—` › `p>b` | 4 | 4 | 1.00 | structure-only |
| 6693 | body | EXTRA | `li` › `—` › `i` | 4 | 4 | 1.00 | structure-only |
| 6694 | body | EXTRA | `div.col-12` › `—` › `p>b` | 4 | 4 | 0.99 | structure-only |
| 6695 | body | EXTRA | `div.introduction.fundamentalsP` › `—` › `div.row.phaseContainer` | 4 | 4 | 1.00 | structure-only |
| 6696 | body | EXTRA | `mfrac` › `—` › `mrow` | 4 | 4 | 1.00 | structure-only |
| 6697 | body | EXTRA | `div.col-12` › `—` › `a` | 4 | 4 | 0.99 | structure-only |
| 6698 | body | EXTRA | `li>a` › `—` › `a` | 4 | 4 | 0.98 | structure-only |
| 6699 | body | MISSING | `b` › `br` › `—` | 4 | 4 | 0.00 | structure-only |
| 6700 | body | MISSING | `div.row` › `div.col-8.offset-2` › `—` | 4 | 4 | 0.01 | structure-only |
| 6701 | body | MISSING | `p` › `img.img-fluid` › `—` | 4 | 4 | 0.00 | structure-only |
| 6702 | body | MISSING | `div.col-md-12.col-12` › `h3` › `—` | 4 | 4 | 0.01 | 1.00 |
| 6703 | body | MISSING | `div.col-8.offset-2` › `img.img-fluid` › `—` | 4 | 4 | 0.01 | structure-only |
| 6704 | body | MISSING | `div.col-md-8.col-12` › `p.quoteAck>a` › `—` | 4 | 4 | 0.00 | 0.75 |
| 6705 | body | MISSING | `div.alert.solid.padding0` › `div` › `—` | 4 | 4 | 0.00 | structure-only |
| 6706 | body | MISSING | `div.col-md-2.col-12.paddingR` › `img.img-fluid` › `—` | 4 | 4 | 0.01 | structure-only |
| 6707 | body | MISSING | `div#body` › `div.inquiryPanel.showing` › `—` | 4 | 4 | 0.02 | 1.00 |
| 6708 | body | MISSING | `div.col-md-8.col-12.super-cont` › `h3` › `—` | 4 | 4 | 0.01 | 1.00 |
| 6709 | body | MISSING | `div.row` › `div.col-md-6.col-12.paddingLR` › `—` | 4 | 4 | 0.00 | 1.00 |
| 6710 | body | MISSING | `div.row` › `div.col-md-8.col-12.paddingLR` › `—` | 4 | 4 | 0.01 | 1.00 |
| 6711 | body | MISSING | `div.videoSection.youtubeShort.` › `iframe` › `—` | 4 | 4 | 0.01 | structure-only |
| 6712 | body | MISSING | `div.fundamentalsPanel` › `div.row.flipCardsContainer` › `—` | 4 | 4 | 0.00 | structure-only |
| 6713 | body | MISSING | `p` › `a` › `—` | 4 | 4 | 0.01 | 0.50 |
| 6714 | body | MISSING | `div.fundamentalsPanel` › `div.row.supervisor` › `—` | 4 | 4 | 0.00 | 1.00 |
| 6715 | body | MISSING | `div.alert` › `img.img-fluid` › `—` | 4 | 4 | 0.00 | structure-only |
| 6716 | body | MISSING | `div.row` › `div.col-md-4` › `—` | 4 | 4 | 0.00 | 0.83 |
| 6717 | body | MISSING | `div.col-md-8.col-12.paddingR` › `div.videoSection.ratio.ratio-16x9` › `—` | 4 | 4 | 0.01 | structure-only |
| 6718 | body | MISSING | `div.col-md-4.offset-md-0.col-1` › `div.alertActivity` › `—` | 4 | 4 | 0.01 | 0.75 |
| 6719 | body | MISSING | `div.phaseLink` › `h3` › `—` | 4 | 4 | 0.01 | 0.91 |
| 6720 | body | MISSING | `div.row` › `div.col-md-3.col-12.paddingLR` › `—` | 4 | 4 | 0.00 | 1.00 |
| 6721 | body | MISSING | `div.row.phaseContainer` › `div.col-md-3.col-6` › `—` | 4 | 4 | 0.02 | 1.00 |
| 6722 | body | MISSING | `li` › `math` › `—` | 4 | 4 | 0.00 | 1.00 |
| 6723 | body | MISSING | `div.row.flipCardsContainer` › `div.col-md-6.col-6.paddingLR` › `—` | 4 | 4 | 0.00 | structure-only |
| 6724 | body | MOVED | `div.col-md-8.col-12` › `p>i` › `p>i` | 4 | 4 | 0.02 | structure-only |
| 6725 | body | MOVED | `div.col-12` › `p` › `p` | 4 | 4 | 0.08 | structure-only |
| 6726 | body | MOVED | `a` › `div.externalButton` › `div.externalButton` | 4 | 4 | 0.08 | structure-only |
| 6727 | body | MOVED | `div.col-md-6.offset-md-0.col-1` › `p` › `p` | 4 | 4 | 0.00 | structure-only |
| 6728 | body | MOVED | `div.phaseLink` › `h3` › `h3` | 4 | 4 | 0.01 | structure-only |
| 6729 | body | MOVED | `div.col-12` › `h3` › `h3` | 4 | 4 | 0.17 | structure-only |
| 6730 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.whakatauki` › `p` | 4 | 4 | 0.06 | structure-only |
| 6731 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.table-responsive` | 4 | 4 | 0.85 | structure-only |
| 6732 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert` › `div.activity` | 4 | 4 | 0.30 | structure-only |
| 6733 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.activity[number=3A]` | 4 | 4 | 0.85 | structure-only |
| 6734 | body | SUBSTITUTED | `div.row` › `div.col-md-4.col-12` › `div.col-md-8.col-12` | 4 | 4 | 0.05 | structure-only |
| 6735 | body | SUBSTITUTED | `div.videoSection.icon.ratio.ra` › `iframe.embed-responsive-item` › `div.row` | 4 | 4 | 0.21 | structure-only |
| 6736 | body | SUBSTITUTED | `div.alert` › `div.row` › `div.row` | 4 | 4 | 0.27 | structure-only |
| 6737 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `WIDGET` | 4 | 4 | 0.40 | structure-only |
| 6738 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `p>b` | 4 | 4 | 0.40 | structure-only |
| 6739 | body | SUBSTITUTED | `div.col-md-4.col-12.paddingLR` › `WIDGET` › `div.col-md-8.col-12` | 4 | 4 | 0.06 | structure-only |
| 6740 | body | SUBSTITUTED | `div.row` › `div.col-12` › `p` | 4 | 4 | 0.55 | structure-only |
| 6741 | body | SUBSTITUTED | `div.col-md-12.col-12` › `h2` › `h3` | 4 | 4 | 0.01 | structure-only |
| 6742 | body | SUBSTITUTED | `div.alertImage` › `img.img-fluid` › `img.img-fluid` | 4 | 4 | 0.13 | structure-only |
| 6743 | body | SUBSTITUTED | `div.row` › `div.col-md-2.col-12.paddingR` › `div.col-md-8.col-12` | 4 | 4 | 0.01 | structure-only |
| 6744 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row` › `a` | 4 | 4 | 0.25 | structure-only |
| 6745 | body | SUBSTITUTED | `div.row` › `div.col-md-2.col-12` › `div.col-md-8.col-12` | 4 | 4 | 0.01 | structure-only |
| 6746 | body | SUBSTITUTED | `div.col-md-8.col-12.paddingL` › `p` › `p` | 4 | 4 | 0.01 | structure-only |
| 6747 | body | SUBSTITUTED | `div.col-md-4.offset-md-0.col-1` › `div.alertImage` › `WIDGET` | 4 | 4 | 0.09 | structure-only |
| 6748 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `p>i` | 4 | 4 | 0.40 | structure-only |
| 6749 | body | SUBSTITUTED | `table.table.table-bordered` › `tr.rowSolid` › `tr` | 4 | 4 | 0.01 | structure-only |
| 6750 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.ratio.ratio-16x9` › `p>a` | 4 | 4 | 0.21 | structure-only |
| 6751 | body | SUBSTITUTED | `div.col-12` › `p` › `td` | 4 | 4 | 0.26 | structure-only |
| 6752 | body | SUBSTITUTED | `div.col-md-8.col-12` › `ul` › `div.table-responsive` | 4 | 4 | 0.23 | structure-only |
| 6753 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `div.row.flipCardsContainer` | 4 | 4 | 0.40 | structure-only |
| 6754 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12.choicePage.choic` › `div.col-md-8.col-12` | 4 | 4 | 0.03 | structure-only |
| 6755 | body | SUBSTITUTED | `div.col-md-8.col-12` › `img.img-fluid` › `h4` | 4 | 4 | 0.24 | structure-only |
| 6756 | body | SUBSTITUTED | `div.row` › `div.col-md-3.offset-md-0.col-12.padd` › `div.col-md-6.col-12` | 4 | 4 | 0.02 | structure-only |
| 6757 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `h5` | 4 | 4 | 0.40 | structure-only |
| 6758 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `div.alert` | 4 | 4 | 0.40 | structure-only |
| 6759 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert` › `img.img-fluid` | 4 | 4 | 0.30 | structure-only |
| 6760 | body | SUBSTITUTED | `div.col-md-8.col-12` › `img.img-fluid` › `h3` | 4 | 4 | 0.24 | structure-only |
| 6761 | body | SUBSTITUTED | `div#body` › `div.row` › `div.videoSection.icon.ratio.ratio-16` | 4 | 4 | 0.94 | structure-only |
| 6762 | body | SUBSTITUTED | `div.row` › `div.row` › `div#footer` | 4 | 4 | 0.07 | structure-only |
| 6763 | body | SUBSTITUTED | `div.row` › `div.col-md-4.offset-md-0.col-6.offse` › `div.row` | 4 | 4 | 0.03 | structure-only |
| 6764 | body | SUBSTITUTED | `div.row` › `div.col-md-4.offset-md-0.col-12` › `div.col-md-8.col-12` | 4 | 4 | 0.21 | structure-only |
| 6765 | body | SUBSTITUTED | `div.col-md-6.col-12.paddingLR` › `WIDGET` › `div.row` | 4 | 4 | 0.04 | structure-only |
| 6766 | body | SUBSTITUTED | `div.row.flipCardsContainer` › `div.col-md-6.col-12.paddingLR` › `div.col-md-8.col-12` | 4 | 4 | 0.03 | structure-only |
| 6767 | body | SUBSTITUTED | `p` › `b` › `i` | 4 | 4 | 0.18 | structure-only |
| 6768 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert.solid` › `h5` | 4 | 4 | 0.07 | structure-only |
| 6769 | body | SUBSTITUTED | `div.col-md-8.col-12.paddingR` › `p` › `p` | 4 | 4 | 0.12 | structure-only |
| 6770 | body | SUBSTITUTED | `div.col-md-8.col-12` › `img.img-fluid` › `div.videoSection.ratio.ratio-16x9` | 4 | 4 | 0.24 | structure-only |
| 6771 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert.solid` › `div.row` | 4 | 4 | 0.07 | structure-only |
| 6772 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row.flipCardsContainer` › `div.col-md-4.col-12.paddingLR` | 4 | 4 | 0.07 | structure-only |
| 6773 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row` › `div.button` | 4 | 4 | 0.25 | structure-only |
| 6774 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.whakatauki` › `img.img-fluid` | 4 | 4 | 0.06 | structure-only |
| 6775 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `div.button` | 4 | 4 | 0.40 | structure-only |
| 6776 | body | SUBSTITUTED | `div.whakatauki` › `p` › `p>b` | 4 | 4 | 0.10 | structure-only |
| 6777 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12` › `img.img-fluid` | 4 | 4 | 0.98 | structure-only |
| 6778 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `div.clickDropContent` | 4 | 4 | 0.40 | structure-only |
| 6779 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p.quoteText` › `div.quoteText` | 4 | 4 | 0.03 | structure-only |
| 6780 | body | SUBSTITUTED | `div.row` › `div.col-md-4.offset-md-0.col-12` › `div.col-12` | 4 | 4 | 0.21 | structure-only |
| 6781 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h2` › `div.col-md-8.col-12` | 4 | 4 | 0.15 | structure-only |
| 6782 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert.solid` › `p` | 4 | 4 | 0.07 | structure-only |
| 6783 | body | SUBSTITUTED | `div.col-md-8.col-12.paddingR` › `div.row` › `img.img-fluid` | 4 | 4 | 0.01 | structure-only |
| 6784 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row.flipCardsContainer` › `h3` | 4 | 4 | 0.07 | structure-only |
| 6785 | body | SUBSTITUTED | `div.row` › `div.row` › `li>a.home-nav` | 4 | 4 | 0.07 | structure-only |
| 6786 | body | SUBSTITUTED | `div.col-md-8.col-12` › `ol` › `p` | 4 | 4 | 0.04 | structure-only |
| 6787 | body | SUBSTITUTED | `div.col-md-8.col-12` › `img.img-fluid` › `p>b` | 4 | 4 | 0.24 | structure-only |
| 6788 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p>b` › `ul` | 4 | 4 | 0.20 | structure-only |
| 6789 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p>b` › `p` | 4 | 4 | 0.20 | structure-only |
| 6790 | body | SUBSTITUTED | `div.row` › `div.col-md-7.col-12` › `div.col-md-8.col-12` | 11 | 3 | 0.01 | structure-only |
| 6791 | body | MISSING | `div.col-md-8.col-12` › `h4.hintLink>span.hint` › `—` | 8 | 3 | 0.01 | 1.00 |
| 6792 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p.captionText` › `p` | 8 | 3 | 0.02 | structure-only |
| 6793 | body | EXTRA | `div.col-md-6.col-12` › `—` › `ul` | 6 | 3 | 1.00 | structure-only |
| 6794 | body | MISSING | `div.col-md-8.col-12.offset-md-` › `img.img-fluid` › `—` | 6 | 3 | 0.01 | structure-only |
| 6795 | body | MISSING | `div.col-md-8.col-12` › `div.alert.cultural[layout=combined]` › `—` | 6 | 3 | 0.01 | 1.00 |
| 6796 | body | MISSING | `div.row` › `p` › `—` | 6 | 3 | 0.01 | 0.33 |
| 6797 | body | SUBSTITUTED | `div#body` › `WIDGET` › `div.table-responsive` | 6 | 3 | 0.06 | structure-only |
| 6798 | body | SUBSTITUTED | `div.row` › `div.col-md-12` › `div.col-md-8.col-12` | 6 | 3 | 0.01 | structure-only |
| 6799 | body | SUBSTITUTED | `div.alert` › `p>b` › `div.row` | 6 | 3 | 0.01 | structure-only |
| 6800 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p.quoteText` › `p>i` | 6 | 3 | 0.03 | structure-only |
| 6801 | body | SUBSTITUTED | `p` › `ul` › `ul` | 6 | 3 | 0.01 | structure-only |
| 6802 | body | MISSING | `div.row` › `div.col-md-4.paddingL.col-12` › `—` | 5 | 3 | 0.00 | 1.00 |
| 6803 | body | MISSING | `div.col-md-4.offset-md-0.col-1` › `img.img-fluid` › `—` | 5 | 3 | 0.01 | structure-only |
| 6804 | body | MISSING | `div.col-md-8.col-12` › `hr` › `—` | 5 | 3 | 0.00 | structure-only |
| 6805 | body | MISSING | `div.col-12.choicePage.choiceHe` › `WIDGET` › `—` | 5 | 3 | 0.00 | structure-only |
| 6806 | body | MISSING | `div.row.supervisor` › `div.col-md-8.col-12.super-content-bu` › `—` | 5 | 3 | 0.07 | 0.80 |
| 6807 | body | MISSING | `div.col-md-8.col-12` › `p>a` › `—` | 5 | 3 | 0.01 | 0.40 |
| 6808 | body | MISSING | `div.row` › `div.col-md-2.offset-md-0.col-12.padd` › `—` | 5 | 3 | 0.00 | structure-only |
| 6809 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row.supervisor` › `p` | 5 | 3 | 0.01 | structure-only |
| 6810 | body | SUBSTITUTED | `div.alert.top` › `p.margB0` › `p` | 5 | 3 | 0.01 | structure-only |
| 6811 | body | SUBSTITUTED | `div.col-12` › `p>b` › `p` | 5 | 3 | 0.04 | structure-only |
| 6812 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.col-md-8.offset-md-2.col-12` › `img.img-fluid` | 5 | 3 | 0.00 | structure-only |
| 6813 | body | SUBSTITUTED | `ul` › `li>b` › `li` | 5 | 3 | 0.07 | structure-only |
| 6814 | body | SUBSTITUTED | `div.row` › `div.col-12.choicePage.choiceHeightMa` › `div.col-md-8.col-12` | 5 | 3 | 0.00 | structure-only |
| 6815 | body | SUBSTITUTED | `div.row` › `div.col-sm-8` › `div.col-md-8.col-12` | 5 | 3 | 0.01 | structure-only |
| 6816 | body | SUBSTITUTED | `p` › `math` › `i` | 5 | 3 | 0.02 | structure-only |
| 6817 | body | SUBSTITUTED | `div.row.flipCardsContainer` › `div.col-md-4.col-12.paddingLR` › `div.col-md-4.col-12.paddingLR` | 5 | 3 | 0.05 | structure-only |
| 6818 | body | EXTRA | `div.col-md-3.col-12` › `—` › `p` | 4 | 3 | 1.00 | structure-only |
| 6819 | body | EXTRA | `div.row` › `—` › `div.col-md-3.col-12` | 4 | 3 | 1.00 | structure-only |
| 6820 | body | EXTRA | `p` › `—` › `math` | 4 | 3 | 0.98 | structure-only |
| 6821 | body | MISSING | `div.col-8` › `div.alert` › `—` | 4 | 3 | 0.02 | 1.00 |
| 6822 | body | MISSING | `div.col-md-8.col-12.paddingR` › `br` › `—` | 4 | 3 | 0.01 | structure-only |
| 6823 | body | MISSING | `th` › `br` › `—` | 4 | 3 | 0.00 | structure-only |
| 6824 | body | MISSING | `td` › `ul` › `—` | 4 | 3 | 0.00 | 1.00 |
| 6825 | body | MISSING | `p>u` › `u` › `—` | 4 | 3 | 0.00 | 1.00 |
| 6826 | body | MISSING | `math` › `mn` › `—` | 4 | 3 | 0.01 | 1.00 |
| 6827 | body | MISSING | `math` › `mo` › `—` | 4 | 3 | 0.00 | 0.08 |
| 6828 | body | MOVED | `div.alertActivity` › `p>b` › `p` | 4 | 3 | 0.00 | structure-only |
| 6829 | body | MOVED | `div.col-12` › `p>i` › `p>i` | 4 | 3 | 0.00 | structure-only |
| 6830 | body | MOVED | `div.col-md-4.offset-md-0.col-1` › `p.captionText` › `p.captionText` | 4 | 3 | 0.01 | structure-only |
| 6831 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12` › `div.videoSection.icon.ratio.ratio-16` | 4 | 3 | 0.98 | structure-only |
| 6832 | body | SUBSTITUTED | `div.alert` › `h3` › `div.row` | 4 | 3 | 0.01 | structure-only |
| 6833 | body | SUBSTITUTED | `div.alertActivity` › `div.row` › `p` | 4 | 3 | 0.02 | structure-only |
| 6834 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.icon.ratio.ratio-16` › `audio.audioPlayer.icon` | 4 | 3 | 0.26 | structure-only |
| 6835 | body | SUBSTITUTED | `table.table.table-bordered` › `tr.rowSolid.primary-light` › `tr` | 4 | 3 | 0.00 | structure-only |
| 6836 | body | SUBSTITUTED | `table.table.table-bordered.tab` › `tr.rowSolid` › `tr` | 4 | 3 | 0.00 | structure-only |
| 6837 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert` › `p>a` | 4 | 3 | 0.30 | structure-only |
| 6838 | body | SUBSTITUTED | `div.col-md-8.col-12.paddingR` › `div.alert` › `p` | 4 | 3 | 0.01 | structure-only |
| 6839 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h2` › `p>b` | 4 | 3 | 0.15 | structure-only |
| 6840 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert.cultural[layout=combined]` › `div.row` | 4 | 3 | 0.02 | structure-only |
| 6841 | body | SUBSTITUTED | `p>span.infoTrigger` › `span.infoTrigger` › `i` | 4 | 3 | 0.15 | structure-only |
| 6842 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12.paddingL` › `div.col-md-6.col-12` | 4 | 3 | 0.01 | structure-only |
| 6843 | body | SUBSTITUTED | `div.videoSection.icon.ratio.ra` › `iframe.embed-responsive-item` › `div.button` | 4 | 3 | 0.21 | structure-only |
| 6844 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p.quoteAck` › `p>a` | 4 | 3 | 0.02 | structure-only |
| 6845 | body | SUBSTITUTED | `div.table-responsive` › `table.table.center-text` › `table.table.table-bordered` | 4 | 3 | 0.00 | structure-only |
| 6846 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `div.col-12` | 4 | 3 | 0.40 | structure-only |
| 6847 | body | SUBSTITUTED | `div.row` › `div.col-md-6.col-12` › `div.col-md-8.col-12` | 4 | 3 | 0.02 | structure-only |
| 6848 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row` › `div.row.flipCardsContainer` | 4 | 3 | 0.25 | structure-only |
| 6849 | body | EXTRA | `div.col-md-8.col-12` › `—` › `h4>b` | 3 | 3 | 1.00 | structure-only |
| 6850 | body | EXTRA | `p` › `—` › `a` | 3 | 3 | 1.00 | structure-only |
| 6851 | body | EXTRA | `ol` › `—` › `li>b` | 3 | 3 | 0.99 | structure-only |
| 6852 | body | EXTRA | `div.inquiryPanel` › `—` › `div.row.supervisor` | 3 | 3 | 1.00 | structure-only |
| 6853 | body | EXTRA | `th` › `—` › `b` | 3 | 3 | 1.00 | structure-only |
| 6854 | body | EXTRA | `div.col-md-8.col-12` › `—` › `h3>b` | 3 | 3 | 1.00 | structure-only |
| 6855 | body | EXTRA | `ul` › `—` › `li>i` | 3 | 3 | 1.00 | structure-only |
| 6856 | body | EXTRA | `div.TKmodal` › `—` › `div.videoSection.ratio.ratio-16x9` | 3 | 3 | 1.00 | structure-only |
| 6857 | body | EXTRA | `div.col-12` › `—` › `p>i` | 3 | 3 | 0.99 | structure-only |
| 6858 | body | EXTRA | `li` › `—` › `ol` | 3 | 3 | 1.00 | structure-only |
| 6859 | body | EXTRA | `a` › `—` › `div.button.downloadButton` | 3 | 3 | 1.00 | structure-only |
| 6860 | body | EXTRA | `div.row.phaseContainer` › `—` › `div.col-md-3.col-6` | 3 | 3 | 0.98 | structure-only |
| 6861 | body | EXTRA | `div.fundamentalsPanel` › `—` › `h3` | 3 | 3 | 1.00 | structure-only |
| 6862 | body | EXTRA | `td` › `—` › `img.img-fluid` | 3 | 3 | 0.97 | structure-only |
| 6863 | body | MISSING | `div.row` › `div.col-6` › `—` | 3 | 3 | 0.00 | 1.00 |
| 6864 | body | MISSING | `li` › `br` › `—` | 3 | 3 | 0.01 | structure-only |
| 6865 | body | MISSING | `div.col.paddingLR` › `img.img-fluid` › `—` | 3 | 3 | 0.00 | structure-only |
| 6866 | body | MISSING | `div.col-12` › `ul.margB0` › `—` | 3 | 3 | 0.01 | 0.67 |
| 6867 | body | MISSING | `a` › `img.img-fluid` › `—` | 3 | 3 | 0.00 | structure-only |
| 6868 | body | MISSING | `div.row` › `div.col-md-4.offset-md-0.col-12.alig` › `—` | 3 | 3 | 0.00 | 1.00 |
| 6869 | body | MISSING | `div.row` › `div.col-md-4.col-6.offset-3.offset-m` › `—` | 3 | 3 | 0.00 | 0.67 |
| 6870 | body | MISSING | `div.row` › `div.col-md-2.col-12.paddingR` › `—` | 3 | 3 | 0.01 | structure-only |
| 6871 | body | MISSING | `p` › `p` › `—` | 3 | 3 | 0.00 | 1.00 |
| 6872 | body | MISSING | `div.col-md-3.col-12.paddingR` › `img.img-fluid` › `—` | 3 | 3 | 0.00 | structure-only |
| 6873 | body | MISSING | `div.row` › `div.col-md-8.col-12.paddingT` › `—` | 3 | 3 | 0.00 | 0.00 |
| 6874 | body | MISSING | `div.TKmodal` › `img.img-fluid` › `—` | 3 | 3 | 0.01 | structure-only |
| 6875 | body | MISSING | `div.alert.solid` › `p` › `—` | 3 | 3 | 0.00 | 1.00 |
| 6876 | body | MISSING | `div.col-md-8.col-12.choicePage` › `WIDGET` › `—` | 3 | 3 | 0.02 | structure-only |
| 6877 | body | MISSING | `table.table.table-bordered.tab` › `tr` › `—` | 3 | 3 | 0.00 | 0.80 |
| 6878 | body | MISSING | `table.table.tableFixed.table-b` › `tr` › `—` | 3 | 3 | 0.00 | 1.00 |
| 6879 | body | MISSING | `div.col-md-12.col-12` › `div.clickDropContent` › `—` | 3 | 3 | 0.00 | 1.00 |
| 6880 | body | MISSING | `div.col-md-4.offset-md-0.col-1` › `WIDGET` › `—` | 3 | 3 | 0.00 | structure-only |
| 6881 | body | MISSING | `div.col-md-12.col-12` › `div.row.flipCardsContainer` › `—` | 3 | 3 | 0.03 | structure-only |
| 6882 | body | MISSING | `td` › `b` › `—` | 3 | 3 | 0.01 | 1.00 |
| 6883 | body | MISSING | `div.col-md-8.col-12` › `div.row.margB2.primary-bg` › `—` | 3 | 3 | 0.00 | 1.00 |
| 6884 | body | MISSING | `div.row` › `div.col-md-8.offset-md-0.col-12` › `—` | 3 | 3 | 0.01 | 1.00 |
| 6885 | body | MISSING | `div.row` › `div.col-md-6.offset-md-0.col-12.padd` › `—` | 3 | 3 | 0.01 | 0.75 |
| 6886 | body | MISSING | `div.col-md-6.offset-md-0.col-1` › `img.img-fluid` › `—` | 3 | 3 | 0.00 | structure-only |
| 6887 | body | MISSING | `div#body` › `div.col-12` › `—` | 3 | 3 | 0.00 | 0.67 |
| 6888 | body | MISSING | `div.col-md-8.col-12` › `div.embedPDF[layout=portrait]` › `—` | 3 | 3 | 0.00 | 1.00 |
| 6889 | body | MISSING | `div.clickDropContent` › `div.videoSection.icon.ratio.ratio-16` › `—` | 3 | 3 | 0.00 | structure-only |
| 6890 | body | MISSING | `div.row` › `div.clickDropContent` › `—` | 3 | 3 | 0.00 | 1.00 |
| 6891 | body | MISSING | `div#body` › `p` › `—` | 3 | 3 | 0.00 | 0.00 |
| 6892 | body | MISSING | `div.clickDropContent` › `div.videoSection.ratio.ratio-16x9` › `—` | 3 | 3 | 0.01 | structure-only |
| 6893 | body | MISSING | `span.infoTrigger>b` › `b` › `—` | 3 | 3 | 0.01 | 0.67 |
| 6894 | body | MISSING | `div.col-md-8.col-12` › `div.alert.blank` › `—` | 3 | 3 | 0.01 | 0.75 |
| 6895 | body | MISSING | `ul` › `p` › `—` | 3 | 3 | 0.00 | 0.33 |
| 6896 | body | MISSING | `div.col-md-8.col-12` › `img.img-fluid.margB2` › `—` | 3 | 3 | 0.00 | structure-only |
| 6897 | body | MISSING | `div.col-md-8.col-12.paddingR` › `div.table-responsive` › `—` | 3 | 3 | 0.01 | 0.67 |
| 6898 | body | MISSING | `li` › `span.infoTrigger` › `—` | 3 | 3 | 0.00 | 1.00 |
| 6899 | body | MISSING | `p` › `sup` › `—` | 3 | 3 | 0.00 | 1.00 |
| 6900 | body | MISSING | `div.col-md-8.col-12.paddingR` › `p>b` › `—` | 3 | 3 | 0.02 | 1.00 |
| 6901 | body | MISSING | `div.col-md-4.offset-md-0.col-1` › `div.alert.top` › `—` | 3 | 3 | 0.01 | 0.67 |
| 6902 | body | MISSING | `div.col-12` › `p.quoteText` › `—` | 3 | 3 | 0.01 | 1.00 |
| 6903 | body | MISSING | `div.col-12` › `div.videoSection.icon.ratio.ratio-16` › `—` | 3 | 3 | 0.00 | structure-only |
| 6904 | body | MISSING | `div.row` › `div.col-md-4.offset-md-0.col-12.padd` › `—` | 3 | 3 | 0.00 | 1.00 |
| 6905 | body | MISSING | `div.introduction.fundamentalsP` › `div.row.phaseContainer.justify-conte` › `—` | 3 | 3 | 0.00 | 1.00 |
| 6906 | body | MISSING | `div.col-md-8.col-12` › `img.img-fluid.mb-3` › `—` | 3 | 3 | 0.00 | structure-only |
| 6907 | body | MISSING | `div.col-md-8.col-12.paddingR` › `div.row` › `—` | 3 | 3 | 0.01 | 1.00 |
| 6908 | body | MISSING | `p` › `span` › `—` | 3 | 3 | 0.00 | 1.00 |
| 6909 | body | MISSING | `div.col-md-8.col-12` › `div.row.margB3` › `—` | 3 | 3 | 0.00 | 1.00 |
| 6910 | body | MISSING | `div.col-md-8.col-12` › `p.center-text` › `—` | 3 | 3 | 0.00 | 0.00 |
| 6911 | body | MISSING | `div.shape` › `h4` › `—` | 3 | 3 | 0.01 | 1.00 |
| 6912 | body | MISSING | `div.col-md-8.col-12` › `h1` › `—` | 3 | 3 | 0.00 | 0.25 |
| 6913 | body | MISSING | `div.inquiryPanel` › `div.row.clickDropContent.noBorder` › `—` | 3 | 3 | 0.00 | 1.00 |
| 6914 | body | MOVED | `div.col-12` › `p>span.highlight` › `p` | 3 | 3 | 0.01 | structure-only |
| 6915 | body | MOVED | `div.col-md-10.col-12.paddingL` › `p` › `p` | 3 | 3 | 0.01 | structure-only |
| 6916 | body | MOVED | `div.col-md-9.col-12` › `p` › `p` | 3 | 3 | 0.01 | structure-only |
| 6917 | body | MOVED | `div.col-md-8.col-12.paddingR` › `p>b` › `p>b` | 3 | 3 | 0.00 | structure-only |
| 6918 | body | MOVED | `p>i` › `i` › `i` | 3 | 3 | 0.03 | structure-only |
| 6919 | body | MOVED | `div.col-md-8.col-12.paddingR` › `p` › `p` | 3 | 3 | 0.07 | structure-only |
| 6920 | body | MOVED | `div.clickDropContent` › `h4` › `h4` | 3 | 3 | 0.01 | structure-only |
| 6921 | body | MOVED | `div.TKmodal` › `p` › `p` | 3 | 3 | 0.00 | structure-only |
| 6922 | body | MOVED | `ul` › `li>i` › `li>i` | 3 | 3 | 0.00 | structure-only |
| 6923 | body | MOVED | `div.col-md-8.col-12` › `p>strong` › `p>b` | 3 | 3 | 0.00 | structure-only |
| 6924 | body | MOVED | `p` › `b` › `b` | 3 | 3 | 0.07 | structure-only |
| 6925 | body | MOVED | `div.col-md-10.col-12` › `p` › `p` | 3 | 3 | 0.01 | structure-only |
| 6926 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h5` › `p>b` | 3 | 3 | 0.05 | structure-only |
| 6927 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p>b` › `img.img-fluid` | 3 | 3 | 0.20 | structure-only |
| 6928 | body | SUBSTITUTED | `div.col-md-8.col-12` › `img.img-fluid` › `div.alert.solid` | 3 | 3 | 0.24 | structure-only |
| 6929 | body | SUBSTITUTED | `ul` › `li` › `tr` | 3 | 3 | 0.35 | structure-only |
| 6930 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.whakatauki` › `h4` | 3 | 3 | 0.06 | structure-only |
| 6931 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h4` › `div.alert.solid` | 3 | 3 | 0.19 | structure-only |
| 6932 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.activity.interactive` | 3 | 3 | 0.48 | structure-only |
| 6933 | body | SUBSTITUTED | `div.alert` › `div.row` › `li` | 3 | 3 | 0.27 | structure-only |
| 6934 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.activity.interactive[number=3A]` | 3 | 3 | 0.85 | structure-only |
| 6935 | body | SUBSTITUTED | `div.col.paddingLR` › `p.captionText` › `p` | 3 | 3 | 0.00 | structure-only |
| 6936 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.activity[number=4C]` | 3 | 3 | 0.85 | structure-only |
| 6937 | body | SUBSTITUTED | `div.col-md-4.offset-md-0.col-1` › `div.alert.top` › `p` | 3 | 3 | 0.01 | structure-only |
| 6938 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.col-md-8.col-12` › `img.img-fluid` | 3 | 3 | 0.01 | structure-only |
| 6939 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12` › `li>a.home-nav` | 3 | 3 | 0.98 | structure-only |
| 6940 | body | SUBSTITUTED | `a` › `div.externalButton` › `iframe` | 3 | 3 | 0.08 | structure-only |
| 6941 | body | SUBSTITUTED | `div.row` › `div.col-md-4.offset-md-0.col-6.offse` › `div.col-md-4.offset-md-0.col-12` | 3 | 3 | 0.03 | structure-only |
| 6942 | body | SUBSTITUTED | `div.caption` › `p` › `p` | 3 | 3 | 0.01 | structure-only |
| 6943 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.videoSection.icon.ratio.ratio-16` | 3 | 3 | 0.85 | structure-only |
| 6944 | body | SUBSTITUTED | `a` › `div.externalButton` › `div.col-md-8.col-12` | 3 | 3 | 0.08 | structure-only |
| 6945 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.activity.interactive[number=3A]` | 3 | 3 | 0.48 | structure-only |
| 6946 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.ratio.ratio-16x9` › `div.col-md-8.col-12` | 3 | 3 | 0.21 | structure-only |
| 6947 | body | SUBSTITUTED | `div.videoSection.ratio.ratio-1` › `iframe` › `div.row` | 3 | 3 | 0.22 | structure-only |
| 6948 | body | SUBSTITUTED | `div.col-md-12.col-12` › `h3` › `h4` | 3 | 3 | 0.03 | structure-only |
| 6949 | body | SUBSTITUTED | `a` › `div.externalButton` › `WIDGET` | 3 | 3 | 0.08 | structure-only |
| 6950 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.icon.ratio.ratio-16` › `p>b` | 3 | 3 | 0.26 | structure-only |
| 6951 | body | SUBSTITUTED | `p>span.infoTrigger` › `span.infoTrigger` › `a` | 3 | 3 | 0.15 | structure-only |
| 6952 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row` › `div.activity` | 3 | 3 | 0.25 | structure-only |
| 6953 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12` › `div.acks.acksTemplate` | 3 | 3 | 0.98 | structure-only |
| 6954 | body | SUBSTITUTED | `div.col-12` › `p` › `p>i` | 3 | 3 | 0.26 | structure-only |
| 6955 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.activity[number=1A]` | 3 | 3 | 0.85 | structure-only |
| 6956 | body | SUBSTITUTED | `div.row` › `div.col-md-3.offset-md-0.col-6.offse` › `div.row` | 3 | 3 | 0.01 | structure-only |
| 6957 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12` › `div.TKmodal` | 3 | 3 | 0.98 | structure-only |
| 6958 | body | SUBSTITUTED | `div.col-12` › `h2` › `h3` | 3 | 3 | 0.01 | structure-only |
| 6959 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12` › `p>i` | 3 | 3 | 0.98 | structure-only |
| 6960 | body | SUBSTITUTED | `div.inquiryPanel` › `div.row.supervisor` › `div.row` | 3 | 3 | 0.01 | structure-only |
| 6961 | body | SUBSTITUTED | `div.row.supervisor` › `div.col-md-10.col-12` › `div.col-md-8.col-12` | 3 | 3 | 0.00 | structure-only |
| 6962 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div` › `p>b` | 3 | 3 | 0.02 | structure-only |
| 6963 | body | SUBSTITUTED | `div.alertActivity` › `h4` › `p` | 3 | 3 | 0.05 | structure-only |
| 6964 | body | SUBSTITUTED | `div.alertActivity` › `p.margB0` › `p` | 3 | 3 | 0.01 | structure-only |
| 6965 | body | SUBSTITUTED | `div.row` › `div.col-md-2.offset-md-0.col-12` › `div.col-md-8.col-12` | 3 | 3 | 0.01 | structure-only |
| 6966 | body | SUBSTITUTED | `div.col-md-8.col-12.super-cont` › `div.videoSection.icon.ratio.ratio-16` › `p` | 3 | 3 | 0.01 | structure-only |
| 6967 | body | SUBSTITUTED | `div.row` › `div.row.supervisor` › `div.col-md-8.col-12` | 3 | 3 | 0.01 | structure-only |
| 6968 | body | SUBSTITUTED | `div.col-12` › `p>a` › `p>a` | 3 | 3 | 0.04 | structure-only |
| 6969 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `audio.audioPlayer.icon` | 3 | 3 | 0.85 | structure-only |
| 6970 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h2` › `a` | 3 | 3 | 0.15 | structure-only |
| 6971 | body | SUBSTITUTED | `td` › `br` › `b` | 3 | 3 | 0.02 | structure-only |
| 6972 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h2` › `div.alert.solid` | 3 | 3 | 0.15 | structure-only |
| 6973 | body | SUBSTITUTED | `div.alertImage` › `img.img-fluid` › `li` | 3 | 3 | 0.13 | structure-only |
| 6974 | body | SUBSTITUTED | `p` › `b` › `a` | 3 | 3 | 0.18 | structure-only |
| 6975 | body | SUBSTITUTED | `div.row` › `div.col-md-4.col-12.paddingR` › `div.col-md-6.col-12` | 3 | 3 | 0.01 | structure-only |
| 6976 | body | SUBSTITUTED | `div.row` › `div.col-md-4.offset-md-0.col-12.padd` › `div.col-md-6.col-12` | 3 | 3 | 0.14 | structure-only |
| 6977 | body | SUBSTITUTED | `div.alert.cultural[layout=comb` › `div.row` › `div.row` | 3 | 3 | 0.02 | structure-only |
| 6978 | body | SUBSTITUTED | `div.table-responsive` › `table.table.table-bordered.tableFixe` › `table.table.table-bordered` | 3 | 3 | 0.00 | structure-only |
| 6979 | body | SUBSTITUTED | `td` › `p` › `b` | 3 | 3 | 0.02 | structure-only |
| 6980 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.alert.top` | 3 | 3 | 0.48 | structure-only |
| 6981 | body | SUBSTITUTED | `div.row` › `div.col-md-4.col-12.paddingL` › `div.col-md-6.col-12` | 3 | 3 | 0.06 | structure-only |
| 6982 | body | SUBSTITUTED | `ol` › `li` › `td` | 3 | 3 | 0.06 | structure-only |
| 6983 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row.selectionBox` › `WIDGET` | 3 | 3 | 0.01 | structure-only |
| 6984 | body | SUBSTITUTED | `div.col-md-8.col-12` › `img.img-fluid` › `WIDGET` | 3 | 3 | 0.24 | structure-only |
| 6985 | body | SUBSTITUTED | `div.col-12` › `p.quoteText` › `p` | 3 | 3 | 0.01 | structure-only |
| 6986 | body | SUBSTITUTED | `div.col-md-12.col-12` › `div.row.flipCardsContainer` › `WIDGET` | 3 | 3 | 0.03 | structure-only |
| 6987 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12.paddingR` › `div.col-12` | 3 | 3 | 0.14 | structure-only |
| 6988 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.icon.ratio.ratio-16` › `h3` | 3 | 3 | 0.26 | structure-only |
| 6989 | body | SUBSTITUTED | `div.col-md-12.col-12.paddingLR` › `WIDGET` › `div.row` | 3 | 3 | 0.01 | structure-only |
| 6990 | body | SUBSTITUTED | `ul` › `li` › `div.row` | 3 | 3 | 0.35 | structure-only |
| 6991 | body | SUBSTITUTED | `div.alert.solid` › `div.row` › `div.row` | 3 | 3 | 0.07 | structure-only |
| 6992 | body | SUBSTITUTED | `div.fundamentalsPanel` › `WIDGET` › `WIDGET` | 3 | 3 | 0.01 | structure-only |
| 6993 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.activity.interactive[number=2C]` | 3 | 3 | 0.48 | structure-only |
| 6994 | body | SUBSTITUTED | `div.fundamentalsPanel` › `div.row` › `div.col-md-4.col-12.paddingLR` | 3 | 3 | 0.03 | structure-only |
| 6995 | body | SUBSTITUTED | `li` › `br` › `b` | 3 | 3 | 0.01 | structure-only |
| 6996 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `h5>i` | 3 | 3 | 0.85 | structure-only |
| 6997 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h2` › `ul` | 3 | 3 | 0.15 | structure-only |
| 6998 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert` › `div.col-md-8.col-12` | 3 | 3 | 0.30 | structure-only |
| 6999 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert.solid` › `h4` | 3 | 3 | 0.07 | structure-only |
| 7000 | body | SUBSTITUTED | `div.alert.solid` › `p` › `p` | 3 | 3 | 0.01 | structure-only |
| 7001 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `p>i` | 3 | 3 | 0.85 | structure-only |
| 7002 | body | SUBSTITUTED | `div.row` › `div.col-md-4.offset-md-0.col-12` › `div.col-md-6.col-12` | 3 | 3 | 0.21 | structure-only |
| 7003 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.table-responsive` › `img.img-fluid` | 3 | 3 | 0.08 | structure-only |
| 7004 | body | SUBSTITUTED | `div#body` › `div.row` › `div.col-md-4.col-12.paddingLR` | 3 | 3 | 0.94 | structure-only |
| 7005 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row` › `h5` | 3 | 3 | 0.25 | structure-only |
| 7006 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.activity[number=1D]` | 3 | 3 | 0.85 | structure-only |
| 7007 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h4` › `div.activity` | 3 | 3 | 0.19 | structure-only |
| 7008 | body | SUBSTITUTED | `div.alert.top` › `p` › `div.row` | 3 | 3 | 0.03 | structure-only |
| 7009 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.col-md-12.col-12` › `p` | 3 | 3 | 0.03 | structure-only |
| 7010 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.activity[number=3A]` | 3 | 3 | 0.48 | structure-only |
| 7011 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.activity[number=6A]` | 3 | 3 | 0.85 | structure-only |
| 7012 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert` › `p>b` | 3 | 3 | 0.30 | structure-only |
| 7013 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.activity[number=2A]` | 3 | 3 | 0.85 | structure-only |
| 7014 | body | SUBSTITUTED | `div.row.flipCardsContainer` › `div.col-md-6.col-12.paddingLR` › `div.row` | 3 | 3 | 0.03 | structure-only |
| 7015 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.clickDropContent` › `div.table-responsive` | 3 | 3 | 0.08 | structure-only |
| 7016 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.clickDropContent` › `div.col-md-8.col-12` | 3 | 3 | 0.08 | structure-only |
| 7017 | body | SUBSTITUTED | `div.col-md-8.col-12.paddingR` › `p` › `p>i` | 3 | 3 | 0.12 | structure-only |
| 7018 | body | SUBSTITUTED | `div.alert.top` › `p` › `p` | 3 | 3 | 0.03 | structure-only |
| 7019 | body | SUBSTITUTED | `div.col-md-4.col-12.paddingLR` › `WIDGET` › `div.col-md-4.col-12.paddingLR` | 3 | 3 | 0.06 | structure-only |
| 7020 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `h3` | 3 | 3 | 0.48 | structure-only |
| 7021 | body | SUBSTITUTED | `div.col-md-6.offset-md-0.col-1` › `img.img-fluid` › `img.img-fluid` | 3 | 3 | 0.01 | structure-only |
| 7022 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.activity[number=1B]` | 3 | 3 | 0.85 | structure-only |
| 7023 | body | SUBSTITUTED | `div.alert` › `p` › `p` | 3 | 3 | 0.06 | structure-only |
| 7024 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.button` | 3 | 3 | 0.85 | structure-only |
| 7025 | body | SUBSTITUTED | `div.row` › `div.col-md-4.col-12.paddingLR` › `div.col-md-4.col-12.paddingLR` | 3 | 3 | 0.02 | structure-only |
| 7026 | body | SUBSTITUTED | `div.row` › `div.col-md-6.offset-md-0.col-12` › `div.col-md-8.col-12` | 3 | 3 | 0.02 | structure-only |
| 7027 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12` › `div.row.flipCardsContainer` | 3 | 3 | 0.98 | structure-only |
| 7028 | body | SUBSTITUTED | `div.captionImage` › `div.captionTrigger` › `div.row` | 3 | 3 | 0.01 | structure-only |
| 7029 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p>b` › `div.alert` | 3 | 3 | 0.20 | structure-only |
| 7030 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `div.button.TKmodalButton` | 3 | 3 | 0.40 | structure-only |
| 7031 | body | SUBSTITUTED | `div.col-12` › `h3` › `p` | 3 | 3 | 0.17 | structure-only |
| 7032 | body | SUBSTITUTED | `div.alert` › `ul` › `div.row` | 3 | 3 | 0.03 | structure-only |
| 7033 | body | SUBSTITUTED | `div.whakatauki` › `p` › `p>i` | 3 | 3 | 0.10 | structure-only |
| 7034 | body | SUBSTITUTED | `div.col.paddingLR` › `img.img-fluid` › `img.img-fluid` | 3 | 3 | 0.01 | structure-only |
| 7035 | body | SUBSTITUTED | `p>strong` › `strong` › `b` | 3 | 3 | 0.01 | structure-only |
| 7036 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `ol` | 3 | 3 | 0.85 | structure-only |
| 7037 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p>span.infoTrigger` › `h4` | 3 | 3 | 0.14 | structure-only |
| 7038 | body | SUBSTITUTED | `div.col-md-4.offset-md-0.col-1` › `div.alert.top` › `div.row` | 3 | 3 | 0.04 | structure-only |
| 7039 | body | SUBSTITUTED | `div.col-md-4.col-12.paddingLR` › `WIDGET` › `div.col-12` | 3 | 3 | 0.06 | structure-only |
| 7040 | body | SUBSTITUTED | `div.row` › `div.col-md-4.offset-md-0.col-12.padd` › `div.col-12` | 3 | 3 | 0.14 | structure-only |
| 7041 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.col-md-10.col-12` › `img.img-fluid` | 3 | 3 | 0.00 | structure-only |
| 7042 | body | SUBSTITUTED | `p>b` › `b` › `i` | 3 | 3 | 0.27 | structure-only |
| 7043 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.icon.ratio.ratio-16` › `div.button` | 3 | 3 | 0.26 | structure-only |
| 7044 | body | SUBSTITUTED | `div.fundamentalsPanel` › `div.row` › `WIDGET` | 3 | 3 | 0.03 | structure-only |
| 7045 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert` › `div.activity[number=3A]` | 3 | 3 | 0.30 | structure-only |
| 7046 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row.flipCardsContainer` › `ul` | 3 | 3 | 0.07 | structure-only |
| 7047 | body | SUBSTITUTED | `div.col-md-8.col-12` › `img.img-fluid.mb-3` › `img.img-fluid` | 3 | 3 | 0.00 | structure-only |
| 7048 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.clickDropContent` › `div.col-12` | 3 | 3 | 0.08 | structure-only |
| 7049 | body | SUBSTITUTED | `ul` › `li` › `p` | 3 | 3 | 0.35 | structure-only |
| 7050 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h4` › `div.alert` | 3 | 3 | 0.19 | structure-only |
| 7051 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.activity[number=4A]` | 3 | 3 | 0.48 | structure-only |
| 7052 | body | SUBSTITUTED | `mfrac` › `mn` › `mn` | 3 | 3 | 0.01 | structure-only |
| 7053 | body | SUBSTITUTED | `math` › `mfrac` › `mfrac` | 3 | 3 | 0.02 | structure-only |
| 7054 | body | SUBSTITUTED | `p` › `br` › `li` | 3 | 3 | 0.14 | structure-only |
| 7055 | body | SUBSTITUTED | `div.col-md-8.col-12` › `ol` › `ul` | 3 | 3 | 0.04 | structure-only |
| 7056 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.activity[number=2B]` | 3 | 3 | 0.85 | structure-only |
| 7057 | body | SUBSTITUTED | `div.row` › `div.col-md-4.offset-md-0.col-12.padd` › `WIDGET` | 3 | 3 | 0.14 | structure-only |
| 7058 | body | SUBSTITUTED | `div.fundamentalsPanel` › `div.row` › `div.row` | 3 | 3 | 0.03 | structure-only |
| 7059 | body | SUBSTITUTED | `div.row` › `div.col-md-4.offset-md-0.col-12` › `div.clickDropContent` | 3 | 3 | 0.21 | structure-only |
| 7060 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row.flipCardsContainer` › `h4` | 3 | 3 | 0.07 | structure-only |
| 7061 | body | SUBSTITUTED | `div.col-md-12.col-12` › `p` › `p` | 3 | 3 | 0.03 | structure-only |
| 7062 | body | SUBSTITUTED | `div.col-md-6.col-12.paddingLR` › `WIDGET` › `WIDGET` | 3 | 3 | 0.04 | structure-only |
| 7063 | body | SUBSTITUTED | `p>i` › `i` › `b` | 3 | 3 | 0.09 | structure-only |
| 7064 | body | SUBSTITUTED | `div.fundamentalsPanel` › `div.row` › `h3` | 3 | 3 | 0.03 | structure-only |
| 7065 | body | SUBSTITUTED | `div.hintDropContent` › `p` › `p` | 3 | 3 | 0.02 | structure-only |
| 7066 | body | SUBSTITUTED | `p>i` › `i>b` › `b` | 3 | 3 | 0.01 | structure-only |
| 7067 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.col-md-12.col-12` › `p>b` | 3 | 3 | 0.03 | structure-only |
| 7068 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert` › `div.clickDropContent.activity.dropbo` | 3 | 3 | 0.30 | structure-only |
| 7069 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert` › `div.clickDropContent.activity.dropbo` | 3 | 3 | 0.30 | structure-only |
| 7070 | body | SUBSTITUTED | `a` › `div.button` › `div.row` | 3 | 3 | 0.03 | structure-only |
| 7071 | body | SUBSTITUTED | `div.col-12` › `div.hintDropContent` › `div.clickDropContent` | 3 | 3 | 0.01 | structure-only |
| 7072 | body | SUBSTITUTED | `div.col-md-8.col-12` › `br` › `h4` | 9 | 2 | 0.05 | structure-only |
| 7073 | body | SUBSTITUTED | `div.col-12` › `ul` › `ol` | 8 | 2 | 0.12 | structure-only |
| 7074 | body | SUBSTITUTED | `div.col-12` › `p.margB0` › `div` | 7 | 2 | 0.04 | structure-only |
| 7075 | body | MISSING | `div.alertActivity` › `h3` › `—` | 6 | 2 | 0.01 | 0.83 |
| 7076 | body | MOVED | `div.hintDropContent` › `p` › `p` | 6 | 2 | 0.02 | structure-only |
| 7077 | body | SUBSTITUTED | `div.row.supervisor` › `div.col-md-8.col-12.super-content-bu` › `div.col-md-8.col-12.super-content-bu` | 6 | 2 | 0.00 | structure-only |
| 7078 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert.cultural[layout=combined]` › `div.alert.top` | 6 | 2 | 0.02 | structure-only |
| 7079 | body | EXTRA | `div.col-md-8.col-12` › `—` › `div.hintDropContent` | 5 | 2 | 0.99 | structure-only |
| 7080 | body | SUBSTITUTED | `div.col-md-8.col-12` › `br` › `div.alert` | 5 | 2 | 0.05 | structure-only |
| 7081 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert.blank` › `div.alert.solid` | 5 | 2 | 0.01 | structure-only |
| 7082 | body | SUBSTITUTED | `div.alert` › `div.row` › `p` | 5 | 2 | 0.27 | structure-only |
| 7083 | body | SUBSTITUTED | `div.videoSection.ratio.ratio-1` › `iframe.embed-responsive-item` › `iframe` | 5 | 2 | 0.00 | structure-only |
| 7084 | body | SUBSTITUTED | `div.col-12` › `div.row` › `WIDGET` | 5 | 2 | 0.02 | structure-only |
| 7085 | body | MISSING | `div.col-md-12.col-12` › `h2` › `—` | 4 | 2 | 0.01 | 1.00 |
| 7086 | body | MISSING | `h3>i` › `i` › `—` | 4 | 2 | 0.01 | 1.00 |
| 7087 | body | MISSING | `div.row` › `div.col-md-12` › `—` | 4 | 2 | 0.00 | 1.00 |
| 7088 | body | MISSING | `div.col-md-8.col-12` › `div.button.TKmodalButton` › `—` | 4 | 2 | 0.01 | 1.00 |
| 7089 | body | MISSING | `div.alert` › `h5` › `—` | 4 | 2 | 0.00 | 1.00 |
| 7090 | body | MISSING | `div.alert.solid` › `ul` › `—` | 4 | 2 | 0.00 | 1.00 |
| 7091 | body | SUBSTITUTED | `tbody` › `tr` › `td` | 4 | 2 | 0.01 | structure-only |
| 7092 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p.quoteText` › `p` | 4 | 2 | 0.03 | structure-only |
| 7093 | body | SUBSTITUTED | `div.row` › `WIDGET` › `table.table.table-bordered` | 4 | 2 | 0.02 | structure-only |
| 7094 | body | SUBSTITUTED | `div.col-md-4.offset-md-0.col-1` › `WIDGET` › `div.clickDropContent` | 4 | 2 | 0.01 | structure-only |
| 7095 | body | SUBSTITUTED | `div#body` › `div.row.supervisor` › `div.videoSection.ratio.ratio-16x9` | 4 | 2 | 0.12 | structure-only |
| 7096 | body | EXTRA | `div.super-content.row` › `—` › `div.row` | 3 | 2 | 0.94 | structure-only |
| 7097 | body | EXTRA | `div.col-md-6.col-12` › `—` › `p>i` | 3 | 2 | 1.00 | structure-only |
| 7098 | body | EXTRA | `h3>b` › `—` › `b` | 3 | 2 | 1.00 | structure-only |
| 7099 | body | EXTRA | `li` › `—` › `ul` | 3 | 2 | 1.00 | structure-only |
| 7100 | body | MISSING | `div.carousel-btns` › `div.button` › `—` | 3 | 2 | 0.00 | 0.36 |
| 7101 | body | MISSING | `div.captionTrigger` › `img.img-fluid` › `—` | 3 | 2 | 0.01 | structure-only |
| 7102 | body | MISSING | `div.row` › `div.col-md-3.offset-md-1.col-12` › `—` | 3 | 2 | 0.00 | structure-only |
| 7103 | body | MISSING | `div.alert.solid` › `WIDGET` › `—` | 3 | 2 | 0.00 | structure-only |
| 7104 | body | MISSING | `table.table.tableFixed` › `tr` › `—` | 3 | 2 | 0.01 | 1.00 |
| 7105 | body | MISSING | `div.row` › `div.col-md-3.offset-md-1.col-6.offse` › `—` | 3 | 2 | 0.00 | 1.00 |
| 7106 | body | MISSING | `p` › `span.audioTrigger` › `—` | 3 | 2 | 0.00 | 1.00 |
| 7107 | body | MISSING | `div.col-md-8.col-12.paddingR` › `p>span.infoTrigger` › `—` | 3 | 2 | 0.01 | 1.00 |
| 7108 | body | MISSING | `th` › `p` › `—` | 3 | 2 | 0.00 | 0.33 |
| 7109 | body | MISSING | `div.row` › `div.col-10.offset-1` › `—` | 3 | 2 | 0.00 | structure-only |
| 7110 | body | MISSING | `p>sup` › `sup` › `—` | 3 | 2 | 0.00 | 1.00 |
| 7111 | body | MISSING | `div.offset-md-2.col-md-8.col-1` › `img.img-fluid` › `—` | 3 | 2 | 0.00 | structure-only |
| 7112 | body | MISSING | `div.row` › `div.col-md-10.col-12.offset-md-1` › `—` | 3 | 2 | 0.00 | structure-only |
| 7113 | body | MISSING | `div.shapeHover` › `div.placeholderContent` › `—` | 3 | 2 | 0.00 | 1.00 |
| 7114 | body | MISSING | `div.col-md-8.col-12.super-cont` › `WIDGET` › `—` | 3 | 2 | 0.01 | structure-only |
| 7115 | body | MISSING | `p` › `span.highlight` › `—` | 3 | 2 | 0.00 | 1.00 |
| 7116 | body | MOVED | `div.col-md-8.col-12` › `p>span.infoTrigger` › `p>span.infoTrigger` | 3 | 2 | 0.14 | structure-only |
| 7117 | body | MOVED | `div.alert` › `p>b` › `p>b` | 3 | 2 | 0.00 | structure-only |
| 7118 | body | MOVED | `div.col-md-8.col-12.paddingLR` › `p` › `p` | 3 | 2 | 0.00 | structure-only |
| 7119 | body | MOVED | `div.clickDropContent` › `p` › `p` | 3 | 2 | 0.05 | structure-only |
| 7120 | body | SUBSTITUTED | `div.col-md-4.col-12.paddingL` › `div.alert.top` › `div.col-md-8.col-12` | 3 | 2 | 0.01 | structure-only |
| 7121 | body | SUBSTITUTED | `div.alertActivity` › `p` › `div.row` | 3 | 2 | 0.10 | structure-only |
| 7122 | body | SUBSTITUTED | `div.alert` › `div.row` › `div.button` | 3 | 2 | 0.27 | structure-only |
| 7123 | body | SUBSTITUTED | `div.col-md-8.col-12.super-cont` › `div.videoSection.icon.ratio.ratio-16` › `div.videoSection.ratio.ratio-16x9` | 3 | 2 | 0.01 | structure-only |
| 7124 | body | SUBSTITUTED | `div.col-8` › `div.alert` › `p` | 3 | 2 | 0.02 | structure-only |
| 7125 | body | SUBSTITUTED | `thead` › `tr.rowSolid` › `th>b` | 3 | 2 | 0.00 | structure-only |
| 7126 | body | SUBSTITUTED | `tr.rowSolid` › `th` › `th` | 3 | 2 | 0.02 | structure-only |
| 7127 | body | SUBSTITUTED | `div.alert.cultural[layout=comb` › `div.row` › `div.col-md-8.col-12` | 3 | 2 | 0.02 | structure-only |
| 7128 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p.quoteText` › `div.alert.solid` | 3 | 2 | 0.03 | structure-only |
| 7129 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert.solid` › `img.img-fluid` | 3 | 2 | 0.07 | structure-only |
| 7130 | body | SUBSTITUTED | `ul` › `li>b` › `li>b` | 3 | 2 | 0.07 | structure-only |
| 7131 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert.solid` › `div.activity` | 3 | 2 | 0.07 | structure-only |
| 7132 | body | SUBSTITUTED | `a` › `div.externalButton` › `div.button.externalButton` | 3 | 2 | 0.08 | structure-only |
| 7133 | body | SUBSTITUTED | `table.table.center-text` › `tr.rowSolid` › `tr` | 3 | 2 | 0.00 | structure-only |
| 7134 | body | SUBSTITUTED | `p` › `br` › `div.col-12` | 3 | 2 | 0.14 | structure-only |
| 7135 | body | SUBSTITUTED | `div.row` › `div.col-md-4.col-12.paddingL` › `div.videoSection.ratio.ratio-16x9` | 3 | 2 | 0.06 | structure-only |
| 7136 | body | EXTRA | `div.alertActivity` › `—` › `ul` | 2 | 2 | 0.98 | structure-only |
| 7137 | body | EXTRA | `b>a` › `—` › `a` | 2 | 2 | 1.00 | structure-only |
| 7138 | body | EXTRA | `div.col-md-8.col-12.paddingR` › `—` › `h4` | 2 | 2 | 1.00 | structure-only |
| 7139 | body | EXTRA | `div.row.supervisor` › `—` › `div.col-md-8.col-12` | 2 | 2 | 0.91 | structure-only |
| 7140 | body | EXTRA | `tr` › `—` › `th>a` | 2 | 2 | 1.00 | structure-only |
| 7141 | body | EXTRA | `div.col-md-8.col-12` › `—` › `h3>a` | 2 | 2 | 1.00 | structure-only |
| 7142 | body | EXTRA | `h3>a` › `—` › `a` | 2 | 2 | 1.00 | structure-only |
| 7143 | body | EXTRA | `div.col-md-8.col-12` › `—` › `div.wananga` | 2 | 2 | 1.00 | structure-only |
| 7144 | body | EXTRA | `ol` › `—` › `li>i` | 2 | 2 | 1.00 | structure-only |
| 7145 | body | EXTRA | `tr` › `—` › `td>i` | 2 | 2 | 1.00 | structure-only |
| 7146 | body | EXTRA | `div.alert.top` › `—` › `p>b` | 2 | 2 | 1.00 | structure-only |
| 7147 | body | EXTRA | `div.col-md-4.col-12` › `—` › `img.img-fluid` | 2 | 2 | 0.99 | structure-only |
| 7148 | body | EXTRA | `div.col-12` › `—` › `img.img-fluid` | 2 | 2 | 0.96 | structure-only |
| 7149 | body | EXTRA | `div.TKmodal` › `—` › `h5` | 2 | 2 | 1.00 | structure-only |
| 7150 | body | EXTRA | `div.clickDropContent` › `—` › `ol` | 2 | 2 | 1.00 | structure-only |
| 7151 | body | EXTRA | `div.phaseLink` › `—` › `img.phaseImg` | 2 | 2 | 0.99 | structure-only |
| 7152 | body | EXTRA | `div.phaseLink` › `—` › `h3` | 2 | 2 | 1.00 | structure-only |
| 7153 | body | EXTRA | `mrow` › `—` › `mn` | 2 | 2 | 1.00 | structure-only |
| 7154 | body | EXTRA | `math` › `—` › `mo` | 2 | 2 | 0.99 | structure-only |
| 7155 | body | EXTRA | `msup` › `—` › `mrow` | 2 | 2 | 1.00 | structure-only |
| 7156 | body | EXTRA | `mrow` › `—` › `mrow` | 2 | 2 | 1.00 | structure-only |
| 7157 | body | EXTRA | `math` › `—` › `mfrac` | 2 | 2 | 0.98 | structure-only |
| 7158 | body | EXTRA | `p>i` › `—` › `i>a` | 2 | 2 | 1.00 | structure-only |
| 7159 | body | EXTRA | `div.col-md-6.col-12` › `—` › `h4` | 2 | 2 | 1.00 | structure-only |
| 7160 | body | EXTRA | `div#body` › `—` › `div.inquiryPanel.showing` | 2 | 2 | 0.98 | structure-only |
| 7161 | body | EXTRA | `div.row.flipCardsContainer` › `—` › `div.col-md-6.col-sm-6.col-12.padding` | 2 | 2 | 1.00 | structure-only |
| 7162 | body | EXTRA | `div.col-md-3.col-12` › `—` › `p>b` | 2 | 2 | 1.00 | structure-only |
| 7163 | body | EXTRA | `th` › `—` › `img.img-fluid` | 2 | 2 | 1.00 | structure-only |
| 7164 | body | EXTRA | `div.inquiryPanel` › `—` › `WIDGET` | 2 | 2 | 1.00 | structure-only |
| 7165 | body | EXTRA | `div.alert` › `—` › `p` | 2 | 2 | 0.99 | structure-only |
| 7166 | body | EXTRA | `div.alert` › `—` › `h4` | 2 | 2 | 0.97 | structure-only |
| 7167 | body | EXTRA | `div.col-12` › `—` › `WIDGET` | 2 | 2 | 1.00 | structure-only |
| 7168 | body | EXTRA | `div.col-md-3.col-12` › `—` › `img.img-fluid` | 2 | 2 | 1.00 | structure-only |
| 7169 | body | MISSING | `p>b.blue-text` › `b.blue-text` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7170 | body | MISSING | `p` › `sub` › `—` | 2 | 2 | 0.00 | 0.33 |
| 7171 | body | MISSING | `div.col.paddingR` › `img.img-fluid` › `—` | 2 | 2 | 0.01 | structure-only |
| 7172 | body | MISSING | `div.col-md-8.col-12` › `div.col-md-10.col-12` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7173 | body | MISSING | `div.col-md-8.col-12.super-cont` › `div.videoSection.icon.ratio.ratio-16` › `—` | 2 | 2 | 0.01 | structure-only |
| 7174 | body | MISSING | `div.col-md-12.col-12` › `div.row` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7175 | body | MISSING | `div.choiceImg` › `img` › `—` | 2 | 2 | 0.00 | structure-only |
| 7176 | body | MISSING | `div.row` › `div.col-md-3.offset-md-0.col-6.paddi` › `—` | 2 | 2 | 0.00 | structure-only |
| 7177 | body | MISSING | `div.row` › `div.col-md-3.offset-md-0.col-6` › `—` | 2 | 2 | 0.00 | structure-only |
| 7178 | body | MISSING | `div.row` › `div.col-2` › `—` | 2 | 2 | 0.00 | structure-only |
| 7179 | body | MISSING | `div.col-md-2.offset-md-0.col-1` › `img.img-fluid` › `—` | 2 | 2 | 0.01 | structure-only |
| 7180 | body | MISSING | `div.row` › `div.col-md-4.col-12.PaddingLR` › `—` | 2 | 2 | 0.00 | structure-only |
| 7181 | body | MISSING | `p` › `span.sassoonI-text` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7182 | body | MISSING | `p` › `b.secondary-text` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7183 | body | MISSING | `div.col-md-8.col-12.super-cont` › `p.paddingR` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7184 | body | MISSING | `div.row` › `div.col-md-4.offset-md-0.col-12.alig` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7185 | body | MISSING | `div.row` › `div.col-md-3.col-12.paddingR` › `—` | 2 | 2 | 0.00 | structure-only |
| 7186 | body | MISSING | `div.row.supervisor` › `div.col-12.super-content-button.padd` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7187 | body | MISSING | `div.col-md-8.col-12` › `div.col-12.paddingR` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7188 | body | MISSING | `div.table-responsive` › `table.table.tableFixed.table-bordere` › `—` | 2 | 2 | 0.01 | 1.00 |
| 7189 | body | MISSING | `th>b` › `b` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7190 | body | MISSING | `div.col-md-12.col-12` › `WIDGET` › `—` | 2 | 2 | 0.00 | structure-only |
| 7191 | body | MISSING | `mrow` › `mo` › `—` | 2 | 2 | 0.01 | 0.50 |
| 7192 | body | MISSING | `mrow` › `mi` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7193 | body | MISSING | `div.col-12.paddingLR` › `WIDGET` › `—` | 2 | 2 | 0.00 | structure-only |
| 7194 | body | MISSING | `div.col-12` › `audio.audioPlayer` › `—` | 2 | 2 | 0.00 | structure-only |
| 7195 | body | MISSING | `div.table-responsive.marg0` › `table.table` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7196 | body | MISSING | `span.infoTrigger` › `span.ch-text` › `—` | 2 | 2 | 0.00 | 0.50 |
| 7197 | body | MISSING | `span.infoTrigger` › `span.pinyin` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7198 | body | MISSING | `div.videoSection.icon.ratio.ra` › `iframe` › `—` | 2 | 2 | 0.00 | structure-only |
| 7199 | body | MISSING | `p` › `b>span.ch-text` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7200 | body | MISSING | `td` › `i` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7201 | body | MISSING | `p` › `span.infoTrigger>b` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7202 | body | MISSING | `div.fundamentalsPanel` › `br` › `—` | 2 | 2 | 0.00 | structure-only |
| 7203 | body | MISSING | `p.quoteText` › `br` › `—` | 2 | 2 | 0.00 | structure-only |
| 7204 | body | MISSING | `div.col-md-8.col-12` › `div.col-md-10.offset-md-1.col-12` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7205 | body | MISSING | `div.col-12` › `ol` › `—` | 2 | 2 | 0.01 | 1.00 |
| 7206 | body | MISSING | `div.row` › `div.col-md-3.col-12.align-self-cente` › `—` | 2 | 2 | 0.00 | 0.50 |
| 7207 | body | MISSING | `div.alert.top` › `h4` › `—` | 2 | 2 | 0.00 | 0.00 |
| 7208 | body | MISSING | `div.row` › `img.img-fluid` › `—` | 2 | 2 | 0.00 | structure-only |
| 7209 | body | MISSING | `div#body` › `div.row.margB2` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7210 | body | MISSING | `div.row` › `div.col-md-4.col-6.paddingLR` › `—` | 2 | 2 | 0.00 | 0.86 |
| 7211 | body | MISSING | `div.col.choicePage.imgHeadVis.` › `div.choice>a` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7212 | body | MISSING | `td` › `p>b` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7213 | body | MISSING | `p.center-text` › `br` › `—` | 2 | 2 | 0.00 | structure-only |
| 7214 | body | MISSING | `div.col-md-10.col-12` › `div.row.flipCardsContainer` › `—` | 2 | 2 | 0.00 | structure-only |
| 7215 | body | MISSING | `div.row` › `div.col-4.paddingLR` › `—` | 2 | 2 | 0.00 | structure-only |
| 7216 | body | MISSING | `div.row` › `div.col-md-3.col-6.paddingR` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7217 | body | MISSING | `div.col-md-3.col-12.paddingL` › `img.img-fluid` › `—` | 2 | 2 | 0.01 | structure-only |
| 7218 | body | MISSING | `div.col-md-4.offset-md-0.col-1` › `img.img-fluid` › `—` | 2 | 2 | 0.00 | structure-only |
| 7219 | body | MISSING | `div.table-responsive` › `table.table.table-bordered.tableFixe` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7220 | body | MISSING | `div.col-xs-12` › `h3` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7221 | body | MISSING | `div.row` › `h3` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7222 | body | MISSING | `div.col-12` › `div.table-responsive` › `—` | 2 | 2 | 0.01 | 1.00 |
| 7223 | body | MISSING | `div.col-md-8.col-12` › `div.col-md-6.offset-md-3.col-12.padd` › `—` | 2 | 2 | 0.00 | structure-only |
| 7224 | body | MISSING | `div.col.paddingLR` › `WIDGET` › `—` | 2 | 2 | 0.00 | structure-only |
| 7225 | body | MISSING | `div#body` › `div.row.selectionBox` › `—` | 2 | 2 | 0.00 | 0.50 |
| 7226 | body | MISSING | `a` › `div.button.downloadButton` › `—` | 2 | 2 | 0.00 | 0.67 |
| 7227 | body | MISSING | `table.table` › `colgroup` › `—` | 2 | 2 | 0.00 | structure-only |
| 7228 | body | MISSING | `div.row` › `div.col-3.paddingLR` › `—` | 2 | 2 | 0.00 | structure-only |
| 7229 | body | MISSING | `div.row` › `div.offset-md-2.col-md-8.col-12` › `—` | 2 | 2 | 0.00 | structure-only |
| 7230 | body | MISSING | `div.captionImage` › `div.captionTrigger` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7231 | body | MISSING | `p` › `WIDGET` › `—` | 2 | 2 | 0.00 | structure-only |
| 7232 | body | MISSING | `td` › `h5` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7233 | body | MISSING | `div.col-md-6.col-12` › `img.img-fluid` › `—` | 2 | 2 | 0.00 | structure-only |
| 7234 | body | MISSING | `div.row.margB2.justify-content` › `div.col-3` › `—` | 2 | 2 | 0.00 | structure-only |
| 7235 | body | MISSING | `div.alert` › `a` › `—` | 2 | 2 | 0.00 | 0.33 |
| 7236 | body | MISSING | `body.container-fluid` › `div#body` › `—` | 2 | 2 | 0.80 | 0.00 |
| 7237 | body | MISSING | `div.alert.blank` › `div.row` › `—` | 2 | 2 | 0.01 | 0.50 |
| 7238 | body | MISSING | `div.col-12` › `h2` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7239 | body | MISSING | `div.TKmodal` › `br` › `—` | 2 | 2 | 0.00 | structure-only |
| 7240 | body | MISSING | `div.button.TKmodalButton` › `img.img-fluid` › `—` | 2 | 2 | 0.00 | structure-only |
| 7241 | body | MISSING | `div.col-md-8.col-12.paddingR` › `div.clickDropContent` › `—` | 2 | 2 | 0.00 | 0.89 |
| 7242 | body | MISSING | `div.row` › `div.TKmodal` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7243 | body | MISSING | `div.col-md-8.col-12.paddingR` › `h4` › `—` | 2 | 2 | 0.00 | 0.67 |
| 7244 | body | MISSING | `div.col-md-8.col-12` › `p.quoteAck>b` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7245 | body | MISSING | `div.col-12` › `p>i` › `—` | 2 | 2 | 0.01 | 1.00 |
| 7246 | body | MISSING | `div.col-md-3.col-12.paddingLR` › `img.img-fluid` › `—` | 2 | 2 | 0.00 | structure-only |
| 7247 | body | MISSING | `div.row.flipCardsContainer` › `div.col-md-4.col-6.paddingR` › `—` | 2 | 2 | 0.00 | structure-only |
| 7248 | body | MISSING | `div.col-md-4.col-6.paddingR` › `WIDGET` › `—` | 2 | 2 | 0.00 | structure-only |
| 7249 | body | MISSING | `div.fundamentalsPanel` › `div.col-md-8.col-12` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7250 | body | MISSING | `div.clickDropContent` › `img.img-fluid` › `—` | 2 | 2 | 0.00 | structure-only |
| 7251 | body | MISSING | `math` › `mrow` › `—` | 2 | 2 | 0.00 | 0.33 |
| 7252 | body | MISSING | `mrow` › `mn` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7253 | body | MISSING | `div.col-4` › `div.alert.top.paddingL` › `—` | 2 | 2 | 0.00 | 0.50 |
| 7254 | body | MISSING | `mfrac` › `mn` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7255 | body | MISSING | `div.embedPDF[layout=portrait]` › `object` › `—` | 2 | 2 | 0.00 | 0.33 |
| 7256 | body | MISSING | `object` › `p>a` › `—` | 2 | 2 | 0.01 | 0.00 |
| 7257 | body | MISSING | `table.table.center-text` › `tr` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7258 | body | MISSING | `div.row` › `div.col-md-3.paddingL.offset-md-0.co` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7259 | body | MISSING | `div.col-md-6.offset-md-3.col-1` › `img.img-fluid` › `—` | 2 | 2 | 0.00 | structure-only |
| 7260 | body | MISSING | `li` › `u` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7261 | body | MISSING | `div.col-md-3.offset-md-0.col-1` › `img.img-fluid` › `—` | 2 | 2 | 0.00 | structure-only |
| 7262 | body | MISSING | `div.col-md-4.offset-md-0.col-6` › `div.alertImage` › `—` | 2 | 2 | 0.00 | structure-only |
| 7263 | body | MISSING | `div.col-md-8.col-12.paddingR` › `ol` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7264 | body | MISSING | `div.col-12` › `div.clickDropContent` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7265 | body | MISSING | `div.col-md-8.col-12` › `div.clickDropContent.overflowYScroll` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7266 | body | MISSING | `div.row` › `div.col-12.paddingR` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7267 | body | MISSING | `div.alert.solid` › `h4` › `—` | 2 | 2 | 0.01 | 1.00 |
| 7268 | body | MISSING | `div.alertActivity` › `br` › `—` | 2 | 2 | 0.00 | structure-only |
| 7269 | body | MISSING | `div.introduction` › `div.row.phaseContainer` › `—` | 2 | 2 | 0.02 | 1.00 |
| 7270 | body | MISSING | `div.col-md-3.col-6` › `div.phaseLink` › `—` | 2 | 2 | 0.02 | 1.00 |
| 7271 | body | MISSING | `div.row` › `div.col-md-8.col-12.infoImage` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7272 | body | MISSING | `div.clickDropContent` › `div.embedPDF[layout=portrait]` › `—` | 2 | 2 | 0.00 | 0.00 |
| 7273 | body | MISSING | `table.table.noHover.center-tex` › `tr` › `—` | 2 | 2 | 0.00 | structure-only |
| 7274 | body | MISSING | `div.shapeContent` › `div` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7275 | body | MISSING | `b>span.audioTrigger` › `span.audioTrigger` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7276 | body | MISSING | `div.col-md-10.col-12` › `img.img-fluid` › `—` | 2 | 2 | 0.01 | structure-only |
| 7277 | body | MISSING | `div.col-md-10.col-12` › `p.captionText` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7278 | body | MISSING | `div.row` › `div.col-md-4.col-6.offset-3.offset-m` › `—` | 2 | 2 | 0.00 | structure-only |
| 7279 | body | MISSING | `div.col-md-8.col-12` › `div.row.align-items-center` › `—` | 2 | 2 | 0.00 | 0.50 |
| 7280 | body | MISSING | `div.col-md-10.col-12` › `div.clickDropContent` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7281 | body | MISSING | `div.col-12` › `div.hintDropContent` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7282 | body | MISSING | `div.col-md-8.col-12` › `p.captionText>i` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7283 | body | MISSING | `div.alertActivity` › `ul` › `—` | 2 | 2 | 0.02 | 1.00 |
| 7284 | body | MISSING | `div.row` › `a` › `—` | 2 | 2 | 0.00 | 0.50 |
| 7285 | body | MISSING | `p` › `b>i` › `—` | 2 | 2 | 0.00 | 0.33 |
| 7286 | body | MISSING | `div.col-md-6.col-6.paddingLR` › `WIDGET` › `—` | 2 | 2 | 0.00 | structure-only |
| 7287 | body | MISSING | `div#body` › `div.col-md-12.col-12` › `—` | 2 | 2 | 0.00 | 1.00 |
| 7288 | body | MISSING | `div.row.super-content` › `div.row` › `—` | 2 | 2 | 0.02 | 0.50 |
| 7289 | body | MISSING | `div.row.supervisor` › `div.col-md-8.col-12` › `—` | 2 | 2 | 0.01 | 0.67 |
| 7290 | body | MOVED | `ul` › `li>span.infoTrigger` › `li` | 2 | 2 | 0.01 | structure-only |
| 7291 | body | MOVED | `ul.margB0` › `li` › `li` | 2 | 2 | 0.00 | structure-only |
| 7292 | body | MOVED | `p` › `p` › `p` | 2 | 2 | 0.00 | structure-only |
| 7293 | body | MOVED | `div.col-12` › `p>a` › `p>a` | 2 | 2 | 0.00 | structure-only |
| 7294 | body | MOVED | `div.col-md-6.col-12.paddingL` › `p` › `p` | 2 | 2 | 0.01 | structure-only |
| 7295 | body | MOVED | `div.col-md-10.col-12.paddingL` › `p` › `p` | 2 | 2 | 0.01 | structure-only |
| 7296 | body | MOVED | `div.col-12.paddingR` › `p` › `p` | 2 | 2 | 0.00 | structure-only |
| 7297 | body | MOVED | `a` › `div.button` › `div.button` | 2 | 2 | 0.01 | structure-only |
| 7298 | body | MOVED | `div.clickDropContent` › `p>i` › `p>i` | 2 | 2 | 0.00 | structure-only |
| 7299 | body | MOVED | `div.col-md-8.col-12.paddingL` › `p` › `p` | 2 | 2 | 0.00 | structure-only |
| 7300 | body | MOVED | `div.col-md-8.col-12.paddingR` › `h4` › `h4` | 2 | 2 | 0.00 | structure-only |
| 7301 | body | MOVED | `ol` › `li` › `li` | 2 | 2 | 0.04 | structure-only |
| 7302 | body | MOVED | `div.alert.top` › `p>b` › `p>b` | 2 | 2 | 0.00 | structure-only |
| 7303 | body | MOVED | `div.col-md-8.col-12` › `a` › `a` | 2 | 2 | 0.01 | structure-only |
| 7304 | body | MOVED | `div.TKmodal` › `h5` › `h5` | 2 | 2 | 0.00 | structure-only |
| 7305 | body | MOVED | `div.alertImage` › `p.captionText` › `p.captionText` | 2 | 2 | 0.00 | structure-only |
| 7306 | body | MOVED | `div.col-12` › `p.captionText` › `p.captionText` | 2 | 2 | 0.00 | structure-only |
| 7307 | body | MOVED | `ul` › `li>strong` › `li>b` | 2 | 2 | 0.00 | structure-only |
| 7308 | body | MOVED | `li` › `p` › `p` | 2 | 2 | 0.00 | structure-only |
| 7309 | body | MOVED | `div.col-md-7.col-12` › `p` › `p` | 2 | 2 | 0.01 | structure-only |
| 7310 | body | MOVED | `div.col-md-8.col-12` › `p>em` › `p>i` | 2 | 2 | 0.00 | structure-only |
| 7311 | body | MOVED | `div.col-md-8.col-12` › `p.hintLink` › `p.hintLink` | 2 | 2 | 0.01 | structure-only |
| 7312 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert.blank` › `p>b` | 2 | 2 | 0.01 | structure-only |
| 7313 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert` › `ol` | 2 | 2 | 0.30 | structure-only |
| 7314 | body | SUBSTITUTED | `div.row` › `div.col-12` › `div.table-responsive` | 2 | 2 | 0.55 | structure-only |
| 7315 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12` › `div.externalButton` | 2 | 2 | 0.98 | structure-only |
| 7316 | body | SUBSTITUTED | `tr` › `td` › `WIDGET` | 2 | 2 | 0.12 | structure-only |
| 7317 | body | SUBSTITUTED | `ul` › `li` › `div.button` | 2 | 2 | 0.35 | structure-only |
| 7318 | body | SUBSTITUTED | `div.col-12` › `h3` › `img.img-fluid` | 2 | 2 | 0.17 | structure-only |
| 7319 | body | SUBSTITUTED | `div.whakatauki` › `p` › `iframe` | 2 | 2 | 0.10 | structure-only |
| 7320 | body | SUBSTITUTED | `div.row` › `div.col.paddingR` › `WIDGET` | 2 | 2 | 0.01 | structure-only |
| 7321 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12` › `div.table-responsive` | 2 | 2 | 0.98 | structure-only |
| 7322 | body | SUBSTITUTED | `div.row` › `div.col-md-4.offset-md-0.col-12.padd` › `div.table-responsive` | 2 | 2 | 0.14 | structure-only |
| 7323 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.activity[number=5A]` | 2 | 2 | 0.48 | structure-only |
| 7324 | body | SUBSTITUTED | `div.col-md-8.col-12` › `a` › `div.videoSection.icon.ratio.ratio-16` | 2 | 2 | 0.07 | structure-only |
| 7325 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `p>a` | 2 | 2 | 0.85 | structure-only |
| 7326 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12` › `div.row.supervisor` | 2 | 2 | 0.98 | structure-only |
| 7327 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.col-md-8.col-12` › `p` | 2 | 2 | 0.01 | structure-only |
| 7328 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.activity[number=4A]` | 2 | 2 | 0.85 | structure-only |
| 7329 | body | SUBSTITUTED | `div.translate` › `p` › `p` | 2 | 2 | 0.00 | structure-only |
| 7330 | body | SUBSTITUTED | `div.col-12` › `p` › `h3` | 2 | 2 | 0.26 | structure-only |
| 7331 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.ratio.ratio-16x9` › `div.activity` | 2 | 2 | 0.21 | structure-only |
| 7332 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.activity.interactive[number=9A]` | 2 | 2 | 0.85 | structure-only |
| 7333 | body | SUBSTITUTED | `div.col-md-8.col-12.paddingR` › `div.alert.blank` › `p` | 2 | 2 | 0.00 | structure-only |
| 7334 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row` › `div.col-md-4.col-12` | 2 | 2 | 0.25 | structure-only |
| 7335 | body | SUBSTITUTED | `div.row.flipCardsContainer` › `div.col-md-4.col-12.paddingLR` › `div.col-md-8.col-12` | 2 | 2 | 0.05 | structure-only |
| 7336 | body | SUBSTITUTED | `div#body` › `WIDGET` › `div.ratio.ratio-16x9` | 2 | 2 | 0.06 | structure-only |
| 7337 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.activity[number=3C]` | 2 | 2 | 0.85 | structure-only |
| 7338 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.ratio.ratio-16x9` | 2 | 2 | 0.48 | structure-only |
| 7339 | body | SUBSTITUTED | `div.row` › `div.col-8.offset-2` › `div.row` | 2 | 2 | 0.01 | structure-only |
| 7340 | body | SUBSTITUTED | `div#body` › `div.row` › `div` | 2 | 2 | 0.94 | structure-only |
| 7341 | body | SUBSTITUTED | `div.videoSection.icon.ratio.ra` › `iframe` › `div.row` | 2 | 2 | 0.09 | structure-only |
| 7342 | body | SUBSTITUTED | `div#body` › `WIDGET` › `div.col-12` | 2 | 2 | 0.06 | structure-only |
| 7343 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.col-md-12.col-12.infoImage` › `img.img-fluid` | 2 | 2 | 0.00 | structure-only |
| 7344 | body | SUBSTITUTED | `a` › `div.button` › `div.externalButton` | 2 | 2 | 0.03 | structure-only |
| 7345 | body | SUBSTITUTED | `div.row` › `div.col-md-4.offset-md-0.col-12.padd` › `div.videoSection.icon.ratio.ratio-16` | 2 | 2 | 0.14 | structure-only |
| 7346 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row` › `div.alert` | 2 | 2 | 0.25 | structure-only |
| 7347 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row.flipCardsContainer` › `div.alert` | 2 | 2 | 0.07 | structure-only |
| 7348 | body | SUBSTITUTED | `div.row` › `div.col-md-3.offset-md-0.col-12` › `div.col-md-8.col-12` | 2 | 2 | 0.04 | structure-only |
| 7349 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row.flipCardsContainer` › `img.img-fluid` | 2 | 2 | 0.07 | structure-only |
| 7350 | body | SUBSTITUTED | `div.col-md-3.offset-md-0.col-1` › `img.img-fluid.paddingLR` › `img.img-fluid` | 2 | 2 | 0.00 | structure-only |
| 7351 | body | SUBSTITUTED | `div#body` › `div.row` › `div.col-md-8.col-12` | 2 | 2 | 0.94 | structure-only |
| 7352 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `p>a` | 2 | 2 | 0.48 | structure-only |
| 7353 | body | SUBSTITUTED | `div.row` › `div.col.paddingLR` › `div.row` | 2 | 2 | 0.01 | structure-only |
| 7354 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.icon.ratio.ratio-16` › `h5` | 2 | 2 | 0.26 | structure-only |
| 7355 | body | SUBSTITUTED | `div.choiceText` › `p` › `p` | 2 | 2 | 0.00 | structure-only |
| 7356 | body | SUBSTITUTED | `a` › `div.choiceImg` › `div.row` | 2 | 2 | 0.01 | structure-only |
| 7357 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h2` › `h3>b` | 2 | 2 | 0.15 | structure-only |
| 7358 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.icon.ratio.ratio-16` › `h3>b` | 2 | 2 | 0.26 | structure-only |
| 7359 | body | SUBSTITUTED | `div.row.supervisor` › `div.col-md-8.col-12` › `div.col-md-8.col-12.super-content-bu` | 2 | 2 | 0.09 | structure-only |
| 7360 | body | SUBSTITUTED | `div.row` › `div.col-12` › `h3` | 2 | 2 | 0.55 | structure-only |
| 7361 | body | SUBSTITUTED | `div.col-md-3.offset-md-0.col-6` › `div.alertActivity.solid` › `div.col-md-8.col-12` | 2 | 2 | 0.00 | structure-only |
| 7362 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.activity[number=8C]` | 2 | 2 | 0.85 | structure-only |
| 7363 | body | SUBSTITUTED | `div.row` › `div.row` › `div.col-md-4.col-12.paddingLR` | 2 | 2 | 0.07 | structure-only |
| 7364 | body | SUBSTITUTED | `div.col-md-8.col-12.paddingR` › `div` › `div.row` | 2 | 2 | 0.00 | structure-only |
| 7365 | body | SUBSTITUTED | `div.col-md-8.col-12.paddingR` › `br` › `p>b` | 2 | 2 | 0.01 | structure-only |
| 7366 | body | SUBSTITUTED | `div.col-md-8.col-12` › `br` › `p>b` | 2 | 2 | 0.05 | structure-only |
| 7367 | body | SUBSTITUTED | `div.row` › `div.col-md-2.offset-md-0.col-12` › `div.col-md-8.col-12>a` | 2 | 2 | 0.01 | structure-only |
| 7368 | body | SUBSTITUTED | `div.row` › `div.col-md-6.col-12.paddingL` › `div.row` | 2 | 2 | 0.01 | structure-only |
| 7369 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row` › `div.activity[number=1B]` | 2 | 2 | 0.25 | structure-only |
| 7370 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert.solid.padding0` › `p>a` | 2 | 2 | 0.01 | structure-only |
| 7371 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert.solid.padding0` › `div.row` | 2 | 2 | 0.01 | structure-only |
| 7372 | body | SUBSTITUTED | `div.alert.solid.padding0` › `div.videoSection.icon.ratio.ratio-16` › `div.col-md-8.col-12` | 2 | 2 | 0.01 | structure-only |
| 7373 | body | SUBSTITUTED | `div.row` › `div.row` › `div.buttonD` | 2 | 2 | 0.07 | structure-only |
| 7374 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h4` › `a` | 2 | 2 | 0.19 | structure-only |
| 7375 | body | SUBSTITUTED | `div.row` › `div.col-md-6.col-12` › `div.row` | 2 | 2 | 0.02 | structure-only |
| 7376 | body | SUBSTITUTED | `div.col-12` › `a` › `a` | 2 | 2 | 0.02 | structure-only |
| 7377 | body | SUBSTITUTED | `div.row.supervisor` › `div.col-md-8.col-12.paddingL` › `div.col-md-8.col-12` | 2 | 2 | 0.00 | structure-only |
| 7378 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div` › `div.col-md-8.col-12` | 2 | 2 | 0.02 | structure-only |
| 7379 | body | SUBSTITUTED | `div.col-md-12.col-12` › `h2` › `h4` | 2 | 2 | 0.01 | structure-only |
| 7380 | body | SUBSTITUTED | `div#body` › `div.col-md-8.col-12` › `div.buttonD` | 2 | 2 | 0.02 | structure-only |
| 7381 | body | SUBSTITUTED | `div.row.supervisor` › `div.col-md-8.col-12` › `div.col-md-8.col-12` | 2 | 2 | 0.09 | structure-only |
| 7382 | body | SUBSTITUTED | `div.row` › `div.col-md-2.col-12` › `p` | 2 | 2 | 0.01 | structure-only |
| 7383 | body | SUBSTITUTED | `div.videoSection.icon.ratio.ra` › `p.red-text` › `p` | 2 | 2 | 0.00 | structure-only |
| 7384 | body | SUBSTITUTED | `div.col-md-3.offset-md-0.col-1` › `img.img-fluid` › `p` | 2 | 2 | 0.01 | structure-only |
| 7385 | body | SUBSTITUTED | `div.alert.solid` › `h4` › `div.row` | 2 | 2 | 0.01 | structure-only |
| 7386 | body | SUBSTITUTED | `div.col-12` › `div.clickDropContent` › `img.img-fluid` | 2 | 2 | 0.01 | structure-only |
| 7387 | body | SUBSTITUTED | `div.row` › `div.col-4` › `WIDGET` | 2 | 2 | 0.02 | structure-only |
| 7388 | body | SUBSTITUTED | `div.row` › `div.col-md-3.col-12` › `div.button` | 2 | 2 | 0.03 | structure-only |
| 7389 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12.offset-md-2` › `div.col-md-8.col-12` | 2 | 2 | 0.01 | structure-only |
| 7390 | body | SUBSTITUTED | `div.col-md-8.col-12.choicePage` › `WIDGET` › `div.col-12` | 2 | 2 | 0.03 | structure-only |
| 7391 | body | SUBSTITUTED | `div.col-md-4.offset-md-0.col-1` › `img.img-fluid` › `p>b` | 2 | 2 | 0.04 | structure-only |
| 7392 | body | SUBSTITUTED | `tr` › `td` › `th>b` | 2 | 2 | 0.12 | structure-only |
| 7393 | body | SUBSTITUTED | `div.row` › `div.col-12` › `div.wananga` | 2 | 2 | 0.55 | structure-only |
| 7394 | body | SUBSTITUTED | `div.col-12` › `h5` › `h4>b` | 2 | 2 | 0.01 | structure-only |
| 7395 | body | SUBSTITUTED | `div.col-md-12.col-12` › `WIDGET` › `h4` | 2 | 2 | 0.03 | structure-only |
| 7396 | body | SUBSTITUTED | `div.whakatauki` › `p` › `li>i` | 2 | 2 | 0.10 | structure-only |
| 7397 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.table-responsive` | 2 | 2 | 0.48 | structure-only |
| 7398 | body | SUBSTITUTED | `div#body` › `div.inquiryPanel` › `div.row` | 2 | 2 | 0.02 | structure-only |
| 7399 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert.cultural[layout=combined]` › `p` | 2 | 2 | 0.02 | structure-only |
| 7400 | body | SUBSTITUTED | `thead` › `tr.rowSolid` › `th` | 2 | 2 | 0.00 | structure-only |
| 7401 | body | SUBSTITUTED | `a` › `div.externalButton` › `div.externalButton` | 2 | 2 | 0.08 | structure-only |
| 7402 | body | SUBSTITUTED | `div.col-md-8.col-12.paddingR` › `div.alert` › `img.img-fluid` | 2 | 2 | 0.01 | structure-only |
| 7403 | body | SUBSTITUTED | `div.row` › `div.col-12` › `div.videoSection.ratio.ratio-16x9` | 2 | 2 | 0.55 | structure-only |
| 7404 | body | SUBSTITUTED | `div.row` › `div.col-md-12.col-12` › `div.button` | 2 | 2 | 0.25 | structure-only |
| 7405 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert` › `div.table-responsive` | 2 | 2 | 0.30 | structure-only |
| 7406 | body | SUBSTITUTED | `div.alert` › `div.row` › `div.table-responsive` | 2 | 2 | 0.27 | structure-only |
| 7407 | body | SUBSTITUTED | `div.row` › `div.col-md-12.col-12` › `div.col-md-6.col-12` | 2 | 2 | 0.25 | structure-only |
| 7408 | body | SUBSTITUTED | `div.row` › `div.col` › `li` | 2 | 2 | 0.02 | structure-only |
| 7409 | body | SUBSTITUTED | `div.row` › `div.col` › `div.col-12` | 2 | 2 | 0.02 | structure-only |
| 7410 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h4` › `div.table-responsive` | 2 | 2 | 0.19 | structure-only |
| 7411 | body | SUBSTITUTED | `div.row` › `div.col-md-12.col-12` › `div.table-responsive` | 2 | 2 | 0.25 | structure-only |
| 7412 | body | SUBSTITUTED | `div.row` › `div.col` › `div.row` | 2 | 2 | 0.02 | structure-only |
| 7413 | body | SUBSTITUTED | `div.row` › `div.col-md-6.col-12.paddingR` › `table.table.table-bordered` | 2 | 2 | 0.01 | structure-only |
| 7414 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `ol` | 2 | 2 | 0.40 | structure-only |
| 7415 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h2` › `div.table-responsive` | 2 | 2 | 0.15 | structure-only |
| 7416 | body | SUBSTITUTED | `div.row` › `div.col-md-4.offset-md-0.col-12.padd` › `div.row` | 2 | 2 | 0.01 | structure-only |
| 7417 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p>b` › `h4` | 2 | 2 | 0.20 | structure-only |
| 7418 | body | SUBSTITUTED | `div.alert.cultural[layout=comb` › `div.row` › `div.button` | 2 | 2 | 0.02 | structure-only |
| 7419 | body | SUBSTITUTED | `td` › `img.img-fluid` › `img.img-fluid` | 2 | 2 | 0.04 | structure-only |
| 7420 | body | SUBSTITUTED | `div.col-12` › `p.quoteText` › `p>i` | 2 | 2 | 0.01 | structure-only |
| 7421 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.activity.interactive[number=2A]` | 2 | 2 | 0.48 | structure-only |
| 7422 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12` › `ul` | 2 | 2 | 0.98 | structure-only |
| 7423 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12` › `p>b` | 2 | 2 | 0.98 | structure-only |
| 7424 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `li` | 2 | 2 | 0.85 | structure-only |
| 7425 | body | SUBSTITUTED | `div.col-md-8.col-12` › `ul` › `li` | 2 | 2 | 0.23 | structure-only |
| 7426 | body | SUBSTITUTED | `div.inquiryPanel.showing` › `div.row` › `div.row` | 2 | 2 | 0.02 | structure-only |
| 7427 | body | SUBSTITUTED | `div.whakatauki` › `p` › `div.col-12` | 2 | 2 | 0.10 | structure-only |
| 7428 | body | SUBSTITUTED | `div.inquiryPanel` › `div.row` › `div.button` | 2 | 2 | 0.02 | structure-only |
| 7429 | body | SUBSTITUTED | `div.col-md-4.offset-md-0.col-1` › `div.alert.top` › `div.alert.solid` | 2 | 2 | 0.04 | structure-only |
| 7430 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h2` › `div.button` | 2 | 2 | 0.15 | structure-only |
| 7431 | body | SUBSTITUTED | `div.table-responsive` › `table.table.table-bordered.tableFixe` › `table.table.table-bordered` | 2 | 2 | 0.00 | structure-only |
| 7432 | body | SUBSTITUTED | `div.inquiryPanel` › `div.row` › `div.col-12` | 2 | 2 | 0.02 | structure-only |
| 7433 | body | SUBSTITUTED | `div.col-md-12.col-12` › `div.row.flipCardsContainer` › `p` | 2 | 2 | 0.03 | structure-only |
| 7434 | body | SUBSTITUTED | `div.row.flipCardsContainer` › `div.col-md-3.col-6.paddingLR` › `div.col-md-4.col-12.paddingLR` | 2 | 2 | 0.00 | structure-only |
| 7435 | body | SUBSTITUTED | `table.table` › `tr` › `tr` | 2 | 2 | 0.03 | structure-only |
| 7436 | body | SUBSTITUTED | `td` › `img.img-fluid` › `a` | 2 | 2 | 0.04 | structure-only |
| 7437 | body | SUBSTITUTED | `tr` › `th` › `td` | 2 | 2 | 0.04 | structure-only |
| 7438 | body | SUBSTITUTED | `tr` › `th` › `td>b` | 2 | 2 | 0.04 | structure-only |
| 7439 | body | SUBSTITUTED | `div.row.flipCardsContainer` › `div.col-md-8.offset-md-2.col-12` › `div.col-md-4.col-12.paddingLR` | 2 | 2 | 0.00 | structure-only |
| 7440 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.youtubeShort.ratio.` › `WIDGET` | 2 | 2 | 0.01 | structure-only |
| 7441 | body | SUBSTITUTED | `div.row` › `div.col-md-6.col-12` › `b` | 2 | 2 | 0.02 | structure-only |
| 7442 | body | SUBSTITUTED | `div#body` › `div.fundamentalsPanel` › `div.col-md-8.col-12` | 2 | 2 | 0.03 | structure-only |
| 7443 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.icon.ratio.ratio-16` › `div#footer` | 2 | 2 | 0.26 | structure-only |
| 7444 | body | SUBSTITUTED | `div.fundamentalsPanel` › `div.row` › `div.col-md-8.col-12` | 2 | 2 | 0.03 | structure-only |
| 7445 | body | SUBSTITUTED | `div.col-md-3.offset-md-0.col-1` › `img.img-fluid` › `p` | 2 | 2 | 0.02 | structure-only |
| 7446 | body | SUBSTITUTED | `div.row` › `div.col-md-4.col-12.paddingR` › `div.row` | 2 | 2 | 0.01 | structure-only |
| 7447 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.activity[number=3B]` | 2 | 2 | 0.48 | structure-only |
| 7448 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h4.center-text` › `ul` | 2 | 2 | 0.01 | structure-only |
| 7449 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p>b` › `p>b` | 2 | 2 | 0.20 | structure-only |
| 7450 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.activity.interactive[number=1B]` | 2 | 2 | 0.48 | structure-only |
| 7451 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert` › `div.col-md-6.col-12` | 2 | 2 | 0.30 | structure-only |
| 7452 | body | SUBSTITUTED | `div.col-12` › `h4` › `h5` | 2 | 2 | 0.16 | structure-only |
| 7453 | body | SUBSTITUTED | `div#body` › `div.fundamentalsPanel` › `div.row` | 2 | 2 | 0.03 | structure-only |
| 7454 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.activity[number=3D]` | 2 | 2 | 0.48 | structure-only |
| 7455 | body | SUBSTITUTED | `div.row` › `div.col-md-11.col-12` › `WIDGET` | 2 | 2 | 0.02 | structure-only |
| 7456 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row.flipCardsContainer` › `div.col-md-8.col-12` | 2 | 2 | 0.07 | structure-only |
| 7457 | body | SUBSTITUTED | `div.fundamentalsPanel` › `WIDGET` › `div.row` | 2 | 2 | 0.01 | structure-only |
| 7458 | body | SUBSTITUTED | `div.col-12` › `h4` › `WIDGET` | 2 | 2 | 0.16 | structure-only |
| 7459 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.table-responsive` › `div.col-md-8.col-12` | 2 | 2 | 0.08 | structure-only |
| 7460 | body | SUBSTITUTED | `div.row` › `WIDGET` › `div.row` | 2 | 2 | 0.02 | structure-only |
| 7461 | body | SUBSTITUTED | `div.col-md-10.col-12` › `img.img-fluid` › `img.img-fluid` | 2 | 2 | 0.01 | structure-only |
| 7462 | body | SUBSTITUTED | `div.col-12` › `h4` › `h4` | 2 | 2 | 0.16 | structure-only |
| 7463 | body | SUBSTITUTED | `div.col-md-4.col-12.paddingR` › `img.img-fluid` › `img.img-fluid` | 2 | 2 | 0.01 | structure-only |
| 7464 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.activity.interactive[number=7B]` | 2 | 2 | 0.48 | structure-only |
| 7465 | body | SUBSTITUTED | `div.row` › `div.col-md-6.offset-md-0.col-12.padd` › `div.col-md-6.col-12` | 2 | 2 | 0.01 | structure-only |
| 7466 | body | SUBSTITUTED | `div.row` › `div.col-md-6.offset-md-0.col-12.padd` › `div.col-md-6.col-12` | 2 | 2 | 0.02 | structure-only |
| 7467 | body | SUBSTITUTED | `div.row` › `div.col-md-4.col-12.paddingLR` › `div.row` | 2 | 2 | 0.02 | structure-only |
| 7468 | body | SUBSTITUTED | `a` › `div.button.externalButton` › `div.externalButton` | 2 | 2 | 0.01 | structure-only |
| 7469 | body | SUBSTITUTED | `p>b` › `b` › `a` | 2 | 2 | 0.27 | structure-only |
| 7470 | body | SUBSTITUTED | `div.col-12.choicePage.choiceHe` › `WIDGET` › `WIDGET` | 2 | 2 | 0.00 | structure-only |
| 7471 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.row.flipCardsContainer` | 2 | 2 | 0.85 | structure-only |
| 7472 | body | SUBSTITUTED | `p` › `br` › `div.col-md-4.col-12.paddingLR` | 2 | 2 | 0.14 | structure-only |
| 7473 | body | SUBSTITUTED | `div.col` › `WIDGET` › `p` | 2 | 2 | 0.02 | structure-only |
| 7474 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row` › `div.ratio.ratio-16x9` | 2 | 2 | 0.25 | structure-only |
| 7475 | body | SUBSTITUTED | `div.col-md-8.col-12.paddingR` › `h4` › `h3` | 2 | 2 | 0.01 | structure-only |
| 7476 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.TKmodal` › `WIDGET` | 2 | 2 | 0.01 | structure-only |
| 7477 | body | SUBSTITUTED | `div.row` › `div.col-4` › `div.row` | 2 | 2 | 0.02 | structure-only |
| 7478 | body | SUBSTITUTED | `div.row` › `div.col` › `WIDGET` | 2 | 2 | 0.02 | structure-only |
| 7479 | body | SUBSTITUTED | `p` › `br` › `span.infoTrigger` | 2 | 2 | 0.14 | structure-only |
| 7480 | body | SUBSTITUTED | `a` › `div.externalButton` › `div.ratio.ratio-16x9` | 2 | 2 | 0.08 | structure-only |
| 7481 | body | SUBSTITUTED | `div.col-md-8.col-12.paddingR` › `div.videoSection.icon.ratio.ratio-16` › `p>a` | 2 | 2 | 0.02 | structure-only |
| 7482 | body | SUBSTITUTED | `div.col-md-8.col-12` › `a` › `a` | 2 | 2 | 0.07 | structure-only |
| 7483 | body | SUBSTITUTED | `div#body` › `div.row` › `div#footer` | 2 | 2 | 0.94 | structure-only |
| 7484 | body | SUBSTITUTED | `div.col-md-4.offset-md-0.col-6` › `div.alertImage` › `div.col-md-8.col-12` | 2 | 2 | 0.01 | structure-only |
| 7485 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p>span.infoTrigger` › `WIDGET` | 2 | 2 | 0.14 | structure-only |
| 7486 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12` › `div.col-md-4.col-12.paddingLR` | 2 | 2 | 0.98 | structure-only |
| 7487 | body | SUBSTITUTED | `div.col-md-8.col-12.paddingR` › `WIDGET` › `div.col-md-6.col-12` | 2 | 2 | 0.03 | structure-only |
| 7488 | body | SUBSTITUTED | `div.row` › `div.col-md-3.col-12.paddingL` › `div.col-md-6.col-12` | 2 | 2 | 0.01 | structure-only |
| 7489 | body | SUBSTITUTED | `div.col-md-6.col-12.paddingLR` › `WIDGET` › `div.col-12` | 2 | 2 | 0.04 | structure-only |
| 7490 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.activity[number=4B]` | 2 | 2 | 0.48 | structure-only |
| 7491 | body | SUBSTITUTED | `div.row` › `div.col-4` › `div.col-12` | 2 | 2 | 0.02 | structure-only |
| 7492 | body | SUBSTITUTED | `div.alert.top` › `p>b` › `p>b` | 2 | 2 | 0.00 | structure-only |
| 7493 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `div.activity[number=4B]` | 2 | 2 | 0.40 | structure-only |
| 7494 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h5` › `WIDGET` | 2 | 2 | 0.05 | structure-only |
| 7495 | body | SUBSTITUTED | `div.alert.solid` › `p` › `p>b` | 2 | 2 | 0.01 | structure-only |
| 7496 | body | SUBSTITUTED | `div.row` › `div.row` › `div.button` | 2 | 2 | 0.07 | structure-only |
| 7497 | body | SUBSTITUTED | `ol` › `li>b` › `li>a.home-nav` | 2 | 2 | 0.02 | structure-only |
| 7498 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12.mt-3` › `div.col-md-8.col-12` | 2 | 2 | 0.00 | structure-only |
| 7499 | body | SUBSTITUTED | `div.alert` › `div.row` › `li>b` | 2 | 2 | 0.27 | structure-only |
| 7500 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.activity[number=4C]` | 2 | 2 | 0.48 | structure-only |
| 7501 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.activity.interactive[number=1D]` | 2 | 2 | 0.85 | structure-only |
| 7502 | body | SUBSTITUTED | `div.row.supervisor` › `div.col-md-4.offset-md-0.col-12` › `WIDGET` | 2 | 2 | 0.01 | structure-only |
| 7503 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `div.alert.solid` | 2 | 2 | 0.40 | structure-only |
| 7504 | body | SUBSTITUTED | `tr` › `th` › `th` | 2 | 2 | 0.04 | structure-only |
| 7505 | body | SUBSTITUTED | `div.alert.top` › `div.row` › `div.row` | 2 | 2 | 0.07 | structure-only |
| 7506 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h5` › `div.table-responsive` | 2 | 2 | 0.05 | structure-only |
| 7507 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.activity[number=7A]` | 2 | 2 | 0.85 | structure-only |
| 7508 | body | SUBSTITUTED | `div.col-md-8.col-12` › `br` › `h3` | 2 | 2 | 0.05 | structure-only |
| 7509 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row.flipCardsContainer` › `div.row` | 2 | 2 | 0.07 | structure-only |
| 7510 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12` › `div.alertActivity` | 2 | 2 | 0.98 | structure-only |
| 7511 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p>span.infoTrigger` › `p` | 2 | 2 | 0.14 | structure-only |
| 7512 | body | SUBSTITUTED | `div.col-12` › `h3` › `p>b` | 2 | 2 | 0.17 | structure-only |
| 7513 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `p>b` | 2 | 2 | 0.48 | structure-only |
| 7514 | body | SUBSTITUTED | `div.captionTrigger` › `img.img-fluid` › `div.col-12` | 2 | 2 | 0.01 | structure-only |
| 7515 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.clickDropContent` › `div.TKmodal` | 2 | 2 | 0.08 | structure-only |
| 7516 | body | SUBSTITUTED | `div.row` › `div.col-md-6.col-12` › `WIDGET` | 2 | 2 | 0.02 | structure-only |
| 7517 | body | SUBSTITUTED | `div.alert` › `p` › `div.externalButton` | 2 | 2 | 0.06 | structure-only |
| 7518 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h4` › `div.whakatauki` | 2 | 2 | 0.19 | structure-only |
| 7519 | body | SUBSTITUTED | `div.clickDropContent` › `p` › `tr` | 2 | 2 | 0.08 | structure-only |
| 7520 | body | SUBSTITUTED | `div.row` › `div.col-md-4.col-12` › `li` | 2 | 2 | 0.05 | structure-only |
| 7521 | body | SUBSTITUTED | `table.table.table-bordered` › `tr` › `td` | 2 | 2 | 0.04 | structure-only |
| 7522 | body | SUBSTITUTED | `div.table-responsive` › `table.table.table-bordered` › `tr` | 2 | 2 | 0.04 | structure-only |
| 7523 | body | SUBSTITUTED | `div.col-md-8.col-12.paddingR` › `WIDGET` › `p` | 2 | 2 | 0.03 | structure-only |
| 7524 | body | SUBSTITUTED | `div.TKmodal` › `div.row` › `div.row` | 2 | 2 | 0.00 | structure-only |
| 7525 | body | SUBSTITUTED | `div.hoverContent` › `div.shapeContent` › `tr` | 2 | 2 | 0.02 | structure-only |
| 7526 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.whakatauki` › `p>i` | 2 | 2 | 0.06 | structure-only |
| 7527 | body | SUBSTITUTED | `div.whakatauki` › `p` › `li` | 2 | 2 | 0.10 | structure-only |
| 7528 | body | SUBSTITUTED | `tr` › `td>b` › `th` | 2 | 2 | 0.02 | structure-only |
| 7529 | body | SUBSTITUTED | `div.row` › `div.row` › `div.activity` | 2 | 2 | 0.07 | structure-only |
| 7530 | body | SUBSTITUTED | `div.col-md-4.offset-md-0.col-1` › `div.alert.top` › `div.alert` | 2 | 2 | 0.04 | structure-only |
| 7531 | body | SUBSTITUTED | `div.col-md-4.offset-md-0.col-1` › `div.alert.top` › `div.activity` | 2 | 2 | 0.04 | structure-only |
| 7532 | body | SUBSTITUTED | `div.alert.top` › `div.row` › `p` | 2 | 2 | 0.07 | structure-only |
| 7533 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.activity.interactive[number=4D]` | 2 | 2 | 0.85 | structure-only |
| 7534 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p.quoteText` › `ul` | 2 | 2 | 0.03 | structure-only |
| 7535 | body | SUBSTITUTED | `div.row` › `div.col-md-6.offset-md-0.col-12.padd` › `div.col-md-8.col-12` | 2 | 2 | 0.02 | structure-only |
| 7536 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.activity[number=1C]` | 2 | 2 | 0.85 | structure-only |
| 7537 | body | SUBSTITUTED | `div.row` › `div.col-md-4.offset-md-0.col-12` › `div.videoSection.icon.ratio.ratio-16` | 2 | 2 | 0.21 | structure-only |
| 7538 | body | SUBSTITUTED | `div.row` › `div.col-md-4.offset-md-0.col-12.padd` › `div.row` | 2 | 2 | 0.00 | structure-only |
| 7539 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h1` › `h3` | 2 | 2 | 0.00 | structure-only |
| 7540 | body | SUBSTITUTED | `div.row.justify-content-center` › `div.col-md-3.col-6` › `div.phaseLink` | 2 | 2 | 0.00 | structure-only |
| 7541 | body | SUBSTITUTED | `div.col-md-3.col-6` › `div.phaseLink` › `h3` | 2 | 2 | 0.02 | structure-only |
| 7542 | body | SUBSTITUTED | `div.col-md-3.col-6` › `div.phaseLink` › `img.phaseImg` | 2 | 2 | 0.02 | structure-only |
| 7543 | body | SUBSTITUTED | `div.fundamentalsPanel` › `div.row` › `div.table-responsive` | 2 | 2 | 0.03 | structure-only |
| 7544 | body | SUBSTITUTED | `div.col-md-11.col-12` › `div.row.flipCardsContainer` › `WIDGET` | 2 | 2 | 0.01 | structure-only |
| 7545 | body | SUBSTITUTED | `div.col-md-4.col-12` › `img.img-fluid` › `img.img-fluid` | 2 | 2 | 0.02 | structure-only |
| 7546 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.shapeHover` › `img.img-fluid` | 2 | 2 | 0.01 | structure-only |
| 7547 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.clickDropContent` › `div.row` | 2 | 2 | 0.08 | structure-only |
| 7548 | body | SUBSTITUTED | `div.fundamentalsPanel` › `div.row` › `div.button` | 2 | 2 | 0.03 | structure-only |
| 7549 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.activity[number=7C]` | 2 | 2 | 0.48 | structure-only |
| 7550 | body | SUBSTITUTED | `div#body` › `div.col-md-12.col-12` › `div.row` | 2 | 2 | 0.00 | structure-only |
| 7551 | body | SUBSTITUTED | `div.row` › `div.offset-md-2.col-md-8.col-12` › `div.col-12` | 2 | 2 | 0.00 | structure-only |
| 7552 | body | SUBSTITUTED | `div.col-md-12.col-12` › `div.whakatauki` › `div.row` | 2 | 2 | 0.04 | structure-only |
| 7553 | body | SUBSTITUTED | `div.row` › `div.col-md-4.offset-md-0.col-12` › `div.externalButton` | 2 | 2 | 0.21 | structure-only |
| 7554 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.table-responsive` › `div.videoSection.ratio.ratio-16x9` | 2 | 2 | 0.08 | structure-only |
| 7555 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.activity[number=6B]` | 2 | 2 | 0.85 | structure-only |
| 7556 | body | SUBSTITUTED | `mfrac` › `mn` › `mrow` | 2 | 2 | 0.01 | structure-only |
| 7557 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row.margB2` › `div.table-responsive` | 2 | 2 | 0.00 | structure-only |
| 7558 | body | SUBSTITUTED | `math` › `mfrac` › `math` | 2 | 2 | 0.02 | structure-only |
| 7559 | body | SUBSTITUTED | `mfrac` › `mn` › `mfrac` | 2 | 2 | 0.01 | structure-only |
| 7560 | body | SUBSTITUTED | `div.row.supervisor` › `div.col-md-8.col-12.super-content-bu` › `div.col-md-8.col-12.super-content-bu` | 2 | 2 | 0.00 | structure-only |
| 7561 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.activity[number=2A]` | 2 | 2 | 0.48 | structure-only |
| 7562 | body | SUBSTITUTED | `div.row.supervisor` › `div.col-md-8.col-12.super-content-bu` › `div.col-md-8.col-12` | 2 | 2 | 0.00 | structure-only |
| 7563 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.activity[number=8A]` | 2 | 2 | 0.85 | structure-only |
| 7564 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.embedPDF[layout=portrait]` › `div.ratio.ratio-16x9` | 2 | 2 | 0.00 | structure-only |
| 7565 | body | SUBSTITUTED | `div.row` › `div.col-md-4.offset-md-0.col-12.padd` › `div.videoSection.ratio.ratio-16x9` | 2 | 2 | 0.14 | structure-only |
| 7566 | body | SUBSTITUTED | `tr.rowSolid.primary-light` › `th` › `td>b` | 2 | 2 | 0.00 | structure-only |
| 7567 | body | SUBSTITUTED | `p` › `img.img-fluid` › `img.img-fluid` | 2 | 2 | 0.01 | structure-only |
| 7568 | body | SUBSTITUTED | `li` › `p` › `p` | 2 | 2 | 0.00 | structure-only |
| 7569 | body | SUBSTITUTED | `div.col-md-4.offset-md-0.col-1` › `div.alertActivity` › `p` | 2 | 2 | 0.09 | structure-only |
| 7570 | body | SUBSTITUTED | `div.row` › `div.col-md-3.offset-md-0.col-12.padd` › `div.table-responsive` | 2 | 2 | 0.02 | structure-only |
| 7571 | body | SUBSTITUTED | `ul` › `li` › `li>a#prev-lesson` | 2 | 2 | 0.35 | structure-only |
| 7572 | body | SUBSTITUTED | `ul` › `li` › `li>a#next-lesson` | 2 | 2 | 0.35 | structure-only |
| 7573 | body | SUBSTITUTED | `ul` › `li` › `li>a.home-nav` | 2 | 2 | 0.35 | structure-only |
| 7574 | body | SUBSTITUTED | `p` › `br` › `tr` | 2 | 2 | 0.14 | structure-only |
| 7575 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.activity.interactive[number=1D]` | 2 | 2 | 0.48 | structure-only |
| 7576 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h4` › `div.activity[number=3A]` | 2 | 2 | 0.19 | structure-only |
| 7577 | body | SUBSTITUTED | `tr` › `th` › `WIDGET` | 2 | 2 | 0.04 | structure-only |
| 7578 | body | SUBSTITUTED | `div.row.flipCardsContainer` › `div.col-md-4.col-12.paddingLR` › `li` | 2 | 2 | 0.05 | structure-only |
| 7579 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.activity[number=7B]` | 2 | 2 | 0.48 | structure-only |
| 7580 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.activity[number=9C]` | 2 | 2 | 0.48 | structure-only |
| 7581 | body | SUBSTITUTED | `div.alert.top` › `div.row` › `table.table.table-bordered` | 2 | 2 | 0.07 | structure-only |
| 7582 | body | SUBSTITUTED | `div.col-12` › `p` › `th` | 2 | 2 | 0.26 | structure-only |
| 7583 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `div.activity.interactive[number=1A]` | 2 | 2 | 0.40 | structure-only |
| 7584 | body | SUBSTITUTED | `div.col-md-6.offset-md-0.col-1` › `p` › `p` | 2 | 2 | 0.00 | structure-only |
| 7585 | body | SUBSTITUTED | `div.table-responsive` › `table.table.table-bordered.table-fix` › `table.table.table-bordered` | 2 | 2 | 0.00 | structure-only |
| 7586 | body | SUBSTITUTED | `p` › `b` › `iframe` | 2 | 2 | 0.18 | structure-only |
| 7587 | body | SUBSTITUTED | `div.row` › `div.col-md-4.offset-md-0.col-12` › `div.button` | 2 | 2 | 0.21 | structure-only |
| 7588 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.col-md-12.col-12` › `p>i` | 2 | 2 | 0.03 | structure-only |
| 7589 | body | SUBSTITUTED | `div.col-md-8.col-12.paddingR` › `div.row` › `WIDGET` | 2 | 2 | 0.01 | structure-only |
| 7590 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.activity.interactive[number=2A]` | 2 | 2 | 0.85 | structure-only |
| 7591 | body | SUBSTITUTED | `div.row` › `div.row` › `li>a#prev-lesson` | 2 | 2 | 0.07 | structure-only |
| 7592 | body | SUBSTITUTED | `div#body` › `div.introduction` › `div` | 2 | 2 | 0.02 | structure-only |
| 7593 | body | SUBSTITUTED | `div.row.phaseContainer` › `div.col-md-3.col-6` › `div.col-md-8.col-12` | 2 | 2 | 0.02 | structure-only |
| 7594 | body | SUBSTITUTED | `div.phaseLink` › `img.phaseImg` › `p` | 2 | 2 | 0.02 | structure-only |
| 7595 | body | SUBSTITUTED | `div.shapeHover` › `div.outerContent` › `WIDGET` | 2 | 2 | 0.01 | structure-only |
| 7596 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.shapeHover[layout=clockwise]` › `h4` | 2 | 2 | 0.01 | structure-only |
| 7597 | body | SUBSTITUTED | `div.outerContent` › `div.shape` › `WIDGET` | 2 | 2 | 0.02 | structure-only |
| 7598 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `div.activity[number=3A]` | 2 | 2 | 0.40 | structure-only |
| 7599 | body | SUBSTITUTED | `p>span.audioTrigger` › `span.audioTrigger` › `b` | 2 | 2 | 0.00 | structure-only |
| 7600 | body | SUBSTITUTED | `div.col-12` › `div.row` › `p` | 2 | 2 | 0.02 | structure-only |
| 7601 | body | SUBSTITUTED | `div.row.flipCardsContainer` › `div.col-md-4.col-12.paddingLR` › `div.col-md-6.col-sm-6.col-12.padding` | 2 | 2 | 0.05 | structure-only |
| 7602 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.youtubeShort.ratio.` › `div.videoSection.ratio.ratio-16x9` | 2 | 2 | 0.01 | structure-only |
| 7603 | body | SUBSTITUTED | `div.row` › `div.col-md-4.col-12.offset-md-4` › `WIDGET` | 2 | 2 | 0.00 | structure-only |
| 7604 | body | SUBSTITUTED | `div.col-md-4.col-12.offset-md-` › `WIDGET` › `WIDGET` | 2 | 2 | 0.00 | structure-only |
| 7605 | body | SUBSTITUTED | `div.col-md-4.col-12` › `WIDGET` › `div.clickDropContent` | 2 | 2 | 0.01 | structure-only |
| 7606 | body | SUBSTITUTED | `div.col-md-4.col-12` › `img.img-fluid` › `ul` | 2 | 2 | 0.02 | structure-only |
| 7607 | body | SUBSTITUTED | `div.row` › `div.col-md-4.col-12.offset-md-4` › `div.clickDropContent` | 2 | 2 | 0.00 | structure-only |
| 7608 | body | SUBSTITUTED | `div.col-md-4.col-12.offset-md-` › `WIDGET` › `p>b` | 2 | 2 | 0.00 | structure-only |
| 7609 | body | SUBSTITUTED | `ul` › `li` › `p>b` | 2 | 2 | 0.35 | structure-only |
| 7610 | body | SUBSTITUTED | `div.clickDropContent` › `ul` › `div.clickDropContent` | 2 | 2 | 0.02 | structure-only |
| 7611 | body | SUBSTITUTED | `div.col-12` › `p.marg0` › `p` | 2 | 2 | 0.00 | structure-only |
| 7612 | body | SUBSTITUTED | `div.col-md-4.offset-md-0.col-1` › `WIDGET` › `ul` | 2 | 2 | 0.01 | structure-only |
| 7613 | body | SUBSTITUTED | `div.clickDropContent` › `ul` › `ul` | 2 | 2 | 0.02 | structure-only |
| 7614 | body | SUBSTITUTED | `div.table-responsive` › `table.table.noHover.center-text` › `WIDGET` | 2 | 2 | 0.00 | structure-only |
| 7615 | body | SUBSTITUTED | `td` › `WIDGET` › `div.clickDropContent` | 2 | 2 | 0.00 | structure-only |
| 7616 | body | SUBSTITUTED | `div.col-12` › `div.button.TKmodalButton` › `div.row` | 2 | 2 | 0.00 | structure-only |
| 7617 | body | SUBSTITUTED | `div.row.flipCardsContainer` › `div.col-sm-6.col-12.paddingLR` › `div.col-md-4.col-12.paddingLR` | 2 | 2 | 0.00 | structure-only |
| 7618 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.ratio.ratio-16x9` › `h5` | 2 | 2 | 0.21 | structure-only |
| 7619 | body | SUBSTITUTED | `div.col-md-4.offset-md-0.col-1` › `WIDGET` › `p` | 2 | 2 | 0.01 | structure-only |
| 7620 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `div.activity[number=5B]` | 2 | 2 | 0.48 | structure-only |
| 7621 | body | SUBSTITUTED | `div.col-md-8.col-12` › `WIDGET` › `div.activity[number=1A]` | 2 | 2 | 0.40 | structure-only |
| 7622 | body | SUBSTITUTED | `div.col-md-8.col-12` › `a` › `p>b` | 2 | 2 | 0.07 | structure-only |
| 7623 | body | SUBSTITUTED | `ul` › `li` › `li>b` | 2 | 2 | 0.35 | structure-only |
| 7624 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.videoSection.icon.ratio.ratio-16` › `div.activity` | 2 | 2 | 0.26 | structure-only |
| 7625 | body | SUBSTITUTED | `div.col-md-4.col-12` › `div.alert.top` › `div.col-md-8.col-12` | 2 | 2 | 0.01 | structure-only |
| 7626 | body | SUBSTITUTED | `div.col-md-3.col-12.paddingLR` › `WIDGET` › `WIDGET` | 2 | 2 | 0.01 | structure-only |
| 7627 | body | SUBSTITUTED | `div.clickDropContent` › `p>b` › `div.clickDropContent` | 2 | 2 | 0.02 | structure-only |
| 7628 | body | SUBSTITUTED | `div.clickDropContent` › `p>b` › `p>b` | 2 | 2 | 0.02 | structure-only |
| 7629 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.activity.dropbox[number=2F]` | 2 | 2 | 0.85 | structure-only |
| 7630 | body | SUBSTITUTED | `div` › `p` › `p` | 2 | 2 | 0.02 | structure-only |
| 7631 | body | SUBSTITUTED | `div.row` › `div.col-md-8.col-12.paddingR` › `p` | 2 | 2 | 0.14 | structure-only |
| 7632 | body | SUBSTITUTED | `div.col-md-4.offset-md-0.col-1` › `div.alertActivity` › `div.row` | 2 | 2 | 0.09 | structure-only |
| 7633 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row.flipCardsContainer` › `p>b` | 2 | 2 | 0.07 | structure-only |
| 7634 | body | SUBSTITUTED | `div.row.flipCardsContainer` › `div.col-md-4.col-12.paddingLR` › `div.button` | 2 | 2 | 0.05 | structure-only |
| 7635 | body | SUBSTITUTED | `div.col-md-8.col-12` › `ul` › `p>b` | 2 | 2 | 0.23 | structure-only |
| 7636 | body | SUBSTITUTED | `div.row` › `div.col` › `div.table-responsive` | 2 | 2 | 0.02 | structure-only |
| 7637 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.row.flipCardsContainer` › `div.activity.interactive[number=1A]` | 2 | 2 | 0.07 | structure-only |
| 7638 | body | SUBSTITUTED | `div.row.flipCardsContainer` › `div.col-md-6.col-6.paddingLR` › `div.row` | 2 | 2 | 0.00 | structure-only |
| 7639 | body | SUBSTITUTED | `div.col-md-6.col-6.paddingLR` › `WIDGET` › `div.col-12` | 2 | 2 | 0.00 | structure-only |
| 7640 | body | SUBSTITUTED | `a` › `div.externalButton` › `li` | 2 | 2 | 0.08 | structure-only |
| 7641 | body | SUBSTITUTED | `p` › `span.infoTrigger` › `li` | 2 | 2 | 0.09 | structure-only |
| 7642 | body | SUBSTITUTED | `div.col-md-8.col-12.super-cont` › `div.super-content.row` › `div.row` | 2 | 2 | 0.05 | structure-only |
| 7643 | body | SUBSTITUTED | `div.col-md-8.col-12` › `h3` › `audio.audioPlayer.icon` | 2 | 2 | 0.48 | structure-only |
| 7644 | body | SUBSTITUTED | `div.col-md-8.col-12.choicePage` › `WIDGET` › `div.row` | 2 | 2 | 0.03 | structure-only |
| 7645 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert` › `div.clickDropContent.activity.dropbo` | 2 | 2 | 0.30 | structure-only |
| 7646 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.alert` › `div.clickDropContent.activity.dropbo` | 2 | 2 | 0.30 | structure-only |
| 7647 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.clickDropContent.activity.dropbo` | 2 | 2 | 0.85 | structure-only |
| 7648 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.clickDropContent.activity.dropbo` | 2 | 2 | 0.85 | structure-only |
| 7649 | body | SUBSTITUTED | `div.col-md-8.col-12` › `p` › `div.clickDropContent.activity.dropbo` | 2 | 2 | 0.85 | structure-only |
| 7650 | body | SUBSTITUTED | `div.col-12` › `p.margB0` › `WIDGET` | 2 | 2 | 0.04 | structure-only |
| 7651 | body | SUBSTITUTED | `div.col-md-8.col-12` › `div.whakatauki` › `audio.audioPlayer.icon` | 2 | 2 | 0.06 | structure-only |
| 7652 | body | SUBSTITUTED | `div.row` › `div.col.choicePage.imgHeadVis.choice` › `div.col-md-8.col-12` | 2 | 2 | 0.00 | structure-only |
| 7653 | body | SUBSTITUTED | `div.col-md-8.col-12` › `a` › `p>a` | 2 | 2 | 0.07 | structure-only |
| 7654 | body | SUBSTITUTED | `div.col` › `WIDGET` › `tr` | 2 | 2 | 0.02 | structure-only |
| 7655 | body | SUBSTITUTED | `div.col` › `WIDGET` › `img.img-fluid` | 2 | 2 | 0.02 | structure-only |
| 10908 | root | MISSING | `body.container-fluid` › `div.row` › `—` | 195 | 172 | 0.13 | 1.00 |
| 10909 | root | SUBSTITUTED | `#root` › `body.container-fluid.mathJax` › `body.container-fluid` | 62 | 16 | 0.05 | structure-only |
| 10910 | root | SUBSTITUTED | `#root` › `body.inquiry.container-fluid` › `body.container-fluid` | 15 | 14 | 0.03 | structure-only |
| 10911 | root | EXTRA | `body.fundamentals.container-fl` › `—` › `div.row` | 14 | 14 | 0.98 | structure-only |
| 10913 | root | MISSING | `html.notranslate` › `head` › `—` | 95 | 10 | 0.05 | 0.00 |
| 10914 | root | EXTRA | `body.container-fluid.reoTransl` › `—` › `div.row` | 10 | 10 | 0.99 | structure-only |
| 10915 | root | SUBSTITUTED | `#root` › `body.container-fluid` › `body.container-fluid.mathJax` | 11 | 8 | 0.81 | structure-only |
| 10916 | root | MISSING | `body.container-fluid.reoTransl` › `div.row` › `—` | 10 | 8 | 0.01 | structure-only |
| 10917 | root | MISSING | `html.notranslate` › `div.row` › `—` | 8 | 8 | 0.01 | structure-only |
| 10918 | root | MISSING | `body.container-fluid` › `div.col-md-8.col-12` › `—` | 7 | 7 | 0.00 | structure-only |
| 10919 | root | MISSING | `body.container-fluid.mathJax` › `div.row` › `—` | 7 | 7 | 0.00 | 1.00 |
| 10920 | root | EXTRA | `body.inquiry.container-fluid` › `—` › `div.row` | 4 | 4 | 0.98 | structure-only |
| 10921 | root | EXTRA | `div.row` › `—` › `div.col-md-8.col-12` | 3 | 3 | 0.83 | structure-only |
| 10922 | root | EXTRA | `body.container-fluid.mathJax` › `—` › `div.row` | 3 | 3 | 1.00 | structure-only |
| 10923 | root | MISSING | `body.inquiry.container-fluid` › `div.row` › `—` | 3 | 3 | 0.01 | structure-only |
| 10924 | root | SUBSTITUTED | `#root` › `body.container-fluid` › `body.fundamentals.container-fluid` | 8 | 2 | 0.81 | structure-only |
| 10925 | root | MOVED | `ul` › `li` › `li` | 2 | 2 | 0.00 | structure-only |
| 10926 | root | SUBSTITUTED | `body.container-fluid` › `div.row` › `div.row` | 2 | 2 | 0.13 | structure-only |
| 10927 | root | SUBSTITUTED | `div.row` › `div.col-md-8.col-12` › `div.col-md-8.col-12` | 2 | 2 | 0.17 | structure-only |
| 10928 | root | SUBSTITUTED | `#root` › `body.fundamentals.container-fluid` › `body.inquiry.container-fluid` | 2 | 2 | 0.03 | structure-only |

(7639 single-module classes are in the JSON only.)
