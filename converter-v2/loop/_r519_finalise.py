#!/usr/bin/env python3
"""ROUND 519 finalise (session 50 Round 12 — the drag-and-drop fill-in-the-blank (FIB) form + the Standard form for
'one answer at the line's end', DDFIB_OFF). WSL. argv: MEAN RAW."""
import sys
import _s50_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-26 (round 519, build 260620.80) — THE DRAG-AND-DROP FILL-IN-THE-BLANK FORM: a writer's `[drag and drop]` whose answers are RED WORDS INSIDE BLACK SENTENCES builds KB 03B's FIB layout (the red words the drags, each a blank in its sentence), and where every line ends in its one answer, KB 03B's Standard (matching) layout; 9 widgets / 8 modules built (5 FIB + 4 Standard), 59 drags, 52 of them the gold's own drags; the verifier learns the FIB form

### 1. WHAT CHANGED

**The class** (`_s50_r12_fib.cjs`: 31 un-built dragAndDrop bundles / 21 modules carry ≥ 2 lines of black text with a short red word on them, no table, no media — the MX family most). The writer types the sentence with the answers in red and says so ("The words in red are in the correct place — can we make these draggable and muddle up please"; "Correct answers are in red"). D10-3 (the build lane) + D13-4 (only where the writer marked the answer).

**The build** (`InteractiveBuilder.#typing` with a `fib` option — r449's red-answer reading reused, so a red answer is an answer by `Utils.AnswerKeyRedWord` exactly as in the typing quiz; the dragAndDrop dispatch tries it only where the r69 text / r350 image / r351 column forms all declined; data `interactive_builders.dragAndDrop.fib`, env **`DDFIB_OFF`**):
- **FIB** (KB 03B "FIB Layout"): `div.dragAndDrop layout="FIB"` > `div.row.dropContainer` of the sentences, each red answer an inline `<span class="drop" option="n">`, then a `div.row` of `div.drag option="n"` holding the answers in order, then the button row.
- **Standard** (`fib.trailing_as_standard`): when EVERY line is a prompt ending in its one answer and the answers are distinct, the widget is KB 03B's matching form (the prompts the questions, the answers the drags — the gold's own MXFL401 6B form); a FIB needs the blank inside the sentence.
- **autoCheck** from the WRITER's own words ("self marking" — the r449 list): the class and, per KB 03B "With autoCheck", the Reset button only (`fib.buttons_autocheck`).
- **Declines** (the hand-off box stays): a drawn blank (`____` — MXDI201's number line, which the gold builds as a scatter image; CEDO402's blank-line copy of the sentences), two answers with no words between them (MXDB302's tab-laid table — the gold builds a table widget), a line with no words, plus every r449 decline (a table, a nested widget, a red instruction inside a line, an answer-key label, > 6 words, a bracket).
- The FIB / Standard build places every member itself, so the r351 members rule (`#ddWithMembers`, which would re-render the sentences as prose or decline on the red words) is skipped for it.

**The tool** (`reference/tests/_verify_dragdrop.cjs`): `checkFib` — drops == drags, every option paired, no empty drag, no sentence without words, no drawn blank, the button row, no raw [tag], no lazy; per-module `FIB n` in the totals; the selftest gains BLL241 (LIVENESS 6 widgets on 4 fixtures; DETECTION 0 → 14 with an unpaired FIB drag injected). Its first run caught MXEO301 / MXFL301's autoCheck widgets carrying the Undo / Check row — fixed before the ship.

### 2. PROOF

- In-memory probe over all 545 modules: `DDFIB_OFF=1` → 0 pages changed; ON → **8 modules** (BLL235, BLL237, BLL241, MXEO301, MXFL201, MXFL301, MXFL401, MXFU401). `scoped_ship.sh … --round 519` PASS (0 stale, containment 8 ⊆ 8, the 12-module spot-check byte-identical).
- `_verify_dragdrop.cjs` over the 8: **9 widgets (FIB 5, Standard 4), 59 drags, defect 0**; 52 drags (88 %) are the gold's own drag texts, 5 more words of the gold's page; BLL237's writer marked "tomatoes / and / … / roasted" where the gold chose "small / … / stews" — the writer's red is the target (D13-4).
- Coverage dashboard: dragAndDrop hand-off boxes **1028 → 1019**, built 130 → 139.

### 3. PROTECTED GATES

Skeleton **55.7491 → {MEAN} % @ 2486** — a NAMED −0.0001pp, one page: MXFL401_6_0 scaffold 31.36 → 31.09 % (matched lines HELD at 37; 118 → 119 lines — the built widget's one extra line) while its RAW rose 22.09 → 29.94 % (`--accept-named "skeleton SCAFFOLD mean"`); ≥50 1612 / ≥75 285 / ≥90 26 held; RAW → {RAW} %; cs exact 16769 / EXTRA 204 / missing 886, body ANY 235, clean 98.40 %, leak 52 / 42 all EXACT; tags 9557; every verifier ✓, every COUNT held (dragdrop 21 on its gate set) (`_r519_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 519`; `--gate-baseline-check` PASS. Plateau (D10-3 (a), a build round): 9 sites converted, under the 20-site progress line — counts 1 of 3.

**Ledger:** scoped #5 since the r513 FULL · data `interactive_builders.dragAndDrop.fib` (decline_text_pattern, trailing_as_standard, buttons_autocheck) · env `DDFIB_OFF` · code `InteractiveBuilder.#typing` (the `fib` / `ddTpl` options) + the dragAndDrop dispatch + the `#ddWithMembers` skip · tool `_verify_dragdrop.cjs` checkFib + the BLL241 fixture (`_selftest_core.cjs`) · session 50 Round 12.
"""
F.finalise(
    N=519, old_build="260620.79", new_build="260620.80", entry=entry,
    config_comment="THE DRAG-AND-DROP FILL-IN-THE-BLANK FORM (session 50 Round 12): red answers inside black sentences -> KB 03B "
                   "FIB; one answer at every line's end -> the Standard matching form. Env DDFIB_OFF.",
    og9=None,
    og11="| `DDFIB_OFF` | 519 | **THE DRAG-AND-DROP FIB FORM** (session 50 Round 12). Reverts `interactive_builders.dragAndDrop.fib`: "
         "the writer's `[drag and drop]` with red answers inside black sentences (BLL235 / 237 / 241, MXFL301, MXFU401 → FIB; MXEO301 ×2, "
         "MXFL201, MXFL401 → Standard) goes back to the hand-off box (the r518 output exactly). |",
    og14=f"- **Build:** `260620.80` (round 519 — **the drag-and-drop FIB form**; `DDFIB_OFF`; scoped #5 since the r513 FULL; 9 widgets / "
         f"8 modules, 52 of 59 drags the gold's own; skeleton {MEAN} % (a NAMED −0.0001pp, MXFL401_6_0), RAW {RAW} %).",
    gb_note=f"Round 519 (session 50 Round 12, 2026-09-26) — THE DRAG-AND-DROP FIB FORM (DDFIB_OFF): 9 widgets / 8 modules (5 FIB + 4 "
            f"Standard), 59 drags, 52 the gold's own; _verify_dragdrop.cjs checkFib + BLL241 fixture; skeleton {MEAN} (NAMED -0.0001pp, "
            f"MXFL401_6_0 matched 37 held, lines 118 -> 119, RAW 22.09 -> 29.94); scoped #5.",
    no_round=f"- **No round in flight** (26 Sept 2026 {T}, session 50 Round 12 — r519 (the drag-and-drop FIB form) SHIPPED and "
             "committed; the in-flight marker is cleared). LAST SHIPPED **r519** (260620.80); **LAST FULL = r513 (the session-50 Round 5 "
             "backstop)**; ledger **scoped #5** (3 of headroom). Ride-along patches (LOOP §3 step 1 reads this list at every PICK): "
             "`outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, 10 pages / "
             "9 modules — CEDK401, HIS1002, HPRE203, MXDI201, MXDI202 ×2, MXEX302, SSOG105, TWHA906, XGF9004) / `_r468_declined.patch` "
             "(the lesson menu's `[H2]` lead, 3 pages — CBI1008 L1 / L2, PES1004_8_0) / `_r489_accbullet_declined.patch` (the accordion "
             "bulleted bold lead, 8 accordions / 4 modules — MXEX302, ENGS101, XGF9003, XLP05) / `_r463_declined.patch` (the WJFUN "
             "tile's \"Year N\" lead, 1 page) / `_r512_declined.patch` (the `[Activity: Embedded] <widget>` bracket, 10 modules — rides "
             "only after the TRR table-dialect ownership fix). Checked at r519: none rides (none of their pages is in the 8).",
    last_shipped=f"- LAST SHIPPED: **r519** (build 260620.80, 26 Sept {T}, session 50 Round 12 — THE DRAG-AND-DROP FILL-IN-THE-BLANK "
                 "FORM, `DDFIB_OFF`; SCOPED, **scoped #5 since the r513 FULL**; 9 widgets / 8 modules (5 FIB + 4 Standard), 52 of 59 "
                 f"drags the gold's own; dragAndDrop boxes 1028 → 1019; skeleton {MEAN} % (a NAMED −0.0001pp on MXFL401_6_0), RAW {RAW} %).",
    before_them_add="the typing quiz's table form",
    plateau="- Plateau window (§4): **1 of 3** — r519 a widget build, 9 sites converted (< the D10-3 (a) 20-site line: counts); "
            "r518 a measurement-tool round + guard, gate-neutral (neither); ",
    standing="- Standing facts: AppVersion **260620.80** (r519 the drag-and-drop FIB form — session 50 Round 12, 26 Sept); before it "
             "260620.79 (",
    roundlog=f"- s50-r12 (engine r519, build 260620.80, 26 Sept ≈04:27 → {T}) · a PICK pass (the hand-off lane `_s43_wl2_run.sh s50`; "
             "`[Summary]` class C; the r510 9-word lead recorded) then THE DRAG-AND-DROP FILL-IN-THE-BLANK FORM (+ the Standard form for "
             "one answer at the line's end) · SHIPPED scoped #5 · 9 widgets / 8 modules, 52 of 59 drags the gold's own, boxes 1028 → "
             "1019 · skeleton −0.0001pp NAMED · plateau 1 of 3 (a build round under 20 sites).",
    archive_extra="- **What shipped (r519, 260620.80):** `#typing` fib / ddTpl options + dispatch + #ddWithMembers skip; "
                  "`dragAndDrop.fib` (decline_text_pattern, trailing_as_standard, buttons_autocheck) (DDFIB_OFF); `_verify_dragdrop.cjs` "
                  "checkFib + BLL241 fixture. Probe OFF 0; ON 8 modules; named −0.0001pp (MXFL401_6_0).",
)
