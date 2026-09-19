#!/usr/bin/env python3
"""ROUND 406 (loop session 27 Round 11 — the bracket-less red `Activity 4A` line is the `[Activity 4A]` opener) — finalise:
changelog (entry text in _s27_r406_entry.md), CLAUDE.md §9 / §11 / §14, gate_baseline.json, loop/README.md.
(Config.js AppVersion 260619.77 was edited directly with the Edit tool.) Idempotent; LF preserved.
Run under WSL: python3 _s27_r406_finalise.py"""
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
ENTRY = rd(os.path.join(HERE, "_s27_r406_entry.md")).replace("\r\n", "\n")
if not ENTRY.endswith("\n\n"): ENTRY = ENTRY.rstrip("\n") + "\n\n"
if "round 406, build 260619.77" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r406 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
assert '"260619.77"' in s, "Config.js not bumped"

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "`BAREACT_OFF` | 406" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 405 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 406 BASELINE (the bracket-less red `Activity 4A` line is the `[Activity 4A]` opener — "
            "`opener_rule.bare_red_opener`; 7 modules / 15 pages; SCOPED regeneration of the 7, the probe proving the other 409 byte-identical; scoped ship #1 since the r405 full): "
            "SCAFFOLD mean 54.025% / >=50% 1176 / >=75% 200 / >=90% 18 / RAW 38.012% @ 1956 pairs, pairs skipped 0 — hold-or-improve; 12 movers (9 up, 3 down — ENGS302_6_0 −4.0 "
            "the scorer's alignment on a page whose gold boxes 6C too, PES1001_10_0 −3.6 the gold's colon-split title, PES1001_1_0 −1.9 the gold's own un-boxed 1B, named). "
            "compare_structure exact 11795 (the text-matched pool 13814 → 13813, the r344 relocation class) / 172 / 626; body_compare 42 / 4 / 173 / 218 EXACT.** Previous — ROUND 405 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `JOURNALBOX_OFF` | 405 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `BAREACT_OFF` | 406 | **THE BRACKET-LESS RED `Activity 4A` LINE IS THE `[Activity 4A]` OPENER** (the autonomous loop's session 27 Round 11 — Round 10's recorded "
             "follow-up, `_s27_r11_bareact.out`: 36 sites / 14 modules on the parsed WTs, 27 on the 8 tracked ones, the gold's box count exceeding Claude's on every one — ENGI102 16 vs 9, "
             "PES1001 20 vs 9, TWHA902 27 vs 1). A writer colours the opener red but types no brackets (`🔴Activity 4A🔴` + `[H4] Check your understanding` + a red instruction + the "
             "answer table — ENGI102 lesson 8, whose gold ships `activity interactive 4A` with the built dragAndDrop); the span parses as noise with no primary and the box never opens. "
             "Data `BoundaryBank._meta.opener_rule.bare_red_opener {enabled, env, pattern}` — `InteractiveScanner.#bareRedOpeners` (a pre-pass beside `#idHeadingOpeners`) re-parses a "
             "tag-less, primary-less red span whose ENTIRE folded text matches the pattern (`activity <id>`, optional bold markers / colon) in place as the typed `[Activity <ID>]` opener; "
             "every downstream rule then sees a typed opener (the r148 bare-lead class — a whole-span exact predicate cannot over-fire on prose; a table-cell line is not an item; a "
             "title-tailed line is the r377 word form's). OFF = the r405 output (probe 2109 / 2109). 15 pages / 7 modules; skeleton +0.0244pp (9 up / 3 down, named), ≥50 +1; every "
             "other gate EXACT (compare_structure exact −1 = the matched pool −1). Recorded: the re-parsed opener + `[H4]` + instruction + `[Body]` + table takes the r362 MEMBER form "
             "(an empty box + the section free after it) where the gold's box holds h3 + p + the built widget — the owner form for a drag-and-drop-instructed lead is the measured "
             "follow-up. |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.76` (round 405"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.77` (round 406 — **the bracket-less red `Activity 4A` line is the `[Activity 4A]` opener** (a red span with no resolved tag whose entire folded text "
             "is the word + id is re-parsed in place as the typed opener; `InteractiveScanner.#bareRedOpeners`, `opener_rule.bare_red_opener`, env `BAREACT_OFF`); the autonomous "
             "loop's session 27 Round 11 — 36 sites / 14 modules on the parsed WTs, the gold's box count exceeding Claude's on every tracked one; 15 pages / 7 modules changed; SCOPED "
             "regeneration of the 7 (scoped ship #1 since the r405 full); skeleton 54.001 → 54.025 % (+0.0244pp; 12 movers 9 up / 3 down, named), ≥50 1175 → 1176, ≥75 200, ≥90 18, "
             "RAW 38.008 → 38.012 %; compare_structure exact 11795 (pool −1) / 172 / 626; body_compare / every verifier EXACT; the plateau window RESET). Previous: `260619.76` (round 405"
             + OLD14[len("- **Build:** `260619.76` (round 405"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r406" not in d["_meta"]:
    d["_meta"]["build"] = "260619.77"; d["_meta"]["round"] = 406; d["_meta"]["date"] = "2026-09-19"
    d["_meta"]["_note_r406"] = ("Round 406: the bracket-less red `Activity 4A` line is the `[Activity 4A]` opener (15 pages / 7 modules; SCOPED regeneration of the 7, scoped ship #1 "
                               "since the r405 full). Skeleton 54.001 -> 54.025 (+0.0244pp; 12 movers 9 up / 3 down, named), >=50 1175 -> 1176, >=75 200, >=90 18, RAW 38.008 -> 38.012; "
                               "compare_structure exact 11795 (the text-matched pool 13814 -> 13813) / 172 / 626; every other gate EXACT; every verifier RESULT identical to r405.")
    sk = d["skeleton"]; sk["mean_scaffold_pct"] = 54.025; sk["raw_mean_pct"] = 38.012; sk["pages_ge_50"] = 1176
    if "pages_ge_75" in sk: sk["pages_ge_75"] = 200
    sk["_note_r406"] = ("Round 406: SCAFFOLD 54.0009 -> 54.0253 (+0.0244pp; 12 movers, 9 up / 3 down, pp-sum +47.8 — ENGS302_6_0 -4.0, PES1001_10_0 -3.6, PES1001_1_0 -1.9), "
                        ">=50 1176 (PES1001_2_0 up), >=75 200, >=90 18; RAW 38.008 -> 38.012; 1956 pairs / 0 skipped.")
    if "compare_structure" in d and isinstance(d["compare_structure"], dict):
        cs = d["compare_structure"]
        for k in ("exact", "exact_chain", "exact_wrapper_chain"):
            if k in cs and cs[k] == 11796: cs[k] = 11795
        cs["_note_r406"] = "Round 406: exact 11796 -> 11795 = the text-matched pool 13814 -> 13813 (the r344 relocation class); EXTRA 172 / MISSING 626 EXACT."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r406")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_s27_r406_finalise.py" not in s:
    A = "| `_s27_r10_pick.md` + `_s27_r10_inprogress.py`"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_s27_r11_bareact.out` + `_s27_r11_pick.md` + `_s27_r11_inprogress.py` / `_s27_r11_itemdump.cjs` + `_s27_r11_movedata.py` (the item dump that found the "
           "config-level miss + the data relocation) / `_s27_r406_probe.cjs` + `_s27_r406_probe_run.sh` + their OFF / ON logs + `_s27_r406_on/` / `_s27_r406_pagescore.py` + `.out` / "
           "`_s27_r406_affected.txt` + `_s27_r406_batches.sh` + `_s27_r406_regen_run.sh` + `_s27_r406_batch_N.log` / `_s27_r406_gates.sh` + `.log` + `_s27_r406_regen_vs_probe.log` + "
           "`_s27_r406_sk_final.json` + `_s27_r406_sk_full.log` + `_s27_r406_skdelta.py` + `.out` / `_s27_r406_postship.sh` + the selftest / fast-loop / manifest / index logs / "
           "`_diff_miner_s27_r406.log` + `_diff_queue_pre_r406.md` + `_s27_r406_qdelta.py` + `_s27_r406_queue_delta.log` / `_s27_r406_entry.md` + `_s27_r406_finalise.py` + "
           "`_s27_r406_checksums.sh` + `_s27_r406_loopstate.py` | "
           + loc + " | Session 27 Round 11 (engine r406, build 260619.77) — the bracket-less red `Activity 4A` line is the `[Activity 4A]` opener: the probe (OFF 2109 / 2109, "
           "ON 15 pages / 7 modules — after the item dump found the data block one level too deep), the gate-scored ON pages (9 up / 3 down, +47.8), the scoped regeneration of "
           "the 7 (0 stale, probe == disk 39 / 39), the gates and the finalise. |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r406 row")
print("finalise done")
