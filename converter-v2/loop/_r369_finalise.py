#!/usr/bin/env python3
"""ROUND 369 (loop session 22 Round 1 — the page's activity numbers made consecutive: DECLINED on the gate's own scorer, shipped inert) —
finalise: changelog, AppVersion (260619.39 → 260619.40), CLAUDE.md §11 (a new NUMNORM_OFF row) / §14, gate_baseline.json
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
ENTRY = """## 2026-09-18 (round 369, build 260619.40) — THE PAGE'S ACTIVITY NUMBERS MADE CONSECUTIVE: DECLINED ON THE GATE'S OWN SCORER, SHIPPED INERT — the autonomous loop's session 22, Round 1

### 1. WHAT CHANGED, IN ONE LINE

**Nothing in the output.** A page-level post-pass (`ContentConverter.#pageNumberNormalise`, data `Emit_Templates.activity_wrapper.page_number_normalise`, env `NUMNORM_OFF`) that renumbers a page's activity boxes consecutively — a duplicate writer id (`5A, 5A`) or a foreign lesson digit (`4A, 4B, 2A`) taking the KB's next letter (00B_CONVERSION_PIPELINE + constraint 62 / 65: "each subsequent interactive takes the next letter … renumber the following activities accordingly"; the gold: Standard lesson pages follow `{page number}{A, B, C …}` on 0.86 of 1,540) — was built, probed in memory over all 416 modules and **DECLINED**: the corpus is byte-identical to r366 (`enabled: false`; the inert re-probe 2110 / 2110), every r366 baseline stands.

### 2. WHY IT WAS PICKED — the miner could not see the class

The session opened by testing session 21's EXHAUSTION verdict rather than accepting it: a Chris-style hand read of four mid-band pages (AGH1002 L2, MXFU201 L4, BLL234 overview, XGF9002 L5 — `outputs/_s22_spotcheck.py`) and a class-level census (`_s22_census.py`) surfaced one mechanism the DIFF MINER cannot see: it keys its classes by the full signature INCLUDING the `number=` value, so "the box's number differs" fragmented into one row per number value and never reached the floor. Measured (`_s22_actnum.py` / `_s22_actnum2.py` / `_s22_actnum3.py` / `_s22_actnum5.py`): the gold is self-consistent (digit = page number) on 0.86 of Standard lesson pages; Claude ships 224 digit-wrong + 276 letters-not-sequential Standard pages; a position-wise box-by-box pre-measure (variant DL — majority digit + smallest unused letter) read **+228 boxes agreeing / 47 pages gained / 1 lost** in Standard, Inquiry +20 boxes, no page lost.

### 3. WHY IT WAS DECLINED — the pre-measure was the wrong instrument

The in-memory probe (`outputs/_r369_probe.cjs`, 4 shards): OFF (`NUMNORM_OFF=1`) = disk **2110 / 2110**; ON = **279 pages / 136 modules**, every differing line a `number=` attribute (`_r369_diffcheck.py`: 650 attributes, 0 other lines). Scored with the skeleton gate's OWN `match()` (`_r369_pagescore.py` → `_r369_pagescore.log`): **266 paired pages 46 up / 77 down / 143 same, pp-sum −106**. The skeleton aligns on the box line's `number=`, and a duplicate id on Claude's page is as often Claude's OWN extra box as the writer's repeat — ENGJ102 L4: Claude `4A 4B 4C 4C` where the first `4C` is an empty synthetic box and the second the writer's poem box, the gold `4A 4B 4C`; renaming the second occurrence drags the gold's `4C` onto the wrong subtree (−11pp on that page; BLL126 L1 −14.9, ANZH303 L1 −12.4, BLL112 L1 −10.6, ENGS401 L4 −10.1). Every letter policy re-scored with the gate's scorer directly on the disk pages (`_r369_variants.py` → `_r369_variants.{log,json}`): smallest-unused-letter (this rule) −106.4 pp-sum / 48 up / 78 down; look-ahead letter (later writer letters untouched) −66.6 / 33 / 60; majority digit only −5.9 / 8 / 7 (68 pages); letters only −59.0 / 24 / 50. No policy readable from the HTML is net-positive. The only remaining discriminator is BOX PROVENANCE — a writer-tagged `[Activity 4C]` keeps its id, the r217 synthetic / journal-instruction box takes the next free letter — which needs engine-side marking: recorded as its own round, not attempted here. The round-306 rule stands (the writer's own id, never invented; the gold's renumber is a NAMED divergence).

### 4. ALSO THIS ROUND

- `reference/tests/_diff_miner.py` `role()` now folds the `number=` VALUE to `[number=*]` in the class role (the diff still compares the full signature), so the activity-number class is one visible row in `DIFF_QUEUE.md` instead of hundreds of sub-floor fragments; re-mined on the r366 corpus.
- AppVersion 260619.40; CLAUDE.md §11 (the `NUMNORM_OFF` row) / §14; `gate_baseline.json` `_meta` (every r366 baseline stands); loop README; `_MIGRATION/CHECKSUMS__engine.txt` + `CHECKSUMS__gates.txt` refreshed (`.pre-r369.bak` kept).

### 5. PROTECTED GATES

Not re-run: the corpus is byte-identical to r366 (the inert re-probe 2110 / 2110) — skeleton **52.698 % / ≥50 1123 / ≥75 173 / ≥90 15 @ 1956**, RAW 37.193 %, compare_structure 11631 / 175 / 617, body_compare 202 / 42 / 4 / 157, every verifier at its recorded baseline, all unchanged.

"""
if "round 369, build 260619.40" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r369 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.40"' not in s:
    old = '\tstatic AppVersion = "260619.39";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, '\t// ROUND 369 (260619.40): the page\'s activity numbers made consecutive (ContentConverter.#pageNumberNormalise, data activity_wrapper.page_number_normalise, env NUMNORM_OFF) — DECLINED on the gate\'s own scorer (46 up / 77 down, pp-sum −106 over 266 paired pages; a duplicate id is as often Claude\'s own extra box as the writer\'s repeat) and shipped INERT (enabled: false); the corpus is byte-identical to r366. The autonomous loop\'s session 22 Round 1.\n\tstatic AppVersion = "260619.40";')
    wr(P, s); print("Config.js: 260619.40")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "`NUMNORM_OFF` | 369" not in s:
    OLD11 = "| `SABOX367_OFF` | 367 / 368 | **DECLINED — INERT**"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `NUMNORM_OFF` | 369 | **DECLINED — INERT** (`page_number_normalise.enabled: false`). The page's activity numbers made consecutive — a duplicate writer id (`5A, 5A`) or a foreign lesson digit (`4A, 4B, 2A`) taking the next letter (KB 00B / constraint 62 / 65; the gold's own form on 0.86 of Standard lesson pages) — built as a page-level post-pass outermost in the body chain (`ContentConverter.#pageNumberNormalise`), probed in memory over all 416 (OFF = disk 2110 / 2110; ON 279 pages / 136 modules, every line a `number=` attribute) and scored with the skeleton gate's own `match()`: **46 up / 77 down, pp-sum −106** — the alignment anchors on the box's number and a duplicate is as often Claude's own extra box as the writer's repeat (ENGJ102 L4). Every letter policy re-scored on the disk pages (`_r369_variants.py`): all net-negative. The only remaining discriminator is box PROVENANCE (engine-side marking — its own round). The round-306 rule stands. With `enabled: false` the hook is a no-op and the env is moot; the corpus is byte-identical to r366. |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.39` (round 368"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.40` (round 369 — **DECLINED, shipped inert**: the page's activity numbers made consecutive (`ContentConverter.#pageNumberNormalise`, data `activity_wrapper.page_number_normalise`, env `NUMNORM_OFF`, `enabled: false`) — the position-wise pre-measure read +228 boxes / 47 pages gained, the gate's own scorer read 46 up / 77 down (pp-sum −106): a duplicate id is as often Claude's own extra box as the writer's repeat, so renaming it drags the alignment; every letter policy net-negative (`_r369_variants.py`); the only remaining discriminator is box provenance (its own round). The DIFF MINER now folds the `number=` value into `[number=*]` so the class is one visible row. The corpus is byte-identical to r366 — every r366 baseline stands. The autonomous loop's session 22 Round 1). Previous: "
             + OLD14[len("- **Build:** "):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r369" not in d["_meta"]:
    d["_meta"]["build"] = "260619.40"; d["_meta"]["round"] = 369; d["_meta"]["date"] = "2026-09-18"
    d["_meta"]["_note_r369"] = "Round 369: DECLINED on the gate's own scorer (the page's activity numbers made consecutive — 46 up / 77 down over 266 paired pages), shipped inert; the corpus is byte-identical to r366 — every r366 baseline stands."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r369 meta")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_r369_finalise.py" not in s:
    A = "| `_measure_r368_leadlist.py`"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_s22_spotcheck.py` / `_s22_spot_{a,b}.log` (the session-22 hand read of four pages) / `_s22_census.py` / `_s22_census.{json,log}` (alert / colour-text / videoSection icon / paddingR / activity-digit census) / `_s22_actnum.py` … `_s22_actnum5.py` + `.{json,log}` (the activity-number measurements, position-wise) / `_r369_probe.cjs` + `_r369_probe_{OFF,ON,INERT}_0[0-3].log` (the in-memory A/B over all 416) / `_r369_diffcheck.py` + `_r369_changed_{modules,pages}.txt` / `_r369_pagescore.py` + `_r369_pagescore.log` (the ON pages scored with the gate's own match()) / `_r369_variants.py` + `_r369_variants.{json,log}` (four letter policies scored on the disk pages) / `_r369_finalise.py` | "
           + loc + " | Session 22 Round 1 (engine r369, build 260619.40) — DECLINED, inert: the consecutive activity-number post-pass; the pre-measure (+228 boxes) vs the gate's scorer (46 up / 77 down); the miner's `[number=*]` fold; the inert re-probe (2110 / 2110). |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r369 row")
print("finalise done")
