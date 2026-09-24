#!/usr/bin/env python3
"""ROUND 483 finalise (session 44 Round 8 — KB c38: autoCheck on the 1-3 / 4-6 / ECH templates, TPLAUTOCHECK_OFF). WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 483," not in sc[:4000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.46";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 482 BASELINE"; a11 = "| `LESSONPIN_OFF` | 482 |"; a14 = "- **FULL backstop** at `260620.46`"
for a in (a9, a11, a14): assert so.count(a) == 1, a
PK = os.path.join(ROOT, "KB_AMALGAMATION_STATUS.md"); sk = rd(PK)
k38 = "| 38 | `autoCheck` auto-applied on ECH / 1-3 / 4-6 templates | pre-ledger | 1-3 + 4-6 modules (880 Claude pages) | **UNVERIFIED** — check the built widgets' `autoCheck` attribute by template | builders |"
assert sk.count(k38) == 1
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 483 IN FLIGHT — NOT PROVEN**", "- **No round in flight** (25 Sept 2026 ≈02:10, session 44 Round 6", "- LAST SHIPPED: **r482**",
          "- Before it: **r481**", "- Before them: **r480**", "- Plateau window (§4): **0 of 3** — r482", "- Standing facts: AppVersion 260620.46",
          "## Round log", "**Next session starts with:**", "## Session 44 — Round 8 PICK (engine r483)"):
    find(p)
entry = """## 2026-09-25 (round 483, build 260620.47) — KB CONSTRAINT 38: AUTOCHECK ON THE 1-3 / 4-6 / ECH TEMPLATES — every built drag-and-drop on those pages carries `autoCheck` with only its Reset button (KB 03B)

### 1. WHAT CHANGED

**The find** (session 44 Round 8 — the KB queue's UNVERIFIED rows re-read; `outputs/_s44_r8_autocheck.py`, by each page's `<html template>`): KB constraint 38 / 03A "autoCheck Auto-Application" — on the three dedicated templates (ECH / 1-3 / 4-6) `autoCheck` MUST be applied to every interactive that supports it, the Undo / Check buttons dropped exactly as the component's "With autoCheck" example shows. Claude built 51 dragAndDrops on 1-3 / 4-6 pages (38 modules: standard 24, images 13, column 14) and **none** carried it (the builders derive `autoCheck` only from the writer's own wording). The gold on 1-3: dragAndDrop 348 / 793, multiChoiceQuiz 237 / 310, dropQuiz 42 / 65, radioQuiz 46 / 59 — far above its 7-8 / 9-10 / NCEA rates (its pre-rule builds keep the rest).

**The fix** (KB 03B: `<div class="dragAndDrop autoCheck …">` + the button row reduced to Reset; the free-form area layout never takes it): `SkeletonBuilder.BuildPage` — once the page's template attribute / level is resolved (the widget builders run before the skeleton knows it) — runs `#templateAutoCheck` over the body: every listed widget root without `autoCheck` (not in `skip_layouts`) gains the class and loses its own `drop_buttons`. Data `Emit_Templates.skeleton.template_autocheck` {enabled, env, templates [1-3, 4-6], levels [ech], widgets.dragAndDrop {skip_layouts [area], drop_buttons [undo, checkAnswer]}}; env **`TPLAUTOCHECK_OFF`**, byte-identical OFF. **The gate tool:** `reference/tests/_verify_dragdrop.cjs` learns KB 03B's autoCheck form (`btnOk` — an autoCheck widget keeps ONLY Reset; every other widget the reset / undo hidden / checkAnswer hidden row). The quiz types on those templates (7 multiChoiceQuiz, 5 dropQuiz, 1 typing — 12 widgets) are recorded for a later round.

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 3222 / 3222 identical**; ON 43 pages / 38 modules (`outputs/_affected_r483.txt`); every one of the 51 widgets `dragAndDrop autoCheck`, no Undo / Check button left.
- Regeneration of the 38 + the 12-module spot-check (`_r483_regen.sh`): 0 truly stale, 12 / 12 byte-identical; **`scoped_ship.sh` PASS**.

### 3. PROTECTED GATES

- Skeleton **55.3280 % @ 2491 — EXACT** (0 movers; skeleton-blind by design — the root class and its button row sit inside the collapsed WIDGET line); RAW 39.237 → 39.224 % (−0.013pp — the unprotected full-content score sees the two dropped buttons per widget; the gold keeps them on its pre-rule D&Ds); compare_structure / body / clean / leak EXACT.
- **The dragAndDrop verifier over the whole family: "every built dragAndDrop is the KB 03B form ✓"**; its selftest GREEN (LIVENESS + DETECTION); every other verifier RESULT line ✓; 17 selftests + the skeleton selftest green; the miner 195 CANDIDATE.
- Plateau (§4): a KB-rule round, skeleton-blind by design; neither counts nor resets: **0 of 3**.

**Ledger:** scoped #1 since the r482 FULL backstop · data `skeleton.template_autocheck` · env `TPLAUTOCHECK_OFF` · code `SkeletonBuilder.BuildPage` / `#templateAutoCheck` · gate tool `_verify_dragdrop.cjs` (btnOk) · tools `_s44_r8_{autocheck,pick}.py`, `_r483_{regen,postship}.sh`, `_r483_finalise.py` · session 44 Round 8.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 483 (260620.47): KB c38 AUTOCHECK ON THE 1-3 / 4-6 / ECH TEMPLATES (session 44 Round 8) — SkeletonBuilder's "
                "#templateAutoCheck gives every built dragAndDrop on those pages autoCheck + only the Reset button. Env TPLAUTOCHECK_OFF.\n"
                + '\tstatic AppVersion = "260620.47";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 483 BASELINE (KB c38 autoCheck on the 1-3 / 4-6 / ECH templates, "
                "`TPLAUTOCHECK_OFF`; SCOPED, scoped #1 since the r482 FULL backstop; scoped_ship PASS): SCAFFOLD mean 55.3280% EXACT (skeleton-blind) / "
                ">=50% 1582 / >=75% 275 / >=90% 25 / RAW 39.224% @ 2491 pairs; cs / body / clean / leak EXACT; dragAndDrop verifier ✓ (taught the "
                "03B autoCheck form).** Previous: **ROUND 482 BASELINE")
so = so.replace(a11, "| `TPLAUTOCHECK_OFF` | 483 | **KB c38 AUTOCHECK ON THE 1-3 / 4-6 / ECH TEMPLATES** (session 44 Round 8). Reverts "
                "`skeleton.template_autocheck`: the built dragAndDrops on those pages lose `autoCheck` and get their Undo / Check buttons back — "
                "38 modules / 43 pages; byte-identical to r482. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.47` (round 483 — **KB c38: autoCheck on the 1-3 / 4-6 / ECH templates** (the dragAndDrop); "
                "`TPLAUTOCHECK_OFF`; scoped #1 since the r482 FULL; 38 modules; skeleton EXACT 55.3280 %).\n" + a14)
wr(PO, so); print("OG ok")
sk = sk.replace(k38, "| 38 | `autoCheck` auto-applied on ECH / 1-3 / 4-6 templates | pre-ledger | 1-3 + 4-6 modules (880 Claude pages) | **CAPTURED-LIVE for "
                "the dragAndDrop — round 483 (2026-09-25, session 44 Round 8): `skeleton.template_autocheck`, `TPLAUTOCHECK_OFF`; 51 built D&Ds on "
                "1-3 / 4-6 pages / 38 modules → `autoCheck` + Reset only (KB 03B); the D&D verifier taught the form. REMAINING: the quiz types on "
                "those templates (7 multiChoiceQuiz, 5 dropQuiz, 1 typing — `_s44_r8_autocheck.py`).** | `SkeletonBuilder.#templateAutoCheck` |")
wr(PK, sk); print("KB status ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r483.bak")
G = rd(P).split("\n")
def setv(key, old, new):
    for i, l in enumerate(G):
        if l.strip().startswith(f'"{key}": '):
            assert l.strip().rstrip(",") == f'"{key}": {old}', (key, l)
            G[i] = l.replace(f'"{key}": {old}', f'"{key}": {new}'); return i
    raise SystemExit(f"not found {key}")
def insert_before(key, line):
    for i, l in enumerate(G):
        if l.strip().startswith(f'"{key}": '): G.insert(i, line); return
    raise SystemExit(f"anchor {key}")
setv("build", '"260620.46"', '"260620.47"'); setv("round", "482", "483")
insert_before("_note_s44_full", '    "_note_r483": "Round 483 (session 44 Round 8, 2026-09-25) — KB c38 AUTOCHECK ON THE 1-3 / 4-6 / ECH TEMPLATES (TPLAUTOCHECK_OFF): '
              '38 modules / 43 pages, 51 dragAndDrops -> autoCheck + Reset only; SCAFFOLD 55.3280 EXACT (skeleton-blind); RAW 39.237 -> 39.224 (the '
              'dropped buttons); cs / body / clean / leak EXACT; the dragAndDrop verifier taught the 03B autoCheck form; scoped #1 since the r482 FULL.",')
setv("raw_mean_pct", "39.24", "39.22")
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-r483-finalise.bak")
i = find("- **ROUND 483 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (25 Sept 2026 ≈02:45, session 44 Round 8 — r483 (KB c38, autoCheck on the 1-3 / 4-6 / ECH templates) SHIPPED "
        "and committed; the in-flight marker is cleared). LAST SHIPPED **r483** (260620.47); **LAST FULL = r482 (the s44 backstop)**; ledger "
        "**scoped #1** (7 of headroom). Ride-along patches `outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` (buttons, "
        "10 pages) / `_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages).")
k = find("- **No round in flight** (25 Sept 2026 ≈02:10, session 44 Round 6"); prior = L[k]; del L[k]
k = find("- Before it: **r481**"); r481 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r482**"); L[k] = L[k].replace("- LAST SHIPPED: **r482**", "- Before it: **r482**", 1)
L.insert(k, "- LAST SHIPPED: **r483** (build 260620.47, 25 Sept ≈02:45, session 44 Round 8 — KB c38 AUTOCHECK ON THE 1-3 / 4-6 / ECH TEMPLATES "
         "(the dragAndDrop), `TPLAUTOCHECK_OFF`; SCOPED, **scoped #1 since the r482 FULL backstop**, scoped_ship PASS; **skeleton 55.3280 % @ 2491 "
         "EXACT** (skeleton-blind), ≥50 1582, ≥75 275, ≥90 25, RAW 39.224 %; cs / body / clean / leak EXACT; the dragAndDrop verifier ✓ (taught "
         "the 03B autoCheck form); `gate_baseline.json` at r483).")
k = find("- Before them: **r480**")
L[k] = L[k].replace("- Before them: **r480**", "- Before them: **r481** (260620.45, the MTK data-row hand-off — verbatim → "
                    "LOOP_STATE_ARCHIVE.md 'Position — LAST SHIPPED r481 (verbatim, s44 r483)'), **r480**", 1)
k = find("- Plateau window (§4): **0 of 3** — r482")
L[k] = L[k].replace("- Plateau window (§4): **0 of 3** — r482", "- Plateau window (§4): **0 of 3** — r483 a KB-rule round, skeleton-blind "
                    "(neither); r482", 1)
k = find("- Standing facts: AppVersion 260620.46")
L[k] = L[k].replace("- Standing facts: AppVersion 260620.46 (r482", "- Standing facts: AppVersion 260620.47 (r483 KB c38 template autoCheck — "
                    "session 44 Round 8, 25 Sept); before it 260620.46 (r482", 1)
k = find("## Round log")
L.insert(k + 1, "- s44-r8 (engine r483, build 260620.47, 25 Sept 02:25 → ≈02:45) · KB c38 AUTOCHECK ON THE 1-3 / 4-6 / ECH TEMPLATES (the KB queue's "
         "UNVERIFIED rows re-read; 51 built D&Ds, 0 had it) — `autoCheck` + Reset only per KB 03B; the D&D verifier taught the form · SHIPPED scoped "
         "#1 since the r482 FULL, scoped_ship PASS · 38 modules / 43 pages · skeleton EXACT (skeleton-blind) · plateau 0 of 3 (neither).")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r483** (260620.47, "
        "KB c38 template autoCheck); LAST FULL = **r482** (the s44 backstop); ledger scoped #1; plateau **0 of 3**; 2,491 pairs; census 552 / 545 / "
        "2,679. Ride-along patches `_r469_declined.patch` (alerts) / `_r469b_declined.patch` (buttons) / `_r468_declined.patch`. Needs Chris "
        "#17–#19, #22.")
k = find("## Session 44 — Round 8 PICK (engine r483)")
j = k + 1
while j < len(L) and not L[j].startswith("## "): j += 1
pick = L[k:j]; del L[k:j]
L.insert(k, "## Session 44 — Round 8 PICK (engine r483) — KB c38 AUTOCHECK ON THE 1-3 / 4-6 / ECH TEMPLATES — SHIPPED; the PICK + what-shipped record "
         "is in LOOP_STATE_ARCHIVE.md 'Session 44 — Round 8 PICK (engine r483) + what shipped'; the one-line summary is the s44-r8 Round-log line below.\n")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r481 (verbatim, s44 r483)\n\n" + r481 + "\n"
    "\n## Session 44 — Round 8 PICK (engine r483) + what shipped\n\n" + marker + "\n" + prior + "\n" + "\n".join(pick[1:]).rstrip() + "\n"
    "- **What shipped (r483, 260620.47):** `skeleton.template_autocheck` (env `TPLAUTOCHECK_OFF`) — SkeletonBuilder.#templateAutoCheck over the "
    "body once the template is resolved; the D&D verifier's btnOk. Probe OFF 3222 identical; ON 43 pages / 38 modules; scoped_ship PASS; "
    "skeleton EXACT; RAW −0.013pp named; verifier ✓.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
