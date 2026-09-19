#!/usr/bin/env python3
"""ROUND 400 (loop session 27 Round 5 — the un-numbered activity opener takes the next positional letter) — finalise:
changelog (entry text in _s27_r400_entry.md), CLAUDE.md §9 / §11 / §14, gate_baseline.json, loop/README.md.
(Config.js AppVersion 260619.71 was edited directly with the Edit tool.) Idempotent; LF preserved.
Run under WSL: python3 _s27_r400_finalise.py"""
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
ENTRY = rd(os.path.join(HERE, "_s27_r400_entry.md")).replace("\r\n", "\n")
if not ENTRY.endswith("\n\n"): ENTRY = ENTRY.rstrip("\n") + "\n\n"
if "round 400, build 260619.71" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r400 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
assert '"260619.71"' in s, "Config.js not bumped"

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "`ACTUNNUM_OFF` | 400" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 399 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 400 BASELINE (the un-numbered activity opener takes the next positional letter — "
            "`activity_wrapper.lesson_letter_number.unnumbered_positional`; 94 modules; SCOPED regeneration of the 94, the probe proving the other 322 byte-identical; "
            "scoped ship #4 since the r396 full): SCAFFOLD mean 53.979% / >=50% 1174 / >=75% 200 / >=90% 18 / RAW 37.995% @ 1956 pairs, pairs skipped 0 — hold-or-improve; "
            "80 movers (67 up, 13 down — ENGI201_2_0 −11.3 the r369 letter-shift class on a page whose gold has four boxes to Claude's two, MXFL203_3_0 −6.1, HIS1005_4_0 −5.3, "
            "ANZH301_7_0 −4.5, the rest ≤ 2.8 — named). compare_structure 11798 / 172 / 626 EXACT; body_compare 42 / 4 / 173 / 218 EXACT.** Previous — ROUND 399 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `WANANGA_OFF` | 399 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `ACTUNNUM_OFF` | 400 | **THE UN-NUMBERED ACTIVITY OPENER TAKES THE NEXT POSITIONAL LETTER** (the autonomous loop's session 27 Round 5 — the position-free label "
             "census's EXTRA `div.activity` 529 lines / 265 pages, the gold 6 numberless boxes in 2385 pages; `_s27_r5_numberless.py` / `_s27_r5_posnum.py`). A writer's bare "
             "`[Activity]` / `[Activity: Embedded]` / `[interactive] …` opener with no id shipped a plain `div.activity` (629 on the paired pages) because the r88 rule lettered only "
             "an id-carrying opener and the r217 synthetic box; the gold numbers every box `{lesson}{letter}`. Measured on the paired lesson pages where both sides ship the same box "
             "count: the positional k-th letter is the gold's on 69 / 101 = 0.68 (NCEA1 0.65, Leaving to Learn 0.67, Mathematics 0.86). Data "
             "`activity_wrapper.lesson_letter_number.unnumbered_positional {enabled, env}` — `ActivitiesBuilder.activityOpen` enters an id-less opener into the letter counter under "
             "the r217 gate (`#pageLessonNumber != null`, the r325 phase pages included) and gives it the next letter; writer-lettered ids, bare-digit renumbering and pages without a "
             "lesson number unchanged. OFF = the r399 output (probe 2109 / 2109). 281 pages / 94 modules; skeleton +0.118pp (67 up / 13 down — the dips the r369 letter-shift class, "
             "named), ≥50 +4, ≥75 +3; compare_structure / body_compare / every verifier EXACT. |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.70` (round 399"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.71` (round 400 — **the un-numbered activity opener takes the next positional letter** (a writer's bare `[Activity]` / `[Activity: Embedded]` / "
             "`[interactive] …` opener on a numbered-lesson page ships `number=\"{lesson}{letter}\"` like every other box; `activity_wrapper.lesson_letter_number.unnumbered_positional`, "
             "env `ACTUNNUM_OFF`; KB 01F / 03A, constraint 62); the autonomous loop's session 27 Round 5 — found by the position-free label census's EXTRA side (`div.activity` 529 lines, "
             "the gold 6); 281 pages / 94 modules changed; SCOPED regeneration of the 94 (scoped ship #4 since the r396 full); skeleton 53.862 → 53.979 % (+0.118pp; 80 movers 67 up / 13 "
             "down, named), ≥50 1170 → 1174, ≥75 197 → 200, ≥90 18, RAW 37.918 → 37.995 %; compare_structure / body_compare / every verifier EXACT). Previous: `260619.70` (round 399"
             + OLD14[len("- **Build:** `260619.70` (round 399"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r400" not in d["_meta"]:
    d["_meta"]["build"] = "260619.71"; d["_meta"]["round"] = 400; d["_meta"]["date"] = "2026-09-19"
    d["_meta"]["_note_r400"] = ("Round 400: the un-numbered activity opener takes the next positional letter (281 pages / 94 modules; scoped ship #4 since the r396 full). "
                               "Skeleton 53.862 -> 53.979 (+0.118pp; 80 movers 67 up / 13 down, named), >=50 1170 -> 1174, >=75 197 -> 200, >=90 18, RAW 37.918 -> 37.995; "
                               "compare_structure 11798 / 172 / 626 EXACT; every other gate EXACT; every verifier RESULT identical to r399.")
    sk = d["skeleton"]; sk["mean_scaffold_pct"] = 53.979; sk["raw_mean_pct"] = 37.995; sk["pages_ge_50"] = 1174
    if "pages_ge_75" in sk: sk["pages_ge_75"] = 200
    sk["_note_r400"] = ("Round 400: SCAFFOLD 53.8616 -> 53.9791 (+0.118pp; 80 movers, 67 up / 13 down, pp-sum +230.0 — ENGI201_2_0 -11.3, MXFL203_3_0 -6.1, HIS1005_4_0 -5.3, "
                        "ANZH301_7_0 -4.5, ENGI203_10_0 -2.8, ANZH301_2_0 -2.6, ANZH301_4_0 -2.3, the rest <= 1.4: the r369 letter-shift class), >=50 1170 -> 1174, >=75 197 -> 200, "
                        ">=90 18; RAW 37.918 -> 37.995; 1956 pairs / 0 skipped.")
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r400")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_s27_r400_finalise.py" not in s:
    A = "| `_s27_r2_alertclass.py` + `.out` (THE PAIRED CALLOUT-CLASS CENSUS"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_s27_r4_ddhead.cjs` + `.json` + `_s27_r4_dddump.cjs` (the D10-3 dragAndDrop lane: every un-built table-less D&D bundle, the items after it, the gold verdict; the per-module "
           "bundle dump) / `_s27_r4_emptyhead.py` / `_s27_r4_col12md12.py` / `_s27_r4_brseries.py` + `.json` / `_s27_r4_goldbr.py` / `_s27_r4_brjoin.py` / `_s27_r4_pkinds.py` (+ their "
           "`.out`; the Round-4 PICK pass — the `<br>` follow-up closed, the widened wrapper re-declined, the missing `<p>` decomposed) / `_s27_r4_pass.md` + `_s27_r4_loopstate.py` + "
           "`_s27_r4_commit.txt` / `_s27_r5_orderloss.py` + `.json` + `.out` + `_s27_r5_skdiff.py` (the per-page ORDER-loss ranking + the opcode diff) / `_s27_r5_col8.py` + `.out` / "
           "`_s27_r5_numberless.py` + `.out` (CLAUDE'S NUMBERLESS ACTIVITY BOXES by page kind / content / gold verdict — the round's instrument) / `_s27_r5_posnum.py` + `.out` (the "
           "positional-letter rule tested against the gold's numbers) / `_s27_r5_parse1.cjs` / `_s27_r400_pick.md` + `_s27_r400_inprogress.py` / `_s27_r400_probe.cjs` + "
           "`_s27_r400_probe_run.sh` + their OFF / ON logs + `_s27_r400_on/` / `_s27_r400_pagescore.py` + `_s27_r400_onscore.json` / `_s27_r400_batches.sh` + `_s27_r400_regen_run.sh` + "
           "the batch logs / `_s27_r400_regen_vs_probe.log` / `_s27_r400_gates.sh` + `.log` + `_s27_r400_sk_final.json` + `_s27_r400_sk_full.log` + `_s27_r400_skdelta.py` + "
           "`_s27_r400_sk_delta.log` / `_s27_r400_postship.sh` + the selftest / fast-loop / manifest / index logs / `_diff_miner_s27_r400.log` + `_diff_queue_pre_r400.md` + "
           "`_s27_r400_qdelta.py` + `_s27_r400_queue_delta.log` / `_s27_r400_entry.md` + `_s27_r400_finalise.py` + `_s27_r400_checksums.sh` + `_s27_r400_loopstate.py` | "
           + loc + " | Session 27 Rounds 4–5 (engine r400, build 260619.71) — Round 4's PICK pass (the D10-3 build lane and the `<br>` follow-up measured to the floor) and Round 5's "
           "ship: the un-numbered activity opener takes the next positional letter — the numberless-box census (the round's instrument), the positional rule tested against the gold, "
           "the in-memory probe (OFF 2109 / 2109, ON 281 pages / 94 modules), the gate-scored ON pages (67 up / 13 down, +229.9), the scoped regeneration, the gates and the finalise. |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r400 row")
print("finalise done")
