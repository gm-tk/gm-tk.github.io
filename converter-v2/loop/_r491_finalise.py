#!/usr/bin/env python3
"""ROUND 491 finalise (session 46 Round 1 — the accordion marker-cell table, ACCMARKTABLE_OFF + the r489 ride-along ACCBULLETLEAD_OFF). WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 491," not in sc[:4000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.53";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 490 BASELINE"; a11 = "| `LOWALTALERT_OFF` | 490 |"; a14 = "- **Build:** `260620.53` (round 490"
for a in (a9, a11, a14): assert so.count(a) == 1, a
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 491 IN FLIGHT — NOT PROVEN**", "- **No round in flight** (25 Sept 2026 08:45, session 45 STOPPED", "- LAST SHIPPED: **r490**",
          "- Before it: **r488**", "- Before them: **r487 → r467**", "- Plateau window (§4): **0 of 3** — r490", "- Standing facts: AppVersion **260620.53**",
          "## Round log", "**Next session starts with:**", "## Session 46 — Round 1 PICK (engine r491)", "- **(s45-r5) the carousel after r488:**"):
    find(p)

entry = """## 2026-09-25 (round 491, build 260620.54) — THE ACCORDION MARKER-CELL TABLE: an accordion laid out in a table whose cells carry the writer's OWN panel markers (`[Accordion N]` / `[Hn]` title, `[Accordion N text]` / `[drop down text N]` / `[Body]` body) builds its panels from those markers (+ the column-label row, + the bulleted bold lead) — 24 hand-off boxes → built accordions

### 1. WHAT CHANGED

**The find** (session 46 Round 1 — the D10-3 widget-build lane, the standing "accordion vocabulary batch" follow-up): `WHY_UNBUILT__accordion.md` (written at r306) ranked six builder items at 58 activities; none but item 1's prototype (s45's `_r489_accbullet_declined.patch`) had been taken. Re-measured on the current corpus (`_s46_r1_accdump.cjs` — every declined accordion bundle with its members and table rows, 8 shards in 43 s; `_s46_r1_accclass.py`): 294 un-built / 132 modules; **item 2 — the writer's panel markers INSIDE the table cells — 37 bundles / 27 pages / 23 modules**, grown past the 20-page floor by the intakes. The r278 D2 table reading takes a table one way (a short first cell = the heading) and refused every one of them; `_s46_goldloc.py` (the gold's container chain for each panel title) shows the human built the accordion from exactly those markers — PWY1009 1.2 / 2.0 / 3.2 (`div.accordion.accKeepOpen`), PWY1008 3.2, CEDK102 ×2, TEDC401 ×2, MXEX301 4.0, CEDR501 5.0, PWYWHA1.

**The fix** (`InteractiveBuilder.#accMarkerTablePanels`, tried as D5 in `#accResolvePanels` AFTER D1–D4 have all declined — every accordion that built before is byte-identical by construction; the table must be the widget, text parts may only precede it as the r289 lead): every cell becomes a stream of MARKERS (the red spans, read by data patterns) and black TEXT, and the grid pairs them — a cell that opens with a title marker opens a panel (the title is the marker's own payload or the next text); a cell that opens with body joins the panel still without text to its LEFT in the row, else the one ABOVE it in the column, else (one column) continues the previous panel. Four layouts fall out of the one rule: alternating title / text rows (PWY1009 1.3 — eight Acts; CEDK102), a row of titles over a row of texts paired by column (PWY1008 2.2 / 3.2, PWY1007 2.0 whose title cells also carry the panel picture), title cell beside body cell (XMES101 after its `Images | Instructions` label row, XMES202 whose head-less panels take their heading from the body's bulleted bold lead), one whole panel per cell (PWYWHA1's `[H3] **…** / [Dropdown information] …`). A body marker's number must agree with its title's; the writer's flip-card slip `[Accordion 8 front]` / `[Accordion 6 back]` reads as title / body; an image marker with a URL (on its own line or the next — SSOG105's `[Image] please use scroll image` / URL) is the panel image by the r278 name rule, without one an asset-request red note; a developer cue (`Dev team please add:`, `[CS note: …]`), an unbracketed red sentence of 6+ words (SSOG103's "Could the Coin images please be muddled up …") and words typed inside a body marker's own red span ("[Body text] Can this be placed onto the scroll please.") become red notes after the widget. ANY other red span — a hover trigger (CEDK102 #4), an `[Alert]` (MXEX301 4.0), a `[table]` (TEDC401 1.0), a `[hyperlink` (PWY1009 3.3), a speech-bubble spec (TEDC401 0.0) — keeps the honest box. **Item 3 rides along:** a first row of column labels (wholly red, or the label words) is peeled, and when the rest carries no marker the ordinary D2 reading runs on it with the marker table's 16-word heading limit (CHFUN01's `Heading [h4] | Content [body]` → the gold's six panels). **Item 1 rides along** (the s45 r489 prototype, unchanged): the D4 bold-lead reading accepts an optional leading bullet and a spaced dash separator as a fallback after the r278 reading (MXEX302 ×5, ENGS101, XGF9003, XLP05). Data `interactive_builders.accordion.panel_delimiters.marker_table` (env `ACCMARKTABLE_OFF`) and `.bullet_bold_lead` (env `ACCBULLETLEAD_OFF`).

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF (both toggles) 0 pages changed**; ON **19 pages / 15 modules** (+ their `_interactives.txt` hand-off lists). Regeneration + 12-module spot-check clean; **`scoped_ship.sh` PASS** (scoped #1 since the r490 FULL backstop).
- **24 accordions built, 0 lost** (the dump OFF → ON: 510 → 534 built): 13 marker tables (CEDK102 ×2, CHFUN01, PWY1007, PWY1008 ×2, PWY1009 ×2, PWYWHA1, SSOG103 4.0, XMES101 ×2, XMES202), 3 more marker tables the classifier filed elsewhere (SSOG103 1.0, SSOG105 1.0, SSCI104 3.0), 8 bulleted bold leads. **Coverage dashboard: accordion 510 → 534 built of 804, Still-a-box 294 → 270** (the §4 widget-build test: 24 ≥ 20).
- Against the gold (`_s46_r1_headcheck.py`, every new panel title located in the module's gold): ≈ 70 of 112 are gold accordion headings (58 matched verbatim + CHFUN01's five whose gold titles carry `ch-text` spans + SSOG103's four whose gold drops the writer's "1." numbering); the rest are the developer's substitutions the writer's tag outranks (A1): MXEX302's bullet leads → clickDrop buttons (24), XMES101 → a carousel (7), PWY1007 → flip cards (5), XGF9003 1.0 (4, mixed). `_verify_accordion.cjs` over the WHOLE accordion family (231 modules, 4 shards): **1,263 built panels across 180 modules, defect 0 — RESULT ✓**.

### 3. PROTECTED GATES

- Skeleton **55.3705 % → 55.3709 % @ 2491 (+0.0004pp)**, **RAW 39.285 → 39.321 % (+0.036)**; ≥50 1585, ≥75 277, ≥90 26 HELD; 3 movers, all in the affected set (2 up / 1 down): XMES101_6_0 +0.6, SSOG103_1_0 +0.5; **SSOG105_1_0 −0.2 NAMED** — its position-free overlap rises 125 → 126 (`_r491_companion.py`: an alignment artefact). A widget-build round is skeleton-blind by design (the hand-off box and the built accordion both collapse to one WIDGET line; A1 — judged on the widget's own verifier).
- compare_structure exact 16702 / EXTRA 198 / missing 878 / row-wrap 24 EXACT; body 238 / clean 2587 / 2633 / leak 75 / 46 EXACT; tags 9557 / 9557; every `run_all_gates.sh` verifier RESULT ✓; selftests 50 green / 0 fail; feature index GREEN; the miner 194 CANDIDATE. (`_gatecheck.py` refused both calls on its mtime stale-guard — a scoped ship leaves the untouched modules older than the engine edit; the scoped ship's content-hash 0-stale proof supersedes it, the r490 precedent.)
- Plateau (§4): a widget-build round — neither counts nor resets; **0 of 3**.

**Recorded, not built** (each under the floor or a different mechanism): item 2's refusals by red span — CEDR501 6.0's five bundles (the D1 `[accordion N]` + `[H3]` panels whose body is a `[Body] | [Image]` table — a D1 table-body dialect), CEDK102 #4's `[hover trigger] ( … )` definitions, MXEX301 4.0's `[Alert]` inside a panel, TEDC401 1.0's `[table]` and trailing sentence, PWY1009 3.3's `[hyperlink URL]`, TEDC401 / TEDC402 0.0's avatar + speech-bubble specs, HPFUN903 / TWHK907's phase-label columns (`Facing: [h4]` / `Reverse: [body text]`), ENFUN05's `Title of accordion` label rows with a Canva note, FRFUN06's `[Video N]` / `[Audio Button]` cells, TRR304's MTK activity table; WHY_UNBUILT__accordion items 4 (the empty trailing panel, 5), 5 (an ordinary `[button]`, 22) and 6 / 1C (one-row tables, 17) — the next accordion rounds.

**Ledger:** scoped #1 since the r490 FULL · data `interactive_builders.accordion.panel_delimiters.marker_table` + `.bullet_bold_lead` · env `ACCMARKTABLE_OFF` / `ACCBULLETLEAD_OFF` · code `InteractiveBuilder.#accMarkerTablePanels` (+ `#accResolvePanels` D5, the D4 bulleted fallback) · tools `_s46_r1_{accdump.cjs,accclass,item2list,redspans,flipped,headcheck}.py`, `_s46_goldloc.py`, `_s46_trace.cjs`, `_s46_shardrun.sh`, `_r491_companion.py`, `_r491_finalise.py` · session 46 Round 1.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 491 (260620.54): THE ACCORDION MARKER-CELL TABLE (session 46 Round 1) — an accordion laid out in a table whose cells carry "
                "the writer's own panel markers builds from them (D5 in #accResolvePanels) + the column-label row + the r489 bulleted bold lead. "
                "Env ACCMARKTABLE_OFF / ACCBULLETLEAD_OFF.\n" + '\tstatic AppVersion = "260620.54";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 491 BASELINE (the accordion marker-cell table, "
                "`ACCMARKTABLE_OFF` + `ACCBULLETLEAD_OFF`; SCOPED, scoped #1 since the r490 FULL; scoped_ship PASS; a widget-build round — "
                "accordion Still-a-box 294 -> 270): SCAFFOLD mean 55.3709% / >=50% 1585 / >=75% 277 / >=90% 26 / RAW 39.321% @ 2491 pairs — "
                "+0.0004pp (2 up / 1 down NAMED); cs / body / clean / leak EXACT.** Previous: **ROUND 490 BASELINE")
so = so.replace(a11, "| `ACCMARKTABLE_OFF` | 491 | **THE ACCORDION MARKER-CELL TABLE** (session 46 Round 1). Reverts "
                "`interactive_builders.accordion.panel_delimiters.marker_table`: an accordion laid out in a table whose cells carry the writer's own "
                "`[Accordion N]` / `[Hn]` / `[Accordion N text]` / `[Body]` markers (and a table behind a column-label row) ships as the hand-off box "
                "again — 16 accordions / 12 modules; byte-identical to r490 together with `ACCBULLETLEAD_OFF`. |\n"
                "| `ACCBULLETLEAD_OFF` | 491 | **THE BULLETED BOLD LEAD** (the s45 r489 prototype, shipped as r491's ride-along). Reverts "
                "`interactive_builders.accordion.panel_delimiters.bullet_bold_lead`: the D4 bold-lead reading takes only `**Head:** body` lines again "
                "— 8 accordions / 4 modules (MXEX302, ENGS101, XGF9003, XLP05) return to the box. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.54` (round 491 — **the accordion marker-cell table** + the column-label row + the bulleted bold lead; "
                "`ACCMARKTABLE_OFF` / `ACCBULLETLEAD_OFF`; scoped #1 since the r490 FULL; 15 modules / 19 pages; 24 accordions built — Still-a-box "
                "294 -> 270; skeleton 55.3709 % @ 2491, +0.0004pp).\n" + a14)
wr(PO, so); print("OG ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r491.bak")
G = rd(P).split("\n")
def setv(key, old, new):
    for i, l in enumerate(G):
        if l.strip().startswith(f'"{key}": '):
            assert l.strip().rstrip(",") == f'"{key}": {old}', (key, l)
            G[i] = l.replace(f'"{key}": {old}', f'"{key}": {new}'); return i
    raise SystemExit(f"not found {key}")
def insert_before(key, line):
    for i, l in enumerate(G):
        if l.strip().startswith(f'"{key}": '): G.insert(i, line); return
    raise SystemExit(f"anchor {key}")
setv("build", '"260620.53"', '"260620.54"'); setv("round", "490", "491")
insert_before("_note_r490", '    "_note_r491": "Round 491 (session 46 Round 1, 2026-09-25) — THE ACCORDION MARKER-CELL TABLE (ACCMARKTABLE_OFF) + the '
              'r489 bulleted bold lead (ACCBULLETLEAD_OFF): 15 modules / 19 pages, 24 accordions built (Still-a-box 294 -> 270); SCAFFOLD 55.3705 -> '
              '55.3709 @ 2491 (+0.0004pp, 2 up / 1 down NAMED); RAW 39.285 -> 39.321; cs / body / clean / leak EXACT; accordion verifier 1,263 '
              'panels / 180 modules defect 0; scoped #1 since the r490 FULL; scoped_ship PASS.",')
setv("raw_mean_pct", "39.28", "39.32")
insert_before("_note_r490_state", '    "_note_r491_state": "r491 (the accordion marker-cell table): SCAFFOLD 55.3709 @ 2491, RAW 39.321; 3 movers (2 up / 1 down NAMED).",')
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")

shutil.copyfile(S, S + ".pre-r491-finalise.bak")
i = find("- **ROUND 491 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (25 Sept 2026 ≈11:00, session 46 Round 1 — r491 (the accordion marker-cell table) SHIPPED and committed; the "
        "in-flight marker is cleared). LAST SHIPPED **r491** (260620.54); **LAST FULL = r490 (the s45 Round 10 backstop)**; ledger **scoped #1** "
        "(7 of headroom). Ride-along patches `outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` (buttons, 10 pages) / "
        "`_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages); the r489 accordion patch SHIPPED inside r491.")
k = find("- **No round in flight** (25 Sept 2026 08:45, session 45 STOPPED"); prior = L[k]; del L[k]
k = find("- Before it: **r488**"); r488 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r490**"); L[k] = L[k].replace("- LAST SHIPPED: **r490**", "- Before it: **r490**", 1)
L.insert(k, "- LAST SHIPPED: **r491** (build 260620.54, 25 Sept ≈11:00, session 46 Round 1 — THE ACCORDION MARKER-CELL TABLE + the column-label "
         "row + the bulleted bold lead, `ACCMARKTABLE_OFF` / `ACCBULLETLEAD_OFF`; SCOPED, **scoped #1 since the r490 FULL backstop**, scoped_ship "
         "PASS; a widget-BUILD round — **accordion Still-a-box 294 → 270 (24 built)**; **skeleton 55.3705 → 55.3709 % @ 2491 (+0.0004pp, 2 up / "
         "1 down NAMED)**, ≥50 1585, ≥75 277, ≥90 26, RAW 39.321 % (+0.036); cs / body / clean / leak EXACT; accordion verifier ✓ over the "
         "family; `gate_baseline.json` at r491; the miner 194 CANDIDATE).")
k = find("- Before them: **r487 → r467**")
L[k] = L[k].replace("- Before them: **r487 → r467** (260620.51 → 260620.34 — the unquoted named hover anchor,",
                    "- Before them: **r488 → r467** (260620.52 → 260620.34 — the story-reference carousel shell, the unquoted named hover anchor,", 1)
assert "r488 → r467" in L[k]
k = find("- Plateau window (§4): **0 of 3** — r490")
L[k] = L[k].replace("- Plateau window (§4): **0 of 3** — r490", "- Plateau window (§4): **0 of 3** — r491 a widget-build round (+0.0004pp; "
                    "neither); r490", 1)
k = find("- Standing facts: AppVersion **260620.53**")
L[k] = L[k].replace("AppVersion **260620.53** (r490 the lesson overview's WALT alert — session 45 Round 9, 25 Sept); before it 260620.52",
                    "AppVersion **260620.54** (r491 the accordion marker-cell table — session 46 Round 1, 25 Sept); before it 260620.53 (r490 the "
                    "lesson overview's WALT alert — session 45 Round 9); before it 260620.52", 1)
assert "260620.54" in L[k]
k = find("## Round log")
L.insert(k + 1, "- s46-r1 (engine r491, build 260620.54, 25 Sept 08:51 → ≈11:00) · THE ACCORDION MARKER-CELL TABLE (the hand-off-box lane, D10-3; "
         "WHY_UNBUILT__accordion item 2 = 37 bundles / 27 pages, + item 3 the label row + item 1 the r489 bulleted bold lead) · SHIPPED scoped #1, "
         "scoped_ship PASS · 15 modules / 19 pages, **24 accordions built — Still-a-box 294 → 270**; verifier 1,263 panels defect 0 · skeleton "
         "+0.0004pp (2 up / 1 down NAMED), RAW +0.036 · plateau 0 of 3 (neither — a widget-build round).")
k = find("- **(s45-r5) the carousel after r488:**")
L.insert(k, "- **(s46-r1) the accordion after r491 (270 still a box, `_s46_r1_accdump.json` + `_s46_r1_accclass.py`):** item 2's refusals by red span "
         "(`_s46_r1_redspans.py`) — CEDR501 6.0 ×5 (a D1 `[accordion N]` + `[H3]` panel whose body is a `[Body] | [Image]` table — the gold builds the "
         "accordion, a D1 table-body dialect), CEDK102 #4 `[hover trigger] ( … )`, MXEX301 4.0 `[Alert]` in a panel, TEDC401 1.0 `[table]` + a trailing "
         "line, PWY1009 3.3 `[hyperlink URL]`, TEDC401 / TEDC402 0.0 avatar + speech-bubble specs, HPFUN903 / TWHK907 phase-label columns, ENFUN05 "
         "label rows + a Canva note, FRFUN06 `[Video N]` / `[Audio Button]` cells; the doc's item 5 (an ordinary `[button]` in the bundle, 22 / 14 "
         "modules), item 6 / 1C (one-row tables, 17 / 9), item 4 (empty trailing panel, 5), 1B plain grids 44 / 37, 1D multi-table 14, nested "
         "widgets 16 — size each before the next accordion round.")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r491** (260620.54, the "
        "accordion marker-cell table); LAST FULL = **r490** (the s45 backstop); ledger scoped #1; plateau **0 of 3**; 2,491 pairs; census 552 / "
        "545 / 2,679. Ride-along patches `_r469_declined.patch` / `_r469b_declined.patch` / `_r468_declined.patch`. Needs Chris #17–#19, #22, #23.")
k = find("## Session 46 — Round 1 PICK (engine r491)")
j = k + 1
while j < len(L) and not L[j].startswith("## "): j += 1
pick = L[k:j]; del L[k:j]
L.insert(k, "## Session 46 — Round 1 PICK (engine r491) — THE ACCORDION MARKER-CELL TABLE — SHIPPED; the PICK + what-shipped record is in "
         "LOOP_STATE_ARCHIVE.md 'Session 46 — Round 1 PICK (engine r491) + what shipped'; the one-line summary is the s46-r1 Round-log line below.\n")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r488 + the s45 stop's no-round line (verbatim, s46 r491)\n\n" + r488 + "\n" + prior + "\n"
    "\n## Session 46 — Round 1 PICK (engine r491) + what shipped\n\n" + marker + "\n" + "\n".join(pick[1:]).rstrip() + "\n"
    "- **What shipped (r491, 260620.54):** `interactive_builders.accordion.panel_delimiters.marker_table` (env `ACCMARKTABLE_OFF`) — "
    "`InteractiveBuilder.#accMarkerTablePanels` as D5 in `#accResolvePanels` (after D1–D4) — and `.bullet_bold_lead` (env `ACCBULLETLEAD_OFF`, "
    "the r489 patch). Probe OFF 0 changed; ON 19 pages / 15 modules; 24 accordions built, 0 lost (dashboard Still-a-box 294 → 270); ≈ 70 of 112 "
    "new panel titles are gold accordion headings, the rest developer substitutions (MXEX302 clickDrop, XMES101 carousel, PWY1007 flip cards); "
    "accordion verifier 1,263 panels / 180 modules defect 0; scoped_ship PASS; +0.0004pp, SSOG105_1_0 −0.2 NAMED (overlap 125 → 126). Built "
    "through five instrument fixes found by `_s46_trace.cjs` (the `accord(io|ia)n` spelling, whitespace between two red spans, the developer-cue "
    "/ instruction-sentence notes, the image URL on the next line, a titled panel with only a picture still waiting for its body).\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
