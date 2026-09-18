#!/usr/bin/env python3
"""ROUND 395 (loop session 26 Round 9 — the flip-card column width follows the card count) — finalise: changelog (entry text
in _s26_r395_entry.md), AppVersion (260619.65 -> 260619.66), CLAUDE.md §9 / §11 / §14, gate_baseline.json, loop/README.md.
Idempotent; LF preserved. Run under WSL: python3 _s26_r395_finalise.py"""
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
ENTRY = rd(os.path.join(HERE, "_s26_r395_entry.md")).replace("\r\n", "\n")
if not ENTRY.endswith("\n\n"): ENTRY = ENTRY.rstrip("\n") + "\n\n"
if "round 395, build 260619.66" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r395 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.66"' not in s:
    old = '\tstatic AppVersion = "260619.65";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, "\t// ROUND 395 (260619.66): the flip-card column width follows the card count — a 2-card or 4-card group's cards are col-md-6 col-12 paddingLR (interactive.flipCard.card_col_by_count + exclude_subjects_by_count, InteractiveBuilder.#flipCardsByCount, env FLIPCOL_OFF; the gold 0.86 / 0.76; English's 4-card tie, ConnectED / NCEA1's col-md-3 lead, NCEA1 / TEDC's 2-card forms excluded). 39 pages / 37 modules; scoped ship #7 since the r388 full — the next ship is the FULL backstop.\n\tstatic AppVersion = \"260619.66\";")
    wr(P, s); print("Config.js: 260619.66")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "`FLIPCOL_OFF` | 395" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 394 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 395 BASELINE (the flip-card column width follows the card count — `interactive.flipCard.card_col_by_count`; 37 modules; SCOPED regeneration of the 37, the probe proving the other 379 byte-identical; scoped ship #7 since the r388 full — the next ship is the FULL backstop): SCAFFOLD mean 53.684% / >=50% 1163 / >=75% 195 / >=90% 18 / RAW 37.784% @ 1956 pairs, pairs skipped 0 — hold-or-improve; 16 movers (15 up, 1 down — TEFUN08_0_0 −0.2). compare_structure 11723 / 172 / 626 EXACT; body_compare 42 / 4 / 173 / 218 EXACT.** Previous — ROUND 394 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD11 = "| `CDROW_OFF` | 394 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `FLIPCOL_OFF` | 395 | **THE FLIP-CARD COLUMN WIDTH FOLLOWS THE CARD COUNT** (the autonomous loop's session 26 Round 9 — the r394 column census followed through by `_s26_r395_flipcols.py`, every flipCardsContainer's card count + column class, gold vs Claude, per subject). Gold: a 4-card group's cards `col-md-6 col-12 paddingLR` 0.76 (48 + 9 col-sm-6 of 75; col-md-3 16, col-md-4 2), a 2-card group's 0.86 (39 + 11 col-6 of 58; col-md-4 8); 3 cards and 5+ cards col-md-4 (the template default, Claude already matching). Claude shipped every card col-md-4 (4-card 57 on 49 pages / 43 modules, 2-card 19 on 18 / 14). Per subject the 4-card form is a TIE in English (10 / 9) and col-md-3-led in ConnectED (4 / 3) and NCEA1 (2 / 1); the 2-card form is col-md-4 in NCEA1 and a tie in the subject-less TEDC modules — excluded. A 1-card group is col-md-12 in the gold (0.63 on 16 pages) but on 8 Claude pages — under the floor, recorded. Data `interactive.flipCard.card_col_by_count {enabled, env, default, by_count, exclude_subjects_by_count}` — `#flipCardsByCount(tpl, cards, run)` swaps the default column class for the by-count class in each finished card at the four `tpl.card` join sites; the image-front `card_image_front` family untouched. OFF = the r394 output (probe 2109 / 2109). 39 pages / 37 modules; skeleton +0.010pp, ≥75 +1; every other gate EXACT. |\n"
             + OLD11)
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.65` (round 394"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.66` (round 395 — **the flip-card column width follows the card count** (`interactive.flipCard.card_col_by_count`, `InteractiveBuilder.#flipCardsByCount`, env `FLIPCOL_OFF`); the autonomous loop's session 26 Round 9 — a 2-card / 4-card group's cards are `col-md-6` (the gold 0.86 / 0.76; English's 4-card tie, ConnectED / NCEA1's col-md-3 lead, NCEA1 / TEDC's 2-card forms excluded); 39 pages / 37 modules changed; SCOPED regeneration of the 37 (scoped ship #7 since the r388 full — the next ship is the FULL backstop); skeleton 53.674 → 53.684 % (+0.010pp; 16 movers 15 up / 1 down), ≥75 194 → 195, ≥50 1163, ≥90 18, RAW 37.779 → 37.784 %; every other gate EXACT, every verifier RESULT identical; the miner re-mined 173 CANDIDATE rows (#3649 gone, nothing new)). Previous: `260619.65` (round 394"
             + OLD14[len("- **Build:** `260619.65` (round 394"):])
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r395" not in d["_meta"]:
    d["_meta"]["build"] = "260619.66"; d["_meta"]["round"] = 395; d["_meta"]["date"] = "2026-09-19"
    d["_meta"]["_note_r395"] = "Round 395: the flip-card column width follows the card count (39 pages / 37 modules; scoped ship #7 since the r388 full — the next ship is the FULL backstop). Skeleton 53.674 -> 53.684 (+0.010pp; 16 movers 15 up / 1 down, pp-sum +19.4), >=50 1163, >=75 194 -> 195, >=90 18, RAW 37.779 -> 37.784; compare_structure 11723 / 172 / 626 and every other gate EXACT; every verifier RESULT identical."
    sk = d["skeleton"]; sk["mean_scaffold_pct"] = 53.684; sk["median_scaffold_pct"] = 54.3; sk["pages_ge_50"] = 1163; sk["pages_ge_75"] = 195; sk["pages_ge_90"] = 18; sk["raw_mean_pct"] = 37.784
    sk["_note_r395"] = "Round 395: SCAFFOLD 53.6736 -> 53.6835 (+0.010pp; 16 movers, 15 up / 1 down, pp-sum +19.4 - TEFUN08_0_0 -0.2), >=50 1163, >=75 195 (OSOH201_2_0 up), >=90 18, median 54.3, RAW 37.784; SCOPED regeneration of the 37 affected modules. State outputs/_s26_r395_sk_final.json."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: r395")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_s26_r395_finalise.py" not in s:
    A = "| `_s26_r394_colrow.py` + `.out`"
    assert s.count(A) == 1, "README anchor"
    line = [l for l in s.split("\n") if l.startswith(A)][0]
    cells = line.split(" | ")
    loc = cells[1] if len(cells) >= 3 else "`CONVERTER_V2/outputs/`"
    ROW = ("| `_s26_r395_flipcols.py` + `.out` (every flipCardsContainer's card count + column class, gold vs Claude, per subject in full) / `_s26_r395_splice.py` + `_s26_r395_splice2.py` (the PICK + the data + engine splice; the per-subject exclusions) / `_s26_r395_probe.cjs` + `_s26_r395_probe_run.sh` + their OFF / ON logs + `_s26_r395_on/` / `_s26_r395_pagescore.py` + `_s26_r395_onscore.json` / `_s26_r395_batches.sh` + `_s26_r395_regen_run.sh` + the batch logs / `_s26_r395_fresh.log` + `_s26_r395_manifest_diff.log` + `_s26_r395_regen_vs_probe.log` / `_s26_r395_gates.sh` + `.log` + `_s26_r395_sk_final.json` + `_s26_r395_sk_full.log` + `_s26_r395_skdelta.py` + `_s26_r395_sk_delta.log` / `_s26_r395_postship.sh` + the selftest / fast-loop / manifest / index logs / `_s26_r395_ledger.log` / `_diff_miner_s26_r395.log` + `_diff_queue_pre_r395.md` + `_s26_r395_qdelta.py` + `_s26_r395_queue_delta.log` / `_s26_r395_entry.md` + `_s26_r395_finalise.py` + `_s26_r395_checksums.sh` | "
           + loc + " | Session 26 Round 9 (engine r395, build 260619.66) — the flip-card column width follows the card count: the census (the gold's 2-card 0.86 / 4-card 0.76 col-md-6; Claude all col-md-4), the two cuts (English's tie + ConnectED / NCEA1 / TEDC excluded on the second), the probe (OFF 2109 / 2109; ON 39 pages / 37 modules, 15 up / 1 down, +19.4), the scoped regen + gates (skeleton 53.674 → 53.684, ≥75 +1; every other gate EXACT), the miner re-mine (173 rows; #3649 gone), the finalise. |\n")
    s = s.replace(line, ROW + line, 1)
    wr(P, s); print("README: r395 row")
print("finalise done")
