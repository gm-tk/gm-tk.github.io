## 2026-09-19 (round 397, build 260619.68) — A TABLE HEADER CELL IS PLAIN: the writer's **bold** header row renders `<th>text</th>`, not `<th><b>text</b></th>` (`elements.table.header_cell_plain`, `TablesAndGrids`' cell emit, env `THPLAIN_OFF`); the autonomous loop's session 26 Round 11 — the r394 miner row #3725 followed through; SCOPED regeneration of the 58 affected modules (scoped ship #1 since the r396 full); skeleton 53.684 → 53.695 % (+0.012pp; 80 movers 70 up / 7 down), ≥50 1163 / ≥75 195 / ≥90 18 EXACT, RAW 37.780 → 37.782 %; every other gate EXACT, every verifier RESULT identical

### 1. WHAT CHANGED

The r383 first-row-header rule promotes a writer's wholly-bold first row to `<th>`; the cell's own `**…**` markdown then rendered `<b>` inside it. The position-free census (`outputs/_s26_r397_thb.py` → `.out`, every `<th>` in every paired page's live body): **the gold's 2170 header cells are wholly bold 97 = 0.04 (plain 0.96); Claude's 2012 were wholly bold 369 = 0.18 on 86 pages / 56 modules** — Mathematics gold 0.93 plain (Claude bold 114 on 24 pages / 15 modules), ConnectED 0.98 (44 on 14 pages), TEDC 1.00 (37 on 8), NCEA1 1.00 (25 on 7), EXPlore 1.00 (39 on 3), Leaving to Learn 1.00 (11 on 5); English is the one place the gold keeps some bold (0.17) and Claude was already below it there.

**The fix (DATA OVER CODE):** `elements.table.header_cell_plain {enabled, env: "THPLAIN_OFF"}` — at the cell emit in `TablesAndGrids` (free-body tables only, `!insidePlaceholder`): a header cell whose rendered content is exactly ONE `<b>…</b>` / `<strong>…</strong>` span with no other bold inside drops the wrapper; data cells (`<td>`) keep theirs (the gold keeps `<td><b>` for a matrix's row labels). OFF = the r396 output (the probe 2109 / 2109).

### 2. HOW IT WAS FOUND

- The r394 miner's row #3725 (`body EXTRA th>b › b`, 20 pages / 15 modules, consensus 1.00) fell under the floor at r394's re-mine — the position-free census showed the class four times larger than the alignment could see.
- KB-first: 05D's table forms are `<tr><th>Header 1</th><th>Header 2</th></tr>` — plain header cells; `renderCellInline`'s own comment already states the convention for tag-rendered cells ("PLAIN text in a HEADER cell — already bold by default in the site's CSS"), the markdown path had kept the wrapper → §1b level 1 / 3. Markup-only, deterministic → derivable.

### 3. THE PROBE + THE SCOPED REGENERATION + THE GATES

- Probe over all 416 (`_s26_r397_probe.cjs`): **OFF 2109 / 2109; ON 92 pages / 58 modules** (every change a `<th><b>…</b></th>` → `<th>…</th>`). Scored with the gate's own `match()` before regenerating: 87 paired, **73 up / 7 down / 7 same, pp-sum +23.0**; the 7 dips are English pages whose own gold keeps the bold (ENGJ403_6_0 −0.9, ENGI405_6_0 −0.8, ENGJ402_4_0 −0.6) and three ≤ −0.7 alignment shifts.
- 58 modules in 7 batches (all rc 0); `fresh --affected` **0 truly stale**; the manifest diff = **92 pages / 58 modules, 0 added / removed** (= the probe's ON set); **probe ON == disk 430 / 430**.
- **PRIMARY skeleton (`_s26_r397_sk_final.json`, delta `_s26_r397_sk_delta.log`): SCAFFOLD 53.6835 → 53.6953 % (+0.012pp) / ≥50 1163 / ≥75 195 / ≥90 18 / median 54.3 EXACT / RAW 37.780 → 37.782 % @ 1956, skipped 0; 80 movers (70 up / 7 down, pp-sum +23.6), 0 outside the affected set**. Best: SCFUN01_0_0 +7.3, XTAS103_3_1 +4.1. compare_structure **11723 / 172 / 626** EXACT; body_compare **42 / 4 / 173 / 218** EXACT; clean **2079 / 2102**, leak **26 / 23** EXACT; every verifier RESULT identical to r396; 15 selftests + the feature-index selftest GREEN; fast-loop / manifest / feature index refreshed.
- The DIFF MINER re-mined (`_diff_miner_s26_r397.log`): **173 CANDIDATE rows — unchanged** (the `th>b` class was already under the alignment's floor).

### 4. RECORDED

- A plateau-magnitude round (+0.012pp, no bucket moved) — the §4 window stands at **2 of 3** (r396 was the first).
- Measured and DECLINED the same round: the speech bubble's character image (`_s26_r397_bubbles.py` / `_bubbles2.py` / `_bubbles3.py`): Claude ships 454 text-only `bubble-top` speech bubbles on 129 pages / 62 modules where the gold ships a bubble WITH a developer-chosen character image (Online Safety 0.95, TEDC 0.91, Inquiry-LtL 0.65 — iStock stock photos and module mascots such as "Kōwhai Quill, a friendly bookworm") in five column layouts none ≥ 0.6 (`col-md-2 | col-md-6` 117, `col-md-4 | col-md-8` 32, text-left / image-right 41 …); Leaving to Learn (0.68 text-only), English and Mathematics (ties) keep Claude's form. The image is the developer's asset choice, not in the WT — a needs-Chris question (a placeholder character image per subject?), not a rule.
