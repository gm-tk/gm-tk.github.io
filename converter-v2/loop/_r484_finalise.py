#!/usr/bin/env python3
"""ROUND 484 finalise (session 44 Round 9 — KB c38 for the quiz types, TPLAUTOQUIZ_OFF). WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 484," not in sc[:4000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.47";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 483 BASELINE"; a11 = "| `TPLAUTOCHECK_OFF` | 483 |"; a14 = "- **Build:** `260620.47` (round 483"
for a in (a9, a11, a14): assert so.count(a) == 1, a
PK = os.path.join(ROOT, "KB_AMALGAMATION_STATUS.md"); sk = rd(PK)
k38 = "REMAINING: the quiz types on those templates (7 multiChoiceQuiz, 5 dropQuiz, 1 typing — `_s44_r8_autocheck.py`).** |"; assert sk.count(k38) == 1
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 484 IN FLIGHT — NOT PROVEN**", "- **No round in flight** (25 Sept 2026 ≈02:45, session 44 Round 8", "- LAST SHIPPED: **r483**",
          "- Before it: **r482**", "- Before them: **r481**", "- Plateau window (§4): **0 of 3** — r483", "- Standing facts: AppVersion 260620.47",
          "## Round log", "**Next session starts with:**", "## Session 44 — Round 9 PICK (engine r484)"):
    find(p)
entry = """## 2026-09-25 (round 484, build 260620.48) — KB CONSTRAINT 38 FOR THE QUIZ TYPES: on the 1-3 / 4-6 / ECH templates the built multiChoiceQuiz / dropQuiz (and typing / radioQuiz / wordSelect) carry `autoCheck` too

### 1. WHAT CHANGED

**The find** (r483's remainder, `outputs/_s44_r8_autocheck.py`): on 1-3 / 4-6 pages Claude builds 7 multiChoiceQuiz (1 with autoCheck), 5 dropQuiz (3), 1 typing (1). KB 03A lists MCQ / multiChoiceQuiz / Dropdown Quiz / Radio Quiz / Word Select / typing as autoCheck-capable. Claude's quiz builders emit NO Undo / Check row in either form — their own writer-worded autoCheck form (r287 / r449) is the root class alone (BLL273_2_0 / BLL251_2_0 against their plain siblings) — and KB 03D keeps the typing quiz's buttons.

**The fix:** r483's `skeleton.template_autocheck.widgets` gains multiChoiceQuiz / dropQuiz / typing / radioQuiz / wordSelect with empty `drop_buttons` and a per-widget env; `SkeletonBuilder.#templateAutoCheck` skips `_`-keys and honours the per-widget env. Env **`TPLAUTOQUIZ_OFF`** (byte-identical OFF); `TPLAUTOCHECK_OFF` reverts r483 + r484.

### 2. PROOF AND GATES

- In-memory A/B over all 545 modules: **OFF 3222 / 3222 identical**; ON 7 pages / 7 modules (BLLR201 CEDO202 ENGC101 ENGC206 SSEA203 WJFUN105 WJFUN206): 6 multiChoiceQuiz + 2 dropQuiz gain the class. Regeneration + 12-module spot-check clean; **`scoped_ship.sh` PASS**; skeleton 55.3280 % EXACT (0 movers — skeleton-blind), RAW EXACT; cs / body / clean / leak EXACT; every verifier RESULT line ✓; selftests green; the miner 195 CANDIDATE. Plateau: a KB-rule round, skeleton-blind — neither; **0 of 3**.

**Ledger:** scoped #2 since the r482 FULL · data `skeleton.template_autocheck.widgets` (the quiz rows) · env `TPLAUTOQUIZ_OFF` · code `SkeletonBuilder.#templateAutoCheck` · tools `_s44_r9_pick.py`, `_r484_{regen,postship}.sh`, `_r484_finalise.py` · session 44 Round 9.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 484 (260620.48): KB c38 FOR THE QUIZ TYPES (session 44 Round 9) — the template autoCheck post-pass covers "
                "multiChoiceQuiz / dropQuiz / typing / radioQuiz / wordSelect (the class only). Env TPLAUTOQUIZ_OFF.\n" + '\tstatic AppVersion = "260620.48";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 484 BASELINE (KB c38 for the quiz types, `TPLAUTOQUIZ_OFF`; "
                "SCOPED, scoped #2 since the r482 FULL; scoped_ship PASS): SCAFFOLD mean 55.3280% EXACT / >=50% 1582 / >=75% 275 / >=90% 25 / RAW "
                "39.224% @ 2491 pairs; cs / body / clean / leak EXACT.** Previous: **ROUND 483 BASELINE")
so = so.replace(a11, "| `TPLAUTOQUIZ_OFF` | 484 | **KB c38 FOR THE QUIZ TYPES** (session 44 Round 9). Reverts the quiz rows of "
                "`skeleton.template_autocheck.widgets`: the built multiChoiceQuiz / dropQuiz on 1-3 / 4-6 pages lose the template autoCheck — 7 "
                "modules / 7 pages; byte-identical to r483. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.48` (round 484 — **KB c38 for the quiz types**; `TPLAUTOQUIZ_OFF`; scoped #2 since the r482 FULL; 7 "
                "modules; skeleton EXACT).\n" + a14)
wr(PO, so); print("OG ok")
sk = sk.replace(k38, "**r484 (session 44 Round 9): the quiz types too — multiChoiceQuiz / dropQuiz / typing / radioQuiz / wordSelect take the class "
                "only (`TPLAUTOQUIZ_OFF`; 6 multiChoiceQuiz + 2 dropQuiz on 7 pages).** |")
wr(PK, sk); print("KB status ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r484.bak")
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
setv("build", '"260620.47"', '"260620.48"'); setv("round", "483", "484")
insert_before("_note_r483", '    "_note_r484": "Round 484 (session 44 Round 9, 2026-09-25) — KB c38 FOR THE QUIZ TYPES (TPLAUTOQUIZ_OFF): 7 modules / 7 pages, 6 '
              'multiChoiceQuiz + 2 dropQuiz -> autoCheck; every gate EXACT (skeleton-blind); scoped #2 since the r482 FULL; scoped_ship PASS.",')
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-r484-finalise.bak")
i = find("- **ROUND 484 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (25 Sept 2026 ≈03:00, session 44 Round 9 — r484 (KB c38 for the quiz types) SHIPPED and committed; the in-flight "
        "marker is cleared). LAST SHIPPED **r484** (260620.48); **LAST FULL = r482 (the s44 backstop)**; ledger **scoped #2** (6 of headroom). "
        "Ride-along patches `outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` (buttons, 10 pages) / `_r468_declined.patch` "
        "(the lesson menu's `[H2]` lead, 3 pages).")
k = find("- **No round in flight** (25 Sept 2026 ≈02:45, session 44 Round 8"); prior = L[k]; del L[k]
k = find("- Before it: **r482**"); r482 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r483**"); L[k] = L[k].replace("- LAST SHIPPED: **r483**", "- Before it: **r483**", 1)
L.insert(k, "- LAST SHIPPED: **r484** (build 260620.48, 25 Sept ≈03:00, session 44 Round 9 — KB c38 FOR THE QUIZ TYPES, `TPLAUTOQUIZ_OFF`; SCOPED, "
         "**scoped #2 since the r482 FULL backstop**, scoped_ship PASS; **skeleton 55.3280 % @ 2491 EXACT** (skeleton-blind), ≥50 1582, ≥75 275, "
         "≥90 25, RAW 39.224 %; cs / body / clean / leak EXACT; every verifier ✓; `gate_baseline.json` at r484).")
k = find("- Before them: **r481**")
L[k] = L[k].replace("- Before them: **r481**", "- Before them: **r482** (260620.46, KB 07D the bilingual lesson title h2 — verbatim → "
                    "LOOP_STATE_ARCHIVE.md 'Position — LAST SHIPPED r482 (verbatim, s44 r484)'), **r481**", 1)
k = find("- Plateau window (§4): **0 of 3** — r483")
L[k] = L[k].replace("- Plateau window (§4): **0 of 3** — r483", "- Plateau window (§4): **0 of 3** — r484 a KB-rule round, skeleton-blind "
                    "(neither); r483", 1)
k = find("- Standing facts: AppVersion 260620.47")
L[k] = L[k].replace("- Standing facts: AppVersion 260620.47 (r483", "- Standing facts: AppVersion 260620.48 (r484 KB c38 for the quiz types — "
                    "session 44 Round 9, 25 Sept); before it 260620.47 (r483", 1)
k = find("## Round log")
L.insert(k + 1, "- s44-r9 (engine r484, build 260620.48, 25 Sept 02:45 → ≈03:00) · KB c38 FOR THE QUIZ TYPES (r483's remainder: 6 multiChoiceQuiz + "
         "2 dropQuiz on 1-3 / 4-6 pages take `autoCheck`, the class only — the builders' own autoCheck form) · SHIPPED scoped #2, scoped_ship PASS · "
         "7 modules / 7 pages · every gate EXACT (skeleton-blind) · plateau 0 of 3 (neither).")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r484** (260620.48, "
        "KB c38 for the quiz types); LAST FULL = **r482** (the s44 backstop); ledger scoped #2; plateau **0 of 3**; 2,491 pairs; census 552 / 545 / "
        "2,679. Ride-along patches `_r469_declined.patch` (alerts) / `_r469b_declined.patch` (buttons) / `_r468_declined.patch`. Needs Chris "
        "#17–#19, #22.")
k = find("## Session 44 — Round 9 PICK (engine r484)")
j = k + 1
while j < len(L) and not L[j].startswith("## "): j += 1
pick = L[k:j]; del L[k:j]
L.insert(k, "## Session 44 — Round 9 PICK (engine r484) — KB c38 FOR THE QUIZ TYPES — SHIPPED; the PICK + what-shipped record is in "
         "LOOP_STATE_ARCHIVE.md 'Session 44 — Round 9 PICK (engine r484) + what shipped'; the one-line summary is the s44-r9 Round-log line below.\n")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r482 (verbatim, s44 r484)\n\n" + r482 + "\n"
    "\n## Session 44 — Round 9 PICK (engine r484) + what shipped\n\n" + marker + "\n" + prior + "\n" + "\n".join(pick[1:]).rstrip() + "\n"
    "- **What shipped (r484, 260620.48):** the quiz rows of `skeleton.template_autocheck.widgets` (env `TPLAUTOQUIZ_OFF`); the post-pass skips "
    "`_`-keys and honours a per-widget env. Probe OFF 3222 identical; ON 7 pages / 7 modules; scoped_ship PASS; every gate EXACT.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
