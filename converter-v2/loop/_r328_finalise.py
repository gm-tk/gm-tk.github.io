#!/usr/bin/env python3
"""ROUND 328 — finalise: changelog, AppVersion, CLAUDE.md §9/§11/§14, KB status row 55 (both copies), gate_baseline.json,
LOOP_STATE.md (what shipped + position + round log). Idempotent."""
import io, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)
SK, RAW = "50.492", "34.831"

CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
ENTRY = f"""## 2026-09-15 (round 328, build 260618.99) — A SUBMISSION BUTTON KEEPS ITS FULL "GO TO" LABEL (KB constraint 55's label half + CL-0038 / constraint 65 + 14.11; the autonomous loop, session 4, Round 3; **SCOPED regeneration of the 40 affected modules; gate-neutral — every protected gate EXACT; scoped ship #2 since the round-326 full**)

### 1. WHAT CHANGED, IN ONE LINE

**A writer's bare noun on a submission button — `[Button] Portfolio`, `[Add button] Quiz button`, `[Add button] Quiz`, `[Button] Dropbox` — now ships the KB's canonical label: `Go to portfolio`, `Go to quiz`, `Go to dropbox` (and `Upload to Dropbox` in the BLL / LS / HPE families, 14.11). 47 pages / 40 modules changed; Claude's bare `Quiz` / `Quiz button` / `Portfolio` / `Dropbox` labels 84 → 0.**

### 2. THE EVIDENCE (docx → human → Claude)

- **EXPFUN04** — docx: `[Button] Portfolio` ×6 (after "Head back to the journal or portfolio you are using…") → gold: `<a …><div class="button">Go to portfolio</div></a>` → Claude before: `Portfolio`; after: `Go to portfolio`.
- **HIS1004 lessons 2 / 3 / 6** — docx: `[Add button] Quiz button` / `[Add button] Quiz` → gold: `Go to quiz` → Claude before: `Quiz button` / `Quiz`; after: `Go to quiz` (the r326 anchor's quiz row already gave these `href="#"` and the quiz To Do wording — the canonical label now keys them by name).
- **HPFUN101** — docx: `[Add button] Quiz` → gold: `Go to quiz` → Claude after: `Go to quiz`.
- **The KB:** constraint 55 — "A submission button that sends the student to the dropbox or to their portfolio keeps its full 'Go to' label — 'Go to dropbox' / 'Go to portfolio' — the leading 'Go to' is never dropped to a bare 'Dropbox' / 'Portfolio'"; CL-0038 / constraint 65 — the quiz button reads `Go to quiz`; 14.11 / 14D — "the BLL, LS and HPE families label the dropbox button 'Upload to Dropbox'", a series-scoped label alongside the universal default. Round 323 captured row 55's full-stop half; this is the prefix half.

### 3. THE MEASUREMENT (every Claude page)

- **94 bare-noun labels on 54 pages / 44 modules** — quiz 34 + `quiz button` 11, portfolio 25, dropbox 13 + `drop box` 1, journal 10 (Fundamentals 35 / Standard 32 / Inquiry 27). In the same modules the gold's labels: quiz → `Go to quiz` ×128 (no other form), portfolio → `Go to portfolio` ×77, dropbox → `Upload to dropbox` ×58 (the gold's dominant dropbox label corpus-wide; the KB's universal default is `Go to dropbox` — the KB outranks the gold, §1b-1). `Journal` (10) has no KB label rule and is untouched (the r239 h4 rule covers `go to journal` labels only). The gold's own bare `Quiz` (4) / `Dropbox` (3) are its outliers.
- After: bare `Quiz` / `Quiz button` / `Portfolio` / `Dropbox` / `Drop box` **0**; `Go to quiz` 130, `Go to portfolio` 52, `Go to dropbox` 46, `Upload to Dropbox` 34 (the 14.11 families).

### 4. THE FIX — one data block `Emit_Templates.buttons.canonical_labels` `{{ enabled, env: "BTNLABEL_OFF", rules[] }}`

- **`ContentConverter.#buttonCanonicalLabel`** at the generic `[button]` seam (key === "button" only), after the round-323 trim and before the round-326 anchor: the first rule whose `label_match` hits the trimmed label supplies the canonical label (`^(?:the )?quiz(?: button)?$` → `Go to quiz`; portfolio → `Go to portfolio`; `drop ?box` → `Go to dropbox`); a rule's `family_labels` row wins for a module whose code prefix is listed (BLL / XLP XDLS XLS LS SLO SL / HES PHE PES HPE → `Upload to Dropbox`). Any other label is untouched.
- **Env toggle `BTNLABEL_OFF`** reverts byte-for-byte.

### 5. THE PROOF AND THE GATES

- The in-memory ON probe over ALL 416 modules (`_r328_probe_on_0*.log`) names **47 pages / 40 modules**; scoped regeneration (`_r328_batches_run.sh`); `_content_manifest.py fresh --affected` → **0 truly stale**; OFF in memory vs disk on the 40 = exactly the 47 changed pages; ON in memory = disk on 152/152.
- **Every protected gate EXACT** (`_fastloop_diff.py` PASS — 10 metrics HELD, every delta 0; the full suite `_r328_gates.log` identical to r327): skeleton SCAFFOLD mean **{SK}%** / ≥50% 1030 / ≥75% 196 / ≥90% 15 / skipped 0 @ 1954, RAW {RAW}% (`_r328_sk_final.json`: 0 pages moved) · cs exact 11360 / EXTRA 186 / missing 591 · clean 2056/2102 / leak 288/46 · body 191 · tags 9557/9557 · flipCard TOTAL 61 divergence 0 · mtkQuiz 17 shells defect 0 · entry-parity PASS · index-sync 33/28 · **13 selftests GREEN**.
- **Ceiling:** SCAFFOLD {SK}% = **55.1% of achievable** (unchanged).

### 6. NAMED, NOT CHASED

- The round-308 upload box's own `Upload to dropbox` label (the `[dropbox]` marker family, Chris's "Build it") and the writer-typed `Upload to dropbox` labels are untouched — constraint 55 governs the bare-noun defect, not a re-labelling of the gold-dominant form.
- `[Button] Journal` (10) — no KB label rule; `[Button] Go to` (13, a truncated writer label) — nothing derivable.

**Ledger:** scoped ship #2 since the r326 full · data `buttons.canonical_labels` · env `BTNLABEL_OFF` · tools `outputs/_r328_finalise.py` (the measurement is the inline probe recorded in `LOOP_STATE.md`) · state `outputs/_r328_sk_final.json` (FRESH, identical) · logs `_r328_gates.log`, `_r328_sk_full.log`, `_r328_fastloop.log`, `_r328_selftests.log`, `_r328_probe_on_0*.log`, `_r328_probe_off.log`, `_r328_probe_on.log`, `_r328_regen.log`, `_r328_affected.txt`.

"""
if "round 328, build 260618.99" not in s:
    assert s.startswith(head); s = head + ENTRY + s[len(head):]; wr(CL, s); print("changelog prepended")

CF = os.path.join(PF, "app", "js", "Config.js"); c = rd(CF)
OLD = '\tstatic AppVersion = "260618.98";\n'
NEW = ('\t// ROUND 328 (2026-09-15, build 260618.99): a submission button keeps its full "Go to" label (KB\n'
       '\t// constraint 55 / CL-0038 / 14.11): a writer\'s bare "Quiz" / "Portfolio" / "Dropbox" becomes "Go to\n'
       '\t// quiz" / "Go to portfolio" / "Go to dropbox" ("Upload to Dropbox" in BLL / LS / HPE). 47 pages /\n'
       '\t// 40 modules, scoped. Env BTNLABEL_OFF; data buttons.canonical_labels.\n'
       '\tstatic AppVersion = "260618.99";\n')
if '"260618.99"' not in c:
    assert c.count(OLD) == 1; c = c.replace(OLD, NEW, 1); wr(CF, c); print("AppVersion bumped")

CM = os.path.join(PF, "CLAUDE.md"); m = rd(CM)
OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 327 BASELINE (a multi-word ALL-CAPS title renders in sentence case — the KB's title-casing rule; scoped, gate-neutral)"
NEW9 = (f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 328 BASELINE (a submission button keeps its full 'Go to' label — KB constraint 55's label half; scoped, gate-neutral): SCAFFOLD mean {SK}% / >=50% 1030 / >=75% 196 / >=90% 15 / skipped 0 @ 1954; RAW {RAW}%** (state `outputs/_r328_sk_final.json`, FRESH; 0 pages moved — identical to r326 / r327). Older r327 text: **ROUND 327 BASELINE (a multi-word ALL-CAPS title renders in sentence case — the KB's title-casing rule; scoped, gate-neutral)")
if "ROUND 328 BASELINE" not in m:
    assert m.count(OLD9) == 1, "§9"; m = m.replace(OLD9, NEW9, 1); print("§9")
ROW = ("| `BTNLABEL_OFF` | 328 | **A SUBMISSION BUTTON KEEPS ITS FULL 'GO TO' LABEL** (KB constraint 55's label half + CL-0038 / constraint 65 + 14.11 / 14D; the autonomous loop's session-4 Round 3; **SCOPED regeneration of the 40 affected modules; scoped ship #2 since the r326 full**). Reverts byte-for-byte. ON (default), `buttons.canonical_labels`: at the generic `[button]` seam (`#buttonCanonicalLabel`, key === 'button' only, after the r323 trim and before the r326 anchor) a writer's bare noun becomes the KB's canonical label — `Quiz` / `Quiz button` → `Go to quiz`, `Portfolio` → `Go to portfolio`, `Dropbox` → `Go to dropbox` (`Upload to Dropbox` for the BLL / LS (XLP XDLS XLS LS SLO SL) / HPE (HES PHE PES HPE) prefixes — the rule's `family_labels`); any other label untouched. MEASURED: 94 bare-noun labels on 54 pages / 44 modules (quiz 45, portfolio 25, dropbox 14, journal 10 — journal has no KB rule); the gold in those modules ships `Go to quiz` ×128 / `Go to portfolio` ×77. 47 pages / 40 modules changed; bare-noun labels 84 → 0. Gate-neutral: every gate EXACT, 13 selftests GREEN. |\n")
if "| `BTNLABEL_OFF` | 328 |" not in m:
    A = "| `TITLECASE_OFF` | 327 |"; assert m.count(A) == 1, "§11"; m = m.replace(A, ROW + A, 1); print("§11")
B14 = (f"- **Build:** `260618.99` (round 328 — **a submission button keeps its full 'Go to' label** (KB constraint 55's label half; the autonomous loop's session-4 Round 3; **SCOPED regeneration of 40 modules; scoped ship #2 since the r326 full**). **ROUND 328 BASELINE = r326: SCAFFOLD mean {SK}% / ≥50% 1030 / ≥75% 196 / ≥90% 15 / skipped 0 @ 1954; RAW {RAW}%** (state `outputs/_r328_sk_final.json`, FRESH, 0 pages moved) = **55.1% of achievable** (ceiling 91.6%). Every gate EXACT: cs exact **11360** / EXTRA **186** / missing **591** · clean **2056/2102** / leak **288/46** · body **191** · tags **9557/9557** · flipCard TOTAL 61 divergence 0 · index-sync 33/28 · entry-parity PASS · mtkQuiz shell defect 0 · all THIRTEEN selftests GREEN. Corpus 2102 pages / 413 modules, 0-stale, **47 pages / 40 modules changed, 0 added/removed**; toggle `BTNLABEL_OFF`; data `buttons.canonical_labels`. Bare `Quiz` / `Portfolio` / `Dropbox` labels 84 → 0. **Plateau window: r326 +0.057 · r327 0.000 · r328 0.000.**)\n")
if "- **Build:** `260618.99` (round 328" not in m:
    A = "- **Build:** `260618.98` (round 327 —"; assert m.count(A) == 1, "§14"; m = m.replace(A, B14 + A, 1); print("§14")
wr(CM, m)

# ---------------------------------------------------------------- KB status row 55 (both copies)
for P in (os.path.join(HERE, "..", "..", "KB_AMALGAMATION_STATUS.md"), os.path.join(PF, "loop", "KB_AMALGAMATION_STATUS.md")):
    k = rd(P)
    OLD55 = "| **LIVE — the text defect CLEARED (round 323, 2026-09-15, the loop's session-3 Round 10)**:"
    NEW55 = "| **LIVE — the text defect CLEARED (round 323) and the LABEL half CAPTURED (round 328, 2026-09-15, the loop's session-4 Round 3: `buttons.canonical_labels`, `BTNLABEL_OFF` — a bare `Quiz` / `Portfolio` / `Dropbox` → `Go to quiz` / `Go to portfolio` / `Go to dropbox`, `Upload to Dropbox` in BLL / LS / HPE; 84 bare labels on 47 pages / 40 modules → 0)**:"
    if NEW55 not in k:
        assert k.count(OLD55) == 1, P; k = k.replace(OLD55, NEW55, 1); wr(P, k); print("KB row 55:", os.path.basename(os.path.dirname(P)))

# ---------------------------------------------------------------- gate_baseline.json
GB = os.path.join(HERE, "..", "reference", "tests", "gate_baseline.json"); raw = rd(GB); d = json.loads(raw)
d["_meta"]["build"] = "260618.99"; d["_meta"]["round"] = 328; d["_meta"]["date"] = "2026-09-15"
d["_meta"]["_round328_note"] = "Round 328 (a submission button keeps its full 'Go to' label — KB constraint 55's label half; scoped 40-module regeneration, scoped ship #2 since the r326 full). Gate-neutral: every gate EXACT to round 327, skeleton page-for-page identical."
wr(GB, json.dumps(d, ensure_ascii=False) + ("\n" if raw.endswith("\n") else "")); print("gate_baseline.json refreshed")

# ---------------------------------------------------------------- LOOP_STATE.md
LS = os.path.join(HERE, "..", "..", "LOOP_STATE.md"); s = rd(LS); nl = "\r\n" if "\r\n" in s[:3000] else "\n"
def L(t): return t.replace("\n", nl)
SEC = L(f"""## Session 4 · Round 3 (engine r328) — what shipped (KB constraint 55's label half)
- **Fix:** `buttons.canonical_labels` {{enabled, env BTNLABEL_OFF, rules [quiz → Go to quiz; portfolio → Go to portfolio; dropbox → Go to dropbox,
  family_labels BLL / LS / HPE → Upload to Dropbox]}} — `ContentConverter.#buttonCanonicalLabel` at the generic `[button]` seam, after the r323
  trim and before the r326 anchor. 'Journal' (10) untouched (no KB rule).
- **Regeneration:** scoped — the in-memory ON probe over all 416 named 47 pages / 40 modules; regenerated; 0 truly stale; OFF vs disk = exactly
  the 47 pages; ON = disk 152/152. Bare `Quiz` / `Quiz button` / `Portfolio` / `Dropbox` labels 84 → 0.
- **Gates:** every gate EXACT (fastloop PASS, 10 metrics HELD; full suite identical; skeleton {SK}, 0 moved); 13 selftests GREEN. **55.1% of
  achievable** (unchanged). KB status row 55 → the label half CAPTURED.
- **Plateau window:** r326 +0.057 · r327 0.000 · r328 0.000 — two consecutive sub-threshold rounds; a third stops the loop (§4).

""")
ANCHOR = "## Session 4 · Round 3 PICK (engine r328)"
if "## Session 4 · Round 3 (engine r328) — what shipped" not in s:
    assert s.count(ANCHOR) == 1; s = s.replace(ANCHOR, SEC + ANCHOR, 1); print("LOOP_STATE section")
OLD_P = "- Session 4 Round 2 (engine r327 — a multi-word ALL-CAPS title renders in sentence case, the KB's title-casing rule): SHIPPED 2026-09-15 ≈15:15 (session 4). AppVersion 260618.98, CLAUDE.md §9/§11/§14, KB status row 1 → ALL-CAPS normalisation CAPTURED-LIVE, scoped ship #1 since the r326 full. Gate-neutral."
NEW_P = OLD_P + nl + "- Session 4 Round 3 (engine r328 — a submission button keeps its full 'Go to' label, KB constraint 55's label half): SHIPPED 2026-09-15 ≈15:25 (session 4). AppVersion 260618.99, CLAUDE.md §9/§11/§14, KB status row 55 → the label half CAPTURED, scoped ship #2 since the r326 full. Gate-neutral."
if "- Session 4 Round 3 (engine r328" not in s:
    assert s.count(OLD_P) == 1, "position"; s = s.replace(OLD_P, NEW_P, 1); print("position")
OLD_R = "- s4-r2 (engine r327) · a multi-word ALL-CAPS header title renders in sentence case"
i = s.find(OLD_R); assert i > 0; j = s.find(nl, i) + len(nl)
NEW_R = f"- s4-r3 (engine r328) · a submission button keeps its full 'Go to' label (KB constraint 55's label half: bare `Quiz` / `Portfolio` / `Dropbox` → `Go to quiz` / `Go to portfolio` / `Go to dropbox`, `Upload to Dropbox` in BLL / LS / HPE) · SHIPPED 2026-09-15 · scoped regeneration, 47 pages / 40 modules · gate-neutral, every gate EXACT (scaffold {SK}, 0 moved) · bare-noun labels 84→0 · 55.1% of achievable · commit (see git log)" + nl
if "- s4-r3 (engine r328)" not in s:
    s = s[:j] + NEW_R + s[j:]; print("round log")
wr(LS, s); print("LOOP_STATE.md written")
