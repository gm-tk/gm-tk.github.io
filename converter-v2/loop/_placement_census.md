# THE PLACEMENT CENSUS (LOOP §1g, D14-S1) — where the human puts it vs where Claude puts it

Generated 2026-09-24 15:42 by `outputs/_placement_census.py` over 533 modules / 2488 paired pages (`_corpus.gate_mods()`; the skeleton gate's pairing) in 95 s. A block = one h1–h6 / p / li / td / th / figcaption / dt / dd with ≥ 20 characters or ≥ 4 words; the module menu's nav labels are not blocks.

## Summary — the fate of every gold block

- **SAME**: 64806 (39.7 %)
- **MOVED**: 37067 (22.7 %)
- **OTHER-PAGE**: 8164 (5.0 %)
- **ABSENT-inWT**: 16889 (10.3 %)
- **ABSENT-notWT**: 36464 (22.3 %)
- total gold blocks: 163390

`SAME` = Claude has the text on the paired page in the same container path; `MOVED` = on the paired page in a DIFFERENT container (the table below); `OTHER-PAGE` = only on another Claude page of the module; `ABSENT-inWT` = on no Claude page but in the Writers Template (a derivable loss); `ABSENT-notWT` = the developer's own words (not derivable).

## 1. The transition table — gold region → Claude region (MOVED, OTHER-PAGE and ABSENT), largest first

Floors (§1d / §1g): a chrome transition (header / menu / footer on either side) needs 10 modules; a body transition 20 pages. `share` = of the gold's region-A blocks in the best family (that Claude has anywhere), the share that took this fate — a consistent placement at ≥ 0.60 over the floor is a CANDIDATE.

| # | gold region | Claude region / fate | blocks | pages | modules | best family (share, blocks, modules) | templates | flag |
|---:|---|---|---:|---:|---:|---|---|---|
| 1 | `acks` | `ABSENT-notWT` | 16665 | 512 | 483 | XOTPG (0.94, 76, 5) | Standard 11881, Inquiry 2293, Fundamentals 1932 | not derivable |
| 2 | `body:activity` | `ABSENT-notWT` | 4290 | 1132 | 380 | ART (0.67, 195, 4) | Standard 3178, Bilingual 509, Fundamentals 451 | not derivable |
| 3 | `body:free` | `ABSENT-notWT` | 3994 | 946 | 359 | MXEX (0.36, 146, 5) | Standard 3098, Fundamentals 573, Bilingual 248 | not derivable |
| 4 | `acks` | `OTHER-PAGE` | 3489 | 254 | 240 | XTAS (0.77, 340, 3) | Standard 3402, Inquiry 45, Bilingual 42 | acks gate |
| 5 | `body:activity` | `body:free` | 3349 | 679 | 331 | CBI (0.36, 31, 4) | Standard 2072, Bilingual 899, Fundamentals 291 | floor ok |
| 6 | `body:widget:dragAndDrop` | `body:widget:cv2-interactive` | 3196 | 432 | 263 | OSAI (0.99, 70, 4) | Standard 2683, Fundamentals 432, Inquiry 43 | un-built widget (A1) |
| 7 | `body:activity` | `body:widget:cv2-interactive` | 2683 | 710 | 334 | OSOH (0.43, 53, 5) | Standard 2041, Fundamentals 382, Bilingual 235 | floor ok |
| 8 | `body:free` | `ABSENT-inWT` | 2370 | 655 | 294 | OSOH (0.20, 96, 5) | Standard 1874, Fundamentals 418, Inquiry 48 | floor ok |
| 9 | `body:activity` | `ABSENT-inWT` | 2352 | 733 | 325 | PWY (0.50, 137, 5) | Standard 1791, Fundamentals 326, Bilingual 162 | floor ok |
| 10 | `body:widget:multiChoiceQuiz` | `body:widget:cv2-interactive` | 2336 | 228 | 149 | ENGJ (0.97, 33, 4) | Standard 1849, Fundamentals 442, Inquiry 37 | un-built widget (A1) |
| 11 | `body:free` | `body:widget:cv2-interactive` | 1743 | 374 | 215 | OSAH (0.38, 80, 3) | Standard 1449, Fundamentals 236, Bilingual 30 | floor ok |
| 12 | `body:widget:accordion` | `ABSENT-notWT` | 1692 | 178 | 113 | HIS (0.65, 192, 4) | Standard 1409, Fundamentals 143, Bilingual 77 | not derivable |
| 13 | `menu:flat` | `ABSENT-notWT` | 1501 | 472 | 192 | ARFUN (1.00, 5, 5) | Standard 1275, Inquiry 169, Fundamentals 57 | not derivable |
| 14 | `menu:flat` | `OTHER-PAGE` | 1466 | 259 | 69 | PWY (0.55, 44, 5) | Standard 1440, Inquiry 21, Fundamentals 5 | floor ok |
| 15 | `body:widget:accordion` | `body:widget:cv2-interactive` | 1391 | 178 | 122 | ENGS (0.35, 23, 3) | Standard 1165, Fundamentals 184, Inquiry 42 | un-built widget (A1) |
| 16 | `body:widget:accordion` | `ABSENT-inWT` | 1321 | 216 | 133 | XMES (0.58, 127, 3) | Standard 1086, Fundamentals 218, Inquiry 15 | floor ok |
| 17 | `body:alert` | `body:free` | 1262 | 375 | 167 | BLLR (1.00, 37, 3) | Standard 1068, Fundamentals 107, Bilingual 80 | CANDIDATE |
| 18 | `acks` | `ABSENT-inWT` | 1246 | 251 | 237 | PWY (0.29, 74, 5) | Standard 928, Inquiry 210, Fundamentals 100 | acks gate |
| 19 | `body:widget:accordion` | `body:free` | 1185 | 142 | 83 | TEFUN (0.74, 64, 4) | Standard 897, Fundamentals 157, Inquiry 116 | CANDIDATE |
| 20 | `body:free` | `body:activity` | 1015 | 287 | 150 | SSFUN (0.13, 33, 5) | Standard 792, Bilingual 138, Fundamentals 82 | floor ok |
| 21 | `body:widget:multiChoiceQuiz` | `ABSENT-inWT` | 941 | 140 | 92 | PWY (0.57, 184, 5) | Standard 765, Fundamentals 145, Inquiry 31 | floor ok |
| 22 | `menu:flat` | `ABSENT-inWT` | 932 | 548 | 176 | XOTPB (0.36, 52, 6) | Standard 886, Inquiry 44, Fundamentals 2 | floor ok |
| 23 | `body:free` | `OTHER-PAGE` | 878 | 112 | 79 | TRR (0.25, 367, 4) | Standard 480, Bilingual 367, Fundamentals 16 | floor ok |
| 24 | `body:widget:dragAndDrop` | `ABSENT-notWT` | 793 | 165 | 124 | HES (1.00, 50, 3) | Standard 630, Fundamentals 121, Bilingual 33 | not derivable |
| 25 | `body:widget:flipCard` | `body:widget:cv2-interactive` | 750 | 115 | 94 | XOTPB (1.00, 36, 6) | Standard 607, Fundamentals 132, Bilingual 6 | un-built widget (A1) |
| 26 | `body:alert` | `ABSENT-notWT` | 740 | 276 | 136 | PHE (0.69, 20, 4) | Standard 591, Bilingual 63, Fundamentals 57 | not derivable |
| 27 | `body:panel:activity` | `body:panel:widget:cv2-interactive` | 707 | 40 | 40 | CEDR (0.21, 65, 4) | Inquiry 705, Standard 2 | floor ok |
| 28 | `body:widget:dragAndDrop` | `ABSENT-inWT` | 690 | 195 | 133 | OSGM (0.40, 27, 3) | Standard 585, Fundamentals 92, Inquiry 7 | floor ok |
| 29 | `body:widget:tabs` | `ABSENT-inWT` | 679 | 95 | 64 | OSOH (0.53, 31, 3) | Standard 614, Fundamentals 65 | floor ok |
| 30 | `body:widget:tabs` | `body:free` | 643 | 72 | 59 | TEFUN (0.70, 101, 5) | Standard 508, Fundamentals 129, Inquiry 6 | CANDIDATE |
| 31 | `body:widget:carousel` | `ABSENT-inWT` | 639 | 137 | 107 | BLL (0.49, 99, 13) | Standard 558, Fundamentals 71, Inquiry 5 | floor ok |
| 32 | `body:panel:activity` | `ABSENT-notWT` | 621 | 52 | 50 | TWHA (0.38, 239, 6) | Inquiry 605, Standard 16 | not derivable |
| 33 | `body:widget:dropQuiz` | `body:widget:cv2-interactive` | 617 | 114 | 95 | OSAI (0.89, 33, 4) | Standard 421, Fundamentals 196 | un-built widget (A1) |
| 34 | `body:widget:dropDown` | `ABSENT-inWT` | 617 | 60 | 55 | OSAI (0.82, 62, 4) | Standard 493, Fundamentals 124 | CANDIDATE |
| 35 | `body:widget:carousel` | `ABSENT-notWT` | 611 | 119 | 94 | XDLS (0.42, 64, 5) | Standard 459, Fundamentals 100, Inquiry 37 | not derivable |
| 36 | `body:widget:flipCard` | `ABSENT-inWT` | 593 | 113 | 83 | PNR (0.60, 15, 3) | Standard 468, Fundamentals 101, Bilingual 15 | CANDIDATE |
| 37 | `body:activity` | `OTHER-PAGE` | 582 | 207 | 94 | TRR (0.09, 198, 8) | Standard 379, Bilingual 199, Inquiry 4 | floor ok |
| 38 | `body:widget:tabs` | `body:widget:cv2-interactive` | 561 | 83 | 55 | ANZH (0.43, 21, 4) | Standard 539, Fundamentals 17, Inquiry 5 | un-built widget (A1) |
| 39 | `body:widget:carousel` | `body:widget:cv2-interactive` | 547 | 99 | 78 | BLLR (0.37, 23, 3) | Standard 415, Fundamentals 100, Bilingual 29 | un-built widget (A1) |
| 40 | `body:widget:reorder` | `body:widget:cv2-interactive` | 543 | 77 | 57 | BLL (0.88, 68, 10) | Standard 478, Fundamentals 62, Bilingual 3 | un-built widget (A1) |
| 41 | `body:alert` | `ABSENT-inWT` | 519 | 212 | 119 | ENGR (0.38, 15, 3) | Standard 437, Fundamentals 62, Bilingual 11 | floor ok |
| 42 | `body:widget:typing` | `body:widget:cv2-interactive` | 512 | 102 | 62 | ENGC (1.00, 13, 3) | Standard 468, Fundamentals 42, Bilingual 2 | un-built widget (A1) |
| 43 | `body:widget:radioQuiz` | `body:widget:cv2-interactive` | 494 | 75 | 63 | ENGC (0.87, 53, 6) | Standard 379, Fundamentals 115 | un-built widget (A1) |
| 44 | `body:panel:activity` | `ABSENT-inWT` | 490 | 43 | 42 | TWHK (0.32, 73, 4) | Inquiry 487, Standard 3 | floor ok |
| 45 | `body:widget:tabs` | `ABSENT-notWT` | 486 | 70 | 48 | AGH (0.36, 39, 4) | Standard 458, Fundamentals 27, Inquiry 1 | not derivable |
| 46 | `body:widget:multiChoiceQuiz` | `body:free` | 480 | 52 | 42 | WJFUN (0.29, 93, 3) | Standard 331, Fundamentals 135, Bilingual 10 | floor ok |
| 47 | `body:widget:accordion` | `body:activity` | 478 | 48 | 33 | BLL (0.07, 53, 10) | Standard 431, Bilingual 39, Inquiry 7 | floor ok |
| 48 | `body:panel:free` | `ABSENT-notWT` | 452 | 41 | 37 | TWHA (0.39, 167, 6) | Inquiry 320, Standard 132 | not derivable |
| 49 | `body:widget:wordHighlighter` | `body:free` | 436 | 55 | 42 | WJFUN (0.72, 277, 9) | Fundamentals 306, Standard 130 | CANDIDATE |
| 50 | `body:widget:multiChoiceQuiz` | `ABSENT-notWT` | 430 | 75 | 63 | SSFUN (0.81, 42, 4) | Standard 285, Fundamentals 107, Bilingual 30 | not derivable |
| 51 | `body:panel:widget:accordion` | `ABSENT-inWT` | 417 | 14 | 13 | EXPFUN (0.47, 330, 4) | Inquiry 410, Standard 7 | below floor |
| 52 | `body:panel:activity` | `body:panel:free` | 395 | 43 | 41 | CEDK (0.20, 44, 3) | Inquiry 383, Standard 12 | floor ok |
| 53 | `body:widget:multiChoiceQuiz` | `body:activity` | 355 | 57 | 43 | PES (0.73, 81, 3) | Standard 284, Fundamentals 65, Bilingual 5 | CANDIDATE |
| 54 | `body:widget:dropDown` | `ABSENT-notWT` | 346 | 21 | 19 | ENGI (0.26, 11, 3) | Standard 234, Fundamentals 112 | not derivable |
| 55 | `menu:Information` | `menu:Overview` | 339 | 23 | 23 | BLL (0.90, 171, 7) | Standard 322, Bilingual 17 | CANDIDATE |
| 56 | `body:widget:typing` | `ABSENT-notWT` | 335 | 73 | 51 | MXEX (0.52, 35, 4) | Standard 293, Fundamentals 38, Bilingual 4 | not derivable |
| 57 | `body:widget:accordion` | `OTHER-PAGE` | 314 | 18 | 16 |  | Standard 292, Bilingual 21, Inquiry 1 | below floor |
| 58 | `body:widget:speechBubble` | `ABSENT-inWT` | 312 | 103 | 69 | MXFL (0.47, 26, 4) | Standard 254, Fundamentals 42, Inquiry 14 | floor ok |
| 59 | `menu:Information` | `ABSENT-notWT` | 305 | 98 | 86 | ART (0.69, 33, 3) | Standard 255, Bilingual 49, Inquiry 1 | not derivable |
| 60 | `menu:flat` | `body:free` | 303 | 85 | 44 | EXPFUN (0.86, 18, 4) | Standard 247, Inquiry 34, Fundamentals 22 | CANDIDATE |
| 61 | `menu:Overview` | `ABSENT-notWT` | 276 | 92 | 91 | MXFL (0.41, 22, 5) | Standard 244, Bilingual 26, Fundamentals 4 | not derivable |
| 62 | `body:widget:dropDown` | `body:widget:cv2-interactive` | 275 | 34 | 30 | BLL (0.90, 72, 4) | Standard 206, Fundamentals 60, Bilingual 9 | un-built widget (A1) |
| 63 | `menu:Information` | `OTHER-PAGE` | 274 | 37 | 10 |  | Standard 274 | floor ok |
| 64 | `body:widget:dropQuiz` | `ABSENT-inWT` | 267 | 63 | 57 | BLL (0.26, 27, 5) | Standard 179, Fundamentals 88 | floor ok |
| 65 | `menu:Overview` | `OTHER-PAGE` | 267 | 35 | 12 |  | Standard 267 | floor ok |
| 66 | `body:panel:widget:accordion` | `body:panel:free` | 262 | 14 | 14 | TWHA (0.37, 11, 3) | Inquiry 262 | below floor |
| 67 | `body:widget:carousel` | `body:free` | 260 | 61 | 56 | TEFUN (0.36, 47, 4) | Standard 171, Fundamentals 82, Bilingual 6 | floor ok |
| 68 | `body:widget:dropQuiz` | `ABSENT-notWT` | 247 | 50 | 42 | SSFUN (0.38, 26, 4) | Standard 178, Fundamentals 69 | not derivable |
| 69 | `body:panel:widget:accordion` | `ABSENT-notWT` | 233 | 16 | 15 | EXPFUN (0.21, 148, 3) | Inquiry 177, Standard 56 | not derivable |
| 70 | `body:widget:dragAndDrop` | `body:free` | 230 | 44 | 39 | PES (0.17, 15, 3) | Standard 147, Fundamentals 36, Inquiry 34 | floor ok |
| 71 | `header:other` | `ABSENT-notWT` | 225 | 210 | 111 | MXFUN (1.00, 3, 3) | Standard 184, Fundamentals 17, Bilingual 17 | not derivable |
| 72 | `body:panel:free` | `ABSENT-inWT` | 212 | 42 | 39 | CEDO (0.11, 24, 4) | Inquiry 181, Standard 31 | floor ok |
| 73 | `body:widget:flipCard` | `ABSENT-notWT` | 206 | 62 | 56 | SSFUN (0.38, 18, 3) | Standard 138, Fundamentals 61, Bilingual 4 | not derivable |
| 74 | `body:panel:free` | `body:panel:widget:cv2-interactive` | 200 | 27 | 27 | CEDR (0.17, 40, 3) | Inquiry 197, Standard 3 | floor ok |
| 75 | `body:widget:wordHighlighter` | `ABSENT-inWT` | 199 | 48 | 40 | ENGJ (0.55, 23, 5) | Standard 107, Fundamentals 92 | floor ok |
| 76 | `body:widget:speechBubble` | `body:widget:cv2-interactive` | 198 | 92 | 60 | XDLS (0.26, 47, 5) | Standard 175, Fundamentals 20, Inquiry 3 | un-built widget (A1) |
| 77 | `body:activity` | `body:alert` | 196 | 55 | 34 | ANZH (0.08, 49, 3) | Standard 190, Fundamentals 3, Bilingual 2 | floor ok |
| 78 | `body:free` | `body:widget:accordion` | 188 | 37 | 31 | ENG (0.05, 5, 3) | Standard 160, Fundamentals 20, Inquiry 8 | floor ok |
| 79 | `body:widget:speechBubble` | `ABSENT-notWT` | 188 | 70 | 51 | XOTPB (1.00, 6, 6) | Standard 113, Fundamentals 44, Bilingual 19 | not derivable |
| 80 | `body:alert:side` | `body:alert` | 188 | 96 | 59 | ENGJ (0.40, 6, 3) | Standard 161, Fundamentals 21, Inquiry 6 | floor ok |
| 81 | `body:alert` | `body:activity` | 185 | 61 | 36 | ENGJ (0.26, 32, 4) | Standard 155, Bilingual 26, Fundamentals 4 | floor ok |
| 82 | `body:free` | `body:alert` | 183 | 78 | 44 | HIS (0.02, 28, 4) | Standard 165, Fundamentals 15, Inquiry 3 | floor ok |
| 83 | `body:widget:typing` | `ABSENT-inWT` | 183 | 51 | 39 | MXEO (0.22, 19, 4) | Standard 155, Fundamentals 28 | floor ok |
| 84 | `body:widget:dragAndDrop` | `body:activity` | 171 | 34 | 29 | TRR (0.10, 10, 3) | Standard 157, Bilingual 11, Fundamentals 3 | floor ok |
| 85 | `body:alert:side` | `ABSENT-notWT` | 169 | 88 | 58 | MXEX (0.50, 9, 3) | Standard 126, Fundamentals 29, Bilingual 13 | not derivable |
| 86 | `header:other` | `OTHER-PAGE` | 169 | 140 | 45 | ANZH (0.23, 23, 4) | Standard 158, Bilingual 9, Inquiry 2 | floor ok |
| 87 | `body:widget:radioQuiz` | `body:activity` | 167 | 29 | 22 | ANZH (0.62, 16, 3) | Standard 139, Fundamentals 22, Bilingual 6 | CANDIDATE |
| 88 | `body:widget:speechBubble` | `body:free` | 167 | 87 | 54 | TRR (0.35, 18, 4) | Standard 112, Fundamentals 30, Bilingual 18 | floor ok |
| 89 | `body:widget:flipCard` | `body:free` | 164 | 35 | 31 | SSFUN (0.21, 10, 3) | Standard 133, Fundamentals 31 | floor ok |
| 90 | `body:widget:tabs` | `OTHER-PAGE` | 164 | 15 | 11 |  | Standard 160, Fundamentals 4 | below floor |
| 91 | `menu:Information` | `menu:Knowledge` | 162 | 11 | 2 |  | Standard 162 | below floor |
| 92 | `menu:Overview` | `ABSENT-inWT` | 161 | 80 | 65 | GEO (0.11, 7, 3) | Standard 135, Fundamentals 16, Bilingual 6 | floor ok |
| 93 | `body:free` | `body:widget:carousel` | 161 | 36 | 33 | AGH (0.02, 23, 3) | Standard 128, Fundamentals 33 | floor ok |
| 94 | `menu:Information` | `ABSENT-inWT` | 158 | 81 | 69 | OSGM (0.29, 6, 3) | Standard 151, Bilingual 4, Inquiry 3 | floor ok |
| 95 | `body:alert` | `OTHER-PAGE` | 155 | 58 | 33 | TRR (0.26, 62, 4) | Standard 93, Bilingual 62 | floor ok |
| 96 | `body:activity` | `body:widget:accordion` | 155 | 35 | 31 | BLL (0.01, 19, 13) | Standard 142, Fundamentals 12, Inquiry 1 | floor ok |
| 97 | `menu:LI` | `menu:Overview` | 153 | 12 | 12 | XMES (0.98, 61, 3) | Standard 103, Bilingual 43, Inquiry 6 | CANDIDATE |
| 98 | `header:other` | `ABSENT-inWT` | 147 | 140 | 74 | PES (0.36, 17, 5) | Standard 137, Inquiry 8, Fundamentals 2 | floor ok |
| 99 | `body:panel:widget:dragAndDrop` | `body:panel:widget:cv2-interactive` | 147 | 20 | 20 | CEDO (0.91, 31, 3) | Inquiry 147 | un-built widget (A1) |
| 100 | `body:free:side` | `body:free` | 145 | 50 | 40 | HIS (0.77, 30, 6) | Standard 97, Fundamentals 46, Inquiry 2 | CANDIDATE |
| 101 | `menu:Knowledge` | `menu:Overview` | 144 | 12 | 12 | BLL (0.88, 142, 11) | Standard 131, Inquiry 11, Fundamentals 2 | CANDIDATE |
| 102 | `body:widget:hintSlider` | `body:widget:cv2-interactive` | 141 | 21 | 18 | ENFUN (0.21, 15, 3) | Standard 116, Fundamentals 25 | un-built widget (A1) |
| 103 | `body:widget:accordion` | `body:widget:carousel` | 137 | 17 | 11 |  | Standard 137 | below floor |
| 104 | `body:panel:free` | `body:panel:activity` | 131 | 26 | 26 | BLL (0.24, 29, 8) | Inquiry 131 | floor ok |
| 105 | `body:panel:widget:multiChoiceQuiz` | `body:panel:widget:cv2-interactive` | 126 | 9 | 9 | TWHA (0.25, 60, 3) | Inquiry 126 | un-built widget (A1) |
| 106 | `body:alert` | `body:widget:cv2-interactive` | 125 | 59 | 47 | ENGI (0.12, 10, 3) | Standard 87, Fundamentals 28, Bilingual 10 | floor ok |
| 107 | `body:free` | `header:other` | 123 | 123 | 50 | ANZH (0.03, 16, 4) | Standard 120, Inquiry 3 | floor ok |
| 108 | `body:widget:typing` | `body:activity` | 120 | 34 | 25 | MXDI (0.16, 28, 3) | Standard 118, Fundamentals 2 | floor ok |
| 109 | `body:panel:widget:accordion` | `body:panel:widget:cv2-interactive` | 120 | 10 | 10 |  | Inquiry 118, Standard 2 | un-built widget (A1) |
| 110 | `body:widget:radioQuiz` | `ABSENT-inWT` | 119 | 22 | 22 | HPFUN (0.41, 28, 3) | Standard 73, Fundamentals 37, Inquiry 9 | floor ok |
| 111 | `body:free:side` | `ABSENT-notWT` | 119 | 43 | 36 | XDLS (0.35, 7, 3) | Standard 91, Fundamentals 26, Inquiry 2 | not derivable |
| 112 | `body:alert:side` | `ABSENT-inWT` | 118 | 61 | 46 | MXFU (0.50, 22, 3) | Standard 102, Fundamentals 11, Bilingual 5 | floor ok |
| 113 | `body:widget:accordion` | `body:alert` | 118 | 25 | 16 | XDLS (0.01, 8, 5) | Standard 117, Inquiry 1 | floor ok |
| 114 | `body:widget:radioQuiz` | `ABSENT-notWT` | 114 | 20 | 18 | AGH (0.26, 19, 3) | Standard 102, Bilingual 11, Fundamentals 1 | not derivable |
| 115 | `body:panel:widget:multiChoiceQuiz` | `ABSENT-inWT` | 113 | 8 | 8 | TWHA (0.36, 85, 4) | Inquiry 113 | below floor |
| 116 | `body:widget:memoryGame` | `body:widget:cv2-interactive` | 113 | 22 | 19 |  | Standard 89, Fundamentals 12, Bilingual 12 | un-built widget (A1) |
| 117 | `body:widget:reorder` | `ABSENT-inWT` | 112 | 30 | 23 |  | Standard 100, Fundamentals 12 | floor ok |
| 118 | `body:panel:widget:flipCard` | `ABSENT-notWT` | 109 | 7 | 7 | TWHA (0.44, 90, 4) | Inquiry 109 | not derivable |
| 119 | `body:alert:side` | `body:free` | 108 | 51 | 36 | ENGI (0.17, 5, 3) | Standard 81, Fundamentals 21, Bilingual 6 | floor ok |
| 120 | `menu:LI` | `menu:Information` | 108 | 5 | 5 | TRR (0.41, 108, 5) | Bilingual 108 | below floor |
| 121 | `body:widget:wordHighlighter` | `ABSENT-notWT` | 105 | 24 | 22 | ENFUN (0.31, 22, 4) | Standard 60, Fundamentals 45 | not derivable |
| 122 | `body:panel:widget:multiChoiceQuiz` | `ABSENT-notWT` | 105 | 7 | 7 | TWHA (0.39, 94, 4) | Inquiry 97, Standard 8 | not derivable |
| 123 | `body:panel:widget:tabs` | `ABSENT-notWT` | 105 | 3 | 2 |  | Standard 105 | not derivable |
| 124 | `body:widget:selfCheck` | `body:widget:cv2-interactive` | 104 | 31 | 20 | BLL (0.71, 10, 3) | Standard 93, Bilingual 6, Fundamentals 4 | un-built widget (A1) |
| 125 | `body:widget:hintSlider` | `body:widget:flipCard` | 103 | 7 | 5 | ENFUN (0.30, 21, 4) | Standard 82, Fundamentals 21 | below floor |
| 126 | `body:panel:widget:flipCard` | `body:panel:widget:cv2-interactive` | 100 | 13 | 13 |  | Inquiry 100 | un-built widget (A1) |
| 127 | `body:panel:widget:flipCard` | `ABSENT-inWT` | 100 | 7 | 7 | TWHA (0.21, 43, 4) | Inquiry 100 | below floor |
| 128 | `other:free` | `body:free` | 94 | 5 | 5 |  | Standard 94 | below floor |
| 129 | `menu:Standards` | `ABSENT-notWT` | 92 | 42 | 40 | GEO (0.40, 4, 3) | Standard 89, Inquiry 3 | not derivable |
| 130 | `body:activity` | `body:widget:flipCard` | 92 | 11 | 8 |  | Standard 85, Inquiry 7 | below floor |
| 131 | `body:widget:tabs` | `body:widget:carousel` | 92 | 10 | 6 |  | Standard 68, Fundamentals 24 | below floor |
| 132 | `body:widget:selfCheck` | `ABSENT-inWT` | 91 | 26 | 21 |  | Standard 70, Inquiry 14, Fundamentals 7 | floor ok |
| 133 | `body:free` | `body:widget:flipCard` | 91 | 14 | 13 | XLP (0.03, 12, 3) | Standard 59, Fundamentals 32 | below floor |
| 134 | `body:widget:dropQuiz` | `body:activity` | 89 | 15 | 14 | HPFUN (0.28, 30, 4) | Fundamentals 45, Standard 44 | below floor |
| 135 | `menu:Practices` | `menu:Overview` | 86 | 11 | 11 | BLL (1.00, 85, 10) | Standard 85, Fundamentals 1 | CANDIDATE |
| 136 | `body:widget:wordHighlighter` | `body:widget:cv2-interactive` | 86 | 19 | 18 | BLL (0.35, 15, 3) | Standard 45, Fundamentals 41 | un-built widget (A1) |
| 137 | `body:widget:tabs` | `body:alert` | 86 | 7 | 5 |  | Standard 86 | below floor |
| 138 | `menu:pane2` | `menu:Overview` | 86 | 7 | 7 | XMES (1.00, 45, 3) | Standard 64, Bilingual 22 | below floor |
| 139 | `body:widget:multiChoiceQuiz` | `OTHER-PAGE` | 80 | 12 | 10 |  | Standard 60, Bilingual 20 | below floor |
| 140 | `body:alert:side` | `body:activity` | 79 | 36 | 20 | TRR (0.51, 29, 3) | Standard 48, Bilingual 29, Inquiry 1 | floor ok |
| 141 | `body:free:side` | `ABSENT-inWT` | 78 | 30 | 29 |  | Standard 75, Fundamentals 2, Inquiry 1 | floor ok |
| 142 | `menu:Standards` | `ABSENT-inWT` | 78 | 53 | 46 | XDLS (0.34, 20, 8) | Standard 68, Inquiry 10 | floor ok |
| 143 | `body:widget:dropQuiz` | `body:free` | 78 | 11 | 11 |  | Fundamentals 41, Standard 27, Bilingual 10 | below floor |
| 144 | `body:panel:widget:carousel` | `ABSENT-inWT` | 76 | 12 | 12 | BLL (0.86, 42, 3) | Inquiry 71, Standard 5 | below floor |
| 145 | `body:widget:hintSlider` | `ABSENT-notWT` | 75 | 16 | 14 |  | Standard 56, Fundamentals 19 | not derivable |
| 146 | `body:widget:wordSelect` | `body:activity` | 74 | 21 | 19 | WJFUN (0.56, 30, 4) | Standard 35, Fundamentals 33, Bilingual 6 | floor ok |
| 147 | `body:widget:wordSelect` | `ABSENT-inWT` | 71 | 19 | 16 |  | Fundamentals 37, Standard 33, Bilingual 1 | below floor |
| 148 | `body:widget:tabs` | `body:activity` | 70 | 11 | 10 | HIS (0.12, 20, 3) | Standard 69, Fundamentals 1 | below floor |
| 149 | `body:widget:hintSlider` | `ABSENT-inWT` | 70 | 13 | 10 |  | Standard 57, Fundamentals 11, Inquiry 2 | below floor |
| 150 | `body:widget:accordion` | `body:widget:flipCard` | 69 | 7 | 6 |  | Standard 69 | below floor |

## 2. Headings only (the SECTIONS) — gold region → Claude region / fate

| gold region | Claude region / fate | headings | pages | modules | examples |
|---|---|---:|---:|---:|---|
| `body:activity` | `ABSENT-notWT` | 796 | 453 | 198 | AGH1001 AGH1001_1_0.html <h3>→<—> “What are primary products?”; AGH1001 AGH1001_1_0.html <h3>→<—> “Agricultural and horticultural products”; AGH1001 AGH1001_2_0.html <h3>→<—> “Value of Primary Products” |
| `body:activity` | `ABSENT-inWT` | 498 | 352 | 194 | AGH1001 AGH1001_3_0.html <h3>→<—> “Māori creation story”; AGH1001 AGH1001_4_0.html <h3>→<—> “New Zealand’s four seasons”; AGH1002 AGH1002_6_0.html <h3>→<—> “Levels of organic matter” |
| `body:activity` | `body:free` | 397 | 240 | 150 | AGH1001 AGH1001_3_0.html <h3>→<h3> “Self Check: True or False”; AGH1004 AGH1004_1_0.html <h3>→<h3> “Knowledge self-check”; AGH1004 AGH1004_2_0.html <h3>→<h3> “Reflective questions” |
| `body:free` | `ABSENT-notWT` | 365 | 204 | 119 | AGH1001 AGH1001_2_0.html <h4>→<—> “Pre-European settlement”; AGH1001 AGH1001_2_0.html <h4>→<—> “Late 18th Century - Mid 19th Century”; AGH1001 AGH1001_2_0.html <h4>→<—> “Late 19th Century - Mid 20th Century” |
| `body:activity` | `body:widget:cv2-interactive` | 357 | 191 | 104 | ANZH203 ANZH203_1_0.html <h3>→<p> “Comprehension activity”; ARFUN02 ARFUN02_0_0.html <h3>→<p> “What Have I Learned? He aha aku i ako ai?”; ARFUN03 ARFUN03_0_0.html <h3>→<p> “What have I learnt?” |
| `body:widget:accordion` | `ABSENT-notWT` | 313 | 80 | 56 | AGH1003 AGH1003_4_0.html <h4>→<—> “Returning crop residues”; AGH1003 AGH1003_7_0.html <h4>→<—> “What causes poor drainage?”; AGH1003 AGH1003_7_0.html <h5>→<—> “This open drain is an example of surface drainage.” |
| `menu:flat` | `ABSENT-inWT` | 312 | 293 | 80 | AGH1001 AGH1001_1_0.html <h5>→<—> “We are learning to:”; AGH1001 AGH1001_2_0.html <h5>→<—> “We are learning to:”; AGH1001 AGH1001_3_0.html <h5>→<—> “We are learning to:” |
| `body:free` | `ABSENT-inWT` | 291 | 182 | 132 | AGH1001 AGH1001_0_0.html <h3>→<—> “An introduction to agricultural and horticultural ”; AGH1002 AGH1002_3_0.html <h4>→<—> “C = carbon, H = Hydrogen, O = Oxygen”; AGH1005 AGH1005_6_0.html <h4>→<—> “Mycorrhizal associations” |
| `body:widget:accordion` | `body:widget:cv2-interactive` | 248 | 87 | 68 | AGH1008 AGH1008_3_0.html <h4>→<td> “Forward/creep grazing”; AGH1009 AGH1009_1_0.html <h5>→<td> “Cultural recognition (Cultural recognition princip”; AGH1009 AGH1009_1_0.html <h5>→<td> “Sustainable Resource Management (Sustainable Resou” |
| `body:widget:accordion` | `ABSENT-inWT` | 243 | 113 | 80 | AGH1003 AGH1003_4_0.html <h4>→<—> “Slurry Tankers/Umbilical Systems”; AGH1005 AGH1005_2_0.html <h4>→<—> “Disease and pest resistance”; AGH1005 AGH1005_2_0.html <h4>→<—> “Breeding and selection” |
| `header:other` | `ABSENT-notWT` | 222 | 207 | 110 | AGH1004 AGH1004_1_0.html <h1>→<—> “Factors influencing where primary production syste”; AGH1004 AGH1004_5_0.html <h1>→<—> “Where does our water come from?”; AGH1004 AGH1004_6_0.html <h1>→<—> “Market Factor Influences” |
| `body:activity` | `OTHER-PAGE` | 194 | 130 | 55 | ANZH301 ANZH301_1_0.html <h4>→<—> “Go to your journal”; ANZH303 ANZH303_4_0.html <h4>→<—> “Go to your journal”; ANZH303 ANZH303_6_0.html <h4>→<—> “Go to your journal” |
| `menu:flat` | `ABSENT-notWT` | 185 | 185 | 63 | ARFUN01 ARFUN01_0_0.html <h5>→<—> “You will show your understanding by:”; ARFUN02 ARFUN02_0_0.html <h5>→<—> “You will show your understanding by:”; ARFUN03 ARFUN03_0_0.html <h5>→<—> “You will show your understanding by:” |
| `header:other` | `OTHER-PAGE` | 169 | 140 | 45 | AGH1007 AGH1007_7_0.html <h1>→<—> “Livestock and Agriculture in Aotearoa New Zealand”; AGH1009 AGH1009_8_0.html <h1>→<—> “Primary production and soil quality.”; ANZH101 ANZH101_1_0.html <h1>→<—> “Tangata Whenua Origin Stories” |
| `header:other` | `ABSENT-inWT` | 147 | 140 | 74 | AGH1001 AGH1001_0_0.html <h1>→<—> “From the Ground Up”; AGH1001 AGH1001_0_0.html <h1>→<—> “Mai i te Nuku ki te Rangi”; AGH1002 AGH1002_4_0.html <h1>→<—> “Physical properties of soil” |
| `body:free` | `body:widget:cv2-interactive` | 147 | 75 | 61 | AGH1002 AGH1002_3_0.html <h4>→<th> “Air level in soil”; AGH1006 AGH1006_4_0.html <h3>→<p> “Protective Structures”; AGH1009 AGH1009_1_0.html <h4>→<th> “European world view (Colonial times)” |
| `body:widget:accordion` | `body:free` | 132 | 54 | 40 | AGH1004 AGH1004_2_0.html <h4>→<h4> “Semi-intensive Farming”; AGH1004 AGH1004_2_0.html <h4>→<h4> “Semi-extensive Farming”; AGH1006 AGH1006_6_0.html <h4>→<h3> “Integrated weed management” |
| `menu:flat` | `OTHER-PAGE` | 130 | 104 | 21 | ANZH203 ANZH203_1_0.html <h4>→<—> “How will I know if I’ve learned it?”; ANZH203 ANZH203_2_0.html <h4>→<—> “How will I know if I’ve learned it?”; ANZH203 ANZH203_3_0.html <h4>→<—> “How will I know if I’ve learned it?” |
| `body:free` | `body:activity` | 129 | 104 | 71 | AGH1003 AGH1003_3_0.html <h3>→<p> “Flowers and fertilisers”; AGH1004 AGH1004_5_0.html <h3>→<h3> “Impact of Irrigation on Production”; AGH1005 AGH1005_7_0.html <h3>→<p> “Common pests and diseases” |
| `body:widget:flipCard` | `ABSENT-inWT` | 123 | 46 | 38 | CEDO502 CEDO502_1_1.html <h5>→<—> “Credit card shopping”; CEDO502 CEDO502_5_0.html <h5>→<—> “What is a closed question?”; CEDO502 CEDO502_5_0.html <h5>→<—> “What is an open question?” |
| `body:free` | `header:other` | 121 | 121 | 48 | AGH1005 AGH1005_0_0.html <h3>→<h1> “Ko te tūhura i te tipu me te tukanga i Aotearoa | ”; AGH1005 AGH1005_2_0.html <h3>→<h1> “Exploring plant anatomy and its impact on primary ”; AGH1005 AGH1005_5_0.html <h3>→<h1> “Exploring the plant process of respiration and its” |
| `body:alert` | `body:free` | 93 | 76 | 51 | AGH1003 AGH1003_5_0.html <h4>→<p> “Why is it important to add lime before fertiliser ”; AGH1009 AGH1009_4_0.html <h4>→<p> “A note on sprays”; ANZH103 ANZH103_1_0.html <h3>→<h3> “What happened after the Treaty was signed on 6 Feb” |
| `body:widget:carousel` | `ABSENT-inWT` | 83 | 33 | 27 | ANZH105 ANZH105_6_0.html <h4>→<—> “New Zealand Māori Kapa haka”; ANZH303 ANZH303_5_0.html <h4>→<—> “The Eight-pointed Stars”; BLL262 BLL262_3_0.html <h5>→<—> “Pointillism Fish Part 1” |
| `body:panel:activity` | `body:panel:free` | 75 | 22 | 22 | BLL240 BLL240_0_0.html <h4>→<h5> “Words making the 'ear' sound”; BLL240 BLL240_0_0.html <h4>→<h5> “Words making the 'air' sound”; BLL240 BLL240_0_0.html <h4>→<h5> “Words making the 'ur' sound” |
| `body:widget:carousel` | `ABSENT-notWT` | 74 | 25 | 19 | AGH1009 AGH1009_2_0.html <h4>→<—> “Decomposition and fossilisation”; AGH1009 AGH1009_2_0.html <h4>→<—> “Ocean Sedimentationand Absorption”; ART1006 ART1006_1_0.html <h4>→<—> “PowerPoint/slideshow presentations” |
| `body:panel:activity` | `ABSENT-notWT` | 74 | 30 | 28 | BLL120 BLL120_0_0.html <h3>→<—> “Writing words with the digraph ck”; BLL250 BLL250_0_0.html <h4>→<—> “Ben the Lamb and the Gentle Climb”; BLL250 BLL250_0_0.html <h4>→<—> “The Sleigh in the Snow” |
| `menu:Information` | `ABSENT-notWT` | 73 | 64 | 58 | AGH1001 AGH1001_0_0.html <h5>→<—> “Want to know where to start?”; AGH1002 AGH1002_0_0.html <h5>→<—> “Want to know where to start?”; AGH1003 AGH1003_0_0.html <h5>→<—> “Want to know where to start?” |
| `body:alert` | `ABSENT-notWT` | 72 | 54 | 29 | AGH1007 AGH1007_3_0.html <h4>→<—> “Key points from the lesson:”; AGH1007 AGH1007_4_0.html <h4>→<—> “Key points from the lesson:”; AGH1007 AGH1007_5_0.html <h4>→<—> “Key points from the lesson:” |
| `body:free` | `OTHER-PAGE` | 69 | 31 | 24 | AGH1005 AGH1005_4_0.html <h3>→<—> “Exploring the plant process of transpiration”; CBI1009 CBI1009_1_0.html <h2>→<—> “Soluble and insoluble Salts”; CEDO501 CEDO501_3_0.html <h3>→<—> “Search engines and Artificial Intelligence” |
| `body:widget:flipCard` | `body:widget:cv2-interactive` | 68 | 22 | 18 | ANZH105 ANZH105_5_0.html <h4>→<td> “What is it made of?”; ANZH105 ANZH105_5_0.html <h4>→<td> “Where is it from?”; ANZH105 ANZH105_5_0.html <h4>→<td> “How old is it?” |
| `body:alert` | `ABSENT-inWT` | 62 | 50 | 35 | AGH1003 AGH1003_1_0.html <h4>→<—> “Need some extra help?”; ANZH301 ANZH301_7_0.html <h4>→<—> “Want to know more?”; ANZH301 ANZH301_9_0.html <h4>→<—> “Some other examples of urban marae:” |
| `body:panel:activity` | `ABSENT-inWT` | 61 | 24 | 23 | BLL120 BLL120_0_0.html <h3>→<—> “Writing the letter k”; BLL120 BLL120_0_0.html <h3>→<—> “My name is, my sound is…”; BLL160 BLL160_0_0.html <h4>→<—> “A child was in bed sleeping. A duck ran in the doo” |
| `body:widget:carousel` | `body:widget:cv2-interactive` | 57 | 20 | 18 | BLL271 BLL271_1_0.html <h4>→<td> “pa / ki / hi / wi”; CEDO502 CEDO502_5_0.html <h5>→<p> “Use keywords carefully”; CEDO502 CEDO502_5_0.html <h5>→<p> “Use headings and subheadings” |
| `menu:Information` | `ABSENT-inWT` | 56 | 45 | 43 | BLL251 BLL251_0_0.html <h4>→<—> “Tirohanga Whānui | Overview”; BLL255 BLL255_0_0.html <h4>→<—> “Tirohanga Whānui | Overview”; BLL257 BLL257_0_0.html <h4>→<—> “Tirohanga Whānui | Overview” |
| `body:panel:widget:accordion` | `body:panel:free` | 55 | 12 | 12 | CEDK401 CEDK401_0_0.html <h4>→<h4> “Go to your journal”; CEDK401 CEDK401_0_0.html <h4>→<h4> “Go to your journal”; CEDK401 CEDK401_0_0.html <h4>→<h4> “Go to your journal” |
| `header:other` | `body:free` | 54 | 49 | 38 | AGH1006 AGH1006_8_0.html <h1>→<h3> “Pest and disease management”; ANZH301 ANZH301_1_0.html <h1>→<h3> “Life before, during and after the Second World War”; ANZH303 ANZH303_4_0.html <h1>→<h3> “Innovation, Interactions and Mana.” |
| `body:panel:free` | `ABSENT-inWT` | 53 | 21 | 19 | CEDK101 CEDK101_0_0.html <h2>→<—> “Light and technology”; CEDO202 CEDO202_0_0.html <h2>→<—> “Creating and sharing your dance”; CEDO204 CEDO204_0_0.html <h4>→<—> “Beaver dams and lodges” |
| `body:widget:wordHighlighter` | `body:free` | 45 | 10 | 10 | ENFUN01 ENFUN01_0_0.html <h3>→<h5> “Why is knowing about author’s purpose important?”; ENFUN04 ENFUN04_0_0.html <h3>→<h5> “Homophones, homonyms and homographs”; ENFUN05 ENFUN05_0_0.html <h3>→<h3> “Full stops, capital letters, exclamation marks” |
| `body:widget:tabs` | `ABSENT-inWT` | 44 | 19 | 15 | AGH1001 AGH1001_2_0.html <h5>→<—> “Mussel Farmer – Jake Bartram, Hauraki Gulf New Zea”; ENGS201 ENGS201_4_0.html <h5>→<—> “Write a what if scenario.”; ENGS201 ENGS201_4_0.html <h5>→<—> “Imagine you are a superhero!” |
| `body:widget:tabs` | `body:widget:cv2-interactive` | 44 | 19 | 16 | ANZH203 ANZH203_6_0.html <h4>→<p> “Charles Heaphy: Artist, Draughtsman and Explorer”; ENGC301 ENGC301_1_0.html <h4>→<th> “Static advertisement”; ENGC301 ENGC301_7_0.html <h4>→<th> “Static advertisement” |
| `menu:Overview` | `ABSENT-notWT` | 40 | 36 | 35 | BLL253 BLL253_0_0.html <h4>→<—> “How will I know if I've learned it?”; BLL271 BLL271_0_0.html <h4>→<—> “How will I know I have learned it?”; BLL273 BLL273_0_0.html <h4>→<—> “How will I know if I've learned it?” |
| `body:panel:free` | `ABSENT-notWT` | 40 | 13 | 9 | CEDR101 CEDR101_0_0.html <h3>→<—> “TLearning from friends and whānau”; CEDR101 CEDR101_0_0.html <h3>→<—> “Who is leading the score?”; CEDR203 CEDR203_0_0.html <h2>→<—> “Aotearoa New Zealand Eco-leaders” |
| `body:widget:tabs` | `body:free` | 35 | 16 | 16 | AGH1001 AGH1001_2_0.html <h5>→<p> “Farm Advisor – Ash Phillips, Wairoa New Zealand”; ANZH203 ANZH203_6_0.html <h4>→<p> “Thomas Brunner: Surveyor and Explorer”; ENGC403 ENGC403_12_0.html <h4>→<h5> “Oral presentation part” |
| `menu:flat` | `body:free` | 33 | 21 | 13 | BLL124 BLL124_0_0.html <h5>→<h4> “Whāinga Ako | Learning Intentions”; BLL124 BLL124_0_0.html <h5>→<h4> “Paearu Angitu | How will I know if I’ve learned it”; CBI1008 CBI1008_1_0.html <h5>→<h3> “We are learning about:” |
| `body:widget:flipCard` | `ABSENT-notWT` | 31 | 16 | 16 | CHFUN05 CHFUN05_0_0.html <h5>→<—> “我不吃。wǒ bù chīI don’t eat.”; CHFUN05 CHFUN05_0_0.html <h5>→<—> “你不喜欢。nǐ bù xǐhuānYou don’t like it.”; CHFUN05 CHFUN05_0_0.html <h5>→<—> “然后ránhòuafterwards / after that” |
| `body:activity:side` | `ABSENT-notWT` | 31 | 11 | 3 | TEDC402 TEDC402_8_0.html <h5>→<—> “Spot the issue A”; XTAS102 XTAS102_1_0.html <h5>→<—> “Not fun. Too hard.”; XTAS102 XTAS102_1_0.html <h5>→<—> “Ok. I had to work hard to do this.” |
| `body:widget:accordion` | `body:activity` | 29 | 11 | 9 | AGH1008 AGH1008_5_0.html <h4>→<h5> “Increased chance of pregnancy”; AGH1008 AGH1008_5_0.html <h4>→<h5> “Increased production through better genetic select”; AGH1008 AGH1008_5_0.html <h4>→<h5> “Reduced need for having a bull on farm” |
| `body:widget:carousel` | `body:free` | 26 | 12 | 12 | ANZH105 ANZH105_6_0.html <h4>→<h4> “Cook Island Māori drumming and dancing”; CEDR501 CEDR501_6_0.html <h4>→<h3> “Speaking too fast or too quietly.”; CEDR501 CEDR501_6_0.html <h4>→<h3> “Using slang, filler words, or casual talk.” |
| `body:free:side` | `ABSENT-inWT` | 24 | 11 | 11 | ART1002 ART1002_0_0.html <h5>→<—> “Wrecking the White Page”; ART1002 ART1002_0_0.html <h5>→<—> “The Visual Arts Diary”; DTC1005 DTC1005_1_0.html <h3>→<—> “Digital Outcome Domain of your choice” |
| `body:activity` | `body:alert` | 23 | 9 | 5 | AGH1001 AGH1001_5_0.html <h3>→<li> “Management Practices on a Production System”; ENGS102 ENGS102_6_0.html <h4>→<p> “The girl was in the woods.”; ENGS302 ENGS302_6_0.html <h3>→<h5> “What is a timetable?” |
| `body:free` | `body:widget:carousel` | 21 | 14 | 14 | ANZH205 ANZH205_7_0.html <h3>→<h4> “What can we do to honour te titiri?”; ARFUN02 ARFUN02_0_0.html <h4>→<h4> “How to understand it:”; ENFUN03 ENFUN03_0_0.html <h3>→<h4> “Adverb sentence starters” |
| `body:widget:tabs` | `ABSENT-notWT` | 21 | 12 | 11 | ART1006 ART1006_1_0.html <h5>→<—> “(this is where others can input into your idea)”; ENG1005 ENG1005_0_0.html <h5>→<—> “Demonstrate perceptive understanding of studied te”; HES1002 HES1002_7_0.html <h4>→<—> “Va, Va'a or Vaha” |
| `body:widget:flipCard` | `body:free` | 21 | 8 | 8 | BLLR202 BLLR202_4_0.html <h5>→<td> “Read between the lines”; CHFUN05 CHFUN05_0_0.html <h5>→<td> “我吃。wǒ chī.I eat.”; CHFUN05 CHFUN05_0_0.html <h5>→<td> “他去。tā qù.He is going.” |
| `body:activity` | `body:widget:flipCard` | 21 | 4 | 2 | ENGI102 ENGI102_2_0.html <h4>→<p> “Dress-up or Puppet Play”; ENGI102 ENGI102_2_0.html <h4>→<p> “Make a picture of a scene in the story”; ENGI102 ENGI102_2_0.html <h4>→<p> “Create an important item from the fairytale out of” |
| `menu:LI` | `menu:Overview` | 21 | 9 | 9 | MXS1004 MXS1004_0_0.html <h5>→<h4> “Whāinga Ako | Learning Intentions”; MXS1004 MXS1004_0_0.html <h5>→<h4> “Paearu Angitu | How will I know if I’ve learned it”; PMT101 PMT101_0_0.html <h5>→<td> “Kei te ako au kia:” |
| `menu:LI` | `menu:Information` | 21 | 5 | 5 | TRR103 TRR103_0_0.html <h5>→<h5> “Whakamaheretia tō wā:”; TRR103 TRR103_0_0.html <h5>→<h5> “He aha tāku hei tīmata?”; TRR103 TRR103_0_0.html <h5>→<h5> “What do I need to get started?” |
| `body:panel:free` | `body:panel:activity` | 20 | 10 | 10 | BLL250 BLL250_0_0.html <h2>→<h3> “The 'augh' letter team”; CEDK101 CEDK101_0_0.html <h3>→<h3> “How does light travel?”; CEDK101 CEDK101_0_0.html <h3>→<h3> “Light reflection and refraction” |
| `body:widget:accordion` | `body:widget:carousel` | 19 | 5 | 5 | AGH1005 AGH1005_7_0.html <h5>→<li> “Powdery mildew (various species):”; AGH1005 AGH1005_7_0.html <h5>→<li> “Rust diseases (various species):”; AGH1005 AGH1005_7_0.html <h5>→<li> “Tomato yellow leaf curl virus (TYLCV):” |
| `body:panel:activity` | `body:panel:widget:cv2-interactive` | 19 | 9 | 9 | BLL120 BLL120_0_0.html <h3>→<p> “Where is the /k/ sound?”; BLL210 BLL210_0_0.html <h5>→<th> “Uses one of these things:”; CEDR204 CEDR204_0_0.html <h4>→<p> “A Day at the Beach” |
| `menu:Overview` | `OTHER-PAGE` | 19 | 19 | 6 | ENGJ201 ENGJ201_1_0.html <h3>→<—> “How will I know if I’ve learned it?”; ENGJ201 ENGJ201_2_0.html <h3>→<—> “How will I know if I’ve learned it?”; ENGJ201 ENGJ201_3_0.html <h3>→<—> “How will I know if I’ve learned it?” |

## 3. Region agreement — of the gold's blocks in region A that Claude has on the paired page, the share it keeps in A

| gold region | matched on page | kept in region | moved | agreement |
|---|---:|---:|---:|---:|
| `body:free` | 23979 | 20203 | 3776 | 0.843 |
| `body:activity` | 18165 | 11582 | 6583 | 0.638 |
| `menu:flat` | 7743 | 7316 | 427 | 0.945 |
| `body:widget:accordion` | 6132 | 2749 | 3383 | 0.448 |
| `body:widget:dragAndDrop` | 4005 | 328 | 3677 | 0.082 |
| `acks` | 3935 | 3925 | 10 | 0.997 |
| `body:alert` | 3617 | 1899 | 1718 | 0.525 |
| `menu:Overview` | 3359 | 3246 | 113 | 0.966 |
| `body:widget:multiChoiceQuiz` | 3318 | 90 | 3228 | 0.027 |
| `body:panel:activity` | 3206 | 2047 | 1159 | 0.638 |
| `body:panel:free` | 3032 | 2584 | 448 | 0.852 |
| `body:widget:carousel` | 2131 | 1140 | 991 | 0.535 |
| `body:widget:flipCard` | 2113 | 1093 | 1020 | 0.517 |
| `menu:Information` | 2087 | 1435 | 652 | 0.688 |
| `body:widget:tabs` | 2043 | 508 | 1535 | 0.249 |
| `body:widget:speechBubble` | 1364 | 960 | 404 | 0.704 |
| `header:other` | 1335 | 1266 | 69 | 0.948 |
| `body:widget:dropQuiz` | 881 | 81 | 800 | 0.092 |
| `body:panel:widget:accordion` | 794 | 350 | 444 | 0.441 |
| `body:widget:radioQuiz` | 715 | 0 | 715 | 0.000 |
| `body:widget:typing` | 699 | 21 | 678 | 0.030 |
| `body:widget:wordHighlighter` | 598 | 0 | 598 | 0.000 |
| `body:widget:reorder` | 589 | 0 | 589 | 0.000 |
| `body:alert:side` | 542 | 98 | 444 | 0.181 |
| `body:widget:hintSlider` | 490 | 185 | 305 | 0.378 |
| `menu:LI` | 399 | 131 | 268 | 0.328 |
| `menu:pane2` | 399 | 242 | 157 | 0.607 |
| `body:widget:dropDown` | 363 | 60 | 303 | 0.165 |
| `menu:Standards` | 361 | 331 | 30 | 0.917 |
| `menu:pane3` | 342 | 218 | 124 | 0.637 |
| `menu:Knowledge` | 334 | 170 | 164 | 0.509 |
| `body:free:side` | 240 | 39 | 201 | 0.163 |
| `body:panel:widget:dragAndDrop` | 223 | 35 | 188 | 0.157 |
| `body:panel:widget:carousel` | 221 | 132 | 89 | 0.597 |
| `body:panel:widget:flipCard` | 201 | 65 | 136 | 0.323 |
| `body:widget:selfCheck` | 197 | 0 | 197 | 0.000 |
| `menu:Practices` | 187 | 101 | 86 | 0.540 |
| `other:free` | 180 | 0 | 180 | 0.000 |
| `body:panel:widget:multiChoiceQuiz` | 172 | 29 | 143 | 0.169 |
| `body:panel:alert` | 165 | 104 | 61 | 0.630 |

## 4. Examples for the 25 largest transitions

### `acks` → `ABSENT-notWT` — 16665 blocks / 512 pages / 483 modules
families: BLL 2501, MXFL 1202, XDLS 654, ANZH 585, TRR 503, ENGS 452, XGF 439, HPFUN 434
- AGH1001 `AGH1001_5_0.html` <p>→<—> “Every effort has been made to acknowledge and contact copyright holders. Te Aho o Te Kura ”
- AGH1002 `AGH1002_6_0.html` <p>→<—> “Every effort has been made to acknowledge and contact copyright holders. Te Aho o Te Kura ”
- AGH1003 `AGH1003_8_0.html` <p>→<—> “Every effort has been made to acknowledge and contact copyright holders. Te Aho o Te Kura ”
- AGH1005 `AGH1005_8_0.html` <p>→<—> “Every effort has been made to acknowledge and contact copyright holders. Te Aho o Te Kura ”
- AGH1007 `AGH1007_9_0.html` <p>→<—> “Every effort has been made to acknowledge and contact copyright holders. Te Aho o Te Kura ”
- AGH1007 `AGH1007_9_0.html` <p>→<—> “Video: Delicious Starts Here - Farmer Story, Silver Fern Farms, https://www.youtube.com/wa”

### `body:activity` → `ABSENT-notWT` — 4290 blocks / 1132 pages / 380 modules
families: TRR 486, XDLS 338, HIS 224, AGH 213, ART 195, BLL 186, MXFL 134, ENGI 126
- AGH1001 `AGH1001_1_0.html` <h3>→<—> “What are primary products?”
- AGH1002 `AGH1002_2_0.html` <h3>→<—> “Soil practical – Texture by sedimentation”
- AGH1003 `AGH1003_2_0.html` <h3>→<—> “Soil properties review”
- AGH1004 `AGH1004_1_0.html` <p>→<—> “Drag and drop the correct factor to the correct classification.”
- AGH1005 `AGH1005_1_0.html` <h3>→<—> “Māori and Western views on plants and their purpose”
- AGH1005 `AGH1005_1_0.html` <p>→<—> “Let’s review the viticulture practices video in the South Island and make a critical judge”

### `body:free` → `ABSENT-notWT` — 3994 blocks / 946 pages / 359 modules
families: HIS 280, TRR 230, XGF 213, MXFL 186, MXFU 179, AGH 172, XDLS 169, MXDI 153
- AGH1001 `AGH1001_0_0.html` <p>→<—> “This module will cover:”
- AGH1002 `AGH1002_6_0.html` <p>→<—> “Biological properties include:”
- AGH1003 `AGH1003_1_0.html` <li>→<—> “Increase the rate of pasture and crop growth.”
- AGH1004 `AGH1004_2_0.html` <th>→<—> “Stocking rate (number of sheep per hectare)”
- AGH1005 `AGH1005_1_0.html` <p>→<—> “The mauri model decision making framework was created by Dr Kepa Morgan. It has been desig”
- AGH1005 `AGH1005_2_0.html` <p>→<—> “Plant anatomy focuses on the structure and organisation of plant parts (cells and tissues)”

### `acks` → `OTHER-PAGE` — 3489 blocks / 254 pages / 240 modules
families: MXFL 852, BLL 518, XTAS 340, XDLS 296, XLP 160, OSAI 137, XMES 102, AGH 101
- AGH1001 `AGH1001_5_0.html` <p>→<—> “Photo: Roast beef on cutting board with salt and pepper. Top view, iStock 645249428, Getty”
- AGH1002 `AGH1002_6_0.html` <p>→<—> “Photo: Yellow gorse flowers on a bush, iStock 685756664, Getty Images. Used with permissio”
- AGH1003 `AGH1003_8_0.html` <p>→<—> “Photo: Kiwifruit industry in New Zealand, iStock 1401383311, Getty Images. Used with permi”
- AGH1005 `AGH1005_8_0.html` <p>→<—> “Photo: Tractor spraying young corn with pesticides, iStock 1224290959, Getty Images. Used ”
- AGH1008 `AGH1008_8_0.html` <p>→<—> “Photo: Oral Drench, PGG Wrightsons, https://store.pggwrightson.co.nz/animal-health/sheep-o”
- AGH1008 `AGH1008_8_0.html` <p>→<—> “Photo: Pour on Drench, PGG Wrightsons, https://store.pggwrightson.co.nz/animal-health/catt”

### `body:activity` → `body:free` — 3349 blocks / 679 pages / 331 modules
families: TRR 758, XGF 261, BLL 148, TEDC 145, XDLS 141, PMT 121, HIS 120, WJFUN 87
- AGH1001 `AGH1001_2_0.html` <p>→<p> “Watch these videos and complete activity 2C in your learning journal.”
- AGH1002 `AGH1002_2_0.html` <p>→<p> “Go to your learning journal and complete activity 2B.”
- AGH1003 `AGH1003_2_0.html` <p>→<p> “Revisit this list from earlier in the lesson. Select the soil properties which are altered”
- AGH1004 `AGH1004_1_0.html` <h3>→<h3> “Knowledge self-check”
- AGH1005 `AGH1005_3_0.html` <p>→<p> “Complete activity 3A in your learning journal.”
- AGH1005 `AGH1005_4_0.html` <p>→<p> “Complete activity 5B in your learning journal.”

### `body:widget:dragAndDrop` → `body:widget:cv2-interactive` — 3196 blocks / 432 pages / 263 modules
families: BLL 265, WJFUN 209, ENGI 178, MXFL 160, XGF 148, ENGC 138, PWY 130, OSBY 110
- AGH1001 `AGH1001_1_0.html` <p>→<th> “Agricultural Production”
- AGH1003 `AGH1003_2_0.html` <p>→<td> “Small sheep and beef farm”
- AGH1004 `AGH1004_2_0.html` <p>→<th> “Mountains and high country”
- AGH1005 `AGH1005_1_0.html` <p>→<li> “Plants are important for food, feeding stock and industrial uses.”
- AGH1007 `AGH1007_5_0.html` <p>→<td> “Ewe pregnant with singles”
- AGH1007 `AGH1007_5_0.html` <p>→<li> “Ewe lamb being finished”

### `body:activity` → `body:widget:cv2-interactive` — 2683 blocks / 710 pages / 334 modules
families: BLL 258, TRR 221, XMES 151, FRNO 143, WJFUN 127, MXDB 108, MXFL 103, HIS 102
- AGH1001 `AGH1001_1_0.html` <p>→<p> “Select the primary products below which you think are produced in New Zealand or Pacific I”
- AGH1002 `AGH1002_5_0.html` <p>→<p> “Match the chemical symbol with the nutrient.”
- AGH1003 `AGH1003_2_0.html` <p>→<p> “For each production type, identify the irrigation system which would be best suited.”
- AGH1004 `AGH1004_3_0.html` <p>→<p> “From the list, select the region that has the best average of GDD days for each year.”
- AGH1005 `AGH1005_1_0.html` <p>→<p> “Order the following phrases into similarities and differences.”
- AGH1005 `AGH1005_6_0.html` <p>→<p> “Getting the correct amount of nutrients in the soil is a balancing act for many growers. H”

### `body:free` → `ABSENT-inWT` — 2370 blocks / 655 pages / 294 modules
families: TEDC 152, ENGJ 104, PWY 103, OSOH 96, XDLS 94, AGH 93, CHFUN 92, WJFUN 86
- AGH1001 `AGH1001_0_0.html` <h3>→<—> “An introduction to agricultural and horticultural science in Aotearoa New Zealand | He wha”
- AGH1002 `AGH1002_1_0.html` <p>→<—> “As soil gets older, more horizons form. Click on the horizons below to find out more about”
- AGH1003 `AGH1003_0_0.html` <p>→<—> “This module explores the ways farmers and growers do this on various production systems wh”
- AGH1005 `AGH1005_0_0.html` <p>→<—> “It’s important that you fully understand these processes and that they do not occur in iso”
- AGH1006 `AGH1006_2_0.html` <p>→<—> “Commercial crop production uses three main ways to propagate new plants; sowing seeds, cut”
- AGH1006 `AGH1006_3_0.html` <p>→<—> “Cultivation is especially important in intensive horticulture-like commercial market garde”

### `body:activity` → `ABSENT-inWT` — 2352 blocks / 733 pages / 325 modules
families: TEDC 217, ENGS 138, PWY 137, BLL 117, WJFUN 93, XDLS 90, TRR 83, XMES 81
- AGH1001 `AGH1001_2_0.html` <p>→<—> “Complete activity 2B in your learning journal.”
- AGH1002 `AGH1002_4_0.html` <p>→<—> “Go to your learning journal and complete activity 4B and 4C.”
- AGH1003 `AGH1003_3_0.html` <h3>→<—> “Fertiliser application”
- AGH1004 `AGH1004_2_0.html` <h4>→<—> “New Zealand Topographical Map”
- AGH1005 `AGH1005_8_0.html` <h3>→<—> “How plants flower and produce fruit”
- AGH1008 `AGH1008_1_0.html` <h3>→<—> “Manaakitanga in practice”

### `body:widget:multiChoiceQuiz` → `body:widget:cv2-interactive` — 2336 blocks / 228 pages / 149 modules
families: XGF 359, BLL 186, WJFUN 165, MXFL 129, MXFU 117, ENGR 101, PWY 86, ENFUN 79
- AGH1003 `AGH1003_2_0.html` <p>→<td> “Water-holding capacity”
- ANZH104 `ANZH104_7_0.html` <p>→<li> “My journal is complete”
- ANZH105 `ANZH105_8_0.html` <p>→<li> “My journal is complete.”
- ANZH203 `ANZH203_1_0.html` <p>→<li> “What nationality was Abel Tasman”
- ARFUN03 `ARFUN03_0_0.html` <p>→<p> “The dancer’s focus is the audience.”
- ARFUN03 `ARFUN03_0_0.html` <p>→<p> “The dancer's focus is his foot.”

### `body:free` → `body:widget:cv2-interactive` — 1743 blocks / 374 pages / 215 modules
families: XDLS 125, OSAH 80, ENGI 78, OSAI 71, SSCI 67, AGH 66, MXFL 62, OSSM 62
- AGH1001 `AGH1001_2_0.html` <p>→<p> “Below is a brief timeline of the events that have shaped Aotearoa into where we stand toda”
- AGH1002 `AGH1002_3_0.html` <h4>→<th> “Air level in soil”
- AGH1003 `AGH1003_2_0.html` <p>→<p> “While the irrigation system used mainly depends on the size of the production, a range of ”
- AGH1004 `AGH1004_6_0.html` <p>→<p> “As you can see, this process is highly dependent on the ability to store and keep milk bel”
- AGH1005 `AGH1005_1_0.html` <p>→<p> “What differences do you notice between each model of growing plants?”
- AGH1005 `AGH1005_1_0.html` <p>→<p> “As you can see, both models support the use of plants for the purpose of keeping people an”

### `body:widget:accordion` → `ABSENT-notWT` — 1692 blocks / 178 pages / 113 modules
families: MXFL 352, HIS 192, XDLS 109, XGF 78, TRR 74, MXFU 70, ENGC 60, XLP 60
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

### `body:widget:accordion` → `body:widget:cv2-interactive` — 1391 blocks / 178 pages / 122 modules
families: BLL 151, XGF 94, XDLS 84, PWY 71, MXFL 56, HPRE 55, ENGJ 53, WJFUN 50
- AGH1008 `AGH1008_3_0.html` <p>→<th> “Cows, or sheep, are kept in one big group and moved around paddocks daily, or every second”
- AGH1009 `AGH1009_1_0.html` <p>→<th> “The Treaty of Waitangi is about partnership between the Crown and Māori. This partnership ”
- ANZH203 `ANZH203_3_0.html` <h4>→<p> “Tupaia and the Endeavour”
- ANZH304 `ANZH304_1_0.html` <p>→<p> “Felton Mathew, living in Sydney, accepted an offer to come to New Zealand with Hobson as t”
- BLL112 `BLL112_2_0.html` <li>→<li> “Why do you think the tap might be running?”
- BLL112 `BLL112_2_0.html` <li>→<li> “What do you notice about this tap?”

### `body:widget:accordion` → `ABSENT-inWT` — 1321 blocks / 216 pages / 133 modules
families: XMES 127, TEDC 111, CHFUN 109, PWY 92, CEDR 75, AGH 63, BLL 58, XGF 56
- AGH1003 `AGH1003_4_0.html` <h4>→<—> “Slurry Tankers/Umbilical Systems”
- AGH1005 `AGH1005_2_0.html` <h4>→<—> “Disease and pest resistance”
- AGH1006 `AGH1006_1_0.html` <h4>→<—> “Integrated pest management (IPM)”
- AGH1008 `AGH1008_3_0.html` <li>→<—> “high dry matter (average 85 percent DM)”
- AGH1009 `AGH1009_1_0.html` <h5>→<—> “Partnership (Partnership principle)”
- AGH1009 `AGH1009_1_0.html` <h4>→<—> “Cultural recognition”

### `body:alert` → `body:free` — 1262 blocks / 375 pages / 167 modules
families: HIS 96, PES 95, HPRE 81, XGF 77, CEDO 74, TRR 70, ANZH 59, ENFUN 51
- AGH1001 `AGH1001_5_0.html` <p>→<p> “A management practice is an activity or job done by a farmer or a grower to produce their ”
- AGH1002 `AGH1002_1_0.html` <li>→<li> “The importance of soils to Māori goes back to the creation story and the first humans.”
- AGH1003 `AGH1003_2_0.html` <p>→<p> “This is why earthworms come to the surface after heavy rain – to escape from the water tha”
- AGH1005 `AGH1005_3_0.html` <li>→<li> “Plants are producers. This means they make their own food.”
- AGH1007 `AGH1007_9_0.html` <li>→<li> “Diseases are caused by bacteria, parasites, viruses, fungi and metabolic issues.”
- AGH1007 `AGH1007_9_0.html` <li>→<li> “Bacteria and parasites are the most common cause of health problems in livestock.”

### `acks` → `ABSENT-inWT` — 1246 blocks / 251 pages / 237 modules
families: BLL 242, ANZH 106, PWY 74, MXFL 69, CEDO 56, HIS 50, ENGS 49, MXDI 41
- AGH1001 `AGH1001_5_0.html` <p>→<—> “Photo: Colm & Gaynor Tierney, RNZ/Carol Stiles, https://www.rnz.co.nz/national/programmes/”
- AGH1005 `AGH1005_8_0.html` <p>→<—> “Photo: Abstract Weather Concept - Sun In Serene Sky With Flare Effect, iStock 1300645794, ”
- AGH1007 `AGH1007_9_0.html` <p>→<—> “Illustration: Pigs mouth, https://quizlet.com/365126001/exercise-science-fetal-pig-1-exter”
- AGH1009 `AGH1009_9_0.html` <p>→<—> “Photo: Farmer hold a smartphone on a background of a field with a pepper plantations. Agri”
- ANZH101 `ANZH101_3_0.html` <p>→<—> “Image: New shoot of fern frond on New Zealand tree fern, iStock 1703245930, Getty Images. ”
- ANZH101 `ANZH101_3_0.html` <p>→<—> “Google Slides: e Waka o Aoraki,Connected – Ministry of Education https://docs.google.com/p”

### `body:widget:accordion` → `body:free` — 1185 blocks / 142 pages / 83 modules
families: XGF 139, MXFL 96, ENGFUN 89, TEFUN 64, XDLS 56, CEDR 55, ENGJ 49, WJFUN 44
- AGH1004 `AGH1004_2_0.html` <p>→<p> “Intensive farming is farming where high numbers of animals or crop plants are grown in a s”
- AGH1006 `AGH1006_5_0.html` <p>→<p> “Pruning is the removal of branches or roots from a plant. This is done to change the plant”
- AGH1008 `AGH1008_3_0.html` <p>→<td> “Tough fibrous feed which is usually fed as a supplementary feed during the winter months a”
- ANZH101 `ANZH101_2_0.html` <h4>→<h4> “Ranginui and Papatūānuku”
- ARFUN02 `ARFUN02_0_0.html` <p>→<h5> “Today we're exploring how Rhythm (Ūngēri) works together with repetition. (Takiruaruatanga”
- ARFUN02 `ARFUN02_0_0.html` <h4>→<h5> “How Rhythm and Repetition Work Together:”

### `body:free` → `body:activity` — 1015 blocks / 287 pages / 150 modules
families: TRR 134, AGH 100, HIS 100, MXFL 72, MXDI 61, XDLS 53, MXFU 52, ANZH 42
- AGH1001 `AGH1001_4_0.html` <p>→<p> “Traditional Māori horticultural practices were guided by maramataka or the lunar calendar.”
- AGH1002 `AGH1002_2_0.html` <p>→<p> “The proportion of sand, silt and clay describes a soil's texture. BUT soil particles don’t”
- AGH1003 `AGH1003_1_0.html` <p>→<p> “Soil management practices are the focus of this module. They are the management practices ”
- AGH1004 `AGH1004_5_0.html` <p>→<p> “Here is a video of how water is used to feed crops and pasture:”
- AGH1005 `AGH1005_2_0.html` <p>→<p> “Fruit is formed from the ovary of a flower after fertilisation. Fruit contain seeds used f”
- AGH1005 `AGH1005_2_0.html` <p>→<p> “The main functions of fruits and seeds are to:”

### `body:widget:multiChoiceQuiz` → `ABSENT-inWT` — 941 blocks / 140 pages / 92 modules
families: PWY 184, TEDC 98, BLL 56, HPFUN 46, MXFL 44, CEDR 39, OSAI 39, MXFUN 34
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
families: TRR 367, GENO 77, AGH 59, MXDI 54, SSFUN 26, XGF 25, XDLS 24, XLP 19
- AGH1005 `AGH1005_4_0.html` <h3>→<—> “Exploring the plant process of transpiration”
- AGH1007 `AGH1007_3_0.html` <p>→<—> “Digestion is a key life process that livestock in New Zealand carry out. Digestion is the ”
- AGH1009 `AGH1009_5_0.html` <p>→<—> “Farmers and growers use chemicals on plants and animals to prevent or quickly control: ins”
- ANZH105 `ANZH105_7_0.html` <p>→<—> “We have all come to Aotearoa New Zealand from somewhere else. Although we may live in a di”
- ANZH401 `ANZH401_13_0.html` <p>→<—> “Watch this video and think about what our society might be like in the future. You have a ”
- ART1006 `ART1006_2_0.html` <p>→<—> “Refer to your statement of intent. What are you intending on creating?”

### `body:widget:dragAndDrop` → `ABSENT-notWT` — 793 blocks / 165 pages / 124 modules
families: HIS 82, SSFUN 60, XGF 59, AGH 57, HES 50, TEDC 40, ENGS 38, MXFL 36
- AGH1002 `AGH1002_6_0.html` <p>→<—> “binds inorganic particles”
- AGH1003 `AGH1003_2_0.html` <p>→<—> “Boom or centre pivot”
- AGH1004 `AGH1004_1_0.html` <p>→<—> “Precipitation or rainfall”
- AGH1006 `AGH1006_5_0.html` <p>→<—> “Plant protected from the weather, look and grow better, and fruit and flowers don't drag o”
- ANZH203 `ANZH203_4_0.html` <p>→<—> “Cook renamed many places that were already named by Māori.”
- ARFUN02 `ARFUN02_0_0.html` <p>→<—> “Nguru: A nose flute”

### `body:widget:flipCard` → `body:widget:cv2-interactive` — 750 blocks / 115 pages / 94 modules
families: HPFUN 73, MXFL 52, BLL 48, OSSC 44, HPRE 42, PWY 41, XOTPB 36, TEDC 35
- ANZH105 `ANZH105_5_0.html` <h4>→<td> “What is it made of?”
- ANZH304 `ANZH304_4_0.html` <p>→<p> “Colonial officials mainly understood Te Tiriti o Waitangi (the Treaty of Waitangi) based o”
- ARFUN01 `ARFUN01_0_0.html` <p>→<p> “William Shakespeare is a famous playwright. Reading or watching his plays show us what it ”
- ARFUN03 `ARFUN03_0_0.html` <p>→<p> “The dancers are on a high level.”
- BLL171 `BLL171_2_0.html` <h4>→<th> “If you could create a new ice cream flavour, what would it taste like?”
- BLL171 `BLL171_2_0.html` <h4>→<th> “Would you rather be able to fly like a bird or swim like a fish?”

