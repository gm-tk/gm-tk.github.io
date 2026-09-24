#!/usr/bin/env python3
"""ROUND 470 finalise (session 42 Round 8 — the table-cell title bar recognises the Writers Template: TRR115 converts, TABLETBWT_OFF) —
BUILD_CHANGELOG.md (prepend), Config.js AppVersion 260620.34 -> 260620.35, OPERATING_GUIDE §9 / §11 / §14, gate_baseline.json (every
headline field: the four new pairs), LOOP_STATE.md (marker cleared, Position, plateau, round log, next-session line; the marker →
archive). Line edits only; .bak kept; nothing written until every anchor is found. Run under WSL."""
import io, os, json, shutil, statistics
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
SK = json.load(open(os.path.join(ROOT, "CONVERTER_V2", "outputs", "_r470_sk_final.json")))
MED = round(statistics.median([p["scaffold"] for p in SK["per_page"]]) * 100, 1)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 470," not in sc[:3000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.34";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 467 BASELINE"; a11 = "| `STDTAB_OFF` | 467 |"; a14 = "- **Build:** `260620.34` (round 467"
for a in (a9, a11, a14): assert so.count(a) == 1, a
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 470 IN FLIGHT — NOT PROVEN**", "- **Before r470: no round in flight**", "- LAST SHIPPED: **r467**",
          "- Plateau window (§4): **2 of 3** — r467", "- Standing facts: AppVersion 260620.34", "## Round log", "**Next session starts with:**"):
    find(p)
entry = f"""## 2026-09-24 (round 470, build 260620.35) — THE TABLE-CELL TITLE BAR RECOGNISES THE WRITERS TEMPLATE: TRR115 CONVERTS — a Writers Template that types every tag, its `[TITLE BAR]` included, inside bilingual table cells is no longer refused as "no Writers Template" — the loop's session 42 Round 8 (the recognition / no-build lane)

### 1. WHAT CHANGED

**The find** (the recognition / no-build lane — the three Claude dirs holding only a `_run.json`): TRR104 / TRR105 have no Writers Template (a Media List only — correct refusals); **TRR115 holds a real Writers Template** (`TRR115 Writers Template.docx`, 146 red tags, the MTK bilingual form) but was refused `no Writers Template (no content opener found)` — on today's engine too (`prep refused (no-wt)`). `DocxExtractor.LooksLikeWritersTemplate` reads PARAGRAPH-level red tags only (a content-start, or a fallback directive), and TRR115 types every tag inside bilingual table cells — its `[TITLE BAR]` included (`│ [TITLE BAR] ║ [TITLE BAR] ║`, then the Overview / Strand / Dispositions / Key objectives / Critical point / Learning intentions tables). So the module was refused before r453's table-cell title-bar opener (`content_start.table_title_bar_opener`) could open it.

**The fix** (`DocxExtractor.LooksLikeWritersTemplate`; data `Input_Doc_Rules.content_start.table_title_bar_opener.recognise_wt` {{enabled, env}}; env **`TABLETBWT_OFF`**, byte-identical OFF): after the paragraph checks, a TABLE block holding a cell whose red span resolves to `title bar` identifies the Writers Template — r453's own predicate (it is also off whenever `TABLETB_OFF` is). The module then opens at that table exactly as r453 opens TRR102–116.

### 2. PROOF

- In-memory A/B over all 545 modules (`outputs/_s42_probe_run.sh r470`): **OFF 3217 / 3217 identical; ON 0 existing pages changed + TRR115's 5 new outputs** (4 pages + `TRR115_interactives.txt`).
- Regeneration of TRR115 + the 12-module spot-check (`_r470_regen.sh`): 0 truly stale, spot-check 12 / 12 byte-identical. The scoped ship's decomposition flagged the NEW MODULE's own figures (`_r470_scoped_ship.log`); committed NAMED with `_fastloop_diff.py --accept-named` (the r453 precedent, `_r470_fastloop_named.log`; `outputs/_r470_commit_named.sh`).
- **Population split (§1e):** the pre-existing 2,487 pairs are byte-identical (0 movers, `_r470_skdelta.log`); the new batch = TRR115's four pairs: **TRR115_0_0 55.4 %, _1_0 23.7 %, _2_0 18.6 %, _3_0 21.2 %** (mean 29.7 % — the TRR lesson pages' known level, the r453 follow-up).

### 3. PROTECTED GATES (every movement is TRR115's own new pages — NAMED)

- Skeleton **55.2654 % @ 2487 → 55.2245 % @ 2491 (−0.0410pp = the four new pairs entering below the mean; the pre-existing pairs EXACT)**; **≥50 1575 → 1576** (TRR115_0_0), ≥75 276, ≥90 25; RAW 39.216 → 39.194; median {MED}.
- compare_structure (531 modules): matched 19457 → 19530; **exact 16709 → 16757 (+48)**; EXTRA 208; **missing 896 → 903 (+7, all on TRR115's newly compared elements)**; row-wrap 24. body_compare 2629 → 2633 pages, ANY 238 / over 61 / runaway 5 / empty 175 EXACT. Structurally clean 2584 / 2629 → **2587 / 2633** (3 of the 4 new pages clean); **literal-tag leak 74 / 45 → 75 / 46 (+1 NAMED: TRR115_1_0 — the writer's own BLACK `[Answer: A]` annotation inside an untagged quiz typed as plain bullets, not a red tag)**; tags 9557; every verifier ✓; selftests 50 PASS / 0 FAIL; feature index GREEN; the miner 197 CANDIDATE @ 2491.
- Census: Claude pages 2675 → **2679** (`_MIGRATION/verify_after_transfer.sh` line 78, `.pre-r470.bak`; LOOP §0).
- Plateau (§4): a recognition round — neither counts nor resets: **2 of 3** stands.

**Ledger:** scoped #4 since the r460 FULL · data `Input_Doc_Rules.content_start.table_title_bar_opener.recognise_wt` · env `TABLETBWT_OFF` · code `DocxExtractor.LooksLikeWritersTemplate` · tools `outputs/_r470_{{regen,postship,commit_named,checksums}}.sh`, `_r470_finalise.py`, `_r470_{{scoped_ship,fastloop_named,gates,sk_full,skdelta,selftests,index}}.log`, `_r470_sk_final.json`, `_affected_r470.txt` · AppVersion 260620.35.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 470 (260620.35): THE TABLE-CELL TITLE BAR RECOGNISES THE WRITERS TEMPLATE (session 42 Round 8; the recognition lane). DocxExtractor.LooksLikeWritersTemplate also accepts a table cell whose red span resolves to 'title bar' (r453's predicate), so TRR115 — every tag typed inside bilingual table cells — is no longer refused as 'no Writers Template'. Input_Doc_Rules content_start.table_title_bar_opener.recognise_wt, env TABLETBWT_OFF; TRR115 converts (4 pages); the pre-existing 2487 pairs byte-identical.\n" + '\tstatic AppVersion = "260620.35";', 1)
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 470 BASELINE (TRR115 converts — the table-cell title bar recognises the Writers Template, `TABLETBWT_OFF`; SCOPED, scoped #4 since the r460 FULL): SCAFFOLD mean 55.2245% / >=50% 1576 / >=75% 276 / >=90% 25 / RAW 39.194% @ 2491 pairs — −0.0410pp = TRR115's four new pairs (mean 29.7 %) entering below the mean; the pre-existing 2487 pairs EXACT; cs 16757 / 208 / 903 / 24, body 61 / 5 / 175 / 238, clean 2587 / 2633, leak 75 / 46 (+1 NAMED: TRR115_1_0's black `[Answer: A]`).** Previous: **ROUND 467 BASELINE", 1)
so = so.replace(a11, "| `TABLETBWT_OFF` | 470 | **THE TABLE-CELL TITLE BAR RECOGNISES THE WRITERS TEMPLATE** (session 42 Round 8; the recognition lane). Reverts `content_start.table_title_bar_opener.recognise_wt`: a Writers Template whose every tag sits in table cells is refused as 'no Writers Template' again (TRR115 ships no pages); byte-identical to r467 on every other module. |\n" + a11, 1)
so = so.replace(a14, "- **Build:** `260620.35` (round 470 — **TRR115 CONVERTS** (the table-cell `[TITLE BAR]` recognises its Writers Template); `TABLETBWT_OFF`; scoped #4 since the r460 FULL; 4 new pages; skeleton 55.2245 % @ 2491, the pre-existing pairs exact).\n" + a14, 1)
wr(PO, so); print("OG ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r470.bak")
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
setv("build", '"260620.34"', '"260620.35"'); setv("round", "467", "470")
setv("claude_pages", "2675", "2679"); setv("paired_pages", "2487", "2491"); setv("gated_dirs", "530", "531")
insert_before("_note_r467", '    "_note_r470": "Round 470 (session 42 Round 8, 2026-09-24; the recognition lane) — TRR115 CONVERTS (TABLETBWT_OFF): 4 new pages / pairs; SCAFFOLD 55.2654 @ 2487 -> 55.2245 @ 2491 (the new pairs, mean 29.7 %, enter below the mean; the pre-existing pairs EXACT), >=50 1575 -> 1576, RAW 39.216 -> 39.194; cs exact 16709 -> 16757, missing 896 -> 903 (+7 on the new elements); clean 2584/2629 -> 2587/2633; leak 74/45 -> 75/46 (+1 NAMED: TRR115_1_0 the writer\'s black [Answer: A]); body EXACT; scoped #4 since the r460 FULL.",')
setv("mean_scaffold_pct", "55.27", "55.22"); setv("median_scaffold_pct", "56.3", str(MED)); setv("pages_ge_50", "1575", "1576")
setv("raw_mean_pct", "39.22", "39.19"); setv("pairs", "2487", "2491")
insert_before("_note_r467_state", '    "_note_r470_state": "r470 (TRR115 converts): SCAFFOLD 55.2245 @ 2491, RAW 39.194; 0 movers, 4 new pairs.",')
setv("exact_chain", "16709", "16757"); setv("claude_missing_container", "896", "903")
setv("clean_pages", "2584", "2587"); setv("total_pages", "2629", "2633"); setv("clean_pct", "98.29", "98.25")
setv("literal_tag_leak_occ", "74", "75"); setv("leak_pages", "45", "46")
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-r470-finalise.bak")
i = find("- **ROUND 470 IN FLIGHT — NOT PROVEN**"); marker = L[i].replace("24 Sept ≈17:30 real clock", "24 Sept 16:01 real clock")
k = find("**Session 42 started:**")
L[k] += (" **Clock note (16:20):** the ≈ times written on s42-r5 → r8 (≈15:40 / 16:00 / 17:00 / 17:30) ran 20–80 min ahead of the real clock "
         "(the commits: r467 15:24, R5 15:37, R6 15:50, R7 16:00; r470 started 16:01) — read the commit times.")
L[i] = ("- **No round in flight** (24 Sept 2026 ≈16:25 real clock, session 42 Round 8 — r470 (TRR115 converts) SHIPPED and committed; the "
        "in-flight marker is cleared). LAST SHIPPED **r470** (260620.35); **LAST FULL = r460**; ledger **scoped #4** since it (4 of headroom).")
k = find("- **Before r470: no round in flight**"); prior = L[k]; del L[k]
k = find("- LAST SHIPPED: **r467**"); L[k] = L[k].replace("- LAST SHIPPED: **r467**", "- Before it: **r467**", 1)
L.insert(k, "- LAST SHIPPED: **r470** (build 260620.35, 24 Sept ≈16:25, session 42 Round 8 — THE TABLE-CELL TITLE BAR RECOGNISES THE WRITERS "
         "TEMPLATE, `TABLETBWT_OFF`: **TRR115 converts** (4 pages); SCOPED, **scoped #4 since the r460 FULL**, committed NAMED (the r453 "
         "precedent); **skeleton 55.2654 % @ 2487 → 55.2245 % @ 2491 (−0.0410pp = the four new pairs, mean 29.7 %; the pre-existing pairs "
         "EXACT)**, ≥50 1576, ≥75 276, ≥90 25, RAW 39.194 %; cs 16757 / 208 / 903 / 24; body 61 / 5 / 175 / 238; clean 2587 / 2633; leak "
         "75 / 46 (+1 named, TRR115_1_0's black `[Answer: A]`); census Claude pages 2679; `gate_baseline.json` at r470; the miner 197 "
         "CANDIDATE @ 2491).")
k = find("- Plateau window (§4): **2 of 3** — r467")
L[k] = L[k].replace("- Plateau window (§4): **2 of 3** — r467", "- Plateau window (§4): **2 of 3** — r470 a recognition round (neither "
                    "counts nor resets); r467", 1)
k = find("- Standing facts: AppVersion 260620.34")
L[k] = L[k].replace("- Standing facts: AppVersion 260620.34 (r467", "- Standing facts: AppVersion 260620.35 (r470 TRR115 converts — "
                    "session 42 Round 8, 24 Sept); before it 260620.34 (r467", 1)
k = find("## Round log")
L.insert(k + 1, "- s42-r8 (engine r470, build 260620.35, 24 Sept 16:01 → ≈16:25 real clock) · THE TABLE-CELL TITLE BAR RECOGNISES THE WRITERS TEMPLATE: TRR115 converts (the recognition lane; every tag in table "
         "cells) · SHIPPED scoped #4, committed NAMED · 4 new pages (55.4 / 23.7 / 18.6 / 21.2 %) · skeleton 55.2654 → 55.2245 @ 2491 "
         "(population; the pre-existing pairs EXACT) · census 2675 → 2679 pages · plateau 2 of 3 (neither).")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r470** (260620.35, "
        "TRR115 converts); LAST FULL = **r460**; ledger scoped #4; plateau **2 of 3**; 2,491 pairs; census 552 / 545 / 2,679. Ride-along "
        "patches `_r469_declined.patch` (alerts) / `_r469b_declined.patch` (buttons). Needs Chris #17–#19, #22.")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Session 42 — Round 8 PICK (engine r470) + what shipped\n\n" + marker + "\n" + prior + "\n"
    "- **What shipped (r470, 260620.35):** `DocxExtractor.LooksLikeWritersTemplate` accepts a table cell whose red span resolves to "
    "`title bar` (data `content_start.table_title_bar_opener.recognise_wt`, env `TABLETBWT_OFF`); TRR115 converts (4 pages). Probe OFF "
    "3217 identical / ON 0 changed + 5 new outputs; committed NAMED (`_r470_fastloop_named.log`). TRR104 / TRR105 stay refused (a Media "
    "List only — correct).\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
