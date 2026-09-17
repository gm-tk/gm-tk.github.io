#!/usr/bin/env python3
"""ROUND 355 (loop session 15 Round 5 — a measurement-tool round: the skeleton scorer's autojunk cliff) — finalise: changelog,
AppVersion (260619.25 → 260619.26), CLAUDE.md §9 / §14, gate_baseline.json skeleton block, loop/README.md rows, LOOP_STATE.md
(ceiling quote + round record). Idempotent."""
import io, os, json
ROOT = r"C:\Users\Gavin\TeKura\FINAL_MODULE_DATA"
PF = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)

CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)" + chr(10) + chr(10)
ENTRY = """## 2026-09-17 (round 355, build 260619.26) — THE SKELETON SCORER'S AUTOJUNK CLIFF: `_skeleton_compare.py` NOW SCORES WITH `autojunk=False` — 128 pages (every long single-page Fundamentals / BLL module) had been scored with most of their structure IGNORED by difflib's junk heuristic (BLL170 0.0 read 14.1 % where its true ratio is 58.2 %); the corpus mean is RE-BASELINED 50.965 → 51.979 % (+1.01pp, an INSTRUMENT correction, never a gain), ≥ 50 % 1073 → 1093, RAW 35.117 → 36.711 %; a measurement-tool round (the r315 precedent; the autonomous loop's session-15 Round 5) — no engine or data change, no regeneration, every other gate untouched, gate-neutral by design

### 1. WHAT CHANGED

**`difflib.SequenceMatcher`'s AUTOJUNK heuristic (on by default) marks any element that occurs in more than 1 % of a sequence of 200+ items as "junk" and never matches on it. A page skeleton IS made of such lines ("p", "WIDGET", "div.row", "div.col-md-8.col-12"), so every page whose skeleton reaches 200 lines was scored with most of its structure ignored** — the cliff r352 hit when five restored `<p>` (the gold has them) pushed CHFUN06 0.0 from 198 to 203 lines and its score from 56.1 to 25.5 %. The scorer now compares with `autojunk=False` (`SKAUTOJUNK=1` restores the pre-355 numbers for a one-off comparison — proven identical: 50.9646 %); every baseline that carries a skeleton number is re-established on the same corpus.

### 2. THE MEASUREMENT (`outputs/_r355_skeleton_noautojunk.py` — the trial scorer on the r354 corpus → `_r355_sk_noautojunk.{json,log}`; the shipped scorer reproduces it per page — `_r355_sk_final.json`)

- **128 pages change, 126 UP, 2 down by < 1pp:** BLL170 0.0 14.1 → 58.2, TEFUN02 0.0 13.4 → 57.1, BLL210 0.0 14.3 → 54.8, BLL140 0.0 16.2 → 56.2, TEFUN04 0.0 14.3 → 53.3, CEDO502 1.1 18.5 → 53.3 … — the long single-page Fundamentals / BLL / TE modules the dashboard's "worst pages" list has carried for months were a measurement artefact; the two dips TWHK901 0.0 6.8 → 5.8 and CEDT104 0.0 6.0 → 5.7 are the same pages scored honestly.
- **Corpus: SCAFFOLD 50.9646 → 51.9788 % (+1.0142pp), ≥ 50 % 1073 → 1093, ≥ 75 % 160, ≥ 90 % 14 @ 1955; RAW 35.1173 → 36.7108 %.** The ceiling instrument (`_measure_ceiling.py`) does not use SequenceMatcher — the ceiling stays 91.9 %; **% of achievable = 56.6 % (was 55.5 %)** — an instrument correction, recorded as such.
- Every other gate is untouched (no engine / data change, no regeneration): cs 11607 / 175 / 617, clean 2080/2103, leak 26/23, body 182, tags 9557/9557, every verifier EXACT; the scorer's `--selftest` GREEN.

**Ledger:** no ship (no regeneration) · no data flag (a gate tool; env `SKAUTOJUNK=1` = the old instrument) · gate tools (outside git, mirrored to `loop/`) `_skeleton_compare.py`, `gate_baseline.json` · tools `outputs/_r355_skeleton_noautojunk.py`, `_r355_sk_noautojunk.{json,log}`, `_r355_sk_final.json`, `_r355_sk_full.log`, `_r355_sk_old.{json,log}`, `_r355_widgetloss*.{json,log}` / `_r355_losses_by_shape.log` / `_r355_overcapture_census.log` / `_r355_tagred.{json,log}` (the PICK measurements that found the queue exhausted at the floor), `_r355_finalise.py` · AppVersion 260619.26.

"""
if "round 355, build 260619.26" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r355 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.26"' not in s:
    old = '\tstatic AppVersion = "260619.25";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, '\t// ROUND 355 (260619.26): a measurement-tool round — _skeleton_compare.py scores with autojunk=False (128 long pages were scored with most of their structure ignored); the skeleton baselines re-established.\n' + '\tstatic AppVersion = "260619.26";', 1)
    wr(P, s); print("Config.js: 260619.26")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "ROUND 355 BASELINE" not in s:
    OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 352 BASELINE"
    assert s.count(OLD9) == 1, "§9 anchor"
    NEW9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 355 BASELINE — THE INSTRUMENT CORRECTED: the scorer compares with `autojunk=False` (difflib's junk heuristic had ignored most of the structure on every page whose skeleton reaches 200 lines — 128 pages, BLL170 0.0 14 → 58 %); re-established on the r354 corpus, no page changed: SCAFFOLD mean 51.979% / >=50% 1093 / >=75% 160 / >=90% 14 / skipped 0 @ 1955; RAW 36.711%** (state `outputs/_r355_sk_final.json`, FRESH) = **56.6% of achievable** (ceiling 91.9%). The +1.01pp is an instrument correction, never a gain; `SKAUTOJUNK=1` reproduces the old 50.965%. Older r352 text: **ROUND 352 BASELINE")
    s = s.replace(OLD9, NEW9, 1)
    OLD14 = "- **Build:** `260619.25` (round 354"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.26` (round 355 — **a measurement-tool round: `_skeleton_compare.py` scores with `autojunk=False`** — difflib's junk heuristic had scored every 200+-line skeleton with most of its structure ignored (128 pages, 126 up: BLL170 14 → 58, TEFUN02 13 → 57, BLL210 14 → 55); the loop's session-15 Round 5; no engine / data change, no regeneration). **ROUND 355 BASELINE (the r354 corpus, re-scored): SCAFFOLD mean 51.979% / ≥50% 1093 / ≥75% 160 / ≥90% 14 / skipped 0 @ 1955 (50.965 → 51.979 = +1.01pp, an INSTRUMENT correction); RAW 36.711% (35.117 → 36.711)** (state `outputs/_r355_sk_final.json`, FRESH) = **56.6% of achievable** (ceiling 91.9%). Every other number = the r352 state (cs 11607 / 175 / 617; clean 2080/2103; leak 26/23; body 182; math 323/323; all verifiers EXACT). `SKAUTOJUNK=1` restores the old instrument for a one-off comparison.\n"
             "- **Build:** `260619.25` (round 354")
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §9 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if "_note_r355" not in d["skeleton"]:
    d["skeleton"]["mean_scaffold_pct"] = 51.979
    d["skeleton"]["pages_ge_50"] = 1093
    d["skeleton"]["raw_mean_pct"] = 36.711
    d["skeleton"]["_note_r355"] = "Round 355: the scorer compares with autojunk=False (difflib's junk heuristic had ignored most of the structure on every 200+-line skeleton — 128 pages, 126 up); re-established on the r354 corpus with no page change: SCAFFOLD 51.979 (was 50.965 — an instrument correction, never a gain), >=50 1093, >=75 160, >=90 14, RAW 36.711. SKAUTOJUNK=1 reproduces the old numbers. State outputs/_r355_sk_final.json."
    d["_meta"]["build"] = "260619.26"; d["_meta"]["round"] = 355
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: skeleton re-baselined")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_r355_finalise.py" not in s:
    A = "| `_measure_r354_tagwords.cjs` / `_r354_tw_run.sh`"
    assert s.count(A) == 1, "README anchor"
    ROWS = ("| `_skeleton_compare.py` / `gate_baseline.json` | `CONVERTER_V2/reference/tests/` | Session 15 Round 5 (r355, a measurement-tool round) — `autojunk=False` in the skeleton scorer (difflib's junk heuristic had ignored most of the structure on every 200+-line skeleton; 128 pages re-scored, 126 up); the skeleton baseline re-established on the r354 corpus (51.979 / 1093 / 160 / 14; RAW 36.711). `SKAUTOJUNK=1` = the old instrument. |\n"
            "| `_r355_skeleton_noautojunk.py` / `_r355_sk_noautojunk.{json,log}` / `_r355_sk_final.json` / `_r355_sk_full.log` / `_r355_sk_old.{json,log}` / `_measure_r355_widgetloss.cjs` / `_r355_wl_run.sh` / `_r355_widgetloss.json` / `_r355_widgetloss_confirm.log` / `_r355_losses_by_shape.log` / `_r355_overcapture_census.log` / `_measure_r355_tagred.cjs` / `_r355_tr_run.sh` / `_r355_tagred.{json,log}` / `_r355_debug.cjs` / `_r355_finalise.py` | `CONVERTER_V2/outputs/` | Session 15 Round 5 (r355) — the PICK measurements that found the queue exhausted at the 20-site floor after r354 (every text-loss shape < 20; the tag-line red runs 0 lost), the trial scorer and the re-scored corpus. |\n")
    s = s.replace(A, ROWS + A, 1)
    wr(P, s); print("README: r355 rows")

P = os.path.join(ROOT, "LOOP_STATE.md"); s = rd(P)
if "## Session 15 · Round 5 (measurement-tool round r355" not in s:
    A = "## Session 15 · Round 5 PICK (measurement-tool round r355"
    assert s.count(A) == 1, "LOOP_STATE PICK anchor"
    SHIPPED = """## Session 15 · Round 5 (measurement-tool round r355 — the skeleton scorer's autojunk cliff) — what shipped
- **Shipped 2026-09-17 ≈13:05 NZST (session 15).** AppVersion 260619.26, changelog entry r355, CLAUDE.md §9 / §14, `gate_baseline.json` skeleton block (51.979 / 1093 / 160 / 14; RAW 36.711), loop/README rows; `_skeleton_compare.py` compares with `autojunk=False` (`SKAUTOJUNK=1` = the old instrument, proven to reproduce 50.9646 % exactly); the fast-loop skeleton snapshot re-taken. No engine / data change, no regeneration; every other gate untouched.
- **Result:** the same r354 corpus re-scored — **SCAFFOLD 50.9646 → 51.9788 % (+1.01pp, an INSTRUMENT correction, never a gain), ≥ 50 % 1073 → 1093, ≥ 75 % 160, ≥ 90 % 14; RAW 35.117 → 36.711 %; % of achievable 55.5 → 56.6 %** (ceiling 91.9 % — the ceiling instrument does not use SequenceMatcher). 128 pages change, 126 up (BLL170 0.0 14.1 → 58.2, TEFUN02 13.4 → 57.1, BLL210 14.3 → 54.8, BLL140 16.2 → 56.2, TEFUN04 14.3 → 53.3, CEDO502 1.1 18.5 → 53.3 — the "worst pages" the dashboard listed for months were the instrument's), 2 down by < 1pp (TWHK901, CEDT104). Gate-neutral by design: outside the plateau window (neither counts nor resets).
- **The scorecard baseline from here:** the r355 state (`_r355_sk_final.json`): SCAFFOLD 51.979 % = 56.6 % of achievable, RAW 36.711 %, 1955 pairs, ceiling 91.9 %; cs 11607 / 175 / 617; clean 2080/2103; leak 26/23; body 182; math 323/323.

"""
    s = s.replace(A, SHIPPED + A, 1)
    B = "- Remaining KB queue (§D): stickyNav (BLOCKED"
    assert s.count(B) == 1, "position anchor"
    s = s.replace(B, "- Session 15 Round 5 (measurement-tool round r355 — the skeleton scorer's autojunk cliff: `autojunk=False`, 128 long pages re-scored honestly, the skeleton baseline re-established at 51.979 % / 1093 / 160 / 14, RAW 36.711 %, = 56.6 % of achievable — an instrument correction, never a gain): **SHIPPED 2026-09-17 ≈13:05 (session 15)**. AppVersion 260619.26, CLAUDE.md §9/§14, `gate_baseline.json`. No engine / data change, no regeneration.\n" + B, 1)
    C = "- s15-r4 (engine r354, the tag-line words → Writers Note)"
    assert s.count(C) == 1, "round log anchor"
    s = s.replace(C, "- s15-r5 (measurement-tool round r355, the skeleton scorer's autojunk cliff) · `_skeleton_compare.py` scores with autojunk=False — difflib's junk heuristic had ignored most of the structure on every 200+-line skeleton (128 pages, 126 up: BLL170 14 → 58) · SHIPPED · SCAFFOLD re-baselined 50.965 → 51.979 % (an instrument correction), ≥50 1073 → 1093, RAW 36.711 %; every other gate untouched · no regeneration · commit — see git log\n" + C, 1)
    # the ceiling quote
    D = "- **r313 SCAFFOLD 49.941% = 54.5% of achievable (band 53.0-54.5%)**; RAW 34.430% = 39.5% of achievable."
    if s.count(D) == 1:
        s = s.replace(D, D + "\n- **r355 (session 15, the instrument corrected — `autojunk=False`): SCAFFOLD 51.979% = 56.6% of achievable; RAW 36.711% = 39.9% (full-scope ceiling)**; the r313 → r354 numbers above and below were read through difflib's autojunk heuristic (every 200+-line skeleton scored with most of its structure ignored) — comparable among themselves, ≈ 1.0pp under the honest instrument.", 1)
    wr(P, s); print("LOOP_STATE.md: round 5 recorded")
print("finalise done")
