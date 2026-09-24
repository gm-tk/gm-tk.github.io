#!/usr/bin/env python3
"""ROUND 478 finalise (session 43 Round 10, finished session 44 Round 1 — KB c75: the activity's lead keeps its links, LEADLINKS_OFF) —
BUILD_CHANGELOG.md (prepend), Config.js AppVersion 260620.41 -> 260620.42, OPERATING_GUIDE §9 / §11 / §14, gate_baseline.json (build / round /
notes / skeleton), KB_AMALGAMATION_STATUS.md row 75, LOOP_STATE.md (marker cleared, Position, plateau, round log, next-session line;
the PICK → archive). Line edits only; .bak kept; nothing written until every anchor is found. WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 478," not in sc[:3000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.41";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 477 BASELINE"; a11 = "| `GATHERLINKS_OFF` | 477 |"; a14 = "- **Build:** `260620.41` (round 477"
for a in (a9, a11, a14): assert so.count(a) == 1, a
PK = os.path.join(ROOT, "KB_AMALGAMATION_STATUS.md"); sk = rd(PK)
k75 = "Remaining: table cells (a precision question). |"
assert sk.count(k75) == 1
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND r478 IN FLIGHT — NOT PROVEN", "- **Before r478: no round in flight**", "- LAST SHIPPED: **r477**", "- Before it: **r476**",
          "- Before them: **r475**", "- Plateau window (§4): **2 of 3** — r477", "- Standing facts: AppVersion 260620.41", "## Round log",
          "**Next session starts with:**", "## Session 43 — Round 10 PICK (engine r478)"):
    find(p)

entry = """## 2026-09-25 (round 478, build 260620.42) — KB CONSTRAINT 75 FOR THE ACTIVITY'S LEAD PROSE: a bundle-owned activity's lead (the writer's instruction block before the widget box) keeps the writer's inline links — public web targets, whole-phrase anchors

### 1. WHAT CHANGED

**The find** (session 43 Round 10 — the r475 link census re-run on the r477 corpus, `outputs/_s43_r10_linkdet.py`; traced with `outputs/_s43_r8_linkdbg.cjs HES1007 "Commodifying childhood"`): HES1007-3.0 activity 3B "Energy drink resources" — `[Activity 3B] [H3]` + `[body]` + five `__title__ [LINK: url] source` reading lines + a clickDrop — is a BUNDLE-OWNED activity; its lead prose is buffered by `ContentConverter.ConvertPage`'s `flushLead` and rendered through `renderBlackText(leadBuf.join("\\n"), run)` with NO links, so every writer link in it lost its href (the gold links each reading title). A third free-body path beside r477's two (`#element`'s body default, `#calloutOpen`).

**The fix** (`ContentConverter.#leadLinks(bundle)` = the owner's `block.links` + every non-table lead item's `block.links`, through r477's filter — factored out as `#weaveableLinks`: r476's target exclusion (ONE pattern) and a ≥ 3-character phrase floor; `flushLead` passes them to `renderBlackText`; data `Emit_Templates.body_region.activity_lead_links` {enabled, env, exclude_targets, min_text_chars 3}; env **`LEADLINKS_OFF`**, byte-identical OFF — the r477 call is kept byte for byte when the flag is off).

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 3222 / 3222 identical**; ON 21 pages / 13 modules (BLL173 ENFUN08 ENGJ301 ENO2060 HES1007 HIS1003 HIS1004 MXFL203 MXFU201 MXFU202 TWHK901 XDLS912 XTAS101 — `outputs/_affected_r478.txt`, identical in session 43 and session 44); 63 hrefs added, 43 of them links the gold carries, 20 public pages the gold drops; every added `<a>` inside a `<p>` / `<b>` / `<i>` (`_s43_r10_parents.py`).
- Regeneration of the 13 + the 12-module spot-check (`_r478_regen.sh`): 0 truly stale, 12 / 12 byte-identical; `scoped_ship.sh` containment OK (13 ⊆ 13), every decomposed gate HELD except the mean (−0.0027pp) → committed NAMED (`_r478_commit_named.sh`, `--accept-named "skeleton SCAFFOLD mean"`).
- Built in session 43, toggled OFF at Chris's `/loop-stop` (the 13 regenerated back, manifest 0 pages differ), finished in session 44 Round 1 with identical measurements.

### 3. PROTECTED GATES

- Skeleton **55.2360 % → 55.2333 % @ 2491 (−0.0027pp, NAMED — §1b "Gates and KB overrides": KB c75 outranks the gold)**, RAW 39.195 → 39.194 %; ≥50 1577; ≥75 275; ≥90 25; 21 movers (5 up / 16 down, pp-sum −6.7), none outside the affected set. Worst: HES1007_8_0 53.0 → 51.3 (the gold keeps HES1007's reading links but as a `<ul><li>` list), MXFL203_10_0 40.9 → 39.4, ENO2060_2_0 41.2 → 40.0 (the writer's public link the gold drops); best XDLS912_5_0 +0.5, MXFU202_6_0 +0.5.
- compare_structure exact 16759, EXTRA 208, missing 903; body ANY 238; clean 2587 / 2633; leak 75 / 46 — all EXACT; every verifier RESULT line ✓; 17 selftests + the skeleton selftest green (50 PASS / GREEN, 0 FAIL); the feature index green; the miner 197 CANDIDATE.
- Plateau (§4): a KB-rule round; neither counts nor resets: **2 of 3** stands.

**Ledger:** scoped #4 since the r474 FULL · data `body_region.activity_lead_links` · env `LEADLINKS_OFF` · code `ContentConverter.#leadLinks` / `#weaveableLinks` / `ConvertPage` `flushLead` · tools `_r478_{regen,postship,commit_named,finalise}` · session 44 Round 1.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 478 (260620.42): KB c75 FOR THE ACTIVITY'S LEAD PROSE (session 43 Round 10, finished session 44 Round 1). "
                "ContentConverter.#leadLinks hands flushLead the owner's + the lead items' links (public web targets, >= 3-character phrases). "
                "Env LEADLINKS_OFF.\n"
                '\tstatic AppVersion = "260620.42";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 478 BASELINE (KB c75 for the activity's lead prose — the "
                "writer's links in a bundle-owned activity's lead, `LEADLINKS_OFF`; SCOPED, scoped #4 since the r474 FULL): "
                "SCAFFOLD mean 55.2333% / >=50% 1577 / >=75% 275 / >=90% 25 / RAW 39.194% @ 2491 pairs — −0.0027pp NAMED "
                "(KB c75 outranks the gold: HES1007's list-form reading links, public links the gold drops); cs / body / clean / leak EXACT.** Previous: "
                "**ROUND 477 BASELINE")
so = so.replace(a11, "| `LEADLINKS_OFF` | 478 | **KB c75 FOR THE ACTIVITY'S LEAD PROSE** (session 43 Round 10, finished session 44 Round 1). Reverts "
                "`body_region.activity_lead_links`: a bundle-owned activity's lead prose loses the writer's inline links again — 13 "
                "modules / 21 pages; byte-identical to r477. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.42` (round 478 — **KB c75 FOR THE ACTIVITY'S LEAD PROSE**; `LEADLINKS_OFF`; scoped #4 since the r474 FULL; "
                "13 modules; skeleton 55.2333 % @ 2491, −0.0027pp NAMED; cs exact 16759).\n" + a14)
wr(PO, so); print("OG ok")
sk = sk.replace(k75, "**r478 (session 43 Round 10, finished session 44 Round 1): the ACTIVITY LEAD half — a bundle-owned activity's lead prose "
                "weaves the writer's public-web links (`body_region.activity_lead_links`, `LEADLINKS_OFF`; 13 modules / 21 pages).** "
                "Remaining: table cells (a precision question). |")
wr(PK, sk); print("KB status ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r478.bak")
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
setv("build", '"260620.41"', '"260620.42"'); setv("round", "477", "478")
insert_before("_note_r477", '    "_note_r478": "Round 478 (session 43 Round 10, finished session 44 Round 1, 2026-09-25) — KB c75 FOR THE ACTIVITY\'S LEAD PROSE '
              '(LEADLINKS_OFF): 13 modules / 21 pages; SCAFFOLD 55.2360 -> 55.2333 @ 2491 (-0.0027pp NAMED, 5 up / 16 down, no crossing — KB c75 '
              'outranks the gold: HES1007\'s list-form reading links, public links the gold drops); RAW 39.195 -> 39.194; cs / body / clean / '
              'leak EXACT; scoped #4 since the r474 FULL; committed NAMED.",')
setv("mean_scaffold_pct", "55.24", "55.23"); setv("raw_mean_pct", "39.2", "39.19")
insert_before("_note_r477_state", '    "_note_r478_state": "r478 (the activity-lead links): SCAFFOLD 55.2333 @ 2491, RAW 39.194; 21 movers (5 up / 16 down).",')
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-r478-finalise.bak")
i = find("- **ROUND r478 IN FLIGHT — NOT PROVEN"); marker = L[i]
L[i] = ("- **No round in flight** (25 Sept 2026 ≈00:05, session 44 Round 1 — r478 (KB c75 for the activity's lead prose) FINISHED, SHIPPED and "
        "committed; the in-flight marker is cleared). LAST SHIPPED **r478** (260620.42); **LAST FULL = r474**; ledger **scoped #4** (4 of "
        "headroom). Ride-along patches `outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` (buttons, 10 pages) / "
        "`_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages).")
k = find("- **Before r478: no round in flight**"); prior = L[k]; del L[k]
k = find("- Before it: **r476**"); r476 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r477**"); L[k] = L[k].replace("- LAST SHIPPED: **r477**", "- Before it: **r477**", 1)
L.insert(k, "- LAST SHIPPED: **r478** (build 260620.42, 25 Sept ≈00:05, session 44 Round 1 — KB c75 FOR THE ACTIVITY'S LEAD PROSE, "
         "`LEADLINKS_OFF`; built s43 Round 10, toggled OFF at the stop, finished here; SCOPED, **scoped #4 since the r474 FULL**, committed NAMED; "
         "**skeleton 55.2360 → 55.2333 % @ 2491 (−0.0027pp NAMED, 5 up / 16 down, no crossing)**, ≥50 1577, ≥75 275, ≥90 25, RAW 39.194 %; "
         "cs exact 16759; body / clean / leak EXACT; `gate_baseline.json` at r478; the miner 197 CANDIDATE).")
k = find("- Before them: **r475**")
L[k] = L[k].replace("- Before them: **r475**", "- Before them: **r476** (260620.40, KB c75 for built widgets — verbatim → "
                    "LOOP_STATE_ARCHIVE.md 'Position — LAST SHIPPED r476 (verbatim, s44 r478)'), **r475**", 1)
k = find("- Plateau window (§4): **2 of 3** — r477")
L[k] = L[k].replace("- Plateau window (§4): **2 of 3** — r477", "- Plateau window (§4): **2 of 3** — r478 a KB-rule round (−0.0027pp NAMED; "
                    "neither counts nor resets); r477", 1)
k = find("- Standing facts: AppVersion 260620.41")
L[k] = L[k].replace("- Standing facts: AppVersion 260620.41 (r477", "- Standing facts: AppVersion 260620.42 (r478 KB c75 for the activity's lead "
                    "prose — session 44 Round 1, 25 Sept); before it 260620.41 (r477", 1)
k = find("## Round log")
L.insert(k + 1, "- s44-r1 (engine r478, build 260620.42, 24 Sept 23:40 → 25 Sept ≈00:05) · KB c75 FOR THE ACTIVITY'S LEAD PROSE: a bundle-owned "
         "activity's lead keeps the writer's links (HES1007 3B's reading list) — built s43-r10, toggled OFF at the stop, FINISHED here · SHIPPED "
         "scoped #4, committed NAMED · 13 modules / 21 pages · skeleton −0.0027pp NAMED (5 up / 16 down) · cs / body EXACT · plateau 2 of 3 (neither).")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r478** (260620.42, "
        "KB c75 for the activity's lead prose); LAST FULL = **r474**; ledger scoped #4; plateau **2 of 3**; 2,491 pairs; census 552 / 545 / 2,679. "
        "Ride-along patches `_r469_declined.patch` (alerts) / `_r469b_declined.patch` (buttons) / `_r468_declined.patch`. Needs Chris #17–#19, #22.")
k = find("## Session 43 — Round 10 PICK (engine r478)")
j = k + 1
while j < len(L) and not L[j].startswith("## "): j += 1
pick = L[k:j]; del L[k:j]
L.insert(k, "## Session 43 — Round 10 PICK (engine r478) — KB c75 FOR THE ACTIVITY'S LEAD PROSE — SHIPPED (finished session 44 Round 1); the PICK + "
         "what-shipped record is in LOOP_STATE_ARCHIVE.md 'Session 43 — Round 10 PICK (engine r478) + what shipped'; the one-line summary is the "
         "s44-r1 Round-log line below.\n")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r476 (verbatim, s44 r478)\n\n" + r476 + "\n"
    "\n## Session 43 — Round 10 PICK (engine r478) + what shipped\n\n" + marker + "\n" + prior + "\n" + "\n".join(pick[1:]).rstrip() + "\n"
    "- **What shipped (r478, 260620.42, session 44 Round 1):** `body_region.activity_lead_links` (env `LEADLINKS_OFF`; exclude_targets, "
    "min_text_chars 3) — #leadLinks hands flushLead the owner's + the lead items' links through r477's filter (#weaveableLinks). Probe ON "
    "21 pages / 13 modules (identical to s43); scoped_ship containment OK, every gate HELD but the mean (−0.0027pp) → committed NAMED "
    "(`_r478_commit_named.sh`); post-ship suite green; the miner 197 CANDIDATE.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
