#!/usr/bin/env python3
"""ROUND 501 finalise (session 49 Round 1 — THE GATE-TOOL ROUND, measurement-tool, gate-neutral). WSL.
Notes only: every gate_baseline.json aggregate and the verifier counts were written by the tools themselves."""
import io, os, json, shutil, subprocess
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
NOW = subprocess.run(["date", "+%H:%M"], capture_output=True, text=True).stdout.strip()
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 501," not in sc[:4000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.63";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a14 = "- **Build:** `260620.63` (round 500"
a12 = "3. Note the **data flag** + **env toggle** you added (keep §11 of this file current).\n"
for a in (a14, a12): assert so.count(a) == 1, a
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 501 IN FLIGHT — NOT PROVEN**", "- **No round in flight** (25 Sept 2026 ≈15:55, session 46 Round 12", "- LAST SHIPPED: **r500**",
          "- Before it: **r499**", "- Before them: **r498 → r467**", "- Plateau window (§4): **0 of 3** — r500", "- Standing facts: AppVersion **260620.63**",
          "## Round log"):
    find(p)

entry = """## 2026-09-25 (round 501, build 260620.64 — NO engine change; measurement-tool round, gate-neutral by design) — THE GATE-TOOL ROUND: the committed gate baseline's aggregates are written by the tools, and every count-bearing verifier turns red when its count FALLS

### 1. WHAT CHANGED

**Why** (the third `/loop-review`, 25 Sept 2026, LOOP §3 steps 6–7): the r494–r498 finalise scripts typed `gate_baseline.json` fields by hand and missed some (`mean_scaffold_pct`, `median_scaffold_pct`, `body_compare.any_breakdown`) — eight rounds were judged against a stale baseline until the session-46 backstop re-based it; and the bingo / typing / dragAndDrop verifiers read ✓ at defect 0 even when NOTHING was built (a builder that stops building passes vacuously).

**The tools** (`CONVERTER_V2/reference/tests/`, outside git — mirrored into `converter-v2/loop/`):
- `_fastloop_diff.py` — `gate_fields()` computes EVERY aggregate `gate_baseline.json` carries (skeleton mean / upper median / ≥50 / ≥75 / ≥90 / RAW / pairs / skipped; compare_structure exact / EXTRA / missing / row-wrap; body_compare ANY / over-capture / runaway / empty; defect clean / total / clean % / leak occ / leak pages) with each gate's own formula and rounding; `write_gate_baseline()` writes them by a section-aware LINE edit (the file mixes 2- and 4-space indents, so it is never re-serialised) and sets `_meta.round` / `build` / `date`; `--commit` (PASS or `--accept-named`) now calls it, keeps the fast-loop skeleton wrapper's summary in step, and takes `--round N` / `--build X`; **`--gate-baseline-check`** compares the committed file with the shipped state (exit 1 on drift).
- `_gatecheck.py --commit --round N` — the same write from a FULL run's live gate JSONs (the backstop re-base).
- `scoped_ship.sh` — `--round` is passed to `_fastloop_diff.py --commit`; `--accept-named M` passes a NAMED mover through.
- NEW `_verify_count.cjs` + `_verify_{bingo,typing,dragdrop,flipcard,math,menulabels}.cjs` — each prints `COUNT (<key>): … vs <baseline>` for its totals AND per module, on its recorded `run_all_gates.sh` module set (an ad-hoc set reads n/a), and its RESULT reads ✗ (exit 1) when a count FELL; `VERIFY_COUNT_RECORD=1` records the counts (`count_per_module`, `count_modules`) by the same line edit. `_selftest_core.cjs` never passes the record flag to a fixture run. All six, not the three the review named: flipCard / math / menulabels had no count test either.

### 2. PROOF

- **The drift the tool found at once** (`_fastloop_diff.py --gate-baseline-check` on the r500 shipped state): three committed fields were stale — `skeleton.median_scaffold_pct` 56.5 (live 56.6), `body_compare.over_capture` 61 (live 59), `body_compare.empty_container` 175 (live 171); each matches the r500 full gate log's own printout (`_r500_gates.log`: "median 56.6%", "OVER-CAPTURE … 59", "EMPTY … 171"). The other 18 fields were already equal.
- **The commit path** (`_r501_commit_proof.log`): CEDO105 regenerated with the r500 engine — **byte-identical** (`_content_manifest.py changed` = none) — then `_fastloop_diff.py CEDO105 --commit --round 501 --build 260620.64`: every protected gate HELD, PASS; it wrote exactly the three corrections + `_meta`; the diff of `gate_baseline.json` against `.pre-r501.bak` is those six lines and nothing else; `--gate-baseline-check` → PASS.
- **The counts** recorded on the r500 corpus (`_r501_verifiers.sh`, `VERIFY_COUNT_RECORD=1`): flipCard 61, math 323 / 323, menulabels **111** (the committed 99 was stale — another typed field), dragAndDrop 21, bingo 52 grids / 624 cells, typing 8 quizzes / 57 inputs; each total equals the r500 gate log.
- **The null test:** `BINGO_OFF=1` → `COUNT (bingo): grids 0 vs 52 … ✗ FELL` and RESULT ✗, rc 1 (before r501 the same run read "every built bingo grid is the KB 03E form ✓"); ON → ✓ held; an ad-hoc one-module run → n/a.
- **Selftests:** flipCard / math / menulabels / dragAndDrop / bingo GREEN (`_selftest_core.cjs`), typing SELFTEST GREEN (`_r501_selftests.log`).

### 3. PROTECTED GATES

- Full suite `_r501_gates.log` on the r500 corpus (no Claude page changed): skeleton **55.4588 % @ 2491** (≥50 1592 / ≥75 277 / ≥90 26), pairs skipped 0; cs exact 16746 / EXTRA 198 / missing 888 / row-wrap 24; body ANY 232; clean 2591 / 2633; leak 52 / 42; tags 9557 / 9557; every verifier RESULT ✓ with its COUNT line "held (per module too)". **Gate-neutral by design** — plateau: neither.

**Ledger:** no ship (no regeneration beyond the byte-identical CEDO105 proof) — still scoped #4 since the r498 FULL · no data flag / env toggle (no engine or data file touched) · tools `_fastloop_diff.py`, `_gatecheck.py`, `scoped_ship.sh`, `_verify_count.cjs`, the six verifiers, `_selftest_core.cjs`, `_r501_verifiers.sh`, `_r501_finalise.py` · session 49 Round 1.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 501 (260620.64): THE GATE-TOOL ROUND (session 49 Round 1) — no engine change: the committed gate baseline's "
                "aggregates are written by _fastloop_diff.py / _gatecheck.py --commit; six verifiers gained the count-vs-baseline test.\n"
                + '\tstatic AppVersion = "260620.64";')
wr(PJ, sj); print("config ok")
so = so.replace(a14, "- **Build:** `260620.64` (round 501 — **the gate-tool round**, NO engine change: `_fastloop_diff.py` / `_gatecheck.py "
                "--commit --round N` write every `gate_baseline.json` aggregate, `--gate-baseline-check` proves no drift; the six count-bearing "
                "verifiers print `COUNT` vs the baseline and read ✗ when it FELL; the baseline's three stale fields corrected — median 56.6, "
                "over-capture 59, empty 171; menulabels 111).\n" + a14)
so = so.replace(a12, a12 + "3b. **The committed gate baseline is written by the tools, never by hand (ROUND 501, 25 Sept 2026).** "
                "`scoped_ship.sh … --commit --round N` (→ `_fastloop_diff.py … --commit --round N`) and, after a FULL run, "
                "`_gatecheck.py … --commit --round N` write EVERY `gate_baseline.json` aggregate and `_meta.round`; a verifier count that "
                "legitimately grew (or a NAMED shrink) is recorded with `VERIFY_COUNT_RECORD=1 bash run_all_gates.sh`; the finalise script "
                "edits notes and `_meta.build` only. `_fastloop_diff.py --gate-baseline-check` must print PASS before the commit.\n")
wr(PO, so); print("OG ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json")
G = rd(P).split("\n")
hits = [i for i, l in enumerate(G) if l.strip().startswith('"_note_r500": ')]; assert len(hits) == 1
G.insert(hits[0], '    "_note_r501": "Round 501 (session 49 Round 1, 2026-09-25) — THE GATE-TOOL ROUND (no engine change): every aggregate here is now '
         'written by _fastloop_diff.py / _gatecheck.py --commit (never typed); its first write corrected three stale fields — '
         'skeleton.median_scaffold_pct 56.5 -> 56.6, body_compare.over_capture 61 -> 59, body_compare.empty_container 175 -> 171 '
         '(each = the r500 full gate log). The six count-bearing verifiers record count_per_module / count_modules (VERIFY_COUNT_RECORD=1); '
         'menulabels.labels 99 -> 111 (stale). Gates HELD on the r500 corpus.",')
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline note ok")
os.makedirs(os.path.join(ROOT, "_Backups", "loop_state"), exist_ok=True)
shutil.copyfile(S, os.path.join(ROOT, "_Backups", "loop_state", "LOOP_STATE.md.pre-r501-finalise.bak"))
i = find("- **ROUND 501 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = (f"- **No round in flight** (25 Sept 2026 {NOW}, session 49 Round 1 — r501 (the gate-tool round) SHIPPED and committed; the in-flight "
        "marker is cleared). LAST SHIPPED **r501** (260620.64); **LAST FULL = r498 (the session-46 Round 10 backstop)**; ledger **scoped #4** "
        "(r501 regenerated nothing — 4 of headroom). Ride-along patches (LOOP §3 step 1 reads this list at every PICK): "
        "`outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` (buttons, 10 pages) / `_r468_declined.patch` (the lesson "
        "menu's `[H2]` lead, 3 pages) / `_r489_accbullet_declined.patch` (the accordion bulleted bold lead, 8 accordions / 4 modules) / "
        "`_r463_declined.patch` (the WJFUN tile's \"Year N\" lead, 1 page).")
k = find("- **No round in flight** (25 Sept 2026 ≈15:55, session 46 Round 12"); prior = L[k]; del L[k]
k = find("- Before it: **r499**"); r499 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r500**"); L[k] = L[k].replace("- LAST SHIPPED: **r500**", "- Before it: **r500**", 1)
L.insert(k, f"- LAST SHIPPED: **r501** (build 260620.64, 25 Sept {NOW}, session 49 Round 1 — THE GATE-TOOL ROUND, measurement-tool, NO engine "
         "change, no regeneration: `_fastloop_diff.py` / `_gatecheck.py --commit --round N` write every `gate_baseline.json` aggregate, "
         "`--gate-baseline-check` proves no drift; the six count-bearing verifiers print COUNT vs the baseline and read ✗ when it FELL "
         "(null-tested: BINGO_OFF → ✗); the baseline's stale fields corrected — median 56.5 → 56.6, over-capture 61 → 59, empty 175 → 171, "
         "menulabels 99 → 111; every gate HELD on the r500 corpus: skeleton 55.4588 % @ 2491, ≥50 1592, ≥75 277, ≥90 26, cs exact 16746, "
         "body ANY 232, clean 2591, leak 52 / 42).")
k = find("- Before them: **r498 → r467**")
L[k] = L[k].replace("- Before them: **r498 → r467** (260620.61 → 260620.34 — the hover definition's red first letter,",
                    "- Before them: **r499 → r467** (260620.62 → 260620.34 — the hover definition after the full stop, the hover definition's red first letter,", 1)
assert "r499 → r467" in L[k]
k = find("- Plateau window (§4): **0 of 3** — r500")
L[k] = L[k].replace("- Plateau window (§4): **0 of 3** — r500", "- Plateau window (§4): **0 of 3** — r501 a measurement-tool round, gate-neutral by design (neither); r500", 1)
k = find("- Standing facts: AppVersion **260620.63**")
L[k] = L[k].replace("AppVersion **260620.63** (r500 the back-to-back split trigger — session 46 Round 12, 25 Sept); before it 260620.62",
                    "AppVersion **260620.64** (r501 the gate-tool round, no engine change — session 49 Round 1, 25 Sept); before it 260620.63 (r500 "
                    "the back-to-back split trigger — session 46 Round 12); before it 260620.62", 1)
assert "260620.64" in L[k]
k = find("## Round log")
L.insert(k + 1, f"- s49-r1 (r501, build 260620.64, 25 Sept 18:00 → {NOW}; NO engine change) · THE GATE-TOOL ROUND (LOOP §3 steps 6–7): the tools write "
         "every `gate_baseline.json` aggregate (`--commit --round N`; `--gate-baseline-check`), six verifiers gain the count-vs-baseline test "
         "(✗ when a count FELL; null-tested BINGO_OFF) · SHIPPED, no regeneration · 3 stale baseline fields + menulabels 99 → 111 corrected · "
         "every gate HELD · plateau 0 of 3 (neither).")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r499 + the r500 no-round line (verbatim, s49 r501)\n\n" + r499 + "\n" + prior + "\n"
    "\n## Session 49 — Round 1 (r501) — the gate-tool round\n\n" + marker + "\n"
    "- **What shipped (r501, 260620.64, no engine change):** `_fastloop_diff.py` gate_fields / write_gate_baseline / --gate-baseline-check; "
    "`_gatecheck.py --commit`; `scoped_ship.sh --round / --accept-named` passthrough; `_verify_count.cjs` + six verifiers; `_selftest_core.cjs` "
    "record-flag guard. Proof: drift found (median / over-capture / empty); commit path PASS (CEDO105 byte-identical); counts recorded; "
    "BINGO_OFF null test ✗; selftests GREEN; full suite HELD.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
