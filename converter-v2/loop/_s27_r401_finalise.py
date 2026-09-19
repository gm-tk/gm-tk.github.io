#!/usr/bin/env python3
"""ROUND 401 (loop session 27 Round 6 — no synthetic activity box around a widget that captured nothing) — finalise:
changelog (entry text in _s27_r401_entry.md), CLAUDE.md §9 / §11 / §14, gate_baseline.json, loop/README.md.
(Config.js AppVersion 260619.72 was edited directly with the Edit tool.) Idempotent; LF preserved.
Run under WSL: python3 _s27_r401_finalise.py"""
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
ENTRY = rd(os.path.join(HERE, "_s27_r401_entry.md")).replace("\r\n", "\n")
if not ENTRY.endswith("\n\n"): ENTRY = ENTRY.rstrip("\n") + "\n\n"
if "round 401, build 260619.72" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r401 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
assert '"260619.72"' in s, "Config.js not bumped"

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "`SABOXEMPTY_OFF` | 401" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 400 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 401 BASELINE (no synthetic activity box around a widget that captured nothing — "
            "`activity_wrapper.standalone_widget_box.skip_empty`; 22 modules; SCOPED regeneration of the 22, the probe proving the other 394 byte-identical; "
            "scoped ship #5 since the r396 full): SCAFFOLD mean 53.989% / >=50% 1174 / >=75% 200 / >=90% 18 / RAW 38.000% @ 1956 pairs, pairs skipped 0 — hold-or-improve; "
            "26 movers (22 up, 4 down — XLP05_5_0 −1.0, AGH1004_6_0 −0.9, AGH1006_2_0 −0.7, TEDC401_4_0 −0.6: pages whose gold ships a numbered box with the widget BUILT where "
            "Claude's empty box had matched its line by coincidence — the capture class, named). compare_structure 11798 / 172 / 626 EXACT; body_compare 42 / 4 / 173 / 218 EXACT.** "
            "Previous — ROUND 400 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `ACTUNNUM_OFF` | 400 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `SABOXEMPTY_OFF` | 401 | **NO SYNTHETIC ACTIVITY BOX AROUND A WIDGET THAT CAPTURED NOTHING** (the autonomous loop's session 27 Round 6 — the post-r400 activity-box "
             "census `_s27_r6_numbers.py` → `_s27_r6_claudeboxes.py` → `_s27_r6_emptybox.py`: 98 note-only boxes on 74 paired pages, 89 of them the `no content captured` flag; the gold "
             "ships 4 empty boxes in 2385 pages). The r217 standalone box wrapped every task-type bundle, including one whose invocation captured nothing (a tag-only `[drag and drop]` / "
             "`[radio quiz]` whose title heading terminated the walk, an inline marker, a stray end tag) — the page carried `div.activity.interactive[number=6B] > row > col-12 > p.cv2-note` "
             "and nothing else, and the box SPENT a positional letter so every later box on the page was lettered one too far (AGH1006 4A / 4B / 4C vs the gold's 4A / 4B). Data "
             "`activity_wrapper.standalone_widget_box.skip_empty {enabled, env}` — the placeholder's own emptiness test (headingText / instructions / tables / media / a member with words "
             "or the r342 embedded text) is factored verbatim into `ContentConverter.#bundleEmbeddedText` / `#bundleItemHasText` / `#bundleHasContent` (the placeholder byte-identical by "
             "construction) and `saOn` declines a content-less bundle: the flag renders alone in the section flow, no box, no letter. A writer's OWN opener owning an empty bundle keeps "
             "its box (the gold ships that box with the widget built — the capture class). OFF = the r400 output (probe 2109 / 2109). 27 pages / 22 modules; skeleton +0.0095pp (22 up / "
             "4 down, named), buckets EXACT; compare_structure / body_compare / every verifier EXACT. Recorded: the `[interactive: video]` bracket resolves an `activity` tag and the "
             "scanner's owner lookback takes it as the following widget's OWNER (AGH1005 lesson 2 — the video never renders, the box opens empty; a primary-tag fence, its own round). |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.71` (round 400"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.72` (round 401 — **no synthetic activity box around a widget that captured nothing** (the r217 standalone box consults the placeholder's own content "
             "test; a content-less bundle renders its `no content captured` flag alone in the section flow and spends no positional letter; "
             "`activity_wrapper.standalone_widget_box.skip_empty`, env `SABOXEMPTY_OFF`; KB 01F, constraint 62 / 65); the autonomous loop's session 27 Round 6 — found by the post-r400 "
             "activity-box census (98 note-only boxes on the paired pages, the gold 4 in 2385); 27 pages / 22 modules changed; SCOPED regeneration of the 22 (scoped ship #5 since the "
             "r396 full); skeleton 53.979 → 53.989 % (+0.0095pp; 26 movers 22 up / 4 down, named), ≥50 1174, ≥75 200, ≥90 18 EXACT, RAW 37.995 → 38.000 %; compare_structure / "
             "body_compare / every verifier EXACT). Previous: `260619.71` (round 400"
             + OLD14[len("- **Build:** `260619.71` (round 400"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r401" not in d["_meta"]:
    d["_meta"]["build"] = "260619.72"; d["_meta"]["round"] = 401; d["_meta"]["date"] = "2026-09-19"
    d["_meta"]["_note_r401"] = ("Round 401: no synthetic activity box around a widget that captured nothing (27 pages / 22 modules; scoped ship #5 since the r396 full). "
                               "Skeleton 53.979 -> 53.989 (+0.0095pp; 26 movers 22 up / 4 down, named), >=50 1174, >=75 200, >=90 18 EXACT, RAW 37.995 -> 38.000; "
                               "compare_structure 11798 / 172 / 626 EXACT; every other gate EXACT; every verifier RESULT identical to r400.")
    sk = d["skeleton"]; sk["mean_scaffold_pct"] = 53.989; sk["raw_mean_pct"] = 38.000; sk["pages_ge_50"] = 1174
    if "pages_ge_75" in sk: sk["pages_ge_75"] = 200
    sk["_note_r401"] = ("Round 401: SCAFFOLD 53.9791 -> 53.9886 (+0.0095pp; 26 movers, 22 up / 4 down, pp-sum +18.4 — XLP05_5_0 -1.0, AGH1004_6_0 -0.9, AGH1006_2_0 -0.7, "
                        "TEDC401_4_0 -0.6: the gold ships a numbered box with the widget built where Claude's empty box had matched its line), >=50 1174, >=75 200, >=90 18; "
                        "RAW 37.995 -> 38.000; 1956 pairs / 0 skipped.")
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r401")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_s27_r401_finalise.py" not in s:
    A = "| `_s27_r4_ddhead.cjs` + `.json` + `_s27_r4_dddump.cjs`"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_s27_r6_numbers.py` + `.out` (the post-r400 activity-box census: count relations + k-th verdicts) / `_s27_r6_goldboxes.py` + `.out` (the gold's extra boxes — invented "
           "titles) / `_s27_r6_claudeboxes_gen.py` → `_s27_r6_claudeboxes.py` + `.out` (Claude's extra boxes by kind) / `_s27_r6_journalsec.py` + `.out` (the journal-button section, "
           "under the floor) / `_s27_r6_emptybox.py` + `.out` (THE NOTE-ONLY ACTIVITY BOXES — the round's instrument) / `_s27_r401_emptybox_off.py` + `_s27_r401_emptybox_on.py` + "
           "their `.out` (the census on the disk vs the probe's ON pages: 98 → 78) / `_s27_r401_pick.md` + `_s27_r401_inprogress.py` / `_s27_r401_probe.cjs` + `_s27_r401_probe_run.sh` "
           "+ their OFF / ON logs + `_s27_r401_on/` + `_s27_r401_changed_pages.txt` / `_s27_r401_pagescore.py` + `_s27_r401_onscore.json` / `_s27_r401_batches.sh` + "
           "`_s27_r401_regen_run.sh` + the batch logs / `_s27_r401_regen_vs_probe.log` / `_s27_r401_gates.sh` + `.log` + `_s27_r401_sk_final.json` + `_s27_r401_sk_full.log` + "
           "`_s27_r401_skdelta.py` + `_s27_r401_sk_delta.log` / `_s27_r401_postship.sh` + the selftest / fast-loop / manifest / index logs / `_diff_miner_s27_r401.log` + "
           "`_diff_queue_pre_r401.md` + `_s27_r401_qdelta.py` + `_s27_r401_queue_delta.log` / `_s27_r401_entry.md` + `_s27_r401_finalise.py` + `_s27_r401_checksums.sh` + "
           "`_s27_r401_loopstate.py` | "
           + loc + " | Session 27 Round 6 (engine r401, build 260619.72) — no synthetic activity box around a widget that captured nothing: the note-only-box census (the round's "
           "instrument), the in-memory probe (OFF 2109 / 2109, ON 27 pages / 22 modules), the gate-scored ON pages (22 up / 4 down, +18.5), the census re-run on the ON pages "
           "(98 → 78), the scoped regeneration, the gates and the finalise. |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r401 row")
print("finalise done")
