#!/usr/bin/env python3
"""ROUND 399 (loop session 27 Round 2 — the wānanga / talanoa box is the KB's cultural alert) — finalise:
changelog (entry text in _s27_r399_entry.md), CLAUDE.md §9 / §11 / §14, gate_baseline.json, loop/README.md.
(Config.js AppVersion 260619.70 was edited directly with the Edit tool.) Idempotent; LF preserved.
Run under WSL: python3 _s27_r399_finalise.py"""
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
ENTRY = rd(os.path.join(HERE, "_s27_r399_entry.md")).replace("\r\n", "\n")
if not ENTRY.endswith("\n\n"): ENTRY = ENTRY.rstrip("\n") + "\n\n"
if "round 399, build 260619.70" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r399 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
assert '"260619.70"' in s, "Config.js not bumped"

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "`WANANGA_OFF` | 399" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 398 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 399 BASELINE (the wānanga / talanoa box is the KB's cultural alert — "
            "`callouts.by_tag.wananga.kb_form` + `table_cell_content` + the `tag_promote` carousel→wananga rule; 6 modules; SCOPED regeneration of the 6, the probe "
            "proving the other 410 byte-identical; scoped ship #3 since the r396 full): SCAFFOLD mean 53.862% / >=50% 1170 / >=75% 197 / >=90% 18 / RAW 37.918% @ 1956 pairs, "
            "pairs skipped 0 — hold-or-improve; 44 movers (39 up, 5 down — CEDT501_7_0 −4.4 the gold's flow-after minority, CEDT501_2_0 −1.9 the gold's box-inside-the-activity "
            "minority, CEDT501_5_0 −1.4, CEDW501_2_1 −0.5, CEDT501_6_0 −0.3 — named). compare_structure exact 11723 → 11798 (+75 IMPROVED) / 172 / 626 EXACT; "
            "body_compare 42 / 4 / 173 / 218 EXACT.** Previous — ROUND 398 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `VIDEOICONWIDGET_OFF` | 398 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `WANANGA_OFF` | 399 | **THE WĀNANGA / TALANOA BOX IS THE KB'S CULTURAL ALERT** (the autonomous loop's session 27 Round 2 — the paired callout-class census "
             "`_s27_r2_alertclass.py` → `_s27_r2_wananga.py` / `_s27_r2_callouttbl.py`). The CED Phase-5 writers type `[Wānanga/Talanoa box]` (+ `[Wananga box]`, "
             "`[Talanoa/Wananga box]`, typos, CEDT501's `[Banner - Wānanga/Talanoa box]`) then a ONE-CELL table holding the prompt; the gold renders every one as KB 05B's "
             "Cultural Alert `<div class=\"alert cultural\" layout=\"combined\"> > row > col-12 > p…` (63 / 63 combined — KB 14A §14.4: 'all alerts are combined unless otherwise "
             "specified'; a bulleted cell → `<ul>`; no h4). Claude shipped an EMPTY `div.wananga` + a red flag + the table as a kept `<table>` (56 flags / 35 pages / 6 modules); "
             "measured over every callout tag typed bare + a one-cell table on all 416 WTs the idiom is exactly this class (55 sites / 6 modules / 37 gold pages, gold `alert "
             "cultural` 50 = 0.91). Data `callouts.by_tag.wananga.kb_form {open, close, wrap_content}` (the def swap in `#calloutOpen`; the legacy `div.wananga` is the OFF form) + "
             "`.table_cell_content` (STRICT mode: an empty gather + a next one-row one-cell table → the cell through `TablesAndGrids.renderCellParts`, the table consumed; "
             "`#calloutWrapsStructured` yields via the new `#calloutTableCell`) + `Tag_Lexicon._meta.tag_promote` carousel→wananga on the `[Banner - Wānanga…` spelling "
             "(`clear_remainder`; `[Rolling Banner - …]` excluded). OFF = the r398 output (probe 2109 / 2109). 47 pages / 6 modules; skeleton +0.103pp, ≥50 +4, ≥75 +2; "
             "compare_structure exact +75; every other gate EXACT, every verifier RESULT identical. Recorded: the 2 / 74 gold boxes inside an activity (the CONTAINER_OPEN "
             "auto-close class), the 15 / 74 flow-after minority. |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.69` (round 398"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.70` (round 399 — **the wānanga / talanoa box is the KB's cultural alert** (the CED Phase-5 writer's `[Wānanga/Talanoa box]` + one-cell table → "
             "`div.alert.cultural[layout=combined] > row > col-12 > p…`; `callouts.by_tag.wananga.kb_form` + `table_cell_content`, the `tag_promote` carousel→wananga rule for "
             "the `[Banner - …]` spelling, env `WANANGA_OFF`; KB 05B + 14A §14.4); the autonomous loop's session 27 Round 2 — found by the paired callout-class census; "
             "47 pages / 6 modules changed; SCOPED regeneration of the 6 (scoped ship #3 since the r396 full); skeleton 53.759 → 53.862 % (+0.103pp; 44 movers 39 up / 5 down, "
             "named), ≥50 1166 → 1170, ≥75 195 → 197, ≥90 18, RAW 37.846 → 37.918 %; compare_structure exact 11723 → 11798 (+75); every other gate EXACT, every verifier RESULT "
             "identical). Previous: `260619.69` (round 398"
             + OLD14[len("- **Build:** `260619.69` (round 398"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r399" not in d["_meta"]:
    d["_meta"]["build"] = "260619.70"; d["_meta"]["round"] = 399; d["_meta"]["date"] = "2026-09-19"
    d["_meta"]["_note_r399"] = ("Round 399: the wananga / talanoa box is the KB cultural alert (47 pages / 6 modules; scoped ship #3 since the r396 full). "
                               "Skeleton 53.759 -> 53.862 (+0.103pp; 44 movers 39 up / 5 down, named), >=50 1166 -> 1170, >=75 195 -> 197, >=90 18, RAW 37.846 -> 37.918; "
                               "compare_structure exact 11723 -> 11798 (+75), EXTRA 172 / MISSING 626 EXACT; every other gate EXACT; every verifier RESULT identical to r398.")
    sk = d["skeleton"]; sk["mean_scaffold_pct"] = 53.862; sk["raw_mean_pct"] = 37.918; sk["pages_ge_50"] = 1170
    if "pages_ge_75" in sk: sk["pages_ge_75"] = 197
    sk["_note_r399"] = ("Round 399: SCAFFOLD 53.7589 -> 53.8616 (+0.103pp; 44 movers, 39 up / 5 down, pp-sum +200.9 — CEDT501_7_0 -4.4 the gold's flow-after minority, "
                        "CEDT501_2_0 -1.9 the gold's box-inside-the-activity minority, CEDT501_5_0 -1.4, CEDW501_2_1 -0.5, CEDT501_6_0 -0.3), >=50 1166 -> 1170, >=75 195 -> 197, >=90 18; "
                        "RAW 37.846 -> 37.918; 1956 pairs / 0 skipped.")
    cs = d.get("compare_structure")
    if isinstance(cs, dict):
        for k in ("exact", "exact_chain", "exact_wrapper_chain"):
            if k in cs: cs[k] = 11798
        cs["_note_r399"] = "Round 399: exact 11723 -> 11798 (+75 — the cultural box's <p>s text-match the gold's); EXTRA 172 / MISSING 626 EXACT."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r399")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_s27_r399_finalise.py" not in s:
    A = "| `_s27_condense.py` + `_s27_startnote.py` + `_s27_insert_section.py`"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_s27_r2_alertclass.py` + `.out` (THE PAIRED CALLOUT-CLASS CENSUS — every gold callout box paired to the Claude box holding the same opening words, class-set × class-set "
           "by group) / `_s27_r2_brcensus.py` + `.out` / `_s27_r2_col12.py` + `.out` / `_s27_r2_acttail.py` + `_s27_r2_acttail2.py` + `.out` (the Round-2 PICK pass: the gold `<br>`, "
           "the `col-12.col-md-12` column, the bare activity opener's id-in-tail — all measured and declined / recorded) / `_s27_r2_wananga.py` + `.out` (the wānanga tag sites → gold "
           "→ Claude) / `_s27_r2_callouttbl.py` + `.out` (every callout tag typed bare + a one-cell table, all 416 WTs) / `_s27_r2_parse.cjs` + `_s27_r2_parse2.cjs` (the live parse of "
           "every bracket spelling) / `_s27_r399_pick.md` / `_s27_r399_inprogress.py` / `_s27_r399_patch.py` (the data + engine edits, exact-string, LF) / `_s27_r399_probe.cjs` + "
           "`_s27_r399_probe_run.sh` + their OFF / ON logs + `_s27_r399_on/` / `_s27_r399_pagescore.py` + `_s27_r399_onscore.json` / `_s27_r399_flow.py` + `_s27_r399_flow2.py` (the "
           "row-break + inside-activity census on the gold's cultural boxes) / `_s27_r399_batches.sh` + `_s27_r399_regen_run.sh` + the batch log / `_s27_r399_regen_vs_probe.log` / "
           "`_s27_r399_gates.sh` + `.log` + `_s27_r399_sk_final.json` + `_s27_r399_sk_full.log` + `_s27_r399_skdelta.py` + `_s27_r399_sk_delta.log` / `_s27_r399_postship.sh` + the "
           "selftest / fast-loop / manifest / index logs / `_s27_r399_ledger.log` / `_diff_miner_s27_r399.log` + `_diff_queue_pre_r399.md` + `_s27_r399_qdelta.py` + "
           "`_s27_r399_queue_delta.log` / `_s27_r399_entry.md` + `_s27_r399_finalise.py` + `_s27_r399_checksums.sh` + `_s27_r399_loopstate.py` | "
           + loc + " | Session 27 Round 2 (engine r399, build 260619.70) — the wānanga / talanoa box is the KB's cultural alert: the paired callout-class census (the round's "
           "instrument), the tag-site trace, the bare-callout + one-cell-table generalisation, the in-memory probe (OFF 2109 / 2109, ON 47 pages / 6 modules), the gate-scored "
           "ON pages (39 up / 5 down, +200.8), the scoped regeneration, the gates and the finalise. |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r399 row")
print("finalise done")
