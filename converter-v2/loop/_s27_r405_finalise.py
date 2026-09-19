#!/usr/bin/env python3
"""ROUND 405 (loop session 27 Round 10 — the journal section is an activity box; the FULL-regeneration backstop) — finalise:
changelog (entry text in _s27_r405_entry.md), CLAUDE.md §9 / §11 / §14, gate_baseline.json, loop/README.md.
(Config.js AppVersion 260619.76 was edited directly with the Edit tool.) Idempotent; LF preserved.
Run under WSL: python3 _s27_r405_finalise.py"""
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
ENTRY = rd(os.path.join(HERE, "_s27_r405_entry.md")).replace("\r\n", "\n")
if not ENTRY.endswith("\n\n"): ENTRY = ENTRY.rstrip("\n") + "\n\n"
if "round 405, build 260619.76" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r405 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
assert '"260619.76"' in s, "Config.js not bumped"

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "`JOURNALBOX_OFF` | 405" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 403 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 405 BASELINE (the journal section is an activity box — "
            "`opener_rule.id_heading_opener.journal_section`; 5 modules / 11 pages; a FULL regeneration of all 416 (the ledger's backstop after seven scoped ships), 0 stale, "
            "the manifest diff = the round's 11 pages exactly — no residue from r397–r403): SCAFFOLD mean 54.001% / >=50% 1175 / >=75% 200 / >=90% 18 / RAW 38.008% @ 1956 pairs, "
            "pairs skipped 0 — hold-or-improve; 9 movers (6 up, 2 down — XGF9006_2_0 −0.3, XGF9006_6_0 −0.2, named). compare_structure exact 11796 (the text-matched pool "
            "13816 → 13814, the r344 relocation class) / 172 / 626; body_compare 42 / 4 / 173 / 218 EXACT.** Previous — ROUND 403 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `SIDECOLSUBJ_OFF` | 404 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `JOURNALBOX_OFF` | 405 | **THE JOURNAL SECTION IS AN ACTIVITY BOX** (the autonomous loop's session 27 Round 10 — Round 6's `_s27_r6_journalsec.py`: every free "
             "heading section on Claude's paired pages holding a journal / activity-id button, the gold's rendering of that heading — 1-10 English gold:box 15 / 17 = 0.88, "
             "Leaving to Learn 9 / 10 = 0.90; NCEA1 0.50 / Mathematics 0.45 ties, EXPlore's gold drops the heading). A writer's free `[H3] Title` + prose + `[button] Go to journal` "
             "(no `[Activity]` opener) shipped free; the gold boxes the task. Data `opener_rule.id_heading_opener.journal_section {enabled, env, subjects, heading_tags, stop_tags, "
             "max_items}` — `InteractiveScanner.#idHeadingOpeners` re-tags such a free h2–h4 heading as a bare `[Activity]` opener when its section (before the next heading / opener / "
             "section marker / table / widget invocation) carries a `[button]` `#isGoJournalButton` recognises, in a listed subject: the heading's words are the box title, the r400 "
             "positional letter numbers it, r239 puts the goJournal h4 inside; a heading directly after a writer's `[Activity]` opener is never re-tagged. OFF = the r404 output "
             "(probe 2109 / 2109). 11 pages / 5 modules; skeleton +0.0032pp (6 up / 2 down, named); every other gate EXACT (compare_structure exact −2 = the matched pool −2). "
             "Shipped as THE FULL-REGENERATION BACKSTOP (scoped #7 since r396 → full): all 416 rebuilt, 0 stale, the manifest diff = the probe's 11 pages. |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.75` (round 404"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.76` (round 405 — **the journal section is an activity box** (a free h2–h4 heading whose section ends in a go-to-journal `[button]` is re-tagged as "
             "a bare `[Activity]` opener in English / Leaving to Learn, where the gold boxes it 0.88 / 0.90; `opener_rule.id_heading_opener.journal_section`, env `JOURNALBOX_OFF`); "
             "the autonomous loop's session 27 Round 10; 11 pages / 5 modules changed; **THE FULL-regeneration backstop** — all 416 rebuilt (36 batches rc 0), 0 stale, the manifest "
             "diff = the round's 11 pages exactly (no residue from the seven scoped ships r397–r403), the ledger's scoped counter reset to 0; skeleton 53.998 → 54.001 % (+0.0032pp; "
             "9 movers 6 up / 2 down, named), ≥50 1175, ≥75 200, ≥90 18 EXACT, RAW 38.006 → 38.008 %; compare_structure exact 11796 (pool −2) / 172 / 626; body_compare / every "
             "verifier EXACT). Previous: `260619.75` (round 404"
             + OLD14[len("- **Build:** `260619.75` (round 404"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r405" not in d["_meta"]:
    d["_meta"]["build"] = "260619.76"; d["_meta"]["round"] = 405; d["_meta"]["date"] = "2026-09-19"
    d["_meta"]["_note_r405"] = ("Round 405: the journal section is an activity box (11 pages / 5 modules; the FULL-regeneration backstop — all 416 rebuilt, 0 stale, no residue "
                               "from r397–r403; scoped counter reset). Skeleton 53.998 -> 54.001 (+0.0032pp; 9 movers 6 up / 2 down, named), >=50 1175, >=75 200, >=90 18, "
                               "RAW 38.006 -> 38.008; compare_structure exact 11796 (the text-matched pool 13816 -> 13814) / 172 / 626; every other gate EXACT; every verifier "
                               "RESULT identical to r403.")
    sk = d["skeleton"]; sk["mean_scaffold_pct"] = 54.001; sk["raw_mean_pct"] = 38.008; sk["pages_ge_50"] = 1175
    if "pages_ge_75" in sk: sk["pages_ge_75"] = 200
    sk["_note_r405"] = ("Round 405: SCAFFOLD 53.9977 -> 54.0009 (+0.0032pp; 9 movers, 6 up / 2 down, pp-sum +6.4 — XGF9006_2_0 -0.3, XGF9006_6_0 -0.2), >=50 1175, >=75 200, "
                        ">=90 18; RAW 38.006 -> 38.008; 1956 pairs / 0 skipped.")
    if "compare_structure" in d and isinstance(d["compare_structure"], dict):
        cs = d["compare_structure"]
        for k in ("exact", "exact_chain", "exact_wrapper_chain"):
            if k in cs and cs[k] == 11798: cs[k] = 11796
        cs["_note_r405"] = "Round 405: exact 11798 -> 11796 = the text-matched pool 13816 -> 13814 (the r344 relocation class); EXTRA 172 / MISSING 626 EXACT."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r405")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_s27_r405_finalise.py" not in s:
    A = "| `_s27_r9_sidepair.py` + `.out`"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_s27_r10_pick.md` + `_s27_r10_inprogress.py` / `_s27_r405_probe.cjs` + `_s27_r405_probe_run.sh` + their OFF / ON logs + `_s27_r405_on/` / `_s27_r405_pagescore.py` + "
           "`_s27_r405_onscore.json` / `_s27_r405_fullship_run.sh` + `_s27_r405_fullship_par.sh` + `_s27_r405_batch_N.sh` / `.log` (×36) + `_s27_r405_fullship_regen.log` (THE FULL "
           "REGENERATION) / `_s27_r405_gates.sh` + `.log` + `_s27_r405_sk_final.json` + `_s27_r405_sk_full.log` + `_s27_r405_skdelta.py` + `_s27_r405_sk_delta.log` / "
           "`_s27_r405_postship.sh` + the selftest / fast-loop / manifest / index logs / `_diff_miner_s27_r405.log` + `_diff_queue_pre_r405.md` + `_s27_r405_qdelta.py` + "
           "`_s27_r405_queue_delta.log` / `_s27_r405_entry.md` + `_s27_r405_finalise.py` + `_s27_r405_checksums.sh` + `_s27_r405_loopstate.py` | "
           + loc + " | Session 27 Round 10 (engine r405, build 260619.76) — the journal section is an activity box (English / LtL): the probe (OFF 2109 / 2109, ON 11 pages / 5 "
           "modules), the gate-scored ON pages (6 up / 3 down, +6.3), THE FULL regeneration of all 416 (0 stale, the manifest diff = the 11 pages, no residue from r397–r403), the "
           "gates and the finalise. |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r405 row")
print("finalise done")
