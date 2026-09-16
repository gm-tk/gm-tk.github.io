#!/usr/bin/env python3
"""ROUND 344 (loop session 12 Round 1 — Chris's D10-1, KB constraint 47 in full) — finalise: changelog, AppVersion
(260619.14 → 260619.15), CLAUDE.md §9/§11/§14, CONVERTER_V2_GUIDE, gate_baseline.json, KB status rows, LOOP_STATE.md
(what shipped + position + round log). Idempotent; LF kept (io.open newline=""); never json.dumps a data file."""
import io, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)

SK_B, SK_A, RAW_B, RAW_A = "51.265", "51.281", "35.394", "35.407"
SK_B4, SK_A4 = "51.2646", "51.2809"
GE50, GE75, GE90, PAIRS = 1073, 198, 15, 1955
CS_B, CS_A, EX, MI = 11469, 11461, 175, 607
POOL_B, POOL_A = 13516, 13508
CLEAN = "2080/2103 = 98.91%"
PCT, CEIL = "55.8", "91.9"
AFF = "CEDO105 CEDT207 ENG1005 ENGI102 ENGI202 ENGR202 HES1006 HIS1001 HIS1006 MXEO202 MXFU201 MXFU302 PES1002 PES1005 PES1008 SCCH301 SCPH301 SSOG101 SSOG301 XDLS906 XLP02"
MOVERS = ("33 moved — 21 up / 12 down, every mover in the affected set, pp-sum +31.82 scaffold AND +24.49 RAW; the gains: ENGI102_10_0 +9.87, SSOG101_3_0 +9.13 (42.77 → 51.90), PES1002_8_0 +7.65 (43.06 → 50.70, crosses ≥50), PES1002_2_0 +5.17, PES1002_7_0 +4.18, PES1002_9_0 +3.76, PES1002_3_0 +3.40, HES1006_3_0 +2.54, PES1002_10_0 / _6_0 +1.89 / +1.79, HIS1001_7_0 +1.79 …; the 12 dips are NAMED and of three kinds: (a) the D10-1 named overrides — the gold KEEPS the repeat where its header carries the MODULE title and the body h3 is the lesson's name: SCCH301_5_0 −1.26 / _3_0 −0.64 / _6_0 −0.57 / _2_0 −0.53 / _7_0 −0.50, SCPH301_8_0 −1.12 (50.37 → 49.25, the ≥50 down-crosser that PES1002_8_0's up-crossing balances) / _3_0 −0.64 / _4_0 −0.63, MXEO202_3_0 −1.14; (b) the scorer's alignment artefact on a strictly closer element set — PES1002_4_0 −10.31 and MXFU302_1_0 −6.17, both gold-ABSENT pages whose remaining headings re-rank h4 → h3 = the gold's own h3s (`_r344_posfree.log`: position-free skeleton-line overlap RISES 47 → 49 and 63 → 64, heading lines 13 → 12 = the gold's 12); (c) ENGI202_6_0 −0.95 = a coincidental positional match lost (the dropped `Celebration of your learning` h3 had matched one of the gold's 22 heading lines by position; the gold does not carry the text)")

# ---------------------------------------------------------------- 1. BUILD_CHANGELOG.md
CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)" + chr(10) + chr(10)
ENTRY = f"""## 2026-09-16 (round 344, build 260619.15) — THE OPENING DUPLICATE BODY HEADING IS DROPPED IN FULL — KB constraint 47 (Chris's decision D10-1, Option A: "the lesson number is isolated to the top-right corner and the lesson title is kept as the h1") + the header title's stray markdown markers (c79 hygiene); the autonomous loop's session-12 Round 1; SCOPED regeneration of the 21 affected modules (48 pages) — scoped ship #1 since the r342 full; every protected gate HELD-or-IMPROVED, the −8 on compare_structure exact = the matched pool −8, named

### 1. WHAT CHANGED, IN ONE LINE

**On a lesson page the FIRST RENDERED free-body heading whose text equals the header title — once case, punctuation and a `Lesson N` label are ignored — is dropped (the header already shows the title; the lesson NUMBER stays in the `#module-code` chip), a heading inside an activity box is never a candidate, and a lesson's header title never carries a writer's `*` / `**` marker.** The gold's SSOG101_3.0 / MXFU302_1.0 shape: `<h1><span>Police Officers</span></h1>` … `<div id="body">` … `<p>The police are like community helpers …` with no repeated heading; Claude shipped `<h1><span>* Police Officers</span></h1>` … `<h3>Lesson 3: Police Officers</h3>`.

### 2. THE MEASUREMENT (before any code — `outputs/_measure_r344_c47.py`, the first FREE-BODY heading, activity-box titles and later section repeats excluded)

- The session-11 PICK had counted 40 target pages with the r320 tool, which compares EVERY body heading by text. Re-measured on the first free-body heading only (a heading under an `activity` / widget / hand-off container is not free — ENGI101's "Being Frank" is the activity's own title, D10-1 KEEP; a repeated section title deeper in the page is not the OPENING heading): **31 target pages / 15 modules** in the scored population (Standard 29 / Inquiry 2; Bilingual 2 EXCLUDED — KB 07B governs the MTK section heading), the gold DROPS the heading on **20** (the gain) and KEEPS it on **11** (SCCH301 ×5 / SCPH301 ×3 / HIS1001 / MXEO202 / XDLS903 — the NAMED overrides D10-1 pre-decides). The comparison LADDER the seam walks: exact (the r75 compare already matched — the heading survived only because an EARLIER heading spent the slot) 16, lesson-prefix 11, punct 4.
- The three live traces of session 11 named the mechanisms: **MXEO202_3_0** — `[H2] *Lesson 3 Triangles*` is CONSUMED by the de-dup and sets `#firstBodyHeadingSeen`, so `[H3] Triangles` — the real opening heading — is never tested (the mechanism behind most of the 31); **HIS1001_7_0** — the title's curly quotes `“pacific proving grounds”` vs the heading's none (the punctuation fold); **ENGI101_1_1** — `[Activity 2A] *Being Frank*` is the activity's own title rendered by `activityOpen` (KEEP; the measurement tool's `inbox` test fixed first, as the trace required). The PICK's "PES1002 needs the r316 pair's English half" was a misreading: PES1002's title `Fossil Fuels** *Te reo* Māori translation needed` is the writer's trailing NOTE with leaked `**` markers, and the punctuation fold closes it (the note itself stays — recorded, under the floor).
- **The sibling** (D10-1's second half): **23 header titles / 8 modules** still carried a markdown marker — MXFU302 `**Statistics and Sports**`, PES1008 `*Heat Capacity Calculations*` ×5 (+3 unpaired pages), XDLS906, SSOG101 `* Police Officers` ×2, SSOG301, MXFU201 `**3**` / `**5**` / `**8. …**`, PES1002 ×9; the gold ships **0 of 2385** header titles with a marker.

### 3. THE SEAM (data `body_region.lesson_title_dedup.c47` + `.title_markers`; env `DEDUPC47_OFF` + `TITLEMARK_OFF`)

- `ContentConverter` heading branch (`#element`): the c47 gate is computed BEFORE the first-heading slot test (lesson pages only — `#pageIsLesson`, set beside `#pageLessonTitle`; the overview keeps the r80 exact de-dup; `exclude_body_class` `reoTranslate` fences the Bilingual template). **`first_rendered_heading`** — the slot is spent only when a heading RENDERS (after the compare), so a consumed title repeat never hides the real opening heading; **`ignore_punctuation`** — the compare key is `Utils.Fold(_stripLessonPfx(s))` with every non-letter / non-digit removed (the r75 key removes whitespace only); **`skip_inside_activity`** — a heading with an open `activity` frame on the container stack is never the candidate and never spends the slot. With the toggle OFF every line is the r75 / r324 path byte-for-byte.
- `PageSplitter` title post-pass (before the r324 label / bare-number tests): a `page.pageTitle` carrying a `*` loses every marker and collapses whitespace; a title left with no letter or digit (XLP02_4_0's `*:`) is emptied so the module-title fallback applies. Fires only on a title with a marker — the blast radius is the measured class. `**3**` → the bare number `3` → the r324 fill takes the lesson's own name from its first heading (MXFU201_3_0 `Convert 12 hour to 24-hour time` = the gold's title verbatim).

### 4. THE PROOF

- In-memory probe over ALL 416 modules (`_r344_probe.cjs` = the r342 probe; 4 shards): **BOTH-OFF = disk 2110 / 2110** (`_r344_probe_off_0*.log`); **ON = 48 pages / 21 modules changed, 0 added / 0 removed** (`_r344_probe_on_0*.log`, `_r344_changed_pages.txt`, `_affected_r344.txt`) — the other 395 modules byte-identical in memory = the §0b whole-family proof (every module whose first heading the r75 de-dup already consumes, and every marker-free title, is proven untouched). SCOPED regeneration of the 21 (`_r344_regen.log`, 4 batches, all rc 0); `_content_manifest.py fresh --affected` **OK — 0 truly stale**; `_content_manifest.py diff` = **exactly the 48 pages / 21 modules, 0 added / 0 removed** (containment + completeness). `_stalecheck.sh`'s 392 "stale" = the scoped-regen mtime false alarm (§10a), content-proven false.
- Three modules outside the measured set changed for the same reasons: CEDT207_4_0 / ENG1005_2_0 (unpaired pages — a heading-only `row > col` dropped whole with its heading), PES1005_4_0 (`** **Te whānau mārama` cleaned, which unlocks the `Lesson 3:` de-dup).
- **The round's verifier (`_measure_r344_c47.py` re-run): c47 targets 31 → 1** (XDLS903_1_0's `<h4>Poi</h4>` is an IMAGE-CAPTION render, not a writer heading — the gold keeps it; residue, not c47); **marker titles 23 → 0 corpus-wide** (0 of all 2110 pages).
- **Skeleton (PRIMARY): SCAFFOLD mean {SK_B}% → {SK_A}% (+0.016pp; {SK_B4} → {SK_A4}) / ≥50% {GE50} / ≥75% {GE75} / ≥90% {GE90} EXACT / skipped 0 @ {PAIRS}; RAW {RAW_B}% → {RAW_A}%** (state `outputs/_r344_sk_final.json`, FRESH; movers `_r344_sk_movers.log`) = **{PCT}% of achievable** (ceiling {CEIL}%). {MOVERS}.
- **compare_structure exact {CS_B} → {CS_A} (−8) = the text-matched pool {POOL_B} → {POOL_A} (−8) to the element** — the dropped gold-KEPT headings leave the matched pool (the r57 / r147 relocation class; no element's chain got worse); EXTRA {EX} / missing {MI} / diff-order 1040 / row-wrap 23 / other 202 EXACT. **body 180 EXACT; clean {CLEAN} / leak 26/23 EXACT (line-for-line); tags 9557/9557; flipCard TOTAL 61 divergence 0; speechBubble defect 4 = the r341 standing baseline; modal / mtkQuiz defect 0; entry-parity PASS; index-sync OK; 13 selftests GREEN (`_r344_selftests.log`); accordion over the 21: 68 panels / 9 modules, every panel matches the human.** Fast-loop `_fastloop_diff.py` on the 21 reproduces the suite; `--commit --accept-named "compare_structure exact chain"` (the r289 override, decomposed above); baseline PATCHED + manifest refreshed; `_ship_ledger.py record-scoped --round 344` (scoped #1 since the r342 full, 7 of headroom); feature index `--rehtml` + `--merge`, selftest GREEN.

### 5. NAMED, RECORDED, NOT CHASED

- The 11 gold-kept repeats (SCCH301 / SCPH301 / HIS1001 / MXEO202 — their golds show the MODULE title in the header, so the body h3 is the lesson's name there; c79 says the lesson's own title is the h1) — the KB-over-gold override D10-1 pre-decided.
- The writer's trailing note in PES1002's titles (`… Te reo Māori translation needed`, 9 pages / 1 module) and MXFU201_8's `8.` number prefix (1 page) — title-hygiene classes under the 20-page floor.
- XDLS903_1_0's image-caption `<h4>Poi</h4>` (the gold's own form); the Bilingual TRR111 ×2 section-box headings (07B).
- The re-leveller's rank rule moving the remaining headings one level up once the title repeat goes (SSOG101 h4 → h3 against a gold that mixes h3 / h4 on the same page) — the r324 named class.

**Ledger:** SCOPED ship #1 since the r342 full (7 of headroom) · data `body_region.lesson_title_dedup.c47` {{first_rendered_heading, ignore_punctuation, skip_inside_activity, exclude_body_class}} + `.title_markers` · env `DEDUPC47_OFF` / `TITLEMARK_OFF` · tools `outputs/_measure_r344_c47.py` (+ `_r344_c47.json`, `_r344_c47_pre.json`, `_r344_c47_post.log`), `_r344_splice.py`, `_r344_probe.cjs` + `_r344_probe_{{off,on}}_0*.log`, `_r344_changed_pages.txt`, `_affected_r344.txt`, `_r344_regen.log`, `_r344_gates.log`, `_r344_sk_final.json` / `_r344_sk_full.log`, `_r344_sk_movers.log`, `_r344_posfree.log`, `_r344_fastloop.log` / `_r344_fastloop_commit.log`, `_r344_selftests.log`, `_r344_feature_index.log`, `_r344_finalise.py` · AppVersion 260619.15.

"""
if "round 344, build 260619.15" not in s:
    assert s.startswith(head); s = head + ENTRY + s[len(head):]; wr(CL, s); print("changelog prepended")

# ---------------------------------------------------------------- 2. Config.js
CF = os.path.join(PF, "app", "js", "Config.js"); c = rd(CF)
OLD = '\tstatic AppVersion = "260619.14";' + chr(10)
NEW = ('\t// ROUND 344 (2026-09-16, build 260619.15): the opening duplicate body heading is dropped in full — KB constraint 47' + chr(10) +
       '\t// (Chris\'s D10-1): the first RENDERED free-body heading equal to the title once case, punctuation and a Lesson N label' + chr(10) +
       '\t// are ignored (a consumed heading no longer spends the slot; activity-box titles never candidates; Bilingual excluded by' + chr(10) +
       '\t// 07B) + the header title\'s stray markdown markers stripped; scoped regeneration of 21 modules / 48 pages.' + chr(10) +
       '\tstatic AppVersion = "260619.15";' + chr(10))
if '"260619.15"' not in c:
    assert c.count(OLD) == 1; c = c.replace(OLD, NEW, 1); wr(CF, c); print("AppVersion bumped")

# ---------------------------------------------------------------- 3. CLAUDE.md §9 / §11 / §14
CM = os.path.join(PF, "CLAUDE.md"); m = rd(CM)
OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 343 BASELINE — RE-ESTABLISHED ON THE D10-6 POPULATION"
NEW9 = (f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 344 BASELINE (the opening duplicate body heading dropped in full — KB constraint 47, Chris's D10-1; + the header title's stray markdown markers; SCOPED regeneration of 21 modules / 48 pages, scoped ship #1 since the r342 full): SCAFFOLD mean {SK_A}% / >=50% {GE50} / >=75% {GE75} / >=90% {GE90} / skipped 0 @ {PAIRS}; RAW {RAW_A}%** (state `outputs/_r344_sk_final.json`, FRESH) = **{PCT}% of achievable** (ceiling {CEIL}%). r344 +0.016 ({SK_B4} → {SK_A4}; {MOVERS}); compare_structure exact {CS_B} → {CS_A} (−8 = the text-matched pool {POOL_B} → {POOL_A}, the dropped gold-kept headings leaving the pool — the r57 / r147 relocation class; EXTRA {EX} / missing {MI} EXACT); clean {CLEAN} / leak 26/23 / body 180 EXACT; every other gate EXACT. Older r343 text: **ROUND 343 BASELINE — RE-ESTABLISHED ON THE D10-6 POPULATION")
if "ROUND 344 BASELINE" not in m:
    assert m.count(OLD9) == 1, "§9"; m = m.replace(OLD9, NEW9, 1); print("§9")
A11 = "| `HYPERTAG_OFF` | 342 | **A WRITER'S MEDIA TAG TYPED AS A HYPERLINK IS STILL A TAG**"
R11 = ("| `DEDUPC47_OFF` | 344 | **THE OPENING DUPLICATE BODY HEADING IS DROPPED IN FULL — KB constraint 47** (Chris's D10-1, Option A; the autonomous loop's session-12 Round 1; **SCOPED regeneration of the 21 affected modules / 48 pages; scoped ship #1 since the r342 full**). Reverts byte-for-byte (OFF in memory = disk 2110/2110). ON (default), `body_region.lesson_title_dedup.c47` `{ enabled, env, first_rendered_heading, ignore_punctuation, skip_inside_activity, exclude_body_class }`: on a LESSON page (`#pageIsLesson`; the overview keeps the r80 exact de-dup) the r75 first-heading de-dup is refined three ways — a heading CONSUMED by the de-dup no longer spends the first-heading slot, so the real opening heading is tested (MXEO202_3_0's `[H2] *Lesson 3 Triangles*` then `[H3] Triangles`); the compare key keeps letters and digits only (HIS1001_7_0's curly quotes, ENGR202's italicised `*:*`, PES1002's `**` + trailing note); a heading with an open `activity` frame on the container stack is never the candidate and never spends the slot (ENGI101 \"Being Frank\" = the activity's own title, KEPT). The Bilingual template (body class `reoTranslate`) is excluded — KB 07B governs the MTK section heading. MEASURED (`outputs/_measure_r344_c47.py`, the first FREE-BODY heading): 31 target pages / 15 modules, gold drops 20 / keeps 11 (the NAMED overrides — SCCH301 ×5 / SCPH301 ×3 / HIS1001 / MXEO202 / XDLS903, whose golds show the MODULE title in the header). After: targets 31 → 1 (XDLS903's image-caption h4, the gold's own). Skeleton +0.016pp (33 moved — 21 up / 12 down, pp-sum +31.82; every dip named — the overrides, the scorer's alignment artefact on PES1002_4_0 / MXFU302_1_0 with position-free overlap RISING, one coincidental match); cs exact −8 = the matched pool −8; every other gate EXACT. |\n"
       "| `TITLEMARK_OFF` | 344 | **A HEADER TITLE NEVER CARRIES A WRITER'S MARKDOWN MARKER** (D10-1's sibling — KB c79 hygiene, upstream of the r327 title-casing seam; ships with r344). Reverts byte-for-byte. ON (default), `body_region.lesson_title_dedup.title_markers`: in `PageSplitter`'s title post-pass, BEFORE the r324 label / bare-number tests, a `page.pageTitle` carrying a `*` loses every marker and collapses whitespace; a title left with no letter or digit (XLP02_4_0's `*:`) is emptied so the module-title fallback applies. Fires only on a title with a marker. `**3**` → `3` → the r324 fill takes the lesson's own name from its first heading (MXFU201_3_0 `Convert 12 hour to 24-hour time` = the gold's title verbatim). MEASURED: 23 header titles / 8 modules carried a marker (MXFU302 `**Statistics and Sports**`, PES1008 `*Heat Capacity Calculations*` ×8, XDLS906, SSOG101 `* Police Officers` ×2, SSOG301, MXFU201 ×3, PES1002 ×9 — its trailing `Te reo Māori translation needed` note and MXFU201_8's `8.` prefix stay, recorded under the floor); the gold ships 0 of 2385 with a marker. After: 0 of all 2110 pages. |\n")
if "| `DEDUPC47_OFF` | 344 |" not in m:
    assert m.count(A11) == 1, "§11"; m = m.replace(A11, R11 + A11, 1); print("§11")
B14 = (f"- **Build:** `260619.15` (round 344 — **the opening duplicate body heading is dropped in full — KB constraint 47** (Chris's D10-1, Option A: the lesson NUMBER in the `#module-code` chip, the lesson's own title as the h1, no repeated body heading; the first RENDERED free-body heading equal to the title once case, punctuation and a `Lesson N` label are ignored — a consumed heading no longer spends the slot, activity-box titles are never candidates, the Bilingual template is excluded by 07B) **+ the header title's stray markdown markers** (c79 hygiene: `* Police Officers` / `**3**` / `*Heat Capacity Calculations*` cleaned, 23 → 0 corpus-wide); the autonomous loop's session-12 Round 1; **SCOPED regeneration of 21 modules / 48 pages; scoped ship #1 since the r342 full**). **ROUND 344 BASELINE: SCAFFOLD mean {SK_A}% / ≥50% {GE50} / ≥75% {GE75} / ≥90% {GE90} / skipped 0 @ {PAIRS}; RAW {RAW_A}%** (state `outputs/_r344_sk_final.json`, FRESH) = **{PCT}% of achievable** (ceiling {CEIL}%). +0.016pp ({SK_B4} → {SK_A4}; 33 moved — 21 up / 12 down, pp-sum +31.82, every mover in the affected set; the 12 dips NAMED — see §9). cs exact **{CS_A}** (−8 = the matched pool {POOL_B} → {POOL_A}: the dropped gold-kept headings leaving the pool, the r57 / r147 class) / EXTRA **{EX}** / missing **{MI}** EXACT; clean **{CLEAN}** / leak **26/23**; body **180** EXACT; every other gate EXACT; 13 selftests GREEN. Corpus 2110 pages / 416 modules, 0 truly stale, **48 pages / 21 modules changed, 0 added/removed**; toggles `DEDUPC47_OFF` / `TITLEMARK_OFF`; data `body_region.lesson_title_dedup.c47` + `.title_markers`. c47 targets 31 → 1 (XDLS903's image-caption h4, the gold's own). **Plateau window: r342 −0.003 · r344 +0.016 (two under-0.02 rounds; r343 is a population change and does not count).**\n")
if "- **Build:** `260619.15` (round 344" not in m:
    A = "- **Build:** `260619.14` (round 343 —"; assert m.count(A) == 1, "§14"; m = m.replace(A, B14 + A, 1); print("§14")
wr(CM, m)

# ---------------------------------------------------------------- 3b. CONVERTER_V2_GUIDE.md (B12 PageSplitter — the title-harvest paragraph)
GD = os.path.join(HERE, "..", "..", "pageforge-site", "CONVERTER_V2_GUIDE.md"); g = rd(GD)
AG = "- **Title harvesting rules** live in the post-pass loop near the end of `Split`, gated by `Emit_Templates.json → body_region.lesson_title_dedup`."
NG = AG + " **Since round 344** the post-pass first strips every `*` / `**` marker a writer left in the `[LESSON]` payload (`title_markers`, env `TITLEMARK_OFF`) — so `**3**` reads as the bare number it is and takes the lesson's own name from its first heading — and the body de-dup in `ContentConverter` applies KB constraint 47 in full (`c47`, env `DEDUPC47_OFF`): the first RENDERED free-body heading equal to the title once case, punctuation and a `Lesson N` label are ignored is dropped; a heading consumed as the title repeat no longer hides the real opening heading, a heading inside an activity box is never a candidate, and the Bilingual template is left to KB 07B."
if "Since round 344" not in g:
    assert g.count(AG) == 1, "guide"; g = g.replace(AG, NG, 1); wr(GD, g); print("guide")

# ---------------------------------------------------------------- 4. gate_baseline.json
GB = os.path.join(HERE, "..", "reference", "tests", "gate_baseline.json"); raw = rd(GB); d = json.loads(raw)
d["_meta"]["build"] = "260619.15"; d["_meta"]["round"] = 344; d["_meta"]["date"] = "2026-09-16"
d["skeleton"].update({"mean_scaffold_pct": float(SK_A), "raw_mean_pct": float(RAW_A), "pages_ge_50": GE50, "pages_ge_75": GE75, "pages_ge_90": GE90})
if "compare_structure" in d and isinstance(d["compare_structure"], dict):
    cs = d["compare_structure"]
    for k, v in (("exact_chain", CS_A),):
        if k in cs: cs[k] = v
d["_meta"]["_round344_note"] = (f"Round 344 (D10-1: KB c47 in full + the title markers; scoped regeneration 21 modules / 48 pages). skeleton {SK_B4}->{SK_A4} (+0.016pp; 33 moved 21 up / 12 down, every dip named); "
    f"buckets {GE50}/{GE75}/{GE90} EXACT; cs exact {CS_B}->{CS_A} = the matched pool {POOL_B}->{POOL_A} (the dropped gold-kept headings leaving the pool); EXTRA {EX} / missing {MI} / clean 2080/2103 / body 180 / leak 26/23 EXACT.")
wr(GB, json.dumps(d, ensure_ascii=False) + (chr(10) if raw.endswith(chr(10)) else "")); print("gate_baseline.json refreshed")

# ---------------------------------------------------------------- 5. KB_AMALGAMATION_STATUS.md — row 47, queue row 7, a D-row
KB = os.path.join(HERE, "..", "..", "KB_AMALGAMATION_STATUS.md"); k = rd(KB)
O47 = "| 47 | Drop a body heading identical to the lesson `<h1>` (ignoring `Lesson N`) | pre-ledger | lesson pages | **AUTHORISED — Chris D10-1 (2026-09-16): c47 in full"
N47 = "| 47 | Drop a body heading identical to the lesson `<h1>` (ignoring `Lesson N`) | pre-ledger | lesson pages | **CAPTURED-LIVE — round 344 (2026-09-16): c47 in full, the first RENDERED free-body heading equal to the title once case / punctuation / `Lesson N` are ignored (a consumed heading no longer spends the slot; activity-box titles kept; Bilingual left to 07B); c47 targets 31 → 1 (XDLS903's image-caption h4, the gold's own); 11 gold-kept repeats = the D10-1 named overrides.** Was: **AUTHORISED — Chris D10-1 (2026-09-16): c47 in full"
if "CAPTURED-LIVE — round 344" not in k:
    assert k.count(O47) == 1, "kb row 47"; k = k.replace(O47, N47, 1); print("KB row 47")
OQ7 = "| 7 | c47 / c95 `Lesson N` body-heading strip / drop | **AUTHORISED — Chris D10-1 (2026-09-16), queued item 2**;"
NQ7 = "| 7 | c47 / c95 `Lesson N` body-heading strip / drop | **SHIPPED round 344 (2026-09-16)** — 31 target pages / 15 modules re-measured on the first free-body heading (gold drops 20 / keeps 11), 48 pages / 21 modules changed incl. the title-marker sibling (23 → 0); skeleton +0.016pp. Was: **AUTHORISED — Chris D10-1 (2026-09-16), queued item 2**;"
if "SHIPPED round 344" not in k:
    assert k.count(OQ7) == 1, "kb queue 7"; k = k.replace(OQ7, NQ7, 1); print("KB queue row 7")
anchor = "| ~~—~~ | (not a KB row — Chris's D10-6, Option C) the eight CED revision-brief modules"
drow = ("| ~~—~~ | (KB c47 in full + c79 title hygiene — Chris's D10-1, Option A) on a lesson page the first RENDERED free-body heading equal to the header title (case, punctuation, `Lesson N` ignored) is dropped; a consumed heading no longer spends the first-heading slot; activity-box titles never candidates; Bilingual left to 07B; the header title loses a writer's `*` / `**` markers | **SHIPPED round 344** (scoped regeneration 21 modules / 48 pages) | 48 pages / 21 modules; c47 targets 31 → 1; marker titles 23 → 0 | skeleton +0.016pp (11 gold-kept repeats = named overrides; 2 scorer alignment artefacts named); cs exact −8 = the matched pool −8; every other gate EXACT | `DEDUPC47_OFF` / `TITLEMARK_OFF` | DECIDED (Chris D10-1; `_measure_r344_c47.py`) |\n")
if "(KB c47 in full + c79 title hygiene" not in k:
    assert k.count(anchor) == 1, "kb drow"; k = k.replace(anchor, drow + anchor, 1); print("KB status D-row")
wr(KB, k)

# ---------------------------------------------------------------- 6. LOOP_STATE.md
LS = os.path.join(HERE, "..", "..", "LOOP_STATE.md"); s = rd(LS); nl = chr(13) + chr(10) if chr(13) + chr(10) in s[:3000] else chr(10)
def L(t): return t.replace(chr(10), nl)
SEC = L(f"""## Session 12 · Round 1 (engine r344 — D10-1, KB constraint 47 in full) — what shipped (the opening duplicate body heading is dropped; the header title loses its stray markers)
- **Fix:** `body_region.lesson_title_dedup.c47` {{enabled, env DEDUPC47_OFF, first_rendered_heading, ignore_punctuation, skip_inside_activity, exclude_body_class
  "reoTranslate"}} at the `ContentConverter` heading branch (the c47 gate computed before the first-heading slot test; `#pageIsLesson` set beside
  `#pageLessonTitle` — the overview keeps the r80 exact de-dup): a heading CONSUMED by the de-dup no longer spends the slot (MXEO202's mechanism), the
  compare key keeps letters and digits only (HIS1001's quotes, ENGR202's `*:*`, PES1002's `**` + note), a heading with an open `activity` frame on the
  container stack is never the candidate (ENGI101 "Being Frank" KEPT), the Bilingual template excluded (07B). **Riding on it:** `title_markers`
  {{enabled, env TITLEMARK_OFF}} in `PageSplitter`'s title post-pass — every `*` stripped from `page.pageTitle` BEFORE the r324 label / bare-number tests
  (`**3**` → `3` → the lesson's own name from its first heading = MXFU201_3_0's gold title verbatim); a title left with no letter or digit emptied.
  Splice `outputs/_r344_splice.py` (idempotent; LF kept; 59 insertions / 4 deletions over 3 files).
- **Measured first** (`_measure_r344_c47.py` — the first FREE-BODY heading; the measurement tool's `inbox` test fixed as the trace required): the
  session-11 count of 40 (every body heading by text) is **31 target pages / 15 modules** on the first free heading (Standard 29 / Inquiry 2; Bilingual 2
  excluded by 07B); gold drops 20 / keeps 11 (SCCH301 ×5 / SCPH301 ×3 / HIS1001 / MXEO202 / XDLS903 — the NAMED overrides; their golds show the MODULE
  title in the header). Ladder: exact 16 (the slot mechanism) / lesson-prefix 11 / punct 4. The PICK's "PES1002 needs the pair's English half" was a
  misreading — the title carries the writer's trailing NOTE with leaked `**`; the punctuation fold closes it. Sibling: 23 marker titles / 8 modules.
- **Regeneration:** SCOPED — the in-memory probe over ALL 416 (`_r344_probe.cjs`, 4 shards): BOTH-OFF = disk 2110/2110; ON = **48 pages / 21 modules**
  (`_affected_r344.txt`: {AFF}); the other 395 byte-identical in memory (= the §0b whole-family proof). 4 batches rc 0; `_content_manifest.py fresh`
  0 truly stale; `diff` = exactly the 48 / 21, 0 added / removed. Three unmeasured modules changed for the same reasons (CEDT207_4_0 / ENG1005_2_0
  unpaired heading-only rows; PES1005_4_0's `** **` title unlocking its `Lesson 3:` de-dup).
- **Verifier:** c47 targets **31 → 1** (XDLS903_1_0's `<h4>Poi</h4>` is an image-caption render the gold keeps — residue, not c47); marker titles
  **23 → 0** over all 2110 pages; accordion over the 21: 68 panels / 9 modules every one matching the human; 13 selftests GREEN.
- **Gates:** skeleton **{SK_B} → {SK_A} (+0.016pp; {SK_B4} → {SK_A4})**; ≥50 {GE50} / ≥75 {GE75} / ≥90 {GE90} EXACT; RAW {RAW_B} → {RAW_A}; {MOVERS}.
  cs exact {CS_B} → {CS_A} (−8 = the matched pool {POOL_B} → {POOL_A}: the dropped gold-kept headings leaving the pool, the r57/r147 relocation class) /
  EXTRA {EX} / missing {MI} EXACT; body 180 EXACT; clean {CLEAN} / leak 26/23 EXACT (line-for-line); tags 9557/9557; flipCard 61 divergence 0;
  speechBubble defect 4 = the r341 baseline; modal / mtkQuiz defect 0; entry-parity PASS. Fast-loop `--commit --accept-named "compare_structure exact
  chain"` (decomposed above), ledger scoped #1 since the r342 full (7 of headroom), feature index rebuilt (selftest GREEN). **{PCT}% of achievable.**
- **Named:** the 11 gold-kept repeats (D10-1's override); PES1002's trailing title note (9 pages / 1 module) + MXFU201_8's `8.` prefix (1 page) — under
  the floor; XDLS903's image-caption h4; the re-leveller's rank rule (SSOG101 h4 → h3 vs a gold mixing h3 / h4 on the page — the r324 class).
- **Plateau window: r342 −0.003 · r344 +0.016 — two consecutive under-0.02 shipped rounds** (r343 is a population change and does not count); a third
  under-0.02 round with no other gate moved stops the loop on the plateau rule.

""")
ANCHOR = "## Session 11 · Round 2 PICK (engine r344 — D10-1, KB constraint 47 in full: the opening duplicate body heading)"
if "## Session 12 · Round 1 (engine r344 — D10-1, KB constraint 47 in full) — what shipped" not in s:
    assert s.count(ANCHOR) == 1, "state anchor"; s = s.replace(ANCHOR, SEC + ANCHOR, 1); print("LOOP_STATE section")
OLD_P = "- Remaining KB queue (§D):"
NEW_P = (f"- Session 12 Round 1 (engine r344 — Chris's D10-1: KB constraint 47 in full — the first RENDERED free-body heading equal to the title (case / punctuation / `Lesson N` ignored) is dropped, a consumed heading no longer spends the slot, activity-box titles kept, Bilingual left to 07B; + the header title's stray `*` / `**` markers): **SHIPPED 2026-09-16 ≈18:55 (session 12)**. AppVersion 260619.15, CLAUDE.md §9/§11/§14, KB status row 47 → CAPTURED-LIVE + queue row 7 SHIPPED + D-row, CONVERTER_V2_GUIDE B12, **SCOPED regeneration of 21 modules / 48 pages (scoped ship #1 since the r342 full)**. Skeleton +0.016pp (33 moved, 21 up; the 12 dips named), cs exact −8 = the matched pool −8, every other gate EXACT; c47 targets 31 → 1, marker titles 23 → 0.\n")
if "- Session 12 Round 1 (engine r344" not in s:
    assert s.count(OLD_P) == 1, "position"; s = s.replace(OLD_P, L(NEW_P) + OLD_P, 1); print("position")
OLD_R = "- s11-pick2 (no engine round) · r344 D10-1 c47 PICK + MEASUREMENT"
i = s.find(OLD_R); assert i > 0, "round log anchor"; j = s.find(nl, i) + len(nl)
NEW_R = (f"- s12-r1 (engine r344, D10-1) · KB constraint 47 in full — the first RENDERED free-body heading equal to the title (case / punctuation / `Lesson N` ignored) is dropped (a consumed heading no longer spends the slot — the MXEO202 mechanism; activity-box titles never candidates; Bilingual left to 07B) + the header title's stray `*` / `**` markers stripped (`**3**` → the lesson's own name) · SHIPPED 2026-09-16 ≈18:55 · SCOPED regeneration 21 modules / 48 pages, 0 added/removed (scoped #1 since the r342 full) · scaffold {SK_B}→{SK_A} (+0.016; {SK_B4}→{SK_A4}; 33 moved — 21 up / 12 down, pp-sum +31.82 / RAW +24.49, every mover in the affected set; the dips = the 11 D10-1 named overrides (SCCH301 / SCPH301 / MXEO202 — golds whose header shows the MODULE title) + PES1002_4_0 −10.31 / MXFU302_1_0 −6.17 the scorer's alignment artefact with position-free overlap RISING + ENGI202_6_0 a coincidental match), ≥50 {GE50} / ≥75 {GE75} / ≥90 {GE90} EXACT, cs exact {CS_B}→{CS_A} (−8 = the matched pool −8, the r57/r147 class) / EXTRA {EX} / missing {MI} EXACT, body 180, clean 98.91% / leak 26/23, every other gate EXACT · c47 targets 31→1 (XDLS903's image-caption h4, gold's own), marker titles 23→0 · {PCT}% of achievable · commit (see git log) · **plateau window: r342 −0.003 · r344 +0.016 (two under-0.02)**\n")
if "- s12-r1 (engine r344, D10-1)" not in s:
    s = s[:j] + L(NEW_R) + s[j:]; print("round log")
wr(LS, s); print("LOOP_STATE.md written")
