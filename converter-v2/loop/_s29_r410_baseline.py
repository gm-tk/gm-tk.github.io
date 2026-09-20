#!/usr/bin/env python3
"""r410 finalise — refresh reference/tests/gate_baseline.json to the r410 gate readings (CLAUDE.md §12 / loop §3 step 7).
Edits the values in place with a regex per key (the file is hand-formatted; never json.dumps it whole)."""
import re
p = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests/gate_baseline.json"
s = open(p, encoding="utf-8").read()

def setv(key, old, new, count=1):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=count)
    assert n == count, (key, old, new, n)

setv("build", '"260619.79"', '"260619.81"')
setv("round", 408, 410)
setv("mean_scaffold_pct", 53.68, 53.79)
setv("median_scaffold_pct", 54.4, 54.6)
setv("pages_ge_50", 1398, 1406)
setv("raw_mean_pct", 37.88, 37.93)
setv("exact_chain", 14091, 14175)
setv("labels", 91, 99)

note = ('    "_note_r410": "Round 410 (session 29 Round 1; built in session 28 Task 3): the WJFUN tile-page dialect (body_region.fundamentals_panels.tile_pages, env TILEPAGE_OFF; 21 WJFUN modules / 21 pages; SCOPED regeneration of the 23 WJFUN + JPFUN modules, scoped ship #2 since the 19 Sept full; the probe OFF = disk 2555/2555, ON exactly the 21 WJFUN overviews, the other 471 modules byte-identical). Skeleton 53.680 -> 53.789 (+0.1095pp; 21 movers, 21 up / 0 down, 0 outside the set), >=50 1398 -> 1406, >=75 236, >=90 20, RAW 37.884 -> 37.925, median 54.4 -> 54.6; compare_structure exact 14091 -> 14175 (the text-matched pool 16414 -> 16470) / EXTRA 186 / MISSING 690 / row-wrap 23 EXACT; body_compare 54 / 6 / 190 / 248 EXACT; defect clean 2504/2548 = 98.27, leak 73 / 44 EXACT; every verifier EXACT (menulabels labels 91 -> 99 is the r408 count the baseline had not carried — defect 0 is the criterion); 16 selftests GREEN. WJFUN family 37.6 -> 49.9.",\n')
anchor = '    "_note_r408": "Round 408 (session 28 Task 1)'
assert s.count(anchor) == 1
s = s.replace(anchor, note + anchor)
# the per-block notes r408 also kept (skeleton / compare_structure / body / defect)
blocks = {
    '    "_note_r408": "Round 408: SCAFFOLD 53.1341': '    "_note_r410": "Round 410: SCAFFOLD 53.6797 -> 53.7891 (+0.1095pp; 21 movers, 21 up / 0 down — the WJFUN tile-page dialect; 0 outside the 23-module affected set), >=50 1398 -> 1406, >=75 236, >=90 20, RAW 37.884 -> 37.925, median 54.4 -> 54.6; 2349 pairs. State outputs/_s29_r410_sk_final.json. Hold-or-improve from here.",\n',
    '    "_note_r408": "Round 408: exact 13410 -> 14091': '    "_note_r410": "Round 410: exact 14091 -> 14175 (the text-matched pool 16414 -> 16470 — the WJFUN tile panes and tile rows now align); EXTRA 186 / MISSING 690 / row-wrap 23 EXACT.",\n',
    '    "_note_r408": "Round 408: over-capture 54': '    "_note_r410": "Round 410: over-capture 54 / runaway 6 / EMPTY 190 / ANY 248 — EXACT (the WJFUN pages carry no widget breakdown flag either way).",\n',
    '    "_note_r408": "Round 408: 2606 -> 2548 pages': '    "_note_r410": "Round 410: clean 2504 / 2548 = 98.27, leak 73 occ / 44 pages — EXACT.",\n',
}
for a, n in blocks.items():
    assert s.count(a) == 1, a
    s = s.replace(a, n + a)
open(p, "w", encoding="utf-8", newline="\n").write(s)
import json; json.load(open(p, encoding="utf-8"))
print("gate_baseline.json refreshed to r410 and still valid JSON")
