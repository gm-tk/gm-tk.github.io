#!/usr/bin/env python3
"""ROUND 391 (loop session 26 Round 5 — the own-row supervisor panel's text column in Leaving to Learn) — finalise: changelog
(entry text in _s26_r391_entry.md), AppVersion (260619.61 -> 260619.62), CLAUDE.md §9 / §11 / §14, gate_baseline.json,
loop/README.md. Idempotent; LF preserved. Run under WSL: python3 _s26_r391_finalise.py"""
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
ENTRY = rd(os.path.join(HERE, "_s26_r391_entry.md")).replace("\r\n", "\n")
if not ENTRY.endswith("\n\n"): ENTRY = ENTRY.rstrip("\n") + "\n\n"
if "round 391, build 260619.62" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r391 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.62"' not in s:
    old = '\tstatic AppVersion = "260619.61";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, "\t// ROUND 391 (260619.62): the own-row supervisor panel's text column is `col-12 col-md-12` in the Leaving to Learn family (callouts.by_tag.'supervisor note'.inner_row.text_col_by_subject, env PANELCOL_OFF; gold 28 / 37 = 0.76 on 35 pages / 15 modules; the activity-owned panel untouched). 28 pages / 6 modules; scoped ship #3 since the r388 full.\n\tstatic AppVersion = \"260619.62\";")
    wr(P, s); print("Config.js: 260619.62")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "`PANELCOL_OFF` | 391" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 390 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 391 BASELINE (the own-row supervisor panel's text column is `col-12 col-md-12` in the Leaving to Learn family; 6 modules; SCOPED regeneration of the 6, the probe proving the other 410 byte-identical; scoped ship #3 since the r388 full): SCAFFOLD mean 53.525% / >=50% 1158 / >=75% 191 / >=90% 15 / RAW 37.762% @ 1956 pairs, pairs skipped 0 — hold-or-improve; 23 movers (21 up, 2 down — XDLS901_2_0 −0.9, XDLS901_4_0 −0.7, the family's `col-12` minority). compare_structure 11700 / 172 / 625 EXACT; body_compare 42 / 4 / 173 / 218 EXACT.** Previous — ROUND 390 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `SUPSPAN_OFF` | 390 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `PANELCOL_OFF` | 391 | **THE OWN-ROW SUPERVISOR PANEL'S TEXT COLUMN IS `col-12 col-md-12` IN THE LEAVING TO LEARN FAMILY** (the autonomous loop's session 26 Round 5 — the r390 miner's one new row #3735 `body EXTRA div.col-12 › ul` decomposed by `_s26_r391_panelcol.py`: a parent-label mismatch, the gold's panel text column carrying `col-md-12`). Gold corpus-wide `col-12` 327 / `col-12 col-md-12` 93 (the template's default stays); Leaving to Learn OWN-ROW panels 28 / 37 = 0.76 on 35 pages / 15 modules (XDLS90x 28 / 37); LtL activity-owned panels 0.37 and English 0.50 = ties (untouched); English own-row 7 / 9 on 9 pages (under the floor). Data `callouts.by_tag.\"supervisor note\".inner_row.text_col_by_subject {enabled, env, by_subject}` — `#calloutOpen`'s inner_row def swap rewrites the LAST `<div class=\"col-12\">` of the open string to the module's subject class (`module_meta.subject`); `activity_wrapper.super_content.panel_open` untouched. OFF = the r390 output (probe 2109 / 2109). 28 pages / 6 modules; skeleton +0.008pp, ≥50 +1; every other gate EXACT. |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.61` (round 390"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.62` (round 391 — **the own-row supervisor panel's text column is `col-12 col-md-12` in the Leaving to Learn family** (`callouts.by_tag.\"supervisor note\".inner_row.text_col_by_subject`, env `PANELCOL_OFF`); the autonomous loop's session 26 Round 5 — the r390 miner's one new row decomposed (gold 28 / 37 = 0.76 on 35 pages / 15 modules; the activity-owned panel a tie, untouched); 28 pages / 6 modules changed; SCOPED regeneration of the 6 (scoped ship #3 since the r388 full); skeleton 53.518 → 53.525 % (+0.008pp; 23 movers 21 up / 2 down, named), ≥50 1157 → 1158, ≥75 191, ≥90 15, RAW 37.756 → 37.762 %; every other gate EXACT; the miner re-mined 178 CANDIDATE rows (#3735 gone, one new #4286 = the panel's bullets split by their inline `[link]` markers into separate `<ul>`s, 21 pages / 3 modules — the next candidate)). Previous: `260619.61` (round 390"
             + OLD14[len("- **Build:** `260619.61` (round 390"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r391" not in d["_meta"]:
    d["_meta"]["build"] = "260619.62"; d["_meta"]["round"] = 391; d["_meta"]["date"] = "2026-09-19"
    d["_meta"]["_note_r391"] = "Round 391: the own-row supervisor panel's text column in Leaving to Learn (28 pages / 6 modules; scoped ship #3 since the r388 full). Skeleton 53.518 -> 53.525 (+0.008pp; 23 movers 21 up / 2 down, pp-sum +15.2), >=50 1157 -> 1158, >=75 191, >=90 15, RAW 37.756 -> 37.762; every other gate EXACT."
    sk = d["skeleton"]; sk["mean_scaffold_pct"] = 53.525; sk["median_scaffold_pct"] = 54.0; sk["pages_ge_50"] = 1158; sk["pages_ge_75"] = 191; sk["pages_ge_90"] = 15; sk["raw_mean_pct"] = 37.762
    sk["_note_r391"] = "Round 391: SCAFFOLD 53.5175 -> 53.5253 (+0.008pp; 23 movers, 21 up / 2 down, pp-sum +15.2 - XDLS901_2_0 -0.9 / XDLS901_4_0 -0.7 the family's col-12 minority), >=50 1158 (XDLS906_2_0 up), >=75 191, >=90 15, RAW 37.762; SCOPED regeneration of the 6 LtL own-row-panel modules. State outputs/_s26_r391_sk_final.json."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r391")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_s26_r391_finalise.py" not in s:
    A = "| `_s26_r390_supclose.py` + `.out`"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_s26_r391_panelcol.py` + `.out` + `_s26_r391_panelcol2.out` (every super-content panel's text-column class, gold vs Claude, per group; the own-row / activity split) / `_s26_r391_splice.py` (the PICK + the data + engine splice) / `_s26_r391_probe.cjs` + `_s26_r391_probe_run.sh` + their OFF / ON logs + `_s26_r391_on/` / `_s26_r391_pagescore.py` + `_s26_r391_onscore.json` / `_s26_r391_batches.sh` + `_s26_r391_regen_run.sh` + the batch log / `_s26_r391_fresh.log` + `_s26_r391_manifest_diff.log` + `_s26_r391_regen_vs_probe.log` / `_s26_r391_gates.sh` + `.log` + `_s26_r391_sk_final.json` + `_s26_r391_sk_full.log` + `_s26_r391_sk_delta.log` / `_s26_r391_postship.sh` + the selftest / fast-loop / manifest / index logs / `_s26_r391_ledger.log` / `_diff_miner_s26_r391.log` + `_diff_queue_pre_r391.md` + `_s26_r391_queue_delta.log` / `_s26_r391_entry.md` + `_s26_r391_finalise.py` + `_s26_r391_checksums.sh` | "
           + loc + " | Session 26 Round 5 (engine r391, build 260619.62) — the own-row supervisor panel's text column is `col-12 col-md-12` in Leaving to Learn: the r390 miner row decomposed (gold 0.76 on 35 pages), the probe (OFF 2109 / 2109; ON 28 pages / 6 modules, 21 up / 2 down, +15.2), the scoped regen + gates (skeleton 53.518 → 53.525, ≥50 +1; every other gate EXACT), the miner re-mine (178 rows; #3735 gone, #4286 new), the finalise. |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r391 row")
print("finalise done")
