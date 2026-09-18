#!/usr/bin/env python3
"""ROUND 390 (loop session 26 Round 4 — the supervisor note's explicit closer makes the panel a span) — finalise: changelog (entry
text in _s26_r390_entry.md), AppVersion (260619.60 -> 260619.61), CLAUDE.md §9 / §11 / §14, gate_baseline.json, loop/README.md.
Idempotent; LF preserved. Run under WSL: python3 _s26_r390_finalise.py"""
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
ENTRY = rd(os.path.join(HERE, "_s26_r390_entry.md")).replace("\r\n", "\n")
if not ENTRY.endswith("\n\n"): ENTRY = ENTRY.rstrip("\n") + "\n\n"
if "round 390, build 260619.61" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r390 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.61"' not in s:
    old = '\tstatic AppVersion = "260619.60";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, "\t// ROUND 390 (260619.61): the supervisor note's explicit closer makes the panel a SPAN — a [Supervisor Button] … [End Supervisor button] pair holds everything between (callouts.by_tag.'supervisor note'.explicit_close_span, env SUPSPAN_OFF; #explicitCloseAhead accepts a tag_promote source's closer on the own-row call and stops at an [Activity] opener; stack mode span-own, emit() opens no content row meanwhile). Leaving to Learn paired 22 / 0; 21 pages / 3 modules (XDLS904 / 905 / 906); scoped ship #2 since the r388 full.\n\tstatic AppVersion = \"260619.61\";")
    wr(P, s); print("Config.js: 260619.61")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "`SUPSPAN_OFF` | 390" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 389 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 390 BASELINE (the supervisor note's explicit closer makes the panel a span — XDLS904 / 905 / 906's `[Supervisor Button] … [End Supervisor button]` pairs hold everything between; 3 modules; SCOPED regeneration of the 3, the probe proving the other 413 byte-identical; scoped ship #2 since the r388 full): SCAFFOLD mean 53.518% / >=50% 1157 / >=75% 191 / >=90% 15 / RAW 37.756% @ 1956 pairs, pairs skipped 0 — hold-or-improve; 21 movers, ALL up (XDLS905_7_0 +19.7, XDLS905_1_0 +15.7). compare_structure exact 11643 → 11700 (+57 IMPROVED) / EXTRA 172 / MISSING 625; body_compare 42 / 4 / 173 / 218 EXACT.** Previous — ROUND 389 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `FLIPBREAK_OFF` | 389 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `SUPSPAN_OFF` | 390 | **THE SUPERVISOR NOTE'S EXPLICIT CLOSER MAKES THE PANEL A SPAN** (the autonomous loop's session 26 Round 4 — the r388 paired row-break census's `row` kind = the super-content panel, Leaving to Learn 22 / 0; the panel-content census `_s26_r390_supclose.py` + the run-shape census `_s26_r390_supshape.py`). The own_row supervisor panel was always STRICT (`#calloutOpen(…, false)` — `gatherFollowing` stops at the first tag item); the XDLS904 / 905 / 906 writer opens `[Supervisor Button]` (r170 → `supervisor note`), types paragraphs + bullets whose items end in an inline `[link to X]` marker, and closes with `[End Supervisor button]` — the gold's panel holds everything to the closer (21 pairs). Data `callouts.by_tag.\"supervisor note\".explicit_close_span {enabled, env, stop_at_activity}`: the own_row branch asks `#explicitCloseAhead(…, {stopAtActivity, promotedClosers: true})` — the family set also accepts a `tag_promote` SOURCE's closer (`end supervisor button`) on THIS call only (unguarded it moved EXIP901 / SCFUN01 through the `side alert` / `interactive` promotions — the probe's OFF leg caught it), and an `[Activity]` opener ends the scan; on a hit the panel opens in SPAN mode (stack mode `span-own`): the loop renders the items between inside the panel's column, `emit()` opens no content row while `ownSpanClose` is set and pushes the close directly, `autoClose` treats `span-own` like a writer's span, the closer pops it. Every family without an explicit closer is untouched by construction (Mathematics 0 / 9, BLL 0 / 4 agree with the strict panel); XDLS502 / XDLS901's `[end supervisor note]` is typed in BLACK (no tag). OFF = the r389 output (probe 2109 / 2109). 21 pages / 3 modules; skeleton +0.047pp (21 up / 0 down); compare_structure exact +57; every other gate EXACT. |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.60` (round 389"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.61` (round 390 — **the supervisor note's explicit closer makes the panel a span: a `[Supervisor Button] … [End Supervisor button]` pair holds everything between** (`callouts.by_tag.\"supervisor note\".explicit_close_span`, env `SUPSPAN_OFF`; `#explicitCloseAhead` accepts a `tag_promote` source's closer on the own-row call and stops at an `[Activity]` opener; stack mode `span-own`, `emit()` opens no content row meanwhile); the autonomous loop's session 26 Round 4 — the r388 paired row-break census's `row` kind (Leaving to Learn 22 / 0) triangulated to the writer's closer (XDLS904 / 905 / 906, 21 pairs; every other family agrees with the strict panel); 21 pages / 3 modules changed; SCOPED regeneration of the 3 (the probe proving the other 413 byte-identical; scoped ship #2 since the r388 full); skeleton 53.470 → 53.518 % (+0.047pp; 21 movers, ALL up), ≥50 1157 / ≥75 191 / ≥90 15 EXACT, RAW 37.725 → 37.756 %; compare_structure exact 11643 → 11700 (+57 IMPROVED); every other gate EXACT; the miner re-mined 178 CANDIDATE rows (177 → 178: the new row #3735 = the panel text column's class, gold `col-12 col-md-12` in Leaving to Learn 0.76 — the next candidate)). Previous: `260619.60` (round 389"
             + OLD14[len("- **Build:** `260619.60` (round 389"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r390" not in d["_meta"]:
    d["_meta"]["build"] = "260619.61"; d["_meta"]["round"] = 390; d["_meta"]["date"] = "2026-09-19"
    d["_meta"]["_note_r390"] = "Round 390: the supervisor note's explicit closer makes the panel a span (21 pages / 3 modules; scoped ship #2 since the r388 full). Skeleton 53.470 -> 53.518 (+0.047pp; 21 movers all up, pp-sum +92.5), >=50 1157, >=75 191, >=90 15 EXACT, RAW 37.725 -> 37.756; compare_structure exact 11643 -> 11700 (+57 IMPROVED); every other gate EXACT."
    sk = d["skeleton"]; sk["mean_scaffold_pct"] = 53.518; sk["median_scaffold_pct"] = 54.0; sk["pages_ge_50"] = 1157; sk["pages_ge_75"] = 191; sk["pages_ge_90"] = 15; sk["raw_mean_pct"] = 37.756
    sk["_note_r390"] = "Round 390: SCAFFOLD 53.4702 -> 53.5175 (+0.047pp; 21 movers, ALL up, pp-sum +92.5 - XDLS905_7_0 +19.7, XDLS905_1_0 +15.7, XDLS906_2_0 +5.7, XDLS904_1_0 +4.8), >=50 1157, >=75 191, >=90 15, RAW 37.756; SCOPED regeneration of XDLS904 / 905 / 906, the probe proving the other 413 byte-identical. State outputs/_s26_r390_sk_final.json."
    cs = d.get("compare_structure") or d.get("structure") or {}
    for key in ("exact", "exact_chain", "exact_wrapper_chain"):
        if key in cs: cs[key] = 11700
    d["_meta"]["_note_r390_cs"] = "compare_structure exact wrapper chain 11643 -> 11700 (+57) at r390; EXTRA 172 / MISSING 625 unchanged."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r390")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_s26_r390_finalise.py" not in s:
    A = "| `_s26_r389_divpair_gen.py`"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_s26_r390_supclose.py` + `.out` (the WT closer census + the paired panel-content census: after a Claude non-activity supervisor panel, is the next prose inside the gold's panel?) / `_s26_r390_supshape.py` + `.out` (the gold panel's run shape per group) / `_s26_r390_parse.cjs` (the live parse of the closer forms) / `_s26_r390_pick.py` / `_s26_r390_splice.py` + `_s26_r390_splice2.py` (the engine + data splice; splice 2 = the promoted-closer family gated to the own-row call) / `_s26_r390_probe.cjs` + `_s26_r390_probe_run.sh` + their OFF / ON logs + `_s26_r390_on/` / `_s26_r390_pagescore.py` + `_s26_r390_onscore.json` / `_s26_r390_batches.sh` + `_s26_r390_regen_run.sh` + the batch log / `_s26_r390_fresh.log` + `_s26_r390_manifest_diff.log` + `_s26_r390_regen_vs_probe.log` / `_s26_r390_gates.sh` + `.log` + `_s26_r390_sk_final.json` + `_s26_r390_sk_full.log` + `_s26_r390_sk_delta.log` / `_s26_r390_postship.sh` + `_s26_r390_selftests.log` + `_s26_r390_fastloop_snapshot.log` + `_s26_r390_manifest_snapshot.log` + `_s26_r390_index.log` / `_s26_r390_ledger.log` / `_diff_miner_s26_r390.log` + `_diff_queue_pre_r390.md` + `_s26_r390_queue_delta.log` / `_s26_r391_panelcol.py` + `.out` (the panel text-column class census — the new miner row #3735 decomposed) / `_s26_r390_entry.md` + `_s26_r390_finalise.py` + `_s26_r390_checksums.sh` | "
           + loc + " | Session 26 Round 4 (engine r390, build 260619.61) — the supervisor note's explicit closer makes the panel a span: the paired panel-content census (LtL 22 / 0; every other family agrees with the strict panel), the writer's closer parsed live, the probe (the first OFF leg caught an unguarded promoted-closer leak on EXIP901 / SCFUN01 → re-gated; OFF 2109 / 2109; ON 21 pages / 3 modules, 21 up / 0 down, pp-sum +92.5), the scoped regen + gates (skeleton 53.470 → 53.518; compare_structure exact +57; every other gate EXACT), the miner re-mine (178 rows, the new #3735 decomposed), the finalise. |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r390 row")
print("finalise done")
