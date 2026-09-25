# THE PLACEMENT CENSUS (LOOP §1g, D14-S1) — where the human puts it vs where Claude puts it

Generated 2026-09-25 21:12 by `outputs/_placement_census.py` over 533 modules / 2487 paired pages (`_corpus.gate_mods()`; the skeleton gate's pairing) in 80 s. A block = one h1–h6 / p / li / td / th / figcaption / dt / dd with ≥ 20 characters or ≥ 4 words; the module menu's nav labels are not blocks.

## Summary — the fate of every gold block

- **SAME**: 65975 (40.3 %)
- **MOVED**: 36511 (22.3 %)
- **OTHER-PAGE**: 8190 (5.0 %)
- **ABSENT-inWT**: 16603 (10.1 %)
- **ABSENT-notWT**: 36558 (22.3 %)
- total gold blocks: 163837

`SAME` = Claude has the text on the paired page in the same container path; `MOVED` = on the paired page in a DIFFERENT container (the table below); `OTHER-PAGE` = only on another Claude page of the module; `ABSENT-inWT` = on no Claude page but in the Writers Template (a derivable loss); `ABSENT-notWT` = the developer's own words (not derivable).

## 1. The transition table — gold region → Claude region (MOVED, OTHER-PAGE and ABSENT), largest first

Floors (§1d / §1g): a chrome transition (header / menu / footer on either side) needs 10 modules; a body transition 20 pages. `share` = of the gold's region-A blocks in the best family (that Claude has anywhere), the share that took this fate — a consistent placement at ≥ 0.60 over the floor is a CANDIDATE.

| # | gold region | Claude region / fate | blocks | pages | modules | best family (share, blocks, modules) | templates | flag |
|---:|---|---|---:|---:|---:|---|---|---|
| 1 | `acks` | `ABSENT-notWT` | 16716 | 514 | 485 | XOTPG (0.94, 76, 5) | Standard 11881, Inquiry 2318, Fundamentals 1932 | not derivable |
| 2 | `body:activity` | `ABSENT-notWT` | 4320 | 1132 | 380 | ART (0.67, 195, 4) | Standard 3178, Bilingual 544, Fundamentals 451 | not derivable |
| 3 | `body:free` | `ABSENT-notWT` | 3989 | 945 | 358 | MXEX (0.35, 142, 5) | Standard 3094, Fundamentals 573, Bilingual 249 | not derivable |
| 4 | `acks` | `OTHER-PAGE` | 3489 | 254 | 240 | XTAS (0.77, 340, 3) | Standard 3402, Inquiry 45, Bilingual 42 | acks gate |
| 5 | `body:widget:dragAndDrop` | `body:widget:cv2-interactive` | 3200 | 433 | 263 | OSAI (0.99, 70, 4) | Standard 2682, Fundamentals 432, Inquiry 43 | un-built widget (A1) |
| 6 | `body:activity` | `body:free` | 3154 | 668 | 328 | FRFUN (0.37, 38, 3) | Standard 2068, Bilingual 707, Fundamentals 293 | floor ok |
| 7 | `body:activity` | `body:widget:cv2-interactive` | 2649 | 702 | 332 | OSOH (0.43, 53, 5) | Standard 2014, Fundamentals 376, Bilingual 236 | floor ok |
| 8 | `body:free` | `ABSENT-inWT` | 2378 | 652 | 293 | OSOH (0.23, 110, 5) | Standard 1883, Fundamentals 418, Inquiry 47 | floor ok |
| 9 | `body:activity` | `ABSENT-inWT` | 2336 | 728 | 324 | PWY (0.50, 137, 5) | Standard 1779, Fundamentals 325, Bilingual 162 | floor ok |
| 10 | `body:widget:multiChoiceQuiz` | `body:widget:cv2-interactive` | 2299 | 226 | 149 | ENGJ (0.97, 33, 4) | Standard 1813, Fundamentals 440, Inquiry 37 | un-built widget (A1) |
| 11 | `body:widget:accordion` | `ABSENT-notWT` | 1692 | 178 | 113 | HIS (0.65, 192, 4) | Standard 1409, Fundamentals 143, Bilingual 77 | not derivable |
| 12 | `body:free` | `body:widget:cv2-interactive` | 1666 | 361 | 211 | OSAH (0.38, 80, 3) | Standard 1379, Fundamentals 229, Bilingual 30 | floor ok |
| 13 | `menu:flat` | `ABSENT-notWT` | 1501 | 472 | 192 | ARFUN (1.00, 5, 5) | Standard 1275, Inquiry 169, Fundamentals 57 | not derivable |
| 14 | `menu:flat` | `OTHER-PAGE` | 1466 | 259 | 69 | PWY (0.55, 44, 5) | Standard 1440, Inquiry 21, Fundamentals 5 | floor ok |
| 15 | `body:widget:accordion` | `body:widget:cv2-interactive` | 1292 | 163 | 115 | HPFUN (0.28, 39, 3) | Standard 1075, Fundamentals 175, Inquiry 42 | un-built widget (A1) |
| 16 | `body:alert` | `body:free` | 1275 | 380 | 169 | BLLR (1.00, 37, 3) | Standard 1072, Fundamentals 107, Bilingual 89 | CANDIDATE |
| 17 | `acks` | `ABSENT-inWT` | 1246 | 251 | 237 | PWY (0.29, 74, 5) | Standard 928, Inquiry 210, Fundamentals 100 | acks gate |
| 18 | `body:widget:accordion` | `ABSENT-inWT` | 1193 | 208 | 128 | XMES (0.53, 116, 3) | Standard 960, Fundamentals 218, Inquiry 13 | floor ok |
| 19 | `body:widget:accordion` | `body:free` | 1127 | 138 | 82 | TEFUN (0.74, 64, 4) | Standard 839, Fundamentals 157, Inquiry 116 | CANDIDATE |
| 20 | `body:free` | `body:activity` | 1111 | 291 | 152 | TRR (0.15, 228, 10) | Standard 794, Bilingual 232, Fundamentals 82 | floor ok |
| 21 | `body:widget:multiChoiceQuiz` | `ABSENT-inWT` | 936 | 140 | 92 | PWY (0.56, 179, 5) | Standard 760, Fundamentals 145, Inquiry 31 | floor ok |
| 22 | `menu:flat` | `ABSENT-inWT` | 932 | 548 | 176 | XOTPB (0.36, 52, 6) | Standard 886, Inquiry 44, Fundamentals 2 | floor ok |
| 23 | `body:free` | `OTHER-PAGE` | 880 | 113 | 79 | TRR (0.25, 372, 5) | Standard 480, Bilingual 372, Fundamentals 16 | floor ok |
| 24 | `body:widget:dragAndDrop` | `ABSENT-notWT` | 793 | 165 | 124 | HES (1.00, 50, 3) | Standard 630, Fundamentals 121, Bilingual 33 | not derivable |
| 25 | `body:widget:flipCard` | `body:widget:cv2-interactive` | 746 | 116 | 95 | XOTPB (1.00, 36, 6) | Standard 602, Fundamentals 132, Bilingual 7 | un-built widget (A1) |
| 26 | `body:alert` | `ABSENT-notWT` | 738 | 275 | 135 | PHE (0.69, 20, 4) | Standard 591, Bilingual 63, Fundamentals 57 | not derivable |
| 27 | `body:panel:activity` | `body:panel:widget:cv2-interactive` | 735 | 42 | 42 | BLL (0.21, 412, 12) | Inquiry 733, Standard 2 | floor ok |
| 28 | `body:widget:dragAndDrop` | `ABSENT-inWT` | 688 | 194 | 132 | OSGM (0.40, 27, 3) | Standard 583, Fundamentals 92, Inquiry 7 | floor ok |
| 29 | `body:widget:tabs` | `body:free` | 658 | 72 | 59 | TEFUN (0.80, 116, 5) | Standard 508, Fundamentals 144, Inquiry 6 | CANDIDATE |
| 30 | `body:widget:tabs` | `ABSENT-inWT` | 656 | 92 | 63 | OSOH (0.53, 31, 3) | Standard 606, Fundamentals 50 | floor ok |
| 31 | `body:widget:carousel` | `ABSENT-inWT` | 633 | 135 | 106 | BLL (0.49, 99, 13) | Standard 551, Fundamentals 72, Inquiry 5 | floor ok |
| 32 | `body:panel:activity` | `ABSENT-notWT` | 626 | 53 | 51 | TWHA (0.38, 239, 6) | Inquiry 610, Standard 16 | not derivable |
| 33 | `body:widget:dropQuiz` | `body:widget:cv2-interactive` | 617 | 114 | 95 | OSAI (0.89, 33, 4) | Standard 421, Fundamentals 196 | un-built widget (A1) |
| 34 | `body:widget:dropDown` | `ABSENT-inWT` | 617 | 60 | 55 | OSAI (0.82, 62, 4) | Standard 493, Fundamentals 124 | CANDIDATE |
| 35 | `body:widget:carousel` | `ABSENT-notWT` | 611 | 119 | 94 | XDLS (0.42, 64, 5) | Standard 459, Fundamentals 100, Inquiry 37 | not derivable |
| 36 | `body:activity` | `OTHER-PAGE` | 585 | 210 | 96 | TRR (0.08, 198, 8) | Standard 382, Bilingual 199, Inquiry 4 | floor ok |
| 37 | `body:widget:tabs` | `body:widget:cv2-interactive` | 569 | 85 | 55 | ENGJ (0.44, 85, 5) | Standard 547, Fundamentals 17, Inquiry 5 | un-built widget (A1) |
| 38 | `body:widget:flipCard` | `ABSENT-inWT` | 546 | 99 | 77 | PNR (0.60, 15, 3) | Standard 424, Fundamentals 98, Bilingual 15 | CANDIDATE |
| 39 | `body:widget:reorder` | `body:widget:cv2-interactive` | 543 | 77 | 57 | BLL (0.88, 68, 10) | Standard 478, Fundamentals 62, Bilingual 3 | un-built widget (A1) |
| 40 | `body:alert` | `ABSENT-inWT` | 516 | 211 | 118 | ENGR (0.38, 15, 3) | Standard 436, Fundamentals 62, Bilingual 11 | floor ok |
| 41 | `body:widget:typing` | `body:widget:cv2-interactive` | 512 | 102 | 62 | ENGC (1.00, 13, 3) | Standard 468, Fundamentals 42, Bilingual 2 | un-built widget (A1) |
| 42 | `body:widget:radioQuiz` | `body:widget:cv2-interactive` | 500 | 76 | 64 | ENGC (0.87, 53, 6) | Standard 379, Fundamentals 115, Bilingual 6 | un-built widget (A1) |
| 43 | `body:widget:carousel` | `body:widget:cv2-interactive` | 490 | 87 | 70 | BLLR (0.37, 23, 3) | Standard 361, Fundamentals 97, Bilingual 29 | un-built widget (A1) |
| 44 | `body:widget:tabs` | `ABSENT-notWT` | 486 | 70 | 48 | AGH (0.36, 39, 4) | Standard 458, Fundamentals 27, Inquiry 1 | not derivable |
| 45 | `body:widget:multiChoiceQuiz` | `body:free` | 484 | 53 | 43 | WJFUN (0.29, 93, 3) | Standard 331, Fundamentals 137, Bilingual 12 | floor ok |
| 46 | `body:widget:accordion` | `body:activity` | 480 | 49 | 34 | BLL (0.08, 59, 11) | Standard 440, Bilingual 39, Fundamentals 1 | floor ok |
| 47 | `body:panel:activity` | `ABSENT-inWT` | 461 | 43 | 42 | TWHK (0.32, 73, 4) | Inquiry 458, Standard 3 | floor ok |
| 48 | `body:panel:free` | `ABSENT-notWT` | 454 | 42 | 38 | TWHA (0.39, 167, 6) | Inquiry 322, Standard 132 | not derivable |
| 49 | `body:widget:wordHighlighter` | `body:free` | 438 | 55 | 42 | WJFUN (0.72, 277, 9) | Fundamentals 308, Standard 130 | CANDIDATE |
| 50 | `body:widget:multiChoiceQuiz` | `ABSENT-notWT` | 430 | 75 | 63 | SSFUN (0.81, 42, 4) | Standard 285, Fundamentals 107, Bilingual 30 | not derivable |
| 51 | `body:panel:activity` | `body:panel:free` | 401 | 44 | 42 | CEDK (0.20, 44, 3) | Inquiry 389, Standard 12 | floor ok |
| 52 | `body:panel:widget:accordion` | `ABSENT-inWT` | 391 | 15 | 14 | EXPFUN (0.47, 330, 4) | Inquiry 384, Standard 7 | below floor |
| 53 | `body:widget:multiChoiceQuiz` | `body:activity` | 354 | 56 | 42 | PES (0.73, 81, 3) | Standard 284, Fundamentals 65, Bilingual 4 | CANDIDATE |
| 54 | `body:widget:dropDown` | `ABSENT-notWT` | 346 | 21 | 19 | ENGI (0.26, 11, 3) | Standard 234, Fundamentals 112 | not derivable |
| 55 | `body:widget:typing` | `ABSENT-notWT` | 337 | 74 | 52 | MXEX (0.52, 35, 4) | Standard 293, Fundamentals 38, Bilingual 6 | not derivable |
| 56 | `body:widget:accordion` | `OTHER-PAGE` | 330 | 19 | 17 |  | Standard 308, Bilingual 21, Inquiry 1 | below floor |
| 57 | `body:widget:speechBubble` | `ABSENT-inWT` | 312 | 103 | 69 | MXFL (0.47, 26, 4) | Standard 254, Fundamentals 42, Inquiry 14 | floor ok |
| 58 | `menu:Information` | `ABSENT-notWT` | 308 | 99 | 87 | ART (0.69, 33, 3) | Standard 255, Bilingual 52, Inquiry 1 | not derivable |
| 59 | `menu:flat` | `body:free` | 303 | 85 | 44 | EXPFUN (0.86, 18, 4) | Standard 247, Inquiry 34, Fundamentals 22 | CANDIDATE |
| 60 | `menu:Overview` | `ABSENT-notWT` | 276 | 92 | 91 | MXFL (0.41, 22, 5) | Standard 244, Bilingual 26, Fundamentals 4 | not derivable |
| 61 | `body:widget:dropDown` | `body:widget:cv2-interactive` | 275 | 34 | 30 | BLL (0.90, 72, 4) | Standard 206, Fundamentals 60, Bilingual 9 | un-built widget (A1) |
| 62 | `menu:Information` | `OTHER-PAGE` | 274 | 37 | 10 |  | Standard 274 | floor ok |
| 63 | `body:widget:dropQuiz` | `ABSENT-inWT` | 267 | 63 | 57 | BLL (0.26, 27, 5) | Standard 179, Fundamentals 88 | floor ok |
| 64 | `menu:Information` | `menu:Knowledge` | 267 | 18 | 9 | BLL (0.55, 105, 7) | Standard 267 | below floor |
| 65 | `menu:Overview` | `OTHER-PAGE` | 267 | 35 | 12 |  | Standard 267 | floor ok |
| 66 | `body:panel:widget:accordion` | `body:panel:free` | 262 | 14 | 14 | TWHA (0.37, 11, 3) | Inquiry 262 | below floor |
| 67 | `body:widget:carousel` | `body:free` | 260 | 61 | 55 | TEFUN (0.36, 47, 4) | Standard 171, Fundamentals 82, Bilingual 6 | floor ok |
| 68 | `body:widget:dropQuiz` | `ABSENT-notWT` | 247 | 50 | 42 | SSFUN (0.38, 26, 4) | Standard 178, Fundamentals 69 | not derivable |
| 69 | `body:panel:widget:accordion` | `ABSENT-notWT` | 233 | 16 | 15 | EXPFUN (0.21, 148, 3) | Inquiry 177, Standard 56 | not derivable |
| 70 | `body:widget:dragAndDrop` | `body:free` | 232 | 45 | 40 | PES (0.17, 15, 3) | Standard 147, Fundamentals 36, Inquiry 34 | floor ok |
| 71 | `header:other` | `ABSENT-notWT` | 224 | 209 | 111 | MXFUN (1.00, 3, 3) | Standard 184, Fundamentals 17, Bilingual 17 | not derivable |
| 72 | `body:panel:free` | `ABSENT-inWT` | 210 | 41 | 38 | CEDO (0.11, 24, 4) | Inquiry 179, Standard 31 | floor ok |
| 73 | `body:widget:flipCard` | `ABSENT-notWT` | 206 | 62 | 56 | SSFUN (0.38, 18, 3) | Standard 138, Fundamentals 61, Bilingual 4 | not derivable |
| 74 | `body:free` | `body:widget:accordion` | 203 | 38 | 31 | ENG (0.05, 5, 3) | Standard 175, Fundamentals 20, Inquiry 8 | floor ok |
| 75 | `body:widget:speechBubble` | `body:widget:cv2-interactive` | 201 | 92 | 60 | XDLS (0.26, 47, 5) | Standard 174, Fundamentals 20, Bilingual 4 | un-built widget (A1) |
| 76 | `body:widget:wordHighlighter` | `ABSENT-inWT` | 199 | 48 | 40 | ENGJ (0.55, 23, 5) | Standard 107, Fundamentals 92 | floor ok |
| 77 | `body:panel:free` | `body:panel:widget:cv2-interactive` | 198 | 23 | 23 | CEDR (0.18, 42, 3) | Inquiry 195, Standard 3 | floor ok |
| 78 | `body:activity` | `body:alert` | 195 | 55 | 34 | ANZH (0.08, 49, 3) | Standard 189, Fundamentals 3, Bilingual 2 | floor ok |
| 79 | `body:alert` | `body:activity` | 188 | 63 | 38 | ENGJ (0.26, 32, 4) | Standard 155, Bilingual 29, Fundamentals 4 | floor ok |
| 80 | `body:widget:speechBubble` | `ABSENT-notWT` | 188 | 70 | 51 | XOTPB (1.00, 6, 6) | Standard 113, Fundamentals 44, Bilingual 19 | not derivable |
| 81 | `body:free` | `body:alert` | 183 | 78 | 44 | HIS (0.02, 28, 4) | Standard 165, Fundamentals 15, Inquiry 3 | floor ok |
| 82 | `body:widget:typing` | `ABSENT-inWT` | 183 | 51 | 39 | MXEO (0.22, 19, 4) | Standard 155, Fundamentals 28 | floor ok |
| 83 | `body:alert:side` | `body:alert` | 181 | 90 | 53 | ENGJ (0.40, 6, 3) | Standard 157, Fundamentals 18, Inquiry 6 | floor ok |
| 84 | `body:alert:side` | `ABSENT-notWT` | 173 | 90 | 59 | MXEX (0.50, 9, 3) | Standard 126, Fundamentals 29, Bilingual 17 | not derivable |
| 85 | `header:other` | `OTHER-PAGE` | 170 | 141 | 46 | ANZH (0.23, 23, 4) | Standard 159, Bilingual 9, Inquiry 2 | floor ok |
| 86 | `menu:Information` | `menu:Overview` | 168 | 16 | 16 | MXDI (0.33, 28, 3) | Standard 151, Bilingual 17 | floor ok |
| 87 | `body:widget:dragAndDrop` | `body:activity` | 166 | 33 | 28 | MXFL (0.10, 23, 4) | Standard 157, Bilingual 6, Fundamentals 3 | floor ok |
| 88 | `body:widget:flipCard` | `body:free` | 164 | 35 | 31 | SSFUN (0.21, 10, 3) | Standard 133, Fundamentals 31 | floor ok |
| 89 | `body:widget:tabs` | `OTHER-PAGE` | 164 | 15 | 11 |  | Standard 160, Fundamentals 4 | below floor |
| 90 | `menu:Overview` | `ABSENT-inWT` | 161 | 80 | 65 | GEO (0.11, 7, 3) | Standard 135, Fundamentals 16, Bilingual 6 | floor ok |
| 91 | `body:widget:radioQuiz` | `body:activity` | 161 | 28 | 21 | ANZH (0.62, 16, 3) | Standard 139, Fundamentals 22 | CANDIDATE |
| 92 | `body:free` | `body:widget:carousel` | 161 | 36 | 33 | AGH (0.02, 23, 3) | Standard 128, Fundamentals 33 | floor ok |
| 93 | `body:widget:speechBubble` | `body:free` | 158 | 86 | 53 | TEFUN (0.23, 12, 4) | Standard 113, Fundamentals 30, Bilingual 8 | floor ok |
| 94 | `menu:Information` | `ABSENT-inWT` | 157 | 80 | 68 | OSGM (0.29, 6, 3) | Standard 151, Bilingual 4, Inquiry 2 | floor ok |
| 95 | `body:alert` | `OTHER-PAGE` | 155 | 58 | 33 | TRR (0.25, 62, 4) | Standard 93, Bilingual 62 | floor ok |
| 96 | `body:activity` | `body:widget:accordion` | 155 | 35 | 31 | BLL (0.01, 19, 13) | Standard 142, Fundamentals 12, Inquiry 1 | floor ok |
| 97 | `menu:LI` | `menu:Overview` | 153 | 12 | 12 | XMES (0.98, 61, 3) | Standard 103, Bilingual 43, Inquiry 6 | CANDIDATE |
| 98 | `body:panel:widget:dragAndDrop` | `body:panel:widget:cv2-interactive` | 147 | 20 | 20 | CEDO (0.91, 31, 3) | Inquiry 147 | un-built widget (A1) |
| 99 | `body:free:side` | `body:free` | 146 | 51 | 41 | HIS (0.77, 30, 6) | Standard 98, Fundamentals 46, Inquiry 2 | CANDIDATE |
| 100 | `header:other` | `ABSENT-inWT` | 142 | 136 | 71 | PES (0.36, 17, 5) | Standard 133, Inquiry 7, Fundamentals 2 | floor ok |
| 101 | `body:widget:hintSlider` | `body:widget:cv2-interactive` | 141 | 21 | 18 | ENFUN (0.21, 15, 3) | Standard 116, Fundamentals 25 | un-built widget (A1) |
| 102 | `body:widget:accordion` | `body:widget:carousel` | 137 | 17 | 11 |  | Standard 137 | below floor |
| 103 | `body:panel:free` | `body:panel:activity` | 131 | 27 | 27 | BLL (0.23, 28, 8) | Inquiry 131 | floor ok |
| 104 | `body:panel:widget:accordion` | `body:panel:widget:cv2-interactive` | 127 | 11 | 11 |  | Inquiry 125, Standard 2 | un-built widget (A1) |
| 105 | `body:panel:widget:multiChoiceQuiz` | `body:panel:widget:cv2-interactive` | 126 | 9 | 9 | TWHA (0.25, 60, 3) | Inquiry 126 | un-built widget (A1) |
| 106 | `body:free` | `header:other` | 123 | 123 | 50 | ANZH (0.03, 16, 4) | Standard 120, Inquiry 3 | floor ok |
| 107 | `body:widget:typing` | `body:activity` | 120 | 34 | 25 | MXDI (0.16, 28, 3) | Standard 118, Fundamentals 2 | floor ok |
| 108 | `body:widget:radioQuiz` | `ABSENT-inWT` | 119 | 22 | 22 | HPFUN (0.41, 28, 3) | Standard 73, Fundamentals 37, Inquiry 9 | floor ok |
| 109 | `body:free:side` | `ABSENT-notWT` | 119 | 43 | 36 | XDLS (0.35, 7, 3) | Standard 91, Fundamentals 26, Inquiry 2 | not derivable |
| 110 | `body:alert:side` | `ABSENT-inWT` | 118 | 61 | 46 | MXFU (0.50, 22, 3) | Standard 102, Fundamentals 11, Bilingual 5 | floor ok |
| 111 | `body:widget:accordion` | `body:alert` | 118 | 25 | 16 | XDLS (0.01, 8, 5) | Standard 117, Inquiry 1 | floor ok |
| 112 | `body:alert` | `body:widget:cv2-interactive` | 117 | 55 | 43 | ENFUN (0.09, 10, 5) | Standard 79, Fundamentals 28, Bilingual 10 | floor ok |
| 113 | `menu:Information` | `menu:Practices` | 117 | 18 | 9 | BLL (0.35, 66, 7) | Standard 117 | below floor |
| 114 | `body:widget:radioQuiz` | `ABSENT-notWT` | 114 | 20 | 18 | AGH (0.26, 19, 3) | Standard 102, Bilingual 11, Fundamentals 1 | not derivable |
| 115 | `body:panel:widget:multiChoiceQuiz` | `ABSENT-inWT` | 113 | 8 | 8 | TWHA (0.36, 85, 4) | Inquiry 113 | below floor |
| 116 | `body:widget:memoryGame` | `body:widget:cv2-interactive` | 113 | 22 | 19 |  | Standard 89, Fundamentals 12, Bilingual 12 | un-built widget (A1) |
| 117 | `body:widget:reorder` | `ABSENT-inWT` | 112 | 30 | 23 |  | Standard 100, Fundamentals 12 | floor ok |
| 118 | `body:panel:widget:flipCard` | `ABSENT-notWT` | 109 | 7 | 7 | TWHA (0.44, 90, 4) | Inquiry 109 | not derivable |
| 119 | `menu:LI` | `menu:Information` | 108 | 5 | 5 | TRR (0.41, 108, 5) | Bilingual 108 | below floor |
| 120 | `body:widget:wordHighlighter` | `ABSENT-notWT` | 105 | 24 | 22 | ENFUN (0.31, 22, 4) | Standard 60, Fundamentals 45 | not derivable |
| 121 | `body:panel:widget:multiChoiceQuiz` | `ABSENT-notWT` | 105 | 7 | 7 | TWHA (0.39, 94, 4) | Inquiry 97, Standard 8 | not derivable |
| 122 | `body:panel:widget:tabs` | `ABSENT-notWT` | 105 | 3 | 2 |  | Standard 105 | not derivable |
| 123 | `body:widget:selfCheck` | `body:widget:cv2-interactive` | 104 | 31 | 20 | BLL (0.71, 10, 3) | Standard 93, Bilingual 6, Fundamentals 4 | un-built widget (A1) |
| 124 | `body:widget:hintSlider` | `body:widget:flipCard` | 103 | 7 | 5 | ENFUN (0.30, 21, 4) | Standard 82, Fundamentals 21 | below floor |
| 125 | `body:panel:widget:flipCard` | `body:panel:widget:cv2-interactive` | 100 | 13 | 13 |  | Inquiry 100 | un-built widget (A1) |
| 126 | `body:panel:widget:flipCard` | `ABSENT-inWT` | 100 | 7 | 7 | TWHA (0.21, 43, 4) | Inquiry 100 | below floor |
| 127 | `menu:Standards` | `ABSENT-notWT` | 92 | 42 | 40 | GEO (0.40, 4, 3) | Standard 89, Inquiry 3 | not derivable |
| 128 | `body:free` | `body:widget:flipCard` | 92 | 14 | 13 | XLP (0.03, 12, 3) | Standard 60, Fundamentals 32 | below floor |
| 129 | `body:activity` | `body:widget:flipCard` | 92 | 11 | 8 |  | Standard 85, Inquiry 7 | below floor |
| 130 | `body:widget:tabs` | `body:widget:carousel` | 92 | 10 | 6 |  | Standard 68, Fundamentals 24 | below floor |
| 131 | `body:widget:selfCheck` | `ABSENT-inWT` | 91 | 26 | 21 |  | Standard 70, Inquiry 14, Fundamentals 7 | floor ok |
| 132 | `body:widget:dropQuiz` | `body:activity` | 89 | 15 | 14 | HPFUN (0.28, 30, 4) | Fundamentals 45, Standard 44 | below floor |
| 133 | `body:alert:side` | `body:free` | 88 | 43 | 35 | ENGI (0.17, 5, 3) | Standard 64, Fundamentals 18, Bilingual 6 | floor ok |
| 134 | `body:widget:tabs` | `body:alert` | 86 | 7 | 5 |  | Standard 86 | below floor |
| 135 | `other:free` | `body:free` | 86 | 5 | 5 |  | Standard 86 | below floor |
| 136 | `menu:pane2` | `menu:Overview` | 86 | 7 | 7 | XMES (1.00, 45, 3) | Standard 64, Bilingual 22 | below floor |
| 137 | `body:widget:multiChoiceQuiz` | `OTHER-PAGE` | 85 | 13 | 11 |  | Standard 65, Bilingual 20 | below floor |
| 138 | `body:widget:wordHighlighter` | `body:widget:cv2-interactive` | 84 | 18 | 17 | BLL (0.35, 15, 3) | Standard 45, Fundamentals 39 | un-built widget (A1) |
| 139 | `body:free:side` | `ABSENT-inWT` | 78 | 30 | 29 |  | Standard 75, Fundamentals 2, Inquiry 1 | floor ok |
| 140 | `menu:Standards` | `ABSENT-inWT` | 78 | 53 | 46 | XDLS (0.34, 20, 8) | Standard 68, Inquiry 10 | floor ok |
| 141 | `body:alert:side` | `body:activity` | 78 | 35 | 19 | TRR (0.48, 29, 3) | Standard 48, Bilingual 29, Fundamentals 1 | floor ok |
| 142 | `body:alert` | `body:alert:side` | 78 | 42 | 28 | BLL (0.13, 4, 4) | Standard 63, Fundamentals 15 | floor ok |
| 143 | `body:widget:dropQuiz` | `body:free` | 78 | 11 | 11 |  | Fundamentals 41, Standard 27, Bilingual 10 | below floor |
| 144 | `body:panel:widget:carousel` | `ABSENT-inWT` | 76 | 12 | 12 | BLL (0.86, 42, 3) | Inquiry 71, Standard 5 | below floor |
| 145 | `body:widget:hintSlider` | `ABSENT-notWT` | 75 | 16 | 14 |  | Standard 56, Fundamentals 19 | not derivable |
| 146 | `body:widget:wordSelect` | `body:activity` | 72 | 20 | 19 | WJFUN (0.56, 30, 4) | Standard 35, Fundamentals 33, Bilingual 4 | floor ok |
| 147 | `body:widget:wordSelect` | `ABSENT-inWT` | 71 | 19 | 16 |  | Fundamentals 37, Standard 33, Bilingual 1 | below floor |
| 148 | `body:widget:tabs` | `body:activity` | 70 | 11 | 10 | HIS (0.12, 20, 3) | Standard 69, Fundamentals 1 | below floor |
| 149 | `body:free` | `menu:flat` | 68 | 11 | 11 |  | Fundamentals 48, Standard 13, Inquiry 7 | floor ok |
| 150 | `body:widget:selfCheck` | `ABSENT-notWT` | 67 | 12 | 10 |  | Fundamentals 35, Standard 26, Bilingual 6 | not derivable |

## 2. Headings only (the SECTIONS) — gold region → Claude region / fate

| gold region | Claude region / fate | headings | pages | modules | examples |
|---|---|---:|---:|---:|---|
| `body:activity` | `ABSENT-notWT` | 801 | 454 | 198 | AGH1001 AGH1001_1_0.html <h3>→<—> “What are primary products?”; AGH1001 AGH1001_1_0.html <h3>→<—> “Agricultural and horticultural products”; AGH1001 AGH1001_2_0.html <h3>→<—> “Value of Primary Products” |
| `body:activity` | `ABSENT-inWT` | 495 | 349 | 193 | AGH1001 AGH1001_3_0.html <h3>→<—> “Māori creation story”; AGH1001 AGH1001_4_0.html <h3>→<—> “New Zealand’s four seasons”; AGH1002 AGH1002_6_0.html <h3>→<—> “Levels of organic matter” |
| `body:activity` | `body:free` | 401 | 235 | 146 | AGH1001 AGH1001_3_0.html <h3>→<h3> “Self Check: True or False”; AGH1004 AGH1004_1_0.html <h3>→<h3> “Knowledge self-check”; AGH1004 AGH1004_2_0.html <h3>→<h3> “Reflective questions” |
| `body:free` | `ABSENT-notWT` | 366 | 204 | 119 | AGH1001 AGH1001_2_0.html <h4>→<—> “Pre-European settlement”; AGH1001 AGH1001_2_0.html <h4>→<—> “Late 18th Century - Mid 19th Century”; AGH1001 AGH1001_2_0.html <h4>→<—> “Late 19th Century - Mid 20th Century” |
| `body:activity` | `body:widget:cv2-interactive` | 354 | 189 | 103 | ANZH203 ANZH203_1_0.html <h3>→<p> “Comprehension activity”; ARFUN02 ARFUN02_0_0.html <h3>→<p> “What Have I Learned? He aha aku i ako ai?”; ARFUN03 ARFUN03_0_0.html <h3>→<p> “What have I learnt?” |
| `body:widget:accordion` | `ABSENT-notWT` | 313 | 80 | 56 | AGH1003 AGH1003_4_0.html <h4>→<—> “Returning crop residues”; AGH1003 AGH1003_7_0.html <h4>→<—> “What causes poor drainage?”; AGH1003 AGH1003_7_0.html <h5>→<—> “This open drain is an example of surface drainage.” |
| `menu:flat` | `ABSENT-inWT` | 312 | 293 | 80 | AGH1001 AGH1001_1_0.html <h5>→<—> “We are learning to:”; AGH1001 AGH1001_2_0.html <h5>→<—> “We are learning to:”; AGH1001 AGH1001_3_0.html <h5>→<—> “We are learning to:” |
| `body:free` | `ABSENT-inWT` | 292 | 182 | 132 | AGH1001 AGH1001_0_0.html <h3>→<—> “An introduction to agricultural and horticultural ”; AGH1002 AGH1002_3_0.html <h4>→<—> “C = carbon, H = Hydrogen, O = Oxygen”; AGH1005 AGH1005_6_0.html <h4>→<—> “Mycorrhizal associations” |
| `body:widget:accordion` | `ABSENT-inWT` | 238 | 109 | 78 | AGH1003 AGH1003_4_0.html <h4>→<—> “Slurry Tankers/Umbilical Systems”; AGH1005 AGH1005_2_0.html <h4>→<—> “Disease and pest resistance”; AGH1005 AGH1005_2_0.html <h4>→<—> “Breeding and selection” |
| `header:other` | `ABSENT-notWT` | 221 | 206 | 110 | AGH1004 AGH1004_1_0.html <h1>→<—> “Factors influencing where primary production syste”; AGH1004 AGH1004_5_0.html <h1>→<—> “Where does our water come from?”; AGH1004 AGH1004_6_0.html <h1>→<—> “Market Factor Influences” |
| `body:widget:accordion` | `body:widget:cv2-interactive` | 212 | 77 | 63 | AGH1008 AGH1008_3_0.html <h4>→<td> “Forward/creep grazing”; AGH1009 AGH1009_1_0.html <h5>→<td> “Cultural recognition (Cultural recognition princip”; AGH1009 AGH1009_1_0.html <h5>→<td> “Sustainable Resource Management (Sustainable Resou” |
| `body:activity` | `OTHER-PAGE` | 196 | 132 | 56 | ANZH301 ANZH301_1_0.html <h4>→<—> “Go to your journal”; ANZH303 ANZH303_4_0.html <h4>→<—> “Go to your journal”; ANZH303 ANZH303_6_0.html <h4>→<—> “Go to your journal” |
| `menu:flat` | `ABSENT-notWT` | 185 | 185 | 63 | ARFUN01 ARFUN01_0_0.html <h5>→<—> “You will show your understanding by:”; ARFUN02 ARFUN02_0_0.html <h5>→<—> “You will show your understanding by:”; ARFUN03 ARFUN03_0_0.html <h5>→<—> “You will show your understanding by:” |
| `header:other` | `OTHER-PAGE` | 170 | 141 | 46 | AGH1007 AGH1007_7_0.html <h1>→<—> “Livestock and Agriculture in Aotearoa New Zealand”; AGH1009 AGH1009_8_0.html <h1>→<—> “Primary production and soil quality.”; ANZH101 ANZH101_1_0.html <h1>→<—> “Tangata Whenua Origin Stories” |
| `body:free` | `body:widget:cv2-interactive` | 148 | 75 | 61 | AGH1002 AGH1002_3_0.html <h4>→<th> “Air level in soil”; AGH1006 AGH1006_4_0.html <h3>→<p> “Protective Structures”; AGH1009 AGH1009_1_0.html <h4>→<th> “European world view (Colonial times)” |
| `header:other` | `ABSENT-inWT` | 142 | 136 | 71 | AGH1001 AGH1001_0_0.html <h1>→<—> “From the Ground Up”; AGH1001 AGH1001_0_0.html <h1>→<—> “Mai i te Nuku ki te Rangi”; AGH1002 AGH1002_4_0.html <h1>→<—> “Physical properties of soil” |
| `body:free` | `body:activity` | 138 | 107 | 73 | AGH1003 AGH1003_3_0.html <h3>→<p> “Flowers and fertilisers”; AGH1004 AGH1004_5_0.html <h3>→<h3> “Impact of Irrigation on Production”; AGH1005 AGH1005_7_0.html <h3>→<p> “Common pests and diseases” |
| `body:widget:accordion` | `body:free` | 130 | 52 | 40 | AGH1004 AGH1004_2_0.html <h4>→<h4> “Semi-intensive Farming”; AGH1004 AGH1004_2_0.html <h4>→<h4> “Semi-extensive Farming”; AGH1006 AGH1006_6_0.html <h4>→<h3> “Integrated weed management” |
| `menu:flat` | `OTHER-PAGE` | 130 | 104 | 21 | ANZH203 ANZH203_1_0.html <h4>→<—> “How will I know if I’ve learned it?”; ANZH203 ANZH203_2_0.html <h4>→<—> “How will I know if I’ve learned it?”; ANZH203 ANZH203_3_0.html <h4>→<—> “How will I know if I’ve learned it?” |
| `body:free` | `header:other` | 121 | 121 | 48 | AGH1005 AGH1005_0_0.html <h3>→<h1> “Ko te tūhura i te tipu me te tukanga i Aotearoa | ”; AGH1005 AGH1005_2_0.html <h3>→<h1> “Exploring plant anatomy and its impact on primary ”; AGH1005 AGH1005_5_0.html <h3>→<h1> “Exploring the plant process of respiration and its” |
| `body:widget:flipCard` | `ABSENT-inWT` | 109 | 39 | 33 | CEDO502 CEDO502_1_1.html <h5>→<—> “Credit card shopping”; CEDR501 CEDR501_4_0.html <h4>→<—> “Pānui 1: Aiko arrives early”; CEDR501 CEDR501_4_0.html <h4>→<—> “Pānui 2: Taika is late” |
| `body:alert` | `body:free` | 92 | 75 | 51 | AGH1003 AGH1003_5_0.html <h4>→<p> “Why is it important to add lime before fertiliser ”; AGH1009 AGH1009_4_0.html <h4>→<p> “A note on sprays”; ANZH103 ANZH103_1_0.html <h3>→<h3> “What happened after the Treaty was signed on 6 Feb” |
| `body:widget:carousel` | `ABSENT-inWT` | 83 | 33 | 27 | ANZH105 ANZH105_6_0.html <h4>→<—> “New Zealand Māori Kapa haka”; ANZH303 ANZH303_5_0.html <h4>→<—> “The Eight-pointed Stars”; BLL262 BLL262_3_0.html <h5>→<—> “Pointillism Fish Part 1” |
| `body:panel:activity` | `ABSENT-notWT` | 75 | 31 | 29 | BLL120 BLL120_0_0.html <h3>→<—> “Writing words with the digraph ck”; BLL250 BLL250_0_0.html <h4>→<—> “Ben the Lamb and the Gentle Climb”; BLL250 BLL250_0_0.html <h4>→<—> “The Sleigh in the Snow” |
| `body:panel:activity` | `body:panel:free` | 75 | 22 | 22 | BLL240 BLL240_0_0.html <h4>→<h5> “Words making the 'ear' sound”; BLL240 BLL240_0_0.html <h4>→<h5> “Words making the 'air' sound”; BLL240 BLL240_0_0.html <h4>→<h5> “Words making the 'ur' sound” |
| `body:widget:carousel` | `ABSENT-notWT` | 74 | 25 | 19 | AGH1009 AGH1009_2_0.html <h4>→<—> “Decomposition and fossilisation”; AGH1009 AGH1009_2_0.html <h4>→<—> “Ocean Sedimentationand Absorption”; ART1006 ART1006_1_0.html <h4>→<—> “PowerPoint/slideshow presentations” |
| `menu:Information` | `ABSENT-notWT` | 73 | 64 | 58 | AGH1001 AGH1001_0_0.html <h5>→<—> “Want to know where to start?”; AGH1002 AGH1002_0_0.html <h5>→<—> “Want to know where to start?”; AGH1003 AGH1003_0_0.html <h5>→<—> “Want to know where to start?” |
| `body:alert` | `ABSENT-notWT` | 72 | 54 | 29 | AGH1007 AGH1007_3_0.html <h4>→<—> “Key points from the lesson:”; AGH1007 AGH1007_4_0.html <h4>→<—> “Key points from the lesson:”; AGH1007 AGH1007_5_0.html <h4>→<—> “Key points from the lesson:” |
| `body:free` | `OTHER-PAGE` | 69 | 31 | 24 | AGH1005 AGH1005_4_0.html <h3>→<—> “Exploring the plant process of transpiration”; CBI1009 CBI1009_1_0.html <h2>→<—> “Soluble and insoluble Salts”; CEDO501 CEDO501_3_0.html <h3>→<—> “Search engines and Artificial Intelligence” |
| `body:widget:flipCard` | `body:widget:cv2-interactive` | 68 | 22 | 18 | ANZH105 ANZH105_5_0.html <h4>→<td> “What is it made of?”; ANZH105 ANZH105_5_0.html <h4>→<td> “Where is it from?”; ANZH105 ANZH105_5_0.html <h4>→<td> “How old is it?” |
| `body:alert` | `ABSENT-inWT` | 62 | 50 | 35 | AGH1003 AGH1003_1_0.html <h4>→<—> “Need some extra help?”; ANZH301 ANZH301_7_0.html <h4>→<—> “Want to know more?”; ANZH301 ANZH301_9_0.html <h4>→<—> “Some other examples of urban marae:” |
| `body:panel:activity` | `ABSENT-inWT` | 61 | 25 | 24 | BLL120 BLL120_0_0.html <h3>→<—> “Writing the letter k”; BLL120 BLL120_0_0.html <h3>→<—> “My name is, my sound is…”; BLL160 BLL160_0_0.html <h4>→<—> “A child was in bed sleeping. A duck ran in the doo” |
| `menu:Information` | `ABSENT-inWT` | 56 | 45 | 43 | BLL251 BLL251_0_0.html <h4>→<—> “Tirohanga Whānui | Overview”; BLL255 BLL255_0_0.html <h4>→<—> “Tirohanga Whānui | Overview”; BLL257 BLL257_0_0.html <h4>→<—> “Tirohanga Whānui | Overview” |
| `body:panel:widget:accordion` | `body:panel:free` | 55 | 12 | 12 | CEDK401 CEDK401_0_0.html <h4>→<h4> “Go to your journal”; CEDK401 CEDK401_0_0.html <h4>→<h4> “Go to your journal”; CEDK401 CEDK401_0_0.html <h4>→<h4> “Go to your journal” |
| `header:other` | `body:free` | 54 | 49 | 38 | AGH1006 AGH1006_8_0.html <h1>→<h3> “Pest and disease management”; ANZH301 ANZH301_1_0.html <h1>→<h3> “Life before, during and after the Second World War”; ANZH303 ANZH303_4_0.html <h1>→<h3> “Innovation, Interactions and Mana.” |
| `body:panel:free` | `ABSENT-inWT` | 53 | 21 | 19 | CEDK101 CEDK101_0_0.html <h2>→<—> “Light and technology”; CEDO202 CEDO202_0_0.html <h2>→<—> “Creating and sharing your dance”; CEDO204 CEDO204_0_0.html <h4>→<—> “Beaver dams and lodges” |
| `body:widget:wordHighlighter` | `body:free` | 45 | 10 | 10 | ENFUN01 ENFUN01_0_0.html <h3>→<h5> “Why is knowing about author’s purpose important?”; ENFUN04 ENFUN04_0_0.html <h3>→<h5> “Homophones, homonyms and homographs”; ENFUN05 ENFUN05_0_0.html <h3>→<h3> “Full stops, capital letters, exclamation marks” |
| `body:widget:tabs` | `ABSENT-inWT` | 44 | 19 | 15 | AGH1001 AGH1001_2_0.html <h5>→<—> “Mussel Farmer – Jake Bartram, Hauraki Gulf New Zea”; ENGS201 ENGS201_4_0.html <h5>→<—> “Write a what if scenario.”; ENGS201 ENGS201_4_0.html <h5>→<—> “Imagine you are a superhero!” |
| `body:widget:tabs` | `body:widget:cv2-interactive` | 44 | 19 | 16 | ANZH203 ANZH203_6_0.html <h4>→<p> “Charles Heaphy: Artist, Draughtsman and Explorer”; ENGC301 ENGC301_1_0.html <h4>→<th> “Static advertisement”; ENGC301 ENGC301_7_0.html <h4>→<th> “Static advertisement” |
| `body:widget:carousel` | `body:widget:cv2-interactive` | 44 | 16 | 14 | BLL271 BLL271_1_0.html <h4>→<td> “pa / ki / hi / wi”; CEDO502 CEDO502_5_0.html <h5>→<p> “Use keywords carefully”; CEDO502 CEDO502_5_0.html <h5>→<p> “Use headings and subheadings” |
| `menu:Overview` | `ABSENT-notWT` | 40 | 36 | 35 | BLL253 BLL253_0_0.html <h4>→<—> “How will I know if I've learned it?”; BLL271 BLL271_0_0.html <h4>→<—> “How will I know I have learned it?”; BLL273 BLL273_0_0.html <h4>→<—> “How will I know if I've learned it?” |
| `body:panel:free` | `ABSENT-notWT` | 40 | 13 | 9 | CEDR101 CEDR101_0_0.html <h3>→<—> “TLearning from friends and whānau”; CEDR101 CEDR101_0_0.html <h3>→<—> “Who is leading the score?”; CEDR203 CEDR203_0_0.html <h2>→<—> “Aotearoa New Zealand Eco-leaders” |
| `body:widget:tabs` | `body:free` | 35 | 16 | 16 | AGH1001 AGH1001_2_0.html <h5>→<p> “Farm Advisor – Ash Phillips, Wairoa New Zealand”; ANZH203 ANZH203_6_0.html <h4>→<p> “Thomas Brunner: Surveyor and Explorer”; ENGC403 ENGC403_12_0.html <h4>→<h5> “Oral presentation part” |
| `menu:flat` | `body:free` | 33 | 21 | 13 | BLL124 BLL124_0_0.html <h5>→<h4> “Whāinga Ako | Learning Intentions”; BLL124 BLL124_0_0.html <h5>→<h4> “Paearu Angitu | How will I know if I’ve learned it”; CBI1008 CBI1008_1_0.html <h5>→<h3> “We are learning about:” |
| `body:activity:side` | `ABSENT-notWT` | 32 | 12 | 4 | TEDC402 TEDC402_8_0.html <h5>→<—> “Spot the issue A”; TRR115 TRR115_2_0.html <h4>→<—> “A - re - wha - na”; XTAS102 XTAS102_1_0.html <h5>→<—> “Not fun. Too hard.” |
| `body:widget:flipCard` | `ABSENT-notWT` | 31 | 16 | 16 | CHFUN05 CHFUN05_0_0.html <h5>→<—> “我不吃。wǒ bù chīI don’t eat.”; CHFUN05 CHFUN05_0_0.html <h5>→<—> “你不喜欢。nǐ bù xǐhuānYou don’t like it.”; CHFUN05 CHFUN05_0_0.html <h5>→<—> “然后ránhòuafterwards / after that” |
| `body:widget:accordion` | `body:activity` | 29 | 11 | 9 | AGH1008 AGH1008_5_0.html <h4>→<h5> “Increased chance of pregnancy”; AGH1008 AGH1008_5_0.html <h4>→<h5> “Increased production through better genetic select”; AGH1008 AGH1008_5_0.html <h4>→<h5> “Reduced need for having a bull on farm” |
| `body:free:side` | `ABSENT-inWT` | 24 | 11 | 11 | ART1002 ART1002_0_0.html <h5>→<—> “Wrecking the White Page”; ART1002 ART1002_0_0.html <h5>→<—> “The Visual Arts Diary”; DTC1005 DTC1005_1_0.html <h3>→<—> “Digital Outcome Domain of your choice” |
| `body:activity` | `body:alert` | 23 | 9 | 5 | AGH1001 AGH1001_5_0.html <h3>→<li> “Management Practices on a Production System”; ENGS102 ENGS102_6_0.html <h4>→<p> “The girl was in the woods.”; ENGS302 ENGS302_6_0.html <h3>→<h5> “What is a timetable?” |
| `body:widget:carousel` | `body:free` | 22 | 11 | 11 | ANZH105 ANZH105_6_0.html <h4>→<h4> “Cook Island Māori drumming and dancing”; DAN1006 DAN1006_6_0.html <h4>→<h4> “Whole dance with cues”; DAN1006 DAN1006_6_0.html <h4>→<h4> “Whole dance facing the front with music” |
| `body:free` | `body:widget:carousel` | 21 | 14 | 14 | ANZH205 ANZH205_7_0.html <h3>→<h4> “What can we do to honour te titiri?”; ARFUN02 ARFUN02_0_0.html <h4>→<h4> “How to understand it:”; ENFUN03 ENFUN03_0_0.html <h3>→<h4> “Adverb sentence starters” |
| `body:widget:tabs` | `ABSENT-notWT` | 21 | 12 | 11 | ART1006 ART1006_1_0.html <h5>→<—> “(this is where others can input into your idea)”; ENG1005 ENG1005_0_0.html <h5>→<—> “Demonstrate perceptive understanding of studied te”; HES1002 HES1002_7_0.html <h4>→<—> “Va, Va'a or Vaha” |
| `body:widget:flipCard` | `body:free` | 21 | 8 | 8 | BLLR202 BLLR202_4_0.html <h5>→<td> “Read between the lines”; CHFUN05 CHFUN05_0_0.html <h5>→<td> “我吃。wǒ chī.I eat.”; CHFUN05 CHFUN05_0_0.html <h5>→<td> “他去。tā qù.He is going.” |
| `body:activity` | `body:widget:flipCard` | 21 | 4 | 2 | ENGI102 ENGI102_2_0.html <h4>→<p> “Dress-up or Puppet Play”; ENGI102 ENGI102_2_0.html <h4>→<p> “Make a picture of a scene in the story”; ENGI102 ENGI102_2_0.html <h4>→<p> “Create an important item from the fairytale out of” |
| `menu:LI` | `menu:Overview` | 21 | 9 | 9 | MXS1004 MXS1004_0_0.html <h5>→<h4> “Whāinga Ako | Learning Intentions”; MXS1004 MXS1004_0_0.html <h5>→<h4> “Paearu Angitu | How will I know if I’ve learned it”; PMT101 PMT101_0_0.html <h5>→<td> “Kei te ako au kia:” |
| `menu:LI` | `menu:Information` | 21 | 5 | 5 | TRR103 TRR103_0_0.html <h5>→<h5> “Whakamaheretia tō wā:”; TRR103 TRR103_0_0.html <h5>→<h5> “He aha tāku hei tīmata?”; TRR103 TRR103_0_0.html <h5>→<h5> “What do I need to get started?” |
| `body:panel:activity` | `body:panel:widget:cv2-interactive` | 20 | 10 | 10 | BLL120 BLL120_0_0.html <h3>→<p> “Where is the /k/ sound?”; BLL210 BLL210_0_0.html <h5>→<th> “Uses one of these things:”; CEDK102 CEDK102_0_0.html <h4>→<p> “How to change your MTK profile picture” |
| `body:panel:free` | `body:panel:activity` | 20 | 10 | 10 | BLL250 BLL250_0_0.html <h2>→<h3> “The 'augh' letter team”; CEDK101 CEDK101_0_0.html <h3>→<h3> “How does light travel?”; CEDK101 CEDK101_0_0.html <h3>→<h3> “Light reflection and refraction” |
| `body:widget:accordion` | `body:widget:carousel` | 19 | 5 | 5 | AGH1005 AGH1005_7_0.html <h5>→<li> “Powdery mildew (various species):”; AGH1005 AGH1005_7_0.html <h5>→<li> “Rust diseases (various species):”; AGH1005 AGH1005_7_0.html <h5>→<li> “Tomato yellow leaf curl virus (TYLCV):” |
| `menu:Overview` | `OTHER-PAGE` | 19 | 19 | 6 | ENGJ201 ENGJ201_1_0.html <h3>→<—> “How will I know if I’ve learned it?”; ENGJ201 ENGJ201_2_0.html <h3>→<—> “How will I know if I’ve learned it?”; ENGJ201 ENGJ201_3_0.html <h3>→<—> “How will I know if I’ve learned it?” |

## 3. Region agreement — of the gold's blocks in region A that Claude has on the paired page, the share it keeps in A

| gold region | matched on page | kept in region | moved | agreement |
|---|---:|---:|---:|---:|
| `body:free` | 24003 | 20191 | 3812 | 0.841 |
| `body:activity` | 18256 | 11901 | 6355 | 0.652 |
| `menu:flat` | 7743 | 7335 | 408 | 0.947 |
| `body:widget:accordion` | 6235 | 3009 | 3226 | 0.483 |
| `body:widget:dragAndDrop` | 4009 | 328 | 3681 | 0.082 |
| `acks` | 3949 | 3939 | 10 | 0.997 |
| `body:alert` | 3630 | 1870 | 1760 | 0.515 |
| `menu:Overview` | 3371 | 3258 | 113 | 0.966 |
| `body:panel:activity` | 3343 | 2149 | 1194 | 0.643 |
| `body:widget:multiChoiceQuiz` | 3320 | 126 | 3194 | 0.038 |
| `body:panel:free` | 3049 | 2601 | 448 | 0.853 |
| `body:widget:flipCard` | 2159 | 1139 | 1020 | 0.528 |
| `body:widget:carousel` | 2137 | 1180 | 957 | 0.552 |
| `menu:Information` | 2130 | 1478 | 652 | 0.694 |
| `body:widget:tabs` | 2066 | 508 | 1558 | 0.246 |
| `body:widget:speechBubble` | 1364 | 960 | 404 | 0.704 |
| `header:other` | 1340 | 1271 | 69 | 0.949 |
| `body:widget:dropQuiz` | 881 | 81 | 800 | 0.092 |
| `body:panel:widget:accordion` | 829 | 371 | 458 | 0.448 |
| `body:widget:radioQuiz` | 715 | 0 | 715 | 0.000 |
| `body:widget:typing` | 699 | 21 | 678 | 0.030 |
| `body:widget:wordHighlighter` | 598 | 0 | 598 | 0.000 |
| `body:widget:reorder` | 591 | 0 | 591 | 0.000 |
| `body:alert:side` | 541 | 125 | 416 | 0.231 |
| `body:widget:hintSlider` | 493 | 188 | 305 | 0.381 |
| `menu:pane2` | 410 | 253 | 157 | 0.617 |
| `menu:LI` | 399 | 131 | 268 | 0.328 |
| `body:widget:dropDown` | 363 | 60 | 303 | 0.165 |
| `menu:Standards` | 361 | 331 | 30 | 0.917 |
| `menu:pane3` | 352 | 228 | 124 | 0.648 |
| `menu:Knowledge` | 334 | 310 | 24 | 0.928 |
| `body:free:side` | 240 | 39 | 201 | 0.163 |
| `body:panel:widget:dragAndDrop` | 223 | 35 | 188 | 0.157 |
| `body:panel:widget:carousel` | 221 | 132 | 89 | 0.597 |
| `body:panel:widget:flipCard` | 201 | 65 | 136 | 0.323 |
| `body:widget:selfCheck` | 197 | 0 | 197 | 0.000 |
| `menu:Practices` | 187 | 186 | 1 | 0.995 |
| `other:free` | 180 | 0 | 180 | 0.000 |
| `body:panel:widget:multiChoiceQuiz` | 172 | 29 | 143 | 0.169 |
| `body:panel:alert` | 165 | 104 | 61 | 0.630 |

## 5. ORDER — blocks Claude places in a different order than the human (same page; session 42 Round 11)

Every gold block matched on the paired page, in gold order, carries its Claude position; the blocks outside the longest increasing subsequence of those positions are the ones in a different ORDER (a whole section moved, an introduction after a note, a lead after its list). Regions first, then the recurring blocks by modules (a text that moves in many modules is a systematic placement rule; `before` = the gold block it should precede).

| gold region | matched | out of order | share | pages | modules |
|---|---:|---:|---:|---:|---:|
| `body:free` | 24003 | 856 | 0.036 | 373 | 213 |
| `body:activity` | 18256 | 839 | 0.046 | 345 | 187 |
| `menu:flat` | 7743 | 93 | 0.012 | 56 | 43 |
| `body:widget:accordion` | 6235 | 200 | 0.032 | 62 | 51 |
| `body:widget:dragAndDrop` | 4009 | 732 | 0.183 | 204 | 147 |
| `acks` | 3949 | 158 | 0.040 | 67 | 67 |
| `body:alert` | 3630 | 184 | 0.051 | 118 | 76 |
| `menu:Overview` | 3371 | 115 | 0.034 | 31 | 31 |
| `body:panel:activity` | 3343 | 245 | 0.073 | 38 | 38 |
| `body:widget:multiChoiceQuiz` | 3320 | 245 | 0.074 | 65 | 48 |
| `body:panel:free` | 3049 | 133 | 0.044 | 29 | 26 |
| `body:widget:flipCard` | 2159 | 79 | 0.037 | 31 | 28 |
| `body:widget:carousel` | 2137 | 90 | 0.042 | 38 | 35 |
| `menu:Information` | 2130 | 71 | 0.033 | 19 | 19 |
| `body:widget:tabs` | 2066 | 114 | 0.055 | 56 | 45 |
| `body:widget:speechBubble` | 1364 | 59 | 0.043 | 34 | 29 |
| `header:other` | 1340 | 43 | 0.032 | 41 | 35 |
| `body:widget:dropQuiz` | 881 | 48 | 0.054 | 25 | 22 |
| `body:panel:widget:accordion` | 829 | 55 | 0.066 | 10 | 10 |
| `body:widget:radioQuiz` | 715 | 14 | 0.020 | 9 | 9 |
| `body:widget:typing` | 699 | 20 | 0.029 | 11 | 11 |
| `body:widget:wordHighlighter` | 598 | 23 | 0.038 | 14 | 11 |
| `body:widget:reorder` | 591 | 131 | 0.222 | 32 | 23 |
| `body:alert:side` | 541 | 127 | 0.235 | 73 | 48 |
| `body:widget:hintSlider` | 493 | 25 | 0.051 | 3 | 2 |
| `menu:pane2` | 410 | 27 | 0.066 | 7 | 7 |
| `menu:LI` | 399 | 45 | 0.113 | 9 | 9 |
| `body:widget:dropDown` | 363 | 46 | 0.127 | 14 | 13 |
| `menu:Standards` | 361 | 7 | 0.019 | 5 | 5 |
| `menu:pane3` | 352 | 31 | 0.088 | 11 | 11 |

| block (tag: first words) | modules | pages | families | example: gold places it before … |
|---|---:|---:|---|---|
| `h4:go to your journal` | 42 | 85 | XGF 29, CEDK 20, CEDR 16, HES 16 | ANZH301 ANZH301_1_0.html: “Go to your journal” before “Māori involvement in the war effort also had anoth” |
| `li:decoding an unknown word with` | 15 | 15 | BLL 15 | BLL240 BLL240_0_0.html: “Decoding an unknown word (with one syllable) involves:” before “Identifying and recording phonemes in words includ” |
| `h3:he aha tāku i ako` | 7 | 11 | TRR 12, PMT 2, PNR 1 | PMT101 PMT101_3_0.html: “He aha tāku i ako ai?” before “Tohua ngā mea kua akona e koe mō te orangatonutang” |
| `li:identifying and recording phonemes in` | 6 | 6 | BLL 6 | BLL271 BLL271_0_0.html: “Identifying and recording phonemes in words, including:” before “Decoding words with less common graphemes or graph” |
| `h5:hei te mutunga o te` | 5 | 5 | TRR 5 | TRR102 TRR102_0_0.html: “Hei te mutunga o te tau:” before “By the end of the year:” |
| `p:take a photo of your` | 4 | 4 | BLL 5, ENGR 1, MXFL 1 | BLL110 BLL110_0_0.html: “Take a photo of your handwriting and upload it to show your ” before “Choose one or more of these activities to do. Clic” |
| `p:find things in your home` | 4 | 4 | BLL 13 | BLL110 BLL110_0_0.html: “Find things in your home or in your neighbourhood that have ” before “Draw some things that start with /t/ sound.” |
| `h4:what have i learned` | 4 | 4 | TRR 6, CEDT 1 | CEDT104 CEDT104_0_0.html: “What have I learned?” before “I know the words and signs for five body parts.” |
| `h3:check your understanding` | 4 | 4 | CHFUN 39, WJFUN 2 | CHFUN05 CHFUN05_0_0.html: “Check your understanding” before “Identify S, V, O. Select words that belong to thes” |
| `p:we are learning to` | 4 | 4 | ENFUN 4 | ENFUN01 ENFUN01_0_0.html: “We are learning to:” before “You will show your understanding by:” |
| `p:watch this video to learn` | 4 | 4 | MXFUN 4, MXDI 1, MXFU 1, XDLS 1 | MXDI103 MXDI103_3_0.html: “Watch this video to learn more about place value houses:” before “7 is a digit, but 12 is not as 12 has two digits i” |
| `p:whakarongo pīkarikari ki ēnei kupu` | 4 | 4 | TRR 4 | TRR110 TRR110_1_0.html: “Whakarongo pīkarikari ki ēnei kupu. Kātahi ka whakatau mēna ” before “Listen carefully to these words and decide if they” |
| `p:below are activities you can` | 3 | 19 | XDLS 19 | XDLS904 XDLS904_1_0.html: “Below are activities. You can choose the activities you feel” before “In this activity, you and your whānau will learn b” |
| `p:in this lesson you are` | 3 | 9 | ANZH 8, HIS 1 | ANZH401 ANZH401_6_0.html: “In this lesson you are learning to understand that data from” before “Conclusions about Early Migrants” |
| `p:email or phone the kaiako` | 3 | 8 | SSOG 5, XLP 2, XMES 1 | SSOG105 SSOG105_1_0.html: “Email or phone the kaiako. You can ring 0800 65 99 88 and as” before “Ka pai, detectives! Now I understand – some days a” |
| `h3:rapua ngā kupu e huarite` | 3 | 6 | TRR 6 | TRR109 TRR109_1_0.html: “Rapua ngā kupu e huarite ana” before “Find the rhyming words” |
| `h3:rapua te kupu tika` | 3 | 5 | TRR 5 | TRR109 TRR109_2_0.html: “Rapua te kupu tika” before “Find the correct word” |
| `p:āta whakarongo ki ēnei kupu` | 3 | 5 | TRR 5 | TRR110 TRR110_2_0.html: “Āta whakarongo ki ēnei kupu. Tōia te kupu huarite ki te orop” before “Listen carefully to these kupu. Drag only the kupu” |
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
| `body:widget:dragAndDrop` · p | 725 | 147 |
| `body:free` · p | 494 | 173 |
| `body:activity` · p | 401 | 128 |
| `body:widget:multiChoiceQuiz` · p | 225 | 45 |
| `body:activity` · h3 | 168 | 62 |
| `acks` · p | 158 | 67 |
| `body:alert` · p | 139 | 68 |
| `body:panel:activity` · p | 138 | 29 |
| `body:activity` · li | 132 | 42 |
| `body:widget:reorder` · p | 129 | 22 |
| `body:activity` · h4 | 129 | 34 |
| `body:free` · h3 | 105 | 54 |
| `body:free` · li | 92 | 22 |
| `menu:Overview` · li | 89 | 18 |
| `body:alert:side` · p | 87 | 45 |
| `body:widget:accordion` · p | 84 | 28 |
| `menu:flat` · li | 82 | 36 |
| `body:widget:accordion` · li | 75 | 20 |
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

### `body:activity` → `ABSENT-notWT` — 4320 blocks / 1132 pages / 380 modules
families: TRR 521, XDLS 338, HIS 224, AGH 213, ART 195, BLL 186, MXFL 134, ENGI 126
- AGH1001 `AGH1001_1_0.html` <h3>→<—> “What are primary products?”
- AGH1002 `AGH1002_2_0.html` <h3>→<—> “Soil practical – Texture by sedimentation”
- AGH1003 `AGH1003_2_0.html` <h3>→<—> “Soil properties review”
- AGH1004 `AGH1004_1_0.html` <p>→<—> “Drag and drop the correct factor to the correct classification.”
- AGH1005 `AGH1005_1_0.html` <h3>→<—> “Māori and Western views on plants and their purpose”
- AGH1005 `AGH1005_1_0.html` <p>→<—> “Let’s review the viticulture practices video in the South Island and make a critical judge”

### `body:free` → `ABSENT-notWT` — 3989 blocks / 945 pages / 358 modules
families: HIS 280, TRR 231, XGF 213, MXFL 186, MXFU 179, AGH 172, XDLS 169, MXDI 153
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

### `body:widget:dragAndDrop` → `body:widget:cv2-interactive` — 3200 blocks / 433 pages / 263 modules
families: BLL 265, WJFUN 209, ENGI 178, MXFL 160, XGF 148, ENGC 138, PWY 130, OSBY 110
- AGH1001 `AGH1001_1_0.html` <p>→<th> “Agricultural Production”
- AGH1003 `AGH1003_2_0.html` <p>→<td> “Small sheep and beef farm”
- AGH1004 `AGH1004_2_0.html` <p>→<th> “Mountains and high country”
- AGH1005 `AGH1005_1_0.html` <p>→<li> “Plants are important for food, feeding stock and industrial uses.”
- AGH1007 `AGH1007_5_0.html` <p>→<td> “Ewe pregnant with singles”
- AGH1007 `AGH1007_5_0.html` <p>→<li> “Ewe lamb being finished”

### `body:activity` → `body:free` — 3154 blocks / 668 pages / 328 modules
families: TRR 566, XGF 261, BLL 148, TEDC 145, XDLS 137, PMT 121, HIS 120, WJFUN 87
- AGH1001 `AGH1001_2_0.html` <p>→<p> “Watch these videos and complete activity 2C in your learning journal.”
- AGH1002 `AGH1002_2_0.html` <p>→<p> “Go to your learning journal and complete activity 2B.”
- AGH1003 `AGH1003_2_0.html` <p>→<p> “Revisit this list from earlier in the lesson. Select the soil properties which are altered”
- AGH1004 `AGH1004_1_0.html` <h3>→<h3> “Knowledge self-check”
- AGH1005 `AGH1005_3_0.html` <p>→<p> “Complete activity 3A in your learning journal.”
- AGH1005 `AGH1005_4_0.html` <p>→<p> “Complete activity 5B in your learning journal.”

### `body:activity` → `body:widget:cv2-interactive` — 2649 blocks / 702 pages / 332 modules
families: BLL 241, TRR 222, XMES 144, FRNO 143, WJFUN 127, MXDB 108, HIS 106, MXFL 103
- AGH1001 `AGH1001_1_0.html` <p>→<p> “Select the primary products below which you think are produced in New Zealand or Pacific I”
- AGH1002 `AGH1002_5_0.html` <p>→<p> “Match the chemical symbol with the nutrient.”
- AGH1003 `AGH1003_2_0.html` <p>→<p> “For each production type, identify the irrigation system which would be best suited.”
- AGH1004 `AGH1004_3_0.html` <p>→<p> “From the list, select the region that has the best average of GDD days for each year.”
- AGH1005 `AGH1005_1_0.html` <p>→<p> “Order the following phrases into similarities and differences.”
- AGH1005 `AGH1005_6_0.html` <p>→<p> “Getting the correct amount of nutrients in the soil is a balancing act for many growers. H”

### `body:free` → `ABSENT-inWT` — 2378 blocks / 652 pages / 293 modules
families: TEDC 152, OSOH 110, ENGJ 104, PWY 103, XDLS 94, AGH 93, CHFUN 92, WJFUN 86
- AGH1001 `AGH1001_0_0.html` <h3>→<—> “An introduction to agricultural and horticultural science in Aotearoa New Zealand | He wha”
- AGH1002 `AGH1002_1_0.html` <p>→<—> “As soil gets older, more horizons form. Click on the horizons below to find out more about”
- AGH1003 `AGH1003_0_0.html` <p>→<—> “This module explores the ways farmers and growers do this on various production systems wh”
- AGH1005 `AGH1005_0_0.html` <p>→<—> “It’s important that you fully understand these processes and that they do not occur in iso”
- AGH1006 `AGH1006_2_0.html` <p>→<—> “Commercial crop production uses three main ways to propagate new plants; sowing seeds, cut”
- AGH1006 `AGH1006_3_0.html` <p>→<—> “Cultivation is especially important in intensive horticulture-like commercial market garde”

### `body:activity` → `ABSENT-inWT` — 2336 blocks / 728 pages / 324 modules
families: TEDC 217, ENGS 138, PWY 137, BLL 117, WJFUN 93, XDLS 89, TRR 83, XMES 81
- AGH1001 `AGH1001_2_0.html` <p>→<—> “Complete activity 2B in your learning journal.”
- AGH1002 `AGH1002_4_0.html` <p>→<—> “Go to your learning journal and complete activity 4B and 4C.”
- AGH1003 `AGH1003_3_0.html` <h3>→<—> “Fertiliser application”
- AGH1004 `AGH1004_2_0.html` <h4>→<—> “New Zealand Topographical Map”
- AGH1005 `AGH1005_8_0.html` <h3>→<—> “How plants flower and produce fruit”
- AGH1008 `AGH1008_1_0.html` <h3>→<—> “Manaakitanga in practice”

### `body:widget:multiChoiceQuiz` → `body:widget:cv2-interactive` — 2299 blocks / 226 pages / 149 modules
families: XGF 359, BLL 186, WJFUN 165, MXFL 129, MXFU 117, ENGR 101, PWY 86, ENFUN 79
- AGH1003 `AGH1003_2_0.html` <p>→<td> “Water-holding capacity”
- ANZH104 `ANZH104_7_0.html` <p>→<li> “My journal is complete”
- ANZH105 `ANZH105_8_0.html` <p>→<li> “My journal is complete.”
- ANZH203 `ANZH203_1_0.html` <p>→<li> “What nationality was Abel Tasman”
- ARFUN03 `ARFUN03_0_0.html` <p>→<p> “The dancer’s focus is the audience.”
- ARFUN03 `ARFUN03_0_0.html` <p>→<p> “The dancer's focus is his foot.”

### `body:widget:accordion` → `ABSENT-notWT` — 1692 blocks / 178 pages / 113 modules
families: MXFL 352, HIS 192, XDLS 109, XGF 78, TRR 74, MXFU 70, ENGC 60, XLP 60
- AGH1003 `AGH1003_4_0.html` <p>→<—> “Compost is made from all sorts of organic materials including old plant material and anima”
- AGH1006 `AGH1006_3_0.html` <h4>→<—> “Power-driven methods”
- AGH1008 `AGH1008_3_0.html` <p>→<—> “Examples: plantain, turnips.”
- ANZH205 `ANZH205_7_0.html` <p>→<—> “Contact your Te kura kaiako about other available Te reo Māori courses.”
- ANZH302 `ANZH302_2_0.html` <h4>→<—> “Source 1 – Kesi Ramji’s Mother”
- ANZH302 `ANZH302_2_0.html` <p>→<—> “Our family home was filled with people, love, laughter and lots of delicious food. We had ”

### `body:free` → `body:widget:cv2-interactive` — 1666 blocks / 361 pages / 211 modules
families: XDLS 117, OSAH 80, ENGI 78, OSAI 71, SSCI 67, AGH 63, OSSM 63, MXFL 62
- AGH1001 `AGH1001_2_0.html` <p>→<p> “Below is a brief timeline of the events that have shaped Aotearoa into where we stand toda”
- AGH1002 `AGH1002_3_0.html` <h4>→<th> “Air level in soil”
- AGH1003 `AGH1003_2_0.html` <p>→<p> “While the irrigation system used mainly depends on the size of the production, a range of ”
- AGH1004 `AGH1004_6_0.html` <p>→<p> “As you can see, this process is highly dependent on the ability to store and keep milk bel”
- AGH1005 `AGH1005_1_0.html` <p>→<p> “What differences do you notice between each model of growing plants?”
- AGH1005 `AGH1005_1_0.html` <p>→<p> “As you can see, both models support the use of plants for the purpose of keeping people an”

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

### `body:widget:accordion` → `body:widget:cv2-interactive` — 1292 blocks / 163 pages / 115 modules
families: BLL 145, XDLS 84, XGF 77, HPRE 55, ENGJ 52, WJFUN 50, PWY 45, OSSC 40
- AGH1008 `AGH1008_3_0.html` <p>→<th> “Cows, or sheep, are kept in one big group and moved around paddocks daily, or every second”
- AGH1009 `AGH1009_1_0.html` <p>→<th> “The Treaty of Waitangi is about partnership between the Crown and Māori. This partnership ”
- ANZH203 `ANZH203_3_0.html` <h4>→<p> “Tupaia and the Endeavour”
- ANZH304 `ANZH304_1_0.html` <p>→<p> “Felton Mathew, living in Sydney, accepted an offer to come to New Zealand with Hobson as t”
- BLL112 `BLL112_2_0.html` <li>→<li> “Why do you think the tap might be running?”
- BLL112 `BLL112_2_0.html` <li>→<li> “What do you notice about this tap?”

### `body:alert` → `body:free` — 1275 blocks / 380 pages / 169 modules
families: HIS 96, PES 95, HPRE 80, TRR 79, XGF 77, CEDO 74, ANZH 59, ENFUN 51
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

### `body:widget:accordion` → `ABSENT-inWT` — 1193 blocks / 208 pages / 128 modules
families: XMES 116, TEDC 111, CHFUN 109, AGH 63, XGF 59, BLL 58, PWY 52, ENGJ 46
- AGH1003 `AGH1003_4_0.html` <h4>→<—> “Slurry Tankers/Umbilical Systems”
- AGH1005 `AGH1005_2_0.html` <h4>→<—> “Disease and pest resistance”
- AGH1006 `AGH1006_1_0.html` <h4>→<—> “Integrated pest management (IPM)”
- AGH1008 `AGH1008_3_0.html` <li>→<—> “high dry matter (average 85 percent DM)”
- AGH1009 `AGH1009_1_0.html` <h5>→<—> “Partnership (Partnership principle)”
- AGH1009 `AGH1009_1_0.html` <h4>→<—> “Cultural recognition”

### `body:widget:accordion` → `body:free` — 1127 blocks / 138 pages / 82 modules
families: XGF 139, ENGFUN 89, MXFL 84, TEFUN 64, XDLS 56, ENGJ 48, WJFUN 44, CEDO 43
- AGH1004 `AGH1004_2_0.html` <p>→<p> “Intensive farming is farming where high numbers of animals or crop plants are grown in a s”
- AGH1006 `AGH1006_5_0.html` <p>→<p> “Pruning is the removal of branches or roots from a plant. This is done to change the plant”
- AGH1008 `AGH1008_3_0.html` <p>→<td> “Tough fibrous feed which is usually fed as a supplementary feed during the winter months a”
- ANZH101 `ANZH101_2_0.html` <h4>→<h4> “Ranginui and Papatūānuku”
- ARFUN02 `ARFUN02_0_0.html` <p>→<h5> “Today we're exploring how Rhythm (Ūngēri) works together with repetition. (Takiruaruatanga”
- ARFUN02 `ARFUN02_0_0.html` <h4>→<h5> “How Rhythm and Repetition Work Together:”

### `body:free` → `body:activity` — 1111 blocks / 291 pages / 152 modules
families: TRR 228, AGH 100, HIS 100, MXFL 72, MXDI 61, XDLS 56, MXFU 52, ANZH 42
- AGH1001 `AGH1001_4_0.html` <p>→<p> “Traditional Māori horticultural practices were guided by maramataka or the lunar calendar.”
- AGH1002 `AGH1002_2_0.html` <p>→<p> “The proportion of sand, silt and clay describes a soil's texture. BUT soil particles don’t”
- AGH1003 `AGH1003_1_0.html` <p>→<p> “Soil management practices are the focus of this module. They are the management practices ”
- AGH1004 `AGH1004_5_0.html` <p>→<p> “Here is a video of how water is used to feed crops and pasture:”
- AGH1005 `AGH1005_2_0.html` <p>→<p> “Fruit is formed from the ovary of a flower after fertilisation. Fruit contain seeds used f”
- AGH1005 `AGH1005_2_0.html` <p>→<p> “The main functions of fruits and seeds are to:”

### `body:widget:multiChoiceQuiz` → `ABSENT-inWT` — 936 blocks / 140 pages / 92 modules
families: PWY 179, TEDC 98, BLL 56, HPFUN 46, MXFL 44, CEDR 39, OSAI 39, MXFUN 34
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

### `body:free` → `OTHER-PAGE` — 880 blocks / 113 pages / 79 modules
families: TRR 372, GENO 77, AGH 59, MXDI 54, SSFUN 26, XGF 25, XDLS 24, XLP 19
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

### `body:widget:flipCard` → `body:widget:cv2-interactive` — 746 blocks / 116 pages / 95 modules
families: HPFUN 73, MXFL 52, BLL 48, OSSC 44, HPRE 42, PWY 36, XOTPB 36, TEDC 35
- ANZH105 `ANZH105_5_0.html` <h4>→<td> “What is it made of?”
- ANZH304 `ANZH304_4_0.html` <p>→<p> “Colonial officials mainly understood Te Tiriti o Waitangi (the Treaty of Waitangi) based o”
- ARFUN01 `ARFUN01_0_0.html` <p>→<p> “William Shakespeare is a famous playwright. Reading or watching his plays show us what it ”
- ARFUN03 `ARFUN03_0_0.html` <p>→<p> “The dancers are on a high level.”
- BLL171 `BLL171_2_0.html` <h4>→<th> “If you could create a new ice cream flavour, what would it taste like?”
- BLL171 `BLL171_2_0.html` <h4>→<th> “Would you rather be able to fly like a bird or swim like a fish?”

