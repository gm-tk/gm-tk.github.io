#!/usr/bin/env python3
"""ROUND 482 finalise (session 44 Round 6 — KB 07D: the bilingual lesson title keeps its h2, LESSONPIN_OFF). WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 482," not in sc[:3000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.45";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 481 BASELINE"; a11 = "| `ACTDATA_OFF` | 481 |"; a14 = "- **Build:** `260620.45` (round 481"
for a in (a9, a11, a14): assert so.count(a) == 1, a
PK = os.path.join(ROOT, "KB_AMALGAMATION_STATUS.md"); sk = rd(PK); KL = sk.split("\n")
kd = [i for i, l in enumerate(KL) if l.startswith('| ~~—~~ | 07B MTK "Activity Structure" — the `Activity NX')]; assert len(kd) == 1
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 482 IN FLIGHT — NOT PROVEN**", "- **No round in flight** (25 Sept 2026 ≈01:35, session 44 Round 4", "- LAST SHIPPED: **r481**",
          "- Before it: **r480**", "- Before them: **r479**", "- Plateau window (§4): **0 of 3** — r481", "- Standing facts: AppVersion 260620.45",
          "## Round log", "**Next session starts with:**", "## Session 44 — Round 6 PICK (engine r482)"):
    find(p)
entry = """## 2026-09-25 (round 482, build 260620.46) — KB 07D: THE BILINGUAL LESSON TITLE KEEPS ITS h2 — the `[H2] Lesson N / Hei Mahi N` title the page's re-level pass demoted to h3 is pinned at the level r137 forces

### 1. WHAT CHANGED

**The find** (session 44 Round 6 — the Bilingual low-module scan, `outputs/_s44_famdiff.py` over TRR304 / TRR301 / TRR115 / TRR107 / TRR203 / PMT101: `body SUBSTITUTED h2 → h3 «Hei Mahi N»`): the gold ships the bilingual lesson title (`Hei Mahi N` / `Ngohe N` + `Lesson N`) at **h2 on 22 / 22** (16 pages / 7 modules); Claude shipped **h3 on 30 / 30** (14 pages). `BilingualBuilder.bilingualLessonTitleHtml` FORCES `section_grouping.lesson_heading.title_level` (2) on the title (r137), but `ContentConverter.#relevelHeadings` (the page's rank normalisation, base h3) still took it as the page's shallowest free heading and mapped it to h3.

**The fix** (KB 07D's MTK lesson skeleton `<h2 reo>{MAORI_LESSON_HEADING}</h2>`; the gold 22 / 22): the title's heading tags carry the transient r371 writer-digit marker `data-wd="<title_level>"`; the re-level pass pins a marked heading at its digit, still counts it in the rank pool (the page's other headings keep their levels) and strips the marker. Data `section_grouping.lesson_heading.pin_title` {enabled, env}; env **`LESSONPIN_OFF`**, byte-identical OFF.

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 3222 / 3222 identical**; ON 18 pages / 7 modules (TRR107 TRR108 TRR114 TRR115 TRR203 TRR301 TRR304 — `outputs/_affected_r482.txt`); no `data-wd` marker in any output.
- Regeneration of the 7 + the 12-module spot-check (`_r482_regen.sh`): 0 truly stale, 12 / 12 byte-identical; **`scoped_ship.sh` PASS**.

### 3. PROTECTED GATES

- Skeleton **55.3255 % → 55.3280 % @ 2491 (+0.0024pp)**, RAW 39.236 → 39.237 %; ≥50 1582; ≥75 275; ≥90 25; 11 movers (9 up / 2 down, pp-sum +6.1): TRR108_1_0 +3.4, TRR114_2_0 +2.0 …; NAMED: TRR114_3_0 23.3 → 18.9 (the writer repeats the `[H2] Ngohe 3` opener before each activity — three title rows where the gold has one; the two repeats now ship at h2 where the gold's h3 section headings sit), TRR304_1_0 −0.4.
- compare_structure / body / clean / leak EXACT; every verifier RESULT line ✓; selftests green; the feature index green; the miner 195 CANDIDATE.
- Plateau (§4): a KB-rule round; neither counts nor resets: **0 of 3**.

**Ledger:** scoped #8 since the r474 FULL — **the FULL backstop is due (cadence 8)** · data `section_grouping.lesson_heading.pin_title` · env `LESSONPIN_OFF` · code `BilingualBuilder.bilingualLessonTitleHtml` · tools `_s44_r6_pick.py`, `_r482_{regen,postship}.sh`, `_r482_finalise.py` · session 44 Round 6.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 482 (260620.46): KB 07D THE BILINGUAL LESSON TITLE KEEPS ITS h2 (session 44 Round 6) — the r371 writer-digit marker "
                "pins the r137 title level through the re-level pass. Env LESSONPIN_OFF.\n" + '\tstatic AppVersion = "260620.46";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 482 BASELINE (KB 07D the bilingual lesson title keeps its h2, "
                "`LESSONPIN_OFF`; SCOPED, scoped #8 since the r474 FULL; scoped_ship PASS): SCAFFOLD mean 55.3280% / >=50% 1582 / >=75% 275 / >=90% 25 / "
                "RAW 39.237% @ 2491 pairs — +0.0024pp (9 up / 2 down); cs / body / clean / leak EXACT.** Previous: **ROUND 481 BASELINE")
so = so.replace(a11, "| `LESSONPIN_OFF` | 482 | **KB 07D THE BILINGUAL LESSON TITLE KEEPS ITS h2** (session 44 Round 6). Reverts "
                "`section_grouping.lesson_heading.pin_title`: the page's re-level pass demotes the `[H2] Lesson N / Hei Mahi N` title to h3 again — "
                "7 modules / 18 pages; byte-identical to r481. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.46` (round 482 — **KB 07D: the bilingual lesson title keeps its h2**; `LESSONPIN_OFF`; scoped #8 since the "
                "r474 FULL; 7 modules; skeleton 55.3280 % @ 2491, +0.0024pp).\n" + a14)
wr(PO, so); print("OG ok")
KL.insert(kd[0] + 1, "| ~~—~~ | 07D MTK lesson skeleton — the `[H2] Lesson N / Hei Mahi N` lesson title is `<h2 reo>` / `<h2 eng>` in its own "
          "`row > col-md-8` | **SHIPPED round 482 (2026-09-25, session 44 Round 6)** — the r137 title_level (2) pinned through the page's re-level "
          "pass (`lesson_heading.pin_title`, `LESSONPIN_OFF`); gold 22 / 22 h2, Claude 30 h3 → h2; 7 modules / 18 pages; +0.0024pp. |")
wr(PK, "\n".join(KL)); print("KB status ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r482.bak")
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
setv("build", '"260620.45"', '"260620.46"'); setv("round", "481", "482")
insert_before("_note_r481", '    "_note_r482": "Round 482 (session 44 Round 6, 2026-09-25) — KB 07D THE BILINGUAL LESSON TITLE KEEPS ITS h2 (LESSONPIN_OFF): 7 '
              'modules / 18 pages; SCAFFOLD 55.3255 -> 55.3280 @ 2491 (+0.0024pp, 9 up / 2 down); RAW 39.236 -> 39.237; cs / body / clean / leak '
              'EXACT; scoped #8 since the r474 FULL (the FULL backstop due); scoped_ship PASS.",')
insert_before("_note_r481_state", '    "_note_r482_state": "r482 (the bilingual lesson title h2): SCAFFOLD 55.3280 @ 2491, RAW 39.237; 11 movers (9 up / 2 down).",')
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-r482-finalise.bak")
i = find("- **ROUND 482 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (25 Sept 2026 ≈02:10, session 44 Round 6 — r482 (KB 07D, the bilingual lesson title keeps its h2) SHIPPED and "
        "committed; the in-flight marker is cleared). LAST SHIPPED **r482** (260620.46); **LAST FULL = r474**; ledger **scoped #8 — the FULL backstop "
        "is DUE**. Ride-along patches `outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` (buttons, 10 pages) / "
        "`_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages).")
k = find("- **No round in flight** (25 Sept 2026 ≈01:35, session 44 Round 4"); prior = L[k]; del L[k]
k = find("- Before it: **r480**"); r480 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r481**"); L[k] = L[k].replace("- LAST SHIPPED: **r481**", "- Before it: **r481**", 1)
L.insert(k, "- LAST SHIPPED: **r482** (build 260620.46, 25 Sept ≈02:10, session 44 Round 6 — KB 07D THE BILINGUAL LESSON TITLE KEEPS ITS h2, "
         "`LESSONPIN_OFF`; SCOPED, **scoped #8 since the r474 FULL**, scoped_ship PASS; **skeleton 55.3255 → 55.3280 % @ 2491 (+0.0024pp, 9 up / 2 "
         "down)**, ≥50 1582, ≥75 275, ≥90 25, RAW 39.237 %; cs exact 16691 / EXTRA 208 / missing 872; body / clean / leak EXACT; "
         "`gate_baseline.json` at r482; the miner 195 CANDIDATE).")
k = find("- Before them: **r479**")
L[k] = L[k].replace("- Before them: **r479**", "- Before them: **r480** (260620.44, KB 07B the MTK one-box activity — verbatim → "
                    "LOOP_STATE_ARCHIVE.md 'Position — LAST SHIPPED r480 (verbatim, s44 r482)'), **r479**", 1)
k = find("- Plateau window (§4): **0 of 3** — r481")
L[k] = L[k].replace("- Plateau window (§4): **0 of 3** — r481", "- Plateau window (§4): **0 of 3** — r482 a KB-rule round (+0.0024pp; neither); r481", 1)
k = find("- Standing facts: AppVersion 260620.45")
L[k] = L[k].replace("- Standing facts: AppVersion 260620.45 (r481", "- Standing facts: AppVersion 260620.46 (r482 KB 07D the bilingual lesson "
                    "title h2 — session 44 Round 6, 25 Sept); before it 260620.45 (r481", 1)
k = find("## Round log")
L.insert(k + 1, "- s44-r6 (engine r482, build 260620.46, 25 Sept 01:55 → ≈02:10) · KB 07D THE BILINGUAL LESSON TITLE KEEPS ITS h2 (the r137 forced level "
         "pinned through the re-level pass; gold 22 / 22 h2, Claude 30 h3) · SHIPPED scoped #8, scoped_ship PASS · 7 modules / 18 pages · skeleton "
         "+0.0024pp (9 up / 2 down) · plateau 0 of 3 (neither).")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r482** (260620.46, "
        "KB 07D the bilingual lesson title h2); LAST FULL = **r474**; ledger scoped #8 (**the FULL backstop is DUE**); plateau **0 of 3**; 2,491 "
        "pairs; census 552 / 545 / 2,679. Ride-along patches `_r469_declined.patch` (alerts) / `_r469b_declined.patch` (buttons) / "
        "`_r468_declined.patch`. Needs Chris #17–#19, #22.")
k = find("## Session 44 — Round 6 PICK (engine r482)")
j = k + 1
while j < len(L) and not L[j].startswith("## "): j += 1
pick = L[k:j]; del L[k:j]
L.insert(k, "## Session 44 — Round 6 PICK (engine r482) — KB 07D THE BILINGUAL LESSON TITLE KEEPS ITS h2 — SHIPPED; the PICK + what-shipped record "
         "is in LOOP_STATE_ARCHIVE.md 'Session 44 — Round 6 PICK (engine r482) + what shipped'; the one-line summary is the s44-r6 Round-log line below.\n")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r480 (verbatim, s44 r482)\n\n" + r480 + "\n"
    "\n## Session 44 — Round 6 PICK (engine r482) + what shipped\n\n" + marker + "\n" + prior + "\n" + "\n".join(pick[1:]).rstrip() + "\n"
    "- **What shipped (r482, 260620.46):** `section_grouping.lesson_heading.pin_title` (env `LESSONPIN_OFF`) — bilingualLessonTitleHtml marks the "
    "title's heading tags data-wd=<title_level>; #relevelHeadings pins and strips. Probe OFF 3222 identical; ON 18 pages / 7 modules; scoped_ship "
    "PASS; +0.0024pp (9 up / 2 down; TRR114_3_0 −4.4 named — the writer's repeated opener).\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
