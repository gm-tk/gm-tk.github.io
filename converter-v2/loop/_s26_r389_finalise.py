#!/usr/bin/env python3
"""ROUND 389 (loop session 26 Round 3 — the built flipCard group closes its column) — finalise: changelog (entry text in
_s26_r389_entry.md), AppVersion (260619.59 -> 260619.60), CLAUDE.md §9 / §11 / §14, gate_baseline.json, loop/README.md.
Idempotent; LF preserved. Run under WSL: python3 _s26_r389_finalise.py"""
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
ENTRY = rd(os.path.join(HERE, "_s26_r389_entry.md")).replace("\r\n", "\n")
if not ENTRY.endswith("\n\n"): ENTRY = ENTRY.rstrip("\n") + "\n\n"
if "round 389, build 260619.60" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r389 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.60"' not in s:
    old = '\tstatic AppVersion = "260619.59";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, "\t// ROUND 389 (260619.60): the built flipCard group closes its column — the prose after a built div.row.flipCardsContainer opens a new row (body_region.row_breaks.after_built_widgets, env FLIPBREAK_OFF; ContentConverter.#breaksAfterBuilt at the inline widget site). Standard template, Leaving to Learn / NCEA1 / 1-10 English excluded on the gate's own scorer; paired 0.82, the gold's LAST-or-only 0.75; 29 pages / 21 modules; scoped ship #1 since the r388 full.\n\tstatic AppVersion = \"260619.60\";")
    wr(P, s); print("Config.js: 260619.60")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "`FLIPBREAK_OFF` | 389" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 388 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 389 BASELINE (the built flipCard group closes its column — the prose after a built `div.row.flipCardsContainer` opens a new row; 21 modules; SCOPED regeneration of the 21, the probe proving the other 395 byte-identical; scoped ship #1 since the r388 full): SCAFFOLD mean 53.470% / >=50% 1157 / >=75% 191 / >=90% 15 / RAW 37.725% @ 1956 pairs, pairs skipped 0 — hold-or-improve; 29 movers (23 up, 6 down — the 6 = the family's gold-flow minority, named in the r389 changelog: OSAH301_1_0 −2.8 = the ≥75 down-crosser accepted BY NAME, OSOH101_3_0 −1.0, the rest ≤ 0.5). compare_structure 11643 / 172 / 625 EXACT; body_compare 42 / 4 / 173 / 218 EXACT.** Previous — ROUND 388 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `ALERTFLOW_OFF` | 388 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `FLIPBREAK_OFF` | 389 | **THE BUILT FLIPCARD GROUP CLOSES ITS COLUMN** (the autonomous loop's session 26 Round 3 — the r388 paired row-break census cut by the built widget's own signature, `_s26_r389_divpair.py`, + the gold-side position census `_s26_r389_flipgold.py`). The r51 `flow_blocks` rule keeps every built widget in the section row and lets the next prose flow on; the gold does that for every built widget but ONE — after a built flipCard group (`div.row.flipCardsContainer`) it closes the column and opens a new row for the prose: paired 23 / 5 = 0.82 (26 pages / 20 modules), the gold-side LAST-or-only 0.75 of 187 (English 0.87, Mathematics 0.93, ConnectED 0.82, Online Safety 0.82; Leaving to Learn 0.32). The reader's WIDGET kind (every other built widget) is a tie at 0.55 and keeps r51; the break BEFORE the group (FIRST-or-only 0.45) and the col-md-12 width (0.31) are not taken. Data `body_region.row_breaks.after_built_widgets {enabled, env, rules: [{class_match \\\\bflipCardsContainer\\\\b, templates [Standard], exclude_subjects [Leaving to Learn, NCEA1, 1-10 English]}]}` — `ContentConverter.#breaksAfterBuilt(html, run)` tests the built html's open-tag class + the module's `module_meta` template_type / subject; the INLINE widget site (`!stack.length`) calls `breakRow()` after a match; the bundle-owned site (inside an activity box) never breaks. The three subjects are excluded on the gate's own scorer over the probe's ON pages (LtL 0 up / 13 down, NCEA1 0 / 3, English 3 / 4 a tie — `_s26_r389_bysubject.log`). OFF = the r388 output (probe 2109 / 2109). 29 pages / 21 modules; skeleton +0.016pp, ≥50 +2, ≥75 −1 (OSAH301_1_0, named); every other gate EXACT. |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.59` (round 388"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.60` (round 389 — **the built flipCard group closes its column: the prose after a built `div.row.flipCardsContainer` opens a new row** (`body_region.row_breaks.after_built_widgets`, env `FLIPBREAK_OFF`; `ContentConverter.#breaksAfterBuilt` at the inline widget site); the autonomous loop's session 26 Round 3 — the r388 paired row-break census cut by the built widget's own signature (the flipCard group the ONE built widget whose after-rule the gold breaks: paired 0.82, the gold's LAST-or-only 0.75; every other built widget a tie at 0.55; Leaving to Learn / NCEA1 / 1-10 English excluded on the gate's own scorer); 29 pages / 21 modules changed; SCOPED regeneration of the 21 (the probe proving the other 395 byte-identical; scoped ship #1 since the r388 full); skeleton 53.455 → 53.470 % (+0.016pp; 29 movers 23 up / 6 down — the 6 the family's gold-flow minority, named), ≥50 1155 → 1157, ≥75 192 → 191 (OSAH301_1_0, named), ≥90 15, RAW 37.719 → 37.725 %; every other gate EXACT; the miner re-mined 177 CANDIDATE rows (178 → 177, 0 new)). Previous: `260619.59` (round 388"
             + OLD14[len("- **Build:** `260619.59` (round 388"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r389" not in d["_meta"]:
    d["_meta"]["build"] = "260619.60"; d["_meta"]["round"] = 389; d["_meta"]["date"] = "2026-09-19"
    d["_meta"]["_note_r389"] = "Round 389: the built flipCard group closes its column (29 pages / 21 modules; scoped ship #1 since the r388 full). Skeleton 53.455 -> 53.470 (+0.016pp; 29 movers 23 up / 6 down, pp-sum +30.7), >=50 1155 -> 1157, >=75 192 -> 191 (OSAH301_1_0 named), >=90 15, RAW 37.719 -> 37.725; every other gate EXACT."
    sk = d["skeleton"]; sk["mean_scaffold_pct"] = 53.470; sk["median_scaffold_pct"] = 54.0; sk["pages_ge_50"] = 1157; sk["pages_ge_75"] = 191; sk["pages_ge_90"] = 15; sk["raw_mean_pct"] = 37.725
    sk["_note_r389"] = "Round 389: SCAFFOLD 53.4546 -> 53.4702 (+0.016pp; 29 movers, 23 up / 6 down, pp-sum +30.7 - the 6 dips the flipCard family's gold-flow minority: OSAH301_1_0 -2.8 (76.2 -> 73.4, the >=75 down-crosser, accepted by name), OSOH101_3_0 -1.0, OSBY101_1_0 -0.5, OSOH401_1_0 -0.3, TEDC401_4_0 -0.2, TEDC402_2_0 -0.1), >=50 1157 (CEDO501_2_0 + MXFL301_1_0 cross up), >=75 191, >=90 15, RAW 37.725; SCOPED regeneration of the 21 flipCard modules, the probe proving the other 395 byte-identical. State outputs/_s26_r389_sk_final.json."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r389")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_s26_r389_finalise.py" not in s:
    A = "| `_s26_rowpair.py` + `.out` + `_s26_rowpair_alert.py`"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_s26_r389_divpair_gen.py` → `_s26_r389_divpair.py` + `.out` (the paired row-break census, direction B, cut by the FULL signature of the `div` kind) / `_s26_r389_flipgold_gen.py` → `_s26_r389_flipgold.py` + `.out` (the gold-side position + column census of every top-level flipCardsContainer; the paired before-rule) / `_s26_r389_pick.py` / `_s26_r389_splice.py` (the engine + data splice) / `_s26_r389_probe.cjs` + `_s26_r389_probe_run.sh` + their OFF / ON logs + `_s26_r389_on/` / `_s26_r389_pagescore.py` + `_s26_r389_onscore.json` + `_s26_r389_bysubject.log` + `_s26_r389_bysubject2.log` / `_s26_r389_batches.sh` + `_s26_r389_regen_run.sh` + the batch logs / `_s26_r389_fresh.log` + `_s26_r389_manifest_diff.log` + `_s26_r389_regen_vs_probe.log` / `_s26_r389_gates.sh` + `.log` + `_s26_r389_sk_final.json` + `_s26_r389_sk_full.log` + `_s26_r389_sk_delta.log` / `_s26_r389_postship.sh` + `_s26_r389_selftests.log` + `_s26_r389_fastloop_snapshot.log` + `_s26_r389_manifest_snapshot.log` + `_s26_r389_index.log` / `_s26_r389_ledger.log` / `_diff_miner_s26_r389.log` + `_diff_queue_pre_r389.md` + `_s26_r389_queue_delta.log` / `_s26_r389_entry.md` + `_s26_r389_finalise.py` + `_s26_r389_checksums.sh` | "
           + loc + " | Session 26 Round 3 (engine r389, build 260619.60) — the built flipCard group closes its column: the paired census by signature (gold breaks 0.82; the gold-side LAST-or-only 0.75, FIRST-or-only 0.45 a tie), the probe (OFF 2109 / 2109; ON first cut 54 pages 26 up / 26 down → three subjects excluded on the scorer → 29 pages / 21 modules, 23 up / 6 down, pp-sum +30.7), the scoped regen + gates (skeleton 53.455 → 53.470, ≥50 +2, ≥75 −1 named; every other gate EXACT), the miner re-mine (177 rows), the finalise. |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r389 row")
print("finalise done")
