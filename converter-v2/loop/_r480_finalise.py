#!/usr/bin/env python3
"""ROUND 480 finalise (session 44 Round 3 — KB 07B: the MTK activity is ONE box, a §1d TRR family dialect, ACTLABELBOX_OFF) —
BUILD_CHANGELOG.md (prepend), Config.js AppVersion 260620.43 -> 260620.44, OPERATING_GUIDE §9 / §11 / §14, gate_baseline.json, KB status
(a §D 07B row), LOOP_STATE.md (marker cleared, Position, plateau RESET, round log, next-session line, Follow-up, Declined; the PICK →
archive). Line edits only; .bak kept; nothing written until every anchor is found. WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 480," not in sc[:3000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.43";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 479 BASELINE"; a11 = "| `PROVERBBOX_OFF` | 479 |"; a14 = "- **Build:** `260620.43` (round 479"
for a in (a9, a11, a14): assert so.count(a) == 1, a
PK = os.path.join(ROOT, "KB_AMALGAMATION_STATUS.md"); sk = rd(PK); KL = sk.split("\n")
kd = [i for i, l in enumerate(KL) if l.startswith('| ~~—~~ | 07B MTK "Whakatauki / Proverb"')]; assert len(kd) == 1
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 480 IN FLIGHT — NOT PROVEN**", "- **No round in flight** (25 Sept 2026 ≈00:40, session 44 Round 2", "- LAST SHIPPED: **r479**",
          "- Before it: **r478**", "- Before them: **r477**", "- Plateau window (§4): **2 of 3** — r479", "- Standing facts: AppVersion 260620.43",
          "## Round log", "**Next session starts with:**", "## Session 44 — Round 3 PICK (engine r480)", "- **(s44-r2) THE TRR1 LESSON-PAGE LANE",
          "## Declined classes"):
    find(p)

entry = """## 2026-09-25 (round 480, build 260620.44) — KB 07B "ACTIVITY STRUCTURE" (a §1d TRR FAMILY DIALECT): the MTK activity is ONE box — the `Activity NX: ║ Ngohe NX:` intro table + its `[Activity: Embedded]` table render as one `div.activity`

### 1. WHAT CHANGED

**The find** (session 44 Round 3 — the TRR1 lesson-page lane, the loss ledger's lowest-scoring large family; triangulated TRR116_4_0 / TRR116_1_0 / TRR106_2_0 with `outputs/_s44_skdump.py`): TRR116 / TRR106 / TRR103 write each activity as TWO tables — a bilingual intro (`English ║ Te Reo Māori` / `Activity 4E: ║ Ngohe 4E:` / `[H2] title` / `[Body] …`) and the red `[Activity: Embedded] <type>` table (the instructions + the widget's data). The gold boxes them TOGETHER — one `div.activity` holding the title, the prose and the instructions (`outputs/_s44_r3_acttables.cjs` + `_s44_r3_actgold2.py`, every heading occurrence counted: TRR116 43 / 43 boxed, TRR103 8 boxed / 5 mixed / 2 free, TRR106 5 / 9; 89 label tables in 4 modules); Claude rendered the intro as free `row > col-md-8` prose (`bilingualTable` catches the header row before the activity gather) and the embedded table as a separate box.

**The fix** (KB 07B §7 "Activity Structure": `| Activity 1A: | Ngohe 1A: |` + `[H2]` + `[Body]` → ONE `div.activity number=` holding `<h3 reo>` / `<h3 eng>` + the prose): the reoMode dispatch in `ContentConverter`, BEFORE `bilingualTable` — a bilingual table whose first content row is the label pair (`BilingualBuilder.isActLabelTable`, read through bold / red / tags) gathers itself + a following `[Activity: Embedded]` marker table + its spec tables (the existing gather's stops) into `bilingualActivity(blocks, run, norm, alb)`: the intro unfolds exactly as it does free (`bilingualRows` — header skipped, reo / eng interleaved, the label line stripped) with its `[H2]` emitted at h3 (`intro_h2_level`); the box takes the KB 07D lesson wrapper and the r454 numbering (lesson.position); an intro with no widget table is a plain `div.activity`. Data `Emit_Templates.elements.dual_language.act_label_box` {enabled, env, code_prefixes ["TRR"], exclude_codes ["TRR102"], label_pattern, intro_h2_level 3, data_rows_handoff false}; env **`ACTLABELBOX_OFF`**, byte-identical OFF. **Scope — a §1d family dialect:** TRR102's own gold keeps the intro FREE on 15 of its 22 label tables (it contradicts KB 07B's form at 0.68 — §2 (c)), so it is excluded by name and keeps the r479 output. **Built OFF for its own round:** (B) the marker table's data rows as ONE hand-off (`data_rows_handoff`, the code in place, false) — pre-scored +41.7 pp-sum on TRR116 on top of (A), its own gate effect not yet separated. **Measured and declined:** (b) the identical reo = eng pair shipped once (`outputs/_s44_r3_bilpairs.py`: the gold ships it once 111 / twice 132 — no consensus).

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 3222 / 3222 identical**; ON 14 pages / 3 modules (TRR103 TRR106 TRR116 — `outputs/_affected_r480.txt`). Pre-scored on the saved ON pages (`outputs/_s42_prescore.py r480`) through four iterations (the bilingualActivity row unfold → `bilingualRows`; TRR102 excluded; the h3 title; (B) off).
- Regeneration of the 3 + the 12-module spot-check (`_r480_regen.sh`): 0 truly stale, 12 / 12 byte-identical; `scoped_ship.sh` containment OK (3 ⊆ 3); its decomposition flagged compare_structure exact −80 → committed NAMED (`_r480_commit_named.sh`, `--accept-named "compare_structure exact chain"`).

### 3. PROTECTED GATES

- Skeleton **55.2477 % → 55.3088 % @ 2491 (+0.0611pp)**, RAW 39.200 → 39.240 %; **≥50 1576 → 1580 (+4)**; ≥75 275; ≥90 25; 14 movers (**12 up / 2 down**, pp-sum **+152.2**), none outside the affected set: TRR116_1_0 +26.5 (31.8 → 58.3), TRR106_2_0 +24.7, TRR116_2_0 +24.3, TRR116_9_0 +19.0, TRR116_7_0 +13.5, TRR116_3_0 +11.1, TRR103_2_0 +10.4, TRR106_1_0 +8.3, TRR116_4_0 +7.5, TRR116_6_0 +7.4 …; NAMED dips: TRR116_5_0 29.6 → 26.5 (a side-alert table sits BETWEEN the intro and its activity table in the Writers Template, so the box gathers the intro alone — the gold's one box holds both with the alert beside it), TRR103_1_0 39.0 → 38.4 (TRR103's 1A intro is one its gold keeps free).
- compare_structure **exact 16771 → 16691 (−80) NAMED = the matched pool 19533 → 19453 (−80)**: the intro elements now sit inside `div.activity`, a subtree compare_structure excludes on BOTH sides (`activity` is in its INTERACTIVE_CLASSES) — the r344 pool-shrink precedent; EXTRA 208 / missing 872 EXACT; body ANY 238; clean 2587 / 2633; leak 75 / 46 — EXACT; every verifier RESULT line ✓; 17 selftests + the skeleton selftest green; the feature index green; the miner 197 → 195 CANDIDATE.
- Plateau (§4): the PICK predicted a skeleton move and it delivered +0.0611pp (≥ 0.02) — **the window RESETS: 0 of 3**.

**Ledger:** scoped #6 since the r474 FULL · data `elements.dual_language.act_label_box` · env `ACTLABELBOX_OFF` · code `ContentConverter` (the reoMode dispatch), `BilingualBuilder.actLabelBoxCfg` / `isActLabelTable` / `bilingualActivity` (alb) / `#albClean` / `#markerDataFrom` · tools `_s44_r3_{bilpairs,actgold,actgold2,pick}.py`, `_s44_r3_{embrows,actprobe,acttables}.cjs`, `_s44_dashboard_run.sh`, `_r480_{regen,commit_named,postship}.sh`, `_r480_finalise.py` · session 44 Round 3.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 480 (260620.44): KB 07B THE MTK ACTIVITY IS ONE BOX (session 44 Round 3, a TRR family dialect). The `Activity NX: ║ Ngohe NX:` "
                "intro table + its [Activity: Embedded] table render as one div.activity (BilingualBuilder.isActLabelTable / bilingualActivity alb). "
                "Env ACTLABELBOX_OFF.\n"
                '\tstatic AppVersion = "260620.44";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 480 BASELINE (KB 07B the MTK activity is ONE box — a §1d TRR "
                "family dialect, `ACTLABELBOX_OFF`; SCOPED, scoped #6 since the r474 FULL): SCAFFOLD mean 55.3088% / >=50% 1580 / >=75% 275 / "
                ">=90% 25 / RAW 39.240% @ 2491 pairs — +0.0611pp (12 up / 2 down, ≥50 +4); cs exact 16691 (−80 NAMED = the pool shrink, the intros "
                "now inside div.activity which compare_structure excludes); EXTRA / missing / body / clean / leak EXACT.** Previous: **ROUND 479 BASELINE")
so = so.replace(a11, "| `ACTLABELBOX_OFF` | 480 | **KB 07B THE MTK ACTIVITY IS ONE BOX** (session 44 Round 3; TRR family dialect, TRR102 excluded). Reverts "
                "`elements.dual_language.act_label_box`: the `Activity NX: ║ Ngohe NX:` intro renders free again and its `[Activity: Embedded]` "
                "table as a separate box — 3 modules / 14 pages; byte-identical to r479. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.44` (round 480 — **KB 07B: the MTK activity is one box** (TRR family dialect); `ACTLABELBOX_OFF`; scoped "
                "#6 since the r474 FULL; 3 modules; skeleton 55.3088 % @ 2491, +0.0611pp, ≥50 +4; cs exact 16691, −80 NAMED pool shrink).\n" + a14)
wr(PO, so); print("OG ok")
KL.insert(kd[0] + 1, "| ~~—~~ | 07B MTK \"Activity Structure\" — the `Activity NX: ║ Ngohe NX:` intro table (+ `[H2]` title + `[Body]`) and its "
          "`[Activity: Embedded]` table are ONE `div.activity` holding `<h3 reo>` / `<h3 eng>` + the prose + the instructions | **SHIPPED round 480 "
          "(2026-09-25, session 44 Round 3)** — `elements.dual_language.act_label_box`, `ACTLABELBOX_OFF`; a §1d TRR family dialect (TRR116 / "
          "TRR106 / TRR103; TRR102 excluded — its gold keeps the intro free 15 / 22); 3 modules / 14 pages; +0.0611pp, ≥50 +4. |")
wr(PK, "\n".join(KL)); print("KB status ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r480.bak")
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
setv("build", '"260620.43"', '"260620.44"'); setv("round", "479", "480")
insert_before("_note_r479", '    "_note_r480": "Round 480 (session 44 Round 3, 2026-09-25) — KB 07B THE MTK ACTIVITY IS ONE BOX (ACTLABELBOX_OFF; a §1d TRR family '
              'dialect, TRR102 excluded): 3 modules / 14 pages; SCAFFOLD 55.2477 -> 55.3088 @ 2491 (+0.0611pp, 12 up / 2 down, pp-sum +152.2); RAW '
              '39.200 -> 39.240; >=50 1576 -> 1580; cs exact 16771 -> 16691 NAMED (the matched pool 19533 -> 19453: the intros inside div.activity, '
              'which compare_structure excludes on both sides); EXTRA / missing / body / clean / leak EXACT; scoped #6 since the r474 FULL; committed NAMED.",')
setv("mean_scaffold_pct", "55.25", "55.31"); setv("pages_ge_50", "1576", "1580"); setv("raw_mean_pct", "39.2", "39.24")
insert_before("_note_r479_state", '    "_note_r480_state": "r480 (the MTK one-box activity): SCAFFOLD 55.3088 @ 2491, RAW 39.240; 14 movers (12 up / 2 down).",')
setv("exact_chain", "16771", "16691")
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-r480-finalise.bak")
i = find("- **ROUND 480 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (25 Sept 2026 ≈01:20, session 44 Round 3 — r480 (KB 07B, the MTK activity is one box) SHIPPED and committed; "
        "the in-flight marker is cleared). LAST SHIPPED **r480** (260620.44); **LAST FULL = r474**; ledger **scoped #6** (2 of headroom). Ride-along "
        "patches `outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` (buttons, 10 pages) / `_r468_declined.patch` (the "
        "lesson menu's `[H2]` lead, 3 pages).")
k = find("- **No round in flight** (25 Sept 2026 ≈00:40, session 44 Round 2"); prior = L[k]; del L[k]
k = find("- Before it: **r478**"); r478 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r479**"); L[k] = L[k].replace("- LAST SHIPPED: **r479**", "- Before it: **r479**", 1)
L.insert(k, "- LAST SHIPPED: **r480** (build 260620.44, 25 Sept ≈01:20, session 44 Round 3 — KB 07B THE MTK ACTIVITY IS ONE BOX (a §1d TRR "
         "family dialect, TRR102 excluded), `ACTLABELBOX_OFF`; SCOPED, **scoped #6 since the r474 FULL**, committed NAMED; **skeleton 55.2477 → "
         "55.3088 % @ 2491 (+0.0611pp, 12 up / 2 down, pp-sum +152.2)**, **≥50 1580 (+4)**, ≥75 275, ≥90 25, RAW 39.240 %; **cs exact 16691 (−80 "
         "NAMED — the pool shrink)**, EXTRA 208, missing 872; body / clean / leak EXACT; `gate_baseline.json` at r480; the miner 195 CANDIDATE).")
k = find("- Before them: **r477**")
L[k] = L[k].replace("- Before them: **r477**", "- Before them: **r478** (260620.42, KB c75 the activity's lead prose — verbatim → "
                    "LOOP_STATE_ARCHIVE.md 'Position — LAST SHIPPED r478 (verbatim, s44 r480)'), **r477**", 1)
k = find("- Plateau window (§4): **2 of 3** — r479")
L[k] = L[k].replace("- Plateau window (§4): **2 of 3** — r479", "- Plateau window (§4): **0 of 3 — RESET by r480** (its PICK predicted a skeleton "
                    "move and it delivered +0.0611pp ≥ 0.02); before it: 2 of 3 — r479", 1)
k = find("- Standing facts: AppVersion 260620.43")
L[k] = L[k].replace("- Standing facts: AppVersion 260620.43 (r479", "- Standing facts: AppVersion 260620.44 (r480 KB 07B the MTK one-box activity — "
                    "session 44 Round 3, 25 Sept); before it 260620.43 (r479", 1)
k = find("## Round log")
L.insert(k + 1, "- s44-r3 (engine r480, build 260620.44, 25 Sept 00:45 → ≈01:20) · KB 07B THE MTK ACTIVITY IS ONE BOX (the `Activity NX: ║ Ngohe NX:` "
         "intro + its `[Activity: Embedded]` table; a §1d TRR family dialect, TRR102 excluded; the identical-pair (b) declined; the data "
         "hand-off (B) built OFF for its own round) · SHIPPED scoped #6, committed NAMED (cs exact −80 pool shrink) · 3 modules / 14 pages · skeleton +0.0611pp "
         "(12 up / 2 down), ≥50 +4 · plateau RESET (0 of 3).")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r480** (260620.44, "
        "KB 07B the MTK one-box activity); LAST FULL = **r474**; ledger scoped #6 (2 of headroom — a FULL backstop is due within 2 ships); plateau "
        "**0 of 3**; 2,491 pairs; census 552 / 545 / 2,679. Ride-along patches `_r469_declined.patch` (alerts) / `_r469b_declined.patch` (buttons) / "
        "`_r468_declined.patch`. Needs Chris #17–#19, #22.")
k = find("- **(s44-r2) THE TRR1 LESSON-PAGE LANE")
L[k] = L[k].replace("Taken: the whakatauki box (r479). Left, each measured: (a) the `Activity NX: ║ Ngohe NX:` + `[H2]` intro table the gold boxes "
                    "TOGETHER with the following `[Activity: Embedded]` table (KB 07B 'Activity Structure') — 52 tables in TRR116 (43) / TRR106 (9) only, "
                    "gold boxes the title 47 / 50, Claude 0 — ≈ 12 pages / 2 modules, a §1d family-dialect candidate (`_s44_r2_actlabel.py`); (b) the "
                    "reo = eng identical heading pair (`h3 reo Hea` + `h3 eng Hea`) the gold ships ONCE;",
                    "Taken: the whakatauki box (r479); the one-box MTK activity (r480 — TRR116 / TRR106 / TRR103; TRR102 excluded, its gold keeps the "
                    "intro free 15 / 22). Measured and DECLINED s44-r3: (b) the reo = eng identical pair (the gold ships it once 111 / twice 132). NEXT: (B) the "
                    "marker table's data rows as one hand-off — built in r480, OFF (`data_rows_handoff`), pre-scored +41.7 pp-sum on TRR116; measure "
                    "its own gate effect and ship it as its own round. Left: TRR116_5_0's side-alert table BETWEEN an intro and its activity table (the gold "
                    "boxes both, the alert beside);", 1)
assert "r480 — TRR116" in L[k]
k = find("## Declined classes")
L.insert(k + 1, "- **Session 44 Round 3 (25 Sept 00:45 → 01:20) — inside r480's PICK, two sub-classes of the TRR1 lesson lane DECLINED on "
         "measurement:** (b) the identical reo = eng pair shipped ONCE (`_s44_r3_bilpairs.py`: gold once 111 / twice 132 pairs — no consensus); (c) "
         "the audio-word line `p.center-text.sassoonI-text` (98 in 4 modules, 84 of them TRR111 — one module's dialect, below floor).")
k = find("## Session 44 — Round 3 PICK (engine r480)")
j = k + 1
while j < len(L) and not L[j].startswith("## "): j += 1
pick = L[k:j]; del L[k:j]
L.insert(k, "## Session 44 — Round 3 PICK (engine r480) — KB 07B THE MTK ACTIVITY IS ONE BOX — SHIPPED; the PICK + what-shipped record is in "
         "LOOP_STATE_ARCHIVE.md 'Session 44 — Round 3 PICK (engine r480) + what shipped'; the one-line summary is the s44-r3 Round-log line below.\n")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r478 (verbatim, s44 r480)\n\n" + r478 + "\n"
    "\n## Session 44 — Round 3 PICK (engine r480) + what shipped\n\n" + marker + "\n" + prior + "\n" + "\n".join(pick[1:]).rstrip() + "\n"
    "- **What shipped (r480, 260620.44):** `elements.dual_language.act_label_box` (env `ACTLABELBOX_OFF`; code_prefixes TRR, exclude_codes "
    "TRR102, intro_h2_level 3, data_rows_handoff false) — the reoMode dispatch gathers the label-intro table + its marker table (+ spec tables) "
    "into bilingualActivity(alb): the intro through bilingualRows (interleaved, header skipped, label stripped), its [H2] at h3, the r454 "
    "numbering and the 07D wrapper. Four pre-score iterations: the raw row unfold (+0.0192pp, TRR102 −75) → bilingualRows (+0.0512pp) → TRR102 "
    "excluded (+0.0702pp) → h3 (+0.0779pp with (B)); the scoped ship's cs exact −80 is the pool shrink of the boxing itself (it stayed −80 "
    "with (B) OFF), so (B) — its own effect not separated — is left OFF for its own round. Shipped (A): +0.0611pp, ≥50 +4, 12 up / 2 down; cs exact −80 named.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
