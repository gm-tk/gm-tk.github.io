#!/usr/bin/env python3
"""r420 finalise — LOOP_STATE.md: the Round 2 PICK section moves to the archive (+ the what-shipped record), the Position updates,
the Round-log line is appended. Run under WSL."""
import os, io
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
STATE, ARCH = R + "LOOP_STATE.md", R + "LOOP_STATE_ARCHIVE.md"
lines = io.open(STATE, encoding="utf-8").read().split("\n")
def idx(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix): return i
    raise SystemExit("not found: " + prefix)
a = idx("## Session 30 — Round 2 PICK (engine r420)"); b = idx("## Round log")
pick = lines[a:b]
shipped = ("- **What shipped (r420, build 260619.91, 21 Sept ≈17:45):** `interactive_builders.selfCheck.letter_grid_bingo {enabled, env BINGO_OFF, max_cell_chars 2, "
           "min_cells 4, grid_by_cells, grid_default 4, lead / open / container_open / cell / cell_correct_attr / container_close / buttons / close, cell_class_by_prefix "
           "{BLL: sassoonI-text}, correct_from [red, lead_quote], lead_quote_pattern, asset_note_pattern, note_prefix}` + `InteractiveBuilder.#letterGridBingo` before the "
           "r69 question-list form; the NEW protected gate `_verify_bingo.cjs` (+ `_selftest_core.cjs` inject spec, the `run_all_gates.sh` line over the 9 BLL modules, "
           "`gate_baseline.json.bingo`, the gates checksum manifest 86 → 87). Verifier: 52 grids / 624 cells on 7 modules — exact 34 / copy-edit 11 / dev-edit 7 / defect 0; "
           "selftest GREEN. Probe OFF = disk 2555 / 2555; ON 7 pages / 7 modules (BLL113 / BLL154 decline by design); scored RAW +4.7pp-sum (every page up), scaffold "
           "−1.1pp-sum (6 down 0.1–0.6, BLL170 +0.4 — the built `p + WIDGET` pairs inside Claude's inner `row > col-12` where the gold's BLL bingo boxes are bare: the "
           "r289 widget-marker class, NAMED and accepted via `_fastloop_diff.py --commit --accept-named 'skeleton SCAFFOLD mean'`; the bare box measured corpus-wide "
           "`_s30_r2_boxinner.py` 0.07 / BLL Inquiry 0.21 — not a class). SCOPED regeneration of the 7 + 12 spot-checks (0 stale; 12 / 12; containment 7 ⊆ 7; the ledger "
           "scoped #4 since the r416 FULL — 4 of headroom). `run_all_gates.sh`: skeleton 54.2072 → 54.2067 % (−0.0005pp, named), ≥50 1441 / ≥75 238 / ≥90 20 EXACT, RAW "
           "38.227 → 38.229; cs 14170 / 186 / 683 / 23, body 54 / 5 / 190 / 247, clean 2504 / 2548, leak 73 / 44, tags 9557 — all EXACT; every verifier ✓; 17 selftests "
           "GREEN (49 / 0); feature index GREEN; miner 182 → 182; KB status D10-3 row updated (selfCheck kickoff shape 1); checksums refreshed. D10-3's moved test: "
           "selfCheck still-a-box 215 → 163. Next shape: the Question | Model-answer selfCheck table (58 sites).")
lines[a:b] = ["## Session 30 — Round 2 (engine r420) — THE LETTER-GRID BINGO: the BLL family's `[Self check]` + a table of letters builds the KB's 03E bingo (D10-3, the selfCheck kickoff's shape 1) — SHIPPED; the PICK (with the three declined measurements: pinyin below floor, `div.alert.solid` KB-correct, the widened wrapper per built layout) + what-shipped record is in LOOP_STATE_ARCHIVE.md 'Session 30 — Round 2 PICK (engine r420) + what shipped'; the one-line summary is the s30-r2 Round-log line below.", ""]
p = idx("- LAST SHIPPED: **r419**")
old = lines[p]
head = "- LAST SHIPPED: **r419** (build 260619.90, 21 Sept ≈16:50, session 30 Round 1 — "
assert old.startswith(head)
rest = old[len(head):]
r419_short = ("**r419** (build 260619.90, 21 Sept ≈16:50, session 30 Round 1 — the language-font wrap: every CJK run takes `span.ch-text` / `span.jp-text`, KB constraint 92, "
              "`LANGFONT_OFF`, 13 up / 7 down, +0.0212pp, ≥50 +2)")
tail_ix = rest.find("; before it **r418**")
assert tail_ix > 0
tail = rest[tail_ix + len("; before it "):]
lines[p] = ("- LAST SHIPPED: **r420** (build 260619.91, 21 Sept ≈17:45, session 30 Round 2 — THE LETTER-GRID BINGO: the BLL family's `[Self check]` + a table of "
            "letters builds the KB's 03E bingo (D10-3's selfCheck kickoff, shape 1 — 55 tables / 9 modules; `letter_grid_bingo`, env `BINGO_OFF`; the NEW protected gate "
            "`_verify_bingo.cjs`: 52 grids / 7 modules, exact 34 / copy-edit 11 / dev-edit 7 / defect 0); probe OFF = disk 2555 / 2555, ON 7 pages / 7 modules; SCOPED "
            "regeneration of the 7 (scoped ship #4 since the r416 FULL); **skeleton 54.2072 → 54.2067 % (−0.0005pp — the r289 widget-marker class, NAMED), ≥50 1441, ≥75 "
            "238, ≥90 20, RAW 38.229 % @ 2349 pairs**; cs 14170 / 186 / 683 / 23, body 54 / 5 / 190 / 247, clean 2504 / 2548, leak 73 / 44 — all EXACT; every verifier "
            "EXACT; 17 selftests GREEN; the miner 182 → 182; selfCheck still-a-box 215 → 163); before it " + r419_short + ", " + tail)
lines[p] = lines[p].replace("**Corpus = r419** (2555 pages / 494 dirs / 2349 pairs; `gate_baseline.json` at r419; `outputs/_s30_r419_sk_final.json` the skeleton state; ceiling 90.9 % → 54.207 = **59.6 % of achievable**)",
                            "**Corpus = r420** (2555 pages / 494 dirs / 2349 pairs; `gate_baseline.json` at r420; `outputs/_s30_r420_sk_final.json` the skeleton state; ceiling 90.9 % → 54.207 = **59.6 % of achievable**)")
assert "Corpus = r420" in lines[p]
q = idx("- Plateau window (§4): **0 of 3**")
lines[q] = "- Plateau window (§4): **0 of 3** — r420 a build round (D10-3's moved test: selfCheck still-a-box 215 → 163; scaffold −0.0005pp named), r419 +0.0212pp (≥50 +2), r418 +0.0630pp (≥50 +1). Read every delta on the post-intake 2,349-pair population (§1e)."
r = idx("- Standing facts: AppVersion 260619.90")
lines[r] = lines[r].replace("AppVersion 260619.90 (r419, session 30 Round 1, 21 Sept); before it 260619.89 (r418)", "AppVersion 260619.91 (r420, session 30 Round 2, 21 Sept); before it 260619.90 (r419) / 260619.89 (r418)")
assert "260619.91" in lines[r]
t = idx("- s30-r1 (engine r419")
lines.insert(t + 1, "- s30-r2 (engine r420, build 260619.91, 21 Sept ≈16:55 → 17:45) · THE LETTER-GRID BINGO — the BLL family's `[Self check] Click on the lower case letter ‘s’.` + a table of single letters (the correct cells in red) builds the KB's 03E bingo (`div.bingo.col-12 > div.bingoContainer[grid] > div.number[value=correct] > p.sassoonI-text` + the Reset / Check row; Chris's D10-3 build lane — the selfCheck type's largest un-built shape, 55 tables / ≈ 28 bundles / 9 modules, found by reading the r286 decline records by CONTENT (`_s30_r2_shapes.py`, `_s30_r2_bingo.py`, `_s30_r2_scdump.cjs`) where the s27-r4 signature-string census had split the family across table dimensions; `InteractiveBuilder.#letterGridBingo`, `letter_grid_bingo`, env `BINGO_OFF`; the writer's audio request → the Writers Note; NEW protected gate `_verify_bingo.cjs`) · PICK pass first: pinyin BELOW FLOOR (7 Claude pages), `div.alert.solid` DECLINED KB-correct (`_s30_r2_alertsolid.py`: the gold keeps solid 22 / 295), the widened wrapper per built layout DECLINED (`_s30_r2_widecol.py`: ≤ 0.36 in every group; D10-3's item closed) · SHIPPED · verifier 52 grids / 624 cells / 7 modules, exact 34 / copy-edit 11 / dev-edit 7 / defect 0; probe OFF = disk 2555 / 2555, ON 7 pages · SCOPED regen of the 7 + 12 spot-checks (0 stale; 12 / 12; containment 7 ⊆ 7; scoped #4 since the r416 FULL) · RAW +4.7pp-sum; scaffold 54.2072 → 54.2067 (−0.0005pp — the r289 widget-marker class, NAMED via `--accept-named`; the bare BLL bingo box 0.07 corpus-wide, not a class), buckets EXACT; all else EXACT; every verifier ✓; 17 selftests GREEN; miner 182 → 182 · selfCheck still-a-box 215 → 163 · plateau 0 of 3 · build 260619.91")
io.open(STATE, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
with io.open(ARCH, "a", encoding="utf-8", newline="\n") as f:
    f.write("\n## Session 30 — Round 2 PICK (engine r420) + what shipped — THE LETTER-GRID BINGO (D10-3's selfCheck kickoff, shape 1) (21 Sept ≈16:55 → 17:45 NZST)\n\n" + "\n".join(pick).rstrip("\n") + "\n" + shipped + "\n")
print("LOOP_STATE.md", os.path.getsize(STATE), "bytes; archive", os.path.getsize(ARCH))
