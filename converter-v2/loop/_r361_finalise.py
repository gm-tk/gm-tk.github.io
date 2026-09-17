#!/usr/bin/env python3
"""ROUND 361 (loop session 19 Round 5 — the EXPlore "Navigation with N sections" inquiry dialect) — finalise: changelog,
AppVersion (260619.31 → 260619.32), CLAUDE.md §9 / §11 (SECTIONNAV_OFF row) / §14, gate_baseline.json, loop/README.md.
Idempotent; LF via wr()."""
import io, os, json
ROOT = r"C:\Users\Gavin\TeKura\FINAL_MODULE_DATA"
PF = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)

CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)" + chr(10) + chr(10)
ENTRY = """## 2026-09-17 (round 361, build 260619.32) — THE EXPlore "NAVIGATION WITH N SECTIONS" INQUIRY DIALECT: the writer's one-line `[Side / Tab Navigation with 6 sections: Learner, Communicator, … and Innovator]` instruction plus its section openers (`[section N] Label`, `TAB NAV N: Label` lines, or a top-level heading naming the label) become the KB 06 §3.4 `div.crumbs` + `div.inquiryPanel` scaffold — `PanelsBuilder.detectInquirySections` + a `sectionMode` of `inquiryPanels`, the body-loop sentinel split beside the r102 one, data `inquiry_tabs.section_nav`, env `SECTIONNAV_OFF`; the autonomous loop's session-19 Round 5, the DIFF MINER's crumbs fact F23 (its largest derivable dialect: EXPFUN02 / 03 / 04 / 05); **FULL regeneration of all 416 (36 batches, all rc 0), 4 modules / 4 pages changed; skeleton SCAFFOLD 52.076 → 52.093 % (+0.016pp; 4 movers, all up, no dips), compare_structure exact wrapper chain 11617 → 11645, every other gate EXACT; ledger FULL (counter 0)**

### 1. WHAT CHANGED, IN ONE LINE

**Four single-page EXPlore Inquiry modules declared their whole crumb trail in one writer instruction and opened each section with a marker the engine had no grammar for — so the instruction shipped as a red Writers Note, the `[section N]` tags as "Orphan sub-tag" notes with a stray `<p>Learner</p>`, the `TAB NAV` lines as paragraphs and the body flat (every body skeleton line one indent short of the gold's: 7–9 % SCAFFOLD); now the page carries the seven crumbs («Intro» + the six labels, the first `showing`), the seven `inquiryPanel`s and the `inquiry container-fluid` body class the gold and KB 06 §3.4 build.**

### 2. THE EVIDENCE (docx → human → Claude)

- **EXPFUN02** — WT line 83 `[Side Navigation with 6 sections: Learner, Communicator, Scientist, Social Scientist, Mathematician and Innovator]`, 87 `[H3] Introduction` … 121 `[End page]`, 123 `[section 1] Learner`, 306 `[Section 2] Communicator`, 504 `[H2] Think like a scientist`, 681 `[H1] Think like a social scientist`, 859 `[H1] Think like a mathematician`, 1037 `[H1] Think like an Innovator`; gold `EXPFUN02_0.0.html` `<body class="inquiry container-fluid">` … `<div id="body"><div class="crumbs"><div class="showing" crumb="1"><p>Intro</p></div><div crumb="2"><p>Learner</p></div> … <div crumb="7"><p>Innovator</p></div></div><div class="inquiryPanel showing" rel="1">` …; Claude before: `<body class="container-fluid">`, `Writers Note: [Side Navigation with 6 sections: …]`, `Red Flag: Orphan sub-tag [shape n] outside an interactive …` + `<p>Learner</p>`, flat rows; after: the gold's scaffold, seven panels.
- **EXPFUN04** — WT 59 `[Tab Navigation with 6 sections: …]`, 61 `TAB NAV 1: Introduction`, 85 `TAB NAV 2: Learner` … 746 `TAB NAV 7: Innovator`, `[End Tab]` after each; gold 7 crumbs / 7 panels; Claude before `<p>TAB NAV 2: Learner</p>` paragraphs in a flat body; after the scaffold. **EXPFUN03 / 05** the same grammar with `TAB NAV: Intro` / `TAB NAV 1: Introduction` and the first section line typed in BLACK (`TAB NAV 1: Learner`) inside a merged black run.

### 3. THE MEASUREMENT (before coding — the DIFF MINER's F23 (13 modules) decomposed by WT grammar; `outputs/_r361_items.cjs` for the live item shapes)

- **The 13 crumb-less pages split into dialects:** (A) the EXPlore section-navigation family — EXPFUN02 / 03 / 04 / 05, the only four WTs in the corpus carrying "Navigation with N sections" (census of every parsed WT; the `TAB NAV` phrase elsewhere is HPFUN / TWHA / XDLS one-liners with no instruction — no over-fire population); (B) the CED labelled in-stream `[Tab N] Label` openers with `[MODULE INTRODUCTION]` — CEDT207 / CEDT208 / CEDW201 (r108 measured them, deferred; a second dialect round); (C) not derivable — BLL240 and CEDK501 (media-list-only WTs), CEDT104 (`[Lesson N content]` panels, one module), TWHA905 / TWHK901 (bold heading lists, no markers), EXIP901 (the EX multi-file `[New side tab]` family, r112's plan-deferred structure).
- **The live item shapes:** the instruction is an unknown `tag` item (02) or a `tab n` SUBTAG item (03–05 — which is why r112's `_emptyOpeners` counted it); `[section N]` normalises to a `shape n` SUBTAG with the label in `blackAfter`; the `TAB NAV` lines are red `tag` items (`TAB NAV N:` + the label in `blackAfter`, or the whole line in the text) or plain `black` runs — and a black run reaches the body loop MERGED with its neighbours ("Be a Learner\\nBe a Communicator\\n…\\nTAB NAV 1: Learner"), then gathered whole by the preceding `[image]`.
- **§1b authority:** KB level 1 — 06 §3.4 "Navigation: Breadcrumb/tab-based — `div.crumbs` containing crumb tabs, then `div.inquiryPanel[rel]` content panels. First panel has `class="inquiryPanel showing"` and first crumb has `class="showing"`"; the gold agrees 4 / 4. No override.

### 4. THE MECHANISM (ENGINE + data — the r100 / r102 / r111 PanelsBuilder dialect pattern)

- **`PanelsBuilder.detectInquirySections(page, tpl)`** (data `body_region.inquiry_tabs.section_nav` {enabled, env `SECTIONNAV_OFF`, intro_label "Intro", intro_words, min_sections 3, heading_openers [h1, h2]}): finds the instruction (`(side|tab) navigation with N sections: <list>`), splits the labels on commas / "and", then walks the items after it matching each expected label IN ORDER to the next opener — a `[section N]` tag (consumed), a `TAB NAV [N]: label` line (consumed; the first one whose label is Intro / Introduction opens the intro panel; a black run is tested LINE by line and recorded by line index), or a top-level unconsumed h1 / h2 heading whose text contains the label (kept as the panel's first heading). Fires only when every label found an opener. With no explicit intro opener the instruction item itself opens the intro panel. Runs on the BODY partition (`{ items: bodyItems }`) so its flags land on the objects the loop visits; single-file pages only, never alongside the BLL / heading-label / CED modes.
- **ContentConverter:** a pre-pass cuts a merged black run at a flagged LINE into black(before) + a non-black `{type:"inqsection"}` marker + black(after) — the phase-text pre-pass's own cut, which stops every black-run gatherer; in the body loop (beside the r102 `_inquiryCrumb` skip) a flagged opener closes any open activity, `breakRow()`s and pushes the `INQ_SENTINEL` (the r102 `[page N]` split verbatim), and a consumed opener renders nothing. `inquiryPanels` gains `sectionMode`: segment 0 — the content BEFORE the first sentinel (the overview's learning-intention rows, the r359 q2 residue) — stays OUTSIDE the scaffold; then N+1 unified crumbs (page_split `crumb_item`, the first `showing`) and N+1 panels (page_split `panel_open`, the first `showing`). `inquiryActive` includes the mode → the r107 `body_class_requires_build` stamps `inquiry container-fluid`.

### 5. THE PROOF

- **The in-memory probe over all 416 (`_r361_probe.cjs`, 4 shards):** `SECTIONNAV_OFF=1` — every one of the 2110 pages byte-identical to disk; ON — exactly 4 changed pages (EXPFUN02 / 03 / 04 / 05), each now 7 crumbs («Intro», Learner, Communicator, Scientist, Social Scientist, Mathematician, Innovator) + 7 `inquiryPanel`s, no Writers Note for the instruction, no orphan-sub-tag note, no `TAB NAV` paragraph.
- **FULL regeneration** (`_r361_fullship_par.sh`, 36 batches, all rc 0): `_stalecheck.sh` 0 stale; `_content_manifest.py changed` = the 4 exactly.
- **Gates (`_r361_gates.log`, every RESULT ✓, 0 ✗, pairs skipped 0):** **skeleton SCAFFOLD 52.0761 → 52.0925 % (+0.016pp; 4 movers, all up — EXPFUN04 6.85 → 19.53, EXPFUN02 8.12 → 18.36, EXPFUN03 9.09 → 15.15, EXPFUN05 6.68 → 9.64 — no dips), ≥50 1096 / ≥75 161 / ≥90 14 EXACT, RAW 36.766 → 36.780 %**; **compare_structure exact wrapper chain 11617 → 11645** (the crumbs / panel wrappers now match), EXTRA 175 / missing 617 EXACT; body_compare 182 EXACT; structural defect clean 98.9 % (2080 / 2103, 23 pages) EXACT; tags 9557 / 9557; every widget verifier ✓, entry parity PASS. The residue inside the panels (the gold's `speechBubble` row, its accordion placement, its h2 / h3 heading levels against Claude's h4 / h5, its per-row splits) is body content — the miner's activity / body queue, not this class.

**Ledger:** FULL regeneration of all 416, `_ship_ledger.py record-full --round 361` (counter 0) · selftests GREEN, fast-loop baseline, content manifest, feature index refreshed (`_r361_postship.sh`) · `DIFF_QUEUE.md` re-mined on the r361 corpus (F23 falls to 9 modules, below the floor) · KB delta: none (06 §3.4 states the form).

"""
if "round 361, build 260619.32" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r361 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.32"' not in s:
    old = '\tstatic AppVersion = "260619.31";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, '\t// ROUND 361 (260619.32): the EXPlore "Navigation with N sections" inquiry dialect — the writer\'s one-line section list + its openers become the KB 06 §3.4 crumbs + inquiryPanel scaffold (PanelsBuilder.detectInquirySections, inquiryPanels sectionMode; data inquiry_tabs.section_nav, env SECTIONNAV_OFF); the diff miner\'s crumbs fact F23.\n\tstatic AppVersion = "260619.32";')
    wr(P, s); print("Config.js: 260619.32")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "ROUND 361 BASELINE" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 360 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 361 BASELINE (the EXPlore \"Navigation with N sections\" inquiry dialect — crumbs + inquiryPanel scaffold on EXPFUN02–05; FULL regeneration of all 416, ledger 0): SCAFFOLD mean 52.093% / >=50% 1096 / >=75% 161 / >=90% 14 / RAW 36.780% @ 1955 pairs, pairs skipped 0 — hold-or-improve; 4 movers, all up, no dips.** Previous — ROUND 360 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| *(no new toggle)* | 360 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `SECTIONNAV_OFF` | 361 | **THE EXPlore \"NAVIGATION WITH N SECTIONS\" INQUIRY DIALECT** (the autonomous loop's session 19 Round 5 — the DIFF MINER's crumbs fact F23; KB 06 §3.4). `PanelsBuilder.detectInquirySections`: the writer's one-line `[Side / Tab Navigation with N sections: A, B, … and F]` instruction names the crumb trail; each section opens on a `[section N] Label` tag, a `TAB NAV N: Label` line (the first one Intro / Introduction opens the intro panel; a black run is matched line by line and cut by a pre-pass) or a top-level h1 / h2 heading naming the label — every label must find an opener. The body loop pushes the panel sentinel at each opener (the r102 split) and renders the consumed ones as nothing; `inquiryPanels` `sectionMode` keeps the content before the first sentinel outside the scaffold, then N+1 unified crumbs («Intro» + the list, the first showing) + N+1 panels. Data `body_region.inquiry_tabs.section_nav`. Fires on EXPFUN02 / 03 / 04 / 05 only (the corpus census); OFF = byte-identical on all 416. |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.31` (round 360"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.32` (round 361 — **the EXPlore \"Navigation with N sections\" inquiry dialect** (the writer's one-line section list + `[section N]` / `TAB NAV N:` / heading openers → the KB 06 §3.4 `div.crumbs` + `div.inquiryPanel` scaffold and the `inquiry container-fluid` body class; `PanelsBuilder.detectInquirySections`, `inquiryPanels` sectionMode, the body-loop sentinel split, data `inquiry_tabs.section_nav`, env `SECTIONNAV_OFF`); the autonomous loop's session-19 Round 5, the DIFF MINER's crumbs fact F23; FULL regeneration of all 416, 4 modules / 4 pages changed; skeleton 52.076 → 52.093 % (+0.016pp, 4 up, no dips), compare_structure exact 11617 → 11645, every other gate EXACT; ledger FULL, counter 0).\n"
             + OLD14)
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r361" not in d["skeleton"]:
    d["skeleton"]["mean_scaffold_pct"] = 52.093
    d["skeleton"]["raw_mean_pct"] = 36.780
    d["skeleton"]["_note_r361"] = "Round 361: the EXPlore section-navigation inquiry dialect (crumbs + inquiryPanel scaffold on EXPFUN02–05) — SCAFFOLD 52.0761 → 52.0925 (+0.016pp; 4 movers, all up, no dips), ≥50 1096 / ≥75 161 / ≥90 14 EXACT, RAW 36.766 → 36.780. Hold-or-improve from here."
    cs = d.get("compare_structure")
    if isinstance(cs, dict):
        for k in list(cs.keys()):
            if not k.startswith("_") and isinstance(cs[k], (int, float)) and cs[k] == 11617:
                cs[k] = 11645; cs["_note_r361"] = "Round 361: exact wrapper chain 11617 → 11645 (the EXPFUN02–05 crumbs / panel wrappers now match)."
    d["_meta"]["build"] = "260619.32"; d["_meta"]["round"] = 361
    d["_meta"]["_note_r361"] = "Round 361: the EXPlore section-navigation inquiry dialect — skeleton +0.016pp (no dips), compare_structure exact +28, every other gate EXACT; FULL regeneration of all 416, 4 modules / 4 pages; ledger FULL (counter 0)."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r361")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_r361_finalise.py" not in s:
    A = "| `_measure_r360_footer.py`"
    assert s.count(A) == 1, "README anchor"
    ROWS = ("| `_r361_items.cjs` / `_r361_keys.cjs` / `_r361_splice.py` / `_r361_probe.cjs` / `_r361_probe_run.sh` / `_r361_probe_{off,on}_0*.log` / `_r361_fullship_par.sh` / `_r361_fullship_run.sh` / `_r361_fullship_regen.log` / `_r361_gates.log` / `_r361_sk_full.log` / `_r361_sk_final.json` / `_r361_postship.sh` / `_r361_selftests.log` / `_r361_fastloop_snapshot.log` / `_r361_manifest_snapshot.log` / `_r361_ledger.log` / `_r361_index.log` / `_r361_miner.log` / `_r361_finalise.py` | `CONVERTER_V2/outputs/` | Session 19 Round 5 (engine r361 — the diff miner's crumbs fact F23: the EXPlore \"Navigation with N sections\" inquiry dialect → the KB 06 §3.4 crumbs + inquiryPanel scaffold on EXPFUN02–05) — the live item-stream dumps (the opener shapes, the merged black run), the anchored splice, the in-memory OFF / ON probe over all 416, the full regeneration, the gate suite, the fresh skeleton score, the post-ship housekeeping, the miner re-run, the finalise |\n")
    s = s.replace(A, ROWS + A, 1)
    wr(P, s); print("README: r361 rows")
print("finalise done")
