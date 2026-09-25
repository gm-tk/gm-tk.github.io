#!/usr/bin/env python3
"""ROUND 520 finalise (session 50 Round 13 — the FIB form's remainder, DDFIBREST_OFF). WSL. argv: MEAN RAW."""
import sys
import _s50_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-26 (round 520, build 260620.81) — THE FIB FORM'S REMAINDER: three writer shapes r519 declined inside its own family now build — a red `<` / `>` answer (MXEO301 3F / 6A "Greater than or less than?"), a trailing `[button] Check answers` / `Answers` the KB button row covers (TWHK907, TWHA906), the prose the capture ran on into after the questions (rendered after the widget) — and the sentence's own full stop leaves the drag; 4 widgets / 3 modules, 34 drags, 31 the gold's own; dragAndDrop boxes 1019 → 1015

### 1. WHAT CHANGED

**The measure** (`_s50_r13_fibrest.cjs` — every FIB-shaped dragAndDrop bundle r519 did not build, with its member signature: 40 bundles). Merged multi-widget bundles (the MX "[Activity 3A – drag and drop] [Activity 3B – type the answer]" pairs) and tables are left alone; the rest decline on a handful of writer habits.

**The build** (`InteractiveBuilder.#typing`, fib mode only — the typing quiz is unchanged; data `interactive_builders.dragAndDrop.fib.remainder`, env **`DDFIBREST_OFF`** = the r519 output exactly):
- `symbol_answer_pattern` — a red `<` / `>` / `≤` / `≥` / `=` is the writer's answer (the r448 red-word reader skips a word with no letter or digit).
- `button_label_pattern` — a trailing `[button]` labelled Check answers / Reset / Undo / Answers is the KB button row the build already emits.
- `trailing_prose` — answer-less paragraphs the capture ran on into AFTER the questions (MXEO301 6A's following `[body]` paragraph) render as prose after the widget; a question after them still declines.
- `answer_trailing_punct` — 'publishers.' → the drag 'publishers', the full stop stays in the sentence after the blank.
- `marker_tag_pattern` — the writer's `[correct answer]` marker after each red word is read as the answer marker (a word inside the marker's own run is the answer); `headless_first_row_declines` — when the FIRST sentence alone opens on its blank, its head was left outside the capture (BLL247 "The bus": the scanner keeps black text right after the opener out of the bundle — the shipped page already renders it as a list item before the box), so BLL247 stays a hand-off box rather than ship a headless sentence (the scanner fix is recorded as a follow-up).

### 2. PROOF

- In-memory probe over all 545 modules: `DDFIBREST_OFF=1` → 0 pages changed; ON → **3 modules** (MXEO301, TWHA906, TWHK907). `scoped_ship.sh … --round 520` PASS (0 stale, containment 3 ⊆ 3, the 12-module spot-check byte-identical).
- `_verify_dragdrop.cjs` over the 3 (+ BLL247): FIB 4 + MXEO301's r519 Standard widgets, 45 drags, **defect 0**; the 4 new widgets' 34 drags — 31 the gold's own drag texts, 1 more a word of the gold's page.
- Coverage dashboard: dragAndDrop hand-off boxes **1019 → 1015**, built 139 → 143.

### 3. PROTECTED GATES

Skeleton **55.7490 → {MEAN} % @ 2486** — a NAMED −0.0001pp, one page: MXEO301_6_0 scaffold 60.14 → 59.93 % (matched lines HELD at 166; 276 → 277 lines — the built widget's one extra line) while its RAW rose 32.71 → 33.56 % (`--accept-named "skeleton SCAFFOLD mean"`); ≥50 1612 / ≥75 285 / ≥90 26 held; RAW → {RAW} %; cs exact 16769 / EXTRA 204 / missing 886, body ANY 235, clean 98.40 %, leak 52 / 42 all EXACT; tags 9557; every verifier ✓, every COUNT held (`_r520_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 520`; `--gate-baseline-check` PASS. Plateau (D10-3 (a)): 4 sites converted, under the 20-site line — counts 2 of 3.

**Ledger:** scoped #6 since the r513 FULL · data `interactive_builders.dragAndDrop.fib.remainder` · env `DDFIBREST_OFF` · code `InteractiveBuilder.#typing` (fib mode) · session 50 Round 13.
"""
F.finalise(
    N=520, old_build="260620.80", new_build="260620.81", entry=entry,
    config_comment="THE FIB FORM'S REMAINDER (session 50 Round 13): symbol answers, a trailing KB button tag, the prose after "
                   "the questions, the sentence's full stop out of the drag. Env DDFIBREST_OFF.",
    og9=None,
    og11="| `DDFIBREST_OFF` | 520 | **THE FIB FORM'S REMAINDER** (session 50 Round 13). Reverts `interactive_builders.dragAndDrop.fib.remainder`: "
         "MXEO301 3F / 6A (symbol answers), TWHK907 / TWHA906 (a trailing `[button]`) go back to the hand-off box (the r519 output exactly). |",
    og14=f"- **Build:** `260620.81` (round 520 — **the FIB form's remainder**; `DDFIBREST_OFF`; scoped #6 since the r513 FULL; 4 widgets / "
         f"3 modules, 31 of 34 drags the gold's own; skeleton {MEAN} % (a NAMED −0.0001pp, MXEO301_6_0), RAW {RAW} %).",
    gb_note=f"Round 520 (session 50 Round 13, 2026-09-26) — THE FIB FORM'S REMAINDER (DDFIBREST_OFF): 4 widgets / 3 modules (MXEO301 x2, "
            f"TWHA906, TWHK907), 34 drags, 31 the gold's own; skeleton {MEAN} (NAMED -0.0001pp, MXEO301_6_0 matched 166 held, lines "
            f"276 -> 277, RAW 32.71 -> 33.56); scoped #6.",
    no_round=f"- **No round in flight** (26 Sept 2026 {T}, session 50 Round 13 — r520 (the FIB form's remainder) SHIPPED and "
             "committed; the in-flight marker is cleared). LAST SHIPPED **r520** (260620.81); **LAST FULL = r513 (the session-50 Round 5 "
             "backstop)**; ledger **scoped #6** (2 of headroom). Ride-along patches (LOOP §3 step 1 reads this list at every PICK): "
             "`outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, 10 pages / "
             "9 modules — CEDK401, HIS1002, HPRE203, MXDI201, MXDI202 ×2, MXEX302, SSOG105, TWHA906, XGF9004) / `_r468_declined.patch` "
             "(the lesson menu's `[H2]` lead, 3 pages — CBI1008 L1 / L2, PES1004_8_0) / `_r489_accbullet_declined.patch` (the accordion "
             "bulleted bold lead, 8 accordions / 4 modules — MXEX302, ENGS101, XGF9003, XLP05) / `_r463_declined.patch` (the WJFUN "
             "tile's \"Year N\" lead, 1 page) / `_r512_declined.patch` (the `[Activity: Embedded] <widget>` bracket, 10 modules — rides "
             "only after the TRR table-dialect ownership fix). Checked at r520: none rides (no patch has all its pages inside the 3).",
    last_shipped=f"- LAST SHIPPED: **r520** (build 260620.81, 26 Sept {T}, session 50 Round 13 — THE FIB FORM'S REMAINDER, "
                 "`DDFIBREST_OFF`; SCOPED, **scoped #6 since the r513 FULL**; 4 widgets / 3 modules, 31 of 34 drags the gold's own; "
                 f"dragAndDrop boxes 1019 → 1015; skeleton {MEAN} % (a NAMED −0.0001pp on MXEO301_6_0), RAW {RAW} %).",
    before_them_add="the typing verifier's table form + guards",
    plateau="- Plateau window (§4): **2 of 3** — r520 a widget build, 4 sites (< the D10-3 (a) 20-site line: counts); "
            "",
    standing="- Standing facts: AppVersion **260620.81** (r520 the FIB form's remainder — session 50 Round 13, 26 Sept); before it "
             "260620.80 (",
    roundlog=f"- s50-r13 (engine r520, build 260620.81, 26 Sept ≈05:08 → {T}) · a PICK pass (the dashboard's ranked queue; "
             "`_s50_r13_fibrest.cjs` — 40 FIB-shaped bundles r519 left) then THE FIB FORM'S REMAINDER (symbol answers, a trailing KB "
             "button tag, the prose after the questions, the full stop out of the drag; BLL247 declined — headless first sentence) · "
             "SHIPPED scoped #6 · 4 widgets / 3 modules, 31 of 34 drags the gold's own, boxes 1019 → 1015 · skeleton −0.0001pp NAMED · "
             "plateau 2 of 3.",
    archive_extra="- **What shipped (r520, 260620.81):** `#typing` fib-mode remainder readings; `dragAndDrop.fib.remainder` "
                  "(DDFIBREST_OFF). Probe OFF 0; ON 3 modules; named −0.0001pp (MXEO301_6_0).",
)
