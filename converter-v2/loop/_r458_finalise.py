#!/usr/bin/env python3
"""ROUND 458 finalise — gate_baseline.json (line edits) + LOOP_STATE.md (the r457 pattern). .pre-r458.bak / .pre-r458-finalise.bak
kept. Run under WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json")
shutil.copyfile(P, P + ".pre-r458.bak")
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
setv("build", '"260620.27"', '"260620.28"'); setv("round", "457", "458")
insert_before("_note_r457", '    "_note_r458": "Round 458 (session 41 Round 6, 2026-09-24; the page-model lane — the over-split census) — A PLACEMENT NOTE IS NOT A PAGE BOUNDARY: \'[Kōwhai Avatar – right hand side of the page]\', \'[Insert bookworm on right side of page …]\' (BLLR201–203), \'[Create two new colour boxes to go on the side of the page …]\' (ART1006) and HIS1001\'s \'on the left of the whole page\' no longer open pages (r245 lesson_boundary_guard.deny_position_pattern, POSNOTE_OFF). SCOPED ship #5 since the r452 FULL: 5 modules, pages 2700 -> 2691, pairs 2519 -> 2518 (ART1006_4.0 lost — that module\'s human restructured its pages). SCAFFOLD 54.8967 -> 54.9291 (+0.0324pp; the pre-existing pairs +46.1 pp-sum, 0 dips), >=50 1577 -> 1578; cs exact 16045 -> 16282 (+237, matched +261). NAMED: cs missing 847 -> 860 (+13 on the +261 newly matched BLLR elements), clean 2646/2692 -> 2637/2683 (98.29: the 9 removed pages were all clean; unclean held at 46). _fastloop_diff --accept-named, outputs/_r458_fastloop_named.log.",')
setv("mean_scaffold_pct", "54.9", "54.93"); setv("median_scaffold_pct", "55.96", "56.0")
setv("pages_ge_50", "1577", "1578"); setv("raw_mean_pct", "38.9", "38.92"); setv("pairs", "2519", "2518")
insert_before("_note_r457_state", '    "_note_r458_state": "r458 (the placement note): SCAFFOLD 54.8967 @ 2519 -> 54.9291 @ 2518 (+0.0324pp), RAW 38.896 -> 38.917; the pre-existing pairs +46.1 pp-sum with 0 dips by gold page (outputs/_r458_split.py); 0 movers outside the affected set. outputs/_r458_sk_final.json, _r458_skdelta.log, _r458_prescore.log.",')
setv("exact_chain", "16045", "16282"); setv("claude_missing_container", "847", "860")
setv("clean_pages", "2646", "2637"); setv("total_pages", "2692", "2683")
out = "\n".join(L); json.loads(out)
tmp = P + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="\n").write(out); os.replace(tmp, P)
print("gate_baseline.json -> r458")
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
shutil.copyfile(S, S + ".pre-r458-finalise.bak")
s = io.open(S, encoding="utf-8").read(); L = s.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
i = find("- **ROUND 458 IN FLIGHT — NOT PROVEN**"); j = find("- Before r458: **no round in flight**"); assert j == i + 1
marker = L[i]
L[i:j + 1] = ["- **No round in flight** (24 Sept 2026 ≈10:40, session 41 Round 6 — r458 SHIPPED and committed; the in-flight marker is cleared). LAST SHIPPED **r458** (260620.28); **LAST FULL = the r452 state**; ledger **scoped #5** since it (3 of headroom)."]
k = find("- LAST SHIPPED: **r457**")
L[k] = "- Before it: **r457** (260620.27, the section-label marker is not a page boundary, +0.0263pp, ≥50 +2; 3 modules) — gate row in BUILD_CHANGELOG.md round 457."
L.insert(k, "- LAST SHIPPED: **r458** (build 260620.28, 24 Sept ≈10:35, session 41 Round 6 — A PLACEMENT NOTE IS NOT A PAGE BOUNDARY, `POSNOTE_OFF`; 5 modules (ART1006 / BLLR201–203 / HIS1001), pages 2700 → 2691; SCOPED, **scoped #5 since the r452 FULL**; **skeleton 54.8967 % @ 2519 → 54.9291 % @ 2518 (+0.0324pp)**, ≥50 1578, ≥75 270, ≥90 24, RAW 38.917 %; cs 16282 / 199 / 860 / 24 (exact +237; missing +13 NAMED); body 62 / 5 / 176 / 240; clean 2637 / 2683 (NAMED); leak 75 / 46; `gate_baseline.json` at r458; the miner 196 CANDIDATE @ 2518).")
k = find("- Plateau window (§4): **0 of 3** — r457")
L[k] = L[k].replace("- Plateau window (§4): **0 of 3** — r457", "- Plateau window (§4): **0 of 3** — r458 predicted a move and delivered +0.0324pp; r457", 1)
k = find("- Standing facts: AppVersion 260620.27")
L[k] = L[k].replace("- Standing facts: AppVersion 260620.27 (r457", "- Standing facts: AppVersion 260620.28 (r458 the placement note — session 41 Round 6, 24 Sept); before it 260620.27 (r457", 1)
k = find("## Round log")
L.insert(k + 1, "- s41-r6 (engine r458, build 260620.28, 24 Sept ≈10:28 → ≈10:40) · A PLACEMENT NOTE IS NOT A PAGE BOUNDARY (`[Kōwhai Avatar – right hand side of the page]`, `[Insert bookworm on right side of page …]` — the embedded `page` word is a position) · `POSNOTE_OFF`, 5 modules, 29 pages, −9 files · SHIPPED · scaffold 54.8967 → 54.9291 (+0.0324pp), ≥50 +1, cs exact +237 · two movers NAMED · scoped #5.")
k = find("**Next session starts with:**")
L[k] = L[k].replace("census 552 / 545 / **2,700** pages / **2,519** pairs", "census 552 / 545 / **2,691** pages / **2,518** pairs", 1).replace("LAST SHIPPED **r457** (260620.27); LAST FULL = the **r452 state**; ledger scoped #4;", "LAST SHIPPED **r458** (260620.28); LAST FULL = the **r452 state**; ledger scoped #5;", 1)
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## Session 41 — Round 6 PICK (engine r458) + what shipped\n\n" + marker + "\n- **What shipped (r458, 260620.28):** the r245 guard's `deny_position_pattern`; OFF identical; ON 29 pages / 5 modules; the pre-existing pairs +46.1 pp-sum, 0 dips; scoped regen 5 + 12; disk = probe 40 / 40; decomposition: skeleton +0.03 / ≥50 +1 / cs exact +237 IMPROVED, missing +13 / clean −0.01 NAMED; post-ship green.\n")
out = "\n".join(L); tmp = S + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="\n").write(out); os.replace(tmp, S)
print("LOOP_STATE.md", len(s.encode("utf-8")), "->", os.path.getsize(S))
