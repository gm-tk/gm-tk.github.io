# Round 0 — THE CEILING (what no converter rule can ever close)

Generated 2026-09-24 14:26:42 by `outputs/_measure_ceiling.py`. Modules measured 512 / requested 540; without a parsed WT (skipped): TRR115, ENGJ403, GER1003, GER1004, GER1005, GER1006, GER1007, SAM1005, SAM1006; parsed files present but none looks like a Writers Template (skipped): TRR102, TRR103, TRR104, TRR105, TRR107, TRR108, TRR109, TRR111, TRR112, TRR113, TRR203, TRR301, TRR304, XOTPG01, XOTPG03, XOTPG04, XOTPG05, XOTPG06; modules read from the UNION of 203×2+ parsed files; gold-only (no Claude dir, never paired): 0.

**Plain English.** A *block* is one piece of text on the human's finished page (a heading, a paragraph, a bullet, a table cell). A block has a *source* when the same words — or a distinctive run of them — appear anywhere in the writer's template. Blocks with **no source** were written by the developer (verbal feedback, house copy): no rule that reads the template can produce them. **Boilerplate** is no-source text that recurs across many modules (a convention a rule CAN emit), so the honest ceiling removes it (**net**). *Scaffold scope* ignores text inside interactive widgets, because the primary skeleton gate ignores widget internals too.

## Headline (the PAIRED population — the pages the skeleton gate scores)

- pages 2414 / modules 512 / text blocks (scaffold scope) 112495
- no-source share, scaffold scope: per-page mean **raw 10.9% → net 8.3%** (pooled raw 10.0% → net 8.2%)
- no-source share, full scope (widget internals included): per-page mean raw 15.8% → net 12.6%
- **CEILING (scaffold) = 91.7%** (round-110 test) — loose upper bound 94.3% (every content word of the block found somewhere in the WT) · ceiling (full) = 87.4% / loose 89.8%
- baseline `_r465_sk_final.json` (2487 pairs): SCAFFOLD mean 55.252% / RAW mean 39.193%
- **SCAFFOLD 55.25% = 60.2% of achievable** (band 58.6%–60.2%: the loose ceiling gives the lower figure); RAW 39.19% = 44.8% of its own ceiling (band 43.7%–44.8%); per-page mean of (score ÷ own ceiling) = 60.7% over 2413 joined pages

| population | pages | modules | blocks (scaffold) | mean no-source raw | mean no-source NET | mean no-source LOOSE | ceiling (scaffold) | ceiling loose | mean full raw | mean full NET |
|---|---|---|---|---|---|---|---|---|---|---|
| paired (gate population) | 2414 | 512 | 112495 | 10.9% | 8.3% | 5.7% | 91.7% | 94.3% | 15.8% | 12.6% |
| compare_set ∩ paired | 995 | 198 | 46928 | 10.8% | 8.1% | 5.5% | 91.9% | 94.5% | 15.5% | 12.5% |
| ALL gold pages with a WT | 2751 | 512 | 126200 | 13.0% | 10.3% | 7.4% | 89.7% | 92.6% | 17.6% | 14.4% |

## By Template family (folder) — paired population

| group | pages | modules | mean no-source raw | mean no-source NET | mean LOOSE | ceiling | ceiling loose | pooled NET |
|---|---|---|---|---|---|---|---|---|
| Standard | 2171 | 362 | 11.2% | 8.4% | 5.9% | 91.6% | 94.1% | 8.3% |
| Fundamentals | 111 | 81 | 9.0% | 7.3% | 4.8% | 92.7% | 95.2% | 9.0% |
| Inquiry | 94 | 60 | 9.3% | 7.0% | 4.6% | 93.0% | 95.4% | 6.8% |
| Bilingual | 38 | 9 | 5.8% | 5.7% | 3.1% | 94.3% | 96.9% | 5.7% |

## By HTML sub-type (KB 06) — paired population

| group | pages | modules | mean no-source raw | mean no-source NET | mean LOOSE | ceiling | ceiling loose | pooled NET |
|---|---|---|---|---|---|---|---|---|
| Standard | 2030 | 342 | 11.3% | 8.5% | 5.9% | 91.5% | 94.1% | 8.3% |
| Combo | 173 | 27 | 9.0% | 6.9% | 4.6% | 93.1% | 95.4% | 7.7% |
| Fundamentals | 107 | 82 | 9.4% | 7.7% | 5.1% | 92.3% | 94.9% | 9.2% |
| Inquiry | 66 | 61 | 8.9% | 7.7% | 5.7% | 92.3% | 94.3% | 7.1% |
| Bilingual | 38 | 9 | 5.8% | 5.7% | 3.1% | 94.3% | 96.9% | 5.7% |

## By Legacy (True) vs Refresh (False) — paired population

| group | pages | modules | mean no-source raw | mean no-source NET | mean LOOSE | ceiling | ceiling loose | pooled NET |
|---|---|---|---|---|---|---|---|---|
| False | 2414 | 512 | 10.9% | 8.3% | 5.7% | 91.7% | 94.3% | 8.2% |

## By KB subject family (14.x, prefix heuristic) — paired population

| group | pages | modules | mean no-source raw | mean no-source NET | mean LOOSE | ceiling | ceiling loose | pooled NET |
|---|---|---|---|---|---|---|---|---|
| no KB family | 1544 | 247 | 11.9% | 9.4% | 6.4% | 90.6% | 93.6% | 9.4% |
| BLL (14.7) | 298 | 109 | 8.1% | 3.7% | 3.0% | 96.3% | 97.0% | 3.0% |
| X-prefixed other (learningSupport) | 127 | 25 | 10.5% | 7.8% | 5.4% | 92.2% | 94.6% | 9.0% |
| CED (14.4) | 108 | 29 | 9.0% | 6.5% | 4.2% | 93.5% | 95.8% | 5.5% |
| LS (14.6) | 104 | 18 | 12.4% | 9.7% | 6.8% | 90.3% | 93.2% | 9.8% |
| Languages (14.1) | 85 | 19 | 9.2% | 7.0% | 5.8% | 93.0% | 94.2% | 6.9% |
| Pathways (14.2) | 46 | 6 | 4.8% | 3.6% | 3.3% | 96.4% | 96.7% | 3.2% |
| MiW/WJ (14.10) | 21 | 21 | 8.8% | 7.1% | 5.3% | 92.9% | 94.7% | 5.5% |
| BLLR (14.9) | 21 | 3 | 7.9% | 5.4% | 4.2% | 94.6% | 95.8% | 3.2% |
| HPE content (14.8) | 21 | 2 | 3.8% | 2.5% | 2.4% | 97.5% | 97.6% | 1.7% |
| Taonga/Arts (14.3) | 16 | 10 | 23.3% | 21.6% | 16.9% | 78.4% | 83.1% | 20.1% |
| H&PE FUNdamentals (14.5) | 15 | 15 | 11.7% | 10.9% | 6.4% | 89.1% | 93.6% | 12.2% |
| Technology (14.12) | 8 | 8 | 8.4% | 7.5% | 4.8% | 92.5% | 95.2% | 7.0% |

## By Subject (Module_Structure_Index) — paired population

| group | pages | modules | mean no-source raw | mean no-source NET | mean LOOSE | ceiling | ceiling loose | pooled NET |
|---|---|---|---|---|---|---|---|---|
| NCEA1 | 543 | 74 | 14.5% | 12.5% | 8.9% | 87.5% | 91.1% | 12.5% |
| 1-10 Mathematics | 338 | 42 | 12.5% | 10.4% | 6.6% | 89.6% | 93.4% | 12.1% |
| 1-10 English | 333 | 52 | 9.3% | 6.1% | 4.0% | 93.9% | 96.0% | 6.5% |
| 1-10 Blended Literacy | 319 | 112 | 8.1% | 3.8% | 3.1% | 96.2% | 96.9% | 3.0% |
| Leaving to Learn | 231 | 43 | 11.3% | 8.7% | 6.0% | 91.3% | 94.0% | 9.4% |
| Online Safety (OS9000) | 136 | 29 | 5.4% | 2.8% | 2.4% | 97.2% | 97.6% | 2.4% |
| ConnectED | 108 | 29 | 9.0% | 6.5% | 4.2% | 93.5% | 95.8% | 5.5% |
| ANZH | 95 | 13 | 17.0% | 14.6% | 11.6% | 85.4% | 88.4% | 13.9% |
| 1-10 Languages | 65 | 16 | 6.6% | 4.3% | 3.2% | 95.7% | 96.8% | 4.6% |
| 1-10 Social Science | 61 | 14 | 13.4% | 6.9% | 3.8% | 93.1% | 96.2% | 5.3% |
| Te Marautanga o Aotearoa TMoA | 38 | 9 | 5.8% | 5.7% | 3.1% | 94.3% | 96.9% | 5.7% |
| 1-10 Health and PE | 36 | 17 | 7.1% | 6.0% | 4.1% | 94.0% | 95.9% | 7.7% |
| 1-10 Science | 33 | 5 | 6.0% | 3.3% | 2.4% | 96.7% | 97.6% | 3.9% |
| 1-10 Technology | 24 | 10 | 7.3% | 6.3% | 3.6% | 93.7% | 96.4% | 7.0% |
| 1-10 Writing (MiW) | 21 | 21 | 8.8% | 7.1% | 5.3% | 92.9% | 94.7% | 5.5% |
| EXPlore | 15 | 8 | 13.6% | 13.4% | 7.4% | 86.6% | 92.6% | 8.1% |
| Te ara Whakapuawa -Wellbeing | 13 | 13 | 14.0% | 13.8% | 10.8% | 86.2% | 89.2% | 15.4% |
| 1-10 Arts | 5 | 5 | 8.5% | 5.3% | 2.6% | 94.7% | 97.4% | 5.5% |

## By Series prefix — paired population

| group | pages | modules | mean no-source raw | mean no-source NET | mean LOOSE | ceiling | ceiling loose | pooled NET |
|---|---|---|---|---|---|---|---|---|
| BLL | 298 | 109 | 8.1% | 3.7% | 3.0% | 96.3% | 97.0% | 3.0% |
| MXFL | 99 | 11 | 9.1% | 7.8% | 4.7% | 92.2% | 95.3% | 8.3% |
| ANZH | 94 | 12 | 16.9% | 14.5% | 11.5% | 85.5% | 88.5% | 13.6% |
| ENGI | 84 | 12 | 10.1% | 6.2% | 4.8% | 93.8% | 95.2% | 6.4% |
| ENGC | 81 | 10 | 8.4% | 5.7% | 3.8% | 94.3% | 96.2% | 6.4% |
| HIS | 77 | 8 | 9.7% | 8.5% | 6.0% | 91.5% | 94.0% | 7.9% |
| PES | 76 | 7 | 14.0% | 11.3% | 8.3% | 88.7% | 91.7% | 13.7% |
| XDLS | 75 | 12 | 14.2% | 11.2% | 7.6% | 88.8% | 92.4% | 11.1% |
| AGH | 74 | 9 | 11.7% | 10.9% | 7.0% | 89.1% | 93.0% | 12.3% |
| ENGS | 64 | 9 | 10.2% | 6.7% | 4.4% | 93.3% | 95.6% | 6.7% |
| MXFU | 58 | 6 | 12.7% | 11.5% | 7.8% | 88.5% | 92.2% | 12.8% |
| MXDI | 55 | 6 | 12.3% | 10.0% | 5.2% | 90.0% | 94.8% | 10.2% |
| ENGJ | 50 | 7 | 7.4% | 4.5% | 2.3% | 95.5% | 97.7% | 4.7% |
| PHE | 50 | 8 | 24.7% | 22.5% | 16.6% | 77.5% | 83.4% | 22.6% |
| HES | 48 | 6 | 22.6% | 20.2% | 16.2% | 79.8% | 83.8% | 17.1% |
| ENGR | 46 | 6 | 10.0% | 7.3% | 3.9% | 92.7% | 96.1% | 6.8% |
| PWY | 45 | 5 | 4.2% | 3.1% | 2.8% | 96.9% | 97.2% | 2.4% |
| MXDB | 42 | 5 | 12.4% | 9.6% | 6.5% | 90.4% | 93.5% | 9.8% |
| MXEX | 41 | 6 | 20.4% | 16.6% | 11.2% | 83.4% | 88.8% | 22.8% |
| XGF | 41 | 5 | 9.9% | 8.7% | 6.1% | 91.3% | 93.9% | 12.4% |
| CEDO | 40 | 9 | 13.4% | 11.6% | 7.8% | 88.4% | 92.2% | 5.7% |
| MXEO | 40 | 5 | 12.0% | 9.9% | 6.6% | 90.1% | 93.4% | 10.1% |
| XMES | 39 | 6 | 8.9% | 7.3% | 4.8% | 92.7% | 95.2% | 6.6% |
| CBI | 31 | 4 | 6.5% | 5.0% | 3.0% | 95.0% | 97.0% | 3.7% |
| XLP | 29 | 6 | 7.5% | 5.9% | 4.7% | 94.1% | 95.3% | 6.0% |
| FRFUN | 28 | 3 | 6.7% | 4.1% | 2.7% | 95.9% | 97.3% | 3.7% |
| DAN | 28 | 3 | 18.1% | 13.5% | 5.3% | 86.5% | 94.7% | 15.2% |
| SSOG | 28 | 4 | 17.0% | 4.6% | 1.7% | 95.4% | 98.3% | 3.0% |
| CEDT | 27 | 8 | 6.1% | 3.2% | 1.7% | 96.8% | 98.3% | 5.9% |
| COM | 25 | 3 | 15.0% | 11.0% | 6.7% | 89.0% | 93.3% | 11.6% |
| TRR | 23 | 4 | 6.3% | 6.2% | 3.2% | 93.8% | 96.8% | 5.6% |
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
| SSCI | 17 | 2 | 3.1% | 1.0% | 0.7% | 99.0% | 99.3% | 0.8% |
| GEO | 16 | 3 | 8.0% | 6.2% | 5.4% | 93.8% | 94.6% | 4.4% |
| OSSM | 16 | 3 | 4.2% | 1.3% | 1.3% | 98.7% | 98.7% | 0.7% |
| TEDC | 16 | 2 | 6.7% | 5.8% | 3.1% | 94.2% | 96.9% | 7.0% |
| HPFUN | 15 | 15 | 11.7% | 10.9% | 6.4% | 89.1% | 93.6% | 12.2% |
| OSAH | 15 | 3 | 6.4% | 3.0% | 3.0% | 97.0% | 97.0% | 2.7% |
| OSSC | 15 | 3 | 6.7% | 4.6% | 4.6% | 95.4% | 95.4% | 3.7% |
| CEDK | 14 | 4 | 5.3% | 2.3% | 1.5% | 97.7% | 98.5% | 2.8% |
| CEDR | 14 | 5 | 4.6% | 2.8% | 1.7% | 97.2% | 98.3% | 3.8% |
| CEDW | 13 | 3 | 10.3% | 6.7% | 3.8% | 93.3% | 96.2% | 10.6% |
| MUS | 12 | 2 | 16.4% | 14.3% | 9.7% | 85.7% | 90.3% | 12.8% |
| XOTPB | 12 | 6 | 19.5% | 5.9% | 4.9% | 94.1% | 95.1% | 5.9% |
| PNR | 11 | 4 | 3.9% | 3.7% | 2.3% | 96.3% | 97.7% | 3.3% |
| ART | 11 | 5 | 30.0% | 29.0% | 23.4% | 71.0% | 76.6% | 46.5% |
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
| MXFUN | 3 | 3 | 20.9% | 14.1% | 8.5% | 85.9% | 91.5% | 26.2% |
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

## Boilerplate — no-source text recurring in ≥ 5 modules (168 strings; top 60)

These are conventions a rule can emit (most are documented in the KB); they are removed from the NET figures.

| modules | text |
|---|---|
| 482 | acknowledgements |
| 404 | every effort has been made to acknowledge and contact copyright holders te aho o te kura pounamu apologises for any omis |
| 402 | copyright board of trustees of te aho o te kura pounamu private bag 39992 wellington mail centre lower hutt 5045 new zea |
| 376 | all other images te aho o te kura pounamu wellington new zealand |
| 146 | select one |
| 116 | 02 |
| 116 | 01 |
| 90 | image avatar heygen wwwheygencom used with permission |
| 74 | 03 |
| 73 | how will i know if ive learned it |
| 70 | 40 |
| 67 | 04 |
| 64 | 20 |
| 63 | 50 |
| 57 | 30 |
| 52 | 70 |
| 52 | 60 |
| 51 | all illustrations te aho o te kura pounamu wellington new zealand |
| 51 | 10 |
| 49 | standards |
| 48 | 05 |
| 42 | want to know where to start |
| 39 | unable to display pdf file download here |
| 38 | 80 |
| 34 | learning intentions |
| 33 | 06 |
| 32 | click here to view a basic year plan talk to your kaiako about creating a specific learning plan to meet your needs |
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

## Outlier pages — paired pages whose NET no-source share ≥ 50% with ≥ 8 blocks (52 pages; top 60)

These pages will score low against gold no matter what the converter does; the samples show the developer-authored text.

| page | family | sub-type | KB family | blocks | no-source (net) | share | skeleton score | samples of unsourced text |
|---|---|---|---|---|---|---|---|---|
| HES1002_3_0.html | Standard | Standard | no KB family | 37 | 35 | 94.6% | 43.5% | <h1> Pacific Health Models ¦ <p> O le tele o sulu e maua ai se figota, e mama se avega pe a ta amo fa’atasi ¦ <p> My strength does not come from me alone, but from many. |
| HES1002_4_0.html | Standard | Standard | no KB family | 14 | 13 | 92.9% | 45.0% | <h1> Pacific Health Models ¦ <h1> Pacific Health Models ¦ <h3> More Examples of Pacific Models of Health: |
| DTC1005_2_0.html | Standard | Standard | no KB family | 17 | 15 | 88.2% | 70.6% | <h3> Manage data ¦ <p> Databases are incredibly widespread – they underlie technology used by most people every day if not every hour ¦ <p> Databases sit behind a huge number of websites and they're a crucial component of, for example: |
| XGF9004-06.0.html | Standard | Combo | X-prefixed other (learningSupport) | 59 | 52 | 88.1% | 34.8% | <h1> Brain Boosters – Resources and Games ¦ <p> Games help your brain stretch, flex, and grow stronger, just like muscles do when you exercise. ¦ <p> No matter your age – five, fifteen, or older – this section has something for everyone. Start with board and c |
| CEDO301_3.0.html | Standard | Standard | CED (14.4) | 28 | 24 | 85.7% | 49.1% | <h1> Science Investigation ¦ <h3> Testing my idea ¦ <p> Designer note: Link to be updated to orgunit link |
| DAN1006_7_0.html | Standard | Standard | no KB family | 24 | 20 | 83.3% | 43.2% | <h1> Rehearsing the sequence ¦ <p> Go through your sequence and decide on your counts, listen for musical cues if you are using music. ¦ <p> Rehearse your dance focusing on the counts and cues – count out loud as you rehearse. |
| SPA1004_3_0.html | Standard | Standard | Languages (14.1) | 120 | 97 | 80.8% | 17.1% | <h1> ¿Qué Vamos A Hacer? ¦ <h1> What Are We Going To Do? ¦ <h2> Los planes para la fiesta... ¦ Plans for the party... |
| HES1002_6_0.html | Standard | Standard | no KB family | 20 | 16 | 80.0% | 46.8% | <h1> My Model of Wellbeing/Health ¦ <p> Create your own model of wellbeing. ¦ <li> Take another look at the different models of wellbeing/health that you have learnt about in this topic. Decide |
| ART1006_2.0.html | Standard | Standard | Taonga/Arts (14.3) | 125 | 98 | 78.4% | 22.5% | <h1> Plan your Project ¦ <p> Once completed upload this to your internal portfolio. ¦ <h4> City of Dreams Mural |
| PHE1004_3.0.html | Standard | Standard | no KB family | 17 | 13 | 76.5% | 52.5% | <h1> Time for Action ¦ <h3> So they say practice makes perfect! ¦ <p> Include and provide supporting evidence/examples by using photos and or video footage. These reflections and r |
| MXEX301_05.0.html | Standard | Standard | no KB family | 43 | 31 | 72.1% | 22.5% | <p> A line is straight and has no beginning or end point. It is infinite. When you draw a line, you put arrows at  ¦ <p> This line can be named using two points on it. It can be called line AB or ¦ <p> A ray is a part of a line. It starts at a point and extends in one direction forever. |
| SPA1004_0_0.html | Standard | Standard | Languages (14.1) | 14 | 10 | 71.4% | 63.5% | <p> E rere te huata, kapohia ¦ <p> Aprovecha al máximo cada oportunidad. Make the most of every opportunity. ¦ <h3> ¿Tienes alguna idea? ¦ Do you have any ideas? |
| HES1002_1_0.html | Standard | Standard | no KB family | 17 | 12 | 70.6% | 50.4% | <h1> Let’s recap ¦ <h3> Let's recap ¦ <p> Kupu Māori meanings for hauora, oranga, mauri and waiora are from Te Aka Māori Dictionary. |
| XGF9004-03.0.html | Standard | Combo | X-prefixed other (learningSupport) | 134 | 92 | 68.7% | 23.8% | <h1> Self-monitoring ¦ <h2> Self-monitoring ¦ <p> Self-monitoring is about noticing your thoughts, actions, and feelings and making changes when needed. You hav |
| DTC1005_3_0.html | Standard | Standard | no KB family | 35 | 24 | 68.6% | 53.7% | <p> Websites can be used: ¦ <li> to sell products ¦ <li> to buy products |
| ART1006_4.0.html | Standard | Standard | Taonga/Arts (14.3) | 98 | 65 | 66.3% | 19.5% | <p> Required: 1–2 A4 pages of notes and drawings ¦ Time: 1 hour. ¦ <p> Here are two examples of how other ākonga have assessed their projects. ¦ <h4> Passion Project Self-Assessment Rubric |
| MXEX301_03.1.html | Standard | Standard | no KB family | 38 | 25 | 65.8% | 23.0% | <p> This is a very small amount. A teaspoon holds about five millilitres. ¦ <p> 1000 millilitres is called a litre. ¦ <p> This is the basic unit for capacity. A carton of milk holds a litre. |
| XDLS501.01.html | Standard | Standard | LS (14.6) | 35 | 23 | 65.7% | 31.1% | <li> that the space between us and others depends on who they are ¦ <li> that the space between us and others depends on where we are ¦ <li> that intimate information and intimate space is for special people in our lives. |
| EXBP901_1.1.html | Standard | Standard | no KB family | 47 | 30 | 63.8% | 25.9% | <h1> The Learning Cycle ¦ <h4> Learning objective ¦ <p> You will complete a quiz about the learning cycle. |
| XDLS501.04.html | Standard | Standard | LS (14.6) | 63 | 40 | 63.5% | 16.4% | <h1> Conflict Resolution ¦ <li> how to strive towards peace ¦ <li> how to negotiate things you want and need. |
| HES1002_5_0.html | Standard | Standard | no KB family | 24 | 15 | 62.5% | 38.0% | <h4> The Model ¦ <p> It is a visual representation of Pasifika values and beliefs. It uses the Samoan fale or house to describe the ¦ <h3> Fonofale – join ‘Pale in the Fale’ |
| PHE1001_3.0.html | Standard | Standard | no KB family | 24 | 15 | 62.5% | 69.2% | <p> What are external cues? External cues are unpredictable influences or factors that we might face in a game or  ¦ <p> Some external cues could be: ¦ <li> environmental factors |
| HES1005_7.0.html | Standard | Standard | no KB family | 45 | 28 | 62.2% | 40.0% | <h1> Oranga Taihema ¦ <p> This lesson is not compulsory. If you have any concerns or queries about the topics of sexuality or gender ide ¦ <h3> What should Jo choose? |
| MXFL204_6.0.html | Standard | Standard | no KB family | 26 | 16 | 61.5% | 39.7% | <p> The line graph below shows how a puppy’s weight has changed as it grows each week. ¦ <h5> In this line graph: ¦ <li> The horizontal axis (x-axis), the one along the bottom represents the time. In this graph, the puppy’s age in  |
| ANZH104_02.0.html | Standard | Standard | no KB family | 13 | 8 | 61.5% | 58.7% | <p> The wharepuni was the family sleeping house. It was made with a wooden frame and covered with raupō or nıkau l ¦ <p> The chief’s family had a bigger whare with beautiful carvings on the outside. If there was no wharenui in the  ¦ <p> Cooking and eating was always done outside. Māori had no stoves or metal pots. They had kete and kumete to gat |
| MXDI101_5.0.html | Standard | Standard | no KB family | 13 | 8 | 61.5% | 56.5% | <p> Here are six groups of two lollipops. ¦ <p> Here are three rows of five flowers: ¦ <p> Here are six rows of 10 trees: |
| ANZH104_03.0.html | Standard | Standard | no KB family | 10 | 6 | 60.0% | 71.2% | <p> In the early days, most of the clothing was made from harakeke or flax. Both women and men wore flax skirts. W ¦ <p> Chiefs wore cloaks made with dog skin and dog hair. bird feathers were used to decorate the cloaks. ¦ <p> Māori often wore earrings and necklaces made of shells, bone and pounamu. Men wore their hair in a topknot and |
| HIS1001-0.0.html | Standard | Standard | no KB family | 10 | 6 | 60.0% | 52.3% | <h1> HIS1001 ¦ <h1> Karihi Te moana-nui-a-kiwa ¦ <p> He moana tātou, he moana waiwai. Ko te ao moana, ko tātou tērā. |
| MXEX301_03.0.html | Standard | Standard | no KB family | 74 | 44 | 59.5% | 21.7% | <h4> Depth ¦ <h4> Perimeter ¦ <h4> Thickness |
| MXDB301_6.0.html | Standard | Standard | no KB family | 39 | 23 | 59.0% | 16.5% | <li> calculate the surface area for 3D shapes. ¦ <li> calculating the surface area of 3D shapes by calculating area of a 2D net. ¦ <p> Packaging relies on three-dimensional shapes, some of which you will already know. However, there may be a few |
| PES1003_4.0.html | Standard | Standard | no KB family | 36 | 21 | 58.3% | 43.0% | <p> Go to your journal and complete Activity 4A. ¦ <th> Thermal conductivity (watts per metre per degree Celsius (W/m/°C)) ¦ <td> Copper |
| XDLS902.00.html | Standard | Combo | LS (14.6) | 24 | 14 | 58.3% | 69.3% | <h1> XDLS9002 ¦ <p> He hauora te taonga ¦ <p> Health is a treasure |
| HES1002_2_0.html | Standard | Standard | no KB family | 12 | 7 | 58.3% | 62.4% | <h1> Health and wellbeing models ¦ <h3> What is a health model? ¦ <p> A health or wellbeing model basically breaks down the different parts or aspects of being healthy or well. For |
| XGF9004-04.0.html | Standard | Combo | X-prefixed other (learningSupport) | 63 | 36 | 57.1% | 37.3% | <h1> Flexible thinking ¦ <h4> Key question ¦ <h2> Problem solving |
| PES1003_1.0.html | Standard | Standard | no KB family | 42 | 24 | 57.1% | 35.9% | <h3> Hands-on activity: see it melt ¦ <p> Download the learning journal and complete the practical activity 1A. ¦ <h3> Solid to liquid – melting |
| MXEX401_04.0.html | Standard | Standard | no KB family | 35 | 20 | 57.1% | 26.0% | <p> The longest side of a right angled triangle is called a hypotenuse. It is always opposite the right angle (not ¦ <h3> Identifying the hypotenuse ¦ <p> Click on the hypotenuse of each of the right-angled triangles shown below. |
| MXFL203_5.0.html | Standard | Standard | no KB family | 73 | 41 | 56.2% | 53.8% | <li> Show ²⁄₂ ¦ <p> 1½ ¦ <p> 2½ |
| XGF9004-02.0.html | Standard | Combo | X-prefixed other (learningSupport) | 93 | 51 | 54.8% | 26.6% | <p> Being organised helps your brain stay calm, focused, and ready to learn. It’s more than just having a tidy spa ¦ <p> When you are well-organised, you can complete tasks more efficiently, reduce stress, and have more time for ac ¦ <h3> Skills for organisation |
| HIS1001-10.0.html | Standard | Standard | no KB family | 62 | 33 | 53.2% | 26.7% | <li> synthesise evidence from sources to write a paragraph ¦ <li> examine the collective remembrance of historic events (maumaharatanga). ¦ <li> identifying the parts of a paragraph |
| MUS1004_1_1.html | Standard | Standard | no KB family | 19 | 10 | 52.6% | 38.1% | <p> Listen to these basic rhythmic patterns all in the simple time meter of 4 crotchet beats to a bar. ¦ <th> Comment ¦ <td> Crotchets and minims (half and quarter notes). |
| ENGS404_4_0.html | Standard | Standard | no KB family | 50 | 26 | 52.0% | 33.5% | <p> The aim of writing is to have someone to read it. If you don’t use standard conventions of punctuation, senten ¦ <p> For example: “I will see you later,” Marama shouted. ¦ <li> put every word that was spoken inside speech marks |
| PHE1006_5.0.html | Standard | Standard | no KB family | 25 | 13 | 52.0% | 37.0% | <h1> Movement Experiences and Context ¦ <p> If we take the example of basketball, some movement experience examples would be basketball drills (like learn ¦ <p> Click below to see how a context wouldn’t work, and also how it would work. |
| HIS1001-9.0.html | Standard | Standard | no KB family | 52 | 27 | 51.9% | 28.3% | <li> identify perspectives in the historic records. ¦ <li> identifying evidence of perspectives in primary sources ¦ <li> explaining why a person or group holds the perspective they do. |
| MXFU202_7.0.html | Standard | Standard | no KB family | 120 | 62 | 51.7% | 36.0% | <h1> Times Table Relationships ¦ <li> spot patterns in multiplication and use patterns to solve problems faster. ¦ <h3> 3 × 3 basketball |
| MXDB301_8.0.html | Standard | Standard | no KB family | 35 | 18 | 51.4% | 29.2% | <li> design a package to specifications. ¦ <li> creating a presentation that includes a net, the surface area and the volume of the package. ¦ <p> Follow the steps below to give you some ideas and guidance for how to tackle this task. |
| XGF9004-05.0.html | Standard | Combo | X-prefixed other (learningSupport) | 72 | 37 | 51.4% | 27.5% | <h1> Working memory ¦ <p> What helps you make good decisions when you have choices to make? ¦ <p> Working memory is like a mental sticky note – it holds onto information just long enough for you to use it. Yo |
| XDLS501.03.html | Standard | Standard | LS (14.6) | 86 | 43 | 50.0% | 30.6% | <p> Mindfulness is about taking a moment to pause and pay attention to what we’re doing, feeling, and thinking. It ¦ <p> Some people use a prop to help ground them. For example, you might love Star Wars and keep a Yoda toy in your  ¦ <h3> The way you live: personal conduct |
| AGH1003_07.0.html | Standard | Standard | no KB family | 60 | 30 | 50.0% | 45.4% | <h3> Why is good drainage important? ¦ <p> Good drainage is crucial for agriculture and horticulture success for many reasons. ¦ <h3> Poor drainage |
| MXFU302_7.0.html | Standard | Standard | no KB family | 22 | 11 | 50.0% | 33.0% | <p> Designer note: Please provide information for the drop down ^^^^ ¦ <h3> Writing rules using algebra ¦ <p> This video shows some examples of how to write rules using algebra. |
| ANZH104_01.0.html | Standard | Standard | no KB family | 12 | 6 | 50.0% | 62.8% | <h3> Important kupu ¦ <p> Before you begin the lesson, have a go at matching the English word to the Māori word. You can try this activi ¦ <h4> Early Māori life before Europeans arrived |
| DAN1006_4_0.html | Standard | Standard | no KB family | 12 | 6 | 50.0% | 67.6% | <h5> Video six ¦ <h5> Video seven ¦ <h5> Video eight |
| PHE1004_1.0.html | Standard | Standard | no KB family | 8 | 4 | 50.0% | 82.1% | <p> For example, tuakana-teina could look like grouping more experienced person/athlete (tuakana) with less experi ¦ <p> Another example could be providing opportunities for people/athletes to exercise rangatiratanga by participati ¦ <h3> Definitions of strategies promoting kotahitanga |

## Worst modules by mean NET no-source share (paired pages; top 40)

| module | pages | mean NET no-source share |
|---|---|---|
| HES1002 | 8 | 68.8% |
| CEDO301 | 4 | 62.7% |
| SSFUN07 | 3 | 61.1% |
| SPA1004 | 3 | 56.3% |
| XDLS501 | 4 | 47.6% |
| ART1006 | 5 | 47.2% |
| XGF9004 | 7 | 46.0% |
| HIS1001 | 8 | 45.1% |
| PHE1004 | 4 | 41.5% |
| ART1003 | 1 | 38.9% |
| ANZH302 | 11 | 38.4% |
| TWHA904 | 1 | 37.4% |
| ANZH104 | 8 | 36.9% |
| HPFUN101 | 1 | 35.3% |
| SSFUN05 | 1 | 33.7% |
| ENG1005 | 1 | 33.3% |
| PHE1001 | 5 | 31.9% |
| TWHA901 | 1 | 31.6% |
| MXDB301 | 7 | 30.3% |
| DAN1006 | 10 | 30.0% |
| XWHA01 | 2 | 29.9% |
| MXFUN01 | 1 | 29.8% |
| EXBP901 | 5 | 29.6% |
| MXEX301 | 9 | 29.2% |
| WJFUN105 | 1 | 28.6% |
| TWHA903 | 1 | 28.6% |
| ANZH103 | 2 | 28.3% |
| PWYWHA1 | 1 | 26.7% |
| PHE1003 | 8 | 26.6% |
| TWHA905 | 1 | 26.6% |
| XFUN01 | 1 | 25.3% |
| PES1007 | 10 | 24.6% |
| WJFUN108 | 1 | 24.5% |
| HES1005 | 8 | 24.0% |
| MXFU202 | 10 | 24.0% |
| XDLS909 | 5 | 23.0% |
| HPFUN401 | 1 | 22.9% |
| WJFUN106 | 1 | 22.4% |
| MXFL401 | 8 | 22.0% |
| MXEX401 | 7 | 21.9% |
