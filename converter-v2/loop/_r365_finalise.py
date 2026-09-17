#!/usr/bin/env python3
"""ROUND 365 (loop session 21 Round 2 — the widget-typed activity tag's tail is the box title) — finalise:
changelog, AppVersion (260619.35 → 260619.36), CLAUDE.md §9 / §11 (TYPEDTAG_OFF row) / §14, gate_baseline.json,
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
ENTRY = """## 2026-09-18 (round 365, build 260619.36) — THE WIDGET-TYPED ACTIVITY TAG'S TAIL IS THE BOX TITLE: `[Activity 1B – self-marking type the answer] Fill in the blanks` opens the gold's `<div class="activity interactive" number="1B"><h3>Fill in the blanks</h3>` — the title leaves the capture (the autonomous loop's session 21, Round 2; the r363 residue (a))

### 1. WHAT CHANGED, IN ONE LINE

**The Mathematics MXFL / MXEO / MXFU / MXDB family (and ENGJ / ENGR) types the widget TYPE inside the activity tag — `[Activity 1B – self-marking type the answer] Fill in the blanks`, `[Activity 3A – self-marking drag and drop] Negatives on the number line`, `… – self-marking drop down quiz]`, `… – memory card game]`, `… – reorder]`, `… – radio quiz]`, `… – multi-choice quiz]` — so the tag parses as the WIDGET (typing quiz / drag and drop / dropdown / memory game / reorder / radio quiz / mcq; number 1B) with the title as its tail, and the round-92 embedded-activity form made the tag its own box's owner with the title riding INTO the capture (or the built widget's r354 Writers Note) as a `<p>`. The gold opens the numbered box with `<h3>Title</h3>`. Now the converter's embedded-activity branch emits the title heading right after the box opens (the r266 level-pages precedent) and blanks the tag's tail so the capture, the built widget's note and the `.txt` hand-off never repeat it.** 36 pages / 6 modules change; skeleton +0.014pp, ≥50 +3.

### 2. THE EVIDENCE (docx → human → Claude)

- **MXEO301 lesson 1, 1B** — WT `[Activity 1B – self-marking type the answer] Fill in the blanks` + the questions; gold `<div class="activity interactive" number="1B"><div class="row"><div class="col-12"><h3>Fill in the blanks</h3>` + the typing widget; Claude (r364) `<div class="activity interactive" number="1B">` → the capture with `<p>Fill in the blanks</p>` inside (`MXEO301_1_0.html` line 167). Now: `<h3>Fill in the blanks</h3>` first, then the capture without the title.
- **MXFL301 lesson 2** — `[Activity 2A – self-marking drop down quiz] Using a ratio scale`, `[Activity 2B – self-marking type the answer] Finding the distance`, `… 2C …] Calculating scales`; gold each box `<h3>` first; Claude the captures. Now the three `<h3>`s (the disk diff is exactly `+<h3>Using a ratio scale</h3>` / `−<p>Using a ratio scale</p>` ×3).
- **MXFU301 1A** — `[Activity 1A – self-marking, reorder interactive] How likely? (Currently in correct order – please jumble)`: the title is `How likely?`; the bracketed writer note stays the tag's tail (the capture / the r354 note).
- **The item stream** (`outputs/_r365_items.cjs` on MXEO301): `[Activity 1B – self-marking type the answer] ‖ Fill in the blanks` → `tag=typing quiz nums=["1b"] dir=INTERACTIVE`, blackAfter = the title, `bundle.activityOwner` null, `bundle.activityId` "1B" → `embeddedAct`. (MXEO301 1A is typed in BLACK — `[Activity 1A – self-marking drag and drop] Prime factorisation Drag and drop …` — a writer error the engine renders literally: not this class.)

### 3. THE MEASUREMENT (before coding — `outputs/_measure_r365_typedtag.py` → `_r365_typedtag.{json,log}`; the r363 probe's box + state logic)

- 216 such openers in 12 modules' WTs (MXFL302 43, MXFL301 36, MXEO301 33, MXDB302 31, MXFU301 24, ENGR302 20, ENGJ302 14, ENGJ301 7, MXFU302 4, MXEX301 2, ENGR102 1, MXEO202 1), 170 with a title tail; 158 on the gate modules / 10 modules / 43 Claude pages. **The gold opens `<div class="activity interactive" number="N">` with `<h3>Title</h3>` on 0.81 of the 100 paired boxes (MXFU301 1.00, MXFU302 1.00, MXFL302 0.96, MXFL301 0.91, MXEO301 0.58, MXDB302 0.57); Claude 0.05** — the title inside the capture (77 boxes) or Claude's box under another number (58). THE MISS: 71 boxes / 6 modules / 32 pages — ≥ the 20-page body floor, consensus ≥ 0.60 in the Mathematics family, structure-only (the title is the tag's own tail). Authority: KB 01F (the `<h3>` activity heading inside the activity) + the family's gold.
- **The queue walked first (chrome before body, `DIFF_QUEUE.md` re-mined on the r364 corpus, 167 candidates) — every chrome row dispositioned, none a round:** title #5 (11 modules × 1 page: Claude ships the KB's `<h1><span>` where 11 disparate golds have none — gold outliers); the module-menu rows (the D10-9 `<h5>` override, the BLL banner form, the lesson-menu KB 01B rule); **the crumbs census (23 modules) decomposed with `outputs/_measure_r365_crumbs.py` (→ `_r365_crumbs.{json,log}`): 4 DUAL-BUILD gold dirs the gate pairs by position (BLL240 / CEDK501 / CEDT207 / CEDT301 — a single-file inquiry build beside the paged build; a pairing artefact), 2 the incomplete-`[page N]` label-list dialect (CEDT208 / CEDW201), 3 with no section tags at all (CEDT104 / TWHA905 / TWHK901), 3 with BLANK crumb labels (CEDW101 / EXBP901 / EXIP901 — the empty `[Tab N]` opener's label lookahead finds nothing), 2 label wording — no sub-class at the 10-module floor;** phases-nav (10 modules, the PICK-7 dispositions + ≤ 2 lines each); the footer rows (the r360 recorded overrides); acks #506 (the r317 KB template form); the journal button (#537 / #538 — a registry + a decision, recorded); #534 / #535 / #540 (`p` alignment residue, no single mechanism).

### 4. THE MECHANISM (ENGINE + data)

- **Data:** `Emit_Templates.activity_wrapper.embedded_interactive_activity.typed_tag_title` {enabled, env `TYPEDTAG_OFF`, tag_pattern (the raw tag text: `[Activity` + an id + a dash), title_heading `<h3>{title}</h3>`, min_title_chars 2, strip_trailing_note true}.
- **`ContentConverter`** (the bundle-owner path, right after `activityOpen` and the r266 `lvOwner` heading): when `embeddedAct` holds and the tag matches tag_pattern, the tail (markers stripped, whitespace folded; a trailing bracketed note split off) becomes `<h3>{title}</h3>`; `it._typedTitle` records it and `it.blackAfter` keeps only the note, so `InteractiveBuilder` (the capture, the r354 note) and `ManifestBuilder` (the `.txt`) never repeat it. Never on reoMode pages; a bracket-only tail is not a title. OFF = byte-identical.

### 5. THE PROOF

- **A/B (the in-memory probe `_r365_probe.cjs`, 4 shards under WSL):** `TYPEDTAG_OFF=1` = disk **2110 / 2110** byte-identical; ON = **36 pages / 6 modules** (MXDB302, MXEO301, MXFL301, MXFL302, MXFU301, MXFU302 — `_r365_changed_{pages,modules}.txt`; the six other typed-tag modules carry no title tail on a gate page).
- **SCOPED regeneration** of the 12-module family (`_r365_affected.txt`, one `batch_convert.cjs` call, rc 0): `_content_manifest.py diff` **36 pages / 6 modules changed, 0 added / 0 removed** = the probe's set; every regenerated page byte-identical to the probe's ON page (36 / 36); `fresh --affected` (the 12) → 0 truly stale, the other 401 byte-identical to the manifest (`_stalecheck.sh`'s 401 "stale" is the mtime false alarm after the data edit — the content-hash check is the proof). Scoped ship #1 since the r364 full (ledger).
- **Gates (`_r365_gates.log`, rc 0, pairs skipped 0):** skeleton SCAFFOLD mean **52.637 → 52.651 % (+0.014pp)**, **≥50 1118 → 1121 (+3)**, ≥75 173 / ≥90 15 EXACT, RAW 37.162 → 37.166 %; **35 movers — 28 up / 7 down** (`_r365_movers.log`, `_r364_sk_final.json` → `_r365_sk_final.json`). compare_structure 11631 / 175 / 617 / 23 EXACT; body_compare 197 / 42 / 4 / 152 EXACT; defect audit (leak 26 / 23), tags 9557 / 9557, every widget verifier line-for-line IDENTICAL to r364; the 16 selftests green.
- **The dips, named (7):** MXFL302_6_0 34.1 → 21.0 (the disk diff is four lines — two `<h3>` gained, two `<p>` gone — and difflib re-aligned the long page: the r363 precedent; `match()` on the r364 page gives 20.7 today, so the earlier 34.1 was itself an alignment artefact), MXFL301_2_0 49.5 → 45.6 (three titles gained; the box numbers differ from the gold's 2A–2D), MXFU301_10_0 26.5 → 24.6, MXFU301_9_0 39.0 → 37.5, MXFL302_1_0 71.3 → 70.7, MXFL302_8_0 51.7 → 51.3, MXFU301_3_0 34.5 → 34.2. The largest gains: MXFL302_2_0 27.5 → 35.2, MXDB302_2_0 37.8 → 45.5, MXFL302_7_0 61.7 → 64.7, MXFU301_7_0 48.1 → 50.5.
- **Residue recorded, not chased:** the "other number" boxes (58 of the 158 tags — Claude's box carries a sequence letter where the gold keeps the writer's id) are the r217 numbering, out of scope here; the BLACK-typed tag (MXEO301 1A) is a writer error.
- Ledger: SCOPED (counter 1). AppVersion 260619.36; CLAUDE.md §9 / §11 / §14; `gate_baseline.json` (skeleton 52.651 / 1121 / 173 / 15; RAW 37.166); loop README; `_MIGRATION/CHECKSUMS__engine.txt` refreshed (`.pre-r365.bak` kept).

"""
if "round 365, build 260619.36" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r365 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.36"' not in s:
    old = '\tstatic AppVersion = "260619.35";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, '\t// ROUND 365 (260619.36): the widget-typed activity tag\'s tail is the box title — `[Activity 1B – self-marking type the answer] Fill in the blanks` opens the gold\'s numbered box with <h3>Fill in the blanks</h3> and the title leaves the capture (data Emit_Templates.activity_wrapper.embedded_interactive_activity.typed_tag_title; env TYPEDTAG_OFF). The autonomous loop\'s session 21 Round 2.\n\tstatic AppVersion = "260619.36";')
    wr(P, s); print("Config.js: 260619.36")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "ROUND 365 BASELINE" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 364 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 365 BASELINE (the widget-typed activity tag's tail is the box title — 6 modules; SCOPED regeneration of the 12-module family, scoped ship #1 since the r364 full): SCAFFOLD mean 52.651% / >=50% 1121 / >=75% 173 / >=90% 15 / RAW 37.166% @ 1956 pairs, pairs skipped 0 — hold-or-improve; 35 movers (28 up, 7 down — the dips named in the r365 changelog: difflib re-alignment on long pages after a title `<p>` → `<h3>`).** Previous — ROUND 364 BASELINE"
             + OLD9[len("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 364 BASELINE"):])
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `IDHEAD_OFF` | 364 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `TYPEDTAG_OFF` | 365 | **THE WIDGET-TYPED ACTIVITY TAG'S TAIL IS THE BOX TITLE** (the autonomous loop's session 21 Round 2 — the r363 residue (a); KB 01F). The Mathematics MXFL / MXEO / MXFU / MXDB family types `[Activity 1B – self-marking type the answer] Fill in the blanks`: the tag parses as the WIDGET (number 1B) and the round-92 embedded form put the title INSIDE the capture as a `<p>`; the gold opens the box with `<h3>Title</h3>` (0.81 of 100 paired boxes). Now the converter emits `<h3>{title}</h3>` right after the box opens (the r266 precedent) and blanks the tag's tail (a trailing bracketed writer note stays). Data `Emit_Templates.activity_wrapper.embedded_interactive_activity.typed_tag_title`. OFF = byte-identical (2110 / 2110). 36 pages / 6 modules; skeleton +0.014pp, ≥50 +3. |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.35` (round 364"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.36` (round 365 — **the widget-typed activity tag's tail is the box title** (`[Activity 1B – self-marking type the answer] Fill in the blanks` → the gold's numbered box opening with `<h3>Fill in the blanks</h3>`, the title out of the capture; data `Emit_Templates.activity_wrapper.embedded_interactive_activity.typed_tag_title`, env `TYPEDTAG_OFF`); the autonomous loop's session-21 Round 2, the r363 residue (a); 36 pages / 6 modules; SCOPED regeneration of the 12-module family (scoped ship #1 since the r364 full); skeleton 52.637 → 52.651 %, ≥50 1121, ≥75 173, ≥90 15, RAW 37.166 %, every other gate EXACT). Previous: `260619.35` (round 364"
             + OLD14[len("- **Build:** `260619.35` (round 364"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r365" not in d["skeleton"]:
    d["skeleton"]["mean_scaffold_pct"] = 52.651
    d["skeleton"]["raw_mean_pct"] = 37.166
    d["skeleton"]["pages_ge_50"] = 1121
    d["skeleton"]["pages_ge_75"] = 173
    d["skeleton"]["pages_ge_90"] = 15
    d["skeleton"]["_note_r365"] = "Round 365: the widget-typed activity tag's tail is the box title — SCAFFOLD 52.6374 → 52.6514 (+0.014pp; 35 movers, 28 up / 7 down, the dips named in the changelog — difflib re-alignment on long pages after a title <p> → <h3>), ≥50 1118 → 1121, ≥75 173 / ≥90 15 EXACT, RAW 37.162 → 37.166; SCOPED regeneration of the 12-module typed-tag family (36 pages / 6 modules)."
    d["_meta"]["build"] = "260619.36"; d["_meta"]["round"] = 365; d["_meta"]["date"] = "2026-09-18"
    d["_meta"]["_note_r365"] = "Round 365: the widget-typed activity tag's tail is the box title — skeleton +0.014pp (≥50 +3), every other gate EXACT; SCOPED regeneration (12 modules; scoped ship #1 since the r364 full)."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r365")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_r365_finalise.py" not in s:
    A = "| `_measure_r364_idheading.py`"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_measure_r365_crumbs.py` / `_r365_crumbs.{json,log}` (the crumbs census decomposed) / `_measure_r365_typedtag.py` / `_r365_typedtag.{json,log}` / `_r365_items.cjs` / `_r365_probe.cjs` / `_r365_probe_{OFF,ON}_[0-3].log` / `_r365_changed_{modules,pages}.txt` / `_r365_on/` (the probe's ON pages, byte-identical to the shipped disk) / `_r365_pagescore.py` / `_r365_onscore.json` / `_r365_affected.txt` / `_r365_regen.log` / `_r365_manifest_diff.log` / `_r365_stalecheck.log` / `_r365_fresh.log` / `_r365_gates.log` / `_r365_sk_full.log` / `_r365_sk_final.json` / `_r365_movers.log` / `_r365_ledger.log` / `_r365_finalise.py` / `_r365_postship.sh` / `_r365_selftests.log` / `_r365_fastloop_snapshot.log` / `_r365_manifest_snapshot.log` / `_r365_index.log` | "
           + loc + " | Session 21 Round 2 (engine r365, build 260619.36) — the widget-typed activity tag's tail is the box title: the queue walk (the crumbs census decomposed below the floor), the class measurement, the probe, the scoped regeneration of the 12-module family, gates, movers, finalise and post-ship logs. |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r365 rows")
print("finalise done")
