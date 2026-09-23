#!/usr/bin/env python3
"""ROUND 456 — refresh reference/tests/gate_baseline.json IN PLACE (line edits, the r453 pattern): every protected field + the r456
notes. A .pre-r456.bak is kept. Run under WSL from anywhere."""
import io, os, json, shutil
P = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "tests", "gate_baseline.json"))
shutil.copyfile(P, P + ".pre-r456.bak")
L = io.open(P, encoding="utf-8").read().split("\n")
def setv(key, old, new):
    for i, l in enumerate(L):
        if l.strip().startswith(f'"{key}": '):
            assert l.strip().rstrip(",") == f'"{key}": {old}', (key, l)
            L[i] = l.replace(f'"{key}": {old}', f'"{key}": {new}')
            return i
    raise SystemExit(f"not found {key}")
def insert_before(key, line):
    for i, l in enumerate(L):
        if l.strip().startswith(f'"{key}": '):
            L.insert(i, line); return
    raise SystemExit(f"anchor not found {key}")
setv("build", '"260620.25"', '"260620.26"'); setv("round", "454", "456")
insert_before("_note_r454", '    "_note_r456": "Round 456 (session 41 Round 4, 2026-09-24; the recognition lane — the under-split census of Round 1) — THE MID-PAGE LESSON HEADING OPENS ITS LESSON PAGE: a lesson opened by a heading (\'[H1] Lesson Four: …\', \'[H2] Lesson 2 …\') or a black \'[LESSON 5]\' / \'LESSON 3\' line with no [End page] before it was merged into the page before; PageSplitter now opens page N.0 there (page_split.mid_page_lesson_heading, MIDLESSON_OFF). SCOPED ship #3 since the r452 FULL: 22 modules, pages 2676 -> 2717, pairs 2487 -> 2520 (+37 new at a 53.9 mean, 4 lost to the gate\'s content pairing). SCAFFOLD 54.7680 -> 54.8705 (+0.1025pp; the pre-existing pairs +0.1177pp), >=50 1549 -> 1575, >=75 265 -> 270, >=90 23 -> 24; cs exact 15855 -> 16024, missing 840 held. NAMED: body ANY 238 -> 239 (the same flagged widgets moved with their content to renumbered / split pages — PHE1003 net +1), clean 2623/2668 -> 2663/2709 (98.31 -> 98.30: 40 of the 41 new pages clean; the 41st is CBI1008\'s split leaking page), leak 75 occ held / pages 45 -> 46 (CBI1008\'s page with 2 leak occurrences is now two pages with one each). _fastloop_diff --accept-named, outputs/_r456_fastloop_named.log.",')
setv("mean_scaffold_pct", "54.77", "54.87"); setv("median_scaffold_pct", "55.8", "55.92")
setv("pages_ge_50", "1549", "1575"); setv("pages_ge_75", "265", "270"); setv("pages_ge_90", "23", "24")
setv("raw_mean_pct", "38.73", "38.88"); setv("pairs", "2487", "2520")
insert_before("_note_r454_state", '    "_note_r456_state": "r456 (the mid-page lesson heading): SCAFFOLD 54.7680 @ 2487 -> 54.8705 @ 2520 (+0.1025pp; the pre-existing population +0.1177pp), RAW 38.726 -> 38.878; movers 40 (29 up / 11 down, 5 of the downs re-pairings — MXDI301_02.0, GEO1004_1_0, MXDB301_6.0, COM1005_3_0, MXFL202_5.0), pp-sum +266.7; 42 new-only / 9 gone Claude pages; 0 movers outside the affected set. outputs/_r456_sk_final.json, _r456_skdelta.log, _r456_prescore.log, _r456_split.py.",')
setv("exact_chain", "15855", "16024")
setv("any_breakdown", "238", "239"); setv("over_capture", "59", "61")
setv("clean_pages", "2623", "2663"); setv("total_pages", "2668", "2709"); setv("clean_pct", "98.31", "98.3")
setv("leak_pages", "45", "46")
out = "\n".join(L); json.loads(out)
tmp = P + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="\n").write(out); os.replace(tmp, P)
print("gate_baseline.json refreshed to r456;", os.path.getsize(P), "bytes")
