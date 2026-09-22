#!/usr/bin/env python3
"""ROUND 0d (session 33 Round 3, 22 Sept 2026) — Phase 6 records for the 38-module intake: the changelog entry (no engine change,
no AppVersion bump), OPERATING_GUIDE §9 / §14, gate_baseline.json re-based to 2491 pairs, the loop file's §0 census table + §2
no-build bullet, verify_after_transfer.sh's expect values, LOOP_STATE.md (Position, Round log, next-session line). Run under WSL."""
import re, json, shutil
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
PF = R + "pageforge-site/converter-v2/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

entry = """## 2026-09-22 (FULL CORPUS REGENERATION + INTAKE RE-BASELINE, build 260619.98 — no engine change) — Round 0d for the 38 PRE-INTAKE modules that held a Writers Template but had never been converted: all 38 convert (0 refusals), 161 pages / 114 pairs join the corpus (2583 → 2744 pages, 507 → 545 dirs, 2377 → 2491 pairs); the autonomous loop's session 33 Round 3 (LOOP §1f, Phases 2 + 3 + 5–7)

### 1. WHAT HAPPENED

**The 38 (the 22 Sept `/loop-review`'s adversarial finding — the gold-only gap was 57, not 19).** BLL243 BLL247 BLL250 BLL255 BLL256 BLL257 BLL260 BLL261 BLL264 BLL265 BLL266 BLL270 BLL271 BLL272 BLL273 BLL274 BLL275 BLL276 CEDK401 CEDO201 CEDO402 CEDR101 CEDR203 CEDR401 CEDT102 CEDW303 HPRE301 OSSM501 SSCI104 SSEA203 SSOG105 TRR110 TWHK902 TWHK907 TWHR905 TWHR907 TWHT903 XMES202 — every one holds a Writers Template + Media List docx and its `_parsed.txt` (`outputs/_intake_2026-09-22_delta.txt`), every one is a `Module_Structure_Index.module_meta` key, none had a Claude dir (the "r285 ghost-directory class": never in `compare_set.txt`, and a full regeneration enumerates Claude dirs, so nothing ever reached them). Phase 1 skipped (placed, parsed, indexed); Phase 2: the 38 nested dirs pre-created (28 Standard-or-Inquiry-or-Bilingual per their gold folder), converted by explicit code list in four batches (`_intake_2026-09-22_convert.sh`, rc 0 × 4) — **38 / 38 converted, 0 refused, 0 ghost dirs** (`_intake_2026-09-22_results.txt`): 161 Claude pages against 125 gold pages. The page-count mismatches are the finding: **eight single-page Inquiry golds that Claude splits into lesson pages** (BLL250 8 / BLL260 13 / BLL270 5 / CEDK401 12 / CEDO402 6 / TWHT903 5 / CEDR101 2 / CEDR401 2 pages against the gold's ONE) and one the other way (CEDR203: 1 Claude page vs 11 gold) — the `page_model` registry rows for these codes were never mined because they were never members of a Style-Anchor level (BLL2's `page_model_exceptions` lists BLL210 / 220 / 230 but not the never-converted BLL250 / 260 / 270). Phase 4 (the registries) is therefore NOT skipped: it is the next round, as its own ledgered registry round.

**Phase 3 — the FULL regeneration on the unchanged registries** (`_intake_2026-09-22_fullship_par.sh`: 42 batches, 4 workers, 6 min, all rc 0; `_stalecheck.sh` 0 stale; `_content_manifest.py changed` = EXACTLY the 38; `fresh --affected` the 504 pre-existing page-bearing modules byte-identical). `_ship_ledger.py record-full --round intake-2026-09-22 --build 260619.98` (counter 0); the fast-loop baseline re-snapshot (2491 pairs); the content manifest snapshot (2744 pages / 542 page-bearing modules — TRR104 / 105 / 115 still hold only a `_run.json`).

### 2. THE GATES, SPLIT BY POPULATION (LOOP §1e; `_intake_split.py` — new, generalised from `_s28_t1_split.cjs`, kept for the next intake; `_intake_2026-09-22_split.log`)

| gate | PRE-EXISTING (2377 pairs / 504 modules) — must equal r422e | NEW batch (114 pairs / 38 modules) | WHOLE population (the new committed baseline) |
|---|---|---|---|
| skeleton SCAFFOLD mean / ≥50 / ≥75 / ≥90 | **54.2466 % / 1464 / 238 / 20 — EXACT, 0 movers** (`_s29_skdelta.py`) | 51.42 % / 67 / 16 / 3 | **54.1172 % @ 2491 / 1531 / 254 / 23**, RAW 38.049 |
| compare_structure matched / exact / EXTRA / missing / row-wrap | 16620 / 14318 / 186 / 689 / 23 EXACT | 1004 / 813 / 8 / 84 / 0 | 17624 / **15131 / 194 / 773 / 23** |
| body_compare pages / over-capture / runaway / EMPTY / ANY | 2576 / 55 / 5 / 193 / 251 EXACT | 160 / 2 / 0 / 13 / 14 | 2736 / **57 / 5 / 206 / 265** |
| structurally clean / leak | 2532 / 2576 = 98.29 %, 73 occ / 44 pages EXACT | 158 / 160, 2 occ / 2 pages (BLL260_0_0 `[tab n]` ×7 … BLL260_6_1 `[video 1]`) | **2690 / 2736 = 98.32 %, 75 / 46** |
| tags / verifiers / selftests | 9557 / 9557; every verifier ✓; 17 selftests GREEN (49 / 0) | — | same |

Every "REGRESSED" row `_gatecheck.py` printed (mean −0.13, EXTRA +8, missing +84, ANY +14, leak +2) is the new batch's own contribution — population arithmetic, not a mover: the whole-population mean = (54.2466 × 2377 + 51.42 × 114) / 2491. The new batch per module (`_intake_2026-09-22_split.log`): the multi-page Standard modules score 39–74 % (BLL255 73.6, BLL273 69.5, HPRE301 65.8 / 13 pairs, SSEA203 63.1, XMES202 62.3, OSSM501 61.8 …); the eight over-split single-page Inquiry modules 3–10 % (one pair each, the rest of their pages unpaired) — the registry item above; the CED / TWH single-page modules 8–40 % (their gated siblings score 7–55 %, so family-typical). The verifiers' fixed module sets need no extension: the 38 carry hand-off boxes, no built widget type with a verifier.

### 3. THE INSTRUMENTS (LOOP §1f Phase 5)

The ceiling re-measured on 2491 pairs (`_ceiling_intake_2026-09-22.{json,md,log}`): **scaffold 91.2 %** (loose 93.6 %; was 90.9 %) → **54.117 % = 59.4 % of achievable**. `COVERAGE_DASHBOARD.md` rebuilt (`_intake_2026-09-22_dashboard_run.sh` + `--refresh --allow-stale`: coverage 50.7 % = 2902 of 5723 tagged widgets; the `--allow-stale` because the feature index was rebuilt AFTER the census in the same script — a same-corpus mtime nit, recorded; rebuild the index BEFORE the census next time). The DIFF MINER full (`DIFF_QUEUE.md`: 2491 pairs / 533 modules, 9367 classes, **190 CANDIDATE** — was 184; the six new candidate rows are all this batch's: #63 / #73 / #85 the BLL single-page module-menu items, #438 crumbs MISSING, #496 the inquiry footer prev-lesson, #4098 `div.inquiryPanel` MISSING — the single-page Inquiry page-model family; plus #4177 an EXTRA `col-md-6 > img` on 19 Standard modules to read) and scoped over the 38 (`_diff_miner_scoped.{md,json}`: 115 pairs, 1380 classes, 11 CANDIDATE; chrome facts F1 / F2 the lesson chip `decimal-number` vs `lesson-number` on 14 BLL / SS modules, F15 crumbs MISSING and F16 the inquiry footer on the 14 single-page Inquiry modules). The feature index rebuilt GREEN (552 modules).

### 4. RECORDS

`gate_baseline.json` re-based to 2491 pairs with `_meta._note_intake_2026_09_22` (the split above); OPERATING_GUIDE §9 / §14; the loop file's §0 census table (545 dirs / 2,744 pages / 2,491 pairs) and §2 no-build bullet (the 38 are IN; the no-build list is now the 7 with no Writers Template); `verify_after_transfer.sh` expect values (`.pre-intake-2026-09-22.bak`); the checksum manifests; the handover `LOOP_INTAKE__2026-09-22_38_Modules.md` + `NEW_MODULES__Intake_2026-09-22.md` (§7 re-ranked order: the single-page Inquiry page-model registry rows first). No engine, data or registry file changed; `AppVersion` stays 260619.98.

"""
p = PF + "BUILD_CHANGELOG.md"; s = rd(p)
head, rest = s.split("\n", 1)
assert head.startswith("# BUILD CHANGELOG") and rest.lstrip("\n").startswith("## 2026-09-22 (round 422 ENABLED")
wr(p, head + "\n\n" + entry + rest.lstrip("\n"))

p = PF + "OPERATING_GUIDE.md"; s = rd(p)
old9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 422-ENABLED BASELINE ("; assert s.count(old9) == 1
new9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **INTAKE 2026-09-22 BASELINE (the 38 pre-intake never-converted modules join the corpus — "
        "no engine change; FULL regeneration on the unchanged registries, counter 0): SCAFFOLD mean 54.1172% / >=50% 1531 / >=75% 254 / >=90% 23 / RAW 38.049% "
        "@ 2491 pairs, pairs skipped 0 — the 2377 pre-existing pairs hold r422e EXACTLY (54.2466 %, 0 movers); the new 114 pairs enter at 51.42 % (the eight "
        "over-split single-page Inquiry modules at 3–10 % are the next registry round); every other gate EXACT on the pre-existing population and RE-BASED "
        "(cs 15131 / 194 / 773 / 23, body 57 / 5 / 206 / 265, clean 2690 / 2736 = 98.32 %, leak 75 / 46). Ceiling re-measured 91.2 % → 59.4 % of achievable.** "
        "Previous — ROUND 422-ENABLED BASELINE (")
s = s.replace(old9, new9)
old14 = "- **Build:** `260619.98` (round 422 ENABLED — **THE SIDE-TAB"; assert s.count(old14) == 1
b14 = ("- **Build:** `260619.98` (**FULL CORPUS REGENERATION + INTAKE RE-BASELINE, 22 Sept 2026 — no engine change**: the 38 pre-intake modules that held a "
       "Writers Template but were never converted (the 22 Sept review's finding) all convert — 161 pages / 114 pairs, **2583 → 2744 pages / 507 → 545 dirs / "
       "2377 → 2491 pairs**; the autonomous loop's session 33 Round 3 = LOOP §1f Round 0d; **INTAKE 2026-09-22 BASELINE: SCAFFOLD mean 54.1172% / >=50% 1531 / "
       ">=75% 254 / >=90% 23 / RAW 38.049% @ 2491 pairs** — the pre-existing 2377 pairs EXACT (0 movers), the new batch 51.42 %; cs 15131 / 194 / 773 / 23, "
       "body 57 / 5 / 206 / 265, clean 2690 / 2736, leak 75 / 46; every verifier EXACT; 17 selftests GREEN; the miner 184 → 190 CANDIDATE (the six new rows = the "
       "single-page Inquiry page-model family); the ceiling 91.2 % (54.117 = 59.4 % of achievable); the dashboard rebuilt; the ledger FULL at intake-2026-09-22, "
       "counter 0). Previous: ")
s = s.replace(old14, b14 + old14)
wr(p, s)

p = R + "CONVERTER_V2/reference/tests/gate_baseline.json"; s = rd(p)
def setv(key, old, new):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=1); assert n == 1, key
setv("round", 422, '"intake-2026-09-22"')
setv("claude_pages", 2634, 2795); setv("paired_pages", 2377, 2491); setv("gated_dirs", 497, 534)
setv("mean_scaffold_pct", 54.25, 54.12); setv("median_scaffold_pct", 55.3, 55.0); setv("pages_ge_50", 1464, 1531); setv("pages_ge_75", 238, 254); setv("pages_ge_90", 20, 23); setv("raw_mean_pct", 38.25, 38.05)
setv("pairs", 2377, 2491)
setv("exact_chain", 14318, 15131); setv("claude_extra_container", 186, 194); setv("claude_missing_container", 689, 773)
setv("any_breakdown", 251, 265); setv("over_capture", 55, 57); setv("empty_container", 193, 206)
setv("clean_pages", 2532, 2690); setv("total_pages", 2576, 2736); setv("clean_pct", 98.29, 98.32)
a = '    "_note_r422e": "Round 422 ENABLED (session 33 Round 2'; assert s.count(a) == 1
s = s.replace(a, '    "_note_intake_2026_09_22": "INTAKE 2026-09-22 (session 33 Round 3 = LOOP 1f Round 0d, no engine change): the 38 pre-intake never-converted modules (BLL243-276 block, CEDK401, CEDO201, CEDO402, CEDR101, CEDR203, CEDR401, CEDT102, CEDW303, HPRE301, OSSM501, SSCI104, SSEA203, SSOG105, TRR110, TWHK902, TWHK907, TWHR905, TWHR907, TWHT903, XMES202) all convert — 161 pages / 114 pairs; FULL regeneration on the unchanged registries, 0 stale, the 504 pre-existing modules byte-identical. SPLIT BY POPULATION (_intake_split.py): the 2377 pre-existing pairs reproduce r422e EXACTLY (skeleton 54.2466 / 1464 / 238 / 20, 0 movers; cs 16620 / 14318 / 186 / 689 / 23; body 251; clean 2532 / 2576; leak 73 / 44); the NEW 114 pairs: skeleton 51.42 / 67 / 16 / 3, cs 1004 / 813 / 8 / 84 / 0, body 14 ANY (2 over-capture, 13 EMPTY), clean 158 / 160, leak 2 occ / 2 pages (BLL260). Every absolute below is the whole 2491-pair population. The eight single-page Inquiry golds Claude over-splits (BLL250 / 260 / 270, CEDK401, CEDO402, TWHT903, CEDR101, CEDR401 — 3-10 %) are a registry page_model item, the next round.",\n' + a)
a2 = '    "_note_r422e": "Round 422 ENABLED: SCAFFOLD 54.2320'; assert s.count(a2) == 1
s = s.replace(a2, '    "_note_intake_2026_09_22": "INTAKE 2026-09-22: SCAFFOLD 54.2466 @ 2377 -> 54.1172 @ 2491 pairs (population arithmetic = (54.2466 x 2377 + 51.42 x 114) / 2491; 0 movers on the pre-existing pairs); >=50 1464 -> 1531 (+67 = the new pages >= 50), >=75 238 -> 254 (+16), >=90 20 -> 23 (+3); RAW 38.249 -> 38.049; median 55.0. State outputs/_intake_2026-09-22_sk_final.json (= _r0d-20260922_sk_final.json for the dashboard).",\n' + a2)
a3 = '    "_note_r425": "Round 425 FINISHED: exact 14255 -> 14318'; assert s.count(a3) == 1
s = s.replace(a3, '    "_note_intake_2026_09_22": "INTAKE 2026-09-22: exact 14318 -> 15131 (+813), EXTRA 186 -> 194 (+8), missing 689 -> 773 (+84) = the text-matched pool 16620 -> 17624 (+1004) — all the 38 new modules\' own pages; the pre-existing 14318 / 186 / 689 / 23 EXACT.",\n' + a3)
a4 = '    "_note_r425": "Round 425 FINISHED: EMPTY 190 -> 193'; assert s.count(a4) == 1
s = s.replace(a4, '    "_note_intake_2026_09_22": "INTAKE 2026-09-22: over-capture 55 -> 57 (+2), EMPTY 193 -> 206 (+13), ANY 251 -> 265 (+14) = the 38 new modules\' own pages (BLL250 2, BLL260 3, BLL265, BLL266, BLL270, CEDO402, CEDR203, CEDR401, OSSM501, TRR110, TWHK902 — hand-off boxes and the over-split single-page modules); the pre-existing 2576 pages\' flags unchanged; runaway 5 EXACT.",\n' + a4)
a5 = '    "_note_r425": "Round 425 FINISHED: clean 2508 / 2552'; assert s.count(a5) == 1
s = s.replace(a5, '    "_note_intake_2026_09_22": "INTAKE 2026-09-22: clean 2532 / 2576 -> 2690 / 2736 = 98.32 (158 of the 160 new pages clean); leak 73 occ / 44 pages -> 75 / 46 = BLL260_0_0 ([tab n] x7) + BLL260_6_1 ([video 1]) — the new batch\'s own; the pre-existing 73 / 44 EXACT.",\n' + a5)
json.loads(s); wr(p, s)

# the loop file: §0 census table + no-build paragraph, §2 bullet
p = R + "LOOP__Autonomous_Rounds.md"; s = rd(p)
old = ("| Claude module dirs | 416 | **507** |\n| Claude pages | 2,109 | **2,583** |\n| gold dirs | 454 | **552** |\n"
       "| Writers Template / Media List docx | 619 | **762** |\n| skeleton paired pages | 1,956 | **2,377** |")
assert s.count(old) == 1
s = s.replace(old, ("| Claude module dirs | 416 | **545** |\n| Claude pages | 2,109 | **2,744** |\n| gold dirs | 454 | **552** |\n"
                    "| Writers Template / Media List docx | 619 | **762** |\n| skeleton paired pages | 1,956 | **2,491** |"))
o = "Current (22 September 2026, build 260619.97 — r425 finished, the 12 XOTP modules IN):"; assert s.count(o) == 1
s = s.replace(o, "Current (22 September 2026, build 260619.98 — after the 22 Sept Round 0d: the 12 XOTP modules and the 38 pre-intake never-converted modules are IN):")
m = re.search(r"\*\*552 gold dirs against 507 Claude dirs is CORRECT, not a fault — but the gap is 45, not 7\.\*\*.*?(?=\n\n## 1\. The measure of success)", s, re.S)
assert m, "census paragraph"
s = s.replace(m.group(0), ("**552 gold dirs against 545 Claude dirs is CORRECT, not a fault — the gap is exactly the 7 with no source.**\n"
    "The 7 (`GER1003–1007`, `SAM1005`, `SAM1006`) have no Writers Template at all (§2). The 12 XOTP modules joined the\n"
    "corpus when r425 finished (22 Sept 2026, session 33 Round 1) and **the 38 pre-intake never-converted modules\n"
    "joined at the 22 Sept Round 0d (session 33 Round 3: 38 / 38 converted, 0 refused — `LOOP_INTAKE__2026-09-22_38_Modules.md`)**.\n"
    "Three Claude dirs (`TRR104`, `TRR105`, `TRR115`) hold only a `_run.json` (no Writers Template / a pre-existing refusal)\n"
    "and are not pairs. A gold-only dir is the expected state for a recorded no-build. The table above and\n"
    "`_MIGRATION/verify_after_transfer.sh` lines 77–78 are updated at every finalise that changes them (`.pre-<tag>.bak` kept)."))
o = ("`PMT101` converts since r423 (the table-row page markers). **And 38\n"
     "  PRE-INTAKE modules hold a Writers Template but were never converted** (the §0 list: the\n"
     "  BLL243–BLL276 block, CEDK401, CEDO201, CEDO402, CEDR101, CEDR203, CEDR401, CEDT102, CEDW303,\n"
     "  HPRE301, OSSM501, SSCI104, SSEA203, SSOG105, TRR110, TWHK902, TWHK907, TWHR905, TWHR907,\n"
     "  TWHT903, XMES202) — their first conversion is a Round 0d job (§0); until it runs they count as\n"
     "  RECORDED no-builds, and once it has run each is either converted or recorded by cause.")
assert s.count(o) == 1
s = s.replace(o, ("`PMT101` converts since r423 (the table-row page markers). **The 38\n"
     "  PRE-INTAKE modules that held a Writers Template but were never converted** (the BLL243–BLL276\n"
     "  block, CEDK401, CEDO201, CEDO402, CEDR101, CEDR203, CEDR401, CEDT102, CEDW303, HPRE301, OSSM501,\n"
     "  SSCI104, SSEA203, SSOG105, TRR110, TWHK902, TWHK907, TWHR905, TWHR907, TWHT903, XMES202) were\n"
     "  converted at the 22 Sept 2026 Round 0d (session 33 Round 3): 38 / 38 built, 0 refused — they are\n"
     "  ordinary corpus members now (`LOOP_INTAKE__2026-09-22_38_Modules.md`)."))
o = "12 XOTP modules (`XOTPB08–13`, `XOTPG01`, `XOTPG03–06`, `XOTPO01`) are refused\n  until the r425 activity-table adapter is enabled (built and proven on the twelve on 21 Sept,\n  `Input_Doc_Rules.input_shapes.activity_table.adapter.enabled: false`; the spec is"
assert s.count(o) == 1
s = s.replace(o, "The 12 XOTP modules (`XOTPB08–13`, `XOTPG01`, `XOTPG03–06`, `XOTPO01`) convert\n  since r425 finished on 22 Sept (the activity-table adapter enabled,\n  `Input_Doc_Rules.input_shapes.activity_table.adapter.enabled: true`; the spec is")
wr(p, s)

# verify script
p = R + "_MIGRATION/verify_after_transfer.sh"; s = rd(p)
shutil.copyfile(p, p + ".pre-intake-2026-09-22.bak")
o1 = '"507"   # r425 finished (2026-09-22): 495 -> 507'; o2 = '"2583"   # r425 finished (2026-09-22): 2559 -> 2583'
assert s.count(o1) == 1 and s.count(o2) == 1
s = s.replace(o1, '"545"   # Round 0d (2026-09-22): 507 -> 545, the 38 pre-intake never-converted modules (all convert); r425 finished (2026-09-22): 495 -> 507')
s = s.replace(o2, '"2744"   # Round 0d (2026-09-22): 2583 -> 2744, the 38 modules x 161 pages; r425 finished (2026-09-22): 2559 -> 2583')
wr(p, s)
print("FINALISE_INTAKE_DONE")
