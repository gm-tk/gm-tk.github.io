#!/usr/bin/env python3
"""SESSION 28 / TASK 1 (round 408, build 260619.79 — the mined registries rebuilt over the 552-module gold corpus) — finalise:
changelog (entry text in _s28_t1_entry.md), CLAUDE.md §9 / §13 / §14, gate_baseline.json, loop/README.md, CONVERTER_V2_GUIDE.md.
(Config.js AppVersion 260619.79 was edited directly with the Edit tool.) Idempotent; LF preserved.
Run under WSL: python3 _s28_t1_finalise.py"""
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


# ---- changelog -------------------------------------------------------------------------------------
CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)" + chr(10) + chr(10)
ENTRY = rd(os.path.join(HERE, "_s28_t1_entry.md")).replace("\r\n", "\n")
if not ENTRY.endswith("\n\n"): ENTRY = ENTRY.rstrip("\n") + "\n\n"
if "round 408, build 260619.79" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r408 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
assert '"260619.79"' in s, "Config.js not bumped"

# ---- CLAUDE.md §9 / §13 / §14 -----------------------------------------------------------------------
P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "ROUND 408 BASELINE" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 407 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 408 BASELINE (the mined registries rebuilt over the 552-module gold corpus — the "
            "September intake's 98 modules join Module_Structure_Index / the Style-Anchor bases / the Menu, Convention, lexicon, feature and consensus registries in ONE pass; "
            "SCOPED regeneration of the 103 modules the rebuild touches, the probe proving the other 391 byte-identical; scoped ship #1 since the 19 Sept full): SCAFFOLD mean "
            "53.680% / >=50% 1398 / >=75% 236 / >=90% 20 / RAW 37.884% @ 2349 pairs (the WHOLE post-intake population), pairs skipped 0 — hold-or-improve; 275 movers (197 up, "
            "76 down — GEO1006_3_0 −11.3 / GEO1004_1_0 −9.4 the NCEA phase's h4 → h3, ENGS404_6_1 −8.2, PWY1001_2_3_0 −7.0, CHI1003 ×3 ≈ −5 the mined second h1 — named); the "
            "1813 unaffected pairs EXACT. compare_structure exact 14091 (pool 15668 → 16414) / EXTRA 186 / MISSING 690 / row-wrap 23 (the +2 / +5 inside five newly single-file "
            "WJFUN / JPFUN modules, named); body_compare over-capture 54 / runaway 6 / EMPTY 190 / ANY 248; defect clean 2504 / 2548 = 98.27% (58 clean WJFUN extras left the "
            "population; defect pages 44 / leak 73 EXACT); WJFUN 10.4 → 37.6%.** Previous — ROUND 407 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD13 = ("  **ROUND 253 RECIPE (the 454-dir corpus outgrew the old 12-way slice): run\n"
             "  `outputs/_r253_shard_driver.sh` repeatedly until it prints ALL_SHARDS_PRESENT (48-way shards,\n"
             "  resumable — finished shards are skipped), then `--merge` → `--selftest`.** `--query \"menu|@h5\"`\n")
    assert s.count(OLD13) == 1, "§13 anchor"
    NEW13 = ("  **ROUND 253 RECIPE (the 454-dir corpus outgrew the old 12-way slice): run\n"
             "  `outputs/_r253_shard_driver.sh` repeatedly until it prints ALL_SHARDS_PRESENT (48-way shards,\n"
             "  resumable — finished shards are skipped), then `--merge` → `--selftest`.** **ROUND 408 RECIPE (WSL, no\n"
             "  45 s wall — the whole intake rebuild, `outputs/_s28_t1_*`): park the old shards, `--shard K 8` ×8 in\n"
             "  parallel (2.5 min for 552 dirs) → `--merge` → `--selftest`; the subject map = the `All_Template_Reports`\n"
             "  folders PLUS `data/Subject_Prefix_Map.json` for the prefixes the reports never filed (gaps only). THEN, IN\n"
             "  THE SAME ROUND (the r263 stale-registry trap): mine every new family's Style-Anchor row from its gold with\n"
             "  `ReferenceMiner.Distil` (`_s28_t1_mine_sar.cjs` → `_s28_t1_update_sar.cjs`: complete base_rules per prefix,\n"
             "  a level per first digit; a base whose evidence floor flips OFF must have its Stage-1 row checked against\n"
             "  the gold — ANZHFUN / ENO / XOTP* carried junk), `derive_menu_type.cjs`, `build_convention_registry.py`\n"
             "  (AFTER the Style-Anchor members — it groups by them), `build_menu_heading_lexicon.py`, the feature index\n"
             "  (`--shard K 16` ×16 → `--merge` → `--selftest`), the legacy consensus (`anchor_compare.py --build-consensus`\n"
             "  ×8 → `--merge-consensus`, built WITH `GRANULAR_SIG_OFF=1`); re-pin the cascade / parity selftest fixtures\n"
             "  the population moved; then the in-memory probe over every Claude-dir module (OFF = the pre snapshot swapped\n"
             "  in via `--pre <dir>`) sizes the regeneration.** `--query \"menu|@h5\"`\n")
    s = s.replace(OLD13, NEW13, 1)
    OLD14 = "- **Build:** `260619.78` (round 407"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.79` (round 408 — **the mined registries rebuilt over the 552-module gold corpus** (session 28, pre-loop Task 1 — a DATA round: "
             "`Module_Structure_Index.module_meta` 454 → 552 with all 98 September-intake codes (the Reference-module picker now lists 552; blank subjects 12 → 0; "
             "template types exactly Standard 380 / Fundamentals 81 / Inquiry 68 / Bilingual 23), the Granular registry (710 element-keys / 1264 reliable nodes), "
             "**24 NEW Style_Anchor_Registry bases mined per family** (BLLR · CBI CHI COM DAN DTC GEO GER JPN MUS MXS PWY PWYWHA SAM SPA · CHWHA FRNO GENO GEWHA JPFUN · "
             "SCBI SCES · PMT · WJFUN — WJFUN + JPFUN `page_model single-file`, the CHFUN r265 precedent) + new members on 7 bases + the r263 floor-flip rows corrected "
             "(ANZHFUN / ENO / XOTPB / XOTPG / XOTPO); `Menu_Scaffold_Registry` 120 → 174 groups / 370 → 525 series rows; `Html_Convention_Registry` 43 → 52 groups "
             "(14 re-measured); the heading lexicon 61 → 66; the feature index 552 / 143 GREEN; the legacy consensus 604 / 147; the NEW `data/Subject_Prefix_Map.json` "
             "(30 prefix labels, PROPOSED — Chris approves); **FRFUN held back, measured** (the multi-file level-page fundamentals dialect has no renderer — the faithful "
             "row scored 26 / 28 pages down); SCOPED regeneration of the 103 modules the probe named (OFF = the pre snapshot 2613 / 2613; ON 457 pages / 103 modules; "
             "scoped ship #1 since the 19 Sept FULL); skeleton 53.134 → 53.680 % (+0.5455pp; 275 movers 197 up / 76 down, 0 outside the set, the 1813 unaffected pairs "
             "EXACT), ≥50 1378 → 1398, ≥75 228 → 236, ≥90 19 → 20, RAW 37.487 → 37.884 %; WJFUN 10.4 → 37.6 %; compare_structure exact 13410 → 14091 (pool +746) / 186 / "
             "690; body_compare 54 / 6 / 190 / 248 (EMPTY −2, ANY −2); defect pages 44 / leak 73 EXACT (clean 2504 / 2548 — 58 clean WJFUN extras left); every verifier "
             "EXACT; miner 187 → 183 — the five WJFUN chrome rows collapsed as one, `nav:phases` MISSING (WJFUN's in-page phases) is the next class). Previous: "
             "`260619.78` (round 407" + OLD14[len("- **Build:** `260619.78` (round 407"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §13 / §14")

# ---- gate_baseline.json ----------------------------------------------------------------------------
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r408" not in d["_meta"]:
    d["_meta"]["build"] = "260619.79"; d["_meta"]["round"] = 408; d["_meta"]["date"] = "2026-09-20"
    d["_meta"]["_note_r408"] = ("Round 408 (session 28 Task 1): the mined registries rebuilt over the 552-module gold corpus (Module_Structure_Index / Granular / "
                               "24 new Style-Anchor bases + floor-flip corrections / Menu / Convention / lexicon / feature index / legacy consensus; "
                               "data/Subject_Prefix_Map.json PROPOSED). SCOPED regeneration of the 103 modules the probe named (OFF = pre snapshot 2613/2613; "
                               "scoped ship #1 since the 19 Sept full). Skeleton 53.134 -> 53.680 (+0.5455pp; 275 movers 197 up / 76 down, 0 outside the set, "
                               "the 1813 unaffected pairs EXACT), >=50 1378 -> 1398, >=75 228 -> 236, >=90 19 -> 20, RAW 37.487 -> 37.884; compare_structure "
                               "exact 13410 -> 14091 (the text-matched pool 15668 -> 16414) / EXTRA 184 -> 186 / MISSING 685 -> 690 (inside five newly "
                               "single-file WJFUN / JPFUN modules) / row-wrap 23; body_compare over-capture 54 (the 19 Sept fast-loop snapshot's own value — "
                               "the re-base had carried r407's 42; corrected here), runaway 6, EMPTY 192 -> 190, ANY 250 -> 248; defect clean 2504/2548 = 98.27 "
                               "(58 clean WJFUN / JPFUN extra pages left the population; defect pages 44 / leak 73 EXACT); every verifier EXACT.")
    sk = d["skeleton"]; sk["mean_scaffold_pct"] = 53.68; sk["median_scaffold_pct"] = 54.4; sk["raw_mean_pct"] = 37.88
    sk["pages_ge_50"] = 1398; sk["pages_ge_75"] = 236; sk["pages_ge_90"] = 20; sk["pairs"] = 2349; sk["pairs_skipped"] = 0
    sk["_note_r408"] = ("Round 408: SCAFFOLD 53.1341 -> 53.6797 (+0.5455pp; 275 movers, 197 up / 76 down, pp-sum +725.6 — GEO1006_3_0 -11.3, GEO1004_1_0 -9.4, "
                        "ENGS404_6_1 -8.2, PWY1001_2_3_0 -7.0, CHI1003_8_0 -5.0), >=50 1398, >=75 236, >=90 20; RAW 37.487 -> 37.884; 2349 pairs / 0 skipped. "
                        "State outputs/_s28_t1_sk_final.json.")
    cs = d["compare_structure"]
    cs["exact_chain"] = 14091; cs["claude_extra_container"] = 186; cs["claude_missing_container"] = 690; cs["row_wrap_missing"] = 23
    cs["_note_r408"] = "Round 408: exact 13410 -> 14091 (pool 15668 -> 16414), EXTRA 184 -> 186 (WJFUN206), MISSING 685 -> 690 (JPFUN01 / WJFUN108 / WJFUN109 +1, WJFUN304 +2), row-wrap 23; every unaffected module EXACT."
    bc = d["body_compare"]
    bc["any_breakdown"] = 248; bc["over_capture"] = 54; bc["runaway"] = 6; bc["empty_container"] = 190
    bc["_note_r408"] = "Round 408: over-capture 54 (the 19 Sept fast-loop snapshot value; gate_baseline had carried r407's 42), runaway 6, EMPTY 192 -> 190, ANY 250 -> 248 (WJFUN304); every unaffected module EXACT."
    df = d["structural_defect"]
    df["clean_pages"] = 2504; df["total_pages"] = 2548; df["clean_pct"] = 98.27; df["literal_tag_leak_occ"] = 73; df["leak_pages"] = 44
    df["_note_r408"] = "Round 408: 2606 -> 2548 pages (58 clean WJFUN / JPFUN extra pages left the population when the families went single-file); defect pages 44 / leak 73 EXACT; 0 new defects."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r408")

# ---- loop/README.md row ------------------------------------------------------------------------------
P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_s28_t1_finalise.py" not in s:
    A = "| `_s27_r12_emptyowner.py` + `.out` + `_s27_r12_pick.md`"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_s28_t1_census.cjs` + `.out` / `_s28_t1_shards.sh` + `.log` / `_s28_t1_mine_sar.cjs` + `.out` + `.json` / `_s28_t1_update_sar.cjs` + `.out` / "
           "`_s28_t1_patch_builder.py` / `_s28_t1_menudiff.cjs` + `.out` / `_s28_t1_convdiff.cjs` + `.out` / `_s28_t1_consensus.sh` + `.log` / `_s28_t1_repin.py` / "
           "`_s28_t1_probe.cjs` + `_s28_t1_probe_run.sh` + the OFF / ON logs / `_s28_t1_pagescore.py` + `_s28_t1_onscore.json` / `_s28_t1_affected.txt` + "
           "`_s28_t1_changed_pages.txt` + `_s28_t1_regen.sh` + the batch logs / `_s28_t1_gates.sh` + `.log` + `_s28_t1_regen_vs_probe.log` + `_s28_t1_sk_final.json` + "
           "`_s28_t1_sk_full.log` + `_s28_t1_skdelta.py` + `.out` + `_s28_t1_split.cjs` + `.out` / `_s28_t1_postship.sh` + the selftest / fast-loop / manifest / index / "
           "ledger logs / `_diff_miner_s28_t1.log` + `_diff_queue_pre_s28t1.md` + `_s28_t1_qdelta.py` + `_s28_t1_queue_delta.log` / `_s28_t1_entry.md` + "
           "`_s28_t1_finalise.py` + `_s28_t1_checksums.sh` | "
           + loc + " | Session 28 pre-loop Task 1 (round 408, build 260619.79) — the mined registries rebuilt over the 552-module gold corpus: the census of the 98 "
           "intake modules against the registries, the 8 + 16 shard builds, the per-family Style-Anchor mining (162 gold modules, 38 prefixes), the Menu / Convention "
           "diffs, the legacy consensus, the cascade re-pins, the probe (OFF 2613 / 2613, ON 457 pages / 103 modules), the gate-scored ON pages (199 up / 77 down, "
           "+732.9), the scoped regeneration of the 103 (0 stale, probe == disk 590 / 590), the gates, the population split and the finalise. |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: s28 t1 row")
print("finalise done")
