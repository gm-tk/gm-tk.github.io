# Round 0 — THE CEILING (what no converter rule can ever close)

Generated 2026-09-14 22:30:43 by `outputs/_measure_ceiling.py`. Modules measured 438 / requested 454; without a parsed WT (skipped): TRR115, ENGJ403; parsed files present but none looks like a Writers Template (skipped): TRR102, TRR103, TRR104, TRR105, TRR107, TRR108, TRR109, TRR111, TRR112, TRR113, TRR203, TRR301, TRR304; modules read from the UNION of 153×2+ parsed files; gold-only (no Claude dir, never paired): 38.

**Plain English.** A *block* is one piece of text on the human's finished page (a heading, a paragraph, a bullet, a table cell). A block has a *source* when the same words — or a distinctive run of them — appear anywhere in the writer's template. Blocks with **no source** were written by the developer (verbal feedback, house copy): no rule that reads the template can produce them. **Boilerplate** is no-source text that recurs across many modules (a convention a rule CAN emit), so the honest ceiling removes it (**net**). *Scaffold scope* ignores text inside interactive widgets, because the primary skeleton gate ignores widget internals too.

## Headline (the PAIRED population — the pages the skeleton gate scores)

- pages 1880 / modules 400 / text blocks (scaffold scope) 87502
- no-source share, scaffold scope: per-page mean **raw 11.1% → net 8.4%** (pooled raw 11.1% → net 9.2%)
- no-source share, full scope (widget internals included): per-page mean raw 16.2% → net 12.9%
- **CEILING (scaffold) = 91.6%** (round-110 test) — loose upper bound 94.2% (every content word of the block found somewhere in the WT) · ceiling (full) = 87.1% / loose 89.5%
- baseline `_r313_sk_final.json` (1939 pairs): SCAFFOLD mean 49.941% / RAW mean 34.430%
- **SCAFFOLD 49.94% = 54.5% of achievable** (band 53.0%–54.5%: the loose ceiling gives the lower figure); RAW 34.43% = 39.5% of its own ceiling (band 38.5%–39.5%); per-page mean of (score ÷ own ceiling) = 55.2% over 1879 joined pages

| population | pages | modules | blocks (scaffold) | mean no-source raw | mean no-source NET | mean no-source LOOSE | ceiling (scaffold) | ceiling loose | mean full raw | mean full NET |
|---|---|---|---|---|---|---|---|---|---|---|
| paired (gate population) | 1880 | 400 | 87502 | 11.1% | 8.4% | 5.8% | 91.6% | 94.2% | 16.2% | 12.9% |
| compare_set ∩ paired | 967 | 198 | 45515 | 10.8% | 8.2% | 5.5% | 91.8% | 94.5% | 15.3% | 12.5% |
| ALL gold pages with a WT | 2301 | 438 | 106511 | 12.5% | 9.7% | 6.9% | 90.3% | 93.1% | 17.4% | 14.1% |

## By Template family (folder) — paired population

| group | pages | modules | mean no-source raw | mean no-source NET | mean LOOSE | ceiling | ceiling loose | pooled NET |
|---|---|---|---|---|---|---|---|---|
| Standard | 1708 | 293 | 10.9% | 8.2% | 5.6% | 91.8% | 94.4% | 8.4% |
| Inquiry | 94 | 49 | 17.1% | 13.2% | 10.6% | 86.8% | 89.4% | 12.3% |
| Fundamentals | 64 | 53 | 10.4% | 8.9% | 4.9% | 91.1% | 95.1% | 10.7% |
| Bilingual | 14 | 5 | 5.1% | 4.9% | 4.0% | 95.1% | 96.0% | 7.2% |

## By HTML sub-type (KB 06) — paired population

| group | pages | modules | mean no-source raw | mean no-source NET | mean LOOSE | ceiling | ceiling loose | pooled NET |
|---|---|---|---|---|---|---|---|---|
| Standard | 1614 | 278 | 11.0% | 8.1% | 5.6% | 91.9% | 94.4% | 8.2% |
| Combo | 141 | 24 | 9.8% | 7.8% | 5.1% | 92.2% | 94.9% | 9.1% |
| Inquiry | 57 | 52 | 21.3% | 18.0% | 15.8% | 82.0% | 84.2% | 13.3% |
| Fundamentals | 54 | 54 | 10.8% | 9.5% | 5.8% | 90.5% | 94.2% | 11.1% |
| Bilingual | 14 | 5 | 5.1% | 4.9% | 4.0% | 95.1% | 96.0% | 7.2% |

## By Legacy (True) vs Refresh (False) — paired population

| group | pages | modules | mean no-source raw | mean no-source NET | mean LOOSE | ceiling | ceiling loose | pooled NET |
|---|---|---|---|---|---|---|---|---|
| False | 1880 | 400 | 11.1% | 8.4% | 5.8% | 91.6% | 94.2% | 9.2% |

## By KB subject family (14.x, prefix heuristic) — paired population

| group | pages | modules | mean no-source raw | mean no-source NET | mean LOOSE | ceiling | ceiling loose | pooled NET |
|---|---|---|---|---|---|---|---|---|
| no KB family | 1249 | 206 | 11.5% | 9.0% | 6.1% | 91.0% | 93.9% | 9.4% |
| BLL (14.7) | 257 | 91 | 8.0% | 3.5% | 2.6% | 96.5% | 97.4% | 3.2% |
| CED (14.4) | 113 | 28 | 14.1% | 10.6% | 8.3% | 89.4% | 91.7% | 14.0% |
| X-prefixed other (learningSupport) | 102 | 17 | 10.2% | 8.7% | 5.8% | 91.3% | 94.2% | 10.3% |
| LS (14.6) | 102 | 18 | 12.5% | 9.9% | 6.7% | 90.1% | 93.3% | 10.5% |
| Taonga/Arts (14.3) | 15 | 10 | 19.1% | 17.3% | 12.8% | 82.7% | 87.2% | 14.0% |
| H&PE FUNdamentals (14.5) | 15 | 15 | 11.7% | 10.9% | 6.4% | 89.1% | 93.6% | 12.2% |
| Technology (14.12) | 8 | 8 | 8.4% | 7.5% | 4.8% | 92.5% | 95.2% | 7.0% |
| HPE content (14.8) | 8 | 1 | 4.4% | 3.0% | 3.0% | 97.0% | 97.0% | 2.5% |
| BLLR (14.9) | 6 | 1 | 12.4% | 9.9% | 6.5% | 90.1% | 93.5% | 4.1% |
| Languages (14.1) | 5 | 5 | 5.1% | 5.1% | 3.3% | 94.9% | 96.7% | 5.8% |

## By Subject (Module_Structure_Index) — paired population

| group | pages | modules | mean no-source raw | mean no-source NET | mean LOOSE | ceiling | ceiling loose | pooled NET |
|---|---|---|---|---|---|---|---|---|
| 1-10 Mathematics | 332 | 42 | 12.6% | 10.5% | 6.6% | 89.5% | 93.4% | 12.1% |
| NCEA1 | 323 | 46 | 14.2% | 12.5% | 9.0% | 87.5% | 91.0% | 12.2% |
| 1-10 English | 288 | 48 | 9.6% | 6.1% | 4.0% | 93.9% | 96.0% | 6.5% |
| 1-10 Blended Literacy | 257 | 91 | 8.0% | 3.5% | 2.6% | 96.5% | 97.4% | 3.2% |
| Leaving to Learn | 204 | 35 | 11.3% | 9.3% | 6.3% | 90.7% | 93.7% | 10.4% |
| Online Safety (OS9000) | 128 | 28 | 5.6% | 3.0% | 2.6% | 97.0% | 97.4% | 2.7% |
| ConnectED | 113 | 28 | 14.1% | 10.6% | 8.3% | 89.4% | 91.7% | 14.0% |
| ANZH | 78 | 10 | 12.8% | 11.0% | 9.2% | 89.0% | 90.8% | 8.9% |
| None | 45 | 10 | 7.1% | 5.2% | 3.6% | 94.8% | 96.4% | 5.6% |
| 1-10 Social Science | 38 | 11 | 19.6% | 10.4% | 5.5% | 89.6% | 94.5% | 8.1% |
| 1-10 Health and PE | 15 | 15 | 11.7% | 10.9% | 6.4% | 89.1% | 93.6% | 12.2% |
| Te Marautanga o Aotearoa TMoA | 14 | 5 | 5.1% | 4.9% | 4.0% | 95.1% | 96.0% | 7.2% |
| EXPlore | 14 | 8 | 10.0% | 9.8% | 6.2% | 90.2% | 93.8% | 7.2% |
| 1-10 Science | 10 | 2 | 6.7% | 4.7% | 2.4% | 95.3% | 97.6% | 4.8% |
| 1-10 Technology | 8 | 8 | 8.4% | 7.5% | 4.8% | 92.5% | 95.2% | 7.0% |
| Te ara Whakapuawa -Wellbeing | 8 | 8 | 18.2% | 18.2% | 14.2% | 81.8% | 85.8% | 18.5% |
| 1-10 Arts | 5 | 5 | 8.3% | 4.7% | 2.1% | 95.3% | 97.9% | 5.6% |

## By Series prefix — paired population

| group | pages | modules | mean no-source raw | mean no-source NET | mean LOOSE | ceiling | ceiling loose | pooled NET |
|---|---|---|---|---|---|---|---|---|
| BLL | 257 | 91 | 8.0% | 3.5% | 2.6% | 96.5% | 97.4% | 3.2% |
| MXFL | 95 | 11 | 10.0% | 8.8% | 5.4% | 91.2% | 94.6% | 9.0% |
| ENGI | 82 | 12 | 10.5% | 6.5% | 5.0% | 93.5% | 95.0% | 6.6% |
| ANZH | 78 | 10 | 12.8% | 11.0% | 9.2% | 89.0% | 90.8% | 8.9% |
| XDLS | 75 | 12 | 14.1% | 11.2% | 7.4% | 88.8% | 92.6% | 11.9% |
| PES | 75 | 7 | 13.9% | 11.3% | 8.3% | 88.7% | 91.7% | 13.6% |
| AGH | 73 | 9 | 11.1% | 10.4% | 6.4% | 89.6% | 93.6% | 11.8% |
| HIS | 73 | 8 | 10.0% | 8.8% | 6.2% | 91.2% | 93.8% | 8.3% |
| MXFU | 56 | 6 | 11.4% | 10.3% | 7.0% | 89.7% | 93.0% | 11.6% |
| ENGC | 54 | 7 | 9.9% | 6.4% | 4.6% | 93.6% | 95.4% | 7.3% |
| ENGS | 52 | 8 | 9.4% | 5.3% | 3.3% | 94.7% | 96.7% | 5.5% |
| MXDI | 52 | 6 | 12.2% | 9.8% | 5.2% | 90.2% | 94.8% | 9.8% |
| ENGJ | 48 | 7 | 7.2% | 4.7% | 2.4% | 95.3% | 97.6% | 5.1% |
| PHE | 48 | 8 | 23.7% | 21.9% | 16.5% | 78.1% | 83.5% | 21.2% |
| ENGR | 44 | 6 | 10.2% | 7.2% | 4.0% | 92.8% | 96.0% | 6.7% |
| MXDB | 41 | 5 | 12.1% | 9.2% | 6.1% | 90.8% | 93.9% | 9.4% |
| MXEX | 41 | 6 | 20.5% | 16.6% | 11.2% | 83.4% | 88.8% | 23.2% |
| HES | 38 | 5 | 13.0% | 10.9% | 7.5% | 89.1% | 92.5% | 9.3% |
| MXEO | 38 | 5 | 12.4% | 10.2% | 6.8% | 89.8% | 93.2% | 10.6% |
| XGF | 38 | 5 | 10.9% | 9.6% | 6.7% | 90.4% | 93.3% | 13.1% |
| CEDO | 37 | 6 | 13.0% | 11.2% | 7.1% | 88.8% | 92.9% | 6.1% |
| CEDT | 35 | 11 | 16.2% | 11.3% | 9.7% | 88.7% | 90.3% | 19.8% |
| XMES | 31 | 5 | 9.9% | 8.3% | 4.8% | 91.7% | 95.2% | 8.3% |
| XLP | 27 | 6 | 8.0% | 6.3% | 4.9% | 93.7% | 95.1% | 6.4% |
| OSBY | 23 | 5 | 6.7% | 4.1% | 3.1% | 95.9% | 96.9% | 4.0% |
| OSOH | 23 | 5 | 4.3% | 2.9% | 2.6% | 97.1% | 97.4% | 2.4% |
| OSGM | 22 | 5 | 4.8% | 2.0% | 1.6% | 98.0% | 98.4% | 1.4% |
| OSAI | 20 | 5 | 5.1% | 2.3% | 1.5% | 97.7% | 98.5% | 2.4% |
| SSOG | 19 | 3 | 23.5% | 6.0% | 1.8% | 94.0% | 98.2% | 4.8% |
| XTAS | 18 | 3 | 7.6% | 6.4% | 4.0% | 93.6% | 96.0% | 6.4% |
| TEDC | 17 | 2 | 6.7% | 5.6% | 3.1% | 94.4% | 96.9% | 6.9% |
| HPFUN | 15 | 15 | 11.7% | 10.9% | 6.4% | 89.1% | 93.6% | 12.2% |
| OSAH | 15 | 3 | 6.4% | 3.0% | 3.0% | 97.0% | 97.0% | 2.7% |
| OSSC | 15 | 3 | 6.7% | 4.6% | 4.6% | 95.4% | 95.4% | 3.7% |
| CEDK | 14 | 3 | 6.4% | 3.3% | 2.7% | 96.7% | 97.3% | 3.5% |
| CEDR | 14 | 5 | 23.3% | 18.1% | 17.3% | 81.9% | 82.7% | 26.7% |
| CEDW | 13 | 3 | 10.3% | 6.7% | 3.8% | 93.3% | 96.2% | 10.6% |
| ART | 10 | 5 | 24.5% | 23.7% | 18.2% | 76.3% | 81.8% | 35.0% |
| OSSM | 10 | 2 | 5.8% | 2.2% | 2.2% | 97.8% | 97.8% | 1.9% |
| SSCI | 10 | 1 | 2.8% | 1.3% | 1.1% | 98.7% | 98.9% | 0.9% |
| MXFUN | 9 | 3 | 17.0% | 12.1% | 3.2% | 87.9% | 96.8% | 21.5% |
| SSFUN | 9 | 7 | 29.9% | 29.7% | 18.2% | 70.3% | 81.8% | 15.7% |
| SCCH | 9 | 1 | 6.8% | 4.6% | 2.1% | 95.4% | 97.9% | 4.6% |
| SCPH | 9 | 1 | 7.6% | 3.5% | 3.5% | 96.5% | 96.5% | 3.2% |
| PNR | 8 | 3 | 2.8% | 2.5% | 1.0% | 97.5% | 99.0% | 2.9% |
| ENFUN | 8 | 8 | 9.7% | 8.2% | 5.5% | 91.8% | 94.5% | 8.4% |
| TEFUN | 8 | 8 | 8.4% | 7.5% | 4.8% | 92.5% | 95.2% | 7.0% |
| HPRE | 8 | 1 | 4.4% | 3.0% | 3.0% | 97.0% | 97.0% | 2.5% |
| XWHA | 8 | 2 | 18.1% | 15.0% | 12.3% | 85.0% | 87.7% | 18.3% |
| XFUN | 7 | 2 | 5.0% | 4.7% | 2.6% | 95.3% | 97.4% | 8.3% |
| TRR | 6 | 2 | 8.2% | 8.2% | 8.0% | 91.8% | 92.0% | 9.3% |
| EXPFUN | 6 | 6 | 5.7% | 5.4% | 3.0% | 94.6% | 97.0% | 3.8% |
| TWHA | 6 | 6 | 23.8% | 23.8% | 18.8% | 76.2% | 81.2% | 22.7% |
| BLLR | 6 | 1 | 12.4% | 9.9% | 6.5% | 90.1% | 93.5% | 4.1% |
| ARFUN | 5 | 5 | 8.3% | 4.7% | 2.1% | 95.3% | 97.9% | 5.6% |
| CHFUN | 5 | 5 | 5.1% | 5.1% | 3.3% | 94.9% | 96.7% | 5.8% |
| ENG | 5 | 3 | 11.6% | 10.9% | 7.9% | 89.1% | 92.1% | 9.2% |
| EXBP | 4 | 1 | 21.1% | 21.1% | 13.2% | 78.9% | 86.8% | 23.7% |
| EXIP | 4 | 1 | 5.2% | 5.2% | 4.2% | 94.8% | 95.8% | 4.6% |
| TWHK | 2 | 2 | 1.5% | 1.5% | 0.3% | 98.5% | 99.7% | 2.1% |
| SCFUN | 1 | 1 | 5.7% | 5.7% | 5.7% | 94.3% | 94.3% | 5.7% |
| ENGFUN | 1 | 1 | 50.0% | 50.0% | 50.0% | 50.0% | 50.0% | 50.0% |

## Boilerplate — no-source text recurring in ≥ 5 modules (170 strings; top 60)

These are conventions a rule can emit (most are documented in the KB); they are removed from the NET figures.

| modules | text |
|---|---|
| 413 | acknowledgements |
| 366 | every effort has been made to acknowledge and contact copyright holders te aho o te kura pounamu apologises for any omis |
| 366 | copyright board of trustees of te aho o te kura pounamu private bag 39992 wellington mail centre lower hutt 5045 new zea |
| 321 | all other images te aho o te kura pounamu wellington new zealand |
| 112 | select one |
| 109 | 02 |
| 109 | 01 |
| 88 | image avatar heygen wwwheygencom used with permission |
| 70 | how will i know if ive learned it |
| 67 | 03 |
| 60 | 04 |
| 58 | 20 |
| 57 | 40 |
| 49 | 10 |
| 47 | 50 |
| 44 | 30 |
| 43 | 05 |
| 42 | 60 |
| 40 | all illustrations te aho o te kura pounamu wellington new zealand |
| 39 | 70 |
| 35 | standards |
| 34 | unable to display pdf file download here |
| 30 | i can |
| 28 | want to know where to start |
| 28 | 80 |
| 27 | 06 |
| 26 | intro |
| 24 | t |
| 24 | f |
| 24 | 07 |
| 23 | we are learning |
| 23 | information |
| 22 | go to your journal |
| 22 | click here to view a basic year plan talk to your kaiako about creating a specific learning plan to meet your needs |
| 21 | learning intentions |
| 21 | 90 |
| 20 | success criteria |
| 19 | all other images and audio te aho o te kura pounamu wellington new zealand |
| 17 | you will show your understanding by |
| 16 | video avatar heygen wwwheygencom used with permission |
| 16 | all other illustrations te aho o te kura pounamu wellington new zealand |
| 15 | important note |
| 12 | 08 |
| 11 | they write with ease and automaticity and correctly spell a wide range of words including those with advanced spelling p |
| 11 | share your learning |
| 11 | designer note audio to come |
| 10 | word 3 |
| 10 | word 2 |
| 10 | step 2 |
| 10 | step 1 |
| 10 | share with us |
| 10 | n |
| 9 | word 9 |
| 9 | word 8 |
| 9 | word 7 |
| 9 | word 6 |
| 9 | word 5 |
| 9 | word 4 |
| 9 | word 1 |
| 9 | step 3 |

## Outlier pages — paired pages whose NET no-source share ≥ 50% with ≥ 8 blocks (42 pages; top 60)

These pages will score low against gold no matter what the converter does; the samples show the developer-authored text.

| page | family | sub-type | KB family | blocks | no-source (net) | share | skeleton score | samples of unsourced text |
|---|---|---|---|---|---|---|---|---|
| XGF9004-06.0.html | Standard | Combo | X-prefixed other (learningSupport) | 59 | 52 | 88.1% | 34.4% | <h1> Brain Boosters – Resources and Games ¦ <p> Games help your brain stretch, flex, and grow stronger, just like muscles do when you exercise. ¦ <p> No matter your age – five, fifteen, or older – this section has something for everyone. Start with board and c |
| CEDR302 Light and No Light.html | Inquiry | Inquiry | CED (14.4) | 154 | 123 | 79.9% | 7.4% | <h1> Tūrama me te Kore Tūrama ¦ <p> This inquiry explores Science and Te ao Tangata (Social Science) ¦ <p> Making connections across related contexts (Social Sciences and English) and learning areas by drawing on prio |
| CEDT203 My Pepeha.html | Inquiry | Inquiry | CED (14.4) | 121 | 94 | 77.7% | 15.7% | <h1> My Pepeha ¦ <p> This inquiry explores Te ao tangata (Social Sciences) Languages including Aotearoa New Zealand’s Histories and ¦ <p> Making connections across related contexts (Social Sciences and Languages) and learning areas by drawing on pr |
| PHE1004_3.0.html | Standard | Standard | no KB family | 17 | 13 | 76.5% | 52.0% | <h1> Time for Action ¦ <h3> So they say practice makes perfect! ¦ <p> Include and provide supporting evidence/examples by using photos and or video footage. These reflections and r |
| CEDR301 People Making a Difference.html | Inquiry | Inquiry | CED (14.4) | 122 | 93 | 76.2% | 7.8% | <h1> Te Iwi Whakahuri i te Ao ¦ <p> This inquiry explores Te ao tangata (Social Sciences) and English. ¦ <p> Making connections across related contexts (Social Sciences and English) and learning areas by drawing on prio |
| CEDT201 Let’s Make Some Noise.html | Inquiry | Inquiry | CED (14.4) | 121 | 92 | 76.0% | 11.0% | <h1> Te Āhuahanga me te Toi ¦ <p> This inquiry explores The Arts (Music) and Technology. ¦ <p> Making connections across related contexts (Music and Technology) and learning areas by drawing on prior knowl |
| MXFL204_3.1.html | Standard | Standard | no KB family | 26 | 19 | 73.1% | 48.1% | <h1> 3.1 ¦ <h1> Interpreting Comparisons, Trends and Patterns in Graphs ¦ <p> Designer note: Overview Required |
| MXEX301_05.0.html | Standard | Standard | no KB family | 43 | 31 | 72.1% | 22.6% | <p> A line is straight and has no beginning or end point. It is infinite. When you draw a line, you put arrows at  ¦ <p> This line can be named using two points on it. It can be called line AB or ¦ <p> A ray is a part of a line. It starts at a point and extends in one direction forever. |
| CEDR201 Mixing Colours.html | Inquiry | Inquiry | CED (14.4) | 109 | 78 | 71.6% | 7.7% | <h1> Te Whakahanumi tae ¦ <p> This inquiry explores Visual Arts and Science. ¦ <p> Making connections across related contexts (Visual Arts and Science) and learning areas by drawing on prior kn |
| CEDT202 Chemical Reactions.html | Inquiry | Inquiry | CED (14.4) | 104 | 74 | 71.2% | 18.6% | <h1> Ngā Tauhohe Matū ¦ <p> This inquiry explores Science and English. ¦ <p> Making connections across related contexts (Science and English) and learning areas by drawing on prior knowle |
| CEDT204 Geometry and Art.html | Inquiry | Inquiry | CED (14.4) | 90 | 64 | 71.1% | 17.1% | <h1> Geometry and Art ¦ <h1> Te Āhuahanga me te Toi ¦ <p> This inquiry explores The Arts (Visual Arts) and Mathematics & Statistics. |
| XGF9004-03.0.html | Standard | Combo | X-prefixed other (learningSupport) | 134 | 92 | 68.7% | 23.8% | <h1> Self-monitoring ¦ <h2> Self-monitoring ¦ <p> Self-monitoring is about noticing your thoughts, actions, and feelings and making changes when needed. You hav |
| ART1006_4.0.html | Standard | Standard | Taonga/Arts (14.3) | 98 | 65 | 66.3% | 19.0% | <p> Required: 1–2 A4 pages of notes and drawings ¦ Time: 1 hour. ¦ <p> Here are two examples of how other ākonga have assessed their projects. ¦ <h4> Passion Project Self-Assessment Rubric |
| MXEX301_03.1.html | Standard | Standard | no KB family | 38 | 25 | 65.8% | 23.1% | <p> This is a very small amount. A teaspoon holds about five millilitres. ¦ <p> 1000 millilitres is called a litre. ¦ <p> This is the basic unit for capacity. A carton of milk holds a litre. |
| XDLS501.04.html | Standard | Standard | LS (14.6) | 63 | 40 | 63.5% | 18.2% | <h1> Conflict Resolution ¦ <li> how to strive towards peace ¦ <li> how to negotiate things you want and need. |
| PHE1001_3.0.html | Standard | Standard | no KB family | 24 | 15 | 62.5% | 67.3% | <p> What are external cues? External cues are unpredictable influences or factors that we might face in a game or  ¦ <p> Some external cues could be: ¦ <li> environmental factors |
| HES1005_7.0.html | Standard | Standard | no KB family | 45 | 28 | 62.2% | 30.4% | <h1> Oranga Taihema ¦ <p> This lesson is not compulsory. If you have any concerns or queries about the topics of sexuality or gender ide ¦ <h3> What should Jo choose? |
| MXFL204_6.0.html | Standard | Standard | no KB family | 26 | 16 | 61.5% | 35.7% | <p> The line graph below shows how a puppy’s weight has changed as it grows each week. ¦ <h5> In this line graph: ¦ <li> The horizontal axis (x-axis), the one along the bottom represents the time. In this graph, the puppy’s age in  |
| ANZH104_02.0.html | Standard | Standard | no KB family | 13 | 8 | 61.5% | 46.2% | <p> The wharepuni was the family sleeping house. It was made with a wooden frame and covered with raupō or nıkau l ¦ <p> The chief’s family had a bigger whare with beautiful carvings on the outside. If there was no wharenui in the  ¦ <p> Cooking and eating was always done outside. Māori had no stoves or metal pots. They had kete and kumete to gat |
| MXDI101_5.0.html | Standard | Standard | no KB family | 13 | 8 | 61.5% | 56.5% | <p> Here are six groups of two lollipops. ¦ <p> Here are three rows of five flowers: ¦ <p> Here are six rows of 10 trees: |
| ANZH104_03.0.html | Standard | Standard | no KB family | 10 | 6 | 60.0% | 57.9% | <p> In the early days, most of the clothing was made from harakeke or flax. Both women and men wore flax skirts. W ¦ <p> Chiefs wore cloaks made with dog skin and dog hair. bird feathers were used to decorate the cloaks. ¦ <p> Māori often wore earrings and necklaces made of shells, bone and pounamu. Men wore their hair in a topknot and |
| HIS1001-0.0.html | Standard | Standard | no KB family | 10 | 6 | 60.0% | 49.2% | <h1> HIS1001 ¦ <h1> Karihi Te moana-nui-a-kiwa ¦ <p> He moana tātou, he moana waiwai. Ko te ao moana, ko tātou tērā. |
| MXEX301_03.0.html | Standard | Standard | no KB family | 74 | 44 | 59.5% | 21.7% | <h4> Depth ¦ <h4> Perimeter ¦ <h4> Thickness |
| MXDB301_6.0.html | Standard | Standard | no KB family | 39 | 23 | 59.0% | 28.0% | <li> calculate the surface area for 3D shapes. ¦ <li> calculating the surface area of 3D shapes by calculating area of a 2D net. ¦ <p> Packaging relies on three-dimensional shapes, some of which you will already know. However, there may be a few |
| XDLS501.02.html | Standard | Standard | LS (14.6) | 95 | 56 | 58.9% | 32.4% | <li> how to look friendly ¦ <li> how to look strong and confident; to make your whakamana visible. ¦ <li> mirror the people around me to help me understand how they are feeling |
| PES1003_4.0.html | Standard | Standard | no KB family | 36 | 21 | 58.3% | 43.5% | <p> Go to your journal and complete Activity 4A. ¦ <th> Thermal conductivity (watts per metre per degree Celsius (W/m/°C)) ¦ <td> Copper |
| XDLS902.00.html | Standard | Combo | LS (14.6) | 24 | 14 | 58.3% | 68.0% | <h1> XDLS9002 ¦ <p> He hauora te taonga ¦ <p> Health is a treasure |
| XGF9004-04.0.html | Standard | Combo | X-prefixed other (learningSupport) | 63 | 36 | 57.1% | 44.8% | <h1> Flexible thinking ¦ <h4> Key question ¦ <h2> Problem solving |
| PES1003_1.0.html | Standard | Standard | no KB family | 42 | 24 | 57.1% | 35.9% | <h3> Hands-on activity: see it melt ¦ <p> Download the learning journal and complete the practical activity 1A. ¦ <h3> Solid to liquid – melting |
| MXEX401_04.0.html | Standard | Standard | no KB family | 35 | 20 | 57.1% | 26.2% | <p> The longest side of a right angled triangle is called a hypotenuse. It is always opposite the right angle (not ¦ <h3> Identifying the hypotenuse ¦ <p> Click on the hypotenuse of each of the right-angled triangles shown below. |
| MXFL203_5.0.html | Standard | Standard | no KB family | 73 | 41 | 56.2% | 52.7% | <li> Show ²⁄₂ ¦ <p> 1½ ¦ <p> 2½ |
| XGF9004-02.0.html | Standard | Combo | X-prefixed other (learningSupport) | 93 | 51 | 54.8% | 26.2% | <p> Being organised helps your brain stay calm, focused, and ready to learn. It’s more than just having a tidy spa ¦ <p> When you are well-organised, you can complete tasks more efficiently, reduce stress, and have more time for ac ¦ <h3> Skills for organisation |
| HIS1001-10.0.html | Standard | Standard | no KB family | 62 | 33 | 53.2% | 20.0% | <li> synthesise evidence from sources to write a paragraph ¦ <li> examine the collective remembrance of historic events (maumaharatanga). ¦ <li> identifying the parts of a paragraph |
| PHE1006_5.0.html | Standard | Standard | no KB family | 25 | 13 | 52.0% | 37.0% | <h1> Movement Experiences and Context ¦ <p> If we take the example of basketball, some movement experience examples would be basketball drills (like learn ¦ <p> Click below to see how a context wouldn’t work, and also how it would work. |
| HIS1001-9.0.html | Standard | Standard | no KB family | 52 | 27 | 51.9% | 28.1% | <li> identify perspectives in the historic records. ¦ <li> identifying evidence of perspectives in primary sources ¦ <li> explaining why a person or group holds the perspective they do. |
| MXFU202_7.0.html | Standard | Standard | no KB family | 120 | 62 | 51.7% | 27.2% | <h1> Times Table Relationships ¦ <li> spot patterns in multiplication and use patterns to solve problems faster. ¦ <h3> 3 × 3 basketball |
| XGF9004-05.0.html | Standard | Combo | X-prefixed other (learningSupport) | 72 | 37 | 51.4% | 27.3% | <h1> Working memory ¦ <p> What helps you make good decisions when you have choices to make? ¦ <p> Working memory is like a mental sticky note – it holds onto information just long enough for you to use it. Yo |
| XDLS501.03.html | Standard | Standard | LS (14.6) | 86 | 43 | 50.0% | 29.8% | <p> Mindfulness is about taking a moment to pause and pay attention to what we’re doing, feeling, and thinking. It ¦ <p> Some people use a prop to help ground them. For example, you might love Star Wars and keep a Yoda toy in your  ¦ <h3> The way you live: personal conduct |
| AGH1003_07.0.html | Standard | Standard | no KB family | 60 | 30 | 50.0% | 44.2% | <h3> Why is good drainage important? ¦ <p> Good drainage is crucial for agriculture and horticulture success for many reasons. ¦ <h3> Poor drainage |
| ANZH104_01.0.html | Standard | Standard | no KB family | 12 | 6 | 50.0% | 56.8% | <h3> Important kupu ¦ <p> Before you begin the lesson, have a go at matching the English word to the Māori word. You can try this activi ¦ <h4> Early Māori life before Europeans arrived |
| PHE1003_5.1.html | Standard | Standard | no KB family | 8 | 4 | 50.0% | 60.6% | <h1> 5.1 ¦ <h1> Kotahitanga Strategies 9-12 ¦ <p> For each strategy complete the best choice for each question then check your answers before moving on to the n |
| PHE1004_1.0.html | Standard | Standard | no KB family | 8 | 4 | 50.0% | 80.0% | <p> For example, tuakana-teina could look like grouping more experienced person/athlete (tuakana) with less experi ¦ <p> Another example could be providing opportunities for people/athletes to exercise rangatiratanga by participati ¦ <h3> Definitions of strategies promoting kotahitanga |

## Worst modules by mean NET no-source share (paired pages; top 40)

| module | pages | mean NET no-source share |
|---|---|---|
| CEDR302 | 1 | 79.9% |
| CEDT203 | 1 | 77.7% |
| CEDR301 | 1 | 76.2% |
| CEDT201 | 1 | 76.0% |
| CEDR201 | 1 | 71.6% |
| CEDT202 | 1 | 71.2% |
| CEDT204 | 1 | 71.1% |
| SSFUN07 | 3 | 61.1% |
| CEDO301 | 4 | 51.9% |
| ENGFUN02 | 1 | 50.0% |
| XGF9004 | 7 | 46.0% |
| XDLS501 | 4 | 45.9% |
| HIS1001 | 8 | 45.1% |
| PHE1004 | 4 | 41.5% |
| XWHA01 | 2 | 39.8% |
| ART1006 | 4 | 39.4% |
| ART1003 | 1 | 38.9% |
| TWHA904 | 1 | 37.4% |
| ANZH104 | 8 | 36.9% |
| HPFUN101 | 1 | 35.3% |
| SSFUN05 | 1 | 33.7% |
| ENG1005 | 1 | 33.3% |
| PHE1001 | 5 | 31.9% |
| TWHA901 | 1 | 31.6% |
| TWHA903 | 1 | 28.6% |
| MXEX301 | 8 | 27.8% |
| MXDB301 | 7 | 26.8% |
| TWHA905 | 1 | 26.6% |
| MXFL204 | 12 | 26.2% |
| PHE1003 | 7 | 26.1% |
| XFUN01 | 1 | 25.3% |
| PES1007 | 10 | 24.6% |
| HES1005 | 8 | 24.0% |
| MXFU202 | 10 | 24.0% |
| XDLS909 | 5 | 23.0% |
| HPFUN401 | 1 | 22.9% |
| MXFL401 | 8 | 22.0% |
| MXEX401 | 7 | 21.9% |
| EXBP901 | 4 | 21.1% |
| XDLS902 | 8 | 21.1% |
