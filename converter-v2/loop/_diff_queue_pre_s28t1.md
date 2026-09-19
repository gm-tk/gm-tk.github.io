# DIFF_QUEUE.md — the diff miner's ranked class queue (LOOP__Autonomous_Rounds.md §1d)

**Produced:** 2026-09-19 20:42 NZST by `reference/tests/_diff_miner.py` on the CURRENT corpus (pageforge-site HEAD bb32cfd; Claude corpus 494 dirs). **Population:** the skeleton gate's own — 2349 paired pages / 483 modules (compare_exclusions.txt honoured; acks / glossary / references pages excluded); parse errors skipped: 0 (must be 0); modules without a parsed WT: 2. Run time 134.1 s.

**What a row is.** One CLASS = (region, parent element, gold form, Claude form, direction) over every differing skeleton line of every paired page — the same lines, labels, widget collapse and difflib alignment the PRIMARY gate scores (each element its own line so it can be quoted). Direction: MISSING = gold has it, Claude lacks it; EXTRA = Claude has it, gold lacks it; SUBSTITUTED = same position, different tag / class / wrapper; MOVED = same text, different place. Consensus = of the gold pages in the group where the region exists, the share carrying the gold form (for EXTRA: the share NOT carrying Claude's form). Derivable = the gold line's text is in the module's parsed Writers Template (round-110 tolerance); structure-only differences are always derivable.

**Candidate rule (§1d).** modules ≥ 10 for a chrome class (module-code / title / header / module-menu / crumbs / phases-nav / footer / acks), pages ≥ 20 for a body / activity class; gold consensus ≥ 0.60 in at least one template or subject group that itself reaches the floor; structure-only or derivable share ≥ 0.60. A class below the floor is listed, never dropped. A CANDIDATE still goes through the PICK's KB-first check, the triangulation and the §3 corpus-wide measurement before any code — this table is the queue, not the verdict.

## Summary

- differing skeleton lines: 269709 — by direction {'MISSING': 144060, 'SUBSTITUTED': 23923, 'EXTRA': 92689, 'MOVED': 9037}
- by region: {'module-code': 15, 'title': 360, 'header': 5, 'module-menu': 14736, 'phases-nav': 203, 'crumbs': 202, 'footer': 2409, 'acks': 1340, 'activity': 96315, 'body': 152470, 'root': 1654}
- classes: 8934 — CANDIDATE 188, below floor 8463, the rest below consensus / not derivable

## Completeness census — the repeating chrome (§1d item 4)

| region | pages with region | gold items | gold items in WT | Claude items | derivable misses | pages with misses | modules with misses | status |
|---|---|---|---|---|---|---|---|---|
| module-menu | 1497 | 15805 | 14565 | 12136 | 5335 | 762 | 201 | CANDIDATE (verify by eye — text presence, not position) |
| crumbs | 57 | 300 | 285 | 207 | 115 | 28 | 24 | CANDIDATE (verify by eye — text presence, not position) |
| phases-nav | 90 | 356 | 323 | 211 | 153 | 51 | 42 | CANDIDATE (verify by eye — text presence, not position) |
| footer | 14 | 70 | 56 | 0 | 56 | 14 | 6 | BELOW FLOOR |

- **module-menu** by template: Fundamentals 12m/22p/89 misses; Inquiry 28m/50p/307 misses; Standard 161m/690p/4939 misses
  - MXFL202 MXFL202_1_0.html: gold 53 items (51 in WT) / Claude 0 — 51 derivable misses, e.g. h3 «Understand» · span «Understand»
  - MXFL202 MXFL202_2_0.html: gold 53 items (51 in WT) / Claude 0 — 51 derivable misses, e.g. h3 «Understand» · span «Understand»
  - MXFL202 MXFL202_4_0.html: gold 53 items (51 in WT) / Claude 0 — 51 derivable misses, e.g. h3 «Understand» · span «Understand»
  - MXFL202 MXFL202_6_0.html: gold 53 items (51 in WT) / Claude 0 — 51 derivable misses, e.g. h3 «Understand» · span «Understand»
- **crumbs** by template: Fundamentals 0m/0p/0 misses; Inquiry 22m/22p/83 misses; Standard 2m/6p/32 misses
  - BLL240 BLL240_1_0.html: gold 8 items (8 in WT) / Claude 0 — 8 derivable misses, e.g. p «Introduction» · p «wh»
  - CEDK501 CEDK501_0_0.html: gold 8 items (7 in WT) / Claude 0 — 7 derivable misses, e.g. p «Dream it, plan it, do it» · p «Costing it out: budgeting for success»
  - CEDT104 CEDT104_0_0.html: gold 8 items (7 in WT) / Claude 0 — 7 derivable misses, e.g. p «Introduction» · p «Pepeha»
  - TWHA902 TWHA902_0_0.html: gold 9 items (8 in WT) / Claude 1 — 7 derivable misses, e.g. p «Listening, speaking, reading, writing» · p «Active listening»
- **phases-nav** by template: Fundamentals 41m/50p/149 misses; Standard 1m/1p/4 misses
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
| F1 | MISSING | `header:title-h1-count=2` | 277 | 138 | 0.23 | 0.23 | subject+ptype=1-10 English/overview c=0.94 n=17 | CANDIDATE |
| F2 | EXTRA | `header:title-h1-count=1` | 274 | 135 | 0.76 | 0.24 | subject+ptype=1-10 English/overview c=0.94 n=17 | CANDIDATE |
| F3 | EXTRA | `header:chip=decimal-number` | 243 | 73 | 0.57 | 0.43 | series=WJFUN c=1.00 n=20 | CANDIDATE |
| F4 | MISSING | `header:chip=module-code` | 96 | 63 | 0.17 | 0.17 | series=WJFUN c=1.00 n=20 | CANDIDATE |
| F5 | MISSING | `header:chip=decimal-number` | 119 | 52 | 0.57 | 0.57 | template+ptype=Standard/lesson c=0.71 n=41 | CANDIDATE |
| F6 | EXTRA | `header:menu-content` | 115 | 45 | 0.75 | 0.25 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F7 | EXTRA | `header:head-buttons` | 109 | 42 | 0.77 | 0.23 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F8 | EXTRA | `header:chip=lesson-number` | 78 | 34 | 0.19 | 0.81 | era=Refresh c=0.81 n=34 | CANDIDATE |
| F9 | MISSING | `header:chip=lesson-number` | 181 | 32 | 0.19 | 0.19 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F10 | EXTRA | `header:chip=other` | 75 | 27 | 0.04 | 0.96 | ptype=lesson c=0.99 n=15 | CANDIDATE |
| F11 | EXTRA | `header:chip=module-code` | 27 | 27 | 0.17 | 0.83 | template=Standard c=0.86 n=14 | CANDIDATE |
| F12 | MISSING | `header:head-buttons` | 68 | 24 | 0.77 | 0.77 | template=Standard c=0.78 n=17 | CANDIDATE |
| F13 | EXTRA | `header:title-h1-count=2` | 20 | 19 | 0.23 | 0.77 | template=Standard c=0.81 n=15 | CANDIDATE |
| F14 | MISSING | `header:title-h1-count=1` | 17 | 16 | 0.76 | 0.76 | template=Standard c=0.81 n=13 | CANDIDATE |
| F15 | MISSING | `header:chip=other` | 26 | 15 | 0.04 | 0.04 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F16 | MISSING | `header:menu-content` | 41 | 11 | 0.75 | 0.75 | era=Refresh c=0.75 n=11 | CANDIDATE |
| F17 | MISSING | `header:title-h1-count=3` | 6 | 6 | 0.00 | 0.00 | — | BELOW FLOOR |
| F18 | EXTRA | `header:title-h1-count=0` | 5 | 5 | 0.00 | 1.00 | — | BELOW FLOOR |
| F19 | EXTRA | `header:chip` | 5 | 5 | 0.97 | 0.03 | — | BELOW FLOOR |
| F20 | MISSING | `header:chip` | 3 | 3 | 0.97 | 0.97 | — | BELOW FLOOR |
| F21 | EXTRA | `header:title-h1-count=3` | 1 | 1 | 0.00 | 1.00 | — | BELOW FLOOR |
| F22 | EXTRA | `header:chip=lesson-number(00)` | 1 | 1 | 0.00 | 1.00 | — | BELOW FLOOR |
| F23 | MISSING | `nav:phases` | 41 | 32 | 0.04 | 0.04 | series=WJFUN c=1.00 n=21 | CANDIDATE |
| F24 | MISSING | `nav:crumbs` | 11 | 11 | 0.02 | 0.02 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F25 | EXTRA | `nav:crumbs` | 12 | 3 | 0.02 | 0.98 | — | BELOW FLOOR |
| F26 | MISSING | `footer:inside-body` | 168 | 127 | 0.07 | 0.07 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F27 | EXTRA | `footer:links=next-lesson,home-nav` | 106 | 105 | 0.12 | 0.88 | template=Fundamentals c=0.99 n=13 | CANDIDATE |
| F28 | EXTRA | `footer:links=prev-lesson,next-lesson,home-nav` | 246 | 102 | 0.61 | 0.39 | ptype=overview c=0.95 n=35 | CANDIDATE |
| F29 | EXTRA | `footer:links=prev-lesson,home-nav` | 94 | 94 | 0.13 | 0.87 | series=WJFUN c=1.00 n=11 | CANDIDATE |
| F30 | MISSING | `footer:links=prev-lesson,next-lesson,home-nav` | 77 | 72 | 0.61 | 0.61 | template+ptype=Bilingual/lesson c=0.81 n=10 | CANDIDATE |
| F31 | MISSING | `footer:link=next-lesson` | 71 | 71 | 0.82 | 0.82 | template=Bilingual c=0.86 n=10 | CANDIDATE |
| F32 | MISSING | `footer:links=home-nav,next-lesson` | 69 | 68 | 0.03 | 0.03 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F33 | EXTRA | `footer:link=next-lesson` | 107 | 57 | 0.82 | 0.18 | series=WJFUN c=1.00 n=10 | CANDIDATE |
| F34 | EXTRA | `footer:link=prev-lesson` | 65 | 49 | 0.81 | 0.19 | series=WJFUN c=1.00 n=20 | CANDIDATE |
| F35 | MISSING | `footer:links=home-nav,prev-lesson,next-lesson` | 112 | 47 | 0.05 | 0.05 | subject=1-10 Health and PE c=0.80 n=12 | CANDIDATE |
| F36 | MISSING | `footer:links=home-nav` | 60 | 47 | 0.04 | 0.04 | series=WJFUN c=1.00 n=21 | CANDIDATE |
| F37 | MISSING | `footer:ul=footer-nav` | 75 | 26 | 0.85 | 0.85 | template+ptype=Standard/lesson c=0.90 n=14 | CANDIDATE |
| F38 | EXTRA | `footer:ul=footer-nav` | 34 | 26 | 0.85 | 0.15 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F39 | EXTRA | `footer:ul=footer-nav inquiry-nav` | 85 | 22 | 0.12 | 0.88 | ptype=lesson c=0.91 n=19 | CANDIDATE |
| F40 | MISSING | `footer:links=prev-lesson,home-nav` | 52 | 22 | 0.13 | 0.13 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F41 | MISSING | `footer:link=prev-lesson` | 20 | 19 | 0.81 | 0.81 | template=Standard c=0.84 n=11 | CANDIDATE |
| F42 | MISSING | `footer:ul=footer-nav fundamentals-nav` | 27 | 18 | 0.02 | 0.02 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F43 | MISSING | `footer:links=next-lesson,home-nav` | 10 | 10 | 0.12 | 0.12 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| F44 | MISSING | `footer:ul=footer-nav inquiry-nav` | 14 | 7 | 0.12 | 0.12 | — | BELOW FLOOR |
| F45 | MISSING | `footer:links=home-nav,prev-lesson` | 7 | 7 | 0.00 | 0.00 | — | BELOW FLOOR |
| F46 | EXTRA | `footer:ul=footer-nav fundamentals-nav` | 7 | 7 | 0.02 | 0.98 | — | BELOW FLOOR |
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

### F1 · MISSING `header:title-h1-count=2` — CANDIDATE (pages 277 / modules 138)
- by template+ptype: Standard/overview 54m/54p gold 0.65 Claude 0.53 c=0.65; Standard/lesson 42m/152p gold 0.10 Claude 0.02 c=0.10; Fundamentals/overview 25m/25p gold 0.70 Claude 0.32 c=0.70; Fundamentals/lesson 14m/14p gold 0.25 Claude 0.00 c=0.25; Inquiry/overview 6m/6p gold 0.53 Claude 0.44 c=0.53; Bilingual/overview 5m/5p gold 1.00 Claude 0.72 c=1.00; Bilingual/lesson 5m/15p gold 1.00 Claude 0.72 c=1.00; Inquiry/lesson 3m/6p gold 0.14 Claude 0.02 c=0.14
- by subject: None 33m/100p gold 0.33 Claude 0.12 c=0.33; 1-10 English 19m/19p gold 0.15 Claude 0.10 c=0.15; Leaving to Learn 15m/23p gold 0.26 Claude 0.17 c=0.26; Online Safety (OS9000) 13m/29p gold 0.33 Claude 0.11 c=0.33; NCEA1 12m/18p gold 0.13 Claude 0.09 c=0.13; 1-10 Mathematics 11m/11p gold 0.14 Claude 0.11 c=0.14; ConnectED 6m/6p gold 0.22 Claude 0.18 c=0.22; ANZH 5m/30p gold 0.55 Claude 0.17 c=0.55
- **AGH1005** AGH1005_0_0.html ↔ AGH1005.00.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=3']
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ANZH103** ANZH103_0_0.html ↔ ANZH103_0_0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: AGH1005, ANZH101, ANZH103, ANZH104, ANZH301, ANZH401, ANZH404, ARFUN01, ARFUN02, ARFUN03, ARFUN04, ARFUN05, ART1006, CEDK102, CEDK501, CEDO202, CEDO502, CEDR204, CEDT301, CHI1003, CHI1004, CHI1005, DTC1005, ENFUN01 …

### F2 · EXTRA `header:title-h1-count=1` — CANDIDATE (pages 274 / modules 135)
- by template+ptype: Standard/overview 53m/53p gold 0.33 Claude 0.46 c=0.67; Standard/lesson 41m/151p gold 0.90 Claude 0.98 c=0.10; Fundamentals/overview 23m/23p gold 0.30 Claude 0.65 c=0.70; Fundamentals/lesson 14m/14p gold 0.75 Claude 1.00 c=0.25; Inquiry/overview 7m/7p gold 0.42 Claude 0.56 c=0.58; Bilingual/overview 5m/5p gold 0.00 Claude 0.28 c=1.00; Bilingual/lesson 5m/15p gold 0.00 Claude 0.28 c=1.00; Inquiry/lesson 3m/6p gold 0.86 Claude 0.98 c=0.14
- by subject: None 33m/100p gold 0.66 Claude 0.88 c=0.34; 1-10 English 19m/19p gold 0.84 Claude 0.91 c=0.15; Leaving to Learn 15m/23p gold 0.74 Claude 0.83 c=0.26; Online Safety (OS9000) 13m/29p gold 0.67 Claude 0.89 c=0.33; NCEA1 11m/17p gold 0.86 Claude 0.90 c=0.14; 1-10 Mathematics 11m/11p gold 0.85 Claude 0.89 c=0.14; ConnectED 6m/6p gold 0.78 Claude 0.82 c=0.22; ANZH 5m/30p gold 0.45 Claude 0.83 c=0.55
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ANZH103** ANZH103_0_0.html ↔ ANZH103_0_0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ANZH104** ANZH104_4_0.html ↔ ANZH104_04.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1']
- modules: ANZH101, ANZH103, ANZH104, ANZH301, ANZH401, ANZH404, ARFUN02, ARFUN03, ARFUN04, ARFUN05, ART1006, CEDK102, CEDK501, CEDO202, CEDO502, CEDR204, CEDT301, CHI1003, CHI1004, CHI1005, CHWHA, DTC1005, ENFUN01, ENFUN02 …

### F3 · EXTRA `header:chip=decimal-number` — CANDIDATE (pages 243 / modules 73)
- by template+ptype: Standard/lesson 44m/192p gold 0.71 Claude 0.76 c=0.29; Fundamentals/lesson 21m/21p gold 0.53 Claude 0.90 c=0.47; Inquiry/lesson 7m/25p gold 0.49 Claude 1.00 c=0.51; Bilingual/lesson 1m/5p gold 0.77 Claude 0.87 c=0.23
- by subject: None 37m/105p gold 0.61 Claude 0.77 c=0.39; Leaving to Learn 8m/38p gold 0.41 Claude 0.53 c=0.59; 1-10 English 7m/30p gold 0.59 Claude 0.66 c=0.41; 1-10 Blended Literacy 5m/15p gold 0.40 Claude 0.28 c=0.60; NCEA1 5m/21p gold 0.82 Claude 0.87 c=0.18; 1-10 Mathematics 5m/18p gold 0.72 Claude 0.74 c=0.28; ConnectED 3m/3p gold 0.71 Claude 0.73 c=0.29; ANZH 2m/8p gold 0.54 Claude 0.64 c=0.46
- **ANZH101** ANZH101_1_0.html ↔ ANZH101_1.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ANZH103** ANZH103_1_0.html ↔ ANZH103_3_0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1']
- **ANZH203** ANZH203_1_0.html ↔ ANZH203_1.0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: ANZH101, ANZH103, ANZH203, ANZH302, BLL236, BLL240, BLL253, BLL262, BLL263, CEDK501, CEDT207, CEDT301, CHI1004, ENGC204, ENGC206, ENGI101, ENGI102, ENGJ201, ENGR102, ENGR201, ENGS301, ENGS401, ENO2060, FRNO901 …

### F4 · MISSING `header:chip=module-code` — CANDIDATE (pages 96 / modules 63)
- by template+ptype: Standard/lesson 21m/47p gold 0.03 Claude 0.00 c=0.03; Fundamentals/lesson 21m/21p gold 0.37 Claude 0.00 c=0.37; Standard/overview 10m/10p gold 0.74 Claude 0.75 c=0.74; Bilingual/lesson 4m/11p gold 0.21 Claude 0.00 c=0.21; Inquiry/overview 3m/3p gold 0.33 Claude 0.38 c=0.33; Inquiry/lesson 3m/3p gold 0.06 Claude 0.00 c=0.06; Fundamentals/overview 1m/1p gold 0.52 Claude 0.58 c=0.52
- by subject: None 31m/32p gold 0.20 Claude 0.14 c=0.20; 1-10 Blended Literacy 9m/9p gold 0.05 Claude 0.02 c=0.05; 1-10 Mathematics 5m/18p gold 0.16 Claude 0.11 c=0.16; NCEA1 4m/4p gold 0.13 Claude 0.13 c=0.13; Te Marautanga o Aotearoa TMoA 3m/9p gold 0.36 Claude 0.25 c=0.36; Leaving to Learn 3m/5p gold 0.15 Claude 0.17 c=0.15; ConnectED 2m/2p gold 0.09 Claude 0.07 c=0.09; 1-10 English 2m/2p gold 0.14 Claude 0.13 c=0.14
- **ANZH401** ANZH401_1_0.html ↔ ANZH401_1.0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ANZHFUN05** MODULE_0_0.html ↔ ANZHFUN05_0_0.html: gold ['header:chip', 'header:chip=module-code', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2']
- **BLL170** BLL170_0_0.html ↔ BLL170.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: ANZH401, ANZHFUN05, BLL170, BLL172, BLL174, BLL175, BLL176, BLL177, BLL240, BLL252, BLL253, BLLR201, BLLR202, BLLR203, CEDK501, CEDT207, CHI1004, CHWHA, ENGR102, ENGS401, EXBP901, EXIP901, GEO1004, GEWHA …

### F5 · MISSING `header:chip=decimal-number` — CANDIDATE (pages 119 / modules 52)
- by template+ptype: Standard/lesson 41m/107p gold 0.71 Claude 0.76 c=0.71; Standard/overview 6m/6p gold 0.02 Claude 0.00 c=0.02; Bilingual/overview 3m/3p gold 0.17 Claude 0.00 c=0.17; Inquiry/overview 2m/2p gold 0.04 Claude 0.00 c=0.04; Fundamentals/overview 1m/1p gold 0.02 Claude 0.00 c=0.02
- by subject: 1-10 Blended Literacy 23m/45p gold 0.40 Claude 0.28 c=0.40; None 9m/34p gold 0.61 Claude 0.77 c=0.61; 1-10 Mathematics 6m/10p gold 0.72 Claude 0.74 c=0.72; NCEA1 4m/4p gold 0.82 Claude 0.87 c=0.82; Leaving to Learn 4m/12p gold 0.41 Claude 0.53 c=0.41; 1-10 English 2m/9p gold 0.59 Claude 0.66 c=0.59; Te Marautanga o Aotearoa TMoA 2m/2p gold 0.62 Claude 0.67 c=0.62; ConnectED 1m/1p gold 0.71 Claude 0.73 c=0.71
- **ART1004** ART1004_0_0.html ↔ ART1004_4.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **ART1005** ART1005_0_0.html ↔ ART1005_3.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **BLL141** BLL141_1_0.html ↔ BLL141-1.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- modules: ART1004, ART1005, BLL141, BLL142, BLL143, BLL144, BLL145, BLL146, BLL147, BLL151, BLL152, BLL154, BLL156, BLL157, BLL161, BLL162, BLL163, BLL164, BLL165, BLL166, BLL167, BLL171, BLL172, BLL173 …

### F8 · EXTRA `header:chip=lesson-number` — CANDIDATE (pages 78 / modules 34)
- by template+ptype: Standard/lesson 31m/72p gold 0.24 Claude 0.19 c=0.76; Bilingual/lesson 3m/6p gold 0.02 Claude 0.13 c=0.98
- by subject: 1-10 Blended Literacy 22m/44p gold 0.24 Claude 0.37 c=0.76; Leaving to Learn 5m/15p gold 0.40 Claude 0.30 c=0.60; 1-10 English 2m/9p gold 0.22 Claude 0.18 c=0.78; Te Marautanga o Aotearoa TMoA 2m/4p gold 0.02 Claude 0.08 c=0.98; ConnectED 1m/1p gold 0.07 Claude 0.07 c=0.94; 1-10 Mathematics 1m/3p gold 0.10 Claude 0.11 c=0.90; None 1m/2p gold 0.17 Claude 0.01 c=0.83
- **BLL141** BLL141_1_0.html ↔ BLL141-1.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- **BLL142** BLL142_1_0.html ↔ BLL142-1.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- **BLL143** BLL143_1_0.html ↔ BLL143-1.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- modules: BLL141, BLL142, BLL143, BLL144, BLL145, BLL146, BLL147, BLL151, BLL152, BLL154, BLL156, BLL157, BLL161, BLL162, BLL163, BLL164, BLL165, BLL166, BLL167, BLL171, BLL172, BLL173, CEDR501, ENGJ101 …

### F10 · EXTRA `header:chip=other` — CANDIDATE (pages 75 / modules 27)
- by template+ptype: Standard/lesson 15m/62p gold 0.01 Claude 0.04 c=0.99; Standard/overview 10m/10p gold 0.24 Claude 0.25 c=0.76; Inquiry/overview 2m/2p gold 0.07 Claude 0.04 c=0.93; Fundamentals/overview 1m/1p gold 0.00 Claude 0.02 c=1.00
- by subject: None 11m/37p gold 0.02 Claude 0.08 c=0.98; 1-10 Blended Literacy 7m/7p gold 0.29 Claude 0.31 c=0.71; 1-10 Mathematics 5m/7p gold 0.00 Claude 0.02 c=1.00; 1-10 Social Science 2m/11p gold 0.00 Claude 0.29 c=1.00; ANZH 1m/12p gold 0.08 Claude 0.23 c=0.92; Leaving to Learn 1m/1p gold 0.04 Claude 0.01 c=0.96
- **ANZH401** ANZH401_1_0.html ↔ ANZH401_1.0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- **ANZHFUN05** MODULE_0_0.html ↔ ANZHFUN05_0_0.html: gold ['header:chip', 'header:chip=module-code', 'header:title-h1-count=2'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2']
- **BLL172** BLL172_0_0.html ↔ BLL172-00.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: ANZH401, ANZHFUN05, BLL172, BLL174, BLL175, BLL176, BLL177, BLL252, BLL253, BLLR201, BLLR202, BLLR203, CHWHA, GEWHA, MXDB301, MXEO301, MXEX301, MXFL302, MXFU302, PWY1001, PWY1002, PWY1008, PWY1009, PWYWHA1 …

### F11 · EXTRA `header:chip=module-code` — CANDIDATE (pages 27 / modules 27)
- by template+ptype: Standard/overview 12m/12p gold 0.74 Claude 0.75 c=0.26; Inquiry/overview 5m/5p gold 0.33 Claude 0.38 c=0.67; Fundamentals/overview 5m/5p gold 0.52 Claude 0.58 c=0.48; Bilingual/overview 3m/3p gold 0.83 Claude 1.00 c=0.17; Standard/lesson 2m/2p gold 0.03 Claude 0.00 c=0.97
- by subject: Leaving to Learn 9m/9p gold 0.15 Claude 0.17 c=0.85; None 5m/5p gold 0.20 Claude 0.14 c=0.80; NCEA1 4m/4p gold 0.13 Claude 0.13 c=0.87; 1-10 Health and PE 2m/2p gold 0.87 Claude 1.00 c=0.13; 1-10 Social Science 2m/2p gold 0.26 Claude 0.29 c=0.74; Te Marautanga o Aotearoa TMoA 2m/2p gold 0.36 Claude 0.25 c=0.64; 1-10 Blended Literacy 1m/1p gold 0.05 Claude 0.02 c=0.95; 1-10 Mathematics 1m/1p gold 0.16 Claude 0.11 c=0.84
- **ART1004** ART1004_0_0.html ↔ ART1004_4.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **ART1005** ART1005_0_0.html ↔ ART1005_3.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **BLL240** BLL240_0_0.html ↔ BLL240-0.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1']
- modules: ART1004, ART1005, BLL240, COM1002, ENG1004, ENGFUN02, FRFUN06, GEO1004, GER1002, HPFUN201, HPFUN302, MXDB201, OSOH101, SSFUN01, SSFUN07, TRR112, TRR113, TRR116, XDLS901, XDLS902, XDLS903, XDLS909, XFUN01, XGF9001 …

### F12 · MISSING `header:head-buttons` — CANDIDATE (pages 68 / modules 24)
- by template+ptype: Standard/lesson 16m/51p gold 0.75 Claude 0.76 c=0.75; Bilingual/lesson 5m/12p gold 0.23 Claude 0.00 c=0.23; Inquiry/lesson 2m/3p gold 0.71 Claude 0.69 c=0.71; Standard/overview 2m/2p gold 0.98 Claude 0.99 c=0.98
- by subject: None 6m/22p gold 0.81 Claude 0.93 c=0.81; 1-10 Blended Literacy 4m/8p gold 0.41 Claude 0.38 c=0.41; Te Marautanga o Aotearoa TMoA 4m/10p gold 0.38 Claude 0.25 c=0.38; Leaving to Learn 3m/12p gold 0.88 Claude 0.83 c=0.88; ConnectED 2m/3p gold 0.76 Claude 0.87 c=0.76; Online Safety (OS9000) 2m/9p gold 1.00 Claude 0.93 c=1.00; EXPlore 1m/1p gold 1.00 Claude 0.93 c=1.00; NCEA1 1m/1p gold 0.71 Claude 0.73 c=0.71
- **ANZH103** ANZH103_1_0.html ↔ ANZH103_3_0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1']
- **BLL114** BLL114_1_0.html ↔ BLL114-02.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- **BLL116** BLL116_1_0.html ↔ BLL116-02.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=lesson-number', 'header:title-h1-count=1']
- modules: ANZH103, BLL114, BLL116, BLL153, BLL236, BLLR201, BLLR202, BLLR203, CEDT207, CEDT301, EXPFUN07, HES1002, HES1006, MXFL401, OSSC401, OSSC501, PNR101, PNR102, PNR104, PNR107, TRR109, XGF9002, XGF9004, XLP06

### F13 · EXTRA `header:title-h1-count=2` — CANDIDATE (pages 20 / modules 19)
- by template+ptype: Standard/overview 12m/12p gold 0.65 Claude 0.53 c=0.35; Standard/lesson 4m/4p gold 0.10 Claude 0.02 c=0.90; Inquiry/overview 2m/2p gold 0.53 Claude 0.44 c=0.47; Fundamentals/overview 2m/2p gold 0.70 Claude 0.32 c=0.30
- by subject: None 8m/9p gold 0.33 Claude 0.12 c=0.67; Leaving to Learn 4m/4p gold 0.26 Claude 0.17 c=0.74; NCEA1 3m/3p gold 0.13 Claude 0.09 c=0.87; 1-10 Blended Literacy 1m/1p gold 0.00 Claude 0.00 c=1.00; ConnectED 1m/1p gold 0.22 Claude 0.18 c=0.78; 1-10 English 1m/1p gold 0.15 Claude 0.10 c=0.84; 1-10 Social Science 1m/1p gold 0.29 Claude 0.18 c=0.71
- **ANZH302** ANZH302_0_0.html ↔ ANZH302_0_0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2']
- **BLL246** BLL246_0_0.html ↔ BLL246_0.0.html: gold ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=other', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2']
- **CEDO105** CEDO105_0_0.html ↔ CEDO105.0.0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2']
- modules: ANZH302, BLL246, CEDO105, ENGFUN02, ENGI103, FRFUN06, GENO901, GEWHA, HIS1002, JPN1004, PHE1004, PWY1002, PWYWHA1, SPA1004, SSFUN07, XDLS904, XDLS906, XFUN02, XGF9004

### F14 · MISSING `header:title-h1-count=1` — CANDIDATE (pages 17 / modules 16)
- by template+ptype: Standard/overview 10m/10p gold 0.33 Claude 0.46 c=0.33; Standard/lesson 4m/4p gold 0.90 Claude 0.98 c=0.90; Fundamentals/overview 2m/2p gold 0.30 Claude 0.65 c=0.30; Inquiry/overview 1m/1p gold 0.42 Claude 0.56 c=0.42
- by subject: None 4m/5p gold 0.66 Claude 0.88 c=0.66; NCEA1 4m/4p gold 0.86 Claude 0.90 c=0.86; Leaving to Learn 4m/4p gold 0.74 Claude 0.83 c=0.74; 1-10 Blended Literacy 1m/1p gold 1.00 Claude 1.00 c=1.00; ConnectED 1m/1p gold 0.78 Claude 0.82 c=0.78; 1-10 English 1m/1p gold 0.84 Claude 0.91 c=0.84; 1-10 Social Science 1m/1p gold 0.71 Claude 0.79 c=0.71
- **ANZH302** ANZH302_0_0.html ↔ ANZH302_0_0.html: gold ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=2']
- **ART1004** ART1004_0_0.html ↔ ART1004_4.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- **ART1005** ART1005_0_0.html ↔ ART1005_3.0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=module-code', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=0']
- modules: ANZH302, ART1004, ART1005, BLL246, CEDO105, ENGFUN02, ENGI103, FRFUN06, HIS1002, PWY1002, PWYWHA1, SSFUN07, XDLS904, XDLS906, XFUN02, XGF9004

### F16 · MISSING `header:menu-content` — CANDIDATE (pages 41 / modules 11)
- by template+ptype: Standard/lesson 9m/38p gold 0.73 Claude 0.76 c=0.73; Inquiry/lesson 2m/3p gold 0.71 Claude 0.69 c=0.71
- by subject: None 4m/19p gold 0.80 Claude 0.93 c=0.80; ConnectED 2m/3p gold 0.76 Claude 0.87 c=0.76; Online Safety (OS9000) 2m/9p gold 1.00 Claude 0.93 c=1.00; Leaving to Learn 2m/9p gold 0.87 Claude 0.83 c=0.87; NCEA1 1m/1p gold 0.71 Claude 0.73 c=0.71
- **ANZH103** ANZH103_1_0.html ↔ ANZH103_3_0.html: gold ['header:chip', 'header:chip=lesson-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1']
- **BLLR201** BLLR201_1_1.html ↔ BLLR201_1_0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1']
- **BLLR202** BLLR202_1_1.html ↔ BLLR202_1_0.html: gold ['header:chip', 'header:chip=decimal-number', 'header:head-buttons', 'header:menu-content', 'header:title-h1-count=1'] · Claude ['header:chip', 'header:chip=decimal-number', 'header:title-h1-count=1']
- modules: ANZH103, BLLR201, BLLR202, BLLR203, CEDT207, CEDT301, HES1006, OSSC401, OSSC501, XGF9002, XGF9004

### F23 · MISSING `nav:phases` — CANDIDATE (pages 41 / modules 32)
- by template+ptype: Fundamentals/lesson 22m/30p gold 0.53 Claude 0.00 c=0.53; Fundamentals/overview 10m/10p gold 0.98 Claude 0.82 c=0.98; Standard/lesson 1m/1p gold 0.00 Claude 0.00 c=0.00
- by subject: None 27m/36p gold 0.10 Claude 0.01 c=0.10; 1-10 Mathematics 3m/3p gold 0.01 Claude 0.00 c=0.01; 1-10 Arts 1m/1p gold 1.00 Claude 0.80 c=1.00; 1-10 Social Science 1m/1p gold 0.18 Claude 0.16 c=0.18
- **ANZHFUN05** MODULE_0_0.html ↔ ANZHFUN05_0_0.html: gold ['nav:phases'] · Claude []
- **ARFUN04** ARFUN04_0_0.html ↔ ARFUN04_0.00.html: gold ['nav:phases'] · Claude []
- **FRFUN06** FRFUN06_0_0.html ↔ FRFUN06_1_0_Novice.html: gold ['nav:phases'] · Claude ['nav:crumbs']
- modules: ANZHFUN05, ARFUN04, FRFUN06, FRFUN07, FRFUN08, JPFUN01, JPFUN02, MXFUN01, MXFUN02, MXFUN03, SSFUN07, WJFUN105, WJFUN106, WJFUN107, WJFUN108, WJFUN109, WJFUN110, WJFUN112, WJFUN113, WJFUN115, WJFUN116, WJFUN205, WJFUN206, WJFUN208 …

### F27 · EXTRA `footer:links=next-lesson,home-nav` — CANDIDATE (pages 106 / modules 105)
- by template+ptype: Standard/overview 77m/77p gold 0.76 Claude 0.99 c=0.24; Fundamentals/overview 13m/13p gold 0.02 Claude 0.23 c=0.98; Inquiry/overview 11m/11p gold 0.02 Claude 0.24 c=0.98; Bilingual/overview 3m/3p gold 0.83 Claude 1.00 c=0.17; Standard/lesson 2m/2p gold 0.01 Claude 0.00 c=0.99
- by subject: Leaving to Learn 27m/27p gold 0.03 Claude 0.17 c=0.97; None 15m/16p gold 0.11 Claude 0.14 c=0.89; 1-10 Mathematics 13m/13p gold 0.07 Claude 0.11 c=0.93; NCEA1 11m/11p gold 0.10 Claude 0.13 c=0.90; Online Safety (OS9000) 9m/9p gold 0.15 Claude 0.21 c=0.85; 1-10 English 8m/8p gold 0.11 Claude 0.13 c=0.89; 1-10 Blended Literacy 6m/6p gold 0.30 Claude 0.31 c=0.70; 1-10 Social Science 6m/6p gold 0.13 Claude 0.29 c=0.87
- **ANZH401** ANZH401_0_0.html ↔ ANZH401_0.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH404** ANZH404_0_0.html ↔ ANZH404_0.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZHFUN05** MODULE_0_0.html ↔ ANZHFUN05_0_0.html: gold ['footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav fundamentals-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: ANZH401, ANZH404, ANZHFUN05, ART1004, ART1005, BLL114, BLL116, BLL174, BLL175, BLL176, BLL177, BLLR201, CBI1004, CEDO204, CEDO301, CEDT104, CEDT207, CEDT208, CEDT301, CHWHA, COM1002, ENG1004, ENGFUN02, ENGI101 …

### F28 · EXTRA `footer:links=prev-lesson,next-lesson,home-nav` — CANDIDATE (pages 246 / modules 102)
- by template+ptype: Standard/lesson 50m/175p gold 0.75 Claude 0.82 c=0.25; Inquiry/overview 22m/22p gold 0.18 Claude 0.67 c=0.82; Fundamentals/overview 12m/12p gold 0.07 Claude 0.25 c=0.93; Fundamentals/lesson 11m/18p gold 0.44 Claude 0.74 c=0.56; Inquiry/lesson 6m/16p gold 0.53 Claude 0.84 c=0.47; Bilingual/lesson 2m/2p gold 0.81 Claude 0.66 c=0.19; Standard/overview 1m/1p gold 0.03 Claude 0.01 c=0.97
- by subject: None 18m/25p gold 0.70 Claude 0.71 c=0.30; 1-10 Health and PE 12m/12p gold 0.20 Claude 1.00 c=0.80; NCEA1 10m/25p gold 0.72 Claude 0.77 c=0.28; ConnectED 10m/16p gold 0.68 Claude 0.81 c=0.32; Leaving to Learn 10m/39p gold 0.52 Claude 0.69 c=0.48; 1-10 Blended Literacy 9m/10p gold 0.40 Claude 0.38 c=0.60; 1-10 Mathematics 9m/52p gold 0.62 Claude 0.77 c=0.38; 1-10 English 8m/34p gold 0.62 Claude 0.71 c=0.38
- **AGH1008** AGH1008_8_0.html ↔ AGH1008.08.html: gold ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH401** ANZH401_1_0.html ↔ ANZH401_1.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH404** ANZH404_1_0.html ↔ ANZH404_1.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: AGH1008, ANZH401, ANZH404, ART1002, BLL120, BLL140, BLL150, BLL170, BLL175, BLL210, BLL220, BLL230, BLL240, BLLR202, CEDK101, CEDK102, CEDK501, CEDO102, CEDO202, CEDO301, CEDR204, CEDT207, CEDT301, CEDW201 …

### F29 · EXTRA `footer:links=prev-lesson,home-nav` — CANDIDATE (pages 94 / modules 94)
- by template+ptype: Standard/lesson 67m/67p gold 0.16 Claude 0.18 c=0.84; Fundamentals/lesson 13m/13p gold 0.04 Claude 0.26 c=0.96; Bilingual/lesson 11m/11p gold 0.15 Claude 0.34 c=0.85; Inquiry/lesson 3m/3p gold 0.22 Claude 0.16 c=0.78
- by subject: None 28m/28p gold 0.08 Claude 0.14 c=0.92; 1-10 Blended Literacy 16m/16p gold 0.25 Claude 0.31 c=0.75; 1-10 English 11m/11p gold 0.10 Claude 0.13 c=0.90; Te Marautanga o Aotearoa TMoA 10m/10p gold 0.11 Claude 0.25 c=0.89; 1-10 Mathematics 8m/8p gold 0.09 Claude 0.11 c=0.91; NCEA1 7m/7p gold 0.11 Claude 0.10 c=0.89; Leaving to Learn 4m/4p gold 0.29 Claude 0.15 c=0.71; ANZH 3m/3p gold 0.09 Claude 0.13 c=0.91
- **AGH1004** AGH1004_6_0.html ↔ AGH1004.07.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **AGH1009** AGH1009_9_0.html ↔ AGH1009.09.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH103** ANZH103_1_0.html ↔ ANZH103_3_0.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: AGH1004, AGH1009, ANZH103, ANZH205, ANZH301, ANZH302, ANZH303, BLL141, BLL146, BLL151, BLL157, BLL167, BLL171, BLL176, BLL177, BLL224, BLL225, BLL226, BLL227, BLL231, BLL234, BLL236, BLL237, BLLR201 …

### F30 · MISSING `footer:links=prev-lesson,next-lesson,home-nav` — CANDIDATE (pages 77 / modules 72)
- by template+ptype: Standard/lesson 53m/53p gold 0.75 Claude 0.82 c=0.75; Bilingual/lesson 10m/10p gold 0.81 Claude 0.66 c=0.81; Standard/overview 8m/8p gold 0.03 Claude 0.01 c=0.03; Bilingual/overview 3m/3p gold 0.17 Claude 0.00 c=0.17; Inquiry/lesson 1m/1p gold 0.53 Claude 0.84 c=0.53; Fundamentals/lesson 1m/1p gold 0.44 Claude 0.74 c=0.44; Fundamentals/overview 1m/1p gold 0.07 Claude 0.25 c=0.07
- by subject: None 19m/22p gold 0.70 Claude 0.71 c=0.70; 1-10 Blended Literacy 14m/14p gold 0.40 Claude 0.38 c=0.40; Te Marautanga o Aotearoa TMoA 9m/11p gold 0.64 Claude 0.49 c=0.64; NCEA1 8m/8p gold 0.72 Claude 0.77 c=0.72; 1-10 English 6m/6p gold 0.62 Claude 0.71 c=0.62; Leaving to Learn 4m/4p gold 0.52 Claude 0.69 c=0.52; ANZH 3m/3p gold 0.58 Claude 0.74 c=0.58; 1-10 Mathematics 3m/3p gold 0.62 Claude 0.77 c=0.62
- **AGH1004** AGH1004_6_0.html ↔ AGH1004.07.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **AGH1009** AGH1009_9_0.html ↔ AGH1009.09.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH103** ANZH103_1_0.html ↔ ANZH103_3_0.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: AGH1004, AGH1009, ANZH103, ANZH205, ANZH301, ANZH302, ANZH303, ART1005, BLL141, BLL146, BLL151, BLL157, BLL167, BLL171, BLL224, BLL225, BLL226, BLL227, BLL231, BLL234, BLL236, BLL237, BLLR201, CBI1004 …

### F31 · MISSING `footer:link=next-lesson` — CANDIDATE (pages 71 / modules 71)
- by template+ptype: Standard/lesson 58m/58p gold 0.83 Claude 0.82 c=0.83; Bilingual/lesson 10m/10p gold 0.81 Claude 0.66 c=0.81; Inquiry/lesson 2m/2p gold 0.69 Claude 0.84 c=0.69; Fundamentals/lesson 1m/1p gold 0.44 Claude 0.74 c=0.44
- by subject: 1-10 Blended Literacy 16m/16p gold 0.74 Claude 0.69 c=0.74; None 15m/15p gold 0.81 Claude 0.85 c=0.81; Te Marautanga o Aotearoa TMoA 9m/9p gold 0.86 Claude 0.75 c=0.86; 1-10 English 7m/7p gold 0.86 Claude 0.84 c=0.86; 1-10 Mathematics 7m/7p gold 0.90 Claude 0.88 c=0.90; NCEA1 5m/5p gold 0.87 Claude 0.90 c=0.87; ANZH 3m/3p gold 0.91 Claude 0.87 c=0.91; ConnectED 3m/3p gold 0.94 Claude 0.93 c=0.94
- **AGH1004** AGH1004_6_0.html ↔ AGH1004.07.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **AGH1009** AGH1009_9_0.html ↔ AGH1009.09.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZH103** ANZH103_1_0.html ↔ ANZH103_3_0.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: AGH1004, AGH1009, ANZH103, ANZH205, ANZH301, ANZH302, ANZH303, BLL141, BLL146, BLL151, BLL157, BLL167, BLL171, BLL176, BLL177, BLL224, BLL225, BLL226, BLL227, BLL231, BLL234, BLL236, BLL237, BLLR201 …

### F33 · EXTRA `footer:link=next-lesson` — CANDIDATE (pages 107 / modules 57)
- by template+ptype: Standard/lesson 24m/52p gold 0.83 Claude 0.82 c=0.17; Fundamentals/overview 11m/11p gold 0.30 Claude 0.48 c=0.70; Fundamentals/lesson 11m/18p gold 0.44 Claude 0.74 c=0.56; Standard/overview 8m/8p gold 0.98 Claude 1.00 c=0.02; Inquiry/overview 7m/7p gold 0.80 Claude 0.96 c=0.20; Inquiry/lesson 2m/9p gold 0.69 Claude 0.84 c=0.31; Bilingual/lesson 2m/2p gold 0.81 Claude 0.66 c=0.19
- by subject: None 23m/31p gold 0.81 Claude 0.85 c=0.19; Leaving to Learn 11m/45p gold 0.65 Claude 0.85 c=0.35; NCEA1 7m/15p gold 0.87 Claude 0.90 c=0.13; 1-10 Social Science 6m/6p gold 0.79 Claude 0.95 c=0.21; 1-10 Blended Literacy 3m/3p gold 0.74 Claude 0.69 c=0.26; 1-10 English 2m/2p gold 0.86 Claude 0.84 c=0.14; Te Marautanga o Aotearoa TMoA 2m/2p gold 0.86 Claude 0.75 c=0.14; ConnectED 1m/1p gold 0.94 Claude 0.93 c=0.06
- **AGH1008** AGH1008_8_0.html ↔ AGH1008.08.html: gold ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ANZHFUN05** MODULE_0_0.html ↔ ANZHFUN05_0_0.html: gold ['footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav fundamentals-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ART1002** ART1002_5_0.html ↔ ART1002_2.0.html: gold ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- modules: AGH1008, ANZHFUN05, ART1002, ART1004, BLL120, BLL140, BLL150, BLLR202, CEDO301, CHI1004, CHWHA, COM1005, ENGC403, ENGFUN02, ENGI401, ENGS201, EXPFUN07, FRFUN06, FRFUN07, FRFUN08, GEWHA, HES1005, HES1007, HIS1005 …

### F34 · EXTRA `footer:link=prev-lesson` — CANDIDATE (pages 65 / modules 49)
- by template+ptype: Fundamentals/lesson 22m/30p gold 0.47 Claude 1.00 c=0.53; Standard/lesson 18m/22p gold 0.99 Claude 1.00 c=0.01; Inquiry/overview 4m/4p gold 0.71 Claude 0.71 c=0.29; Inquiry/lesson 3m/6p gold 0.88 Claude 1.00 c=0.12; Standard/overview 1m/1p gold 0.03 Claude 0.01 c=0.97; Bilingual/lesson 1m/2p gold 0.96 Claude 1.00 c=0.04
- by subject: None 25m/33p gold 0.79 Claude 0.84 c=0.21; 1-10 Blended Literacy 7m/7p gold 0.66 Claude 0.69 c=0.34; NCEA1 5m/8p gold 0.86 Claude 0.87 c=0.14; EXPlore 3m/3p gold 0.73 Claude 0.93 c=0.27; ConnectED 2m/2p gold 0.92 Claude 0.91 c=0.08; 1-10 Mathematics 2m/2p gold 0.88 Claude 0.88 c=0.12; Leaving to Learn 2m/6p gold 0.81 Claude 0.83 c=0.19; 1-10 English 1m/1p gold 0.84 Claude 0.84 c=0.16
- **BLL120** BLL120_0_0.html ↔ BLL120.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL140** BLL140_0_0.html ↔ BLL140.html: gold ['footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL150** BLL150_0_0.html ↔ BLL150.html: gold ['footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL120, BLL140, BLL150, BLL175, BLL176, BLL177, BLL240, CEDK501, CEDT207, CHI1004, COM1005, ENGFUN02, ENGR102, EXBP901, EXIP901, EXPFUN07, FRFUN06, GEO1004, HES1006, HIS1002, HIS1003, JPFUN01, MXEX101, MXFL201 …

### F35 · MISSING `footer:links=home-nav,prev-lesson,next-lesson` — CANDIDATE (pages 112 / modules 47)
- by template+ptype: Inquiry/overview 22m/22p gold 0.53 Claude 0.04 c=0.53; Fundamentals/overview 12m/12p gold 0.20 Claude 0.00 c=0.20; Standard/lesson 11m/76p gold 0.04 Claude 0.00 c=0.04; Inquiry/lesson 2m/2p gold 0.04 Claude 0.00 c=0.04
- by subject: 1-10 Health and PE 12m/12p gold 0.80 Claude 0.00 c=0.80; ConnectED 11m/11p gold 0.12 Claude 0.02 c=0.12; Te ara Whakapuawa -Wellbeing 6m/6p gold 0.75 Claude 0.00 c=0.75; 1-10 Blended Literacy 5m/5p gold 0.02 Claude 0.00 c=0.02; 1-10 English 5m/32p gold 0.10 Claude 0.00 c=0.10; 1-10 Mathematics 5m/40p gold 0.12 Claude 0.00 c=0.12; None 1m/1p gold 0.00 Claude 0.00 c=0.00; EXPlore 1m/1p gold 0.07 Claude 0.00 c=0.07
- **BLL170** BLL170_0_0.html ↔ BLL170.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=home-nav,prev-lesson,next-lesson', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL210** BLL210_0_0.html ↔ BLL210.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=home-nav,prev-lesson,next-lesson', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL220** BLL220_0_0.html ↔ BLL220.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=home-nav,prev-lesson,next-lesson', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL170, BLL210, BLL220, BLL230, BLL240, CEDK101, CEDK102, CEDK501, CEDO102, CEDO202, CEDO204, CEDR204, CEDT104, CEDT207, CEDT208, CEDT301, CEDW201, ENGJ101, ENGJ301, ENGJ302, ENGJ402, ENGJ403, EXPFUN06, HPFUN101 …

### F36 · MISSING `footer:links=home-nav` — CANDIDATE (pages 60 / modules 47)
- by template+ptype: Fundamentals/lesson 22m/30p gold 0.53 Claude 0.00 c=0.53; Fundamentals/overview 11m/11p gold 0.68 Claude 0.52 c=0.68; Inquiry/overview 7m/7p gold 0.20 Claude 0.04 c=0.20; Standard/overview 6m/6p gold 0.02 Claude 0.00 c=0.02; Standard/lesson 2m/2p gold 0.00 Claude 0.00 c=0.00; Inquiry/lesson 1m/4p gold 0.08 Claude 0.00 c=0.08
- by subject: None 30m/39p gold 0.10 Claude 0.01 c=0.10; 1-10 Social Science 6m/6p gold 0.16 Claude 0.00 c=0.16; Leaving to Learn 6m/6p gold 0.03 Claude 0.00 c=0.03; 1-10 Blended Literacy 3m/3p gold 0.01 Claude 0.00 c=0.01; NCEA1 1m/5p gold 0.01 Claude 0.00 c=0.01; EXPlore 1m/1p gold 0.07 Claude 0.00 c=0.07
- **ANZHFUN05** MODULE_0_0.html ↔ ANZHFUN05_0_0.html: gold ['footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav fundamentals-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **BLL120** BLL120_0_0.html ↔ BLL120.html: gold ['footer:inside-body', 'footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL140** BLL140_0_0.html ↔ BLL140.html: gold ['footer:link=home-nav', 'footer:links=home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: ANZHFUN05, BLL120, BLL140, BLL150, CHI1004, CHWHA, ENGFUN02, EXPFUN07, FRFUN06, FRFUN07, FRFUN08, GEWHA, JPFUN01, JPFUN02, SSFUN01, SSFUN03, SSFUN05, SSFUN06, SSFUN07, SSFUN08, WJFUN105, WJFUN106, WJFUN107, WJFUN108 …

### F37 · MISSING `footer:ul=footer-nav` — CANDIDATE (pages 75 / modules 26)
- by template+ptype: Standard/lesson 14m/36p gold 0.90 Claude 0.89 c=0.90; Standard/overview 11m/11p gold 0.76 Claude 0.73 c=0.76; Fundamentals/overview 8m/8p gold 0.45 Claude 0.42 c=0.45; Inquiry/overview 3m/3p gold 0.16 Claude 0.18 c=0.16; Inquiry/lesson 3m/17p gold 0.96 Claude 0.61 c=0.96
- by subject: 1-10 Blended Literacy 12m/41p gold 0.16 Claude 0.00 c=0.16; 1-10 Technology 5m/5p gold 0.62 Claude 0.00 c=0.62; ConnectED 4m/21p gold 0.87 Claude 0.69 c=0.87; EXPlore 2m/5p gold 0.53 Claude 0.27 c=0.53; 1-10 Mathematics 2m/2p gold 0.98 Claude 0.99 c=0.98; 1-10 Health and PE 1m/1p gold 0.27 Claude 0.20 c=0.27
- **BLL121** BLL121_0_0.html ↔ BLL121-01.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL172** BLL172_0_0.html ↔ BLL172-00.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL174** BLL174_0_0.html ↔ BLL174-00.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL121, BLL172, BLL174, BLL175, BLL176, BLL177, BLL236, BLL237, BLL240, BLL241, BLL244, BLL245, CEDR501, CEDT207, CEDT301, CEDW101, EXBP901, EXIP901, HPFUN301, MXFUN02, MXFUN03, TEFUN01, TEFUN02, TEFUN05 …

### F39 · EXTRA `footer:ul=footer-nav inquiry-nav` — CANDIDATE (pages 85 / modules 22)
- by template+ptype: Standard/lesson 15m/41p gold 0.10 Claude 0.11 c=0.91; Standard/overview 12m/12p gold 0.23 Claude 0.27 c=0.77; Inquiry/overview 3m/3p gold 0.84 Claude 0.82 c=0.16; Inquiry/lesson 3m/17p gold 0.04 Claude 0.39 c=0.96; Fundamentals/overview 3m/3p gold 0.00 Claude 0.05 c=1.00; Fundamentals/lesson 1m/9p gold 0.00 Claude 0.16 c=1.00
- by subject: 1-10 Blended Literacy 12m/41p gold 0.84 Claude 1.00 c=0.16; ConnectED 4m/21p gold 0.13 Claude 0.31 c=0.87; EXPlore 2m/5p gold 0.47 Claude 0.73 c=0.53; 1-10 Mathematics 2m/2p gold 0.02 Claude 0.01 c=0.98; None 1m/10p gold 0.06 Claude 0.07 c=0.94; Leaving to Learn 1m/6p gold 0.02 Claude 0.04 c=0.98
- **BLL121** BLL121_0_0.html ↔ BLL121-01.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL172** BLL172_0_0.html ↔ BLL172-00.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- **BLL174** BLL174_0_0.html ↔ BLL174-00.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=home-nav,next-lesson', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: BLL121, BLL172, BLL174, BLL175, BLL176, BLL177, BLL236, BLL237, BLL240, BLL241, BLL244, BLL245, CEDR501, CEDT207, CEDT301, CEDW101, EXBP901, EXIP901, FRFUN06, MXFUN02, MXFUN03, XWHA02

### F41 · MISSING `footer:link=prev-lesson` — CANDIDATE (pages 20 / modules 19)
- by template+ptype: Standard/overview 10m/10p gold 0.03 Claude 0.01 c=0.03; Inquiry/overview 4m/4p gold 0.71 Claude 0.71 c=0.71; Bilingual/overview 3m/3p gold 0.17 Claude 0.00 c=0.17; Standard/lesson 2m/2p gold 0.99 Claude 1.00 c=0.99; Fundamentals/overview 1m/1p gold 0.27 Claude 0.25 c=0.27
- by subject: None 7m/8p gold 0.79 Claude 0.84 c=0.79; NCEA1 4m/4p gold 0.86 Claude 0.87 c=0.86; ConnectED 3m/3p gold 0.92 Claude 0.91 c=0.92; Te Marautanga o Aotearoa TMoA 2m/2p gold 0.75 Claude 0.75 c=0.75; 1-10 Mathematics 1m/1p gold 0.88 Claude 0.88 c=0.88; 1-10 Social Science 1m/1p gold 0.71 Claude 0.71 c=0.71; Leaving to Learn 1m/1p gold 0.81 Claude 0.83 c=0.81
- **ART1004** ART1004_0_0.html ↔ ART1004_4.0.html: gold ['footer:link=home-nav', 'footer:link=prev-lesson', 'footer:links=prev-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **ART1005** ART1005_0_0.html ↔ ART1005_3.0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav']
- **BLLR201** BLLR201_0_0.html ↔ BLLR201_0_0.html: gold ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:link=prev-lesson', 'footer:links=prev-lesson,next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav'] · Claude ['footer:link=home-nav', 'footer:link=next-lesson', 'footer:links=next-lesson,home-nav', 'footer:present', 'footer:ul=footer-nav inquiry-nav']
- modules: ART1004, ART1005, BLLR201, CBI1004, CEDO204, CEDT104, CEDT207, CEDT208, COM1002, ENG1004, GEO1004, MXFL101, PES1002, PWYWHA1, SSFUN02, TRR112, TRR113, TRR116, XGF9001


## The ranked queue — chrome regions first, then by modules affected

| # | region | dir | parent | gold form | Claude form | pages | modules | consensus (all) | best group | derivable | KB | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | module-code | EXTRA | `div#header` | `—` | `div#module-code` | 4 | 4 | 0.03 of 2349 | — | structure | yes | BELOW FLOOR |
| 2 | module-code | MISSING | `div#header` | `div#module-code` | `—` | 3 | 3 | 0.97 of 2349 | — | structure | yes | BELOW FLOOR |
| 3 | module-code | EXTRA | `div#module-code` | `—` | `h1` | 1 | 1 | 0.03 of 2349 | — | structure | yes | BELOW FLOOR |
| 4 | title | MISSING | `div#header` | `h1>span` | `—` | 257 | 138 | 0.23 of 2349 | subject+ptype=1-10 English/overview c=0.94 n=17 | 0.74 | yes | CANDIDATE |
| 5 | title | EXTRA | `div#header` | `—` | `h1>span` | 15 | 14 | 0.77 of 2349 | template=Standard c=0.82 n=11 | structure | yes | CANDIDATE |
| 6 | title | SUBSTITUTED | `div#header` | `h1>span` | `div#module-head-buttons` | 5 | 5 | 1.00 of 2349 | — | structure | yes | BELOW FLOOR |
| 7 | title | MISSING | `span>span.sassoonI-text` | `span.sassoonI-text` | `—` | 14 | 4 | 0.01 of 2349 | — | 0.79 | — | BELOW FLOOR |
| 8 | title | MISSING | `div#header` | `h1>span.ch-text` | `—` | 21 | 3 | 0.01 of 2349 | — | 0.00 | yes | BELOW FLOOR |
| 9 | title | MISSING | `span` | `apan.jp-text` | `—` | 10 | 1 | 0.00 of 2349 | — | 0.90 | yes | BELOW FLOOR |
| 10 | title | MISSING | `div.titlebar` | `h1.moduleTitle>span.module-subtitle.text-lowercase` | `—` | 2 | 1 | 0.00 of 2349 | — | 1.00 | — | BELOW FLOOR |
| 11 | title | EXTRA | `span>span` | `—` | `span` | 1 | 1 | 0.99 of 2349 | — | structure | — | BELOW FLOOR |
| 12 | title | EXTRA | `h1>span` | `—` | `span` | 1 | 1 | 0.01 of 2349 | — | structure | — | BELOW FLOOR |
| 13 | title | EXTRA | `msub` | `—` | `mrow` | 1 | 1 | 1.00 of 2349 | — | structure | — | BELOW FLOOR |
| 14 | title | EXTRA | `mfrac` | `—` | `mrow` | 1 | 1 | 1.00 of 2349 | — | structure | — | BELOW FLOOR |
| 15 | title | EXTRA | `mrow` | `—` | `mi` | 1 | 1 | 1.00 of 2349 | — | structure | — | BELOW FLOOR |
| 16 | title | EXTRA | `msup` | `—` | `mrow` | 1 | 1 | 1.00 of 2349 | — | structure | — | BELOW FLOOR |
| 17 | title | MISSING | `span>span` | `span` | `—` | 1 | 1 | 0.01 of 2349 | — | 1.00 | — | BELOW FLOOR |
| 18 | title | MISSING | `span>span.text-lowercase` | `span.text-lowercase` | `—` | 1 | 1 | 0.00 of 2349 | — | 1.00 | — | BELOW FLOOR |
| 19 | title | MISSING | `div#header` | `h1>span.jp-text` | `—` | 1 | 1 | 0.00 of 2349 | — | 1.00 | yes | BELOW FLOOR |
| 20 | title | MISSING | `msup` | `mn` | `—` | 1 | 1 | 0.00 of 2349 | — | 1.00 | — | BELOW FLOOR |
| 21 | title | SUBSTITUTED | `msub` | `mi` | `mrow` | 1 | 1 | 0.00 of 2349 | — | structure | — | BELOW FLOOR |
| 22 | title | SUBSTITUTED | `msub` | `mi` | `mi` | 1 | 1 | 0.00 of 2349 | — | structure | — | BELOW FLOOR |
| 23 | title | SUBSTITUTED | `mfrac` | `mn` | `mrow` | 1 | 1 | 0.00 of 2349 | — | structure | — | BELOW FLOOR |
| 24 | title | SUBSTITUTED | `mfrac` | `mn` | `mn` | 1 | 1 | 0.00 of 2349 | — | structure | — | BELOW FLOOR |
| 25 | title | SUBSTITUTED | `msup` | `mi` | `mrow` | 1 | 1 | 0.00 of 2349 | — | structure | — | BELOW FLOOR |
| 26 | title | SUBSTITUTED | `div#header` | `h1>span` | `div#module-code` | 1 | 1 | 1.00 of 2349 | — | structure | yes | BELOW FLOOR |
| 27 | header | MISSING | `div#header` | `p` | `—` | 3 | 1 | 0.00 of 2349 | — | 0.00 | yes | BELOW FLOOR |
| 28 | header | SUBSTITUTED | `div#header` | `div.titlebar` | `h1>span` | 2 | 1 | 0.00 of 2349 | — | structure | yes | BELOW FLOOR |
| 29 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `p` | `h5` | 83 | 83 | 0.06 of 2349 | subject=1-10 Health and PE c=0.93 n=14 | structure | yes | CANDIDATE |
| 30 | module-menu | MISSING | `ul` | `li` | `—` | 114 | 76 | 0.10 of 2349 | subject+ptype=1-10 Blended Literacy/overview c=0.66 n=21 | 0.89 | — | CANDIDATE |
| 31 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-6.paddingR` | 69 | 52 | 0.97 of 2349 | era=Refresh c=0.97 n=52 | structure | yes | CANDIDATE |
| 32 | module-menu | MISSING | `div.col-12.col-md-8` | `ul` | `—` | 196 | 49 | 0.29 of 2349 | — | 0.91 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 33 | module-menu | EXTRA | `div#header` | `—` | `div#module-menu-content.moduleMenu` | 115 | 45 | 0.25 of 2349 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 34 | module-menu | MISSING | `div.col-12.col-md-8` | `p` | `—` | 205 | 44 | 0.10 of 2349 | — | 0.84 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 35 | module-menu | MISSING | `div.col-12.col-md-8` | `h5` | `—` | 195 | 43 | 0.24 of 2349 | — | 0.83 | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 36 | module-menu | EXTRA | `ul` | `—` | `li` | 81 | 43 | 0.79 of 2349 | ptype=lesson c=0.83 n=15 | structure | — | CANDIDATE |
| 37 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingL` | `p` | `h5` | 38 | 38 | 0.03 of 2349 | subject=1-10 Health and PE c=0.93 n=14 | structure | yes | CANDIDATE |
| 38 | module-menu | EXTRA | `div#header` | `—` | `div#module-head-buttons` | 102 | 37 | 0.23 of 2349 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 39 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `p` | `—` | 50 | 37 | 0.04 of 2349 | subject+ptype=1-10 Blended Literacy/overview c=0.78 n=23 | 0.71 | yes | CANDIDATE |
| 40 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `h5` | 86 | 36 | 0.76 of 2349 | era=Refresh c=0.76 n=36 | structure | — | CANDIDATE |
| 41 | module-menu | MOVED | `ul` | `li` | `li>i` | 95 | 34 | 0.26 of 2349 | — | structure | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 42 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 67 | 29 | 0.87 of 2349 | era=Refresh c=0.87 n=29 | structure | — | CANDIDATE |
| 43 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-8` | 110 | 28 | 0.66 of 2349 | template+ptype=Fundamentals/lesson c=1.00 n=13 | structure | — | CANDIDATE |
| 44 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `ul` | 53 | 27 | 0.71 of 2349 | era=Refresh c=0.71 n=27 | structure | — | CANDIDATE |
| 45 | module-menu | MISSING | `div#header` | `div#module-head-buttons` | `—` | 65 | 22 | 0.77 of 2349 | template=Standard c=0.78 n=15 | structure | yes | CANDIDATE |
| 46 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `ul` | `—` | 30 | 22 | 0.05 of 2349 | — | 0.77 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 47 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `p>b` | 22 | 22 | 1.00 of 2349 | era=Refresh c=1.00 n=22 | structure | yes | CANDIDATE |
| 48 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6.paddingL` | `—` | 40 | 21 | 0.04 of 2349 | — | 1.00 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 49 | module-menu | SUBSTITUTED | `ul` | `li` | `li` | 84 | 20 | 0.58 of 2349 | template+ptype=Standard/lesson c=0.64 n=16 | structure | — | CANDIDATE |
| 50 | module-menu | MISSING | `p` | `br` | `—` | 35 | 20 | 0.01 of 2349 | — | structure | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 51 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `p` | `h5` | 26 | 20 | 0.04 of 2349 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 52 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `h4>span` | `—` | 20 | 20 | 0.01 of 2349 | — | 1.00 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 53 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `—` | 87 | 19 | 0.03 of 2349 | — | 0.96 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 54 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6.offset-md-0` | `—` | 78 | 19 | 0.05 of 2349 | — | 0.87 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 55 | module-menu | SUBSTITUTED | `div.row` | `WIDGET` | `div.col-12.col-md-8` | 32 | 19 | 0.12 of 2349 | — | structure | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 56 | module-menu | EXTRA | `div.col-12.col-md-6.offset-md-0` | `—` | `p` | 24 | 18 | 0.99 of 2349 | era=Refresh c=0.99 n=18 | structure | yes | CANDIDATE |
| 57 | module-menu | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `h5` | 62 | 17 | 0.13 of 2349 | — | structure | — | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 58 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `p` | 17 | 17 | 0.95 of 2349 | template=Standard c=0.95 n=14 | structure | yes | CANDIDATE |
| 59 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-6.offset-md-0` | 32 | 16 | 0.95 of 2349 | era=Refresh c=0.95 n=16 | structure | yes | CANDIDATE |
| 60 | module-menu | EXTRA | `div.row` | `—` | `div.col-12.col-md-12.paddingR` | 18 | 16 | 0.96 of 2349 | template=Standard c=0.96 n=16 | structure | yes | CANDIDATE |
| 61 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `h4>span` | `h5>span` | 15 | 15 | 0.03 of 2349 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 62 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0` | `ul` | `—` | 71 | 14 | 0.02 of 2349 | — | 0.83 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 63 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.paddingR` | `ul` | `p>b` | 14 | 14 | 0.06 of 2349 | subject+ptype=1-10 Blended Literacy/overview c=0.85 n=14 | structure | yes | CANDIDATE |
| 64 | module-menu | MISSING | `div#module-menu-content.moduleMenu` | `ul` | `—` | 88 | 13 | 0.04 of 2349 | — | 0.91 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 65 | module-menu | SUBSTITUTED | `div#module-menu-content.moduleMenu` | `h5` | `div.row` | 82 | 13 | 0.04 of 2349 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 66 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.paddingR` | `div.col-12.col-md-12.paddingR` | 13 | 13 | 0.07 of 2349 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 67 | module-menu | SUBSTITUTED | `div#module-menu-content.moduleMenu` | `div.item` | `div.row` | 82 | 12 | 0.04 of 2349 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 68 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `h5` | 14 | 12 | 0.99 of 2349 | ptype=overview c=1.00 n=10 | structure | yes | CANDIDATE |
| 69 | module-menu | EXTRA | `div.col-12.col-md-12.paddingR` | `—` | `h4>span` | 12 | 12 | 0.97 of 2349 | template=Standard c=0.98 n=10 | structure | yes | CANDIDATE |
| 70 | module-menu | MISSING | `div.row` | `div.col-12.col-md-6.offset-md-0.paddingL` | `—` | 12 | 12 | 0.01 of 2349 | — | 0.42 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 71 | module-menu | MISSING | `div#header` | `div#module-menu-content.moduleMenu` | `—` | 41 | 11 | 0.75 of 2349 | era=Refresh c=0.75 n=11 | 1.00 | yes | CANDIDATE |
| 72 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.paddingL` | `div.col-12.col-md-6.paddingR` | 11 | 11 | 0.04 of 2349 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 73 | module-menu | MISSING | `div.col-12.col-md-6.offset-md-0` | `p` | `—` | 48 | 10 | 0.02 of 2349 | — | 0.75 | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 74 | module-menu | EXTRA | `li>b` | `—` | `b` | 23 | 10 | 0.99 of 2349 | era=Refresh c=0.99 n=10 | structure | — | CANDIDATE |
| 75 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `h5` | 17 | 10 | 0.04 of 2349 | — | structure | yes | BELOW CONSENSUS (no group ≥ 0.60 at the floor) |
| 76 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `h5>span` | 10 | 10 | 0.97 of 2349 | era=Refresh c=0.97 n=10 | structure | yes | CANDIDATE |
| 77 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-8.paddingR` | `div.col-12.col-md-8` | 70 | 9 | 0.03 of 2349 | — | structure | yes | BELOW FLOOR |
| 78 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.offset-md-0` | `div.col-12.col-md-8` | 56 | 9 | 0.05 of 2349 | — | structure | yes | BELOW FLOOR |
| 79 | module-menu | MISSING | `div.col-12.col-md-8.paddingR` | `ul` | `—` | 48 | 9 | 0.02 of 2349 | — | 0.99 | yes | BELOW FLOOR |
| 80 | module-menu | MISSING | `div#module-menu-content.moduleMenu` | `h5` | `—` | 45 | 9 | 0.04 of 2349 | — | 0.71 | yes | BELOW FLOOR |
| 81 | module-menu | MOVED | `ul` | `li` | `li` | 37 | 9 | 0.35 of 2349 | — | structure | — | BELOW FLOOR |
| 82 | module-menu | EXTRA | `div.col-12.col-md-6.offset-md-0` | `—` | `ul` | 9 | 9 | 0.98 of 2349 | — | structure | yes | BELOW FLOOR |
| 83 | module-menu | MISSING | `div.col-12.col-md-6.paddingR` | `h5>span` | `—` | 9 | 9 | 0.03 of 2349 | — | 1.00 | yes | BELOW FLOOR |
| 84 | module-menu | SUBSTITUTED | `div.col-12.col-md-6` | `h4>span` | `h5>span` | 9 | 9 | 0.01 of 2349 | — | structure | yes | BELOW FLOOR |
| 85 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `h3>span` | `h4>span` | 11 | 8 | 0.04 of 2349 | — | structure | yes | BELOW FLOOR |
| 86 | module-menu | EXTRA | `p>b` | `—` | `b` | 8 | 8 | 0.99 of 2349 | — | structure | — | BELOW FLOOR |
| 87 | module-menu | EXTRA | `div.col-12.col-md-6.paddingL` | `—` | `h5` | 8 | 8 | 1.00 of 2349 | — | structure | yes | BELOW FLOOR |
| 88 | module-menu | MISSING | `h5>span` | `span` | `—` | 8 | 8 | 0.03 of 2349 | — | 1.00 | — | BELOW FLOOR |
| 89 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0.paddingR` | `p` | `h5` | 8 | 8 | 0.01 of 2349 | — | structure | yes | BELOW FLOOR |
| 90 | module-menu | SUBSTITUTED | `div.row` | `div.col-12` | `div.col-12.col-md-8` | 51 | 7 | 0.02 of 2349 | — | structure | — | BELOW FLOOR |
| 91 | module-menu | SUBSTITUTED | `div.item` | `div.row` | `div.col-12.col-md-8` | 42 | 7 | 0.03 of 2349 | — | structure | yes | BELOW FLOOR |
| 92 | module-menu | MOVED | `div#module-menu-content.moduleMenu` | `h5` | `h5` | 35 | 7 | 0.04 of 2349 | — | structure | yes | BELOW FLOOR |
| 93 | module-menu | SUBSTITUTED | `div.col-12.col-md-6.offset-md-0` | `ul` | `p` | 15 | 7 | 0.05 of 2349 | — | structure | yes | BELOW FLOOR |
| 94 | module-menu | MOVED | `div.col-12.col-md-8` | `p` | `p` | 12 | 7 | 0.13 of 2349 | — | structure | — | BELOW FLOOR |
| 95 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-6.offset-md-0` | `div.col-12.col-md-12.paddingR` | 10 | 7 | 0.05 of 2349 | — | structure | yes | BELOW FLOOR |
| 96 | module-menu | EXTRA | `div.col-12.col-md-6.paddingR` | `—` | `ul` | 7 | 7 | 1.00 of 2349 | — | structure | yes | BELOW FLOOR |
| 97 | module-menu | EXTRA | `div.col-12.col-md-8` | `—` | `p>b` | 7 | 7 | 0.98 of 2349 | — | structure | — | BELOW FLOOR |
| 98 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-12` | `div.col-12.col-md-12.paddingR` | 7 | 7 | 0.01 of 2349 | — | structure | yes | BELOW FLOOR |
| 99 | module-menu | MISSING | `div.col-12.col-md-8.paddingR` | `h5` | `—` | 30 | 6 | 0.02 of 2349 | — | 1.00 | yes | BELOW FLOOR |
| 100 | module-menu | SUBSTITUTED | `div.row` | `div.col-12.col-md-12.paddingR` | `div.col-12.col-md-8` | 30 | 6 | 0.04 of 2349 | — | structure | yes | BELOW FLOOR |
| 444 | footer | MISSING | `ul.footer-nav` | `li>a.home-nav` | `—` | 107 | 64 | 0.85 of 2349 | subject=1-10 English c=1.00 n=12 | structure | yes | CANDIDATE |
| 445 | footer | MISSING | `ul.footer-nav` | `li>a#next-lesson` | `—` | 97 | 60 | 0.73 of 2349 | subject+ptype=1-10 Mathematics/overview c=0.93 n=12 | structure | yes | CANDIDATE |
| 446 | footer | MISSING | `li>a#next-lesson` | `a#next-lesson` | `—` | 58 | 58 | 0.82 of 2349 | template=Bilingual c=0.86 n=10 | structure | yes | CANDIDATE |
| 447 | footer | MISSING | `ul.footer-nav.inquiry-nav` | `li>a.home-nav` | `—` | 38 | 33 | 0.12 of 2349 | subject+ptype=1-10 Blended Literacy/overview c=0.87 n=20 | structure | yes | CANDIDATE |
| 450 | footer | EXTRA | `li>a#prev-lesson` | `—` | `a#prev-lesson` | 25 | 22 | 0.19 of 2349 | series=WJFUN c=1.00 n=12 | structure | yes | CANDIDATE |
| 451 | footer | EXTRA | `ul.footer-nav` | `—` | `li>a#next-lesson` | 24 | 22 | 0.27 of 2349 | series=WJFUN c=1.00 n=10 | structure | yes | CANDIDATE |
| 452 | footer | MISSING | `ul.footer-nav` | `li>a#prev-lesson` | `—` | 38 | 21 | 0.72 of 2349 | template+ptype=Standard/lesson c=0.89 n=13 | structure | yes | CANDIDATE |
| 453 | footer | EXTRA | `ul.footer-nav.inquiry-nav` | `—` | `li>a.home-nav` | 19 | 19 | 0.88 of 2349 | era=Refresh c=0.88 n=19 | structure | yes | CANDIDATE |
| 454 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav` | `ul.footer-nav.inquiry-nav` | 64 | 18 | 0.85 of 2349 | template+ptype=Standard/lesson c=0.90 n=12 | structure | yes | CANDIDATE |
| 455 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav` | `ul.footer-nav` | 18 | 17 | 0.85 of 2349 | template+ptype=Standard/lesson c=0.90 n=10 | structure | yes | CANDIDATE |
| 456 | footer | SUBSTITUTED | `ul.footer-nav.inquiry-nav` | `li>a#next-lesson` | `li>a.home-nav` | 16 | 16 | 0.09 of 2349 | subject+ptype=1-10 Blended Literacy/overview c=0.83 n=15 | structure | yes | CANDIDATE |
| 458 | footer | SUBSTITUTED | `div#footer` | `ul.footer-nav.inquiry-nav` | `li>a#next-lesson` | 15 | 15 | 0.12 of 2349 | subject+ptype=1-10 Blended Literacy/overview c=0.87 n=15 | structure | yes | CANDIDATE |
| 459 | footer | MISSING | `li>a.home-nav` | `a.home-nav` | `—` | 25 | 14 | 0.99 of 2349 | era=Refresh c=0.99 n=14 | structure | yes | CANDIDATE |
| 460 | footer | EXTRA | `div#footer` | `—` | `ul.footer-nav.inquiry-nav` | 15 | 13 | 0.88 of 2349 | template=Standard c=0.88 n=10 | structure | yes | CANDIDATE |
| 461 | footer | SUBSTITUTED | `ul.footer-nav` | `li>a#next-lesson` | `li>a#next-lesson` | 14 | 13 | 0.73 of 2349 | template=Standard c=0.76 n=11 | structure | yes | CANDIDATE |
| 464 | footer | SUBSTITUTED | `ul.footer-nav` | `li>a.home-nav` | `li>a.home-nav` | 13 | 11 | 0.85 of 2349 | era=Refresh c=0.85 n=11 | structure | yes | CANDIDATE |
| 465 | footer | MISSING | `div#footer` | `ul.footer-nav` | `—` | 11 | 11 | 0.85 of 2349 | template=Standard c=0.88 n=10 | structure | yes | CANDIDATE |
| 466 | footer | EXTRA | `ul.footer-nav.fundamentals-nav` | `—` | `li>a.home-nav` | 10 | 10 | 0.98 of 2349 | era=Refresh c=0.98 n=10 | structure | yes | CANDIDATE |
| 551 | acks | SUBSTITUTED | `div.col-12.col-md-8` | `div.acks` | `div.acks.acksTemplate` | 89 | 89 | 0.15 of 2349 | template+ptype=Inquiry/overview c=0.82 n=29 | structure | yes | CANDIDATE |
| 581 | activity | MISSING | `div.col-12` | `p` | `—` | 717 | 335 | 0.29 of 2342 | subject+ptype=1-10 Blended Literacy/lesson c=0.78 n=98 | 0.80 | — | CANDIDATE |
| 582 | activity | EXTRA | `div.col-12` | `—` | `p` | 565 | 276 | 0.88 of 2342 | series=XDLS90 c=1.00 n=22 | structure | — | CANDIDATE |
| 585 | activity | MISSING | `div.col-12` | `a` | `—` | 429 | 216 | 0.29 of 2342 | series=HIS10 c=0.71 n=40 | 0.62 | — | CANDIDATE |
| 586 | activity | MISSING | `div.col-12` | `h3` | `—` | 387 | 188 | 0.43 of 2342 | template+ptype=Fundamentals/overview c=0.87 n=21 | 0.70 | — | CANDIDATE |
| 587 | activity | EXTRA | `div.col-12` | `—` | `WIDGET` | 313 | 188 | 0.82 of 2342 | subject=NCEA1 c=0.97 n=29 | structure | — | CANDIDATE |
| 588 | activity | MOVED | `div.col-12` | `p` | `p` | 287 | 184 | 0.19 of 2342 | template+ptype=Fundamentals/overview c=0.60 n=24 | structure | — | CANDIDATE |
| 589 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `div.activity[number=*]` | 241 | 163 | 0.42 of 2342 | subject+ptype=1-10 Blended Literacy/lesson c=0.72 n=53 | structure | yes | CANDIDATE |
| 592 | activity | EXTRA | `div.col-12` | `—` | `img.img-fluid` | 226 | 139 | 0.97 of 2342 | subject=1-10 English c=0.99 n=22 | structure | — | CANDIDATE |
| 593 | activity | MOVED | `div.col-12` | `p` | `p` | 166 | 133 | 0.15 of 2342 | template+ptype=Inquiry/overview c=0.71 n=21 | structure | — | CANDIDATE |
| 594 | activity | EXTRA | `div.row` | `—` | `div.col-12` | 181 | 132 | 0.83 of 2342 | series=XDLS90 c=0.97 n=21 | structure | — | CANDIDATE |
| 596 | activity | EXTRA | `div.activity[number=*]` | `—` | `div.row` | 149 | 104 | 0.94 of 2342 | template=Standard c=0.96 n=121 | structure | yes | CANDIDATE |
| 599 | activity | EXTRA | `div.col-12` | `—` | `p>a` | 126 | 101 | 1.00 of 2342 | subject+ptype=1-10 Blended Literacy/lesson c=1.00 n=33 | structure | — | CANDIDATE |
| 600 | activity | EXTRA | `div.activity.interactive[number=*]` | `—` | `div.row` | 128 | 100 | 0.79 of 2342 | subject=NCEA1 c=0.93 n=22 | structure | yes | CANDIDATE |
| 603 | activity | SUBSTITUTED | `div.col-12` | `p` | `p` | 113 | 87 | 0.75 of 2342 | template+ptype=Standard/lesson c=0.88 n=72 | structure | — | CANDIDATE |
| 605 | activity | EXTRA | `div.col-12` | `—` | `p>b` | 123 | 83 | 0.95 of 2342 | subject=1-10 Blended Literacy c=0.96 n=20 | structure | — | CANDIDATE |
| 606 | activity | EXTRA | `div.col-12` | `—` | `ol` | 130 | 82 | 0.96 of 2342 | subject=1-10 Mathematics c=0.98 n=31 | structure | — | CANDIDATE |
| 607 | activity | EXTRA | `div.col-12` | `—` | `h3` | 109 | 82 | 0.87 of 2342 | template=Standard c=0.92 n=66 | structure | — | CANDIDATE |
| 609 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `div.activity.interactive[number=*]` | 111 | 80 | 0.46 of 2342 | subject+ptype=1-10 Blended Literacy/lesson c=0.86 n=23 | structure | yes | CANDIDATE |
| 611 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `div.activity[number=*]` | 112 | 79 | 0.46 of 2342 | subject+ptype=1-10 Mathematics/lesson c=0.68 n=22 | structure | yes | CANDIDATE |
| 615 | activity | EXTRA | `div.col-12` | `—` | `ul` | 100 | 74 | 0.94 of 2342 | template=Standard c=0.96 n=87 | structure | — | CANDIDATE |
| 616 | activity | EXTRA | `p>b` | `—` | `b` | 91 | 68 | 0.93 of 2342 | template=Standard c=0.94 n=58 | structure | — | CANDIDATE |
| 617 | activity | EXTRA | `div.col-12` | `—` | `a` | 107 | 67 | 0.87 of 2342 | series=XDLS90 c=0.95 n=21 | structure | — | CANDIDATE |
| 619 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity.interactive[number=*]` | `div.activity.interactive[number=*]` | 94 | 67 | 0.42 of 2342 | subject+ptype=1-10 Mathematics/lesson c=0.65 n=21 | structure | yes | CANDIDATE |
| 620 | activity | EXTRA | `a` | `—` | `div.button` | 103 | 66 | 0.77 of 2342 | series=XDLS90 c=0.92 n=31 | structure | yes | CANDIDATE |
| 621 | activity | EXTRA | `p>a` | `—` | `a` | 77 | 66 | 0.98 of 2342 | subject+ptype=1-10 Blended Literacy/lesson c=1.00 n=27 | structure | — | CANDIDATE |
| 623 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `p` | 77 | 62 | 0.60 of 2342 | subject+ptype=1-10 Mathematics/lesson c=0.78 n=31 | structure | — | CANDIDATE |
| 625 | activity | SUBSTITUTED | `div.col-12.col-md-8` | `div.activity[number=*]` | `h3` | 85 | 59 | 0.46 of 2342 | subject+ptype=NCEA1/lesson c=0.63 n=36 | structure | yes | CANDIDATE |
| 628 | activity | EXTRA | `div.col-12` | `—` | `h4.goJournal` | 129 | 55 | 0.95 of 2342 | series=HIS10 c=1.00 n=33 | structure | — | CANDIDATE |
| 629 | activity | EXTRA | `div.col-12.col-md-8` | `—` | `div.activity[number=*]` | 65 | 55 | 0.95 of 2342 | template=Standard c=0.98 n=51 | structure | yes | CANDIDATE |
| 630 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `div.row` | 57 | 55 | 0.60 of 2342 | ptype=lesson c=0.70 n=48 | structure | — | CANDIDATE |
| 632 | activity | SUBSTITUTED | `div.col-12` | `p` | `WIDGET` | 63 | 54 | 0.75 of 2342 | template+ptype=Standard/lesson c=0.88 n=47 | structure | — | CANDIDATE |
| 633 | activity | SUBSTITUTED | `div.col-12` | `a` | `h4.goJournal` | 117 | 53 | 0.56 of 2342 | series=HIS10 c=0.83 n=20 | structure | — | CANDIDATE |
| 635 | activity | EXTRA | `ol` | `—` | `li` | 67 | 51 | 0.96 of 2342 | template=Standard c=0.96 n=52 | structure | — | CANDIDATE |
| 637 | activity | SUBSTITUTED | `div.col-12` | `a` | `p` | 71 | 49 | 0.56 of 2342 | subject+ptype=1-10 Mathematics/lesson c=0.80 n=20 | structure | — | CANDIDATE |
| 639 | activity | EXTRA | `div.col-12` | `—` | `p>i` | 53 | 47 | 0.98 of 2342 | template=Standard c=0.98 n=45 | structure | — | CANDIDATE |
| 651 | activity | EXTRA | `p>i` | `—` | `i` | 48 | 40 | 0.89 of 2342 | template=Standard c=0.90 n=44 | structure | — | CANDIDATE |
| 655 | activity | EXTRA | `div.col-12.col-md-8` | `—` | `div.activity.interactive[number=*]` | 41 | 39 | 0.89 of 2342 | template=Standard c=0.92 n=28 | structure | yes | CANDIDATE |
| 656 | activity | EXTRA | `a` | `—` | `div.externalButton` | 49 | 38 | 0.91 of 2342 | template=Standard c=0.91 n=35 | structure | — | CANDIDATE |
| 663 | activity | SUBSTITUTED | `div.row` | `div.col-12` | `div.col-12.col-md-8` | 37 | 33 | 0.79 of 2342 | ptype=lesson c=0.92 n=30 | structure | — | CANDIDATE |
| 666 | activity | EXTRA | `div.col-12` | `—` | `div.icon.ratio.ratio-16x9.videoSection` | 47 | 32 | 0.98 of 2342 | template=Standard c=0.98 n=39 | structure | yes | CANDIDATE |
| 671 | activity | SUBSTITUTED | `div.col-12` | `a` | `WIDGET` | 36 | 31 | 0.56 of 2342 | template+ptype=Standard/lesson c=0.66 n=33 | structure | — | CANDIDATE |
| 674 | activity | EXTRA | `p` | `—` | `b` | 38 | 30 | 0.96 of 2342 | template=Standard c=0.97 n=35 | structure | — | CANDIDATE |
| 678 | activity | SUBSTITUTED | `div.row` | `div.col-12` | `WIDGET` | 31 | 30 | 0.79 of 2342 | ptype=lesson c=0.92 n=25 | structure | — | CANDIDATE |
| 679 | activity | EXTRA | `div.col-12` | `—` | `audio.audioPlayer.icon` | 44 | 29 | 1.00 of 2342 | subject=1-10 Blended Literacy c=1.00 n=21 | structure | yes | CANDIDATE |
| 682 | activity | EXTRA | `div.col-12` | `—` | `div.activity.interactive[number=*]` | 32 | 29 | 0.89 of 2342 | era=Refresh c=0.89 n=32 | structure | yes | CANDIDATE |
| 683 | activity | EXTRA | `ul` | `—` | `li` | 30 | 29 | 0.93 of 2342 | template=Standard c=0.95 n=25 | structure | — | CANDIDATE |
| 685 | activity | SUBSTITUTED | `div.col-12` | `h3` | `WIDGET` | 35 | 28 | 0.76 of 2342 | template+ptype=Standard/lesson c=0.89 n=28 | structure | — | CANDIDATE |
| 687 | activity | SUBSTITUTED | `div.row` | `div.col-12` | `div.row` | 29 | 28 | 0.79 of 2342 | ptype=lesson c=0.92 n=23 | structure | — | CANDIDATE |
| 688 | activity | EXTRA | `div.col-12` | `—` | `div.ratio.ratio-16x9.videoSection` | 49 | 27 | 0.99 of 2342 | template=Standard c=0.99 n=40 | structure | yes | CANDIDATE |
| 698 | activity | SUBSTITUTED | `div.activity.interactive[number=*]` | `div.row` | `WIDGET` | 28 | 25 | 0.55 of 2342 | ptype=lesson c=0.63 n=25 | structure | yes | CANDIDATE |
| 699 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `div.col-12.col-md-8` | 26 | 25 | 0.60 of 2342 | ptype=lesson c=0.70 n=21 | structure | — | CANDIDATE |
| 700 | activity | EXTRA | `div.col-12` | `—` | `h5` | 28 | 24 | 0.99 of 2342 | template=Standard c=0.99 n=23 | structure | — | CANDIDATE |
| 701 | activity | EXTRA | `div.icon.ratio.ratio-16x9.videoSection` | `—` | `iframe` | 27 | 24 | 0.99 of 2342 | template=Standard c=1.00 n=20 | structure | yes | CANDIDATE |
| 704 | activity | SUBSTITUTED | `div.col-12` | `WIDGET` | `ol` | 25 | 23 | 0.60 of 2342 | ptype=lesson c=0.70 n=22 | structure | — | CANDIDATE |
| 706 | activity | SUBSTITUTED | `div.col-12` | `h3` | `h3` | 30 | 22 | 0.76 of 2342 | template+ptype=Standard/lesson c=0.89 n=20 | structure | — | CANDIDATE |
| 714 | activity | SUBSTITUTED | `div.col-12` | `p` | `p>b` | 26 | 20 | 0.75 of 2342 | ptype=lesson c=0.88 n=22 | structure | — | CANDIDATE |
| 718 | activity | EXTRA | `div.col-12` | `—` | `div.button` | 30 | 19 | 1.00 of 2342 | template=Standard c=1.00 n=26 | structure | yes | CANDIDATE |
| 719 | activity | EXTRA | `div.ratio.ratio-16x9.videoSection` | `—` | `iframe` | 27 | 19 | 0.99 of 2342 | ptype=lesson c=0.99 n=25 | structure | yes | CANDIDATE |
| 725 | activity | SUBSTITUTED | `div.row` | `div.col-12` | `div.col-12` | 21 | 19 | 0.79 of 2342 | ptype=lesson c=0.92 n=20 | structure | — | CANDIDATE |
| 768 | activity | SUBSTITUTED | `div.col-12` | `p` | `h4.goJournal` | 22 | 13 | 0.75 of 2342 | template+ptype=Standard/lesson c=0.88 n=21 | structure | — | CANDIDATE |
| 3696 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p` | 1057 | 380 | 0.82 of 2342 | subject=1-10 Blended Literacy c=1.00 n=36 | structure | — | CANDIDATE |
| 3697 | body | EXTRA | `div#body` | `—` | `div.row` | 1406 | 374 | 0.73 of 2342 | subject+ptype=1-10 Blended Literacy/overview c=1.00 n=29 | structure | — | CANDIDATE |
| 3698 | body | MISSING | `div#body` | `div.row` | `—` | 1295 | 323 | 0.34 of 2342 | series=CEDO50 c=0.76 n=20 | 0.86 | — | CANDIDATE |
| 3699 | body | MISSING | `div.col-12.col-md-8` | `p` | `—` | 596 | 278 | 0.25 of 2342 | template+ptype=Fundamentals/overview c=0.88 n=34 | 0.82 | — | CANDIDATE |
| 3700 | body | EXTRA | `div.col-12.col-md-8` | `—` | `img.img-fluid` | 526 | 230 | 0.96 of 2342 | template+ptype=Standard/overview c=1.00 n=25 | structure | — | CANDIDATE |
| 3701 | body | MOVED | `div.col-12.col-md-8` | `p` | `p` | 336 | 220 | 0.16 of 2342 | template+ptype=Fundamentals/overview c=0.82 n=36 | structure | — | CANDIDATE |
| 3702 | body | EXTRA | `div.col-12.col-md-8` | `—` | `WIDGET` | 345 | 210 | 0.89 of 2342 | subject=NCEA1 c=0.96 n=23 | structure | — | CANDIDATE |
| 3703 | body | EXTRA | `div.row` | `—` | `div.col-12.col-md-8` | 288 | 199 | 0.85 of 2342 | subject+ptype=1-10 Blended Literacy/lesson c=0.99 n=21 | structure | — | CANDIDATE |
| 3704 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p>b` | 315 | 188 | 0.97 of 2342 | subject=1-10 Blended Literacy c=1.00 n=37 | structure | — | CANDIDATE |
| 3705 | body | SUBSTITUTED | `div.row` | `div.col-12` | `div.col-12.col-md-8` | 317 | 182 | 0.55 of 2342 | subject+ptype=1-10 Blended Literacy/overview c=0.99 n=64 | structure | — | CANDIDATE |
| 3706 | body | EXTRA | `div.col-12.col-md-8` | `—` | `ul` | 303 | 169 | 0.95 of 2342 | subject=1-10 English c=0.99 n=26 | structure | — | CANDIDATE |
| 3707 | body | EXTRA | `div.col-12.col-md-8` | `—` | `h3` | 272 | 168 | 0.82 of 2342 | subject=1-10 Blended Literacy c=1.00 n=20 | structure | — | CANDIDATE |
| 3708 | body | MISSING | `div.row` | `div.col-12.col-md-8` | `—` | 302 | 167 | 0.29 of 2342 | template=Fundamentals c=0.78 n=29 | 0.94 | — | CANDIDATE |
| 3713 | body | EXTRA | `div.col-12.col-md-8` | `—` | `a` | 212 | 134 | 0.98 of 2342 | subject=ConnectED c=1.00 n=28 | structure | — | CANDIDATE |
| 3716 | body | EXTRA | `p>b` | `—` | `b` | 179 | 112 | 0.94 of 2342 | subject=1-10 Mathematics c=0.97 n=32 | structure | — | CANDIDATE |
| 3718 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.ratio.ratio-16x9.videoSection` | 169 | 108 | 0.94 of 2342 | ptype=overview c=0.95 n=28 | structure | yes | CANDIDATE |
| 3719 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p>a` | 160 | 106 | 0.99 of 2342 | subject=None c=0.99 n=44 | structure | — | CANDIDATE |
| 3720 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.table-responsive` | 154 | 104 | 0.92 of 2342 | template=Standard c=0.92 n=138 | structure | — | CANDIDATE |
| 3724 | body | EXTRA | `a` | `—` | `div.button` | 167 | 99 | 0.96 of 2342 | subject+ptype=NCEA1/lesson c=0.98 n=20 | structure | — | CANDIDATE |
| 3728 | body | EXTRA | `div.table-responsive` | `—` | `table.table.table-bordered` | 140 | 93 | 0.96 of 2342 | template=Standard c=0.96 n=113 | structure | yes | CANDIDATE |
| 3729 | body | EXTRA | `p` | `—` | `b` | 119 | 92 | 0.93 of 2342 | subject=NCEA1 c=0.96 n=20 | structure | — | CANDIDATE |
| 3734 | body | EXTRA | `p>i` | `—` | `i` | 106 | 78 | 0.97 of 2342 | subject=1-10 Blended Literacy c=1.00 n=26 | structure | — | CANDIDATE |
| 3735 | body | SUBSTITUTED | `div.icon.ratio.ratio-16x9.videoSection` | `iframe.embed-responsive-item` | `iframe` | 208 | 77 | 0.20 of 2342 | series=PES10 c=0.68 n=35 | structure | yes | CANDIDATE |
| 3737 | body | EXTRA | `div.col-12.col-md-8` | `—` | `ol` | 103 | 77 | 0.99 of 2342 | template=Standard c=0.99 n=85 | structure | — | CANDIDATE |
| 3738 | body | MOVED | `div.col-12.col-md-8` | `h3` | `h3` | 88 | 75 | 0.11 of 2342 | template+ptype=Fundamentals/overview c=0.68 n=20 | structure | — | CANDIDATE |
| 3740 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p>i` | 100 | 72 | 0.98 of 2342 | subject=NCEA1 c=0.99 n=23 | structure | — | CANDIDATE |
| 3742 | body | EXTRA | `p>a` | `—` | `a` | 97 | 71 | 0.99 of 2342 | template=Standard c=1.00 n=76 | structure | — | CANDIDATE |
| 3743 | body | EXTRA | `div.row` | `—` | `div.col-12` | 123 | 70 | 0.71 of 2342 | subject=None c=0.77 n=22 | structure | — | CANDIDATE |
| 3745 | body | SUBSTITUTED | `div#body` | `div.row` | `WIDGET` | 110 | 69 | 0.94 of 2342 | subject=Online Safety (OS9000) c=1.00 n=25 | structure | — | CANDIDATE |
| 3746 | body | EXTRA | `table.table.table-bordered` | `—` | `tr` | 95 | 69 | 0.98 of 2342 | template=Standard c=0.98 n=79 | structure | yes | CANDIDATE |
| 3748 | body | EXTRA | `div.col-12.col-md-8` | `—` | `h4` | 80 | 69 | 0.94 of 2342 | subject+ptype=None/lesson c=0.97 n=26 | structure | — | CANDIDATE |
| 3752 | body | EXTRA | `div.col-12.col-md-8` | `—` | `audio.audioPlayer.icon` | 121 | 67 | 1.00 of 2342 | subject=Leaving to Learn c=1.00 n=34 | structure | yes | CANDIDATE |
| 3756 | body | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `div.col-12.col-md-8` | 74 | 65 | 0.98 of 2342 | ptype=lesson c=0.99 n=45 | structure | — | CANDIDATE |
| 3761 | body | EXTRA | `a` | `—` | `div.externalButton` | 86 | 60 | 0.92 of 2342 | template=Standard c=0.92 n=74 | structure | — | CANDIDATE |
| 3763 | body | EXTRA | `ul` | `—` | `li` | 70 | 59 | 0.93 of 2342 | template=Standard c=0.94 n=53 | structure | — | CANDIDATE |
| 3765 | body | EXTRA | `div.ratio.ratio-16x9.videoSection` | `—` | `iframe` | 75 | 58 | 0.77 of 2342 | template+ptype=Standard/lesson c=0.80 n=45 | structure | yes | CANDIDATE |
| 3767 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `p` | 71 | 57 | 0.85 of 2342 | template+ptype=Standard/lesson c=0.86 n=46 | structure | — | CANDIDATE |
| 3772 | body | EXTRA | `div.col-12` | `—` | `p` | 85 | 50 | 0.93 of 2342 | template=Standard c=0.94 n=73 | structure | — | CANDIDATE |
| 3773 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `div.activity[number=*]` | 56 | 50 | 0.85 of 2342 | template+ptype=Standard/lesson c=0.86 n=48 | structure | yes | CANDIDATE |
| 3774 | body | EXTRA | `tr` | `—` | `td` | 58 | 49 | 0.94 of 2342 | template=Standard c=0.95 n=53 | structure | — | CANDIDATE |
| 3776 | body | SUBSTITUTED | `div.col-12.col-md-8` | `h3` | `h4` | 76 | 47 | 0.50 of 2342 | subject+ptype=None/lesson c=0.67 n=32 | structure | — | CANDIDATE |
| 3777 | body | EXTRA | `div.alert` | `—` | `div.row` | 60 | 47 | 0.91 of 2342 | template=Standard c=0.92 n=44 | structure | — | CANDIDATE |
| 3779 | body | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `WIDGET` | 49 | 47 | 0.98 of 2342 | ptype=lesson c=0.99 n=42 | structure | — | CANDIDATE |
| 3782 | body | MISSING | `div#body` | `div.fundamentalsPanel` | `—` | 53 | 45 | 0.02 of 2342 | template+ptype=Fundamentals/overview c=0.80 n=37 | 0.98 | yes | CANDIDATE |
| 3783 | body | EXTRA | `div.fundamentalsPanel` | `—` | `div.row` | 45 | 45 | 0.99 of 2342 | era=Refresh c=0.99 n=45 | structure | — | CANDIDATE |
| 3784 | body | EXTRA | `div.row` | `—` | `div.col-12.col-md-6` | 63 | 44 | 0.99 of 2342 | subject=Online Safety (OS9000) c=1.00 n=20 | structure | — | CANDIDATE |
| 3785 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.alert` | 59 | 44 | 0.91 of 2342 | template=Standard c=0.92 n=46 | structure | — | CANDIDATE |
| 3788 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.icon.ratio.ratio-16x9.videoSection` | 60 | 43 | 0.92 of 2342 | template=Standard c=0.93 n=52 | structure | yes | CANDIDATE |
| 3792 | body | EXTRA | `div#body` | `—` | `WIDGET` | 78 | 41 | 0.93 of 2342 | era=Refresh c=0.93 n=78 | structure | — | CANDIDATE |
| 3795 | body | EXTRA | `tr` | `—` | `th` | 44 | 41 | 0.99 of 2342 | template=Standard c=1.00 n=34 | structure | — | CANDIDATE |
| 3800 | body | EXTRA | `p` | `—` | `i` | 44 | 38 | 0.96 of 2342 | template=Standard c=0.97 n=40 | structure | — | CANDIDATE |
| 3804 | body | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `div.row` | 38 | 37 | 0.98 of 2342 | ptype=lesson c=0.99 n=24 | structure | — | CANDIDATE |
| 3809 | body | EXTRA | `div#body` | `—` | `div.row.supervisor` | 43 | 33 | 0.90 of 2342 | ptype=lesson c=0.91 n=38 | structure | yes | CANDIDATE |
| 3811 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `WIDGET` | 34 | 33 | 0.85 of 2342 | template+ptype=Standard/lesson c=0.86 n=23 | structure | — | CANDIDATE |
| 3814 | body | EXTRA | `div.col-12.col-md-8` | `—` | `p>span.infoTrigger` | 36 | 32 | 0.86 of 2342 | template=Standard c=0.87 n=30 | structure | — | CANDIDATE |
| 3816 | body | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `p` | 33 | 32 | 0.98 of 2342 | ptype=lesson c=0.99 n=27 | structure | — | CANDIDATE |
| 3819 | body | EXTRA | `div.row` | `—` | `div.col-12.col-md-4.offset-md-0` | 31 | 31 | 0.80 of 2342 | template=Standard c=0.80 n=21 | structure | — | CANDIDATE |
| 3823 | body | EXTRA | `div.alert.solid` | `—` | `div.row` | 41 | 29 | 0.99 of 2342 | template=Standard c=0.99 n=36 | structure | yes | CANDIDATE |
| 3824 | body | EXTRA | `div.col-12.col-md-8` | `—` | `h5` | 39 | 29 | 0.98 of 2342 | era=Refresh c=0.98 n=39 | structure | — | CANDIDATE |
| 3825 | body | EXTRA | `div.icon.ratio.ratio-16x9.videoSection` | `—` | `iframe` | 36 | 29 | 0.97 of 2342 | ptype=lesson c=0.98 n=30 | structure | yes | CANDIDATE |
| 3827 | body | EXTRA | `body.container-fluid` | `—` | `div#body` | 29 | 29 | 0.21 of 2342 | series=WJFUN c=1.00 n=20 | structure | — | CANDIDATE |
| 3828 | body | EXTRA | `div.col-12.col-md-8` | `—` | `h4.goJournal` | 37 | 28 | 1.00 of 2342 | era=Refresh c=1.00 n=37 | structure | — | CANDIDATE |
| 3832 | body | EXTRA | `div.inquiryPanel` | `—` | `div.row` | 30 | 28 | 0.99 of 2342 | era=Refresh c=0.99 n=30 | structure | — | CANDIDATE |
| 3833 | body | EXTRA | `div#body` | `—` | `div.fundamentalsPanel` | 28 | 28 | 0.98 of 2342 | era=Refresh c=0.98 n=28 | structure | yes | CANDIDATE |
| 3836 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.flipCardsContainer.row` | 30 | 27 | 0.94 of 2342 | template=Standard c=0.95 n=24 | structure | — | CANDIDATE |
| 3845 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `img.img-fluid` | 26 | 25 | 0.85 of 2342 | era=Refresh c=0.85 n=26 | structure | — | CANDIDATE |
| 3850 | body | EXTRA | `div.row` | `—` | `div.col-12.col-md-4` | 31 | 24 | 0.95 of 2342 | template=Standard c=0.95 n=26 | structure | — | CANDIDATE |
| 3852 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.clickDropContent` | 28 | 24 | 0.95 of 2342 | template=Standard c=0.95 n=23 | structure | — | CANDIDATE |
| 3861 | body | EXTRA | `div.col-12.col-md-8` | `—` | `div.alert.solid` | 27 | 22 | 0.99 of 2342 | era=Refresh c=0.99 n=27 | structure | yes | CANDIDATE |
| 3864 | body | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `div.col-12.col-md-6` | 25 | 22 | 0.98 of 2342 | ptype=lesson c=0.99 n=21 | structure | — | CANDIDATE |
| 3865 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `div.activity.interactive[number=*]` | 24 | 22 | 0.85 of 2342 | template+ptype=Standard/lesson c=0.86 n=22 | structure | yes | CANDIDATE |
| 3867 | body | EXTRA | `p>span.infoTrigger` | `—` | `span.infoTrigger` | 22 | 22 | 0.84 of 2342 | era=Refresh c=0.84 n=22 | structure | — | CANDIDATE |
| 3869 | body | EXTRA | `div#body` | `—` | `div.inquiryPanel` | 29 | 21 | 0.98 of 2342 | era=Refresh c=0.98 n=29 | structure | — | CANDIDATE |
| 3875 | body | SUBSTITUTED | `div.row` | `div.col-12.col-md-8` | `div.col-12` | 23 | 21 | 0.98 of 2342 | era=Refresh c=0.98 n=23 | structure | — | CANDIDATE |
| 3885 | body | SUBSTITUTED | `div.col-12.col-md-8` | `p` | `div.alert` | 26 | 19 | 0.85 of 2342 | era=Refresh c=0.85 n=26 | structure | — | CANDIDATE |
| 3889 | body | EXTRA | `div.flipCardsContainer.row` | `—` | `div.col-12.col-md-4.paddingLR` | 20 | 19 | 0.97 of 2342 | era=Refresh c=0.97 n=20 | structure | — | CANDIDATE |
| 3907 | body | SUBSTITUTED | `div#body` | `div.row` | `div.table-responsive` | 22 | 16 | 0.94 of 2342 | template=Standard c=0.98 n=20 | structure | — | CANDIDATE |
| 3922 | body | MISSING | `div#body` | `div.clickDropContent.noBorder.row` | `—` | 50 | 15 | 0.02 of 2342 | series=XDLS90 c=0.64 n=38 | 0.93 | yes | CANDIDATE |
| 3934 | body | EXTRA | `div.col-12.col-md-6` | `—` | `p` | 23 | 14 | 1.00 of 2342 | ptype=lesson c=1.00 n=21 | structure | — | CANDIDATE |
| 4386 | body | SUBSTITUTED | `div.col-12.col-md-8` | `div.alert` | `div.activity.clickDropContent.dropbox[number=*]` | 20 | 4 | 0.31 of 2342 | series=XDLS90 c=0.80 n=20 | structure | yes | CANDIDATE |
| 8859 | root | EXTRA | `body.container-fluid` | `—` | `div.row` | 263 | 263 | 0.88 of 2349 | subject+ptype=NCEA1/overview c=0.98 n=41 | structure | — | CANDIDATE |
| 8861 | root | SUBSTITUTED | `#root` | `body.container-fluid.fundamentals` | `body.container-fluid` | 42 | 26 | 0.04 of 2349 | series=WJFUN c=1.00 n=21 | structure | yes | CANDIDATE |
| 8862 | root | MISSING | `body.container-fluid.fundamentals` | `div.row` | `—` | 21 | 21 | 0.02 of 2349 | series=WJFUN c=1.00 n=20 | structure | yes | CANDIDATE |
| 8864 | root | SUBSTITUTED | `#root` | `body` | `body.container-fluid` | 138 | 15 | 0.06 of 2349 | series=PWY10 c=1.00 n=44 | structure | yes | CANDIDATE |

## Details — in the companion file `CONVERTER_V2/outputs/_diff_queue_details.md`
Every CANDIDATE and every top-40 row has three quoted examples (WT / gold / Claude) there, plus the
below-floor list. **NEVER read the companion whole** (hundreds of KB): `grep -n '^### #<rank> ' CONVERTER_V2/outputs/_diff_queue_details.md` then `sed -n '<start>,<start+40>p'`. The top 25
candidates' detail blocks are repeated below for convenience.

### #4 · title · MISSING · `div#header` › gold `h1>span` vs Claude `—` — CANDIDATE
- pages 257 / modules 138 / lines 260; consensus (all) 0.23 of 2349 gold pages with the region; derivable 0.74 (68 lines with no WT source)
- by template: Standard 85m/187p c=0.18; Fundamentals 37m/37p c=0.48; Inquiry 11m/14p c=0.35; Bilingual 5m/19p c=1.00
- by subject: None 35m/82p c=0.29; 1-10 English 19m/19p c=0.15; Leaving to Learn 14m/22p c=0.26; NCEA1 13m/19p c=0.14; Online Safety (OS9000) 13m/29p c=0.33; 1-10 Mathematics 11m/11p c=0.14
- by era: Refresh 138m/257p c=0.23
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
- modules: ANZH101, ANZH103, ANZH104, ANZH301, ANZH401, ANZH404, ARFUN01, ARFUN02, ARFUN03, ARFUN04, ARFUN05, ART1004, ART1006, CEDK102, CEDK501, CEDO202, CEDR204, CEDT301, CHI1003, CHI1005, CHWHA, DTC1005, ENFUN01, ENFUN02 …

### #5 · title · EXTRA · `div#header` › gold `—` vs Claude `h1>span` — CANDIDATE
- pages 15 / modules 14 / lines 15; consensus (all) 0.77 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 11m/12p c=0.82; Fundamentals 2m/2p c=0.52; Inquiry 1m/1p c=0.65
- by subject: None 4m/5p c=0.71; NCEA1 3m/3p c=0.86; Leaving to Learn 3m/3p c=0.74; 1-10 Blended Literacy 1m/1p c=1.00; ConnectED 1m/1p c=0.78; 1-10 English 1m/1p c=0.84
- by era: Refresh 14m/15p c=0.77
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
- modules: AGH1005, ANZH302, BLL246, CEDO105, ENGFUN02, ENGI103, FRFUN06, HIS1002, PWY1002, PWYWHA1, SSFUN07, XDLS904, XDLS906, XFUN02

### #29 · module-menu · SUBSTITUTED · `div.col-12.col-md-6.paddingR` › gold `p` vs Claude `h5` — CANDIDATE
- pages 83 / modules 83 / lines 150; consensus (all) 0.06 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 61m/61p c=0.05; Fundamentals 14m/14p c=0.12; Inquiry 8m/8p c=0.35
- by subject: 1-10 Blended Literacy 69m/69p c=0.30; 1-10 Health and PE 14m/14p c=0.93
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

### #30 · module-menu · MISSING · `ul` › gold `li` vs Claude `—` — CANDIDATE
- pages 114 / modules 76 / lines 327; consensus (all) 0.10 of 2349 gold pages with the region; derivable 0.89 (37 lines with no WT source)
- by template: Standard 57m/95p c=0.10; Inquiry 11m/11p c=0.26; Fundamentals 8m/8p c=0.01
- by subject: 1-10 English 22m/39p c=0.12; 1-10 Blended Literacy 21m/21p c=0.24; 1-10 Mathematics 8m/23p c=0.09; NCEA1 7m/7p c=0.02; Te ara Whakapuawa -Wellbeing 5m/5p c=0.88; None 3m/6p c=0.07
- by era: Refresh 76m/114p c=0.10
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
- modules: AGH1003, AGH1007, AGH1008, ANZH101, ANZH103, BLL110, BLL125, BLL126, BLL127, BLL130, BLL134, BLL136, BLL137, BLL140, BLL141, BLL143, BLL146, BLL147, BLL150, BLL151, BLL153, BLL154, BLL173, BLL210 …

### #31 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `div.col-12.col-md-6.paddingR` — CANDIDATE
- pages 69 / modules 52 / lines 110; consensus (all) 0.97 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 44m/61p c=0.97; Inquiry 5m/5p c=0.90; Fundamentals 3m/3p c=1.00
- by subject: 1-10 Blended Literacy 19m/19p c=0.70; 1-10 Mathematics 7m/18p c=1.00; ANZH 6m/9p c=1.00; None 6m/6p c=1.00; 1-10 English 4m/4p c=1.00; Leaving to Learn 4m/4p c=1.00
- by era: Refresh 52m/69p c=0.97
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

### #36 · module-menu · EXTRA · `ul` › gold `—` vs Claude `li` — CANDIDATE
- pages 81 / modules 43 / lines 166; consensus (all) 0.79 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 30m/68p c=0.79; Inquiry 10m/10p c=0.46; Fundamentals 3m/3p c=0.77
- by subject: 1-10 Blended Literacy 10m/10p c=0.64; 1-10 English 8m/11p c=0.73; ConnectED 6m/6p c=0.56; NCEA1 5m/12p c=0.96; None 5m/22p c=0.81; Te ara Whakapuawa -Wellbeing 4m/4p c=0.12
- by era: Refresh 43m/81p c=0.79
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

### #37 · module-menu · SUBSTITUTED · `div.col-12.col-md-6.paddingL` › gold `p` vs Claude `h5` — CANDIDATE
- pages 38 / modules 38 / lines 57; consensus (all) 0.03 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Fundamentals 14m/14p c=0.12; Standard 13m/13p c=0.02; Inquiry 11m/11p c=0.20
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

### #39 · module-menu · MISSING · `div.col-12.col-md-6.paddingR` › gold `p` vs Claude `—` — CANDIDATE
- pages 50 / modules 37 / lines 65; consensus (all) 0.04 of 2349 gold pages with the region; derivable 0.71 (19 lines with no WT source)
- by template: Standard 28m/41p c=0.04; Inquiry 9m/9p c=0.18
- by subject: 1-10 Blended Literacy 23m/23p c=0.28; EXPlore 5m/8p c=0.00; ConnectED 3m/3p c=0.09; ANZH 2m/2p c=0.00; None 2m/4p c=0.00; 1-10 Mathematics 2m/10p c=0.04
- by era: Refresh 37m/50p c=0.04
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

### #40 · module-menu · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `h5` — CANDIDATE
- pages 86 / modules 36 / lines 131; consensus (all) 0.76 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 27m/76p c=0.73; Fundamentals 8m/8p c=0.99; Inquiry 1m/2p c=0.81
- by subject: None 13m/32p c=0.62; 1-10 English 7m/14p c=0.50; Leaving to Learn 7m/15p c=0.86; Online Safety (OS9000) 3m/6p c=0.41; NCEA1 1m/3p c=0.82; ANZH 1m/2p c=1.00
- by era: Refresh 36m/86p c=0.76
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
- modules: AGH1009, ANZH301, CEDO501, ENFUN07, ENGC201, ENGC202, ENGI102, ENGI301, ENGS302, ENGS404, ENGS405, ENO2060, JPN1004, MXEO102, MXS1004, OSAI301, OSBY301, OSSM401, SCBI301, SCCH301, SCPH301, SSCI205, WJFUN116, WJFUN205 …

### #42 · module-menu · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `p` — CANDIDATE
- pages 67 / modules 29 / lines 92; consensus (all) 0.87 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 27m/64p c=0.86; Fundamentals 1m/1p c=1.00; Inquiry 1m/2p c=0.84
- by subject: Leaving to Learn 9m/20p c=0.64; NCEA1 5m/14p c=0.92; None 5m/12p c=0.88; Online Safety (OS9000) 5m/12p c=0.81; 1-10 English 2m/2p c=0.82; 1-10 Mathematics 2m/5p c=0.93
- by era: Refresh 29m/67p c=0.87
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
- modules: AGH1003, ANZH301, ENGC201, ENGS404, ENGS405, GEO1005, HIS1005, HIS1006, JPN1004, MXDI201, MXEO202, MXS1004, OSAI101, OSBY301, OSGM201, OSOH101, OSSM401, PES1002, PES1005, WJFUN116, XDLS903, XDLS904, XDLS905, XDLS906 …

### #43 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `div.col-12.col-md-8` — CANDIDATE
- pages 110 / modules 28 / lines 110; consensus (all) 0.66 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 15m/97p c=0.62; Fundamentals 13m/13p c=0.99
- by subject: None 13m/13p c=0.53; 1-10 Mathematics 12m/81p c=0.77; 1-10 English 2m/11p c=0.42; ConnectED 1m/5p c=0.53
- by era: Refresh 28m/110p c=0.66
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
- modules: CEDO105, ENGI102, ENGI103, FRFUN06, MXDB301, MXDB302, MXDI301, MXEX101, MXEX301, MXEX302, MXFL204, MXFU201, MXFU202, MXFU301, MXFU302, MXFU402, WJFUN105, WJFUN106, WJFUN108, WJFUN109, WJFUN110, WJFUN112, WJFUN113, WJFUN115 …

### #44 · module-menu · EXTRA · `div.col-12.col-md-8` › gold `—` vs Claude `ul` — CANDIDATE
- pages 53 / modules 27 / lines 96; consensus (all) 0.71 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 20m/46p c=0.68; Fundamentals 7m/7p c=0.99
- by subject: None 11m/15p c=0.65; 1-10 English 5m/16p c=0.42; Leaving to Learn 4m/8p c=0.53; Online Safety (OS9000) 2m/5p c=0.28; NCEA1 1m/1p c=0.80; ANZH 1m/2p c=1.00
- by era: Refresh 27m/53p c=0.71
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
- modules: AGH1009, ANZH301, CEDO501, ENFUN07, ENGC201, ENGC202, ENGI102, ENGS404, ENGS405, ENO2060, GEO1005, JPN1004, MXEO102, MXS1004, OSBY301, OSSM401, SSCI205, WJFUN107, WJFUN116, WJFUN205, WJFUN206, WJFUN208, WJFUN211, XLP01 …

### #45 · module-menu · MISSING · `div#header` › gold `div#module-head-buttons` vs Claude `—` — CANDIDATE
- pages 65 / modules 22 / lines 65; consensus (all) 0.77 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 15m/50p c=0.78; Bilingual 5m/12p c=0.38; Inquiry 2m/3p c=0.83
- by subject: None 6m/22p c=0.81; Te Marautanga o Aotearoa TMoA 4m/10p c=0.38; 1-10 Blended Literacy 3m/6p c=0.40; ConnectED 2m/3p c=0.76; Online Safety (OS9000) 2m/9p c=1.00; Leaving to Learn 2m/11p c=0.88
- by era: Refresh 22m/65p c=0.77
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:94 — **Header:** `#module-code` → `<h1>` (module code or lesson number), then `<h1><span>Title</span></h1>`, then `#module-head-buttons` → `#module-menu-bu
  - KB: 13_SPLIT_MODE.md:70 — <div id="header"> … module-code, title h1(s), menu button, full #module-menu-content … </div>
  - KB: INDEX.md:115 — - Sections: 10 — Corpus-Validated Scaffolding Reference · 1. Header title casing · 2. Menu archetype — safe fallbacks (only when no reference/series p
- **ANZH103** ANZH103_1_0.html ↔ ANZH103_3_0.html (structure, derivable=True)
  - gold: `div#module-head-buttons`
  - Claude: `—`
- **BLL114** BLL114_1_0.html ↔ BLL114-02.html (structure, derivable=True)
  - gold: `div#module-head-buttons`
  - Claude: `—`
- **BLL116** BLL116_1_0.html ↔ BLL116-02.html (structure, derivable=True)
  - gold: `div#module-head-buttons`
  - Claude: `—`
- modules: ANZH103, BLL114, BLL116, BLL153, BLLR201, BLLR202, BLLR203, CEDT207, CEDT301, EXPFUN07, HES1002, HES1006, MXFL401, OSSC401, OSSC501, PNR101, PNR102, PNR104, PNR107, TRR109, XGF9002, XLP06

### #47 · module-menu · EXTRA · `div.col-12.col-md-6.paddingR` › gold `—` vs Claude `p>b` — CANDIDATE
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

### #49 · module-menu · SUBSTITUTED · `ul` › gold `li` vs Claude `li` — CANDIDATE
- pages 84 / modules 20 / lines 294; consensus (all) 0.58 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 20m/84p c=0.60
- by subject: 1-10 Mathematics 9m/28p c=0.54; None 5m/27p c=0.56; 1-10 English 3m/20p c=0.88; NCEA1 1m/1p c=0.49; 1-10 Science 1m/7p c=0.80; Leaving to Learn 1m/1p c=0.72
- by era: Refresh 20m/84p c=0.58
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

### #56 · module-menu · EXTRA · `div.col-12.col-md-6.offset-md-0` › gold `—` vs Claude `p` — CANDIDATE
- pages 24 / modules 18 / lines 59; consensus (all) 0.99 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 18m/24p c=0.98
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

### #58 · module-menu · EXTRA · `div.col-12.col-md-6.paddingR` › gold `—` vs Claude `p` — CANDIDATE
- pages 17 / modules 17 / lines 40; consensus (all) 0.95 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 14m/14p c=0.95; Inquiry 3m/3p c=0.74
- by subject: 1-10 Blended Literacy 8m/8p c=0.70; ConnectED 3m/3p c=0.89; 1-10 English 3m/3p c=0.99; ANZH 1m/1p c=0.96; 1-10 Mathematics 1m/1p c=0.95; Leaving to Learn 1m/1p c=1.00
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

### #59 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `div.col-12.col-md-6.offset-md-0` — CANDIDATE
- pages 32 / modules 16 / lines 32; consensus (all) 0.95 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 14m/30p c=0.95; Fundamentals 2m/2p c=0.95
- by subject: 1-10 English 11m/27p c=0.89; None 2m/2p c=0.97; 1-10 Mathematics 2m/2p c=0.94; 1-10 Social Science 1m/1p c=0.68
- by era: Refresh 16m/32p c=0.95
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
- modules: ENGC101, ENGC102, ENGC201, ENGC204, ENGC206, ENGI103, ENGI201, ENGI202, ENGI203, ENGI400, ENGJ102, ENGS202, ENGS301, MXFUN02, MXFUN03, SSOG101

### #60 · module-menu · EXTRA · `div.row` › gold `—` vs Claude `div.col-12.col-md-12.paddingR` — CANDIDATE
- pages 18 / modules 16 / lines 18; consensus (all) 0.96 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 16m/18p c=0.96
- by subject: 1-10 Blended Literacy 13m/13p c=0.76; EXPlore 2m/4p c=1.00; None 1m/1p c=1.00
- by era: Refresh 16m/18p c=0.96
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
- modules: BLL112, BLL113, BLL125, BLL141, BLL142, BLL143, BLL144, BLL162, BLL163, BLL166, BLL236, BLL237, BLL251, BLLR201, EXBP901, EXIP901

### #63 · module-menu · SUBSTITUTED · `div.col-12.col-md-6.paddingR` › gold `ul` vs Claude `p>b` — CANDIDATE
- pages 14 / modules 14 / lines 14; consensus (all) 0.06 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 12m/12p c=0.05; Inquiry 2m/2p c=0.33
- by subject: 1-10 Blended Literacy 14m/14p c=0.30
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

### #69 · module-menu · EXTRA · `div.col-12.col-md-12.paddingR` › gold `—` vs Claude `h4>span` — CANDIDATE
- pages 12 / modules 12 / lines 12; consensus (all) 0.97 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 10m/10p c=0.98; Fundamentals 2m/2p c=1.00
- by subject: 1-10 Blended Literacy 7m/7p c=0.78; None 3m/3p c=1.00; 1-10 Arts 2m/2p c=1.00
- by era: Refresh 12m/12p c=0.97
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:158 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **ARFUN02** ARFUN02_0_0.html ↔ ARFUN02.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h4  «Learning Intentions»`
- **ARFUN03** ARFUN03_0_0.html ↔ ARFUN03.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h4  «Learning Intentions»`
- **BLL152** BLL152_0_0.html ↔ BLL152-0.0.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h4  «Overview»`
- modules: ARFUN02, ARFUN03, BLL152, BLL241, BLL244, BLL245, BLL253, BLL262, BLL263, BLLR202, BLLR203, ENGC403

### #71 · module-menu · MISSING · `div#header` › gold `div#module-menu-content.moduleMenu` vs Claude `—` — CANDIDATE
- pages 41 / modules 11 / lines 41; consensus (all) 0.75 of 2349 gold pages with the region; derivable 1.00 (0 lines with no WT source)
- by template: Standard 9m/38p c=0.77; Inquiry 2m/3p c=0.83
- by subject: None 4m/19p c=0.80; ConnectED 2m/3p c=0.76; Online Safety (OS9000) 2m/9p c=1.00; Leaving to Learn 2m/9p c=0.87; NCEA1 1m/1p c=0.71
- by era: Refresh 11m/41p c=0.75
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:45 — | Menu content class | `class="bg row"` | `class="moduleMenu"` |
  - KB: 06_TEMPLATE_RECOGNITION.md:94 — **Header:** `#module-code` → `<h1>` (module code or lesson number), then `<h1><span>Title</span></h1>`, then `#module-head-buttons` → `#module-menu-bu
  - KB: 10_CORPUS_VALIDATED_SCAFFOLDING.md:23 — - **Lesson pages → `simplified`** is dominant by a wide margin (plain `<h5>` label menu inside `#module-menu-content`). A minority of series ship **no
- **ANZH103** ANZH103_1_0.html ↔ ANZH103_3_0.html (content, derivable=True)
  - gold: `div#module-menu-content.moduleMenu  «Understand»`
  - Claude: `—`
  - WT: `**UNDERSTAND**`
- **BLLR201** BLLR201_1_1.html ↔ BLLR201_1_0.html (content, derivable=True)
  - gold: `div#module-menu-content.moduleMenu  «We are learning:»`
  - Claude: `—`
  - WT: `*We are learning:*`
- **BLLR202** BLLR202_1_1.html ↔ BLLR202_1_0.html (content, derivable=True)
  - gold: `div#module-menu-content.moduleMenu  «We are learning:»`
  - Claude: `—`
  - WT: `*We are learning:*`
- modules: ANZH103, BLLR201, BLLR202, BLLR203, CEDT207, CEDT301, HES1006, OSSC401, OSSC501, XGF9002, XGF9004

### #74 · module-menu · EXTRA · `li>b` › gold `—` vs Claude `b` — CANDIDATE
- pages 23 / modules 10 / lines 43; consensus (all) 0.99 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
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

### #76 · module-menu · EXTRA · `div.col-12.col-md-6.paddingR` › gold `—` vs Claude `h5>span` — CANDIDATE
- pages 10 / modules 10 / lines 12; consensus (all) 0.97 of 2349 gold pages with the region; derivable structure-only (0 lines with no WT source)
- by template: Standard 10m/10p c=0.97
- by subject: 1-10 Blended Literacy 5m/5p c=0.75; 1-10 English 3m/3p c=1.00; None 1m/1p c=1.00; Leaving to Learn 1m/1p c=1.00
- by era: Refresh 10m/10p c=0.97
- authority (§1b): 1 — KB rule (verify the hit's scope)
  - KB: 06_TEMPLATE_RECOGNITION.md:158 — **Module menu:** Two-column layout (`col-md-6 col-12 paddingR` + `col-md-6 col-12 paddingL`).
- **BLL131** BLL131_0_0.html ↔ BLL131-01.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «Do»`
- **BLL174** BLL174_0_0.html ↔ BLL174-00.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «Do»`
- **BLL175** BLL175_0_0.html ↔ BLL175-00.html (structure, derivable=True)
  - gold: `—`
  - Claude: `h5  «Do»`
- modules: BLL131, BLL174, BLL175, BLL176, BLL177, ENGC301, ENGC302, ENGC401, ENGC403, XWHA02
