# New module intake — 22 September 2026 (the 38 pre-intake never-converted modules)

Run by the autonomous loop (session 33 Round 3 = LOOP §1f Round 0d) — the first intake the loop
has done unattended. Nothing new arrived in the human-developer folders: these 38 gold modules
had been in `01-Finalized_Modules_` since before August 2026 with a Writers Template, a Media
List and their `_parsed.txt`, but had never been converted (never in `compare_set.txt`; a full
regeneration enumerates Claude dirs). No engine, data or registry change; nothing shipped as a
converter round; `AppVersion` stays 260619.98.

## 1. What was created

`01-Claude_Modules_/{Template}/{CODE}/` for every one of the 38, built by `batch_convert.cjs`
from the existing docx in four batches of ≤ 10 (`CONVERTER_V2/outputs/_intake_2026-09-22_convert.sh`,
all rc 0): **38 / 38 converted, 0 refused, 0 ghost dirs.** 161 pages + 38 `_interactives.txt`.

| template | modules | codes |
|---|--:|---|
| Standard | 21 | BLL243 BLL247 BLL255 BLL256 BLL257 BLL261 BLL264 BLL265 BLL266 BLL271 BLL272 BLL273 BLL274 BLL275 BLL276 HPRE301 OSSM501 SSCI104 SSEA203 SSOG105 XMES202 |
| Inquiry | 16 | BLL250 BLL260 BLL270 CEDK401 CEDO201 CEDO402 CEDR101 CEDR203 CEDR401 CEDT102 CEDW303 TWHK902 TWHK907 TWHR905 TWHR907 TWHT903 |
| Bilingual | 1 | TRR110 |


## 2. Results (`_intake_2026-09-22_results.txt`)

| module | Claude pages | gold pages | skeleton mean | note |
|---|--:|--:|--:|---|
| BLL243 / 247 / 255 / 256 / 257 / 261 / 264 / 265 / 266 / 271 / 272 / 273 / 274 / 275 / 276 | 3 each (BLL265 4) | 3 | 39–74 % | the multi-page BLL 2xx Standard family, family-typical |
| HPRE301 | 13 | 13 | 65.8 % | |
| OSSM501 / SSCI104 / SSEA203 / SSOG105 / XMES202 | 6 / 7 / 7 / 8 / 7 | same | 50–63 % | |
| TRR110 | 6 | 6 | 43.3 % | Bilingual |
| **BLL250 / BLL260 / BLL270** | **8 / 13 / 5** | **1** | 3–5 % | single-page gold OVER-SPLIT — registry page_model item |
| **CEDK401 / CEDO402 / TWHT903 / CEDR101 / CEDR401** | **12 / 6 / 5 / 2 / 2** | **1** | 5–10 % | same family |
| CEDO201 / CEDT102 / TWHK902 / TWHK907 / TWHR905 / TWHR907 | 1 | 1 | 11–40 % | one page, family-typical (gated siblings 7–55 %) |
| CEDR203 | 1 | 11 | 13.4 % | the reverse case — read its WT |
| CEDW303 | 1 | 1 | — | `compare_exclusions.txt` (CED revision brief): converted, not scored |

## 3. Gate numbers (the full suite on the 545-module corpus; `_intake_2026-09-22_gates.log`, split by `_intake_split.py`)

- Pre-existing 2377 pairs: **EXACT = r422e on every gate, 0 movers** (skeleton 54.2466 / 1464 /
  238 / 20; cs 14318 / 186 / 689 / 23; body 251; clean 2532 / 2576; leak 73 / 44).
- New batch (114 pairs): skeleton 51.42 % / 67 / 16 / 3; cs 813 / 8 / 84 / 0; body ANY 14
  (2 over-capture, 13 EMPTY); clean 158 / 160; leak 2 occ / 2 pages (BLL260_0_0 `[tab n]` × 7,
  BLL260_6_1 `[video 1]`).
- Whole population (the new committed baseline, `gate_baseline.json` `_note_intake_2026_09_22`):
  **skeleton 54.1172 % @ 2491 / 1531 / 254 / 23, RAW 38.049**; cs 15131 / 194 / 773 / 23; body
  57 / 5 / 206 / 265; clean 2690 / 2736 = 98.32 %; leak 75 / 46; tags 9557 / 9557; every
  verifier ✓; 17 selftests GREEN; feature index GREEN.
- Ceiling 91.2 % → 59.4 % of achievable. Miner 190 CANDIDATE. Dashboard coverage 50.7 %.

## 4. Findings

1. **The single-page Inquiry page model is the whole story** for the low scorers: the gold builds
   one page with a crumb nav and inquiry panels; Claude splits eight of them into lesson pages
   because their codes are in no Style-Anchor level's members / `page_model_exceptions`
   (BLL2's list has BLL210 / 220 / 230, the gated x0 modules, and not BLL250 / 260 / 270). A
   registry round, next.
2. The lesson chip on the BLL 2xx / SS Standard modules (`decimal-number` vs the gold's
   `lesson-number`, 14 modules) — a family-convention check.
3. `#4177` an EXTRA `col-md-6 > img` on 19 Standard modules — triangulate before judging.
4. Nothing needs Chris; no new no-build.
