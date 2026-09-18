#!/usr/bin/env python3
"""ROUND 387 (loop session 26 Round 1 — the whakatauki does not close its column) — finalise: changelog (entry text in
_s26_r387_entry.md), AppVersion (260619.57 -> 260619.58), CLAUDE.md §9 / §11 / §14, gate_baseline.json, loop/README.md.
Idempotent; LF preserved. Run under WSL: python3 _s26_r387_finalise.py"""
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
ENTRY = rd(os.path.join(HERE, "_s26_r387_entry.md")).replace("\r\n", "\n")
if not ENTRY.endswith("\n\n"): ENTRY = ENTRY.rstrip("\n") + "\n\n"
if "round 387, build 260619.58" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r387 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.58"' not in s:
    old = '\tstatic AppVersion = "260619.57";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, "\t// ROUND 387 (260619.58): the whakatauki does not close its column — the commentary paragraph after the proverb flows on inside the same col-md-8 (callouts.flow_after_tags, env WHFLOW_OFF; ContentConverter.#flowsAfter at both after-box breakRow sites). Standard template, NCEA1 excluded; the gold 0.70 / paired 0.81 on 35 pages; 63 pages / 59 modules; scoped ship #7 since the r377 full.\n\tstatic AppVersion = \"260619.58\";")
    wr(P, s); print("Config.js: 260619.58")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "`WHFLOW_OFF` | 387" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 386 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 387 BASELINE (the whakataukī does not close its column — the commentary paragraph after the proverb flows on inside the same col-md-8; 59 modules; SCOPED regeneration of the 59, the probe proving the other 357 byte-identical; scoped ship #7 since the r377 full — the next ship is the FULL backstop): SCAFFOLD mean 53.395% / >=50% 1152 / >=75% 189 / >=90% 15 / RAW 37.688% @ 1956 pairs, pairs skipped 0 — hold-or-improve; 62 movers (54 up, 8 down — the 8 = the family's gold-BREAK minority, named in the r387 changelog: OSAI201_0_0 −3.4, SSCI205_0_0 −2.8, HPRE203_0_0 −2.6, the rest ≤ 1.0). compare_structure 11643 / 172 / 625 EXACT; body_compare 42 / 4 / 173 / 218 EXACT.** Previous — ROUND 386 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `PANELH2_OFF` | 385 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `WHFLOW_OFF` | 387 | **THE WHAKATAUKĪ DOES NOT CLOSE ITS COLUMN** (the autonomous loop's session 26 Round 1 — the score-band ledger `_s26_ledger2.py` + the after-block census extended to every block type `_s26_after2.py` / `_s26_before2.py`, paired by `_s26_whpair.py`). The r51 `row_breaks.after` rule closes the section row after every boxed callout; the gold's `div.whakatauki` OPENS its column (FIRST-in-column 0.78) but the writer's commentary paragraph after the proverb flows on INSIDE the same col-md-8 (Standard followed-on 0.70 over 81 boxes / 57 pages / 51 modules; PAIRED to the very next text FLOW 35 / BREAK 8 = 0.81 on 35 pages / 35 modules; Online Safety 0.92, Leaving to Learn 4 / 1, ConnectED 3 / 0). Every other box type agrees with r51 or is a tie (alert 0.74 LAST, alert.solid 0.90, alert.top 0.97, alertActivity 0.99, activity 1.00; img / table / video ties). Data `callouts.flow_after_tags {enabled, env, tags: [whakatauki], templates: [Standard], exclude_subjects: [NCEA1]}` — `ContentConverter.#flowsAfter(tag, run)` reads the module's `module_meta` template_type / subject; a listed tag skips the after-box `breakRow()` at BOTH sites (the strict box and the CONTAINER_CLOSE of a spanning box); the break BEFORE the box is unchanged. NCEA1 excluded (paired 1 / 3 — the HIS 'The whakataukī chosen for this module…' paragraph opens a gold row; census 0.56 = a tie); Inquiry / Bilingual not listed (gold LAST 5 / 5 each). OFF = the r386 output (probe 2109 / 2109). 63 pages / 59 modules; skeleton +0.043pp, ≥50 +1, ≥75 +4; every other gate EXACT. |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.57` (round 386"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.58` (round 387 — **the whakataukī does not close its column: the commentary paragraph after the proverb flows on inside the same col-md-8** (`callouts.flow_after_tags`, env `WHFLOW_OFF`; `ContentConverter.#flowsAfter` at both after-box breakRow sites); the autonomous loop's session 26 Round 1 — found by the score-band ledger + the after-block census extended to every block type (the whakataukī the ONE block whose gold after-rule contradicts r51: gold followed-on 0.70, paired 0.81 on 35 pages / 35 modules; NCEA1 excluded, Inquiry / Bilingual not listed); 63 pages / 59 modules changed; SCOPED regeneration of the 59 (the probe proving the other 357 byte-identical; scoped ship #7 since the r377 full — the next ship is the FULL backstop); skeleton 53.351 → 53.395 % (+0.043pp; 62 movers 54 up / 8 down — the 8 the family's gold-BREAK minority, named), ≥50 1151 → 1152, ≥75 185 → 189, ≥90 15, RAW 37.675 → 37.688 %; every other gate EXACT). Previous: `260619.57` (round 386"
             + OLD14[len("- **Build:** `260619.57` (round 386"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r387" not in d["_meta"]:
    d["_meta"]["build"] = "260619.58"; d["_meta"]["round"] = 387; d["_meta"]["date"] = "2026-09-19"
    d["_meta"]["_note_r387"] = "Round 387: the whakatauki does not close its column (63 pages / 59 modules; scoped ship #7 since the r377 full). Skeleton 53.351 -> 53.395 (+0.043pp; 62 movers 54 up / 8 down, pp-sum +84.7), >=50 1151 -> 1152, >=75 185 -> 189, >=90 15, RAW 37.675 -> 37.688; every other gate EXACT."
    sk = d["skeleton"]; sk["mean_scaffold_pct"] = 53.395; sk["median_scaffold_pct"] = 54.0; sk["pages_ge_50"] = 1152; sk["pages_ge_75"] = 189; sk["pages_ge_90"] = 15; sk["raw_mean_pct"] = 37.688
    sk["_note_r387"] = "Round 387: SCAFFOLD 53.3513 -> 53.3946 (+0.043pp; 62 movers, 54 up / 8 down, pp-sum +84.7 - the 8 dips the whakatauki family's gold-BREAK minority: OSAI201_0_0 -3.4, SSCI205_0_0 -2.8, HPRE203_0_0 -2.6, EXBP901_2_0 -1.0, OSBY401_0_0 -0.8, CEDO301_0_0 -0.7, EXIP901_5_0 -0.6, CEDW501_1_0 -0.3), >=50 1152, >=75 189, >=90 15, RAW 37.688; SCOPED regeneration of the 59 whakatauki modules, the probe proving the other 357 byte-identical. State outputs/_s26_r387_sk_final.json."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r387")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_s26_r387_finalise.py" not in s:
    A = "| `_s24_panelhead.py` + `_s24_panelhead2.py`"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_s26_ledger2.py` + `.out` (the s25 loss ledger by the gate's own SCORE BAND, the chrome family split by region / signature / modules) / `_s26_menucensus.py` + `_s26_menudeficit.py` + `_s26_menu_peek.py` (the module-menu list-form census and the lesson-menu li deficit located: repeat / editorial / WT) / `_s26_extrarow.py` (every Claude EXTRA row whose text matched, on pages ≥ 0.60, keyed by what closed the previous row) / `_s26_after2.py` + `_s26_before2.py` + `_s26_after_wh.py` (the after- / before-block census extended to every block type) / `_s26_whpair.py` (the PAIRED whakataukī after-rule) / `_s26_r387_splice.py` (the engine splice) / `_s26_r387_probe.cjs` + `_s26_r387_probe_run.sh` + their OFF / ON logs + `_s26_r387_on/` / `_s26_r387_pagescore.py` + `_s26_r387_onscore.json` / `_s26_r387_batches.sh` + `_s26_r387_regen_run.sh` + the batch logs / `_s26_r387_fresh.log` + `_s26_r387_regen_vs_probe.log` / `_s26_r387_gates.sh` + `.log` + `_s26_r387_sk_final.json` + `_s26_r387_sk_full.log` / `_s26_r387_postship.sh` + `_s26_r387_selftests.log` + `_s26_r387_fastloop_snapshot.log` + `_s26_r387_manifest_snapshot.log` + `_s26_r387_index.log` / `_s26_r387_ledger.log` / `_s26_r387_entry.md` + `_s26_r387_finalise.py` + `_s26_r387_checksums.sh` | "
           + loc + " | Session 26 Round 1 (engine r387, build 260619.58) — the whakataukī does not close its column: the score-band ledger + the extended after-block census (gold followed-on 0.70; paired 0.81 on 35 pages / 35 modules), the probe (OFF 2109 / 2109; ON 63 pages / 59 modules, 54 up / 8 down, pp-sum +84.7), the scoped regen + gates (skeleton 53.351 → 53.395, ≥75 185 → 189; every other gate EXACT), the finalise. |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r387 row")
print("finalise done")
