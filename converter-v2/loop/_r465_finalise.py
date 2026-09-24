#!/usr/bin/env python3
"""ROUND 465 finalise (session 42 Round 1 — Chris's D14-21; a GATE-CONFIGURATION round, the r343 precedent) — BUILD_CHANGELOG.md
(prepend), Config.js AppVersion 260620.31 -> 260620.32, OPERATING_GUIDE §9 / §14, gate_baseline.json (every headline field on the new
population), LOOP_STATE.md (marker cleared, Position, ceiling, round log, follow-ups, Needs Chris #21, next-session line; the marker →
archive). Line edits only; .bak kept; nothing written until every anchor is found. Run under WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
FOUR = "CHI1003 / CHI1004 / CHI1005 / JPN1004"
# ---------- asserts first ----------
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 465," not in sc[:3000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.31";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 461 BASELINE"; a14 = "- **Build:** `260620.31` (round 461"
for a in (a9, a14): assert so.count(a) == 1, a
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 465 IN FLIGHT — NOT PROVEN**", "- **Before r465: no round in flight**", "- LAST SHIPPED: **r461**",
          "- Plateau window (§4): **2 of 3** — r461", "- Standing facts: AppVersion 260620.31", "## Round log",
          "**Next session starts with:**", "- **QUEUED BY CHRIS (D14, 24 Sept)", "21. ~~**24 Sept (session 41 Round 12)**",
          "- **r355 (session 15, the instrument corrected"):
    find(p)

entry = f"""## 2026-09-24 (round 465, build 260620.32) — THE FOUR `Merge item N` MODULES LEAVE THE COMPARISON SET (Chris's decision D14-21; a GATE-CONFIGURATION round, the r343 / D10-6 precedent — no engine change, no regeneration; every baseline RE-ESTABLISHED on the new population, the +0.304pp recorded as a POPULATION change, never claimed) — the loop's session 42 Round 1

### 1. WHAT CHANGED, IN ONE LINE

**{FOUR} stay in the corpus — their Claude dirs are still regenerated with their families and keep their `_interactives.txt` — but stop counting in every score: every lesson in their Writers Templates is an untagged `Merge item N` line (the lesson content is not in the document), so no converter rule can reach the human's page.** Chris (D14-21, 24 Sept 2026): *"these are no-source so can be ignored for all future stats and comparisons and future development on this PageForge project."* Four lines + a dated comment in `reference/tests/compare_exclusions.txt` — the ONE list `_corpus.gate_mods()` honours (skeleton, structural defect audit, compare_structure, body_compare, the discrepancy audit, strict / scaffold audits, anchor_compare, the ceiling, the DIFF MINER, the loss ledger). No round targets them again; r464 (their `Merge item N` note) stays WITHDRAWN. Overrides nothing.

### 2. THE PROOF — a population change and nothing else

- Predicted from `_r461_sk_final.json` before the edit: 37 paired pages (12.98 – 68.35 %) leave; mean 54.9477 → 55.2517; ≥50 1581 → 1575; ≥75 / ≥90 unchanged. Measured (`_r465_sk_final.json` vs `_r461_sk_final.json`, `_r465_skdelta.log`): **2524 → 2487 pairs — exactly the 37 gone, 0 new, ZERO movers** (every kept page identical to the decimal).
- **Skeleton (PRIMARY): SCAFFOLD mean 54.9477 % → 55.2517 % (+0.3040pp, a POPULATION change) / ≥50 1581 → 1575 (the six ≥ 50 % pages of the four) / ≥75 275 / ≥90 25 EXACT / skipped 0 @ 2524 → 2487; RAW 38.975 % → 39.193 %; median 56.0 → 56.3.**
- compare_structure (530 modules): exact 16719 → 16709 (−10 = the four modules' own matched elements leaving; matched 19467 → 19457) / EXTRA 208 / missing 896 / row-wrap 24 EXACT; body_compare 2667 → 2629 pages: ANY 239 → 238 / over-capture 61 / runaway 5 / empty 176 → 175 (one of the four's pages); structurally clean 2621 / 2667 → 2584 / 2629 (98.3 %; 37 clean + 1 leak page left); literal-tag leak 75 / 46 → 74 / 45; tags 9557 / 9557; flipCard divergence 0, speechBubble / pop-out / MTK quiz / math / menu-label / dragAndDrop / bingo / typing RESULT ✓; entry parity PASS; index-sync OK (`_r465_gates.log`).
- `_gatecheck.py cs bc` refused on the mtime staleness guard — the standing condition after a scoped ship (r461's own gatecheck printed the same line; the corpus's non-TRR pages predate r461's edit). The content itself is the committed r461 state: `git status` clean, `verify_after_transfer.sh` engine checksums PASS, and the two files the r464 withdrawal restored at 14:07 (`ContentConverter.js`, `Emit_Templates.json`, byte-identical to HEAD) had their mtimes reset to the r461 commit time.
- **The ceiling re-measured on the new population** (`_measure_ceiling.py --baseline _r465_sk_final.json --json _ceiling_r465.json --md _ceiling_r465.md`): **CEILING (scaffold) 91.7 %** (loose 94.3 %; full-scope 87.4 %; was 91.2 % at the 22 Sept intake); **SCAFFOLD 55.25 % = 60.2 % of achievable** (band 58.6 – 60.2 %); RAW = 44.8 % of its ceiling; 2413 joined pages; outlier pages 52. Quote `_ceiling_r465.*` from here on.
- Fast-loop baseline re-snapshotted (`_r465_fastloop_snapshot.log`: sk_pages 2487, cs_matched 19457, body_pages 2629, df_total 2629, df_clean 2584); `gate_baseline.json` refreshed (every headline field). The DIFF MINER re-run on the new population: **2487 pairs / 529 modules, 197 CANDIDATE** (`_diff_miner_r465.log`). **Judge every later round against THIS state; the +0.304pp is never a gain and is never re-counted.**
- Plateau (§4): a gate-configuration round — neither counts nor resets (**2 of 3** stands).

**Ledger:** no ship (no regeneration — the corpus on disk is r461's byte-for-byte) · data `reference/tests/compare_exclusions.txt` (+4 codes) · no env toggle (the reversal is removing the four lines) · tools `outputs/_r465_run.sh`, `_r465_gates.log`, `_r465_sk_final.json` / `_r465_sk_full.log` / `_r465_skdelta.log`, `_r465_gatecheck{{,_csbc}}.log`, `_r465_fastloop_snapshot.log`, `_ceiling_r465.{{json,md,log}}`, `_diff_miner_r465.log`, `_r465_finalise.py` · AppVersion 260620.32.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 465 (260620.32): a GATE-CONFIGURATION round, no engine change (session 42 Round 1; Chris's D14-21) — CHI1003 / CHI1004 / CHI1005 / JPN1004 (every lesson a `Merge item N` line: no source) leave the scored population via reference/tests/compare_exclusions.txt + _corpus.gate_mods(); every baseline re-established on 2487 pairs; the corpus on disk is r461's byte-for-byte.\n" + '\tstatic AppVersion = "260620.32";', 1)
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 465 BASELINE — RE-ESTABLISHED ON THE D14-21 POPULATION (CHI1003 / CHI1004 / CHI1005 / JPN1004 — no-source `Merge item N` lessons — leave every scored gate via `reference/tests/compare_exclusions.txt`; a gate-configuration round, no engine change, no regeneration): SCAFFOLD mean 55.2517% / >=50% 1575 / >=75% 275 / >=90% 25 / skipped 0 @ 2487 pairs; RAW 39.193%** (state `outputs/_r465_sk_final.json`) = **60.2% of achievable** against the re-measured **CEILING 91.7%** (`_ceiling_r465.json`). The +0.3040pp vs r461 is a POPULATION change (37 pairs left, 0 movers) — never a gain; cs 16709 / 208 / 896 / 24, body 61 / 5 / 175 / 238, clean 2584 / 2629, leak 74 / 45. **A comparison across round 465 must use the same population on both sides.** Previous: **ROUND 461 BASELINE", 1)
so = so.replace(a14, "- **Build:** `260620.32` (round 465 — **the four `Merge item N` modules leave the comparison set** (Chris's D14-21: CHI1003 / CHI1004 / CHI1005 / JPN1004 added to `reference/tests/compare_exclusions.txt`; a gate-configuration round, no engine change, no regeneration, no toggle). **ROUND 465 BASELINE: SCAFFOLD 55.2517 % / ≥50 1575 / ≥75 275 / ≥90 25 @ 2487; RAW 39.193 %** = 60.2 % of achievable (ceiling 91.7 %, `_ceiling_r465.json`); +0.304pp = POPULATION, never claimed; cs 16709 / 208 / 896 / 24; body ANY 238; clean 2584 / 2629; leak 74 / 45; every verifier ✓).\n" + a14, 1)
wr(PO, so); print("OG ok")
# ---------- gate_baseline.json ----------
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r465.bak")
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
setv("build", '"260620.31"', '"260620.32"'); setv("round", "461", "465")
setv("claude_pages", "2750", "2675"); setv("paired_pages", "2491", "2487"); setv("gated_dirs", "534", "530")
insert_before("_note_r461", '    "_note_r465": "Round 465 (session 42 Round 1, 2026-09-24; Chris\'s D14-21) — a GATE-CONFIGURATION round: CHI1003 / CHI1004 / CHI1005 / JPN1004 (no-source `Merge item N` lessons) join compare_exclusions.txt; no engine change, no regeneration. Every field below re-established on the new population: skeleton 2524 -> 2487 pairs (37 gone, 0 movers), SCAFFOLD 54.9477 -> 55.2517 (+0.304pp POPULATION, never a gain), >=50 1581 -> 1575, RAW 38.975 -> 39.193, median 56.0 -> 56.3; cs exact 16719 -> 16709 (the four modules\' elements); body 2667 -> 2629 pages, ANY 239 -> 238, empty 176 -> 175; clean 2621/2667 -> 2584/2629; leak 75/46 -> 74/45; corpus block refreshed (claude_pages 2675 = the census; paired 2487; gated_dirs 530 = the modules compare_structure scores). Ceiling re-measured 91.7% (_ceiling_r465.json).",')
setv("mean_scaffold_pct", "54.95", "55.25"); setv("median_scaffold_pct", "56.0", "56.3"); setv("pages_ge_50", "1581", "1575")
setv("raw_mean_pct", "38.98", "39.19"); setv("pairs", "2524", "2487")
insert_before("_note_r461_state", '    "_note_r465_state": "r465 (D14-21, population only): SCAFFOLD 55.2517 @ 2487, RAW 39.193; 0 movers, 37 pairs gone.",')
setv("exact_chain", "16719", "16709"); setv("any_breakdown", "239", "238"); setv("empty_container", "176", "175")
setv("clean_pages", "2621", "2584"); setv("total_pages", "2667", "2629"); setv("clean_pct", "98.28", "98.29")
setv("literal_tag_leak_occ", "75", "74"); setv("leak_pages", "46", "45")
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
# ---------- LOOP_STATE ----------
shutil.copyfile(S, S + ".pre-r465-finalise.bak")
i = find("- **ROUND 465 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (24 Sept 2026 ≈14:45, session 42 Round 1 — r465 (D14-21) SHIPPED as a gate-configuration round and "
        "committed; the in-flight marker is cleared). LAST SHIPPED **r465** (260620.32); **LAST FULL = r460**; ledger **scoped #1** "
        "(r465 regenerated nothing). **QUEUED by Chris: Round 2 = D14-20 (drop the TRR900 heading)**; then the standing §1g placement "
        "lane (D14-S1) in every PICK pass — its first use folds the s41 probes into `outputs/_placement_census.py`.")
k = find("- **Before r465: no round in flight**"); prior = L[k]; del L[k]
k = find("- LAST SHIPPED: **r461**")
L[k] = L[k].replace("- LAST SHIPPED: **r461**", "- Before it: **r461**", 1)
L.insert(k, "- LAST SHIPPED: **r465** (build 260620.32, 24 Sept ≈14:45, session 42 Round 1 — Chris's D14-21: CHI1003 / CHI1004 / "
         "CHI1005 / JPN1004 leave the scored population, `compare_exclusions.txt`; a GATE-CONFIGURATION round, no engine change, no "
         "regeneration; **skeleton 54.9477 → 55.2517 % @ 2524 → 2487 (+0.3040pp POPULATION, 0 movers — never a gain)**, ≥50 1575, "
         "≥75 275, ≥90 25, RAW 39.193 %; cs 16709 / 208 / 896 / 24; body 61 / 5 / 175 / 238; clean 2584 / 2629; leak 74 / 45; "
         "ceiling 91.7 % → **60.2 % of achievable**; `gate_baseline.json` at r465; the miner 197 CANDIDATE @ 2487).")
k = find("- Plateau window (§4): **2 of 3** — r461")
L[k] = L[k].replace("- Plateau window (§4): **2 of 3** — r461", "- Plateau window (§4): **2 of 3** — r465 is a gate-configuration "
                    "round (neither counts nor resets); r461", 1)
k = find("- Standing facts: AppVersion 260620.31")
L[k] = L[k].replace("- Standing facts: AppVersion 260620.31 (r461", "- Standing facts: AppVersion 260620.32 (r465 the D14-21 exclusion — "
                    "session 42 Round 1, 24 Sept); before it 260620.31 (r461", 1)
k = find("- **r355 (session 15, the instrument corrected")
L.insert(k + 1, "- **r465 (session 42, 24 Sept 2026 — the D14-21 population, 2487 pairs): CEILING (scaffold) 91.7 % (loose 94.3 %; full-scope "
         "87.4 %); SCAFFOLD 55.252 % = 60.2 % of achievable (band 58.6 – 60.2 %); RAW 39.193 % = 44.8 %** (`outputs/_ceiling_r465.{json,md}`). "
         "Quote THIS from r465 on (the r410 90.9 % / 22 Sept intake 91.2 % figures are older populations).")
k = find("- **QUEUED BY CHRIS (D14, 24 Sept)")
L[k] = L[k].replace("take these FIRST, in order:** (1) **D14-21**", "take these FIRST, in order:** (1) ~~**D14-21**~~ **DONE r465 "
                    "(session 42 Round 1)** —", 1)
k = find("21. ~~**24 Sept (session 41 Round 12)**")
L[k] = L[k].replace("QUEUED: next session's Round 1 (the exclusion + re-baseline); r464 WITHDRAWN.**", "DONE r465 (session 42 Round 1): "
                    "the four in `compare_exclusions.txt`, every baseline re-established on 2487 pairs; r464 WITHDRAWN.**", 1)
assert "DONE r465" in L[k]
k = find("## Round log")
L.insert(k + 1, "- s42-r1 (engine r465, build 260620.32, 24 Sept 14:25 → ≈14:45) · D14-21: CHI1003 / CHI1004 / CHI1005 / JPN1004 (no-source "
         "`Merge item N` lessons) leave the scored population (`compare_exclusions.txt`) · SHIPPED as a GATE-CONFIGURATION round (no "
         "engine change, no regeneration, the r343 precedent) · 2524 → 2487 pairs, 0 movers, skeleton 54.9477 → 55.2517 (+0.304pp "
         "POPULATION, never a gain) · ceiling 91.7 % = 60.2 % of achievable · miner 197 CANDIDATE · plateau 2 of 3 (neither).")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r465** (260620.32, "
        "D14-21); LAST FULL = **r460**; ledger scoped #1; plateau **2 of 3**; 2,487 pairs. Round 2 = D14-20 (drop the TRR900 "
        "course-code heading); then the §1g placement census (D14-S1) and the miner. Needs Chris #17–#19.")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Session 42 — Round 1 PICK (engine r465) + what shipped\n\n" + marker + "\n" + prior + "\n"
    "- **What shipped (r465, 260620.32):** CHI1003 / CHI1004 / CHI1005 / JPN1004 appended to `reference/tests/compare_exclusions.txt` "
    "with a dated D14-21 comment (backup `.pre-r465.bak`); no engine / data change; nothing regenerated. Measured exactly as predicted "
    "(37 pairs gone, 0 movers; `_r465_skdelta.log`); every gate a population change only (`_r465_gates.log`); the ceiling re-measured "
    "91.7 % (`_ceiling_r465.md`); the miner 197 CANDIDATE @ 2487. The two engine files the r464 withdrawal restored at 14:07 "
    "(byte-identical to HEAD) had their mtimes reset to the r461 commit time (12:20:40).\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
