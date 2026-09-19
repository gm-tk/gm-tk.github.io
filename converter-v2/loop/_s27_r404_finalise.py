#!/usr/bin/env python3
"""ROUND 404 (loop session 27 Round 9 — DECLINED, shipped inert: the alert-top side column's class by subject) — finalise:
changelog (entry text in _s27_r404_entry.md), CLAUDE.md §11 / §14 (§9 unchanged — the r403 baseline stands), gate_baseline.json note,
loop/README.md. (Config.js AppVersion 260619.75 was edited directly with the Edit tool.) Idempotent; LF preserved.
Run under WSL: python3 _s27_r404_finalise.py"""
import io, os, json
ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
PF = os.path.join(ROOT, "pageforge-site", "converter-v2")
HERE = os.path.dirname(os.path.abspath(__file__))


def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f:
        return f.read()


def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s)


CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)" + chr(10) + chr(10)
ENTRY = rd(os.path.join(HERE, "_s27_r404_entry.md")).replace("\r\n", "\n")
if not ENTRY.endswith("\n\n"): ENTRY = ENTRY.rstrip("\n") + "\n\n"
if "round 404, build 260619.75" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r404 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
assert '"260619.75"' in s, "Config.js not bumped"

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "`SIDECOLSUBJ_OFF` | 404" not in s:
    OLD11 = "| `EMBEDBTN_OFF` | 403 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `SIDECOLSUBJ_OFF` | 404 | **DECLINED — INERT** (`positional_side_alert.after_content.side_column_by_subject` is EMPTY). The alert-top side column's class by subject: "
             "the two-column side-pair census (`_s27_r9_sidepair.py`) reads the gold's `col-md-4 offset-md-0 col-12 paddingL` at 0.51 corpus-wide (a tie) and 0.70 / 0.75 / 0.86 in "
             "NCEA1 / Mathematics / TMoA; built as a `#sideAlertCol` data map and probed over all 416: 17 pages / 10 modules changed, +1.4 pp-sum (2 up / 13 same) — the subject share "
             "is a per-module mix of four spellings (MXFU301 `col-md-4 col-12 paddingL`, HIS1004 the offset form) and Claude's alert-top pairs sit mostly in the English / LtL ties. "
             "The hook is a no-op with the empty map; the corpus is byte-identical to r403. Re-open only with a per-series measurement. |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.74` (round 403"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.75` (round 404 — **DECLINED, shipped inert**: the alert-top side column's class by subject (`#sideAlertCol` reads the def's "
             "`side_column_by_subject` map, EMPTY; env `SIDECOLSUBJ_OFF`) — the gold's `col-md-4 offset-md-0 col-12 paddingL` is 0.51 corpus-wide and a per-module mix; the probe "
             "changed 17 pages for +1.4 pp-sum (`_s27_r9_sidepair.py`); the corpus is byte-identical to r403 — every r403 baseline stands; the autonomous loop's session 27 Round 9). "
             "Previous: `260619.74` (round 403"
             + OLD14[len("- **Build:** `260619.74` (round 403"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r404" not in d["_meta"]:
    d["_meta"]["build"] = "260619.75"; d["_meta"]["round"] = 404
    d["_meta"]["_note_r404"] = "Round 404: DECLINED, shipped inert (the alert-top side column's class by subject — an empty map); no regeneration; every r403 baseline stands."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r404 note")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_s27_r404_finalise.py" not in s:
    A = "| `_s27_r8_mergebox.py` + `.out`"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_s27_r9_sidepair.py` + `.out` (THE TWO-COLUMN SIDE PAIR — every gold col-md-8 | col-md-4 row by the right column's first child; the round's instrument) / "
           "`_s27_r9_pick.md` + `_s27_r9_inprogress.py` / `_s27_r404_probe.cjs` + `_s27_r404_probe_run.sh` + their OFF / ON logs + `_s27_r404_on/` (the ON leg re-run with the "
           "empty map = disk 2109 / 2109) / `_s27_r404_pagescore.py` + `_s27_r404_onscore.json` (17 pages, +1.4 — the decline) / `_s27_r404_entry.md` + `_s27_r404_finalise.py` + "
           "`_s27_r404_checksums.sh` + `_s27_r404_loopstate.py` | "
           + loc + " | Session 27 Round 9 (engine r404, build 260619.75) — DECLINED, shipped inert: the alert-top side column's class by subject (a per-module mix of four "
           "spellings; 17 pages for +1.4). |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r404 row")
print("finalise done")
