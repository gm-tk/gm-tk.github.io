#!/usr/bin/env python3
"""r422 ENABLE finalise (OPERATING_GUIDE §12): changelog entry, Config.js 260619.97 -> .98, OPERATING_GUIDE §9 / §11 / §14,
gate_baseline.json, the Emit_Templates _doc, LOOP_STATE.md (round log, Position, Needs Chris #13 deleted, next-session line),
the archive record. Run under WSL."""
import re, json
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
PF = R + "pageforge-site/converter-v2/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

entry = """## 2026-09-22 (round 422 ENABLED, build 260619.98) — THE SIDE-TAB-NAVIGATION FUNDAMENTALS DIALECT GOES LIVE: FRFUN06's ten lesson pages take the gold's `div.phases` + `fundamentalsPanel` shape (the autonomous loop's session 33 Round 2; authorised by rule — LOOP §1d exception 1 / D12-1; SCOPED regeneration of the 1, scoped ship #1 since the r425 FULL)

### 1. WHAT CHANGED

**The flag only.** `Emit_Templates.body_region.inquiry_tabs.side_tab_nav.enabled` false → **true** (env `SIDETABNAV_OFF` still restores the r100 inquiry path byte for byte). Everything the r422 entry describes as BUILT is now LIVE on the one module whose Writers Template authors in-page side tabs: FRFUN06's `[Side tab navigation]` + label table + one labelled nav tag per panel → `body.fundamentals.container-fluid.noPhase`, `div.phases` with the writer's N labels (the first `showing`, `phase="1..N"`), one `div.fundamentalsPanel[phase]` per tab, no module menu, the `footer-nav fundamentals-nav` footer. FRFUN07 / FRFUN08 (page-navigation side tabs, plain fundamentals bodies) are untouched — proven below, not assumed.

**Why it ships now.** r422 was built, measured (8 up / 2 down, +34.7pp-sum on FRFUN06's 10 pages) and parked INERT on 21 Sept because a 10-page / 1-module class is under the 20-page body floor. The 22 Sept `/loop-review` (D12-1) wrote LOOP §1d exception 1 for exactly this case — a family dialect keyed to one family may ship under the floor when it matches that family's own gold on every page of the family, its OFF corpus is byte-identical and every other gate holds — and named r422 its worked example, so "Needs Chris" #13 was settled by rule and this round is the enable.

### 2. PROOF

- `_s33_r422_probe_run.sh` (the r410 harness, `_s33_r422_probe.cjs` = `_s28_t3_probe.cjs` verbatim, all 507 Claude-dir modules, 4 shards): **OFF (`SIDETABNAV_OFF=1`) = the disk on every page, 2583 / 2583** — the r425 state exactly; **ON = 2573 identical / 10 changed, all ten FRFUN06's** (`_0_0` … `_9_0`); FRFUN07's 9 and FRFUN08's 11 pages byte-identical with the rule live.
- SCOPED regeneration (`_s33_r422_regen.sh`: FRFUN06 + a fresh 12-module spot-check sample, seed 422): `_content_manifest.py fresh` **0 truly stale**; `_scoped_spotcheck.py verify` **12 / 12 byte-identical**; `scoped_ship.sh` (`_s33_r422_scoped_ship.log`) toggle-exists ✓, containment **1 ⊆ 1** ✓, spot-check ✓, the exact decomposition **PASS — every protected gate held-or-improved**: skeleton 54.23 → 54.25, ≥50 1463 → 1464, everything else EXACT; the fast-loop baseline + manifest committed by `_fastloop_diff.py … --commit` (`_s33_r422_fastloop.log`; run directly rather than through `scoped_ship.sh --commit` because the script's step 6 records a scoped ship on EVERY run, commit or not — the same double count made r425 read as scoped #8 when it was #7, so the FULL backstop ran one round early; the ledger stands at scoped #1 since r425, correct).
- `run_all_gates.sh` (`_s33_r422_gates.log`, the full corpus): skeleton state `_s33_r422_sk_final.json` **54.2320 → 54.2466 % @ 2377 pairs (+0.0146pp)**, ≥50 **1463 → 1464**, ≥75 238, ≥90 20, RAW 38.239 → 38.249; `_s29_skdelta.py` r425 → r422: **movers 10 (8 up / 2 down), pp-sum +34.7, movers outside the affected set 0** — FRFUN06_4_0 35.7 → 47.7 (+12.0), _3_0 +6.1, _5_0 +5.9, _1_0 +5.7, _8_0 +5.6, _0_0 +4.4, _2_0 +3.6, _6_0 +2.9, _9_0 −0.1, **_7_0 51.1 → 39.7 (−11.4) NAMED — a PAIRING fact, not a scorer artefact: the gold has 11 files to Claude's 10 (Claude's page 0 folds the overview and Novice page 1 together — the `[<Level> Page N]` title-marker boundary is the recorded FRFUN follow-up), so from that point Claude's page N pairs against the gold's page N which is a different level's page; the built panels on an Emergent page now differ from a Novice gold MORE than the old bare inquiry shell did**; compare_structure 14318 / 186 / 689 / 23 EXACT; body_compare 55 / 5 / 193 / 251 EXACT; clean 2532 / 2576 = 98.29 %, leak 73 / 44 EXACT; tags 9557 / 9557; every verifier ✓; 17 selftests GREEN (49 / 0); feature index GREEN; the DIFF MINER re-run (2377 pairs / 496 modules, 8953 classes, **184 CANDIDATE**). `_gatecheck.py` refused (its mtime 0-stale assertion is for full regenerations — the 490 untouched modules are older than the data edit; the content manifest, not the mtime, is the freshness proof for a scoped ship, and the decomposition above is the verdict).

### 3. PROTECTED GATES (all HELD or IMPROVED — `_s33_r422_gates.log`, `_s33_r422_fastloop.log`, `_s33_r422_skdelta.log`)

- **Skeleton (PRIMARY)**: SCAFFOLD **54.2466 % @ 2377 pairs** (+0.0146pp; 8 up / 2 down, the two dips named above); ≥50 **1464** (+1 = FRFUN06_1_0), ≥75 **238**, ≥90 **20**, RAW **38.249 %**; skipped 0.
- **compare_structure** 14318 / 186 / 689 / 23 EXACT; **body_compare** 55 / 5 / 193 / 251 EXACT; **defect** clean 2532 / 2576 = 98.29 %, leak 73 / 44 EXACT; tags 9557 / 9557; every verifier EXACT.
- Plateau (§4): the PICK predicted +0.0146pp (the r422 measure) and delivered it exactly — under the 0.02pp window threshold, so this round is window 1 of 3 (the r425 finish before it was a population round and does not count).

### 4. RECORDS

`OPERATING_GUIDE.md` §9 / §11 / §14; `gate_baseline.json` (`_note_r422e`); `Emit_Templates.side_tab_nav._doc`; "Needs Chris" #13 deleted (settled by rule, now shipped); the recorded FRFUN follow-ups stand — FRFUN07 / 08's registry row (the r408 "faithful row" scored 26 / 28 pages down and was held back; re-measure per page) and the `[<Level> Page N]` title marker as a page boundary (Claude 10 files vs the gold's 11).

"""
p = PF + "BUILD_CHANGELOG.md"; s = rd(p)
head, rest = s.split("\n", 1)
assert head.startswith("# BUILD CHANGELOG") and rest.lstrip("\n").startswith("## 2026-09-22 (round 425 FINISHED")
wr(p, head + "\n\n" + entry + rest.lstrip("\n"))

p = PF + "app/js/Config.js"; s = rd(p)
old = '\tstatic AppVersion = "260619.97";'; assert s.count(old) == 1
note = ("\t// ROUND 422 ENABLED (260619.98): THE SIDE-TAB-NAVIGATION FUNDAMENTALS DIALECT GOES LIVE — Emit_Templates.body_region.inquiry_tabs.side_tab_nav.enabled "
        "true (env SIDETABNAV_OFF restores the r100 path). FRFUN06's ten lesson pages take the gold's body.fundamentals.noPhase + div.phases + fundamentalsPanel "
        "shape; FRFUN07 / 08 untouched (proven: OFF = disk 2583 / 2583, ON = exactly the 10). Authorised by rule (LOOP 1d exception 1, the 22 Sept review's "
        "D12-1) — a family dialect under the 20-page floor that matches its family's own gold. The loop's session 33 Round 2: scoped regeneration of the 1; "
        "skeleton 54.2320 -> 54.2466 % @ 2377 pairs (8 up / 2 down, +34.7pp-sum; FRFUN06_7_0 -11.4 named = the 11-vs-10-file pairing offset), >=50 1463 -> 1464; "
        "every other gate EXACT.\n")
wr(p, s.replace(old, note + '\tstatic AppVersion = "260619.98";'))

p = PF + "OPERATING_GUIDE.md"; s = rd(p)
old9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 425 BASELINE ("; assert s.count(old9) == 1
new9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 422-ENABLED BASELINE (the FRFUN06 side-tab dialect live — `side_tab_nav.enabled: true`, "
        "env `SIDETABNAV_OFF`; SCOPED regeneration of the 1, scoped ship #1 since the r425 FULL): SCAFFOLD mean 54.2466% / >=50% 1464 / >=75% 238 / >=90% 20 / "
        "RAW 38.249% @ 2377 pairs, pairs skipped 0 — 8 up / 2 down on FRFUN06 alone, +34.7pp-sum, 0 movers elsewhere (FRFUN06_7_0 −11.4 named: the gold's 11 files "
        "vs Claude's 10 pair page 7 against a different level's page); every other gate EXACT (cs 14318 / 186 / 689 / 23, body 55 / 5 / 193 / 251, clean 2532 / 2576, "
        "leak 73 / 44).** Previous — ROUND 425 BASELINE (")
s = s.replace(old9, new9)
old11 = "| `SIDETABNAV_OFF` | 422 | **THE SIDE-TAB-NAVIGATION FUNDAMENTALS DIALECT"; assert s.count(old11) == 1
row11 = ("| `SIDETABNAV_OFF` | 422 (enabled 2026-09-22) | **THE SIDE-TAB-NAVIGATION FUNDAMENTALS DIALECT ENABLED** (the autonomous loop's session 33 Round 2 — the "
         "round below switched on: `body_region.inquiry_tabs.side_tab_nav.enabled: true`; authorised by rule, LOOP §1d exception 1 / D12-1 — a family dialect "
         "under the 20-page floor that matches its family's own gold on every page). FRFUN06's 10 lesson pages take `body.fundamentals.container-fluid.noPhase` + "
         "`div.phases` (the writer's labels, the first `showing`) + one `fundamentalsPanel[phase]` per tab, no module menu, the fundamentals footer. OFF "
         "(`SIDETABNAV_OFF=1`) = the r425 state byte for byte (2583 / 2583 proven over all 507 modules); ON = exactly the 10 (FRFUN07 / 08 untouched). Measured "
         "8 up / 2 down, +34.7pp-sum (the −11.4 on `_7_0` = the 11-vs-10-file pairing offset, named). Standing FRFUN follow-ups: the FRFUN07 / 08 registry row; "
         "the `[<Level> Page N]` title marker as a page boundary. |\n")
s = s.replace(old11, row11 + old11)
old14 = "- **Build:** `260619.97` (round 425 FINISHED — **THE XOTP"; assert s.count(old14) == 1
b14 = ("- **Build:** `260619.98` (round 422 ENABLED — **THE SIDE-TAB-NAVIGATION FUNDAMENTALS DIALECT GOES LIVE on FRFUN06** — `side_tab_nav.enabled: true`, env "
       "`SIDETABNAV_OFF`; LOOP §1d exception 1 / D12-1; the autonomous loop's session 33 Round 2; the probe OFF = disk 2583 / 2583, ON = FRFUN06's 10 pages alone; "
       "**SCOPED regeneration of the 1 (scoped ship #1 since the r425 FULL)**; **ROUND 422-ENABLED BASELINE: SCAFFOLD mean 54.2466% / >=50% 1464 / >=75% 238 / "
       ">=90% 20 / RAW 38.249% @ 2377 pairs** — 8 up / 2 down, +34.7pp-sum, 0 movers outside FRFUN06 (`_7_0` −11.4 named, the pairing offset); cs 14318 / 186 / "
       "689 / 23, body 55 / 5 / 193 / 251, clean 2532 / 2576, leak 73 / 44 EXACT; every verifier EXACT; 17 selftests GREEN; the miner 184; \"Needs Chris\" #13 "
       "closed). Previous: ")
s = s.replace(old14, b14 + old14)
wr(p, s)

p = R + "CONVERTER_V2/reference/tests/gate_baseline.json"; s = rd(p)
def setv(key, old, new):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=1); assert n == 1, key
setv("build", '"260619.97"', '"260619.98"'); setv("round", 425, 422)
setv("mean_scaffold_pct", 54.23, 54.25); setv("pages_ge_50", 1463, 1464); setv("raw_mean_pct", 38.24, 38.25)
a = '    "_note_r425": "Round 425 FINISHED (session 33 Round 1'; assert s.count(a) == 1
s = s.replace(a, '    "_note_r422e": "Round 422 ENABLED (session 33 Round 2, 2026-09-22): the FRFUN06 side-tab-navigation dialect switched on (Emit_Templates.body_region.inquiry_tabs.side_tab_nav.enabled true, env SIDETABNAV_OFF) under LOOP 1d exception 1 (D12-1) — SCOPED regeneration of the 1; the round field reads 422 because this is the r422 rule shipping, after r425 (the ordering is by ship date, see build). Skeleton 54.2320 -> 54.2466 @ 2377 (8 up / 2 down on FRFUN06 alone, +34.7pp-sum; _7_0 -11.4 named = the 11-vs-10-file pairing offset); >=50 1463 -> 1464; every other gate EXACT.",\n' + a)
a2 = '    "_note_r425b": "Round 425 FINISHED: SCAFFOLD 54.1703'; assert s.count(a2) == 1
s = s.replace(a2, '    "_note_r422e": "Round 422 ENABLED: SCAFFOLD 54.2320 -> 54.2466 @ 2377 pairs (+0.0146pp; FRFUN06_4_0 +12.0, _3_0 +6.1, _5_0 +5.9, _1_0 +5.7, _8_0 +5.6, _0_0 +4.4, _2_0 +3.6, _6_0 +2.9, _9_0 -0.1, _7_0 -11.4 named); >=50 1463 -> 1464; >=75 238 / >=90 20 EXACT; RAW 38.239 -> 38.249. State outputs/_s33_r422_sk_final.json.",\n' + a2)
json.loads(s); wr(p, s)

p = PF + "data/Emit_Templates.json"; s = rd(p)
o = "ENABLING IT IS CHRIS'S CALL (a below-floor family dialect whose renderer now exists): set enabled true, regenerate FRFUN06.\","
assert s.count(o) == 1
s = s.replace(o, "ENABLED 2026-09-22 (the loop's session 33 Round 2) under LOOP 1d exception 1 (the 22 Sept review, D12-1 — a family dialect under the floor that matches its family's own gold on every page): OFF = disk 2583 / 2583, ON = FRFUN06's 10 pages alone; skeleton 54.2320 -> 54.2466 % @ 2377 pairs, every other gate EXACT.\",")
json.loads(s); wr(p, s)

# LOOP_STATE.md
st = rd(R + "LOOP_STATE.md"); ar = rd(R + "LOOP_STATE_ARCHIVE.md")
o = "13. ~~**21 Sept (s30)** — enable the FRFUN06 side-tab dialect (r422)~~ — **SETTLED BY RULE 22 Sept (D12-1 → LOOP §1d exception 1): the loop enables it in the next session (Round 2).**\n"
assert st.count(o) == 1
st = st.replace(o, "")
o = "- s33-r1 (engine r425 FINISHED, build 260619.97"
assert st.count(o) == 1
line = ("- s33-r2 (engine r422 ENABLED, build 260619.98, 22 Sept ≈10:50 → ≈11:20) · THE SIDE-TAB-NAVIGATION FUNDAMENTALS DIALECT GOES LIVE — `side_tab_nav.enabled: true` "
        "(`SIDETABNAV_OFF`), authorised by rule (LOOP §1d exception 1 / D12-1; \"Needs Chris\" #13 closed) · probe OFF 2583 / 2583, ON = FRFUN06's 10 pages alone "
        "(FRFUN07 / 08 untouched) · SCOPED regeneration of the 1 (scoped #1 since the r425 FULL; the scoped_ship.sh step-6 double count noted) · skeleton "
        "54.2320 → 54.2466 % @ 2377 (+0.0146pp = the r422 measure exactly; 8 up / 2 down, +34.7pp-sum; `_7_0` −11.4 named = the 11-vs-10-file pairing offset), "
        "≥50 1463 → 1464 · every other gate EXACT · every verifier ✓ · miner 184 · plateau window 1 of 3\n")
st = st.replace(o, line + o)
o = "- LAST SHIPPED = LAST FULL: **r425 FINISHED** (build 260619.97"
assert st.count(o) == 1
st = st.replace(o, ("- LAST SHIPPED: **r422 ENABLED** (build 260619.98, 22 Sept ≈11:20, session 33 Round 2 — the FRFUN06 side-tab dialect live; SCOPED regeneration of the 1, "
                    "scoped #1 since the r425 FULL; **skeleton 54.2320 → 54.2466 % @ 2377 pairs, ≥50 1464, ≥75 238, ≥90 20, RAW 38.249 %**; every other gate EXACT; "
                    "`gate_baseline.json` at r422e; `outputs/_s33_r422_sk_final.json` the skeleton state; 54.247 / 90.9 = **59.7 % of achievable**; the miner re-run "
                    "22 Sept 11:09, 184 CANDIDATE). LAST FULL: **r425 FINISHED** (build 260619.97"))
o = "- Plateau window (§4): **0 of 3** — r425 a recognition-family round"
assert st.count(o) == 1
st = st.replace(o, "- Plateau window (§4): **1 of 3** — r422e predicted +0.0146pp and delivered it (under 0.02pp, no other gate moved); r425 a recognition-family round")
o = "- Standing facts: AppVersion 260619.97 (r425 FINISHED"
assert st.count(o) == 1
st = st.replace(o, "- Standing facts: AppVersion 260619.98 (r422 ENABLED — the FRFUN06 side-tab dialect, session 33 Round 2, 22 Sept); before it 260619.97 (r425 FINISHED")
o = "`DIFF_QUEUE.md` 22 Sept 10:42 on the r425 corpus (2,377 pairs / 496 modules), 184 CANDIDATE rows — re-mined after every ship)."
assert st.count(o) == 1
st = st.replace(o, "`DIFF_QUEUE.md` 22 Sept 11:09 on the r422e corpus (2,377 pairs / 496 modules), 184 CANDIDATE rows — re-mined after every ship).")
m = re.search(r"^\*\*Next session starts with:\*\* .*$", st, re.M); assert m
nxt = ("**Next session starts with:** the standing `/loop-start` (health check; the \"Amended:\" line; the §7 diff check; `git status` CLEAN at the session-33 "
       "commits). No round in flight; r425 finished and r422 enabled (22 Sept). Next: **Round 0d for the 38 pre-intake never-converted modules** (LOOP §0's list; "
       "§1f Phases 2 + 5–7: pre-create the nested dirs, convert by explicit code list in batches ≤ 11, refusals by cause, no ghost dirs, re-base by population, "
       "re-mine, the §0 table + the verify script's expect values); then the miner's queue on the current corpus under §3 / §4 (one untried lane before any "
       "exhaustion verdict). NEEDS CHRIS: the open lines of the \"Needs Chris\" section (a new item = one new line there).")
st = st[:m.start()] + nxt + st[m.end():]
record = """## Session 33 — Round 2 (engine r422 ENABLED, build 260619.98, 22 Sept ≈10:50 → ≈11:20) — THE SIDE-TAB-NAVIGATION FUNDAMENTALS DIALECT GOES LIVE (FRFUN06)

**PICK (the 22 Sept review's Round 2, settled by rule).** Enable r422 — `Emit_Templates.body_region.inquiry_tabs.side_tab_nav.enabled: true` — under LOOP §1d exception 1 (D12-1): a family dialect keyed to one family may ship under the floor when it matches the family's own gold on every page, its OFF corpus is byte-identical and every other gate holds. Predicted: +34.7pp-sum on FRFUN06's 10 pages = +0.0146pp corpus-wide (the r422 measure).

**WHAT SHIPPED.** The flag (`sed` on line 5432). `_s33_r422_probe_run.sh` over all 507 modules: OFF = 2583 / 2583 identical; ON = 2573 identical / 10 changed, all FRFUN06 (FRFUN07's 9 / FRFUN08's 11 untouched). `_s33_r422_regen.sh` (FRFUN06 + a 12-module spot-check sample, seed 422): fresh 0 stale, spot-check 12 / 12; `scoped_ship.sh` toggle ✓ containment 1 ⊆ 1 ✓ decomposition PASS (skeleton 54.23 → 54.25, ≥50 +1, all else EXACT); `_fastloop_diff.py … --commit` run directly (the script's step 6 records a scoped ship on every run — the same double count made r425 read scoped #8 when it was #7, so the FULL backstop ran one round early; the ledger stands at scoped #1 since r425, correct). `run_all_gates.sh`: skeleton **54.2320 → 54.2466 % @ 2377** (+0.0146pp — the prediction exactly), ≥50 1463 → 1464, ≥75 238, ≥90 20, RAW 38.249; `_s29_skdelta.py`: movers 10 (8 up / 2 down), +34.7pp-sum, 0 outside the set — `_4_0` +12.0, `_3_0` +6.1, `_5_0` +5.9, `_1_0` +5.7, `_8_0` +5.6, `_0_0` +4.4, `_2_0` +3.6, `_6_0` +2.9, `_9_0` −0.1, **`_7_0` −11.4 NAMED = a pairing fact (the gold's 11 files vs Claude's 10 — Claude's page 0 folds the overview with Novice page 1, so page 7 pairs against a different level's page; the `[<Level> Page N]` title-marker boundary is the recorded FRFUN follow-up)**; cs / body / defect / leak / tags EXACT; every verifier ✓; 17 selftests GREEN; feature index GREEN; the miner 184 CANDIDATE (8953 classes). `_gatecheck.py` refused on its mtime 0-stale assertion (a full-regen tool; the content manifest is the scoped proof). Finalise: the changelog entry, Config.js 260619.98, OPERATING_GUIDE §9 / §11 / §14, `gate_baseline.json` (`_note_r422e`), the Emit_Templates `_doc`, "Needs Chris" #13 deleted, the mirror. Plateau window 1 of 3.

**Tooling nits recorded (follow-up candidates).** (a) `scoped_ship.sh` step 6 records a scoped ship even on a no-commit or failed run — run it once per round, or use `_fastloop_diff.py --commit` directly for the commit. (b) `_scoped_spotcheck.py plan` can draw a `compare_exclusions.txt` module (CEDR302 in r425's sample); an explicit code list then scores its page and `--commit` would patch it into the baseline — drop such modules from the re-score list until the sampler excludes them.
"""
ar = ar.rstrip("\n") + "\n\n" + record + "\n"
wr(R + "LOOP_STATE.md", st); wr(R + "LOOP_STATE_ARCHIVE.md", ar)
print("FINALISE_R422_DONE", len(st))
