# THE PLACEMENT CENSUS (LOOP §1g, D14-S1) — where the human puts it vs where Claude puts it

Generated 2026-09-27 03:41 by `outputs/_placement_census.py` over 533 modules / 2487 paired pages (`_corpus.gate_mods()`; the skeleton gate's pairing) in 83 s. A block = one h1–h6 / p / li / td / th / figcaption / dt / dd with ≥ 20 characters or ≥ 4 words; the module menu's nav labels are not blocks.

## Summary — the fate of every gold block

- **SAME**: 67133 (41.0 %)
- **MOVED**: 35501 (21.7 %)
- **OTHER-PAGE**: 8166 (5.0 %)
- **ABSENT-inWT**: 16495 (10.1 %)
- **ABSENT-notWT**: 36583 (22.3 %)
- total gold blocks: 163878

`SAME` = Claude has the text on the paired page in the same container path; `MOVED` = on the paired page in a DIFFERENT container (the table below); `OTHER-PAGE` = only on another Claude page of the module; `ABSENT-inWT` = on no Claude page but in the Writers Template (a derivable loss); `ABSENT-notWT` = the developer's own words (not derivable).

## 1. The transition table — gold region → Claude region (MOVED, OTHER-PAGE and ABSENT), largest first

Floors (§1d / §1g): a chrome transition (header / menu / footer on either side) needs 10 modules; a body transition 20 pages. `share` = of the gold's region-A blocks in the best family (that Claude has anywhere), the share that took this fate — a consistent placement at ≥ 0.60 over the floor is a CANDIDATE.

| # | gold region | Claude region / fate | blocks | pages | modules | best family (share, blocks, modules) | templates | flag |
|---:|---|---|---:|---:|---:|---|---|---|
| 1 | `acks` | `ABSENT-notWT` | 16716 | 514 | 485 | XOTPG (0.94, 76, 5) | Standard 11881, Inquiry 2318, Fundamentals 1932 | not derivable |
| 2 | `body:activity` | `ABSENT-notWT` | 4352 | 1131 | 380 | ART (0.67, 195, 4) | Standard 3176, Bilingual 579, Fundamentals 450 | not derivable |
| 3 | `body:free` | `ABSENT-notWT` | 3993 | 945 | 358 | MXEX (0.35, 142, 5) | Standard 3096, Fundamentals 573, Bilingual 251 | not derivable |
| 4 | `acks` | `OTHER-PAGE` | 3488 | 254 | 240 | XTAS (0.77, 340, 3) | Standard 3401, Inquiry 45, Bilingual 42 | acks gate |
| 5 | `body:widget:dragAndDrop` | `body:widget:cv2-interactive` | 3168 | 430 | 261 | OSAI (0.99, 70, 4) | Standard 2661, Fundamentals 421, Inquiry 43 | un-built widget (A1) |
| 6 | `body:activity` | `body:free` | 2870 | 614 | 322 | FRFUN (0.37, 38, 3) | Standard 1838, Bilingual 697, Fundamentals 274 | floor ok |
| 7 | `body:activity` | `body:widget:cv2-interactive` | 2624 | 699 | 334 | OSOH (0.43, 53, 5) | Standard 1974, Fundamentals 384, Bilingual 239 | floor ok |
| 8 | `body:widget:multiChoiceQuiz` | `body:widget:cv2-interactive` | 2348 | 229 | 150 | ENGJ (0.97, 33, 4) | Standard 1867, Fundamentals 433, Inquiry 39 | un-built widget (A1) |
| 9 | `body:activity` | `ABSENT-inWT` | 2342 | 728 | 324 | PWY (0.50, 137, 5) | Standard 1779, Fundamentals 324, Bilingual 162 | floor ok |
| 10 | `body:free` | `ABSENT-inWT` | 2336 | 653 | 293 | OSOH (0.23, 110, 5) | Standard 1836, Fundamentals 418, Inquiry 52 | floor ok |
| 11 | `body:free` | `body:widget:cv2-interactive` | 1718 | 367 | 211 | OSAH (0.38, 80, 3) | Standard 1423, Fundamentals 221, Inquiry 44 | floor ok |
| 12 | `body:widget:accordion` | `ABSENT-notWT` | 1693 | 179 | 113 | HIS (0.65, 192, 4) | Standard 1410, Fundamentals 143, Bilingual 77 | not derivable |
| 13 | `menu:flat` | `ABSENT-notWT` | 1501 | 472 | 192 | ARFUN (1.00, 5, 5) | Standard 1275, Inquiry 169, Fundamentals 57 | not derivable |
| 14 | `menu:flat` | `OTHER-PAGE` | 1466 | 259 | 69 | PWY (0.55, 44, 5) | Standard 1440, Inquiry 21, Fundamentals 5 | floor ok |
| 15 | `body:widget:accordion` | `body:widget:cv2-interactive` | 1291 | 163 | 114 | HPFUN (0.28, 39, 3) | Standard 1074, Fundamentals 175, Inquiry 42 | un-built widget (A1) |
| 16 | `acks` | `ABSENT-inWT` | 1249 | 252 | 238 | PWY (0.29, 74, 5) | Standard 929, Inquiry 211, Fundamentals 101 | acks gate |
| 17 | `body:widget:accordion` | `ABSENT-inWT` | 1193 | 208 | 128 | XMES (0.53, 116, 3) | Standard 960, Fundamentals 218, Inquiry 13 | floor ok |
| 18 | `body:widget:accordion` | `body:free` | 1155 | 140 | 80 | TEFUN (0.74, 64, 4) | Standard 879, Fundamentals 145, Inquiry 116 | CANDIDATE |
| 19 | `body:free` | `body:activity` | 1053 | 295 | 157 | TRR (0.15, 226, 10) | Standard 739, Bilingual 230, Fundamentals 81 | floor ok |
| 20 | `body:alert` | `body:free` | 978 | 300 | 164 | BLLR (0.49, 18, 3) | Standard 782, Fundamentals 100, Bilingual 89 | floor ok |
| 21 | `body:widget:multiChoiceQuiz` | `ABSENT-inWT` | 942 | 139 | 91 | PWY (0.56, 179, 5) | Standard 758, Fundamentals 153, Inquiry 31 | floor ok |
| 22 | `menu:flat` | `ABSENT-inWT` | 932 | 548 | 176 | XOTPB (0.36, 52, 6) | Standard 886, Inquiry 44, Fundamentals 2 | floor ok |
| 23 | `body:free` | `OTHER-PAGE` | 878 | 112 | 79 | TRR (0.25, 372, 5) | Standard 478, Bilingual 372, Fundamentals 16 | floor ok |
| 24 | `body:widget:dragAndDrop` | `ABSENT-notWT` | 793 | 164 | 122 | HES (1.00, 50, 3) | Standard 630, Fundamentals 121, Bilingual 33 | not derivable |
| 25 | `body:panel:activity` | `body:panel:widget:cv2-interactive` | 755 | 42 | 42 | BLL (0.22, 414, 12) | Inquiry 753, Standard 2 | floor ok |
| 26 | `body:alert` | `ABSENT-notWT` | 738 | 275 | 135 | PHE (0.69, 20, 4) | Standard 591, Bilingual 63, Fundamentals 57 | not derivable |
| 27 | `body:widget:flipCard` | `body:widget:cv2-interactive` | 716 | 115 | 94 | XOTPB (1.00, 36, 6) | Standard 609, Fundamentals 95, Bilingual 7 | un-built widget (A1) |
| 28 | `body:widget:dragAndDrop` | `ABSENT-inWT` | 680 | 191 | 130 | OSGM (0.40, 27, 3) | Standard 575, Fundamentals 92, Inquiry 7 | floor ok |
| 29 | `body:widget:tabs` | `ABSENT-inWT` | 665 | 94 | 64 | OSOH (0.53, 31, 3) | Standard 615, Fundamentals 50 | floor ok |
| 30 | `body:widget:carousel` | `ABSENT-inWT` | 634 | 136 | 107 | BLL (0.49, 99, 13) | Standard 550, Fundamentals 74, Inquiry 5 | floor ok |
| 31 | `body:panel:activity` | `ABSENT-notWT` | 626 | 53 | 51 | TWHA (0.38, 239, 6) | Inquiry 610, Standard 16 | not derivable |
| 32 | `body:widget:tabs` | `body:free` | 612 | 70 | 57 | TEFUN (0.80, 116, 5) | Standard 462, Fundamentals 144, Inquiry 6 | CANDIDATE |
| 33 | `body:widget:carousel` | `ABSENT-notWT` | 610 | 118 | 94 | XDLS (0.42, 64, 5) | Standard 458, Fundamentals 100, Inquiry 37 | not derivable |
| 34 | `body:widget:dropDown` | `ABSENT-inWT` | 603 | 58 | 54 | OSAI (0.82, 62, 4) | Standard 479, Fundamentals 124 | CANDIDATE |
| 35 | `body:widget:dropQuiz` | `body:widget:cv2-interactive` | 602 | 110 | 94 | OSAI (0.89, 33, 4) | Standard 391, Fundamentals 211 | un-built widget (A1) |
| 36 | `body:widget:tabs` | `body:widget:cv2-interactive` | 568 | 86 | 56 | ENGJ (0.44, 85, 5) | Standard 546, Fundamentals 17, Inquiry 5 | un-built widget (A1) |
| 37 | `body:activity` | `OTHER-PAGE` | 567 | 213 | 97 | TRR (0.07, 177, 8) | Standard 385, Bilingual 178, Inquiry 4 | floor ok |
| 38 | `body:widget:radioQuiz` | `body:widget:cv2-interactive` | 558 | 84 | 70 | ENGC (0.87, 53, 6) | Standard 415, Fundamentals 137, Bilingual 6 | un-built widget (A1) |
| 39 | `body:widget:reorder` | `body:widget:cv2-interactive` | 554 | 80 | 59 | BLL (0.88, 68, 10) | Standard 488, Fundamentals 62, Bilingual 3 | un-built widget (A1) |
| 40 | `body:alert` | `ABSENT-inWT` | 516 | 211 | 118 | ENGR (0.38, 15, 3) | Standard 436, Fundamentals 62, Bilingual 11 | floor ok |
| 41 | `body:widget:flipCard` | `ABSENT-inWT` | 516 | 98 | 76 | PNR (0.60, 15, 3) | Standard 424, Fundamentals 68, Bilingual 15 | CANDIDATE |
| 42 | `body:widget:accordion` | `body:activity` | 490 | 50 | 35 | BLL (0.08, 59, 11) | Standard 450, Bilingual 39, Fundamentals 1 | floor ok |
| 43 | `body:widget:tabs` | `ABSENT-notWT` | 486 | 70 | 48 | AGH (0.36, 39, 4) | Standard 458, Fundamentals 27, Inquiry 1 | not derivable |
| 44 | `body:widget:carousel` | `body:widget:cv2-interactive` | 478 | 85 | 68 | BLLR (0.37, 23, 3) | Standard 349, Fundamentals 97, Bilingual 29 | un-built widget (A1) |
| 45 | `body:widget:typing` | `body:widget:cv2-interactive` | 463 | 100 | 63 | ENGC (1.00, 13, 3) | Standard 419, Fundamentals 42, Bilingual 2 | un-built widget (A1) |
| 46 | `body:panel:activity` | `ABSENT-inWT` | 461 | 43 | 42 | TWHK (0.32, 73, 4) | Inquiry 458, Standard 3 | floor ok |
| 47 | `body:panel:free` | `ABSENT-notWT` | 454 | 42 | 38 | TWHA (0.39, 167, 6) | Inquiry 322, Standard 132 | not derivable |
| 48 | `body:widget:wordHighlighter` | `body:free` | 438 | 55 | 42 | WJFUN (0.72, 277, 9) | Fundamentals 308, Standard 130 | CANDIDATE |
| 49 | `body:widget:multiChoiceQuiz` | `ABSENT-notWT` | 430 | 75 | 63 | SSFUN (0.81, 42, 4) | Standard 285, Fundamentals 107, Bilingual 30 | not derivable |
| 50 | `body:panel:activity` | `body:panel:free` | 401 | 44 | 42 | CEDK (0.20, 44, 3) | Inquiry 391, Standard 10 | floor ok |
| 51 | `body:widget:multiChoiceQuiz` | `body:free` | 399 | 47 | 42 | WJFUN (0.29, 93, 3) | Standard 248, Fundamentals 137, Bilingual 12 | floor ok |
| 52 | `body:panel:widget:accordion` | `ABSENT-inWT` | 391 | 15 | 14 | EXPFUN (0.47, 330, 4) | Inquiry 384, Standard 7 | below floor |
| 53 | `body:widget:multiChoiceQuiz` | `body:activity` | 383 | 59 | 44 | PES (0.73, 81, 3) | Standard 314, Fundamentals 64, Bilingual 4 | CANDIDATE |
| 54 | `body:widget:dropDown` | `ABSENT-notWT` | 343 | 20 | 18 | ENGI (0.26, 11, 3) | Standard 231, Fundamentals 112 | not derivable |
| 55 | `body:widget:typing` | `ABSENT-notWT` | 336 | 73 | 51 | MXEX (0.51, 34, 3) | Standard 292, Fundamentals 38, Bilingual 6 | not derivable |
| 56 | `body:widget:accordion` | `OTHER-PAGE` | 330 | 19 | 17 |  | Standard 308, Bilingual 21, Inquiry 1 | below floor |
| 57 | `body:widget:speechBubble` | `ABSENT-inWT` | 312 | 103 | 69 | MXFL (0.47, 26, 4) | Standard 254, Fundamentals 42, Inquiry 14 | floor ok |
| 58 | `menu:Information` | `ABSENT-notWT` | 308 | 99 | 87 | ART (0.69, 33, 3) | Standard 255, Bilingual 52, Inquiry 1 | not derivable |
| 59 | `menu:flat` | `body:free` | 285 | 83 | 44 | EXPFUN (0.86, 18, 4) | Standard 229, Inquiry 34, Fundamentals 22 | CANDIDATE |
| 60 | `menu:Overview` | `ABSENT-notWT` | 276 | 92 | 91 | MXFL (0.41, 22, 5) | Standard 244, Bilingual 26, Fundamentals 4 | not derivable |
| 61 | `body:widget:dropDown` | `body:widget:cv2-interactive` | 275 | 34 | 30 | BLL (0.90, 72, 4) | Standard 206, Fundamentals 60, Bilingual 9 | un-built widget (A1) |
| 62 | `menu:Information` | `OTHER-PAGE` | 274 | 37 | 10 |  | Standard 274 | floor ok |
| 63 | `menu:Information` | `menu:Knowledge` | 267 | 18 | 9 | BLL (0.55, 105, 7) | Standard 267 | below floor |
| 64 | `menu:Overview` | `OTHER-PAGE` | 267 | 35 | 12 |  | Standard 267 | floor ok |
| 65 | `body:panel:widget:accordion` | `body:panel:free` | 262 | 14 | 14 | TWHA (0.37, 11, 3) | Inquiry 262 | below floor |
| 66 | `body:widget:dropQuiz` | `ABSENT-inWT` | 260 | 61 | 56 | BLL (0.26, 27, 5) | Standard 166, Fundamentals 94 | floor ok |
| 67 | `body:widget:carousel` | `body:free` | 248 | 58 | 53 | TEFUN (0.36, 47, 4) | Standard 169, Fundamentals 72, Bilingual 6 | floor ok |
| 68 | `body:widget:dropQuiz` | `ABSENT-notWT` | 244 | 49 | 42 | SSFUN (0.38, 26, 4) | Standard 175, Fundamentals 69 | not derivable |
| 69 | `body:panel:widget:accordion` | `ABSENT-notWT` | 233 | 16 | 15 | EXPFUN (0.21, 148, 3) | Inquiry 177, Standard 56 | not derivable |
| 70 | `body:widget:dragAndDrop` | `body:free` | 229 | 44 | 39 | PES (0.17, 15, 3) | Standard 144, Fundamentals 36, Inquiry 34 | floor ok |
| 71 | `header:other` | `ABSENT-notWT` | 224 | 209 | 111 | MXFUN (1.00, 3, 3) | Standard 184, Fundamentals 17, Bilingual 17 | not derivable |
| 72 | `body:panel:free` | `ABSENT-inWT` | 208 | 40 | 38 | CEDO (0.11, 24, 4) | Inquiry 178, Standard 30 | floor ok |
| 73 | `body:widget:flipCard` | `ABSENT-notWT` | 206 | 63 | 57 | SSFUN (0.38, 18, 3) | Standard 138, Fundamentals 60, Bilingual 5 | not derivable |
| 74 | `body:free` | `body:alert` | 206 | 80 | 42 | HIS (0.02, 28, 4) | Standard 190, Fundamentals 15, Inquiry 1 | floor ok |
| 75 | `body:free` | `body:widget:accordion` | 202 | 37 | 30 | ENG (0.05, 5, 3) | Standard 174, Fundamentals 20, Inquiry 8 | floor ok |
| 76 | `body:alert:side` | `body:alert` | 201 | 98 | 57 | ENGJ (0.40, 6, 3) | Standard 175, Fundamentals 20, Inquiry 6 | floor ok |
| 77 | `body:widget:speechBubble` | `body:widget:cv2-interactive` | 200 | 92 | 60 | XDLS (0.26, 47, 5) | Standard 173, Fundamentals 20, Bilingual 4 | un-built widget (A1) |
| 78 | `body:widget:wordHighlighter` | `ABSENT-inWT` | 199 | 48 | 40 | ENGJ (0.55, 23, 5) | Standard 107, Fundamentals 92 | floor ok |
| 79 | `body:panel:free` | `body:panel:widget:cv2-interactive` | 199 | 23 | 23 | CEDR (0.18, 42, 3) | Inquiry 196, Standard 3 | floor ok |
| 80 | `body:widget:speechBubble` | `ABSENT-notWT` | 188 | 70 | 51 | XOTPB (1.00, 6, 6) | Standard 113, Fundamentals 44, Bilingual 19 | not derivable |
| 81 | `body:widget:typing` | `ABSENT-inWT` | 182 | 51 | 39 | MXEO (0.23, 20, 4) | Standard 154, Fundamentals 28 | floor ok |
| 82 | `body:alert:side` | `ABSENT-notWT` | 173 | 90 | 59 | MXEX (0.50, 9, 3) | Standard 126, Fundamentals 29, Bilingual 17 | not derivable |
| 83 | `header:other` | `OTHER-PAGE` | 169 | 140 | 46 | ANZH (0.22, 22, 4) | Standard 158, Bilingual 9, Inquiry 2 | floor ok |
| 84 | `menu:Information` | `menu:Overview` | 168 | 16 | 16 | MXDI (0.33, 28, 3) | Standard 151, Bilingual 17 | floor ok |
| 85 | `body:free` | `body:widget:carousel` | 166 | 38 | 35 | AGH (0.02, 23, 3) | Standard 131, Fundamentals 35 | floor ok |
| 86 | `body:widget:flipCard` | `body:free` | 164 | 35 | 31 | SSFUN (0.21, 10, 3) | Standard 133, Fundamentals 31 | floor ok |
| 87 | `body:widget:tabs` | `OTHER-PAGE` | 164 | 15 | 11 |  | Standard 160, Fundamentals 4 | below floor |
| 88 | `menu:Overview` | `ABSENT-inWT` | 162 | 81 | 66 | GEO (0.11, 7, 3) | Standard 136, Fundamentals 16, Bilingual 6 | floor ok |
| 89 | `body:widget:speechBubble` | `body:free` | 159 | 86 | 53 | TEFUN (0.23, 12, 4) | Standard 114, Fundamentals 30, Bilingual 8 | floor ok |
| 90 | `body:widget:accordion` | `body:widget:carousel` | 158 | 18 | 12 |  | Standard 158 | below floor |
| 91 | `menu:Information` | `ABSENT-inWT` | 157 | 80 | 68 | OSGM (0.29, 6, 3) | Standard 151, Bilingual 4, Inquiry 2 | floor ok |
| 92 | `body:alert` | `OTHER-PAGE` | 155 | 58 | 33 | TRR (0.25, 62, 4) | Standard 93, Bilingual 62 | floor ok |
| 93 | `body:activity` | `body:alert` | 154 | 53 | 34 | ANZH (0.08, 49, 3) | Standard 148, Fundamentals 3, Bilingual 2 | floor ok |
| 94 | `menu:LI` | `menu:Overview` | 153 | 12 | 12 | XMES (0.98, 61, 3) | Standard 103, Bilingual 43, Inquiry 6 | CANDIDATE |
| 95 | `body:activity` | `body:widget:accordion` | 147 | 36 | 31 | MXFL (0.01, 13, 3) | Standard 146, Inquiry 1 | floor ok |
| 96 | `body:panel:widget:dragAndDrop` | `body:panel:widget:cv2-interactive` | 147 | 20 | 20 | CEDO (0.91, 31, 3) | Inquiry 147 | un-built widget (A1) |
| 97 | `body:free:side` | `body:free` | 146 | 51 | 41 | HIS (0.77, 30, 6) | Standard 98, Fundamentals 46, Inquiry 2 | CANDIDATE |
| 98 | `header:other` | `ABSENT-inWT` | 142 | 136 | 71 | PES (0.36, 17, 5) | Standard 133, Inquiry 7, Fundamentals 2 | floor ok |
| 99 | `body:panel:widget:multiChoiceQuiz` | `body:panel:widget:cv2-interactive` | 132 | 9 | 9 | TWHA (0.25, 60, 3) | Inquiry 132 | un-built widget (A1) |
| 100 | `body:widget:hintSlider` | `body:widget:cv2-interactive` | 127 | 20 | 17 | ENFUN (0.21, 15, 3) | Standard 102, Fundamentals 25 | un-built widget (A1) |
| 101 | `body:panel:widget:accordion` | `body:panel:widget:cv2-interactive` | 127 | 11 | 11 |  | Inquiry 125, Standard 2 | un-built widget (A1) |
| 102 | `body:panel:free` | `body:panel:activity` | 125 | 27 | 27 | BLL (0.23, 28, 8) | Inquiry 125 | floor ok |
| 103 | `body:free` | `header:other` | 123 | 123 | 50 | ANZH (0.03, 16, 4) | Standard 120, Inquiry 3 | floor ok |
| 104 | `body:widget:dragAndDrop` | `body:activity` | 122 | 25 | 24 | MXFL (0.07, 18, 4) | Standard 116, Bilingual 6 | floor ok |
| 105 | `body:widget:tabs` | `body:alert` | 120 | 9 | 6 |  | Standard 120 | below floor |
| 106 | `body:widget:radioQuiz` | `ABSENT-inWT` | 119 | 22 | 22 | HPFUN (0.41, 28, 3) | Standard 73, Fundamentals 37, Inquiry 9 | floor ok |
| 107 | `body:free:side` | `ABSENT-notWT` | 119 | 43 | 36 | XDLS (0.35, 7, 3) | Standard 91, Fundamentals 26, Inquiry 2 | not derivable |
| 108 | `body:alert` | `body:activity` | 119 | 44 | 33 | ENGJ (0.26, 32, 4) | Standard 86, Bilingual 29, Fundamentals 4 | floor ok |
| 109 | `body:alert:side` | `ABSENT-inWT` | 117 | 61 | 46 | MXFU (0.50, 22, 3) | Standard 102, Fundamentals 10, Bilingual 5 | floor ok |
| 110 | `menu:Information` | `menu:Practices` | 117 | 18 | 9 | BLL (0.35, 66, 7) | Standard 117 | below floor |
| 111 | `body:widget:radioQuiz` | `ABSENT-notWT` | 114 | 20 | 18 | AGH (0.26, 19, 3) | Standard 102, Bilingual 11, Fundamentals 1 | not derivable |
| 112 | `body:alert` | `body:widget:cv2-interactive` | 114 | 54 | 42 | ENFUN (0.09, 10, 5) | Standard 76, Fundamentals 28, Bilingual 10 | floor ok |
| 113 | `body:panel:widget:multiChoiceQuiz` | `ABSENT-inWT` | 113 | 8 | 8 | TWHA (0.36, 85, 4) | Inquiry 113 | below floor |
| 114 | `body:widget:memoryGame` | `body:widget:cv2-interactive` | 113 | 22 | 19 |  | Standard 89, Fundamentals 12, Bilingual 12 | un-built widget (A1) |
| 115 | `body:widget:reorder` | `ABSENT-inWT` | 112 | 30 | 23 |  | Standard 100, Fundamentals 12 | floor ok |
| 116 | `body:widget:radioQuiz` | `body:activity` | 109 | 22 | 17 | ANZH (0.62, 16, 3) | Standard 109 | CANDIDATE |
| 117 | `body:panel:widget:flipCard` | `ABSENT-notWT` | 109 | 7 | 7 | TWHA (0.44, 90, 4) | Inquiry 109 | not derivable |
| 118 | `menu:LI` | `menu:Information` | 108 | 5 | 5 | TRR (0.41, 108, 5) | Bilingual 108 | below floor |
| 119 | `body:widget:selfCheck` | `body:widget:cv2-interactive` | 107 | 33 | 21 | BLL (0.71, 10, 3) | Standard 94, Bilingual 6, Fundamentals 4 | un-built widget (A1) |
| 120 | `body:widget:wordHighlighter` | `ABSENT-notWT` | 105 | 24 | 22 | ENFUN (0.31, 22, 4) | Standard 60, Fundamentals 45 | not derivable |
| 121 | `body:panel:widget:multiChoiceQuiz` | `ABSENT-notWT` | 105 | 7 | 7 | TWHA (0.39, 94, 4) | Inquiry 97, Standard 8 | not derivable |
| 122 | `body:widget:tabs` | `body:widget:carousel` | 105 | 11 | 7 |  | Standard 81, Fundamentals 24 | below floor |
| 123 | `body:panel:widget:tabs` | `ABSENT-notWT` | 105 | 3 | 2 |  | Standard 105 | not derivable |
| 124 | `body:widget:hintSlider` | `body:widget:flipCard` | 103 | 7 | 5 | ENFUN (0.30, 21, 4) | Standard 82, Fundamentals 21 | below floor |
| 125 | `menu:Standards` | `ABSENT-notWT` | 92 | 42 | 40 | GEO (0.40, 4, 3) | Standard 89, Inquiry 3 | not derivable |
| 126 | `body:free` | `body:widget:flipCard` | 92 | 14 | 13 | XLP (0.03, 12, 3) | Standard 60, Fundamentals 32 | below floor |
| 127 | `body:activity` | `body:widget:flipCard` | 92 | 11 | 8 |  | Standard 85, Inquiry 7 | below floor |
| 128 | `body:widget:selfCheck` | `ABSENT-inWT` | 91 | 26 | 21 |  | Standard 70, Inquiry 14, Fundamentals 7 | floor ok |
| 129 | `body:widget:typing` | `body:activity` | 90 | 29 | 23 | MXFL (0.05, 10, 4) | Standard 88, Fundamentals 2 | floor ok |
| 130 | `body:panel:widget:flipCard` | `body:panel:widget:cv2-interactive` | 88 | 13 | 13 |  | Inquiry 88 | un-built widget (A1) |
| 131 | `other:free` | `body:free` | 86 | 5 | 5 |  | Standard 86 | below floor |
| 132 | `menu:pane2` | `menu:Overview` | 86 | 7 | 7 | XMES (1.00, 45, 3) | Standard 64, Bilingual 22 | below floor |
| 133 | `body:widget:multiChoiceQuiz` | `OTHER-PAGE` | 84 | 12 | 10 |  | Standard 64, Bilingual 20 | below floor |
| 134 | `body:widget:wordHighlighter` | `body:widget:cv2-interactive` | 84 | 18 | 17 | BLL (0.35, 15, 3) | Standard 45, Fundamentals 39 | un-built widget (A1) |
| 135 | `body:alert:side` | `body:activity` | 79 | 36 | 20 | TRR (0.48, 29, 3) | Standard 49, Bilingual 29, Fundamentals 1 | floor ok |
| 136 | `body:free:side` | `ABSENT-inWT` | 78 | 30 | 29 |  | Standard 75, Fundamentals 2, Inquiry 1 | floor ok |
| 137 | `menu:Standards` | `ABSENT-inWT` | 78 | 53 | 46 | XDLS (0.34, 20, 8) | Standard 68, Inquiry 10 | floor ok |
| 138 | `body:alert` | `body:alert:side` | 78 | 42 | 28 | BLL (0.13, 4, 4) | Standard 63, Fundamentals 15 | floor ok |
| 139 | `body:panel:widget:carousel` | `ABSENT-inWT` | 76 | 12 | 12 | BLL (0.86, 42, 3) | Inquiry 71, Standard 5 | below floor |
| 140 | `body:widget:hintSlider` | `ABSENT-notWT` | 75 | 16 | 14 |  | Standard 56, Fundamentals 19 | not derivable |
| 141 | `body:widget:wordSelect` | `body:activity` | 75 | 21 | 20 | WJFUN (0.61, 33, 5) | Fundamentals 36, Standard 35, Bilingual 4 | CANDIDATE |
| 142 | `body:widget:dropQuiz` | `body:free` | 74 | 10 | 10 |  | Fundamentals 41, Standard 23, Bilingual 10 | below floor |
| 143 | `body:panel:widget:flipCard` | `ABSENT-inWT` | 73 | 7 | 7 | TWHA (0.16, 33, 4) | Inquiry 73 | below floor |
| 144 | `body:widget:wordSelect` | `ABSENT-inWT` | 71 | 19 | 16 |  | Fundamentals 37, Standard 33, Bilingual 1 | below floor |
| 145 | `body:widget:accordion` | `body:alert` | 71 | 21 | 15 | XDLS (0.01, 8, 5) | Standard 70, Inquiry 1 | floor ok |
| 146 | `body:widget:tabs` | `body:activity` | 70 | 11 | 10 | HIS (0.12, 20, 3) | Standard 69, Fundamentals 1 | below floor |
| 147 | `body:free` | `menu:flat` | 68 | 11 | 11 |  | Fundamentals 48, Standard 13, Inquiry 7 | floor ok |
| 148 | `body:widget:selfCheck` | `ABSENT-notWT` | 67 | 12 | 10 |  | Fundamentals 35, Standard 26, Bilingual 6 | not derivable |
| 149 | `body:alert:side` | `body:free` | 67 | 34 | 31 | ENGI (0.17, 5, 3) | Standard 44, Fundamentals 17, Bilingual 6 | floor ok |
| 150 | `body:widget:accordion` | `body:widget:flipCard` | 67 | 6 | 5 |  | Standard 67 | below floor |

## 2. Headings only (the SECTIONS) — gold region → Claude region / fate

| gold region | Claude region / fate | headings | pages | modules | examples |
|---|---|---:|---:|---:|---|
| `body:activity` | `ABSENT-notWT` | 800 | 453 | 197 | AGH1001 AGH1001_1_0.html <h3>→<—> “What are primary products?”; AGH1001 AGH1001_1_0.html <h3>→<—> “Agricultural and horticultural products”; AGH1001 AGH1001_2_0.html <h3>→<—> “Value of Primary Products” |
| `body:activity` | `ABSENT-inWT` | 497 | 351 | 194 | AGH1001 AGH1001_3_0.html <h3>→<—> “Māori creation story”; AGH1001 AGH1001_4_0.html <h3>→<—> “New Zealand’s four seasons”; AGH1002 AGH1002_6_0.html <h3>→<—> “Levels of organic matter” |
| `body:free` | `ABSENT-notWT` | 366 | 204 | 119 | AGH1001 AGH1001_2_0.html <h4>→<—> “Pre-European settlement”; AGH1001 AGH1001_2_0.html <h4>→<—> “Late 18th Century - Mid 19th Century”; AGH1001 AGH1001_2_0.html <h4>→<—> “Late 19th Century - Mid 20th Century” |
| `body:activity` | `body:free` | 332 | 198 | 133 | AGH1001 AGH1001_3_0.html <h3>→<h3> “Self Check: True or False”; AGH1004 AGH1004_1_0.html <h3>→<h3> “Knowledge self-check”; AGH1004 AGH1004_2_0.html <h3>→<h3> “Reflective questions” |
| `body:widget:accordion` | `ABSENT-notWT` | 313 | 80 | 56 | AGH1003 AGH1003_4_0.html <h4>→<—> “Returning crop residues”; AGH1003 AGH1003_7_0.html <h4>→<—> “What causes poor drainage?”; AGH1003 AGH1003_7_0.html <h5>→<—> “This open drain is an example of surface drainage.” |
| `menu:flat` | `ABSENT-inWT` | 312 | 293 | 80 | AGH1001 AGH1001_1_0.html <h5>→<—> “We are learning to:”; AGH1001 AGH1001_2_0.html <h5>→<—> “We are learning to:”; AGH1001 AGH1001_3_0.html <h5>→<—> “We are learning to:” |
| `body:activity` | `body:widget:cv2-interactive` | 312 | 171 | 100 | ANZH203 ANZH203_1_0.html <h3>→<p> “Comprehension activity”; ARFUN02 ARFUN02_0_0.html <h3>→<p> “What Have I Learned? He aha aku i ako ai?”; ARFUN03 ARFUN03_0_0.html <h3>→<p> “What have I learnt?” |
| `body:free` | `ABSENT-inWT` | 295 | 185 | 132 | AGH1001 AGH1001_0_0.html <h3>→<—> “An introduction to agricultural and horticultural ”; AGH1002 AGH1002_3_0.html <h4>→<—> “C = carbon, H = Hydrogen, O = Oxygen”; AGH1005 AGH1005_6_0.html <h4>→<—> “Mycorrhizal associations” |
| `body:widget:accordion` | `ABSENT-inWT` | 238 | 109 | 78 | AGH1003 AGH1003_4_0.html <h4>→<—> “Slurry Tankers/Umbilical Systems”; AGH1005 AGH1005_2_0.html <h4>→<—> “Disease and pest resistance”; AGH1005 AGH1005_2_0.html <h4>→<—> “Breeding and selection” |
| `header:other` | `ABSENT-notWT` | 221 | 206 | 110 | AGH1004 AGH1004_1_0.html <h1>→<—> “Factors influencing where primary production syste”; AGH1004 AGH1004_5_0.html <h1>→<—> “Where does our water come from?”; AGH1004 AGH1004_6_0.html <h1>→<—> “Market Factor Influences” |
| `body:widget:accordion` | `body:widget:cv2-interactive` | 211 | 76 | 62 | AGH1009 AGH1009_1_0.html <h5>→<td> “Cultural recognition (Cultural recognition princip”; AGH1009 AGH1009_1_0.html <h5>→<td> “Sustainable Resource Management (Sustainable Resou”; ANZH203 ANZH203_3_0.html <h4>→<p> “Tupaia and the Endeavour” |
| `body:activity` | `OTHER-PAGE` | 197 | 133 | 56 | ANZH301 ANZH301_1_0.html <h4>→<—> “Go to your journal”; ANZH303 ANZH303_4_0.html <h4>→<—> “Go to your journal”; ANZH303 ANZH303_6_0.html <h4>→<—> “Go to your journal” |
| `menu:flat` | `ABSENT-notWT` | 185 | 185 | 63 | ARFUN01 ARFUN01_0_0.html <h5>→<—> “You will show your understanding by:”; ARFUN02 ARFUN02_0_0.html <h5>→<—> “You will show your understanding by:”; ARFUN03 ARFUN03_0_0.html <h5>→<—> “You will show your understanding by:” |
| `header:other` | `OTHER-PAGE` | 169 | 140 | 46 | AGH1007 AGH1007_7_0.html <h1>→<—> “Livestock and Agriculture in Aotearoa New Zealand”; AGH1009 AGH1009_8_0.html <h1>→<—> “Primary production and soil quality.”; ANZH101 ANZH101_1_0.html <h1>→<—> “Tangata Whenua Origin Stories” |
| `body:free` | `body:widget:cv2-interactive` | 154 | 79 | 65 | AGH1002 AGH1002_3_0.html <h4>→<th> “Air level in soil”; AGH1006 AGH1006_4_0.html <h3>→<p> “Protective Structures”; AGH1009 AGH1009_1_0.html <h4>→<th> “European world view (Colonial times)” |
| `header:other` | `ABSENT-inWT` | 142 | 136 | 71 | AGH1001 AGH1001_0_0.html <h1>→<—> “From the Ground Up”; AGH1001 AGH1001_0_0.html <h1>→<—> “Mai i te Nuku ki te Rangi”; AGH1002 AGH1002_4_0.html <h1>→<—> “Physical properties of soil” |
| `body:widget:accordion` | `body:free` | 135 | 55 | 39 | AGH1004 AGH1004_2_0.html <h4>→<h4> “Semi-intensive Farming”; AGH1004 AGH1004_2_0.html <h4>→<h4> “Semi-extensive Farming”; AGH1006 AGH1006_6_0.html <h4>→<h3> “Integrated weed management” |
| `body:free` | `body:activity` | 133 | 103 | 72 | AGH1004 AGH1004_5_0.html <h3>→<h3> “Impact of Irrigation on Production”; AGH1005 AGH1005_7_0.html <h3>→<p> “Common pests and diseases”; AGH1006 AGH1006_5_0.html <h3>→<p> “What to avoid when making pruning cuts” |
| `menu:flat` | `OTHER-PAGE` | 130 | 104 | 21 | ANZH203 ANZH203_1_0.html <h4>→<—> “How will I know if I’ve learned it?”; ANZH203 ANZH203_2_0.html <h4>→<—> “How will I know if I’ve learned it?”; ANZH203 ANZH203_3_0.html <h4>→<—> “How will I know if I’ve learned it?” |
| `body:free` | `header:other` | 121 | 121 | 48 | AGH1005 AGH1005_0_0.html <h3>→<h1> “Ko te tūhura i te tipu me te tukanga i Aotearoa | ”; AGH1005 AGH1005_2_0.html <h3>→<h1> “Exploring plant anatomy and its impact on primary ”; AGH1005 AGH1005_5_0.html <h3>→<h1> “Exploring the plant process of respiration and its” |
| `body:widget:flipCard` | `ABSENT-inWT` | 108 | 38 | 32 | CEDO502 CEDO502_1_1.html <h5>→<—> “Credit card shopping”; CEDR501 CEDR501_4_0.html <h4>→<—> “Pānui 1: Aiko arrives early”; CEDR501 CEDR501_4_0.html <h4>→<—> “Pānui 2: Taika is late” |
| `body:widget:carousel` | `ABSENT-inWT` | 83 | 33 | 27 | ANZH105 ANZH105_6_0.html <h4>→<—> “New Zealand Māori Kapa haka”; ANZH303 ANZH303_5_0.html <h4>→<—> “The Eight-pointed Stars”; BLL262 BLL262_3_0.html <h5>→<—> “Pointillism Fish Part 1” |
| `body:panel:activity` | `ABSENT-notWT` | 75 | 31 | 29 | BLL120 BLL120_0_0.html <h3>→<—> “Writing words with the digraph ck”; BLL250 BLL250_0_0.html <h4>→<—> “Ben the Lamb and the Gentle Climb”; BLL250 BLL250_0_0.html <h4>→<—> “The Sleigh in the Snow” |
| `body:widget:carousel` | `ABSENT-notWT` | 74 | 25 | 19 | AGH1009 AGH1009_2_0.html <h4>→<—> “Decomposition and fossilisation”; AGH1009 AGH1009_2_0.html <h4>→<—> “Ocean Sedimentationand Absorption”; ART1006 ART1006_1_0.html <h4>→<—> “PowerPoint/slideshow presentations” |
| `body:panel:activity` | `body:panel:free` | 74 | 22 | 22 | BLL240 BLL240_0_0.html <h4>→<h5> “Words making the 'ear' sound”; BLL240 BLL240_0_0.html <h4>→<h5> “Words making the 'air' sound”; BLL240 BLL240_0_0.html <h4>→<h5> “Words making the 'ur' sound” |
| `menu:Information` | `ABSENT-notWT` | 73 | 64 | 58 | AGH1001 AGH1001_0_0.html <h5>→<—> “Want to know where to start?”; AGH1002 AGH1002_0_0.html <h5>→<—> “Want to know where to start?”; AGH1003 AGH1003_0_0.html <h5>→<—> “Want to know where to start?” |
| `body:alert` | `ABSENT-notWT` | 72 | 54 | 29 | AGH1007 AGH1007_3_0.html <h4>→<—> “Key points from the lesson:”; AGH1007 AGH1007_4_0.html <h4>→<—> “Key points from the lesson:”; AGH1007 AGH1007_5_0.html <h4>→<—> “Key points from the lesson:” |
| `body:free` | `OTHER-PAGE` | 69 | 31 | 24 | AGH1005 AGH1005_4_0.html <h3>→<—> “Exploring the plant process of transpiration”; CBI1009 CBI1009_1_0.html <h2>→<—> “Soluble and insoluble Salts”; CEDO501 CEDO501_3_0.html <h3>→<—> “Search engines and Artificial Intelligence” |
| `body:alert` | `body:free` | 68 | 53 | 39 | AGH1003 AGH1003_5_0.html <h4>→<p> “Why is it important to add lime before fertiliser ”; AGH1009 AGH1009_4_0.html <h4>→<p> “A note on sprays”; ANZH103 ANZH103_1_0.html <h3>→<h3> “What happened after the Treaty was signed on 6 Feb” |
| `body:widget:flipCard` | `body:widget:cv2-interactive` | 66 | 21 | 17 | ANZH105 ANZH105_5_0.html <h4>→<td> “What is it made of?”; ANZH105 ANZH105_5_0.html <h4>→<td> “Where is it from?”; ANZH105 ANZH105_5_0.html <h4>→<td> “How old is it?” |
| `body:alert` | `ABSENT-inWT` | 62 | 50 | 35 | AGH1003 AGH1003_1_0.html <h4>→<—> “Need some extra help?”; ANZH301 ANZH301_7_0.html <h4>→<—> “Want to know more?”; ANZH301 ANZH301_9_0.html <h4>→<—> “Some other examples of urban marae:” |
| `body:panel:activity` | `ABSENT-inWT` | 61 | 25 | 24 | BLL120 BLL120_0_0.html <h3>→<—> “Writing the letter k”; BLL120 BLL120_0_0.html <h3>→<—> “My name is, my sound is…”; BLL160 BLL160_0_0.html <h4>→<—> “A child was in bed sleeping. A duck ran in the doo” |
| `menu:Information` | `ABSENT-inWT` | 56 | 45 | 43 | BLL251 BLL251_0_0.html <h4>→<—> “Tirohanga Whānui | Overview”; BLL255 BLL255_0_0.html <h4>→<—> “Tirohanga Whānui | Overview”; BLL257 BLL257_0_0.html <h4>→<—> “Tirohanga Whānui | Overview” |
| `body:panel:widget:accordion` | `body:panel:free` | 55 | 12 | 12 | CEDK401 CEDK401_0_0.html <h4>→<h4> “Go to your journal”; CEDK401 CEDK401_0_0.html <h4>→<h4> “Go to your journal”; CEDK401 CEDK401_0_0.html <h4>→<h4> “Go to your journal” |
| `header:other` | `body:free` | 54 | 49 | 38 | AGH1006 AGH1006_8_0.html <h1>→<h3> “Pest and disease management”; ANZH301 ANZH301_1_0.html <h1>→<h3> “Life before, during and after the Second World War”; ANZH303 ANZH303_4_0.html <h1>→<h3> “Innovation, Interactions and Mana.” |
| `body:panel:free` | `ABSENT-inWT` | 52 | 20 | 18 | CEDK101 CEDK101_0_0.html <h2>→<—> “Light and technology”; CEDO202 CEDO202_0_0.html <h2>→<—> “Creating and sharing your dance”; CEDO204 CEDO204_0_0.html <h4>→<—> “Beaver dams and lodges” |
| `body:widget:tabs` | `ABSENT-inWT` | 45 | 20 | 15 | AGH1001 AGH1001_2_0.html <h5>→<—> “Mussel Farmer – Jake Bartram, Hauraki Gulf New Zea”; ENGS201 ENGS201_4_0.html <h5>→<—> “Write a what if scenario.”; ENGS201 ENGS201_4_0.html <h5>→<—> “Imagine you are a superhero!” |
| `body:widget:wordHighlighter` | `body:free` | 45 | 10 | 10 | ENFUN01 ENFUN01_0_0.html <h3>→<h5> “Why is knowing about author’s purpose important?”; ENFUN04 ENFUN04_0_0.html <h3>→<h5> “Homophones, homonyms and homographs”; ENFUN05 ENFUN05_0_0.html <h3>→<h3> “Full stops, capital letters, exclamation marks” |
| `body:widget:tabs` | `body:widget:cv2-interactive` | 44 | 19 | 16 | ANZH203 ANZH203_6_0.html <h4>→<p> “Charles Heaphy: Artist, Draughtsman and Explorer”; ENGC301 ENGC301_1_0.html <h4>→<th> “Static advertisement”; ENGC301 ENGC301_7_0.html <h4>→<th> “Static advertisement” |
| `body:widget:carousel` | `body:widget:cv2-interactive` | 42 | 15 | 13 | BLL271 BLL271_1_0.html <h4>→<td> “pa / ki / hi / wi”; CEDO502 CEDO502_5_0.html <h5>→<p> “Use keywords carefully”; CEDO502 CEDO502_5_0.html <h5>→<p> “Use headings and subheadings” |
| `menu:Overview` | `ABSENT-notWT` | 40 | 36 | 35 | BLL253 BLL253_0_0.html <h4>→<—> “How will I know if I've learned it?”; BLL271 BLL271_0_0.html <h4>→<—> “How will I know I have learned it?”; BLL273 BLL273_0_0.html <h4>→<—> “How will I know if I've learned it?” |
| `body:panel:free` | `ABSENT-notWT` | 40 | 13 | 9 | CEDR101 CEDR101_0_0.html <h3>→<—> “TLearning from friends and whānau”; CEDR101 CEDR101_0_0.html <h3>→<—> “Who is leading the score?”; CEDR203 CEDR203_0_0.html <h2>→<—> “Aotearoa New Zealand Eco-leaders” |
| `body:widget:tabs` | `body:free` | 32 | 14 | 14 | AGH1001 AGH1001_2_0.html <h5>→<p> “Farm Advisor – Ash Phillips, Wairoa New Zealand”; ANZH203 ANZH203_6_0.html <h4>→<p> “Thomas Brunner: Surveyor and Explorer”; ENGC403 ENGC403_12_0.html <h4>→<h4> “Oral presentation part” |
| `body:widget:flipCard` | `ABSENT-notWT` | 32 | 17 | 17 | CHFUN05 CHFUN05_0_0.html <h5>→<—> “我不吃。wǒ bù chīI don’t eat.”; CHFUN05 CHFUN05_0_0.html <h5>→<—> “你不喜欢。nǐ bù xǐhuānYou don’t like it.”; CHFUN05 CHFUN05_0_0.html <h5>→<—> “然后ránhòuafterwards / after that” |
| `body:activity:side` | `ABSENT-notWT` | 32 | 12 | 4 | TEDC402 TEDC402_8_0.html <h5>→<—> “Spot the issue A”; TRR115 TRR115_2_0.html <h4>→<—> “A - re - wha - na”; XTAS102 XTAS102_1_0.html <h5>→<—> “Not fun. Too hard.” |
| `body:widget:accordion` | `body:activity` | 31 | 11 | 9 | ANZH303 ANZH303_2_0.html <h4>→<p> “Option 1: Questions to answer”; ANZH404 ANZH404_5_0.html <h4>→<p> “Example 1: Pakaitore/Moutoa gardens”; ANZH404 ANZH404_5_0.html <h4>→<p> “Example 2: The Foreshore and Seabed Act and hikoi” |
| `menu:flat` | `body:free` | 29 | 19 | 13 | BLL124 BLL124_0_0.html <h5>→<h4> “Whāinga Ako | Learning Intentions”; BLL124 BLL124_0_0.html <h5>→<h4> “Paearu Angitu | How will I know if I’ve learned it”; CBI1008 CBI1008_3_0.html <h5>→<h4> “We are learning about:” |
| `body:free:side` | `ABSENT-inWT` | 24 | 11 | 11 | ART1002 ART1002_0_0.html <h5>→<—> “Wrecking the White Page”; ART1002 ART1002_0_0.html <h5>→<—> “The Visual Arts Diary”; DTC1005 DTC1005_1_0.html <h3>→<—> “Digital Outcome Domain of your choice” |
| `body:widget:carousel` | `body:free` | 22 | 11 | 11 | ANZH105 ANZH105_6_0.html <h4>→<h4> “Cook Island Māori drumming and dancing”; DAN1006 DAN1006_6_0.html <h4>→<h4> “Whole dance with cues”; DAN1006 DAN1006_6_0.html <h4>→<h4> “Whole dance facing the front with music” |
| `body:widget:accordion` | `body:widget:carousel` | 21 | 6 | 6 | AGH1005 AGH1005_7_0.html <h5>→<li> “Powdery mildew (various species):”; AGH1005 AGH1005_7_0.html <h5>→<li> “Rust diseases (various species):”; AGH1005 AGH1005_7_0.html <h5>→<li> “Tomato yellow leaf curl virus (TYLCV):” |
| `body:free` | `body:widget:carousel` | 21 | 14 | 14 | ANZH205 ANZH205_7_0.html <h3>→<h4> “What can we do to honour te titiri?”; ARFUN02 ARFUN02_0_0.html <h4>→<h4> “How to understand it:”; ENFUN03 ENFUN03_0_0.html <h3>→<h4> “Adverb sentence starters” |
| `body:widget:tabs` | `ABSENT-notWT` | 21 | 12 | 11 | ART1006 ART1006_1_0.html <h5>→<—> “(this is where others can input into your idea)”; ENG1005 ENG1005_0_0.html <h5>→<—> “Demonstrate perceptive understanding of studied te”; HES1002 HES1002_7_0.html <h4>→<—> “Va, Va'a or Vaha” |
| `body:widget:flipCard` | `body:free` | 21 | 8 | 8 | BLLR202 BLLR202_4_0.html <h5>→<td> “Read between the lines”; CHFUN05 CHFUN05_0_0.html <h5>→<td> “我吃。wǒ chī.I eat.”; CHFUN05 CHFUN05_0_0.html <h5>→<td> “他去。tā qù.He is going.” |
| `body:activity` | `body:widget:flipCard` | 21 | 4 | 2 | ENGI102 ENGI102_2_0.html <h4>→<p> “Dress-up or Puppet Play”; ENGI102 ENGI102_2_0.html <h4>→<p> “Make a picture of a scene in the story”; ENGI102 ENGI102_2_0.html <h4>→<p> “Create an important item from the fairytale out of” |
| `menu:LI` | `menu:Overview` | 21 | 9 | 9 | MXS1004 MXS1004_0_0.html <h5>→<h4> “Whāinga Ako | Learning Intentions”; MXS1004 MXS1004_0_0.html <h5>→<h4> “Paearu Angitu | How will I know if I’ve learned it”; PMT101 PMT101_0_0.html <h5>→<td> “Kei te ako au kia:” |
| `menu:LI` | `menu:Information` | 21 | 5 | 5 | TRR103 TRR103_0_0.html <h5>→<h5> “Whakamaheretia tō wā:”; TRR103 TRR103_0_0.html <h5>→<h5> “He aha tāku hei tīmata?”; TRR103 TRR103_0_0.html <h5>→<h5> “What do I need to get started?” |
| `body:panel:activity` | `body:panel:widget:cv2-interactive` | 20 | 10 | 10 | BLL120 BLL120_0_0.html <h3>→<p> “Where is the /k/ sound?”; BLL210 BLL210_0_0.html <h5>→<th> “Uses one of these things:”; CEDK102 CEDK102_0_0.html <h4>→<p> “How to change your MTK profile picture” |
| `body:panel:free` | `body:panel:activity` | 20 | 10 | 10 | BLL250 BLL250_0_0.html <h2>→<h3> “The 'augh' letter team”; CEDK101 CEDK101_0_0.html <h3>→<h3> “How does light travel?”; CEDK101 CEDK101_0_0.html <h3>→<h3> “Light reflection and refraction” |
| `body:widget:tabs` | `body:alert` | 20 | 3 | 2 | ENGC403 ENGC403_7_0.html <h5>→<h4> “Introduction, topic and point of view”; ENGC403 ENGC403_7_0.html <h5>→<p> “Structure and organisation”; ENGC403 ENGC403_7_0.html <h5>→<p> “Language and clarity” |
| `menu:Overview` | `OTHER-PAGE` | 19 | 19 | 6 | ENGJ201 ENGJ201_1_0.html <h3>→<—> “How will I know if I’ve learned it?”; ENGJ201 ENGJ201_2_0.html <h3>→<—> “How will I know if I’ve learned it?”; ENGJ201 ENGJ201_3_0.html <h3>→<—> “How will I know if I’ve learned it?” |

## 3. Region agreement — of the gold's blocks in region A that Claude has on the paired page, the share it keeps in A

| gold region | matched on page | kept in region | moved | agreement |
|---|---:|---:|---:|---:|
| `body:free` | 24035 | 20205 | 3830 | 0.841 |
| `body:activity` | 18252 | 12246 | 6006 | 0.671 |
| `menu:flat` | 7743 | 7352 | 391 | 0.950 |
| `body:widget:accordion` | 6282 | 3044 | 3238 | 0.485 |
| `body:widget:dragAndDrop` | 4027 | 423 | 3604 | 0.105 |
| `acks` | 3947 | 3939 | 8 | 0.998 |
| `body:alert` | 3630 | 2243 | 1387 | 0.618 |
| `menu:Overview` | 3370 | 3257 | 113 | 0.966 |
| `body:panel:activity` | 3343 | 2127 | 1216 | 0.636 |
| `body:widget:multiChoiceQuiz` | 3291 | 120 | 3171 | 0.036 |
| `body:panel:free` | 3051 | 2610 | 441 | 0.855 |
| `body:widget:flipCard` | 2190 | 1212 | 978 | 0.553 |
| `menu:Information` | 2130 | 1478 | 652 | 0.694 |
| `body:widget:carousel` | 2128 | 1188 | 940 | 0.558 |
| `body:widget:tabs` | 2070 | 508 | 1562 | 0.245 |
| `body:widget:speechBubble` | 1364 | 960 | 404 | 0.704 |
| `header:other` | 1341 | 1272 | 69 | 0.949 |
| `body:widget:dropQuiz` | 882 | 125 | 757 | 0.142 |
| `body:panel:widget:accordion` | 829 | 371 | 458 | 0.448 |
| `body:widget:typing` | 716 | 111 | 605 | 0.155 |
| `body:widget:radioQuiz` | 715 | 0 | 715 | 0.000 |
| `body:widget:wordHighlighter` | 598 | 0 | 598 | 0.000 |
| `body:widget:reorder` | 591 | 0 | 591 | 0.000 |
| `body:alert:side` | 542 | 126 | 416 | 0.232 |
| `body:widget:hintSlider` | 479 | 188 | 291 | 0.392 |
| `menu:pane2` | 410 | 253 | 157 | 0.617 |
| `menu:LI` | 399 | 131 | 268 | 0.328 |
| `body:widget:dropDown` | 383 | 81 | 302 | 0.211 |
| `menu:Standards` | 361 | 331 | 30 | 0.917 |
| `menu:pane3` | 352 | 228 | 124 | 0.648 |
| `menu:Knowledge` | 334 | 310 | 24 | 0.928 |
| `body:free:side` | 240 | 39 | 201 | 0.163 |
| `body:panel:widget:dragAndDrop` | 230 | 51 | 179 | 0.222 |
| `body:panel:widget:flipCard` | 228 | 104 | 124 | 0.456 |
| `body:panel:widget:carousel` | 221 | 132 | 89 | 0.597 |
| `body:widget:selfCheck` | 197 | 5 | 192 | 0.025 |
| `menu:Practices` | 187 | 186 | 1 | 0.995 |
| `other:free` | 180 | 0 | 180 | 0.000 |
| `body:panel:widget:multiChoiceQuiz` | 172 | 29 | 143 | 0.169 |
| `body:panel:alert` | 165 | 105 | 60 | 0.636 |

## 5. ORDER — blocks Claude places in a different order than the human (same page; session 42 Round 11)

Every gold block matched on the paired page, in gold order, carries its Claude position; the blocks outside the longest increasing subsequence of those positions are the ones in a different ORDER (a whole section moved, an introduction after a note, a lead after its list). Regions first, then the recurring blocks by modules (a text that moves in many modules is a systematic placement rule; `before` = the gold block it should precede).

| gold region | matched | out of order | share | pages | modules |
|---|---:|---:|---:|---:|---:|
| `body:free` | 24035 | 863 | 0.036 | 372 | 213 |
| `body:activity` | 18252 | 809 | 0.044 | 338 | 184 |
| `menu:flat` | 7743 | 93 | 0.012 | 56 | 43 |
| `body:widget:accordion` | 6282 | 196 | 0.031 | 62 | 50 |
| `body:widget:dragAndDrop` | 4027 | 725 | 0.180 | 202 | 146 |
| `acks` | 3947 | 156 | 0.040 | 66 | 66 |
| `body:alert` | 3630 | 186 | 0.051 | 119 | 78 |
| `menu:Overview` | 3370 | 115 | 0.034 | 31 | 31 |
| `body:panel:activity` | 3343 | 247 | 0.074 | 38 | 38 |
| `body:widget:multiChoiceQuiz` | 3291 | 244 | 0.074 | 64 | 47 |
| `body:panel:free` | 3051 | 133 | 0.044 | 29 | 26 |
| `body:widget:flipCard` | 2190 | 79 | 0.036 | 31 | 28 |
| `menu:Information` | 2130 | 71 | 0.033 | 19 | 19 |
| `body:widget:carousel` | 2128 | 85 | 0.040 | 36 | 33 |
| `body:widget:tabs` | 2070 | 113 | 0.055 | 55 | 45 |
| `body:widget:speechBubble` | 1364 | 59 | 0.043 | 34 | 29 |
| `header:other` | 1341 | 43 | 0.032 | 41 | 35 |
| `body:widget:dropQuiz` | 882 | 48 | 0.054 | 25 | 22 |
| `body:panel:widget:accordion` | 829 | 55 | 0.066 | 10 | 10 |
| `body:widget:typing` | 716 | 27 | 0.038 | 14 | 12 |
| `body:widget:radioQuiz` | 715 | 14 | 0.020 | 9 | 9 |
| `body:widget:wordHighlighter` | 598 | 23 | 0.038 | 14 | 11 |
| `body:widget:reorder` | 591 | 131 | 0.222 | 32 | 23 |
| `body:alert:side` | 542 | 128 | 0.236 | 74 | 48 |
| `body:widget:hintSlider` | 479 | 25 | 0.052 | 3 | 2 |
| `menu:pane2` | 410 | 27 | 0.066 | 7 | 7 |
| `menu:LI` | 399 | 45 | 0.113 | 9 | 9 |
| `body:widget:dropDown` | 383 | 45 | 0.117 | 13 | 12 |
| `menu:Standards` | 361 | 7 | 0.019 | 5 | 5 |
| `menu:pane3` | 352 | 31 | 0.088 | 11 | 11 |

| block (tag: first words) | modules | pages | families | example: gold places it before … |
|---|---:|---:|---|---|
| `h4:go to your journal` | 42 | 82 | XGF 21, CEDK 20, CEDR 16, HES 16 | ANZH301 ANZH301_1_0.html: “Go to your journal” before “Māori involvement in the war effort also had anoth” |
| `li:decoding an unknown word with` | 15 | 15 | BLL 15 | BLL240 BLL240_0_0.html: “Decoding an unknown word (with one syllable) involves:” before “Identifying and recording phonemes in words includ” |
| `h3:he aha tāku i ako` | 7 | 11 | TRR 12, PMT 2, PNR 1 | PMT101 PMT101_3_0.html: “He aha tāku i ako ai?” before “Tohua ngā mea kua akona e koe mō te orangatonutang” |
| `li:identifying and recording phonemes in` | 6 | 6 | BLL 6 | BLL271 BLL271_0_0.html: “Identifying and recording phonemes in words, including:” before “Decoding words with less common graphemes or graph” |
| `h5:hei te mutunga o te` | 5 | 5 | TRR 5 | TRR102 TRR102_0_0.html: “Hei te mutunga o te tau:” before “By the end of the year:” |
| `p:āta whakarongo ki ēnei kupu` | 4 | 6 | TRR 6 | TRR109 TRR109_1_0.html: “Āta whakarongo ki ēnei kupu. Ko ēhea kupu he oropuare pūrua ” before “Listen carefully to these kupu. Which words have t” |
| `p:take a photo of your` | 4 | 4 | BLL 5, ENGR 1, MXFL 1 | BLL110 BLL110_0_0.html: “Take a photo of your handwriting and upload it to show your ” before “Choose one or more of these activities to do. Clic” |
| `p:find things in your home` | 4 | 4 | BLL 13 | BLL110 BLL110_0_0.html: “Find things in your home or in your neighbourhood that have ” before “Draw some things that start with /t/ sound.” |
| `h4:what have i learned` | 4 | 4 | TRR 6, CEDT 1 | CEDT104 CEDT104_0_0.html: “What have I learned?” before “I know the words and signs for five body parts.” |
| `p:we are learning to` | 4 | 4 | ENFUN 4 | ENFUN01 ENFUN01_0_0.html: “We are learning to:” before “You will show your understanding by:” |
| `p:watch this video to learn` | 4 | 4 | MXFUN 4, MXDI 1, MXFU 1, XDLS 1 | MXDI103 MXDI103_3_0.html: “Watch this video to learn more about place value houses:” before “7 is a digit, but 12 is not as 12 has two digits i” |
| `p:whakarongo pīkarikari ki ēnei kupu` | 4 | 4 | TRR 4 | TRR110 TRR110_1_0.html: “Whakarongo pīkarikari ki ēnei kupu. Kātahi ka whakatau mēna ” before “Listen carefully to these words and decide if they” |
| `p:below are activities you can` | 3 | 19 | XDLS 19 | XDLS904 XDLS904_1_0.html: “Below are activities. You can choose the activities you feel” before “In this activity, you and your whānau will learn b” |
| `p:in this lesson you are` | 3 | 9 | ANZH 8, HIS 1 | ANZH401 ANZH401_6_0.html: “In this lesson you are learning to understand that data from” before “Conclusions about Early Migrants” |
| `p:email or phone the kaiako` | 3 | 8 | SSOG 5, XLP 2, XMES 1 | SSOG105 SSOG105_1_0.html: “Email or phone the kaiako. You can ring 0800 65 99 88 and as” before “Ka pai, detectives! Now I understand – some days a” |
| `h3:rapua ngā kupu e huarite` | 3 | 6 | TRR 6 | TRR109 TRR109_1_0.html: “Rapua ngā kupu e huarite ana” before “Find the rhyming words” |
| `h3:rapua te kupu tika` | 3 | 5 | TRR 5 | TRR109 TRR109_2_0.html: “Rapua te kupu tika” before “Find the correct word” |
| `p:it may take more or` | 3 | 3 | ANZH 1, SPA 1, TWHK 1 | ANZH301 ANZH301_0_0.html: “It may take more or less time, depending on what you know an” before “read, view and listen to multiple narratives about” |
| `li:what is the main idea` | 3 | 3 | HIS 3, ANZH 1 | ANZH304 ANZH304_1_0.html: “What is the main idea that this map shows you about missiona” before “Map 2 shows me that the church with the largest zo” |
| `p:watch the following videos` | 3 | 3 | BLL 17 | BLL110 BLL110_0_0.html: “Watch the following videos:” before “My name is, my sound is…” |
| `p:if your ākonga is having` | 3 | 3 | BLL 13 | BLL110 BLL110_0_0.html: “If your ākonga is having difficulty remembering both the nam” before “My name is, my sound is…” |
| `p:when a letter is written` | 3 | 3 | BLL 4 | BLL110 BLL110_0_0.html: “When a letter is written as ‘i’ we want you to say its name.” before “Find the letter i” |
| `p:draw some things that start` | 3 | 3 | BLL 7 | BLL120 BLL120_0_0.html: “Draw some things that start with /k/.” before “Watch the video and complete one or more of the cr” |
| `p:watch these videos to learn` | 3 | 3 | BLL 4 | BLL140 BLL140_0_0.html: “Watch these videos to learn more about short and long vowels” before “If a letter is written as /a/ it means we want you” |
| `p:lets re read the book` | 3 | 3 | BLL 3 | BLL154 BLL154_1_0.html: “Let’s re-read the book from the last module, Sant sings a so” before “These are some sentences from the book ‘Sant sings” |
| `p:when you have finished writing` | 3 | 3 | BLL 3 | BLL216 BLL216_2_0.html: “When you have finished writing the sentences, read the sente” before “Remember to start your sentence with a capital let” |
| `p:once you have finished writing` | 3 | 3 | BLL 3 | BLL224 BLL224_1_0.html: “Once you have finished writing all six sentences read them b” before “Remember to use the correct punctuation to end you” |
| `h3:what have i learned` | 3 | 3 | CEDT 2, PMT 2, TRR 1 | CEDT104 CEDT104_0_0.html: “What have I learned?” before “Tick the boxes you have tried:” |
| `h3:check your understanding` | 3 | 3 | CHFUN 39 | CHFUN05 CHFUN05_0_0.html: “Check your understanding” before “Identify S, V, O. Select words that belong to thes” |
| `li:achievement with excellence` | 3 | 3 | ENG 3 | ENG1004 ENG1004_0_0.html: “Achievement with Excellence” before “Context and presentation mode selection” |
| `p:think like a scientist` | 3 | 3 | TWHA 3, EXPFUN 1 | EXPFUN02 EXPFUN02_0_0.html: “Think like a Scientist” before “Learning goals and learning intentions” |
| `p:think like a social scientist` | 3 | 3 | TWHA 2, EXPFUN 1 | EXPFUN02 EXPFUN02_0_0.html: “Think like a Social Scientist” before “Learning goals and learning intentions” |
| `p:think like a mathematician` | 3 | 3 | TWHA 3, EXPFUN 1 | EXPFUN02 EXPFUN02_0_0.html: “Think like a Mathematician” before “Learning goals and learning intentions” |
| `p:think like an innovator` | 3 | 3 | TWHA 3, EXPFUN 1 | EXPFUN02 EXPFUN02_0_0.html: “Think like an Innovator” before “Learning goals and learning intentions” |
| `h4:how will i know i` | 3 | 3 | TEDC 2, FRNO 1 | FRNO901 FRNO901_0_0.html: “How will I know I have learned it?” before “Bonjour et Bienvenue Your French journey begins he” |
| `p:photo fun cat 3d illustration` | 3 | 3 | OSGM 5 | OSGM301 OSGM301_0_0.html: “Photo: Fun cat - 3D Illustration stock photo, iStock 9733426” before “Photo: Under 18 years prohibition sign. adults onl” |
| `p:charge it properly plug it` | 3 | 3 | OSOH 3 | OSOH201 OSOH201_2_0.html: “Charge it properly – plug it in before the battery runs out ” before “Eat or drink near your device – spills can cause s” |
| `p:use a case or bag` | 3 | 3 | OSOH 3 | OSOH201 OSOH201_2_0.html: “Use a case or bag – protect it when carrying it around.” before “Eat or drink near your device – spills can cause s” |
| `p:keep it safe store it` | 3 | 3 | OSOH 3 | OSOH201 OSOH201_2_0.html: “Keep it safe – store it in a dry, cool place away from water” before “Eat or drink near your device – spills can cause s” |
| `p:ask for help if something` | 3 | 3 | OSOH 3 | OSOH201 OSOH201_2_0.html: “Ask for help – if something doesn’t look right or stops work” before “Eat or drink near your device – spills can cause s” |
| `p:mokopuna should be able to` | 3 | 3 | TRR 3 | TRR103 TRR103_0_0.html: “Mokopuna should be able to distinguish between different sou” before “Nau mai ki tēnei akoranga mō te oropuare E.” |
| `p:me mōhio ngā mokopuna ki` | 3 | 3 | TRR 3 | TRR103 TRR103_0_0.html: “me mōhio ngā mokopuna ki te tūhono i te oromotu ki te orotuh” before “Nau mai ki tēnei akoranga mō te oropuare E.” |
| `p:mokopuna need to be able` | 3 | 3 | TRR 3 | TRR103 TRR103_0_0.html: “Mokopuna need to be able to correctly match sounds (phonemes” before “Nau mai ki tēnei akoranga mō te oropuare E.” |
| `li:whakamahi i ngā kāri whakamahara` | 3 | 3 | TRR 3 | TRR107 TRR107_0_0.html: “whakamahi i ngā kāri whakamahara me ngā kēmu pāhekoheko hei ” before “identify individual orokati through sound and symb” |
| `p:hei te mutunga o te` | 3 | 3 | TRR 3 | TRR108 TRR108_0_0.html: “Hei te mutunga o te tau: Ka āhei te tamaiti ki te rongo i ng” before “By the end of the year: The child will be able to ” |
| `p:kaua e wareware ki te` | 3 | 3 | TRR 3 | TRR109 TRR109_2_0.html: “Kaua e wareware ki te kapo whakaahua, ā, tukuna atu āu mahi ” before “Don't forget to take photos and share your mahi wi” |
| `li:explain how language features help` | 3 | 3 | WJFUN 5 | WJFUN115 WJFUN115_0_0.html: “explain how language features help readers hear sounds, crea” before “how writers choose words that help readers create ” |
| `p:the learning in this lesson` | 2 | 3 | HIS 3 | HIS1003 HIS1003_3_0.html: “The learning in this lesson links to the previous lesson and” before “When processing information from different sources” |
| `h3:ngā tohutohu hei mahi` | 2 | 3 | TRR 3 | TRR102 TRR102_4_0.html: “Ngā tohutohu hei mahi” before “The kiwi group's learning guide” |
| `h5:what do i need to` | 2 | 2 | AGH 1, ANZH 1 | AGH1001 AGH1001_0_0.html: “What do I need to get started?” before “How will I know if I’ve learned it?” |

| gold region · tag | out-of-order blocks | modules |
|---|---:|---:|
| `body:widget:dragAndDrop` · p | 718 | 146 |
| `body:free` · p | 497 | 173 |
| `body:activity` · p | 399 | 126 |
| `body:widget:multiChoiceQuiz` · p | 224 | 44 |
| `body:activity` · h3 | 159 | 58 |
| `acks` · p | 156 | 66 |
| `body:alert` · p | 140 | 69 |
| `body:panel:activity` · p | 140 | 29 |
| `body:widget:reorder` · p | 129 | 22 |
| `body:activity` · li | 121 | 42 |
| `body:activity` · h4 | 120 | 34 |
| `body:free` · h3 | 105 | 54 |
| `body:free` · li | 96 | 23 |
| `menu:Overview` · li | 89 | 18 |
| `body:alert:side` · p | 88 | 45 |
| `body:widget:accordion` · p | 85 | 28 |
| `menu:flat` · li | 82 | 36 |
| `body:widget:accordion` · li | 70 | 19 |
| `body:panel:free` · p | 69 | 22 |
| `body:panel:activity` · h4 | 62 | 15 |
| `body:widget:tabs` · li | 58 | 33 |
| `body:widget:carousel` · p | 58 | 26 |
| `body:free` · h4 | 58 | 25 |
| `body:free` · h2 | 57 | 29 |
| `body:widget:speechBubble` · p | 55 | 27 |

## 4. Examples for the 25 largest transitions

### `acks` → `ABSENT-notWT` — 16716 blocks / 514 pages / 485 modules
families: BLL 2501, MXFL 1202, XDLS 654, ANZH 585, TRR 529, ENGS 452, XGF 439, HPFUN 434
- AGH1001 `AGH1001_5_0.html` <p>→<—> “Every effort has been made to acknowledge and contact copyright holders. Te Aho o Te Kura ”
- AGH1002 `AGH1002_6_0.html` <p>→<—> “Every effort has been made to acknowledge and contact copyright holders. Te Aho o Te Kura ”
- AGH1003 `AGH1003_8_0.html` <p>→<—> “Every effort has been made to acknowledge and contact copyright holders. Te Aho o Te Kura ”
- AGH1005 `AGH1005_8_0.html` <p>→<—> “Every effort has been made to acknowledge and contact copyright holders. Te Aho o Te Kura ”
- AGH1007 `AGH1007_9_0.html` <p>→<—> “Every effort has been made to acknowledge and contact copyright holders. Te Aho o Te Kura ”
- AGH1007 `AGH1007_9_0.html` <p>→<—> “Video: Delicious Starts Here - Farmer Story, Silver Fern Farms, https://www.youtube.com/wa”

### `body:activity` → `ABSENT-notWT` — 4352 blocks / 1131 pages / 380 modules
families: TRR 556, XDLS 338, HIS 224, AGH 202, ART 195, BLL 186, MXFL 136, ENGI 126
- AGH1001 `AGH1001_1_0.html` <h3>→<—> “What are primary products?”
- AGH1002 `AGH1002_2_0.html` <h3>→<—> “Soil practical – Texture by sedimentation”
- AGH1003 `AGH1003_2_0.html` <h3>→<—> “Soil properties review”
- AGH1004 `AGH1004_1_0.html` <p>→<—> “Drag and drop the correct factor to the correct classification.”
- AGH1005 `AGH1005_1_0.html` <h3>→<—> “Māori and Western views on plants and their purpose”
- AGH1005 `AGH1005_1_0.html` <p>→<—> “Let’s review the viticulture practices video in the South Island and make a critical judge”

### `body:free` → `ABSENT-notWT` — 3993 blocks / 945 pages / 358 modules
families: HIS 280, TRR 233, XGF 213, MXFL 186, MXFU 179, AGH 172, XDLS 169, MXDI 153
- AGH1001 `AGH1001_0_0.html` <p>→<—> “This module will cover:”
- AGH1002 `AGH1002_6_0.html` <p>→<—> “Biological properties include:”
- AGH1003 `AGH1003_1_0.html` <li>→<—> “Increase the rate of pasture and crop growth.”
- AGH1004 `AGH1004_2_0.html` <th>→<—> “Stocking rate (number of sheep per hectare)”
- AGH1005 `AGH1005_1_0.html` <p>→<—> “The mauri model decision making framework was created by Dr Kepa Morgan. It has been desig”
- AGH1005 `AGH1005_2_0.html` <p>→<—> “Plant anatomy focuses on the structure and organisation of plant parts (cells and tissues)”

### `acks` → `OTHER-PAGE` — 3488 blocks / 254 pages / 240 modules
families: MXFL 852, BLL 518, XTAS 340, XDLS 296, XLP 160, OSAI 137, XMES 102, AGH 101
- AGH1001 `AGH1001_5_0.html` <p>→<—> “Photo: Roast beef on cutting board with salt and pepper. Top view, iStock 645249428, Getty”
- AGH1002 `AGH1002_6_0.html` <p>→<—> “Photo: Yellow gorse flowers on a bush, iStock 685756664, Getty Images. Used with permissio”
- AGH1003 `AGH1003_8_0.html` <p>→<—> “Photo: Kiwifruit industry in New Zealand, iStock 1401383311, Getty Images. Used with permi”
- AGH1005 `AGH1005_8_0.html` <p>→<—> “Photo: Tractor spraying young corn with pesticides, iStock 1224290959, Getty Images. Used ”
- AGH1008 `AGH1008_8_0.html` <p>→<—> “Photo: Oral Drench, PGG Wrightsons, https://store.pggwrightson.co.nz/animal-health/sheep-o”
- AGH1008 `AGH1008_8_0.html` <p>→<—> “Photo: Pour on Drench, PGG Wrightsons, https://store.pggwrightson.co.nz/animal-health/catt”

### `body:widget:dragAndDrop` → `body:widget:cv2-interactive` — 3168 blocks / 430 pages / 261 modules
families: BLL 264, WJFUN 209, ENGI 178, MXFL 154, XGF 148, ENGC 138, MXFU 115, OSBY 110
- AGH1001 `AGH1001_1_0.html` <p>→<th> “Agricultural Production”
- AGH1003 `AGH1003_2_0.html` <p>→<td> “Small sheep and beef farm”
- AGH1004 `AGH1004_2_0.html` <p>→<th> “Mountains and high country”
- AGH1005 `AGH1005_1_0.html` <p>→<li> “Plants are important for food, feeding stock and industrial uses.”
- AGH1007 `AGH1007_5_0.html` <p>→<td> “Ewe pregnant with singles”
- AGH1007 `AGH1007_5_0.html` <p>→<li> “Ewe lamb being finished”

### `body:activity` → `body:free` — 2870 blocks / 614 pages / 322 modules
families: TRR 556, XGF 262, BLL 149, XDLS 135, TEDC 130, PMT 121, HIS 113, WJFUN 62
- AGH1001 `AGH1001_3_0.html` <h3>→<h3> “Self Check: True or False”
- AGH1002 `AGH1002_3_0.html` <p>→<p> “Go to your learning journal and complete activity 3A.”
- AGH1003 `AGH1003_2_0.html` <p>→<p> “Revisit this list from earlier in the lesson. Select the soil properties which are altered”
- AGH1004 `AGH1004_1_0.html` <h3>→<h3> “Knowledge self-check”
- AGH1005 `AGH1005_6_0.html` <h3>→<h3> “Knowledge self-check”
- AGH1005 `AGH1005_6_0.html` <p>→<p> “Which of these statements is true or false?”

### `body:activity` → `body:widget:cv2-interactive` — 2624 blocks / 699 pages / 334 modules
families: BLL 240, TRR 225, WJFUN 145, XMES 144, FRNO 121, HIS 106, MXDB 102, MXFL 88
- AGH1001 `AGH1001_1_0.html` <p>→<p> “Select the primary products below which you think are produced in New Zealand or Pacific I”
- AGH1002 `AGH1002_5_0.html` <p>→<p> “Match the chemical symbol with the nutrient.”
- AGH1003 `AGH1003_2_0.html` <p>→<p> “For each production type, identify the irrigation system which would be best suited.”
- AGH1004 `AGH1004_3_0.html` <p>→<p> “From the list, select the region that has the best average of GDD days for each year.”
- AGH1005 `AGH1005_1_0.html` <p>→<p> “Order the following phrases into similarities and differences.”
- AGH1005 `AGH1005_6_0.html` <p>→<p> “Getting the correct amount of nutrients in the soil is a balancing act for many growers. H”

### `body:widget:multiChoiceQuiz` → `body:widget:cv2-interactive` — 2348 blocks / 229 pages / 150 modules
families: XGF 359, BLL 185, WJFUN 165, CEDO 128, MXFU 117, MXFL 115, ENGR 101, PWY 81
- AGH1003 `AGH1003_2_0.html` <p>→<td> “Water-holding capacity”
- ANZH104 `ANZH104_7_0.html` <p>→<li> “My journal is complete”
- ANZH105 `ANZH105_8_0.html` <p>→<li> “My journal is complete.”
- ANZH203 `ANZH203_1_0.html` <p>→<li> “What nationality was Abel Tasman”
- ARFUN03 `ARFUN03_0_0.html` <p>→<p> “The dancer’s focus is the audience.”
- ARFUN03 `ARFUN03_0_0.html` <p>→<p> “The dancer's focus is his foot.”

### `body:activity` → `ABSENT-inWT` — 2342 blocks / 728 pages / 324 modules
families: TEDC 221, ENGS 138, PWY 137, BLL 117, WJFUN 91, XDLS 85, TRR 83, XMES 81
- AGH1001 `AGH1001_2_0.html` <p>→<—> “Complete activity 2B in your learning journal.”
- AGH1002 `AGH1002_6_0.html` <h3>→<—> “Levels of organic matter”
- AGH1003 `AGH1003_3_0.html` <h3>→<—> “Fertiliser application”
- AGH1004 `AGH1004_2_0.html` <h4>→<—> “New Zealand Topographical Map”
- AGH1005 `AGH1005_8_0.html` <h3>→<—> “How plants flower and produce fruit”
- AGH1008 `AGH1008_1_0.html` <h3>→<—> “Manaakitanga in practice”

### `body:free` → `ABSENT-inWT` — 2336 blocks / 653 pages / 293 modules
families: OSOH 110, ENGJ 104, TEDC 104, PWY 103, XDLS 94, AGH 93, CHFUN 92, WJFUN 86
- AGH1001 `AGH1001_0_0.html` <h3>→<—> “An introduction to agricultural and horticultural science in Aotearoa New Zealand | He wha”
- AGH1002 `AGH1002_1_0.html` <p>→<—> “As soil gets older, more horizons form. Click on the horizons below to find out more about”
- AGH1003 `AGH1003_0_0.html` <p>→<—> “This module explores the ways farmers and growers do this on various production systems wh”
- AGH1005 `AGH1005_0_0.html` <p>→<—> “It’s important that you fully understand these processes and that they do not occur in iso”
- AGH1006 `AGH1006_2_0.html` <p>→<—> “Commercial crop production uses three main ways to propagate new plants; sowing seeds, cut”
- AGH1006 `AGH1006_3_0.html` <p>→<—> “Cultivation is especially important in intensive horticulture-like commercial market garde”

### `body:free` → `body:widget:cv2-interactive` — 1718 blocks / 367 pages / 211 modules
families: XDLS 117, OSAH 80, ENGI 78, OSAI 71, MXFL 70, SSCI 67, OSSM 63, AGH 56
- AGH1001 `AGH1001_2_0.html` <p>→<p> “Below is a brief timeline of the events that have shaped Aotearoa into where we stand toda”
- AGH1002 `AGH1002_3_0.html` <h4>→<th> “Air level in soil”
- AGH1003 `AGH1003_2_0.html` <p>→<p> “While the irrigation system used mainly depends on the size of the production, a range of ”
- AGH1004 `AGH1004_6_0.html` <p>→<p> “As you can see, this process is highly dependent on the ability to store and keep milk bel”
- AGH1005 `AGH1005_1_0.html` <p>→<p> “What differences do you notice between each model of growing plants?”
- AGH1005 `AGH1005_1_0.html` <p>→<p> “As you can see, both models support the use of plants for the purpose of keeping people an”

### `body:widget:accordion` → `ABSENT-notWT` — 1693 blocks / 179 pages / 113 modules
families: MXFL 353, HIS 192, XDLS 109, XGF 78, TRR 74, MXFU 70, ENGC 60, XLP 60
- AGH1003 `AGH1003_4_0.html` <p>→<—> “Compost is made from all sorts of organic materials including old plant material and anima”
- AGH1006 `AGH1006_3_0.html` <h4>→<—> “Power-driven methods”
- AGH1008 `AGH1008_3_0.html` <p>→<—> “Examples: plantain, turnips.”
- ANZH205 `ANZH205_7_0.html` <p>→<—> “Contact your Te kura kaiako about other available Te reo Māori courses.”
- ANZH302 `ANZH302_2_0.html` <h4>→<—> “Source 1 – Kesi Ramji’s Mother”
- ANZH302 `ANZH302_2_0.html` <p>→<—> “Our family home was filled with people, love, laughter and lots of delicious food. We had ”

### `menu:flat` → `ABSENT-notWT` — 1501 blocks / 472 pages / 192 modules
families: ANZH 251, BLL 247, XOTPB 91, ENGS 83, TWHA 72, ENGR 67, MXEX 47, ENFUN 45
- AGH1004 `AGH1004_1_0.html` <li>→<—> “We are learning about factors that impact where primary products are grown.”
- AGH1007 `AGH1007_3_0.html` <li>→<—> “demonstrating the differences between monogastric and ruminant digestive systems in animal”
- ANZH101 `ANZH101_0_0.html` <p>→<—> “As you work through this module, keep in mind that there are different versions of stories”
- ANZH103 `ANZH103_0_0.html` <p>→<—> “Colonisation and settlement have been central to Aotearoa New Zealand’s histories for the ”
- ANZH302 `ANZH302_0_0.html` <p>→<—> “I am beginning to understand that:”
- ANZH302 `ANZH302_0_0.html` <li>→<—> “people hold different perspectives on the world depending on their values, traditions, and”

### `menu:flat` → `OTHER-PAGE` — 1466 blocks / 259 pages / 69 modules
families: HPRE 342, ANZH 290, ENGI 245, SSOG 211, ENGC 44, PWY 44, XWHA 35, ENGJ 22
- AGH1009 `AGH1009_8_0.html` <li>→<—> “identify and describe the impact historic primary production practices have had on the soi”
- ANZH103 `ANZH103_1_0.html` <li>→<—> “recognise the importance of the Treaty of Waitangi”
- ANZH203 `ANZH203_1_0.html` <h4>→<—> “How will I know if I’ve learned it?”
- ANZH302 `ANZH302_1_0.html` <li>→<—> “construct a narrative of cause and effect for one cultural community in Aotearoa New Zeala”
- ANZH401 `ANZH401_1_0.html` <p>→<—> “I am beginning to understand that ...”
- ANZH401 `ANZH401_1_0.html` <li>→<—> “Colonisation and settlement have been central to Aotearoa New Zealand’s Histories for the ”

### `body:widget:accordion` → `body:widget:cv2-interactive` — 1291 blocks / 163 pages / 114 modules
families: BLL 145, XDLS 84, XGF 77, HPRE 55, ENGJ 52, WJFUN 50, PWY 45, OSSC 40
- AGH1009 `AGH1009_1_0.html` <p>→<th> “The Treaty of Waitangi is about partnership between the Crown and Māori. This partnership ”
- ANZH203 `ANZH203_3_0.html` <h4>→<p> “Tupaia and the Endeavour”
- ANZH304 `ANZH304_1_0.html` <p>→<p> “Felton Mathew, living in Sydney, accepted an offer to come to New Zealand with Hobson as t”
- BLL112 `BLL112_2_0.html` <li>→<li> “Why do you think the tap might be running?”
- BLL122 `BLL122_2_0.html` <li>→<li> “Kim and Mick were looking for things at the tip. What do you think they were looking for? ”
- BLL122 `BLL122_2_0.html` <li>→<li> “What do you think the ants were doing in the tin?”

### `acks` → `ABSENT-inWT` — 1249 blocks / 252 pages / 238 modules
families: BLL 242, ANZH 106, PWY 74, MXFL 69, CEDO 57, HIS 50, ENGS 49, MXDI 41
- AGH1001 `AGH1001_5_0.html` <p>→<—> “Photo: Colm & Gaynor Tierney, RNZ/Carol Stiles, https://www.rnz.co.nz/national/programmes/”
- AGH1005 `AGH1005_8_0.html` <p>→<—> “Photo: Abstract Weather Concept - Sun In Serene Sky With Flare Effect, iStock 1300645794, ”
- AGH1007 `AGH1007_9_0.html` <p>→<—> “Illustration: Pigs mouth, https://quizlet.com/365126001/exercise-science-fetal-pig-1-exter”
- AGH1009 `AGH1009_9_0.html` <p>→<—> “Photo: Farmer hold a smartphone on a background of a field with a pepper plantations. Agri”
- ANZH101 `ANZH101_3_0.html` <p>→<—> “Image: New shoot of fern frond on New Zealand tree fern, iStock 1703245930, Getty Images. ”
- ANZH101 `ANZH101_3_0.html` <p>→<—> “Google Slides: e Waka o Aoraki,Connected – Ministry of Education https://docs.google.com/p”

### `body:widget:accordion` → `ABSENT-inWT` — 1193 blocks / 208 pages / 128 modules
families: XMES 116, TEDC 111, CHFUN 109, AGH 63, XGF 59, BLL 58, PWY 52, ENGJ 46
- AGH1003 `AGH1003_4_0.html` <h4>→<—> “Slurry Tankers/Umbilical Systems”
- AGH1005 `AGH1005_2_0.html` <h4>→<—> “Disease and pest resistance”
- AGH1006 `AGH1006_1_0.html` <h4>→<—> “Integrated pest management (IPM)”
- AGH1008 `AGH1008_3_0.html` <li>→<—> “high dry matter (average 85 percent DM)”
- AGH1009 `AGH1009_1_0.html` <h5>→<—> “Partnership (Partnership principle)”
- AGH1009 `AGH1009_1_0.html` <h4>→<—> “Cultural recognition”

### `body:widget:accordion` → `body:free` — 1155 blocks / 140 pages / 80 modules
families: XGF 177, ENGFUN 89, MXFL 86, TEFUN 64, XDLS 57, ENGJ 48, AGH 46, PES 41
- AGH1003 `AGH1003_4_0.html` <p>→<td> “Effluent spreaders are similar to irrigation systems but are designed to spread effluent r”
- AGH1004 `AGH1004_2_0.html` <p>→<p> “Intensive farming is farming where high numbers of animals or crop plants are grown in a s”
- AGH1006 `AGH1006_5_0.html` <p>→<p> “Pruning is the removal of branches or roots from a plant. This is done to change the plant”
- AGH1008 `AGH1008_3_0.html` <p>→<td> “Tough fibrous feed which is usually fed as a supplementary feed during the winter months a”
- ANZH101 `ANZH101_2_0.html` <h4>→<h4> “Ranginui and Papatūānuku”
- ANZH101 `ANZH101_2_0.html` <h4>→<h4> “Te Ika a Maui”

### `body:free` → `body:activity` — 1053 blocks / 295 pages / 157 modules
families: TRR 226, HIS 80, MXFL 69, AGH 62, MXDI 60, XDLS 56, MXFU 46, ANZH 43
- AGH1001 `AGH1001_4_0.html` <p>→<p> “Traditional Māori horticultural practices were guided by maramataka or the lunar calendar.”
- AGH1002 `AGH1002_3_0.html` <p>→<p> “Plants don’t breathe like humans do, but they do respire. Respiration is the process where”
- AGH1003 `AGH1003_1_0.html` <p>→<p> “Soil management practices are the focus of this module. They are the management practices ”
- AGH1004 `AGH1004_5_0.html` <p>→<p> “Here is a video of how water is used to feed crops and pasture:”
- AGH1005 `AGH1005_2_0.html` <p>→<p> “Fruit is formed from the ovary of a flower after fertilisation. Fruit contain seeds used f”
- AGH1005 `AGH1005_2_0.html` <p>→<p> “The main functions of fruits and seeds are to:”

### `body:alert` → `body:free` — 978 blocks / 300 pages / 164 modules
families: TRR 79, CEDO 74, ANZH 57, HIS 52, ENFUN 51, ENGC 48, MXFL 43, ENGS 39
- AGH1001 `AGH1001_5_0.html` <p>→<p> “A management practice is an activity or job done by a farmer or a grower to produce their ”
- AGH1002 `AGH1002_4_0.html` <p>→<p> “There are four physical properties of soil. Two of these relate to the water levels in soi”
- AGH1003 `AGH1003_2_0.html` <p>→<p> “This is why earthworms come to the surface after heavy rain – to escape from the water tha”
- AGH1005 `AGH1005_3_0.html` <li>→<li> “Plants are producers. This means they make their own food.”
- AGH1009 `AGH1009_4_0.html` <p>→<p> “It is important to remember as you work through this section that these are actions that w”
- AGH1009 `AGH1009_4_0.html` <h4>→<p> “A note on sprays”

### `body:widget:multiChoiceQuiz` → `ABSENT-inWT` — 942 blocks / 139 pages / 91 modules
families: PWY 179, TEDC 99, BLL 57, HPFUN 46, MXFL 40, CEDR 39, OSAI 39, MXFUN 34
- AGH1007 `AGH1007_6_0.html` <p>→<—> “What organ is responsible for producing the egg.”
- AGH1008 `AGH1008_4_0.html` <p>→<—> “Wool micron (fineness)”
- BLL114 `BLL114_1_0.html` <p>→<—> “Click on the letter ...”
- BLL146 `BLL146_2_0.html` <p>→<—> “The jeep skids and gets stuck.”
- BLL147 `BLL147_1_0.html` <p>→<—> “/ j / ee / p / = 3 sounds”
- BLL147 `BLL147_1_0.html` <p>→<—> “They encounter deep ruts in the road.”

### `menu:flat` → `ABSENT-inWT` — 932 blocks / 548 pages / 176 modules
families: ENGI 95, MXFL 92, BLL 87, HPRE 70, AGH 68, HIS 58, XOTPB 52, ANZH 39
- AGH1001 `AGH1001_1_0.html` <h5>→<—> “We are learning to:”
- AGH1002 `AGH1002_1_0.html` <h5>→<—> “We are learning to:”
- AGH1003 `AGH1003_1_0.html` <h5>→<—> “We are learning to:”
- AGH1004 `AGH1004_1_0.html` <h5>→<—> “We are learning to:”
- AGH1005 `AGH1005_1_0.html` <h5>→<—> “We are learning to:”
- AGH1005 `AGH1005_2_0.html` <h5>→<—> “We are learning to:”

### `body:free` → `OTHER-PAGE` — 878 blocks / 112 pages / 79 modules
families: TRR 372, GENO 77, AGH 59, MXDI 54, SSFUN 26, XGF 25, XDLS 24, XLP 19
- AGH1005 `AGH1005_4_0.html` <h3>→<—> “Exploring the plant process of transpiration”
- AGH1007 `AGH1007_3_0.html` <p>→<—> “Digestion is a key life process that livestock in New Zealand carry out. Digestion is the ”
- AGH1009 `AGH1009_5_0.html` <p>→<—> “Farmers and growers use chemicals on plants and animals to prevent or quickly control: ins”
- ANZH105 `ANZH105_7_0.html` <p>→<—> “We have all come to Aotearoa New Zealand from somewhere else. Although we may live in a di”
- ANZH401 `ANZH401_13_0.html` <p>→<—> “Watch this video and think about what our society might be like in the future. You have a ”
- ART1006 `ART1006_2_0.html` <p>→<—> “Refer to your statement of intent. What are you intending on creating?”

### `body:widget:dragAndDrop` → `ABSENT-notWT` — 793 blocks / 164 pages / 122 modules
families: HIS 82, SSFUN 60, XGF 59, AGH 57, HES 50, TEDC 40, ENGS 38, MXFL 38
- AGH1002 `AGH1002_6_0.html` <p>→<—> “binds inorganic particles”
- AGH1003 `AGH1003_2_0.html` <p>→<—> “Boom or centre pivot”
- AGH1004 `AGH1004_1_0.html` <p>→<—> “Precipitation or rainfall”
- AGH1006 `AGH1006_5_0.html` <p>→<—> “Plant protected from the weather, look and grow better, and fruit and flowers don't drag o”
- ANZH203 `ANZH203_4_0.html` <p>→<—> “Cook renamed many places that were already named by Māori.”
- ARFUN02 `ARFUN02_0_0.html` <p>→<—> “Nguru: A nose flute”

### `body:panel:activity` → `body:panel:widget:cv2-interactive` — 755 blocks / 42 pages / 42 modules
families: BLL 414, TWHA 95, CEDR 66, CEDT 63, CEDK 36, TWHK 34, CEDO 17, CEDW 14
- BLL120 `BLL120_0_0.html` <h3>→<p> “Where is the /k/ sound?”
- BLL140 `BLL140_0_0.html` <p>→<p> “Find things in your house that start with the sound / j /.”
- BLL150 `BLL150_0_0.html` <p>→<p> “Find things in your house that start with the sound /k/.”
- BLL160 `BLL160_0_0.html` <p>→<p> “Find things in your house or neighbourhood that have any of the three ‘y’ sounds.”
- BLL170 `BLL170_0_0.html` <p>→<p> “Find things in your house or neighbourhood that start with the sound / qu /.”
- BLL170 `BLL170_0_0.html` <p>→<p> “Find things in your home or neighbourhood that have the letters ‘qu’ written on them.”

