# DIFF_QUEUE.md — the diff miner's ranked class queue (LOOP__Autonomous_Rounds.md §1d)

**Produced:** 2026-09-17 12:23 NZST by `reference/tests/_diff_miner.py` on the CURRENT corpus (pageforge-site HEAD a7401ed; Claude corpus 416 dirs). **Population:** the skeleton gate's own — 1956 paired pages / 405 modules (compare_exclusions.txt honoured; acks / glossary / references pages excluded); parse errors skipped: 0 (must be 0); modules without a parsed WT: 2. Run time 73.0 s.

**What a row is.** One CLASS = (region, parent element, gold form, Claude form, direction) over every differing skeleton line of every paired page — the same lines, labels, widget collapse and difflib alignment the PRIMARY gate scores (each element its own line so it can be quoted). Direction: MISSING = gold has it, Claude lacks it; EXTRA = Claude has it, gold lacks it; SUBSTITUTED = same position, different tag / class / wrapper; MOVED = same text, different place. Consensus = of the gold pages in the group where the region exists, the share carrying the gold form (for EXTRA: the share NOT carrying Claude's form). Derivable = the gold line's text is in the module's parsed Writers Template (round-110 tolerance); structure-only differences are always derivable.

**Candidate rule (§1d).** modules ≥ 10 for a chrome class (module-code / title / header / module-menu / crumbs / phases-nav / footer / acks), pages ≥ 20 for a body / activity class; gold consensus ≥ 0.60 in at least one template or subject group that itself reaches the floor; structure-only or derivable share ≥ 0.60. A class below the floor is listed, never dropped. A CANDIDATE still goes through the PICK's KB-first check, the triangulation and the §3 corpus-wide measurement before any code — this table is the queue, not the verdict.

## Summary

- differing skeleton lines: 236712 — by direction {'MISSING': 121718, 'SUBSTITUTED': 21129, 'EXTRA': 85696, 'MOVED': 8169}
- by region: {'module-code': 17, 'title': 253, 'header': 6, 'module-menu': 11990, 'phases-nav': 48, 'crumbs': 180, 'footer': 2093, 'acks': 1175, 'activity': 85383, 'body': 133675, 'root': 1892}
- classes: 11025 — CANDIDATE 166, below floor 10636, the rest below consensus / not derivable

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

### F5 · EXTRA `header:chip=lesson-number` — CANDIDATE (pages 76 / modules 33)
- by template+ptype: Standard/lesson 31m/72p gold 0.26 Claude 0.23 c=0.74; Bilingual/lesson 2m/4p gold 0.02 Claude 0.11 c=0.98
- by subject: 1-10 Blended Literacy 22m/44p gold 0.24 Claude 0.37 c=0.76; Leaving to Learn 5m/15p gold 0.40 Claude 0.30 c=0.60; 1-10 English 2m/9p gold 0.22 Claude 0.18 c=0.78; Te Marautanga o Aotearoa TMoA 2m/4p gold 0.02 Claude 0.08 c=0.98; ConnectED 1m/1p gold 0.07 Claude 0.07 c=0.94; 1-10 Mathematics 1m/3p gold 0.10 Claude 0.11 c=0.90
- **BLL141** BLL141_1_0.html ↔ BLL141-1.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- **BLL142** BLL142_1_0.html ↔ BLL142-1.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- **BLL143** BLL143_1_0.html ↔ BLL143-1.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- modules: BLL141, BLL142, BLL143, BLL144, BLL145, BLL146, BLL147, BLL151, BLL152, BLL154, BLL156, BLL157, BLL161, BLL162, BLL163, BLL164, BLL165, BLL166, BLL167, BLL171, BLL172, BLL173, CEDR501, ENGJ101 …

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

### F35 · MISSING `footer:ul=footer-nav` — CANDIDATE (pages 75 / modules 26)
- by template+ptype: Standard/lesson 14m/36p gold 0.89 Claude 0.87 c=0.89; Standard/overview 11m/11p gold 0.74 Claude 0.70 c=0.74; Fundamentals/overview 8m/8p gold 0.49 Claude 0.38 c=0.49; Inquiry/overview 3m/3p gold 0.17 Claude 0.14 c=0.17; Inquiry/lesson 3m/17p gold 0.96 Claude 0.61 c=0.96
- by subject: 1-10 Blended Literacy 12m/41p gold 0.16 Claude 0.00 c=0.16; 1-10 Technology 5m/5p gold 0.62 Claude 0.00 c=0.62; ConnectED 4m/21p gold 0.87 Claude 0.69 c=0.87; EXPlore 2m/5p gold 0.53 Claude 0.27 c=0.53; 1-10 Mathematics 2m/2p gold 0.98 Claude 0.99 c=0.98; 1-10 Health and PE 1m/1p gold 0.27 Claude 0.20 c=0.27
- **BLL121** BLL121_0_0.html ↔ BLL121-01.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL172** BLL172_0_0.html ↔ BLL172-00.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL174** BLL174_0_0.html ↔ BLL174-00.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL121, BLL172, BLL174, BLL175, BLL176, BLL177, BLL236, BLL237, BLL240, BLL241, BLL244, BLL245, CEDR501, CEDT207, CEDT301, CEDW101, EXBP901, EXIP901, HPFUN301, MXFUN02, MXFUN03, TEFUN01, TEFUN02, TEFUN05 …

### F37 · EXTRA `footer:ul=footer-nav inquiry-nav` — CANDIDATE (pages 75 / modules 21)
- by template+ptype: Standard/lesson 15m/41p gold 0.10 Claude 0.13 c=0.90; Standard/overview 12m/12p gold 0.26 Claude 0.30 c=0.74; Inquiry/overview 3m/3p gold 0.83 Claude 0.86 c=0.17; Inquiry/lesson 3m/17p gold 0.04 Claude 0.39 c=0.96; Fundamentals/overview 2m/2p gold 0.00 Claude 0.04 c=1.00
- by subject: 1-10 Blended Literacy 12m/41p gold 0.84 Claude 1.00 c=0.16; ConnectED 4m/21p gold 0.13 Claude 0.31 c=0.87; EXPlore 2m/5p gold 0.47 Claude 0.73 c=0.53; 1-10 Mathematics 2m/2p gold 0.02 Claude 0.01 c=0.98; Leaving to Learn 1m/6p gold 0.02 Claude 0.04 c=0.98
- **BLL121** BLL121_0_0.html ↔ BLL121-01.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL172** BLL172_0_0.html ↔ BLL172-00.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL174** BLL174_0_0.html ↔ BLL174-00.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL121, BLL172, BLL174, BLL175, BLL176, BLL177, BLL236, BLL237, BLL240, BLL241, BLL244, BLL245, CEDR501, CEDT207, CEDT301, CEDW101, EXBP901, EXIP901, MXFUN02, MXFUN03, XWHA02

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
| 534 | activity | MISSING | `div.col-12` | `p` | `—` | 687 | 294 | 0.31 of 1950 | subject+ptype=1-10 Blended Literacy/lesson c=0.78 n=106 | 0.83 | — | CANDIDATE |
| 535 | activity | EXTRA | `div.col-12` | `—` | `p` | 471 | 240 | 0.88 of 1950 | series=XDLS90 c=1.00 n=21 | structure | — | CANDIDATE |
| 537 | activity | MISSING | `div.col-12` | `a` | `—` | 422 | 206 | 0.29 of 1950 | series=HIS10 c=0.71 n=41 | 0.65 | — | CANDIDATE |
| 538 | activity | MISSING | `a` | `div.button` | `—` | 528 | 195 | 0.23 of 1950 | series=HIS10 c=0.71 n=36 | 0.63 | yes | CANDIDATE |
| 539 | activity | MISSING | `div.col-12` | `h3` | `—` | 368 | 169 | 0.32 of 1950 | template+ptype=Fundamentals/overview c=0.87 n=23 | 0.74 | — | CANDIDATE |
| 540 | activity | MOVED | `div.col-12` | `p` | `p` | 279 | 151 | 0.19 of 1950 | template+ptype=Fundamentals/overview c=0.62 n=20 | structure | — | CANDIDATE |
| 541 | activity | EXTRA | `div.col-12` | `—` | `WIDGET` | 232 | 151 | 0.82 of 1950 | subject=1-10 English c=0.92 n=35 | structure | — | CANDIDATE |
| 543 | activity | EXTRA | `div.row` | `—` | `div.col-12` | 154 | 109 | 0.89 of 1950 | template=Standard c=0.92 n=128 | structure | — | CANDIDATE |
| 544 | activity | EXTRA | `div.col-12` | `—` | `p>a` | 126 | 104 | 1.00 of 1950 | subject+ptype=1-10 Blended Literacy/lesson c=1.00 n=33 | structure | — | CANDIDATE |
| 546 | activity | EXTRA | `div.col-12` | `—` | `img.img-fluid` | 138 | 92 | 0.97 of 1950 | template=Standard c=0.98 n=92 | structure | — | CANDIDATE |
| 549 | activity | MOVED | `div.col-12` | `h3` | `h3` | 100 | 82 | 0.23 of 1950 | subject+ptype=1-10 Blended Literacy/lesson c=0.77 n=24 | structure | — | CANDIDATE |
| 551 | activity | EXTRA | `div.col-12` | `—` | `ul` | 93 | 77 | 0.94 of 1950 | subject=1-10 Blended Literacy c=0.96 n=22 | structure | — | CANDIDATE |
| 552 | activity | EXTRA | `div.col-12` | `—` | `p>b` | 108 | 75 | 0.97 of 1950 | template=Standard c=0.98 n=75 | structure | — | CANDIDATE |
| 554 | activity | EXTRA | `div.col-12` | `—` | `ol` | 105 | 74 | 0.96 of 1950 | template=Standard c=0.97 n=87 | structure | — | CANDIDATE |
| 556 | activity | SUBSTITUTED | `div.col-12` | `p` | `p` | 90 | 68 | 0.76 of 1950 | template+ptype=Standard/lesson c=0.89 n=63 | structure | — | CANDIDATE |
| 558 | activity | EXTRA | `div.col-12` | `—` | `h3` | 91 | 67 | 0.86 of 1950 | template=Standard c=0.91 n=54 | structure | — | CANDIDATE |
| 560 | activity | EXTRA | `p>a` | `—` | `a` | 72 | 63 | 0.98 of 1950 | subject+ptype=1-10 Blended Literacy/lesson c=1.00 n=27 | structure | — | CANDIDATE |
| 561 | activity | EXTRA | `p>b` | `—` | `b` | 82 | 59 | 0.93 of 1950 | template=Standard c=0.94 n=54 | structure | — | CANDIDATE |
| 565 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `div.row` | 63 | 53 | 0.60 of 1950 | ptype=lesson c=0.70 n=56 | structure | — | CANDIDATE |
| 566 | activity | EXTRA | `div.col-12` | `—` | `h4.goJournal` | 122 | 52 | 0.95 of 1950 | series=HIS10 c=1.00 n=33 | structure | — | CANDIDATE |
| 570 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `p` | 56 | 50 | 0.60 of 1950 | subject+ptype=1-10 Mathematics/lesson c=0.78 n=22 | structure | — | CANDIDATE |
| 572 | activity | EXTRA | `ol` | `—` | `li` | 67 | 49 | 0.96 of 1950 | template=Standard c=0.97 n=53 | structure | — | CANDIDATE |
| 573 | activity | SUBSTITUTED | `div.col-12` | `a` | `h4.goJournal` | 109 | 48 | 0.57 of 1950 | series=HIS10 c=0.83 n=20 | structure | — | CANDIDATE |
| 574 | activity | EXTRA | `div.col-12` | `—` | `a` | 80 | 48 | 0.86 of 1950 | template=Standard c=0.87 n=72 | structure | — | CANDIDATE |
| 576 | activity | SUBSTITUTED | `div.col-12` | `p` | `WIDGET` | 62 | 48 | 0.76 of 1950 | subject+ptype=1-10 English/lesson c=0.93 n=21 | structure | — | CANDIDATE |
| 577 | activity | EXTRA | `a` | `—` | `div.button` | 82 | 47 | 0.77 of 1950 | series=XDLS90 c=0.92 n=31 | structure | yes | CANDIDATE |
| 579 | activity | EXTRA | `div.col-12` | `—` | `p>i` | 48 | 42 | 0.97 of 1950 | template=Standard c=0.98 n=40 | structure | — | CANDIDATE |
| 583 | activity | EXTRA | `p>i` | `—` | `i` | 46 | 40 | 0.96 of 1950 | template=Standard c=0.97 n=44 | structure | — | CANDIDATE |
| 584 | activity | SUBSTITUTED | `div.col-12` | `a` | `p` | 51 | 38 | 0.57 of 1950 | template+ptype=Standard/lesson c=0.68 n=50 | structure | — | CANDIDATE |
| 593 | activity | SUBSTITUTED | `div.col-12` | `h3` | `WIDGET` | 52 | 34 | 0.76 of 1950 | subject+ptype=1-10 Mathematics/lesson c=0.95 n=21 | structure | — | CANDIDATE |
| 596 | activity | EXTRA | `div.col-12` | `—` | `div.videoSection.ratio.ratio-16x9` | 42 | 30 | 0.99 of 1950 | template=Standard c=0.99 n=32 | structure | yes | CANDIDATE |
| 597 | activity | EXTRA | `ul` | `—` | `li` | 31 | 30 | 0.93 of 1950 | template=Standard c=0.95 n=26 | structure | — | CANDIDATE |
| 602 | activity | SUBSTITUTED | `div.col-12` | `a` | `WIDGET` | 33 | 29 | 0.57 of 1950 | template+ptype=Standard/lesson c=0.68 n=28 | structure | — | CANDIDATE |
| 603 | activity | EXTRA | `div.activity` | `—` | `div.row` | 40 | 27 | 1.00 of 1950 | era=Refresh c=1.00 n=40 | structure | yes | CANDIDATE |
| 608 | activity | EXTRA | `div.videoSection.ratio.ratio-16x9` | `—` | `iframe` | 35 | 26 | 0.97 of 1950 | template=Standard c=0.98 n=22 | structure | yes | CANDIDATE |
| 609 | activity | EXTRA | `div.col-12` | `—` | `audio.audioPlayer.icon` | 41 | 25 | 1.00 of 1950 | era=Refresh c=1.00 n=41 | structure | yes | CANDIDATE |
| 611 | activity | EXTRA | `div.col-12` | `—` | `h5` | 31 | 25 | 0.96 of 1950 | template=Standard c=0.96 n=26 | structure | — | CANDIDATE |
| 616 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `div.col-md-8.col-12` | 25 | 24 | 0.60 of 1950 | era=Refresh c=0.60 n=25 | structure | — | CANDIDATE |
| 618 | activity | EXTRA | `p` | `—` | `b` | 31 | 23 | 0.96 of 1950 | template=Standard c=0.96 n=28 | structure | — | CANDIDATE |
| 622 | activity | EXTRA | `div.col-12` | `—` | `div.videoSection.icon.ratio.ratio-16x9` | 38 | 22 | 0.97 of 1950 | template=Standard c=0.98 n=32 | structure | yes | CANDIDATE |
| 624 | activity | SUBSTITUTED | `div.row` | `div.col-12` | `div.col-md-8.col-12` | 25 | 22 | 0.79 of 1950 | era=Refresh c=0.79 n=25 | structure | — | CANDIDATE |
| 630 | activity | SUBSTITUTED | `div.row` | `div.col-12` | `div.row` | 21 | 21 | 0.79 of 1950 | era=Refresh c=0.79 n=21 | structure | — | CANDIDATE |
| 633 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `ol` | 21 | 20 | 0.60 of 1950 | era=Refresh c=0.60 n=21 | structure | — | CANDIDATE |
| 637 | activity | EXTRA | `a` | `—` | `div.externalButton` | 26 | 19 | 0.91 of 1950 | era=Refresh c=0.91 n=26 | structure | — | CANDIDATE |
| 638 | activity | SUBSTITUTED | `div.row` | `div.col-12` | `WIDGET` | 21 | 19 | 0.79 of 1950 | era=Refresh c=0.79 n=21 | structure | — | CANDIDATE |
| 640 | activity | EXTRA | `div.col-12` | `—` | `div.button` | 30 | 18 | 1.00 of 1950 | template=Standard c=1.00 n=26 | structure | yes | CANDIDATE |
| 643 | activity | EXTRA | `div.col-12` | `—` | `div.TKmodal` | 20 | 17 | 0.99 of 1950 | era=Refresh c=0.99 n=20 | structure | — | CANDIDATE |
| 650 | activity | EXTRA | `div.row` | `—` | `div.clickDropContent` | 23 | 15 | 0.99 of 1950 | template=Standard c=1.00 n=23 | structure | — | CANDIDATE |
| 651 | activity | EXTRA | `div.row` | `—` | `WIDGET` | 22 | 15 | 1.00 of 1950 | era=Refresh c=1.00 n=22 | structure | — | CANDIDATE |
| 660 | activity | SUBSTITUTED | `div.col-12` | `p` | `h4.goJournal` | 23 | 14 | 0.76 of 1950 | template+ptype=Standard/lesson c=0.89 n=22 | structure | — | CANDIDATE |
| 661 | activity | EXTRA | `div.col-md-8.col-12` | `—` | `div.activity` | 20 | 14 | 1.00 of 1950 | era=Refresh c=1.00 n=20 | structure | yes | CANDIDATE |
| 6075 | body | EXTRA | `div#body` | `—` | `div.row` | 1261 | 324 | 0.73 of 1950 | subject+ptype=1-10 Blended Literacy/overview c=1.00 n=29 | structure | — | CANDIDATE |
| 6076 | body | EXTRA | `div.col-md-8.col-12` | `—` | `p` | 869 | 321 | 0.82 of 1950 | subject=1-10 Blended Literacy c=1.00 n=35 | structure | — | CANDIDATE |
| 6077 | body | MISSING | `div#body` | `div.row` | `—` | 1073 | 279 | 0.34 of 1950 | series=MXDI20 c=0.83 n=21 | 0.86 | — | CANDIDATE |
| 6078 | body | MISSING | `div.col-md-8.col-12` | `p` | `—` | 504 | 240 | 0.29 of 1950 | template+ptype=Fundamentals/overview c=0.93 n=32 | 0.82 | — | CANDIDATE |
| 6079 | body | EXTRA | `div.col-md-8.col-12` | `—` | `img.img-fluid` | 459 | 195 | 0.97 of 1950 | template+ptype=Standard/overview c=1.00 n=25 | structure | — | CANDIDATE |
| 6080 | body | MOVED | `div.col-md-8.col-12` | `p` | `p` | 301 | 189 | 0.18 of 1950 | template+ptype=Fundamentals/overview c=0.87 n=37 | structure | — | CANDIDATE |
| 6081 | body | EXTRA | `div.col-md-8.col-12` | `—` | `WIDGET` | 270 | 172 | 0.89 of 1950 | subject=NCEA1 c=0.96 n=23 | structure | — | CANDIDATE |
| 6082 | body | SUBSTITUTED | `div.row` | `div.col-12` | `div.col-md-8.col-12` | 288 | 160 | 0.55 of 1950 | subject+ptype=1-10 Blended Literacy/overview c=0.99 n=64 | structure | — | CANDIDATE |
| 6083 | body | EXTRA | `div.col-md-8.col-12` | `—` | `ul` | 281 | 158 | 0.96 of 1950 | subject=1-10 English c=0.99 n=24 | structure | — | CANDIDATE |
| 6084 | body | EXTRA | `div.col-md-8.col-12` | `—` | `p>b` | 263 | 156 | 0.95 of 1950 | subject=1-10 Blended Literacy c=1.00 n=37 | structure | — | CANDIDATE |
| 6085 | body | EXTRA | `div.row` | `—` | `div.col-md-8.col-12` | 239 | 156 | 0.89 of 1950 | subject+ptype=1-10 Blended Literacy/lesson c=0.99 n=20 | structure | — | CANDIDATE |
| 6086 | body | MISSING | `div.col-md-8.col-12` | `WIDGET` | `—` | 231 | 142 | 0.19 of 1950 | subject+ptype=Online Safety (OS9000)/lesson c=0.65 n=22 | structure | — | CANDIDATE |
| 6087 | body | EXTRA | `div.col-md-8.col-12` | `—` | `h3` | 211 | 140 | 0.72 of 1950 | subject=1-10 Blended Literacy c=1.00 n=20 | structure | — | CANDIDATE |
| 6090 | body | MISSING | `div.col-md-8.col-12` | `h3` | `—` | 220 | 130 | 0.17 of 1950 | template+ptype=Fundamentals/overview c=0.81 n=21 | 0.92 | — | CANDIDATE |
| 6093 | body | EXTRA | `div.col-md-8.col-12` | `—` | `a` | 191 | 108 | 0.98 of 1950 | subject=ConnectED c=1.00 n=28 | structure | — | CANDIDATE |
| 6094 | body | EXTRA | `div.col-md-8.col-12` | `—` | `div.table-responsive` | 176 | 105 | 0.98 of 1950 | subject+ptype=1-10 English/lesson c=0.99 n=22 | structure | — | CANDIDATE |
| 6096 | body | EXTRA | `div.col-md-8.col-12` | `—` | `div.videoSection.ratio.ratio-16x9` | 176 | 103 | 0.94 of 1950 | subject=1-10 English c=0.97 n=32 | structure | yes | CANDIDATE |
| 6098 | body | EXTRA | `p>b` | `—` | `b` | 151 | 95 | 0.91 of 1950 | subject=1-10 Mathematics c=0.94 n=30 | structure | — | CANDIDATE |
| 6099 | body | EXTRA | `a` | `—` | `div.button` | 170 | 88 | 0.99 of 1950 | subject=NCEA1 c=0.99 n=20 | structure | — | CANDIDATE |
| 6101 | body | EXTRA | `div.col-md-8.col-12` | `—` | `h4` | 118 | 88 | 0.98 of 1950 | template=Standard c=0.99 n=77 | structure | — | CANDIDATE |
| 6102 | body | EXTRA | `div.col-md-8.col-12` | `—` | `p>a` | 128 | 85 | 0.99 of 1950 | subject=1-10 Mathematics c=1.00 n=26 | structure | — | CANDIDATE |
| 6107 | body | EXTRA | `p` | `—` | `b` | 99 | 79 | 0.93 of 1950 | template=Standard c=0.94 n=84 | structure | — | CANDIDATE |
| 6108 | body | SUBSTITUTED | `div.col-md-8.col-12` | `h3` | `h4` | 113 | 77 | 0.48 of 1950 | template+ptype=Fundamentals/overview c=0.93 n=20 | structure | — | CANDIDATE |
| 6110 | body | EXTRA | `p>i` | `—` | `i` | 98 | 73 | 0.97 of 1950 | subject=1-10 Blended Literacy c=1.00 n=26 | structure | — | CANDIDATE |
| 6111 | body | EXTRA | `div.table-responsive` | `—` | `table.table.table-bordered` | 117 | 72 | 0.96 of 1950 | template=Standard c=0.97 n=104 | structure | yes | CANDIDATE |
| 6116 | body | SUBSTITUTED | `div.videoSection.icon.ratio.ratio-16x9` | `iframe.embed-responsive-item` | `iframe` | 173 | 67 | 0.21 of 1950 | series=PES10 c=0.68 n=35 | structure | yes | CANDIDATE |
| 6117 | body | EXTRA | `div.col-md-8.col-12` | `—` | `ol` | 98 | 67 | 0.99 of 1950 | ptype=overview c=0.99 n=24 | structure | — | CANDIDATE |
| 6120 | body | EXTRA | `table.table.table-bordered` | `—` | `tr` | 98 | 63 | 0.98 of 1950 | template=Standard c=0.99 n=87 | structure | yes | CANDIDATE |
| 6122 | body | EXTRA | `div.col-md-8.col-12` | `—` | `p>i` | 89 | 63 | 0.98 of 1950 | subject=NCEA1 c=0.99 n=23 | structure | — | CANDIDATE |
| 6124 | body | EXTRA | `div.col-md-8.col-12` | `—` | `audio.audioPlayer.icon` | 106 | 62 | 1.00 of 1950 | subject=Leaving to Learn c=1.00 n=34 | structure | yes | CANDIDATE |
| 6128 | body | EXTRA | `div.row` | `—` | `div.col-12` | 110 | 60 | 0.84 of 1950 | subject=ANZH c=0.87 n=20 | structure | — | CANDIDATE |
| 6129 | body | EXTRA | `div.videoSection.ratio.ratio-16x9` | `—` | `iframe` | 80 | 60 | 0.93 of 1950 | subject=1-10 Mathematics c=0.95 n=25 | structure | yes | CANDIDATE |
| 6135 | body | EXTRA | `ul` | `—` | `li` | 67 | 55 | 0.92 of 1950 | template=Standard c=0.94 n=49 | structure | — | CANDIDATE |
| 6136 | body | EXTRA | `p>a` | `—` | `a` | 63 | 55 | 0.99 of 1950 | template=Standard c=1.00 n=44 | structure | — | CANDIDATE |
| 6143 | body | SUBSTITUTED | `div.row` | `div.col-md-8.col-12` | `div.col-md-8.col-12` | 56 | 49 | 0.98 of 1950 | ptype=lesson c=0.99 n=28 | structure | — | CANDIDATE |
| 6144 | body | SUBSTITUTED | `div#body` | `div.row` | `WIDGET` | 58 | 48 | 0.94 of 1950 | template+ptype=Standard/lesson c=0.98 n=51 | structure | — | CANDIDATE |
| 6146 | body | EXTRA | `div.fundamentalsPanel` | `—` | `div.row` | 45 | 45 | 0.99 of 1950 | era=Refresh c=0.99 n=45 | structure | — | CANDIDATE |
| 6149 | body | EXTRA | `div.alert` | `—` | `div.row` | 56 | 43 | 0.91 of 1950 | template=Standard c=0.92 n=42 | structure | — | CANDIDATE |
| 6153 | body | EXTRA | `div.col-12` | `—` | `p` | 68 | 41 | 0.86 of 1950 | template=Standard c=0.88 n=59 | structure | — | CANDIDATE |
| 6154 | body | EXTRA | `div.row` | `—` | `div.col-md-6.col-12` | 58 | 41 | 0.99 of 1950 | subject=Online Safety (OS9000) c=1.00 n=20 | structure | — | CANDIDATE |
| 6155 | body | SUBSTITUTED | `div.col-md-8.col-12` | `p` | `p` | 55 | 41 | 0.85 of 1950 | template+ptype=Standard/lesson c=0.85 n=37 | structure | — | CANDIDATE |
| 6157 | body | EXTRA | `tr` | `—` | `th` | 46 | 41 | 0.99 of 1950 | template=Standard c=0.99 n=41 | structure | — | CANDIDATE |
| 6158 | body | EXTRA | `a` | `—` | `div.externalButton` | 63 | 40 | 0.92 of 1950 | template=Standard c=0.93 n=57 | structure | — | CANDIDATE |
| 6161 | body | EXTRA | `div#body` | `—` | `div.row.supervisor` | 50 | 38 | 0.88 of 1950 | ptype=lesson c=0.89 n=45 | structure | yes | CANDIDATE |
| 6162 | body | EXTRA | `tr` | `—` | `td` | 42 | 38 | 0.95 of 1950 | template=Standard c=0.95 n=35 | structure | — | CANDIDATE |
| 6169 | body | MISSING | `div#body` | `div.fundamentalsPanel` | `—` | 36 | 36 | 0.02 of 1950 | template+ptype=Fundamentals/overview c=0.87 n=35 | 1.00 | yes | CANDIDATE |
| 6172 | body | EXTRA | `p` | `—` | `i` | 43 | 35 | 0.97 of 1950 | template=Standard c=0.97 n=41 | structure | — | CANDIDATE |
| 6178 | body | EXTRA | `div.col-md-8.col-12` | `—` | `h5` | 38 | 32 | 1.00 of 1950 | template=Standard c=1.00 n=21 | structure | — | CANDIDATE |
| 6180 | body | SUBSTITUTED | `div.row` | `div.col-md-8.col-12` | `WIDGET` | 33 | 32 | 0.98 of 1950 | ptype=lesson c=0.99 n=28 | structure | — | CANDIDATE |
| 6181 | body | EXTRA | `div#body` | `—` | `WIDGET` | 48 | 31 | 0.94 of 1950 | era=Refresh c=0.94 n=48 | structure | — | CANDIDATE |
| 6183 | body | EXTRA | `div.col-md-8.col-12` | `—` | `h4.goJournal` | 41 | 30 | 1.00 of 1950 | subject=1-10 Mathematics c=1.00 n=22 | structure | — | CANDIDATE |
| 6185 | body | EXTRA | `div.col-md-8.col-12` | `—` | `div.videoSection.icon.ratio.ratio-16x9` | 44 | 29 | 0.91 of 1950 | template=Standard c=0.93 n=33 | structure | yes | CANDIDATE |
| 6188 | body | EXTRA | `div#body` | `—` | `div.fundamentalsPanel` | 29 | 29 | 0.98 of 1950 | era=Refresh c=0.98 n=29 | structure | yes | CANDIDATE |
| 6189 | body | EXTRA | `div.inquiryPanel` | `—` | `div.row` | 29 | 29 | 0.99 of 1950 | era=Refresh c=0.99 n=29 | structure | — | CANDIDATE |
| 6190 | body | SUBSTITUTED | `div.row` | `div.col-md-8.col-12` | `div.row` | 29 | 29 | 0.98 of 1950 | era=Refresh c=0.98 n=29 | structure | — | CANDIDATE |
| 6191 | body | EXTRA | `div.col-md-8.col-12` | `—` | `div.alert` | 36 | 28 | 0.91 of 1950 | template=Standard c=0.92 n=29 | structure | — | CANDIDATE |
| 6196 | body | EXTRA | `div.row` | `—` | `div.col-md-4.offset-md-0.col-12` | 27 | 27 | 0.79 of 1950 | era=Refresh c=0.79 n=27 | structure | — | CANDIDATE |
| 6209 | body | SUBSTITUTED | `div.col-md-8.col-12` | `p` | `WIDGET` | 25 | 24 | 0.85 of 1950 | era=Refresh c=0.85 n=25 | structure | — | CANDIDATE |
| 6210 | body | EXTRA | `div#body` | `—` | `div.inquiryPanel` | 24 | 24 | 0.99 of 1950 | era=Refresh c=0.99 n=24 | structure | — | CANDIDATE |
| 6212 | body | EXTRA | `div.col-md-8.col-12` | `—` | `p>span.infoTrigger` | 29 | 23 | 0.86 of 1950 | template=Standard c=0.87 n=26 | structure | — | CANDIDATE |
| 6214 | body | EXTRA | `div.alert.solid` | `—` | `div.row` | 31 | 22 | 0.99 of 1950 | template=Standard c=0.99 n=26 | structure | yes | CANDIDATE |
| 6215 | body | EXTRA | `div.col-md-8.col-12` | `—` | `div.row.flipCardsContainer` | 27 | 22 | 0.93 of 1950 | template=Standard c=0.94 n=23 | structure | — | CANDIDATE |
| 6222 | body | EXTRA | `div.row.flipCardsContainer` | `—` | `div.col-md-4.col-12.paddingLR` | 23 | 22 | 0.97 of 1950 | era=Refresh c=0.97 n=23 | structure | — | CANDIDATE |
| 6229 | body | SUBSTITUTED | `div.col-md-8.col-12` | `p` | `img.img-fluid` | 21 | 21 | 0.85 of 1950 | era=Refresh c=0.85 n=21 | structure | — | CANDIDATE |
| 6233 | body | EXTRA | `div.videoSection.icon.ratio.ratio-16x9` | `—` | `iframe` | 26 | 20 | 0.97 of 1950 | ptype=lesson c=0.98 n=21 | structure | yes | CANDIDATE |
| 6239 | body | EXTRA | `div.col-md-8.col-12` | `—` | `div.alert.solid` | 25 | 19 | 0.99 of 1950 | era=Refresh c=0.99 n=25 | structure | yes | CANDIDATE |
| 6243 | body | EXTRA | `div.row` | `—` | `div.col-md-4.col-12` | 23 | 19 | 0.95 of 1950 | era=Refresh c=0.95 n=23 | structure | — | CANDIDATE |
| 6244 | body | EXTRA | `div.row` | `—` | `div.clickDropContent` | 21 | 19 | 1.00 of 1950 | era=Refresh c=1.00 n=21 | structure | — | CANDIDATE |
| 6245 | body | EXTRA | `div.col-md-8.col-12` | `—` | `div.row` | 21 | 19 | 0.75 of 1950 | era=Refresh c=0.75 n=21 | structure | — | CANDIDATE |
| 6246 | body | SUBSTITUTED | `div.col-md-8.col-12` | `p` | `ul` | 21 | 19 | 0.85 of 1950 | era=Refresh c=0.85 n=21 | structure | — | CANDIDATE |
| 6247 | body | SUBSTITUTED | `div.row` | `div.col-md-8.col-12` | `div.col-md-6.col-12` | 21 | 19 | 0.98 of 1950 | era=Refresh c=0.98 n=21 | structure | — | CANDIDATE |
| 6254 | body | SUBSTITUTED | `div.col-md-8.col-12` | `p` | `h3` | 20 | 18 | 0.85 of 1950 | era=Refresh c=0.85 n=20 | structure | — | CANDIDATE |
| 6258 | body | SUBSTITUTED | `div.col-md-8.col-12` | `p` | `div.alert` | 26 | 17 | 0.85 of 1950 | era=Refresh c=0.85 n=26 | structure | — | CANDIDATE |
| 6265 | body | EXTRA | `th>b` | `—` | `b` | 22 | 16 | 1.00 of 1950 | era=Refresh c=1.00 n=22 | structure | — | CANDIDATE |
| 6281 | body | MISSING | `div#body` | `div.row.clickDropContent.noBorder` | `—` | 49 | 14 | 0.03 of 1950 | series=XDLS90 c=0.64 n=38 | 0.94 | yes | CANDIDATE |
| 6282 | body | EXTRA | `div.col-12` | `—` | `ul` | 20 | 14 | 0.88 of 1950 | era=Refresh c=0.88 n=20 | structure | — | CANDIDATE |
| 10952 | root | EXTRA | `body.container-fluid` | `—` | `div.row` | 233 | 233 | 0.87 of 1956 | subject+ptype=NCEA1/overview c=0.98 n=41 | structure | — | CANDIDATE |
| 10957 | root | SUBSTITUTED | `#root` | `html.notranslate` | `body.container-fluid` | 95 | 11 | 0.05 of 1956 | series=CEDO50 c=1.00 n=25 | structure | yes | CANDIDATE |

## Details — in the companion file `CONVERTER_V2/outputs/_diff_queue_details.md`
Every CANDIDATE and every top-40 row has three quoted examples (WT / gold / Claude) there, plus the
below-floor list. **NEVER read the companion whole** (hundreds of KB): `grep -n '^### #<rank> ' CONVERTER_V2/outputs/_diff_queue_details.md` then `sed -n '<start>,<start+40>p'`. The top 25
candidates' detail blocks are repeated below for convenience.

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
