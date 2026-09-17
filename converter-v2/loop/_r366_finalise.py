#!/usr/bin/env python3
"""ROUND 366 (loop session 21 Round 3 — the lead prose after the widget tag renders free inside the box) — finalise:
changelog, AppVersion (260619.36 → 260619.37), CLAUDE.md §9 / §11 (LEADFREE_OFF row) / §14, gate_baseline.json,
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
ENTRY = """## 2026-09-18 (round 366, build 260619.37) — THE LEAD PROSE AFTER THE WIDGET TAG RENDERS FREE INSIDE THE BOX: `[Interactive]` / `Drag and drop the products into the correct category.` / TABLE → `<h3>…</h3><p>Drag and drop …</p>` + the widget, the instruction no longer a capture member — scoped by widget type (the autonomous loop's session 21, Round 3)

### 1. WHAT CHANGED, IN ONE LINE

**A writer types the widget tag, then the instruction paragraph, then the widget's table. `InteractiveScanner.#swallowMembers` walks that black run into the bundle as a MEMBER, so an un-built capture showed the instruction inside the dashed box (and a built widget's hand-off carried it) while the gold keeps it FREE in the activity box — `<h3>Title</h3><p>Drag and drop …</p>` then the widget. Now, for the widget types whose gold keeps the lead free (dragAndDrop, dropDown, reorder, typing, modal, radioQuiz, and a standalone unclassified capture), the converter renders the FIRST paragraph of the first black member after the tag as a free paragraph inside the box and takes it out of the member list before the capture is built; the paragraphs after it (typing answers, reorder steps, image / drive links) stay members.** 106 pages / 46 modules change; skeleton +0.046pp, ≥50 +2.

### 2. THE EVIDENCE (docx → human → Claude)

- **AGH1001 lesson 1, 1B** — WT `[Interactive]` / `Drag and drop the products into the correct category.` / a two-column TABLE; gold `<div class="activity interactive" number="1B"><h3>Agricultural and horticultural products</h3><p>Drag and drop the products into the correct category.</p><div class="dragAndDrop …">`; Claude (r365) the r217 standalone box → the capture `⚙ INTERACTIVE (un-built) #2: interactive — Activity (inline)` with `<p>Drag and drop …</p>` as its first member. Now the `<p>` is free inside the box, the capture holds the table.
- **MXDB302 lesson 2, 2A** — WT `[Activity 2A – auto self-marking drag and drop] Which Unit?` / `Drag each item into the correct column …` / TABLE; gold `<h3>Which Unit?</h3><p>Drag each item …</p><div class="ddColumn">`; Claude (r365) the `<h3>` (r365) then the capture with the instruction inside. Now `<h3>` + `<p>` + the capture (the disk diff is `+<p>Find the perimeter …</p>` / `−<p>Find the perimeter …</p>` ×4 on that page).
- **MXFL302 lesson 5** — `Match up the improper fraction and mixed number pairs …` and `Calculate the following equations …` leave their captures (+9.2pp on `MXFL302_5_1_0`); **AGH1004 lesson 3** +12.0pp; **MXEO301 lesson 6** +10.3pp.

### 3. THE MEASUREMENT (before coding)

- **The activity rows decomposed by mechanism** (`outputs/_measure_r366_actmiss.py` → `_r366_actmiss.{json,log}`; every gold skeleton line in the `activity` region with no source among Claude's skeleton lines of the page, located on Claude's page): 8,449 lines — **3,414 INSIDE a Claude capture (617 pages / 293 modules: `p` 1,923 / 556 pages, `li` 1,013 / 156, `h3` first-in-box 254 / 147 pages / 79 modules, `h4` 149)**, 400 inside a built widget or a Writers Note (148 pages), 4,635 not on Claude's page (974 pages; that run's WT test fell through — the class-C / lost split is owed to the next PICK).
- **The lead-prose class** (`outputs/_measure_r366_leadprose.py` → `_r366_leadprose.{json,log}`; every un-built capture with a leading black paragraph — 1,525 on 769 pages / 329 modules — its header type + owner kind, and the gold's treatment of that text): the gold keeps the lead FREE on **0.52 overall — a tie — but by WIDGET TYPE it splits: dragAndDrop 0.60 standalone / 0.63 owned, dropDown 0.75, reorder 0.93 / 0.68, typing 0.82 / 0.84, standalone unclassified 0.64, modal 0.65 / 0.85, radioQuiz 0.80 / 0.67 — against carousel 0.25 / 0.08, flipCard 0.28, accordion 0.38, selfCheck 0.47 / 0.35, clickDrop 0.42, multiChoiceQuiz 0.37 / 0.58, tabs 0.38 (those fold the lead INTO the widget — r352's territory).** The scoped set (types_standalone / types_owned): **579 captures, gold-free 0.69, 366 pages / 219 modules — Standard 0.68, Fundamentals 0.70, Inquiry 0.76; Mathematics 0.73, English 0.74, NCEA1 0.66, ConnectED 0.89, OS9000 0.81, Blended Literacy 0.60, Technology 0.70, HPE 0.78; Social Science 0.08 (12 captures / 5 modules) and Arts 0.22 (9 / 4) EXCLUDED by code prefix (SSCI / SSFUN / SSOG / ARFUN).** The miss: 401 captures / 264 pages / 164 modules. Authority: the gold's group consensus by widget type (§1b level 3) + KB 01F (activity-level prose is free prose; the widget follows).
- **The first probe freed the WHOLE leading black run** (every paragraph before the table): 109 pages, 57 up / 45 down, +36pp-sum — the later paragraphs are the widget's own content typed as prose (typing answers, reorder steps, image / drive links) and became EXTRA `p`s. The rule was tightened to the first paragraph of the first black member: 106 pages, **65 up / 34 down, +91pp-sum**.
- **Queue rows recorded, not chased:** the un-boxed standalone dropDown / typing / reorder widgets (the r217 `standalone_widget_box.types` list has no box for them — their gold has one: its own class); the r362 residue (b) (7 boxes / 6 modules); the "other number" boxes of the typed tags (r365).

### 4. THE MECHANISM (ENGINE + data)

- **Data:** `Emit_Templates.activity_wrapper.lead_free_after_tag` {enabled, env `LEADFREE_OFF`, types_standalone [dragAndDrop, dropDown, reorder, typing, unclassified, modal, radioQuiz], types_owned [dragAndDrop, typing, reorder, modal, radioQuiz], exclude_code_prefixes [SSCI, SSFUN, SSOG, ARFUN], require_remaining_member true, min_words 2 (default), max_first_words (unset)}.
- **`ContentConverter`** (the bundle-owner path, after the owner's lead renders and before `#interactivePlaceholder`): for a box (standalone `saOwner` or owned) whose `bundle.type` is in the list for its owner kind, the first black member after the opener tag has its FIRST paragraph rendered free (`ListsAndRuns.renderBlackText`, the r362 lead's own renderer, through `actDeBold`) when it is not URL-like and at least one non-black member (a table / list / tag) remains; the remainder of that member's text stays the member (`_leadFreed` records the freed line), or the member leaves `bundle.memberItems` when nothing remains (`consumedBy = "lead-free"`). `#interactivePlaceholder` → `InteractiveBuilder.Build` reads the members live, so the capture, the build and the `.txt` hand-off never repeat the freed line. Never on reoMode pages or in the MTK quiz shell. OFF = byte-identical.

### 5. THE PROOF

- **A/B (the in-memory probe `_r366_probe.cjs`, 4 shards under WSL):** `LEADFREE_OFF=1` = disk **2110 / 2110** byte-identical; ON = **106 pages / 46 modules** (`_r366_changed_{pages,modules}.txt`).
- **FULL regeneration** (`_r366_fullship_par.sh`, 36 batches, all rc 0, 4 m 55 s; the touched widget families span most of the corpus): `_content_manifest.py diff` **106 pages / 46 modules changed, 0 added / 0 removed** = the probe's set; every regenerated page byte-identical to the probe's ON page (106 / 106); `_stalecheck.sh` 0 stale; `fresh --affected` 0 truly stale. Ledger FULL (counter 0).
- **Gates (`_r366_gates.log`, rc 0, pairs skipped 0):** skeleton SCAFFOLD mean **52.651 → 52.698 % (+0.046pp)**, median 53.0 → 53.1, **≥50 1121 → 1123 (+2)**, ≥75 173 / ≥90 15 EXACT, RAW 37.166 → 37.193 %; **99 movers — 65 up / 34 down** (`_r366_movers.log`). compare_structure 11631 / 175 / 617 / 23 EXACT; structural defect audit (leak 26 / 23) EXACT; tags 9557 / 9557; every widget verifier (dragAndDrop 21 widgets defect 0, dropDown, modal, …) line-for-line IDENTICAL to r365; the 16 selftests green. **body_compare: over-capture 42 EXACT, runaway 4 EXACT, EMPTY interactive container 152 → 157 (+5) and any 197 → 202 — NAMED:** the EMPTY heuristic reads a capture whose visible prose left it; the flagged pages among the 106 changed are MXEO301_5_0 / _6_0 (+10.3pp), AGH1007_2_0, ENGI405_5_0, HES1003_8_0, HIS1005_9_1, HIS1007_3_1, MXDB302_2_0 / _9_0 — each still holds its table.
- **The dips, named (34; the largest):** MXDB302_2_0 45.5 → 42.9 (four instructions freed, one beside a drive link the gold renders as an image), MXEO301_5_0 45.4 → 43.5, PES1005_7_0 76.6 → 75.4, ENGS401_4_0 −0.6, MXFL302_1_0 −0.6, ENGS102_6_0 −0.5, CEDO301_3_0 −0.5 — difflib re-alignment after a `p` moves out of a collapsed widget; none below −2.6. The largest gains: AGH1004_3_0 34.9 → 46.9, MXEO301_6_0 49.6 → 59.9, MXFL302_5_1_0 64.6 → 73.8, MXFL302_4_0 55.0 → 60.0, ENGC101_3_0 56.6 → 61.5.
- Ledger: FULL (counter 0). AppVersion 260619.37; CLAUDE.md §9 / §11 / §14; `gate_baseline.json` (skeleton 52.698 / 1123 / 173 / 15; RAW 37.193; body_compare 202 / 42 / 4 / 157 NAMED); loop README; `_MIGRATION/CHECKSUMS__engine.txt` refreshed (`.pre-r366.bak` kept); `DIFF_QUEUE.md` re-mined on the r366 corpus (169 candidates).

"""
if "round 366, build 260619.37" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r366 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.37"' not in s:
    old = '\tstatic AppVersion = "260619.36";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, '\t// ROUND 366 (260619.37): the lead prose after the widget tag renders free inside the box — the instruction paragraph between `[Interactive]` and its table becomes the box\'s free <p> (the gold\'s h3 + p + widget) for the widget types whose gold keeps it free (data Emit_Templates.activity_wrapper.lead_free_after_tag; env LEADFREE_OFF). The autonomous loop\'s session 21 Round 3.\n\tstatic AppVersion = "260619.37";')
    wr(P, s); print("Config.js: 260619.37")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "ROUND 366 BASELINE" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 365 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 366 BASELINE (the lead prose after the widget tag renders free inside the box — 46 modules; FULL regeneration of all 416, ledger 0): SCAFFOLD mean 52.698% / >=50% 1123 / >=75% 173 / >=90% 15 / RAW 37.193% @ 1956 pairs, pairs skipped 0 — hold-or-improve; 99 movers (65 up, 34 down — the dips named in the r366 changelog: difflib re-alignment after a `p` leaves a collapsed widget; none below −2.6).** Previous — ROUND 365 BASELINE"
             + OLD9[len("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 365 BASELINE"):])
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `TYPEDTAG_OFF` | 365 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `LEADFREE_OFF` | 366 | **THE LEAD PROSE AFTER THE WIDGET TAG RENDERS FREE INSIDE THE BOX** (the autonomous loop's session 21 Round 3; KB 01F). The instruction paragraph a writer types between the widget tag and its table (`[Interactive]` / `Drag and drop the products …` / TABLE) was a capture MEMBER; the gold keeps it free (h3 + p + the widget) for dragAndDrop 0.60–0.63, dropDown 0.75, reorder 0.68–0.93, typing 0.82–0.84, standalone unclassified 0.64, modal 0.65–0.85, radioQuiz 0.67–0.80 (a carousel / flipCard / accordion / selfCheck / clickDrop fold it in and are NOT listed). The converter frees the FIRST paragraph of the first black member after the tag (URL-like lines and the paragraphs after it stay members; at least one non-black member must remain; Social Science / Arts codes excluded — gold 0.08 / 0.22). Data `Emit_Templates.activity_wrapper.lead_free_after_tag`. OFF = byte-identical (2110 / 2110). 106 pages / 46 modules; skeleton +0.046pp, ≥50 +2; body_compare EMPTY +5 named. |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.36` (round 365"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.37` (round 366 — **the lead prose after the widget tag renders free inside the box** (the instruction paragraph between `[Interactive]` and its table → the box's free `<p>`, out of the capture, for the widget types whose gold keeps it free; data `Emit_Templates.activity_wrapper.lead_free_after_tag`, env `LEADFREE_OFF`); the autonomous loop's session-21 Round 3; 106 pages / 46 modules; FULL regeneration; skeleton 52.651 → 52.698 %, ≥50 1123, ≥75 173, ≥90 15, RAW 37.193 %, compare_structure EXACT, body_compare 202 / 42 / 4 / 157 named). Previous: `260619.36` (round 365"
             + OLD14[len("- **Build:** `260619.36` (round 365"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r366" not in d["skeleton"]:
    d["skeleton"]["mean_scaffold_pct"] = 52.698
    d["skeleton"]["raw_mean_pct"] = 37.193
    d["skeleton"]["pages_ge_50"] = 1123
    d["skeleton"]["pages_ge_75"] = 173
    d["skeleton"]["pages_ge_90"] = 15
    d["skeleton"]["_note_r366"] = "Round 366: the lead prose after the widget tag renders free inside the box — SCAFFOLD 52.6514 → 52.6979 (+0.046pp; 99 movers, 65 up / 34 down, the dips named in the changelog — none below −2.6), ≥50 1121 → 1123, ≥75 173 / ≥90 15 EXACT, RAW 37.166 → 37.193; FULL regeneration of all 416 (106 pages / 46 modules)."
    bc = d["body_compare"]
    bc["any_breakdown"] = 202; bc["over_capture"] = 42; bc["runaway"] = 4; bc["empty_container"] = 157
    bc["_note_r366"] = "Round 366: EMPTY interactive container 152 → 157 and any_breakdown 197 → 202 — NAMED (the heuristic reads a capture whose visible instruction left it for the box; MXEO301_5_0 / _6_0, AGH1007_2_0, ENGI405_5_0, HES1003_8_0, HIS1005_9_1, HIS1007_3_1, MXDB302_2_0 / _9_0 — each still holds its table); over_capture 42 / runaway 4 EXACT. Hold-or-improve from 202 / 42 / 4 / 157."
    d["_meta"]["build"] = "260619.37"; d["_meta"]["round"] = 366; d["_meta"]["date"] = "2026-09-18"
    d["_meta"]["_note_r366"] = "Round 366: the lead prose after the widget tag renders free — skeleton +0.046pp (≥50 +2), compare_structure EXACT, body_compare EMPTY +5 named; FULL regeneration of all 416, 46 modules / 106 pages; ledger FULL (counter 0)."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r366")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_r366_finalise.py" not in s:
    A = "| `_measure_r365_crumbs.py`"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_measure_r366_actmiss.py` / `_r366_actmiss.{json,log}` (the activity rows decomposed by mechanism) / `_measure_r366_leadprose.py` / `_r366_leadprose.{json,log}` / `_r366_probe.cjs` / `_r366_probe_{OFF,ON}_[0-3].log` / `_r366_changed_{modules,pages}.txt` / `_r366_on/` (the probe's ON pages, byte-identical to the shipped disk) / `_r366_pagescore.py` / `_r366_onscore.json` / `_r366_fullship_{run,par}.sh` / `_r366_batch_*.{sh,log}` / `_r366_fullship_regen.log` / `_r366_manifest_diff.log` / `_r366_stalecheck.log` / `_r366_fresh.log` / `_r366_gates.log` / `_r366_bodycompare_changed.log` / `_r366_sk_full.log` / `_r366_sk_final.json` / `_r366_movers.log` / `_r366_ledger.log` / `_r366_finalise.py` / `_r366_postship.sh` / `_r366_selftests.log` / `_r366_fastloop_snapshot.log` / `_r366_manifest_snapshot.log` / `_r366_index.log` / `_r366_miner.log` | "
           + loc + " | Session 21 Round 3 (engine r366, build 260619.37) — the lead prose after the widget tag renders free inside the box: the mechanism decomposition of the miner's activity rows, the lead-prose class measured by widget type, the probe (whole-run then first-paragraph variants), the FULL regeneration, gates, movers, finalise and post-ship logs. |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r366 rows")
print("finalise done")
