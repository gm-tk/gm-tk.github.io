#!/usr/bin/env python3
"""ROUND 359 (loop session 19 Round 3 — the INQUIRY OVERVIEW MENU is the KB 06 §3.4 two-column form) — finalise: changelog,
AppVersion (260619.29 → 260619.30), CLAUDE.md §9 / §11 / §14, gate_baseline.json (skeleton + the two menulabels per-module
baselines), loop/README.md rows. Idempotent; LF via wr()."""
import io, os, json
ROOT = r"C:\Users\Gavin\TeKura\FINAL_MODULE_DATA"
PF = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)

CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)" + chr(10) + chr(10)
ENTRY = """## 2026-09-17 (round 359, build 260619.30) — THE INQUIRY OVERVIEW MENU IS THE KB 06 §3.4 TWO-COLUMN FORM: `col-md-6 paddingR` (the curriculum `<h4><span>Understand / Know / Do</span></h4>` block) + `col-md-6 paddingL` (the `<h5>` Learning-intentions / How-will-I-know sections), NO banner row — a new `inquiry_family` in `menu.two_col_li` (`MenuBuilder.#inquiryFamilyFor`: an Inquiry-template overview by the module index, the BLL parents excluded because their own gold IS the banner form; the archetype forced to two_col_li, the banner family off, the `two_col_inquiry` shell, a registry 'none' verdict → 'simplified' when the page has menu content) + the content-based overview partition now recognises a section label typed WITH A COLON (`Understand:`) inside that family; the autonomous loop's session-19 Round 3, the DIFF MINER's module-menu classes #36 / #46 / #28 / #54 — Chris's BLL110 finding, generalised to the families whose gold carries it; **FULL regeneration of all 416 (36 batches, all rc 0), 29 modules / 29 pages changed; skeleton SCAFFOLD 52.052 → 52.072 % (+0.021pp; 22 movers, 20 up, the 2 dips named), ≥50 1095 → 1096, ≥75 160 → 161, every other gate EXACT; ledger FULL (counter 0)**

### 1. WHAT CHANGED, IN ONE LINE

**Every ConnectED, Te ara Whakapuawa and EXPlore Inquiry overview shipped its module menu in the wrong shell — the BLL banner (a full-width `Learning Intentions` row, two `paddingR` columns, `h5>span` curriculum headings), a single `col-md-8` column, or no menu at all — where the KB's Inquiry form (06 §3.4) and 23 of the 29 golds carry two columns, `paddingR` | `paddingL`, with `h4>span` Understand / Know / Do on the left and `h5` sections on the right; they now do, and a writer's `Understand:` (with its colon) reaches the menu instead of the body.**

### 2. THE EVIDENCE (docx → human → Claude)

- **CEDT101 overview** — WT `[H1] Tirohanga Whānui | Overview` · `[H2] **Understand:**` + italic prose · `[H2] **Know:**` … · `[H2] **Do:**` … · `[H2] Whāinga Ako | Learning Intentions` · bullets · `[H2] Paearu Angitu | How will I know if I've learned it?` · bullets · Planning your time · Connections · `Tab 1 - Introduction` (no `[MODULE INTRODUCTION]`); gold `<div class="col-md-6 col-12 paddingR"><h4><span>Understand</span></h4><p>…</p><h4><span>Know</span></h4><p>…</p><h4><span>Do</span></h4><p>…</p></div><div class="col-md-6 col-12 paddingL"><h5>Learning Intentions</h5><ul>…</ul><h5>How will I know if I've learned it?</h5><ul>…`; Claude before: one `col-md-8` column holding the LI / SC sections while `<h3>Understand:</h3>` + the prose sat in the BODY (the label test needed a following space); after: the gold's form line for line.
- **TWHA901** — WT: LI, SC, Planning, Started, Connections, Assessment (NO Understand / Know / Do — the gold's left column is the developer's own, written from the curriculum); gold `paddingR[h4>span,ul,h4>span,ul,h4>span,p,ul] | paddingL[h5,p,ul,h5,p,ul,h5,p,p]`; Claude before: one `col-md-8` (no overview row in `Html_Convention_Registry` → 'flat'); after: `paddingR` (a Writers Note — the curriculum statements go here) | `paddingL` with the sections.
- **CEDO102** — gold `paddingR[h4>span,p ×3] | paddingL[h5,p,ul,h5,p,ul]`; Claude before: the BLL banner + `h5>span` (`ConnectED|4-6` two_col_li with `banner_h4_span:false` → the generic path = the BLL shell); after: the two columns, `h4>span` left. **CEDW101 / CEDW201 / CEDR204** — no menu at all before (a no-evidence `menu_type`); after: the two columns (the gold's `h3>span` banner row above them is a named miss).
- **The BLL parents are NOT in this class:** the census shows their own gold IS the banner form Claude already ships (BLL130 / 140 / 150 / 170 / 210 / 220 / 230 — 7 of 11; BLL110 / BLL120 carry `h4>span` and are the family's outliers, the r178 rule). Chris's BLL110 observations 2–5 (the `h4>span` headings, the `Ākonga will:` `<p>`, the paddingR-both-columns row, the `Overview` banner) are the gold of the OTHER Inquiry families, generalised here.

### 3. THE MEASUREMENT (before coding — `outputs/_measure_r359_inqmenu.py` → `_r359_inqmenu.{json,log}`; the in-memory probe `_r359_probe.cjs` over all 416, four iterations)

- **The census:** every paired overview's module-menu COLUMN SHAPE (the gate's tree), gold vs Claude — Inquiry 42 (Claude = gold on 3): gold `paddingR | paddingL` ×19 with `h4>span, h5` ×17; TWHA / TWHK 8 / 8, ConnectED 11 / 14 (4 with a banner row above), EXPlore 4 / 5; the BLL parents 7 / 11 the banner form. Standard 285 (= 117), Fundamentals 53 (= 17), Bilingual 16 (= 3) — the tabs / ENG-offset / fundamentals shells, untouched.
- **The probe (OFF = disk 2110 / 2110 every iteration once the toggle was renamed — `INQMENU_OFF` was already the r119 `inquiry_tab_ends_overview_menu` toggle, and the first OFF run had switched THAT off on ARFUN04 / EXPFUN06 / TWHA):** 29 → 45 → 33 → **29 changed pages / 29 modules** — the 20 ConnectED Inquiry overviews (7 of them the D10-6 revision briefs, out of the gate population), TWHA / TWHK 8, EXPFUN06 (its `Understand:` block now inside the Overview tab pane, as the gold's is). Removed on the way: ENGFUN02's empty shell (a 'none' verdict converted to 'simplified' with nothing to show — now stays 'none'), the general colon match's 12 Standard / tabs overviews (queued — see below), EXPFUN02–05 (their LI block sits in the body: a partition class of its own, queued).
- **§1b authority:** KB level 1 — 06 §3.4 (quoted above), 01B's overview heading & column rules (`h4>span` titles; Var 1 `col-md-6` ×2 `paddingR` / `paddingL`), D10-9 (f) (the `<h5>` labels stay — the gold's `<p>` lead-in is the recorded named override). Gold: TWHA 1.00, ConnectED 0.79, EXPlore 0.80.

### 4. THE MECHANISM (`outputs/_r359_splice.py` + `_r359b_splice.py` + two patches)

- **Data** `Emit_Templates.menu.two_col_li.inquiry_family` {enabled, env `INQFAMILY_OFF`, template_type "Inquiry" (source: `Module_Structure_Index.module_meta`), exclude_subjects ["BLL"], shell "two_col_inquiry", left_heading `<h4><span>{heading}</span></h4>`, right_heading `<h5>{heading}</h5>`, none_becomes "simplified", empty_left_note}; `menu.shells.two_col_inquiry`; `menu.overview_section_labels_colon` {enabled, env `INQFAMILY_OFF`, inquiry_only true}.
- **Engine** `MenuBuilder.#inquiryFamilyFor` (+ the public `inquiryFamilyFor`), `menuTypeFor` → `#menuTypeForBase` + the 'none' → none_becomes conversion (flagged on the page so an EMPTY conversion reverts to 'none'), `buildMenu` (the forced archetype, the banner family off, the family's heading templates at the three generic-path sites); `SkeletonBuilder` (the `two_col_inquiry` shell, no banner, the empty-left note); `ContentConverter.#partitionItems` (the colon label match, inside the family).

### 5. THE PROOF

- **FULL regeneration** (`_r359_fullship_par.sh`, 36 batches, all rc 0, 4 m 54 s): `_stalecheck.sh` 0 stale; `_content_manifest.py changed` = exactly the probe's 29 modules.
- **Gates (`_r359_gates.log`, every RESULT ✓, 0 ✗, pairs skipped 0):** **skeleton SCAFFOLD 52.0516 → 52.0723 % (+0.021pp; 22 movers — 20 up, pp-sum +40.4), ≥50 1095 → 1096 (TWHA906 crosses), ≥75 160 → 161 (CEDT301 80.81), ≥90 14 EXACT, RAW 36.748 → 36.763 %**; the two dips NAMED — EXPFUN06_0_0 27.10 → 25.16 (the `Understand:` block moved from the body into the Overview tab pane, where the gold's is — difflib re-aligns a 27 % page) and CEDK101_0_0 51.65 → 51.57 (the gold keeps a full-width `Understand` row above its two columns — one of the 4 ConnectED banner-row golds, named). compare_structure exact 11617 / EXTRA 175 / missing 617 EXACT; body_compare 182 EXACT; structural defect clean 98.9 % (26 occ / 23 pages) EXACT; tags 9557 / 9557; flipCard divergence 0, speechBubble ✓, modal ✓, MTK shell ✓, math ✓, menu labels ✓ (the gate set), dragAndDrop ✓, entry parity PASS.
- **The menu-label verifier over the whole changed family (`_r359_menulabels_family.log`, 22 modules, 33 labels):** defect 2 — CEDT104 and TWHA904, each a writer's own paragraph between a label and its list (`<h5>We are learning:</h5><p><b>Think like social scientists by:</b></p><ol>`): TWHA904's sequence is byte-identical in the `INQFAMILY_OFF` output, CEDT104's `<p>Knowledge context:</p>` was already there under `<h5>Know: Ākonga will know:</h5>` (the label was simply not recognisable before the `Know` heading split off) — PRE-EXISTING content shapes, recorded as the two modules' per-module baseline (the r348 mechanism), not chased.

**Ledger:** FULL regeneration of all 416, `_ship_ledger.py record-full --round 359` (counter 0) · selftests 16 GREEN, fast-loop baseline, content manifest, feature index refreshed (`_r359_postship.sh`) · `DIFF_QUEUE.md` re-mined on the r359 corpus · env `INQFAMILY_OFF` · **queued from this round (their own measurement owed):** the general colon label match for Standard / tabs overviews (ANZH104 / XGF9004's golds carry Understand / Know / Do in the menu; the five tabs overviews ART1006 / HIS1007 / MXDI101 / MXEO201 / MXFL103 per 01B's Know → Knowledge, Do → Practices; ENGR102 / HES1006 / HIS1002 / PES1005 / XDLS501 unpaired), EXPFUN02–05's LI / SC block landing in the body (the empty menu shell), the 4 ConnectED golds with a banner row above the two columns (CEDK101 `h4>span Understand`, CEDT404 / CEDW101 / CEDW201 `h3>span Tirohanga Whānui | Overview`), ENGFUN02 (a gold menu with an LI block Claude's WT does not carry).

"""
if "round 359, build 260619.30" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r359 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.30"' not in s:
    old = '\tstatic AppVersion = "260619.29";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, '\t// ROUND 359 (260619.30): the Inquiry overview menu is the KB 06 §3.4 two-column form — menu.two_col_li.inquiry_family (MenuBuilder.#inquiryFamilyFor; the two_col_inquiry shell; a colon label reaches the menu; env INQFAMILY_OFF); the diff miner\'s module-menu classes.\n\tstatic AppVersion = "260619.30";')
    wr(P, s); print("Config.js: 260619.30")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "ROUND 359 BASELINE" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 358 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 359 BASELINE (the Inquiry overview menu is the KB 06 §3.4 two-column form — the `inquiry_family`; FULL regeneration of all 416, ledger 0): SCAFFOLD mean 52.072% / >=50% 1096 / >=75% 161 / >=90% 14 / RAW 36.763% @ 1955 pairs, pairs skipped 0 — hold-or-improve; the two r359 dips named (EXPFUN06_0_0, CEDK101_0_0).** Previous — ROUND 358 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `REODETECT_OFF` | 358 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `INQFAMILY_OFF` | 359 | **THE INQUIRY OVERVIEW MENU IS THE KB 06 §3.4 TWO-COLUMN FORM.** `menu.two_col_li.inquiry_family`: an Inquiry-template overview (the module index's template_type; a module the index does not know keeps today's path) outside `exclude_subjects` (BLL — the parents' own gold is the banner form) forces the two_col_li archetype, disables the banner family and the banner, renders through the `two_col_inquiry` shell (`col-md-6 paddingR` | `col-md-6 paddingL`) with `h4>span` left headings and `h5` right headings, turns a registry 'none' menu verdict into 'simplified' when the page has menu content (an empty conversion reverts to 'none'), leaves a Writers Note in an empty left column (TWHA — the curriculum statements are the developer's), and — inside the family only (`menu.overview_section_labels_colon.inquiry_only`) — lets the content-based overview partition recognise a section label typed with a colon (`Understand:`). OFF = the r358 output on every page (the in-memory probe 2110 / 2110). NOT `INQMENU_OFF`, which is the r119 `inquiry_tab_ends_overview_menu` toggle. |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.29` (round 358"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.30` (round 359 — **the Inquiry overview menu is the KB 06 §3.4 two-column form** (`menu.two_col_li.inquiry_family` + the `two_col_inquiry` shell + the colon label match; `MenuBuilder.#inquiryFamilyFor`; env `INQFAMILY_OFF`); the autonomous loop's session-19 Round 3, the DIFF MINER's module-menu classes — Chris's BLL110 finding generalised to the ConnectED / TWHA / EXPlore families (the BLL parents' own gold is the banner form); FULL regeneration of all 416, 29 modules / 29 pages changed; skeleton 52.052 → 52.072 % (+0.021pp, ≥50 +1, ≥75 +1, two dips named), every other gate EXACT; ledger FULL, counter 0).\n"
             + OLD14)
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r359" not in d["skeleton"]:
    d["skeleton"]["mean_scaffold_pct"] = 52.072
    d["skeleton"]["pages_ge_50"] = 1096
    d["skeleton"]["pages_ge_75"] = 161
    d["skeleton"]["raw_mean_pct"] = 36.763
    d["skeleton"]["_note_r359"] = "Round 359: the Inquiry overview menu family — SCAFFOLD 52.0516 → 52.0723 (+0.021pp; 22 movers, 20 up; dips NAMED: EXPFUN06_0_0 — the Understand: block moved into the Overview tab pane where the gold's is, a 27 % page re-aligned; CEDK101_0_0 — the gold's banner row above the two columns), ≥50 1095 → 1096, ≥75 160 → 161, ≥90 14 EXACT, RAW 36.748 → 36.763. Hold-or-improve from here."
    pm = d["menulabels"].setdefault("per_module", {})
    pm["CEDT104"] = 1; pm["TWHA904"] = 1
    d["menulabels"]["_note_r359"] = "Round 359: the verifier over the whole changed Inquiry family (22 modules, 33 labels) — CEDT104 and TWHA904 each carry ONE pre-existing p-between (a writer's own paragraph between a label and its list: TWHA904 byte-identical under INQFAMILY_OFF; CEDT104's `<p>Knowledge context:</p>` already sat under `<h5>Know: Ākonga will know:</h5>`, unrecognised as a label until the Know heading split off). Recorded as their per-module baseline; ✗ only above 1."
    d["_meta"]["build"] = "260619.30"; d["_meta"]["round"] = 359
    d["_meta"]["_note_r359"] = "Round 359: the Inquiry overview menu family — skeleton +0.021pp (named dips), ≥50 +1, ≥75 +1, every other gate EXACT; FULL regeneration of all 416, 29 modules / 29 pages; ledger FULL (counter 0)."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r359")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_r359_finalise.py" not in s:
    A = "| `_measure_r358_titlepair.py`"
    assert s.count(A) == 1, "README anchor"
    ROWS = ("| `_measure_r359_inqmenu.py` / `_r359_inqmenu.{json,log}` / `_r359_resolve_all.cjs` / `_r359_resolved.json` / `_r359_splice.py` / `_r359b_splice.py` / `_r359_probe.cjs` / `_r359_probe_run.sh` / `_r359_probe_{off,on}_0*.log` / `_r359_fullship_par.sh` / `_r359_fullship_run.sh` / `_r359_fullship_regen.log` / `_r359_changed_modules.txt` / `_r359_gates.log` / `_r359_sk_full.log` / `_r359_sk_final.json` / `_r359_menulabels_family.log` / `_r359_postship.sh` / `_r359_selftests.log` / `_r359_fastloop_snapshot.log` / `_r359_manifest_snapshot.log` / `_r359_ledger.log` / `_r359_index.log` / `_r359_finalise.py` | `CONVERTER_V2/outputs/` | Session 19 Round 3 (engine r359 — the diff miner's module-menu classes: the Inquiry overview menu is the KB 06 §3.4 two-column form; the `inquiry_family` + the `two_col_inquiry` shell + the colon label match) — the overview-menu column-form census (every paired overview, gold vs Claude, per template / subject), the resolved menu values, the two anchored splices, the in-memory OFF / ON probe over all 416 (four iterations; the INQMENU_OFF collision found and the toggle renamed), the full regeneration, the gate suite, the fresh skeleton score, the family verifier, the post-ship housekeeping, the finalise |\n")
    s = s.replace(A, ROWS + A, 1)
    wr(P, s); print("README: r359 rows")
print("finalise done")
