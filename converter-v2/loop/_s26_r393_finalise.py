#!/usr/bin/env python3
"""ROUND 393 (loop session 26 Round 7 — a glyph-only line renders nothing) — finalise: changelog (entry text in
_s26_r393_entry.md), AppVersion (260619.63 -> 260619.64), CLAUDE.md §9 / §11 / §14, gate_baseline.json, loop/README.md.
Idempotent; LF preserved. Run under WSL: python3 _s26_r393_finalise.py"""
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
ENTRY = rd(os.path.join(HERE, "_s26_r393_entry.md")).replace("\r\n", "\n")
if not ENTRY.endswith("\n\n"): ENTRY = ENTRY.rstrip("\n") + "\n\n"
if "round 393, build 260619.64" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r393 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.64"' not in s:
    old = '\tstatic AppVersion = "260619.63";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, "\t// ROUND 393 (260619.64): a glyph-only line renders nothing — a free-body line whose whole content is one punctuation glyph (a stray . or , / a text-box [ ] / a broken equation's + = – / PNR102's ✔) never ships as a <p> (body_region.drop_glyph_only_lines, ListsAndRuns.renderBlackText's line filter, env GLYPHLINE_OFF; Claude 170 on 69 pages vs the gold's 0 = dropped 1.00). 68 pages / 60 modules; scoped ship #5 since the r388 full.\n\tstatic AppVersion = \"260619.64\";")
    wr(P, s); print("Config.js: 260619.64")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "`GLYPHLINE_OFF` | 393" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 392 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 393 BASELINE (a glyph-only line renders nothing — `body_region.drop_glyph_only_lines`; 60 modules; SCOPED regeneration of the 60, the probe proving the other 356 byte-identical; scoped ship #5 since the r388 full): SCAFFOLD mean 53.560% / >=50% 1159 / >=75% 191 / >=90% 15 / RAW 37.787% @ 1956 pairs, pairs skipped 0 — hold-or-improve; 47 movers (35 up, 6 down — CEDK501_5_1 −9.1 crossing below 50 and ENGI301_4_0 −4.1 are the gate's repeat-collapse alignment: the removed stray glyph had been standing in for a gold paragraph Claude lacks). compare_structure 11723 / 172 / 626 EXACT; body_compare 42 / 4 / 173 / 218 EXACT.** Previous — ROUND 392 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `ULMERGE_OFF` | 392 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `GLYPHLINE_OFF` | 393 | **A GLYPH-ONLY LINE RENDERS NOTHING** (the autonomous loop's session 26 Round 7 — the r392 adjacent-list census's `<p>.</p>` followed up by the paired census `_s26_r393_punct.py`): a free-body line whose whole content is ONE punctuation glyph — a writer's stray `.` / `,`, a text-box bracket `[` / `]` left after an image, a broken equation's `+` `=` `–`, PNR102's `✔` ticks — shipped as `<p>.</p>`: Claude 170 on 69 pages / 64 modules, the gold the same glyph paragraph on NONE of them (dropped 170 / 170 = 1.00; the gold's own `?` / `°` / `✓` paragraphs sit where Claude ships none). Data `body_region.drop_glyph_only_lines {enabled, env, keep: [•]}` — in `ListsAndRuns.renderBlackText`'s line filter (free-body text only, `stitch` true; the placeholder / built-widget dumps untouched): a line that, with its `*` markers removed (a lone `*` is itself the glyph), is exactly one character that is not a letter / digit / `_` / kept glyph is dropped before it can become a paragraph. Measured and declined the same round: adjacent `<ol>` merge (MERGED 0.11 — no consensus) and the gold's unclosed rows (815 `row › row` nestings, predicted by nothing at 0.01–0.03). OFF = the r392 output (probe 2109 / 2109). 68 pages / 60 modules; skeleton +0.0065pp, ≥50 −1 (named); every other gate EXACT. |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.63` (round 392"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.64` (round 393 — **a glyph-only line renders nothing** (`body_region.drop_glyph_only_lines`, `ListsAndRuns.renderBlackText`'s line filter, env `GLYPHLINE_OFF`); the autonomous loop's session 26 Round 7 — Claude 170 glyph-only `<p>`s on 69 pages / 64 modules vs the gold's 0 (dropped 1.00); 68 pages / 60 modules changed; SCOPED regeneration of the 60 (scoped ship #5 since the r388 full); skeleton 53.554 → 53.560 % (+0.0065pp; 47 movers 35 up / 6 down, named), ≥50 1160 → 1159 (CEDK501_5_1 — the gate's repeat-collapse alignment, named), ≥75 191, ≥90 15, RAW 37.785 → 37.787 %; every other gate EXACT; the miner re-mined 178 CANDIDATE rows (one new #3699 `body EXTRA div.col-12.col-md-8 › div.row`, 20 pages / 18 modules at the floor — a Claude row opened inside the text column; the next candidate); adjacent `<ol>` merge and the gold's unclosed rows measured and declined). Previous: `260619.63` (round 392"
             + OLD14[len("- **Build:** `260619.63` (round 392"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r393" not in d["_meta"]:
    d["_meta"]["build"] = "260619.64"; d["_meta"]["round"] = 393; d["_meta"]["date"] = "2026-09-19"
    d["_meta"]["_note_r393"] = "Round 393: a glyph-only line renders nothing (68 pages / 60 modules; scoped ship #5 since the r388 full). Skeleton 53.554 -> 53.560 (+0.0065pp; 47 movers 35 up / 6 down, pp-sum +12.6), >=50 1160 -> 1159 (CEDK501_5_1, the gate's repeat-collapse alignment), >=75 191, >=90 15, RAW 37.785 -> 37.787; compare_structure 11723 / 172 / 626 and every other gate EXACT."
    sk = d["skeleton"]; sk["mean_scaffold_pct"] = 53.560; sk["median_scaffold_pct"] = 54.0; sk["pages_ge_50"] = 1159; sk["pages_ge_75"] = 191; sk["pages_ge_90"] = 15; sk["raw_mean_pct"] = 37.787
    sk["_note_r393"] = "Round 393: SCAFFOLD 53.5537 -> 53.5602 (+0.0065pp; 47 movers, 35 up / 6 down, pp-sum +12.6 - CEDK501_5_1 -9.1 / ENGI301_4_0 -4.1 the repeat-collapse alignment), >=50 1159 (CEDK501_5_1 down), >=75 191, >=90 15, RAW 37.787; SCOPED regeneration of the 60 affected modules. State outputs/_s26_r393_sk_final.json."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r393")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_s26_r393_finalise.py" not in s:
    A = "| `_s26_r392_adjul.py` + `.out`"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_s26_r393_adjol.py` + `.out` (adjacent `<ol>` pairs — the gold's form, declined) / `_s26_r393_rowrow.py` + `.out` + `_s26_r393_rowrow_gold.py` + `.out` + `_s26_r393_rowchain.py` + `.out` + `_s26_r393_unclosed.py` + `.out` (row-in-row = the gold's unclosed rows, declined) / `_s26_r393_punct.py` + `.out` (glyph-only paragraphs per glyph, Claude vs gold) / `_s26_r393_cedk.py` (the two alignment dips explained) / `_s26_r393_splice.py` (the PICK + the data + engine splice) / `_s26_r393_probe.cjs` + `_s26_r393_probe_run.sh` + their OFF / ON logs + `_s26_r393_on/` / `_s26_r393_pagescore.py` + `_s26_r393_onscore.json` / `_s26_r393_batches.sh` + `_s26_r393_regen_run.sh` + the batch logs / `_s26_r393_fresh.log` + `_s26_r393_manifest_diff.log` + `_s26_r393_regen_vs_probe.log` / `_s26_r393_gates.sh` + `.log` + `_s26_r393_sk_final.json` + `_s26_r393_sk_full.log` + `_s26_r393_skdelta.py` + `_s26_r393_sk_delta.log` / `_s26_r393_postship.sh` + the selftest / fast-loop / manifest / index logs / `_s26_r393_ledger.log` / `_diff_miner_s26_r393.log` + `_diff_queue_pre_r393.md` + `_s26_r393_qdelta.py` + `_s26_r393_queue_delta.log` / `_s26_r393_entry.md` + `_s26_r393_finalise.py` + `_s26_r393_checksums.sh` | "
           + loc + " | Session 26 Round 7 (engine r393, build 260619.64) — a glyph-only line renders nothing: the paired census (Claude 170 glyph-only `<p>`s on 69 pages / 64 modules, the gold 0 = dropped 1.00), the probe (OFF 2109 / 2109; ON 68 pages / 60 modules, 41 up / 6 down, +12.7), the scoped regen + gates (skeleton 53.554 → 53.560, ≥50 −1 named; every other gate EXACT), the miner re-mine (178 rows; #3699 new at the floor), the finalise; adjacent `<ol>` and the gold's unclosed rows measured and declined. |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r393 row")
print("finalise done")
