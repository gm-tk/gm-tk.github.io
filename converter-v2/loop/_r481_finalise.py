#!/usr/bin/env python3
"""ROUND 481 finalise (session 44 Round 4 — the MTK activity's data rows are one hand-off, ACTDATA_OFF) — BUILD_CHANGELOG.md (prepend),
Config.js AppVersion 260620.44 -> 260620.45, OPERATING_GUIDE §9 / §11 / §14, gate_baseline.json, KB status (the r480 07B row extended),
LOOP_STATE.md (marker cleared, Position, plateau, round log, next-session line, Follow-up; the PICK → archive). WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 481," not in sc[:3000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.44";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 480 BASELINE"; a11 = "| `ACTLABELBOX_OFF` | 480 |"; a14 = "- **Build:** `260620.44` (round 480"
for a in (a9, a11, a14): assert so.count(a) == 1, a
PK = os.path.join(ROOT, "KB_AMALGAMATION_STATUS.md"); sk = rd(PK)
k80 = "3 modules / 14 pages; +0.0611pp, ≥50 +4. |"; assert sk.count(k80) == 1
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 481 IN FLIGHT — NOT PROVEN**", "- **No round in flight** (25 Sept 2026 ≈01:20, session 44 Round 3", "- LAST SHIPPED: **r480**",
          "- Before it: **r479**", "- Before them: **r478**", "- Plateau window (§4): **0 of 3 — RESET by r480**", "- Standing facts: AppVersion 260620.44",
          "## Round log", "**Next session starts with:**", "## Session 44 — Round 4 PICK (engine r481)", "- **(s44-r2) THE TRR1 LESSON-PAGE LANE"):
    find(p)

entry = """## 2026-09-25 (round 481, build 260620.45) — THE MTK ACTIVITY'S DATA ROWS ARE ONE HAND-OFF: inside the r480 box, the `[Activity: Embedded]` table's data grid ships whole in one `cv2-interactive` hand-off instead of loose paragraphs that kept only its first two columns

### 1. WHAT CHANGED

**The find** (session 44 Round 3's census, `outputs/_s44_r3_embrows.cjs` / `_s44_r3_actprobe.cjs`): the `[Activity: Embedded]` table's rows after its marker / `[H#]` / `[Body]` rows are the widget's DATA — the nested `Sentence ║ Word choice ║ Picture ║ AudioImage` grids, flip-card `Side 1 Text ║ Side 1 [AudioHover] ║ Side 2` tables, word lists, `Note to CS` lines (3- to 6-column rows). `BilingualBuilder.bilingualActivity` unfolded each row as `p reo` / `p eng` from the FIRST TWO cells only — every third+ cell (the picture, the audio item, the answer) was LOST from the page and the gold's one WIDGET line met a run of Claude paragraphs.

**The fix** (built inert in r480, switched on here): `act_label_box.data_rows_handoff` true — `#markerDataFrom` finds the first data row; from there the whole grid ships as ONE `<div class="cv2-interactive bilingual-unbuilt">` + `TablesAndGrids.contentTable` (every column kept) inside the box — the r451 hand-off form for an un-built widget's data. Own env **`ACTDATA_OFF`** (data `data_env`), byte-identical OFF = the r480 output; `ACTLABELBOX_OFF` reverts both.

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 3222 / 3222 identical**; ON 9 pages / 1 module (TRR116 — the only r480 module whose marker tables carry data rows inside them); pre-scored +41.7 pp-sum (`_r481_prescore.log`).
- Regeneration of TRR116 + the 12-module spot-check (`_r481_regen.sh`): 0 truly stale, 12 / 12 byte-identical; **`scoped_ship.sh` PASS** — every protected gate held or improved.

### 3. PROTECTED GATES

- Skeleton **55.3088 % → 55.3255 % @ 2491 (+0.0167pp)**, RAW 39.240 → 39.236 %; **≥50 1580 → 1582 (+2)**; ≥75 275; ≥90 25; 9 movers (7 up / 2 down, pp-sum +41.7): TRR116_8_0 +13.3, TRR116_4_0 +10.6, TRR116_6_0 +9.0 (crosses 50), TRR116_9_0 +5.0, TRR116_3_0 +4.9, TRR116_5_0 +3.4, TRR116_7_0 +2.8 (crosses 50); down TRR116_1_0 58.3 → 51.6 (its flip-card / map grids the gold partly shows as visible `audioImage` / `sassoonI-text` lines beside its widgets, which the loose paragraphs happened to align with) and TRR116_2_0 −0.6.
- compare_structure exact 16691 / EXTRA 208 / missing 872 — EXACT (the rows sat inside `div.activity` before and after, excluded either way); body ANY 238; clean 2587 / 2633; leak 75 / 46 — EXACT; every verifier RESULT line ✓; selftests green; the feature index green; the miner 195 CANDIDATE.
- Plateau (§4): +0.0167pp (< 0.02) but ≥50 +2 — a protected bucket moved: neither counts nor resets; **0 of 3** stands.

**Ledger:** scoped #7 since the r474 FULL (1 of headroom — the FULL backstop is due at the next ship) · data `elements.dual_language.act_label_box.data_rows_handoff` / `data_env` · env `ACTDATA_OFF` · code `BilingualBuilder.actLabelBoxCfg` / `bilingualActivity` / `#markerDataFrom` · tools `_s44_r4_pick.py`, `_r481_{regen,postship}.sh`, `_r481_finalise.py` · session 44 Round 4.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 481 (260620.45): THE MTK ACTIVITY'S DATA ROWS ARE ONE HAND-OFF (session 44 Round 4) — inside the r480 box the "
                "[Activity: Embedded] table's data grid ships whole in one cv2-interactive hand-off (every column kept). Env ACTDATA_OFF.\n"
                '\tstatic AppVersion = "260620.45";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 481 BASELINE (the MTK activity's data rows are one "
                "hand-off, `ACTDATA_OFF`; SCOPED, scoped #7 since the r474 FULL; scoped_ship PASS): SCAFFOLD mean 55.3255% / >=50% 1582 / >=75% 275 "
                "/ >=90% 25 / RAW 39.236% @ 2491 pairs — +0.0167pp (7 up / 2 down, ≥50 +2); cs / body / clean / leak EXACT.** Previous: **ROUND 480 BASELINE")
so = so.replace(a11, "| `ACTDATA_OFF` | 481 | **THE MTK ACTIVITY'S DATA ROWS ARE ONE HAND-OFF** (session 44 Round 4). Reverts "
                "`act_label_box.data_rows_handoff`: inside the r480 box the `[Activity: Embedded]` table's data rows unfold as loose paragraphs "
                "again (first two cells only) — TRR116, 9 pages; byte-identical to r480. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.45` (round 481 — **the MTK activity's data rows are one hand-off**; `ACTDATA_OFF`; scoped #7 since the "
                "r474 FULL; TRR116; skeleton 55.3255 % @ 2491, +0.0167pp, ≥50 +2).\n" + a14)
wr(PO, so); print("OG ok")
sk = sk.replace(k80, "3 modules / 14 pages; +0.0611pp, ≥50 +4. **r481 (session 44 Round 4): the `[Activity: Embedded]` table's data rows inside the "
                "box ship as ONE hand-off, every column kept (`data_rows_handoff`, `ACTDATA_OFF`; TRR116; +0.0167pp).** |")
wr(PK, sk); print("KB status ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r481.bak")
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
setv("build", '"260620.44"', '"260620.45"'); setv("round", "480", "481")
insert_before("_note_r480", '    "_note_r481": "Round 481 (session 44 Round 4, 2026-09-25) — THE MTK ACTIVITY\'S DATA ROWS ARE ONE HAND-OFF (ACTDATA_OFF): TRR116, '
              '9 pages; SCAFFOLD 55.3088 -> 55.3255 @ 2491 (+0.0167pp, 7 up / 2 down, pp-sum +41.7); RAW 39.240 -> 39.236; >=50 1580 -> 1582; cs / '
              'body / clean / leak EXACT; scoped #7 since the r474 FULL; scoped_ship PASS.",')
setv("mean_scaffold_pct", "55.31", "55.33"); setv("pages_ge_50", "1580", "1582")
insert_before("_note_r480_state", '    "_note_r481_state": "r481 (the MTK data-row hand-off): SCAFFOLD 55.3255 @ 2491, RAW 39.236; 9 movers (7 up / 2 down).",')
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-r481-finalise.bak")
i = find("- **ROUND 481 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (25 Sept 2026 ≈01:35, session 44 Round 4 — r481 (the MTK activity's data rows are one hand-off) SHIPPED and "
        "committed; the in-flight marker is cleared). LAST SHIPPED **r481** (260620.45); **LAST FULL = r474**; ledger **scoped #7** (1 of headroom — "
        "the next ship takes the FULL backstop). Ride-along patches `outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` "
        "(buttons, 10 pages) / `_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages).")
k = find("- **No round in flight** (25 Sept 2026 ≈01:20, session 44 Round 3"); prior = L[k]; del L[k]
k = find("- Before it: **r479**"); r479 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r480**"); L[k] = L[k].replace("- LAST SHIPPED: **r480**", "- Before it: **r480**", 1)
L.insert(k, "- LAST SHIPPED: **r481** (build 260620.45, 25 Sept ≈01:35, session 44 Round 4 — THE MTK ACTIVITY'S DATA ROWS ARE ONE HAND-OFF, "
         "`ACTDATA_OFF`; SCOPED, **scoped #7 since the r474 FULL**, scoped_ship PASS; **skeleton 55.3088 → 55.3255 % @ 2491 (+0.0167pp, 7 up / 2 "
         "down)**, **≥50 1582 (+2)**, ≥75 275, ≥90 25, RAW 39.236 %; cs exact 16691 / EXTRA 208 / missing 872; body / clean / leak EXACT; "
         "`gate_baseline.json` at r481; the miner 195 CANDIDATE).")
k = find("- Before them: **r478**")
L[k] = L[k].replace("- Before them: **r478**", "- Before them: **r479** (260620.43, KB 07B the bilingual whakatauki box — verbatim → "
                    "LOOP_STATE_ARCHIVE.md 'Position — LAST SHIPPED r479 (verbatim, s44 r481)'), **r478**", 1)
k = find("- Plateau window (§4): **0 of 3 — RESET by r480**")
L[k] = L[k].replace("- Plateau window (§4): **0 of 3 — RESET by r480**", "- Plateau window (§4): **0 of 3** — r481 +0.0167pp (< 0.02) but ≥50 +2 "
                    "(a protected bucket moved: neither counts nor resets); **RESET by r480**", 1)
k = find("- Standing facts: AppVersion 260620.44")
L[k] = L[k].replace("- Standing facts: AppVersion 260620.44 (r480", "- Standing facts: AppVersion 260620.45 (r481 the MTK data-row hand-off — "
                    "session 44 Round 4, 25 Sept); before it 260620.44 (r480", 1)
k = find("## Round log")
L.insert(k + 1, "- s44-r4 (engine r481, build 260620.45, 25 Sept 01:35 → ≈01:40) · THE MTK ACTIVITY'S DATA ROWS ARE ONE HAND-OFF (the r480 box's "
         "`[Activity: Embedded]` data grid whole in one cv2 hand-off — the paragraph unfold kept only 2 of its 3–6 columns) · SHIPPED scoped #7, "
         "scoped_ship PASS · TRR116, 9 pages · skeleton +0.0167pp (7 up / 2 down), ≥50 +2 · plateau 0 of 3 (neither).")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r481** (260620.45, "
        "the MTK data-row hand-off); LAST FULL = **r474**; ledger scoped #7 (**1 of headroom — the next ship is the FULL backstop**); plateau "
        "**0 of 3**; 2,491 pairs; census 552 / 545 / 2,679. Ride-along patches `_r469_declined.patch` (alerts) / `_r469b_declined.patch` (buttons) / "
        "`_r468_declined.patch`. Needs Chris #17–#19, #22.")
k = find("- **(s44-r2) THE TRR1 LESSON-PAGE LANE")
L[k] = L[k].replace("NEXT: (B) the marker table's data rows as one hand-off — built in r480, OFF (`data_rows_handoff`), pre-scored +41.7 pp-sum on "
                    "TRR116; measure its own gate effect and ship it as its own round.", "(B) the marker table's data rows as one hand-off — "
                    "SHIPPED r481 (+0.0167pp, scoped_ship PASS).", 1)
assert "SHIPPED r481" in L[k]
k = find("## Session 44 — Round 4 PICK (engine r481)")
j = k + 1
while j < len(L) and not L[j].startswith("## "): j += 1
pick = L[k:j]; del L[k:j]
L.insert(k, "## Session 44 — Round 4 PICK (engine r481) — THE MTK ACTIVITY'S DATA ROWS ARE ONE HAND-OFF — SHIPPED; the PICK + what-shipped record "
         "is in LOOP_STATE_ARCHIVE.md 'Session 44 — Round 4 PICK (engine r481) + what shipped'; the one-line summary is the s44-r4 Round-log line below.\n")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r479 (verbatim, s44 r481)\n\n" + r479 + "\n"
    "\n## Session 44 — Round 4 PICK (engine r481) + what shipped\n\n" + marker + "\n" + prior + "\n" + "\n".join(pick[1:]).rstrip() + "\n"
    "- **What shipped (r481, 260620.45):** `act_label_box.data_rows_handoff` true + `data_env` ACTDATA_OFF. Probe OFF 3222 identical; ON 9 "
    "pages / TRR116; scoped_ship PASS (compare_structure EXACT — the rows sat inside div.activity before and after); +0.0167pp, ≥50 +2, 7 up / "
    "2 down (TRR116_1_0 −6.7 named: its flip-card / map grids the gold partly shows as visible audioImage / sassoonI lines).\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
