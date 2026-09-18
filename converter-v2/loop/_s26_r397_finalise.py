#!/usr/bin/env python3
"""ROUND 397 (loop session 26 Round 11 — a table header cell is plain) — finalise: changelog (entry text in _s26_r397_entry.md),
AppVersion (260619.67 -> 260619.68), CLAUDE.md §9 / §11 / §14, gate_baseline.json, loop/README.md. Idempotent; LF preserved.
Run under WSL: python3 _s26_r397_finalise.py"""
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
ENTRY = rd(os.path.join(HERE, "_s26_r397_entry.md")).replace("\r\n", "\n")
if not ENTRY.endswith("\n\n"): ENTRY = ENTRY.rstrip("\n") + "\n\n"
if "round 397, build 260619.68" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r397 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.68"' not in s:
    old = '\tstatic AppVersion = "260619.67";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, "\t// ROUND 397 (260619.68): a table header cell is plain — a <th> whose whole content is one <b>/<strong> span drops the wrapper (elements.table.header_cell_plain, TablesAndGrids' cell emit, env THPLAIN_OFF; the gold's th plain 0.96, Claude's bold 0.18 on 86 pages). 92 pages / 58 modules; scoped ship #1 since the r396 full.\n\tstatic AppVersion = \"260619.68\";")
    wr(P, s); print("Config.js: 260619.68")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "`THPLAIN_OFF` | 397" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 396 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 397 BASELINE (a table header cell is plain — `elements.table.header_cell_plain`; 58 modules; SCOPED regeneration of the 58, the probe proving the other 358 byte-identical; scoped ship #1 since the r396 full): SCAFFOLD mean 53.695% / >=50% 1163 / >=75% 195 / >=90% 18 / RAW 37.782% @ 1956 pairs, pairs skipped 0 — hold-or-improve; 80 movers (70 up, 7 down — ENGJ403_6_0 −0.9, ENGI405_6_0 −0.8: English pages whose own gold keeps the bold). compare_structure 11723 / 172 / 626 EXACT; body_compare 42 / 4 / 173 / 218 EXACT.** Previous — ROUND 396 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `ITEMVIDEO_OFF` | 396 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `THPLAIN_OFF` | 397 | **A TABLE HEADER CELL IS PLAIN** (the autonomous loop's session 26 Round 11 — the r394 miner row #3725 `body EXTRA th>b › b` followed through by the position-free census `_s26_r397_thb.py`): the gold's 2170 `<th>` cells are wholly bold 97 = 0.04 (plain 0.96 — Mathematics 0.93, ConnectED 0.98, TEDC / NCEA1 / EXPlore / LtL 1.00; English keeps some, 0.17); Claude's were wholly bold 369 = 0.18 on 86 pages / 56 modules — the r383 first-row-header rule promotes a writer's **bold** row to `<th>` and the cell's markdown then rendered `<b>` inside it, against KB 05D's `<tr><th>Header 1</th>…` form and `renderCellInline`'s own stated convention for tag-rendered cells. Data `elements.table.header_cell_plain {enabled, env}` — at the cell emit (free-body tables only) a header cell whose rendered content is exactly one `<b>` / `<strong>` span with no other bold inside drops the wrapper; `<td>` cells keep theirs (the gold's matrix row labels). OFF = the r396 output (probe 2109 / 2109). 92 pages / 58 modules; skeleton +0.012pp; every other gate EXACT. Measured and declined the same round: the speech bubble's character image (the gold's developers add one in Online Safety 0.95 / TEDC 0.91 in five layouts none ≥ 0.6 — a needs-Chris question, not a rule). |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.67` (round 396"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.68` (round 397 — **a table header cell is plain** (`elements.table.header_cell_plain`, `TablesAndGrids`' cell emit, env `THPLAIN_OFF`); the autonomous loop's session 26 Round 11 — the gold's `<th>` plain 0.96, Claude's wholly-bold 0.18 on 86 pages / 56 modules; 92 pages / 58 modules changed; SCOPED regeneration of the 58 (scoped ship #1 since the r396 full); skeleton 53.684 → 53.695 % (+0.012pp; 80 movers 70 up / 7 down, named), ≥50 1163, ≥75 195, ≥90 18, RAW 37.780 → 37.782 %; every other gate EXACT, every verifier RESULT identical; the miner re-mined 173 CANDIDATE rows (unchanged); the speech bubble's character image measured and declined). Previous: `260619.67` (round 396"
             + OLD14[len("- **Build:** `260619.67` (round 396"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r397" not in d["_meta"]:
    d["_meta"]["build"] = "260619.68"; d["_meta"]["round"] = 397; d["_meta"]["date"] = "2026-09-19"
    d["_meta"]["_note_r397"] = "Round 397: a table header cell is plain (92 pages / 58 modules; scoped ship #1 since the r396 full). Skeleton 53.684 -> 53.695 (+0.012pp; 80 movers 70 up / 7 down, pp-sum +23.6), >=50 1163, >=75 195, >=90 18, RAW 37.780 -> 37.782; compare_structure 11723 / 172 / 626 and every other gate EXACT; every verifier RESULT identical."
    sk = d["skeleton"]; sk["mean_scaffold_pct"] = 53.695; sk["raw_mean_pct"] = 37.782
    sk["_note_r397"] = "Round 397: SCAFFOLD 53.6835 -> 53.6953 (+0.012pp; 80 movers, 70 up / 7 down, pp-sum +23.6 - ENGJ403_6_0 -0.9 / ENGI405_6_0 -0.8 English pages whose gold keeps the bold), >=50 1163, >=75 195, >=90 18, median 54.3, RAW 37.782; SCOPED regeneration of the 58 affected modules. State outputs/_s26_r397_sk_final.json."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r397")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_s26_r397_finalise.py" not in s:
    A = "| `_s26_r396_widgetwrap.py` + `.out`"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_s26_r397_bubbles.py` + `.out` + `_s26_r397_bubbles2.py` + `.out` + `_s26_r397_bubbles3.py` + `.out` (the speech bubble's grouping, tail class × character image, the gold's samples — declined) / `_s26_r397_thb.py` + `.out` (bold inside `<th>`, gold vs Claude, per group) / `_s26_r397_splice.py` (the PICK + the data + engine splice) / `_s26_r397_probe.cjs` + `_s26_r397_probe_run.sh` + their OFF / ON logs + `_s26_r397_on/` / `_s26_r397_pagescore.py` + `_s26_r397_onscore.json` / `_s26_r397_batches.sh` + `_s26_r397_regen_run.sh` + the batch logs / `_s26_r397_fresh.log` + `_s26_r397_manifest_diff.log` + `_s26_r397_regen_vs_probe.log` / `_s26_r397_gates.sh` + `.log` + `_s26_r397_sk_final.json` + `_s26_r397_sk_full.log` + `_s26_r397_skdelta.py` + `_s26_r397_sk_delta.log` / `_s26_r397_postship.sh` + the selftest / fast-loop / manifest / index logs / `_s26_r397_ledger.log` / `_diff_miner_s26_r397.log` + `_diff_queue_pre_r397.md` + `_s26_r397_qdelta.py` + `_s26_r397_queue_delta.log` / `_s26_r397_entry.md` + `_s26_r397_finalise.py` + `_s26_r397_checksums.sh` | "
           + loc + " | Session 26 Round 11 (engine r397, build 260619.68) — a table header cell is plain: the position-free census (the gold's th plain 0.96; Claude's bold 0.18 on 86 pages), the probe (OFF 2109 / 2109; ON 92 pages / 58 modules, 73 up / 7 down, +23.0), the scoped regen + gates (skeleton 53.684 → 53.695; every other gate EXACT), the miner re-mine (173 rows, unchanged), the finalise; the speech bubble's character image measured and declined. |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r397 row")
print("finalise done")
