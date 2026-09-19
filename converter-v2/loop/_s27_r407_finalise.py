#!/usr/bin/env python3
"""ROUND 407 (loop session 27 Round 12 — the heading-led numbered opener takes the owner form too) — finalise:
changelog (entry text in _s27_r407_entry.md), CLAUDE.md §9 / §11 / §14, gate_baseline.json, loop/README.md.
(Config.js AppVersion 260619.78 was edited directly with the Edit tool.) Idempotent; LF preserved.
Run under WSL: python3 _s27_r407_finalise.py"""
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
ENTRY = rd(os.path.join(HERE, "_s27_r407_entry.md")).replace("\r\n", "\n")
if not ENTRY.endswith("\n\n"): ENTRY = ENTRY.rstrip("\n") + "\n\n"
if "round 407, build 260619.78" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r407 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
assert '"260619.78"' in s, "Config.js not bumped"

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "`HEADLEDOWNER_OFF` | 407" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 406 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 407 BASELINE (the heading-led numbered opener takes the owner form too — "
            "`unclassified_activity_lead.heading_led_owner.empty_walk_owner`; 24 modules / 56 pages; SCOPED regeneration of the 24, the probe proving the other 392 byte-identical; "
            "scoped ship #2 since the r405 full): SCAFFOLD mean 54.084% / >=50% 1181 / >=75% 202 / >=90% 18 / RAW 38.022% @ 1956 pairs, pairs skipped 0 — hold-or-improve; 38 movers "
            "(32 up, 6 down — MXFUN01_6_2 −11.5 and MXFUN01_5_0 −5.9 the r362-named type-and-check tables now inside the hand-off box, AGH1008_3_0 −4.6 the gold has no box #2C, "
            "TEDC401_1_0 −1.6, MXEO401_3_0 −1.4, XTAS102_1_0 −0.9 — named). compare_structure exact 11779 (the text-matched pool 13813 → 13794, the r344 relocation class) / 172 / 626; "
            "body_compare 42 / 5 / 170 / 216 (runaway +1 = ENGI202_2_0 named; EMPTY −3 / ANY −2 IMPROVED).** Previous — ROUND 406 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `BAREACT_OFF` | 406 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `HEADLEDOWNER_OFF` | 407 | **THE HEADING-LED NUMBERED OPENER TAKES THE OWNER FORM TOO** (the autonomous loop's session 27 Round 12, the budget's last — Round 11's recorded "
             "follow-up measured by `_s27_r12_emptyowner.py`: 75 writer-owned EMPTY boxes on 53 pages / 31 modules — a numbered `[Activity N]` opener directly followed by an `[H2]`–`[H5]` "
             "heading kept the r362 / r363 MEMBER form, whose walk the heading ends at once, so the box shipped with the `no content captured` flag alone and the heading / prose / table "
             "free AFTER it; the gold's same-numbered box holds the section INSIDE — h3 + widget 43, h3 + prose 13, h3 + table 3, widget 2 = 0.81, absent 14). Data "
             "`unclassified_activity_lead.heading_led_owner.empty_walk_owner {enabled, env}` — when on, `member_form_tags` is ignored and every heading-led numbered opener takes the r362 "
             "owner form (opener → activityOwner, heading + prose → activityLeadItems, members from the first table; the converter's lead rendering promotes the heading to the box's "
             "`<h3>`). Scoped to the unclassified path; the typed-widget empty boxes (the normal path's, 20) are the recorded follow-up. OFF = the r406 output (probe 2109 / 2109). "
             "56 pages / 24 modules; skeleton +0.0583pp (32 up / 6 down — the r362-named MXFUN01 type-and-check tables −11.5 / −5.9, AGH1008_3_0 −4.6 the gold's absent box, named), "
             "≥50 +5, ≥75 +2; compare_structure exact −16 = the matched pool −19; body_compare runaway +1 (ENGI202_2_0, named) / EMPTY −3 / ANY −2; every other gate EXACT; the miner's "
             "`activity MISSING div.col-12 › h3` row dropped under the floor (169 → 168). |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.77` (round 406"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.78` (round 407 — **the heading-led numbered opener takes the owner form too** (the r362 / r363 member form kept for an h2–h5-led lead was an EMPTY "
             "box with the section free after it; the gold's same-numbered box holds h3 + widget / prose / table on 61 of 75 = 0.81; "
             "`unclassified_activity_lead.heading_led_owner.empty_walk_owner`, env `HEADLEDOWNER_OFF`); the autonomous loop's session 27 Round 12 (the budget's last); 56 pages / 24 "
             "modules changed; SCOPED regeneration of the 24 (scoped ship #2 since the r405 full); skeleton 54.025 → 54.084 % (+0.0583pp; 38 movers 32 up / 6 down, named), ≥50 1176 → "
             "1181, ≥75 200 → 202, ≥90 18, RAW 38.012 → 38.022 %; compare_structure exact 11779 (pool −19) / 172 / 626; body_compare 42 / 5 / 170 / 216 (runaway +1 named, EMPTY −3, "
             "ANY −2); every verifier EXACT; miner 169 → 168). Previous: `260619.77` (round 406"
             + OLD14[len("- **Build:** `260619.77` (round 406"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r407" not in d["_meta"]:
    d["_meta"]["build"] = "260619.78"; d["_meta"]["round"] = 407; d["_meta"]["date"] = "2026-09-19"
    d["_meta"]["_note_r407"] = ("Round 407: the heading-led numbered opener takes the owner form too (56 pages / 24 modules; SCOPED regeneration of the 24, scoped ship #2 since the "
                               "r405 full). Skeleton 54.025 -> 54.084 (+0.0583pp; 38 movers 32 up / 6 down, named), >=50 1176 -> 1181, >=75 200 -> 202, >=90 18, RAW 38.012 -> "
                               "38.022; compare_structure exact 11779 (the text-matched pool 13813 -> 13794) / 172 / 626; body_compare over-capture 42, runaway 4 -> 5 (ENGI202_2_0, "
                               "named), EMPTY 173 -> 170, ANY 218 -> 216; every other gate EXACT; every verifier RESULT identical to r406.")
    sk = d["skeleton"]; sk["mean_scaffold_pct"] = 54.084; sk["raw_mean_pct"] = 38.022; sk["pages_ge_50"] = 1181
    if "pages_ge_75" in sk: sk["pages_ge_75"] = 202
    sk["_note_r407"] = ("Round 407: SCAFFOLD 54.0253 -> 54.0836 (+0.0583pp; 38 movers, 32 up / 6 down, pp-sum +114.0 — MXFUN01_6_2 -11.5, MXFUN01_5_0 -5.9, AGH1008_3_0 -4.6, "
                        "TEDC401_1_0 -1.6, MXEO401_3_0 -1.4, XTAS102_1_0 -0.9), >=50 1181, >=75 202, >=90 18; RAW 38.012 -> 38.022; 1956 pairs / 0 skipped.")
    if "compare_structure" in d and isinstance(d["compare_structure"], dict):
        cs = d["compare_structure"]
        for k in ("exact", "exact_chain", "exact_wrapper_chain"):
            if k in cs and cs[k] == 11795: cs[k] = 11779
        cs["_note_r407"] = "Round 407: exact 11795 -> 11779 = the text-matched pool 13813 -> 13794 (the r344 relocation class); EXTRA 172 / MISSING 626 EXACT."
    if "body_compare" in d and isinstance(d["body_compare"], dict):
        bc = d["body_compare"]
        for k, old, new in (("runaway", 4, 5), ("empty", 173, 170), ("any", 218, 216), ("any_breakdown", 218, 216), ("empty_widgets", 173, 170)):
            if k in bc and bc[k] == old: bc[k] = new
        bc["_note_r407"] = "Round 407: runaway 4 -> 5 (ENGI202_2_0 — the 2A owner-form walk absorbs table + list + bubble, named), EMPTY 173 -> 170, ANY 218 -> 216, over-capture 42."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r407")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_s27_r407_finalise.py" not in s:
    A = "| `_s27_r11_bareact.out` + `_s27_r11_pick.md`"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_s27_r12_emptyowner.py` + `.out` + `_s27_r12_pick.md` + `_s27_r12_inprogress.py` / `_s27_r407_probe.cjs` + `_s27_r407_probe_run.sh` + their OFF / ON logs + "
           "`_s27_r407_on/` / `_s27_r407_pagescore.py` + `.out` + `_s27_r407_onscore.json` / `_s27_r407_affected.txt` + `_s27_r407_batches.sh` + `_s27_r407_regen_run.sh` + "
           "`_s27_r407_batch_N.log` / `_s27_r407_gates.sh` + `.log` + `_s27_r407_regen_vs_probe.log` + `_s27_r407_sk_final.json` + `_s27_r407_sk_full.log` + `_s27_r407_skdelta.py` + "
           "`.out` / `_s27_r407_postship.sh` + the selftest / fast-loop / manifest / index logs / `_diff_miner_s27_r407.log` + `_diff_queue_pre_r407.md` + `_s27_r407_qdelta.py` + "
           "`_s27_r407_queue_delta.log` / `_s27_r407_entry.md` + `_s27_r407_finalise.py` + `_s27_r407_checksums.sh` + `_s27_r407_loopstate.py` | "
           + loc + " | Session 27 Round 12 (engine r407, build 260619.78) — the heading-led numbered opener takes the owner form too: the census (75 writer-owned empty boxes, the gold "
           "boxes the section 0.81), the probe (OFF 2109 / 2109, ON 56 pages / 24 modules), the gate-scored ON pages (32 up / 6 down, +114.0), the scoped regeneration of the 24 "
           "(0 stale, probe == disk 197 / 197), the gates and the finalise. |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r407 row")
print("finalise done")
