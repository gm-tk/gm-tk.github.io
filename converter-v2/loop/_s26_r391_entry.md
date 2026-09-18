## 2026-09-19 (round 391, build 260619.62) — THE OWN-ROW SUPERVISOR PANEL'S TEXT COLUMN IS `col-12 col-md-12` IN THE LEAVING TO LEARN FAMILY (`callouts.by_tag."supervisor note".inner_row.text_col_by_subject`, env `PANELCOL_OFF`); the autonomous loop's session 26 Round 5 — the r390 miner's one new row (#3735) decomposed; SCOPED regeneration of the 6 affected modules (scoped ship #3 since the r388 full); skeleton 53.518 → 53.525 % (+0.008pp; 23 movers 21 up / 2 down, named), ≥50 1157 → 1158, ≥75 191 / ≥90 15 EXACT, RAW 37.756 → 37.762 %; every other gate EXACT

### 1. WHAT CHANGED

The r160 inner-row supervisor panel template writes its TEXT column as `<div class="col-12">` — the corpus majority (gold `col-12` 327 / `col-12 col-md-12` 93; BLL 163 / 3, Mathematics 21 / 8). The Leaving to Learn family's own-row panels carry **`col-12 col-md-12`** (gold 28 / 37 = 0.76 on 35 pages / 15 modules; the XDLS90x series 28 / 37) — the r390 miner surfaced it as row #3735 (`body EXTRA div.col-12 › ul`, 32 pages / 14 modules, LtL 26): a parent-LABEL mismatch, the gold's `ul` keyed under a different parent class than Claude's, not an extra list.

**The fix (DATA OVER CODE):** `inner_row.text_col_by_subject {enabled, env: "PANELCOL_OFF", by_subject: {"Leaving to Learn": "col-12 col-md-12"}}` — `#calloutOpen`'s inner_row def swap rewrites the LAST `<div class="col-12">` of the open string to the subject's class (the module's `module_meta.subject`). The activity-owned panel template (`activity_wrapper.super_content.panel_open`) is untouched — measured separately (`_s26_r391_panelcol2.out`): LtL activity panels `col-md-12` 7 / 19 = 0.37, English 9 / 9 (ties). OFF = the r390 output (the probe 2109 / 2109).

### 2. HOW IT WAS FOUND

- `outputs/_s26_r391_panelcol.py` → `.out`: every super-content panel's text column (the inner row's last col), gold vs Claude, per template / subject / series; `_s26_r391_panelcol2.out` the own-row / activity split for the four candidate subjects. English own-row 7 / 9 = 0.78 sits on 9 pages (under the floor); ConnectED own-row 1 / 5, OS 2 / 4, BLL 3 / 169.
- KB-first: 05B / 01F give the `col-12` panel form (the BLL / MXDI majority); the LtL column is that family's own consensus → §1b level 4. A wrapper class token → structure-only, derivable.

### 3. THE PROBE + THE SCOPED REGENERATION + THE GATES

- Probe over all 416 (`_s26_r391_probe.cjs`): **OFF 2109 / 2109; ON 28 pages / 6 modules** (XDLS502 XDLS901 XDLS904 XDLS905 XDLS906 XDLS911 — XDLS908 / 909, XTAS102 / 103, XMES203's panels are activity-owned and stay `col-12` by design). Scored with the gate's own `match()` before regenerating: 28 paired, **21 up / 2 down / 5 same, pp-sum +15.2** (the 2 dips XDLS901_2_0 −0.9, XDLS901_4_0 −0.7 — XDLS901's gold panels are the family's `col-12` minority).
- 6 modules in 1 batch (rc 0); `fresh --affected` **0 truly stale**; the manifest diff = **28 pages / 6 modules, 0 added / removed**; **probe ON == disk 36 / 36**.
- **PRIMARY skeleton (`_s26_r391_sk_final.json`): SCAFFOLD 53.5175 → 53.5253 % (+0.008pp) / ≥50 1157 → 1158 (XDLS906_2_0 crosses up) / ≥75 191 / ≥90 15 / RAW 37.756 → 37.762 % @ 1956, skipped 0; 23 movers (21 up / 2 down, pp-sum +15.2 = the prediction), 0 outside the affected set** = 58.3 % of achievable. compare_structure **11700 / 172 / 625** EXACT; body_compare **42 / 4 / 173 / 218** EXACT; clean **2079 / 2102**, leak **26 / 23** EXACT; tags 9557 / 9557; every verifier RESULT identical to r390; 15 selftests + the skeleton selftest GREEN; fast-loop / manifest / feature index refreshed.
- The DIFF MINER re-mined: **178 CANDIDATE rows (178 → 178: #3735 GONE, one NEW #4286 `body EXTRA div.col-12.col-md-12 › ul`, 21 pages / 3 modules = XDLS904 / 905 / 906's panel lists — the writer's consecutive bullets are split by their trailing inline `[link to X]` markers into separate `<ul>`s where the gold ships ONE list; the next candidate, a list-merge question).

### 4. RECORDED

- A plateau-magnitude round (+0.008pp) but gold-matching on a whole family's wrapper class; §4's plateau window counts it (1 of 3) only if no other protected gate moved — ≥50 +1 moved, so it does not count.
- XDLS901's `col-12` panels (2 dips) are the LtL family's own 0.24 minority.
