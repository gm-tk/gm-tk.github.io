#!/usr/bin/env python3
"""ROUND 362 (loop session 19 Round 6 — the unclassified activity keeps its title heading and lead prose free) — finalise:
changelog, AppVersion (260619.32 → 260619.33), CLAUDE.md §9 / §11 (UNCLASSLEAD_OFF row) / §14, gate_baseline.json,
loop/README.md. Idempotent; LF via wr()."""
import io, os, json
ROOT = r"C:\Users\Gavin\TeKura\FINAL_MODULE_DATA"
PF = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)

CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)" + chr(10) + chr(10)
ENTRY = """## 2026-09-17 (round 362, build 260619.33) — THE UNCLASSIFIED ACTIVITY KEEPS ITS TITLE HEADING AND LEAD PROSE FREE: an `[Activity N] Title` whose only widget signal is a data table used to be captured WHOLE — title, instruction paragraph and all — as the unclassified placeholder box; now the opener is the bundle's `activityOwner` and the prose before the first table its `activityLeadItems`, exactly the normal path's owner form, so the box opens with the KB 01F `<h3>` title + the instruction `<p>` and the hand-off box follows — `InteractiveScanner` (the unclassified-activity path), the converter's lead rendering (a media / URL tail is never the title), data `Interactive_Boundary_ChildTag_Bank._meta.opener_rule.unclassified_activity_lead`, env `UNCLASSLEAD_OFF`; the autonomous loop's session-19 Round 6, the DIFF MINER's activity classes #542 / #535 / #533; **FULL regeneration of all 416 (36 batches, all rc 0), 158 modules / 291 paired pages changed; skeleton SCAFFOLD 52.093 → 52.266 % (+0.173pp; 287 movers — 200 up, 87 down, the dips named), ≥75 161 → 168, ≥50 1096 → 1098; compare_structure EXACT (11645); body_compare over-capture 43 → 42, its EMPTY-container heuristic 136 → 151 (named — the title text now sits outside the box); ledger FULL (counter 0)**

### 1. WHAT CHANGED, IN ONE LINE

**958 activity boxes on 535 pages opened with a capture where the gold opens with the title heading — the writer's `[Activity 1A] How many sounds?` + `[body] When we are learning…` + the widget's data table were one unclassified bundle, so the title and the paragraph lived inside the raw hand-off dump; the human keeps them free (`<h3>How many sounds?</h3><p>When we are learning…</p>` then the widget), and now so does Claude.**

### 2. THE EVIDENCE (docx → human → Claude)

- **BLL116 lesson 1, activity 1A** — WT `[Activity 1A] How many sounds?` / `[body] When we are learning to read words we sound the letters out …` / a TABLE (audio + tick boxes) / `[body] Now it's your turn…` / a TABLE; gold `BLL116-02.html` `<div class="activity interactive" number="1A"><div class="row"><div class="col-12"><h3>How many sounds?</h3><p>When we are learning to read …</p>` then the built widget; Claude before `<div class="activity" number="1A"><div class="row"><div class="col-12"><div class="cv2-interactive …"><span>BLL116-INT-01-01-unclassified</span>` — the title and the paragraph inside the dump; after `<h3>How many sounds?</h3><p>When we are learning …</p><div class="cv2-interactive …">`. BLL117 1A («Where is the sound?»), BLL121 1C, BLL114 1B, ENGR202 5A («Photo Match-up» + two paragraphs), XMES201 2C the same.
- **The live item stream** (`outputs/_r361_items.cjs` on BLL116): every item of the activity — the `[Activity 1A]` opener included — carried `consumedBy = 0`.

### 3. THE MEASUREMENT (before coding — `outputs/_measure_r362_actlead.py` → `_r362_actlead.{json,log}`: every paired page, the activity boxes keyed by `number` on both sides, each box's leading element sequence up to its first widget)

- **4024 number-paired boxes / 409 modules: 2605 open with `h3` on BOTH sides; 958 boxes / 247 modules / 535 pages open with `h3` in the gold and a WIDGET in Claude's — 908 a `cv2-interactive` capture, 39 a super-content panel, 11 built widgets; in 527 the gold's h3 text sits inside Claude's box (swallowed), in 431 it is absent; by base BLL 229, MXFU 102, MXFL 59, MXDI 58, MXDB 48, XMES 40, AGH 34, ENFUN 31, ENGJ 30 …** The gold `h3` vs Claude `p` / none / `ol` residue (187 boxes) is a different class (the title lost or demoted), recorded.
- **§1b authority:** KB level 1 — 01F `activity_heading` → `<h3>Activity heading text</h3>` within the activity; the instruction paragraph is activity-level prose; the widget follows. The gold agrees on 2605 boxes and on the 958 of the class.

### 4. THE MECHANISM (ENGINE + data)

- **InteractiveScanner — the "activity WITHOUT a widget keyword but WITH a data table" path** (data `BoundaryBank._meta.opener_rule.unclassified_activity_lead` {enabled, env `UNCLASSLEAD_OFF`}): for a NUMBERED opener (`[Activity 1A] …` — the number is what makes the span the box's own opener; an unnumbered `[interactive activity] drag and drop …` span nested inside a numbered box, MXFU201's shape, keeps the member form), the items after it up to the first TABLE — black runs, ELEMENT tags ([body] / media), instruction spans; a heading tag only as the lead's FIRST item — become `bundle.activityLeadItems`, the opener becomes `bundle.activityOwner`, and `#swallowMembers` starts at that table. A lead that OPENS with a heading tag (`[Activity N]` + `[h4] What is the value?` + prose + a type-and-check table — MXFUN01, MXFL203, AGH1008) keeps the member form: there the heading already terminated the old walk, so the table rendered free and the heading + prose as ordinary content, and owning it measured worse on both the skeleton and compare_structure. The marking loop and the converter's existing owner rendering do the rest.
- **ContentConverter — the owned-bundle lead rendering**, for `_unclassLead` bundles only: a MEDIA tail (`[image] url`, `[video] url`, a `[button]` label) or a URL-like run is never promoted to the box's `<h3>` (buffered as prose); a title arriving after buffered prose flushes the prose first. Everything else keeps the normal path's rule — the first heading / text line is the title (MXDI101 1A's plain-text «Counting in twos»).
- Env `UNCLASSLEAD_OFF` = the opener collected as the first member, as before — byte-identical on all 416 (the in-memory probe, 2110 / 2110).

### 5. THE PROOF

- **The in-memory probe over all 416 (`_r362_probe.cjs`, 4 shards):** `UNCLASSLEAD_OFF=1` — every page byte-identical to the r361 corpus; ON (the final code) — 158 modules / 291 paired pages changed, scored against the r361 pages page by page: up 200, down 89, +399pp-pages; compare_structure over the changed modules exact 2954 → 2954, matched 3355 → 3355 (the first draft's owner form on heading-led leads had cost 46 exact matches and was measured out — `_r362_cs_offon.json`, `_r362_off/`, `_r362_on2/`, `_r362_on3/`).
- **FULL regeneration** (`_r362_fullship_par.sh`, 36 batches, all rc 0): `_stalecheck.sh` 0 stale.
- **Gates (`_r362_gates.log`, every RESULT ✓, 0 ✗, pairs skipped 0):** **skeleton SCAFFOLD 52.0925 → 52.2658 % (+0.173pp; 287 movers — 200 up, 87 down; pp-sum +364), ≥50 1096 → 1098, ≥75 161 → 168, ≥90 14 EXACT, RAW 36.780 → 36.944 %, pairs 1955 → 1956 (the page pairing of MXDI101 / MXFL101 shifted with their content — MXDI101_1_0 / _1_7 and MXFL101_2_1 / _3_1 in, MXDI101_1_2 / MXFL101_3_0 / _3_6 out)**; the dips NAMED — ENGR302_1_0 58.3 → 40.0, CEDT301_6_0 24.5 → 7.4, BLL224_1_0 62.6 → 47.7, MXDI102_1_0 40.0 → 30.1, ENGR202_5_0 48.8 → 39.8, MXFL204_2_0 35.3 → 26.5, XMES102_1_0 51.9 → 44.4, BLL145_1_0 57.0 → 49.7 …: on every one inspected the changed boxes now open `h3, p, capture` exactly as the gold's `h3, p, widget`, and the page score falls through difflib's re-alignment of the long stretch after them (BLL224 1A / 1E, ENGR202 5A, MXFL204 2A) or through content the gold renders in another form (ENGJ302 4A's poem as a zoomable image vs Claude's free paragraphs). **compare_structure exact 11645 / diff-order 1052 / EXTRA 175 / missing 617 / row-wrap 23 / other 197 — all EXACT**; **body_compare: over-capture 43 → 42 (better), runaway 4, EMPTY interactive container 136 → 151 and pages-with-any-flag 182 → 196 — NAMED: 16 pages (BLL114 / 120 / 121 / 125 / 131 / 132 / 156 / 157 / 160, CEDT208, MXFL101 ×5, XLP03) whose capture text fell under the 40-character EMPTY heuristic because the title and the instruction paragraph now render OUTSIDE the box (BLL114_1_0: 697 → 6 characters in the box, the widget's members — an audio / image table — unchanged); the box count, the over-capture share and the lost-block counts of those pages are unchanged, so the heuristic moved, not the content**; structural defect clean 98.9 % (2080 / 2103, 26 occ / 23 pages) EXACT; tags 9557 / 9557; every widget verifier ✓, entry parity PASS.

**Ledger:** FULL regeneration of all 416, `_ship_ledger.py record-full --round 362` (counter 0) · selftests GREEN, fast-loop baseline, content manifest, feature index refreshed (`_r362_postship.sh`) · `DIFF_QUEUE.md` re-mined on the r362 corpus (#535 MISSING `h3` 478 → 394 pages, #533 MISSING `p` 760 → 705) · KB delta: none (01F states the form).

"""
if "round 362, build 260619.33" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r362 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.33"' not in s:
    old = '\tstatic AppVersion = "260619.32";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, '\t// ROUND 362 (260619.33): the unclassified activity keeps its title heading and lead prose free — the numbered `[Activity N] Title` opener becomes the bundle\'s activityOwner and the prose before the first table its lead (KB 01F activity_heading h3 + the instruction p, then the hand-off box); data BoundaryBank._meta.opener_rule.unclassified_activity_lead, env UNCLASSLEAD_OFF; the diff miner\'s activity classes #542 / #535 / #533.\n\tstatic AppVersion = "260619.33";')
    wr(P, s); print("Config.js: 260619.33")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "ROUND 362 BASELINE" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 361 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 362 BASELINE (the unclassified activity keeps its title heading and lead prose free — 158 modules; FULL regeneration of all 416, ledger 0): SCAFFOLD mean 52.266% / >=50% 1098 / >=75% 168 / >=90% 14 / RAW 36.944% @ 1956 pairs, pairs skipped 0 — hold-or-improve; 287 movers (200 up, 87 down — the dips named in the r362 changelog: re-alignment after boxes that now open h3 + p + capture like the gold).** Previous — ROUND 361 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `SECTIONNAV_OFF` | 361 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `UNCLASSLEAD_OFF` | 362 | **THE UNCLASSIFIED ACTIVITY KEEPS ITS TITLE HEADING AND LEAD PROSE FREE** (the autonomous loop's session 19 Round 6 — the DIFF MINER's activity classes #542 / #535 / #533; KB 01F `activity_heading`). InteractiveScanner's \"activity without a widget keyword but with a data table\" path used to collect the `[Activity N] Title` opener as the bundle's first member, so the whole activity — title and instruction paragraph included — became the placeholder box (958 boxes / 535 pages measured, `outputs/_measure_r362_actlead.py`). Now a NUMBERED opener becomes `bundle.activityOwner`, the prose before the first table (a heading tag only as the lead's first item) its `activityLeadItems`, and the members start at the table — the normal path's owner form, which ContentConverter renders as `<h3>` title + lead prose + the hand-off box. Guards: an unnumbered nested `[interactive activity]` span and a lead that opens with a heading tag keep the member form (both measured worse the other way); in the converter a media / URL tail is never promoted to the title. Data `Interactive_Boundary_ChildTag_Bank._meta.opener_rule.unclassified_activity_lead`. OFF = byte-identical on all 416. body_compare's EMPTY-container heuristic rose 136 → 151 with the text now outside the box (named). |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.32` (round 361"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.33` (round 362 — **the unclassified activity keeps its title heading and lead prose free** (the numbered `[Activity N] Title` opener → `activityOwner`, the prose before the first table → `activityLeadItems`; KB 01F `<h3>` title + instruction `<p>` + the hand-off box; InteractiveScanner + the converter's lead rendering; data `BoundaryBank._meta.opener_rule.unclassified_activity_lead`, env `UNCLASSLEAD_OFF`); the autonomous loop's session-19 Round 6, the DIFF MINER's activity classes #542 / #535 / #533; FULL regeneration of all 416, 158 modules / 291 pages changed; skeleton 52.093 → 52.266 % (+0.173pp, 200 up / 87 down named), ≥75 161 → 168; compare_structure EXACT; body_compare over-capture 43 → 42, EMPTY heuristic 136 → 151 named; ledger FULL, counter 0).\n"
             + OLD14)
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r362" not in d["skeleton"]:
    d["skeleton"]["mean_scaffold_pct"] = 52.266
    d["skeleton"]["raw_mean_pct"] = 36.944
    d["skeleton"]["pages_ge_50"] = 1098
    d["skeleton"]["pages_ge_75"] = 168
    d["skeleton"]["pairs"] = 1956
    d["skeleton"]["_note_r362"] = "Round 362: the unclassified activity keeps its title heading and lead prose free — SCAFFOLD 52.0925 → 52.2658 (+0.173pp; 287 movers, 200 up / 87 down, the dips named in the changelog), ≥50 1096 → 1098, ≥75 161 → 168, ≥90 14, RAW 36.780 → 36.944; pairs 1955 → 1956 (MXDI101 / MXFL101 page pairing shifted with their content). Hold-or-improve from here."
    bc = d["body_compare"]
    bc["any_breakdown"] = 196; bc["over_capture"] = 42; bc["runaway"] = 4; bc["empty_container"] = 151
    bc["_note_r362"] = "Round 362: over_capture 43 → 42 (better); EMPTY interactive container 136 → 151 and any_breakdown 182 → 196 — 16 pages (BLL114 / 120 / 121 / 125 / 131 / 132 / 156 / 157 / 160, CEDT208, MXFL101 ×5, XLP03) whose capture text fell under the 40-character EMPTY heuristic because the activity's title and instruction paragraph now render OUTSIDE the hand-off box (the class itself; the widget members — audio / image data tables — are unchanged, the box counts and lost-block counts identical). Hold-or-improve from 196 / 42 / 4 / 151."
    d["_meta"]["build"] = "260619.33"; d["_meta"]["round"] = 362
    d["_meta"]["_note_r362"] = "Round 362: the unclassified activity lead — skeleton +0.173pp (≥75 +7), compare_structure EXACT, body_compare over-capture better and its EMPTY heuristic named; FULL regeneration of all 416, 158 modules / 291 pages; ledger FULL (counter 0)."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r362")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_r362_finalise.py" not in s:
    A = "| `_r361_items.cjs`"
    assert s.count(A) == 1, "README anchor"
    ROWS = ("| `_measure_r362_actlead.py` / `_r362_actlead.{json,log}` / `_r362_splice.py` / `_r362_probe.cjs` / `_r362_probe_run.sh` / `_r362_probe_{off,on}_0*.log` / `_r362_off/` (the r361 pages of the changed modules, saved for the per-module gate comparison) / `_r362_on2/` / `_r362_on3/` / `_r362_cs_offon.json` / `_r362_onscore.json` / `_r362_on3score.json` / `_r362_changed_modules.txt` / `_r362_fullship_par.sh` / `_r362_fullship_run.sh` / `_r362_fullship_regen.log` / `_r362_gates.log` / `_r362_sk_full.log` / `_r362_sk_final.json` / `_r362_postship.sh` / `_r362_selftests.log` / `_r362_fastloop_snapshot.log` / `_r362_manifest_snapshot.log` / `_r362_ledger.log` / `_r362_index.log` / `_r362_miner.log` / `_r362_finalise.py` | `CONVERTER_V2/outputs/` | Session 19 Round 6 (engine r362 — the diff miner's activity classes #542 / #535 / #533: the unclassified activity keeps its title heading and lead prose free) — the box-lead census (4024 number-paired boxes), the anchored splice, the in-memory OFF / ON probes over all 416 (three drafts, each measured on the skeleton AND compare_structure per module against the saved r361 pages), the full regeneration, the gate suite, the fresh skeleton score, the post-ship housekeeping, the miner re-run, the finalise |\n")
    s = s.replace(A, ROWS + A, 1)
    wr(P, s); print("README: r362 rows")
print("finalise done")
