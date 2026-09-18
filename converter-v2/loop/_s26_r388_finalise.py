#!/usr/bin/env python3
"""ROUND 388 (loop session 26 Round 2 — the plain / solid alert does not close its column either) — finalise: changelog (entry
text in _s26_r388_entry.md), AppVersion (260619.58 -> 260619.59), CLAUDE.md §9 / §11 / §14, gate_baseline.json, loop/README.md.
Idempotent; LF preserved. Run under WSL: python3 _s26_r388_finalise.py"""
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
ENTRY = rd(os.path.join(HERE, "_s26_r388_entry.md")).replace("\r\n", "\n")
if not ENTRY.endswith("\n\n"): ENTRY = ENTRY.rstrip("\n") + "\n\n"
if "round 388, build 260619.59" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r388 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.59"' not in s:
    old = '\tstatic AppVersion = "260619.58";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, "\t// ROUND 388 (260619.59): the plain / solid alert box does not close its column either — the prose after a div.alert / div.alert.solid flows on inside the same col-md-8 (callouts.flow_after_tags.rules, rule 2; per-rule env ALERTFLOW_OFF on top of the family's WHFLOW_OFF; #flowsAfter tests the box's own open tag so `alert top` keeps the r51 break). Standard template; the paired census 0.74 / 0.74; 323 pages / 138 modules; FULL regeneration (the ledger's backstop, counter 0).\n\tstatic AppVersion = \"260619.59\";")
    wr(P, s); print("Config.js: 260619.59")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "`ALERTFLOW_OFF` | 388" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 387 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 388 BASELINE (the plain / solid alert box does not close its column either — the prose after a `div.alert` / `div.alert.solid` flows on inside the same col-md-8; 138 modules; FULL regeneration of all 416 — the ledger's backstop, scoped counter 0, no residue from r378–r387): SCAFFOLD mean 53.455% / >=50% 1155 / >=75% 192 / >=90% 15 / RAW 37.719% @ 1956 pairs, pairs skipped 0 — hold-or-improve; 298 movers (244 up, 54 down — the 54 = the family's gold-BREAK minority, named in the r388 changelog: XLP06_2_0 −4.9, MXDB302_5_0 −4.1, ENGJ201_3_0 −2.9, ENGS302_3_0 −2.8, TEDC402_1_0 −2.6, the rest ≤ 2.3). compare_structure 11643 / 172 / 625 EXACT; body_compare 42 / 4 / 173 / 218 EXACT.** Previous — ROUND 387 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `WHFLOW_OFF` | 387 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `ALERTFLOW_OFF` | 388 | **THE PLAIN / SOLID ALERT BOX DOES NOT CLOSE ITS COLUMN EITHER** (the autonomous loop's session 26 Round 2 — the PAIRED row-break census for every block type in both directions, `_s26_rowpair.py` / `_s26_rowpair_alert.py`). The r51 `row_breaks.after` rule closes the section row after every boxed callout; paired on the boundaries the fix changes, the gold FLOWS the prose after a `div.alert` on 0.74 (60 / 21; 50 pages / 39 modules) and after a `div.alert.solid` on 0.74 (32 / 11; 27 pages / 19 modules) — every Standard subject group with ≥ 5 boundaries ≥ 0.64 (Online Safety 14 / 3, Leaving to Learn 13 / 5, ANZH 9 / 2, ConnectED 8 / 2 + 7 / 4, English 7 / 2 + 7 / 2, NCEA1 solid 10 / 0). The s25 \"an alert is its column's last child at 0.86\" counted the alerts a heading follows (a row on both sides) — the paired instrument corrected it. Direction B (Claude flows) clears the r51 flow rule for images 0.82 / video 0.78 / lists 0.90 / tables 0.63 / paragraphs 0.92. Data `callouts.flow_after_tags.rules` — rule 1 = the r387 whakataukī rule verbatim, rule 2 = `{tags: [alert, important], templates: [Standard], exclude_class_match: \"\\\\btop\\\\b\", env: ALERTFLOW_OFF}`; `ContentConverter.#flowsAfter(tag, run, boxOpen)` walks the rules and tests the box's OWN emitted open tag against `exclude_class_match` (so `alert top` keeps the break; the span push records `boxOpen` for the CONTAINER_CLOSE site) and honours a per-rule `env` on top of the family's `WHFLOW_OFF`. Not listed: `alert.top` (2 / 2, by class), `alertActivity` (the side column), Bilingual solid 0.38, Inquiry / Fundamentals (≤ 1 boundary); not taken: activity 0.45 (a tie), h3 (Claude right). OFF: `ALERTFLOW_OFF` = the r387 output; `WHFLOW_OFF` = the r386 output (both rules). 323 pages / 138 modules; FULL regeneration (the backstop; the manifest diff = the probe's 323 pages, no residue from the seven scoped ships); skeleton +0.060pp (298 movers 244 up / 54 down), ≥50 +3, ≥75 +3; every other gate EXACT. |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.58` (round 387"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.59` (round 388 — **the plain / solid alert box does not close its column either: the prose after a `div.alert` / `div.alert.solid` flows on inside the same col-md-8** (`callouts.flow_after_tags.rules` rule 2, per-rule env `ALERTFLOW_OFF` on top of the family's `WHFLOW_OFF`; `ContentConverter.#flowsAfter(tag, run, boxOpen)` tests the box's own open tag so `alert top` keeps the r51 break); the autonomous loop's session 26 Round 2 — found by the PAIRED row-break census for every block type in both directions (`_s26_rowpair.py`: gold flows after a plain alert 0.74, a solid alert 0.74, every Standard subject group ≥ 0.64; direction B clears the r51 flow rule for images / video / lists / tables / paragraphs); 323 pages / 138 modules changed; FULL regeneration of all 416 (the ledger's backstop, scoped counter 0 — the manifest diff = the probe's 323 pages to the page, NO residue from the seven scoped ships r378–r387); skeleton 53.395 → 53.455 % (+0.060pp; 298 movers 244 up / 54 down — the 54 the family's gold-BREAK minority, named), ≥50 1152 → 1155, ≥75 189 → 192, ≥90 15, RAW 37.688 → 37.719 %; every other gate EXACT; the miner re-mined 178 CANDIDATE rows (179 → 178, 0 new)). Previous: `260619.58` (round 387"
             + OLD14[len("- **Build:** `260619.58` (round 387"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r388" not in d["_meta"]:
    d["_meta"]["build"] = "260619.59"; d["_meta"]["round"] = 388; d["_meta"]["date"] = "2026-09-19"
    d["_meta"]["_note_r388"] = "Round 388: the plain / solid alert box does not close its column either (323 pages / 138 modules; FULL regeneration, the ledger's backstop, counter 0). Skeleton 53.395 -> 53.455 (+0.060pp; 298 movers 244 up / 54 down, pp-sum +117.3), >=50 1152 -> 1155, >=75 189 -> 192, >=90 15, RAW 37.688 -> 37.719; every other gate EXACT."
    sk = d["skeleton"]; sk["mean_scaffold_pct"] = 53.455; sk["median_scaffold_pct"] = 54.0; sk["pages_ge_50"] = 1155; sk["pages_ge_75"] = 192; sk["pages_ge_90"] = 15; sk["raw_mean_pct"] = 37.719
    sk["_note_r388"] = "Round 388: SCAFFOLD 53.3946 -> 53.4546 (+0.060pp; 298 movers, 244 up / 54 down, pp-sum +117.3 - the 54 dips the alert family's gold-BREAK minority: XLP06_2_0 -4.9, MXDB302_5_0 -4.1, ENGJ201_3_0 -2.9, ENGS302_3_0 -2.8, TEDC402_1_0 -2.6, ENGS101_3_0 -2.3, ENGI201_1_0 -2.3, ENGJ102_3_0 -2.2, AGH1005_3_0 -2.1, MXDB102_1_0 -2.0, AGH1007_9_0 -2.0, OSOH201_3_0 -1.8, the rest <= 1.8), >=50 1155, >=75 192, >=90 15, RAW 37.719; FULL regeneration of all 416 (0 movers outside the 138 affected modules). State outputs/_s26_r388_sk_final.json."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r388")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_s26_r388_finalise.py" not in s:
    A = "| `_s26_ledger2.py` + `.out`"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_s26_rowpair.py` + `.out` + `_s26_rowpair_alert.py` (the PAIRED row-break census for every block type in both directions — (A) Claude breaks: does the gold flow? (B) Claude flows: does the gold break? — per template and subject group) / `_s26_r388_splice.py` + `_s26_r388_ruleenv.py` (the engine splices: `rules`, the box's own open tag, the per-rule env) / `_s26_r388_probe.cjs` + `_s26_r388_probe_run.sh` + their OFF / ON logs + `_s26_r388_on/` / `_s26_r388_pagescore.py` + `_s26_r388_onscore.json` / `_s26_r388_fullship_par.sh` + `_s26_r388_fullship_run.sh` + the 36 batch logs + `_s26_r388_fullship_regen.log` / `_s26_r388_stalecheck.log` + `_s26_r388_manifest_diff.log` + `_s26_r388_regen_vs_probe.log` / `_s26_r388_gates.sh` + `.log` + `_s26_r388_sk_final.json` + `_s26_r388_sk_full.log` + `_s26_r388_sk_delta.log` / `_s26_r388_postship.sh` + `_s26_r388_selftests.log` + `_s26_r388_fastloop_snapshot.log` + `_s26_r388_manifest_snapshot.log` + `_s26_r388_index.log` / `_s26_r388_ledger.log` / `_diff_miner_s26_r388.log` + `_diff_queue_pre_r388.md` + `_s26_r388_queue_delta.log` / `_s26_r388_entry.md` + `_s26_r388_finalise.py` + `_s26_r388_checksums.sh` | "
           + loc + " | Session 26 Round 2 (engine r388, build 260619.59) — the plain / solid alert box does not close its column either: the paired row-break census (gold flows after a plain alert 0.74, a solid alert 0.74; direction B clears the r51 flow rule), the probe (OFF = the r387 set exactly; ON 323 pages / 138 modules, 244 up / 54 down, pp-sum +117.3), the FULL regeneration (the ledger's backstop; the manifest diff = the probe's 323 pages, no residue) + gates (skeleton 53.395 → 53.455, ≥50 +3, ≥75 +3; every other gate EXACT), the miner re-mine (178 rows), the finalise. |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r388 row")
print("finalise done")
