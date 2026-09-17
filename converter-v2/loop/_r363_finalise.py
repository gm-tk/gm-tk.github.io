#!/usr/bin/env python3
"""ROUND 363 (loop session 20 Round 7 — the heading-tag-led unclassified activity takes the owner form) — finalise:
changelog, AppVersion (260619.33 → 260619.34), CLAUDE.md §9 / §11 (UNCLASSHEAD_OFF row) / §14, gate_baseline.json,
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
ENTRY = """## 2026-09-17 (round 363, build 260619.34) — THE HEADING-TAG-LED UNCLASSIFIED ACTIVITY TAKES THE OWNER FORM: a bare `[Activity N]` whose next line is `[Activity Heading] Title` / `[Activity heading H3] Title` / `[Heading] Title` keeps the gold's `<h3>` title and lead prose free of the hand-off capture — the r362 guard corrected (the autonomous loop's session 20, Round 7)

### 1. WHAT CHANGED, IN ONE LINE

**r362 kept the OLD member form for any unclassified activity whose lead OPENS with a heading tag, on the premise that "the heading already terminated the old walk so the table rendered FREE" — true for the tags `#swallowMembers` terminates on (h2–h5) and FALSE for the KB's own `activity_heading` tag (and `heading`, `h1`, `h6`), which the walk swallows whole: title, prose and table into the placeholder. Now only a lead that opens with a member-form tag (h2–h5) keeps the member form; every other heading-tag-led lead takes the owner form (opener → `activityOwner`, the heading + prose → `activityLeadItems`, members from the first table), and the converter's existing lead rendering promotes the heading item to the box's `<h3>`.** 76 pages / 31 modules change; skeleton +0.081pp.

### 2. THE EVIDENCE (docx → human → Claude)

- **ENFUN02 overview, activity 1** — WT `[Activity 1]` / `[Activity Heading] What do you think about?` / `[body] Look at this picture.` / two bullets / `Click the sliders to see some ideas …` / a TABLE (an `[image]` cell); gold `<div class="activity interactive" number="1A"><div class="row"><div class="col-12"><h3>What do you think about?</h3><p>Look at this picture. </p><ul><li>…</li><li>…</li></ul><img …>` then the widget; Claude (r362) `<div class="activity" number="1A">…<div class="cv2-interactive …"><span>ENFUN02-INT-00-01-unclassified</span> … <p>What do you think about?</p><p>Look at this picture.</p><ul>…` — title, prose and list all inside the capture. Now: `<h3>What do you think about?</h3><p>Look at this picture.</p><ul>…</ul><p>Click the sliders …</p>` then the r229 ENFUN inner widget row with the capture (the gold's shape).
- **ENGC201 lesson 6, 6A** — WT `[Activity 6A]` / `[Activity heading H3] Which sound?` / `[body] …`; gold `<h3>Which sound?</h3>` first. **MXFU402 lesson 2, 2C** — WT `[Activity 2C]` / `[Heading] Roll and record – experimental probability` / …; gold `<h3>Roll and record – experimental probability</h3>` first; Claude (r362) the capture with `<p>Roll and record …</p>` inside.
- **The live item stream** (`outputs/_r363b_items.cjs` on ENGC201): `[Activity 2A]` → tag `activity` CONTAINER_OPEN, then `[Activity heading H3] Expanding contractions` → tag `activity heading` ELEMENT, then `[body] …` — all `consumedBy` the same bundle.

### 3. THE MEASUREMENT (before coding)

- **The r362 residue re-measured on the r362 corpus** (`_measure_r362_actlead.py` re-run): 574 gold-`h3` / Claude-widget boxes, **227 with the gold's title INSIDE Claude's capture**; decomposed by the WT line that carries the title (`outputs/_r363_swallowed.py`): **112 sit on a TAG line** — 40 `[Activity Heading] T` (16 modules), 12 `[Activity heading H3] T` (6), 12 `[Heading] T` (MXFU402), 4 `[H3] T`, 29 with the widget type INSIDE the activity tag (`[Activity 3A – self-marking drag and drop] T`, 7 modules / 25 pages — a separate class, queued), 7 super-content-first (the supervisor row hoisted above the title — 6 modules, queued); 37 in no WT line (class C), 29 plain lines, 14 plain-line-after-tag.
- **The class corpus-wide** (`outputs/_measure_r363_headled.py` → `_r363_headled.{json,log}`): a BARE numbered `[Activity N]` opener whose next non-blank WT line is a heading TAG with a title — **721 paired boxes** (`[H3]` 347, `[Activity Heading]` 184, `[Activity heading H3]` 121, `[H2]` 32, `[Heading]` 30). **The gold opens the box with `<h3>Title</h3>` at 0.74 overall — `activity heading` 0.83, `activity heading h3` 0.92, `heading` 0.90; Standard 0.77, English 0.82** (the `[H3]` form 0.64, where Claude is already at 0.72 — no class). The MISS (gold h3-first, Claude's title inside a capture): **69 boxes / 53 pages / 23 modules** (+ ≈ 80 rows the probe could not pair by number — a bare `[Activity 1]` the r325 phase numbering ships as `1A`: ENFUN02 / ENFUN05's `[Activity Heading]` boxes are in the swallowed set above). Body floor 20 pages met; structure-derivable; consensus ≥ 0.60 in every group.
- **§1b authority:** KB level 1 — 01F `activity_heading` → `<h3>Activity heading text</h3>` within the activity; the instruction paragraph is activity-level prose; the widget follows.

### 4. THE MECHANISM (ENGINE + data)

- **InteractiveScanner — the unclassified-activity path, the r362 guard** (data `BoundaryBank._meta.opener_rule.unclassified_activity_lead.heading_led_owner` {enabled, env `UNCLASSHEAD_OFF`, member_form_tags [h2, h3, h4, h5]}): `_ualLeadHeads` — the test that sends a heading-led lead to the OLD member form — now counts a heading item only when its tag is in `member_form_tags` (the tags `#swallowMembers` actually terminates on — the r362-measured MXFUN01 / MXFL203 / AGH1008 `[h4]` shape, byte-identical). A lead opening with `activity heading` / `heading` / `h1` / `h6` takes the OWNER form. No converter change: `addLead` already promotes a `["h1","h2","h3","h4","h5","heading","activity heading"]` lead item to the `<h3>`.
- Env `UNCLASSHEAD_OFF` = r362's guard — byte-identical on all 416 (the in-memory probe, 2110 / 2110).

### 5. THE PROOF

- **The in-memory probe over all 416 (`_r363_probe.cjs` = the r362 probe, 4 shards, `_r363_probe_run.sh`):** `UNCLASSHEAD_OFF=1` — every page byte-identical to the r362 corpus (2110 / 2110); ON — **76 pages / 31 modules** changed (ENFUN01–05 / 07–09, ENGC201 / 202 / 301 / 302 / 401, ENGI103 / 302 / 303 / 401, ENGJ201, ENGR101 / 201 / 301, ENGS102 / 201 / 202 / 301 / 401, MXFU402, OSAH501, OSAI301, OSOH301, OSOH401); the ON pages saved (`_r363_on/`) and scored page by page against the r362 pages with the gate's own `match()` (`_r363_pagescore.py` → `_r363_onscore.json`): **up 59 / down 17, pp-sum +158.8**.
- **FULL regeneration** (`_r363_fullship_par.sh`, 36 batches, all rc 0, 4 m 50 s): `_content_manifest.py diff` → 76 pages / 31 modules changed, 0 added / 0 removed = the probe's set exactly; the regenerated pages byte-identical to the probe's ON pages (177 / 177); `fresh --affected` (the 31) → 0 truly stale, the other 382 byte-identical (TRR104 / 105 / 115 have no Writers Template and no pages — the manifest's 413).
- **Gates (`_r363_gates.log`, every RESULT ✓, 0 ✗, pairs skipped 0):** **skeleton SCAFFOLD 52.2658 → 52.3470 % (+0.081pp; 76 movers — 59 up, 17 down), ≥50 1098 → 1103, ≥75 168 → 170, ≥90 14 → 15, RAW 36.944 → 37.021 %, pairs 1956**; compare_structure exact 11645 / EXTRA 175 / missing 617 / row-wrap 23 / other 197, matched 13709 — ALL EXACT; body_compare over-capture 42 → 41 (better), runaway 4, EMPTY 151, any-flag 196 → 195 (better); structural defect 98.9 % / 26 occ / 23 pages EXACT; tags 9557 / 9557; flipCard divergence 0, speechBubble, modal, MTK shell, math, menu-label, dragAndDrop verifiers ✓. **Dips NAMED:** OSAI301_2_0 73.8 → 68.6, ENGI302_4_0 49.1 → 43.9, OSOH401_3_0 55.7 → 52.2 — each a single `<p>` → `<h3>` change on the box's opener (the gold HAS the `<h3>`: OSAI301 2A `<h3>Applying AI risks and benefits</h3>`, ENGI302 4A `<h3>Characters in Cinderella</h3>`) that re-aligns difflib's whole-page match; the other 14 dips are under 1.3pp of the same kind. Gains: ENFUN07_0_0 22.9 → 39.9, ENGC202_1_0 47.7 → 63.3, ENFUN05_0_0 30.5 → 43.1, MXFU402_3_0 30.7 → 42.5.

**Ledger:** FULL regeneration of all 416, `_ship_ledger.py record-full --round 363` (counter 0) · selftests GREEN, fast-loop baseline, content manifest, feature index refreshed (`_r363_postship.sh`) · `DIFF_QUEUE.md` re-mined on the r363 corpus · AppVersion 260619.34 · CLAUDE.md §9 / §11 (`UNCLASSHEAD_OFF` | 363) / §14 · `gate_baseline.json` · loop README rows.

**Recorded, not chased (the r363 residue):** (a) the widget type INSIDE the activity tag — `[Activity 3A – self-marking drag and drop] Title` (29 boxes / 7 modules / 25 pages: MXEO301, MXFL301, MXFU301, MXDB302, ANZH203, ENGR102, ENGS302) — the classified path, the tail words swallowed as a `<p>` member; (b) the supervisor row hoisted above the box's title (7 boxes / 6 modules — BLL122 / 123 / 163 / 214, ENGR101 …; Chris's BLL110 finding 6); (c) 29 plain-line titles (the writer's bare first line) and 14 plain-line-after-tag; (d) 37 gold titles in no WT line — class C.

"""
if "round 363, build 260619.34" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r363 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.34"' not in s:
    old = '\tstatic AppVersion = "260619.33";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, '\t// ROUND 363 (260619.34): the heading-tag-led unclassified activity takes the owner form — a bare `[Activity N]` + `[Activity Heading] Title` / `[Heading] Title` keeps the gold\'s <h3> title and lead prose free of the capture (the r362 guard scoped to the h2–h5 tags #swallowMembers terminates on; data unclassified_activity_lead.heading_led_owner, env UNCLASSHEAD_OFF). 76 pages / 31 modules; skeleton +0.081pp.\n\tstatic AppVersion = "260619.34";')
    wr(P, s); print("Config.js: 260619.34")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "ROUND 363 BASELINE" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 362 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 363 BASELINE (the heading-tag-led unclassified activity takes the owner form — 31 modules; FULL regeneration of all 416, ledger 0): SCAFFOLD mean 52.347% / >=50% 1103 / >=75% 170 / >=90% 15 / RAW 37.021% @ 1956 pairs, pairs skipped 0 — hold-or-improve; 76 movers (59 up, 17 down — the dips named in the r363 changelog: a single `<p>` → `<h3>` on a box's opener re-aligning difflib's whole-page match).** Previous — "
             + OLD9[len("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **"):])
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `UNCLASSLEAD_OFF` | 362 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `UNCLASSHEAD_OFF` | 363 | **THE HEADING-TAG-LED UNCLASSIFIED ACTIVITY TAKES THE OWNER FORM** (the autonomous loop's session 20 Round 7 — the r362 residue decomposed; KB 01F `activity_heading`). r362's guard kept the OLD member form for any lead opening with a heading tag, on the premise that the heading terminated the old walk; `#swallowMembers` terminates only on h2–h5, so an `[Activity Heading]` / `[Activity heading H3]` / `[Heading]` lead was swallowed whole — title, prose and table into the capture. Now only a `member_form_tags` (h2–h5) heading keeps the member form; the rest take the owner form (opener → `activityOwner`, heading + prose → `activityLeadItems`, members from the first table) and the converter's lead rendering promotes the heading item to the `<h3>`. Gold h3-first 0.83–0.92 on the tag forms (721 boxes measured); 76 pages / 31 modules; skeleton +0.081pp, ≥90 14 → 15, body_compare over-capture 42 → 41. Data `BoundaryBank._meta.opener_rule.unclassified_activity_lead.heading_led_owner`. OFF = r362's guard, byte-identical. |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.33` (round 362"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.34` (round 363 — **the heading-tag-led unclassified activity takes the owner form** (a bare `[Activity N]` + `[Activity Heading] Title` / `[Activity heading H3] Title` / `[Heading] Title` → the gold's `<h3>` title + lead prose free of the capture; the r362 guard scoped to the h2–h5 tags `#swallowMembers` terminates on; InteractiveScanner only; data `BoundaryBank._meta.opener_rule.unclassified_activity_lead.heading_led_owner`, env `UNCLASSHEAD_OFF`); the autonomous loop's session-20 Round 7, the r362 residue decomposed; 76 pages / 31 modules; FULL regeneration; skeleton 52.266 → 52.347 %, ≥50 1103, ≥75 170, ≥90 15, RAW 37.021 %, compare_structure EXACT, body_compare over-capture 41). Previous: "
             + OLD14[len("- **Build:** "):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r363" not in d["skeleton"]:
    d["skeleton"]["mean_scaffold_pct"] = 52.347
    d["skeleton"]["raw_mean_pct"] = 37.021
    d["skeleton"]["pages_ge_50"] = 1103
    d["skeleton"]["pages_ge_75"] = 170
    d["skeleton"]["pages_ge_90"] = 15
    d["skeleton"]["pairs"] = 1956
    d["skeleton"]["_note_r363"] = "Round 363: the heading-tag-led unclassified activity takes the owner form — SCAFFOLD 52.2658 → 52.3470 (+0.081pp; 76 movers, 59 up / 17 down, the dips named in the changelog — a single <p> → <h3> on a box's opener re-aligning the page), ≥50 1098 → 1103, ≥75 168 → 170, ≥90 14 → 15, RAW 36.944 → 37.021; pairs 1956. Hold-or-improve from here."
    bc = d["body_compare"]
    bc["any_breakdown"] = 195; bc["over_capture"] = 41; bc["runaway"] = 4; bc["empty_container"] = 151
    bc["_note_r363"] = "Round 363: over_capture 42 → 41 and any_breakdown 196 → 195 (better — a title + prose that used to sit inside a capture now render free); runaway 4 / EMPTY 151 EXACT. Hold-or-improve from 195 / 41 / 4 / 151."
    d["_meta"]["build"] = "260619.34"; d["_meta"]["round"] = 363
    d["_meta"]["_note_r363"] = "Round 363: the heading-tag-led activity lead — skeleton +0.081pp (≥50 +5, ≥75 +2, ≥90 +1), compare_structure EXACT, body_compare over-capture better; FULL regeneration of all 416, 31 modules / 76 pages; ledger FULL (counter 0)."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r363")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_r363_finalise.py" not in s:
    A = "| `_measure_r362_actlead.py`"
    assert s.count(A) == 1, "README anchor"
    ROWS = ("| `_measure_r363_lessonmenu.py` / `_r363_lessonmenu.{json,log}` / `_r363_swallowed.py` / `_measure_r363_headled.py` / `_r363_headled.{json,log}` / `_r363b_items.cjs` / `_r363_probe.cjs` / `_r363_probe_run.sh` / `_r363_shard[0-3].txt` / `_r363_probe_{OFF,ON}_[0-3].log` / `_r363_on/` (the probe's ON pages of the 31 changed modules) / `_r363_pagescore.py` / `_r363_onscore.json` / `_r363_changed_modules.txt` / `_r363_fullship_run.sh` / `_r363_fullship_par.sh` / `_r363_batch_*.{sh,log}` / `_r363_gates.log` / `_r363_sk_final.json` / `_r363_movers.py` / `_r363_finalise.py` / `_r363_postship.sh` | Session 20 · Round 7 (engine r363): the heading-tag-led unclassified activity takes the owner form. The PICK pass first measured the queued chrome items — the CED `[Tab N]` label-list crumbs dialect (2 modules, below floor), F11 `module-head-buttons` (the KB 01B `[Lesson Overview]` rule holds at 0.94 in the gold and 0.93 in Claude; the derivable miss 17 pages / 6 modules, below floor) — then decomposed the r362 residue (227 swallowed titles → 112 on a tag line → the `[Activity Heading]` / `[Heading]` sub-class), measured the class corpus-wide (721 boxes, gold h3-first 0.83–0.92), probed OFF (2110 / 2110) and ON (76 pages / 31 modules), regenerated in full, gated (skeleton +0.081pp, ≥90 14 → 15, over-capture 42 → 41, every other gate EXACT). |\n"
            + A)
    s = s.replace(A, ROWS + A, 1)
    wr(P, s); print("README: r363 rows")
print("finalise done")
