# Round 0 — THE CEILING (what no converter rule can ever close)

Generated 2026-09-22 11:47:56 by `outputs/_measure_ceiling.py`. Modules measured 516 / requested 544; without a parsed WT (skipped): TRR115, ENGJ403, GER1003, GER1004, GER1005, GER1006, GER1007, SAM1005, SAM1006; parsed files present but none looks like a Writers Template (skipped): TRR102, TRR103, TRR104, TRR105, TRR107, TRR108, TRR109, TRR111, TRR112, TRR113, TRR203, TRR301, TRR304, XOTPG01, XOTPG03, XOTPG04, XOTPG05, XOTPG06; modules read from the UNION of 203×2+ parsed files; gold-only (no Claude dir, never paired): 0.

**Plain English.** A *block* is one piece of text on the human's finished page (a heading, a paragraph, a bullet, a table cell). A block has a *source* when the same words — or a distinctive run of them — appear anywhere in the writer's template. Blocks with **no source** were written by the developer (verbal feedback, house copy): no rule that reads the template can produce them. **Boilerplate** is no-source text that recurs across many modules (a convention a rule CAN emit), so the honest ceiling removes it (**net**). *Scaffold scope* ignores text inside interactive widgets, because the primary skeleton gate ignores widget internals too.

## Headline (the PAIRED population — the pages the skeleton gate scores)

- pages 2422 / modules 516 / text blocks (scaffold scope) 114035
- no-source share, scaffold scope: per-page mean **raw 11.5% → net 8.8%** (pooled raw 11.0% → net 9.2%)
- no-source share, full scope (widget internals included): per-page mean raw 16.2% → net 13.0%
- **CEILING (scaffold) = 91.2%** (round-110 test) — loose upper bound 93.6% (every content word of the block found somewhere in the WT) · ceiling (full) = 87.0% / loose 89.3%
- baseline `_intake_2026-09-22_sk_final.json` (2491 pairs): SCAFFOLD mean 54.117% / RAW mean 38.049%
- **SCAFFOLD 54.12% = 59.4% of achievable** (band 57.8%–59.4%: the loose ceiling gives the lower figure); RAW 38.05% = 43.7% of its own ceiling (band 42.6%–43.7%); per-page mean of (score ÷ own ceiling) = 59.9% over 2417 joined pages

| population | pages | modules | blocks (scaffold) | mean no-source raw | mean no-source NET | mean no-source LOOSE | ceiling (scaffold) | ceiling loose | mean full raw | mean full NET |
|---|---|---|---|---|---|---|---|---|---|---|
| paired (gate population) | 2422 | 516 | 114035 | 11.5% | 8.8% | 6.4% | 91.2% | 93.6% | 16.2% | 13.0% |
| compare_set ∩ paired | 982 | 198 | 46355 | 10.7% | 8.0% | 5.4% | 92.0% | 94.6% | 15.3% | 12.4% |
| ALL gold pages with a WT | 2798 | 516 | 129242 | 13.8% | 11.1% | 8.2% | 88.9% | 91.8% | 18.4% | 15.2% |

## By Template family (folder) — paired population

| group | pages | modules | mean no-source raw | mean no-source NET | mean LOOSE | ceiling | ceiling loose | pooled NET |
|---|---|---|---|---|---|---|---|---|
| Standard | 2164 | 366 | 11.8% | 9.1% | 6.6% | 90.9% | 93.4% | 9.7% |
| Fundamentals | 117 | 81 | 9.3% | 7.5% | 4.6% | 92.5% | 95.4% | 9.0% |
| Inquiry | 109 | 60 | 9.3% | 6.8% | 4.5% | 93.2% | 95.5% | 6.8% |
| Bilingual | 32 | 9 | 4.8% | 4.7% | 3.4% | 95.3% | 96.6% | 5.7% |

## By HTML sub-type (KB 06) — paired population

| group | pages | modules | mean no-source raw | mean no-source NET | mean LOOSE | ceiling | ceiling loose | pooled NET |
|---|---|---|---|---|---|---|---|---|
| Standard | 2046 | 349 | 12.0% | 9.1% | 6.6% | 90.9% | 93.4% | 9.7% |
| Combo | 169 | 27 | 9.2% | 7.1% | 4.7% | 92.9% | 95.3% | 7.8% |
| Fundamentals | 107 | 82 | 9.4% | 7.7% | 5.1% | 92.3% | 94.9% | 9.2% |
| Inquiry | 68 | 63 | 9.0% | 7.8% | 5.8% | 92.2% | 94.2% | 7.1% |
| Bilingual | 32 | 9 | 4.8% | 4.7% | 3.4% | 95.3% | 96.6% | 5.7% |

## By Legacy (True) vs Refresh (False) — paired population

| group | pages | modules | mean no-source raw | mean no-source NET | mean LOOSE | ceiling | ceiling loose | pooled NET |
|---|---|---|---|---|---|---|---|---|
| False | 2422 | 516 | 11.5% | 8.8% | 6.4% | 91.2% | 93.6% | 9.2% |

## By KB subject family (14.x, prefix heuristic) — paired population

| group | pages | modules | mean no-source raw | mean no-source NET | mean LOOSE | ceiling | ceiling loose | pooled NET |
|---|---|---|---|---|---|---|---|---|
| no KB family | 1508 | 247 | 11.6% | 9.2% | 6.2% | 90.8% | 93.8% | 9.2% |
| BLL (14.7) | 306 | 109 | 8.2% | 3.8% | 3.0% | 96.2% | 97.0% | 3.2% |
| X-prefixed other (learningSupport) | 124 | 25 | 10.8% | 8.0% | 5.5% | 92.0% | 94.5% | 9.2% |
| Languages (14.1) | 120 | 23 | 24.6% | 22.5% | 20.6% | 77.5% | 79.4% | 25.5% |
| CED (14.4) | 115 | 29 | 8.7% | 6.3% | 4.1% | 93.7% | 95.9% | 5.5% |
| LS (14.6) | 103 | 18 | 12.5% | 9.8% | 6.8% | 90.2% | 93.2% | 9.9% |
| Pathways (14.2) | 45 | 6 | 4.8% | 3.7% | 3.4% | 96.3% | 96.6% | 3.2% |
| MiW/WJ (14.10) | 21 | 21 | 8.8% | 7.1% | 5.3% | 92.9% | 94.7% | 5.5% |
| BLLR (14.9) | 21 | 3 | 7.9% | 5.4% | 4.2% | 94.6% | 95.8% | 3.2% |
| HPE content (14.8) | 21 | 2 | 3.8% | 2.5% | 2.4% | 97.5% | 97.6% | 1.7% |
| Taonga/Arts (14.3) | 15 | 10 | 19.6% | 17.8% | 13.3% | 82.2% | 86.7% | 13.6% |
| H&PE FUNdamentals (14.5) | 15 | 15 | 11.7% | 10.9% | 6.4% | 89.1% | 93.6% | 12.2% |
| Technology (14.12) | 8 | 8 | 8.4% | 7.5% | 4.8% | 92.5% | 95.2% | 7.0% |

## By Subject (Module_Structure_Index) — paired population

| group | pages | modules | mean no-source raw | mean no-source NET | mean LOOSE | ceiling | ceiling loose | pooled NET |
|---|---|---|---|---|---|---|---|---|
| NCEA1 | 555 | 78 | 17.0% | 15.1% | 11.7% | 84.9% | 88.3% | 18.4% |
| 1-10 English | 333 | 52 | 9.3% | 6.1% | 4.0% | 93.9% | 96.0% | 6.5% |
| 1-10 Mathematics | 332 | 42 | 12.2% | 10.1% | 6.2% | 89.9% | 93.8% | 11.9% |
| 1-10 Blended Literacy | 327 | 112 | 8.2% | 3.9% | 3.1% | 96.1% | 96.9% | 3.2% |
| Leaving to Learn | 227 | 43 | 11.5% | 8.8% | 6.1% | 91.2% | 93.9% | 9.5% |
| Online Safety (OS9000) | 136 | 29 | 5.4% | 2.8% | 2.4% | 97.2% | 97.6% | 2.4% |
| ConnectED | 115 | 29 | 8.7% | 6.3% | 4.1% | 93.7% | 95.9% | 5.5% |
| ANZH | 92 | 13 | 17.1% | 14.8% | 11.6% | 85.2% | 88.4% | 14.0% |
| 1-10 Languages | 65 | 16 | 6.6% | 4.3% | 3.2% | 95.7% | 96.8% | 4.6% |
| 1-10 Social Science | 60 | 14 | 13.6% | 7.0% | 3.8% | 93.0% | 96.2% | 5.3% |
| 1-10 Health and PE | 36 | 17 | 7.1% | 6.0% | 4.1% | 94.0% | 95.9% | 7.7% |
| 1-10 Science | 33 | 5 | 6.0% | 3.3% | 2.4% | 96.7% | 97.6% | 3.9% |
| Te Marautanga o Aotearoa TMoA | 32 | 9 | 4.8% | 4.7% | 3.4% | 95.3% | 96.6% | 5.7% |
| 1-10 Technology | 25 | 10 | 7.3% | 6.2% | 3.6% | 93.8% | 96.4% | 7.0% |
| 1-10 Writing (MiW) | 21 | 21 | 8.8% | 7.1% | 5.3% | 92.9% | 94.7% | 5.5% |
| EXPlore | 15 | 8 | 13.6% | 13.4% | 7.4% | 86.6% | 92.6% | 8.1% |
| Te ara Whakapuawa -Wellbeing | 13 | 13 | 14.0% | 13.8% | 10.8% | 86.2% | 89.2% | 15.4% |
| 1-10 Arts | 5 | 5 | 8.5% | 5.3% | 2.6% | 94.7% | 97.4% | 5.5% |

## By Series prefix — paired population

| group | pages | modules | mean no-source raw | mean no-source NET | mean LOOSE | ceiling | ceiling loose | pooled NET |
|---|---|---|---|---|---|---|---|---|
| BLL | 306 | 109 | 8.2% | 3.8% | 3.0% | 96.2% | 97.0% | 3.2% |
| MXFL | 94 | 11 | 9.3% | 8.0% | 4.8% | 92.0% | 95.2% | 8.7% |
| ANZH | 91 | 12 | 17.0% | 14.7% | 11.6% | 85.3% | 88.4% | 13.8% |
| ENGI | 84 | 12 | 10.1% | 6.2% | 4.8% | 93.8% | 95.2% | 6.4% |
| ENGC | 81 | 10 | 8.4% | 5.7% | 3.8% | 94.3% | 96.2% | 6.4% |
| HIS | 77 | 8 | 9.7% | 8.5% | 6.0% | 91.5% | 94.0% | 7.9% |
| XDLS | 75 | 12 | 14.2% | 11.2% | 7.6% | 88.8% | 92.4% | 11.1% |
| PES | 75 | 7 | 13.9% | 11.2% | 8.3% | 88.8% | 91.7% | 13.6% |
| AGH | 74 | 9 | 11.7% | 10.9% | 7.0% | 89.1% | 93.0% | 12.3% |
| ENGS | 64 | 9 | 10.2% | 6.7% | 4.4% | 93.3% | 95.6% | 6.7% |
| MXFU | 56 | 6 | 11.6% | 10.4% | 7.1% | 89.6% | 92.9% | 11.6% |
| MXDI | 52 | 6 | 12.3% | 10.0% | 5.0% | 90.0% | 95.0% | 10.2% |
| ENGJ | 50 | 7 | 7.4% | 4.5% | 2.3% | 95.5% | 97.7% | 4.7% |
| PHE | 49 | 8 | 24.0% | 21.9% | 16.4% | 78.1% | 83.6% | 21.3% |
| ENGR | 46 | 6 | 10.0% | 7.3% | 3.9% | 92.7% | 96.1% | 6.8% |
| HES | 45 | 6 | 21.7% | 19.3% | 15.4% | 80.7% | 84.6% | 14.8% |
| PWY | 44 | 5 | 4.2% | 3.1% | 2.9% | 96.9% | 97.1% | 2.4% |
| MXDB | 41 | 5 | 11.5% | 8.6% | 5.6% | 91.4% | 94.4% | 8.7% |
| CEDO | 40 | 9 | 13.4% | 11.6% | 7.8% | 88.4% | 92.2% | 5.7% |
| MXEO | 40 | 5 | 12.0% | 9.9% | 6.6% | 90.1% | 93.4% | 10.1% |
| MXEX | 40 | 6 | 19.8% | 16.0% | 10.6% | 84.0% | 89.4% | 22.6% |
| XMES | 39 | 6 | 8.9% | 7.3% | 4.8% | 92.7% | 95.2% | 6.6% |
| XGF | 38 | 5 | 10.7% | 9.4% | 6.6% | 90.6% | 93.4% | 13.0% |
| CEDT | 33 | 8 | 5.3% | 2.6% | 1.3% | 97.4% | 98.7% | 5.4% |
| FRFUN | 28 | 3 | 6.7% | 4.1% | 2.7% | 95.9% | 97.3% | 3.7% |
| CBI | 28 | 4 | 6.4% | 4.8% | 2.8% | 95.2% | 97.2% | 3.0% |
| XLP | 28 | 6 | 7.7% | 6.0% | 4.8% | 94.0% | 95.2% | 6.1% |
| SSOG | 27 | 4 | 17.6% | 4.8% | 1.8% | 95.2% | 98.2% | 3.0% |
| CHI | 26 | 3 | 80.6% | 78.9% | 75.8% | 21.1% | 24.2% | 84.8% |
| COM | 23 | 3 | 15.2% | 11.3% | 7.0% | 88.7% | 93.0% | 11.8% |
| OSBY | 23 | 5 | 6.7% | 4.1% | 3.1% | 95.9% | 96.9% | 4.0% |
| OSOH | 23 | 5 | 4.3% | 2.8% | 2.5% | 97.2% | 97.5% | 2.3% |
| OSAI | 22 | 5 | 5.0% | 2.2% | 1.5% | 97.8% | 98.5% | 2.4% |
| OSGM | 22 | 5 | 4.8% | 2.0% | 1.6% | 98.0% | 98.4% | 1.4% |
| WJFUN | 21 | 21 | 8.8% | 7.1% | 5.3% | 92.9% | 94.7% | 5.5% |
| BLLR | 21 | 3 | 7.9% | 5.4% | 4.2% | 94.6% | 95.8% | 3.2% |
| HPRE | 21 | 2 | 3.8% | 2.5% | 2.4% | 97.5% | 97.6% | 1.7% |
| DTC | 18 | 2 | 17.6% | 15.3% | 10.9% | 84.7% | 89.1% | 14.1% |
| FRNO | 18 | 2 | 3.2% | 2.0% | 2.0% | 98.0% | 98.0% | 1.5% |
| XTAS | 18 | 3 | 7.6% | 6.4% | 4.0% | 93.6% | 96.0% | 6.4% |
| TRR | 17 | 4 | 4.6% | 4.6% | 3.6% | 95.4% | 96.4% | 5.6% |
| DAN | 17 | 3 | 13.8% | 9.1% | 3.5% | 90.9% | 96.5% | 9.8% |
| SSCI | 17 | 2 | 3.1% | 1.0% | 0.7% | 99.0% | 99.3% | 0.8% |
| TEDC | 17 | 2 | 6.7% | 5.6% | 3.1% | 94.4% | 96.9% | 6.9% |
| OSSM | 16 | 3 | 4.2% | 1.3% | 1.3% | 98.7% | 98.7% | 0.7% |
| HPFUN | 15 | 15 | 11.7% | 10.9% | 6.4% | 89.1% | 93.6% | 12.2% |
| CEDK | 15 | 4 | 6.2% | 3.4% | 2.6% | 96.6% | 97.4% | 3.5% |
| OSAH | 15 | 3 | 6.4% | 3.0% | 3.0% | 97.0% | 97.0% | 2.7% |
| OSSC | 15 | 3 | 6.7% | 4.6% | 4.6% | 95.4% | 95.4% | 3.7% |
| CEDR | 14 | 5 | 4.6% | 2.8% | 1.7% | 97.2% | 98.3% | 3.8% |
| GEO | 14 | 3 | 8.8% | 5.1% | 4.2% | 94.9% | 95.8% | 4.3% |
| CEDW | 13 | 3 | 10.3% | 6.7% | 3.8% | 93.3% | 96.2% | 10.6% |
| MUS | 12 | 2 | 16.4% | 14.3% | 9.7% | 85.7% | 90.3% | 12.8% |
| XOTPB | 12 | 6 | 19.5% | 5.9% | 4.9% | 94.1% | 95.1% | 5.9% |
| PNR | 11 | 4 | 3.9% | 3.7% | 2.3% | 96.3% | 97.7% | 3.3% |
| JPN | 11 | 1 | 7.4% | 6.8% | 3.9% | 93.2% | 96.1% | 5.4% |
| ART | 10 | 5 | 25.2% | 24.1% | 18.7% | 75.9% | 81.3% | 34.1% |
| MXFUN | 9 | 3 | 17.0% | 12.1% | 3.2% | 87.9% | 96.8% | 21.5% |
| SSFUN | 9 | 7 | 29.9% | 29.7% | 18.2% | 70.3% | 81.8% | 15.7% |
| GENO | 9 | 1 | 13.5% | 7.7% | 5.8% | 92.3% | 94.2% | 8.7% |
| MXS | 9 | 1 | 21.9% | 19.4% | 9.3% | 80.6% | 90.7% | 18.1% |
| SCBI | 9 | 1 | 0.7% | 0.3% | 0.3% | 99.7% | 99.7% | 0.4% |
| SCCH | 9 | 1 | 6.8% | 4.6% | 2.1% | 95.4% | 97.9% | 4.6% |
| SCPH | 9 | 1 | 7.6% | 3.1% | 3.1% | 96.9% | 96.9% | 2.8% |
| ENFUN | 8 | 8 | 9.7% | 8.2% | 5.5% | 91.8% | 94.5% | 8.4% |
| TEFUN | 8 | 8 | 8.4% | 7.5% | 4.8% | 92.5% | 95.2% | 7.0% |
| XWHA | 8 | 2 | 18.1% | 12.5% | 9.8% | 87.5% | 90.2% | 15.2% |
| XFUN | 7 | 2 | 5.0% | 4.7% | 2.6% | 95.3% | 97.4% | 8.3% |
| SSEA | 7 | 1 | 3.0% | 0.7% | 0.7% | 99.3% | 99.3% | 0.4% |
| CHFUN | 6 | 6 | 5.5% | 5.5% | 4.0% | 94.5% | 96.0% | 6.0% |
| EXPFUN | 6 | 6 | 5.7% | 5.4% | 3.0% | 94.6% | 97.0% | 3.8% |
| TWHA | 6 | 6 | 23.8% | 23.8% | 18.8% | 76.2% | 81.2% | 22.7% |
| ENO | 6 | 1 | 9.1% | 9.1% | 5.8% | 90.9% | 94.2% | 8.0% |
| ARFUN | 5 | 5 | 8.5% | 5.3% | 2.6% | 94.7% | 97.4% | 5.5% |
| ENGFUN | 5 | 1 | 6.1% | 3.5% | 2.9% | 96.5% | 97.2% | 3.9% |
| ENG | 5 | 3 | 11.6% | 10.9% | 7.9% | 89.1% | 92.1% | 9.2% |
| EXBP | 5 | 1 | 29.6% | 29.6% | 15.2% | 70.4% | 84.8% | 27.3% |
| SCES | 5 | 1 | 10.8% | 6.6% | 4.9% | 93.4% | 95.1% | 7.9% |
| PMT | 4 | 1 | 8.1% | 8.1% | 5.3% | 91.9% | 94.7% | 8.8% |
| TWHK | 4 | 4 | 3.3% | 2.5% | 1.6% | 97.5% | 98.4% | 2.8% |
| EXIP | 4 | 1 | 5.2% | 5.2% | 4.2% | 94.8% | 95.8% | 4.6% |
| GER | 3 | 1 | 21.8% | 21.8% | 18.6% | 78.2% | 81.4% | 30.3% |
| SPA | 3 | 1 | 59.4% | 56.3% | 50.6% | 43.7% | 49.4% | 74.7% |
| JPFUN | 2 | 2 | 8.5% | 8.5% | 4.8% | 91.5% | 95.2% | 8.6% |
| TWHR | 2 | 2 | 3.6% | 3.6% | 3.2% | 96.4% | 96.8% | 3.9% |
| XOTPO | 2 | 1 | 14.9% | 13.6% | 12.4% | 86.4% | 87.6% | 13.8% |
| ANZHFUN | 1 | 1 | 20.0% | 20.0% | 20.0% | 80.0% | 80.0% | 20.0% |
| SCFUN | 1 | 1 | 5.7% | 5.7% | 5.7% | 94.3% | 94.3% | 5.7% |
| CHWHA | 1 | 1 | 9.1% | 9.1% | 9.1% | 90.9% | 90.9% | 9.1% |
| GEWHA | 1 | 1 | 1.6% | 0.0% | 0.0% | 100.0% | 100.0% | 0.0% |
| TWHT | 1 | 1 | 19.3% | 19.3% | 15.2% | 80.7% | 84.8% | 19.3% |
| PWYWHA | 1 | 1 | 28.9% | 26.7% | 26.7% | 73.3% | 73.3% | 26.7% |

## Boilerplate — no-source text recurring in ≥ 5 modules (170 strings; top 60)

These are conventions a rule can emit (most are documented in the KB); they are removed from the NET figures.

| modules | text |
|---|---|
| 486 | acknowledgements |
| 408 | every effort has been made to acknowledge and contact copyright holders te aho o te kura pounamu apologises for any omis |
| 406 | copyright board of trustees of te aho o te kura pounamu private bag 39992 wellington mail centre lower hutt 5045 new zea |
| 378 | all other images te aho o te kura pounamu wellington new zealand |
| 148 | select one |
| 116 | 02 |
| 116 | 01 |
| 90 | image avatar heygen wwwheygencom used with permission |
| 74 | 03 |
| 73 | how will i know if ive learned it |
| 73 | 40 |
| 67 | 20 |
| 67 | 04 |
| 66 | 50 |
| 61 | 30 |
| 56 | 70 |
| 55 | 60 |
| 51 | all illustrations te aho o te kura pounamu wellington new zealand |
| 51 | 10 |
| 49 | standards |
| 48 | 05 |
| 46 | want to know where to start |
| 42 | 80 |
| 39 | unable to display pdf file download here |
| 36 | click here to view a basic year plan talk to your kaiako about creating a specific learning plan to meet your needs |
| 34 | learning intentions |
| 33 | 06 |
| 30 | i can |
| 28 | f |
| 28 | 07 |
| 26 | t |
| 26 | 90 |
| 25 | go to your journal |
| 24 | success criteria |
| 24 | information |
| 23 | designer note audio to come |
| 22 | we are learning |
| 20 | you will show your understanding by |
| 20 | photo new zealand topographic relief map 3d render istock 1454804075 getty images used with permission |
| 19 | intro |
| 19 | all other images and audio te aho o te kura pounamu wellington new zealand |
| 16 | video avatar heygen wwwheygencom used with permission |
| 16 | 08 |
| 15 | how will i know i have learned it |
| 14 | important note |
| 11 | they write with ease and automaticity and correctly spell a wide range of words including those with advanced spelling p |
| 11 | share your learning |
| 10 | word 3 |
| 10 | word 2 |
| 10 | step 2 |
| 10 | step 1 |
| 10 | n |
| 10 | all other illustrations te aho o te kura pounamu wellington new zealand |
| 9 | yes |
| 9 | word 9 |
| 9 | word 8 |
| 9 | word 7 |
| 9 | word 6 |
| 9 | word 5 |
| 9 | word 4 |

## Outlier pages — paired pages whose NET no-source share ≥ 50% with ≥ 8 blocks (69 pages; top 60)

These pages will score low against gold no matter what the converter does; the samples show the developer-authored text.

| page | family | sub-type | KB family | blocks | no-source (net) | share | skeleton score | samples of unsourced text |
|---|---|---|---|---|---|---|---|---|
| CHI1003_5_0.html | Standard | Standard | Languages (14.1) | 152 | 147 | 96.7% | — | <h1> 第五课 ¦ <h1> Giving reasons - making comparisons ¦ <p> In this lesson, you will have opportunities to |
| CHI1003_7_0.html | Standard | Standard | Languages (14.1) | 25 | 24 | 96.0% | — | <h1> 第七课 ¦ <h1> Revising – likes and dislikes ¦ <p> In this lesson, you will focus on: |
| CHI1003_4_0.html | Standard | Standard | Languages (14.1) | 65 | 62 | 95.4% | — | <h1> 第四课 ¦ <h1> More about seasons and weather ¦ <li> review the words and phrases on seasons and weather |
| CHI1004_9_0_Vocabulary.html | Standard | Standard | Languages (14.1) | 122 | 116 | 95.1% | — | <h1> Word list ¦ <h3> Module word list ¦ <p> You should be able to understand and say all these words and know the Pinyin spelling. |
| CHI1003_2_0.html | Standard | Standard | Languages (14.1) | 100 | 95 | 95.0% | 16.4% | <h1> 第二课 ¦ <h1> Years, ages and dates of birth ¦ <p> In this lesson, you will focus on |
| CHI1003_6_0.html | Standard | Standard | Languages (14.1) | 18 | 17 | 94.4% | 42.1% | <h1> 第六课 ¦ <h1> Revising date of birth and seasons ¦ <p> In this lesson, you will focus on: |
| HES1002_4_0.html | Standard | Standard | no KB family | 14 | 13 | 92.9% | 45.0% | <h1> Pacific Health Models ¦ <h1> Pacific Health Models ¦ <h3> More Examples of Pacific Models of Health: |
| CHI1003_3_0.html | Standard | Standard | Languages (14.1) | 82 | 75 | 91.5% | 22.9% | <h1> 第三课 ¦ <h1> Talking about seasons and weather ¦ <p> In this lesson, you will focus on |
| CHI1004_6_0.html | Standard | Standard | Languages (14.1) | 67 | 61 | 91.0% | 25.3% | <h1> 第六课 ¦ <h1> Speaking and writing practice ¦ <p> In this lesson, you will have opportunities to: |
| CHI1005_5_0.html | Standard | Standard | Languages (14.1) | 55 | 50 | 90.9% | 32.1% | <h1> 第五课 ¦ <h1> Speaking and reading practice ¦ <p> In this lesson, you will have opportunities to learn some new words and structures as well as practise your re |
| CHI1004_4_0.html | Standard | Standard | Languages (14.1) | 81 | 73 | 90.1% | 32.1% | <h1> 第四课 ¦ <p> In this lesson, you will have opportunities to learn: ¦ <li> how Chinese celebrate Spring Festival |
| CHI1005_6_0.html | Standard | Standard | Languages (14.1) | 68 | 61 | 89.7% | 22.9% | <h1> 第六课 ¦ <h1> Describing and narrating activities in sequence ¦ <p> It will take you approximately an hour to complete this lesson. |
| DTC1005_2_0.html | Standard | Standard | no KB family | 17 | 15 | 88.2% | 70.6% | <h3> Manage data ¦ <p> Databases are incredibly widespread – they underlie technology used by most people every day if not every hour ¦ <p> Databases sit behind a huge number of websites and they're a crucial component of, for example: |
| XGF9004-06.0.html | Standard | Combo | X-prefixed other (learningSupport) | 59 | 52 | 88.1% | 34.8% | <h1> Brain Boosters – Resources and Games ¦ <p> Games help your brain stretch, flex, and grow stronger, just like muscles do when you exercise. ¦ <p> No matter your age – five, fifteen, or older – this section has something for everyone. Start with board and c |
| CHI1003_8_0.html | Standard | Standard | Languages (14.1) | 23 | 20 | 87.0% | 36.2% | <h1> 第八课 ¦ <p> In this lesson, you will focus on: ¦ <li> reviewing dates of birth and seasons. |
| CEDO301_3.0.html | Standard | Standard | CED (14.4) | 28 | 24 | 85.7% | 49.1% | <h1> Science Investigation ¦ <h3> Testing my idea ¦ <p> Designer note: Link to be updated to orgunit link |
| CHI1005_3_0.html | Standard | Standard | Languages (14.1) | 41 | 35 | 85.4% | 26.8% | <h1> 第三课 ¦ <p> In this lesson, you will have opportunities to learn about clothes shopping and focus on: ¦ <li> reading comprehension and listening skills in routines description |
| CHI1004_5_0.html | Standard | Standard | Languages (14.1) | 102 | 85 | 83.3% | 21.8% | <h1> 第五课 ¦ <p> In this lesson, you will have opportunities to read and listen to: ¦ <p> It will take you approximately an hour and a half to complete this lesson. |
| CHI1003_1_0.html | Standard | Standard | Languages (14.1) | 72 | 60 | 83.3% | 25.3% | <h1> 第一课 ¦ <p> In this lesson, you will have opportunities to ¦ <li> review 12 zodiacs |
| CHI1004_2_0.html | Standard | Standard | Languages (14.1) | 116 | 96 | 82.8% | 24.2% | <h1> 第二课 ¦ <p> In this lesson, you will focus on: ¦ <li> learning words about clothes and describing them. |
| CHI1005_1_0.html | Standard | Standard | Languages (14.1) | 73 | 60 | 82.2% | 32.6% | <h1> 第一课 ¦ <h1> Cultural Comparison ¦ <p> In this lesson, you will have opportunities to: |
| SPA1004_3_0.html | Standard | Standard | Languages (14.1) | 120 | 97 | 80.8% | 17.1% | <h1> ¿Qué Vamos A Hacer? ¦ <h1> What Are We Going To Do? ¦ <h2> Los planes para la fiesta... ¦ Plans for the party... |
| HES1002_6_0.html | Standard | Standard | no KB family | 20 | 16 | 80.0% | 51.1% | <h1> My Model of Wellbeing/Health ¦ <p> Create your own model of wellbeing. ¦ <li> Take another look at the different models of wellbeing/health that you have learnt about in this topic. Decide |
| CHI1005_7_0.html | Standard | Standard | Languages (14.1) | 14 | 11 | 78.6% | 55.8% | <h1> 第七课 ¦ <h1> Revision: Reading and writing ¦ <p> It will take you approximately an hour to complete this lesson. |
| CHI1005_4_0.html | Standard | Standard | Languages (14.1) | 36 | 28 | 77.8% | 34.1% | <h1> 第四课 ¦ <p> In this lesson, you will have opportunities to learn: ¦ <p> It will take you approximately an hour and a half to complete this lesson. |
| CHI1004_7_0.html | Standard | Standard | Languages (14.1) | 191 | 147 | 77.0% | 13.0% | <h1> 第七课 ¦ <h1> Revision: More reading and writing practice ¦ <p> In this lesson, you will have: |
| PHE1004_3.0.html | Standard | Standard | no KB family | 17 | 13 | 76.5% | 52.5% | <h1> Time for Action ¦ <h3> So they say practice makes perfect! ¦ <p> Include and provide supporting evidence/examples by using photos and or video footage. These reflections and r |
| CHI1005_2_0.html | Standard | Standard | Languages (14.1) | 105 | 79 | 75.2% | 18.0% | <h1> 第二课 ¦ <h1> What's school like in NZ? ¦ <p> In this lesson, you will focus on: |
| MXEX301_05.0.html | Standard | Standard | no KB family | 43 | 31 | 72.1% | 22.5% | <p> A line is straight and has no beginning or end point. It is infinite. When you draw a line, you put arrows at  ¦ <p> This line can be named using two points on it. It can be called line AB or ¦ <p> A ray is a part of a line. It starts at a point and extends in one direction forever. |
| SPA1004_0_0.html | Standard | Standard | Languages (14.1) | 14 | 10 | 71.4% | 63.5% | <p> E rere te huata, kapohia ¦ <p> Aprovecha al máximo cada oportunidad. Make the most of every opportunity. ¦ <h3> ¿Tienes alguna idea? ¦ Do you have any ideas? |
| HES1002_1_0.html | Standard | Standard | no KB family | 17 | 12 | 70.6% | 52.9% | <h1> Let’s recap ¦ <h3> Let's recap ¦ <p> Kupu Māori meanings for hauora, oranga, mauri and waiora are from Te Aka Māori Dictionary. |
| CHI1004_3_0.html | Standard | Standard | Languages (14.1) | 44 | 31 | 70.5% | 36.2% | <h1> 第三课 ¦ <h1> More clothes shopping ¦ <p> In this lesson, you will have opportunities to learn about clothes shopping and focus on: |
| XGF9004-03.0.html | Standard | Combo | X-prefixed other (learningSupport) | 134 | 92 | 68.7% | 23.8% | <h1> Self-monitoring ¦ <h2> Self-monitoring ¦ <p> Self-monitoring is about noticing your thoughts, actions, and feelings and making changes when needed. You hav |
| DTC1005_3_0.html | Standard | Standard | no KB family | 35 | 24 | 68.6% | 53.7% | <p> Websites can be used: ¦ <li> to sell products ¦ <li> to buy products |
| ART1006_4.0.html | Standard | Standard | Taonga/Arts (14.3) | 98 | 65 | 66.3% | 19.5% | <p> Required: 1–2 A4 pages of notes and drawings ¦ Time: 1 hour. ¦ <p> Here are two examples of how other ākonga have assessed their projects. ¦ <h4> Passion Project Self-Assessment Rubric |
| MXEX301_03.1.html | Standard | Standard | no KB family | 38 | 25 | 65.8% | 23.0% | <p> This is a very small amount. A teaspoon holds about five millilitres. ¦ <p> 1000 millilitres is called a litre. ¦ <p> This is the basic unit for capacity. A carton of milk holds a litre. |
| XDLS501.01.html | Standard | Standard | LS (14.6) | 35 | 23 | 65.7% | 31.1% | <li> that the space between us and others depends on who they are ¦ <li> that the space between us and others depends on where we are ¦ <li> that intimate information and intimate space is for special people in our lives. |
| EXBP901_1.1.html | Standard | Standard | no KB family | 47 | 30 | 63.8% | 25.7% | <h1> The Learning Cycle ¦ <h4> Learning objective ¦ <p> You will complete a quiz about the learning cycle. |
| XDLS501.04.html | Standard | Standard | LS (14.6) | 63 | 40 | 63.5% | 21.2% | <h1> Conflict Resolution ¦ <li> how to strive towards peace ¦ <li> how to negotiate things you want and need. |
| CHI1004_8_0.html | Standard | Standard | Languages (14.1) | 46 | 29 | 63.0% | 36.2% | <h1> 第八课 ¦ <h1> Practise all four skills ¦ <p> In this lesson, you will revise your listening, reading, speaking and writing skills through various activitie |
| HES1002_5_0.html | Standard | Standard | no KB family | 24 | 15 | 62.5% | 38.0% | <h4> The Model ¦ <p> It is a visual representation of Pasifika values and beliefs. It uses the Samoan fale or house to describe the ¦ <h3> Fonofale – join ‘Pale in the Fale’ |
| PHE1001_3.0.html | Standard | Standard | no KB family | 24 | 15 | 62.5% | 72.2% | <p> What are external cues? External cues are unpredictable influences or factors that we might face in a game or  ¦ <p> Some external cues could be: ¦ <li> environmental factors |
| HES1005_7.0.html | Standard | Standard | no KB family | 45 | 28 | 62.2% | 41.7% | <h1> Oranga Taihema ¦ <p> This lesson is not compulsory. If you have any concerns or queries about the topics of sexuality or gender ide ¦ <h3> What should Jo choose? |
| MXFL204_6.0.html | Standard | Standard | no KB family | 26 | 16 | 61.5% | 39.7% | <p> The line graph below shows how a puppy’s weight has changed as it grows each week. ¦ <h5> In this line graph: ¦ <li> The horizontal axis (x-axis), the one along the bottom represents the time. In this graph, the puppy’s age in  |
| ANZH104_02.0.html | Standard | Standard | no KB family | 13 | 8 | 61.5% | 58.7% | <p> The wharepuni was the family sleeping house. It was made with a wooden frame and covered with raupō or nıkau l ¦ <p> The chief’s family had a bigger whare with beautiful carvings on the outside. If there was no wharenui in the  ¦ <p> Cooking and eating was always done outside. Māori had no stoves or metal pots. They had kete and kumete to gat |
| MXDI101_5.0.html | Standard | Standard | no KB family | 13 | 8 | 61.5% | 56.5% | <p> Here are six groups of two lollipops. ¦ <p> Here are three rows of five flowers: ¦ <p> Here are six rows of 10 trees: |
| ANZH104_03.0.html | Standard | Standard | no KB family | 10 | 6 | 60.0% | 76.7% | <p> In the early days, most of the clothing was made from harakeke or flax. Both women and men wore flax skirts. W ¦ <p> Chiefs wore cloaks made with dog skin and dog hair. bird feathers were used to decorate the cloaks. ¦ <p> Māori often wore earrings and necklaces made of shells, bone and pounamu. Men wore their hair in a topknot and |
| HIS1001-0.0.html | Standard | Standard | no KB family | 10 | 6 | 60.0% | 52.3% | <h1> HIS1001 ¦ <h1> Karihi Te moana-nui-a-kiwa ¦ <p> He moana tātou, he moana waiwai. Ko te ao moana, ko tātou tērā. |
| MXEX301_03.0.html | Standard | Standard | no KB family | 74 | 44 | 59.5% | 21.7% | <h4> Depth ¦ <h4> Perimeter ¦ <h4> Thickness |
| MXDB301_6.0.html | Standard | Standard | no KB family | 39 | 23 | 59.0% | 27.7% | <li> calculate the surface area for 3D shapes. ¦ <li> calculating the surface area of 3D shapes by calculating area of a 2D net. ¦ <p> Packaging relies on three-dimensional shapes, some of which you will already know. However, there may be a few |
| PES1003_4.0.html | Standard | Standard | no KB family | 36 | 21 | 58.3% | 43.0% | <p> Go to your journal and complete Activity 4A. ¦ <th> Thermal conductivity (watts per metre per degree Celsius (W/m/°C)) ¦ <td> Copper |
| XDLS902.00.html | Standard | Combo | LS (14.6) | 24 | 14 | 58.3% | 69.3% | <h1> XDLS9002 ¦ <p> He hauora te taonga ¦ <p> Health is a treasure |
| HES1002_2_0.html | Standard | Standard | no KB family | 12 | 7 | 58.3% | 66.0% | <h1> Health and wellbeing models ¦ <h3> What is a health model? ¦ <p> A health or wellbeing model basically breaks down the different parts or aspects of being healthy or well. For |
| XGF9004-04.0.html | Standard | Combo | X-prefixed other (learningSupport) | 63 | 36 | 57.1% | 36.5% | <h1> Flexible thinking ¦ <h4> Key question ¦ <h2> Problem solving |
| PES1003_1.0.html | Standard | Standard | no KB family | 42 | 24 | 57.1% | 35.9% | <h3> Hands-on activity: see it melt ¦ <p> Download the learning journal and complete the practical activity 1A. ¦ <h3> Solid to liquid – melting |
| MXEX401_04.0.html | Standard | Standard | no KB family | 35 | 20 | 57.1% | 26.0% | <p> The longest side of a right angled triangle is called a hypotenuse. It is always opposite the right angle (not ¦ <h3> Identifying the hypotenuse ¦ <p> Click on the hypotenuse of each of the right-angled triangles shown below. |
| MXFL203_5.0.html | Standard | Standard | no KB family | 73 | 41 | 56.2% | 55.9% | <li> Show ²⁄₂ ¦ <p> 1½ ¦ <p> 2½ |
| XGF9004-02.0.html | Standard | Combo | X-prefixed other (learningSupport) | 93 | 51 | 54.8% | 26.6% | <p> Being organised helps your brain stay calm, focused, and ready to learn. It’s more than just having a tidy spa ¦ <p> When you are well-organised, you can complete tasks more efficiently, reduce stress, and have more time for ac ¦ <h3> Skills for organisation |
| HIS1001-10.0.html | Standard | Standard | no KB family | 62 | 33 | 53.2% | 26.7% | <li> synthesise evidence from sources to write a paragraph ¦ <li> examine the collective remembrance of historic events (maumaharatanga). ¦ <li> identifying the parts of a paragraph |
| MUS1004_1_1.html | Standard | Standard | no KB family | 19 | 10 | 52.6% | 38.1% | <p> Listen to these basic rhythmic patterns all in the simple time meter of 4 crotchet beats to a bar. ¦ <th> Comment ¦ <td> Crotchets and minims (half and quarter notes). |

## Worst modules by mean NET no-source share (paired pages; top 40)

| module | pages | mean NET no-source share |
|---|---|---|
| CHI1003 | 9 | 82.1% |
| CHI1004 | 9 | 77.3% |
| CHI1005 | 8 | 77.2% |
| HES1002 | 7 | 65.1% |
| CEDO301 | 4 | 62.7% |
| SSFUN07 | 3 | 61.1% |
| SPA1004 | 3 | 56.3% |
| XDLS501 | 4 | 47.6% |
| XGF9004 | 7 | 46.0% |
| HIS1001 | 8 | 45.1% |
| PHE1004 | 4 | 41.5% |
| ART1006 | 4 | 39.4% |
| ART1003 | 1 | 38.9% |
| ANZH302 | 11 | 38.4% |
| TWHA904 | 1 | 37.4% |
| ANZH104 | 8 | 36.9% |
| HPFUN101 | 1 | 35.3% |
| SSFUN05 | 1 | 33.7% |
| ENG1005 | 1 | 33.3% |
| PHE1001 | 5 | 31.9% |
| TWHA901 | 1 | 31.6% |
| XWHA01 | 2 | 29.9% |
| EXBP901 | 5 | 29.6% |
| WJFUN105 | 1 | 28.6% |
| TWHA903 | 1 | 28.6% |
| ANZH103 | 2 | 28.3% |
| MXEX301 | 8 | 27.8% |
| MXDB301 | 6 | 26.8% |
| PWYWHA1 | 1 | 26.7% |
| TWHA905 | 1 | 26.6% |
| PHE1003 | 8 | 25.7% |
| XFUN01 | 1 | 25.3% |
| PES1007 | 10 | 24.6% |
| WJFUN108 | 1 | 24.5% |
| HES1005 | 8 | 24.0% |
| MXFU202 | 10 | 24.0% |
| XDLS909 | 5 | 23.0% |
| HPFUN401 | 1 | 22.9% |
| WJFUN106 | 1 | 22.4% |
| MXFL401 | 8 | 22.0% |
