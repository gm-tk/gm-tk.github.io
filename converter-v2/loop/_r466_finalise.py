#!/usr/bin/env python3
"""ROUND 466 finalise (session 42 Round 2 — Chris's D14-20, the course-code heading, COURSECODE_OFF) — BUILD_CHANGELOG.md (prepend),
Config.js AppVersion 260620.32 -> 260620.33, OPERATING_GUIDE §9 / §11 / §14, gate_baseline.json, KB_AMALGAMATION_STATUS.md (the 07D
override row), LOOP_STATE.md (marker cleared, Position, plateau, round log, follow-ups, Needs Chris #20, next-session line; the marker
→ archive; the r465 clock times corrected). Line edits only; .bak kept; nothing written until every anchor is found. Run under WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
# ---------- asserts first ----------
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 466," not in sc[:3000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.32";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 465 BASELINE"; a11 = "| `AUDIOIMGTAG_OFF` | 461 |"; a14 = "- **Build:** `260620.32` (round 465"
for a in (a9, a11, a14): assert so.count(a) == 1, a
PK = os.path.join(ROOT, "KB_AMALGAMATION_STATUS.md"); sk = rd(PK); kanchor = "| ~~—~~ | 07B MTK \"Activity Structure\" — the writer's bare `[H1] N.M` section id"; assert sk.count(kanchor) == 1
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 466 IN FLIGHT — NOT PROVEN**", "- **Before r466: no round in flight**", "- LAST SHIPPED: **r465**",
          "- Plateau window (§4): **2 of 3** — r465", "- Standing facts: AppVersion 260620.32", "## Round log",
          "**Next session starts with:**", "- **QUEUED BY CHRIS (D14, 24 Sept)", "20. ~~**24 Sept (session 41 Round 1, r453)**",
          "- s42-r1 (engine r465"):
    find(p)

entry = """## 2026-09-24 (round 466, build 260620.33) — THE WRITER'S COURSE-CODE HEADING IS DROPPED (Chris's decision D14-20): the `| [H1] TRR900 | [H1] TRR900 |` row at the head of a bilingual table — the MTK Module Introduction (TRR1 / TRR2 / TRR3, PMT101) and every PNR activity table — no longer ships as a reo / eng heading pair; the human drops it — the loop's session 42 Round 2

### 1. WHAT CHANGED

**The find** (r453, Needs Chris #20): the MTK introduction table the r453 overview restoration brought back opens with the writer's course-code row `[H1] TRR900` (both columns), and Claude rendered it as `<h3 reo>TRR900</h3><h3 eng>TRR900</h3>` above "Kōwae Ako Whakataki / Introduction". Census this round (`grep` over both corpora): **Claude 22 pages / 18 modules** — the introduction of TRR102 / 103 / 106 / 107 / 109–114 / 203 / 301 (two pages) / 304_1 and PMT101_1 (`PMT101` as the code), plus the PNR family's lesson pages, where EVERY activity table opens `| [H1] TRR900 | [H1] TRR900 | / | [H1] 1.1 | …` (PNR101 / 102 / 104 / 107, 42 heading pairs on 8 pages). **Gold: 0 bare-code h2–h6 on every Bilingual page** — 17 of the 18 introductions drop it; TRR108_0.0 keeps it as an `h1` pair (the one NAMED override); the PNR gold carries TRR900 nowhere. KB 07D's skeleton comment says "Typically: course code h1"; Chris (D14-20, 24 Sept 2026): *"Follow the recommended course of action (drop the TRR900 course headings)."*

**The fix** (`BilingualBuilder.bilingualRows`, the r330 section-id seam — the per-element interleave strip that already drops the bare `[H1] 1.1` id and the "Activity NX:" label; new `BilingualBuilder.courseCodeStripRe()`): a rendered HEADING (`h1`–`h6`) whose whole text matches `code_pattern` (`^[A-Z]{2,6}\\d{3}[:.]?$`) is dropped; a paragraph that happens to be a code stays; the module-code chip in the header is untouched. Data `Emit_Templates.elements.dual_language.section_grouping.course_code_heading` {enabled, env, code_pattern}; env **`COURSECODE_OFF`** (byte-identical OFF).

### 2. PROOF

- In-memory A/B over all 545 modules (`outputs/_s42_probe_run.sh r466`, the r448 harness): **OFF 3217 / 3217 identical; ON = exactly the census — 22 pages / 18 modules**, every diff a pure deletion of the heading pairs (`_r466_on/`), no residual bare-code heading.
- Pre-score (`_s42_prescore.py r466`): **12 up / 0 down, pp-sum +34.2** — TRR114_0 58.3 → 63.9, PMT101_1 19.7 → 23.8, PNR102_1 60.6 → 64.5, PNR104_2 / _1 +3.6 / +3.5, TRR113_0 +3.1 (72.7 → 75.8, a new ≥75 page), TRR111_0 / TRR107_0 +2.2, TRR301_0 +1.8, TRR203_0 +1.6, PNR107_1 / _2 +1.4 / +1.1; the other 10 changed pages move 0 (the heading sat beside a collapsed widget or at an aligned position).
- Scoped regeneration of the 18 + the 12-module spot-check (`_r466_regen.sh`, 3 batches): `_content_manifest.py fresh` 0 truly stale (18 affected, 524 untouched byte-identical); spot-check 12 / 12 byte-identical; the disk = the probe's ON files 78 / 78. `scoped_ship.sh --toggle COURSECODE_OFF --round 466`: **PASS** (exact, decomposition-proven), scoped **#2** since the r460 FULL.

### 3. PROTECTED GATES

- Skeleton **55.2517 % → 55.2654 % @ 2487 (+0.0137pp; 12 up / 0 down, 0 movers outside the affected set)**; ≥50 1575, **≥75 275 → 276**, ≥90 25; RAW 39.193 → 39.200.
- compare_structure 16709 / 208 / 896 / 24 EXACT; body_compare 61 / 5 / 175 / 238 EXACT; clean 2584 / 2629 EXACT; leak 74 / 45 EXACT; tags 9557 / 9557; every verifier RESULT ✓; selftests 50 PASS / 0 FAIL; feature index GREEN; the miner 197 CANDIDATE @ 2487 (`_diff_miner_r466.log`).
- Plateau (§4): a Chris-decided NAMED override (D14-20) — neither counts nor resets (the r444 / r445 / r447 precedent): **2 of 3** stands.
- Named override: TRR108_0.0 (the gold keeps the course code as an `h1` pair) — Claude never rendered it there (TRR108's introduction takes another path), so no page dips.

**Ledger:** scoped #2 since the r460 FULL · data `Emit_Templates.elements.dual_language.section_grouping.course_code_heading` · env `COURSECODE_OFF` · code `BilingualBuilder.bilingualRows` / `courseCodeStripRe` · tools `outputs/_s42_probe_run.sh`, `_s42_prescore.py`, `_r466_{regen,postship}.sh`, `_r466_finalise.py`, `_r466_{prescore,scoped_ship,gates,sk_full,skdelta,selftests,index}.log`, `_r466_sk_final.json`, `_affected_r466.txt` · AppVersion 260620.33.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 466 (260620.33): THE WRITER'S COURSE-CODE HEADING IS DROPPED (session 42 Round 2; Chris's D14-20). The `| [H1] TRR900 | [H1] TRR900 |` row at the head of a bilingual table (the MTK introduction, the PNR activity tables) no longer ships as a reo / eng heading pair — the gold drops it on every Bilingual page (TRR108_0.0's h1 the one named override). Emit_Templates dual_language.section_grouping.course_code_heading, env COURSECODE_OFF; 18 modules / 22 pages; skeleton +0.0137pp (12 up / 0 down), >=75 +1; every other gate exact.\n" + '\tstatic AppVersion = "260620.33";', 1)
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 466 BASELINE (the course-code heading dropped — Chris's D14-20, `COURSECODE_OFF`; SCOPED, scoped #2 since the r460 FULL): SCAFFOLD mean 55.2654% / >=50% 1575 / >=75% 276 / >=90% 25 / RAW 39.200% @ 2487 pairs — +0.0137pp (12 up / 0 down); cs 16709 / 208 / 896 / 24, body 61 / 5 / 175 / 238, clean 2584 / 2629, leak 74 / 45 — all EXACT.** Previous: **ROUND 465 BASELINE", 1)
so = so.replace(a11, "| `COURSECODE_OFF` | 466 | **THE WRITER'S COURSE-CODE HEADING IS DROPPED** (session 42 Round 2; Chris's D14-20). Reverts `elements.dual_language.section_grouping.course_code_heading`: the `[H1] TRR900` row at the head of a bilingual table (the MTK introduction, the PNR activity tables) ships as a reo / eng heading pair again; byte-identical to r465. 18 modules / 22 pages; skeleton +0.0137pp (12 up / 0 down). |\n" + a11, 1)
so = so.replace(a14, "- **Build:** `260620.33` (round 466 — **THE WRITER'S COURSE-CODE HEADING IS DROPPED** (Chris's D14-20): the bilingual `[H1] TRR900` row no longer ships as a heading pair; `COURSECODE_OFF`; scoped #2 since the r460 FULL; 18 modules / 22 pages; skeleton 55.2654 %, ≥75 276).\n" + a14, 1)
wr(PO, so); print("OG ok")
# ---------- gate_baseline.json ----------
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r466.bak")
G = rd(P).split("\n")
def setv(key, old, new):
    for i, l in enumerate(G):
        if l.strip().startswith(f'"{key}": '):
            assert l.strip().rstrip(",") == f'"{key}": {old}', (key, l)
            G[i] = l.replace(f'"{key}": {old}', f'"{key}": {new}'); return
    raise SystemExit(f"not found {key}")
def insert_before(key, line):
    for i, l in enumerate(G):
        if l.strip().startswith(f'"{key}": '): G.insert(i, line); return
    raise SystemExit(f"anchor {key}")
setv("build", '"260620.32"', '"260620.33"'); setv("round", "465", "466")
insert_before("_note_r465", '    "_note_r466": "Round 466 (session 42 Round 2, 2026-09-24; Chris\'s D14-20) — THE WRITER\'S COURSE-CODE HEADING IS DROPPED (COURSECODE_OFF): 18 modules / 22 pages; SCAFFOLD 55.2517 -> 55.2654 (+0.0137pp; 12 up / 0 down), >=75 275 -> 276, RAW 39.193 -> 39.200; every other gate EXACT; scoped #2 since the r460 FULL.",')
setv("mean_scaffold_pct", "55.25", "55.27"); setv("pages_ge_75", "275", "276"); setv("raw_mean_pct", "39.19", "39.2")
insert_before("_note_r465_state", '    "_note_r466_state": "r466 (the course-code heading): SCAFFOLD 55.2517 -> 55.2654 @ 2487, RAW 39.193 -> 39.200; 12 movers, 0 outside the affected set.",')
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
# ---------- KB status ----------
i = sk.index(kanchor); j = sk.index("\n", i) + 1
sk = sk[:j] + "| — | 07D MTK skeleton comment \"Typically: course code h1\" — the writer's `[H1] TRR900` course-code row at the head of the Module Introduction (and of the PNR activity tables) | 07D | MTK bilingual (TRR1–3, PMT101, PNR) | **NAMED OVERRIDE by Chris's D14-20 — SHIPPED round 466 (2026-09-24)**: the heading is DROPPED (`dual_language.section_grouping.course_code_heading`, COURSECODE_OFF; 18 modules / 22 pages) — the gold drops it on every Bilingual page but TRR108_0.0's `h1` | BilingualBuilder |\n" + sk[j:]
wr(PK, sk); print("KB ok")
# ---------- LOOP_STATE ----------
shutil.copyfile(S, S + ".pre-r466-finalise.bak")
i = find("- **ROUND 466 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (24 Sept 2026 ≈14:55, session 42 Round 2 — r466 (D14-20) SHIPPED and committed; the in-flight marker "
        "is cleared). LAST SHIPPED **r466** (260620.33); **LAST FULL = r460**; ledger **scoped #2** since it (6 of headroom). Chris's D14 "
        "queue is DONE (r465 / r466); next: the standing §1g placement lane (D14-S1) — its first use folds the s41 probes into "
        "`outputs/_placement_census.py` — and the miner's rows.")
k = find("- **Before r466: no round in flight**"); prior = L[k]; del L[k]
k = find("- LAST SHIPPED: **r465**")
L[k] = L[k].replace("- LAST SHIPPED: **r465** (build 260620.32, 24 Sept ≈14:45,", "- Before it: **r465** (build 260620.32, 24 Sept 14:33,", 1)
assert L[k].startswith("- Before it: **r465**"), L[k][:80]
L.insert(k, "- LAST SHIPPED: **r466** (build 260620.33, 24 Sept ≈14:55, session 42 Round 2 — Chris's D14-20: THE WRITER'S COURSE-CODE "
         "HEADING IS DROPPED, `COURSECODE_OFF`; 18 modules / 22 pages (the MTK introductions + the PNR activity tables); SCOPED, "
         "**scoped #2 since the r460 FULL**, scoped_ship PASS; **skeleton 55.2517 → 55.2654 % @ 2487 (+0.0137pp; 12 up / 0 down)**, "
         "≥50 1575, **≥75 276**, ≥90 25, RAW 39.200 %; cs / body / clean / leak EXACT; `gate_baseline.json` at r466; the miner 197 "
         "CANDIDATE).")
k = find("- Plateau window (§4): **2 of 3** — r465")
L[k] = L[k].replace("- Plateau window (§4): **2 of 3** — r465", "- Plateau window (§4): **2 of 3** — r466 a Chris-decided NAMED "
                    "override (D14-20; +0.0137pp, 12 up / 0 down, ≥75 +1): neither counts nor resets (the r444 / r445 / r447 "
                    "precedent); r465", 1)
k = find("- Standing facts: AppVersion 260620.32")
L[k] = L[k].replace("- Standing facts: AppVersion 260620.32 (r465", "- Standing facts: AppVersion 260620.33 (r466 the course-code "
                    "heading dropped, D14-20 — session 42 Round 2, 24 Sept); before it 260620.32 (r465", 1)
k = find("- **QUEUED BY CHRIS (D14, 24 Sept)")
L[k] = L[k].replace("(2) **D14-20** —", "(2) ~~**D14-20**~~ **DONE r466 (session 42 Round 2)** —", 1)
assert "DONE r466" in L[k], "queued line"
k = find("20. ~~**24 Sept (session 41 Round 1, r453)**")
L[k] = L[k].replace("QUEUED: next session's Round 2.**", "DONE r466 (session 42 Round 2): 18 modules / 22 pages, +0.0137pp, "
                    "12 up / 0 down.**", 1)
assert "DONE r466" in L[k]
k = find("- s42-r1 (engine r465")
L[k] = L[k].replace("24 Sept 14:25 → ≈14:45)", "24 Sept 14:16 → 14:33, real clock)", 1)
k = find("## Round log")
L.insert(k + 1, "- s42-r2 (engine r466, build 260620.33, 24 Sept 14:36 → ≈14:55) · D14-20: THE WRITER'S COURSE-CODE HEADING IS DROPPED "
         "(the bilingual `[H1] TRR900` row — MTK introductions + PNR activity tables) · SHIPPED scoped #2 · 18 modules / 22 pages · "
         "skeleton 55.2517 → 55.2654 (+0.0137pp; 12 up / 0 down), ≥75 +1 · every other gate EXACT · TRR108_0.0's gold `h1` the one "
         "named override (no dip) · plateau 2 of 3 (a decided override: neither).")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r466** (260620.33, "
        "D14-20); LAST FULL = **r460**; ledger scoped #2; plateau **2 of 3**; 2,487 pairs. Chris's D14 queue DONE; next: the §1g "
        "placement census (D14-S1) and the miner's rows. Needs Chris #17–#19.")
marker = marker.replace("24 Sept 15:05 NZST", "24 Sept 14:36 NZST (real clock)")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Session 42 — Round 2 PICK (engine r466) + what shipped\n\n" + marker + "\n" + prior + "\n"
    "- **What shipped (r466, 260620.33):** `BilingualBuilder.bilingualRows` drops a rendered heading whose whole text is a course / "
    "module code at the r330 section-id seam (`courseCodeStripRe`; data `dual_language.section_grouping.course_code_heading`, env "
    "`COURSECODE_OFF`). Census: Claude 22 pages / 18 modules (15 intro-type pages + 8 PNR lesson pages … the PNR tables open every "
    "activity with `[H1] TRR900`), gold 0 bare-code h2–h6 on every Bilingual page. Probe OFF 3217 identical / ON exactly the census; "
    "12 up / 0 down, +34.2 pp-sum; scoped_ship PASS. Evidence: `outputs/_r466_prescore.log`, `_r466_skdelta.log`, `_r466_scoped_ship.log`.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
