#!/usr/bin/env python3
"""ROUND 368 (loop session 21 Round 5 — the r367 hook corrected for the upload box and re-probed: DECLINED again, inert) —
finalise: changelog, AppVersion (260619.38 → 260619.39), CLAUDE.md §11 (the r367 row amended) / §14, gate_baseline.json
_meta only (the corpus is byte-identical to r366), loop/README.md. Idempotent; LF via wr()."""
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
ENTRY = """## 2026-09-18 (round 368, build 260619.39) — THE r217 BOX FOR A BARE dropDown / typing WIDGET, RE-OPENED WITH THE UPLOAD BOX EXCLUDED AND DECLINED AGAIN: `[drop down]` is not one widget — the corpus stays byte-identical to r366 (the autonomous loop's session 21, Round 5)

### 1. WHAT CHANGED, IN ONE LINE

**Nothing in the output.** A widget-level census (`outputs/_measure_r368_boxshare.py` → `_r368_boxshare.{json,log}`: every widget element on every paired page — the skeleton's WIDGET_MARKERS classes on the gold side, the captures + built classes on Claude's — and whether it sits inside a `div.activity`) showed the gold boxes every TASK widget at 0.98–1.00 (dragAndDrop 0.99 of 1,224, multiChoiceQuiz 0.98, typing 0.98 of 477, dropQuiz 0.99 of 227, reorder / radioQuiz 0.99, wordDrag / bingo / wordSelect / memoryGame / crossword 1.00, selfCheck 0.99) and the DISPLAY widgets at 0.09–0.48 (flipCard 0.46, carousel 0.48, clickDrop 0.31, accordion 0.22, tabs 0.21, speechBubble 0.13 …) — the r217 list is right and Claude follows it, except `capture:dropDown` 0.58 and `capture:typing` 0.83 boxed. r367's −275 was traced to the KB c43 UPLOAD BOX: `[upload to dropbox]` is a dropDown-typed bundle through the lexicon's `dropbox` alias and lives inside the preceding activity (r314) — 184 of r367's boxes wrapped upload buttons. The hook now excludes `InteractiveBuilder.UploadBoxCandidate` bundles (a one-line guard, kept), the list was refilled and PROBED again: **76 pages / 63 modules, 72 paired pages 19 up / 52 down, pp-sum −32.** The remaining dropDown-typed captures are mostly the writer's `[drop down]` REVEAL / go-to / dropbox variants that the gold folds into the PRECEDING activity (ENGC202 lesson 1: the gold keeps "The big reveal" inside box 1A; r368 opened a phantom 1B) — not the dropQuiz widgets the census counted. No derivable discriminator between a `[drop down]` quiz and a `[drop down]` reveal → DECLINED; the list ships EMPTY, the corpus byte-identical (`_r368_probe_INERT_[0-3].log` 2110 / 2110).

### 2. ALSO RECORDED THIS ROUND (the PICK walk, no output change)

- The captured LIST leads (`outputs/_measure_r368_leadlist.py` → `_r368_leadlist.{json,log}`): 316 un-built captures with a leading list on 228 pages / 154 modules; the gold keeps the list free on 0.33 (mcq 0.09 / 0.42, dropDown 0.20 / 0.33, typing 0.26, accordion 0.54, dragAndDrop 0.38); no (owner, type) group at the floor reaches 0.60 — the list is the widget's own items. DECLINED.
- The body-region queue rows (#6080–#6112: EXTRA / MISSING `div.row` / `p` / `img` / `ul` / `h3` in BOTH directions on hundreds of pages) are difflib alignment of the gold's row splits and dropped images — no single mechanism; recorded.
- AppVersion 260619.39; CLAUDE.md §11 (the `SABOX367_OFF` row amended) / §14; `gate_baseline.json` `_meta` (every r366 baseline stands); loop README; `_MIGRATION/CHECKSUMS__engine.txt` refreshed (`.pre-r368.bak` kept). No regeneration.

"""
if "round 368, build 260619.39" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r368 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.39"' not in s:
    old = '\tstatic AppVersion = "260619.38";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, '\t// ROUND 368 (260619.39): the r217 box for a bare dropDown / typing widget re-opened with the KB c43 upload box excluded (InteractiveBuilder.UploadBoxCandidate) and DECLINED again on the probe (19 up / 52 down) — `[drop down]` is a reveal as often as a quiz; the list stays empty, the corpus byte-identical to r366. The autonomous loop\'s session 21 Round 5.\n\tstatic AppVersion = "260619.39";')
    wr(P, s); print("Config.js: 260619.39")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "re-opened as r368" not in s:
    OLD11 = "| `SABOX367_OFF` | 367 | **DECLINED — INERT.**"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = "| `SABOX367_OFF` | 367 / 368 | **DECLINED — INERT** (re-opened as r368 with the KB c43 upload box excluded — `InteractiveBuilder.UploadBoxCandidate`, a guard kept in `saOn` — and declined again: 19 up / 52 down; a writer's `[drop down]` is a reveal / go-to as often as a quiz and the gold folds those into the preceding activity)."
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.38` (round 367"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.39` (round 368 — **DECLINED again, inert**: the r217 box for a bare dropDown / typing widget re-opened with the upload box excluded (the widget-level census `_measure_r368_boxshare.py` reads the gold at 0.98–0.99 for real dropQuiz / typing widgets) and probed at 19 up / 52 down — Claude's `[drop down]` captures are reveals as often as quizzes; the list stays empty; the corpus is byte-identical to r366; the autonomous loop's session-21 Round 5). Previous: `260619.38` (round 367"
             + OLD14[len("- **Build:** `260619.38` (round 367"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r368" not in d["_meta"]:
    d["_meta"]["build"] = "260619.39"; d["_meta"]["round"] = 368; d["_meta"]["date"] = "2026-09-18"
    d["_meta"]["_note_r368"] = "Round 368: DECLINED again on the probe (the r217 box for a bare dropDown / typing widget with the upload box excluded — 19 up / 52 down), inert; the corpus is byte-identical to r366 — every r366 baseline stands."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r368 meta")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_r368_finalise.py" not in s:
    A = "| `_measure_r367_tagtail.py`"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_measure_r368_leadlist.py` / `_r368_leadlist.{json,log}` (the captured list leads — declined) / `_measure_r368_boxshare.py` / `_r368_boxshare.{json,log}` (who boxes which widget — the widget-level census) / `_r368_probe.cjs` / `_r368_probe_{OFF,ON,INERT}_[0-3].log` / `_r368_changed_{modules,pages}.txt` / `_r368_on/` / `_r368_pagescore.py` / `_r368_onscore.json` / `_r368_finalise.py` | "
           + loc + " | Session 21 Round 5 (engine r368, build 260619.39) — DECLINED again, inert: the widget-level box census, the upload-box exclusion, the corrected probe (19 up / 52 down), the inert re-probe (2110 / 2110); the captured-list class measured and declined. |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r368 rows")
print("finalise done")
