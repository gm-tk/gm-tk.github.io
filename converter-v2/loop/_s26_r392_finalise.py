#!/usr/bin/env python3
"""ROUND 392 (loop session 26 Round 6 — adjacent sibling lists are one list) — finalise: changelog (entry text in
_s26_r392_entry.md), AppVersion (260619.62 -> 260619.63), CLAUDE.md §9 / §11 / §14, gate_baseline.json, loop/README.md.
Idempotent; LF preserved. Run under WSL: python3 _s26_r392_finalise.py"""
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
ENTRY = rd(os.path.join(HERE, "_s26_r392_entry.md")).replace("\r\n", "\n")
if not ENTRY.endswith("\n\n"): ENTRY = ENTRY.rstrip("\n") + "\n\n"
if "round 392, build 260619.63" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r392 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.63"' not in s:
    old = '\tstatic AppVersion = "260619.62";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, "\t// ROUND 392 (260619.63): adjacent sibling lists are one list — a bare </ul> + whitespace + <ul> in the live body joins (body_region.merge_adjacent_lists, ListsAndRuns.MergeAdjacentLists at the TypedNumberList seam, env ULMERGE_OFF; Claude 106 pairs on 54 pages vs the gold's 3 = 0.97; ol deliberately not listed). 51 pages / 32 modules; scoped ship #4 since the r388 full.\n\tstatic AppVersion = \"260619.63\";")
    wr(P, s); print("Config.js: 260619.63")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "`ULMERGE_OFF` | 392" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 391 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 392 BASELINE (adjacent sibling lists are one list — `body_region.merge_adjacent_lists`; 32 modules; SCOPED regeneration of the 32, the probe proving the other 384 byte-identical; scoped ship #4 since the r388 full): SCAFFOLD mean 53.554% / >=50% 1160 / >=75% 191 / >=90% 15 / RAW 37.785% @ 1956 pairs, pairs skipped 0 — hold-or-improve; 38 movers (35 up, 2 down — SSOG103_0_0 −0.9, ENGI103_1_0 −0.5, both alignment shifts where the gold keeps its lists apart with paragraphs Claude does not emit). compare_structure 11723 / 172 / 626; body_compare 42 / 4 / 173 / 218 EXACT.** Previous — ROUND 391 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `PANELCOL_OFF` | 391 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `ULMERGE_OFF` | 392 | **ADJACENT SIBLING LISTS ARE ONE LIST** (the autonomous loop's session 26 Round 6 — the r391 miner's one new row #4286 `body EXTRA div.col-12.col-md-12 › ul` decomposed: XDLS904 / 905 / 906's panel bullets each end in an inline `[link to X]` marker that renders nothing, splitting the black run into two `<ul>`s). The census `_s26_r392_adjul.py` over every paired page's LIVE body (cv2 dumps / notes / r337 verbatim widgets carved out): Claude 106 adjacent `</ul> <ul>` pairs on 54 pages / 34 modules, the gold 3 on 3 pages = 0.97 one list (LtL 27, NCEA1 20, English 18, TEDC 17, Fundamentals 7, Maths 6, ConnectED 5, Arts 3); every splitting mechanism (inline marker, consumed item, an image between bullets) ends in the same gold form. Data `body_region.merge_adjacent_lists {enabled, env, tags: [ul]}` — `ListsAndRuns.MergeAdjacentLists(html)`, a full-page post-pass at the r337 seam (PageAssembler after TypedNumberList, before the link-text pass; the same verbatim zones): a bare `</ul>` + whitespace + a bare `<ul>` becomes the whitespace. `ol` deliberately NOT listed (Claude 202 pairs / gold 0 — a Word numbering restart is a NEW list; measure the gold's restart form first). OFF = the r391 output (probe 2109 / 2109). 51 pages / 32 modules; skeleton +0.028pp, ≥50 +2, compare_structure exact +23; every other gate EXACT. |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.62` (round 391"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.63` (round 392 — **adjacent sibling lists are one list** (`body_region.merge_adjacent_lists`, `ListsAndRuns.MergeAdjacentLists`, env `ULMERGE_OFF`); the autonomous loop's session 26 Round 6 — the r391 miner's one new row decomposed (Claude 106 adjacent `</ul> <ul>` pairs on 54 pages / 34 modules vs the gold's 3 = 0.97 one list; `ol` not taken — a restart is a new list); 51 pages / 32 modules changed; SCOPED regeneration of the 32 (scoped ship #4 since the r388 full); skeleton 53.525 → 53.554 % (+0.028pp; 38 movers 35 up / 2 down, named), ≥50 1158 → 1160, ≥75 191, ≥90 15, RAW 37.762 → 37.785 %; compare_structure exact 11700 → 11723; every other gate EXACT; the miner re-mined 177 CANDIDATE rows (#4286 gone, #3682 under the floor, one new #660 `activity SUBSTITUTED div.row › div.col-12 / div.row` at the 20-page floor — an alignment artefact, measure first)). Previous: `260619.62` (round 391"
             + OLD14[len("- **Build:** `260619.62` (round 391"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r392" not in d["_meta"]:
    d["_meta"]["build"] = "260619.63"; d["_meta"]["round"] = 392; d["_meta"]["date"] = "2026-09-19"
    d["_meta"]["_note_r392"] = "Round 392: adjacent sibling lists are one list (51 pages / 32 modules; scoped ship #4 since the r388 full). Skeleton 53.525 -> 53.554 (+0.028pp; 38 movers 35 up / 2 down, pp-sum +55.5), >=50 1158 -> 1160, >=75 191, >=90 15, RAW 37.762 -> 37.785; compare_structure exact 11700 -> 11723 (MISSING 625 -> 626); every other gate EXACT."
    sk = d["skeleton"]; sk["mean_scaffold_pct"] = 53.554; sk["median_scaffold_pct"] = 54.0; sk["pages_ge_50"] = 1160; sk["pages_ge_75"] = 191; sk["pages_ge_90"] = 15; sk["raw_mean_pct"] = 37.785
    sk["_note_r392"] = "Round 392: SCAFFOLD 53.5253 -> 53.5537 (+0.028pp; 38 movers, 35 up / 2 down, pp-sum +55.5 - SSOG103_0_0 -0.9 / ENGI103_1_0 -0.5 alignment shifts), >=50 1160 (AGH1006_5_0, XDLS905_2_0 up), >=75 191, >=90 15, RAW 37.785; SCOPED regeneration of the 32 affected modules. State outputs/_s26_r392_sk_final.json."
    cs = d.get("compare_structure")
    if isinstance(cs, dict):
        for k, v in (("exact_chain", 11723), ("claude_missing_container", 626)):
            if k in cs: cs[k] = v
        cs["_note_r392"] = "Round 392: exact 11700 -> 11723; EXTRA 172; MISSING 625 -> 626; row-wrap 23."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n")
    print("gate_baseline.json: r392;", "compare_structure keys:", [k for k in cs if not k.startswith("_")] if isinstance(cs, dict) else "no cs block")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_s26_r392_finalise.py" not in s:
    A = "| `_s26_r391_panelcol.py` + `.out`"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_s26_r392_adjul.py` + `.out` (adjacent `</ul> <ul>` pairs in every paired page's live body, Claude vs gold, per template / subject) / `_s26_r392_splice.py` (the PICK + the data + engine splice) / `_s26_r392_probe.cjs` + `_s26_r392_probe_run.sh` + their OFF / ON logs + `_s26_r392_on/` / `_s26_r392_pagescore.py` + `_s26_r392_onscore.json` / `_s26_r392_batches.sh` + `_s26_r392_regen_run.sh` + the batch logs / `_s26_r392_fresh.log` + `_s26_r392_manifest_diff.log` + `_s26_r392_regen_vs_probe.log` / `_s26_r392_gates.sh` + `.log` + `_s26_r392_sk_final.json` + `_s26_r392_sk_full.log` + `_s26_r392_skdelta.py` + `_s26_r392_sk_delta.log` / `_s26_r392_postship.sh` + the selftest / fast-loop / manifest / index logs / `_s26_r392_ledger.log` / `_diff_miner_s26_r392.log` + `_diff_queue_pre_r392.md` + `_s26_r392_qdelta.py` + `_s26_r392_queue_delta.log` / `_s26_r392_entry.md` + `_s26_r392_finalise.py` + `_s26_r392_checksums.sh` | "
           + loc + " | Session 26 Round 6 (engine r392, build 260619.63) — adjacent sibling lists are one list: the r391 miner row #4286 decomposed (Claude 106 pairs / gold 3 = 0.97 on 54 pages), the probe (OFF 2109 / 2109; ON 51 pages / 32 modules, 40 up / 5 down, +48.2), the scoped regen + gates (skeleton 53.525 → 53.554, ≥50 +2, compare_structure exact +23; every other gate EXACT), the miner re-mine (177 rows; #4286 gone, #660 new at the floor), the finalise. |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r392 row")
print("finalise done")
