#!/usr/bin/env python3
"""ROUND 367 (loop session 21 Round 4 — the r217 box for a bare dropDown / typing widget: DECLINED on the probe, shipped INERT) —
finalise: changelog, AppVersion (260619.37 → 260619.38), CLAUDE.md §11 (SABOX367_OFF row, inert) / §14, gate_baseline.json
_meta only (no baseline moves — the corpus is byte-identical to r366), loop/README.md. Idempotent; LF via wr()."""
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
ENTRY = """## 2026-09-18 (round 367, build 260619.38) — THE r217 STANDALONE BOX FOR A BARE dropDown / typing WIDGET — DECLINED ON THE PROBE, SHIPPED INERT: the corpus is byte-identical to r366 (the autonomous loop's session 21, Round 4)

### 1. WHAT CHANGED, IN ONE LINE

**Nothing in the output.** The round measured whether the gold wraps a bare `[drop down]` / `[typing]` widget (no `[Activity]` opener) in a numbered activity box the way the r217 standalone box does for dragAndDrop / unclassified / multiChoiceQuiz / radioQuiz / selfCheck / interactive, read 0.61 / 0.62 from a loose text match, built the hook (`standalone_widget_box.types_round367`, env `SABOX367_OFF`) and PROBED it over all 416 modules: **189 pages / 116 modules changed, 173 paired pages scored 36 up / 135 down, pp-sum −275** — the gold does NOT box them. The list ships EMPTY; the one-line engine hook is inert; `SABOX367_OFF` is a no-op until the list is filled.

### 2. THE EVIDENCE

- `outputs/_measure_r367_unboxed.py` → `_r367_unboxed.{json,log}`: every un-built capture in no activity box on Claude's page (1,079 on 515 pages / 255 modules), matched on the gold page by its first paragraph / cell — dropDown "gold-boxed" 0.61 (64 captures), typing 0.62 (25). The match was the flaw: a paragraph found INSIDE any gold box counted as "boxed", and the BLL / XMES / ENG pages' text sits in neighbouring boxes.
- The probe (`_r367_probe.cjs`, `_r367_probe_{OFF,ON}_[0-3].log`, `_r367_pagescore.py` → `_r367_onscore.json`): OFF = disk 2110 / 2110; ON 189 pages / 116 modules; by prefix BLL −121pp-sum (42 pages), XMES −60, ENG −35, XTAS −23, XGF −21, XDLS −17; the un-built captures alone −277 over 154 pages (29 up / 125 down). Worst: XGF9001_6_0 47.7 → 32.5, BLL147_1_1 59.3 → 45.5, BLL154_1_1 74.6 → 62.0.
- With `types_round367` emptied: `_r367_probe_INERT_[0-3].log` = disk 2110 / 2110.

### 3. THE DECISION

DECLINED (LOOP §2 — the measured share of the corpus that follows the candidate rule is below 0.60 once measured by the probe itself); recorded in `LOOP_STATE.md` Declined classes. Re-open only with a widget-level match (the gold's `dropQuiz` / typing element inside the same box as the Claude capture's table), never a text match.

### 4. ALSO RECORDED THIS ROUND (the PICK walk, no output change)

- The chip's TEXT form (queue F3 / F5 / F12 — the gold's `1.0` decimal chip vs Claude's zero-padded `01`) is KB 00D constraint 16: the KB outranks the gold.
- The dropped activity titles on UN-numbered tags (`outputs/_measure_r367_tagtail.py` → `_r367_tagtail.{json,log}`; 1,444 tags / 177 modules): the gold opens the box with the `<h3>` on 0.85 of the 946 it boxes, Claude already on 0.79 (the bare `[Activity] Title` is the r362 owner form: gold 0.91 / Claude 0.89); the miss is 108 rows / 78 pages / 52 modules spread over `[Interactive] Title` (29 rows — gold 0.45 for that tag), `[Activity box] Ka pai!` closers, `[Activity: Embedded]` + a red line, `[Activity individual - 3A]` … — no sub-form at the floor.
- The activity rows re-decomposed on the r366 corpus with the WT check fixed (`_measure_r366_actmiss.py`): in-capture 3,328 lines / 596 pages; absent-in-wt 1,486 / 440 pages (BLL240 / MXFUN01 / CEDT301 / CEDT207 / CEDK501 = the dual-build and hub pairing artefacts; the rest: journal lines, Likert options, designer notes — diffuse); not-in-wt 3,147 / 839 pages (class C).
- AppVersion 260619.38; CLAUDE.md §11 / §14; `gate_baseline.json` `_meta` (build / round; every baseline stands at r366); loop README; `_MIGRATION/CHECKSUMS__engine.txt` refreshed (`.pre-r367.bak` kept). No regeneration.

"""
if "round 367, build 260619.38" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r367 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.38"' not in s:
    old = '\tstatic AppVersion = "260619.37";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, '\t// ROUND 367 (260619.38): the r217 standalone box for a bare dropDown / typing widget — DECLINED on the probe (173 paired pages, 36 up / 135 down), shipped INERT (standalone_widget_box.types_round367 = []; env SABOX367_OFF a no-op); the corpus is byte-identical to r366. The autonomous loop\'s session 21 Round 4.\n\tstatic AppVersion = "260619.38";')
    wr(P, s); print("Config.js: 260619.38")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "| `SABOX367_OFF` | 367 |" not in s:
    OLD11 = "| `LEADFREE_OFF` | 366 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `SABOX367_OFF` | 367 | **DECLINED — INERT.** The r217 standalone box for a bare dropDown / typing widget (`standalone_widget_box.types_round367`, shipped EMPTY): measured at 0.61 / 0.62 by a loose text match, probed over all 416 modules at 36 up / 135 down (pp-sum −275, BLL −121) — the gold does NOT box them. The hook accepts a type on the list unless the env is set; with the list empty both are no-ops and the corpus is byte-identical to r366. Re-open only with a widget-level match. |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.37` (round 366"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.38` (round 367 — **DECLINED, shipped inert**: the r217 standalone box for a bare dropDown / typing widget probed at 36 up / 135 down and left with an empty type list (`standalone_widget_box.types_round367`, env `SABOX367_OFF`); the corpus is byte-identical to r366 — every r366 baseline stands; the autonomous loop's session-21 Round 4). Previous: `260619.37` (round 366"
             + OLD14[len("- **Build:** `260619.37` (round 366"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r367" not in d["_meta"]:
    d["_meta"]["build"] = "260619.38"; d["_meta"]["round"] = 367; d["_meta"]["date"] = "2026-09-18"
    d["_meta"]["_note_r367"] = "Round 367: DECLINED on the probe (the r217 box for a bare dropDown / typing widget — 36 up / 135 down), shipped inert; the corpus is byte-identical to r366 — every r366 baseline stands (skeleton 52.698 / 1123 / 173 / 15; RAW 37.193; body_compare 202 / 42 / 4 / 157)."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r367 meta")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_r367_finalise.py" not in s:
    A = "| `_measure_r366_actmiss.py`"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_measure_r367_tagtail.py` / `_r367_tagtail.{json,log}` (the dropped titles on un-numbered tags — below floor) / `_measure_r367_unboxed.py` / `_r367_unboxed.{json,log}` / `_r367_probe.cjs` / `_r367_probe_{OFF,ON,INERT}_[0-3].log` / `_r367_changed_{modules,pages}.txt` / `_r367_on/` / `_r367_pagescore.py` / `_r367_onscore.json` / `_r367_finalise.py` | "
           + loc + " | Session 21 Round 4 (engine r367, build 260619.38) — DECLINED on the probe, shipped inert: the un-boxed standalone widget measured (a loose text match read 0.61 / 0.62 for dropDown / typing), the probe over all 416 modules (36 up / 135 down), the inert re-probe (2110 / 2110); the tag-title and chip-form dispositions of the PICK walk. |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r367 rows")
print("finalise done")
