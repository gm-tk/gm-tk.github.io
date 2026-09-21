#!/usr/bin/env python3
"""r422 finalise (DECLINED-INERT — the r369 / r404 precedent): changelog entry, Config.js bump, CLAUDE.md §11 / §14, gate_baseline.json
build / round (no metric moves — the corpus is byte-identical), LOOP_STATE.md (the Round 5 record + Round-log line). Run under WSL."""
import re, json, io, os
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
PF = R + "pageforge-site/converter-v2/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

entry = """## 2026-09-21 (round 422, build 260619.93) — THE SIDE-TAB-NAVIGATION FUNDAMENTALS DIALECT (the FRFUN family) — BUILT, MEASURED, SHIPPED INERT (`side_tab_nav.enabled: false`, the r369 / r404 precedent; the autonomous loop's session 30 Round 5; the corpus byte-identical)

### 1. WHAT CHANGED

**The class (the s28 "multi-file level-page renderer" follow-up, decomposed from the DIFF MINER's F23).** FRFUN06 authors each lesson page as `[Side tab navigation]` + a ONE-COLUMN TABLE of the tab labels (the crumb list), then one `[Side tab navigation] <label>` per panel (the label typed black OR inside the red span) + `[Title] [H2]` + the panel's content. The lexicon reads `[Side tab navigation]` as `tab n`, so the r100 BLL inquiry mode already FIRED on these pages (`_emptyOpeners` ≥ 2 because the red-span labels read as empty) — but the base walk only knows `[Tab N]`: a labelled nav tag has no N, so its label was dropped and NO panel opened. Claude's FRFUN06 lesson pages shipped `body.inquiry` + `div.crumbs` with two EMPTY crumbs + 3 `inquiryPanel`s, the label table rendered as a table inside panel 1 (`_s30_r5_items.cjs` — the item stream). The gold: `body.fundamentals.container-fluid.noPhase` + `div.phases` (the N labels, the first `showing`, `phase="1..N"`) + one `div.fundamentalsPanel[phase]` per tab (the first `showing`), no module menu, the `footer-nav fundamentals-nav` footer — 10 / 10 lesson pages of FRFUN06.

**The build (DATA OVER CODE).** `inquiry_tabs.side_tab_nav {enabled, env SIDETABNAV_OFF, nav_tag_pattern, min_labelled 3, label_table, label_max_words 4, flavour, flavours.fundamentals {crumbs_open, crumb_item, crumb_showing_attr, crumbs_close, panel_open, panel_showing_class, panel_close, body_class, footer_class, lesson_menu}}`. ContentConverter: a page with ≥ `min_labelled` labelled nav tags fires side-tab mode (the shared inquiry machinery runs); the bare nav tag + its label table are consumed; each labelled nav tag closes an open activity, breaks the row, pushes the sentinel and records its label (`inquiryLabels[++sideTabCount]`); the page result carries `inquiryFlavour` and, for a lesson page whose flavour says `lesson_menu: "none"`, `menu: {kind: "none"}`. `PanelsBuilder.inquiryPanels` gains the `sideTabMode` branch: N UNIFIED crumbs (the writer's own labels — the first IS the Introduction, no synthetic intro crumb) + N panels, the first of each `showing`, numbered `phase="1..N"`, from the flavour's templates; a non-empty lead segment before the first tab is prepended to panel 1. SkeletonBuilder takes the flavour's `body_class` / `footer_class` when the page built its panels.

**Measured (the in-memory probe, `_s30_r422_on`; `_s30_r422_pagescore.py` on the gate's own `match()`):** FRFUN06 10 / 10 pages change — **8 up / 2 down, SCAFFOLD pp-sum +34.7 (mean +3.5pp per page), RAW +22.5** (FRFUN06_4_0 +12.0, _3_0 +6.1, _5_0 +5.9, _1_0 +5.7, _8_0 +5.6; _7_0 −11.4 = its Emergent page pairs against a Novice gold, _9_0 −0.1). **FRFUN07 / FRFUN08 do not change**: they author their side tabs as PAGE navigation (one lesson per page, `[End page]` after each, the label table = the lesson list) and their gold lesson pages are plain `body.fundamentals.container-fluid` bodies with no phases (`_s30_r5_items.cjs` FRFUN07; the gold files) — a different, plain shape.

**Why INERT.** The in-page side-tab shape is **10 pages / 1 module** — under the 20-page body floor (§1d), and a one-module dialect is exactly what the floor exists to keep out of the general rules. The renderer now exists behind its data flag (the s28 follow-up delivered), the corpus is byte-identical with it off, and **enabling it is Chris's call** (`side_tab_nav.enabled: true` + regenerate FRFUN06 — expected +34.7pp-sum on the 10 pages; the round's NEEDS-CHRIS line). Recorded with it: FRFUN07 / 08's remaining gap is the registry row (they run on global defaults — `body.container-fluid` where the gold has `fundamentals`; the r408 "faithful row" scored 26 / 28 pages DOWN and was held back — its re-measure per page is the next FRFUN item), and the `[<Level> Page N]` title marker as a page boundary (Claude's FRFUN page 0 holds the overview AND Novice page 1; the gold has 11 files to Claude's 10).

### 2. PROOF

- `_s30_r422_probe_run.sh ON` (the live data with `enabled: false`, all 494 Claude-dir modules): **identical 2555 / 2555** — the corpus is byte-identical; `_content_manifest.py changed` = none; 16 verifier selftests + the skeleton selftest GREEN (`_s30_r422_selftests.log`); entry parity PASS; index-sync OK.
- The dialect's own probe (enabled true, in memory): FRFUN06 10 changed / FRFUN07 9 identical / FRFUN08 11 identical; the built lesson page 1: `div.phases` with 5 labels (Introduction showing), 5 `fundamentalsPanel`s, `body.fundamentals.container-fluid.noPhase`, `footer-nav fundamentals-nav`, no module menu (`_s30_r422_on/FRFUN06/`).

### 3. PROTECTED GATES

- Unchanged — the corpus is byte-identical to r421 (skeleton 54.2065 % / 1441 / 238 / 20, RAW 38.229; cs 14170 / 186 / 683 / 23; body 54 / 5 / 190 / 247; clean 2504 / 2548; leak 73 / 44; tags 9557; every verifier as at r421). No regeneration; the ledger stays at scoped #5 since the r416 FULL.

"""
p = PF + "BUILD_CHANGELOG.md"; s = rd(p)
head, rest = s.split("\n", 1)
assert head.startswith("# BUILD CHANGELOG") and rest.lstrip("\n").startswith("## 2026-09-21 (round 421")
wr(p, head + "\n\n" + entry + rest.lstrip("\n"))

p = PF + "app/js/Config.js"; s = rd(p)
old = '\tstatic AppVersion = "260619.92";'; assert s.count(old) == 1
note = ("\t// ROUND 422 (260619.93): THE SIDE-TAB-NAVIGATION FUNDAMENTALS DIALECT (FRFUN06: `[Side tab navigation]` + a label table, then one labelled nav tag per "
        "panel) — ContentConverter's side-tab mode + PanelsBuilder.inquiryPanels' sideTabMode branch (N unified phases + N fundamentalsPanels from the flavour "
        "templates) + SkeletonBuilder's flavour body / footer class and lesson_menu none (inquiry_tabs.side_tab_nav, env SIDETABNAV_OFF). BUILT and MEASURED "
        "(FRFUN06 10 pages: 8 up / 2 down, +34.7pp-sum; FRFUN07 / 08 unchanged — their side tabs are page navigation) but SHIPPED INERT (enabled: false): 10 "
        "pages / 1 module is under the 20-page floor — enabling it is Chris's call. The loop's session 30 Round 5; the corpus byte-identical (2555 / 2555).\n")
wr(p, s.replace(old, note + '\tstatic AppVersion = "260619.93";'))

p = PF + "CLAUDE.md"; s = rd(p)
old11 = "| `CODEREG_OFF` | 421 | **THE REGISTRY-KNOWN MODULE CODE"; assert s.count(old11) == 1
row11 = ("| `SIDETABNAV_OFF` | 422 | **THE SIDE-TAB-NAVIGATION FUNDAMENTALS DIALECT — SHIPPED INERT (`inquiry_tabs.side_tab_nav.enabled: false`)** (the autonomous "
         "loop's session 30 Round 5; the s28 'multi-file level-page renderer' follow-up from the miner's F23). FRFUN06 authors each lesson page as `[Side tab "
         "navigation]` + a one-column TABLE of tab labels, then one `[Side tab navigation] <label>` per panel (the label black or inside the red span) + `[Title] [H2]` "
         "+ content; the lexicon reads the tag as `tab n`, the r100 inquiry mode fired, but the base walk knows only `[Tab N]` — the labels were dropped and no panel "
         "opened (two empty crumbs, 3 panels, the label table rendered). The build: side-tab mode in ContentConverter (≥ `min_labelled` labelled nav tags; the bare tag + "
         "its label table consumed; each labelled tag closes an open activity, pushes the sentinel, records its label), `PanelsBuilder.inquiryPanels` `sideTabMode` (N "
         "unified crumbs + N panels, the first `showing`, `phase=\"1..N\"`, from `flavours.fundamentals` — the gold's `div.phases` + `div.fundamentalsPanel`), "
         "SkeletonBuilder's flavour `body_class` (`fundamentals container-fluid noPhase`) / `footer_class` (`fundamentals-nav`) and `lesson_menu: none`. MEASURED: "
         "FRFUN06 10 / 10 pages, 8 up / 2 down, +34.7pp-sum (FRFUN06_4_0 +12.0); FRFUN07 / 08 unchanged (their side tabs are PAGE navigation, plain fundamentals bodies). "
         "INERT because 10 pages / 1 module is under the 20-page floor — **enabling it is Chris's call** (set `enabled: true`, regenerate FRFUN06). The corpus is "
         "byte-identical with it off (2555 / 2555). |\n")
s = s.replace(old11, row11 + old11)
old14 = "- **Build:** `260619.92` (round 421 — **the registry-known module code"; assert s.count(old14) == 1
b14 = ("- **Build:** `260619.93` (round 422 — **the side-tab-navigation fundamentals dialect (FRFUN06) — BUILT, MEASURED, SHIPPED INERT** (`inquiry_tabs.side_tab_nav`, "
       "`enabled: false`, env `SIDETABNAV_OFF`; ContentConverter side-tab mode + `PanelsBuilder.inquiryPanels` sideTabMode + SkeletonBuilder's flavour body / footer): "
       "FRFUN06 10 pages 8 up / 2 down, +34.7pp-sum in the in-memory probe; FRFUN07 / 08 unchanged; 10 pages / 1 module is under the 20-page floor — enabling it is "
       "Chris's call; the autonomous loop's session 30 Round 5; the corpus byte-identical to r421 (2555 / 2555), no regeneration, every gate as at r421). Previous: ")
s = s.replace(old14, b14 + old14)
wr(p, s)

p = R + "CONVERTER_V2/reference/tests/gate_baseline.json"; s = rd(p)
def setv(key, old, new):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=1); assert n == 1, key
setv("build", '"260619.92"', '"260619.93"'); setv("round", 421, 422)
a = '    "_note_r421": "Round 421 (session 30 Round 4)'; assert s.count(a) == 1
s = s.replace(a, '    "_note_r422": "Round 422 (session 30 Round 5): the side-tab-navigation fundamentals dialect (FRFUN06) BUILT and MEASURED (+34.7pp-sum on 10 pages) but SHIPPED INERT (inquiry_tabs.side_tab_nav.enabled false — 10 pages / 1 module, under the floor; enabling it is Chris\'s call). The corpus is byte-identical to r421; no metric moves.",\n' + a)
wr(p, s); json.load(open(p, encoding="utf-8"))

# ---- LOOP_STATE.md: the Round 5 record + Round-log line + Position
p = R + "LOOP_STATE.md"; lines = io.open(p, encoding="utf-8").read().split("\n")
def idx(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix): return i
    raise SystemExit("not found: " + prefix)
b = idx("## Round log")
lines[b:b] = [
    "## Session 30 — Round 5 (engine r422, DECLINED-INERT, no regen) — THE SIDE-TAB-NAVIGATION FUNDAMENTALS DIALECT (FRFUN06) — BUILT, MEASURED, SHIPPED INERT",
    "- **The class** (the s28 'multi-file level-page renderer' follow-up, from F23): FRFUN06 authors each lesson page as `[Side tab navigation]` + a one-column label TABLE, then one `[Side tab navigation] <label>` per panel (the label black or inside the red span) + `[Title] [H2]` + content. The lexicon reads the tag as `tab n`, the r100 inquiry mode fired, but the base walk knows only `[Tab N]`: the labels were dropped, no panel opened — Claude shipped `body.inquiry` + 2 EMPTY crumbs + 3 inquiryPanels with the label table rendered (`_s30_r5_items.cjs`). The gold: `body.fundamentals.container-fluid.noPhase` + `div.phases` (N labels, the first `showing`, phase 1..N) + N `fundamentalsPanel`s, no menu, the `fundamentals-nav` footer — 10 / 10 FRFUN06 lesson pages.",
    "- **Built** (`inquiry_tabs.side_tab_nav` + flavours; ContentConverter side-tab mode; `PanelsBuilder.inquiryPanels` sideTabMode; SkeletonBuilder flavour body / footer; `lesson_menu: none`) and **measured** (`_s30_r422_on`, `_s30_r422_pagescore.py`): FRFUN06 10 / 10 pages — **8 up / 2 down, +34.7pp-sum** (FRFUN06_4_0 +12.0, _3_0 +6.1, _5_0 +5.9, _1_0 +5.7; _7_0 −11.4 = an Emergent page paired to a Novice gold). **FRFUN07 / 08 unchanged**: their side tabs are PAGE navigation (one lesson per page, the label table = the lesson list) and their gold lesson pages are plain `body.fundamentals.container-fluid` bodies.",
    "- **Verdict: DECLINED-INERT** — 10 pages / 1 module is under the 20-page body floor (§1d); `enabled: false` (the r369 / r404 precedent), env `SIDETABNAV_OFF`; the corpus byte-identical (probe 2555 / 2555; `_content_manifest.py changed` = none); 16 verifier selftests + skeleton selftest GREEN, entry parity PASS, index sync OK. **NEEDS CHRIS (not a block):** enable the FRFUN06 dialect? (`side_tab_nav.enabled: true` + regenerate FRFUN06 → +34.7pp-sum expected on 10 pages). Recorded follow-ups: FRFUN07 / 08 run on global defaults (`body.container-fluid` where the gold has `fundamentals`) — the r408 faithful row's per-page re-measure; the `[<Level> Page N]` title as a page boundary (Claude's page 0 = the overview + Novice page 1; the gold has 11 files to Claude's 10).",
    "",
]
t = idx("- s30-r4 (engine r421")
lines.insert(t, "- s30-r5 (engine r422, build 260619.93, DECLINED-INERT, no regen, 21 Sept ≈18:32 → 18:50) · THE SIDE-TAB-NAVIGATION FUNDAMENTALS DIALECT — FRFUN06's `[Side tab navigation]` + label table + one labelled nav tag per panel → the gold's `div.phases` + N `fundamentalsPanel`s, `body.fundamentals.noPhase`, the fundamentals footer, no menu (the r100 inquiry mode had fired on the tag but dropped every label: 2 empty crumbs, 3 panels; `_s30_r5_items.cjs`); built as `inquiry_tabs.side_tab_nav` + `flavours.fundamentals` (ContentConverter side-tab mode, `PanelsBuilder.inquiryPanels` sideTabMode, SkeletonBuilder flavour body / footer, `lesson_menu: none`), env `SIDETABNAV_OFF` · measured FRFUN06 10 / 10 pages 8 up / 2 down, +34.7pp-sum; FRFUN07 / 08 unchanged (page-navigation side tabs, plain fundamentals bodies) · **shipped INERT (`enabled: false`) — 10 pages / 1 module under the floor; enabling it is Chris's call** · corpus byte-identical 2555 / 2555; selftests GREEN; every gate as at r421 · plateau 0 of 3 · build 260619.93")
p2 = idx("- Standing facts: AppVersion 260619.92")
lines[p2] = lines[p2].replace("AppVersion 260619.92 (r421, session 30 Round 4, 21 Sept); before it 260619.91 (r420)", "AppVersion 260619.93 (r422 DECLINED-INERT, session 30 Round 5, 21 Sept); before it 260619.92 (r421) / 260619.91 (r420)")
assert "260619.93" in lines[p2]
io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("r422 finalise done; LOOP_STATE.md", os.path.getsize(p))
