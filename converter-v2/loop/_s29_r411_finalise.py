#!/usr/bin/env python3
"""r411 finalise (CLAUDE.md §12): changelog entry, Config.js bump, CLAUDE.md §9 / §11 / §14, gate_baseline.json."""
import re, json
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
PF = R + "pageforge-site/converter-v2/"

def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

# ---------- 1. changelog ----------
entry = """## 2026-09-20 (round 411, build 260619.82) — THE TILE DIALECT'S MENU TAKES THE GOLD'S ROW+COL TABS SHELL: `moduleMenu › div.row › div.tabs.col-12`, the form every other tabs menu already ships (the autonomous loop's session 29 Round 2 — the DIFF MINER's rows #47 / #48, surfaced by r410; **SCOPED regeneration of the 21 WJFUN modules — scoped ship #3 since the 19 Sept FULL**; every protected gate held-or-improved: skeleton +0.0058pp, 21 up / 0 down)

### 1. WHAT CHANGED

**The class (DIFF_QUEUE #47 `module-menu MISSING div.row › WIDGET` + #48 `SUBSTITUTED div#module-menu-content.moduleMenu › div.row / WIDGET`, 22 pages / 22 modules, subject=1-10 Writing c=1.00 n=21).** The r410 tile dialect composes its menu through `MenuBuilder.#levelTabs` → the r221 `writer_tabs` shell, which is BARE (`moduleMenu › div.tabs`) by design for its own family (ENGJ403's gold) and for the r265 CHFUN level pages (gold bare 6 / 6). The WJFUN gold wraps the tabs in the corpus form — `div.row › div.tabs.col-12` — on 21 / 21. Measured on every paired page whose gold `#module-menu-content` holds a tabs menu (`_s29_r2_menutabs.py` → `_s29_r2_menutabs.out`, the gate's own pairing, 293 pages / 246 modules): the gold is ROW+COL **279 = 0.95** (BARE 13 = 0.04: CHFUN 6, ENGJ 1, BLL / BLLR / SSFUN scatter); Claude already emits ROW+COL on 253 (the `tabs` / `tabs_two_col` / `reo_tabs` shells) and is bare on 29 — **the 21 WJFUN overviews + ENGS404 are the only pages where the gold is ROW+COL and Claude is bare.** Per subject every group ≥ 0.86 ROW+COL except 1-10 Languages (CHFUN's gold IS bare). Authority §1b 3 — the family's own gold, agreeing with the corpus convention; the KB's 06 §3.3 has no tabs-shell rule. NEW-FAMILY CHECK: the class holds outside the family (0.95), and Claude is already right there, so the fix is confined to the tile dialect's registry.

**The fix (DATA OVER CODE, env `TILEMENUROW_OFF`).** `Emit_Templates.menu.shells.writer_tabs_row` — the writer-tabs shell in the ROW+COL form; `body_region.fundamentals_panels.tile_pages.menu.shell_row {enabled, env, shell}` names it. `MenuBuilder.#levelTabs` returns the shell key when its cfg carries the block (the level-pages cfg does not → CHFUN keeps the bare shell), both call sites pass `wtShell`, and `SkeletonBuilder`'s shell selection honours `content.menu.wtShell` when the name exists in `menu.shells` (else the bare `writer_tabs`). OFF = the r410 output byte-for-byte.

### 2. PROOF

- `_s29_r411_probe_run.sh` (the r410 harness over all 494 Claude-dir modules): **OFF = disk 2555 / 2555** (516 + 711 + 816 + 512, 0 changed); **ON = exactly the 21 WJFUN overviews**, the other 473 modules / 2534 pages byte-identical — CHFUN01 / 04–08 (the bare-gold level pages) and ENGS404 (the writer partition) untouched by construction.
- `_s29_r411_pagescore.py` (the gate's own `match()` on the ON pages before regenerating): **21 / 21 up, pp-sum +13.6 scaffold (mean +0.65 per page) / +87.3 RAW**, 0 down — WJFUN105 35.5 → 36.7, WJFUN109 62.7 → 63.6, WJFUN107 52.6 → 53.4, WJFUN106 44.2 → 45.0 …
- `REGENERATE CORPUS - the WJFUN modules` → the 21 (`_affected_r411.txt`, 2 batches rc 0); `scoped_ship.sh --affected _affected_r411.txt --toggle TILEMENUROW_OFF --no-regen --commit --round 411` (`_s29_r411_scoped_ship.log`): **0 truly stale**, **containment 21 ⊆ 21**, the 12-module spot-check (BLL164 BLL172 BLL237 ENGI405 ENGJ403 ENGR101 HPFUN403 OSBY201 OSOH401 PHE1004 TRR111 XMES102, regenerated with the fix ON — ENGJ403, the bare shell's own family, among them) **all byte-identical**; the decomposition PASS.
- `_s29_skdelta.py _s29_r410_sk_final.json _s29_r411_sk_final.json`: **21 movers, 21 up / 0 down, 0 outside the affected set, 0 pages added or gone.**

### 3. PROTECTED GATES (all HELD-or-IMPROVED — `_s29_r411_gates.log`, `_s29_r411_scoped_ship.log`)

- **Skeleton (PRIMARY)**: SCAFFOLD **53.789 → 53.795 % (+0.0058pp)**; ≥50 **1406** / ≥75 **236** / ≥90 **20** EXACT; RAW **37.925 → 37.963 %**; 2349 pairs / 0 skipped (state `outputs/_s29_r411_sk_final.json`).
- **compare_structure** exact **14175** / EXTRA **186** / MISSING **690** / row-wrap **23** EXACT (a `#header`-scoped change — invisible to it by construction); **body_compare** 54 / 6 / 190 / 248 EXACT; **defect audit** clean **2504 / 2548 = 98.27 %**, leak **73 / 44** EXACT.
- tags **9557 / 9557**; flipCard 61 / divergence 0; speechBubble defect 4 (baseline); modal 0; mtkQuiz 0; math 323 / 323; menulabels 99 / 0; dragAndDrop 21 / 0; entry-parity PASS; **16 selftests GREEN** (46 PASS / GREEN, 0 FAIL); feature index GREEN.
- Ship ledger: **scoped ship #3 since the 19 Sept FULL** (5 of headroom); fast-loop baseline + content manifest refreshed.
- DIFF MINER re-mined on the r411 corpus (`_diff_miner_s29_r411.log`): **184 → 182 CANDIDATE rows** — GONE: exactly this round's two rows (#47 / #48); NEW: none.
- Plateau: **+0.0058pp, no bucket moved — the window advances to 1 of 3** (r410 reset it). Read on the post-intake 2,349-pair population (§1e).

### 4. RECORDED, NOT TAKEN

- **ENGS404** (Standard, 1-10 English) takes the r221 writer tab-partition path and its gold is ROW+COL, while its sibling ENGJ403's gold is bare — a tie at n = 2, under the floor; the bare shell stays the partition's default.
- The 9 pages where Claude's tabs menu opens `div.row › div.col-md-8.col-12` while the gold's is `div.row › div.tabs.col-12` (ANZH ×2, HIS ×2, XDLS, PES, CEDO …) — a different class (the simplified-vs-tabs verdict on those pages), ≈ 9 modules, under the 10-module chrome floor.
- The 6 pages where the gold is bare and Claude ROW+COL (BLL / BLLR / SSFUN) — under the floor.

"""
p = PF + "BUILD_CHANGELOG.md"; s = rd(p)
head, rest = s.split("\n", 1)
assert head.startswith("# BUILD CHANGELOG") and rest.lstrip("\n").startswith("## 2026-09-20 (round 410")
wr(p, head + "\n\n" + entry + rest.lstrip("\n"))

# ---------- 2. Config.js ----------
p = PF + "app/js/Config.js"; s = rd(p)
old = '\tstatic AppVersion = "260619.81";'; assert s.count(old) == 1
note = ("\t// ROUND 411 (260619.82): the tile dialect's menu takes the gold's ROW+COL tabs shell — `moduleMenu › div.row › div.tabs.col-12`, the form "
        "every other tabs menu already ships (the gold 279 / 293 = 0.95; WJFUN 21 / 21); the r410 branch had inherited the bare r221 writer_tabs "
        "shell. `menu.shells.writer_tabs_row` + `tile_pages.menu.shell_row`, MenuBuilder.#levelTabs → wtShell → SkeletonBuilder; env TILEMENUROW_OFF. "
        "The loop's session 29 Round 2 (DIFF MINER rows #47 / #48): OFF = disk 2555 / 2555, ON exactly the 21 WJFUN overviews (21 up / 0 down, +13.6pp-sum); "
        "SCOPED regeneration of the 21 (scoped ship #3 since the 19 Sept FULL); skeleton 53.789 → 53.795 % (+0.0058pp), every other gate EXACT; miner 184 → 182.\n")
wr(p, s.replace(old, note + '\tstatic AppVersion = "260619.82";'))

# ---------- 3. CLAUDE.md ----------
p = PF + "CLAUDE.md"; s = rd(p)
old9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 410 BASELINE ("; assert s.count(old9) == 1
new9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 411 BASELINE (the tile dialect's menu takes the gold's ROW+COL tabs shell — "
        "`menu.shells.writer_tabs_row` + `tile_pages.menu.shell_row`, env `TILEMENUROW_OFF`; 21 WJFUN modules / 21 pages; SCOPED regeneration of the 21, "
        "the probe proving the other 473 byte-identical; scoped ship #3 since the 19 Sept full): SCAFFOLD mean 53.795% / >=50% 1406 / >=75% 236 / >=90% 20 / "
        "RAW 37.963% @ 2349 pairs, pairs skipped 0 — hold-or-improve; 21 movers (21 up, 0 down; 0 outside the affected set); the 2328 unaffected pairs EXACT. "
        "compare_structure exact 14175 / EXTRA 186 / MISSING 690 / row-wrap 23 EXACT; body_compare 54 / 6 / 190 / 248 EXACT; defect clean 2504 / 2548 = 98.27%, "
        "leak 73 / 44 EXACT.** Previous — ROUND 410 BASELINE (")
s = s.replace(old9, new9)
old11 = "| `TILEPAGE_OFF` | 410 | **THE WJFUN \"MY TE KURA WRITING\" TILE-PAGE DIALECT**"; assert s.count(old11) == 1
row11 = ("| `TILEMENUROW_OFF` | 411 | **THE TILE DIALECT'S MENU TAKES THE GOLD'S ROW+COL TABS SHELL** (the autonomous loop's session 29 Round 2 — the DIFF MINER's "
         "rows #47 / #48, surfaced by r410). The r410 tile dialect composed its menu through `MenuBuilder.#levelTabs` → the r221 `writer_tabs` shell, BARE "
         "(`moduleMenu › div.tabs`) by design for the writer tab partition (ENGJ403's gold) and the r265 CHFUN level pages (gold bare 6 / 6); the WJFUN gold "
         "wraps the tabs in the corpus form `div.row › div.tabs.col-12` on 21 / 21 — and measured on every paired page whose gold menu is a tabs menu "
         "(`_s29_r2_menutabs.py`, 293 pages / 246 modules) the gold is ROW+COL 279 = 0.95, Claude already emitting it on 253; the 21 WJFUN overviews + ENGS404 "
         "were the only ROW+COL-gold / bare-Claude pages. Data `menu.shells.writer_tabs_row` (the ROW+COL writer-tabs shell) + "
         "`body_region.fundamentals_panels.tile_pages.menu.shell_row {enabled, env, shell}`; `#levelTabs` returns the shell key when its cfg carries the block "
         "(the level-pages cfg does not → CHFUN stays bare), `wtShell` rides the menu result, `SkeletonBuilder` selects it when the name exists in `menu.shells`. "
         "OFF = the r410 output byte-for-byte (2555 / 2555). ON = exactly the 21 WJFUN overviews, 21 up / 0 down (+13.6pp-sum). Recorded: ENGS404 (the partition "
         "path; its sibling ENGJ403's gold bare — a tie at n = 2); the 9 `row › col-md-8` pages and the 6 bare-gold pages, both under the floor. |\n")
s = s.replace(old11, row11 + old11)
old14 = "- **Build:** `260619.81` (round 410 — **the WJFUN \"My Te Kura Writing\" tile-page dialect"; assert s.count(old14) == 1
b14 = ("- **Build:** `260619.82` (round 411 — **the tile dialect's menu takes the gold's ROW+COL tabs shell** (`moduleMenu › div.row › div.tabs.col-12` — the "
       "form every other tabs menu already ships: the gold 279 / 293 = 0.95, WJFUN 21 / 21; the r410 branch had inherited the bare r221 writer_tabs shell; "
       "`menu.shells.writer_tabs_row` + `tile_pages.menu.shell_row`, `MenuBuilder.#levelTabs` → `wtShell` → `SkeletonBuilder`, env `TILEMENUROW_OFF`); the "
       "autonomous loop's session 29 Round 2 — the DIFF MINER's rows #47 / #48; the probe OFF = disk 2555 / 2555, ON exactly the 21 WJFUN overviews (21 up / "
       "0 down, +13.6pp-sum, 0 outside the set); **SCOPED regeneration of the 21 (scoped ship #3 since the 19 Sept FULL)**; **ROUND 411 BASELINE: SCAFFOLD mean "
       "53.795% / >=50% 1406 / >=75% 236 / >=90% 20 / RAW 37.963% @ 2349 pairs** (+0.0058pp; buckets EXACT); compare_structure 14175 / 186 / 690 / 23, body 54 / 6 / 190 / 248, "
       "clean 2504 / 2548, leak 73 / 44 — all EXACT; every verifier EXACT; 16 selftests GREEN; the miner 184 → 182 (the two rows gone, nothing new); plateau window 1 of 3). Previous: ")
s = s.replace(old14, b14 + old14)
wr(p, s)

# ---------- 4. gate_baseline.json ----------
p = R + "CONVERTER_V2/reference/tests/gate_baseline.json"; s = rd(p)
def setv(key, old, new):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=1); assert n == 1, key
setv("build", '"260619.81"', '"260619.82"'); setv("round", 410, 411)
setv("mean_scaffold_pct", 53.79, 53.79)  # unchanged at 2 dp (53.7949) — kept for the assert
setv("raw_mean_pct", 37.93, 37.96)
a = '    "_note_r410": "Round 410 (session 29 Round 1'; assert s.count(a) == 1
s = s.replace(a, '    "_note_r411": "Round 411 (session 29 Round 2): the tile dialect\'s menu takes the gold\'s ROW+COL tabs shell (menu.shells.writer_tabs_row + tile_pages.menu.shell_row, env TILEMENUROW_OFF; 21 WJFUN modules / 21 pages; SCOPED regeneration of the 21, scoped ship #3 since the 19 Sept full; the probe OFF = disk 2555/2555, ON exactly the 21 WJFUN overviews). Skeleton 53.7891 -> 53.7949 (+0.0058pp; 21 movers, 21 up / 0 down, 0 outside the set), >=50 1406, >=75 236, >=90 20 EXACT, RAW 37.925 -> 37.963; compare_structure 14175 / 186 / 690 / 23 EXACT; body_compare 54 / 6 / 190 / 248 EXACT; defect clean 2504/2548, leak 73 / 44 EXACT; every verifier EXACT; 16 selftests GREEN.",\n' + a)
a2 = '    "_note_r410": "Round 410: SCAFFOLD 53.6797'; assert s.count(a2) == 1
s = s.replace(a2, '    "_note_r410b": "Round 411: SCAFFOLD 53.7891 -> 53.7949 (+0.0058pp; 21 movers all up — the WJFUN tile menu shell; 0 outside the 21-module affected set), buckets 1406 / 236 / 20 EXACT, RAW 37.925 -> 37.963; 2349 pairs. State outputs/_s29_r411_sk_final.json. Hold-or-improve from here.",\n' + a2)
wr(p, s); json.load(open(p, encoding="utf-8"))
print("r411 finalise: changelog + Config.js 260619.82 + CLAUDE.md §9/§11/§14 + gate_baseline.json done")
