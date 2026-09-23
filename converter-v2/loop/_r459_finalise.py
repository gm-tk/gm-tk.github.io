#!/usr/bin/env python3
"""ROUND 459 finalise — gate_baseline.json (line edits) + LOOP_STATE.md (the r458 pattern). .pre-r459.bak / .pre-r459-finalise.bak
kept. Run under WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json")
shutil.copyfile(P, P + ".pre-r459.bak")
L = io.open(P, encoding="utf-8").read().split("\n")
def setv(key, old, new):
    for i, l in enumerate(L):
        if l.strip().startswith(f'"{key}": '):
            assert l.strip().rstrip(",") == f'"{key}": {old}', (key, l)
            L[i] = l.replace(f'"{key}": {old}', f'"{key}": {new}'); return i
    raise SystemExit(f"not found {key}")
def insert_before(key, line):
    for i, l in enumerate(L):
        if l.strip().startswith(f'"{key}": '):
            L.insert(i, line); return
    raise SystemExit(f"anchor not found {key}")
setv("build", '"260620.28"', '"260620.29"'); setv("round", "458", "459")
insert_before("_note_r458", '    "_note_r459": "Round 459 (session 41 Round 7, 2026-09-24; the page-model lane) — THE MODULE INTRODUCTION STAYS ON THE OVERVIEW: AR-1 now also recognises the introduction typed BLACK, glued to another tag, behind a CS instruction tag, or as a heading ([H2] Introduction / [H1] **INTRODUCTION** / [H3] **MODULE INTRODUCTION**) — page_split.intro_cluster_forms, INTROFORM_OFF — and a lesson heading after a merged introduction opens its page (the r456 opener on that overview). SCOPED ship #6 since the r452 FULL: 17 modules, pages 2691 -> 2675, pairs 2518 -> 2524. SCAFFOLD 54.9291 -> 54.9376 (+0.0085pp; the pre-existing pairs +0.0264pp), >=50 1578 -> 1581, >=75 270 -> 275, >=90 24 -> 25; cs matched 18925 -> 19467, exact 16282 -> 16719 (+437); body ANY 240 -> 239. NAMED: cs EXTRA 199 -> 208 and missing 860 -> 896 (all on the +542 newly compared introduction elements — HIS1002 +167 / +32 missing), clean 2637/2683 -> 2621/2667 (98.28: the 16 removed pages were all clean; unclean held at 46); dips COM1005_0_0 -10.8 / DAN1003_0_0 -6.8 (their humans render the introduction inside a module-menu tab — no #body), COM1006_2_0 -9.4, XDLS501_4 -4.8; lost pair TEDC402-9.0 (the old intro page; the overview rose 59.0 -> 81.6). _fastloop_diff --accept-named, outputs/_r459_fastloop_named.log.",')
setv("mean_scaffold_pct", "54.93", "54.94")
setv("pages_ge_50", "1578", "1581"); setv("pages_ge_75", "270", "275"); setv("pages_ge_90", "24", "25")
setv("raw_mean_pct", "38.92", "38.93"); setv("pairs", "2518", "2524")
insert_before("_note_r458_state", '    "_note_r459_state": "r459 (the introduction on the overview): SCAFFOLD 54.9291 @ 2518 -> 54.9376 @ 2524 (+0.0085pp; pre-existing +0.0264pp), RAW 38.917 -> 38.934; 27 new-only / 21 gone Claude pages, 0 movers outside the affected set. outputs/_r459_sk_final.json, _r459_skdelta.log, _r459_prescore2.log, _r459_split.py.",')
setv("exact_chain", "16282", "16719"); setv("claude_extra_container", "199", "208"); setv("claude_missing_container", "860", "896")
setv("any_breakdown", "240", "239"); setv("over_capture", "62", "61")
setv("clean_pages", "2637", "2621"); setv("total_pages", "2683", "2667"); setv("clean_pct", "98.29", "98.28")
out = "\n".join(L); json.loads(out)
tmp = P + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="\n").write(out); os.replace(tmp, P)
print("gate_baseline.json -> r459")
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
shutil.copyfile(S, S + ".pre-r459-finalise.bak")
s = io.open(S, encoding="utf-8").read(); L = s.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
i = find("- **ROUND 459 IN FLIGHT — NOT PROVEN**"); j = find("- Before r459: **no round in flight**"); assert j == i + 1
marker = L[i]
L[i:j + 1] = ["- **No round in flight** (24 Sept 2026 ≈11:00, session 41 Round 7 — r459 SHIPPED and committed; the in-flight marker is cleared). LAST SHIPPED **r459** (260620.29); **LAST FULL = the r452 state**; ledger **scoped #6** since it (2 of headroom — the FULL backstop is due within two ships)."]
k = find("- LAST SHIPPED: **r458**")
L[k] = "- Before it: **r458** (260620.28, a placement note is not a page boundary, +0.0324pp; 5 modules) — gate row in BUILD_CHANGELOG.md round 458."
L.insert(k, "- LAST SHIPPED: **r459** (build 260620.29, 24 Sept ≈10:57, session 41 Round 7 — THE MODULE INTRODUCTION STAYS ON THE OVERVIEW, `INTROFORM_OFF`; 17 modules, pages 2691 → 2675; SCOPED, **scoped #6 since the r452 FULL**; **skeleton 54.9291 % @ 2518 → 54.9376 % @ 2524 (+0.0085pp; the pre-existing pairs +0.0264pp)**, **≥50 1581** (+3), **≥75 275** (+5), ≥90 25, RAW 38.934 %; cs 16719 / 208 / 896 / 24 (exact +437; EXTRA +9 / missing +36 NAMED); body 61 / 5 / 176 / 239 (−1); clean 2621 / 2667 (NAMED); leak 75 / 46; `gate_baseline.json` at r459; the miner 197 CANDIDATE @ 2524).")
k = find("- Plateau window (§4): **0 of 3** — r458")
L[k] = L[k].replace("- Plateau window (§4): **0 of 3** — r458", "- Plateau window (§4): **0 of 3** — r459 delivered +0.0085pp on the grown population but +0.0264pp on the pre-existing pairs with ≥50 +3 / ≥75 +5 (read on the pre-existing population, §1e: moved); r458", 1)
k = find("- Standing facts: AppVersion 260620.28")
L[k] = L[k].replace("- Standing facts: AppVersion 260620.28 (r458", "- Standing facts: AppVersion 260620.29 (r459 the introduction on the overview — session 41 Round 7, 24 Sept); before it 260620.28 (r458", 1)
k = find("## Round log")
L.insert(k + 1, "- s41-r7 (engine r459, build 260620.29, 24 Sept ≈10:45 → ≈11:00) · THE MODULE INTRODUCTION STAYS ON THE OVERVIEW (AR-1 missed the black / glued / behind-an-instruction / heading forms of the introduction marker; the intro shipped as its own page 1.0 in 17 modules) · `INTROFORM_OFF` · SHIPPED · scaffold 54.9291 @ 2518 → 54.9376 @ 2524 (pre-existing +0.0264pp), ≥50 +3, ≥75 +5, cs exact +437 · in-round repair: DAN1004's lessons 1–2 fell onto the overview → the r456 opener allowed after a merged intro · three movers NAMED · scoped #6.")
k = find("**Next session starts with:**")
L[k] = L[k].replace("census 552 / 545 / **2,691** pages / **2,518** pairs", "census 552 / 545 / **2,675** pages / **2,524** pairs", 1).replace("LAST SHIPPED **r458** (260620.28); LAST FULL = the **r452 state**; ledger scoped #5;", "LAST SHIPPED **r459** (260620.29); LAST FULL = the **r452 state**; ledger scoped #6;", 1)
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## Session 41 — Round 7 PICK (engine r459) + what shipped\n\n" + marker + "\n- **What shipped (r459, 260620.29):** AR-1's overview peek recognises `intro_cluster_forms` (black / embedded / heading; unresolved tags looked past); a merged intro marks the overview `_introMerged`, which lets the r456 mid-page opener fire there. OFF identical; ON 135 pages / 17 modules; first probe DAN1004 −26 on its overview + 2 lost pairs (lessons 1–2 merged into the overview) → the opener after a merged intro; final pre-existing pairs +70.0 pp-sum; scoped regen 17 + 12; disk = probe 152 / 152; decomposition: skeleton +0.01 / ≥50 +3 / ≥75 +5 / cs exact +437 / body −1 IMPROVED, EXTRA +9 / missing +36 / clean −0.01 NAMED; post-ship green.\n")
out = "\n".join(L); tmp = S + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="\n").write(out); os.replace(tmp, S)
print("LOOP_STATE.md", len(s.encode("utf-8")), "->", os.path.getsize(S))
