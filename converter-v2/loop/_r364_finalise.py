#!/usr/bin/env python3
"""ROUND 364 (loop session 21 Round 1 — the id-carrying heading is the activity opener; the lead-media half scoped) — finalise:
changelog, AppVersion (260619.34 → 260619.35), CLAUDE.md §9 / §11 (IDHEAD_OFF + LEADMEDIA_OFF rows) / §14, gate_baseline.json,
loop/README.md. Idempotent; LF via wr()."""
import io, os, json
ROOT = r"C:\Users\Gavin\TeKura\FINAL_MODULE_DATA"
PF = os.path.join(ROOT, "pageforge-site", "converter-v2")


def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f:
        return f.read()


def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s)


CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)" + chr(10) + chr(10)
ENTRY = """## 2026-09-18 (round 364, build 260619.35) — THE ID-CARRYING HEADING IS THE ACTIVITY OPENER: `[H3] 1A Spot the place value` opens the gold's `<div class="activity interactive" number="1A"><h3>Spot the place value</h3>` box, the family's unnumbered `[interactive activity] …` span nests inside it, and a media item in an activity's lead renders as media (scoped to Standard + Fundamentals) — the r362 residue's other half (the autonomous loop's session 20 Round 8, reconciled and finished in session 21 Round 1)

### 1. WHAT CHANGED, IN ONE LINE

**The Mathematics MXDI / MXFU family (and SSFUN01, CEDT104, ART1003 / 1005, CEDO202, EXPFUN04 / 05, MXFL201 …) never types `[Activity 1A] Title`: it types a HEADING whose text starts with the activity id — `[H3] 1A Spot the place value` — followed by the activity's prose, its video and an UNNUMBERED `[interactive activity] drop down …` span with the widget's table. The gold opens the numbered box AT the heading (`<h3>` title, the id stripped) and keeps everything, widget included, inside it; Claude rendered the heading free (`<h4>1A Spot the place value</h4>`), opened an r217 standalone box at the widget and numbered it by sequence. Now `InteractiveScanner.#idHeadingOpeners` re-tags such a heading IN PLACE as the `[Activity 1A]` opener it is (the normaliser's own parse, the id-stripped title as its tail), the unclassified path nests the family's unnumbered `[interactive activity]` span in that box (scanner lookback + the converter's autoClose guard), the box that OWNS a widget bundle ships `activity interactive` exactly like the r217 box it replaces, and an `[image]` / `[video]` / `[audio]` item in an owned bundle's LEAD goes down the body's own `#element` path instead of rendering its link text as a `<p>` — the last half measured as its own class and SCOPED to the Standard + Fundamentals templates (Inquiry 0.50 = a tie).** 190 pages / 115 modules change; skeleton **+0.290pp** (52.347 → 52.637 %), ≥50 +15, ≥75 +3.

### 2. THE EVIDENCE (docx → human → Claude)

- **MXDI201 lesson 1, 1A** — WT `[H3] 1A Spot the place value` / `[body] …` / `[video] …` / `[interactive activity] drop down …` + a data table; gold `<div class="activity interactive" number="1A"><div class="row"><div class="col-12"><h3>Spot the place value</h3><p>…</p><div class="videoSection …">…</div>` then the widget, all inside `number="1A"`; Claude (r363) `<h4>1A Spot the place value</h4><p>…</p><p><a href="https://youtu.be/…">https://youtu.be/…</a></p>` free above `<div class="activity interactive" number="1A">` holding only the capture. Now: the box opens at the heading with `<h3>Spot the place value</h3>`, the prose, the `videoSection` embed and the capture inside it. Page 1_0 of MXDI201 → the module's pages moved 20.6 → 59.1 (8_0), 22.4 → 62.7 (10_0), 37.7 → 68.2 (3_0).
- **MXFU202 lesson 9, 9A–9F** — WT `[H3] 9A Cycling successes` … `[H3] 9F Olympic village divided`; gold six boxes `activity interactive` 9A–9E + `activity alertPadding` 9F, each `<h3>` first; Claude (r363) each `<h4>9A Cycling successes</h4>` free, a sequence-numbered widget box beneath. Now: six id-numbered boxes with the `<h3>` first; 9A–9E `activity interactive` (the owning-a-widget rule), 9F plain.
- **The lead-media half (ANZH105 lesson 4, HIS1002, ENGS102 …)** — WT `[Activity 4A] Title` / `[image] iStock-1275747565` / prose / the widget; gold `<h3>Title</h3><img class="img-fluid" …>`; Claude (r363) `<p><a href="https://www.istockphoto.com/…">https://www.istockphoto.com/…</a></p>` — the image tag's link text as a paragraph inside the box. Now: the `<img>` placeholder the body loop has always shipped for an `[image]` tag.
- **The counter-examples (recorded, r178):** SSOG301 (`[H3] 1B …` are section titles — gold boxes 0.12) and EXPFUN03's repeated `[H2] 1A Designing your own Learning Goals` (0 / 6) stay as they are (both below the floor in their own module; the rule is corpus-wide and their pages are the accepted cost). MXDB102 lesson 1's `[H3] 2D shapes` / `3D printing` are dimension words: `title_start_pattern` (a title must start with a capital, a digit, a quote or a bracket) keeps them headings — session 20's probe had opened a phantom box `2D` titled `shapes` there.

### 3. THE MEASUREMENT (before coding — `outputs/_measure_r364_idheading.py` → `_r364_idheading.{json,log}` (session 20); `_measure_r364_leadmedia.py` → `_r364_leadmedia.json` (session 21))

- **The class:** 432 id-carrying headings / 33 modules (h3 333, h2 64, h4 24, h5 11; a widget ahead 340). The gold builds `<div class="activity …" number="1A">` opening with `<h3>Title</h3>` on **0.88** (MXFU201 1.00, MXDI201 0.99, MXFU202 0.93, MXDI202 0.76, SSFUN01 / CEDT104 / ART1003 1.00); Claude had a box for 0.37 (the r217 standalone box, numbered by sequence, the heading free above it as h4 / p) and opened NONE at the heading. Standard only (the family's number lives in a table row on Bilingual pages — reoMode excluded). Authority: KB 01F (the `<h3>` activity heading inside the activity) — §1b level 1 — and the family's own gold.
- **The lead-media half, measured as its own class in session 21** (over the 146 pages ONLY that half changes, boxes keyed by `number` on both sides): 167 boxes gained a media element; of the 149 the gold also numbers, the gold carries media in the same box on **0.85 — Standard 0.92 (n 110), Fundamentals 0.84 (19), Inquiry 0.50 (20; the BLL golds drop the stock image: a tie)** → SCOPED to Standard + Fundamentals by `lead_media_exclude_templates: ["Inquiry"]` (matched against `Module_Structure_Index` `module_meta.template_type`), with its own env `LEADMEDIA_OFF` inside the round's `IDHEAD_OFF`. Authority: the body's existing media rule (KB 01E) extended to the activity lead.
- **Attribution (the in-memory probe with each data key switched off in turn, `_r364s21_changed_pages_{NOMEDIA,NONEST}.txt`):** sub-rules 1 + 2 (the opener + the nesting) = 53 pages / 10 modules; the lead-media half alone = a further 146 pages / 113 modules (→ 137 pages / 105 modules once scoped); the nesting adds no page of its own (every one is inside the opener's pages).

### 4. THE MECHANISM (ENGINE + data — one block `Interactive_Boundary_ChildTag_Bank._meta.opener_rule.id_heading_opener`, env `IDHEAD_OFF` = the whole round OFF; `LEADMEDIA_OFF` = the lead-media half only)

- **`InteractiveScanner.#idHeadingOpeners`** (called first in `ScanPage`): an unconsumed ELEMENT item whose primary tag is in `heading_tags` (h2–h5) and whose tail matches `id_pattern` (`\\d{1,2}[A-Z]` + a title of ≥ `min_title_chars` that passes `title_start_pattern`; `exclude_ids` the manual escape) is re-tagged in place — `it.text = "[Activity 1A]"`, `it.parse = normaliser.Parse(...)`, `it.blackAfter = title`, `it._idHeading = {level, raw, tail}` — unless a typed `[Activity]` opener with the SAME id sits within `same_id_window` items (both forms in one WT) or the page is reoMode. Every downstream rule (the owner lookback, the unclassified path, the numbering, `ActivitiesBuilder`'s box) then sees exactly a typed opener.
- **`unnumbered_nests_in_numbered`** — in the scanner's unclassified-activity branch an UNNUMBERED `activity` CONTAINER_OPEN looks back (black runs, ELEMENT / opener tags; stop at a consumed item or anything else) for a NUMBERED opener carrying `_idHeading`; found → the bundle is OWNED by it (the r362 owner form: opener → `activityOwner`, the items between → `activityLeadItems`, the span + its table → members, `_nestedInNumbered`). The converter's matching guard (before `autoClose`) turns a stray unnumbered `[interactive activity] label` opener inside an open `_idHeading` box into a Writers Note in that box instead of a second box. Scoped to id-heading boxes: a typed `[Activity N]` + unnumbered `[activity]` pair keeps today's two-box form (HPFUN101 1A measured worse nested).
- **`force_interactive`** (session 21) — `forceInt` in the bundle-owner path now also fires for `actOwner._idHeading`: an id-heading box that OWNS a widget bundle is `activity interactive`, like the r217 synthetic box it replaces; the widget-less heading box never comes through that path and stays plain. Without it the probe lost 11–12pp on MXFU202_9_0 / _6_0 — the skeleton signature carries the class.
- **`lead_media_tags`** (+ `lead_media_env`, `lead_media_exclude_templates`) — in the converter's owned-lead rendering a lead item whose primary tag is `image` / `video` / `audio` is flushed through `#element` (the body loop's own path) instead of `addLead(text)`.
- `ActivitiesBuilder.activityOpen` records `idHeading: !!it._idHeading` on the stack frame for the converter's guard. Data over code: every threshold, tag list and pattern is in the block; `IDHEAD_OFF=1` = byte-identical.

### 5. THE PROOF

- **A/B (the in-memory probe `_r364_probe.cjs`, 4 shards under WSL, `_r364s21b_probe_{OFF,ON}_[0-3].log`):** `IDHEAD_OFF=1` = disk **2110 / 2110** byte-identical; ON = **190 pages / 115 modules** (`_r364s21b_changed_{pages,modules}.txt`). Session 20's own probe logs (`_r364_probe_*`, `_r364_onsave_*`, `_r364_on/`) pre-date the `title_start_pattern` guard and are superseded.
- **FULL regeneration** (`_r364_fullship_par.sh`, 36 batches, all rc 0, 4 m 53 s): `_content_manifest.py diff` **190 pages / 115 modules changed, 0 added / 0 removed** = the probe's set; every regenerated page byte-identical to the probe's ON page (190 / 190); `_stalecheck.sh` 0 stale; `fresh --affected` (the 115) → 0 truly stale, the other 298 byte-identical to the manifest.
- **Gates (`_r364_gates.log`, rc 0, pairs skipped 0):** skeleton SCAFFOLD mean **52.347 → 52.637 % (+0.290pp)**, median 52.6 → 53.0, **≥50 1103 → 1118 (+15), ≥75 170 → 173 (+3), ≥90 15 EXACT**, ≥95 2 EXACT, RAW 37.021 → 37.162 %; **171 movers — 118 up / 53 down** (`_r364_movers.log`, the gate's own `--json` states `_r363_sk_final.json` → `_r364_sk_final.json`). compare_structure: exact wrapper chain 11645 → 11631 (−14) = the text-matched pool 13709 → 13695 (−14; the id-stripped titles and the dropped link paragraphs no longer text-match — the r344 population precedent), 84.9 % EXACT, EXTRA 175 / MISSING 617 / row-wrap 23 / diff-order 1052 / other 197 all EXACT. body_compare: over-capture 41 → 42 (MXDI202_11_0 — its skeleton 29.7 → 51.4), EMPTY container 151 → 152 (MXDI202_6_0 + _3_0 gained a flag, PHE1005 lost one), runaway 4 EXACT, any 195 → 197 — NAMED. Structural defect audit EXACT (leak 26 occ / 23 pages), tags 9557 / 9557, every widget verifier (flipCard, speechBubble, accordion, tabs, clickDrop, dropDown, modal, mtkQuiz, hintSlider, image carousel, carousel, intextract, math, menu-labels, dragAndDrop) line-for-line IDENTICAL to r363.
- **The dips, named (53; the largest):** MXFUN01_6_2 23.4 → 11.3 (two `[image]` tags in an activity lead now ship the `<img>` placeholder the body rule has always shipped — the gold dropped the generic `image.jpg`); MXFU202_9_0 35.9 → 28.6, _6_0 38.2 → 35.5, _1_0 31.9 → 29.5 and MXFU201_2_0 33.8 → 32.4 (the RESIDUE below); MXFL204_5_1 44.1 → 39.7 (the box is now numbered `3F` from the heading where the gold renumbered the page's boxes 6A–6C); BLL163_1_1 / BLL135_1_1 / HES1003_1_0 / SCPH301_5_0 / MXDI101_1_7 / MXFL103_1_5 (−1.2 to −2.2: a lead image the gold drops or places outside the box). The largest gains: MXFU201_5_0 25.3 → 69.1, MXDI201_10_0 22.4 → 62.7, MXDI201_8_0 20.6 → 59.1, MXDI201_3_0 37.7 → 68.2, MXDI202_9_0 42.5 → 69.7, MXFU201_7_0 30.3 → 56.4.
- **RESIDUE recorded, not chased:** the SECOND widget of an id-heading activity (MXFU202 9B's second table → an r217 box sequence-numbered `9C` beside the heading's own 9C): the nesting lookback stops at the first bundle's consumed members; the gold nests both. 18 pages / 4 modules (MXDI201, MXDI202, MXFU201, MXFU202) gain a duplicate box number this way (35 pages already carried one on disk) — below the 10-module floor; a follow-up class if it grows.
- Ledger: FULL (counter 0). AppVersion 260619.35; CLAUDE.md §9 / §11 / §14; `gate_baseline.json` (skeleton 52.637 / 1118 / 173 / 15; RAW 37.162; cs exact 11631; body_compare 197 / 42 / 4 / 152 NAMED); loop README; `_MIGRATION/CHECKSUMS__engine.txt` refreshed (`.pre-r364.bak` kept).

"""
if "round 364, build 260619.35" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r364 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.35"' not in s:
    old = '\tstatic AppVersion = "260619.34";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, '\t// ROUND 364 (260619.35): the id-carrying heading is the activity opener — `[H3] 1A Title` opens the gold\'s numbered box with the <h3> title, the family\'s unnumbered [interactive activity] span nests inside it (activity interactive when it owns a widget), and a media item in an activity\'s lead renders as media (Standard + Fundamentals; data BoundaryBank._meta.opener_rule.id_heading_opener; env IDHEAD_OFF / LEADMEDIA_OFF). The autonomous loop\'s session 20 Round 8, finished in session 21 Round 1.\n\tstatic AppVersion = "260619.35";')
    wr(P, s); print("Config.js: 260619.35")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "ROUND 364 BASELINE" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 363 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 364 BASELINE (the id-carrying heading is the activity opener + the lead-media half scoped to Standard / Fundamentals — 115 modules; FULL regeneration of all 416, ledger 0): SCAFFOLD mean 52.637% / >=50% 1118 / >=75% 173 / >=90% 15 / RAW 37.162% @ 1956 pairs, pairs skipped 0 — hold-or-improve; 171 movers (118 up, 53 down — the dips named in the r364 changelog: a lead image the gold drops, the second-widget residue, a heading-numbered box the gold renumbered).** Previous — ROUND 363 BASELINE"
             + OLD9[len("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 363 BASELINE"):])
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `UNCLASSHEAD_OFF` | 363 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `IDHEAD_OFF` | 364 | **THE ID-CARRYING HEADING IS THE ACTIVITY OPENER** (the autonomous loop's session 20 Round 8, finished in session 21 Round 1 — the r362 residue's other half; KB 01F). The MXDI / MXFU family types `[H3] 1A Spot the place value` instead of `[Activity 1A] Title`; the gold opens the numbered box at the heading with the `<h3>` title (0.88 of 432 headings / 33 modules). `InteractiveScanner.#idHeadingOpeners` re-tags the heading in place as the `[Activity 1A]` opener (guards: `heading_tags`, `id_pattern`, `min_title_chars`, `title_start_pattern` — `2D shapes` is not an id —, `same_id_window`, never on reoMode pages); `unnumbered_nests_in_numbered` nests the family's unnumbered `[interactive activity]` span in that box; `force_interactive` makes the box that owns a widget `activity interactive` like the r217 box it replaces. Data `BoundaryBank._meta.opener_rule.id_heading_opener`. OFF = byte-identical (2110 / 2110). 190 pages / 115 modules (with the lead-media half); skeleton +0.290pp. |\n"
             "| `LEADMEDIA_OFF` | 364 | **A MEDIA ITEM IN AN ACTIVITY'S LEAD RENDERS AS MEDIA** (the r364 block's `lead_media_tags`; its own env inside `IDHEAD_OFF`). An owned bundle's lead used to render an `[image]` / `[video]` / `[audio]` item's tail as a `<p>` of link text; it now goes down the body loop's own `#element` path (the `<img>` placeholder / the `videoSection` embed). Measured as its own class in session 21 (`_measure_r364_leadmedia.py`): the gold carries the media in the same-numbered box on 0.85 — Standard 0.92, Fundamentals 0.84, Inquiry 0.50 (a tie) — so `lead_media_exclude_templates: [\"Inquiry\"]` (matched against `module_meta.template_type`). 137 pages / 105 modules of the round's 190. |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.34` (round 363"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.35` (round 364 — **the id-carrying heading is the activity opener** (`[H3] 1A Title` → the gold's numbered box opening with the `<h3>` title; the family's unnumbered `[interactive activity]` span nests inside it; the box that owns a widget is `activity interactive`; + a media item in an activity's lead renders as media, scoped to Standard / Fundamentals — data `BoundaryBank._meta.opener_rule.id_heading_opener`, env `IDHEAD_OFF` / `LEADMEDIA_OFF`); the autonomous loop's session-20 Round 8 finished in session-21 Round 1; 190 pages / 115 modules; FULL regeneration; skeleton 52.347 → 52.637 %, ≥50 1118, ≥75 173, ≥90 15, RAW 37.162 %, compare_structure exact 11631 (= the matched pool −14), body_compare 197 / 42 / 4 / 152 named). Previous: `260619.34` (round 363"
             + OLD14[len("- **Build:** `260619.34` (round 363"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r364" not in d["skeleton"]:
    d["skeleton"]["mean_scaffold_pct"] = 52.637
    d["skeleton"]["raw_mean_pct"] = 37.162
    d["skeleton"]["pages_ge_50"] = 1118
    d["skeleton"]["pages_ge_75"] = 173
    d["skeleton"]["pages_ge_90"] = 15
    d["skeleton"]["pairs"] = 1956
    d["skeleton"]["_note_r364"] = "Round 364: the id-carrying heading is the activity opener (+ the lead-media half scoped to Standard / Fundamentals) — SCAFFOLD 52.3470 → 52.6374 (+0.290pp; 171 movers, 118 up / 53 down, the dips named in the changelog — a lead image the gold drops, the second-widget residue, a heading-numbered box the gold renumbered), ≥50 1103 → 1118, ≥75 170 → 173, ≥90 15 EXACT, RAW 37.021 → 37.162; FULL regeneration of all 416 (190 pages / 115 modules)."
    cs = d["compare_structure"]
    cs["exact_chain"] = 11631
    cs["_note_r364"] = "Round 364: exact wrapper chain 11645 → 11631 (−14) = the text-matched pool 13709 → 13695 (−14): the id-stripped titles and the dropped link paragraphs no longer text-match (the r344 population precedent, 84.9% EXACT); EXTRA 175 / missing 617 / row-wrap 23 EXACT. Hold-or-improve from 11631."
    bc = d["body_compare"]
    bc["any_breakdown"] = 197; bc["over_capture"] = 42; bc["runaway"] = 4; bc["empty_container"] = 152
    bc["_note_r364"] = "Round 364: over_capture 41 → 42 (MXDI202_11_0 — its skeleton 29.7 → 51.4), EMPTY 151 → 152 (MXDI202_6_0 + _3_0 gained a flag, PHE1005 lost one), any_breakdown 195 → 197 — NAMED; runaway 4 EXACT. Hold-or-improve from 197 / 42 / 4 / 152."
    d["_meta"]["build"] = "260619.35"; d["_meta"]["round"] = 364; d["_meta"]["date"] = "2026-09-18"
    d["_meta"]["_note_r364"] = "Round 364: the id-carrying heading is the activity opener + the lead-media half — skeleton +0.290pp (≥50 +15, ≥75 +3, ≥90 EXACT), compare_structure exact −14 = the matched pool −14, body_compare +1 / +1 named; FULL regeneration of all 416, 115 modules / 190 pages; ledger FULL (counter 0)."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r364")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_r364_finalise.py" not in s:
    A = "| `_measure_r363_lessonmenu.py`"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_measure_r364_idheading.py` / `_r364_idheading.{json,log}` / `_r364_absent.py` / `_r364_items.cjs` / `_r364b_items.cjs` / `_r364_probe.cjs` / `_r364_probe_run.sh` / `_r364_shard[0-3].txt` / "
           "`_r364_probe_{OFF,ON}_[0-3].log` + `_r364_onsave_0[0-3].log` + `_r364_on/` + `_r364_pagescore.py` + `_r364_onscore.json` + `_r364_changed_{modules,lines}.txt` + `_r364_chg_0[0-3]` (session 20 — SUPERSEDED: they pre-date the `title_start_pattern` guard) / "
           "`_r364s21_probe_{OFF,ON,NOMEDIA,NONEST}_[0-3].log` / `_r364s21_changed_{modules,pages}.txt` / `_r364s21_changed_pages_{NOMEDIA,NONEST}.txt` / `_r364_on_s21/` / `_r364s21_pagescore.py` / `_r364s21_onscore.json` / "
           "`_measure_r364_leadmedia.py` / `_r364_leadmedia.json` / `_r364_bank_backup.json` / "
           "`_r364s21b_probe_{OFF,ON}_[0-3].log` / `_r364s21b_changed_{modules,pages}.txt` / `_r364_on_s21b/` (the probe's ON pages of the 115 changed modules, byte-identical to the shipped disk) / `_r364s21b_pagescore.py` / `_r364s21b_onscore.json` / "
           "`_r364_fullship_run.sh` / `_r364_fullship_par.sh` / `_r364_batch_*.{sh,log}` / `_r364_fullship_regen.log` / `_r364_manifest_diff.log` / `_r364_stalecheck.log` / `_r364_fresh.log` / `_r364_gates.log` / `_r364_sk_full.log` / `_r364_sk_final.json` / `_r364_movers.log` / `_r364_finalise.py` / `_r364_postship.sh` / `_r364_selftests.log` / `_r364_fastloop_snapshot.log` / `_r364_manifest_snapshot.log` / `_r364_ledger.log` / `_r364_index.log` / `_r364_miner.log` | "
           + loc + " | Session 21 Round 1 (engine r364, build 260619.35) — the id-carrying heading is the activity opener (+ the nesting, `force_interactive`, and the lead-media half measured as its own class and scoped to Standard / Fundamentals): the r364 measurement (session 20), the two attribution probe runs and the gold-consensus measure (session 21), the FULL regeneration, gates, movers, finalise and post-ship logs. |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r364 rows")
print("finalise done")
