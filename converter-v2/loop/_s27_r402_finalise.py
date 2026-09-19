#!/usr/bin/env python3
"""ROUND 402 (loop session 27 Round 7 — the [interactive: video] line is the box's first lead element) — finalise:
changelog (entry text in _s27_r402_entry.md), CLAUDE.md §9 / §11 / §14, gate_baseline.json, loop/README.md.
(Config.js AppVersion 260619.73 was edited directly with the Edit tool.) Idempotent; LF preserved.
Run under WSL: python3 _s27_r402_finalise.py"""
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
ENTRY = rd(os.path.join(HERE, "_s27_r402_entry.md")).replace("\r\n", "\n")
if not ENTRY.endswith("\n\n"): ENTRY = ENTRY.rstrip("\n") + "\n\n"
if "round 402, build 260619.73" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r402 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
assert '"260619.73"' in s, "Config.js not bumped"

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "`OWNERALIAS_OFF` | 402" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 401 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 402 BASELINE = r401 page-for-page (the `[interactive: video]` line is the box's first "
            "lead element — `opener_rule.owner_alias_exclude`; 3 modules / 12 pages, every change a `cv2-note`; SCOPED regeneration of the 3, the probe proving the other 413 "
            "byte-identical; scoped ship #6 since the r396 full): SCAFFOLD mean 53.989% / >=50% 1174 / >=75% 200 / >=90% 18 / RAW 38.000% @ 1956 pairs, pairs skipped 0 — "
            "hold-or-improve; 0 movers. compare_structure 11798 / 172 / 626 EXACT; body_compare 42 / 4 / 173 / 218 EXACT.** Previous — ROUND 401 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `SABOXEMPTY_OFF` | 401 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `OWNERALIAS_OFF` | 402 | **THE `[interactive: video]` LINE BEFORE A WIDGET IS THE BOX'S FIRST LEAD ELEMENT, NOT ITS SWALLOWED OPENER** (the autonomous loop's "
             "session 27 Round 7 — recorded at the r401 ship). `[interactive: video]` parses to `video` as the primary with a second `activity` tag whose alias word is "
             "`interactive`; the scanner's owner lookback takes any span carrying an `activity` tag as the following widget's owner, so the AGH writer's video line became the "
             "drag-and-drop's owner and was rendered as the box opener — the video request vanished without a note. Measured through the live scanner over all 416 "
             "(`_s27_r7_ownerscan.cjs`): 128 non-activity-primary owners, 20 with the `interactive` alias (14 `[interactive: video]` on AGH1004 / AGH1005 / AGH1006). Two "
             "variants scored with the gate's own `match()`: NOT an owner (the standalone widget) 4 up / 14 down −31.0 — the gold BOXES the group the line leads — DECLINED; the "
             "owner KEPT but the span rendered as the box's first LEAD element through the r364 lead_media path behind a synthetic bare opener — 14 same / 4 down, the dips the "
             "embedded image / list forms, so SCOPED by `element_tags` + `exclude_primary_hows` to the 14 `[interactive: video]` sites: gate-neutral, the video's `no URL` flag now "
             "surfaces inside the box (its URL is a Media-List item, the r292 class). Data `BoundaryBank._meta.opener_rule.owner_alias_exclude {enabled, env, alias_words, "
             "element_tags, exclude_primary_hows}`. OFF = the r401 output (probe 2109 / 2109). 12 pages / 3 modules; every gate EXACT, 0 skeleton movers. |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.72` (round 401"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.73` (round 402 — **the `[interactive: video]` line before a widget is the box's first lead element, not its swallowed opener** (the scanner's "
             "owner lookback keeps the span as the owner — the gold boxes the group it leads, the standalone form scored 4 up / 14 down — but renders it through the r364 lead_media "
             "path so the writer's video request surfaces; `BoundaryBank._meta.opener_rule.owner_alias_exclude`, env `OWNERALIAS_OFF`); the autonomous loop's session 27 Round 7 — "
             "the r401 recorded candidate measured over all 416 (128 non-activity-primary owners, 20 aliased); 12 pages / 3 AGH modules changed, every change a `cv2-note`; "
             "SCOPED regeneration of the 3 (scoped ship #6 since the r396 full); gate-neutral — skeleton 53.989 % / 1174 / 200 / 18 / RAW 38.000 % page-for-page, "
             "compare_structure / body_compare / every verifier EXACT). Previous: `260619.72` (round 401"
             + OLD14[len("- **Build:** `260619.72` (round 401"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r402" not in d["_meta"]:
    d["_meta"]["build"] = "260619.73"; d["_meta"]["round"] = 402; d["_meta"]["date"] = "2026-09-19"
    d["_meta"]["_note_r402"] = ("Round 402: the [interactive: video] line is the box's first lead element (12 pages / 3 modules, every change a cv2-note; scoped ship #6 since the "
                               "r396 full). Skeleton 53.989 / 1174 / 200 / 18 / RAW 38.000 page-for-page = r401 (0 movers); every other gate EXACT; every verifier RESULT identical to r401.")
    d["skeleton"]["_note_r402"] = "Round 402: 0 movers — the r401 state page-for-page (1956 pairs / 0 skipped)."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r402")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_s27_r402_finalise.py" not in s:
    A = "| `_s27_r6_numbers.py` + `.out` (the post-r400 activity-box census"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_s27_r7_pick.md` + `_s27_r7_inprogress.py` / `_s27_r7_ownerscan.cjs` + `_s27_r7_ownerscan_0*.log` + `_s27_r7_ownerscan.tsv` (EVERY BUNDLE WHOSE OWNER SPAN'S PRIMARY "
           "IS NOT `activity`, through the live scanner — the round's instrument) / `_s27_r402_probe.cjs` + `_s27_r402_probe_run.sh` + their OFF / ON logs + `_s27_r402_on/` / "
           "`_s27_r402_pagescore.py` + `_s27_r402_onscore.json` (the two variants scored — the standalone form 4 up / 14 down, declined; the lead-element form 14 same / 4 down, "
           "scoped) / `_s27_r402_batches.sh` + `_s27_r402_regen_run.sh` + the batch log / `_s27_r402_regen_vs_probe.log` / `_s27_r402_gates.sh` + `.log` + `_s27_r402_sk_final.json` "
           "+ `_s27_r402_sk_full.log` + `_s27_r402_skdelta.py` + `_s27_r402_sk_delta.log` / `_s27_r402_postship.sh` + the selftest / fast-loop / manifest / index logs / "
           "`_diff_miner_s27_r402.log` + `_diff_queue_pre_r402.md` + `_s27_r402_qdelta.py` + `_s27_r402_queue_delta.log` / `_s27_r402_entry.md` + `_s27_r402_finalise.py` + "
           "`_s27_r402_checksums.sh` + `_s27_r402_loopstate.py` | "
           + loc + " | Session 27 Round 7 (engine r402, build 260619.73) — the `[interactive: video]` line before a widget is the box's first lead element, not its swallowed "
           "opener: the owner-span census over all 416, the two variants probed and scored (the standalone form declined on the gold's own boxes), the scoped regeneration of the "
           "3 AGH modules (gate-neutral), the gates and the finalise. |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r402 row")
print("finalise done")
