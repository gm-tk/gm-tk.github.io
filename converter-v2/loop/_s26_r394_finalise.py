#!/usr/bin/env python3
"""ROUND 394 (loop session 26 Round 8 — the clickDrop buttons sit directly in the column) — finalise: changelog (entry text in
_s26_r394_entry.md), AppVersion (260619.64 -> 260619.65), CLAUDE.md §9 / §11 / §14, gate_baseline.json, loop/README.md.
Idempotent; LF preserved. Run under WSL: python3 _s26_r394_finalise.py"""
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
ENTRY = rd(os.path.join(HERE, "_s26_r394_entry.md")).replace("\r\n", "\n")
if not ENTRY.endswith("\n\n"): ENTRY = ENTRY.rstrip("\n") + "\n\n"
if "round 394, build 260619.65" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r394 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.65"' not in s:
    old = '\tstatic AppVersion = "260619.64";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, "\t// ROUND 394 (260619.65): the clickDrop buttons sit directly in the column — the built widget's inner <div class=\"row\"> is dropped (interactive.clickDrop.no_row_wrapper, InteractiveBuilder.#cdWrap, env CDROW_OFF; the gold's 385 groups: parent = a column 0.78, an inner row 0.05; Claude wrapped 127 / 128). 122 pages / 77 modules; scoped ship #6 since the r388 full.\n\tstatic AppVersion = \"260619.65\";")
    wr(P, s); print("Config.js: 260619.65")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "`CDROW_OFF` | 394" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 393 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 394 BASELINE (the clickDrop buttons sit directly in the column — `interactive.clickDrop.no_row_wrapper`; 77 modules; SCOPED regeneration of the 77, the probe proving the other 339 byte-identical; scoped ship #6 since the r388 full): SCAFFOLD mean 53.674% / >=50% 1163 / >=75% 194 / >=90% 18 / RAW 37.779% @ 1956 pairs, pairs skipped 0 — hold-or-improve; 117 movers (84 up, 29 down — OSBY201_1_0 −6.2, MXFU301_7_0 −6.1, BLL217_2_0 −5.1: the gate's alignment re-pairing after the row line goes). compare_structure 11723 / 172 / 626 EXACT; body_compare 42 / 4 / 173 / 218 EXACT.** Previous — ROUND 393 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `GLYPHLINE_OFF` | 393 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `CDROW_OFF` | 394 | **THE CLICKDROP BUTTONS SIT DIRECTLY IN THE COLUMN** (the autonomous loop's session 26 Round 8 — the r393 miner's one new row #3699 `body EXTRA div.col-12.col-md-8 › div.row` decomposed: the r283 clickDrop builder's own `open` row). The paired widget census `_s26_r394_clickdrop.py` (the three wrappers enclosing every clickDrop button group): gold 385 groups — the buttons' parent is a column (the page's col-md-8 / the activity box's col-12) 302 = 0.78, an inner `div.row` 19 = 0.05; every subject at the floor ≥ 0.73 (Mathematics 71 / 0, Online Safety 47 / 2, NCEA1 41 / 3, English 35 / 6, BLL 26 / 0, ConnectED 22 / 0, LtL 13 / 0); Claude 128 groups, 127 wrapped. Data `interactive.clickDrop.no_row_wrapper {enabled, env}` — both emit sites (`#clickDrop`, `#clickDropEntry`) take `open` / `close` from `#cdWrap(tpl)`, empty when on (the r307 tile grid and the conversation reveal bubble keep their own wrappers); the r283 verifier pairs by index, the wrapper invisible to it (RESULT identical). OFF = the r393 output (probe 2109 / 2109). 122 pages / 77 modules; skeleton +0.114pp, ≥50 +4, ≥75 +3, ≥90 +3; every other gate EXACT. |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.64` (round 393"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.65` (round 394 — **the clickDrop buttons sit directly in the column** (`interactive.clickDrop.no_row_wrapper`, `InteractiveBuilder.#cdWrap`, env `CDROW_OFF`); the autonomous loop's session 26 Round 8 — the r393 miner's one new row decomposed (the gold's 385 clickDrop groups: parent = a column 0.78, an inner row 0.05; Claude wrapped 127 / 128); 122 pages / 77 modules changed; SCOPED regeneration of the 77 (scoped ship #6 since the r388 full); skeleton 53.560 → 53.674 % (+0.114pp; 117 movers 84 up / 29 down, named), ≥50 1159 → 1163, ≥75 191 → 194, ≥90 15 → 18, RAW 37.787 → 37.779 %; every other gate EXACT, every verifier RESULT identical; the miner re-mined 174 CANDIDATE rows (#3699 + the three panels-under-the-row shadows gone; two new — #3633 the panels' alignment residue, #3606 the Inquiry `inquiryPanel` under consensus)). Previous: `260619.64` (round 393"
             + OLD14[len("- **Build:** `260619.64` (round 393"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r394" not in d["_meta"]:
    d["_meta"]["build"] = "260619.65"; d["_meta"]["round"] = 394; d["_meta"]["date"] = "2026-09-19"
    d["_meta"]["_note_r394"] = "Round 394: the clickDrop buttons sit directly in the column (122 pages / 77 modules; scoped ship #6 since the r388 full). Skeleton 53.560 -> 53.674 (+0.114pp; 117 movers 84 up / 29 down, pp-sum +221.9), >=50 1159 -> 1163, >=75 191 -> 194, >=90 15 -> 18, RAW 37.787 -> 37.779; compare_structure 11723 / 172 / 626 and every other gate EXACT; every verifier RESULT identical."
    sk = d["skeleton"]; sk["mean_scaffold_pct"] = 53.674; sk["median_scaffold_pct"] = 54.2; sk["pages_ge_50"] = 1163; sk["pages_ge_75"] = 194; sk["pages_ge_90"] = 18; sk["raw_mean_pct"] = 37.779
    sk["_note_r394"] = "Round 394: SCAFFOLD 53.5602 -> 53.6736 (+0.114pp; 117 movers, 84 up / 29 down, pp-sum +221.9 - OSBY201_1_0 -6.2 / MXFU301_7_0 -6.1 / BLL217_2_0 -5.1 the alignment re-pairing), >=50 1163 (7 up / 3 down), >=75 194 (+3), >=90 18 (+3), median 54.2, RAW 37.779; SCOPED regeneration of the 77 affected modules. State outputs/_s26_r394_sk_final.json."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r394")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_s26_r394_finalise.py" not in s:
    A = "| `_s26_r393_adjol.py` + `.out`"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_s26_r394_colrow.py` + `.out` (a `div.row` directly inside the col-md-8 column, by kind, Claude vs gold) / `_s26_r394_clickdrop.py` + `.out` (the three wrappers enclosing every clickDrop button group, per subject) / `_s26_r394_why.py` (the alignment behind the largest dips) / `_s26_r394_splice.py` (the PICK + the data + engine splice) / `_s26_r394_probe.cjs` + `_s26_r394_probe_run.sh` + their OFF / ON logs + `_s26_r394_on/` / `_s26_r394_pagescore.py` + `_s26_r394_onscore.json` / `_s26_r394_batches.sh` + `_s26_r394_regen_run.sh` + the batch logs / `_s26_r394_fresh.log` + `_s26_r394_manifest_diff.log` + `_s26_r394_regen_vs_probe.log` / `_s26_r394_gates.sh` + `.log` + `_s26_r394_sk_final.json` + `_s26_r394_sk_full.log` + `_s26_r394_skdelta.py` + `_s26_r394_sk_delta.log` / `_s26_r394_postship.sh` + the selftest / fast-loop / manifest / index logs / `_s26_r394_ledger.log` / `_diff_miner_s26_r394.log` + `_diff_queue_pre_r394.md` + `_s26_r394_qdelta.py` + `_s26_r394_queue_delta.log` / `_s26_r394_entry.md` + `_s26_r394_finalise.py` + `_s26_r394_checksums.sh` | "
           + loc + " | Session 26 Round 8 (engine r394, build 260619.65) — the clickDrop buttons sit directly in the column: the r393 miner row #3699 decomposed (the gold's 385 groups: parent = a column 0.78, an inner row 0.05; Claude wrapped 127 / 128), the probe (OFF 2109 / 2109; ON 122 pages / 77 modules, 88 up / 29 down, +221.9), the scoped regen + gates (skeleton 53.560 → 53.674, ≥50 +4, ≥75 +3, ≥90 +3; every other gate EXACT), the miner re-mine (174 rows; the lead + 3 shadows gone, 2 new dispositioned), the finalise. |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r394 row")
print("finalise done")
